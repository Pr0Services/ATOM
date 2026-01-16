"""
CHE·NU™ V75 - Templates Router
System Templates API.

Templates = Reusable patterns for documents, workflows, dataspaces

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

class TemplateCreate(BaseModel):
    """Create template."""
    name: str = Field(..., min_length=1, max_length=200)
    template_type: str  # document, workflow, dataspace, meeting, report, estimation
    category: str
    description: Optional[str] = None
    content: Dict[str, Any] = {}
    variables: List[Dict[str, Any]] = []
    tags: List[str] = []


class TemplateUpdate(BaseModel):
    """Update template."""
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    variables: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class TemplateApplyRequest(BaseModel):
    """Apply template with variables."""
    variables: Dict[str, Any] = {}
    target_dataspace_id: Optional[str] = None


# ============================================================================
# MOCK DATA
# ============================================================================

TEMPLATE_TYPES = ["document", "workflow", "dataspace", "meeting", "report", "estimation", "email", "contract"]

TEMPLATE_CATEGORIES = [
    "construction", "immobilier", "finance", "legal", "creative",
    "management", "communication", "analysis", "planning", "general"
]

MOCK_TEMPLATES = [
    {
        "id": "tpl_001",
        "user_id": "user_001",
        "identity_id": "identity_002",
        "name": "Estimation Rénovation Standard",
        "template_type": "estimation",
        "category": "construction",
        "description": "Template d'estimation pour projets de rénovation résidentielle",
        "content": {
            "sections": [
                {"title": "Informations Client", "fields": ["client_name", "client_address", "client_phone"]},
                {"title": "Description du Projet", "fields": ["project_type", "project_description", "start_date"]},
                {"title": "Main d'oeuvre", "fields": ["labor_hours", "labor_rate"]},
                {"title": "Matériaux", "fields": ["materials_list", "materials_cost"]},
                {"title": "Contingence", "fields": ["contingency_percent"]},
                {"title": "Total", "fields": ["subtotal", "taxes", "grand_total"]},
            ],
            "formulas": {
                "labor_total": "labor_hours * labor_rate",
                "subtotal": "labor_total + materials_cost",
                "contingency": "subtotal * contingency_percent / 100",
                "total_before_tax": "subtotal + contingency",
                "tps": "total_before_tax * 0.05",
                "tvq": "total_before_tax * 0.09975",
                "grand_total": "total_before_tax + tps + tvq",
            },
        },
        "variables": [
            {"name": "client_name", "type": "string", "required": True, "label": "Nom du client"},
            {"name": "client_address", "type": "string", "required": True, "label": "Adresse"},
            {"name": "project_type", "type": "select", "options": ["Cuisine", "Salle de bain", "Sous-sol", "Toiture", "Autre"]},
            {"name": "labor_hours", "type": "number", "required": True, "label": "Heures de travail"},
            {"name": "labor_rate", "type": "number", "default": 75, "label": "Taux horaire ($)"},
            {"name": "contingency_percent", "type": "number", "default": 15, "label": "Contingence (%)"},
        ],
        "tags": ["construction", "estimation", "rénovation"],
        "is_system": False,
        "is_active": True,
        "usage_count": 47,
        "created_at": "2025-06-01T10:00:00Z",
        "updated_at": "2026-01-05T14:00:00Z",
    },
    {
        "id": "tpl_002",
        "user_id": None,
        "identity_id": None,
        "name": "Bail Résidentiel Québec",
        "template_type": "contract",
        "category": "immobilier",
        "description": "Template de bail conforme au TAL du Québec",
        "content": {
            "sections": [
                {"title": "Identification des Parties", "fields": ["landlord_name", "tenant_name"]},
                {"title": "Description du Logement", "fields": ["property_address", "unit_number", "description"]},
                {"title": "Durée du Bail", "fields": ["start_date", "end_date", "lease_type"]},
                {"title": "Loyer", "fields": ["monthly_rent", "payment_day", "payment_method"]},
                {"title": "Charges", "fields": ["electricity", "heating", "hot_water", "parking"]},
                {"title": "Conditions Particulières", "fields": ["special_conditions"]},
            ],
        },
        "variables": [
            {"name": "landlord_name", "type": "string", "required": True, "label": "Nom du propriétaire"},
            {"name": "tenant_name", "type": "string", "required": True, "label": "Nom du locataire"},
            {"name": "property_address", "type": "string", "required": True, "label": "Adresse de l'immeuble"},
            {"name": "unit_number", "type": "string", "required": True, "label": "Numéro de logement"},
            {"name": "monthly_rent", "type": "number", "required": True, "label": "Loyer mensuel ($)"},
            {"name": "start_date", "type": "date", "required": True, "label": "Date de début"},
            {"name": "lease_type", "type": "select", "options": ["12 mois", "Mois à mois", "Autre durée"]},
        ],
        "tags": ["immobilier", "bail", "québec", "tal"],
        "is_system": True,
        "is_active": True,
        "usage_count": 156,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2025-12-15T10:00:00Z",
    },
    {
        "id": "tpl_003",
        "user_id": None,
        "identity_id": None,
        "name": "Compte-rendu de Réunion",
        "template_type": "meeting",
        "category": "management",
        "description": "Template standard pour compte-rendu de réunion",
        "content": {
            "sections": [
                {"title": "Informations", "fields": ["meeting_title", "meeting_date", "meeting_location"]},
                {"title": "Participants", "fields": ["attendees", "absent"]},
                {"title": "Ordre du Jour", "fields": ["agenda_items"]},
                {"title": "Discussions", "fields": ["discussion_notes"]},
                {"title": "Décisions", "fields": ["decisions"]},
                {"title": "Actions", "fields": ["action_items"]},
                {"title": "Prochaine Réunion", "fields": ["next_meeting_date", "next_meeting_topics"]},
            ],
        },
        "variables": [
            {"name": "meeting_title", "type": "string", "required": True, "label": "Titre de la réunion"},
            {"name": "meeting_date", "type": "datetime", "required": True, "label": "Date et heure"},
            {"name": "attendees", "type": "array", "label": "Participants présents"},
            {"name": "agenda_items", "type": "array", "label": "Points à l'ordre du jour"},
        ],
        "tags": ["réunion", "compte-rendu", "management"],
        "is_system": True,
        "is_active": True,
        "usage_count": 312,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2025-11-20T09:00:00Z",
    },
    {
        "id": "tpl_004",
        "user_id": None,
        "identity_id": None,
        "name": "Rapport Mensuel Immobilier",
        "template_type": "report",
        "category": "immobilier",
        "description": "Rapport mensuel de performance du portfolio immobilier",
        "content": {
            "sections": [
                {"title": "Résumé Exécutif", "fields": ["summary"]},
                {"title": "Performance Financière", "fields": ["revenue", "expenses", "net_income", "occupancy_rate"]},
                {"title": "Par Propriété", "fields": ["property_details"]},
                {"title": "Maintenance", "fields": ["maintenance_completed", "maintenance_pending"]},
                {"title": "Locataires", "fields": ["new_tenants", "departures", "renewals"]},
                {"title": "Prévisions", "fields": ["forecast"]},
            ],
        },
        "variables": [
            {"name": "report_month", "type": "string", "required": True, "label": "Mois du rapport"},
            {"name": "total_properties", "type": "number", "label": "Nombre de propriétés"},
            {"name": "total_units", "type": "number", "label": "Nombre d'unités"},
        ],
        "tags": ["immobilier", "rapport", "mensuel", "finance"],
        "is_system": True,
        "is_active": True,
        "usage_count": 89,
        "created_at": "2024-06-01T00:00:00Z",
        "updated_at": "2025-12-01T10:00:00Z",
    },
]


# ============================================================================
# TEMPLATES
# ============================================================================

@router.get("", response_model=dict)
async def list_templates(
    template_type: Optional[str] = None,
    category: Optional[str] = None,
    is_system: Optional[bool] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    List templates.
    """
    templates = MOCK_TEMPLATES.copy()
    
    if template_type:
        templates = [t for t in templates if t["template_type"] == template_type]
    if category:
        templates = [t for t in templates if t["category"] == category]
    if is_system is not None:
        templates = [t for t in templates if t["is_system"] == is_system]
    if search:
        search_lower = search.lower()
        templates = [t for t in templates if search_lower in t["name"].lower() or search_lower in (t.get("description") or "").lower()]
    
    templates = [t for t in templates if t["is_active"]]
    
    total = len(templates)
    
    return {
        "success": True,
        "data": {
            "templates": templates,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit,
        },
    }


@router.get("/types", response_model=dict)
async def list_types():
    """
    List template types.
    """
    return {
        "success": True,
        "data": {
            "types": [
                {"id": "document", "label": "Document", "icon": "📄"},
                {"id": "workflow", "label": "Workflow", "icon": "🔄"},
                {"id": "dataspace", "label": "DataSpace", "icon": "📦"},
                {"id": "meeting", "label": "Réunion", "icon": "📅"},
                {"id": "report", "label": "Rapport", "icon": "📊"},
                {"id": "estimation", "label": "Estimation", "icon": "💰"},
                {"id": "email", "label": "Email", "icon": "✉️"},
                {"id": "contract", "label": "Contrat", "icon": "📝"},
            ],
        },
    }


@router.get("/categories", response_model=dict)
async def list_categories():
    """
    List template categories.
    """
    return {
        "success": True,
        "data": {
            "categories": [
                {"id": "construction", "label": "Construction", "icon": "🏗️"},
                {"id": "immobilier", "label": "Immobilier", "icon": "🏠"},
                {"id": "finance", "label": "Finance", "icon": "💰"},
                {"id": "legal", "label": "Légal", "icon": "⚖️"},
                {"id": "creative", "label": "Créatif", "icon": "🎨"},
                {"id": "management", "label": "Management", "icon": "📋"},
                {"id": "communication", "label": "Communication", "icon": "💬"},
                {"id": "analysis", "label": "Analyse", "icon": "📈"},
                {"id": "planning", "label": "Planification", "icon": "📅"},
                {"id": "general", "label": "Général", "icon": "📁"},
            ],
        },
    }


@router.get("/{template_id}", response_model=dict)
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


@router.post("", response_model=dict)
async def create_template(data: TemplateCreate):
    """
    Create new template.
    """
    if data.template_type not in TEMPLATE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid template type. Must be one of: {TEMPLATE_TYPES}")
    if data.category not in TEMPLATE_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {TEMPLATE_CATEGORIES}")
    
    template = {
        "id": f"tpl_{len(MOCK_TEMPLATES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "name": data.name,
        "template_type": data.template_type,
        "category": data.category,
        "description": data.description,
        "content": data.content,
        "variables": data.variables,
        "tags": data.tags,
        "is_system": False,
        "is_active": True,
        "usage_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_TEMPLATES.append(template)
    
    return {
        "success": True,
        "data": template,
        "message": "Template créé",
    }


@router.patch("/{template_id}", response_model=dict)
async def update_template(template_id: str, data: TemplateUpdate):
    """
    Update template.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template["is_system"]:
        raise HTTPException(status_code=403, detail="Cannot modify system template")
    
    if data.name:
        template["name"] = data.name
    if data.description is not None:
        template["description"] = data.description
    if data.content is not None:
        template["content"] = data.content
    if data.variables is not None:
        template["variables"] = data.variables
    if data.tags is not None:
        template["tags"] = data.tags
    if data.is_active is not None:
        template["is_active"] = data.is_active
    
    template["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": template,
    }


@router.delete("/{template_id}", response_model=dict)
async def delete_template(template_id: str):
    """
    Delete template.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if template["is_system"]:
        raise HTTPException(status_code=403, detail="Cannot delete system template")
    
    template["is_active"] = False
    template["deleted_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "message": "Template supprimé",
    }


# ============================================================================
# APPLY TEMPLATE
# ============================================================================

@router.post("/{template_id}/apply", response_model=dict)
async def apply_template(template_id: str, data: TemplateApplyRequest):
    """
    Apply template with variables.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Validate required variables
    for var in template["variables"]:
        if var.get("required") and var["name"] not in data.variables:
            raise HTTPException(status_code=400, detail=f"Missing required variable: {var['name']}")
    
    # Simulate template application
    result = {
        "template_id": template_id,
        "template_name": template["name"],
        "applied_variables": data.variables,
        "output_type": template["template_type"],
        "target_dataspace_id": data.target_dataspace_id,
        "applied_at": datetime.utcnow().isoformat(),
    }
    
    # Increment usage count
    template["usage_count"] += 1
    
    return {
        "success": True,
        "data": result,
        "message": "Template appliqué",
    }


@router.post("/{template_id}/preview", response_model=dict)
async def preview_template(template_id: str, variables: Dict[str, Any] = {}):
    """
    Preview template with variables.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    preview = {
        "template_id": template_id,
        "template_name": template["name"],
        "variables_applied": variables,
        "preview_content": template["content"],
        "generated_at": datetime.utcnow().isoformat(),
    }
    
    return {
        "success": True,
        "data": preview,
    }


@router.post("/{template_id}/duplicate", response_model=dict)
async def duplicate_template(template_id: str, new_name: str = ""):
    """
    Duplicate template.
    """
    template = next((t for t in MOCK_TEMPLATES if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    new_template = {
        **template,
        "id": f"tpl_{len(MOCK_TEMPLATES) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "name": new_name or f"{template['name']} (copie)",
        "is_system": False,
        "usage_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_TEMPLATES.append(new_template)
    
    return {
        "success": True,
        "data": new_template,
        "message": "Template dupliqué",
    }
