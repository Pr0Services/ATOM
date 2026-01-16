"""
CHE·NU™ V75 Backend - Nova Router

RÈGLE: Nova = L0 système
- Toujours disponible
- READ ONLY - suggère mais ne décide pas
- L'humain garde le contrôle

@version 75.0.0
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
import uuid

from config import get_db, settings
from schemas.base import BaseResponse
from routers.auth import require_auth

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class NovaStatus(BaseModel):
    """Nova system status."""
    available: bool = True
    status: str = "online"  # 'online', 'busy', 'maintenance'
    model: str = "nova-v75"
    capabilities: List[str] = []
    response_time_ms: int = 0
    last_active: datetime


class NovaQuery(BaseModel):
    """Query to Nova."""
    query: str
    context: Optional[dict] = None
    thread_id: Optional[str] = None
    sphere_id: Optional[str] = None


class NovaResponse(BaseModel):
    """Response from Nova."""
    id: str
    query: str
    response: str
    suggestions: List["NovaSuggestion"] = []
    confidence: float = 0.0
    sources: List[str] = []
    processing_time_ms: int
    created_at: datetime


class NovaSuggestion(BaseModel):
    """Nova suggestion (user decides whether to accept)."""
    id: str
    type: str  # 'action', 'agent', 'dataspace', 'thread'
    title: str
    description: str
    confidence: float
    metadata: dict = {}


class NovaExplanation(BaseModel):
    """Nova explanation for transparency."""
    id: str
    topic: str
    explanation: str
    reasoning_steps: List[str] = []
    sources: List[str] = []
    created_at: datetime


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/status", response_model=BaseResponse[NovaStatus])
async def get_nova_status(
    user: dict = Depends(require_auth),
):
    """Get Nova system status."""
    return BaseResponse(
        success=True,
        data=NovaStatus(
            available=settings.NOVA_ENABLED,
            status="online",
            model="nova-v75",
            capabilities=[
                "analysis",
                "research",
                "summarization",
                "suggestion",
                "explanation",
            ],
            response_time_ms=150,
            last_active=datetime.utcnow(),
        ),
    )


@router.post("/query", response_model=BaseResponse[NovaResponse])
async def query_nova(
    request: NovaQuery,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Query Nova for assistance.
    
    RÈGLE: Nova suggère, l'humain décide.
    """
    now = datetime.utcnow()
    
    # TODO: Implement actual LLM call
    # For now, mock response
    
    response = NovaResponse(
        id=str(uuid.uuid4()),
        query=request.query,
        response=f"Je comprends votre question sur '{request.query}'. Voici mon analyse...",
        suggestions=[
            NovaSuggestion(
                id="sug-1",
                type="action",
                title="Create a new thread",
                description="Based on your query, you might want to start a dedicated thread for this topic",
                confidence=0.85,
            ),
            NovaSuggestion(
                id="sug-2",
                type="agent",
                title="Hire Research Assistant",
                description="A research agent could help gather more information",
                confidence=0.72,
            ),
        ],
        confidence=0.88,
        sources=["knowledge_base", "context"],
        processing_time_ms=250,
        created_at=now,
    )
    
    return BaseResponse(success=True, data=response)


@router.get("/suggestions", response_model=BaseResponse[List[NovaSuggestion]])
async def get_nova_suggestions(
    user: dict = Depends(require_auth),
    context_type: Optional[str] = None,
    sphere_id: Optional[str] = None,
    limit: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """
    Get contextual suggestions from Nova.
    
    RÈGLE: Suggestions only - user decides whether to act.
    """
    suggestions = [
        NovaSuggestion(
            id="sug-1",
            type="action",
            title="Review pending decisions",
            description="You have 3 decisions awaiting your input",
            confidence=0.95,
            metadata={"count": 3, "urgent": 1},
        ),
        NovaSuggestion(
            id="sug-2",
            type="thread",
            title="Continue Q4 planning",
            description="Your Q4 planning thread has new activity",
            confidence=0.82,
            metadata={"thread_id": "thread-1"},
        ),
    ]
    
    return BaseResponse(success=True, data=suggestions[:limit])


@router.get("/explain/{topic}", response_model=BaseResponse[NovaExplanation])
async def get_nova_explanation(
    topic: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Get Nova's explanation on a topic.
    
    For transparency and understanding.
    """
    now = datetime.utcnow()
    
    explanation = NovaExplanation(
        id=str(uuid.uuid4()),
        topic=topic,
        explanation=f"Voici mon explication sur '{topic}'...",
        reasoning_steps=[
            "Analyse du contexte actuel",
            "Identification des éléments pertinents",
            "Formulation de la réponse",
        ],
        sources=["documentation", "knowledge_base"],
        created_at=now,
    )
    
    return BaseResponse(success=True, data=explanation)


@router.get("/conversation", response_model=BaseResponse[List[NovaResponse]])
async def get_conversation_history(
    user: dict = Depends(require_auth),
    thread_id: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get conversation history with Nova."""
    now = datetime.utcnow()
    
    # TODO: Fetch from database
    history = [
        NovaResponse(
            id="resp-1",
            query="What's the status of Q4 planning?",
            response="Q4 planning is progressing well...",
            suggestions=[],
            confidence=0.9,
            processing_time_ms=200,
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=history[:limit])
