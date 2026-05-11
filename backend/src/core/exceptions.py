from fastapi import HTTPException, status
from typing import Any


class OrionError(Exception):
    """Base exception for Orion-LD client errors."""
    pass


class OrionNotFound(OrionError):
    """Entity not found in Orion-LD."""
    pass


class OrionUnavailable(OrionError):
    """Orion-LD service is unavailable."""
    pass


class OrionBadQuery(OrionError):
    """Malformed Orion-LD query."""
    pass


class TimescaleError(Exception):
    """Base exception for TimescaleDB errors."""
    pass


class VroomError(Exception):
    """Base exception for VROOM service errors."""
    pass


class OSRMError(Exception):
    """Base exception for OSRM service errors."""
    pass


class CacheError(Exception):
    """Base exception for Redis cache errors."""
    pass


def map_exception_to_http(exc: Exception) -> HTTPException:
    """Map internal exceptions to HTTP responses."""
    if isinstance(exc, OrionNotFound):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Container not found in context broker"
        )
    elif isinstance(exc, OrionUnavailable):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Context broker is temporarily unavailable"
        )
    elif isinstance(exc, OrionBadQuery):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid query to context broker"
        )
    elif isinstance(exc, VroomError):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Route optimization service error"
        )
    elif isinstance(exc, OSRMError):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Route geometry service error"
        )
    elif isinstance(exc, (TimescaleError, CacheError)):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Internal service temporarily unavailable"
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
