"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V75 — IDENTITY BOUNDARY MIDDLEWARE                ║
║                                                                              ║
║  HTTP 403 FORBIDDEN pour violations de frontières d'identité                 ║
║  RÈGLE R&D #3: Sphere Integrity - No cross-identity access                   ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)

# Patterns de routes qui nécessitent vérification d'identité
PROTECTED_PATTERNS = [
    r'/api/v1/threads/([^/]+)',
    r'/api/v1/decisions/([^/]+)',
    r'/api/v1/agents/([^/]+)',
    r'/api/v1/files/([^/]+)',
    r'/api/v1/memory/thread/([^/]+)',
    r'/api/v1/xr/environments/([^/]+)',
    r'/api/v1/spheres/([^/]+)',
]

# Routes exemptées
EXEMPT_ROUTES = [
    '/api/v1/auth/',
    '/api/v1/health',
    '/api/v1/search/',
    '/api/v1/xr/templates',
    '/docs',
    '/redoc',
    '/openapi.json',
    '/health',
    '/',
]

class IdentityBoundaryMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour enforcer les frontières d'identité.
    
    Règle: Un utilisateur ne peut accéder qu'à ses propres ressources.
    Violation = HTTP 403 FORBIDDEN
    """
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip routes exemptées
        for exempt in EXEMPT_ROUTES:
            if path.startswith(exempt):
                return await call_next(request)
        
        # Extraire user_id
        current_user_id = self._extract_user_id(request)
        
        if current_user_id is None:
            return await call_next(request)
        
        # Vérifier ownership
        resource_owner_id = await self._get_resource_owner(request)
        
        if resource_owner_id and resource_owner_id != current_user_id:
            logger.warning(
                f"Identity boundary violation: user {current_user_id} "
                f"attempted to access resource owned by {resource_owner_id}"
            )
            
            return JSONResponse(
                status_code=403,
                content={
                    "error": "identity_boundary_violation",
                    "message": "Access denied: resource belongs to different identity",
                    "requested_identity": current_user_id,
                    "resource_identity": resource_owner_id,
                    "rule": "R&D Rule #3: Sphere Integrity",
                }
            )
        
        return await call_next(request)
    
    def _extract_user_id(self, request: Request) -> Optional[str]:
        """Extract user ID from authorization header."""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            if "_" in token:
                return token.split("_")[1]
        return request.headers.get("X-User-ID")
    
    async def _get_resource_owner(self, request: Request) -> Optional[str]:
        """Get resource owner (mock - real impl would query DB)."""
        return None


def create_identity_boundary_error(
    requested_by: str,
    resource_owner: str,
    resource_type: str = "resource",
) -> HTTPException:
    """Create HTTP 403 exception for boundary violation."""
    return HTTPException(
        status_code=403,
        detail={
            "error": "identity_boundary_violation",
            "message": f"Access denied: {resource_type} belongs to different identity",
            "requested_identity": requested_by,
            "resource_identity": resource_owner,
        }
    )


def verify_ownership(
    resource_owner_id: str,
    current_user_id: str,
    resource_type: str = "resource",
) -> None:
    """Verify ownership or raise HTTP 403."""
    if resource_owner_id != current_user_id:
        raise create_identity_boundary_error(
            requested_by=current_user_id,
            resource_owner=resource_owner_id,
            resource_type=resource_type,
        )
