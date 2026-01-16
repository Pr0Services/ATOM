"""
============================================================================
CHE·NU™ V69 — DIVERGENCE CALCULATOR
============================================================================
Version: 1.0.0
Purpose: Calculate divergence points between simulation scenarios
Principle: Help executives see WHERE and WHY trajectories diverge
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import math

from ..models.artifacts import (
    DivergencePoint,
    DivergenceConfig,
    ScenarioDiff,
    DiffV1,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TIMELINE (from simulation)
# ============================================================================

class TimelineSnapshot:
    """Snapshot of state at a simulation step"""
    
    def __init__(
        self,
        step: int,
        slots: Dict[str, float],
        events: Optional[List[str]] = None,
    ):
        self.step = step
        self.slots = slots
        self.events = events or []
    
    def get_value(self, slot: str, default: float = 0.0) -> float:
        return self.slots.get(slot, default)


class Timeline:
    """Complete timeline of a simulation scenario"""
    
    def __init__(
        self,
        scenario_id: str,
        scenario_name: str = "",
    ):
        self.scenario_id = scenario_id
        self.scenario_name = scenario_name
        self.snapshots: Dict[int, TimelineSnapshot] = {}
    
    def add_snapshot(self, snapshot: TimelineSnapshot) -> None:
        self.snapshots[snapshot.step] = snapshot
    
    def get_snapshot(self, step: int) -> Optional[TimelineSnapshot]:
        return self.snapshots.get(step)
    
    @property
    def steps(self) -> List[int]:
        return sorted(self.snapshots.keys())
    
    @property
    def slots(self) -> List[str]:
        if not self.snapshots:
            return []
        first = next(iter(self.snapshots.values()))
        return list(first.slots.keys())


# ============================================================================
# DIVERGENCE CALCULATOR
# ============================================================================

class DivergenceCalculator:
    """
    Calculates divergence points between simulation scenarios.
    
    A divergence point is a step where the difference between
    baseline and scenario exceeds configured thresholds.
    
    This helps executives focus on:
    - WHERE trajectories diverge
    - WHY they diverge (top reasons)
    - IMPACT of the divergence
    
    Usage:
        calculator = DivergenceCalculator(config)
        
        # Add timelines
        calculator.set_baseline(baseline_timeline)
        calculator.add_scenario(scenario_timeline)
        
        # Calculate divergence
        diff = calculator.calculate()
    """
    
    def __init__(self, config: Optional[DivergenceConfig] = None):
        self.config = config or DivergenceConfig()
        self.baseline: Optional[Timeline] = None
        self.scenarios: List[Timeline] = []
    
    def set_baseline(self, timeline: Timeline) -> None:
        """Set baseline scenario for comparison"""
        self.baseline = timeline
    
    def add_scenario(self, timeline: Timeline) -> None:
        """Add scenario to compare against baseline"""
        self.scenarios.append(timeline)
    
    def calculate(self, simulation_id: str = "") -> DiffV1:
        """
        Calculate divergence analysis.
        
        Returns:
            DiffV1 with divergence points and scenario diffs
        """
        if self.baseline is None:
            raise ValueError("Baseline timeline not set")
        
        diff = DiffV1(
            simulation_id=simulation_id,
            baseline_scenario=self.baseline.scenario_id,
        )
        
        # Set thresholds
        diff.divergence["thresholds"] = {
            "budget": self.config.budget_threshold,
            "risk": self.config.risk_threshold,
            "velocity": self.config.velocity_threshold,
        }
        
        # Calculate for each scenario
        all_divergence_points: List[DivergencePoint] = []
        
        for scenario in self.scenarios:
            scenario_diff, points = self._calculate_scenario_diff(scenario)
            diff.scenarios.append(scenario_diff)
            all_divergence_points.extend(points)
        
        # Sort by step and limit
        all_divergence_points.sort(key=lambda p: p.step)
        
        # Take top N by severity
        sorted_by_severity = sorted(
            all_divergence_points,
            key=lambda p: self._severity_score(p),
            reverse=True,
        )[:self.config.max_points]
        
        # Re-sort by step for output
        sorted_by_severity.sort(key=lambda p: p.step)
        
        for point in sorted_by_severity:
            diff.add_divergence_point(point)
        
        # Generate summary
        diff.summary = self._generate_summary(diff)
        
        return diff
    
    def _calculate_scenario_diff(
        self,
        scenario: Timeline,
    ) -> Tuple[ScenarioDiff, List[DivergencePoint]]:
        """Calculate diff for a single scenario"""
        if self.baseline is None:
            raise ValueError("Baseline not set")
        
        scenario_diff = ScenarioDiff(
            baseline_id=self.baseline.scenario_id,
            scenario_id=scenario.scenario_id,
            scenario_name=scenario.scenario_name,
        )
        
        divergence_points: List[DivergencePoint] = []
        
        # Get all steps
        all_steps = sorted(set(self.baseline.steps) | set(scenario.steps))
        all_slots = list(set(self.baseline.slots) | set(scenario.slots))
        
        # Initialize deltas
        for slot in all_slots:
            scenario_diff.deltas[slot] = []
        
        max_delta = 0
        total_divergence = 0
        
        for step in all_steps:
            base_snap = self.baseline.get_snapshot(step)
            scen_snap = scenario.get_snapshot(step)
            
            if base_snap is None or scen_snap is None:
                continue
            
            step_signals: Dict[str, float] = {}
            step_reasons: List[str] = []
            is_divergent = False
            
            for slot in all_slots:
                base_val = base_snap.get_value(slot)
                scen_val = scen_snap.get_value(slot)
                delta = scen_val - base_val
                
                scenario_diff.deltas[slot].append(delta)
                
                abs_delta = abs(delta)
                max_delta = max(max_delta, abs_delta)
                total_divergence += abs_delta
                
                # Check thresholds
                threshold = self._get_threshold_for_slot(slot)
                if abs_delta > threshold:
                    is_divergent = True
                    step_signals[f"{slot}_delta"] = delta
                    
                    # Generate reason
                    direction = "increased" if delta > 0 else "decreased"
                    step_reasons.append(f"{slot} {direction} by {abs_delta:.2f}")
            
            # Add events as reasons
            if scen_snap.events:
                step_reasons.extend(scen_snap.events[:3])
            
            if is_divergent:
                severity = self._calculate_severity(step_signals)
                
                point = DivergencePoint(
                    step=step,
                    signals=step_signals,
                    top_reasons=step_reasons[:5],
                    summary=self._generate_point_summary(step, step_signals, scenario),
                    severity=severity,
                )
                divergence_points.append(point)
        
        scenario_diff.max_delta = max_delta
        scenario_diff.total_divergence = total_divergence
        
        return scenario_diff, divergence_points
    
    def _get_threshold_for_slot(self, slot: str) -> float:
        """Get threshold for a slot"""
        slot_lower = slot.lower()
        
        if "budget" in slot_lower or "cost" in slot_lower or "revenue" in slot_lower:
            return self.config.budget_threshold
        elif "risk" in slot_lower:
            return self.config.risk_threshold
        elif "velocity" in slot_lower or "speed" in slot_lower:
            return self.config.velocity_threshold
        else:
            # Default: use budget threshold as fallback
            return self.config.budget_threshold
    
    def _calculate_severity(self, signals: Dict[str, float]) -> str:
        """Calculate severity level from signals"""
        if not signals:
            return "low"
        
        max_signal = max(abs(v) for v in signals.values())
        
        # Normalize by thresholds
        normalized = max_signal / max(
            self.config.budget_threshold,
            self.config.risk_threshold * 1000,
            self.config.velocity_threshold * 1000,
        )
        
        if normalized > 5:
            return "critical"
        elif normalized > 2:
            return "high"
        elif normalized > 1:
            return "medium"
        else:
            return "low"
    
    def _severity_score(self, point: DivergencePoint) -> float:
        """Get numeric score for severity"""
        severity_map = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
        }
        base_score = severity_map.get(point.severity, 1)
        
        # Add signal magnitude
        if point.signals:
            signal_score = sum(abs(v) for v in point.signals.values())
        else:
            signal_score = 0
        
        return base_score * 1000 + signal_score
    
    def _generate_point_summary(
        self,
        step: int,
        signals: Dict[str, float],
        scenario: Timeline,
    ) -> str:
        """Generate human-readable summary for a divergence point"""
        parts = [f"At step {step}"]
        
        # Describe signals
        signal_parts = []
        for key, value in sorted(signals.items(), key=lambda x: abs(x[1]), reverse=True)[:3]:
            direction = "+" if value > 0 else ""
            signal_parts.append(f"{key}: {direction}{value:.2f}")
        
        if signal_parts:
            parts.append(f"({', '.join(signal_parts)})")
        
        parts.append(f"in scenario '{scenario.scenario_name}'")
        
        return " ".join(parts)
    
    def _generate_summary(self, diff: DiffV1) -> str:
        """Generate overall summary"""
        num_points = len(diff.divergence.get("points", []))
        num_scenarios = len(diff.scenarios)
        
        if num_points == 0:
            return f"No significant divergence detected across {num_scenarios} scenario(s)."
        
        # Find most divergent scenario
        max_div_scenario = max(
            diff.scenarios,
            key=lambda s: s.total_divergence,
            default=None,
        )
        
        summary = f"Detected {num_points} divergence point(s) across {num_scenarios} scenario(s)."
        
        if max_div_scenario:
            summary += f" Most divergent: '{max_div_scenario.scenario_name}' (total delta: {max_div_scenario.total_divergence:.2f})."
        
        return summary


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_timeline_from_states(
    scenario_id: str,
    states: List[Dict[str, Any]],
    scenario_name: str = "",
) -> Timeline:
    """
    Create Timeline from list of state dictionaries.
    
    Args:
        scenario_id: Unique scenario identifier
        states: List of {"step": int, "slots": {name: value}, "events": [...]}
        scenario_name: Human-readable name
    """
    timeline = Timeline(scenario_id, scenario_name)
    
    for state in states:
        snapshot = TimelineSnapshot(
            step=state.get("step", 0),
            slots=state.get("slots", {}),
            events=state.get("events", []),
        )
        timeline.add_snapshot(snapshot)
    
    return timeline


def calculate_divergence(
    baseline_states: List[Dict[str, Any]],
    scenario_states: List[Dict[str, Any]],
    simulation_id: str = "",
    config: Optional[DivergenceConfig] = None,
) -> DiffV1:
    """
    Quick helper to calculate divergence between two state lists.
    """
    baseline = create_timeline_from_states(
        "baseline",
        baseline_states,
        "Baseline",
    )
    
    scenario = create_timeline_from_states(
        "scenario_1",
        scenario_states,
        "Alternative Scenario",
    )
    
    calculator = DivergenceCalculator(config)
    calculator.set_baseline(baseline)
    calculator.add_scenario(scenario)
    
    return calculator.calculate(simulation_id)
