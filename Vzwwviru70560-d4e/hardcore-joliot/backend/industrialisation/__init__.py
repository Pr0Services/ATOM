"""
============================================================================
CHE·NU™ V69 — INDUSTRIALISATION MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_INDUSTRIALISATION_PLAN.md
- CHE-NU_XR_PACK_AUTOGEN_V1_4.md
- CHE-NU_WORLD_SIM_GAMEPLAY_MECHANICS.md
- CHE-NU_Prompt_Collection_Architecture.md
- CHE-NU_V52_API_Agent_Management_Best_Practices.md
- CHE-NU_V52_OPA_Policy_Bundles_Templates.md

"POC → MVP → Enterprise: GOUVERNANCE > EXÉCUTION"

Principle: Default Deny, Structure not Restriction
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # Industrialization
    ProductLayer, IndustrializationPhase,
    ProductLayerSpec, IndustrializationPlan,
    # XR Pack
    XRPackManifest, ReplayFrame, HeatmapTile, DiffEntry, XRPack,
    # Gameplay
    GameplayMechanicType, Quest, GameplayState,
    # Prompt Collection
    PromptAxis, PromptAsset, PromptLibrary,
    # API Agent Management
    AgentRegistryEntry, EvaluationResult, APIAgentManagementConfig,
    # OPA Bundles
    PolicyRule, PolicyBundle, BundleRegistry,
)

# Systems
from .systems import (
    IndustrializationService,
    XRPackAutoGenService,
    GameplayMechanicsService,
    PromptCollectionService,
    APIAgentManagementService,
    OPAPolicyBundlesService,
    create_industrialization_service,
    create_xr_pack_service,
    create_gameplay_service,
    create_prompt_collection_service,
    create_api_agent_service,
    create_opa_bundles_service,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash",
    # Industrialization
    "ProductLayer", "IndustrializationPhase",
    "ProductLayerSpec", "IndustrializationPlan",
    # XR Pack
    "XRPackManifest", "ReplayFrame", "HeatmapTile", "DiffEntry", "XRPack",
    # Gameplay
    "GameplayMechanicType", "Quest", "GameplayState",
    # Prompt Collection
    "PromptAxis", "PromptAsset", "PromptLibrary",
    # API Agent Management
    "AgentRegistryEntry", "EvaluationResult", "APIAgentManagementConfig",
    # OPA Bundles
    "PolicyRule", "PolicyBundle", "BundleRegistry",
    # Services
    "IndustrializationService", "XRPackAutoGenService",
    "GameplayMechanicsService", "PromptCollectionService",
    "APIAgentManagementService", "OPAPolicyBundlesService",
    "create_industrialization_service", "create_xr_pack_service",
    "create_gameplay_service", "create_prompt_collection_service",
    "create_api_agent_service", "create_opa_bundles_service",
]
