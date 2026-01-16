"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT GAME TEMPLATE GENERATOR
============================================================================
Spec: GPT1/CHE-NU_ENT_GAME_GEN_LLM_TEMPLATES.md

Objective: Use LLM to generate serious game blueprints (JSON) from
WorldEngine simulations.

Principle: CHE·NU ne crée pas un moteur de jeu.
Il génère des templates interprétables par le moteur XR existant.

Agent: L2/L3 — Game Design Agent
Three layers: Narrative, Mechanic, Visual

Templates: The Optimizer, Crisis Protocol, The Explorer
Output: GAME_MANIFEST.json (signé OPA)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging
import json

from ..models import (
    GameManifest,
    GameTemplateType,
    GameLayer,
    NarrativeLayer,
    MechanicLayer,
    VisualLayer,
    CrisisCard,
    ScenarioBranch,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TEMPLATE GENERATORS
# ============================================================================

class OptimizerGenerator:
    """
    Generate The Optimizer template.
    
    Per spec: Équilibrer ressources critiques sous contraintes.
    """
    
    def generate(
        self,
        simulation_data: Dict[str, Any],
        kpis: List[str],
    ) -> GameManifest:
        """Generate optimizer game manifest"""
        manifest = GameManifest(
            manifest_id=generate_id(),
            template_type=GameTemplateType.THE_OPTIMIZER,
            simulation_ref=simulation_data.get("simulation_id", ""),
        )
        
        # Narrative layer
        manifest.narrative = NarrativeLayer(
            title=f"Resource Optimizer: {simulation_data.get('domain', 'General')}",
            description="Balance critical resources under constraints to achieve optimal outcomes.",
            stakes=[
                "Resource depletion risk",
                "Stakeholder satisfaction",
                "Long-term sustainability",
            ],
            kpis=kpis,
            scenario_context=simulation_data.get("context", ""),
        )
        
        # Mechanic layer
        resources = simulation_data.get("resources", [])
        manifest.mechanic = MechanicLayer(
            rules=[
                {"type": "allocation", "description": "Allocate resources each turn"},
                {"type": "constraint", "description": "Stay within budget limits"},
                {"type": "feedback", "description": "Receive impact feedback after each decision"},
            ],
            resources=[
                {"name": r, "initial": 100, "min": 0, "max": 200}
                for r in resources
            ] if resources else [
                {"name": "budget", "initial": 100, "min": 0, "max": 200},
                {"name": "time", "initial": 100, "min": 0, "max": 100},
                {"name": "workforce", "initial": 50, "min": 0, "max": 100},
            ],
            costs={
                "action_small": 10,
                "action_medium": 25,
                "action_large": 50,
            },
            trade_offs=[
                {"choice": "speed_vs_quality", "description": "Faster delivery reduces quality"},
                {"choice": "cost_vs_scope", "description": "Lower cost means reduced scope"},
            ],
            win_conditions=["Achieve all KPI targets", "Maintain resource balance"],
            lose_conditions=["Resource depletion", "Critical KPI failure"],
        )
        
        # Visual layer
        manifest.visual = VisualLayer(
            xr_assets=["dashboard_3d", "resource_bars", "kpi_gauges"],
            environment="control_room",
            ui_template="optimizer_ui",
            color_scheme={
                "primary": "#3EB4A2",
                "secondary": "#D8B26A",
                "alert": "#C74B50",
            },
        )
        
        return manifest


class CrisisProtocolGenerator:
    """
    Generate Crisis Protocol template.
    
    Per spec: Créer des cartes à gains immédiats / risques longs termes.
    """
    
    def generate(
        self,
        simulation_data: Dict[str, Any],
        crisis_scenario: str,
    ) -> Tuple[GameManifest, List[CrisisCard]]:
        """Generate crisis protocol game with cards"""
        manifest = GameManifest(
            manifest_id=generate_id(),
            template_type=GameTemplateType.CRISIS_PROTOCOL,
            simulation_ref=simulation_data.get("simulation_id", ""),
        )
        
        # Narrative layer
        manifest.narrative = NarrativeLayer(
            title=f"Crisis Protocol: {crisis_scenario}",
            description="Navigate crisis situations through strategic card play.",
            stakes=[
                "Immediate crisis management",
                "Long-term consequences",
                "Stakeholder trust",
            ],
            kpis=["crisis_contained", "resources_preserved", "trust_maintained"],
            scenario_context=crisis_scenario,
        )
        
        # Mechanic layer
        manifest.mechanic = MechanicLayer(
            rules=[
                {"type": "draw", "description": "Draw crisis cards each round"},
                {"type": "play", "description": "Play response cards"},
                {"type": "resolve", "description": "Resolve crisis effects"},
            ],
            resources=[
                {"name": "action_points", "initial": 3, "min": 0, "max": 5},
                {"name": "emergency_fund", "initial": 100, "min": 0, "max": 200},
                {"name": "public_trust", "initial": 75, "min": 0, "max": 100},
            ],
            trade_offs=[
                {"choice": "quick_fix", "description": "Immediate gain, future debt"},
                {"choice": "cautious_approach", "description": "Slow but stable"},
            ],
            win_conditions=["Crisis contained", "Trust above 50%"],
            lose_conditions=["Total collapse", "Trust at 0%"],
        )
        
        # Visual layer
        manifest.visual = VisualLayer(
            xr_assets=["card_deck_3d", "crisis_meter", "trust_gauge"],
            environment="war_room",
            ui_template="crisis_ui",
        )
        
        # Generate crisis cards
        cards = self._generate_crisis_cards(crisis_scenario)
        
        return manifest, cards
    
    def _generate_crisis_cards(self, scenario: str) -> List[CrisisCard]:
        """Generate crisis cards"""
        cards = []
        
        # Quick fix card
        cards.append(CrisisCard(
            card_id=generate_id(),
            title="Quick Fix",
            description="Apply immediate patch to contain the crisis.",
            immediate_gain={"crisis_reduction": 30},
            long_term_risk={"technical_debt": 20, "recurrence_chance": 0.3},
            cost={"action_points": 1, "emergency_fund": 20},
            category="response",
            rarity="common",
        ))
        
        # Expert consultation card
        cards.append(CrisisCard(
            card_id=generate_id(),
            title="Expert Consultation",
            description="Bring in specialists for thorough analysis.",
            immediate_gain={"crisis_reduction": 15, "insight": 25},
            long_term_risk={"cost_overrun": 10},
            cost={"action_points": 2, "emergency_fund": 40},
            category="strategy",
            rarity="uncommon",
        ))
        
        # Public statement card
        cards.append(CrisisCard(
            card_id=generate_id(),
            title="Transparent Communication",
            description="Issue honest public statement about the situation.",
            immediate_gain={"trust_boost": 10},
            long_term_risk={"reputation_exposure": 15},
            cost={"action_points": 1},
            category="communication",
            rarity="common",
        ))
        
        # Emergency measures card
        cards.append(CrisisCard(
            card_id=generate_id(),
            title="Emergency Measures",
            description="Activate emergency protocols.",
            immediate_gain={"crisis_reduction": 50},
            long_term_risk={"resource_drain": 30, "team_burnout": 20},
            cost={"action_points": 3, "emergency_fund": 60},
            category="response",
            rarity="rare",
        ))
        
        return cards


class ExplorerGenerator:
    """
    Generate The Explorer template.
    
    Per spec: Explorer les conséquences RH / légales complexes.
    """
    
    def generate(
        self,
        simulation_data: Dict[str, Any],
        scenario_tree: Dict[str, Any] = None,
    ) -> Tuple[GameManifest, List[ScenarioBranch]]:
        """Generate explorer game with branching scenarios"""
        manifest = GameManifest(
            manifest_id=generate_id(),
            template_type=GameTemplateType.THE_EXPLORER,
            simulation_ref=simulation_data.get("simulation_id", ""),
        )
        
        # Narrative layer
        manifest.narrative = NarrativeLayer(
            title="The Explorer: Decision Consequences",
            description="Navigate complex decisions and explore their consequences.",
            stakes=[
                "HR implications",
                "Legal considerations",
                "Ethical dimensions",
            ],
            kpis=["outcome_quality", "risk_management", "stakeholder_satisfaction"],
            scenario_context=simulation_data.get("context", "Complex organizational decision"),
        )
        
        # Mechanic layer
        manifest.mechanic = MechanicLayer(
            rules=[
                {"type": "choice", "description": "Make choices at each branch"},
                {"type": "consequence", "description": "Experience consequences"},
                {"type": "backtrack", "description": "Option to explore alternatives"},
            ],
            trade_offs=[
                {"choice": "ethical_vs_profitable", "description": "Ethics vs profit"},
                {"choice": "short_vs_long", "description": "Short-term vs long-term"},
            ],
            win_conditions=["Navigate to positive outcome"],
            lose_conditions=["Critical failure state reached"],
        )
        
        # Visual layer
        manifest.visual = VisualLayer(
            xr_assets=["branch_tree_3d", "consequence_visualizer", "timeline_view"],
            environment="decision_chamber",
            ui_template="explorer_ui",
        )
        
        # Generate branches
        branches = self._generate_branches(scenario_tree)
        
        return manifest, branches
    
    def _generate_branches(self, tree: Dict = None) -> List[ScenarioBranch]:
        """Generate scenario branches"""
        branches = []
        
        # Root branch
        root = ScenarioBranch(
            branch_id="root",
            title="Initial Situation",
            description="You face a complex organizational challenge.",
            choice_text="How do you approach this situation?",
            next_branches=["branch_a", "branch_b"],
        )
        branches.append(root)
        
        # Branch A - Proactive approach
        branch_a = ScenarioBranch(
            branch_id="branch_a",
            title="Proactive Approach",
            description="Take immediate action to address the challenge.",
            choice_text="You decided to act quickly.",
            consequences=[
                "Resources committed early",
                "Stakeholders notified",
                "Risk of incomplete analysis",
            ],
            next_branches=["branch_a1", "branch_a2"],
        )
        branches.append(branch_a)
        
        # Branch B - Analytical approach
        branch_b = ScenarioBranch(
            branch_id="branch_b",
            title="Analytical Approach",
            description="Gather more information before acting.",
            choice_text="You decided to analyze first.",
            consequences=[
                "Better understanding achieved",
                "Time invested in analysis",
                "Possible opportunity cost",
            ],
            next_branches=["branch_b1", "branch_b2"],
        )
        branches.append(branch_b)
        
        return branches


# ============================================================================
# GAME TEMPLATE GENERATOR (MAIN)
# ============================================================================

class GameTemplateGenerator:
    """
    Main game template generator.
    
    Per spec: Agent L2/L3 — Game Design Agent
    """
    
    def __init__(self):
        self.optimizer_gen = OptimizerGenerator()
        self.crisis_gen = CrisisProtocolGenerator()
        self.explorer_gen = ExplorerGenerator()
        
        # Storage
        self._manifests: Dict[str, GameManifest] = {}
    
    def generate(
        self,
        template_type: GameTemplateType,
        simulation_data: Dict[str, Any],
        **kwargs,
    ) -> GameManifest:
        """
        Generate game template from simulation.
        
        Per spec: LLM génère des blueprints de jeux sérieux (JSON)
        """
        if template_type == GameTemplateType.THE_OPTIMIZER:
            manifest = self.optimizer_gen.generate(
                simulation_data,
                kwargs.get("kpis", ["efficiency", "cost", "quality"]),
            )
        
        elif template_type == GameTemplateType.CRISIS_PROTOCOL:
            manifest, cards = self.crisis_gen.generate(
                simulation_data,
                kwargs.get("crisis_scenario", "General Crisis"),
            )
            # Store cards in manifest
            manifest.mechanic.rules.append({
                "type": "cards",
                "card_ids": [c.card_id for c in cards],
            })
        
        elif template_type == GameTemplateType.THE_EXPLORER:
            manifest, branches = self.explorer_gen.generate(
                simulation_data,
                kwargs.get("scenario_tree"),
            )
            # Store branches in manifest
            manifest.mechanic.rules.append({
                "type": "branches",
                "branch_ids": [b.branch_id for b in branches],
            })
        
        else:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # Sign manifest
        manifest.signature = sign_artifact({
            "manifest_id": manifest.manifest_id,
            "template_type": manifest.template_type.value,
            "simulation_ref": manifest.simulation_ref,
        }, "game_design_agent")
        
        manifest.created_by = "L2_GameArchitect"
        
        self._manifests[manifest.manifest_id] = manifest
        
        logger.info(
            f"Generated {template_type.value} manifest {manifest.manifest_id}"
        )
        
        return manifest
    
    def export_manifest(self, manifest_id: str) -> Dict[str, Any]:
        """
        Export manifest as JSON.
        
        Per spec output: GAME_MANIFEST.json (signé OPA)
        """
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            return {}
        
        return {
            "schema_version": "1.0",
            "manifest_id": manifest.manifest_id,
            "template_type": manifest.template_type.value,
            "narrative": {
                "title": manifest.narrative.title,
                "description": manifest.narrative.description,
                "stakes": manifest.narrative.stakes,
                "kpis": manifest.narrative.kpis,
            },
            "mechanic": {
                "rules": manifest.mechanic.rules,
                "resources": manifest.mechanic.resources,
                "trade_offs": manifest.mechanic.trade_offs,
                "win_conditions": manifest.mechanic.win_conditions,
                "lose_conditions": manifest.mechanic.lose_conditions,
            },
            "visual": {
                "xr_assets": manifest.visual.xr_assets,
                "environment": manifest.visual.environment,
                "ui_template": manifest.visual.ui_template,
            },
            "simulation_ref": manifest.simulation_ref,
            "opa_compliant": manifest.opa_compliant,
            "signature": manifest.signature,
            "created_by": manifest.created_by,
        }
    
    def get_manifest(self, manifest_id: str) -> Optional[GameManifest]:
        """Get manifest by ID"""
        return self._manifests.get(manifest_id)


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_generator() -> GameTemplateGenerator:
    """Create game template generator"""
    return GameTemplateGenerator()
