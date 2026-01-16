"""
CHE·NU™ V75 - Notifications Router
System Notifications API.

Notifications = Real-time alerts, updates, reminders

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class NotificationCreate(BaseModel):
    """Create notification."""
    notification_type: str  # info, success, warning, error, task, meeting, agent, governance
    title: str = Field(..., min_length=1, max_length=200)
    message: str
    priority: str = "normal"  # low, normal, high, urgent
    category: str = "system"  # system, task, meeting, agent, governance, dataspace
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    metadata: Dict[str, Any] = {}
    expires_at: Optional[str] = None


class NotificationUpdate(BaseModel):
    """Update notification."""
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None


class NotificationPreferences(BaseModel):
    """Notification preferences."""
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    quiet_hours_start: Optional[str] = None  # HH:MM
    quiet_hours_end: Optional[str] = None
    categories: Dict[str, bool] = {}


# ============================================================================
# MOCK DATA
# ============================================================================

NOTIFICATION_TYPES = ["info", "success", "warning", "error", "task", "meeting", "agent", "governance"]
NOTIFICATION_PRIORITIES = ["low", "normal", "high", "urgent"]
NOTIFICATION_CATEGORIES = ["system", "task", "meeting", "agent", "governance", "dataspace", "immobilier", "construction"]

MOCK_NOTIFICATIONS = [
    {
        "id": "notif_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "notification_type": "task",
        "title": "Tâche due demain",
        "message": "La tâche 'Commander armoires sur mesure' est due demain.",
        "priority": "high",
        "category": "task",
        "action_url": "/dataspaces/ds_001/tasks/task_001",
        "action_label": "Voir la tâche",
        "metadata": {"task_id": "task_001", "dataspace_id": "ds_001"},
        "is_read": False,
        "is_archived": False,
        "created_at": "2026-01-07T14:00:00Z",
        "read_at": None,
        "expires_at": None,
    },
    {
        "id": "notif_002",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "notification_type": "meeting",
        "title": "Réunion dans 30 minutes",
        "message": "Réunion 'Sprint Planning Q1' commence dans 30 minutes.",
        "priority": "high",
        "category": "meeting",
        "action_url": "/meetings/meet_001",
        "action_label": "Rejoindre",
        "metadata": {"meeting_id": "meet_001"},
        "is_read": False,
        "is_archived": False,
        "created_at": "2026-01-07T15:30:00Z",
        "read_at": None,
        "expires_at": "2026-01-07T16:30:00Z",
    },
    {
        "id": "notif_003",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "notification_type": "governance",
        "title": "Approbation requise",
        "message": "Le workflow 'Créer Estimation' requiert votre approbation.",
        "priority": "urgent",
        "category": "governance",
        "action_url": "/governance/checkpoints/chk_001",
        "action_label": "Approuver",
        "metadata": {"checkpoint_id": "chk_001", "workflow_id": "wf_001"},
        "is_read": False,
        "is_archived": False,
        "created_at": "2026-01-07T16:00:00Z",
        "read_at": None,
        "expires_at": None,
    },
    {
        "id": "notif_004",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "notification_type": "agent",
        "title": "Suggestion de Nova",
        "message": "Nova a une suggestion pour optimiser votre projet.",
        "priority": "normal",
        "category": "agent",
        "action_url": "/nova/suggestions/sugg_001",
        "action_label": "Voir",
        "metadata": {"agent": "nova", "suggestion_id": "sugg_001"},
        "is_read": True,
        "is_archived": False,
        "created_at": "2026-01-07T10:00:00Z",
        "read_at": "2026-01-07T10:15:00Z",
        "expires_at": None,
    },
    {
        "id": "notif_005",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "notification_type": "success",
        "title": "Paiement reçu",
        "message": "Paiement de 1,250$ reçu pour le logement 101.",
        "priority": "normal",
        "category": "immobilier",
        "action_url": "/immobilier/properties/prop_001/payments",
        "action_label": "Voir détails",
        "metadata": {"property_id": "prop_001", "unit_id": "unit_001", "amount": 1250},
        "is_read": True,
        "is_archived": False,
        "created_at": "2026-01-05T09:00:00Z",
        "read_at": "2026-01-05T09:30:00Z",
        "expires_at": None,
    },
]

MOCK_PREFERENCES = {
    "user_001": {
        "email_enabled": True,
        "push_enabled": True,
        "in_app_enabled": True,
        "quiet_hours_start": "22:00",
        "quiet_hours_end": "07:00",
        "categories": {
            "system": True,
            "task": True,
            "meeting": True,
            "agent": True,
            "governance": True,
            "dataspace": True,
            "immobilier": True,
            "construction": True,
        },
    },
}


# ============================================================================
# NOTIFICATIONS
# ============================================================================

@router.get("", response_model=dict)
async def list_notifications(
    identity_id: Optional[str] = None,
    notification_type: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    is_read: Optional[bool] = None,
    is_archived: Optional[bool] = False,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List notifications.
    
    GOUVERNANCE: Returns only notifications for current identity.
    """
    notifications = MOCK_NOTIFICATIONS.copy()
    
    # Filter by current user
    notifications = [n for n in notifications if n["user_id"] == "user_001"]
    
    if identity_id:
        notifications = [n for n in notifications if n["identity_id"] == identity_id]
    if notification_type:
        notifications = [n for n in notifications if n["notification_type"] == notification_type]
    if category:
        notifications = [n for n in notifications if n["category"] == category]
    if priority:
        notifications = [n for n in notifications if n["priority"] == priority]
    if is_read is not None:
        notifications = [n for n in notifications if n["is_read"] == is_read]
    if is_archived is not None:
        notifications = [n for n in notifications if n["is_archived"] == is_archived]
    
    # Sort by created_at desc
    notifications.sort(key=lambda x: x["created_at"], reverse=True)
    
    total = len(notifications)
    
    return {
        "success": True,
        "data": {
            "notifications": notifications,
            "total": total,
            "unread_count": len([n for n in notifications if not n["is_read"]]),
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/unread-count", response_model=dict)
async def get_unread_count(identity_id: Optional[str] = None):
    """
    Get unread notification count.
    """
    notifications = [n for n in MOCK_NOTIFICATIONS if n["user_id"] == "user_001" and not n["is_read"] and not n["is_archived"]]
    
    if identity_id:
        notifications = [n for n in notifications if n["identity_id"] == identity_id]
    
    by_category = {}
    by_priority = {}
    
    for n in notifications:
        cat = n["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
        
        pri = n["priority"]
        by_priority[pri] = by_priority.get(pri, 0) + 1
    
    return {
        "success": True,
        "data": {
            "total": len(notifications),
            "by_category": by_category,
            "by_priority": by_priority,
            "has_urgent": by_priority.get("urgent", 0) > 0,
        },
    }


@router.get("/{notification_id}", response_model=dict)
async def get_notification(notification_id: str):
    """
    Get notification details.
    """
    notification = next((n for n in MOCK_NOTIFICATIONS if n["id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {
        "success": True,
        "data": notification,
    }


@router.post("", response_model=dict)
async def create_notification(data: NotificationCreate):
    """
    Create notification (internal use).
    """
    if data.notification_type not in NOTIFICATION_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid notification type. Must be one of: {NOTIFICATION_TYPES}")
    
    notification = {
        "id": f"notif_{len(MOCK_NOTIFICATIONS) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "notification_type": data.notification_type,
        "title": data.title,
        "message": data.message,
        "priority": data.priority,
        "category": data.category,
        "action_url": data.action_url,
        "action_label": data.action_label,
        "metadata": data.metadata,
        "is_read": False,
        "is_archived": False,
        "created_at": datetime.utcnow().isoformat(),
        "read_at": None,
        "expires_at": data.expires_at,
    }
    
    MOCK_NOTIFICATIONS.append(notification)
    
    return {
        "success": True,
        "data": notification,
    }


@router.patch("/{notification_id}", response_model=dict)
async def update_notification(notification_id: str, data: NotificationUpdate):
    """
    Update notification (mark as read, archive).
    """
    notification = next((n for n in MOCK_NOTIFICATIONS if n["id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if data.is_read is not None:
        notification["is_read"] = data.is_read
        if data.is_read:
            notification["read_at"] = datetime.utcnow().isoformat()
    
    if data.is_archived is not None:
        notification["is_archived"] = data.is_archived
    
    return {
        "success": True,
        "data": notification,
    }


@router.post("/{notification_id}/read", response_model=dict)
async def mark_as_read(notification_id: str):
    """
    Mark notification as read.
    """
    notification = next((n for n in MOCK_NOTIFICATIONS if n["id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification["is_read"] = True
    notification["read_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": notification,
    }


@router.post("/mark-all-read", response_model=dict)
async def mark_all_as_read(identity_id: Optional[str] = None):
    """
    Mark all notifications as read.
    """
    count = 0
    for n in MOCK_NOTIFICATIONS:
        if n["user_id"] == "user_001" and not n["is_read"]:
            if identity_id is None or n["identity_id"] == identity_id:
                n["is_read"] = True
                n["read_at"] = datetime.utcnow().isoformat()
                count += 1
    
    return {
        "success": True,
        "data": {
            "marked_count": count,
        },
        "message": f"{count} notifications marquées comme lues",
    }


@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(notification_id: str):
    """
    Delete notification.
    """
    notification = next((n for n in MOCK_NOTIFICATIONS if n["id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    MOCK_NOTIFICATIONS.remove(notification)
    
    return {
        "success": True,
        "message": "Notification supprimée",
    }


# ============================================================================
# PREFERENCES
# ============================================================================

@router.get("/preferences", response_model=dict)
async def get_preferences():
    """
    Get notification preferences.
    """
    prefs = MOCK_PREFERENCES.get("user_001", {})
    
    return {
        "success": True,
        "data": prefs,
    }


@router.patch("/preferences", response_model=dict)
async def update_preferences(data: NotificationPreferences):
    """
    Update notification preferences.
    """
    MOCK_PREFERENCES["user_001"] = {
        "email_enabled": data.email_enabled,
        "push_enabled": data.push_enabled,
        "in_app_enabled": data.in_app_enabled,
        "quiet_hours_start": data.quiet_hours_start,
        "quiet_hours_end": data.quiet_hours_end,
        "categories": data.categories,
    }
    
    return {
        "success": True,
        "data": MOCK_PREFERENCES["user_001"],
        "message": "Préférences mises à jour",
    }
