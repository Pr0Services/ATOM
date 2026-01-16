"""
CHE·NU™ V75 Backend - Agents Router

RÈGLE: L'IA ILLUMINE, ne décide jamais
- Nova est L0 (système), toujours disponible
- Agents L1-L3 sont "hired" par l'utilisateur
- Aucun agent autonome

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

from config import get_db
from schemas.base import BaseResponse, PaginatedResponse, PaginationMeta, AgentLevel, AgentStatus
from routers.auth import require_auth
from middleware.governance import check_governance

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class AgentCapability(BaseModel):
    """Agent capability."""
    id: str
    name: str
    description: str
    category: str


class Agent(BaseModel):
    """Agent entity."""
    id: str
    name: str
    description: str
    level: AgentLevel
    status: AgentStatus
    sphere_ids: List[str] = []
    capabilities: List[AgentCapability] = []
    avatar_url: Optional[str] = None
    hired_at: Optional[datetime] = None
    last_active: Optional[datetime] = None
    tasks_completed: int = 0
    created_at: datetime


class AgentTask(BaseModel):
    """Task assigned to agent."""
    id: str
    agent_id: str
    thread_id: Optional[str] = None
    description: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    progress: int = 0
    result: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class HireAgentRequest(BaseModel):
    """Request to hire an agent."""
    agent_id: str
    sphere_ids: List[str] = []


class AssignTaskRequest(BaseModel):
    """Request to assign task to agent."""
    description: str
    thread_id: Optional[str] = None
    priority: str = "normal"  # 'low', 'normal', 'high'


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("", response_model=PaginatedResponse[Agent])
async def list_agents(
    user: dict = Depends(require_auth),
    level: Optional[AgentLevel] = None,
    status: Optional[AgentStatus] = None,
    sphere_id: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all available agents."""
    now = datetime.utcnow()
    
    agents = [
        Agent(
            id="nova",
            name="Nova",
            description="Système d'intelligence centrale CHE·NU - L0, toujours disponible",
            level=AgentLevel.L0,
            status=AgentStatus.AVAILABLE,
            sphere_ids=["personal", "business", "team"],
            capabilities=[
                AgentCapability(id="c1", name="Analysis", description="Data analysis", category="intelligence"),
                AgentCapability(id="c2", name="Research", description="Web research", category="intelligence"),
            ],
            created_at=now,
        ),
        Agent(
            id="agent-research",
            name="Research Assistant",
            description="Specialized research and analysis agent",
            level=AgentLevel.L2,
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability(id="c3", name="Deep Research", description="In-depth research", category="research"),
            ],
            created_at=now,
        ),
        Agent(
            id="agent-writer",
            name="Writing Assistant",
            description="Content creation and editing",
            level=AgentLevel.L2,
            status=AgentStatus.AVAILABLE,
            capabilities=[
                AgentCapability(id="c4", name="Writing", description="Content writing", category="creative"),
            ],
            created_at=now,
        ),
    ]
    
    # Filter by level
    if level:
        agents = [a for a in agents if a.level == level]
    
    # Filter by status
    if status:
        agents = [a for a in agents if a.status == status]
    
    return PaginatedResponse(
        success=True,
        data=agents,
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=len(agents),
            total_pages=1,
        ),
    )


@router.get("/hired", response_model=BaseResponse[List[Agent]])
async def get_hired_agents(
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get user's hired agents."""
    now = datetime.utcnow()
    
    agents = [
        Agent(
            id="agent-research",
            name="Research Assistant",
            description="Specialized research agent",
            level=AgentLevel.L2,
            status=AgentStatus.HIRED,
            hired_at=now,
            last_active=now,
            tasks_completed=42,
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=agents)


@router.get("/available", response_model=BaseResponse[List[Agent]])
async def get_available_agents(
    user: dict = Depends(require_auth),
    sphere_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get agents available for hire."""
    now = datetime.utcnow()
    
    agents = [
        Agent(
            id="agent-writer",
            name="Writing Assistant",
            description="Content creation",
            level=AgentLevel.L2,
            status=AgentStatus.AVAILABLE,
            created_at=now,
        ),
        Agent(
            id="agent-analyst",
            name="Data Analyst",
            description="Data analysis and visualization",
            level=AgentLevel.L2,
            status=AgentStatus.AVAILABLE,
            created_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=agents)


@router.get("/{agent_id}", response_model=BaseResponse[Agent])
async def get_agent(
    agent_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get agent details."""
    now = datetime.utcnow()
    
    agent = Agent(
        id=agent_id,
        name="Research Assistant",
        description="Specialized research and analysis agent",
        level=AgentLevel.L2,
        status=AgentStatus.HIRED,
        capabilities=[
            AgentCapability(id="c1", name="Research", description="Deep research", category="research"),
        ],
        hired_at=now,
        tasks_completed=42,
        created_at=now,
    )
    
    return BaseResponse(success=True, data=agent)


@router.get("/{agent_id}/capabilities", response_model=BaseResponse[List[AgentCapability]])
async def get_agent_capabilities(
    agent_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get agent capabilities."""
    capabilities = [
        AgentCapability(id="c1", name="Research", description="Deep research", category="research"),
        AgentCapability(id="c2", name="Analysis", description="Data analysis", category="intelligence"),
        AgentCapability(id="c3", name="Summarization", description="Content summarization", category="writing"),
    ]
    
    return BaseResponse(success=True, data=capabilities)


@router.post("/hire", response_model=BaseResponse[Agent])
async def hire_agent(
    request: HireAgentRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Hire an agent (requires governance check).
    
    RÈGLE: Hiring agents is a governance-controlled action.
    """
    # Governance check
    gov_result = await check_governance(
        operation="agent.hire",
        user_id=user["id"],
        resource_id=request.agent_id,
    )
    
    if not gov_result["allow"]:
        raise HTTPException(
            status_code=403,
            detail=f"Governance denied: {gov_result['reason']}",
        )
    
    now = datetime.utcnow()
    
    agent = Agent(
        id=request.agent_id,
        name="Research Assistant",
        description="Now hired",
        level=AgentLevel.L2,
        status=AgentStatus.HIRED,
        sphere_ids=request.sphere_ids,
        hired_at=now,
        created_at=now,
    )
    
    return BaseResponse(success=True, data=agent)


@router.post("/{agent_id}/fire")
async def fire_agent(
    agent_id: str,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Fire (unhire) an agent."""
    # Nova (L0) cannot be fired
    if agent_id == "nova":
        raise HTTPException(
            status_code=400,
            detail="Nova (L0) is a system agent and cannot be fired",
        )
    
    return BaseResponse(
        success=True,
        data={"id": agent_id, "status": "available"},
    )


@router.post("/{agent_id}/assign", response_model=BaseResponse[AgentTask])
async def assign_task(
    agent_id: str,
    request: AssignTaskRequest,
    user: dict = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Assign a task to an agent.
    
    RÈGLE: L'agent exécute, l'humain valide le résultat.
    """
    now = datetime.utcnow()
    
    task = AgentTask(
        id=str(uuid.uuid4()),
        agent_id=agent_id,
        thread_id=request.thread_id,
        description=request.description,
        status="pending",
        progress=0,
        created_at=now,
    )
    
    return BaseResponse(success=True, data=task)


@router.get("/{agent_id}/tasks", response_model=BaseResponse[List[AgentTask]])
async def get_agent_tasks(
    agent_id: str,
    user: dict = Depends(require_auth),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get tasks assigned to an agent."""
    now = datetime.utcnow()
    
    tasks = [
        AgentTask(
            id="task-1",
            agent_id=agent_id,
            description="Research market trends",
            status="completed",
            progress=100,
            result="Analysis complete",
            created_at=now,
            completed_at=now,
        ),
    ]
    
    return BaseResponse(success=True, data=tasks)
