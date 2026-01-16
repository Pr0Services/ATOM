"""
============================================================================
CHE·NU™ V69 — XR CAUSAL TRACE VISUALIZATION
============================================================================
Spec: GPT1/CHE-NU_XR_CAUSAL_TRACE_VISUALIZATION.md

Features:
1. Causal Path (Fil d'Ariane) - Luminous links
2. Nœuds d'Incertitude - Pulsing cloud spheres
3. Mode Intervention Virtuelle (do) - do(X) visualization
4. Heatmap Contrefactuelle - Gains/losses overlay

Interactions:
- Point link → L2 explanation
- Open uncertainty node → missing slots
- Grab parameter → apply do(X)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import copy

from ..models import (
    CausalPath,
    UncertaintyNode,
    ConterfactualHeatmap,
    RiskHeatmapCell,
    ImpactColor,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CAUSAL PATH RENDERER
# ============================================================================

class CausalPathRenderer:
    """
    Render causal paths as luminous threads.
    
    Per spec: Liens lumineux entre causes et effets
    """
    
    def __init__(self):
        self._paths: List[CausalPath] = []
    
    def add_path(
        self,
        source_slot: str,
        target_slot: str,
        strength: float,
        certainty: float,
        intermediate_nodes: List[str] = None,
    ) -> CausalPath:
        """
        Add a causal path.
        
        Per spec: Épaisseur = force causale, Intensité = certitude
        """
        path = CausalPath(
            path_id=generate_id(),
            source_slot=source_slot,
            target_slot=target_slot,
            thickness=max(0.1, min(5.0, strength * 5)),  # Scale to visual
            intensity=max(0.1, min(1.0, certainty)),
            path_nodes=intermediate_nodes or [],
        )
        
        self._paths.append(path)
        return path
    
    def get_explanation(
        self,
        path_id: str,
        variation_percent: float,
    ) -> str:
        """
        Get L2 explanation for a path.
        
        Per spec: Pointer un lien → explication L2:
        "Si X varie de -5%, impact final = -12%"
        """
        path = next((p for p in self._paths if p.path_id == path_id), None)
        if not path:
            return "Path not found"
        
        # Calculate impact based on strength
        impact = variation_percent * path.thickness / 2
        
        return (f"Si {path.source_slot} varie de {variation_percent:+.1f}%, "
                f"impact sur {path.target_slot} = {impact:+.1f}%")
    
    def get_all_paths(self) -> List[CausalPath]:
        """Get all paths"""
        return self._paths
    
    def render_manifest(self) -> Dict[str, Any]:
        """Get render manifest for paths"""
        return {
            "type": "causal_threads",
            "paths": [
                {
                    "id": p.path_id,
                    "source": p.source_slot,
                    "target": p.target_slot,
                    "thickness": p.thickness,
                    "intensity": p.intensity,
                    "nodes": p.path_nodes,
                    "material": "luminous",
                }
                for p in self._paths
            ],
        }


# ============================================================================
# UNCERTAINTY NODE MANAGER
# ============================================================================

class UncertaintyNodeManager:
    """
    Manage uncertainty nodes.
    
    Per spec: Sphères nuageuses pulsantes - hypothèses non stabilisées
    """
    
    def __init__(self):
        self._nodes: Dict[str, UncertaintyNode] = {}
    
    def add_node(
        self,
        slot_id: str,
        missing_slots: List[str],
        pulse_rate: float = 1.0,
    ) -> UncertaintyNode:
        """Add an uncertainty node"""
        node = UncertaintyNode(
            node_id=generate_id(),
            slot_id=slot_id,
            missing_slots=missing_slots,
            pulse_rate=pulse_rate,
            cloud_density=0.3 + 0.1 * len(missing_slots),  # More missing = denser
        )
        
        self._nodes[node.node_id] = node
        return node
    
    def open_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Open a node to see missing data.
        
        Per spec: Ouvrir le nœud → slots manquants, Invitation à enrichir données
        """
        node = self._nodes.get(node_id)
        if not node:
            return None
        
        return {
            "node_id": node.node_id,
            "slot_id": node.slot_id,
            "missing_slots": node.missing_slots,
            "message": f"Pour stabiliser {node.slot_id}, enrichissez: {', '.join(node.missing_slots)}",
        }
    
    def get_all_nodes(self) -> List[UncertaintyNode]:
        """Get all uncertainty nodes"""
        return list(self._nodes.values())
    
    def render_manifest(self) -> Dict[str, Any]:
        """Get render manifest for uncertainty nodes"""
        return {
            "type": "uncertainty_clouds",
            "nodes": [
                {
                    "id": n.node_id,
                    "slot": n.slot_id,
                    "missing_count": len(n.missing_slots),
                    "pulse_rate": n.pulse_rate,
                    "cloud_density": n.cloud_density,
                    "material": "cloud_pulsing",
                }
                for n in self._nodes.values()
            ],
        }


# ============================================================================
# DO INTERVENTION VISUALIZER
# ============================================================================

class DoInterventionVisualizer:
    """
    Visualize do(X) interventions.
    
    Per spec: Mode Intervention Virtuelle (do)
    """
    
    def __init__(self):
        self._base_state: Dict[str, float] = {}
        self._modified_state: Dict[str, float] = {}
        self._active_intervention: Optional[str] = None
    
    def set_base_state(self, state: Dict[str, float]) -> None:
        """Set the base world state"""
        self._base_state = copy.deepcopy(state)
        self._modified_state = copy.deepcopy(state)
    
    def apply_do(
        self,
        slot_id: str,
        new_value: float,
        propagation_map: Dict[str, float] = None,
    ) -> Dict[str, float]:
        """
        Apply do(X) intervention.
        
        Per spec: Geste de saisie d'un paramètre → Application intervention causale
        """
        self._active_intervention = slot_id
        self._modified_state = copy.deepcopy(self._base_state)
        
        # Set the intervention value
        self._modified_state[slot_id] = new_value
        
        # Propagate effects
        propagation_map = propagation_map or {}
        for target, strength in propagation_map.items():
            if target in self._modified_state:
                delta = (new_value - self._base_state.get(slot_id, 0)) * strength
                self._modified_state[target] += delta
        
        logger.info(f"Applied do({slot_id}={new_value})")
        return self._modified_state
    
    def get_comparison(self) -> Dict[str, Any]:
        """
        Get base vs modified comparison.
        
        Per spec: Comparaison monde base vs monde modifié
        """
        comparison = {}
        
        for slot in set(self._base_state.keys()) | set(self._modified_state.keys()):
            base_val = self._base_state.get(slot, 0)
            mod_val = self._modified_state.get(slot, 0)
            
            comparison[slot] = {
                "base": base_val,
                "modified": mod_val,
                "delta": mod_val - base_val,
                "changed": base_val != mod_val,
            }
        
        return comparison
    
    def render_manifest(self) -> Dict[str, Any]:
        """Get render manifest"""
        return {
            "type": "do_intervention",
            "active_intervention": self._active_intervention,
            "comparison": self.get_comparison(),
            "mode": "split_view",  # Base on left, modified on right
        }


# ============================================================================
# COUNTERFACTUAL HEATMAP
# ============================================================================

class CounterfactualHeatmapGenerator:
    """
    Generate counterfactual heatmaps.
    
    Per spec: Heatmap Contrefactuelle - Vert: gains, Rouge: effets négatifs
    """
    
    def generate(
        self,
        base_state: Dict[str, float],
        modified_state: Dict[str, float],
    ) -> ConterfactualHeatmap:
        """Generate heatmap from state comparison"""
        cells = []
        
        for slot in set(base_state.keys()) | set(modified_state.keys()):
            base_val = base_state.get(slot, 0)
            mod_val = modified_state.get(slot, 0)
            
            delta = mod_val - base_val
            
            # Determine color
            if delta > 0:
                color = ImpactColor.GREEN
            elif delta < 0:
                color = ImpactColor.RED
            else:
                color = ImpactColor.YELLOW
            
            # Risk level = magnitude of change
            risk = min(1.0, abs(delta) / max(1, abs(base_val)))
            
            cell = RiskHeatmapCell(
                slot_id=slot,
                time=0,  # Current state
                risk_level=risk,
                color=color,
            )
            cells.append(cell)
        
        heatmap = ConterfactualHeatmap(
            heatmap_id=generate_id(),
            base_state=base_state,
            modified_state=modified_state,
            cells=cells,
        )
        
        return heatmap
    
    def get_compromise_summary(
        self,
        heatmap: ConterfactualHeatmap,
    ) -> Dict[str, Any]:
        """
        Get decision compromise summary.
        
        Per spec: Lecture immédiate du compromis décisionnel
        """
        gains = [c for c in heatmap.cells if c.color == ImpactColor.GREEN]
        losses = [c for c in heatmap.cells if c.color == ImpactColor.RED]
        neutral = [c for c in heatmap.cells if c.color == ImpactColor.YELLOW]
        
        return {
            "gains_count": len(gains),
            "losses_count": len(losses),
            "neutral_count": len(neutral),
            "net_impact": len(gains) - len(losses),
            "summary": (
                f"{len(gains)} gains, {len(losses)} effets négatifs. "
                f"Impact net: {'positif' if len(gains) > len(losses) else 'négatif' if len(losses) > len(gains) else 'neutre'}"
            ),
        }


# ============================================================================
# CAUSAL TRACE VISUALIZATION SYSTEM
# ============================================================================

class CausalTraceVisualization:
    """
    Main causal trace visualization system.
    
    Per spec: XR Causal Trace Visualization
    """
    
    def __init__(self):
        self.paths = CausalPathRenderer()
        self.uncertainty = UncertaintyNodeManager()
        self.do_viz = DoInterventionVisualizer()
        self.heatmap_gen = CounterfactualHeatmapGenerator()
        
        self._current_heatmap: Optional[ConterfactualHeatmap] = None
    
    def add_causal_path(
        self,
        source: str,
        target: str,
        strength: float,
        certainty: float,
    ) -> CausalPath:
        """Add a causal path"""
        return self.paths.add_path(source, target, strength, certainty)
    
    def add_uncertainty(
        self,
        slot_id: str,
        missing: List[str],
    ) -> UncertaintyNode:
        """Add an uncertainty node"""
        return self.uncertainty.add_node(slot_id, missing)
    
    def set_world_state(self, state: Dict[str, float]) -> None:
        """Set the base world state"""
        self.do_viz.set_base_state(state)
    
    def apply_intervention(
        self,
        slot_id: str,
        new_value: float,
        propagation: Dict[str, float] = None,
    ) -> Dict[str, Any]:
        """Apply a do(X) intervention"""
        modified = self.do_viz.apply_do(slot_id, new_value, propagation)
        
        # Generate heatmap
        self._current_heatmap = self.heatmap_gen.generate(
            self.do_viz._base_state,
            modified,
        )
        
        return {
            "modified_state": modified,
            "heatmap": self._current_heatmap,
            "compromise": self.heatmap_gen.get_compromise_summary(self._current_heatmap),
        }
    
    def point_at_link(
        self,
        path_id: str,
        variation: float,
    ) -> str:
        """Point at a causal link for explanation"""
        return self.paths.get_explanation(path_id, variation)
    
    def inspect_uncertainty(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Inspect an uncertainty node"""
        return self.uncertainty.open_node(node_id)
    
    def get_full_manifest(self) -> Dict[str, Any]:
        """Get complete XR manifest"""
        return {
            "type": "causal_trace_visualization",
            "layers": {
                "causal_threads": self.paths.render_manifest(),
                "uncertainty_clouds": self.uncertainty.render_manifest(),
                "do_intervention": self.do_viz.render_manifest(),
            },
            "heatmap_active": self._current_heatmap is not None,
            "read_only": True,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_causal_trace_viz() -> CausalTraceVisualization:
    """Create causal trace visualization"""
    return CausalTraceVisualization()
