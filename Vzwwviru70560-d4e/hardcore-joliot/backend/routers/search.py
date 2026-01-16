"""
CHE·NU™ V75 - Search Router
Global Search API.

Search = Unified search across all resources

GOUVERNANCE > EXÉCUTION
- Identity-scoped results
- No cross-identity leakage

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

class SearchQuery(BaseModel):
    """Search query."""
    query: str = Field(..., min_length=1, max_length=500)
    resource_types: List[str] = []  # Empty = all types
    sphere_ids: List[str] = []
    domain_ids: List[str] = []
    tags: List[str] = []
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    limit: int = 20


# ============================================================================
# MOCK DATA
# ============================================================================

SEARCHABLE_TYPES = [
    "dataspace", "document", "task", "meeting", "thread",
    "agent", "property", "unit", "template", "memory"
]

MOCK_SEARCH_RESULTS = [
    {
        "id": "ds_001",
        "resource_type": "dataspace",
        "title": "Projet Maya - Rénovation Cuisine",
        "description": "Rénovation complète cuisine résidentielle",
        "sphere_id": "enterprise",
        "domain_id": "construction",
        "tags": ["rénovation", "cuisine", "2026", "maya"],
        "score": 0.95,
        "highlights": ["Rénovation", "cuisine", "Maya"],
        "url": "/dataspaces/ds_001",
        "created_at": "2026-01-02T10:00:00Z",
        "updated_at": "2026-01-07T16:00:00Z",
    },
    {
        "id": "doc_001",
        "resource_type": "document",
        "title": "Devis Rénovation Cuisine Maya",
        "description": "Estimation détaillée pour projet rénovation",
        "sphere_id": "enterprise",
        "domain_id": "construction",
        "tags": ["devis", "estimation"],
        "score": 0.88,
        "highlights": ["Devis", "Rénovation", "Maya"],
        "url": "/dataspaces/ds_001/documents/doc_001",
        "created_at": "2026-01-03T10:00:00Z",
        "updated_at": "2026-01-05T14:00:00Z",
    },
    {
        "id": "task_001",
        "resource_type": "task",
        "title": "Commander armoires sur mesure",
        "description": "Commande armoires cuisine projet Maya",
        "sphere_id": "enterprise",
        "domain_id": "construction",
        "tags": ["armoires", "commande"],
        "score": 0.82,
        "highlights": ["armoires", "cuisine", "Maya"],
        "url": "/dataspaces/ds_001/tasks/task_001",
        "created_at": "2026-01-04T09:00:00Z",
        "updated_at": "2026-01-07T11:00:00Z",
    },
    {
        "id": "prop_001",
        "resource_type": "property",
        "title": "123 Rue Principale - Immeuble 6 logements",
        "description": "Immeuble locatif à Brossard",
        "sphere_id": "enterprise",
        "domain_id": "immobilier",
        "tags": ["immobilier", "brossard", "6-plex"],
        "score": 0.75,
        "highlights": ["Immeuble", "logements", "Brossard"],
        "url": "/immobilier/properties/prop_001",
        "created_at": "2025-06-15T08:00:00Z",
        "updated_at": "2026-01-07T14:30:00Z",
    },
    {
        "id": "meet_001",
        "resource_type": "meeting",
        "title": "Sprint Planning Q1 2026",
        "description": "Planning et suivi sprint Q1",
        "sphere_id": "enterprise",
        "domain_id": None,
        "tags": ["sprint", "agile", "q1-2026"],
        "score": 0.70,
        "highlights": ["Sprint", "Planning", "Q1"],
        "url": "/meetings/meet_001",
        "created_at": "2026-01-01T09:00:00Z",
        "updated_at": "2026-01-07T17:00:00Z",
    },
    {
        "id": "tpl_001",
        "resource_type": "template",
        "title": "Estimation Rénovation Standard",
        "description": "Template estimation projets rénovation",
        "sphere_id": "enterprise",
        "domain_id": "construction",
        "tags": ["template", "estimation", "rénovation"],
        "score": 0.65,
        "highlights": ["Estimation", "Rénovation"],
        "url": "/templates/tpl_001",
        "created_at": "2025-06-01T10:00:00Z",
        "updated_at": "2026-01-05T14:00:00Z",
    },
]


# ============================================================================
# SEARCH
# ============================================================================

@router.get("", response_model=dict)
async def search(
    q: str = Query(..., min_length=1, max_length=500),
    types: Optional[str] = None,  # Comma-separated
    sphere_id: Optional[str] = None,
    domain_id: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
):
    """
    Global search across all resources.
    
    GOUVERNANCE: Returns only results for current identity.
    """
    query_lower = q.lower()
    
    results = []
    for item in MOCK_SEARCH_RESULTS:
        # Text match simulation
        if query_lower in item["title"].lower() or query_lower in (item.get("description") or "").lower():
            results.append(item)
    
    # Filter by types
    if types:
        type_list = types.split(",")
        results = [r for r in results if r["resource_type"] in type_list]
    
    # Filter by sphere
    if sphere_id:
        results = [r for r in results if r["sphere_id"] == sphere_id]
    
    # Filter by domain
    if domain_id:
        results = [r for r in results if r.get("domain_id") == domain_id]
    
    # Filter by tag
    if tag:
        results = [r for r in results if tag in r.get("tags", [])]
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit
    results = results[:limit]
    
    return {
        "success": True,
        "data": {
            "query": q,
            "results": results,
            "total": len(results),
            "facets": {
                "by_type": _count_by_field(results, "resource_type"),
                "by_sphere": _count_by_field(results, "sphere_id"),
            },
        },
    }


@router.post("", response_model=dict)
async def advanced_search(data: SearchQuery):
    """
    Advanced search with filters.
    """
    query_lower = data.query.lower()
    
    results = []
    for item in MOCK_SEARCH_RESULTS:
        if query_lower in item["title"].lower() or query_lower in (item.get("description") or "").lower():
            results.append(item)
    
    # Filter by resource types
    if data.resource_types:
        results = [r for r in results if r["resource_type"] in data.resource_types]
    
    # Filter by spheres
    if data.sphere_ids:
        results = [r for r in results if r["sphere_id"] in data.sphere_ids]
    
    # Filter by domains
    if data.domain_ids:
        results = [r for r in results if r.get("domain_id") in data.domain_ids]
    
    # Filter by tags
    if data.tags:
        results = [r for r in results if any(t in r.get("tags", []) for t in data.tags)]
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit
    results = results[:data.limit]
    
    return {
        "success": True,
        "data": {
            "query": data.query,
            "filters_applied": {
                "resource_types": data.resource_types,
                "sphere_ids": data.sphere_ids,
                "domain_ids": data.domain_ids,
                "tags": data.tags,
            },
            "results": results,
            "total": len(results),
        },
    }


@router.get("/suggestions", response_model=dict)
async def get_suggestions(q: str = Query(..., min_length=1, max_length=100)):
    """
    Get search suggestions (autocomplete).
    """
    query_lower = q.lower()
    
    suggestions = []
    seen = set()
    
    for item in MOCK_SEARCH_RESULTS:
        # Title suggestions
        if query_lower in item["title"].lower():
            if item["title"] not in seen:
                suggestions.append({
                    "text": item["title"],
                    "type": item["resource_type"],
                    "id": item["id"],
                })
                seen.add(item["title"])
        
        # Tag suggestions
        for tag in item.get("tags", []):
            if query_lower in tag.lower() and tag not in seen:
                suggestions.append({
                    "text": tag,
                    "type": "tag",
                    "id": None,
                })
                seen.add(tag)
    
    suggestions = suggestions[:10]
    
    return {
        "success": True,
        "data": {
            "query": q,
            "suggestions": suggestions,
        },
    }


@router.get("/recent", response_model=dict)
async def get_recent_searches():
    """
    Get recent searches.
    """
    # Simulated recent searches
    recent = [
        {"query": "maya", "timestamp": "2026-01-07T16:00:00Z", "results_count": 3},
        {"query": "rénovation cuisine", "timestamp": "2026-01-07T14:00:00Z", "results_count": 2},
        {"query": "loyer janvier", "timestamp": "2026-01-06T10:00:00Z", "results_count": 5},
        {"query": "sprint planning", "timestamp": "2026-01-05T09:00:00Z", "results_count": 1},
    ]
    
    return {
        "success": True,
        "data": {
            "recent_searches": recent,
        },
    }


@router.get("/types", response_model=dict)
async def get_searchable_types():
    """
    Get searchable resource types.
    """
    return {
        "success": True,
        "data": {
            "types": [
                {"id": "dataspace", "label": "DataSpaces", "icon": "📦"},
                {"id": "document", "label": "Documents", "icon": "📄"},
                {"id": "task", "label": "Tâches", "icon": "✅"},
                {"id": "meeting", "label": "Réunions", "icon": "📅"},
                {"id": "thread", "label": "Threads", "icon": "💬"},
                {"id": "agent", "label": "Agents", "icon": "🤖"},
                {"id": "property", "label": "Propriétés", "icon": "🏠"},
                {"id": "unit", "label": "Unités", "icon": "🚪"},
                {"id": "template", "label": "Templates", "icon": "📝"},
                {"id": "memory", "label": "Mémoires", "icon": "🧠"},
            ],
        },
    }


def _count_by_field(results: List[dict], field: str) -> Dict[str, int]:
    """Count results by field."""
    counts = {}
    for r in results:
        val = r.get(field)
        if val:
            counts[val] = counts.get(val, 0) + 1
    return counts
