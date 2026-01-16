"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — LAYOUT ENGINE ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase B2: Backend Routers
Date: 8 Janvier 2026

R&D COMPLIANCE:
- Rule #1: HTTP 423 on DELETE layout, RESET layout
- Rule #3: HTTP 403 on owner_id mismatch
- Rule #6: id, created_by, created_at on all entities
- Rule #7: Frozen architecture (9 spheres, 6 sections max)
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/api/v2/layout-engine", tags=["Layout Engine"])


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereType(str, Enum):
    """Les 9 sphères CHE·NU - FROZEN ARCHITECTURE."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    STUDIO = "studio"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"


class BureauSection(str, Enum):
    """Les 6 sections de bureau - FROZEN ARCHITECTURE."""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


# Maximum 6 sections par bureau - FROZEN
MAX_BUREAU_SECTIONS = 6

# Exactement 9 sphères - FROZEN
SPHERE_COUNT = 9


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class LayoutCreate(BaseModel):
    """Création d'un layout."""
    name: str = Field(..., min_length=1, max_length=100)
    sphere_id: SphereType
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class LayoutUpdate(BaseModel):
    """Mise à jour d'un layout."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None


class BureauConfig(BaseModel):
    """Configuration d'un bureau."""
    sections: List[BureauSection] = Field(
        default_factory=lambda: list(BureauSection),
        max_length=MAX_BUREAU_SECTIONS  # R&D Rule #7: Max 6 sections
    )
    layout_type: str = "grid"
    columns: int = Field(default=2, ge=1, le=4)
    compact_mode: bool = False


class WidgetPosition(BaseModel):
    """Position d'un widget."""
    widget_id: str
    section: BureauSection
    order: int = Field(ge=0)
    width: int = Field(default=1, ge=1, le=4)
    height: int = Field(default=1, ge=1, le=4)


class LayoutResponse(BaseModel):
    """Réponse layout."""
    id: str
    name: str
    sphere_id: str
    description: Optional[str]
    config: Dict[str, Any]
    is_default: bool
    owner_id: str
    created_by: str  # R&D Rule #6
    created_at: str  # R&D Rule #6
    updated_at: str
    synthetic: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

_layouts_db: Dict[str, Dict[str, Any]] = {}
_checkpoints_db: Dict[str, Dict[str, Any]] = {}


def get_current_user_id() -> str:
    """Mock: retourne l'ID utilisateur courant."""
    return "user_123"


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - LAYOUTS CRUD
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/layouts", response_model=List[LayoutResponse])
async def list_layouts(
    sphere_id: Optional[SphereType] = Query(None, description="Filter by sphere"),
    is_default: Optional[bool] = Query(None, description="Filter default layouts"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Liste les layouts de l'utilisateur.
    
    R&D Rule #3: Filtre automatique par owner_id
    R&D Rule #5: Tri chronologique (pas de ranking)
    """
    user_id = get_current_user_id()
    
    # Filtrer par owner
    layouts = [
        l for l in _layouts_db.values()
        if l["owner_id"] == user_id
    ]
    
    # Filtrer par sphere si spécifié
    if sphere_id:
        layouts = [l for l in layouts if l["sphere_id"] == sphere_id.value]
    
    # Filtrer par is_default si spécifié
    if is_default is not None:
        layouts = [l for l in layouts if l["is_default"] == is_default]
    
    # R&D Rule #5: Tri chronologique
    layouts.sort(key=lambda x: x["created_at"], reverse=True)
    
    return layouts[skip:skip + limit]


@router.post("/layouts", response_model=LayoutResponse, status_code=201)
async def create_layout(layout: LayoutCreate):
    """
    Crée un nouveau layout.
    
    R&D Rule #6: Traçabilité complète
    R&D Rule #7: Validation architecture frozen
    """
    user_id = get_current_user_id()
    now = datetime.utcnow().isoformat() + "Z"
    
    # Vérifier que la sphère est valide (R&D Rule #7)
    if layout.sphere_id not in SphereType:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sphere. Must be one of {[s.value for s in SphereType]}"
        )
    
    layout_id = str(uuid4())
    
    new_layout = {
        "id": layout_id,
        "name": layout.name,
        "sphere_id": layout.sphere_id.value,
        "description": layout.description,
        "config": layout.config or {},
        "is_default": False,
        "owner_id": user_id,
        "created_by": user_id,  # R&D Rule #6
        "created_at": now,      # R&D Rule #6
        "updated_at": now,
        "synthetic": True
    }
    
    _layouts_db[layout_id] = new_layout
    
    return new_layout


@router.get("/layouts/{layout_id}", response_model=LayoutResponse)
async def get_layout(layout_id: str = Path(..., description="Layout ID")):
    """
    Récupère un layout par ID.
    
    R&D Rule #3: Vérifie ownership
    """
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    # R&D Rule #3: Identity boundary
    if layout["owner_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: layout belongs to another user"
        )
    
    return layout


@router.put("/layouts/{layout_id}", response_model=LayoutResponse)
async def update_layout(
    layout_id: str = Path(...),
    update: LayoutUpdate = Body(...)
):
    """
    Met à jour un layout.
    
    R&D Rule #3: Vérifie ownership
    """
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    # R&D Rule #3: Identity boundary
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Appliquer les mises à jour
    if update.name is not None:
        layout["name"] = update.name
    if update.description is not None:
        layout["description"] = update.description
    if update.config is not None:
        layout["config"] = update.config
    if update.is_default is not None:
        layout["is_default"] = update.is_default
    
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return layout


@router.delete("/layouts/{layout_id}")
async def delete_layout(
    layout_id: str = Path(...),
    checkpoint_id: Optional[str] = Query(None, description="Approved checkpoint ID")
):
    """
    Supprime un layout.
    
    R&D Rule #1: HTTP 423 - Nécessite checkpoint approuvé
    R&D Rule #3: Vérifie ownership
    """
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    # R&D Rule #3: Identity boundary
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Checkpoint requis
    if not checkpoint_id:
        # Créer un checkpoint et retourner 423
        cp_id = str(uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        
        _checkpoints_db[cp_id] = {
            "id": cp_id,
            "action_type": "delete_layout",
            "status": "pending",
            "user_id": user_id,
            "context": {"layout_id": layout_id, "layout_name": layout["name"]},
            "created_at": now,
            "created_by": user_id
        }
        
        raise HTTPException(
            status_code=423,
            detail={
                "message": "Checkpoint required for layout deletion",
                "checkpoint_id": cp_id,
                "action": "delete_layout",
                "resource_id": layout_id
            }
        )
    
    # Vérifier que le checkpoint est approuvé
    if checkpoint_id not in _checkpoints_db:
        raise HTTPException(status_code=400, detail="Invalid checkpoint")
    
    checkpoint = _checkpoints_db[checkpoint_id]
    if checkpoint["status"] != "approved":
        raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    # Supprimer le layout
    del _layouts_db[layout_id]
    
    return {"message": "Layout deleted", "id": layout_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - BUREAU CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/layouts/{layout_id}/bureau", response_model=BureauConfig)
async def get_bureau_config(layout_id: str = Path(...)):
    """Récupère la configuration du bureau."""
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Retourner config bureau ou défaut
    bureau_config = layout["config"].get("bureau", {})
    
    return BureauConfig(
        sections=bureau_config.get("sections", list(BureauSection)),
        layout_type=bureau_config.get("layout_type", "grid"),
        columns=bureau_config.get("columns", 2),
        compact_mode=bureau_config.get("compact_mode", False)
    )


@router.put("/layouts/{layout_id}/bureau", response_model=BureauConfig)
async def update_bureau_config(
    layout_id: str = Path(...),
    config: BureauConfig = Body(...)
):
    """
    Met à jour la configuration du bureau.
    
    R&D Rule #7: Maximum 6 sections (frozen architecture)
    """
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #7: Valider max 6 sections
    if len(config.sections) > MAX_BUREAU_SECTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_BUREAU_SECTIONS} sections allowed (frozen architecture)"
        )
    
    layout["config"]["bureau"] = {
        "sections": [s.value for s in config.sections],
        "layout_type": config.layout_type,
        "columns": config.columns,
        "compact_mode": config.compact_mode
    }
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return config


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/layouts/{layout_id}/widgets", response_model=List[WidgetPosition])
async def list_widgets(layout_id: str = Path(...)):
    """Liste les widgets d'un layout."""
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    widgets = layout["config"].get("widgets", [])
    return widgets


@router.post("/layouts/{layout_id}/widgets", response_model=WidgetPosition, status_code=201)
async def add_widget(
    layout_id: str = Path(...),
    widget: WidgetPosition = Body(...)
):
    """Ajoute un widget au layout."""
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #7: Vérifier que la section est valide
    if widget.section not in BureauSection:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section. Must be one of {[s.value for s in BureauSection]}"
        )
    
    if "widgets" not in layout["config"]:
        layout["config"]["widgets"] = []
    
    layout["config"]["widgets"].append(widget.model_dump())
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return widget


@router.delete("/layouts/{layout_id}/widgets/{widget_id}")
async def remove_widget(
    layout_id: str = Path(...),
    widget_id: str = Path(...)
):
    """Supprime un widget du layout."""
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    widgets = layout["config"].get("widgets", [])
    layout["config"]["widgets"] = [w for w in widgets if w.get("widget_id") != widget_id]
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Widget removed", "widget_id": widget_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - TEMPLATES & DEFAULTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/templates")
async def list_templates():
    """
    Liste les templates de layout disponibles.
    
    Templates système (read-only, partagés).
    """
    return [
        {
            "id": "template_default",
            "name": "Default Layout",
            "description": "Standard 2-column grid layout",
            "preview_url": "/assets/templates/default.png",
            "config": {"columns": 2, "layout_type": "grid"}
        },
        {
            "id": "template_compact",
            "name": "Compact Layout",
            "description": "Dense single-column layout",
            "preview_url": "/assets/templates/compact.png",
            "config": {"columns": 1, "layout_type": "list", "compact_mode": True}
        },
        {
            "id": "template_dashboard",
            "name": "Dashboard Layout",
            "description": "4-column dashboard with widgets",
            "preview_url": "/assets/templates/dashboard.png",
            "config": {"columns": 4, "layout_type": "dashboard"}
        }
    ]


@router.post("/layouts/{layout_id}/set-default")
async def set_default_layout(
    layout_id: str = Path(...),
    sphere_id: SphereType = Query(..., description="Sphere to set default for")
):
    """Définit un layout comme défaut pour une sphère."""
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Retirer le défaut des autres layouts de cette sphère
    for lid, l in _layouts_db.items():
        if l["owner_id"] == user_id and l["sphere_id"] == sphere_id.value:
            l["is_default"] = False
    
    # Définir ce layout comme défaut
    layout["is_default"] = True
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Default layout set", "layout_id": layout_id, "sphere": sphere_id.value}


@router.post("/layouts/{layout_id}/reset")
async def reset_layout(
    layout_id: str = Path(...),
    checkpoint_id: Optional[str] = Query(None)
):
    """
    Réinitialise un layout aux valeurs par défaut.
    
    R&D Rule #1: HTTP 423 - Nécessite checkpoint
    """
    user_id = get_current_user_id()
    
    if layout_id not in _layouts_db:
        raise HTTPException(status_code=404, detail="Layout not found")
    
    layout = _layouts_db[layout_id]
    
    if layout["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Checkpoint requis
    if not checkpoint_id:
        cp_id = str(uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        
        _checkpoints_db[cp_id] = {
            "id": cp_id,
            "action_type": "reset_layout",
            "status": "pending",
            "user_id": user_id,
            "context": {"layout_id": layout_id},
            "created_at": now,
            "created_by": user_id
        }
        
        raise HTTPException(
            status_code=423,
            detail={
                "message": "Checkpoint required for layout reset",
                "checkpoint_id": cp_id,
                "action": "reset_layout"
            }
        )
    
    # Vérifier checkpoint approuvé
    if checkpoint_id not in _checkpoints_db:
        raise HTTPException(status_code=400, detail="Invalid checkpoint")
    
    if _checkpoints_db[checkpoint_id]["status"] != "approved":
        raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    # Réinitialiser
    layout["config"] = {}
    layout["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Layout reset to defaults", "layout_id": layout_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - SPHERES INFO (READ-ONLY)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/spheres")
async def list_spheres():
    """
    Liste les 9 sphères CHE·NU.
    
    R&D Rule #7: Architecture frozen - exactement 9 sphères.
    """
    return [
        {"id": s.value, "name": s.name.replace("_", " ").title(), "order": i}
        for i, s in enumerate(SphereType)
    ]


@router.get("/sections")
async def list_sections():
    """
    Liste les 6 sections de bureau.
    
    R&D Rule #7: Architecture frozen - maximum 6 sections.
    """
    return [
        {"id": s.value, "name": s.name.replace("_", " ").title(), "order": i}
        for i, s in enumerate(BureauSection)
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - STATS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_layout_stats():
    """Statistiques des layouts utilisateur."""
    user_id = get_current_user_id()
    
    user_layouts = [l for l in _layouts_db.values() if l["owner_id"] == user_id]
    
    # Compter par sphère
    by_sphere = {}
    for s in SphereType:
        by_sphere[s.value] = len([l for l in user_layouts if l["sphere_id"] == s.value])
    
    return {
        "total_layouts": len(user_layouts),
        "by_sphere": by_sphere,
        "default_count": len([l for l in user_layouts if l["is_default"]]),
        "spheres_available": SPHERE_COUNT,
        "max_sections_per_bureau": MAX_BUREAU_SECTIONS
    }
