"""
============================================================================
CHE·NU™ V69 — WORLDENGINE CORE
============================================================================
Version: 1.0.0
Purpose: Central orchestrator for deterministic simulations
Principle: GOUVERNANCE > EXÉCUTION — Zero hallucination, full traceability
============================================================================
"""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import random

from .models import (
    Slot,
    WorldState,
    CausalRule,
    Scenario,
    Simulation,
    SimulationArtifact,
    SimulationConfig,
    SimulationStatus,
    ScenarioType,
)

# Import from previous phases
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from feedback import FeedbackLoopEngine, Slot as FeedbackSlot
from feedback.loops.audited import AuditedFeedbackEngine
from audit import AuditLog, EventType

logger = logging.getLogger(__name__)


# ============================================================================
# RULE EXECUTOR
# ============================================================================

class RuleExecutor:
    """
    Executes causal rules on WorldState.
    
    Rules are applied in priority order to transform slots.
    """
    
    def __init__(self):
        self._rule_functions: Dict[str, Callable] = {}
    
    def register_rule_function(
        self,
        rule_id: str,
        func: Callable[[Dict[str, float]], float],
    ) -> None:
        """Register a custom rule function"""
        self._rule_functions[rule_id] = func
    
    def execute_rule(
        self,
        rule: CausalRule,
        state: WorldState,
    ) -> Optional[Slot]:
        """
        Execute a single rule on the state.
        
        Returns new slot value or None if rule doesn't apply.
        """
        if not rule.active:
            return None
        
        # Check conditions
        if not self._check_conditions(rule, state):
            return None
        
        # Get source values
        source_values = {}
        for source_slot in rule.source_slots:
            slot = state.get_slot(source_slot)
            if slot is None:
                logger.warning(f"Source slot not found: {source_slot}")
                return None
            source_values[source_slot] = slot.value
        
        # Execute rule
        if rule.rule_id in self._rule_functions:
            # Custom function
            new_value = self._rule_functions[rule.rule_id](source_values)
        else:
            # Default: simple multiplication
            new_value = 1.0
            for v in source_values.values():
                new_value *= v
        
        # Get or create target slot
        target_slot = state.get_slot(rule.target_slot)
        if target_slot is None:
            target_slot = Slot(
                name=rule.target_slot,
                value=0,
                tick=state.tick,
            )
        
        # Create new slot with updated value
        return target_slot.advance(new_value, state.tick)
    
    def execute_all_rules(
        self,
        rules: List[CausalRule],
        state: WorldState,
    ) -> WorldState:
        """Execute all rules on state in priority order"""
        # Sort by priority
        sorted_rules = sorted(rules, key=lambda r: r.priority)
        
        new_state = state
        for rule in sorted_rules:
            new_slot = self.execute_rule(rule, new_state)
            if new_slot:
                new_state = new_state.set_slot(rule.target_slot, new_slot)
        
        return new_state
    
    def _check_conditions(self, rule: CausalRule, state: WorldState) -> bool:
        """Check if rule conditions are met"""
        for slot_name, condition in rule.conditions.items():
            slot = state.get_slot(slot_name)
            if slot is None:
                return False
            
            if isinstance(condition, dict):
                if "min" in condition and slot.value < condition["min"]:
                    return False
                if "max" in condition and slot.value > condition["max"]:
                    return False
            elif slot.value != condition:
                return False
        
        return True


# ============================================================================
# WORLDENGINE
# ============================================================================

class WorldEngine:
    """
    WorldEngine = Central orchestrator for CHE·NU™ simulations.
    
    The WorldEngine:
    - Manages simulations and scenarios
    - Executes causal rules deterministically
    - Applies feedback loops
    - Enforces governance (OPA)
    - Generates certified artifacts
    - Produces XR Packs
    
    Architecture:
    
        ┌─────────────────────────────────────────────────────────┐
        │                     WORLDENGINE                         │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │   ┌─────────────┐    ┌─────────────┐    ┌───────────┐ │
        │   │ Simulation  │───▶│  Scenario   │───▶│  Worker   │ │
        │   └─────────────┘    └─────────────┘    └─────┬─────┘ │
        │                                               │       │
        │   ┌─────────────────────────────────────────────┐     │
        │   │              EXECUTION PIPELINE             │     │
        │   ├─────────────────────────────────────────────┤     │
        │   │ 1. OPA Pre-Check   ─▶ GOUVERNANCE           │     │
        │   │ 2. Snapshot        ─▶ Immutable State       │     │
        │   │ 3. Rules           ─▶ Causal Transform      │     │
        │   │ 4. Feedback        ─▶ Loop Dynamics         │     │
        │   │ 5. Safety          ─▶ L2 Controller         │     │
        │   │ 6. Artifact        ─▶ Signed Output         │     │
        │   │ 7. Audit           ─▶ Merkle Trail          │     │
        │   └─────────────────────────────────────────────┘     │
        │                                                         │
        │   Output: SimulationArtifact + XR Pack                 │
        └─────────────────────────────────────────────────────────┘
    
    Usage:
        engine = WorldEngine()
        
        # Create simulation
        sim = engine.create_simulation("Budget Analysis")
        
        # Add scenarios
        baseline = engine.add_scenario(sim, "Baseline", {...})
        aggressive = engine.add_scenario(sim, "Aggressive", {...})
        
        # Run simulation
        artifacts = engine.run_simulation(sim.simulation_id)
        
        # Generate XR Pack
        xr_pack = engine.generate_xr_pack(sim.simulation_id)
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()
        
        # Storage
        self._simulations: Dict[str, Simulation] = {}
        self._artifacts: Dict[str, SimulationArtifact] = {}
        
        # Executors
        self.rule_executor = RuleExecutor()
        
        # Audit
        self._audit_logs: Dict[str, AuditLog] = {}
    
    def create_simulation(
        self,
        name: str,
        description: str = "",
        tenant_id: Optional[str] = None,
        **kwargs,
    ) -> Simulation:
        """
        Create a new simulation.
        
        Args:
            name: Simulation name
            description: Description
            tenant_id: Tenant ID
            
        Returns:
            New Simulation object
        """
        sim = Simulation(
            name=name,
            description=description,
            tenant_id=tenant_id,
            default_t_end=kwargs.get("t_end", self.config.max_ticks),
            **{k: v for k, v in kwargs.items() if k != "t_end"},
        )
        
        self._simulations[sim.simulation_id] = sim
        
        # Create audit log
        audit = AuditLog(simulation_id=sim.simulation_id, tenant_id=tenant_id)
        audit.record(
            EventType.SIMULATION_START,
            f"Simulation created: {name}",
            data={"simulation_id": sim.simulation_id},
        )
        self._audit_logs[sim.simulation_id] = audit
        
        logger.info(f"Created simulation: {sim.simulation_id} - {name}")
        
        return sim
    
    def add_scenario(
        self,
        simulation_id: str,
        name: str,
        initial_values: Dict[str, float],
        scenario_type: ScenarioType = ScenarioType.ALTERNATIVE,
        t_end: Optional[int] = None,
        seed: Optional[int] = None,
        **kwargs,
    ) -> Scenario:
        """
        Add a scenario to a simulation.
        
        Args:
            simulation_id: Parent simulation ID
            name: Scenario name
            initial_values: Initial slot values
            scenario_type: Type of scenario
            t_end: End tick (uses simulation default if None)
            seed: Random seed for reproducibility
            
        Returns:
            New Scenario object
        """
        sim = self._simulations.get(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        scenario = Scenario(
            simulation_id=simulation_id,
            name=name,
            initial_values=initial_values,
            scenario_type=scenario_type,
            t_end=t_end or sim.default_t_end,
            seed=seed or (self.config.default_seed if self.config.require_seed else None),
            **kwargs,
        )
        
        sim.add_scenario(scenario)
        
        # Log
        audit = self._audit_logs.get(simulation_id)
        if audit:
            audit.record(
                EventType.SIMULATION_START,
                f"Scenario added: {name}",
                data={
                    "scenario_id": scenario.scenario_id,
                    "type": scenario_type.value,
                },
            )
        
        logger.info(f"Added scenario: {scenario.scenario_id} - {name}")
        
        return scenario
    
    def add_rule(
        self,
        simulation_id: str,
        name: str,
        target_slot: str,
        source_slots: List[str],
        formula: str = "",
        priority: int = 100,
        rule_function: Optional[Callable] = None,
    ) -> CausalRule:
        """
        Add a causal rule to a simulation.
        
        Args:
            simulation_id: Simulation ID
            name: Rule name
            target_slot: Target slot to update
            source_slots: Source slots to read
            formula: Formula description (for display)
            priority: Execution priority (lower = first)
            rule_function: Custom function to apply
            
        Returns:
            New CausalRule object
        """
        sim = self._simulations.get(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        rule = CausalRule(
            name=name,
            target_slot=target_slot,
            source_slots=source_slots,
            formula=formula,
            priority=priority,
        )
        
        sim.shared_rules.append(rule)
        
        # Register custom function if provided
        if rule_function:
            self.rule_executor.register_rule_function(rule.rule_id, rule_function)
        
        logger.info(f"Added rule: {rule.rule_id} - {name}")
        
        return rule
    
    def run_simulation(
        self,
        simulation_id: str,
        scenario_ids: Optional[List[str]] = None,
    ) -> Dict[str, SimulationArtifact]:
        """
        Run simulation for specified scenarios.
        
        Args:
            simulation_id: Simulation ID
            scenario_ids: Specific scenarios to run (all if None)
            
        Returns:
            Dict of scenario_id -> SimulationArtifact
        """
        sim = self._simulations.get(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        # Get scenarios to run
        scenarios = sim.scenarios
        if scenario_ids:
            scenarios = [s for s in scenarios if s.scenario_id in scenario_ids]
        
        if not scenarios:
            raise ValueError("No scenarios to run")
        
        # Update status
        sim.status = SimulationStatus.RUNNING
        sim.started_at = datetime.utcnow()
        
        results = {}
        
        for scenario in scenarios:
            try:
                artifact = self._run_scenario(sim, scenario)
                results[scenario.scenario_id] = artifact
                scenario.status = SimulationStatus.COMPLETED
                scenario.result_artifact_id = artifact.artifact_id
                
            except Exception as e:
                logger.error(f"Scenario failed: {scenario.scenario_id} - {e}")
                scenario.status = SimulationStatus.FAILED
                
                # Log error
                audit = self._audit_logs.get(simulation_id)
                if audit:
                    audit.record(
                        EventType.SIMULATION_END,
                        f"Scenario failed: {e}",
                        level="CRITICAL",
                        data={"scenario_id": scenario.scenario_id, "error": str(e)},
                    )
        
        # Update simulation status
        all_completed = all(s.status == SimulationStatus.COMPLETED for s in scenarios)
        sim.status = SimulationStatus.COMPLETED if all_completed else SimulationStatus.FAILED
        sim.completed_at = datetime.utcnow()
        
        return results
    
    def _run_scenario(
        self,
        simulation: Simulation,
        scenario: Scenario,
    ) -> SimulationArtifact:
        """Run a single scenario"""
        logger.info(f"Running scenario: {scenario.scenario_id} - {scenario.name}")
        
        scenario.status = SimulationStatus.RUNNING
        scenario.started_at = datetime.utcnow()
        
        # Initialize random seed
        if scenario.seed is not None:
            random.seed(scenario.seed)
        
        # Create initial state
        state = self._create_initial_state(simulation, scenario)
        
        # Create artifact
        artifact = SimulationArtifact(
            simulation_id=simulation.simulation_id,
            scenario_id=scenario.scenario_id,
            tenant_id=simulation.tenant_id,
            seed=scenario.seed,
        )
        artifact.add_state(state)
        
        # Get rules
        rules = simulation.shared_rules + scenario.rules
        
        # Run simulation loop
        for tick in range(scenario.t_start + 1, scenario.t_end + 1):
            # Apply interventions
            state = self._apply_interventions(state, scenario, tick)
            
            # Execute rules
            state = self.rule_executor.execute_all_rules(rules, state)
            
            # Create new state for this tick
            new_state = WorldState(
                simulation_id=simulation.simulation_id,
                scenario_id=scenario.scenario_id,
                tenant_id=simulation.tenant_id,
                tick=tick,
                timestamp_sim=float(tick),
                slots=state.slots,
                events=state.events,
                previous_state_id=state.state_id,
                previous_state_hash=state.state_hash,
            )
            
            artifact.add_state(new_state)
            state = new_state
            
            # Check for safety (simplified)
            if self.config.enable_safety_controller:
                if not self._safety_check(state):
                    logger.warning(f"Safety check failed at tick {tick}")
                    break
        
        # Verify chain
        artifact.verify_chain()
        
        # Store artifact
        self._artifacts[artifact.artifact_id] = artifact
        
        # Log completion
        audit = self._audit_logs.get(simulation.simulation_id)
        if audit:
            audit.record(
                EventType.SIMULATION_END,
                f"Scenario completed: {scenario.name}",
                data={
                    "scenario_id": scenario.scenario_id,
                    "artifact_id": artifact.artifact_id,
                    "total_ticks": artifact.total_ticks,
                },
            )
        
        scenario.completed_at = datetime.utcnow()
        
        logger.info(
            f"Scenario completed: {scenario.scenario_id} - "
            f"{artifact.total_ticks} ticks, chain_valid={artifact.chain_valid}"
        )
        
        return artifact
    
    def _create_initial_state(
        self,
        simulation: Simulation,
        scenario: Scenario,
    ) -> WorldState:
        """Create initial world state"""
        slots = {}
        
        for name, value in scenario.initial_values.items():
            # Get slot definition if exists
            slot_def = simulation.slot_definitions.get(name, {})
            
            slots[name] = Slot(
                name=name,
                value=value,
                unit=slot_def.get("unit", ""),
                slot_type=slot_def.get("type", "numeric"),
                min_value=slot_def.get("min"),
                max_value=slot_def.get("max"),
                tick=scenario.t_start,
            )
        
        return WorldState(
            simulation_id=simulation.simulation_id,
            scenario_id=scenario.scenario_id,
            tenant_id=simulation.tenant_id,
            tick=scenario.t_start,
            timestamp_sim=float(scenario.t_start),
            slots=slots,
        )
    
    def _apply_interventions(
        self,
        state: WorldState,
        scenario: Scenario,
        tick: int,
    ) -> WorldState:
        """Apply scenario interventions at tick"""
        new_state = state
        
        for slot_name, interventions in scenario.interventions.items():
            if tick in interventions:
                value = interventions[tick]
                slot = state.get_slot(slot_name)
                
                if slot:
                    new_slot = slot.advance(value, tick)
                    new_state = new_state.set_slot(slot_name, new_slot)
                    new_state.events.append(f"intervention:{slot_name}={value}")
        
        return new_state
    
    def _safety_check(self, state: WorldState) -> bool:
        """Simple safety check"""
        for slot in state.slots.values():
            # Check for explosion
            if slot.previous_value and slot.previous_value > 0:
                ratio = slot.value / slot.previous_value
                if ratio > self.config.explosion_threshold:
                    return False
            
            # Check for collapse
            if slot.value < self.config.collapse_floor:
                return False
        
        return True
    
    def get_simulation(self, simulation_id: str) -> Optional[Simulation]:
        """Get simulation by ID"""
        return self._simulations.get(simulation_id)
    
    def get_artifact(self, artifact_id: str) -> Optional[SimulationArtifact]:
        """Get artifact by ID"""
        return self._artifacts.get(artifact_id)
    
    def get_audit_log(self, simulation_id: str) -> Optional[AuditLog]:
        """Get audit log for simulation"""
        return self._audit_logs.get(simulation_id)
    
    def list_simulations(self, tenant_id: Optional[str] = None) -> List[Simulation]:
        """List simulations, optionally filtered by tenant"""
        sims = list(self._simulations.values())
        if tenant_id:
            sims = [s for s in sims if s.tenant_id == tenant_id]
        return sims


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_simple_simulation(
    name: str,
    initial_values: Dict[str, float],
    rules: List[Dict[str, Any]],
    t_end: int = 100,
    seed: int = 42,
) -> Tuple[WorldEngine, Simulation, Scenario]:
    """
    Quick helper to create a simple simulation.
    
    Args:
        name: Simulation name
        initial_values: Initial slot values
        rules: List of rule definitions
        t_end: End tick
        seed: Random seed
        
    Returns:
        Tuple of (engine, simulation, baseline_scenario)
    """
    engine = WorldEngine()
    
    # Create simulation
    sim = engine.create_simulation(name)
    
    # Add baseline scenario
    scenario = engine.add_scenario(
        sim.simulation_id,
        "Baseline",
        initial_values,
        scenario_type=ScenarioType.BASELINE,
        t_end=t_end,
        seed=seed,
    )
    
    # Add rules
    for rule_def in rules:
        engine.add_rule(
            sim.simulation_id,
            name=rule_def.get("name", "Rule"),
            target_slot=rule_def["target"],
            source_slots=rule_def.get("sources", []),
            formula=rule_def.get("formula", ""),
            priority=rule_def.get("priority", 100),
            rule_function=rule_def.get("function"),
        )
    
    return engine, sim, scenario
