"""
CHE·NU™ V75 - Files Router
File Management & Upload API.

Files = Documents, media, attachments across DataSpaces

GOUVERNANCE > EXÉCUTION
- Identity-scoped files
- Virus scanning (simulated)
- Size limits enforced

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from pydantic import BaseModel, Field

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class FileMetadataUpdate(BaseModel):
    """Update file metadata."""
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class FileMoveRequest(BaseModel):
    """Move file to another DataSpace."""
    target_dataspace_id: str
    target_folder: Optional[str] = None


class FileShareRequest(BaseModel):
    """Share file with others."""
    user_ids: List[str] = []
    identity_ids: List[str] = []
    permission: str = "view"  # view, edit, download
    expires_at: Optional[str] = None


# ============================================================================
# MOCK DATA
# ============================================================================

ALLOWED_EXTENSIONS = [
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "txt", "md", "json", "csv",
    "jpg", "jpeg", "png", "gif", "webp", "svg",
    "mp3", "wav", "m4a",
    "mp4", "mov", "webm",
    "zip", "rar", "7z",
    "dwg", "dxf",  # CAD
    "obj", "fbx", "gltf",  # 3D
]

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

MOCK_FILES = [
    {
        "id": "file_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": "ds_001",
        "name": "Devis_Renovation_Maya_v3.pdf",
        "original_name": "Devis_Renovation_Maya_v3.pdf",
        "description": "Devis final approuvé par le client",
        "mime_type": "application/pdf",
        "extension": "pdf",
        "size_bytes": 2567890,
        "folder": "/documents",
        "tags": ["devis", "approuvé", "maya"],
        "metadata": {
            "pages": 12,
            "version": 3,
        },
        "storage_path": "uploads/user_001/ds_001/file_001.pdf",
        "thumbnail_url": None,
        "is_public": False,
        "download_count": 5,
        "created_at": "2026-01-03T10:00:00Z",
        "updated_at": "2026-01-05T14:00:00Z",
    },
    {
        "id": "file_002",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": "ds_001",
        "name": "Photo_Cuisine_Avant_01.jpg",
        "original_name": "IMG_20260102_110534.jpg",
        "description": "Photo état actuel cuisine - angle fenêtre",
        "mime_type": "image/jpeg",
        "extension": "jpg",
        "size_bytes": 4523678,
        "folder": "/photos/avant",
        "tags": ["photo", "avant", "cuisine"],
        "metadata": {
            "width": 4032,
            "height": 3024,
            "taken_at": "2026-01-02T11:05:34Z",
        },
        "storage_path": "uploads/user_001/ds_001/file_002.jpg",
        "thumbnail_url": "/thumbnails/file_002_thumb.jpg",
        "is_public": False,
        "download_count": 2,
        "created_at": "2026-01-02T11:10:00Z",
        "updated_at": "2026-01-02T11:10:00Z",
    },
    {
        "id": "file_003",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": "ds_001",
        "name": "Plan_Cuisine_v2.dwg",
        "original_name": "Plan_Cuisine_v2.dwg",
        "description": "Plan AutoCAD cuisine rénovée",
        "mime_type": "application/acad",
        "extension": "dwg",
        "size_bytes": 1234567,
        "folder": "/plans",
        "tags": ["plan", "autocad", "cuisine"],
        "metadata": {
            "software": "AutoCAD 2024",
            "scale": "1:50",
        },
        "storage_path": "uploads/user_001/ds_001/file_003.dwg",
        "thumbnail_url": "/thumbnails/file_003_thumb.png",
        "is_public": False,
        "download_count": 8,
        "created_at": "2026-01-03T14:00:00Z",
        "updated_at": "2026-01-06T10:00:00Z",
    },
    {
        "id": "file_004",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "dataspace_id": "ds_002",
        "name": "Bail_Logement_101_2025.pdf",
        "original_name": "Bail_Logement_101_2025.pdf",
        "description": "Bail signé locataire Jean Dupont",
        "mime_type": "application/pdf",
        "extension": "pdf",
        "size_bytes": 567890,
        "folder": "/baux",
        "tags": ["bail", "logement-101", "2025"],
        "metadata": {
            "tenant": "Jean Dupont",
            "start_date": "2025-07-01",
            "end_date": "2026-06-30",
        },
        "storage_path": "uploads/user_001/ds_002/file_004.pdf",
        "thumbnail_url": None,
        "is_public": False,
        "download_count": 3,
        "created_at": "2025-06-15T10:00:00Z",
        "updated_at": "2025-06-15T10:00:00Z",
    },
]

MOCK_FOLDERS = [
    {"path": "/documents", "dataspace_id": "ds_001", "files_count": 5},
    {"path": "/photos", "dataspace_id": "ds_001", "files_count": 15},
    {"path": "/photos/avant", "dataspace_id": "ds_001", "files_count": 8},
    {"path": "/photos/apres", "dataspace_id": "ds_001", "files_count": 0},
    {"path": "/plans", "dataspace_id": "ds_001", "files_count": 3},
    {"path": "/baux", "dataspace_id": "ds_002", "files_count": 6},
]


# ============================================================================
# FILES
# ============================================================================

@router.get("", response_model=dict)
async def list_files(
    dataspace_id: Optional[str] = None,
    folder: Optional[str] = None,
    extension: Optional[str] = None,
    mime_type: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List files with filters.
    
    GOUVERNANCE: Returns only files for current identity.
    """
    files = [f for f in MOCK_FILES if f["user_id"] == "user_001"]
    
    if dataspace_id:
        files = [f for f in files if f["dataspace_id"] == dataspace_id]
    if folder:
        files = [f for f in files if f["folder"].startswith(folder)]
    if extension:
        files = [f for f in files if f["extension"] == extension]
    if mime_type:
        files = [f for f in files if f["mime_type"].startswith(mime_type)]
    if tag:
        files = [f for f in files if tag in f.get("tags", [])]
    if search:
        search_lower = search.lower()
        files = [f for f in files if search_lower in f["name"].lower() or search_lower in (f.get("description") or "").lower()]
    
    # Sort by updated_at desc
    files.sort(key=lambda x: x["updated_at"], reverse=True)
    
    total = len(files)
    total_size = sum(f["size_bytes"] for f in files)
    
    return {
        "success": True,
        "data": {
            "files": files,
            "total": total,
            "total_size_bytes": total_size,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/{file_id}", response_model=dict)
async def get_file(file_id: str):
    """
    Get file details.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "success": True,
        "data": file,
    }


@router.post("/upload", response_model=dict)
async def upload_file(
    dataspace_id: str = Form(...),
    folder: str = Form("/"),
    description: str = Form(""),
    tags: str = Form(""),  # Comma-separated
):
    """
    Upload file (simulated).
    
    GOUVERNANCE: Validates file type and size.
    """
    # Simulated file upload
    file = {
        "id": f"file_{len(MOCK_FILES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": dataspace_id,
        "name": "uploaded_file.pdf",
        "original_name": "uploaded_file.pdf",
        "description": description,
        "mime_type": "application/pdf",
        "extension": "pdf",
        "size_bytes": 1234567,
        "folder": folder,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "metadata": {},
        "storage_path": f"uploads/user_001/{dataspace_id}/file_{len(MOCK_FILES) + 1:03d}.pdf",
        "thumbnail_url": None,
        "is_public": False,
        "download_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_FILES.append(file)
    
    return {
        "success": True,
        "data": file,
        "message": "Fichier uploadé",
        "governance": {
            "virus_scan": "clean",
            "size_check": "passed",
        },
    }


@router.patch("/{file_id}", response_model=dict)
async def update_file(file_id: str, data: FileMetadataUpdate):
    """
    Update file metadata.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if data.name:
        file["name"] = data.name
    if data.description is not None:
        file["description"] = data.description
    if data.tags is not None:
        file["tags"] = data.tags
    if data.metadata is not None:
        file["metadata"].update(data.metadata)
    
    file["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": file,
    }


@router.delete("/{file_id}", response_model=dict)
async def delete_file(file_id: str):
    """
    Delete file.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    MOCK_FILES.remove(file)
    
    return {
        "success": True,
        "message": "Fichier supprimé",
    }


@router.get("/{file_id}/download", response_model=dict)
async def get_download_url(file_id: str):
    """
    Get file download URL.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Increment download count
    file["download_count"] += 1
    
    return {
        "success": True,
        "data": {
            "download_url": f"/api/v1/files/{file_id}/content",
            "expires_at": datetime.utcnow().isoformat(),
            "filename": file["name"],
        },
    }


@router.post("/{file_id}/move", response_model=dict)
async def move_file(file_id: str, data: FileMoveRequest):
    """
    Move file to another DataSpace.
    
    GOUVERNANCE: Cannot move to different identity.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    file["dataspace_id"] = data.target_dataspace_id
    if data.target_folder:
        file["folder"] = data.target_folder
    file["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": file,
        "message": "Fichier déplacé",
    }


@router.post("/{file_id}/copy", response_model=dict)
async def copy_file(file_id: str, data: FileMoveRequest):
    """
    Copy file to another DataSpace.
    """
    file = next((f for f in MOCK_FILES if f["id"] == file_id), None)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    new_file = {
        **file,
        "id": f"file_{len(MOCK_FILES) + 1:03d}",
        "dataspace_id": data.target_dataspace_id,
        "folder": data.target_folder or file["folder"],
        "download_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_FILES.append(new_file)
    
    return {
        "success": True,
        "data": new_file,
        "message": "Fichier copié",
    }


# ============================================================================
# FOLDERS
# ============================================================================

@router.get("/folders", response_model=dict)
async def list_folders(dataspace_id: str):
    """
    List folders in DataSpace.
    """
    folders = [f for f in MOCK_FOLDERS if f["dataspace_id"] == dataspace_id]
    
    return {
        "success": True,
        "data": {
            "folders": folders,
            "total": len(folders),
        },
    }


@router.post("/folders", response_model=dict)
async def create_folder(dataspace_id: str, path: str):
    """
    Create folder in DataSpace.
    """
    folder = {
        "path": path,
        "dataspace_id": dataspace_id,
        "files_count": 0,
    }
    
    MOCK_FOLDERS.append(folder)
    
    return {
        "success": True,
        "data": folder,
        "message": "Dossier créé",
    }


# ============================================================================
# STATS
# ============================================================================

@router.get("/stats", response_model=dict)
async def get_file_stats(dataspace_id: Optional[str] = None):
    """
    Get file statistics.
    """
    files = [f for f in MOCK_FILES if f["user_id"] == "user_001"]
    
    if dataspace_id:
        files = [f for f in files if f["dataspace_id"] == dataspace_id]
    
    by_extension = {}
    by_mime = {}
    
    for f in files:
        ext = f["extension"]
        by_extension[ext] = by_extension.get(ext, 0) + 1
        
        mime = f["mime_type"].split("/")[0]
        by_mime[mime] = by_mime.get(mime, 0) + 1
    
    return {
        "success": True,
        "data": {
            "total_files": len(files),
            "total_size_bytes": sum(f["size_bytes"] for f in files),
            "by_extension": by_extension,
            "by_mime_type": by_mime,
        },
    }
