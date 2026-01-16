"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V75 — XR ENVIRONMENT API                          ║
║                                                                              ║
║  Endpoints pour génération et gestion des environnements XR                  ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel
from enum import Enum

router = APIRouter(prefix="/xr", tags=["XR"])

# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class XRTemplateType(str, Enum):
    PERSONAL_ROOM = "personal_room"
    BUSINESS_ROOM = "business_room"
    CAUSE_ROOM = "cause_room"
    LAB_ROOM = "lab_room"
    CUSTOM_ROOM = "custom_room"

class XRZoneType(str, Enum):
    INTENT_WALL = "intent_wall"
    DECISION_WALL = "decision_wall"
    ACTION_TABLE = "action_table"
    MEMORY_KIOSK = "memory_kiosk"
    TIMELINE_STRIP = "timeline_strip"
    RESOURCE_SHELF = "resource_shelf"

class Vector3(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class XRZone(BaseModel):
    id: str
    type: XRZoneType
    position: Vector3
    rotation: Vector3
    scale: Vector3
    content: Optional[dict] = None
    interactive: bool = True
    visible: bool = True

class XRLighting(BaseModel):
    ambient_color: str = "#1a1a2e"
    ambient_intensity: float = 0.3
    directional_color: str = "#ffffff"
    directional_intensity: float = 0.8
    fog_enabled: bool = False
    fog_color: str = "#1a1a2e"
    fog_density: float = 0.02

class XREnvironment(BaseModel):
    id: str
    template: XRTemplateType
    thread_id: str
    sphere_id: str
    zones: List[XRZone]
    lighting: XRLighting
    created_at: datetime
    updated_at: datetime

class XRTemplate(BaseModel):
    id: str
    type: XRTemplateType
    name: str
    description: str
    default_zones: List[XRZoneType]
    preview_url: Optional[str] = None

class GenerateXRRequest(BaseModel):
    thread_id: str
    sphere_id: str
    template: Optional[XRTemplateType] = None

# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

XR_TEMPLATES = [
    XRTemplate(
        id="tpl-personal",
        type=XRTemplateType.PERSONAL_ROOM,
        name="Personal Room",
        description="Espace personnel calme pour réflexion et organisation",
        default_zones=[XRZoneType.INTENT_WALL, XRZoneType.ACTION_TABLE, XRZoneType.MEMORY_KIOSK]
    ),
    XRTemplate(
        id="tpl-business",
        type=XRTemplateType.BUSINESS_ROOM,
        name="Business Room",
        description="Salle de réunion professionnelle avec outils de décision",
        default_zones=[XRZoneType.INTENT_WALL, XRZoneType.DECISION_WALL, XRZoneType.ACTION_TABLE, XRZoneType.TIMELINE_STRIP]
    ),
    XRTemplate(
        id="tpl-cause",
        type=XRTemplateType.CAUSE_ROOM,
        name="Cause Room",
        description="Espace collaboratif pour projets communautaires",
        default_zones=[XRZoneType.INTENT_WALL, XRZoneType.RESOURCE_SHELF]
    ),
    XRTemplate(
        id="tpl-lab",
        type=XRTemplateType.LAB_ROOM,
        name="Lab Room",
        description="Laboratoire de recherche et expérimentation",
        default_zones=[XRZoneType.INTENT_WALL, XRZoneType.ACTION_TABLE, XRZoneType.MEMORY_KIOSK]
    ),
    XRTemplate(
        id="tpl-custom",
        type=XRTemplateType.CUSTOM_ROOM,
        name="Custom Room",
        description="Espace personnalisable",
        default_zones=[]
    ),
]

ENVIRONMENTS_DB: dict[str, XREnvironment] = {}

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_zone(zone_type: XRZoneType, index: int) -> XRZone:
    """Create a zone with default positioning"""
    positions = {
        XRZoneType.INTENT_WALL: Vector3(x=0, y=2, z=-5),
        XRZoneType.DECISION_WALL: Vector3(x=-4, y=2, z=-3),
        XRZoneType.ACTION_TABLE: Vector3(x=0, y=1, z=0),
        XRZoneType.MEMORY_KIOSK: Vector3(x=4, y=1.5, z=-2),
        XRZoneType.TIMELINE_STRIP: Vector3(x=0, y=0.5, z=3),
        XRZoneType.RESOURCE_SHELF: Vector3(x=4, y=2, z=-3),
    }
    return XRZone(
        id=f"zone-{zone_type.value}-{uuid4().hex[:8]}",
        type=zone_type,
        position=positions.get(zone_type, Vector3()),
        rotation=Vector3(),
        scale=Vector3(x=1, y=1, z=1),
    )

def get_template_for_sphere(sphere_id: str) -> XRTemplateType:
    """Map sphere to default template"""
    mapping = {
        "personal": XRTemplateType.PERSONAL_ROOM,
        "business": XRTemplateType.BUSINESS_ROOM,
        "community": XRTemplateType.CAUSE_ROOM,
        "scholar": XRTemplateType.LAB_ROOM,
    }
    for key, template in mapping.items():
        if key in sphere_id.lower():
            return template
    return XRTemplateType.PERSONAL_ROOM

# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/templates", response_model=List[XRTemplate])
async def list_templates():
    """List all available XR templates."""
    return XR_TEMPLATES

@router.get("/templates/{template_type}", response_model=XRTemplate)
async def get_template(template_type: XRTemplateType):
    """Get a specific XR template."""
    for tpl in XR_TEMPLATES:
        if tpl.type == template_type:
            return tpl
    raise HTTPException(status_code=404, detail="Template not found")

@router.get("/environments", response_model=List[XREnvironment])
async def list_environments():
    """List all generated XR environments."""
    return list(ENVIRONMENTS_DB.values())

@router.post("/generate", response_model=XREnvironment)
async def generate_environment(request: GenerateXRRequest):
    """Generate a new XR environment for a thread."""
    # Determine template
    template_type = request.template or get_template_for_sphere(request.sphere_id)
    
    # Find template
    template = None
    for tpl in XR_TEMPLATES:
        if tpl.type == template_type:
            template = tpl
            break
    
    if not template:
        template = XR_TEMPLATES[0]  # Default to personal
    
    # Create zones
    zones = [create_zone(zt, i) for i, zt in enumerate(template.default_zones)]
    
    # Create environment
    env = XREnvironment(
        id=f"xr-{uuid4().hex[:12]}",
        template=template_type,
        thread_id=request.thread_id,
        sphere_id=request.sphere_id,
        zones=zones,
        lighting=XRLighting(
            ambient_color="#16213e" if template_type == XRTemplateType.PERSONAL_ROOM else "#1a1a2e",
            fog_enabled=template_type in [XRTemplateType.PERSONAL_ROOM, XRTemplateType.LAB_ROOM],
        ),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    ENVIRONMENTS_DB[env.id] = env
    return env

@router.get("/environments/{env_id}", response_model=XREnvironment)
async def get_environment(env_id: str):
    """Get a specific XR environment."""
    if env_id not in ENVIRONMENTS_DB:
        raise HTTPException(status_code=404, detail="Environment not found")
    return ENVIRONMENTS_DB[env_id]

@router.get("/environments/{env_id}/preview")
async def preview_environment(env_id: str):
    """Get preview data for an XR environment."""
    if env_id not in ENVIRONMENTS_DB:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    env = ENVIRONMENTS_DB[env_id]
    return {
        "id": env.id,
        "template": env.template,
        "zone_count": len(env.zones),
        "preview_url": f"/static/xr-previews/{env.template.value}.jpg",
        "thumbnail_url": f"/static/xr-thumbnails/{env.template.value}.jpg",
    }

@router.delete("/environments/{env_id}")
async def delete_environment(env_id: str):
    """Delete an XR environment."""
    if env_id not in ENVIRONMENTS_DB:
        raise HTTPException(status_code=404, detail="Environment not found")
    del ENVIRONMENTS_DB[env_id]
    return {"success": True, "message": "Environment deleted"}
