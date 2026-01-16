"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V75 — MEMORY API                                  ║
║                                                                              ║
║  Tri-Layer Memory System: Hot/Warm/Cold                                      ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/memory", tags=["Memory"])

# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class MemoryLayer(str, Enum):
    HOT = "hot"      # Immediate - Redis
    WARM = "warm"    # Recent - PostgreSQL
    COLD = "cold"    # Archive - Object Storage

class MemoryType(str, Enum):
    EVENT = "event"
    DECISION = "decision"
    NOTE = "note"
    SNAPSHOT = "snapshot"
    CONTEXT = "context"

class MemoryItem(BaseModel):
    id: str
    thread_id: str
    type: MemoryType
    layer: MemoryLayer
    content: str
    summary: Optional[str] = None
    relevance_score: float = 0.0
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0

class MemorySearchRequest(BaseModel):
    query: str
    thread_ids: Optional[List[str]] = None
    types: Optional[List[MemoryType]] = None
    layers: Optional[List[MemoryLayer]] = None
    limit: int = 20

class MemorySearchResult(BaseModel):
    items: List[MemoryItem]
    total: int
    query: str
    took_ms: int

class ThreadMemoryStats(BaseModel):
    thread_id: str
    hot_count: int
    warm_count: int
    cold_count: int
    total_items: int
    last_accessed: datetime

# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

MEMORY_DB: List[MemoryItem] = [
    MemoryItem(
        id="mem-001",
        thread_id="thread-1",
        type=MemoryType.EVENT,
        layer=MemoryLayer.HOT,
        content="User created new thread for Q1 planning",
        summary="Q1 planning thread created",
        relevance_score=0.95,
        created_at=datetime.utcnow() - timedelta(hours=1),
        accessed_at=datetime.utcnow(),
        access_count=5,
    ),
    MemoryItem(
        id="mem-002",
        thread_id="thread-1",
        type=MemoryType.DECISION,
        layer=MemoryLayer.HOT,
        content="Decision: Approve budget allocation for marketing",
        summary="Marketing budget approved",
        relevance_score=0.88,
        created_at=datetime.utcnow() - timedelta(hours=2),
        accessed_at=datetime.utcnow() - timedelta(minutes=30),
        access_count=3,
    ),
    MemoryItem(
        id="mem-003",
        thread_id="thread-2",
        type=MemoryType.NOTE,
        layer=MemoryLayer.WARM,
        content="Meeting notes: Discussed product roadmap with team",
        summary="Product roadmap meeting",
        relevance_score=0.72,
        created_at=datetime.utcnow() - timedelta(days=3),
        accessed_at=datetime.utcnow() - timedelta(days=1),
        access_count=8,
    ),
    MemoryItem(
        id="mem-004",
        thread_id="thread-1",
        type=MemoryType.SNAPSHOT,
        layer=MemoryLayer.COLD,
        content="Weekly summary: 5 decisions made, 12 actions completed",
        summary="Week 1 summary",
        relevance_score=0.45,
        created_at=datetime.utcnow() - timedelta(days=30),
        accessed_at=datetime.utcnow() - timedelta(days=15),
        access_count=2,
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/search", response_model=MemorySearchResult)
async def search_memory(request: MemorySearchRequest):
    """Search across memory layers."""
    import time
    start = time.time()
    
    results = []
    query_lower = request.query.lower()
    
    for item in MEMORY_DB:
        # Filter by thread_ids
        if request.thread_ids and item.thread_id not in request.thread_ids:
            continue
        # Filter by types
        if request.types and item.type not in request.types:
            continue
        # Filter by layers
        if request.layers and item.layer not in request.layers:
            continue
        # Search in content
        if query_lower in item.content.lower() or (item.summary and query_lower in item.summary.lower()):
            results.append(item)
    
    # Sort by relevance
    results.sort(key=lambda x: x.relevance_score, reverse=True)
    
    # Limit
    results = results[:request.limit]
    
    took_ms = int((time.time() - start) * 1000)
    
    return MemorySearchResult(
        items=results,
        total=len(results),
        query=request.query,
        took_ms=took_ms,
    )

@router.get("/recent", response_model=List[MemoryItem])
async def get_recent_memory(
    limit: int = Query(default=10, le=50),
    layer: Optional[MemoryLayer] = None,
):
    """Get recently accessed memory items."""
    results = MEMORY_DB.copy()
    
    if layer:
        results = [m for m in results if m.layer == layer]
    
    results.sort(key=lambda x: x.accessed_at, reverse=True)
    return results[:limit]

@router.get("/thread/{thread_id}", response_model=List[MemoryItem])
async def get_thread_memory(
    thread_id: str,
    layer: Optional[MemoryLayer] = None,
    limit: int = Query(default=20, le=100),
):
    """Get memory items for a specific thread."""
    results = [m for m in MEMORY_DB if m.thread_id == thread_id]
    
    if layer:
        results = [m for m in results if m.layer == layer]
    
    results.sort(key=lambda x: x.created_at, reverse=True)
    return results[:limit]

@router.get("/thread/{thread_id}/stats", response_model=ThreadMemoryStats)
async def get_thread_memory_stats(thread_id: str):
    """Get memory statistics for a thread."""
    items = [m for m in MEMORY_DB if m.thread_id == thread_id]
    
    hot = len([m for m in items if m.layer == MemoryLayer.HOT])
    warm = len([m for m in items if m.layer == MemoryLayer.WARM])
    cold = len([m for m in items if m.layer == MemoryLayer.COLD])
    
    last_accessed = max((m.accessed_at for m in items), default=datetime.utcnow())
    
    return ThreadMemoryStats(
        thread_id=thread_id,
        hot_count=hot,
        warm_count=warm,
        cold_count=cold,
        total_items=len(items),
        last_accessed=last_accessed,
    )

@router.post("/compress/{thread_id}")
async def compress_thread_memory(thread_id: str):
    """Compress hot memory to warm, warm to cold."""
    # In production: move items between layers based on age/access
    return {
        "success": True,
        "thread_id": thread_id,
        "message": "Memory compression initiated",
        "items_processed": len([m for m in MEMORY_DB if m.thread_id == thread_id]),
    }
