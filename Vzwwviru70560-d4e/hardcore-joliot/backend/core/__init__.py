"""
CHE·NU™ Core Module

Central configuration, security, database, and utilities.
"""

from backend.core.config import settings, get_settings
from backend.core.database import (
    Base,
    get_db,
    get_db_context,
    init_db,
    close_db,
    check_db_health,
    engine,
    async_session_factory,
)
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_token_pair,
    decode_token,
    verify_access_token,
    verify_refresh_token,
    blacklist_token,
    is_token_blacklisted,
    check_identity_boundary,
    TokenPayload,
    TokenPair,
    TokenVerificationError,
    IdentityBoundaryViolation,
)
from backend.core.redis import (
    get_redis,
    close_redis,
    check_redis_health,
    CacheService,
    PubSubService,
    session_cache,
    thread_cache,
    user_cache,
    agent_cache,
    rate_limit_cache,
    pubsub,
)
from backend.core.exceptions import (
    CHENUBaseException,
    AuthenticationError,
    AuthorizationError,
    IdentityBoundaryError,
    NotFoundError,
    ValidationError,
    CheckpointRequiredError,
    GovernanceViolationError,
    ThreadImmutabilityError,
    RateLimitExceededError,
    AIServiceError,
)
# AT·OM Ethical Safeguard - Protocole de Sécurité
from backend.core.security import (
    EthicalSafeguard,
    IntentionAnalyzer,
    FrequencySignature,
    BriseCircuit,
    DispersionMode,
    EthicalViolationType,
    SystemState,
)

__all__ = [
    # Config
    "settings",
    "get_settings",
    # Database
    "Base",
    "get_db",
    "get_db_context",
    "init_db",
    "close_db",
    "check_db_health",
    "engine",
    "async_session_factory",
    # Security
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "create_token_pair",
    "decode_token",
    "verify_access_token",
    "verify_refresh_token",
    "blacklist_token",
    "is_token_blacklisted",
    "check_identity_boundary",
    "TokenPayload",
    "TokenPair",
    "TokenVerificationError",
    "IdentityBoundaryViolation",
    # Redis
    "get_redis",
    "close_redis",
    "check_redis_health",
    "CacheService",
    "PubSubService",
    "session_cache",
    "thread_cache",
    "user_cache",
    "agent_cache",
    "rate_limit_cache",
    "pubsub",
    # Exceptions
    "CHENUBaseException",
    "AuthenticationError",
    "AuthorizationError",
    "IdentityBoundaryError",
    "NotFoundError",
    "ValidationError",
    "CheckpointRequiredError",
    "GovernanceViolationError",
    "ThreadImmutabilityError",
    "RateLimitExceededError",
    "AIServiceError",
    # AT·OM Ethical Safeguard
    "EthicalSafeguard",
    "IntentionAnalyzer",
    "FrequencySignature",
    "BriseCircuit",
    "DispersionMode",
    "EthicalViolationType",
    "SystemState",
]
