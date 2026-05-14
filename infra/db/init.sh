#!/usr/bin/env bash
set -euo pipefail

if [ -z "${TIMESCALEDB_URL:-}" ]; then
  echo "Please set TIMESCALEDB_URL environment variable (postgres://user:pass@host:port/db)"
  exit 1
fi

psql "$TIMESCALEDB_URL" -f continuous_aggregates.sql
psql "$TIMESCALEDB_URL" -f retention_policy.sql
echo "TimescaleDB policies applied."
