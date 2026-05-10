import pytest
from fastapi.testclient import TestClient
from src.app import create_app
from unittest.mock import patch, AsyncMock


def test_health_endpoint():
    """Test that /health endpoint is accessible."""
    app = create_app()
    client = TestClient(app)
    
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.skip(reason="Requires full stack setup")
def test_nearby_containers_returns_200_with_valid_coords():
    """Test nearby containers endpoint returns 200 with valid coordinates."""
    # This requires the full Compose stack running
    pass


@pytest.mark.skip(reason="Requires full stack setup")
def test_route_optimization_returns_valid_response():
    """Test route optimization endpoint returns valid response."""
    # This requires the full Compose stack running
    pass
