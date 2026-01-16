"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Database Session Management
═══════════════════════════════════════════════════════════════════════════════

Async database session management with:
- Connection pooling
- Transaction support
- Identity context injection
- Audit logging hooks
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from uuid import UUID
import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool
from sqlalchemy import event

from .base import Base


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class DatabaseConfig:
    """Database configuration from environment."""
    
    def __init__(self):
        self.url = os.getenv(
            "CHENU_DATABASE_URL",
            "postgresql+asyncpg://chenu:chenu@localhost:5432/chenu"
        )
        self.pool_size = int(os.getenv("CHENU_DB_POOL_SIZE", "10"))
        self.max_overflow = int(os.getenv("CHENU_DB_MAX_OVERFLOW", "20"))
        self.pool_timeout = int(os.getenv("CHENU_DB_POOL_TIMEOUT", "30"))
        self.echo = os.getenv("CHENU_DB_ECHO", "false").lower() == "true"
    
    @property
    def is_test(self) -> bool:
        """Check if running in test mode."""
        return "test" in self.url or os.getenv("CHENU_TEST_MODE") == "true"


# Global config
db_config = DatabaseConfig()


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE & SESSION FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def create_engine(config: Optional[DatabaseConfig] = None) -> AsyncEngine:
    """
    Create async database engine.
    
    Uses NullPool for testing, connection pool for production.
    """
    config = config or db_config
    
    # Use NullPool for tests to avoid connection issues
    if config.is_test:
        return create_async_engine(
            config.url,
            echo=config.echo,
            poolclass=NullPool
        )
    
    # Production with connection pooling
    return create_async_engine(
        config.url,
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        pool_timeout=config.pool_timeout,
        pool_pre_ping=True  # Verify connections before use
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create async session factory."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )


# Global instances (initialized on startup)
_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


async def init_database(config: Optional[DatabaseConfig] = None) -> None:
    """
    Initialize database connection.
    
    Call this on application startup.
    """
    global _engine, _session_factory
    
    config = config or db_config
    _engine = create_engine(config)
    _session_factory = create_session_factory(_engine)
    
    # Create tables if they don't exist (for development)
    if config.is_test:
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def close_database() -> None:
    """
    Close database connection.
    
    Call this on application shutdown.
    """
    global _engine, _session_factory
    
    if _engine:
        await _engine.dispose()
        _engine = None
        _session_factory = None


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════

class SessionContext:
    """
    Session context with identity binding.
    
    R&D Rule #3: All operations are scoped to an identity.
    """
    
    def __init__(
        self,
        session: AsyncSession,
        identity_id: Optional[UUID] = None,
        request_id: Optional[UUID] = None
    ):
        self.session = session
        self.identity_id = identity_id
        self.request_id = request_id
    
    def with_identity(self, identity_id: UUID) -> "SessionContext":
        """Create new context with identity."""
        return SessionContext(
            session=self.session,
            identity_id=identity_id,
            request_id=self.request_id
        )


@asynccontextmanager
async def get_session(
    identity_id: Optional[UUID] = None,
    request_id: Optional[UUID] = None
) -> AsyncGenerator[SessionContext, None]:
    """
    Get database session with context.
    
    Usage:
        async with get_session(identity_id=user.id) as ctx:
            result = await ctx.session.execute(query)
    """
    if not _session_factory:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    async with _session_factory() as session:
        ctx = SessionContext(
            session=session,
            identity_id=identity_id,
            request_id=request_id
        )
        try:
            yield ctx
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_transaction(
    identity_id: Optional[UUID] = None,
    request_id: Optional[UUID] = None
) -> AsyncGenerator[SessionContext, None]:
    """
    Get database session with explicit transaction.
    
    Same as get_session but makes transaction explicit.
    """
    async with get_session(identity_id, request_id) as ctx:
        async with ctx.session.begin():
            yield ctx


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI DEPENDENCY
# ═══════════════════════════════════════════════════════════════════════════════

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database session.
    
    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    if not _session_factory:
        raise RuntimeError("Database not initialized")
    
    async with _session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ═══════════════════════════════════════════════════════════════════════════════
# UNIT OF WORK PATTERN
# ═══════════════════════════════════════════════════════════════════════════════

class UnitOfWork:
    """
    Unit of Work pattern for coordinating repositories.
    
    Ensures all operations in a business transaction use the same session.
    
    Usage:
        async with UnitOfWork(identity_id=user.id) as uow:
            thread = await uow.threads.create(...)
            await uow.audit.log(...)
            await uow.commit()
    """
    
    def __init__(
        self,
        identity_id: Optional[UUID] = None,
        request_id: Optional[UUID] = None
    ):
        self.identity_id = identity_id
        self.request_id = request_id
        self._session: Optional[AsyncSession] = None
        
        # Repositories (lazy initialized)
        self._threads = None
        self._checkpoints = None
        self._audit = None
    
    async def __aenter__(self) -> "UnitOfWork":
        if not _session_factory:
            raise RuntimeError("Database not initialized")
        
        self._session = _session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self._session.close()
    
    async def commit(self):
        """Commit the transaction."""
        await self._session.commit()
    
    async def rollback(self):
        """Rollback the transaction."""
        await self._session.rollback()
    
    @property
    def session(self) -> AsyncSession:
        """Get the current session."""
        if not self._session:
            raise RuntimeError("UnitOfWork not entered")
        return self._session
    
    @property
    def threads(self):
        """Get thread repository."""
        if not self._threads:
            from .base_repository import ThreadRepository
            self._threads = ThreadRepository(self.session)
        return self._threads
    
    @property
    def checkpoints(self):
        """Get checkpoint repository."""
        if not self._checkpoints:
            from .base_repository import CheckpointRepository
            self._checkpoints = CheckpointRepository(self.session)
        return self._checkpoints
    
    @property
    def audit(self):
        """Get audit log repository."""
        if not self._audit:
            from .base_repository import AuditLogRepository
            self._audit = AuditLogRepository(self.session)
        return self._audit


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

async def check_database_health() -> dict:
    """
    Check database connectivity.
    
    Returns health status for monitoring endpoints.
    """
    try:
        async with get_session() as ctx:
            result = await ctx.session.execute("SELECT 1")
            result.scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "pool_size": db_config.pool_size if _engine else 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "DatabaseConfig",
    "db_config",
    "create_engine",
    "create_session_factory",
    "init_database",
    "close_database",
    "SessionContext",
    "get_session",
    "get_transaction",
    "get_db",
    "UnitOfWork",
    "check_database_health",
]
