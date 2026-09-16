from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.estimate_command import EstimateCommand
from app.application.use_cases.decision_pipeline import DecisionPipeline
from app.infrastructure.bootstrap.decision_pipeline import build_decision_pipeline


@dataclass(frozen=True)
class PrivateAgeInferenceObservation:
    internal_estimate: float
    signal_quality_score: float


class RecordingScientificObserver:
    def __init__(self) -> None:
        self._observation: PrivateAgeInferenceObservation | None = None

    def reset(self) -> None:
        self._observation = None

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


class PrivateAgeInferenceSession:
    """
    Long-lived private scientific inference session.

    The production-equivalent pipeline and its model-backed adapters are
    constructed once and reused across samples. The observer is reset before
    every execution so an unsuccessful sample cannot inherit signals from a
    previous successful inference.
    """

    def __init__(
        self,
        *,
        pipeline: DecisionPipeline | None = None,
        observer: RecordingScientificObserver | None = None,
    ) -> None:
        self._observer = observer or RecordingScientificObserver()

        self._pipeline = pipeline or build_decision_pipeline(
            runtime_calibration=None,
            scientific_observer=self._observer,
        )

    def observe(
        self,
        *,
        image_bytes: bytes,
        content_type: str = "image/jpeg",
    ) -> PrivateAgeInferenceObservation | None:
        self._observer.reset()

        command = EstimateCommand(
            image_bytes=image_bytes,
            content_type=content_type,
            request_id="scientific-observation",
            correlation_id="scientific-observation",
            age_threshold=None,
            majority_country=None,
        )

        self._pipeline.run(command)

        return self._observer.observation()


def observe_private_age_inference(
    *,
    image_bytes: bytes,
    content_type: str = "image/jpeg",
) -> PrivateAgeInferenceObservation | None:
    """
    Execute one private scientific observation.

    Batch scientific execution should use PrivateAgeInferenceSession directly
    so the production-equivalent pipeline is constructed only once.
    """
    session = PrivateAgeInferenceSession()

    return session.observe(
        image_bytes=image_bytes,
        content_type=content_type,
    )
