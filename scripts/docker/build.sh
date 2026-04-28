#!/usr/bin/env bash
set -euo pipefail

IMAGE_TYPE="${1:-prod}"

read_json() {
  docker run --rm \
    -v "$PWD:/workspace" \
    -w /workspace \
    python:3.14-slim \
    python -c "import json; print(json.load(open('project.json'))$1)"
}

VERSION=$(read_json "['version']")
REPOSITORY=$(read_json "['repository']")
LICENSE=$(read_json "['docker']['license']")

case "$IMAGE_TYPE" in
  prod)
    DOCKERFILE="Dockerfile"
    IMAGE_NAME=$(read_json "['docker']['prod_image']")
    TITLE=$(read_json "['docker']['prod_title']")
    DESCRIPTION=$(read_json "['docker']['prod_description']")
    ;;
  dev)
    DOCKERFILE="Dockerfile.dev"
    IMAGE_NAME=$(read_json "['docker']['dev_image']")
    TITLE=$(read_json "['docker']['dev_title']")
    DESCRIPTION=$(read_json "['docker']['dev_description']")
    ;;
  *)
    echo "Usage: $0 [prod|dev]"
    exit 1
    ;;
esac

docker build \
  -f "$DOCKERFILE" \
  --build-arg VERSION="$VERSION" \
  --build-arg REPOSITORY="$REPOSITORY" \
  --build-arg TITLE="$TITLE" \
  --build-arg DESCRIPTION="$DESCRIPTION" \
  --build-arg LICENSE="$LICENSE" \
  -t "$IMAGE_NAME:$VERSION" \
  .
