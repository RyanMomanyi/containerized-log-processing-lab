#!/usr/bin/env bash
set -euo pipefail
if command -v podman >/dev/null 2>&1; then RUNNER="podman compose"; else RUNNER="docker compose"; fi
$RUNNER ps
$RUNNER exec -T db pg_isready -U "${POSTGRES_USER:-lab}" -d "${POSTGRES_DB:-logs}"
$RUNNER exec -T db psql -U "${POSTGRES_USER:-lab}" -d "${POSTGRES_DB:-logs}" -c 'SELECT COUNT(*) AS stored_logs FROM app_logs;'
