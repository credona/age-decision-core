#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

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


def main() -> int:
    session = PrivateAgeInferenceSession()

    for raw_line in sys.stdin:
        if not raw_line.strip():
            continue

        try:
            payload = json.loads(raw_line)

            request = PrivateBatchRequest(
                sample_id=str(payload["sample_id"]),
                image_path=str(payload["image_path"]),
                content_type=str(
                    payload.get(
                        "content_type",
                        "image/jpeg",
                    )
                ),
            )

            result = execute_private_batch_request(
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


if __name__ == "__main__":
    raise SystemExit(main())
