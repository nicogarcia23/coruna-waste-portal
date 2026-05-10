from fastapi import APIRouter, status


def create_hooks_router() -> APIRouter:
    """Create router for webhook endpoints."""
    router = APIRouter(prefix="/api/v1", tags=["webhooks"])
    
    @router.post("/hooks/orion", status_code=status.HTTP_200_OK)
    async def orion_webhook(payload: dict):
        """
        Webhook receiver for Orion-LD entity change notifications.
        
        Used to trigger cache invalidation when entity data changes.
        """
        # Extract entity IDs from the notification payload
        # Format varies; basic approach shown here
        try:
            # In a real deployment, parse the NGSI-LD subscription notification
            # and extract affected entity IDs, then purge related cache keys
            
            # For now, log and acknowledge
            print(f"Received Orion webhook: {payload}")
            
            # TODO Phase 5+: Implement targeted cache invalidation
            # based on entity IDs from the notification
            
            return {"status": "received"}
        
        except Exception as e:
            print(f"Error processing Orion webhook: {e}")
            return {"status": "error", "detail": str(e)}
    
    return router
