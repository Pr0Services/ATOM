"""
CHE·NU™ Security Module

JWT token handling, password hashing, and security utilities.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.core.config import settings


# ═══════════════════════════════════════════════════════════════════════════════
# PASSWORD HASHING
# ═══════════════════════════════════════════════════════════════════════════════

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class TokenPayload(BaseModel):
    """JWT token payload structure."""
    sub: str  # user_id
    identity_id: str  # identity boundary
    type: str  # access | refresh
    jti: str  # unique token id
    iat: datetime
    exp: datetime
    
    # Optional claims
    email: Optional[str] = None
    name: Optional[str] = None
    roles: list[str] = []


class TokenPair(BaseModel):
    """Access and refresh token pair."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_access_token(
    user_id: str,
    identity_id: str,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: User identifier
        identity_id: Identity boundary identifier
        additional_claims: Extra claims to include
        
    Returns:
        Encoded JWT string
    """
    now = datetime.utcnow()
    expires = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": user_id,
        "identity_id": identity_id,
        "type": "access",
        "jti": str(uuid4()),
        "iat": now,
        "exp": expires,
    }
    
    if additional_claims:
        payload.update(additional_claims)
    
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(
    user_id: str,
    identity_id: str,
) -> str:
    """
    Create a JWT refresh token.
    
    Refresh tokens have longer expiry and fewer claims.
    """
    now = datetime.utcnow()
    expires = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": user_id,
        "identity_id": identity_id,
        "type": "refresh",
        "jti": str(uuid4()),
        "iat": now,
        "exp": expires,
    }
    
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_token_pair(
    user_id: str,
    identity_id: str,
    additional_claims: Optional[Dict[str, Any]] = None,
) -> TokenPair:
    """Create both access and refresh tokens."""
    return TokenPair(
        access_token=create_access_token(user_id, identity_id, additional_claims),
        refresh_token=create_refresh_token(user_id, identity_id),
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

class TokenVerificationError(Exception):
    """Raised when token verification fails."""
    pass


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT string
        
    Returns:
        TokenPayload with decoded claims
        
    Raises:
        TokenVerificationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        
        return TokenPayload(
            sub=payload["sub"],
            identity_id=payload["identity_id"],
            type=payload["type"],
            jti=payload["jti"],
            iat=datetime.fromtimestamp(payload["iat"]),
            exp=datetime.fromtimestamp(payload["exp"]),
            email=payload.get("email"),
            name=payload.get("name"),
            roles=payload.get("roles", []),
        )
        
    except JWTError as e:
        raise TokenVerificationError(f"Invalid token: {e}")


def verify_access_token(token: str) -> TokenPayload:
    """Verify an access token."""
    payload = decode_token(token)
    
    if payload.type != "access":
        raise TokenVerificationError("Not an access token")
    
    return payload


def verify_refresh_token(token: str) -> TokenPayload:
    """Verify a refresh token."""
    payload = decode_token(token)
    
    if payload.type != "refresh":
        raise TokenVerificationError("Not a refresh token")
    
    return payload


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN BLACKLIST (Optional - for logout)
# ═══════════════════════════════════════════════════════════════════════════════

# In production, use Redis for token blacklist
_token_blacklist: set[str] = set()


def blacklist_token(jti: str) -> None:
    """Add token to blacklist (for logout)."""
    _token_blacklist.add(jti)


def is_token_blacklisted(jti: str) -> bool:
    """Check if token is blacklisted."""
    return jti in _token_blacklist


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY BOUNDARY
# ═══════════════════════════════════════════════════════════════════════════════

class IdentityBoundaryViolation(Exception):
    """Raised when access crosses identity boundaries."""
    
    def __init__(
        self,
        requested_identity: str,
        resource_identity: str,
        resource_type: str = "resource",
    ):
        self.requested_identity = requested_identity
        self.resource_identity = resource_identity
        self.resource_type = resource_type
        super().__init__(
            f"Identity boundary violation: {resource_type} belongs to "
            f"{resource_identity}, not {requested_identity}"
        )


def check_identity_boundary(
    token_identity: str,
    resource_identity: str,
    resource_type: str = "resource",
) -> bool:
    """
    Check if access is within identity boundary.
    
    Args:
        token_identity: Identity from JWT
        resource_identity: Identity that owns the resource
        resource_type: Type of resource for error message
        
    Returns:
        True if access is allowed
        
    Raises:
        IdentityBoundaryViolation: If identities don't match
    """
    if token_identity != resource_identity:
        raise IdentityBoundaryViolation(
            requested_identity=token_identity,
            resource_identity=resource_identity,
            resource_type=resource_type,
        )
    return True
