"""
CHE·NU™ V75 Backend - Governance Models

RÈGLE ABSOLUE: GOUVERNANCE > EXÉCUTION
- Tout action sensible nécessite approbation
- Checkpoints avec aging visuel (GREEN → YELLOW → RED → BLINK)
- Audit log complet

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from config.database import Base


class Checkpoint(Base):
    """
    Governance checkpoint.
    
    Types:
    - governance: Policy-related decisions
    - cost: Financial approvals
    - identity: Identity verification
    - sensitive: Sensitive data access
    - agent: Agent operations
    - external: External API calls
    
    Aging Status:
    - green: < 25% time elapsed
    - yellow: 25-50% elapsed
    - red: 50-75% elapsed
    - blink: > 75% elapsed (urgent)
    """
    
    __tablename__ = "checkpoints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    type = Column(String(50), nullable=False)  # governance, cost, identity, sensitive, agent, external
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    status = Column(String(20), default="pending")  # pending, approved, rejected, expired
    
    requester_id = Column(String(255), nullable=False)
    requester_type = Column(String(20), nullable=False)  # user, agent, system
    
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255), nullable=False)
    
    context = Column(JSONB, default={})
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution_comment = Column(Text, nullable=True)
    
    # Relationships
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<Checkpoint {self.type}: {self.title}>"
    
    @property
    def aging_status(self) -> str:
        """
        Calculate checkpoint aging status.
        
        GREEN: < 25% of time elapsed
        YELLOW: 25-50% elapsed
        RED: 50-75% elapsed
        BLINK: > 75% elapsed (urgent)
        """
        if self.status != "pending":
            return "resolved"
        
        now = datetime.utcnow()
        expires = self.expires_at or (self.created_at + timedelta(hours=24))
        
        if now >= expires:
            return "expired"
        
        total_time = (expires - self.created_at).total_seconds()
        elapsed_time = (now - self.created_at).total_seconds()
        
        if elapsed_time < 0:
            return "green"
        
        percentage = elapsed_time / total_time
        
        if percentage < 0.25:
            return "green"
        elif percentage < 0.50:
            return "yellow"
        elif percentage < 0.75:
            return "red"
        else:
            return "blink"
    
    @property
    def is_expired(self) -> bool:
        """Check if checkpoint has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() >= self.expires_at


class Policy(Base):
    """
    Governance policy definition.
    
    Policies are loaded into OPA for enforcement.
    """
    
    __tablename__ = "policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    type = Column(String(50), nullable=False)  # cost, external, agent, identity, data
    rules = Column(JSONB, nullable=False, default={})
    
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=100)  # Lower = higher priority
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Policy {self.name}>"


class AuditLog(Base):
    """
    Governance audit log.
    
    Every governance decision is logged for compliance and transparency.
    """
    
    __tablename__ = "audit_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    action = Column(String(100), nullable=False)  # e.g., checkpoint.approve, agent.hire
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255), nullable=False)
    
    actor_id = Column(String(255), nullable=False)
    actor_type = Column(String(20), nullable=False)  # user, agent, system
    
    details = Column(JSONB, default={})
    
    # OPA decision info
    opa_decision = Column(Boolean, nullable=True)
    opa_policy = Column(String(100), nullable=True)
    
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.action} on {self.resource_type}/{self.resource_id}>"
    
    @classmethod
    def log(cls, action: str, resource_type: str, resource_id: str, 
            actor_id: str, actor_type: str = "user", **details):
        """Create an audit log entry."""
        return cls(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            actor_type=actor_type,
            details=details,
        )
