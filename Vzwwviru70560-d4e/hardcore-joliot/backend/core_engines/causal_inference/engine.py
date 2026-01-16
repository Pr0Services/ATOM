"""
============================================================================
CHE·NU™ V69 — CAUSAL INFERENCE ENGINE
============================================================================
Spec: GPT1/CHE-NU_CAUSAL_INFERENCE_ENGINE.md

Purpose: Move from correlation-based simulation to causal reasoning.

Core Concept: DAGs to model cause → effect relationships.

Capabilities:
- Counterfactual analysis ("What if X had not happened?")
- Root-cause explanations
- Intervention simulation (do-calculus inspired)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import copy

from ..models import (
    Slot,
    CausalDAG,
    CausalEdge,
    EdgeType,
    Intervention,
    InterventionType,
    CounterfactualQuery,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# DAG BUILDER
# ============================================================================

class DAGBuilder:
    """Build causal DAGs"""
    
    def __init__(self):
        self._current_dag: Optional[CausalDAG] = None
    
    def new_dag(self, name: str) -> 'DAGBuilder':
        """Start building a new DAG"""
        self._current_dag = CausalDAG(
            dag_id=generate_id(),
            name=name,
        )
        return self
    
    def add_slot(
        self,
        name: str,
        value: float = 0.0,
        unit: str = "",
    ) -> 'DAGBuilder':
        """Add a slot to the DAG"""
        if not self._current_dag:
            raise ValueError("No DAG started")
        
        slot = Slot(
            slot_id=generate_id(),
            name=name,
            value=value,
            unit=unit,
        )
        self._current_dag.slots[name] = slot
        return self
    
    def add_edge(
        self,
        source: str,
        target: str,
        strength: float = 0.5,
        edge_type: EdgeType = EdgeType.DIRECT,
    ) -> 'DAGBuilder':
        """Add a causal edge"""
        if not self._current_dag:
            raise ValueError("No DAG started")
        
        edge = CausalEdge(
            edge_id=generate_id(),
            source_slot=source,
            target_slot=target,
            edge_type=edge_type,
            strength=strength,
        )
        self._current_dag.edges.append(edge)
        
        # Update slot parents/children
        if source in self._current_dag.slots:
            self._current_dag.slots[source].causal_children.append(target)
        if target in self._current_dag.slots:
            self._current_dag.slots[target].causal_parents.append(source)
        
        return self
    
    def build(self) -> CausalDAG:
        """Build and return the DAG"""
        if not self._current_dag:
            raise ValueError("No DAG started")
        
        dag = self._current_dag
        self._current_dag = None
        return dag


# ============================================================================
# CAUSAL INFERENCE ENGINE
# ============================================================================

class CausalInferenceEngine:
    """
    Engine for causal inference and reasoning.
    
    Per spec: DAG layer attached to WorldEngine
    """
    
    def __init__(self):
        self._dags: Dict[str, CausalDAG] = {}
        self._interventions: List[Intervention] = []
    
    def register_dag(self, dag: CausalDAG) -> None:
        """Register a causal DAG"""
        self._dags[dag.dag_id] = dag
        logger.info(f"Registered DAG {dag.dag_id}: {dag.name}")
    
    def get_dag(self, dag_id: str) -> Optional[CausalDAG]:
        """Get DAG by ID"""
        return self._dags.get(dag_id)
    
    def get_parents(self, dag_id: str, slot_name: str) -> List[str]:
        """Get causal parents of a slot"""
        dag = self._dags.get(dag_id)
        if not dag or slot_name not in dag.slots:
            return []
        
        return dag.slots[slot_name].causal_parents
    
    def get_children(self, dag_id: str, slot_name: str) -> List[str]:
        """Get causal children of a slot"""
        dag = self._dags.get(dag_id)
        if not dag or slot_name not in dag.slots:
            return []
        
        return dag.slots[slot_name].causal_children
    
    def find_root_causes(
        self,
        dag_id: str,
        target_slot: str,
    ) -> List[str]:
        """
        Find root causes (nodes with no parents) affecting target.
        
        Per spec: Root-cause explanations
        """
        dag = self._dags.get(dag_id)
        if not dag:
            return []
        
        # BFS backwards to find roots
        visited = set()
        roots = []
        queue = [target_slot]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            if current in dag.slots:
                parents = dag.slots[current].causal_parents
                if not parents:
                    roots.append(current)
                else:
                    queue.extend(parents)
        
        return roots
    
    def trace_causal_path(
        self,
        dag_id: str,
        source: str,
        target: str,
    ) -> List[List[str]]:
        """Find all causal paths from source to target"""
        dag = self._dags.get(dag_id)
        if not dag:
            return []
        
        paths = []
        self._dfs_paths(dag, source, target, [source], paths)
        return paths
    
    def _dfs_paths(
        self,
        dag: CausalDAG,
        current: str,
        target: str,
        path: List[str],
        paths: List[List[str]],
    ) -> None:
        """DFS to find all paths"""
        if current == target:
            paths.append(path.copy())
            return
        
        if current not in dag.slots:
            return
        
        for child in dag.slots[current].causal_children:
            if child not in path:  # Avoid cycles
                path.append(child)
                self._dfs_paths(dag, child, target, path, paths)
                path.pop()
    
    def do_intervention(
        self,
        dag_id: str,
        slot_name: str,
        new_value: float,
        approver_id: str = "",
    ) -> Tuple[CausalDAG, Intervention]:
        """
        Apply do(X) intervention.
        
        Per spec: Intervention simulation (do-calculus)
        """
        dag = self._dags.get(dag_id)
        if not dag:
            raise ValueError(f"DAG {dag_id} not found")
        
        # Create intervention
        intervention = Intervention(
            intervention_id=generate_id(),
            slot_id=slot_name,
            intervention_type=InterventionType.DO,
            new_value=new_value,
            approved=bool(approver_id),
            approver_id=approver_id,
        )
        
        # Create modified DAG (do(X) removes incoming edges)
        modified_dag = copy.deepcopy(dag)
        modified_dag.dag_id = f"{dag_id}_do_{slot_name}"
        
        # Set the value
        if slot_name in modified_dag.slots:
            modified_dag.slots[slot_name].value = new_value
            # Remove incoming edges (do-calculus)
            modified_dag.slots[slot_name].causal_parents = []
        
        # Remove edges pointing to this slot
        modified_dag.edges = [
            e for e in modified_dag.edges
            if e.target_slot != slot_name
        ]
        
        self._interventions.append(intervention)
        
        logger.info(f"Applied do({slot_name}={new_value}) intervention")
        return modified_dag, intervention
    
    def propagate_effect(
        self,
        dag: CausalDAG,
        changed_slot: str,
    ) -> Dict[str, float]:
        """
        Propagate causal effect through the DAG.
        
        Returns estimated effects on downstream slots.
        """
        effects = {}
        
        if changed_slot not in dag.slots:
            return effects
        
        source_value = dag.slots[changed_slot].value
        
        # BFS forward propagation
        queue = [(changed_slot, 1.0)]  # (slot, cumulative_strength)
        visited = set()
        
        while queue:
            current, strength = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            # Find outgoing edges
            for edge in dag.edges:
                if edge.source_slot == current:
                    effect = strength * edge.strength
                    effects[edge.target_slot] = effect
                    
                    queue.append((edge.target_slot, effect))
        
        return effects
    
    def counterfactual_query(
        self,
        dag_id: str,
        query: CounterfactualQuery,
    ) -> Dict[str, Any]:
        """
        Answer counterfactual query.
        
        Per spec: "What if X had not happened?"
        """
        dag = self._dags.get(dag_id)
        if not dag:
            return {"error": "DAG not found"}
        
        # Apply counterfactual intervention
        modified_dag, _ = self.do_intervention(
            dag_id,
            query.intervention.slot_id,
            query.intervention.new_value,
        )
        
        # Propagate effects
        effects = self.propagate_effect(
            modified_dag,
            query.intervention.slot_id,
        )
        
        # Get target effect
        target_effect = effects.get(query.target_slot, 0)
        
        return {
            "query_id": query.query_id,
            "question": query.question,
            "intervention": {
                "slot": query.intervention.slot_id,
                "value": query.intervention.new_value,
            },
            "target_slot": query.target_slot,
            "estimated_effect": target_effect,
            "all_effects": effects,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_inference_engine() -> CausalInferenceEngine:
    """Create causal inference engine"""
    return CausalInferenceEngine()


def create_dag_builder() -> DAGBuilder:
    """Create DAG builder"""
    return DAGBuilder()


def create_intervention(
    slot_id: str,
    new_value: float,
    intervention_type: InterventionType = InterventionType.DO,
) -> Intervention:
    """Create intervention"""
    return Intervention(
        intervention_id=generate_id(),
        slot_id=slot_id,
        intervention_type=intervention_type,
        new_value=new_value,
    )
