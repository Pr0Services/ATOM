"""
============================================================================
CHE·NU™ V69 — ENTERPRISE MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_XR_PACK_V1_7_TRUE_SIGNALS_EXPLAIN_ONDEMAND_WASM_VERIFY.md
- CHE-NU_Agent_Intelligence_System.md
- CHE-NU_Performance_Dashboard_Spec.md
- CHE-NU_FASTAPI_SERVICE_GENERATOR_V1_1.md
- CHE-NU_OPA_REAL_INTEGRATION_V1_3.md

"Enterprise-grade XR cockpit with 287+ agents"

Principle: GOUVERNANCE > EXÉCUTION, XR = READ ONLY
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash, sign_artifact,
    # XR Pack V1.7
    SignalSeries, SphereSignals, GlobalMetrics, TrueSignals,
    HeatmapTile, TrueHeatmap,
    ExplainRange, ExplainItem, ExplainIndex,
    WASMVerifyConfig,
    # Agent Intelligence
    AgentTier, AgentDomain, RiskLevel,
    AgentBlueprint, AgentInstance, AgentHealth,
    # Performance
    SystemHealth, AgentMetrics, MultiAgentMetrics,
    GovernanceMetrics, PerformanceDashboard,
    # FastAPI Service
    SimulationRequest, OPADecision, ArtifactMetadata,
)

# XR Pack V1.7
from .xr_pack_v17 import (
    XRPackV17Builder,
    SignalGenerator,
    HeatmapCalculator,
    ExplainRangeBuilder,
    WASMVerifier,
    create_xr_pack_v17_builder,
)

# Systems (Agent Intelligence, Performance, OPA, FastAPI)
from .systems import (
    BlueprintRegistry,
    AgentIntelligenceSystem,
    PerformanceDashboardService,
    OPARealIntegration,
    FastAPIServiceGenerator,
    create_agent_intelligence,
    create_performance_dashboard,
    create_opa_integration,
    create_fastapi_service,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash", "sign_artifact",
    # XR Pack V1.7 Models
    "SignalSeries", "SphereSignals", "GlobalMetrics", "TrueSignals",
    "HeatmapTile", "TrueHeatmap",
    "ExplainRange", "ExplainItem", "ExplainIndex",
    "WASMVerifyConfig",
    # Agent Intelligence Models
    "AgentTier", "AgentDomain", "RiskLevel",
    "AgentBlueprint", "AgentInstance", "AgentHealth",
    # Performance Models
    "SystemHealth", "AgentMetrics", "MultiAgentMetrics",
    "GovernanceMetrics", "PerformanceDashboard",
    # FastAPI Models
    "SimulationRequest", "OPADecision", "ArtifactMetadata",
    # XR Pack V1.7
    "XRPackV17Builder", "SignalGenerator", "HeatmapCalculator",
    "ExplainRangeBuilder", "WASMVerifier", "create_xr_pack_v17_builder",
    # Systems
    "BlueprintRegistry", "AgentIntelligenceSystem",
    "PerformanceDashboardService", "OPARealIntegration",
    "FastAPIServiceGenerator",
    "create_agent_intelligence", "create_performance_dashboard",
    "create_opa_integration", "create_fastapi_service",
]
