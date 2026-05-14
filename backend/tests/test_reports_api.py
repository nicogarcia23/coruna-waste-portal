import pytest
from fastapi.testclient import TestClient
from src.app import create_app
from src.core.security import require_operator


@pytest.fixture
def client():
    app = create_app()
    
    async def _allow_any():
        class Dummy: 
            pass
        return Dummy()

    app.dependency_overrides[require_operator] = _allow_any
    return TestClient(app)


def test_alerts_endpoint_accepts_grafana_payload(client):
    """Test that Grafana alert webhook endpoint is registered and functional."""
    payload = {"message": "Container near overflow"}
    resp = client.post("/api/v1/alerts", json=payload)
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"
