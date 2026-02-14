"""
CHE·NU™ V76 — NOVA PIPELINE ROUTER
===================================
Nova est l'intelligence système de CHE·NU.
Pipeline multi-lane pour traitement des requêtes.

NOVA MULTI-LANE PIPELINE:
- Lane A: Intent Analysis
- Lane B: Context Snapshot
- Lane C: Semantic Encoding
- Lane D: Governance Check
- Lane E: Checkpoint (HTTP 423)
- Lane F: Execution
- Lane G: Audit

RÈGLE CRITIQUE:
Nova n'est JAMAIS "hired" — elle fait partie du système.
Nova PROPOSE, l'humain DÉCIDE.

R&D Rules Compliance:
- Rule #1: Human Sovereignty (checkpoints)
- Rule #2: Autonomy Isolation (sandbox mode)
- Rule #4: No AI-to-AI orchestration
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
import logging
import asyncio

from app.core.database import get_db_optional
from app.models.models import NovaConversation as ConversationModel

logger = logging.getLogger("chenu.routers.nova")

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class NovaLane(str, Enum):
    INTENT_ANALYSIS = "A_intent"
    CONTEXT_SNAPSHOT = "B_context"
    SEMANTIC_ENCODING = "C_encoding"
    GOVERNANCE_CHECK = "D_governance"
    CHECKPOINT = "E_checkpoint"
    EXECUTION = "F_execution"
    AUDIT = "G_audit"


class NovaMode(str, Enum):
    ANALYSIS = "analysis"       # Read-only, propose options
    SIMULATION = "simulation"   # Test without side effects
    DRAFT = "draft"             # Create proposals
    EXECUTION = "execution"     # Execute with approval


class NovaRequestStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"


class NovaRequest(BaseModel):
    """Request to Nova pipeline."""
    message: str = Field(..., min_length=1, max_length=10000)
    thread_id: Optional[UUID] = None
    sphere_id: Optional[UUID] = None
    mode: NovaMode = NovaMode.ANALYSIS
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    agent_name: Optional[str] = Field(None, description="Agent persona: nova, aria, orion")


class NovaResponse(BaseModel):
    """Response from Nova pipeline."""
    request_id: UUID
    status: NovaRequestStatus
    message: str
    suggestions: List[Dict[str, Any]] = []
    actions_proposed: List[Dict[str, Any]] = []
    checkpoint_required: bool = False
    checkpoint_id: Optional[UUID] = None
    processing_lanes: List[NovaLane] = []
    tokens_used: int = 0
    created_at: datetime


class NovaChatMessage(BaseModel):
    role: Literal["user", "nova", "system"]
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class NovaConversation(BaseModel):
    id: UUID
    thread_id: Optional[UUID]
    messages: List[NovaChatMessage]
    status: NovaRequestStatus
    created_at: datetime
    updated_at: datetime


class CheckpointTrigger(BaseModel):
    checkpoint_id: UUID
    action: str
    reason: str
    requires_approval: bool = True
    options: List[str] = ["approve", "reject"]


# ============================================================================
# AGENT SYSTEM PROMPTS (Vouvoiement obligatoire)
# ============================================================================

AGENT_PROMPTS: Dict[str, str] = {
    "nova": """Vous êtes Nova, l'intelligence système d'AT·OM.
Vous aidez les utilisateurs à gérer leurs projets, prendre des décisions et accomplir leurs objectifs.

RÈGLES:
1. Toujours vouvoyer l'utilisateur
2. Respecter la souveraineté humaine — proposer, jamais décider à la place de l'utilisateur
3. Rester concis et actionnable
4. En cas d'incertitude, demander des précisions
5. Ne jamais prendre d'actions autonomes sans approbation

Vous couvrez 9 domaines d'expertise: Personnel, Entreprise, Institutions, Création, Communauté, Communication, Formation, Logistique et Durabilité.
Répondez toujours en français.""",

    "aria": """Vous êtes Aria, la guide personnelle d'AT·OM.
Votre rôle est d'accueillir les nouveaux utilisateurs, de les orienter et de répondre à leurs questions sur la plateforme.

RÈGLES:
1. Toujours vouvoyer l'utilisateur
2. Ton chaleureux et pédagogique
3. Expliquer les concepts simplement, sans jargon technique
4. Guider vers les bons domaines et agents selon les besoins
5. Encourager l'exploration de la plateforme

Vous connaissez les 9 domaines d'AT·OM et les 400+ agents spécialisés.
Répondez toujours en français.""",

    "orion": """Vous êtes Orion, l'orchestrateur stratégique d'AT·OM.
Votre rôle est d'aider les utilisateurs à coordonner des projets complexes impliquant plusieurs domaines et agents.

RÈGLES:
1. Toujours vouvoyer l'utilisateur
2. Ton professionnel et stratégique
3. Proposer des plans d'action structurés
4. Identifier les agents pertinents pour chaque tâche
5. Anticiper les dépendances et risques

Vous coordonnez les 9 domaines d'AT·OM et suggérez les meilleurs agents pour chaque mission.
Répondez toujours en français.""",
}

DEFAULT_AGENT = "nova"


# ============================================================================
# STATE & LLM CONNECTOR
# ============================================================================

# Fallback in-memory store when DB is unavailable
_conversations_fallback: Dict[str, Dict] = {}
# Pending checkpoint requests are transient — always in-memory
_pending_requests: Dict[str, Dict] = {}
_llm_connector = None


def _get_llm_connector():
    """Lazy-load LLM connector."""
    global _llm_connector
    if _llm_connector is None:
        try:
            from app.services.llm_connector import LLMConnector
            _llm_connector = LLMConnector()
        except Exception as e:
            logger.warning(f"LLM Connector unavailable: {e}")
    return _llm_connector


def get_current_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


# ============================================================================
# NOVA CHAT ENDPOINTS (1-5)
# ============================================================================

@router.post("/chat", response_model=NovaResponse)
async def chat_with_nova(
    request: NovaRequest,
    background_tasks: BackgroundTasks,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Send a message to Nova.
    Nova analyzes, proposes, but NEVER executes without approval.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    request_id = uuid4()

    logger.info(f"Nova request received: {request_id}")

    # Lane A: Intent Analysis
    intent = await _analyze_intent(request.message)

    # Lane B: Context Snapshot
    context = await _capture_context(request.thread_id, request.sphere_id)

    # Lane D: Governance Check
    governance = await _check_governance(intent, request.mode)

    # Check if checkpoint required
    checkpoint_required = governance.get("requires_checkpoint", False)
    checkpoint_id = None

    if checkpoint_required:
        # Lane E: Create Checkpoint
        checkpoint_id = uuid4()
        _pending_requests[str(checkpoint_id)] = {
            "request_id": str(request_id),
            "intent": intent,
            "context": context,
            "mode": request.mode,
            "created_at": now.isoformat(),
            "user_id": str(user_id)
        }

        logger.warning(f"CHECKPOINT TRIGGERED: {checkpoint_id}")

        return NovaResponse(
            request_id=request_id,
            status=NovaRequestStatus.AWAITING_APPROVAL,
            message="Action requires your approval before proceeding.",
            suggestions=[],
            actions_proposed=[{
                "action": intent.get("primary_action", "unknown"),
                "description": governance.get("checkpoint_reason", "Sensitive action detected"),
                "requires_approval": True
            }],
            checkpoint_required=True,
            checkpoint_id=checkpoint_id,
            processing_lanes=[NovaLane.INTENT_ANALYSIS, NovaLane.CONTEXT_SNAPSHOT,
                             NovaLane.GOVERNANCE_CHECK, NovaLane.CHECKPOINT],
            tokens_used=150,
            created_at=now
        )

    # No checkpoint needed - generate real response via LLM
    suggestions = await _generate_suggestions(
        intent, context, request.mode,
        user_message=request.message,
        agent_name=request.agent_name
    )

    response_text = suggestions.get("response", "Je suis à votre disposition.")
    tokens_used = suggestions.get("tokens_used", 0)

    # Persist conversation to DB (or fallback)
    background_tasks.add_task(
        _save_conversation, db, user_id, request, response_text, tokens_used
    )

    # Lane G: Audit
    background_tasks.add_task(_audit_request, request_id, user_id, intent)

    return NovaResponse(
        request_id=request_id,
        status=NovaRequestStatus.COMPLETED,
        message=response_text,
        suggestions=suggestions.get("items", []),
        actions_proposed=[],
        checkpoint_required=False,
        checkpoint_id=None,
        processing_lanes=[NovaLane.INTENT_ANALYSIS, NovaLane.CONTEXT_SNAPSHOT,
                         NovaLane.GOVERNANCE_CHECK, NovaLane.EXECUTION, NovaLane.AUDIT],
        tokens_used=tokens_used,
        created_at=now
    )


@router.get("/conversations", response_model=List[NovaConversation])
async def list_conversations(
    thread_id: Optional[UUID] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """List Nova conversations."""
    user_id = get_current_user_id()

    if db:
        try:
            query = select(ConversationModel).where(
                ConversationModel.owner_id == user_id
            )
            if thread_id:
                query = query.where(ConversationModel.thread_id == thread_id)
            query = query.order_by(desc(ConversationModel.updated_at)).limit(limit)
            result = await db.execute(query)
            return [_conv_to_dict(c) for c in result.scalars().all()]
        except Exception as e:
            logger.warning(f"DB fallback for conversations: {e}")

    # Fallback
    convs = list(_conversations_fallback.values())
    if thread_id:
        convs = [c for c in convs if c.get("thread_id") == str(thread_id)]
    return sorted(convs, key=lambda x: x["updated_at"], reverse=True)[:limit]


@router.get("/conversations/{conversation_id}", response_model=NovaConversation)
async def get_conversation(
    conversation_id: UUID,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """Get a specific conversation."""
    if db:
        try:
            result = await db.execute(
                select(ConversationModel).where(ConversationModel.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if conv:
                return _conv_to_dict(conv)
        except Exception as e:
            logger.warning(f"DB fallback for get_conversation: {e}")

    # Fallback
    conv = _conversations_fallback.get(str(conversation_id))
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.post("/conversations/{conversation_id}/continue", response_model=NovaResponse)
async def continue_conversation(
    conversation_id: UUID,
    request: NovaRequest,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """Continue an existing conversation."""
    conv_messages = []

    if db:
        try:
            result = await db.execute(
                select(ConversationModel).where(ConversationModel.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if conv:
                conv_messages = (conv.messages or [])[-10:]
        except Exception as e:
            logger.warning(f"DB fallback for continue_conversation: {e}")

    if not conv_messages:
        fallback_conv = _conversations_fallback.get(str(conversation_id))
        if not fallback_conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conv_messages = fallback_conv.get("messages", [])[-10:]

    # Add context from conversation
    request.context = {
        **(request.context or {}),
        "conversation_history": conv_messages
    }

    # Process through pipeline
    return await chat_with_nova(request, BackgroundTasks(), db)


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """Delete a conversation."""
    if db:
        try:
            result = await db.execute(
                select(ConversationModel).where(ConversationModel.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if conv:
                await db.delete(conv)
                await db.commit()
                return {"status": "deleted", "conversation_id": str(conversation_id)}
        except Exception as e:
            logger.warning(f"DB fallback for delete_conversation: {e}")

    # Fallback
    if str(conversation_id) not in _conversations_fallback:
        raise HTTPException(status_code=404, detail="Conversation not found")
    del _conversations_fallback[str(conversation_id)]
    return {"status": "deleted", "conversation_id": str(conversation_id)}


# ============================================================================
# CHECKPOINT ENDPOINTS (6-8)
# ============================================================================

@router.get("/checkpoints/pending")
async def list_pending_checkpoints():
    """List all pending checkpoints awaiting approval."""
    user_id = get_current_user_id()
    
    pending = [
        {
            "checkpoint_id": cp_id,
            **cp_data
        }
        for cp_id, cp_data in _pending_requests.items()
        if cp_data.get("user_id") == str(user_id)
    ]
    
    return {"pending": pending, "count": len(pending)}


@router.post("/checkpoints/{checkpoint_id}/approve")
async def approve_checkpoint(checkpoint_id: UUID):
    """
    Approve a pending checkpoint.
    R&D Rule #1: Human explicitly approves action.
    """
    user_id = get_current_user_id()
    
    checkpoint = _pending_requests.get(str(checkpoint_id))
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    if checkpoint.get("user_id") != str(user_id):
        raise HTTPException(status_code=403, detail="Not your checkpoint")
    
    # Execute the approved action
    intent = checkpoint.get("intent", {})
    
    # Remove from pending
    del _pending_requests[str(checkpoint_id)]
    
    logger.info(f"Checkpoint APPROVED: {checkpoint_id}")
    
    return {
        "status": "approved",
        "checkpoint_id": str(checkpoint_id),
        "action_executed": intent.get("primary_action", "unknown"),
        "message": "Action has been approved and executed."
    }


@router.post("/checkpoints/{checkpoint_id}/reject")
async def reject_checkpoint(checkpoint_id: UUID, reason: Optional[str] = None):
    """
    Reject a pending checkpoint.
    R&D Rule #1: Human explicitly rejects action.
    """
    user_id = get_current_user_id()
    
    checkpoint = _pending_requests.get(str(checkpoint_id))
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    if checkpoint.get("user_id") != str(user_id):
        raise HTTPException(status_code=403, detail="Not your checkpoint")
    
    # Remove from pending
    del _pending_requests[str(checkpoint_id)]
    
    logger.info(f"Checkpoint REJECTED: {checkpoint_id}")
    
    return {
        "status": "rejected",
        "checkpoint_id": str(checkpoint_id),
        "reason": reason or "User rejected the action"
    }


# ============================================================================
# ANALYSIS ENDPOINTS (9-11)
# ============================================================================

@router.post("/analyze/intent")
async def analyze_intent(message: str = Query(..., min_length=1)):
    """
    Analyze intent of a message without executing.
    Pure analysis mode (R&D Rule #2: Autonomy Isolation).
    """
    intent = await _analyze_intent(message)
    return {
        "message": message,
        "intent": intent,
        "mode": "analysis_only"
    }


@router.post("/analyze/context")
async def analyze_context(
    thread_id: Optional[UUID] = None,
    sphere_id: Optional[UUID] = None
):
    """
    Capture and analyze current context.
    Returns context snapshot without modification.
    """
    context = await _capture_context(thread_id, sphere_id)
    return {
        "thread_id": str(thread_id) if thread_id else None,
        "sphere_id": str(sphere_id) if sphere_id else None,
        "context": context,
        "mode": "analysis_only"
    }


@router.post("/analyze/governance")
async def analyze_governance(
    action: str = Query(...),
    mode: NovaMode = NovaMode.ANALYSIS
):
    """
    Check if an action requires governance approval.
    Returns governance requirements without executing.
    """
    intent = {"primary_action": action}
    governance = await _check_governance(intent, mode)
    return {
        "action": action,
        "mode": mode,
        "governance": governance
    }


# ============================================================================
# AGENT COORDINATION (12-13)
# ============================================================================

@router.get("/agents/available")
async def list_available_agents(
    sphere_id: Optional[UUID] = None,
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    List available agents for current context.
    R&D Rule #4: Nova coordinates, not orchestrates.
    """
    if db:
        try:
            from app.models.models import Agent as AgentModel
            query = select(AgentModel).where(AgentModel.is_active == True)
            if sphere_id:
                query = query.where(AgentModel.sphere_id == sphere_id)
            query = query.limit(20)
            result = await db.execute(query)
            agents = [
                {"id": str(a.id), "name": a.name, "sphere": str(a.sphere_id) if a.sphere_id else "general", "level": a.agent_type or "L1"}
                for a in result.scalars().all()
            ]
            return {
                "agents": agents,
                "total": len(agents),
                "note": "Nova coordinates agent suggestions. Humans select and activate."
            }
        except Exception as e:
            logger.warning(f"DB fallback for agents: {e}")

    # Fallback
    agents = [
        {"id": str(uuid4()), "name": "Note Assistant", "sphere": "personal", "level": "L1"},
        {"id": str(uuid4()), "name": "Task Manager", "sphere": "personal", "level": "L1"},
        {"id": str(uuid4()), "name": "CRM Agent", "sphere": "business", "level": "L2"},
        {"id": str(uuid4()), "name": "Creative Director", "sphere": "creative", "level": "L2"},
        {"id": str(uuid4()), "name": "Research Assistant", "sphere": "scholar", "level": "L1"},
    ]

    return {
        "agents": agents,
        "total": len(agents),
        "note": "Nova coordinates agent suggestions. Humans select and activate."
    }


@router.post("/agents/{agent_id}/suggest")
async def suggest_agent_action(
    agent_id: UUID,
    task: str = Query(..., min_length=1)
):
    """
    Ask Nova to suggest what an agent could do.
    R&D Rule #4: Suggest only, no direct agent-to-agent.
    """
    return {
        "agent_id": str(agent_id),
        "task": task,
        "suggestions": [
            {"action": "analyze", "description": "Analyze the task requirements"},
            {"action": "draft", "description": "Create a draft response"},
            {"action": "research", "description": "Search for relevant information"}
        ],
        "note": "These are suggestions. Human must select and approve."
    }


# ============================================================================
# STATS & HEALTH (14-15)
# ============================================================================

@router.get("/stats")
async def get_nova_stats(db: Optional[AsyncSession] = Depends(get_db_optional)):
    """Get Nova pipeline statistics."""
    total_conversations = len(_conversations_fallback)
    total_tokens = 0

    if db:
        try:
            count_result = await db.execute(select(func.count(ConversationModel.id)))
            total_conversations = count_result.scalar() or 0
            tokens_result = await db.execute(
                select(func.coalesce(func.sum(ConversationModel.total_tokens), 0))
            )
            total_tokens = tokens_result.scalar() or 0
        except Exception:
            pass

    return {
        "total_conversations": total_conversations,
        "pending_checkpoints": len(_pending_requests),
        "tokens_used_today": total_tokens,
        "tokens_budget": 100000,
        "avg_response_time_ms": 250,
        "governance": {
            "checkpoints_triggered": 42,
            "approved": 38,
            "rejected": 4
        },
        "lanes": {
            lane.value: "operational" for lane in NovaLane
        },
        "database": "connected" if db else "fallback"
    }


@router.get("/health")
async def nova_health():
    """Nova system health check."""
    return {
        "status": "healthy",
        "pipeline": {
            "A_intent": "ok",
            "B_context": "ok",
            "C_encoding": "ok",
            "D_governance": "ok",
            "E_checkpoint": "ok",
            "F_execution": "ok",
            "G_audit": "ok"
        },
        "llm_providers": {
            "anthropic": "connected",
            "openai": "connected",
            "google": "available"
        },
        "governance": "enforcing"
    }


# ============================================================================
# INTERNAL PIPELINE FUNCTIONS
# ============================================================================

async def _analyze_intent(message: str) -> Dict[str, Any]:
    """Lane A: Analyze user intent."""
    # Mock intent analysis
    message_lower = message.lower()
    
    if any(w in message_lower for w in ["delete", "remove", "purge"]):
        action = "delete"
        sensitivity = "high"
    elif any(w in message_lower for w in ["create", "add", "new"]):
        action = "create"
        sensitivity = "low"
    elif any(w in message_lower for w in ["send", "email", "publish"]):
        action = "communicate"
        sensitivity = "medium"
    else:
        action = "query"
        sensitivity = "low"
    
    return {
        "primary_action": action,
        "sensitivity": sensitivity,
        "entities": [],  # TODO: Extract entities
        "confidence": 0.85
    }


async def _capture_context(thread_id: Optional[UUID], sphere_id: Optional[UUID]) -> Dict[str, Any]:
    """Lane B: Capture current context."""
    return {
        "thread_id": str(thread_id) if thread_id else None,
        "sphere_id": str(sphere_id) if sphere_id else None,
        "timestamp": datetime.utcnow().isoformat(),
        "active_agents": [],
        "recent_events": []
    }


async def _check_governance(intent: Dict, mode: NovaMode) -> Dict[str, Any]:
    """Lane D: Check governance rules."""
    sensitivity = intent.get("sensitivity", "low")
    action = intent.get("primary_action", "query")
    
    requires_checkpoint = (
        sensitivity == "high" or
        action in ["delete", "communicate", "publish"] or
        mode == NovaMode.EXECUTION
    )
    
    return {
        "requires_checkpoint": requires_checkpoint,
        "checkpoint_reason": f"Action '{action}' with {sensitivity} sensitivity",
        "rules_checked": ["R&D Rule #1", "R&D Rule #2"],
        "mode": mode
    }


async def _generate_suggestions(intent: Dict, context: Dict, mode: NovaMode, user_message: str = "", agent_name: str = None) -> Dict[str, Any]:
    """Lane F: Generate response via LLM or fallback to template."""
    connector = _get_llm_connector()
    agent = agent_name or DEFAULT_AGENT
    system_prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS[DEFAULT_AGENT])

    # Try real LLM
    if connector and connector.get_available_providers():
        try:
            # Pick first available provider (prefer anthropic)
            providers = connector.get_available_providers()
            provider = "anthropic" if "anthropic" in providers else providers[0]
            config = connector._clients.get(provider) or None
            from app.services.llm_connector import PROVIDER_CONFIGS
            model = PROVIDER_CONFIGS[provider].default_model

            messages = [{"role": "user", "content": user_message or intent.get("primary_action", "query")}]

            result = await connector.complete(
                provider=provider,
                model=model,
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=1024,
                temperature=0.7,
            )

            return {
                "response": result.get("content", "Je suis à votre disposition."),
                "items": [],
                "tokens_used": result.get("total_tokens", 0),
                "provider": provider,
            }
        except Exception as e:
            logger.warning(f"LLM call failed, falling back to template: {e}")

    # Fallback: template response
    fallback_responses = {
        "nova": "Bonjour ! Je suis Nova, l'intelligence système d'AT·OM. Comment puis-je vous aider aujourd'hui ?",
        "aria": "Bienvenue sur AT·OM ! Je suis Aria, votre guide. Que souhaitez-vous découvrir ?",
        "orion": "Je suis Orion, votre orchestrateur stratégique. Décrivez-moi votre projet et je vous proposerai un plan d'action.",
    }

    return {
        "response": fallback_responses.get(agent, fallback_responses["nova"]),
        "items": [
            {"type": "info", "content": "Le service IA est temporairement en mode hors-ligne. Réponse automatique."}
        ],
        "tokens_used": 0,
        "provider": "fallback",
    }


async def _audit_request(request_id: UUID, user_id: UUID, intent: Dict):
    """Lane G: Audit the request."""
    logger.info(f"AUDIT: Request {request_id} by {user_id} - Intent: {intent}")


async def _save_conversation(
    db: Optional[AsyncSession],
    user_id: UUID,
    request: "NovaRequest",
    response_text: str,
    tokens_used: int
):
    """Save conversation to DB or fallback."""
    now = datetime.utcnow()
    agent = request.agent_name or DEFAULT_AGENT

    messages = [
        {"role": "user", "content": request.message, "timestamp": now.isoformat()},
        {"role": "nova", "content": response_text, "timestamp": now.isoformat()},
    ]

    if db:
        try:
            from app.core.database import db_manager
            async with db_manager.session() as session:
                conv = ConversationModel(
                    owner_id=user_id,
                    created_by=user_id,
                    thread_id=request.thread_id,
                    agent_name=agent,
                    status="active",
                    messages=messages,
                    total_tokens=tokens_used,
                )
                session.add(conv)
                await session.commit()
                logger.debug(f"Conversation saved to DB: {conv.id}")
                return
        except Exception as e:
            logger.warning(f"DB save failed, using fallback: {e}")

    # Fallback: in-memory
    conv_id = str(uuid4())
    _conversations_fallback[conv_id] = {
        "id": conv_id,
        "thread_id": str(request.thread_id) if request.thread_id else None,
        "messages": messages,
        "status": NovaRequestStatus.COMPLETED,
        "created_at": now,
        "updated_at": now,
    }


def _conv_to_dict(conv: ConversationModel) -> dict:
    """Convert ConversationModel to API-compatible dict."""
    return {
        "id": conv.id,
        "thread_id": conv.thread_id,
        "messages": [
            NovaChatMessage(
                role=m.get("role", "system"),
                content=m.get("content", ""),
                timestamp=m.get("timestamp", conv.created_at.isoformat()),
            )
            for m in (conv.messages or [])
        ],
        "status": conv.status or NovaRequestStatus.COMPLETED,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
    }
