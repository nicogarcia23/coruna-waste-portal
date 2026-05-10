import pytest
from src.clients.orion import OrionLDClient
from src.core.exceptions import OrionNotFound, OrionUnavailable, OrionBadQuery
import httpx
import respx
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_orion_nearby_containers_with_respx():
    """Test nearby query with respx mocking."""
    http_client = httpx.AsyncClient()
    client = OrionLDClient(
        base_url="http://localhost:1026",
        http_client=http_client,
        service_path="/waste"
    )
    
    # Mock Orion response
    with respx.mock:
        respx.get("http://localhost:1026/ngsi-ld/v1/entities").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {
                        "id": "urn:ngsi-ld:WasteContainer:test-001",
                        "name": {"value": "Container 1"},
                        "location": {"value": {"type": "Point", "coordinates": [-8.39, 43.37]}},
                        "fillLevel": {"value": 75.0}
                    }
                ]
            )
        )
        
        result = await client.nearby_containers(
            lat=43.37,
            lon=-8.39,
            radius=500,
            waste_type="organic",
            limit=20
        )
        
        assert len(result) >= 1
        assert result[0]["id"] == "urn:ngsi-ld:WasteContainer:test-001"


@pytest.mark.asyncio
async def test_orion_extract_entity_values():
    """Test extraction of NGSI-LD entity values."""
    from unittest.mock import MagicMock
    
    client = OrionLDClient(
        base_url="http://localhost:1026",
        http_client=MagicMock(),
        service_path="/waste"
    )
    
    ngsi_entity = {
        "id": "urn:ngsi-ld:WasteContainer:test-001",
        "name": {"value": "Container 1"},
        "fillLevel": {"value": 75.0},
        "location": {"value": {"type": "Point", "coordinates": [-8.39, 43.37]}}
    }
    
    result = client._extract_entity_values(ngsi_entity)
    
    assert result["id"] == "urn:ngsi-ld:WasteContainer:test-001"
    assert result["name"] == "Container 1"
    assert result["fillLevel"] == 75.0
    assert result["location"]["type"] == "Point"
