"""
CHE·NU™ V75 - File Upload Service
Secure file handling with validation.

GOUVERNANCE > EXÉCUTION
- All uploads logged
- File access requires authentication
- Sensitive files require checkpoint approval

@version 75.0.0
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import os
import shutil
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Tuple

from fastapi import HTTPException, UploadFile
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class FileConfig:
    """File upload configuration."""
    
    # Base upload directory
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")
    
    # Max file size (50MB default)
    MAX_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 52428800))
    
    # Allowed extensions
    ALLOWED_EXTENSIONS = {
        # Documents
        "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
        "txt", "md", "csv", "json", "xml",
        # Images
        "png", "jpg", "jpeg", "gif", "webp", "svg",
        # Audio
        "mp3", "wav", "ogg", "m4a",
        # Video
        "mp4", "webm", "mov",
        # Archives
        "zip", "tar", "gz",
    }
    
    # Dangerous extensions (blocked)
    BLOCKED_EXTENSIONS = {
        "exe", "bat", "cmd", "sh", "ps1", "dll", "so",
        "php", "asp", "aspx", "jsp", "cgi",
    }
    
    # MIME type mapping
    MIME_TYPES = {
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
    }


# ============================================================================
# MODELS
# ============================================================================

class FileStatus(str, Enum):
    """File status."""
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"
    DELETED = "deleted"


class FileMetadata(BaseModel):
    """File metadata."""
    id: str
    original_name: str
    stored_name: str
    extension: str
    mime_type: str
    size_bytes: int
    checksum_sha256: str
    status: FileStatus
    uploaded_by: str
    dataspace_id: Optional[str] = None
    sphere_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    path: str
    url: Optional[str] = None
    metadata: Dict = {}


class UploadResult(BaseModel):
    """Upload result."""
    success: bool
    file_id: Optional[str] = None
    file: Optional[FileMetadata] = None
    error: Optional[str] = None


# ============================================================================
# FILE SERVICE
# ============================================================================

class FileService:
    """
    File upload and management service.
    
    Features:
    - Secure file validation
    - Checksum verification
    - Organized storage
    - Metadata tracking
    """
    
    def __init__(self, upload_dir: Optional[str] = None):
        self.upload_dir = Path(upload_dir or FileConfig.UPLOAD_DIR)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories."""
        dirs = [
            self.upload_dir,
            self.upload_dir / "documents",
            self.upload_dir / "images",
            self.upload_dir / "media",
            self.upload_dir / "temp",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # VALIDATION
    # ========================================================================
    
    def _get_extension(self, filename: str) -> str:
        """Extract file extension."""
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        return ext
    
    def _validate_extension(self, filename: str) -> Tuple[bool, str]:
        """Validate file extension."""
        ext = self._get_extension(filename)
        
        if ext in FileConfig.BLOCKED_EXTENSIONS:
            return False, f"Extension '{ext}' is blocked for security"
        
        if ext not in FileConfig.ALLOWED_EXTENSIONS:
            return False, f"Extension '{ext}' is not allowed"
        
        return True, ext
    
    def _validate_size(self, size: int) -> Tuple[bool, str]:
        """Validate file size."""
        if size > FileConfig.MAX_SIZE:
            max_mb = FileConfig.MAX_SIZE / (1024 * 1024)
            return False, f"File size exceeds maximum ({max_mb}MB)"
        return True, ""
    
    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _get_mime_type(self, filename: str, ext: str) -> str:
        """Determine MIME type."""
        # Try config first
        if ext in FileConfig.MIME_TYPES:
            return FileConfig.MIME_TYPES[ext]
        
        # Try mimetypes library
        mime, _ = mimetypes.guess_type(filename)
        return mime or "application/octet-stream"
    
    def _get_storage_category(self, ext: str) -> str:
        """Determine storage category."""
        if ext in {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "md", "csv", "json", "xml"}:
            return "documents"
        elif ext in {"png", "jpg", "jpeg", "gif", "webp", "svg"}:
            return "images"
        elif ext in {"mp3", "wav", "ogg", "m4a", "mp4", "webm", "mov"}:
            return "media"
        return "documents"
    
    # ========================================================================
    # UPLOAD
    # ========================================================================
    
    async def upload_file(
        self,
        file: UploadFile,
        user_id: str,
        dataspace_id: Optional[str] = None,
        sphere_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> UploadResult:
        """
        Upload a file.
        
        Steps:
        1. Validate extension
        2. Save to temp
        3. Validate size
        4. Compute checksum
        5. Move to final location
        6. Create metadata
        """
        try:
            # Validate extension
            valid, ext = self._validate_extension(file.filename or "unknown")
            if not valid:
                return UploadResult(success=False, error=ext)
            
            # Generate unique ID
            file_id = str(uuid.uuid4())
            stored_name = f"{file_id}.{ext}"
            
            # Save to temp first
            temp_path = self.upload_dir / "temp" / stored_name
            
            try:
                with open(temp_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
            except Exception as e:
                return UploadResult(success=False, error=f"Failed to save file: {e}")
            
            # Validate size
            size = temp_path.stat().st_size
            valid, error = self._validate_size(size)
            if not valid:
                temp_path.unlink(missing_ok=True)
                return UploadResult(success=False, error=error)
            
            # Compute checksum
            checksum = self._compute_checksum(temp_path)
            
            # Determine final location
            category = self._get_storage_category(ext)
            final_dir = self.upload_dir / category / datetime.utcnow().strftime("%Y/%m")
            final_dir.mkdir(parents=True, exist_ok=True)
            final_path = final_dir / stored_name
            
            # Move to final location
            shutil.move(str(temp_path), str(final_path))
            
            # Create metadata
            file_metadata = FileMetadata(
                id=file_id,
                original_name=file.filename or "unknown",
                stored_name=stored_name,
                extension=ext,
                mime_type=self._get_mime_type(file.filename or "", ext),
                size_bytes=size,
                checksum_sha256=checksum,
                status=FileStatus.READY,
                uploaded_by=user_id,
                dataspace_id=dataspace_id,
                sphere_id=sphere_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                path=str(final_path.relative_to(self.upload_dir)),
                metadata=metadata or {},
            )
            
            logger.info(f"File uploaded: {file_id} by {user_id}")
            
            return UploadResult(
                success=True,
                file_id=file_id,
                file=file_metadata,
            )
            
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return UploadResult(success=False, error=str(e))
    
    # ========================================================================
    # RETRIEVAL
    # ========================================================================
    
    def get_file_path(self, file_metadata: FileMetadata) -> Path:
        """Get full file path."""
        return self.upload_dir / file_metadata.path
    
    async def get_file_content(self, file_metadata: FileMetadata) -> bytes:
        """Get file content."""
        path = self.get_file_path(file_metadata)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(path, "rb") as f:
            return f.read()
    
    def verify_checksum(self, file_metadata: FileMetadata) -> bool:
        """Verify file integrity."""
        path = self.get_file_path(file_metadata)
        if not path.exists():
            return False
        
        current_checksum = self._compute_checksum(path)
        return current_checksum == file_metadata.checksum_sha256
    
    # ========================================================================
    # DELETION (Soft delete - APPEND ONLY philosophy)
    # ========================================================================
    
    async def soft_delete(self, file_id: str, user_id: str) -> bool:
        """
        Soft delete a file.
        
        NOTE: Following APPEND ONLY - file is marked deleted but not removed.
        Actual removal requires admin checkpoint approval.
        """
        # In real implementation, update database status to DELETED
        logger.info(f"File {file_id} marked for deletion by {user_id}")
        return True
    
    async def hard_delete(
        self,
        file_metadata: FileMetadata,
        approved_by: str,
        checkpoint_id: str,
    ) -> bool:
        """
        Hard delete a file (requires checkpoint approval).
        
        GOUVERNANCE > EXÉCUTION
        This requires explicit human approval via checkpoint.
        """
        if not checkpoint_id:
            raise HTTPException(
                status_code=403,
                detail="Hard delete requires checkpoint approval"
            )
        
        path = self.get_file_path(file_metadata)
        if path.exists():
            path.unlink()
            logger.info(
                f"File {file_metadata.id} deleted by {approved_by} "
                f"(checkpoint: {checkpoint_id})"
            )
            return True
        
        return False
    
    # ========================================================================
    # UTILITIES
    # ========================================================================
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics."""
        total_size = 0
        file_count = 0
        
        for root, _, files in os.walk(self.upload_dir):
            for f in files:
                path = Path(root) / f
                total_size += path.stat().st_size
                file_count += 1
        
        return {
            "total_files": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

file_service = FileService()
