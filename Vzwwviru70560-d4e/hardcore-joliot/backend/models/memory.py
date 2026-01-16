"""
CHE·NU™ V75 - Memory & Governance Models
Complete memory system with governance controls.

GOUVERNANCE > EXÉCUTION
- All memory operations are audited
- Cross-identity access is blocked
- Elevation requires human approval

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.identity import Identity
    from models.dataspace import DataSpace
    from models.thread import Thread


class MemoryType(str, Enum):
    """Memory duration types."""
    SHORT_TERM = "short_term"  # Session-based
    MID_TERM = "mid_term"      # Days
    LONG_TERM = "long_term"    # Persistent
    INSTITUTIONAL = "institutional"  # Org-wide
    AGENT = "agent"            # Agent-specific (no personal data)


class MemoryCategory(str, Enum):
    """Memory content categories."""
    PREFERENCE = "preference"
    INSTRUCTION = "instruction"
    FACT = "fact"
    CONTEXT = "context"
    RULE = "rule"


class MemoryStatus(str, Enum):
    """Memory status."""
    ACTIVE = "active"
    PINNED = "pinned"
    ARCHIVED = "archived"
    DELETED = "deleted"


class AuditActionType(str, Enum):
    """Audit action types."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SHARE = "share"
    ELEVATE = "elevate"


class ElevationStatus(str, Enum):
    """Elevation request status."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class MemoryItem(Base):
    """
    Memory item model.
    
    GOUVERNANCE:
    - Memories are scoped to identity (no cross-identity access)
    - Agent memories cannot contain personal data
    - All access is logged
    """
    
    __tablename__ = "memory_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id", ondelete="CASCADE"), nullable=False)
    
    memory_type = Column(String(50), nullable=False)
    memory_category = Column(String(50))
    
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default=dict)
    
    # Optional links
    dataspace_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="SET NULL"))
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="SET NULL"))
    
    # Lifecycle
    status = Column(String(20), default=MemoryStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_accessed_at = Column(DateTime)
    
    # Governance
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime)
    
    def __repr__(self):
        return f"<MemoryItem {self.memory_type}:{self.memory_category}>"
    
    @property
    def is_expired(self) -> bool:
        """Check if memory has expired."""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "identity_id": str(self.identity_id),
            "memory_type": self.memory_type,
            "memory_category": self.memory_category,
            "content": self.content,
            "metadata": self.metadata,
            "dataspace_id": str(self.dataspace_id) if self.dataspace_id else None,
            "thread_id": str(self.thread_id) if self.thread_id else None,
            "status": self.status,
            "is_expired": self.is_expired,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


class GovernanceAuditLog(Base):
    """
    Governance audit log.
    
    Records ALL actions for compliance and reversibility.
    This is APPEND ONLY - records are never deleted.
    """
    
    __tablename__ = "governance_audit_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"))
    agent_id = Column(UUID(as_uuid=True))
    
    action_type = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)  # memory, dataspace, thread, file, agent
    resource_id = Column(UUID(as_uuid=True), nullable=False)
    
    action_details = Column(JSON, default=dict)
    
    # State snapshots for reversibility
    before_state = Column(JSON)
    after_state = Column(JSON)
    
    # Permission context
    permission_used = Column(String(100))
    elevation_required = Column(Boolean, default=False)
    elevation_approved = Column(Boolean)
    
    # Request metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<GovernanceAuditLog {self.action_type} on {self.resource_type}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "identity_id": str(self.identity_id) if self.identity_id else None,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "action_type": self.action_type,
            "resource_type": self.resource_type,
            "resource_id": str(self.resource_id),
            "action_details": self.action_details,
            "elevation_required": self.elevation_required,
            "elevation_approved": self.elevation_approved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ElevationRequest(Base):
    """
    Elevation request for sensitive actions.
    
    GOUVERNANCE:
    - Certain actions require explicit human approval
    - Requests expire if not acted upon
    - All requests are logged
    """
    
    __tablename__ = "elevation_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    requested_action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=False)
    
    reason = Column(Text)
    
    status = Column(String(20), default=ElevationStatus.PENDING.value)
    
    requested_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    responded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    expires_at = Column(DateTime)
    
    metadata = Column(JSON, default=dict)
    
    def __repr__(self):
        return f"<ElevationRequest {self.requested_action} ({self.status})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if request has expired."""
        if self.expires_at and self.status == ElevationStatus.PENDING.value:
            return datetime.utcnow() > self.expires_at
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "identity_id": str(self.identity_id),
            "requested_action": self.requested_action,
            "resource_type": self.resource_type,
            "resource_id": str(self.resource_id),
            "reason": self.reason,
            "status": self.status,
            "is_expired": self.is_expired,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "responded_at": self.responded_at.isoformat() if self.responded_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


class CrossIdentityBlock(Base):
    """
    Records blocked cross-identity access attempts.
    
    GOUVERNANCE:
    - Prevents data leakage between identities
    - Logs all blocked attempts for security review
    """
    
    __tablename__ = "cross_identity_blocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    source_identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    target_identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    blocked_action = Column(String(100), nullable=False)
    blocked_resource_type = Column(String(50))
    blocked_resource_id = Column(UUID(as_uuid=True))
    
    block_reason = Column(Text)
    
    blocked_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CrossIdentityBlock {self.source_identity_id} -> {self.target_identity_id}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "source_identity_id": str(self.source_identity_id),
            "target_identity_id": str(self.target_identity_id),
            "blocked_action": self.blocked_action,
            "blocked_resource_type": self.blocked_resource_type,
            "block_reason": self.block_reason,
            "blocked_at": self.blocked_at.isoformat() if self.blocked_at else None,
        }
