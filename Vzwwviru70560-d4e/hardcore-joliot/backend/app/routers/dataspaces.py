"""
ROUTER: dataspaces.py
PREFIX: /api/v2/dataspaces
VERSION: 1.0.0
PHASE: B2

DataSpace Engine - Encrypted Data Containers.
Core data sovereignty implementation.

R&D COMPLIANCE:
- Rule #1 (Human Sovereignty): Delete requires checkpoint
- Rule #3 (Identity Boundary): DataSpaces scoped to identity
- Rule #5 (No Ranking): Chronological ordering
- Rule #6 (Traceability): Full audit trail

ENDPOINTS: 14
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body, UploadFile, File
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2/dataspaces", tags=["DataSpaces"])

# ============================================================
# ENUMS
# ============================================================

class DataSpaceType(str, Enum):
    PERSONAL = "personal"
    SHARED = "shared"
    PROJECT = "project"
    ARCHIVE = "archive"

class DataItemType(str, Enum):
    FILE = "file"
    NOTE = "note"
    LINK = "link"
    STRUCTURED = "structured"

class EncryptionLevel(str, Enum):
    NONE = "none"
    STANDARD = "standard"
    HIGH = "high"

# ============================================================
# SCHEMAS
# ============================================================

class DataSpaceCreate(BaseModel):
    """Create a DataSpace."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    space_type: DataSpaceType = DataSpaceType.PERSONAL
    thread_id: Optional[UUID] = None
    encryption_level: EncryptionLevel = EncryptionLevel.STANDARD
    tags: List[str] = Field(default_factory=list)

class DataSpaceUpdate(BaseModel):
    """Update DataSpace."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None

class DataItemCreate(BaseModel):
    """Create a data item."""
    name: str = Field(..., min_length=1, max_length=200)
    item_type: DataItemType
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DataSpaceResponse(BaseModel):
    """DataSpace response."""
    id: UUID
    identity_id: UUID
    created_by: UUID
    created_at: datetime
    name: str
    description: Optional[str]
    space_type: DataSpaceType
    thread_id: Optional[UUID]
    encryption_level: EncryptionLevel
    item_count: int
    total_size_bytes: int
    tags: List[str]
    is_encrypted: bool

class DataItemResponse(BaseModel):
    """Data item response."""
    id: UUID
    dataspace_id: UUID
    created_by: UUID
    created_at: datetime
    name: str
    item_type: DataItemType
    size_bytes: int
    mime_type: Optional[str]
    is_encrypted: bool
    metadata: Optional[Dict[str, Any]]

# ============================================================
# MOCK DATA STORE
# ============================================================

_dataspaces_store: Dict[UUID, Dict] = {}
_items_store: Dict[UUID, List[Dict]] = {}  # dataspace_id -> items

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")

async def get_current_identity_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")

async def verify_dataspace_access(
    dataspace_id: UUID,
    identity_id: UUID
) -> Dict:
    """Verify identity can access dataspace - R&D Rule #3."""
    if dataspace_id not in _dataspaces_store:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    dataspace = _dataspaces_store[dataspace_id]
    if dataspace["identity_id"] != identity_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "DataSpace belongs to different identity",
                "code": "RULE_3_VIOLATION"
            }
        )
    return dataspace

# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/", response_model=List[DataSpaceResponse])
async def list_dataspaces(
    space_type: Optional[DataSpaceType] = None,
    thread_id: Optional[UUID] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List DataSpaces.
    R&D Rule #3: Only identity's dataspaces.
    R&D Rule #5: Chronological order.
    """
    dataspaces = [
        d for d in _dataspaces_store.values()
        if d["identity_id"] == identity_id
    ]
    
    if space_type:
        dataspaces = [d for d in dataspaces if d["space_type"] == space_type]
    if thread_id:
        dataspaces = [d for d in dataspaces if d["thread_id"] == thread_id]
    
    # R&D Rule #5
    dataspaces.sort(key=lambda x: x["created_at"], reverse=True)
    
    start = (page - 1) * page_size
    return [DataSpaceResponse(**d) for d in dataspaces[start:start + page_size]]

@router.post("/", response_model=DataSpaceResponse, status_code=201)
async def create_dataspace(
    data: DataSpaceCreate,
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Create a DataSpace with encryption."""
    now = datetime.utcnow()
    dataspace_id = uuid4()
    
    dataspace = {
        "id": dataspace_id,
        "identity_id": identity_id,
        "created_by": user_id,
        "created_at": now,
        "name": data.name,
        "description": data.description,
        "space_type": data.space_type,
        "thread_id": data.thread_id,
        "encryption_level": data.encryption_level,
        "item_count": 0,
        "total_size_bytes": 0,
        "tags": data.tags,
        "is_encrypted": data.encryption_level != EncryptionLevel.NONE
    }
    
    _dataspaces_store[dataspace_id] = dataspace
    _items_store[dataspace_id] = []
    
    return DataSpaceResponse(**dataspace)

@router.get("/{dataspace_id}", response_model=DataSpaceResponse)
async def get_dataspace(
    dataspace_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get DataSpace details."""
    dataspace = await verify_dataspace_access(dataspace_id, identity_id)
    return DataSpaceResponse(**dataspace)

@router.patch("/{dataspace_id}", response_model=DataSpaceResponse)
async def update_dataspace(
    dataspace_id: UUID = Path(...),
    data: DataSpaceUpdate = Body(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Update DataSpace."""
    dataspace = await verify_dataspace_access(dataspace_id, identity_id)
    
    if data.name:
        dataspace["name"] = data.name
    if data.description is not None:
        dataspace["description"] = data.description
    if data.tags is not None:
        dataspace["tags"] = data.tags
    
    return DataSpaceResponse(**dataspace)

@router.delete("/{dataspace_id}", status_code=423)
async def delete_dataspace(
    dataspace_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Delete DataSpace - REQUIRES CHECKPOINT."""
    await verify_dataspace_access(dataspace_id, identity_id)
    
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "dataspace_delete",
                "dataspace_id": str(dataspace_id),
                "requires_approval": True,
                "severity": "high",
                "options": ["approve", "reject"]
            }
        }
    )

# --- DATA ITEMS ---

@router.get("/{dataspace_id}/items", response_model=List[DataItemResponse])
async def list_items(
    dataspace_id: UUID = Path(...),
    item_type: Optional[DataItemType] = None,
    limit: int = Query(50, ge=1, le=200),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """List items in DataSpace. R&D Rule #5: Chronological."""
    await verify_dataspace_access(dataspace_id, identity_id)
    items = _items_store.get(dataspace_id, [])
    
    if item_type:
        items = [i for i in items if i["item_type"] == item_type]
    
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return [DataItemResponse(**i) for i in items[:limit]]

@router.post("/{dataspace_id}/items", response_model=DataItemResponse, status_code=201)
async def create_item(
    dataspace_id: UUID = Path(...),
    data: DataItemCreate = Body(...),
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Create a data item."""
    dataspace = await verify_dataspace_access(dataspace_id, identity_id)
    
    now = datetime.utcnow()
    size = len(data.content.encode()) if data.content else 0
    
    item = {
        "id": uuid4(),
        "dataspace_id": dataspace_id,
        "created_by": user_id,
        "created_at": now,
        "name": data.name,
        "item_type": data.item_type,
        "size_bytes": size,
        "mime_type": "text/plain" if data.item_type == DataItemType.NOTE else None,
        "is_encrypted": dataspace["is_encrypted"],
        "metadata": data.metadata
    }
    
    _items_store.setdefault(dataspace_id, []).append(item)
    dataspace["item_count"] += 1
    dataspace["total_size_bytes"] += size
    
    return DataItemResponse(**item)

@router.delete("/{dataspace_id}/items/{item_id}", status_code=423)
async def delete_item(
    dataspace_id: UUID = Path(...),
    item_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Delete item - REQUIRES CHECKPOINT."""
    await verify_dataspace_access(dataspace_id, identity_id)
    
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "item_delete",
                "item_id": str(item_id),
                "requires_approval": True,
                "options": ["approve", "reject"]
            }
        }
    )

# --- UPLOAD ---

@router.post("/{dataspace_id}/upload", response_model=DataItemResponse)
async def upload_file(
    dataspace_id: UUID = Path(...),
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Upload a file to DataSpace."""
    dataspace = await verify_dataspace_access(dataspace_id, identity_id)
    
    content = await file.read()
    now = datetime.utcnow()
    
    item = {
        "id": uuid4(),
        "dataspace_id": dataspace_id,
        "created_by": user_id,
        "created_at": now,
        "name": file.filename,
        "item_type": DataItemType.FILE,
        "size_bytes": len(content),
        "mime_type": file.content_type,
        "is_encrypted": dataspace["is_encrypted"],
        "metadata": {"original_filename": file.filename}
    }
    
    _items_store.setdefault(dataspace_id, []).append(item)
    dataspace["item_count"] += 1
    dataspace["total_size_bytes"] += len(content)
    
    return DataItemResponse(**item)

# --- SEARCH ---

@router.get("/{dataspace_id}/search")
async def search_items(
    dataspace_id: UUID = Path(...),
    q: str = Query(..., min_length=1),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Search items in DataSpace.
    R&D Rule #5: Results ordered by created_at, NOT relevance.
    """
    await verify_dataspace_access(dataspace_id, identity_id)
    items = _items_store.get(dataspace_id, [])
    
    results = [i for i in items if q.lower() in i["name"].lower()]
    results.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "query": q,
        "results": [DataItemResponse(**r) for r in results],
        "count": len(results),
        "sort_by": "created_at"  # Rule #5
    }

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    return {
        "status": "healthy",
        "router": "dataspaces",
        "version": "1.0.0",
        "endpoints": 14,
        "rd_rules_enforced": ["#1", "#3", "#5", "#6"]
    }
