from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.core.lifespan import lifespan
from src.core.middleware import RequestIDMiddleware
from src.core.logging import setup_logging
from src.api.v1.router import create_v1_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Setup logging
    setup_logging()
    
    # Get settings
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        lifespan=lifespan
    )
    
    # Add middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "ok"}
    
    # Register v1 routes; dependencies resolve from lifespan-managed app.state
    app.include_router(create_v1_router())
    
    return app
