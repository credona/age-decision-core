from fastapi import UploadFile

from app.config import settings
from app.domain.cred_score import CredScoreCalculator
from app.domain.decision_policy import DecisionPolicy
from app.domain.privacy import PrivacyMetadataBuilder
from app.domain.proof import ProofMetadataBuilder
from app.models.age_predictor import AgePredictor
from app.policies.country_rules import CountryRules
from app.utils.logger import get_logger, log_event
from app.vision.face_cropper import FaceCropper
from app.vision.face_detector import FaceDetector
from app.vision.face_preprocessor import FacePreprocessor
from app.vision.image_loader import load_image_from_bytes


class AgeEstimationService:
    """
    Main age threshold decision pipeline.

    The pipeline is privacy-first:
    - raw images are processed in memory only;
    - raw images are not stored;
    - biometric templates are not stored;
    - estimated age is never exposed in public responses;
    - logs must only contain safe metadata.
    """

    def __init__(self):
        self.default_age_threshold = settings.age_threshold
        self.default_age_margin = settings.age_margin
        self.default_confidence_threshold = settings.confidence_threshold

        self.country_rules = CountryRules()
        self.decision_policy = DecisionPolicy()
        self.cred_score_calculator = CredScoreCalculator()
        self.privacy_builder = PrivacyMetadataBuilder()
        self.proof_builder = ProofMetadataBuilder()

        self.face_detector = FaceDetector()
        self.face_cropper = FaceCropper()
        self.face_preprocessor = FacePreprocessor()
        self.age_predictor = AgePredictor()

        self.logger = get_logger()

    def get_model_status(self) -> dict:
        return {
            "face_detection": self.face_detector.get_status(),
            "age_estimation": self.age_predictor.get_status(),
        }

    async def estimate(
        self,
        file: UploadFile,
        request_id: str,
        correlation_id: str,
        age_threshold: int | None = None,
        majority_country: str | None = None,
    ) -> dict:
        image_bytes = await file.read()

        self._validate_file(file=file, image_bytes=image_bytes)

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
            response = self._uncertain_response(
                request_id=request_id,
                correlation_id=correlation_id,
                threshold=threshold,
                face_count=0,
                rejection_reason="no_face",
            )
            self._log(response)
            return response

        if face_count > 1:
            response = self._uncertain_response(
                request_id=request_id,
                correlation_id=correlation_id,
                threshold=threshold,
                face_count=face_count,
                rejection_reason="multiple_faces",
            )
            self._log(response)
            return response

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

    def _uncertain_response(
        self,
        request_id: str,
        correlation_id: str,
        threshold: dict,
        face_count: int,
        rejection_reason: str,
    ) -> dict:
        cred_decision_score = self.cred_score_calculator.compute(
            decision="uncertain",
            confidence=None,
            estimated_age=None,
            threshold=threshold["value"],
            margin=self.default_age_margin,
        )

        return {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "decision": "uncertain",
            "threshold": threshold,
            "face_detected": face_count > 0,
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

    def _resolve_threshold(
        self,
        age_threshold: int | None,
        majority_country: str | None,
    ) -> tuple[int, str]:
        if age_threshold is not None:
            return age_threshold, "explicit"

        country_threshold = self.country_rules.get_threshold(majority_country)

        if country_threshold is not None:
            return country_threshold, "majority_country"

        return self.default_age_threshold, "default"

    def _build_threshold_policy(
        self,
        value: int,
        source: str,
        majority_country: str | None,
    ) -> dict:
        return {
            "type": "minimum_age",
            "value": value,
            "source": source,
            "majority_country": majority_country.upper() if majority_country else None,
        }

    def _build_model_info(self) -> dict:
        return {
            "face_detector": "YuNet",
            "age_estimator": "age-gender-prediction-ONNX",
            "age_model_path": settings.age_model_path,
            "face_detection_model_path": settings.face_detection_model_path,
        }

    def _build_spoof_check(self) -> dict:
        return {
            "status": "required",
            "passed": None,
            "provider": None,
        }

    def _validate_file(self, file: UploadFile, image_bytes: bytes) -> None:
        if not image_bytes:
            raise ValueError("Empty file.")

        if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError("Unsupported file type.")

    def _log(self, response: dict) -> None:
        log_event(
            self.logger,
            {
                "level": "info",
                "event": "age_decision_completed",
                "request_id": response["request_id"],
                "correlation_id": response["correlation_id"],
                "decision": response["decision"],
                "rejection_reason": response["rejection_reason"],
                "threshold_type": response["threshold"]["type"],
                "threshold_value": response["threshold"]["value"],
                "threshold_source": response["threshold"]["source"],
                "majority_country": response["threshold"]["majority_country"],
                "face_count": response["face_count"],
                "cred_decision_score": response["cred_decision_score"]["score"],
                "cred_decision_score_level": response["cred_decision_score"]["level"],
                "spoof_check_required": response["spoof_check_required"],
                "spoof_check_status": response["spoof_check"]["status"],
                "privacy_mode": settings.privacy_mode,
                "zk_ready": settings.enable_zk_ready,
            },
        )
