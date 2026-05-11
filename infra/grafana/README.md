This folder contains Grafana provisioning configuration and dashboards for the Waste Portal.

Required environment variables (see infra/.env.example):
- GRAFANA_ADMIN_USER
- GRAFANA_ADMIN_PASSWORD
- GRAFANA_DB_HOST
- GRAFANA_DB_PORT
- GRAFANA_DB_USER
- GRAFANA_DB_PASSWORD
- GRAFANA_DB_NAME
- GRAFANA_SLACK_WEBHOOK_URL
- GRAFANA_BACKEND_WEBHOOK_URL

Provisioning files are mounted into the container at `/etc/grafana/provisioning`.
Dashboards are placed under `/var/lib/grafana/dashboards`.

Plugins:
- yesoreyeram-infinity-datasource (for GeoJSON/HTTP-backed panels)

Workflow:
1. Edit dashboard JSON in `infra/grafana/dashboards/`.
2. Start Grafana via docker compose. Dashboards will be auto-loaded.
3. To iterate visually: edit in UI, export JSON, and commit.
