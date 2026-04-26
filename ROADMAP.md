<h1>Age Decision Core Roadmap</h1>

This document tracks the public roadmap of Age Decision Core.

<h2>Versioning Strategy</h2>

Age Decision Core follows semantic versioning:

```text
vX.Y.Z
```

Meaning:

- `X` changes for major architectural or contract changes
- `Y` changes for feature releases
- `Z` changes for patches, automation, documentation, CI, distribution, and maintenance

Examples:

```text
v1.0.1 -> automation and distribution patch
v1.1.0 -> first feature release after v1.0
v2.0.0 -> privacy-first and Zero Knowledge architecture milestone
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

- [x] Add GitHub Actions CI
- [x] Add automated tests on pull requests
- [x] Add Docker image build
- [x] Add automated release workflow
- [x] Add automated tag-based release notes
- [x] Publish Docker image
- [x] Add CodeQL scanning
- [x] Add Dependabot configuration
- [x] Add distribution Dockerfile
- [x] Embed model files in Docker image
- [x] Add `.dockerignore`
- [x] Add `.env.example`
- [x] Move roadmap to `ROADMAP.md`


<h3>v1.0.2 - Security and Dependency Maintenance</h3>

- [x] Update FastAPI
- [x] Update Pydantic
- [x] Update Pillow
- [x] Update python-multipart
- [x] Update Requests
- [x] Update Pytest
- [x] Update NumPy
- [x] Update OpenCV headless
- [x] Keep Python 3.11 runtime for ML compatibility
- [x] Validate Docker runtime after dependency updates
- [x] Validate `/health` endpoint
- [x] Validate `/estimate` endpoint with real image


<h3>v1.1.0 - Python Runtime Upgrade</h3>

- [x] Upgrade Docker runtime from Python 3.11 to Python 3.14
- [x] Upgrade ONNX Runtime for Python 3.14 compatibility
- [x] Validate ONNX Runtime compatibility with Python 3.14
- [x] Validate OpenCV compatibility with Python 3.14
- [x] Validate `/health` endpoint
- [x] Validate `/model/status` endpoint
- [x] Validate `/estimate` endpoint with real image


<h3>v1.2.0 - API Contract Stabilization</h3>

- [x] Rename `cred_score` to `cred_decision_score`
- [x] Keep `cred_score` temporarily as legacy alias
- [x] Add stable error response schema
- [x] Add request tracing to error responses
- [x] Normalize `/estimate` response contract
- [x] Add contract tests for `cred_decision_score`
- [x] Add backward compatibility tests for `cred_score`
- [x] Add OpenAPI schema tests
- [x] Add stricter error response documentation
- [x] Update README response examples

<h3>v1.3.0 - Evaluation and Calibration</h3>

- [ ] Improve confidence calibration
- [ ] Add model evaluation notes
- [ ] Add richer benchmark reports
- [ ] Add synthetic test image generation

<h3>v1.4.0 - SDK and Production Readiness</h3>

- [ ] Add SDK-ready examples
- [ ] Add documented production deployment examples
- [ ] Add image metadata validation
- [ ] Add more country rules

<h3>v2 - Privacy-first and Zero Knowledge</h3>

- [ ] Complete privacy-first architecture
- [ ] Full Zero Knowledge proof
- [ ] Verifiable claim without exposing estimated age
- [ ] Proof generation module
- [ ] Proof verification module
- [ ] SDK-friendly proof API
- [ ] Verifiable decision claim format
- [ ] Public proof verification example

<h3>v3 - Image Sequence and Video</h3>

- [ ] Image sequence input
- [ ] Short video input
- [ ] Temporal consistency checks
- [ ] Advanced liveness validation
- [ ] Stronger spoof resistance
