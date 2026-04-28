#!/usr/bin/env bash
set -euo pipefail

python scripts/dev/update_all.sh
python scripts/metadata/sync_compatibility_version.py
python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py
python scripts/metadata/check_release_metadata.py

git diff --exit-code

echo "Release preparation passed."
