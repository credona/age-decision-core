<h1>Usage</h1>

This document describes how to run and use Age Decision Core.

<hr>

<h2>Contributor usage</h2>

Start the development environment:

```bash
./scripts/docker/dev.sh
```

Download models:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
```

Stop the environment:

```bash
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml down
```

<hr>

<h2>Health checks</h2>

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/version
curl -i http://localhost:8000/engine/status
```

Expected health response:

<!-- BEGIN:HEALTH_RESPONSE -->
```json
{
  "status": "ok",
  "service": "age-decision-core",
  "version": "2.4.0",
  "contract_version": "2.4"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-core",
  "app_name": "Age Decision Core",
  "version": "2.4.0",
  "contract_version": "2.4",
  "repository": "https://github.com/credona/age-decision-core",
  "image": "ghcr.io/credona/age-decision-core"
}
```
<!-- END:VERSION_RESPONSE -->

<hr>

<h2>Run an age decision</h2>

```bash
curl -X POST "http://localhost:8000/estimate?majority_country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

Standardized validation error example (missing multipart file):

```bash
curl -X POST "http://localhost:8000/estimate" \
  -H "X-Request-ID: test-request-002" \
  -H "X-Correlation-ID: test-correlation-002"
```

Expected response:

```json
{
  "request_id": "test-request-002",
  "correlation_id": "test-correlation-002",
  "error": {
    "code": "missing_file",
    "message": "Invalid request."
  }
}
```

<hr>

<h2>Runtime configuration</h2>

Default runtime values are declared in `project.json`.

Generated runtime files are written to:

```text
.generated/runtime/
```

Generated Compose files are written to:

```text
.generated/compose/
```

Do not edit generated files manually.

Regenerate them with:

```bash
./scripts/config/generate_env.sh dev
```

<hr>

<h2>External Docker usage</h2>

Run from the published image:

```bash
docker run --rm \
  -p 8000:8000 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

Override runtime values:

```bash
docker run --rm \
  -p 8000:8000 \
  -e AGE_THRESHOLD=21 \
  -e CONFIDENCE_THRESHOLD=0.9 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

<hr>

<h2>Validation</h2>

Run the full auto-fix and validation pipeline:

```bash
./scripts/ci/fix_all_docker.sh
```

Run validation only:

```bash
./scripts/ci/check_all_docker.sh
```

<hr>

<h2>Compatibility metadata</h2>

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.4.0",
  "contract_version": "2.4",
  "compatible_with": {
    "age-decision-api": ">=2.0.0 <3.0.0",
    "age-decision-js": ">=2.0.0 <3.0.0"
  },
  "public_contract": {
    "internal_estimate_exposed": false,
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

<h2>Notes</h2>

Age Decision Core returns a probabilistic threshold decision.

It does not expose estimated age.

It does not perform identity verification, face recognition, document verification, or legal age proof.
