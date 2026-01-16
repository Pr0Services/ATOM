"""
============================================================================
CHE·NU™ V69 — WORLDENGINE
============================================================================
Version: 1.0.0
Purpose: Central orchestrator for deterministic simulations
Principle: GOUVERNANCE > EXÉCUTION — Zero hallucination, full traceability

The WorldEngine is the heart of CHE·NU™ simulation system.
It transforms Slots (structured data) into certified Artifacts
by applying verifiable causal rules, governed by OPA.

Key features:
- Deterministic execution (same inputs = same outputs)
- Causal rule engine
- Feedback loop dynamics
- Long-term projections (50-100 years)
- Full audit trail
- PQC signatures
- XR Pack generation

Usage:
    from world_engine import IntegratedWorldEngine, ScenarioType
    
    # Create engine
    engine = IntegratedWorldEngine()
    
    # Create simulation
    sim = engine.create_simulation("Budget Forecast")
    
    # Add scenarios
    baseline = engine.add_scenario(
        sim.simulation_id,
        "Baseline",
        {"Budget": 1000000, "Efficiency": 0.85},
        scenario_type=ScenarioType.BASELINE,
    )
    
    aggressive = engine.add_scenario(
        sim.simulation_id,
        "Aggressive",
        {"Budget": 1500000, "Efficiency": 0.75},
    )
    
    # Add rules
    engine.add_rule(
        sim.simulation_id,
        name="Production",
        target_slot="Production",
        source_slots=["Budget", "Efficiency"],
        formula="Production = Budget * Efficiency",
    )
    
    # Run simulation
    results = engine.run_simulation(sim.simulation_id)
    
    # Generate XR Pack
    xr_pack = engine.generate_xr_pack(sim.simulation_id)
    
    # Get audit report
    report = engine.get_audit_report(sim.simulation_id)
============================================================================
"""

# Core
from .core import (
    # Models
    Slot,
    WorldState,
    CausalRule,
    Scenario,
    Simulation,
    SimulationArtifact,
    SimulationConfig,
    SimulationStatus,
    ScenarioType,
    WorkerTask,
    WorkerStatus,
    TimeUnit,
    # Engine
    WorldEngine,
    RuleExecutor,
    create_simple_simulation,
)

# Scenarios
from .scenarios import (
    ScenarioManager,
    ScenarioComparison,
    WhatIfAnalyzer,
)

# Workers
from .workers import (
    Worker,
    WorkerPool,
    WorkerManager,
)

# Temporal
from .temporal import (
    TemporalIterator,
    TemporalRange,
    TemporalSchedule,
    ScheduledEvent,
    LongTermProjector,
    convert_time_units,
)

# Integration
from .integration import (
    IntegratedWorldEngine,
    create_integrated_engine,
    run_quick_simulation,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Core Models
    "Slot",
    "WorldState",
    "CausalRule",
    "Scenario",
    "Simulation",
    "SimulationArtifact",
    "SimulationConfig",
    "SimulationStatus",
    "ScenarioType",
    "WorkerTask",
    "WorkerStatus",
    "TimeUnit",
    # Core Engine
    "WorldEngine",
    "RuleExecutor",
    "create_simple_simulation",
    # Scenarios
    "ScenarioManager",
    "ScenarioComparison",
    "WhatIfAnalyzer",
    # Workers
    "Worker",
    "WorkerPool",
    "WorkerManager",
    # Temporal
    "TemporalIterator",
    "TemporalRange",
    "TemporalSchedule",
    "ScheduledEvent",
    "LongTermProjector",
    "convert_time_units",
    # Integration
    "IntegratedWorldEngine",
    "create_integrated_engine",
    "run_quick_simulation",
]
