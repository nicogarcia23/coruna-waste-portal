import redis.asyncio as redis
import json
from typing import Optional, Any
import hashlib
from src.core.exceptions import CacheError


class RedisClient:
    """Wrapper around redis.asyncio for caching."""

    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        try:
            return await self.client.get(key)
        except redis.RedisError as e:
            raise CacheError(f"Redis get error: {e}")

    async def set(self, key: str, value: str, ttl: int) -> None:
        """Set value in cache with TTL (seconds)."""
        try:
            await self.client.setex(key, ttl, value)
        except redis.RedisError as e:
            raise CacheError(f"Redis set error: {e}")

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        try:
            await self.client.delete(key)
        except redis.RedisError as e:
            raise CacheError(f"Redis delete error: {e}")

    async def delete_pattern(self, pattern: str) -> None:
        """Delete all keys matching pattern."""
        try:
            cursor = 0
            while True:
                cursor, keys = await self.client.scan(cursor, match=pattern)
                if keys:
                    await self.client.delete(*keys)
                if cursor == 0:
                    break
        except redis.RedisError as e:
            raise CacheError(f"Redis pattern delete error: {e}")

    def cache_key(self, *parts: str) -> str:
        """Build a cache key from parts."""
        return ":".join(parts)

    def payload_hash(self, payload: dict) -> str:
        """Hash a payload for cache key."""
        json_str = json.dumps(payload, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
