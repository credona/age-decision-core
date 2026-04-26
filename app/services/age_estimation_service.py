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
    Main age decision pipeline.

    The pipeline is privacy-first:
    - raw images are processed in memory only;
    - raw images are not stored;
    - biometric templates are not stored;
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
        age_margin: int | None = None,
        confidence_threshold: float | None = None,
        country: str | None = None,
    ) -> dict:
        image_bytes = await file.read()

        self._validate_file(file=file, image_bytes=image_bytes)

        threshold, threshold_source = self._resolve_threshold(age_threshold, country)
        margin = age_margin or self.default_age_margin
        conf_threshold = confidence_threshold or self.default_confidence_threshold

        image = load_image_from_bytes(image_bytes)

        faces = self.face_detector.detect(image)
        face_count = len(faces)

        if face_count == 0:
            response = self._unknown_response(
                request_id=request_id,
                correlation_id=correlation_id,
                threshold=threshold,
                margin=margin,
                confidence_threshold=conf_threshold,
                country=country,
                threshold_source=threshold_source,
                face_count=0,
                rejection_reason="no_face",
            )
            self._log(response)
            return response

        if face_count > 1:
            response = self._unknown_response(
                request_id=request_id,
                correlation_id=correlation_id,
                threshold=threshold,
                margin=margin,
                confidence_threshold=conf_threshold,
                country=country,
                threshold_source=threshold_source,
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
            threshold=threshold,
            margin=margin,
            confidence_threshold=conf_threshold,
        )

        is_adult = None

        if decision == "adult":
            is_adult = True
        elif decision == "minor":
            is_adult = False

        cred_decision_score = self.cred_score_calculator.compute(
            decision=decision,
            confidence=confidence,
            estimated_age=estimated_age,
            threshold=threshold,
            margin=margin,
        )

        response = {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "estimated_age": estimated_age,
            "confidence": confidence,
            "is_adult": is_adult,
            "decision": decision,
            "threshold": threshold,
            "age_margin": margin,
            "confidence_threshold": conf_threshold,
            "country": country.upper() if country else None,
            "face_detected": True,
            "face_count": face_count,
            "spoof_check_required": True,
            "spoof_check": self._build_spoof_check(),
            "cred_decision_score": cred_decision_score,
            "cred_score": cred_decision_score,
            "privacy": self.privacy_builder.build(
                zk_ready=settings.enable_zk_ready,
            ),
            "proof": self.proof_builder.build(
                enabled=settings.enable_zk_ready,
                threshold=threshold,
            ),
            "rejection_reason": rejection_reason,
            "request_policy": self._build_request_policy(
                threshold_source=threshold_source,
                country=country,
                threshold=threshold,
                margin=margin,
                confidence_threshold=conf_threshold,
            ),
            "model_info": self._build_model_info(),
        }

        self._log(response)

        return response

    def _unknown_response(
        self,
        request_id: str,
        correlation_id: str,
        threshold: int,
        margin: int,
        confidence_threshold: float,
        country: str | None,
        threshold_source: str,
        face_count: int,
        rejection_reason: str,
    ) -> dict:
        cred_decision_score = self.cred_score_calculator.compute(
            decision="unknown",
            confidence=None,
            estimated_age=None,
            threshold=threshold,
            margin=margin,
        )

        return {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "estimated_age": None,
            "confidence": None,
            "is_adult": None,
            "decision": "unknown",
            "threshold": threshold,
            "age_margin": margin,
            "confidence_threshold": confidence_threshold,
            "country": country.upper() if country else None,
            "face_detected": face_count > 0,
            "face_count": face_count,
            "spoof_check_required": True,
            "spoof_check": self._build_spoof_check(),
            "cred_decision_score": cred_decision_score,
            "cred_score": cred_decision_score,
            "privacy": self.privacy_builder.build(
                zk_ready=settings.enable_zk_ready,
            ),
            "proof": self.proof_builder.build(
                enabled=settings.enable_zk_ready,
                threshold=threshold,
            ),
            "rejection_reason": rejection_reason,
            "request_policy": self._build_request_policy(
                threshold_source=threshold_source,
                country=country,
                threshold=threshold,
                margin=margin,
                confidence_threshold=confidence_threshold,
            ),
            "model_info": self._build_model_info(),
        }

    def _resolve_threshold(self, age_threshold: int | None, country: str | None) -> tuple[int, str]:
        if age_threshold is not None:
            return age_threshold, "explicit"

        country_threshold = self.country_rules.get_threshold(country)

        if country_threshold is not None:
            return country_threshold, "country"

        return self.default_age_threshold, "default"

    def _build_request_policy(
        self,
        threshold_source: str,
        country: str | None,
        threshold: int,
        margin: int,
        confidence_threshold: float,
    ) -> dict:
        return {
            "threshold_source": threshold_source,
            "country": country.upper() if country else None,
            "threshold": threshold,
            "age_margin": margin,
            "confidence_threshold": confidence_threshold,
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
                "threshold": response["threshold"],
                "country": response["country"],
                "face_count": response["face_count"],
                "confidence": response["confidence"],
                "estimated_age": response["estimated_age"],
                "cred_decision_score": response["cred_decision_score"]["score"],
                "cred_decision_score_level": response["cred_decision_score"]["level"],
                "spoof_check_required": response["spoof_check_required"],
                "spoof_check_status": response["spoof_check"]["status"],
                "privacy_mode": settings.privacy_mode,
                "zk_ready": settings.enable_zk_ready,
            },
        )