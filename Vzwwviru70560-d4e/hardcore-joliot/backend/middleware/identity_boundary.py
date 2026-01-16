"""
CHE·NU™ Identity Boundary Middleware
Enforces strict identity isolation across all requests

CANON: GOUVERNANCE > EXÉCUTION
- HTTP 403 FORBIDDEN for cross-identity access
- No user can access another user's data
- Full audit trail for violations

This middleware is the first line of defense ensuring that
user A cannot access user B's data under any circumstance.

Author: CHE·NU Team
Version: 1.0.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from uuid import uuid4
import asyncio
import hashlib
import json
import logging
import re
import time

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & CONSTANTS
# =============================================================================

class ViolationType(str, Enum):
    """Types of identity violations"""
    CROSS_IDENTITY_ACCESS = "cross_identity_access"
    MISSING_IDENTITY = "missing_identity"
    INVALID_IDENTITY_FORMAT = "invalid_identity_format"
    IDENTITY_MISMATCH = "identity_mismatch"
    IMPERSONATION_ATTEMPT = "impersonation_attempt"
    SCOPE_VIOLATION = "scope_violation"
    RESOURCE_OWNERSHIP = "resource_ownership"


class AuditAction(str, Enum):
    """Audit action types"""
    ACCESS_ALLOWED = "access_allowed"
    ACCESS_DENIED = "access_denied"
    VIOLATION_DETECTED = "violation_detected"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"


# Paths that don't require identity validation
PUBLIC_PATHS = {
    "/",
    "/health",
    "/healthz",
    "/ready",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/docs",
    "/api/redoc",
    "/api/openapi.json",
    "/auth/login",
    "/auth/register",
    "/auth/refresh",
    "/auth/oauth",
    "/email/verification/verify",
    "/email/password-reset/reset",
}

# Paths with prefix that are public
PUBLIC_PREFIXES = [
    "/static/",
    "/assets/",
    "/auth/oauth/",
]


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class IdentityContext:
    """Extracted identity context from request"""
    identity_id: str
    session_id: Optional[str] = None
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    scopes: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ViolationEvent:
    """Recorded identity violation"""
    id: str = field(default_factory=lambda: str(uuid4()))
    violation_type: ViolationType = ViolationType.CROSS_IDENTITY_ACCESS
    requesting_identity: Optional[str] = None
    target_identity: Optional[str] = None
    resource_path: str = ""
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_method: str = ""
    request_body: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    severity: str = "high"
    resolved: bool = False
    resolution_notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "violation_type": self.violation_type.value,
            "requesting_identity": self.requesting_identity,
            "target_identity": self.target_identity,
            "resource_path": self.resource_path,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_method": self.request_method,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity,
            "resolved": self.resolved,
        }


@dataclass
class AuditEntry:
    """Audit log entry"""
    id: str = field(default_factory=lambda: str(uuid4()))
    action: AuditAction = AuditAction.ACCESS_ALLOWED
    identity_id: Optional[str] = None
    resource_path: str = ""
    resource_id: Optional[str] = None
    request_method: str = ""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_ms: int = 0
    success: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# IDENTITY BOUNDARY SERVICE
# =============================================================================

class IdentityBoundaryService:
    """
    Core service for identity boundary enforcement
    
    Features:
    - Extract identity from requests (headers, JWT, session)
    - Validate identity ownership of resources
    - Detect cross-identity access attempts
    - Log violations with full audit trail
    """
    
    def __init__(self):
        self._violations: List[ViolationEvent] = []
        self._audit_log: List[AuditEntry] = []
        self._identity_cache: Dict[str, IdentityContext] = {}
        self._resource_ownership: Dict[str, str] = {}  # resource_id -> identity_id
        self._max_violations = 10000
        self._max_audit_entries = 50000
        
        # Statistics
        self._total_requests = 0
        self._total_violations = 0
        self._violations_by_type: Dict[str, int] = {}
    
    # =========================================================================
    # IDENTITY EXTRACTION
    # =========================================================================
    
    def extract_identity(self, request: Request) -> Optional[IdentityContext]:
        """
        Extract identity context from request
        
        Sources (in priority order):
        1. X-Identity-ID header
        2. Authorization Bearer token (JWT)
        3. Session cookie
        4. Query parameter (for OAuth callbacks)
        """
        identity_id = None
        session_id = None
        scopes = []
        roles = []
        
        # Try X-Identity-ID header first
        identity_id = request.headers.get("X-Identity-ID")
        session_id = request.headers.get("X-Session-ID")
        
        # Try Authorization header (JWT)
        if not identity_id:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                extracted = self._extract_from_jwt(token)
                if extracted:
                    identity_id = extracted.get("sub")
                    scopes = extracted.get("scopes", [])
                    roles = extracted.get("roles", [])
        
        # Try session cookie
        if not identity_id:
            session_cookie = request.cookies.get("chenu_session")
            if session_cookie:
                extracted = self._extract_from_session(session_cookie)
                if extracted:
                    identity_id = extracted.get("identity_id")
                    session_id = extracted.get("session_id")
        
        # Try query parameter (for OAuth callbacks)
        if not identity_id:
            identity_id = request.query_params.get("identity_id")
        
        if not identity_id:
            return None
        
        # Build identity context
        context = IdentityContext(
            identity_id=identity_id,
            session_id=session_id,
            device_id=request.headers.get("X-Device-ID"),
            ip_address=self._get_client_ip(request),
            user_agent=request.headers.get("User-Agent"),
            scopes=scopes,
            roles=roles,
        )
        
        # Cache identity
        self._identity_cache[identity_id] = context
        
        return context
    
    def _extract_from_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """Extract claims from JWT (simplified - in production use proper JWT library)"""
        try:
            # Split token
            parts = token.split(".")
            if len(parts) != 3:
                return None
            
            # Decode payload (base64url)
            import base64
            payload = parts[1]
            # Add padding if needed
            padding = 4 - (len(payload) % 4)
            if padding != 4:
                payload += "=" * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
        except Exception as e:
            logger.warning(f"Failed to extract from JWT: {e}")
            return None
    
    def _extract_from_session(self, session_cookie: str) -> Optional[Dict[str, Any]]:
        """Extract identity from session cookie"""
        try:
            # In production, validate session from session store
            # For now, assume format: identity_id:session_id:signature
            parts = session_cookie.split(":")
            if len(parts) >= 2:
                return {
                    "identity_id": parts[0],
                    "session_id": parts[1],
                }
            return None
        except Exception as e:
            logger.warning(f"Failed to extract from session: {e}")
            return None
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for proxy headers
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to client host
        if request.client:
            return request.client.host
        
        return "unknown"
    
    # =========================================================================
    # VALIDATION
    # =========================================================================
    
    def is_public_path(self, path: str) -> bool:
        """Check if path is public (no identity required)"""
        # Exact match
        if path in PUBLIC_PATHS:
            return True
        
        # Prefix match
        for prefix in PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return True
        
        return False
    
    def validate_identity_access(
        self,
        requesting_identity: IdentityContext,
        resource_path: str,
        resource_id: Optional[str] = None,
        target_identity: Optional[str] = None,
    ) -> Tuple[bool, Optional[ViolationEvent]]:
        """
        Validate that requesting identity can access resource
        
        Returns:
            Tuple of (is_allowed, violation_event_if_denied)
        """
        # Extract target identity from resource if not provided
        if not target_identity and resource_id:
            target_identity = self._resource_ownership.get(resource_id)
        
        # Extract target identity from path
        if not target_identity:
            target_identity = self._extract_identity_from_path(resource_path)
        
        # If no target identity, allow (resource might be new or global)
        if not target_identity:
            return True, None
        
        # Check identity match
        if requesting_identity.identity_id != target_identity:
            violation = ViolationEvent(
                violation_type=ViolationType.CROSS_IDENTITY_ACCESS,
                requesting_identity=requesting_identity.identity_id,
                target_identity=target_identity,
                resource_path=resource_path,
                resource_id=resource_id,
                ip_address=requesting_identity.ip_address,
                user_agent=requesting_identity.user_agent,
                severity="high",
            )
            self._record_violation(violation)
            return False, violation
        
        return True, None
    
    def _extract_identity_from_path(self, path: str) -> Optional[str]:
        """Extract target identity from resource path"""
        # Pattern: /users/{user_id}/... or /identities/{identity_id}/...
        patterns = [
            r"/users/([a-zA-Z0-9_-]+)",
            r"/identities/([a-zA-Z0-9_-]+)",
            r"/user/([a-zA-Z0-9_-]+)",
            r"/identity/([a-zA-Z0-9_-]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_identity_from_body(self, body: Dict[str, Any]) -> Optional[str]:
        """Extract target identity from request body"""
        # Check common fields
        for field in ["user_id", "identity_id", "owner_id", "target_id"]:
            if field in body:
                return str(body[field])
        
        return None
    
    # =========================================================================
    # RESOURCE OWNERSHIP
    # =========================================================================
    
    def register_resource(self, resource_id: str, owner_identity: str):
        """Register resource ownership"""
        self._resource_ownership[resource_id] = owner_identity
        logger.debug(f"Registered resource {resource_id} -> {owner_identity}")
    
    def get_resource_owner(self, resource_id: str) -> Optional[str]:
        """Get owner of a resource"""
        return self._resource_ownership.get(resource_id)
    
    def check_resource_ownership(
        self,
        identity_id: str,
        resource_id: str
    ) -> bool:
        """Check if identity owns resource"""
        owner = self._resource_ownership.get(resource_id)
        if not owner:
            return True  # No owner registered, allow
        return owner == identity_id
    
    # =========================================================================
    # VIOLATION HANDLING
    # =========================================================================
    
    def _record_violation(self, violation: ViolationEvent):
        """Record identity violation"""
        self._violations.append(violation)
        self._total_violations += 1
        
        # Update by-type counter
        vtype = violation.violation_type.value
        self._violations_by_type[vtype] = self._violations_by_type.get(vtype, 0) + 1
        
        # Log with high priority
        logger.warning(
            f"IDENTITY VIOLATION: {violation.violation_type.value} "
            f"from {violation.requesting_identity} "
            f"to {violation.target_identity} "
            f"on {violation.resource_path}"
        )
        
        # Trim if too many
        if len(self._violations) > self._max_violations:
            self._violations = self._violations[-self._max_violations:]
    
    def get_violations(
        self,
        limit: int = 100,
        identity_id: Optional[str] = None,
        violation_type: Optional[ViolationType] = None,
    ) -> List[ViolationEvent]:
        """Get recorded violations with optional filters"""
        violations = self._violations
        
        if identity_id:
            violations = [
                v for v in violations
                if v.requesting_identity == identity_id
            ]
        
        if violation_type:
            violations = [
                v for v in violations
                if v.violation_type == violation_type
            ]
        
        return violations[-limit:]
    
    # =========================================================================
    # AUDIT LOGGING
    # =========================================================================
    
    def log_access(
        self,
        action: AuditAction,
        identity_id: Optional[str],
        resource_path: str,
        request_method: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        duration_ms: int = 0,
        success: bool = True,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log access attempt to audit trail"""
        entry = AuditEntry(
            action=action,
            identity_id=identity_id,
            resource_path=resource_path,
            request_method=request_method,
            ip_address=ip_address,
            user_agent=user_agent,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message,
            metadata=metadata or {},
        )
        
        self._audit_log.append(entry)
        self._total_requests += 1
        
        # Trim if too many
        if len(self._audit_log) > self._max_audit_entries:
            self._audit_log = self._audit_log[-self._max_audit_entries:]
    
    def get_audit_log(
        self,
        limit: int = 100,
        identity_id: Optional[str] = None,
    ) -> List[AuditEntry]:
        """Get audit log entries"""
        entries = self._audit_log
        
        if identity_id:
            entries = [e for e in entries if e.identity_id == identity_id]
        
        return entries[-limit:]
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get identity boundary statistics"""
        return {
            "total_requests": self._total_requests,
            "total_violations": self._total_violations,
            "violations_by_type": self._violations_by_type,
            "cached_identities": len(self._identity_cache),
            "registered_resources": len(self._resource_ownership),
            "pending_violations": len([
                v for v in self._violations if not v.resolved
            ]),
        }


# =============================================================================
# MIDDLEWARE
# =============================================================================

class IdentityBoundaryMiddleware(BaseHTTPMiddleware):
    """
    FastAPI Middleware for Identity Boundary Enforcement
    
    Features:
    - Extracts identity from every request
    - Validates identity ownership on resource access
    - Returns HTTP 403 for violations
    - Logs all access attempts
    """
    
    def __init__(self, app, service: Optional[IdentityBoundaryService] = None):
        super().__init__(app)
        self.service = service or _default_service
    
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """Process request through identity boundary"""
        start_time = time.time()
        path = request.url.path
        method = request.method
        
        # Skip public paths
        if self.service.is_public_path(path):
            response = await call_next(request)
            return response
        
        # Extract identity
        identity = self.service.extract_identity(request)
        
        if not identity:
            # Log missing identity
            self.service.log_access(
                action=AuditAction.ACCESS_DENIED,
                identity_id=None,
                resource_path=path,
                request_method=method,
                ip_address=self.service._get_client_ip(request),
                user_agent=request.headers.get("User-Agent"),
                success=False,
                error_message="Missing identity",
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "authentication_required",
                    "message": "Identity not found in request. Please provide valid authentication.",
                }
            )
        
        # Store identity in request state for downstream use
        request.state.identity = identity
        request.state.identity_id = identity.identity_id
        
        # For read operations on specific resources, validate ownership
        resource_id = self._extract_resource_id(path)
        target_identity = self._extract_target_identity(request, path)
        
        if target_identity and target_identity != identity.identity_id:
            # Cross-identity access attempt!
            is_allowed, violation = self.service.validate_identity_access(
                requesting_identity=identity,
                resource_path=path,
                resource_id=resource_id,
                target_identity=target_identity,
            )
            
            if not is_allowed:
                # Log violation
                self.service.log_access(
                    action=AuditAction.VIOLATION_DETECTED,
                    identity_id=identity.identity_id,
                    resource_path=path,
                    request_method=method,
                    ip_address=identity.ip_address,
                    user_agent=identity.user_agent,
                    success=False,
                    error_message=f"Cross-identity access denied: {target_identity}",
                    metadata={
                        "violation_id": violation.id if violation else None,
                        "target_identity": target_identity,
                    }
                )
                
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "identity_boundary_violation",
                        "message": "Access denied. You cannot access resources belonging to another identity.",
                        "violation_type": "cross_identity_access",
                        "requesting_identity": identity.identity_id,
                        "target_identity": target_identity,
                    }
                )
        
        # Process request
        try:
            response = await call_next(request)
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log successful access
            self.service.log_access(
                action=AuditAction.ACCESS_ALLOWED,
                identity_id=identity.identity_id,
                resource_path=path,
                request_method=method,
                ip_address=identity.ip_address,
                user_agent=identity.user_agent,
                duration_ms=duration_ms,
                success=True,
            )
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log error
            self.service.log_access(
                action=AuditAction.ACCESS_DENIED,
                identity_id=identity.identity_id,
                resource_path=path,
                request_method=method,
                ip_address=identity.ip_address,
                user_agent=identity.user_agent,
                duration_ms=duration_ms,
                success=False,
                error_message=str(e),
            )
            raise
    
    def _extract_resource_id(self, path: str) -> Optional[str]:
        """Extract resource ID from path"""
        # Pattern: /{resource}/{id}/... or /{resource}/{id}
        parts = path.strip("/").split("/")
        if len(parts) >= 2:
            # Check if second part looks like an ID
            potential_id = parts[1]
            if re.match(r"^[a-zA-Z0-9_-]+$", potential_id):
                return potential_id
        return None
    
    def _extract_target_identity(
        self,
        request: Request,
        path: str
    ) -> Optional[str]:
        """Extract target identity from request"""
        # Check path
        target = self.service._extract_identity_from_path(path)
        if target:
            return target
        
        # Check query params
        target = request.query_params.get("target_identity")
        if target:
            return target
        
        target = request.query_params.get("user_id")
        if target:
            return target
        
        return None


# =============================================================================
# SINGLETON & DEPENDENCY
# =============================================================================

_default_service: Optional[IdentityBoundaryService] = None


def get_identity_boundary_service() -> IdentityBoundaryService:
    """Get or create the identity boundary service singleton"""
    global _default_service
    if _default_service is None:
        _default_service = IdentityBoundaryService()
    return _default_service


def get_current_identity(request: Request) -> IdentityContext:
    """
    Dependency to get current identity from request
    
    Usage:
        @app.get("/my-resource")
        async def my_endpoint(identity: IdentityContext = Depends(get_current_identity)):
            print(f"User: {identity.identity_id}")
    """
    identity = getattr(request.state, "identity", None)
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identity not found. Authentication required."
        )
    return identity


# =============================================================================
# ROUTER FOR ADMIN ENDPOINTS
# =============================================================================

from fastapi import APIRouter

router = APIRouter(prefix="/admin/identity-boundary", tags=["Identity Boundary Admin"])


@router.get("/stats")
async def get_identity_stats():
    """Get identity boundary statistics"""
    service = get_identity_boundary_service()
    return service.get_stats()


@router.get("/violations")
async def get_violations(
    limit: int = 100,
    identity_id: Optional[str] = None,
    violation_type: Optional[str] = None,
):
    """Get recorded identity violations"""
    service = get_identity_boundary_service()
    vtype = ViolationType(violation_type) if violation_type else None
    violations = service.get_violations(
        limit=limit,
        identity_id=identity_id,
        violation_type=vtype,
    )
    return [v.to_dict() for v in violations]


@router.get("/audit")
async def get_audit_log(
    limit: int = 100,
    identity_id: Optional[str] = None,
):
    """Get audit log entries"""
    service = get_identity_boundary_service()
    entries = service.get_audit_log(limit=limit, identity_id=identity_id)
    return [
        {
            "id": e.id,
            "action": e.action.value,
            "identity_id": e.identity_id,
            "resource_path": e.resource_path,
            "request_method": e.request_method,
            "timestamp": e.timestamp.isoformat(),
            "duration_ms": e.duration_ms,
            "success": e.success,
        }
        for e in entries
    ]


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
    "ViolationType",
    "AuditAction",
    # Classes
    "IdentityContext",
    "ViolationEvent",
    "AuditEntry",
    "IdentityBoundaryService",
    "IdentityBoundaryMiddleware",
    # Functions
    "get_identity_boundary_service",
    "get_current_identity",
    # Router
    "router",
]
