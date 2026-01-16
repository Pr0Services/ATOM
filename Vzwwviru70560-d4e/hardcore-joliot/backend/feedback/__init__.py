"""
============================================================================
CHE·NU™ V69 — FEEDBACK ENGINE
============================================================================
Version: 1.0.0
Purpose: Temporal feedback simulation with stability control
Principle: GOUVERNANCE > EXÉCUTION - Deterministic, auditable loops

The Feedback Engine transforms static causal calculations into dynamic
temporal simulations with feedback loops (T -> T+1).

Supports:
- Positive loops (auto-reinforcing): growth, contagion, compound
- Negative loops (stabilizing): regulation, saturation, limits
- L2 Safety Controller: stability monitoring, clamping, damping

Usage:
    from feedback import create_audited_simulation
    
    engine = create_audited_simulation(
        name="Supply Chain",
        initial_values={"Budget": 1000000, "Efficiency": 0.85},
        feedback_rules={"Budget": {"Budget": 0.95, "Production": 0.1}},
        transfer_rules={"Production": {"Budget": 0.85}},
        num_ticks=10,
    )
    
    results = engine.run()
    print(f"Merkle Root: {engine.get_merkle_root()}")
============================================================================
"""

# Models
from .models import (
    # Enums
    LoopType,
    FeedbackModel,
    SafetyAction,
    StabilityStatus,
    # Core models
    Slot,
    WorldState,
    FeedbackEdge,
    TransferFunction,
    FeedbackParams,
    SimulationArtifact,
    SimulationConfig,
)

# Engines
from .loops import (
    L2SafetyController,
    FeedbackLoopEngine,
    create_simple_simulation,
    AuditedFeedbackEngine,
    create_audited_simulation,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Enums
    "LoopType",
    "FeedbackModel",
    "SafetyAction",
    "StabilityStatus",
    # Models
    "Slot",
    "WorldState",
    "FeedbackEdge",
    "TransferFunction",
    "FeedbackParams",
    "SimulationArtifact",
    "SimulationConfig",
    # Engines
    "L2SafetyController",
    "FeedbackLoopEngine",
    "create_simple_simulation",
    "AuditedFeedbackEngine",
    "create_audited_simulation",
]
