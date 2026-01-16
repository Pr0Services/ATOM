"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — REDIS CACHE MANAGER
═══════════════════════════════════════════════════════════════════════════════
Tri-layer memory caching with Redis
═══════════════════════════════════════════════════════════════════════════════
"""

import redis.asyncio as redis
from typing import Optional, Any, Dict, List
import json
import logging
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE KEY PREFIXES
# ═══════════════════════════════════════════════════════════════════════════════

class CachePrefix:
    """Cache key prefixes for different domains."""
    
    # Core entities
    THREAD = "thread"
    CHECKPOINT = "checkpoint"
    IDENTITY = "identity"
    SPHERE = "sphere"
    WORKSPACE = "workspace"
    DATASPACE = "dataspace"
    
    # Memory layers (Rule #6: Traceability)
    MEMORY_HOT = "memory:hot"
    MEMORY_WARM = "memory:warm"
    MEMORY_SNAPSHOT = "memory:snapshot"
    
    # Nova pipeline
    NOVA_CONTEXT = "nova:context"
    NOVA_RESULT = "nova:result"
    
    # Sessions
    SESSION = "session"
    USER = "user"
    
    # Governance (Rule #1: Human Sovereignty)
    PENDING_CHECKPOINT = "pending:checkpoint"


# ═══════════════════════════════════════════════════════════════════════════════
# REDIS CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

class RedisCache:
    """
    Redis cache manager for CHE·NU V76.
    
    Implements tri-layer memory caching:
    - HOT: Active context (5 min TTL)
    - WARM: Recent data (1 hour TTL)
    - COLD: Archived (handled by PostgreSQL)
    """
    
    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Establish Redis connection."""
        try:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self._client.ping()
            self._connected = True
            logger.info("✅ Redis connection established")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self._connected = False
            raise
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._connected = False
            logger.info("✅ Redis connection closed")
    
    @property
    def client(self) -> redis.Redis:
        """Get Redis client."""
        if not self._client or not self._connected:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BASIC OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        return await self.client.get(key)
    
    async def set(
        self, 
        key: str, 
        value: str, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value with optional TTL."""
        if ttl:
            return await self.client.setex(key, ttl, value)
        return await self.client.set(key, value)
    
    async def delete(self, key: str) -> int:
        """Delete key."""
        return await self.client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.client.exists(key) > 0
    
    async def ttl(self, key: str) -> int:
        """Get TTL of key."""
        return await self.client.ttl(key)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # JSON OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """Get and parse JSON value."""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set_json(
        self, 
        key: str, 
        value: Dict[str, Any], 
        ttl: Optional[int] = None
    ) -> bool:
        """Serialize and set JSON value."""
        return await self.set(key, json.dumps(value, default=str), ttl)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TRI-LAYER MEMORY (Rule #6)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def set_hot_memory(
        self, 
        thread_id: str, 
        context: Dict[str, Any]
    ) -> bool:
        """
        Store hot memory (immediate context).
        TTL: 5 minutes (configurable)
        """
        key = f"{CachePrefix.MEMORY_HOT}:{thread_id}"
        context["cached_at"] = datetime.utcnow().isoformat()
        return await self.set_json(key, context, settings.CACHE_TTL_HOT_MEMORY)
    
    async def get_hot_memory(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get hot memory for thread."""
        key = f"{CachePrefix.MEMORY_HOT}:{thread_id}"
        return await self.get_json(key)
    
    async def set_warm_memory(
        self, 
        thread_id: str, 
        snapshot: Dict[str, Any]
    ) -> bool:
        """
        Store warm memory (recent snapshot).
        TTL: 1 hour
        """
        key = f"{CachePrefix.MEMORY_WARM}:{thread_id}"
        snapshot["cached_at"] = datetime.utcnow().isoformat()
        return await self.set_json(key, snapshot, settings.CACHE_TTL_LONG)
    
    async def get_warm_memory(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get warm memory for thread."""
        key = f"{CachePrefix.MEMORY_WARM}:{thread_id}"
        return await self.get_json(key)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECKPOINT CACHE (Rule #1)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def cache_pending_checkpoint(
        self, 
        checkpoint_id: str, 
        checkpoint_data: Dict[str, Any]
    ) -> bool:
        """
        Cache pending checkpoint for quick access.
        TTL: Checkpoint timeout (default 1 hour)
        """
        key = f"{CachePrefix.PENDING_CHECKPOINT}:{checkpoint_id}"
        return await self.set_json(
            key, 
            checkpoint_data, 
            settings.CHECKPOINT_TIMEOUT_SECONDS
        )
    
    async def get_pending_checkpoint(
        self, 
        checkpoint_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get pending checkpoint."""
        key = f"{CachePrefix.PENDING_CHECKPOINT}:{checkpoint_id}"
        return await self.get_json(key)
    
    async def remove_pending_checkpoint(self, checkpoint_id: str) -> int:
        """Remove checkpoint after approval/rejection."""
        key = f"{CachePrefix.PENDING_CHECKPOINT}:{checkpoint_id}"
        return await self.delete(key)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ENTITY CACHING
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def cache_thread(
        self, 
        thread_id: str, 
        thread_data: Dict[str, Any]
    ) -> bool:
        """Cache thread data."""
        key = f"{CachePrefix.THREAD}:{thread_id}"
        return await self.set_json(key, thread_data, settings.CACHE_TTL_MEDIUM)
    
    async def get_cached_thread(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get cached thread."""
        key = f"{CachePrefix.THREAD}:{thread_id}"
        return await self.get_json(key)
    
    async def invalidate_thread(self, thread_id: str) -> int:
        """Invalidate thread cache."""
        key = f"{CachePrefix.THREAD}:{thread_id}"
        return await self.delete(key)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NOVA PIPELINE CACHE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def cache_nova_context(
        self, 
        execution_id: str, 
        context: Dict[str, Any]
    ) -> bool:
        """Cache Nova execution context."""
        key = f"{CachePrefix.NOVA_CONTEXT}:{execution_id}"
        return await self.set_json(key, context, settings.CACHE_TTL_SHORT)
    
    async def get_nova_context(
        self, 
        execution_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get Nova execution context."""
        key = f"{CachePrefix.NOVA_CONTEXT}:{execution_id}"
        return await self.get_json(key)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BULK OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def mget(self, keys: List[str]) -> List[Optional[str]]:
        """Get multiple keys."""
        return await self.client.mget(keys)
    
    async def mset(self, mapping: Dict[str, str]) -> bool:
        """Set multiple keys."""
        return await self.client.mset(mapping)
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        keys = []
        async for key in self.client.scan_iter(match=pattern):
            keys.append(key)
        if keys:
            return await self.client.delete(*keys)
        return 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        info = await self.client.info()
        return {
            "connected": self._connected,
            "used_memory": info.get("used_memory_human"),
            "connected_clients": info.get("connected_clients"),
            "total_keys": await self.client.dbsize(),
            "uptime_days": info.get("uptime_in_days")
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

cache = RedisCache()


async def get_cache() -> RedisCache:
    """Dependency injection for cache."""
    return cache
