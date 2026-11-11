#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/queue
if command -v podman >/dev/null 2>&1; then RUNNER="podman compose"; elif command -v docker >/dev/null 2>&1; then RUNNER="docker compose"; else echo 'Install Podman Compose or Docker Compose first' >&2; exit 1; fi
$RUNNER up --build -d
printf 'Started services with %s\n' "$RUNNER"
