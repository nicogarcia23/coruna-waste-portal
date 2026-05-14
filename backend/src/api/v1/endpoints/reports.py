from fastapi import APIRouter, Depends, Query, HTTPException, Response
from typing import Optional
from datetime import datetime
from src.core.dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.reporting_service import ReportingService
from src.core.security import require_operator


def create_reports_router() -> APIRouter:
    router = APIRouter()

    @router.get("/api/v1/reports/containers/aggregated")
    async def aggregated(
        start: Optional[datetime] = Query(None),
        end: Optional[datetime] = Query(None),
        group_by: str = Query("hour", enum=["hour", "day"]),
        format: str = Query("json", enum=["json", "csv"]),
        db_session: AsyncSession = Depends(get_db_session),
        _ = Depends(require_operator)
    ):
        service = ReportingService(db_session)
        rows = await service.get_aggregated_containers(start, end, group_by, format)
        return rows

    @router.get("/api/v1/reports/containers/geojson")
    async def containers_geojson(
        fill_min: Optional[float] = Query(None),
        db_session: AsyncSession = Depends(get_db_session),
        _ = Depends(require_operator)
    ):
        service = ReportingService(db_session)
        data = await service.get_containers_geojson({"fill_min": fill_min})
        return data

    @router.get("/api/v1/reports/routes/summary")
    async def routes_summary(
        start: Optional[datetime] = Query(None),
        end: Optional[datetime] = Query(None),
        db_session: AsyncSession = Depends(get_db_session),
        _ = Depends(require_operator)
    ):
        service = ReportingService(db_session)
        rows = await service.get_route_summaries(start, end)
        return rows

    @router.get("/api/v1/reports/events/overflows")
    async def overflows(
        start: Optional[datetime] = Query(None),
        end: Optional[datetime] = Query(None),
        threshold: float = Query(90),
        db_session: AsyncSession = Depends(get_db_session),
        _ = Depends(require_operator)
    ):
        service = ReportingService(db_session)
        rows = await service.get_overflow_events(start, end, threshold)
        return rows

    @router.post("/api/v1/alerts")
    async def receive_alert(payload: dict):
        # Grafana will post alerts here. For now, log and acknowledge.
        import logging
        logger = logging.getLogger("grafana.alerts")
        logger.info("Received Grafana alert: %s", payload)
        return {"status": "ok"}

    return router
