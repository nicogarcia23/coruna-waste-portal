from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.clients.orion import OrionLDClient
from src.repositories.aggregate_repository import AggregateRepository
from src.utils.time import default_window


class AnalyticsService:
    """Service for analytics and operational dashboards."""

    def __init__(
        self,
        orion_client: OrionLDClient,
        aggregate_repo: AggregateRepository
    ):
        self.orion_client = orion_client
        self.aggregate_repo = aggregate_repo

    async def get_container_overview(
        self,
        isle_id: Optional[str] = None,
        waste_type: Optional[str] = None
    ) -> dict:
        """
        Get overview stats for containers.

        Returns:
            {
                "totalContainers": int,
                "byStatus": {"needs_collection": int, ...},
                "avgFillLevel": float
            }
        """
        # Build query filters
        q = None
        filters = []
        if waste_type:
            filters.append(f"containerType=={waste_type}")
        if isle_id:
            filters.append(f"isleId=={isle_id}")
        
        if filters:
            q = ";".join(filters)
        
        # Query Orion-LD
        entities = await self.orion_client.query_entities(
            entity_type="WasteContainer",
            attrs=["id", "fillLevel", "status"],
            q=q,
            limit=1000,
            offset=0
        )
        
        # Compute stats
        total = len(entities)
        status_counts = {}
        fill_levels = []
        
        for entity in entities:
            extracted = self.orion_client._extract_entity_values(entity)
            
            status = extracted.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
            
            fill_level = extracted.get("fillLevel")
            if fill_level is not None:
                fill_levels.append(fill_level)
        
        avg_fill = sum(fill_levels) / len(fill_levels) if fill_levels else 0.0
        
        return {
            "totalContainers": total,
            "byStatus": status_counts,
            "avgFillLevel": round(avg_fill, 2)
        }

    async def get_aggregates(
        self,
        group_by: str,
        metric: str,
        granularity: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        isle_id: Optional[str] = None,
        waste_type: Optional[str] = None
    ) -> List[dict]:
        """
        Get time-bucketed aggregates.

        Args:
            group_by: "isle" or "model"
            metric: "avg", "max", "p95"
            granularity: "1h", "6h", "1d"
            start, end: Time window (defaults to last 24h)
            isle_id, waste_type: Optional filters

        Returns:
            List of aggregate results
        """
        if start is None or end is None:
            start, end = default_window(days=1)
        
        return await self.aggregate_repo.get_aggregates(
            group_by=group_by,
            metric=metric,
            granularity=granularity,
            start=start,
            end=end,
            isle_id=isle_id,
            waste_type=waste_type
        )
