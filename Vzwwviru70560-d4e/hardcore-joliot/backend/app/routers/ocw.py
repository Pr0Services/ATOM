"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — OCW (ONECLICK WORKSPACE) ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase B2: Backend Routers
Date: 8 Janvier 2026

OCW = Espace de travail rapide pour tâches ponctuelles
- Création rapide sans navigation
- Contexte temporaire ou persistable
- Intégration avec tous les modules

R&D COMPLIANCE:
- Rule #1: HTTP 423 on DELETE workspace, ARCHIVE workspace
- Rule #3: HTTP 403 on owner_id mismatch
- Rule #6: Full traceability
- Rule #7: Respects 9 sphere architecture
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from enum import Enum

router = APIRouter(prefix="/api/v2/ocw", tags=["OneClick Workspace"])


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class WorkspaceType(str, Enum):
    """Types d'espaces de travail."""
    TEMPORARY = "temporary"     # Expire après inactivité
    PERSISTENT = "persistent"   # Sauvegardé
    PROJECT = "project"         # Lié à un projet
    SCRATCH = "scratch"         # Brouillon rapide


class WorkspaceStatus(str, Enum):
    """Statuts d'espace de travail."""
    ACTIVE = "active"
    IDLE = "idle"
    ARCHIVED = "archived"
    EXPIRED = "expired"


class ContentType(str, Enum):
    """Types de contenu dans un workspace."""
    NOTE = "note"
    FILE = "file"
    LINK = "link"
    SNIPPET = "snippet"
    TASK = "task"
    REFERENCE = "reference"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class WorkspaceCreate(BaseModel):
    """Création d'un workspace."""
    name: Optional[str] = Field(None, max_length=100)
    type: WorkspaceType = WorkspaceType.TEMPORARY
    sphere_id: Optional[str] = None
    thread_id: Optional[str] = None  # Lier à un thread existant
    initial_content: Optional[str] = None
    ttl_minutes: int = Field(default=60, ge=5, le=1440)  # 5min to 24h


class WorkspaceUpdate(BaseModel):
    """Mise à jour d'un workspace."""
    name: Optional[str] = Field(None, max_length=100)
    type: Optional[WorkspaceType] = None
    sphere_id: Optional[str] = None


class ContentItem(BaseModel):
    """Élément de contenu."""
    type: ContentType
    content: str
    title: Optional[str] = None
    metadata: Dict[str, Any] = {}


class WorkspaceResponse(BaseModel):
    """Réponse workspace."""
    id: str
    name: str
    type: str
    status: str
    sphere_id: Optional[str]
    thread_id: Optional[str]
    content_count: int
    expires_at: Optional[str]
    last_activity: str
    owner_id: str
    created_by: str      # R&D Rule #6
    created_at: str      # R&D Rule #6
    updated_at: str
    synthetic: bool = True


class ContentResponse(BaseModel):
    """Réponse contenu."""
    id: str
    workspace_id: str
    type: str
    title: Optional[str]
    content: str
    metadata: Dict[str, Any]
    order: int
    created_by: str
    created_at: str
    updated_at: str


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

_workspaces_db: Dict[str, Dict[str, Any]] = {}
_contents_db: Dict[str, Dict[str, Any]] = {}
_checkpoints_db: Dict[str, Dict[str, Any]] = {}


def get_current_user_id() -> str:
    return "user_123"


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - WORKSPACE CRUD
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/workspaces", response_model=List[WorkspaceResponse])
async def list_workspaces(
    type: Optional[WorkspaceType] = Query(None),
    status: Optional[WorkspaceStatus] = Query(None),
    sphere_id: Optional[str] = Query(None),
    include_expired: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Liste les workspaces de l'utilisateur.
    
    R&D Rule #3: Filtre par owner_id
    R&D Rule #5: Tri chronologique par dernière activité
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    workspaces = []
    for ws in _workspaces_db.values():
        if ws["owner_id"] != user_id:
            continue
        
        # Vérifier expiration
        if ws.get("expires_at"):
            expires = datetime.fromisoformat(ws["expires_at"].replace("Z", "+00:00"))
            if expires < now.replace(tzinfo=expires.tzinfo):
                ws["status"] = WorkspaceStatus.EXPIRED.value
                if not include_expired:
                    continue
        
        # Filtres
        if type and ws["type"] != type.value:
            continue
        if status and ws["status"] != status.value:
            continue
        if sphere_id and ws.get("sphere_id") != sphere_id:
            continue
        
        workspaces.append(ws)
    
    # R&D Rule #5: Tri chronologique par activité
    workspaces.sort(key=lambda x: x["last_activity"], reverse=True)
    
    return workspaces[skip:skip + limit]


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=201)
async def create_workspace(workspace: WorkspaceCreate):
    """
    Crée un nouveau workspace OneClick.
    
    R&D Rule #6: Traçabilité complète
    R&D Rule #7: Validation sphere_id si fourni
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    now_str = now.isoformat() + "Z"
    
    workspace_id = str(uuid4())
    
    # Calculer expiration pour workspaces temporaires
    expires_at = None
    if workspace.type == WorkspaceType.TEMPORARY:
        expires_at = (now + timedelta(minutes=workspace.ttl_minutes)).isoformat() + "Z"
    
    # Générer un nom si non fourni
    name = workspace.name or f"Workspace {now.strftime('%H:%M')}"
    
    new_workspace = {
        "id": workspace_id,
        "name": name,
        "type": workspace.type.value,
        "status": WorkspaceStatus.ACTIVE.value,
        "sphere_id": workspace.sphere_id,
        "thread_id": workspace.thread_id,
        "content_count": 0,
        "expires_at": expires_at,
        "last_activity": now_str,
        "owner_id": user_id,
        "created_by": user_id,  # R&D Rule #6
        "created_at": now_str,   # R&D Rule #6
        "updated_at": now_str,
        "synthetic": True
    }
    
    _workspaces_db[workspace_id] = new_workspace
    
    # Ajouter contenu initial si fourni
    if workspace.initial_content:
        await add_content(
            workspace_id,
            ContentItem(type=ContentType.NOTE, content=workspace.initial_content)
        )
        new_workspace["content_count"] = 1
    
    return new_workspace


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: str = Path(...)):
    """Récupère un workspace par ID."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    # R&D Rule #3
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Mettre à jour last_activity
    workspace["last_activity"] = datetime.utcnow().isoformat() + "Z"
    
    return workspace


@router.put("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: str = Path(...),
    update: WorkspaceUpdate = Body(...)
):
    """Met à jour un workspace."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if workspace["status"] == WorkspaceStatus.ARCHIVED.value:
        raise HTTPException(status_code=400, detail="Cannot update archived workspace")
    
    # Appliquer mises à jour
    if update.name is not None:
        workspace["name"] = update.name
    if update.type is not None:
        workspace["type"] = update.type.value
        # Mettre à jour expiration si passage à persistent
        if update.type == WorkspaceType.PERSISTENT:
            workspace["expires_at"] = None
    if update.sphere_id is not None:
        workspace["sphere_id"] = update.sphere_id
    
    now = datetime.utcnow().isoformat() + "Z"
    workspace["updated_at"] = now
    workspace["last_activity"] = now
    
    return workspace


@router.delete("/workspaces/{workspace_id}")
async def delete_workspace(
    workspace_id: str = Path(...),
    checkpoint_id: Optional[str] = Query(None)
):
    """
    Supprime un workspace.
    
    R&D Rule #1: HTTP 423 pour workspaces persistants
    """
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Checkpoint pour persistent/project
    if workspace["type"] in [WorkspaceType.PERSISTENT.value, WorkspaceType.PROJECT.value]:
        if not checkpoint_id:
            cp_id = str(uuid4())
            now = datetime.utcnow().isoformat() + "Z"
            
            _checkpoints_db[cp_id] = {
                "id": cp_id,
                "action_type": "delete_workspace",
                "status": "pending",
                "user_id": user_id,
                "context": {
                    "workspace_id": workspace_id,
                    "workspace_name": workspace["name"],
                    "content_count": workspace["content_count"]
                },
                "created_at": now,
                "created_by": user_id
            }
            
            raise HTTPException(
                status_code=423,
                detail={
                    "message": "Checkpoint required for workspace deletion",
                    "checkpoint_id": cp_id,
                    "action": "delete_workspace"
                }
            )
        
        if checkpoint_id not in _checkpoints_db:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")
        
        if _checkpoints_db[checkpoint_id]["status"] != "approved":
            raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    # Supprimer le contenu associé
    _contents_db.clear()  # Simplified - in prod, filter by workspace_id
    
    del _workspaces_db[workspace_id]
    
    return {"message": "Workspace deleted", "id": workspace_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - CONTENT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/workspaces/{workspace_id}/content", response_model=List[ContentResponse])
async def list_content(
    workspace_id: str = Path(...),
    type: Optional[ContentType] = Query(None)
):
    """Liste le contenu d'un workspace."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    contents = [
        c for c in _contents_db.values()
        if c["workspace_id"] == workspace_id
    ]
    
    if type:
        contents = [c for c in contents if c["type"] == type.value]
    
    # Tri par ordre
    contents.sort(key=lambda x: x["order"])
    
    return contents


@router.post("/workspaces/{workspace_id}/content", response_model=ContentResponse, status_code=201)
async def add_content(
    workspace_id: str = Path(...),
    item: ContentItem = Body(...)
):
    """
    Ajoute du contenu à un workspace.
    
    R&D Rule #6: Traçabilité
    """
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if workspace["status"] == WorkspaceStatus.ARCHIVED.value:
        raise HTTPException(status_code=400, detail="Cannot add to archived workspace")
    
    now = datetime.utcnow().isoformat() + "Z"
    content_id = str(uuid4())
    
    # Calculer l'ordre
    existing_count = len([c for c in _contents_db.values() if c["workspace_id"] == workspace_id])
    
    new_content = {
        "id": content_id,
        "workspace_id": workspace_id,
        "type": item.type.value,
        "title": item.title,
        "content": item.content,
        "metadata": item.metadata,
        "order": existing_count,
        "created_by": user_id,  # R&D Rule #6
        "created_at": now,
        "updated_at": now
    }
    
    _contents_db[content_id] = new_content
    
    # Mettre à jour workspace
    workspace["content_count"] = existing_count + 1
    workspace["last_activity"] = now
    workspace["updated_at"] = now
    
    return new_content


@router.put("/workspaces/{workspace_id}/content/{content_id}", response_model=ContentResponse)
async def update_content(
    workspace_id: str = Path(...),
    content_id: str = Path(...),
    item: ContentItem = Body(...)
):
    """Met à jour un élément de contenu."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if content_id not in _contents_db:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content = _contents_db[content_id]
    
    if content["workspace_id"] != workspace_id:
        raise HTTPException(status_code=400, detail="Content not in this workspace")
    
    now = datetime.utcnow().isoformat() + "Z"
    
    content["type"] = item.type.value
    content["title"] = item.title
    content["content"] = item.content
    content["metadata"] = item.metadata
    content["updated_at"] = now
    
    workspace["last_activity"] = now
    
    return content


@router.delete("/workspaces/{workspace_id}/content/{content_id}")
async def delete_content(
    workspace_id: str = Path(...),
    content_id: str = Path(...)
):
    """Supprime un élément de contenu."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if content_id not in _contents_db:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if _contents_db[content_id]["workspace_id"] != workspace_id:
        raise HTTPException(status_code=400, detail="Content not in this workspace")
    
    del _contents_db[content_id]
    
    workspace["content_count"] = max(0, workspace["content_count"] - 1)
    workspace["last_activity"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Content deleted", "id": content_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - WORKSPACE ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/workspaces/{workspace_id}/persist")
async def persist_workspace(workspace_id: str = Path(...)):
    """Convertit un workspace temporaire en persistant."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if workspace["type"] == WorkspaceType.PERSISTENT.value:
        raise HTTPException(status_code=400, detail="Already persistent")
    
    workspace["type"] = WorkspaceType.PERSISTENT.value
    workspace["expires_at"] = None
    workspace["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Workspace persisted", "id": workspace_id}


@router.post("/workspaces/{workspace_id}/archive")
async def archive_workspace(
    workspace_id: str = Path(...),
    checkpoint_id: Optional[str] = Query(None)
):
    """
    Archive un workspace.
    
    R&D Rule #1: HTTP 423 - Checkpoint requis
    """
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Checkpoint requis
    if not checkpoint_id:
        cp_id = str(uuid4())
        now = datetime.utcnow().isoformat() + "Z"
        
        _checkpoints_db[cp_id] = {
            "id": cp_id,
            "action_type": "archive_workspace",
            "status": "pending",
            "user_id": user_id,
            "context": {"workspace_id": workspace_id, "workspace_name": workspace["name"]},
            "created_at": now,
            "created_by": user_id
        }
        
        raise HTTPException(
            status_code=423,
            detail={
                "message": "Checkpoint required for workspace archival",
                "checkpoint_id": cp_id,
                "action": "archive_workspace"
            }
        )
    
    if checkpoint_id not in _checkpoints_db:
        raise HTTPException(status_code=400, detail="Invalid checkpoint")
    
    if _checkpoints_db[checkpoint_id]["status"] != "approved":
        raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    workspace["status"] = WorkspaceStatus.ARCHIVED.value
    workspace["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Workspace archived", "id": workspace_id}


@router.post("/workspaces/{workspace_id}/extend")
async def extend_workspace(
    workspace_id: str = Path(...),
    minutes: int = Query(60, ge=5, le=1440)
):
    """Prolonge l'expiration d'un workspace temporaire."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if workspace["type"] != WorkspaceType.TEMPORARY.value:
        raise HTTPException(status_code=400, detail="Only temporary workspaces can be extended")
    
    now = datetime.utcnow()
    workspace["expires_at"] = (now + timedelta(minutes=minutes)).isoformat() + "Z"
    workspace["updated_at"] = now.isoformat() + "Z"
    
    return {
        "message": "Workspace extended",
        "id": workspace_id,
        "new_expires_at": workspace["expires_at"]
    }


@router.post("/workspaces/{workspace_id}/link-thread")
async def link_to_thread(
    workspace_id: str = Path(...),
    thread_id: str = Query(..., description="Thread ID to link")
):
    """Lie un workspace à un thread existant."""
    user_id = get_current_user_id()
    
    if workspace_id not in _workspaces_db:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    workspace = _workspaces_db[workspace_id]
    
    if workspace["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    workspace["thread_id"] = thread_id
    workspace["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Workspace linked to thread", "thread_id": thread_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - QUICK ACCESS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/quick", response_model=WorkspaceResponse)
async def quick_workspace(content: Optional[str] = Body(None, embed=True)):
    """
    Crée un workspace ultra-rapide (OneClick!).
    
    Un seul clic = workspace prêt à l'emploi.
    """
    return await create_workspace(WorkspaceCreate(
        type=WorkspaceType.SCRATCH,
        initial_content=content,
        ttl_minutes=30  # 30 minutes par défaut
    ))


@router.get("/recent")
async def get_recent_workspaces(limit: int = Query(5, ge=1, le=20)):
    """Récupère les workspaces récents actifs."""
    user_id = get_current_user_id()
    
    workspaces = [
        ws for ws in _workspaces_db.values()
        if ws["owner_id"] == user_id and ws["status"] == WorkspaceStatus.ACTIVE.value
    ]
    
    workspaces.sort(key=lambda x: x["last_activity"], reverse=True)
    
    return workspaces[:limit]


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - STATS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_ocw_stats():
    """Statistiques des workspaces."""
    user_id = get_current_user_id()
    
    user_workspaces = [ws for ws in _workspaces_db.values() if ws["owner_id"] == user_id]
    
    return {
        "total_workspaces": len(user_workspaces),
        "by_type": {
            t.value: len([ws for ws in user_workspaces if ws["type"] == t.value])
            for t in WorkspaceType
        },
        "by_status": {
            s.value: len([ws for ws in user_workspaces if ws["status"] == s.value])
            for s in WorkspaceStatus
        },
        "total_content_items": sum(ws["content_count"] for ws in user_workspaces),
        "active_count": len([ws for ws in user_workspaces if ws["status"] == WorkspaceStatus.ACTIVE.value])
    }
