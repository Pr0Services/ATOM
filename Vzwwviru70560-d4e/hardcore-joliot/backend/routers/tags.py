"""
CHE·NU™ V75 - Tags Router
Tags Management API.

Tags = Organization, categorization, filtering

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

class TagCreate(BaseModel):
    """Create tag."""
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class TagUpdate(BaseModel):
    """Update tag."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class TagAssignment(BaseModel):
    """Assign tags to resource."""
    tags: List[str]


# ============================================================================
# MOCK DATA
# ============================================================================

TAG_CATEGORIES = ["project", "priority", "status", "domain", "custom"]

MOCK_TAGS = [
    {"id": "tag_001", "name": "urgent", "color": "#E74C3C", "description": "Tâches urgentes", "category": "priority", "usage_count": 15, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_002", "name": "important", "color": "#D8B26A", "description": "Éléments importants", "category": "priority", "usage_count": 28, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_003", "name": "en-cours", "color": "#3EB4A2", "description": "En cours de réalisation", "category": "status", "usage_count": 45, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_004", "name": "complété", "color": "#3F7249", "description": "Terminé", "category": "status", "usage_count": 67, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_005", "name": "en-attente", "color": "#8D8371", "description": "En attente de validation", "category": "status", "usage_count": 23, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_006", "name": "rénovation", "color": "#7A593A", "description": "Projets rénovation", "category": "domain", "usage_count": 12, "created_at": "2025-03-01T00:00:00Z"},
    {"id": "tag_007", "name": "cuisine", "color": "#E67E22", "description": "Cuisine", "category": "domain", "usage_count": 8, "created_at": "2025-03-01T00:00:00Z"},
    {"id": "tag_008", "name": "maya", "color": "#9B59B6", "description": "Projet Maya", "category": "project", "usage_count": 34, "created_at": "2026-01-02T00:00:00Z"},
    {"id": "tag_009", "name": "immobilier", "color": "#2F4C39", "description": "Gestion immobilière", "category": "domain", "usage_count": 56, "created_at": "2025-01-01T00:00:00Z"},
    {"id": "tag_010", "name": "locataire", "color": "#3498DB", "description": "Lié aux locataires", "category": "domain", "usage_count": 42, "created_at": "2025-01-01T00:00:00Z"},
]

MOCK_TAG_ASSIGNMENTS = [
    {"resource_type": "dataspace", "resource_id": "ds_001", "tags": ["rénovation", "cuisine", "maya"]},
    {"resource_type": "document", "resource_id": "doc_001", "tags": ["important", "maya"]},
    {"resource_type": "task", "resource_id": "task_001", "tags": ["urgent", "en-cours"]},
    {"resource_type": "property", "resource_id": "prop_001", "tags": ["immobilier"]},
]


# ============================================================================
# TAGS
# ============================================================================

@router.get("", response_model=dict)
async def list_tags(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("name", pattern="^(name|usage_count|created_at)$"),
):
    """
    List all tags.
    """
    tags = MOCK_TAGS.copy()
    
    if category:
        tags = [t for t in tags if t["category"] == category]
    if search:
        search_lower = search.lower()
        tags = [t for t in tags if search_lower in t["name"].lower() or search_lower in (t.get("description") or "").lower()]
    
    # Sort
    reverse = sort_by == "usage_count"
    tags.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
    
    return {
        "success": True,
        "data": {
            "tags": tags,
            "total": len(tags),
        },
    }


@router.get("/categories", response_model=dict)
async def list_categories():
    """
    List tag categories.
    """
    return {
        "success": True,
        "data": {
            "categories": [
                {"id": "project", "label": "Projet", "icon": "📁"},
                {"id": "priority", "label": "Priorité", "icon": "🔥"},
                {"id": "status", "label": "Statut", "icon": "📊"},
                {"id": "domain", "label": "Domaine", "icon": "🏷️"},
                {"id": "custom", "label": "Personnalisé", "icon": "⚙️"},
            ],
        },
    }


@router.get("/popular", response_model=dict)
async def get_popular_tags(limit: int = Query(10, ge=1, le=50)):
    """
    Get most used tags.
    """
    tags = sorted(MOCK_TAGS, key=lambda x: x["usage_count"], reverse=True)[:limit]
    
    return {
        "success": True,
        "data": {
            "tags": tags,
        },
    }


@router.get("/{tag_id}", response_model=dict)
async def get_tag(tag_id: str):
    """
    Get tag details.
    """
    tag = next((t for t in MOCK_TAGS if t["id"] == tag_id), None)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    return {
        "success": True,
        "data": tag,
    }


@router.post("", response_model=dict)
async def create_tag(data: TagCreate):
    """
    Create tag.
    """
    # Check if tag already exists
    existing = next((t for t in MOCK_TAGS if t["name"].lower() == data.name.lower()), None)
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    
    tag = {
        "id": f"tag_{len(MOCK_TAGS) + 1:03d}",
        "name": data.name.lower().replace(" ", "-"),
        "color": data.color or "#8D8371",
        "description": data.description,
        "category": data.category or "custom",
        "usage_count": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    MOCK_TAGS.append(tag)
    
    return {
        "success": True,
        "data": tag,
        "message": "Tag créé",
    }


@router.patch("/{tag_id}", response_model=dict)
async def update_tag(tag_id: str, data: TagUpdate):
    """
    Update tag.
    """
    tag = next((t for t in MOCK_TAGS if t["id"] == tag_id), None)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    if data.name:
        tag["name"] = data.name.lower().replace(" ", "-")
    if data.color:
        tag["color"] = data.color
    if data.description is not None:
        tag["description"] = data.description
    if data.category:
        tag["category"] = data.category
    
    return {
        "success": True,
        "data": tag,
    }


@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(tag_id: str):
    """
    Delete tag.
    """
    tag = next((t for t in MOCK_TAGS if t["id"] == tag_id), None)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    MOCK_TAGS.remove(tag)
    
    return {
        "success": True,
        "message": "Tag supprimé",
    }


# ============================================================================
# TAG ASSIGNMENTS
# ============================================================================

@router.get("/resource/{resource_type}/{resource_id}", response_model=dict)
async def get_resource_tags(resource_type: str, resource_id: str):
    """
    Get tags for a resource.
    """
    assignment = next(
        (a for a in MOCK_TAG_ASSIGNMENTS if a["resource_type"] == resource_type and a["resource_id"] == resource_id),
        None
    )
    
    tag_names = assignment["tags"] if assignment else []
    tags = [t for t in MOCK_TAGS if t["name"] in tag_names]
    
    return {
        "success": True,
        "data": {
            "tags": tags,
            "tag_names": tag_names,
        },
    }


@router.post("/resource/{resource_type}/{resource_id}", response_model=dict)
async def assign_tags(resource_type: str, resource_id: str, data: TagAssignment):
    """
    Assign tags to resource.
    """
    # Find or create assignment
    assignment = next(
        (a for a in MOCK_TAG_ASSIGNMENTS if a["resource_type"] == resource_type and a["resource_id"] == resource_id),
        None
    )
    
    if assignment:
        # Add new tags
        for tag_name in data.tags:
            if tag_name not in assignment["tags"]:
                assignment["tags"].append(tag_name)
    else:
        assignment = {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "tags": data.tags,
        }
        MOCK_TAG_ASSIGNMENTS.append(assignment)
    
    # Update usage counts
    for tag_name in data.tags:
        tag = next((t for t in MOCK_TAGS if t["name"] == tag_name), None)
        if tag:
            tag["usage_count"] += 1
    
    return {
        "success": True,
        "data": assignment,
        "message": "Tags assignés",
    }


@router.delete("/resource/{resource_type}/{resource_id}/{tag_name}", response_model=dict)
async def remove_tag_from_resource(resource_type: str, resource_id: str, tag_name: str):
    """
    Remove tag from resource.
    """
    assignment = next(
        (a for a in MOCK_TAG_ASSIGNMENTS if a["resource_type"] == resource_type and a["resource_id"] == resource_id),
        None
    )
    
    if assignment and tag_name in assignment["tags"]:
        assignment["tags"].remove(tag_name)
        
        # Update usage count
        tag = next((t for t in MOCK_TAGS if t["name"] == tag_name), None)
        if tag:
            tag["usage_count"] = max(0, tag["usage_count"] - 1)
    
    return {
        "success": True,
        "message": "Tag retiré",
    }


# ============================================================================
# SEARCH BY TAG
# ============================================================================

@router.get("/search/{tag_name}", response_model=dict)
async def search_by_tag(tag_name: str):
    """
    Find all resources with a specific tag.
    """
    resources = [
        {
            "resource_type": a["resource_type"],
            "resource_id": a["resource_id"],
        }
        for a in MOCK_TAG_ASSIGNMENTS
        if tag_name in a["tags"]
    ]
    
    return {
        "success": True,
        "data": {
            "tag": tag_name,
            "resources": resources,
            "total": len(resources),
        },
    }
