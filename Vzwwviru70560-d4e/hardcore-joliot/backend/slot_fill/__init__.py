"""
============================================================================
CHE·NU™ V69 — SLOT FILL ENGINE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_ENG_SLOT_FILL_AGENT_ASSIGNMENT.md
- CHE-NU_ENG_SLOT_FILL_CAUSAL_PRIORITY.md
- CHE-NU_ENG_SLOT_FILL_EXPLAINABILITY.md
- CHE-NU_ENG_SLOT_FILL_XR_VISUALIZATION.md
- CHE-NU_ENG_NEUROMORPHIC_LATTICE_V1.md
- CHE-NU_ENG_SEMANTIC_AGENT_COMMUNICATION.md

Principle: GOUVERNANCE > EXÉCUTION

Core concepts:
- 1 slot = 1 agent principal
- Aucun agent ne contrôle tout le document
- Un agent remplit. Un autre vérifie. Un humain décide.
- XR = lecture seule
- Explainability obligatoire avant HITL
============================================================================
"""

# Models
from .models import (
    Slot,
    SlotType,
    SlotStatus,
    RiskLevel,
    AgentType,
    SlotExplainability,
    XRSlotVisualization,
    CausalPriority,
    SlotFillRequest,
    SlotFillResult,
    Document,
    SLOT_TO_AGENT_MAPPING,
)

# Assignment
from .assignment import (
    SlotAssigner,
    SlotFillOrchestrator,
    AssignmentRule,
    AssignmentResult,
    create_assigner,
    create_orchestrator,
)

# Priority
from .priority import (
    CausalImpactCalculator,
    SlotPriorityRanker,
    PriorityFilter,
    ImpactFactors,
    create_impact_calculator,
    create_priority_ranker,
    create_priority_filter,
)

# Explainability
from .explainability import (
    ExplainabilityGenerator,
    ExplainabilityValidator,
    ExplainabilityStore,
    ExplainabilityLayer,
    ExplainabilityLevel,
    get_required_level,
    create_explainability_layer,
)

# XR Visualization
from .xr import (
    XRSceneBuilder,
    XRLayoutEngine,
    XRInteractionHandler,
    XRSlotFillArtifact,
    XRScene,
    XRNode,
    XRConnection,
    XRPosition,
    LayoutStrategy,
    status_to_color,
    create_scene_builder,
    create_interaction_handler,
    create_artifact_generator,
)

# Neuromorphic
from .neuromorphic import (
    NeuromorphicLattice,
    SignalBus,
    SpikeEvent,
    Synapse,
    AgentNeuroMap,
    SpikeInputType,
    SpikeOutputType,
    create_lattice,
    create_agent_map,
)

# Semantic Communication
from .semantic import (
    SemanticPacket,
    SemanticCodec,
    SemanticChannel,
    SemanticGovernance,
    OntologyRegistry,
    Concept,
    Relation,
    ConceptCategory,
    RelationType,
    StateType,
    create_ontology,
    create_codec,
    create_channel,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "Slot", "SlotType", "SlotStatus", "RiskLevel", "AgentType",
    "SlotExplainability", "XRSlotVisualization", "CausalPriority",
    "SlotFillRequest", "SlotFillResult", "Document",
    "SLOT_TO_AGENT_MAPPING",
    # Assignment
    "SlotAssigner", "SlotFillOrchestrator",
    "AssignmentRule", "AssignmentResult",
    "create_assigner", "create_orchestrator",
    # Priority
    "CausalImpactCalculator", "SlotPriorityRanker", "PriorityFilter",
    "ImpactFactors",
    "create_impact_calculator", "create_priority_ranker", "create_priority_filter",
    # Explainability
    "ExplainabilityGenerator", "ExplainabilityValidator",
    "ExplainabilityStore", "ExplainabilityLayer",
    "ExplainabilityLevel", "get_required_level",
    "create_explainability_layer",
    # XR
    "XRSceneBuilder", "XRLayoutEngine", "XRInteractionHandler", "XRSlotFillArtifact",
    "XRScene", "XRNode", "XRConnection", "XRPosition",
    "LayoutStrategy", "status_to_color",
    "create_scene_builder", "create_interaction_handler", "create_artifact_generator",
    # Neuromorphic
    "NeuromorphicLattice", "SignalBus", "SpikeEvent",
    "Synapse", "AgentNeuroMap",
    "SpikeInputType", "SpikeOutputType",
    "create_lattice", "create_agent_map",
    # Semantic
    "SemanticPacket", "SemanticCodec", "SemanticChannel",
    "SemanticGovernance", "OntologyRegistry",
    "Concept", "Relation",
    "ConceptCategory", "RelationType", "StateType",
    "create_ontology", "create_codec", "create_channel",
]
