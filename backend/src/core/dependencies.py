from collections.abc import AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import redis.asyncio as redis
from src.core.config import get_settings
from src.clients.osrm import OSRMClient
from src.clients.orion import OrionLDClient
from src.clients.vroom import VroomClient
from src.services.container_service import ContainerService


settings = get_settings()


def get_http_client(request: Request) -> httpx.AsyncClient:
    """Get the shared HTTP client for Orion and VROOM calls."""
    return request.app.state.http_client


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Get a database session for TimescaleDB queries."""
    async_session = request.app.state.async_session
    async with async_session() as session:
        yield session


def get_redis_client(request: Request) -> redis.Redis:
    """Get the Redis client for caching."""
    return request.app.state.redis_client


def get_orion_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> OrionLDClient:
    """Build Orion-LD client using lifespan-managed HTTP client."""
    return OrionLDClient(
        base_url=settings.orion_ld_url,
        http_client=http_client,
        service_path=settings.orion_service_path,
        tenant=settings.orion_tenant,
    )


def get_vroom_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> VroomClient:
    """Build VROOM client using lifespan-managed HTTP client."""
    return VroomClient(
        base_url=settings.vroom_url,
        http_client=http_client,
    )


def get_osrm_client(request: Request) -> OSRMClient:
    """Get the OSRM client built at startup."""
    return request.app.state.osrm_client


def get_container_service(
    orion_client: OrionLDClient = Depends(get_orion_client),
) -> ContainerService:
    """Create container service for citizen routes."""
    return ContainerService(orion_client)


def get_settings_dep() -> type[type]:
    """Get settings dependency."""
    return settings
