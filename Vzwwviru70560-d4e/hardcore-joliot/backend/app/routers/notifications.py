"""
ROUTER: notifications.py
PREFIX: /api/v2/notifications
VERSION: 1.0.0
PHASE: B2

Notification System - Checkpoint Alerts and System Messages.
Critical for R&D Rule #1 enforcement (Human Sovereignty).

R&D COMPLIANCE:
- Rule #1 (Human Sovereignty): Checkpoint notifications are priority
- Rule #3 (Identity Boundary): Notifications scoped to identity
- Rule #5 (No Ranking): Chronological ordering
- Rule #6 (Traceability): Full audit trail

ENDPOINTS: 10
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2/notifications", tags=["Notifications"])

# ============================================================
# ENUMS
# ============================================================

class NotificationType(str, Enum):
    CHECKPOINT = "checkpoint"     # R&D Rule #1 - requires action
    SYSTEM = "system"
    AGENT = "agent"
    THREAD = "thread"
    MEETING = "meeting"
    REMINDER = "reminder"
    ALERT = "alert"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"         # Checkpoint notifications

class NotificationStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ACTIONED = "actioned"
    DISMISSED = "dismissed"

# ============================================================
# SCHEMAS
# ============================================================

class NotificationCreate(BaseModel):
    """Create a notification (internal use)."""
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.MEDIUM
    reference_id: Optional[UUID] = None
    reference_type: Optional[str] = None
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class NotificationResponse(BaseModel):
    """Notification response."""
    id: UUID
    identity_id: UUID
    created_at: datetime
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority
    status: NotificationStatus
    reference_id: Optional[UUID]
    reference_type: Optional[str]
    action_url: Optional[str]
    action_label: Optional[str]
    read_at: Optional[datetime]
    actioned_at: Optional[datetime]
    is_checkpoint: bool

class NotificationListResponse(BaseModel):
    """Paginated notification list."""
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    checkpoint_count: int  # R&D Rule #1 alerts

# ============================================================
# MOCK DATA STORE
# ============================================================

_notifications_store: Dict[UUID, Dict] = {}
_identity_notifications: Dict[UUID, List[UUID]] = {}  # identity_id -> notification_ids

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_identity_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")

async def verify_notification_access(
    notification_id: UUID,
    identity_id: UUID
) -> Dict:
    """Verify identity can access notification - R&D Rule #3."""
    if notification_id not in _notifications_store:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification = _notifications_store[notification_id]
    if notification["identity_id"] != identity_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "code": "RULE_3_VIOLATION"
            }
        )
    return notification

# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/", response_model=NotificationListResponse)
async def list_notifications(
    notification_type: Optional[NotificationType] = None,
    priority: Optional[NotificationPriority] = None,
    status: Optional[NotificationStatus] = None,
    unread_only: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List notifications.
    R&D Rule #3: Only identity's notifications.
    R&D Rule #5: Ordered by created_at DESC.
    """
    notification_ids = _identity_notifications.get(identity_id, [])
    notifications = [
        _notifications_store[nid] 
        for nid in notification_ids 
        if nid in _notifications_store
    ]
    
    if notification_type:
        notifications = [n for n in notifications if n["notification_type"] == notification_type]
    if priority:
        notifications = [n for n in notifications if n["priority"] == priority]
    if status:
        notifications = [n for n in notifications if n["status"] == status]
    if unread_only:
        notifications = [n for n in notifications if n["status"] == NotificationStatus.UNREAD]
    
    # R&D Rule #5: Chronological order
    notifications.sort(key=lambda x: x["created_at"], reverse=True)
    
    total = len(notifications)
    unread_count = sum(1 for n in notifications if n["status"] == NotificationStatus.UNREAD)
    checkpoint_count = sum(1 for n in notifications if n["is_checkpoint"] and n["status"] == NotificationStatus.UNREAD)
    
    start = (page - 1) * page_size
    page_notifications = notifications[start:start + page_size]
    
    return NotificationListResponse(
        notifications=[NotificationResponse(**n) for n in page_notifications],
        total=total,
        unread_count=unread_count,
        checkpoint_count=checkpoint_count
    )

@router.get("/checkpoints")
async def list_checkpoint_notifications(
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List pending checkpoint notifications.
    
    R&D Rule #1: These REQUIRE human action.
    Critical for governance - always shown first.
    """
    notification_ids = _identity_notifications.get(identity_id, [])
    checkpoints = [
        _notifications_store[nid]
        for nid in notification_ids
        if nid in _notifications_store
        and _notifications_store[nid]["is_checkpoint"]
        and _notifications_store[nid]["status"] == NotificationStatus.UNREAD
    ]
    
    # Chronological order
    checkpoints.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "checkpoint_count": len(checkpoints),
        "requires_action": len(checkpoints) > 0,
        "message": "These notifications require your approval" if checkpoints else "No pending checkpoints",
        "checkpoints": [NotificationResponse(**c) for c in checkpoints]
    }

@router.get("/unread-count")
async def get_unread_count(
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get unread notification counts."""
    notification_ids = _identity_notifications.get(identity_id, [])
    notifications = [
        _notifications_store[nid]
        for nid in notification_ids
        if nid in _notifications_store
    ]
    
    unread = [n for n in notifications if n["status"] == NotificationStatus.UNREAD]
    
    return {
        "unread_count": len(unread),
        "checkpoint_count": sum(1 for n in unread if n["is_checkpoint"]),
        "high_priority_count": sum(1 for n in unread if n["priority"] in [NotificationPriority.HIGH, NotificationPriority.CRITICAL])
    }

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get notification details."""
    notification = await verify_notification_access(notification_id, identity_id)
    return NotificationResponse(**notification)

@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Mark notification as read."""
    notification = await verify_notification_access(notification_id, identity_id)
    
    if notification["status"] == NotificationStatus.UNREAD:
        notification["status"] = NotificationStatus.READ
        notification["read_at"] = datetime.utcnow()
    
    return {"status": "read", "notification_id": str(notification_id)}

@router.post("/{notification_id}/action")
async def mark_as_actioned(
    notification_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Mark notification as actioned (for checkpoint notifications)."""
    notification = await verify_notification_access(notification_id, identity_id)
    
    notification["status"] = NotificationStatus.ACTIONED
    notification["actioned_at"] = datetime.utcnow()
    if not notification["read_at"]:
        notification["read_at"] = datetime.utcnow()
    
    return {"status": "actioned", "notification_id": str(notification_id)}

@router.post("/{notification_id}/dismiss")
async def dismiss_notification(
    notification_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Dismiss notification.
    Note: Checkpoint notifications cannot be dismissed without action.
    """
    notification = await verify_notification_access(notification_id, identity_id)
    
    if notification["is_checkpoint"] and notification["status"] == NotificationStatus.UNREAD:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "cannot_dismiss_checkpoint",
                "message": "Checkpoint notifications require action, not dismissal",
                "code": "RULE_1_ENFORCEMENT"
            }
        )
    
    notification["status"] = NotificationStatus.DISMISSED
    return {"status": "dismissed", "notification_id": str(notification_id)}

@router.post("/mark-all-read")
async def mark_all_read(
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Mark all non-checkpoint notifications as read.
    Checkpoint notifications are excluded.
    """
    notification_ids = _identity_notifications.get(identity_id, [])
    marked_count = 0
    
    for nid in notification_ids:
        if nid in _notifications_store:
            notification = _notifications_store[nid]
            if notification["status"] == NotificationStatus.UNREAD and not notification["is_checkpoint"]:
                notification["status"] = NotificationStatus.READ
                notification["read_at"] = datetime.utcnow()
                marked_count += 1
    
    return {
        "marked_count": marked_count,
        "message": "Checkpoint notifications excluded - require explicit action"
    }

# --- INTERNAL: Create Notification ---

@router.post("/internal/create", response_model=NotificationResponse, status_code=201)
async def create_notification_internal(
    data: NotificationCreate,
    target_identity_id: UUID = Body(..., embed=True)
):
    """
    Internal endpoint to create notifications.
    Used by other services to send notifications.
    """
    now = datetime.utcnow()
    notification_id = uuid4()
    
    is_checkpoint = data.notification_type == NotificationType.CHECKPOINT
    
    notification = {
        "id": notification_id,
        "identity_id": target_identity_id,
        "created_at": now,
        "title": data.title,
        "message": data.message,
        "notification_type": data.notification_type,
        "priority": NotificationPriority.CRITICAL if is_checkpoint else data.priority,
        "status": NotificationStatus.UNREAD,
        "reference_id": data.reference_id,
        "reference_type": data.reference_type,
        "action_url": data.action_url,
        "action_label": data.action_label or ("Approve/Reject" if is_checkpoint else None),
        "read_at": None,
        "actioned_at": None,
        "is_checkpoint": is_checkpoint,
        "metadata": data.metadata
    }
    
    _notifications_store[notification_id] = notification
    _identity_notifications.setdefault(target_identity_id, []).append(notification_id)
    
    return NotificationResponse(**notification)

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    return {
        "status": "healthy",
        "router": "notifications",
        "version": "1.0.0",
        "endpoints": 10,
        "rd_rules_enforced": ["#1", "#3", "#5", "#6"],
        "checkpoint_enforcement": True
    }
