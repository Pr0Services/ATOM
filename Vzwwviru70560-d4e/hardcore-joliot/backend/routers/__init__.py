"""
CHE·NU™ V75 Backend - Routers Package

All API routers.

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from routers.auth import router as auth_router
from routers.dashboard import router as dashboard_router
from routers.threads import router as threads_router
from routers.agents import router as agents_router
from routers.governance import router as governance_router
from routers.nova import router as nova_router
from routers.spheres import router as spheres_router
from routers.xr import router as xr_router
from routers.decisions import router as decisions_router
from routers.dataspaces import router as dataspaces_router
from routers.streaming import router as streaming_router

# V75 Extended routers
from routers.meetings import router as meetings_router
from routers.immobilier import router as immobilier_router
from routers.workspaces import router as workspaces_router
from routers.oneclick import router as oneclick_router
from routers.ocw import router as ocw_router
from routers.backstage import router as backstage_router
from routers.memory import router as memory_router
from routers.dataspace_engine import router as dataspace_engine_router
from routers.layout import router as layout_router
from routers.identity import router as identity_router
from routers.templates import router as templates_router
from routers.notifications import router as notifications_router
from routers.activity import router as activity_router
from routers.search import router as search_router
from routers.files import router as files_router
from routers.comments import router as comments_router
from routers.tags import router as tags_router

# Module aliases for main.py compatibility
from routers import auth, dashboard, threads, agents, governance, nova, spheres, xr, decisions, dataspaces, streaming

__all__ = [
    # Routers
    "auth_router",
    "dashboard_router",
    "threads_router",
    "agents_router",
    "governance_router",
    "nova_router",
    "spheres_router",
    "xr_router",
    "decisions_router",
    "dataspaces_router",
    "streaming_router",
    # V75 Extended
    "meetings_router",
    "immobilier_router",
    # Modules
    "auth",
    "dashboard",
    "threads",
    "agents",
    "governance",
    "nova",
    "spheres",
    "xr",
    "decisions",
    "dataspaces",
    "streaming",
]
