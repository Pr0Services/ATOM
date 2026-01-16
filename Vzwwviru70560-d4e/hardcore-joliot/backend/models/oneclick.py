"""
CHE·NU™ V75 - OneClick Assistant Models
1-Click workflow automation system.

GOUVERNANCE > EXÉCUTION
- All workflows require human confirmation
- No autonomous execution without approval

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.sphere import Sphere, Domain
    from models.user import User
    from models.identity import Identity


class WorkflowStatus(str, Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"  # GOUVERNANCE checkpoint
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InputType(str, Enum):
    """Workflow input types."""
    PROMPT = "prompt"
    FILE = "file"
    CONTEXT = "context"
    DATASPACE = "dataspace"
    FORM = "form"


class OutputType(str, Enum):
    """Workflow output types."""
    DOCUMENT = "document"
    DATASPACE = "dataspace"
    DASHBOARD = "dashboard"
    XR = "xr"
    REPORT = "report"
    NOTIFICATION = "notification"


class OneClickWorkflow(Base):
    """
    OneClick workflow definition.
    
    Workflows are triggered by intent patterns and
    execute a series of steps to produce outputs.
    """
    
    __tablename__ = "oneclick_workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Trigger patterns (NLP intent matching)
    trigger_patterns = Column(ARRAY(Text), default=list)
    
    # Scope
    sphere_id = Column(UUID(as_uuid=True), ForeignKey("spheres.id"))
    domain_id = Column(UUID(as_uuid=True), ForeignKey("domains.id"))
    
    # Workflow definition
    workflow_steps = Column(JSON, nullable=False)  # Array of step definitions
    
    # Input/Output schema
    required_inputs = Column(JSON, default=list)
    output_types = Column(ARRAY(Text), default=list)
    
    # Flags
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Governance
    requires_approval = Column(Boolean, default=True)  # GOUVERNANCE
    approval_level = Column(String(20), default="user")  # user, admin, owner
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    executions = relationship("OneClickExecution", back_populates="workflow")
    templates = relationship("OneClickTemplate", back_populates="workflow")
    
    def __repr__(self):
        return f"<OneClickWorkflow {self.name}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "trigger_patterns": self.trigger_patterns,
            "sphere_id": str(self.sphere_id) if self.sphere_id else None,
            "domain_id": str(self.domain_id) if self.domain_id else None,
            "workflow_steps": self.workflow_steps,
            "required_inputs": self.required_inputs,
            "output_types": self.output_types,
            "is_system": self.is_system,
            "is_active": self.is_active,
            "requires_approval": self.requires_approval,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class OneClickExecution(Base):
    """
    Workflow execution record.
    
    GOUVERNANCE:
    - Tracks all execution steps
    - Records approval decisions
    - Maintains audit trail
    """
    
    __tablename__ = "oneclick_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("oneclick_workflows.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    
    # Input
    input_data = Column(JSON, nullable=False)
    input_type = Column(String(50))
    
    # Status
    status = Column(String(20), default=WorkflowStatus.PENDING.value)
    
    # Progress
    steps_completed = Column(Integer, default=0)
    total_steps = Column(Integer)
    current_step = Column(String(100))
    
    # Output
    output_data = Column(JSON)
    output_dataspaces = Column(ARRAY(UUID(as_uuid=True)))
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Error handling
    error_message = Column(Text)
    execution_log = Column(JSON, default=list)
    
    # Governance
    approval_checkpoint_id = Column(UUID(as_uuid=True))
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(DateTime)
    
    # Relationships
    workflow = relationship("OneClickWorkflow", back_populates="executions")
    
    def __repr__(self):
        return f"<OneClickExecution {self.id} ({self.status})>"
    
    @property
    def progress_percent(self) -> int:
        """Calculate progress percentage."""
        if self.total_steps and self.total_steps > 0:
            return int((self.steps_completed / self.total_steps) * 100)
        return 0
    
    @property
    def duration_seconds(self) -> Optional[int]:
        """Calculate execution duration."""
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            return int(delta.total_seconds())
        return None
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "workflow_id": str(self.workflow_id),
            "user_id": str(self.user_id),
            "identity_id": str(self.identity_id),
            "input_type": self.input_type,
            "status": self.status,
            "steps_completed": self.steps_completed,
            "total_steps": self.total_steps,
            "current_step": self.current_step,
            "progress_percent": self.progress_percent,
            "output_data": self.output_data,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
        }


class OneClickTemplate(Base):
    """
    Predefined templates for common workflows.
    """
    
    __tablename__ = "oneclick_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # construction, immobilier, finance, creative, enterprise
    
    prompt_template = Column(Text, nullable=False)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("oneclick_workflows.id"))
    
    example_inputs = Column(JSON, default=list)
    
    usage_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = relationship("OneClickWorkflow", back_populates="templates")
    
    def __repr__(self):
        return f"<OneClickTemplate {self.name}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "prompt_template": self.prompt_template,
            "workflow_id": str(self.workflow_id) if self.workflow_id else None,
            "example_inputs": self.example_inputs,
            "usage_count": self.usage_count,
            "is_featured": self.is_featured,
        }
