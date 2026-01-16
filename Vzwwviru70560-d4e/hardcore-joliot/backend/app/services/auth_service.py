"""
CHE·NU™ Auth Service

Complete authentication service with:
- User registration
- Login/logout
- Token management
- Password changes
- Identity boundary enforcement
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import uuid4
import hashlib
import logging

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_token_pair,
    verify_refresh_token,
    blacklist_token,
    TokenPayload,
    TokenPair,
)
from app.core.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    NotFoundError,
    DuplicateResourceError,
    ValidationError,
)
from app.models.user import User, RefreshToken
from app.schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    UserCreate,
    UserUpdate,
    UserResponse,
    AuthResponse,
    TokenResponse,
)

logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication service.
    
    Handles all auth operations with proper error handling
    and audit logging.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ═══════════════════════════════════════════════════════════════════════════
    # USER REGISTRATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def register(self, request: RegisterRequest) -> AuthResponse:
        """
        Register a new user.
        
        Args:
            request: Registration data
            
        Returns:
            AuthResponse with tokens and user info
            
        Raises:
            DuplicateResourceError: If email already exists
        """
        # Check if email already exists
        existing = await self._get_user_by_email(request.email)
        if existing:
            logger.warning(f"Registration attempt with existing email: {request.email}")
            raise DuplicateResourceError(
                message="Email already registered",
                details={"email": request.email},
            )
        
        # Create user
        user_id = str(uuid4())
        identity_id = user_id  # Same as user_id by default
        
        user = User(
            id=user_id,
            identity_id=identity_id,
            email=request.email.lower(),
            hashed_password=hash_password(request.password),
            name=request.name,
            roles=["user"],
            is_active=True,
            is_verified=False,
            token_budget_daily=settings.DEFAULT_TOKEN_BUDGET_DAILY,
            token_budget_monthly=settings.DEFAULT_TOKEN_BUDGET_MONTHLY,
        )
        
        self.db.add(user)
        
        try:
            await self.db.flush()
        except IntegrityError:
            await self.db.rollback()
            raise DuplicateResourceError(
                message="Email already registered",
                details={"email": request.email},
            )
        
        # Generate tokens
        token_pair = create_token_pair(
            user_id=user_id,
            identity_id=identity_id,
            additional_claims={
                "email": user.email,
                "name": user.name,
                "roles": user.roles,
            },
        )
        
        # Store refresh token
        await self._store_refresh_token(user_id, token_pair.refresh_token)
        
        await self.db.commit()
        
        logger.info(f"New user registered: {user.email} (id={user_id})")
        
        return AuthResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type="bearer",
            expires_in=token_pair.expires_in,
            user=UserResponse.model_validate(user),
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOGIN
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def login(self, request: LoginRequest) -> AuthResponse:
        """
        Authenticate user with email and password.
        
        Args:
            request: Login credentials
            
        Returns:
            AuthResponse with tokens and user info
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Get user by email
        user = await self._get_user_by_email(request.email)
        
        if not user:
            logger.warning(f"Login attempt for non-existent email: {request.email}")
            raise InvalidCredentialsError(
                message="Invalid email or password",
            )
        
        # Verify password
        if not verify_password(request.password, user.hashed_password):
            logger.warning(f"Failed login attempt for: {request.email}")
            raise InvalidCredentialsError(
                message="Invalid email or password",
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt for deactivated account: {request.email}")
            raise AuthenticationError(
                message="Account is deactivated",
            )
        
        # Generate tokens
        token_pair = create_token_pair(
            user_id=user.id,
            identity_id=user.identity_id,
            additional_claims={
                "email": user.email,
                "name": user.name,
                "roles": user.roles or [],
            },
        )
        
        # Store refresh token
        await self._store_refresh_token(user.id, token_pair.refresh_token)
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.db.commit()
        
        logger.info(f"User logged in: {user.email}")
        
        return AuthResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            token_type="bearer",
            expires_in=token_pair.expires_in,
            user=UserResponse.model_validate(user),
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TOKEN REFRESH
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New token pair
            
        Raises:
            TokenInvalidError: If refresh token is invalid
            TokenExpiredError: If refresh token is expired
        """
        try:
            # Verify refresh token
            payload = verify_refresh_token(refresh_token)
            
        except Exception as e:
            if "expired" in str(e).lower():
                raise TokenExpiredError(message="Refresh token has expired")
            raise TokenInvalidError(message="Invalid refresh token")
        
        # Check if token is revoked
        token_hash = self._hash_token(refresh_token)
        stored_token = await self._get_refresh_token(token_hash)
        
        if not stored_token or stored_token.is_revoked:
            raise TokenInvalidError(message="Refresh token has been revoked")
        
        # Get user
        user = await self._get_user_by_id(payload.sub)
        if not user or not user.is_active:
            raise TokenInvalidError(message="User not found or inactive")
        
        # Revoke old refresh token
        stored_token.is_revoked = True
        
        # Generate new tokens
        token_pair = create_token_pair(
            user_id=user.id,
            identity_id=user.identity_id,
            additional_claims={
                "email": user.email,
                "name": user.name,
                "roles": user.roles or [],
            },
        )
        
        # Store new refresh token
        await self._store_refresh_token(user.id, token_pair.refresh_token)
        
        await self.db.commit()
        
        logger.info(f"Tokens refreshed for user: {user.email}")
        
        return TokenResponse(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            expires_in=token_pair.expires_in,
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOGOUT
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def logout(self, user_id: str, token_jti: str) -> None:
        """
        Logout user by blacklisting their current token.
        
        Args:
            user_id: User ID
            token_jti: JWT token ID to blacklist
        """
        # Blacklist the access token
        blacklist_token(token_jti)
        
        # Revoke all refresh tokens for this user (optional: just current session)
        await self._revoke_user_refresh_tokens(user_id)
        
        await self.db.commit()
        
        logger.info(f"User logged out: {user_id}")
    
    async def logout_all_devices(self, user_id: str) -> None:
        """
        Logout user from all devices.
        
        Args:
            user_id: User ID
        """
        await self._revoke_user_refresh_tokens(user_id)
        await self.db.commit()
        
        logger.info(f"User logged out from all devices: {user_id}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASSWORD MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> None:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password for verification
            new_password: New password
            
        Raises:
            InvalidCredentialsError: If current password is wrong
        """
        user = await self._get_user_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError(message="Current password is incorrect")
        
        # Update password
        user.hashed_password = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        
        # Revoke all refresh tokens (security: force re-login on all devices)
        await self._revoke_user_refresh_tokens(user_id)
        
        await self.db.commit()
        
        logger.info(f"Password changed for user: {user_id}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # USER RETRIEVAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return await self._get_user_by_id(user_id)
    
    async def get_user_response(self, user_id: str) -> UserResponse:
        """Get user as response model."""
        user = await self._get_user_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        return UserResponse.model_validate(user)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PROFILE UPDATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def update_profile(
        self,
        user_id: str,
        update_data: UserUpdate,
    ) -> UserResponse:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            update_data: Fields to update
            
        Returns:
            Updated user response
        """
        user = await self._get_user_by_id(user_id)
        if not user:
            raise NotFoundError(message="User not found")
        
        # Update fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            if value is not None:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await self.db.commit()
        
        logger.info(f"Profile updated for user: {user_id}")
        
        return UserResponse.model_validate(user)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PRIVATE HELPERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (case-insensitive)."""
        result = await self.db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()
    
    async def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    def _hash_token(self, token: str) -> str:
        """Hash a token for storage."""
        return hashlib.sha256(token.encode()).hexdigest()
    
    async def _store_refresh_token(
        self,
        user_id: str,
        refresh_token: str,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> None:
        """Store refresh token in database."""
        token_hash = self._hash_token(refresh_token)
        expires_at = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        stored_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires_at,
        )
        
        self.db.add(stored_token)
    
    async def _get_refresh_token(self, token_hash: str) -> Optional[RefreshToken]:
        """Get refresh token by hash."""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
    
    async def _revoke_user_refresh_tokens(self, user_id: str) -> None:
        """Revoke all refresh tokens for a user."""
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .where(RefreshToken.is_revoked == False)
            .values(is_revoked=True)
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def get_auth_service(db: AsyncSession) -> AuthService:
    """Factory function for AuthService."""
    return AuthService(db)
