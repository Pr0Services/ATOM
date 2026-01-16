"""
============================================================================
CHE·NU™ V69 — INDUSTRIALISATION MODULE MODELS
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_INDUSTRIALISATION_PLAN.md
- CHE-NU_XR_PACK_AUTOGEN_V1_4.md
- CHE-NU_WORLD_SIM_GAMEPLAY_MECHANICS.md
- CHE-NU_Prompt_Collection_Architecture.md
- CHE-NU_V52_API_Agent_Management_Best_Practices.md
- CHE-NU_V52_OPA_Policy_Bundles_Templates.md

"POC → MVP → Enterprise: GOUVERNANCE > EXÉCUTION"
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import hashlib
import json


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    return str(uuid.uuid4())

def compute_hash(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif isinstance(data, bytes):
        pass
    else:
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


# ============================================================================
# 1. INDUSTRIALISATION PLAN MODELS
# ============================================================================

class ProductLayer(str, Enum):
    """Product architecture layers"""
    UX_XR = "ux_xr"
    EXPLAINABILITY = "explainability"
    SIMULATION = "simulation"
    AGENT = "agent"
    GOVERNANCE = "governance"
    DATA_FABRIC = "data_fabric"


class IndustrializationPhase(str, Enum):
    """Phases from POC to Enterprise"""
    POC = "poc"
    MVP = "mvp"
    PILOT = "pilot"
    ENTERPRISE = "enterprise"


@dataclass
class ProductLayerSpec:
    """Product layer specification"""
    layer: ProductLayer
    description: str
    requirements: List[str] = field(default_factory=list)
    ready: bool = False


@dataclass
class IndustrializationPlan:
    """
    Industrialization Plan.
    
    Per spec: POC XR++ → Enterprise V1
    """
    plan_id: str
    current_phase: IndustrializationPhase = IndustrializationPhase.POC
    
    layers: List[ProductLayerSpec] = field(default_factory=list)
    
    # Non-negotiable rules
    no_ai_sovereignty: bool = True
    hitl_for_real_transitions: bool = True
    
    # Objectives
    allow_data_connection: bool = True
    allow_future_simulation: bool = True
    allow_understanding_before_action: bool = True
    no_total_autonomy: bool = True


# ============================================================================
# 2. XR PACK AUTOGEN MODELS
# ============================================================================

@dataclass
class XRPackManifest:
    """XR Pack manifest"""
    schema_version: str = "v1"
    simulation_id: str = ""
    tenant_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    files: List[str] = field(default_factory=lambda: [
        "manifest.v1.json",
        "replay.v1.json",
        "heatmap.v1.json",
        "diff.v1.json",
        "explain.v1.json",
    ])


@dataclass
class ReplayFrame:
    """A replay frame"""
    step: int
    state: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class HeatmapTile:
    """Heatmap tile (e.g., sphere)"""
    tile_id: str
    name: str
    
    risk_score: float = 0.0
    cost_score: float = 0.0
    velocity_score: float = 0.0


@dataclass
class DiffEntry:
    """Scenario diff entry"""
    metric: str
    baseline: float
    scenario: float
    delta: float = 0.0
    delta_percent: float = 0.0


@dataclass
class XRPack:
    """
    XR Pack for WebXR consumption.
    
    Per spec: READ ONLY, static, no POST/PUT
    """
    pack_id: str
    manifest: XRPackManifest = field(default_factory=XRPackManifest)
    
    replay: List[ReplayFrame] = field(default_factory=list)
    heatmap: List[HeatmapTile] = field(default_factory=list)
    diff: List[DiffEntry] = field(default_factory=list)
    explain: List[Dict[str, str]] = field(default_factory=list)
    
    # Governance
    read_only: bool = True  # ENFORCED
    opa_approved: bool = False


# ============================================================================
# 3. GAMEPLAY MECHANICS MODELS
# ============================================================================

class GameplayMechanicType(str, Enum):
    """Types of gameplay mechanics"""
    QUEST = "quest"       # Business objective
    TIMELINE = "timeline" # Sprint
    RISK = "risk"         # Anomaly
    RESOURCE = "resource" # Budget/time/energy


@dataclass
class Quest:
    """A quest (business objective)"""
    quest_id: str
    name: str
    objective: str
    
    progress: float = 0.0  # 0-1
    completed: bool = False
    
    # Governance
    real_impact_simulated: bool = True
    justified: bool = True


@dataclass
class GameplayState:
    """
    Gameplay state for simulation.
    
    Per spec: Gameplay is observed, not controlled
    """
    state_id: str
    
    quests: List[Quest] = field(default_factory=list)
    resources: Dict[str, float] = field(default_factory=dict)
    risks: List[str] = field(default_factory=list)
    current_timeline: int = 0
    
    # Rules
    no_points_without_impact: bool = True
    no_reward_without_justification: bool = True
    human_decides: bool = True


# ============================================================================
# 4. PROMPT COLLECTION MODELS
# ============================================================================

class PromptAxis(str, Enum):
    """Prompt classification axes"""
    ROLE = "role"   # Who is speaking
    AGENT = "agent" # Who is executing
    TASK = "task"   # What is being done


@dataclass
class PromptAsset:
    """
    A structured prompt asset.
    
    Per spec: All three axes required
    """
    asset_id: str
    
    role: str      # Required
    agent: str     # Required
    task: str      # Required
    
    content: str = ""
    version: str = "1.0"
    
    # Metadata
    layer: str = "task"  # system, operating_mode, role, agent, task
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PromptLibrary:
    """Governed prompt library"""
    library_id: str
    assets: Dict[str, PromptAsset] = field(default_factory=dict)
    
    # Stats
    total_prompts: int = 0
    by_role: Dict[str, int] = field(default_factory=dict)
    by_agent: Dict[str, int] = field(default_factory=dict)


# ============================================================================
# 5. API AGENT MANAGEMENT MODELS
# ============================================================================

@dataclass
class AgentRegistryEntry:
    """Agent registry entry with metadata"""
    agent_id: str
    blueprint_id: str
    
    scope: str = ""
    level: str = "L0"
    sphere: str = ""
    
    # Evaluation
    eval_score: float = 0.0
    last_eval: Optional[datetime] = None
    
    # API info
    api_endpoint: str = ""
    rate_limit: int = 100


@dataclass
class EvaluationResult:
    """Multi-level evaluation result"""
    eval_id: str
    agent_id: str
    
    accuracy: float = 0.0
    reliability: float = 0.0
    governance_compliance: float = 0.0
    
    overall_score: float = 0.0
    passed: bool = False
    
    evaluated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class APIAgentManagementConfig:
    """
    API & Agent Management configuration.
    
    Per spec: Structure, not restriction
    """
    config_id: str
    
    # Registry
    total_agents: int = 287
    total_engines: int = 95
    total_spheres: int = 9
    
    # Architecture
    uses_gateway: bool = True
    uses_service_mesh: bool = True
    uses_observability: bool = True
    nova_authority: bool = True


# ============================================================================
# 6. OPA POLICY BUNDLES MODELS
# ============================================================================

@dataclass
class PolicyRule:
    """An OPA policy rule"""
    rule_id: str
    name: str
    description: str
    
    default_action: str = "deny"  # default deny
    rego_snippet: str = ""


@dataclass
class PolicyBundle:
    """
    OPA Policy Bundle.
    
    Per spec: default deny, allow by explicit rule
    """
    bundle_id: str
    name: str
    
    rules: List[PolicyRule] = field(default_factory=list)
    
    # Structure
    env_policies: List[str] = field(default_factory=lambda: ["labs", "pilot", "prod"])
    sphere_policies: List[str] = field(default_factory=list)
    agent_policies: List[str] = field(default_factory=lambda: ["l0", "l1", "l2", "l3"])


@dataclass
class BundleRegistry:
    """Registry of all policy bundles"""
    registry_id: str
    bundles: Dict[str, PolicyBundle] = field(default_factory=dict)
    
    # Core principle
    default_deny: bool = True


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Utils
    "generate_id", "compute_hash",
    # Industrialization
    "ProductLayer", "IndustrializationPhase",
    "ProductLayerSpec", "IndustrializationPlan",
    # XR Pack
    "XRPackManifest", "ReplayFrame", "HeatmapTile", "DiffEntry", "XRPack",
    # Gameplay
    "GameplayMechanicType", "Quest", "GameplayState",
    # Prompt Collection
    "PromptAxis", "PromptAsset", "PromptLibrary",
    # API Agent Management
    "AgentRegistryEntry", "EvaluationResult", "APIAgentManagementConfig",
    # OPA Bundles
    "PolicyRule", "PolicyBundle", "BundleRegistry",
]
