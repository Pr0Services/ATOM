"""
============================================================================
CHE·NU™ V69 — LABS ADVANCED MODULE
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

Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # Transparency
    AIUsageType, ExplainabilityLevel,
    AIUsageScope, TransparencyReport, ExplainabilityTrace,
    # Taxonomy
    AgentTier, AutonomyLevel,
    AgentBlueprint, IndustryDomain, AgentTaxonomy,
    # Experiments
    ExperimentScope, ExperimentStatus,
    ExperimentMetric, Experiment, ExperimentsMatrix,
    # Scoring
    ScoreDimension, AgentScore, ScoringConfig,
    # Prompt Audit
    PromptType, RiskLevel,
    PromptInventoryItem, PromptAuditReport,
    # Performance
    OptimizationCategory, OptimizationTechnique,
    PerformanceTarget, PerformanceOptimizationPlan,
)

# Systems
from .systems import (
    AITransparencyService,
    AgentTaxonomyService,
    ExperimentsService,
    AgentScoringService,
    PromptAuditService,
    PerformanceOptimizationService,
    create_transparency_service,
    create_taxonomy_service,
    create_experiments_service,
    create_scoring_service,
    create_prompt_audit_service,
    create_performance_service,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
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
    # Services
    "AITransparencyService", "AgentTaxonomyService",
    "ExperimentsService", "AgentScoringService",
    "PromptAuditService", "PerformanceOptimizationService",
    "create_transparency_service", "create_taxonomy_service",
    "create_experiments_service", "create_scoring_service",
    "create_prompt_audit_service", "create_performance_service",
]
