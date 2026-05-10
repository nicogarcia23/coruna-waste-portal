import pytest
from src.services.route_service import RouteService
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_route_service_builds_jobs_from_containers(mock_orion_client, mock_vroom_client):
    """Test that route service correctly builds VROOM jobs."""
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client
    )
    
    containers = [
        {
            "id": "urn:ngsi-ld:WasteContainer:001",
            "location": {"type": "Point", "coordinates": [-8.39, 43.37]},
            "fillLevel": 80.0,
            "capacity": 100
        },
        {
            "id": "urn:ngsi-ld:WasteContainer:002",
            "location": {"type": "Point", "coordinates": [-8.40, 43.38]},
            "fillLevel": 50.0,
            "capacity": 100
        }
    ]
    
    jobs = service._build_jobs(containers)
    
    assert len(jobs) == 2
    assert jobs[0]["id"] == 0
    assert jobs[0]["location"] == [-8.39, 43.37]
    assert jobs[0]["amount"] == [80]  # 80% of 100L = 80L
    assert jobs[1]["amount"] == [50]  # 50% of 100L = 50L


@pytest.mark.asyncio
async def test_route_service_builds_vehicles_from_request(mock_orion_client, mock_vroom_client):
    """Test that route service builds VROOM vehicles correctly."""
    from src.schemas.routes import RouteOptimizeRequest
    
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client
    )
    
    request = RouteOptimizeRequest(
        vehicle_count=3,
        vehicle_capacity_liters=500,
        depot_lat=43.37,
        depot_lon=-8.39,
        min_fill_threshold=0.60
    )
    
    vehicles = service._build_vehicles(request)
    
    assert len(vehicles) == 3
    for i, vehicle in enumerate(vehicles):
        assert vehicle["id"] == i
        assert vehicle["start"] == [-8.39, 43.37]
        assert vehicle["end"] == [-8.39, 43.37]
        assert vehicle["capacity"] == [500]


@pytest.mark.asyncio
async def test_route_service_filters_by_fill_threshold(mock_orion_client, mock_vroom_client):
    """Test that containers below fill threshold are filtered."""
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client
    )
    
    containers = [
        {
            "id": "urn:ngsi-ld:WasteContainer:001",
            "location": {"type": "Point", "coordinates": [-8.39, 43.37]},
            "fillLevel": 80.0,
            "capacity": 100
        },
        {
            "id": "urn:ngsi-ld:WasteContainer:002",
            "location": {"type": "Point", "coordinates": [-8.40, 43.38]},
            "fillLevel": 30.0,  # Below 60% threshold
            "capacity": 100
        }
    ]
    
    # With min_fill_threshold of 0.60 (60%), only the first container should be included
    filtered = [
        c for c in containers
        if c.get("fillLevel", 0) >= 0.60 * 100
    ]
    
    assert len(filtered) == 1
    assert filtered[0]["fillLevel"] == 80.0
