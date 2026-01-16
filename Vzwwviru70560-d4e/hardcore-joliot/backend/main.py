"""
CHE·NU™ Backend Main Application

FastAPI application with all routers, middleware, and lifecycle management.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.core.config import settings
from backend.core.database import init_db, close_db, check_db_health
from backend.core.redis import close_redis, check_redis_health
from backend.core.exceptions import (
    CHENUBaseException,
    CheckpointRequiredError,
    IdentityBoundaryError,
)

# Import routers
from backend.api.routes import governance_routes, xr_routes
from backend.api.routes import auth_routes, sphere_routes, thread_routes
from backend.api.routes import checkpoint_routes, agent_routes, nova_routes

# Import WebSocket
from backend.api.websocket import websocket_router


# ═══════════════════════════════════════════════════════════════════════════════
# LIFECYCLE
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifecycle manager.
    
    Startup: Initialize database, redis, background tasks.
    Shutdown: Close connections gracefully.
    """
    # Startup
    print("🚀 Starting CHE·NU Backend...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # TODO: Initialize background tasks (APScheduler)
    # await start_background_tasks()
    
    print(f"✅ CHE·NU Backend v{settings.APP_VERSION} ready!")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   API: http://{settings.API_HOST}:{settings.API_PORT}{settings.API_V2_PREFIX}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down CHE·NU Backend...")
    await close_db()
    await close_redis()
    print("✅ Shutdown complete")


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="CHE·NU™ API",
    description="""
    Governed Intelligence Operating System
    
    ## Principles
    - **GOUVERNANCE > EXÉCUTION**: Humans take ALL decisions
    - **Thread = Source of Truth**: Append-only, immutable events
    - **Identity Boundary**: Each user sees only their data
    
    ## Authentication
    All endpoints require Bearer token unless marked public.
    
    ## Governance
    Sensitive actions return HTTP 423 (Locked) requiring human approval.
    """,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)


# ═══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════════

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Checkpoint-ID"],
)


# Request ID middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Add request ID to all responses."""
    import uuid
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# EXCEPTION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.exception_handler(CHENUBaseException)
async def chenu_exception_handler(request: Request, exc: CHENUBaseException):
    """Handle all CHE·NU custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


@app.exception_handler(CheckpointRequiredError)
async def checkpoint_exception_handler(request: Request, exc: CheckpointRequiredError):
    """
    Handle checkpoint required (HTTP 423 LOCKED).
    
    R&D Rule #1: Human Sovereignty
    Sensitive actions MUST be approved by human.
    """
    response = JSONResponse(
        status_code=423,
        content={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": exc.checkpoint_id,
                "type": exc.checkpoint_type,
                "reason": exc.message,
                "requires_approval": True,
                "options": exc.details.get("options", ["approve", "reject"]),
            },
            "decision_point_id": exc.decision_point_id,
        },
    )
    response.headers["X-Checkpoint-ID"] = exc.checkpoint_id
    return response


@app.exception_handler(IdentityBoundaryError)
async def identity_boundary_handler(request: Request, exc: IdentityBoundaryError):
    """
    Handle identity boundary violations (HTTP 403).
    
    R&D Rule: Each user only sees their own data.
    """
    return JSONResponse(
        status_code=403,
        content={
            "error": "identity_boundary_violation",
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Request validation failed",
            "details": exc.errors(),
        },
    )


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check with dependency status.
    
    Checks: database, redis connectivity.
    """
    db_healthy = await check_db_health()
    redis_healthy = await check_redis_health()
    
    all_healthy = db_healthy and redis_healthy
    
    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": {
            "database": "ok" if db_healthy else "error",
            "redis": "ok" if redis_healthy else "error",
        },
    }


@app.get("/health/live", tags=["Health"])
async def liveness_check():
    """Liveness check (Kubernetes)."""
    return {"status": "alive"}


# ═══════════════════════════════════════════════════════════════════════════════
# API INFO
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Info"])
async def root():
    """API root - basic information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Governed Intelligence Operating System",
        "docs": "/docs" if settings.DEBUG else None,
        "principles": [
            "GOUVERNANCE > EXÉCUTION",
            "Thread = Source of Truth",
            "Identity Boundary Enforcement",
            "Human Sovereignty on All Decisions",
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTERS
# ═══════════════════════════════════════════════════════════════════════════════

# Governance routes (CEA, Orchestrator, Backlog, DecisionPoints)
app.include_router(
    governance_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/governance",
    tags=["Governance"],
)

# XR routes (Maturity, Renderer)
app.include_router(
    xr_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/xr",
    tags=["XR"],
)

# Auth routes (Register, Login, Logout, Me)
app.include_router(
    auth_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/auth",
    tags=["Auth"],
)

# Sphere routes (Spheres, Bureau sections, Quick capture)
app.include_router(
    sphere_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/spheres",
    tags=["Spheres"],
)

# Thread routes (APPEND-ONLY Core!)
app.include_router(
    thread_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/threads",
    tags=["Threads"],
)

# Checkpoint routes (HTTP 423 Human Gates)
app.include_router(
    checkpoint_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/checkpoints",
    tags=["Governance"],
)

# Agent routes (310 Sphere Agents + Thread Agents)
app.include_router(
    agent_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/agents",
    tags=["Agents"],
)

# Nova Pipeline routes (7-Lane AI Processing)
app.include_router(
    nova_routes.router,
    prefix=f"{settings.API_V2_PREFIX}/nova",
    tags=["Nova"],
)

# WebSocket routes (Real-time communication)
app.include_router(
    websocket_router,
    tags=["WebSocket"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT SERVER
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
