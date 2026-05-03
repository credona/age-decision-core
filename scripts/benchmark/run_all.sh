#!/usr/bin/env sh
set -eu

scripts/benchmark/run_core_model_benchmark.sh

if [ "${BENCHMARK_RUN_SERVICE:-false}" = "true" ]; then
  scripts/benchmark/run_core_service_benchmark.sh
fi
