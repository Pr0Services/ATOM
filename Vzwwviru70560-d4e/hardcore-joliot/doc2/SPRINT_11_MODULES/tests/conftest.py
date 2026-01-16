"""
CHE·NU™ - PYTEST CONFTEST
Shared fixtures for all tests
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta
import uuid
import os

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

from app.main import app
from app.db.models import Base, User, Thread, TokenBudget, Agent
from app.db.session import get_db
from app.core.config import settings


# ═══════════════════════════════════════════════════════════════
# DATABASE FIXTURES
# ═══════════════════════════════════════════════════════════════

# Test database URL (SQLite for speed)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
SYNC_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engines
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

sync_test_engine = create_engine(
    SYNC_TEST_DATABASE_URL,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create all tables before tests, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Cleanup test database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a test database session."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    """Override the get_db dependency."""
    async def _override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════
# CLIENT FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def client(override_get_db) -> Generator[TestClient, None, None]:
    """Sync test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ═══════════════════════════════════════════════════════════════
# USER FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=str(uuid.uuid4()),
        email=f"test_{uuid.uuid4().hex[:8]}@chenu.io",
        username=f"testuser_{uuid.uuid4().hex[:8]}",
        display_name="Test User",
        password_hash="hashed_password",
        role="user",
        token_balance=10000,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Generate auth headers for test user."""
    # In real tests, you'd generate a proper JWT
    return {
        "Authorization": f"Bearer test-token-{test_user.id}",
        "X-User-Id": test_user.id,
    }


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """Create an admin user."""
    user = User(
        id=str(uuid.uuid4()),
        email=f"admin_{uuid.uuid4().hex[:8]}@chenu.io",
        username=f"admin_{uuid.uuid4().hex[:8]}",
        display_name="Admin User",
        password_hash="hashed_password",
        role="admin",
        token_balance=100000,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


# ═══════════════════════════════════════════════════════════════
# THREAD FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
async def test_thread(db_session: AsyncSession, test_user: User) -> Thread:
    """Create a test thread."""
    thread = Thread(
        id=str(uuid.uuid4()),
        title="Test Thread",
        description="A thread for testing",
        sphere_id="personal",
        owner_id=test_user.id,
        status="active",
        token_budget=5000,
        tokens_used=0,
        encoding_mode="standard",
    )
    db_session.add(thread)
    await db_session.commit()
    await db_session.refresh(thread)
    return thread


@pytest.fixture
async def multiple_threads(db_session: AsyncSession, test_user: User) -> list[Thread]:
    """Create multiple test threads."""
    spheres = ["personal", "business", "studio"]
    threads = []
    
    for i, sphere in enumerate(spheres):
        thread = Thread(
            id=str(uuid.uuid4()),
            title=f"Test Thread {i + 1}",
            sphere_id=sphere,
            owner_id=test_user.id,
            status="active",
            token_budget=5000,
            tokens_used=i * 100,
        )
        db_session.add(thread)
        threads.append(thread)
    
    await db_session.commit()
    for thread in threads:
        await db_session.refresh(thread)
    
    return threads


# ═══════════════════════════════════════════════════════════════
# TOKEN BUDGET FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
async def test_budget(db_session: AsyncSession, test_user: User) -> TokenBudget:
    """Create a test token budget."""
    budget = TokenBudget(
        id=str(uuid.uuid4()),
        name="Test Budget",
        owner_id=test_user.id,
        sphere_id="personal",
        total_allocated=10000,
        total_used=2500,
        period="monthly",
        reset_at=datetime.utcnow() + timedelta(days=30),
    )
    db_session.add(budget)
    await db_session.commit()
    await db_session.refresh(budget)
    return budget


@pytest.fixture
async def multiple_budgets(db_session: AsyncSession, test_user: User) -> list[TokenBudget]:
    """Create multiple token budgets."""
    budgets = []
    spheres = ["personal", "business", "studio"]
    
    for i, sphere in enumerate(spheres):
        budget = TokenBudget(
            id=str(uuid.uuid4()),
            name=f"{sphere.title()} Budget",
            owner_id=test_user.id,
            sphere_id=sphere,
            total_allocated=10000 * (i + 1),
            total_used=1000 * i,
            period="monthly",
        )
        db_session.add(budget)
        budgets.append(budget)
    
    await db_session.commit()
    for budget in budgets:
        await db_session.refresh(budget)
    
    return budgets


# ═══════════════════════════════════════════════════════════════
# AGENT FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
async def test_agent(db_session: AsyncSession) -> Agent:
    """Create a test agent."""
    agent = Agent(
        id=str(uuid.uuid4()),
        name="Test Agent",
        type="specialist",
        description="A test agent",
        avatar="🤖",
        capabilities=["analysis", "reporting"],
        sphere_scopes=["personal", "business"],
        base_cost_per_token=0.001,
        is_system=False,
        is_active=True,
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)
    return agent


@pytest.fixture
async def nova_agent(db_session: AsyncSession) -> Agent:
    """Create Nova (system agent)."""
    agent = Agent(
        id="nova",
        name="Nova",
        type="nova",
        description="System intelligence",
        avatar="✧",
        capabilities=["guidance", "memory", "governance", "supervision"],
        sphere_scopes=["all"],
        base_cost_per_token=0.0005,
        is_system=True,
        is_active=True,
    )
    db_session.add(agent)
    await db_session.commit()
    await db_session.refresh(agent)
    return agent


# ═══════════════════════════════════════════════════════════════
# UTILITY FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def sphere_ids() -> list[str]:
    """Return all 9 valid sphere IDs (FROZEN architecture)."""
    return [
        "personal",
        "business",
        "government",
        "creative",  # was "studio"
        "community",
        "social",
        "entertainment",
        "team",
        "scholar",  # 9th sphere
    ]


@pytest.fixture
def bureau_section_ids() -> list[str]:
    """Return all 6 bureau section IDs (HARD LIMIT)."""
    return [
        "quick_capture",
        "resume_workspace",
        "threads",
        "data_files",
        "active_agents",
        "meetings",
    ]


@pytest.fixture
def governance_laws() -> dict:
    """Return governance laws for testing."""
    return {
        "L1": "CONSENT_PRIMACY",
        "L2": "TEMPORAL_SOVEREIGNTY",
        "L3": "CONTEXTUAL_FIDELITY",
        "L4": "HIERARCHICAL_RESPECT",
        "L5": "AUDIT_COMPLETENESS",
        "L6": "ENCODING_TRANSPARENCY",
        "L7": "AGENT_NON_AUTONOMY",
        "L8": "BUDGET_ACCOUNTABILITY",
        "L9": "CROSS_SPHERE_ISOLATION",
        "L10": "DELETION_COMPLETENESS",
    }


# ═══════════════════════════════════════════════════════════════
# MOCK FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def mock_ai_response():
    """Mock AI response for Nova."""
    return {
        "response": "This is a mock AI response for testing purposes.",
        "tokens_used": 50,
        "suggestions": [
            {"type": "task", "content": "Review the document"},
            {"type": "meeting", "content": "Schedule follow-up"},
        ],
    }


@pytest.fixture
def mock_encoding_result():
    """Mock encoding result."""
    return {
        "encoded_text": "TST:ENC",
        "original_tokens": 10,
        "encoded_tokens": 3,
        "compression_ratio": 3.33,
        "quality_score": 95,
    }


# ═══════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
async def cleanup(db_session: AsyncSession):
    """Clean up after each test."""
    yield
    # Rollback any uncommitted changes
    await db_session.rollback()
