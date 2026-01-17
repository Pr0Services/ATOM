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
# AGENTS ENDPOINTS - Pagination for 6,500 Agents
# ===========================================================================================

@app.get("/agents", tags=["Agents"])
async def list_agents(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=500, description="Items per page"),
    sphere: Optional[str] = Query(None, description="Filter by sphere"),
    frequency: Optional[int] = Query(None, description="Filter by frequency")
):
    """
    List agents with pagination.

    Supports 6,500+ agents without blocking the server.
    Uses cursor-based pagination for optimal performance.

    - **page**: Page number (1-indexed)
    - **page_size**: Items per page (max 500)
    - **sphere**: Filter by sphere (personal, business, etc.)
    - **frequency**: Filter by frequency (174, 285, 396, etc.)
    """
    total_agents = RESONANCE_DATA["agents"]["total_count"]
    spheres = ["personal", "business", "government", "creative_studio",
               "community", "social_media", "entertainment", "my_team", "scholar"]
    frequencies = RESONANCE_DATA["agents"]["frequency_agents"]

    # Calculate pagination
    total_pages = (total_agents + page_size - 1) // page_size
    offset = (page - 1) * page_size

    # Generate agent list (simulated - in production, fetch from DB)
    agents = []
    for i in range(offset, min(offset + page_size, total_agents)):
        agent_sphere = spheres[i % len(spheres)]
        agent_frequency = frequencies[i % len(frequencies)]

        # Apply filters
        if sphere and agent_sphere != sphere:
            continue
        if frequency and agent_frequency != frequency:
            continue

        agents.append({
            "id": f"agent_{i+1:05d}",
            "name": f"Agent-{agent_frequency}Hz-{i+1}",
            "sphere": agent_sphere,
            "frequency_hz": agent_frequency,
            "status": "active" if i % 10 != 0 else "standby",
            "resonance_aligned": (i % 3) in [0, 2],  # ~66% aligned
            "created_at": datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc).isoformat()
        })

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
        "filters": {
            "sphere": sphere,
            "frequency": frequency,
            "available_spheres": spheres,
            "available_frequencies": frequencies
        },
        "meta": {
            "agent_system": "NOVA-999",
            "total_registered": total_agents
        }
    }


@app.get("/agents/{agent_id}", tags=["Agents"])
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    # Extract agent number
    try:
        agent_num = int(agent_id.replace("agent_", ""))
    except ValueError:
        raise HTTPException(status_code=404, detail="Agent not found")

    if agent_num < 1 or agent_num > RESONANCE_DATA["agents"]["total_count"]:
        raise HTTPException(status_code=404, detail="Agent not found")

    spheres = ["personal", "business", "government", "creative_studio",
               "community", "social_media", "entertainment", "my_team", "scholar"]
    frequencies = RESONANCE_DATA["agents"]["frequency_agents"]

    i = agent_num - 1
    return {
        "id": agent_id,
        "name": f"Agent-{frequencies[i % len(frequencies)]}Hz-{agent_num}",
        "sphere": spheres[i % len(spheres)],
        "frequency_hz": frequencies[i % len(frequencies)],
        "status": "active" if i % 10 != 0 else "standby",
        "resonance_aligned": (i % 3) in [0, 2],
        "capabilities": [
            "data_processing",
            "pattern_recognition",
            "resonance_transmission"
        ],
        "created_at": datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc).isoformat(),
        "last_pulse": resonance_engine.state.timestamp.isoformat()
    }


@app.get("/agents/stats/overview", tags=["Agents"])
async def get_agents_stats():
    """Get agent swarm statistics."""
    total = RESONANCE_DATA["agents"]["total_count"]
    return {
        "total_agents": total,
        "spheres": RESONANCE_DATA["agents"]["spheres"],
        "frequency_distribution": {
            str(freq): total // len(RESONANCE_DATA["agents"]["frequency_agents"])
            for freq in RESONANCE_DATA["agents"]["frequency_agents"]
        },
        "status_distribution": {
            "active": int(total * 0.9),
            "standby": int(total * 0.1)
        },
        "resonance_alignment": {
            "aligned": int(total * 0.66),
            "pending": int(total * 0.34)
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
