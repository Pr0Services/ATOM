"""
AT·OM API Routes
================

Canon AT·OM Protocol de Connexion API.

ENDPOINTS:
- POST /api/v1/sceau/activate : Validate Sceau 2s activation
- POST /api/v1/swarm/activate : Trigger swarm explosion
- GET /api/v1/modules/status : Get 350 agents health status
- DELETE /api/v1/protocol-999 : Trigger dispersion (Levels 1-3)
- GET /api/v1/frequency : Get current 999Hz resonance
- GET /api/v1/health : Technical health check

ZERO LOG: No personal data stored.
"""

from .swarm_routes import router as swarm_router

__all__ = ["swarm_router"]
