"""
ROUTER: decisions.py
PREFIX: /api/v2/decisions
VERSION: 1.0.0
PHASE: B2

Decision Management with Checkpoint Workflow.
Implements R&D Rule #1 (Human Sovereignty) for governance.

R&D COMPLIANCE:
- Rule #1 (Human Sovereignty): All decisions require explicit approval
- Rule #3 (Identity Boundary): HTTP 403 for cross-identity
- Rule #5 (No Ranking): ORDER BY created_at DESC only
- Rule #6 (Traceability): Full audit trail

ENDPOINTS: 14
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2/decisions", tags=["Decisions"])

# ============================================================
# ENUMS
# ============================================================

class DecisionStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"           # Awaiting approval (checkpoint)
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    EXPIRED = "expired"

class DecisionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DecisionType(str, Enum):
    STANDARD = "standard"         # Normal decision
    GOVERNANCE = "governance"     # System-level
    FINANCIAL = "financial"       # Cost-related
    SENSITIVE = "sensitive"       # Privacy/security
    DESTRUCTIVE = "destructive"   # Delete/archive

# ============================================================
# SCHEMAS
# ============================================================

class DecisionCreate(BaseModel):
    """Create a new decision."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    thread_id: UUID
    decision_type: DecisionType = DecisionType.STANDARD
    severity: DecisionSeverity = DecisionSeverity.MEDIUM
    options: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    auto_submit: bool = False  # If True, immediately creates checkpoint

class DecisionUpdate(BaseModel):
    """Update decision (only in DRAFT status)."""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    options: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

class DecisionApproval(BaseModel):
    """Approve a decision checkpoint."""
    selected_option: Optional[int] = None  # Index of selected option
    approval_notes: Optional[str] = Field(None, max_length=1000)

class DecisionRejection(BaseModel):
    """Reject a decision checkpoint."""
    rejection_reason: str = Field(..., min_length=1, max_length=1000)

class DecisionResponse(BaseModel):
    """Decision response with R&D Rule #6 compliance."""
    id: UUID
    created_by: UUID
    created_at: datetime
    title: str
    description: str
    thread_id: UUID
    decision_type: DecisionType
    severity: DecisionSeverity
    status: DecisionStatus
    options: List[Dict[str, Any]]
    selected_option: Optional[int]
    checkpoint_id: Optional[UUID]
    approved_at: Optional[datetime]
    approved_by: Optional[UUID]
    rejected_at: Optional[datetime]
    rejected_by: Optional[UUID]
    rejection_reason: Optional[str]
    executed_at: Optional[datetime]
    metadata: Optional[Dict[str, Any]]

class CheckpointResponse(BaseModel):
    """Checkpoint for decision approval."""
    id: UUID
    decision_id: UUID
    created_at: datetime
    status: str
    requires_approval: bool
    severity: DecisionSeverity
    expires_at: Optional[datetime]
    options: List[str]

# ============================================================
# MOCK DATA STORE
# ============================================================

_decisions_store: Dict[UUID, Dict] = {}
_checkpoints_store: Dict[UUID, Dict] = {}

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_user_id() -> UUID:
    """Mock current user - replace with real auth."""
    return UUID("11111111-1111-1111-1111-111111111111")

async def verify_decision_ownership(
    decision_id: UUID,
    current_user_id: UUID
) -> Dict:
    """
    Verify user owns the decision - R&D Rule #3.
    """
    if decision_id not in _decisions_store:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    decision = _decisions_store[decision_id]
    if decision["created_by"] != current_user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Access denied: decision belongs to different identity",
                "code": "RULE_3_VIOLATION"
            }
        )
    return decision

# ============================================================
# ENDPOINTS
# ============================================================

# --- LIST & SEARCH ---

@router.get("/", response_model=List[DecisionResponse])
async def list_decisions(
    thread_id: Optional[UUID] = Query(None),
    status: Optional[DecisionStatus] = Query(None),
    severity: Optional[DecisionSeverity] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    List user's decisions.
    
    R&D Rule #3: Only returns decisions owned by current user.
    R&D Rule #5: Ordered by created_at DESC (chronological).
    """
    decisions = [
        d for d in _decisions_store.values()
        if d["created_by"] == current_user_id
    ]
    
    # Apply filters
    if thread_id:
        decisions = [d for d in decisions if d["thread_id"] == thread_id]
    if status:
        decisions = [d for d in decisions if d["status"] == status]
    if severity:
        decisions = [d for d in decisions if d["severity"] == severity]
    
    # R&D Rule #5: Chronological order only
    decisions.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Paginate
    start = (page - 1) * page_size
    return [DecisionResponse(**d) for d in decisions[start:start + page_size]]

@router.get("/pending")
async def list_pending_decisions(
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    List decisions awaiting approval (PENDING status).
    
    R&D Rule #1: These require human action.
    """
    pending = [
        d for d in _decisions_store.values()
        if d["created_by"] == current_user_id
        and d["status"] == DecisionStatus.PENDING
    ]
    
    # Chronological order
    pending.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "pending_count": len(pending),
        "decisions": [DecisionResponse(**d) for d in pending],
        "message": "These decisions require your approval"
    }

# --- CRUD ---

@router.post("/", response_model=DecisionResponse, status_code=201)
async def create_decision(
    data: DecisionCreate,
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Create a new decision.
    
    R&D Rule #1: If auto_submit=True, creates checkpoint immediately.
    R&D Rule #6: Traceability fields added.
    """
    now = datetime.utcnow()
    decision_id = uuid4()
    
    decision = {
        # R&D Rule #6: Traceability
        "id": decision_id,
        "created_by": current_user_id,
        "created_at": now,
        # Decision data
        "title": data.title,
        "description": data.description,
        "thread_id": data.thread_id,
        "decision_type": data.decision_type,
        "severity": data.severity,
        "status": DecisionStatus.DRAFT,
        "options": data.options,
        "selected_option": None,
        "checkpoint_id": None,
        "approved_at": None,
        "approved_by": None,
        "rejected_at": None,
        "rejected_by": None,
        "rejection_reason": None,
        "executed_at": None,
        "metadata": data.metadata or {}
    }
    
    _decisions_store[decision_id] = decision
    
    # If auto_submit, create checkpoint
    if data.auto_submit:
        checkpoint = await _create_checkpoint(decision, current_user_id)
        decision["status"] = DecisionStatus.PENDING
        decision["checkpoint_id"] = checkpoint["id"]
    
    return DecisionResponse(**decision)

@router.get("/{decision_id}", response_model=DecisionResponse)
async def get_decision(
    decision_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Get a specific decision."""
    decision = await verify_decision_ownership(decision_id, current_user_id)
    return DecisionResponse(**decision)

@router.patch("/{decision_id}", response_model=DecisionResponse)
async def update_decision(
    decision_id: UUID = Path(...),
    data: DecisionUpdate = Body(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Update decision (only if DRAFT status).
    
    Once submitted for approval, decision is immutable.
    """
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if decision["status"] != DecisionStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail="Cannot update decision after submission. Only DRAFT decisions can be edited."
        )
    
    if data.title is not None:
        decision["title"] = data.title
    if data.description is not None:
        decision["description"] = data.description
    if data.options is not None:
        decision["options"] = data.options
    if data.metadata is not None:
        decision["metadata"].update(data.metadata)
    
    return DecisionResponse(**decision)

@router.delete("/{decision_id}", status_code=423)
async def delete_decision(
    decision_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Delete a decision - REQUIRES CHECKPOINT.
    
    R&D Rule #1: Destructive actions require approval.
    """
    await verify_decision_ownership(decision_id, current_user_id)
    
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "decision_delete",
                "action": "delete_decision",
                "decision_id": str(decision_id),
                "requires_approval": True,
                "severity": "high",
                "created_at": datetime.utcnow().isoformat(),
                "options": ["approve", "reject"]
            },
            "message": "Decision deletion requires human approval"
        }
    )

# --- CHECKPOINT WORKFLOW (R&D Rule #1) ---

@router.post("/{decision_id}/submit", status_code=423)
async def submit_decision(
    decision_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Submit decision for approval - Creates CHECKPOINT.
    
    R&D Rule #1: Returns HTTP 423 with checkpoint.
    Human must approve before execution.
    """
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if decision["status"] != DecisionStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail=f"Decision already in {decision['status']} status"
        )
    
    # Create checkpoint
    checkpoint = await _create_checkpoint(decision, current_user_id)
    decision["status"] = DecisionStatus.PENDING
    decision["checkpoint_id"] = checkpoint["id"]
    
    # Return HTTP 423 - R&D Rule #1
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint["id"]),
                "type": "decision_approval",
                "decision_id": str(decision_id),
                "decision_title": decision["title"],
                "severity": decision["severity"],
                "requires_approval": True,
                "created_at": checkpoint["created_at"].isoformat(),
                "expires_at": checkpoint["expires_at"].isoformat() if checkpoint.get("expires_at") else None,
                "options": ["approve", "reject"]
            },
            "message": "Decision requires human approval"
        }
    )

@router.post("/{decision_id}/approve", response_model=DecisionResponse)
async def approve_decision(
    decision_id: UUID = Path(...),
    data: DecisionApproval = Body(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Approve a pending decision.
    
    R&D Rule #1: Human explicitly approves.
    """
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if decision["status"] != DecisionStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail=f"Decision is not pending approval (status: {decision['status']})"
        )
    
    now = datetime.utcnow()
    decision["status"] = DecisionStatus.APPROVED
    decision["approved_at"] = now
    decision["approved_by"] = current_user_id
    decision["selected_option"] = data.selected_option
    
    if data.approval_notes:
        decision["metadata"]["approval_notes"] = data.approval_notes
    
    # Update checkpoint
    if decision["checkpoint_id"] in _checkpoints_store:
        _checkpoints_store[decision["checkpoint_id"]]["status"] = "approved"
        _checkpoints_store[decision["checkpoint_id"]]["resolved_at"] = now
    
    return DecisionResponse(**decision)

@router.post("/{decision_id}/reject", response_model=DecisionResponse)
async def reject_decision(
    decision_id: UUID = Path(...),
    data: DecisionRejection = Body(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Reject a pending decision.
    
    R&D Rule #1: Human explicitly rejects.
    """
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if decision["status"] != DecisionStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail=f"Decision is not pending approval (status: {decision['status']})"
        )
    
    now = datetime.utcnow()
    decision["status"] = DecisionStatus.REJECTED
    decision["rejected_at"] = now
    decision["rejected_by"] = current_user_id
    decision["rejection_reason"] = data.rejection_reason
    
    # Update checkpoint
    if decision["checkpoint_id"] in _checkpoints_store:
        _checkpoints_store[decision["checkpoint_id"]]["status"] = "rejected"
        _checkpoints_store[decision["checkpoint_id"]]["resolved_at"] = now
    
    return DecisionResponse(**decision)

@router.post("/{decision_id}/execute", response_model=DecisionResponse)
async def execute_decision(
    decision_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Execute an approved decision.
    
    R&D Rule #1: Only APPROVED decisions can be executed.
    """
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if decision["status"] != DecisionStatus.APPROVED:
        raise HTTPException(
            status_code=400,
            detail="Only approved decisions can be executed"
        )
    
    decision["status"] = DecisionStatus.EXECUTED
    decision["executed_at"] = datetime.utcnow()
    
    return DecisionResponse(**decision)

# --- CHECKPOINT MANAGEMENT ---

@router.get("/{decision_id}/checkpoint", response_model=CheckpointResponse)
async def get_decision_checkpoint(
    decision_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Get the checkpoint for a decision."""
    decision = await verify_decision_ownership(decision_id, current_user_id)
    
    if not decision["checkpoint_id"]:
        raise HTTPException(status_code=404, detail="No checkpoint for this decision")
    
    checkpoint = _checkpoints_store.get(decision["checkpoint_id"])
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    return CheckpointResponse(**checkpoint)

# --- HELPER FUNCTIONS ---

async def _create_checkpoint(decision: Dict, user_id: UUID) -> Dict:
    """Create a checkpoint for a decision."""
    from datetime import timedelta
    
    now = datetime.utcnow()
    checkpoint_id = uuid4()
    
    # Set expiry based on severity
    expiry_hours = {
        DecisionSeverity.LOW: 168,      # 7 days
        DecisionSeverity.MEDIUM: 72,    # 3 days
        DecisionSeverity.HIGH: 24,      # 1 day
        DecisionSeverity.CRITICAL: 4    # 4 hours
    }
    
    checkpoint = {
        "id": checkpoint_id,
        "decision_id": decision["id"],
        "created_at": now,
        "created_by": user_id,
        "status": "pending",
        "requires_approval": True,
        "severity": decision["severity"],
        "expires_at": now + timedelta(hours=expiry_hours.get(decision["severity"], 72)),
        "options": ["approve", "reject"]
    }
    
    _checkpoints_store[checkpoint_id] = checkpoint
    return checkpoint

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    """Health check for decisions router."""
    return {
        "status": "healthy",
        "router": "decisions",
        "version": "1.0.0",
        "endpoints": 14,
        "rd_rules_enforced": ["#1", "#3", "#5", "#6"],
        "checkpoint_workflow": "enabled"
    }
