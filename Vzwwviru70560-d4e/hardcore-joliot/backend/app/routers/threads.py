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
from uuid import uuid4
from enum import Enum

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
# MOCK DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

# In production: PostgreSQL + Redis
MOCK_THREADS: Dict[str, Dict] = {}
MOCK_EVENTS: Dict[str, List[Dict]] = {}  # thread_id -> events
MOCK_CHECKPOINTS: Dict[str, Dict] = {}


def get_current_user_id() -> str:
    """Mock: Get current user from JWT."""
    return "test-user-001"


def verify_ownership(thread: Dict, user_id: str) -> None:
    """Rule #3: Identity Boundary enforcement."""
    if thread.get("owner_id") != user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Access denied: resource belongs to different identity",
                "your_identity": user_id,
                "resource_owner": thread.get("owner_id")
            }
        )


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
    # Rule #5: NO sort_by parameter for ranking
):
    """
    List threads for current user.
    
    R&D RULE #5: Results are ALWAYS chronological (newest first).
    NO engagement/popularity ranking allowed.
    """
    user_id = get_current_user_id()
    
    # Filter by owner (Rule #3)
    threads = [t for t in MOCK_THREADS.values() if t["owner_id"] == user_id]
    
    # Apply filters
    if sphere:
        threads = [t for t in threads if t["sphere"] == sphere]
    if status:
        threads = [t for t in threads if t["status"] == status.value]
    if maturity:
        threads = [t for t in threads if t["maturity_level"] == maturity.value]
    
    # Rule #5: ALWAYS chronological order (newest first)
    threads.sort(key=lambda t: t["created_at"], reverse=True)
    
    # Pagination
    total = len(threads)
    threads = threads[offset:offset + limit]
    
    return {
        "items": threads,
        "total": total,
        "limit": limit,
        "offset": offset,
        "order": "chronological_desc"  # Explicit: Rule #5
    }


@router.post("/", summary="Create new thread", status_code=201)
async def create_thread(
    title: str = Body(..., min_length=1, max_length=200),
    description: Optional[str] = Body(None, max_length=2000),
    sphere: str = Body("Personal"),
    founding_intent: str = Body(..., min_length=1, max_length=500),
    thread_type: ThreadType = Body(ThreadType.PERSONAL),
    parent_thread_id: Optional[str] = Body(None),
    tags: List[str] = Body(default=[])
):
    """
    Create a new thread.
    
    R&D RULE #6: Automatic traceability (id, created_by, created_at)
    R&D RULE #7: founding_intent is IMMUTABLE once set
    """
    user_id = get_current_user_id()
    thread_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    thread = {
        # Identity
        "id": thread_id,
        "title": title,
        "description": description,
        
        # R&D Rule #6: Traceability (MANDATORY)
        "created_by": user_id,
        "created_at": now,
        "updated_at": now,
        
        # Ownership
        "owner_id": user_id,
        "sphere": sphere,
        "thread_type": thread_type.value,
        
        # R&D Rule #7: Founding Intent (IMMUTABLE)
        "founding_intent": founding_intent,
        
        # Hierarchy
        "parent_thread_id": parent_thread_id,
        
        # State
        "status": ThreadStatus.ACTIVE.value,
        "maturity_level": MaturityLevel.SEED.value,
        "maturity_emoji": "🌱",
        
        # Metadata
        "tags": tags,
        "events_count": 1  # Creation event
    }
    
    MOCK_THREADS[thread_id] = thread
    
    # Create initial event (Rule #6: Traceability)
    initial_event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": ThreadEventType.THREAD_CREATED.value,
        "created_by": user_id,
        "created_at": now,
        "data": {
            "title": title,
            "founding_intent": founding_intent
        },
        "immutable": True  # Events are NEVER modified
    }
    MOCK_EVENTS[thread_id] = [initial_event]
    
    return thread


@router.get("/{thread_id}", summary="Get thread by ID")
async def get_thread(thread_id: str):
    """
    Get a specific thread.
    
    R&D RULE #3: Identity boundary enforced.
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3: Identity Boundary
    verify_ownership(thread, user_id)
    
    return thread


@router.patch("/{thread_id}", summary="Update thread")
async def update_thread(
    thread_id: str,
    title: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
    status: Optional[ThreadStatus] = Body(None),
    tags: Optional[List[str]] = Body(None)
    # NOTE: founding_intent NOT accepted - IMMUTABLE (Rule #7)
):
    """
    Update thread metadata.
    
    R&D RULE #7: founding_intent CANNOT be changed.
    R&D RULE #6: updated_at auto-updated.
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3: Identity Boundary
    verify_ownership(thread, user_id)
    
    # Update allowed fields
    now = datetime.now(timezone.utc).isoformat()
    
    if title is not None:
        thread["title"] = title
    if description is not None:
        thread["description"] = description
    if status is not None:
        thread["status"] = status.value
    if tags is not None:
        thread["tags"] = tags
    
    thread["updated_at"] = now
    
    # Log update event
    update_event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": ThreadEventType.THREAD_UPDATED.value,
        "created_by": user_id,
        "created_at": now,
        "data": {"fields_updated": [k for k in [title, description, status, tags] if k]},
        "immutable": True
    }
    
    if thread_id not in MOCK_EVENTS:
        MOCK_EVENTS[thread_id] = []
    MOCK_EVENTS[thread_id].append(update_event)
    thread["events_count"] = len(MOCK_EVENTS[thread_id])
    
    return thread


@router.post("/{thread_id}/archive", summary="Archive thread (checkpoint required)")
async def archive_thread(
    thread_id: str,
    checkpoint_id: Optional[str] = Body(None)
):
    """
    Archive a thread.
    
    R&D RULE #1: Requires human approval (HTTP 423 without checkpoint)
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3: Identity Boundary
    verify_ownership(thread, user_id)
    
    # Rule #1: Human Sovereignty - Checkpoint required
    if not checkpoint_id:
        checkpoint = {
            "id": str(uuid4()),
            "type": "governance",
            "status": "pending",
            "action": "thread.archive",
            "resource_id": thread_id,
            "message": "Thread archival requires human approval",
            "created_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        MOCK_CHECKPOINTS[checkpoint["id"]] = checkpoint
        
        raise HTTPException(
            status_code=423,  # LOCKED
            detail={
                "status": "checkpoint_required",
                "checkpoint_id": checkpoint["id"],
                "message": "Action requires human approval",
                "action": "thread.archive"
            }
        )
    
    # Verify checkpoint is approved
    if checkpoint_id not in MOCK_CHECKPOINTS:
        raise HTTPException(status_code=400, detail="Invalid checkpoint")
    
    checkpoint = MOCK_CHECKPOINTS[checkpoint_id]
    if checkpoint["status"] != "approved":
        raise HTTPException(
            status_code=423,
            detail={
                "status": "checkpoint_not_approved",
                "checkpoint_id": checkpoint_id,
                "checkpoint_status": checkpoint["status"]
            }
        )
    
    # Execute archive
    now = datetime.now(timezone.utc).isoformat()
    thread["status"] = ThreadStatus.ARCHIVED.value
    thread["updated_at"] = now
    thread["archived_at"] = now
    
    # Log archive event
    archive_event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": ThreadEventType.THREAD_ARCHIVED.value,
        "created_by": user_id,
        "created_at": now,
        "data": {"checkpoint_id": checkpoint_id},
        "immutable": True
    }
    MOCK_EVENTS[thread_id].append(archive_event)
    
    return {"status": "archived", "thread": thread}


@router.delete("/{thread_id}", summary="Delete thread (checkpoint required)")
async def delete_thread(
    thread_id: str,
    checkpoint_id: Optional[str] = Body(None)
):
    """
    Delete a thread (soft delete).
    
    R&D RULE #1: CRITICAL action - requires checkpoint
    R&D RULE #7: Events are preserved (append-only)
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3: Identity Boundary
    verify_ownership(thread, user_id)
    
    # Rule #1: CRITICAL - Checkpoint required
    if not checkpoint_id:
        checkpoint = {
            "id": str(uuid4()),
            "type": "destructive",
            "priority": "critical",
            "status": "pending",
            "action": "thread.delete",
            "resource_id": thread_id,
            "message": "Thread deletion is CRITICAL and requires explicit approval",
            "created_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        MOCK_CHECKPOINTS[checkpoint["id"]] = checkpoint
        
        raise HTTPException(
            status_code=423,
            detail={
                "status": "checkpoint_required",
                "checkpoint_id": checkpoint["id"],
                "message": "CRITICAL: Thread deletion requires explicit human approval",
                "action": "thread.delete",
                "priority": "critical"
            }
        )
    
    # Verify checkpoint
    if checkpoint_id not in MOCK_CHECKPOINTS:
        raise HTTPException(status_code=400, detail="Invalid checkpoint")
    
    checkpoint = MOCK_CHECKPOINTS[checkpoint_id]
    if checkpoint["status"] != "approved":
        raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    # Soft delete (events preserved per Rule #7)
    thread["status"] = "deleted"
    thread["deleted_at"] = datetime.now(timezone.utc).isoformat()
    thread["deleted_by"] = user_id
    
    return {"status": "deleted", "thread_id": thread_id, "events_preserved": True}


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{thread_id}/events", summary="Get thread events (chronological)")
async def get_thread_events(
    thread_id: str,
    event_type: Optional[ThreadEventType] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Get events for a thread.
    
    R&D RULE #5: Events are ALWAYS chronological.
    R&D RULE #7: Events are immutable (append-only).
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3
    verify_ownership(thread, user_id)
    
    events = MOCK_EVENTS.get(thread_id, [])
    
    if event_type:
        events = [e for e in events if e["event_type"] == event_type.value]
    
    # Rule #5: Chronological order (oldest first for events)
    events.sort(key=lambda e: e["created_at"])
    
    total = len(events)
    events = events[offset:offset + limit]
    
    return {
        "thread_id": thread_id,
        "events": events,
        "total": total,
        "order": "chronological_asc"  # Events: oldest first
    }


@router.post("/{thread_id}/events", summary="Add event to thread")
async def add_thread_event(
    thread_id: str,
    event_type: ThreadEventType = Body(...),
    content: Optional[str] = Body(None),
    data: Optional[Dict[str, Any]] = Body(None)
):
    """
    Add an event to a thread.
    
    R&D RULE #6: Full traceability.
    R&D RULE #7: Events are IMMUTABLE once created.
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    
    # Rule #3
    verify_ownership(thread, user_id)
    
    now = datetime.now(timezone.utc).isoformat()
    
    event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": event_type.value,
        "content": content,
        "data": data or {},
        # Rule #6: Traceability
        "created_by": user_id,
        "created_at": now,
        # Rule #7: Immutable marker
        "immutable": True
    }
    
    if thread_id not in MOCK_EVENTS:
        MOCK_EVENTS[thread_id] = []
    MOCK_EVENTS[thread_id].append(event)
    
    # Update thread
    thread["events_count"] = len(MOCK_EVENTS[thread_id])
    thread["updated_at"] = now
    
    return event


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
    alternatives_considered: List[str] = Body(default=[])
):
    """
    Record a decision in the thread.
    
    Decisions are special events with structured data.
    """
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    verify_ownership(thread, user_id)
    
    now = datetime.now(timezone.utc).isoformat()
    
    decision_event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": ThreadEventType.DECISION_RECORDED.value,
        "created_by": user_id,
        "created_at": now,
        "data": {
            "title": title,
            "description": description,
            "rationale": rationale,
            "alternatives_considered": alternatives_considered,
            "decided_at": now
        },
        "immutable": True
    }
    
    MOCK_EVENTS[thread_id].append(decision_event)
    thread["events_count"] = len(MOCK_EVENTS[thread_id])
    thread["updated_at"] = now
    
    # Update maturity if first decision
    if thread["maturity_level"] == MaturityLevel.SEED.value:
        thread["maturity_level"] = MaturityLevel.SPROUT.value
        thread["maturity_emoji"] = "🌿"
    
    return decision_event


@router.post("/{thread_id}/notes", summary="Add a note")
async def add_note(
    thread_id: str,
    content: str = Body(...),
    note_type: str = Body("general")  # general, insight, reminder, question
):
    """Add a note to the thread."""
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    verify_ownership(thread, user_id)
    
    now = datetime.now(timezone.utc).isoformat()
    
    note_event = {
        "id": str(uuid4()),
        "thread_id": thread_id,
        "event_type": ThreadEventType.NOTE_ADDED.value,
        "content": content,
        "created_by": user_id,
        "created_at": now,
        "data": {"note_type": note_type},
        "immutable": True
    }
    
    MOCK_EVENTS[thread_id].append(note_event)
    thread["events_count"] = len(MOCK_EVENTS[thread_id])
    thread["updated_at"] = now
    
    return note_event


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD STATS & HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{thread_id}/stats", summary="Get thread statistics")
async def get_thread_stats(thread_id: str):
    """Get statistics for a thread."""
    if thread_id not in MOCK_THREADS:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    thread = MOCK_THREADS[thread_id]
    user_id = get_current_user_id()
    verify_ownership(thread, user_id)
    
    events = MOCK_EVENTS.get(thread_id, [])
    
    # Count by event type
    event_counts = {}
    for event in events:
        et = event["event_type"]
        event_counts[et] = event_counts.get(et, 0) + 1
    
    return {
        "thread_id": thread_id,
        "total_events": len(events),
        "event_breakdown": event_counts,
        "maturity": {
            "level": thread["maturity_level"],
            "emoji": thread["maturity_emoji"]
        },
        "created_at": thread["created_at"],
        "last_activity": thread["updated_at"]
    }


@router.get("/health", summary="Threads service health")
async def threads_health():
    """Health check for threads service."""
    return {
        "service": "threads",
        "status": "healthy",
        "version": "v76",
        "total_threads": len(MOCK_THREADS),
        "total_events": sum(len(e) for e in MOCK_EVENTS.values()),
        "r&d_compliance": {
            "rule_1": "HTTP 423 for archive/delete",
            "rule_3": "Identity boundary enforced",
            "rule_5": "Chronological order only",
            "rule_6": "Full traceability",
            "rule_7": "Events immutable"
        }
    }
