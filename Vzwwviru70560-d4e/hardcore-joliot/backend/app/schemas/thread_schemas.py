"""
CHE·NU™ Thread Schemas

Pydantic models for Thread requests and responses.

Thread = Append-Only Event Log
- Events are IMMUTABLE
- Corrections via NEW events
- Never update, never delete
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadStatusEnum(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ThreadTypeEnum(str, Enum):
    PERSONAL = "personal"
    COLLECTIVE = "collective"
    INSTITUTIONAL = "institutional"


class ThreadVisibilityEnum(str, Enum):
    PRIVATE = "private"
    SEMI_PRIVATE = "semi_private"
    PUBLIC = "public"


class ThreadEventTypeEnum(str, Enum):
    # Lifecycle
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_ARCHIVED = "thread.archived"
    THREAD_RESUMED = "thread.resumed"
    THREAD_COMPLETED = "thread.completed"
    
    # Intent
    INTENT_DECLARED = "intent.declared"
    INTENT_REFINED = "intent.refined"
    
    # Decisions
    DECISION_RECORDED = "decision.recorded"
    DECISION_REVISED = "decision.revised"
    
    # Actions
    ACTION_CREATED = "action.created"
    ACTION_UPDATED = "action.updated"
    ACTION_COMPLETED = "action.completed"
    ACTION_CANCELLED = "action.cancelled"
    
    # Memory
    NOTE_ADDED = "note.added"
    SUMMARY_SNAPSHOT = "summary.snapshot"
    MEMORY_COMPRESSED = "memory.compressed"
    
    # Links
    LINK_ADDED = "link.added"
    THREAD_REFERENCED = "thread.referenced"
    FILE_ATTACHED = "file.attached"
    
    # Governance
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"


class ActionStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class ActionPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadCreate(BaseModel):
    """Create a new thread."""
    
    sphere_id: str = Field(..., description="Sphere this thread belongs to")
    founding_intent: str = Field(
        ..., 
        min_length=10, 
        max_length=2000,
        description="The founding intention (IMMUTABLE after creation)",
    )
    title: Optional[str] = Field(None, max_length=255, description="Display title")
    thread_type: ThreadTypeEnum = ThreadTypeEnum.PERSONAL
    visibility: ThreadVisibilityEnum = ThreadVisibilityEnum.PRIVATE
    tags: List[str] = []
    parent_thread_id: Optional[str] = None
    metadata: dict = {}


class ThreadSummary(BaseModel):
    """Thread summary for list views."""
    
    id: str
    sphere_id: str
    title: Optional[str] = None
    founding_intent: str
    current_intent: Optional[str] = None
    type: ThreadTypeEnum
    status: ThreadStatusEnum
    visibility: ThreadVisibilityEnum
    tags: List[str] = []
    event_count: int = 0
    decision_count: int = 0
    action_count: int = 0
    pending_action_count: int = 0
    created_at: datetime
    last_event_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ThreadResponse(ThreadSummary):
    """Full thread response."""
    
    identity_id: str
    parent_thread_id: Optional[str] = None
    created_by: str
    updated_at: datetime
    metadata: dict = {}


class ThreadUpdate(BaseModel):
    """Update thread metadata (NOT founding_intent)."""
    
    title: Optional[str] = Field(None, max_length=255)
    tags: Optional[List[str]] = None
    visibility: Optional[ThreadVisibilityEnum] = None
    metadata: Optional[dict] = None


# ═══════════════════════════════════════════════════════════════════════════════
# EVENT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class EventCreate(BaseModel):
    """Create a new event (append to thread)."""
    
    event_type: ThreadEventTypeEnum
    payload: dict = {}
    summary: Optional[str] = Field(None, max_length=500)
    source: str = "user"


class EventResponse(BaseModel):
    """Event response."""
    
    id: str
    thread_id: str
    sequence_number: int
    parent_event_id: Optional[str] = None
    event_type: ThreadEventTypeEnum
    payload: dict
    summary: Optional[str] = None
    source: str
    agent_id: Optional[str] = None
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """List of events with pagination."""
    
    events: List[EventResponse]
    total: int
    has_more: bool


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionCreate(BaseModel):
    """Record a new decision."""
    
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = None
    rationale: Optional[str] = None
    options_considered: List[dict] = []
    chosen_option: Optional[int] = None
    tags: List[str] = []


class DecisionResponse(BaseModel):
    """Decision response."""
    
    id: str
    thread_id: str
    event_id: str
    title: str
    description: Optional[str] = None
    rationale: Optional[str] = None
    options_considered: List[dict] = []
    chosen_option: Optional[int] = None
    tags: List[str] = []
    is_active: bool = True
    supersedes_id: Optional[str] = None
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


class DecisionListResponse(BaseModel):
    """List of decisions."""
    
    decisions: List[DecisionResponse]
    total: int


# ═══════════════════════════════════════════════════════════════════════════════
# ACTION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ActionCreate(BaseModel):
    """Create a new action."""
    
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    priority: ActionPriorityEnum = ActionPriorityEnum.MEDIUM
    due_date: Optional[datetime] = None
    assignee_id: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}


class ActionResponse(BaseModel):
    """Action response."""
    
    id: str
    thread_id: str
    event_id: str
    title: str
    description: Optional[str] = None
    status: ActionStatusEnum
    priority: ActionPriorityEnum
    due_date: Optional[datetime] = None
    assignee_id: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    created_by: str
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ActionUpdate(BaseModel):
    """Update action (creates an event)."""
    
    status: Optional[ActionStatusEnum] = None
    priority: Optional[ActionPriorityEnum] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[str] = None


class ActionListResponse(BaseModel):
    """List of actions."""
    
    actions: List[ActionResponse]
    total: int
    pending_count: int


# ═══════════════════════════════════════════════════════════════════════════════
# SNAPSHOT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class SnapshotCreate(BaseModel):
    """Create a snapshot."""
    
    summary: Optional[str] = Field(None, max_length=2000)
    snapshot_type: str = "manual"


class SnapshotResponse(BaseModel):
    """Snapshot response."""
    
    id: str
    thread_id: str
    event_id: str
    sequence_number: int
    snapshot_type: str
    summary: Optional[str] = None
    key_decisions: List[str] = []
    active_actions: List[str] = []
    state: dict
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════════════
# INTENT REFINEMENT
# ═══════════════════════════════════════════════════════════════════════════════

class IntentRefinement(BaseModel):
    """Refine thread intent (creates intent.refined event)."""
    
    refined_intent: str = Field(..., min_length=10, max_length=2000)
    reason: Optional[str] = Field(None, max_length=500)


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT (GOVERNANCE)
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointRequired(BaseModel):
    """Checkpoint response when action requires approval."""
    
    checkpoint_id: str
    checkpoint_type: str
    reason: str
    options: List[str] = ["approve", "reject"]
    event_id: Optional[str] = None
    thread_id: str


# ═══════════════════════════════════════════════════════════════════════════════
# LIST RESPONSES
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadListResponse(BaseModel):
    """List of threads with pagination."""
    
    threads: List[ThreadSummary]
    total: int
    page: int
    page_size: int
    total_pages: int


# ═══════════════════════════════════════════════════════════════════════════════
# PAGINATION
# ═══════════════════════════════════════════════════════════════════════════════

class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size
