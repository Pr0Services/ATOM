"""
CHE·NU™ V75 Backend - Governance Middleware

RÈGLE ABSOLUE: GOUVERNANCE > EXÉCUTION
- Toute action sensible passe par OPA
- Default: DENY
- En cas de doute: DENY

@version 75.0.0
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from config.settings import settings

logger = logging.getLogger("chenu.governance")

# ============================================================================
# SENSITIVE OPERATIONS (require OPA check)
# ============================================================================

SENSITIVE_OPERATIONS = {
    # Agent operations
    ("POST", "/api/v1/agents/hire"): "agent.hire",
    ("POST", "/api/v1/agents/fire"): "agent.fire",
    ("POST", "/api/v1/agents/*/assign"): "agent.assign_task",
    
    # Governance operations
    ("POST", "/api/v1/governance/checkpoints/*/approve"): "governance.approve",
    ("POST", "/api/v1/governance/checkpoints/*/reject"): "governance.reject",
    
    # Decision operations
    ("POST", "/api/v1/decisions/*/resolve"): "decision.resolve",
    
    # XR operations (should be minimal - XR is READ ONLY)
    ("POST", "/api/v1/xr/generate"): "xr.generate",
    
    # Thread operations
    ("DELETE", "/api/v1/threads/*"): "thread.delete",
    ("POST", "/api/v1/threads/*/archive"): "thread.archive",
    
    # DataSpace operations
    ("DELETE", "/api/v1/dataspaces/*"): "dataspace.delete",
    
    # Identity operations
    ("POST", "/api/v1/identities/*/switch"): "identity.switch",
    
    # Nova operations (queries don't need approval, but some actions might)
    ("POST", "/api/v1/nova/execute"): "nova.execute",
}

# ============================================================================
# GOVERNANCE MIDDLEWARE
# ============================================================================

class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces OPA governance policies.
    
    GOUVERNANCE > EXÉCUTION:
    - Checks every request against OPA policies
    - Blocks unauthorized actions
    - Logs all governance decisions
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.opa_client = httpx.AsyncClient(
            base_url=settings.OPA_URL,
            timeout=5.0,
        )
    
    async def dispatch(self, request: Request, call_next):
        """Process each request through governance checks."""
        
        # Skip if OPA is disabled
        if not settings.OPA_ENABLED:
            return await call_next(request)
        
        # Check if this is a sensitive operation
        operation = self._get_operation(request)
        
        if operation:
            # Perform OPA check
            decision = await self._check_policy(request, operation)
            
            # Log the decision
            self._log_decision(request, operation, decision)
            
            # If denied, return 403
            if not decision.get("allow", False):
                return JSONResponse(
                    status_code=403,
                    content={
                        "success": False,
                        "error": {
                            "code": "GOVERNANCE_DENIED",
                            "message": decision.get("reason", "Action denied by governance policy"),
                            "operation": operation,
                        },
                        "meta": {
                            "request_id": getattr(request.state, "request_id", str(uuid.uuid4())),
                            "timestamp": datetime.utcnow().isoformat(),
                            "governance": {
                                "checked": True,
                                "allowed": False,
                                "policy": operation,
                            }
                        }
                    },
                    headers={"X-Governance-Status": "denied"}
                )
            
            # Add governance header
            response = await call_next(request)
            response.headers["X-Governance-Status"] = "approved"
            return response
        
        # Non-sensitive operation, pass through
        return await call_next(request)
    
    def _get_operation(self, request: Request) -> Optional[str]:
        """Determine if request is a sensitive operation."""
        method = request.method
        path = request.url.path
        
        for (op_method, op_pattern), op_name in SENSITIVE_OPERATIONS.items():
            if method != op_method:
                continue
            
            # Check pattern match (supports * wildcard)
            if self._path_matches(path, op_pattern):
                return op_name
        
        return None
    
    def _path_matches(self, path: str, pattern: str) -> bool:
        """Check if path matches pattern with wildcards."""
        path_parts = path.strip("/").split("/")
        pattern_parts = pattern.strip("/").split("/")
        
        if len(path_parts) != len(pattern_parts):
            return False
        
        for pp, pat in zip(path_parts, pattern_parts):
            if pat == "*":
                continue
            if pp != pat:
                return False
        
        return True
    
    async def _check_policy(self, request: Request, operation: str) -> Dict[str, Any]:
        """Check OPA policy for the operation."""
        
        # Build input for OPA
        input_data = {
            "operation": operation,
            "user": {
                "id": getattr(request.state, "user_id", None),
                "identity_id": request.headers.get("X-Identity-ID"),
                "roles": getattr(request.state, "user_roles", []),
            },
            "resource": {
                "path": request.url.path,
                "method": request.method,
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": getattr(request.state, "request_id", str(uuid.uuid4())),
            }
        }
        
        try:
            response = await self.opa_client.post(
                f"/data/{settings.OPA_POLICY_PATH}/allow",
                json={"input": input_data}
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "allow": result.get("result", False),
                    "reason": result.get("reason", "Policy evaluation"),
                }
            else:
                # OPA error - default to DENY
                logger.error(f"OPA error: {response.status_code}")
                return {
                    "allow": False,
                    "reason": "Governance service unavailable - defaulting to DENY",
                }
                
        except Exception as e:
            # Error connecting to OPA - default to DENY
            logger.error(f"OPA connection error: {e}")
            return {
                "allow": False,
                "reason": f"Governance service error: {str(e)} - defaulting to DENY",
            }
    
    def _log_decision(self, request: Request, operation: str, decision: Dict[str, Any]):
        """Log governance decision for audit."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": getattr(request.state, "request_id", "unknown"),
            "operation": operation,
            "path": request.url.path,
            "method": request.method,
            "user_id": getattr(request.state, "user_id", "anonymous"),
            "allowed": decision.get("allow", False),
            "reason": decision.get("reason", ""),
        }
        
        if decision.get("allow"):
            logger.info(f"GOVERNANCE APPROVED: {log_data}")
        else:
            logger.warning(f"GOVERNANCE DENIED: {log_data}")


# ============================================================================
# OPA POLICY HELPER
# ============================================================================

async def check_governance(
    operation: str,
    user_id: str,
    identity_id: Optional[str] = None,
    resource_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Programmatic governance check for use in services.
    
    Returns:
        {"allow": bool, "reason": str, "requires_checkpoint": bool}
    """
    if not settings.OPA_ENABLED:
        return {"allow": True, "reason": "OPA disabled", "requires_checkpoint": False}
    
    input_data = {
        "operation": operation,
        "user": {"id": user_id, "identity_id": identity_id},
        "resource": {"id": resource_id},
        "context": context or {},
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OPA_URL}/data/{settings.OPA_POLICY_PATH}/allow",
                json={"input": input_data},
                timeout=5.0,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "allow": result.get("result", False),
                    "reason": result.get("reason", ""),
                    "requires_checkpoint": result.get("requires_checkpoint", False),
                }
            
    except Exception as e:
        logger.error(f"Governance check error: {e}")
    
    # Default: DENY
    return {
        "allow": False,
        "reason": "Governance check failed - defaulting to DENY",
        "requires_checkpoint": True,
    }
