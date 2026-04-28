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

Internal implementation details are not stable unless explicitly documented.

<hr>

<h2>Stable public endpoints</h2>

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
  "version": "2.2.1",
  "contract_version": "2.2",
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

It is synchronized from `project.json`.

Generated view:

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.2.1",
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

<h2>Stable public fields</h2>

The main estimate response exposes:

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

<hr>

<h2>Proof-ready metadata</h2>

The proof metadata is proof-ready, not proof-generating.

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
- improving developer workflow scripts
- improving release automation

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

<h2>Compatibility checks</h2>

Compatibility is checked through:

- unit contract tests
- OpenAPI contract tests
- privacy response tests
- proof metadata tests
- project metadata checks
- compatibility metadata checks
- Docker metadata checks
- release tag checks
- generated documentation checks

Run all checks:

```bash
./scripts/ci/check_all_docker.sh
```

Auto-fix generated files and run checks:

```bash
./scripts/ci/fix_all_docker.sh
```

<hr>

<h2>Generated documentation</h2>

The following documentation blocks are generated from `project.json` and `compatibility.json`:

```text
HEALTH_RESPONSE
VERSION_RESPONSE
COMPATIBILITY_METADATA
```

Do not edit generated blocks manually.

Use:

```bash
./scripts/ci/fix_all_docker.sh
```

<hr>

<h2>Release checks</h2>

On tag release, CI verifies that the Git tag matches the version declared in `project.json`.

Example:

```text
project.json version: 2.2.1
expected Git tag: v2.2.1
```

A mismatched tag must fail the release workflow.

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
