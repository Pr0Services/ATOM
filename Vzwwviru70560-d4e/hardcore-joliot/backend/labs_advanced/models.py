"""
============================================================================
CHE·NU™ V69 — LABS ADVANCED MODULE MODELS
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_AI_Transparency_Explainability.md
- CHE-NU_Agent_Blueprint_Taxonomy.md
- CHE-NU_LABS_Experiments_Matrix.md
- CHE-NU_WORLD_SIM_AGENT_SCORING.md
- CHE-NU_Prompt_Audit_Playbook.md
- CHE-NU_V52_Performance_Optimization_Consolidation.md

"Transparent, Explainable, Auditable - Enterprise Scale"
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
# 1. AI TRANSPARENCY MODELS
# ============================================================================

class AIUsageType(str, Enum):
    """Types of AI usage"""
    DECISION_SUPPORT = "decision_support"
    AUTONOMOUS_EXECUTION = "autonomous_execution"
    DATA_PROCESSING = "data_processing"
    LEARNING = "learning"


class ExplainabilityLevel(str, Enum):
    """Explainability depth levels"""
    SUMMARY = "summary"       # High-level explanation
    DETAILED = "detailed"     # Step-by-step reasoning
    TECHNICAL = "technical"   # Full technical trace


@dataclass
class AIUsageScope:
    """
    AI usage scope declaration.
    
    Per spec: What CHE·NU does and does NOT do
    """
    decision_support: bool = True
    autonomous_execution: str = "limited"  # limited, none
    human_in_the_loop: str = "mandatory_for_high_risk"
    data_processing: str = "contextual"
    learning_from_users: str = "controlled"


@dataclass
class TransparencyReport:
    """
    AI Transparency Report.
    
    Per spec: Public & Internal versions
    """
    report_id: str
    version: str = "public"  # public, internal
    
    ai_usage_scope: AIUsageScope = field(default_factory=AIUsageScope)
    
    # What CHE·NU does
    capabilities: List[str] = field(default_factory=lambda: [
        "assists decision-making",
        "automates low-risk tasks",
        "proposes actions",
        "structures information",
    ])
    
    # What CHE·NU does NOT do
    limitations: List[str] = field(default_factory=lambda: [
        "replace human judgment",
        "make irreversible legal decisions",
        "give professional advice (legal, medical, financial)",
        "act without governance",
    ])
    
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ExplainabilityTrace:
    """A single explainability trace for a decision"""
    trace_id: str
    decision_id: str
    level: ExplainabilityLevel
    
    reasoning: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    agent_id: str = ""
    prompt_hash: str = ""
    
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 2. AGENT BLUEPRINT TAXONOMY MODELS
# ============================================================================

class AgentTier(str, Enum):
    """Agent hierarchy tier"""
    L0 = "L0"  # Specialist
    L1 = "L1"  # Manager
    L2 = "L2"  # Director
    L3 = "L3"  # Executive


class AutonomyLevel(str, Enum):
    """Agent autonomy levels"""
    INFORMATIONAL = "informational"
    ASSISTED = "assisted"
    GOVERNED = "governed"
    RESTRICTED = "restricted"


@dataclass
class AgentBlueprint:
    """
    Agent Blueprint (ADN).
    
    Per spec: Describes what an agent IS, independent of instance
    """
    blueprint_id: str
    domain: str
    role: str
    
    applicable_industries: List[str] = field(default_factory=list)
    mission: str = ""
    responsibilities: List[str] = field(default_factory=list)
    allowed_actions: List[str] = field(default_factory=list)
    required_data: List[str] = field(default_factory=list)
    connected_tools: List[str] = field(default_factory=list)
    connected_apis: List[str] = field(default_factory=list)
    autonomy_level: AutonomyLevel = AutonomyLevel.GOVERNED
    governance_constraints: List[str] = field(default_factory=list)


@dataclass
class IndustryDomain:
    """Industry domain mapping"""
    industry_id: str
    name: str
    domains: List[str] = field(default_factory=list)


@dataclass
class AgentTaxonomy:
    """
    Complete agent taxonomy.
    
    Per spec: Industry → Domain → Role → Agent Instance
    """
    taxonomy_id: str
    
    industries: List[IndustryDomain] = field(default_factory=list)
    blueprints: Dict[str, AgentBlueprint] = field(default_factory=dict)
    
    total_agents: int = 287


# ============================================================================
# 3. LABS EXPERIMENTS MODELS
# ============================================================================

class ExperimentScope(str, Enum):
    """Experiment scope"""
    LABS = "LABS"
    PILOT = "PILOT"
    PROD = "PROD"


class ExperimentStatus(str, Enum):
    """Experiment status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class ExperimentMetric:
    """A metric for an experiment"""
    name: str
    baseline: float
    current: float = 0.0
    target: float = 0.0
    unit: str = ""


@dataclass
class Experiment:
    """
    LABS Experiment.
    
    Per spec: Controlled experiments with hypothesis, metrics, success criteria
    """
    experiment_id: str
    category: str
    hypothesis: str
    technique: str
    
    scope: ExperimentScope = ExperimentScope.LABS
    
    metrics: List[ExperimentMetric] = field(default_factory=list)
    success_criteria: Dict[str, str] = field(default_factory=dict)
    risks: List[str] = field(default_factory=list)
    
    status: ExperimentStatus = ExperimentStatus.PENDING
    decision: str = "pending"
    
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class ExperimentsMatrix:
    """Matrix of all experiments"""
    matrix_id: str
    experiments: List[Experiment] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 4. WORLD SIM SCORING MODELS
# ============================================================================

class ScoreDimension(str, Enum):
    """Scoring dimensions"""
    DECISION_QUALITY = "decision_quality"
    RULE_COMPLIANCE = "rule_compliance"
    RISK_AWARENESS = "risk_awareness"
    EFFICIENCY = "efficiency"
    COLLABORATION = "collaboration"


@dataclass
class AgentScore:
    """
    Agent score in simulation.
    
    Per spec: Scores are informational only, never decisional alone
    """
    score_id: str
    agent_id: str
    simulation_id: str
    
    dimensions: Dict[ScoreDimension, float] = field(default_factory=dict)
    overall_score: float = 0.0
    
    # Governance
    informational_only: bool = True  # Never decisional alone
    
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ScoringConfig:
    """Scoring configuration"""
    weights: Dict[ScoreDimension, float] = field(default_factory=lambda: {
        ScoreDimension.DECISION_QUALITY: 0.3,
        ScoreDimension.RULE_COMPLIANCE: 0.25,
        ScoreDimension.RISK_AWARENESS: 0.2,
        ScoreDimension.EFFICIENCY: 0.15,
        ScoreDimension.COLLABORATION: 0.1,
    })


# ============================================================================
# 5. PROMPT AUDIT MODELS
# ============================================================================

class PromptType(str, Enum):
    """Prompt types"""
    ROLE = "role"
    AGENT = "agent"
    TASK = "task"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Prompt risk level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PromptInventoryItem:
    """
    Prompt inventory item.
    
    Per spec: Each prompt MUST be listed using this format
    """
    prompt_id: str
    source_location: str
    original_text_hash: str
    
    current_usage: str = ""
    suspected_type: PromptType = PromptType.UNKNOWN
    
    domain: str = ""
    role: str = ""
    agent: str = ""
    
    tools_mentioned: List[str] = field(default_factory=list)
    autonomy_signals: List[str] = field(default_factory=list)
    
    risk_level: RiskLevel = RiskLevel.MEDIUM
    duplication_suspected: bool = False
    
    notes: str = ""


@dataclass
class PromptAuditReport:
    """Complete prompt audit report"""
    report_id: str
    
    inventory: List[PromptInventoryItem] = field(default_factory=list)
    
    total_prompts: int = 0
    duplicates_found: int = 0
    high_risk_count: int = 0
    
    refactor_readiness: float = 0.0  # 0-1
    
    generated_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 6. PERFORMANCE OPTIMIZATION MODELS
# ============================================================================

class OptimizationCategory(str, Enum):
    """Optimization categories"""
    MULTI_AGENT = "multi_agent_orchestration"
    TASK_DECOMPOSITION = "task_decomposition"
    CACHING = "caching"
    BATCHING = "batching"
    SPECULATIVE_DECODING = "speculative_decoding"
    OBSERVABILITY = "observability"


@dataclass
class OptimizationTechnique:
    """An optimization technique"""
    technique_id: str
    category: OptimizationCategory
    name: str
    
    description: str = ""
    expected_gain: str = ""
    
    # Adoption path
    labs_validated: bool = False
    pilot_validated: bool = False
    prod_ready: bool = False


@dataclass
class PerformanceTarget:
    """Performance target"""
    target_id: str
    metric: str
    
    current: float
    target: float
    unit: str
    
    achieved: bool = False


@dataclass
class PerformanceOptimizationPlan:
    """
    Performance optimization plan.
    
    Per spec: LABS → Pilot → Production adoption model
    """
    plan_id: str
    
    techniques: List[OptimizationTechnique] = field(default_factory=list)
    targets: List[PerformanceTarget] = field(default_factory=list)
    
    # Key targets from spec
    scalability_target: int = 70000  # users
    latency_improvement: str = "30+ tokens/s"
    accuracy_target: float = 0.80  # 80%
    error_reduction: str = "17x → 4.4x"
    
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Utils
    "generate_id", "compute_hash",
    # Transparency
    "AIUsageType", "ExplainabilityLevel",
    "AIUsageScope", "TransparencyReport", "ExplainabilityTrace",
    # Taxonomy
    "AgentTier", "AutonomyLevel",
    "AgentBlueprint", "IndustryDomain", "AgentTaxonomy",
    # Experiments
    "ExperimentScope", "ExperimentStatus",
    "ExperimentMetric", "Experiment", "ExperimentsMatrix",
    # Scoring
    "ScoreDimension", "AgentScore", "ScoringConfig",
    # Prompt Audit
    "PromptType", "RiskLevel",
    "PromptInventoryItem", "PromptAuditReport",
    # Performance
    "OptimizationCategory", "OptimizationTechnique",
    "PerformanceTarget", "PerformanceOptimizationPlan",
]
