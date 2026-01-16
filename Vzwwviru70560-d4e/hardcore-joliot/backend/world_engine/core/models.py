"""
============================================================================
CHE·NU™ V69 — WORLDENGINE MODELS
============================================================================
Version: 1.0.0
Purpose: Core models for WorldEngine simulation orchestration
Principle: Deterministic, reproducible, governed simulations
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib
import json


# ============================================================================
# ENUMS
# ============================================================================

class SimulationStatus(str, Enum):
    """Simulation lifecycle status"""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScenarioType(str, Enum):
    """Scenario types"""
    BASELINE = "baseline"
    ALTERNATIVE = "alternative"
    COUNTERFACTUAL = "counterfactual"
    STRESS_TEST = "stress_test"
    MONTE_CARLO = "monte_carlo"


class WorkerStatus(str, Enum):
    """Worker status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class TimeUnit(str, Enum):
    """Time units for simulation"""
    TICK = "tick"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


# ============================================================================
# SLOT (Data Unit)
# ============================================================================

class Slot(BaseModel):
    """
    Slot = Atomic data unit in WorldEngine.
    
    A slot represents a single piece of data with:
    - Type and unit for semantic clarity
    - Confidence level for uncertainty
    - Provenance for traceability
    - Temporal tracking
    """
    
    slot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    value: float = Field(...)
    unit: str = Field(default="")
    
    # Metadata
    slot_type: str = Field(default="numeric")  # numeric, ratio, count, currency
    confidence: float = Field(default=1.0, ge=0, le=1)
    provenance: str = Field(default="input")
    
    # Constraints
    min_value: Optional[float] = Field(default=None)
    max_value: Optional[float] = Field(default=None)
    
    # Temporal
    timestamp_sim: float = Field(default=0)
    tick: int = Field(default=0)
    
    # Previous value for delta calculation
    previous_value: Optional[float] = Field(default=None)
    
    @computed_field
    @property
    def delta(self) -> float:
        """Change from previous value"""
        if self.previous_value is None:
            return 0.0
        return self.value - self.previous_value
    
    def clamp(self) -> "Slot":
        """Apply min/max constraints"""
        new_value = self.value
        if self.min_value is not None:
            new_value = max(new_value, self.min_value)
        if self.max_value is not None:
            new_value = min(new_value, self.max_value)
        return self.model_copy(update={"value": new_value})
    
    def advance(self, new_value: float, new_tick: int) -> "Slot":
        """Create next tick version"""
        return self.model_copy(update={
            "value": new_value,
            "previous_value": self.value,
            "tick": new_tick,
            "timestamp_sim": float(new_tick),
        })


# ============================================================================
# WORLD STATE
# ============================================================================

class WorldState(BaseModel):
    """
    WorldState = Immutable snapshot of the entire simulation at tick T.
    
    The WorldState is:
    - Immutable (new state = new object)
    - Hashable (for verification)
    - Chained (links to previous state)
    """
    
    state_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    simulation_id: str = Field(...)
    scenario_id: str = Field(default="baseline")
    tenant_id: Optional[str] = Field(default=None)
    
    # Temporal
    tick: int = Field(default=0)
    timestamp_sim: float = Field(default=0)
    
    # Slots (the actual data)
    slots: Dict[str, Slot] = Field(default_factory=dict)
    
    # Events at this tick
    events: List[str] = Field(default_factory=list)
    
    # Chain
    previous_state_id: Optional[str] = Field(default=None)
    previous_state_hash: Optional[str] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    synthetic: bool = Field(default=True)
    
    @computed_field
    @property
    def state_hash(self) -> str:
        """Compute state hash for verification"""
        content = {
            "simulation_id": self.simulation_id,
            "scenario_id": self.scenario_id,
            "tick": self.tick,
            "slots": {k: v.value for k, v in self.slots.items()},
            "previous_state_hash": self.previous_state_hash,
        }
        return hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()
    
    def get_slot(self, name: str) -> Optional[Slot]:
        """Get slot by name"""
        return self.slots.get(name)
    
    def get_value(self, name: str, default: float = 0.0) -> float:
        """Get slot value by name"""
        slot = self.slots.get(name)
        return slot.value if slot else default
    
    def set_slot(self, name: str, slot: Slot) -> "WorldState":
        """Create new state with updated slot"""
        new_slots = dict(self.slots)
        new_slots[name] = slot
        return self.model_copy(update={"slots": new_slots})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to simple dict for XR Pack"""
        return {
            "step": self.tick,
            "timestamp": self.timestamp_sim,
            "slots": {k: v.value for k, v in self.slots.items()},
            "events": self.events,
        }


# ============================================================================
# CAUSAL RULE
# ============================================================================

class CausalRule(BaseModel):
    """
    CausalRule = Defines how slots transform.
    
    Example: Production = Budget * Efficiency
    """
    
    rule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    
    # Target slot
    target_slot: str = Field(...)
    
    # Source slots
    source_slots: List[str] = Field(default_factory=list)
    
    # Formula (as string for display)
    formula: str = Field(default="")
    
    # Priority (lower = earlier)
    priority: int = Field(default=100)
    
    # Conditions
    conditions: Dict[str, Any] = Field(default_factory=dict)
    
    # Active?
    active: bool = Field(default=True)
    
    # Governance
    requires_approval: bool = Field(default=False)
    approved: bool = Field(default=False)


# ============================================================================
# SCENARIO
# ============================================================================

class Scenario(BaseModel):
    """
    Scenario = Configuration for a simulation run.
    
    A scenario defines:
    - Initial state
    - Rules to apply
    - Parameters/interventions
    - Duration
    """
    
    scenario_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    simulation_id: str = Field(...)
    name: str = Field(...)
    description: str = Field(default="")
    
    # Type
    scenario_type: ScenarioType = Field(default=ScenarioType.BASELINE)
    
    # Initial values
    initial_values: Dict[str, float] = Field(default_factory=dict)
    
    # Rules
    rules: List[CausalRule] = Field(default_factory=list)
    rule_ids: List[str] = Field(default_factory=list)
    
    # Interventions (slot_name -> {tick: value})
    interventions: Dict[str, Dict[int, float]] = Field(default_factory=dict)
    
    # Duration
    t_start: int = Field(default=0)
    t_end: int = Field(default=100)
    
    # Parameters
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # Seed for reproducibility
    seed: Optional[int] = Field(default=None)
    
    # Status
    status: SimulationStatus = Field(default=SimulationStatus.DRAFT)
    
    # Results (filled after run)
    result_artifact_id: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)


# ============================================================================
# SIMULATION
# ============================================================================

class Simulation(BaseModel):
    """
    Simulation = Container for multiple scenarios.
    
    A simulation groups related scenarios for comparison.
    """
    
    simulation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(default="")
    
    # Tenant
    tenant_id: Optional[str] = Field(default=None)
    
    # Scenarios
    scenarios: List[Scenario] = Field(default_factory=list)
    baseline_scenario_id: Optional[str] = Field(default=None)
    
    # Global configuration
    time_unit: TimeUnit = Field(default=TimeUnit.TICK)
    default_t_end: int = Field(default=100)
    
    # Slot definitions (shared across scenarios)
    slot_definitions: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    
    # Rules (shared across scenarios)
    shared_rules: List[CausalRule] = Field(default_factory=list)
    
    # Status
    status: SimulationStatus = Field(default=SimulationStatus.DRAFT)
    
    # Governance
    requires_approval: bool = Field(default=False)
    approval_token: Optional[str] = Field(default=None)
    approved_by: Optional[str] = Field(default=None)
    approved_at: Optional[datetime] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Results
    xr_pack_id: Optional[str] = Field(default=None)
    
    # Metadata
    synthetic: bool = Field(default=True)
    tags: List[str] = Field(default_factory=list)
    
    def add_scenario(self, scenario: Scenario) -> None:
        """Add scenario to simulation"""
        scenario.simulation_id = self.simulation_id
        self.scenarios.append(scenario)
        
        if scenario.scenario_type == ScenarioType.BASELINE:
            self.baseline_scenario_id = scenario.scenario_id
    
    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """Get scenario by ID"""
        for s in self.scenarios:
            if s.scenario_id == scenario_id:
                return s
        return None
    
    def get_baseline(self) -> Optional[Scenario]:
        """Get baseline scenario"""
        if self.baseline_scenario_id:
            return self.get_scenario(self.baseline_scenario_id)
        return None


# ============================================================================
# WORKER TASK
# ============================================================================

class WorkerTask(BaseModel):
    """
    WorkerTask = Unit of work for simulation execution.
    """
    
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    simulation_id: str = Field(...)
    scenario_id: str = Field(...)
    
    # Task type
    task_type: str = Field(default="simulate")  # simulate, validate, export
    
    # Range
    t_start: int = Field(default=0)
    t_end: int = Field(default=100)
    
    # Status
    status: WorkerStatus = Field(default=WorkerStatus.IDLE)
    progress: float = Field(default=0.0, ge=0, le=1)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    # Results
    result_artifact_id: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    
    # Worker info
    worker_id: Optional[str] = Field(default=None)


# ============================================================================
# SIMULATION ARTIFACT
# ============================================================================

class SimulationArtifact(BaseModel):
    """
    SimulationArtifact = Certified output of a simulation run.
    
    Contains:
    - All states from the simulation
    - Causal chain verification
    - Signature for integrity
    """
    
    artifact_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    simulation_id: str = Field(...)
    scenario_id: str = Field(...)
    tenant_id: Optional[str] = Field(default=None)
    
    # States
    states: List[WorldState] = Field(default_factory=list)
    
    # Summary
    t_start: int = Field(default=0)
    t_end: int = Field(default=0)
    total_ticks: int = Field(default=0)
    
    # Verification
    initial_state_hash: Optional[str] = Field(default=None)
    final_state_hash: Optional[str] = Field(default=None)
    chain_valid: bool = Field(default=False)
    
    # Signature
    signed: bool = Field(default=False)
    signature: Optional[str] = Field(default=None)
    key_id: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata
    synthetic: bool = Field(default=True)
    seed: Optional[int] = Field(default=None)
    
    def add_state(self, state: WorldState) -> None:
        """Add state to artifact"""
        self.states.append(state)
        self.total_ticks = len(self.states)
        
        if len(self.states) == 1:
            self.initial_state_hash = state.state_hash
            self.t_start = state.tick
        
        self.final_state_hash = state.state_hash
        self.t_end = state.tick
    
    def verify_chain(self) -> bool:
        """Verify state chain integrity"""
        if len(self.states) < 2:
            self.chain_valid = True
            return True
        
        for i in range(1, len(self.states)):
            current = self.states[i]
            previous = self.states[i - 1]
            
            if current.previous_state_hash != previous.state_hash:
                self.chain_valid = False
                return False
        
        self.chain_valid = True
        return True
    
    def to_xr_states(self) -> List[Dict[str, Any]]:
        """Convert to XR Pack format"""
        return [s.to_dict() for s in self.states]


# ============================================================================
# SIMULATION CONFIG
# ============================================================================

class SimulationConfig(BaseModel):
    """Global configuration for simulation runs"""
    
    # Execution
    max_ticks: int = Field(default=10000)
    tick_timeout_seconds: float = Field(default=5.0)
    
    # Safety
    enable_safety_controller: bool = Field(default=True)
    explosion_threshold: float = Field(default=1.35)
    collapse_floor: float = Field(default=0.001)
    
    # Determinism
    require_seed: bool = Field(default=True)
    default_seed: int = Field(default=42)
    
    # Governance
    require_opa_approval: bool = Field(default=True)
    require_hitl_for_interventions: bool = Field(default=True)
    
    # Output
    generate_xr_pack: bool = Field(default=True)
    chunk_size: int = Field(default=250)
    sign_artifacts: bool = Field(default=True)
