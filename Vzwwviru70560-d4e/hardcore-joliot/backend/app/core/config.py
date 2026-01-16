"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — CORE CONFIGURATION
═══════════════════════════════════════════════════════════════════════════════
Database, Redis, and application settings
═══════════════════════════════════════════════════════════════════════════════
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ═══════════════════════════════════════════════════════════════════════════
    # APPLICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    APP_NAME: str = "CHE·NU™"
    APP_VERSION: str = "76.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="development", description="development | staging | production")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # API
    # ═══════════════════════════════════════════════════════════════════════════
    
    API_V2_PREFIX: str = "/api/v2"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DATABASE (PostgreSQL)
    # ═══════════════════════════════════════════════════════════════════════════
    
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_USER: str = Field(default="chenu", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(default="chenu_secret", description="PostgreSQL password")
    POSTGRES_DB: str = Field(default="chenu_v76", description="PostgreSQL database")
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Construct sync database URL for Alembic."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Connection pool settings
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # ═══════════════════════════════════════════════════════════════════════════
    # REDIS
    # ═══════════════════════════════════════════════════════════════════════════
    
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Cache TTL settings (seconds)
    CACHE_TTL_SHORT: int = 60          # 1 minute
    CACHE_TTL_MEDIUM: int = 300        # 5 minutes
    CACHE_TTL_LONG: int = 3600         # 1 hour
    CACHE_TTL_HOT_MEMORY: int = 300    # 5 minutes (tri-layer memory)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AUTHENTICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    JWT_SECRET_KEY: str = Field(default="chenu-secret-key-change-in-production", description="JWT secret")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ═══════════════════════════════════════════════════════════════════════════
    # R&D RULES CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Rule #1: Human Sovereignty
    CHECKPOINT_TIMEOUT_SECONDS: int = 3600  # 1 hour to approve/reject
    
    # Rule #5: No Ranking
    DEFAULT_ORDER_BY: str = "created_at"
    DEFAULT_ORDER_DIRECTION: str = "DESC"
    
    # Rule #7: Frozen Architecture
    SPHERES_COUNT: int = 9
    BUREAU_SECTIONS_COUNT: int = 6
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NOVA PIPELINE
    # ═══════════════════════════════════════════════════════════════════════════
    
    NOVA_MAX_PARALLEL_LANES: int = 7
    NOVA_LANE_TIMEOUT_SECONDS: int = 30
    NOVA_DEFAULT_TOKEN_BUDGET: int = 10000
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXTERNAL SERVICES (AI)
    # ═══════════════════════════════════════════════════════════════════════════
    
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOGGING
    # ═══════════════════════════════════════════════════════════════════════════
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience export
settings = get_settings()
