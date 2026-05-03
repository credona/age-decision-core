# Core Benchmarks

This directory contains Age Decision Core benchmark tooling for v2.6.0.

## Scope

Core benchmarks cover:

- model pipeline execution
- HTTP service execution
- privacy-safe report generation
- deterministic benchmark metadata

## Reports

Reports are written as JSON and must follow:

benchmarks/schemas/benchmark-report.schema.json

## Privacy

Benchmark reports must never expose:

- estimated_age
- confidence
- raw scores
- internal thresholds
- score components
- base64 payloads
- raw payloads
- downstream raw responses
- model paths

Only aggregate metrics are allowed.

## Model benchmark

Run:

scripts/benchmark/run_core_model_benchmark.sh

Default output:

benchmarks/reports/core-model-benchmark.json

## Service benchmark

Start the service first, then run:

scripts/benchmark/run_core_service_benchmark.sh

Default URL:

http://localhost:8000/estimate

## All benchmarks

Run model benchmark only:

scripts/benchmark/run_all.sh

Run model and service benchmarks:

BENCHMARK_RUN_SERVICE=true scripts/benchmark/run_all.sh

## Metadata

The following environment variables may be used:

- BENCHMARK_HOSTING_PROVIDER
- BENCHMARK_GPU
- BENCHMARK_SEED
- BENCHMARK_DATASET_NAME
- BENCHMARK_DATASET_VERSION
- BENCHMARK_DATASET_SPLIT
- BENCHMARK_DATASET_LICENSE
- BENCHMARK_DATASET_SOURCE
- BENCHMARK_DOCKER_IMAGE
- BENCHMARK_DOCKER_IMAGE_DIGEST
