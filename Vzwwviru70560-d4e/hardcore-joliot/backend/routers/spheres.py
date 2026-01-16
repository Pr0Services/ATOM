"""
CHE·NU™ V75 Backend - Spheres Router

RÈGLE ABSOLUE: ARCHITECTURE GELÉE
- Exactement 9 sphères canoniques
- Exactement 6 bureaux par sphère
- Aucune modification de structure autorisée

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from config import get_db
from config.settings import CANONICAL_SPHERES, CANONICAL_BUREAUS
from schemas.base import BaseResponse, SphereId, BureauId
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class SphereStats(BaseModel):
    """Sphere statistics."""
    threads_count: int = 0
    agents_count: int = 0
    files_count: int = 0
    decisions_pending: int = 0


class Sphere(BaseModel):
    """Sphere entity (9 canonical)."""
    id: SphereId
    name: str
    description: str
    icon: str
    color: str
    is_active: bool = True
    stats: Optional[SphereStats] = None
    bureaus: List["Bureau"] = []


class Bureau(BaseModel):
    """Bureau entity (6 per sphere)."""
    id: BureauId
    name: str
    description: str
    capabilities: List[str] = []
    is_active: bool = True


class ActivityItem(BaseModel):
    """Sphere activity item."""
    id: str
    type: str
    description: str
    timestamp: datetime
    sphere_id: str
    bureau_id: Optional[str] = None


# ============================================================================
# CANONICAL DATA (FROZEN)
# ============================================================================

SPHERE_METADATA = {
    SphereId.PERSONAL: {
        "name": "Personnel",
        "description": "Votre espace personnel et vie quotidienne",
        "icon": "👤",
        "color": "#D8B26A",
    },
    SphereId.BUSINESS: {
        "name": "Business",
        "description": "Gestion d'entreprise et activités professionnelles",
        "icon": "💼",
        "color": "#3F7249",
    },
    SphereId.GOVERNMENT: {
        "name": "Gouvernement & Institutions",
        "description": "Interactions avec les institutions gouvernementales",
        "icon": "🏛️",
        "color": "#8D8371",
    },
    SphereId.STUDIO: {
        "name": "Studio de création",
        "description": "Création artistique et design",
        "icon": "🎨",
        "color": "#3EB4A2",
    },
    SphereId.COMMUNITY: {
        "name": "Communauté",
        "description": "Associations et groupes communautaires",
        "icon": "🤝",
        "color": "#2F4C39",
    },
    SphereId.SOCIAL: {
        "name": "Social & Médias",
        "description": "Réseaux sociaux et communication",
        "icon": "📱",
        "color": "#7A593A",
    },
    SphereId.ENTERTAINMENT: {
        "name": "Divertissement",
        "description": "Loisirs et divertissement",
        "icon": "🎬",
        "color": "#D8B26A",
    },
    SphereId.TEAM: {
        "name": "Mon équipe",
        "description": "Collaboration et gestion d'équipe",
        "icon": "👥",
        "color": "#3F7249",
    },
    SphereId.SCHOLAR: {
        "name": "Scholar",
        "description": "Éducation et recherche académique",
        "icon": "🎓",
        "color": "#3EB4A2",
    },
}

BUREAU_METADATA = {
    BureauId.QUICK_CAPTURE: {
        "name": "Quick Capture",
        "description": "Capture rapide d'idées et notes",
        "capabilities": ["notes", "voice", "images", "links"],
    },
    BureauId.RESUME_WORKSPACE: {
        "name": "Resume Workspace",
        "description": "Reprendre là où vous avez arrêté",
        "capabilities": ["recent", "pinned", "drafts"],
    },
    BureauId.THREADS: {
        "name": "Threads",
        "description": "Conversations et discussions continues",
        "capabilities": ["conversations", "decisions", "history"],
    },
    BureauId.DATA_FILES: {
        "name": "Data Files",
        "description": "Documents et fichiers",
        "capabilities": ["upload", "organize", "search", "share"],
    },
    BureauId.ACTIVE_AGENTS: {
        "name": "Active Agents",
        "description": "Agents IA assignés",
        "capabilities": ["manage", "assign", "monitor"],
    },
    BureauId.MEETINGS: {
        "name": "Meetings",
        "description": "Réunions et calendrier",
        "capabilities": ["schedule", "notes", "recordings"],
    },
}


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=BaseResponse[List[Sphere]])
async def list_spheres(
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    List all 9 canonical spheres.
    
    RÈGLE: Structure GELÉE - toujours exactement 9 sphères.
    """
    spheres = []
    
    for sphere_id in SphereId:
        meta = SPHERE_METADATA.get(sphere_id, {})
        sphere = Sphere(
            id=sphere_id,
            name=meta.get("name", sphere_id.value),
            description=meta.get("description", ""),
            icon=meta.get("icon", "🔵"),
            color=meta.get("color", "#888888"),
            is_active=True,
            stats=SphereStats(
                threads_count=5,
                agents_count=2,
                files_count=15,
            ),
        )
        spheres.append(sphere)
    
    return BaseResponse(success=True, data=spheres)


@router.get("/{sphere_id}", response_model=BaseResponse[Sphere])
async def get_sphere(
    sphere_id: SphereId,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get sphere details."""
    meta = SPHERE_METADATA.get(sphere_id, {})
    
    # Build bureaus
    bureaus = []
    for bureau_id in BureauId:
        bureau_meta = BUREAU_METADATA.get(bureau_id, {})
        bureaus.append(Bureau(
            id=bureau_id,
            name=bureau_meta.get("name", bureau_id.value),
            description=bureau_meta.get("description", ""),
            capabilities=bureau_meta.get("capabilities", []),
            is_active=True,
        ))
    
    sphere = Sphere(
        id=sphere_id,
        name=meta.get("name", sphere_id.value),
        description=meta.get("description", ""),
        icon=meta.get("icon", "🔵"),
        color=meta.get("color", "#888888"),
        is_active=True,
        stats=SphereStats(
            threads_count=8,
            agents_count=3,
            files_count=24,
            decisions_pending=2,
        ),
        bureaus=bureaus,
    )
    
    return BaseResponse(success=True, data=sphere)


@router.get("/{sphere_id}/bureaus", response_model=BaseResponse[List[Bureau]])
async def get_sphere_bureaus(
    sphere_id: SphereId,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Get bureaus for a sphere.
    
    RÈGLE: Toujours exactement 6 bureaux.
    """
    bureaus = []
    for bureau_id in BureauId:
        bureau_meta = BUREAU_METADATA.get(bureau_id, {})
        bureaus.append(Bureau(
            id=bureau_id,
            name=bureau_meta.get("name", bureau_id.value),
            description=bureau_meta.get("description", ""),
            capabilities=bureau_meta.get("capabilities", []),
            is_active=True,
        ))
    
    return BaseResponse(success=True, data=bureaus)


@router.get("/{sphere_id}/activity", response_model=BaseResponse[dict])
async def get_sphere_activity(
    sphere_id: SphereId,
    user: dict = Depends(require_auth),
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Get recent activity in a sphere."""
    now = datetime.utcnow()
    
    activities = [
        ActivityItem(
            id="act-1",
            type="thread",
            description="New thread created in Threads bureau",
            timestamp=now,
            sphere_id=sphere_id.value,
            bureau_id="threads",
        ),
        ActivityItem(
            id="act-2",
            type="file",
            description="Document uploaded to Data Files",
            timestamp=now,
            sphere_id=sphere_id.value,
            bureau_id="data_files",
        ),
    ]
    
    return BaseResponse(
        success=True,
        data={"activities": activities[:limit]},
    )
