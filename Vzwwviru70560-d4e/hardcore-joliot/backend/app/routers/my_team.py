"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V78 — My Team Sphere Router
═══════════════════════════════════════════════════════════════════════════════

Endpoints: 16
Target Profiles: All (Team Collaboration)

Features:
- Team member management
- Role assignments
- Resource allocation
- Agent hiring (with checkpoints)
- Task delegation
- Team activity feed
- Availability tracking

R&D RULES ENFORCED:
- Rule #1: Human Sovereignty → Checkpoints on hiring/firing
- Rule #4: My Team Restrictions → NO AI orchestrating AI
- Rule #5: NO RANKING → Alphabetical/chronological only
- Rule #6: Traceability → id, created_by, created_at on all entities

⚠️ CRITICAL R&D RULE #4:
   Human coordinates multi-agent work.
   NO autonomous agent-to-agent orchestration.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, time
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# R&D RULE #4 ENFORCEMENT
# ═══════════════════════════════════════════════════════════════════════════════

RD_RULE_4_ENFORCED = True
ORCHESTRATION_POLICY = "human_only"  # NEVER "agent_to_agent"

def validate_no_agent_orchestration(action: str, initiator_type: str) -> bool:
    """
    R&D Rule #4: No AI orchestrating AI.
    
    Only humans can:
    - Hire agents
    - Fire agents
    - Assign tasks to agents
    - Coordinate multi-agent work
    """
    if initiator_type == "agent":
        raise HTTPException(
            status_code=403,
            detail={
                "error": "rd_rule_4_violation",
                "message": "AI cannot orchestrate other AI. Human coordination required.",
                "rule": "R&D Rule #4: My Team Restrictions",
                "action_attempted": action
            }
        )
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class MemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"
    AGENT = "agent"  # AI Agent


class MemberStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"


class AgentType(str, Enum):
    PERSONAL = "personal"
    BUSINESS = "business"
    CREATIVE = "creative"
    SCHOLAR = "scholar"
    CUSTOM = "custom"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class TeamMemberCreate(BaseModel):
    """Add a team member."""
    user_id: Optional[UUID] = None  # None for agents
    name: str
    email: Optional[str] = None
    role: MemberRole
    agent_type: Optional[AgentType] = None  # If role == AGENT
    permissions: List[str] = Field(default_factory=list)
    sphere_access: List[str] = Field(default_factory=list)


class TeamMemberResponse(BaseModel):
    """Team member with metadata."""
    id: UUID
    user_id: Optional[UUID]
    name: str
    email: Optional[str]
    role: MemberRole
    status: MemberStatus
    is_agent: bool
    agent_type: Optional[AgentType]
    permissions: List[str]
    sphere_access: List[str]
    # Activity
    last_active: Optional[datetime]
    tasks_assigned: int
    tasks_completed: int
    # Traceability
    added_by: UUID
    added_at: datetime
    updated_at: datetime


class AgentHireRequest(BaseModel):
    """Request to hire an AI agent."""
    agent_type: AgentType
    name: str
    description: Optional[str] = None
    sphere_access: List[str] = Field(default_factory=list)
    token_budget: int = Field(default=10000, ge=100, le=1000000)
    scope_restrictions: List[str] = Field(default_factory=list)


class TaskCreate(BaseModel):
    """Create a task."""
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[UUID] = None
    due_date: Optional[date] = None
    tags: List[str] = Field(default_factory=list)
    sphere: Optional[str] = None


class TaskResponse(BaseModel):
    """Task with metadata."""
    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assigned_to: Optional[UUID]
    assignee_name: Optional[str]
    due_date: Optional[date]
    tags: List[str]
    sphere: Optional[str]
    # Progress
    subtasks_total: int
    subtasks_completed: int
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]


class AvailabilitySlot(BaseModel):
    """Team member availability."""
    member_id: UUID
    member_name: str
    day_of_week: int  # 0=Monday, 6=Sunday
    start_time: time
    end_time: time
    is_available: bool


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA STORE
# ═══════════════════════════════════════════════════════════════════════════════

_team_members: Dict[UUID, dict] = {}
_tasks: Dict[UUID, dict] = {}
_activity_feed: List[dict] = []
_availability: Dict[UUID, List[dict]] = {}
_pending_checkpoints: Dict[UUID, dict] = {}


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_mock_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def create_checkpoint(action: str, resource_type: str, resource_id: UUID, reason: str) -> dict:
    """Create checkpoint for human approval (R&D Rule #1)."""
    checkpoint = {
        "checkpoint_id": uuid4(),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "reason": reason,
        "options": ["approve", "reject"],
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    _pending_checkpoints[checkpoint["checkpoint_id"]] = checkpoint
    return checkpoint


def log_activity(action: str, actor_id: UUID, actor_name: str, details: Dict):
    """Log team activity."""
    event = {
        "id": uuid4(),
        "action": action,
        "actor_id": actor_id,
        "actor_name": actor_name,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    _activity_feed.insert(0, event)
    # Keep only last 1000 events
    if len(_activity_feed) > 1000:
        _activity_feed.pop()
    return event


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", tags=["Health"])
async def team_health():
    """Health check for My Team sphere."""
    return {
        "status": "healthy",
        "sphere": "my_team",
        "version": "78.0.0",
        "endpoints": 16,
        "features": [
            "team_management",
            "agent_hiring",
            "task_delegation",
            "availability_tracking",
            "activity_feed"
        ],
        "rd_rules": {
            "rule_1": "Human Sovereignty (checkpoints on hire/fire)",
            "rule_4": "NO AI ORCHESTRATING AI — Human coordination only",
            "rule_5": "Alphabetical/chronological ordering",
            "rule_6": "Full Traceability"
        },
        "orchestration_policy": ORCHESTRATION_POLICY,
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TEAM MEMBER ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/members", response_model=List[TeamMemberResponse], tags=["Members"])
async def list_team_members(
    role: Optional[MemberRole] = None,
    status: Optional[MemberStatus] = None,
    include_agents: bool = Query(True)
):
    """
    List team members.
    
    ⚠️ R&D Rule #5: Alphabetical order by name.
    """
    members = list(_team_members.values())
    
    if role:
        members = [m for m in members if m["role"] == role]
    if status:
        members = [m for m in members if m["status"] == status]
    if not include_agents:
        members = [m for m in members if not m["is_agent"]]
    
    # Alphabetical order (R&D Rule #5)
    members.sort(key=lambda x: x["name"].lower())
    
    return members


@router.post("/members", response_model=TeamMemberResponse, status_code=201, tags=["Members"])
async def add_team_member(data: TeamMemberCreate):
    """Add a human team member."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    if data.role == MemberRole.AGENT:
        raise HTTPException(
            status_code=400,
            detail="Use POST /agents/hire to add AI agents"
        )
    
    member = {
        "id": uuid4(),
        **data.dict(),
        "status": MemberStatus.PENDING,
        "is_agent": False,
        "last_active": None,
        "tasks_assigned": 0,
        "tasks_completed": 0,
        "added_by": user_id,
        "added_at": now,
        "updated_at": now
    }
    
    _team_members[member["id"]] = member
    
    log_activity(
        action="member_added",
        actor_id=user_id,
        actor_name="You",
        details={"member_name": data.name, "role": data.role.value}
    )
    
    return member


@router.get("/members/{member_id}", response_model=TeamMemberResponse, tags=["Members"])
async def get_team_member(member_id: UUID):
    """Get team member by ID."""
    if member_id not in _team_members:
        raise HTTPException(status_code=404, detail="Team member not found")
    return _team_members[member_id]


@router.delete("/members/{member_id}", tags=["Members"])
async def remove_team_member(member_id: UUID):
    """
    Remove a team member (requires checkpoint).
    
    ⚠️ R&D Rule #1: Removal requires human approval.
    """
    if member_id not in _team_members:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    member = _team_members[member_id]
    
    checkpoint = create_checkpoint(
        action="remove_member",
        resource_type="team_member",
        resource_id=member_id,
        reason=f"Removing {member['name']} requires human approval"
    )
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint": checkpoint,
            "message": "Human approval required to remove team member"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT HIRING ENDPOINTS (R&D Rule #4 Critical)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/agents/hire", tags=["Agents"])
async def hire_agent(
    data: AgentHireRequest,
    initiator_type: str = Query("human", regex="^(human|agent)$")
):
    """
    Hire an AI agent.
    
    ⚠️ R&D Rule #1: Agent hiring requires human approval (checkpoint).
    ⚠️ R&D Rule #4: ONLY humans can hire agents. Agents CANNOT hire other agents.
    """
    # R&D Rule #4: Validate no agent orchestration
    validate_no_agent_orchestration("hire_agent", initiator_type)
    
    user_id = get_mock_user_id()
    agent_id = uuid4()
    
    # Create checkpoint for human approval
    checkpoint = create_checkpoint(
        action="hire_agent",
        resource_type="agent",
        resource_id=agent_id,
        reason=f"Hiring AI agent '{data.name}' ({data.agent_type.value}) requires human approval"
    )
    
    # Store pending agent data in checkpoint
    checkpoint["agent_data"] = data.dict()
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint": checkpoint,
            "message": "Human approval required to hire AI agent",
            "rd_rule_4": "Only humans can hire agents"
        }
    )


@router.post("/agents/{agent_id}/fire", tags=["Agents"])
async def fire_agent(
    agent_id: UUID,
    initiator_type: str = Query("human", regex="^(human|agent)$")
):
    """
    Fire (remove) an AI agent.
    
    ⚠️ R&D Rule #1: Agent firing requires human approval.
    ⚠️ R&D Rule #4: ONLY humans can fire agents.
    """
    # R&D Rule #4: Validate no agent orchestration
    validate_no_agent_orchestration("fire_agent", initiator_type)
    
    if agent_id not in _team_members:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    member = _team_members[agent_id]
    
    if not member["is_agent"]:
        raise HTTPException(status_code=400, detail="This is not an AI agent")
    
    checkpoint = create_checkpoint(
        action="fire_agent",
        resource_type="agent",
        resource_id=agent_id,
        reason=f"Firing AI agent '{member['name']}' requires human approval"
    )
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint": checkpoint,
            "message": "Human approval required to fire AI agent"
        }
    )


@router.get("/agents", response_model=List[TeamMemberResponse], tags=["Agents"])
async def list_agents():
    """
    List all AI agents in the team.
    
    ⚠️ R&D Rule #5: Alphabetical order.
    """
    agents = [m for m in _team_members.values() if m["is_agent"]]
    
    # Alphabetical (R&D Rule #5)
    agents.sort(key=lambda x: x["name"].lower())
    
    return agents


# ═══════════════════════════════════════════════════════════════════════════════
# TASK ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assigned_to: Optional[UUID] = None,
    limit: int = Query(50, ge=1, le=200)
):
    """
    List tasks.
    
    ⚠️ R&D Rule #5: Chronological order (by created_at).
    """
    tasks = list(_tasks.values())
    
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if assigned_to:
        tasks = [t for t in tasks if t["assigned_to"] == assigned_to]
    
    # Chronological order (R&D Rule #5)
    tasks.sort(key=lambda x: x["created_at"], reverse=True)
    
    return tasks[:limit]


@router.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
async def create_task(
    data: TaskCreate,
    initiator_type: str = Query("human", regex="^(human|agent)$")
):
    """
    Create a task.
    
    ⚠️ R&D Rule #4: If assigning to an agent, only humans can do this.
    """
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    # If assigning to someone, check if it's an agent
    assignee_name = None
    if data.assigned_to:
        if data.assigned_to in _team_members:
            member = _team_members[data.assigned_to]
            assignee_name = member["name"]
            
            # R&D Rule #4: Only humans can assign to agents
            if member["is_agent"]:
                validate_no_agent_orchestration("assign_to_agent", initiator_type)
    
    task = {
        "id": uuid4(),
        **data.dict(),
        "status": TaskStatus.TODO,
        "assignee_name": assignee_name,
        "subtasks_total": 0,
        "subtasks_completed": 0,
        "created_by": user_id,
        "created_at": now,
        "updated_at": now,
        "completed_at": None
    }
    
    _tasks[task["id"]] = task
    
    # Update member task count
    if data.assigned_to and data.assigned_to in _team_members:
        _team_members[data.assigned_to]["tasks_assigned"] += 1
    
    log_activity(
        action="task_created",
        actor_id=user_id,
        actor_name="You",
        details={"task_title": data.title, "assigned_to": assignee_name}
    )
    
    return task


@router.put("/tasks/{task_id}/status", tags=["Tasks"])
async def update_task_status(
    task_id: UUID,
    status: TaskStatus
):
    """Update task status."""
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = _tasks[task_id]
    old_status = task["status"]
    task["status"] = status
    task["updated_at"] = datetime.utcnow()
    
    if status == TaskStatus.COMPLETED:
        task["completed_at"] = datetime.utcnow()
        if task["assigned_to"] and task["assigned_to"] in _team_members:
            _team_members[task["assigned_to"]]["tasks_completed"] += 1
    
    log_activity(
        action="task_status_changed",
        actor_id=get_mock_user_id(),
        actor_name="You",
        details={
            "task_title": task["title"],
            "from": old_status.value,
            "to": status.value
        }
    )
    
    return {"message": f"Task status updated to {status.value}"}


# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY FEED
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/activity", tags=["Activity"])
async def get_activity_feed(
    limit: int = Query(50, ge=1, le=200)
):
    """
    Get team activity feed.
    
    ⚠️ R&D Rule #5: Chronological order (newest first).
    """
    return {
        "activities": _activity_feed[:limit],
        "total": len(_activity_feed)
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AVAILABILITY
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/availability", tags=["Availability"])
async def get_team_availability(
    day_of_week: Optional[int] = Query(None, ge=0, le=6)
):
    """Get team availability."""
    all_slots = []
    
    for member_id, slots in _availability.items():
        if member_id in _team_members:
            member = _team_members[member_id]
            for slot in slots:
                if day_of_week is None or slot["day_of_week"] == day_of_week:
                    all_slots.append({
                        **slot,
                        "member_id": member_id,
                        "member_name": member["name"]
                    })
    
    return {"slots": all_slots}


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/checkpoints/{checkpoint_id}/approve", tags=["Checkpoints"])
async def approve_checkpoint(checkpoint_id: UUID):
    """Approve a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    action = checkpoint["action"]
    resource_id = checkpoint["resource_id"]
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    if action == "hire_agent":
        # Create the agent
        agent_data = checkpoint.get("agent_data", {})
        agent = {
            "id": resource_id,
            "user_id": None,
            "name": agent_data.get("name", "AI Agent"),
            "email": None,
            "role": MemberRole.AGENT,
            "status": MemberStatus.ACTIVE,
            "is_agent": True,
            "agent_type": agent_data.get("agent_type", AgentType.CUSTOM),
            "permissions": [],
            "sphere_access": agent_data.get("sphere_access", []),
            "last_active": None,
            "tasks_assigned": 0,
            "tasks_completed": 0,
            "added_by": user_id,
            "added_at": now,
            "updated_at": now
        }
        _team_members[resource_id] = agent
        
        log_activity(
            action="agent_hired",
            actor_id=user_id,
            actor_name="You",
            details={"agent_name": agent["name"], "agent_type": str(agent["agent_type"])}
        )
    
    elif action == "fire_agent":
        if resource_id in _team_members:
            agent_name = _team_members[resource_id]["name"]
            del _team_members[resource_id]
            
            log_activity(
                action="agent_fired",
                actor_id=user_id,
                actor_name="You",
                details={"agent_name": agent_name}
            )
    
    elif action == "remove_member":
        if resource_id in _team_members:
            member_name = _team_members[resource_id]["name"]
            del _team_members[resource_id]
            
            log_activity(
                action="member_removed",
                actor_id=user_id,
                actor_name="You",
                details={"member_name": member_name}
            )
    
    checkpoint["status"] = "approved"
    checkpoint["resolved_at"] = now
    
    return {"message": "Checkpoint approved", "action": action, "executed": True}


@router.post("/checkpoints/{checkpoint_id}/reject", tags=["Checkpoints"])
async def reject_checkpoint(checkpoint_id: UUID):
    """Reject a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    checkpoint["status"] = "rejected"
    checkpoint["resolved_at"] = datetime.utcnow()
    
    return {"message": "Checkpoint rejected", "action": checkpoint["action"], "executed": False}
