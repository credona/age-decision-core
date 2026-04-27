<h1>Contributing to Age Decision Core</h1>

This repository contains the Core service.

For global contribution rules, see:

```text
https://github.com/credona/age-decision/blob/main/CONTRIBUTING.md
```

<hr>

<h2>Local setup</h2>

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
```

<hr>

<h2>Run tests</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/download_models.py
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

<hr>

<h2>Contribution scope</h2>

Good Core contributions include:

- age decision policy improvements
- stable API contract improvements
- model loading improvements
- safer error handling
- privacy metadata improvements
- benchmark improvements
- tests and documentation

<hr>

<h2>Rules</h2>

Do not commit:

- private images
- biometric templates
- credentials
- generated cache folders
- local secrets
- unlicensed model files
- ONNX model binaries
- large generated artifacts

Model files must be downloaded explicitly through:

```text
scripts/download_models.py
```

<hr>

<h2>Model policy</h2>

When adding or changing a model, update:

- docs/models.md
- scripts/download_models.py
- related tests
- benchmark notes when applicable

Each model entry must document:

- model name
- source URL
- expected local path
- upstream license when known
- project usage
- known limitations
- redistribution notes

<hr>

<h2>Documentation</h2>

Use:

- README.md for the repository entry point
- docs/usage.md for service usage
- docs/models.md for model transparency and third-party notices
- docs/benchmarks.md for benchmark methodology
- CHANGELOG.md for release history
