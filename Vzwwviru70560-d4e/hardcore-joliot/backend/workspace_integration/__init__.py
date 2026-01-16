"""
============================================================================
CHE·NU™ V69 — WORKSPACE INTEGRATION MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_WORKSPACE_ENGINE_MAP.md
- CHE-NU_WORLD_ENGINE_INTEGRATION_V1_2.md
- CHE-NU_Domaines_Metiers_Industries.md
- CHE-NU_Explainability_UI_and_Public_Transparency.md
- CHE-NU_V52_Phase_4_Execution_Playbook.md
- CHE-NU_V52_Phase_5_Enterprise_Adoption_Playbook.md

"Engines = representational-only, GOUVERNANCE > EXÉCUTION"

Principle: LABS → PILOT → PROD
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # Engine Map
    EngineType, WorkspaceEngine, EngineMap,
    # World Engine
    WorldEngineConfig, WorldState, WorldEvent, WorldSimulationResult,
    # Domains
    DomainRole, BusinessDomain, DomainDictionary,
    # Explainability UI
    ExplainabilityAccessLevel, ExplainabilityVisibility,
    ExplainabilityUIConfig, ExplainabilityEntry,
    # Playbooks
    PhaseGateStatus, ReadinessChecklistItem, PerformanceTarget,
    Phase4Playbook, Phase5Playbook,
)

# Systems
from .systems import (
    WorkspaceEngineMapService,
    WorldEngineIntegrationService,
    DomainDictionaryService,
    ExplainabilityUIService,
    PlaybookService,
    create_engine_map_service,
    create_world_engine_service,
    create_domain_dictionary_service,
    create_explainability_ui_service,
    create_playbook_service,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash",
    # Engine Map
    "EngineType", "WorkspaceEngine", "EngineMap",
    # World Engine
    "WorldEngineConfig", "WorldState", "WorldEvent", "WorldSimulationResult",
    # Domains
    "DomainRole", "BusinessDomain", "DomainDictionary",
    # Explainability UI
    "ExplainabilityAccessLevel", "ExplainabilityVisibility",
    "ExplainabilityUIConfig", "ExplainabilityEntry",
    # Playbooks
    "PhaseGateStatus", "ReadinessChecklistItem", "PerformanceTarget",
    "Phase4Playbook", "Phase5Playbook",
    # Services
    "WorkspaceEngineMapService", "WorldEngineIntegrationService",
    "DomainDictionaryService", "ExplainabilityUIService", "PlaybookService",
    "create_engine_map_service", "create_world_engine_service",
    "create_domain_dictionary_service", "create_explainability_ui_service",
    "create_playbook_service",
]
