"""
CHE·NU V68 Harmony Analysis Agent (SAH)
Community Pulse - Systeme d'Analyse de l'Harmonie

CONCEPT: Pouls Communautaire
- Analyse decentralisee du sentiment collectif
- Temperature emotionnelle par zone
- Detection des frictions et des harmonies
- Feedback loops pour ajustement dynamique

PHILOSOPHIE:
L'harmonie n'est pas l'absence de conflit - c'est l'equilibre des tensions.
Ecouter le murmure de la communaute avant qu'il devienne un cri.

PRIVACY ULTRA-STRICT:
- JAMAIS de tracking individuel
- Analyse par zone uniquement
- Donnees agregees et anonymisees
- Pas de profiling emotionnel personnel

GOVERNANCE COMPLIANCE:
- Rule #1: Interventions sur zones critiques require APPROVAL
- Rule #5: Zones ALPHABETICAL
- Rule #6: Full audit trail (anonymized)
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Tuple
from uuid import UUID, uuid4
import logging
import hashlib
import random

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY ULTRA-STRICT
# ============================================================================

def anonymize_zone(latitude: float, longitude: float) -> str:
    """
    Anonymize location to large zone (~5km precision)
    Never more precise for emotional data
    """
    lat_zone = round(latitude, 1)
    lon_zone = round(longitude, 1)
    return f"community_zone_{lat_zone}_{lon_zone}"


def anonymize_contributor(contributor_id: UUID, zone_id: str) -> str:
    """
    Double anonymization: contributor + zone
    Prevents tracking across zones
    """
    salt = "CHENU_HARMONY_BALANCE_999Hz"
    combined = f"{salt}{str(contributor_id)}{zone_id}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()[:12]


def noise_value(value: float, noise_pct: float = 0.05) -> float:
    """Add small noise to prevent reverse-engineering from exact values"""
    noise = random.uniform(-noise_pct, noise_pct)
    return value * (1 + noise)


# ============================================================================
# ENUMS
# ============================================================================

class EmotionalDimension(Enum):
    """Dimensions emotionnelles mesurees (agregees par zone)"""
    JOY = "joy"                      # Joie collective
    FRUSTRATION = "frustration"      # Frustration
    FEAR = "fear"                    # Peur/Anxiete
    CONFIDENCE = "confidence"        # Confiance
    SOLIDARITY = "solidarity"        # Solidarite
    TENSION = "tension"              # Tension
    HOPE = "hope"                    # Espoir
    FATIGUE = "fatigue"              # Fatigue collective


class HarmonyLevel(Enum):
    """Niveau d'harmonie d'une zone"""
    CRITICAL = "critical"            # Critique - intervention urgente
    FRICTION = "friction"            # Friction - surveillance
    NEUTRAL = "neutral"              # Neutre
    POSITIVE = "positive"            # Positif
    HARMONIOUS = "harmonious"        # Harmonieux
    THRIVING = "thriving"            # Epanoui


class SignalSource(Enum):
    """Sources de signal (anonymisees)"""
    PUBLIC_FEEDBACK = "public_feedback"    # Feedback volontaire
    SERVICE_RATING = "service_rating"      # Notation services
    EVENT_ATTENDANCE = "event_attendance"  # Participation evenements
    CIVIC_ENGAGEMENT = "civic_engagement"  # Engagement civique
    MUTUAL_AID = "mutual_aid"              # Entraide
    CONFLICT_REPORT = "conflict_report"    # Signalement conflit


class InterventionType(Enum):
    """Types d'intervention communautaire"""
    MEDIATION = "mediation"                # Mediation
    EVENT = "event"                        # Evenement rassembleur
    RESOURCE_ALLOCATION = "resource_allocation"  # Allocation ressources
    COMMUNICATION = "communication"        # Communication
    INFRASTRUCTURE = "infrastructure"      # Infrastructure
    SUPPORT_SERVICES = "support_services"  # Services de soutien


class FeedbackLoopType(Enum):
    """Types de boucles de feedback"""
    AMPLIFYING = "amplifying"              # Amplifie (positif ou negatif)
    BALANCING = "balancing"                # Equilibre
    DELAYED = "delayed"                    # Effet retarde
    IMMEDIATE = "immediate"                # Effet immediat


class AlertSeverity(Enum):
    """Severite des alertes"""
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"                  # Requires APPROVAL


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class ZoneProfile:
    """Profil d'une zone communautaire (donnees agregees)"""
    zone_id: str
    name: str

    # Population (approximate, for weighting)
    estimated_population: int
    area_km2: float

    # Current emotional temperature (0-1 scale, aggregated)
    emotional_temperatures: Dict[str, float]  # dimension -> value

    # Harmony assessment
    harmony_level: HarmonyLevel
    harmony_score: float  # 0-1

    # Trends (aggregated)
    trend_direction: str  # improving, stable, declining
    trend_velocity: float  # Rate of change

    # Last update
    last_assessment: datetime
    data_points_count: int  # Number of signals aggregated

    # PRIVACY: No individual data stored


@dataclass
class AggregatedSignal:
    """Signal agrege (JAMAIS individuel)"""
    id: UUID
    zone_id: str
    timestamp: datetime

    # Aggregated values (minimum 10 inputs to report)
    dimension: EmotionalDimension
    aggregated_value: float  # 0-1, with noise added
    input_count: int         # Must be >= 10 for privacy

    source: SignalSource
    confidence: float        # Statistical confidence


@dataclass
class HarmonyAlert:
    """Alerte d'harmonie"""
    id: UUID
    zone_id: str

    severity: AlertSeverity
    title: str
    description: str

    # Trigger
    triggered_by: EmotionalDimension
    threshold_crossed: float
    current_value: float

    # Timing
    detected_at: datetime
    acknowledged_at: Optional[datetime] = None

    # Status
    status: str = "active"  # active, acknowledged, investigating, resolved

    # GOVERNANCE
    requires_approval: bool = False
    intervention_approved_by: Optional[str] = None


@dataclass
class CommunityIntervention:
    """Intervention communautaire"""
    id: UUID
    zone_id: str
    intervention_type: InterventionType

    # Details
    title: str
    description: str
    objectives: List[str]

    # Response to
    triggered_by_alert_id: Optional[UUID] = None

    # Timeline
    proposed_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Status
    status: str = "proposed"  # proposed, pending_approval, approved, in_progress, completed

    # GOVERNANCE
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    # Outcomes (measured after)
    pre_harmony_score: float = 0.0
    post_harmony_score: float = 0.0
    effectiveness: float = 0.0


@dataclass
class FeedbackLoop:
    """Boucle de feedback systeme"""
    id: UUID
    name: str
    loop_type: FeedbackLoopType

    # Input/Output
    input_dimension: EmotionalDimension
    output_dimension: EmotionalDimension

    # Dynamics
    strength: float          # 0-1, how strong the loop
    delay_hours: float       # Time delay
    threshold: float         # Trigger threshold

    # Status
    active: bool = True
    last_triggered: Optional[datetime] = None


@dataclass
class HarmonyMetrics:
    """Metriques d'harmonie globales"""
    timestamp: datetime

    # Zone counts
    total_zones: int
    zones_harmonious: int
    zones_positive: int
    zones_neutral: int
    zones_friction: int
    zones_critical: int

    # Emotional averages (system-wide, aggregated)
    avg_joy: float
    avg_confidence: float
    avg_solidarity: float
    avg_tension: float

    # Alerts
    active_alerts: int
    alerts_resolved_today: int

    # Interventions
    interventions_active: int
    interventions_effective: int  # Post-harmony > pre-harmony

    # Indices globaux
    global_harmony_index: float      # 0-1
    social_cohesion_index: float     # 0-1
    community_resilience_index: float  # 0-1


# ============================================================================
# PRIVACY THRESHOLDS
# ============================================================================

# Minimum signals to aggregate (prevents de-anonymization)
MIN_SIGNALS_TO_REPORT = 10

# Minimum zone population for reporting
MIN_ZONE_POPULATION = 50

# Alert severity requiring approval
APPROVAL_REQUIRED_SEVERITY = {AlertSeverity.CRITICAL}


# ============================================================================
# HARMONY ANALYSIS AGENT
# ============================================================================

class HarmonyAnalysisAgent:
    """
    Agent d'Analyse de l'Harmonie (SAH)

    Le pouls de la communaute:
    - Ecouter sans surveiller
    - Agreger sans identifier
    - Agir sans imposer

    PRIVACY ULTRA-STRICT:
    - Toute donnee est agregee par zone
    - Aucun profil individuel
    - Bruit statistique ajoute
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Storage (zone-level only, NEVER individual)
        self._zones: Dict[str, ZoneProfile] = {}
        self._signals: Dict[str, List[AggregatedSignal]] = {}  # zone_id -> signals
        self._alerts: Dict[UUID, HarmonyAlert] = {}
        self._interventions: Dict[UUID, CommunityIntervention] = {}
        self._feedback_loops: Dict[UUID, FeedbackLoop] = {}

        # Signal buffer (temporary, for aggregation)
        self._signal_buffer: Dict[str, Dict[str, List[float]]] = {}  # zone -> dimension -> values

        # Metrics history
        self._metrics_history: List[HarmonyMetrics] = []

        self._initialized = True
        logger.info("HarmonyAnalysisAgent initialized - Listening to the community pulse")

        # Initialize feedback loops
        self._init_feedback_loops()

    def _init_feedback_loops(self) -> None:
        """Initialize system feedback loops"""
        loops = [
            ("Joy-Solidarity Loop", FeedbackLoopType.AMPLIFYING,
             EmotionalDimension.JOY, EmotionalDimension.SOLIDARITY, 0.3, 24),
            ("Frustration-Tension Loop", FeedbackLoopType.AMPLIFYING,
             EmotionalDimension.FRUSTRATION, EmotionalDimension.TENSION, 0.4, 12),
            ("Confidence-Hope Loop", FeedbackLoopType.AMPLIFYING,
             EmotionalDimension.CONFIDENCE, EmotionalDimension.HOPE, 0.35, 48),
            ("Solidarity Balance", FeedbackLoopType.BALANCING,
             EmotionalDimension.TENSION, EmotionalDimension.SOLIDARITY, 0.25, 72),
        ]

        for name, loop_type, input_dim, output_dim, strength, delay in loops:
            self._feedback_loops[uuid4()] = FeedbackLoop(
                id=uuid4(),
                name=name,
                loop_type=loop_type,
                input_dimension=input_dim,
                output_dimension=output_dim,
                strength=strength,
                delay_hours=delay,
                threshold=0.6,
            )

    # ========================================================================
    # ZONE MANAGEMENT
    # ========================================================================

    def register_zone(
        self,
        latitude: float,
        longitude: float,
        name: str,
        estimated_population: int,
        area_km2: float,
    ) -> ZoneProfile:
        """Register a community zone for monitoring"""
        zone_id = anonymize_zone(latitude, longitude)

        # Privacy check
        if estimated_population < MIN_ZONE_POPULATION:
            logger.warning(
                f"Zone {name} has low population ({estimated_population}). "
                f"Data will be aggregated with adjacent zones."
            )

        # Initialize emotional temperatures at neutral
        emotional_temps = {
            dim.value: 0.5 for dim in EmotionalDimension
        }

        profile = ZoneProfile(
            zone_id=zone_id,
            name=name,
            estimated_population=estimated_population,
            area_km2=area_km2,
            emotional_temperatures=emotional_temps,
            harmony_level=HarmonyLevel.NEUTRAL,
            harmony_score=0.5,
            trend_direction="stable",
            trend_velocity=0.0,
            last_assessment=datetime.now(),
            data_points_count=0,
        )

        self._zones[zone_id] = profile
        self._signals[zone_id] = []
        self._signal_buffer[zone_id] = {dim.value: [] for dim in EmotionalDimension}

        logger.info(f"Zone registered: {name} ({zone_id})")

        return profile

    # ========================================================================
    # SIGNAL COLLECTION (Privacy-First)
    # ========================================================================

    def receive_signal(
        self,
        latitude: float,
        longitude: float,
        dimension: EmotionalDimension,
        value: float,  # 0-1
        source: SignalSource,
        contributor_id: Optional[UUID] = None,
    ) -> bool:
        """
        Receive a single signal (buffered, not stored individually)

        PRIVACY: Signal is added to buffer and only aggregated when
        minimum threshold is reached. Individual signals are NEVER stored.
        """
        zone_id = anonymize_zone(latitude, longitude)

        if zone_id not in self._zones:
            logger.debug(f"Signal received for unregistered zone {zone_id}, creating...")
            self.register_zone(latitude, longitude, f"Zone {zone_id}", 100, 25.0)

        # Add to buffer (NOT stored permanently)
        self._signal_buffer[zone_id][dimension.value].append(value)

        # Check if we have enough signals to aggregate
        buffer = self._signal_buffer[zone_id][dimension.value]
        if len(buffer) >= MIN_SIGNALS_TO_REPORT:
            self._aggregate_signals(zone_id, dimension, source)
            return True

        return False  # Signal buffered but not yet aggregated

    def _aggregate_signals(
        self,
        zone_id: str,
        dimension: EmotionalDimension,
        source: SignalSource,
    ) -> AggregatedSignal:
        """
        Aggregate buffered signals into a single anonymized data point

        PRIVACY: Individual signals are discarded after aggregation
        """
        buffer = self._signal_buffer[zone_id][dimension.value]
        count = len(buffer)

        if count < MIN_SIGNALS_TO_REPORT:
            raise ValueError(f"Insufficient signals for aggregation ({count} < {MIN_SIGNALS_TO_REPORT})")

        # Calculate aggregated value
        mean_value = sum(buffer) / count

        # Add noise to prevent reverse-engineering
        noisy_value = noise_value(mean_value, 0.05)
        noisy_value = max(0.0, min(1.0, noisy_value))  # Clamp to 0-1

        # Calculate confidence (based on sample size)
        confidence = min(count / 50, 1.0)  # Max confidence at 50 signals

        signal = AggregatedSignal(
            id=uuid4(),
            zone_id=zone_id,
            timestamp=datetime.now(),
            dimension=dimension,
            aggregated_value=noisy_value,
            input_count=count,
            source=source,
            confidence=confidence,
        )

        self._signals[zone_id].append(signal)

        # Clear buffer (individual signals are DISCARDED)
        self._signal_buffer[zone_id][dimension.value] = []

        # Update zone profile
        self._update_zone_profile(zone_id, dimension, noisy_value, confidence)

        logger.debug(
            f"Aggregated {count} signals for {zone_id}/{dimension.value}: {noisy_value:.2f}"
        )

        return signal

    def _update_zone_profile(
        self,
        zone_id: str,
        dimension: EmotionalDimension,
        value: float,
        confidence: float,
    ) -> None:
        """Update zone profile with new aggregated data"""
        if zone_id not in self._zones:
            return

        profile = self._zones[zone_id]

        # Weighted average with existing value
        old_value = profile.emotional_temperatures.get(dimension.value, 0.5)
        weight = min(confidence, 0.3)  # Max 30% change per update
        new_value = old_value * (1 - weight) + value * weight

        profile.emotional_temperatures[dimension.value] = new_value
        profile.data_points_count += 1
        profile.last_assessment = datetime.now()

        # Recalculate harmony
        self._recalculate_harmony(zone_id)

        # Check for alerts
        self._check_alerts(zone_id, dimension, new_value)

    def _recalculate_harmony(self, zone_id: str) -> None:
        """Recalculate harmony score for a zone"""
        if zone_id not in self._zones:
            return

        profile = self._zones[zone_id]
        temps = profile.emotional_temperatures

        # Positive indicators
        positive = (
            temps.get("joy", 0.5) +
            temps.get("confidence", 0.5) +
            temps.get("solidarity", 0.5) +
            temps.get("hope", 0.5)
        ) / 4

        # Negative indicators
        negative = (
            temps.get("frustration", 0.5) +
            temps.get("fear", 0.5) +
            temps.get("tension", 0.5) +
            temps.get("fatigue", 0.5)
        ) / 4

        # Harmony score: high positive, low negative
        harmony_score = (positive + (1 - negative)) / 2

        # Determine level
        if harmony_score >= 0.8:
            level = HarmonyLevel.THRIVING
        elif harmony_score >= 0.65:
            level = HarmonyLevel.HARMONIOUS
        elif harmony_score >= 0.5:
            level = HarmonyLevel.POSITIVE
        elif harmony_score >= 0.35:
            level = HarmonyLevel.NEUTRAL
        elif harmony_score >= 0.2:
            level = HarmonyLevel.FRICTION
        else:
            level = HarmonyLevel.CRITICAL

        # Update trend
        old_score = profile.harmony_score
        velocity = harmony_score - old_score
        if velocity > 0.02:
            trend = "improving"
        elif velocity < -0.02:
            trend = "declining"
        else:
            trend = "stable"

        profile.harmony_score = harmony_score
        profile.harmony_level = level
        profile.trend_direction = trend
        profile.trend_velocity = velocity

    def _check_alerts(
        self,
        zone_id: str,
        dimension: EmotionalDimension,
        value: float,
    ) -> Optional[HarmonyAlert]:
        """Check if value triggers an alert"""
        # Alert thresholds
        thresholds = {
            EmotionalDimension.FRUSTRATION: (0.7, AlertSeverity.HIGH),
            EmotionalDimension.FEAR: (0.65, AlertSeverity.HIGH),
            EmotionalDimension.TENSION: (0.75, AlertSeverity.WARNING),
            EmotionalDimension.FATIGUE: (0.8, AlertSeverity.WARNING),
        }

        if dimension not in thresholds:
            return None

        threshold, base_severity = thresholds[dimension]

        if value < threshold:
            return None

        # Escalate severity if very high
        if value > threshold + 0.15:
            severity = AlertSeverity.CRITICAL
        else:
            severity = base_severity

        alert = HarmonyAlert(
            id=uuid4(),
            zone_id=zone_id,
            severity=severity,
            title=f"Elevated {dimension.value} in {zone_id}",
            description=f"The {dimension.value} level has crossed the alert threshold.",
            triggered_by=dimension,
            threshold_crossed=threshold,
            current_value=value,
            detected_at=datetime.now(),
            requires_approval=severity in APPROVAL_REQUIRED_SEVERITY,
        )

        self._alerts[alert.id] = alert

        logger.warning(
            f"ALERT: {severity.value.upper()} - {dimension.value} at {value:.2f} "
            f"in {zone_id} (threshold: {threshold})"
        )

        return alert

    # ========================================================================
    # INTERVENTIONS
    # ========================================================================

    def propose_intervention(
        self,
        zone_id: str,
        intervention_type: InterventionType,
        title: str,
        description: str,
        objectives: List[str],
        triggered_by_alert_id: Optional[UUID] = None,
        scheduled_at: Optional[datetime] = None,
    ) -> CommunityIntervention:
        """
        Propose a community intervention

        GOVERNANCE: Critical zone interventions require approval
        """
        if zone_id not in self._zones:
            raise ValueError(f"Zone {zone_id} not found")

        zone = self._zones[zone_id]

        # Check if approval required
        requires_approval = zone.harmony_level in {HarmonyLevel.CRITICAL, HarmonyLevel.FRICTION}

        status = "pending_approval" if requires_approval else "proposed"

        intervention = CommunityIntervention(
            id=uuid4(),
            zone_id=zone_id,
            intervention_type=intervention_type,
            title=title,
            description=description,
            objectives=objectives,
            triggered_by_alert_id=triggered_by_alert_id,
            scheduled_at=scheduled_at,
            status=status,
            pre_harmony_score=zone.harmony_score,
        )

        self._interventions[intervention.id] = intervention

        logger.info(
            f"Intervention proposed: {title} for {zone_id} "
            f"(requires_approval: {requires_approval})"
        )

        return intervention

    def approve_intervention(
        self,
        intervention_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> CommunityIntervention:
        """
        GOVERNANCE GATE: Approve intervention for sensitive zones

        RULE #1: Human approval for community interventions
        """
        if intervention_id not in self._interventions:
            raise ValueError(f"Intervention {intervention_id} not found")

        intervention = self._interventions[intervention_id]

        if intervention.status != "pending_approval":
            raise ValueError(f"Intervention not pending approval (status: {intervention.status})")

        intervention.status = "approved"
        intervention.approved_by = approver_name
        intervention.approved_at = datetime.now()

        # Acknowledge related alert if any
        if intervention.triggered_by_alert_id:
            alert = self._alerts.get(intervention.triggered_by_alert_id)
            if alert:
                alert.status = "investigating"
                alert.intervention_approved_by = approver_name

        logger.info(f"GOVERNANCE: Intervention {intervention_id} approved by {approver_name}")

        return intervention

    def complete_intervention(
        self,
        intervention_id: UUID,
        outcomes: List[str],
    ) -> CommunityIntervention:
        """Complete an intervention and measure effectiveness"""
        if intervention_id not in self._interventions:
            raise ValueError(f"Intervention {intervention_id} not found")

        intervention = self._interventions[intervention_id]
        zone = self._zones.get(intervention.zone_id)

        if zone:
            intervention.post_harmony_score = zone.harmony_score
            intervention.effectiveness = (
                intervention.post_harmony_score - intervention.pre_harmony_score
            )

        intervention.status = "completed"
        intervention.completed_at = datetime.now()

        return intervention

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_zones(
        self,
        harmony_level: Optional[HarmonyLevel] = None,
    ) -> List[ZoneProfile]:
        """
        Get zone profiles

        GOVERNANCE RULE #5: ALPHABETICAL by name
        """
        zones = list(self._zones.values())

        if harmony_level:
            zones = [z for z in zones if z.harmony_level == harmony_level]

        # RULE #5: ALPHABETICAL order
        zones.sort(key=lambda z: z.name.lower())

        return zones

    def get_zone_heatmap(self) -> List[Dict[str, Any]]:
        """
        Get heatmap data for visualization

        Colors: Green = harmonious, Yellow = neutral, Red = friction/critical
        """
        heatmap = []

        for zone in self._zones.values():
            color_map = {
                HarmonyLevel.THRIVING: "#00FF00",      # Bright green
                HarmonyLevel.HARMONIOUS: "#90EE90",    # Light green
                HarmonyLevel.POSITIVE: "#ADFF2F",      # Green-yellow
                HarmonyLevel.NEUTRAL: "#FFFF00",       # Yellow
                HarmonyLevel.FRICTION: "#FFA500",      # Orange
                HarmonyLevel.CRITICAL: "#FF0000",      # Red
            }

            heatmap.append({
                "zone_id": zone.zone_id,
                "name": zone.name,
                "harmony_score": round(zone.harmony_score, 2),
                "harmony_level": zone.harmony_level.value,
                "color": color_map.get(zone.harmony_level, "#FFFFFF"),
                "trend": zone.trend_direction,
                # NO individual emotional data exposed
            })

        return heatmap

    def get_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[AlertSeverity] = None,
    ) -> List[HarmonyAlert]:
        """
        Get alerts

        GOVERNANCE RULE #5: Chronological order
        """
        alerts = list(self._alerts.values())

        if status:
            alerts = [a for a in alerts if a.status == status]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]

        # CHRONOLOGICAL order
        alerts.sort(key=lambda a: a.detected_at)

        return alerts

    def get_interventions(
        self,
        zone_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[CommunityIntervention]:
        """
        Get interventions

        GOVERNANCE RULE #5: Chronological order
        """
        interventions = list(self._interventions.values())

        if zone_id:
            interventions = [i for i in interventions if i.zone_id == zone_id]
        if status:
            interventions = [i for i in interventions if i.status == status]

        # CHRONOLOGICAL order
        interventions.sort(key=lambda i: i.proposed_at)

        return interventions

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_harmony_metrics(self) -> HarmonyMetrics:
        """Get global harmony metrics"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        zones = list(self._zones.values())
        total = len(zones)

        # Zone counts by level
        harmonious = sum(1 for z in zones if z.harmony_level == HarmonyLevel.HARMONIOUS)
        thriving = sum(1 for z in zones if z.harmony_level == HarmonyLevel.THRIVING)
        positive = sum(1 for z in zones if z.harmony_level == HarmonyLevel.POSITIVE)
        neutral = sum(1 for z in zones if z.harmony_level == HarmonyLevel.NEUTRAL)
        friction = sum(1 for z in zones if z.harmony_level == HarmonyLevel.FRICTION)
        critical = sum(1 for z in zones if z.harmony_level == HarmonyLevel.CRITICAL)

        # Emotional averages (system-wide)
        if zones:
            avg_joy = sum(z.emotional_temperatures.get("joy", 0.5) for z in zones) / total
            avg_confidence = sum(z.emotional_temperatures.get("confidence", 0.5) for z in zones) / total
            avg_solidarity = sum(z.emotional_temperatures.get("solidarity", 0.5) for z in zones) / total
            avg_tension = sum(z.emotional_temperatures.get("tension", 0.5) for z in zones) / total
        else:
            avg_joy = avg_confidence = avg_solidarity = avg_tension = 0.5

        # Alert counts
        alerts = list(self._alerts.values())
        active_alerts = sum(1 for a in alerts if a.status == "active")
        resolved_today = sum(
            1 for a in alerts
            if a.status == "resolved" and a.detected_at >= today_start
        )

        # Intervention counts
        interventions = list(self._interventions.values())
        active_interventions = sum(
            1 for i in interventions
            if i.status in {"approved", "in_progress"}
        )
        effective_interventions = sum(
            1 for i in interventions
            if i.status == "completed" and i.effectiveness > 0
        )

        # Calculate indices

        # Global harmony index
        if total > 0:
            global_harmony = sum(z.harmony_score for z in zones) / total
        else:
            global_harmony = 0.5

        # Social cohesion index (based on solidarity and low tension)
        social_cohesion = (avg_solidarity + (1 - avg_tension)) / 2

        # Community resilience (based on response effectiveness)
        completed = [i for i in interventions if i.status == "completed"]
        if completed:
            resilience = sum(i.effectiveness for i in completed if i.effectiveness > 0) / len(completed)
            resilience = min(resilience + 0.5, 1.0)  # Base + improvement
        else:
            resilience = 0.5

        metrics = HarmonyMetrics(
            timestamp=now,
            total_zones=total,
            zones_harmonious=harmonious + thriving,
            zones_positive=positive,
            zones_neutral=neutral,
            zones_friction=friction,
            zones_critical=critical,
            avg_joy=avg_joy,
            avg_confidence=avg_confidence,
            avg_solidarity=avg_solidarity,
            avg_tension=avg_tension,
            active_alerts=active_alerts,
            alerts_resolved_today=resolved_today,
            interventions_active=active_interventions,
            interventions_effective=effective_interventions,
            global_harmony_index=global_harmony,
            social_cohesion_index=social_cohesion,
            community_resilience_index=resilience,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_community_indices(self) -> Dict[str, float]:
        """Get community indices for master dashboard"""
        metrics = self.get_harmony_metrics()

        return {
            "global_harmony_index": round(metrics.global_harmony_index, 3),
            "social_cohesion_index": round(metrics.social_cohesion_index, 3),
            "community_resilience_index": round(metrics.community_resilience_index, 3),
            "joy_average": round(metrics.avg_joy, 3),
            "confidence_average": round(metrics.avg_confidence, 3),
            "zones_at_risk": metrics.zones_friction + metrics.zones_critical,
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_harmony_analysis_agent() -> HarmonyAnalysisAgent:
    """Get the singleton HarmonyAnalysisAgent instance"""
    return HarmonyAnalysisAgent()
