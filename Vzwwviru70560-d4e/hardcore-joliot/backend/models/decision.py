"""
CHE·NU™ V75 Backend - Decision Model

⚠️ RÈGLE ABSOLUE: LES HUMAINS PRENNENT TOUTES LES DÉCISIONS
- Aucune décision automatique
- Aucun agent autonome
- L'IA illumine, ne décide jamais

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, event
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

from config.database import Base


class Decision(Base):
    """
    Decision requiring human input.
    
    RÈGLE: Seul l'HUMAIN peut résoudre une décision.
    
    Types:
    - approval: Yes/No approval
    - choice: Multiple options
    - confirmation: Confirm action
    - input: Free text input required
    - escalation: Needs higher authority
    """
    
    __tablename__ = "decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    type = Column(String(50), nullable=False)  # approval, choice, confirmation, input, escalation
    status = Column(String(20), default="pending")  # pending, resolved, cancelled, expired
    
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=True)
    sphere_id = Column(String(50), ForeignKey("spheres.id"), nullable=True)
    
    # Decision options (for choice/approval types)
    options = Column(JSONB, default=[])
    
    # AI context (for information only - AI does NOT decide)
    ai_context = Column(Text, nullable=True)
    ai_recommendation = Column(String(50), nullable=True)  # Option ID that AI suggests
    
    # For input type
    input_placeholder = Column(String(255), nullable=True)
    input_validation = Column(JSONB, nullable=True)  # Validation rules
    
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Resolution (human action)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_option = Column(String(50), nullable=True)
    resolved_input = Column(Text, nullable=True)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution_comment = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="decisions", foreign_keys=[user_id])
    resolver = relationship("User", foreign_keys=[resolved_by])
    thread = relationship("Thread", back_populates="decisions")
    sphere = relationship("Sphere", back_populates="decisions")
    
    def __repr__(self):
        return f"<Decision {self.title} ({self.status})>"
    
    @property
    def is_pending(self) -> bool:
        """Check if decision is pending."""
        return self.status == "pending"
    
    @property
    def is_expired(self) -> bool:
        """Check if decision has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() >= self.expires_at and self.status == "pending"
    
    @property
    def is_urgent(self) -> bool:
        """Check if decision is urgent."""
        if self.priority == "urgent":
            return True
        
        if self.expires_at:
            time_left = self.expires_at - datetime.utcnow()
            if time_left < timedelta(hours=4):
                return True
        
        return False
    
    @property
    def time_remaining(self) -> timedelta:
        """Get time remaining before expiration."""
        if not self.expires_at:
            return None
        return max(self.expires_at - datetime.utcnow(), timedelta(0))
    
    def resolve(self, user_id: str, option_id: str = None, 
                input_text: str = None, comment: str = None):
        """
        Resolve the decision.
        
        RÈGLE: This must be called by a human user.
        """
        self.status = "resolved"
        self.resolved_at = datetime.utcnow()
        self.resolved_by = user_id
        self.resolved_option = option_id
        self.resolved_input = input_text
        self.resolution_comment = comment
    
    def cancel(self, reason: str = None):
        """Cancel the decision."""
        self.status = "cancelled"
        self.resolved_at = datetime.utcnow()
        self.resolution_comment = reason


# ============================================================================
# DECISION ENFORCEMENT
# ============================================================================

@event.listens_for(Decision, 'before_update')
def validate_human_resolution(mapper, connection, target):
    """
    Validate that decisions are resolved by humans.
    
    RÈGLE: Agents cannot resolve decisions.
    """
    # If status is changing to resolved, ensure resolved_by is set
    if target.status == "resolved" and not target.resolved_by:
        raise ValueError(
            "Decision must be resolved by a human user. "
            "resolved_by is required."
        )


class DecisionOption:
    """
    Helper class for decision options.
    
    Structure stored in Decision.options JSONB:
    {
        "id": "opt-1",
        "label": "Approve",
        "description": "Approve the request",
        "is_recommended": false,
        "is_destructive": false,
        "metadata": {}
    }
    """
    
    @staticmethod
    def create(
        id: str,
        label: str,
        description: str = None,
        is_recommended: bool = False,
        is_destructive: bool = False,
        metadata: dict = None
    ) -> dict:
        """Create a decision option dict."""
        return {
            "id": id,
            "label": label,
            "description": description,
            "is_recommended": is_recommended,
            "is_destructive": is_destructive,
            "metadata": metadata or {},
        }
    
    @staticmethod
    def approval_options() -> list:
        """Standard approval options."""
        return [
            DecisionOption.create("approve", "Approve", is_recommended=True),
            DecisionOption.create("reject", "Reject", is_destructive=True),
        ]
    
    @staticmethod
    def confirmation_options() -> list:
        """Standard confirmation options."""
        return [
            DecisionOption.create("confirm", "Confirm", is_recommended=True),
            DecisionOption.create("cancel", "Cancel"),
        ]
