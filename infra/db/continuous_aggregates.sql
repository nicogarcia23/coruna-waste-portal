-- Hourly average fill level per container
CREATE MATERIALIZED VIEW IF NOT EXISTS waste_fill_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time_index) AS bucket,
  entity_id,
  AVG(fill_level) AS avg_fill,
  MAX(fill_level) AS max_fill,
  MIN(fill_level) AS min_fill,
  percentile_cont(0.95) WITHIN GROUP 
    (ORDER BY fill_level) AS p95_fill,
  COUNT(*) AS observation_count
FROM etwasteobserved
GROUP BY bucket, entity_id
WITH NO DATA;

SELECT add_continuous_aggregate_policy('waste_fill_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');

-- Daily aggregate per container
CREATE MATERIALIZED VIEW IF NOT EXISTS waste_fill_daily
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', bucket) AS day,
  entity_id,
  AVG(avg_fill) AS avg_fill,
  MAX(max_fill) AS max_fill,
  percentile_cont(0.95) WITHIN GROUP 
    (ORDER BY p95_fill) AS p95_fill,
  SUM(observation_count) AS total_observations
FROM waste_fill_hourly
GROUP BY day, entity_id
WITH NO DATA;

SELECT add_continuous_aggregate_policy('waste_fill_daily',
  start_offset => INTERVAL '2 days',
  end_offset   => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 day');

-- Emptying events (fill level drop > 40 points)
CREATE MATERIALIZED VIEW IF NOT EXISTS waste_emptying_events
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time_index) AS bucket,
  entity_id,
  COUNT(*) AS emptying_count
FROM (
  SELECT
    time_index,
    entity_id,
    fill_level,
    LAG(fill_level) OVER 
      (PARTITION BY entity_id ORDER BY time_index) AS prev_fill
  FROM etwasteobserved
) drops
WHERE prev_fill - fill_level > 40
GROUP BY bucket, entity_id
WITH NO DATA;

SELECT add_continuous_aggregate_policy('waste_emptying_events',
  start_offset => INTERVAL '3 hours',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');
