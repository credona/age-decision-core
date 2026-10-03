import asyncio
from unittest.mock import AsyncMock, patch

from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceNotReached,
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
    observer = RecordingScientificObserver()
    pipeline = AsyncMock()

    async def run(**kwargs):
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

        first = asyncio.run(
            session.observe(
                image_bytes=b"first-image",
                content_type="image/jpeg",
            )
        )

        second = asyncio.run(
            session.observe(
                image_bytes=b"second-image",
                content_type="image/png",
            )
        )

    factory.assert_called_once_with(
        runtime_calibration=None,
        scientific_observer=observer,
    )

    assert pipeline.run.await_count == 2

    first_call = pipeline.run.await_args_list[0].kwargs
    second_call = pipeline.run.await_args_list[1].kwargs

    assert first_call["image_bytes"] == b"first-image"
    assert first_call["content_type"] == "image/jpeg"
    assert second_call["image_bytes"] == b"second-image"
    assert second_call["content_type"] == "image/png"

    for call in (first_call, second_call):
        assert call["request_id"] == "scientific-observation"
        assert call["correlation_id"] == "scientific-observation"
        assert call["age_threshold"] is None
        assert call["majority_country"] is None

    assert first == PrivateAgeInferenceObservation(
        internal_estimate=22.5,
        signal_quality_score=0.73,
    )
    assert second == first


def test_session_resets_observer_between_samples() -> None:
    observer = RecordingScientificObserver()
    pipeline = AsyncMock()

    calls = 0

    async def run(**kwargs):
        nonlocal calls
        calls += 1

        if calls == 1:
            observer.observe_age_inference(
                internal_estimate=18.5,
                signal_quality_score=0.66,
            )
            return {
                "decision": "uncertain",
                "rejection_reason": "threshold_uncertain",
            }

        return {
            "decision": "uncertain",
            "rejection_reason": "no_face",
        }

    pipeline.run.side_effect = run

    session = PrivateAgeInferenceSession(
        pipeline=pipeline,
        observer=observer,
    )

    first = asyncio.run(
        session.observe(
            image_bytes=b"successful-image",
        )
    )
    second = asyncio.run(
        session.observe(
            image_bytes=b"no-inference-image",
        )
    )

    assert first == PrivateAgeInferenceObservation(
        internal_estimate=18.5,
        signal_quality_score=0.66,
    )

    assert second == PrivateAgeInferenceNotReached(
        reason="no_face",
    )


def test_session_reports_multiple_faces_before_inference() -> None:
    observer = RecordingScientificObserver()
    pipeline = AsyncMock()
    pipeline.run.return_value = {
        "decision": "uncertain",
        "rejection_reason": "multiple_faces",
    }

    session = PrivateAgeInferenceSession(
        pipeline=pipeline,
        observer=observer,
    )

    result = asyncio.run(
        session.observe(
            image_bytes=b"multiple-faces",
        )
    )

    assert result == PrivateAgeInferenceNotReached(
        reason="multiple_faces",
    )


def test_session_rejects_unexplained_missing_inference() -> None:
    observer = RecordingScientificObserver()
    pipeline = AsyncMock()
    pipeline.run.return_value = {
        "decision": "uncertain",
        "rejection_reason": "threshold_uncertain",
    }

    session = PrivateAgeInferenceSession(
        pipeline=pipeline,
        observer=observer,
    )

    try:
        asyncio.run(
            session.observe(
                image_bytes=b"unexpected-no-inference",
            )
        )
    except RuntimeError:
        return

    raise AssertionError("unexplained missing inference was accepted")


def test_single_observation_wrapper_uses_session() -> None:
    session = AsyncMock()
    session.observe.return_value = PrivateAgeInferenceObservation(
        internal_estimate=20.0,
        signal_quality_score=0.75,
    )

    with patch(
        "app.infrastructure.science.private_inference.PrivateAgeInferenceSession",
        return_value=session,
    ):
        observation = asyncio.run(
            observe_private_age_inference(
                image_bytes=b"private-image-bytes",
                content_type="image/jpeg",
            )
        )

    session.observe.assert_awaited_once_with(
        image_bytes=b"private-image-bytes",
        content_type="image/jpeg",
    )

    assert observation == PrivateAgeInferenceObservation(
        internal_estimate=20.0,
        signal_quality_score=0.75,
    )
