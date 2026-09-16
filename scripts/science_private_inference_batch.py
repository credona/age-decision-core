#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from app.infrastructure.science.private_batch import (
    PrivateBatchRequest,
    execute_private_batch_request,
)
from app.infrastructure.science.private_inference import (
    PrivateAgeInferenceSession,
)


def emit(payload: dict) -> None:
    sys.stdout.write(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    )
    sys.stdout.flush()


def require_string(
    payload: dict[str, Any],
    field: str,
    *,
    default: str | None = None,
) -> str:
    if field not in payload:
        if default is None:
            raise ValueError(f"missing protocol field: {field}")
        return default

    value = payload[field]

    if not isinstance(value, str) or not value:
        raise ValueError(f"protocol field must be a non-empty string: {field}")

    return value


async def main_async() -> int:
    session = PrivateAgeInferenceSession()

    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue

        try:
            payload = json.loads(raw_line)

            if not isinstance(payload, dict):
                raise ValueError("protocol payload must be an object")

            request = PrivateBatchRequest(
                sample_id=require_string(
                    payload,
                    "sample_id",
                ),
                image_path=require_string(
                    payload,
                    "image_path",
                ),
                content_type=require_string(
                    payload,
                    "content_type",
                    default="image/jpeg",
                ),
            )

            result = await execute_private_batch_request(
                request=request,
                session=session,
            )
        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ):
            # Invalid protocol input is a runner/configuration failure rather
            # than a scientific sample result. Do not echo malformed input.
            return 2

        emit(result)

    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
