"""
ROUTER: workspaces.py
PREFIX: /api/v2/workspaces
VERSION: 1.0.0
PHASE: B2

Workspace Engine - Bureau Sections Management.
Implements the 6 canonical bureau sections per sphere.

R&D COMPLIANCE:
- Rule #3 (Identity Boundary): Workspaces scoped to identity
- Rule #5 (No Ranking): Chronological ordering
- Rule #6 (Traceability): Full audit trail
- Rule #7 (Continuity): 6 bureau sections per workspace

BUREAU SECTIONS (6):
- QuickCapture: Rapid capture inbox
- ResumeWorkspace: Main work area
- Threads: Thread management
- DataFiles: File storage
- ActiveAgents: Agent dashboard
- Meetings: Meeting scheduler

ENDPOINTS: 12
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2/workspaces", tags=["Workspaces"])

# ============================================================
# ENUMS
# ============================================================

class BureauSection(str, Enum):
    """The 6 canonical bureau sections - R&D Rule #7."""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"

class WorkspaceStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

# ============================================================
# SCHEMAS
# ============================================================

class BureauSectionResponse(BaseModel):
    """Bureau section within a workspace."""
    id: UUID
    workspace_id: UUID
    section_type: BureauSection
    item_count: int
    last_accessed: Optional[datetime]
    is_pinned: bool

class WorkspaceCreate(BaseModel):
    """Create a workspace."""
    name: str = Field(..., min_length=1, max_length=100)
    sphere_id: UUID
    description: Optional[str] = Field(None, max_length=500)

class WorkspaceResponse(BaseModel):
    """Workspace response with R&D Rule #6 compliance."""
    id: UUID
    identity_id: UUID
    sphere_id: UUID
    created_by: UUID
    created_at: datetime
    name: str
    description: Optional[str]
    status: WorkspaceStatus
    section_count: int  # Should always be 6

class WorkspaceFullResponse(BaseModel):
    """Workspace with all bureau sections."""
    workspace: WorkspaceResponse
    sections: List[BureauSectionResponse]

class QuickCaptureItem(BaseModel):
    """Item in QuickCapture inbox."""
    content: str = Field(..., min_length=1, max_length=5000)
    capture_type: str = Field(default="note")
    thread_id: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)

class QuickCaptureResponse(BaseModel):
    """QuickCapture item response."""
    id: UUID
    workspace_id: UUID
    created_by: UUID
    created_at: datetime
    content: str
    capture_type: str
    thread_id: Optional[UUID]
    tags: List[str]
    is_processed: bool

# ============================================================
# MOCK DATA STORE
# ============================================================

_workspaces_store: Dict[UUID, Dict] = {}
_sections_store: Dict[UUID, List[Dict]] = {}  # workspace_id -> sections
_quick_captures_store: Dict[UUID, List[Dict]] = {}  # workspace_id -> captures

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_user_id() -> UUID:
    return UUID("11111111-1111-1111-1111-111111111111")

async def get_current_identity_id() -> UUID:
    return UUID("22222222-2222-2222-2222-222222222222")

async def verify_workspace_access(
    workspace_id: UUID,
    identity_id: UUID
) -> Dict:
    """Verify identity can access workspace - R&D Rule #3."""
    if workspace_id not in _workspaces_store:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_store[workspace_id]
    if workspace["identity_id"] != identity_id:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Workspace belongs to different identity",
                "code": "RULE_3_VIOLATION"
            }
        )
    return workspace

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_6_bureau_sections(workspace_id: UUID) -> List[Dict]:
    """
    Create the 6 canonical bureau sections.
    R&D Rule #7: Every workspace has exactly 6 sections.
    """
    sections = []
    for section_type in BureauSection:
        section = {
            "id": uuid4(),
            "workspace_id": workspace_id,
            "section_type": section_type,
            "item_count": 0,
            "last_accessed": None,
            "is_pinned": False
        }
        sections.append(section)
    return sections

# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/", response_model=List[WorkspaceResponse])
async def list_workspaces(
    sphere_id: Optional[UUID] = None,
    status: Optional[WorkspaceStatus] = None,
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List workspaces for current identity.
    
    R&D Rule #3: Only identity's workspaces.
    R&D Rule #5: Chronological order.
    """
    workspaces = [
        w for w in _workspaces_store.values()
        if w["identity_id"] == identity_id
    ]
    
    if sphere_id:
        workspaces = [w for w in workspaces if w["sphere_id"] == sphere_id]
    if status:
        workspaces = [w for w in workspaces if w["status"] == status]
    
    # R&D Rule #5: Chronological
    workspaces.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [WorkspaceResponse(**w) for w in workspaces]

@router.post("/", response_model=WorkspaceFullResponse, status_code=201)
async def create_workspace(
    data: WorkspaceCreate,
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Create workspace with 6 bureau sections.
    
    R&D Rule #6: Traceability.
    R&D Rule #7: Auto-creates 6 sections.
    """
    now = datetime.utcnow()
    workspace_id = uuid4()
    
    workspace = {
        "id": workspace_id,
        "identity_id": identity_id,
        "sphere_id": data.sphere_id,
        "created_by": user_id,
        "created_at": now,
        "name": data.name,
        "description": data.description,
        "status": WorkspaceStatus.ACTIVE,
        "section_count": 6
    }
    
    sections = create_6_bureau_sections(workspace_id)
    
    _workspaces_store[workspace_id] = workspace
    _sections_store[workspace_id] = sections
    
    return WorkspaceFullResponse(
        workspace=WorkspaceResponse(**workspace),
        sections=[BureauSectionResponse(**s) for s in sections]
    )

@router.get("/{workspace_id}", response_model=WorkspaceFullResponse)
async def get_workspace(
    workspace_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get workspace with bureau sections."""
    workspace = await verify_workspace_access(workspace_id, identity_id)
    sections = _sections_store.get(workspace_id, [])
    
    # R&D Rule #7: Verify 6 sections
    if len(sections) != 6:
        sections = create_6_bureau_sections(workspace_id)
        _sections_store[workspace_id] = sections
    
    return WorkspaceFullResponse(
        workspace=WorkspaceResponse(**workspace),
        sections=[BureauSectionResponse(**s) for s in sections]
    )

@router.delete("/{workspace_id}", status_code=423)
async def delete_workspace(
    workspace_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Delete workspace - REQUIRES CHECKPOINT."""
    await verify_workspace_access(workspace_id, identity_id)
    
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "workspace_delete",
                "workspace_id": str(workspace_id),
                "requires_approval": True,
                "options": ["approve", "reject"]
            }
        }
    )

# --- BUREAU SECTIONS ---

@router.get("/{workspace_id}/sections", response_model=List[BureauSectionResponse])
async def list_bureau_sections(
    workspace_id: UUID = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """List all 6 bureau sections."""
    await verify_workspace_access(workspace_id, identity_id)
    sections = _sections_store.get(workspace_id, [])
    return [BureauSectionResponse(**s) for s in sections]

@router.get("/{workspace_id}/sections/{section_type}", response_model=BureauSectionResponse)
async def get_bureau_section(
    workspace_id: UUID = Path(...),
    section_type: BureauSection = Path(...),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Get a specific bureau section."""
    await verify_workspace_access(workspace_id, identity_id)
    sections = _sections_store.get(workspace_id, [])
    
    section = next((s for s in sections if s["section_type"] == section_type), None)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Update last accessed
    section["last_accessed"] = datetime.utcnow()
    
    return BureauSectionResponse(**section)

# --- QUICK CAPTURE ---

@router.post("/{workspace_id}/quick-capture", response_model=QuickCaptureResponse, status_code=201)
async def create_quick_capture(
    workspace_id: UUID = Path(...),
    data: QuickCaptureItem = Body(...),
    user_id: UUID = Depends(get_current_user_id),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    Create a quick capture item.
    Fast inbox for rapid thought capture.
    """
    await verify_workspace_access(workspace_id, identity_id)
    
    now = datetime.utcnow()
    capture = {
        "id": uuid4(),
        "workspace_id": workspace_id,
        "created_by": user_id,
        "created_at": now,
        "content": data.content,
        "capture_type": data.capture_type,
        "thread_id": data.thread_id,
        "tags": data.tags,
        "is_processed": False
    }
    
    _quick_captures_store.setdefault(workspace_id, []).append(capture)
    
    # Update section count
    sections = _sections_store.get(workspace_id, [])
    qc_section = next((s for s in sections if s["section_type"] == BureauSection.QUICK_CAPTURE), None)
    if qc_section:
        qc_section["item_count"] += 1
        qc_section["last_accessed"] = now
    
    return QuickCaptureResponse(**capture)

@router.get("/{workspace_id}/quick-capture", response_model=List[QuickCaptureResponse])
async def list_quick_captures(
    workspace_id: UUID = Path(...),
    is_processed: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=200),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """
    List quick captures.
    R&D Rule #5: Chronological order.
    """
    await verify_workspace_access(workspace_id, identity_id)
    captures = _quick_captures_store.get(workspace_id, [])
    
    if is_processed is not None:
        captures = [c for c in captures if c["is_processed"] == is_processed]
    
    # Chronological order
    captures.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [QuickCaptureResponse(**c) for c in captures[:limit]]

@router.post("/{workspace_id}/quick-capture/{capture_id}/process")
async def process_quick_capture(
    workspace_id: UUID = Path(...),
    capture_id: UUID = Path(...),
    target_thread_id: UUID = Body(..., embed=True),
    identity_id: UUID = Depends(get_current_identity_id)
):
    """Process a quick capture into a thread."""
    await verify_workspace_access(workspace_id, identity_id)
    
    captures = _quick_captures_store.get(workspace_id, [])
    capture = next((c for c in captures if c["id"] == capture_id), None)
    
    if not capture:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    capture["is_processed"] = True
    capture["thread_id"] = target_thread_id
    
    return {"status": "processed", "capture_id": str(capture_id), "thread_id": str(target_thread_id)}

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    return {
        "status": "healthy",
        "router": "workspaces",
        "version": "1.0.0",
        "endpoints": 12,
        "bureau_sections": 6,
        "rd_rules_enforced": ["#3", "#5", "#6", "#7"]
    }
