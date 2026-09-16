from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceSession,
)

STATUS_OBSERVED = "observed"
STATUS_FAILED = "failed"

FAILURE_INFERENCE_NOT_REACHED = "inference_not_reached"
FAILURE_EXECUTION_ERROR = "execution_error"


@dataclass(frozen=True)
class PrivateBatchRequest:
    sample_id: str
    image_path: str
    content_type: str


async def execute_private_batch_request(
    *,
    request: PrivateBatchRequest,
    session: PrivateAgeInferenceSession,
    read_bytes: Callable[[Path], bytes] | None = None,
) -> dict:
    """
    Execute one private scientific inference request.

    image_path is private execution input only. It must never be copied into
    the returned result or emitted by callers as part of the scientific
    observation artifact.
    """
    if not request.sample_id:
        raise ValueError("sample_id must not be empty")

    if not request.image_path:
        raise ValueError("image_path must not be empty")

    if request.content_type not in {
        "image/jpeg",
        "image/png",
        "image/webp",
    }:
        raise ValueError("unsupported content_type")

    loader = read_bytes or Path.read_bytes

    try:
        image_bytes = loader(Path(request.image_path))

        observation = await session.observe(
            image_bytes=image_bytes,
            content_type=request.content_type,
        )
    except Exception:
        return {
            "sample_id": request.sample_id,
            "status": STATUS_FAILED,
            "failure_reason": FAILURE_EXECUTION_ERROR,
        }

    if observation is None:
        return {
            "sample_id": request.sample_id,
            "status": STATUS_FAILED,
            "failure_reason": FAILURE_INFERENCE_NOT_REACHED,
        }

    return {
        "sample_id": request.sample_id,
        "status": STATUS_OBSERVED,
        "signals": {
            "internal_estimate": float(observation.internal_estimate),
            "signal_quality_score": float(observation.signal_quality_score),
        },
    }
