"""
CHE·NU™ V75 Backend - Governance Router

RÈGLE ABSOLUE: GOUVERNANCE > EXÉCUTION
- Tout action sensible nécessite approbation
- Checkpoints avec aging visuel (GREEN → YELLOW → RED → BLINK)
- Audit log complet

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import uuid

from config import get_db
from schemas.base import (
    BaseResponse, PaginatedResponse, PaginationMeta,
    CheckpointType, CheckpointStatus
)
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Checkpoint(BaseModel):
    """Governance checkpoint."""
    id: str
    type: CheckpointType
    title: str
    description: str
    status: CheckpointStatus = CheckpointStatus.PENDING
    requester_id: str
    requester_type: str  # 'user', 'agent', 'system'
    resource_type: str
    resource_id: str
    context: dict = {}
    aging_status: str = "green"  # 'green', 'yellow', 'red', 'blink'
    created_at: datetime
    expires_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


class Policy(BaseModel):
    """Governance policy."""
    id: str
    name: str
    description: str
    type: str
    rules: dict
    is_active: bool = True
    created_at: datetime


class AuditLogEntry(BaseModel):
    """Audit log entry."""
    id: str
    action: str
    resource_type: str
    resource_id: str
    actor_id: str
    actor_type: str
    details: dict = {}
    timestamp: datetime


class ApproveCheckpointRequest(BaseModel):
    """Approve checkpoint request."""
    comment: Optional[str] = None


class RejectCheckpointRequest(BaseModel):
    """Reject checkpoint request."""
    reason: str


# ============================================================================
# HELPERS
# ============================================================================

def calculate_aging_status(created_at: datetime, expires_at: Optional[datetime]) -> str:
    """
    Calculate checkpoint aging status.
    
    GREEN: < 25% of time elapsed
    YELLOW: 25-50% elapsed
    RED: 50-75% elapsed
    BLINK: > 75% elapsed (urgent)
    """
    if not expires_at:
        # Default: 24 hours
        expires_at = created_at + timedelta(hours=24)
    
    now = datetime.utcnow()
    total_time = (expires_at - created_at).total_seconds()
    elapsed_time = (now - created_at).total_seconds()
    
    if elapsed_time < 0:
        return "green"
    
    percentage = elapsed_time / total_time
    
    if percentage < 0.25:
        return "green"
    elif percentage < 0.50:
        return "yellow"
    elif percentage < 0.75:
        return "red"
    else:
        return "blink"


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/checkpoints", response_model=PaginatedResponse[Checkpoint])
async def list_checkpoints(
    user: dict = Depends(require_auth),
    status: Optional[CheckpointStatus] = None,
    type: Optional[CheckpointType] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List governance checkpoints."""
    now = datetime.utcnow()
    
    checkpoints = [
        Checkpoint(
            id="ckpt-1",
            type=CheckpointType.COST,
            title="Budget Approval Required",
            description="Approve $25,000 marketing spend",
            status=CheckpointStatus.PENDING,
            requester_id="agent-1",
            requester_type="agent",
            resource_type="budget",
            resource_id="budget-q4",
            context={"amount": 25000, "currency": "CAD"},
            aging_status="yellow",
            created_at=now - timedelta(hours=6),
            expires_at=now + timedelta(hours=18),
        ),
        Checkpoint(
            id="ckpt-2",
            type=CheckpointType.EXTERNAL,
            title="API Integration",
            description="Allow external API call to payment processor",
            status=CheckpointStatus.PENDING,
            requester_id="system",
            requester_type="system",
            resource_type="api",
            resource_id="payment-api",
            aging_status="green",
            created_at=now - timedelta(hours=1),
            expires_at=now + timedelta(hours=23),
        ),
    ]
    
    # Update aging status
    for ckpt in checkpoints:
        ckpt.aging_status = calculate_aging_status(ckpt.created_at, ckpt.expires_at)
    
    # Filter by status
    if status:
        checkpoints = [c for c in checkpoints if c.status == status]
    
    # Filter by type
    if type:
        checkpoints = [c for c in checkpoints if c.type == type]
    
    return PaginatedResponse(
        success=True,
        data=checkpoints,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(checkpoints),
            total_pages=1,
        ),
    )


@router.get("/checkpoints/pending", response_model=BaseResponse[List[Checkpoint]])
async def get_pending_checkpoints(
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get pending checkpoints requiring action."""
    now = datetime.utcnow()
    
    checkpoints = [
        Checkpoint(
            id="ckpt-1",
            type=CheckpointType.COST,
            title="Budget Approval",
            description="Approve Q4 budget",
            status=CheckpointStatus.PENDING,
            requester_id="agent-1",
            requester_type="agent",
            resource_type="budget",
            resource_id="budget-q4",
            aging_status="yellow",
            created_at=now - timedelta(hours=6),
        ),
    ]
    
    return BaseResponse(success=True, data=checkpoints)


@router.get("/checkpoints/{checkpoint_id}", response_model=BaseResponse[Checkpoint])
async def get_checkpoint(
    checkpoint_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get checkpoint details."""
    now = datetime.utcnow()
    
    checkpoint = Checkpoint(
        id=checkpoint_id,
        type=CheckpointType.COST,
        title="Budget Approval",
        description="Approve Q4 marketing budget of $25,000",
        status=CheckpointStatus.PENDING,
        requester_id="agent-1",
        requester_type="agent",
        resource_type="budget",
        resource_id="budget-q4",
        context={"amount": 25000, "currency": "CAD", "department": "Marketing"},
        aging_status="yellow",
        created_at=now - timedelta(hours=6),
        expires_at=now + timedelta(hours=18),
    )
    
    return BaseResponse(success=True, data=checkpoint)


@router.post("/checkpoints/{checkpoint_id}/approve")
async def approve_checkpoint(
    checkpoint_id: str,
    request: ApproveCheckpointRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Approve a checkpoint.
    
    RÈGLE: Only humans can approve checkpoints.
    """
    now = datetime.utcnow()
    
    # TODO: Update in database
    
    return BaseResponse(
        success=True,
        data={
            "id": checkpoint_id,
            "status": "approved",
            "resolved_at": now.isoformat(),
            "resolved_by": user["id"],
        },
    )


@router.post("/checkpoints/{checkpoint_id}/reject")
async def reject_checkpoint(
    checkpoint_id: str,
    request: RejectCheckpointRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Reject a checkpoint."""
    now = datetime.utcnow()
    
    return BaseResponse(
        success=True,
        data={
            "id": checkpoint_id,
            "status": "rejected",
            "reason": request.reason,
            "resolved_at": now.isoformat(),
            "resolved_by": user["id"],
        },
    )


@router.get("/policies", response_model=BaseResponse[List[Policy]])
async def list_policies(
    user: dict = Depends(require_auth),
    active_only: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
):
    """List governance policies."""
    now = datetime.utcnow()
    
    policies = [
        Policy(
            id="policy-1",
            name="Cost Approval",
            description="Requires approval for expenses over $1000",
            type="cost",
            rules={"threshold": 1000, "currency": "CAD"},
            is_active=True,
            created_at=now,
        ),
        Policy(
            id="policy-2",
            name="External API",
            description="Requires approval for external API calls",
            type="external",
            rules={"allow_list": ["api.stripe.com", "api.openai.com"]},
            is_active=True,
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=policies)


@router.get("/audit", response_model=PaginatedResponse[AuditLogEntry])
async def get_audit_log(
    user: dict = Depends(require_auth),
    resource_type: Optional[str] = None,
    action: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get governance audit log."""
    now = datetime.utcnow()
    
    entries = [
        AuditLogEntry(
            id="audit-1",
            action="checkpoint.approve",
            resource_type="checkpoint",
            resource_id="ckpt-old",
            actor_id=user["id"],
            actor_type="user",
            details={"comment": "Approved"},
            timestamp=now - timedelta(hours=2),
        ),
        AuditLogEntry(
            id="audit-2",
            action="agent.hire",
            resource_type="agent",
            resource_id="agent-research",
            actor_id=user["id"],
            actor_type="user",
            details={},
            timestamp=now - timedelta(hours=5),
        ),
    ]
    
    return PaginatedResponse(
        success=True,
        data=entries,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(entries),
            total_pages=1,
        ),
    )
