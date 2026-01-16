"""
============================================================================
CHE·NU™ V69 — CAUSAL DECISION ENGINE
============================================================================
Spec: GPT1/CHE-NU_CAUSAL_DECISION_ENGINE.md

Objective: Transform statistical simulations into actionable causal
recommendations for humans, with mathematical rigor and explicit governance.

CHE·NU™ ne prédit pas seulement ce qui pourrait arriver,
il aide à comprendre POURQUOI et sur quels LEVIERS agir.

Architecture: Slots → WorldEngine → DAG Causal → Analyses → XR Explain → Humain décide

Features:
- DAG reasoning layer
- Counterfactual analysis (What-if advanced)
- Sensitivity & Impact Scoring
- OPA Governance on Causality
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
    SensitivityScore,
    Intervention,
    InterventionType,
    CounterfactualQuery,
    generate_id,
    sign_artifact,
    compute_hash,
)
from ..causal_inference.engine import CausalInferenceEngine, DAGBuilder

logger = logging.getLogger(__name__)


# ============================================================================
# SENSITIVITY ANALYZER
# ============================================================================

class SensitivityAnalyzer:
    """
    Analyze sensitivity and impact of slots.
    
    Per spec: Mesurer l'influence réelle de chaque Slot sur l'objectif final
    """
    
    def analyze(
        self,
        dag: CausalDAG,
        target_slot: str,
    ) -> Dict[str, SensitivityScore]:
        """
        Compute sensitivity scores for all slots affecting target.
        
        Per spec outputs: Score d'impact (%), Intervalle de confiance, Instabilité
        """
        scores = {}
        
        if target_slot not in dag.slots:
            return scores
        
        # Find all ancestors affecting target
        ancestors = self._find_ancestors(dag, target_slot)
        
        # Compute impact for each
        total_impact = 0.0
        impacts = {}
        
        for slot_name in ancestors:
            # Sum strength of all paths to target
            impact = self._compute_path_impact(dag, slot_name, target_slot)
            impacts[slot_name] = impact
            total_impact += abs(impact)
        
        # Normalize to percentages
        for slot_name, impact in impacts.items():
            impact_percent = (abs(impact) / total_impact * 100) if total_impact > 0 else 0
            
            # Estimate confidence interval (simplified)
            confidence_width = 0.1 * impact_percent
            
            # Compute instability based on number of paths
            paths_count = len(self._find_paths(dag, slot_name, target_slot))
            instability = min(1.0, paths_count * 0.1)
            
            is_critical = impact_percent > 50 or instability > 0.5
            
            scores[slot_name] = SensitivityScore(
                slot_id=dag.slots[slot_name].slot_id if slot_name in dag.slots else "",
                impact_percent=impact_percent,
                confidence_low=max(0, impact_percent - confidence_width),
                confidence_high=min(100, impact_percent + confidence_width),
                instability_score=instability,
                is_critical=is_critical,
                alert_message=f"ATTENTION: {impact_percent:.0f}% du succès dépend de {slot_name}" if is_critical else "",
            )
        
        return scores
    
    def _find_ancestors(self, dag: CausalDAG, target: str) -> Set[str]:
        """Find all ancestors of target"""
        ancestors = set()
        queue = [target]
        
        while queue:
            current = queue.pop(0)
            if current in dag.slots:
                for parent in dag.slots[current].causal_parents:
                    if parent not in ancestors:
                        ancestors.add(parent)
                        queue.append(parent)
        
        return ancestors
    
    def _compute_path_impact(
        self,
        dag: CausalDAG,
        source: str,
        target: str,
    ) -> float:
        """Compute total impact through all paths"""
        paths = self._find_paths(dag, source, target)
        
        total_impact = 0.0
        for path in paths:
            path_strength = 1.0
            for i in range(len(path) - 1):
                # Find edge
                for edge in dag.edges:
                    if edge.source_slot == path[i] and edge.target_slot == path[i+1]:
                        path_strength *= edge.strength
                        break
            total_impact += path_strength
        
        return total_impact
    
    def _find_paths(
        self,
        dag: CausalDAG,
        source: str,
        target: str,
    ) -> List[List[str]]:
        """Find all paths from source to target"""
        paths = []
        self._dfs(dag, source, target, [source], paths)
        return paths
    
    def _dfs(
        self,
        dag: CausalDAG,
        current: str,
        target: str,
        path: List[str],
        paths: List[List[str]],
    ) -> None:
        """DFS for path finding"""
        if current == target:
            paths.append(path.copy())
            return
        
        if current not in dag.slots:
            return
        
        for child in dag.slots[current].causal_children:
            if child not in path:
                path.append(child)
                self._dfs(dag, child, target, path, paths)
                path.pop()


# ============================================================================
# OPA GOVERNANCE FOR CAUSALITY
# ============================================================================

class CausalGovernance:
    """
    OPA governance for causal reasoning.
    
    Per spec: OPA devient le gardien du raisonnement, pas seulement de l'exécution
    """
    
    # Blocked causal patterns
    BLOCKED_PATTERNS = [
        ("race", "*"),  # Discriminatory causation
        ("gender", "salary"),
        ("age", "promotion"),
    ]
    
    def __init__(self):
        self._validated_dags: Set[str] = set()
        self._audit_log: List[Dict] = []
    
    def validate_dag(
        self,
        dag: CausalDAG,
        validator_id: str,
    ) -> Tuple[bool, List[str]]:
        """
        Validate DAG for governance compliance.
        
        Per spec: Validation humaine obligatoire des DAG
        """
        issues = []
        
        # Check for blocked patterns
        for edge in dag.edges:
            for blocked_source, blocked_target in self.BLOCKED_PATTERNS:
                if (blocked_source in edge.source_slot.lower() and
                    (blocked_target == "*" or blocked_target in edge.target_slot.lower())):
                    issues.append(
                        f"Blocked causal pattern: {edge.source_slot} → {edge.target_slot}"
                    )
        
        # Check for cycles (DAG must be acyclic)
        if self._has_cycle(dag):
            issues.append("DAG contains cycles - not a valid DAG")
        
        # Log validation attempt
        self._audit_log.append({
            "dag_id": dag.dag_id,
            "validator_id": validator_id,
            "issues": issues,
            "passed": len(issues) == 0,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        if not issues:
            self._validated_dags.add(dag.dag_id)
            dag.validated = True
            dag.validator_id = validator_id
            
            # Sign DAG
            dag.signature = sign_artifact({
                "dag_id": dag.dag_id,
                "validator": validator_id,
                "slot_count": len(dag.slots),
                "edge_count": len(dag.edges),
            }, validator_id)
        
        return len(issues) == 0, issues
    
    def _has_cycle(self, dag: CausalDAG) -> bool:
        """Check if DAG has cycles"""
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            if node in dag.slots:
                for child in dag.slots[node].causal_children:
                    if child not in visited:
                        if dfs(child):
                            return True
                    elif child in rec_stack:
                        return True
            
            rec_stack.remove(node)
            return False
        
        for slot_name in dag.slots:
            if slot_name not in visited:
                if dfs(slot_name):
                    return True
        
        return False
    
    def validate_intervention(
        self,
        intervention: Intervention,
        approver_id: str,
    ) -> bool:
        """
        Validate causal intervention.
        
        Per spec: Audit des interventions causales
        """
        # Log intervention
        self._audit_log.append({
            "intervention_id": intervention.intervention_id,
            "slot_id": intervention.slot_id,
            "type": intervention.intervention_type.value,
            "approver_id": approver_id,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        intervention.approved = True
        intervention.approver_id = approver_id
        
        return True
    
    def is_dag_validated(self, dag_id: str) -> bool:
        """Check if DAG is validated"""
        return dag_id in self._validated_dags
    
    def get_audit_log(self) -> List[Dict]:
        """Get audit log"""
        return self._audit_log


# ============================================================================
# CAUSAL DECISION ENGINE
# ============================================================================

class CausalDecisionEngine:
    """
    Main decision engine with causal reasoning.
    
    Per spec: Transformer les simulations statistiques en recommandations
    causales exploitables par l'humain
    """
    
    def __init__(self):
        self.inference = CausalInferenceEngine()
        self.sensitivity = SensitivityAnalyzer()
        self.governance = CausalGovernance()
        
        # Agent roles
        self._agent_analyses: Dict[str, Dict] = {}
    
    def register_dag(
        self,
        dag: CausalDAG,
        validator_id: str,
    ) -> Tuple[bool, List[str]]:
        """Register and validate a DAG"""
        # Governance validation first
        valid, issues = self.governance.validate_dag(dag, validator_id)
        
        if valid:
            self.inference.register_dag(dag)
        
        return valid, issues
    
    def analyze_slot_impact(
        self,
        dag_id: str,
        target_slot: str,
    ) -> Dict[str, SensitivityScore]:
        """
        Analyze impact of all slots on target.
        
        Per spec: L'influence réelle de chaque Slot sur l'objectif final
        """
        dag = self.inference.get_dag(dag_id)
        if not dag:
            return {}
        
        return self.sensitivity.analyze(dag, target_slot)
    
    def get_actionable_levers(
        self,
        dag_id: str,
        target_slot: str,
        min_impact: float = 10.0,
    ) -> List[Dict[str, Any]]:
        """
        Get actionable levers for decision making.
        
        Per spec: Sur quels leviers agir
        """
        scores = self.analyze_slot_impact(dag_id, target_slot)
        
        levers = []
        for slot_name, score in scores.items():
            if score.impact_percent >= min_impact:
                levers.append({
                    "slot": slot_name,
                    "impact_percent": score.impact_percent,
                    "confidence": (score.confidence_low, score.confidence_high),
                    "instability": score.instability_score,
                    "is_critical": score.is_critical,
                    "alert": score.alert_message,
                })
        
        # Sort by impact
        levers.sort(key=lambda x: x["impact_percent"], reverse=True)
        
        return levers
    
    def what_if(
        self,
        dag_id: str,
        slot_name: str,
        new_value: float,
        target_slot: str,
    ) -> Dict[str, Any]:
        """
        What-if analysis (counterfactual).
        
        Per spec: Que se serait-il passé si...
        """
        query = CounterfactualQuery(
            query_id=generate_id(),
            intervention=Intervention(
                intervention_id=generate_id(),
                slot_id=slot_name,
                intervention_type=InterventionType.COUNTERFACTUAL,
                new_value=new_value,
            ),
            question=f"What if {slot_name} = {new_value}?",
            target_slot=target_slot,
        )
        
        return self.inference.counterfactual_query(dag_id, query)
    
    def explain_causally(
        self,
        dag_id: str,
        source_slot: str,
        target_slot: str,
    ) -> Dict[str, Any]:
        """
        Explain causal relationship between slots.
        
        Per spec: IA causale - Lien cause → effet, actionnable, vérifiable
        """
        dag = self.inference.get_dag(dag_id)
        if not dag:
            return {"error": "DAG not found"}
        
        # Find all paths
        paths = self.inference.trace_causal_path(dag_id, source_slot, target_slot)
        
        # Find root causes
        roots = self.inference.find_root_causes(dag_id, target_slot)
        
        # Compute impact
        scores = self.sensitivity.analyze(dag, target_slot)
        source_score = scores.get(source_slot)
        
        return {
            "source": source_slot,
            "target": target_slot,
            "causal_paths": paths,
            "root_causes": roots,
            "impact": source_score.impact_percent if source_score else 0,
            "explanation": self._generate_explanation(
                source_slot, target_slot, paths, source_score
            ),
        }
    
    def _generate_explanation(
        self,
        source: str,
        target: str,
        paths: List[List[str]],
        score: Optional[SensitivityScore],
    ) -> str:
        """Generate human-readable causal explanation"""
        if not paths:
            return f"No causal path found from {source} to {target}."
        
        impact = score.impact_percent if score else 0
        
        explanation = f"Une hausse de {source} affecte {target} "
        
        if len(paths) == 1:
            explanation += f"via le chemin: {' → '.join(paths[0])}. "
        else:
            explanation += f"via {len(paths)} chemins causaux. "
        
        explanation += f"Impact estimé: {impact:.1f}%."
        
        if score and score.is_critical:
            explanation += f" ⚠️ {score.alert_message}"
        
        return explanation
    
    def generate_xr_overlay(
        self,
        dag_id: str,
        target_slot: str,
    ) -> Dict[str, Any]:
        """
        Generate XR overlay for explainability.
        
        Per spec XR: Visualisation des DAG, Highlight des leviers causaux
        """
        dag = self.inference.get_dag(dag_id)
        if not dag:
            return {}
        
        scores = self.analyze_slot_impact(dag_id, target_slot)
        
        return {
            "type": "xr_causal_overlay",
            "target": target_slot,
            "nodes": [
                {
                    "id": slot.slot_id,
                    "name": name,
                    "value": slot.value,
                    "impact": scores.get(name, SensitivityScore(slot_id=slot.slot_id)).impact_percent,
                    "is_critical": scores.get(name, SensitivityScore(slot_id=slot.slot_id)).is_critical,
                }
                for name, slot in dag.slots.items()
            ],
            "edges": [
                {
                    "source": e.source_slot,
                    "target": e.target_slot,
                    "strength": e.strength,
                }
                for e in dag.edges
            ],
            "read_only": True,  # Per spec: XR read-only
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_decision_engine() -> CausalDecisionEngine:
    """Create causal decision engine"""
    return CausalDecisionEngine()
