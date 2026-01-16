"""
============================================================================
CHE·NU™ V69 — TIMELINE DIVERGENCE VISUALIZATION (XR)
============================================================================
Spec: GPT1/CHE-NU_TIMELINE_DIVERGENCE_UI.md

Purpose: Visually compare multiple simulated futures in XR.

Features:
- Parallel timelines
- Divergence markers
- Differential risk heatmaps
- Key-decision anchors

Interaction:
- Scrub time
- Toggle scenarios
- Inspect delta causes

Value: Executive clarity, Faster alignment, Strategic insight
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    Timeline,
    TimelinePoint,
    DivergenceMarker,
    RiskHeatmapCell,
    ImpactColor,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TIMELINE BUILDER
# ============================================================================

class TimelineBuilder:
    """Build timelines from simulation data"""
    
    def build_timeline(
        self,
        scenario_id: str,
        name: str,
        data_points: List[Dict[str, float]],
        key_decisions: List[int] = None,
    ) -> Timeline:
        """Build a timeline from data points"""
        timeline = Timeline(
            timeline_id=generate_id(),
            scenario_id=scenario_id,
            name=name,
        )
        
        key_decisions = key_decisions or []
        
        for i, values in enumerate(data_points):
            point = TimelinePoint(
                time=i,
                values=values,
                is_key_decision=i in key_decisions,
            )
            timeline.points.append(point)
        
        return timeline


# ============================================================================
# DIVERGENCE DETECTOR
# ============================================================================

class DivergenceDetector:
    """
    Detect where timelines diverge.
    
    Per spec: Divergence markers
    """
    
    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
    
    def find_divergences(
        self,
        timeline_a: Timeline,
        timeline_b: Timeline,
    ) -> List[DivergenceMarker]:
        """Find all divergence points between two timelines"""
        markers = []
        
        min_len = min(len(timeline_a.points), len(timeline_b.points))
        
        for i in range(min_len):
            point_a = timeline_a.points[i]
            point_b = timeline_b.points[i]
            
            # Find deltas
            deltas = {}
            for key in set(point_a.values.keys()) | set(point_b.values.keys()):
                val_a = point_a.values.get(key, 0)
                val_b = point_b.values.get(key, 0)
                
                if abs(val_a - val_b) > self.threshold:
                    deltas[key] = val_b - val_a
            
            if deltas:
                marker = DivergenceMarker(
                    marker_id=generate_id(),
                    time=i,
                    timeline_a=timeline_a.timeline_id,
                    timeline_b=timeline_b.timeline_id,
                    delta_values=deltas,
                    cause=self._infer_cause(deltas),
                )
                markers.append(marker)
        
        return markers
    
    def _infer_cause(self, deltas: Dict[str, float]) -> str:
        """Infer the primary cause of divergence"""
        if not deltas:
            return "Unknown"
        
        # Find biggest delta
        max_key = max(deltas.keys(), key=lambda k: abs(deltas[k]))
        return f"Primary delta in {max_key}: {deltas[max_key]:+.2f}"


# ============================================================================
# RISK HEATMAP GENERATOR
# ============================================================================

class RiskHeatmapGenerator:
    """
    Generate differential risk heatmaps.
    
    Per spec: Differential risk heatmaps
    """
    
    def generate(
        self,
        timelines: List[Timeline],
        target_slot: str,
    ) -> List[RiskHeatmapCell]:
        """Generate heatmap cells for a target slot across timelines"""
        cells = []
        
        if not timelines:
            return cells
        
        # Get all time points
        max_time = max(len(t.points) for t in timelines)
        
        for t in range(max_time):
            values = []
            for timeline in timelines:
                if t < len(timeline.points):
                    val = timeline.points[t].values.get(target_slot, 0)
                    values.append(val)
            
            if values:
                # Compute risk as variance
                mean = sum(values) / len(values)
                variance = sum((v - mean) ** 2 for v in values) / len(values)
                risk_level = min(1.0, variance / 100)  # Normalize
                
                # Determine color
                if risk_level < 0.3:
                    color = ImpactColor.GREEN
                elif risk_level < 0.7:
                    color = ImpactColor.YELLOW
                else:
                    color = ImpactColor.RED
                
                cell = RiskHeatmapCell(
                    slot_id=target_slot,
                    time=t,
                    risk_level=risk_level,
                    color=color,
                )
                cells.append(cell)
        
        return cells


# ============================================================================
# TIMELINE VISUALIZATION SYSTEM
# ============================================================================

class TimelineDivergenceVisualization:
    """
    Main timeline divergence visualization system.
    
    Per spec: Visually compare multiple simulated futures in XR
    """
    
    def __init__(self):
        self.builder = TimelineBuilder()
        self.detector = DivergenceDetector()
        self.heatmap = RiskHeatmapGenerator()
        
        self._timelines: Dict[str, Timeline] = {}
        self._current_time: int = 0
        self._visible_timelines: List[str] = []
    
    def add_timeline(
        self,
        scenario_id: str,
        name: str,
        data: List[Dict[str, float]],
        key_decisions: List[int] = None,
    ) -> Timeline:
        """Add a timeline"""
        timeline = self.builder.build_timeline(
            scenario_id, name, data, key_decisions
        )
        self._timelines[timeline.timeline_id] = timeline
        self._visible_timelines.append(timeline.timeline_id)
        
        logger.info(f"Added timeline {timeline.name}: {len(data)} points")
        return timeline
    
    def toggle_scenario(self, timeline_id: str) -> None:
        """
        Toggle scenario visibility.
        
        Per spec interaction: Toggle scenarios
        """
        if timeline_id in self._visible_timelines:
            self._visible_timelines.remove(timeline_id)
            logger.info(f"Hidden timeline {timeline_id}")
        else:
            self._visible_timelines.append(timeline_id)
            logger.info(f"Shown timeline {timeline_id}")
    
    def scrub_time(self, time: int) -> Dict[str, Any]:
        """
        Scrub to a specific time.
        
        Per spec interaction: Scrub time
        """
        self._current_time = time
        
        # Get values at this time for all visible timelines
        snapshot = {}
        for tid in self._visible_timelines:
            timeline = self._timelines.get(tid)
            if timeline and time < len(timeline.points):
                snapshot[timeline.name] = timeline.points[time].values
        
        return {
            "time": time,
            "snapshot": snapshot,
        }
    
    def inspect_delta(
        self,
        timeline_a_id: str,
        timeline_b_id: str,
    ) -> List[DivergenceMarker]:
        """
        Inspect delta causes between timelines.
        
        Per spec interaction: Inspect delta causes
        """
        timeline_a = self._timelines.get(timeline_a_id)
        timeline_b = self._timelines.get(timeline_b_id)
        
        if not timeline_a or not timeline_b:
            return []
        
        return self.detector.find_divergences(timeline_a, timeline_b)
    
    def get_key_decisions(self) -> List[Dict[str, Any]]:
        """
        Get all key decision points.
        
        Per spec: Key-decision anchors
        """
        decisions = []
        
        for timeline in self._timelines.values():
            for point in timeline.points:
                if point.is_key_decision:
                    decisions.append({
                        "timeline": timeline.name,
                        "time": point.time,
                        "values": point.values,
                    })
        
        return decisions
    
    def generate_risk_heatmap(
        self,
        target_slot: str,
    ) -> List[RiskHeatmapCell]:
        """Generate risk heatmap for a slot"""
        visible = [
            self._timelines[tid]
            for tid in self._visible_timelines
            if tid in self._timelines
        ]
        return self.heatmap.generate(visible, target_slot)
    
    def export_xr_manifest(self) -> Dict[str, Any]:
        """Export XR manifest for rendering"""
        return {
            "type": "timeline_divergence",
            "timelines": [
                {
                    "id": t.timeline_id,
                    "name": t.name,
                    "color": t.color,
                    "visible": t.timeline_id in self._visible_timelines,
                    "point_count": len(t.points),
                }
                for t in self._timelines.values()
            ],
            "current_time": self._current_time,
            "read_only": True,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_timeline_visualization() -> TimelineDivergenceVisualization:
    """Create timeline divergence visualization"""
    return TimelineDivergenceVisualization()
