"""
CHE·NU™ V75 - Workspace Models
Dynamic workspace system with multiple view modes.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.identity import Identity
    from models.dataspace import DataSpace


class WorkspaceMode(str, Enum):
    """Workspace view modes."""
    DOCUMENT = "document"
    BOARD = "board"
    TIMELINE = "timeline"
    SPREADSHEET = "spreadsheet"
    DASHBOARD = "dashboard"
    DIAGRAM = "diagram"
    WHITEBOARD = "whiteboard"
    XR = "xr"
    HYBRID = "hybrid"


class PanelType(str, Enum):
    """Panel types in workspace."""
    EDITOR = "editor"
    PREVIEW = "preview"
    CHAT = "chat"
    FILES = "files"
    AGENTS = "agents"
    TIMELINE = "timeline"
    CANVAS = "canvas"
    TERMINAL = "terminal"
    BROWSER = "browser"


class Workspace(Base):
    """
    Workspace model.
    
    Workspaces provide customizable views for working with dataspaces.
    Supports multiple modes and panel configurations.
    """
    
    __tablename__ = "workspaces"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False)
    dataspace_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id"))
    
    name = Column(String(255), nullable=False)
    workspace_mode = Column(String(50), nullable=False, default=WorkspaceMode.DOCUMENT.value)
    
    # Layout configuration
    layout_config = Column(JSON, default=dict)
    view_state = Column(JSON, default=dict)
    
    is_default = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    panels = relationship("WorkspacePanel", back_populates="workspace", cascade="all, delete-orphan")
    states = relationship("WorkspaceState", back_populates="workspace", cascade="all, delete-orphan")
    transformations = relationship("WorkspaceTransformation", back_populates="workspace", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workspace {self.name} ({self.workspace_mode})>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "identity_id": str(self.identity_id),
            "dataspace_id": str(self.dataspace_id) if self.dataspace_id else None,
            "name": self.name,
            "workspace_mode": self.workspace_mode,
            "layout_config": self.layout_config,
            "view_state": self.view_state,
            "is_default": self.is_default,
            "panels_count": len(self.panels) if self.panels else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class WorkspacePanel(Base):
    """
    Individual panel within a workspace.
    """
    
    __tablename__ = "workspace_panels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    
    panel_type = Column(String(50), nullable=False)
    position = Column(JSON, nullable=False)  # {x, y, width, height}
    
    config = Column(JSON, default=dict)
    is_visible = Column(Boolean, default=True)
    z_index = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="panels")
    
    def __repr__(self):
        return f"<WorkspacePanel {self.panel_type}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "workspace_id": str(self.workspace_id),
            "panel_type": self.panel_type,
            "position": self.position,
            "config": self.config,
            "is_visible": self.is_visible,
            "z_index": self.z_index,
        }


class WorkspaceState(Base):
    """
    Saved workspace state for quick restore.
    """
    
    __tablename__ = "workspace_states"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    
    state_name = Column(String(100))
    state_data = Column(JSON, nullable=False)
    
    is_autosave = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    workspace = relationship("Workspace", back_populates="states")
    
    def __repr__(self):
        return f"<WorkspaceState {self.state_name}>"


class WorkspaceTransformation(Base):
    """
    Records workspace mode transformations.
    Supports reversibility for undo operations.
    """
    
    __tablename__ = "workspace_transformations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    
    from_mode = Column(String(50), nullable=False)
    to_mode = Column(String(50), nullable=False)
    
    transformation_data = Column(JSON, nullable=False)
    
    triggered_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    triggered_at = Column(DateTime, default=datetime.utcnow)
    
    is_reversible = Column(Boolean, default=True)
    reverse_data = Column(JSON)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="transformations")
    
    def __repr__(self):
        return f"<WorkspaceTransformation {self.from_mode} -> {self.to_mode}>"
