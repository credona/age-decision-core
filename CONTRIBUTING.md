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
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
```

<hr>

<h2>Developer workflow</h2>

Run the full local check:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core scripts/dev/check_local.sh
```

Update generated files:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core scripts/dev/update_all.sh
```

Prepare a release:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core scripts/ci/release_prepare.sh
```

<hr>

<h2>Run tests</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/models/download_models.py
docker compose -f docker-compose.dev.yml exec age-decision-core pytest
```

<hr>

<h2>Run quality checks</h2>

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core ruff check .
docker compose -f docker-compose.dev.yml exec age-decision-core ruff format --check .
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/metadata/check_project_metadata.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/metadata/check_compatibility_metadata.py
```

<hr>

<h2>Update generated documentation</h2>

Some documentation blocks are generated from `project.json` and `compatibility.json`.

Run:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core scripts/dev/update_all.sh
```

Or run scripts individually:

```bash
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/docs/update_readme_examples.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/docs/update_docs_usage.py
docker compose -f docker-compose.dev.yml exec age-decision-core python scripts/docs/update_docs_compatibility.py
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
- developer workflow improvements
- release automation improvements

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
scripts/models/download_models.py
```

<hr>

<h2>Project metadata policy</h2>

Project identity metadata must be edited in:

```text
project.json
```

Compatibility metadata is generated from:

```text
project.json
```

using:

```text
scripts/docs/update_compatibility.py
```

Do not duplicate the service name, application name, version or contract version in environment files.

Release tags must match the version declared in `project.json`.

Example:

```text
project.json version: 2.2.0
Git tag: v2.2.0
```

<hr>

<h2>Release policy</h2>

After a successful CI run on `main`, the release automation creates a Git tag from `project.json`.

The tag then triggers:

- the GitHub release workflow
- the Docker image workflow

Do not create a release tag manually unless automation failed and the repository state has been verified.

<hr>

<h2>Model policy</h2>

When adding or changing a model, update:

- docs/models.md
- scripts/models/download_models.py
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
