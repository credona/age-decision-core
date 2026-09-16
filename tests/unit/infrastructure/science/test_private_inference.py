from unittest.mock import Mock, patch

from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceObservation,
    PrivateAgeInferenceSession,
    RecordingScientificObserver,
    observe_private_age_inference,
)


def test_recording_observer_captures_and_resets_private_signals() -> None:
    observer = RecordingScientificObserver()

    observer.observe_age_inference(
        internal_estimate=19.25,
        signal_quality_score=0.81,
    )

    assert observer.observation() == PrivateAgeInferenceObservation(
        internal_estimate=19.25,
        signal_quality_score=0.81,
    )

    observer.reset()

    assert observer.observation() is None


def test_session_constructs_production_pipeline_once() -> None:
    pipeline = Mock()
    observer = RecordingScientificObserver()

    def run(command):
        observer.observe_age_inference(
            internal_estimate=22.5,
            signal_quality_score=0.73,
        )
        return {"decision": "match"}

    pipeline.run.side_effect = run

    with patch(
        "app.infrastructure.science.private_inference.build_decision_pipeline",
        return_value=pipeline,
    ) as factory:
        session = PrivateAgeInferenceSession(
            observer=observer,
        )

        first = session.observe(
            image_bytes=b"first-image",
            content_type="image/jpeg",
        )

        second = session.observe(
            image_bytes=b"second-image",
            content_type="image/png",
        )

    factory.assert_called_once_with(
        runtime_calibration=None,
        scientific_observer=observer,
    )

    assert pipeline.run.call_count == 2

    assert first == PrivateAgeInferenceObservation(
        internal_estimate=22.5,
        signal_quality_score=0.73,
    )
    assert second == first

    first_command = pipeline.run.call_args_list[0].args[0]
    second_command = pipeline.run.call_args_list[1].args[0]

    assert first_command.image_bytes == b"first-image"
    assert first_command.content_type == "image/jpeg"
    assert second_command.image_bytes == b"second-image"
    assert second_command.content_type == "image/png"

    for command in (first_command, second_command):
        assert command.request_id == "scientific-observation"
        assert command.correlation_id == "scientific-observation"
        assert command.age_threshold is None
        assert command.majority_country is None


def test_session_resets_observer_between_samples() -> None:
    observer = RecordingScientificObserver()
    pipeline = Mock()

    calls = 0

    def run(command):
        nonlocal calls
        calls += 1

        if calls == 1:
            observer.observe_age_inference(
                internal_estimate=18.5,
                signal_quality_score=0.66,
            )

        return {"decision": "uncertain"}

    pipeline.run.side_effect = run

    session = PrivateAgeInferenceSession(
        pipeline=pipeline,
        observer=observer,
    )

    first = session.observe(
        image_bytes=b"successful-image",
    )
    second = session.observe(
        image_bytes=b"no-inference-image",
    )

    assert first == PrivateAgeInferenceObservation(
        internal_estimate=18.5,
        signal_quality_score=0.66,
    )

    assert second is None


def test_single_observation_wrapper_uses_session() -> None:
    session = Mock()
    session.observe.return_value = PrivateAgeInferenceObservation(
        internal_estimate=20.0,
        signal_quality_score=0.75,
    )

    with patch(
        "app.infrastructure.science.private_inference.PrivateAgeInferenceSession",
        return_value=session,
    ):
        observation = observe_private_age_inference(
            image_bytes=b"private-image-bytes",
            content_type="image/jpeg",
        )

    session.observe.assert_called_once_with(
        image_bytes=b"private-image-bytes",
        content_type="image/jpeg",
    )

    assert observation == PrivateAgeInferenceObservation(
        internal_estimate=20.0,
        signal_quality_score=0.75,
    )
