"""
CHE·NU™ V75 — File Upload Routes
=================================
File upload with governance checkpoints
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4
import os
import hashlib
import mimetypes

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel

from app.core.auth import get_current_user

router = APIRouter(prefix="/files", tags=["Files"])

# =============================================================================
# MODELS
# =============================================================================

class FileResponse(BaseModel):
    id: str
    filename: str
    original_name: str
    mime_type: str
    size: int
    url: str
    thumbnail_url: Optional[str] = None
    thread_id: Optional[str] = None
    sphere_id: Optional[str] = None
    folder: Optional[str] = None
    tags: List[str] = []
    created_at: str
    created_by: str

# =============================================================================
# CONSTANTS
# =============================================================================

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {
    # Images
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml',
    # Documents
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    # Text
    'text/plain', 'text/markdown', 'text/csv',
    # Code
    'application/json', 'text/html', 'text/css', 'text/javascript',
    # Archives
    'application/zip',
    # Audio/Video
    'audio/mpeg', 'video/mp4',
}

# In-memory storage (replace with DB in production)
FILES_DB: dict[str, FileResponse] = {}

# =============================================================================
# HELPERS
# =============================================================================

def generate_filename(original: str) -> str:
    """Generate unique filename"""
    ext = os.path.splitext(original)[1]
    unique_id = uuid4().hex[:12]
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    return f"{timestamp}_{unique_id}{ext}"

def get_mime_type(filename: str, content_type: str) -> str:
    """Get MIME type"""
    if content_type and content_type != 'application/octet-stream':
        return content_type
    guessed = mimetypes.guess_type(filename)[0]
    return guessed or 'application/octet-stream'

# =============================================================================
# ROUTES
# =============================================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    thread_id: Optional[str] = Form(None),
    sphere_id: Optional[str] = Form(None),
    folder: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a file.
    
    Human Gate: Files are stored but require explicit access.
    Governance: Large files or sensitive types may trigger checkpoints.
    """
    # Validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum: {MAX_FILE_SIZE // 1024 // 1024} MB"
        )
    
    # Validate type
    mime_type = get_mime_type(file.filename or "file", file.content_type or "")
    if mime_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"File type not allowed: {mime_type}"
        )
    
    # Generate ID and filename
    file_id = str(uuid4())
    filename = generate_filename(file.filename or "file")
    
    # Parse tags
    tag_list = []
    if tags:
        try:
            import json
            tag_list = json.loads(tags)
        except:
            tag_list = []
    
    # Create file record
    file_record = FileResponse(
        id=file_id,
        filename=filename,
        original_name=file.filename or "file",
        mime_type=mime_type,
        size=len(content),
        url=f"/api/v1/files/{file_id}",
        thumbnail_url=f"/api/v1/files/{file_id}/thumbnail" if mime_type.startswith('image/') else None,
        thread_id=thread_id,
        sphere_id=sphere_id,
        folder=folder,
        tags=tag_list,
        created_at=datetime.utcnow().isoformat(),
        created_by=current_user.get("id", "unknown"),
    )
    
    # Store (in-memory for now)
    FILES_DB[file_id] = file_record
    
    # In production: save file to storage
    # os.makedirs(UPLOAD_DIR, exist_ok=True)
    # with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
    #     f.write(content)
    
    return {
        "success": True,
        "data": file_record.model_dump(),
    }


@router.get("")
async def list_files(
    thread_id: Optional[str] = None,
    sphere_id: Optional[str] = None,
    folder: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
):
    """List files with filters"""
    user_id = current_user.get("id", "unknown")
    
    # Filter files
    files = []
    for f in FILES_DB.values():
        # Identity boundary
        if f.created_by != user_id:
            continue
        # Filters
        if thread_id and f.thread_id != thread_id:
            continue
        if sphere_id and f.sphere_id != sphere_id:
            continue
        if folder and f.folder != folder:
            continue
        files.append(f)
    
    # Sort by date desc
    files.sort(key=lambda x: x.created_at, reverse=True)
    
    # Paginate
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "success": True,
        "data": {
            "files": [f.model_dump() for f in files[start:end]],
            "total": len(files),
            "page": page,
            "limit": limit,
        }
    }


@router.get("/{file_id}")
async def get_file(
    file_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get file details"""
    file = FILES_DB.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Identity boundary
    if file.created_by != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "success": True,
        "data": file.model_dump(),
    }


@router.get("/{file_id}/thumbnail")
async def get_thumbnail(
    file_id: str,
    size: str = "medium",
    current_user: dict = Depends(get_current_user),
):
    """Get file thumbnail (placeholder)"""
    file = FILES_DB.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Identity boundary
    if file.created_by != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # In production: return actual thumbnail
    return {
        "success": True,
        "data": {
            "url": f"/api/v1/files/{file_id}/thumbnail/{size}",
            "size": size,
        }
    }


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a file.
    
    Human Gate: Deletion requires explicit action.
    """
    file = FILES_DB.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Identity boundary
    if file.created_by != current_user.get("id"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Delete from storage
    del FILES_DB[file_id]
    
    # In production: also delete physical file
    
    return {
        "success": True,
        "message": "File deleted",
    }


# =============================================================================
# STATS
# =============================================================================

@router.get("/user/stats")
async def get_file_stats(
    current_user: dict = Depends(get_current_user),
):
    """Get file statistics for current user"""
    user_id = current_user.get("id", "unknown")
    
    user_files = [f for f in FILES_DB.values() if f.created_by == user_id]
    
    total_size = sum(f.size for f in user_files)
    by_type = {}
    for f in user_files:
        category = f.mime_type.split('/')[0]
        by_type[category] = by_type.get(category, 0) + 1
    
    return {
        "success": True,
        "data": {
            "total_files": len(user_files),
            "total_size": total_size,
            "by_type": by_type,
        }
    }
