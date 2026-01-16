"""
CHE·NU™ V75 Backend - User Model

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base


class User(Base):
    """User account model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    avatar_url = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    roles = Column(ARRAY(String), default=["user"])
    permissions = Column(ARRAY(String), default=["read", "write"])
    
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    identities = relationship("Identity", back_populates="user", cascade="all, delete-orphan")
    threads = relationship("Thread", back_populates="user", cascade="all, delete-orphan")
    hired_agents = relationship("HiredAgent", back_populates="user", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="user", foreign_keys="Decision.user_id")
    dataspaces = relationship("DataSpace", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return "admin" in (self.roles or [])
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        return permission in (self.permissions or [])


class Identity(Base):
    """User identity (personal, enterprise, creative, etc.)."""
    
    __tablename__ = "identities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    identity_type = Column(String(50), nullable=False)
    identity_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    config = Column(Text, default="{}")  # JSON stored as text
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="identities")
    
    def __repr__(self):
        return f"<Identity {self.identity_name} ({self.identity_type})>"
