from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional
from src.services.container_service import ContainerService
from src.schemas.citizen import (
    NearbyContainerResponse, ContainerStatusResponse
)
from src.core.exceptions import OrionNotFound, OrionUnavailable, map_exception_to_http
from src.core.dependencies import get_container_service
from src.utils.geo import validate_coordinates


def create_citizen_router() -> APIRouter:
    """Create router for citizen endpoints."""
    router = APIRouter(prefix="/api/v1", tags=["citizen"])
    
    @router.get("/containers/nearby", response_model=list[NearbyContainerResponse])
    async def nearby_containers(
        lat: float = Query(..., ge=-90, le=90, description="Latitude"),
        lon: float = Query(..., ge=-180, le=180, description="Longitude"),
        radius: int = Query(500, ge=50, le=5000, description="Search radius in meters"),
        wasteType: Optional[str] = Query(None, description="Container type filter"),
        limit: int = Query(20, ge=1, le=50, description="Max results"),
        container_service: ContainerService = Depends(get_container_service),
    ):
        """Find nearby waste containers."""
        try:
            if not validate_coordinates(lat, lon):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid coordinates"
                )
            
            containers = await container_service.get_nearby_containers(
                lat=lat,
                lon=lon,
                radius=radius,
                waste_type=wasteType,
                limit=limit
            )
            
            return [
                NearbyContainerResponse(
                    id=c.get("id"),
                    name=c.get("name"),
                    containerType=c.get("containerType"),
                    fillLevel=c.get("fillLevel"),
                    status=c.get("status"),
                    distance=c.get("distance"),
                    location=c.get("location")
                )
                for c in containers
            ]
        
        except (OrionNotFound, OrionUnavailable) as e:
            raise map_exception_to_http(e)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    @router.get("/containers/{container_id}/status", response_model=ContainerStatusResponse)
    async def container_status(
        container_id: str,
        container_service: ContainerService = Depends(get_container_service),
    ):
        """Get current status of a container."""
        try:
            status_data = await container_service.get_container_status(container_id)
            return ContainerStatusResponse(**status_data)
        
        except OrionNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
        except (OrionUnavailable) as e:
            raise map_exception_to_http(e)
    
    return router
