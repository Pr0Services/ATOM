"""
CHE·NU V68 Symbiotic Energy Agent
Module Environnement 2/4 - Energie en Symbiose

CONCEPT: Energie Symbiotique
- Micro-reseaux locaux decentralises
- Optimisation solaire selon l'orientation
- Stockage distribue et partage
- Production = Consommation locale

PHILOSOPHIE:
L'energie n'est pas une marchandise - c'est un flux naturel.
Comme le soleil partage sa lumiere, nous partageons l'energie.

PRIVACY:
- Consommation par zone, pas par foyer
- Pas de tracking individuel
- Anonymisation des producteurs

GOVERNANCE COMPLIANCE:
- Rule #1: Connexions haute puissance require APPROVAL
- Rule #5: Producteurs ALPHABETICAL
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
import math

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY HELPERS
# ============================================================================

def anonymize_location(latitude: float, longitude: float) -> str:
    """Anonymize location to microgrid zone (~500m precision)"""
    lat_zone = round(latitude, 3)
    lon_zone = round(longitude, 3)
    return f"grid_zone_{lat_zone}_{lon_zone}"


def anonymize_producer_id(producer_id: UUID) -> str:
    """Anonymize producer ID"""
    salt = "CHENU_ENERGY_SUN_999Hz"
    return hashlib.sha256(f"{salt}{str(producer_id)}{salt}".encode()).hexdigest()[:16]


# ============================================================================
# ENUMS
# ============================================================================

class EnergySource(Enum):
    """Sources d'energie"""
    SOLAR = "solar"                  # Solaire photovoltaique
    SOLAR_THERMAL = "solar_thermal"  # Solaire thermique
    WIND = "wind"                    # Eolien
    HYDRO = "hydro"                  # Hydro (petite echelle)
    BIOMASS = "biomass"              # Biomasse
    GEOTHERMAL = "geothermal"        # Geothermie
    HYBRID = "hybrid"                # Hybride (multiple sources)


class StorageType(Enum):
    """Types de stockage"""
    BATTERY_LITHIUM = "battery_lithium"
    BATTERY_FLOW = "battery_flow"
    BATTERY_SODIUM = "battery_sodium"
    THERMAL = "thermal"              # Stockage thermique
    GRAVITY = "gravity"              # Stockage gravitaire
    HYDROGEN = "hydrogen"            # Hydrogene
    NONE = "none"                    # Pas de stockage


class GridStatus(Enum):
    """Statut du micro-reseau"""
    OFFLINE = "offline"              # Hors ligne
    STARTING = "starting"            # Demarrage
    BALANCED = "balanced"            # Equilibre
    SURPLUS = "surplus"              # Surplus
    DEFICIT = "deficit"              # Deficit
    CRITICAL = "critical"            # Critique
    MAINTENANCE = "maintenance"      # Maintenance


class FlowDirection(Enum):
    """Direction du flux d'energie"""
    PRODUCING = "producing"          # Production
    CONSUMING = "consuming"          # Consommation
    STORING = "storing"              # Stockage
    SHARING = "sharing"              # Partage
    RECEIVING = "receiving"          # Reception


class ConnectionType(Enum):
    """Type de connexion au reseau"""
    PRODUCER = "producer"            # Producteur pur
    CONSUMER = "consumer"            # Consommateur pur
    PROSUMER = "prosumer"            # Producteur-consommateur
    STORAGE = "storage"              # Stockage pur
    HUB = "hub"                      # Hub de distribution


class TimeOfDay(Enum):
    """Periode de la journee (pour tarification solaire)"""
    DAWN = "dawn"                    # 5-7h
    MORNING = "morning"              # 7-12h
    PEAK = "peak"                    # 12-15h (pic solaire)
    AFTERNOON = "afternoon"          # 15-18h
    DUSK = "dusk"                    # 18-20h
    NIGHT = "night"                  # 20-5h


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoPoint:
    """Point geographique (precision reduite)"""
    latitude: float
    longitude: float

    def __post_init__(self):
        self.latitude = round(self.latitude, 3)
        self.longitude = round(self.longitude, 3)


@dataclass
class SolarOrientation:
    """Orientation pour optimisation solaire"""
    azimuth_deg: float     # 0=Nord, 90=Est, 180=Sud, 270=Ouest
    tilt_deg: float        # Inclinaison (optimal ~15-20deg pour tropiques)
    shading_factor: float  # 0-1, 1=pas d'ombre

    @property
    def efficiency_factor(self) -> float:
        """Calculate efficiency based on orientation"""
        # Optimal for tropics: azimuth=180 (sud), tilt=15-20
        azimuth_factor = 1.0 - abs(self.azimuth_deg - 180) / 180 * 0.3
        tilt_factor = 1.0 - abs(self.tilt_deg - 17) / 90 * 0.4
        return azimuth_factor * tilt_factor * self.shading_factor


@dataclass
class EnergyNode:
    """Noeud de production/consommation"""
    id: UUID
    zone_id: str
    connection_type: ConnectionType
    location: GeoPoint

    # Capacity
    capacity_kw: Decimal           # Capacite installee
    current_output_kw: Decimal     # Production/consommation actuelle

    # Source (for producers)
    energy_source: Optional[EnergySource] = None
    orientation: Optional[SolarOrientation] = None

    # Storage (if applicable)
    storage_type: StorageType = StorageType.NONE
    storage_capacity_kwh: Decimal = Decimal("0")
    storage_level_kwh: Decimal = Decimal("0")

    # Status
    status: str = "active"
    last_reading: datetime = field(default_factory=datetime.now)

    # PRIVACY
    owner_anon_id: str = ""

    # Audit
    audit_log: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MicroGrid:
    """Micro-reseau local"""
    id: UUID
    name: str
    zone_id: str
    center: GeoPoint
    radius_km: float

    # Nodes
    node_ids: List[UUID] = field(default_factory=list)

    # Capacity
    total_capacity_kw: Decimal = Decimal("0")
    total_storage_kwh: Decimal = Decimal("0")

    # Current state
    status: GridStatus = GridStatus.OFFLINE
    current_production_kw: Decimal = Decimal("0")
    current_consumption_kw: Decimal = Decimal("0")
    current_storage_kwh: Decimal = Decimal("0")

    # Balance
    balance_kw: Decimal = Decimal("0")  # Positive = surplus

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)


@dataclass
class EnergyTransfer:
    """Transfert d'energie entre zones"""
    id: UUID
    from_grid_id: UUID
    to_grid_id: UUID

    amount_kwh: Decimal
    duration_hours: float
    power_kw: Decimal

    # Timing
    started_at: datetime
    completed_at: Optional[datetime] = None

    # Status
    status: str = "pending"  # pending, pending_approval, approved, in_progress, completed

    # GOVERNANCE
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None


@dataclass
class SolarForecast:
    """Prevision solaire"""
    zone_id: str
    forecast_date: datetime
    time_of_day: TimeOfDay

    # Predictions
    irradiance_wm2: float      # Irradiance solaire
    cloud_cover_pct: float     # Couverture nuageuse
    expected_output_pct: float # % de capacite attendu

    # Confidence
    confidence: float = 0.8


@dataclass
class EnergyMetrics:
    """Metriques energetiques"""
    timestamp: datetime

    # Production
    total_production_kwh: Decimal
    solar_production_kwh: Decimal
    other_renewable_kwh: Decimal

    # Consumption
    total_consumption_kwh: Decimal

    # Balance
    self_sufficiency_pct: float  # % de consommation couverte localement
    surplus_shared_kwh: Decimal
    deficit_received_kwh: Decimal

    # Grid health
    active_grids: int
    grids_balanced: int
    grids_surplus: int
    grids_deficit: int

    # Indices
    symbiosis_index: float       # 0-1, degree of local sharing
    solar_efficiency_index: float # 0-1, actual vs optimal solar


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Transfer power threshold requiring approval
HIGH_POWER_THRESHOLD_KW = Decimal("100")

# Large transfer requiring approval
LARGE_TRANSFER_THRESHOLD_KWH = Decimal("500")


# ============================================================================
# SYMBIOTIC ENERGY AGENT
# ============================================================================

class SymbioticEnergyAgent:
    """
    Agent d'Energie Symbiotique

    L'energie comme un flux naturel:
    - Le soleil donne, nous recevons
    - Le surplus se partage
    - L'equilibre se trouve

    Mission: Optimiser la production locale, minimiser les pertes
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
        self._nodes: Dict[UUID, EnergyNode] = {}
        self._grids: Dict[UUID, MicroGrid] = {}
        self._transfers: Dict[UUID, EnergyTransfer] = {}
        self._forecasts: Dict[str, List[SolarForecast]] = {}  # zone_id -> forecasts

        # Metrics history
        self._metrics_history: List[EnergyMetrics] = []

        # Daily production tracking
        self._daily_production: Dict[str, Decimal] = {}  # zone_id -> kwh

        self._initialized = True
        logger.info("SymbioticEnergyAgent initialized - Energy flows like sunlight")

    # ========================================================================
    # NODE MANAGEMENT
    # ========================================================================

    def register_node(
        self,
        latitude: float,
        longitude: float,
        connection_type: ConnectionType,
        capacity_kw: Decimal,
        owner_id: UUID,
        energy_source: Optional[EnergySource] = None,
        azimuth_deg: float = 180,
        tilt_deg: float = 17,
        shading_factor: float = 1.0,
        storage_type: StorageType = StorageType.NONE,
        storage_capacity_kwh: Decimal = Decimal("0"),
    ) -> EnergyNode:
        """Register a new energy node (producer/consumer/prosumer)"""
        node_id = uuid4()
        zone_id = anonymize_location(latitude, longitude)

        orientation = None
        if energy_source == EnergySource.SOLAR:
            orientation = SolarOrientation(
                azimuth_deg=azimuth_deg,
                tilt_deg=tilt_deg,
                shading_factor=shading_factor,
            )

        node = EnergyNode(
            id=node_id,
            zone_id=zone_id,
            connection_type=connection_type,
            location=GeoPoint(latitude, longitude),
            capacity_kw=capacity_kw,
            current_output_kw=Decimal("0"),
            energy_source=energy_source,
            orientation=orientation,
            storage_type=storage_type,
            storage_capacity_kwh=storage_capacity_kwh,
            storage_level_kwh=Decimal("0"),
            owner_anon_id=anonymize_producer_id(owner_id),
            audit_log=[{
                "action": "registered",
                "timestamp": datetime.now().isoformat(),
            }],
        )

        self._nodes[node_id] = node

        # Auto-assign to grid
        self._assign_to_grid(node)

        logger.info(
            f"Node registered: {connection_type.value} "
            f"({capacity_kw}kW, source: {energy_source.value if energy_source else 'N/A'})"
        )

        return node

    def _assign_to_grid(self, node: EnergyNode) -> None:
        """Assign node to nearest micro-grid or create new one"""
        # Find existing grid in zone
        for grid in self._grids.values():
            if grid.zone_id == node.zone_id:
                grid.node_ids.append(node.id)
                self._update_grid_capacity(grid)
                return

        # Create new grid
        grid = MicroGrid(
            id=uuid4(),
            name=f"Grid {node.zone_id}",
            zone_id=node.zone_id,
            center=node.location,
            radius_km=0.5,
            node_ids=[node.id],
        )
        self._grids[grid.id] = grid
        self._update_grid_capacity(grid)

    def _update_grid_capacity(self, grid: MicroGrid) -> None:
        """Update grid totals from nodes"""
        total_capacity = Decimal("0")
        total_storage = Decimal("0")

        for node_id in grid.node_ids:
            if node_id in self._nodes:
                node = self._nodes[node_id]
                if node.connection_type in {ConnectionType.PRODUCER, ConnectionType.PROSUMER}:
                    total_capacity += node.capacity_kw
                total_storage += node.storage_capacity_kwh

        grid.total_capacity_kw = total_capacity
        grid.total_storage_kwh = total_storage

    # ========================================================================
    # READINGS & BALANCE
    # ========================================================================

    def record_reading(
        self,
        node_id: UUID,
        current_output_kw: Decimal,
        storage_level_kwh: Optional[Decimal] = None,
    ) -> EnergyNode:
        """Record current output/consumption reading"""
        if node_id not in self._nodes:
            raise ValueError(f"Node {node_id} not found")

        node = self._nodes[node_id]
        node.current_output_kw = current_output_kw
        node.last_reading = datetime.now()

        if storage_level_kwh is not None:
            node.storage_level_kwh = storage_level_kwh

        # Update daily production tracking
        if node.connection_type in {ConnectionType.PRODUCER, ConnectionType.PROSUMER}:
            if node.zone_id not in self._daily_production:
                self._daily_production[node.zone_id] = Decimal("0")
            # Add production for this hour (assuming hourly readings)
            self._daily_production[node.zone_id] += current_output_kw

        # Update grid balance
        self._update_grid_balance(node.zone_id)

        return node

    def _update_grid_balance(self, zone_id: str) -> None:
        """Update grid balance after readings"""
        for grid in self._grids.values():
            if grid.zone_id != zone_id:
                continue

            production = Decimal("0")
            consumption = Decimal("0")
            storage = Decimal("0")

            for node_id in grid.node_ids:
                if node_id not in self._nodes:
                    continue
                node = self._nodes[node_id]

                if node.connection_type == ConnectionType.PRODUCER:
                    production += node.current_output_kw
                elif node.connection_type == ConnectionType.CONSUMER:
                    consumption += node.current_output_kw
                elif node.connection_type == ConnectionType.PROSUMER:
                    if node.current_output_kw > 0:
                        production += node.current_output_kw
                    else:
                        consumption += abs(node.current_output_kw)

                storage += node.storage_level_kwh

            grid.current_production_kw = production
            grid.current_consumption_kw = consumption
            grid.current_storage_kwh = storage
            grid.balance_kw = production - consumption
            grid.last_update = datetime.now()

            # Update status
            if production == 0 and consumption == 0:
                grid.status = GridStatus.OFFLINE
            elif grid.balance_kw > Decimal("10"):
                grid.status = GridStatus.SURPLUS
            elif grid.balance_kw < Decimal("-10"):
                grid.status = GridStatus.DEFICIT
            else:
                grid.status = GridStatus.BALANCED

    def get_optimal_solar_output(
        self,
        node_id: UUID,
        time_of_day: Optional[TimeOfDay] = None,
    ) -> Dict[str, Any]:
        """Calculate optimal vs actual solar output"""
        if node_id not in self._nodes:
            raise ValueError(f"Node {node_id} not found")

        node = self._nodes[node_id]

        if node.energy_source != EnergySource.SOLAR or not node.orientation:
            return {"error": "Not a solar node"}

        # Time-based factor
        if time_of_day is None:
            hour = datetime.now().hour
            if 5 <= hour < 7:
                time_of_day = TimeOfDay.DAWN
            elif 7 <= hour < 12:
                time_of_day = TimeOfDay.MORNING
            elif 12 <= hour < 15:
                time_of_day = TimeOfDay.PEAK
            elif 15 <= hour < 18:
                time_of_day = TimeOfDay.AFTERNOON
            elif 18 <= hour < 20:
                time_of_day = TimeOfDay.DUSK
            else:
                time_of_day = TimeOfDay.NIGHT

        time_factors = {
            TimeOfDay.DAWN: 0.2,
            TimeOfDay.MORNING: 0.7,
            TimeOfDay.PEAK: 1.0,
            TimeOfDay.AFTERNOON: 0.8,
            TimeOfDay.DUSK: 0.3,
            TimeOfDay.NIGHT: 0.0,
        }

        time_factor = time_factors.get(time_of_day, 0.5)
        orientation_factor = node.orientation.efficiency_factor
        optimal_output = node.capacity_kw * Decimal(str(time_factor * orientation_factor))

        actual = node.current_output_kw
        efficiency = float(actual / optimal_output) if optimal_output > 0 else 0

        return {
            "node_id": str(node_id),
            "capacity_kw": float(node.capacity_kw),
            "optimal_output_kw": float(optimal_output),
            "actual_output_kw": float(actual),
            "efficiency_pct": round(efficiency * 100, 1),
            "orientation_factor": round(orientation_factor, 2),
            "time_of_day": time_of_day.value,
            "time_factor": time_factor,
            "recommendations": self._get_solar_recommendations(node, efficiency),
        }

    def _get_solar_recommendations(
        self,
        node: EnergyNode,
        efficiency: float,
    ) -> List[str]:
        """Generate recommendations for improving solar efficiency"""
        recs = []

        if not node.orientation:
            return recs

        if node.orientation.azimuth_deg < 150 or node.orientation.azimuth_deg > 210:
            recs.append("Consider adjusting azimuth closer to 180 (south)")

        if node.orientation.tilt_deg < 10 or node.orientation.tilt_deg > 25:
            recs.append("Optimal tilt for tropics is 15-20 degrees")

        if node.orientation.shading_factor < 0.9:
            recs.append("Reduce shading for improved output")

        if efficiency < 0.6:
            recs.append("Panel cleaning recommended")

        return recs

    # ========================================================================
    # ENERGY TRANSFERS
    # ========================================================================

    def request_transfer(
        self,
        from_grid_id: UUID,
        to_grid_id: UUID,
        amount_kwh: Decimal,
        duration_hours: float,
    ) -> EnergyTransfer:
        """
        Request energy transfer between grids

        GOVERNANCE: High power/large transfers require approval
        """
        if from_grid_id not in self._grids:
            raise ValueError(f"Source grid {from_grid_id} not found")
        if to_grid_id not in self._grids:
            raise ValueError(f"Destination grid {to_grid_id} not found")

        from_grid = self._grids[from_grid_id]
        to_grid = self._grids[to_grid_id]

        # Check source has surplus
        if from_grid.status != GridStatus.SURPLUS:
            raise ValueError("Source grid has no surplus to share")

        # Calculate power
        power_kw = amount_kwh / Decimal(str(duration_hours))

        # Determine if approval required
        requires_approval = (
            power_kw > HIGH_POWER_THRESHOLD_KW
            or amount_kwh > LARGE_TRANSFER_THRESHOLD_KWH
        )

        transfer = EnergyTransfer(
            id=uuid4(),
            from_grid_id=from_grid_id,
            to_grid_id=to_grid_id,
            amount_kwh=amount_kwh,
            duration_hours=duration_hours,
            power_kw=power_kw,
            started_at=datetime.now(),
            status="pending_approval" if requires_approval else "pending",
            requires_approval=requires_approval,
        )

        self._transfers[transfer.id] = transfer

        logger.info(
            f"Transfer requested: {amount_kwh}kWh from {from_grid.name} to {to_grid.name} "
            f"(requires_approval: {requires_approval})"
        )

        return transfer

    def approve_transfer(
        self,
        transfer_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> EnergyTransfer:
        """
        GOVERNANCE GATE: Approve high-power transfer

        RULE #1: Human approval for significant transfers
        """
        if transfer_id not in self._transfers:
            raise ValueError(f"Transfer {transfer_id} not found")

        transfer = self._transfers[transfer_id]

        if transfer.status != "pending_approval":
            raise ValueError(f"Transfer not pending approval (status: {transfer.status})")

        transfer.status = "approved"
        transfer.approved_by = approver_name
        transfer.approved_at = datetime.now()

        logger.info(f"GOVERNANCE: Transfer {transfer_id} approved by {approver_name}")

        return transfer

    def start_transfer(self, transfer_id: UUID) -> EnergyTransfer:
        """Start an approved transfer"""
        if transfer_id not in self._transfers:
            raise ValueError(f"Transfer {transfer_id} not found")

        transfer = self._transfers[transfer_id]

        if transfer.status not in {"pending", "approved"}:
            raise ValueError(f"Cannot start transfer (status: {transfer.status})")

        if transfer.requires_approval and not transfer.approved_by:
            raise ValueError("Transfer requires approval before starting")

        transfer.status = "in_progress"
        transfer.started_at = datetime.now()

        return transfer

    def complete_transfer(self, transfer_id: UUID) -> EnergyTransfer:
        """Complete a transfer"""
        if transfer_id not in self._transfers:
            raise ValueError(f"Transfer {transfer_id} not found")

        transfer = self._transfers[transfer_id]

        if transfer.status != "in_progress":
            raise ValueError(f"Transfer not in progress (status: {transfer.status})")

        transfer.status = "completed"
        transfer.completed_at = datetime.now()

        return transfer

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_grids(
        self,
        status: Optional[GridStatus] = None,
    ) -> List[MicroGrid]:
        """
        Get all micro-grids

        GOVERNANCE RULE #5: Alphabetical by name
        """
        grids = list(self._grids.values())

        if status:
            grids = [g for g in grids if g.status == status]

        # RULE #5: ALPHABETICAL order
        grids.sort(key=lambda g: g.name.lower())

        return grids

    def get_nodes(
        self,
        zone_id: Optional[str] = None,
        connection_type: Optional[ConnectionType] = None,
        energy_source: Optional[EnergySource] = None,
    ) -> List[EnergyNode]:
        """
        Get nodes with filters

        GOVERNANCE RULE #5: Alphabetical by zone
        """
        nodes = list(self._nodes.values())

        if zone_id:
            nodes = [n for n in nodes if n.zone_id == zone_id]
        if connection_type:
            nodes = [n for n in nodes if n.connection_type == connection_type]
        if energy_source:
            nodes = [n for n in nodes if n.energy_source == energy_source]

        # ALPHABETICAL by zone
        nodes.sort(key=lambda n: n.zone_id)

        return nodes

    def get_transfers(
        self,
        status: Optional[str] = None,
    ) -> List[EnergyTransfer]:
        """
        Get transfers

        GOVERNANCE RULE #5: Chronological order
        """
        transfers = list(self._transfers.values())

        if status:
            transfers = [t for t in transfers if t.status == status]

        # CHRONOLOGICAL order
        transfers.sort(key=lambda t: t.started_at)

        return transfers

    def get_grid_status(self, grid_id: UUID) -> Dict[str, Any]:
        """Get detailed grid status"""
        if grid_id not in self._grids:
            raise ValueError(f"Grid {grid_id} not found")

        grid = self._grids[grid_id]

        return {
            "grid_id": str(grid_id),
            "name": grid.name,
            "status": grid.status.value,
            "nodes_count": len(grid.node_ids),
            "total_capacity_kw": float(grid.total_capacity_kw),
            "total_storage_kwh": float(grid.total_storage_kwh),
            "current_production_kw": float(grid.current_production_kw),
            "current_consumption_kw": float(grid.current_consumption_kw),
            "current_storage_kwh": float(grid.current_storage_kwh),
            "balance_kw": float(grid.balance_kw),
            "last_update": grid.last_update.isoformat(),
            "self_sufficient": grid.balance_kw >= 0,
        }

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_energy_metrics(self) -> EnergyMetrics:
        """Get current energy metrics"""
        now = datetime.now()

        # Production totals
        total_production = sum(self._daily_production.values())
        solar_production = Decimal("0")
        for node in self._nodes.values():
            if node.energy_source == EnergySource.SOLAR:
                # Estimate from capacity and time
                solar_production += node.capacity_kw * Decimal("0.2")  # 20% capacity factor

        # Consumption (sum of current consumption)
        total_consumption = sum(
            g.current_consumption_kw for g in self._grids.values()
        )

        # Self-sufficiency
        if total_consumption > 0:
            self_sufficiency = float(
                min(total_production, total_consumption) / total_consumption * 100
            )
        else:
            self_sufficiency = 100.0

        # Grid counts
        grids = list(self._grids.values())
        active = len([g for g in grids if g.status != GridStatus.OFFLINE])
        balanced = len([g for g in grids if g.status == GridStatus.BALANCED])
        surplus = len([g for g in grids if g.status == GridStatus.SURPLUS])
        deficit = len([g for g in grids if g.status == GridStatus.DEFICIT])

        # Calculate transfers
        completed = [t for t in self._transfers.values() if t.status == "completed"]
        surplus_shared = sum(t.amount_kwh for t in completed)

        # Symbiosis index (how much energy is shared locally)
        if total_production > 0:
            symbiosis = float(surplus_shared / total_production)
        else:
            symbiosis = 0.0

        # Solar efficiency (actual vs optimal)
        solar_nodes = [n for n in self._nodes.values() if n.energy_source == EnergySource.SOLAR]
        if solar_nodes:
            efficiencies = []
            for node in solar_nodes:
                if node.orientation:
                    efficiencies.append(node.orientation.efficiency_factor)
            solar_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        else:
            solar_efficiency = 0

        metrics = EnergyMetrics(
            timestamp=now,
            total_production_kwh=total_production,
            solar_production_kwh=solar_production,
            other_renewable_kwh=total_production - solar_production,
            total_consumption_kwh=total_consumption,
            self_sufficiency_pct=self_sufficiency,
            surplus_shared_kwh=surplus_shared,
            deficit_received_kwh=Decimal("0"),  # Would need tracking
            active_grids=active,
            grids_balanced=balanced,
            grids_surplus=surplus,
            grids_deficit=deficit,
            symbiosis_index=min(symbiosis, 1.0),
            solar_efficiency_index=solar_efficiency,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_energy_indices(self) -> Dict[str, float]:
        """Get energy indices for dashboard"""
        metrics = self.get_energy_metrics()

        return {
            "symbiosis_index": round(metrics.symbiosis_index, 3),
            "solar_efficiency_index": round(metrics.solar_efficiency_index, 3),
            "self_sufficiency_pct": round(metrics.self_sufficiency_pct / 100, 3),
            "grid_balance": round(
                metrics.grids_balanced / max(metrics.active_grids, 1), 3
            ),
            "renewable_ratio": round(
                float(metrics.solar_production_kwh / max(metrics.total_production_kwh, Decimal("1"))),
                3
            ),
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_symbiotic_energy_agent() -> SymbioticEnergyAgent:
    """Get the singleton SymbioticEnergyAgent instance"""
    return SymbioticEnergyAgent()
