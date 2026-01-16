"""
============================================================================
CHE·NU™ V69 — GOVERNANCE PACKAGE
============================================================================
Version: 2.0.0
Purpose: OPA-based governance for CHE·NU™
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from .models import (
    # Enums
    Environment,
    AgentLevel,
    Sphere,
    Autonomy,
    RiskLevel,
    ActionType,
    ActionTarget,
    DataClassification,
    AuditLevel,
    TenantPlan,
    # Models
    Tenant,
    Actor,
    Agent,
    Action,
    HITL,
    Explainability,
    Controls,
    Resource,
    Context,
    OPARequest,
    OPADecision,
    AuditDecision,
    # Factories
    create_simulation_request,
    create_export_request,
)

from .opa_client import (
    OPAConfig,
    OPAClient,
    get_opa_client,
    opa_decide,
    opa_decide_sync,
    require_governance,
)

from .middleware import (
    GovernedRoute,
    GovernanceMiddleware,
    GovernanceChecker,
    get_governance_checker,
    setup_governance,
    DEFAULT_GOVERNED_ROUTES,
)

__all__ = [
    # Enums
    "Environment",
    "AgentLevel",
    "Sphere",
    "Autonomy",
    "RiskLevel",
    "ActionType",
    "ActionTarget",
    "DataClassification",
    "AuditLevel",
    "TenantPlan",
    # Models
    "Tenant",
    "Actor",
    "Agent",
    "Action",
    "HITL",
    "Explainability",
    "Controls",
    "Resource",
    "Context",
    "OPARequest",
    "OPADecision",
    "AuditDecision",
    # Factories
    "create_simulation_request",
    "create_export_request",
    # Client
    "OPAConfig",
    "OPAClient",
    "get_opa_client",
    "opa_decide",
    "opa_decide_sync",
    "require_governance",
    # Middleware
    "GovernedRoute",
    "GovernanceMiddleware",
    "GovernanceChecker",
    "get_governance_checker",
    "setup_governance",
    "DEFAULT_GOVERNED_ROUTES",
]

__version__ = "2.0.0"
