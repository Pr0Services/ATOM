"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V72 — OPA GOVERNANCE                              ║
║                                                                              ║
║  Open Policy Agent integration for governance decisions                      ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from pydantic import BaseModel

from app.core.config import settings, governance_config

logger = logging.getLogger("chenu.governance")

# ═══════════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class GovernanceDecision(BaseModel):
    """Result of a governance check."""
    allowed: bool
    reason: Optional[str] = None
    require_checkpoint: bool = False
    risk_level: str = "low"
    policies_applied: List[str] = []

class CheckpointRequest(BaseModel):
    """Request to create a checkpoint."""
    action_type: str
    description: str
    requested_by: str
    risk_level: str = "low"
    context: Dict[str, Any] = {}

class Checkpoint(BaseModel):
    """Checkpoint awaiting approval."""
    id: str
    action_type: str
    description: str
    requested_by: str
    status: str = "pending"
    risk_level: str = "low"
    context: Dict[str, Any] = {}
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════════
# OPA CLIENT
# ═══════════════════════════════════════════════════════════════════════════════

class OPAClient:
    """Client for Open Policy Agent governance checks."""
    
    def __init__(self):
        self.base_url = settings.OPA_URL
        self.policy_path = settings.OPA_POLICY_PATH
        self.timeout = settings.OPA_TIMEOUT
        self._client = httpx.AsyncClient(timeout=self.timeout)
    
    async def check_policy(
        self,
        action: str,
        resource: str,
        user_id: str,
        context: Dict[str, Any] = {}
    ) -> GovernanceDecision:
        """Check if an action is allowed by OPA policies."""
        
        input_data = {
            "input": {
                "action": action,
                "resource": resource,
                "user_id": user_id,
                "context": context,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }
        
        try:
            response = await self._client.post(
                f"{self.base_url}{self.policy_path}",
                json=input_data
            )
            response.raise_for_status()
            
            result = response.json().get("result", {})
            
            return GovernanceDecision(
                allowed=result.get("allow", False),
                reason=result.get("reason"),
                require_checkpoint=result.get("require_checkpoint", False),
                risk_level=result.get("risk_level", "low"),
                policies_applied=result.get("policies", []),
            )
            
        except httpx.HTTPError as e:
            logger.error(f"OPA request failed: {e}")
            # Default to deny on OPA failure (fail-safe)
            return GovernanceDecision(
                allowed=False,
                reason="Governance service unavailable",
                require_checkpoint=True,
                risk_level="high",
            )
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

# Global OPA client
opa_client = OPAClient()

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def check_governance(
    action: str,
    resource: str,
    user_id: str,
    context: Dict[str, Any] = {}
) -> GovernanceDecision:
    """Check governance rules for an action.
    
    GOUVERNANCE > EXÉCUTION - All actions must pass governance check.
    """
    
    # Check if action requires checkpoint regardless of OPA
    if action in governance_config.REQUIRE_CHECKPOINT_FOR:
        return GovernanceDecision(
            allowed=True,
            require_checkpoint=True,
            risk_level=_determine_risk_level(action, context),
            reason=f"Action '{action}' requires checkpoint approval",
        )
    
    # Check OPA policies
    decision = await opa_client.check_policy(action, resource, user_id, context)
    
    # Log governance decision
    logger.info(
        f"Governance check: action={action}, resource={resource}, "
        f"user={user_id}, allowed={decision.allowed}, "
        f"checkpoint={decision.require_checkpoint}"
    )
    
    return decision

def _determine_risk_level(action: str, context: Dict[str, Any]) -> str:
    """Determine risk level for an action."""
    
    # High-risk actions
    high_risk = ["data_delete", "data_export", "settings_change"]
    if action in high_risk:
        return "high"
    
    # Critical actions
    critical = ["admin_action", "security_change"]
    if action in critical:
        return "critical"
    
    # Check context for risk indicators
    if context.get("external", False):
        return "medium"
    if context.get("sensitive_data", False):
        return "high"
    
    return "low"

# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

# In-memory checkpoint storage (replace with database in production)
_checkpoints: Dict[str, Checkpoint] = {}

async def create_checkpoint(
    action_type: str,
    description: str,
    requested_by: str,
    risk_level: str = "low",
    context: Dict[str, Any] = {}
) -> Checkpoint:
    """Create a new checkpoint for approval."""
    
    checkpoint = Checkpoint(
        id=str(uuid.uuid4()),
        action_type=action_type,
        description=description,
        requested_by=requested_by,
        risk_level=risk_level,
        context=context,
        created_at=datetime.utcnow(),
    )
    
    _checkpoints[checkpoint.id] = checkpoint
    
    logger.info(
        f"Checkpoint created: id={checkpoint.id}, action={action_type}, "
        f"risk={risk_level}, requested_by={requested_by}"
    )
    
    return checkpoint

async def get_checkpoint(checkpoint_id: str) -> Optional[Checkpoint]:
    """Get checkpoint by ID."""
    return _checkpoints.get(checkpoint_id)

async def get_pending_checkpoints(user_id: Optional[str] = None) -> List[Checkpoint]:
    """Get all pending checkpoints."""
    pending = [
        cp for cp in _checkpoints.values()
        if cp.status == "pending"
    ]
    return pending

async def resolve_checkpoint(
    checkpoint_id: str,
    action: str,  # "approve" or "reject"
    resolved_by: str,
    notes: Optional[str] = None
) -> Optional[Checkpoint]:
    """Resolve a checkpoint (approve or reject)."""
    
    checkpoint = _checkpoints.get(checkpoint_id)
    if not checkpoint:
        return None
    
    if checkpoint.status != "pending":
        logger.warning(f"Attempted to resolve non-pending checkpoint: {checkpoint_id}")
        return checkpoint
    
    checkpoint.status = "approved" if action == "approve" else "rejected"
    checkpoint.resolved_at = datetime.utcnow()
    checkpoint.resolved_by = resolved_by
    checkpoint.resolution_notes = notes
    
    logger.info(
        f"Checkpoint resolved: id={checkpoint_id}, action={action}, "
        f"resolved_by={resolved_by}"
    )
    
    return checkpoint

async def execute_if_approved(checkpoint_id: str, executor: callable) -> Any:
    """Execute an action only if checkpoint was approved."""
    
    checkpoint = await get_checkpoint(checkpoint_id)
    
    if not checkpoint:
        raise ValueError(f"Checkpoint {checkpoint_id} not found")
    
    if checkpoint.status != "approved":
        raise PermissionError(
            f"Checkpoint {checkpoint_id} is not approved (status: {checkpoint.status})"
        )
    
    return await executor()

# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

class AuditLog:
    """Audit logging for governance events."""
    
    def __init__(self):
        self._events: List[Dict[str, Any]] = []
    
    def log(
        self,
        event_type: str,
        action: str,
        actor: str,
        target: Optional[str] = None,
        sphere_id: Optional[str] = None,
        details: Dict[str, Any] = {}
    ):
        """Log an audit event."""
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "action": action,
            "actor": actor,
            "target": target,
            "sphere_id": sphere_id,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        self._events.append(event)
        logger.info(f"Audit: {event_type} - {action} by {actor}")
    
    def get_events(
        self,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get audit events with optional filters."""
        events = self._events
        
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        if actor:
            events = [e for e in events if e["actor"] == actor]
        
        return events[-limit:]

# Global audit log
audit_log = AuditLog()

# ═══════════════════════════════════════════════════════════════════════════════
# DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════

def require_checkpoint(action_type: str, risk_level: str = "medium"):
    """Decorator to require checkpoint approval for an endpoint."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user from request
            request = kwargs.get("request") or args[0]
            user_id = getattr(request.state, "user_id", "unknown")
            
            # Create checkpoint
            checkpoint = await create_checkpoint(
                action_type=action_type,
                description=f"Action: {func.__name__}",
                requested_by=user_id,
                risk_level=risk_level,
            )
            
            # Return checkpoint for approval
            return {
                "checkpoint_required": True,
                "checkpoint": checkpoint,
                "message": "Action requires approval"
            }
        
        return wrapper
    return decorator

def audit(event_type: str):
    """Decorator to audit an endpoint."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or args[0]
            user_id = getattr(request.state, "user_id", "unknown")
            
            result = await func(*args, **kwargs)
            
            audit_log.log(
                event_type=event_type,
                action=func.__name__,
                actor=user_id,
                details={"result": "success"}
            )
            
            return result
        
        return wrapper
    return decorator
