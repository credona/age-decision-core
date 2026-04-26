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

<h3>v1.x - Next Improvements</h3>

- [ ] Improve confidence calibration
- [ ] Add more country rules
- [ ] Add richer benchmark reports
- [ ] Add SDK-ready examples
- [ ] Add model evaluation notes
- [ ] Add synthetic test image generation
- [ ] Add documented production deployment examples
- [ ] Add image metadata validation
- [ ] Add stricter error response documentation

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
