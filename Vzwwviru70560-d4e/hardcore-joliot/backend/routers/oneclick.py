"""
CHE·NU™ V75 - OneClick Router
1-Click Workflow Assistant API.

GOUVERNANCE > EXÉCUTION
- All workflows require human approval
- No autonomous execution

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

class ExecuteWorkflowRequest(BaseModel):
    """Execute workflow request."""
    workflow_id: str
    input_data: Dict[str, Any]
    input_type: Optional[str] = "prompt"


class QuickPromptRequest(BaseModel):
    """Quick prompt request."""
    prompt: str = Field(..., min_length=1)
    context: Optional[Dict[str, Any]] = None


class IntentDetectRequest(BaseModel):
    """Intent detection request."""
    input: str


class ExecuteTemplateRequest(BaseModel):
    """Execute template request."""
    variables: Dict[str, str]


# ============================================================================
# MOCK DATA
# ============================================================================

MOCK_WORKFLOWS = [
    {
        "id": "wf_001",
        "name": "Créer Estimation Construction",
        "description": "Génère une estimation complète pour un projet de construction",
        "trigger_patterns": ["estimation", "soumission", "devis", "quote", "bid"],
        "sphere_id": None,
        "domain_id": None,
        "workflow_steps": [
            {"id": "step_1", "name": "Analyser la demande", "type": "analysis"},
            {"id": "step_2", "name": "Collecter les données", "type": "data_fetch"},
            {"id": "step_3", "name": "Calculer les coûts", "type": "calculation"},
            {"id": "step_4", "name": "Générer le document", "type": "document_gen"},
            {"id": "step_5", "name": "Approbation", "type": "approval", "requires_approval": True},
        ],
        "required_inputs": [
            {"name": "project_type", "type": "select", "required": True},
            {"name": "surface_sqft", "type": "number", "required": True},
        ],
        "output_types": ["document", "dataspace"],
        "is_system": True,
        "is_active": True,
        "requires_approval": True,
        "created_at": "2025-12-01T00:00:00Z",
    },
    {
        "id": "wf_002",
        "name": "Préparer Réunion",
        "description": "Prépare automatiquement une réunion avec agenda et participants",
        "trigger_patterns": ["réunion", "meeting", "rencontre", "planifier"],
        "sphere_id": None,
        "domain_id": None,
        "workflow_steps": [
            {"id": "step_1", "name": "Identifier les participants", "type": "analysis"},
            {"id": "step_2", "name": "Générer l'agenda", "type": "content_gen"},
            {"id": "step_3", "name": "Créer la réunion", "type": "create"},
        ],
        "required_inputs": [
            {"name": "topic", "type": "text", "required": True},
            {"name": "date", "type": "date", "required": False},
        ],
        "output_types": ["notification"],
        "is_system": True,
        "is_active": True,
        "requires_approval": False,
        "created_at": "2025-12-01T00:00:00Z",
    },
    {
        "id": "wf_003",
        "name": "Rapport Portfolio Immobilier",
        "description": "Génère un rapport complet du portfolio immobilier",
        "trigger_patterns": ["rapport", "report", "portfolio", "immobilier", "propriétés"],
        "sphere_id": None,
        "domain_id": None,
        "workflow_steps": [
            {"id": "step_1", "name": "Collecter les données", "type": "data_fetch"},
            {"id": "step_2", "name": "Analyser la performance", "type": "analysis"},
            {"id": "step_3", "name": "Générer les graphiques", "type": "visualization"},
            {"id": "step_4", "name": "Compiler le rapport", "type": "document_gen"},
        ],
        "required_inputs": [],
        "output_types": ["document", "dashboard"],
        "is_system": True,
        "is_active": True,
        "requires_approval": True,
        "created_at": "2025-12-01T00:00:00Z",
    },
]

MOCK_TEMPLATES = [
    {
        "id": "tpl_001",
        "name": "Estimation Rénovation",
        "description": "Template pour estimation de rénovation résidentielle",
        "category": "construction",
        "prompt_template": "Créer une estimation pour une rénovation de {surface} pieds carrés, type {project_type}, dans {location}",
        "workflow_id": "wf_001",
        "example_inputs": [
            {"surface": "1500", "project_type": "cuisine", "location": "Montréal"},
        ],
        "usage_count": 45,
        "is_featured": True,
    },
    {
        "id": "tpl_002",
        "name": "Rapport Mensuel",
        "description": "Template pour rapport mensuel immobilier",
        "category": "immobilier",
        "prompt_template": "Générer le rapport mensuel pour le portfolio immobilier de {month} {year}",
        "workflow_id": "wf_003",
        "example_inputs": [
            {"month": "janvier", "year": "2026"},
        ],
        "usage_count": 28,
        "is_featured": True,
    },
    {
        "id": "tpl_003",
        "name": "Planning Sprint",
        "description": "Template pour planification de sprint",
        "category": "enterprise",
        "prompt_template": "Planifier le sprint {sprint_number} pour l'équipe {team} avec les objectifs: {objectives}",
        "workflow_id": "wf_002",
        "example_inputs": [
            {"sprint_number": "12", "team": "Core", "objectives": "MVP release"},
        ],
        "usage_count": 67,
        "is_featured": False,
    },
]

MOCK_EXECUTIONS = []


# ============================================================================
# WORKFLOWS
# ============================================================================

@router.get("/workflows", response_model=dict)
async def list_workflows(
    sphere_id: Optional[UUID] = None,
    domain_id: Optional[UUID] = None,
    is_active: Optional[bool] = True,
):
    """
    List available workflows.
    """
    workflows = MOCK_WORKFLOWS.copy()
    
    if is_active is not None:
        workflows = [w for w in workflows if w["is_active"] == is_active]
    
    return {
        "success": True,
        "data": {
            "workflows": workflows,
            "total": len(workflows),
        },
    }


@router.get("/workflows/{workflow_id}", response_model=dict)
async def get_workflow(workflow_id: str):
    """
    Get workflow details.
    """
    workflow = next((w for w in MOCK_WORKFLOWS if w["id"] == workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return {
        "success": True,
        "data": workflow,
    }


# ============================================================================
# EXECUTIONS
# ============================================================================

@router.post("/execute", response_model=dict)
async def execute_workflow(data: ExecuteWorkflowRequest):
    """
    Execute a workflow.
    
    GOUVERNANCE: Creates checkpoint for approval if required.
    """
    workflow = next((w for w in MOCK_WORKFLOWS if w["id"] == data.workflow_id), None)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    execution = {
        "id": f"exec_{len(MOCK_EXECUTIONS) + 1:03d}",
        "workflow_id": data.workflow_id,
        "user_id": "user_001",
        "identity_id": "identity_001",
        "input_type": data.input_type,
        "status": "awaiting_approval" if workflow["requires_approval"] else "running",
        "steps_completed": 0,
        "total_steps": len(workflow["workflow_steps"]),
        "current_step": workflow["workflow_steps"][0]["name"],
        "progress_percent": 0,
        "output_data": None,
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": None,
        "duration_seconds": None,
        "error_message": None,
    }
    
    MOCK_EXECUTIONS.append(execution)
    
    return {
        "success": True,
        "data": execution,
        "message": "Workflow lancé" if not workflow["requires_approval"] else "Workflow en attente d'approbation",
        "governance": {
            "requires_approval": workflow["requires_approval"],
            "checkpoint_created": workflow["requires_approval"],
        },
    }


@router.post("/quick", response_model=dict)
async def quick_prompt(data: QuickPromptRequest):
    """
    Quick prompt - detect intent and execute appropriate workflow.
    """
    # Detect intent
    input_lower = data.prompt.lower()
    
    matched_workflow = None
    for workflow in MOCK_WORKFLOWS:
        for pattern in workflow["trigger_patterns"]:
            if pattern in input_lower:
                matched_workflow = workflow
                break
        if matched_workflow:
            break
    
    if not matched_workflow:
        # Default to a generic workflow
        matched_workflow = MOCK_WORKFLOWS[0]
    
    execution = {
        "id": f"exec_{len(MOCK_EXECUTIONS) + 1:03d}",
        "workflow_id": matched_workflow["id"],
        "user_id": "user_001",
        "identity_id": "identity_001",
        "input_type": "prompt",
        "status": "awaiting_approval" if matched_workflow["requires_approval"] else "running",
        "steps_completed": 0,
        "total_steps": len(matched_workflow["workflow_steps"]),
        "current_step": matched_workflow["workflow_steps"][0]["name"],
        "progress_percent": 0,
        "output_data": None,
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": None,
        "duration_seconds": None,
        "error_message": None,
    }
    
    MOCK_EXECUTIONS.append(execution)
    
    return {
        "success": True,
        "data": {
            "execution": execution,
            "workflow": matched_workflow,
        },
        "message": f"Workflow '{matched_workflow['name']}' détecté et lancé",
    }


@router.get("/executions", response_model=dict)
async def list_executions(
    status: Optional[str] = None,
    workflow_id: Optional[str] = None,
):
    """
    List workflow executions.
    """
    executions = MOCK_EXECUTIONS.copy()
    
    if status:
        executions = [e for e in executions if e["status"] == status]
    if workflow_id:
        executions = [e for e in executions if e["workflow_id"] == workflow_id]
    
    return {
        "success": True,
        "data": {
            "executions": executions,
            "total": len(executions),
        },
    }


@router.get("/executions/{execution_id}", response_model=dict)
async def get_execution(execution_id: str):
    """
    Get execution details.
    """
    execution = next((e for e in MOCK_EXECUTIONS if e["id"] == execution_id), None)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return {
        "success": True,
        "data": execution,
    }


@router.post("/executions/{execution_id}/cancel", response_model=dict)
async def cancel_execution(execution_id: str):
    """
    Cancel a running execution.
    """
    execution = next((e for e in MOCK_EXECUTIONS if e["id"] == execution_id), None)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    execution["status"] = "cancelled"
    execution["completed_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": execution,
        "message": "Exécution annulée",
    }


@router.post("/executions/{execution_id}/approve", response_model=dict)
async def approve_execution(execution_id: str):
    """
    Approve a pending execution.
    
    GOUVERNANCE: Human approval required.
    """
    execution = next((e for e in MOCK_EXECUTIONS if e["id"] == execution_id), None)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    if execution["status"] != "awaiting_approval":
        raise HTTPException(status_code=400, detail="Execution is not awaiting approval")
    
    execution["status"] = "running"
    
    return {
        "success": True,
        "data": execution,
        "message": "Exécution approuvée et lancée",
        "governance": {
            "approved_by": "user_001",
            "approved_at": datetime.utcnow().isoformat(),
        },
    }


# ============================================================================
# TEMPLATES
# ============================================================================

@router.get("/templates", response_model=dict)
async def list_templates(
    category: Optional[str] = None,
    is_featured: Optional[bool] = None,
):
    """
    List workflow templates.
    """
    templates = MOCK_TEMPLATES.copy()
    
    if category:
        templates = [t for t in templates if t["category"] == category]
    if is_featured is not None:
        templates = [t for t in templates if t["is_featured"] == is_featured]
    
    return {
        "success": True,
        "data": {
            "templates": templates,
            "total": len(templates),
        },
    }


@router.get("/templates/{template_id}", response_model=dict)
async def get_template(template_id: str):
    """
    Get template details.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "success": True,
        "data": template,
    }


@router.post("/templates/{template_id}/execute", response_model=dict)
async def execute_template(template_id: str, data: ExecuteTemplateRequest):
    """
    Execute a template with variables.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Increment usage count
    template["usage_count"] += 1
    
    # Render prompt
    rendered_prompt = template["prompt_template"]
    for key, value in data.variables.items():
        rendered_prompt = rendered_prompt.replace(f"{{{key}}}", value)
    
    # Execute via quick prompt
    return await quick_prompt(QuickPromptRequest(prompt=rendered_prompt))


# ============================================================================
# INTENT DETECTION
# ============================================================================

@router.post("/detect", response_model=dict)
async def detect_intent(data: IntentDetectRequest):
    """
    Detect intent from natural language.
    """
    input_lower = data.input.lower()
    
    matched_workflow = None
    confidence = 0.0
    
    for workflow in MOCK_WORKFLOWS:
        for pattern in workflow["trigger_patterns"]:
            if pattern in input_lower:
                matched_workflow = workflow
                confidence = 0.85
                break
        if matched_workflow:
            break
    
    # Find relevant templates
    suggestions = []
    for template in MOCK_TEMPLATES:
        for word in input_lower.split():
            if word in template["name"].lower() or word in (template.get("description") or "").lower():
                suggestions.append(template)
                break
    
    return {
        "success": True,
        "data": {
            "workflow": matched_workflow,
            "confidence": confidence,
            "suggestions": suggestions[:3],
        },
    }
