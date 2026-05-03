from __future__ import annotations

import argparse
import asyncio
import time
from pathlib import Path

from app.application.dto.estimate_command import EstimateCommand
from app.application.use_cases.decision_pipeline import DecisionPipeline
from app.application.use_cases.run_decision import RunDecisionUseCase
from app.infrastructure.logging.safe_event_logger import SafeEventLogger
from app.infrastructure.models.onnx_inference_engine import OnnxInferenceEngine
from app.infrastructure.vision.face_cropper import FaceCropper
from app.infrastructure.vision.face_preprocessor import FacePreprocessor
from app.infrastructure.vision.opencv_image_loader import load_image_from_bytes
from app.infrastructure.vision.opencv_input_analyzer import OpenCvInputAnalyzer
from benchmarks.common.report import build_benchmark_report, write_report


class OpenCvImageDecoder:
    def decode(self, image_bytes: bytes):
        return load_image_from_bytes(image_bytes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Age Decision Core model benchmark.")
    parser.add_argument("--input-file", default="test-face.jpg")
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--output", default="benchmarks/reports/core-model-benchmark.json")
    return parser.parse_args()


async def run_model_benchmark(args: argparse.Namespace) -> dict[str, object]:
    input_path = Path(args.input_file)
    image_bytes = input_path.read_bytes()

    pipeline = DecisionPipeline(
        inference_engine=OnnxInferenceEngine(),
        input_analyzer=OpenCvInputAnalyzer(),
        image_decoder=OpenCvImageDecoder(),
        face_cropper=FaceCropper(),
        input_preprocessor=FacePreprocessor(),
        event_logger=SafeEventLogger(),
    )

    use_case = RunDecisionUseCase(pipeline)
    durations_ms: list[float] = []
    decisions: list[str] = []

    for index in range(args.iterations):
        start = time.perf_counter()
        result = await use_case.execute(
            EstimateCommand(
                image_bytes=image_bytes,
                content_type="image/jpeg",
                request_id=f"benchmark-core-model-{index}",
                correlation_id="benchmark-core-model",
                age_threshold=None,
                majority_country=None,
            )
        )
        durations_ms.append((time.perf_counter() - start) * 1000)
        decisions.append(str(result.get("decision", "uncertain")))

    return build_benchmark_report(
        benchmark_target="model",
        durations_ms=durations_ms,
        decisions=decisions,
        command=(
            "python -m benchmarks.model.run_model_benchmark "
            f"--input-file {args.input_file} --iterations {args.iterations} --output {args.output}"
        ),
        sample_count=args.iterations,
    )


def main() -> None:
    args = parse_args()
    report = asyncio.run(run_model_benchmark(args))
    write_report(report, args.output)
    print(f"Benchmark report written to {args.output}")


if __name__ == "__main__":
    main()
