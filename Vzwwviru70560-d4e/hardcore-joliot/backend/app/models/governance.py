"""
CHE·NU™ Governance Models
=========================

Database models for governance features:
- GovernanceCheckpoint: HTTP 423 human gates
- AuditLog: Complete audit trail

R&D COMPLIANCE:
✅ Rule #1: Human sovereignty via checkpoints
✅ Rule #6: Full traceability via audit logs
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, DateTime,
    ForeignKey, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# =============================================================================
# ENUMS
# =============================================================================

class CheckpointType:
    """Types of governance checkpoints."""
    GOVERNANCE = "governance"      # Rule-based checkpoint
    COST = "cost"                  # Budget threshold
    IDENTITY = "identity"          # Cross-identity action
    SENSITIVE = "sensitive"        # Sensitive data/action
    EXTERNAL = "external"          # External communication
    FINANCIAL = "financial"        # Financial transaction
    DELETION = "deletion"          # Data deletion


class CheckpointStatus:
    """Checkpoint resolution status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


# =============================================================================
# GOVERNANCE CHECKPOINT MODEL
# =============================================================================

class GovernanceCheckpoint(Base):
    """
    Governance checkpoint for human approval gates.
    
    When a sensitive action is detected, a checkpoint is created
    and the system returns HTTP 423 LOCKED until human resolution.
    
    R&D COMPLIANCE:
    - Rule #1: Human Sovereignty - humans approve all sensitive actions
    - Rule #6: Traceability - full audit of checkpoint lifecycle
    """
    __tablename__ = "governance_checkpoints"
    
    # Primary key
    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Ownership (for identity boundary)
    identity_id: UUID = Column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Context
    thread_id: Optional[UUID] = Column(
        PGUUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Checkpoint details
    checkpoint_type: str = Column(String(50), nullable=False)
    reason: str = Column(Text, nullable=False)
    
    # The pending action data
    action_data: Dict[str, Any] = Column(JSONB, nullable=False, default={})
    
    # Available options for resolution
    options: List[str] = Column(JSONB, nullable=False, default=["approve", "reject"])
    
    # Resolution status
    status: str = Column(String(50), nullable=False, default=CheckpointStatus.PENDING)
    resolution: Optional[str] = Column(String(50), nullable=True)
    resolution_reason: Optional[str] = Column(Text, nullable=True)
    resolved_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True)
    resolved_by: Optional[UUID] = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Expiration
    expires_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True)
    
    # Checkpoint metadata
    checkpoint_metadata: Dict[str, Any] = Column(JSONB, nullable=False, default={})
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    identity = relationship("User", back_populates="checkpoints")
    thread = relationship("Thread", back_populates="checkpoints")
    
    def __repr__(self) -> str:
        return f"<GovernanceCheckpoint(id={self.id}, type={self.checkpoint_type}, status={self.status})>"
    
    @property
    def is_pending(self) -> bool:
        """Check if checkpoint is still pending."""
        return self.status == CheckpointStatus.PENDING
    
    @property
    def is_expired(self) -> bool:
        """Check if checkpoint has expired."""
        if self.expires_at and self.status == CheckpointStatus.PENDING:
            return datetime.utcnow() > self.expires_at
        return False
    
    def approve(self, resolved_by: UUID, reason: Optional[str] = None) -> None:
        """Approve the checkpoint."""
        self.status = CheckpointStatus.APPROVED
        self.resolution = "approve"
        self.resolution_reason = reason
        self.resolved_at = datetime.utcnow()
        self.resolved_by = resolved_by
    
    def reject(self, resolved_by: UUID, reason: Optional[str] = None) -> None:
        """Reject the checkpoint."""
        self.status = CheckpointStatus.REJECTED
        self.resolution = "reject"
        self.resolution_reason = reason
        self.resolved_at = datetime.utcnow()
        self.resolved_by = resolved_by
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "id": str(self.id),
            "identity_id": str(self.identity_id),
            "thread_id": str(self.thread_id) if self.thread_id else None,
            "checkpoint_type": self.checkpoint_type,
            "reason": self.reason,
            "action_data": self.action_data,
            "options": self.options,
            "status": self.status,
            "resolution": self.resolution,
            "resolution_reason": self.resolution_reason,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": str(self.resolved_by) if self.resolved_by else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.checkpoint_metadata,
            "created_at": self.created_at.isoformat(),
        }


# =============================================================================
# AUDIT LOG MODEL
# =============================================================================

class AuditLog(Base):
    """
    Audit log for complete system traceability.
    
    Every significant action in CHE·NU is logged here for:
    - Security auditing
    - Compliance requirements
    - Debugging and support
    - User activity history
    
    R&D COMPLIANCE:
    - Rule #6: Module Traceability - all actions logged
    - Rule #7: R&D Continuity - historical record maintained
    """
    __tablename__ = "audit_logs"
    
    # Primary key
    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Who performed the action (can be null for system actions)
    identity_id: Optional[UUID] = Column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # What action was performed
    action: str = Column(String(100), nullable=False, index=True)
    
    # What resource was affected
    resource_type: str = Column(String(100), nullable=False)
    resource_id: Optional[UUID] = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Action details
    details: Dict[str, Any] = Column(JSONB, nullable=False, default={})
    
    # Request context
    ip_address: Optional[str] = Column(String(45), nullable=True)
    user_agent: Optional[str] = Column(String(500), nullable=True)
    
    # Timestamp
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    # Relationships
    identity = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "id": str(self.id),
            "identity_id": str(self.identity_id) if self.identity_id else None,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": str(self.resource_id) if self.resource_id else None,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat(),
        }


# =============================================================================
# AUDIT ACTION TYPES
# =============================================================================

class AuditAction:
    """Standard audit action types."""
    # Authentication
    LOGIN = "auth.login"
    LOGOUT = "auth.logout"
    LOGIN_FAILED = "auth.login_failed"
    PASSWORD_CHANGED = "auth.password_changed"
    PASSWORD_RESET_REQUESTED = "auth.password_reset_requested"
    TOKEN_REFRESHED = "auth.token_refreshed"
    
    # User
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    
    # Sphere
    SPHERE_CREATED = "sphere.created"
    SPHERE_UPDATED = "sphere.updated"
    SPHERE_ACCESSED = "sphere.accessed"
    
    # Thread
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_ARCHIVED = "thread.archived"
    EVENT_APPENDED = "thread.event_appended"
    
    # Decision
    DECISION_RECORDED = "decision.recorded"
    DECISION_SUPERSEDED = "decision.superseded"
    
    # Action
    ACTION_CREATED = "action.created"
    ACTION_COMPLETED = "action.completed"
    ACTION_CANCELLED = "action.cancelled"
    
    # Checkpoint
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"
    CHECKPOINT_EXPIRED = "checkpoint.expired"
    
    # Agent
    AGENT_INVOKED = "agent.invoked"
    AGENT_COMPLETED = "agent.completed"
    AGENT_FAILED = "agent.failed"
    
    # Data
    DATA_EXPORTED = "data.exported"
    DATA_IMPORTED = "data.imported"
    
    # System
    SYSTEM_ERROR = "system.error"
    RATE_LIMIT_EXCEEDED = "system.rate_limit"


# =============================================================================
# AUDIT RESOURCE TYPES
# =============================================================================

class AuditResourceType:
    """Standard resource types for audit logs."""
    USER = "user"
    SESSION = "session"
    SPHERE = "sphere"
    BUREAU_SECTION = "bureau_section"
    QUICK_CAPTURE = "quick_capture"
    THREAD = "thread"
    EVENT = "event"
    DECISION = "decision"
    ACTION = "action"
    SNAPSHOT = "snapshot"
    CHECKPOINT = "checkpoint"
    AGENT = "agent"
    SYSTEM = "system"
