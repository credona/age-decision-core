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

<h2>Quickstart for contributors</h2>

Start the development environment:

```bash
./scripts/docker/dev.sh
```

Download local model files:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
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
  "version": "2.2.2",
  "contract_version": "2.2"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-core",
  "app_name": "Age Decision Core",
  "version": "2.2.2",
  "contract_version": "2.2",
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

<h2>One-command workflow</h2>

Auto-fix, regenerate metadata and documentation, then validate everything:

```bash
./scripts/ci/fix_all_docker.sh
```

Run strict validation only:

```bash
./scripts/ci/check_all_docker.sh
```

Start the development container:

```bash
./scripts/docker/dev.sh
```

Build an image with metadata from `project.json`:

```bash
./scripts/docker/build.sh prod
./scripts/docker/build.sh dev
```

<hr>

<h2>Configuration model</h2>

Project metadata is declared once in:

```text
project.json
```

Generated environment files are created under:

```text
.generated/
```

Do not edit generated files manually.

Runtime defaults are generated from `project.json`.

External users may still override runtime values with Docker environment variables.

Example:

```bash
docker run --rm \
  -p 8000:8000 \
  -e AGE_THRESHOLD=21 \
  -e CONFIDENCE_THRESHOLD=0.9 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

<hr>

<h2>Model files</h2>

Age Decision Core uses external ONNX model files.

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image by default.

Download them explicitly when needed:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
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

The public response does not expose:

- estimated age
- raw model confidence
- threshold distance
- legacy `cred_score` alias

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is declared in `compatibility.json` and synchronized from `project.json`.

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.2.2",
  "contract_version": "2.2",
  "compatible_with": {
    "age-decision-api": ">=2.0.0 <3.0.0",
    "age-decision-js": ">=2.0.0 <3.0.0"
  },
  "public_contract": {
    "estimated_age_exposed": false,
    "raw_confidence_exposed": false,
    "legacy_cred_score_exposed": false,
    "score_field": "cred_decision_score",
    "decision_values": [
      "match",
      "no_match",
      "uncertain"
    ]
  }
}
```
<!-- END:COMPATIBILITY_METADATA -->

<hr>

<h2>Docker image</h2>

```text
ghcr.io/credona/age-decision-core
```

The public Docker image contains the application runtime.

It should not contain ONNX model binaries by default.

Run with mounted models:

```bash
docker run --rm \
  -p 8000:8000 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

See LICENSE for details.

Third-party models may have their own upstream license, origin, and redistribution terms.

See docs/models.md for model transparency notes.
