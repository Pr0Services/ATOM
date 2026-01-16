"""
CHE·NU™ Auth Schemas

Pydantic models for authentication requests and responses.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class RegisterRequest(BaseModel):
    """User registration request."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 chars)")
    name: str = Field(..., min_length=2, max_length=100, description="Display name")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Clean and validate name."""
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v


class LoginRequest(BaseModel):
    """User login request."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    
    refresh_token: str = Field(..., description="Refresh token from login")


class ChangePasswordRequest(BaseModel):
    """Password change request."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class UpdateProfileRequest(BaseModel):
    """Profile update request."""
    
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    bio: Optional[str] = Field(None, max_length=1000)
    settings: Optional[dict] = None


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class UserResponse(BaseModel):
    """User information response (safe, no password)."""
    
    id: str
    identity_id: str = Field(..., description="Identity boundary ID")
    email: str
    name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roles: List[str] = []
    is_active: bool = True
    is_verified: bool = False
    is_admin: bool = False
    token_budget_daily: int = 100000
    token_budget_monthly: int = 2000000
    tokens_used_today: int = 0
    tokens_used_month: int = 0
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token pair response."""
    
    access_token: str = Field(..., description="JWT access token (30 min)")
    refresh_token: str = Field(..., description="JWT refresh token (7 days)")
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiry in seconds")


class AuthResponse(BaseModel):
    """Full authentication response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    """Simple message response."""
    
    message: str


# ═══════════════════════════════════════════════════════════════════════════════
# INTERNAL SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class UserCreate(BaseModel):
    """Internal user creation model."""
    
    email: str
    hashed_password: str
    name: str
    roles: List[str] = ["user"]
    is_active: bool = True
    is_verified: bool = False


class UserUpdate(BaseModel):
    """Internal user update model."""
    
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    settings: Optional[dict] = None
    last_login_at: Optional[datetime] = None
