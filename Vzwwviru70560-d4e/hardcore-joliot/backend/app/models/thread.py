"""
CHE·NU™ Thread Models

SQLAlchemy models for the Thread V2 system.

╔══════════════════════════════════════════════════════════════════════════════╗
║  THREAD V2 — CORE PRINCIPLES (NON-NEGOTIABLE)                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  1. APPEND-ONLY: Events are IMMUTABLE. Never update, never delete.          ║
║  2. SINGLE SOURCE: Thread IS the truth. Everything else is projection.      ║
║  3. CAUSAL ORDER: Events reference parent for deterministic ordering.       ║
║  4. IDENTITY BOUND: Each thread belongs to ONE identity. No cross-access.   ║
║  5. FOUNDING INTENT: The original intent is FROZEN forever.                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4
from enum import Enum

from sqlalchemy import (
    String, Boolean, DateTime, Text, JSON, Integer, 
    ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadStatus(str, Enum):
    """Thread lifecycle status."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ThreadType(str, Enum):
    """Thread type."""
    PERSONAL = "personal"
    COLLECTIVE = "collective"
    INSTITUTIONAL = "institutional"


class ThreadVisibility(str, Enum):
    """Thread visibility scope."""
    PRIVATE = "private"
    SEMI_PRIVATE = "semi_private"
    PUBLIC = "public"


class ThreadEventType(str, Enum):
    """
    All possible event types in a Thread.
    
    Events are the IMMUTABLE building blocks of threads.
    """
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
    
    # XR
    ENV_BLUEPRINT_GENERATED = "env.blueprint.generated"
    
    # Live
    LIVE_STARTED = "live.started"
    LIVE_ENDED = "live.ended"
    
    # Governance
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"
    
    # Agent
    AGENT_ASSIGNED = "agent.assigned"
    AGENT_REMOVED = "agent.removed"
    AGENT_EXECUTED = "agent.executed"


class ActionStatus(str, Enum):
    """Status of an action within a thread."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class ActionPriority(str, Enum):
    """Priority level for actions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Thread(Base):
    """
    Thread - The core object of CHE·NU.
    
    A Thread is an APPEND-ONLY event log representing an intention,
    project, or activity. It is the SINGLE SOURCE OF TRUTH.
    
    ⚠️ IMMUTABLE RULES:
    - founding_intent CANNOT be changed after creation
    - Events CANNOT be modified or deleted
    - The Thread itself stores metadata; events store history
    """
    
    __tablename__ = "threads"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PRIMARY IDENTIFIERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Identity boundary - CRITICAL for data isolation
    identity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
    )
    
    # Parent sphere
    sphere_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("spheres.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREAD HIERARCHY
    # ═══════════════════════════════════════════════════════════════════════════
    
    parent_thread_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("threads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CORE CONTENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    # IMMUTABLE - Set once, never changed
    founding_intent: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Mutable title (for display)
    title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Current refined intent (updated via events)
    current_intent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CLASSIFICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    thread_type: Mapped[ThreadType] = mapped_column(
        default=ThreadType.PERSONAL,
        nullable=False,
    )
    
    status: Mapped[ThreadStatus] = mapped_column(
        default=ThreadStatus.ACTIVE,
        nullable=False,
        index=True,
    )
    
    visibility: Mapped[ThreadVisibility] = mapped_column(
        default=ThreadVisibility.PRIVATE,
        nullable=False,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TAGS & METADATA
    # ═══════════════════════════════════════════════════════════════════════════
    
    tags: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    event_metadata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COUNTERS (Cached, derived from events)
    # ═══════════════════════════════════════════════════════════════════════════
    
    event_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    decision_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    action_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    pending_action_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMESTAMPS
    # ═══════════════════════════════════════════════════════════════════════════
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    last_event_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    archived_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ═══════════════════════════════════════════════════════════════════════════
    
    events: Mapped[List["ThreadEvent"]] = relationship(
        "ThreadEvent",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="ThreadEvent.sequence_number",
    )
    
    actions: Mapped[List["ThreadAction"]] = relationship(
        "ThreadAction",
        back_populates="thread",
        cascade="all, delete-orphan",
    )
    
    decisions: Mapped[List["ThreadDecision"]] = relationship(
        "ThreadDecision",
        back_populates="thread",
        cascade="all, delete-orphan",
    )
    
    # Self-referential for hierarchy
    children: Mapped[List["Thread"]] = relationship(
        "Thread",
        back_populates="parent",
        remote_side=[id],
    )
    
    parent: Mapped[Optional["Thread"]] = relationship(
        "Thread",
        back_populates="children",
        remote_side=[parent_thread_id],
    )
    
    # Owner identity
    identity = relationship("User", back_populates="threads")
    
    # Governance checkpoints for this thread
    checkpoints = relationship(
        "GovernanceCheckpoint",
        back_populates="thread",
        lazy="dynamic"
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INDEXES
    # ═══════════════════════════════════════════════════════════════════════════
    
    __table_args__ = (
        Index("ix_threads_identity_sphere", "identity_id", "sphere_id"),
        Index("ix_threads_identity_status", "identity_id", "status"),
        Index("ix_threads_last_event", "identity_id", "last_event_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Thread {self.id[:8]}... ({self.status.value})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "identity_id": self.identity_id,
            "sphere_id": self.sphere_id,
            "parent_thread_id": self.parent_thread_id,
            "founding_intent": self.founding_intent,
            "title": self.title,
            "current_intent": self.current_intent or self.founding_intent,
            "type": self.thread_type.value,
            "status": self.status.value,
            "visibility": self.visibility.value,
            "tags": self.tags,
            "event_count": self.event_count,
            "decision_count": self.decision_count,
            "action_count": self.action_count,
            "pending_action_count": self.pending_action_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_event_at": self.last_event_at.isoformat() if self.last_event_at else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENT MODEL (IMMUTABLE)
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadEvent(Base):
    """
    Thread Event - IMMUTABLE event in a thread's history.
    
    ⚠️ CRITICAL RULES:
    - NEVER update an event after creation
    - NEVER delete an event
    - Corrections are made by adding NEW events
    
    This is the core of the append-only architecture.
    """
    
    __tablename__ = "thread_events"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Parent thread
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Sequence for ordering (monotonically increasing)
    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    # Causal ordering - reference to parent event
    parent_event_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("thread_events.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Event type
    event_type: Mapped[ThreadEventType] = mapped_column(
        nullable=False,
        index=True,
    )
    
    # Event payload (JSONB for efficient querying)
    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    
    # Summary for display
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Source of the event
    source: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )
    
    # Agent that created this event (if any)
    agent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
    )
    
    # Timestamp (IMMUTABLE)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    # Who created this event
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    # Relationship
    thread: Mapped["Thread"] = relationship(
        "Thread",
        back_populates="events",
    )
    
    # Indexes
    __table_args__ = (
        Index("ix_thread_events_thread_seq", "thread_id", "sequence_number"),
        Index("ix_thread_events_type", "thread_id", "event_type"),
        # Ensure sequence numbers are unique per thread
        Index(
            "uq_thread_events_thread_seq",
            "thread_id", "sequence_number",
            unique=True,
        ),
    )
    
    def __repr__(self) -> str:
        return f"<ThreadEvent {self.event_type.value} #{self.sequence_number}>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "sequence_number": self.sequence_number,
            "parent_event_id": self.parent_event_id,
            "event_type": self.event_type.value,
            "payload": self.payload,
            "summary": self.summary,
            "source": self.source,
            "agent_id": self.agent_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD DECISION MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadDecision(Base):
    """
    Decision recorded in a thread.
    
    Decisions are derived from DECISION_RECORDED events.
    This model provides a queryable view of decisions.
    """
    
    __tablename__ = "thread_decisions"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Link to the event that created this decision
    event_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("thread_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Decision content
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    rationale: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Options that were considered
    options_considered: Mapped[List[dict]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # The chosen option index (if options were provided)
    chosen_option: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Tags
    tags: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # Is this decision still valid?
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Revision (if this supersedes another decision)
    supersedes_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("thread_decisions.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    # Relationship
    thread: Mapped["Thread"] = relationship(
        "Thread",
        back_populates="decisions",
    )
    
    def __repr__(self) -> str:
        return f"<ThreadDecision {self.title[:30]}...>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "rationale": self.rationale,
            "options_considered": self.options_considered,
            "chosen_option": self.chosen_option,
            "tags": self.tags,
            "is_active": self.is_active,
            "supersedes_id": self.supersedes_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD ACTION MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadAction(Base):
    """
    Action item in a thread.
    
    Actions are derived from ACTION_CREATED events.
    Status changes create new events (append-only).
    """
    
    __tablename__ = "thread_actions"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Link to the event that created this action
    event_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("thread_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Action content
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Status (updated via events)
    status: Mapped[ActionStatus] = mapped_column(
        default=ActionStatus.PENDING,
        nullable=False,
        index=True,
    )
    
    priority: Mapped[ActionPriority] = mapped_column(
        default=ActionPriority.MEDIUM,
        nullable=False,
    )
    
    # Due date
    due_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # Assignee (if any)
    assignee_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
    )
    
    # Tags
    tags: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # Metadata
    event_metadata: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # Relationship
    thread: Mapped["Thread"] = relationship(
        "Thread",
        back_populates="actions",
    )
    
    # Index for pending actions
    __table_args__ = (
        Index("ix_thread_actions_status", "thread_id", "status"),
        Index("ix_thread_actions_due", "thread_id", "due_date"),
    )
    
    def __repr__(self) -> str:
        return f"<ThreadAction {self.title[:30]}... ({self.status.value})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "assignee_id": self.assignee_id,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SNAPSHOT MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadSnapshot(Base):
    """
    Point-in-time snapshot of thread state.
    
    Used for:
    - Memory compression (warm → cold)
    - Quick state retrieval
    - XR environment generation
    """
    
    __tablename__ = "thread_snapshots"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Link to the event that triggered this snapshot
    event_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("thread_events.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Snapshot at this sequence number
    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    # Snapshot type
    snapshot_type: Mapped[str] = mapped_column(
        String(50),
        default="summary",
        nullable=False,
    )
    
    # Snapshot content
    state: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )
    
    # Summary text
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Key decisions at this point
    key_decisions: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # Active actions at this point
    active_actions: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<ThreadSnapshot #{self.sequence_number} ({self.snapshot_type})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "event_id": self.event_id,
            "sequence_number": self.sequence_number,
            "snapshot_type": self.snapshot_type,
            "state": self.state,
            "summary": self.summary,
            "key_decisions": self.key_decisions,
            "active_actions": self.active_actions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
