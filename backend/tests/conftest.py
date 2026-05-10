import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis

# Assuming pytest is configured for async
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture
async def mock_http_client():
    """Mock httpx.AsyncClient."""
    return AsyncMock(spec=httpx.AsyncClient)


@pytest.fixture
async def mock_db_session():
    """Mock AsyncSession."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
async def mock_redis_client():
    """Mock Redis client."""
    return AsyncMock(spec=redis.Redis)


@pytest.fixture
async def mock_vroom_client(mock_http_client):
    """Mock VROOM client."""
    from src.clients.vroom import VroomClient
    return VroomClient(base_url="http://localhost:3002", http_client=mock_http_client)


@pytest.fixture
async def mock_orion_client(mock_http_client):
    """Mock Orion client."""
    from src.clients.orion import OrionLDClient
    return OrionLDClient(
        base_url="http://localhost:1026",
        http_client=mock_http_client,
        service_path="/waste"
    )


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    from src.app import create_app
    app = create_app()
    return TestClient(app)
