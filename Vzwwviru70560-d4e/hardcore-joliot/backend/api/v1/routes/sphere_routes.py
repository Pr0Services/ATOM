"""
CHE·NU™ Sphere Routes

Sphere endpoints:
- GET /spheres - List user's spheres
- GET /spheres/{sphere_id} - Get sphere details
- PATCH /spheres/{sphere_id} - Update sphere
- GET /spheres/{sphere_id}/stats - Get statistics
- GET /spheres/{sphere_id}/bureau - List bureau sections
- GET /spheres/{sphere_id}/bureau/{section_type} - Get section content
- POST /spheres/{sphere_id}/bureau/quick_capture - Quick capture
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import (
    SphereNotFoundError,
    IdentityBoundaryError,
    ValidationError,
)
from backend.api.dependencies import get_current_user, CurrentUser
from backend.services.sphere.sphere_service import SphereService, get_sphere_service
from backend.models.sphere import BureauSectionType
from backend.schemas.sphere_schemas import (
    SphereTypeEnum,
    BureauSectionTypeEnum,
    SphereSummary,
    SphereDetail,
    SphereUpdate,
    SphereStats,
    SphereListResponse,
    BureauSectionResponse,
    BureauSectionListResponse,
    BureauSectionContent,
    QuickCaptureRequest,
    QuickCaptureResponse,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE LIST & DETAILS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/",
    response_model=SphereListResponse,
    summary="List user's spheres",
    description="""
    Get all 9 spheres for the current user.
    
    Each user has exactly 9 spheres (one of each type):
    - Personal, Business, Government, Creative, Community
    - Social, Entertainment, Team, Scholar
    
    **Identity Boundary:** Only returns spheres belonging to the authenticated user.
    """,
)
async def list_spheres(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereListResponse:
    """List all spheres for current user."""
    service = get_sphere_service(db, current_user.identity_id)
    
    spheres = await service.list_spheres()
    
    return SphereListResponse(
        spheres=spheres,
        total=len(spheres),
    )


@router.get(
    "/{sphere_id}",
    response_model=SphereDetail,
    summary="Get sphere details",
    description="""
    Get full details for a sphere including bureau sections.
    
    **Identity Boundary:** Returns HTTP 403 if sphere belongs to different identity.
    """,
)
async def get_sphere(
    sphere_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereDetail:
    """Get sphere details."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        return await service.get_sphere(sphere_id)
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.get(
    "/type/{sphere_type}",
    response_model=SphereDetail,
    summary="Get sphere by type",
    description="Get sphere details by sphere type (personal, business, etc.).",
)
async def get_sphere_by_type(
    sphere_type: SphereTypeEnum,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereDetail:
    """Get sphere by type."""
    from backend.models.sphere import SphereType
    
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        return await service.get_sphere_by_type(SphereType(sphere_type.value))
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE UPDATE
# ═══════════════════════════════════════════════════════════════════════════════

@router.patch(
    "/{sphere_id}",
    response_model=SphereDetail,
    summary="Update sphere",
    description="""
    Update sphere settings.
    
    **Note:** Sphere type cannot be changed (FROZEN).
    
    Updatable fields:
    - name, icon, color, description
    - is_active, is_pinned
    - display_order, settings
    """,
)
async def update_sphere(
    sphere_id: str,
    request: SphereUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereDetail:
    """Update sphere settings."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        return await service.update_sphere(sphere_id, request)
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.post(
    "/reorder",
    response_model=SphereListResponse,
    summary="Reorder spheres",
    description="Set display order for spheres.",
)
async def reorder_spheres(
    sphere_order: List[str],
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereListResponse:
    """Reorder spheres."""
    service = get_sphere_service(db, current_user.identity_id)
    
    spheres = await service.reorder_spheres(sphere_order)
    
    return SphereListResponse(
        spheres=spheres,
        total=len(spheres),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{sphere_id}/stats",
    response_model=SphereStats,
    summary="Get sphere statistics",
    description="""
    Get activity statistics for a sphere.
    
    **Period options:** day, week, month, year
    """,
)
async def get_sphere_stats(
    sphere_id: str,
    period: str = Query("week", regex="^(day|week|month|year)$"),
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SphereStats:
    """Get sphere statistics."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        return await service.get_sphere_stats(sphere_id, period)
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU SECTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/{sphere_id}/bureau",
    response_model=BureauSectionListResponse,
    summary="List bureau sections",
    description="""
    Get all 6 bureau sections for a sphere.
    
    Each sphere has exactly 6 sections:
    - quick_capture: Inbox for quick captures
    - resume_workspace: Main workspace
    - threads: All threads in this sphere
    - data_files: Files and documents
    - active_agents: Running AI agents
    - meetings: Calendar and meetings
    """,
)
async def list_bureau_sections(
    sphere_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BureauSectionListResponse:
    """List bureau sections."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        sections = await service.get_bureau_sections(sphere_id)
        return BureauSectionListResponse(sections=sections)
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


@router.get(
    "/{sphere_id}/bureau/{section_type}",
    response_model=BureauSectionContent,
    summary="Get bureau section content",
    description="""
    Get content for a specific bureau section.
    
    Content varies by section type:
    - **quick_capture**: Quick capture items
    - **threads**: Thread summaries
    - **active_agents**: Running agents
    - **data_files**: Files and documents
    - **meetings**: Upcoming meetings
    - **resume_workspace**: Active work items
    """,
)
async def get_bureau_section_content(
    sphere_id: str,
    section_type: BureauSectionTypeEnum,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BureauSectionContent:
    """Get bureau section content."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        content = await service.get_bureau_section_content(
            sphere_id,
            BureauSectionType(section_type.value),
            page,
            page_size,
        )
        
        return BureauSectionContent(
            type=section_type,
            items=content.get("items", []),
            pagination={
                "page": content.get("page", page),
                "page_size": content.get("page_size", page_size),
                "total": content.get("total", 0),
                "total_pages": (content.get("total", 0) + page_size - 1) // page_size,
            },
        )
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/{sphere_id}/bureau/quick_capture",
    response_model=QuickCaptureResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create quick capture",
    description="""
    Quickly capture a note, task, idea, or link in a sphere's inbox.
    
    Quick captures land in the quick_capture bureau section
    and can be later routed to threads.
    
    **Types:**
    - note: General note
    - task: Action item
    - idea: Creative thought
    - link: URL reference
    """,
)
async def create_quick_capture(
    sphere_id: str,
    request: QuickCaptureRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> QuickCaptureResponse:
    """Create quick capture."""
    service = get_sphere_service(db, current_user.identity_id)
    
    try:
        return await service.create_quick_capture(
            sphere_id,
            request,
            current_user.id,
        )
    except SphereNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )
    except IdentityBoundaryError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.to_dict(),
        )
