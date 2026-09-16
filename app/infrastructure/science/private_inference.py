from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.estimate_command import EstimateCommand
from app.infrastructure.bootstrap.decision_pipeline import build_decision_pipeline


@dataclass(frozen=True)
class PrivateAgeInferenceObservation:
    internal_estimate: float
    signal_quality_score: float


class RecordingScientificObserver:
    def __init__(self) -> None:
        self._observation: PrivateAgeInferenceObservation | None = None

    def observe_age_inference(
        self,
        *,
        internal_estimate: float,
        signal_quality_score: float,
    ) -> None:
        self._observation = PrivateAgeInferenceObservation(
            internal_estimate=float(internal_estimate),
            signal_quality_score=float(signal_quality_score),
        )

    def observation(self) -> PrivateAgeInferenceObservation | None:
        return self._observation


def observe_private_age_inference(
    *,
    image_bytes: bytes,
    content_type: str = "image/jpeg",
) -> PrivateAgeInferenceObservation | None:
    """
    Execute the production-equivalent Core pipeline and return only the
    private raw age inference signals captured before runtime calibration.

    This primitive is intended exclusively for authorized private scientific
    execution. It does not alter the public API response contract and does
    not expose observations through HTTP or production logs.
    """
    observer = RecordingScientificObserver()

    pipeline = build_decision_pipeline(
        runtime_calibration=None,
        scientific_observer=observer,
    )

    command = EstimateCommand(
        image_bytes=image_bytes,
        content_type=content_type,
        request_id="scientific-observation",
        correlation_id="scientific-observation",
        age_threshold=None,
        majority_country=None,
    )

    pipeline.run(command)

    return observer.observation()
