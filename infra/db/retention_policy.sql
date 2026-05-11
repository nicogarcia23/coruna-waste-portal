-- Compression policy: compress raw data after 2 days
SELECT add_compression_policy('etwasteobserved', 
  INTERVAL '2 days');

-- Retention policy: drop raw data older than 30 days
SELECT add_retention_policy('etwasteobserved', 
  INTERVAL '30 days');

-- Retention policy: drop hourly aggregates older than 1 year
SELECT add_retention_policy('waste_fill_hourly', 
  INTERVAL '1 year');

-- Retention policy: drop daily aggregates older than 3 years
SELECT add_retention_policy('waste_fill_daily', 
  INTERVAL '3 years');
