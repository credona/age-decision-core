<h1>Status contract (Age Decision Core)</h1>

This document describes stable, privacy-first HTTP status responses for endpoints owned by Age Decision Core. It omits roadmap-level ownership—see the central ecosystem documentation only for organizational context.

<hr>

<h2>Endpoints</h2>

Core exposes these public status-style endpoints:

<ul>
  <li><code>GET /health</code> — liveness and version contract line.</li>
  <li><code>GET /version</code> — project metadata bundle.</li>
  <li><code>GET /engine/status</code> — coarse readiness of bundled face-detection and age-estimation pipelines.</li>
</ul>

The decision endpoint (<code>POST /estimate</code>) is documented in usage and compatibility material; runtime errors returning JSON use <code>docs/error-model.md</code>.

<hr>

<h2>/health response</h2>

Stable JSON keys:

<ul>
  <li><strong>status</strong>: textual service state (<code>ok</code> when healthy).</li>
  <li><strong>service</strong>: service slug from repository metadata (<code>project.json</code>).</li>
  <li><strong>version</strong>: release semver for this deployment.</li>
  <li><strong>contract_version</strong>: public contract line aligned with semver minor series.</li>
</ul>

Excluded from public payloads: inferred age outputs, biometric confidence snapshots, undisclosed score fields, downstream raw payloads, internal thresholds or margins, timings used as diagnostics, stack traces.

<hr>

<h2>/version response</h2>

<code>GET /version</code> exposes a fixed metadata envelope derived from single-source project metadata—for example:

<ul>
  <li><strong>service_name</strong>, <strong>app_name</strong>: stable naming.</li>
  <li><strong>version</strong>: release semver.</li>
  <li><strong>contract_version</strong>: same semantics as health.</li>
  <li><strong>repository</strong>, <strong>image</strong>: provenance identifiers.</li>
</ul>

Treat any additional keys surfaced under this endpoint as regressions unless released with updated documentation.

<hr>

<h2>/engine/status response</h2>

Top-level keys are constrained to subsystem buckets:

<ul>
  <li><strong>face_detection</strong>: readiness describing the YuNet ONNX bundle (presence, path hints, loaded state).</li>
  <li><strong>age_estimation</strong>: readiness describing the ONNX or mock predictor configuration (paths, loaded flag, coarse capability notes).</li>
</ul>

These structures answer “are model assets loaded for this deployment?”—not per-request diagnostics. Responses must omit estimated ages, numerical confidence summaries, thresholds, cropped image buffers, and stack traces even when ONNX metadata lists tensor names or ranks for interoperability checks behind tests.

<hr>

<h2><code>contract_version</code> behavior</h2>

<code>contract_version</code> echoes the advertised public contract minor line for this artifact. Bump it when observable JSON contracts intentionally change according to semver and compatibility rules; callers should correlate it against published compatibility matrices instead of probing undocumented fields.

<hr>

<h2>No internal diagnostics</h2>

Public status payloads intentionally leave out profiler output, goroutine snapshots, downstream HTTP bodies, credential scores, biometric measurements, verbose parser traces, environment dumps, or anything analogous. Logs may carry richer operator detail under separate logging governance—never surfaced through these endpoints.
