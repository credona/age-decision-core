<h1>Age Decision Core</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/docker.yml?branch=main&label=Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/codeql.yml?branch=main&label=CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-core" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision Core is the age estimation and decision policy service of the Age Decision ecosystem.

It detects a face, estimates apparent age, applies threshold rules, and returns a probabilistic age decision.

It does not perform identity verification, face recognition, document verification, or legal age proof.

<hr>

<h2>Documentation</h2>

- Usage: docs/usage.md
- Models: docs/models.md
- Benchmarks: docs/benchmarks.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md
- Global project: https://github.com/credona/age-decision

<hr>

<h2>Quickstart</h2>

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
```

Check the service:

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/model/status
```

Run an age decision:

```bash
curl -X POST http://localhost:8000/estimate \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

<h2>Public contract</h2>

The main response exposes:

- `decision`
- `cred_decision_score`
- temporary `cred_score` compatibility alias
- `request_id`
- `correlation_id`
- `privacy`
- `proof`
- `rejection_reason`

`cred_decision_score` is the explicit age decision score produced by this service.

`cred_score` is kept only as a temporary compatibility alias.

<hr>

<h2>Docker image</h2>

```text
ghcr.io/credona/age-decision-core
```

<hr>

<h2>Testing</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

See LICENSE for details.
