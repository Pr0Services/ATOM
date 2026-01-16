"""
CHE·NU™ V75 Backend - Thread Model

RÈGLE: Thread = APPEND-ONLY
- founding_intent est IMMUTABLE
- Events ne peuvent qu'être ajoutés

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, ARRAY, event
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, validates
from datetime import datetime
import uuid

from config.database import Base


class Thread(Base):
    """
    Thread entity.
    
    RÈGLE: founding_intent est IMMUTABLE après création.
    """
    
    __tablename__ = "threads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    founding_intent = Column(Text, nullable=False)  # IMMUTABLE
    
    sphere_id = Column(String(50), ForeignKey("spheres.id"), nullable=True)
    bureau_id = Column(String(50), ForeignKey("bureaus.id"), nullable=True)
    
    status = Column(String(20), default="active")  # active, paused, completed, archived
    participants = Column(ARRAY(UUID(as_uuid=True)), default=[])
    
    last_activity = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Track original founding_intent to enforce immutability
    _original_founding_intent = None
    
    # Relationships
    user = relationship("User", back_populates="threads")
    sphere = relationship("Sphere", back_populates="threads")
    bureau = relationship("Bureau", back_populates="threads")
    events = relationship("ThreadEvent", back_populates="thread", cascade="all, delete-orphan", order_by="ThreadEvent.created_at")
    decisions = relationship("Decision", back_populates="thread")
    
    def __repr__(self):
        return f"<Thread {self.title}>"
    
    @validates('founding_intent')
    def validate_founding_intent(self, key, value):
        """
        Validate founding_intent immutability.
        
        RÈGLE: founding_intent ne peut être modifié après création.
        """
        # Allow setting on new instances
        if self._original_founding_intent is None:
            self._original_founding_intent = value
            return value
        
        # Prevent modification on existing instances
        if value != self._original_founding_intent:
            raise ValueError("founding_intent is IMMUTABLE and cannot be modified")
        
        return value
    
    @property
    def events_count(self) -> int:
        """Get count of events."""
        return len(self.events) if self.events else 0


class ThreadEvent(Base):
    """
    Thread event (APPEND-ONLY).
    
    RÈGLE: Events ne peuvent qu'être ajoutés, jamais modifiés ou supprimés.
    """
    
    __tablename__ = "thread_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), nullable=False, index=True)
    
    event_type = Column(String(50), nullable=False)  # message, decision, agent_action, file, checkpoint
    content = Column(Text, nullable=False)
    
    actor_id = Column(String(255), nullable=False)
    actor_type = Column(String(20), nullable=False)  # user, agent, system
    
    metadata = Column(JSONB, default={})
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    thread = relationship("Thread", back_populates="events")
    
    def __repr__(self):
        return f"<ThreadEvent {self.event_type} by {self.actor_type}>"


# ============================================================================
# APPEND-ONLY ENFORCEMENT
# ============================================================================

@event.listens_for(ThreadEvent, 'before_update')
def prevent_thread_event_update(mapper, connection, target):
    """Prevent updates to thread events - APPEND-ONLY."""
    raise ValueError("ThreadEvent is APPEND-ONLY and cannot be updated")


@event.listens_for(ThreadEvent, 'before_delete')
def prevent_thread_event_delete(mapper, connection, target):
    """Prevent deletion of thread events - APPEND-ONLY."""
    # Note: CASCADE deletes from parent thread are allowed
    # This only prevents direct deletion
    raise ValueError("ThreadEvent is APPEND-ONLY and cannot be deleted directly")
