"""
============================================================================
CHE·NU™ V69 — EDUCATION MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_EDU_SKILL_LATTICE_V1.md
- CHE-NU_EDU_ADAPTIVE_LEARNING_PROTOCOL.md
- CHE-NU_EDU_GHOST_TEACHING_XR.md
- CHE-NU_EDU_SKILL_TO_EQUITY_BRIDGE.md

Principle: GOUVERNANCE > EXÉCUTION
Just-in-Time learning linked to action, never automatic decision on real.
============================================================================
"""

# Models
from .models import (
    Skill,
    SkillCategory,
    LearningFormat,
    LessonUnit,
    Pathway,
    Assessment,
    AssessmentMode,
    AssessmentResult,
    NanoCertification,
    LearnerProfile,
    LearnerPreference,
    PerformanceMetrics,
    AdaptationDecision,
    DifficultyLevel,
    GhostTrack,
    InteractionEvent,
    GhostTeachingSession,
    EligibilityRule,
    EligibilityTier,
    EligibilityProof,
    TaskEquityOffer,
    MentorSession,
    generate_id,
    compute_hash,
    sign_artifact,
)

# Skill Lattice
from .skill_lattice import (
    SkillLattice,
    SkillRegistry,
    PathwayManager,
    AssessmentEngine,
    MentorMatcher,
    create_skill_lattice,
    create_skill,
)

# Adaptive Learning
from .adaptive_learning import (
    AdaptiveLearningProtocol,
    SignalAnalyzer,
    DifficultyAdapter,
    LearningLoopManager,
    create_protocol,
    create_learner_profile,
)

# Ghost Teaching XR
from .ghost_teaching import (
    GhostTeachingEngine,
    GhostTrackRecorder,
    SafetyBubble,
    ScoringEngine,
    create_ghost_teaching_engine,
    create_recorder,
    create_safety_bubble,
)

# Skill to Equity Bridge
from .skill_equity import (
    SkillToEquityBridge,
    EligibilityEvaluator,
    EquityCalculator,
    TaskOfferGenerator,
    create_bridge,
    create_eligibility_rule,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "Skill", "SkillCategory", "LearningFormat", "LessonUnit", "Pathway",
    "Assessment", "AssessmentMode", "AssessmentResult", "NanoCertification",
    "LearnerProfile", "LearnerPreference", "PerformanceMetrics",
    "AdaptationDecision", "DifficultyLevel",
    "GhostTrack", "InteractionEvent", "GhostTeachingSession",
    "EligibilityRule", "EligibilityTier", "EligibilityProof", "TaskEquityOffer",
    "MentorSession",
    "generate_id", "compute_hash", "sign_artifact",
    # Skill Lattice
    "SkillLattice", "SkillRegistry", "PathwayManager", "AssessmentEngine",
    "MentorMatcher", "create_skill_lattice", "create_skill",
    # Adaptive Learning
    "AdaptiveLearningProtocol", "SignalAnalyzer", "DifficultyAdapter",
    "LearningLoopManager", "create_protocol", "create_learner_profile",
    # Ghost Teaching XR
    "GhostTeachingEngine", "GhostTrackRecorder", "SafetyBubble", "ScoringEngine",
    "create_ghost_teaching_engine", "create_recorder", "create_safety_bubble",
    # Skill to Equity Bridge
    "SkillToEquityBridge", "EligibilityEvaluator", "EquityCalculator",
    "TaskOfferGenerator", "create_bridge", "create_eligibility_rule",
]
