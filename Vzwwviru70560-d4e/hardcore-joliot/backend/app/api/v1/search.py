"""
CHE·NU™ V75 — Advanced Search Service
======================================
Full-text search with filters across all entities
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import uuid4
from enum import Enum

from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.auth import get_current_user

router = APIRouter(prefix="/search", tags=["Search"])

# =============================================================================
# MODELS
# =============================================================================

class SearchResultType(str, Enum):
    THREAD = "thread"
    DECISION = "decision"
    AGENT = "agent"
    FILE = "file"
    NOTE = "note"
    CHECKPOINT = "checkpoint"

class SearchResult(BaseModel):
    id: str
    type: SearchResultType
    title: str
    description: Optional[str] = None
    sphere_id: Optional[str] = None
    sphere_name: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    relevance_score: float = 0.0
    highlights: List[str] = []
    url: str
    metadata: Dict[str, Any] = {}

class SearchResponse(BaseModel):
    query: str
    total: int
    page: int
    limit: int
    results: List[SearchResult]
    facets: Dict[str, Dict[str, int]] = {}
    suggestions: List[str] = []
    took_ms: float = 0.0

class SearchFilters(BaseModel):
    types: Optional[List[SearchResultType]] = None
    sphere_ids: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    status: Optional[List[str]] = None
    tags: Optional[List[str]] = None

# =============================================================================
# MOCK DATA
# =============================================================================

MOCK_DATA = {
    "threads": [
        {"id": "t1", "title": "Projet Marketing Q1", "description": "Stratégie marketing premier trimestre 2026", "sphere_id": "business", "created_at": "2026-01-05T10:00:00Z", "status": "active"},
        {"id": "t2", "title": "Refonte Site Web", "description": "Nouvelle version du site corporate", "sphere_id": "business", "created_at": "2026-01-03T14:00:00Z", "status": "active"},
        {"id": "t3", "title": "Formation IA", "description": "Cours sur l'intelligence artificielle", "sphere_id": "scholar", "created_at": "2026-01-02T09:00:00Z", "status": "active"},
        {"id": "t4", "title": "Budget Personnel 2026", "description": "Planification financière personnelle", "sphere_id": "personal", "created_at": "2026-01-01T08:00:00Z", "status": "active"},
        {"id": "t5", "title": "Événement Communautaire", "description": "Organisation meetup développeurs", "sphere_id": "community", "created_at": "2025-12-28T15:00:00Z", "status": "completed"},
    ],
    "decisions": [
        {"id": "d1", "title": "Choix Framework Frontend", "description": "React vs Vue vs Svelte", "sphere_id": "business", "created_at": "2026-01-06T11:00:00Z", "status": "pending"},
        {"id": "d2", "title": "Nouvelle Stratégie SEO", "description": "Optimisation moteurs de recherche", "sphere_id": "business", "created_at": "2026-01-04T16:00:00Z", "status": "approved"},
        {"id": "d3", "title": "Investissement Formation", "description": "Budget formation équipe", "sphere_id": "business", "created_at": "2026-01-02T10:00:00Z", "status": "pending"},
    ],
    "agents": [
        {"id": "a1", "title": "Research Agent", "description": "Recherche et analyse de données", "sphere_id": "scholar", "created_at": "2026-01-01T00:00:00Z", "status": "active"},
        {"id": "a2", "title": "Creative Writer", "description": "Génération de contenu créatif", "sphere_id": "studio", "created_at": "2026-01-01T00:00:00Z", "status": "active"},
        {"id": "a3", "title": "Data Analyst", "description": "Analyse données business", "sphere_id": "business", "created_at": "2026-01-01T00:00:00Z", "status": "active"},
        {"id": "a4", "title": "Task Manager", "description": "Gestion des tâches et rappels", "sphere_id": "personal", "created_at": "2026-01-01T00:00:00Z", "status": "active"},
    ],
    "files": [
        {"id": "f1", "title": "Rapport Q4 2025.pdf", "description": "Rapport trimestriel", "sphere_id": "business", "created_at": "2026-01-05T09:00:00Z"},
        {"id": "f2", "title": "Présentation Stratégie.pptx", "description": "Slides stratégie 2026", "sphere_id": "business", "created_at": "2026-01-04T14:00:00Z"},
        {"id": "f3", "title": "Notes Réunion.md", "description": "Notes de la réunion d'équipe", "sphere_id": "business", "created_at": "2026-01-03T11:00:00Z"},
    ],
}

SPHERE_NAMES = {
    "personal": "Personnel",
    "business": "Affaires",
    "government": "Gouvernement",
    "studio": "Studio Créatif",
    "community": "Communauté",
    "social": "Social & Média",
    "entertainment": "Divertissement",
    "myteam": "Mon Équipe",
    "scholar": "Scholar",
}

# =============================================================================
# SEARCH LOGIC
# =============================================================================

def calculate_relevance(query: str, title: str, description: str = "") -> float:
    """Calculate relevance score (0-1)"""
    query_lower = query.lower()
    title_lower = title.lower()
    desc_lower = (description or "").lower()
    
    score = 0.0
    
    # Exact match in title
    if query_lower in title_lower:
        score += 0.5
        if title_lower.startswith(query_lower):
            score += 0.2
    
    # Partial word match in title
    query_words = query_lower.split()
    title_words = title_lower.split()
    matching_words = sum(1 for qw in query_words for tw in title_words if qw in tw)
    score += (matching_words / max(len(query_words), 1)) * 0.2
    
    # Match in description
    if query_lower in desc_lower:
        score += 0.1
    
    return min(score, 1.0)

def extract_highlights(query: str, text: str, max_length: int = 100) -> List[str]:
    """Extract highlighted snippets"""
    if not text or not query:
        return []
    
    query_lower = query.lower()
    text_lower = text.lower()
    
    highlights = []
    pos = text_lower.find(query_lower)
    
    if pos != -1:
        start = max(0, pos - 30)
        end = min(len(text), pos + len(query) + 30)
        snippet = text[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        highlights.append(snippet)
    
    return highlights

def search_items(
    data_type: str,
    query: str,
    filters: SearchFilters,
    user_id: str,
) -> List[SearchResult]:
    """Search within a specific data type"""
    items = MOCK_DATA.get(data_type, [])
    results = []
    
    type_map = {
        "threads": SearchResultType.THREAD,
        "decisions": SearchResultType.DECISION,
        "agents": SearchResultType.AGENT,
        "files": SearchResultType.FILE,
    }
    
    url_map = {
        "threads": "/threads",
        "decisions": "/decisions",
        "agents": "/agents",
        "files": "/files",
    }
    
    for item in items:
        # Calculate relevance
        relevance = calculate_relevance(
            query,
            item.get("title", ""),
            item.get("description", "")
        )
        
        if relevance == 0:
            continue
        
        # Apply filters
        if filters.sphere_ids and item.get("sphere_id") not in filters.sphere_ids:
            continue
        
        if filters.status and item.get("status") not in filters.status:
            continue
        
        if filters.date_from:
            item_date = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
            if item_date < filters.date_from:
                continue
        
        if filters.date_to:
            item_date = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
            if item_date > filters.date_to:
                continue
        
        results.append(SearchResult(
            id=item["id"],
            type=type_map[data_type],
            title=item["title"],
            description=item.get("description"),
            sphere_id=item.get("sphere_id"),
            sphere_name=SPHERE_NAMES.get(item.get("sphere_id", "")),
            created_at=item["created_at"],
            relevance_score=relevance,
            highlights=extract_highlights(query, item.get("description", "")),
            url=f"{url_map[data_type]}/{item['id']}",
            metadata={"status": item.get("status")},
        ))
    
    return results

def get_suggestions(query: str) -> List[str]:
    """Get search suggestions based on query"""
    all_titles = []
    for data_type in MOCK_DATA:
        for item in MOCK_DATA[data_type]:
            all_titles.append(item["title"])
    
    query_lower = query.lower()
    suggestions = [
        title for title in all_titles
        if query_lower in title.lower() and title.lower() != query_lower
    ]
    
    return suggestions[:5]

def get_facets(results: List[SearchResult]) -> Dict[str, Dict[str, int]]:
    """Calculate facets from results"""
    type_counts: Dict[str, int] = {}
    sphere_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}
    
    for result in results:
        # Type facet
        type_counts[result.type.value] = type_counts.get(result.type.value, 0) + 1
        
        # Sphere facet
        if result.sphere_name:
            sphere_counts[result.sphere_name] = sphere_counts.get(result.sphere_name, 0) + 1
        
        # Status facet
        status = result.metadata.get("status")
        if status:
            status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "types": type_counts,
        "spheres": sphere_counts,
        "status": status_counts,
    }

# =============================================================================
# ROUTES
# =============================================================================

@router.get("/advanced", response_model=SearchResponse)
async def advanced_search(
    q: str = Query(..., min_length=2, description="Search query"),
    types: Optional[str] = Query(None, description="Comma-separated types: thread,decision,agent,file"),
    sphere_ids: Optional[str] = Query(None, description="Comma-separated sphere IDs"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    status: Optional[str] = Query(None, description="Comma-separated statuses"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """
    Advanced search across all entities.
    
    Supports:
    - Full-text search
    - Type filtering (thread, decision, agent, file)
    - Sphere filtering
    - Date range filtering
    - Status filtering
    - Faceted results
    - Search suggestions
    """
    import time
    start_time = time.time()
    
    user_id = current_user.get("id", "unknown")
    
    # Parse filters
    filters = SearchFilters(
        types=[SearchResultType(t.strip()) for t in types.split(",")] if types else None,
        sphere_ids=sphere_ids.split(",") if sphere_ids else None,
        date_from=date_from,
        date_to=date_to,
        status=status.split(",") if status else None,
    )
    
    # Determine which types to search
    search_types = ["threads", "decisions", "agents", "files"]
    if filters.types:
        type_map = {
            SearchResultType.THREAD: "threads",
            SearchResultType.DECISION: "decisions",
            SearchResultType.AGENT: "agents",
            SearchResultType.FILE: "files",
        }
        search_types = [type_map[t] for t in filters.types if t in type_map]
    
    # Perform search
    all_results = []
    for data_type in search_types:
        results = search_items(data_type, q, filters, user_id)
        all_results.extend(results)
    
    # Sort by relevance
    all_results.sort(key=lambda x: x.relevance_score, reverse=True)
    
    # Pagination
    total = len(all_results)
    start = (page - 1) * limit
    end = start + limit
    paginated_results = all_results[start:end]
    
    # Get facets and suggestions
    facets = get_facets(all_results)
    suggestions = get_suggestions(q)
    
    took_ms = (time.time() - start_time) * 1000
    
    return SearchResponse(
        query=q,
        total=total,
        page=page,
        limit=limit,
        results=paginated_results,
        facets=facets,
        suggestions=suggestions,
        took_ms=round(took_ms, 2),
    )


@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=10),
    current_user: dict = Depends(get_current_user),
):
    """Get search suggestions as user types"""
    suggestions = get_suggestions(q)[:limit]
    
    return {
        "success": True,
        "data": {
            "query": q,
            "suggestions": suggestions,
        }
    }


@router.get("/recent")
async def get_recent_searches(
    limit: int = Query(10, ge=1, le=20),
    current_user: dict = Depends(get_current_user),
):
    """Get user's recent searches"""
    # In production, this would be stored per user
    return {
        "success": True,
        "data": {
            "searches": [
                {"query": "marketing", "timestamp": "2026-01-08T10:00:00Z"},
                {"query": "budget", "timestamp": "2026-01-07T15:00:00Z"},
                {"query": "formation", "timestamp": "2026-01-06T09:00:00Z"},
            ]
        }
    }


@router.delete("/recent")
async def clear_recent_searches(
    current_user: dict = Depends(get_current_user),
):
    """Clear user's recent searches"""
    return {
        "success": True,
        "message": "Recent searches cleared",
    }
