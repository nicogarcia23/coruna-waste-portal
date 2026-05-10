from src.api.v1.endpoints import citizen, operator, admin, hooks
from fastapi import APIRouter


def create_v1_router() -> APIRouter:
    """Create the main v1 router with all endpoints."""
    router = APIRouter()
    
    # Include endpoint routers
    router.include_router(citizen.create_citizen_router())
    router.include_router(operator.create_operator_router())
    router.include_router(admin.create_admin_router())
    router.include_router(hooks.create_hooks_router())
    
    return router
