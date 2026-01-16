"""
CHE·NU™ Exception Definitions

Centralized exception handling for the entire backend.
All custom exceptions inherit from CHENUBaseException.
"""

from typing import Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════════════════════
# BASE EXCEPTION
# ═══════════════════════════════════════════════════════════════════════════════

class CHENUBaseException(Exception):
    """Base exception for all CHE·NU errors."""
    
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.details = details or {}
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API response format."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION EXCEPTIONS (401)
# ═══════════════════════════════════════════════════════════════════════════════

class AuthenticationError(CHENUBaseException):
    """Authentication failed."""
    status_code = 401
    error_code = "AUTHENTICATION_FAILED"


class InvalidCredentialsError(AuthenticationError):
    """Invalid username or password."""
    error_code = "INVALID_CREDENTIALS"


class TokenExpiredError(AuthenticationError):
    """JWT token has expired."""
    error_code = "TOKEN_EXPIRED"


class TokenInvalidError(AuthenticationError):
    """JWT token is invalid."""
    error_code = "TOKEN_INVALID"


class TokenBlacklistedError(AuthenticationError):
    """JWT token has been blacklisted (logged out)."""
    error_code = "TOKEN_BLACKLISTED"


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORIZATION EXCEPTIONS (403)
# ═══════════════════════════════════════════════════════════════════════════════

class AuthorizationError(CHENUBaseException):
    """Authorization failed."""
    status_code = 403
    error_code = "AUTHORIZATION_FAILED"


class IdentityBoundaryError(AuthorizationError):
    """
    Identity boundary violation (HTTP 403).
    
    R&D Rule: Each user only sees their own data.
    Cross-identity access is FORBIDDEN.
    """
    error_code = "IDENTITY_BOUNDARY_VIOLATION"
    
    def __init__(
        self,
        requested_identity: str,
        resource_identity: str,
        resource_type: str = "resource",
    ):
        super().__init__(
            message=f"Access denied: {resource_type} belongs to different identity",
            details={
                "requested_identity": requested_identity,
                "resource_identity": resource_identity,
                "resource_type": resource_type,
            },
        )


class InsufficientPermissionsError(AuthorizationError):
    """User lacks required permissions."""
    error_code = "INSUFFICIENT_PERMISSIONS"


# Alias for common usage
ForbiddenError = AuthorizationError


class SphereAccessDeniedError(AuthorizationError):
    """User cannot access this sphere."""
    error_code = "SPHERE_ACCESS_DENIED"


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE EXCEPTIONS (404)
# ═══════════════════════════════════════════════════════════════════════════════

class NotFoundError(CHENUBaseException):
    """Resource not found."""
    status_code = 404
    error_code = "NOT_FOUND"


class UserNotFoundError(NotFoundError):
    """User not found."""
    error_code = "USER_NOT_FOUND"


class ThreadNotFoundError(NotFoundError):
    """Thread not found."""
    error_code = "THREAD_NOT_FOUND"


class SphereNotFoundError(NotFoundError):
    """Sphere not found."""
    error_code = "SPHERE_NOT_FOUND"


class AgentNotFoundError(NotFoundError):
    """Agent not found."""
    error_code = "AGENT_NOT_FOUND"


class DecisionPointNotFoundError(NotFoundError):
    """Decision point not found."""
    error_code = "DECISION_POINT_NOT_FOUND"


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION EXCEPTIONS (400, 422)
# ═══════════════════════════════════════════════════════════════════════════════

class ValidationError(CHENUBaseException):
    """Request validation failed."""
    status_code = 422
    error_code = "VALIDATION_ERROR"


class InvalidInputError(CHENUBaseException):
    """Invalid input provided."""
    status_code = 400
    error_code = "INVALID_INPUT"


class DuplicateResourceError(CHENUBaseException):
    """Resource already exists."""
    status_code = 409
    error_code = "DUPLICATE_RESOURCE"


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE EXCEPTIONS (423)
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointRequiredError(CHENUBaseException):
    """
    Checkpoint required - action blocked pending human approval (HTTP 423).
    
    R&D Rule #1: HUMAN SOVEREIGNTY
    Sensitive actions MUST be approved by human before execution.
    """
    status_code = 423
    error_code = "CHECKPOINT_REQUIRED"
    
    def __init__(
        self,
        checkpoint_id: str,
        checkpoint_type: str,
        reason: str,
        options: list[str] = None,
        decision_point_id: Optional[str] = None,
    ):
        super().__init__(
            message=reason,
            details={
                "checkpoint_id": checkpoint_id,
                "checkpoint_type": checkpoint_type,
                "requires_approval": True,
                "options": options or ["approve", "reject"],
                "decision_point_id": decision_point_id,
            },
        )
        self.checkpoint_id = checkpoint_id
        self.checkpoint_type = checkpoint_type
        self.decision_point_id = decision_point_id


class GovernanceViolationError(CHENUBaseException):
    """Governance rule violated."""
    status_code = 403
    error_code = "GOVERNANCE_VIOLATION"


class ThreadImmutabilityError(GovernanceViolationError):
    """
    Attempt to modify immutable Thread data.
    
    R&D Rule: Threads are APPEND-ONLY.
    No updates, no deletes on ThreadEvents.
    """
    error_code = "THREAD_IMMUTABILITY_VIOLATION"


class CrossSphereViolationError(GovernanceViolationError):
    """
    Implicit cross-sphere data access attempted.
    
    R&D Rule #3: SPHERE INTEGRITY
    Cross-sphere requires EXPLICIT workflow.
    """
    error_code = "CROSS_SPHERE_VIOLATION"


# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMITING (429)
# ═══════════════════════════════════════════════════════════════════════════════

class RateLimitExceededError(CHENUBaseException):
    """Rate limit exceeded."""
    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"
    
    def __init__(
        self,
        limit: int,
        window: int,
        retry_after: int,
    ):
        super().__init__(
            message=f"Rate limit exceeded: {limit} requests per {window}s",
            details={
                "limit": limit,
                "window": window,
                "retry_after": retry_after,
            },
        )
        self.retry_after = retry_after


class TokenBudgetExceededError(RateLimitExceededError):
    """AI token budget exceeded."""
    error_code = "TOKEN_BUDGET_EXCEEDED"


# ═══════════════════════════════════════════════════════════════════════════════
# AI/AGENT EXCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class AIServiceError(CHENUBaseException):
    """AI service error."""
    status_code = 502
    error_code = "AI_SERVICE_ERROR"


class AgentExecutionError(CHENUBaseException):
    """Agent execution failed."""
    status_code = 500
    error_code = "AGENT_EXECUTION_ERROR"


class NovaTimeoutError(CHENUBaseException):
    """Nova pipeline timeout."""
    status_code = 504
    error_code = "NOVA_TIMEOUT"


# ═══════════════════════════════════════════════════════════════════════════════
# XR EXCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class XRRenderError(CHENUBaseException):
    """XR rendering failed."""
    status_code = 500
    error_code = "XR_RENDER_ERROR"


class MaturityNotMetError(CHENUBaseException):
    """Thread doesn't meet XR maturity requirements."""
    status_code = 400
    error_code = "MATURITY_NOT_MET"


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE EXCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class DatabaseError(CHENUBaseException):
    """Database operation failed."""
    status_code = 500
    error_code = "DATABASE_ERROR"


class TransactionError(DatabaseError):
    """Transaction failed."""
    error_code = "TRANSACTION_ERROR"
