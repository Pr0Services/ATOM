"""
============================================================================
CHE·NU™ V69 — ENTERPRISE MODULE MODELS
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_XR_PACK_V1_7_TRUE_SIGNALS_EXPLAIN_ONDEMAND_WASM_VERIFY.md
- CHE-NU_Agent_Intelligence_System.md
- CHE-NU_Performance_Dashboard_Spec.md
- CHE-NU_FASTAPI_SERVICE_GENERATOR_V1_1.md
- CHE-NU_OPA_REAL_INTEGRATION_V1_3.md

Principle: GOUVERNANCE > EXÉCUTION, XR = READ ONLY
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
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

def sign_artifact(data: Dict[str, Any], signer: str) -> str:
    return compute_hash(f"{json.dumps(data, sort_keys=True, default=str)}:{signer}")


# ============================================================================
# 1. XR PACK V1.7 MODELS (True Signals + WASM Verify)
# ============================================================================

@dataclass
class SignalSeries:
    """Time series signal for a sphere"""
    step: int
    cost: float = 0.0
    risk: float = 0.0
    velocity: float = 1.0
    activity: int = 0
    incidents: int = 0
    quality: float = 1.0


@dataclass
class SphereSignals:
    """Signals for a single sphere"""
    sphere_id: str
    series: List[SignalSeries] = field(default_factory=list)


@dataclass
class GlobalMetrics:
    """Global system metrics per step"""
    step: int
    tokens: int = 0
    latency_ms: float = 0.0
    cache_hit_rate: float = 0.0
    policy_denies: int = 0


@dataclass
class TrueSignals:
    """
    signals.v1.json - Source of truth for heatmap
    
    Per spec V1.7: True Signals with sphere series
    """
    schema_version: str = "v1"
    tenant_id: str = ""
    simulation_id: str = ""
    trace_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    windowing_mode: str = "step"
    step_count: int = 0
    
    spheres: List[SphereSignals] = field(default_factory=list)
    global_metrics: List[GlobalMetrics] = field(default_factory=list)


@dataclass
class HeatmapTile:
    """A single tile in the heatmap"""
    sphere_id: str
    risk: float = 0.0
    cost: float = 0.0
    velocity: float = 1.0
    activity: int = 0
    incidents: int = 0
    quality: float = 1.0
    
    # Normalized scores
    scores: Dict[str, float] = field(default_factory=dict)
    sparkline: Dict[str, List[float]] = field(default_factory=dict)


@dataclass
class TrueHeatmap:
    """
    heatmap.v1.json - Calculated from signals
    
    Per spec: True Heatmap with scores per sphere
    """
    schema_version: str = "v1"
    tenant_id: str = ""
    simulation_id: str = ""
    trace_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    mode: str = "baseline"
    
    tiles: List[HeatmapTile] = field(default_factory=list)


@dataclass
class ExplainRange:
    """A range of explain items"""
    range_id: int
    from_step: int
    to_step: int
    file: str = ""
    sha256: str = ""


@dataclass
class ExplainItem:
    """A single explain item"""
    step: int
    why: List[str] = field(default_factory=list)
    sphere: str = ""
    impact: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0


@dataclass
class ExplainIndex:
    """
    explain/index.v1.json - Index for ranged explain
    
    Per spec: On-demand explain loading
    """
    schema_version: str = "v1"
    mode: str = "ranged"
    range_size: int = 500
    ranges: List[ExplainRange] = field(default_factory=list)


@dataclass
class WASMVerifyConfig:
    """WASM Ed25519 verification config"""
    enabled: bool = True
    signature_file: str = "xr_pack.v1.sig.json"
    pubkey_file: str = "xr_pack.v1.pubkey.json"
    wasm_asset: str = "ed25519_verify.wasm"


# ============================================================================
# 2. AGENT INTELLIGENCE SYSTEM MODELS
# ============================================================================

class AgentTier(str, Enum):
    """Agent hierarchy tier"""
    L0 = "L0"  # Specialist
    L1 = "L1"  # Manager
    L2 = "L2"  # Director
    L3 = "L3"  # Executive


class AgentDomain(str, Enum):
    """Functional domain"""
    FINANCE = "finance"
    HR = "hr"
    SALES = "sales"
    OPERATIONS = "operations"
    IT = "it"
    LEGAL = "legal"
    MARKETING = "marketing"
    PRODUCT = "product"
    GOVERNANCE = "governance"


class RiskLevel(str, Enum):
    """Agent risk level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentBlueprint:
    """
    Agent Blueprint - ADN canonique
    
    Per spec: Stable, versioned, reusable
    """
    blueprint_id: str
    domain: AgentDomain
    role: str
    mission: str = ""
    
    applicable_industries: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    allowed_actions: List[str] = field(default_factory=list)
    required_data: List[str] = field(default_factory=list)
    connected_tools: List[str] = field(default_factory=list)
    connected_apis: List[str] = field(default_factory=list)
    
    autonomy_level: float = 0.0  # 0-1
    governance_constraints: List[str] = field(default_factory=list)


@dataclass
class AgentInstance:
    """
    Agent Instance - 287+ agents
    
    Per spec: Concrete agent in CHE·NU
    """
    agent_id: str
    blueprint_id: str
    industry: str = ""
    tier: AgentTier = AgentTier.L0
    scope: str = ""
    risk_level: RiskLevel = RiskLevel.MEDIUM
    autonomy_level: float = 0.0
    enabled: bool = True


@dataclass
class AgentHealth:
    """Agent health metrics"""
    agent_id: str
    success_rate: float = 1.0
    avg_latency_ms: float = 0.0
    retry_rate: float = 0.0
    escalation_rate: float = 0.0
    last_active: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 3. PERFORMANCE DASHBOARD MODELS
# ============================================================================

@dataclass
class SystemHealth:
    """System health metrics"""
    uptime_seconds: int = 0
    request_rate: float = 0.0
    error_rate: float = 0.0
    latency_p95_ms: float = 0.0


@dataclass
class AgentMetrics:
    """Aggregated agent metrics"""
    active_agents: int = 0
    avg_latency_ms: float = 0.0
    success_rate: float = 1.0
    retry_rate: float = 0.0
    escalation_rate: float = 0.0


@dataclass
class MultiAgentMetrics:
    """Multi-agent coordination metrics"""
    parallel_tasks_ratio: float = 0.0
    coordination_overhead_ms: float = 0.0
    accuracy_parallel: float = 1.0
    accuracy_sequential: float = 1.0


@dataclass
class GovernanceMetrics:
    """Governance metrics"""
    opa_decisions: int = 0
    allow_rate: float = 1.0
    deny_rate: float = 0.0
    hitl_requests: int = 0
    average_approval_time_ms: float = 0.0


@dataclass
class PerformanceDashboard:
    """
    Complete Performance Dashboard
    
    Per spec: Read-only, explainable, audit-ready
    """
    environment: str = "prod"  # labs, pilot, prod
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    system: SystemHealth = field(default_factory=SystemHealth)
    agents: AgentMetrics = field(default_factory=AgentMetrics)
    multi_agent: MultiAgentMetrics = field(default_factory=MultiAgentMetrics)
    governance: GovernanceMetrics = field(default_factory=GovernanceMetrics)


# ============================================================================
# 4. FASTAPI SERVICE MODELS
# ============================================================================

@dataclass
class SimulationRequest:
    """Simulation request"""
    tenant_id: str
    simulation_id: str = ""
    scenario: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OPADecision:
    """
    OPA decision result
    
    Per spec V1.3: Standard decision format
    """
    allow: bool = False
    require_human_approval: bool = False
    reasons: List[str] = field(default_factory=list)
    redactions: List[str] = field(default_factory=list)
    audit_level: str = "standard"


@dataclass
class ArtifactMetadata:
    """Artifact metadata"""
    artifact_id: str
    tenant_id: str
    simulation_id: str
    version: str = "v1"
    created_at: datetime = field(default_factory=datetime.utcnow)
    sha256: str = ""
    signed: bool = False


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Utils
    "generate_id", "compute_hash", "sign_artifact",
    # XR Pack V1.7
    "SignalSeries", "SphereSignals", "GlobalMetrics", "TrueSignals",
    "HeatmapTile", "TrueHeatmap",
    "ExplainRange", "ExplainItem", "ExplainIndex",
    "WASMVerifyConfig",
    # Agent Intelligence
    "AgentTier", "AgentDomain", "RiskLevel",
    "AgentBlueprint", "AgentInstance", "AgentHealth",
    # Performance
    "SystemHealth", "AgentMetrics", "MultiAgentMetrics",
    "GovernanceMetrics", "PerformanceDashboard",
    # FastAPI Service
    "SimulationRequest", "OPADecision", "ArtifactMetadata",
]
