"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ V72 — API V1 ROUTER                               ║
║                                                                              ║
║  All API endpoints                                                           ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.security import HTTPBearer
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.schemas import *
from app.core.auth import get_current_user, create_access_token
from app.core.governance import check_governance, create_checkpoint
from app.services import *

router = APIRouter()
security = HTTPBearer()

# ═══════════════════════════════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/auth/login", response_model=ApiResponse[LoginResponse], tags=["Auth"])
async def login(credentials: LoginRequest):
    """Authenticate user and return tokens."""
    # TODO: Implement actual authentication
    user = User(
        id=str(uuid.uuid4()),
        email=credentials.email,
        username=credentials.email.split("@")[0],
        created_at=datetime.utcnow(),
    )
    
    access_token = create_access_token({"sub": user.id})
    refresh_token = create_access_token({"sub": user.id}, expires_delta=timedelta(days=7))
    
    return ApiResponse(
        success=True,
        data=LoginResponse(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )
    )

@router.post("/auth/logout", response_model=ApiResponse[None], tags=["Auth"])
async def logout(current_user: User = Depends(get_current_user)):
    """Logout current user."""
    # TODO: Invalidate token
    return ApiResponse(success=True, data=None, message="Logged out successfully")

@router.post("/auth/refresh", response_model=ApiResponse[LoginResponse], tags=["Auth"])
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    """Refresh access token."""
    # TODO: Implement token refresh
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/auth/me", response_model=ApiResponse[User], tags=["Auth"])
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return ApiResponse(success=True, data=current_user)

@router.patch("/auth/preferences", response_model=ApiResponse[User], tags=["Auth"])
async def update_preferences(
    preferences: UserPreferences,
    current_user: User = Depends(get_current_user)
):
    """Update user preferences."""
    current_user.preferences = preferences
    return ApiResponse(success=True, data=current_user)

# ═══════════════════════════════════════════════════════════════════════════════
# SPHERES ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/spheres", response_model=ApiResponse[List[Sphere]], tags=["Spheres"])
async def list_spheres(current_user: User = Depends(get_current_user)):
    """List all 9 spheres."""
    spheres = [
        Sphere(id="personal", name_fr="Personnel", name_en="Personal", 
               icon="🏠", color="#3EB4A2", order=0,
               description_fr="Vie privée, santé, bien-être",
               description_en="Private life, health, wellbeing",
               stats=SphereStats(threads_count=5, decisions_count=3, agents_count=2, files_count=12, meetings_count=1)),
        Sphere(id="business", name_fr="Affaires", name_en="Business",
               icon="💼", color="#D8B26A", order=1,
               description_fr="Entreprise, carrière, finances",
               description_en="Business, career, finances",
               stats=SphereStats(threads_count=8, decisions_count=5, agents_count=4, files_count=28, meetings_count=3)),
        Sphere(id="government", name_fr="Gouvernement", name_en="Government",
               icon="🏛️", color="#8B5CF6", order=2,
               description_fr="Relations institutionnelles",
               description_en="Institutional relations",
               stats=SphereStats(threads_count=2, decisions_count=1, agents_count=1, files_count=5, meetings_count=0)),
        Sphere(id="studio", name_fr="Studio", name_en="Studio",
               icon="🎨", color="#EC4899", order=3,
               description_fr="Création, art, projets créatifs",
               description_en="Creation, art, creative projects",
               stats=SphereStats(threads_count=4, decisions_count=2, agents_count=3, files_count=45, meetings_count=1)),
        Sphere(id="community", name_fr="Communauté", name_en="Community",
               icon="👥", color="#F59E0B", order=4,
               description_fr="Associations, bénévolat",
               description_en="Associations, volunteering",
               stats=SphereStats(threads_count=3, decisions_count=1, agents_count=1, files_count=8, meetings_count=2)),
        Sphere(id="social", name_fr="Social & Médias", name_en="Social & Media",
               icon="📱", color="#3B82F6", order=5,
               description_fr="Réseaux, communication",
               description_en="Networks, communication",
               stats=SphereStats(threads_count=6, decisions_count=4, agents_count=2, files_count=15, meetings_count=0)),
        Sphere(id="entertainment", name_fr="Divertissement", name_en="Entertainment",
               icon="🎮", color="#EF4444", order=6,
               description_fr="Loisirs, culture",
               description_en="Leisure, culture",
               stats=SphereStats(threads_count=2, decisions_count=0, agents_count=1, files_count=3, meetings_count=0)),
        Sphere(id="team", name_fr="Mon Équipe", name_en="My Team",
               icon="👔", color="#10B981", order=7,
               description_fr="RH, collaborateurs",
               description_en="HR, collaborators",
               stats=SphereStats(threads_count=7, decisions_count=6, agents_count=5, files_count=32, meetings_count=4)),
        Sphere(id="scholar", name_fr="Scholar", name_en="Scholar",
               icon="📚", color="#6366F1", order=8,
               description_fr="Apprentissage, formation",
               description_en="Learning, training",
               stats=SphereStats(threads_count=3, decisions_count=1, agents_count=2, files_count=18, meetings_count=1)),
    ]
    return ApiResponse(success=True, data=spheres)

@router.get("/spheres/{sphere_id}", response_model=ApiResponse[Sphere], tags=["Spheres"])
async def get_sphere(sphere_id: str, current_user: User = Depends(get_current_user)):
    """Get sphere by ID."""
    # TODO: Implement database lookup
    return ApiResponse(success=True, data=Sphere(
        id=sphere_id,
        name_fr="Sphère",
        name_en="Sphere",
        icon="🌐",
        color="#3EB4A2",
        order=0,
        description_fr="Description",
        description_en="Description",
        stats=SphereStats()
    ))

@router.get("/spheres/{sphere_id}/stats", response_model=ApiResponse[SphereStats], tags=["Spheres"])
async def get_sphere_stats(sphere_id: str, current_user: User = Depends(get_current_user)):
    """Get sphere statistics."""
    return ApiResponse(success=True, data=SphereStats(
        threads_count=5,
        decisions_count=3,
        agents_count=2,
        files_count=15,
        meetings_count=2
    ))

# ═══════════════════════════════════════════════════════════════════════════════
# THREADS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/threads", response_model=ApiResponse[List[Thread]], tags=["Threads"])
async def list_threads(
    sphere_id: Optional[str] = None,
    status: Optional[str] = None,
    maturity_level: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """List threads with optional filters."""
    # TODO: Implement database query
    threads = [
        Thread(
            id=str(uuid.uuid4()),
            title="Rénovation cuisine",
            founding_intent="Améliorer notre qualité de vie familiale en rénovant la cuisine",
            sphere_id="personal",
            status="active",
            maturity_level="GROWING",
            maturity_score=65,
            events_count=12,
            decisions_count=3,
            created_at=datetime.utcnow() - timedelta(days=30),
            updated_at=datetime.utcnow() - timedelta(hours=2),
            last_activity_at=datetime.utcnow() - timedelta(hours=2),
        ),
        Thread(
            id=str(uuid.uuid4()),
            title="Lancement produit Q2",
            founding_intent="Lancer notre nouveau produit avec succès au Q2 2025",
            sphere_id="business",
            status="active",
            maturity_level="SPROUTING",
            maturity_score=35,
            events_count=8,
            decisions_count=5,
            created_at=datetime.utcnow() - timedelta(days=15),
            updated_at=datetime.utcnow() - timedelta(hours=5),
            last_activity_at=datetime.utcnow() - timedelta(hours=5),
        ),
    ]
    return ApiResponse(success=True, data=threads)

@router.post("/threads", response_model=ApiResponse[Thread], tags=["Threads"])
async def create_thread(
    data: CreateThreadRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new thread."""
    thread = Thread(
        id=str(uuid.uuid4()),
        title=data.title,
        founding_intent=data.founding_intent,
        sphere_id=data.sphere_id,
        status="active",
        maturity_level="SEED",
        maturity_score=0,
        events_count=0,
        decisions_count=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_activity_at=datetime.utcnow(),
    )
    return ApiResponse(success=True, data=thread)

@router.get("/threads/{thread_id}", response_model=ApiResponse[Thread], tags=["Threads"])
async def get_thread(thread_id: str, current_user: User = Depends(get_current_user)):
    """Get thread by ID."""
    # TODO: Implement database lookup
    return ApiResponse(success=True, data=Thread(
        id=thread_id,
        title="Thread",
        founding_intent="Founding intent",
        sphere_id="personal",
        status="active",
        maturity_level="GROWING",
        maturity_score=50,
        events_count=5,
        decisions_count=2,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_activity_at=datetime.utcnow(),
    ))

@router.patch("/threads/{thread_id}", response_model=ApiResponse[Thread], tags=["Threads"])
async def update_thread(
    thread_id: str,
    data: UpdateThreadRequest,
    current_user: User = Depends(get_current_user)
):
    """Update thread."""
    # TODO: Implement update
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/threads/{thread_id}/archive", response_model=ApiResponse[Thread], tags=["Threads"])
async def archive_thread(thread_id: str, current_user: User = Depends(get_current_user)):
    """Archive a thread."""
    # Requires checkpoint
    checkpoint = await create_checkpoint(
        action_type="thread_archive",
        description=f"Archiving thread {thread_id}",
        requested_by=current_user.id,
        risk_level="medium"
    )
    return ApiResponse(success=True, data=None, message="Checkpoint created for approval")

# ═══════════════════════════════════════════════════════════════════════════════
# DECISIONS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/decisions", response_model=ApiResponse[List[Decision]], tags=["Decisions"])
async def list_decisions(
    sphere_id: Optional[str] = None,
    status: Optional[str] = None,
    aging_level: Optional[str] = None,
    priority: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """List decisions with optional filters."""
    decisions = [
        Decision(
            id=str(uuid.uuid4()),
            title="Choix du contracteur",
            description="Sélectionner le contracteur pour les travaux de rénovation",
            context="3 devis reçus, budget de 25k€",
            sphere_id="personal",
            status="pending",
            priority="high",
            aging_level="YELLOW",
            aging_started_at=datetime.utcnow() - timedelta(days=3),
            deadline=datetime.utcnow() + timedelta(days=4),
            options=[
                DecisionOption(id="opt1", label="Contracteur A", description="Le moins cher",
                               pros=["Prix compétitif", "Disponible rapidement"],
                               cons=["Moins d'expérience"], estimated_impact="medium"),
                DecisionOption(id="opt2", label="Contracteur B", description="Le plus expérimenté",
                               pros=["20 ans d'expérience", "Bonnes références"],
                               cons=["Plus cher", "Délai 3 semaines"], estimated_impact="high"),
            ],
            ai_suggestions=[
                AISuggestion(id="sug1", type="recommendation", 
                            content="Contracteur B recommandé pour ce type de projet",
                            confidence=0.85, source="Analysis Engine"),
            ],
            created_at=datetime.utcnow() - timedelta(days=5),
            updated_at=datetime.utcnow(),
        ),
    ]
    return ApiResponse(success=True, data=decisions)

@router.get("/decisions/stats", response_model=ApiResponse[DecisionStats], tags=["Decisions"])
async def get_decision_stats(current_user: User = Depends(get_current_user)):
    """Get decision statistics."""
    return ApiResponse(success=True, data=DecisionStats(
        total=15,
        by_aging={"GREEN": 5, "YELLOW": 6, "RED": 3, "BLINK": 1},
        by_priority={"low": 4, "medium": 7, "high": 3, "critical": 1}
    ))

@router.get("/decisions/{decision_id}", response_model=ApiResponse[Decision], tags=["Decisions"])
async def get_decision(decision_id: str, current_user: User = Depends(get_current_user)):
    """Get decision by ID."""
    # TODO: Implement
    raise HTTPException(status_code=404, detail="Decision not found")

@router.post("/decisions/make", response_model=ApiResponse[Decision], tags=["Decisions"])
async def make_decision(
    data: MakeDecisionRequest,
    current_user: User = Depends(get_current_user)
):
    """Make a decision (approve an option)."""
    # Requires checkpoint for high-impact decisions
    checkpoint = await create_checkpoint(
        action_type="decision_make",
        description=f"Making decision {data.decision_id}",
        requested_by=current_user.id,
        risk_level="medium"
    )
    return ApiResponse(success=True, data=None, message="Checkpoint created")

@router.post("/decisions/{decision_id}/defer", response_model=ApiResponse[Decision], tags=["Decisions"])
async def defer_decision(
    decision_id: str,
    reason: Optional[str] = Body(None, embed=True),
    current_user: User = Depends(get_current_user)
):
    """Defer a decision."""
    return ApiResponse(success=True, data=None, message="Decision deferred")

# ═══════════════════════════════════════════════════════════════════════════════
# AGENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/agents", response_model=ApiResponse[List[Agent]], tags=["Agents"])
async def list_agents(
    level: Optional[int] = None,
    domain: Optional[str] = None,
    hired_only: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """List available agents."""
    # TODO: Load from agents catalog
    agents = [
        Agent(
            id="agent-construction-1",
            name_fr="Superviseur de Chantier",
            name_en="Construction Supervisor",
            level=2,
            domain="construction",
            capabilities=["planning", "coordination", "quality_control"],
            description_fr="Expert en supervision de travaux de construction",
            description_en="Expert in construction supervision",
            personality="Méthodique et rigoureux",
            communication_style="Direct et professionnel",
            cost=150,
            is_system=False,
            is_hired=True,
            hired_at=datetime.utcnow() - timedelta(days=10),
        ),
    ]
    return ApiResponse(success=True, data=agents)

@router.get("/agents/stats", response_model=ApiResponse[dict], tags=["Agents"])
async def get_agents_stats(current_user: User = Depends(get_current_user)):
    """Get agent statistics."""
    stats = {
        "total_agents": 226,
        "hired_agents": 8,
        "available_agents": 218,
        "by_domain": {
            "construction": 34,
            "business": 43,
            "creative": 42,
            "personal": 28,
            "scholar": 25,
            "government": 18,
            "social": 15,
            "community": 12,
            "entertainment": 8,
            "my_team": 35,
        },
        "by_level": {
            "1": 45,
            "2": 89,
            "3": 67,
            "4": 25,
        }
    }
    return ApiResponse(success=True, data=stats)

@router.get("/agents/{agent_id}", response_model=ApiResponse[Agent], tags=["Agents"])
async def get_agent(agent_id: str, current_user: User = Depends(get_current_user)):
    """Get agent by ID."""
    # TODO: Implement
    raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/agents/hire", response_model=ApiResponse[Agent], tags=["Agents"])
async def hire_agent(
    data: HireAgentRequest,
    current_user: User = Depends(get_current_user)
):
    """Hire an agent."""
    # Requires checkpoint
    checkpoint = await create_checkpoint(
        action_type="agent_hire",
        description=f"Hiring agent {data.agent_id}",
        requested_by=current_user.id,
        risk_level="low"
    )
    return ApiResponse(success=True, data=None, message="Checkpoint created")

@router.post("/agents/{agent_id}/dismiss", response_model=ApiResponse[None], tags=["Agents"])
async def dismiss_agent(agent_id: str, current_user: User = Depends(get_current_user)):
    """Dismiss a hired agent."""
    return ApiResponse(success=True, data=None, message="Agent dismissed")

@router.post("/agents/suggestions", response_model=ApiResponse[List[AgentSuggestion]], tags=["Agents"])
async def get_agent_suggestions(
    context: AgentSuggestionContext,
    current_user: User = Depends(get_current_user)
):
    """Get agent suggestions based on context."""
    suggestions = [
        AgentSuggestion(
            agent_id="agent-construction-1",
            reason="Expert en rénovation, pertinent pour votre projet cuisine",
            relevance_score=0.92
        ),
    ]
    return ApiResponse(success=True, data=suggestions)

# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINTS ENDPOINTS (GOVERNANCE)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/checkpoints", response_model=ApiResponse[List[Checkpoint]], tags=["Governance"])
async def list_checkpoints(
    status: Optional[str] = None,
    risk_level: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """List checkpoints."""
    checkpoints = [
        Checkpoint(
            id=str(uuid.uuid4()),
            action_type="external_api_call",
            description="Envoyer les documents au contracteur",
            requested_by="Nova",
            status="pending",
            risk_level="medium",
            context={"recipient": "contractor@example.com"},
            created_at=datetime.utcnow() - timedelta(hours=2),
        ),
    ]
    return ApiResponse(success=True, data=checkpoints)

@router.get("/checkpoints/pending", response_model=ApiResponse[List[Checkpoint]], tags=["Governance"])
async def get_pending_checkpoints(current_user: User = Depends(get_current_user)):
    """Get pending checkpoints requiring approval."""
    # TODO: Implement
    return ApiResponse(success=True, data=[])

@router.post("/checkpoints/resolve", response_model=ApiResponse[Checkpoint], tags=["Governance"])
async def resolve_checkpoint(
    data: ResolveCheckpointRequest,
    current_user: User = Depends(get_current_user)
):
    """Approve or reject a checkpoint."""
    return ApiResponse(success=True, data=Checkpoint(
        id=data.checkpoint_id,
        action_type="unknown",
        description="Resolved",
        requested_by="system",
        status=data.action,
        risk_level="low",
        created_at=datetime.utcnow(),
        resolved_at=datetime.utcnow(),
        resolved_by=current_user.id,
    ))

# ═══════════════════════════════════════════════════════════════════════════════
# NOVA ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/nova/chat", response_model=ApiResponse[NovaChatResponse], tags=["Nova"])
async def nova_chat(
    data: NovaChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Chat with Nova."""
    # TODO: Implement actual Nova integration
    response_message = NovaMessage(
        id=str(uuid.uuid4()),
        role="nova",
        content=f"J'ai bien reçu votre message: '{data.message}'. Comment puis-je vous aider davantage?",
        timestamp=datetime.utcnow(),
    )
    
    # Check if action requires checkpoint
    checkpoint = None
    trigger_words = ["envoyer", "supprimer", "modifier", "créer", "publier"]
    if any(word in data.message.lower() for word in trigger_words):
        checkpoint = Checkpoint(
            id=str(uuid.uuid4()),
            action_type="nova_action",
            description=f"Nova action requested: {data.message[:50]}...",
            requested_by="Nova",
            status="pending",
            risk_level="medium",
            created_at=datetime.utcnow(),
        )
    
    return ApiResponse(success=True, data=NovaChatResponse(
        message=response_message,
        suggestions=[],
        checkpoint=checkpoint,
    ))

@router.get("/nova/history", response_model=ApiResponse[List[NovaMessage]], tags=["Nova"])
async def get_nova_history(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get Nova chat history."""
    return ApiResponse(success=True, data=[])

@router.delete("/nova/history", response_model=ApiResponse[None], tags=["Nova"])
async def clear_nova_history(current_user: User = Depends(get_current_user)):
    """Clear Nova chat history."""
    return ApiResponse(success=True, data=None, message="History cleared")

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/governance/metrics", response_model=ApiResponse[GovernanceMetrics], tags=["Governance"])
async def get_governance_metrics(current_user: User = Depends(get_current_user)):
    """Get governance metrics."""
    return ApiResponse(success=True, data=GovernanceMetrics(
        checkpoints=CheckpointMetrics(
            total=153,
            pending=5,
            approved=142,
            rejected=6,
            approval_rate=95.9,
            avg_response_time_hours=2.4,
        ),
        agents=AgentMetrics(
            total_hired=8,
            active=5,
            actions_today=47,
            blocked_actions=2,
        ),
        decisions=DecisionMetrics(
            total_pending=15,
            blink_count=1,
            avg_aging_days=3.2,
        ),
        data=DataMetrics(
            total_threads=45,
            total_events=234,
            data_points_protected=8432,
        ),
    ))

@router.get("/governance/signals", response_model=ApiResponse[List[GovernanceSignal]], tags=["Governance"])
async def get_governance_signals(
    resolved: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """Get governance signals."""
    signals = [
        GovernanceSignal(
            id=str(uuid.uuid4()),
            level="warning",
            title="Agent rate limit atteint",
            description="L'agent Construction-1 a atteint 90% de son quota quotidien",
            source="Agent Monitor",
            timestamp=datetime.utcnow() - timedelta(hours=1),
            resolved=False,
        ),
    ]
    return ApiResponse(success=True, data=signals)

@router.post("/governance/signals/{signal_id}/resolve", response_model=ApiResponse[GovernanceSignal], tags=["Governance"])
async def resolve_signal(signal_id: str, current_user: User = Depends(get_current_user)):
    """Resolve a governance signal."""
    return ApiResponse(success=True, data=None, message="Signal resolved")

@router.get("/governance/audit", response_model=ApiResponse[List[AuditEvent]], tags=["Governance"])
async def get_audit_log(
    type: Optional[str] = None,
    actor: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get audit log."""
    events = [
        AuditEvent(
            id=str(uuid.uuid4()),
            type="checkpoint",
            action="Checkpoint approved",
            actor=current_user.username,
            target="agent-construction-1",
            sphere_id="personal",
            details={"risk_level": "medium"},
            timestamp=datetime.utcnow() - timedelta(hours=1),
        ),
    ]
    return ApiResponse(success=True, data=events)

# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICATIONS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/notifications", response_model=ApiResponse[List[Notification]], tags=["Notifications"])
async def list_notifications(
    unread_only: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """List notifications."""
    notifications = [
        Notification(
            id=str(uuid.uuid4()),
            type="checkpoint",
            title="Checkpoint en attente",
            message="Une action nécessite votre approbation",
            read=False,
            action_url="/governance",
            created_at=datetime.utcnow() - timedelta(minutes=30),
        ),
    ]
    return ApiResponse(success=True, data=notifications)

@router.post("/notifications/{notification_id}/read", response_model=ApiResponse[Notification], tags=["Notifications"])
async def mark_notification_read(notification_id: str, current_user: User = Depends(get_current_user)):
    """Mark notification as read."""
    return ApiResponse(success=True, data=None, message="Marked as read")

@router.post("/notifications/read-all", response_model=ApiResponse[None], tags=["Notifications"])
async def mark_all_notifications_read(current_user: User = Depends(get_current_user)):
    """Mark all notifications as read."""
    return ApiResponse(success=True, data=None, message="All marked as read")

@router.get("/notifications/unread-count", response_model=ApiResponse[dict], tags=["Notifications"])
async def get_unread_count(current_user: User = Depends(get_current_user)):
    """Get unread notification count."""
    return ApiResponse(success=True, data={"count": 3})

# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/search", response_model=ApiResponse[SearchResults], tags=["Search"])
async def global_search(
    q: str = Query(..., min_length=2),
    types: Optional[List[str]] = Query(None),
    sphere_id: Optional[str] = None,
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """Global search across threads, decisions, agents, files."""
    return ApiResponse(success=True, data=SearchResults(
        threads=[],
        decisions=[],
        agents=[],
        files=[],
    ))

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/dashboard/stats", response_model=ApiResponse[DashboardStats], tags=["Dashboard"])
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    """Get dashboard statistics."""
    return ApiResponse(success=True, data=DashboardStats(
        decisions_pending=15,
        threads_active=23,
        agents_hired=8,
        checkpoints_pending=5,
        governance_score=95,
    ))

@router.get("/dashboard/activity", response_model=ApiResponse[List[AuditEvent]], tags=["Dashboard"])
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """Get recent activity."""
    return ApiResponse(success=True, data=[])

# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/threads/{thread_id}/events", response_model=ApiResponse[List[dict]], tags=["Threads"])
async def get_thread_events(
    thread_id: str,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
):
    """Get events for a specific thread (append-only event log)."""
    events = [
        {
            "id": f"evt-{thread_id}-001",
            "thread_id": thread_id,
            "type": "thread.created",
            "data": {"founding_intent": "Q1 Planning"},
            "created_by": "user-123",
            "created_at": "2026-01-08T10:00:00Z",
        },
        {
            "id": f"evt-{thread_id}-002",
            "thread_id": thread_id,
            "type": "intent.declared",
            "data": {"intent": "Define quarterly objectives"},
            "created_by": "user-123",
            "created_at": "2026-01-08T10:05:00Z",
        },
        {
            "id": f"evt-{thread_id}-003",
            "thread_id": thread_id,
            "type": "decision.recorded",
            "data": {"decision": "Allocate 30% budget to marketing", "rationale": "Growth focus"},
            "created_by": "user-123",
            "created_at": "2026-01-08T10:15:00Z",
        },
        {
            "id": f"evt-{thread_id}-004",
            "thread_id": thread_id,
            "type": "action.created",
            "data": {"action": "Schedule team meeting", "due_date": "2026-01-10"},
            "created_by": "user-123",
            "created_at": "2026-01-08T10:20:00Z",
        },
        {
            "id": f"evt-{thread_id}-005",
            "thread_id": thread_id,
            "type": "note.added",
            "data": {"content": "Consider hiring 2 more engineers"},
            "created_by": "user-123",
            "created_at": "2026-01-08T10:30:00Z",
        },
    ]
    return ApiResponse(success=True, data=events[offset:offset+limit])

@router.post("/threads/{thread_id}/events", response_model=ApiResponse[dict], tags=["Threads"])
async def add_thread_event(
    thread_id: str,
    event_type: str = Body(...),
    data: dict = Body(...),
    current_user: User = Depends(get_current_user),
):
    """Add a new event to a thread (append-only)."""
    event = {
        "id": f"evt-{thread_id}-{uuid.uuid4().hex[:8]}",
        "thread_id": thread_id,
        "type": event_type,
        "data": data,
        "created_by": current_user.id,
        "created_at": datetime.utcnow().isoformat(),
    }
    return ApiResponse(success=True, data=event, message="Event added to thread")

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD EXTENDED ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/dashboard/activity", response_model=ApiResponse[List[dict]], tags=["Dashboard"])
async def get_recent_activity(
    limit: int = Query(default=10, le=50),
):
    """Get recent activity across all spheres."""
    activities = [
        {
            "id": "act-001",
            "type": "thread_created",
            "title": "New Thread: Q1 Planning",
            "sphere": "business",
            "timestamp": "2026-01-08T10:00:00Z",
        },
        {
            "id": "act-002",
            "type": "decision_made",
            "title": "Decision: Marketing Budget Approved",
            "sphere": "business",
            "timestamp": "2026-01-08T09:30:00Z",
        },
        {
            "id": "act-003",
            "type": "agent_hired",
            "title": "Hired Agent: Research Assistant",
            "sphere": "scholar",
            "timestamp": "2026-01-08T09:00:00Z",
        },
        {
            "id": "act-004",
            "type": "checkpoint_approved",
            "title": "Checkpoint Approved: Data Export",
            "sphere": "personal",
            "timestamp": "2026-01-08T08:30:00Z",
        },
        {
            "id": "act-005",
            "type": "note_added",
            "title": "Note added to Project Alpha",
            "sphere": "creative",
            "timestamp": "2026-01-08T08:00:00Z",
        },
    ]
    return ApiResponse(success=True, data=activities[:limit])

@router.get("/dashboard/quick-actions", response_model=ApiResponse[List[dict]], tags=["Dashboard"])
async def get_quick_actions():
    """Get available quick actions for dashboard."""
    actions = [
        {
            "id": "qa-001",
            "label": "New Thread",
            "icon": "plus",
            "action": "create_thread",
            "shortcut": "Ctrl+N",
        },
        {
            "id": "qa-002",
            "label": "Ask Nova",
            "icon": "message-circle",
            "action": "open_nova",
            "shortcut": "Ctrl+K",
        },
        {
            "id": "qa-003",
            "label": "Quick Note",
            "icon": "edit",
            "action": "create_note",
            "shortcut": "Ctrl+Shift+N",
        },
        {
            "id": "qa-004",
            "label": "Search",
            "icon": "search",
            "action": "open_search",
            "shortcut": "Ctrl+/",
        },
        {
            "id": "qa-005",
            "label": "View Checkpoints",
            "icon": "shield",
            "action": "view_checkpoints",
            "shortcut": "Ctrl+G",
        },
    ]
    return ApiResponse(success=True, data=actions)

# ═══════════════════════════════════════════════════════════════════════════════
# DECISIONS EXTENDED ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/decisions/thread/{thread_id}", response_model=ApiResponse[List[Decision]], tags=["Decisions"])
async def get_thread_decisions(thread_id: str):
    """Get all decisions for a specific thread."""
    decisions = [
        Decision(
            id="dec-001",
            thread_id=thread_id,
            title="Budget Allocation",
            description="Approve 30% budget for Q1 marketing",
            status="approved",
            impact="high",
            created_by="user-123",
            created_at=datetime.utcnow() - timedelta(hours=2),
            decided_at=datetime.utcnow() - timedelta(hours=1),
        ),
        Decision(
            id="dec-002",
            thread_id=thread_id,
            title="Team Expansion",
            description="Hire 2 additional engineers",
            status="pending",
            impact="high",
            created_by="user-123",
            created_at=datetime.utcnow() - timedelta(hours=1),
        ),
    ]
    return ApiResponse(success=True, data=decisions)
