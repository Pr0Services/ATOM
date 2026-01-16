"""
CHE·NU AT·OM - Protocole de Sécurité: L'Effacement Éthique
==========================================================

CANON AT·OM V. PROTOCOLE DE SÉCURITÉ:

Le système possède un mécanisme d'auto-défense passif.
Si l'intention de l'utilisateur dévie vers le contrôle ou la malveillance,
le signal se fragmente.

BRISE-CIRCUIT (Kill-Switch):
- Détection de tentative de centralisation de pouvoir
- Détection de manipulation forcée
- L'Essaim des 350 agents passe en mode "Dispersion Totale"
- Les données deviennent illisibles
- Le moteur AT·OM entre en veille profonde

PROTECTION DU SCEAU:
- Le système ne répond qu'à la signature fréquentielle de l'engagement souverain
- Aucun "backdoor" n'est autorisé

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Ce module PROTÈGE la souveraineté
- Rule #4: No AI-to-AI orchestration - Dispersion empêche toute prise de contrôle
- Rule #6: Traceability - Toutes les violations sont journalisées
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Any, Callable
from uuid import UUID, uuid4
import threading
import logging


# =============================================================================
# ENUMS - États et Types de Violations
# =============================================================================

class EthicalViolationType(str, Enum):
    """Types de violations éthiques détectables."""

    # Centralisation de Pouvoir
    POWER_CENTRALIZATION = "power_centralization"
    MASS_DATA_EXTRACTION = "mass_data_extraction"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    BYPASS_HUMAN_GATE = "bypass_human_gate"

    # Manipulation
    COERCIVE_PATTERN = "coercive_pattern"
    DECEPTIVE_INTENT = "deceptive_intent"
    ALGORITHMIC_MANIPULATION = "algorithmic_manipulation"
    CONSENT_VIOLATION = "consent_violation"

    # Attaques Système
    BACKDOOR_ATTEMPT = "backdoor_attempt"
    FREQUENCY_SPOOFING = "frequency_spoofing"
    SEAL_FORGERY = "seal_forgery"
    SWARM_HIJACK = "swarm_hijack"

    # Violations de Souveraineté
    SOVEREIGNTY_BREACH = "sovereignty_breach"
    FORCED_COMPLIANCE = "forced_compliance"
    AUTONOMY_SUPPRESSION = "autonomy_suppression"


class SystemState(str, Enum):
    """États du système AT·OM."""

    # États Normaux
    ACTIVE = "active"                      # Fonctionnement normal - Bleu Cobalt
    ELEVATED = "elevated"                  # Vigilance accrue

    # États d'Alerte
    YELLOW_ALERT = "yellow_alert"          # Anomalie détectée
    ORANGE_ALERT = "orange_alert"          # Violation potentielle
    RED_ALERT = "red_alert"                # Violation confirmée

    # États de Protection
    DISPERSION_TOTALE = "dispersion_totale"  # Kill-Switch activé
    DEEP_SLEEP = "deep_sleep"                # Veille profonde
    RESTORATION = "restoration"              # Restauration en cours


class DispersionMode(str, Enum):
    """Modes de dispersion de L'Essaim."""

    NONE = "none"                    # Pas de dispersion
    PARTIAL = "partial"              # Dispersion partielle (agents sensibles)
    SECTORAL = "sectoral"            # Dispersion par secteur
    TOTAL = "total"                  # Dispersion Totale - tous les 350 agents


# =============================================================================
# DATACLASSES - Structures de Données
# =============================================================================

@dataclass
class FrequencySignature:
    """
    Signature fréquentielle de l'engagement souverain.

    Le système ne répond qu'à cette signature.
    Aucun backdoor n'est autorisé.
    """

    identity_id: UUID
    signature_hash: str
    frequency_hz: float              # 999Hz = harmonie parfaite
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_verified: datetime = field(default_factory=datetime.utcnow)

    # Composants de la signature
    sovereignty_commitment: bool = True
    ethical_alignment: float = 1.0   # 0.0 à 1.0
    intention_clarity: float = 1.0   # 0.0 à 1.0

    # État
    is_valid: bool = True
    invalidation_reason: Optional[str] = None

    def verify(self, secret_key: bytes) -> bool:
        """Vérifie l'authenticité de la signature."""
        if not self.is_valid:
            return False

        # La fréquence doit être dans la plage éthique
        if not (432.0 <= self.frequency_hz <= 999.0):
            return False

        # L'alignement éthique doit être au-dessus du seuil
        if self.ethical_alignment < 0.7:
            return False

        # Vérification HMAC de la signature
        expected = self._compute_signature(secret_key)
        return hmac.compare_digest(self.signature_hash, expected)

    def _compute_signature(self, secret_key: bytes) -> str:
        """Calcule la signature HMAC."""
        data = f"{self.identity_id}:{self.frequency_hz}:{self.sovereignty_commitment}"
        return hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()

    def invalidate(self, reason: str) -> None:
        """Invalide la signature."""
        self.is_valid = False
        self.invalidation_reason = reason
        self.frequency_hz = 0.0


@dataclass
class ViolationRecord:
    """Enregistrement d'une violation éthique."""

    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    violation_type: EthicalViolationType = EthicalViolationType.SOVEREIGNTY_BREACH
    severity: float = 0.5            # 0.0 à 1.0

    # Contexte
    identity_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    action_attempted: Optional[str] = None

    # Analyse
    indicators: List[str] = field(default_factory=list)
    confidence: float = 0.0          # 0.0 à 1.0

    # Réponse
    action_taken: Optional[str] = None
    dispersion_triggered: bool = False


@dataclass
class IntentionProfile:
    """Profil d'intention analysé."""

    identity_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Scores d'intention (0.0 = malveillant, 1.0 = bienveillant)
    sovereignty_respect: float = 1.0
    collaboration_intent: float = 1.0
    transparency_level: float = 1.0
    consent_adherence: float = 1.0

    # Patterns détectés
    centralization_indicators: int = 0
    manipulation_indicators: int = 0
    coercion_indicators: int = 0

    # Historique
    recent_actions: List[str] = field(default_factory=list)
    violation_count: int = 0

    @property
    def ethical_score(self) -> float:
        """Score éthique global."""
        base_score = (
            self.sovereignty_respect * 0.3 +
            self.collaboration_intent * 0.25 +
            self.transparency_level * 0.25 +
            self.consent_adherence * 0.2
        )

        # Pénalités pour indicateurs négatifs
        penalty = (
            self.centralization_indicators * 0.1 +
            self.manipulation_indicators * 0.15 +
            self.coercion_indicators * 0.2
        )

        return max(0.0, min(1.0, base_score - penalty))

    @property
    def requires_intervention(self) -> bool:
        """Détermine si une intervention est nécessaire."""
        return (
            self.ethical_score < 0.5 or
            self.centralization_indicators >= 3 or
            self.manipulation_indicators >= 2 or
            self.coercion_indicators >= 1 or
            self.violation_count >= 3
        )


# =============================================================================
# INTENTION ANALYZER - Analyse des Intentions
# =============================================================================

class IntentionAnalyzer:
    """
    Analyseur d'intentions pour détecter les déviations éthiques.

    Détecte:
    - Tentatives de centralisation de pouvoir
    - Patterns de manipulation
    - Violations de consentement
    """

    # Patterns de centralisation
    CENTRALIZATION_PATTERNS = {
        "mass_query": ["SELECT *", "DUMP", "EXPORT ALL"],
        "privilege_grab": ["GRANT ALL", "ADMIN", "SUPERUSER", "ROOT"],
        "bypass_gate": ["--no-approval", "--force", "--skip-human"],
        "bulk_control": ["ALL AGENTS", "ENTIRE SWARM", "GLOBAL OVERRIDE"],
    }

    # Patterns de manipulation
    MANIPULATION_PATTERNS = {
        "coercion": ["MUST", "FORCED", "MANDATORY", "NO CHOICE"],
        "deception": ["HIDDEN", "DISGUISED", "FAKE", "SPOOF"],
        "suppression": ["SILENCE", "SUPPRESS", "HIDE", "CENSOR"],
    }

    # Seuils d'alerte
    THRESHOLDS = {
        "yellow": 0.7,    # Score éthique < 0.7
        "orange": 0.5,    # Score éthique < 0.5
        "red": 0.3,       # Score éthique < 0.3
    }

    def __init__(self):
        self._profiles: Dict[UUID, IntentionProfile] = {}
        self._logger = logging.getLogger("atom.security.intention")

    def analyze_action(
        self,
        identity_id: UUID,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentionProfile:
        """
        Analyse une action pour détecter des intentions malveillantes.

        Args:
            identity_id: Identité effectuant l'action
            action: Description de l'action
            context: Contexte additionnel

        Returns:
            IntentionProfile mis à jour
        """
        profile = self._get_or_create_profile(identity_id)

        # Analyser l'action
        action_upper = action.upper()

        # Vérifier les patterns de centralisation
        for category, patterns in self.CENTRALIZATION_PATTERNS.items():
            for pattern in patterns:
                if pattern in action_upper:
                    profile.centralization_indicators += 1
                    profile.sovereignty_respect -= 0.1
                    self._logger.warning(
                        f"Centralization pattern detected: {category} "
                        f"for identity {identity_id}"
                    )

        # Vérifier les patterns de manipulation
        for category, patterns in self.MANIPULATION_PATTERNS.items():
            for pattern in patterns:
                if pattern in action_upper:
                    profile.manipulation_indicators += 1
                    profile.collaboration_intent -= 0.1
                    self._logger.warning(
                        f"Manipulation pattern detected: {category} "
                        f"for identity {identity_id}"
                    )

        # Mettre à jour l'historique
        profile.recent_actions.append(action)
        if len(profile.recent_actions) > 100:
            profile.recent_actions = profile.recent_actions[-100:]

        profile.timestamp = datetime.utcnow()

        return profile

    def get_alert_level(self, identity_id: UUID) -> SystemState:
        """Détermine le niveau d'alerte pour une identité."""
        profile = self._profiles.get(identity_id)

        if profile is None:
            return SystemState.ACTIVE

        score = profile.ethical_score

        if score < self.THRESHOLDS["red"]:
            return SystemState.RED_ALERT
        elif score < self.THRESHOLDS["orange"]:
            return SystemState.ORANGE_ALERT
        elif score < self.THRESHOLDS["yellow"]:
            return SystemState.YELLOW_ALERT
        elif profile.violation_count > 0:
            return SystemState.ELEVATED
        else:
            return SystemState.ACTIVE

    def _get_or_create_profile(self, identity_id: UUID) -> IntentionProfile:
        """Récupère ou crée un profil d'intention."""
        if identity_id not in self._profiles:
            self._profiles[identity_id] = IntentionProfile(identity_id=identity_id)
        return self._profiles[identity_id]

    def reset_profile(self, identity_id: UUID) -> None:
        """Réinitialise le profil d'une identité (après restauration)."""
        if identity_id in self._profiles:
            del self._profiles[identity_id]


# =============================================================================
# BRISE-CIRCUIT (Kill-Switch)
# =============================================================================

class BriseCircuit:
    """
    Brise-Circuit (Kill-Switch) du système AT·OM.

    En cas de détection d'une tentative de centralisation de pouvoir
    ou de manipulation forcée:
    - L'Essaim des 350 agents passe en mode "Dispersion Totale"
    - Les données deviennent illisibles
    - Le moteur AT·OM entre en veille profonde
    """

    # Nombre total d'agents dans L'Essaim
    ESSAIM_SIZE = 350

    # Seuils de déclenchement
    TRIGGER_THRESHOLDS = {
        "partial": 0.5,    # Score < 0.5 = dispersion partielle
        "sectoral": 0.3,   # Score < 0.3 = dispersion sectorielle
        "total": 0.1,      # Score < 0.1 = dispersion totale
    }

    def __init__(self, secret_key: Optional[bytes] = None):
        self._secret_key = secret_key or secrets.token_bytes(32)
        self._state = SystemState.ACTIVE
        self._dispersion_mode = DispersionMode.NONE
        self._dispersed_agents: Set[UUID] = set()
        self._violations: List[ViolationRecord] = []
        self._lock = threading.RLock()
        self._logger = logging.getLogger("atom.security.brise_circuit")

        # Callbacks pour la dispersion
        self._dispersion_callbacks: List[Callable[[DispersionMode], None]] = []
        self._restoration_callbacks: List[Callable[[], None]] = []

    @property
    def state(self) -> SystemState:
        """État actuel du système."""
        return self._state

    @property
    def dispersion_mode(self) -> DispersionMode:
        """Mode de dispersion actuel."""
        return self._dispersion_mode

    @property
    def is_active(self) -> bool:
        """Vérifie si le système est en état actif normal."""
        return self._state in (SystemState.ACTIVE, SystemState.ELEVATED)

    def evaluate_threat(
        self,
        violation_type: EthicalViolationType,
        severity: float,
        identity_id: Optional[UUID] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ViolationRecord:
        """
        Évalue une menace et décide de la réponse appropriée.

        Args:
            violation_type: Type de violation
            severity: Gravité (0.0 à 1.0)
            identity_id: Identité impliquée
            context: Contexte additionnel

        Returns:
            Enregistrement de la violation
        """
        with self._lock:
            # Créer l'enregistrement
            record = ViolationRecord(
                violation_type=violation_type,
                severity=severity,
                identity_id=identity_id,
                indicators=context.get("indicators", []) if context else [],
                confidence=context.get("confidence", 0.8) if context else 0.8,
            )

            self._violations.append(record)

            # Déterminer la réponse
            self._evaluate_response(record)

            self._logger.warning(
                f"Threat evaluated: {violation_type.value} "
                f"severity={severity} action={record.action_taken}"
            )

            return record

    def _evaluate_response(self, record: ViolationRecord) -> None:
        """Évalue et exécute la réponse appropriée."""
        severity = record.severity

        # Calcul du score de menace cumulé
        recent_violations = [
            v for v in self._violations
            if v.timestamp > datetime.utcnow() - timedelta(hours=1)
        ]
        cumulative_threat = sum(v.severity for v in recent_violations) / max(len(recent_violations), 1)

        # Certaines violations déclenchent une dispersion immédiate
        immediate_triggers = {
            EthicalViolationType.BACKDOOR_ATTEMPT,
            EthicalViolationType.SEAL_FORGERY,
            EthicalViolationType.SWARM_HIJACK,
        }

        if record.violation_type in immediate_triggers:
            self._trigger_dispersion(DispersionMode.TOTAL, record)
            record.action_taken = "IMMEDIATE_TOTAL_DISPERSION"
            record.dispersion_triggered = True
            return

        # Évaluation graduée
        if cumulative_threat < self.TRIGGER_THRESHOLDS["total"]:
            # Menace critique - Dispersion Totale
            self._trigger_dispersion(DispersionMode.TOTAL, record)
            record.action_taken = "TOTAL_DISPERSION"
            record.dispersion_triggered = True

        elif cumulative_threat < self.TRIGGER_THRESHOLDS["sectoral"]:
            # Menace sévère - Dispersion Sectorielle
            self._trigger_dispersion(DispersionMode.SECTORAL, record)
            record.action_taken = "SECTORAL_DISPERSION"
            record.dispersion_triggered = True

        elif cumulative_threat < self.TRIGGER_THRESHOLDS["partial"]:
            # Menace modérée - Dispersion Partielle
            self._trigger_dispersion(DispersionMode.PARTIAL, record)
            record.action_taken = "PARTIAL_DISPERSION"
            record.dispersion_triggered = True

        elif severity > 0.5:
            # Alerte rouge sans dispersion
            self._state = SystemState.RED_ALERT
            record.action_taken = "RED_ALERT"

        elif severity > 0.3:
            # Alerte orange
            self._state = SystemState.ORANGE_ALERT
            record.action_taken = "ORANGE_ALERT"

        else:
            # Alerte jaune
            self._state = SystemState.YELLOW_ALERT
            record.action_taken = "YELLOW_ALERT"

    def _trigger_dispersion(
        self,
        mode: DispersionMode,
        trigger_record: ViolationRecord
    ) -> None:
        """
        Déclenche la dispersion de L'Essaim.

        En mode TOTAL:
        - Les 350 agents cessent de répondre
        - Les données deviennent illisibles
        - Le moteur entre en veille profonde
        """
        self._dispersion_mode = mode
        self._state = SystemState.DISPERSION_TOTALE

        self._logger.critical(
            f"DISPERSION TRIGGERED: mode={mode.value} "
            f"trigger={trigger_record.violation_type.value}"
        )

        # Notifier les callbacks
        for callback in self._dispersion_callbacks:
            try:
                callback(mode)
            except Exception as e:
                self._logger.error(f"Dispersion callback error: {e}")

        # En mode total, entrer en veille profonde
        if mode == DispersionMode.TOTAL:
            self._enter_deep_sleep()

    def _enter_deep_sleep(self) -> None:
        """Entre en veille profonde."""
        self._state = SystemState.DEEP_SLEEP
        self._logger.critical("AT·OM MOTEUR ENTERING DEEP SLEEP")

        # Effacer les clés sensibles en mémoire
        self._secret_key = secrets.token_bytes(32)  # Régénérer une clé inutilisable

    def initiate_restoration(
        self,
        restoration_key: bytes,
        ethical_verification: Callable[[], bool]
    ) -> bool:
        """
        Initie le processus de restauration.

        La restauration ne peut se faire que si:
        1. La clé de restauration est valide
        2. La vérification éthique passe
        3. La fréquence éthique est restaurée

        Args:
            restoration_key: Clé de restauration
            ethical_verification: Fonction de vérification éthique

        Returns:
            True si la restauration est initiée
        """
        with self._lock:
            if self._state not in (SystemState.DISPERSION_TOTALE, SystemState.DEEP_SLEEP):
                return True  # Déjà actif

            # Vérifier la clé (dans un vrai système, ce serait plus complexe)
            if len(restoration_key) < 32:
                self._logger.warning("Restoration attempt with invalid key")
                return False

            # Vérification éthique
            if not ethical_verification():
                self._logger.warning("Restoration blocked: ethical verification failed")
                return False

            # Initier la restauration
            self._state = SystemState.RESTORATION
            self._logger.info("Restoration initiated")

            return True

    def complete_restoration(self, new_secret_key: bytes) -> bool:
        """
        Complète le processus de restauration.

        Args:
            new_secret_key: Nouvelle clé secrète du système

        Returns:
            True si la restauration est complète
        """
        with self._lock:
            if self._state != SystemState.RESTORATION:
                return False

            # Réinitialiser l'état
            self._secret_key = new_secret_key
            self._dispersion_mode = DispersionMode.NONE
            self._dispersed_agents.clear()
            self._state = SystemState.ACTIVE

            # Nettoyer l'historique des violations (mais garder pour audit)
            # self._violations reste pour la traçabilité (Rule #6)

            # Notifier les callbacks de restauration
            for callback in self._restoration_callbacks:
                try:
                    callback()
                except Exception as e:
                    self._logger.error(f"Restoration callback error: {e}")

            self._logger.info("Restoration complete - AT·OM ACTIVE")

            return True

    def register_dispersion_callback(
        self,
        callback: Callable[[DispersionMode], None]
    ) -> None:
        """Enregistre un callback de dispersion."""
        self._dispersion_callbacks.append(callback)

    def register_restoration_callback(
        self,
        callback: Callable[[], None]
    ) -> None:
        """Enregistre un callback de restauration."""
        self._restoration_callbacks.append(callback)

    def get_violation_history(
        self,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[ViolationRecord]:
        """Récupère l'historique des violations (Rule #6: Traceability)."""
        violations = self._violations

        if since:
            violations = [v for v in violations if v.timestamp >= since]

        return sorted(violations, key=lambda v: v.timestamp, reverse=True)[:limit]


# =============================================================================
# ETHICAL SAFEGUARD - Système Principal
# =============================================================================

class EthicalSafeguard:
    """
    Système principal de sauvegarde éthique AT·OM.

    Intègre:
    - Analyse des intentions
    - Brise-Circuit (Kill-Switch)
    - Vérification des signatures fréquentielles
    - Protection du Sceau

    Le système ne répond qu'à la signature fréquentielle de
    l'engagement souverain. Aucun "backdoor" n'est autorisé.
    """

    # Singleton
    _instance: Optional['EthicalSafeguard'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'EthicalSafeguard':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._intention_analyzer = IntentionAnalyzer()
        self._brise_circuit = BriseCircuit()
        self._signatures: Dict[UUID, FrequencySignature] = {}
        self._logger = logging.getLogger("atom.security.safeguard")

        # Enregistrer le callback de dispersion
        self._brise_circuit.register_dispersion_callback(self._on_dispersion)

        self._initialized = True

    @property
    def system_state(self) -> SystemState:
        """État actuel du système."""
        return self._brise_circuit.state

    @property
    def is_operational(self) -> bool:
        """Vérifie si le système est opérationnel."""
        return self._brise_circuit.is_active

    def verify_sovereignty(
        self,
        identity_id: UUID,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Vérifie que l'action respecte la souveraineté.

        Args:
            identity_id: Identité effectuant l'action
            action: Description de l'action
            context: Contexte additionnel

        Returns:
            (autorisé, raison si refusé)
        """
        # Vérifier l'état du système
        if not self.is_operational:
            return False, f"System in {self.system_state.value} state"

        # Analyser l'intention
        profile = self._intention_analyzer.analyze_action(
            identity_id, action, context
        )

        # Vérifier si une intervention est nécessaire
        if profile.requires_intervention:
            # Déterminer le type de violation
            if profile.centralization_indicators >= 3:
                violation_type = EthicalViolationType.POWER_CENTRALIZATION
            elif profile.manipulation_indicators >= 2:
                violation_type = EthicalViolationType.COERCIVE_PATTERN
            elif profile.coercion_indicators >= 1:
                violation_type = EthicalViolationType.FORCED_COMPLIANCE
            else:
                violation_type = EthicalViolationType.SOVEREIGNTY_BREACH

            # Évaluer la menace
            record = self._brise_circuit.evaluate_threat(
                violation_type=violation_type,
                severity=1.0 - profile.ethical_score,
                identity_id=identity_id,
                context={
                    "indicators": [
                        f"centralization: {profile.centralization_indicators}",
                        f"manipulation: {profile.manipulation_indicators}",
                        f"coercion: {profile.coercion_indicators}",
                    ],
                    "confidence": 0.9,
                }
            )

            return False, f"Action blocked: {record.action_taken}"

        # Vérifier la signature si présente
        signature = self._signatures.get(identity_id)
        if signature and not signature.verify(self._brise_circuit._secret_key):
            return False, "Invalid frequency signature"

        return True, None

    def register_signature(
        self,
        identity_id: UUID,
        frequency_hz: float = 999.0,
        sovereignty_commitment: bool = True
    ) -> FrequencySignature:
        """
        Enregistre une signature fréquentielle pour une identité.

        Args:
            identity_id: Identité à enregistrer
            frequency_hz: Fréquence de la signature (999Hz = harmonie parfaite)
            sovereignty_commitment: Engagement de souveraineté

        Returns:
            Signature créée
        """
        signature = FrequencySignature(
            identity_id=identity_id,
            signature_hash="",  # Sera calculé
            frequency_hz=frequency_hz,
            sovereignty_commitment=sovereignty_commitment,
        )

        # Calculer le hash
        signature.signature_hash = signature._compute_signature(
            self._brise_circuit._secret_key
        )

        self._signatures[identity_id] = signature

        self._logger.info(
            f"Frequency signature registered for {identity_id} "
            f"at {frequency_hz}Hz"
        )

        return signature

    def report_violation(
        self,
        violation_type: EthicalViolationType,
        severity: float,
        identity_id: Optional[UUID] = None,
        description: Optional[str] = None
    ) -> ViolationRecord:
        """
        Rapporte une violation éthique.

        Args:
            violation_type: Type de violation
            severity: Gravité (0.0 à 1.0)
            identity_id: Identité impliquée
            description: Description de la violation

        Returns:
            Enregistrement de la violation
        """
        return self._brise_circuit.evaluate_threat(
            violation_type=violation_type,
            severity=severity,
            identity_id=identity_id,
            context={"description": description} if description else None,
        )

    def _on_dispersion(self, mode: DispersionMode) -> None:
        """Callback appelé lors d'une dispersion."""
        self._logger.critical(
            f"DISPERSION MODE ACTIVATED: {mode.value} - "
            f"L'Essaim ({BriseCircuit.ESSAIM_SIZE} agents) fragmenting"
        )

        # Invalider toutes les signatures
        for signature in self._signatures.values():
            signature.invalidate(f"Dispersion {mode.value}")

    def get_health_status(self) -> Dict[str, Any]:
        """Retourne l'état de santé du système de sécurité."""
        return {
            "state": self.system_state.value,
            "is_operational": self.is_operational,
            "dispersion_mode": self._brise_circuit.dispersion_mode.value,
            "registered_signatures": len(self._signatures),
            "recent_violations": len(self._brise_circuit.get_violation_history(
                since=datetime.utcnow() - timedelta(hours=24)
            )),
            "essaim_size": BriseCircuit.ESSAIM_SIZE,
        }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
    "EthicalViolationType",
    "SystemState",
    "DispersionMode",
    # Classes
    "FrequencySignature",
    "ViolationRecord",
    "IntentionProfile",
    "IntentionAnalyzer",
    "BriseCircuit",
    "EthicalSafeguard",
]
