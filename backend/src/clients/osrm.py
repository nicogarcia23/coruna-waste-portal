import asyncio
from typing import List, Tuple

import httpx

from src.core.exceptions import OSRMError


class OSRMClient:
    """Async client for OSRM route geometry service."""

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client

    async def get_route_geometry(
        self,
        waypoints: List[Tuple[float, float]],
    ) -> List[List[float]]:
        """Get route geometry from OSRM for ordered waypoints (lat, lon)."""
        if len(waypoints) < 2:
            return [[float(lon), float(lat)] for lat, lon in waypoints]

        coords = ";".join(f"{lon},{lat}" for lat, lon in waypoints)

        try:
            response = await self.http_client.get(
                f"{self.base_url}/route/v1/driving/{coords}",
                params={
                    "overview": "full",
                    "geometries": "geojson",
                    "steps": "false",
                },
                timeout=20.0,
            )
            response.raise_for_status()

            payload = response.json()
            routes = payload.get("routes", [])
            if not routes:
                raise OSRMError("OSRM returned no routes")

            geometry = routes[0].get("geometry", {})
            if geometry.get("type") != "LineString":
                raise OSRMError("OSRM returned invalid geometry type")

            coordinates = geometry.get("coordinates", [])
            if not isinstance(coordinates, list):
                raise OSRMError("OSRM returned invalid coordinates")

            return [[float(point[0]), float(point[1])] for point in coordinates]

        except httpx.HTTPError as exc:
            raise OSRMError(f"OSRM request failed: {exc}") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise OSRMError(f"OSRM response parsing failed: {exc}") from exc

    async def get_routes_geometry(
        self,
        routes: List[List[Tuple[float, float]]],
    ) -> List[List[List[float]]]:
        """Get route geometry for multiple vehicle routes in parallel."""
        tasks = [self.get_route_geometry(waypoints) for waypoints in routes]
        return await asyncio.gather(*tasks)
