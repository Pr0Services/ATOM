"""
============================================================================
CHE·NU™ V69 — COUNTERFACTUAL ANALYSIS ENGINE
============================================================================
Version: 1.0.0
Purpose: What-if analysis and counterfactual reasoning
Principle: Test impossible scenarios safely - SYNTHETIC ONLY
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import math

from ..core.models import (
    CausalDAG,
    CausalNode,
    CausalQuery,
    CausalEffect,
    CounterfactualResult,
    Intervention,
    InterventionType,
    ConfidenceLevel,
    NodeType,
)
from ..core.inference import CausalEffectEstimator

logger = logging.getLogger(__name__)


# ============================================================================
# COUNTERFACTUAL ENGINE
# ============================================================================

class CounterfactualEngine:
    """
    Engine for counterfactual analysis.
    
    Answers questions like:
    - "What if X had not happened?"
    - "What would Y be if we had done Z?"
    - "What was the effect of past decision D?"
    
    NOTE: All analysis is SYNTHETIC - no real consequences.
    """
    
    def __init__(self, dag: CausalDAG):
        self.dag = dag
        self.estimator = CausalEffectEstimator(dag)
    
    def what_if(
        self,
        intervention_node: str,
        intervention_value: float,
        outcome_node: str,
        factual_value: Optional[float] = None,
        baseline_intervention_value: Optional[float] = None,
    ) -> CounterfactualResult:
        """
        Answer: "What if [node] had been [value]?"
        
        Args:
            intervention_node: Node to intervene on
            intervention_value: Counterfactual value
            outcome_node: Outcome to evaluate
            factual_value: Actual observed outcome
            baseline_intervention_value: Actual intervention value (for comparison)
        """
        query = CausalQuery(
            dag_id=self.dag.id,
            query_type="counterfactual",
            treatment=intervention_node,
            outcome=outcome_node,
            interventions=[
                Intervention(
                    node_id=intervention_node,
                    intervention_type=InterventionType.COUNTERFACTUAL,
                    value=intervention_value,
                )
            ],
            synthetic=True,
        )
        
        # Get the intervention node
        int_node = self._get_node(intervention_node)
        
        # Baseline value
        if baseline_intervention_value is None:
            baseline_intervention_value = int_node.observed_value or 0
        
        # Change in intervention
        delta_intervention = intervention_value - baseline_intervention_value
        
        # Estimate causal effect
        effect = self.estimator.estimate_ate(intervention_node, outcome_node)
        
        # Calculate counterfactual outcome
        # Y_cf = Y_factual + ATE * delta_intervention
        if factual_value is None:
            out_node = self._get_node(outcome_node)
            factual_value = out_node.observed_value or 0
        
        counterfactual_outcome = factual_value + (effect.ate or 0) * delta_intervention
        
        # Calculate effect
        effect_value = counterfactual_outcome - factual_value
        relative_effect = None
        if factual_value != 0:
            relative_effect = effect_value / factual_value
        
        # Confidence interval (propagate uncertainty)
        ci = None
        if effect.confidence_interval:
            ci_low = factual_value + effect.confidence_interval[0] * delta_intervention
            ci_high = factual_value + effect.confidence_interval[1] * delta_intervention
            ci = (ci_low - factual_value, ci_high - factual_value)
        
        # Interpretation
        interpretation = self._generate_interpretation(
            intervention_node,
            intervention_value,
            baseline_intervention_value,
            outcome_node,
            factual_value,
            counterfactual_outcome,
        )
        
        return CounterfactualResult(
            query_id=query.id,
            factual_outcome=factual_value,
            counterfactual_outcome=counterfactual_outcome,
            effect=effect_value,
            relative_effect=relative_effect,
            confidence_interval=ci,
            interpretation=interpretation,
        )
    
    def what_if_not(
        self,
        intervention_node: str,
        outcome_node: str,
        factual_value: Optional[float] = None,
    ) -> CounterfactualResult:
        """
        Answer: "What if [node] had NOT happened?"
        
        Sets intervention to 0 or baseline.
        """
        int_node = self._get_node(intervention_node)
        
        # "Not happened" = set to 0 or domain minimum
        counterfactual_value = 0
        if int_node.domain:
            counterfactual_value = int_node.domain[0]
        
        return self.what_if(
            intervention_node=intervention_node,
            intervention_value=counterfactual_value,
            outcome_node=outcome_node,
            factual_value=factual_value,
        )
    
    def compare_scenarios(
        self,
        base_scenario: Dict[str, float],
        alternative_scenario: Dict[str, float],
        outcome_node: str,
    ) -> Dict[str, CounterfactualResult]:
        """
        Compare two intervention scenarios.
        
        Args:
            base_scenario: {node_name: value} for base case
            alternative_scenario: {node_name: value} for alternative
            outcome_node: Outcome to compare
        """
        results = {}
        
        for node_name in alternative_scenario:
            if node_name not in base_scenario:
                continue
            
            base_value = base_scenario[node_name]
            alt_value = alternative_scenario[node_name]
            
            if base_value == alt_value:
                continue
            
            result = self.what_if(
                intervention_node=node_name,
                intervention_value=alt_value,
                outcome_node=outcome_node,
                baseline_intervention_value=base_value,
            )
            
            results[node_name] = result
        
        return results
    
    def analyze_past_decision(
        self,
        decision_node: str,
        decision_value: float,
        outcome_node: str,
        actual_outcome: float,
        alternative_values: List[float],
    ) -> Dict[str, Any]:
        """
        Post-mortem analysis of a past decision.
        
        "What would have happened if we had chosen differently?"
        
        Returns analysis of all alternatives vs actual decision.
        """
        results = []
        
        # Analyze each alternative
        for alt_value in alternative_values:
            cf_result = self.what_if(
                intervention_node=decision_node,
                intervention_value=alt_value,
                outcome_node=outcome_node,
                factual_value=actual_outcome,
                baseline_intervention_value=decision_value,
            )
            
            results.append({
                "alternative_value": alt_value,
                "counterfactual_outcome": cf_result.counterfactual_outcome,
                "effect_vs_actual": cf_result.effect,
                "would_have_been_better": cf_result.effect > 0,
            })
        
        # Find best alternative
        best_alt = max(results, key=lambda r: r["counterfactual_outcome"])
        worst_alt = min(results, key=lambda r: r["counterfactual_outcome"])
        
        # Was actual decision optimal?
        was_optimal = all(
            r["counterfactual_outcome"] <= actual_outcome
            for r in results
        )
        
        return {
            "decision_node": decision_node,
            "actual_decision": decision_value,
            "actual_outcome": actual_outcome,
            "alternatives_analyzed": results,
            "best_alternative": best_alt,
            "worst_alternative": worst_alt,
            "was_optimal": was_optimal,
            "regret": best_alt["counterfactual_outcome"] - actual_outcome,
            "synthetic": True,
            "analyzed_at": datetime.utcnow().isoformat(),
        }
    
    def blame_attribution(
        self,
        outcome_node: str,
        outcome_deviation: float,
        candidate_causes: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Attribute blame for outcome deviation to candidate causes.
        
        "Why did the outcome deviate by X? Which factors contributed?"
        
        Returns attribution scores for each candidate.
        """
        attributions = []
        total_explained = 0
        
        for cause in candidate_causes:
            # Get node
            cause_node = self._get_node(cause)
            
            # Estimate effect
            effect = self.estimator.estimate_ate(cause, outcome_node)
            
            # Calculate contribution
            # Simplified: assume deviation proportional to effect * variable deviation
            if cause_node.observed_value is not None and cause_node.mean is not None:
                var_deviation = cause_node.observed_value - cause_node.mean
            else:
                var_deviation = 1  # Unknown
            
            contribution = (effect.ate or 0) * var_deviation
            
            attributions.append({
                "cause": cause,
                "effect_size": effect.ate,
                "variable_deviation": var_deviation,
                "contribution_to_outcome": contribution,
                "confidence": effect.is_significant,
            })
            
            total_explained += abs(contribution)
        
        # Normalize to get percentages
        if total_explained > 0:
            for attr in attributions:
                attr["blame_percentage"] = abs(attr["contribution_to_outcome"]) / total_explained
        
        # Sort by blame
        attributions.sort(key=lambda a: abs(a.get("blame_percentage", 0)), reverse=True)
        
        return attributions
    
    def _get_node(self, name_or_id: str) -> CausalNode:
        """Get node by name or ID"""
        if name_or_id in self.dag.nodes:
            return self.dag.nodes[name_or_id]
        
        for node_id, node in self.dag.nodes.items():
            if node.name == name_or_id:
                return node
        
        raise ValueError(f"Node not found: {name_or_id}")
    
    def _generate_interpretation(
        self,
        intervention_node: str,
        intervention_value: float,
        baseline_value: float,
        outcome_node: str,
        factual_outcome: float,
        counterfactual_outcome: float,
    ) -> str:
        """Generate human-readable interpretation"""
        int_node = self._get_node(intervention_node)
        out_node = self._get_node(outcome_node)
        
        # Direction of intervention
        int_direction = "increased" if intervention_value > baseline_value else "decreased"
        int_change = abs(intervention_value - baseline_value)
        
        # Direction of outcome change
        out_change = counterfactual_outcome - factual_outcome
        out_direction = "higher" if out_change > 0 else "lower"
        
        return (
            f"If {int_node.name} had been {int_direction} by {int_change:.2f} "
            f"(to {intervention_value:.2f}), {out_node.name} would have been "
            f"{abs(out_change):.2f} {out_direction} ({counterfactual_outcome:.2f} "
            f"instead of {factual_outcome:.2f})."
        )


# ============================================================================
# SCENARIO COMPARATOR
# ============================================================================

class ScenarioComparator:
    """
    Compare multiple simulation scenarios for decision support.
    """
    
    def __init__(self, dag: CausalDAG):
        self.dag = dag
        self.cf_engine = CounterfactualEngine(dag)
    
    def compare_n_scenarios(
        self,
        scenarios: List[Dict[str, float]],
        outcome_node: str,
        scenario_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Compare N scenarios on a given outcome.
        
        Args:
            scenarios: List of {node_name: value} dicts
            outcome_node: Outcome to compare
            scenario_names: Optional names for scenarios
        """
        if scenario_names is None:
            scenario_names = [f"Scenario {i+1}" for i in range(len(scenarios))]
        
        results = []
        base_scenario = scenarios[0]
        
        for i, scenario in enumerate(scenarios):
            if i == 0:
                # Base scenario
                out_node = self._get_node(outcome_node)
                results.append({
                    "name": scenario_names[i],
                    "outcome": out_node.observed_value or 0,
                    "vs_base": 0,
                    "is_base": True,
                })
            else:
                # Compare to base
                comparison = self.cf_engine.compare_scenarios(
                    base_scenario,
                    scenario,
                    outcome_node,
                )
                
                # Sum all effects
                total_effect = sum(
                    cf.effect for cf in comparison.values()
                )
                
                base_outcome = results[0]["outcome"]
                results.append({
                    "name": scenario_names[i],
                    "outcome": base_outcome + total_effect,
                    "vs_base": total_effect,
                    "is_base": False,
                    "breakdown": {
                        node: {
                            "effect": cf.effect,
                            "interpretation": cf.interpretation,
                        }
                        for node, cf in comparison.items()
                    },
                })
        
        # Rank by outcome
        ranked = sorted(results, key=lambda r: r["outcome"], reverse=True)
        for i, r in enumerate(ranked):
            r["rank"] = i + 1
        
        # Best scenario
        best = ranked[0]
        
        return {
            "outcome_variable": outcome_node,
            "scenarios_compared": len(scenarios),
            "results": results,
            "ranking": [r["name"] for r in ranked],
            "best_scenario": best["name"],
            "best_outcome": best["outcome"],
            "synthetic": True,
            "compared_at": datetime.utcnow().isoformat(),
        }
    
    def _get_node(self, name_or_id: str) -> CausalNode:
        """Get node by name or ID"""
        if name_or_id in self.dag.nodes:
            return self.dag.nodes[name_or_id]
        
        for node_id, node in self.dag.nodes.items():
            if node.name == name_or_id:
                return node
        
        raise ValueError(f"Node not found: {name_or_id}")
    
    def pareto_frontier(
        self,
        scenarios: List[Dict[str, float]],
        outcome_nodes: List[str],
        scenario_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Find Pareto-optimal scenarios across multiple outcomes.
        
        A scenario is Pareto-optimal if no other scenario is better
        on ALL outcomes.
        """
        if scenario_names is None:
            scenario_names = [f"Scenario {i+1}" for i in range(len(scenarios))]
        
        # Evaluate all scenarios on all outcomes
        evaluated = []
        for i, scenario in enumerate(scenarios):
            outcomes = {}
            for out_node in outcome_nodes:
                # Get base value and apply scenario
                node = self._get_node(out_node)
                outcomes[out_node] = node.observed_value or 0
                
                # Apply causal effects from scenario changes
                for var, val in scenario.items():
                    effect = self.cf_engine.estimator.estimate_ate(var, out_node)
                    var_node = self._get_node(var)
                    delta = val - (var_node.observed_value or 0)
                    outcomes[out_node] += (effect.ate or 0) * delta
            
            evaluated.append({
                "name": scenario_names[i],
                "scenario": scenario,
                "outcomes": outcomes,
            })
        
        # Find Pareto frontier
        pareto_optimal = []
        for i, eval_i in enumerate(evaluated):
            is_dominated = False
            for j, eval_j in enumerate(evaluated):
                if i == j:
                    continue
                
                # Check if j dominates i (j is better on ALL outcomes)
                j_dominates = all(
                    eval_j["outcomes"][o] >= eval_i["outcomes"][o]
                    for o in outcome_nodes
                ) and any(
                    eval_j["outcomes"][o] > eval_i["outcomes"][o]
                    for o in outcome_nodes
                )
                
                if j_dominates:
                    is_dominated = True
                    break
            
            if not is_dominated:
                pareto_optimal.append(eval_i)
        
        return {
            "outcomes_evaluated": outcome_nodes,
            "total_scenarios": len(scenarios),
            "pareto_optimal_count": len(pareto_optimal),
            "pareto_optimal": pareto_optimal,
            "all_evaluated": evaluated,
            "synthetic": True,
        }
