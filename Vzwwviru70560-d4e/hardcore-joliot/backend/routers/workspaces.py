"""
CHE·NU™ V75 - Workspaces Router
Workspace Engine API with multi-mode support.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class PanelPosition(BaseModel):
    """Panel position and size."""
    x: int
    y: int
    width: int
    height: int


class PanelCreate(BaseModel):
    """Create panel request."""
    panel_type: str
    position: PanelPosition
    config: Dict[str, Any] = {}


class WorkspaceCreate(BaseModel):
    """Create workspace request."""
    name: str = Field(..., min_length=1, max_length=255)
    workspace_mode: str = "document"
    dataspace_id: Optional[UUID] = None
    layout_config: Dict[str, Any] = {}


class WorkspaceUpdate(BaseModel):
    """Update workspace request."""
    name: Optional[str] = None
    workspace_mode: Optional[str] = None
    layout_config: Optional[Dict[str, Any]] = None
    view_state: Optional[Dict[str, Any]] = None


class TransformRequest(BaseModel):
    """Transform workspace mode request."""
    to_mode: str


class IntentDetectRequest(BaseModel):
    """Intent detection request."""
    input: str


# ============================================================================
# MOCK DATA
# ============================================================================

WORKSPACE_MODES = [
    "document", "board", "timeline", "spreadsheet",
    "dashboard", "diagram", "whiteboard", "xr", "hybrid"
]

PANEL_TYPES = [
    "editor", "preview", "chat", "files",
    "agents", "timeline", "canvas", "terminal", "browser"
]

MOCK_WORKSPACES = [
    {
        "id": "ws_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": "ds_001",
        "name": "Projet Rénovation Maya",
        "workspace_mode": "hybrid",
        "layout_config": {
            "layout": "split",
            "main_panel": "editor",
            "side_panel": "chat",
        },
        "view_state": {},
        "is_default": False,
        "panels_count": 3,
        "created_at": "2026-01-05T10:00:00Z",
        "updated_at": "2026-01-07T15:30:00Z",
    },
    {
        "id": "ws_002",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": "ds_002",
        "name": "Sprint Board Q1",
        "workspace_mode": "board",
        "layout_config": {
            "columns": ["todo", "in_progress", "review", "done"],
        },
        "view_state": {},
        "is_default": True,
        "panels_count": 1,
        "created_at": "2026-01-02T08:00:00Z",
        "updated_at": "2026-01-07T16:00:00Z",
    },
    {
        "id": "ws_003",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "dataspace_id": None,
        "name": "Dashboard Immobilier",
        "workspace_mode": "dashboard",
        "layout_config": {
            "widgets": ["portfolio_value", "occupancy", "rent_collection", "maintenance"],
        },
        "view_state": {},
        "is_default": False,
        "panels_count": 4,
        "created_at": "2026-01-01T09:00:00Z",
        "updated_at": "2026-01-07T12:00:00Z",
    },
]

# Intent to mode mapping
INTENT_PATTERNS = {
    "document": ["write", "document", "report", "draft", "rédiger", "écrire"],
    "board": ["organize", "task", "kanban", "board", "tâche", "organiser"],
    "timeline": ["plan", "schedule", "roadmap", "gantt", "planifier", "calendrier"],
    "spreadsheet": ["data", "numbers", "budget", "calculate", "données", "calcul"],
    "dashboard": ["monitor", "metrics", "kpi", "overview", "tableau de bord", "métriques"],
    "diagram": ["diagram", "flowchart", "architecture", "diagramme", "flux"],
    "whiteboard": ["brainstorm", "sketch", "ideas", "whiteboard", "idées", "croquis"],
    "xr": ["immersive", "3d", "vr", "xr", "virtual", "immersif"],
}


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=dict)
async def list_workspaces(
    dataspace_id: Optional[UUID] = None,
    mode: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List workspaces with optional filters.
    """
    workspaces = MOCK_WORKSPACES.copy()
    
    if dataspace_id:
        workspaces = [w for w in workspaces if w["dataspace_id"] == str(dataspace_id)]
    if mode:
        workspaces = [w for w in workspaces if w["workspace_mode"] == mode]
    
    total = len(workspaces)
    
    return {
        "success": True,
        "data": {
            "workspaces": workspaces,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/modes", response_model=dict)
async def list_modes():
    """
    List available workspace modes.
    """
    return {
        "success": True,
        "data": {
            "modes": [
                {"id": "document", "label": "Document", "icon": "📄", "description": "Rich text editing"},
                {"id": "board", "label": "Board", "icon": "📋", "description": "Kanban task management"},
                {"id": "timeline", "label": "Timeline", "icon": "📅", "description": "Chronological planning"},
                {"id": "spreadsheet", "label": "Spreadsheet", "icon": "📊", "description": "Data tables"},
                {"id": "dashboard", "label": "Dashboard", "icon": "📈", "description": "KPIs and metrics"},
                {"id": "diagram", "label": "Diagram", "icon": "🔀", "description": "Visual diagrams"},
                {"id": "whiteboard", "label": "Whiteboard", "icon": "🎨", "description": "Freeform canvas"},
                {"id": "xr", "label": "XR", "icon": "🥽", "description": "Immersive experience"},
                {"id": "hybrid", "label": "Hybrid", "icon": "🔲", "description": "Multi-mode layout"},
            ],
        },
    }


@router.get("/{workspace_id}", response_model=dict)
async def get_workspace(workspace_id: str):
    """
    Get workspace details.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return {
        "success": True,
        "data": workspace,
    }


@router.post("", response_model=dict)
async def create_workspace(data: WorkspaceCreate):
    """
    Create a new workspace.
    """
    if data.workspace_mode not in WORKSPACE_MODES:
        raise HTTPException(status_code=400, detail=f"Invalid workspace mode. Must be one of: {WORKSPACE_MODES}")
    
    workspace = {
        "id": f"ws_{len(MOCK_WORKSPACES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "dataspace_id": str(data.dataspace_id) if data.dataspace_id else None,
        "name": data.name,
        "workspace_mode": data.workspace_mode,
        "layout_config": data.layout_config,
        "view_state": {},
        "is_default": False,
        "panels_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    return {
        "success": True,
        "data": workspace,
        "message": "Workspace créé avec succès",
    }


@router.patch("/{workspace_id}", response_model=dict)
async def update_workspace(workspace_id: str, data: WorkspaceUpdate):
    """
    Update workspace details.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if data.name:
        workspace["name"] = data.name
    if data.workspace_mode:
        if data.workspace_mode not in WORKSPACE_MODES:
            raise HTTPException(status_code=400, detail=f"Invalid workspace mode")
        workspace["workspace_mode"] = data.workspace_mode
    if data.layout_config is not None:
        workspace["layout_config"] = data.layout_config
    if data.view_state is not None:
        workspace["view_state"] = data.view_state
    
    workspace["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": workspace,
    }


@router.delete("/{workspace_id}", response_model=dict)
async def delete_workspace(workspace_id: str):
    """
    Delete workspace.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return {
        "success": True,
        "message": "Workspace supprimé",
    }


# ============================================================================
# PANELS
# ============================================================================

@router.get("/{workspace_id}/panels", response_model=dict)
async def list_panels(workspace_id: str):
    """
    List panels in workspace.
    """
    panels = [
        {"id": "panel_001", "workspace_id": workspace_id, "panel_type": "editor", "position": {"x": 0, "y": 0, "width": 800, "height": 600}, "config": {}, "is_visible": True, "z_index": 0},
        {"id": "panel_002", "workspace_id": workspace_id, "panel_type": "chat", "position": {"x": 800, "y": 0, "width": 400, "height": 600}, "config": {}, "is_visible": True, "z_index": 1},
    ]
    
    return {
        "success": True,
        "data": {
            "panels": panels,
        },
    }


@router.post("/{workspace_id}/panels", response_model=dict)
async def create_panel(workspace_id: str, data: PanelCreate):
    """
    Add panel to workspace.
    """
    if data.panel_type not in PANEL_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid panel type. Must be one of: {PANEL_TYPES}")
    
    panel = {
        "id": "panel_new",
        "workspace_id": workspace_id,
        "panel_type": data.panel_type,
        "position": data.position.dict(),
        "config": data.config,
        "is_visible": True,
        "z_index": 0,
    }
    
    return {
        "success": True,
        "data": panel,
        "message": "Panel ajouté",
    }


@router.patch("/{workspace_id}/panels/{panel_id}", response_model=dict)
async def update_panel(workspace_id: str, panel_id: str, data: dict):
    """
    Update panel configuration.
    """
    return {
        "success": True,
        "data": {
            "id": panel_id,
            "workspace_id": workspace_id,
            **data,
        },
    }


@router.delete("/{workspace_id}/panels/{panel_id}", response_model=dict)
async def delete_panel(workspace_id: str, panel_id: str):
    """
    Remove panel from workspace.
    """
    return {
        "success": True,
        "message": "Panel supprimé",
    }


# ============================================================================
# STATES
# ============================================================================

@router.get("/{workspace_id}/states", response_model=dict)
async def list_states(workspace_id: str):
    """
    List saved workspace states.
    """
    states = [
        {"id": "state_001", "workspace_id": workspace_id, "state_name": "Configuration initiale", "is_autosave": False, "created_at": "2026-01-05T10:00:00Z"},
        {"id": "state_002", "workspace_id": workspace_id, "state_name": "Autosave", "is_autosave": True, "created_at": "2026-01-07T15:30:00Z"},
    ]
    
    return {
        "success": True,
        "data": {
            "states": states,
        },
    }


@router.post("/{workspace_id}/states", response_model=dict)
async def save_state(workspace_id: str, state_name: str = ""):
    """
    Save current workspace state.
    """
    state = {
        "id": "state_new",
        "workspace_id": workspace_id,
        "state_name": state_name or f"Sauvegarde {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        "is_autosave": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    return {
        "success": True,
        "data": state,
        "message": "État sauvegardé",
    }


@router.post("/{workspace_id}/states/{state_id}/restore", response_model=dict)
async def restore_state(workspace_id: str, state_id: str):
    """
    Restore workspace to saved state.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return {
        "success": True,
        "data": workspace,
        "message": "État restauré",
    }


# ============================================================================
# TRANSFORMATIONS
# ============================================================================

@router.post("/{workspace_id}/transform", response_model=dict)
async def transform_workspace(workspace_id: str, data: TransformRequest):
    """
    Transform workspace to different mode.
    
    GOUVERNANCE: Transformation is logged and reversible.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if data.to_mode not in WORKSPACE_MODES:
        raise HTTPException(status_code=400, detail=f"Invalid workspace mode")
    
    from_mode = workspace["workspace_mode"]
    
    transformation = {
        "id": "transform_001",
        "workspace_id": workspace_id,
        "from_mode": from_mode,
        "to_mode": data.to_mode,
        "transformation_data": {
            "preserved_content": True,
            "layout_adapted": True,
        },
        "triggered_at": datetime.utcnow().isoformat(),
        "is_reversible": True,
    }
    
    workspace["workspace_mode"] = data.to_mode
    workspace["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": transformation,
        "message": f"Workspace transformé de {from_mode} vers {data.to_mode}",
    }


@router.post("/{workspace_id}/transformations/{transformation_id}/undo", response_model=dict)
async def undo_transformation(workspace_id: str, transformation_id: str):
    """
    Undo transformation.
    """
    workspace = next((w for w in MOCK_WORKSPACES if w["id"] == workspace_id), None)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return {
        "success": True,
        "data": workspace,
        "message": "Transformation annulée",
    }


# ============================================================================
# INTENT DETECTION
# ============================================================================

@router.post("/detect-intent", response_model=dict)
async def detect_intent(data: IntentDetectRequest):
    """
    Detect user intent and suggest workspace mode.
    """
    input_lower = data.input.lower()
    
    suggested_mode = "document"  # Default
    confidence = 0.5
    tools = []
    
    for mode, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if pattern in input_lower:
                suggested_mode = mode
                confidence = 0.85
                break
    
    # Determine tools based on mode
    mode_tools = {
        "document": ["rich_editor", "templates", "export"],
        "board": ["kanban", "cards", "filters"],
        "timeline": ["gantt", "milestones", "dependencies"],
        "spreadsheet": ["formulas", "charts", "pivot"],
        "dashboard": ["widgets", "kpis", "alerts"],
        "diagram": ["shapes", "connectors", "auto_layout"],
        "whiteboard": ["drawing", "sticky_notes", "sections"],
        "xr": ["vr_launch", "3d_preview", "spatial_audio"],
    }
    
    tools = mode_tools.get(suggested_mode, [])
    
    return {
        "success": True,
        "data": {
            "suggested_mode": suggested_mode,
            "confidence": confidence,
            "tools": tools,
            "input_analyzed": data.input,
        },
    }
