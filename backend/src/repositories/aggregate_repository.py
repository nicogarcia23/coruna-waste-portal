from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, List
from datetime import datetime
from src.utils.time import granularity_to_interval
from src.core.exceptions import TimescaleError


class AggregateRepository:
    """Repository for computing aggregates from TimescaleDB."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_aggregates(
        self,
        group_by: str,  # "isle" or "model"
        metric: str,  # "avg", "max", "p95"
        granularity: str,  # "1h", "6h", "1d"
        start: datetime,
        end: datetime,
        isle_id: Optional[str] = None,
        waste_type: Optional[str] = None
    ) -> List[dict]:
        """
        Get time-bucketed aggregates for containers.

        Args:
            group_by: Grouping dimension (isle or model)
            metric: Aggregation metric (avg, max, p95)
            granularity: Time bucket size (1h, 6h, 1d)
            start: Window start
            end: Window end
            isle_id: Optional filter by isle
            waste_type: Optional filter by waste type

        Returns:
            List of aggregate results
        """
        interval = granularity_to_interval(granularity)
        
        # Build metric expression
        if metric == "avg":
            metric_expr = "AVG(fillLevel)"
        elif metric == "max":
            metric_expr = "MAX(fillLevel)"
        elif metric == "p95":
            metric_expr = "percentile_cont(0.95) WITHIN GROUP (ORDER BY fillLevel)"
        else:
            metric_expr = "AVG(fillLevel)"
        
        # Build GROUP BY clause
        group_clause = "bucket"
        if group_by == "isle":
            group_clause += ", isleId"
        elif group_by == "model":
            group_clause += ", modelId"
        
        # Build WHERE filters
        where_filters = [
            "time_index BETWEEN :start AND :end"
        ]
        if isle_id:
            where_filters.append("isleId = :isle_id")
        if waste_type:
            where_filters.append("containerType = :waste_type")
        
        where_clause = " AND ".join(where_filters)
        
        query = text(f"""
            SELECT 
                time_bucket('{interval}', time_index) AS bucket,
                {group_clause},
                {metric_expr} AS value
            FROM etwasteobserved
            WHERE {where_clause}
            GROUP BY {group_clause}
            ORDER BY bucket ASC
        """)
        
        params = {"start": start, "end": end}
        if isle_id:
            params["isle_id"] = isle_id
        if waste_type:
            params["waste_type"] = waste_type
        
        result = await self.session.execute(query, params)
        
        aggregates = []
        for row in result.fetchall():
            bucket = row[0]
            group_value = row[1] if group_by in ("isle", "model") else None
            metric_value = row[2]
            
            aggregates.append({
                "period_start": bucket,
                "period_end": bucket + self._get_interval_timedelta(interval),
                "group": group_value or "all",
                "metric": metric_value
            })
        
        return aggregates

    def _get_interval_timedelta(self, interval: str) -> object:
        """Get timedelta for interval string."""
        from datetime import timedelta
        
        if "hour" in interval:
            hours = int(interval.split()[0])
            return timedelta(hours=hours)
        elif "day" in interval:
            days = int(interval.split()[0])
            return timedelta(days=days)
        else:
            return timedelta(hours=1)
