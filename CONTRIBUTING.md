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
```

<hr>

<h2>Run tests</h2>

```bash
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

<hr>

<h2>Documentation</h2>

Use:

- README.md for the repository entry point
- docs/usage.md for service usage
- docs/models.md for model transparency
- docs/benchmarks.md for benchmark methodology
- CHANGELOG.md for release history
