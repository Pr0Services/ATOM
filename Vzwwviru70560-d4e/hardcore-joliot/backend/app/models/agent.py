"""
CHE·NU™ Agent Models
====================

Agent system with 226 specialized agents across 9 spheres.

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Agents NEVER take autonomous decisions
- Rule #4: My Team Restrictions - NO AI-to-AI orchestration
- Rule #6: Module Traceability - All executions audited

CANON ARCHITECTURE:
- 226 agents total across 9 spheres
- Each agent has defined scope, capabilities, token budget
- Agents PROPOSE, humans DECIDE
- All executions create audit trail
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    Float,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# =============================================================================
# ENUMS
# =============================================================================

class SphereType(str, enum.Enum):
    """The 10 canonical spheres - includes SYSTEM for AT·OM agents."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"
    SYSTEM = "system"  # AT·OM System Agents (Universe + Profile Mapping)


class AgentStatus(str, enum.Enum):
    """Agent availability status."""
    ACTIVE = "active"          # Available for use
    INACTIVE = "inactive"      # Disabled
    DEPRECATED = "deprecated"  # Being phased out
    BETA = "beta"              # Testing phase


class AgentCapabilityType(str, enum.Enum):
    """Types of agent capabilities."""
    # Analysis
    ANALYSIS = "analysis"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    
    # Generation
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    IMAGE_GENERATION = "image_generation"
    AUDIO_GENERATION = "audio_generation"
    
    # Processing
    DATA_PROCESSING = "data_processing"
    DOCUMENT_PROCESSING = "document_processing"
    
    # Communication (REQUIRES HUMAN GATE)
    EMAIL_DRAFT = "email_draft"
    MESSAGE_DRAFT = "message_draft"
    NOTIFICATION_DRAFT = "notification_draft"
    
    # Decision Support (NEVER autonomous)
    RECOMMENDATION = "recommendation"
    SCORING = "scoring"
    PRIORITIZATION = "prioritization"
    
    # Research
    RESEARCH = "research"
    SEARCH = "search"
    FACT_CHECK = "fact_check"
    
    # Creative
    BRAINSTORM = "brainstorm"
    DESIGN_ASSIST = "design_assist"
    CONTENT_PLANNING = "content_planning"


class ExecutionStatus(str, enum.Enum):
    """Agent execution status."""
    PENDING = "pending"                    # Waiting to start
    RUNNING = "running"                    # Currently executing
    AWAITING_APPROVAL = "awaiting_approval"  # Human gate triggered
    APPROVED = "approved"                  # Human approved
    REJECTED = "rejected"                  # Human rejected
    COMPLETED = "completed"                # Successfully finished
    FAILED = "failed"                      # Error occurred
    CANCELLED = "cancelled"                # User cancelled


class ExecutionTrigger(str, enum.Enum):
    """What triggered the agent execution."""
    USER_REQUEST = "user_request"       # Direct user action
    SCHEDULED = "scheduled"             # Scheduled task
    THREAD_EVENT = "thread_event"       # Thread event triggered
    WORKFLOW = "workflow"               # Part of a workflow
    # NO "AGENT_REQUEST" - Rule #4 forbids AI-to-AI orchestration


# =============================================================================
# AGENT DEFINITION MODEL
# =============================================================================

class Agent(Base):
    """
    Agent definition - one of 226 specialized agents.
    
    Agents are pre-defined by the system and cannot be created by users.
    Each agent has specific capabilities, scope, and token budget.
    
    R&D COMPLIANCE:
    - Agents NEVER take autonomous decisions
    - Agents PROPOSE, humans DECIDE
    - All capabilities respect Human Sovereignty (Rule #1)
    """
    __tablename__ = "agents"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, nullable=False)
    
    # Definition
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Sphere assignment (which sphere this agent belongs to)
    sphere_type = Column(
        SQLEnum(SphereType, name="agent_sphere_type"),
        nullable=False,
        index=True
    )
    
    # Status
    status = Column(
        SQLEnum(AgentStatus, name="agent_status"),
        nullable=False,
        default=AgentStatus.ACTIVE
    )
    
    # Capabilities (list of capability types)
    capabilities = Column(JSON, nullable=False, default=list)
    
    # Scope definition - what the agent can access
    scope = Column(JSON, nullable=False, default=dict)
    # Example: {"read": ["threads", "notes"], "write": ["drafts"], "execute": ["analysis"]}
    
    # Token budget (per execution)
    default_token_budget = Column(Integer, nullable=False, default=10000)
    max_token_budget = Column(Integer, nullable=False, default=50000)
    
    # Cost per 1K tokens (for billing)
    cost_per_1k_tokens = Column(Float, nullable=False, default=0.01)
    
    # LLM configuration
    preferred_llm = Column(String(50), nullable=True)  # e.g., "claude-3.5-sonnet"
    llm_config = Column(JSON, nullable=True)  # Temperature, etc.
    
    # Human gate requirements
    requires_human_gate = Column(Boolean, nullable=False, default=False)
    human_gate_capabilities = Column(JSON, nullable=False, default=list)
    # Capabilities that ALWAYS require human approval

    # AT·OM System Agent flags
    is_system_agent = Column(Boolean, nullable=False, default=False)
    # True for AT·OM mapping agents (Universe + Profile)
    auto_activate = Column(Boolean, nullable=False, default=False)
    # True if agent should auto-activate on identity creation

    # Prompts and templates
    system_prompt = Column(Text, nullable=True)
    prompt_templates = Column(JSON, nullable=True)

    # Metadata
    version = Column(String(20), nullable=False, default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    executions = relationship("AgentExecution", back_populates="agent", lazy="dynamic")
    user_configs = relationship("UserAgentConfig", back_populates="agent", lazy="dynamic")
    
    # Indexes
    __table_args__ = (
        Index("ix_agents_sphere_status", "sphere_type", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<Agent {self.name} ({self.sphere_type.value})>"
    
    def has_capability(self, capability: AgentCapabilityType) -> bool:
        """Check if agent has a specific capability."""
        return capability.value in self.capabilities
    
    def requires_approval_for(self, capability: AgentCapabilityType) -> bool:
        """Check if capability requires human approval."""
        if self.requires_human_gate:
            return True
        return capability.value in self.human_gate_capabilities


# =============================================================================
# USER AGENT CONFIGURATION
# =============================================================================

class UserAgentConfig(Base):
    """
    User-specific agent configuration.
    
    Users can customize agents (enable/disable, adjust budget)
    but CANNOT change capabilities or bypass human gates.
    """
    __tablename__ = "user_agent_configs"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, nullable=False)
    identity_id = Column(PGUUID(as_uuid=True), ForeignKey("identities.id"), nullable=False, index=True)
    agent_id = Column(PGUUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    
    # User settings
    enabled = Column(Boolean, nullable=False, default=True)
    custom_name = Column(String(200), nullable=True)  # User's nickname for agent
    
    # Budget overrides (cannot exceed agent max)
    token_budget_override = Column(Integer, nullable=True)
    
    # Usage tracking
    total_executions = Column(Integer, nullable=False, default=0)
    total_tokens_used = Column(Integer, nullable=False, default=0)
    total_cost = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="user_configs")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("identity_id", "agent_id", name="uq_user_agent_config"),
        Index("ix_user_agent_configs_identity_agent", "identity_id", "agent_id"),
    )
    
    def __repr__(self) -> str:
        return f"<UserAgentConfig {self.identity_id}:{self.agent_id}>"
    
    @property
    def effective_token_budget(self) -> int:
        """Get effective token budget (user override or agent default)."""
        if self.token_budget_override:
            return min(self.token_budget_override, self.agent.max_token_budget)
        return self.agent.default_token_budget


# =============================================================================
# AGENT EXECUTION MODEL
# =============================================================================

class AgentExecution(Base):
    """
    Record of an agent execution.
    
    EVERY agent execution is recorded for:
    - Audit trail (Rule #6: Traceability)
    - Human gate tracking (Rule #1: Human Sovereignty)
    - Cost tracking
    - Performance analysis
    
    R&D COMPLIANCE:
    - No "triggered_by_agent_id" - Rule #4 forbids AI-to-AI orchestration
    - Human is ALWAYS in the loop for sensitive actions
    """
    __tablename__ = "agent_executions"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, nullable=False)
    
    # Agent reference
    agent_id = Column(PGUUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    
    # User/Identity who initiated (ALWAYS a human, never an agent)
    identity_id = Column(PGUUID(as_uuid=True), ForeignKey("identities.id"), nullable=False, index=True)
    
    # Context
    sphere_id = Column(PGUUID(as_uuid=True), ForeignKey("spheres.id"), nullable=True, index=True)
    thread_id = Column(PGUUID(as_uuid=True), ForeignKey("threads.id"), nullable=True, index=True)
    
    # Trigger
    trigger = Column(
        SQLEnum(ExecutionTrigger, name="execution_trigger"),
        nullable=False,
        default=ExecutionTrigger.USER_REQUEST
    )
    
    # Status
    status = Column(
        SQLEnum(ExecutionStatus, name="execution_status"),
        nullable=False,
        default=ExecutionStatus.PENDING,
        index=True
    )
    
    # Request
    capability_used = Column(String(50), nullable=False)  # Which capability was invoked
    input_data = Column(JSON, nullable=False)  # Input provided to agent
    input_tokens = Column(Integer, nullable=True)
    
    # Output
    output_data = Column(JSON, nullable=True)  # Agent's output/proposal
    output_tokens = Column(Integer, nullable=True)
    
    # Human Gate (Rule #1: Human Sovereignty)
    requires_approval = Column(Boolean, nullable=False, default=False)
    checkpoint_id = Column(PGUUID(as_uuid=True), ForeignKey("governance_checkpoints.id"), nullable=True)
    approved_by = Column(PGUUID(as_uuid=True), nullable=True)  # Who approved (if required)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Performance
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)  # Execution time in milliseconds
    
    # Cost
    total_tokens = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    
    # LLM details
    llm_used = Column(String(50), nullable=True)
    llm_response_id = Column(String(200), nullable=True)  # For debugging
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    
    # Traceability (Rule #6)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)  # Always the human user
    
    # Relationships
    agent = relationship("Agent", back_populates="executions")
    
    # Indexes for common queries
    __table_args__ = (
        Index("ix_agent_executions_identity_status", "identity_id", "status"),
        Index("ix_agent_executions_agent_status", "agent_id", "status"),
        Index("ix_agent_executions_created_at", "created_at"),
        CheckConstraint(
            "trigger != 'agent_request'",
            name="ck_no_ai_to_ai_orchestration"
        ),
    )
    
    def __repr__(self) -> str:
        return f"<AgentExecution {self.id} ({self.status.value})>"
    
    @property
    def is_pending_approval(self) -> bool:
        """Check if execution is waiting for human approval."""
        return self.status == ExecutionStatus.AWAITING_APPROVAL
    
    @property
    def execution_time_seconds(self) -> Optional[float]:
        """Get execution time in seconds."""
        if self.duration_ms:
            return self.duration_ms / 1000.0
        return None


# =============================================================================
# AGENT EXECUTION STEP (for multi-step agents)
# =============================================================================

class AgentExecutionStep(Base):
    """
    Individual step within a multi-step agent execution.
    
    Some agents perform multiple LLM calls or processing steps.
    Each step is recorded for transparency and debugging.
    """
    __tablename__ = "agent_execution_steps"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, nullable=False)
    execution_id = Column(PGUUID(as_uuid=True), ForeignKey("agent_executions.id"), nullable=False, index=True)
    
    # Step info
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(100), nullable=False)
    step_type = Column(String(50), nullable=False)  # "llm_call", "processing", "validation"
    
    # Input/Output
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    
    # Tokens (for LLM steps)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(20), nullable=False, default="pending")
    error_message = Column(Text, nullable=True)
    
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    
    # Traceability
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("execution_id", "step_number", name="uq_execution_step_number"),
        Index("ix_agent_execution_steps_execution", "execution_id"),
    )
    
    def __repr__(self) -> str:
        return f"<AgentExecutionStep {self.execution_id}:{self.step_number}>"


# =============================================================================
# AGENT METRICS (for analytics)
# =============================================================================

class AgentMetrics(Base):
    """
    Aggregated metrics for agent performance.
    
    Updated periodically for dashboard displays.
    """
    __tablename__ = "agent_metrics"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, nullable=False)
    agent_id = Column(PGUUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    period_type = Column(String(20), nullable=False)  # "hourly", "daily", "weekly", "monthly"
    
    # Execution counts
    total_executions = Column(Integer, nullable=False, default=0)
    successful_executions = Column(Integer, nullable=False, default=0)
    failed_executions = Column(Integer, nullable=False, default=0)
    
    # Human gate stats
    approvals_required = Column(Integer, nullable=False, default=0)
    approvals_granted = Column(Integer, nullable=False, default=0)
    approvals_rejected = Column(Integer, nullable=False, default=0)
    
    # Performance
    avg_duration_ms = Column(Float, nullable=True)
    p95_duration_ms = Column(Float, nullable=True)
    
    # Token usage
    total_tokens = Column(Integer, nullable=False, default=0)
    avg_tokens_per_execution = Column(Float, nullable=True)
    
    # Cost
    total_cost = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint("agent_id", "period_start", "period_type", name="uq_agent_metrics_period"),
        Index("ix_agent_metrics_agent_period", "agent_id", "period_start"),
    )
    
    def __repr__(self) -> str:
        return f"<AgentMetrics {self.agent_id} ({self.period_type})>"


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
    "SphereType",
    "AgentStatus",
    "AgentCapabilityType",
    "ExecutionStatus",
    "ExecutionTrigger",
    # Models
    "Agent",
    "UserAgentConfig",
    "AgentExecution",
    "AgentExecutionStep",
    "AgentMetrics",
]
