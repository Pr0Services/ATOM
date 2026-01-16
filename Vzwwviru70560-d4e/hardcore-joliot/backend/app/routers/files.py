"""
CHE·NU™ V76 — FILES ROUTER
===========================
Gestion centralisée des fichiers uploadés.

Supporte:
- Upload/Download
- Versioning
- Metadata
- Recherche
- Liens avec Threads/DataSpaces

R&D Rules Compliance:
- Rule #1: Human gates sur delete
- Rule #3: Identity boundary sur tous fichiers
- Rule #6: Traçabilité complète
"""

from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
import logging
import io

logger = logging.getLogger("chenu.routers.files")

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class FileType(str, Enum):
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    CODE = "code"
    OTHER = "other"


class FileStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class FileMetadata(BaseModel):
    id: UUID
    name: str
    original_name: str
    mime_type: str
    size_bytes: int
    file_type: FileType
    status: FileStatus
    checksum: Optional[str]
    
    # Links
    thread_id: Optional[UUID]
    dataspace_id: Optional[UUID]
    sphere_id: Optional[UUID]
    
    # Versioning
    version: int = 1
    parent_version_id: Optional[UUID]
    
    # Metadata
    tags: List[str] = []
    custom_metadata: Dict[str, Any] = {}
    
    # Audit
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID


class FileUploadResponse(BaseModel):
    file_id: UUID
    name: str
    size_bytes: int
    status: FileStatus
    upload_url: Optional[str]


class CheckpointResponse(BaseModel):
    checkpoint_id: UUID
    action: str
    resource_id: UUID
    status: str = "awaiting_approval"
    message: str


# ============================================================================
# MOCK DATABASE
# ============================================================================

_files_db: Dict[str, Dict] = {}
_file_contents: Dict[str, bytes] = {}  # Mock storage


def get_current_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def _detect_file_type(mime_type: str) -> FileType:
    """Detect file type from MIME type."""
    if mime_type.startswith("image/"):
        return FileType.IMAGE
    elif mime_type.startswith("video/"):
        return FileType.VIDEO
    elif mime_type.startswith("audio/"):
        return FileType.AUDIO
    elif mime_type in ["application/pdf", "application/msword", 
                       "application/vnd.openxmlformats-officedocument"]:
        return FileType.DOCUMENT
    elif mime_type in ["application/zip", "application/x-tar", "application/gzip"]:
        return FileType.ARCHIVE
    elif mime_type in ["text/plain", "application/json", "text/html", "text/css",
                       "application/javascript", "text/x-python"]:
        return FileType.CODE
    else:
        return FileType.OTHER


# ============================================================================
# UPLOAD ENDPOINTS (1-3)
# ============================================================================

@router.post("/upload", response_model=FileUploadResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    thread_id: Optional[UUID] = Form(None),
    dataspace_id: Optional[UUID] = Form(None),
    sphere_id: Optional[UUID] = Form(None),
    tags: str = Form("")  # Comma-separated
):
    """
    Upload a file.
    File is associated with Thread, DataSpace, or Sphere.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    # Read file content
    content = await file.read()
    size = len(content)
    
    # Detect file type
    mime_type = file.content_type or "application/octet-stream"
    file_type = _detect_file_type(mime_type)
    
    # Create file record
    file_id = uuid4()
    file_record = {
        "id": str(file_id),
        "name": file.filename,
        "original_name": file.filename,
        "mime_type": mime_type,
        "size_bytes": size,
        "file_type": file_type,
        "status": FileStatus.READY,
        "checksum": None,  # TODO: Calculate hash
        
        "thread_id": str(thread_id) if thread_id else None,
        "dataspace_id": str(dataspace_id) if dataspace_id else None,
        "sphere_id": str(sphere_id) if sphere_id else None,
        
        "version": 1,
        "parent_version_id": None,
        
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "custom_metadata": {},
        
        "owner_id": str(user_id),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "created_by": str(user_id)
    }
    
    _files_db[str(file_id)] = file_record
    _file_contents[str(file_id)] = content
    
    logger.info(f"File uploaded: {file_id} - {file.filename} ({size} bytes)")
    
    return FileUploadResponse(
        file_id=file_id,
        name=file.filename,
        size_bytes=size,
        status=FileStatus.READY,
        upload_url=None
    )


@router.post("/upload/multipart/init")
async def init_multipart_upload(
    filename: str,
    total_size: int,
    mime_type: str = "application/octet-stream"
):
    """
    Initialize multipart upload for large files.
    Returns upload_id for subsequent parts.
    """
    user_id = get_current_user_id()
    upload_id = uuid4()
    
    # TODO: Initialize multipart upload in storage
    
    return {
        "upload_id": str(upload_id),
        "filename": filename,
        "total_size": total_size,
        "part_size_recommended": 5 * 1024 * 1024,  # 5MB
        "expires_at": datetime.utcnow().isoformat()
    }


@router.post("/upload/multipart/{upload_id}/part")
async def upload_part(
    upload_id: UUID,
    part_number: int,
    file: UploadFile = File(...)
):
    """Upload a part of multipart upload."""
    content = await file.read()
    
    # TODO: Store part
    
    return {
        "upload_id": str(upload_id),
        "part_number": part_number,
        "size": len(content),
        "status": "received"
    }


# ============================================================================
# FILE CRUD (4-8)
# ============================================================================

@router.get("/", response_model=List[FileMetadata])
async def list_files(
    thread_id: Optional[UUID] = None,
    dataspace_id: Optional[UUID] = None,
    sphere_id: Optional[UUID] = None,
    file_type: Optional[FileType] = None,
    tags: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """List files for current user."""
    user_id = get_current_user_id()
    
    files = [f for f in _files_db.values() if f["owner_id"] == str(user_id)]
    
    if thread_id:
        files = [f for f in files if f.get("thread_id") == str(thread_id)]
    if dataspace_id:
        files = [f for f in files if f.get("dataspace_id") == str(dataspace_id)]
    if sphere_id:
        files = [f for f in files if f.get("sphere_id") == str(sphere_id)]
    if file_type:
        files = [f for f in files if f["file_type"] == file_type]
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        files = [f for f in files if any(t in f["tags"] for t in tag_list)]
    
    return sorted(files, key=lambda x: x["created_at"], reverse=True)[offset:offset + limit]


@router.get("/{file_id}", response_model=FileMetadata)
async def get_file_metadata(file_id: UUID):
    """Get file metadata."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    return file


@router.get("/{file_id}/download")
async def download_file(file_id: UUID):
    """Download file content."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    content = _file_contents.get(str(file_id))
    if not content:
        raise HTTPException(status_code=404, detail="File content not found")
    
    return StreamingResponse(
        io.BytesIO(content),
        media_type=file["mime_type"],
        headers={
            "Content-Disposition": f'attachment; filename="{file["name"]}"'
        }
    )


@router.put("/{file_id}", response_model=FileMetadata)
async def update_file_metadata(
    file_id: UUID,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    custom_metadata: Optional[Dict[str, Any]] = None,
    thread_id: Optional[UUID] = None,
    dataspace_id: Optional[UUID] = None
):
    """Update file metadata."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    if name:
        file["name"] = name
    if tags is not None:
        file["tags"] = tags
    if custom_metadata is not None:
        file["custom_metadata"].update(custom_metadata)
    if thread_id:
        file["thread_id"] = str(thread_id)
    if dataspace_id:
        file["dataspace_id"] = str(dataspace_id)
    
    file["updated_at"] = datetime.utcnow().isoformat()
    
    return file


@router.delete("/{file_id}", response_model=CheckpointResponse)
async def delete_file(file_id: UUID):
    """
    Delete a file.
    R&D Rule #1: Requires human approval.
    """
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # R&D Rule #1: Human gate
    checkpoint = CheckpointResponse(
        checkpoint_id=uuid4(),
        action="delete_file",
        resource_id=file_id,
        status="awaiting_approval",
        message=f"Confirm deletion of file '{file['name']}' ({file['size_bytes']} bytes)"
    )
    
    logger.warning(f"CHECKPOINT: Delete file {file_id}")
    raise HTTPException(status_code=423, detail=checkpoint.dict())


# ============================================================================
# VERSIONING (9-10)
# ============================================================================

@router.post("/{file_id}/versions", response_model=FileMetadata, status_code=201)
async def create_new_version(
    file_id: UUID,
    file: UploadFile = File(...)
):
    """
    Create a new version of a file.
    Previous version is preserved.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    original = _files_db.get(str(file_id))
    if not original:
        raise HTTPException(status_code=404, detail="File not found")
    
    if original["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # Read new content
    content = await file.read()
    size = len(content)
    
    # Create new version
    new_id = uuid4()
    new_file = {
        **original,
        "id": str(new_id),
        "size_bytes": size,
        "version": original["version"] + 1,
        "parent_version_id": str(file_id),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    
    _files_db[str(new_id)] = new_file
    _file_contents[str(new_id)] = content
    
    logger.info(f"New version created: {new_id} (v{new_file['version']}) of {file_id}")
    
    return new_file


@router.get("/{file_id}/versions", response_model=List[FileMetadata])
async def list_file_versions(file_id: UUID):
    """List all versions of a file."""
    user_id = get_current_user_id()
    
    file = _files_db.get(str(file_id))
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file["owner_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    # Find all versions (forward and backward)
    versions = [file]
    
    # Look for parent versions
    current = file
    while current.get("parent_version_id"):
        parent = _files_db.get(current["parent_version_id"])
        if parent:
            versions.append(parent)
            current = parent
        else:
            break
    
    # Look for child versions
    for f in _files_db.values():
        if f.get("parent_version_id") == str(file_id):
            versions.append(f)
    
    return sorted(versions, key=lambda x: x["version"])


# ============================================================================
# SEARCH (11)
# ============================================================================

@router.get("/search")
async def search_files(
    q: str = Query(..., min_length=1),
    file_type: Optional[FileType] = None,
    sphere_id: Optional[UUID] = None,
    limit: int = Query(50, ge=1, le=200)
):
    """Search files by name, tags, or metadata."""
    user_id = get_current_user_id()
    
    files = [f for f in _files_db.values() if f["owner_id"] == str(user_id)]
    
    if file_type:
        files = [f for f in files if f["file_type"] == file_type]
    if sphere_id:
        files = [f for f in files if f.get("sphere_id") == str(sphere_id)]
    
    # Simple search
    q_lower = q.lower()
    results = []
    
    for f in files:
        if q_lower in f["name"].lower():
            results.append({"file": f, "match": "name"})
        elif any(q_lower in tag.lower() for tag in f["tags"]):
            results.append({"file": f, "match": "tag"})
        elif q_lower in str(f["custom_metadata"]).lower():
            results.append({"file": f, "match": "metadata"})
        
        if len(results) >= limit:
            break
    
    return {
        "query": q,
        "results": results,
        "total": len(results)
    }


# ============================================================================
# STATS & HEALTH (12-13)
# ============================================================================

@router.get("/stats")
async def get_file_stats():
    """Get file storage statistics."""
    user_id = get_current_user_id()
    
    user_files = [f for f in _files_db.values() if f["owner_id"] == str(user_id)]
    
    total_size = sum(f["size_bytes"] for f in user_files)
    by_type = {}
    for f in user_files:
        ft = f["file_type"]
        if ft not in by_type:
            by_type[ft] = {"count": 0, "size": 0}
        by_type[ft]["count"] += 1
        by_type[ft]["size"] += f["size_bytes"]
    
    return {
        "total_files": len(user_files),
        "total_size_bytes": total_size,
        "by_type": by_type,
        "storage_quota_bytes": 10 * 1024 * 1024 * 1024,  # 10GB mock
        "storage_used_percent": round(total_size / (10 * 1024 * 1024 * 1024) * 100, 2)
    }


@router.get("/health")
async def files_health():
    """Files system health check."""
    return {
        "status": "healthy",
        "storage": "available",
        "upload_enabled": True,
        "max_file_size_bytes": 100 * 1024 * 1024,  # 100MB
        "supported_types": list(FileType)
    }
