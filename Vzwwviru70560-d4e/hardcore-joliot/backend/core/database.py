"""
CHE·NU™ Database Configuration

Async SQLAlchemy setup with PostgreSQL.
Includes session management and connection pooling.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from backend.core.config import settings


# ═══════════════════════════════════════════════════════════════════════════════
# BASE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE & SESSION
# ═══════════════════════════════════════════════════════════════════════════════

def create_engine() -> AsyncEngine:
    """Create async database engine."""
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
    )


def create_test_engine() -> AsyncEngine:
    """Create engine for testing (no connection pooling)."""
    return create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        poolclass=NullPool,
    )


# Global engine instance
engine = create_engine()

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION DEPENDENCY
# ═══════════════════════════════════════════════════════════════════════════════

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.
    
    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions (non-FastAPI use).
    
    Usage:
        async with get_db_context() as db:
            result = await db.execute(...)
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ═══════════════════════════════════════════════════════════════════════════════
# LIFECYCLE
# ═══════════════════════════════════════════════════════════════════════════════

async def init_db() -> None:
    """Initialize database (create tables if not exist)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

async def check_db_health() -> bool:
    """Check database connectivity."""
    try:
        async with async_session_factory() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False
