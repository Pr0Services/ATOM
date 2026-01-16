"""
============================================================================
CHE·NU™ V69 — SLOT FILL CAUSAL PRIORITY
============================================================================
Spec: GPT1/CHE-NU_ENG_SLOT_FILL_CAUSAL_PRIORITY.md

Objective: Prioritize slot filling based on real causal impact.

Principle:
- Tous les slots n'ont pas la même valeur décisionnelle.
- Le moteur causal mesure l'impact, calcule la sensibilité, ignore les négligeables

Before: Slot vide = à remplir
After: Slot vide mais impact < seuil → ignoré, impact élevé → prioritaire

Outputs:
- Liste priorisée des slots
- Justification causale
- Score de confiance
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import math

from ..models import (
    Slot,
    SlotStatus,
    CausalPriority,
    Document,
)

logger = logging.getLogger(__name__)


# ============================================================================
# IMPACT CALCULATOR
# ============================================================================

@dataclass
class ImpactFactors:
    """Factors contributing to causal impact"""
    
    # Direct impact on outcomes
    outcome_sensitivity: float = 0.0  # How much outcomes change when this changes
    
    # Downstream effects
    downstream_slots: int = 0  # Number of slots that depend on this
    propagation_depth: int = 0  # How deep the causal chain goes
    
    # Uncertainty factors
    current_uncertainty: float = 0.0  # Uncertainty in current value
    value_range: float = 0.0  # Range of possible values
    
    # Time factors
    time_sensitivity: float = 0.0  # Does timing matter?
    
    # Weights for combining
    weights: Dict[str, float] = field(default_factory=lambda: {
        "outcome_sensitivity": 0.35,
        "downstream_effect": 0.25,
        "uncertainty": 0.20,
        "time_sensitivity": 0.20,
    })


class CausalImpactCalculator:
    """
    Calculates causal impact of slots.
    
    Per spec:
    - mesure l'impact
    - calcule la sensibilité
    - ignore les variables négligeables
    """
    
    def __init__(
        self,
        impact_threshold: float = 0.1,
        sensitivity_threshold: float = 0.05,
    ):
        self.impact_threshold = impact_threshold
        self.sensitivity_threshold = sensitivity_threshold
        
        # Custom impact functions per slot type
        self._impact_functions: Dict[str, Callable] = {}
        
        # Causal graph (simplified DAG representation)
        self._dependencies: Dict[str, List[str]] = {}  # slot_id → dependent slot_ids
    
    def set_dependencies(self, dependencies: Dict[str, List[str]]) -> None:
        """Set slot dependencies (causal graph)"""
        self._dependencies = dependencies
    
    def add_impact_function(
        self,
        slot_type: str,
        func: Callable[[Slot], float],
    ) -> None:
        """Add custom impact function for a slot type"""
        self._impact_functions[slot_type] = func
    
    def calculate_impact(self, slot: Slot) -> ImpactFactors:
        """Calculate impact factors for a slot"""
        factors = ImpactFactors()
        
        # Calculate outcome sensitivity
        if slot.slot_type.value in self._impact_functions:
            factors.outcome_sensitivity = self._impact_functions[slot.slot_type.value](slot)
        else:
            factors.outcome_sensitivity = self._default_outcome_sensitivity(slot)
        
        # Calculate downstream effects
        downstream = self._get_downstream_slots(slot.slot_id)
        factors.downstream_slots = len(downstream)
        factors.propagation_depth = self._calculate_propagation_depth(slot.slot_id)
        
        # Calculate uncertainty
        factors.current_uncertainty = self._calculate_uncertainty(slot)
        
        # Calculate time sensitivity
        factors.time_sensitivity = self._calculate_time_sensitivity(slot)
        
        return factors
    
    def calculate_causal_impact(self, slot: Slot) -> float:
        """
        Calculate overall causal impact score (0-1).
        
        High impact = high priority for filling.
        """
        factors = self.calculate_impact(slot)
        
        # Combine factors with weights
        weights = factors.weights
        
        # Normalize downstream effect (assume max 10 downstream slots)
        downstream_normalized = min(factors.downstream_slots / 10, 1.0)
        
        # Normalize propagation depth (assume max depth 5)
        depth_normalized = min(factors.propagation_depth / 5, 1.0)
        
        downstream_effect = (downstream_normalized + depth_normalized) / 2
        
        impact = (
            weights["outcome_sensitivity"] * factors.outcome_sensitivity +
            weights["downstream_effect"] * downstream_effect +
            weights["uncertainty"] * factors.current_uncertainty +
            weights["time_sensitivity"] * factors.time_sensitivity
        )
        
        # Clamp to 0-1
        return max(0.0, min(1.0, impact))
    
    def calculate_sensitivity(self, slot: Slot) -> float:
        """
        Calculate sensitivity score (0-1).
        
        How sensitive is the system to changes in this slot?
        """
        factors = self.calculate_impact(slot)
        
        # Sensitivity is primarily about outcome sensitivity and downstream effects
        downstream_normalized = min(factors.downstream_slots / 10, 1.0)
        
        sensitivity = (
            0.6 * factors.outcome_sensitivity +
            0.4 * downstream_normalized
        )
        
        return max(0.0, min(1.0, sensitivity))
    
    def is_negligible(self, slot: Slot) -> bool:
        """
        Check if slot is negligible (can be ignored).
        
        Per spec: impact < seuil → ignoré
        """
        impact = self.calculate_causal_impact(slot)
        sensitivity = self.calculate_sensitivity(slot)
        
        return (
            impact < self.impact_threshold and
            sensitivity < self.sensitivity_threshold
        )
    
    def _default_outcome_sensitivity(self, slot: Slot) -> float:
        """Default outcome sensitivity based on slot properties"""
        base_sensitivity = 0.3  # Default
        
        # Adjust based on risk level
        risk_multipliers = {
            "low": 0.5,
            "medium": 1.0,
            "high": 1.5,
            "critical": 2.0,
        }
        multiplier = risk_multipliers.get(slot.risk_level.value, 1.0)
        
        # Adjust based on whether it has dependencies
        if slot.dependencies:
            multiplier *= 1.2
        
        return min(base_sensitivity * multiplier, 1.0)
    
    def _get_downstream_slots(self, slot_id: str) -> List[str]:
        """Get all slots that depend on this slot"""
        return self._dependencies.get(slot_id, [])
    
    def _calculate_propagation_depth(
        self,
        slot_id: str,
        visited: set = None,
    ) -> int:
        """Calculate how deep the causal chain goes"""
        if visited is None:
            visited = set()
        
        if slot_id in visited:
            return 0
        
        visited.add(slot_id)
        downstream = self._get_downstream_slots(slot_id)
        
        if not downstream:
            return 0
        
        max_depth = 0
        for child_id in downstream:
            depth = self._calculate_propagation_depth(child_id, visited)
            max_depth = max(max_depth, depth)
        
        return max_depth + 1
    
    def _calculate_uncertainty(self, slot: Slot) -> float:
        """Calculate uncertainty in slot value"""
        if slot.status == SlotStatus.VALIDATED:
            return 0.0
        elif slot.status == SlotStatus.FILLED:
            return 0.2
        elif slot.status == SlotStatus.PENDING:
            return 0.5
        else:
            return 1.0  # Empty = maximum uncertainty
    
    def _calculate_time_sensitivity(self, slot: Slot) -> float:
        """Calculate time sensitivity (does timing matter?)"""
        # For now, simple heuristic based on slot type
        time_sensitive_types = {"date", "finance", "legal"}
        
        if slot.slot_type.value in time_sensitive_types:
            return 0.7
        return 0.2


# ============================================================================
# PRIORITY RANKER
# ============================================================================

class SlotPriorityRanker:
    """
    Ranks slots by priority based on causal impact.
    
    Per spec outputs:
    - Liste priorisée des slots
    - Justification causale
    - Score de confiance
    """
    
    def __init__(self, calculator: CausalImpactCalculator = None):
        self.calculator = calculator or CausalImpactCalculator()
    
    def rank_slots(
        self,
        slots: List[Slot],
        include_negligible: bool = False,
    ) -> List[Tuple[Slot, CausalPriority]]:
        """
        Rank slots by causal priority.
        
        Returns list of (slot, priority) tuples sorted by priority (high to low).
        """
        priorities: List[Tuple[Slot, CausalPriority]] = []
        
        for slot in slots:
            priority = self._compute_priority(slot)
            
            # Skip negligible slots unless requested
            if priority.is_negligible and not include_negligible:
                logger.debug(f"Skipping negligible slot {slot.slot_id}")
                continue
            
            priorities.append((slot, priority))
        
        # Sort by priority score (descending)
        priorities.sort(key=lambda x: x[1].priority_score, reverse=True)
        
        # Assign ranks
        for rank, (slot, priority) in enumerate(priorities, start=1):
            priority.priority_rank = rank
            slot.priority_rank = rank
        
        return priorities
    
    def rank_document(
        self,
        document: Document,
        include_negligible: bool = False,
    ) -> List[Tuple[Slot, CausalPriority]]:
        """Rank all slots in a document"""
        slots = list(document.slots.values())
        return self.rank_slots(slots, include_negligible)
    
    def get_top_priority_slots(
        self,
        slots: List[Slot],
        top_n: int = 10,
    ) -> List[Tuple[Slot, CausalPriority]]:
        """Get the top N priority slots"""
        ranked = self.rank_slots(slots)
        return ranked[:top_n]
    
    def _compute_priority(self, slot: Slot) -> CausalPriority:
        """Compute priority for a single slot"""
        causal_impact = self.calculator.calculate_causal_impact(slot)
        sensitivity = self.calculator.calculate_sensitivity(slot)
        uncertainty = self.calculator._calculate_uncertainty(slot)
        
        priority = CausalPriority(
            slot_id=slot.slot_id,
            causal_impact=causal_impact,
            sensitivity=sensitivity,
            uncertainty=uncertainty,
        )
        
        # Compute combined priority score
        priority.compute_priority()
        
        # Check if negligible
        priority.is_negligible = self.calculator.is_negligible(slot)
        
        # Generate justification
        priority.justification = self._generate_justification(slot, priority)
        priority.contributing_factors = self._get_contributing_factors(slot, priority)
        
        # Update slot
        slot.causal_impact = causal_impact
        slot.sensitivity_score = sensitivity
        
        return priority
    
    def _generate_justification(
        self,
        slot: Slot,
        priority: CausalPriority,
    ) -> str:
        """Generate human-readable justification"""
        if priority.is_negligible:
            return f"Slot '{slot.name}' has low causal impact ({priority.causal_impact:.2f}) and can be deferred."
        
        impact_level = "high" if priority.causal_impact > 0.6 else "medium" if priority.causal_impact > 0.3 else "low"
        sensitivity_level = "high" if priority.sensitivity > 0.6 else "medium" if priority.sensitivity > 0.3 else "low"
        
        return (
            f"Slot '{slot.name}' has {impact_level} causal impact ({priority.causal_impact:.2f}) "
            f"and {sensitivity_level} sensitivity ({priority.sensitivity:.2f}). "
            f"Priority rank: {priority.priority_rank}."
        )
    
    def _get_contributing_factors(
        self,
        slot: Slot,
        priority: CausalPriority,
    ) -> List[str]:
        """Get list of contributing factors"""
        factors = []
        
        if priority.causal_impact > 0.5:
            factors.append("High outcome sensitivity")
        
        if priority.sensitivity > 0.5:
            factors.append("Many downstream dependencies")
        
        if priority.uncertainty > 0.5:
            factors.append("High uncertainty in current value")
        
        if slot.risk_level.value in ["high", "critical"]:
            factors.append(f"Risk level: {slot.risk_level.value}")
        
        if slot.dependencies:
            factors.append(f"{len(slot.dependencies)} upstream dependencies")
        
        return factors


# ============================================================================
# PRIORITY FILTER
# ============================================================================

class PriorityFilter:
    """Filter slots based on priority criteria"""
    
    def __init__(
        self,
        min_impact: float = 0.1,
        min_confidence: float = 0.5,
    ):
        self.min_impact = min_impact
        self.min_confidence = min_confidence
    
    def filter_by_impact(
        self,
        priorities: List[Tuple[Slot, CausalPriority]],
    ) -> List[Tuple[Slot, CausalPriority]]:
        """Filter out slots below minimum impact"""
        return [
            (slot, priority) for slot, priority in priorities
            if priority.causal_impact >= self.min_impact
        ]
    
    def filter_actionable(
        self,
        priorities: List[Tuple[Slot, CausalPriority]],
    ) -> List[Tuple[Slot, CausalPriority]]:
        """Get only actionable slots (non-negligible, not validated)"""
        return [
            (slot, priority) for slot, priority in priorities
            if not priority.is_negligible and slot.status != SlotStatus.VALIDATED
        ]
    
    def get_high_priority(
        self,
        priorities: List[Tuple[Slot, CausalPriority]],
        threshold: float = 0.6,
    ) -> List[Tuple[Slot, CausalPriority]]:
        """Get high priority slots only"""
        return [
            (slot, priority) for slot, priority in priorities
            if priority.priority_score >= threshold
        ]


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_impact_calculator(
    impact_threshold: float = 0.1,
    sensitivity_threshold: float = 0.05,
) -> CausalImpactCalculator:
    """Create a causal impact calculator"""
    return CausalImpactCalculator(impact_threshold, sensitivity_threshold)


def create_priority_ranker(
    calculator: CausalImpactCalculator = None,
) -> SlotPriorityRanker:
    """Create a slot priority ranker"""
    return SlotPriorityRanker(calculator)


def create_priority_filter(
    min_impact: float = 0.1,
    min_confidence: float = 0.5,
) -> PriorityFilter:
    """Create a priority filter"""
    return PriorityFilter(min_impact, min_confidence)
