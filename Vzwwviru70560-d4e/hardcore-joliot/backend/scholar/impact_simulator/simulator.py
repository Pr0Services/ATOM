"""
============================================================================
CHE·NU™ V69 — SCHOLAR GLOBAL IMPACT SIMULATOR
============================================================================
Spec: GPT1/CHE-NU_SCH_GLOBAL_IMPACT_SIMULATOR.md

Objective: Simulate causal impact of funding.

Inputs (per spec):
- Montant
- Domaine
- Horizon temporel

Outputs (per spec):
- PIB, santé publique, résilience
- Heatmaps XR
- Scoring d'impact

Targets: Investors, governments, foundations.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import math
import random

from ..models import (
    FundingScenario,
    ImpactResult,
    ImpactMetric,
    generate_id,
)

logger = logging.getLogger(__name__)


# ============================================================================
# IMPACT MODELS (Domain-specific multipliers)
# ============================================================================

# Impact multipliers by domain (simplified model)
DOMAIN_IMPACT_MULTIPLIERS = {
    "biotech": {
        ImpactMetric.GDP: 1.2,
        ImpactMetric.PUBLIC_HEALTH: 2.5,
        ImpactMetric.RESILIENCE: 1.3,
        ImpactMetric.SUSTAINABILITY: 1.0,
        ImpactMetric.INNOVATION: 2.0,
        ImpactMetric.EMPLOYMENT: 1.1,
    },
    "clean_energy": {
        ImpactMetric.GDP: 1.5,
        ImpactMetric.PUBLIC_HEALTH: 1.2,
        ImpactMetric.RESILIENCE: 2.0,
        ImpactMetric.SUSTAINABILITY: 3.0,
        ImpactMetric.INNOVATION: 1.8,
        ImpactMetric.EMPLOYMENT: 1.5,
    },
    "ai_ml": {
        ImpactMetric.GDP: 2.0,
        ImpactMetric.PUBLIC_HEALTH: 1.0,
        ImpactMetric.RESILIENCE: 1.5,
        ImpactMetric.SUSTAINABILITY: 1.2,
        ImpactMetric.INNOVATION: 3.0,
        ImpactMetric.EMPLOYMENT: 0.8,  # May reduce some jobs
    },
    "education": {
        ImpactMetric.GDP: 1.8,
        ImpactMetric.PUBLIC_HEALTH: 1.3,
        ImpactMetric.RESILIENCE: 1.5,
        ImpactMetric.SUSTAINABILITY: 1.4,
        ImpactMetric.INNOVATION: 1.5,
        ImpactMetric.EMPLOYMENT: 1.3,
    },
    "healthcare": {
        ImpactMetric.GDP: 1.3,
        ImpactMetric.PUBLIC_HEALTH: 3.0,
        ImpactMetric.RESILIENCE: 2.0,
        ImpactMetric.SUSTAINABILITY: 1.2,
        ImpactMetric.INNOVATION: 1.5,
        ImpactMetric.EMPLOYMENT: 1.4,
    },
    "infrastructure": {
        ImpactMetric.GDP: 2.2,
        ImpactMetric.PUBLIC_HEALTH: 1.1,
        ImpactMetric.RESILIENCE: 2.5,
        ImpactMetric.SUSTAINABILITY: 1.5,
        ImpactMetric.INNOVATION: 1.2,
        ImpactMetric.EMPLOYMENT: 2.0,
    },
    "default": {
        ImpactMetric.GDP: 1.0,
        ImpactMetric.PUBLIC_HEALTH: 1.0,
        ImpactMetric.RESILIENCE: 1.0,
        ImpactMetric.SUSTAINABILITY: 1.0,
        ImpactMetric.INNOVATION: 1.0,
        ImpactMetric.EMPLOYMENT: 1.0,
    },
}

# Time decay factors (impact diminishes or grows over time)
TIME_FACTORS = {
    ImpactMetric.GDP: 1.05,  # Compounds over time
    ImpactMetric.PUBLIC_HEALTH: 1.02,
    ImpactMetric.RESILIENCE: 1.03,
    ImpactMetric.SUSTAINABILITY: 1.04,
    ImpactMetric.INNOVATION: 1.08,  # Strong compound
    ImpactMetric.EMPLOYMENT: 1.01,
}


# ============================================================================
# IMPACT CALCULATOR
# ============================================================================

class ImpactCalculator:
    """
    Calculate impact scores for funding scenarios.
    """
    
    def __init__(self):
        self._base_impact_per_million = 0.1  # Base impact score per $1M
    
    def calculate_impact(
        self,
        scenario: FundingScenario,
    ) -> Dict[ImpactMetric, float]:
        """Calculate impact across all metrics"""
        multipliers = DOMAIN_IMPACT_MULTIPLIERS.get(
            scenario.domain,
            DOMAIN_IMPACT_MULTIPLIERS["default"]
        )
        
        # Base impact from amount
        base = (scenario.amount / 1_000_000) * self._base_impact_per_million
        
        impacts = {}
        for metric in ImpactMetric:
            # Apply domain multiplier
            mult = multipliers.get(metric, 1.0)
            
            # Apply time factor (compound over years)
            time_factor = TIME_FACTORS.get(metric, 1.0)
            time_mult = math.pow(time_factor, scenario.time_horizon_years)
            
            # Calculate final impact
            impact = base * mult * time_mult
            
            # Add some realistic variance (±10%)
            variance = 0.1 * impact * (random.random() - 0.5)
            impacts[metric] = max(0, impact + variance)
        
        return impacts
    
    def calculate_projections(
        self,
        scenario: FundingScenario,
    ) -> Dict[str, List[float]]:
        """Calculate year-by-year projections"""
        multipliers = DOMAIN_IMPACT_MULTIPLIERS.get(
            scenario.domain,
            DOMAIN_IMPACT_MULTIPLIERS["default"]
        )
        
        base = (scenario.amount / 1_000_000) * self._base_impact_per_million
        
        projections = {}
        for metric in ImpactMetric:
            mult = multipliers.get(metric, 1.0)
            time_factor = TIME_FACTORS.get(metric, 1.0)
            
            yearly = []
            for year in range(1, scenario.time_horizon_years + 1):
                time_mult = math.pow(time_factor, year)
                value = base * mult * time_mult
                yearly.append(value)
            
            projections[metric.value] = yearly
        
        return projections


# ============================================================================
# HEATMAP GENERATOR
# ============================================================================

class HeatmapGenerator:
    """
    Generate XR heatmaps for impact visualization.
    
    Per spec: Heatmaps XR
    """
    
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
    
    def generate_heatmap(
        self,
        impacts: Dict[ImpactMetric, float],
        domain: str,
    ) -> Dict[str, Any]:
        """Generate heatmap data for XR visualization"""
        # Create a grid where intensity = impact level
        grid = []
        
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                # Combine metrics with spatial variation
                total_impact = sum(impacts.values())
                
                # Add spatial pattern (center = higher impact)
                center_dist = math.sqrt(
                    (i - self.grid_size/2)**2 + (j - self.grid_size/2)**2
                )
                spatial_factor = 1 - (center_dist / (self.grid_size * 0.7))
                spatial_factor = max(0, spatial_factor)
                
                intensity = total_impact * spatial_factor * 0.5
                row.append(intensity)
            grid.append(row)
        
        return {
            "type": "impact_heatmap",
            "domain": domain,
            "grid_size": self.grid_size,
            "grid": grid,
            "metrics": {m.value: v for m, v in impacts.items()},
            "color_scale": {
                "low": "#0000FF",
                "medium": "#00FF00",
                "high": "#FF0000",
            },
        }


# ============================================================================
# GLOBAL IMPACT SIMULATOR
# ============================================================================

class GlobalImpactSimulator:
    """
    Main simulator for funding impact analysis.
    
    Per spec: Funding Sandbox
    """
    
    def __init__(self):
        self.calculator = ImpactCalculator()
        self.heatmap_gen = HeatmapGenerator()
        
        # Results cache
        self._results: Dict[str, ImpactResult] = {}
    
    def create_scenario(
        self,
        name: str,
        amount: float,
        domain: str,
        time_horizon_years: int,
        allocation: Dict[str, float] = None,
        assumptions: Dict[str, Any] = None,
    ) -> FundingScenario:
        """
        Create a funding scenario.
        
        Per spec inputs: Montant, Domaine, Horizon temporel
        """
        return FundingScenario(
            scenario_id=generate_id(),
            name=name,
            amount=amount,
            domain=domain,
            time_horizon_years=time_horizon_years,
            allocation=allocation or {},
            assumptions=assumptions or {},
        )
    
    def simulate(
        self,
        scenario: FundingScenario,
    ) -> ImpactResult:
        """
        Run impact simulation.
        
        Per spec outputs: PIB, santé publique, résilience, Heatmaps XR, Scoring
        """
        # Calculate impacts
        impacts = self.calculator.calculate_impact(scenario)
        
        # Calculate projections
        projections = self.calculator.calculate_projections(scenario)
        
        # Generate heatmap
        heatmap = self.heatmap_gen.generate_heatmap(impacts, scenario.domain)
        
        # Calculate total score
        total_score = sum(impacts.values())
        
        # Calculate confidence (higher for well-studied domains)
        well_studied = {"biotech", "healthcare", "education", "clean_energy"}
        confidence = 0.8 if scenario.domain in well_studied else 0.6
        
        # Calculate uncertainty range
        uncertainty = total_score * (1 - confidence) * 0.5
        uncertainty_range = (total_score - uncertainty, total_score + uncertainty)
        
        result = ImpactResult(
            result_id=generate_id(),
            scenario_id=scenario.scenario_id,
            impacts={m.value: v for m, v in impacts.items()},
            total_impact_score=total_score,
            projections=projections,
            heatmap_data=heatmap,
            confidence_score=confidence,
            uncertainty_range=uncertainty_range,
        )
        
        self._results[result.result_id] = result
        
        logger.info(
            f"Simulated scenario {scenario.name}: "
            f"total_score={total_score:.2f}, confidence={confidence:.0%}"
        )
        
        return result
    
    def compare_scenarios(
        self,
        scenarios: List[FundingScenario],
    ) -> Dict[str, Any]:
        """Compare multiple funding scenarios"""
        results = []
        
        for scenario in scenarios:
            result = self.simulate(scenario)
            results.append({
                "scenario_id": scenario.scenario_id,
                "name": scenario.name,
                "amount": scenario.amount,
                "domain": scenario.domain,
                "total_score": result.total_impact_score,
                "impacts": result.impacts,
                "confidence": result.confidence_score,
            })
        
        # Rank by total score
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        return {
            "comparison": results,
            "best_scenario": results[0]["name"] if results else None,
            "summary": {
                "total_scenarios": len(scenarios),
                "total_funding": sum(s.amount for s in scenarios),
                "avg_impact": sum(r["total_score"] for r in results) / len(results) if results else 0,
            },
        }
    
    def get_result(self, result_id: str) -> Optional[ImpactResult]:
        """Get simulation result by ID"""
        return self._results.get(result_id)
    
    def export_for_xr(self, result: ImpactResult) -> Dict[str, Any]:
        """
        Export result for XR visualization.
        
        Per spec: Heatmaps XR
        """
        return {
            "type": "impact_visualization",
            "schema_version": "v1",
            "result_id": result.result_id,
            "total_score": result.total_impact_score,
            "metrics": result.impacts,
            "projections": result.projections,
            "heatmap": result.heatmap_data,
            "confidence": result.confidence_score,
            "uncertainty": result.uncertainty_range,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_simulator() -> GlobalImpactSimulator:
    """Create a global impact simulator"""
    return GlobalImpactSimulator()


def create_scenario(
    name: str,
    amount: float,
    domain: str,
    years: int,
) -> FundingScenario:
    """Create a funding scenario"""
    return FundingScenario(
        scenario_id=generate_id(),
        name=name,
        amount=amount,
        domain=domain,
        time_horizon_years=years,
    )
