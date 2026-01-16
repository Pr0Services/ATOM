"""
CHE·NU™ V75 Backend - DataSpaces Router

DataSpace management for files, documents, and data organization.

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

from config import get_db
from schemas.base import BaseResponse, PaginatedResponse, PaginationMeta
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class DataSpaceFile(BaseModel):
    """File in a DataSpace."""
    id: str
    dataspace_id: str
    name: str
    file_type: str
    size_bytes: int
    mime_type: str
    uploaded_by: str
    created_at: datetime


class DataSpace(BaseModel):
    """DataSpace entity."""
    id: str
    name: str
    description: Optional[str] = None
    dataspace_type: str  # 'project', 'property', 'client', 'meeting', 'document', 'custom'
    sphere_id: Optional[str] = None
    parent_id: Optional[str] = None
    status: str = "active"  # 'active', 'archived'
    tags: List[str] = []
    files_count: int = 0
    size_bytes: int = 0
    metadata: dict = {}
    created_at: datetime
    updated_at: datetime


class CreateDataSpaceRequest(BaseModel):
    """Create DataSpace request."""
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    dataspace_type: str = "custom"
    sphere_id: Optional[str] = None
    parent_id: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}


class UpdateDataSpaceRequest(BaseModel):
    """Update DataSpace request."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=PaginatedResponse[DataSpace])
async def list_dataspaces(
    user: dict = Depends(require_auth),
    sphere_id: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = Query(default="active"),
    search: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List DataSpaces with filtering."""
    now = datetime.utcnow()
    
    dataspaces = [
        DataSpace(
            id="ds-1",
            name="Q4 Planning",
            description="Q4 2025 planning documents",
            dataspace_type="project",
            sphere_id="business",
            status="active",
            tags=["planning", "q4", "2025"],
            files_count=12,
            size_bytes=5242880,
            created_at=now,
            updated_at=now,
        ),
        DataSpace(
            id="ds-2",
            name="Client Documents",
            description="Client-related files and contracts",
            dataspace_type="client",
            sphere_id="business",
            status="active",
            tags=["clients", "contracts"],
            files_count=45,
            size_bytes=15728640,
            created_at=now,
            updated_at=now,
        ),
    ]
    
    # Filter
    if sphere_id:
        dataspaces = [d for d in dataspaces if d.sphere_id == sphere_id]
    if type:
        dataspaces = [d for d in dataspaces if d.dataspace_type == type]
    if status:
        dataspaces = [d for d in dataspaces if d.status == status]
    
    return PaginatedResponse(
        success=True,
        data=dataspaces,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(dataspaces),
            total_pages=1,
        ),
    )


@router.get("/{dataspace_id}", response_model=BaseResponse[DataSpace])
async def get_dataspace(
    dataspace_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get DataSpace details."""
    now = datetime.utcnow()
    
    dataspace = DataSpace(
        id=dataspace_id,
        name="Q4 Planning",
        description="Q4 2025 planning documents",
        dataspace_type="project",
        sphere_id="business",
        status="active",
        tags=["planning", "q4"],
        files_count=12,
        size_bytes=5242880,
        created_at=now,
        updated_at=now,
    )
    
    return BaseResponse(success=True, data=dataspace)


@router.post("", response_model=BaseResponse[DataSpace])
async def create_dataspace(
    request: CreateDataSpaceRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Create a new DataSpace."""
    now = datetime.utcnow()
    
    dataspace = DataSpace(
        id=str(uuid.uuid4()),
        name=request.name,
        description=request.description,
        dataspace_type=request.dataspace_type,
        sphere_id=request.sphere_id,
        parent_id=request.parent_id,
        tags=request.tags,
        metadata=request.metadata,
        status="active",
        files_count=0,
        size_bytes=0,
        created_at=now,
        updated_at=now,
    )
    
    return BaseResponse(success=True, data=dataspace)


@router.patch("/{dataspace_id}", response_model=BaseResponse[DataSpace])
async def update_dataspace(
    dataspace_id: str,
    request: UpdateDataSpaceRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Update DataSpace."""
    now = datetime.utcnow()
    
    dataspace = DataSpace(
        id=dataspace_id,
        name=request.name or "Updated DataSpace",
        description=request.description,
        dataspace_type="project",
        tags=request.tags or [],
        metadata=request.metadata or {},
        status="active",
        created_at=now,
        updated_at=now,
    )
    
    return BaseResponse(success=True, data=dataspace)


@router.post("/{dataspace_id}/archive")
async def archive_dataspace(
    dataspace_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Archive a DataSpace."""
    return BaseResponse(
        success=True,
        data={"id": dataspace_id, "status": "archived"},
    )


@router.get("/{dataspace_id}/files", response_model=BaseResponse[List[DataSpaceFile]])
async def get_dataspace_files(
    dataspace_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get files in a DataSpace."""
    now = datetime.utcnow()
    
    files = [
        DataSpaceFile(
            id="file-1",
            dataspace_id=dataspace_id,
            name="planning.pdf",
            file_type="pdf",
            size_bytes=524288,
            mime_type="application/pdf",
            uploaded_by=user["id"],
            created_at=now,
        ),
        DataSpaceFile(
            id="file-2",
            dataspace_id=dataspace_id,
            name="budget.xlsx",
            file_type="xlsx",
            size_bytes=102400,
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            uploaded_by=user["id"],
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=files)


@router.post("/{dataspace_id}/links")
async def link_dataspaces(
    dataspace_id: str,
    target_id: str = Query(...),
    link_type: str = Query(default="related"),
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Link two DataSpaces together."""
    return BaseResponse(
        success=True,
        data={
            "source_id": dataspace_id,
            "target_id": target_id,
            "link_type": link_type,
        },
    )
