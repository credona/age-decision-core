<h1>Error model (Age Decision Core)</h1>

This document describes standardized error responses emitted by Age Decision Core. It is scoped to Core only; gateways and downstream services may normalize further.

<hr>

<h2>ErrorResponse shape</h2>

Error bodies use one JSON envelope:

```json
{
  "request_id": "...",
  "correlation_id": "...",
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

- <code>request_id</code> and <code>correlation_id</code> correlate the failure with inbound headers when provided; identifiers are synthesized when headers are omitted (see tracing documentation in compatibility notes).

- <code>error.code</code> is a stable machine-readable code for this repository.

- <code>error.message</code> is a short, intentionally limited client-visible string—it does not include stack traces, raw downstream bodies, thresholds, numeric confidence, or inferred age values.

<hr>

<h2>HTTP usage</h2>

- Validation and client-side contract failures aligned with normalized handling use HTTP <strong>400</strong> plus an <code>ErrorResponse</code>.

- Model runtime failures on the estimation path respond with HTTP <strong>500</strong> plus an <code>ErrorResponse</code> using codes documented below—without attaching internal diagnostics to the payload.

<hr>

<h2>Known error codes</h2>

These codes originate from Core handlers and validators in this repository:

<ul>
  <li><strong>missing_file</strong>: multipart <code>file</code> absent on <code>POST /estimate</code>.</li>
  <li><strong>unsupported_file_type</strong>: uploaded content is rejected as incompatible with image processing expectations.</li>
  <li><strong>empty_file</strong>: upload present but degenerate or empty payload during validation.</li>
  <li><strong>invalid_request</strong>: other validation-domain failures routed through the standardized envelope after normalization.</li>
  <li><strong>model_runtime_error</strong>: internal model execution failure surfaced as HTTP 500 with a generic external message (<code>An internal error has occurred.</code>).</li>
</ul>

Treat additional codes listed only in changelog or transitional notes as undocumented until surfaced here and in OpenAPI for this repo.

<hr>

<h2>Forbidden fields</h2>

Public error JSON must expose <strong>only</strong> the top-level keys <code>request_id</code>, <code>correlation_id</code>, and <code>error</code>. The nested <code>error</code> object exposes <strong>only</strong> <code>code</code> and <code>message</code>.

Consumers and contract tests enforce absence of extras such as <code>detail</code> arrays mirroring frameworks, traceback fields, raw upstream errors, inferred ages, numerical confidence blobs, credential scores outside success responses, and internal thresholds.
