from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, List, Tuple
from datetime import datetime
from src.core.exceptions import TimescaleError


class ObservationRepository:
    """Repository for WasteObserved historical data from TimescaleDB."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_latest_observation(self, container_id: str) -> Optional[dict]:
        """
        Get the latest observation for a container.

        Note: TimescaleDB table name assumes QuantumLeap's default naming.
        Verify actual table name if this queries fail.
        """
        query = text("""
            SELECT entity_id, time_index, fillLevel
            FROM etwasteobserved
            WHERE entity_id = :container_id
            ORDER BY time_index DESC
            LIMIT 1
        """)
        
        result = await self.session.execute(query, {"container_id": container_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        return {
            "entity_id": row[0],
            "timestamp": row[1],
            "fill_level": row[2]
        }

    async def get_history(
        self,
        container_id: str,
        start: datetime,
        end: datetime,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[dict], int]:
        """
        Get observation history for a container.

        Returns:
            Tuple of (observations, total_count)
        """
        # Get total count
        count_query = text("""
            SELECT COUNT(*)
            FROM etwasteobserved
            WHERE entity_id = :container_id
            AND time_index BETWEEN :start AND :end
        """)
        
        count_result = await self.session.execute(
            count_query,
            {"container_id": container_id, "start": start, "end": end}
        )
        total = count_result.scalar() or 0
        
        # Get paginated results
        query = text("""
            SELECT entity_id, time_index, fillLevel
            FROM etwasteobserved
            WHERE entity_id = :container_id
            AND time_index BETWEEN :start AND :end
            ORDER BY time_index DESC
            LIMIT :limit OFFSET :offset
        """)
        
        result = await self.session.execute(
            query,
            {
                "container_id": container_id,
                "start": start,
                "end": end,
                "limit": limit,
                "offset": offset
            }
        )
        
        observations = []
        for row in result.fetchall():
            observations.append({
                "entity_id": row[0],
                "timestamp": row[1],
                "fill_level": row[2]
            })
        
        return observations, total
