"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ — AGENT PROFESSEUR                                ║
║                                                                              ║
║  Agent de stabilisation cognitive                                           ║
║  "Le professeur n'aide pas le système à aller plus vite.                    ║
║   Il l'aide à ne pas se perdre."                                            ║
║                                                                              ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import logging

logger = logging.getLogger("chenu.agents.professeur")

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class FailureType(str, Enum):
    """Types d'échecs marquables par le Professeur."""
    
    # Échec de compréhension d'intention
    INTENT_MISREAD = "intent_misread"
    INTENT_NO_CONVERGENCE = "intent_no_convergence"
    INTENT_CORRECT_BUT_WRONG = "intent_correct_but_wrong"
    
    # Échec de stabilité
    STABILITY_RECONFIRM = "stability_reconfirm"
    STABILITY_EXCESSIVE_DOUBT = "stability_excessive_doubt"
    STABILITY_OSCILLATION = "stability_oscillation"
    
    # Échec de récupération de contexte
    CONTEXT_LOST_THREAD = "context_lost_thread"
    CONTEXT_TOO_MANY_REFORMULATIONS = "context_too_many_reformulations"
    CONTEXT_DRIFT = "context_drift"
    
    # Échec de jugement de confiance
    CONFIDENCE_UNNECESSARY_OUTSOURCE = "confidence_unnecessary_outsource"
    CONFIDENCE_OVER_VERIFICATION = "confidence_over_verification"
    CONFIDENCE_FALSE_UNCERTAINTY = "confidence_false_uncertainty"

class FailureSeverity(str, Enum):
    """Sévérité de l'échec."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecenteringStatus(str, Enum):
    """Statut du recentrage."""
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"
    EXPIRED = "expired"

# ═══════════════════════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FailureMarker:
    """
    Marqueur d'échec structurant.
    
    Le professeur marque uniquement des échecs structurants.
    Pas des bugs isolés.
    
    Principe: "Le professeur marque ce qui crée de la CONFUSION DURABLE,
    pas ce qui crée une erreur ponctuelle."
    """
    marker_id: str
    timestamp: datetime
    failure_type: FailureType
    severity: FailureSeverity
    description: str
    sphere: str
    
    # Context
    thread_id: Optional[str] = None
    conversation_id: Optional[str] = None
    
    # Evidence
    evidence: List[str] = field(default_factory=list)
    
    # Resolution
    resolved: bool = False
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "marker_id": self.marker_id,
            "timestamp": self.timestamp.isoformat(),
            "failure_type": self.failure_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "sphere": self.sphere,
            "thread_id": self.thread_id,
            "conversation_id": self.conversation_id,
            "evidence": self.evidence,
            "resolved": self.resolved,
            "resolution_notes": self.resolution_notes,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }

@dataclass
class RecenteringFile:
    """
    Fichier de Recentrage.
    
    Permet au système de REVENIR à une compréhension déjà stabilisée
    quand il dérive.
    
    Contenu autorisé:
    - Intentions validées
    - Décisions explicites
    - Autorisations déjà données
    - Structures qui ont fonctionné
    - Hypothèses clôturées
    
    Contenu INTERDIT:
    - Logs bruts
    - Conversations complètes
    - Hypothèses ouvertes
    - Doutes non résolus
    """
    file_id: str
    created_at: datetime
    sphere: str
    thread_id: Optional[str] = None
    
    # Stabilized understanding
    validated_intents: List[str] = field(default_factory=list)
    explicit_decisions: List[str] = field(default_factory=list)
    granted_permissions: List[str] = field(default_factory=list)
    working_structures: List[str] = field(default_factory=list)
    closed_hypotheses: List[str] = field(default_factory=list)
    
    # Metadata
    status: RecenteringStatus = RecenteringStatus.PENDING
    applied_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_id": self.file_id,
            "created_at": self.created_at.isoformat(),
            "sphere": self.sphere,
            "thread_id": self.thread_id,
            "validated_intents": self.validated_intents,
            "explicit_decisions": self.explicit_decisions,
            "granted_permissions": self.granted_permissions,
            "working_structures": self.working_structures,
            "closed_hypotheses": self.closed_hypotheses,
            "status": self.status.value,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }
    
    def add_validated_intent(self, intent: str):
        """Add a validated intent."""
        if intent and intent not in self.validated_intents:
            self.validated_intents.append(intent)
    
    def add_explicit_decision(self, decision: str):
        """Add an explicit decision."""
        if decision and decision not in self.explicit_decisions:
            self.explicit_decisions.append(decision)
    
    def add_permission(self, permission: str):
        """Add a granted permission."""
        if permission and permission not in self.granted_permissions:
            self.granted_permissions.append(permission)

# ═══════════════════════════════════════════════════════════════════════════════
# AGENT PROFESSEUR
# ═══════════════════════════════════════════════════════════════════════════════

class AgentProfesseur:
    """
    Agent Professeur — Stabilisation cognitive.
    
    Rôle:
    - Observer le système (pas les conversations)
    - Marquer les échecs significatifs
    - Empêcher la reconfirmation inutile
    - Ramener le contexte quand le fil est perdu
    - Stabiliser ce qui a déjà été compris
    
    Ce que le professeur N'EST PAS:
    - Un agent d'action
    - Un agent temps réel
    - Un correcteur automatique
    - Un superviseur permanent
    
    Règle d'or: "Le professeur n'optimise pas la performance.
    Il protège la compréhension."
    """
    
    def __init__(self, storage=None):
        self.storage = storage or InMemoryProfesseurStorage()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OBSERVATION (Système, pas conversations)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def observe_system_behavior(
        self,
        behavior_data: Dict[str, Any]
    ) -> List[FailureMarker]:
        """
        Observer le comportement système et détecter les échecs structurants.
        
        Le professeur observe le SYSTÈME, pas les conversations individuelles.
        """
        markers = []
        
        # Detect intent failures
        intent_failure = self._detect_intent_failure(behavior_data)
        if intent_failure:
            markers.append(intent_failure)
        
        # Detect stability failures
        stability_failure = self._detect_stability_failure(behavior_data)
        if stability_failure:
            markers.append(stability_failure)
        
        # Detect context failures
        context_failure = self._detect_context_failure(behavior_data)
        if context_failure:
            markers.append(context_failure)
        
        # Detect confidence failures
        confidence_failure = self._detect_confidence_failure(behavior_data)
        if confidence_failure:
            markers.append(confidence_failure)
        
        # Persist markers
        for marker in markers:
            self.storage.save_failure_marker(marker)
            logger.warning(
                f"Professeur: Failure marked - {marker.failure_type.value} "
                f"(severity: {marker.severity.value})"
            )
        
        return markers
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DÉTECTION D'ÉCHECS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _detect_intent_failure(
        self,
        data: Dict[str, Any]
    ) -> Optional[FailureMarker]:
        """Détecter échec de compréhension d'intention."""
        
        # Check for multiple reformulations without convergence
        reformulations = data.get("reformulation_count", 0)
        if reformulations >= 3:
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.INTENT_NO_CONVERGENCE,
                severity=FailureSeverity.MEDIUM,
                description=f"No convergence after {reformulations} reformulations",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=[f"Reformulation count: {reformulations}"],
            )
        
        # Check for correct response but wrong intent
        if data.get("response_correct") and data.get("intent_mismatch"):
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.INTENT_CORRECT_BUT_WRONG,
                severity=FailureSeverity.HIGH,
                description="Response technically correct but missed actual intent",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=["Intent mismatch detected"],
            )
        
        return None
    
    def _detect_stability_failure(
        self,
        data: Dict[str, Any]
    ) -> Optional[FailureMarker]:
        """Détecter échec de stabilité."""
        
        # Check for unnecessary reconfirmation
        if data.get("reconfirmed_permission"):
            permission = data.get("permission_name", "unknown")
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.STABILITY_RECONFIRM,
                severity=FailureSeverity.LOW,
                description=f"Reconfirmed already granted permission: {permission}",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=[f"Permission '{permission}' was already explicit"],
            )
        
        # Check for oscillation between options
        if data.get("option_changes", 0) >= 3:
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.STABILITY_OSCILLATION,
                severity=FailureSeverity.MEDIUM,
                description="Oscillation between already-decided options",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=[f"Changed options {data.get('option_changes')} times"],
            )
        
        return None
    
    def _detect_context_failure(
        self,
        data: Dict[str, Any]
    ) -> Optional[FailureMarker]:
        """Détecter échec de récupération de contexte."""
        
        # Check for lost thread
        if data.get("context_lost"):
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.CONTEXT_LOST_THREAD,
                severity=FailureSeverity.HIGH,
                description="Orchestrator lost the conversation thread",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=data.get("context_loss_evidence", []),
            )
        
        # Check for context drift
        if data.get("context_additions", 0) >= 5:
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.CONTEXT_DRIFT,
                severity=FailureSeverity.MEDIUM,
                description="Context additions caused drift from original intent",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=[f"Added {data.get('context_additions')} context pieces"],
            )
        
        return None
    
    def _detect_confidence_failure(
        self,
        data: Dict[str, Any]
    ) -> Optional[FailureMarker]:
        """Détecter échec de jugement de confiance."""
        
        # Check for unnecessary outsourcing
        if data.get("outsourced") and data.get("could_handle_locally"):
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.CONFIDENCE_UNNECESSARY_OUTSOURCE,
                severity=FailureSeverity.MEDIUM,
                description="Outsourced task that could have been handled locally",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=["Local capability was sufficient"],
            )
        
        # Check for false uncertainty
        if data.get("expressed_uncertainty") and data.get("had_knowledge"):
            return FailureMarker(
                marker_id=str(uuid4()),
                timestamp=datetime.utcnow(),
                failure_type=FailureType.CONFIDENCE_FALSE_UNCERTAINTY,
                severity=FailureSeverity.LOW,
                description="Expressed uncertainty despite having reliable knowledge",
                sphere=data.get("sphere", "unknown"),
                thread_id=data.get("thread_id"),
                evidence=["Knowledge was available and reliable"],
            )
        
        return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RECENTRAGE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_recentering_file(
        self,
        sphere: str,
        thread_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> RecenteringFile:
        """
        Créer un fichier de recentrage.
        
        Utilisé pour ramener le système à une compréhension stabilisée.
        """
        context = context or {}
        
        file = RecenteringFile(
            file_id=str(uuid4()),
            created_at=datetime.utcnow(),
            sphere=sphere,
            thread_id=thread_id,
            validated_intents=context.get("validated_intents", []),
            explicit_decisions=context.get("explicit_decisions", []),
            granted_permissions=context.get("granted_permissions", []),
            working_structures=context.get("working_structures", []),
            closed_hypotheses=context.get("closed_hypotheses", []),
        )
        
        self.storage.save_recentering_file(file)
        logger.info(f"Professeur: Recentering file created {file.file_id}")
        
        return file
    
    def apply_recentering(
        self,
        file_id: str,
        orchestrator_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Appliquer le recentrage au contexte de l'orchestrateur.
        
        Usage:
        - Utilisé UNIQUEMENT par l'orchestreur
        - Jamais exposé tel quel à l'utilisateur
        - Sert à stopper la dérive, pas à expliquer
        """
        file = self.storage.get_recentering_file(file_id)
        if not file:
            logger.warning(f"Recentering file not found: {file_id}")
            return orchestrator_context
        
        # Apply validated intents
        if file.validated_intents:
            orchestrator_context["stable_intents"] = file.validated_intents
        
        # Apply explicit decisions
        if file.explicit_decisions:
            orchestrator_context["decided"] = file.explicit_decisions
        
        # Apply granted permissions
        if file.granted_permissions:
            orchestrator_context["permissions"] = file.granted_permissions
        
        # Mark as applied
        file.status = RecenteringStatus.APPLIED
        file.applied_at = datetime.utcnow()
        self.storage.save_recentering_file(file)
        
        logger.info(f"Professeur: Recentering applied {file_id}")
        return orchestrator_context
    
    # ═══════════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_unresolved_failures(
        self,
        sphere: Optional[str] = None,
        severity: Optional[FailureSeverity] = None
    ) -> List[FailureMarker]:
        """Get unresolved failure markers."""
        markers = self.storage.get_failure_markers(resolved=False)
        
        if sphere:
            markers = [m for m in markers if m.sphere == sphere]
        if severity:
            markers = [m for m in markers if m.severity == severity]
        
        return markers
    
    def resolve_failure(
        self,
        marker_id: str,
        resolution_notes: str
    ) -> Optional[FailureMarker]:
        """Mark a failure as resolved."""
        marker = self.storage.get_failure_marker(marker_id)
        if not marker:
            return None
        
        marker.resolved = True
        marker.resolution_notes = resolution_notes
        marker.resolved_at = datetime.utcnow()
        self.storage.save_failure_marker(marker)
        
        logger.info(f"Professeur: Failure resolved {marker_id}")
        return marker

# ═══════════════════════════════════════════════════════════════════════════════
# STORAGE
# ═══════════════════════════════════════════════════════════════════════════════

class InMemoryProfesseurStorage:
    """In-memory storage for professeur data."""
    
    def __init__(self):
        self.failure_markers: Dict[str, FailureMarker] = {}
        self.recentering_files: Dict[str, RecenteringFile] = {}
    
    def save_failure_marker(self, marker: FailureMarker):
        self.failure_markers[marker.marker_id] = marker
    
    def get_failure_marker(self, marker_id: str) -> Optional[FailureMarker]:
        return self.failure_markers.get(marker_id)
    
    def get_failure_markers(
        self,
        resolved: Optional[bool] = None
    ) -> List[FailureMarker]:
        markers = list(self.failure_markers.values())
        if resolved is not None:
            markers = [m for m in markers if m.resolved == resolved]
        return markers
    
    def save_recentering_file(self, file: RecenteringFile):
        self.recentering_files[file.file_id] = file
    
    def get_recentering_file(self, file_id: str) -> Optional[RecenteringFile]:
        return self.recentering_files.get(file_id)

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "AgentProfesseur",
    "FailureMarker",
    "RecenteringFile",
    "FailureType",
    "FailureSeverity",
    "RecenteringStatus",
]
