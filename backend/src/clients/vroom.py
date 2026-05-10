import httpx
from typing import Any, Dict, List, Optional
from src.core.exceptions import VroomError


class VroomClient:
    """Async client for VROOM route optimization service."""

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client

    async def optimize(
        self,
        jobs: List[Dict[str, Any]],
        vehicles: List[Dict[str, Any]],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Call VROOM to optimize routes.

        Args:
            jobs: List of job dicts with id, location, description, amount
            vehicles: List of vehicle dicts with id, start, end, capacity
            options: Additional VROOM options (e.g., time_factor, energy)

        Returns:
            VROOM response dict with routes and unassigned
        
        Raises:
            VroomError: If VROOM request fails
        """
        payload = {
            "jobs": jobs,
            "vehicles": vehicles,
            "options": options or {}
        }
        
        try:
            response = await self.http_client.post(
                f"{self.base_url}/",
                json=payload,
                timeout=60.0  # Route optimization can take time
            )
            
            if response.status_code >= 500:
                raise VroomError(f"VROOM returned status {response.status_code}: {response.text}")
            elif response.status_code >= 400:
                raise VroomError(f"Invalid VROOM request: {response.text}")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            raise VroomError(f"Failed to call VROOM: {e}")
