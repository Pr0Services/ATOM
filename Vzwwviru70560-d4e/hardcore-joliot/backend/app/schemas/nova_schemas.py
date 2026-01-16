"""
SCHEMAS: nova_schemas.py
PURPOSE: Pydantic schemas for Nova Pipeline API
VERSION: 1.0.0

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Checkpoint schemas for HTTP 423
- Rule #6: Traceability - All responses include audit fields
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# ENUMS (Mirror of model enums for API)
# ============================================================================

class PipelineLane(str, Enum):
    """Nova pipeline lanes."""
    INTENT_ANALYSIS = "intent_analysis"
    CONTEXT_SNAPSHOT = "context_snapshot"
    SEMANTIC_ENCODING = "semantic_encoding"
    GOVERNANCE_CHECK = "governance_check"
    CHECKPOINT = "checkpoint"
    EXECUTION = "execution"
    AUDIT = "audit"


class PipelineStatus(str, Enum):
    """Pipeline processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IntentType(str, Enum):
    """Types of user intent."""
    QUERY = "query"
    COMMAND = "command"
    CREATION = "creation"
    MODIFICATION = "modification"
    DELETION = "deletion"
    ANALYSIS = "analysis"
    GENERATION = "generation"
    COMMUNICATION = "communication"
    NAVIGATION = "navigation"
    SEARCH = "search"
    UNKNOWN = "unknown"


class IntentUrgency(str, Enum):
    """Urgency level of intent."""
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"


class GovernanceAction(str, Enum):
    """Actions governance can take."""
    ALLOW = "allow"
    CHECKPOINT = "checkpoint"
    DENY = "deny"
    ESCALATE = "escalate"
    REVIEW = "review"


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class NovaPipelineCreate(BaseModel):
    """Request to process through Nova pipeline."""
    
    input_text: str = Field(..., min_length=1, max_length=50000, description="User input to process")
    input_context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    # Optional targeting
    thread_id: Optional[UUID] = Field(None, description="Thread context")
    sphere_id: Optional[UUID] = Field(None, description="Target sphere")
    
    # Processing options
    preferred_agent: Optional[str] = Field(None, description="Preferred agent name")
    preferred_llm: Optional[str] = Field(None, description="Preferred LLM provider")
    max_tokens: Optional[int] = Field(None, ge=1, le=100000, description="Max tokens to use")
    
    # Priority
    urgency: IntentUrgency = Field(IntentUrgency.NORMAL, description="Request urgency")
    
    @field_validator("input_text")
    @classmethod
    def validate_input(cls, v: str) -> str:
        """Validate input is not just whitespace."""
        if not v.strip():
            raise ValueError("Input cannot be empty or whitespace only")
        return v.strip()


class NovaPipelineApproval(BaseModel):
    """Approve a pipeline checkpoint."""
    
    approve: bool = Field(..., description="True to approve, False to reject")
    reason: Optional[str] = Field(None, max_length=1000, description="Reason for decision")
    modifications: Optional[Dict[str, Any]] = Field(None, description="Modifications to apply")


# ============================================================================
# LANE RESULT SCHEMAS
# ============================================================================

class IntentAnalysisResult(BaseModel):
    """Result from Lane A: Intent Analysis."""
    
    intent_type: IntentType
    intent_confidence: float = Field(..., ge=0.0, le=1.0)
    urgency: IntentUrgency
    
    # Extracted info
    entities: Optional[Dict[str, List[str]]] = None
    keywords: Optional[List[str]] = None
    
    # Targets
    target_sphere: Optional[str] = None
    target_thread_id: Optional[UUID] = None
    target_agent: Optional[str] = None
    
    # Actions
    primary_action: Optional[str] = None
    secondary_actions: Optional[List[str]] = None
    
    # Sensitivity
    is_sensitive: bool = False
    sensitivity_reasons: Optional[List[str]] = None
    requires_confirmation: bool = False


class ContextSnapshotResult(BaseModel):
    """Result from Lane B: Context Snapshot."""
    
    # Thread context
    thread_id: Optional[UUID] = None
    thread_event_count: Optional[int] = None
    thread_last_event_type: Optional[str] = None
    
    # Sphere context
    sphere_id: Optional[UUID] = None
    sphere_type: Optional[str] = None
    active_agents_count: int = 0
    
    # User context
    user_preferences: Optional[Dict[str, Any]] = None
    recent_actions_count: int = 0
    
    # Conversation context
    conversation_turns: int = 0
    conversation_summary: Optional[str] = None
    
    # Memory context
    hot_memory_items: int = 0
    warm_memory_available: bool = False


class GovernanceCheckResultSchema(BaseModel):
    """Result from Lane D: Governance Check."""
    
    action: GovernanceAction
    
    # Permission results
    has_sphere_access: bool = True
    has_thread_access: bool = True
    has_agent_access: bool = True
    has_action_permission: bool = True
    
    # Rule checks
    rules_checked: List[str] = []
    rules_violated: List[str] = []
    
    # Budget
    within_token_budget: bool = True
    estimated_tokens: Optional[int] = None
    available_budget: Optional[int] = None
    
    # Checkpoint info
    checkpoint_required: bool = False
    checkpoint_type: Optional[str] = None
    checkpoint_reason: Optional[str] = None
    checkpoint_options: Optional[List[str]] = None
    
    # Cross-sphere
    is_cross_sphere: bool = False
    source_sphere: Optional[str] = None
    target_sphere: Optional[str] = None
    
    # Identity
    identity_boundary_ok: bool = True


class ExecutionResultSchema(BaseModel):
    """Result from Lane F: Execution."""
    
    execution_type: str
    success: bool
    
    # LLM info
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    
    # Agent info
    agent_name: Optional[str] = None
    agent_execution_id: Optional[UUID] = None
    
    # Output
    output_text: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    
    # Events created
    events_created: List[UUID] = []
    events_count: int = 0
    
    # Metrics
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost: Optional[float] = None
    latency_ms: Optional[int] = None
    
    # Error
    error_message: Optional[str] = None


class AuditResultSchema(BaseModel):
    """Result from Lane G: Audit."""
    
    request_type: str
    request_summary: str
    
    # Processing
    lanes_executed: List[PipelineLane]
    total_duration_ms: int
    
    # Outcome
    outcome: str
    outcome_reason: Optional[str] = None
    
    # Checkpoint
    checkpoint_triggered: bool = False
    checkpoint_outcome: Optional[str] = None
    checkpoint_duration_ms: Optional[int] = None
    
    # Resources
    total_tokens: Optional[int] = None
    total_cost: Optional[float] = None
    
    # Changes
    threads_affected: List[UUID] = []
    events_created: List[UUID] = []


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class LaneResultResponse(BaseModel):
    """Response for individual lane result."""
    
    lane: PipelineLane
    lane_order: int
    status: str
    
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    
    # Result data (type depends on lane)
    result: Optional[Dict[str, Any]] = None
    
    # Error
    error_message: Optional[str] = None


class NovaPipelineResponse(BaseModel):
    """Full response for a pipeline request."""
    
    # Identity
    id: UUID
    identity_id: UUID
    
    # Request
    input_text: str
    input_context: Optional[Dict[str, Any]] = None
    
    # Context
    thread_id: Optional[UUID] = None
    sphere_id: Optional[UUID] = None
    
    # Status
    status: PipelineStatus
    current_lane: Optional[PipelineLane] = None
    
    # Output
    output_text: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    
    # Lane results
    lane_results: List[LaneResultResponse] = []
    
    # Checkpoint
    checkpoint_triggered: bool = False
    checkpoint_id: Optional[UUID] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    
    # Execution details
    agent_id: Optional[UUID] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    
    # Metrics
    total_tokens: Optional[int] = None
    total_cost: Optional[float] = None
    processing_time_ms: Optional[int] = None
    
    # Error
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    
    # Traceability
    created_at: datetime
    created_by: UUID
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class NovaPipelineSummary(BaseModel):
    """Summary of a pipeline request (for lists)."""
    
    id: UUID
    status: PipelineStatus
    
    input_preview: str  # First N chars of input
    output_preview: Optional[str] = None  # First N chars of output
    
    intent_type: Optional[IntentType] = None
    checkpoint_triggered: bool = False
    
    thread_id: Optional[UUID] = None
    sphere_id: Optional[UUID] = None
    
    processing_time_ms: Optional[int] = None
    created_at: datetime


class NovaPipelineListResponse(BaseModel):
    """List of pipeline requests with pagination."""
    
    items: List[NovaPipelineSummary]
    total: int
    page: int
    page_size: int
    pages: int


# ============================================================================
# CHECKPOINT RESPONSE (HTTP 423)
# ============================================================================

class NovaPipelineCheckpointResponse(BaseModel):
    """
    Response when pipeline requires approval (HTTP 423).
    
    R&D COMPLIANCE:
    - Rule #1: Human Sovereignty - Full context for informed decision
    """
    
    status: str = "checkpoint_pending"
    
    # Pipeline info
    pipeline_id: UUID
    current_lane: PipelineLane
    
    # Checkpoint details
    checkpoint: Dict[str, Any] = Field(..., description="Checkpoint details")
    
    # What triggered it
    trigger_reason: str
    trigger_details: Optional[Dict[str, Any]] = None
    
    # Proposed action (for preview)
    proposed_action: str
    proposed_action_preview: Optional[str] = None
    
    # Options
    options: List[str] = ["approve", "reject"]
    
    # Context for decision
    intent_analysis: Optional[IntentAnalysisResult] = None
    governance_check: Optional[GovernanceCheckResultSchema] = None
    
    # Estimated impact
    estimated_tokens: Optional[int] = None
    estimated_cost: Optional[float] = None
    
    # Links
    approval_url: str
    rejection_url: str


# ============================================================================
# METRICS SCHEMAS
# ============================================================================

class LaneMetrics(BaseModel):
    """Metrics for a single lane."""
    
    lane: PipelineLane
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    avg_duration_ms: Optional[float] = None
    p95_duration_ms: Optional[float] = None


class NovaPipelineMetrics(BaseModel):
    """Overall Nova pipeline metrics."""
    
    # Time period
    period_start: datetime
    period_end: datetime
    period_type: str
    
    # Request metrics
    total_requests: int = 0
    completed_requests: int = 0
    failed_requests: int = 0
    cancelled_requests: int = 0
    
    # Checkpoint metrics
    checkpoints_triggered: int = 0
    checkpoints_approved: int = 0
    checkpoints_rejected: int = 0
    avg_checkpoint_duration_ms: Optional[float] = None
    
    # Performance
    avg_processing_time_ms: Optional[float] = None
    p50_processing_time_ms: Optional[float] = None
    p95_processing_time_ms: Optional[float] = None
    p99_processing_time_ms: Optional[float] = None
    
    # Lane metrics
    lane_metrics: List[LaneMetrics] = []
    
    # Resources
    total_tokens: int = 0
    total_cost: float = 0.0
    
    # Intent distribution
    intent_distribution: Dict[str, int] = {}
    
    # Errors
    error_count: int = 0
    error_distribution: Dict[str, int] = {}


class NovaSystemStats(BaseModel):
    """Current system statistics."""
    
    # Queues
    pending_requests: int = 0
    awaiting_approval: int = 0
    processing: int = 0
    
    # Today's stats
    today_requests: int = 0
    today_completed: int = 0
    today_checkpoints: int = 0
    
    # Resource usage
    tokens_used_today: int = 0
    cost_today: float = 0.0
    
    # Performance (last hour)
    avg_processing_time_ms: Optional[float] = None
    requests_per_minute: Optional[float] = None


# ============================================================================
# STREAMING SCHEMAS
# ============================================================================

class NovaPipelineStreamEvent(BaseModel):
    """Event for streaming pipeline progress."""
    
    event_type: str  # lane_started, lane_completed, checkpoint, completed, error
    pipeline_id: UUID
    
    # Lane info (if applicable)
    lane: Optional[PipelineLane] = None
    lane_status: Optional[str] = None
    
    # Progress
    lanes_completed: int = 0
    total_lanes: int = 7
    
    # Partial output (if applicable)
    partial_output: Optional[str] = None
    
    # Checkpoint (if applicable)
    checkpoint: Optional[Dict[str, Any]] = None
    
    # Error (if applicable)
    error: Optional[str] = None
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# CONSTANTS
# ============================================================================

# Lane execution order
LANE_ORDER = {
    PipelineLane.INTENT_ANALYSIS: 1,
    PipelineLane.CONTEXT_SNAPSHOT: 2,
    PipelineLane.SEMANTIC_ENCODING: 3,
    PipelineLane.GOVERNANCE_CHECK: 4,
    PipelineLane.CHECKPOINT: 5,
    PipelineLane.EXECUTION: 6,
    PipelineLane.AUDIT: 7,
}

# Lanes that can trigger checkpoints
CHECKPOINT_TRIGGER_LANES = [
    PipelineLane.GOVERNANCE_CHECK,
    PipelineLane.EXECUTION,
]

# Lanes that always run
MANDATORY_LANES = [
    PipelineLane.INTENT_ANALYSIS,
    PipelineLane.GOVERNANCE_CHECK,
    PipelineLane.AUDIT,
]
