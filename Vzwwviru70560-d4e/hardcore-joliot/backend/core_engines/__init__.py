"""
============================================================================
CHE·NU™ V69 — CORE ENGINES MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_CAUSAL_DECISION_ENGINE.md
- CHE-NU_CAUSAL_INFERENCE_ENGINE.md
- CHE-NU_WORLDENGINE_CORE_V1.md
- CHE-NU_WORLD_TO_GAME_LOGIC_BRIDGE.md

"CHE·NU ne dit pas quoi faire. Il révèle ce qui compte vraiment."

Principle: GOUVERNANCE > EXÉCUTION
Architecture: Slots → WorldEngine → DAG Causal → Analyses → XR Explain → Humain décide
============================================================================
"""

# Models
from .models import (
    Slot,
    CausalDAG,
    CausalEdge,
    EdgeType,
    Artifact,
    WorldState,
    Intervention,
    InterventionType,
    CounterfactualQuery,
    SensitivityScore,
    FeedbackLoop,
    FeedbackType,
    GameMapping,
    GameMechanicType,
    generate_id,
    compute_hash,
    sign_artifact,
    verify_signature,
)

# WorldEngine
from .world_engine import (
    WorldEngineCore,
    Worker,
    CausalRule,
    create_engine,
    create_feedback_loop,
)

# Causal Inference
from .causal_inference import (
    CausalInferenceEngine,
    DAGBuilder,
    create_inference_engine,
    create_dag_builder,
    create_intervention,
)

# Causal Decision
from .causal_decision import (
    CausalDecisionEngine,
    SensitivityAnalyzer,
    CausalGovernance,
    create_decision_engine,
)

# Game Bridge
from .game_bridge import (
    WorldToGameBridge,
    MechanicFilter,
    MappingRule,
    create_bridge,
    create_filter,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "Slot", "CausalDAG", "CausalEdge", "EdgeType",
    "Artifact", "WorldState",
    "Intervention", "InterventionType", "CounterfactualQuery",
    "SensitivityScore", "FeedbackLoop", "FeedbackType",
    "GameMapping", "GameMechanicType",
    "generate_id", "compute_hash", "sign_artifact", "verify_signature",
    # WorldEngine
    "WorldEngineCore", "Worker", "CausalRule",
    "create_engine", "create_feedback_loop",
    # Causal Inference
    "CausalInferenceEngine", "DAGBuilder",
    "create_inference_engine", "create_dag_builder", "create_intervention",
    # Causal Decision
    "CausalDecisionEngine", "SensitivityAnalyzer", "CausalGovernance",
    "create_decision_engine",
    # Game Bridge
    "WorldToGameBridge", "MechanicFilter", "MappingRule",
    "create_bridge", "create_filter",
]
