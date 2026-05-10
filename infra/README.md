## Infrastructure Notes

### OSRM Service

The Compose stack includes an `osrm` service for route geometry enrichment.

- On first startup, the container downloads the Galicia extract from Geofabrik
  (`galicia-latest.osm.pbf`) and preprocesses it with `osrm-extract`,
  `osrm-partition`, and `osrm-customize`.
- This first run can take several minutes and downloads around 100MB+.
- Processed files are persisted in the `osrm-data` Docker volume.
- Subsequent startups reuse `osrm-data` and start much faster.

Runtime URL for backend integration:

- `OSRM_URL=http://osrm:5000`