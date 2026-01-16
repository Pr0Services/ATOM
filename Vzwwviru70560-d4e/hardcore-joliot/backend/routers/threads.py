"""
CHE·NU™ V75 Backend - Threads Router

RÈGLE: Thread = APPEND-ONLY
- founding_intent est IMMUTABLE
- Events ne peuvent qu'être ajoutés

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

from config import get_db
from schemas.base import BaseResponse, PaginatedResponse, PaginationMeta, ThreadStatus
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ThreadEvent(BaseModel):
    """Thread event (APPEND-ONLY)."""
    id: str
    thread_id: str
    event_type: str  # 'message', 'decision', 'agent_action', 'file', 'checkpoint'
    content: str
    actor_id: str
    actor_type: str  # 'user', 'agent', 'system'
    metadata: dict = {}
    created_at: datetime


class Thread(BaseModel):
    """Thread entity."""
    id: str
    title: str
    founding_intent: str  # IMMUTABLE
    sphere_id: str
    bureau_id: Optional[str] = None
    status: ThreadStatus = ThreadStatus.ACTIVE
    participants: List[str] = []
    events_count: int = 0
    last_activity: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class CreateThreadRequest(BaseModel):
    """Create thread request."""
    title: str = Field(min_length=1, max_length=200)
    founding_intent: str = Field(min_length=1, max_length=1000)
    sphere_id: str
    bureau_id: Optional[str] = None
    participants: List[str] = []


class UpdateThreadRequest(BaseModel):
    """Update thread request (limited fields - founding_intent is IMMUTABLE)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[ThreadStatus] = None
    participants: Optional[List[str]] = None


class AddEventRequest(BaseModel):
    """Add event to thread."""
    event_type: str
    content: str
    metadata: dict = {}


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=PaginatedResponse[Thread])
async def list_threads(
    user: dict = Depends(require_auth),
    status: Optional[ThreadStatus] = None,
    sphere_id: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List threads with filtering and pagination."""
    now = datetime.utcnow()
    
    # TODO: Replace with actual database query
    threads = [
        Thread(
            id="thread-1",
            title="Q4 Budget Planning",
            founding_intent="Plan and approve Q4 marketing budget allocation",
            sphere_id="business",
            bureau_id="threads",
            status=ThreadStatus.ACTIVE,
            participants=[user["id"]],
            events_count=15,
            last_activity=now,
            created_at=now,
            updated_at=now,
        ),
        Thread(
            id="thread-2",
            title="Team Onboarding",
            founding_intent="Coordinate new team member onboarding process",
            sphere_id="team",
            bureau_id="threads",
            status=ThreadStatus.ACTIVE,
            participants=[user["id"]],
            events_count=8,
            last_activity=now,
            created_at=now,
            updated_at=now,
        ),
    ]
    
    return PaginatedResponse(
        success=True,
        data=threads,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(threads),
            total_pages=1,
            has_next=False,
            has_prev=False,
        ),
    )


@router.get("/active", response_model=BaseResponse[List[Thread]])
async def get_active_threads(
    user: dict = Depends(require_auth),
    limit: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Get user's active threads."""
    now = datetime.utcnow()
    
    threads = [
        Thread(
            id="thread-1",
            title="Q4 Budget Planning",
            founding_intent="Plan and approve Q4 marketing budget",
            sphere_id="business",
            status=ThreadStatus.ACTIVE,
            events_count=15,
            last_activity=now,
            created_at=now,
            updated_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=threads[:limit])


@router.get("/{thread_id}", response_model=BaseResponse[Thread])
async def get_thread(
    thread_id: str = Path(...),
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get thread by ID."""
    now = datetime.utcnow()
    
    # TODO: Fetch from database
    thread = Thread(
        id=thread_id,
        title="Q4 Budget Planning",
        founding_intent="Plan and approve Q4 marketing budget allocation",
        sphere_id="business",
        bureau_id="threads",
        status=ThreadStatus.ACTIVE,
        participants=[user["id"]],
        events_count=15,
        last_activity=now,
        created_at=now,
        updated_at=now,
    )
    
    return BaseResponse(success=True, data=thread)


@router.post("", response_model=BaseResponse[Thread])
async def create_thread(
    request: CreateThreadRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new thread.
    
    RÈGLE: founding_intent is set at creation and IMMUTABLE.
    """
    now = datetime.utcnow()
    
    thread = Thread(
        id=str(uuid.uuid4()),
        title=request.title,
        founding_intent=request.founding_intent,  # Set once, never changes
        sphere_id=request.sphere_id,
        bureau_id=request.bureau_id,
        status=ThreadStatus.ACTIVE,
        participants=[user["id"]] + request.participants,
        events_count=0,
        last_activity=now,
        created_at=now,
        updated_at=now,
    )
    
    # TODO: Save to database
    
    return BaseResponse(success=True, data=thread)


@router.patch("/{thread_id}", response_model=BaseResponse[Thread])
async def update_thread(
    thread_id: str,
    request: UpdateThreadRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Update thread (limited fields).
    
    RÈGLE: founding_intent is IMMUTABLE and cannot be changed.
    """
    now = datetime.utcnow()
    
    # TODO: Fetch and update in database
    thread = Thread(
        id=thread_id,
        title=request.title or "Updated Thread",
        founding_intent="Original intent (IMMUTABLE)",
        sphere_id="business",
        status=request.status or ThreadStatus.ACTIVE,
        participants=request.participants or [user["id"]],
        events_count=15,
        last_activity=now,
        created_at=now,
        updated_at=now,
    )
    
    return BaseResponse(success=True, data=thread)


@router.post("/{thread_id}/archive")
async def archive_thread(
    thread_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Archive a thread (requires governance check)."""
    # TODO: Implement with governance check
    
    return BaseResponse(
        success=True,
        data={"id": thread_id, "status": "archived"},
    )


@router.get("/{thread_id}/events", response_model=PaginatedResponse[ThreadEvent])
async def get_thread_events(
    thread_id: str,
    user: dict = Depends(require_auth),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Get thread events (APPEND-ONLY history).
    
    Events are returned in chronological order.
    """
    now = datetime.utcnow()
    
    events = [
        ThreadEvent(
            id="event-1",
            thread_id=thread_id,
            event_type="message",
            content="Thread started",
            actor_id=user["id"],
            actor_type="user",
            created_at=now,
        ),
        ThreadEvent(
            id="event-2",
            thread_id=thread_id,
            event_type="agent_action",
            content="Agent completed research task",
            actor_id="agent-1",
            actor_type="agent",
            metadata={"agent_name": "Research Assistant"},
            created_at=now,
        ),
    ]
    
    return PaginatedResponse(
        success=True,
        data=events,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(events),
            total_pages=1,
            has_next=False,
            has_prev=False,
        ),
    )


@router.post("/{thread_id}/events", response_model=BaseResponse[ThreadEvent])
async def add_thread_event(
    thread_id: str,
    request: AddEventRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Add event to thread (APPEND-ONLY).
    
    Events can only be added, never modified or deleted.
    """
    now = datetime.utcnow()
    
    event = ThreadEvent(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        event_type=request.event_type,
        content=request.content,
        actor_id=user["id"],
        actor_type="user",
        metadata=request.metadata,
        created_at=now,
    )
    
    # TODO: Save to database
    
    return BaseResponse(success=True, data=event)
