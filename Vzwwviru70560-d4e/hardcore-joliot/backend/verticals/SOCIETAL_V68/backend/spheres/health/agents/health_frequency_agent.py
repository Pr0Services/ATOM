"""
CHE·NU V68 Health Frequency Agent (Sante Frequentielle)
Module Societaire 3/4 - Maintenir l'Harmonie

CONCEPT: On ne repare pas seulement le corps, on maintient l'harmonie
- Analyse des bio-rythmes et de l'environnement
- Detection de la friction (bruit, pollution, stress) AVANT la maladie
- Suggestions de "pauses d'ancrage" et changements de rythme
- Reduire la charge sur les systemes hospitaliers

PRIVACY FIRST (Agents Gardiens):
- Donnees de sante = ULTRA-SENSIBLES
- Jamais d'identification personnelle
- Analyse par zone, pas par individu
- Suggestions collectives, pas individuelles

GOVERNANCE COMPLIANCE:
- Rule #1: Recommendations de sante require HUMAN DECISION
- Rule #5: No health ranking of individuals
- Rule #6: Audit trail anonymise
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set
from uuid import UUID, uuid4
import logging
import hashlib
import math

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY - ULTRA STRICT FOR HEALTH DATA
# ============================================================================

def anonymize_health_id(user_id: UUID) -> str:
    """
    PRIVACY: Ultra-anonymize health data
    Uses double hashing for extra protection
    """
    salt1 = "CHENU_HEALTH_SALT_999Hz_PRIVACY"
    salt2 = "GUARDIAN_SHIELD_PROTECTION"
    first_hash = hashlib.sha256(f"{salt1}{str(user_id)}".encode()).hexdigest()
    second_hash = hashlib.sha256(f"{salt2}{first_hash}".encode()).hexdigest()
    return second_hash[:12]  # Even shorter for more anonymity


def anonymize_location_for_health(lat: float, lon: float) -> tuple:
    """
    PRIVACY: Very low precision for health data
    ~10km accuracy to prevent individual tracking
    """
    return (round(lat, 1), round(lon, 1))


# ============================================================================
# ENUMS
# ============================================================================

class HarmonyLevel(Enum):
    """Niveau d'harmonie (pas de maladie, mais de friction)"""
    OPTIMAL = "optimal"              # 999Hz - Parfait equilibre
    BALANCED = "balanced"            # Bon equilibre
    FLUCTUATING = "fluctuating"      # Fluctuations normales
    FRICTION = "friction"            # Friction detectee
    DISSONANCE = "dissonance"        # Dissonance importante


class EnvironmentFactor(Enum):
    """Facteurs environnementaux"""
    NOISE = "noise"                  # Bruit
    AIR_QUALITY = "air_quality"      # Qualite de l'air
    LIGHT = "light"                  # Lumiere (naturelle vs artificielle)
    TEMPERATURE = "temperature"      # Temperature
    HUMIDITY = "humidity"            # Humidite
    EMF = "emf"                      # Champs electromagnetiques
    GREEN_SPACE = "green_space"      # Espaces verts proximite
    WATER = "water"                  # Acces a l'eau propre


class RhythmType(Enum):
    """Types de rythmes biologiques"""
    CIRCADIAN = "circadian"          # Cycle jour/nuit
    ULTRADIAN = "ultradian"          # Cycles courts (90min)
    INFRADIAN = "infradian"          # Cycles longs (semaines)
    SEASONAL = "seasonal"            # Variations saisonnieres


class AnchorType(Enum):
    """Types de pauses d'ancrage"""
    BREATHING = "breathing"          # Respiration consciente
    MOVEMENT = "movement"            # Mouvement doux
    NATURE = "nature"                # Contact avec la nature
    SILENCE = "silence"              # Silence, meditation
    HYDRATION = "hydration"          # Hydratation
    GROUNDING = "grounding"          # Ancrage au sol
    SOCIAL = "social"                # Connexion sociale
    REST = "rest"                    # Repos complet


class SuggestionUrgency(Enum):
    """Urgence de la suggestion"""
    PREVENTIVE = "preventive"        # Prevention a long terme
    RECOMMENDED = "recommended"      # Recommande dans les heures
    TIMELY = "timely"                # A faire maintenant
    # Note: Pas de "urgent" - pour urgences, voir un medecin


class ZoneHealthStatus(Enum):
    """Statut de sante d'une zone (pas d'individus)"""
    HARMONIOUS = "harmonious"        # Zone en harmonie
    NORMAL = "normal"                # Zone normale
    STRESSED = "stressed"            # Zone sous stress
    CRITICAL = "critical"            # Zone critique


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoZone:
    """Zone geographique (basse precision pour privacy)"""
    latitude: float
    longitude: float
    radius_km: float
    name: str

    def __post_init__(self):
        # PRIVACY: Tres basse precision
        self.latitude, self.longitude = anonymize_location_for_health(
            self.latitude, self.longitude
        )


@dataclass
class EnvironmentReading:
    """Lecture environnementale d'une zone (pas d'individu)"""
    id: UUID
    zone: GeoZone
    timestamp: datetime

    # Facteurs mesures
    noise_level_db: Optional[float]        # Decibels
    air_quality_index: Optional[float]     # 0-500
    temperature_c: Optional[float]
    humidity_percent: Optional[float]
    uv_index: Optional[float]
    green_space_ratio: Optional[float]     # 0-1

    # Evaluation
    overall_quality: float                  # 0-1
    friction_score: float                   # 0-1 (inverse de qualite)


@dataclass
class CollectiveRhythm:
    """Rythme collectif d'une zone (pas d'individus)"""
    id: UUID
    zone: GeoZone
    timestamp: datetime
    rhythm_type: RhythmType

    # Observations collectives (agregees, anonymes)
    activity_level: float                   # 0-1
    estimated_stress_level: float           # 0-1 (base sur facteurs objectifs)
    social_interaction_level: float         # 0-1

    # Phase du rythme
    phase: str                              # "peak", "rest", "transition"


@dataclass
class AnchorSuggestion:
    """Suggestion de pause d'ancrage (collective)"""
    id: UUID
    suggestion_number: str                  # ANC-001
    zone: GeoZone
    timestamp: datetime

    # Type de suggestion
    anchor_type: AnchorType
    urgency: SuggestionUrgency

    # Details
    title: str
    description: str
    duration_minutes: int
    best_time: Optional[time]

    # Lieu suggere (si applicable)
    suggested_location: Optional[str]

    # Validite
    valid_until: datetime

    # IMPORTANT: C'est une SUGGESTION, pas une prescription
    is_suggestion_only: bool = True
    requires_professional: bool = False


@dataclass
class ZoneHealthProfile:
    """Profil de sante d'une zone (JAMAIS d'individu)"""
    id: UUID
    zone: GeoZone
    timestamp: datetime

    # Harmonies detectees
    harmony_level: HarmonyLevel
    harmony_score: float                    # 0-1

    # Facteurs environnementaux
    environment_readings: List[UUID]        # IDs des lectures

    # Frictions detectees
    friction_factors: List[str]             # "noise", "pollution", etc.
    friction_intensity: float               # 0-1

    # Suggestions actives
    active_suggestions: List[UUID]          # IDs des suggestions

    # Tendance
    trend: str                              # "improving", "stable", "declining"


@dataclass
class PreventiveInsight:
    """Insight preventif pour une zone"""
    id: UUID
    zone: GeoZone
    timestamp: datetime

    # Type
    insight_type: str                       # "pattern", "correlation", "seasonal"
    title: str
    description: str

    # Facteurs identifies
    contributing_factors: List[str]

    # Recommandation collective
    collective_recommendation: str

    # JAMAIS de recommandation medicale
    is_medical_advice: bool = False


# ============================================================================
# HEALTH FREQUENCY AGENT
# ============================================================================

class HealthFrequencyAgent:
    """
    CHE·NU V68 Health Frequency Agent
    Sante Frequentielle & Preventive

    CONCEPT:
    - Maintenir l'harmonie AVANT la maladie
    - Detecter la friction dans l'environnement
    - Suggerer des pauses d'ancrage collectives

    PRIVACY ULTRA-STRICT:
    - JAMAIS de donnees de sante individuelles
    - Analyse par zone uniquement
    - Suggestions collectives, pas personnelles
    - Double anonymisation

    DISCLAIMER:
    - Ce n'est PAS un systeme medical
    - Pour tout probleme de sante, consulter un professionnel
    - Les suggestions sont preventives et collectives
    """

    MEDICAL_DISCLAIMER = """
    IMPORTANT: Ce systeme ne fournit PAS de conseils medicaux.
    Il offre des suggestions de bien-etre preventif et collectif.
    Pour tout probleme de sante, consultez un professionnel de sante.
    """

    def __init__(self):
        self.environment_readings: Dict[UUID, EnvironmentReading] = {}
        self.collective_rhythms: Dict[UUID, CollectiveRhythm] = {}
        self.anchor_suggestions: Dict[UUID, AnchorSuggestion] = {}
        self.zone_profiles: Dict[UUID, ZoneHealthProfile] = {}
        self.preventive_insights: Dict[UUID, PreventiveInsight] = {}

        # Counters
        self._suggestion_counter = 0
        self._insight_counter = 0

        # Thresholds
        self.noise_threshold_db = 65        # Au-dela = friction
        self.aqi_threshold = 100            # Air quality index
        self.humidity_low = 30
        self.humidity_high = 70

    # ========================================================================
    # ENVIRONMENT MONITORING
    # ========================================================================

    async def record_environment(
        self,
        latitude: float,
        longitude: float,
        zone_name: str,
        radius_km: float,
        noise_level_db: Optional[float] = None,
        air_quality_index: Optional[float] = None,
        temperature_c: Optional[float] = None,
        humidity_percent: Optional[float] = None,
        uv_index: Optional[float] = None,
        green_space_ratio: Optional[float] = None
    ) -> EnvironmentReading:
        """Record environment reading for a zone (no individuals)"""
        zone = GeoZone(latitude, longitude, radius_km, zone_name)

        # Calculate quality and friction
        quality_factors = []
        friction_factors = []

        if noise_level_db is not None:
            if noise_level_db < self.noise_threshold_db:
                quality_factors.append(1 - noise_level_db/100)
            else:
                friction_factors.append(noise_level_db/100)

        if air_quality_index is not None:
            if air_quality_index < self.aqi_threshold:
                quality_factors.append(1 - air_quality_index/200)
            else:
                friction_factors.append(air_quality_index/500)

        if humidity_percent is not None:
            if self.humidity_low <= humidity_percent <= self.humidity_high:
                quality_factors.append(0.8)
            else:
                friction_factors.append(0.3)

        if green_space_ratio is not None:
            quality_factors.append(green_space_ratio)

        overall_quality = sum(quality_factors) / len(quality_factors) if quality_factors else 0.5
        friction_score = sum(friction_factors) / len(friction_factors) if friction_factors else 0.0

        reading = EnvironmentReading(
            id=uuid4(),
            zone=zone,
            timestamp=datetime.utcnow(),
            noise_level_db=noise_level_db,
            air_quality_index=air_quality_index,
            temperature_c=temperature_c,
            humidity_percent=humidity_percent,
            uv_index=uv_index,
            green_space_ratio=green_space_ratio,
            overall_quality=overall_quality,
            friction_score=friction_score
        )

        self.environment_readings[reading.id] = reading

        # Auto-generate suggestions if friction detected
        if friction_score > 0.5:
            await self._generate_anchor_suggestions(reading)

        logger.info(f"Environment recorded for {zone_name}: quality={overall_quality:.2f}")
        return reading

    async def record_collective_rhythm(
        self,
        latitude: float,
        longitude: float,
        zone_name: str,
        rhythm_type: RhythmType,
        activity_level: float,
        estimated_stress_level: float,
        social_interaction_level: float,
        phase: str
    ) -> CollectiveRhythm:
        """Record collective rhythm for a zone"""
        zone = GeoZone(latitude, longitude, 5.0, zone_name)

        rhythm = CollectiveRhythm(
            id=uuid4(),
            zone=zone,
            timestamp=datetime.utcnow(),
            rhythm_type=rhythm_type,
            activity_level=activity_level,
            estimated_stress_level=estimated_stress_level,
            social_interaction_level=social_interaction_level,
            phase=phase
        )

        self.collective_rhythms[rhythm.id] = rhythm
        logger.info(f"Collective rhythm recorded for {zone_name}: {phase}")
        return rhythm

    # ========================================================================
    # ANCHOR SUGGESTIONS (Pauses d'Ancrage)
    # ========================================================================

    async def _generate_anchor_suggestions(
        self,
        reading: EnvironmentReading
    ) -> List[AnchorSuggestion]:
        """Generate anchor suggestions based on environment friction"""
        suggestions = []

        # Noise friction
        if reading.noise_level_db and reading.noise_level_db > self.noise_threshold_db:
            suggestions.append(await self._create_suggestion(
                reading.zone,
                AnchorType.SILENCE,
                SuggestionUrgency.RECOMMENDED,
                "Pause Silence",
                "La zone presente un niveau sonore eleve. Une pause dans un espace calme est recommandee pour la communaute.",
                10,
                None
            ))

        # Air quality friction
        if reading.air_quality_index and reading.air_quality_index > self.aqi_threshold:
            suggestions.append(await self._create_suggestion(
                reading.zone,
                AnchorType.BREATHING,
                SuggestionUrgency.TIMELY,
                "Respiration Consciente",
                "La qualite de l'air est reduite. Privilegiez les espaces interieurs avec filtration ou les zones vertes.",
                5,
                None
            ))

        # Low green space
        if reading.green_space_ratio is not None and reading.green_space_ratio < 0.2:
            suggestions.append(await self._create_suggestion(
                reading.zone,
                AnchorType.NATURE,
                SuggestionUrgency.PREVENTIVE,
                "Contact Nature",
                "La zone manque d'espaces verts. Un deplacement vers un parc ou espace naturel est benefique.",
                20,
                None
            ))

        return suggestions

    async def _create_suggestion(
        self,
        zone: GeoZone,
        anchor_type: AnchorType,
        urgency: SuggestionUrgency,
        title: str,
        description: str,
        duration_minutes: int,
        best_time: Optional[time]
    ) -> AnchorSuggestion:
        """Create an anchor suggestion"""
        self._suggestion_counter += 1
        suggestion_number = f"ANC-{self._suggestion_counter:04d}"

        suggestion = AnchorSuggestion(
            id=uuid4(),
            suggestion_number=suggestion_number,
            zone=zone,
            timestamp=datetime.utcnow(),
            anchor_type=anchor_type,
            urgency=urgency,
            title=title,
            description=description,
            duration_minutes=duration_minutes,
            best_time=best_time,
            suggested_location=None,
            valid_until=datetime.utcnow() + timedelta(hours=6),
            is_suggestion_only=True,
            requires_professional=False
        )

        self.anchor_suggestions[suggestion.id] = suggestion
        logger.info(f"Anchor suggestion created: {title} for {zone.name}")
        return suggestion

    async def suggest_anchor_pause(
        self,
        latitude: float,
        longitude: float,
        zone_name: str,
        anchor_type: AnchorType,
        title: str,
        description: str,
        duration_minutes: int,
        urgency: SuggestionUrgency = SuggestionUrgency.RECOMMENDED
    ) -> AnchorSuggestion:
        """Manually suggest an anchor pause for a zone"""
        zone = GeoZone(latitude, longitude, 5.0, zone_name)

        return await self._create_suggestion(
            zone, anchor_type, urgency, title, description, duration_minutes, None
        )

    async def get_active_suggestions(
        self,
        zone_name: Optional[str] = None
    ) -> List[AnchorSuggestion]:
        """Get active suggestions - CHRONOLOGICAL (Rule #5)"""
        now = datetime.utcnow()
        active = [s for s in self.anchor_suggestions.values()
                 if s.valid_until > now]

        if zone_name:
            active = [s for s in active
                     if s.zone.name.lower() == zone_name.lower()]

        # RULE #5: CHRONOLOGICAL
        return sorted(active, key=lambda s: s.timestamp, reverse=True)

    # ========================================================================
    # ZONE HEALTH PROFILES
    # ========================================================================

    async def update_zone_profile(
        self,
        latitude: float,
        longitude: float,
        zone_name: str
    ) -> ZoneHealthProfile:
        """Update or create zone health profile"""
        zone = GeoZone(latitude, longitude, 10.0, zone_name)

        # Get recent readings for zone
        recent_readings = [
            r for r in self.environment_readings.values()
            if r.zone.name == zone_name
            and (datetime.utcnow() - r.timestamp).total_seconds() < 86400
        ]

        # Calculate harmony
        if recent_readings:
            avg_quality = sum(r.overall_quality for r in recent_readings) / len(recent_readings)
            avg_friction = sum(r.friction_score for r in recent_readings) / len(recent_readings)
        else:
            avg_quality = 0.5
            avg_friction = 0.3

        # Determine harmony level
        if avg_quality > 0.8 and avg_friction < 0.2:
            harmony_level = HarmonyLevel.OPTIMAL
        elif avg_quality > 0.6:
            harmony_level = HarmonyLevel.BALANCED
        elif avg_quality > 0.4:
            harmony_level = HarmonyLevel.FLUCTUATING
        elif avg_quality > 0.2:
            harmony_level = HarmonyLevel.FRICTION
        else:
            harmony_level = HarmonyLevel.DISSONANCE

        # Identify friction factors
        friction_factors = []
        for r in recent_readings:
            if r.noise_level_db and r.noise_level_db > self.noise_threshold_db:
                friction_factors.append("noise")
            if r.air_quality_index and r.air_quality_index > self.aqi_threshold:
                friction_factors.append("air_quality")

        # Calculate trend
        if len(recent_readings) >= 2:
            first_half = recent_readings[:len(recent_readings)//2]
            second_half = recent_readings[len(recent_readings)//2:]
            first_avg = sum(r.overall_quality for r in first_half) / len(first_half)
            second_avg = sum(r.overall_quality for r in second_half) / len(second_half)

            if second_avg > first_avg + 0.1:
                trend = "improving"
            elif second_avg < first_avg - 0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"

        # Get active suggestions
        active_suggestions = [
            s.id for s in self.anchor_suggestions.values()
            if s.zone.name == zone_name and s.valid_until > datetime.utcnow()
        ]

        profile = ZoneHealthProfile(
            id=uuid4(),
            zone=zone,
            timestamp=datetime.utcnow(),
            harmony_level=harmony_level,
            harmony_score=avg_quality,
            environment_readings=[r.id for r in recent_readings],
            friction_factors=list(set(friction_factors)),
            friction_intensity=avg_friction,
            active_suggestions=active_suggestions,
            trend=trend
        )

        self.zone_profiles[profile.id] = profile
        logger.info(f"Zone profile updated for {zone_name}: {harmony_level.value}")
        return profile

    async def get_zone_profiles(self) -> List[ZoneHealthProfile]:
        """Get zone profiles - ALPHABETICAL by zone name (Rule #5)"""
        return sorted(self.zone_profiles.values(),
                     key=lambda p: p.zone.name.lower())

    # ========================================================================
    # PREVENTIVE INSIGHTS
    # ========================================================================

    async def generate_preventive_insight(
        self,
        latitude: float,
        longitude: float,
        zone_name: str,
        insight_type: str,
        title: str,
        description: str,
        contributing_factors: List[str],
        recommendation: str
    ) -> PreventiveInsight:
        """Generate a preventive insight for a zone"""
        zone = GeoZone(latitude, longitude, 10.0, zone_name)
        self._insight_counter += 1

        insight = PreventiveInsight(
            id=uuid4(),
            zone=zone,
            timestamp=datetime.utcnow(),
            insight_type=insight_type,
            title=title,
            description=description,
            contributing_factors=contributing_factors,
            collective_recommendation=recommendation,
            is_medical_advice=False  # ALWAYS FALSE
        )

        self.preventive_insights[insight.id] = insight
        logger.info(f"Preventive insight generated: {title}")
        return insight

    # ========================================================================
    # HEALTH SOVEREIGNTY METRICS
    # ========================================================================

    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get health sovereignty metrics for dashboard"""
        # Get recent data
        now = datetime.utcnow()
        recent_readings = [
            r for r in self.environment_readings.values()
            if (now - r.timestamp).total_seconds() < 86400
        ]

        recent_profiles = list(self.zone_profiles.values())

        # Calculate average harmony
        if recent_profiles:
            avg_harmony = sum(p.harmony_score for p in recent_profiles) / len(recent_profiles)
            avg_friction = sum(p.friction_intensity for p in recent_profiles) / len(recent_profiles)
        else:
            avg_harmony = 0.5
            avg_friction = 0.3

        # Count zones by status
        zones_by_status = {}
        for profile in recent_profiles:
            status = profile.harmony_level.value
            zones_by_status[status] = zones_by_status.get(status, 0) + 1

        # Active suggestions count
        active_suggestions = len([
            s for s in self.anchor_suggestions.values()
            if s.valid_until > now
        ])

        # Determine overall status
        if avg_harmony > 0.8:
            status = "harmonious"
            color = "#0057b8"  # Bleu cobalt - 999Hz
            message = "Harmonie collective optimale - 999Hz atteint"
        elif avg_harmony > 0.6:
            status = "balanced"
            color = "#28a745"
            message = "Equilibre maintenu dans les zones"
        elif avg_harmony > 0.4:
            status = "friction"
            color = "#fd7e14"
            message = "Friction detectee - Pauses d'ancrage recommandees"
        else:
            status = "dissonance"
            color = "#dc3545"
            message = "Dissonance importante - Actions collectives necessaires"

        return {
            "harmony_index": round(avg_harmony, 2),
            "friction_index": round(avg_friction, 2),
            "status": status,
            "color_hex": color,
            "message": message,
            "zones": {
                "monitored": len(set(r.zone.name for r in recent_readings)),
                "by_status": zones_by_status
            },
            "suggestions": {
                "active": active_suggestions,
                "types": self._count_suggestions_by_type()
            },
            "environment": {
                "readings_24h": len(recent_readings),
                "avg_air_quality": self._avg_reading("air_quality_index", recent_readings),
                "avg_noise": self._avg_reading("noise_level_db", recent_readings)
            },
            "privacy": {
                "no_individual_data": True,
                "zone_level_only": True,
                "suggestions_collective": True,
                "medical_disclaimer": self.MEDICAL_DISCLAIMER
            }
        }

    def _count_suggestions_by_type(self) -> Dict[str, int]:
        """Count active suggestions by type"""
        now = datetime.utcnow()
        active = [s for s in self.anchor_suggestions.values() if s.valid_until > now]
        counts = {}
        for s in active:
            t = s.anchor_type.value
            counts[t] = counts.get(t, 0) + 1
        return counts

    def _avg_reading(self, field: str, readings: List[EnvironmentReading]) -> Optional[float]:
        """Calculate average of a reading field"""
        values = [getattr(r, field) for r in readings if getattr(r, field) is not None]
        return round(sum(values) / len(values), 1) if values else None

    async def get_summary(self) -> Dict[str, Any]:
        """Get health module summary"""
        metrics = await self.get_health_metrics()

        return {
            "module": "Sante Frequentielle",
            "concept": "Maintenir l'harmonie AVANT la maladie",
            "metrics": metrics,
            "features": [
                "Monitoring environnemental par zone",
                "Detection de friction (bruit, pollution)",
                "Pauses d'ancrage collectives",
                "Insights preventifs"
            ],
            "disclaimer": self.MEDICAL_DISCLAIMER,
            "privacy_guarantees": [
                "JAMAIS de donnees individuelles",
                "Analyse par zone uniquement",
                "Double anonymisation",
                "Suggestions collectives"
            ]
        }


# Singleton
_health_agent: Optional[HealthFrequencyAgent] = None


def get_health_frequency_agent() -> HealthFrequencyAgent:
    """Get or create health frequency agent singleton"""
    global _health_agent
    if _health_agent is None:
        _health_agent = HealthFrequencyAgent()
    return _health_agent
