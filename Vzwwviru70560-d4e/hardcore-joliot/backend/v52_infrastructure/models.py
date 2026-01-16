"""
============================================================================
CHE·NU™ V69 — V52 INFRASTRUCTURE MODULE MODELS
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_V52_Gateway_Mesh_Registry_Internal_Spec.md
- CHE-NU_V52_OPA_7_Rules_Complete_Pack.md
- CHE-NU_V52_Agent_Learning_From_Backlogs.md
- CHE-NU_AutoGen_Integration.md
- CHE-NU_Prompt_System.md
- CHE-NU_Intelligence_Control_Layer.md

Principle: GOUVERNANCE > EXÉCUTION, Nova = Authority
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


# ============================================================================
# 1. GATEWAY MESH REGISTRY MODELS
# ============================================================================

class Environment(str, Enum):
    """Environment types"""
    LABS = "labs"
    PILOT = "pilot"
    PROD = "prod"


class AuthMethod(str, Enum):
    """Authentication methods"""
    OAUTH2_OIDC = "oauth2_oidc"
    API_KEY = "api_key"
    MTLS = "mTLS"


class RiskCategory(str, Enum):
    """Request risk categories"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RateLimit:
    """Rate limit configuration"""
    rps: int = 100
    burst: int = 200
    window_seconds: int = 60


@dataclass
class APIRoute:
    """
    API Route configuration.
    
    Per spec: Gateway routing model
    """
    route_id: str
    service_name: str
    environment: Environment
    auth_required: bool = True
    rate_limit: RateLimit = field(default_factory=RateLimit)
    
    risk_category: RiskCategory = RiskCategory.MEDIUM
    data_classification: str = "internal"
    
    enabled: bool = True


@dataclass
class ServiceMeshPolicy:
    """
    Service Mesh policy (Istio).
    
    Per spec: Reliability, policy, observability
    """
    policy_id: str
    service_name: str
    
    circuit_breaker_enabled: bool = True
    retry_enabled: bool = True
    max_retries: int = 3
    timeout_ms: int = 5000
    
    mtls_mode: str = "STRICT"


# ============================================================================
# 2. OPA 7 RULES MODELS
# ============================================================================

class ActorType(str, Enum):
    """Actor types"""
    USER = "user"
    ORG_ADMIN = "org_admin"
    AGENT = "agent"


class ActionType(str, Enum):
    """Action types for OPA"""
    DISCUSS = "discuss"
    PROPOSE = "propose"
    PLAN = "plan"
    EXECUTE = "execute"
    WRITE = "write"
    DELETE = "delete"
    EXPORT = "export"
    CONNECT = "connect"


class AutonomyLevel(str, Enum):
    """Agent autonomy levels"""
    INFORMATIONAL = "informational"
    ASSISTED = "assisted"
    GOVERNED = "governed"
    RESTRICTED = "restricted"


@dataclass
class OPARequest:
    """
    Canonical OPA request input.
    
    Per spec: Keep this schema stable across Nova / Gateway / Mesh
    """
    request_id: str
    timestamp: datetime
    environment: Environment
    
    # Tenant
    tenant_id: str
    tenant_plan: str = "free"
    
    # Actor
    actor_type: ActorType = ActorType.USER
    actor_id: str = ""
    
    # Agent (if applicable)
    agent_blueprint_id: str = ""
    agent_level: str = "L0"
    agent_sphere: str = "personal"
    agent_autonomy: AutonomyLevel = AutonomyLevel.GOVERNED
    agent_risk_level: RiskCategory = RiskCategory.MEDIUM
    
    # Action
    action_type: ActionType = ActionType.DISCUSS
    action_target: str = "system"
    resource_id: str = ""
    data_classification: str = "internal"
    
    # HITL
    hitl_required: bool = False
    hitl_approved: bool = False
    hitl_approver_id: str = ""
    
    # Explainability
    explainability_required: bool = True
    explainability_provided: bool = False
    
    # Controls
    audit_logging: bool = True
    trace_context: str = ""


@dataclass
class OPAPolicyResult:
    """OPA policy evaluation result"""
    allow: bool = False
    deny_reasons: List[str] = field(default_factory=list)
    require_hitl: bool = False
    require_explainability: bool = True
    audit_level: str = "standard"


# ============================================================================
# 3. AGENT LEARNING MODELS
# ============================================================================

class LearningTechnique(str, Enum):
    """Learning techniques"""
    RAG = "rag"
    DSLM = "dslm"  # Domain-Specific Language Model
    CONVERSATIONAL = "conversational"


@dataclass
class BacklogEntry:
    """A backlog entry for learning"""
    entry_id: str
    task_description: str
    outcome: str
    sphere: str
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    human_corrections: List[str] = field(default_factory=list)


@dataclass
class LearningSession:
    """
    Learning session for agent.
    
    Per spec: No agent trains itself autonomously
    """
    session_id: str
    agent_id: str
    technique: LearningTechnique
    
    backlog_entries: List[str] = field(default_factory=list)  # Entry IDs
    
    status: str = "pending"  # pending, approved, in_progress, completed
    nova_validated: bool = False
    human_approved: bool = False


@dataclass
class KnowledgeThread:
    """
    Knowledge thread for agent.
    
    Per spec: Memory & Knowledge Threads
    """
    thread_id: str
    agent_id: str
    topic: str
    
    entries: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 4. AUTOGEN INTEGRATION MODELS
# ============================================================================

class AutoGenUseCase(str, Enum):
    """Authorized AutoGen use cases"""
    ARCHITECTURE_EXPLORATION = "architecture_exploration"
    TRADEOFF_ANALYSIS = "tradeoff_analysis"
    BRAINSTORMING = "brainstorming"
    CODE_REVIEW = "code_review"
    THREAT_MODELING = "threat_modeling"
    FEATURE_DECOMPOSITION = "feature_decomposition"
    REGULATORY_SIMULATION = "regulatory_simulation"


class AutoGenSessionStatus(str, Enum):
    """AutoGen session status"""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class AutoGenSession:
    """
    AutoGen session.
    
    Per spec: Sandboxed multi-agent collaboration
    """
    session_id: str
    use_case: AutoGenUseCase
    
    agents: List[str] = field(default_factory=list)
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    
    status: AutoGenSessionStatus = AutoGenSessionStatus.CREATED
    
    nova_reviewed: bool = False
    claude_validated: bool = False
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    output: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# 5. PROMPT SYSTEM MODELS
# ============================================================================

class PromptLayer(str, Enum):
    """Prompt hierarchy layers"""
    SYSTEM = "system"
    OPERATING_MODE = "operating_mode"
    ROLE = "role"
    TASK = "task"
    USER = "user"


@dataclass
class Prompt:
    """
    A prompt in the hierarchy.
    
    Per spec: A layer cannot contradict a layer above
    """
    prompt_id: str
    layer: PromptLayer
    content: str
    
    parent_id: Optional[str] = None
    version: str = "1.0"
    
    is_inviolable: bool = False  # System prompts are inviolable


@dataclass
class PromptComposition:
    """Composed prompt from hierarchy"""
    composition_id: str
    layers: List[Prompt] = field(default_factory=list)
    
    final_prompt: str = ""
    conflicts_detected: bool = False


# ============================================================================
# 6. INTELLIGENCE CONTROL LAYER MODELS
# ============================================================================

class SelfTestCategory(str, Enum):
    """Self-test categories"""
    ARCHITECTURE = "architecture"
    AGENT_SYSTEM = "agent_system"
    PROMPT_SYSTEM = "prompt_system"
    DOMAIN_REALISM = "domain_realism"
    GOVERNANCE = "governance"


@dataclass
class SelfTestResult:
    """
    Self-test result.
    
    Per spec: If any test fails → execution must stop
    """
    test_id: str
    category: SelfTestCategory
    test_name: str
    
    passed: bool = False
    message: str = ""
    
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SelfTestSuite:
    """Complete self-test suite"""
    suite_id: str
    results: List[SelfTestResult] = field(default_factory=list)
    
    all_passed: bool = False
    execution_allowed: bool = False
    
    run_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AuditEntry:
    """Nova auto-audit entry"""
    entry_id: str
    action: str
    actor: str
    
    decision: str = ""
    reason: str = ""
    
    timestamp: datetime = field(default_factory=datetime.utcnow)
    trace_id: str = ""


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Utils
    "generate_id", "compute_hash",
    # Gateway
    "Environment", "AuthMethod", "RiskCategory",
    "RateLimit", "APIRoute", "ServiceMeshPolicy",
    # OPA
    "ActorType", "ActionType", "AutonomyLevel",
    "OPARequest", "OPAPolicyResult",
    # Agent Learning
    "LearningTechnique", "BacklogEntry", "LearningSession", "KnowledgeThread",
    # AutoGen
    "AutoGenUseCase", "AutoGenSessionStatus", "AutoGenSession",
    # Prompt System
    "PromptLayer", "Prompt", "PromptComposition",
    # Intelligence Control
    "SelfTestCategory", "SelfTestResult", "SelfTestSuite", "AuditEntry",
]
