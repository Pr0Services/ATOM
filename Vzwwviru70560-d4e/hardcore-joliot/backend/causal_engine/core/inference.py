"""
============================================================================
CHE·NU™ V69 — CAUSAL INFERENCE ENGINE
============================================================================
Version: 1.0.0
Purpose: Estimate causal effects, sensitivity, and provide decision support
Principle: GOUVERNANCE > EXÉCUTION - Analyze, don't decide
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import random
import math

from .models import (
    CausalDAG,
    CausalNode,
    CausalEdge,
    CausalQuery,
    CausalEffect,
    SensitivityScore,
    Intervention,
    InterventionType,
    ConfidenceLevel,
    NodeType,
    ValidationStatus,
)

logger = logging.getLogger(__name__)


# ============================================================================
# ADJUSTMENT SET FINDER
# ============================================================================

class AdjustmentSetFinder:
    """
    Find valid adjustment sets for causal effect estimation.
    Implements backdoor criterion.
    """
    
    def __init__(self, dag: CausalDAG):
        self.dag = dag
    
    def find_backdoor_set(
        self,
        treatment: str,
        outcome: str,
    ) -> Optional[List[str]]:
        """
        Find a minimal adjustment set using backdoor criterion.
        
        A valid adjustment set Z satisfies:
        1. No node in Z is a descendant of treatment
        2. Z blocks all backdoor paths from treatment to outcome
        """
        # Get descendants of treatment (cannot be in adjustment set)
        treatment_descendants = self.dag.get_descendants(treatment)
        
        # Get all nodes that are not descendants of treatment
        candidates = [
            node_id for node_id in self.dag.nodes
            if node_id not in treatment_descendants
            and node_id != treatment
            and node_id != outcome
        ]
        
        # Get parents of treatment (good candidates)
        treatment_parents = self.dag.get_parents(treatment)
        
        # Start with parents as adjustment set
        adjustment_set = [p for p in treatment_parents if p in candidates]
        
        # Simple heuristic: add confounders
        for node_id, node in self.dag.nodes.items():
            if node.node_type == NodeType.CONFOUNDER and node_id in candidates:
                if node_id not in adjustment_set:
                    adjustment_set.append(node_id)
        
        return adjustment_set if adjustment_set else None
    
    def find_frontdoor_set(
        self,
        treatment: str,
        outcome: str,
    ) -> Optional[List[str]]:
        """
        Find a frontdoor adjustment set.
        
        Valid when:
        1. Mediator M intercepts all directed paths from treatment to outcome
        2. No unblocked backdoor path from treatment to M
        3. All backdoor paths from M to outcome blocked by treatment
        """
        # Find mediators between treatment and outcome
        treatment_children = self.dag.get_children(treatment)
        outcome_parents = self.dag.get_parents(outcome)
        
        # Intersection = potential mediators
        mediators = [
            node_id for node_id in treatment_children
            if node_id in self.dag.get_ancestors(outcome)
        ]
        
        if not mediators:
            return None
        
        # Return first valid mediator set
        for mediator in mediators:
            node = self.dag.nodes.get(mediator)
            if node and node.node_type == NodeType.MEDIATOR:
                return [mediator]
        
        return mediators[:1] if mediators else None


# ============================================================================
# EFFECT ESTIMATOR
# ============================================================================

class CausalEffectEstimator:
    """
    Estimate causal effects from DAG and data.
    
    NOTE: This is a simplified mock implementation.
    Production would use DoWhy for proper estimation.
    """
    
    def __init__(self, dag: CausalDAG):
        self.dag = dag
        self.adjustment_finder = AdjustmentSetFinder(dag)
    
    def estimate_ate(
        self,
        treatment: str,
        outcome: str,
        data: Optional[Dict[str, List[float]]] = None,
    ) -> CausalEffect:
        """
        Estimate Average Treatment Effect (ATE).
        
        ATE = E[Y | do(X=1)] - E[Y | do(X=0)]
        """
        query = CausalQuery(
            dag_id=self.dag.id,
            query_type="ate",
            treatment=treatment,
            outcome=outcome,
            synthetic=True,
        )
        
        # Find adjustment set
        adjustment_set = self.adjustment_finder.find_backdoor_set(treatment, outcome)
        
        if adjustment_set is None:
            logger.warning(f"No valid adjustment set for {treatment} -> {outcome}")
        
        # Get edge coefficient if available
        edge = self._find_edge(treatment, outcome)
        
        if edge and edge.coefficient is not None:
            # Use edge coefficient as effect estimate
            ate = edge.coefficient
            std_error = abs(ate) * 0.1  # Mock: 10% standard error
        else:
            # Mock estimation from data
            ate = self._mock_estimate(treatment, outcome, data)
            std_error = abs(ate) * 0.2  # Higher uncertainty
        
        # Confidence interval (mock: 95% CI)
        ci_lower = ate - 1.96 * std_error
        ci_upper = ate + 1.96 * std_error
        
        # Significance
        p_value = self._mock_p_value(ate, std_error)
        is_significant = p_value < 0.05
        
        return CausalEffect(
            query_id=query.id,
            ate=ate,
            confidence_interval=(ci_lower, ci_upper),
            p_value=p_value,
            standard_error=std_error,
            estimator="backdoor_adjustment" if adjustment_set else "naive",
            is_significant=is_significant,
            effect_size_interpretation=self._interpret_effect(ate),
        )
    
    def estimate_with_intervention(
        self,
        intervention: Intervention,
        outcome: str,
        baseline_value: Optional[float] = None,
    ) -> CausalEffect:
        """Estimate effect of a specific intervention"""
        query = CausalQuery(
            dag_id=self.dag.id,
            query_type="intervention",
            treatment=intervention.node_id,
            outcome=outcome,
            interventions=[intervention],
            synthetic=True,
        )
        
        # Get baseline effect
        base_effect = self.estimate_ate(intervention.node_id, outcome)
        
        # Scale by intervention magnitude
        if intervention.value is not None and baseline_value is not None:
            scale = intervention.value - baseline_value
        elif intervention.value_change is not None:
            scale = intervention.value_change
        else:
            scale = 1.0
        
        scaled_ate = (base_effect.ate or 0) * scale
        
        return CausalEffect(
            query_id=query.id,
            ate=scaled_ate,
            confidence_interval=base_effect.confidence_interval,
            p_value=base_effect.p_value,
            standard_error=(base_effect.standard_error or 0) * abs(scale),
            estimator=f"intervention_do_{intervention.node_id}",
            is_significant=base_effect.is_significant,
        )
    
    def _find_edge(self, source: str, target: str) -> Optional[CausalEdge]:
        """Find direct edge between nodes"""
        source_id = self._resolve_id(source)
        target_id = self._resolve_id(target)
        
        for edge in self.dag.edges:
            if edge.source_id == source_id and edge.target_id == target_id:
                return edge
        return None
    
    def _resolve_id(self, name_or_id: str) -> str:
        """Resolve node name to ID"""
        if name_or_id in self.dag.nodes:
            return name_or_id
        
        for node_id, node in self.dag.nodes.items():
            if node.name == name_or_id:
                return node_id
        
        return name_or_id
    
    def _mock_estimate(
        self,
        treatment: str,
        outcome: str,
        data: Optional[Dict[str, List[float]]],
    ) -> float:
        """Mock ATE estimation when no edge coefficient"""
        # Use path analysis
        path_coeff = self._compute_path_coefficient(treatment, outcome)
        if path_coeff is not None:
            return path_coeff
        
        # Random mock as last resort
        return random.uniform(-0.5, 0.5)
    
    def _compute_path_coefficient(self, source: str, target: str) -> Optional[float]:
        """Compute total effect via all directed paths"""
        source_id = self._resolve_id(source)
        target_id = self._resolve_id(target)
        
        # BFS to find all paths
        paths = self._find_all_paths(source_id, target_id)
        
        if not paths:
            return None
        
        # Sum product of coefficients along each path
        total_effect = 0.0
        for path in paths:
            path_coeff = 1.0
            for i in range(len(path) - 1):
                edge = self._find_edge(path[i], path[i + 1])
                if edge and edge.coefficient is not None:
                    path_coeff *= edge.coefficient
                else:
                    path_coeff *= 0.5  # Default assumption
            total_effect += path_coeff
        
        return total_effect
    
    def _find_all_paths(
        self,
        source: str,
        target: str,
        max_length: int = 5,
    ) -> List[List[str]]:
        """Find all directed paths from source to target"""
        paths = []
        stack = [(source, [source])]
        
        while stack:
            node, path = stack.pop()
            
            if len(path) > max_length:
                continue
            
            if node == target:
                paths.append(path)
                continue
            
            children = self.dag.get_children(node)
            for child in children:
                if child not in path:  # Avoid cycles
                    stack.append((child, path + [child]))
        
        return paths
    
    def _mock_p_value(self, effect: float, std_error: float) -> float:
        """Mock p-value calculation"""
        if std_error == 0:
            return 0.001 if effect != 0 else 1.0
        
        z = abs(effect / std_error)
        # Approximate two-tailed p-value
        p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
        return max(0.001, min(1.0, p))
    
    def _interpret_effect(self, ate: float) -> str:
        """Interpret effect size"""
        abs_ate = abs(ate)
        
        if abs_ate < 0.1:
            return "negligible"
        elif abs_ate < 0.3:
            return "small"
        elif abs_ate < 0.5:
            return "medium"
        else:
            return "large"


# ============================================================================
# SENSITIVITY ANALYZER
# ============================================================================

class SensitivityAnalyzer:
    """
    Analyze variable sensitivity and impact on outcomes.
    """
    
    def __init__(self, dag: CausalDAG):
        self.dag = dag
        self.estimator = CausalEffectEstimator(dag)
    
    def analyze_all_variables(
        self,
        outcome: str,
    ) -> List[SensitivityScore]:
        """Analyze sensitivity of all variables to outcome"""
        scores = []
        
        outcome_id = self._resolve_id(outcome)
        
        for node_id, node in self.dag.nodes.items():
            if node_id == outcome_id:
                continue
            
            if node.node_type == NodeType.OUTCOME:
                continue
            
            score = self.analyze_variable(node_id, outcome)
            scores.append(score)
        
        # Rank by impact
        scores.sort(key=lambda s: s.impact_score, reverse=True)
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        return scores
    
    def analyze_variable(
        self,
        variable: str,
        outcome: str,
    ) -> SensitivityScore:
        """Analyze sensitivity of single variable to outcome"""
        var_id = self._resolve_id(variable)
        node = self.dag.nodes.get(var_id)
        
        if node is None:
            raise ValueError(f"Node not found: {variable}")
        
        # Estimate causal effect
        effect = self.estimator.estimate_ate(variable, outcome)
        
        # Compute impact score (normalized |ATE|)
        impact = min(1.0, abs(effect.ate or 0))
        
        # Estimate volatility from node statistics
        volatility = self._estimate_volatility(node)
        
        # Controllability based on node type
        controllability = self._estimate_controllability(node)
        
        # Determine if critical
        is_critical = impact > 0.5 and volatility > 0.5
        
        alert_message = None
        if is_critical:
            alert_message = (
                f"⚠️ CRITICAL: {node.name} has high impact ({impact:.0%}) "
                f"AND high volatility ({volatility:.0%})"
            )
        
        return SensitivityScore(
            node_id=var_id,
            node_name=node.name,
            impact_score=impact,
            volatility=volatility,
            controllability=controllability,
            confidence=effect.is_significant and ConfidenceLevel.STRONG or ConfidenceLevel.MODERATE,
            is_critical=is_critical,
            alert_message=alert_message,
        )
    
    def _resolve_id(self, name_or_id: str) -> str:
        """Resolve node name to ID"""
        if name_or_id in self.dag.nodes:
            return name_or_id
        
        for node_id, node in self.dag.nodes.items():
            if node.name == name_or_id:
                return node_id
        
        return name_or_id
    
    def _estimate_volatility(self, node: CausalNode) -> float:
        """Estimate variable volatility"""
        if node.std is not None and node.mean is not None and node.mean != 0:
            # Coefficient of variation
            cv = abs(node.std / node.mean)
            return min(1.0, cv)
        
        # Default based on node type
        if node.node_type == NodeType.CONFOUNDER:
            return 0.7
        elif node.node_type == NodeType.LATENT:
            return 0.9
        elif node.node_type == NodeType.INTERVENTION:
            return 0.2
        else:
            return 0.5
    
    def _estimate_controllability(self, node: CausalNode) -> float:
        """Estimate how controllable a variable is"""
        if not node.is_manipulable:
            return 0.0
        
        if not node.is_observable:
            return 0.1
        
        if node.node_type == NodeType.INTERVENTION:
            return 1.0
        elif node.node_type == NodeType.SLOT:
            return 0.8
        elif node.node_type == NodeType.CONFOUNDER:
            return 0.3
        elif node.node_type == NodeType.LATENT:
            return 0.0
        else:
            return 0.5
    
    def get_key_levers(
        self,
        outcome: str,
        top_n: int = 5,
    ) -> List[SensitivityScore]:
        """Get top N most impactful AND controllable variables"""
        all_scores = self.analyze_all_variables(outcome)
        
        # Score = impact * controllability
        scored = sorted(
            all_scores,
            key=lambda s: s.impact_score * s.controllability,
            reverse=True,
        )
        
        return scored[:top_n]
    
    def get_risk_factors(
        self,
        outcome: str,
        top_n: int = 5,
    ) -> List[SensitivityScore]:
        """Get top N highest risk factors (high impact, high volatility)"""
        all_scores = self.analyze_all_variables(outcome)
        
        # Score = impact * volatility
        scored = sorted(
            all_scores,
            key=lambda s: s.risk_score,
            reverse=True,
        )
        
        return scored[:top_n]


# ============================================================================
# CAUSAL ENGINE (MAIN ENTRY POINT)
# ============================================================================

class CausalEngine:
    """
    Main entry point for causal reasoning in CHE·NU™.
    
    Usage:
        engine = CausalEngine(dag)
        
        # Estimate effect
        effect = engine.estimate_effect("price", "demand")
        
        # Sensitivity analysis
        sensitivity = engine.analyze_sensitivity("revenue")
        
        # Key levers
        levers = engine.get_key_levers("revenue", top_n=3)
    """
    
    def __init__(self, dag: CausalDAG):
        if dag.status not in [ValidationStatus.APPROVED, ValidationStatus.DRAFT]:
            logger.warning(f"Using non-approved DAG: {dag.status}")
        
        self.dag = dag
        self.estimator = CausalEffectEstimator(dag)
        self.sensitivity = SensitivityAnalyzer(dag)
    
    def estimate_effect(
        self,
        treatment: str,
        outcome: str,
        data: Optional[Dict[str, List[float]]] = None,
    ) -> CausalEffect:
        """Estimate causal effect of treatment on outcome"""
        return self.estimator.estimate_ate(treatment, outcome, data)
    
    def estimate_intervention(
        self,
        intervention: Intervention,
        outcome: str,
        baseline_value: Optional[float] = None,
    ) -> CausalEffect:
        """Estimate effect of a specific intervention"""
        return self.estimator.estimate_with_intervention(
            intervention, outcome, baseline_value
        )
    
    def analyze_sensitivity(
        self,
        outcome: str,
    ) -> List[SensitivityScore]:
        """Full sensitivity analysis for outcome"""
        return self.sensitivity.analyze_all_variables(outcome)
    
    def get_key_levers(
        self,
        outcome: str,
        top_n: int = 5,
    ) -> List[SensitivityScore]:
        """Get most actionable variables for outcome"""
        return self.sensitivity.get_key_levers(outcome, top_n)
    
    def get_risk_factors(
        self,
        outcome: str,
        top_n: int = 5,
    ) -> List[SensitivityScore]:
        """Get highest risk variables for outcome"""
        return self.sensitivity.get_risk_factors(outcome, top_n)
    
    def generate_summary(
        self,
        outcome: str,
    ) -> Dict[str, Any]:
        """Generate summary report for decision support"""
        levers = self.get_key_levers(outcome, top_n=3)
        risks = self.get_risk_factors(outcome, top_n=3)
        
        return {
            "dag_id": self.dag.id,
            "dag_name": self.dag.name,
            "outcome": outcome,
            "key_levers": [
                {
                    "name": l.node_name,
                    "impact": f"{l.impact_score:.0%}",
                    "controllability": f"{l.controllability:.0%}",
                }
                for l in levers
            ],
            "risk_factors": [
                {
                    "name": r.node_name,
                    "risk_score": f"{r.risk_score:.0%}",
                    "alert": r.alert_message,
                }
                for r in risks
            ],
            "critical_alerts": [
                r.alert_message for r in risks if r.is_critical
            ],
            "synthetic": self.dag.synthetic,
            "dag_status": self.dag.status.value,
            "generated_at": datetime.utcnow().isoformat(),
        }
