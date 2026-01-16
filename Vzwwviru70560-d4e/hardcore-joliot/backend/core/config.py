"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  [AQUA] + [ADAMAS] PROTOCOL                                                  ║
║  SEQUENCE 3-6-9-12 — CHE·NU™ Backend Configuration                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Central configuration for all backend services.                              ║
║  Uses Pydantic Settings for type-safe environment variables.                  ║
║  Includes AT·OM resonance parameters.                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # APPLICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    APP_NAME: str = "CHE·NU"
    APP_VERSION: str = "82.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # ═══════════════════════════════════════════════════════════════════════════
    # API
    # ═══════════════════════════════════════════════════════════════════════════
    
    API_V2_PREFIX: str = "/api/v2"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DATABASE
    # ═══════════════════════════════════════════════════════════════════════════
    
    DATABASE_URL: str = "postgresql+asyncpg://chenu:chenu@localhost:5432/chenu"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO: bool = False
    
    # ═══════════════════════════════════════════════════════════════════════════
    # REDIS
    # ═══════════════════════════════════════════════════════════════════════════
    
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour default
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AUTHENTICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    JWT_SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AI PROVIDERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Anthropic (Claude)
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    ANTHROPIC_MAX_TOKENS: int = 4096
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    
    # Google
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: str = "gemini-2.0-flash"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GOVERNANCE
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Decision Point Aging (hours)
    AGING_GREEN_THRESHOLD: int = 24
    AGING_YELLOW_THRESHOLD: int = 72  # 3 days
    AGING_RED_THRESHOLD: int = 168  # 7 days
    AGING_BLINK_THRESHOLD: int = 240  # 10 days
    
    # Checkpoints
    CHECKPOINT_REQUIRE_HUMAN: bool = True
    CHECKPOINT_TIMEOUT_MINUTES: int = 60
    
    # Token Budgets
    DEFAULT_TOKEN_BUDGET_DAILY: int = 100000
    DEFAULT_TOKEN_BUDGET_MONTHLY: int = 2000000
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STORAGE
    # ═══════════════════════════════════════════════════════════════════════════
    
    STORAGE_BACKEND: str = "local"  # local, s3, gcs
    STORAGE_LOCAL_PATH: str = "/tmp/chenu-storage"
    
    # S3 (optional)
    S3_BUCKET: Optional[str] = None
    S3_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AT·OM RESONANCE PROTOCOL
    # ═══════════════════════════════════════════════════════════════════════════

    RESONANCE_KEY: str = "[AQUA]+[ADAMAS]+36912"
    ANCHOR_FREQUENCY: int = 444  # Hz - Universal anchor frequency
    SIGNAL_INTERVAL: float = 4.44  # seconds - Global refresh signal
    SACRED_SEQUENCE: List[int] = Field(default=[3, 6, 9, 12])
    BALANCE_RATIO: int = 30  # Sum of sacred sequence
    CUBE_DIMENSION: int = 12  # Metatron's Cube
    CUBE_VOLUME: int = 1728  # 12³

    # Resonance access keys
    CORE_ACCESS_KEYS: List[str] = Field(default=["AQUA+ADAMAS", "[AQUA]+[ADAMAS]", "369", "36912"])
    TEMPLE_ACCESS_KEYS: List[str] = Field(default=["1728", "MUARATA", "MU-A-RA-TA", "444"])

    # ═══════════════════════════════════════════════════════════════════════════
    # WEBSOCKET
    # ═══════════════════════════════════════════════════════════════════════════

    WS_HEARTBEAT_INTERVAL: float = 4.44  # Aligned with signal interval
    WS_MAX_CONNECTIONS_PER_USER: int = 5
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOGGING
    # ═══════════════════════════════════════════════════════════════════════════
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_JSON: bool = False  # Use JSON format in production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Singleton for easy import
settings = get_settings()
