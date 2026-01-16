"""
============================================================================
CHE·NU™ V70 — CORS CONFIGURATION
============================================================================
CORS middleware configuration for Backend V69 to accept Frontend V68.6 requests
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.
    
    This allows the Frontend V68.6 (Vite dev server at localhost:5173)
    to communicate with Backend V69 (FastAPI at localhost:8000).
    """
    
    # Allowed origins
    origins = [
        # Frontend development server
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        
        # Frontend production (update with actual domain)
        "https://app.che-nu.com",
        "https://che-nu.com",
        
        # Additional development origins
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=[
            "X-Request-ID",
            "X-Checkpoint-ID",
            "X-Simulation-ID",
        ],
    )


# For production, use environment variables
def configure_cors_production(app: FastAPI, allowed_origins: list[str]) -> None:
    """
    Configure CORS for production with specific allowed origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Request-ID",
        ],
        expose_headers=[
            "X-Request-ID",
            "X-Checkpoint-ID", 
            "X-Simulation-ID",
        ],
        max_age=600,  # Cache preflight for 10 minutes
    )
