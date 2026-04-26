from typing import Literal

from pydantic import BaseModel


class RequestPolicy(BaseModel):
    threshold_source: Literal["explicit", "country", "default"]
    country: str | None
    threshold: int
    age_margin: int
    confidence_threshold: float


class ModelInfo(BaseModel):
    face_detector: str
    age_estimator: str
    age_model_path: str
    face_detection_model_path: str


class SpoofCheck(BaseModel):
    status: Literal["required", "not_available"]
    passed: bool | None
    provider: str | None


class CredScoreFactors(BaseModel):
    age_confidence: float | None
    threshold_distance: float | None


class CredScore(BaseModel):
    score: float
    level: Literal["high", "medium", "low", "none"]
    factors: CredScoreFactors


class PrivacyMetadata(BaseModel):
    image_stored: bool
    biometric_template_stored: bool
    processing: Literal["ephemeral"]
    zk_ready: bool


class ProofMetadata(BaseModel):
    type: Literal["none", "zk-ready"]
    status: Literal["disabled", "not_generated"]
    claim: str | None
    threshold: int


class AgeDecisionResponse(BaseModel):
    request_id: str
    correlation_id: str

    estimated_age: float | None
    confidence: float | None
    is_adult: bool | None
    decision: Literal["adult", "minor", "unknown"]

    threshold: int
    age_margin: int
    confidence_threshold: float
    country: str | None

    face_detected: bool
    face_count: int

    spoof_check_required: bool
    spoof_check: SpoofCheck

    cred_score: CredScore
    privacy: PrivacyMetadata
    proof: ProofMetadata

    rejection_reason: Literal[
        "low_confidence",
        "age_uncertain",
        "no_face",
        "multiple_faces",
        None,
    ]

    request_policy: RequestPolicy
    model_info: ModelInfo