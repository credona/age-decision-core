#!/usr/bin/env bash
set -euo pipefail

./scripts/config/generate_env.sh dev

docker compose \
  --env-file .generated/compose/dev.env \
  -f docker-compose.dev.yml \
  run --rm age-decision-core \
  ./scripts/ci/check_all.sh
