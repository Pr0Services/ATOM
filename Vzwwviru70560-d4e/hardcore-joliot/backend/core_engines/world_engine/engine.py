"""
============================================================================
CHE·NU™ V69 — WORLDENGINE CORE
============================================================================
Spec: GPT1/CHE-NU_WORLDENGINE_CORE_V1.md

Vision: Le WorldEngine est le cœur déterministe de CHE·NU™.
Il transforme des Slots en Artifacts certifiés, avec causalité explicite.

Objectives:
- Zéro hallucination (causalité explicite)
- Reproductibilité scientifique
- Scalabilité industrielle

Cycle: Snapshot → Propagation Causale → Résolution Conflits → Artifact
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import copy

from ..models import (
    Slot,
    Artifact,
    WorldState,
    CausalDAG,
    CausalEdge,
    FeedbackLoop,
    FeedbackType,
    generate_id,
    compute_hash,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CAUSAL RULES
# ============================================================================

@dataclass
class CausalRule:
    """A causal rule for propagation"""
    rule_id: str
    name: str
    
    # Input/output slots
    input_slots: List[str]
    output_slot: str
    
    # Function
    function: Callable[[Dict[str, float]], float] = None
    formula: str = ""
    
    # OPA
    opa_validated: bool = True


# ============================================================================
# WORKER
# ============================================================================

class Worker:
    """
    An isolated worker for deterministic execution.
    
    Per spec: Chaque Worker s'exécute isolé (Docker/WASM)
    """
    
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self._rules: Dict[str, CausalRule] = {}
    
    def register_rule(self, rule: CausalRule) -> None:
        """Register a causal rule"""
        self._rules[rule.rule_id] = rule
    
    def execute(
        self,
        rule_id: str,
        inputs: Dict[str, float],
    ) -> float:
        """Execute a causal rule"""
        rule = self._rules.get(rule_id)
        if not rule:
            raise ValueError(f"Rule {rule_id} not found")
        
        if rule.function:
            return rule.function(inputs)
        
        # Default: sum inputs
        return sum(inputs.values())


# ============================================================================
# WORLDENGINE CORE
# ============================================================================

class WorldEngineCore:
    """
    The deterministic core of CHE·NU™.
    
    Per spec: Moteur de réalité déterministe gouvernée
    """
    
    def __init__(self):
        self._workers: Dict[str, Worker] = {}
        self._states: Dict[str, WorldState] = {}
        self._artifacts: Dict[str, Artifact] = {}
        self._dags: Dict[str, CausalDAG] = {}
        self._feedback_loops: Dict[str, FeedbackLoop] = {}
        
        # Default worker
        self._default_worker = Worker("default")
        self._register_default_rules()
    
    def _register_default_rules(self) -> None:
        """Register default causal rules"""
        # Production rule
        self._default_worker.register_rule(CausalRule(
            rule_id="production",
            name="Production = Budget × Efficiency",
            input_slots=["budget", "efficiency"],
            output_slot="production",
            function=lambda x: x.get("budget", 0) * x.get("efficiency", 1),
            formula="production = budget * efficiency",
        ))
        
        # Growth rule
        self._default_worker.register_rule(CausalRule(
            rule_id="growth",
            name="Growth = Base × (1 + Rate)",
            input_slots=["base", "rate"],
            output_slot="growth",
            function=lambda x: x.get("base", 0) * (1 + x.get("rate", 0)),
            formula="growth = base * (1 + rate)",
        ))
        
        # Feedback rule
        self._default_worker.register_rule(CausalRule(
            rule_id="feedback",
            name="Next = Current × (1 - Depletion) + Input × Reinvest",
            input_slots=["current", "depletion", "input", "reinvest"],
            output_slot="next",
            function=lambda x: (
                x.get("current", 0) * (1 - x.get("depletion", 0)) +
                x.get("input", 0) * x.get("reinvest", 0)
            ),
        ))
    
    def create_state(
        self,
        slots: Dict[str, float],
        dag_ref: str = "",
    ) -> WorldState:
        """
        Create a world state from slots.
        
        Per spec input: WorldState.json
        """
        state = WorldState(
            state_id=generate_id(),
            dag_ref=dag_ref,
        )
        
        for name, value in slots.items():
            state.slots[name] = Slot(
                slot_id=generate_id(),
                name=name,
                value=value,
            )
        
        # Sign state
        state.signature = sign_artifact({
            "state_id": state.state_id,
            "slot_count": len(state.slots),
        }, "worldengine")
        
        self._states[state.state_id] = state
        return state
    
    def snapshot(self, state_id: str) -> WorldState:
        """
        Step 1: Capture immuable des Slots entrants.
        
        Per spec: Snapshot
        """
        state = self._states.get(state_id)
        if not state:
            raise ValueError(f"State {state_id} not found")
        
        # Deep copy for immutability
        snapshot = copy.deepcopy(state)
        snapshot.state_id = f"{state_id}_snapshot_{generate_id()[:8]}"
        
        logger.info(f"Snapshot created: {snapshot.state_id}")
        return snapshot
    
    def propagate(
        self,
        state: WorldState,
        rule_id: str,
        input_mapping: Dict[str, str],
        output_slot: str,
    ) -> WorldState:
        """
        Step 2: Propagation causale.
        
        Per spec: Application des fonctions f(x)
        """
        # Get input values
        inputs = {}
        for param_name, slot_name in input_mapping.items():
            if slot_name in state.slots:
                inputs[param_name] = state.slots[slot_name].value
            else:
                inputs[param_name] = 0.0
        
        # Execute rule
        result = self._default_worker.execute(rule_id, inputs)
        
        # Update state
        if output_slot in state.slots:
            state.slots[output_slot].value = result
        else:
            state.slots[output_slot] = Slot(
                slot_id=generate_id(),
                name=output_slot,
                value=result,
            )
        
        state.sim_time += 1
        
        logger.info(f"Propagated {rule_id}: {inputs} → {output_slot}={result}")
        return state
    
    def resolve_conflicts(
        self,
        state: WorldState,
        conflicts: List[Tuple[str, float, float]],
    ) -> WorldState:
        """
        Step 3: Résolution de conflits.
        
        Per spec: Arbitrage L2-Orchestrator
        """
        for slot_name, value1, value2 in conflicts:
            # Default: average (in production: semantic priority)
            resolved = (value1 + value2) / 2
            
            if slot_name in state.slots:
                state.slots[slot_name].value = resolved
            
            logger.info(f"Resolved conflict {slot_name}: {value1}, {value2} → {resolved}")
        
        return state
    
    def generate_artifact(
        self,
        input_state: WorldState,
        output_state: WorldState,
        rule_id: str,
    ) -> Artifact:
        """
        Step 4: Génération d'Artifact.
        
        Per spec: Artifact JSON certifié, reproductible
        """
        artifact = Artifact(
            artifact_id=generate_id(),
            inputs=list(input_state.slots.values()),
            outputs=list(output_state.slots.values()),
            causal_rule_id=rule_id,
        )
        
        # Compute hash
        artifact.hash = compute_hash({
            "inputs": {s.name: s.value for s in artifact.inputs},
            "outputs": {s.name: s.value for s in artifact.outputs},
            "rule": rule_id,
        })
        
        # Sign with PQC (mock)
        artifact.signature = sign_artifact({
            "artifact_id": artifact.artifact_id,
            "hash": artifact.hash,
        }, "worldengine_pqc")
        
        self._artifacts[artifact.artifact_id] = artifact
        
        logger.info(f"Generated artifact {artifact.artifact_id}")
        return artifact
    
    def run_cycle(
        self,
        state_id: str,
        rule_id: str,
        input_mapping: Dict[str, str],
        output_slot: str,
    ) -> Tuple[WorldState, Artifact]:
        """
        Run complete deterministic cycle.
        
        Per spec: Snapshot → Propagation → Resolution → Artifact
        """
        # Step 1: Snapshot
        input_state = self.snapshot(state_id)
        
        # Step 2: Propagate
        output_state = copy.deepcopy(input_state)
        output_state = self.propagate(output_state, rule_id, input_mapping, output_slot)
        
        # Step 3: Conflicts (none in simple case)
        
        # Step 4: Artifact
        artifact = self.generate_artifact(input_state, output_state, rule_id)
        
        # Store new state
        self._states[output_state.state_id] = output_state
        
        return output_state, artifact
    
    def add_feedback_loop(self, loop: FeedbackLoop) -> None:
        """Add a feedback loop"""
        self._feedback_loops[loop.loop_id] = loop
    
    def run_feedback_cycle(
        self,
        state: WorldState,
        loop_id: str,
        iterations: int = 1,
    ) -> List[WorldState]:
        """
        Run feedback loop iterations.
        
        Per spec: Feedback Loops (Systèmes Vivants)
        """
        loop = self._feedback_loops.get(loop_id)
        if not loop:
            raise ValueError(f"Loop {loop_id} not found")
        
        states = [state]
        current = copy.deepcopy(state)
        
        for i in range(iterations):
            # Apply feedback
            if loop.feedback_type == FeedbackType.POSITIVE:
                # Exponential growth
                for slot_name in loop.slot_chain:
                    if slot_name in current.slots:
                        current.slots[slot_name].value *= loop.gain
            else:
                # Negative: stabilization with damping
                for slot_name in loop.slot_chain:
                    if slot_name in current.slots:
                        target = loop.safety_threshold
                        current.slots[slot_name].value += (
                            (target - current.slots[slot_name].value) * loop.damping
                        )
            
            current.sim_time += 1
            states.append(copy.deepcopy(current))
            
            # Safety check
            for slot_name in loop.slot_chain:
                if slot_name in current.slots:
                    if current.slots[slot_name].value > loop.safety_threshold * 10:
                        logger.warning(f"Safety threshold exceeded for {slot_name}")
                        break
        
        return states
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID"""
        return self._artifacts.get(artifact_id)
    
    def verify_artifact(self, artifact: Artifact) -> bool:
        """Verify artifact integrity"""
        expected_hash = compute_hash({
            "inputs": {s.name: s.value for s in artifact.inputs},
            "outputs": {s.name: s.value for s in artifact.outputs},
            "rule": artifact.causal_rule_id,
        })
        return artifact.hash == expected_hash


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_engine() -> WorldEngineCore:
    """Create WorldEngine core"""
    return WorldEngineCore()


def create_feedback_loop(
    name: str,
    feedback_type: FeedbackType,
    slots: List[str],
    gain: float = 1.1,
    damping: float = 0.1,
) -> FeedbackLoop:
    """Create feedback loop"""
    return FeedbackLoop(
        loop_id=generate_id(),
        name=name,
        feedback_type=feedback_type,
        slot_chain=slots,
        gain=gain,
        damping=damping,
    )
