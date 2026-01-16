"""
CHE·NU™ Agent Schemas
=====================

Pydantic schemas for Agent API validation.

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - execution requests clearly marked
- Rule #4: No AI-to-AI orchestration in trigger types
- Rule #6: Traceability fields required
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict, field_validator


# =============================================================================
# ENUMS (mirror of SQLAlchemy enums)
# =============================================================================

class SphereType(str, Enum):
    """
    The AT·OM Spheres - 16 Domains of the Ecosystem

    Original 9 + Transport + Societal + Environment + Community Pulse +
    Privacy + Jeunesse + Dashboard
    """
    # Original 9 Spheres
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"

    # V68 Expansions - AT·OM Ecosystem
    TRANSPORT = "transport"          # AT·OM Flow - Transport & Logistics (50 agents)
    SOCIETAL = "societal"            # Équilibre, Éducation, Santé, Gouvernance
    ENVIRONMENT = "environment"      # Régénération, Énergie, Biodiversité, Circulaire
    PRIVACY = "privacy"              # Privacy Guardian
    JEUNESSE = "jeunesse"            # Génie de Demain - Éducation Souveraine
    DASHBOARD = "dashboard"          # Master Dashboard - AT·OM Vision


class AgentStatus(str, Enum):
    """Agent availability status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    BETA = "beta"


class AgentCapabilityType(str, Enum):
    """Types of agent capabilities."""
    ANALYSIS = "analysis"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    IMAGE_GENERATION = "image_generation"
    AUDIO_GENERATION = "audio_generation"
    DATA_PROCESSING = "data_processing"
    DOCUMENT_PROCESSING = "document_processing"
    EMAIL_DRAFT = "email_draft"
    MESSAGE_DRAFT = "message_draft"
    NOTIFICATION_DRAFT = "notification_draft"
    RECOMMENDATION = "recommendation"
    SCORING = "scoring"
    PRIORITIZATION = "prioritization"
    RESEARCH = "research"
    SEARCH = "search"
    FACT_CHECK = "fact_check"
    BRAINSTORM = "brainstorm"
    DESIGN_ASSIST = "design_assist"
    CONTENT_PLANNING = "content_planning"


class ExecutionStatus(str, Enum):
    """Agent execution status."""
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionTrigger(str, Enum):
    """What triggered the agent execution - NO AGENT_REQUEST (Rule #4)."""
    USER_REQUEST = "user_request"
    SCHEDULED = "scheduled"
    THREAD_EVENT = "thread_event"
    WORKFLOW = "workflow"


# =============================================================================
# AGENT SCHEMAS
# =============================================================================

class AgentCapability(BaseModel):
    """Single capability definition."""
    type: AgentCapabilityType
    description: Optional[str] = None
    requires_approval: bool = False


class AgentScope(BaseModel):
    """Agent's access scope."""
    read: List[str] = Field(default_factory=list)
    write: List[str] = Field(default_factory=list)
    execute: List[str] = Field(default_factory=list)


class AgentBase(BaseModel):
    """Base agent properties."""
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)
    description: str
    sphere_type: SphereType


class AgentCreate(AgentBase):
    """Schema for creating an agent (admin only)."""
    capabilities: List[AgentCapabilityType] = Field(default_factory=list)
    scope: AgentScope = Field(default_factory=AgentScope)
    default_token_budget: int = Field(default=10000, ge=1000, le=100000)
    max_token_budget: int = Field(default=50000, ge=1000, le=500000)
    cost_per_1k_tokens: float = Field(default=0.01, ge=0)
    preferred_llm: Optional[str] = None
    requires_human_gate: bool = False
    human_gate_capabilities: List[AgentCapabilityType] = Field(default_factory=list)
    system_prompt: Optional[str] = None


class AgentUpdate(BaseModel):
    """Schema for updating an agent (admin only)."""
    display_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    capabilities: Optional[List[AgentCapabilityType]] = None
    scope: Optional[AgentScope] = None
    default_token_budget: Optional[int] = Field(None, ge=1000, le=100000)
    max_token_budget: Optional[int] = Field(None, ge=1000, le=500000)
    cost_per_1k_tokens: Optional[float] = Field(None, ge=0)
    preferred_llm: Optional[str] = None
    requires_human_gate: Optional[bool] = None
    human_gate_capabilities: Optional[List[AgentCapabilityType]] = None
    system_prompt: Optional[str] = None


class AgentResponse(AgentBase):
    """Full agent response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    status: AgentStatus
    capabilities: List[str]
    scope: Dict[str, Any]
    default_token_budget: int
    max_token_budget: int
    cost_per_1k_tokens: float
    preferred_llm: Optional[str]
    requires_human_gate: bool
    human_gate_capabilities: List[str]
    version: str
    created_at: datetime
    updated_at: Optional[datetime]


class AgentSummary(BaseModel):
    """Lightweight agent summary for listings."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    display_name: str
    sphere_type: SphereType
    status: AgentStatus
    capabilities: List[str]
    requires_human_gate: bool


class AgentListResponse(BaseModel):
    """Response for listing agents."""
    agents: List[AgentSummary]
    total: int
    by_sphere: Dict[str, int]


# =============================================================================
# USER AGENT CONFIG SCHEMAS
# =============================================================================

class UserAgentConfigCreate(BaseModel):
    """Create user-specific agent configuration."""
    agent_id: UUID
    enabled: bool = True
    custom_name: Optional[str] = Field(None, max_length=200)
    token_budget_override: Optional[int] = Field(None, ge=1000, le=100000)


class UserAgentConfigUpdate(BaseModel):
    """Update user-specific agent configuration."""
    enabled: Optional[bool] = None
    custom_name: Optional[str] = Field(None, max_length=200)
    token_budget_override: Optional[int] = Field(None, ge=1000, le=100000)


class UserAgentConfigResponse(BaseModel):
    """User's agent configuration response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    agent_id: UUID
    identity_id: UUID
    enabled: bool
    custom_name: Optional[str]
    token_budget_override: Optional[int]
    effective_token_budget: int
    total_executions: int
    total_tokens_used: int
    total_cost: float
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Include agent summary
    agent: AgentSummary


# =============================================================================
# EXECUTION SCHEMAS
# =============================================================================

class ExecutionRequest(BaseModel):
    """
    Request to execute an agent.
    
    R&D COMPLIANCE:
    - trigger cannot be "agent_request" (Rule #4: No AI-to-AI orchestration)
    - Human is always the initiator
    """
    agent_id: UUID
    capability: AgentCapabilityType
    input_data: Dict[str, Any]
    
    # Optional context
    sphere_id: Optional[UUID] = None
    thread_id: Optional[UUID] = None
    
    # Trigger (NO AGENT_REQUEST allowed)
    trigger: ExecutionTrigger = ExecutionTrigger.USER_REQUEST
    
    # Budget override for this execution
    token_budget: Optional[int] = Field(None, ge=100, le=100000)
    
    @field_validator("trigger")
    @classmethod
    def validate_trigger(cls, v: ExecutionTrigger) -> ExecutionTrigger:
        """Ensure no AI-to-AI orchestration (Rule #4)."""
        # ExecutionTrigger enum already excludes AGENT_REQUEST
        # but this is a safety check
        if v.value == "agent_request":
            raise ValueError("AI-to-AI orchestration is forbidden (Rule #4)")
        return v


class ExecutionApproval(BaseModel):
    """Approve a pending execution (Human Gate)."""
    execution_id: UUID
    approved: bool
    rejection_reason: Optional[str] = Field(None, max_length=1000)


class ExecutionStepResponse(BaseModel):
    """Individual execution step."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    step_number: int
    step_name: str
    step_type: str
    status: str
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    duration_ms: Optional[int]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]


class ExecutionResponse(BaseModel):
    """Full execution response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    agent_id: UUID
    identity_id: UUID
    sphere_id: Optional[UUID]
    thread_id: Optional[UUID]
    
    trigger: ExecutionTrigger
    status: ExecutionStatus
    capability_used: str
    
    # Input/Output
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    
    # Human Gate
    requires_approval: bool
    checkpoint_id: Optional[UUID]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    
    # Performance
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    total_tokens: Optional[int]
    cost: Optional[float]
    duration_ms: Optional[int]
    
    # LLM info
    llm_used: Optional[str]
    
    # Error
    error_message: Optional[str]
    error_code: Optional[str]
    
    # Timestamps (Traceability - Rule #6)
    created_at: datetime
    created_by: UUID
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    # Steps (for multi-step executions)
    steps: List[ExecutionStepResponse] = Field(default_factory=list)


class ExecutionSummary(BaseModel):
    """Lightweight execution summary for listings."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    agent_id: UUID
    status: ExecutionStatus
    capability_used: str
    requires_approval: bool
    total_tokens: Optional[int]
    cost: Optional[float]
    duration_ms: Optional[int]
    created_at: datetime


class ExecutionListResponse(BaseModel):
    """Response for listing executions."""
    executions: List[ExecutionSummary]
    total: int
    by_status: Dict[str, int]


# =============================================================================
# CHECKPOINT RESPONSE (HTTP 423)
# =============================================================================

class ExecutionCheckpointResponse(BaseModel):
    """
    Response when execution requires human approval (HTTP 423).
    
    This is returned instead of the execution result when
    the agent's action requires human gate.
    """
    status: str = "checkpoint_pending"
    message: str = "Execution requires human approval"
    execution_id: UUID
    checkpoint_id: UUID
    agent_name: str
    capability: str
    preview: Optional[Dict[str, Any]] = None  # Preview of what agent wants to do
    options: List[str] = Field(default=["approve", "reject"])


# =============================================================================
# METRICS SCHEMAS
# =============================================================================

class AgentMetricsResponse(BaseModel):
    """Agent metrics for a period."""
    model_config = ConfigDict(from_attributes=True)
    
    agent_id: UUID
    period_start: datetime
    period_end: datetime
    period_type: str
    
    total_executions: int
    successful_executions: int
    failed_executions: int
    success_rate: float
    
    approvals_required: int
    approvals_granted: int
    approvals_rejected: int
    approval_rate: Optional[float]
    
    avg_duration_ms: Optional[float]
    p95_duration_ms: Optional[float]
    
    total_tokens: int
    avg_tokens_per_execution: Optional[float]
    total_cost: float


class UserAgentMetrics(BaseModel):
    """User's overall agent usage metrics."""
    total_executions: int
    total_tokens_used: int
    total_cost: float
    most_used_agents: List[Dict[str, Any]]
    executions_by_sphere: Dict[str, int]
    executions_by_status: Dict[str, int]


# =============================================================================
# SPHERE AGENT SUMMARY
# =============================================================================

class SphereAgentSummary(BaseModel):
    """Summary of agents available in a sphere."""
    sphere_type: SphereType
    total_agents: int
    active_agents: int
    agents: List[AgentSummary]


class AllSpheresAgentSummary(BaseModel):
    """Summary of agents across all 9 spheres."""
    total_agents: int
    by_sphere: Dict[str, SphereAgentSummary]


# =============================================================================
# AGENT REGISTRY CONSTANTS
# =============================================================================

# Distribution of 350 agents across 16 spheres (AT·OM L'ESSAIM - The Swarm)
AGENT_DISTRIBUTION = {
    # Original 9 Spheres (226 agents)
    SphereType.PERSONAL: 28,
    SphereType.BUSINESS: 43,
    SphereType.GOVERNMENT: 18,
    SphereType.CREATIVE_STUDIO: 42,
    SphereType.COMMUNITY: 12,
    SphereType.SOCIAL_MEDIA: 15,
    SphereType.ENTERTAINMENT: 8,
    SphereType.MY_TEAM: 35,
    SphereType.SCHOLAR: 25,

    # V68 AT·OM Ecosystem Expansions (124 agents)
    SphereType.TRANSPORT: 50,      # AT·OM Flow - Division Cinétique Urbaine
    SphereType.SOCIETAL: 20,       # Équilibre, Éducation, Santé, Gouvernance (Consensus Liquide)
    SphereType.ENVIRONMENT: 25,    # Régénération, Énergie, Biodiversité, Circulaire
    SphereType.PRIVACY: 8,         # Privacy Guardian - Data Sovereignty
    SphereType.JEUNESSE: 15,       # Génie de Demain - Éducation Souveraine
    SphereType.DASHBOARD: 6,       # Master Dashboard - AT·OM Vision
}

TOTAL_AGENTS = 350  # L'ESSAIM - The Swarm (Canon AT·OM)


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
    # Agent schemas
    "AgentCapability",
    "AgentScope",
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentSummary",
    "AgentListResponse",
    # User config
    "UserAgentConfigCreate",
    "UserAgentConfigUpdate",
    "UserAgentConfigResponse",
    # Execution
    "ExecutionRequest",
    "ExecutionApproval",
    "ExecutionStepResponse",
    "ExecutionResponse",
    "ExecutionSummary",
    "ExecutionListResponse",
    "ExecutionCheckpointResponse",
    # Metrics
    "AgentMetricsResponse",
    "UserAgentMetrics",
    # Summaries
    "SphereAgentSummary",
    "AllSpheresAgentSummary",
    # Constants
    "AGENT_DISTRIBUTION",
    "TOTAL_AGENTS",
]
