"""
============================================================================
CHE·NU™ V69 — SCENARIO MANAGER
============================================================================
Version: 1.0.0
Purpose: Advanced scenario management and comparison
Principle: Support decision-making through scenario analysis
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import copy

from ..core.models import (
    Simulation,
    Scenario,
    ScenarioType,
    SimulationArtifact,
    SimulationStatus,
    WorldState,
)

logger = logging.getLogger(__name__)


# ============================================================================
# SCENARIO COMPARISON
# ============================================================================

class ScenarioComparison:
    """
    Comparison results between two scenarios.
    """
    
    def __init__(
        self,
        baseline_id: str,
        scenario_id: str,
        baseline_name: str = "",
        scenario_name: str = "",
    ):
        self.baseline_id = baseline_id
        self.scenario_id = scenario_id
        self.baseline_name = baseline_name
        self.scenario_name = scenario_name
        
        # Slot comparisons
        self.slot_deltas: Dict[str, List[float]] = {}
        self.max_deltas: Dict[str, float] = {}
        self.avg_deltas: Dict[str, float] = {}
        
        # Key metrics
        self.divergence_points: List[Dict[str, Any]] = []
        self.total_divergence: float = 0.0
        
        # Summary
        self.summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "scenario_id": self.scenario_id,
            "baseline_name": self.baseline_name,
            "scenario_name": self.scenario_name,
            "max_deltas": self.max_deltas,
            "avg_deltas": self.avg_deltas,
            "total_divergence": self.total_divergence,
            "divergence_points_count": len(self.divergence_points),
            "summary": self.summary,
        }


# ============================================================================
# SCENARIO MANAGER
# ============================================================================

class ScenarioManager:
    """
    Manages scenario creation, cloning, and comparison.
    
    Features:
    - Clone scenarios with modifications
    - Compare scenarios against baseline
    - Generate what-if variants
    - Sensitivity analysis
    
    Usage:
        manager = ScenarioManager(simulation)
        
        # Clone with modifications
        aggressive = manager.clone_scenario(
            baseline,
            name="Aggressive",
            modifications={"Budget": lambda v: v * 1.5},
        )
        
        # Compare results
        comparison = manager.compare_artifacts(
            baseline_artifact,
            aggressive_artifact,
        )
    """
    
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
    
    def clone_scenario(
        self,
        source: Scenario,
        name: str,
        modifications: Optional[Dict[str, Any]] = None,
        interventions: Optional[Dict[str, Dict[int, float]]] = None,
        scenario_type: ScenarioType = ScenarioType.ALTERNATIVE,
    ) -> Scenario:
        """
        Clone a scenario with modifications.
        
        Args:
            source: Source scenario to clone
            name: Name for new scenario
            modifications: Dict of slot_name -> new_value or callable
            interventions: New interventions to apply
            scenario_type: Type for new scenario
            
        Returns:
            New cloned Scenario
        """
        # Clone initial values
        new_initial = dict(source.initial_values)
        
        # Apply modifications
        if modifications:
            for slot_name, mod in modifications.items():
                if slot_name in new_initial:
                    if callable(mod):
                        new_initial[slot_name] = mod(new_initial[slot_name])
                    else:
                        new_initial[slot_name] = mod
        
        # Clone interventions
        new_interventions = copy.deepcopy(source.interventions)
        if interventions:
            for slot_name, slot_interventions in interventions.items():
                if slot_name not in new_interventions:
                    new_interventions[slot_name] = {}
                new_interventions[slot_name].update(slot_interventions)
        
        # Create new scenario
        new_scenario = Scenario(
            simulation_id=self.simulation.simulation_id,
            name=name,
            description=f"Cloned from {source.name}",
            scenario_type=scenario_type,
            initial_values=new_initial,
            interventions=new_interventions,
            t_start=source.t_start,
            t_end=source.t_end,
            seed=source.seed,
            parameters=dict(source.parameters),
        )
        
        # Copy rules
        new_scenario.rules = list(source.rules)
        new_scenario.rule_ids = list(source.rule_ids)
        
        # Add to simulation
        self.simulation.scenarios.append(new_scenario)
        
        logger.info(f"Cloned scenario: {source.scenario_id} -> {new_scenario.scenario_id}")
        
        return new_scenario
    
    def create_sensitivity_variants(
        self,
        source: Scenario,
        slot_name: str,
        variations: List[float],
        name_prefix: str = "Sensitivity",
    ) -> List[Scenario]:
        """
        Create multiple scenarios varying a single slot.
        
        Args:
            source: Source scenario
            slot_name: Slot to vary
            variations: List of multipliers (e.g., [0.8, 0.9, 1.1, 1.2])
            name_prefix: Prefix for scenario names
            
        Returns:
            List of new scenarios
        """
        scenarios = []
        
        for var in variations:
            name = f"{name_prefix}_{slot_name}_{var:.0%}"
            scenario = self.clone_scenario(
                source,
                name=name,
                modifications={slot_name: lambda v, m=var: v * m},
                scenario_type=ScenarioType.ALTERNATIVE,
            )
            scenarios.append(scenario)
        
        return scenarios
    
    def create_stress_test(
        self,
        source: Scenario,
        name: str,
        stress_factors: Dict[str, float],
    ) -> Scenario:
        """
        Create a stress test scenario.
        
        Args:
            source: Source scenario
            name: Stress test name
            stress_factors: Dict of slot_name -> stress multiplier
            
        Returns:
            Stress test scenario
        """
        modifications = {
            slot: lambda v, f=factor: v * f
            for slot, factor in stress_factors.items()
        }
        
        return self.clone_scenario(
            source,
            name=name,
            modifications=modifications,
            scenario_type=ScenarioType.STRESS_TEST,
        )
    
    def compare_artifacts(
        self,
        baseline_artifact: SimulationArtifact,
        scenario_artifact: SimulationArtifact,
        divergence_threshold: float = 0.1,
    ) -> ScenarioComparison:
        """
        Compare two scenario artifacts.
        
        Args:
            baseline_artifact: Baseline artifact
            scenario_artifact: Scenario to compare
            divergence_threshold: Threshold for divergence detection
            
        Returns:
            ScenarioComparison results
        """
        comparison = ScenarioComparison(
            baseline_id=baseline_artifact.scenario_id,
            scenario_id=scenario_artifact.scenario_id,
        )
        
        # Get common ticks
        baseline_states = {s.tick: s for s in baseline_artifact.states}
        scenario_states = {s.tick: s for s in scenario_artifact.states}
        
        common_ticks = sorted(set(baseline_states.keys()) & set(scenario_states.keys()))
        
        if not common_ticks:
            comparison.summary = "No common ticks found"
            return comparison
        
        # Get all slot names
        first_baseline = baseline_states[common_ticks[0]]
        slot_names = list(first_baseline.slots.keys())
        
        # Initialize delta tracking
        for slot_name in slot_names:
            comparison.slot_deltas[slot_name] = []
        
        # Calculate deltas for each tick
        for tick in common_ticks:
            baseline_state = baseline_states[tick]
            scenario_state = scenario_states[tick]
            
            tick_deltas = {}
            
            for slot_name in slot_names:
                baseline_val = baseline_state.get_value(slot_name)
                scenario_val = scenario_state.get_value(slot_name)
                
                delta = scenario_val - baseline_val
                comparison.slot_deltas[slot_name].append(delta)
                tick_deltas[slot_name] = delta
                
                # Check for divergence
                if baseline_val != 0:
                    relative_delta = abs(delta) / abs(baseline_val)
                    if relative_delta > divergence_threshold:
                        comparison.divergence_points.append({
                            "tick": tick,
                            "slot": slot_name,
                            "baseline_value": baseline_val,
                            "scenario_value": scenario_val,
                            "delta": delta,
                            "relative_delta": relative_delta,
                        })
        
        # Calculate summary statistics
        for slot_name, deltas in comparison.slot_deltas.items():
            if deltas:
                comparison.max_deltas[slot_name] = max(abs(d) for d in deltas)
                comparison.avg_deltas[slot_name] = sum(deltas) / len(deltas)
        
        # Calculate total divergence
        comparison.total_divergence = sum(comparison.max_deltas.values())
        
        # Generate summary
        if comparison.divergence_points:
            most_divergent = max(
                comparison.divergence_points,
                key=lambda p: abs(p["delta"]),
            )
            comparison.summary = (
                f"Found {len(comparison.divergence_points)} divergence points. "
                f"Maximum at tick {most_divergent['tick']} for {most_divergent['slot']}."
            )
        else:
            comparison.summary = "No significant divergence detected."
        
        return comparison
    
    def get_baseline(self) -> Optional[Scenario]:
        """Get baseline scenario"""
        return self.simulation.get_baseline()
    
    def list_scenarios(
        self,
        scenario_type: Optional[ScenarioType] = None,
    ) -> List[Scenario]:
        """List scenarios, optionally filtered by type"""
        scenarios = self.simulation.scenarios
        
        if scenario_type:
            scenarios = [s for s in scenarios if s.scenario_type == scenario_type]
        
        return scenarios


# ============================================================================
# WHAT-IF ANALYZER
# ============================================================================

class WhatIfAnalyzer:
    """
    Analyzes what-if scenarios and interventions.
    
    Helps answer questions like:
    - What if we increase budget by 20%?
    - What if we delay the project by 3 months?
    - What is the impact of a specific intervention?
    """
    
    def __init__(self, scenario_manager: ScenarioManager):
        self.manager = scenario_manager
    
    def what_if_initial_change(
        self,
        baseline: Scenario,
        slot_name: str,
        new_value: float,
        name: Optional[str] = None,
    ) -> Scenario:
        """
        Create a what-if scenario with changed initial value.
        
        Args:
            baseline: Baseline scenario
            slot_name: Slot to change
            new_value: New initial value
            name: Scenario name
            
        Returns:
            New what-if scenario
        """
        name = name or f"What-If {slot_name}={new_value}"
        
        return self.manager.clone_scenario(
            baseline,
            name=name,
            modifications={slot_name: new_value},
            scenario_type=ScenarioType.COUNTERFACTUAL,
        )
    
    def what_if_intervention(
        self,
        baseline: Scenario,
        slot_name: str,
        tick: int,
        value: float,
        name: Optional[str] = None,
    ) -> Scenario:
        """
        Create a what-if scenario with an intervention.
        
        Args:
            baseline: Baseline scenario
            slot_name: Slot to intervene on
            tick: Tick to apply intervention
            value: Intervention value
            name: Scenario name
            
        Returns:
            New what-if scenario
        """
        name = name or f"What-If {slot_name}@{tick}={value}"
        
        return self.manager.clone_scenario(
            baseline,
            name=name,
            interventions={slot_name: {tick: value}},
            scenario_type=ScenarioType.COUNTERFACTUAL,
        )
    
    def sensitivity_analysis(
        self,
        baseline: Scenario,
        slot_name: str,
        range_pct: float = 0.2,
        num_steps: int = 5,
    ) -> List[Scenario]:
        """
        Create scenarios for sensitivity analysis.
        
        Args:
            baseline: Baseline scenario
            slot_name: Slot to vary
            range_pct: Variation range (e.g., 0.2 = ±20%)
            num_steps: Number of steps in each direction
            
        Returns:
            List of scenarios
        """
        step_size = range_pct / num_steps
        
        variations = []
        for i in range(-num_steps, num_steps + 1):
            if i != 0:  # Skip baseline
                variations.append(1 + (i * step_size))
        
        return self.manager.create_sensitivity_variants(
            baseline,
            slot_name,
            variations,
            name_prefix=f"Sensitivity_{slot_name}",
        )
