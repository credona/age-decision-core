<h1>Age Decision Core Benchmarks</h1>

This document describes benchmark expectations for Age Decision Core.

Benchmark results must be reproducible and tied to explicit model identifiers.

<hr>

<h2>Benchmark script</h2>

The repository includes:

<pre>
../age-decision-benchmark/scripts/server/run_all_service_contract_benchmarks_local.sh
</pre>

Run from the development container:

<pre>
cd ../age-decision-benchmark && scripts/server/run_all_service_contract_benchmarks_local.sh
</pre>

<hr>

<h2>What the benchmark measures</h2>

The current benchmark focuses on service execution behavior:

- request count
- success count
- average latency
- percentile latency

<hr>

<h2>Model reproducibility requirements</h2>

Every benchmark MUST specify:

<pre>
model_id
model_version
scoring_policy_id
runtime (onnx / mock)
execution provider
</pre>

Low-level model paths must not be used as reference identifiers.

<hr>

<h2>Dataset transparency</h2>

Benchmark reports must include:

<pre>
dataset name
dataset size
dataset source
known biases
preprocessing steps
</pre>

<hr>

<h2>What the benchmark does not prove</h2>

Benchmarks do not prove:

- legal age verification accuracy
- demographic fairness
- spoof resistance
- regulatory compliance
- real-world calibration

<hr>

<h2>Evaluation direction</h2>

Future work:

- calibration curves
- threshold sensitivity analysis
- uncertainty distribution
- cross-dataset validation
- reproducible benchmark snapshots

<hr>

<h2>Reporting format</h2>

<pre>
date
model_id
model_version
scoring_policy_id
dataset name
dataset size
request count
success count
average latency
p95 latency
error count
known limitations
</pre>
