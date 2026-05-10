from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContainerStatusResponse(BaseModel):
    """Response schema for container status endpoint."""
    id: str
    fillLevel: Optional[float] = None
    status: Optional[str] = None
    lastSeen: Optional[datetime] = None
    nextCollection: Optional[datetime] = None


class NearbyContainerResponse(BaseModel):
    """Response schema for nearby containers endpoint."""
    id: str
    name: Optional[str] = None
    containerType: Optional[str] = None
    fillLevel: Optional[float] = None
    status: Optional[str] = None
    distance: Optional[float] = None
    location: Optional[dict] = None


class ContainerOverviewResponse(BaseModel):
    """Response schema for overview endpoint."""
    totalContainers: int
    byStatus: dict
    avgFillLevel: float


class AggregateResultResponse(BaseModel):
    """Response schema for aggregate results."""
    periodStart: datetime
    periodEnd: datetime
    group: str
    metric: float


class HistoryRecordResponse(BaseModel):
    """Response schema for individual history records."""
    timestamp: datetime
    fillLevel: float


class PaginatedHistoryResponse(BaseModel):
    """Response schema for paginated history."""
    items: list[HistoryRecordResponse]
    total: int
    limit: int
    offset: int
