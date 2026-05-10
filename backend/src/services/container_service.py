from typing import List, Optional
from src.clients.orion import OrionLDClient
from src.utils.geo import sort_by_distance, validate_coordinates
from src.utils.pagination import normalize_limit


class ContainerService:
    """Service for container queries and operations."""

    def __init__(self, orion_client: OrionLDClient):
        self.orion_client = orion_client

    async def get_nearby_containers(
        self,
        lat: float,
        lon: float,
        radius: int = 500,
        waste_type: Optional[str] = None,
        limit: int = 20
    ) -> List[dict]:
        """
        Find containers near a location.

        Args:
            lat, lon: Reference point
            radius: Search radius in meters (max 5000)
            waste_type: Optional filter
            limit: Max results (max 50)

        Returns:
            Sorted list of nearby containers with distance
        """
        # Validate coordinates
        if not validate_coordinates(lat, lon):
            raise ValueError("Invalid coordinates")
        
        # Normalize parameters
        radius = min(radius, 5000)
        limit = normalize_limit(limit, max_limit=50)
        
        # Query Orion-LD
        return await self.orion_client.nearby_containers(
            lat=lat,
            lon=lon,
            radius=radius,
            waste_type=waste_type,
            limit=limit
        )

    async def get_container_status(self, container_id: str) -> dict:
        """Get current status of a container."""
        entity = await self.orion_client.get_entity(container_id)
        
        # Extract NGSI-LD values
        status_data = self.orion_client._extract_entity_values(entity)
        
        return {
            "id": status_data.get("id"),
            "fillLevel": status_data.get("fillLevel"),
            "status": status_data.get("status"),
            "lastSeen": status_data.get("lastSeen"),
            "nextCollection": None  # Phase 4: placeholder, will be null
        }
