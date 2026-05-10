import math
from typing import List, Optional, Dict, Any
from src.clients.orion import OrionLDClient
from src.clients.vroom import VroomClient
from src.core.exceptions import VroomError


class RouteService:
    """Service for route optimization."""

    def __init__(self, orion_client: OrionLDClient, vroom_client: VroomClient):
        self.orion_client = orion_client
        self.vroom_client = vroom_client

    async def optimize_routes(self, request: "RouteOptimizeRequest") -> "RouteOptimizeResponse":
        """
        Optimize collection routes for given containers and vehicles.

        Args:
            request: RouteOptimizeRequest with filter and vehicle params

        Returns:
            RouteOptimizeResponse with optimized tours
        """
        # Step 1: Resolve candidate containers
        containers = await self._resolve_containers(request)
        
        # Step 2: Filter by fill level threshold
        filtered = [
            c for c in containers
            if c.get("fillLevel", 0) >= (request.min_fill_threshold * 100)
        ]
        
        # Step 3: Build VROOM jobs
        jobs = self._build_jobs(filtered)
        
        # Step 4: Build VROOM vehicles
        vehicles = self._build_vehicles(request)
        
        # Step 5: Call VROOM
        try:
            vroom_response = await self.vroom_client.optimize(
                jobs=jobs,
                vehicles=vehicles,
                options={}
            )
        except VroomError as e:
            raise e
        
        # Step 6: Map response
        return self._map_vroom_response(vroom_response, filtered, request)

    async def _resolve_containers(self, request: "RouteOptimizeRequest") -> List[dict]:
        """Resolve candidate containers from request filters."""
        if request.container_ids:
            # Fetch explicit container IDs
            containers = []
            for cid in request.container_ids:
                try:
                    entity = await self.orion_client.get_entity(cid)
                    container = self.orion_client._extract_entity_values(entity)
                    containers.append(container)
                except Exception:
                    continue
            return containers
        else:
            # Query by waste type and/or isle
            q_filters = []
            if request.waste_type:
                q_filters.append(f"containerType=={request.waste_type}")
            if request.isle_id:
                q_filters.append(f"isleId=={request.isle_id}")
            
            q = ";".join(q_filters) if q_filters else None
            
            entities = await self.orion_client.query_entities(
                entity_type="WasteContainer",
                attrs=["id", "location", "fillLevel", "capacity", "containerType"],
                q=q,
                limit=500
            )
            
            return [
                self.orion_client._extract_entity_values(e)
                for e in entities
            ]

    def _build_jobs(self, containers: List[dict]) -> List[Dict[str, Any]]:
        """Build VROOM jobs from containers."""
        jobs = []
        for idx, container in enumerate(containers):
            loc = container.get("location", {})
            if loc.get("type") == "Point" and loc.get("coordinates"):
                coords = loc["coordinates"]  # [lon, lat]
                
                # Calculate amount based on fill level and capacity
                fill_level = container.get("fillLevel", 0)  # 0-100 percentage
                capacity = container.get("capacity", 100)  # liters
                amount = max(1, math.ceil(fill_level / 100 * capacity))
                
                job = {
                    "id": idx,
                    "description": container.get("id", f"container_{idx}"),
                    "location": list(coords),  # [lon, lat]
                    "amount": [amount]
                }
                jobs.append(job)
        
        return jobs

    def _build_vehicles(self, request: "RouteOptimizeRequest") -> List[Dict[str, Any]]:
        """Build VROOM vehicles from request."""
        vehicles = []
        for idx in range(request.vehicle_count):
            vehicle = {
                "id": idx,
                "start": [request.depot_lon, request.depot_lat],
                "end": [request.depot_lon, request.depot_lat],
                "capacity": [request.vehicle_capacity_liters]
            }
            vehicles.append(vehicle)
        
        return vehicles

    def _map_vroom_response(
        self,
        vroom_response: dict,
        containers: List[dict],
        request: "RouteOptimizeRequest"
    ) -> "RouteOptimizeResponse":
        """Map VROOM response to RouteOptimizeResponse."""
        from ..schemas.routes import (
            RouteOptimizeResponse, RouteSummary, UnassignedContainer,
            RouteSummaryTotal
        )
        
        # Build routes
        routes = []
        total_distance = 0
        total_load = 0
        
        for route in vroom_response.get("routes", []):
            vehicle_id = route.get("vehicle")
            steps = route.get("steps", [])
            distance = route.get("distance", 0)
            load = route.get("load", 0)
            
            total_distance += distance
            total_load += load
            
            # Build ordered stops
            stops = []
            for step in steps:
                if step.get("type") == "job":
                    job_id = step.get("job")
                    if job_id is not None and job_id < len(containers):
                        stops.append({
                            "container_id": containers[job_id].get("id"),
                            "order": step.get("arrival_time"),
                            "distance_m": distance
                        })
            
            route_summary = RouteSummary(
                vehicle_id=vehicle_id,
                stops=stops,
                total_distance_m=distance,
                total_load_liters=load
            )
            routes.append(route_summary)
        
        # Build unassigned
        unassigned = []
        for job_id in vroom_response.get("unassigned", []):
            if job_id < len(containers):
                unassigned.append(
                    UnassignedContainer(
                        container_id=containers[job_id].get("id"),
                        reason="Could not assign to any vehicle"
                    )
                )
        
        return RouteOptimizeResponse(
            routes=routes,
            unassigned=unassigned,
            summary=RouteSummaryTotal(
                total_distance_m=total_distance,
                total_containers=len(containers),
                total_vehicles=request.vehicle_count
            ),
            debug=vroom_response if request.debug else None
        )
