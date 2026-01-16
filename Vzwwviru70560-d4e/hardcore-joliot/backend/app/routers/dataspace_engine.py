"""
CHE·NU™ V76 — DATASPACE ENGINE ROUTER
======================================
Gestion des DataSpaces (espaces de données par Thread/Sphère).

19 Endpoints pour:
- CRUD DataSpaces
- Gestion des fichiers
- Métadonnées et tags
- Recherche et filtres

R&D Rules Compliance:
- Rule #1: Human gates sur delete/export
- Rule #3: Identity boundary enforcement
- Rule #6: Traçabilité complète
"""

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("chenu.routers.dataspace_engine")

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class DataSpaceType(str, Enum):
    THREAD = "thread"
    SPHERE = "sphere"
    PROJECT = "project"
    SHARED = "shared"


class DataSpaceStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    LOCKED = "locked"


class DataSpaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: DataSpaceType = DataSpaceType.THREAD
    description: Optional[str] = None
    thread_id: Optional[UUID] = None
    sphere_id: Optional[UUID] = None
    metadata: Optional[Dict[str, Any]] = None


class DataSpaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[DataSpaceStatus] = None


class DataSpaceResponse(BaseModel):
    id: UUID
    name: str
    type: DataSpaceType
    status: DataSpaceStatus
    description: Optional[str]
    thread_id: Optional[UUID]
    sphere_id: Optional[UUID]
    owner_id: UUID
    file_count: int
    total_size_bytes: int
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    created_by: UUID


class FileMetadata(BaseModel):
    id: UUID
    name: str
    mime_type: str
    size_bytes: int
    dataspace_id: UUID
    path: str
    tags: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    created_by: UUID


class CheckpointResponse(BaseModel):
    """R&D Rule #1: Human gate checkpoint."""
    checkpoint_id: UUID
    action: str
    resource_id: UUID
    status: str = "awaiting_approval"
    message: str
    expires_at: datetime


# ============================================================================
# MOCK DATABASE (Replace with real DB in production)
# ============================================================================

_dataspaces_db: Dict[str, Dict] = {}
_files_db: Dict[str, Dict] = {}


def get_current_user_id() -> UUID:
    """Mock: Get current authenticated user ID."""
    return UUID("00000000-0000-0000-0000-000000000001")


# ============================================================================
# DATASPACE CRUD ENDPOINTS (1-6)
# ============================================================================

@router.get("/", response_model=List[DataSpaceResponse])
async def list_dataspaces(
    type: Optional[DataSpaceType] = None,
    status: Optional[DataSpaceStatus] = None,
    thread_id: Optional[UUID] = None,
    sphere_id: Optional[UUID] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List all DataSpaces for current user.
    Supports filtering by type, status, thread, or sphere.
    """
    user_id = get_current_user_id()
    
    results = []
    for ds in _dataspaces_db.values():
        if ds["owner_id"] != str(user_id):
            continue
        if type and ds["type"] != type:
            continue
        if status and ds["status"] != status:
            continue
        if thread_id and ds.get("thread_id") != str(thread_id):
            continue
        if sphere_id and ds.get("sphere_id") != str(sphere_id):
            continue
        results.append(ds)
    
    return results[offset:offset + limit]


@router.post("/", response_model=DataSpaceResponse, status_code=201)
async def create_dataspace(data: DataSpaceCreate):
    """Create a new DataSpace."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    dataspace = {
        "id": str(uuid4()),
        "name": data.name,
        "type": data.type,
        "status": DataSpaceStatus.ACTIVE,
        "description": data.description,
        "thread_id": str(data.thread_id) if data.thread_id else None,
        "sphere_id": str(data.sphere_id) if data.sphere_id else None,
        "owner_id": str(user_id),
        "file_count": 0,
        "total_size_bytes": 0,
        "metadata": data.metadata or {},
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "created_by": str(user_id)
    }
    
    _dataspaces_db[dataspace["id"]] = dataspace
    logger.info(f"DataSpace created: {dataspace['id']} by user {user_id}")
    
    return dataspace


@router.get("/{dataspace_id}", response_model=DataSpaceResponse)
async def get_dataspace(dataspace_id: UUID):
    """Get a specific DataSpace by ID."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    # R&D Rule #3: Identity boundary
    if ds["owner_id"] != str(user_id):
        raise HTTPException(
            status_code=403, 
            detail="Identity boundary violation: DataSpace belongs to another user"
        )
    
    return ds


@router.put("/{dataspace_id}", response_model=DataSpaceResponse)
async def update_dataspace(dataspace_id: UUID, data: DataSpaceUpdate):
    """Update a DataSpace."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # Update fields
    if data.name is not None:
        ds["name"] = data.name
    if data.description is not None:
        ds["description"] = data.description
    if data.metadata is not None:
        ds["metadata"].update(data.metadata)
    if data.status is not None:
        ds["status"] = data.status
    
    ds["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"DataSpace updated: {dataspace_id}")
    return ds


@router.delete("/{dataspace_id}", response_model=CheckpointResponse)
async def delete_dataspace(dataspace_id: UUID):
    """
    Delete a DataSpace.
    R&D Rule #1: Returns checkpoint for human approval.
    """
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # R&D Rule #1: Human gate for destructive action
    checkpoint = CheckpointResponse(
        checkpoint_id=uuid4(),
        action="delete_dataspace",
        resource_id=dataspace_id,
        status="awaiting_approval",
        message=f"Confirm deletion of DataSpace '{ds['name']}' with {ds['file_count']} files",
        expires_at=datetime.utcnow()
    )
    
    logger.warning(f"CHECKPOINT: Delete DataSpace {dataspace_id} requires approval")
    
    raise HTTPException(
        status_code=423,
        detail=checkpoint.dict()
    )


@router.post("/{dataspace_id}/archive", response_model=DataSpaceResponse)
async def archive_dataspace(dataspace_id: UUID):
    """Archive a DataSpace (soft delete)."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    ds["status"] = DataSpaceStatus.ARCHIVED
    ds["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"DataSpace archived: {dataspace_id}")
    return ds


# ============================================================================
# FILE MANAGEMENT ENDPOINTS (7-13)
# ============================================================================

@router.get("/{dataspace_id}/files", response_model=List[FileMetadata])
async def list_files(
    dataspace_id: UUID,
    path: Optional[str] = "/",
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """List files in a DataSpace."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    files = [
        f for f in _files_db.values()
        if f["dataspace_id"] == str(dataspace_id)
        and f["path"].startswith(path)
    ]
    
    return files[offset:offset + limit]


@router.post("/{dataspace_id}/files", response_model=FileMetadata, status_code=201)
async def upload_file(
    dataspace_id: UUID,
    file: UploadFile = File(...),
    path: str = Query("/", description="Target path in DataSpace"),
    tags: List[str] = Query(default=[])
):
    """Upload a file to DataSpace."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # Read file content (in production, stream to storage)
    content = await file.read()
    size = len(content)
    
    file_meta = {
        "id": str(uuid4()),
        "name": file.filename,
        "mime_type": file.content_type or "application/octet-stream",
        "size_bytes": size,
        "dataspace_id": str(dataspace_id),
        "path": path,
        "tags": tags,
        "metadata": {},
        "created_at": datetime.utcnow().isoformat(),
        "created_by": str(user_id)
    }
    
    _files_db[file_meta["id"]] = file_meta
    
    # Update DataSpace stats
    ds["file_count"] += 1
    ds["total_size_bytes"] += size
    ds["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"File uploaded: {file.filename} to DataSpace {dataspace_id}")
    return file_meta


@router.get("/{dataspace_id}/files/{file_id}", response_model=FileMetadata)
async def get_file_metadata(dataspace_id: UUID, file_id: UUID):
    """Get file metadata."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    return file


@router.delete("/{dataspace_id}/files/{file_id}", response_model=CheckpointResponse)
async def delete_file(dataspace_id: UUID, file_id: UUID):
    """
    Delete a file.
    R&D Rule #1: Returns checkpoint for human approval.
    """
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # R&D Rule #1: Human gate
    checkpoint = CheckpointResponse(
        checkpoint_id=uuid4(),
        action="delete_file",
        resource_id=file_id,
        status="awaiting_approval",
        message=f"Confirm deletion of file '{file['name']}'",
        expires_at=datetime.utcnow()
    )
    
    raise HTTPException(status_code=423, detail=checkpoint.dict())


@router.post("/{dataspace_id}/files/{file_id}/move")
async def move_file(
    dataspace_id: UUID, 
    file_id: UUID,
    new_path: str = Query(...),
    new_dataspace_id: Optional[UUID] = None
):
    """Move file to new path or DataSpace."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # Update path
    file["path"] = new_path
    
    if new_dataspace_id:
        new_ds = _dataspaces_db.get(str(new_dataspace_id))
        if not new_ds or new_ds["owner_id"] != str(user_id):
            raise HTTPException(status_code=403, detail="Target DataSpace not accessible")
        
        file["dataspace_id"] = str(new_dataspace_id)
        ds["file_count"] -= 1
        new_ds["file_count"] += 1
    
    logger.info(f"File moved: {file_id} to {new_path}")
    return {"status": "moved", "new_path": new_path}


@router.post("/{dataspace_id}/files/{file_id}/copy")
async def copy_file(
    dataspace_id: UUID,
    file_id: UUID,
    target_path: str = Query(...),
    target_dataspace_id: Optional[UUID] = None
):
    """Copy file to new location."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    target_ds_id = str(target_dataspace_id) if target_dataspace_id else str(dataspace_id)
    
    new_file = {
        **file,
        "id": str(uuid4()),
        "path": target_path,
        "dataspace_id": target_ds_id,
        "created_at": datetime.utcnow().isoformat()
    }
    
    _files_db[new_file["id"]] = new_file
    
    target_ds = _dataspaces_db.get(target_ds_id)
    target_ds["file_count"] += 1
    target_ds["total_size_bytes"] += file["size_bytes"]
    
    logger.info(f"File copied: {file_id} to {target_path}")
    return {"status": "copied", "new_file_id": new_file["id"]}


# ============================================================================
# SEARCH & METADATA ENDPOINTS (14-17)
# ============================================================================

@router.get("/{dataspace_id}/search")
async def search_files(
    dataspace_id: UUID,
    q: str = Query(..., min_length=1),
    tags: Optional[List[str]] = Query(None),
    mime_type: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200)
):
    """Search files in DataSpace."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    results = []
    for file in _files_db.values():
        if file["dataspace_id"] != str(dataspace_id):
            continue
        
        # Simple search in name
        if q.lower() not in file["name"].lower():
            continue
        
        # Filter by tags
        if tags and not set(tags).issubset(set(file["tags"])):
            continue
        
        # Filter by mime type
        if mime_type and file["mime_type"] != mime_type:
            continue
        
        results.append(file)
        
        if len(results) >= limit:
            break
    
    return {"results": results, "total": len(results)}


@router.get("/{dataspace_id}/stats")
async def get_dataspace_stats(dataspace_id: UUID):
    """Get DataSpace statistics."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    files = [f for f in _files_db.values() if f["dataspace_id"] == str(dataspace_id)]
    
    # Calculate stats
    mime_types = {}
    for f in files:
        mime_types[f["mime_type"]] = mime_types.get(f["mime_type"], 0) + 1
    
    return {
        "dataspace_id": str(dataspace_id),
        "file_count": len(files),
        "total_size_bytes": sum(f["size_bytes"] for f in files),
        "mime_type_distribution": mime_types,
        "last_modified": ds["updated_at"]
    }


@router.put("/{dataspace_id}/files/{file_id}/tags")
async def update_file_tags(
    dataspace_id: UUID,
    file_id: UUID,
    tags: List[str]
):
    """Update file tags."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    file["tags"] = tags
    return {"status": "updated", "tags": tags}


@router.put("/{dataspace_id}/files/{file_id}/metadata")
async def update_file_metadata(
    dataspace_id: UUID,
    file_id: UUID,
    metadata: Dict[str, Any]
):
    """Update file custom metadata."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file or file["dataspace_id"] != str(dataspace_id):
        raise HTTPException(status_code=404, detail="File not found")
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    file["metadata"].update(metadata)
    return {"status": "updated", "metadata": file["metadata"]}


# ============================================================================
# EXPORT & SYNC ENDPOINTS (18-19)
# ============================================================================

@router.post("/{dataspace_id}/export", response_model=CheckpointResponse)
async def export_dataspace(
    dataspace_id: UUID,
    format: str = Query("zip", regex="^(zip|tar|json)$")
):
    """
    Export entire DataSpace.
    R&D Rule #1: Returns checkpoint for human approval.
    """
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    if not ds:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # R&D Rule #1: Human gate for data export
    checkpoint = CheckpointResponse(
        checkpoint_id=uuid4(),
        action="export_dataspace",
        resource_id=dataspace_id,
        status="awaiting_approval",
        message=f"Confirm export of DataSpace '{ds['name']}' ({ds['file_count']} files, {ds['total_size_bytes']} bytes) as {format}",
        expires_at=datetime.utcnow()
    )
    
    logger.warning(f"CHECKPOINT: Export DataSpace {dataspace_id} requires approval")
    raise HTTPException(status_code=423, detail=checkpoint.dict())


@router.post("/{dataspace_id}/sync")
async def sync_dataspace(
    dataspace_id: UUID,
    target_id: UUID
):
    """Sync DataSpace with another (bidirectional)."""
    user_id = get_current_user_id()
    
    ds = _dataspaces_db.get(str(dataspace_id))
    target = _dataspaces_db.get(str(target_id))
    
    if not ds or not target:
        raise HTTPException(status_code=404, detail="DataSpace not found")
    
    if ds["owner_id"] != str(user_id) or target["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # TODO: Implement actual sync logic
    logger.info(f"DataSpace sync initiated: {dataspace_id} <-> {target_id}")
    
    return {
        "status": "sync_started",
        "source": str(dataspace_id),
        "target": str(target_id),
        "sync_id": str(uuid4())
    }
