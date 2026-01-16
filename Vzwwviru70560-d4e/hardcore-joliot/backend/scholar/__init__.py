"""
============================================================================
CHE·NU™ V69 — SCHOLAR MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_SCH_CAUSAL_KNOWLEDGE_GRAPH.md
- CHE-NU_SCH_AGENT_CROSS_POLLINATOR_LOGIC.md
- CHE-NU_SCH_ANALOGICAL_SEARCH_ENGINE.md
- CHE-NU_SCH_GLOBAL_IMPACT_SIMULATOR.md
- CHE-NU_SCH_MICRO_CONTRIBUTION_TRACKING.md
- CHE-NU_SCH_REPRODUCIBILITY_PROTOCOL.md
- CHE-NU_SCH_BIO_DIGITAL_STORAGE_V1.md

Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

# Models
from .models import (
    CausalNode,
    CausalLink,
    CausalLinkStrength,
    VerificationStatus,
    TopologicalPattern,
    AnalogicalMatch,
    FundingScenario,
    ImpactResult,
    ImpactMetric,
    MicroContribution,
    ScholarEquity,
    ContributionType,
    ReproducibilityJob,
    ReproducibilityStatus,
    VerifiedBadge,
    BioCapsule,
    DNAShard,
    DecodeRequest,
    BioStorageStatus,
    CrossPollinationMatch,
    TaskForce,
    generate_id,
    compute_hash,
)

# Knowledge Graph
from .knowledge_graph import (
    CausalKnowledgeGraph,
    SplitViewAnalyzer,
    create_knowledge_graph,
    create_split_view_analyzer,
)

# Analogical Search
from .analogical_search import (
    AnalogicalSearchEngine,
    TopologicalExtractor,
    PatternMatcher,
    create_search_engine,
    create_extractor,
    create_matcher,
)

# Impact Simulator
from .impact_simulator import (
    GlobalImpactSimulator,
    ImpactCalculator,
    HeatmapGenerator,
    create_simulator,
    create_scenario,
)

# Contribution Tracking
from .contribution_tracking import (
    ContributionTracker,
    ContributionLedger,
    EquityCalculator,
    create_tracker,
    create_ledger,
    create_equity_calculator,
)

# Reproducibility
from .reproducibility import (
    ReproducibilityProtocol,
    ReproducibilityWorker,
    BadgeGenerator,
    create_protocol,
    create_worker,
    create_badge_generator,
)

# Bio Storage
from .bio_storage import (
    BioStorageService,
    BioEncoderWorker,
    BioDecoderWorker,
    create_storage_service,
    create_encoder,
    create_decoder,
)

# Cross-Pollinator
from .cross_pollinator import (
    CrossPollinatorAgent,
    CrossPollinatorScanner,
    TaskForceManager,
    create_cross_pollinator,
    create_scanner,
    create_task_force_manager,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "CausalNode", "CausalLink", "CausalLinkStrength", "VerificationStatus",
    "TopologicalPattern", "AnalogicalMatch",
    "FundingScenario", "ImpactResult", "ImpactMetric",
    "MicroContribution", "ScholarEquity", "ContributionType",
    "ReproducibilityJob", "ReproducibilityStatus", "VerifiedBadge",
    "BioCapsule", "DNAShard", "DecodeRequest", "BioStorageStatus",
    "CrossPollinationMatch", "TaskForce",
    "generate_id", "compute_hash",
    # Knowledge Graph
    "CausalKnowledgeGraph", "SplitViewAnalyzer",
    "create_knowledge_graph", "create_split_view_analyzer",
    # Analogical Search
    "AnalogicalSearchEngine", "TopologicalExtractor", "PatternMatcher",
    "create_search_engine", "create_extractor", "create_matcher",
    # Impact Simulator
    "GlobalImpactSimulator", "ImpactCalculator", "HeatmapGenerator",
    "create_simulator", "create_scenario",
    # Contribution Tracking
    "ContributionTracker", "ContributionLedger", "EquityCalculator",
    "create_tracker", "create_ledger", "create_equity_calculator",
    # Reproducibility
    "ReproducibilityProtocol", "ReproducibilityWorker", "BadgeGenerator",
    "create_protocol", "create_worker", "create_badge_generator",
    # Bio Storage
    "BioStorageService", "BioEncoderWorker", "BioDecoderWorker",
    "create_storage_service", "create_encoder", "create_decoder",
    # Cross-Pollinator
    "CrossPollinatorAgent", "CrossPollinatorScanner", "TaskForceManager",
    "create_cross_pollinator", "create_scanner", "create_task_force_manager",
]
