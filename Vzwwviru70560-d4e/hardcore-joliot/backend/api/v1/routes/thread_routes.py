"""
CHE·NU™ Thread Routes

Thread endpoints implementing APPEND-ONLY architecture:
- GET /threads - List threads
- POST /threads - Create thread
- GET /threads/{id} - Get thread
- POST /threads/{id}/archive - Archive thread
- GET /threads/{id}/events - List events
- POST /threads/{id}/events - Append event (IMMUTABLE)
- POST /threads/{id}/intent - Refine intent
- GET /threads/{id}/decisions - List decisions
- POST /threads/{id}/decisions - Record decision
- GET /threads/{id}/actions - List actions
- POST /threads/{id}/actions - Create action
- POST /threads/{id}/actions/{action_id}/complete - Complete action
- GET /threads/{id}/snapshot - Get snapshot
- POST /threads/{id}/snapshot - Create snapshot

⚠️ CRITICAL: No PUT/DELETE on events - APPEND-ONLY!
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import (
    ThreadNotFoundError,
    IdentityBoundaryError,
    ValidationError,
    CheckpointRequiredError,
)
from backend.api.dependencies import get_current_user, CurrentUser
from backend.services.thread.thread_service import ThreadService, get_thread_service
from backend.models.thread import ThreadStatus, ActionStatus
from backend.schemas.thread_schemas import (
    ThreadStatusEnum,
    ActionStatusEnum,
    ThreadCreate,
    ThreadResponse,
    ThreadSummary,
    ThreadUpdate,
    ThreadListResponse,
    EventCreate,
    EventResponse,
    EventListResponse,
    DecisionCreate,
    DecisionResponse,
    DecisionListResponse,
    ActionCreate,
    ActionResponse,
    ActionListResponse,
    SnapshotCreate,
    SnapshotResponse,
    IntentRefinement,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD LIST & CREATE
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/",
    response_model=ThreadListResponse,
    summary="List threads",
    description="""
    List threads for the current user with optional filters.
    
    **Identity Boundary:** Only returns threads belonging to the authenticated user.
    """,
)
async def list_threads(
    sphere_id: Optional[str] = None,
    status: Optional[ThreadStatusEnum] = None,
    search: Optional[str] = Query(None, max_length=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadListResponse:
    """List threads with filters."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    thread_status = ThreadStatus(status.value) if status else None
    
    threads, total = await service.list_threads(
        sphere_id=sphere_id,
        status=thread_status,
        search=search,
        page=page,
        page_size=page_size,
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return ThreadListResponse(
        threads=threads,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post(
    "/",
    response_model=ThreadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create thread",
    description="""
    Create a new thread with founding intent.
    
    **CRITICAL:** The `founding_intent` is IMMUTABLE - it cannot be changed after creation.
    This is the thread's permanent foundation.
    
    Creates `thread.created` and `intent.declared` events.
    """,
)
async def create_thread(
    request: ThreadCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadResponse:
    """Create a new thread."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.create_thread(request)
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD DETAILS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{thread_id}",
    response_model=ThreadResponse,
    summary="Get thread",
    description="""
    Get full thread details.
    
    **Identity Boundary:** Returns HTTP 403 if thread belongs to different identity.
    """,
)
async def get_thread(
    thread_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadResponse:
    """Get thread details."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.get_thread(thread_id)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.patch(
    "/{thread_id}",
    response_model=ThreadResponse,
    summary="Update thread",
    description="""
    Update thread metadata.
    
    **NOTE:** `founding_intent` CANNOT be changed! Use `/intent` to refine.
    
    Creates `thread.updated` event.
    """,
)
async def update_thread(
    thread_id: str,
    request: ThreadUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadResponse:
    """Update thread metadata."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.update_thread(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/archive",
    response_model=ThreadResponse,
    summary="Archive thread",
    description="""
    Archive a thread (soft delete).
    
    Creates `thread.archived` event.
    """,
)
async def archive_thread(
    thread_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadResponse:
    """Archive thread."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.archive_thread(thread_id)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# EVENTS (APPEND-ONLY - THE CORE!)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{thread_id}/events",
    response_model=EventListResponse,
    summary="List events",
    description="""
    Get events for a thread in causal order.
    
    Events are the IMMUTABLE building blocks of threads.
    They are NEVER modified or deleted.
    """,
)
async def list_events(
    thread_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> EventListResponse:
    """List thread events."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        events, total, has_more = await service.get_events(
            thread_id,
            page=page,
            page_size=page_size,
        )
        
        return EventListResponse(
            events=events,
            total=total,
            has_more=has_more,
        )
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Append event",
    description="""
    Append a new IMMUTABLE event to the thread.
    
    **CRITICAL RULES:**
    - Events are NEVER modified after creation
    - Events are NEVER deleted
    - Corrections are made by appending NEW events
    
    **May return HTTP 423** if the event requires governance approval.
    """,
)
async def append_event(
    thread_id: str,
    request: EventCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> EventResponse:
    """Append event to thread."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.append_event(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )
    except CheckpointRequiredError as e:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=e.to_dict(),
            headers={"X-Checkpoint-ID": e.checkpoint_id},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# INTENT REFINEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/{thread_id}/intent",
    response_model=ThreadResponse,
    summary="Refine intent",
    description="""
    Refine the thread's current intent.
    
    **NOTE:** The `founding_intent` remains unchanged!
    This updates `current_intent` for display purposes.
    
    Creates `intent.refined` event.
    """,
)
async def refine_intent(
    thread_id: str,
    request: IntentRefinement,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ThreadResponse:
    """Refine thread intent."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.refine_intent(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DECISIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{thread_id}/decisions",
    response_model=DecisionListResponse,
    summary="List decisions",
    description="Get all decisions recorded in a thread.",
)
async def list_decisions(
    thread_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DecisionListResponse:
    """List thread decisions."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        decisions = await service.get_decisions(thread_id)
        return DecisionListResponse(
            decisions=decisions,
            total=len(decisions),
        )
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/decisions",
    response_model=DecisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record decision",
    description="""
    Record a decision in the thread.
    
    Creates `decision.recorded` event.
    """,
)
async def record_decision(
    thread_id: str,
    request: DecisionCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DecisionResponse:
    """Record a decision."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.record_decision(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{thread_id}/actions",
    response_model=ActionListResponse,
    summary="List actions",
    description="Get actions in a thread with optional status filter.",
)
async def list_actions(
    thread_id: str,
    status: Optional[ActionStatusEnum] = None,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ActionListResponse:
    """List thread actions."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        action_status = ActionStatus(status.value) if status else None
        actions, pending_count = await service.get_actions(thread_id, action_status)
        
        return ActionListResponse(
            actions=actions,
            total=len(actions),
            pending_count=pending_count,
        )
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/actions",
    response_model=ActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create action",
    description="""
    Create an action item in the thread.
    
    Creates `action.created` event.
    """,
)
async def create_action(
    thread_id: str,
    request: ActionCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ActionResponse:
    """Create an action."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.create_action(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/actions/{action_id}/complete",
    response_model=ActionResponse,
    summary="Complete action",
    description="""
    Mark an action as completed.
    
    Creates `action.completed` event.
    """,
)
async def complete_action(
    thread_id: str,
    action_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ActionResponse:
    """Complete an action."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.complete_action(thread_id, action_id)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SNAPSHOTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{thread_id}/snapshot",
    response_model=SnapshotResponse,
    summary="Get snapshot",
    description="""
    Get current thread state snapshot.
    
    Returns the latest computed state derived from the event log.
    """,
)
async def get_snapshot(
    thread_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SnapshotResponse:
    """Get thread snapshot."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.get_snapshot(thread_id)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/{thread_id}/snapshot",
    response_model=SnapshotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create snapshot",
    description="""
    Create a manual snapshot for memory compression.
    
    Creates `summary.snapshot` event.
    """,
)
async def create_snapshot(
    thread_id: str,
    request: SnapshotCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SnapshotResponse:
    """Create thread snapshot."""
    service = get_thread_service(db, current_user.identity_id, current_user.id)
    
    try:
        return await service.create_snapshot(thread_id, request)
    except ThreadNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )
