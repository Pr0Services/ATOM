"""
CHE·NU™ V75 - Activity Router
Activity Feed & Timeline API.

Activity = All system events, user actions, agent activities

GOUVERNANCE > EXÉCUTION
- All activities logged
- Identity-scoped feeds

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

class ActivityCreate(BaseModel):
    """Create activity."""
    activity_type: str  # user_action, agent_action, system_event, governance_event
    action: str
    resource_type: str
    resource_id: str
    description: str
    metadata: Dict[str, Any] = {}


# ============================================================================
# MOCK DATA
# ============================================================================

ACTIVITY_TYPES = ["user_action", "agent_action", "system_event", "governance_event", "integration_event"]

ACTIONS = [
    "created", "updated", "deleted", "archived", "viewed",
    "approved", "denied", "submitted", "completed", "started",
    "uploaded", "downloaded", "shared", "commented", "assigned",
    "switched_identity", "logged_in", "logged_out",
]

RESOURCE_TYPES = [
    "dataspace", "document", "task", "meeting", "thread",
    "agent", "workflow", "checkpoint", "property", "unit",
    "notification", "template", "identity", "memory",
]

MOCK_ACTIVITIES = [
    {
        "id": "act_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "activity_type": "user_action",
        "action": "created",
        "resource_type": "dataspace",
        "resource_id": "ds_001",
        "resource_name": "Projet Maya - Rénovation Cuisine",
        "description": "DataSpace créé: Projet Maya - Rénovation Cuisine",
        "metadata": {"dataspace_type": "construction"},
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": "2026-01-07T16:00:00Z",
    },
    {
        "id": "act_002",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "activity_type": "user_action",
        "action": "uploaded",
        "resource_type": "document",
        "resource_id": "doc_001",
        "resource_name": "Devis Rénovation v3",
        "description": "Document uploadé: Devis Rénovation v3",
        "metadata": {"file_type": "pdf", "size_bytes": 2500000},
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": "2026-01-07T15:30:00Z",
    },
    {
        "id": "act_003",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "activity_type": "agent_action",
        "action": "completed",
        "resource_type": "task",
        "resource_id": "task_001",
        "resource_name": "Analyser les photos du chantier",
        "description": "Nova a complété l'analyse des photos",
        "metadata": {"agent": "nova", "photos_analyzed": 15},
        "actor": {"type": "agent", "id": "nova", "name": "Nova"},
        "created_at": "2026-01-07T15:00:00Z",
    },
    {
        "id": "act_004",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "activity_type": "governance_event",
        "action": "approved",
        "resource_type": "checkpoint",
        "resource_id": "chk_001",
        "resource_name": "Création estimation client",
        "description": "Checkpoint approuvé pour création estimation",
        "metadata": {"workflow_id": "wf_001", "checkpoint_type": "human_approval"},
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": "2026-01-07T14:30:00Z",
    },
    {
        "id": "act_005",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "activity_type": "user_action",
        "action": "switched_identity",
        "resource_type": "identity",
        "resource_id": "identity_002",
        "resource_name": "Entreprise Construction",
        "description": "Changement d'identité: Personnel → Entreprise Construction",
        "metadata": {"from_identity": "identity_001", "to_identity": "identity_002"},
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": "2026-01-07T14:00:00Z",
    },
    {
        "id": "act_006",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "activity_type": "system_event",
        "action": "created",
        "resource_type": "meeting",
        "resource_id": "meet_001",
        "resource_name": "Sprint Planning Q1",
        "description": "Réunion programmée: Sprint Planning Q1",
        "metadata": {"scheduled_at": "2026-01-08T10:00:00Z", "participants": 5},
        "actor": {"type": "system", "id": "system", "name": "Système"},
        "created_at": "2026-01-07T13:00:00Z",
    },
    {
        "id": "act_007",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "activity_type": "user_action",
        "action": "assigned",
        "resource_type": "task",
        "resource_id": "task_002",
        "resource_name": "Commander armoires sur mesure",
        "description": "Tâche assignée à Jonathan",
        "metadata": {"assignee_id": "user_001", "due_date": "2026-01-15"},
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": "2026-01-07T12:00:00Z",
    },
    {
        "id": "act_008",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "activity_type": "integration_event",
        "action": "completed",
        "resource_type": "workflow",
        "resource_id": "wf_002",
        "resource_name": "Rappel loyer automatique",
        "description": "Workflow OneClick exécuté: Rappel loyer",
        "metadata": {"recipients": 3, "emails_sent": 3},
        "actor": {"type": "system", "id": "oneclick", "name": "OneClick"},
        "created_at": "2026-01-07T09:00:00Z",
    },
]


# ============================================================================
# ACTIVITIES
# ============================================================================

@router.get("", response_model=dict)
async def list_activities(
    identity_id: Optional[str] = None,
    activity_type: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    actor_type: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List activities (activity feed).
    
    GOUVERNANCE: Returns only activities for current user.
    """
    activities = MOCK_ACTIVITIES.copy()
    
    # Filter by user
    activities = [a for a in activities if a["user_id"] == "user_001"]
    
    if identity_id:
        activities = [a for a in activities if a["identity_id"] == identity_id]
    if activity_type:
        activities = [a for a in activities if a["activity_type"] == activity_type]
    if action:
        activities = [a for a in activities if a["action"] == action]
    if resource_type:
        activities = [a for a in activities if a["resource_type"] == resource_type]
    if resource_id:
        activities = [a for a in activities if a["resource_id"] == resource_id]
    if actor_type:
        activities = [a for a in activities if a["actor"]["type"] == actor_type]
    
    # Date filters
    if since:
        activities = [a for a in activities if a["created_at"] >= since]
    if until:
        activities = [a for a in activities if a["created_at"] <= until]
    
    # Sort by created_at desc
    activities.sort(key=lambda x: x["created_at"], reverse=True)
    
    total = len(activities)
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    activities = activities[start:end]
    
    return {
        "success": True,
        "data": {
            "activities": activities,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/timeline", response_model=dict)
async def get_timeline(
    identity_id: Optional[str] = None,
    days: int = Query(7, ge=1, le=30),
):
    """
    Get activity timeline grouped by day.
    """
    activities = [a for a in MOCK_ACTIVITIES if a["user_id"] == "user_001"]
    
    if identity_id:
        activities = [a for a in activities if a["identity_id"] == identity_id]
    
    # Group by date
    timeline = {}
    for a in activities:
        date = a["created_at"][:10]  # YYYY-MM-DD
        if date not in timeline:
            timeline[date] = []
        timeline[date].append(a)
    
    # Sort each day's activities
    for date in timeline:
        timeline[date].sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "success": True,
        "data": {
            "timeline": timeline,
            "days_count": len(timeline),
            "total_activities": len(activities),
        },
    }


@router.get("/resource/{resource_type}/{resource_id}", response_model=dict)
async def get_resource_activities(resource_type: str, resource_id: str):
    """
    Get activities for a specific resource.
    """
    activities = [
        a for a in MOCK_ACTIVITIES 
        if a["resource_type"] == resource_type and a["resource_id"] == resource_id
    ]
    
    activities.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "success": True,
        "data": {
            "activities": activities,
            "total": len(activities),
            "resource": {"type": resource_type, "id": resource_id},
        },
    }


@router.get("/stats", response_model=dict)
async def get_activity_stats(
    identity_id: Optional[str] = None,
    days: int = Query(7, ge=1, le=30),
):
    """
    Get activity statistics.
    """
    activities = [a for a in MOCK_ACTIVITIES if a["user_id"] == "user_001"]
    
    if identity_id:
        activities = [a for a in activities if a["identity_id"] == identity_id]
    
    stats = {
        "total_activities": len(activities),
        "by_type": {},
        "by_action": {},
        "by_resource": {},
        "by_actor_type": {},
    }
    
    for a in activities:
        # By type
        t = a["activity_type"]
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
        
        # By action
        act = a["action"]
        stats["by_action"][act] = stats["by_action"].get(act, 0) + 1
        
        # By resource
        res = a["resource_type"]
        stats["by_resource"][res] = stats["by_resource"].get(res, 0) + 1
        
        # By actor type
        actor = a["actor"]["type"]
        stats["by_actor_type"][actor] = stats["by_actor_type"].get(actor, 0) + 1
    
    return {
        "success": True,
        "data": stats,
    }


@router.post("", response_model=dict)
async def create_activity(data: ActivityCreate):
    """
    Create activity (internal logging).
    """
    activity = {
        "id": f"act_{len(MOCK_ACTIVITIES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "activity_type": data.activity_type,
        "action": data.action,
        "resource_type": data.resource_type,
        "resource_id": data.resource_id,
        "resource_name": data.metadata.get("resource_name", ""),
        "description": data.description,
        "metadata": data.metadata,
        "actor": {"type": "user", "id": "user_001", "name": "Jonathan"},
        "created_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_ACTIVITIES.insert(0, activity)
    
    return {
        "success": True,
        "data": activity,
    }


# ============================================================================
# RECENT
# ============================================================================

@router.get("/recent", response_model=dict)
async def get_recent_activities(limit: int = Query(10, ge=1, le=50)):
    """
    Get most recent activities.
    """
    activities = [a for a in MOCK_ACTIVITIES if a["user_id"] == "user_001"]
    activities.sort(key=lambda x: x["created_at"], reverse=True)
    activities = activities[:limit]
    
    return {
        "success": True,
        "data": {
            "activities": activities,
            "total": len(activities),
        },
    }


@router.get("/recent-by-me", response_model=dict)
async def get_my_recent_activities(limit: int = Query(10, ge=1, le=50)):
    """
    Get my recent user actions.
    """
    activities = [
        a for a in MOCK_ACTIVITIES 
        if a["user_id"] == "user_001" and a["actor"]["type"] == "user"
    ]
    activities.sort(key=lambda x: x["created_at"], reverse=True)
    activities = activities[:limit]
    
    return {
        "success": True,
        "data": {
            "activities": activities,
            "total": len(activities),
        },
    }


@router.get("/recent-agents", response_model=dict)
async def get_recent_agent_activities(limit: int = Query(10, ge=1, le=50)):
    """
    Get recent agent activities.
    """
    activities = [
        a for a in MOCK_ACTIVITIES 
        if a["user_id"] == "user_001" and a["activity_type"] == "agent_action"
    ]
    activities.sort(key=lambda x: x["created_at"], reverse=True)
    activities = activities[:limit]
    
    return {
        "success": True,
        "data": {
            "activities": activities,
            "total": len(activities),
        },
    }
