import httpx
import json
from typing import Any, List, Optional
from urllib.parse import urlencode
from src.core.exceptions import OrionNotFound, OrionUnavailable, OrionBadQuery, OrionError
from src.utils.geo import haversine


class OrionLDClient:
    """Async client for Orion-LD NGSI-LD context broker."""

    def __init__(
        self,
        base_url: str,
        http_client: httpx.AsyncClient,
        service_path: str = "/waste",
        tenant: Optional[str] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client
        self.service_path = service_path
        self.tenant = tenant
        self.ngsi_ld_path = "/ngsi-ld/v1"

    def _get_headers(self) -> dict[str, str]:
        """Build common NGSI-LD headers."""
        headers = {
            "Content-Type": "application/ld+json",
            "Link": '<https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"'
        }
        if self.tenant:
            headers["FIWARE-Service"] = self.tenant
            headers["FIWARE-ServicePath"] = self.service_path
        return headers

    def _build_georel(self, lat: float, lon: float, radius: int) -> str:
        """Build georel filter for nearby query."""
        return f"near;maxDistance=={radius}"

    def _build_q_filter(self, **kwargs) -> Optional[str]:
        """Build q filter from keyword arguments."""
        conditions = []
        for key, value in kwargs.items():
            if value is not None:
                conditions.append(f"{key}=={value}")
        return ";".join(conditions) if conditions else None

    def _project_attrs(self, attrs: List[str]) -> str:
        """Build attrs projection string."""
        return ",".join(attrs)

    async def query_entities(
        self,
        entity_type: str,
        attrs: Optional[List[str]] = None,
        q: Optional[str] = None,
        georel: Optional[str] = None,
        geometry: Optional[str] = None,
        coordinates: Optional[List[float]] = None,
        geoproperty: str = "location",
        limit: int = 100,
        offset: int = 0
    ) -> List[dict]:
        """
        Query entities from Orion-LD.

        Args:
            entity_type: NGSI-LD entity type
            attrs: List of attributes to retrieve
            q: NGSI query string
            georel: Geospatial relationship (e.g., "near;maxDistance==500")
            geometry: GeoJSON geometry type (e.g., "Point")
            coordinates: GeoJSON coordinates [lon, lat]
            geoproperty: Property to use for geospatial query
            limit: Maximum number of results
            offset: Result offset for pagination

        Returns:
            List of entity dictionaries
        """
        url = f"{self.base_url}{self.ngsi_ld_path}/entities"
        
        params = {
            "type": entity_type,
            "limit": limit,
            "offset": offset
        }
        
        if attrs:
            params["attrs"] = self._project_attrs(attrs)
        
        if q:
            params["q"] = q
        
        if georel and geometry and coordinates:
            params["georel"] = georel
            params["geometry"] = geometry
            params["coordinates"] = json.dumps(coordinates)
            params["geoproperty"] = geoproperty
        
        try:
            response = await self.http_client.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise OrionNotFound(f"No entities found for type: {entity_type}")
            elif response.status_code == 503:
                raise OrionUnavailable("Orion-LD is unavailable")
            elif response.status_code == 400:
                raise OrionBadQuery(f"Invalid query parameters: {response.text}")
            elif response.status_code >= 500:
                raise OrionUnavailable(f"Orion-LD returned status {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            if "503" in str(e) or "Connection" in str(e):
                raise OrionUnavailable(f"Failed to connect to Orion-LD: {e}")
            raise OrionError(f"HTTP error querying Orion-LD: {e}")

    async def get_entity(self, entity_id: str) -> dict:
        """
        Retrieve a single entity by ID.

        Args:
            entity_id: NGSI-LD entity URN

        Returns:
            Entity dictionary

        Raises:
            OrionNotFound: If entity doesn't exist
            OrionUnavailable: If Orion-LD is unavailable
        """
        url = f"{self.base_url}{self.ngsi_ld_path}/entities/{entity_id}"
        
        try:
            response = await self.http_client.get(
                url,
                headers=self._get_headers(),
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise OrionNotFound(f"Entity not found: {entity_id}")
            elif response.status_code == 503:
                raise OrionUnavailable("Orion-LD is unavailable")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            if "503" in str(e) or "Connection" in str(e):
                raise OrionUnavailable(f"Failed to connect to Orion-LD: {e}")
            raise OrionError(f"Error fetching entity {entity_id}: {e}")

    async def nearby_containers(
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
            lat: Reference latitude
            lon: Reference longitude
            radius: Search radius in meters
            waste_type: Optional container type filter (organic, glass, paper, plastic, general)
            limit: Maximum results

        Returns:
            List of nearby containers with distance computed
        """
        q = None
        if waste_type:
            q = f"containerType=={waste_type}"
        
        entities = await self.query_entities(
            entity_type="WasteContainer",
            attrs=["id", "name", "containerType", "fillLevel", "status", "location"],
            q=q,
            georel=self._build_georel(lat, lon, radius),
            geometry="Point",
            coordinates=[lon, lat],
            geoproperty="location",
            limit=limit
        )
        
        # Extract NGSI-LD response and compute distances
        result = []
        for entity in entities:
            container = self._extract_entity_values(entity)
            if "location" in container and container["location"]:
                loc = container["location"]
                if isinstance(loc, dict) and "type" in loc and loc["type"] == "Point":
                    coords = loc.get("coordinates", [])
                    if len(coords) == 2:
                        dist = haversine(lat, lon, coords[1], coords[0])
                        container["distance"] = dist
            result.append(container)
        
        # Sort by distance
        return sorted(result, key=lambda x: x.get("distance", float("inf")))

    def _extract_entity_values(self, entity: dict) -> dict:
        """
        Extract simple property values from NGSI-LD entity.
        
        NGSI-LD format wraps values in property objects with 'value' or 'object' keys.
        This function extracts the actual values.
        """
        result = {"id": entity.get("id")}
        
        for key, prop in entity.items():
            if key in ("id", "@context"):
                continue
            
            if isinstance(prop, dict):
                if "value" in prop:
                    result[key] = prop["value"]
                elif "object" in prop:
                    result[key] = prop["object"]
                else:
                    # It might be location or other structured data
                    result[key] = prop
            else:
                result[key] = prop
        
        return result

    async def patch_entity_attrs(self, entity_id: str, attrs: dict) -> None:
        """
        Update entity attributes.

        Args:
            entity_id: NGSI-LD entity URN
            attrs: Dictionary of attributes to update (flat format, will be wrapped)
        """
        url = f"{self.base_url}{self.ngsi_ld_path}/entities/{entity_id}/attrs"
        
        # Wrap attributes in NGSI-LD format
        payload = {}
        for key, value in attrs.items():
            payload[key] = {"value": value}
        
        try:
            response = await self.http_client.patch(
                url,
                json=payload,
                headers=self._get_headers(),
                timeout=10.0
            )
            
            if response.status_code == 404:
                raise OrionNotFound(f"Entity not found: {entity_id}")
            elif response.status_code == 503:
                raise OrionUnavailable("Orion-LD is unavailable")
            
            response.raise_for_status()
        
        except httpx.HTTPError as e:
            if "503" in str(e) or "Connection" in str(e):
                raise OrionUnavailable(f"Failed to connect to Orion-LD: {e}")
            raise OrionError(f"Error updating entity {entity_id}: {e}")
