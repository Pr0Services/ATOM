"""
CHE·NU™ Authentication Module

Re-exports from security module for backward compatibility.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
import uuid

from jose import JWTError, jwt

# Import from local config
try:
    from app.core.config import settings
except ImportError:
    from .config import settings

# ═══════════════════════════════════════════════════════════════════════════════
# SECURITY SCHEME
# ═══════════════════════════════════════════════════════════════════════════════

security = HTTPBearer(auto_error=False)


# ═══════════════════════════════════════════════════════════════════════════════
# USER MODEL (Simplified for auth)
# ═══════════════════════════════════════════════════════════════════════════════

class User:
    """User model for authentication context."""
    def __init__(
        self,
        id: str,
        email: str,
        username: str,
        identity_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        preferences: Optional[dict] = None,
    ):
        self.id = id
        self.email = email
        self.username = username
        self.identity_id = identity_id or id
        self.created_at = created_at or datetime.utcnow()
        self.preferences = preferences


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data (should include 'sub' for user_id)
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "access",
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> User:
    """
    FastAPI dependency to get current authenticated user.
    
    Returns mock user if no token provided (for development).
    In production, should require valid token.
    """
    # Development mode: return mock user if no auth
    if not credentials:
        return User(
            id="dev-user-001",
            email="dev@chenu.local",
            username="dev_user",
            identity_id="dev-identity-001",
        )
    
    # Validate token
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        
        # In production, fetch user from database
        # For now, create user from token
        return User(
            id=user_id,
            email=payload.get("email", f"{user_id}@chenu.local"),
            username=payload.get("name", user_id),
            identity_id=payload.get("identity_id", user_id),
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[User]:
    """
    FastAPI dependency for optional authentication.
    Returns None if no valid token.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "User",
    "create_access_token",
    "decode_token",
    "get_current_user",
    "get_optional_user",
    "security",
]
