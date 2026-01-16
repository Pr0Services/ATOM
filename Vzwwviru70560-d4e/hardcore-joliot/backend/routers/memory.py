"""
CHE·NU™ V75 - Memory Router
Governed Memory System API.

GOUVERNANCE > EXÉCUTION
- All memory access is governed
- Cross-identity access blocked
- Audit trail for all operations

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

class MemoryItemCreate(BaseModel):
    """Create memory item."""
    memory_type: str = "short_term"  # short_term, mid_term, long_term, institutional, agent
    memory_category: str = "fact"  # preference, instruction, fact, context, rule
    content: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = {}
    dataspace_id: Optional[str] = None
    thread_id: Optional[str] = None


class MemoryItemUpdate(BaseModel):
    """Update memory item."""
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ElevationRequestCreate(BaseModel):
    """Create elevation request."""
    requested_action: str
    resource_type: str
    resource_id: str
    reason: str


class AuditLogFilter(BaseModel):
    """Audit log filter."""
    action_type: Optional[str] = None
    resource_type: Optional[str] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None


# ============================================================================
# MOCK DATA
# ============================================================================

MEMORY_TYPES = ["short_term", "mid_term", "long_term", "institutional", "agent"]
MEMORY_CATEGORIES = ["preference", "instruction", "fact", "context", "rule"]
MEMORY_STATUSES = ["active", "pinned", "archived", "deleted"]

MOCK_MEMORIES = [
    {
        "id": "mem_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "memory_type": "long_term",
        "memory_category": "preference",
        "content": "Préfère les rapports en format PDF avec graphiques",
        "metadata": {"source": "conversation", "confidence": 0.9},
        "dataspace_id": None,
        "thread_id": "thread_001",
        "status": "active",
        "expires_at": None,
        "created_at": "2026-01-01T10:00:00Z",
        "updated_at": "2026-01-07T15:00:00Z",
    },
    {
        "id": "mem_002",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "memory_type": "institutional",
        "memory_category": "rule",
        "content": "Estimations construction doivent inclure 15% contingence",
        "metadata": {"domain": "construction", "mandatory": True},
        "dataspace_id": "ds_construction_001",
        "thread_id": None,
        "status": "pinned",
        "expires_at": None,
        "created_at": "2025-12-15T09:00:00Z",
        "updated_at": "2026-01-05T12:00:00Z",
    },
    {
        "id": "mem_003",
        "user_id": "user_001",
        "identity_id": "identity_002",  # Different identity
        "memory_type": "short_term",
        "memory_category": "context",
        "content": "Travaille sur le projet Maya cette semaine",
        "metadata": {"project": "maya"},
        "dataspace_id": None,
        "thread_id": "thread_project_maya",
        "status": "active",
        "expires_at": "2026-01-14T00:00:00Z",
        "created_at": "2026-01-07T08:00:00Z",
        "updated_at": "2026-01-07T08:00:00Z",
    },
]

MOCK_AUDIT_LOG = [
    {
        "id": "audit_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "agent_id": None,
        "action_type": "create",
        "resource_type": "memory",
        "resource_id": "mem_001",
        "action_details": {"memory_type": "long_term"},
        "before_state": None,
        "after_state": {"content": "Préfère les rapports..."},
        "permission_used": "memory.write",
        "elevation_required": False,
        "elevation_approved": None,
        "ip_address": "192.168.1.1",
        "user_agent": "CHE-NU/1.0",
        "created_at": "2026-01-01T10:00:00Z",
    },
]

MOCK_ELEVATION_REQUESTS = []


# ============================================================================
# MEMORY ITEMS
# ============================================================================

@router.get("/items", response_model=dict)
async def list_memories(
    memory_type: Optional[str] = None,
    memory_category: Optional[str] = None,
    status: Optional[str] = "active",
    dataspace_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List memory items.
    
    GOUVERNANCE: Only returns memories for current identity.
    """
    # Filter by current identity (simulated as identity_001)
    current_identity = "identity_001"
    memories = [m for m in MOCK_MEMORIES if m["identity_id"] == current_identity]
    
    if memory_type:
        memories = [m for m in memories if m["memory_type"] == memory_type]
    if memory_category:
        memories = [m for m in memories if m["memory_category"] == memory_category]
    if status:
        memories = [m for m in memories if m["status"] == status]
    if dataspace_id:
        memories = [m for m in memories if m["dataspace_id"] == dataspace_id]
    
    total = len(memories)
    
    return {
        "success": True,
        "data": {
            "items": memories,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
        "governance": {
            "identity_filtered": True,
            "current_identity": current_identity,
        },
    }


@router.get("/items/{memory_id}", response_model=dict)
async def get_memory(memory_id: str):
    """
    Get memory item details.
    
    GOUVERNANCE: Checks identity access.
    """
    current_identity = "identity_001"
    memory = next((m for m in MOCK_MEMORIES if m["id"] == memory_id), None)
    
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    # GOUVERNANCE: Block cross-identity access
    if memory["identity_id"] != current_identity:
        raise HTTPException(
            status_code=403, 
            detail="Cross-identity access blocked",
            headers={"X-Governance-Rule": "identity-isolation"}
        )
    
    return {
        "success": True,
        "data": memory,
    }


@router.post("/items", response_model=dict)
async def create_memory(data: MemoryItemCreate):
    """
    Create memory item.
    
    GOUVERNANCE: Logs creation in audit trail.
    """
    if data.memory_type not in MEMORY_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid memory type. Must be one of: {MEMORY_TYPES}")
    if data.memory_category not in MEMORY_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid memory category. Must be one of: {MEMORY_CATEGORIES}")
    
    memory = {
        "id": f"mem_{len(MOCK_MEMORIES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "memory_type": data.memory_type,
        "memory_category": data.memory_category,
        "content": data.content,
        "metadata": data.metadata,
        "dataspace_id": data.dataspace_id,
        "thread_id": data.thread_id,
        "status": "active",
        "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat() if data.memory_type == "short_term" else None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_MEMORIES.append(memory)
    
    # Audit log
    audit_entry = {
        "id": f"audit_{len(MOCK_AUDIT_LOG) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "action_type": "create",
        "resource_type": "memory",
        "resource_id": memory["id"],
        "action_details": {"memory_type": data.memory_type, "category": data.memory_category},
        "created_at": datetime.utcnow().isoformat(),
    }
    MOCK_AUDIT_LOG.append(audit_entry)
    
    return {
        "success": True,
        "data": memory,
        "message": "Mémoire créée",
        "governance": {
            "audit_logged": True,
            "audit_id": audit_entry["id"],
        },
    }


@router.patch("/items/{memory_id}", response_model=dict)
async def update_memory(memory_id: str, data: MemoryItemUpdate):
    """
    Update memory item.
    
    GOUVERNANCE: Logs update in audit trail.
    """
    current_identity = "identity_001"
    memory = next((m for m in MOCK_MEMORIES if m["id"] == memory_id), None)
    
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    if memory["identity_id"] != current_identity:
        raise HTTPException(status_code=403, detail="Cross-identity access blocked")
    
    before_state = memory.copy()
    
    if data.content:
        memory["content"] = data.content
    if data.metadata:
        memory["metadata"].update(data.metadata)
    if data.status:
        if data.status not in MEMORY_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {MEMORY_STATUSES}")
        memory["status"] = data.status
    
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    # Audit log
    audit_entry = {
        "id": f"audit_{len(MOCK_AUDIT_LOG) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "action_type": "update",
        "resource_type": "memory",
        "resource_id": memory_id,
        "before_state": before_state,
        "after_state": memory,
        "created_at": datetime.utcnow().isoformat(),
    }
    MOCK_AUDIT_LOG.append(audit_entry)
    
    return {
        "success": True,
        "data": memory,
        "governance": {
            "audit_logged": True,
            "audit_id": audit_entry["id"],
        },
    }


@router.post("/items/{memory_id}/pin", response_model=dict)
async def pin_memory(memory_id: str):
    """
    Pin memory item (prevents expiration).
    """
    memory = next((m for m in MOCK_MEMORIES if m["id"] == memory_id), None)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    memory["status"] = "pinned"
    memory["expires_at"] = None
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": memory,
        "message": "Mémoire épinglée",
    }


@router.post("/items/{memory_id}/archive", response_model=dict)
async def archive_memory(memory_id: str):
    """
    Archive memory item.
    """
    memory = next((m for m in MOCK_MEMORIES if m["id"] == memory_id), None)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    
    memory["status"] = "archived"
    memory["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": memory,
        "message": "Mémoire archivée",
    }


# ============================================================================
# AUDIT LOG
# ============================================================================

@router.get("/audit", response_model=dict)
async def list_audit_log(
    action_type: Optional[str] = None,
    resource_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
):
    """
    List audit log entries.
    
    GOUVERNANCE: Audit log is append-only, never deleted.
    """
    logs = MOCK_AUDIT_LOG.copy()
    
    if action_type:
        logs = [l for l in logs if l.get("action_type") == action_type]
    if resource_type:
        logs = [l for l in logs if l.get("resource_type") == resource_type]
    
    total = len(logs)
    
    return {
        "success": True,
        "data": {
            "entries": logs,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
        "governance": {
            "append_only": True,
            "retention_days": 365,
        },
    }


@router.get("/audit/{entry_id}", response_model=dict)
async def get_audit_entry(entry_id: str):
    """
    Get audit log entry details.
    """
    entry = next((e for e in MOCK_AUDIT_LOG if e["id"] == entry_id), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Audit entry not found")
    
    return {
        "success": True,
        "data": entry,
    }


# ============================================================================
# ELEVATION REQUESTS
# ============================================================================

@router.get("/elevations", response_model=dict)
async def list_elevations(
    status: Optional[str] = "pending",
):
    """
    List elevation requests.
    """
    elevations = MOCK_ELEVATION_REQUESTS.copy()
    
    if status:
        elevations = [e for e in elevations if e.get("status") == status]
    
    return {
        "success": True,
        "data": {
            "requests": elevations,
            "total": len(elevations),
        },
    }


@router.post("/elevations", response_model=dict)
async def create_elevation_request(data: ElevationRequestCreate):
    """
    Create elevation request.
    
    GOUVERNANCE: Request for elevated permissions.
    """
    elevation = {
        "id": f"elev_{len(MOCK_ELEVATION_REQUESTS) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "requested_action": data.requested_action,
        "resource_type": data.resource_type,
        "resource_id": data.resource_id,
        "reason": data.reason,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
        "responded_at": None,
        "responded_by": None,
    }
    
    MOCK_ELEVATION_REQUESTS.append(elevation)
    
    return {
        "success": True,
        "data": elevation,
        "message": "Demande d'élévation créée",
    }


@router.post("/elevations/{elevation_id}/approve", response_model=dict)
async def approve_elevation(elevation_id: str):
    """
    Approve elevation request.
    
    GOUVERNANCE: Human approval required.
    """
    elevation = next((e for e in MOCK_ELEVATION_REQUESTS if e["id"] == elevation_id), None)
    if not elevation:
        raise HTTPException(status_code=404, detail="Elevation request not found")
    
    elevation["status"] = "approved"
    elevation["responded_at"] = datetime.utcnow().isoformat()
    elevation["responded_by"] = "user_001"
    
    return {
        "success": True,
        "data": elevation,
        "message": "Élévation approuvée",
    }


@router.post("/elevations/{elevation_id}/deny", response_model=dict)
async def deny_elevation(elevation_id: str, reason: str = ""):
    """
    Deny elevation request.
    """
    elevation = next((e for e in MOCK_ELEVATION_REQUESTS if e["id"] == elevation_id), None)
    if not elevation:
        raise HTTPException(status_code=404, detail="Elevation request not found")
    
    elevation["status"] = "denied"
    elevation["responded_at"] = datetime.utcnow().isoformat()
    elevation["responded_by"] = "user_001"
    elevation["denial_reason"] = reason
    
    return {
        "success": True,
        "data": elevation,
        "message": "Élévation refusée",
    }


# ============================================================================
# CROSS-IDENTITY BLOCKS
# ============================================================================

@router.get("/blocks", response_model=dict)
async def list_blocks():
    """
    List cross-identity blocks.
    """
    blocks = [
        {
            "id": "block_001",
            "user_id": "user_001",
            "source_identity_id": "identity_001",
            "target_identity_id": "identity_002",
            "blocked_action": "read",
            "blocked_resource_type": "memory",
            "block_reason": "Identity isolation policy",
            "blocked_at": "2026-01-01T00:00:00Z",
        },
    ]
    
    return {
        "success": True,
        "data": {
            "blocks": blocks,
            "total": len(blocks),
        },
        "governance": {
            "policy": "identity_isolation",
            "enforcement": "strict",
        },
    }


# ============================================================================
# MEMORY STATS
# ============================================================================

@router.get("/stats", response_model=dict)
async def get_memory_stats():
    """
    Get memory statistics.
    """
    current_identity = "identity_001"
    user_memories = [m for m in MOCK_MEMORIES if m["identity_id"] == current_identity]
    
    stats = {
        "total_items": len(user_memories),
        "by_type": {},
        "by_category": {},
        "by_status": {},
        "expiring_soon": 0,
    }
    
    for m in user_memories:
        # By type
        t = m["memory_type"]
        stats["by_type"][t] = stats["by_type"].get(t, 0) + 1
        
        # By category
        c = m["memory_category"]
        stats["by_category"][c] = stats["by_category"].get(c, 0) + 1
        
        # By status
        s = m["status"]
        stats["by_status"][s] = stats["by_status"].get(s, 0) + 1
        
        # Expiring soon
        if m.get("expires_at"):
            exp = datetime.fromisoformat(m["expires_at"].replace("Z", "+00:00"))
            if exp < datetime.now().astimezone() + timedelta(days=3):
                stats["expiring_soon"] += 1
    
    return {
        "success": True,
        "data": stats,
    }
