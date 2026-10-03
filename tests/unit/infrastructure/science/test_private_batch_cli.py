import asyncio
import io
import json
from unittest.mock import AsyncMock, Mock, patch

from scripts.science_private_inference_batch import main_async, require_string


def test_require_string_accepts_valid_values_and_default() -> None:
    assert require_string({"sample_id": "sample-1"}, "sample_id") == "sample-1"

    assert (
        require_string(
            {},
            "content_type",
            default="image/jpeg",
        )
        == "image/jpeg"
    )


def test_require_string_rejects_invalid_values() -> None:
    for payload in (
        {},
        {"sample_id": None},
        {"sample_id": 123},
        {"sample_id": ""},
    ):
        try:
            require_string(payload, "sample_id")
        except ValueError:
            pass
        else:
            raise AssertionError("invalid protocol string accepted")


def test_main_async_reuses_one_session_for_multiple_requests() -> None:
    stdin = io.StringIO(
        "\n".join(
            (
                json.dumps(
                    {
                        "sample_id": "sample-1",
                        "image_path": "/private/sample-1.jpg",
                        "content_type": "image/jpeg",
                    }
                ),
                json.dumps(
                    {
                        "sample_id": "sample-2",
                        "image_path": "/private/sample-2.png",
                        "content_type": "image/png",
                    }
                ),
            )
        )
        + "\n"
    )
    stdout = io.StringIO()

    session = Mock()

    execute = AsyncMock(
        side_effect=(
            {
                "sample_id": "sample-1",
                "status": "observed",
                "signals": {
                    "internal_estimate": 18.25,
                    "signal_quality_score": 0.81,
                },
            },
            {
                "sample_id": "sample-2",
                "status": "failed",
                "failure_reason": "inference_not_reached",
            },
        )
    )

    with (
        patch(
            "scripts.science_private_inference_batch.PrivateAgeInferenceSession",
            return_value=session,
        ) as session_factory,
        patch(
            "scripts.science_private_inference_batch.execute_private_batch_request",
            execute,
        ),
        patch(
            "scripts.science_private_inference_batch.sys.stdin",
            stdin,
        ),
        patch(
            "scripts.science_private_inference_batch.sys.stdout",
            stdout,
        ),
    ):
        exit_code = asyncio.run(main_async())

    assert exit_code == 0
    session_factory.assert_called_once_with()

    assert execute.await_count == 2

    first_call = execute.await_args_list[0].kwargs
    second_call = execute.await_args_list[1].kwargs

    assert first_call["session"] is session
    assert second_call["session"] is session

    assert first_call["request"].sample_id == "sample-1"
    assert first_call["request"].image_path == "/private/sample-1.jpg"
    assert first_call["request"].content_type == "image/jpeg"

    assert second_call["request"].sample_id == "sample-2"
    assert second_call["request"].image_path == "/private/sample-2.png"
    assert second_call["request"].content_type == "image/png"

    output = [json.loads(line) for line in stdout.getvalue().splitlines() if line.strip()]

    assert output == [
        {
            "sample_id": "sample-1",
            "signals": {
                "internal_estimate": 18.25,
                "signal_quality_score": 0.81,
            },
            "status": "observed",
        },
        {
            "failure_reason": "inference_not_reached",
            "sample_id": "sample-2",
            "status": "failed",
        },
    ]

    serialized = stdout.getvalue()

    assert "/private/sample-1.jpg" not in serialized
    assert "/private/sample-2.png" not in serialized
    assert "image_path" not in serialized


def test_main_async_rejects_malformed_protocol_without_echoing_input() -> None:
    private_path = "/private/sensitive/sample.jpg"
    stdin = io.StringIO(
        json.dumps(
            {
                "sample_id": None,
                "image_path": private_path,
            }
        )
        + "\n"
    )
    stdout = io.StringIO()

    with (
        patch(
            "scripts.science_private_inference_batch.PrivateAgeInferenceSession",
            return_value=Mock(),
        ),
        patch(
            "scripts.science_private_inference_batch.sys.stdin",
            stdin,
        ),
        patch(
            "scripts.science_private_inference_batch.sys.stdout",
            stdout,
        ),
    ):
        exit_code = asyncio.run(main_async())

    assert exit_code == 2
    assert stdout.getvalue() == ""
    assert private_path not in stdout.getvalue()
