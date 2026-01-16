"""
============================================================================
CHE·NU™ V69 — EDUCATION MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_EDU_*.md
Principle: GOUVERNANCE > EXÉCUTION
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
# SKILL LATTICE MODELS
# ============================================================================

class SkillCategory(str, Enum):
    """Risk categories for skills"""
    CATEGORY_A = "a"  # Low risk - auto-learning allowed
    CATEGORY_B = "b"  # Medium - simulation validation required
    CATEGORY_C = "c"  # High - HITL supervision required


class LearningFormat(str, Enum):
    """Available learning formats"""
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    XR = "xr"
    INTERACTIVE = "interactive"
    SIMULATION = "simulation"


class AssessmentMode(str, Enum):
    """Assessment modes"""
    QUIZ = "quiz"
    SIMULATION = "simulation"
    REAL_TASK = "real_task"
    XR_EXAM = "xr_exam"


@dataclass
class Skill:
    """
    An atomic skill.
    
    Per spec: compétence atomique (ex: "poser un joint silicone")
    """
    skill_id: str
    name: str
    description: str = ""
    
    # Classification
    domain: str = ""
    category: SkillCategory = SkillCategory.CATEGORY_A
    
    # Prerequisites
    prerequisites: List[str] = field(default_factory=list)  # skill_ids
    
    # Learning
    estimated_duration_minutes: int = 15
    formats_available: List[LearningFormat] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"


@dataclass
class LessonUnit:
    """
    A micro-lesson (5-15 min).
    
    Per spec: micro-leçon 5-15 min (texte/vidéo/XR)
    """
    lesson_id: str
    skill_id: str
    title: str
    
    # Content
    format: LearningFormat = LearningFormat.TEXT
    content_ref: str = ""  # Reference to content
    duration_minutes: int = 10
    
    # Structure
    order: int = 0
    
    # XR assets (if applicable)
    xr_assets: List[str] = field(default_factory=list)


@dataclass
class Pathway:
    """
    A learning pathway (set of skills + validations).
    
    Per spec: parcours (ensemble de skills + validations)
    """
    pathway_id: str
    name: str
    description: str = ""
    
    # Skills in order
    skills: List[str] = field(default_factory=list)  # skill_ids
    
    # Validations required
    assessments: List[str] = field(default_factory=list)  # assessment_ids
    
    # Metadata
    estimated_duration_hours: float = 2.0
    difficulty_level: int = 1  # 1-5


@dataclass
class Assessment:
    """
    A validation/assessment.
    
    Per spec: validation (simulation, quiz, tâche réelle)
    """
    assessment_id: str
    skill_id: str
    
    # Mode
    mode: AssessmentMode = AssessmentMode.QUIZ
    
    # Requirements
    passing_score: float = 0.7  # 0-1
    max_attempts: int = 3
    requires_hitl: bool = False  # Per spec: HITL for high risk


@dataclass
class AssessmentResult:
    """
    Result of an assessment.
    
    Per spec artifact: EDU_ASSESSMENT_RESULT.json
    """
    result_id: str
    assessment_id: str
    user_id: str
    
    # Result
    passed: bool = False
    score: float = 0.0
    
    # Proof
    proof_ref: str = ""
    signature: str = ""
    
    # Timestamps
    completed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class NanoCertification:
    """
    A nano-certification badge.
    
    Per spec: badge signé (Artifact) + liens de preuve
    """
    cert_id: str
    skill_id: str
    user_id: str
    
    # Badge info
    name: str = ""
    scope: str = ""
    
    # Validity
    issued_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    # Proof links
    assessment_proofs: List[str] = field(default_factory=list)
    
    # Signature
    signature: str = ""
    signed_by: str = ""


# ============================================================================
# ADAPTIVE LEARNING MODELS
# ============================================================================

class DifficultyLevel(str, Enum):
    """Difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LearnerPreference(str, Enum):
    """Learner preferences"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING = "reading"


@dataclass
class LearnerProfile:
    """
    Learner profile for adaptation.
    
    Per spec: Profil & contraintes
    """
    user_id: str
    
    # Constraints
    available_time_minutes: int = 30
    language: str = "fr"
    has_xr_device: bool = False
    
    # Accessibility
    needs_subtitles: bool = False
    needs_audio_only: bool = False
    
    # Preferences
    preferred_format: LearnerPreference = LearnerPreference.VISUAL
    prefers_examples_first: bool = True
    complexity_tolerance: float = 0.5  # 0-1


@dataclass
class PerformanceMetrics:
    """
    Performance metrics for adaptation.
    
    Per spec: Performance (mesures)
    """
    user_id: str
    skill_id: str
    
    # Quiz performance
    quiz_success_rate: float = 0.0
    avg_time_per_step_seconds: float = 0.0
    
    # Error tracking
    error_count: int = 0
    error_types: Dict[str, int] = field(default_factory=dict)
    repeated_errors: int = 0  # Same error after correction
    
    # Engagement
    completion_rate: float = 0.0


@dataclass
class AdaptationDecision:
    """
    An adaptation decision.
    
    Per spec artifact: EDU_ADAPT_DECISION.json
    """
    decision_id: str
    skill_id: str
    user_id: str
    
    # Decision
    new_format: LearningFormat = LearningFormat.TEXT
    new_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    
    # Signals used
    signals_used: List[str] = field(default_factory=list)
    
    # Justification
    justification: str = ""
    
    # Signature
    signature: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# GHOST TEACHING XR MODELS
# ============================================================================

@dataclass
class GhostTrack:
    """
    A recorded ghost track for XR teaching.
    
    Per spec: position[], rotation[], tool_state[], event_markers[]
    """
    track_id: str
    skill_id: str
    
    # Track data
    positions: List[Dict[str, float]] = field(default_factory=list)
    rotations: List[Dict[str, float]] = field(default_factory=list)
    tool_states: List[Dict[str, Any]] = field(default_factory=list)
    event_markers: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    duration_seconds: float = 0.0
    frame_rate: int = 60
    
    # Validation
    is_gold_run: bool = False
    validated_by: Optional[str] = None
    
    # Hash
    track_hash: str = ""


@dataclass
class InteractionEvent:
    """
    XR interaction event.
    
    Per spec: grasp/release, toggle, apply_force, confirm_step
    """
    event_id: str
    event_type: str  # grasp, release, toggle, apply_force, confirm_step
    timestamp_ms: int = 0
    
    # Event data
    position: Dict[str, float] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GhostTeachingSession:
    """
    A ghost teaching session.
    """
    session_id: str
    user_id: str
    skill_id: str
    track_id: str  # Gold run being used
    
    # Mode
    mode: str = "guided"  # guided, practice, exam
    
    # Scoring
    trajectory_score: float = 0.0
    timing_score: float = 0.0
    order_score: float = 0.0
    overall_score: float = 0.0
    
    # Status
    completed: bool = False
    passed: bool = False


# ============================================================================
# SKILL TO EQUITY BRIDGE MODELS
# ============================================================================

class EligibilityTier(str, Enum):
    """Eligibility tiers"""
    TIER_0 = "tier_0"  # Observation/shadowing (0 equity)
    TIER_1 = "tier_1"  # Supervised execution (low equity)
    TIER_2 = "tier_2"  # Autonomous (standard equity)
    TIER_3 = "tier_3"  # Conception/optimization (premium equity)


@dataclass
class EligibilityRule:
    """
    Rule for task eligibility.
    
    Per spec: règle d'accès à une famille de tâches
    """
    rule_id: str
    task_family: str
    
    # Requirements
    required_certs: List[str] = field(default_factory=list)
    min_trust_score: float = 0.7
    required_simulations: int = 1
    required_xr_exams: int = 0
    
    # Tier
    tier: EligibilityTier = EligibilityTier.TIER_1


@dataclass
class EligibilityProof:
    """
    Proof of eligibility.
    
    Per spec artifact: ELIGIBILITY_PROOF.json
    """
    proof_id: str
    user_id: str
    
    # Evidence
    certs: List[str] = field(default_factory=list)
    trust_score_snapshot: float = 0.0
    assessment_proof_links: List[str] = field(default_factory=list)
    
    # Signature
    signature: str = ""
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TaskEquityOffer:
    """
    Task with equity offer.
    
    Per spec artifact: TASK_EQUITY_OFFER.json
    """
    offer_id: str
    task_id: str
    user_id: str
    
    # Splits
    salary_split: float = 0.0
    equity_split: float = 0.0
    
    # Vesting
    vesting_months: int = 12
    vesting_rules: Dict[str, Any] = field(default_factory=dict)
    
    # Compliance
    opa_compliant: bool = True
    
    # Status
    status: str = "pending"  # pending, accepted, rejected, completed
    
    # Signature
    signature: str = ""


# ============================================================================
# MENTOR SESSION MODEL
# ============================================================================

@dataclass
class MentorSession:
    """
    P2P mentoring session.
    
    Per spec: mentoring P2P (citoyen ↔ citoyen)
    """
    session_id: str
    mentor_id: str
    learner_id: str
    skill_id: str
    
    # Scheduling
    scheduled_at: Optional[datetime] = None
    duration_minutes: int = 30
    
    # Status
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    
    # Notes
    notes: str = ""
    feedback_score: Optional[float] = None


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
    """Sign an artifact (mock signature)"""
    payload = json.dumps(data, sort_keys=True)
    return compute_hash(f"{payload}:{signer_id}")
