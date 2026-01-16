"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ — AGENT STAGIAIRE                                 ║
║                                                                              ║
║  Agent d'apprentissage qualitatif                                           ║
║  "Le stagiaire n'existe pas pour répondre.                                  ║
║   Il existe pour apprendre à mieux apprendre."                              ║
║                                                                              ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import json
import logging

logger = logging.getLogger("chenu.agents.stagiaire")

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class UserSignal(str, Enum):
    """Signal implicite de l'utilisateur."""
    SILENT = "silent"
    REPHRASE = "rephrase"
    CORRECT = "correct"
    APPROVE = "approve"
    UNKNOWN = "unknown"

class LearningValue(str, Enum):
    """Valeur d'apprentissage estimée."""
    LOW = "low"
    MED = "med"
    HIGH = "high"

class RecurrenceEstimate(str, Enum):
    """Probabilité de récurrence."""
    LOW = "low"
    MED = "med"
    HIGH = "high"

class Priority(str, Enum):
    """Priorité de la note."""
    LOW = "low"
    MED = "med"
    HIGH = "high"

class PromotionStatus(str, Enum):
    """Statut de promotion vers mémoire canonique."""
    NONE = "none"
    CANDIDATE = "candidate"
    PROMOTED = "promoted"
    REJECTED = "rejected"

class StagiaireState(str, Enum):
    """États du stagiaire."""
    IDLE = "idle"
    OBSERVING = "observing"
    PROCESSING = "processing"
    COOLDOWN = "cooldown"

# ═══════════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class StagiaireNote:
    """
    Note créée par le stagiaire à la fin d'une conversation.
    
    Principe: "Si une note n'aide pas le système dans 6 mois, 
    elle ne mérite pas d'exister."
    """
    note_id: str
    timestamp: datetime
    sphere: str
    intent_summary: str
    learning_value: LearningValue
    recurrence_estimate: RecurrenceEstimate
    priority: Priority
    promotion_status: PromotionStatus = PromotionStatus.NONE
    
    # Optional fields
    sector: Optional[str] = None
    ambiguities: List[str] = field(default_factory=list)
    outsourcing_used: bool = False
    outsourcing_reason: Optional[str] = None
    user_signal: UserSignal = UserSignal.UNKNOWN
    question_candidate: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "note_id": self.note_id,
            "timestamp": self.timestamp.isoformat(),
            "sphere": self.sphere,
            "sector": self.sector,
            "intent_summary": self.intent_summary,
            "ambiguities": self.ambiguities,
            "outsourcing_used": self.outsourcing_used,
            "outsourcing_reason": self.outsourcing_reason,
            "user_signal": self.user_signal.value,
            "learning_value": self.learning_value.value,
            "recurrence_estimate": self.recurrence_estimate.value,
            "priority": self.priority.value,
            "question_candidate": self.question_candidate,
            "promotion_status": self.promotion_status.value,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StagiaireNote":
        """Create from dictionary."""
        return cls(
            note_id=data["note_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            sphere=data["sphere"],
            sector=data.get("sector"),
            intent_summary=data["intent_summary"],
            ambiguities=data.get("ambiguities", []),
            outsourcing_used=data.get("outsourcing_used", False),
            outsourcing_reason=data.get("outsourcing_reason"),
            user_signal=UserSignal(data.get("user_signal", "unknown")),
            learning_value=LearningValue(data["learning_value"]),
            recurrence_estimate=RecurrenceEstimate(data["recurrence_estimate"]),
            priority=Priority(data["priority"]),
            question_candidate=data.get("question_candidate"),
            promotion_status=PromotionStatus(data.get("promotion_status", "none")),
        )

@dataclass
class PromotionCandidate:
    """Candidat à la promotion vers mémoire canonique."""
    note_id: str
    sphere: str
    sector: Optional[str]
    intent_summary: str
    question_candidate: Optional[str]
    reason: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "note_id": self.note_id,
            "sphere": self.sphere,
            "sector": self.sector,
            "intent_summary": self.intent_summary,
            "question_candidate": self.question_candidate,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
        }

@dataclass
class CooldownState:
    """État du cooldown (15 min entre activations)."""
    last_activation: Optional[datetime] = None
    cooldown_minutes: int = 15
    
    @property
    def is_in_cooldown(self) -> bool:
        """Check if currently in cooldown."""
        if self.last_activation is None:
            return False
        elapsed = datetime.utcnow() - self.last_activation
        return elapsed < timedelta(minutes=self.cooldown_minutes)
    
    @property
    def remaining_seconds(self) -> int:
        """Seconds remaining in cooldown."""
        if not self.is_in_cooldown:
            return 0
        elapsed = datetime.utcnow() - self.last_activation
        remaining = timedelta(minutes=self.cooldown_minutes) - elapsed
        return max(0, int(remaining.total_seconds()))
    
    def activate(self):
        """Mark activation (starts cooldown)."""
        self.last_activation = datetime.utcnow()

# ═══════════════════════════════════════════════════════════════════════════════
# AGENT STAGIAIRE
# ═══════════════════════════════════════════════════════════════════════════════

class AgentStagiaire:
    """
    Agent Stagiaire — Apprentissage qualitatif.
    
    Rôle:
    - Observe, questionne (rarement), et note
    - Privilégie la QUALITÉ FUTURE plutôt que l'efficacité immédiate
    - Accepte de rester silencieux longtemps
    
    Activé UNIQUEMENT à la fin de conversation.
    Ne décide pas d'actions.
    Ne modifie pas la mémoire canonique directement.
    """
    
    def __init__(self, storage=None):
        self.state = StagiaireState.IDLE
        self.cooldown = CooldownState()
        self.storage = storage or InMemoryStorage()
        self.current_observation: Optional[Dict[str, Any]] = None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACTIVATION (Fin de conversation)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def can_activate(self) -> bool:
        """Check if stagiaire can be activated."""
        return not self.cooldown.is_in_cooldown and self.state == StagiaireState.IDLE
    
    def activate_end_of_conversation(
        self,
        conversation_context: Dict[str, Any]
    ) -> Optional[StagiaireNote]:
        """
        Activation à la fin de conversation.
        
        Le stagiaire analyse et décide s'il y a quelque chose
        qui mérite d'être noté pour l'apprentissage futur.
        """
        if not self.can_activate():
            logger.info(f"Stagiaire in cooldown ({self.cooldown.remaining_seconds}s remaining)")
            return None
        
        self.state = StagiaireState.OBSERVING
        self.cooldown.activate()
        
        try:
            # Phase 1: Observation
            observation = self._observe(conversation_context)
            
            # Phase 2: Filtrage radical
            if not self._should_create_note(observation):
                logger.info("Stagiaire: Nothing worth noting (filtered)")
                return None
            
            # Phase 3: Création de note
            self.state = StagiaireState.PROCESSING
            note = self._create_note(observation, conversation_context)
            
            # Phase 4: Évaluation promotion
            if self._is_promotion_candidate(note):
                note.promotion_status = PromotionStatus.CANDIDATE
                self._create_promotion_candidate(note)
            
            # Persist
            self.storage.save_note(note)
            
            logger.info(f"Stagiaire: Note created {note.note_id} (priority: {note.priority.value})")
            return note
            
        finally:
            self.state = StagiaireState.COOLDOWN
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OBSERVATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _observe(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observer sans juger.
        
        Collecte seulement ce qui aide le futur système à décider mieux.
        """
        return {
            # A. Intention perçue
            "intent": {
                "objective": context.get("user_intent", "unknown"),
                "ambiguities": context.get("ambiguities", []),
                "unsaid": context.get("implicit_needs", []),
            },
            
            # B. Décision du système
            "system_decision": {
                "route": context.get("routing", "local"),
                "confidence": context.get("confidence", "medium"),
            },
            
            # C. Intervention externe
            "external": {
                "used": context.get("outsourced", False),
                "reason": context.get("outsource_reason"),
                "value_added": context.get("external_value"),
            },
            
            # D. Réaction utilisateur
            "user_reaction": {
                "signal": context.get("user_signal", "unknown"),
                "intent_changed": context.get("intent_evolved", False),
            },
            
            # E. Potentiel d'apprentissage
            "learning": {
                "sphere": context.get("sphere", "personal"),
                "sector": context.get("sector"),
                "recurrence": self._estimate_recurrence(context),
                "value": self._estimate_learning_value(context),
            },
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FILTRAGE RADICAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _should_create_note(self, observation: Dict[str, Any]) -> bool:
        """
        Le stagiaire JETTE volontairement:
        - Évidences (cas faciles, non ambigus)
        - Redondances sans surprise
        - Détails contextuels non structurants
        - Certitudes artificielles
        - Cas uniques sans futur (non reproductibles)
        """
        learning = observation.get("learning", {})
        intent = observation.get("intent", {})
        
        # Reject if no learning value
        if learning.get("value") == "low" and learning.get("recurrence") == "low":
            return False
        
        # Reject if obvious (no ambiguity, high confidence)
        if (not intent.get("ambiguities") and 
            observation.get("system_decision", {}).get("confidence") == "high"):
            return False
        
        # Reject if user just approved without any friction
        user_signal = observation.get("user_reaction", {}).get("signal")
        if user_signal == "approve" and not intent.get("unsaid"):
            return False
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CRÉATION DE NOTE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _create_note(
        self,
        observation: Dict[str, Any],
        context: Dict[str, Any]
    ) -> StagiaireNote:
        """Créer une note structurée."""
        learning = observation.get("learning", {})
        intent = observation.get("intent", {})
        external = observation.get("external", {})
        user_reaction = observation.get("user_reaction", {})
        
        # Determine priority
        priority = self._calculate_priority(
            learning.get("value", "low"),
            learning.get("recurrence", "low")
        )
        
        # Extract potential question
        question = self._extract_question_candidate(observation, context)
        
        return StagiaireNote(
            note_id=str(uuid4()),
            timestamp=datetime.utcnow(),
            sphere=learning.get("sphere", "personal"),
            sector=learning.get("sector"),
            intent_summary=intent.get("objective", "")[:200],
            ambiguities=intent.get("ambiguities", [])[:5],
            outsourcing_used=external.get("used", False),
            outsourcing_reason=external.get("reason"),
            user_signal=UserSignal(user_reaction.get("signal", "unknown")),
            learning_value=LearningValue(learning.get("value", "low")),
            recurrence_estimate=RecurrenceEstimate(learning.get("recurrence", "low")),
            priority=Priority(priority),
            question_candidate=question,
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PROMOTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _is_promotion_candidate(self, note: StagiaireNote) -> bool:
        """
        Une note mérite promotion si:
        - HIGH priority
        - Contient une question candidate
        - Learning value = HIGH
        """
        if note.priority != Priority.HIGH:
            return False
        if note.learning_value != LearningValue.HIGH:
            return False
        return True
    
    def _create_promotion_candidate(self, note: StagiaireNote):
        """Create promotion candidate for review."""
        candidate = PromotionCandidate(
            note_id=note.note_id,
            sphere=note.sphere,
            sector=note.sector,
            intent_summary=note.intent_summary,
            question_candidate=note.question_candidate,
            reason=f"High value + High priority in {note.sphere}",
        )
        self.storage.save_promotion_candidate(candidate)
        logger.info(f"Promotion candidate created: {note.note_id}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _estimate_recurrence(self, context: Dict[str, Any]) -> str:
        """Estimate recurrence probability."""
        sphere = context.get("sphere", "personal")
        
        # Business and team spheres tend to have more recurring patterns
        high_recurrence_spheres = ["business", "team", "government"]
        if sphere in high_recurrence_spheres:
            return "high"
        
        # Check for pattern indicators
        if context.get("is_common_task", False):
            return "high"
        if context.get("is_one_off", False):
            return "low"
        
        return "med"
    
    def _estimate_learning_value(self, context: Dict[str, Any]) -> str:
        """Estimate learning value."""
        # High value if there were corrections or rephrasing
        if context.get("user_signal") in ["correct", "rephrase"]:
            return "high"
        
        # High value if system was uncertain
        if context.get("confidence") == "low":
            return "high"
        
        # High value if external was needed
        if context.get("outsourced", False):
            return "med"
        
        return "low"
    
    def _calculate_priority(self, value: str, recurrence: str) -> str:
        """Calculate priority from value and recurrence."""
        matrix = {
            ("high", "high"): "high",
            ("high", "med"): "high",
            ("high", "low"): "med",
            ("med", "high"): "high",
            ("med", "med"): "med",
            ("med", "low"): "low",
            ("low", "high"): "med",
            ("low", "med"): "low",
            ("low", "low"): "low",
        }
        return matrix.get((value, recurrence), "low")
    
    def _extract_question_candidate(
        self,
        observation: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[str]:
        """Extract a potential question that would help future learning."""
        ambiguities = observation.get("intent", {}).get("ambiguities", [])
        unsaid = observation.get("intent", {}).get("unsaid", [])
        
        if ambiguities:
            return f"Clarifier: {ambiguities[0]}"
        if unsaid:
            return f"Explorer: {unsaid[0]}"
        
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# STORAGE (In-Memory for now)
# ═══════════════════════════════════════════════════════════════════════════════

class InMemoryStorage:
    """Simple in-memory storage for stagiaire notes."""
    
    def __init__(self):
        self.notes: Dict[str, StagiaireNote] = {}
        self.promotion_candidates: Dict[str, PromotionCandidate] = {}
    
    def save_note(self, note: StagiaireNote):
        self.notes[note.note_id] = note
    
    def get_note(self, note_id: str) -> Optional[StagiaireNote]:
        return self.notes.get(note_id)
    
    def get_notes_by_sphere(self, sphere: str) -> List[StagiaireNote]:
        return [n for n in self.notes.values() if n.sphere == sphere]
    
    def save_promotion_candidate(self, candidate: PromotionCandidate):
        self.promotion_candidates[candidate.note_id] = candidate
    
    def get_pending_promotions(self) -> List[PromotionCandidate]:
        return list(self.promotion_candidates.values())

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "AgentStagiaire",
    "StagiaireNote",
    "PromotionCandidate",
    "CooldownState",
    "UserSignal",
    "LearningValue",
    "RecurrenceEstimate",
    "Priority",
    "PromotionStatus",
    "StagiaireState",
]
