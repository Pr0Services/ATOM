"""
============================================================================
CHE·NU™ V69 — FEEDBACK LOOP ENGINE
============================================================================
Version: 1.0.0
Purpose: Execute temporal feedback loops T -> T+1
Principle: GOUVERNANCE > EXÉCUTION - Deterministic, OPA-governed
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import hashlib
import json

from .models import (
    Slot,
    WorldState,
    FeedbackEdge,
    TransferFunction,
    FeedbackParams,
    SimulationArtifact,
    SimulationConfig,
    LoopType,
    FeedbackModel,
    SafetyAction,
    StabilityStatus,
)

logger = logging.getLogger(__name__)


# ============================================================================
# L2 SAFETY CONTROLLER
# ============================================================================

class L2SafetyController:
    """
    Monitors simulation stability and applies safety actions.
    
    Detects:
    - Explosion (runaway growth)
    - Collapse (below floor)
    - Oscillation (sign alternation)
    - Divergence (unbounded growth)
    
    Actions:
    - Clamp (bound values)
    - Damping (reduce change rate)
    - Brake (semantic intervention)
    - Alert (warning only)
    - Stop (halt simulation)
    """
    
    def __init__(self, params: FeedbackParams):
        self.params = params
        self.history: List[Dict[str, float]] = []
        self.sign_changes: Dict[str, int] = {}
    
    def analyze(
        self,
        prev_state: WorldState,
        next_state: WorldState,
    ) -> Tuple[StabilityStatus, List[Dict[str, Any]]]:
        """
        Analyze stability between states.
        Returns status and list of safety actions taken.
        """
        actions = []
        worst_status = StabilityStatus.STABLE
        
        for slot_name, slot in next_state.slots.items():
            prev_slot = prev_state.get_slot(slot_name)
            if prev_slot is None:
                continue
            
            status, slot_actions = self._analyze_slot(prev_slot, slot)
            actions.extend(slot_actions)
            
            # Track worst status
            if self._status_severity(status) > self._status_severity(worst_status):
                worst_status = status
        
        return worst_status, actions
    
    def _analyze_slot(
        self,
        prev: Slot,
        current: Slot,
    ) -> Tuple[StabilityStatus, List[Dict[str, Any]]]:
        """Analyze single slot stability"""
        actions = []
        status = StabilityStatus.STABLE
        
        delta = current.value - prev.value
        
        # Growth ratio check
        if prev.value != 0:
            growth = current.value / prev.value
            
            if growth > self.params.max_growth_ratio:
                status = StabilityStatus.EXPLODING
                actions.append({
                    "slot": current.name,
                    "action": SafetyAction.CLAMP.value,
                    "reason": f"Growth ratio {growth:.2f} > {self.params.max_growth_ratio}",
                    "value_before": current.value,
                    "value_after": prev.value * self.params.max_growth_ratio,
                })
                # Apply clamp
                current.value = prev.value * self.params.max_growth_ratio
            
            elif growth < 1 / self.params.max_growth_ratio:
                status = StabilityStatus.COLLAPSING
        
        # Floor check
        if current.value < self.params.min_value_floor:
            status = StabilityStatus.COLLAPSING
            actions.append({
                "slot": current.name,
                "action": SafetyAction.CLAMP.value,
                "reason": f"Value {current.value} < floor {self.params.min_value_floor}",
                "value_before": current.value,
                "value_after": self.params.min_value_floor,
            })
            current.value = self.params.min_value_floor
        
        # Oscillation check
        self._track_oscillation(current.name, delta)
        if self.sign_changes.get(current.name, 0) > self.params.oscillation_threshold:
            status = StabilityStatus.OSCILLATING
            actions.append({
                "slot": current.name,
                "action": SafetyAction.DAMPING.value,
                "reason": f"Oscillation detected ({self.sign_changes[current.name]} sign changes)",
            })
        
        # Apply slot bounds
        if current.apply_clamp():
            actions.append({
                "slot": current.name,
                "action": SafetyAction.CLAMP.value,
                "reason": "Slot bounds applied",
            })
        
        return status, actions
    
    def _track_oscillation(self, slot_name: str, delta: float) -> None:
        """Track sign changes for oscillation detection"""
        if slot_name not in self.sign_changes:
            self.sign_changes[slot_name] = 0
            self.history.append({slot_name: delta})
            return
        
        # Check if sign changed
        prev_deltas = [h.get(slot_name, 0) for h in self.history[-3:]]
        if prev_deltas and (delta * prev_deltas[-1] < 0):
            self.sign_changes[slot_name] += 1
        
        self.history.append({slot_name: delta})
    
    def _status_severity(self, status: StabilityStatus) -> int:
        """Get severity level of status"""
        severity = {
            StabilityStatus.STABLE: 0,
            StabilityStatus.CONVERGING: 1,
            StabilityStatus.OSCILLATING: 2,
            StabilityStatus.DIVERGING: 3,
            StabilityStatus.COLLAPSING: 4,
            StabilityStatus.EXPLODING: 5,
        }
        return severity.get(status, 0)
    
    def should_stop(self, status: StabilityStatus) -> bool:
        """Check if simulation should stop"""
        return status in [StabilityStatus.EXPLODING, StabilityStatus.COLLAPSING]


# ============================================================================
# FEEDBACK LOOP ENGINE
# ============================================================================

class FeedbackLoopEngine:
    """
    Core engine for temporal feedback simulation.
    
    Executes the canonical pipeline:
    1. Snapshot - Load and verify WorldState(T)
    2. OPA Pre-Check - Validate parameters
    3. Propagation - Apply transfer functions
    4. Feedback Update - Compute T+1 values
    5. Stability Monitor - L2 safety check
    6. Artifact Generation - Sign and chain
    
    Usage:
        engine = FeedbackLoopEngine(config)
        results = engine.run()
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.params = config.params
        self.safety = L2SafetyController(self.params)
        
        # State tracking
        self.states: List[WorldState] = []
        self.artifacts: List[SimulationArtifact] = []
        self.current_tick = config.t_start
        
        # Build initial state
        self._initialize_state()
    
    def _initialize_state(self) -> None:
        """Initialize WorldState from config"""
        state = WorldState(
            tick=self.config.t_start,
            simulation_id=self.config.simulation_id,
            tenant_id=self.config.tenant_id,
            synthetic=True,
        )
        
        for slot in self.config.initial_slots:
            slot.timestamp_sim = self.config.t_start
            state.set_slot(slot)
        
        self.states.append(state)
        logger.info(f"Initialized simulation {self.config.simulation_id} at T={self.config.t_start}")
    
    def run(self) -> Dict[str, Any]:
        """
        Run complete simulation from t_start to t_end.
        Returns summary with all states and artifacts.
        """
        logger.info(f"Starting simulation: {self.config.name}")
        
        while self.current_tick < self.config.t_end:
            result = self.step()
            
            if result.get("stopped"):
                logger.warning(f"Simulation stopped at T={self.current_tick}")
                break
            
            self.current_tick += 1
        
        return self._generate_summary()
    
    def step(self) -> Dict[str, Any]:
        """
        Execute single simulation cycle T -> T+1.
        Returns step result with artifact.
        """
        current_state = self.states[-1]
        t_from = current_state.tick
        t_to = t_from + 1
        
        logger.debug(f"Executing step T={t_from} -> T={t_to}")
        
        # 1. Snapshot (already have current_state)
        inputs_hash = current_state.hash
        
        # 2. OPA Pre-Check (mock - would call OPA in production)
        opa_result = self._opa_precheck(current_state)
        if not opa_result["allowed"]:
            return self._create_rejected_artifact(current_state, opa_result)
        
        # 3. Create next state
        next_state = current_state.clone_for_next_tick()
        
        # 4. Apply transfer functions
        rules_applied = self._apply_transfer_functions(current_state, next_state)
        
        # 5. Apply feedback edges
        feedback_applied = self._apply_feedback_edges(current_state, next_state)
        
        # 6. Stability monitor
        stability_status, safety_actions = self.safety.analyze(current_state, next_state)
        
        # 7. Check for stop condition
        should_stop = self.safety.should_stop(stability_status)
        
        # 8. Generate artifact
        artifact = SimulationArtifact(
            t_from=t_from,
            t_to=t_to,
            inputs_hash=inputs_hash,
            outputs_hash=next_state.hash,
            previous_artifact_hash=self.artifacts[-1].hash if self.artifacts else None,
            rules_applied=rules_applied,
            feedback_edges_applied=feedback_applied,
            opa_decision_id=opa_result.get("decision_id"),
            opa_allowed=True,
            safety_actions=safety_actions,
            stability_status=stability_status,
            telemetry=self._generate_telemetry(current_state, next_state),
            simulation_id=self.config.simulation_id,
            tenant_id=self.config.tenant_id,
            synthetic=True,
        )
        artifact.sign()
        
        # Store
        self.states.append(next_state)
        self.artifacts.append(artifact)
        
        logger.info(f"Step T={t_from}->T={t_to} complete. Status: {stability_status.value}")
        
        return {
            "t_from": t_from,
            "t_to": t_to,
            "artifact_id": artifact.artifact_id,
            "stability": stability_status.value,
            "safety_actions": len(safety_actions),
            "stopped": should_stop,
        }
    
    def _opa_precheck(self, state: WorldState) -> Dict[str, Any]:
        """
        OPA pre-execution check.
        In production, calls actual OPA service.
        """
        # Mock OPA check - always allow in simulation
        return {
            "allowed": True,
            "decision_id": f"opa-{state.state_id[:8]}",
            "synthetic": True,
        }
    
    def _apply_transfer_functions(
        self,
        current: WorldState,
        next_state: WorldState,
    ) -> List[str]:
        """Apply all transfer functions in priority order"""
        applied = []
        
        # Sort by priority
        functions = sorted(
            self.config.transfer_functions,
            key=lambda f: f.priority
        )
        
        for func in functions:
            try:
                output_value = func.compute(current)
                
                # Get or create output slot
                existing = current.get_slot(func.output_slot)
                if existing:
                    new_slot = existing.advance(output_value, next_state.tick)
                else:
                    new_slot = Slot(
                        name=func.output_slot,
                        value=output_value,
                        timestamp_sim=next_state.tick,
                    )
                
                next_state.set_slot(new_slot)
                applied.append(func.function_id)
                
            except Exception as e:
                logger.error(f"Transfer function {func.name} failed: {e}")
        
        return applied
    
    def _apply_feedback_edges(
        self,
        current: WorldState,
        next_state: WorldState,
    ) -> List[str]:
        """Apply all feedback edges to compute T+1 values"""
        applied = []
        
        for edge in self.config.feedback_edges:
            try:
                next_value = edge.compute_next_value(
                    current,
                    self.states if edge.delay_ticks > 0 else None
                )
                
                # Update or create slot
                existing = current.get_slot(edge.target_slot)
                if existing:
                    new_slot = existing.advance(next_value, next_state.tick)
                else:
                    new_slot = Slot(
                        name=edge.target_slot,
                        value=next_value,
                        timestamp_sim=next_state.tick,
                    )
                
                next_state.set_slot(new_slot)
                applied.append(edge.edge_id)
                
            except Exception as e:
                logger.error(f"Feedback edge {edge.name} failed: {e}")
        
        return applied
    
    def _generate_telemetry(
        self,
        prev: WorldState,
        current: WorldState,
    ) -> Dict[str, Any]:
        """Generate telemetry data for artifact"""
        telemetry = {
            "slot_count": len(current.slots),
            "deltas": {},
            "growth_ratios": {},
        }
        
        for name, slot in current.slots.items():
            if slot.delta is not None:
                telemetry["deltas"][name] = slot.delta
            if slot.growth_ratio is not None:
                telemetry["growth_ratios"][name] = slot.growth_ratio
        
        return telemetry
    
    def _create_rejected_artifact(
        self,
        state: WorldState,
        opa_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create artifact for OPA rejection"""
        artifact = SimulationArtifact(
            t_from=state.tick,
            t_to=state.tick,
            inputs_hash=state.hash,
            outputs_hash=state.hash,
            previous_artifact_hash=self.artifacts[-1].hash if self.artifacts else None,
            opa_decision_id=opa_result.get("decision_id"),
            opa_allowed=False,
            stability_status=StabilityStatus.STABLE,
            simulation_id=self.config.simulation_id,
            synthetic=True,
        )
        artifact.sign()
        self.artifacts.append(artifact)
        
        return {
            "t_from": state.tick,
            "t_to": state.tick,
            "artifact_id": artifact.artifact_id,
            "stopped": True,
            "reason": "OPA_REJECTED",
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate simulation summary"""
        final_state = self.states[-1]
        
        return {
            "simulation_id": self.config.simulation_id,
            "name": self.config.name,
            "t_start": self.config.t_start,
            "t_end": self.current_tick,
            "ticks_executed": len(self.artifacts),
            "final_state": {
                name: slot.value
                for name, slot in final_state.slots.items()
            },
            "artifacts": [a.artifact_id for a in self.artifacts],
            "artifact_chain_valid": self._verify_chain(),
            "synthetic": True,
            "completed_at": datetime.utcnow().isoformat(),
        }
    
    def _verify_chain(self) -> bool:
        """Verify artifact chain integrity"""
        for i, artifact in enumerate(self.artifacts):
            if not artifact.verify():
                return False
            
            if i > 0:
                expected_prev = self.artifacts[i - 1].hash
                if artifact.previous_artifact_hash != expected_prev:
                    return False
        
        return True
    
    def get_state_at(self, tick: int) -> Optional[WorldState]:
        """Get state at specific tick (for replay)"""
        for state in self.states:
            if state.tick == tick:
                return state
        return None
    
    def get_artifact_at(self, tick: int) -> Optional[SimulationArtifact]:
        """Get artifact for specific transition"""
        for artifact in self.artifacts:
            if artifact.t_from == tick:
                return artifact
        return None


# ============================================================================
# QUICK SIMULATION BUILDER
# ============================================================================

def create_simple_simulation(
    name: str,
    initial_values: Dict[str, float],
    feedback_rules: Dict[str, Dict[str, float]],
    transfer_rules: Optional[Dict[str, Dict[str, float]]] = None,
    num_ticks: int = 10,
    params: Optional[FeedbackParams] = None,
) -> FeedbackLoopEngine:
    """
    Quick helper to create a simple feedback simulation.
    
    Usage:
        engine = create_simple_simulation(
            name="Budget Model",
            initial_values={"Budget": 1000000, "Efficiency": 0.85},
            feedback_rules={
                "Budget": {"Budget": 0.95, "Production": 0.1}
            },
            transfer_rules={
                "Production": {"Budget": 0.85}
            },
            num_ticks=10,
        )
        results = engine.run()
    """
    # Create slots
    slots = [
        Slot(name=name, value=value)
        for name, value in initial_values.items()
    ]
    
    # Create transfer functions
    transfers = []
    if transfer_rules:
        for output, coeffs in transfer_rules.items():
            transfers.append(TransferFunction(
                name=f"compute_{output}",
                output_slot=output,
                input_slots=list(coeffs.keys()),
                coefficients=coeffs,
            ))
    
    # Create feedback edges
    edges = []
    for target, coeffs in feedback_rules.items():
        edges.append(FeedbackEdge(
            name=f"feedback_{target}",
            target_slot=target,
            source_slots=list(coeffs.keys()),
            coefficients=coeffs,
        ))
    
    # Create config
    config = SimulationConfig(
        name=name,
        t_start=0,
        t_end=num_ticks,
        initial_slots=slots,
        transfer_functions=transfers,
        feedback_edges=edges,
        params=params or FeedbackParams(),
    )
    
    return FeedbackLoopEngine(config)
