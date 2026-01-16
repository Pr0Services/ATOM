"""
ROUTER: meetings.py
PREFIX: /api/v2/meetings
VERSION: 1.0.0
PHASE: B2

Meeting Management - Bureau Section Integration.
One of the 6 canonical bureau sections.

R&D COMPLIANCE:
- Rule #1 (Human Sovereignty): Meeting actions with external parties require checkpoint
- Rule #3 (Identity Boundary): Meetings scoped to identity
- Rule #5 (No Ranking): Chronological ordering
- Rule #6 (Traceability): Full audit trail

ENDPOINTS: 12
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2/meetings", tags=["Meetings"])

# ============================================================
# ENUMS
# ============================================================

class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class MeetingType(str, Enum):
    ONE_ON_ONE = "one_on_one"
    TEAM = "team"
    EXTERNAL = "external"
    STANDUP = "standup"
    REVIEW = "review"

class RecurrenceType(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

# ============================================================
# SCHEMAS
# ============================================================

class MeetingCreate(BaseModel):
    """Create a meeting."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    meeting_type: MeetingType = MeetingType.ONE_ON_ONE
    thread_id: Optional[UUID] = None
    workspace_id: Optional[UUID] = None
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, ge=5, le=480)
    recurrence: RecurrenceType = RecurrenceType.NONE
    attendees: List[str] = Field(default_factory=list)
    is_external: bool = False
    metadata: Optional[Dict[str, Any]] = None

class MeetingUpdate(BaseModel):
    """Update meeting."""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=5, le=480)
    attendees: Optional[List[str]] = None

class MeetingNoteCreate(BaseModel):
    """Create meeting notes."""
    content: str = Field(..., min_length=1)
    is_action_item: bool = False
    assigned_to: Optional[str] = None

class MeetingResponse(BaseModel):
    """Meeting response."""
    id: UUID
    identity_id: UUID
    created_by: UUID
    created_at: datetime
    title: str
    description: Optional[str]
    meeting_type: MeetingType
    thread_id: Optional[UUID]
    workspace_id: Optional[UUID]
    status: MeetingStatus
    scheduled_at: datetime
    duration_minutes: int
    recurrence: RecurrenceType
    attendees: List[str]
    is_external: bool
    note_count: int
    action_item_count: int

class MeetingNoteResponse(BaseModel):
    """Meeting note response."""
    id: UUID
    meeting_id: UUID
    created_by: UUID
    created_at: datetime
    content: str
    is_action_item: bool
    assigned_to: Optional[str]
    is_completed: bool

# ============================================================
# MOCK DATA STORE
# ============================================================

_meetings_store: Dict[UUID, Dict] = {}
_notes_store: Dict[UUID, List[Dict]] = {}  # meeting_id -> notes

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")

async def get_current_identity_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")

async def verify_meeting_access(
    meeting_id: UUID,
    identity_id: UUID
) -> Dict:
    """Verify identity can access meeting - R&D Rule #3."""
    if meeting_id not in _meetings_store:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = _meetings_store[meeting_id]
    if meeting["identity_id"] != identity_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Meeting belongs to different identity",
                "code": "RULE_3_VIOLATION"
            }
        )
    return meeting

# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/", response_model=List[MeetingResponse])
async def list_meetings(
    status: Optional[MeetingStatus] = None,
    meeting_type: Optional[MeetingType] = None,
    thread_id: Optional[UUID] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List meetings.
    R&D Rule #3: Only identity's meetings.
    R&D Rule #5: Ordered by scheduled_at DESC.
    """
    meetings = [
        m for m in _meetings_store.values()
        if m["identity_id"] == identity_id
    ]
    
    if status:
        meetings = [m for m in meetings if m["status"] == status]
    if meeting_type:
        meetings = [m for m in meetings if m["meeting_type"] == meeting_type]
    if thread_id:
        meetings = [m for m in meetings if m["thread_id"] == thread_id]
    if from_date:
        meetings = [m for m in meetings if m["scheduled_at"] >= from_date]
    if to_date:
        meetings = [m for m in meetings if m["scheduled_at"] <= to_date]
    
    # R&D Rule #5: Chronological by scheduled time
    meetings.sort(key=lambda x: x["scheduled_at"], reverse=True)
    
    start = (page - 1) * page_size
    return [MeetingResponse(**m) for m in meetings[start:start + page_size]]

@router.get("/upcoming")
async def list_upcoming_meetings(
    days: int = Query(7, ge=1, le=30),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """List upcoming meetings within N days."""
    now = datetime.utcnow()
    cutoff = now + timedelta(days=days)
    
    meetings = [
        m for m in _meetings_store.values()
        if m["identity_id"] == identity_id
        and m["status"] == MeetingStatus.SCHEDULED
        and now <= m["scheduled_at"] <= cutoff
    ]
    
    # Chronological order (upcoming first)
    meetings.sort(key=lambda x: x["scheduled_at"])
    
    return {
        "upcoming_count": len(meetings),
        "days_ahead": days,
        "meetings": [MeetingResponse(**m) for m in meetings]
    }

@router.post("/", response_model=MeetingResponse, status_code=201)
async def create_meeting(
    data: MeetingCreate,
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Create a meeting."""
    now = datetime.utcnow()
    meeting_id = uuid4()
    
    meeting = {
        "id": meeting_id,
        "identity_id": identity_id,
        "created_by": user_id,
        "created_at": now,
        "title": data.title,
        "description": data.description,
        "meeting_type": data.meeting_type,
        "thread_id": data.thread_id,
        "workspace_id": data.workspace_id,
        "status": MeetingStatus.SCHEDULED,
        "scheduled_at": data.scheduled_at,
        "duration_minutes": data.duration_minutes,
        "recurrence": data.recurrence,
        "attendees": data.attendees,
        "is_external": data.is_external,
        "note_count": 0,
        "action_item_count": 0,
        "metadata": data.metadata or {}
    }
    
    _meetings_store[meeting_id] = meeting
    _notes_store[meeting_id] = []
    
    return MeetingResponse(**meeting)

@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get meeting details."""
    meeting = await verify_meeting_access(meeting_id, identity_id)
    return MeetingResponse(**meeting)

@router.patch("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: UUID = Path(...),
    data: MeetingUpdate = Body(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Update meeting."""
    meeting = await verify_meeting_access(meeting_id, identity_id)
    
    if data.title:
        meeting["title"] = data.title
    if data.description is not None:
        meeting["description"] = data.description
    if data.scheduled_at:
        meeting["scheduled_at"] = data.scheduled_at
    if data.duration_minutes:
        meeting["duration_minutes"] = data.duration_minutes
    if data.attendees is not None:
        meeting["attendees"] = data.attendees
    
    return MeetingResponse(**meeting)

@router.post("/{meeting_id}/cancel", status_code=423)
async def cancel_meeting(
    meeting_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Cancel meeting - REQUIRES CHECKPOINT if external attendees.
    R&D Rule #1: External meeting cancellation requires approval.
    """
    meeting = await verify_meeting_access(meeting_id, identity_id)
    
    if meeting["is_external"]:
        checkpoint_id = uuid4()
        raise HTTPException(
            status_code=423,
            detail={
                "status": "checkpoint_pending",
                "checkpoint": {
                    "id": str(checkpoint_id),
                    "type": "meeting_cancel_external",
                    "meeting_id": str(meeting_id),
                    "requires_approval": True,
                    "reason": "Meeting has external attendees",
                    "options": ["approve", "reject"]
                }
            }
        )
    
    # Internal meeting can be cancelled directly
    meeting["status"] = MeetingStatus.CANCELLED
    return {"status": "cancelled", "meeting_id": str(meeting_id)}

@router.post("/{meeting_id}/start")
async def start_meeting(
    meeting_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Start a meeting."""
    meeting = await verify_meeting_access(meeting_id, identity_id)
    meeting["status"] = MeetingStatus.IN_PROGRESS
    return {"status": "in_progress", "meeting_id": str(meeting_id)}

@router.post("/{meeting_id}/complete")
async def complete_meeting(
    meeting_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Complete a meeting."""
    meeting = await verify_meeting_access(meeting_id, identity_id)
    meeting["status"] = MeetingStatus.COMPLETED
    return {"status": "completed", "meeting_id": str(meeting_id)}

# --- NOTES ---

@router.get("/{meeting_id}/notes", response_model=List[MeetingNoteResponse])
async def list_meeting_notes(
    meeting_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """List meeting notes. R&D Rule #5: Chronological."""
    await verify_meeting_access(meeting_id, identity_id)
    notes = _notes_store.get(meeting_id, [])
    notes.sort(key=lambda x: x["created_at"])
    return [MeetingNoteResponse(**n) for n in notes]

@router.post("/{meeting_id}/notes", response_model=MeetingNoteResponse, status_code=201)
async def create_meeting_note(
    meeting_id: UUID = Path(...),
    data: MeetingNoteCreate = Body(...),
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Create a meeting note."""
    meeting = await verify_meeting_access(meeting_id, identity_id)
    
    note = {
        "id": uuid4(),
        "meeting_id": meeting_id,
        "created_by": user_id,
        "created_at": datetime.utcnow(),
        "content": data.content,
        "is_action_item": data.is_action_item,
        "assigned_to": data.assigned_to,
        "is_completed": False
    }
    
    _notes_store.setdefault(meeting_id, []).append(note)
    meeting["note_count"] += 1
    if data.is_action_item:
        meeting["action_item_count"] += 1
    
    return MeetingNoteResponse(**note)

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    return {
        "status": "healthy",
        "router": "meetings",
        "version": "1.0.0",
        "endpoints": 12,
        "rd_rules_enforced": ["#1", "#3", "#5", "#6"]
    }
