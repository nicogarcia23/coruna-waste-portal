from fastapi import APIRouter, Query, Depends
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.analytics_service import AnalyticsService
from src.services.history_service import HistoryService
from src.services.route_service import RouteService
from src.clients.orion import OrionLDClient
from src.clients.vroom import VroomClient
from src.repositories.aggregate_repository import AggregateRepository
from src.repositories.observation_repository import ObservationRepository
from src.core.dependencies import get_orion_client, get_db_session, get_vroom_client
from src.core.security import require_operator
from src.schemas.operator import (
    ContainerOverviewResponse, AggregateResultResponse, 
    PaginatedHistoryResponse, HistoryRecordResponse
)
from src.schemas.routes import RouteOptimizeRequest, RouteOptimizeResponse
from src.core.exceptions import map_exception_to_http


def create_operator_router() -> APIRouter:
    """Create router for operator endpoints."""
    router = APIRouter(prefix="/api/v1", tags=["operator"])
    
    @router.get("/operators/containers/overview", response_model=ContainerOverviewResponse)
    async def containers_overview(
        isle_id: Optional[str] = Query(None),
        wasteType: Optional[str] = Query(None),
        orion_client: OrionLDClient = Depends(get_orion_client),
        db_session: AsyncSession = Depends(get_db_session),
        current_user = Depends(require_operator)
    ):
        """Get operational overview of containers."""
        try:
            analytics_service = AnalyticsService(
                orion_client=orion_client,
                aggregate_repo=AggregateRepository(db_session)
            )
            overview = await analytics_service.get_container_overview(
                isle_id=isle_id,
                waste_type=wasteType
            )
            return ContainerOverviewResponse(**overview)
        
        except Exception as e:
            raise map_exception_to_http(e)
    
    @router.get("/operators/containers/aggregates", response_model=list[AggregateResultResponse])
    async def container_aggregates(
        group_by: str = Query(..., enum=["isle", "model"]),
        metric: str = Query(..., enum=["avg", "max", "p95"]),
        granularity: str = Query(..., enum=["1h", "6h", "1d"]),
        start: Optional[datetime] = Query(None),
        end: Optional[datetime] = Query(None),
        isle_id: Optional[str] = Query(None),
        wasteType: Optional[str] = Query(None),
        orion_client: OrionLDClient = Depends(get_orion_client),
        db_session: AsyncSession = Depends(get_db_session),
        current_user = Depends(require_operator)
    ):
        """Get time-series aggregates of container metrics."""
        try:
            analytics_service = AnalyticsService(
                orion_client=orion_client,
                aggregate_repo=AggregateRepository(db_session)
            )
            aggregates = await analytics_service.get_aggregates(
                group_by=group_by,
                metric=metric,
                granularity=granularity,
                start=start,
                end=end,
                isle_id=isle_id,
                waste_type=wasteType
            )
            
            return [
                AggregateResultResponse(
                    periodStart=a["period_start"],
                    periodEnd=a["period_end"],
                    group=a["group"],
                    metric=a["metric"]
                )
                for a in aggregates
            ]
        
        except Exception as e:
            raise map_exception_to_http(e)
    
    @router.get("/operators/containers/{container_id}/history", response_model=PaginatedHistoryResponse)
    async def container_history(
        container_id: str,
        start: Optional[datetime] = Query(None),
        end: Optional[datetime] = Query(None),
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        db_session: AsyncSession = Depends(get_db_session),
        current_user = Depends(require_operator)
    ):
        """Get historical fill level data for a container."""
        try:
            history_service = HistoryService(
                observation_repo=ObservationRepository(db_session)
            )
            observations, total = await history_service.get_container_history(
                container_id=container_id,
                start=start,
                end=end,
                limit=limit,
                offset=offset
            )
            
            return PaginatedHistoryResponse(
                items=[
                    HistoryRecordResponse(
                        timestamp=obs["timestamp"],
                        fillLevel=obs["fill_level"]
                    )
                    for obs in observations
                ],
                total=total,
                limit=limit,
                offset=offset
            )
        
        except Exception as e:
            raise map_exception_to_http(e)
    
    @router.post("/operators/routes/optimize", response_model=RouteOptimizeResponse)
    async def optimize_routes(
        request: RouteOptimizeRequest,
        orion_client: OrionLDClient = Depends(get_orion_client),
        vroom_client: VroomClient = Depends(get_vroom_client),
        current_user = Depends(require_operator)
    ):
        """Optimize collection routes for given containers and vehicles."""
        try:
            route_service = RouteService(
                orion_client=orion_client,
                vroom_client=vroom_client
            )
            response = await route_service.optimize_routes(request)
            return response
        
        except Exception as e:
            raise map_exception_to_http(e)
    
    return router
