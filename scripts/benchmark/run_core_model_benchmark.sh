#!/usr/bin/env sh
set -eu

INPUT_FILE="${BENCHMARK_INPUT_FILE:-test-face.jpg}"
ITERATIONS="${BENCHMARK_ITERATIONS:-20}"
OUTPUT_PATH="${BENCHMARK_OUTPUT_PATH:-benchmarks/reports/core-model-benchmark.json}"

python -m benchmarks.model.run_model_benchmark   --input-file "$INPUT_FILE"   --iterations "$ITERATIONS"   --output "$OUTPUT_PATH"
