"""
===========================================================================================
NOVA-999 SOVEREIGN ARCHITECTURE - PRODUCTION DATABASE MODULE
===========================================================================================
Version: 999.0.0
Date: January 17, 2026
Platform: DigitalOcean App Platform (NYC9)

Features:
- Async PostgreSQL with asyncpg driver
- Connection pooling with automatic recycling
- SSL/TLS mandatory for managed databases
- Retry logic for transient connection failures
- Pool timeout handling (DigitalOcean specific)
- Health check with pool statistics
===========================================================================================
"""

import os
import logging
from typing import AsyncGenerator, Optional, Dict, Any
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, text
from sqlalchemy.exc import SQLAlchemyError, TimeoutError as SATimeoutError
from sqlalchemy.pool import AsyncAdaptedQueuePool
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# ===========================================================================================
# LOGGING
# ===========================================================================================

logger = logging.getLogger("nova999.database")

# ===========================================================================================
# DATABASE CONFIGURATION
# ===========================================================================================

class DatabaseConfig:
    """Database configuration from environment variables."""

    def __init__(self):
        self.database_url = self._build_database_url()

        # Pool settings optimized for DigitalOcean
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "1800"))  # 30 minutes
        self.connect_timeout = int(os.getenv("DB_CONNECT_TIMEOUT", "10"))
        self.command_timeout = int(os.getenv("DB_COMMAND_TIMEOUT", "60"))

        # Debug mode
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

    def _build_database_url(self) -> str:
        """
        Build database URL from environment.

        Handles:
        - DATABASE_URL (DigitalOcean format)
        - Individual POSTGRES_* variables
        - Automatic conversion to asyncpg format
        - SSL requirement for managed databases
        """
        database_url = os.getenv("DATABASE_URL", "")

        if not database_url:
            # Build from individual components
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            user = os.getenv("POSTGRES_USER", "chenu")
            password = os.getenv("POSTGRES_PASSWORD", "")
            db = os.getenv("POSTGRES_DB", "chenu_v76")

            if password:
                database_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
            else:
                database_url = f"postgresql://{user}@{host}:{port}/{db}"

        # Convert to asyncpg format
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif database_url.startswith("postgresql://") and "+asyncpg" not in database_url:
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Ensure SSL for production (DigitalOcean requirement)
        if database_url and os.getenv("ENVIRONMENT", "production") == "production":
            if "sslmode=" not in database_url and "ssl=" not in database_url:
                separator = "&" if "?" in database_url else "?"
                database_url += f"{separator}ssl=require"

        return database_url


# ===========================================================================================
# BASE MODEL
# ===========================================================================================

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """Base class for all database models."""
    metadata = metadata


# ===========================================================================================
# DATABASE MANAGER
# ===========================================================================================

class DatabaseManager:
    """
    Production-grade database manager for DigitalOcean PostgreSQL.

    Features:
    - Connection pooling with asyncpg
    - Automatic SSL for managed databases
    - Retry logic for transient failures
    - Pool timeout handling
    - Health monitoring
    """

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig()
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._is_connected = False

    @property
    def engine(self) -> Optional[AsyncEngine]:
        """Get the database engine."""
        return self._engine

    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._is_connected

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((ConnectionError, OSError, SATimeoutError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Database connection attempt {retry_state.attempt_number} failed. "
            f"Retrying in {retry_state.next_action.sleep}s..."
        )
    )
    async def connect(self) -> None:
        """
        Initialize database connection with retry logic.

        Handles DigitalOcean-specific connection requirements:
        - SSL/TLS mandatory for managed databases
        - Pool timeout management
        - Connection recycling for long-running apps

        Raises:
            RuntimeError: If connection fails after all retries
        """
        if not self.config.database_url:
            logger.warning("DATABASE_URL not set - running without database")
            return

        logger.info("Connecting to PostgreSQL (DigitalOcean Managed)...")
        logger.debug(f"Pool size: {self.config.pool_size}, Max overflow: {self.config.max_overflow}")

        try:
            # Create async engine with production settings
            self._engine = create_async_engine(
                self.config.database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,  # Validate connections before use
                echo=self.config.debug,
                connect_args={
                    "timeout": self.config.connect_timeout,
                    "command_timeout": self.config.command_timeout,
                    "server_settings": {
                        "application_name": "nova999_backend"
                    }
                }
            )

            # Create session factory
            self._session_factory = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False
            )

            # Test connection
            async with self._engine.begin() as conn:
                result = await conn.execute(text("SELECT 1 as health"))
                row = result.fetchone()
                if row and row[0] == 1:
                    self._is_connected = True
                    logger.info("Database connection established successfully")

        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Gracefully close database connections."""
        if self._engine:
            logger.info("Closing database connections...")
            await self._engine.dispose()
            self._is_connected = False
            logger.info("Database connections closed")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get database session with automatic cleanup.

        Usage:
            async with db_manager.session() as session:
                result = await session.execute(query)

        Yields:
            AsyncSession: Database session

        Raises:
            RuntimeError: If database is not initialized
        """
        if not self._session_factory:
            raise RuntimeError("Database not initialized. Call connect() first.")

        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error: {e}")
                raise
            finally:
                await session.close()

    async def health_check(self) -> Dict[str, Any]:
        """
        Check database health with pool statistics.

        Returns:
            Dict with status, version, and pool statistics
        """
        if not self._engine:
            return {
                "status": "disconnected",
                "message": "Database not configured"
            }

        try:
            async with self._engine.begin() as conn:
                # Get PostgreSQL version
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()

                # Get connection info
                result = await conn.execute(text(
                    "SELECT current_database(), current_user, inet_server_addr()"
                ))
                row = result.fetchone()

            # Get pool statistics
            pool = self._engine.pool
            pool_stats = {
                "size": pool.size() if hasattr(pool, 'size') else self.config.pool_size,
                "checked_in": pool.checkedin() if hasattr(pool, 'checkedin') else 0,
                "checked_out": pool.checkedout() if hasattr(pool, 'checkedout') else 0,
                "overflow": pool.overflow() if hasattr(pool, 'overflow') else 0,
            }

            return {
                "status": "healthy",
                "version": version,
                "database": row[0] if row else None,
                "user": row[1] if row else None,
                "server": str(row[2]) if row and row[2] else None,
                "pool": pool_stats,
                "config": {
                    "pool_size": self.config.pool_size,
                    "max_overflow": self.config.max_overflow,
                    "pool_timeout": self.config.pool_timeout,
                    "pool_recycle": self.config.pool_recycle
                }
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "error_type": type(e).__name__
            }

    async def execute_raw(self, query: str, params: Optional[Dict] = None) -> Any:
        """
        Execute raw SQL query.

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            Query result
        """
        async with self.session() as session:
            result = await session.execute(text(query), params or {})
            return result


# ===========================================================================================
# GLOBAL INSTANCE & DEPENDENCY
# ===========================================================================================

# Configuration
db_config = DatabaseConfig()

# Global database manager instance
db_manager = DatabaseManager(db_config)

# Engine reference (for backward compatibility)
engine: Optional[AsyncEngine] = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.

    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with db_manager.session() as session:
        yield session


async def get_db_optional() -> AsyncGenerator[Optional[AsyncSession], None]:
    """
    FastAPI dependency that yields a DB session or None if DB is unavailable.

    Usage:
        @router.get("/items")
        async def get_items(db: Optional[AsyncSession] = Depends(get_db_optional)):
            if db:
                result = await db.execute(select(Item))
                return result.scalars().all()
            return []  # Fallback
    """
    if not db_manager.is_connected:
        yield None
        return
    try:
        async with db_manager.session() as session:
            yield session
    except Exception:
        yield None


# ===========================================================================================
# LIFECYCLE FUNCTIONS
# ===========================================================================================

async def init_db() -> None:
    """
    Initialize database connection.
    Called during application startup.
    """
    global engine
    await db_manager.connect()
    engine = db_manager.engine


async def close_db() -> None:
    """
    Close database connection.
    Called during application shutdown.
    """
    global engine
    await db_manager.disconnect()
    engine = None


async def check_db_health() -> bool:
    """
    Quick health check for readiness probes.

    Returns:
        True if database is healthy, False otherwise
    """
    result = await db_manager.health_check()
    return result.get("status") == "healthy"


async def create_tables() -> None:
    """
    Create all tables (development only).
    In production, use Alembic migrations.
    """
    if not db_manager.engine:
        logger.warning("Cannot create tables - database not connected")
        return

    logger.info("Creating database tables...")
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def drop_tables() -> None:
    """
    Drop all tables (development only).
    WARNING: This will delete all data!
    """
    if not db_manager.engine:
        logger.warning("Cannot drop tables - database not connected")
        return

    logger.warning("Dropping all database tables...")
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("Database tables dropped")


# ===========================================================================================
# UTILITY FUNCTIONS
# ===========================================================================================

def get_database_url() -> str:
    """Get the configured database URL (masked for logging)."""
    url = db_config.database_url
    if not url:
        return "(not configured)"

    # Mask password in URL for safe logging
    if "@" in url:
        parts = url.split("@")
        credentials = parts[0].split("://")[1] if "://" in parts[0] else parts[0]
        if ":" in credentials:
            user = credentials.split(":")[0]
            masked = f"{url.split('://')[0]}://{user}:****@{parts[1]}"
            return masked

    return url


def get_pool_status() -> Dict[str, Any]:
    """Get current connection pool status."""
    if not db_manager.engine:
        return {"status": "not_initialized"}

    pool = db_manager.engine.pool
    return {
        "size": pool.size() if hasattr(pool, 'size') else db_config.pool_size,
        "checked_in": pool.checkedin() if hasattr(pool, 'checkedin') else 0,
        "checked_out": pool.checkedout() if hasattr(pool, 'checkedout') else 0,
        "overflow": pool.overflow() if hasattr(pool, 'overflow') else 0,
        "invalid": pool.invalidatedcount() if hasattr(pool, 'invalidatedcount') else 0,
    }
