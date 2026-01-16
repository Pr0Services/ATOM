"""
CHE·NU™ Auth Routes

Authentication endpoints:
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- GET /auth/me
- POST /auth/password/change
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    DuplicateResourceError,
    NotFoundError,
)
from backend.api.dependencies import get_current_user, CurrentUser
from backend.services.auth.auth_service import AuthService, get_auth_service
from backend.schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    UpdateProfileRequest,
    AuthResponse,
    TokenResponse,
    UserResponse,
    MessageResponse,
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="""
    Create a new user account.
    
    Returns access and refresh tokens on success.
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one letter
    - At least one number
    """,
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Register a new user."""
    service = get_auth_service(db)
    
    try:
        return await service.register(request)
    except DuplicateResourceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.to_dict(),
        )


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="""
    Authenticate with email and password.
    
    Returns:
    - **access_token**: JWT for API access (30 min expiry)
    - **refresh_token**: JWT for token renewal (7 days expiry)
    - **user**: User profile information
    """,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Login with email and password."""
    service = get_auth_service(db)
    
    try:
        return await service.login(request)
    except (InvalidCredentialsError, AuthenticationError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.to_dict(),
            headers={"WWW-Authenticate": "Bearer"},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN REFRESH
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="""
    Get new access token using refresh token.
    
    Call this when access token expires.
    Also rotates the refresh token for security.
    """,
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Refresh access token."""
    service = get_auth_service(db)
    
    try:
        return await service.refresh_tokens(request.refresh_token)
    except TokenExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "TOKEN_EXPIRED", "message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )
    except TokenInvalidError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "TOKEN_INVALID", "message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="""
    Invalidate current session.
    
    - Blacklists the current access token
    - Revokes all refresh tokens for this user
    """,
)
async def logout(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Logout current user."""
    service = get_auth_service(db)
    
    await service.logout(current_user.id, current_user.token_id)
    
    return MessageResponse(message="Logged out successfully")


@router.post(
    "/logout/all",
    response_model=MessageResponse,
    summary="Logout from all devices",
    description="Revoke all sessions across all devices.",
)
async def logout_all_devices(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Logout from all devices."""
    service = get_auth_service(db)
    
    await service.logout_all_devices(current_user.id)
    
    return MessageResponse(message="Logged out from all devices")


# ═══════════════════════════════════════════════════════════════════════════════
# CURRENT USER
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="""
    Get information about the authenticated user.
    
    Includes:
    - Profile information
    - **identity_id**: For identity boundary enforcement
    - Token budget usage
    """,
)
async def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Get current user profile."""
    service = get_auth_service(db)
    
    try:
        return await service.get_user_response(current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.to_dict(),
        )


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update profile",
    description="Update current user's profile information.",
)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Update current user profile."""
    service = get_auth_service(db)
    
    from backend.schemas.auth_schemas import UserUpdate
    update_data = UserUpdate(
        name=request.name,
        avatar_url=request.avatar_url,
        bio=request.bio,
        settings=request.settings,
    )
    
    return await service.update_profile(current_user.id, update_data)


# ═══════════════════════════════════════════════════════════════════════════════
# PASSWORD MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

@router.post(
    "/password/change",
    response_model=MessageResponse,
    summary="Change password",
    description="""
    Change password for current user.
    
    Requires current password for verification.
    After changing, all other sessions are invalidated.
    """,
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Change current user's password."""
    service = get_auth_service(db)
    
    try:
        await service.change_password(
            user_id=current_user.id,
            current_password=request.current_password,
            new_password=request.new_password,
        )
        return MessageResponse(message="Password changed successfully")
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "INVALID_PASSWORD", "message": "Current password is incorrect"},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN VALIDATION (for other services)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get(
    "/validate",
    summary="Validate token",
    description="Validate current access token. Returns 200 if valid, 401 if invalid.",
)
async def validate_token(
    current_user: CurrentUser = Depends(get_current_user),
) -> dict:
    """Validate current token."""
    return {
        "valid": True,
        "user_id": current_user.id,
        "identity_id": current_user.identity_id,
        "roles": current_user.roles,
    }
