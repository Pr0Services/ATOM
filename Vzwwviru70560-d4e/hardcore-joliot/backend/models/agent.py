"""
CHE·NU™ V75 Backend - Agent Model

RÈGLE: L'IA ILLUMINE, ne décide jamais
- Nova est L0 (système), toujours disponible
- Agents L1-L3 sont "hired" par l'utilisateur
- Aucun agent autonome

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, ARRAY, event
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, validates
from datetime import datetime
import uuid

from config.database import Base


class Agent(Base):
    """
    Agent entity.
    
    Levels:
    - L0: System (Nova only, always available)
    - L1: Personal (user-created assistants)
    - L2: Specialized (domain experts)
    - L3: Enterprise (organization-wide)
    """
    
    __tablename__ = "agents"
    
    id = Column(String(50), primary_key=True)  # String ID for named agents like 'nova'
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    level = Column(String(2), nullable=False)  # L0, L1, L2, L3
    status = Column(String(20), default="available")  # available, busy, offline
    
    capabilities = Column(JSONB, default=[])
    avatar_url = Column(Text, nullable=True)
    
    is_system = Column(Boolean, default=False)  # True for Nova
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    hired_by = relationship("HiredAgent", back_populates="agent")
    tasks = relationship("AgentTask", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.level})>"
    
    @property
    def is_nova(self) -> bool:
        """Check if this is Nova (L0 system agent)."""
        return self.id == "nova" or self.is_system
    
    @validates('level')
    def validate_level(self, key, value):
        """Validate agent level."""
        valid_levels = ['L0', 'L1', 'L2', 'L3']
        if value not in valid_levels:
            raise ValueError(f"Invalid agent level. Must be one of: {valid_levels}")
        return value


class HiredAgent(Base):
    """
    Relationship between user and hired agent.
    
    RÈGLE: Users hire agents (except Nova which is always available).
    """
    
    __tablename__ = "hired_agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(String(50), ForeignKey("agents.id"), nullable=False, index=True)
    
    sphere_ids = Column(ARRAY(String), default=[])
    
    hired_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="hired_agents")
    agent = relationship("Agent", back_populates="hired_by")
    
    def __repr__(self):
        return f"<HiredAgent user={self.user_id} agent={self.agent_id}>"


class AgentTask(Base):
    """
    Task assigned to an agent.
    
    RÈGLE: L'agent exécute, l'humain valide le résultat.
    """
    
    __tablename__ = "agent_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(50), ForeignKey("agents.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=True)
    
    description = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    priority = Column(String(20), default="normal")  # low, normal, high
    
    progress = Column(Integer, default=0)  # 0-100
    result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tasks")
    
    def __repr__(self):
        return f"<AgentTask {self.id} ({self.status})>"


# ============================================================================
# NOVA PROTECTION
# ============================================================================

@event.listens_for(Agent, 'before_delete')
def prevent_nova_deletion(mapper, connection, target):
    """Prevent deletion of Nova (L0 system agent)."""
    if target.id == "nova" or target.is_system:
        raise ValueError("Nova (L0 system agent) cannot be deleted")


@event.listens_for(HiredAgent, 'before_insert')
def prevent_hiring_nova(mapper, connection, target):
    """Prevent hiring Nova (always available)."""
    if target.agent_id == "nova":
        raise ValueError("Nova is always available and does not need to be hired")
