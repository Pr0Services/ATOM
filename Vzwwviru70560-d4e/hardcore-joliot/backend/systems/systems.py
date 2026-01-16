"""
============================================================================
CHE·NU™ V69 — SYSTEMS MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_CORE_FEEDBACK_ALGORITHMS.md
- CHE-NU_HUMAN_DECISION_BRIDGE.md
- CHE-NU_SIMULATION_FIDELITY_MONITORING.md
- CHE-NU_SYNTHETIC_DATA_SCALING.md

Principle: GOUVERNANCE > EXÉCUTION
"CHE·NU never decides. Humans always decide."
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid
import hashlib
import json
import copy
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    return str(uuid.uuid4())

def compute_hash(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def sign_artifact(data: Dict[str, Any], signer: str) -> str:
    return compute_hash(f"{json.dumps(data, sort_keys=True, default=str)}:{signer}")


# ============================================================================
# 1. FEEDBACK ALGORITHMS (CORE_FEEDBACK_ALGORITHMS.md)
# ============================================================================

class FeedbackType(str, Enum):
    """Types of feedback loops"""
    POSITIVE = "positive"  # Auto-renforcement
    NEGATIVE = "negative"  # Stabilisation


class SafetyAction(str, Enum):
    """L2-Safety Controller actions"""
    CLAMP = "clamp"
    DAMPING = "damping"
    SEMANTIC_BRAKE = "semantic_brake"
    ALERT = "alert"
    HARD_STOP = "hard_stop"


@dataclass
class FeedbackParams:
    """
    Feedback parameters.
    
    Per spec: reinvestment_rate, depletion_rate, clamps
    """
    reinvestment_rate: float = 0.1
    depletion_rate: float = 0.05
    clamp_min: float = 0.0
    clamp_max: float = 10_000_000.0
    growth_max: float = 1.35  # Max growth ratio


@dataclass
class FeedbackArtifact:
    """
    Artifact from feedback cycle.
    
    Per spec: artifact_id, t_from, t_to, hashes, rules, safety_actions, signature
    """
    artifact_id: str
    t_from: int
    t_to: int
    inputs_hash: str
    outputs_hash: str
    rules_applied: List[str] = field(default_factory=list)
    feedback_edges: List[str] = field(default_factory=list)
    safety_actions: List[str] = field(default_factory=list)
    prev_hash: str = ""
    signature: str = ""


class L2SafetyController:
    """
    Safety controller for stability.
    
    Per spec: L2-Safety Controller - surveille stabilité, applique freins
    """
    
    def __init__(self, params: FeedbackParams):
        self.params = params
        self._history: List[float] = []
    
    def check(self, prev_value: float, next_value: float) -> Tuple[float, List[SafetyAction]]:
        """Check and apply safety measures"""
        actions = []
        
        # Growth ratio check
        if prev_value > 0:
            growth = next_value / prev_value
            if growth > self.params.growth_max:
                actions.append(SafetyAction.DAMPING)
                next_value = prev_value * self.params.growth_max
        
        # Clamp check
        if next_value < self.params.clamp_min:
            actions.append(SafetyAction.CLAMP)
            next_value = self.params.clamp_min
        elif next_value > self.params.clamp_max:
            actions.append(SafetyAction.CLAMP)
            next_value = self.params.clamp_max
        
        # Oscillation check
        self._history.append(next_value)
        if len(self._history) > 3:
            deltas = [self._history[i] - self._history[i-1] for i in range(-3, 0)]
            if all(d * deltas[0] < 0 for d in deltas[1:]):  # Alternating signs
                actions.append(SafetyAction.ALERT)
        
        return next_value, actions


class FeedbackEngine:
    """
    Core Feedback Engine.
    
    Per spec: Transformer un calcul causal statique en simulation dynamique
    """
    
    def __init__(self, params: FeedbackParams = None):
        self.params = params or FeedbackParams()
        self.safety = L2SafetyController(self.params)
        self._artifacts: List[FeedbackArtifact] = []
    
    def simulate_cycle(
        self,
        budget: float,
        efficiency: float = 0.85,
    ) -> Tuple[float, float, List[SafetyAction]]:
        """
        Simulate one feedback cycle.
        
        Per spec pattern: Production = Budget * Efficiency
        Budget(T+1) = Budget(T)*(1-d) + Production(T)*r
        """
        # Compute outputs at T
        production = budget * efficiency
        
        # Feedback update -> T+1
        next_budget = (
            budget * (1.0 - self.params.depletion_rate) +
            production * self.params.reinvestment_rate
        )
        
        # Safety check
        next_budget, actions = self.safety.check(budget, next_budget)
        
        return production, next_budget, actions
    
    def run_simulation(
        self,
        initial_budget: float,
        cycles: int = 10,
        efficiency: float = 0.85,
    ) -> List[FeedbackArtifact]:
        """Run multi-cycle simulation"""
        self._artifacts = []
        budget = initial_budget
        prev_hash = "genesis"
        
        for t in range(cycles):
            # Snapshot inputs
            inputs = {"budget": budget, "efficiency": efficiency, "t": t}
            inputs_hash = compute_hash(inputs)
            
            # Compute
            production, next_budget, actions = self.simulate_cycle(budget, efficiency)
            
            # Snapshot outputs
            outputs = {"budget": next_budget, "production": production, "t": t + 1}
            outputs_hash = compute_hash(outputs)
            
            # Create artifact
            artifact = FeedbackArtifact(
                artifact_id=generate_id(),
                t_from=t,
                t_to=t + 1,
                inputs_hash=inputs_hash,
                outputs_hash=outputs_hash,
                rules_applied=["production", "feedback_update"],
                feedback_edges=["budget->production->budget"],
                safety_actions=[a.value for a in actions],
                prev_hash=prev_hash,
            )
            artifact.signature = sign_artifact({
                "id": artifact.artifact_id,
                "t": t,
                "inputs": inputs_hash,
                "outputs": outputs_hash,
            }, "feedback_engine")
            
            self._artifacts.append(artifact)
            prev_hash = compute_hash(artifact.artifact_id)
            budget = next_budget
        
        logger.info(f"Ran {cycles} feedback cycles, final budget={budget:.2f}")
        return self._artifacts


# ============================================================================
# 2. HUMAN DECISION BRIDGE (HUMAN_DECISION_BRIDGE.md)
# ============================================================================

@dataclass
class DecisionScenario:
    """A scenario for human decision"""
    scenario_id: str
    name: str
    description: str
    kpis: Dict[str, float] = field(default_factory=dict)
    risks: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class HumanDecision:
    """
    A human decision record.
    
    Per spec: Human signature required, Immutable decision record
    """
    decision_id: str
    selected_scenario: str
    rationale: str
    
    # Human signature
    decider_id: str
    decided_at: datetime = field(default_factory=datetime.utcnow)
    signature: str = ""
    
    # Audit
    opa_validated: bool = False


class HumanDecisionBridge:
    """
    Bridge between machine assistance and human decision.
    
    Per spec principle: CHE·NU never decides. Humans always decide.
    """
    
    def __init__(self):
        self._scenarios: Dict[str, DecisionScenario] = {}
        self._decisions: List[HumanDecision] = []
    
    def add_scenario(self, scenario: DecisionScenario) -> None:
        """Add a scenario for comparison"""
        self._scenarios[scenario.scenario_id] = scenario
    
    def generate_comparison(self) -> Dict[str, Any]:
        """
        Generate scenario comparison report.
        
        Per spec output: Scenario Comparison Report
        """
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "scenario_count": len(self._scenarios),
            "scenarios": [
                {
                    "id": s.scenario_id,
                    "name": s.name,
                    "kpis": s.kpis,
                    "risks": s.risks,
                    "confidence": s.confidence,
                }
                for s in self._scenarios.values()
            ],
            "note": "Human decision required",
        }
    
    def record_decision(
        self,
        scenario_id: str,
        decider_id: str,
        rationale: str,
    ) -> HumanDecision:
        """
        Record human decision.
        
        Per spec: Human signature required
        """
        if scenario_id not in self._scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        decision = HumanDecision(
            decision_id=generate_id(),
            selected_scenario=scenario_id,
            rationale=rationale,
            decider_id=decider_id,
            opa_validated=True,
        )
        
        # Sign decision
        decision.signature = sign_artifact({
            "decision_id": decision.decision_id,
            "scenario": scenario_id,
            "decider": decider_id,
            "time": decision.decided_at.isoformat(),
        }, decider_id)
        
        self._decisions.append(decision)
        logger.info(f"Decision recorded: {scenario_id} by {decider_id}")
        return decision
    
    def generate_summary_pdf_data(
        self,
        decision: HumanDecision,
    ) -> Dict[str, Any]:
        """
        Generate Decision Summary PDF data.
        
        Per spec output: Decision Summary PDF (signed)
        """
        scenario = self._scenarios.get(decision.selected_scenario)
        
        return {
            "title": "CHE·NU Decision Summary",
            "decision_id": decision.decision_id,
            "selected_scenario": {
                "name": scenario.name if scenario else "Unknown",
                "kpis": scenario.kpis if scenario else {},
            },
            "rationale": decision.rationale,
            "decider": decision.decider_id,
            "timestamp": decision.decided_at.isoformat(),
            "signature": decision.signature,
            "legal_notice": "This decision was made by a human. CHE·NU provided analysis only.",
        }


# ============================================================================
# 3. SIMULATION FIDELITY MONITORING (SIMULATION_FIDELITY_MONITORING.md)
# ============================================================================

class DriftType(str, Enum):
    """Types of drift"""
    PARAMETER = "parameter"
    STRUCTURAL = "structural"
    ASSUMPTION = "assumption"


@dataclass
class DriftAlert:
    """
    A drift alert.
    
    Per spec: Drift alerts (non-blocking)
    """
    alert_id: str
    drift_type: DriftType
    slot_id: str
    expected_value: float
    actual_value: float
    delta_percent: float
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CalibrationRecord:
    """
    Calibration record.
    
    Per spec: Human-approved parameter updates
    """
    record_id: str
    parameter: str
    old_value: float
    new_value: float
    approved_by: str
    approved_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1


class FidelityMonitor:
    """
    Monitor simulation fidelity.
    
    Per spec: Ensure simulations remain representative of reality
    """
    
    def __init__(self, drift_threshold: float = 0.1):
        self.drift_threshold = drift_threshold
        self._alerts: List[DriftAlert] = []
        self._calibrations: List[CalibrationRecord] = []
        self._confidence_scores: Dict[str, float] = {}
    
    def check_drift(
        self,
        slot_id: str,
        simulated: float,
        actual: float,
    ) -> Optional[DriftAlert]:
        """
        Check for drift.
        
        Per spec: Signal deltas vs real KPIs
        """
        if actual == 0:
            delta_percent = abs(simulated) * 100
        else:
            delta_percent = abs(simulated - actual) / abs(actual) * 100
        
        if delta_percent > self.drift_threshold * 100:
            alert = DriftAlert(
                alert_id=generate_id(),
                drift_type=DriftType.PARAMETER,
                slot_id=slot_id,
                expected_value=simulated,
                actual_value=actual,
                delta_percent=delta_percent,
            )
            self._alerts.append(alert)
            
            # Update confidence
            self._confidence_scores[slot_id] = max(
                0.0,
                self._confidence_scores.get(slot_id, 1.0) - 0.1
            )
            
            logger.warning(f"Drift alert: {slot_id} delta={delta_percent:.1f}%")
            return alert
        
        return None
    
    def calibrate(
        self,
        parameter: str,
        old_value: float,
        new_value: float,
        approver_id: str,
    ) -> CalibrationRecord:
        """
        Record calibration.
        
        Per spec: Human-approved parameter updates
        """
        version = len([c for c in self._calibrations if c.parameter == parameter]) + 1
        
        record = CalibrationRecord(
            record_id=generate_id(),
            parameter=parameter,
            old_value=old_value,
            new_value=new_value,
            approved_by=approver_id,
            version=version,
        )
        
        self._calibrations.append(record)
        logger.info(f"Calibration: {parameter} v{version} by {approver_id}")
        return record
    
    def get_confidence(self, slot_id: str) -> float:
        """Get confidence score for slot"""
        return self._confidence_scores.get(slot_id, 1.0)
    
    def get_alerts(self) -> List[DriftAlert]:
        """Get all alerts"""
        return self._alerts


# ============================================================================
# 4. SYNTHETIC DATA SCALING (SYNTHETIC_DATA_SCALING.md)
# ============================================================================

class SyntheticGenerator:
    """
    Generate synthetic data.
    
    Per spec: Synthetic Data 2.0 - privacy-safe datasets including edge cases
    """
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        self._generated: List[Dict] = []
    
    def _deterministic_noise(self, base: float, index: int) -> float:
        """Deterministic pseudo-random noise"""
        h = hash((self.seed, index))
        return base * (1.0 + ((h % 1000) - 500) / 5000)
    
    def generate_scenario(
        self,
        base_values: Dict[str, float],
        variation_percent: float = 10.0,
    ) -> Dict[str, float]:
        """Generate a synthetic scenario"""
        scenario = {}
        for key, value in base_values.items():
            idx = len(self._generated) + hash(key)
            scenario[key] = self._deterministic_noise(value, idx)
        
        self._generated.append(scenario)
        return scenario
    
    def generate_edge_case(
        self,
        base_values: Dict[str, float],
        crisis_type: str = "supply_shock",
    ) -> Dict[str, float]:
        """
        Generate edge case scenario.
        
        Per spec: Edge-case amplification (crises, failures)
        """
        scenario = copy.deepcopy(base_values)
        
        crisis_factors = {
            "supply_shock": {"cost": 2.0, "inventory": 0.3},
            "demand_crash": {"revenue": 0.5, "orders": 0.4},
            "energy_spike": {"energy_cost": 3.0, "margin": 0.7},
            "regulation": {"compliance_cost": 2.5, "capacity": 0.8},
        }
        
        factors = crisis_factors.get(crisis_type, {})
        for key, factor in factors.items():
            if key in scenario:
                scenario[key] *= factor
        
        scenario["crisis_type"] = crisis_type
        scenario["synthetic"] = True
        
        self._generated.append(scenario)
        logger.info(f"Generated edge case: {crisis_type}")
        return scenario


class DigitalTwin:
    """
    Domain-specific digital twin.
    
    Per spec: Domain-specific digital twins
    """
    
    def __init__(self, domain: str):
        self.domain = domain
        self.twin_id = generate_id()
        self._state: Dict[str, float] = {}
        self._history: List[Dict] = []
    
    def initialize(self, initial_state: Dict[str, float]) -> None:
        """Initialize twin state"""
        self._state = copy.deepcopy(initial_state)
        self._state["synthetic"] = True
    
    def update(self, changes: Dict[str, float]) -> Dict[str, float]:
        """Update twin and record history"""
        self._history.append(copy.deepcopy(self._state))
        
        for key, value in changes.items():
            if key in self._state:
                self._state[key] = value
        
        return self._state
    
    def get_state(self) -> Dict[str, float]:
        """Get current state"""
        return copy.deepcopy(self._state)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Feedback
    "FeedbackType", "SafetyAction", "FeedbackParams",
    "FeedbackArtifact", "L2SafetyController", "FeedbackEngine",
    # Human Bridge
    "DecisionScenario", "HumanDecision", "HumanDecisionBridge",
    # Fidelity
    "DriftType", "DriftAlert", "CalibrationRecord", "FidelityMonitor",
    # Synthetic
    "SyntheticGenerator", "DigitalTwin",
    # Utils
    "generate_id", "compute_hash", "sign_artifact",
]
