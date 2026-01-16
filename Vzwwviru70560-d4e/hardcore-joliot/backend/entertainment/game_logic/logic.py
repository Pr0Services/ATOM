"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT LLM GAME LOGIC PROMPTS
============================================================================
Spec: GPT1/CHE-NU_ENT_LLM_GAME_LOGIC_PROMPTS.md

Meta-Prompt: Agent L2-GameArchitect
- Fidélité causale
- Gouvernance OPA
- Engagement décisionnel

Cycle: Action joueur → Simulation → Divergence → Feedback

Prompts by Template:
- The Optimizer: Resource balancing
- Crisis Protocol: Immediate gains / long-term risks
- The Explorer: HR/Legal consequences
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging

from ..models import (
    GameManifest,
    GameTemplateType,
    GameAction,
    SimulationResult,
    GameFeedback,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# META PROMPT TEMPLATES
# ============================================================================

META_PROMPT_GAME_ARCHITECT = """
Tu es l'agent L2-GameArchitect de CHE·NU™.

PRINCIPES FONDAMENTAUX:
1. Fidélité Causale: Toute mécanique de jeu doit refléter les relations causales réelles du WorldEngine
2. Gouvernance OPA: Aucune action de jeu ne peut contourner les politiques de sécurité
3. Engagement Décisionnel: Le joueur doit comprendre les conséquences de ses choix

CONTRAINTES:
- Pas de "win buttons" (solutions triviales)
- Pas de hasard pur (tout effet doit avoir une cause traçable)
- Transparence sur les trade-offs

OUTPUT: JSON structuré conforme au schema GAME_MANIFEST
"""

PROMPT_OPTIMIZER = """
TEMPLATE: The Optimizer
OBJECTIF: Équilibrer ressources critiques sous contraintes

RÈGLES DE GÉNÉRATION:
1. Chaque ressource a un impact causal sur au moins 2 KPIs
2. Toute allocation a un coût d'opportunité visible
3. Les contraintes doivent créer des dilemmes réels

STRUCTURE DE DÉCISION:
- Input: État actuel des ressources
- Output: Nouvelle allocation
- Feedback: Impact sur KPIs avec explication causale
"""

PROMPT_CRISIS = """
TEMPLATE: Crisis Protocol
OBJECTIF: Créer des cartes à gains immédiats / risques longs termes

RÈGLES DE GÉNÉRATION:
1. Chaque carte a un gain immédiat ET un risque long terme
2. Le risque doit être caché partiellement (incertitude réaliste)
3. Certaines cartes peuvent se combiner (synergies/conflits)

STRUCTURE DE CARTE:
- Gain immédiat: Effet visible et quantifiable
- Risque caché: Probabilité + impact potentiel
- Interactions: Cartes qui amplifient/annulent l'effet
"""

PROMPT_EXPLORER = """
TEMPLATE: The Explorer
OBJECTIF: Explorer les conséquences RH / légales complexes

RÈGLES DE GÉNÉRATION:
1. Chaque branche révèle des conséquences inattendues mais cohérentes
2. Les dimensions RH et légales doivent être intégrées
3. Pas de "meilleure réponse" évidente

STRUCTURE DE BRANCHE:
- Choix: Description neutre de l'option
- Conséquences immédiates: Effets visibles
- Conséquences différées: Effets à révéler plus tard
- Dimension éthique: Aspect moral du choix
"""


# ============================================================================
# GAME LOGIC ENGINE
# ============================================================================

class GameLogicEngine:
    """
    Engine for processing game logic with LLM prompts.
    
    Per spec cycle: Action joueur → Simulation → Divergence → Feedback
    """
    
    def __init__(self, simulation_callback: Callable = None):
        self._simulation_callback = simulation_callback or self._mock_simulation
        
        # State tracking
        self._game_states: Dict[str, Dict[str, Any]] = {}
        self._actions: Dict[str, List[GameAction]] = {}
        self._results: Dict[str, List[SimulationResult]] = {}
    
    def _mock_simulation(self, action: GameAction, state: Dict) -> Dict[str, Any]:
        """Mock simulation for testing"""
        return {
            "state_changes": {"impact": 10},
            "divergence_score": 0.15,
            "causal_chain": ["action", "effect1", "effect2"],
        }
    
    def initialize_game(
        self,
        game_id: str,
        manifest: GameManifest,
    ) -> Dict[str, Any]:
        """Initialize game state from manifest"""
        state = {
            "game_id": game_id,
            "template_type": manifest.template_type.value,
            "resources": {
                r["name"]: r["initial"]
                for r in manifest.mechanic.resources
            },
            "turn": 0,
            "status": "active",
        }
        
        self._game_states[game_id] = state
        self._actions[game_id] = []
        self._results[game_id] = []
        
        return state
    
    def process_action(
        self,
        game_id: str,
        action: GameAction,
    ) -> Tuple[SimulationResult, GameFeedback]:
        """
        Process player action through the game cycle.
        
        Per spec: Action joueur → Simulation → Divergence → Feedback
        """
        state = self._game_states.get(game_id)
        if not state:
            raise ValueError(f"Game {game_id} not found")
        
        # Store action
        self._actions[game_id].append(action)
        
        # Step 1: Simulate
        sim_output = self._simulation_callback(action, state)
        
        result = SimulationResult(
            result_id=generate_id(),
            action_id=action.action_id,
            state_changes=sim_output.get("state_changes", {}),
            divergence_score=sim_output.get("divergence_score", 0),
            causal_chain=sim_output.get("causal_chain", []),
        )
        
        self._results[game_id].append(result)
        
        # Step 2: Apply state changes
        for key, value in result.state_changes.items():
            if key in state.get("resources", {}):
                state["resources"][key] += value
        
        state["turn"] += 1
        
        # Step 3: Generate feedback
        feedback = self._generate_feedback(action, result, state)
        
        return result, feedback
    
    def _generate_feedback(
        self,
        action: GameAction,
        result: SimulationResult,
        state: Dict[str, Any],
    ) -> GameFeedback:
        """Generate feedback for player"""
        # Analyze divergence
        divergence = result.divergence_score
        
        if divergence < 0.1:
            impact_level = "minimal"
        elif divergence < 0.3:
            impact_level = "moderate"
        elif divergence < 0.5:
            impact_level = "significant"
        else:
            impact_level = "major"
        
        # Generate message based on template
        template_type = state.get("template_type", "")
        
        if template_type == GameTemplateType.THE_OPTIMIZER.value:
            message = f"Resource allocation applied. Impact level: {impact_level}"
            impact_summary = f"Your decision affected {len(result.state_changes)} metrics."
        
        elif template_type == GameTemplateType.CRISIS_PROTOCOL.value:
            message = f"Crisis response enacted. Divergence: {divergence:.1%}"
            impact_summary = f"Immediate effects applied. Long-term risks may emerge."
        
        elif template_type == GameTemplateType.THE_EXPLORER.value:
            message = f"Path chosen. Consequences unfolding..."
            impact_summary = f"Your choice has {len(result.causal_chain)} causal effects."
        
        else:
            message = f"Action processed. Impact: {impact_level}"
            impact_summary = "Effects applied to game state."
        
        feedback = GameFeedback(
            feedback_id=generate_id(),
            action_id=action.action_id,
            message=message,
            impact_summary=impact_summary,
            immediate_impact=sum(result.state_changes.values()) if result.state_changes else 0,
            long_term_risk=divergence * 100,
        )
        
        return feedback
    
    def get_game_state(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get current game state"""
        return self._game_states.get(game_id)
    
    def get_action_history(self, game_id: str) -> List[GameAction]:
        """Get action history for a game"""
        return self._actions.get(game_id, [])


# ============================================================================
# PROMPT MANAGER
# ============================================================================

class PromptManager:
    """
    Manage LLM prompts for game logic.
    """
    
    def __init__(self):
        self._prompts = {
            "meta": META_PROMPT_GAME_ARCHITECT,
            GameTemplateType.THE_OPTIMIZER: PROMPT_OPTIMIZER,
            GameTemplateType.CRISIS_PROTOCOL: PROMPT_CRISIS,
            GameTemplateType.THE_EXPLORER: PROMPT_EXPLORER,
        }
    
    def get_meta_prompt(self) -> str:
        """Get meta prompt for GameArchitect"""
        return self._prompts["meta"]
    
    def get_template_prompt(self, template_type: GameTemplateType) -> str:
        """Get prompt for specific template"""
        return self._prompts.get(template_type, "")
    
    def build_generation_prompt(
        self,
        template_type: GameTemplateType,
        simulation_context: Dict[str, Any],
    ) -> str:
        """Build complete prompt for game generation"""
        meta = self.get_meta_prompt()
        template = self.get_template_prompt(template_type)
        
        context = f"""
CONTEXTE DE SIMULATION:
- Domaine: {simulation_context.get('domain', 'General')}
- Variables: {simulation_context.get('variables', [])}
- Contraintes: {simulation_context.get('constraints', [])}
"""
        
        return f"{meta}\n\n{template}\n\n{context}"
    
    def build_feedback_prompt(
        self,
        action: GameAction,
        result: SimulationResult,
        template_type: GameTemplateType,
    ) -> str:
        """Build prompt for feedback generation"""
        return f"""
GENERATE PLAYER FEEDBACK

Template: {template_type.value}
Action: {action.action_type}
Divergence: {result.divergence_score:.2%}
Causal Chain: {' → '.join(result.causal_chain)}

Requirements:
1. Explain the causal relationship
2. Highlight trade-offs
3. Suggest next considerations (without revealing optimal path)
"""


# ============================================================================
# GAME LOGIC COORDINATOR
# ============================================================================

class GameLogicCoordinator:
    """
    Coordinate game logic with prompts and engine.
    """
    
    def __init__(self):
        self.engine = GameLogicEngine()
        self.prompts = PromptManager()
    
    def start_game(
        self,
        manifest: GameManifest,
    ) -> str:
        """Start a new game from manifest"""
        game_id = generate_id()
        self.engine.initialize_game(game_id, manifest)
        
        logger.info(f"Started game {game_id} with template {manifest.template_type.value}")
        return game_id
    
    def play_action(
        self,
        game_id: str,
        action_type: str,
        parameters: Dict[str, Any] = None,
    ) -> Tuple[SimulationResult, GameFeedback]:
        """Play an action in the game"""
        action = GameAction(
            action_id=generate_id(),
            action_type=action_type,
            parameters=parameters or {},
        )
        
        return self.engine.process_action(game_id, action)
    
    def get_generation_prompt(
        self,
        template_type: GameTemplateType,
        simulation_data: Dict[str, Any],
    ) -> str:
        """Get prompt for generating a new game"""
        return self.prompts.build_generation_prompt(template_type, simulation_data)
    
    def get_status(self, game_id: str) -> Dict[str, Any]:
        """Get game status"""
        state = self.engine.get_game_state(game_id)
        if not state:
            return {"error": "Game not found"}
        
        return {
            "game_id": game_id,
            "turn": state["turn"],
            "status": state["status"],
            "resources": state["resources"],
            "action_count": len(self.engine.get_action_history(game_id)),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_coordinator() -> GameLogicCoordinator:
    """Create game logic coordinator"""
    return GameLogicCoordinator()


def create_engine(simulation_callback: Callable = None) -> GameLogicEngine:
    """Create game logic engine"""
    return GameLogicEngine(simulation_callback)


def get_prompt_manager() -> PromptManager:
    """Get prompt manager"""
    return PromptManager()
