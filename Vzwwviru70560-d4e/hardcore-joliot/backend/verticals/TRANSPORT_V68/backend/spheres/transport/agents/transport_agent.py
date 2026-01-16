"""
CHE·NU V68 Transport & Logistics Agent (AT·OM Flow)
Vertical 16/17 - Intelligent Transport Management

CONCEPT: Le transport comme un reseau neuronal
- Chaque vehicule est un neurone
- Chaque trajet est une synapse
- L'intelligence collective optimise le flux

GOVERNANCE COMPLIANCE:
- Rule #1: Dispatch decisions require APPROVAL for high-value loads
- Rule #1: Sous-traitance contracts require APPROVAL
- Rule #5: Vehicles ALPHABETICAL (not by efficiency score)
- Rule #5: Routes CHRONOLOGICAL (not by profitability)
- Rule #5: Drivers ALPHABETICAL (NOT by rating/performance)
- Rule #6: Full audit trail (UUID, timestamps, created_by)

MODES:
- Commercial: Livraisons B2B, marchandises
- Industrial: Transport lourd, materiaux, equipements
- Personal: Covoiturage, trajets partages
- Sous-traitance: Integration Uber, Taxi, partenaires

Competing with: Samsara ($500/mo), KeepTruckin ($400/mo), Fleet Complete ($300/mo)
CHE·NU pricing: $29/mo with governance differentiators
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID, uuid4
import logging
import math

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class VehicleType(Enum):
    """Type de vehicule"""
    CAMION = "camion"           # Poids lourd
    CAMIONNETTE = "camionnette"  # Utilitaire
    FOURGON = "fourgon"         # Livraison
    VOITURE = "voiture"         # Personnel/covoiturage
    MOTO = "moto"               # Livraison rapide
    VELO_CARGO = "velo_cargo"   # Derniere mile ecologique
    REMORQUE = "remorque"       # Equipement additionnel


class VehicleStatus(Enum):
    """Statut du vehicule"""
    AVAILABLE = "available"          # Disponible
    IN_TRANSIT = "in_transit"        # En route
    LOADING = "loading"              # Chargement
    UNLOADING = "unloading"          # Dechargement
    MAINTENANCE = "maintenance"       # Entretien
    OUT_OF_SERVICE = "out_of_service" # Hors service
    RESERVED = "reserved"            # Reserve


class TripType(Enum):
    """Type de trajet"""
    RECURRENT = "recurrent"    # Trajet regulier (quotidien, hebdo)
    TEMPORARY = "temporary"    # Trajet ponctuel
    ON_DEMAND = "on_demand"    # A la demande
    COVOITURAGE = "covoiturage" # Partage de trajet
    POOLING = "pooling"        # Mutualisation marchandises


class TripStatus(Enum):
    """Statut du trajet"""
    PLANNED = "planned"             # Planifie
    CONFIRMED = "confirmed"         # Confirme
    IN_PROGRESS = "in_progress"     # En cours
    COMPLETED = "completed"         # Termine
    CANCELLED = "cancelled"         # Annule
    DELAYED = "delayed"             # Retarde


class DispatchMode(Enum):
    """Mode de dispatch"""
    DIRECT = "direct"               # Attribution directe
    COLLABORATIVE = "collaborative"  # Intelligence collective
    AUCTION = "auction"             # Mise aux encheres
    ROUND_ROBIN = "round_robin"     # Rotation equitable


class SoustraitanceType(Enum):
    """Type de sous-traitance"""
    UBER = "uber"
    TAXI = "taxi"
    BOLT = "bolt"
    PARTNER = "partner"      # Partenaire local
    FREELANCE = "freelance"  # Chauffeur independant


class SoustraitanceStatus(Enum):
    """Statut de sous-traitance"""
    PENDING = "pending"
    PENDING_APPROVAL = "pending_approval"  # GOVERNANCE Rule #1
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LoadType(Enum):
    """Type de chargement"""
    PACKAGE = "package"          # Colis
    PALLET = "pallet"            # Palette
    BULK = "bulk"                # Vrac
    CONTAINER = "container"      # Conteneur
    PASSENGER = "passenger"      # Passager
    MIXED = "mixed"              # Mixte


class ZoneType(Enum):
    """Type de zone Che-Nu"""
    HUB = "hub"                      # Hub de transit
    TRANSIT = "transit"              # Zone de passage
    HIGH_FRICTION = "high_friction"  # Zone a eviter (centre-ville)
    LOW_FRICTION = "low_friction"    # Zone fluide
    PICKUP = "pickup"                # Point de collecte
    DROPOFF = "dropoff"              # Point de livraison


class OptimizationGoal(Enum):
    """Objectif d'optimisation"""
    FILL_RATE = "fill_rate"          # Maximiser remplissage
    TIME = "time"                     # Minimiser temps
    COST = "cost"                     # Minimiser cout
    EMISSIONS = "emissions"           # Minimiser emissions
    BALANCED = "balanced"             # Equilibre


class FlowStatus(Enum):
    """Statut du flux (visualisation)"""
    FLUID = "fluid"           # Bleu cobalt - 999Hz
    NORMAL = "normal"         # Vert
    CONGESTED = "congested"   # Orange
    BLOCKED = "blocked"       # Rouge


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoPoint:
    """Point geographique"""
    latitude: float
    longitude: float
    address: Optional[str] = None
    name: Optional[str] = None

    def distance_to(self, other: 'GeoPoint') -> float:
        """Calculate distance in km using Haversine formula"""
        R = 6371  # Earth's radius in km
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c


@dataclass
class Vehicle:
    """Vehicule de transport"""
    id: UUID
    registration: str        # Plaque d'immatriculation
    name: str               # Nom/identifiant interne
    vehicle_type: VehicleType
    status: VehicleStatus

    # Capacite
    capacity_kg: float
    capacity_m3: float
    current_load_kg: float
    current_load_m3: float

    # Localisation
    current_location: Optional[GeoPoint]
    destination: Optional[GeoPoint]

    # Chauffeur
    driver_id: Optional[UUID]
    driver_name: Optional[str]

    # Couts
    cost_per_km: Decimal
    fuel_type: str          # diesel, essence, electric, hybrid
    emissions_g_per_km: float

    # Audit
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    @property
    def fill_rate(self) -> float:
        """Taux de remplissage (0-100%)"""
        if self.capacity_kg <= 0:
            return 0.0
        return min(100.0, (self.current_load_kg / self.capacity_kg) * 100)

    @property
    def available_capacity_kg(self) -> float:
        """Capacite disponible en kg"""
        return max(0, self.capacity_kg - self.current_load_kg)

    @property
    def is_underutilized(self) -> bool:
        """Vehicule sous-utilise (<40% remplissage)"""
        return self.fill_rate < 40.0


@dataclass
class Driver:
    """Chauffeur"""
    id: UUID
    name: str
    phone: str
    email: str
    license_number: str
    license_expiry: date
    vehicle_types: List[VehicleType]  # Types autorises
    current_vehicle_id: Optional[UUID]
    status: str  # available, on_trip, break, off_duty

    # Zone de travail preferee
    home_zone: Optional[str]

    # Audit
    created_by: UUID
    created_at: datetime


@dataclass
class CheNuZone:
    """
    Zone de placement intelligent (Champs Numeriques)
    Evite les zones de haute friction
    """
    id: UUID
    name: str
    zone_type: ZoneType
    center: GeoPoint
    radius_km: float

    # Caracteristiques
    friction_level: float  # 0-1 (0=fluide, 1=bloque)
    typical_delay_minutes: int
    peak_hours: List[int]  # Heures de pointe

    # Recommandations
    avoid_if_possible: bool
    alternative_zones: List[UUID]

    created_by: UUID
    created_at: datetime


@dataclass
class Trip:
    """Trajet"""
    id: UUID
    trip_number: str        # TRP-001, TRP-002
    trip_type: TripType
    status: TripStatus

    # Points
    origin: GeoPoint
    destination: GeoPoint
    waypoints: List[GeoPoint]

    # Timing
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]

    # Vehicule et chauffeur
    vehicle_id: Optional[UUID]
    driver_id: Optional[UUID]

    # Chargement
    load_type: LoadType
    load_description: str
    load_weight_kg: float
    load_volume_m3: float

    # Recurrence (pour trajets recurrents)
    recurrence_pattern: Optional[str]  # daily, weekly, monthly
    recurrence_days: Optional[List[int]]  # 0=lundi, 6=dimanche

    # Cout et distance
    estimated_distance_km: float
    actual_distance_km: Optional[float]
    estimated_cost: Decimal
    actual_cost: Optional[Decimal]

    # Covoiturage/Pooling
    allows_pooling: bool
    available_capacity_kg: float
    available_capacity_m3: float
    pooled_loads: List[UUID]  # IDs des charges mutualisees

    # Client
    client_id: Optional[UUID]
    client_name: Optional[str]

    # Audit
    created_by: UUID
    created_at: datetime
    updated_at: datetime


@dataclass
class SoustraitanceContract:
    """
    Contrat de sous-traitance (Uber, Taxi, partenaires)
    GOVERNANCE: Requires approval for execution
    """
    id: UUID
    contract_number: str
    soustraitance_type: SoustraitanceType
    status: SoustraitanceStatus

    # Trajet associe
    trip_id: UUID

    # Details
    partner_name: str
    partner_contact: str

    # Couts
    agreed_price: Decimal
    commission_rate: float  # % pour la plateforme

    # Timing
    requested_at: datetime
    confirmed_at: Optional[datetime]

    # GOVERNANCE - Rule #1
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]

    # Audit
    created_by: UUID
    created_at: datetime


@dataclass
class DispatchDecision:
    """
    Decision de dispatch (attribution de trajet)
    """
    id: UUID
    trip_id: UUID
    dispatch_mode: DispatchMode

    # Vehicule selectionne
    selected_vehicle_id: UUID
    selected_driver_id: Optional[UUID]

    # Score de decision (pour mode collaboratif)
    optimization_score: float
    fill_rate_before: float
    fill_rate_after: float

    # Alternatives considerees
    alternatives: List[Dict[str, Any]]

    # GOVERNANCE - Rule #1 (pour charges de haute valeur)
    requires_approval: bool
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]

    # Audit
    decided_by: UUID  # user_id ou "collaborative_ai"
    created_at: datetime


@dataclass
class PoolingOpportunity:
    """
    Opportunite de mutualisation/covoiturage detectee
    """
    id: UUID
    opportunity_type: str  # covoiturage, pooling_marchandises

    # Trajets pouvant etre combines
    base_trip_id: UUID
    candidate_trip_ids: List[UUID]

    # Economies estimees
    estimated_savings_percent: float
    estimated_emissions_saved_kg: float

    # Faisabilite
    feasibility_score: float  # 0-1
    constraints: List[str]

    # Statut
    status: str  # suggested, accepted, rejected, expired

    created_at: datetime
    expires_at: datetime


@dataclass
class FlowMetric:
    """
    Metrique de flux pour visualisation (Flow Map)
    """
    id: UUID
    zone_id: UUID
    timestamp: datetime

    # Metriques
    flow_status: FlowStatus
    friction_score: float  # 0-1
    fluidity_score: float  # 0-1 (inverse de friction)

    # Volume
    vehicles_count: int
    trips_in_progress: int
    average_speed_kmh: float

    # Couleur pour visualisation (inspiration 999Hz)
    color_hex: str  # #0057b8 (bleu cobalt) quand fluide


# ============================================================================
# TRANSPORT AGENT (AT·OM Flow)
# ============================================================================

class TransportAgent:
    """
    CHE·NU V68 Transport & Logistics Agent (AT·OM Flow)

    CONCEPT: Intelligence collective pour optimisation des transports
    - Chaque vehicule est un neurone
    - Chaque trajet est une synapse
    - Le systeme apprend et s'adapte

    GOVERNANCE COMPLIANCE:
    - Rule #1: Dispatch haute valeur + sous-traitance require APPROVAL
    - Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL (NO ranking)
    - Rule #6: Full audit trail with UUID, timestamps, created_by
    """

    def __init__(self):
        self.vehicles: Dict[UUID, Vehicle] = {}
        self.drivers: Dict[UUID, Driver] = {}
        self.trips: Dict[UUID, Trip] = {}
        self.zones: Dict[UUID, CheNuZone] = {}
        self.soustraitance: Dict[UUID, SoustraitanceContract] = {}
        self.dispatch_decisions: Dict[UUID, DispatchDecision] = {}
        self.pooling_opportunities: Dict[UUID, PoolingOpportunity] = {}
        self.flow_metrics: Dict[UUID, FlowMetric] = {}

        # Counters
        self._trip_counter = 0
        self._contract_counter = 0

        # Configuration
        self.high_value_threshold = Decimal("5000")  # Seuil pour approbation
        self.underutilization_threshold = 40.0  # % remplissage

    # ========================================================================
    # VEHICLE MANAGEMENT
    # ========================================================================

    async def register_vehicle(
        self,
        registration: str,
        name: str,
        vehicle_type: VehicleType,
        capacity_kg: float,
        capacity_m3: float,
        cost_per_km: Decimal,
        fuel_type: str,
        emissions_g_per_km: float,
        created_by: UUID,
        current_location: Optional[GeoPoint] = None
    ) -> Vehicle:
        """Enregistrer un nouveau vehicule"""
        now = datetime.utcnow()

        vehicle = Vehicle(
            id=uuid4(),
            registration=registration,
            name=name,
            vehicle_type=vehicle_type,
            status=VehicleStatus.AVAILABLE,
            capacity_kg=capacity_kg,
            capacity_m3=capacity_m3,
            current_load_kg=0.0,
            current_load_m3=0.0,
            current_location=current_location,
            destination=None,
            driver_id=None,
            driver_name=None,
            cost_per_km=cost_per_km,
            fuel_type=fuel_type,
            emissions_g_per_km=emissions_g_per_km,
            created_by=created_by,
            created_at=now,
            updated_at=now
        )

        self.vehicles[vehicle.id] = vehicle
        logger.info(f"Vehicle registered: {registration} - {name}")
        return vehicle

    async def update_vehicle_location(
        self,
        vehicle_id: UUID,
        location: GeoPoint,
        user_id: UUID
    ) -> Vehicle:
        """Mettre a jour la position du vehicule"""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle not found: {vehicle_id}")

        vehicle = self.vehicles[vehicle_id]
        vehicle.current_location = location
        vehicle.updated_at = datetime.utcnow()

        return vehicle

    async def update_vehicle_load(
        self,
        vehicle_id: UUID,
        load_kg: float,
        load_m3: float,
        user_id: UUID
    ) -> Vehicle:
        """Mettre a jour le chargement du vehicule"""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle not found: {vehicle_id}")

        vehicle = self.vehicles[vehicle_id]
        vehicle.current_load_kg = load_kg
        vehicle.current_load_m3 = load_m3
        vehicle.updated_at = datetime.utcnow()

        # Detecter sous-utilisation
        if vehicle.is_underutilized and vehicle.status == VehicleStatus.IN_TRANSIT:
            logger.info(f"COLLABORATIF: Vehicle {vehicle.name} sous-utilise ({vehicle.fill_rate:.1f}%)")
            await self._suggest_pooling_opportunities(vehicle_id)

        return vehicle

    async def get_vehicles(self) -> List[Vehicle]:
        """
        Get all vehicles - ALPHABETICAL by name (Rule #5)
        NOT sorted by efficiency, fill rate, or utilization
        """
        vehicles = list(self.vehicles.values())
        # RULE #5: ALPHABETICAL by name, NOT by efficiency
        return sorted(vehicles, key=lambda v: v.name.lower())

    async def get_underutilized_vehicles(self) -> List[Vehicle]:
        """
        Get vehicles with low fill rate (<40%)
        ALPHABETICAL (Rule #5) - for collaborative optimization
        """
        underutilized = [v for v in self.vehicles.values()
                        if v.is_underutilized and v.status == VehicleStatus.IN_TRANSIT]
        return sorted(underutilized, key=lambda v: v.name.lower())

    # ========================================================================
    # DRIVER MANAGEMENT
    # ========================================================================

    async def register_driver(
        self,
        name: str,
        phone: str,
        email: str,
        license_number: str,
        license_expiry: date,
        vehicle_types: List[VehicleType],
        created_by: UUID,
        home_zone: Optional[str] = None
    ) -> Driver:
        """Enregistrer un nouveau chauffeur"""
        driver = Driver(
            id=uuid4(),
            name=name,
            phone=phone,
            email=email,
            license_number=license_number,
            license_expiry=license_expiry,
            vehicle_types=vehicle_types,
            current_vehicle_id=None,
            status="available",
            home_zone=home_zone,
            created_by=created_by,
            created_at=datetime.utcnow()
        )

        self.drivers[driver.id] = driver
        logger.info(f"Driver registered: {name}")
        return driver

    async def get_drivers(self) -> List[Driver]:
        """
        Get all drivers - ALPHABETICAL by name (Rule #5)
        NOT sorted by rating, performance, or efficiency
        """
        drivers = list(self.drivers.values())
        # RULE #5: ALPHABETICAL by name, NOT by performance
        return sorted(drivers, key=lambda d: d.name.lower())

    async def assign_driver_to_vehicle(
        self,
        driver_id: UUID,
        vehicle_id: UUID,
        user_id: UUID
    ) -> Tuple[Driver, Vehicle]:
        """Assigner un chauffeur a un vehicule"""
        if driver_id not in self.drivers:
            raise ValueError(f"Driver not found: {driver_id}")
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle not found: {vehicle_id}")

        driver = self.drivers[driver_id]
        vehicle = self.vehicles[vehicle_id]

        # Verifier compatibilite
        if vehicle.vehicle_type not in driver.vehicle_types:
            raise ValueError(f"Driver not authorized for {vehicle.vehicle_type.value}")

        driver.current_vehicle_id = vehicle_id
        vehicle.driver_id = driver_id
        vehicle.driver_name = driver.name
        vehicle.updated_at = datetime.utcnow()

        logger.info(f"Driver {driver.name} assigned to vehicle {vehicle.name}")
        return driver, vehicle

    # ========================================================================
    # CHE-NU ZONES (Placement Intelligent)
    # ========================================================================

    async def create_zone(
        self,
        name: str,
        zone_type: ZoneType,
        center: GeoPoint,
        radius_km: float,
        friction_level: float,
        typical_delay_minutes: int,
        created_by: UUID,
        peak_hours: Optional[List[int]] = None,
        avoid_if_possible: bool = False,
        alternative_zones: Optional[List[UUID]] = None
    ) -> CheNuZone:
        """Creer une zone Che-Nu"""
        zone = CheNuZone(
            id=uuid4(),
            name=name,
            zone_type=zone_type,
            center=center,
            radius_km=radius_km,
            friction_level=friction_level,
            typical_delay_minutes=typical_delay_minutes,
            peak_hours=peak_hours or [],
            avoid_if_possible=avoid_if_possible,
            alternative_zones=alternative_zones or [],
            created_by=created_by,
            created_at=datetime.utcnow()
        )

        self.zones[zone.id] = zone
        logger.info(f"Che-Nu Zone created: {name} ({zone_type.value})")
        return zone

    async def get_zones(self) -> List[CheNuZone]:
        """
        Get all zones - ALPHABETICAL by name (Rule #5)
        """
        zones = list(self.zones.values())
        return sorted(zones, key=lambda z: z.name.lower())

    async def find_zones_to_avoid(self, current_hour: int) -> List[CheNuZone]:
        """
        Find high-friction zones to avoid
        ALPHABETICAL (Rule #5)
        """
        zones_to_avoid = []
        for zone in self.zones.values():
            if zone.avoid_if_possible:
                zones_to_avoid.append(zone)
            elif zone.friction_level > 0.7 and current_hour in zone.peak_hours:
                zones_to_avoid.append(zone)

        return sorted(zones_to_avoid, key=lambda z: z.name.lower())

    async def suggest_alternative_route(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        user_id: UUID
    ) -> Dict[str, Any]:
        """
        Suggest route avoiding high-friction zones
        """
        zones_to_avoid = await self.find_zones_to_avoid(datetime.now().hour)

        # Simplified routing suggestion
        # In production, this would integrate with routing APIs

        return {
            "suggested_route": "Route optimisee evitant les zones haute friction",
            "zones_avoided": [z.name for z in zones_to_avoid],
            "estimated_time_saved_minutes": sum(z.typical_delay_minutes for z in zones_to_avoid),
            "friction_score_reduction": len(zones_to_avoid) * 0.1
        }

    # ========================================================================
    # TRIP MANAGEMENT
    # ========================================================================

    async def create_trip(
        self,
        trip_type: TripType,
        origin: GeoPoint,
        destination: GeoPoint,
        scheduled_departure: datetime,
        scheduled_arrival: datetime,
        load_type: LoadType,
        load_description: str,
        load_weight_kg: float,
        load_volume_m3: float,
        created_by: UUID,
        vehicle_id: Optional[UUID] = None,
        driver_id: Optional[UUID] = None,
        waypoints: Optional[List[GeoPoint]] = None,
        recurrence_pattern: Optional[str] = None,
        recurrence_days: Optional[List[int]] = None,
        allows_pooling: bool = True,
        client_id: Optional[UUID] = None,
        client_name: Optional[str] = None
    ) -> Trip:
        """Creer un trajet"""
        self._trip_counter += 1
        trip_number = f"TRP-{self._trip_counter:04d}"

        # Calculer distance estimee
        estimated_distance = origin.distance_to(destination)
        if waypoints:
            points = [origin] + waypoints + [destination]
            estimated_distance = sum(
                points[i].distance_to(points[i+1])
                for i in range(len(points)-1)
            )

        # Estimer cout
        estimated_cost = Decimal(str(estimated_distance * 2))  # 2$/km par defaut

        now = datetime.utcnow()
        trip = Trip(
            id=uuid4(),
            trip_number=trip_number,
            trip_type=trip_type,
            status=TripStatus.PLANNED,
            origin=origin,
            destination=destination,
            waypoints=waypoints or [],
            scheduled_departure=scheduled_departure,
            scheduled_arrival=scheduled_arrival,
            actual_departure=None,
            actual_arrival=None,
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            load_type=load_type,
            load_description=load_description,
            load_weight_kg=load_weight_kg,
            load_volume_m3=load_volume_m3,
            recurrence_pattern=recurrence_pattern,
            recurrence_days=recurrence_days,
            estimated_distance_km=estimated_distance,
            actual_distance_km=None,
            estimated_cost=estimated_cost,
            actual_cost=None,
            allows_pooling=allows_pooling,
            available_capacity_kg=0,  # Sera calcule si vehicule assigne
            available_capacity_m3=0,
            pooled_loads=[],
            client_id=client_id,
            client_name=client_name,
            created_by=created_by,
            created_at=now,
            updated_at=now
        )

        self.trips[trip.id] = trip
        logger.info(f"Trip created: {trip_number} - {trip_type.value}")

        # Detecter opportunites de pooling si autorise
        if allows_pooling:
            await self._detect_pooling_opportunities(trip.id)

        return trip

    async def start_trip(self, trip_id: UUID, user_id: UUID) -> Trip:
        """Demarrer un trajet"""
        if trip_id not in self.trips:
            raise ValueError(f"Trip not found: {trip_id}")

        trip = self.trips[trip_id]
        trip.status = TripStatus.IN_PROGRESS
        trip.actual_departure = datetime.utcnow()
        trip.updated_at = datetime.utcnow()

        # Mettre a jour le vehicule
        if trip.vehicle_id and trip.vehicle_id in self.vehicles:
            vehicle = self.vehicles[trip.vehicle_id]
            vehicle.status = VehicleStatus.IN_TRANSIT
            vehicle.destination = trip.destination
            vehicle.current_load_kg = trip.load_weight_kg
            vehicle.current_load_m3 = trip.load_volume_m3
            vehicle.updated_at = datetime.utcnow()

        logger.info(f"Trip {trip.trip_number} started")
        return trip

    async def complete_trip(
        self,
        trip_id: UUID,
        actual_distance_km: float,
        actual_cost: Decimal,
        user_id: UUID
    ) -> Trip:
        """Terminer un trajet"""
        if trip_id not in self.trips:
            raise ValueError(f"Trip not found: {trip_id}")

        trip = self.trips[trip_id]
        trip.status = TripStatus.COMPLETED
        trip.actual_arrival = datetime.utcnow()
        trip.actual_distance_km = actual_distance_km
        trip.actual_cost = actual_cost
        trip.updated_at = datetime.utcnow()

        # Liberer le vehicule
        if trip.vehicle_id and trip.vehicle_id in self.vehicles:
            vehicle = self.vehicles[trip.vehicle_id]
            vehicle.status = VehicleStatus.AVAILABLE
            vehicle.destination = None
            vehicle.current_load_kg = 0
            vehicle.current_load_m3 = 0
            vehicle.current_location = trip.destination
            vehicle.updated_at = datetime.utcnow()

        logger.info(f"Trip {trip.trip_number} completed")
        return trip

    async def get_trips(self) -> List[Trip]:
        """
        Get all trips - CHRONOLOGICAL by scheduled_departure (Rule #5)
        NOT sorted by profitability or priority
        """
        trips = list(self.trips.values())
        # RULE #5: CHRONOLOGICAL, NOT by profitability
        return sorted(trips, key=lambda t: t.scheduled_departure, reverse=True)

    async def get_active_trips(self) -> List[Trip]:
        """Get trips in progress - CHRONOLOGICAL (Rule #5)"""
        active = [t for t in self.trips.values()
                 if t.status in [TripStatus.PLANNED, TripStatus.CONFIRMED, TripStatus.IN_PROGRESS]]
        return sorted(active, key=lambda t: t.scheduled_departure)

    # ========================================================================
    # DISPATCH COLLABORATIF
    # ========================================================================

    async def dispatch_collaborative(
        self,
        trip_id: UUID,
        optimization_goal: OptimizationGoal,
        user_id: UUID
    ) -> DispatchDecision:
        """
        Dispatch collaboratif - Intelligence collective
        Trouve le meilleur vehicule en considerant l'efficacite globale
        """
        if trip_id not in self.trips:
            raise ValueError(f"Trip not found: {trip_id}")

        trip = self.trips[trip_id]

        # Trouver vehicules disponibles
        available_vehicles = [
            v for v in self.vehicles.values()
            if v.status == VehicleStatus.AVAILABLE
            and v.available_capacity_kg >= trip.load_weight_kg
        ]

        if not available_vehicles:
            raise ValueError("No available vehicles with sufficient capacity")

        # Evaluer chaque option
        options = []
        for vehicle in available_vehicles:
            # Calculer le score de remplissage apres
            fill_after = ((vehicle.current_load_kg + trip.load_weight_kg) /
                         vehicle.capacity_kg * 100)

            # Score combine base sur l'objectif
            if optimization_goal == OptimizationGoal.FILL_RATE:
                score = fill_after  # Maximiser remplissage
            elif optimization_goal == OptimizationGoal.EMISSIONS:
                score = 100 - (vehicle.emissions_g_per_km * trip.estimated_distance_km / 1000)
            elif optimization_goal == OptimizationGoal.COST:
                score = 100 - float(vehicle.cost_per_km * Decimal(str(trip.estimated_distance_km)))
            else:  # BALANCED
                score = fill_after * 0.5 + (100 - vehicle.emissions_g_per_km/10) * 0.3 + 50 * 0.2

            options.append({
                "vehicle_id": str(vehicle.id),
                "vehicle_name": vehicle.name,
                "fill_rate_before": vehicle.fill_rate,
                "fill_rate_after": fill_after,
                "score": score,
                "emissions_kg": vehicle.emissions_g_per_km * trip.estimated_distance_km / 1000,
                "cost": float(vehicle.cost_per_km * Decimal(str(trip.estimated_distance_km)))
            })

        # Trier par score (interne, pas affiche)
        options.sort(key=lambda x: x["score"], reverse=True)
        best_option = options[0]
        best_vehicle = self.vehicles[UUID(best_option["vehicle_id"])]

        # Verifier si approbation requise (haute valeur)
        requires_approval = trip.estimated_cost >= self.high_value_threshold

        decision = DispatchDecision(
            id=uuid4(),
            trip_id=trip_id,
            dispatch_mode=DispatchMode.COLLABORATIVE,
            selected_vehicle_id=best_vehicle.id,
            selected_driver_id=best_vehicle.driver_id,
            optimization_score=best_option["score"],
            fill_rate_before=best_option["fill_rate_before"],
            fill_rate_after=best_option["fill_rate_after"],
            alternatives=options[1:4],  # Top 3 alternatives
            requires_approval=requires_approval,
            approved_by=None,
            approved_at=None,
            decided_by=user_id,
            created_at=datetime.utcnow()
        )

        self.dispatch_decisions[decision.id] = decision

        # Assigner vehicule au trajet si pas besoin d'approbation
        if not requires_approval:
            trip.vehicle_id = best_vehicle.id
            trip.driver_id = best_vehicle.driver_id
            trip.status = TripStatus.CONFIRMED
            trip.updated_at = datetime.utcnow()
            logger.info(f"COLLABORATIF: Trip {trip.trip_number} assigned to {best_vehicle.name}")
        else:
            logger.info(f"GOVERNANCE: Dispatch for {trip.trip_number} requires approval (value >= {self.high_value_threshold})")

        return decision

    async def approve_dispatch(
        self,
        decision_id: UUID,
        approved: bool,
        approver_id: UUID
    ) -> DispatchDecision:
        """
        GOVERNANCE - Rule #1: Approve or reject a dispatch decision
        """
        if decision_id not in self.dispatch_decisions:
            raise ValueError(f"Dispatch decision not found: {decision_id}")

        decision = self.dispatch_decisions[decision_id]

        if not decision.requires_approval:
            raise ValueError("This decision does not require approval")

        decision.approved_by = approver_id
        decision.approved_at = datetime.utcnow()

        if approved:
            # Appliquer la decision
            trip = self.trips[decision.trip_id]
            trip.vehicle_id = decision.selected_vehicle_id
            trip.driver_id = decision.selected_driver_id
            trip.status = TripStatus.CONFIRMED
            trip.updated_at = datetime.utcnow()

            logger.info(f"GOVERNANCE: Dispatch approved by {approver_id}")
        else:
            logger.info(f"GOVERNANCE: Dispatch rejected by {approver_id}")

        return decision

    # ========================================================================
    # SOUS-TRAITANCE (Uber, Taxi, Partenaires)
    # ========================================================================

    async def request_soustraitance(
        self,
        trip_id: UUID,
        soustraitance_type: SoustraitanceType,
        partner_name: str,
        partner_contact: str,
        agreed_price: Decimal,
        commission_rate: float,
        created_by: UUID
    ) -> SoustraitanceContract:
        """
        Demander sous-traitance
        GOVERNANCE: Requires approval before activation
        """
        if trip_id not in self.trips:
            raise ValueError(f"Trip not found: {trip_id}")

        self._contract_counter += 1
        contract_number = f"SUB-{self._contract_counter:04d}"

        contract = SoustraitanceContract(
            id=uuid4(),
            contract_number=contract_number,
            soustraitance_type=soustraitance_type,
            status=SoustraitanceStatus.PENDING_APPROVAL,  # GOVERNANCE
            trip_id=trip_id,
            partner_name=partner_name,
            partner_contact=partner_contact,
            agreed_price=agreed_price,
            commission_rate=commission_rate,
            requested_at=datetime.utcnow(),
            confirmed_at=None,
            approved_by=None,
            approved_at=None,
            rejection_reason=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )

        self.soustraitance[contract.id] = contract
        logger.info(f"GOVERNANCE: Sous-traitance {contract_number} requires approval")
        return contract

    async def approve_soustraitance(
        self,
        contract_id: UUID,
        approved: bool,
        approver_id: UUID,
        rejection_reason: Optional[str] = None
    ) -> SoustraitanceContract:
        """
        GOVERNANCE - Rule #1: Approve or reject sous-traitance contract
        """
        if contract_id not in self.soustraitance:
            raise ValueError(f"Contract not found: {contract_id}")

        contract = self.soustraitance[contract_id]

        if contract.status != SoustraitanceStatus.PENDING_APPROVAL:
            raise ValueError("Contract is not pending approval")

        contract.approved_by = approver_id
        contract.approved_at = datetime.utcnow()

        if approved:
            contract.status = SoustraitanceStatus.APPROVED
            logger.info(f"GOVERNANCE: Sous-traitance {contract.contract_number} APPROVED by {approver_id}")
        else:
            contract.status = SoustraitanceStatus.REJECTED
            contract.rejection_reason = rejection_reason
            logger.info(f"GOVERNANCE: Sous-traitance {contract.contract_number} REJECTED by {approver_id}")

        return contract

    async def activate_soustraitance(
        self,
        contract_id: UUID,
        user_id: UUID
    ) -> SoustraitanceContract:
        """Activate an approved sous-traitance contract"""
        if contract_id not in self.soustraitance:
            raise ValueError(f"Contract not found: {contract_id}")

        contract = self.soustraitance[contract_id]

        if contract.status != SoustraitanceStatus.APPROVED:
            raise ValueError("Contract must be approved before activation")

        contract.status = SoustraitanceStatus.ACTIVE
        contract.confirmed_at = datetime.utcnow()

        logger.info(f"Sous-traitance {contract.contract_number} activated")
        return contract

    async def get_soustraitance_contracts(self) -> List[SoustraitanceContract]:
        """
        Get all sous-traitance contracts - CHRONOLOGICAL (Rule #5)
        """
        contracts = list(self.soustraitance.values())
        return sorted(contracts, key=lambda c: c.created_at, reverse=True)

    # ========================================================================
    # POOLING & COVOITURAGE
    # ========================================================================

    async def _detect_pooling_opportunities(self, trip_id: UUID) -> List[PoolingOpportunity]:
        """
        Detecter opportunites de mutualisation
        Internal method called when trips are created
        """
        if trip_id not in self.trips:
            return []

        new_trip = self.trips[trip_id]
        opportunities = []

        # Chercher trajets compatibles
        for existing_trip in self.trips.values():
            if existing_trip.id == trip_id:
                continue
            if not existing_trip.allows_pooling:
                continue
            if existing_trip.status not in [TripStatus.PLANNED, TripStatus.CONFIRMED]:
                continue

            # Verifier compatibilite geographique (simplifie)
            origin_distance = new_trip.origin.distance_to(existing_trip.origin)
            dest_distance = new_trip.destination.distance_to(existing_trip.destination)

            if origin_distance < 10 and dest_distance < 10:  # Dans 10km
                # Verifier compatibilite temporelle
                time_diff = abs((new_trip.scheduled_departure - existing_trip.scheduled_departure).total_seconds() / 3600)

                if time_diff < 2:  # Dans 2 heures
                    opportunity = PoolingOpportunity(
                        id=uuid4(),
                        opportunity_type="pooling_marchandises" if new_trip.load_type != LoadType.PASSENGER else "covoiturage",
                        base_trip_id=existing_trip.id,
                        candidate_trip_ids=[new_trip.id],
                        estimated_savings_percent=min(30, (1 - origin_distance/10) * 30),
                        estimated_emissions_saved_kg=(new_trip.estimated_distance_km * 100) / 1000,  # ~100g/km
                        feasibility_score=0.8,
                        constraints=[],
                        status="suggested",
                        created_at=datetime.utcnow(),
                        expires_at=datetime.utcnow()  # + timedelta(hours=24)
                    )

                    self.pooling_opportunities[opportunity.id] = opportunity
                    opportunities.append(opportunity)

                    logger.info(f"COLLABORATIF: Pooling opportunity detected for {new_trip.trip_number}")

        return opportunities

    async def _suggest_pooling_opportunities(self, vehicle_id: UUID) -> None:
        """
        Suggest pooling for underutilized vehicle
        Internal method
        """
        if vehicle_id not in self.vehicles:
            return

        vehicle = self.vehicles[vehicle_id]

        # Trouver des charges a proximite
        available_loads = [
            t for t in self.trips.values()
            if t.status == TripStatus.PLANNED
            and t.vehicle_id is None
            and t.load_weight_kg <= vehicle.available_capacity_kg
        ]

        if available_loads:
            logger.info(f"COLLABORATIF: {len(available_loads)} potential loads for underutilized vehicle {vehicle.name}")

    async def accept_pooling_opportunity(
        self,
        opportunity_id: UUID,
        user_id: UUID
    ) -> PoolingOpportunity:
        """Accept a pooling opportunity"""
        if opportunity_id not in self.pooling_opportunities:
            raise ValueError(f"Opportunity not found: {opportunity_id}")

        opportunity = self.pooling_opportunities[opportunity_id]
        opportunity.status = "accepted"

        # Combiner les trajets
        base_trip = self.trips[opportunity.base_trip_id]
        for candidate_id in opportunity.candidate_trip_ids:
            if candidate_id in self.trips:
                candidate = self.trips[candidate_id]
                base_trip.pooled_loads.append(candidate_id)
                candidate.status = TripStatus.CANCELLED  # Marquer comme combine

        logger.info(f"Pooling opportunity accepted - trips combined")
        return opportunity

    async def get_pooling_opportunities(self) -> List[PoolingOpportunity]:
        """
        Get all pooling opportunities - CHRONOLOGICAL (Rule #5)
        """
        opportunities = [o for o in self.pooling_opportunities.values()
                        if o.status == "suggested"]
        return sorted(opportunities, key=lambda o: o.created_at, reverse=True)

    # ========================================================================
    # FLOW METRICS (Visualisation)
    # ========================================================================

    async def record_flow_metric(
        self,
        zone_id: UUID,
        friction_score: float,
        vehicles_count: int,
        trips_in_progress: int,
        average_speed_kmh: float
    ) -> FlowMetric:
        """Record flow metric for zone"""
        if zone_id not in self.zones:
            raise ValueError(f"Zone not found: {zone_id}")

        fluidity_score = 1 - friction_score

        # Determiner statut du flux
        if fluidity_score > 0.8:
            flow_status = FlowStatus.FLUID
            color_hex = "#0057b8"  # Bleu cobalt - 999Hz
        elif fluidity_score > 0.5:
            flow_status = FlowStatus.NORMAL
            color_hex = "#28a745"  # Vert
        elif fluidity_score > 0.2:
            flow_status = FlowStatus.CONGESTED
            color_hex = "#fd7e14"  # Orange
        else:
            flow_status = FlowStatus.BLOCKED
            color_hex = "#dc3545"  # Rouge

        metric = FlowMetric(
            id=uuid4(),
            zone_id=zone_id,
            timestamp=datetime.utcnow(),
            flow_status=flow_status,
            friction_score=friction_score,
            fluidity_score=fluidity_score,
            vehicles_count=vehicles_count,
            trips_in_progress=trips_in_progress,
            average_speed_kmh=average_speed_kmh,
            color_hex=color_hex
        )

        self.flow_metrics[metric.id] = metric
        return metric

    async def get_global_flow_score(self) -> Dict[str, Any]:
        """
        Get global flow score (Friction vs Fluidite)
        For the iPad beach visualization
        """
        recent_metrics = [
            m for m in self.flow_metrics.values()
            if (datetime.utcnow() - m.timestamp).total_seconds() < 3600  # Last hour
        ]

        if not recent_metrics:
            return {
                "global_fluidity": 0.8,  # Default optimiste
                "global_friction": 0.2,
                "flow_status": "fluid",
                "color_hex": "#0057b8",
                "message": "Flux optimal - 999Hz"
            }

        avg_fluidity = sum(m.fluidity_score for m in recent_metrics) / len(recent_metrics)
        avg_friction = sum(m.friction_score for m in recent_metrics) / len(recent_metrics)

        if avg_fluidity > 0.8:
            status = "fluid"
            color = "#0057b8"
            message = "Flux optimal - 999Hz"
        elif avg_fluidity > 0.5:
            status = "normal"
            color = "#28a745"
            message = "Flux normal"
        elif avg_fluidity > 0.2:
            status = "congested"
            color = "#fd7e14"
            message = "Congestion detectee"
        else:
            status = "blocked"
            color = "#dc3545"
            message = "Flux bloque - intervention requise"

        return {
            "global_fluidity": round(avg_fluidity, 2),
            "global_friction": round(avg_friction, 2),
            "flow_status": status,
            "color_hex": color,
            "message": message,
            "zones_monitored": len(set(m.zone_id for m in recent_metrics)),
            "vehicles_active": sum(m.vehicles_count for m in recent_metrics) // len(recent_metrics)
        }

    # ========================================================================
    # ANALYTICS
    # ========================================================================

    async def get_transport_summary(self) -> Dict[str, Any]:
        """Get transport summary dashboard"""
        vehicles = list(self.vehicles.values())
        trips = list(self.trips.values())
        contracts = list(self.soustraitance.values())

        active_trips = [t for t in trips if t.status == TripStatus.IN_PROGRESS]
        completed_trips = [t for t in trips if t.status == TripStatus.COMPLETED]

        total_distance = sum(t.actual_distance_km or t.estimated_distance_km for t in completed_trips)
        total_revenue = sum(float(t.actual_cost or t.estimated_cost) for t in completed_trips)

        # Calculer efficacite moyenne
        avg_fill_rate = 0
        if vehicles:
            avg_fill_rate = sum(v.fill_rate for v in vehicles if v.status == VehicleStatus.IN_TRANSIT) / max(1, len([v for v in vehicles if v.status == VehicleStatus.IN_TRANSIT]))

        # Flow score
        flow_score = await self.get_global_flow_score()

        return {
            "fleet": {
                "total_vehicles": len(vehicles),
                "available": len([v for v in vehicles if v.status == VehicleStatus.AVAILABLE]),
                "in_transit": len([v for v in vehicles if v.status == VehicleStatus.IN_TRANSIT]),
                "maintenance": len([v for v in vehicles if v.status == VehicleStatus.MAINTENANCE]),
                "avg_fill_rate": round(avg_fill_rate, 1),
            },
            "drivers": {
                "total": len(self.drivers),
                "available": len([d for d in self.drivers.values() if d.status == "available"]),
                "on_trip": len([d for d in self.drivers.values() if d.status == "on_trip"]),
            },
            "trips": {
                "total": len(trips),
                "planned": len([t for t in trips if t.status == TripStatus.PLANNED]),
                "active": len(active_trips),
                "completed": len(completed_trips),
                "total_distance_km": round(total_distance, 1),
            },
            "financials": {
                "total_revenue": round(total_revenue, 2),
                "pending_soustraitance": len([c for c in contracts if c.status == SoustraitanceStatus.PENDING_APPROVAL]),
                "active_soustraitance": len([c for c in contracts if c.status == SoustraitanceStatus.ACTIVE]),
            },
            "optimization": {
                "pooling_opportunities": len([o for o in self.pooling_opportunities.values() if o.status == "suggested"]),
                "underutilized_vehicles": len([v for v in vehicles if v.is_underutilized]),
            },
            "flow": flow_score
        }


# Singleton instance
_transport_agent: Optional[TransportAgent] = None


def get_transport_agent() -> TransportAgent:
    """Get or create transport agent singleton"""
    global _transport_agent
    if _transport_agent is None:
        _transport_agent = TransportAgent()
    return _transport_agent
