"""
============================================================================
CHE·NU™ V69 — API CORE CONFIGURATION
============================================================================
Version: 1.0.0
Purpose: Central API configuration and settings
Principle: Production-ready, secure, governed
============================================================================
"""

from datetime import timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import os


# ============================================================================
# ENVIRONMENT
# ============================================================================

class Environment(str, Enum):
    """Deployment environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# ============================================================================
# SETTINGS
# ============================================================================

class APISettings(BaseSettings):
    """
    API configuration settings.
    
    Values can be overridden via environment variables.
    """
    
    # Application
    app_name: str = "CHE·NU™ API"
    app_version: str = "1.0.0"
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production")
    api_key_header: str = "X-API-Key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    
    # OPA
    opa_enabled: bool = True
    opa_url: str = "http://localhost:8181"
    opa_policy_path: str = "/v1/data/chenu/allow"
    
    # Database (for future)
    database_url: str = "sqlite:///./chenu.db"
    
    # Redis (for caching/sessions)
    redis_url: str = "redis://localhost:6379"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # WebSocket
    ws_heartbeat_interval: int = 30
    ws_max_connections: int = 1000
    
    # File storage
    storage_path: str = "./storage"
    max_upload_size_mb: int = 100
    
    class Config:
        env_prefix = "CHENU_"
        env_file = ".env"


# ============================================================================
# API RESPONSES
# ============================================================================

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PaginatedResponse(APIResponse):
    """Paginated API response"""
    
    page: int = 1
    page_size: int = 20
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


class ErrorResponse(BaseModel):
    """Error response"""
    
    success: bool = False
    error: str
    error_code: str
    details: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None


# ============================================================================
# API ERRORS
# ============================================================================

class APIError(Exception):
    """Base API error"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "API_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found"""
    
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} not found: {resource_id}",
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "id": resource_id},
        )


class ValidationError(APIError):
    """Validation error"""
    
    def __init__(self, message: str, errors: List[Dict[str, Any]]):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details={"errors": errors},
        )


class AuthenticationError(APIError):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(APIError):
    """Authorization error"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
        )


class GovernanceError(APIError):
    """Governance checkpoint failed"""
    
    def __init__(self, message: str, checkpoint_id: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="GOVERNANCE_ERROR",
            status_code=403,
            details={"checkpoint_id": checkpoint_id},
        )


class RateLimitError(APIError):
    """Rate limit exceeded"""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMIT_ERROR",
            status_code=429,
            details={"retry_after": retry_after},
        )


# ============================================================================
# REQUEST CONTEXT
# ============================================================================

class RequestContext(BaseModel):
    """Context for API requests"""
    
    request_id: str
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    agent_id: Optional[str] = None
    
    # Permissions
    roles: Set[str] = Field(default_factory=set)
    permissions: Set[str] = Field(default_factory=set)
    
    # Governance
    environment: str = "labs"
    sphere: Optional[str] = None
    
    # Metadata
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    
    def has_permission(self, permission: str) -> bool:
        """Check if context has permission"""
        return permission in self.permissions or "admin" in self.roles
    
    def has_role(self, role: str) -> bool:
        """Check if context has role"""
        return role in self.roles


# ============================================================================
# API TAGS
# ============================================================================

API_TAGS = [
    {
        "name": "Health",
        "description": "Health check endpoints",
    },
    {
        "name": "Auth",
        "description": "Authentication and authorization",
    },
    {
        "name": "Simulations",
        "description": "Simulation management and execution",
    },
    {
        "name": "Scenarios",
        "description": "Scenario management and comparison",
    },
    {
        "name": "Agents",
        "description": "Agent management and communication",
    },
    {
        "name": "Checkpoints",
        "description": "Governance checkpoints and HITL",
    },
    {
        "name": "XR Packs",
        "description": "XR Pack generation and retrieval",
    },
    {
        "name": "Causal",
        "description": "Causal inference and DAG management",
    },
    {
        "name": "Audit",
        "description": "Audit logs and compliance",
    },
    {
        "name": "WebSocket",
        "description": "Real-time streaming endpoints",
    },
]


# ============================================================================
# FACTORY
# ============================================================================

_settings: Optional[APISettings] = None


def get_settings() -> APISettings:
    """Get API settings singleton"""
    global _settings
    if _settings is None:
        _settings = APISettings()
    return _settings


def get_environment() -> Environment:
    """Get current environment"""
    return get_settings().environment
