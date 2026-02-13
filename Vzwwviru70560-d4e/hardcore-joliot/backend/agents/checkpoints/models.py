"""
============================================================================
CHE-NU V69 - CHECKPOINT PERSISTENCE MODELS
============================================================================
Version: 1.0.0
Purpose: SQLAlchemy models for checkpoint persistence
Principle: Checkpoints survive restarts with full audit trail
============================================================================
"""

from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import enum

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, Enum, ForeignKey, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class PersistedCheckpointType(str, enum.Enum):
    """Types of governance checkpoints"""
    HITL = "hitl"              # Human-In-The-Loop required
    OPA = "opa"                # OPA policy check
    THRESHOLD = "threshold"    # Value threshold check
    ESCALATION = "escalation"  # Escalation to higher level
    APPROVAL = "approval"      # Explicit approval required


class PersistedCheckpointStatus(str, enum.Enum):
    """Checkpoint resolution status"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"


# ============================================================================
# CHECKPOINT AUDIT LOG
# ============================================================================

class CheckpointAuditLog(Base):
    """
    Immutable audit log for checkpoint events.

    Records all checkpoint state changes for compliance and debugging.
    """

    __tablename__ = "checkpoint_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    checkpoint_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("persisted_checkpoints.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_data: Mapped[Dict] = mapped_column(JSONB, default=dict)

    actor_id: Mapped[Optional[str]] = mapped_column(String(255))
    actor_type: Mapped[str] = mapped_column(String(50), default="system")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        Index("ix_checkpoint_audit_checkpoint_id", "checkpoint_id"),
        Index("ix_checkpoint_audit_event_type", "event_type"),
        Index("ix_checkpoint_audit_created_at", "created_at"),
    )


# ============================================================================
# PERSISTED CHECKPOINT
# ============================================================================

class PersistedCheckpoint(Base):
    """
    Database-persisted checkpoint for governance decisions.

    Ensures checkpoints survive application restarts and provides
    durability for audit compliance.

    Features:
    - Full checkpoint lifecycle tracking
    - Audit trail via CheckpointAuditLog
    - Timeout management with expiry
    - Escalation support
    """

    __tablename__ = "persisted_checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Context
    agent_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    action_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Type and reason
    checkpoint_type: Mapped[PersistedCheckpointType] = mapped_column(
        Enum(PersistedCheckpointType),
        nullable=False
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    # Status
    status: Mapped[PersistedCheckpointStatus] = mapped_column(
        Enum(PersistedCheckpointStatus),
        default=PersistedCheckpointStatus.PENDING,
        index=True
    )

    # Details stored as JSON for flexibility
    details: Mapped[Dict] = mapped_column(JSONB, default=dict)

    # Resolution tracking
    resolved_by: Mapped[Optional[str]] = mapped_column(String(255))
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Timing
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
    timeout_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    # Escalation
    escalated_to: Mapped[Optional[str]] = mapped_column(String(255))
    escalation_level: Mapped[int] = mapped_column(Integer, default=0)

    # Created by (for traceability - Rule #6)
    created_by: Mapped[str] = mapped_column(String(255), default="system")

    # Relationships
    audit_logs: Mapped[list["CheckpointAuditLog"]] = relationship(
        "CheckpointAuditLog",
        back_populates="checkpoint",
        cascade="all, delete-orphan",
        order_by="CheckpointAuditLog.created_at"
    )

    __table_args__ = (
        Index("ix_persisted_checkpoints_agent_id", "agent_id"),
        Index("ix_persisted_checkpoints_status", "status"),
        Index("ix_persisted_checkpoints_timeout", "timeout_at"),
        Index("ix_persisted_checkpoints_pending", "status", "timeout_at",
              postgresql_where=(status == PersistedCheckpointStatus.PENDING)),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "checkpoint_id": str(self.id),
            "agent_id": self.agent_id,
            "action_id": self.action_id,
            "checkpoint_type": self.checkpoint_type.value,
            "reason": self.reason,
            "status": self.status.value,
            "details": self.details,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "timeout_at": self.timeout_at.isoformat() if self.timeout_at else None,
            "escalated_to": self.escalated_to,
            "escalation_level": self.escalation_level,
            "is_resolved": self.status in [
                PersistedCheckpointStatus.APPROVED,
                PersistedCheckpointStatus.DENIED,
                PersistedCheckpointStatus.ESCALATED,
                PersistedCheckpointStatus.TIMEOUT,
            ],
            "is_approved": self.status == PersistedCheckpointStatus.APPROVED,
        }


# Add back-reference
CheckpointAuditLog.checkpoint = relationship(
    "PersistedCheckpoint",
    back_populates="audit_logs"
)
