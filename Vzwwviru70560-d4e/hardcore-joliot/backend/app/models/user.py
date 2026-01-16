"""
CHE·NU™ User Model

SQLAlchemy model for user accounts.
Each user has an identity_id for data isolation (Identity Boundary).
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """
    User account model.
    
    Identity Boundary:
    - Each user has a unique identity_id
    - All user data is scoped to this identity
    - Cross-identity access is FORBIDDEN (HTTP 403)
    """
    
    __tablename__ = "users"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PRIMARY KEYS
    # ═══════════════════════════════════════════════════════════════════════════
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Identity boundary - used for data isolation
    # In most cases, identity_id == id, but can differ for shared accounts
    identity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
        default=lambda: str(uuid4()),
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CREDENTIALS
    # ═══════════════════════════════════════════════════════════════════════════
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ROLES & PERMISSIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    roles: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATUS
    # ═══════════════════════════════════════════════════════════════════════════
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TOKEN BUDGETS (Governance)
    # ═══════════════════════════════════════════════════════════════════════════
    
    token_budget_daily: Mapped[int] = mapped_column(
        default=100000,
        nullable=False,
    )
    
    token_budget_monthly: Mapped[int] = mapped_column(
        default=2000000,
        nullable=False,
    )
    
    tokens_used_today: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    
    tokens_used_month: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SETTINGS
    # ═══════════════════════════════════════════════════════════════════════════
    
    settings: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMESTAMPS
    # ═══════════════════════════════════════════════════════════════════════════
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ═══════════════════════════════════════════════════════════════════════════
    
    # User's spheres (9 spheres per user)
    spheres = relationship("Sphere", back_populates="identity", lazy="dynamic")
    
    # User's threads
    threads = relationship("Thread", back_populates="identity", lazy="dynamic")
    
    # User's governance checkpoints
    checkpoints = relationship("GovernanceCheckpoint", back_populates="identity", lazy="dynamic")
    
    # User's audit logs
    audit_logs = relationship("AuditLog", back_populates="identity", lazy="dynamic")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in (self.roles or [])
    
    def add_role(self, role: str) -> None:
        """Add role to user."""
        if self.roles is None:
            self.roles = []
        if role not in self.roles:
            self.roles = [*self.roles, role]
    
    def remove_role(self, role: str) -> None:
        """Remove role from user."""
        if self.roles and role in self.roles:
            self.roles = [r for r in self.roles if r != role]
    
    def can_use_tokens(self, amount: int) -> bool:
        """Check if user has enough token budget."""
        return (
            self.tokens_used_today + amount <= self.token_budget_daily and
            self.tokens_used_month + amount <= self.token_budget_monthly
        )
    
    def use_tokens(self, amount: int) -> bool:
        """Deduct tokens from budget. Returns False if insufficient."""
        if not self.can_use_tokens(amount):
            return False
        self.tokens_used_today += amount
        self.tokens_used_month += amount
        return True
    
    def reset_daily_tokens(self) -> None:
        """Reset daily token usage (called by scheduler)."""
        self.tokens_used_today = 0
    
    def reset_monthly_tokens(self) -> None:
        """Reset monthly token usage (called by scheduler)."""
        self.tokens_used_month = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary (safe for API response)."""
        return {
            "id": self.id,
            "identity_id": self.identity_id,
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "roles": self.roles or [],
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "token_budget_daily": self.token_budget_daily,
            "token_budget_monthly": self.token_budget_monthly,
            "tokens_used_today": self.tokens_used_today,
            "tokens_used_month": self.tokens_used_month,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }


class RefreshToken(Base):
    """
    Refresh token storage for token rotation.
    
    Allows:
    - Token revocation (logout)
    - Token rotation (security)
    - Multi-device sessions
    """
    
    __tablename__ = "refresh_tokens"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
    )
    
    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )
    
    device_info: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),  # IPv6 max length
        nullable=True,
    )
    
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
