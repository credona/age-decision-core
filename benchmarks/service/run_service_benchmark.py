from __future__ import annotations

import argparse
import time
from pathlib import Path

import requests

from benchmarks.common.report import build_benchmark_report, write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Age Decision Core service benchmark.")
    parser.add_argument("--url", default="http://localhost:8000/estimate")
    parser.add_argument("--input-file", default="test-face.jpg")
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--output", default="benchmarks/reports/core-service-benchmark.json")
    return parser.parse_args()


def run_service_benchmark(args: argparse.Namespace) -> dict[str, object]:
    input_path = Path(args.input_file)

    durations_ms: list[float] = []
    decisions: list[str] = []

    for _ in range(args.iterations):
        with input_path.open("rb") as file:
            start = time.perf_counter()
            response = requests.post(
                args.url,
                files={"file": (input_path.name, file, "image/jpeg")},
                timeout=args.timeout,
            )
            durations_ms.append((time.perf_counter() - start) * 1000)

        response.raise_for_status()
        payload = response.json()
        decisions.append(str(payload.get("decision", "uncertain")))

    return build_benchmark_report(
        benchmark_target="service",
        durations_ms=durations_ms,
        decisions=decisions,
        command=(
            "python -m benchmarks.service.run_service_benchmark "
            f"--url {args.url} --input-file {args.input_file} "
            f"--iterations {args.iterations} --timeout {args.timeout} --output {args.output}"
        ),
        sample_count=args.iterations,
    )


def main() -> None:
    args = parse_args()
    report = run_service_benchmark(args)
    write_report(report, args.output)
    print(f"Benchmark report written to {args.output}")


if __name__ == "__main__":
    main()
