from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, List, Dict, Any


class RouteRepository:
    """Repository to persist and query route run summaries."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_route_summary(self, summary: Dict[str, Any]) -> None:
        q = text(
            """
            INSERT INTO route_run_summary (
                run_at, waste_type, isle_id, vehicle_count,
                containers_collected, unassigned_count, total_distance_m,
                total_load_liters, geometry_type, raw_response
            ) VALUES (
                :run_at, :waste_type, :isle_id, :vehicle_count,
                :containers_collected, :unassigned_count, :total_distance_m,
                :total_load_liters, :geometry_type, :raw_response
            )
            """
        )

        await self.session.execute(q, {
            "run_at": summary.get("run_at"),
            "waste_type": summary.get("waste_type"),
            "isle_id": summary.get("isle_id"),
            "vehicle_count": summary.get("vehicle_count"),
            "containers_collected": summary.get("containers_collected"),
            "unassigned_count": summary.get("unassigned_count"),
            "total_distance_m": summary.get("total_distance_m"),
            "total_load_liters": summary.get("total_load_liters"),
            "geometry_type": summary.get("geometry_type"),
            "raw_response": summary.get("raw_response"),
        })
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def get_route_summaries(self, start, end, limit=100, offset=0) -> List[Dict[str, Any]]:
        q = text(
            "SELECT id, run_at, waste_type, isle_id, vehicle_count, containers_collected, unassigned_count, total_distance_m, total_load_liters, geometry_type, raw_response FROM route_run_summary WHERE run_at BETWEEN :start AND :end ORDER BY run_at DESC LIMIT :limit OFFSET :offset"
        )
        result = await self.session.execute(q, {"start": start, "end": end, "limit": limit, "offset": offset})
        rows = result.fetchall()
        out = []
        for r in rows:
            out.append(dict(r._mapping))
        return out
