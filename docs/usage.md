<h1>Age Decision Core Usage</h1>

This document describes how to run and use the Core service.

For global project concepts, see:

```text
https://github.com/credona/age-decision
```

<hr>

<h2>Environment</h2>

Create a local environment file:

```bash
cp .env.example .env
```

Example:

```env
FACE_DETECTION_MODEL_PATH=models/face_detection/face_detection_yunet_2023mar.onnx
AGE_MODEL_PATH=models/age_estimation/age-gender-prediction-ONNX.onnx

USE_MOCK_MODEL=false
DEFAULT_AGE_CONFIDENCE=0.8

AGE_THRESHOLD=18
AGE_MARGIN=2
CONFIDENCE_THRESHOLD=0.7

PRIVACY_MODE=true
ENABLE_ZK_READY=true

LOG_LEVEL=INFO
LOG_FORMAT=json
```

`AGE_MARGIN` and `CONFIDENCE_THRESHOLD` are internal decision policy parameters.

They are not exposed in the public response.

Project identity metadata is stored in:

```text
project.json
```

Runtime environment files must not override:

```text
service_name
app_name
version
contract_version
```

<hr>

<h2>Model setup</h2>

Download model files locally:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

Expected files:

```text
models/face_detection/face_detection_yunet_2023mar.onnx
models/age_estimation/age-gender-prediction-ONNX.onnx
```

Model binaries are not intended to be committed to Git.

Model binaries are not intended to be embedded in the public Docker image by default.

<hr>

<h2>Run with Docker Compose</h2>

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

View logs:

```bash
docker compose -f docker-compose.dev.yml logs -f age-decision-core
```

Stop the service:

```bash
docker compose -f docker-compose.dev.yml down -v
```

<hr>

<h2>Run the public Docker image</h2>

Download models locally first:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

Run the image with mounted models:

```bash
docker run --rm \
  -p 8000:8000 \
  -v "$PWD/models:/app/models" \
  ghcr.io/credona/age-decision-core:latest
```

<hr>

<h2>Health</h2>

```bash
curl -i http://localhost:8000/health
```

Example response:

<!-- BEGIN:HEALTH_RESPONSE -->
```json
{
  "status": "ok",
  "service": "age-decision-core",
  "version": "2.1.1",
  "contract_version": "2.0"
}
```
<!-- END:HEALTH_RESPONSE -->

<hr>

<h2>Version</h2>

```bash
curl -i http://localhost:8000/version
```

Example response:

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

<hr>

<h2>Model status</h2>

```bash
curl -i http://localhost:8000/model/status
```

Example response:

```json
{
  "face_detection": {
    "model": "YuNet",
    "model_path": "models/face_detection/face_detection_yunet_2023mar.onnx",
    "loaded": true
  },
  "age_estimation": {
    "mode": "onnx",
    "use_mock_model": false,
    "model_path": "models/age_estimation/age-gender-prediction-ONNX.onnx",
    "model_loaded": true,
    "age_output_supported": true
  }
}
```

<hr>

<h2>Estimate</h2>

Basic request using the default threshold:

```bash
curl -X POST http://localhost:8000/estimate \
  -F "file=@./test-face.jpg"
```

With request tracing and majority country:

```bash
curl -X POST "http://localhost:8000/estimate?majority_country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

With explicit threshold:

```bash
curl -X POST "http://localhost:8000/estimate?age_threshold=21" \
  -F "file=@./test-face.jpg"
```

Threshold resolution order:

```text
age_threshold > majority_country > default threshold
```

<hr>

<h2>Successful response shape</h2>

```json
{
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "decision": "match",
  "threshold": {
    "type": "minimum_age",
    "value": 18,
    "source": "majority_country",
    "majority_country": "FR"
  },
  "face_detected": true,
  "face_count": 1,
  "spoof_check_required": true,
  "spoof_check": {
    "status": "required",
    "passed": null,
    "provider": null
  },
  "cred_decision_score": {
    "score": 0.86,
    "level": "high",
    "factors": {
      "model_confidence": "medium",
      "threshold_separation": "high"
    }
  },
  "privacy": {
    "image_stored": false,
    "biometric_template_stored": false,
    "estimated_age_exposed": false,
    "processing": "ephemeral",
    "zk_ready": true
  },
  "proof": {
    "type": "zk-ready",
    "status": "not_generated",
    "claim": "age_over_threshold",
    "threshold": {
      "type": "minimum_age",
      "value": 18,
      "source": "majority_country",
      "majority_country": "FR"
    }
  },
  "rejection_reason": null,
  "model_info": {
    "face_detector": "YuNet",
    "age_estimator": "age-gender-prediction-ONNX",
    "age_model_path": "models/age_estimation/age-gender-prediction-ONNX.onnx",
    "face_detection_model_path": "models/face_detection/face_detection_yunet_2023mar.onnx"
  }
}
```

<hr>

<h2>Public privacy contract</h2>

The public response does not expose:

- estimated age
- raw model confidence
- threshold distance
- internal uncertainty margin
- internal confidence threshold
- legacy `cred_score` alias

<hr>

<h2>Decision values</h2>

```text
match
no_match
uncertain
```

<hr>

<h2>Rejection reasons</h2>

```text
low_confidence
threshold_uncertain
no_face
multiple_faces
null
```

<hr>

<h2>Majority country rules</h2>

`majority_country` uses ISO 3166-1 alpha-2 country codes to resolve a default minimum age threshold.

Examples:

```text
FR -> 18
US -> 21
DE -> 18
ES -> 18
IT -> 18
UK -> 18
CA -> 18
AU -> 18
KR -> 19
JP -> 18
```

Unknown majority countries fall back to the configured default threshold.

<hr>

<h2>Compatibility metadata</h2>

Compatibility metadata is declared in:

```text
compatibility.json
```

Generated view:

<!-- BEGIN:COMPATIBILITY_METADATA -->
```json
{
  "service": "age-decision-core",
  "version": "2.1.0",
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
