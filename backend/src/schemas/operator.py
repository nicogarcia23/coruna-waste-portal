from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContainerOverviewResponse(BaseModel):
    """Response schema for container overview."""
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
    """Response schema for history record."""
    timestamp: datetime
    fillLevel: float


class PaginatedHistoryResponse(BaseModel):
    """Response schema for paginated history."""
    items: list[HistoryRecordResponse]
    total: int
    limit: int
    offset: int
