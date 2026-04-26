<h1>Age Decision Core</h1>

Age Decision Core is the main inference service of the Age Decision project.

It estimates whether a person appears to be above a configurable age threshold from a face image and returns a probabilistic decision.

The service is designed as a privacy-first, traceable, and API-friendly core component.

<h2>Features</h2>

- FastAPI service
- Local Docker development setup
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

Age Decision Core is currently at version `v1.0.0`.

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

<h2>Repository Structure</h2>

```text
age-decision-core/
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
├── Dockerfile.dev
├── docker-compose.dev.yml
├── requirements.txt
├── pytest.ini
├── LICENSE
└── README.md
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

Example `.env`:

```env
APP_NAME=Age Decision Core
APP_VERSION=1.0.0
SERVICE_NAME=age-decision-core

CORE_PORT=8000

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

Version `v1.0.0` does not generate a real Zero Knowledge proof.

It only exposes a future-proof response contract for a later proof system.

Example:

```json
{
  "type": "zk-ready",
  "status": "not_generated",
  "claim": "age_over_threshold",
  "threshold": 18
}
```

Full Zero Knowledge proof generation is planned for `v2`.

<h2>Structured JSON Logs</h2>

Every `/estimate` call emits structured JSON logs.

Example:

```json
{
  "timestamp": "2026-04-25T18:41:34.457537+00:00",
  "service": "age-decision-core",
  "version": "1.0.0",
  "level": "info",
  "event": "age_decision_completed",
  "request_id": "test-request-001",
  "correlation_id": "test-correlation-001",
  "decision": "adult",
  "rejection_reason": null,
  "threshold": 18,
  "country": "FR",
  "face_count": 1,
  "confidence": 0.8,
  "estimated_age": 76.0,
  "cred_score": 0.86,
  "cred_score_level": "high",
  "spoof_check_required": true,
  "spoof_check_status": "required",
  "privacy_mode": true,
  "zk_ready": true
}
```

View logs:

```bash
docker compose -f docker-compose.dev.yml logs -f age-decision-core
```

<h2>Benchmark</h2>

Run the benchmark script:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/benchmark.py
```

Example result:

```text
--- Benchmark Results ---
Requests: 20
Success: 20/20
Min latency: 0.2007s
Max latency: 0.2491s
Avg latency: 0.2186s
P95 latency: 0.2485s
```

<h2>Testing</h2>

Run all tests:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

Current result:

```text
19 passed
```

Test structure:

```text
tests/
├── integration/
│   ├── assets/
│   ├── test_estimate_real_image.py
│   └── test_privacy_response.py
└── unit/
    ├── api/
    └── domain/
```

<h2>Model Files</h2>

Model files are expected in:

```text
models/face_detection/face_detection_yunet_2023mar.onnx
models/age_estimation/age-gender-prediction-ONNX.onnx
```

Download models:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

<h2>Scope</h2>

Age Decision Core does not perform:

- identity verification
- document verification
- biometric matching
- anti-spoofing execution
- gender prediction
- emotion prediction
- real Zero Knowledge proof generation in v1.0.0

Its purpose is to:

- detect a single face
- estimate age
- apply a threshold policy
- return a probabilistic decision
- expose traceable and privacy-first metadata

<h2>Anti-Spoofing</h2>

Anti-spoofing is intentionally handled outside this repository.

The response currently includes:

```json
{
  "spoof_check": {
    "status": "required",
    "passed": null,
    "provider": null
  }
}
```

Anti-spoofing is handled by:

```text
age-decision-antispoof
```

<h2>Roadmap</h2>

<h3>v1.0.0 - Credona Initial Public Release</h3>

- [x] Migrate repository to Credona
- [x] Provide clean open source snapshot
- [x] Add Apache License 2.0
- [x] Add FastAPI inference service
- [x] Add YuNet face detection
- [x] Add ONNX age estimation
- [x] Add probabilistic decision policy
- [x] Add `cred_score`
- [x] Add privacy-first response metadata
- [x] Add ZK-ready proof placeholder
- [x] Add structured JSON logs
- [x] Add unit tests
- [x] Add integration tests
- [x] Add benchmark script
- [x] Add local Docker development setup
- [x] Add README documentation

<h3>v1.0.1 - Automation and Distribution</h3>

- [ ] Add GitHub Actions CI
- [ ] Add automated tests on pull requests
- [ ] Add Docker image build
- [ ] Add automated release workflow
- [ ] Add automated tag-based release notes
- [ ] Publish Docker image
- [ ] Add CodeQL scanning
- [ ] Add Dependabot configuration

<h3>v1.x - Next Improvements</h3>

- [ ] Improve confidence calibration
- [ ] Add more country rules
- [ ] Add richer benchmark reports
- [ ] Add SDK-ready examples
- [ ] Add model evaluation notes
- [ ] Add synthetic test image generation

<h3>v2 - Privacy-first and Zero Knowledge</h3>

- [ ] Complete privacy-first architecture
- [ ] Full Zero Knowledge proof
- [ ] Verifiable claim without exposing estimated age
- [ ] Proof generation module
- [ ] Proof verification module
- [ ] SDK-friendly proof API

<h3>v3 - Image Sequence and Video</h3>

- [ ] Image sequence input
- [ ] Short video input
- [ ] Temporal consistency checks
- [ ] Advanced liveness validation
- [ ] Stronger spoof resistance

<h2>License</h2>

This project is licensed under the Apache License 2.0.

See the `LICENSE` file for details.