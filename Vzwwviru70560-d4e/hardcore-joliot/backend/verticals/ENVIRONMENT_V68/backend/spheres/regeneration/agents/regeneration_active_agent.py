"""
CHE·NU V68 Regeneration Active Agent
Module Environnement 1/4 - Cycles de Sol et d'Eau

CONCEPT: Regeneration Active
- Surveillance des cycles naturels (sol, eau, air)
- Cenotes comme points d'ancrage sacres
- Restauration des ecosystemes degrades
- Permaculture et agriculture regenerative

PHILOSOPHIE:
La terre n'appartient pas a l'homme - l'homme appartient a la terre.
Notre role: observer, proteger, regenerer.

PRIVACY:
- Donnees de localisation anonymisees
- Pas de tracking des proprietaires
- Focus sur les zones, pas les individus

GOVERNANCE COMPLIANCE:
- Rule #1: Interventions majeurs require APPROVAL
- Rule #5: Sites ALPHABETICAL by name
- Rule #6: Full audit trail
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set
from uuid import UUID, uuid4
import logging
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY HELPERS
# ============================================================================

def anonymize_location(latitude: float, longitude: float) -> str:
    """Anonymize location to zone (~1km precision for environmental)"""
    lat_zone = round(latitude, 2)
    lon_zone = round(longitude, 2)
    return f"eco_zone_{lat_zone}_{lon_zone}"


def anonymize_contributor_id(contributor_id: UUID) -> str:
    """Anonymize contributor ID"""
    salt = "CHENU_REGENERATION_EARTH_999Hz"
    return hashlib.sha256(f"{salt}{str(contributor_id)}{salt}".encode()).hexdigest()[:16]


# ============================================================================
# ENUMS
# ============================================================================

class EcosystemType(Enum):
    """Types d'ecosystemes"""
    CENOTE = "cenote"                # Cenote sacre
    MANGROVE = "mangrove"            # Mangrove
    FOREST = "forest"                # Foret
    WETLAND = "wetland"              # Zone humide
    COASTAL = "coastal"              # Littoral
    AGRICULTURAL = "agricultural"    # Zone agricole
    URBAN_GREEN = "urban_green"      # Espace vert urbain
    REEF = "reef"                    # Recif corallien
    RIVER = "river"                  # Riviere/ruisseau
    CAVE = "cave"                    # Grotte/caverne


class SoilHealth(Enum):
    """Sante du sol"""
    CRITICAL = "critical"            # Degradation severe
    POOR = "poor"                    # Faible qualite
    MODERATE = "moderate"            # Qualite moyenne
    GOOD = "good"                    # Bonne qualite
    EXCELLENT = "excellent"          # Sol regenere/optimal
    PRISTINE = "pristine"            # Sol vierge intact


class WaterQuality(Enum):
    """Qualite de l'eau"""
    CONTAMINATED = "contaminated"    # Contamine
    POOR = "poor"                    # Mauvaise qualite
    FAIR = "fair"                    # Qualite acceptable
    GOOD = "good"                    # Bonne qualite
    EXCELLENT = "excellent"          # Excellente qualite
    PRISTINE = "pristine"            # Eau pure


class RegenerationStatus(Enum):
    """Statut de regeneration"""
    DEGRADED = "degraded"            # Degrade
    STABILIZING = "stabilizing"      # En stabilisation
    RECOVERING = "recovering"        # En recuperation
    REGENERATING = "regenerating"    # En regeneration active
    THRIVING = "thriving"            # Prospere
    PROTECTED = "protected"          # Protege


class InterventionType(Enum):
    """Types d'interventions"""
    MONITORING = "monitoring"        # Surveillance
    PLANTING = "planting"            # Plantation
    CLEANUP = "cleanup"              # Nettoyage
    RESTORATION = "restoration"      # Restauration
    PROTECTION = "protection"        # Protection
    PERMACULTURE = "permaculture"    # Permaculture
    WATER_MANAGEMENT = "water_management"  # Gestion de l'eau
    SOIL_AMENDMENT = "soil_amendment"      # Amendement du sol


class InterventionPriority(Enum):
    """Priorite d'intervention"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"                # Requires APPROVAL
    CRITICAL = "critical"            # Requires APPROVAL


class CyclePhase(Enum):
    """Phase du cycle naturel"""
    DORMANT = "dormant"              # Dormance
    AWAKENING = "awakening"          # Reveil
    GROWTH = "growth"                # Croissance
    PEAK = "peak"                    # Apogee
    HARVEST = "harvest"              # Recolte
    DECLINE = "decline"              # Declin
    REST = "rest"                    # Repos


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoPoint:
    """Point geographique (precision reduite)"""
    latitude: float
    longitude: float
    altitude_m: Optional[float] = None

    def __post_init__(self):
        # PRIVACY: Reduce precision for privacy
        self.latitude = round(self.latitude, 3)
        self.longitude = round(self.longitude, 3)


@dataclass
class SoilReading:
    """Lecture des parametres du sol"""
    id: UUID
    zone_id: str
    timestamp: datetime

    # Parametres
    ph: float
    moisture_pct: float
    organic_matter_pct: float
    nitrogen_ppm: float
    phosphorus_ppm: float
    potassium_ppm: float

    # Assessment
    health: SoilHealth
    notes: str = ""


@dataclass
class WaterReading:
    """Lecture des parametres de l'eau"""
    id: UUID
    zone_id: str
    timestamp: datetime

    # Parametres
    ph: float
    dissolved_oxygen_ppm: float
    turbidity_ntu: float
    temperature_c: float
    conductivity_us: float

    # Contamination markers
    nitrates_ppm: float = 0.0
    phosphates_ppm: float = 0.0
    bacteria_cfu: int = 0

    # Assessment
    quality: WaterQuality
    potable: bool = False
    notes: str = ""


@dataclass
class EcoSite:
    """Site ecologique"""
    id: UUID
    name: str
    ecosystem_type: EcosystemType
    location: GeoPoint
    zone_id: str

    # Physical
    area_hectares: Decimal
    elevation_m: float

    # Status
    status: RegenerationStatus
    soil_health: SoilHealth
    water_quality: Optional[WaterQuality] = None

    # Current cycle
    cycle_phase: CyclePhase = CyclePhase.DORMANT

    # Protection
    is_protected: bool = False
    protection_level: str = ""

    # Timestamps
    registered_at: datetime = field(default_factory=datetime.now)
    last_assessment: Optional[datetime] = None

    # Audit
    audit_log: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Intervention:
    """Intervention de regeneration"""
    id: UUID
    site_id: UUID
    intervention_type: InterventionType
    priority: InterventionPriority

    # Details
    title: str
    description: str
    objectives: List[str]
    methods: List[str]

    # Resources
    volunteers_needed: int
    materials_needed: List[str]
    estimated_cost: Decimal

    # Timeline
    proposed_date: datetime
    duration_days: int

    # Status
    status: str = "proposed"  # proposed, pending_approval, approved, in_progress, completed
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    # PRIVACY
    proposer_anon_id: str = ""

    # Results
    outcomes: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)


@dataclass
class CenoteProfile:
    """Profil special pour les cenotes (sites sacres)"""
    id: UUID
    site_id: UUID
    name: str

    # Classification
    cenote_type: str  # abierto, semiabierto, subterraneo
    depth_m: float
    water_area_m2: float

    # Sacredness
    cultural_significance: str
    access_restricted: bool
    ceremonial_use: bool

    # Health
    water_quality: WaterQuality
    biodiversity_index: float  # 0-1

    # Threats
    threats: List[str] = field(default_factory=list)
    protection_measures: List[str] = field(default_factory=list)


@dataclass
class RegenerationMetrics:
    """Metriques de regeneration"""
    timestamp: datetime

    # Coverage
    total_sites: int
    sites_protected: int
    sites_degraded: int
    sites_regenerating: int

    # Soil
    avg_soil_health: float  # 0-5 scale
    soil_improving: int
    soil_declining: int

    # Water
    avg_water_quality: float  # 0-5 scale
    water_improving: int
    water_declining: int

    # Activity
    active_interventions: int
    completed_interventions: int
    volunteer_hours: int

    # Indices
    regeneration_index: float  # 0-1, overall health
    biodiversity_trend: float  # -1 to +1, direction


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Priority levels requiring human approval
HIGH_PRIORITY_INTERVENTIONS = {InterventionPriority.URGENT, InterventionPriority.CRITICAL}

# Cost threshold requiring approval
COST_APPROVAL_THRESHOLD = Decimal("5000")

# Protected site intervention always requires approval
PROTECTED_SITE_APPROVAL = True


# ============================================================================
# REGENERATION ACTIVE AGENT
# ============================================================================

class RegenerationActiveAgent:
    """
    Agent de Regeneration Active

    Surveille et protege les cycles naturels:
    - Sol: la peau de la terre
    - Eau: le sang de la terre
    - Cenotes: les yeux de la terre

    Notre mission: observer, proteger, regenerer
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

        # Storage
        self._sites: Dict[UUID, EcoSite] = {}
        self._cenotes: Dict[UUID, CenoteProfile] = {}
        self._interventions: Dict[UUID, Intervention] = {}
        self._soil_readings: Dict[str, List[SoilReading]] = {}  # zone_id -> readings
        self._water_readings: Dict[str, List[WaterReading]] = {}  # zone_id -> readings

        # Metrics history
        self._metrics_history: List[RegenerationMetrics] = []

        self._initialized = True
        logger.info("RegenerationActiveAgent initialized - Guardian of Earth Cycles")

    # ========================================================================
    # SITE MANAGEMENT
    # ========================================================================

    def register_site(
        self,
        name: str,
        ecosystem_type: EcosystemType,
        latitude: float,
        longitude: float,
        area_hectares: Decimal,
        elevation_m: float,
        initial_status: RegenerationStatus = RegenerationStatus.DEGRADED,
        initial_soil_health: SoilHealth = SoilHealth.MODERATE,
        water_quality: Optional[WaterQuality] = None,
        is_protected: bool = False,
        protection_level: str = "",
    ) -> EcoSite:
        """Register a new ecological site for monitoring"""
        site_id = uuid4()
        zone_id = anonymize_location(latitude, longitude)

        site = EcoSite(
            id=site_id,
            name=name,
            ecosystem_type=ecosystem_type,
            location=GeoPoint(latitude, longitude),
            zone_id=zone_id,
            area_hectares=area_hectares,
            elevation_m=elevation_m,
            status=initial_status,
            soil_health=initial_soil_health,
            water_quality=water_quality,
            is_protected=is_protected,
            protection_level=protection_level,
            audit_log=[{
                "action": "registered",
                "timestamp": datetime.now().isoformat(),
            }],
        )

        self._sites[site_id] = site

        logger.info(f"Site registered: {name} ({ecosystem_type.value})")

        return site

    def register_cenote(
        self,
        site_id: UUID,
        name: str,
        cenote_type: str,
        depth_m: float,
        water_area_m2: float,
        cultural_significance: str,
        access_restricted: bool = True,
        ceremonial_use: bool = False,
        water_quality: WaterQuality = WaterQuality.GOOD,
        biodiversity_index: float = 0.5,
    ) -> CenoteProfile:
        """Register a cenote as a sacred site"""
        if site_id not in self._sites:
            raise ValueError(f"Site {site_id} not found")

        cenote = CenoteProfile(
            id=uuid4(),
            site_id=site_id,
            name=name,
            cenote_type=cenote_type,
            depth_m=depth_m,
            water_area_m2=water_area_m2,
            cultural_significance=cultural_significance,
            access_restricted=access_restricted,
            ceremonial_use=ceremonial_use,
            water_quality=water_quality,
            biodiversity_index=biodiversity_index,
        )

        self._cenotes[cenote.id] = cenote

        # Mark site as protected
        site = self._sites[site_id]
        site.is_protected = True
        site.protection_level = "CENOTE_SAGRADO"

        logger.info(f"Cenote registered: {name} (sacred site)")

        return cenote

    # ========================================================================
    # READINGS & MONITORING
    # ========================================================================

    def record_soil_reading(
        self,
        site_id: UUID,
        ph: float,
        moisture_pct: float,
        organic_matter_pct: float,
        nitrogen_ppm: float,
        phosphorus_ppm: float,
        potassium_ppm: float,
        notes: str = "",
    ) -> SoilReading:
        """Record a soil health reading"""
        if site_id not in self._sites:
            raise ValueError(f"Site {site_id} not found")

        site = self._sites[site_id]

        # Assess soil health based on parameters
        health = self._assess_soil_health(
            ph, moisture_pct, organic_matter_pct,
            nitrogen_ppm, phosphorus_ppm, potassium_ppm
        )

        reading = SoilReading(
            id=uuid4(),
            zone_id=site.zone_id,
            timestamp=datetime.now(),
            ph=ph,
            moisture_pct=moisture_pct,
            organic_matter_pct=organic_matter_pct,
            nitrogen_ppm=nitrogen_ppm,
            phosphorus_ppm=phosphorus_ppm,
            potassium_ppm=potassium_ppm,
            health=health,
            notes=notes,
        )

        if site.zone_id not in self._soil_readings:
            self._soil_readings[site.zone_id] = []
        self._soil_readings[site.zone_id].append(reading)

        # Update site
        site.soil_health = health
        site.last_assessment = reading.timestamp

        return reading

    def _assess_soil_health(
        self,
        ph: float,
        moisture: float,
        organic_matter: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
    ) -> SoilHealth:
        """Assess soil health from parameters"""
        score = 0

        # pH (ideal 6.0-7.0)
        if 6.0 <= ph <= 7.0:
            score += 2
        elif 5.5 <= ph <= 7.5:
            score += 1

        # Organic matter (higher is better)
        if organic_matter > 5.0:
            score += 2
        elif organic_matter > 3.0:
            score += 1

        # NPK balance
        if nitrogen > 20 and phosphorus > 15 and potassium > 100:
            score += 2
        elif nitrogen > 10 and phosphorus > 10 and potassium > 50:
            score += 1

        # Moisture (ideal 20-60%)
        if 20 <= moisture <= 60:
            score += 1

        if score >= 6:
            return SoilHealth.EXCELLENT
        elif score >= 4:
            return SoilHealth.GOOD
        elif score >= 2:
            return SoilHealth.MODERATE
        elif score >= 1:
            return SoilHealth.POOR
        else:
            return SoilHealth.CRITICAL

    def record_water_reading(
        self,
        site_id: UUID,
        ph: float,
        dissolved_oxygen_ppm: float,
        turbidity_ntu: float,
        temperature_c: float,
        conductivity_us: float,
        nitrates_ppm: float = 0.0,
        phosphates_ppm: float = 0.0,
        bacteria_cfu: int = 0,
        notes: str = "",
    ) -> WaterReading:
        """Record a water quality reading"""
        if site_id not in self._sites:
            raise ValueError(f"Site {site_id} not found")

        site = self._sites[site_id]

        # Assess water quality
        quality = self._assess_water_quality(
            ph, dissolved_oxygen_ppm, turbidity_ntu,
            nitrates_ppm, phosphates_ppm, bacteria_cfu
        )

        # Check if potable
        potable = (
            quality in {WaterQuality.EXCELLENT, WaterQuality.PRISTINE}
            and bacteria_cfu < 100
            and nitrates_ppm < 10
        )

        reading = WaterReading(
            id=uuid4(),
            zone_id=site.zone_id,
            timestamp=datetime.now(),
            ph=ph,
            dissolved_oxygen_ppm=dissolved_oxygen_ppm,
            turbidity_ntu=turbidity_ntu,
            temperature_c=temperature_c,
            conductivity_us=conductivity_us,
            nitrates_ppm=nitrates_ppm,
            phosphates_ppm=phosphates_ppm,
            bacteria_cfu=bacteria_cfu,
            quality=quality,
            potable=potable,
            notes=notes,
        )

        if site.zone_id not in self._water_readings:
            self._water_readings[site.zone_id] = []
        self._water_readings[site.zone_id].append(reading)

        # Update site
        site.water_quality = quality
        site.last_assessment = reading.timestamp

        return reading

    def _assess_water_quality(
        self,
        ph: float,
        dissolved_oxygen: float,
        turbidity: float,
        nitrates: float,
        phosphates: float,
        bacteria: int,
    ) -> WaterQuality:
        """Assess water quality from parameters"""
        score = 0

        # pH (ideal 6.5-8.5)
        if 6.5 <= ph <= 8.5:
            score += 2
        elif 6.0 <= ph <= 9.0:
            score += 1

        # Dissolved oxygen (higher is better, >6 excellent)
        if dissolved_oxygen > 8:
            score += 2
        elif dissolved_oxygen > 6:
            score += 1

        # Turbidity (lower is better)
        if turbidity < 5:
            score += 2
        elif turbidity < 10:
            score += 1

        # Contamination (lower is better)
        if nitrates < 10 and phosphates < 0.1 and bacteria < 100:
            score += 2
        elif nitrates < 25 and phosphates < 0.5 and bacteria < 500:
            score += 1

        if score >= 7:
            return WaterQuality.PRISTINE
        elif score >= 5:
            return WaterQuality.EXCELLENT
        elif score >= 4:
            return WaterQuality.GOOD
        elif score >= 2:
            return WaterQuality.FAIR
        elif score >= 1:
            return WaterQuality.POOR
        else:
            return WaterQuality.CONTAMINATED

    # ========================================================================
    # INTERVENTIONS
    # ========================================================================

    def propose_intervention(
        self,
        site_id: UUID,
        intervention_type: InterventionType,
        priority: InterventionPriority,
        title: str,
        description: str,
        objectives: List[str],
        methods: List[str],
        volunteers_needed: int,
        materials_needed: List[str],
        estimated_cost: Decimal,
        proposed_date: datetime,
        duration_days: int,
        proposer_id: UUID,
    ) -> Intervention:
        """
        Propose an intervention

        GOVERNANCE: High priority or costly interventions require approval
        """
        if site_id not in self._sites:
            raise ValueError(f"Site {site_id} not found")

        site = self._sites[site_id]

        # Determine if approval required
        requires_approval = (
            priority in HIGH_PRIORITY_INTERVENTIONS
            or estimated_cost > COST_APPROVAL_THRESHOLD
            or (site.is_protected and PROTECTED_SITE_APPROVAL)
        )

        status = "pending_approval" if requires_approval else "proposed"

        intervention = Intervention(
            id=uuid4(),
            site_id=site_id,
            intervention_type=intervention_type,
            priority=priority,
            title=title,
            description=description,
            objectives=objectives,
            methods=methods,
            volunteers_needed=volunteers_needed,
            materials_needed=materials_needed,
            estimated_cost=estimated_cost,
            proposed_date=proposed_date,
            duration_days=duration_days,
            status=status,
            proposer_anon_id=anonymize_contributor_id(proposer_id),
        )

        self._interventions[intervention.id] = intervention

        logger.info(
            f"Intervention proposed: {title} ({intervention_type.value}) - "
            f"status: {status}"
        )

        return intervention

    def approve_intervention(
        self,
        intervention_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> Intervention:
        """
        GOVERNANCE GATE: Approve an intervention

        RULE #1: Human approval for significant interventions
        """
        if intervention_id not in self._interventions:
            raise ValueError(f"Intervention {intervention_id} not found")

        intervention = self._interventions[intervention_id]

        if intervention.status != "pending_approval":
            raise ValueError(f"Intervention not pending approval (status: {intervention.status})")

        intervention.status = "approved"
        intervention.approved_by = approver_name
        intervention.approved_at = datetime.now()

        # Update site audit
        site = self._sites[intervention.site_id]
        site.audit_log.append({
            "action": "intervention_approved",
            "intervention_id": str(intervention_id),
            "timestamp": datetime.now().isoformat(),
            "by": approver_name,
            "notes": approval_notes,
        })

        logger.info(f"GOVERNANCE: Intervention {intervention_id} approved by {approver_name}")

        return intervention

    def complete_intervention(
        self,
        intervention_id: UUID,
        outcomes: List[str],
        lessons_learned: List[str],
    ) -> Intervention:
        """Record completion of an intervention"""
        if intervention_id not in self._interventions:
            raise ValueError(f"Intervention {intervention_id} not found")

        intervention = self._interventions[intervention_id]

        if intervention.status not in {"approved", "in_progress"}:
            raise ValueError(f"Cannot complete intervention (status: {intervention.status})")

        intervention.status = "completed"
        intervention.outcomes = outcomes
        intervention.lessons_learned = lessons_learned

        # Update site status
        site = self._sites[intervention.site_id]
        site.audit_log.append({
            "action": "intervention_completed",
            "intervention_id": str(intervention_id),
            "timestamp": datetime.now().isoformat(),
            "outcomes": outcomes,
        })

        # Potentially improve site status
        if intervention.intervention_type in {
            InterventionType.RESTORATION,
            InterventionType.PERMACULTURE,
            InterventionType.PLANTING,
        }:
            self._improve_site_status(site)

        return intervention

    def _improve_site_status(self, site: EcoSite) -> None:
        """Potentially improve site status after positive intervention"""
        status_progression = [
            RegenerationStatus.DEGRADED,
            RegenerationStatus.STABILIZING,
            RegenerationStatus.RECOVERING,
            RegenerationStatus.REGENERATING,
            RegenerationStatus.THRIVING,
        ]

        current_idx = status_progression.index(site.status) if site.status in status_progression else 0
        if current_idx < len(status_progression) - 1:
            site.status = status_progression[current_idx + 1]

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_sites(
        self,
        ecosystem_type: Optional[EcosystemType] = None,
        status: Optional[RegenerationStatus] = None,
        is_protected: Optional[bool] = None,
    ) -> List[EcoSite]:
        """
        Get sites with optional filters

        GOVERNANCE RULE #5: Return in ALPHABETICAL order by name
        """
        sites = list(self._sites.values())

        if ecosystem_type:
            sites = [s for s in sites if s.ecosystem_type == ecosystem_type]
        if status:
            sites = [s for s in sites if s.status == status]
        if is_protected is not None:
            sites = [s for s in sites if s.is_protected == is_protected]

        # RULE #5: ALPHABETICAL order
        sites.sort(key=lambda s: s.name.lower())

        return sites

    def get_cenotes(self) -> List[CenoteProfile]:
        """
        Get all registered cenotes

        GOVERNANCE RULE #5: Alphabetical order
        """
        cenotes = list(self._cenotes.values())
        cenotes.sort(key=lambda c: c.name.lower())
        return cenotes

    def get_interventions(
        self,
        site_id: Optional[UUID] = None,
        status: Optional[str] = None,
        intervention_type: Optional[InterventionType] = None,
    ) -> List[Intervention]:
        """
        Get interventions with optional filters

        GOVERNANCE RULE #5: Chronological order
        """
        interventions = list(self._interventions.values())

        if site_id:
            interventions = [i for i in interventions if i.site_id == site_id]
        if status:
            interventions = [i for i in interventions if i.status == status]
        if intervention_type:
            interventions = [i for i in interventions if i.intervention_type == intervention_type]

        # CHRONOLOGICAL order
        interventions.sort(key=lambda i: i.proposed_date)

        return interventions

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_regeneration_metrics(self) -> RegenerationMetrics:
        """Get current regeneration metrics"""
        now = datetime.now()

        # Site counts
        sites = list(self._sites.values())
        total_sites = len(sites)
        sites_protected = sum(1 for s in sites if s.is_protected)
        sites_degraded = sum(1 for s in sites if s.status == RegenerationStatus.DEGRADED)
        sites_regenerating = sum(
            1 for s in sites
            if s.status in {RegenerationStatus.RECOVERING, RegenerationStatus.REGENERATING}
        )

        # Soil health average
        soil_scores = {
            SoilHealth.CRITICAL: 1,
            SoilHealth.POOR: 2,
            SoilHealth.MODERATE: 3,
            SoilHealth.GOOD: 4,
            SoilHealth.EXCELLENT: 5,
            SoilHealth.PRISTINE: 5,
        }
        if sites:
            avg_soil = sum(soil_scores.get(s.soil_health, 3) for s in sites) / len(sites)
        else:
            avg_soil = 0

        # Water quality average
        water_scores = {
            WaterQuality.CONTAMINATED: 1,
            WaterQuality.POOR: 2,
            WaterQuality.FAIR: 3,
            WaterQuality.GOOD: 4,
            WaterQuality.EXCELLENT: 5,
            WaterQuality.PRISTINE: 5,
        }
        sites_with_water = [s for s in sites if s.water_quality]
        if sites_with_water:
            avg_water = sum(water_scores.get(s.water_quality, 3) for s in sites_with_water) / len(sites_with_water)
        else:
            avg_water = 0

        # Intervention counts
        interventions = list(self._interventions.values())
        active = sum(1 for i in interventions if i.status in {"approved", "in_progress"})
        completed = sum(1 for i in interventions if i.status == "completed")

        # Calculate regeneration index (0-1)
        if total_sites > 0:
            health_factor = (avg_soil + avg_water) / 10  # Normalize to 0-1
            status_factor = (
                (sites_regenerating + sum(1 for s in sites if s.status == RegenerationStatus.THRIVING))
                / total_sites
            )
            protection_factor = sites_protected / total_sites
            regeneration_index = (health_factor + status_factor + protection_factor) / 3
        else:
            regeneration_index = 0

        metrics = RegenerationMetrics(
            timestamp=now,
            total_sites=total_sites,
            sites_protected=sites_protected,
            sites_degraded=sites_degraded,
            sites_regenerating=sites_regenerating,
            avg_soil_health=avg_soil,
            soil_improving=0,  # Would need historical data
            soil_declining=0,
            avg_water_quality=avg_water,
            water_improving=0,
            water_declining=0,
            active_interventions=active,
            completed_interventions=completed,
            volunteer_hours=completed * 8,  # Estimate
            regeneration_index=regeneration_index,
            biodiversity_trend=0.0,  # Would need biodiversity data
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_environmental_indices(self) -> Dict[str, float]:
        """Get environmental indices for dashboard"""
        metrics = self.get_regeneration_metrics()

        return {
            "regeneration_index": round(metrics.regeneration_index, 3),
            "soil_health_avg": round(metrics.avg_soil_health / 5, 3),  # Normalize to 0-1
            "water_quality_avg": round(metrics.avg_water_quality / 5, 3),
            "protection_coverage": round(
                metrics.sites_protected / max(metrics.total_sites, 1), 3
            ),
            "active_restoration": round(
                metrics.sites_regenerating / max(metrics.total_sites, 1), 3
            ),
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_regeneration_active_agent() -> RegenerationActiveAgent:
    """Get the singleton RegenerationActiveAgent instance"""
    return RegenerationActiveAgent()
