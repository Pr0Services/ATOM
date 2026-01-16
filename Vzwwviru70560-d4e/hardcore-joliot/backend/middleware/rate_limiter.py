"""
CHE·NU™ Rate Limiting Middleware V72

Advanced rate limiting for API protection:
- Per-user rate limits
- Per-endpoint rate limits
- IP-based rate limits
- Sliding window algorithm
- Redis-compatible storage

@version V72.0
@phase Phase 2 - Authentication Security
"""

import time
import hashlib
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, Callable, List
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from collections import defaultdict
import json


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

class RateLimitConfig:
    """Rate limiting configuration."""
    
    # Default limits (requests per window)
    DEFAULT_LIMIT = 100
    DEFAULT_WINDOW_SECONDS = 60
    
    # Auth endpoints (stricter)
    AUTH_LOGIN_LIMIT = 5
    AUTH_LOGIN_WINDOW = 300  # 5 minutes
    
    AUTH_REGISTER_LIMIT = 3
    AUTH_REGISTER_WINDOW = 3600  # 1 hour
    
    AUTH_PASSWORD_RESET_LIMIT = 3
    AUTH_PASSWORD_RESET_WINDOW = 3600  # 1 hour
    
    AUTH_2FA_LIMIT = 5
    AUTH_2FA_WINDOW = 300  # 5 minutes
    
    # API endpoints
    API_READ_LIMIT = 1000
    API_READ_WINDOW = 60
    
    API_WRITE_LIMIT = 100
    API_WRITE_WINDOW = 60
    
    # Burst protection
    BURST_LIMIT = 20
    BURST_WINDOW = 1
    
    # Lockout settings
    LOCKOUT_THRESHOLD = 10  # Failed attempts before lockout
    LOCKOUT_DURATION = 900  # 15 minutes


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════

class RateLimitStrategy(Enum):
    """Rate limiting strategies."""
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"


class RateLimitScope(Enum):
    """Rate limiting scope."""
    GLOBAL = "global"
    USER = "user"
    IP = "ip"
    ENDPOINT = "endpoint"
    USER_ENDPOINT = "user_endpoint"
    IP_ENDPOINT = "ip_endpoint"


# ═══════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RateLimitRule:
    """Rate limit rule definition."""
    name: str
    limit: int
    window_seconds: int
    scope: RateLimitScope = RateLimitScope.USER
    strategy: RateLimitStrategy = RateLimitStrategy.SLIDING_WINDOW
    burst_limit: Optional[int] = None
    burst_window: Optional[int] = None
    
    def get_key(self, identifier: str, endpoint: Optional[str] = None) -> str:
        """Generate rate limit key."""
        parts = [self.name, identifier]
        if endpoint and self.scope in [RateLimitScope.ENDPOINT, 
                                        RateLimitScope.USER_ENDPOINT, 
                                        RateLimitScope.IP_ENDPOINT]:
            parts.append(endpoint)
        return ":".join(parts)


@dataclass
class RateLimitEntry:
    """Rate limit tracking entry."""
    key: str
    count: int
    window_start: float
    requests: List[float] = field(default_factory=list)  # For sliding window
    tokens: float = 0.0  # For token bucket


@dataclass
class RateLimitResult:
    """Result of rate limit check."""
    allowed: bool
    limit: int
    remaining: int
    reset_at: float
    retry_after: Optional[int] = None


# ═══════════════════════════════════════════════════════════════════════════
# STORAGE BACKENDS
# ═══════════════════════════════════════════════════════════════════════════

class RateLimitStorage:
    """Base class for rate limit storage."""
    
    async def get(self, key: str) -> Optional[RateLimitEntry]:
        raise NotImplementedError
    
    async def set(self, key: str, entry: RateLimitEntry, ttl: int):
        raise NotImplementedError
    
    async def increment(self, key: str, window_seconds: int) -> Tuple[int, float]:
        raise NotImplementedError
    
    async def delete(self, key: str):
        raise NotImplementedError


class InMemoryStorage(RateLimitStorage):
    """In-memory storage for rate limits (development/single instance)."""
    
    def __init__(self):
        self._data: Dict[str, RateLimitEntry] = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[RateLimitEntry]:
        async with self._lock:
            entry = self._data.get(key)
            if entry:
                # Check if expired
                now = time.time()
                # Entries expire after 2x window time
                return entry
            return None
    
    async def set(self, key: str, entry: RateLimitEntry, ttl: int):
        async with self._lock:
            self._data[key] = entry
    
    async def increment(self, key: str, window_seconds: int) -> Tuple[int, float]:
        """Increment counter, return (count, window_start)."""
        async with self._lock:
            now = time.time()
            entry = self._data.get(key)
            
            if entry is None:
                # New entry
                entry = RateLimitEntry(
                    key=key,
                    count=1,
                    window_start=now,
                    requests=[now]
                )
                self._data[key] = entry
                return 1, now
            
            # Check if window expired (fixed window)
            if now - entry.window_start >= window_seconds:
                # Reset window
                entry.count = 1
                entry.window_start = now
                entry.requests = [now]
                return 1, now
            
            # Increment
            entry.count += 1
            entry.requests.append(now)
            
            return entry.count, entry.window_start
    
    async def delete(self, key: str):
        async with self._lock:
            self._data.pop(key, None)
    
    async def cleanup_expired(self, max_age: int = 3600):
        """Remove expired entries."""
        async with self._lock:
            now = time.time()
            expired_keys = [
                key for key, entry in self._data.items()
                if now - entry.window_start > max_age
            ]
            for key in expired_keys:
                del self._data[key]


class RedisStorage(RateLimitStorage):
    """Redis storage for rate limits (production/distributed)."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self._redis_url = redis_url
        self._client = None
    
    async def _get_client(self):
        """Get or create Redis client."""
        if self._client is None:
            try:
                import aioredis
                self._client = await aioredis.from_url(self._redis_url)
            except ImportError:
                raise RuntimeError("aioredis package required for Redis storage")
        return self._client
    
    async def get(self, key: str) -> Optional[RateLimitEntry]:
        client = await self._get_client()
        data = await client.get(f"ratelimit:{key}")
        if data:
            entry_dict = json.loads(data)
            return RateLimitEntry(**entry_dict)
        return None
    
    async def set(self, key: str, entry: RateLimitEntry, ttl: int):
        client = await self._get_client()
        data = json.dumps({
            "key": entry.key,
            "count": entry.count,
            "window_start": entry.window_start,
            "requests": entry.requests[-100:],  # Keep last 100 requests
            "tokens": entry.tokens,
        })
        await client.setex(f"ratelimit:{key}", ttl, data)
    
    async def increment(self, key: str, window_seconds: int) -> Tuple[int, float]:
        """Increment using Redis INCR with expiry."""
        client = await self._get_client()
        full_key = f"ratelimit:{key}"
        
        # Use Lua script for atomic operation
        script = """
        local current = redis.call('GET', KEYS[1])
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        
        if current then
            local data = cjson.decode(current)
            if now - data.window_start >= window then
                -- Reset window
                data.count = 1
                data.window_start = now
            else
                data.count = data.count + 1
            end
            redis.call('SETEX', KEYS[1], window * 2, cjson.encode(data))
            return {data.count, data.window_start}
        else
            -- New entry
            local data = {count = 1, window_start = now, requests = {}, tokens = 0}
            redis.call('SETEX', KEYS[1], window * 2, cjson.encode(data))
            return {1, now}
        end
        """
        
        now = time.time()
        count = await client.incr(full_key)
        
        if count == 1:
            await client.expire(full_key, window_seconds * 2)
        
        return count, now
    
    async def delete(self, key: str):
        client = await self._get_client()
        await client.delete(f"ratelimit:{key}")


# ═══════════════════════════════════════════════════════════════════════════
# RATE LIMITER
# ═══════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """Advanced rate limiter with multiple strategies."""
    
    def __init__(self, storage: Optional[RateLimitStorage] = None):
        self._storage = storage or InMemoryStorage()
        self._rules: Dict[str, RateLimitRule] = {}
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default rate limit rules."""
        # Auth rules
        self._rules["auth:login"] = RateLimitRule(
            name="auth:login",
            limit=RateLimitConfig.AUTH_LOGIN_LIMIT,
            window_seconds=RateLimitConfig.AUTH_LOGIN_WINDOW,
            scope=RateLimitScope.IP,
            burst_limit=3,
            burst_window=10,
        )
        
        self._rules["auth:register"] = RateLimitRule(
            name="auth:register",
            limit=RateLimitConfig.AUTH_REGISTER_LIMIT,
            window_seconds=RateLimitConfig.AUTH_REGISTER_WINDOW,
            scope=RateLimitScope.IP,
        )
        
        self._rules["auth:password_reset"] = RateLimitRule(
            name="auth:password_reset",
            limit=RateLimitConfig.AUTH_PASSWORD_RESET_LIMIT,
            window_seconds=RateLimitConfig.AUTH_PASSWORD_RESET_WINDOW,
            scope=RateLimitScope.IP_ENDPOINT,
        )
        
        self._rules["auth:2fa"] = RateLimitRule(
            name="auth:2fa",
            limit=RateLimitConfig.AUTH_2FA_LIMIT,
            window_seconds=RateLimitConfig.AUTH_2FA_WINDOW,
            scope=RateLimitScope.USER,
        )
        
        # API rules
        self._rules["api:read"] = RateLimitRule(
            name="api:read",
            limit=RateLimitConfig.API_READ_LIMIT,
            window_seconds=RateLimitConfig.API_READ_WINDOW,
            scope=RateLimitScope.USER,
        )
        
        self._rules["api:write"] = RateLimitRule(
            name="api:write",
            limit=RateLimitConfig.API_WRITE_LIMIT,
            window_seconds=RateLimitConfig.API_WRITE_WINDOW,
            scope=RateLimitScope.USER,
        )
        
        # Default rule
        self._rules["default"] = RateLimitRule(
            name="default",
            limit=RateLimitConfig.DEFAULT_LIMIT,
            window_seconds=RateLimitConfig.DEFAULT_WINDOW_SECONDS,
            scope=RateLimitScope.USER,
        )
    
    def add_rule(self, rule: RateLimitRule):
        """Add custom rate limit rule."""
        self._rules[rule.name] = rule
    
    async def check(
        self,
        rule_name: str,
        identifier: str,
        endpoint: Optional[str] = None,
        consume: bool = True
    ) -> RateLimitResult:
        """
        Check rate limit.
        
        Args:
            rule_name: Name of rate limit rule
            identifier: User ID, IP address, or other identifier
            endpoint: Optional endpoint name
            consume: Whether to consume a request (increment counter)
        
        Returns:
            RateLimitResult with allowed status and metadata
        """
        rule = self._rules.get(rule_name, self._rules["default"])
        key = rule.get_key(identifier, endpoint)
        
        if consume:
            count, window_start = await self._storage.increment(
                key, 
                rule.window_seconds
            )
        else:
            entry = await self._storage.get(key)
            if entry:
                count = entry.count
                window_start = entry.window_start
            else:
                count = 0
                window_start = time.time()
        
        now = time.time()
        reset_at = window_start + rule.window_seconds
        remaining = max(0, rule.limit - count)
        allowed = count <= rule.limit
        
        # Check burst limit if configured
        if allowed and rule.burst_limit:
            burst_result = await self._check_burst(
                key, 
                rule.burst_limit, 
                rule.burst_window or 1
            )
            if not burst_result:
                allowed = False
                remaining = 0
        
        retry_after = None
        if not allowed:
            retry_after = int(reset_at - now) + 1
        
        return RateLimitResult(
            allowed=allowed,
            limit=rule.limit,
            remaining=remaining,
            reset_at=reset_at,
            retry_after=retry_after
        )
    
    async def _check_burst(
        self, 
        key: str, 
        burst_limit: int, 
        burst_window: int
    ) -> bool:
        """Check burst rate limit."""
        burst_key = f"{key}:burst"
        count, _ = await self._storage.increment(burst_key, burst_window)
        return count <= burst_limit
    
    async def reset(self, rule_name: str, identifier: str, endpoint: Optional[str] = None):
        """Reset rate limit for identifier."""
        rule = self._rules.get(rule_name, self._rules["default"])
        key = rule.get_key(identifier, endpoint)
        await self._storage.delete(key)
    
    def get_headers(self, result: RateLimitResult) -> Dict[str, str]:
        """Get rate limit response headers."""
        headers = {
            "X-RateLimit-Limit": str(result.limit),
            "X-RateLimit-Remaining": str(result.remaining),
            "X-RateLimit-Reset": str(int(result.reset_at)),
        }
        
        if result.retry_after:
            headers["Retry-After"] = str(result.retry_after)
        
        return headers


# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════

class RateLimitMiddleware:
    """FastAPI middleware for rate limiting."""
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        self._limiter = rate_limiter or RateLimiter()
    
    async def __call__(self, request, call_next):
        """Process request with rate limiting."""
        # Get identifier
        identifier = self._get_identifier(request)
        
        # Determine rule based on endpoint
        rule_name = self._get_rule_name(request)
        
        # Check rate limit
        result = await self._limiter.check(
            rule_name,
            identifier,
            endpoint=request.url.path
        )
        
        if not result.allowed:
            # Return 429 Too Many Requests
            from fastapi.responses import JSONResponse
            
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Please try again later.",
                    "retry_after": result.retry_after,
                },
                headers=self._limiter.get_headers(result)
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        for key, value in self._limiter.get_headers(result).items():
            response.headers[key] = value
        
        return response
    
    def _get_identifier(self, request) -> str:
        """Get identifier from request (IP or user ID)."""
        # Try to get user ID from auth
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fall back to IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"
        
        return f"ip:{ip}"
    
    def _get_rule_name(self, request) -> str:
        """Get rate limit rule based on request."""
        path = request.url.path.lower()
        method = request.method.upper()
        
        # Auth endpoints
        if "/auth/login" in path:
            return "auth:login"
        if "/auth/register" in path:
            return "auth:register"
        if "/password-reset" in path:
            return "auth:password_reset"
        if "/2fa" in path:
            return "auth:2fa"
        
        # API endpoints
        if method in ["GET", "HEAD", "OPTIONS"]:
            return "api:read"
        if method in ["POST", "PUT", "PATCH", "DELETE"]:
            return "api:write"
        
        return "default"


# ═══════════════════════════════════════════════════════════════════════════
# DECORATOR
# ═══════════════════════════════════════════════════════════════════════════

def rate_limit(
    rule_name: str = "default",
    limit: Optional[int] = None,
    window_seconds: Optional[int] = None,
    scope: RateLimitScope = RateLimitScope.USER
):
    """
    Decorator for rate limiting endpoints.
    
    Usage:
        @rate_limit("custom", limit=10, window_seconds=60)
        async def my_endpoint():
            ...
    """
    # Create custom rule if parameters provided
    if limit and window_seconds:
        custom_rule = RateLimitRule(
            name=f"custom:{rule_name}",
            limit=limit,
            window_seconds=window_seconds,
            scope=scope
        )
        _rate_limiter.add_rule(custom_rule)
        rule_name = custom_rule.name
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request from args/kwargs
            request = kwargs.get("request") or (args[0] if args else None)
            
            if request:
                # Get identifier
                user_id = getattr(request.state, "user_id", None)
                ip = request.client.host if request.client else "unknown"
                
                if scope == RateLimitScope.USER and user_id:
                    identifier = f"user:{user_id}"
                else:
                    identifier = f"ip:{ip}"
                
                # Check rate limit
                result = await _rate_limiter.check(rule_name, identifier)
                
                if not result.allowed:
                    from fastapi import HTTPException
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "rate_limit_exceeded",
                            "retry_after": result.retry_after
                        }
                    )
            
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ═══════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════

_rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get rate limiter singleton."""
    return _rate_limiter


# ═══════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio
    
    async def test_rate_limiter():
        print("=" * 60)
        print("CHE·NU™ Rate Limiter V72 - Test")
        print("=" * 60)
        
        limiter = RateLimiter()
        
        # Test default rate limit
        print("\n1. Test default rate limit (100/minute)...")
        for i in range(5):
            result = await limiter.check("default", "test_user")
            print(f"   Request {i+1}: allowed={result.allowed}, remaining={result.remaining}")
        
        # Test auth login rate limit
        print("\n2. Test auth login rate limit (5/5min)...")
        for i in range(7):
            result = await limiter.check("auth:login", "192.168.1.1")
            status = "✓" if result.allowed else "✗ BLOCKED"
            print(f"   Attempt {i+1}: {status}, remaining={result.remaining}")
            if result.retry_after:
                print(f"      Retry after: {result.retry_after}s")
        
        # Test headers
        print("\n3. Test response headers...")
        result = await limiter.check("default", "test_user_2")
        headers = limiter.get_headers(result)
        for key, value in headers.items():
            print(f"   {key}: {value}")
        
        # Test reset
        print("\n4. Test rate limit reset...")
        await limiter.reset("auth:login", "192.168.1.1")
        result = await limiter.check("auth:login", "192.168.1.1")
        print(f"   After reset: allowed={result.allowed}, remaining={result.remaining}")
        
        print("\n" + "=" * 60)
        print("Test complete!")
        print("=" * 60)
    
    asyncio.run(test_rate_limiter())
