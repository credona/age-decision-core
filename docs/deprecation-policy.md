<h1>Deprecation policy (public contract)</h1>

This document applies to the Age Decision Core HTTP API surface and schemas owned by this repository.

<hr>

<h2>Principles</h2>

Breaking changes follow semantic versioning documented in ecosystem metadata. Consumers should pin images and integrations to tagged releases aligned with compatibility metadata.

Deprecated public fields remain documented until removal windows close. Operational metadata (for example tracing identifiers) stays stable where it is explicitly part of the public contract.

Privacy-first guarantees supersede versioning convenience: unintended exposure paths are corrected without waiting for coordinated deprecation timelines.

<hr>

<h2>What counts as the public contract</h2>

- Documented endpoints, request constraints, response JSON shapes documented in compatibility and repository docs.

- Stable status responses for <code>/health</code>, <code>/engine/status</code>, and <code>/version</code> as described in <code>docs/status-contract.md</code>.

Internal implementation details—module layout, private helpers, timings, ONNX session layouts used only behind contract tests—not part of this policy.

<hr>

<h2>Deprecated fields before removal</h2>

If a documented public field is scheduled for removal, it stays listed in changelog and docs with clear replacement guidance until the removal ships. Compatibility metadata reflects the consuming contract line (<code>contract_version</code>).

<hr>

<h2>Majors, minors, internals</h2>

Removing or renaming documented public JSON fields normally requires an ecosystem major bump unless explicitly documented as unstable or internal-only elsewhere.

Removing fields that leak privacy-sensitive data follows the correction rule below, not gradual deprecation.

Internal-only payloads (never promised in OpenAPI compatibility tables for this repo) may change in minor or patch releases when they remain non-public.

<hr>

<h2>Privacy leaks</h2>

Fields that contradict privacy guarantees—for example inferred age exposure, raw confidence, raw biometric scores unrelated to documented public aggregates, downstream raw payloads—are removed or corrected immediately in the safest release cadence compatible with CVE-style severity, rather than undergoing a deprecation period.

This repository does not document stack traces or raw downstream payloads in public responses.
