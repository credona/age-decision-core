from typing import Literal

from pydantic import BaseModel


class ThresholdPolicy(BaseModel):
    type: Literal["minimum_age"]
    value: int
    source: Literal["explicit", "majority_country", "default"]
    majority_country: str | None


class EngineInfo(BaseModel):
    input_analyzer: str
    inference_engine: str


class SpoofCheck(BaseModel):
    status: Literal["required", "not_available"]
    passed: bool | None
    provider: str | None


class CredDecisionScoreFactors(BaseModel):
    signal_quality: Literal["high", "medium", "low", "none"]
    threshold_separation: Literal["high", "medium", "low", "none"]


class CredDecisionScore(BaseModel):
    score: float
    level: Literal["high", "medium", "low", "none"]
    factors: CredDecisionScoreFactors


class PrivacyMetadata(BaseModel):
    image_stored: bool
    biometric_template_stored: bool
    internal_estimate_exposed: bool
    processing: Literal["ephemeral"]
    zk_ready: bool


class ProofMetadata(BaseModel):
    type: Literal["none", "zk-ready"]
    status: Literal["disabled", "not_generated"]
    claim: str | None
    threshold: ThresholdPolicy


class DecisionResponse(BaseModel):
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
        "low_signal_quality",
        "threshold_uncertain",
        "no_face",
        "multiple_faces",
        None,
    ]

    engine_info: EngineInfo
