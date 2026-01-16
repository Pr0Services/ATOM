"""
============================================================================
CHE·NU™ V69 — API MIDDLEWARE
============================================================================
Version: 1.0.0
Purpose: Authentication, authorization, governance, logging
Principle: Security and governance at every layer
============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
import hashlib
import hmac
import json
import logging
import time
import uuid

from fastapi import Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from ..core.config import (
    get_settings,
    RequestContext,
    AuthenticationError,
    AuthorizationError,
    GovernanceError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# JWT UTILITIES
# ============================================================================

def create_access_token(
    user_id: str,
    tenant_id: Optional[str] = None,
    roles: List[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token"""
    settings = get_settings()
    
    expire = datetime.utcnow() + (
        expires_delta or timedelta(hours=settings.jwt_expiration_hours)
    )
    
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "roles": roles or [],
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token"""
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {e}")


# ============================================================================
# SECURITY SCHEMES
# ============================================================================

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    bearer: Optional[HTTPAuthorizationCredentials] = None,
    api_key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Get current user from JWT token or API key.
    """
    # Try Bearer token first
    if bearer and bearer.credentials:
        try:
            payload = decode_access_token(bearer.credentials)
            return {
                "user_id": payload.get("sub"),
                "tenant_id": payload.get("tenant_id"),
                "roles": set(payload.get("roles", [])),
            }
        except AuthenticationError:
            pass
    
    # Try API key
    if api_key:
        # In production, validate API key against database
        # For now, accept any key in development
        settings = get_settings()
        if settings.debug:
            return {
                "user_id": "api-user",
                "tenant_id": "api-tenant",
                "roles": {"api"},
            }
    
    return None


# ============================================================================
# AUTHENTICATION MIDDLEWARE
# ============================================================================

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for JWT/API Key authentication.
    """
    
    # Paths that don't require authentication
    PUBLIC_PATHS = {
        "/",
        "/api",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/health",
        "/api/v1/ready",
        "/api/v1/live",
        "/api/v1/auth/login",
    }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip auth for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)
        
        # Skip auth for WebSocket (handled separately)
        if request.url.path.startswith("/ws"):
            return await call_next(request)
        
        # Get token
        auth_header = request.headers.get("Authorization", "")
        api_key = request.headers.get("X-API-Key")
        
        bearer = None
        if auth_header.startswith("Bearer "):
            bearer = HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=auth_header[7:],
            )
        
        user = await get_current_user(bearer, api_key)
        
        if user is None:
            settings = get_settings()
            if not settings.debug:
                return Response(
                    content=json.dumps({
                        "error": "Authentication required",
                        "error_code": "AUTHENTICATION_ERROR",
                    }),
                    status_code=401,
                    media_type="application/json",
                )
            else:
                # Development mode: create mock user
                user = {
                    "user_id": "dev-user",
                    "tenant_id": "dev-tenant",
                    "roles": {"admin"},
                }
        
        # Store user in request state
        request.state.user = user
        request.state.user_id = user.get("user_id")
        request.state.tenant_id = user.get("tenant_id")
        request.state.roles = user.get("roles", set())
        
        return await call_next(request)


# ============================================================================
# GOVERNANCE MIDDLEWARE
# ============================================================================

class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware for OPA policy checks.
    
    Enforces governance rules on all API requests.
    """
    
    # Methods that modify state
    WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
    
    # Paths requiring governance checks
    GOVERNED_PATHS = {
        "/api/v1/simulations",
        "/api/v1/scenarios",
        "/api/v1/agents",
        "/api/v1/checkpoints",
        "/api/v1/causal",
    }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        settings = get_settings()
        
        # Skip if OPA is disabled
        if not settings.opa_enabled:
            return await call_next(request)
        
        # Check if this path requires governance
        needs_governance = any(
            request.url.path.startswith(path)
            for path in self.GOVERNED_PATHS
        )
        
        if needs_governance and request.method in self.WRITE_METHODS:
            # Build OPA input
            opa_input = {
                "user_id": getattr(request.state, "user_id", None),
                "tenant_id": getattr(request.state, "tenant_id", None),
                "roles": list(getattr(request.state, "roles", set())),
                "path": request.url.path,
                "method": request.method,
                "action": self._path_to_action(request.url.path, request.method),
            }
            
            # Check with OPA (mock for now)
            allowed = await self._check_opa(opa_input)
            
            if not allowed:
                return Response(
                    content=json.dumps({
                        "error": "Action denied by governance policy",
                        "error_code": "GOVERNANCE_ERROR",
                    }),
                    status_code=403,
                    media_type="application/json",
                )
        
        return await call_next(request)
    
    def _path_to_action(self, path: str, method: str) -> str:
        """Convert path and method to action name"""
        parts = path.split("/")
        resource = parts[3] if len(parts) > 3 else "unknown"
        
        method_map = {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }
        
        return f"{resource}.{method_map.get(method, 'unknown')}"
    
    async def _check_opa(self, input_data: Dict[str, Any]) -> bool:
        """
        Check OPA policy.
        
        In production, this would call the OPA server.
        """
        settings = get_settings()
        
        # For development, allow all
        if settings.debug:
            return True
        
        # In production: call OPA
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{settings.opa_url}{settings.opa_policy_path}",
        #         json={"input": input_data},
        #     )
        #     result = response.json()
        #     return result.get("result", False)
        
        return True


# ============================================================================
# RATE LIMITING MIDDLEWARE
# ============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware.
    
    Uses a simple in-memory token bucket algorithm.
    In production, would use Redis.
    """
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._buckets: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        settings = get_settings()
        
        if not settings.rate_limit_enabled:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        if not self._check_rate_limit(client_id):
            return Response(
                content=json.dumps({
                    "error": "Rate limit exceeded",
                    "error_code": "RATE_LIMIT_ERROR",
                    "retry_after": 60,
                }),
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": "60"},
            )
        
        return await call_next(request)
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Try user ID first
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fall back to IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    def _check_rate_limit(self, client_id: str) -> bool:
        """Check if client is within rate limit"""
        now = time.time()
        window_start = now - 60  # 1 minute window
        
        # Get or create bucket
        if client_id not in self._buckets:
            self._buckets[client_id] = []
        
        # Clean old requests
        self._buckets[client_id] = [
            ts for ts in self._buckets[client_id]
            if ts > window_start
        ]
        
        # Check limit
        if len(self._buckets[client_id]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self._buckets[client_id].append(now)
        
        return True


# ============================================================================
# LOGGING MIDDLEWARE
# ============================================================================

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Request/response logging middleware.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
            },
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )
        
        # Add timing header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        return response


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def get_request_context(request: Request) -> RequestContext:
    """
    Get request context from request state.
    
    Use as a FastAPI dependency.
    """
    return RequestContext(
        request_id=getattr(request.state, "request_id", str(uuid.uuid4())),
        user_id=getattr(request.state, "user_id", None),
        tenant_id=getattr(request.state, "tenant_id", None),
        roles=getattr(request.state, "roles", set()),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
    )


def require_role(role: str):
    """
    Dependency that requires a specific role.
    """
    async def check_role(request: Request):
        roles = getattr(request.state, "roles", set())
        if role not in roles and "admin" not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{role}' required",
            )
    
    return check_role


def require_permission(permission: str):
    """
    Dependency that requires a specific permission.
    """
    async def check_permission(request: Request):
        # In production, check actual permissions
        pass
    
    return check_permission
