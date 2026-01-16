"""
============================================================================
CHE·NU™ V69 — CORE ENGINES MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_CAUSAL_*.md, CHE-NU_WORLDENGINE_*.md
Principle: GOUVERNANCE > EXÉCUTION

"CHE·NU ne dit pas quoi faire. Il révèle ce qui compte vraiment."
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import uuid
import hashlib
import json


# ============================================================================
# SLOT MODELS
# ============================================================================

@dataclass
class Slot:
    """
    A slot is a causal variable in the simulation.
    
    Per spec: Les Slots deviennent des variables causales
    """
    slot_id: str
    name: str
    value: float
    unit: str = ""
    
    # Causal metadata
    causal_parents: List[str] = field(default_factory=list)
    causal_children: List[str] = field(default_factory=list)
    
    # Impact score
    impact_score: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 1.0)
    
    # Metadata
    domain: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# DAG MODELS (Directed Acyclic Graph)
# ============================================================================

class EdgeType(str, Enum):
    """Types of causal edges"""
    DIRECT = "direct"
    INDIRECT = "indirect"
    CONFOUNDED = "confounded"


@dataclass
class CausalEdge:
    """
    An edge in the causal DAG.
    
    Per spec: Relations cause → effet
    """
    edge_id: str
    source_slot: str
    target_slot: str
    
    # Edge properties
    edge_type: EdgeType = EdgeType.DIRECT
    strength: float = 0.0  # -1 to 1
    p_value: float = 1.0  # Statistical significance
    
    # Validation
    validated: bool = False
    validator_id: str = ""


@dataclass
class CausalDAG:
    """
    Directed Acyclic Graph for causal reasoning.
    
    Per spec: Chaque simulation génère un DAG
    """
    dag_id: str
    name: str
    
    # Graph structure
    slots: Dict[str, Slot] = field(default_factory=dict)
    edges: List[CausalEdge] = field(default_factory=list)
    
    # Validation
    validated: bool = False
    validator_id: str = ""
    
    # Versioning
    version: int = 1
    parent_version: Optional[str] = None
    
    # Signature
    signature: str = ""
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# ARTIFACT MODELS
# ============================================================================

@dataclass
class Artifact:
    """
    A certified artifact from WorldEngine.
    
    Per spec: Artifact JSON certifié, reproductible
    """
    artifact_id: str
    
    # I/O
    inputs: List[Slot] = field(default_factory=list)
    outputs: List[Slot] = field(default_factory=list)
    
    # Causal info
    causal_rule_id: str = ""
    dag_ref: str = ""
    
    # Certification
    hash: str = ""
    signature: str = ""
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"


@dataclass
class WorldState:
    """
    The state of the world at a given time.
    
    Per spec: WorldState.json input
    """
    state_id: str
    
    # Slots
    slots: Dict[str, Slot] = field(default_factory=dict)
    
    # DAG reference
    dag_ref: str = ""
    
    # Simulation time
    sim_time: int = 0
    
    # Signature
    signature: str = ""


# ============================================================================
# INTERVENTION MODELS
# ============================================================================

class InterventionType(str, Enum):
    """Types of causal interventions"""
    DO = "do"  # do(X) - set value
    OBSERVE = "observe"  # condition on observation
    COUNTERFACTUAL = "counterfactual"  # what-if past


@dataclass
class Intervention:
    """
    A causal intervention (do-calculus).
    
    Per spec: Intervention simulation (do-calculus inspired)
    """
    intervention_id: str
    slot_id: str
    
    # Intervention
    intervention_type: InterventionType
    new_value: float
    
    # Context
    description: str = ""
    
    # Audit
    approved: bool = False
    approver_id: str = ""


@dataclass
class CounterfactualQuery:
    """
    A counterfactual query.
    
    Per spec: "What if X had not happened?"
    """
    query_id: str
    
    # The factual state
    factual_state: Dict[str, float] = field(default_factory=dict)
    
    # The counterfactual intervention
    intervention: Intervention = None
    
    # Question
    question: str = ""
    target_slot: str = ""


# ============================================================================
# SENSITIVITY MODELS
# ============================================================================

@dataclass
class SensitivityScore:
    """
    Sensitivity/impact score for a slot.
    
    Per spec: Score d'impact (%), Intervalle de confiance
    """
    slot_id: str
    
    # Impact
    impact_percent: float = 0.0  # 0-100
    confidence_low: float = 0.0
    confidence_high: float = 0.0
    
    # Stability
    instability_score: float = 0.0  # Higher = more volatile
    
    # Alert
    is_critical: bool = False
    alert_message: str = ""


# ============================================================================
# FEEDBACK LOOP MODELS
# ============================================================================

class FeedbackType(str, Enum):
    """Types of feedback loops"""
    POSITIVE = "positive"  # Exponential growth
    NEGATIVE = "negative"  # Stabilization


@dataclass
class FeedbackLoop:
    """
    A feedback loop in the simulation.
    
    Per spec: Positive (growth) / Negative (stabilization)
    """
    loop_id: str
    name: str
    
    # Type
    feedback_type: FeedbackType
    
    # Slots involved
    slot_chain: List[str] = field(default_factory=list)
    
    # Parameters
    gain: float = 1.0
    damping: float = 0.0
    
    # Safety
    safety_threshold: float = 100.0
    is_monitored: bool = True


# ============================================================================
# GAME BRIDGE MODELS
# ============================================================================

class GameMechanicType(str, Enum):
    """Types of game mechanics"""
    POINTS = "points"
    HEALTH_BAR = "health_bar"
    BONUS = "bonus"
    PENALTY = "penalty"
    FOG_OF_WAR = "fog_of_war"


@dataclass
class GameMapping:
    """
    Mapping from simulation to game mechanic.
    
    Per spec: Budget → Points, KPI → Barres, etc.
    """
    mapping_id: str
    slot_id: str
    
    # Game mechanic
    mechanic_type: GameMechanicType
    mechanic_name: str = ""
    
    # Transform
    scale_factor: float = 1.0
    offset: float = 0.0
    
    # Validation
    validated: bool = False


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
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def sign_artifact(data: Dict[str, Any], signer_id: str) -> str:
    """Sign an artifact (mock PQC)"""
    payload = json.dumps(data, sort_keys=True, default=str)
    return compute_hash(f"{payload}:{signer_id}")


def verify_signature(data: Dict[str, Any], signature: str, signer_id: str) -> bool:
    """Verify artifact signature"""
    expected = sign_artifact(data, signer_id)
    return signature == expected
