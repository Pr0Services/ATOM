"""
SCHEMA: governance_schemas.py
VERSION: 1.0.0
INTENT: Pydantic schemas for AT-OM Governance Multi-Agent System

R&D COMPLIANCE: ✅
- Rule #1: Human Sovereignty - All schemas support human approval flows
- Rule #6: Traceability - All objects have id, created_at, created_by
"""

from typing import Optional, List, Dict, Any, Literal
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class GovernanceSignalLevel(str, Enum):
    """Signal levels emitted by CEAs to Orchestrator."""
    WARN = "WARN"           # Annotate and continue
    CORRECT = "CORRECT"     # Inject local instruction (patch)
    PAUSE = "PAUSE"         # Halt executor output until clarified
    BLOCK = "BLOCK"         # Stop and require human approval
    ESCALATE = "ESCALATE"   # Invoke specialist for segment


class GovernanceCriterion(str, Enum):
    """Criteria that CEAs enforce."""
    CANON = "canon"                 # Thread rules (append-only, no duplicate memory)
    SCHEMA = "schema"               # JSON/schema validation
    SECURITY = "security"           # Security invariants
    COHERENCE = "coherence"         # Contradictions/drift from intent
    STYLE = "style"                 # Formatting, clarity
    BUDGET = "budget"               # Token/cost limits
    LATENCY = "latency"             # Response time limits
    COMPLIANCE = "compliance"       # Legal/regulatory compliance


class SpecCategory(str, Enum):
    """Categories for specification checks."""
    CORRECTNESS = "correctness"
    SAFETY = "safety"
    COHERENCE = "coherence"
    STYLE = "style"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"
    COST = "cost"


class BacklogType(str, Enum):
    """Types of backlog items for learning."""
    ERROR = "error"                 # Defects that escaped checks
    SIGNAL = "signal"               # False positives / noisy checkers
    DECISION = "decision"           # Decision outcomes
    COST = "cost"                   # Compute and latency tracking
    GOVERNANCE_DEBT = "governance_debt"  # Structural issues


class BacklogStatus(str, Enum):
    """Status of backlog items."""
    OPEN = "open"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    WONT_FIX = "wont_fix"


class OrchestratorDecision(str, Enum):
    """Decisions the orchestrator can make."""
    RUN_SPEC = "RUN_SPEC"           # Run a specification check
    DEFER = "DEFER"                 # Defer check to later
    ESCALATE = "ESCALATE"           # Escalate to specialist
    PATCH_INSTRUCTION = "PATCH_INSTRUCTION"  # Inject correction
    BLOCK = "BLOCK"                 # Block execution
    ASK_HUMAN = "ASK_HUMAN"         # Request human approval


class ExecutionMode(str, Enum):
    """Execution modes affecting governance decisions."""
    LIVE = "live"           # Real-time, latency-sensitive
    ASYNC = "async"         # Background, quality-focused


class AgentConfiguration(str, Enum):
    """Agent configurations for QCT algorithm."""
    CONFIG_A = "A"  # 1 cheap executor + light CEAs
    CONFIG_B = "B"  # 1 strong executor + light CEAs
    CONFIG_C = "C"  # 1 strong executor + 1 cheap critic + CEAs
    CONFIG_D = "D"  # 1 strong executor + 1 strong critic + CEAs
    CONFIG_E = "E"  # 2 strong workers (parallel) + CEAs (critical only)


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

class SignalScope(BaseModel):
    """Scope of a governance signal."""
    segment_id: Optional[str] = None
    region: Optional[str] = None
    event_ids: Optional[List[str]] = None


class GovernanceSignal(BaseModel):
    """Signal emitted by CEAs to orchestrator."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    level: GovernanceSignalLevel
    criterion: GovernanceCriterion
    message: str
    scope: Optional[SignalScope] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    cea_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "sig_123",
                "level": "CORRECT",
                "criterion": "coherence",
                "message": "Detected contradiction with founding intent",
                "scope": {"segment_id": "seg_12", "region": "paragraph_3"},
                "confidence": 0.82,
                "cea_id": "CoherenceGuardCEA"
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class SpecTriggers(BaseModel):
    """Conditions that trigger a specification check."""
    always_on: bool = False
    on_event_types: Optional[List[str]] = None
    on_segment_criticality_above: Optional[float] = None
    on_cea_signal: Optional[GovernanceSignalLevel] = None


class Spec(BaseModel):
    """A specification check policy."""
    id: str
    name: str
    category: SpecCategory
    cost_level: int = Field(ge=1, le=5)
    latency_level: int = Field(ge=1, le=5)
    risk_coverage: List[str]
    triggers: SpecTriggers
    cooldown: int = 0  # seconds between runs
    output: Literal["signal", "patch", "block"]
    owner_agent: str
    enabled: bool = True
    last_run_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "CANON_GUARD",
                "name": "Canonical Thread Guard",
                "category": "safety",
                "cost_level": 1,
                "latency_level": 1,
                "risk_coverage": ["duplicate_memory", "append_only_violation"],
                "triggers": {"always_on": True},
                "cooldown": 0,
                "output": "block",
                "owner_agent": "CanonGuardCEA"
            }
        }


class SpecRunResult(BaseModel):
    """Result of running a specification check."""
    spec_id: str
    passed: bool
    signals: List[GovernanceSignal] = []
    cost_estimate: float = 0.0
    latency_ms: float = 0.0
    scope: Optional[SignalScope] = None
    run_at: datetime = Field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# PATCH INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class PatchInstruction(BaseModel):
    """Corrective instruction from orchestrator to executor."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    scope: SignalScope
    constraint: str  # What must hold
    correction: str  # What to change
    rationale: str
    verification_spec_id: str  # Which spec confirms the fix
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# QUALITY/COST TARGETING (QCT)
# ═══════════════════════════════════════════════════════════════════════════════

class SegmentScores(BaseModel):
    """Scores for a segment used in QCT algorithm."""
    criticality: float = Field(ge=0.0, le=1.0, alias="C")
    complexity: float = Field(ge=0.0, le=1.0, alias="X")
    exposure: float = Field(ge=0.0, le=1.0, alias="E")
    irreversibility: float = Field(ge=0.0, le=1.0, alias="R")
    uncertainty: float = Field(ge=0.0, le=1.0, alias="U")
    segment_size: float = Field(ge=0.0, le=1.0, alias="S")
    
    class Config:
        populate_by_name = True


class Budgets(BaseModel):
    """Budget constraints for orchestration."""
    cost_remaining: float = Field(ge=0.0)  # Tokens/credits remaining
    latency_budget_ms: float = Field(ge=0.0)  # Max latency allowed
    mode: ExecutionMode = ExecutionMode.ASYNC


class QCTResult(BaseModel):
    """Result of Quality/Cost Targeting algorithm."""
    required_quality: float = Field(ge=0.0, le=1.0)
    expected_error_rate: float = Field(ge=0.0, le=1.0)
    selected_config: AgentConfiguration
    specs_to_run: List[str]
    estimated_cost: float
    estimated_latency_ms: float
    rationale: str


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR DECISIONS
# ═══════════════════════════════════════════════════════════════════════════════

class OrchDecisionPayload(BaseModel):
    """Payload for ORCH_DECISION_MADE event."""
    decision: OrchestratorDecision
    reason: str
    budgets: Budgets
    signals: List[GovernanceSignal] = []
    scope: Optional[SignalScope] = None
    config_selected: Optional[AgentConfiguration] = None
    specs_scheduled: Optional[List[str]] = None
    patch_instruction: Optional[PatchInstruction] = None


class EscalationPayload(BaseModel):
    """Payload for ESCALATION_TRIGGERED event."""
    to_agent: str
    scope: SignalScope
    reason: str
    required_quality: float = Field(ge=0.0, le=1.0)
    triggering_signals: List[str] = []


class SpecDeferredPayload(BaseModel):
    """Payload for SPEC_DEFERRED event."""
    spec_id: str
    defer_to: Literal["post_live", "next_turn", "scheduled"]
    reason: str
    scheduled_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
# BACKLOGS
# ═══════════════════════════════════════════════════════════════════════════════

class BacklogReferences(BaseModel):
    """References to related entities."""
    thread_id: str
    event_ids: List[str] = []
    spec_ids: List[str] = []
    segment_ids: List[str] = []


class BacklogMetrics(BaseModel):
    """Metrics associated with a backlog item."""
    fix_tokens: Optional[int] = None
    fix_time_seconds: Optional[float] = None
    escape_depth: Optional[Literal["early", "mid", "late"]] = None
    false_positive_rate: Optional[float] = None
    cost_estimate_vs_actual: Optional[Dict[str, float]] = None


class BacklogItemCreate(BaseModel):
    """Schema for creating a backlog item."""
    backlog_type: BacklogType
    severity: Optional[Literal["S1", "S2", "S3", "S4", "S5"]] = None
    title: Optional[str] = None
    description: str
    segment_id: Optional[str] = None
    references: Optional[BacklogReferences] = None
    metrics: Optional[BacklogMetrics] = None


class BacklogItem(BacklogItemCreate):
    """Full backlog item with metadata."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    status: BacklogStatus = BacklogStatus.OPEN
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "bl_123",
                "backlog_type": "error",
                "severity": "S3",
                "title": "Schema mismatch in XR blueprint",
                "description": "Blueprint item missing required field",
                "references": {
                    "thread_id": "th_456",
                    "event_ids": ["ev_789"]
                },
                "metrics": {
                    "fix_tokens": 1200,
                    "escape_depth": "late"
                },
                "status": "open"
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE EVENT PAYLOADS (for Thread Event System)
# ═══════════════════════════════════════════════════════════════════════════════

class GovernanceEventType(str, Enum):
    """Event types added by governance system."""
    ORCH_DECISION_MADE = "ORCH_DECISION_MADE"
    SPEC_RUN = "SPEC_RUN"
    SPEC_DEFERRED = "SPEC_DEFERRED"
    ESCALATION_TRIGGERED = "ESCALATION_TRIGGERED"
    GOVERNANCE_SIGNAL = "GOVERNANCE_SIGNAL"
    QUALITY_TARGET_SET = "QUALITY_TARGET_SET"
    THREAD_MATURITY_COMPUTED = "THREAD_MATURITY_COMPUTED"
    BACKLOG_ITEM_CREATED = "BACKLOG_ITEM_CREATED"
    PATCH_INSTRUCTION_APPLIED = "PATCH_INSTRUCTION_APPLIED"


class QualityTargetPayload(BaseModel):
    """Payload for QUALITY_TARGET_SET event."""
    target_level: float = Field(ge=0.0, le=1.0)
    reason: str
    scope: Optional[SignalScope] = None


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT CONTRACTS
# ═══════════════════════════════════════════════════════════════════════════════

class CEAContract(BaseModel):
    """Contract defining a Criterion Enforcement Agent."""
    id: str
    name: str
    criterion: GovernanceCriterion
    description: str
    specs_owned: List[str]
    always_on: bool = False
    cost_level: int = Field(ge=1, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "CanonGuardCEA",
                "name": "Canon Guard",
                "criterion": "canon",
                "description": "Enforces thread truths (append-only, no duplicate memory)",
                "specs_owned": ["CANON_GUARD"],
                "always_on": True,
                "cost_level": 1
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION POINT SYSTEM (Pending Actions with Aging Alerts)
# ═══════════════════════════════════════════════════════════════════════════════

class AgingLevel(str, Enum):
    """
    Time-based aging levels for pending decisions.
    
    Visual indicators:
    - GREEN:   Fresh, just created (0-24 hours)
    - YELLOW:  Needs attention (24h - 3 days)
    - RED:     Urgent (3-7 days)
    - BLINK:   Critical, blinking alert (7-10 days)
    - ARCHIVE: Auto-archived, out of active recall (>10 days)
    """
    GREEN = "green"      # 0-24 hours
    YELLOW = "yellow"    # 24h - 3 days
    RED = "red"          # 3-7 days
    BLINK = "blink"      # 7-10 days (critical, animated)
    ARCHIVE = "archive"  # >10 days (auto-archive)


class DecisionPointType(str, Enum):
    """Types of decision points requiring human action."""
    CONFIRMATION = "confirmation"    # User must confirm an action
    TASK = "task"                    # User must complete a task
    DECISION = "decision"            # User must make a choice
    CHECKPOINT = "checkpoint"        # Governance checkpoint (HTTP 423)
    APPROVAL = "approval"            # Approval required
    REVIEW = "review"                # Review required


class UserResponseType(str, Enum):
    """Types of user responses to decision points."""
    VALIDATE = "validate"        # Accept AI suggestion as-is
    REDIRECT = "redirect"        # Change direction
    COMMENT = "comment"          # Add comment/clarification
    DEFER = "defer"              # Defer decision
    REJECT = "reject"            # Reject suggestion


class AISuggestion(BaseModel):
    """
    Nova's AI suggestion for next step.
    
    R&D Rule #1: This is a SUGGESTION only. Human decides.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    summary: str                      # Brief summary of suggestion
    detailed_explanation: str         # Full explanation
    confidence: float = Field(ge=0.0, le=1.0)  # 0-1 confidence score
    suggested_action: str             # What Nova suggests to do
    alternatives: List[str] = []      # Alternative options
    rationale: str                    # Why this suggestion
    context_used: List[str] = []      # What context informed this
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "sug_123",
                "summary": "Sauvegarder dans Documents/Projets",
                "detailed_explanation": "Basé sur vos habitudes, ce fichier devrait aller dans Documents/Projets/CHE-NU",
                "confidence": 0.85,
                "suggested_action": "save_to_projects",
                "alternatives": ["save_to_downloads", "save_to_desktop", "custom_location"],
                "rationale": "3 fichiers similaires ont été sauvegardés ici récemment",
                "context_used": ["recent_saves", "file_type", "project_context"]
            }
        }


class DecisionPointCreate(BaseModel):
    """Schema for creating a decision point."""
    point_type: DecisionPointType
    thread_id: str
    title: str
    description: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    # Optional pre-generated suggestion
    suggestion: Optional[AISuggestion] = None
    
    # Source info
    source_event_id: Optional[str] = None
    source_module: Optional[str] = None
    
    # Urgency override (if not using time-based)
    urgency_override: Optional[AgingLevel] = None


class UserResponse(BaseModel):
    """User's response to a decision point."""
    response_type: UserResponseType
    comment: Optional[str] = None
    selected_alternative: Optional[str] = None  # If redirect, which alternative
    custom_action: Optional[str] = None         # If fully custom response
    responded_by: str
    responded_at: datetime = Field(default_factory=datetime.utcnow)


class DecisionPoint(BaseModel):
    """
    A pending decision point requiring human action.
    
    This is the core of the "intelligence alert" system.
    Nova suggests, human decides.
    
    R&D Compliance:
    - Rule #1: Human Sovereignty - User MUST act, Nova only suggests
    - Rule #6: Full traceability with created_by, responded_by
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    point_type: DecisionPointType
    thread_id: str
    
    # Content
    title: str
    description: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    # AI Suggestion (Nova's recommendation)
    suggestion: Optional[AISuggestion] = None
    
    # Aging
    aging_level: AgingLevel = AgingLevel.GREEN
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_reminded_at: Optional[datetime] = None
    reminder_count: int = 0
    
    # Status
    is_active: bool = True
    is_archived: bool = False
    archived_at: Optional[datetime] = None
    archive_reason: Optional[str] = None  # "timeout" | "manual" | "superseded"
    
    # Response
    user_response: Optional[UserResponse] = None
    
    # Source
    source_event_id: Optional[str] = None
    source_module: Optional[str] = None
    checkpoint_id: Optional[str] = None  # If linked to HTTP 423 checkpoint
    
    # Traceability
    created_by: str
    sphere_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "dp_123",
                "point_type": "confirmation",
                "thread_id": "th_456",
                "title": "Sauvegarder la photo?",
                "description": "Photo reçue dans la conversation",
                "suggestion": {
                    "summary": "Sauvegarder dans Photos/2026/Janvier",
                    "confidence": 0.82,
                    "suggested_action": "save_to_photos",
                    "alternatives": ["save_to_downloads", "share", "discard"]
                },
                "aging_level": "green",
                "is_active": True,
                "created_by": "user_789"
            }
        }


def compute_aging_level(created_at: datetime) -> AgingLevel:
    """
    Compute aging level based on time elapsed.
    
    GREEN:   0-24 hours
    YELLOW:  24h - 3 days
    RED:     3-7 days
    BLINK:   7-10 days
    ARCHIVE: >10 days
    """
    from datetime import timedelta
    
    now = datetime.utcnow()
    age = now - created_at
    
    if age <= timedelta(hours=24):
        return AgingLevel.GREEN
    elif age <= timedelta(days=3):
        return AgingLevel.YELLOW
    elif age <= timedelta(days=7):
        return AgingLevel.RED
    elif age <= timedelta(days=10):
        return AgingLevel.BLINK
    else:
        return AgingLevel.ARCHIVE


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "GovernanceSignalLevel",
    "GovernanceCriterion", 
    "SpecCategory",
    "BacklogType",
    "BacklogStatus",
    "OrchestratorDecision",
    "ExecutionMode",
    "AgentConfiguration",
    "GovernanceEventType",
    "AgingLevel",
    "DecisionPointType",
    "UserResponseType",
    
    # Models
    "SignalScope",
    "GovernanceSignal",
    "SpecTriggers",
    "Spec",
    "SpecRunResult",
    "PatchInstruction",
    "SegmentScores",
    "Budgets",
    "QCTResult",
    "OrchDecisionPayload",
    "EscalationPayload",
    "SpecDeferredPayload",
    "BacklogReferences",
    "BacklogMetrics",
    "BacklogItemCreate",
    "BacklogItem",
    "QualityTargetPayload",
    "CEAContract",
    "AISuggestion",
    "DecisionPointCreate",
    "UserResponse",
    "DecisionPoint",
    
    # Functions
    "compute_aging_level",
]
