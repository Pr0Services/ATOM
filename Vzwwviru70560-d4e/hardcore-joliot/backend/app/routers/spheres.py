"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — SPHERES ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent B - Phase B2: Core Routers
Date: 8 Janvier 2026

9 SPHÈRES EXACTEMENT (FROZEN):
1. Personal
2. Business
3. Government & Institutions
4. Studio de création
5. Community
6. Social & Media
7. Entertainment
8. My Team
9. Scholar

6 BUREAU SECTIONS PAR SPHÈRE (FROZEN):
1. QuickCapture
2. ResumeWorkspace
3. Threads
4. DataFiles
5. ActiveAgents
6. Meetings

R&D RULES ENFORCED:
- Rule #3: Cross-sphere requires explicit workflow
- Rule #7: Architecture is FROZEN (9 spheres, 6 sections)
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4
from enum import Enum

router = APIRouter(prefix="/api/v2/spheres", tags=["Spheres"])


# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL DEFINITIONS (FROZEN - Rule #7)
# ═══════════════════════════════════════════════════════════════════════════════

# THE 9 SPHERES - IMMUTABLE
CANONICAL_SPHERES = [
    {
        "id": "sphere-personal",
        "name": "Personal",
        "icon": "🏠",
        "description": "Vie personnelle, notes, tâches, habitudes",
        "order": 1,
        "color": "#4F46E5"
    },
    {
        "id": "sphere-business",
        "name": "Business",
        "icon": "💼",
        "description": "Entreprise, CRM, facturation, projets professionnels",
        "order": 2,
        "color": "#059669"
    },
    {
        "id": "sphere-government",
        "name": "Government & Institutions",
        "icon": "🏛️",
        "description": "Relations institutionnelles, compliance, démarches",
        "order": 3,
        "color": "#DC2626"
    },
    {
        "id": "sphere-studio",
        "name": "Studio de création",
        "icon": "🎨",
        "description": "Création, design, médias, génération AI",
        "order": 4,
        "color": "#7C3AED"
    },
    {
        "id": "sphere-community",
        "name": "Community",
        "icon": "👥",
        "description": "Groupes, événements, coordination communautaire",
        "order": 5,
        "color": "#DB2777"
    },
    {
        "id": "sphere-social",
        "name": "Social & Media",
        "icon": "📱",
        "description": "Réseaux sociaux, publication, scheduling",
        "order": 6,
        "color": "#0891B2"
    },
    {
        "id": "sphere-entertainment",
        "name": "Entertainment",
        "icon": "🎬",
        "description": "Streaming, jeux, contenu divertissement",
        "order": 7,
        "color": "#EA580C"
    },
    {
        "id": "sphere-myteam",
        "name": "My Team",
        "icon": "🤝",
        "description": "Collaboration équipe, ressources humaines",
        "order": 8,
        "color": "#65A30D"
    },
    {
        "id": "sphere-scholar",
        "name": "Scholar",
        "icon": "📚",
        "description": "Recherche, académique, apprentissage",
        "order": 9,
        "color": "#9333EA"
    }
]

# THE 6 BUREAU SECTIONS - IMMUTABLE
CANONICAL_BUREAU_SECTIONS = [
    {
        "id": "section-quickcapture",
        "name": "QuickCapture",
        "icon": "📥",
        "description": "Capture rapide, inbox",
        "order": 1
    },
    {
        "id": "section-resumeworkspace",
        "name": "ResumeWorkspace",
        "icon": "📂",
        "description": "Espace de travail principal",
        "order": 2
    },
    {
        "id": "section-threads",
        "name": "Threads",
        "icon": "🧵",
        "description": "Liste des Threads de la sphère",
        "order": 3
    },
    {
        "id": "section-datafiles",
        "name": "DataFiles",
        "icon": "📁",
        "description": "Fichiers et documents",
        "order": 4
    },
    {
        "id": "section-activeagents",
        "name": "ActiveAgents",
        "icon": "🤖",
        "description": "Agents actifs dans la sphère",
        "order": 5
    },
    {
        "id": "section-meetings",
        "name": "Meetings",
        "icon": "📅",
        "description": "Réunions et calendrier",
        "order": 6
    }
]


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

# User sphere settings (per user customization)
MOCK_USER_SPHERES: Dict[str, Dict[str, Dict]] = {}  # user_id -> sphere_id -> settings

# Cross-sphere workflows pending approval
MOCK_CROSS_SPHERE_WORKFLOWS: Dict[str, Dict] = {}


def get_current_user_id() -> str:
    return "test-user-001"


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/", summary="List all spheres")
async def list_spheres():
    """
    List all 9 canonical spheres.
    
    R&D RULE #7: Architecture is FROZEN.
    There are EXACTLY 9 spheres, no more, no less.
    """
    user_id = get_current_user_id()
    
    # Merge canonical with user settings
    spheres = []
    for sphere in CANONICAL_SPHERES:
        sphere_data = sphere.copy()
        
        # Add user-specific settings if any
        user_settings = MOCK_USER_SPHERES.get(user_id, {}).get(sphere["id"], {})
        sphere_data["user_settings"] = user_settings
        sphere_data["is_active"] = user_settings.get("is_active", True)
        sphere_data["pinned"] = user_settings.get("pinned", False)
        
        # Add bureau sections count (always 6)
        sphere_data["bureau_sections"] = [s["name"] for s in CANONICAL_BUREAU_SECTIONS]
        sphere_data["bureau_sections_count"] = 6
        
        spheres.append(sphere_data)
    
    return {
        "spheres": spheres,
        "total": 9,  # Always 9
        "note": "R&D Rule #7: Architecture is FROZEN - exactly 9 spheres"
    }


@router.get("/{sphere_name}", summary="Get sphere details")
async def get_sphere(sphere_name: str):
    """
    Get details of a specific sphere.
    
    R&D RULE #7: Each sphere has exactly 6 bureau sections.
    """
    # Find sphere by name
    sphere = next((s for s in CANONICAL_SPHERES if s["name"] == sphere_name), None)
    
    if not sphere:
        # Try by ID
        sphere = next((s for s in CANONICAL_SPHERES if s["id"] == sphere_name), None)
    
    if not sphere:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "sphere_not_found",
                "message": f"Sphere '{sphere_name}' not found",
                "valid_spheres": [s["name"] for s in CANONICAL_SPHERES]
            }
        )
    
    user_id = get_current_user_id()
    user_settings = MOCK_USER_SPHERES.get(user_id, {}).get(sphere["id"], {})
    
    return {
        **sphere,
        "bureau_sections": CANONICAL_BUREAU_SECTIONS,
        "user_settings": user_settings,
        "is_active": user_settings.get("is_active", True),
        "threads_count": 0,  # Mock
        "agents_count": 0,   # Mock
        "note": "R&D Rule #7: This sphere has exactly 6 bureau sections"
    }


@router.patch("/{sphere_name}/settings", summary="Update sphere settings")
async def update_sphere_settings(
    sphere_name: str,
    is_active: Optional[bool] = Body(None),
    pinned: Optional[bool] = Body(None),
    custom_order: Optional[int] = Body(None),
    custom_color: Optional[str] = Body(None)
):
    """
    Update user-specific sphere settings.
    
    NOTE: Cannot add/remove spheres or bureau sections (Rule #7).
    """
    # Verify sphere exists
    sphere = next((s for s in CANONICAL_SPHERES if s["name"] == sphere_name), None)
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    
    user_id = get_current_user_id()
    
    if user_id not in MOCK_USER_SPHERES:
        MOCK_USER_SPHERES[user_id] = {}
    
    if sphere["id"] not in MOCK_USER_SPHERES[user_id]:
        MOCK_USER_SPHERES[user_id][sphere["id"]] = {}
    
    settings = MOCK_USER_SPHERES[user_id][sphere["id"]]
    
    if is_active is not None:
        settings["is_active"] = is_active
    if pinned is not None:
        settings["pinned"] = pinned
    if custom_order is not None:
        settings["custom_order"] = custom_order
    if custom_color is not None:
        settings["custom_color"] = custom_color
    
    settings["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    return {
        "sphere": sphere_name,
        "settings": settings,
        "message": "Settings updated. Note: Cannot modify sphere structure (Rule #7)"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU SECTION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{sphere_name}/bureau", summary="Get bureau sections")
async def get_bureau_sections(sphere_name: str):
    """
    Get bureau sections for a sphere.
    
    R&D RULE #7: ALWAYS 6 sections, no exceptions.
    """
    # Verify sphere exists
    sphere = next((s for s in CANONICAL_SPHERES if s["name"] == sphere_name), None)
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    
    return {
        "sphere": sphere_name,
        "bureau_sections": CANONICAL_BUREAU_SECTIONS,
        "total": 6,  # Always 6
        "note": "R&D Rule #7: Exactly 6 bureau sections per sphere"
    }


@router.get("/{sphere_name}/bureau/{section_name}", summary="Get bureau section content")
async def get_bureau_section(sphere_name: str, section_name: str):
    """Get content of a specific bureau section."""
    # Verify sphere
    sphere = next((s for s in CANONICAL_SPHERES if s["name"] == sphere_name), None)
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    
    # Verify section
    section = next((s for s in CANONICAL_BUREAU_SECTIONS if s["name"] == section_name), None)
    if not section:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "section_not_found",
                "valid_sections": [s["name"] for s in CANONICAL_BUREAU_SECTIONS]
            }
        )
    
    user_id = get_current_user_id()
    
    # Mock content based on section type
    content = {
        "QuickCapture": {"items": [], "type": "inbox"},
        "ResumeWorkspace": {"recent_threads": [], "pinned_items": []},
        "Threads": {"threads": [], "total": 0},
        "DataFiles": {"files": [], "folders": []},
        "ActiveAgents": {"agents": [], "nova_available": True},
        "Meetings": {"upcoming": [], "past": []}
    }
    
    return {
        "sphere": sphere_name,
        "section": section,
        "content": content.get(section_name, {}),
        "owner_id": user_id
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CROSS-SPHERE WORKFLOWS (Rule #3)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/workflows/cross-sphere", summary="Create cross-sphere workflow")
async def create_cross_sphere_workflow(
    source_sphere: str = Body(...),
    target_sphere: str = Body(...),
    resource_type: str = Body(...),  # thread, file, agent
    resource_id: str = Body(...),
    action: str = Body(...)  # copy, move, link
):
    """
    Create a cross-sphere workflow.
    
    R&D RULE #3: Cross-sphere operations require EXPLICIT workflow and approval.
    Data does NOT flow automatically between spheres.
    """
    user_id = get_current_user_id()
    
    # Verify both spheres exist
    source = next((s for s in CANONICAL_SPHERES if s["name"] == source_sphere), None)
    target = next((s for s in CANONICAL_SPHERES if s["name"] == target_sphere), None)
    
    if not source:
        raise HTTPException(status_code=404, detail=f"Source sphere '{source_sphere}' not found")
    if not target:
        raise HTTPException(status_code=404, detail=f"Target sphere '{target_sphere}' not found")
    
    if source_sphere == target_sphere:
        raise HTTPException(status_code=400, detail="Source and target sphere cannot be the same")
    
    now = datetime.now(timezone.utc).isoformat()
    workflow_id = str(uuid4())
    
    workflow = {
        "id": workflow_id,
        "type": "cross_sphere_transfer",
        "status": "awaiting_approval",  # Always starts pending
        "source_sphere": source_sphere,
        "target_sphere": target_sphere,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "action": action,
        # Rule #6: Traceability
        "initiated_by": user_id,
        "initiated_at": now,
        # Approval tracking
        "approved_by": None,
        "approved_at": None,
        "executed_at": None
    }
    
    MOCK_CROSS_SPHERE_WORKFLOWS[workflow_id] = workflow
    
    return {
        "status": "workflow_created",
        "workflow": workflow,
        "message": "R&D Rule #3: Cross-sphere transfer requires human approval",
        "next_step": f"POST /api/v2/spheres/workflows/{workflow_id}/approve"
    }


@router.get("/workflows/pending", summary="List pending cross-sphere workflows")
async def list_pending_workflows():
    """List pending cross-sphere workflows for current user."""
    user_id = get_current_user_id()
    
    pending = [
        w for w in MOCK_CROSS_SPHERE_WORKFLOWS.values()
        if w["initiated_by"] == user_id and w["status"] == "awaiting_approval"
    ]
    
    return {
        "pending_workflows": pending,
        "total": len(pending),
        "note": "R&D Rule #3: All cross-sphere transfers require approval"
    }


@router.post("/workflows/{workflow_id}/approve", summary="Approve cross-sphere workflow")
async def approve_cross_sphere_workflow(workflow_id: str):
    """
    Approve a cross-sphere workflow.
    
    R&D RULE #3: Human must explicitly approve.
    """
    if workflow_id not in MOCK_CROSS_SPHERE_WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = MOCK_CROSS_SPHERE_WORKFLOWS[workflow_id]
    user_id = get_current_user_id()
    
    # Verify ownership
    if workflow["initiated_by"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to approve this workflow")
    
    if workflow["status"] != "awaiting_approval":
        raise HTTPException(status_code=400, detail=f"Workflow status is '{workflow['status']}', cannot approve")
    
    now = datetime.now(timezone.utc).isoformat()
    
    workflow["status"] = "approved"
    workflow["approved_by"] = user_id
    workflow["approved_at"] = now
    workflow["executed_at"] = now  # Mock immediate execution
    
    return {
        "status": "approved",
        "workflow": workflow,
        "message": "Cross-sphere transfer approved and executed"
    }


@router.post("/workflows/{workflow_id}/reject", summary="Reject cross-sphere workflow")
async def reject_cross_sphere_workflow(
    workflow_id: str,
    reason: Optional[str] = Body(None)
):
    """Reject a cross-sphere workflow."""
    if workflow_id not in MOCK_CROSS_SPHERE_WORKFLOWS:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = MOCK_CROSS_SPHERE_WORKFLOWS[workflow_id]
    user_id = get_current_user_id()
    
    if workflow["initiated_by"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    workflow["status"] = "rejected"
    workflow["rejected_by"] = user_id
    workflow["rejected_at"] = datetime.now(timezone.utc).isoformat()
    workflow["rejection_reason"] = reason
    
    return {
        "status": "rejected",
        "workflow": workflow
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE STATS & HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", summary="Sphere service statistics")
async def sphere_stats():
    """Get sphere service statistics."""
    user_id = get_current_user_id()
    
    pending_workflows = len([
        w for w in MOCK_CROSS_SPHERE_WORKFLOWS.values()
        if w["initiated_by"] == user_id and w["status"] == "awaiting_approval"
    ])
    
    return {
        "user_id": user_id,
        "total_spheres": 9,  # Always 9
        "bureau_sections_per_sphere": 6,  # Always 6
        "pending_cross_sphere_workflows": pending_workflows,
        "r&d_rule_7_compliant": True,
        "architecture_status": "FROZEN"
    }


@router.get("/health", summary="Spheres service health")
async def spheres_health():
    """Health check for spheres service."""
    return {
        "service": "spheres",
        "status": "healthy",
        "version": "v76",
        "canonical_spheres": 9,
        "canonical_bureau_sections": 6,
        "r&d_compliance": {
            "rule_3": "Cross-sphere requires explicit workflow",
            "rule_7": "Architecture FROZEN (9 spheres, 6 sections)"
        }
    }
