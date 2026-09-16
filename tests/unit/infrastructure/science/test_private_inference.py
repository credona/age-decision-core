from unittest.mock import Mock, patch

from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceObservation,
    RecordingScientificObserver,
    observe_private_age_inference,
)


def test_recording_observer_captures_private_signals() -> None:
    observer = RecordingScientificObserver()

    observer.observe_age_inference(
        internal_estimate=19.25,
        signal_quality_score=0.81,
    )

    assert observer.observation() == PrivateAgeInferenceObservation(
        internal_estimate=19.25,
        signal_quality_score=0.81,
    )


def test_private_inference_uses_production_pipeline_factory() -> None:
    pipeline = Mock()

    def run(command):
        observer.observe_age_inference(
            internal_estimate=22.5,
            signal_quality_score=0.73,
        )
        return {"decision": "match"}

    pipeline.run.side_effect = run

    observer = None

    def build_pipeline(
        runtime_calibration=None,
        scientific_observer=None,
    ):
        nonlocal observer

        assert runtime_calibration is None
        observer = scientific_observer

        return pipeline

    with patch(
        "app.infrastructure.science.private_inference.build_decision_pipeline",
        side_effect=build_pipeline,
    ):
        observation = observe_private_age_inference(
            image_bytes=b"private-image-bytes",
            content_type="image/jpeg",
        )

    assert observation == PrivateAgeInferenceObservation(
        internal_estimate=22.5,
        signal_quality_score=0.73,
    )

    command = pipeline.run.call_args.args[0]

    assert command.image_bytes == b"private-image-bytes"
    assert command.content_type == "image/jpeg"
    assert command.request_id == "scientific-observation"
    assert command.correlation_id == "scientific-observation"
    assert command.age_threshold is None
    assert command.majority_country is None


def test_private_inference_returns_none_when_inference_is_not_reached() -> None:
    pipeline = Mock()
    pipeline.run.return_value = {
        "decision": "uncertain",
        "reason": "no_face",
    }

    with patch(
        "app.infrastructure.science.private_inference.build_decision_pipeline",
        return_value=pipeline,
    ):
        observation = observe_private_age_inference(
            image_bytes=b"private-image-bytes",
        )

    assert observation is None
