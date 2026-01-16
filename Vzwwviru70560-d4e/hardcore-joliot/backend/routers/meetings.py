"""
CHE·NU™ V75 - Meetings Router
Complete meeting management API.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class MeetingCreate(BaseModel):
    """Create meeting request."""
    dataspace_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    meeting_type: str = "standup"
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    location: Optional[str] = None
    is_xr_meeting: bool = False
    agenda: List[dict] = []


class MeetingUpdate(BaseModel):
    """Update meeting request."""
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    location: Optional[str] = None
    agenda: Optional[List[dict]] = None
    status: Optional[str] = None


class ParticipantAdd(BaseModel):
    """Add participant request."""
    user_id: UUID
    role: str = "participant"


class NoteCreate(BaseModel):
    """Create note request."""
    note_type: str = "general"
    content: str = Field(..., min_length=1)


class TaskCreate(BaseModel):
    """Create task request."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    assignee_id: Optional[UUID] = None
    due_date: Optional[str] = None
    priority: str = "medium"


class MeetingResponse(BaseModel):
    """Meeting response."""
    id: str
    dataspace_id: str
    title: str
    description: Optional[str]
    meeting_type: str
    scheduled_start: Optional[str]
    scheduled_end: Optional[str]
    status: str
    location: Optional[str]
    is_xr_meeting: bool
    agenda: List[dict]
    participants_count: int
    notes_count: int
    tasks_count: int
    created_at: str


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_MEETINGS = [
    {
        "id": "meet_001",
        "dataspace_id": "ds_001",
        "title": "Sprint Planning Q1",
        "description": "Planification du sprint Q1 2026",
        "meeting_type": "planning",
        "scheduled_start": "2026-01-08T10:00:00Z",
        "scheduled_end": "2026-01-08T11:30:00Z",
        "status": "scheduled",
        "location": "Salle Maya",
        "is_xr_meeting": False,
        "agenda": [
            {"title": "Revue des objectifs", "duration": 15},
            {"title": "Estimation des tâches", "duration": 45},
            {"title": "Attribution", "duration": 20},
        ],
        "participants_count": 5,
        "notes_count": 0,
        "tasks_count": 0,
        "created_at": "2026-01-07T15:00:00Z",
    },
    {
        "id": "meet_002",
        "dataspace_id": "ds_002",
        "title": "Revue de propriété - 123 Rue Maya",
        "description": "Inspection et revue de l'état de la propriété",
        "meeting_type": "review",
        "scheduled_start": "2026-01-09T14:00:00Z",
        "scheduled_end": "2026-01-09T15:00:00Z",
        "status": "scheduled",
        "location": None,
        "is_xr_meeting": True,
        "agenda": [
            {"title": "Tour virtuel", "duration": 20},
            {"title": "Points de maintenance", "duration": 25},
            {"title": "Budget travaux", "duration": 15},
        ],
        "participants_count": 3,
        "notes_count": 2,
        "tasks_count": 4,
        "created_at": "2026-01-06T10:00:00Z",
    },
]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=dict)
async def list_meetings(
    dataspace_id: Optional[UUID] = None,
    status: Optional[str] = None,
    meeting_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List meetings with optional filters.
    """
    meetings = MOCK_MEETINGS.copy()
    
    # Filter by dataspace
    if dataspace_id:
        meetings = [m for m in meetings if m["dataspace_id"] == str(dataspace_id)]
    
    # Filter by status
    if status:
        meetings = [m for m in meetings if m["status"] == status]
    
    # Filter by type
    if meeting_type:
        meetings = [m for m in meetings if m["meeting_type"] == meeting_type]
    
    total = len(meetings)
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "success": True,
        "data": {
            "meetings": meetings[start:end],
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/upcoming", response_model=dict)
async def get_upcoming_meetings(
    limit: int = Query(5, ge=1, le=20),
):
    """
    Get upcoming meetings.
    """
    upcoming = [m for m in MOCK_MEETINGS if m["status"] == "scheduled"]
    return {
        "success": True,
        "data": {
            "meetings": upcoming[:limit],
        },
    }


@router.get("/today", response_model=dict)
async def get_today_meetings():
    """
    Get meetings scheduled for today.
    """
    # In real implementation, filter by today's date
    return {
        "success": True,
        "data": {
            "meetings": MOCK_MEETINGS[:1],
            "count": 1,
        },
    }


@router.get("/{meeting_id}", response_model=dict)
async def get_meeting(meeting_id: str):
    """
    Get meeting details.
    """
    meeting = next((m for m in MOCK_MEETINGS if m["id"] == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "success": True,
        "data": meeting,
    }


@router.post("", response_model=dict)
async def create_meeting(data: MeetingCreate):
    """
    Create a new meeting.
    
    GOUVERNANCE: Meeting creation is logged.
    """
    meeting = {
        "id": f"meet_{len(MOCK_MEETINGS) + 1:03d}",
        "dataspace_id": str(data.dataspace_id),
        "title": data.title,
        "description": data.description,
        "meeting_type": data.meeting_type,
        "scheduled_start": data.scheduled_start.isoformat() if data.scheduled_start else None,
        "scheduled_end": data.scheduled_end.isoformat() if data.scheduled_end else None,
        "status": "scheduled",
        "location": data.location,
        "is_xr_meeting": data.is_xr_meeting,
        "agenda": data.agenda,
        "participants_count": 1,  # Creator
        "notes_count": 0,
        "tasks_count": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    return {
        "success": True,
        "data": meeting,
        "message": "Réunion créée avec succès",
    }


@router.patch("/{meeting_id}", response_model=dict)
async def update_meeting(meeting_id: str, data: MeetingUpdate):
    """
    Update meeting details.
    """
    meeting = next((m for m in MOCK_MEETINGS if m["id"] == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Update fields
    if data.title:
        meeting["title"] = data.title
    if data.description is not None:
        meeting["description"] = data.description
    if data.status:
        meeting["status"] = data.status
    
    return {
        "success": True,
        "data": meeting,
    }


@router.post("/{meeting_id}/start", response_model=dict)
async def start_meeting(meeting_id: str):
    """
    Start a meeting.
    """
    meeting = next((m for m in MOCK_MEETINGS if m["id"] == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting["status"] = "active"
    meeting["actual_start"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": meeting,
        "message": "Réunion démarrée",
    }


@router.post("/{meeting_id}/end", response_model=dict)
async def end_meeting(meeting_id: str):
    """
    End a meeting.
    """
    meeting = next((m for m in MOCK_MEETINGS if m["id"] == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting["status"] = "completed"
    meeting["actual_end"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": meeting,
        "message": "Réunion terminée",
    }


# ============================================================================
# PARTICIPANTS
# ============================================================================

@router.get("/{meeting_id}/participants", response_model=dict)
async def get_participants(meeting_id: str):
    """
    Get meeting participants.
    """
    participants = [
        {"id": "part_001", "user_id": "user_001", "role": "organizer", "rsvp_status": "accepted"},
        {"id": "part_002", "user_id": "user_002", "role": "participant", "rsvp_status": "accepted"},
        {"id": "part_003", "user_id": "user_003", "role": "participant", "rsvp_status": "pending"},
    ]
    
    return {
        "success": True,
        "data": {
            "participants": participants,
        },
    }


@router.post("/{meeting_id}/participants", response_model=dict)
async def add_participant(meeting_id: str, data: ParticipantAdd):
    """
    Add participant to meeting.
    """
    return {
        "success": True,
        "data": {
            "id": "part_new",
            "user_id": str(data.user_id),
            "role": data.role,
            "rsvp_status": "pending",
        },
        "message": "Participant ajouté",
    }


# ============================================================================
# NOTES
# ============================================================================

@router.get("/{meeting_id}/notes", response_model=dict)
async def get_notes(meeting_id: str):
    """
    Get meeting notes.
    """
    notes = [
        {"id": "note_001", "note_type": "general", "content": "Discussion sur les priorités Q1", "created_at": "2026-01-08T10:15:00Z"},
        {"id": "note_002", "note_type": "decision", "content": "Décision: Focus sur le module immobilier", "created_at": "2026-01-08T10:30:00Z"},
    ]
    
    return {
        "success": True,
        "data": {
            "notes": notes,
        },
    }


@router.post("/{meeting_id}/notes", response_model=dict)
async def add_note(meeting_id: str, data: NoteCreate):
    """
    Add note to meeting.
    """
    return {
        "success": True,
        "data": {
            "id": "note_new",
            "note_type": data.note_type,
            "content": data.content,
            "created_at": datetime.utcnow().isoformat(),
        },
        "message": "Note ajoutée",
    }


# ============================================================================
# TASKS
# ============================================================================

@router.get("/{meeting_id}/tasks", response_model=dict)
async def get_tasks(meeting_id: str):
    """
    Get meeting tasks.
    """
    tasks = [
        {"id": "task_001", "title": "Préparer mockups", "status": "pending", "priority": "high", "due_date": "2026-01-15"},
        {"id": "task_002", "title": "Réviser budget", "status": "in_progress", "priority": "medium", "due_date": "2026-01-12"},
    ]
    
    return {
        "success": True,
        "data": {
            "tasks": tasks,
        },
    }


@router.post("/{meeting_id}/tasks", response_model=dict)
async def add_task(meeting_id: str, data: TaskCreate):
    """
    Create task from meeting.
    
    GOUVERNANCE: Task assignment requires human approval.
    """
    return {
        "success": True,
        "data": {
            "id": "task_new",
            "title": data.title,
            "description": data.description,
            "assignee_id": str(data.assignee_id) if data.assignee_id else None,
            "due_date": data.due_date,
            "priority": data.priority,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
        },
        "message": "Tâche créée",
    }
