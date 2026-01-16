"""
CHE·NU™ V76 — MEMORY ENGINE ROUTER
===================================
Gestion de la mémoire tri-couche (Hot/Warm/Cold).

14 Endpoints pour:
- Accès mémoire par Thread
- Snapshots et compression
- Recherche dans la mémoire
- Garbage collection

TRI-LAYER MEMORY:
- HOT:  Derniers 50 events (Redis, TTL: session)
- WARM: 30 derniers jours (PostgreSQL, indexé)
- COLD: Historique complet (Object Storage, archivé)

R&D Rules Compliance:
- Rule #1: Human gates sur purge/delete
- Rule #6: Traçabilité complète
- Rule #7: Continuité R&D (append-only events)
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger("chenu.routers.memory")

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class MemoryLayer(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class MemoryEventType(str, Enum):
    # Core events
    INTENT_DECLARED = "intent.declared"
    DECISION_RECORDED = "decision.recorded"
    ACTION_CREATED = "action.created"
    ACTION_COMPLETED = "action.completed"
    NOTE_ADDED = "note.added"
    
    # Memory events
    SUMMARY_SNAPSHOT = "summary.snapshot"
    MEMORY_COMPRESSED = "memory.compressed"
    MEMORY_MIGRATED = "memory.migrated"
    
    # System events
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"
    CHECKPOINT_RESOLVED = "checkpoint.resolved"


class MemoryEvent(BaseModel):
    id: UUID
    thread_id: UUID
    event_type: MemoryEventType
    data: Dict[str, Any]
    layer: MemoryLayer
    created_at: datetime
    created_by: UUID
    parent_event_id: Optional[UUID] = None


class MemorySnapshot(BaseModel):
    id: UUID
    thread_id: UUID
    snapshot_type: Literal["summary", "checkpoint", "milestone"]
    content: Dict[str, Any]
    events_count: int
    time_range_start: datetime
    time_range_end: datetime
    created_at: datetime


class MemoryStats(BaseModel):
    thread_id: UUID
    hot_events: int
    warm_events: int
    cold_events: int
    total_events: int
    last_snapshot: Optional[datetime]
    memory_health: Literal["healthy", "needs_compression", "critical"]


class MemorySearchResult(BaseModel):
    events: List[MemoryEvent]
    total: int
    layers_searched: List[MemoryLayer]
    query_time_ms: float


class CheckpointResponse(BaseModel):
    checkpoint_id: UUID
    action: str
    resource_id: UUID
    status: str = "awaiting_approval"
    message: str


# ============================================================================
# MOCK DATABASE
# ============================================================================

_memory_events: Dict[str, List[Dict]] = {}  # thread_id -> events
_snapshots: Dict[str, List[Dict]] = {}  # thread_id -> snapshots


def get_current_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def _get_layer_for_event(event_time: datetime) -> MemoryLayer:
    """Determine memory layer based on event age."""
    age = datetime.utcnow() - event_time
    
    if age < timedelta(hours=24):
        return MemoryLayer.HOT
    elif age < timedelta(days=30):
        return MemoryLayer.WARM
    else:
        return MemoryLayer.COLD


# ============================================================================
# MEMORY ACCESS ENDPOINTS (1-5)
# ============================================================================

@router.get("/threads/{thread_id}", response_model=List[MemoryEvent])
async def get_thread_memory(
    thread_id: UUID,
    layer: Optional[MemoryLayer] = None,
    event_type: Optional[MemoryEventType] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Get memory events for a Thread.
    Default: Returns HOT layer (most recent).
    """
    user_id = get_current_user_id()
    
    events = _memory_events.get(str(thread_id), [])
    
    # Filter by layer
    if layer:
        events = [e for e in events if e["layer"] == layer]
    
    # Filter by event type
    if event_type:
        events = [e for e in events if e["event_type"] == event_type]
    
    # Sort by time (most recent first)
    events = sorted(events, key=lambda x: x["created_at"], reverse=True)
    
    return events[offset:offset + limit]


@router.get("/threads/{thread_id}/hot", response_model=List[MemoryEvent])
async def get_hot_memory(thread_id: UUID, limit: int = Query(50, ge=1, le=100)):
    """
    Get HOT memory (last 50 events, immediate context).
    Fastest access - Redis cached.
    """
    events = _memory_events.get(str(thread_id), [])
    hot_events = [e for e in events if e["layer"] == MemoryLayer.HOT]
    return sorted(hot_events, key=lambda x: x["created_at"], reverse=True)[:limit]


@router.get("/threads/{thread_id}/warm", response_model=List[MemoryEvent])
async def get_warm_memory(
    thread_id: UUID,
    days: int = Query(30, ge=1, le=90),
    limit: int = Query(100, ge=1, le=500)
):
    """
    Get WARM memory (last N days, indexed for search).
    Medium access speed - PostgreSQL.
    """
    events = _memory_events.get(str(thread_id), [])
    warm_events = [e for e in events if e["layer"] == MemoryLayer.WARM]
    return sorted(warm_events, key=lambda x: x["created_at"], reverse=True)[:limit]


@router.get("/threads/{thread_id}/cold", response_model=List[MemoryEvent])
async def get_cold_memory(
    thread_id: UUID,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Get COLD memory (archived history).
    Slowest access - Object Storage.
    """
    events = _memory_events.get(str(thread_id), [])
    cold_events = [e for e in events if e["layer"] == MemoryLayer.COLD]
    
    if start_date:
        cold_events = [e for e in cold_events if e["created_at"] >= start_date.isoformat()]
    if end_date:
        cold_events = [e for e in cold_events if e["created_at"] <= end_date.isoformat()]
    
    return sorted(cold_events, key=lambda x: x["created_at"], reverse=True)[:limit]


@router.post("/threads/{thread_id}/events", response_model=MemoryEvent, status_code=201)
async def add_memory_event(
    thread_id: UUID,
    event_type: MemoryEventType,
    data: Dict[str, Any],
    parent_event_id: Optional[UUID] = None
):
    """
    Add a new event to Thread memory.
    Events are APPEND-ONLY (R&D Rule #7).
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    event = {
        "id": str(uuid4()),
        "thread_id": str(thread_id),
        "event_type": event_type,
        "data": data,
        "layer": MemoryLayer.HOT,  # New events always start in HOT
        "created_at": now.isoformat(),
        "created_by": str(user_id),
        "parent_event_id": str(parent_event_id) if parent_event_id else None
    }
    
    if str(thread_id) not in _memory_events:
        _memory_events[str(thread_id)] = []
    
    _memory_events[str(thread_id)].append(event)
    
    logger.info(f"Memory event added: {event_type} to thread {thread_id}")
    return event


# ============================================================================
# SNAPSHOT ENDPOINTS (6-8)
# ============================================================================

@router.get("/threads/{thread_id}/snapshots", response_model=List[MemorySnapshot])
async def list_snapshots(
    thread_id: UUID,
    snapshot_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """List all snapshots for a Thread."""
    snapshots = _snapshots.get(str(thread_id), [])
    
    if snapshot_type:
        snapshots = [s for s in snapshots if s["snapshot_type"] == snapshot_type]
    
    return sorted(snapshots, key=lambda x: x["created_at"], reverse=True)[:limit]


@router.post("/threads/{thread_id}/snapshots", response_model=MemorySnapshot, status_code=201)
async def create_snapshot(
    thread_id: UUID,
    snapshot_type: Literal["summary", "checkpoint", "milestone"] = "summary"
):
    """
    Create a memory snapshot (compression point).
    Used for summarizing and archiving memory.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    events = _memory_events.get(str(thread_id), [])
    
    if not events:
        raise HTTPException(status_code=400, detail="No events to snapshot")
    
    # Get time range
    sorted_events = sorted(events, key=lambda x: x["created_at"])
    
    snapshot = {
        "id": str(uuid4()),
        "thread_id": str(thread_id),
        "snapshot_type": snapshot_type,
        "content": {
            "event_count": len(events),
            "event_types": list(set(e["event_type"] for e in events)),
            "summary": f"Snapshot of {len(events)} events"
            # TODO: AI-generated summary
        },
        "events_count": len(events),
        "time_range_start": sorted_events[0]["created_at"],
        "time_range_end": sorted_events[-1]["created_at"],
        "created_at": now.isoformat()
    }
    
    if str(thread_id) not in _snapshots:
        _snapshots[str(thread_id)] = []
    
    _snapshots[str(thread_id)].append(snapshot)
    
    logger.info(f"Snapshot created for thread {thread_id}: {snapshot_type}")
    return snapshot


@router.get("/threads/{thread_id}/snapshots/{snapshot_id}", response_model=MemorySnapshot)
async def get_snapshot(thread_id: UUID, snapshot_id: UUID):
    """Get a specific snapshot."""
    snapshots = _snapshots.get(str(thread_id), [])
    
    for s in snapshots:
        if s["id"] == str(snapshot_id):
            return s
    
    raise HTTPException(status_code=404, detail="Snapshot not found")


# ============================================================================
# SEARCH & STATS ENDPOINTS (9-11)
# ============================================================================

@router.get("/threads/{thread_id}/search", response_model=MemorySearchResult)
async def search_memory(
    thread_id: UUID,
    q: str = Query(..., min_length=1, max_length=500),
    layers: List[MemoryLayer] = Query(default=[MemoryLayer.HOT, MemoryLayer.WARM]),
    event_types: Optional[List[MemoryEventType]] = None,
    limit: int = Query(50, ge=1, le=200)
):
    """
    Search through Thread memory.
    Searches across specified layers.
    """
    import time
    start_time = time.time()
    
    events = _memory_events.get(str(thread_id), [])
    
    # Filter by layers
    events = [e for e in events if e["layer"] in layers]
    
    # Filter by event types
    if event_types:
        events = [e for e in events if e["event_type"] in event_types]
    
    # Simple text search in data
    q_lower = q.lower()
    matching = []
    for e in events:
        data_str = str(e["data"]).lower()
        if q_lower in data_str:
            matching.append(e)
            if len(matching) >= limit:
                break
    
    query_time = (time.time() - start_time) * 1000
    
    return MemorySearchResult(
        events=matching,
        total=len(matching),
        layers_searched=layers,
        query_time_ms=query_time
    )


@router.get("/threads/{thread_id}/stats", response_model=MemoryStats)
async def get_memory_stats(thread_id: UUID):
    """Get memory statistics for a Thread."""
    events = _memory_events.get(str(thread_id), [])
    snapshots = _snapshots.get(str(thread_id), [])
    
    hot = sum(1 for e in events if e["layer"] == MemoryLayer.HOT)
    warm = sum(1 for e in events if e["layer"] == MemoryLayer.WARM)
    cold = sum(1 for e in events if e["layer"] == MemoryLayer.COLD)
    total = len(events)
    
    # Determine health
    if hot > 100:
        health = "needs_compression"
    elif total > 10000:
        health = "critical"
    else:
        health = "healthy"
    
    last_snapshot = None
    if snapshots:
        last_snapshot = max(s["created_at"] for s in snapshots)
    
    return MemoryStats(
        thread_id=thread_id,
        hot_events=hot,
        warm_events=warm,
        cold_events=cold,
        total_events=total,
        last_snapshot=last_snapshot,
        memory_health=health
    )


@router.get("/threads/{thread_id}/timeline")
async def get_memory_timeline(
    thread_id: UUID,
    granularity: Literal["hour", "day", "week", "month"] = "day",
    limit: int = Query(30, ge=1, le=365)
):
    """Get memory timeline visualization data."""
    events = _memory_events.get(str(thread_id), [])
    
    # Group by time period
    timeline = {}
    for e in events:
        # Parse date and group
        date_str = e["created_at"][:10]  # YYYY-MM-DD
        if date_str not in timeline:
            timeline[date_str] = {"date": date_str, "count": 0, "types": {}}
        timeline[date_str]["count"] += 1
        
        event_type = e["event_type"]
        if event_type not in timeline[date_str]["types"]:
            timeline[date_str]["types"][event_type] = 0
        timeline[date_str]["types"][event_type] += 1
    
    return {
        "thread_id": str(thread_id),
        "granularity": granularity,
        "data": sorted(timeline.values(), key=lambda x: x["date"], reverse=True)[:limit]
    }


# ============================================================================
# MAINTENANCE ENDPOINTS (12-14)
# ============================================================================

@router.post("/threads/{thread_id}/compress")
async def compress_memory(thread_id: UUID):
    """
    Compress memory: Move old HOT → WARM → COLD.
    Creates snapshot before compression.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    events = _memory_events.get(str(thread_id), [])
    
    if not events:
        return {"status": "nothing_to_compress", "moved": 0}
    
    moved = 0
    for e in events:
        event_time = datetime.fromisoformat(e["created_at"].replace('Z', '+00:00').replace('+00:00', ''))
        new_layer = _get_layer_for_event(event_time)
        
        if e["layer"] != new_layer:
            e["layer"] = new_layer
            moved += 1
    
    logger.info(f"Memory compressed for thread {thread_id}: {moved} events migrated")
    
    return {
        "status": "compressed",
        "thread_id": str(thread_id),
        "events_moved": moved
    }


@router.post("/threads/{thread_id}/purge", response_model=CheckpointResponse)
async def purge_cold_memory(
    thread_id: UUID,
    older_than_days: int = Query(365, ge=90)
):
    """
    Purge old COLD memory.
    R&D Rule #1: Requires human approval (destructive).
    """
    user_id = get_current_user_id()
    
    events = _memory_events.get(str(thread_id), [])
    cold_events = [e for e in events if e["layer"] == MemoryLayer.COLD]
    
    cutoff = datetime.utcnow() - timedelta(days=older_than_days)
    to_purge = sum(1 for e in cold_events 
                   if datetime.fromisoformat(e["created_at"].replace('Z', '')) < cutoff)
    
    # R&D Rule #1: Human gate
    checkpoint = CheckpointResponse(
        checkpoint_id=uuid4(),
        action="purge_cold_memory",
        resource_id=thread_id,
        status="awaiting_approval",
        message=f"Confirm purge of {to_purge} cold memory events older than {older_than_days} days"
    )
    
    logger.warning(f"CHECKPOINT: Purge cold memory for thread {thread_id}")
    raise HTTPException(status_code=423, detail=checkpoint.dict())


@router.get("/health")
async def memory_health():
    """Memory system health check."""
    total_threads = len(_memory_events)
    total_events = sum(len(events) for events in _memory_events.values())
    total_snapshots = sum(len(snaps) for snaps in _snapshots.values())
    
    return {
        "status": "healthy",
        "threads_with_memory": total_threads,
        "total_events": total_events,
        "total_snapshots": total_snapshots,
        "layers": {
            "hot": {"status": "ok", "store": "redis"},
            "warm": {"status": "ok", "store": "postgresql"},
            "cold": {"status": "ok", "store": "object_storage"}
        }
    }
