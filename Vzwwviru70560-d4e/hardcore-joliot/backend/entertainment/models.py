"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_ENT_*.md
Principle: GOUVERNANCE > EXÉCUTION

CHE·NU ne crée pas un moteur de jeu.
Il génère des templates interprétables par le moteur XR existant.
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import uuid
import hashlib
import json


# ============================================================================
# GAME TEMPLATE TYPES
# ============================================================================

class GameTemplateType(str, Enum):
    """
    Supported game templates.
    
    Per spec: The Optimizer, Crisis Protocol, The Explorer
    """
    THE_OPTIMIZER = "the_optimizer"  # Resource management
    CRISIS_PROTOCOL = "crisis_protocol"  # Cards / dilemmas
    THE_EXPLORER = "the_explorer"  # Branching scenarios


class GameLayer(str, Enum):
    """
    Game design layers.
    
    Per spec trois couches: Narrative, Mécanique, Visuelle
    """
    NARRATIVE = "narrative"  # KPI → stakes
    MECHANIC = "mechanic"  # Rules, costs, trade-offs
    VISUAL = "visual"  # Existing XR assets


# ============================================================================
# GAME MANIFEST MODELS
# ============================================================================

@dataclass
class NarrativeLayer:
    """
    Narrative layer: KPI → enjeux.
    """
    title: str = ""
    description: str = ""
    stakes: List[str] = field(default_factory=list)
    kpis: List[str] = field(default_factory=list)
    scenario_context: str = ""


@dataclass
class MechanicLayer:
    """
    Mechanic layer: rules, costs, trade-offs.
    """
    rules: List[Dict[str, Any]] = field(default_factory=list)
    resources: List[Dict[str, Any]] = field(default_factory=list)
    costs: Dict[str, float] = field(default_factory=dict)
    trade_offs: List[Dict[str, str]] = field(default_factory=list)
    win_conditions: List[str] = field(default_factory=list)
    lose_conditions: List[str] = field(default_factory=list)


@dataclass
class VisualLayer:
    """
    Visual layer: existing XR assets.
    """
    xr_assets: List[str] = field(default_factory=list)
    environment: str = "default"
    ui_template: str = "standard"
    color_scheme: Dict[str, str] = field(default_factory=dict)


@dataclass
class GameManifest:
    """
    Game manifest (signé OPA).
    
    Per spec output: GAME_MANIFEST.json
    """
    manifest_id: str
    template_type: GameTemplateType
    
    # Layers
    narrative: NarrativeLayer = field(default_factory=NarrativeLayer)
    mechanic: MechanicLayer = field(default_factory=MechanicLayer)
    visual: VisualLayer = field(default_factory=VisualLayer)
    
    # WorldEngine link
    simulation_ref: str = ""
    
    # OPA
    opa_compliant: bool = True
    opa_policy_ref: str = ""
    
    # Signature
    signature: str = ""
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


# ============================================================================
# GAME LOGIC MODELS
# ============================================================================

@dataclass
class GameAction:
    """A player action"""
    action_id: str
    action_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SimulationResult:
    """Result from WorldEngine simulation"""
    result_id: str
    action_id: str
    
    # Outcomes
    state_changes: Dict[str, Any] = field(default_factory=dict)
    divergence_score: float = 0.0
    
    # Causal trace
    causal_chain: List[str] = field(default_factory=list)


@dataclass
class GameFeedback:
    """
    Feedback for player.
    
    Per spec cycle: Action → Simulation → Divergence → Feedback
    """
    feedback_id: str
    action_id: str
    
    # Feedback content
    message: str = ""
    impact_summary: str = ""
    
    # Scores
    immediate_impact: float = 0.0
    long_term_risk: float = 0.0
    
    # XR visualization
    xr_visualization_ref: str = ""


# ============================================================================
# TRUST SCORE MODELS
# ============================================================================

class TrustPillar(str, Enum):
    """
    Trust score pillars.
    
    Per spec: Conformité, Résilience, Précision
    """
    CONFORMITY = "conformity"  # OPA Alignment
    RESILIENCE = "resilience"  # Causal Stability
    PRECISION = "precision"  # Prediction Gap


@dataclass
class TrustScore:
    """
    Player trust score.
    
    Per spec: Mesurer la qualité décisionnelle humaine
    """
    score_id: str
    player_id: str
    
    # Pillar scores (0-100)
    conformity_score: float = 0.0  # OPA alignment
    resilience_score: float = 0.0  # Causal stability
    precision_score: float = 0.0  # Prediction gap
    
    # Overall
    overall_score: float = 0.0
    
    # History
    decision_count: int = 0
    
    # Timestamp
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LeaderboardEntry:
    """
    Leaderboard entry.
    
    Per spec: Scores anonymisés
    """
    entry_id: str
    anonymous_id: str  # Anonymized player ID
    
    # Score
    score: float = 0.0
    rank: int = 0
    
    # Badge
    badge: str = ""  # Trust-Certified badge
    
    # Artifact
    artifact_ref: str = ""
    signature: str = ""


@dataclass
class TrustBadge:
    """
    Trust-Certified badge.
    
    Per spec: Badges Trust-Certified
    """
    badge_id: str
    player_id: str
    
    # Badge info
    level: str = "bronze"  # bronze, silver, gold, platinum
    category: str = ""
    
    # Proof
    artifact_ref: str = ""
    signature: str = ""
    
    # Timestamp
    issued_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# CARD MODELS (Crisis Protocol)
# ============================================================================

@dataclass
class CrisisCard:
    """
    Crisis card for Crisis Protocol game.
    
    Per spec: Cartes à gains immédiats / risques longs termes
    """
    card_id: str
    title: str
    description: str = ""
    
    # Effects
    immediate_gain: Dict[str, float] = field(default_factory=dict)
    long_term_risk: Dict[str, float] = field(default_factory=dict)
    
    # Cost
    cost: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    category: str = ""
    rarity: str = "common"


# ============================================================================
# SCENARIO MODELS (The Explorer)
# ============================================================================

@dataclass
class ScenarioBranch:
    """
    Scenario branch for The Explorer game.
    
    Per spec: Explorer les conséquences RH / légales complexes
    """
    branch_id: str
    title: str
    description: str = ""
    
    # Choice
    choice_text: str = ""
    
    # Consequences
    consequences: List[str] = field(default_factory=list)
    next_branches: List[str] = field(default_factory=list)
    
    # Simulation
    simulation_params: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def compute_hash(data: Any) -> str:
    """Compute hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def sign_artifact(data: Dict[str, Any], signer_id: str) -> str:
    """Sign an artifact"""
    payload = json.dumps(data, sort_keys=True)
    return compute_hash(f"{payload}:{signer_id}")


def anonymize_id(player_id: str) -> str:
    """Anonymize player ID for leaderboard"""
    return compute_hash(player_id)[:12]
