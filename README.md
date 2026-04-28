<h1>Age Decision Core</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/docker.yml?branch=main&label=Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/codeql.yml?branch=main&label=CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-core" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision Core is the age threshold decision service of the Age Decision ecosystem.

It detects a face, runs internal age estimation, applies threshold rules, and returns a probabilistic threshold decision.

It does not expose estimated age.

It does not perform identity verification, face recognition, document verification, or legal age proof.

<hr>

<h2>Documentation</h2>

- Repository: https://github.com/credona/age-decision-core
- Usage: docs/usage.md
- Models and third-party notices: docs/models.md
- Benchmarks: docs/benchmarks.md
- Compatibility: docs/compatibility.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md
- Global project: https://github.com/credona/age-decision

<hr>

<h2>Quickstart</h2>

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

Check the service:

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/version
curl -i http://localhost:8000/model/status
```

Expected health response:

<!-- BEGIN:HEALTH_RESPONSE -->
```json
{
  "status": "ok",
  "service": "age-decision-core",
  "version": "2.1.1",
  "contract_version": "2.0"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-core",
  "app_name": "Age Decision Core",
  "version": "2.1.1",
  "contract_version": "2.0",
  "repository": "https://github.com/credona/age-decision-core",
  "image": "ghcr.io/credona/age-decision-core"
}
```
<!-- END:VERSION_RESPONSE -->

Run an age decision:

```bash
curl -X POST "http://localhost:8000/estimate?majority_country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

<h2>Model files</h2>

Age Decision Core uses external ONNX model files.

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image by default.

Download them explicitly when needed:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

Expected local paths:

```text
models/face_detection/face_detection_yunet_2023mar.onnx
models/age_estimation/age-gender-prediction-ONNX.onnx
```

For model origin, license notes, and redistribution checks, see:

```text
docs/models.md
```

<hr>

<h2>Public contract</h2>

The main response exposes:

- `decision`
- `threshold`
- `cred_decision_score`
- `request_id`
- `correlation_id`
- `privacy`
- `proof`
- `rejection_reason`

`decision` uses:

```text
match
no_match
uncertain
```

`cred_decision_score` is the explicit age threshold decision score produced by this service.

The public response does not expose:

- estimated age
- raw model confidence
- threshold distance
- legacy `cred_score` alias

For compatibility rules, see:

```text
docs/compatibility.md
```

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is declared in `compatibility.json` and checked by CI.

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.1.0",
  "contract_version": "2.0",
  "compatible_with": {
    "age-decision-api": ">=2.0.0 <3.0.0",
    "age-decision-js": ">=2.0.0 <3.0.0"
  },
  "public_contract": {
    "decision_values": [
      "match",
      "no_match",
      "uncertain"
    ],
    "score_field": "cred_decision_score",
    "estimated_age_exposed": false,
    "raw_confidence_exposed": false,
    "legacy_cred_score_exposed": false
  }
}
```
<!-- END:COMPATIBILITY_METADATA -->

<hr>

<h2>Quality and compatibility checks</h2>

Run tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

Run contract tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core pytest tests/unit/contract
```

Run quality checks:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core ruff check .
docker compose -f docker-compose.dev.yml exec age-decision-core ruff format --check .
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/check_project_metadata.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/check_compatibility_metadata.py
```

Update generated documentation blocks:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_readme_examples.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_docs_usage.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_docs_compatibility.py
```

Compile Python files:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python -m compileall app tests scripts
```

<hr>

<h2>Docker image</h2>

```text
ghcr.io/credona/age-decision-core
```

The public Docker image contains the application runtime.

It should not contain ONNX model binaries by default.

Run with mounted models:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py

docker run --rm \
  -p 8000:8000 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

<hr>

<h2>Testing</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

See LICENSE for details.

Third-party models may have their own upstream license, origin, and redistribution terms.

See docs/models.md for model transparency notes.
