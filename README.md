<h1>Age Decision Core</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/docker.yml?branch=main&label=Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/codeql.yml?branch=main&label=CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-core" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision Core is the age threshold decision service of the Age Decision ecosystem.

<h2>Responsibility</h2>

This repository owns face detection, internal age estimation, threshold policy, and age decision scoring for Core responses.

<h2>Scope</h2>

It detects a face, runs internal age estimation, applies threshold rules, and returns a probabilistic threshold decision.

It does not expose estimated age.

It does not perform identity verification, face recognition, document verification, or legal age proof.

Public contract governance in v2.3.0 includes stable status endpoint coverage, standardized public error responses, normalized request validation errors, and enforced privacy-first forbidden field guarantees.

<hr>

<h2>When to use this repository</h2>

- you need age threshold decisions
- you want a privacy-first alternative to raw age estimation
- you are building a pre-filter before identity verification

<h2>When NOT to use this repository</h2>

- you need legal proof of age
- you need identity verification
- you need biometric authentication

<hr>

<h2>Documentation</h2>

- Repository: https://github.com/credona/age-decision-core
- Usage: docs/usage.md
- Models and third-party notices: docs/models.md
- Benchmarks: docs/benchmarks.md
- Compatibility: docs/compatibility.md
- Security: SECURITY.md
- Global architecture and ownership: https://github.com/credona/age-decision/blob/main/docs/architecture.md
- Global scoring model: https://github.com/credona/age-decision/blob/main/docs/scoring.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md
- Global project: https://github.com/credona/age-decision

<hr>

<h2>Usage example</h2>

Run one age decision request:

```bash
curl -X POST "http://localhost:8000/estimate?majority_country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

<hr>

For setup, configuration, runtime options, Docker workflows, and full contract details, see `docs/usage.md`.

<hr>

<h2>License</h2>

This repository is released under the Apache License 2.0.

See LICENSE for details.

Third-party models may have their own upstream license, origin, and redistribution terms.

See docs/models.md for model transparency notes.
