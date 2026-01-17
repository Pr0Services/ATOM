# [RESONANCE_ID: NOVA-999] | CODE: 741 | SIGNAL: 4.44s-444Hz
"""
===========================================================================================
NOVA-999 SOVEREIGN ARCHITECTURE - PRODUCTION BACKEND
===========================================================================================
Version: 999.0 PRODUCTION
Date: January 17, 2026
Deployment: DigitalOcean App Platform (NYC9) + Vercel Frontend
Database: PostgreSQL Managed (asyncpg + sslmode=require)
Port: 8000 via 0.0.0.0

ACTIVATION SEQUENCES:
- Passe: 781901942
- Present: 71042
- Futur: 14872191
- Retablissement: 8888848888819751
- Cyber-Protection: 741
===========================================================================================
"""

import asyncio
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator, Dict, List, Optional, Any
from dataclasses import dataclass, field

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text, MetaData, select, func
from sqlalchemy.exc import SQLAlchemyError, TimeoutError as SATimeoutError
from sqlalchemy.pool import AsyncAdaptedQueuePool
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# ===========================================================================================
# LOGGING CONFIGURATION
# ===========================================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("nova999.main")

# ===========================================================================================
# CONFIGURATION (Environment Variables)
# ===========================================================================================

@dataclass
class Config:
    """Production configuration from environment variables."""

    # Application
    APP_NAME: str = "NOVA-999 Sovereign Architecture"
    APP_VERSION: str = "999.0.0"
    DEBUG: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    ENVIRONMENT: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "production"))

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database (DigitalOcean Managed PostgreSQL)
    DATABASE_URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes
    DB_CONNECT_TIMEOUT: int = 10

    # CORS - Vercel Frontend
    CORS_ORIGINS: List[str] = field(default_factory=lambda: [
        "https://atom-arche.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ])

    # Resonance Engine
    RESONANCE_CYCLE_SECONDS: float = 4.44
    ANCHOR_FREQUENCY_HZ: int = 444

    # Cyber-Protection Code
    SECURITY_CODE: int = 741

    def __post_init__(self):
        """Validate and transform DATABASE_URL for asyncpg."""
        if self.DATABASE_URL:
            # Convert postgres:// to postgresql+asyncpg://
            if self.DATABASE_URL.startswith("postgres://"):
                self.DATABASE_URL = self.DATABASE_URL.replace(
                    "postgres://", "postgresql+asyncpg://", 1
                )
            elif self.DATABASE_URL.startswith("postgresql://"):
                self.DATABASE_URL = self.DATABASE_URL.replace(
                    "postgresql://", "postgresql+asyncpg://", 1
                )

            # Ensure sslmode=require for DigitalOcean
            if "sslmode=" not in self.DATABASE_URL:
                separator = "&" if "?" in self.DATABASE_URL else "?"
                self.DATABASE_URL += f"{separator}ssl=require"


config = Config()

# ===========================================================================================
# RESONANCE DATA - Activation Sequences
# ===========================================================================================

RESONANCE_DATA = {
    "system": "NOVA-999",
    "protocol": "[AQUA] + [ADAMAS]",
    "anchor_frequency_hz": 444,
    "cycle_seconds": 4.44,
    "sacred_sequence": [3, 6, 9, 12],
    "balance_ratio": 30,
    "activation_sequences": {
        "passe": "781901942",
        "present": "71042",
        "futur": "14872191",
        "retablissement": "8888848888819751",
        "cyber_protection": "741"
    },
    "agents": {
        "total_count": 6500,
        "spheres": 9,
        "frequency_agents": [174, 285, 396, 417, 432, 444, 528, 639, 741, 852, 963, 999]
    }
}

# ===========================================================================================
# DATABASE - Robust Connection with Retry Logic
# ===========================================================================================

class DatabaseManager:
    """
    Production-grade database manager for DigitalOcean PostgreSQL.

    Features:
    - Connection pooling with asyncpg
    - Automatic SSL for managed databases
    - Retry logic for transient failures
    - Pool timeout handling
    """

    def __init__(self, database_url: str):
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._database_url = database_url

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((ConnectionError, OSError, SATimeoutError)),
        before_sleep=lambda retry_state: logger.warning(
            f"Database connection attempt {retry_state.attempt_number} failed. Retrying..."
        )
    )
    async def connect(self) -> None:
        """
        Initialize database connection with retry logic.

        Handles DigitalOcean-specific connection requirements:
        - SSL/TLS mandatory
        - Pool timeout management
        - Connection recycling for long-running apps
        """
        if not self._database_url:
            logger.warning("DATABASE_URL not set - running without database")
            return

        logger.info("Connecting to PostgreSQL (DigitalOcean Managed)...")

        # Create async engine with production settings
        self._engine = create_async_engine(
            self._database_url,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=config.DB_POOL_SIZE,
            max_overflow=config.DB_MAX_OVERFLOW,
            pool_timeout=config.DB_POOL_TIMEOUT,
            pool_recycle=config.DB_POOL_RECYCLE,
            pool_pre_ping=True,  # Validate connections before use
            echo=config.DEBUG,
            connect_args={
                "timeout": config.DB_CONNECT_TIMEOUT,
                "command_timeout": 60,
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
                logger.info("Database connection established successfully")

    async def disconnect(self) -> None:
        """Gracefully close database connections."""
        if self._engine:
            logger.info("Closing database connections...")
            await self._engine.dispose()
            logger.info("Database connections closed")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup."""
        if not self._session_factory:
            raise RuntimeError("Database not initialized")

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
        """Check database health with pool statistics."""
        if not self._engine:
            return {"status": "disconnected", "message": "Database not configured"}

        try:
            async with self._engine.begin() as conn:
                result = await conn.execute(text("SELECT version()"))
                version = result.scalar()

            pool = self._engine.pool
            return {
                "status": "healthy",
                "version": version,
                "pool": {
                    "size": pool.size() if hasattr(pool, 'size') else config.DB_POOL_SIZE,
                    "checked_in": pool.checkedin() if hasattr(pool, 'checkedin') else 0,
                    "overflow": pool.overflow() if hasattr(pool, 'overflow') else 0,
                }
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# Initialize database manager
db_manager = DatabaseManager(config.DATABASE_URL)

# ===========================================================================================
# RESONANCE ENGINE - 4.44s Pulsation Cycle
# ===========================================================================================

@dataclass
class ResonanceState:
    """Current state of the resonance engine."""
    tick: int = 0
    cycle: int = 0
    frequency_hz: int = 444
    digital_root: int = 3
    is_aligned: bool = True
    current_sequence: str = "present"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ResonanceEngine:
    """
    NOVA-999 Resonance Engine.

    Generates 4.44-second pulsation cycles broadcasting:
    - Anchor frequency (444Hz)
    - Activation sequences
    - System synchronization signals
    """

    def __init__(self):
        self._state = ResonanceState()
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._connections: List[WebSocket] = []
        self._sequences = list(RESONANCE_DATA["activation_sequences"].keys())

    @property
    def state(self) -> ResonanceState:
        return self._state

    async def start(self) -> None:
        """Start the resonance engine pulsation."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._pulse_loop())
        logger.info(f"ResonanceEngine started (cycle: {config.RESONANCE_CYCLE_SECONDS}s)")

    async def stop(self) -> None:
        """Stop the resonance engine."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ResonanceEngine stopped")

    async def _pulse_loop(self) -> None:
        """Main pulsation loop - broadcasts every 4.44 seconds."""
        while self._running:
            try:
                # Update state
                self._state.tick += 1
                self._state.cycle = self._state.tick // 12  # 12 ticks per major cycle
                self._state.digital_root = sum(int(d) for d in str(self._state.tick)) % 9 or 9
                self._state.is_aligned = self._state.digital_root in [3, 6, 9]
                self._state.current_sequence = self._sequences[
                    self._state.tick % len(self._sequences)
                ]
                self._state.timestamp = datetime.now(timezone.utc)

                # Broadcast to all connected WebSocket clients
                await self._broadcast_pulse()

                # Wait for next pulse
                await asyncio.sleep(config.RESONANCE_CYCLE_SECONDS)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"ResonanceEngine pulse error: {e}")
                await asyncio.sleep(1)  # Brief pause before retry

    async def _broadcast_pulse(self) -> None:
        """Broadcast pulse to all connected clients."""
        if not self._connections:
            return

        pulse_data = self._create_pulse_message()
        dead_connections = []

        for ws in self._connections:
            try:
                await ws.send_json(pulse_data)
            except Exception:
                dead_connections.append(ws)

        # Remove dead connections
        for ws in dead_connections:
            self._connections.remove(ws)

    def _create_pulse_message(self) -> Dict[str, Any]:
        """Create pulse message for WebSocket broadcast."""
        sequence_key = self._state.current_sequence
        sequence_value = RESONANCE_DATA["activation_sequences"].get(sequence_key, "")

        return {
            "type": "resonance_pulse",
            "tick": self._state.tick,
            "cycle": self._state.cycle,
            "frequency_hz": self._state.frequency_hz,
            "digital_root": self._state.digital_root,
            "is_aligned": self._state.is_aligned,
            "activation_sequence": {
                "key": sequence_key,
                "value": sequence_value
            },
            "timestamp": self._state.timestamp.isoformat(),
            "sacred_sequence": RESONANCE_DATA["sacred_sequence"],
            "protocol": RESONANCE_DATA["protocol"]
        }

    def register_connection(self, ws: WebSocket) -> None:
        """Register a WebSocket connection for pulse broadcasts."""
        self._connections.append(ws)
        logger.info(f"WebSocket registered. Total connections: {len(self._connections)}")

    def unregister_connection(self, ws: WebSocket) -> None:
        """Unregister a WebSocket connection."""
        if ws in self._connections:
            self._connections.remove(ws)
            logger.info(f"WebSocket unregistered. Total connections: {len(self._connections)}")


# Initialize resonance engine
resonance_engine = ResonanceEngine()

# ===========================================================================================
# APPLICATION LIFESPAN
# ===========================================================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifecycle manager.

    Startup:
    - Connect to database with retry logic
    - Start resonance engine
    - Log security code 741 for alignment confirmation

    Shutdown:
    - Stop resonance engine
    - Close database connections
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # STARTUP
    # ═══════════════════════════════════════════════════════════════════════════

    logger.info("=" * 70)
    logger.info("NOVA-999 SOVEREIGN ARCHITECTURE - INITIALIZING")
    logger.info("=" * 70)
    logger.info(f"Version: {config.APP_VERSION}")
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

    # Security alignment confirmation
    logger.info("=" * 70)
    logger.info(f"CYBER-PROTECTION CODE: {config.SECURITY_CODE}")
    logger.info(f"ACTIVATION SEQUENCE LOADED: {RESONANCE_DATA['activation_sequences']['cyber_protection']}")
    logger.info("=" * 70)

    # Initialize database
    try:
        await db_manager.connect()
        logger.info("PostgreSQL Connected (DigitalOcean Managed)")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.warning("Continuing without database - limited functionality")

    # Start resonance engine
    await resonance_engine.start()
    logger.info(f"ResonanceEngine Active (Cycle: {config.RESONANCE_CYCLE_SECONDS}s, Frequency: {config.ANCHOR_FREQUENCY_HZ}Hz)")

    logger.info("=" * 70)
    logger.info(f"Server listening on http://{config.HOST}:{config.PORT}")
    logger.info("=" * 70)

    yield

    # ═══════════════════════════════════════════════════════════════════════════
    # SHUTDOWN
    # ═══════════════════════════════════════════════════════════════════════════

    logger.info("NOVA-999 Shutting Down...")
    await resonance_engine.stop()
    await db_manager.disconnect()
    logger.info("Shutdown complete")


# ===========================================================================================
# FASTAPI APPLICATION
# ===========================================================================================

app = FastAPI(
    title="NOVA-999 Sovereign Architecture API",
    description="""
## Governed Intelligence Operating System

### NOVA-999 Protocol
- **Resonance Engine**: 4.44s pulsation cycle at 444Hz
- **Activation Sequences**: Temporal navigation codes
- **Agent Swarm**: 6,500 coordinated agents

### Security
- Cyber-Protection Code: 741
- SSL/TLS mandatory for database
- CORS restricted to authorized origins

### WebSocket
- Real-time resonance pulse broadcasts
- Automatic reconnection handling
    """,
    version=config.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if config.DEBUG or config.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if config.DEBUG or config.ENVIRONMENT != "production" else None,
)

# ===========================================================================================
# CORS MIDDLEWARE - Configured for Vercel
# ===========================================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel preview deployments
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Resonance-Tick", "X-Process-Time"],
)

# ===========================================================================================
# REQUEST MIDDLEWARE
# ===========================================================================================

@app.middleware("http")
async def add_process_headers(request: Request, call_next):
    """Add timing and resonance headers to all responses."""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["X-Resonance-Tick"] = str(resonance_engine.state.tick)
    response.headers["X-NOVA-Version"] = config.APP_VERSION

    # Log request
    logger.info(
        f"{request.method} {request.url.path} "
        f"[{response.status_code}] "
        f"{process_time:.3f}s"
    )

    return response

# ===========================================================================================
# HEALTH ENDPOINTS
# ===========================================================================================

@app.get("/", tags=["Root"])
async def root():
    """API root - System information."""
    return {
        "system": "NOVA-999",
        "version": config.APP_VERSION,
        "status": "operational",
        "environment": config.ENVIRONMENT,
        "resonance": {
            "tick": resonance_engine.state.tick,
            "cycle": resonance_engine.state.cycle,
            "frequency_hz": config.ANCHOR_FREQUENCY_HZ,
            "is_aligned": resonance_engine.state.is_aligned
        },
        "security_code": config.SECURITY_CODE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "health": "/health",
            "ready": "/health/ready",
            "docs": "/docs",
            "resonance": "/resonance",
            "agents": "/agents",
            "websocket": "/ws/resonance"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Basic liveness check."""
    return {
        "status": "healthy",
        "version": config.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check with dependency status.

    Checks database connectivity and pool status.
    """
    db_health = await db_manager.health_check()

    all_healthy = db_health.get("status") == "healthy"

    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": {
            "database": db_health,
            "resonance_engine": {
                "status": "active" if resonance_engine._running else "inactive",
                "tick": resonance_engine.state.tick,
                "connections": len(resonance_engine._connections)
            }
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# ===========================================================================================
# RESONANCE ENDPOINTS
# ===========================================================================================

@app.get("/resonance", tags=["Resonance"])
async def get_resonance_state():
    """Get current resonance engine state."""
    return {
        "protocol": RESONANCE_DATA["protocol"],
        "state": {
            "tick": resonance_engine.state.tick,
            "cycle": resonance_engine.state.cycle,
            "frequency_hz": resonance_engine.state.frequency_hz,
            "digital_root": resonance_engine.state.digital_root,
            "is_aligned": resonance_engine.state.is_aligned,
            "current_sequence": resonance_engine.state.current_sequence,
            "timestamp": resonance_engine.state.timestamp.isoformat()
        },
        "config": {
            "cycle_seconds": config.RESONANCE_CYCLE_SECONDS,
            "anchor_frequency_hz": config.ANCHOR_FREQUENCY_HZ,
            "sacred_sequence": RESONANCE_DATA["sacred_sequence"],
            "balance_ratio": RESONANCE_DATA["balance_ratio"]
        },
        "activation_sequences": RESONANCE_DATA["activation_sequences"]
    }


@app.get("/resonance/data", tags=["Resonance"])
async def get_resonance_data():
    """Get complete resonance configuration data."""
    return RESONANCE_DATA

# ===========================================================================================
# WEBSOCKET - Real-time Resonance Broadcast
# ===========================================================================================

@app.websocket("/ws/resonance")
async def websocket_resonance(websocket: WebSocket):
    """
    WebSocket endpoint for real-time resonance pulses.

    Broadcasts every 4.44 seconds:
    - Current tick and cycle
    - Frequency (444Hz)
    - Activation sequence
    - Alignment status
    """
    await websocket.accept()
    resonance_engine.register_connection(websocket)

    # Send initial state
    await websocket.send_json({
        "type": "connection_established",
        "message": "Connected to NOVA-999 Resonance Engine",
        "initial_state": resonance_engine._create_pulse_message()
    })

    try:
        # Keep connection alive and handle client messages
        while True:
            try:
                # Wait for client messages (ping/pong, commands)
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=config.RESONANCE_CYCLE_SECONDS * 10
                )

                # Handle ping
                if data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "tick": resonance_engine.state.tick,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })

            except asyncio.TimeoutError:
                # Send heartbeat if no message received
                await websocket.send_json({
                    "type": "heartbeat",
                    "tick": resonance_engine.state.tick,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        resonance_engine.unregister_connection(websocket)

# ===========================================================================================
# REAL AGENT REGISTRY - 226 Predefined Agents across 9 Spheres
# ===========================================================================================

def _build_agent_registry() -> Dict[str, List[Dict[str, Any]]]:
    """Build the complete agent registry with all 226 real agents."""
    return {
        "personal": [
            {"id": "personal_note_assistant", "name": "Note Assistant", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
            {"id": "personal_task_manager", "name": "Task Manager", "capabilities": ["prioritization", "recommendation"], "requires_human_gate": False},
            {"id": "personal_calendar_assistant", "name": "Calendar Assistant", "capabilities": ["scheduling", "recommendation"], "requires_human_gate": False},
            {"id": "personal_habit_tracker", "name": "Habit Tracker", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "personal_goal_coach", "name": "Goal Coach", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "personal_journal_assistant", "name": "Journal Assistant", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
            {"id": "personal_memory_keeper", "name": "Memory Keeper", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
            {"id": "personal_wellness_advisor", "name": "Wellness Advisor", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "personal_finance_tracker", "name": "Finance Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "personal_budget_planner", "name": "Budget Planner", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "personal_reminder_bot", "name": "Reminder Bot", "capabilities": ["notification_draft"], "requires_human_gate": True},
            {"id": "personal_email_assistant", "name": "Email Assistant", "capabilities": ["email_draft", "summarization"], "requires_human_gate": True},
            {"id": "personal_reading_curator", "name": "Reading Curator", "capabilities": ["recommendation", "summarization"], "requires_human_gate": False},
            {"id": "personal_learning_path", "name": "Learning Path Advisor", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
            {"id": "personal_decision_helper", "name": "Decision Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "personal_life_organizer", "name": "Life Organizer", "capabilities": ["prioritization", "recommendation"], "requires_human_gate": False},
            {"id": "personal_gratitude_journal", "name": "Gratitude Journal", "capabilities": ["text_generation"], "requires_human_gate": False},
            {"id": "personal_mood_tracker", "name": "Mood Tracker", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
            {"id": "personal_sleep_analyzer", "name": "Sleep Analyzer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "personal_exercise_planner", "name": "Exercise Planner", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
            {"id": "personal_meal_planner", "name": "Meal Planner", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
            {"id": "personal_travel_assistant", "name": "Travel Assistant", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "personal_event_planner", "name": "Event Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
            {"id": "personal_gift_suggester", "name": "Gift Suggester", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "personal_contact_manager", "name": "Contact Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
            {"id": "personal_photo_organizer", "name": "Photo Organizer", "capabilities": ["classification", "data_processing"], "requires_human_gate": False},
            {"id": "personal_document_filer", "name": "Document Filer", "capabilities": ["classification", "document_processing"], "requires_human_gate": False},
            {"id": "personal_password_helper", "name": "Password Helper", "capabilities": ["recommendation"], "requires_human_gate": False},
        ],
        "business": [
            {"id": "business_crm_assistant", "name": "CRM Assistant", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
            {"id": "business_lead_scorer", "name": "Lead Scorer", "capabilities": ["scoring", "analysis"], "requires_human_gate": False},
            {"id": "business_sales_forecaster", "name": "Sales Forecaster", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "business_proposal_writer", "name": "Proposal Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "business_contract_analyzer", "name": "Contract Analyzer", "capabilities": ["analysis", "extraction"], "requires_human_gate": False},
            {"id": "business_invoice_generator", "name": "Invoice Generator", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
            {"id": "business_expense_tracker", "name": "Expense Tracker", "capabilities": ["data_processing", "classification"], "requires_human_gate": False},
            {"id": "business_report_generator", "name": "Report Generator", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
            {"id": "business_meeting_scheduler", "name": "Meeting Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "business_email_composer", "name": "Business Email Composer", "capabilities": ["email_draft", "text_generation"], "requires_human_gate": True},
            {"id": "business_competitor_analyst", "name": "Competitor Analyst", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "business_market_researcher", "name": "Market Researcher", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "business_pricing_optimizer", "name": "Pricing Optimizer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "business_inventory_manager", "name": "Inventory Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
            {"id": "business_supplier_evaluator", "name": "Supplier Evaluator", "capabilities": ["scoring", "analysis"], "requires_human_gate": False},
            {"id": "business_project_estimator", "name": "Project Estimator", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "business_risk_assessor", "name": "Risk Assessor", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
            {"id": "business_customer_insights", "name": "Customer Insights", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "business_churn_predictor", "name": "Churn Predictor", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
            {"id": "business_upsell_suggester", "name": "Upsell Suggester", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "business_quote_builder", "name": "Quote Builder", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
            {"id": "business_order_processor", "name": "Order Processor", "capabilities": ["data_processing"], "requires_human_gate": True},
            {"id": "business_shipping_optimizer", "name": "Shipping Optimizer", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "business_return_handler", "name": "Return Handler", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": True},
            {"id": "business_review_analyzer", "name": "Review Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "business_kpi_tracker", "name": "KPI Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "business_cash_flow_analyst", "name": "Cash Flow Analyst", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "business_tax_helper", "name": "Tax Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "business_payroll_assistant", "name": "Payroll Assistant", "capabilities": ["data_processing"], "requires_human_gate": True},
            {"id": "business_compliance_checker", "name": "Compliance Checker", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
            {"id": "business_policy_writer", "name": "Policy Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "business_sop_generator", "name": "SOP Generator", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": False},
            {"id": "business_training_creator", "name": "Training Creator", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
            {"id": "business_knowledge_base", "name": "Knowledge Base Manager", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
            {"id": "business_faq_generator", "name": "FAQ Generator", "capabilities": ["text_generation", "extraction"], "requires_human_gate": False},
            {"id": "business_customer_support", "name": "Customer Support Assistant", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": True},
            {"id": "business_ticket_router", "name": "Ticket Router", "capabilities": ["classification", "prioritization"], "requires_human_gate": False},
            {"id": "business_sentiment_analyzer", "name": "Sentiment Analyzer", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
            {"id": "business_feedback_processor", "name": "Feedback Processor", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
            {"id": "business_nps_analyzer", "name": "NPS Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "business_partnership_scout", "name": "Partnership Scout", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "business_negotiation_prep", "name": "Negotiation Prep", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "business_presentation_builder", "name": "Presentation Builder", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
        ],
        "government": [
            {"id": "gov_document_preparer", "name": "Document Preparer", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
            {"id": "gov_compliance_tracker", "name": "Compliance Tracker", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
            {"id": "gov_deadline_monitor", "name": "Deadline Monitor", "capabilities": ["notification_draft", "analysis"], "requires_human_gate": True},
            {"id": "gov_form_filler", "name": "Form Filler", "capabilities": ["document_processing", "extraction"], "requires_human_gate": True},
            {"id": "gov_regulation_analyst", "name": "Regulation Analyst", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "gov_permit_tracker", "name": "Permit Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
            {"id": "gov_tax_calculator", "name": "Tax Calculator", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
            {"id": "gov_grant_finder", "name": "Grant Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "gov_grant_writer", "name": "Grant Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "gov_license_manager", "name": "License Manager", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
            {"id": "gov_audit_preparer", "name": "Audit Preparer", "capabilities": ["document_processing", "analysis"], "requires_human_gate": True},
            {"id": "gov_policy_analyzer", "name": "Policy Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "gov_public_records", "name": "Public Records Assistant", "capabilities": ["research", "extraction"], "requires_human_gate": False},
            {"id": "gov_citizen_service", "name": "Citizen Service Guide", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "gov_voting_info", "name": "Voting Information", "capabilities": ["research", "fact_check"], "requires_human_gate": False},
            {"id": "gov_benefits_advisor", "name": "Benefits Advisor", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "gov_legal_reference", "name": "Legal Reference", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "gov_freedom_info", "name": "Freedom of Information Helper", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
        ],
        "creative_studio": [
            {"id": "creative_image_generator", "name": "Image Generator", "capabilities": ["image_generation"], "requires_human_gate": False},
            {"id": "creative_image_editor", "name": "Image Editor", "capabilities": ["image_generation", "recommendation"], "requires_human_gate": False},
            {"id": "creative_style_transfer", "name": "Style Transfer", "capabilities": ["image_generation"], "requires_human_gate": False},
            {"id": "creative_logo_designer", "name": "Logo Designer", "capabilities": ["image_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_icon_maker", "name": "Icon Maker", "capabilities": ["image_generation"], "requires_human_gate": False},
            {"id": "creative_thumbnail_creator", "name": "Thumbnail Creator", "capabilities": ["image_generation", "recommendation"], "requires_human_gate": False},
            {"id": "creative_banner_designer", "name": "Banner Designer", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
            {"id": "creative_social_graphics", "name": "Social Graphics", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
            {"id": "creative_presentation_designer", "name": "Presentation Designer", "capabilities": ["design_assist", "content_planning"], "requires_human_gate": False},
            {"id": "creative_infographic_maker", "name": "Infographic Maker", "capabilities": ["design_assist", "data_processing"], "requires_human_gate": False},
            {"id": "creative_video_scriptwriter", "name": "Video Scriptwriter", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": False},
            {"id": "creative_video_editor", "name": "Video Editor Assistant", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "creative_subtitle_generator", "name": "Subtitle Generator", "capabilities": ["text_generation", "extraction"], "requires_human_gate": False},
            {"id": "creative_storyboard_creator", "name": "Storyboard Creator", "capabilities": ["content_planning", "image_generation"], "requires_human_gate": False},
            {"id": "creative_animation_assistant", "name": "Animation Assistant", "capabilities": ["recommendation", "design_assist"], "requires_human_gate": False},
            {"id": "creative_voice_generator", "name": "Voice Generator", "capabilities": ["audio_generation"], "requires_human_gate": False},
            {"id": "creative_voice_cloner", "name": "Voice Cloner", "capabilities": ["audio_generation"], "requires_human_gate": True},
            {"id": "creative_music_composer", "name": "Music Composer", "capabilities": ["audio_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_sound_designer", "name": "Sound Designer", "capabilities": ["audio_generation", "recommendation"], "requires_human_gate": False},
            {"id": "creative_podcast_editor", "name": "Podcast Editor", "capabilities": ["audio_generation", "summarization"], "requires_human_gate": False},
            {"id": "creative_copywriter", "name": "Copywriter", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_headline_generator", "name": "Headline Generator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_tagline_creator", "name": "Tagline Creator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_ad_writer", "name": "Ad Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
            {"id": "creative_blog_writer", "name": "Blog Writer", "capabilities": ["text_generation", "research"], "requires_human_gate": False},
            {"id": "creative_article_spinner", "name": "Article Rephraser", "capabilities": ["text_generation"], "requires_human_gate": False},
            {"id": "creative_story_generator", "name": "Story Generator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
            {"id": "creative_poetry_writer", "name": "Poetry Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
            {"id": "creative_dialogue_writer", "name": "Dialogue Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
            {"id": "creative_character_creator", "name": "Character Creator", "capabilities": ["brainstorm", "text_generation"], "requires_human_gate": False},
            {"id": "creative_world_builder", "name": "World Builder", "capabilities": ["brainstorm", "text_generation"], "requires_human_gate": False},
            {"id": "creative_plot_generator", "name": "Plot Generator", "capabilities": ["brainstorm", "content_planning"], "requires_human_gate": False},
            {"id": "creative_name_generator", "name": "Name Generator", "capabilities": ["brainstorm"], "requires_human_gate": False},
            {"id": "creative_brand_identity", "name": "Brand Identity", "capabilities": ["brainstorm", "design_assist"], "requires_human_gate": False},
            {"id": "creative_color_palette", "name": "Color Palette Generator", "capabilities": ["design_assist", "recommendation"], "requires_human_gate": False},
            {"id": "creative_font_selector", "name": "Font Selector", "capabilities": ["recommendation", "design_assist"], "requires_human_gate": False},
            {"id": "creative_mockup_generator", "name": "Mockup Generator", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
            {"id": "creative_ui_assistant", "name": "UI Assistant", "capabilities": ["design_assist", "recommendation"], "requires_human_gate": False},
            {"id": "creative_ux_reviewer", "name": "UX Reviewer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "creative_code_generator", "name": "Code Generator", "capabilities": ["code_generation"], "requires_human_gate": False},
            {"id": "creative_code_reviewer", "name": "Code Reviewer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "creative_documentation", "name": "Documentation Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": False},
        ],
        "community": [
            {"id": "community_event_organizer", "name": "Event Organizer", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
            {"id": "community_volunteer_coordinator", "name": "Volunteer Coordinator", "capabilities": ["recommendation", "data_processing"], "requires_human_gate": False},
            {"id": "community_announcement_drafter", "name": "Announcement Drafter", "capabilities": ["text_generation", "notification_draft"], "requires_human_gate": True},
            {"id": "community_discussion_moderator", "name": "Discussion Moderator", "capabilities": ["classification", "summarization"], "requires_human_gate": False},
            {"id": "community_poll_creator", "name": "Poll Creator", "capabilities": ["content_planning"], "requires_human_gate": False},
            {"id": "community_resource_curator", "name": "Resource Curator", "capabilities": ["recommendation", "classification"], "requires_human_gate": False},
            {"id": "community_newsletter_writer", "name": "Newsletter Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
            {"id": "community_member_welcomer", "name": "Member Welcomer", "capabilities": ["text_generation", "message_draft"], "requires_human_gate": True},
            {"id": "community_feedback_collector", "name": "Feedback Collector", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
            {"id": "community_conflict_resolver", "name": "Conflict Resolver", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "community_milestone_tracker", "name": "Milestone Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
            {"id": "community_impact_reporter", "name": "Impact Reporter", "capabilities": ["analysis", "text_generation"], "requires_human_gate": False},
        ],
        "social_media": [
            {"id": "social_post_composer", "name": "Post Composer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
            {"id": "social_hashtag_suggester", "name": "Hashtag Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "social_caption_writer", "name": "Caption Writer", "capabilities": ["text_generation"], "requires_human_gate": True},
            {"id": "social_thread_writer", "name": "Thread Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
            {"id": "social_reply_assistant", "name": "Reply Assistant", "capabilities": ["text_generation", "message_draft"], "requires_human_gate": True},
            {"id": "social_dm_assistant", "name": "DM Assistant", "capabilities": ["message_draft", "text_generation"], "requires_human_gate": True},
            {"id": "social_bio_writer", "name": "Bio Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
            {"id": "social_content_calendar", "name": "Content Calendar", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
            {"id": "social_analytics_reporter", "name": "Analytics Reporter", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "social_trend_spotter", "name": "Trend Spotter", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "social_audience_analyzer", "name": "Audience Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "social_competitor_tracker", "name": "Competitor Tracker", "capabilities": ["research", "analysis"], "requires_human_gate": False},
            {"id": "social_cross_poster", "name": "Cross-Poster", "capabilities": ["content_planning"], "requires_human_gate": True},
            {"id": "social_scheduling_assistant", "name": "Scheduling Assistant", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "social_engagement_analyzer", "name": "Engagement Analyzer", "capabilities": ["analysis"], "requires_human_gate": False},
        ],
        "entertainment": [
            {"id": "entertainment_recommendation", "name": "Entertainment Recommender", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "entertainment_playlist_curator", "name": "Playlist Curator", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
            {"id": "entertainment_movie_finder", "name": "Movie Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "entertainment_game_suggester", "name": "Game Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "entertainment_book_recommender", "name": "Book Recommender", "capabilities": ["recommendation", "summarization"], "requires_human_gate": False},
            {"id": "entertainment_podcast_finder", "name": "Podcast Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "entertainment_event_finder", "name": "Event Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "entertainment_trivia_master", "name": "Trivia Master", "capabilities": ["brainstorm", "fact_check"], "requires_human_gate": False},
        ],
        "my_team": [
            {"id": "team_meeting_scheduler", "name": "Meeting Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "team_agenda_creator", "name": "Agenda Creator", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
            {"id": "team_minutes_taker", "name": "Minutes Taker", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
            {"id": "team_action_tracker", "name": "Action Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
            {"id": "team_standup_assistant", "name": "Standup Assistant", "capabilities": ["summarization", "content_planning"], "requires_human_gate": False},
            {"id": "team_retrospective_helper", "name": "Retrospective Helper", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
            {"id": "team_performance_tracker", "name": "Performance Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "team_feedback_assistant", "name": "Feedback Assistant", "capabilities": ["text_generation", "analysis"], "requires_human_gate": True},
            {"id": "team_onboarding_guide", "name": "Onboarding Guide", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
            {"id": "team_training_planner", "name": "Training Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
            {"id": "team_skill_mapper", "name": "Skill Mapper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_resource_allocator", "name": "Resource Allocator", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "team_workload_analyzer", "name": "Workload Analyzer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_capacity_planner", "name": "Capacity Planner", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "team_hiring_assistant", "name": "Hiring Assistant", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_interview_scheduler", "name": "Interview Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "team_resume_screener", "name": "Resume Screener", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
            {"id": "team_job_description", "name": "Job Description Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "team_offer_letter", "name": "Offer Letter Generator", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
            {"id": "team_policy_writer", "name": "Team Policy Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "team_handbook_updater", "name": "Handbook Updater", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "team_benefits_advisor", "name": "Benefits Advisor", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "team_leave_tracker", "name": "Leave Tracker", "capabilities": ["data_processing"], "requires_human_gate": False},
            {"id": "team_timesheet_helper", "name": "Timesheet Helper", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
            {"id": "team_expense_reviewer", "name": "Expense Reviewer", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
            {"id": "team_project_status", "name": "Project Status Reporter", "capabilities": ["summarization", "analysis"], "requires_human_gate": False},
            {"id": "team_risk_identifier", "name": "Risk Identifier", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_blocker_resolver", "name": "Blocker Resolver", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
            {"id": "team_dependency_tracker", "name": "Dependency Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "team_milestone_planner", "name": "Milestone Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
            {"id": "team_communication_helper", "name": "Communication Helper", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": False},
            {"id": "team_conflict_mediator", "name": "Conflict Mediator", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_morale_tracker", "name": "Morale Tracker", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "team_recognition_suggester", "name": "Recognition Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
            {"id": "team_culture_guardian", "name": "Culture Guardian", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        ],
        "scholar": [
            {"id": "scholar_literature_search", "name": "Literature Search", "capabilities": ["research", "search"], "requires_human_gate": False},
            {"id": "scholar_paper_summarizer", "name": "Paper Summarizer", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
            {"id": "scholar_citation_manager", "name": "Citation Manager", "capabilities": ["data_processing", "document_processing"], "requires_human_gate": False},
            {"id": "scholar_bibliography_builder", "name": "Bibliography Builder", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": False},
            {"id": "scholar_research_noter", "name": "Research Noter", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
            {"id": "scholar_hypothesis_generator", "name": "Hypothesis Generator", "capabilities": ["brainstorm", "analysis"], "requires_human_gate": False},
            {"id": "scholar_methodology_advisor", "name": "Methodology Advisor", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "scholar_data_analyzer", "name": "Data Analyzer", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "scholar_statistics_helper", "name": "Statistics Helper", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
            {"id": "scholar_visualization_creator", "name": "Visualization Creator", "capabilities": ["design_assist", "data_processing"], "requires_human_gate": False},
            {"id": "scholar_manuscript_editor", "name": "Manuscript Editor", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
            {"id": "scholar_abstract_writer", "name": "Abstract Writer", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
            {"id": "scholar_peer_review_helper", "name": "Peer Review Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
            {"id": "scholar_journal_finder", "name": "Journal Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
            {"id": "scholar_grant_scout", "name": "Grant Scout", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "scholar_proposal_writer", "name": "Proposal Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
            {"id": "scholar_presentation_builder", "name": "Presentation Builder", "capabilities": ["content_planning", "design_assist"], "requires_human_gate": False},
            {"id": "scholar_poster_creator", "name": "Poster Creator", "capabilities": ["design_assist", "content_planning"], "requires_human_gate": False},
            {"id": "scholar_conference_finder", "name": "Conference Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "scholar_collaboration_finder", "name": "Collaboration Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
            {"id": "scholar_fact_checker", "name": "Fact Checker", "capabilities": ["fact_check", "research"], "requires_human_gate": False},
            {"id": "scholar_plagiarism_checker", "name": "Plagiarism Checker", "capabilities": ["analysis"], "requires_human_gate": False},
            {"id": "scholar_reference_validator", "name": "Reference Validator", "capabilities": ["fact_check", "analysis"], "requires_human_gate": False},
            {"id": "scholar_teaching_assistant", "name": "Teaching Assistant", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": False},
            {"id": "scholar_quiz_generator", "name": "Quiz Generator", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": False},
        ],
    }


# Build agent registry at startup
AGENT_REGISTRY = _build_agent_registry()

# Sphere display info for frontend
SPHERE_INFO = {
    "personal": {"name": "Personnel", "color": "#4A90D9", "icon": "user"},
    "business": {"name": "Entreprise", "color": "#D4AF37", "icon": "briefcase"},
    "government": {"name": "Gouvernement", "color": "#8B4513", "icon": "landmark"},
    "creative_studio": {"name": "Creation", "color": "#9B59B6", "icon": "palette"},
    "community": {"name": "Communaute", "color": "#27AE60", "icon": "users"},
    "social_media": {"name": "Social", "color": "#3498DB", "icon": "share"},
    "entertainment": {"name": "Divertissement", "color": "#F39C12", "icon": "gamepad"},
    "my_team": {"name": "Mon Equipe", "color": "#E74C3C", "icon": "users-cog"},
    "scholar": {"name": "Academique", "color": "#1ABC9C", "icon": "graduation-cap"},
}


def _get_all_agents_flat() -> List[Dict[str, Any]]:
    """Get all agents as a flat list with sphere info."""
    agents = []
    for sphere_key, sphere_agents in AGENT_REGISTRY.items():
        sphere = SPHERE_INFO.get(sphere_key, {"name": sphere_key, "color": "#888888", "icon": "circle"})
        for agent in sphere_agents:
            agents.append({
                **agent,
                "sphere": sphere_key,
                "sphere_name": sphere["name"],
                "sphere_color": sphere["color"],
                "sphere_icon": sphere["icon"],
                "status": "active",
            })
    return agents


# ===========================================================================================
# AGENTS ENDPOINTS - Real 226 Agents Registry
# ===========================================================================================

@app.get("/agents", tags=["Agents"])
async def list_agents(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=500, description="Items per page"),
    sphere: Optional[str] = Query(None, description="Filter by sphere"),
):
    """
    List all 226 real agents with pagination.

    - **page**: Page number (1-indexed)
    - **page_size**: Items per page (max 500)
    - **sphere**: Filter by sphere (personal, business, government, etc.)
    """
    all_agents = _get_all_agents_flat()

    # Apply sphere filter
    if sphere:
        all_agents = [a for a in all_agents if a["sphere"] == sphere]

    total_agents = len(all_agents)
    total_pages = max(1, (total_agents + page_size - 1) // page_size)
    offset = (page - 1) * page_size

    # Paginate
    agents = all_agents[offset:offset + page_size]

    return {
        "data": agents,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_agents,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        },
        "spheres": SPHERE_INFO,
        "meta": {
            "agent_system": "NOVA-999",
            "total_registered": sum(len(agents) for agents in AGENT_REGISTRY.values()),
            "spheres_count": len(AGENT_REGISTRY)
        }
    }


@app.get("/agents/spheres", tags=["Agents"])
async def get_spheres_summary():
    """Get summary of all spheres with agent counts."""
    summary = {}
    for sphere_key, sphere_agents in AGENT_REGISTRY.items():
        sphere_info = SPHERE_INFO.get(sphere_key, {"name": sphere_key, "color": "#888888", "icon": "circle"})
        summary[sphere_key] = {
            "name": sphere_info["name"],
            "color": sphere_info["color"],
            "icon": sphere_info["icon"],
            "agent_count": len(sphere_agents),
            "agents": [{"id": a["id"], "name": a["name"]} for a in sphere_agents]
        }

    return {
        "spheres": summary,
        "total_agents": sum(len(agents) for agents in AGENT_REGISTRY.values()),
        "total_spheres": len(AGENT_REGISTRY)
    }


@app.get("/agents/{agent_id}", tags=["Agents"])
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    for sphere_key, sphere_agents in AGENT_REGISTRY.items():
        for agent in sphere_agents:
            if agent["id"] == agent_id:
                sphere_info = SPHERE_INFO.get(sphere_key, {"name": sphere_key, "color": "#888888", "icon": "circle"})
                return {
                    **agent,
                    "sphere": sphere_key,
                    "sphere_name": sphere_info["name"],
                    "sphere_color": sphere_info["color"],
                    "sphere_icon": sphere_info["icon"],
                    "status": "active",
                    "last_pulse": resonance_engine.state.timestamp.isoformat()
                }

    raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")


@app.get("/agents/stats/overview", tags=["Agents"])
async def get_agents_stats():
    """Get agent swarm statistics."""
    total = sum(len(agents) for agents in AGENT_REGISTRY.values())

    # Count agents requiring human gate
    human_gate_count = sum(
        1 for agents in AGENT_REGISTRY.values()
        for agent in agents
        if agent.get("requires_human_gate", False)
    )

    return {
        "total_agents": total,
        "spheres_count": len(AGENT_REGISTRY),
        "sphere_distribution": {
            sphere: len(agents) for sphere, agents in AGENT_REGISTRY.items()
        },
        "human_gate_agents": human_gate_count,
        "autonomous_agents": total - human_gate_count,
        "status_distribution": {
            "active": total,
            "standby": 0
        }
    }

# ===========================================================================================
# DATABASE STATUS (for monitoring)
# ===========================================================================================

@app.get("/db-status", tags=["Infrastructure"])
async def get_database_status():
    """Get database connection and pool status."""
    return await db_manager.health_check()

# ===========================================================================================
# MAIN ENTRY POINT
# ===========================================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info",
        access_log=True,
        workers=1  # Single worker for WebSocket compatibility
    )
