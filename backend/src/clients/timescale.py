from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text
from typing import Optional


async def get_timescale_engine(db_url: str) -> AsyncEngine:
    """Create and return an async SQLAlchemy engine for TimescaleDB."""
    # Ensure we use asyncpg for async support
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    
    return engine


def get_session_maker(engine: AsyncEngine):
    """Create a session factory."""
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
