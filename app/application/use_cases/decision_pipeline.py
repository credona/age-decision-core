from app.application.ports.event_logger import EventLoggerPort, NullEventLogger
from app.application.ports.face_cropper import FaceCropperPort
from app.application.ports.image_decoder import ImageDecoderPort
from app.application.ports.inference_engine import InferenceEnginePort
from app.application.ports.input_analyzer import InputAnalyzerPort
from app.application.ports.input_preprocessor import InputPreprocessorPort
from app.domain.decision.constants import (
    DECISION_UNCERTAIN,
    ENGINE_UNKNOWN,
    LOG_EVENT_AGE_DECISION_COMPLETED,
    SPOOF_CHECK_STATUS_REQUIRED,
    THRESHOLD_POLICY_TYPE_MINIMUM_AGE,
)
from app.domain.decision.policy import DecisionPolicy
from app.domain.decision.score import CredScoreCalculator
from app.domain.policies.country_rules import CountryRules
from app.domain.privacy.metadata import PrivacyMetadataBuilder
from app.domain.proof.metadata import ProofMetadataBuilder
from app.domain.scoring.policy import default_age_scoring_policy


class DecisionPipeline:
    def __init__(
        self,
        inference_engine: InferenceEnginePort,
        input_analyzer: InputAnalyzerPort,
        image_decoder: ImageDecoderPort,
        face_cropper: FaceCropperPort,
        input_preprocessor: InputPreprocessorPort,
        event_logger: EventLoggerPort | None = None,
    ):
        self.scoring_policy = default_age_scoring_policy()
        self.country_rules = CountryRules()
        self.decision_policy = DecisionPolicy(self.scoring_policy)
        self.cred_score_calculator = CredScoreCalculator(self.scoring_policy)
        self.privacy_builder = PrivacyMetadataBuilder()
        self.proof_builder = ProofMetadataBuilder()

        self.input_analyzer = input_analyzer
        self.image_decoder = image_decoder
        self.face_cropper = face_cropper
        self.input_preprocessor = input_preprocessor
        self.inference_engine = inference_engine
        self.event_logger = event_logger or NullEventLogger()

    def get_engine_status(self) -> dict:
        return {
            "input_analysis": self.input_analyzer.get_status(),
            "inference": self.inference_engine.get_status(),
        }

    async def run(
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

        image = self.image_decoder.decode(image_bytes)
        faces = self.input_analyzer.detect(image)
        face_count = len(faces)

        if face_count == 0:
            return self._uncertain_response(request_id, correlation_id, threshold, 0, "no_face")

        if face_count > 1:
            return self._uncertain_response(
                request_id, correlation_id, threshold, face_count, "multiple_faces"
            )

        face = self.face_cropper.crop(image, faces)
        prepared_input = self.input_preprocessor.preprocess(face)
        internal_estimate, signal_quality_score = self.inference_engine.predict(prepared_input)

        decision, rejection_reason = self.decision_policy.compute(
            age=internal_estimate,
            signal_quality_score=signal_quality_score,
            threshold=threshold_value,
        )

        cred_decision_score = self.cred_score_calculator.compute(
            decision=decision,
            signal_quality_score=signal_quality_score,
            internal_estimate=internal_estimate,
            threshold=threshold_value,
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
            "privacy": self.privacy_builder.build(zk_ready=True),
            "proof": self.proof_builder.build(enabled=True, threshold=threshold),
            "rejection_reason": rejection_reason,
            "engine_info": self._build_engine_info(),
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

        return self.scoring_policy.age_threshold, "default"

    def _build_threshold_policy(self, value, source, majority_country):
        return {
            "type": THRESHOLD_POLICY_TYPE_MINIMUM_AGE,
            "value": value,
            "source": source,
            "majority_country": majority_country.upper() if majority_country else None,
        }

    def _build_engine_info(self):
        return {
            "input_analyzer": self.input_analyzer.get_status().get("engine", ENGINE_UNKNOWN),
            "inference_engine": self.inference_engine.get_status().get("engine", ENGINE_UNKNOWN),
        }

    def _build_spoof_check(self):
        return {
            "status": SPOOF_CHECK_STATUS_REQUIRED,
            "passed": None,
            "provider": None,
        }

    def _uncertain_response(self, request_id, correlation_id, threshold, face_count, reason):
        return {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "decision": DECISION_UNCERTAIN,
            "threshold": threshold,
            "face_detected": face_count > 0,
            "face_count": face_count,
            "spoof_check_required": True,
            "spoof_check": self._build_spoof_check(),
            "cred_decision_score": self.cred_score_calculator.compute(
                decision=DECISION_UNCERTAIN,
                signal_quality_score=None,
                internal_estimate=None,
                threshold=threshold["value"],
            ),
            "privacy": self.privacy_builder.build(zk_ready=True),
            "proof": self.proof_builder.build(enabled=True, threshold=threshold),
            "rejection_reason": reason,
            "engine_info": self._build_engine_info(),
        }

    def _log(self, response: dict) -> None:
        self.event_logger.info(
            {
                "event": LOG_EVENT_AGE_DECISION_COMPLETED,
                "decision": response["decision"],
                "face_count": response["face_count"],
            }
        )
