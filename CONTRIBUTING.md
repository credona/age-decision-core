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

<h2>Run quality checks</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core ruff check .
docker compose -f docker-compose.dev.yml exec age-decision-core ruff format --check .
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/check_project_metadata.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/check_compatibility_metadata.py
```

<hr>

<h2>Update generated documentation</h2>

Some documentation blocks are generated from `project.json` and `compatibility.json`.

Run:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_readme_examples.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_docs_usage.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/update_docs_compatibility.py
```

Generated blocks are delimited by comments such as:

```text
<!-- BEGIN:HEALTH_RESPONSE -->
<!-- END:HEALTH_RESPONSE -->
```

Do not edit generated blocks manually.

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

<h2>Project metadata policy</h2>

Project identity metadata must be edited in:

```text
project.json
```

Compatibility metadata must be edited in:

```text
compatibility.json
```

Do not duplicate the service name, application name, version or contract version in environment files.

Release tags must match the version declared in `project.json`.

Example:

```text
project.json version: 2.1.0
Git tag: v2.1.0
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
- docs/compatibility.md for compatibility and contract stability rules
- CHANGELOG.md for release history
