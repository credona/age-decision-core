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

<hr>

<h2>Model setup</h2>

Download model files locally:

```bash
python scripts/download_models.py
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

```json
{
  "status": "ok",
  "service": "age-decision-core"
}
```

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

Basic request:

```bash
curl -X POST http://localhost:8000/estimate \
  -F "file=@./test-face.jpg"
```

With request tracing:

```bash
curl -X POST "http://localhost:8000/estimate?country=FR" \
  -H "X-Request-ID: test-request-001" \
  -H "X-Correlation-ID: test-correlation-001" \
  -F "file=@./test-face.jpg"
```

With explicit threshold:

```bash
curl -X POST "http://localhost:8000/estimate?country=US&age_threshold=18" \
  -F "file=@./test-face.jpg"
```

With confidence threshold:

```bash
curl -X POST "http://localhost:8000/estimate?country=FR&confidence_threshold=0.9" \
  -F "file=@./test-face.jpg"
```

<hr>

<h2>Successful response shape</h2>

```json
{
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "estimated_age": 76.0,
  "confidence": 0.8,
  "is_adult": true,
  "decision": "adult",
  "threshold": 18,
  "age_margin": 2,
  "confidence_threshold": 0.7,
  "country": "FR",
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
      "age_confidence": 0.8,
      "threshold_distance": 58.0
    }
  },
  "cred_score": {
    "score": 0.86,
    "level": "high",
    "factors": {
      "age_confidence": 0.8,
      "threshold_distance": 58.0
    }
  },
  "privacy": {
    "image_stored": false,
    "biometric_template_stored": false,
    "processing": "ephemeral",
    "zk_ready": true
  },
  "proof": {
    "type": "zk-ready",
    "status": "not_generated",
    "claim": "age_over_threshold",
    "threshold": 18
  },
  "rejection_reason": null
}
```

<hr>

<h2>Error response shape</h2>

Error responses follow a stable JSON format.

The API does not expose internal exception details.

```json
{
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "error": {
    "code": "unsupported_file_type",
    "message": "Invalid request."
  }
}
```

Known error codes:

```text
empty_file
unsupported_file_type
invalid_request
model_runtime_error
```

<hr>

<h2>Decision values</h2>

```text
adult
minor
unknown
```

<hr>

<h2>Rejection reasons</h2>

```text
low_confidence
age_uncertain
no_face
multiple_faces
null
```

<hr>

<h2>Country rules</h2>

Country rules use ISO 3166-1 alpha-2 country codes.

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

Unknown countries fall back to the configured default threshold.
