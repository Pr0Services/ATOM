"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Base Database Models
═══════════════════════════════════════════════════════════════════════════════

Core SQLAlchemy models with R&D Rule #6 compliance (traceability).

All models include:
- id (UUID primary key)
- created_by (identity reference)
- created_at (timestamp)
- updated_at (timestamp)
"""

from datetime import datetime
from typing import Optional, Any
from uuid import uuid4, UUID
from sqlalchemy import (
    Column, String, DateTime, Text, Boolean, Integer, 
    ForeignKey, Enum as SQLEnum, JSON, Index, event
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum


# ═══════════════════════════════════════════════════════════════════════════════
# BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class Base(DeclarativeBase):
    """Base class for all CHE·NU models."""
    pass


class TimestampMixin:
    """
    Mixin for timestamp fields.
    
    R&D Rule #6: All entities must have created_at and updated_at.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class TraceabilityMixin(TimestampMixin):
    """
    Mixin for full traceability.
    
    R&D Rule #6: All entities must have id, created_by, created_at.
    """
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    created_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereType(str, enum.Enum):
    """The 9 CHE·NU spheres."""
    PERSONAL = "personal"
    BUSINESS = "business"
    CREATIVE_STUDIO = "creative_studio"
    ENTERTAINMENT = "entertainment"
    COMMUNITY = "community"
    SOCIAL = "social"
    SCHOLAR = "scholar"
    GOVERNMENT = "government"
    MY_TEAM = "my_team"


class ThreadStatus(str, enum.Enum):
    """Thread lifecycle status."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ThreadType(str, enum.Enum):
    """Thread ownership type."""
    PERSONAL = "personal"
    COLLECTIVE = "collective"
    INSTITUTIONAL = "institutional"


class Visibility(str, enum.Enum):
    """Content visibility levels."""
    PRIVATE = "private"
    SEMI_PRIVATE = "semi_private"
    PUBLIC = "public"


class CheckpointStatus(str, enum.Enum):
    """Checkpoint approval status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class CheckpointType(str, enum.Enum):
    """Types of checkpoints (R&D Rule #1)."""
    GOVERNANCE = "governance"
    COST = "cost"
    IDENTITY = "identity"
    SENSITIVE = "sensitive"
    CROSS_SPHERE = "cross_sphere"


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Identity(Base, TimestampMixin):
    """
    User identity model.
    
    R&D Rule #3: All data is scoped to an identity.
    """
    __tablename__ = "identities"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Authentication
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Settings
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Relationships
    threads: Mapped[list["Thread"]] = relationship(
        "Thread",
        back_populates="owner",
        foreign_keys="Thread.owner_identity_id"
    )
    
    __table_args__ = (
        Index("ix_identities_email", "email"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD MODEL (Event Sourcing)
# ═══════════════════════════════════════════════════════════════════════════════

class Thread(Base, TimestampMixin):
    """
    Thread model - the core object in CHE·NU.
    
    Threads are append-only event logs with derived snapshots.
    """
    __tablename__ = "threads"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # Ownership (R&D Rule #3)
    owner_identity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )
    
    # Core fields
    founding_intent: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Classification
    sphere: Mapped[SphereType] = mapped_column(
        SQLEnum(SphereType),
        nullable=False,
        index=True
    )
    thread_type: Mapped[ThreadType] = mapped_column(
        SQLEnum(ThreadType),
        default=ThreadType.PERSONAL
    )
    status: Mapped[ThreadStatus] = mapped_column(
        SQLEnum(ThreadStatus),
        default=ThreadStatus.ACTIVE,
        index=True
    )
    visibility: Mapped[Visibility] = mapped_column(
        SQLEnum(Visibility),
        default=Visibility.PRIVATE
    )
    
    # Hierarchy
    parent_thread_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("threads.id"),
        nullable=True
    )
    
    # Metadata
    tags: Mapped[list] = mapped_column(JSON, default=list)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    
    # Event count (for quick access)
    event_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    owner: Mapped["Identity"] = relationship(
        "Identity",
        back_populates="threads",
        foreign_keys=[owner_identity_id]
    )
    events: Mapped[list["ThreadEvent"]] = relationship(
        "ThreadEvent",
        back_populates="thread",
        order_by="ThreadEvent.sequence_number"
    )
    parent: Mapped[Optional["Thread"]] = relationship(
        "Thread",
        remote_side=[id],
        backref="children"
    )
    
    __table_args__ = (
        Index("ix_threads_owner_sphere", "owner_identity_id", "sphere"),
        Index("ix_threads_owner_status", "owner_identity_id", "status"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENT MODEL (Append-Only)
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadEventType(str, enum.Enum):
    """Types of thread events."""
    # Lifecycle
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_ARCHIVED = "thread.archived"
    
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
    
    # Memory
    NOTE_ADDED = "note.added"
    SUMMARY_SNAPSHOT = "summary.snapshot"
    MEMORY_COMPRESSED = "memory.compressed"
    
    # Links
    LINK_ADDED = "link.added"
    THREAD_REFERENCED = "thread.referenced"
    
    # Checkpoints
    CHECKPOINT_TRIGGERED = "checkpoint.triggered"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"


class ThreadEvent(Base):
    """
    Thread event - immutable, append-only.
    
    This is the core of event sourcing. Events are NEVER modified or deleted.
    """
    __tablename__ = "thread_events"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # Thread reference
    thread_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("threads.id"),
        nullable=False,
        index=True
    )
    
    # Event ordering (causal)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_event_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("thread_events.id"),
        nullable=True
    )
    
    # Event data
    event_type: Mapped[ThreadEventType] = mapped_column(
        SQLEnum(ThreadEventType),
        nullable=False,
        index=True
    )
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    
    # Traceability (R&D Rule #6)
    created_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("identities.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Actor info (human or agent)
    actor_type: Mapped[str] = mapped_column(String(50), default="human")
    actor_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    # Relationships
    thread: Mapped["Thread"] = relationship("Thread", back_populates="events")
    
    __table_args__ = (
        Index("ix_thread_events_thread_seq", "thread_id", "sequence_number"),
        Index("ix_thread_events_type", "event_type"),
        # Ensure unique sequence per thread
        Index("uq_thread_events_thread_seq", "thread_id", "sequence_number", unique=True),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT MODEL (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

class Checkpoint(Base, TimestampMixin):
    """
    Checkpoint for human approval.
    
    R&D Rule #1: All sensitive actions require human approval.
    """
    __tablename__ = "checkpoints"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # Ownership
    identity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )
    
    # Context
    sphere: Mapped[SphereType] = mapped_column(SQLEnum(SphereType), nullable=False)
    thread_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("threads.id"),
        nullable=True
    )
    
    # Checkpoint details
    checkpoint_type: Mapped[CheckpointType] = mapped_column(
        SQLEnum(CheckpointType),
        nullable=False
    )
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Status
    status: Mapped[CheckpointStatus] = mapped_column(
        SQLEnum(CheckpointStatus),
        default=CheckpointStatus.PENDING,
        index=True
    )
    
    # Resolution
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    resolved_by: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    resolution_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Expiration
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        Index("ix_checkpoints_identity_status", "identity_id", "status"),
        Index("ix_checkpoints_pending", "status", postgresql_where=(status == CheckpointStatus.PENDING)),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG MODEL (R&D Rule #6)
# ═══════════════════════════════════════════════════════════════════════════════

class AuditLogAction(str, enum.Enum):
    """Types of auditable actions."""
    # Auth
    LOGIN = "login"
    LOGOUT = "logout"
    
    # CRUD
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    
    # Checkpoints
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"
    
    # Agents
    AGENT_HIRED = "agent.hired"
    AGENT_FIRED = "agent.fired"
    AGENT_TASK = "agent.task"
    
    # Cross-sphere
    CROSS_SPHERE_ACCESS = "cross_sphere.access"
    CROSS_SPHERE_TRANSFER = "cross_sphere.transfer"


class AuditLog(Base):
    """
    Complete audit trail.
    
    R&D Rule #6: All significant actions must be logged.
    """
    __tablename__ = "audit_logs"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    
    # When
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    # Who
    identity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )
    actor_type: Mapped[str] = mapped_column(String(50), default="human")
    actor_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    # What
    action: Mapped[AuditLogAction] = mapped_column(
        SQLEnum(AuditLogAction),
        nullable=False,
        index=True
    )
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    # Context
    sphere: Mapped[Optional[SphereType]] = mapped_column(SQLEnum(SphereType))
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Request info
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    request_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    __table_args__ = (
        Index("ix_audit_logs_identity_time", "identity_id", "timestamp"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_resource", "resource_type", "resource_id"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "TraceabilityMixin",
    
    # Enums
    "SphereType",
    "ThreadStatus",
    "ThreadType",
    "Visibility",
    "CheckpointStatus",
    "CheckpointType",
    "ThreadEventType",
    "AuditLogAction",
    
    # Models
    "Identity",
    "Thread",
    "ThreadEvent",
    "Checkpoint",
    "AuditLog",
]
