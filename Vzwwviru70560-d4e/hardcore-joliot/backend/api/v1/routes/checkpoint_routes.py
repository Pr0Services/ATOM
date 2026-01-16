"""
CHE·NU™ Checkpoint API Routes
=============================

API endpoints for governance checkpoints (human gates).

Key endpoints:
- GET /checkpoints - List pending checkpoints
- GET /checkpoints/{id} - Get checkpoint details
- POST /checkpoints/{id}/approve - Approve checkpoint
- POST /checkpoints/{id}/reject - Reject checkpoint

HTTP 423 LOCKED is returned when a checkpoint is required.
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from backend.api.dependencies import get_current_user, get_db
from backend.services.governance.checkpoint_service import (
    CheckpointService,
    AuditService,
)
from backend.models.user import User
from backend.models.governance import CheckpointStatus

router = APIRouter(prefix="/checkpoints", tags=["Governance"])


# =============================================================================
# SCHEMAS
# =============================================================================

class CheckpointResponse(BaseModel):
    """Checkpoint response schema."""
    id: str
    identity_id: str
    thread_id: Optional[str] = None
    checkpoint_type: str
    reason: str
    action_data: dict
    options: List[str]
    status: str
    resolution: Optional[str] = None
    resolution_reason: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    expires_at: Optional[datetime] = None
    metadata: dict
    created_at: datetime

    class Config:
        from_attributes = True


class CheckpointListResponse(BaseModel):
    """Paginated checkpoint list response."""
    checkpoints: List[CheckpointResponse]
    total: int
    limit: int
    offset: int


class ResolveCheckpointRequest(BaseModel):
    """Request to resolve a checkpoint."""
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional reason for resolution"
    )


class AuditLogResponse(BaseModel):
    """Audit log response schema."""
    id: str
    identity_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: dict
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Paginated audit log list response."""
    logs: List[AuditLogResponse]
    total: int
    limit: int
    offset: int


# =============================================================================
# CHECKPOINT ENDPOINTS
# =============================================================================

@router.get(
    "/pending",
    response_model=List[CheckpointResponse],
    summary="List pending checkpoints",
    description="Get all pending checkpoints requiring user approval"
)
async def list_pending_checkpoints(
    thread_id: Optional[UUID] = Query(None, description="Filter by thread"),
    checkpoint_type: Optional[str] = Query(None, description="Filter by type"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """List pending checkpoints for the current user."""
    service = CheckpointService(db)
    
    checkpoints = await service.list_pending_checkpoints(
        identity_id=UUID(current_user.identity_id),
        thread_id=thread_id,
        checkpoint_type=checkpoint_type,
        limit=limit,
    )
    
    return [
        CheckpointResponse(**cp.to_dict())
        for cp in checkpoints
    ]


@router.get(
    "",
    response_model=CheckpointListResponse,
    summary="List all checkpoints",
    description="Get checkpoints with optional filters and pagination"
)
async def list_checkpoints(
    status: Optional[str] = Query(None, description="Filter by status"),
    thread_id: Optional[UUID] = Query(None, description="Filter by thread"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """List checkpoints with pagination."""
    service = CheckpointService(db)
    
    checkpoints, total = await service.list_checkpoints(
        identity_id=UUID(current_user.identity_id),
        status=status,
        thread_id=thread_id,
        limit=limit,
        offset=offset,
    )
    
    return CheckpointListResponse(
        checkpoints=[
            CheckpointResponse(**cp.to_dict())
            for cp in checkpoints
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{checkpoint_id}",
    response_model=CheckpointResponse,
    summary="Get checkpoint details",
    description="Get a specific checkpoint by ID"
)
async def get_checkpoint(
    checkpoint_id: UUID,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get a checkpoint by ID."""
    service = CheckpointService(db)
    
    try:
        checkpoint = await service.get_checkpoint(
            checkpoint_id=checkpoint_id,
            identity_id=UUID(current_user.identity_id),
        )
        return CheckpointResponse(**checkpoint.to_dict())
    
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        if "identity boundary" in str(e).lower():
            raise HTTPException(status_code=403, detail=str(e))
        raise


@router.post(
    "/{checkpoint_id}/approve",
    response_model=CheckpointResponse,
    summary="Approve checkpoint",
    description="Approve a pending checkpoint to allow the action"
)
async def approve_checkpoint(
    checkpoint_id: UUID,
    request: ResolveCheckpointRequest = ResolveCheckpointRequest(),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Approve a pending checkpoint.
    
    This allows the originally blocked action to proceed.
    """
    service = CheckpointService(db)
    
    try:
        checkpoint = await service.approve_checkpoint(
            checkpoint_id=checkpoint_id,
            identity_id=UUID(current_user.identity_id),
            reason=request.reason,
        )
        await db.commit()
        return CheckpointResponse(**checkpoint.to_dict())
    
    except Exception as e:
        await db.rollback()
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        if "identity boundary" in str(e).lower():
            raise HTTPException(status_code=403, detail=str(e))
        if "already resolved" in str(e).lower() or "expired" in str(e).lower():
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{checkpoint_id}/reject",
    response_model=CheckpointResponse,
    summary="Reject checkpoint",
    description="Reject a pending checkpoint to cancel the action"
)
async def reject_checkpoint(
    checkpoint_id: UUID,
    request: ResolveCheckpointRequest = ResolveCheckpointRequest(),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Reject a pending checkpoint.
    
    This cancels the originally blocked action.
    """
    service = CheckpointService(db)
    
    try:
        checkpoint = await service.reject_checkpoint(
            checkpoint_id=checkpoint_id,
            identity_id=UUID(current_user.identity_id),
            reason=request.reason,
        )
        await db.commit()
        return CheckpointResponse(**checkpoint.to_dict())
    
    except Exception as e:
        await db.rollback()
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        if "identity boundary" in str(e).lower():
            raise HTTPException(status_code=403, detail=str(e))
        if "already resolved" in str(e).lower() or "expired" in str(e).lower():
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# AUDIT LOG ENDPOINTS
# =============================================================================

@router.get(
    "/audit/me",
    response_model=List[AuditLogResponse],
    summary="Get my activity",
    description="Get recent audit logs for the current user"
)
async def get_my_activity(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get recent activity for the current user."""
    service = AuditService(db)
    
    logs = await service.get_user_activity(
        identity_id=UUID(current_user.identity_id),
        limit=limit,
    )
    
    return [
        AuditLogResponse(**log.to_dict())
        for log in logs
    ]


@router.get(
    "/audit/resource/{resource_type}/{resource_id}",
    response_model=List[AuditLogResponse],
    summary="Get resource history",
    description="Get audit history for a specific resource"
)
async def get_resource_history(
    resource_type: str,
    resource_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get audit history for a specific resource."""
    service = AuditService(db)
    
    logs = await service.get_resource_history(
        resource_type=resource_type,
        resource_id=resource_id,
        limit=limit,
    )
    
    return [
        AuditLogResponse(**log.to_dict())
        for log in logs
    ]


@router.get(
    "/audit",
    response_model=AuditLogListResponse,
    summary="Query audit logs",
    description="Query audit logs with filters and pagination"
)
async def query_audit_logs(
    action: Optional[str] = Query(None, description="Filter by action"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    resource_id: Optional[UUID] = Query(None, description="Filter by resource ID"),
    start_date: Optional[datetime] = Query(None, description="Filter from date"),
    end_date: Optional[datetime] = Query(None, description="Filter to date"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """
    Query audit logs with filters.
    
    Only returns logs for the current user's identity.
    Admin users can see all logs (future feature).
    """
    service = AuditService(db)
    
    # Regular users only see their own logs
    identity_id = UUID(current_user.identity_id)
    
    logs, total = await service.list_logs(
        identity_id=identity_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )
    
    return AuditLogListResponse(
        logs=[
            AuditLogResponse(**log.to_dict())
            for log in logs
        ],
        total=total,
        limit=limit,
        offset=offset,
    )
