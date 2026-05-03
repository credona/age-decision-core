#!/usr/bin/env sh
set -eu

URL="${BENCHMARK_CORE_URL:-http://localhost:8000/estimate}"
INPUT_FILE="${BENCHMARK_INPUT_FILE:-test-face.jpg}"
ITERATIONS="${BENCHMARK_ITERATIONS:-20}"
TIMEOUT="${BENCHMARK_TIMEOUT:-5}"
OUTPUT_PATH="${BENCHMARK_OUTPUT_PATH:-benchmarks/reports/core-service-benchmark.json}"

python -m benchmarks.service.run_service_benchmark   --url "$URL"   --input-file "$INPUT_FILE"   --iterations "$ITERATIONS"   --timeout "$TIMEOUT"   --output "$OUTPUT_PATH"
