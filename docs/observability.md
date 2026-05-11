**Observability — Grafana dashboards and runbook**

Overview
- Grafana available at http://localhost:3001
- Dashboards: Container Fill Levels, Collection Efficiency, Fleet & Route Summary, System Health

Setup
1. Copy infra/.env.example to infra/.env and fill secrets (GRAFANA_ADMIN_PASSWORD, GRAFANA_SLACK_WEBHOOK_URL)
2. Start services: `make up-all`
3. Apply TimescaleDB policies after first ingestion: `make db-init-policies` (ensure TIMESCALEDB_URL env set)

Alerts
- Container Near Overflow: fill >= 90% for 15m → Slack + backend webhook
- Stale IoT Data: no observations in last 30m → Slack + backend webhook

Dashboards
- Edit in Grafana UI and export JSON to `infra/grafana/dashboards/` to persist changes.
