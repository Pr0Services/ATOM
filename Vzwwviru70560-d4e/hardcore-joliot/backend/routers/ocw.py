"""
CHE·NU™ V75 - OCW Router
Operational Cognitive Workspace API.

OCW = Intelligent Whiteboard + ShareView + Agent Cockpit

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

class CanvasObjectCreate(BaseModel):
    """Create canvas object."""
    object_type: str  # shape, text, image, drawing, sticky, connector, frame
    position: Dict[str, float]  # x, y
    size: Optional[Dict[str, float]] = None  # width, height
    properties: Dict[str, Any] = {}


class CanvasObjectUpdate(BaseModel):
    """Update canvas object."""
    position: Optional[Dict[str, float]] = None
    size: Optional[Dict[str, float]] = None
    rotation: Optional[float] = None
    properties: Optional[Dict[str, Any]] = None


class SessionCreate(BaseModel):
    """Create OCW session."""
    workspace_id: str
    session_type: str = "whiteboard"  # shareview, whiteboard, cockpit, collaboration


class AnnotationCreate(BaseModel):
    """Create annotation."""
    object_id: Optional[str] = None
    annotation_type: str = "comment"  # comment, highlight, marker, voice_note
    content: str
    position: Optional[Dict[str, float]] = None


class ShareViewConfig(BaseModel):
    """ShareView configuration."""
    mode: str = "none"  # full, area, elements, none
    selected_area: Optional[Dict[str, float]] = None  # x, y, width, height
    selected_elements: Optional[List[str]] = None


class TransformRequest(BaseModel):
    """Transform content request."""
    object_ids: List[str]
    transformation: str  # diagram, mindmap, outline, dataspace, formalize


# ============================================================================
# MOCK DATA
# ============================================================================

OBJECT_TYPES = ["shape", "text", "image", "drawing", "sticky", "connector", "frame"]

SESSION_TYPES = ["shareview", "whiteboard", "cockpit", "collaboration"]

MOCK_SESSIONS = [
    {
        "id": "ocw_001",
        "workspace_id": "ws_001",
        "session_type": "whiteboard",
        "host_user_id": "user_001",
        "status": "active",
        "config": {"grid_visible": True, "snap_to_grid": True},
        "participants_count": 1,
        "objects_count": 12,
        "started_at": "2026-01-07T10:00:00Z",
        "ended_at": None,
    },
]

MOCK_OBJECTS = [
    {
        "id": "obj_001",
        "session_id": "ocw_001",
        "object_type": "sticky",
        "position": {"x": 100, "y": 100},
        "size": {"width": 200, "height": 150},
        "rotation": 0,
        "properties": {"color": "#D8B26A", "text": "Idée: Nouveau module"},
        "layer": 0,
        "is_locked": False,
        "created_by": "user_001",
        "created_at": "2026-01-07T10:05:00Z",
    },
    {
        "id": "obj_002",
        "session_id": "ocw_001",
        "object_type": "shape",
        "position": {"x": 400, "y": 100},
        "size": {"width": 150, "height": 100},
        "rotation": 0,
        "properties": {"shape": "rectangle", "fill": "#3EB4A2", "stroke": "#2F4C39"},
        "layer": 0,
        "is_locked": False,
        "created_by": "user_001",
        "created_at": "2026-01-07T10:10:00Z",
    },
    {
        "id": "obj_003",
        "session_id": "ocw_001",
        "object_type": "connector",
        "position": {"x": 300, "y": 150},
        "size": None,
        "rotation": 0,
        "properties": {"from": "obj_001", "to": "obj_002", "style": "arrow"},
        "layer": 1,
        "is_locked": False,
        "created_by": "user_001",
        "created_at": "2026-01-07T10:12:00Z",
    },
    {
        "id": "obj_004",
        "session_id": "ocw_001",
        "object_type": "text",
        "position": {"x": 100, "y": 300},
        "size": {"width": 500, "height": 100},
        "rotation": 0,
        "properties": {"content": "Brainstorm Session - Q1 2026", "fontSize": 24, "fontWeight": "bold"},
        "layer": 0,
        "is_locked": True,
        "created_by": "user_001",
        "created_at": "2026-01-07T10:00:00Z",
    },
]


# ============================================================================
# SESSIONS
# ============================================================================

@router.get("/sessions", response_model=dict)
async def list_sessions(
    workspace_id: Optional[str] = None,
    session_type: Optional[str] = None,
    status: Optional[str] = "active",
):
    """
    List OCW sessions.
    """
    sessions = MOCK_SESSIONS.copy()
    
    if workspace_id:
        sessions = [s for s in sessions if s["workspace_id"] == workspace_id]
    if session_type:
        sessions = [s for s in sessions if s["session_type"] == session_type]
    if status:
        sessions = [s for s in sessions if s["status"] == status]
    
    return {
        "success": True,
        "data": {
            "sessions": sessions,
            "total": len(sessions),
        },
    }


@router.get("/sessions/{session_id}", response_model=dict)
async def get_session(session_id: str):
    """
    Get session details.
    """
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "success": True,
        "data": session,
    }


@router.post("/sessions", response_model=dict)
async def create_session(data: SessionCreate):
    """
    Create new OCW session.
    """
    if data.session_type not in SESSION_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid session type. Must be one of: {SESSION_TYPES}")
    
    session = {
        "id": f"ocw_{len(MOCK_SESSIONS) + 1:03d}",
        "workspace_id": data.workspace_id,
        "session_type": data.session_type,
        "host_user_id": "user_001",
        "status": "active",
        "config": {},
        "participants_count": 1,
        "objects_count": 0,
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
    }
    
    MOCK_SESSIONS.append(session)
    
    return {
        "success": True,
        "data": session,
        "message": "Session OCW créée",
    }


@router.post("/sessions/{session_id}/end", response_model=dict)
async def end_session(session_id: str):
    """
    End OCW session.
    """
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session["status"] = "ended"
    session["ended_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": session,
        "message": "Session terminée",
    }


# ============================================================================
# CANVAS OBJECTS
# ============================================================================

@router.get("/sessions/{session_id}/objects", response_model=dict)
async def list_objects(session_id: str):
    """
    List objects in session.
    """
    objects = [o for o in MOCK_OBJECTS if o["session_id"] == session_id]
    
    return {
        "success": True,
        "data": {
            "objects": objects,
            "total": len(objects),
        },
    }


@router.post("/sessions/{session_id}/objects", response_model=dict)
async def create_object(session_id: str, data: CanvasObjectCreate):
    """
    Create canvas object.
    """
    if data.object_type not in OBJECT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid object type. Must be one of: {OBJECT_TYPES}")
    
    obj = {
        "id": f"obj_{len(MOCK_OBJECTS) + 1:03d}",
        "session_id": session_id,
        "object_type": data.object_type,
        "position": data.position,
        "size": data.size,
        "rotation": 0,
        "properties": data.properties,
        "layer": 0,
        "is_locked": False,
        "created_by": "user_001",
        "created_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_OBJECTS.append(obj)
    
    return {
        "success": True,
        "data": obj,
    }


@router.patch("/sessions/{session_id}/objects/{object_id}", response_model=dict)
async def update_object(session_id: str, object_id: str, data: CanvasObjectUpdate):
    """
    Update canvas object.
    """
    obj = next((o for o in MOCK_OBJECTS if o["id"] == object_id and o["session_id"] == session_id), None)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    if obj["is_locked"]:
        raise HTTPException(status_code=400, detail="Object is locked")
    
    if data.position:
        obj["position"] = data.position
    if data.size:
        obj["size"] = data.size
    if data.rotation is not None:
        obj["rotation"] = data.rotation
    if data.properties:
        obj["properties"].update(data.properties)
    
    obj["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": obj,
    }


@router.delete("/sessions/{session_id}/objects/{object_id}", response_model=dict)
async def delete_object(session_id: str, object_id: str):
    """
    Delete canvas object.
    """
    obj = next((o for o in MOCK_OBJECTS if o["id"] == object_id and o["session_id"] == session_id), None)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    if obj["is_locked"]:
        raise HTTPException(status_code=400, detail="Object is locked")
    
    MOCK_OBJECTS.remove(obj)
    
    return {
        "success": True,
        "message": "Objet supprimé",
    }


@router.post("/sessions/{session_id}/objects/{object_id}/lock", response_model=dict)
async def toggle_lock(session_id: str, object_id: str):
    """
    Toggle object lock.
    """
    obj = next((o for o in MOCK_OBJECTS if o["id"] == object_id and o["session_id"] == session_id), None)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    
    obj["is_locked"] = not obj["is_locked"]
    
    return {
        "success": True,
        "data": obj,
    }


# ============================================================================
# PARTICIPANTS
# ============================================================================

@router.get("/sessions/{session_id}/participants", response_model=dict)
async def list_participants(session_id: str):
    """
    List session participants.
    """
    participants = [
        {"id": "part_001", "user_id": "user_001", "role": "host", "cursor_position": {"x": 250, "y": 180}, "joined_at": "2026-01-07T10:00:00Z"},
    ]
    
    return {
        "success": True,
        "data": {
            "participants": participants,
        },
    }


@router.post("/sessions/{session_id}/join", response_model=dict)
async def join_session(session_id: str):
    """
    Join OCW session.
    """
    return {
        "success": True,
        "data": {
            "participant_id": "part_new",
            "role": "editor",
            "joined_at": datetime.utcnow().isoformat(),
        },
        "message": "Session rejointe",
    }


# ============================================================================
# SHAREVIEW
# ============================================================================

@router.post("/sessions/{session_id}/shareview", response_model=dict)
async def configure_shareview(session_id: str, config: ShareViewConfig):
    """
    Configure ShareView for AI assistance.
    
    GOUVERNANCE: User controls what AI can see.
    """
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    shareview_config = {
        "mode": config.mode,
        "selected_area": config.selected_area,
        "selected_elements": config.selected_elements,
        "enabled_at": datetime.utcnow().isoformat() if config.mode != "none" else None,
    }
    
    session["config"]["shareview"] = shareview_config
    
    return {
        "success": True,
        "data": shareview_config,
        "message": f"ShareView configuré en mode '{config.mode}'",
        "governance": {
            "ai_can_see": config.mode != "none",
            "scope": config.mode,
        },
    }


@router.get("/sessions/{session_id}/shareview/status", response_model=dict)
async def get_shareview_status(session_id: str):
    """
    Get ShareView status.
    """
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    shareview = session.get("config", {}).get("shareview", {"mode": "none"})
    
    return {
        "success": True,
        "data": {
            "mode": shareview.get("mode", "none"),
            "ai_can_see": shareview.get("mode", "none") != "none",
            "enabled_at": shareview.get("enabled_at"),
        },
    }


# ============================================================================
# TRANSFORMATIONS
# ============================================================================

@router.post("/sessions/{session_id}/transform", response_model=dict)
async def transform_content(session_id: str, data: TransformRequest):
    """
    Transform canvas content.
    
    Supported transformations:
    - diagram: Convert sketches to formal diagrams
    - mindmap: Organize as mind map
    - outline: Convert to text outline
    - dataspace: Create DataSpace from content
    - formalize: Clean up and formalize
    
    GOUVERNANCE: Creates checkpoint for approval.
    """
    transformations = ["diagram", "mindmap", "outline", "dataspace", "formalize"]
    
    if data.transformation not in transformations:
        raise HTTPException(status_code=400, detail=f"Invalid transformation. Must be one of: {transformations}")
    
    # Simulate transformation result
    result = {
        "transformation_id": "transform_001",
        "session_id": session_id,
        "object_ids": data.object_ids,
        "transformation": data.transformation,
        "status": "completed",
        "result": {
            "new_objects": [
                {"id": "obj_new_001", "object_type": "frame", "position": {"x": 100, "y": 100}},
            ],
            "removed_objects": data.object_ids if data.transformation != "dataspace" else [],
        },
        "created_at": datetime.utcnow().isoformat(),
    }
    
    if data.transformation == "dataspace":
        result["dataspace_created"] = {
            "id": "ds_new",
            "name": "DataSpace from OCW",
            "items_count": len(data.object_ids),
        }
    
    return {
        "success": True,
        "data": result,
        "message": f"Transformation '{data.transformation}' appliquée",
        "governance": {
            "checkpoint_created": data.transformation == "dataspace",
        },
    }


# ============================================================================
# ANNOTATIONS
# ============================================================================

@router.get("/sessions/{session_id}/annotations", response_model=dict)
async def list_annotations(session_id: str, object_id: Optional[str] = None):
    """
    List annotations in session.
    """
    annotations = [
        {"id": "ann_001", "session_id": session_id, "object_id": "obj_001", "annotation_type": "comment", "content": "À développer", "created_by": "user_001", "created_at": "2026-01-07T10:15:00Z"},
    ]
    
    if object_id:
        annotations = [a for a in annotations if a["object_id"] == object_id]
    
    return {
        "success": True,
        "data": {
            "annotations": annotations,
        },
    }


@router.post("/sessions/{session_id}/annotations", response_model=dict)
async def create_annotation(session_id: str, data: AnnotationCreate):
    """
    Create annotation.
    """
    annotation = {
        "id": "ann_new",
        "session_id": session_id,
        "object_id": data.object_id,
        "annotation_type": data.annotation_type,
        "content": data.content,
        "position": data.position,
        "created_by": "user_001",
        "created_at": datetime.utcnow().isoformat(),
    }
    
    return {
        "success": True,
        "data": annotation,
    }


# ============================================================================
# AGENT MODES
# ============================================================================

@router.get("/sessions/{session_id}/agent-mode", response_model=dict)
async def get_agent_mode(session_id: str):
    """
    Get current agent mode.
    """
    return {
        "success": True,
        "data": {
            "mode": "spectator",  # spectator, advisor, organizer, constructor
            "active_agents": [],
            "suggestions_enabled": False,
        },
    }


@router.post("/sessions/{session_id}/agent-mode", response_model=dict)
async def set_agent_mode(session_id: str, mode: str = "spectator"):
    """
    Set agent mode.
    
    Modes:
    - spectator: Observe only
    - advisor: Suggestions enabled
    - organizer: Can propose restructuring
    - constructor: Can build structures
    
    GOUVERNANCE: User controls agent capabilities.
    """
    modes = ["spectator", "advisor", "organizer", "constructor"]
    
    if mode not in modes:
        raise HTTPException(status_code=400, detail=f"Invalid mode. Must be one of: {modes}")
    
    return {
        "success": True,
        "data": {
            "mode": mode,
            "suggestions_enabled": mode in ["advisor", "organizer", "constructor"],
            "can_modify": mode == "constructor",
        },
        "message": f"Mode agent changé en '{mode}'",
        "governance": {
            "agent_can_observe": True,
            "agent_can_suggest": mode in ["advisor", "organizer", "constructor"],
            "agent_can_modify": mode == "constructor",
        },
    }
