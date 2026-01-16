"""
============================================================================
CHE·NU™ V69 — FEEDBACK ENGINE MODELS
============================================================================
Version: 1.0.0
Purpose: Models for feedback loops, slots, world state, and artifacts
Principle: GOUVERNANCE > EXÉCUTION - Deterministic, auditable simulations
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib
import json


# ============================================================================
# ENUMS
# ============================================================================

class LoopType(str, Enum):
    """Types of feedback loops"""
    POSITIVE = "positive"      # Auto-reinforcing (exponential growth)
    NEGATIVE = "negative"      # Stabilizing (convergence to equilibrium)
    MIXED = "mixed"            # Combination


class FeedbackModel(str, Enum):
    """Supported feedback models"""
    LINEAR = "linear"          # X_{t+1} = A*X_t + B*U_t + c
    LOGISTIC = "logistic"      # X_{t+1} = X_t + r*X_t*(1 - X_t/K)
    STOCK_FLOW = "stock_flow"  # Accumulator with inflow/outflow
    DELAY = "delay"            # With latency/queue
    SHOCK = "shock"            # With deterministic shocks


class SafetyAction(str, Enum):
    """Actions taken by L2-Safety Controller"""
    NONE = "none"
    CLAMP = "clamp"            # Bound to min/max
    DAMPING = "damping"        # Apply damping factor
    BRAKE = "brake"            # Semantic brake
    ALERT = "alert"            # Warning only
    STOP = "stop"              # Hard stop


class StabilityStatus(str, Enum):
    """Stability assessment"""
    STABLE = "stable"
    CONVERGING = "converging"
    OSCILLATING = "oscillating"
    DIVERGING = "diverging"
    EXPLODING = "exploding"
    COLLAPSING = "collapsing"


# ============================================================================
# SLOT (Core data unit)
# ============================================================================

class Slot(BaseModel):
    """
    Core data unit in CHE·NU™ WorldEngine.
    Typed, measured, versioned, with provenance.
    """
    
    slot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Slot name")
    
    # Value
    value: float = Field(..., description="Current value")
    unit: str = Field(default="", description="Unit (EUR, %, units, etc.)")
    
    # Confidence & provenance
    confidence: float = Field(default=1.0, ge=0, le=1)
    provenance: str = Field(default="system", description="Source: agent/worker/user")
    
    # Constraints
    min_value: Optional[float] = Field(default=None)
    max_value: Optional[float] = Field(default=None)
    
    # Metadata
    description: Optional[str] = Field(default=None)
    sphere: Optional[str] = Field(default=None)
    
    # Temporal
    timestamp_sim: int = Field(default=0, description="Simulation tick T")
    
    # History (for delta calculation)
    previous_value: Optional[float] = Field(default=None)
    
    @computed_field
    @property
    def delta(self) -> Optional[float]:
        """Change from previous value"""
        if self.previous_value is not None:
            return self.value - self.previous_value
        return None
    
    @computed_field
    @property
    def growth_ratio(self) -> Optional[float]:
        """Growth ratio from previous value"""
        if self.previous_value is not None and self.previous_value != 0:
            return self.value / self.previous_value
        return None
    
    def apply_clamp(self) -> bool:
        """Apply min/max bounds, return True if clamped"""
        clamped = False
        if self.min_value is not None and self.value < self.min_value:
            self.value = self.min_value
            clamped = True
        if self.max_value is not None and self.value > self.max_value:
            self.value = self.max_value
            clamped = True
        return clamped
    
    def advance(self, new_value: float, new_tick: int) -> "Slot":
        """Create new slot with advanced value"""
        return Slot(
            slot_id=self.slot_id,
            name=self.name,
            value=new_value,
            unit=self.unit,
            confidence=self.confidence,
            provenance=self.provenance,
            min_value=self.min_value,
            max_value=self.max_value,
            description=self.description,
            sphere=self.sphere,
            timestamp_sim=new_tick,
            previous_value=self.value,
        )


# ============================================================================
# WORLD STATE
# ============================================================================

class WorldState(BaseModel):
    """
    Complete snapshot of all slots at simulation time T.
    Immutable once created.
    """
    
    state_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tick: int = Field(..., description="Simulation time T")
    
    # Slots
    slots: Dict[str, Slot] = Field(default_factory=dict)
    
    # Metadata
    simulation_id: str = Field(default="")
    tenant_id: Optional[str] = Field(default=None)
    
    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    previous_state_hash: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)
    
    @computed_field
    @property
    def hash(self) -> str:
        """Compute state hash for integrity"""
        content = {
            "tick": self.tick,
            "slots": {k: v.value for k, v in sorted(self.slots.items())},
        }
        return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    
    def get_slot(self, name: str) -> Optional[Slot]:
        """Get slot by name"""
        return self.slots.get(name)
    
    def get_value(self, name: str, default: float = 0.0) -> float:
        """Get slot value by name"""
        slot = self.slots.get(name)
        return slot.value if slot else default
    
    def set_slot(self, slot: Slot) -> None:
        """Set a slot (for building state)"""
        self.slots[slot.name] = slot
    
    def clone_for_next_tick(self) -> "WorldState":
        """Create a new state for T+1"""
        return WorldState(
            tick=self.tick + 1,
            simulation_id=self.simulation_id,
            tenant_id=self.tenant_id,
            previous_state_hash=self.hash,
            synthetic=True,
        )


# ============================================================================
# FEEDBACK EDGE
# ============================================================================

class FeedbackEdge(BaseModel):
    """
    Defines how output becomes input for next cycle.
    e.g., Budget(T+1) <- Budget(T) + reinvestment_rate * Production(T)
    """
    
    edge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    
    # Source and target slots
    target_slot: str = Field(..., description="Slot to update (e.g., Budget)")
    source_slots: List[str] = Field(..., description="Input slots")
    
    # Loop type
    loop_type: LoopType = Field(default=LoopType.POSITIVE)
    
    # Parameters
    coefficients: Dict[str, float] = Field(
        default_factory=dict,
        description="Coefficients for each source slot"
    )
    constant: float = Field(default=0.0, description="Constant term")
    
    # Model type
    model: FeedbackModel = Field(default=FeedbackModel.LINEAR)
    
    # For logistic model
    carrying_capacity: Optional[float] = Field(default=None, description="K for logistic")
    growth_rate: Optional[float] = Field(default=None, description="r for logistic")
    
    # For delay model
    delay_ticks: int = Field(default=0)
    
    # Governance
    opa_policy_ref: Optional[str] = Field(default=None)
    requires_approval: bool = Field(default=False)
    
    def compute_next_value(
        self,
        current_state: WorldState,
        history: Optional[List[WorldState]] = None,
    ) -> float:
        """Compute the next value for target slot"""
        current_value = current_state.get_value(self.target_slot)
        
        if self.model == FeedbackModel.LINEAR:
            return self._compute_linear(current_state, current_value)
        elif self.model == FeedbackModel.LOGISTIC:
            return self._compute_logistic(current_value)
        elif self.model == FeedbackModel.STOCK_FLOW:
            return self._compute_stock_flow(current_state, current_value)
        elif self.model == FeedbackModel.DELAY:
            return self._compute_delay(current_state, current_value, history)
        else:
            return current_value
    
    def _compute_linear(self, state: WorldState, current: float) -> float:
        """X_{t+1} = sum(coef_i * source_i) + constant"""
        result = self.constant
        for source_name, coef in self.coefficients.items():
            source_value = state.get_value(source_name, 0)
            result += coef * source_value
        return result
    
    def _compute_logistic(self, current: float) -> float:
        """X_{t+1} = X_t + r*X_t*(1 - X_t/K)"""
        if self.carrying_capacity is None or self.growth_rate is None:
            return current
        
        K = self.carrying_capacity
        r = self.growth_rate
        
        if K == 0:
            return current
        
        return current + r * current * (1 - current / K)
    
    def _compute_stock_flow(self, state: WorldState, current: float) -> float:
        """Stock = Stock + Inflow - Outflow"""
        inflow = sum(
            state.get_value(src) * coef
            for src, coef in self.coefficients.items()
            if coef > 0
        )
        outflow = sum(
            state.get_value(src) * abs(coef)
            for src, coef in self.coefficients.items()
            if coef < 0
        )
        return current + inflow - outflow
    
    def _compute_delay(
        self,
        state: WorldState,
        current: float,
        history: Optional[List[WorldState]],
    ) -> float:
        """With delay from history"""
        if not history or self.delay_ticks <= 0:
            return self._compute_linear(state, current)
        
        # Get delayed state
        delay_idx = max(0, len(history) - self.delay_ticks)
        delayed_state = history[delay_idx] if delay_idx < len(history) else state
        
        return self._compute_linear(delayed_state, current)


# ============================================================================
# TRANSFER FUNCTION (Causal Rule)
# ============================================================================

class TransferFunction(BaseModel):
    """
    Deterministic function that transforms slots.
    e.g., Production = Budget * Efficiency
    """
    
    function_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    
    # Output
    output_slot: str = Field(..., description="Slot to write result")
    
    # Input slots
    input_slots: List[str] = Field(...)
    
    # Function definition (expression string or coefficients)
    expression: Optional[str] = Field(default=None, description="e.g., 'Budget * Efficiency'")
    coefficients: Dict[str, float] = Field(default_factory=dict)
    constant: float = Field(default=0.0)
    
    # Execution order (lower = earlier)
    priority: int = Field(default=100)
    
    # Governance
    rule_confidence: float = Field(default=1.0, ge=0, le=1)
    opa_policy_ref: Optional[str] = Field(default=None)
    
    def compute(self, state: WorldState) -> float:
        """Compute output value"""
        # Simple linear combination
        result = self.constant
        for input_name, coef in self.coefficients.items():
            input_value = state.get_value(input_name, 0)
            result += coef * input_value
        return result


# ============================================================================
# FEEDBACK PARAMS
# ============================================================================

class FeedbackParams(BaseModel):
    """Parameters governing feedback behavior"""
    
    # Core rates
    reinvestment_rate: float = Field(default=0.1, ge=0, le=1)
    depletion_rate: float = Field(default=0.05, ge=0, le=1)
    
    # Safety bounds
    clamp_min: float = Field(default=0)
    clamp_max: float = Field(default=1e9)
    
    # Stability thresholds
    max_growth_ratio: float = Field(default=1.35, description="Explosion threshold")
    min_value_floor: float = Field(default=0, description="Collapse floor")
    oscillation_threshold: float = Field(default=3, description="Max sign changes")
    
    # Damping
    damping_factor: float = Field(default=0.8, ge=0, le=1)
    
    # Simulation
    tick_size: str = Field(default="day", description="Time unit per tick")
    
    # Determinism
    seed: Optional[int] = Field(default=None, description="Random seed for shocks")


# ============================================================================
# SIMULATION ARTIFACT
# ============================================================================

class SimulationArtifact(BaseModel):
    """
    Signed artifact produced by each simulation cycle.
    Forms an immutable audit chain.
    """
    
    artifact_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Temporal
    t_from: int = Field(..., description="Start tick")
    t_to: int = Field(..., description="End tick")
    
    # State hashes
    inputs_hash: str = Field(..., description="Hash of WorldState(T)")
    outputs_hash: str = Field(..., description="Hash of WorldState(T+1)")
    
    # Chain
    previous_artifact_hash: Optional[str] = Field(default=None)
    
    # Rules applied
    rules_applied: List[str] = Field(default_factory=list)
    feedback_edges_applied: List[str] = Field(default_factory=list)
    
    # Governance
    opa_decision_id: Optional[str] = Field(default=None)
    opa_allowed: bool = Field(default=True)
    
    # Safety
    safety_actions: List[Dict[str, Any]] = Field(default_factory=list)
    stability_status: StabilityStatus = Field(default=StabilityStatus.STABLE)
    
    # Telemetry
    telemetry: Dict[str, Any] = Field(default_factory=dict)
    
    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    simulation_id: str = Field(default="")
    tenant_id: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)
    
    # Signature
    signature: Optional[str] = Field(default=None)
    signature_algorithm: str = Field(default="sha256")
    
    @computed_field
    @property
    def hash(self) -> str:
        """Compute artifact hash"""
        content = {
            "artifact_id": self.artifact_id,
            "t_from": self.t_from,
            "t_to": self.t_to,
            "inputs_hash": self.inputs_hash,
            "outputs_hash": self.outputs_hash,
            "previous_artifact_hash": self.previous_artifact_hash,
            "rules_applied": sorted(self.rules_applied),
            "feedback_edges_applied": sorted(self.feedback_edges_applied),
            "safety_actions": self.safety_actions,
        }
        return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    
    def sign(self, secret_key: str = "mock-key") -> str:
        """Sign the artifact"""
        payload = self.hash
        signature = hashlib.sha256(f"{payload}{secret_key}".encode()).hexdigest()
        self.signature = signature
        return signature
    
    def verify(self, secret_key: str = "mock-key") -> bool:
        """Verify signature"""
        if not self.signature:
            return False
        expected = hashlib.sha256(f"{self.hash}{secret_key}".encode()).hexdigest()
        return self.signature == expected


# ============================================================================
# SIMULATION CONFIG
# ============================================================================

class SimulationConfig(BaseModel):
    """Configuration for a feedback simulation run"""
    
    simulation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="Simulation")
    
    # Temporal
    t_start: int = Field(default=0)
    t_end: int = Field(default=10)
    tick_size: str = Field(default="day")
    
    # Initial state
    initial_slots: List[Slot] = Field(default_factory=list)
    
    # Rules
    transfer_functions: List[TransferFunction] = Field(default_factory=list)
    feedback_edges: List[FeedbackEdge] = Field(default_factory=list)
    
    # Parameters
    params: FeedbackParams = Field(default_factory=FeedbackParams)
    
    # Governance
    tenant_id: Optional[str] = Field(default=None)
    opa_policy_refs: List[str] = Field(default_factory=list)
    
    # Audit
    synthetic: bool = Field(default=True)
    seed: Optional[int] = Field(default=None)
