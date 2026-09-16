from unittest.mock import Mock

from app.infrastructure.science.private_batch import (
    FAILURE_EXECUTION_ERROR,
    FAILURE_INFERENCE_NOT_REACHED,
    STATUS_FAILED,
    STATUS_OBSERVED,
    PrivateBatchRequest,
    execute_private_batch_request,
)
from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceObservation,
)


def request() -> PrivateBatchRequest:
    return PrivateBatchRequest(
        sample_id="appa_real:appa-real-000001",
        image_path="/private/corpus/sample.jpg",
        content_type="image/jpeg",
    )


def test_private_batch_returns_only_private_signals_on_success() -> None:
    session = Mock()
    session.observe.return_value = PrivateAgeInferenceObservation(
        internal_estimate=19.25,
        signal_quality_score=0.81,
    )

    result = execute_private_batch_request(
        request=request(),
        session=session,
        read_bytes=lambda path: b"image-bytes",
    )

    assert result == {
        "sample_id": "appa_real:appa-real-000001",
        "status": STATUS_OBSERVED,
        "signals": {
            "internal_estimate": 19.25,
            "signal_quality_score": 0.81,
        },
    }

    session.observe.assert_called_once_with(
        image_bytes=b"image-bytes",
        content_type="image/jpeg",
    )

    serialized = str(result)

    assert "/private/corpus/sample.jpg" not in serialized
    assert "image_path" not in serialized


def test_private_batch_reports_inference_not_reached() -> None:
    session = Mock()
    session.observe.return_value = None

    result = execute_private_batch_request(
        request=request(),
        session=session,
        read_bytes=lambda path: b"image-bytes",
    )

    assert result == {
        "sample_id": "appa_real:appa-real-000001",
        "status": STATUS_FAILED,
        "failure_reason": FAILURE_INFERENCE_NOT_REACHED,
    }


def test_private_batch_sanitizes_execution_errors() -> None:
    session = Mock()

    private_error = "failed /private/corpus/sample.jpg with sensitive runtime details"

    session.observe.side_effect = RuntimeError(private_error)

    result = execute_private_batch_request(
        request=request(),
        session=session,
        read_bytes=lambda path: b"image-bytes",
    )

    assert result == {
        "sample_id": "appa_real:appa-real-000001",
        "status": STATUS_FAILED,
        "failure_reason": FAILURE_EXECUTION_ERROR,
    }

    serialized = str(result)

    assert private_error not in serialized
    assert "/private/" not in serialized


def test_private_batch_sanitizes_file_read_errors() -> None:
    session = Mock()

    def fail_read(path):
        raise OSError(f"cannot read private path {path}")

    result = execute_private_batch_request(
        request=request(),
        session=session,
        read_bytes=fail_read,
    )

    assert result == {
        "sample_id": "appa_real:appa-real-000001",
        "status": STATUS_FAILED,
        "failure_reason": FAILURE_EXECUTION_ERROR,
    }

    session.observe.assert_not_called()


def test_private_batch_rejects_invalid_protocol_fields() -> None:
    session = Mock()

    for invalid in (
        PrivateBatchRequest(
            sample_id="",
            image_path="/private/sample.jpg",
            content_type="image/jpeg",
        ),
        PrivateBatchRequest(
            sample_id="sample",
            image_path="",
            content_type="image/jpeg",
        ),
        PrivateBatchRequest(
            sample_id="sample",
            image_path="/private/sample.jpg",
            content_type="text/plain",
        ),
    ):
        try:
            execute_private_batch_request(
                request=invalid,
                session=session,
                read_bytes=lambda path: b"image",
            )
        except ValueError:
            pass
        else:
            raise AssertionError("invalid private batch request accepted")
