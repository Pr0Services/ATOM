"""
CHE·NU™ Nova API Routes
=======================

API endpoints for the Nova Multi-Lane Pipeline.

ENDPOINTS:
- POST /nova/process: Process request through full pipeline
- POST /nova/intent: Analyze intent only (Lane A)
- POST /nova/checkpoint/{id}/approve: Approve pending checkpoint
- POST /nova/checkpoint/{id}/reject: Reject pending checkpoint
- GET /nova/audit/{request_id}: Get audit record for request
- GET /nova/stats: Get Nova pipeline statistics

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - /checkpoint endpoints for approval
- HTTP 423: Returned when checkpoint required
- HTTP 403: Identity boundary violations
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

from backend.core.exceptions import (
    NotFoundError,
    ValidationError,
    ForbiddenError,
    CheckpointRequiredError,
)
from backend.models.agent import SphereType
from backend.services.nova import (
    NovaPipelineService,
    NovaRequest,
    NovaPipelineResult,
    IntentAnalysisResult,
    IntentType,
    ExecutionStatus,
    PipelineLane,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/nova", tags=["Nova Pipeline"])


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class NovaProcessRequest(BaseModel):
    """Request to process through Nova Pipeline."""
    input_text: str = Field(..., min_length=1, max_length=10000)
    thread_id: Optional[UUID] = None
    sphere_type: SphereType = SphereType.PERSONAL
    
    # Optional agent
    agent_id: Optional[UUID] = None
    agent_name: Optional[str] = None
    
    # Options
    input_data: Dict[str, Any] = Field(default_factory=dict)
    max_tokens: int = Field(default=4000, ge=100, le=100000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False


class NovaProcessResponse(BaseModel):
    """Response from Nova Pipeline."""
    request_id: UUID
    status: str
    
    # Output
    output_text: str
    output_data: Dict[str, Any]
    
    # Metadata
    intent_type: Optional[str] = None
    checkpoint_triggered: bool = False
    total_tokens: int = 0
    total_cost: float = 0.0
    duration_ms: int = 0
    
    # If checkpoint required
    checkpoint_id: Optional[UUID] = None
    checkpoint_reason: Optional[str] = None


class IntentAnalysisRequest(BaseModel):
    """Request for intent analysis only."""
    input_text: str = Field(..., min_length=1, max_length=10000)
    sphere_type: SphereType = SphereType.PERSONAL


class IntentAnalysisResponse(BaseModel):
    """Response from intent analysis."""
    intent_type: str
    confidence: float
    requires_checkpoint: bool
    keywords: List[str]
    reasoning: str


class CheckpointApprovalRequest(BaseModel):
    """Request to approve a checkpoint."""
    approved: bool
    reason: Optional[str] = None


class CheckpointResponse(BaseModel):
    """Response after checkpoint action."""
    checkpoint_id: UUID
    status: str
    approved: bool
    approved_at: Optional[datetime] = None
    message: str


class AuditRecordResponse(BaseModel):
    """Audit record for a request."""
    audit_id: UUID
    request_id: UUID
    identity_id: UUID
    
    # Pipeline info
    lanes_executed: List[str]
    total_duration_ms: int
    
    # Results
    final_status: str
    intent_type: str
    checkpoint_triggered: bool
    
    # Token & cost
    total_tokens: int
    total_cost: float
    
    # Timestamps
    started_at: datetime
    completed_at: datetime


class NovaStatsResponse(BaseModel):
    """Nova pipeline statistics."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    checkpoint_triggers: int
    
    # By intent
    requests_by_intent: Dict[str, int]
    
    # Tokens & cost
    total_tokens_used: int
    total_cost: float
    
    # Performance
    avg_duration_ms: float
    p95_duration_ms: float


# =============================================================================
# MOCK DATA (will be replaced with real service)
# =============================================================================

# In-memory stores for demo
_pending_checkpoints: Dict[UUID, Dict[str, Any]] = {}
_audit_records: Dict[UUID, Dict[str, Any]] = {}
_stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "checkpoint_triggers": 0,
    "requests_by_intent": {},
    "total_tokens_used": 0,
    "total_cost": 0.0,
    "durations": [],
}


# =============================================================================
# DEPENDENCY - Get current user
# =============================================================================

async def get_current_user_id() -> UUID:
    """Get current user ID from auth context."""
    # TODO: Integrate with real auth
    from uuid import uuid4
    return uuid4()


# =============================================================================
# ROUTES
# =============================================================================

@router.post(
    "/process",
    response_model=NovaProcessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        423: {"description": "Checkpoint required - awaiting human approval"},
        400: {"description": "Invalid request"},
        403: {"description": "Access denied"},
    },
)
async def process_request(
    request: NovaProcessRequest,
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Process a request through the Nova Multi-Lane Pipeline.
    
    Executes all 7 lanes:
    A → B → C → D → E → F → G
    
    Returns:
    - 200: Request processed successfully
    - 423: Checkpoint required (action needs approval)
    - 400: Invalid request
    - 403: Access denied
    
    When 423 is returned, use /checkpoint/{id}/approve to continue.
    """
    pipeline = NovaPipelineService()
    
    nova_request = NovaRequest(
        identity_id=identity_id,
        thread_id=request.thread_id,
        sphere_type=request.sphere_type,
        input_text=request.input_text,
        input_data=request.input_data,
        agent_id=request.agent_id,
        agent_name=request.agent_name,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stream=request.stream,
    )
    
    try:
        result = await pipeline.process(nova_request)
        
        # Update stats
        _stats["total_requests"] += 1
        if result.status == ExecutionStatus.COMPLETED:
            _stats["successful_requests"] += 1
        else:
            _stats["failed_requests"] += 1
        
        if result.intent:
            intent_key = result.intent.intent_type.value
            _stats["requests_by_intent"][intent_key] = (
                _stats["requests_by_intent"].get(intent_key, 0) + 1
            )
        
        if result.execution:
            _stats["total_tokens_used"] += result.execution.total_tokens
            _stats["total_cost"] += result.execution.cost
        
        _stats["durations"].append(result.total_duration_ms)
        
        # Store audit record
        if result.audit:
            _audit_records[result.request_id] = {
                "audit_id": result.audit.audit_id,
                "request_id": result.request_id,
                "identity_id": identity_id,
                "lanes_executed": result.audit.lanes_executed,
                "total_duration_ms": result.audit.total_duration_ms,
                "final_status": result.audit.final_status.value,
                "intent_type": result.audit.intent_type.value,
                "checkpoint_triggered": result.audit.checkpoint_triggered,
                "total_tokens": result.audit.total_tokens,
                "total_cost": result.audit.total_cost,
                "started_at": result.audit.started_at,
                "completed_at": result.audit.completed_at,
            }
        
        return NovaProcessResponse(
            request_id=result.request_id,
            status=result.status.value,
            output_text=result.output_text,
            output_data=result.output_data,
            intent_type=result.intent.intent_type.value if result.intent else None,
            checkpoint_triggered=result.checkpoint.requires_approval if result.checkpoint else False,
            total_tokens=result.execution.total_tokens if result.execution else 0,
            total_cost=result.execution.cost if result.execution else 0.0,
            duration_ms=result.total_duration_ms,
        )
        
    except CheckpointRequiredError as e:
        # Store pending checkpoint
        _pending_checkpoints[e.checkpoint_id] = {
            "checkpoint_id": e.checkpoint_id,
            "checkpoint_type": e.checkpoint_type,
            "reason": e.reason,
            "action_preview": e.action_preview,
            "identity_id": identity_id,
            "original_request": request.model_dump(),
            "created_at": datetime.utcnow(),
        }
        
        _stats["checkpoint_triggers"] += 1
        
        # Return HTTP 423 Locked
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail={
                "status": "checkpoint_required",
                "checkpoint_id": str(e.checkpoint_id),
                "checkpoint_type": e.checkpoint_type,
                "reason": e.reason,
                "action_preview": e.action_preview,
                "message": "Action requires human approval. Use /checkpoint/{id}/approve to continue.",
            },
        )


@router.post(
    "/intent",
    response_model=IntentAnalysisResponse,
)
async def analyze_intent(
    request: IntentAnalysisRequest,
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Analyze intent only (Lane A).
    
    Useful for previewing what actions will require checkpoints
    without executing the full pipeline.
    """
    from backend.services.nova import IntentAnalyzer, NovaRequest
    
    analyzer = IntentAnalyzer()
    
    nova_request = NovaRequest(
        identity_id=identity_id,
        sphere_type=request.sphere_type,
        input_text=request.input_text,
    )
    
    result = await analyzer.analyze(nova_request)
    
    return IntentAnalysisResponse(
        intent_type=result.intent_type.value,
        confidence=result.confidence,
        requires_checkpoint=result.requires_checkpoint,
        keywords=result.keywords,
        reasoning=result.reasoning,
    )


@router.post(
    "/checkpoint/{checkpoint_id}/approve",
    response_model=NovaProcessResponse,
)
async def approve_checkpoint(
    checkpoint_id: UUID,
    approval: CheckpointApprovalRequest,
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Approve or reject a pending checkpoint.
    
    After approval, the pipeline continues from Lane F (Execution).
    After rejection, the request is cancelled.
    
    Rule #1 Compliance: This endpoint enforces Human Sovereignty
    by requiring explicit approval for sensitive actions.
    """
    # Get pending checkpoint
    checkpoint = _pending_checkpoints.get(checkpoint_id)
    if not checkpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checkpoint not found: {checkpoint_id}",
        )
    
    # Verify identity
    if checkpoint["identity_id"] != identity_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Identity boundary violation: checkpoint belongs to different user",
        )
    
    if not approval.approved:
        # Reject checkpoint
        del _pending_checkpoints[checkpoint_id]
        
        return NovaProcessResponse(
            request_id=checkpoint_id,  # Using checkpoint_id as request_id
            status="rejected",
            output_text=f"Request rejected: {approval.reason or 'User rejected'}",
            output_data={},
            checkpoint_triggered=True,
        )
    
    # Approve and continue pipeline
    pipeline = NovaPipelineService()
    
    # Reconstruct original request
    original = checkpoint["original_request"]
    nova_request = NovaRequest(
        identity_id=identity_id,
        thread_id=original.get("thread_id"),
        sphere_type=SphereType(original["sphere_type"]),
        input_text=original["input_text"],
        input_data=original.get("input_data", {}),
        agent_id=original.get("agent_id"),
        agent_name=original.get("agent_name"),
        max_tokens=original.get("max_tokens", 4000),
        temperature=original.get("temperature", 0.7),
        stream=original.get("stream", False),
    )
    
    # Continue pipeline with approval
    result = await pipeline.approve_checkpoint(
        checkpoint_id=checkpoint_id,
        approved_by=identity_id,
        original_request=nova_request,
    )
    
    # Clean up checkpoint
    del _pending_checkpoints[checkpoint_id]
    
    # Update stats
    _stats["successful_requests"] += 1
    if result.execution:
        _stats["total_tokens_used"] += result.execution.total_tokens
        _stats["total_cost"] += result.execution.cost
    
    return NovaProcessResponse(
        request_id=result.request_id,
        status=result.status.value,
        output_text=result.output_text,
        output_data=result.output_data,
        intent_type=result.intent.intent_type.value if result.intent else None,
        checkpoint_triggered=True,
        total_tokens=result.execution.total_tokens if result.execution else 0,
        total_cost=result.execution.cost if result.execution else 0.0,
        duration_ms=result.total_duration_ms,
    )


@router.get(
    "/checkpoint/{checkpoint_id}",
    response_model=Dict[str, Any],
)
async def get_checkpoint(
    checkpoint_id: UUID,
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Get details of a pending checkpoint.
    """
    checkpoint = _pending_checkpoints.get(checkpoint_id)
    if not checkpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checkpoint not found: {checkpoint_id}",
        )
    
    # Verify identity
    if checkpoint["identity_id"] != identity_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Identity boundary violation",
        )
    
    return {
        "checkpoint_id": str(checkpoint_id),
        "checkpoint_type": checkpoint["checkpoint_type"],
        "reason": checkpoint["reason"],
        "action_preview": checkpoint["action_preview"],
        "created_at": checkpoint["created_at"].isoformat(),
        "status": "pending",
    }


@router.get(
    "/checkpoints/pending",
    response_model=List[Dict[str, Any]],
)
async def list_pending_checkpoints(
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    List all pending checkpoints for the current user.
    """
    user_checkpoints = [
        {
            "checkpoint_id": str(cp["checkpoint_id"]),
            "checkpoint_type": cp["checkpoint_type"],
            "reason": cp["reason"],
            "created_at": cp["created_at"].isoformat(),
        }
        for cp in _pending_checkpoints.values()
        if cp["identity_id"] == identity_id
    ]
    
    return user_checkpoints


@router.get(
    "/audit/{request_id}",
    response_model=AuditRecordResponse,
)
async def get_audit_record(
    request_id: UUID,
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Get audit record for a request.
    
    Rule #6 Compliance: Full traceability of all operations.
    """
    record = _audit_records.get(request_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit record not found: {request_id}",
        )
    
    # Verify identity
    if record["identity_id"] != identity_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Identity boundary violation",
        )
    
    return AuditRecordResponse(**record)


@router.get(
    "/stats",
    response_model=NovaStatsResponse,
)
async def get_stats(
    identity_id: UUID = Depends(get_current_user_id),
):
    """
    Get Nova pipeline statistics.
    """
    durations = _stats["durations"] or [0]
    avg_duration = sum(durations) / len(durations)
    sorted_durations = sorted(durations)
    p95_index = int(len(sorted_durations) * 0.95)
    p95_duration = sorted_durations[p95_index] if sorted_durations else 0
    
    return NovaStatsResponse(
        total_requests=_stats["total_requests"],
        successful_requests=_stats["successful_requests"],
        failed_requests=_stats["failed_requests"],
        checkpoint_triggers=_stats["checkpoint_triggers"],
        requests_by_intent=_stats["requests_by_intent"],
        total_tokens_used=_stats["total_tokens_used"],
        total_cost=_stats["total_cost"],
        avg_duration_ms=avg_duration,
        p95_duration_ms=float(p95_duration),
    )


@router.get("/health")
async def health():
    """Health check for Nova Pipeline."""
    return {
        "status": "healthy",
        "service": "nova_pipeline",
        "version": "1.0.0",
        "lanes": [lane.value for lane in PipelineLane],
    }
