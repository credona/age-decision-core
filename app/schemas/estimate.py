from typing import Literal

from pydantic import BaseModel


class ThresholdPolicy(BaseModel):
    type: Literal["minimum_age"]
    value: int
    source: Literal["explicit", "majority_country", "default"]
    majority_country: str | None


class ModelInfo(BaseModel):
    face_detector: str
    age_estimator: str
    age_model_path: str
    face_detection_model_path: str


class SpoofCheck(BaseModel):
    status: Literal["required", "not_available"]
    passed: bool | None
    provider: str | None


class CredDecisionScoreFactors(BaseModel):
    model_confidence: Literal["high", "medium", "low", "none"]
    threshold_separation: Literal["high", "medium", "low", "none"]


class CredDecisionScore(BaseModel):
    score: float
    level: Literal["high", "medium", "low", "none"]
    factors: CredDecisionScoreFactors


class PrivacyMetadata(BaseModel):
    image_stored: bool
    biometric_template_stored: bool
    estimated_age_exposed: bool
    processing: Literal["ephemeral"]
    zk_ready: bool


class ProofMetadata(BaseModel):
    type: Literal["none", "zk-ready"]
    status: Literal["disabled", "not_generated"]
    claim: str | None
    threshold: ThresholdPolicy


class AgeDecisionResponse(BaseModel):
    request_id: str
    correlation_id: str

    decision: Literal["match", "no_match", "uncertain"]
    threshold: ThresholdPolicy

    face_detected: bool
    face_count: int

    spoof_check_required: bool
    spoof_check: SpoofCheck

    cred_decision_score: CredDecisionScore

    privacy: PrivacyMetadata
    proof: ProofMetadata

    rejection_reason: Literal[
        "low_confidence",
        "threshold_uncertain",
        "no_face",
        "multiple_faces",
        None,
    ]

    model_info: ModelInfo
