from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WasteContainerModel(BaseModel):
    id: str = Field(...)
    type: str = Field("WasteContainerModel")
    manufacturer: Optional[str] = Field(None, description="Static: manufacturer")
    modelNumber: Optional[str] = Field(None)
    capacity: Optional[int] = Field(None, description="Static: capacity in liters")
    communicationProtocol: Optional[str] = Field(None, description="Static: mqtt|http")


class WasteContainerIsleModel(BaseModel):
    id: str
    type: str = Field("WasteContainerIsle")
    name: Optional[str]
    areaServed: Optional[str]
    # location omitted: handled as raw GeoJSON


class WasteContainerModelEntity(BaseModel):
    id: str
    type: str = Field("WasteContainer")
    name: Optional[str]
    description: Optional[str]
    containerType: Optional[str]
    capacity: Optional[int]
    modelId: Optional[str]
    isleId: Optional[str]
    location: Optional[dict]
    fillLevel: Optional[float] = Field(None, description="Dynamic: fill level percentage")
    status: Optional[str] = Field(None, description="Dynamic: status")
    lastSeen: Optional[datetime]


class WasteObservedModel(BaseModel):
    id: str
    type: str = Field("WasteObserved")
    refContainer: str = Field(..., description="URN of measured container")
    fillLevel: float
    temperature: Optional[float]
    battery: Optional[int]
    dateObserved: Optional[datetime]


# Response/utility models
class NearbyContainer(BaseModel):
    id: str
    name: Optional[str]
    containerType: Optional[str]
    fillLevel: Optional[float]
    status: Optional[str]
    distance: Optional[float]
    location: Optional[dict]


class ContainerStatus(BaseModel):
    id: str
    fillLevel: Optional[float]
    status: Optional[str]
    lastSeen: Optional[datetime]
    nextCollection: Optional[datetime]


class ContainerOverview(BaseModel):
    totalContainers: int
    byStatus: dict
    avgFillLevel: Optional[float]


class AggregateResult(BaseModel):
    group: str
    metric: float
    periodStart: datetime
    periodEnd: datetime


class HistoryRecord(BaseModel):
    timestamp: datetime
    fillLevel: float
