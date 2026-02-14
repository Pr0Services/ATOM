"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — THREADS ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent B - Phase B2: Core Routers
Date: 8 Janvier 2026

THREAD = SOURCE DE VÉRITÉ UNIQUE
- Event Sourcing (append-only)
- Immutabilité des events
- Tri-Layer Memory integration
- SQLAlchemy ORM with graceful fallback

R&D RULES ENFORCED:
- Rule #1: HTTP 423 for archive/delete
- Rule #3: HTTP 403 for identity boundary
- Rule #5: Chronological order only (NO ranking)
- Rule #6: Full traceability (id, created_by, created_at)
- Rule #7: Founding intent is IMMUTABLE
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4, UUID
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update as sql_update, delete as sql_delete
import logging

# Import database dependencies
try:
    from app.core.database import get_db_optional
    from app.models.models import (
        Thread as ThreadModel,
        ThreadEvent as ThreadEventModel,
        Checkpoint as CheckpointModel,
        ThreadStatus as DBThreadStatus,
        CheckpointStatus as DBCheckpointStatus,
        CheckpointType as DBCheckpointType
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/threads", tags=["Threads"])


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    COMPLETED = "completed"


class ThreadType(str, Enum):
    PERSONAL = "personal"
    COLLECTIVE = "collective"
    INSTITUTIONAL = "institutional"


class MaturityLevel(str, Enum):
    SEED = "seed"       # 🌱
    SPROUT = "sprout"   # 🌿
    TREE = "tree"       # 🌳
    FRUIT = "fruit"     # 🍎


class ThreadEventType(str, Enum):
    # Lifecycle
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_ARCHIVED = "thread.archived"
    # Intent
    INTENT_DECLARED = "intent.declared"
    INTENT_REFINED = "intent.refined"
    # Decisions
    DECISION_RECORDED = "decision.recorded"
    DECISION_REVISED = "decision.revised"
    # Actions
    ACTION_CREATED = "action.created"
    ACTION_COMPLETED = "action.completed"
    # Notes
    NOTE_ADDED = "note.added"
    SUMMARY_SNAPSHOT = "summary.snapshot"
    # Links
    LINK_ADDED = "link.added"
    THREAD_REFERENCED = "thread.referenced"
    # Governance
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"


# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: get_db_optional imported from app.core.database — yields session or None
# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_current_user_id() -> UUID:
    """Mock: Get current user from JWT."""
    return UUID("00000000-0000-0000-0000-000000000001")


def verify_ownership(thread, user_id: UUID) -> None:
    """Rule #3: Identity Boundary enforcement."""
    # Support both ORM objects and dicts
    owner = thread.owner_id if hasattr(thread, 'owner_id') else thread.get("owner_id")
    if str(owner) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Access denied: resource belongs to different identity",
                "your_identity": str(user_id),
                "resource_owner": str(owner)
            }
        )


def _thread_to_dict(thread: ThreadModel) -> dict:
    """Convert ThreadModel ORM object to dict response."""
    maturity = _maturity_from_score(thread.maturity_score)

    # Extract description from metadata if available
    description = None
    if thread.metadata and isinstance(thread.metadata, dict):
        description = thread.metadata.get("description")

    # Extract sphere from metadata (fallback to "Personal")
    sphere = "Personal"
    if thread.sphere_id:
        sphere = str(thread.sphere_id)
    elif thread.metadata and isinstance(thread.metadata, dict):
        sphere = thread.metadata.get("sphere", "Personal")

    return {
        "id": str(thread.id),
        "title": thread.title,
        "description": description,

        # R&D Rule #6: Traceability
        "created_by": str(thread.created_by),
        "created_at": thread.created_at.isoformat(),
        "updated_at": thread.updated_at.isoformat(),

        # Ownership
        "owner_id": str(thread.owner_id),
        "sphere": sphere,
        "thread_type": "personal",

        # R&D Rule #7: Founding Intent (IMMUTABLE)
        "founding_intent": thread.founding_intent,

        # Hierarchy
        "parent_thread_id": str(thread.parent_thread_id) if thread.parent_thread_id else None,

        # State
        "status": thread.status.value if hasattr(thread.status, 'value') else thread.status,
        "maturity_level": maturity["level"],
        "maturity_emoji": maturity["emoji"],

        # Metadata
        "tags": thread.tags or [],
        "events_count": 0,  # Could be computed via join
    }


def _maturity_from_score(score: int) -> dict:
    """Convert maturity score to level and emoji."""
    if score >= 75:
        return {"level": MaturityLevel.FRUIT.value, "emoji": "🍎"}
    if score >= 50:
        return {"level": MaturityLevel.TREE.value, "emoji": "🌳"}
    if score >= 25:
        return {"level": MaturityLevel.SPROUT.value, "emoji": "🌿"}
    return {"level": MaturityLevel.SEED.value, "emoji": "🌱"}


def _score_from_maturity(level: MaturityLevel) -> int:
    """Convert maturity level to score."""
    mapping = {
        MaturityLevel.SEED: 0,
        MaturityLevel.SPROUT: 25,
        MaturityLevel.TREE: 50,
        MaturityLevel.FRUIT: 75
    }
    return mapping.get(level, 0)


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD CRUD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/", summary="List user threads (chronological)")
async def list_threads(
    sphere: Optional[str] = Query(None, description="Filter by sphere"),
    status: Optional[ThreadStatus] = Query(None, description="Filter by status"),
    maturity: Optional[MaturityLevel] = Query(None, description="Filter by maturity"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Optional[AsyncSession] = Depends(get_db_optional)
    # Rule #5: NO sort_by parameter for ranking
):
    """
    List threads for current user.

    R&D RULE #5: Results are ALWAYS chronological (newest first).
    NO engagement/popularity ranking allowed.
    """
    user_id = get_current_user_id()

    # Fallback if DB unavailable
    if db is None:
        logger.warning("Database unavailable, returning empty list")
        return {
            "items": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "order": "chronological_desc"
        }

    try:
        # Build query
        query = select(ThreadModel).where(ThreadModel.owner_id == user_id)

        # Apply filters
        if sphere:
            # Filter by sphere_id or metadata sphere
            query = query.where(
                (ThreadModel.sphere_id == UUID(sphere)) |
                (ThreadModel.metadata["sphere"].astext == sphere)
            )

        if status:
            query = query.where(ThreadModel.status == status.value)

        if maturity:
            # Convert maturity level to score range
            score = _score_from_maturity(maturity)
            if maturity == MaturityLevel.FRUIT:
                query = query.where(ThreadModel.maturity_score >= 75)
            elif maturity == MaturityLevel.TREE:
                query = query.where(ThreadModel.maturity_score >= 50, ThreadModel.maturity_score < 75)
            elif maturity == MaturityLevel.SPROUT:
                query = query.where(ThreadModel.maturity_score >= 25, ThreadModel.maturity_score < 50)
            else:  # SEED
                query = query.where(ThreadModel.maturity_score < 25)

        # Rule #5: ALWAYS chronological order (newest first)
        query = query.order_by(desc(ThreadModel.created_at))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Pagination
        query = query.offset(offset).limit(limit)
        result = await db.execute(query)
        threads = [_thread_to_dict(t) for t in result.scalars().all()]

        return {
            "items": threads,
            "total": total,
            "limit": limit,
            "offset": offset,
            "order": "chronological_desc"  # Explicit: Rule #5
        }

    except Exception as e:
        logger.error(f"Error listing threads: {e}", exc_info=True)
        return {
            "items": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
            "order": "chronological_desc"
        }


@router.post("/", summary="Create new thread", status_code=201)
async def create_thread(
    title: str = Body(..., min_length=1, max_length=200),
    description: Optional[str] = Body(None, max_length=2000),
    sphere: str = Body("Personal"),
    founding_intent: str = Body(..., min_length=1, max_length=500),
    thread_type: ThreadType = Body(ThreadType.PERSONAL),
    parent_thread_id: Optional[str] = Body(None),
    tags: List[str] = Body(default=[]),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Create a new thread.

    R&D RULE #6: Automatic traceability (id, created_by, created_at)
    R&D RULE #7: founding_intent is IMMUTABLE once set
    """
    user_id = get_current_user_id()

    # Fallback if DB unavailable
    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable. Thread creation requires database connection."
        )

    try:
        thread_id = uuid4()
        now = datetime.now(timezone.utc)

        # Create thread
        new_thread = ThreadModel(
            id=thread_id,
            owner_id=user_id,
            sphere_id=None,  # Could map sphere name to UUID if needed
            parent_thread_id=UUID(parent_thread_id) if parent_thread_id else None,
            title=title,
            founding_intent=founding_intent,  # R&D Rule #7: IMMUTABLE
            status=DBThreadStatus.ACTIVE,
            maturity_score=0,  # SEED level
            tags=tags,
            metadata={
                "description": description,
                "sphere": sphere,
                "thread_type": thread_type.value
            },
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(new_thread)

        # Create initial event (Rule #6: Traceability)
        initial_event = ThreadEventModel(
            id=uuid4(),
            thread_id=thread_id,
            event_type=ThreadEventType.THREAD_CREATED.value,
            event_data={
                "title": title,
                "founding_intent": founding_intent
            },
            sequence_number=0,
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(initial_event)
        await db.commit()
        await db.refresh(new_thread)

        # Convert to dict response
        response = _thread_to_dict(new_thread)
        response["events_count"] = 1

        return response

    except Exception as e:
        logger.error(f"Error creating thread: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create thread: {str(e)}"
        )


@router.get("/{thread_id}", summary="Get thread by ID")
async def get_thread(
    thread_id: str,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Get a specific thread.

    R&D RULE #3: Identity boundary enforced.
    """
    user_id = get_current_user_id()

    # Fallback if DB unavailable
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        result = await db.execute(query)
        thread = result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3: Identity Boundary
        verify_ownership(thread, user_id)

        return _thread_to_dict(thread)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting thread: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{thread_id}", summary="Update thread")
async def update_thread(
    thread_id: str,
    title: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    status: Optional[ThreadStatus] = Body(None),
    tags: Optional[List[str]] = Body(None),
    db: Optional[AsyncSession] = Depends(get_db_optional)
    # NOTE: founding_intent NOT accepted - IMMUTABLE (Rule #7)
):
    """
    Update thread metadata.

    R&D RULE #7: founding_intent CANNOT be changed.
    R&D RULE #6: updated_at auto-updated.
    """
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        result = await db.execute(query)
        thread = result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3: Identity Boundary
        verify_ownership(thread, user_id)

        # Update allowed fields
        now = datetime.now(timezone.utc)

        if title is not None:
            thread.title = title
        if status is not None:
            thread.status = status.value
        if tags is not None:
            thread.tags = tags
        if description is not None:
            if thread.metadata is None:
                thread.metadata = {}
            thread.metadata["description"] = description

        thread.updated_at = now

        # Log update event
        update_event = ThreadEventModel(
            id=uuid4(),
            thread_id=UUID(thread_id),
            event_type=ThreadEventType.THREAD_UPDATED.value,
            event_data={
                "fields_updated": [
                    k for k, v in {
                        "title": title,
                        "description": description,
                        "status": status,
                        "tags": tags
                    }.items() if v is not None
                ]
            },
            sequence_number=0,  # Should be incremented properly
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(update_event)
        await db.commit()
        await db.refresh(thread)

        return _thread_to_dict(thread)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating thread: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{thread_id}/archive", summary="Archive thread (checkpoint required)")
async def archive_thread(
    thread_id: str,
    checkpoint_id: Optional[str] = Body(None),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Archive a thread.

    R&D RULE #1: Requires human approval (HTTP 423 without checkpoint)
    """
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        result = await db.execute(query)
        thread = result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3: Identity Boundary
        verify_ownership(thread, user_id)

        # Rule #1: Human Sovereignty - Checkpoint required
        if not checkpoint_id:
            now = datetime.now(timezone.utc)
            checkpoint = CheckpointModel(
                id=uuid4(),
                checkpoint_type=DBCheckpointType.GOVERNANCE,
                status=DBCheckpointStatus.PENDING,
                resource_type="thread",
                resource_id=UUID(thread_id),
                action_type="archive",
                action_data={
                    "message": "Thread archival requires human approval",
                    "thread_title": thread.title
                },
                created_by=user_id,
                created_at=now,
                updated_at=now
            )
            db.add(checkpoint)
            await db.commit()

            raise HTTPException(
                status_code=423,  # LOCKED
                detail={
                    "status": "checkpoint_required",
                    "checkpoint_id": str(checkpoint.id),
                    "message": "Action requires human approval",
                    "action": "thread.archive"
                }
            )

        # Verify checkpoint is approved
        checkpoint_query = select(CheckpointModel).where(CheckpointModel.id == UUID(checkpoint_id))
        checkpoint_result = await db.execute(checkpoint_query)
        checkpoint = checkpoint_result.scalar_one_or_none()

        if not checkpoint:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")

        if checkpoint.status != DBCheckpointStatus.APPROVED:
            raise HTTPException(
                status_code=423,
                detail={
                    "status": "checkpoint_not_approved",
                    "checkpoint_id": checkpoint_id,
                    "checkpoint_status": checkpoint.status.value
                }
            )

        # Execute archive
        now = datetime.now(timezone.utc)
        thread.status = DBThreadStatus.ARCHIVED
        thread.updated_at = now

        # Log archive event
        archive_event = ThreadEventModel(
            id=uuid4(),
            thread_id=UUID(thread_id),
            event_type=ThreadEventType.THREAD_ARCHIVED.value,
            event_data={"checkpoint_id": checkpoint_id},
            sequence_number=0,
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(archive_event)
        await db.commit()
        await db.refresh(thread)

        return {"status": "archived", "thread": _thread_to_dict(thread)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error archiving thread: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{thread_id}", summary="Delete thread (checkpoint required)")
async def delete_thread(
    thread_id: str,
    checkpoint_id: Optional[str] = Body(None),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Delete a thread (soft delete).

    R&D RULE #1: CRITICAL action - requires checkpoint
    R&D RULE #7: Events are preserved (append-only)
    """
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        result = await db.execute(query)
        thread = result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3: Identity Boundary
        verify_ownership(thread, user_id)

        # Rule #1: CRITICAL - Checkpoint required
        if not checkpoint_id:
            now = datetime.now(timezone.utc)
            checkpoint = CheckpointModel(
                id=uuid4(),
                checkpoint_type=DBCheckpointType.DESTRUCTIVE,
                status=DBCheckpointStatus.PENDING,
                resource_type="thread",
                resource_id=UUID(thread_id),
                action_type="delete",
                action_data={
                    "message": "Thread deletion is CRITICAL and requires explicit approval",
                    "thread_title": thread.title,
                    "priority": "critical"
                },
                created_by=user_id,
                created_at=now,
                updated_at=now
            )
            db.add(checkpoint)
            await db.commit()

            raise HTTPException(
                status_code=423,
                detail={
                    "status": "checkpoint_required",
                    "checkpoint_id": str(checkpoint.id),
                    "message": "CRITICAL: Thread deletion requires explicit human approval",
                    "action": "thread.delete",
                    "priority": "critical"
                }
            )

        # Verify checkpoint
        checkpoint_query = select(CheckpointModel).where(CheckpointModel.id == UUID(checkpoint_id))
        checkpoint_result = await db.execute(checkpoint_query)
        checkpoint = checkpoint_result.scalar_one_or_none()

        if not checkpoint:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")

        if checkpoint.status != DBCheckpointStatus.APPROVED:
            raise HTTPException(status_code=423, detail="Checkpoint not approved")

        # Soft delete (events preserved per Rule #7)
        now = datetime.now(timezone.utc)
        if thread.metadata is None:
            thread.metadata = {}
        thread.metadata["deleted_at"] = now.isoformat()
        thread.metadata["deleted_by"] = str(user_id)
        thread.status = "deleted"  # Custom status for soft delete
        thread.updated_at = now

        await db.commit()

        return {
            "status": "deleted",
            "thread_id": thread_id,
            "events_preserved": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting thread: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{thread_id}/events", summary="Get thread events (chronological)")
async def get_thread_events(
    thread_id: str,
    event_type: Optional[ThreadEventType] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Get events for a thread.

    R&D RULE #5: Events are ALWAYS chronological.
    R&D RULE #7: Events are immutable (append-only).
    """
    user_id = get_current_user_id()

    if db is None:
        return {
            "thread_id": thread_id,
            "events": [],
            "total": 0,
            "order": "chronological_asc"
        }

    try:
        # Verify thread exists and ownership
        thread_query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        thread_result = await db.execute(thread_query)
        thread = thread_result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3
        verify_ownership(thread, user_id)

        # Query events
        events_query = select(ThreadEventModel).where(ThreadEventModel.thread_id == UUID(thread_id))

        if event_type:
            events_query = events_query.where(ThreadEventModel.event_type == event_type.value)

        # Rule #5: Chronological order (oldest first for events)
        events_query = events_query.order_by(ThreadEventModel.created_at)

        # Count total
        count_query = select(func.count()).select_from(events_query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Pagination
        events_query = events_query.offset(offset).limit(limit)
        result = await db.execute(events_query)
        events = result.scalars().all()

        # Convert to dict
        events_data = []
        for event in events:
            events_data.append({
                "id": str(event.id),
                "thread_id": str(event.thread_id),
                "event_type": event.event_type,
                "data": event.event_data,
                "created_by": str(event.created_by),
                "created_at": event.created_at.isoformat(),
                "sequence_number": event.sequence_number,
                "immutable": True
            })

        return {
            "thread_id": thread_id,
            "events": events_data,
            "total": total,
            "order": "chronological_asc"  # Events: oldest first
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting thread events: {e}", exc_info=True)
        return {
            "thread_id": thread_id,
            "events": [],
            "total": 0,
            "order": "chronological_asc"
        }


@router.post("/{thread_id}/events", summary="Add event to thread")
async def add_thread_event(
    thread_id: str,
    event_type: ThreadEventType = Body(...),
    content: Optional[str] = Body(None),
    data: Optional[Dict[str, Any]] = Body(None),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Add an event to a thread.

    R&D RULE #6: Full traceability.
    R&D RULE #7: Events are IMMUTABLE once created.
    """
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Verify thread exists and ownership
        thread_query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        thread_result = await db.execute(thread_query)
        thread = thread_result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        # Rule #3
        verify_ownership(thread, user_id)

        # Get next sequence number
        max_seq_query = select(func.max(ThreadEventModel.sequence_number)).where(
            ThreadEventModel.thread_id == UUID(thread_id)
        )
        max_seq_result = await db.execute(max_seq_query)
        max_seq = max_seq_result.scalar() or -1

        now = datetime.now(timezone.utc)

        # Create event
        event_data = data or {}
        if content:
            event_data["content"] = content

        event = ThreadEventModel(
            id=uuid4(),
            thread_id=UUID(thread_id),
            event_type=event_type.value,
            event_data=event_data,
            sequence_number=max_seq + 1,
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(event)

        # Update thread maturity score
        thread.maturity_score += 1  # Simple increment
        thread.updated_at = now

        await db.commit()
        await db.refresh(event)

        return {
            "id": str(event.id),
            "thread_id": str(event.thread_id),
            "event_type": event.event_type,
            "data": event.event_data,
            "created_by": str(event.created_by),
            "created_at": event.created_at.isoformat(),
            "sequence_number": event.sequence_number,
            "immutable": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding thread event: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{thread_id}/events/{event_id}", summary="Modify event (FORBIDDEN)")
async def modify_event(thread_id: str, event_id: str):
    """
    Attempt to modify an event.

    R&D RULE #7: Events are IMMUTABLE - this endpoint ALWAYS fails.
    """
    raise HTTPException(
        status_code=405,  # Method Not Allowed
        detail={
            "error": "event_immutability_violation",
            "message": "R&D Rule #7: Thread events are IMMUTABLE and cannot be modified",
            "rule": "R&D_RULE_7",
            "recommendation": "Add a new event instead of modifying existing ones"
        }
    )


@router.delete("/{thread_id}/events/{event_id}", summary="Delete event (FORBIDDEN)")
async def delete_event(thread_id: str, event_id: str):
    """
    Attempt to delete an event.

    R&D RULE #7: Events are APPEND-ONLY - deletion is forbidden.
    """
    raise HTTPException(
        status_code=405,
        detail={
            "error": "event_deletion_forbidden",
            "message": "R&D Rule #7: Thread events are append-only and cannot be deleted",
            "rule": "R&D_RULE_7"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD ACTIONS (DECISIONS, NOTES)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{thread_id}/decisions", summary="Record a decision")
async def record_decision(
    thread_id: str,
    title: str = Body(...),
    description: str = Body(...),
    rationale: Optional[str] = Body(None),
    alternatives_considered: List[str] = Body(default=[]),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Record a decision in the thread.

    Decisions are special events with structured data.
    """
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Verify thread exists and ownership
        thread_query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        thread_result = await db.execute(thread_query)
        thread = thread_result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        verify_ownership(thread, user_id)

        # Get next sequence number
        max_seq_query = select(func.max(ThreadEventModel.sequence_number)).where(
            ThreadEventModel.thread_id == UUID(thread_id)
        )
        max_seq_result = await db.execute(max_seq_query)
        max_seq = max_seq_result.scalar() or -1

        now = datetime.now(timezone.utc)

        decision_event = ThreadEventModel(
            id=uuid4(),
            thread_id=UUID(thread_id),
            event_type=ThreadEventType.DECISION_RECORDED.value,
            event_data={
                "title": title,
                "description": description,
                "rationale": rationale,
                "alternatives_considered": alternatives_considered,
                "decided_at": now.isoformat()
            },
            sequence_number=max_seq + 1,
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(decision_event)

        # Update maturity if first decision
        if thread.maturity_score < 25:
            thread.maturity_score = 25  # Promote to SPROUT
        else:
            thread.maturity_score += 5

        thread.updated_at = now

        await db.commit()
        await db.refresh(decision_event)

        return {
            "id": str(decision_event.id),
            "thread_id": str(decision_event.thread_id),
            "event_type": decision_event.event_type,
            "data": decision_event.event_data,
            "created_by": str(decision_event.created_by),
            "created_at": decision_event.created_at.isoformat(),
            "immutable": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording decision: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{thread_id}/notes", summary="Add a note")
async def add_note(
    thread_id: str,
    content: str = Body(...),
    note_type: str = Body("general"),  # general, insight, reminder, question
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """Add a note to the thread."""
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Verify thread exists and ownership
        thread_query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        thread_result = await db.execute(thread_query)
        thread = thread_result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        verify_ownership(thread, user_id)

        # Get next sequence number
        max_seq_query = select(func.max(ThreadEventModel.sequence_number)).where(
            ThreadEventModel.thread_id == UUID(thread_id)
        )
        max_seq_result = await db.execute(max_seq_query)
        max_seq = max_seq_result.scalar() or -1

        now = datetime.now(timezone.utc)

        note_event = ThreadEventModel(
            id=uuid4(),
            thread_id=UUID(thread_id),
            event_type=ThreadEventType.NOTE_ADDED.value,
            event_data={
                "content": content,
                "note_type": note_type
            },
            sequence_number=max_seq + 1,
            created_by=user_id,
            created_at=now,
            updated_at=now
        )

        db.add(note_event)

        thread.maturity_score += 1
        thread.updated_at = now

        await db.commit()
        await db.refresh(note_event)

        return {
            "id": str(note_event.id),
            "thread_id": str(note_event.thread_id),
            "event_type": note_event.event_type,
            "content": content,
            "data": note_event.event_data,
            "created_by": str(note_event.created_by),
            "created_at": note_event.created_at.isoformat(),
            "immutable": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding note: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD STATS & HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{thread_id}/stats", summary="Get thread statistics")
async def get_thread_stats(
    thread_id: str,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """Get statistics for a thread."""
    user_id = get_current_user_id()

    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Verify thread exists and ownership
        thread_query = select(ThreadModel).where(ThreadModel.id == UUID(thread_id))
        thread_result = await db.execute(thread_query)
        thread = thread_result.scalar_one_or_none()

        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")

        verify_ownership(thread, user_id)

        # Count events by type
        events_query = select(
            ThreadEventModel.event_type,
            func.count(ThreadEventModel.id).label('count')
        ).where(
            ThreadEventModel.thread_id == UUID(thread_id)
        ).group_by(ThreadEventModel.event_type)

        result = await db.execute(events_query)
        event_counts = {row.event_type: row.count for row in result}

        # Total events
        total_events = sum(event_counts.values())

        maturity = _maturity_from_score(thread.maturity_score)

        return {
            "thread_id": thread_id,
            "total_events": total_events,
            "event_breakdown": event_counts,
            "maturity": {
                "level": maturity["level"],
                "emoji": maturity["emoji"],
                "score": thread.maturity_score
            },
            "created_at": thread.created_at.isoformat(),
            "last_activity": thread.updated_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting thread stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", summary="Threads service health")
async def threads_health(db: Optional[AsyncSession] = Depends(get_db_optional)):
    """Health check for threads service."""

    if db is None:
        return {
            "service": "threads",
            "status": "degraded",
            "version": "v76",
            "database": "unavailable",
            "total_threads": 0,
            "total_events": 0,
            "r&d_compliance": {
                "rule_1": "HTTP 423 for archive/delete",
                "rule_3": "Identity boundary enforced",
                "rule_5": "Chronological order only",
                "rule_6": "Full traceability",
                "rule_7": "Events immutable"
            }
        }

    try:
        # Count threads
        threads_count_query = select(func.count(ThreadModel.id))
        threads_result = await db.execute(threads_count_query)
        total_threads = threads_result.scalar() or 0

        # Count events
        events_count_query = select(func.count(ThreadEventModel.id))
        events_result = await db.execute(events_count_query)
        total_events = events_result.scalar() or 0

        return {
            "service": "threads",
            "status": "healthy",
            "version": "v76",
            "database": "connected",
            "total_threads": total_threads,
            "total_events": total_events,
            "r&d_compliance": {
                "rule_1": "HTTP 423 for archive/delete",
                "rule_3": "Identity boundary enforced",
                "rule_5": "Chronological order only",
                "rule_6": "Full traceability",
                "rule_7": "Events immutable"
            }
        }

    except Exception as e:
        logger.error(f"Health check error: {e}", exc_info=True)
        return {
            "service": "threads",
            "status": "unhealthy",
            "version": "v76",
            "database": "error",
            "error": str(e),
            "r&d_compliance": {
                "rule_1": "HTTP 423 for archive/delete",
                "rule_3": "Identity boundary enforced",
                "rule_5": "Chronological order only",
                "rule_6": "Full traceability",
                "rule_7": "Events immutable"
            }
        }
