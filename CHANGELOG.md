<h1>Changelog</h1>

This changelog tracks changes specific to Age Decision Core.

Global project direction is tracked in the central Age Decision repository.

<hr>

<h2>1.2.2</h2>

- Documentation structure simplified.
- Repository README reduced to a concise entry point.
- Technical usage moved to docs/usage.md.
- Model transparency moved to docs/models.md.
- Benchmark notes moved to docs/benchmarks.md.

<hr>

<h2>1.2.1</h2>

- Updated dependency and CI maintenance items.
- Validated Docker runtime.
- Validated health endpoint.
- Validated model status endpoint.
- Validated estimate endpoint with a real image.
- Validated full test suite.

<hr>

<h2>1.2.0</h2>

- Renamed `cred_score` to `cred_decision_score`.
- Kept `cred_score` as a temporary compatibility alias.
- Added stable error response schema.
- Added request tracing to error responses.
- Normalized estimate response contract.
- Added contract tests for `cred_decision_score`.
- Added compatibility tests for `cred_score`.
- Added OpenAPI schema tests.
- Updated response documentation.

<hr>

<h2>1.1.0</h2>

- Upgraded Docker runtime to Python 3.14.
- Validated ONNX Runtime compatibility.
- Validated OpenCV compatibility.
- Validated health, model status and estimate endpoints.

<hr>

<h2>1.0.2</h2>

- Updated Python dependencies.
- Kept runtime compatible with ML dependencies.
- Validated Docker runtime and estimate endpoint.

<hr>

<h2>1.0.1</h2>

- Added CI workflow.
- Added Docker image workflow.
- Added release workflow.
- Added CodeQL scanning.
- Added Dependabot configuration.
- Published Docker image.

<hr>

<h2>1.0.0</h2>

- Initial public release.
- Added FastAPI inference service.
- Added YuNet face detection.
- Added ONNX age estimation.
- Added probabilistic decision policy.
- Added privacy metadata.
- Added structured logs.
- Added tests.
- Added Docker development setup.
