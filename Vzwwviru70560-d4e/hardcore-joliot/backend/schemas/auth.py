"""
CHE·NU™ V75 Backend - Auth Schemas

@version 75.0.0
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class LoginRequest(BaseModel):
    """Login request."""
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterRequest(BaseModel):
    """Registration request."""
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=2, max_length=100)
    accept_terms: bool = True


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""
    token: str
    new_password: str = Field(min_length=8)


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class User(BaseModel):
    """User information."""
    id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    roles: List[str] = ["user"]
    permissions: List[str] = []
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AuthTokens(BaseModel):
    """Authentication tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


class AuthResponse(BaseModel):
    """Authentication response with user and tokens."""
    user: User
    tokens: AuthTokens


# ============================================================================
# SESSION SCHEMAS
# ============================================================================

class Session(BaseModel):
    """User session."""
    id: str
    user_id: str
    device: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    is_current: bool = False


class ActiveSessions(BaseModel):
    """List of active sessions."""
    sessions: List[Session]
    current_session_id: str
