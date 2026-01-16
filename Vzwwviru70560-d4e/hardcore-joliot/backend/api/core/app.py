"""
============================================================================
CHE·NU™ V69 — MAIN API APPLICATION
============================================================================
Version: 1.0.0
Purpose: FastAPI application with all routes and middleware
Principle: GOUVERNANCE > EXÉCUTION — Full integration
============================================================================
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict
import logging
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import (
    get_settings,
    APISettings,
    API_TAGS,
    APIError,
    APIResponse,
    ErrorResponse,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 CHE·NU™ API starting up...")
    logger.info(f"Environment: {get_settings().environment.value}")
    logger.info(f"Debug: {get_settings().debug}")
    
    # Initialize components
    app.state.startup_time = datetime.utcnow()
    app.state.request_count = 0
    
    yield
    
    # Shutdown
    logger.info("👋 CHE·NU™ API shutting down...")


# ============================================================================
# CREATE APP
# ============================================================================

def create_app(settings: APISettings = None) -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This is the main entry point for the CHE·NU™ API.
    """
    settings = settings or get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
# CHE·NU™ API

**Governed Intelligence Operating System**

## Principle
> GOUVERNANCE > EXÉCUTION

All AI actions are governed, auditable, and require human approval for sensitive operations.

## Features

- **Simulations**: Run deterministic simulations with multiple scenarios
- **Agents**: L0-L3 agent hierarchy with governance checkpoints
- **Causal Inference**: DAG-based causal reasoning
- **XR Packs**: Immersive visualization artifacts
- **Audit Trail**: Complete traceability with Merkle proofs
- **Post-Quantum Security**: Ed25519 + Dilithium hybrid signatures

## Authentication

Use Bearer token or API key authentication.

## Rate Limits

- Default: 100 requests per minute
- WebSocket: 1000 concurrent connections

        """,
        openapi_tags=API_TAGS,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )
    
    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Add request ID middleware
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        app.state.request_count += 1
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response
    
    # Add error handlers
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.message,
                error_code=exc.error_code,
                details=exc.details,
                trace_id=getattr(request.state, "request_id", None),
            ).model_dump(),
        )
    
    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Internal server error",
                error_code="INTERNAL_ERROR",
                trace_id=getattr(request.state, "request_id", None),
            ).model_dump(),
        )
    
    # Register routers
    from ..endpoints import (
        health_router,
        auth_router,
        simulations_router,
        scenarios_router,
        agents_router,
        checkpoints_router,
        xr_packs_router,
        causal_router,
        audit_router,
    )
    
    app.include_router(health_router, prefix="/api/v1", tags=["Health"])
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(simulations_router, prefix="/api/v1/simulations", tags=["Simulations"])
    app.include_router(scenarios_router, prefix="/api/v1/scenarios", tags=["Scenarios"])
    app.include_router(agents_router, prefix="/api/v1/agents", tags=["Agents"])
    app.include_router(checkpoints_router, prefix="/api/v1/checkpoints", tags=["Checkpoints"])
    app.include_router(xr_packs_router, prefix="/api/v1/xr-packs", tags=["XR Packs"])
    app.include_router(causal_router, prefix="/api/v1/causal", tags=["Causal"])
    app.include_router(audit_router, prefix="/api/v1/audit", tags=["Audit"])
    
    # WebSocket router
    from ..websocket import ws_router
    app.include_router(ws_router, prefix="/ws", tags=["WebSocket"])
    
    return app


# ============================================================================
# APP INSTANCE
# ============================================================================

app = create_app()


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint"""
    return {
        "name": "CHE·NU™ API",
        "version": get_settings().app_version,
        "status": "operational",
        "docs": "/docs",
        "principle": "GOUVERNANCE > EXÉCUTION",
    }


@app.get("/api", include_in_schema=False)
async def api_info():
    """API information"""
    settings = get_settings()
    return APIResponse(
        success=True,
        data={
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment.value,
            "endpoints": {
                "health": "/api/v1/health",
                "auth": "/api/v1/auth",
                "simulations": "/api/v1/simulations",
                "scenarios": "/api/v1/scenarios",
                "agents": "/api/v1/agents",
                "checkpoints": "/api/v1/checkpoints",
                "xr-packs": "/api/v1/xr-packs",
                "causal": "/api/v1/causal",
                "audit": "/api/v1/audit",
                "websocket": "/ws",
            },
        },
        message="CHE·NU™ API is operational",
    ).model_dump()
