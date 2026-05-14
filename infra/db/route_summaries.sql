CREATE TABLE IF NOT EXISTS route_run_summary (
  id          BIGSERIAL PRIMARY KEY,
  run_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  waste_type  TEXT,
  isle_id     TEXT,
  vehicle_count     INT,
  containers_collected INT,
  unassigned_count  INT,
  total_distance_m  FLOAT,
  total_load_liters FLOAT,
  geometry_type     TEXT,
  raw_response      JSONB
);

SELECT create_hypertable('route_run_summary', 'run_at', if_not_exists => TRUE);
