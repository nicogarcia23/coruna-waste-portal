from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Core service URLs
    orion_ld_url: str = Field(default="http://localhost:1026", alias="ORION_LD_URL")
    quantumleap_url: str = Field(default="http://localhost:8668", alias="QUANTUMLEAP_URL")
    timescaledb_url: str = Field(
        default="postgresql://waste:waste-dev-password@localhost:5432/waste",
        alias="TIMESCALEDB_URL"
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    vroom_url: str = Field(default="http://localhost:3002", alias="VROOM_URL")
    osrm_url: str = Field(default="http://localhost:5000", alias="OSRM_URL")

    # Orion-LD configuration
    orion_service_path: str = Field(default="/waste", alias="ORION_SERVICE_PATH")
    orion_tenant: str | None = Field(default=None, alias="ORION_TENANT")

    # Cache TTL (seconds)
    cache_ttl_nearby: int = Field(default=20, alias="CACHE_TTL_NEARBY")
    cache_ttl_status: int = Field(default=12, alias="CACHE_TTL_STATUS")
    cache_ttl_overview: int = Field(default=45, alias="CACHE_TTL_OVERVIEW")
    cache_ttl_aggregates_1h: int = Field(default=300, alias="CACHE_TTL_AGGREGATES_1H")
    cache_ttl_aggregates_6h: int = Field(default=600, alias="CACHE_TTL_AGGREGATES_6H")
    cache_ttl_aggregates_1d: int = Field(default=900, alias="CACHE_TTL_AGGREGATES_1D")
    cache_ttl_route: int = Field(default=20, alias="CACHE_TTL_ROUTE")

    # Security
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")

    # API configuration
    api_title: str = "Smart Waste Management Portal API"
    api_version: str = "0.2.0"

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
