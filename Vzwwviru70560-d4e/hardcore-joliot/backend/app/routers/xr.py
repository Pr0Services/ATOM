"""
CHE·NU™ V76 — XR ENVIRONMENT ROUTER
====================================
Génération d'environnements XR (Mixed Reality) depuis les Threads.

Le Thread est la SOURCE DE VÉRITÉ.
L'environnement XR est une PROJECTION du Thread.

TEMPLATES:
- personal_room
- business_room
- cause_room
- lab_room
- custom_room

CANONICAL ZONES:
- intent_wall      → Intention fondatrice
- decision_wall    → Historique décisions
- action_table     → Actions en cours
- memory_kiosk     → Accès mémoire
- timeline_strip   → Timeline événements
- resource_shelf   → Liens et ressources

R&D Rules Compliance:
- Rule #3: XR = projection, jamais source de vérité
- Rule #6: Traçabilité complète des blueprints
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger("chenu.routers.xr")

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class XRTemplate(str, Enum):
    PERSONAL_ROOM = "personal_room"
    BUSINESS_ROOM = "business_room"
    CAUSE_ROOM = "cause_room"
    LAB_ROOM = "lab_room"
    CUSTOM_ROOM = "custom_room"


class XRZone(str, Enum):
    INTENT_WALL = "intent_wall"
    DECISION_WALL = "decision_wall"
    ACTION_TABLE = "action_table"
    MEMORY_KIOSK = "memory_kiosk"
    TIMELINE_STRIP = "timeline_strip"
    RESOURCE_SHELF = "resource_shelf"


class BlueprintStatus(str, Enum):
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"
    OUTDATED = "outdated"


class Vector3(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class XRObject(BaseModel):
    id: UUID
    type: str
    position: Vector3
    rotation: Vector3
    scale: Vector3
    data: Dict[str, Any]
    interactive: bool = True


class XRZoneConfig(BaseModel):
    zone: XRZone
    position: Vector3
    size: Vector3
    objects: List[XRObject] = []
    visible: bool = True


class XRBlueprintCreate(BaseModel):
    thread_id: UUID
    template: XRTemplate = XRTemplate.PERSONAL_ROOM
    custom_zones: Optional[List[XRZoneConfig]] = None
    options: Optional[Dict[str, Any]] = None


class XRBlueprint(BaseModel):
    id: UUID
    thread_id: UUID
    template: XRTemplate
    status: BlueprintStatus
    zones: List[XRZoneConfig]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    version: int = 1


class XRSession(BaseModel):
    id: UUID
    blueprint_id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: Optional[datetime]
    device_type: str
    interactions: int = 0


# ============================================================================
# MOCK DATABASE
# ============================================================================

_blueprints: Dict[str, Dict] = {}
_sessions: Dict[str, Dict] = {}


def get_current_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def _generate_default_zones(template: XRTemplate) -> List[Dict]:
    """Generate default zone configurations based on template."""
    
    base_zones = [
        {
            "zone": XRZone.INTENT_WALL,
            "position": {"x": 0, "y": 2, "z": -5},
            "size": {"x": 6, "y": 3, "z": 0.1},
            "objects": [],
            "visible": True
        },
        {
            "zone": XRZone.DECISION_WALL,
            "position": {"x": -5, "y": 1.5, "z": 0},
            "size": {"x": 0.1, "y": 4, "z": 8},
            "objects": [],
            "visible": True
        },
        {
            "zone": XRZone.ACTION_TABLE,
            "position": {"x": 0, "y": 0.8, "z": 0},
            "size": {"x": 2, "y": 0.1, "z": 1.5},
            "objects": [],
            "visible": True
        },
        {
            "zone": XRZone.MEMORY_KIOSK,
            "position": {"x": 4, "y": 0, "z": 2},
            "size": {"x": 1, "y": 2, "z": 1},
            "objects": [],
            "visible": True
        },
        {
            "zone": XRZone.TIMELINE_STRIP,
            "position": {"x": 0, "y": 0.1, "z": 4},
            "size": {"x": 10, "y": 0.05, "z": 0.5},
            "objects": [],
            "visible": True
        },
        {
            "zone": XRZone.RESOURCE_SHELF,
            "position": {"x": 5, "y": 1.5, "z": 0},
            "size": {"x": 0.1, "y": 3, "z": 6},
            "objects": [],
            "visible": True
        }
    ]
    
    # Customize based on template
    if template == XRTemplate.BUSINESS_ROOM:
        base_zones[2]["size"] = {"x": 3, "y": 0.1, "z": 2}  # Bigger table
    elif template == XRTemplate.LAB_ROOM:
        base_zones[3]["size"] = {"x": 2, "y": 2.5, "z": 2}  # Bigger kiosk
    
    return base_zones


# ============================================================================
# BLUEPRINT ENDPOINTS (1-7)
# ============================================================================

@router.post("/blueprints", response_model=XRBlueprint, status_code=201)
async def create_blueprint(
    data: XRBlueprintCreate,
    background_tasks: BackgroundTasks
):
    """
    Generate an XR blueprint from a Thread.
    
    The blueprint is a PROJECTION of the Thread's data into 3D space.
    Thread remains the source of truth.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    blueprint = {
        "id": str(uuid4()),
        "thread_id": str(data.thread_id),
        "template": data.template,
        "status": BlueprintStatus.GENERATING,
        "zones": data.custom_zones or _generate_default_zones(data.template),
        "metadata": {
            "options": data.options or {},
            "source": "thread_projection",
            "immutable_source": True  # Thread is truth
        },
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "created_by": str(user_id),
        "version": 1
    }
    
    _blueprints[blueprint["id"]] = blueprint
    
    # Background: populate zones from Thread data
    background_tasks.add_task(_populate_blueprint_from_thread, blueprint["id"], data.thread_id)
    
    logger.info(f"XR Blueprint created: {blueprint['id']} for thread {data.thread_id}")
    
    return blueprint


@router.get("/blueprints", response_model=List[XRBlueprint])
async def list_blueprints(
    thread_id: Optional[UUID] = None,
    template: Optional[XRTemplate] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """List XR blueprints."""
    user_id = get_current_user_id()
    
    blueprints = [
        bp for bp in _blueprints.values()
        if bp["created_by"] == str(user_id)
    ]
    
    if thread_id:
        blueprints = [bp for bp in blueprints if bp["thread_id"] == str(thread_id)]
    if template:
        blueprints = [bp for bp in blueprints if bp["template"] == template]
    
    return sorted(blueprints, key=lambda x: x["updated_at"], reverse=True)[:limit]


@router.get("/blueprints/{blueprint_id}", response_model=XRBlueprint)
async def get_blueprint(blueprint_id: UUID):
    """Get a specific blueprint."""
    user_id = get_current_user_id()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    return bp


@router.put("/blueprints/{blueprint_id}", response_model=XRBlueprint)
async def update_blueprint(
    blueprint_id: UUID,
    zones: Optional[List[XRZoneConfig]] = None,
    template: Optional[XRTemplate] = None
):
    """
    Update blueprint configuration.
    Note: This updates the PROJECTION, not the Thread.
    """
    user_id = get_current_user_id()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    if zones:
        bp["zones"] = [z.dict() if hasattr(z, 'dict') else z for z in zones]
    if template:
        bp["template"] = template
    
    bp["updated_at"] = datetime.utcnow().isoformat()
    bp["version"] += 1
    
    logger.info(f"Blueprint updated: {blueprint_id} v{bp['version']}")
    
    return bp


@router.post("/blueprints/{blueprint_id}/refresh", response_model=XRBlueprint)
async def refresh_blueprint(
    blueprint_id: UUID,
    background_tasks: BackgroundTasks
):
    """
    Refresh blueprint from Thread (re-sync projection).
    Use when Thread has been updated.
    """
    user_id = get_current_user_id()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    bp["status"] = BlueprintStatus.GENERATING
    bp["updated_at"] = datetime.utcnow().isoformat()
    
    # Re-populate from Thread
    background_tasks.add_task(
        _populate_blueprint_from_thread, 
        blueprint_id, 
        UUID(bp["thread_id"])
    )
    
    return bp


@router.delete("/blueprints/{blueprint_id}")
async def delete_blueprint(blueprint_id: UUID):
    """Delete a blueprint."""
    user_id = get_current_user_id()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    del _blueprints[str(blueprint_id)]
    
    return {"status": "deleted", "blueprint_id": str(blueprint_id)}


@router.get("/blueprints/{blueprint_id}/zones/{zone}", response_model=XRZoneConfig)
async def get_zone(blueprint_id: UUID, zone: XRZone):
    """Get a specific zone from a blueprint."""
    user_id = get_current_user_id()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    for z in bp["zones"]:
        if z["zone"] == zone:
            return z
    
    raise HTTPException(status_code=404, detail=f"Zone {zone} not found")


# ============================================================================
# SESSION ENDPOINTS (8-11)
# ============================================================================

@router.post("/sessions", response_model=XRSession, status_code=201)
async def start_session(
    blueprint_id: UUID,
    device_type: str = Query("quest3", description="XR device type")
):
    """Start an XR viewing session."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    bp = _blueprints.get(str(blueprint_id))
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    
    if bp["created_by"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    session = {
        "id": str(uuid4()),
        "blueprint_id": str(blueprint_id),
        "user_id": str(user_id),
        "started_at": now.isoformat(),
        "ended_at": None,
        "device_type": device_type,
        "interactions": 0
    }
    
    _sessions[session["id"]] = session
    
    logger.info(f"XR Session started: {session['id']} on {device_type}")
    
    return session


@router.get("/sessions", response_model=List[XRSession])
async def list_sessions(
    blueprint_id: Optional[UUID] = None,
    active_only: bool = False,
    limit: int = Query(20, ge=1, le=100)
):
    """List XR sessions."""
    user_id = get_current_user_id()
    
    sessions = [
        s for s in _sessions.values()
        if s["user_id"] == str(user_id)
    ]
    
    if blueprint_id:
        sessions = [s for s in sessions if s["blueprint_id"] == str(blueprint_id)]
    if active_only:
        sessions = [s for s in sessions if s["ended_at"] is None]
    
    return sorted(sessions, key=lambda x: x["started_at"], reverse=True)[:limit]


@router.post("/sessions/{session_id}/end", response_model=XRSession)
async def end_session(session_id: UUID):
    """End an XR session."""
    user_id = get_current_user_id()
    
    session = _sessions.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["user_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    session["ended_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"XR Session ended: {session_id} with {session['interactions']} interactions")
    
    return session


@router.post("/sessions/{session_id}/interact")
async def record_interaction(
    session_id: UUID,
    zone: XRZone,
    action: str,
    data: Optional[Dict[str, Any]] = None
):
    """
    Record an interaction in XR.
    Interactions are READ-ONLY visualizations.
    Any edits must go through Thread API.
    """
    user_id = get_current_user_id()
    
    session = _sessions.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session["user_id"] != str(user_id):
        raise HTTPException(status_code=403, detail="Identity boundary violation")
    
    session["interactions"] += 1
    
    # Log interaction but don't modify Thread
    logger.info(f"XR Interaction: {session_id} - {zone} - {action}")
    
    return {
        "status": "recorded",
        "session_id": str(session_id),
        "zone": zone,
        "action": action,
        "note": "XR is read-only projection. Edit via Thread API."
    }


# ============================================================================
# TEMPLATE ENDPOINTS (12-13)
# ============================================================================

@router.get("/templates")
async def list_templates():
    """List available XR templates."""
    return {
        "templates": [
            {
                "id": XRTemplate.PERSONAL_ROOM,
                "name": "Personal Room",
                "description": "Cozy space for personal threads",
                "zones": 6,
                "recommended_for": ["Personal sphere"]
            },
            {
                "id": XRTemplate.BUSINESS_ROOM,
                "name": "Business Room",
                "description": "Professional space for business threads",
                "zones": 6,
                "recommended_for": ["Business sphere", "My Team sphere"]
            },
            {
                "id": XRTemplate.CAUSE_ROOM,
                "name": "Cause Room",
                "description": "Community space for collective threads",
                "zones": 6,
                "recommended_for": ["Community sphere"]
            },
            {
                "id": XRTemplate.LAB_ROOM,
                "name": "Lab Room",
                "description": "Research space for scholarly threads",
                "zones": 6,
                "recommended_for": ["Scholar sphere", "Creative Studio"]
            },
            {
                "id": XRTemplate.CUSTOM_ROOM,
                "name": "Custom Room",
                "description": "Fully customizable space",
                "zones": "variable",
                "recommended_for": ["Any sphere"]
            }
        ]
    }


@router.get("/templates/{template_id}/preview")
async def preview_template(template_id: XRTemplate):
    """Get preview data for a template."""
    zones = _generate_default_zones(template_id)
    
    return {
        "template": template_id,
        "zones": zones,
        "preview_url": f"/assets/xr/previews/{template_id.value}.glb",
        "skybox": f"/assets/xr/skyboxes/{template_id.value}.hdr"
    }


# ============================================================================
# STATS & HEALTH (14-15)
# ============================================================================

@router.get("/stats")
async def get_xr_stats():
    """Get XR usage statistics."""
    user_id = get_current_user_id()
    
    user_blueprints = [bp for bp in _blueprints.values() if bp["created_by"] == str(user_id)]
    user_sessions = [s for s in _sessions.values() if s["user_id"] == str(user_id)]
    
    active_sessions = [s for s in user_sessions if s["ended_at"] is None]
    total_interactions = sum(s["interactions"] for s in user_sessions)
    
    return {
        "blueprints": len(user_blueprints),
        "total_sessions": len(user_sessions),
        "active_sessions": len(active_sessions),
        "total_interactions": total_interactions,
        "templates_used": list(set(bp["template"] for bp in user_blueprints)),
        "devices": list(set(s["device_type"] for s in user_sessions))
    }


@router.get("/health")
async def xr_health():
    """XR system health check."""
    return {
        "status": "healthy",
        "renderer": "webxr",
        "templates_available": 5,
        "zones_supported": 6,
        "devices_supported": ["quest2", "quest3", "vision_pro", "browser"],
        "note": "XR environments are projections of Thread data (read-only)"
    }


# ============================================================================
# INTERNAL FUNCTIONS
# ============================================================================

async def _populate_blueprint_from_thread(blueprint_id: str, thread_id: UUID):
    """Background task: Populate blueprint zones from Thread data."""
    import asyncio
    
    # Simulate processing time
    await asyncio.sleep(1)
    
    bp = _blueprints.get(blueprint_id)
    if not bp:
        return
    
    # TODO: Fetch actual Thread data and populate zones
    # For now, mark as ready
    bp["status"] = BlueprintStatus.READY
    bp["updated_at"] = datetime.utcnow().isoformat()
    
    # Add mock objects to zones
    for zone in bp["zones"]:
        if zone["zone"] == XRZone.INTENT_WALL:
            zone["objects"] = [{
                "id": str(uuid4()),
                "type": "text_panel",
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1},
                "data": {"text": "Thread founding intent goes here"},
                "interactive": True
            }]
    
    logger.info(f"Blueprint populated from thread: {blueprint_id}")
