This folder contains TimescaleDB SQL artifacts for Phase 6 observability.

Files:
- continuous_aggregates.sql — definitions of hourly/daily aggregates and emptying events
- retention_policy.sql — compression and retention policies
- init.sh — helper script to apply the SQL files using the `TIMESCALEDB_URL` env var

Usage:
1. Ensure database is accessible and `TIMESCALEDB_URL` is set, e.g.: 
   export TIMESCALEDB_URL="postgresql://waste:password@timescaledb:5432/waste"
2. Run: `bash init.sh`

Notes:
- Scripts assume the existence of `etwasteobserved` table; verify the table name before applying.
- Retention windows: raw 30 days, hourly 1 year, daily 3 years (configurable by editing SQL files).
