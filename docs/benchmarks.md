<h1>Age Decision Core Benchmarks</h1>

This document describes benchmark expectations for Age Decision Core.

Benchmark results should be reproducible and separated from product claims.

<hr>

<h2>Benchmark script</h2>

The repository includes:

```text
scripts/benchmark.py
```

Run locally from the development container:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/benchmark.py
```

<hr>

<h2>What the benchmark measures</h2>

The current benchmark focuses on service execution behavior.

Typical metrics include:

- number of requests
- success count
- average latency
- percentile latency

<hr>

<h2>What the benchmark does not prove</h2>

The current benchmark does not prove:

- legal age verification accuracy
- demographic fairness
- production reliability
- spoof resistance
- certified compliance
- real-world calibration quality

<hr>

<h2>Evaluation direction</h2>

Future benchmark work should include:

- documented evaluation datasets
- confidence calibration notes
- age threshold evaluation
- uncertainty analysis
- reproducible benchmark reports
- clear separation between local results and upstream model claims

<hr>

<h2>Reporting format</h2>

Benchmark reports should include:

```text
date
runtime
model paths
dataset name
dataset size
request count
success count
average latency
p95 latency
error count
known limitations
```
