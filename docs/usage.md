<h1>Usage</h1>

This document describes how to run and use Age Decision Core.

<hr>

<h2>Contributor usage</h2>

Start the development environment:

<pre>
./scripts/docker/dev.sh
</pre>

Download models:

<pre>
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
</pre>

Stop the environment:

<pre>
docker compose --env-file .generated/compose/dev.env -f docker-compose.dev.yml down
</pre>

<hr>

<h2>Health checks</h2>

<pre>
curl -i http://localhost:8000/health
curl -i http://localhost:8000/version
curl -i http://localhost:8000/engine/status
</pre>

Expected health response:

<!-- BEGIN:HEALTH_RESPONSE -->
```json
{
  "status": "ok",
  "service": "age-decision-core",
  "version": "2.5.0",
  "contract_version": "2.5"
}
```
<!-- END:HEALTH_RESPONSE -->

Expected version response:

<!-- BEGIN:VERSION_RESPONSE -->
```json
{
  "service_name": "age-decision-core",
  "app_name": "Age Decision Core",
  "version": "2.5.0",
  "contract_version": "2.5",
  "repository": "https://github.com/credona/age-decision-core",
  "image": "ghcr.io/credona/age-decision-core"
}
```
<!-- END:VERSION_RESPONSE -->

<hr>

<h2>Run an age decision</h2>

<pre>
curl -X POST "http://localhost:8000/estimate?majority_country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
</pre>

<hr>

<h2>Runtime configuration</h2>

Runtime configuration is defined in project.json.

Generated files:

<pre>
.generated/runtime/
.generated/compose/
</pre>

Regenerate:

<pre>
./scripts/config/generate_env.sh dev
</pre>

Runtime configuration uses model identifiers.

Low-level model paths and threshold values must not be treated as public runtime contract.

<hr>

<h2>External Docker usage</h2>

<pre>
docker run --rm \
  -p 8000:8000 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
</pre>

<hr>

<h2>Validation</h2>

<pre>
./scripts/ci/check_all_docker.sh
</pre>

<hr>

<h2>Compatibility metadata</h2>

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.5.0",
  "contract_version": "2.5",
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
