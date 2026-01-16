"""
CHE·NU™ V72 — Cache Service

Comprehensive caching layer with governance-aware patterns.
Supports identity-scoped caching, invalidation strategies,
and R&D Rule #3 (Sphere Integrity) compliance.

Features:
- Identity-scoped cache keys
- Sphere-aware invalidation
- Thread event invalidation
- Human gate result caching (short TTL)
- Checkpoint caching (pending states)
- Multi-level cache (hot/warm)

R&D Compliance:
- Rule #3: Cache keys scoped by identity
- Rule #6: All cache operations logged
"""

from typing import Optional, Any, Dict, List, Callable, TypeVar, Union
from datetime import datetime, timedelta
from uuid import UUID
import json
import hashlib
import asyncio
import logging
from functools import wraps
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# Type variable for generic caching
T = TypeVar('T')


class CacheTier(str, Enum):
    """Cache tier levels."""
    HOT = "hot"      # Redis - milliseconds access
    WARM = "warm"    # Redis with longer TTL
    COLD = "cold"    # Database (no caching)


class CacheNamespace(str, Enum):
    """Cache key namespaces for different data types."""
    USER = "user"
    THREAD = "thread"
    SPHERE = "sphere"
    AGENT = "agent"
    CHECKPOINT = "checkpoint"
    DECISION = "decision"
    XR = "xr"
    LLM = "llm"
    SESSION = "session"
    STATS = "stats"


@dataclass
class CacheConfig:
    """Configuration for cache behavior."""
    default_ttl: int = 300  # 5 minutes
    hot_ttl: int = 60       # 1 minute
    warm_ttl: int = 900     # 15 minutes
    max_size: int = 10000   # Max entries per namespace
    enable_stats: bool = True
    compress_threshold: int = 1024  # Compress if larger than 1KB


@dataclass
class CacheEntry:
    """Represents a cached value with metadata."""
    value: Any
    created_at: datetime
    expires_at: datetime
    tier: CacheTier
    namespace: CacheNamespace
    identity_id: Optional[str] = None
    hits: int = 0
    size_bytes: int = 0


@dataclass
class CacheStats:
    """Cache statistics for monitoring."""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    total_size_bytes: int = 0
    namespaces: Dict[str, int] = field(default_factory=dict)
    
    @property
    def hit_rate(self) -> float:
        """Calculate hit rate percentage."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0


class CacheKeyBuilder:
    """
    Builds cache keys with identity scoping for R&D Rule #3.
    
    Key format: chenu:{namespace}:{identity_id}:{resource}:{hash}
    """
    
    PREFIX = "chenu"
    
    @classmethod
    def build(
        cls,
        namespace: CacheNamespace,
        resource: str,
        identity_id: Optional[UUID] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build a cache key with optional identity scoping."""
        parts = [cls.PREFIX, namespace.value]
        
        # Add identity scope for R&D Rule #3
        if identity_id:
            parts.append(str(identity_id))
        else:
            parts.append("global")
        
        parts.append(resource)
        
        # Add parameter hash if present
        if params:
            param_hash = cls._hash_params(params)
            parts.append(param_hash)
        
        return ":".join(parts)
    
    @classmethod
    def build_pattern(
        cls,
        namespace: CacheNamespace,
        identity_id: Optional[UUID] = None
    ) -> str:
        """Build a pattern for bulk operations."""
        parts = [cls.PREFIX, namespace.value]
        
        if identity_id:
            parts.append(str(identity_id))
        else:
            parts.append("*")
        
        parts.append("*")
        return ":".join(parts)
    
    @staticmethod
    def _hash_params(params: Dict[str, Any]) -> str:
        """Create a hash of parameters for cache key."""
        # Sort keys for consistent hashing
        sorted_params = json.dumps(params, sort_keys=True, default=str)
        return hashlib.md5(sorted_params.encode()).hexdigest()[:12]


class InMemoryCache:
    """
    In-memory cache for development/testing.
    Also serves as L1 cache in front of Redis.
    """
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = CacheStats()
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        async with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                self._stats.misses += 1
                return None
            
            # Check expiration
            if datetime.utcnow() > entry.expires_at:
                del self._cache[key]
                self._stats.misses += 1
                return None
            
            entry.hits += 1
            self._stats.hits += 1
            return entry.value
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        namespace: CacheNamespace = CacheNamespace.STATS,
        tier: CacheTier = CacheTier.HOT,
        identity_id: Optional[str] = None
    ) -> bool:
        """Set value in cache."""
        async with self._lock:
            ttl = ttl or self.config.default_ttl
            now = datetime.utcnow()
            
            # Estimate size
            size_bytes = len(json.dumps(value, default=str).encode())
            
            entry = CacheEntry(
                value=value,
                created_at=now,
                expires_at=now + timedelta(seconds=ttl),
                tier=tier,
                namespace=namespace,
                identity_id=identity_id,
                size_bytes=size_bytes
            )
            
            self._cache[key] = entry
            self._stats.sets += 1
            self._stats.total_size_bytes += size_bytes
            
            # Update namespace stats
            ns_key = namespace.value
            self._stats.namespaces[ns_key] = self._stats.namespaces.get(ns_key, 0) + 1
            
            # Evict if over max size
            await self._maybe_evict()
            
            return True
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                self._stats.total_size_bytes -= entry.size_bytes
                del self._cache[key]
                self._stats.deletes += 1
                return True
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        async with self._lock:
            # Convert pattern to simple matching
            prefix = pattern.replace("*", "")
            keys_to_delete = [
                k for k in self._cache.keys()
                if k.startswith(prefix)
            ]
            
            for key in keys_to_delete:
                entry = self._cache[key]
                self._stats.total_size_bytes -= entry.size_bytes
                del self._cache[key]
                self._stats.deletes += 1
            
            return len(keys_to_delete)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        value = await self.get(key)
        return value is not None
    
    async def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats
    
    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()
            self._stats = CacheStats()
    
    async def _maybe_evict(self) -> None:
        """Evict entries if over max size."""
        if len(self._cache) > self.config.max_size:
            # LRU eviction - remove oldest entries
            entries = sorted(
                self._cache.items(),
                key=lambda x: x[1].created_at
            )
            
            # Remove 10% of entries
            evict_count = max(1, len(entries) // 10)
            for key, entry in entries[:evict_count]:
                self._stats.total_size_bytes -= entry.size_bytes
                del self._cache[key]
                self._stats.evictions += 1


class CacheService:
    """
    Main cache service with Redis backend and in-memory L1 cache.
    
    Provides governance-aware caching with:
    - Identity-scoped keys (R&D Rule #3)
    - Automatic invalidation on Thread events
    - Checkpoint state caching
    - Statistics and monitoring
    """
    
    def __init__(
        self,
        redis_client: Optional[Any] = None,  # RedisManager instance
        config: Optional[CacheConfig] = None
    ):
        self.redis = redis_client
        self.config = config or CacheConfig()
        self.l1_cache = InMemoryCache(config)
        self._invalidation_handlers: Dict[str, List[Callable]] = {}
    
    # ==================== Core Operations ====================
    
    async def get(
        self,
        namespace: CacheNamespace,
        resource: str,
        identity_id: Optional[UUID] = None,
        params: Optional[Dict[str, Any]] = None,
        use_l1: bool = True
    ) -> Optional[Any]:
        """
        Get value from cache with L1 check first.
        
        Args:
            namespace: Cache namespace
            resource: Resource identifier
            identity_id: Optional identity for scoping
            params: Optional parameters to include in key
            use_l1: Whether to check L1 cache first
        
        Returns:
            Cached value or None
        """
        key = CacheKeyBuilder.build(namespace, resource, identity_id, params)
        
        # Check L1 first
        if use_l1:
            value = await self.l1_cache.get(key)
            if value is not None:
                return value
        
        # Check Redis
        if self.redis:
            try:
                value = await self.redis.get(key)
                if value is not None:
                    # Populate L1 cache
                    if use_l1:
                        await self.l1_cache.set(
                            key, value,
                            ttl=self.config.hot_ttl,
                            namespace=namespace,
                            tier=CacheTier.HOT,
                            identity_id=str(identity_id) if identity_id else None
                        )
                    return value
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        return None
    
    async def set(
        self,
        namespace: CacheNamespace,
        resource: str,
        value: Any,
        identity_id: Optional[UUID] = None,
        params: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        tier: CacheTier = CacheTier.HOT
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            namespace: Cache namespace
            resource: Resource identifier
            value: Value to cache
            identity_id: Optional identity for scoping
            params: Optional parameters to include in key
            ttl: Time to live in seconds
            tier: Cache tier (hot/warm)
        
        Returns:
            Success status
        """
        key = CacheKeyBuilder.build(namespace, resource, identity_id, params)
        
        # Determine TTL based on tier
        if ttl is None:
            ttl = self.config.hot_ttl if tier == CacheTier.HOT else self.config.warm_ttl
        
        # Set in L1
        await self.l1_cache.set(
            key, value,
            ttl=min(ttl, self.config.hot_ttl),  # L1 always uses hot TTL
            namespace=namespace,
            tier=CacheTier.HOT,
            identity_id=str(identity_id) if identity_id else None
        )
        
        # Set in Redis
        if self.redis:
            try:
                await self.redis.set(key, value, ttl)
            except Exception as e:
                logger.error(f"Redis set error: {e}")
                return False
        
        logger.debug(f"Cache set: {key} (ttl={ttl}s)")
        return True
    
    async def delete(
        self,
        namespace: CacheNamespace,
        resource: str,
        identity_id: Optional[UUID] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Delete a specific cache entry."""
        key = CacheKeyBuilder.build(namespace, resource, identity_id, params)
        
        await self.l1_cache.delete(key)
        
        if self.redis:
            try:
                await self.redis.delete(key)
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
                return False
        
        logger.debug(f"Cache delete: {key}")
        return True
    
    async def invalidate_namespace(
        self,
        namespace: CacheNamespace,
        identity_id: Optional[UUID] = None
    ) -> int:
        """Invalidate all entries in a namespace."""
        pattern = CacheKeyBuilder.build_pattern(namespace, identity_id)
        
        count = await self.l1_cache.delete_pattern(pattern)
        
        if self.redis:
            try:
                redis_count = await self.redis.delete_pattern(pattern)
                count += redis_count
            except Exception as e:
                logger.error(f"Redis pattern delete error: {e}")
        
        logger.info(f"Cache invalidated: {pattern} ({count} entries)")
        return count
    
    # ==================== Specialized Caching ====================
    
    async def cache_thread(
        self,
        thread_id: UUID,
        thread_data: Dict[str, Any],
        identity_id: UUID
    ) -> bool:
        """Cache a Thread with identity scoping."""
        return await self.set(
            CacheNamespace.THREAD,
            str(thread_id),
            thread_data,
            identity_id=identity_id,
            tier=CacheTier.WARM
        )
    
    async def get_thread(
        self,
        thread_id: UUID,
        identity_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get cached Thread."""
        return await self.get(
            CacheNamespace.THREAD,
            str(thread_id),
            identity_id=identity_id
        )
    
    async def invalidate_thread(
        self,
        thread_id: UUID,
        identity_id: UUID
    ) -> bool:
        """Invalidate Thread cache on event."""
        return await self.delete(
            CacheNamespace.THREAD,
            str(thread_id),
            identity_id=identity_id
        )
    
    async def cache_sphere(
        self,
        sphere_id: UUID,
        sphere_data: Dict[str, Any],
        identity_id: UUID
    ) -> bool:
        """Cache a Sphere."""
        return await self.set(
            CacheNamespace.SPHERE,
            str(sphere_id),
            sphere_data,
            identity_id=identity_id,
            tier=CacheTier.WARM
        )
    
    async def get_sphere(
        self,
        sphere_id: UUID,
        identity_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get cached Sphere."""
        return await self.get(
            CacheNamespace.SPHERE,
            str(sphere_id),
            identity_id=identity_id
        )
    
    async def cache_checkpoint(
        self,
        checkpoint_id: UUID,
        checkpoint_data: Dict[str, Any],
        identity_id: UUID
    ) -> bool:
        """
        Cache a pending checkpoint.
        Uses short TTL as checkpoints are transient.
        """
        return await self.set(
            CacheNamespace.CHECKPOINT,
            str(checkpoint_id),
            checkpoint_data,
            identity_id=identity_id,
            ttl=300,  # 5 minutes max for pending checkpoints
            tier=CacheTier.HOT
        )
    
    async def get_checkpoint(
        self,
        checkpoint_id: UUID,
        identity_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get cached checkpoint."""
        return await self.get(
            CacheNamespace.CHECKPOINT,
            str(checkpoint_id),
            identity_id=identity_id
        )
    
    async def cache_agent_config(
        self,
        agent_id: str,
        config_data: Dict[str, Any],
        identity_id: UUID
    ) -> bool:
        """Cache user's agent configuration."""
        return await self.set(
            CacheNamespace.AGENT,
            f"config:{agent_id}",
            config_data,
            identity_id=identity_id,
            tier=CacheTier.WARM
        )
    
    async def cache_xr_blueprint(
        self,
        thread_id: UUID,
        blueprint_data: Dict[str, Any],
        identity_id: UUID
    ) -> bool:
        """Cache XR blueprint for a Thread."""
        return await self.set(
            CacheNamespace.XR,
            f"blueprint:{thread_id}",
            blueprint_data,
            identity_id=identity_id,
            tier=CacheTier.WARM,
            ttl=1800  # 30 minutes
        )
    
    async def get_xr_blueprint(
        self,
        thread_id: UUID,
        identity_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get cached XR blueprint."""
        return await self.get(
            CacheNamespace.XR,
            f"blueprint:{thread_id}",
            identity_id=identity_id
        )
    
    async def cache_llm_response(
        self,
        prompt_hash: str,
        response: Dict[str, Any],
        identity_id: UUID,
        ttl: int = 3600
    ) -> bool:
        """Cache LLM response for identical prompts."""
        return await self.set(
            CacheNamespace.LLM,
            f"response:{prompt_hash}",
            response,
            identity_id=identity_id,
            tier=CacheTier.WARM,
            ttl=ttl
        )
    
    async def get_llm_response(
        self,
        prompt_hash: str,
        identity_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get cached LLM response."""
        return await self.get(
            CacheNamespace.LLM,
            f"response:{prompt_hash}",
            identity_id=identity_id
        )
    
    # ==================== Statistics ====================
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get combined cache statistics."""
        l1_stats = await self.l1_cache.get_stats()
        
        stats = {
            "l1_cache": {
                "hits": l1_stats.hits,
                "misses": l1_stats.misses,
                "sets": l1_stats.sets,
                "deletes": l1_stats.deletes,
                "evictions": l1_stats.evictions,
                "hit_rate": l1_stats.hit_rate,
                "total_size_bytes": l1_stats.total_size_bytes,
                "namespaces": l1_stats.namespaces
            },
            "redis": {
                "connected": self.redis is not None
            }
        }
        
        if self.redis:
            try:
                redis_stats = await self.redis.get_stats()
                stats["redis"].update(redis_stats)
            except Exception as e:
                stats["redis"]["error"] = str(e)
        
        return stats
    
    async def clear_all(self) -> None:
        """Clear all caches. Use with caution!"""
        await self.l1_cache.clear()
        
        if self.redis:
            try:
                await self.redis.clear_pattern("chenu:*")
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
        
        logger.warning("All caches cleared")


# ==================== Cache Decorator ====================

def cached(
    namespace: CacheNamespace,
    resource_key: str = "id",
    ttl: Optional[int] = None,
    tier: CacheTier = CacheTier.HOT,
    identity_param: str = "identity_id"
):
    """
    Decorator for caching function results.
    
    Usage:
        @cached(CacheNamespace.THREAD, resource_key="thread_id")
        async def get_thread(thread_id: UUID, identity_id: UUID) -> dict:
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Get cache service from first arg if it has one
            cache_service = None
            if args and hasattr(args[0], 'cache_service'):
                cache_service = args[0].cache_service
            
            if not cache_service:
                return await func(*args, **kwargs)
            
            # Extract identity and resource from kwargs
            identity_id = kwargs.get(identity_param)
            resource = kwargs.get(resource_key) or (
                args[1] if len(args) > 1 else None
            )
            
            if not resource:
                return await func(*args, **kwargs)
            
            # Try to get from cache
            cached_value = await cache_service.get(
                namespace,
                str(resource),
                identity_id=identity_id
            )
            
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                await cache_service.set(
                    namespace,
                    str(resource),
                    result,
                    identity_id=identity_id,
                    ttl=ttl,
                    tier=tier
                )
            
            return result
        
        return wrapper
    return decorator


def invalidate_on_event(
    namespace: CacheNamespace,
    resource_key: str = "id",
    identity_param: str = "identity_id"
):
    """
    Decorator to invalidate cache on write operations.
    
    Usage:
        @invalidate_on_event(CacheNamespace.THREAD, resource_key="thread_id")
        async def update_thread(thread_id: UUID, ...) -> dict:
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Execute function first
            result = await func(*args, **kwargs)
            
            # Get cache service
            cache_service = None
            if args and hasattr(args[0], 'cache_service'):
                cache_service = args[0].cache_service
            
            if cache_service:
                identity_id = kwargs.get(identity_param)
                resource = kwargs.get(resource_key) or (
                    args[1] if len(args) > 1 else None
                )
                
                if resource:
                    await cache_service.delete(
                        namespace,
                        str(resource),
                        identity_id=identity_id
                    )
            
            return result
        
        return wrapper
    return decorator


# ==================== Singleton Instance ====================

_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get or create the singleton cache service."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


def init_cache_service(
    redis_client: Optional[Any] = None,
    config: Optional[CacheConfig] = None
) -> CacheService:
    """Initialize the cache service with configuration."""
    global _cache_service
    _cache_service = CacheService(redis_client, config)
    return _cache_service


# ==================== Exports ====================

__all__ = [
    'CacheTier',
    'CacheNamespace',
    'CacheConfig',
    'CacheEntry',
    'CacheStats',
    'CacheKeyBuilder',
    'InMemoryCache',
    'CacheService',
    'cached',
    'invalidate_on_event',
    'get_cache_service',
    'init_cache_service'
]
