"""
============================================================================
CHE·NU™ V69 — AGENT FRAMEWORK MODELS
============================================================================
Version: 1.0.0
Purpose: Core models for agent hierarchy and governance
Principle: GOUVERNANCE > EXÉCUTION — Agents NEVER decide, humans do
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib


# ============================================================================
# ENUMS
# ============================================================================

class AgentLevel(str, Enum):
    """
    Agent hierarchy levels.
    
    L0: System/Infrastructure - Core platform operations
    L1: Orchestrator - Coordinates L2 agents
    L2: Specialist - Domain-specific tasks
    L3: Assistant - User-facing interactions
    """
    L0 = "L0"  # System/Infrastructure
    L1 = "L1"  # Orchestrator
    L2 = "L2"  # Specialist
    L3 = "L3"  # Assistant


class AgentStatus(str, Enum):
    """Agent lifecycle status"""
    INITIALIZING = "initializing"
    IDLE = "idle"
    ACTIVE = "active"
    WAITING_APPROVAL = "waiting_approval"
    PAUSED = "paused"
    TERMINATED = "terminated"
    ERROR = "error"


class ActionType(str, Enum):
    """Types of agent actions"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    COMMUNICATE = "communicate"
    DELEGATE = "delegate"
    ESCALATE = "escalate"
    CHECKPOINT = "checkpoint"


class ActionStatus(str, Enum):
    """Action execution status"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CheckpointType(str, Enum):
    """Types of governance checkpoints"""
    HITL = "hitl"              # Human-In-The-Loop required
    OPA = "opa"                # OPA policy check
    THRESHOLD = "threshold"    # Value threshold check
    ESCALATION = "escalation"  # Escalation to higher level
    APPROVAL = "approval"      # Explicit approval required


class CheckpointStatus(str, Enum):
    """Checkpoint resolution status"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"


# ============================================================================
# AGENT CAPABILITY
# ============================================================================

class AgentCapability(BaseModel):
    """Defines what an agent can do"""
    
    capability_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(default="")
    
    # Permissions
    allowed_actions: Set[ActionType] = Field(default_factory=set)
    allowed_spheres: Set[str] = Field(default_factory=set)
    allowed_slots: Set[str] = Field(default_factory=set)
    
    # Limits
    max_impact: float = Field(default=1.0)
    requires_approval_above: float = Field(default=0.5)
    
    # Governance
    requires_hitl: bool = Field(default=False)
    auto_checkpoint: bool = Field(default=True)


# ============================================================================
# AGENT ACTION
# ============================================================================

class AgentAction(BaseModel):
    """
    Represents a single agent action.
    
    Every action is:
    - Logged for audit
    - Checked against governance
    - Signed if completed
    """
    
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = Field(...)
    
    # Action details
    action_type: ActionType = Field(...)
    target: str = Field(...)  # Target resource/slot/agent
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # Context
    sphere: Optional[str] = Field(default=None)
    simulation_id: Optional[str] = Field(default=None)
    parent_action_id: Optional[str] = Field(default=None)
    
    # Status
    status: ActionStatus = Field(default=ActionStatus.PENDING)
    
    # Impact assessment
    estimated_impact: float = Field(default=0.0)
    actual_impact: Optional[float] = Field(default=None)
    
    # Governance
    requires_checkpoint: bool = Field(default=False)
    checkpoint_id: Optional[str] = Field(default=None)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Result
    result: Optional[Dict[str, Any]] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    
    # Audit
    signature: Optional[str] = Field(default=None)
    
    @computed_field
    @property
    def duration_ms(self) -> Optional[float]:
        """Execution duration in milliseconds"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds() * 1000
        return None


# ============================================================================
# CHECKPOINT
# ============================================================================

class Checkpoint(BaseModel):
    """
    Governance checkpoint for agent actions.
    
    Checkpoints enforce GOUVERNANCE > EXÉCUTION:
    - Pause execution at critical points
    - Require human approval for sensitive actions
    - Log all decisions for audit
    """
    
    checkpoint_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Context
    agent_id: str = Field(...)
    action_id: str = Field(...)
    
    # Type and reason
    checkpoint_type: CheckpointType = Field(...)
    reason: str = Field(...)
    
    # Status
    status: CheckpointStatus = Field(default=CheckpointStatus.PENDING)
    
    # Details
    details: Dict[str, Any] = Field(default_factory=dict)
    
    # Resolution
    resolved_by: Optional[str] = Field(default=None)  # User ID or "system"
    resolution_notes: Optional[str] = Field(default=None)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = Field(default=None)
    timeout_at: Optional[datetime] = Field(default=None)
    
    # Escalation
    escalated_to: Optional[str] = Field(default=None)
    escalation_level: int = Field(default=0)
    
    @computed_field
    @property
    def is_resolved(self) -> bool:
        return self.status in [
            CheckpointStatus.APPROVED,
            CheckpointStatus.DENIED,
            CheckpointStatus.ESCALATED,
        ]
    
    @computed_field
    @property
    def is_approved(self) -> bool:
        return self.status == CheckpointStatus.APPROVED


# ============================================================================
# AGENT MESSAGE
# ============================================================================

class MessagePriority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class AgentMessage(BaseModel):
    """
    Message for inter-agent communication.
    """
    
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Routing
    from_agent_id: str = Field(...)
    to_agent_id: str = Field(...)
    
    # Content
    message_type: str = Field(...)  # request, response, event, command
    subject: str = Field(...)
    body: Dict[str, Any] = Field(default_factory=dict)
    
    # Priority
    priority: MessagePriority = Field(default=MessagePriority.NORMAL)
    
    # Threading
    correlation_id: Optional[str] = Field(default=None)
    reply_to: Optional[str] = Field(default=None)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)
    delivered_at: Optional[datetime] = Field(default=None)
    read_at: Optional[datetime] = Field(default=None)
    
    # Status
    delivered: bool = Field(default=False)
    read: bool = Field(default=False)


# ============================================================================
# AGENT
# ============================================================================

class Agent(BaseModel):
    """
    Core agent model.
    
    Agents in CHE·NU™:
    - NEVER make autonomous decisions
    - Always operate within governance boundaries
    - Log all actions for audit
    - Can be paused/terminated at any time
    
    Hierarchy:
    - L0: System agents (infrastructure, monitoring)
    - L1: Orchestrator agents (coordinate L2s)
    - L2: Specialist agents (domain experts)
    - L3: Assistant agents (user-facing)
    """
    
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(default="")
    
    # Hierarchy
    level: AgentLevel = Field(...)
    parent_agent_id: Optional[str] = Field(default=None)
    
    # Classification
    agent_type: str = Field(default="generic")
    sphere: Optional[str] = Field(default=None)
    
    # Status
    status: AgentStatus = Field(default=AgentStatus.INITIALIZING)
    
    # Capabilities
    capabilities: List[AgentCapability] = Field(default_factory=list)
    
    # Tenant
    tenant_id: Optional[str] = Field(default=None)
    
    # Governance
    requires_hitl: bool = Field(default=False)
    auto_checkpoint_threshold: float = Field(default=0.5)
    max_actions_before_checkpoint: int = Field(default=10)
    
    # Stats
    actions_since_checkpoint: int = Field(default=0)
    total_actions: int = Field(default=0)
    total_checkpoints: int = Field(default=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: Optional[datetime] = Field(default=None)
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @computed_field
    @property
    def is_active(self) -> bool:
        return self.status in [AgentStatus.IDLE, AgentStatus.ACTIVE]
    
    @computed_field
    @property
    def needs_checkpoint(self) -> bool:
        return self.actions_since_checkpoint >= self.max_actions_before_checkpoint
    
    def can_perform(self, action_type: ActionType, sphere: Optional[str] = None) -> bool:
        """Check if agent can perform an action type"""
        for cap in self.capabilities:
            if action_type in cap.allowed_actions:
                if sphere is None or sphere in cap.allowed_spheres or not cap.allowed_spheres:
                    return True
        return False
    
    def get_impact_threshold(self) -> float:
        """Get the impact threshold requiring approval"""
        thresholds = [cap.requires_approval_above for cap in self.capabilities]
        return min(thresholds) if thresholds else 0.5


# ============================================================================
# AGENT CONTEXT
# ============================================================================

class AgentContext(BaseModel):
    """
    Runtime context for agent execution.
    
    Provides all information an agent needs to operate.
    """
    
    context_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = Field(...)
    
    # Session
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Current state
    current_simulation_id: Optional[str] = Field(default=None)
    current_scenario_id: Optional[str] = Field(default=None)
    current_sphere: Optional[str] = Field(default=None)
    
    # User context
    user_id: Optional[str] = Field(default=None)
    tenant_id: Optional[str] = Field(default=None)
    
    # Permissions (resolved)
    allowed_actions: Set[ActionType] = Field(default_factory=set)
    allowed_spheres: Set[str] = Field(default_factory=set)
    
    # State
    variables: Dict[str, Any] = Field(default_factory=dict)
    
    # History
    action_history: List[str] = Field(default_factory=list)  # Action IDs
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)


# ============================================================================
# AGENT TASK
# ============================================================================

class AgentTask(BaseModel):
    """
    A task assigned to an agent.
    """
    
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = Field(...)
    
    # Task definition
    name: str = Field(...)
    description: str = Field(default="")
    
    # Instructions
    instructions: List[str] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # Context
    simulation_id: Optional[str] = Field(default=None)
    sphere: Optional[str] = Field(default=None)
    
    # Priority
    priority: MessagePriority = Field(default=MessagePriority.NORMAL)
    
    # Status
    status: ActionStatus = Field(default=ActionStatus.PENDING)
    progress: float = Field(default=0.0, ge=0, le=1)
    
    # Results
    actions_performed: List[str] = Field(default_factory=list)
    result: Optional[Dict[str, Any]] = Field(default=None)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    deadline: Optional[datetime] = Field(default=None)


# ============================================================================
# DELEGATION
# ============================================================================

class Delegation(BaseModel):
    """
    Delegation of work from one agent to another.
    """
    
    delegation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Agents
    delegator_id: str = Field(...)  # Agent delegating
    delegate_id: str = Field(...)   # Agent receiving delegation
    
    # Task
    task_id: str = Field(...)
    
    # Scope
    scope: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    
    # Status
    accepted: bool = Field(default=False)
    completed: bool = Field(default=False)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
