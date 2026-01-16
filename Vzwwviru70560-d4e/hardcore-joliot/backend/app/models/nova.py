"""
MODELS: nova.py
PURPOSE: Nova Multi-Lane Pipeline models
VERSION: 1.0.0

Nova is the intelligence system of CHE·NU.
It processes requests through 7 lanes:
- Lane A: Intent Analysis
- Lane B: Context Snapshot  
- Lane C: Semantic Encoding
- Lane D: Governance Check
- Lane E: Checkpoint (HTTP 423)
- Lane F: Execution
- Lane G: Audit

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Checkpoint lane blocks until approval
- Rule #2: Autonomy Isolation - Nova proposes, humans decide
- Rule #6: Traceability - Full audit trail of all processing

HUMAN GATES:
- Lane E triggers HTTP 423 for sensitive operations
- All executions logged in audit trail
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, 
    Text, Integer, Float, JSON, Enum as SQLEnum,
    UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.models.base import Base


# ============================================================================
# ENUMS
# ============================================================================

class PipelineLane(str, Enum):
    """Nova pipeline lanes."""
    INTENT_ANALYSIS = "intent_analysis"       # Lane A: Understand user intent
    CONTEXT_SNAPSHOT = "context_snapshot"     # Lane B: Capture current state
    SEMANTIC_ENCODING = "semantic_encoding"   # Lane C: Encode for AI
    GOVERNANCE_CHECK = "governance_check"     # Lane D: Verify rules/permissions
    CHECKPOINT = "checkpoint"                 # Lane E: Human gate (HTTP 423)
    EXECUTION = "execution"                   # Lane F: Execute after approval
    AUDIT = "audit"                           # Lane G: Log everything


class PipelineStatus(str, Enum):
    """Pipeline processing status."""
    PENDING = "pending"                       # Not started
    PROCESSING = "processing"                 # Currently running
    AWAITING_APPROVAL = "awaiting_approval"   # Blocked at checkpoint
    APPROVED = "approved"                     # Checkpoint approved
    REJECTED = "rejected"                     # Checkpoint rejected
    COMPLETED = "completed"                   # Successfully finished
    FAILED = "failed"                         # Error occurred
    CANCELLED = "cancelled"                   # User cancelled


class LaneStatus(str, Enum):
    """Individual lane status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"                       # Lane not needed for this request
    BLOCKED = "blocked"                       # Waiting for dependency


class IntentType(str, Enum):
    """Types of user intent detected by Lane A."""
    QUERY = "query"                           # Information request
    COMMAND = "command"                       # Action request
    CREATION = "creation"                     # Create something
    MODIFICATION = "modification"             # Change something
    DELETION = "deletion"                     # Remove something
    ANALYSIS = "analysis"                     # Analyze data
    GENERATION = "generation"                 # Generate content
    COMMUNICATION = "communication"           # Send message/email
    NAVIGATION = "navigation"                 # Move/browse
    SEARCH = "search"                         # Find something
    UNKNOWN = "unknown"                       # Could not determine


class IntentUrgency(str, Enum):
    """Urgency level of intent."""
    CRITICAL = "critical"                     # Immediate action needed
    HIGH = "high"                             # Important, soon
    NORMAL = "normal"                         # Standard priority
    LOW = "low"                               # Can wait
    BACKGROUND = "background"                 # Process when convenient


class GovernanceAction(str, Enum):
    """Actions governance can take."""
    ALLOW = "allow"                           # Proceed without checkpoint
    CHECKPOINT = "checkpoint"                 # Require human approval
    DENY = "deny"                             # Block request
    ESCALATE = "escalate"                     # Require higher authority
    REVIEW = "review"                         # Flag for later review


# ============================================================================
# NOVA PIPELINE REQUEST
# ============================================================================

class NovaPipelineRequest(Base):
    """
    A request processed through the Nova pipeline.
    
    This is the main entity tracking a request from input to output
    through all 7 lanes.
    
    R&D COMPLIANCE:
    - Rule #6: Full traceability with created_by, timestamps
    - Rule #1: Status tracks checkpoint approvals
    """
    __tablename__ = "nova_pipeline_requests"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    identity_id = Column(PGUUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    # Request
    input_text = Column(Text, nullable=False)
    input_context = Column(JSON, nullable=True)  # Additional context
    
    # Thread context (if request is within a thread)
    thread_id = Column(PGUUID(as_uuid=True), ForeignKey("threads.id"), nullable=True)
    sphere_id = Column(PGUUID(as_uuid=True), ForeignKey("spheres.id"), nullable=True)
    
    # Status
    status = Column(SQLEnum(PipelineStatus), nullable=False, default=PipelineStatus.PENDING)
    current_lane = Column(SQLEnum(PipelineLane), nullable=True)
    
    # Results
    output_text = Column(Text, nullable=True)
    output_data = Column(JSON, nullable=True)
    
    # Checkpoint (if triggered)
    checkpoint_id = Column(PGUUID(as_uuid=True), ForeignKey("governance_checkpoints.id"), nullable=True)
    checkpoint_triggered = Column(Boolean, nullable=False, default=False)
    approved_by = Column(PGUUID(as_uuid=True), nullable=True)  # User who approved
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Execution details
    agent_id = Column(PGUUID(as_uuid=True), nullable=True)  # If agent was used
    llm_provider = Column(String(50), nullable=True)
    llm_model = Column(String(100), nullable=True)
    
    # Metrics
    total_tokens = Column(Integer, nullable=True)
    total_cost = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    error_lane = Column(SQLEnum(PipelineLane), nullable=True)
    
    # Traceability (Rule #6)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)  # Always human
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    lane_results = relationship("NovaPipelineLaneResult", back_populates="pipeline_request")
    
    # Indexes
    __table_args__ = (
        Index("ix_nova_requests_identity", "identity_id"),
        Index("ix_nova_requests_thread", "thread_id"),
        Index("ix_nova_requests_status", "status"),
        Index("ix_nova_requests_created", "created_at"),
        Index("ix_nova_requests_checkpoint", "checkpoint_triggered"),
    )


# ============================================================================
# LANE RESULTS
# ============================================================================

class NovaPipelineLaneResult(Base):
    """
    Result from processing a single lane.
    
    Each lane produces a result that may be used by subsequent lanes.
    """
    __tablename__ = "nova_lane_results"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False)
    
    # Lane
    lane = Column(SQLEnum(PipelineLane), nullable=False)
    lane_order = Column(Integer, nullable=False)  # Execution order (1-7)
    
    # Status
    status = Column(SQLEnum(LaneStatus), nullable=False, default=LaneStatus.PENDING)
    
    # Input/Output
    lane_input = Column(JSON, nullable=True)
    lane_output = Column(JSON, nullable=True)
    
    # Metrics
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    pipeline_request = relationship("NovaPipelineRequest", back_populates="lane_results")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("pipeline_request_id", "lane", name="uq_lane_per_request"),
        Index("ix_lane_results_request", "pipeline_request_id"),
        Index("ix_lane_results_lane", "lane"),
        Index("ix_lane_results_status", "status"),
    )


# ============================================================================
# INTENT ANALYSIS (Lane A)
# ============================================================================

class IntentAnalysis(Base):
    """
    Result of Lane A: Intent Analysis.
    
    Parses user input to understand what they want to do.
    """
    __tablename__ = "intent_analyses"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False, unique=True)
    
    # Intent classification
    intent_type = Column(SQLEnum(IntentType), nullable=False)
    intent_confidence = Column(Float, nullable=False)  # 0.0 - 1.0
    urgency = Column(SQLEnum(IntentUrgency), nullable=False, default=IntentUrgency.NORMAL)
    
    # Extracted entities
    entities = Column(JSON, nullable=True)  # {type: [values]}
    keywords = Column(JSON, nullable=True)  # Key terms
    
    # Target detection
    target_sphere = Column(String(50), nullable=True)
    target_thread_id = Column(PGUUID(as_uuid=True), nullable=True)
    target_agent = Column(String(100), nullable=True)
    
    # Action analysis
    primary_action = Column(String(100), nullable=True)
    secondary_actions = Column(JSON, nullable=True)  # List of actions
    
    # Sensitivity assessment
    is_sensitive = Column(Boolean, nullable=False, default=False)
    sensitivity_reasons = Column(JSON, nullable=True)  # Why it's sensitive
    requires_confirmation = Column(Boolean, nullable=False, default=False)
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("ix_intent_type", "intent_type"),
        Index("ix_intent_sensitive", "is_sensitive"),
    )


# ============================================================================
# CONTEXT SNAPSHOT (Lane B)
# ============================================================================

class ContextSnapshot(Base):
    """
    Result of Lane B: Context Snapshot.
    
    Captures the current state relevant to the request.
    """
    __tablename__ = "context_snapshots"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False, unique=True)
    
    # Thread context
    thread_snapshot = Column(JSON, nullable=True)  # Thread state at time of request
    thread_event_count = Column(Integer, nullable=True)
    thread_last_event_type = Column(String(50), nullable=True)
    
    # Sphere context
    sphere_snapshot = Column(JSON, nullable=True)  # Sphere state
    active_agents = Column(JSON, nullable=True)  # List of active agents
    
    # User context
    user_preferences = Column(JSON, nullable=True)
    user_recent_actions = Column(JSON, nullable=True)  # Last N actions
    user_session_context = Column(JSON, nullable=True)
    
    # Conversation context
    conversation_history = Column(JSON, nullable=True)  # Recent messages
    conversation_summary = Column(Text, nullable=True)
    
    # Memory context (from tri-layer)
    hot_memory = Column(JSON, nullable=True)  # Immediate context
    warm_memory_summary = Column(Text, nullable=True)  # Recent summary
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# ============================================================================
# GOVERNANCE CHECK (Lane D)
# ============================================================================

class GovernanceCheckResult(Base):
    """
    Result of Lane D: Governance Check.
    
    Verifies rules, permissions, and determines if checkpoint is needed.
    """
    __tablename__ = "governance_check_results"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False, unique=True)
    
    # Decision
    action = Column(SQLEnum(GovernanceAction), nullable=False)
    
    # Permission checks
    has_sphere_access = Column(Boolean, nullable=False, default=True)
    has_thread_access = Column(Boolean, nullable=False, default=True)
    has_agent_access = Column(Boolean, nullable=False, default=True)
    has_action_permission = Column(Boolean, nullable=False, default=True)
    
    # Rule checks
    rules_checked = Column(JSON, nullable=True)  # List of rules checked
    rules_violated = Column(JSON, nullable=True)  # List of violations
    
    # Budget checks
    within_token_budget = Column(Boolean, nullable=False, default=True)
    estimated_tokens = Column(Integer, nullable=True)
    available_budget = Column(Integer, nullable=True)
    
    # Checkpoint triggers
    checkpoint_required = Column(Boolean, nullable=False, default=False)
    checkpoint_type = Column(String(50), nullable=True)
    checkpoint_reason = Column(Text, nullable=True)
    checkpoint_options = Column(JSON, nullable=True)  # approve, reject, modify
    
    # Cross-sphere check (Rule #3)
    is_cross_sphere = Column(Boolean, nullable=False, default=False)
    source_sphere = Column(String(50), nullable=True)
    target_sphere = Column(String(50), nullable=True)
    cross_sphere_workflow_id = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Identity boundary check
    identity_boundary_ok = Column(Boolean, nullable=False, default=True)
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("ix_governance_action", "action"),
        Index("ix_governance_checkpoint_required", "checkpoint_required"),
    )


# ============================================================================
# EXECUTION RECORD (Lane F)
# ============================================================================

class NovaExecutionRecord(Base):
    """
    Result of Lane F: Execution.
    
    Records the actual execution of the request after all checks pass.
    """
    __tablename__ = "nova_execution_records"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False, unique=True)
    
    # Execution type
    execution_type = Column(String(50), nullable=False)  # llm, agent, action, etc.
    
    # LLM details (if applicable)
    llm_provider = Column(String(50), nullable=True)
    llm_model = Column(String(100), nullable=True)
    llm_request = Column(JSON, nullable=True)  # Sanitized request
    llm_response = Column(JSON, nullable=True)  # Sanitized response
    
    # Agent details (if applicable)
    agent_id = Column(PGUUID(as_uuid=True), nullable=True)
    agent_name = Column(String(100), nullable=True)
    agent_execution_id = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Action details (if applicable)
    action_type = Column(String(100), nullable=True)
    action_target = Column(JSON, nullable=True)
    action_result = Column(JSON, nullable=True)
    
    # Thread events created
    events_created = Column(JSON, nullable=True)  # List of event IDs
    events_count = Column(Integer, nullable=False, default=0)
    
    # Metrics
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    
    # Success tracking
    success = Column(Boolean, nullable=False, default=True)
    error_message = Column(Text, nullable=True)
    
    # Traceability
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    executed_by = Column(PGUUID(as_uuid=True), nullable=False)  # User who triggered
    
    # Indexes
    __table_args__ = (
        Index("ix_execution_type", "execution_type"),
        Index("ix_execution_success", "success"),
        Index("ix_execution_llm", "llm_provider", "llm_model"),
    )


# ============================================================================
# AUDIT RECORD (Lane G)
# ============================================================================

class NovaAuditRecord(Base):
    """
    Result of Lane G: Audit.
    
    Comprehensive audit record for the entire pipeline execution.
    """
    __tablename__ = "nova_audit_records"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    pipeline_request_id = Column(PGUUID(as_uuid=True), ForeignKey("nova_pipeline_requests.id"), nullable=False, unique=True)
    identity_id = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Request summary
    request_type = Column(String(50), nullable=False)
    request_summary = Column(Text, nullable=False)
    
    # Processing summary
    lanes_executed = Column(JSON, nullable=False)  # List of lanes that ran
    total_duration_ms = Column(Integer, nullable=False)
    
    # Outcome
    outcome = Column(String(50), nullable=False)  # completed, rejected, failed, cancelled
    outcome_reason = Column(Text, nullable=True)
    
    # Checkpoint audit
    checkpoint_triggered = Column(Boolean, nullable=False, default=False)
    checkpoint_outcome = Column(String(50), nullable=True)  # approved, rejected
    checkpoint_duration_ms = Column(Integer, nullable=True)  # Time to approval
    
    # Resource usage
    total_tokens = Column(Integer, nullable=True)
    total_cost = Column(Float, nullable=True)
    
    # Changes made
    threads_affected = Column(JSON, nullable=True)  # List of thread IDs
    events_created = Column(JSON, nullable=True)  # List of event IDs
    data_modified = Column(JSON, nullable=True)  # Summary of changes
    
    # Security audit
    permissions_used = Column(JSON, nullable=True)
    sensitive_data_accessed = Column(Boolean, nullable=False, default=False)
    cross_sphere_operations = Column(JSON, nullable=True)
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index("ix_audit_identity", "identity_id"),
        Index("ix_audit_outcome", "outcome"),
        Index("ix_audit_created", "created_at"),
        Index("ix_audit_checkpoint", "checkpoint_triggered"),
    )


# ============================================================================
# NOVA METRICS (Aggregated)
# ============================================================================

class NovaMetrics(Base):
    """
    Aggregated metrics for Nova pipeline performance.
    
    Updated periodically to track system health.
    """
    __tablename__ = "nova_metrics"
    
    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Time period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    period_type = Column(String(20), nullable=False)  # hourly, daily, weekly
    
    # Request metrics
    total_requests = Column(Integer, nullable=False, default=0)
    completed_requests = Column(Integer, nullable=False, default=0)
    failed_requests = Column(Integer, nullable=False, default=0)
    cancelled_requests = Column(Integer, nullable=False, default=0)
    
    # Checkpoint metrics
    checkpoints_triggered = Column(Integer, nullable=False, default=0)
    checkpoints_approved = Column(Integer, nullable=False, default=0)
    checkpoints_rejected = Column(Integer, nullable=False, default=0)
    avg_checkpoint_duration_ms = Column(Float, nullable=True)
    
    # Performance metrics
    avg_processing_time_ms = Column(Float, nullable=True)
    p50_processing_time_ms = Column(Float, nullable=True)
    p95_processing_time_ms = Column(Float, nullable=True)
    p99_processing_time_ms = Column(Float, nullable=True)
    
    # Lane metrics
    lane_metrics = Column(JSON, nullable=True)  # Per-lane stats
    
    # Resource metrics
    total_tokens = Column(Integer, nullable=False, default=0)
    total_cost = Column(Float, nullable=False, default=0.0)
    
    # Intent distribution
    intent_distribution = Column(JSON, nullable=True)  # {type: count}
    
    # Error metrics
    error_count = Column(Integer, nullable=False, default=0)
    error_distribution = Column(JSON, nullable=True)  # {error_code: count}
    
    # Traceability
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("period_start", "period_type", name="uq_nova_metrics_period"),
        Index("ix_metrics_period", "period_start", "period_end"),
    )
