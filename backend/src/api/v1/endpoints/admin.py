from fastapi import APIRouter, status, HTTPException


def create_admin_router() -> APIRouter:
    """Create router for admin endpoints."""
    router = APIRouter(prefix="/api/v1", tags=["admin"])
    
    @router.get("/entities")
    async def list_entities():
        """List all entities."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin entity management coming in Phase 7"
        )
    
    @router.post("/entities")
    async def create_entity():
        """Create a new entity."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin entity management coming in Phase 7"
        )
    
    @router.get("/entities/{entity_id}")
    async def get_entity(entity_id: str):
        """Get an entity."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin entity management coming in Phase 7"
        )
    
    @router.patch("/entities/{entity_id}")
    async def update_entity(entity_id: str):
        """Update an entity."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin entity management coming in Phase 7"
        )
    
    @router.delete("/entities/{entity_id}")
    async def delete_entity(entity_id: str):
        """Delete an entity."""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin entity management coming in Phase 7"
        )
    
    return router
