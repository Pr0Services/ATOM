"""
============================================================================
CHE·NU™ V69 — GOVERNANCE MIDDLEWARE
============================================================================
Version: 2.0.0
Purpose: FastAPI middleware for automatic governance checks
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

import logging
import time
from typing import Callable, Dict, List, Optional, Set
from datetime import datetime

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from .models import (
    OPARequest,
    OPADecision,
    Tenant,
    Actor,
    Agent,
    Action,
    HITL,
    Explainability,
    Controls,
    Resource,
    ActionType,
    ActionTarget,
    DataClassification,
    AgentLevel,
    Sphere,
    Autonomy,
    RiskLevel,
    Environment,
    TenantPlan,
)
from .opa_client import OPAClient, OPAConfig

logger = logging.getLogger(__name__)


# ============================================================================
# ROUTE CONFIGURATION
# ============================================================================

class GovernedRoute:
    """Configuration for a governed route"""
    
    def __init__(
        self,
        path_pattern: str,
        method: str,
        action_type: ActionType,
        action_target: ActionTarget,
        data_classification: DataClassification = DataClassification.INTERNAL,
        sphere: Sphere = Sphere.BUSINESS,
        require_hitl: bool = False,
        agent_level: AgentLevel = AgentLevel.L1,
        risk_level: RiskLevel = RiskLevel.LOW,
    ):
        self.path_pattern = path_pattern
        self.method = method.upper()
        self.action_type = action_type
        self.action_target = action_target
        self.data_classification = data_classification
        self.sphere = sphere
        self.require_hitl = require_hitl
        self.agent_level = agent_level
        self.risk_level = risk_level

    def matches(self, path: str, method: str) -> bool:
        """Check if route matches request"""
        # Simple pattern matching (could be enhanced with regex)
        if self.method != method.upper():
            return False
        
        # Check path pattern
        if self.path_pattern.endswith("*"):
            return path.startswith(self.path_pattern[:-1])
        return path == self.path_pattern


# ============================================================================
# DEFAULT GOVERNED ROUTES
# ============================================================================

DEFAULT_GOVERNED_ROUTES: List[GovernedRoute] = [
    # Simulation routes
    GovernedRoute(
        "/api/v1/simulations*",
        "POST",
        ActionType.RUN_SIMULATION,
        ActionTarget.SIMULATION,
        sphere=Sphere.BUSINESS,
    ),
    
    # Export routes - require HITL
    GovernedRoute(
        "/api/v1/exports*",
        "POST",
        ActionType.EXPORT_ARTIFACT,
        ActionTarget.ARTIFACT,
        require_hitl=True,
    ),
    
    # XR routes - read only
    GovernedRoute(
        "/api/v1/xr/*",
        "GET",
        ActionType.DISCUSS,
        ActionTarget.XR,
    ),
    
    # Agent registry
    GovernedRoute(
        "/api/v1/agents*",
        "POST",
        ActionType.WRITE,
        ActionTarget.AGENT_REGISTRY,
        require_hitl=True,
        risk_level=RiskLevel.MEDIUM,
    ),
    
    # Data operations
    GovernedRoute(
        "/api/v1/data*",
        "DELETE",
        ActionType.DELETE,
        ActionTarget.DATA,
        require_hitl=True,
        risk_level=RiskLevel.HIGH,
    ),
]


# ============================================================================
# MIDDLEWARE
# ============================================================================

class GovernanceMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for automatic OPA governance checks.
    
    Usage:
        app = FastAPI()
        app.add_middleware(
            GovernanceMiddleware,
            opa_config=OPAConfig(),
            governed_routes=DEFAULT_GOVERNED_ROUTES,
        )
    """

    def __init__(
        self,
        app: FastAPI,
        opa_config: Optional[OPAConfig] = None,
        governed_routes: Optional[List[GovernedRoute]] = None,
        excluded_paths: Optional[Set[str]] = None,
        fail_open: bool = False,  # Default: fail closed (GOUVERNANCE > EXÉCUTION)
    ):
        super().__init__(app)
        self.opa_client = OPAClient(opa_config)
        self.governed_routes = governed_routes or DEFAULT_GOVERNED_ROUTES
        self.excluded_paths = excluded_paths or {
            "/health",
            "/ready",
            "/metrics",
            "/docs",
            "/openapi.json",
            "/redoc",
        }
        self.fail_open = fail_open

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Process request through governance check"""
        start_time = time.time()
        
        # Skip excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
        
        # Find matching governed route
        governed_route = self._find_matching_route(
            request.url.path,
            request.method,
        )
        
        if governed_route is None:
            # Not a governed route - proceed
            return await call_next(request)
        
        # Build OPA request
        try:
            opa_request = await self._build_opa_request(request, governed_route)
        except Exception as e:
            logger.error(f"Failed to build OPA request: {e}")
            if self.fail_open:
                return await call_next(request)
            return self._deny_response("GOVERNANCE_REQUEST_BUILD_FAILED")
        
        # Make governance decision
        try:
            decision = await self.opa_client.decide(opa_request)
        except Exception as e:
            logger.error(f"OPA decision failed: {e}")
            if self.fail_open:
                return await call_next(request)
            return self._deny_response("GOVERNANCE_DECISION_FAILED")
        
        # Process decision
        if not decision.allow:
            return self._deny_response(
                decision.deny_reasons,
                decision.trace_id,
                decision.required_controls,
            )
        
        # Check if HITL is needed but not provided
        if decision.needs_hitl and not self._has_hitl_approval(request):
            return self._hitl_required_response(
                decision.trace_id,
                decision.required_controls,
            )
        
        # Proceed with request
        response = await call_next(request)
        
        # Add governance headers
        response.headers["X-Governance-Decision"] = "allow"
        response.headers["X-Governance-Trace-Id"] = decision.trace_id or ""
        response.headers["X-Governance-Audit-Level"] = decision.audit_level.value
        
        # Log timing
        duration = time.time() - start_time
        logger.info(
            f"Governance check: {request.url.path} | "
            f"decision=allow | "
            f"duration={duration:.3f}s"
        )
        
        return response

    def _find_matching_route(
        self,
        path: str,
        method: str,
    ) -> Optional[GovernedRoute]:
        """Find matching governed route"""
        for route in self.governed_routes:
            if route.matches(path, method):
                return route
        return None

    async def _build_opa_request(
        self,
        request: Request,
        governed_route: GovernedRoute,
    ) -> OPARequest:
        """Build OPA request from HTTP request"""
        # Extract tenant from header or query
        tenant_id = request.headers.get(
            "X-Tenant-Id",
            request.query_params.get("tenant_id", "unknown"),
        )
        
        # Extract user from header
        user_id = request.headers.get(
            "X-User-Id",
            request.query_params.get("user_id", "unknown"),
        )
        
        # Extract agent from header
        agent_id = request.headers.get(
            "X-Agent-Id",
            "default-agent",
        )
        
        # Extract environment
        env_str = request.headers.get("X-Environment", "labs")
        environment = Environment(env_str) if env_str in ["labs", "pilot", "prod"] else Environment.LABS
        
        # Extract HITL approval
        hitl_approved = request.headers.get("X-HITL-Approved", "false").lower() == "true"
        hitl_approver = request.headers.get("X-HITL-Approver-Id")
        
        # Extract explainability
        explain_provided = request.headers.get("X-Explainability-Provided", "true").lower() == "true"
        
        # Extract trace ID
        trace_id = request.headers.get(
            "X-Trace-Id",
            request.headers.get("X-Request-Id", ""),
        )
        
        # Build request
        return OPARequest(
            trace_id=trace_id or None,
            environment=environment,
            tenant=Tenant(
                id=tenant_id,
                plan=TenantPlan.PRO,  # Could be extracted from JWT
            ),
            actor=Actor(
                type="user",
                id=user_id,
            ),
            agent=Agent(
                blueprint_id=agent_id,
                level=governed_route.agent_level,
                sphere=governed_route.sphere,
                autonomy=Autonomy.ASSISTED,
                risk_level=governed_route.risk_level,
                is_autogen=False,
                is_user_hired=True,
            ),
            action=Action(
                type=governed_route.action_type,
                target=governed_route.action_target,
                resource_id=self._extract_resource_id(request),
                data_classification=governed_route.data_classification,
            ),
            hitl=HITL(
                required=governed_route.require_hitl,
                approved=hitl_approved,
                approver_id=hitl_approver,
            ),
            explainability=Explainability(
                required=True,
                provided=explain_provided,
            ),
            controls=Controls(
                audit_logging=True,
                trace_context=trace_id,
            ),
            resource=Resource(
                synthetic=True,
            ),
        )

    def _extract_resource_id(self, request: Request) -> str:
        """Extract resource ID from request path"""
        # Simple extraction - could be enhanced
        parts = request.url.path.strip("/").split("/")
        if len(parts) > 3:
            return parts[-1]
        return ""

    def _has_hitl_approval(self, request: Request) -> bool:
        """Check if request has HITL approval"""
        return request.headers.get("X-HITL-Approved", "false").lower() == "true"

    def _deny_response(
        self,
        reasons: List[str] | str,
        trace_id: Optional[str] = None,
        required_controls: Optional[List[str]] = None,
    ) -> JSONResponse:
        """Create denial response"""
        if isinstance(reasons, str):
            reasons = [reasons]
        
        return JSONResponse(
            status_code=403,
            content={
                "error": "GOVERNANCE_DENIED",
                "reasons": reasons,
                "required_controls": required_controls or [],
                "trace_id": trace_id,
                "timestamp": datetime.utcnow().isoformat(),
            },
            headers={
                "X-Governance-Decision": "deny",
                "X-Governance-Trace-Id": trace_id or "",
            },
        )

    def _hitl_required_response(
        self,
        trace_id: Optional[str] = None,
        required_controls: Optional[List[str]] = None,
    ) -> JSONResponse:
        """Create HITL required response"""
        return JSONResponse(
            status_code=428,  # Precondition Required
            content={
                "error": "HITL_APPROVAL_REQUIRED",
                "message": "Human-in-the-loop approval is required for this action",
                "required_controls": required_controls or ["HITL_APPROVAL_REQUIRED"],
                "trace_id": trace_id,
                "timestamp": datetime.utcnow().isoformat(),
                "instructions": {
                    "header": "X-HITL-Approved",
                    "value": "true",
                    "approver_header": "X-HITL-Approver-Id",
                },
            },
            headers={
                "X-Governance-Decision": "hitl_required",
                "X-Governance-Trace-Id": trace_id or "",
            },
        )


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

class GovernanceChecker:
    """
    FastAPI dependency for manual governance checks.
    
    Usage:
        @app.post("/api/v1/sensitive-action")
        async def sensitive_action(
            governance: GovernanceChecker = Depends(get_governance_checker),
        ):
            decision = await governance.check(
                action_type=ActionType.EXECUTE,
                action_target=ActionTarget.SYSTEM,
            )
            if not decision.allow:
                raise HTTPException(403, decision.deny_reasons)
    """

    def __init__(
        self,
        request: Request,
        opa_client: Optional[OPAClient] = None,
    ):
        self.request = request
        self.opa_client = opa_client or OPAClient()

    async def check(
        self,
        action_type: ActionType,
        action_target: ActionTarget,
        data_classification: DataClassification = DataClassification.INTERNAL,
        sphere: Sphere = Sphere.BUSINESS,
        resource_id: str = "",
    ) -> OPADecision:
        """Perform governance check"""
        # Build request from HTTP request
        tenant_id = self.request.headers.get("X-Tenant-Id", "unknown")
        user_id = self.request.headers.get("X-User-Id", "unknown")
        agent_id = self.request.headers.get("X-Agent-Id", "default")
        
        opa_request = OPARequest(
            tenant=Tenant(id=tenant_id),
            actor=Actor(type="user", id=user_id),
            agent=Agent(
                blueprint_id=agent_id,
                level=AgentLevel.L1,
                sphere=sphere,
                autonomy=Autonomy.ASSISTED,
                risk_level=RiskLevel.LOW,
            ),
            action=Action(
                type=action_type,
                target=action_target,
                resource_id=resource_id,
                data_classification=data_classification,
            ),
            explainability=Explainability(required=True, provided=True),
            controls=Controls(audit_logging=True),
        )
        
        return await self.opa_client.decide(opa_request)


def get_governance_checker(request: Request) -> GovernanceChecker:
    """Dependency provider for GovernanceChecker"""
    return GovernanceChecker(request)


# ============================================================================
# FASTAPI INTEGRATION
# ============================================================================

def setup_governance(
    app: FastAPI,
    opa_config: Optional[OPAConfig] = None,
    governed_routes: Optional[List[GovernedRoute]] = None,
    excluded_paths: Optional[Set[str]] = None,
):
    """
    Setup governance middleware on FastAPI app.
    
    Usage:
        app = FastAPI()
        setup_governance(app)
    """
    app.add_middleware(
        GovernanceMiddleware,
        opa_config=opa_config,
        governed_routes=governed_routes,
        excluded_paths=excluded_paths,
    )
    
    logger.info("Governance middleware configured")
