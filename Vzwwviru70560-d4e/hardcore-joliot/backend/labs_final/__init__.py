"""
============================================================================
CHE·NU™ V69 — LABS FINAL MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_LABS_Chapter_1.md (Innovation Track)
- CHE-NU_WORKSPACE_AGENT_ROLES.md
- CHE-NU_XR_PACK_V1_5_REAL_DIFF_HEATMAP_SIGNED_ZIP.md
- CHE-NU_XR_PACK_V1_6_CHUNKED_REPLAY_DIVERGENCE_ED25519.md
- CHE-NU_V52_Adoption_Upgrade_Plan_Consolidated.md

"Execution builds the product. LABS builds the future."

Principle: GOUVERNANCE > EXÉCUTION, Human is commit point
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # LABS Chapter 1
    LABSDomain, TaskStatus, LivingTask, LABSFeature, LABSInnovationTrack,
    # Workspace Agent Roles
    AgentCategory, AgentCapability, AgentRestriction,
    WorkspaceAgentRole, WorkspaceAgentRegistry,
    # XR Pack V1.5
    MetricsDelta, ComputedHeatmapTile, PackSignature, XRPackV15,
    # XR Pack V1.6
    DivergencePoint, DivergenceConfig, ReplayChunk, ReplayIndex,
    Ed25519Signature, XRPackV16,
    # Adoption Upgrade Plan
    UpgradePhase, UpgradeTask, PerformanceBaseline, PerformanceTarget,
    AdoptionUpgradePlan,
)

# Systems
from .systems import (
    LABSInnovationService,
    WorkspaceAgentRolesService,
    XRPackV15Service,
    XRPackV16Service,
    AdoptionUpgradePlanService,
    create_labs_innovation_service,
    create_workspace_roles_service,
    create_xr_pack_v15_service,
    create_xr_pack_v16_service,
    create_adoption_upgrade_service,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash",
    # LABS Chapter 1
    "LABSDomain", "TaskStatus", "LivingTask", "LABSFeature", "LABSInnovationTrack",
    # Workspace Agent Roles
    "AgentCategory", "AgentCapability", "AgentRestriction",
    "WorkspaceAgentRole", "WorkspaceAgentRegistry",
    # XR Pack V1.5
    "MetricsDelta", "ComputedHeatmapTile", "PackSignature", "XRPackV15",
    # XR Pack V1.6
    "DivergencePoint", "DivergenceConfig", "ReplayChunk", "ReplayIndex",
    "Ed25519Signature", "XRPackV16",
    # Adoption Upgrade Plan
    "UpgradePhase", "UpgradeTask", "PerformanceBaseline", "PerformanceTarget",
    "AdoptionUpgradePlan",
    # Services
    "LABSInnovationService", "WorkspaceAgentRolesService",
    "XRPackV15Service", "XRPackV16Service", "AdoptionUpgradePlanService",
    "create_labs_innovation_service", "create_workspace_roles_service",
    "create_xr_pack_v15_service", "create_xr_pack_v16_service",
    "create_adoption_upgrade_service",
]
