"""
============================================================================
CHE·NU™ V69 — CAUSAL ENGINE
============================================================================
Version: 1.0.0
Purpose: Causal reasoning for decision intelligence
Principle: GOUVERNANCE > EXÉCUTION

CHE·NU™ transforms statistical simulations into causal recommendations.
It helps understand WHY and WHAT TO ACT ON, not just what might happen.

Core Principles:
1. AI analyzes, humans decide
2. All data is synthetic
3. Causal relationships are validated by humans
4. Every decision is auditable and signed

Usage:
    from causal_engine import DAGBuilder, CausalEngine, HumanDecisionBridge
    
    # Build a causal DAG
    dag = (DAGBuilder("Supply Chain")
        .add_slot_node("price", domain=[0, 100])
        .add_slot_node("demand", domain=[0, 1000])
        .add_outcome_node("revenue")
        .add_causal_edge("price", "demand", coefficient=-0.5)
        .add_causal_edge("demand", "revenue", coefficient=10.0)
        .build())
    
    # Analyze causally
    engine = CausalEngine(dag)
    effect = engine.estimate_effect("price", "revenue")
    levers = engine.get_key_levers("revenue")
    
    # Create decision package for human
    bridge = HumanDecisionBridge(engine)
    package = bridge.create_decision_package(
        title="Q4 Pricing Strategy",
        outcome_node="revenue",
        intervention_scenarios=[
            {"price": 80},
            {"price": 100},
        ],
    )
    
    # Human decides (CRITICAL!)
    record = bridge.record_decision(
        package_id=package.id,
        decider_id="user-123",
        selected_option_id="option-1",
        rationale="Best risk-reward balance",
    )
============================================================================
"""

# Core
from .core import (
    # Enums
    NodeType,
    EdgeType,
    ConfidenceLevel,
    InterventionType,
    ValidationStatus,
    # Models
    CausalNode,
    CausalEdge,
    CausalDAG,
    Intervention,
    CausalQuery,
    CausalEffect,
    SensitivityScore,
    CounterfactualResult,
    DecisionRecommendation,
    # DAG
    DAGBuilder,
    DAGManager,
    StructureLearner,
    get_dag_manager,
    # Inference
    AdjustmentSetFinder,
    CausalEffectEstimator,
    SensitivityAnalyzer,
    CausalEngine,
)

# Counterfactual
from .counterfactual import (
    CounterfactualEngine,
    ScenarioComparator,
)

# Bridge
from .bridge import (
    DecisionStatus,
    DecisionRecord,
    DecisionOption,
    DecisionPackage,
    HumanDecisionBridge,
)

# API
from .api import router as causal_router

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Enums
    "NodeType",
    "EdgeType",
    "ConfidenceLevel",
    "InterventionType",
    "ValidationStatus",
    # Models
    "CausalNode",
    "CausalEdge",
    "CausalDAG",
    "Intervention",
    "CausalQuery",
    "CausalEffect",
    "SensitivityScore",
    "CounterfactualResult",
    "DecisionRecommendation",
    # DAG
    "DAGBuilder",
    "DAGManager",
    "StructureLearner",
    "get_dag_manager",
    # Inference
    "AdjustmentSetFinder",
    "CausalEffectEstimator",
    "SensitivityAnalyzer",
    "CausalEngine",
    # Counterfactual
    "CounterfactualEngine",
    "ScenarioComparator",
    # Bridge
    "DecisionStatus",
    "DecisionRecord",
    "DecisionOption",
    "DecisionPackage",
    "HumanDecisionBridge",
    # API
    "causal_router",
]
