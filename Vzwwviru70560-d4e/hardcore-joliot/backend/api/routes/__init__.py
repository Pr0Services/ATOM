"""
CHE·NU™ V82 — API Routes Re-exports

Re-exports all route modules from v1 for backward compatibility.
"""

from backend.api.v1.routes.auth_routes import router as auth_routes_router
from backend.api.v1.routes.sphere_routes import router as sphere_routes_router
from backend.api.v1.routes.thread_routes import router as thread_routes_router
from backend.api.v1.routes.governance_routes import router as governance_routes_router
from backend.api.v1.routes.xr_routes import router as xr_routes_router
from backend.api.v1.routes.checkpoint_routes import router as checkpoint_routes_router
from backend.api.v1.routes.agent_routes import router as agent_routes_router
from backend.api.v1.routes.nova_routes import router as nova_routes_router


# Create module-like objects for compatibility with main.py imports
class _RouteModule:
    """Wrapper to expose router attribute."""
    def __init__(self, router):
        self.router = router


auth_routes = _RouteModule(auth_routes_router)
sphere_routes = _RouteModule(sphere_routes_router)
thread_routes = _RouteModule(thread_routes_router)
governance_routes = _RouteModule(governance_routes_router)
xr_routes = _RouteModule(xr_routes_router)
checkpoint_routes = _RouteModule(checkpoint_routes_router)
agent_routes = _RouteModule(agent_routes_router)
nova_routes = _RouteModule(nova_routes_router)


__all__ = [
    "auth_routes",
    "sphere_routes",
    "thread_routes",
    "governance_routes",
    "xr_routes",
    "checkpoint_routes",
    "agent_routes",
    "nova_routes",
]
