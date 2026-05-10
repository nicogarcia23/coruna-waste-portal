from contextlib import asynccontextmanager
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis
from fastapi import FastAPI
from src.core.config import get_settings


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    
    Startup: Initialize async clients for Orion, TimescaleDB, Redis, VROOM
    Shutdown: Gracefully close all connections
    """
    # Startup
    print("🚀 Starting up application...")
    
    # Initialize httpx client for Orion and VROOM calls
    http_client = httpx.AsyncClient(timeout=30.0)
    
    # Initialize TimescaleDB async engine
    # Convert postgresql:// to postgresql+asyncpg://
    db_url = settings.timescaledb_url
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(db_url, echo=False, future=True, pool_pre_ping=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Initialize Redis client
    redis_client = await redis.from_url(settings.redis_url, decode_responses=True)
    
    # Store in app state for dependency injection
    app.state.http_client = http_client
    app.state.db_engine = engine
    app.state.async_session = async_session
    app.state.redis_client = redis_client
    
    print("✅ Application startup complete")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down application...")
    
    await http_client.aclose()
    await engine.dispose()
    await redis_client.close()
    
    print("✅ Application shutdown complete")
