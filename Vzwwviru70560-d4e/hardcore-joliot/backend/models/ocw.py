"""
CHE·NU™ V75 - OCW Models
Operational Cognitive Workspace SQLAlchemy models.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float,
    DateTime, ForeignKey, Enum, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from config.database import Base


# ============================================================================
# ENUMS
# ============================================================================

import enum

class SessionType(str, enum.Enum):
    """OCW session types."""
    SHAREVIEW = "shareview"
    WHITEBOARD = "whiteboard"
    COCKPIT = "cockpit"
    COLLABORATION = "collaboration"


class SessionStatus(str, enum.Enum):
    """Session status."""
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"


class ParticipantRole(str, enum.Enum):
    """Participant roles."""
    HOST = "host"
    EDITOR = "editor"
    VIEWER = "viewer"
    SPECTATOR = "spectator"


class ObjectType(str, enum.Enum):
    """Canvas object types."""
    SHAPE = "shape"
    TEXT = "text"
    IMAGE = "image"
    DRAWING = "drawing"
    STICKY = "sticky"
    CONNECTOR = "connector"
    FRAME = "frame"


class AnnotationType(str, enum.Enum):
    """Annotation types."""
    COMMENT = "comment"
    HIGHLIGHT = "highlight"
    MARKER = "marker"
    VOICE_NOTE = "voice_note"


# ============================================================================
# MODELS
# ============================================================================

class OCWSession(Base):
    """
    OCW Session model.
    
    Represents an active workspace session (whiteboard, shareview, cockpit).
    """
    __tablename__ = "ocw_sessions"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    
    session_type: Mapped[SessionType] = mapped_column(
        Enum(SessionType, name="session_type_enum"),
        default=SessionType.WHITEBOARD
    )
    
    host_user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, name="session_status_enum"),
        default=SessionStatus.ACTIVE
    )
    
    # Configuration
    config: Mapped[dict] = mapped_column(JSONB, default=dict)
    shareview_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    participants = relationship("OCWParticipant", back_populates="session", cascade="all, delete-orphan")
    objects = relationship("OCWCanvasObject", back_populates="session", cascade="all, delete-orphan")
    annotations = relationship("OCWAnnotation", back_populates="session", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_ocw_sessions_workspace", "workspace_id"),
        Index("idx_ocw_sessions_host", "host_user_id"),
        Index("idx_ocw_sessions_status", "status"),
    )
    
    @property
    def is_active(self) -> bool:
        return self.status == SessionStatus.ACTIVE
    
    @property
    def duration_minutes(self) -> Optional[int]:
        if self.ended_at:
            delta = self.ended_at - self.started_at
            return int(delta.total_seconds() / 60)
        return None


class OCWParticipant(Base):
    """
    OCW Participant model.
    
    Tracks users in a session with their roles and cursor positions.
    """
    __tablename__ = "ocw_participants"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ocw_sessions.id"), nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    agent_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    
    role: Mapped[ParticipantRole] = mapped_column(
        Enum(ParticipantRole, name="participant_role_enum"),
        default=ParticipantRole.EDITOR
    )
    
    # Real-time state
    cursor_position: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # {x, y}
    viewport: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # {x, y, zoom}
    
    # Timestamps
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    session = relationship("OCWSession", back_populates="participants")
    
    __table_args__ = (
        Index("idx_ocw_participants_session", "session_id"),
        CheckConstraint(
            "(user_id IS NOT NULL) OR (agent_id IS NOT NULL)",
            name="chk_participant_identity"
        ),
    )


class OCWCanvasObject(Base):
    """
    OCW Canvas Object model.
    
    Represents objects on the canvas (shapes, text, stickies, etc.).
    """
    __tablename__ = "ocw_canvas_objects"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ocw_sessions.id"), nullable=False)
    
    object_type: Mapped[ObjectType] = mapped_column(
        Enum(ObjectType, name="object_type_enum"),
        nullable=False
    )
    
    # Position and size
    position: Mapped[dict] = mapped_column(JSONB, nullable=False)  # {x, y}
    size: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # {width, height}
    rotation: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Properties (type-specific)
    properties: Mapped[dict] = mapped_column(JSONB, default=dict)
    
    # Layer management
    layer: Mapped[int] = mapped_column(Integer, default=0)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Ownership
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    session = relationship("OCWSession", back_populates="objects")
    
    __table_args__ = (
        Index("idx_canvas_objects_session", "session_id"),
        Index("idx_canvas_objects_type", "object_type"),
        Index("idx_canvas_objects_layer", "layer"),
    )


class OCWAnnotation(Base):
    """
    OCW Annotation model.
    
    Comments, highlights, markers on canvas objects.
    """
    __tablename__ = "ocw_annotations"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ocw_sessions.id"), nullable=False)
    object_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), ForeignKey("ocw_canvas_objects.id"), nullable=True)
    
    annotation_type: Mapped[AnnotationType] = mapped_column(
        Enum(AnnotationType, name="annotation_type_enum"),
        default=AnnotationType.COMMENT
    )
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)  # {x, y} if not attached to object
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    
    # Ownership
    created_by: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    session = relationship("OCWSession", back_populates="annotations")
    
    __table_args__ = (
        Index("idx_annotations_session", "session_id"),
        Index("idx_annotations_object", "object_id"),
    )


class OCWTransformation(Base):
    """
    OCW Transformation model.
    
    Tracks content transformations (sketch to diagram, etc.).
    
    GOUVERNANCE: Transformations are logged and reversible.
    """
    __tablename__ = "ocw_transformations"
    
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("ocw_sessions.id"), nullable=False)
    
    transformation_type: Mapped[str] = mapped_column(String(50), nullable=False)  # diagram, mindmap, outline, dataspace, formalize
    
    # Input/Output
    input_object_ids: Mapped[list] = mapped_column(JSONB, nullable=False)  # UUIDs of transformed objects
    output_object_ids: Mapped[list] = mapped_column(JSONB, default=list)  # UUIDs of created objects
    
    # Reversibility
    is_reversible: Mapped[bool] = mapped_column(Boolean, default=True)
    reverse_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="completed")
    
    # If created DataSpace
    created_dataspace_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=True), nullable=True)
    
    # Timestamps
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    triggered_by: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    __table_args__ = (
        Index("idx_transformations_session", "session_id"),
    )
