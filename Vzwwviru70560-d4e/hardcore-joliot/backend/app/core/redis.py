"""
CHE·NU™ Redis Configuration

Redis client for caching, sessions, and real-time features.
Falls back to in-memory cache if Redis is not available.
"""

from typing import Optional, Any, Dict
import json
from contextlib import asynccontextmanager
import os

from app.core.config import settings


# ═══════════════════════════════════════════════════════════════════════════════
# IN-MEMORY FALLBACK (for development without Redis)
# ═══════════════════════════════════════════════════════════════════════════════

class InMemoryCache:
    """Simple in-memory cache for development."""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    async def get(self, key: str) -> Optional[str]:
        return self._data.get(key)
    
    async def set(self, key: str, value: str, ex: int = None) -> bool:
        self._data[key] = value
        return True
    
    async def setex(self, key: str, ttl: int, value: str) -> bool:
        self._data[key] = value
        return True
    
    async def delete(self, key: str) -> int:
        if key in self._data:
            del self._data[key]
            return 1
        return 0
    
    async def exists(self, key: str) -> int:
        return 1 if key in self._data else 0
    
    async def incrby(self, key: str, amount: int) -> int:
        val = int(self._data.get(key, 0)) + amount
        self._data[key] = str(val)
        return val
    
    async def expire(self, key: str, ttl: int) -> bool:
        return key in self._data
    
    async def ttl(self, key: str) -> int:
        return -1 if key in self._data else -2
    
    async def ping(self) -> bool:
        return True
    
    async def publish(self, channel: str, message: str) -> int:
        return 0
    
    def pubsub(self):
        return InMemoryPubSub()
    
    async def close(self):
        pass


class InMemoryPubSub:
    """Mock PubSub for development."""
    
    async def subscribe(self, *channels):
        pass
    
    async def unsubscribe(self, *channels):
        pass
    
    async def listen(self):
        # Never yields, just returns empty
        return
        yield  # Make it a generator


# ═══════════════════════════════════════════════════════════════════════════════
# REDIS CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

_redis_client: Optional[Any] = None
_use_mock = os.environ.get("USE_MOCK_REDIS", "true").lower() == "true"


async def get_redis() -> Any:
    """Get Redis client instance (or mock for development)."""
    global _redis_client
    
    if _redis_client is None:
        if _use_mock:
            _redis_client = InMemoryCache()
        else:
            try:
                import redis.asyncio as redis
                from redis.asyncio.connection import ConnectionPool
                
                pool = ConnectionPool.from_url(
                    settings.REDIS_URL,
                    max_connections=50,
                    decode_responses=True,
                )
                _redis_client = redis.Redis(connection_pool=pool)
            except Exception:
                # Fall back to mock
                _redis_client = InMemoryCache()
    
    return _redis_client


async def close_redis() -> None:
    """Close Redis connections."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

class CacheService:
    """High-level caching service."""
    
    def __init__(self, prefix: str = "chenu"):
        self.prefix = prefix
    
    def _key(self, key: str) -> str:
        """Build prefixed cache key."""
        return f"{self.prefix}:{key}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        client = await get_redis()
        value = await client.get(self._key(key))
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set value in cache."""
        client = await get_redis()
        ttl = ttl or settings.REDIS_CACHE_TTL
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        return await client.setex(self._key(key), ttl, value)
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        client = await get_redis()
        return await client.delete(self._key(key)) > 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        client = await get_redis()
        return await client.exists(self._key(key)) > 0
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment counter."""
        client = await get_redis()
        return await client.incrby(self._key(key), amount)
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL on key."""
        client = await get_redis()
        return await client.expire(self._key(key), ttl)
    
    async def ttl(self, key: str) -> int:
        """Get remaining TTL."""
        client = await get_redis()
        return await client.ttl(self._key(key))


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIALIZED CACHES
# ═══════════════════════════════════════════════════════════════════════════════

# Session cache (for auth tokens)
session_cache = CacheService(prefix="chenu:session")

# Thread hot memory cache
thread_cache = CacheService(prefix="chenu:thread")

# User preferences cache
user_cache = CacheService(prefix="chenu:user")

# Agent state cache
agent_cache = CacheService(prefix="chenu:agent")

# Rate limiting cache
rate_limit_cache = CacheService(prefix="chenu:rate")


# ═══════════════════════════════════════════════════════════════════════════════
# PUBSUB FOR REALTIME
# ═══════════════════════════════════════════════════════════════════════════════

class PubSubService:
    """Redis Pub/Sub for real-time events."""
    
    def __init__(self, prefix: str = "chenu:pubsub"):
        self.prefix = prefix
        self._pubsub = None
    
    def _channel(self, channel: str) -> str:
        """Build prefixed channel name."""
        return f"{self.prefix}:{channel}"
    
    async def publish(self, channel: str, message: dict) -> int:
        """Publish message to channel."""
        client = await get_redis()
        return await client.publish(
            self._channel(channel),
            json.dumps(message),
        )
    
    async def subscribe(self, *channels: str):
        """Subscribe to channels."""
        client = await get_redis()
        self._pubsub = client.pubsub()
        await self._pubsub.subscribe(*[self._channel(c) for c in channels])
        return self._pubsub
    
    async def unsubscribe(self, *channels: str):
        """Unsubscribe from channels."""
        if self._pubsub:
            await self._pubsub.unsubscribe(*[self._channel(c) for c in channels])
    
    async def listen(self):
        """Listen for messages (async generator)."""
        if self._pubsub:
            async for message in self._pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        yield {
                            "channel": message["channel"].replace(f"{self.prefix}:", ""),
                            "data": data,
                        }
                    except json.JSONDecodeError:
                        yield {
                            "channel": message["channel"],
                            "data": message["data"],
                        }


# Global pubsub instance
pubsub = PubSubService()


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

async def check_redis_health() -> bool:
    """Check Redis connectivity."""
    try:
        client = await get_redis()
        return await client.ping()
    except Exception:
        return False
