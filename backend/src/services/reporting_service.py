from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json


class ReportingService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_aggregated_containers(self, start, end, group_by: str = "hour", format: str = "json") -> List[Dict[str, Any]]:
        # Use precomputed aggregates if available
        if group_by == "hour":
            q = text("SELECT bucket AS period_start, entity_id, avg_fill FROM waste_fill_hourly WHERE bucket BETWEEN :start AND :end ORDER BY bucket ASC")
        else:
            q = text("SELECT day AS period_start, entity_id, avg_fill FROM waste_fill_daily WHERE day BETWEEN :start AND :end ORDER BY day ASC")

        result = await self.session.execute(q, {"start": start, "end": end})
        rows = result.fetchall()
        return [dict(r._mapping) for r in rows]

    async def get_containers_geojson(self, filters: dict) -> Dict[str, Any]:
        # For simplicity, return an empty FeatureCollection when DB is not populated
        # Try to query latest container states if a view exists
        try:
            q = text("SELECT id, ST_AsGeoJSON(location) as geo, fill_level FROM latest_containers WHERE true LIMIT 1000")
            result = await self.session.execute(q)
            rows = result.fetchall()
            features = []
            for r in rows:
                geo = json.loads(r._mapping.get("geo") or "null")
                features.append({
                    "type": "Feature",
                    "geometry": geo,
                    "properties": {
                        "id": r._mapping.get("id"),
                        "fill_level": r._mapping.get("fill_level")
                    }
                })
            return {"type": "FeatureCollection", "features": features}
        except Exception:
            return {"type": "FeatureCollection", "features": []}

    async def get_route_summaries(self, start, end, limit=100, offset=0):
        q = text("SELECT id, run_at, waste_type, isle_id, vehicle_count, containers_collected, unassigned_count, total_distance_m, total_load_liters, geometry_type FROM route_run_summary WHERE run_at BETWEEN :start AND :end ORDER BY run_at DESC LIMIT :limit OFFSET :offset")
        result = await self.session.execute(q, {"start": start, "end": end, "limit": limit, "offset": offset})
        rows = result.fetchall()
        return [dict(r._mapping) for r in rows]

    async def get_overflow_events(self, start, end, threshold=90, limit=100, offset=0):
        q = text("SELECT time_index AS ts, entity_id, fill_level FROM etwasteobserved WHERE time_index BETWEEN :start AND :end AND fill_level >= :threshold ORDER BY time_index DESC LIMIT :limit OFFSET :offset")
        result = await self.session.execute(q, {"start": start, "end": end, "threshold": threshold, "limit": limit, "offset": offset})
        rows = result.fetchall()
        return [dict(r._mapping) for r in rows]
