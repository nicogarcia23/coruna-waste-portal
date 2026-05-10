from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class WasteTypeEnum(str, Enum):
    organic = "organic"
    glass = "glass"
    paper = "paper"
    plastic = "plastic"
    general = "general"


class GranularityEnum(str, Enum):
    one_hour = "1h"
    six_hours = "6h"
    one_day = "1d"


class MetricEnum(str, Enum):
    avg = "avg"
    max = "max"
    p95 = "p95"


class RouteStop(BaseModel):
    """A stop in an optimized route."""
    container_id: str
    order: Optional[int] = None
    distance_m: Optional[float] = None


class RouteSummary(BaseModel):
    """Summary of a single vehicle's route."""
    vehicle_id: int
    stops: List[RouteStop]
    total_distance_m: float
    total_load_liters: float


class UnassignedContainer(BaseModel):
    """Container that could not be assigned to any vehicle."""
    container_id: str
    reason: str = "Could not assign to any vehicle"


class RouteSummaryTotal(BaseModel):
    """Overall route optimization summary."""
    total_distance_m: float
    total_containers: int
    total_vehicles: int


class RouteOptimizeRequest(BaseModel):
    """Request schema for route optimization."""
    container_ids: Optional[List[str]] = None
    waste_type: Optional[WasteTypeEnum] = None
    isle_id: Optional[str] = None
    min_fill_threshold: float = Field(0.60, ge=0.0, le=1.0)
    vehicle_count: int = Field(1, ge=1, le=20)
    vehicle_capacity_liters: int = Field(ge=100, le=50000)
    depot_lat: float = Field(ge=-90, le=90)
    depot_lon: float = Field(ge=-180, le=180)
    debug: bool = False


class RouteOptimizeResponse(BaseModel):
    """Response schema for route optimization."""
    routes: List[RouteSummary]
    unassigned: List[UnassignedContainer]
    summary: RouteSummaryTotal
    debug: Optional[dict] = None
