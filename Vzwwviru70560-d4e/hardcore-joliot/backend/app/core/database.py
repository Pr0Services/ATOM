"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — DATABASE CONNECTION
═══════════════════════════════════════════════════════════════════════════════
Async PostgreSQL connection with SQLAlchemy 2.0
═══════════════════════════════════════════════════════════════════════════════
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from typing import AsyncGenerator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# NAMING CONVENTION FOR CONSTRAINTS
# ═══════════════════════════════════════════════════════════════════════════════

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


# ═══════════════════════════════════════════════════════════════════════════════
# BASE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Base(DeclarativeBase):
    """Base class for all database models."""
    metadata = metadata


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE & SESSION
# ═══════════════════════════════════════════════════════════════════════════════

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    echo=settings.DEBUG,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY INJECTION
# ═══════════════════════════════════════════════════════════════════════════════

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Usage:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE LIFECYCLE
# ═══════════════════════════════════════════════════════════════════════════════

async def init_db() -> None:
    """Initialize database connection."""
    logger.info("Initializing database connection...")
    try:
        async with engine.begin() as conn:
            # Test connection
            await conn.run_sync(lambda _: None)
        logger.info("✅ Database connection established")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise


async def close_db() -> None:
    """Close database connection."""
    logger.info("Closing database connection...")
    await engine.dispose()
    logger.info("✅ Database connection closed")


async def create_tables() -> None:
    """Create all tables (for development only)."""
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")


async def drop_tables() -> None:
    """Drop all tables (for development only)."""
    logger.warning("⚠️ Dropping all database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info("✅ Database tables dropped")
