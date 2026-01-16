"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — DATABASE MODELS
═══════════════════════════════════════════════════════════════════════════════
SQLAlchemy 2.0 models with full R&D Rules compliance

Rule #6: Full Traceability - All models have id, created_by, created_at
Rule #7: Architecture Frozen - 9 spheres, 6 bureau sections enforced
═══════════════════════════════════════════════════════════════════════════════
"""

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, Enum, ForeignKey, JSON, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid
import enum

from app.core.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereType(str, enum.Enum):
    """9 Spheres - FROZEN (Rule #7)"""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"


class BureauSection(str, enum.Enum):
    """6 Bureau Sections - FROZEN (Rule #7)"""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


class ThreadStatus(str, enum.Enum):
    """Thread lifecycle states"""
    DRAFT = "draft"
    ACTIVE = "active"
    MATURING = "maturing"
    DECISION_READY = "decision_ready"
    DECIDED = "decided"
    ARCHIVED = "archived"


class CheckpointStatus(str, enum.Enum):
    """Checkpoint states (Rule #1)"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class CheckpointType(str, enum.Enum):
    """Checkpoint types (Rule #1)"""
    DELETE = "delete"
    ARCHIVE = "archive"
    CRITICAL_DECISION = "critical_decision"
    TRANSFER = "transfer"
    EXTERNAL_ACTION = "external_action"


class DecisionSeverity(str, enum.Enum):
    """Decision severity levels"""
    INFORMATIONAL = "informational"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


class MemoryLayer(str, enum.Enum):
    """Tri-layer memory"""
    HOT = "hot"      # Active context (Redis)
    WARM = "warm"    # Recent (PostgreSQL + Redis)
    COLD = "cold"    # Archived (PostgreSQL only)


# ═══════════════════════════════════════════════════════════════════════════════
# BASE MIXIN
# ═══════════════════════════════════════════════════════════════════════════════

class TrackedMixin:
    """
    Mixin for Rule #6: Full Traceability
    All objects have id, created_by, created_at
    """
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
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
    
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY
# ═══════════════════════════════════════════════════════════════════════════════

class Identity(TrackedMixin, Base):
    """
    User identity - owns all data within CHE·NU.
    Rule #3: Identity boundary enforcement
    """
    
    __tablename__ = "identities"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Authentication
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500))
    preferences: Mapped[Optional[Dict]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    spheres: Mapped[List["Sphere"]] = relationship(
        "Sphere", 
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    threads: Mapped[List["Thread"]] = relationship(
        "Thread",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index("ix_identities_email", "email"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE (Rule #7: 9 Spheres Frozen)
# ═══════════════════════════════════════════════════════════════════════════════

class Sphere(TrackedMixin, Base):
    """
    Life sphere - one of 9 frozen spheres.
    Auto-created when identity is created.
    """
    
    __tablename__ = "spheres"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    sphere_type: Mapped[SphereType] = mapped_column(
        Enum(SphereType),
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    color: Mapped[Optional[str]] = mapped_column(String(20))
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    settings: Mapped[Optional[Dict]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    owner: Mapped["Identity"] = relationship("Identity", back_populates="spheres")
    workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace",
        back_populates="sphere",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        UniqueConstraint("owner_id", "sphere_type", name="uq_sphere_per_owner"),
        Index("ix_spheres_owner_type", "owner_id", "sphere_type"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# WORKSPACE (Rule #7: 6 Bureau Sections)
# ═══════════════════════════════════════════════════════════════════════════════

class Workspace(TrackedMixin, Base):
    """
    Workspace within a sphere - contains 6 bureau sections.
    Auto-created when sphere is created.
    """
    
    __tablename__ = "workspaces"
    
    sphere_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("spheres.id", ondelete="CASCADE"),
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Bureau sections configuration
    sections: Mapped[Dict] = mapped_column(JSONB, default=dict)
    
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[Dict]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    sphere: Mapped["Sphere"] = relationship("Sphere", back_populates="workspaces")
    
    __table_args__ = (
        Index("ix_workspaces_sphere", "sphere_id"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD
# ═══════════════════════════════════════════════════════════════════════════════

class Thread(TrackedMixin, Base):
    """
    Thread - core unit of work/decision in CHE·NU.
    Event-sourced with immutable events.
    """
    
    __tablename__ = "threads"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    sphere_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("spheres.id", ondelete="SET NULL")
    )
    
    parent_thread_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="SET NULL")
    )
    
    # Core fields
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    founding_intent: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ThreadStatus] = mapped_column(
        Enum(ThreadStatus),
        default=ThreadStatus.DRAFT
    )
    
    # Maturity tracking
    maturity_score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    tags: Mapped[Optional[List]] = mapped_column(JSONB, default=list)
    metadata: Mapped[Optional[Dict]] = mapped_column(JSONB, default=dict)
    
    # Relationships
    owner: Mapped["Identity"] = relationship("Identity", back_populates="threads")
    events: Mapped[List["ThreadEvent"]] = relationship(
        "ThreadEvent",
        back_populates="thread",
        cascade="all, delete-orphan",
        order_by="ThreadEvent.created_at"
    )
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision",
        back_populates="thread",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index("ix_threads_owner", "owner_id"),
        Index("ix_threads_sphere", "sphere_id"),
        Index("ix_threads_status", "status"),
        # Rule #5: Chronological ordering
        Index("ix_threads_created_at", "created_at"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENT (Immutable Event Log)
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadEvent(TrackedMixin, Base):
    """
    Immutable event in thread's event log.
    Append-only - never modified or deleted.
    """
    
    __tablename__ = "thread_events"
    
    thread_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False
    )
    
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_data: Mapped[Dict] = mapped_column(JSONB, nullable=False)
    
    # Causal ordering
    parent_event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("thread_events.id")
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    thread: Mapped["Thread"] = relationship("Thread", back_populates="events")
    
    __table_args__ = (
        Index("ix_thread_events_thread", "thread_id"),
        Index("ix_thread_events_type", "event_type"),
        Index("ix_thread_events_sequence", "thread_id", "sequence_number"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION
# ═══════════════════════════════════════════════════════════════════════════════

class Decision(TrackedMixin, Base):
    """
    Decision recorded on a thread.
    Major/Critical decisions require checkpoint (Rule #1).
    """
    
    __tablename__ = "decisions"
    
    thread_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False
    )
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[DecisionSeverity] = mapped_column(
        Enum(DecisionSeverity),
        default=DecisionSeverity.INFORMATIONAL
    )
    
    # Checkpoint reference (Rule #1)
    checkpoint_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("checkpoints.id")
    )
    
    rationale: Mapped[Optional[str]] = mapped_column(Text)
    outcome: Mapped[Optional[str]] = mapped_column(Text)
    
    is_final: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    thread: Mapped["Thread"] = relationship("Thread", back_populates="decisions")
    
    __table_args__ = (
        Index("ix_decisions_thread", "thread_id"),
        Index("ix_decisions_severity", "severity"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT (Rule #1: Human Sovereignty)
# ═══════════════════════════════════════════════════════════════════════════════

class Checkpoint(TrackedMixin, Base):
    """
    Governance checkpoint requiring human approval.
    HTTP 423 LOCKED until approved/rejected.
    """
    
    __tablename__ = "checkpoints"
    
    checkpoint_type: Mapped[CheckpointType] = mapped_column(
        Enum(CheckpointType),
        nullable=False
    )
    
    status: Mapped[CheckpointStatus] = mapped_column(
        Enum(CheckpointStatus),
        default=CheckpointStatus.PENDING
    )
    
    # Target resource
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    # Action details
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    action_data: Mapped[Dict] = mapped_column(JSONB, nullable=False)
    
    # Approval tracking
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    
    # Expiry
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    
    __table_args__ = (
        Index("ix_checkpoints_status", "status"),
        Index("ix_checkpoints_resource", "resource_type", "resource_id"),
        Index("ix_checkpoints_expires", "expires_at"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DATASPACE
# ═══════════════════════════════════════════════════════════════════════════════

class DataSpace(TrackedMixin, Base):
    """
    Encrypted data container.
    """
    
    __tablename__ = "dataspaces"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Encryption
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=True)
    encryption_key_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Storage
    storage_bytes: Mapped[int] = mapped_column(Integer, default=0)
    file_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    metadata: Mapped[Optional[Dict]] = mapped_column(JSONB, default=dict)
    
    __table_args__ = (
        Index("ix_dataspaces_owner", "owner_id"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class Agent(TrackedMixin, Base):
    """
    AI agent registration.
    Rule #4: No AI-to-AI orchestration
    """
    
    __tablename__ = "agents"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Scope
    sphere_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("spheres.id", ondelete="SET NULL")
    )
    
    # Capabilities
    capabilities: Mapped[List] = mapped_column(JSONB, default=list)
    
    # Rule #4: Cannot call other agents
    can_call_other_agents: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Token budget
    token_budget: Mapped[int] = mapped_column(Integer, default=10000)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_hired: Mapped[bool] = mapped_column(Boolean, default=False)
    
    __table_args__ = (
        Index("ix_agents_owner", "owner_id"),
        Index("ix_agents_type", "agent_type"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY SNAPSHOT
# ═══════════════════════════════════════════════════════════════════════════════

class MemorySnapshot(TrackedMixin, Base):
    """
    Compressed memory snapshot for warm/cold storage.
    """
    
    __tablename__ = "memory_snapshots"
    
    thread_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False
    )
    
    layer: Mapped[MemoryLayer] = mapped_column(
        Enum(MemoryLayer),
        default=MemoryLayer.WARM
    )
    
    snapshot_data: Mapped[Dict] = mapped_column(JSONB, nullable=False)
    compression_ratio: Mapped[Optional[float]] = mapped_column(Float)
    
    events_included: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (
        Index("ix_memory_snapshots_thread", "thread_id"),
        Index("ix_memory_snapshots_layer", "layer"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING
# ═══════════════════════════════════════════════════════════════════════════════

class Meeting(TrackedMixin, Base):
    """
    Meeting entity (bureau section).
    """
    
    __tablename__ = "meetings"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    workspace_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="SET NULL")
    )
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    
    status: Mapped[str] = mapped_column(String(50), default="draft")
    
    # Notes and actions
    notes: Mapped[Optional[str]] = mapped_column(Text)
    action_items: Mapped[Optional[List]] = mapped_column(JSONB, default=list)
    
    __table_args__ = (
        Index("ix_meetings_owner", "owner_id"),
        Index("ix_meetings_scheduled", "scheduled_at"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class Notification(TrackedMixin, Base):
    """
    User notification.
    """
    
    __tablename__ = "notifications"
    
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("identities.id", ondelete="CASCADE"),
        nullable=False
    )
    
    notification_type: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text)
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Related resource
    resource_type: Mapped[Optional[str]] = mapped_column(String(100))
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    
    __table_args__ = (
        Index("ix_notifications_owner", "owner_id"),
        Index("ix_notifications_unread", "owner_id", "is_read"),
    )
