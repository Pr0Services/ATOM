"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — ONECLICK ENGINE ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase B2: Backend Routers
Date: 8 Janvier 2026

R&D COMPLIANCE:
- Rule #1: HTTP 423 on EXECUTE action, DELETE automation
- Rule #2: Actions run in sandbox mode by default
- Rule #3: HTTP 403 on owner_id mismatch
- Rule #4: No AI-to-AI - human triggers all executions
- Rule #6: Full traceability on all actions
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/api/v2/oneclick", tags=["OneClick Engine"])


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ActionType(str, Enum):
    """Types d'actions OneClick."""
    QUICK_ACTION = "quick_action"       # Action simple, un clic
    WORKFLOW = "workflow"               # Séquence d'actions
    AUTOMATION = "automation"           # Action programmée/conditionnelle
    TEMPLATE = "template"               # Modèle réutilisable


class ExecutionMode(str, Enum):
    """Modes d'exécution (R&D Rule #2)."""
    SANDBOX = "sandbox"         # Simulation, pas d'effet réel
    PREVIEW = "preview"         # Aperçu des résultats
    EXECUTE = "execute"         # Exécution réelle (checkpoint requis)


class TriggerType(str, Enum):
    """Types de déclencheurs."""
    MANUAL = "manual"           # Déclenché par l'utilisateur
    SCHEDULED = "scheduled"     # Planifié
    CONDITIONAL = "conditional" # Sur condition
    WEBHOOK = "webhook"         # Via webhook externe


class ActionStatus(str, Enum):
    """Statuts d'exécution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    AWAITING_APPROVAL = "awaiting_approval"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ActionStep(BaseModel):
    """Étape d'une action."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    config: Dict[str, Any] = {}
    condition: Optional[str] = None
    on_error: str = "stop"  # stop, skip, retry


class ActionCreate(BaseModel):
    """Création d'une action OneClick."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    type: ActionType = ActionType.QUICK_ACTION
    steps: List[ActionStep] = []
    trigger: TriggerType = TriggerType.MANUAL
    trigger_config: Optional[Dict[str, Any]] = None
    sphere_id: Optional[str] = None
    tags: List[str] = []


class ActionUpdate(BaseModel):
    """Mise à jour d'une action."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    steps: Optional[List[ActionStep]] = None
    trigger_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None


class ExecutionRequest(BaseModel):
    """Requête d'exécution."""
    mode: ExecutionMode = ExecutionMode.SANDBOX  # R&D Rule #2: Sandbox par défaut
    parameters: Dict[str, Any] = {}
    checkpoint_id: Optional[str] = None  # Requis pour mode EXECUTE


class ActionResponse(BaseModel):
    """Réponse action."""
    id: str
    name: str
    description: Optional[str]
    type: str
    steps: List[Dict[str, Any]]
    trigger: str
    trigger_config: Optional[Dict[str, Any]]
    sphere_id: Optional[str]
    tags: List[str]
    is_active: bool
    execution_count: int
    last_execution: Optional[str]
    owner_id: str
    created_by: str      # R&D Rule #6
    created_at: str      # R&D Rule #6
    updated_at: str
    synthetic: bool = True


class ExecutionResponse(BaseModel):
    """Réponse d'exécution."""
    execution_id: str
    action_id: str
    status: str
    mode: str
    started_at: str
    completed_at: Optional[str]
    results: List[Dict[str, Any]]
    checkpoint_id: Optional[str]
    triggered_by: str    # R&D Rule #6
    synthetic: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ═══════════════════════════════════════════════════════════════════════════════

_actions_db: Dict[str, Dict[str, Any]] = {}
_executions_db: Dict[str, Dict[str, Any]] = {}
_checkpoints_db: Dict[str, Dict[str, Any]] = {}


def get_current_user_id() -> str:
    return "user_123"


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - ACTIONS CRUD
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/actions", response_model=List[ActionResponse])
async def list_actions(
    type: Optional[ActionType] = Query(None),
    sphere_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Liste les actions OneClick de l'utilisateur.
    
    R&D Rule #3: Filtre par owner_id
    R&D Rule #5: Tri chronologique
    """
    user_id = get_current_user_id()
    
    actions = [a for a in _actions_db.values() if a["owner_id"] == user_id]
    
    # Filtres
    if type:
        actions = [a for a in actions if a["type"] == type.value]
    if sphere_id:
        actions = [a for a in actions if a["sphere_id"] == sphere_id]
    if tag:
        actions = [a for a in actions if tag in a.get("tags", [])]
    if is_active is not None:
        actions = [a for a in actions if a["is_active"] == is_active]
    
    # R&D Rule #5: Tri chronologique
    actions.sort(key=lambda x: x["created_at"], reverse=True)
    
    return actions[skip:skip + limit]


@router.post("/actions", response_model=ActionResponse, status_code=201)
async def create_action(action: ActionCreate):
    """
    Crée une nouvelle action OneClick.
    
    R&D Rule #6: Traçabilité complète
    """
    user_id = get_current_user_id()
    now = datetime.utcnow().isoformat() + "Z"
    
    action_id = str(uuid4())
    
    new_action = {
        "id": action_id,
        "name": action.name,
        "description": action.description,
        "type": action.type.value,
        "steps": [s.model_dump() for s in action.steps],
        "trigger": action.trigger.value,
        "trigger_config": action.trigger_config,
        "sphere_id": action.sphere_id,
        "tags": action.tags,
        "is_active": True,
        "execution_count": 0,
        "last_execution": None,
        "owner_id": user_id,
        "created_by": user_id,  # R&D Rule #6
        "created_at": now,       # R&D Rule #6
        "updated_at": now,
        "synthetic": True
    }
    
    _actions_db[action_id] = new_action
    
    return new_action


@router.get("/actions/{action_id}", response_model=ActionResponse)
async def get_action(action_id: str = Path(...)):
    """Récupère une action par ID."""
    user_id = get_current_user_id()
    
    if action_id not in _actions_db:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action = _actions_db[action_id]
    
    # R&D Rule #3
    if action["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return action


@router.put("/actions/{action_id}", response_model=ActionResponse)
async def update_action(
    action_id: str = Path(...),
    update: ActionUpdate = Body(...)
):
    """Met à jour une action."""
    user_id = get_current_user_id()
    
    if action_id not in _actions_db:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action = _actions_db[action_id]
    
    if action["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Appliquer mises à jour
    if update.name is not None:
        action["name"] = update.name
    if update.description is not None:
        action["description"] = update.description
    if update.steps is not None:
        action["steps"] = [s.model_dump() for s in update.steps]
    if update.trigger_config is not None:
        action["trigger_config"] = update.trigger_config
    if update.is_active is not None:
        action["is_active"] = update.is_active
    if update.tags is not None:
        action["tags"] = update.tags
    
    action["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return action


@router.delete("/actions/{action_id}")
async def delete_action(
    action_id: str = Path(...),
    checkpoint_id: Optional[str] = Query(None)
):
    """
    Supprime une action.
    
    R&D Rule #1: HTTP 423 - Checkpoint requis pour automations
    """
    user_id = get_current_user_id()
    
    if action_id not in _actions_db:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action = _actions_db[action_id]
    
    if action["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Checkpoint pour automations
    if action["type"] == ActionType.AUTOMATION.value:
        if not checkpoint_id:
            cp_id = str(uuid4())
            now = datetime.utcnow().isoformat() + "Z"
            
            _checkpoints_db[cp_id] = {
                "id": cp_id,
                "action_type": "delete_automation",
                "status": "pending",
                "user_id": user_id,
                "context": {"action_id": action_id, "action_name": action["name"]},
                "created_at": now,
                "created_by": user_id
            }
            
            raise HTTPException(
                status_code=423,
                detail={
                    "message": "Checkpoint required for automation deletion",
                    "checkpoint_id": cp_id,
                    "action": "delete_automation"
                }
            )
        
        if checkpoint_id not in _checkpoints_db:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")
        
        if _checkpoints_db[checkpoint_id]["status"] != "approved":
            raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    del _actions_db[action_id]
    
    return {"message": "Action deleted", "id": action_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/actions/{action_id}/execute", response_model=ExecutionResponse)
async def execute_action(
    action_id: str = Path(...),
    request: ExecutionRequest = Body(...)
):
    """
    Exécute une action OneClick.
    
    R&D Rule #1: HTTP 423 pour mode EXECUTE (checkpoint requis)
    R&D Rule #2: Mode SANDBOX par défaut
    R&D Rule #4: Déclenché par l'humain, pas par IA
    R&D Rule #6: Traçabilité complète
    """
    user_id = get_current_user_id()
    now = datetime.utcnow().isoformat() + "Z"
    
    if action_id not in _actions_db:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action = _actions_db[action_id]
    
    if action["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not action["is_active"]:
        raise HTTPException(status_code=400, detail="Action is inactive")
    
    # R&D Rule #1: Checkpoint pour mode EXECUTE
    if request.mode == ExecutionMode.EXECUTE:
        if not request.checkpoint_id:
            cp_id = str(uuid4())
            
            _checkpoints_db[cp_id] = {
                "id": cp_id,
                "action_type": "execute_oneclick",
                "status": "pending",
                "user_id": user_id,
                "context": {
                    "action_id": action_id,
                    "action_name": action["name"],
                    "parameters": request.parameters
                },
                "created_at": now,
                "created_by": user_id
            }
            
            raise HTTPException(
                status_code=423,
                detail={
                    "message": "Checkpoint required for action execution",
                    "checkpoint_id": cp_id,
                    "action": "execute_oneclick",
                    "hint": "Use mode='sandbox' or 'preview' for immediate execution"
                }
            )
        
        if request.checkpoint_id not in _checkpoints_db:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")
        
        if _checkpoints_db[request.checkpoint_id]["status"] != "approved":
            raise HTTPException(status_code=423, detail="Checkpoint not approved")
    
    # Créer l'exécution
    execution_id = str(uuid4())
    
    execution = {
        "execution_id": execution_id,
        "action_id": action_id,
        "status": ActionStatus.RUNNING.value,
        "mode": request.mode.value,
        "started_at": now,
        "completed_at": None,
        "results": [],
        "checkpoint_id": request.checkpoint_id,
        "triggered_by": user_id,  # R&D Rule #6 & #4
        "parameters": request.parameters,
        "synthetic": True
    }
    
    # Simuler l'exécution des étapes
    for i, step in enumerate(action["steps"]):
        step_result = {
            "step_id": step["id"],
            "step_name": step["name"],
            "status": "completed" if request.mode != ExecutionMode.EXECUTE else "simulated",
            "output": {"message": f"Step {i+1} executed in {request.mode.value} mode"},
            "duration_ms": 100
        }
        execution["results"].append(step_result)
    
    execution["status"] = ActionStatus.COMPLETED.value
    execution["completed_at"] = datetime.utcnow().isoformat() + "Z"
    
    _executions_db[execution_id] = execution
    
    # Mettre à jour stats action
    action["execution_count"] += 1
    action["last_execution"] = now
    
    return execution


@router.get("/actions/{action_id}/preview")
async def preview_action(
    action_id: str = Path(...),
    parameters: Optional[Dict[str, Any]] = None
):
    """
    Aperçu de ce que l'action va faire.
    
    R&D Rule #2: Preview mode - aucun effet réel.
    """
    user_id = get_current_user_id()
    
    if action_id not in _actions_db:
        raise HTTPException(status_code=404, detail="Action not found")
    
    action = _actions_db[action_id]
    
    if action["owner_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Générer un aperçu
    preview = {
        "action_id": action_id,
        "action_name": action["name"],
        "mode": "preview",
        "steps_preview": []
    }
    
    for step in action["steps"]:
        preview["steps_preview"].append({
            "step_name": step["name"],
            "type": step["type"],
            "will_do": f"Execute {step['type']} operation",
            "estimated_duration_ms": 100
        })
    
    preview["total_steps"] = len(action["steps"])
    preview["estimated_duration_ms"] = len(action["steps"]) * 100
    preview["requires_checkpoint"] = True
    
    return preview


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - EXECUTION HISTORY
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/executions", response_model=List[ExecutionResponse])
async def list_executions(
    action_id: Optional[str] = Query(None),
    status: Optional[ActionStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Liste l'historique des exécutions.
    
    R&D Rule #5: Tri chronologique
    """
    user_id = get_current_user_id()
    
    executions = [e for e in _executions_db.values() if e["triggered_by"] == user_id]
    
    if action_id:
        executions = [e for e in executions if e["action_id"] == action_id]
    if status:
        executions = [e for e in executions if e["status"] == status.value]
    
    # R&D Rule #5: Chronologique
    executions.sort(key=lambda x: x["started_at"], reverse=True)
    
    return executions[skip:skip + limit]


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(execution_id: str = Path(...)):
    """Récupère les détails d'une exécution."""
    user_id = get_current_user_id()
    
    if execution_id not in _executions_db:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    execution = _executions_db[execution_id]
    
    if execution["triggered_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return execution


@router.post("/executions/{execution_id}/cancel")
async def cancel_execution(execution_id: str = Path(...)):
    """Annule une exécution en cours."""
    user_id = get_current_user_id()
    
    if execution_id not in _executions_db:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    execution = _executions_db[execution_id]
    
    if execution["triggered_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if execution["status"] not in [ActionStatus.PENDING.value, ActionStatus.RUNNING.value]:
        raise HTTPException(status_code=400, detail="Execution cannot be cancelled")
    
    execution["status"] = ActionStatus.CANCELLED.value
    execution["completed_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Execution cancelled", "execution_id": execution_id}


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/templates")
async def list_templates():
    """Liste les templates d'actions disponibles."""
    return [
        {
            "id": "template_backup",
            "name": "Quick Backup",
            "description": "Backup selected files to cloud storage",
            "type": ActionType.QUICK_ACTION.value,
            "steps": [
                {"type": "select_files", "name": "Select Files"},
                {"type": "compress", "name": "Compress"},
                {"type": "upload", "name": "Upload to Cloud"}
            ]
        },
        {
            "id": "template_report",
            "name": "Generate Report",
            "description": "Generate and email a weekly report",
            "type": ActionType.WORKFLOW.value,
            "steps": [
                {"type": "collect_data", "name": "Collect Data"},
                {"type": "generate_report", "name": "Generate Report"},
                {"type": "send_email", "name": "Send Email"}
            ]
        },
        {
            "id": "template_cleanup",
            "name": "Auto Cleanup",
            "description": "Clean up old files automatically",
            "type": ActionType.AUTOMATION.value,
            "steps": [
                {"type": "find_old_files", "name": "Find Old Files"},
                {"type": "archive", "name": "Archive"},
                {"type": "delete", "name": "Delete Originals"}
            ],
            "trigger": TriggerType.SCHEDULED.value
        }
    ]


@router.post("/actions/from-template/{template_id}", response_model=ActionResponse)
async def create_from_template(
    template_id: str = Path(...),
    name: str = Query(..., min_length=1, max_length=100),
    sphere_id: Optional[str] = Query(None)
):
    """Crée une action à partir d'un template."""
    templates = {
        "template_backup": {
            "type": ActionType.QUICK_ACTION,
            "steps": [
                ActionStep(name="Select Files", type="select_files"),
                ActionStep(name="Compress", type="compress"),
                ActionStep(name="Upload to Cloud", type="upload")
            ]
        },
        "template_report": {
            "type": ActionType.WORKFLOW,
            "steps": [
                ActionStep(name="Collect Data", type="collect_data"),
                ActionStep(name="Generate Report", type="generate_report"),
                ActionStep(name="Send Email", type="send_email")
            ]
        },
        "template_cleanup": {
            "type": ActionType.AUTOMATION,
            "steps": [
                ActionStep(name="Find Old Files", type="find_old_files"),
                ActionStep(name="Archive", type="archive"),
                ActionStep(name="Delete Originals", type="delete")
            ],
            "trigger": TriggerType.SCHEDULED
        }
    }
    
    if template_id not in templates:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = templates[template_id]
    
    action_create = ActionCreate(
        name=name,
        description=f"Created from template {template_id}",
        type=template["type"],
        steps=template["steps"],
        trigger=template.get("trigger", TriggerType.MANUAL),
        sphere_id=sphere_id
    )
    
    return await create_action(action_create)


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - STATS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_oneclick_stats():
    """Statistiques OneClick de l'utilisateur."""
    user_id = get_current_user_id()
    
    user_actions = [a for a in _actions_db.values() if a["owner_id"] == user_id]
    user_executions = [e for e in _executions_db.values() if e["triggered_by"] == user_id]
    
    return {
        "total_actions": len(user_actions),
        "active_actions": len([a for a in user_actions if a["is_active"]]),
        "by_type": {
            t.value: len([a for a in user_actions if a["type"] == t.value])
            for t in ActionType
        },
        "total_executions": len(user_executions),
        "executions_by_status": {
            s.value: len([e for e in user_executions if e["status"] == s.value])
            for s in ActionStatus
        },
        "executions_by_mode": {
            m.value: len([e for e in user_executions if e["mode"] == m.value])
            for m in ExecutionMode
        }
    }
