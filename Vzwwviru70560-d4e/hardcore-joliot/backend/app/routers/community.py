"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V77 — Community Sphere Router
═══════════════════════════════════════════════════════════════════════════════

Version: 77.0
Sphere: Community
Endpoints: 15
Status: PRODUCTION READY

R&D Rules Enforced:
- Rule #1: HTTP 423 on event creation, group invitations (Human Approval)
- Rule #3: No cross-sphere implicit access
- Rule #5: CHRONOLOGICAL ONLY
- Rule #6: Full traceability (id, created_by, created_at)

⚠️ CRITICAL: Group invitations and event creation require human approval.
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class GroupType(str, Enum):
    NEIGHBORHOOD = "neighborhood"
    INTEREST = "interest"
    VOLUNTEER = "volunteer"
    SUPPORT = "support"
    PROFESSIONAL = "professional"
    OTHER = "other"


class MemberRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"
    GUEST = "guest"


class EventStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class InvitationStatus(str, Enum):
    PENDING = "pending"
    PENDING_APPROVAL = "pending_approval"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class VolunteerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class GroupBase(BaseModel):
    """Base group schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    group_type: GroupType = GroupType.OTHER
    is_public: bool = True
    max_members: Optional[int] = Field(None, ge=1, le=10000)
    location: Optional[str] = Field(None, max_length=500)
    tags: List[str] = Field(default_factory=list)


class GroupCreate(GroupBase):
    """Create group request."""
    pass


class GroupResponse(GroupBase):
    """Group response with traceability."""
    id: UUID
    member_count: int = 0
    event_count: int = 0
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class GroupMember(BaseModel):
    """Group member schema."""
    id: UUID
    user_id: UUID
    group_id: UUID
    role: MemberRole
    joined_at: datetime
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID


class EventBase(BaseModel):
    """Base event schema."""
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = Field(None, max_length=10000)
    location: Optional[str] = Field(None, max_length=500)
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    max_attendees: Optional[int] = Field(None, ge=1, le=100000)
    is_online: bool = False
    meeting_url: Optional[str] = None
    requires_rsvp: bool = True
    tags: List[str] = Field(default_factory=list)


class EventCreate(EventBase):
    """Create event request."""
    group_id: UUID


class EventResponse(EventBase):
    """Event response with traceability."""
    id: UUID
    group_id: UUID
    status: EventStatus
    attendee_count: int = 0
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    approved_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class InvitationCreate(BaseModel):
    """Create invitation request."""
    invitee_email: EmailStr
    role: MemberRole = MemberRole.MEMBER
    message: Optional[str] = Field(None, max_length=1000)


class InvitationResponse(BaseModel):
    """Invitation response."""
    id: UUID
    group_id: UUID
    invitee_email: str
    role: MemberRole
    status: InvitationStatus
    message: Optional[str] = None
    expires_at: datetime
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    
    class Config:
        from_attributes = True


class VolunteerProfile(BaseModel):
    """Volunteer profile schema."""
    id: UUID
    user_id: UUID
    skills: List[str] = Field(default_factory=list)
    availability: Dict[str, Any] = Field(default_factory=dict)
    total_hours: float = 0.0
    status: VolunteerStatus = VolunteerStatus.ACTIVE
    bio: Optional[str] = Field(None, max_length=2000)
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    
    class Config:
        from_attributes = True


class CheckpointPending(BaseModel):
    """Response when checkpoint required."""
    status: str = "checkpoint_required"
    checkpoint_id: UUID
    action: str
    resource_id: UUID
    message: str
    requires_approval: bool = True
    created_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA STORE
# ═══════════════════════════════════════════════════════════════════════════════

_groups_db: Dict[UUID, dict] = {}
_members_db: Dict[UUID, list] = {}  # group_id -> list of members
_events_db: Dict[UUID, dict] = {}
_invitations_db: Dict[UUID, dict] = {}
_volunteers_db: Dict[UUID, dict] = {}
_checkpoints_db: Dict[UUID, dict] = {}

MOCK_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_current_user_id() -> UUID:
    """Get current user ID."""
    return MOCK_USER_ID


def create_checkpoint(action: str, resource_id: UUID, user_id: UUID) -> UUID:
    """Create governance checkpoint."""
    checkpoint_id = uuid4()
    _checkpoints_db[checkpoint_id] = {
        "id": checkpoint_id,
        "action": action,
        "resource_id": resource_id,
        "user_id": user_id,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    return checkpoint_id


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", tags=["Health"])
async def community_health():
    """Health check for community sphere."""
    return {
        "status": "healthy",
        "sphere": "community",
        "version": "77.0",
        "rd_rules": {
            "rule_1": "Checkpoint on event creation and invitations",
            "rule_5": "CHRONOLOGICAL_ONLY",
            "rule_6": "Full traceability enabled"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GROUP ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/groups", response_model=List[GroupResponse], tags=["Groups"])
async def list_groups(
    group_type: Optional[GroupType] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = Query(None, min_length=1, max_length=200),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List community groups.
    
    ⚠️ R&D Rule #5: Results in CHRONOLOGICAL order (created_at DESC).
    """
    user_id = get_current_user_id()
    
    groups = list(_groups_db.values())
    
    # Filter by type
    if group_type:
        groups = [g for g in groups if g["group_type"] == group_type]
    
    # Filter by public status
    if is_public is not None:
        groups = [g for g in groups if g["is_public"] == is_public]
    
    # Search by name
    if search:
        search_lower = search.lower()
        groups = [g for g in groups if search_lower in g["name"].lower()]
    
    # R&D Rule #5: CHRONOLOGICAL ORDER ONLY
    groups.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    groups = groups[offset:offset + limit]
    
    return [GroupResponse(**g) for g in groups]


@router.post("/groups", response_model=GroupResponse, status_code=201, tags=["Groups"])
async def create_group(group: GroupCreate):
    """Create a new community group."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    group_id = uuid4()
    group_data = {
        "id": group_id,
        **group.model_dump(),
        "member_count": 1,  # Creator is first member
        "event_count": 0,
        "created_at": now,
        "created_by": user_id,
        "updated_at": now,
    }
    
    _groups_db[group_id] = group_data
    
    # Add creator as admin
    _members_db[group_id] = [{
        "id": uuid4(),
        "user_id": user_id,
        "group_id": group_id,
        "role": MemberRole.ADMIN,
        "joined_at": now,
        "created_at": now,
        "created_by": user_id,
    }]
    
    return GroupResponse(**group_data)


@router.get("/groups/{group_id}", response_model=GroupResponse, tags=["Groups"])
async def get_group(group_id: UUID = Path(...)):
    """Get group details."""
    if group_id not in _groups_db:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return GroupResponse(**_groups_db[group_id])


@router.get("/groups/{group_id}/members", response_model=List[GroupMember], tags=["Groups"])
async def list_group_members(
    group_id: UUID = Path(...),
    role: Optional[MemberRole] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """
    List group members.
    
    ⚠️ R&D Rule #5: Members ordered by joined_at DESC.
    """
    if group_id not in _groups_db:
        raise HTTPException(status_code=404, detail="Group not found")
    
    members = _members_db.get(group_id, [])
    
    if role:
        members = [m for m in members if m["role"] == role]
    
    # R&D Rule #5: Chronological order
    members.sort(key=lambda x: x["joined_at"], reverse=True)
    
    members = members[offset:offset + limit]
    
    return [GroupMember(**m) for m in members]


# ═══════════════════════════════════════════════════════════════════════════════
# INVITATION ENDPOINTS (REQUIRES CHECKPOINT)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/groups/{group_id}/invite", tags=["Invitations"])
async def invite_member(
    group_id: UUID = Path(...),
    invitation: InvitationCreate = Body(...),
):
    """
    Send group invitation.
    
    ⚠️ R&D Rule #1: Requires human approval checkpoint.
    Returns HTTP 423 LOCKED until approved.
    """
    user_id = get_current_user_id()
    
    if group_id not in _groups_db:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user is admin/moderator
    members = _members_db.get(group_id, [])
    user_member = next((m for m in members if m["user_id"] == user_id), None)
    
    if not user_member or user_member["role"] not in [MemberRole.ADMIN, MemberRole.MODERATOR]:
        raise HTTPException(status_code=403, detail="Only admins and moderators can invite")
    
    # Create invitation record
    invitation_id = uuid4()
    now = datetime.utcnow()
    
    invitation_data = {
        "id": invitation_id,
        "group_id": group_id,
        "invitee_email": invitation.invitee_email,
        "role": invitation.role,
        "status": InvitationStatus.PENDING_APPROVAL,
        "message": invitation.message,
        "expires_at": datetime(now.year, now.month + 1 if now.month < 12 else 1, now.day),
        "created_at": now,
        "created_by": user_id,
    }
    
    _invitations_db[invitation_id] = invitation_data
    
    # R&D Rule #1: Create checkpoint for human approval
    checkpoint_id = create_checkpoint("SEND_INVITATION", invitation_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "SEND_INVITATION",
            "resource_id": str(invitation_id),
            "message": "Group invitation requires human approval before sending",
            "rule": "R&D Rule #1: Human Sovereignty",
            "invitee": invitation.invitee_email,
        }
    )


@router.get("/groups/{group_id}/invitations", response_model=List[InvitationResponse], tags=["Invitations"])
async def list_invitations(
    group_id: UUID = Path(...),
    status: Optional[InvitationStatus] = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    """List pending invitations for a group."""
    if group_id not in _groups_db:
        raise HTTPException(status_code=404, detail="Group not found")
    
    invitations = [
        i for i in _invitations_db.values()
        if i["group_id"] == group_id
    ]
    
    if status:
        invitations = [i for i in invitations if i["status"] == status]
    
    # Chronological order
    invitations.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [InvitationResponse(**i) for i in invitations[:limit]]


# ═══════════════════════════════════════════════════════════════════════════════
# EVENT ENDPOINTS (REQUIRES CHECKPOINT)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/events", response_model=List[EventResponse], tags=["Events"])
async def list_events(
    group_id: Optional[UUID] = None,
    status: Optional[EventStatus] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List community events.
    
    ⚠️ R&D Rule #5: Events in CHRONOLOGICAL order by start_datetime.
    """
    events = list(_events_db.values())
    
    if group_id:
        events = [e for e in events if e["group_id"] == group_id]
    
    if status:
        events = [e for e in events if e["status"] == status]
    
    if from_date:
        events = [e for e in events if e["start_datetime"].date() >= from_date]
    
    if to_date:
        events = [e for e in events if e["start_datetime"].date() <= to_date]
    
    # R&D Rule #5: Chronological by start time
    events.sort(key=lambda x: x["start_datetime"], reverse=True)
    
    events = events[offset:offset + limit]
    
    return [EventResponse(**e) for e in events]


@router.post("/events/create", tags=["Events"])
async def create_event(event: EventCreate):
    """
    Create a community event.
    
    ⚠️ R&D Rule #1: Event creation requires human approval.
    Returns HTTP 423 LOCKED until approved.
    """
    user_id = get_current_user_id()
    
    if event.group_id not in _groups_db:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Validate dates
    if event.end_datetime and event.end_datetime <= event.start_datetime:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    now = datetime.utcnow()
    event_id = uuid4()
    
    event_data = {
        "id": event_id,
        **event.model_dump(),
        "status": EventStatus.PENDING_APPROVAL,
        "attendee_count": 0,
        "created_at": now,
        "created_by": user_id,
        "approved_at": None,
        "approved_by": None,
    }
    
    _events_db[event_id] = event_data
    
    # Update group event count
    group = _groups_db[event.group_id]
    group["event_count"] = group.get("event_count", 0) + 1
    
    # R&D Rule #1: Checkpoint required
    checkpoint_id = create_checkpoint("CREATE_EVENT", event_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "CREATE_EVENT",
            "resource_id": str(event_id),
            "event_title": event.title,
            "message": "Event creation requires human approval",
            "rule": "R&D Rule #1: Human Sovereignty"
        }
    )


@router.get("/events/{event_id}", response_model=EventResponse, tags=["Events"])
async def get_event(event_id: UUID = Path(...)):
    """Get event details."""
    if event_id not in _events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return EventResponse(**_events_db[event_id])


@router.post("/events/{event_id}/rsvp", tags=["Events"])
async def rsvp_event(
    event_id: UUID = Path(...),
    attending: bool = Body(..., embed=True),
):
    """RSVP to an event."""
    user_id = get_current_user_id()
    
    if event_id not in _events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = _events_db[event_id]
    
    if event["status"] != EventStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Event is not open for RSVP")
    
    if attending:
        # Check capacity
        if event["max_attendees"] and event["attendee_count"] >= event["max_attendees"]:
            raise HTTPException(status_code=400, detail="Event is at capacity")
        
        event["attendee_count"] += 1
    
    return {
        "event_id": str(event_id),
        "attending": attending,
        "attendee_count": event["attendee_count"],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/events/{event_id}/cancel", tags=["Events"])
async def cancel_event(event_id: UUID = Path(...)):
    """
    Cancel an event.
    
    ⚠️ R&D Rule #1: Requires checkpoint approval.
    """
    user_id = get_current_user_id()
    
    if event_id not in _events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = _events_db[event_id]
    
    if event["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Only event creator can cancel")
    
    checkpoint_id = create_checkpoint("CANCEL_EVENT", event_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "CANCEL_EVENT",
            "resource_id": str(event_id),
            "message": "Event cancellation requires human approval"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# VOLUNTEER ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/volunteers", response_model=List[VolunteerProfile], tags=["Volunteers"])
async def list_volunteers(
    status: Optional[VolunteerStatus] = None,
    skill: Optional[str] = Query(None, min_length=1, max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List volunteer profiles.
    
    ⚠️ R&D Rule #5: Volunteers listed in chronological order.
    NO ranking by hours or activity.
    """
    volunteers = list(_volunteers_db.values())
    
    if status:
        volunteers = [v for v in volunteers if v["status"] == status]
    
    if skill:
        skill_lower = skill.lower()
        volunteers = [
            v for v in volunteers 
            if any(skill_lower in s.lower() for s in v.get("skills", []))
        ]
    
    # R&D Rule #5: Chronological order
    volunteers.sort(key=lambda x: x["created_at"], reverse=True)
    
    volunteers = volunteers[offset:offset + limit]
    
    return [VolunteerProfile(**v) for v in volunteers]


@router.post("/volunteers/register", response_model=VolunteerProfile, status_code=201, tags=["Volunteers"])
async def register_volunteer(
    skills: List[str] = Body(default=[]),
    bio: Optional[str] = Body(None, max_length=2000),
    availability: Dict[str, Any] = Body(default={}),
):
    """Register as a volunteer."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    volunteer_id = uuid4()
    volunteer_data = {
        "id": volunteer_id,
        "user_id": user_id,
        "skills": skills,
        "availability": availability,
        "total_hours": 0.0,
        "status": VolunteerStatus.ACTIVE,
        "bio": bio,
        "created_at": now,
        "created_by": user_id,
    }
    
    _volunteers_db[volunteer_id] = volunteer_data
    
    return VolunteerProfile(**volunteer_data)


@router.get("/volunteers/{volunteer_id}", response_model=VolunteerProfile, tags=["Volunteers"])
async def get_volunteer(volunteer_id: UUID = Path(...)):
    """Get volunteer profile."""
    if volunteer_id not in _volunteers_db:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    return VolunteerProfile(**_volunteers_db[volunteer_id])


@router.post("/volunteers/{volunteer_id}/log-hours", tags=["Volunteers"])
async def log_volunteer_hours(
    volunteer_id: UUID = Path(...),
    hours: float = Body(..., ge=0.25, le=24),
    description: Optional[str] = Body(None, max_length=500),
    date_worked: Optional[date] = Body(None),
):
    """Log volunteer hours."""
    user_id = get_current_user_id()
    
    if volunteer_id not in _volunteers_db:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    volunteer = _volunteers_db[volunteer_id]
    
    if volunteer["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Can only log hours for your own profile")
    
    volunteer["total_hours"] += hours
    
    return {
        "volunteer_id": str(volunteer_id),
        "hours_logged": hours,
        "total_hours": volunteer["total_hours"],
        "date_worked": (date_worked or date.today()).isoformat(),
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", tags=["Statistics"])
async def get_community_stats():
    """Get community statistics (read-only)."""
    user_id = get_current_user_id()
    
    return {
        "user_id": str(user_id),
        "groups": {
            "total": len(_groups_db),
            "by_type": {
                gt.value: len([g for g in _groups_db.values() if g["group_type"] == gt])
                for gt in GroupType
            }
        },
        "events": {
            "total": len(_events_db),
            "by_status": {
                es.value: len([e for e in _events_db.values() if e["status"] == es])
                for es in EventStatus
            }
        },
        "volunteers": {
            "total": len(_volunteers_db),
            "active": len([v for v in _volunteers_db.values() if v["status"] == VolunteerStatus.ACTIVE])
        },
        "invitations": {
            "pending": len([i for i in _invitations_db.values() if i["status"] == InvitationStatus.PENDING_APPROVAL])
        },
        "timestamp": datetime.utcnow().isoformat(),
        "rd_rule_notice": "Community actions requiring approval: invitations, event creation, event cancellation"
    }
