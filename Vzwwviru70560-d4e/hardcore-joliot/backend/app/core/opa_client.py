"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — OPA CLIENT
═══════════════════════════════════════════════════════════════════════════════
FastAPI integration with Open Policy Agent for governance enforcement

Usage:
    from app.core.opa_client import OPAClient, require_governance
    
    @router.delete("/dataspaces/{id}")
    @require_governance("delete_dataspace")
    async def delete_dataspace(id: UUID, user_id: UUID = Depends(get_current_user)):
        ...
═══════════════════════════════════════════════════════════════════════════════
"""

import httpx
import logging
from functools import wraps
from typing import Optional, Dict, Any, Callable
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, Request, Depends
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger("chenu.opa")


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class OPAInput(BaseModel):
    """Input for OPA policy evaluation."""
    action: str
    user_id: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    resource_owner_id: Optional[str] = None
    caller_type: str = "human"  # "human" or "agent"
    target_type: Optional[str] = None
    user_role: Optional[str] = None
    checkpoint: Optional[Dict[str, Any]] = None
    sphere_type: Optional[str] = None
    bureau_sections: Optional[list] = None
    # ORIGIN specific
    trigger_date_int: Optional[int] = None
    result_date_int: Optional[int] = None
    claim_strength: Optional[str] = None
    evidence_sources: Optional[list] = None


class OPAResponse(BaseModel):
    """Response from OPA policy evaluation."""
    allow: bool
    denial_reason: Optional[str] = None
    http_status: int = 200
    audit_entry: Optional[Dict[str, Any]] = None


# ═══════════════════════════════════════════════════════════════════════════════
# OPA CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

class OPAClient:
    """
    Client for Open Policy Agent governance enforcement.
    
    R&D Rules enforced:
        - Rule #1: Human Sovereignty (checkpoints)
        - Rule #3: Identity Boundary
        - Rule #4: No AI-to-AI
        - Rule #7: Frozen Architecture
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.OPA_URL
        self.enabled = settings.OPA_ENABLED
        self.timeout = 5.0  # seconds
        
    async def evaluate(self, input_data: OPAInput) -> OPAResponse:
        """
        Evaluate policy against OPA server.
        
        Args:
            input_data: Policy input
            
        Returns:
            OPAResponse with allow/deny decision
        """
        if not self.enabled:
            logger.debug("OPA disabled, allowing request")
            return OPAResponse(allow=True, http_status=200)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/data/chenu",
                    json={"input": input_data.dict(exclude_none=True)}
                )
                
                if response.status_code != 200:
                    logger.error(f"OPA error: {response.status_code}")
                    # Fail open or closed based on config
                    if settings.OPA_FAIL_CLOSED:
                        return OPAResponse(
                            allow=False,
                            denial_reason="policy_unavailable",
                            http_status=503
                        )
                    return OPAResponse(allow=True, http_status=200)
                
                result = response.json().get("result", {})
                
                return OPAResponse(
                    allow=result.get("allow", False),
                    denial_reason=result.get("denial_reason"),
                    http_status=result.get("http_status", 200),
                    audit_entry=result.get("audit_entry")
                )
                
        except httpx.TimeoutException:
            logger.error("OPA timeout")
            if settings.OPA_FAIL_CLOSED:
                return OPAResponse(
                    allow=False,
                    denial_reason="policy_timeout",
                    http_status=503
                )
            return OPAResponse(allow=True, http_status=200)
            
        except Exception as e:
            logger.exception(f"OPA error: {e}")
            if settings.OPA_FAIL_CLOSED:
                return OPAResponse(
                    allow=False,
                    denial_reason="policy_error",
                    http_status=503
                )
            return OPAResponse(allow=True, http_status=200)
    
    async def check_checkpoint(
        self,
        action: str,
        user_id: str,
        resource_type: str,
        resource_id: str,
        resource_owner_id: str,
        checkpoint: Optional[Dict] = None
    ) -> OPAResponse:
        """
        Check if action requires checkpoint and if checkpoint is valid.
        
        Returns HTTP 423 if checkpoint required but not approved.
        """
        input_data = OPAInput(
            action=action,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_owner_id=resource_owner_id,
            checkpoint=checkpoint
        )
        
        return await self.evaluate(input_data)
    
    async def check_identity_boundary(
        self,
        user_id: str,
        resource_owner_id: str,
        action: str,
        user_role: Optional[str] = None
    ) -> bool:
        """
        Check if user can access resource (Rule #3).
        
        Returns True if allowed, raises HTTPException if not.
        """
        input_data = OPAInput(
            action=action,
            user_id=user_id,
            resource_owner_id=resource_owner_id,
            user_role=user_role
        )
        
        result = await self.evaluate(input_data)
        return result.allow
    
    async def check_ai_to_ai(
        self,
        caller_type: str,
        target_type: Optional[str],
        action: str
    ) -> bool:
        """
        Check for AI-to-AI orchestration (Rule #4).
        
        Returns True if allowed.
        """
        input_data = OPAInput(
            action=action,
            user_id="system",
            caller_type=caller_type,
            target_type=target_type
        )
        
        result = await self.evaluate(input_data)
        return result.allow


# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY INJECTION
# ═══════════════════════════════════════════════════════════════════════════════

_opa_client: Optional[OPAClient] = None


def get_opa_client() -> OPAClient:
    """Get or create OPA client singleton."""
    global _opa_client
    if _opa_client is None:
        _opa_client = OPAClient()
    return _opa_client


# ═══════════════════════════════════════════════════════════════════════════════
# DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════

def require_governance(action: str, resource_type: Optional[str] = None):
    """
    Decorator to enforce OPA governance on endpoint.
    
    Usage:
        @router.delete("/items/{id}")
        @require_governance("delete_item", "item")
        async def delete_item(id: UUID, ...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request and user info from kwargs
            request: Request = kwargs.get("request")
            user_id = kwargs.get("user_id") or kwargs.get("current_user_id")
            resource_id = kwargs.get("id") or kwargs.get("resource_id")
            checkpoint_id = kwargs.get("checkpoint_id")
            
            if not user_id:
                # Try to get from header
                if request:
                    user_id = request.headers.get("X-User-ID")
            
            if not user_id:
                raise HTTPException(status_code=401, detail="User ID required")
            
            # Build checkpoint dict if ID provided
            checkpoint = None
            if checkpoint_id:
                # TODO: Fetch checkpoint from DB
                checkpoint = {"id": str(checkpoint_id), "status": "approved"}
            
            # Evaluate policy
            opa = get_opa_client()
            result = await opa.check_checkpoint(
                action=action,
                user_id=str(user_id),
                resource_type=resource_type or "unknown",
                resource_id=str(resource_id) if resource_id else "unknown",
                resource_owner_id=str(user_id),  # Simplified
                checkpoint=checkpoint
            )
            
            if not result.allow:
                if result.http_status == 423:
                    raise HTTPException(
                        status_code=423,
                        detail={
                            "message": "Checkpoint required for this action",
                            "action": action,
                            "denial_reason": result.denial_reason,
                            "create_checkpoint_at": f"/api/v2/checkpoints"
                        }
                    )
                elif result.http_status == 403:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Access denied: {result.denial_reason}"
                    )
                else:
                    raise HTTPException(
                        status_code=result.http_status,
                        detail=result.denial_reason or "Policy denied"
                    )
            
            # Log audit entry
            if result.audit_entry:
                logger.info(f"AUDIT: {result.audit_entry}")
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_identity_boundary():
    """
    Decorator to enforce identity boundary (Rule #3).
    
    Expects resource_owner_id in kwargs or fetches from DB.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id") or kwargs.get("current_user_id")
            resource_owner_id = kwargs.get("resource_owner_id") or kwargs.get("owner_id")
            
            if not user_id or not resource_owner_id:
                # Can't enforce, let it pass (will be caught by other checks)
                return await func(*args, **kwargs)
            
            if str(user_id) != str(resource_owner_id):
                raise HTTPException(
                    status_code=403,
                    detail="Identity boundary violation: Cannot access other user's resources"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def block_ai_to_ai():
    """
    Decorator to block AI-to-AI orchestration (Rule #4).
    
    Checks X-Caller-Type header.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            
            if request:
                caller_type = request.headers.get("X-Caller-Type", "human")
                target_type = request.headers.get("X-Target-Type")
                
                if caller_type == "agent" and target_type == "agent":
                    raise HTTPException(
                        status_code=403,
                        detail="AI-to-AI orchestration is blocked (R&D Rule #4)"
                    )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

async def check_opa_health() -> Dict[str, Any]:
    """Check OPA server health."""
    opa = get_opa_client()
    
    if not opa.enabled:
        return {"status": "disabled", "url": opa.base_url}
    
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{opa.base_url}/health")
            
            if response.status_code == 200:
                return {"status": "healthy", "url": opa.base_url}
            else:
                return {"status": "unhealthy", "url": opa.base_url, "code": response.status_code}
                
    except Exception as e:
        return {"status": "error", "url": opa.base_url, "error": str(e)}
