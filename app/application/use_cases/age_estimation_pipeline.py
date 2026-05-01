from app.application.ports.age_predictor import AgePredictorPort
from app.application.ports.face_detector import FaceDetectorPort
from app.domain.decision.policy import DecisionPolicy
from app.domain.decision.score import CredScoreCalculator
from app.domain.policies.country_rules import CountryRules
from app.domain.privacy.metadata import PrivacyMetadataBuilder
from app.domain.proof.metadata import ProofMetadataBuilder
from app.infrastructure.config.settings import settings
from app.infrastructure.logging.safe_logger import get_logger, log_event
from app.infrastructure.vision.face_cropper import FaceCropper
from app.infrastructure.vision.face_preprocessor import FacePreprocessor
from app.infrastructure.vision.opencv_image_loader import load_image_from_bytes


class AgeEstimationService:
    """
    Application service (orchestration).

    Infrastructure dependencies are injected via ports.
    """

    def __init__(
        self,
        age_predictor: AgePredictorPort,
        face_detector: FaceDetectorPort,
    ):
        self.default_age_threshold = settings.age_threshold
        self.default_age_margin = settings.age_margin
        self.default_confidence_threshold = settings.confidence_threshold

        self.country_rules = CountryRules()
        self.decision_policy = DecisionPolicy()
        self.cred_score_calculator = CredScoreCalculator()
        self.privacy_builder = PrivacyMetadataBuilder()
        self.proof_builder = ProofMetadataBuilder()

        self.face_detector = face_detector
        self.face_cropper = FaceCropper()
        self.face_preprocessor = FacePreprocessor()
        self.age_predictor = age_predictor

        self.logger = get_logger()

    def get_model_status(self) -> dict:
        return {
            "face_detection": self.face_detector.get_status(),
            "age_estimation": self.age_predictor.get_status(),
        }

    async def estimate(
        self,
        image_bytes: bytes,
        content_type: str | None,
        request_id: str,
        correlation_id: str,
        age_threshold: int | None = None,
        majority_country: str | None = None,
    ) -> dict:
        self._validate_file(content_type, image_bytes)

        threshold_value, threshold_source = self._resolve_threshold(
            age_threshold=age_threshold,
            majority_country=majority_country,
        )

        threshold = self._build_threshold_policy(
            value=threshold_value,
            source=threshold_source,
            majority_country=majority_country,
        )

        image = load_image_from_bytes(image_bytes)

        faces = self.face_detector.detect(image)
        face_count = len(faces)

        if face_count == 0:
            return self._uncertain_response(request_id, correlation_id, threshold, 0, "no_face")

        if face_count > 1:
            return self._uncertain_response(
                request_id, correlation_id, threshold, face_count, "multiple_faces"
            )

        face = self.face_cropper.crop(image, faces)
        face_tensor = self.face_preprocessor.preprocess(face)

        estimated_age, confidence = self.age_predictor.predict(face_tensor)

        decision, rejection_reason = self.decision_policy.compute(
            age=estimated_age,
            confidence=confidence,
            threshold=threshold_value,
            margin=self.default_age_margin,
            confidence_threshold=self.default_confidence_threshold,
        )

        cred_decision_score = self.cred_score_calculator.compute(
            decision=decision,
            confidence=confidence,
            estimated_age=estimated_age,
            threshold=threshold_value,
            margin=self.default_age_margin,
        )

        response = {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "decision": decision,
            "threshold": threshold,
            "face_detected": True,
            "face_count": face_count,
            "spoof_check_required": True,
            "spoof_check": self._build_spoof_check(),
            "cred_decision_score": cred_decision_score,
            "privacy": self.privacy_builder.build(
                zk_ready=settings.enable_zk_ready,
            ),
            "proof": self.proof_builder.build(
                enabled=settings.enable_zk_ready,
                threshold=threshold,
            ),
            "rejection_reason": rejection_reason,
            "model_info": self._build_model_info(),
        }

        self._log(response)

        return response

    def _validate_file(self, content_type: str | None, image_bytes: bytes) -> None:
        if not image_bytes:
            raise ValueError("Empty file.")

        if content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError("Unsupported file type.")

    def _resolve_threshold(self, age_threshold, majority_country):
        if age_threshold is not None:
            return age_threshold, "explicit"

        country_threshold = self.country_rules.get_threshold(majority_country)

        if country_threshold is not None:
            return country_threshold, "majority_country"

        return self.default_age_threshold, "default"

    def _build_threshold_policy(self, value, source, majority_country):
        return {
            "type": "minimum_age",
            "value": value,
            "source": source,
            "majority_country": majority_country.upper() if majority_country else None,
        }

    def _build_model_info(self):
        return {
            "face_detector": "YuNet",
            "age_estimator": "age-gender-prediction-ONNX",
            "age_model_path": settings.age_model_path,
            "face_detection_model_path": settings.face_detection_model_path,
        }

    def _build_spoof_check(self):
        return {
            "status": "required",
            "passed": None,
            "provider": None,
        }

    def _uncertain_response(self, request_id, correlation_id, threshold, face_count, reason):
        return {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "decision": "uncertain",
            "threshold": threshold,
            "face_detected": face_count > 0,
            "face_count": face_count,
            "spoof_check_required": True,
            "spoof_check": self._build_spoof_check(),
            "cred_decision_score": self.cred_score_calculator.compute(
                decision="uncertain",
                confidence=None,
                estimated_age=None,
                threshold=threshold["value"],
                margin=self.default_age_margin,
            ),
            "privacy": self.privacy_builder.build(
                zk_ready=settings.enable_zk_ready,
            ),
            "proof": self.proof_builder.build(
                enabled=settings.enable_zk_ready,
                threshold=threshold,
            ),
            "rejection_reason": reason,
            "model_info": self._build_model_info(),
        }

    def _log(self, response: dict) -> None:
        log_event(
            self.logger,
            {
                "event": "age_decision_completed",
                "decision": response["decision"],
                "face_count": response["face_count"],
            },
        )
