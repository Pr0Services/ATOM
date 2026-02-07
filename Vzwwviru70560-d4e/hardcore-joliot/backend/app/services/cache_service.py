"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V79 — Caching Layer
═══════════════════════════════════════════════════════════════════════════════

Redis-based caching for performance optimization.

Features:
- Sphere-aware caching (respects R&D Rule #3)
- Identity-scoped cache keys (R&D Rule #3)
- Checkpoint cache invalidation
- TTL management by data type

R&D Rules Compliance:
- Rule #3: Cache keys include identity_id (no cross-identity leaks)
- Rule #6: Cache operations logged
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, List, Union
from uuid import UUID
from enum import Enum
import logging

logger = logging.getLogger("chenu.cache")


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class CacheTTL(Enum):
    """Cache TTL by data type."""
    
    # Short-lived (frequently changing)
    FEED = 60  # 1 minute
    NOTIFICATIONS = 30  # 30 seconds
    ACTIVITY = 60  # 1 minute
    
    # Medium-lived
    THREAD_LIST = 300  # 5 minutes
    SPHERE_DATA = 300  # 5 minutes
    AGENT_STATUS = 120  # 2 minutes
    
    # Long-lived (rarely changing)
    USER_PROFILE = 3600  # 1 hour
    SPHERE_CONFIG = 3600  # 1 hour
    RD_RULES = 86400  # 24 hours
    
    # Static (changes require explicit invalidation)
    REFERENCE_DATA = 86400  # 24 hours
    LITERATURE_SEARCH = 1800  # 30 minutes


class CachePrefix(Enum):
    """Cache key prefixes by sphere."""
    
    PERSONAL = "personal"
    BUSINESS = "business"
    CREATIVE = "creative"
    ENTERTAINMENT = "entertainment"
    COMMUNITY = "community"
    SOCIAL = "social"
    SCHOLAR = "scholar"
    GOVERNMENT = "government"
    MY_TEAM = "my_team"
    SYSTEM = "system"


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE KEY BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

class CacheKeyBuilder:
    """
    Build cache keys that respect identity boundaries.
    
    Format: chenu:{version}:{sphere}:{identity_id}:{resource_type}:{resource_id}
    
    This ensures:
    - No cross-identity cache leaks (R&D Rule #3)
    - Sphere isolation
    - Easy invalidation patterns
    """
    
    VERSION = "v79"
    
    @classmethod
    def build(
        cls,
        sphere: CachePrefix,
        identity_id: UUID,
        resource_type: str,
        resource_id: Optional[Union[UUID, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a cache key.
        
        Args:
            sphere: Sphere prefix
            identity_id: User/identity ID (REQUIRED for isolation)
            resource_type: Type of resource (e.g., "threads", "feed")
            resource_id: Optional specific resource ID
            params: Optional query params to include in key
            
        Returns:
            Cache key string
        """
        parts = [
            "chenu",
            cls.VERSION,
            sphere.value,
            str(identity_id),
            resource_type
        ]
        
        if resource_id:
            parts.append(str(resource_id))
        
        if params:
            # Hash params for consistent key
            param_hash = hashlib.md5(
                json.dumps(params, sort_keys=True).encode()
            ).hexdigest()[:8]
            parts.append(param_hash)
        
        return ":".join(parts)
    
    @classmethod
    def build_system(cls, resource_type: str, resource_id: Optional[str] = None) -> str:
        """Build system-level cache key (not identity-specific)."""
        parts = ["chenu", cls.VERSION, "system", resource_type]
        if resource_id:
            parts.append(resource_id)
        return ":".join(parts)
    
    @classmethod
    def invalidation_pattern(cls, sphere: CachePrefix, identity_id: UUID) -> str:
        """Get pattern for invalidating all cache for a sphere/identity."""
        return f"chenu:{cls.VERSION}:{sphere.value}:{identity_id}:*"


# ═══════════════════════════════════════════════════════════════════════════════
# REDIS CLIENT (Real + Mock fallback)
# ═══════════════════════════════════════════════════════════════════════════════

import os

class MockRedisClient:
    """Mock Redis client for testing when Redis is not available."""

    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._ttls: Dict[str, datetime] = {}
        logger.warning("Using MockRedisClient - for production, set REDIS_URL")

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if key in self._store:
            if key in self._ttls and datetime.utcnow() > self._ttls[key]:
                del self._store[key]
                del self._ttls[key]
                return None
            return self._store[key]
        return None

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        self._store[key] = value
        if ex:
            self._ttls[key] = datetime.utcnow() + timedelta(seconds=ex)
        return True

    async def delete(self, *keys: str) -> int:
        """Delete keys from cache."""
        count = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                if key in self._ttls:
                    del self._ttls[key]
                count += 1
        return count

    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern (simple glob support)."""
        import fnmatch
        return [k for k in self._store.keys() if fnmatch.fnmatch(k, pattern)]

    async def flushdb(self) -> bool:
        """Clear all cache."""
        self._store.clear()
        self._ttls.clear()
        return True


class RealRedisClient:
    """Real Redis client wrapper for async operations."""

    def __init__(self, redis_url: str):
        self._url = redis_url
        self._client = None
        logger.info(f"RealRedisClient initialized with URL: {redis_url[:20]}...")

    async def _get_client(self):
        """Lazy load Redis client."""
        if self._client is None:
            try:
                import redis.asyncio as aioredis
                self._client = aioredis.from_url(
                    self._url,
                    encoding="utf-8",
                    decode_responses=True,
                )
                # Test connection
                await self._client.ping()
                logger.info("✓ Redis connected successfully")
            except ImportError:
                logger.error("redis package not installed. Run: pip install redis")
                raise
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")
                raise
        return self._client

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        client = await self._get_client()
        return await client.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        client = await self._get_client()
        await client.set(key, value, ex=ex)
        return True

    async def delete(self, *keys: str) -> int:
        """Delete keys from cache."""
        if not keys:
            return 0
        client = await self._get_client()
        return await client.delete(*keys)

    async def keys(self, pattern: str) -> List[str]:
        """Get keys matching pattern."""
        client = await self._get_client()
        return await client.keys(pattern)

    async def flushdb(self) -> bool:
        """Clear all cache."""
        client = await self._get_client()
        await client.flushdb()
        return True

    async def close(self):
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None


def create_redis_client():
    """
    Create the appropriate Redis client based on environment.

    Uses REDIS_URL environment variable if set, otherwise falls back to mock.
    """
    redis_url = os.getenv("REDIS_URL")

    if redis_url:
        try:
            return RealRedisClient(redis_url)
        except Exception as e:
            logger.warning(f"Failed to create Redis client: {e}, falling back to mock")
            return MockRedisClient()
    else:
        logger.info("REDIS_URL not set, using MockRedisClient")
        return MockRedisClient()


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class CacheService:
    """
    Cache service with R&D rules compliance.
    
    Features:
    - Identity-scoped caching (Rule #3)
    - Automatic serialization
    - TTL management
    - Pattern-based invalidation
    - Cache statistics
    """
    
    def __init__(self, redis_client=None):
        self.redis = redis_client or create_redis_client()
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "invalidations": 0
        }
    
    async def get(
        self,
        sphere: CachePrefix,
        identity_id: UUID,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        params: Optional[Dict] = None
    ) -> Optional[Any]:
        """
        Get cached data.
        
        Args:
            sphere: Sphere for the data
            identity_id: Owner identity (REQUIRED)
            resource_type: Type of resource
            resource_id: Optional specific resource
            params: Optional query params
            
        Returns:
            Cached data or None
        """
        key = CacheKeyBuilder.build(
            sphere=sphere,
            identity_id=identity_id,
            resource_type=resource_type,
            resource_id=resource_id,
            params=params
        )
        
        cached = await self.redis.get(key)
        
        if cached:
            self.stats["hits"] += 1
            logger.debug(f"Cache HIT: {key}")
            return json.loads(cached)
        
        self.stats["misses"] += 1
        logger.debug(f"Cache MISS: {key}")
        return None
    
    async def set(
        self,
        sphere: CachePrefix,
        identity_id: UUID,
        resource_type: str,
        data: Any,
        resource_id: Optional[UUID] = None,
        params: Optional[Dict] = None,
        ttl: Optional[CacheTTL] = None
    ) -> bool:
        """
        Set cached data.
        
        Args:
            sphere: Sphere for the data
            identity_id: Owner identity (REQUIRED)
            resource_type: Type of resource
            data: Data to cache
            resource_id: Optional specific resource
            params: Optional query params
            ttl: TTL enum value
            
        Returns:
            Success boolean
        """
        key = CacheKeyBuilder.build(
            sphere=sphere,
            identity_id=identity_id,
            resource_type=resource_type,
            resource_id=resource_id,
            params=params
        )
        
        ttl_seconds = ttl.value if ttl else CacheTTL.SPHERE_DATA.value
        
        # Serialize with metadata
        cached_data = {
            "data": data,
            "cached_at": datetime.utcnow().isoformat(),
            "identity_id": str(identity_id),
            "sphere": sphere.value
        }
        
        result = await self.redis.set(
            key,
            json.dumps(cached_data, default=str),
            ex=ttl_seconds
        )
        
        if result:
            self.stats["sets"] += 1
            logger.debug(f"Cache SET: {key} (TTL: {ttl_seconds}s)")
        
        return result
    
    async def invalidate(
        self,
        sphere: CachePrefix,
        identity_id: UUID,
        resource_type: Optional[str] = None
    ) -> int:
        """
        Invalidate cache entries.
        
        Args:
            sphere: Sphere to invalidate
            identity_id: Identity to invalidate
            resource_type: Optional specific resource type
            
        Returns:
            Number of keys invalidated
        """
        if resource_type:
            pattern = f"chenu:{CacheKeyBuilder.VERSION}:{sphere.value}:{identity_id}:{resource_type}:*"
        else:
            pattern = CacheKeyBuilder.invalidation_pattern(sphere, identity_id)
        
        keys = await self.redis.keys(pattern)
        
        if keys:
            count = await self.redis.delete(*keys)
            self.stats["invalidations"] += count
            logger.info(f"Cache INVALIDATE: {pattern} ({count} keys)")
            return count
        
        return 0
    
    async def invalidate_on_checkpoint(
        self,
        checkpoint_id: UUID,
        sphere: CachePrefix,
        identity_id: UUID,
        resource_type: str
    ) -> int:
        """
        Invalidate cache when checkpoint is approved.
        
        Called after checkpoint approval to ensure fresh data.
        """
        logger.info(f"Checkpoint {checkpoint_id} approved - invalidating cache")
        return await self.invalidate(sphere, identity_id, resource_type)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════

def cached(
    sphere: CachePrefix,
    resource_type: str,
    ttl: CacheTTL = CacheTTL.SPHERE_DATA
):
    """
    Decorator for caching endpoint responses.
    
    Usage:
        @cached(CachePrefix.SCHOLAR, "references", CacheTTL.REFERENCE_DATA)
        async def get_references(identity_id: UUID):
            ...
    """
    def decorator(func):
        async def wrapper(*args, identity_id: UUID, **kwargs):
            cache = CacheService()  # Would be injected in production
            
            # Try cache first
            cached_data = await cache.get(
                sphere=sphere,
                identity_id=identity_id,
                resource_type=resource_type,
                params=kwargs if kwargs else None
            )
            
            if cached_data:
                return cached_data["data"]
            
            # Execute function
            result = await func(*args, identity_id=identity_id, **kwargs)
            
            # Cache result
            await cache.set(
                sphere=sphere,
                identity_id=identity_id,
                resource_type=resource_type,
                data=result,
                params=kwargs if kwargs else None,
                ttl=ttl
            )
            
            return result
        
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# CACHE WARMING
# ═══════════════════════════════════════════════════════════════════════════════

class CacheWarmer:
    """Pre-warm cache for common queries."""
    
    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
    
    async def warm_user_session(self, identity_id: UUID) -> Dict[str, int]:
        """
        Warm cache for a user's session.
        
        Pre-loads:
        - User profile
        - Active threads (all spheres)
        - Recent notifications
        - Agent status
        """
        warmed = {}
        
        # System data
        await self.cache.set(
            sphere=CachePrefix.SYSTEM,
            identity_id=identity_id,
            resource_type="rd_rules",
            data=self._get_rd_rules(),
            ttl=CacheTTL.RD_RULES
        )
        warmed["system"] = 1
        
        # Per-sphere warming would happen here
        for sphere in CachePrefix:
            if sphere != CachePrefix.SYSTEM:
                # Would load sphere-specific data
                warmed[sphere.value] = 0
        
        logger.info(f"Cache warmed for identity {identity_id}: {warmed}")
        return warmed
    
    def _get_rd_rules(self) -> List[Dict]:
        """Get R&D rules for caching."""
        return [
            {"number": 1, "name": "Human Sovereignty", "status": "enforced"},
            {"number": 2, "name": "Autonomy Isolation", "status": "enforced"},
            {"number": 3, "name": "Sphere Integrity", "status": "enforced"},
            {"number": 4, "name": "No AI Orchestration", "status": "enforced"},
            {"number": 5, "name": "No Ranking", "status": "enforced"},
            {"number": 6, "name": "Traceability", "status": "enforced"},
            {"number": 7, "name": "R&D Continuity", "status": "enforced"}
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "CacheService",
    "CacheKeyBuilder",
    "CachePrefix",
    "CacheTTL",
    "CacheWarmer",
    "cached",
    "create_redis_client",
    "RealRedisClient",
    "MockRedisClient",
]
