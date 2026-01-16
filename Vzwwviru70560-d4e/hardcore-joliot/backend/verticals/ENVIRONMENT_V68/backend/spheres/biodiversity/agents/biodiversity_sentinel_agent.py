"""
CHE·NU V68 Biodiversity Sentinel Agent
Module Environnement 3/4 - Sentinelles de la Biodiversite

CONCEPT: Sentinelles de la Biodiversite
- Protection des especes locales
- Surveillance des migrations (tortues, oiseaux)
- Alertes de menaces (braconnage, destruction habitat)
- Corridors ecologiques

PHILOSOPHIE:
Chaque espece est un mot dans le livre de la vie.
Perdre une espece, c'est perdre une histoire eternelle.

PRIVACY:
- Localisations sensibles anonymisees
- Pas de tracking des observateurs
- Protection des sites de nidification

GOVERNANCE COMPLIANCE:
- Rule #1: Interventions sur especes protegees require APPROVAL
- Rule #5: Especes ALPHABETICAL
- Rule #6: Full audit trail
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Tuple
from uuid import UUID, uuid4
import logging
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY HELPERS
# ============================================================================

def anonymize_location(latitude: float, longitude: float, precision: int = 2) -> str:
    """Anonymize location (lower precision for sensitive species)"""
    lat_zone = round(latitude, precision)
    lon_zone = round(longitude, precision)
    return f"bio_zone_{lat_zone}_{lon_zone}"


def anonymize_observer_id(observer_id: UUID) -> str:
    """Anonymize observer ID"""
    salt = "CHENU_BIODIVERSITY_LIFE_999Hz"
    return hashlib.sha256(f"{salt}{str(observer_id)}{salt}".encode()).hexdigest()[:16]


def protect_nesting_location(latitude: float, longitude: float) -> Tuple[float, float]:
    """
    Reduce precision for nesting/sensitive locations
    Returns coordinates with 10km precision to protect wildlife
    """
    return (round(latitude, 1), round(longitude, 1))


# ============================================================================
# ENUMS
# ============================================================================

class TaxonomicGroup(Enum):
    """Groupes taxonomiques"""
    MAMMAL = "mammal"                # Mammifere
    BIRD = "bird"                    # Oiseau
    REPTILE = "reptile"              # Reptile
    AMPHIBIAN = "amphibian"          # Amphibien
    FISH = "fish"                    # Poisson
    INVERTEBRATE = "invertebrate"    # Invertebre
    PLANT = "plant"                  # Plante
    FUNGI = "fungi"                  # Champignon
    CORAL = "coral"                  # Corail


class ConservationStatus(Enum):
    """Statut de conservation (IUCN-like)"""
    LEAST_CONCERN = "LC"             # Preoccupation mineure
    NEAR_THREATENED = "NT"           # Quasi menace
    VULNERABLE = "VU"                # Vulnerable
    ENDANGERED = "EN"                # En danger
    CRITICALLY_ENDANGERED = "CR"     # En danger critique
    EXTINCT_WILD = "EW"              # Eteint a l'etat sauvage
    EXTINCT = "EX"                   # Eteint
    DATA_DEFICIENT = "DD"            # Donnees insuffisantes


class ThreatType(Enum):
    """Types de menaces"""
    HABITAT_LOSS = "habitat_loss"         # Perte d'habitat
    POACHING = "poaching"                  # Braconnage
    POLLUTION = "pollution"                # Pollution
    CLIMATE = "climate"                    # Changement climatique
    INVASIVE_SPECIES = "invasive_species"  # Especes invasives
    DISEASE = "disease"                    # Maladie
    HUMAN_DISTURBANCE = "human_disturbance"  # Derangement humain
    OVERFISHING = "overfishing"            # Surpeche
    LIGHT_POLLUTION = "light_pollution"    # Pollution lumineuse


class MigrationType(Enum):
    """Types de migration"""
    SEDENTARY = "sedentary"          # Sedentaire
    SEASONAL = "seasonal"            # Saisonnier
    BREEDING = "breeding"            # Reproduction
    FEEDING = "feeding"              # Alimentation
    NOMADIC = "nomadic"              # Nomade


class ObservationType(Enum):
    """Types d'observation"""
    VISUAL = "visual"                # Visuelle
    ACOUSTIC = "acoustic"            # Acoustique
    TRACK = "track"                  # Traces
    CAMERA_TRAP = "camera_trap"      # Piege photographique
    TELEMETRY = "telemetry"          # Telemetrie
    DNA = "dna"                      # ADN environnemental
    NEST = "nest"                    # Nid/terrier
    REMAINS = "remains"              # Restes


class AlertPriority(Enum):
    """Priorite des alertes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"                # Requires APPROVAL
    CRITICAL = "critical"            # Requires APPROVAL


class CorridorStatus(Enum):
    """Statut du corridor ecologique"""
    INTACT = "intact"                # Intact
    FRAGMENTED = "fragmented"        # Fragmente
    DEGRADED = "degraded"            # Degrade
    BLOCKED = "blocked"              # Bloque
    RESTORED = "restored"            # Restaure


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoPoint:
    """Point geographique (precision variable selon sensibilite)"""
    latitude: float
    longitude: float
    precision: int = 3  # Decimal places

    def __post_init__(self):
        self.latitude = round(self.latitude, self.precision)
        self.longitude = round(self.longitude, self.precision)


@dataclass
class Species:
    """Espece surveillee"""
    id: UUID
    scientific_name: str
    common_name: str
    common_name_local: str  # Nom local (Maya/Espagnol)

    taxonomic_group: TaxonomicGroup
    conservation_status: ConservationStatus

    # Habitat
    habitat_types: List[str]
    migration_type: MigrationType

    # Protection
    is_protected: bool
    protection_law: str = ""  # Reference legale

    # Population
    estimated_population: Optional[int] = None
    population_trend: str = "unknown"  # increasing, stable, decreasing, unknown

    # Sensibilite
    location_sensitive: bool = False  # Si vrai, localisations masquees


@dataclass
class Observation:
    """Observation de terrain"""
    id: UUID
    species_id: UUID
    timestamp: datetime

    # Location (precision reduite si sensible)
    zone_id: str
    location: GeoPoint

    # Details
    observation_type: ObservationType
    count: int
    sex: Optional[str] = None  # male, female, unknown, mixed
    age_class: Optional[str] = None  # juvenile, adult, unknown

    # Behavior
    behavior: str = ""
    notes: str = ""

    # Nesting/breeding
    is_nesting: bool = False
    nest_status: Optional[str] = None

    # PRIVACY
    observer_anon_id: str = ""

    # Verification
    verified: bool = False
    photo_evidence: bool = False


@dataclass
class ThreatAlert:
    """Alerte de menace"""
    id: UUID
    threat_type: ThreatType
    priority: AlertPriority

    # Location
    zone_id: str
    location: GeoPoint
    radius_affected_km: float

    # Details
    title: str
    description: str
    species_affected: List[UUID]

    # Timing
    reported_at: datetime
    first_detected: Optional[datetime] = None

    # Status
    status: str = "active"  # active, investigating, mitigated, resolved

    # GOVERNANCE
    requires_approval: bool = False
    response_approved_by: Optional[str] = None
    response_approved_at: Optional[datetime] = None

    # Response
    response_actions: List[str] = field(default_factory=list)


@dataclass
class MigrationRoute:
    """Route migratoire"""
    id: UUID
    species_id: UUID
    name: str

    # Route
    waypoints: List[GeoPoint]  # Points cles (anonymises)
    total_distance_km: float

    # Timing
    start_month: int
    end_month: int
    peak_month: int

    # Status
    route_status: CorridorStatus
    threats: List[ThreatType] = field(default_factory=list)


@dataclass
class EcologicalCorridor:
    """Corridor ecologique"""
    id: UUID
    name: str

    # Geography
    start_zone: str
    end_zone: str
    length_km: float
    width_avg_m: float

    # Species
    primary_species: List[UUID]
    all_species: List[UUID]

    # Status
    status: CorridorStatus
    connectivity_score: float  # 0-1

    # Threats
    fragmentation_points: int
    barrier_types: List[str]


@dataclass
class NestingSite:
    """Site de nidification (localisation protegee)"""
    id: UUID
    species_id: UUID

    # PRIVACY: Location with reduced precision
    protected_zone_id: str
    protected_location: Tuple[float, float]  # 10km precision

    # Details
    site_type: str  # beach, tree, burrow, cliff, etc.
    capacity: int
    active: bool

    # Season
    season_start_month: int
    season_end_month: int

    # Protection
    buffer_zone_km: float
    access_restricted: bool

    # Monitoring
    last_check: Optional[datetime] = None
    current_nests: int = 0
    success_rate: float = 0.0


@dataclass
class BiodiversityMetrics:
    """Metriques de biodiversite"""
    timestamp: datetime

    # Species counts
    total_species_monitored: int
    species_threatened: int
    species_improving: int
    species_declining: int

    # Observations
    observations_this_month: int
    unique_species_observed: int

    # Threats
    active_alerts: int
    alerts_resolved: int

    # Corridors
    corridors_intact: int
    corridors_fragmented: int

    # Indices
    biodiversity_index: float      # 0-1
    habitat_connectivity: float    # 0-1
    threat_level: float            # 0-1 (higher = more threats)


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Conservation statuses requiring approval for interventions
PROTECTED_STATUSES = {
    ConservationStatus.VULNERABLE,
    ConservationStatus.ENDANGERED,
    ConservationStatus.CRITICALLY_ENDANGERED,
}

# Alert priorities requiring approval
HIGH_PRIORITY_ALERTS = {AlertPriority.URGENT, AlertPriority.CRITICAL}


# ============================================================================
# BIODIVERSITY SENTINEL AGENT
# ============================================================================

class BiodiversitySentinelAgent:
    """
    Agent Sentinelle de la Biodiversite

    Gardien de la vie:
    - Chaque espece compte
    - Les migrations sont sacrees
    - Les menaces sont combattues

    Mission: Observer, proteger, alerter
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
        self._species: Dict[UUID, Species] = {}
        self._observations: Dict[UUID, List[Observation]] = {}  # species_id -> observations
        self._alerts: Dict[UUID, ThreatAlert] = {}
        self._routes: Dict[UUID, MigrationRoute] = {}
        self._corridors: Dict[UUID, EcologicalCorridor] = {}
        self._nesting_sites: Dict[UUID, NestingSite] = {}

        # Metrics history
        self._metrics_history: List[BiodiversityMetrics] = []

        self._initialized = True
        logger.info("BiodiversitySentinelAgent initialized - Guardian of Life")

        # Initialize with some key species
        self._init_key_species()

    def _init_key_species(self) -> None:
        """Initialize monitoring for key local species"""
        key_species = [
            ("Chelonia mydas", "Green Sea Turtle", "Tortuga Verde", TaxonomicGroup.REPTILE,
             ConservationStatus.ENDANGERED, True),
            ("Caretta caretta", "Loggerhead Turtle", "Tortuga Caguama", TaxonomicGroup.REPTILE,
             ConservationStatus.VULNERABLE, True),
            ("Rhincodon typus", "Whale Shark", "Tiburon Ballena", TaxonomicGroup.FISH,
             ConservationStatus.ENDANGERED, True),
            ("Panthera onca", "Jaguar", "Balam", TaxonomicGroup.MAMMAL,
             ConservationStatus.NEAR_THREATENED, True),
            ("Amazona xantholora", "Yellow-lored Amazon", "Loro Yucateco", TaxonomicGroup.BIRD,
             ConservationStatus.LEAST_CONCERN, False),
        ]

        for sci, common, local, group, status, sensitive in key_species:
            self.register_species(
                scientific_name=sci,
                common_name=common,
                common_name_local=local,
                taxonomic_group=group,
                conservation_status=status,
                habitat_types=["coastal", "forest"],
                migration_type=MigrationType.SEASONAL,
                is_protected=status in PROTECTED_STATUSES,
                location_sensitive=sensitive,
            )

    # ========================================================================
    # SPECIES MANAGEMENT
    # ========================================================================

    def register_species(
        self,
        scientific_name: str,
        common_name: str,
        common_name_local: str,
        taxonomic_group: TaxonomicGroup,
        conservation_status: ConservationStatus,
        habitat_types: List[str],
        migration_type: MigrationType,
        is_protected: bool = False,
        protection_law: str = "",
        estimated_population: Optional[int] = None,
        population_trend: str = "unknown",
        location_sensitive: bool = False,
    ) -> Species:
        """Register a species for monitoring"""
        species_id = uuid4()

        species = Species(
            id=species_id,
            scientific_name=scientific_name,
            common_name=common_name,
            common_name_local=common_name_local,
            taxonomic_group=taxonomic_group,
            conservation_status=conservation_status,
            habitat_types=habitat_types,
            migration_type=migration_type,
            is_protected=is_protected,
            protection_law=protection_law,
            estimated_population=estimated_population,
            population_trend=population_trend,
            location_sensitive=location_sensitive,
        )

        self._species[species_id] = species
        self._observations[species_id] = []

        logger.info(f"Species registered: {scientific_name} ({conservation_status.value})")

        return species

    # ========================================================================
    # OBSERVATIONS
    # ========================================================================

    def record_observation(
        self,
        species_id: UUID,
        latitude: float,
        longitude: float,
        observation_type: ObservationType,
        count: int,
        observer_id: UUID,
        sex: Optional[str] = None,
        age_class: Optional[str] = None,
        behavior: str = "",
        notes: str = "",
        is_nesting: bool = False,
        nest_status: Optional[str] = None,
        photo_evidence: bool = False,
    ) -> Observation:
        """Record a wildlife observation"""
        if species_id not in self._species:
            raise ValueError(f"Species {species_id} not found")

        species = self._species[species_id]

        # PRIVACY: Reduce precision for sensitive species
        precision = 1 if species.location_sensitive else 3
        location = GeoPoint(latitude, longitude, precision=precision)
        zone_id = anonymize_location(latitude, longitude, precision)

        observation = Observation(
            id=uuid4(),
            species_id=species_id,
            timestamp=datetime.now(),
            zone_id=zone_id,
            location=location,
            observation_type=observation_type,
            count=count,
            sex=sex,
            age_class=age_class,
            behavior=behavior,
            notes=notes,
            is_nesting=is_nesting,
            nest_status=nest_status,
            observer_anon_id=anonymize_observer_id(observer_id),
            photo_evidence=photo_evidence,
        )

        self._observations[species_id].append(observation)

        logger.debug(
            f"Observation recorded: {species.common_name} x{count} at {zone_id}"
        )

        return observation

    # ========================================================================
    # THREAT ALERTS
    # ========================================================================

    def create_alert(
        self,
        threat_type: ThreatType,
        priority: AlertPriority,
        latitude: float,
        longitude: float,
        radius_affected_km: float,
        title: str,
        description: str,
        species_affected: List[UUID],
        first_detected: Optional[datetime] = None,
    ) -> ThreatAlert:
        """
        Create a threat alert

        GOVERNANCE: High priority alerts require approval for response
        """
        # Reduce location precision for alert
        location = GeoPoint(latitude, longitude, precision=2)
        zone_id = anonymize_location(latitude, longitude, 2)

        requires_approval = priority in HIGH_PRIORITY_ALERTS

        alert = ThreatAlert(
            id=uuid4(),
            threat_type=threat_type,
            priority=priority,
            zone_id=zone_id,
            location=location,
            radius_affected_km=radius_affected_km,
            title=title,
            description=description,
            species_affected=species_affected,
            reported_at=datetime.now(),
            first_detected=first_detected,
            requires_approval=requires_approval,
        )

        self._alerts[alert.id] = alert

        logger.warning(
            f"ALERT: {priority.value.upper()} - {title} "
            f"(zone: {zone_id}, requires_approval: {requires_approval})"
        )

        return alert

    def approve_alert_response(
        self,
        alert_id: UUID,
        approver_name: str,
        response_actions: List[str],
        approval_notes: str = "",
    ) -> ThreatAlert:
        """
        GOVERNANCE GATE: Approve response to critical alert

        RULE #1: Human approval for interventions on protected species
        """
        if alert_id not in self._alerts:
            raise ValueError(f"Alert {alert_id} not found")

        alert = self._alerts[alert_id]

        if not alert.requires_approval:
            raise ValueError("Alert does not require approval")

        alert.response_approved_by = approver_name
        alert.response_approved_at = datetime.now()
        alert.response_actions = response_actions
        alert.status = "investigating"

        logger.info(f"GOVERNANCE: Alert response approved by {approver_name}")

        return alert

    def resolve_alert(
        self,
        alert_id: UUID,
        resolution_notes: str,
        final_actions: List[str],
    ) -> ThreatAlert:
        """Mark an alert as resolved"""
        if alert_id not in self._alerts:
            raise ValueError(f"Alert {alert_id} not found")

        alert = self._alerts[alert_id]

        if alert.requires_approval and not alert.response_approved_by:
            raise ValueError("Cannot resolve without approved response")

        alert.status = "resolved"
        alert.response_actions.extend(final_actions)

        return alert

    # ========================================================================
    # MIGRATION & CORRIDORS
    # ========================================================================

    def register_migration_route(
        self,
        species_id: UUID,
        name: str,
        waypoints: List[Tuple[float, float]],
        start_month: int,
        end_month: int,
        peak_month: int,
        route_status: CorridorStatus = CorridorStatus.INTACT,
    ) -> MigrationRoute:
        """Register a migration route for monitoring"""
        if species_id not in self._species:
            raise ValueError(f"Species {species_id} not found")

        species = self._species[species_id]

        # PRIVACY: Anonymize waypoints for sensitive species
        precision = 1 if species.location_sensitive else 2
        anon_waypoints = [
            GeoPoint(lat, lon, precision=precision)
            for lat, lon in waypoints
        ]

        # Calculate distance
        total_distance = 0.0
        for i in range(len(waypoints) - 1):
            total_distance += self._haversine_distance(
                waypoints[i][0], waypoints[i][1],
                waypoints[i+1][0], waypoints[i+1][1]
            )

        route = MigrationRoute(
            id=uuid4(),
            species_id=species_id,
            name=name,
            waypoints=anon_waypoints,
            total_distance_km=total_distance,
            start_month=start_month,
            end_month=end_month,
            peak_month=peak_month,
            route_status=route_status,
        )

        self._routes[route.id] = route

        return route

    def _haversine_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float,
    ) -> float:
        """Calculate distance between two points in km"""
        import math
        R = 6371  # Earth radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat/2)**2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def register_nesting_site(
        self,
        species_id: UUID,
        latitude: float,
        longitude: float,
        site_type: str,
        capacity: int,
        season_start_month: int,
        season_end_month: int,
        buffer_zone_km: float = 0.5,
        access_restricted: bool = True,
    ) -> NestingSite:
        """
        Register a nesting site with protected location

        PRIVACY: Locations are reduced to 10km precision
        """
        if species_id not in self._species:
            raise ValueError(f"Species {species_id} not found")

        # CRITICAL: Protect nesting location
        protected_loc = protect_nesting_location(latitude, longitude)
        protected_zone = f"nest_zone_{protected_loc[0]}_{protected_loc[1]}"

        site = NestingSite(
            id=uuid4(),
            species_id=species_id,
            protected_zone_id=protected_zone,
            protected_location=protected_loc,
            site_type=site_type,
            capacity=capacity,
            active=True,
            season_start_month=season_start_month,
            season_end_month=season_end_month,
            buffer_zone_km=buffer_zone_km,
            access_restricted=access_restricted,
        )

        self._nesting_sites[site.id] = site

        logger.info(f"Nesting site registered (location protected)")

        return site

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_species(
        self,
        taxonomic_group: Optional[TaxonomicGroup] = None,
        conservation_status: Optional[ConservationStatus] = None,
        is_protected: Optional[bool] = None,
    ) -> List[Species]:
        """
        Get species with optional filters

        GOVERNANCE RULE #5: ALPHABETICAL by scientific name
        """
        species = list(self._species.values())

        if taxonomic_group:
            species = [s for s in species if s.taxonomic_group == taxonomic_group]
        if conservation_status:
            species = [s for s in species if s.conservation_status == conservation_status]
        if is_protected is not None:
            species = [s for s in species if s.is_protected == is_protected]

        # RULE #5: ALPHABETICAL order
        species.sort(key=lambda s: s.scientific_name.lower())

        return species

    def get_observations(
        self,
        species_id: Optional[UUID] = None,
        since: Optional[datetime] = None,
    ) -> List[Observation]:
        """
        Get observations

        GOVERNANCE RULE #5: Chronological order
        """
        if species_id:
            observations = self._observations.get(species_id, [])
        else:
            observations = []
            for obs_list in self._observations.values():
                observations.extend(obs_list)

        if since:
            observations = [o for o in observations if o.timestamp >= since]

        # CHRONOLOGICAL order
        observations.sort(key=lambda o: o.timestamp)

        return observations

    def get_alerts(
        self,
        status: Optional[str] = None,
        priority: Optional[AlertPriority] = None,
    ) -> List[ThreatAlert]:
        """
        Get threat alerts

        GOVERNANCE RULE #5: Chronological order
        """
        alerts = list(self._alerts.values())

        if status:
            alerts = [a for a in alerts if a.status == status]
        if priority:
            alerts = [a for a in alerts if a.priority == priority]

        # CHRONOLOGICAL order
        alerts.sort(key=lambda a: a.reported_at)

        return alerts

    def get_species_status(self, species_id: UUID) -> Dict[str, Any]:
        """Get detailed status for a species"""
        if species_id not in self._species:
            raise ValueError(f"Species {species_id} not found")

        species = self._species[species_id]
        observations = self._observations.get(species_id, [])

        # Recent observations (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent = [o for o in observations if o.timestamp >= thirty_days_ago]

        # Active alerts
        active_alerts = [
            a for a in self._alerts.values()
            if species_id in a.species_affected and a.status == "active"
        ]

        return {
            "species_id": str(species_id),
            "scientific_name": species.scientific_name,
            "common_name": species.common_name,
            "conservation_status": species.conservation_status.value,
            "is_protected": species.is_protected,
            "population_trend": species.population_trend,
            "total_observations": len(observations),
            "recent_observations": len(recent),
            "total_counted": sum(o.count for o in recent),
            "active_threats": len(active_alerts),
            "location_protected": species.location_sensitive,
        }

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_biodiversity_metrics(self) -> BiodiversityMetrics:
        """Get current biodiversity metrics"""
        now = datetime.now()
        month_ago = now - timedelta(days=30)

        # Species counts
        species = list(self._species.values())
        total = len(species)
        threatened = sum(
            1 for s in species
            if s.conservation_status in PROTECTED_STATUSES
        )
        improving = sum(
            1 for s in species
            if s.population_trend == "increasing"
        )
        declining = sum(
            1 for s in species
            if s.population_trend == "decreasing"
        )

        # Observations
        all_obs = []
        for obs_list in self._observations.values():
            all_obs.extend(obs_list)

        recent_obs = [o for o in all_obs if o.timestamp >= month_ago]
        unique_species = len(set(o.species_id for o in recent_obs))

        # Alerts
        alerts = list(self._alerts.values())
        active_alerts = sum(1 for a in alerts if a.status == "active")
        resolved_alerts = sum(1 for a in alerts if a.status == "resolved")

        # Corridors
        corridors = list(self._corridors.values())
        intact = sum(1 for c in corridors if c.status == CorridorStatus.INTACT)
        fragmented = sum(1 for c in corridors if c.status == CorridorStatus.FRAGMENTED)

        # Calculate indices

        # Biodiversity index (0-1)
        # Based on species richness, observations, trends
        if total > 0:
            species_factor = min(total / 100, 1.0)
            health_factor = (total - threatened) / total
            trend_factor = (improving + (total - declining - improving) * 0.5) / total
            biodiversity_index = (species_factor + health_factor + trend_factor) / 3
        else:
            biodiversity_index = 0

        # Habitat connectivity (0-1)
        if corridors:
            connectivity = intact / len(corridors)
        else:
            connectivity = 0.5  # Unknown

        # Threat level (0-1, higher = worse)
        threat_level = min(active_alerts / max(total, 1), 1.0)

        metrics = BiodiversityMetrics(
            timestamp=now,
            total_species_monitored=total,
            species_threatened=threatened,
            species_improving=improving,
            species_declining=declining,
            observations_this_month=len(recent_obs),
            unique_species_observed=unique_species,
            active_alerts=active_alerts,
            alerts_resolved=resolved_alerts,
            corridors_intact=intact,
            corridors_fragmented=fragmented,
            biodiversity_index=biodiversity_index,
            habitat_connectivity=connectivity,
            threat_level=threat_level,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_biodiversity_indices(self) -> Dict[str, float]:
        """Get biodiversity indices for dashboard"""
        metrics = self.get_biodiversity_metrics()

        return {
            "biodiversity_index": round(metrics.biodiversity_index, 3),
            "habitat_connectivity": round(metrics.habitat_connectivity, 3),
            "threat_level": round(metrics.threat_level, 3),
            "species_health": round(
                (metrics.total_species_monitored - metrics.species_threatened) /
                max(metrics.total_species_monitored, 1),
                3
            ),
            "monitoring_coverage": round(
                metrics.unique_species_observed / max(metrics.total_species_monitored, 1),
                3
            ),
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_biodiversity_sentinel_agent() -> BiodiversitySentinelAgent:
    """Get the singleton BiodiversitySentinelAgent instance"""
    return BiodiversitySentinelAgent()
