<h1>Compatibility</h1>

This document describes compatibility expectations for Age Decision Core.

Age Decision Core exposes the age threshold decision contract used by downstream services such as the public API and SDK integrations.

<hr>

<h2>Scope</h2>

This document applies to the public behavior of this repository:

- HTTP endpoints
- request parameters
- public response fields
- error response structure
- privacy metadata
- proof-ready metadata
- OpenAPI schema
- project metadata
- compatibility metadata

Internal implementation details are not considered stable unless explicitly documented.

<hr>

<h2>Stable public endpoints</h2>

The following endpoints are part of the public service contract:

```text
GET /health
GET /version
GET /model/status
POST /estimate
GET /openapi.json
```

The `/estimate` endpoint is the main decision endpoint.

The `/version` endpoint exposes project metadata from `project.json`.

<hr>

<h2>Project metadata</h2>

Project metadata is stored in:

```text
project.json
```

Generated view:

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

The service name, application name, version and contract version must not be duplicated in environment files.

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is stored in:

```text
compatibility.json
```

Generated view:

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.1.1",
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

This file is machine-readable and checked by CI.

It is not a replacement for cross-repository integration tests.

<hr>

<h2>Stable public fields</h2>

The main estimate response exposes the following public fields:

```text
decision
threshold
cred_decision_score
request_id
correlation_id
privacy
proof
rejection_reason
```

These fields should remain stable throughout the v2.x release line.

<hr>

<h2>Decision values</h2>

The public decision field uses:

```text
match
no_match
uncertain
```

These values represent a probabilistic threshold decision.

They do not represent legal proof, identity proof, or certified age proof.

<hr>

<h2>Score ownership</h2>

Age Decision Core owns:

```text
cred_decision_score
```

This score represents the confidence of the threshold decision produced by Core.

Core does not own:

```text
cred_antispoof_score
cred_global_score
```

Those fields belong to other repositories in the Age Decision ecosystem.

<hr>

<h2>Privacy-first contract</h2>

The public response must not expose:

```text
estimated_age
raw model confidence
threshold distance
biometric embeddings
raw image data
legacy cred_score alias
```

This rule protects downstream integrations from depending on sensitive or unstable internals.

<hr>

<h2>Proof-ready metadata</h2>

The proof metadata is proof-ready, not proof-generating.

It may describe:

```text
claim type
threshold
proof status
proof readiness
```

It must not claim to provide a real cryptographic Zero Knowledge proof unless such proof generation is implemented and verified.

<hr>

<h2>Backward-compatible changes</h2>

The following changes are considered backward-compatible in v2.x:

- adding optional metadata fields
- adding internal logs without sensitive data
- improving validation messages without changing public error shape
- improving model loading behavior without changing response semantics
- adding tests
- adding documentation
- adding CI checks

<hr>

<h2>Breaking changes</h2>

The following changes are considered breaking:

- removing a stable public field
- renaming a stable public field
- changing decision values
- exposing estimated age again
- exposing raw confidence again
- changing score ownership
- changing endpoint paths
- changing the public error response shape
- changing request parameter names without transition

Breaking changes should be reserved for a new major version.

<hr>

<h2>Deprecated fields</h2>

Age Decision Core v2.x does not expose the legacy field:

```text
cred_score
```

New integrations must use:

```text
cred_decision_score
```

<hr>

<h2>Compatibility checks</h2>

Compatibility is checked through:

- unit contract tests
- OpenAPI contract tests
- privacy response tests
- proof metadata tests
- project metadata checks
- compatibility metadata checks
- Docker runtime checks
- release tag checks

The compatibility workflow is a baseline for v2.1.0.

Cross-repository integration tests are tracked separately in the global roadmap.

<hr>

<h2>Release checks</h2>

On tag release, CI verifies that the Git tag matches the version declared in `project.json`.

Example:

```text
project.json version: 2.1.0
expected Git tag: v2.1.0
```

A mismatched tag must fail the release workflow.

<hr>

<h2>Generated documentation</h2>

The following documentation blocks are generated from `project.json` and `compatibility.json`:

```text
HEALTH_RESPONSE
VERSION_RESPONSE
COMPATIBILITY_METADATA
```

They are updated by:

```bash
python scripts/update_readme_examples.py
python scripts/update_docs_usage.py
python scripts/update_docs_compatibility.py
```

CI fails if generated documentation is not synchronized.

<hr>

<h2>Integrator guidance</h2>

Integrators should rely on:

- documented response fields
- documented decision values
- `/version`
- `compatibility.json`
- OpenAPI schema
- changelog entries
- release tags

Integrators should not rely on:

- internal model outputs
- internal logs
- private Python classes
- undocumented metadata
- local development-only behavior
