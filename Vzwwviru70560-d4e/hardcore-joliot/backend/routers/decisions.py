"""
CHE·NU™ V75 Backend - Decisions Router

⚠️ RÈGLE ABSOLUE: LES HUMAINS PRENNENT TOUTES LES DÉCISIONS
- Aucune décision automatique
- Aucun agent autonome
- L'IA illumine, ne décide jamais
- GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import uuid

from config import get_db
from schemas.base import BaseResponse, PaginatedResponse, PaginationMeta, DecisionType, DecisionStatus
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class DecisionOption(BaseModel):
    """Option for a decision."""
    id: str
    label: str
    description: Optional[str] = None
    is_recommended: bool = False
    is_destructive: bool = False
    metadata: dict = {}


class Decision(BaseModel):
    """Decision requiring human input."""
    id: str
    title: str
    description: str
    type: DecisionType
    status: DecisionStatus = DecisionStatus.PENDING
    thread_id: Optional[str] = None
    sphere_id: Optional[str] = None
    options: List[DecisionOption] = []
    ai_context: Optional[str] = None  # AI suggestion (for info only)
    input_placeholder: Optional[str] = None  # For input type
    priority: str = "normal"  # 'low', 'normal', 'high', 'urgent'
    created_at: datetime
    expires_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolved_option: Optional[str] = None
    resolved_input: Optional[str] = None
    resolved_by: Optional[str] = None


class ResolveDecisionRequest(BaseModel):
    """Request to resolve a decision."""
    option_id: str
    input: Optional[str] = None
    comment: Optional[str] = None


class CancelDecisionRequest(BaseModel):
    """Request to cancel a decision."""
    reason: Optional[str] = None


# ============================================================================
# HELPERS
# ============================================================================

def is_decision_urgent(decision: Decision) -> bool:
    """Check if decision is urgent based on priority or expiration."""
    if decision.priority == "urgent":
        return True
    
    if decision.expires_at:
        time_left = decision.expires_at - datetime.utcnow()
        if time_left < timedelta(hours=4):
            return True
    
    return False


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=PaginatedResponse[Decision])
async def list_decisions(
    user: dict = Depends(require_auth),
    status: Optional[DecisionStatus] = None,
    type: Optional[DecisionType] = None,
    sphere_id: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List decisions with filtering."""
    now = datetime.utcnow()
    
    decisions = [
        Decision(
            id="dec-1",
            title="Budget Approval",
            description="Approve Q4 marketing budget of $25,000",
            type=DecisionType.APPROVAL,
            status=DecisionStatus.PENDING,
            sphere_id="business",
            options=[
                DecisionOption(
                    id="opt-approve",
                    label="Approve",
                    description="Approve the budget as proposed",
                    is_recommended=True,
                ),
                DecisionOption(
                    id="opt-reject",
                    label="Reject",
                    description="Reject the budget proposal",
                    is_destructive=True,
                ),
                DecisionOption(
                    id="opt-modify",
                    label="Request modification",
                    description="Ask for budget revision",
                ),
            ],
            ai_context="Based on historical data, this budget is 15% higher than Q3 but aligned with growth targets.",
            priority="high",
            created_at=now - timedelta(hours=2),
            expires_at=now + timedelta(hours=22),
        ),
        Decision(
            id="dec-2",
            title="Agent Task Assignment",
            description="Research Assistant wants to access external API",
            type=DecisionType.CONFIRMATION,
            status=DecisionStatus.PENDING,
            sphere_id="business",
            options=[
                DecisionOption(id="opt-allow", label="Allow", is_recommended=True),
                DecisionOption(id="opt-deny", label="Deny"),
            ],
            ai_context="This API call is required to complete the market analysis task.",
            priority="normal",
            created_at=now - timedelta(minutes=30),
        ),
        Decision(
            id="dec-3",
            title="Project Direction",
            description="Choose the development approach for the new feature",
            type=DecisionType.CHOICE,
            status=DecisionStatus.PENDING,
            sphere_id="team",
            options=[
                DecisionOption(id="opt-a", label="Approach A", description="Faster but limited scope"),
                DecisionOption(id="opt-b", label="Approach B", description="Comprehensive but slower", is_recommended=True),
                DecisionOption(id="opt-c", label="Hybrid", description="Mix of both approaches"),
            ],
            priority="normal",
            created_at=now - timedelta(hours=5),
        ),
    ]
    
    # Filter
    if status:
        decisions = [d for d in decisions if d.status == status]
    if type:
        decisions = [d for d in decisions if d.type == type]
    if sphere_id:
        decisions = [d for d in decisions if d.sphere_id == sphere_id]
    
    return PaginatedResponse(
        success=True,
        data=decisions,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(decisions),
            total_pages=1,
        ),
    )


@router.get("/pending", response_model=BaseResponse[dict])
async def get_pending_decisions(
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Get pending decisions requiring user action.
    
    RÈGLE: HUMAIN DÉCIDE - ces décisions attendent votre input.
    """
    now = datetime.utcnow()
    
    decisions = [
        Decision(
            id="dec-1",
            title="Budget Approval",
            description="Approve Q4 marketing budget",
            type=DecisionType.APPROVAL,
            status=DecisionStatus.PENDING,
            options=[
                DecisionOption(id="opt-approve", label="Approve", is_recommended=True),
                DecisionOption(id="opt-reject", label="Reject", is_destructive=True),
            ],
            priority="high",
            created_at=now,
        ),
    ]
    
    return BaseResponse(
        success=True,
        data={"decisions": decisions},
    )


@router.get("/{decision_id}", response_model=BaseResponse[Decision])
async def get_decision(
    decision_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get decision details."""
    now = datetime.utcnow()
    
    decision = Decision(
        id=decision_id,
        title="Budget Approval",
        description="Approve Q4 marketing budget of $25,000",
        type=DecisionType.APPROVAL,
        status=DecisionStatus.PENDING,
        sphere_id="business",
        options=[
            DecisionOption(id="opt-approve", label="Approve", is_recommended=True),
            DecisionOption(id="opt-reject", label="Reject", is_destructive=True),
        ],
        ai_context="Based on analysis, this budget is aligned with growth targets.",
        created_at=now,
    )
    
    return BaseResponse(success=True, data=decision)


@router.post("/{decision_id}/resolve")
async def resolve_decision(
    decision_id: str,
    request: ResolveDecisionRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Resolve a decision.
    
    RÈGLE: Seul l'HUMAIN peut résoudre une décision.
    """
    now = datetime.utcnow()
    
    # TODO: Update in database
    
    return BaseResponse(
        success=True,
        data={
            "id": decision_id,
            "status": "resolved",
            "resolved_option": request.option_id,
            "resolved_input": request.input,
            "resolved_at": now.isoformat(),
            "resolved_by": user["id"],
        },
    )


@router.post("/{decision_id}/cancel")
async def cancel_decision(
    decision_id: str,
    request: CancelDecisionRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a pending decision."""
    now = datetime.utcnow()
    
    return BaseResponse(
        success=True,
        data={
            "id": decision_id,
            "status": "cancelled",
            "reason": request.reason,
            "cancelled_at": now.isoformat(),
        },
    )


@router.get("/thread/{thread_id}", response_model=BaseResponse[List[Decision]])
async def get_thread_decisions(
    thread_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get decisions related to a thread."""
    now = datetime.utcnow()
    
    decisions = [
        Decision(
            id="dec-thread-1",
            title="Thread Action",
            description="Decision in thread context",
            type=DecisionType.CONFIRMATION,
            status=DecisionStatus.PENDING,
            thread_id=thread_id,
            options=[
                DecisionOption(id="opt-yes", label="Yes"),
                DecisionOption(id="opt-no", label="No"),
            ],
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=decisions)
