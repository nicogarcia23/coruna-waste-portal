from typing import List, Optional, Tuple
from datetime import datetime
from src.repositories.observation_repository import ObservationRepository
from src.utils.time import default_window


class HistoryService:
    """Service for historical data queries."""

    def __init__(self, observation_repo: ObservationRepository):
        self.observation_repo = observation_repo

    async def get_container_history(
        self,
        container_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[dict], int]:
        """
        Get fill level history for a container.

        Returns:
            Tuple of (observations, total_count)
        """
        if start is None or end is None:
            start, end = default_window(days=7)
        
        return await self.observation_repo.get_history(
            container_id=container_id,
            start=start,
            end=end,
            limit=limit,
            offset=offset
        )
