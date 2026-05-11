import pytest
from src.services.route_service import RouteService
from src.core.exceptions import OSRMError
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_route_service_builds_jobs_from_containers(mock_orion_client, mock_vroom_client):
    """Test that route service correctly builds VROOM jobs."""
    mock_osrm_client = AsyncMock()
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client,
        osrm_client=mock_osrm_client,
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
    
    mock_osrm_client = AsyncMock()
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client,
        osrm_client=mock_osrm_client,
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
    mock_osrm_client = AsyncMock()
    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client,
        osrm_client=mock_osrm_client,
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


@pytest.mark.asyncio
async def test_route_geometry_attached_to_summary(mock_orion_client, mock_vroom_client):
    """Test that optimized routes include geometry from OSRM."""
    mock_osrm_client = AsyncMock()
    mock_osrm_client.get_routes_geometry = AsyncMock(
        return_value=[[[-8.39, 43.37], [-8.38, 43.371], [-8.39, 43.37]]]
    )

    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client,
        osrm_client=mock_osrm_client,
    )

    containers = [
        {
            "id": "urn:ngsi-ld:WasteContainer:001",
            "location": {"type": "Point", "coordinates": [-8.38, 43.371]},
            "fillLevel": 90.0,
            "capacity": 100,
        }
    ]
    service._resolve_containers = AsyncMock(return_value=containers)

    mock_vroom_client.optimize = AsyncMock(
        return_value={
            "routes": [
                {
                    "vehicle": 0,
                    "steps": [
                        {"type": "start"},
                        {"type": "job", "job": 0, "arrival_time": 120},
                        {"type": "end"},
                    ],
                    "distance": 1500,
                    "load": 90,
                }
            ],
            "unassigned": [],
        }
    )

    from src.schemas.routes import RouteOptimizeRequest

    request = RouteOptimizeRequest(
        vehicle_count=1,
        vehicle_capacity_liters=500,
        depot_lat=43.37,
        depot_lon=-8.39,
        min_fill_threshold=0.60,
    )

    response = await service.optimize_routes(request)

    assert response.routes
    assert response.routes[0].geometry
    assert response.routes[0].geometry_type == "osrm"


@pytest.mark.asyncio
async def test_route_falls_back_to_straight_line_on_osrm_error(mock_orion_client, mock_vroom_client):
    """Test fallback to straight-line geometry when OSRM is unavailable."""
    mock_osrm_client = AsyncMock()
    mock_osrm_client.get_routes_geometry = AsyncMock(side_effect=OSRMError("OSRM down"))

    service = RouteService(
        orion_client=mock_orion_client,
        vroom_client=mock_vroom_client,
        osrm_client=mock_osrm_client,
    )

    containers = [
        {
            "id": "urn:ngsi-ld:WasteContainer:001",
            "location": {"type": "Point", "coordinates": [-8.38, 43.371]},
            "fillLevel": 90.0,
            "capacity": 100,
        }
    ]
    service._resolve_containers = AsyncMock(return_value=containers)

    mock_vroom_client.optimize = AsyncMock(
        return_value={
            "routes": [
                {
                    "vehicle": 0,
                    "steps": [
                        {"type": "start"},
                        {"type": "job", "job": 0, "arrival_time": 120},
                        {"type": "end"},
                    ],
                    "distance": 1500,
                    "load": 90,
                }
            ],
            "unassigned": [],
        }
    )

    from src.schemas.routes import RouteOptimizeRequest

    request = RouteOptimizeRequest(
        vehicle_count=1,
        vehicle_capacity_liters=500,
        depot_lat=43.37,
        depot_lon=-8.39,
        min_fill_threshold=0.60,
    )

    response = await service.optimize_routes(request)

    assert response.routes
    assert response.routes[0].geometry_type == "straight_line"
    assert response.routes[0].geometry
