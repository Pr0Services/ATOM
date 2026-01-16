"""
CHE·NU™ V75 - Identity Models
Multi-identity system for user context separation.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.sphere import Sphere


class IdentityType(str, Enum):
    """Identity types."""
    PERSONAL = "personal"
    ENTERPRISE = "enterprise"
    CREATIVE = "creative"
    DESIGN = "design"
    ARCHITECTURE = "architecture"
    CONSTRUCTION = "construction"


class Identity(Base):
    """
    User identity model.
    
    Users can have multiple identities for different contexts:
    - Personal: Personal life management
    - Enterprise: Business activities
    - Creative: Creative work
    - etc.
    
    GOUVERNANCE: Each identity has separate data isolation.
    """
    
    __tablename__ = "identities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    identity_type = Column(String(50), nullable=False)
    identity_name = Column(String(100), nullable=False)
    
    is_default = Column(Boolean, default=False)
    config = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="identities")
    permissions = relationship("IdentityPermission", back_populates="identity", cascade="all, delete-orphan")
    sphere_access = relationship("UserSphereAccess", back_populates="identity", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Identity {self.identity_type}:{self.identity_name}>"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "identity_type": self.identity_type,
            "identity_name": self.identity_name,
            "is_default": self.is_default,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class IdentityPermission(Base):
    """
    Identity-specific permissions.
    
    Controls what each identity can access.
    """
    
    __tablename__ = "identity_permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id", ondelete="CASCADE"), nullable=False)
    
    permission_key = Column(String(100), nullable=False)
    permission_value = Column(JSON, default=dict)
    
    granted_at = Column(DateTime, default=datetime.utcnow)
    granted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    identity = relationship("Identity", back_populates="permissions")
    
    def __repr__(self):
        return f"<IdentityPermission {self.permission_key}>"


class UserSphereAccess(Base):
    """
    Controls which spheres each identity can access.
    """
    
    __tablename__ = "user_sphere_access"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id", ondelete="CASCADE"), nullable=False)
    sphere_id = Column(UUID(as_uuid=True), ForeignKey("spheres.id"), nullable=False)
    
    access_level = Column(String(20), default="full")  # full, read, limited
    granted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    identity = relationship("Identity", back_populates="sphere_access")
    sphere = relationship("Sphere", back_populates="user_access")
    
    def __repr__(self):
        return f"<UserSphereAccess {self.identity_id} -> {self.sphere_id}>"
