<h1>Age Decision Core</h1>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/ci.yml?branch=main&label=CI" alt="CI">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/docker.yml?branch=main&label=Docker">
  <img src="https://img.shields.io/github/actions/workflow/status/credona/age-decision-core/codeql.yml?branch=main&label=CodeQL">
  <img src="https://img.shields.io/github/v/release/credona/age-decision-core" alt="Release">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License">
</p>

Age Decision Core is the main inference service of the Age Decision project.

It estimates whether a person appears to be above a configurable age threshold from a face image and returns a probabilistic decision.

The service is designed as a privacy-first, traceable, and API-friendly core component.

<h2>Features</h2>

- FastAPI service
- Local Docker development setup
- Distribution Docker image
- GitHub Actions CI
- Automated tests on pull requests
- Automated release workflow
- CodeQL scanning
- Dependabot configuration
- YuNet face detection
- ONNX age estimation
- Country-based threshold rules
- Request-level threshold override
- `request_id` and `correlation_id`
- Structured JSON logs
- Probabilistic decision policy
- `cred_score`
- Privacy metadata
- ZK-ready proof placeholder
- Unit and integration tests
- Benchmark script

<h2>Current Status</h2>

Age Decision Core is currently at version `v1.0.2`.

Current test status:

```text
19 passed
```

Current benchmark result:

```text
Requests: 20
Success: 20/20
Avg latency: 0.2186s
P95 latency: 0.2485s
```

<h2>Docker Image</h2>

The distribution image is published on GitHub Container Registry:

```text
ghcr.io/credona/age-decision-core:v1.0.2
```

Run the image:

```bash
docker run --rm -p 8000:8000 ghcr.io/credona/age-decision-core:v1.0.2
```

Example `docker-compose.yml` usage:

```yaml
services:
  age-decision-core:
    image: ghcr.io/credona/age-decision-core:v1.0.2
    ports:
      - "8000:8000"
    env_file:
      - .env
```

Only runtime behavior parameters should be configured through environment variables.

Service name, application name, and version are managed internally by the project.

<h2>Repository Structure</h2>

```text
age-decision-core/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── codeql.yml
│       ├── docker.yml
│       └── release.yml
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── domain/
│   │   ├── cred_score.py
│   │   ├── decision_policy.py
│   │   ├── privacy.py
│   │   └── proof.py
│   ├── models/
│   │   ├── age_predictor.py
│   │   └── model_loader.py
│   ├── policies/
│   │   └── country_rules.py
│   ├── schemas/
│   │   └── estimate.py
│   ├── services/
│   │   └── age_estimation_service.py
│   ├── utils/
│   │   └── logger.py
│   ├── vision/
│   │   ├── face_cropper.py
│   │   ├── face_detector.py
│   │   ├── face_preprocessor.py
│   │   └── image_loader.py
│   ├── config.py
│   └── main.py
├── models/
├── scripts/
│   ├── benchmark.py
│   └── download_models.py
├── tests/
│   ├── integration/
│   └── unit/
├── .dockerignore
├── .env.example
├── .env.dev.example
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.dev.yml
├── requirements.txt
├── pytest.ini
├── LICENSE
├── README.md
└── ROADMAP.md
```

<h2>Architecture</h2>

```text
api/       FastAPI routes, headers, query parameters, HTTP errors
services/  Main application orchestration
domain/    Pure business logic
schemas/   Pydantic response contracts
vision/    Image loading, face detection, cropping, preprocessing
models/    ONNX model loading and prediction
policies/  Country threshold rules
utils/     Logging utilities
```

<h2>Environment Variables</h2>

Copy the example environment file:

```bash
cp .env.example .env
```

Example `.env`:

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

For local development, use:

```bash
cp .env.dev.example .env
```

<h2>Local Development with Docker</h2>

The Docker configuration in this repository is intended for local development only.

It does not represent the production deployment configuration of Credona hosted services.

Start the service:

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
```

Check containers:

```bash
docker compose -f docker-compose.dev.yml ps
```

View logs:

```bash
docker compose -f docker-compose.dev.yml logs -f age-decision-core
```

<h2>API Endpoints</h2>

<h3>Health Check</h3>

```bash
curl -i http://localhost:8000/health
```

Response:

```json
{
  "status": "ok",
  "service": "age-decision-core"
}
```

<h3>Model Status</h3>

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

<h3>Estimate</h3>

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

With explicit threshold override:

```bash
curl -X POST "http://localhost:8000/estimate?country=US&age_threshold=18" \
  -F "file=@./test-face.jpg"
```

With confidence threshold override:

```bash
curl -X POST "http://localhost:8000/estimate?country=FR&confidence_threshold=0.9" \
  -F "file=@./test-face.jpg"
```

<h2>Estimate Response Example</h2>

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
  "rejection_reason": null,
  "request_policy": {
    "threshold_source": "country",
    "country": "FR",
    "threshold": 18,
    "age_margin": 2,
    "confidence_threshold": 0.7
  },
  "model_info": {
    "face_detector": "YuNet",
    "age_estimator": "age-gender-prediction-ONNX",
    "age_model_path": "models/age_estimation/age-gender-prediction-ONNX.onnx",
    "face_detection_model_path": "models/face_detection/face_detection_yunet_2023mar.onnx"
  }
}
```

<h2>Decision Policy</h2>

Threshold resolution priority:

1. Explicit `age_threshold` query parameter
2. Country rule
3. Default configured threshold

Decision values:

```text
adult
minor
unknown
```

Rejection reasons:

```text
low_confidence
age_uncertain
no_face
multiple_faces
null
```

<h2>Country Rules</h2>

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

Unknown countries fall back to the default configured threshold.

<h2>Cred Score</h2>

`cred_score` is a normalized credibility score for the returned probabilistic decision.

It is not a legal proof, identity proof, or mathematical proof.

It reflects decision confidence using:

- model confidence
- distance from the configured age threshold
- final decision status

Example:

```json
{
  "score": 0.86,
  "level": "high",
  "factors": {
    "age_confidence": 0.8,
    "threshold_distance": 58.0
  }
}
```

<h2>Privacy Metadata</h2>

Age Decision Core follows a privacy-first processing model.

Current guarantees:

- raw images are not stored
- biometric templates are not stored
- processing is ephemeral
- logs do not contain raw images, base64 payloads, embeddings, or file paths

Example:

```json
{
  "image_stored": false,
  "biometric_template_stored": false,
  "processing": "ephemeral",
  "zk_ready": true
}
```

<h2>ZK-Ready Proof Placeholder</h2>

Version `v1.0.2` does not generate a real Zero Knowledge proof.

It only exposes a future-proof response contract for a later proof system.

Full Zero Knowledge proof generation is planned for `v2`.

<h2>Roadmap</h2>

The roadmap has been moved to:

```text
ROADMAP.md
```

<h2>License</h2>

This project is licensed under the Apache License 2.0.

See the `LICENSE` file for details.
