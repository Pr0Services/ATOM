"""
CHE·NU V68 Circular Economy Agent
Module Environnement 4/4 - Economie Circulaire

CONCEPT: Economie Circulaire
- Tracabilite complete des materiaux
- Zero dechet comme objectif
- Recyclage et upcycling
- Symbiose industrielle locale

PHILOSOPHIE:
Il n'y a pas de dechet dans la nature - seulement des ressources mal placees.
Chaque fin est un nouveau debut.

PRIVACY:
- Entreprises anonymisees par categorie
- Pas de tracking des individus
- Focus sur les flux, pas les acteurs

GOVERNANCE COMPLIANCE:
- Rule #1: Flux toxiques require APPROVAL
- Rule #5: Materiaux ALPHABETICAL
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

def anonymize_actor_id(actor_id: UUID) -> str:
    """Anonymize business/actor ID"""
    salt = "CHENU_CIRCULAR_CYCLE_999Hz"
    return hashlib.sha256(f"{salt}{str(actor_id)}{salt}".encode()).hexdigest()[:16]


def anonymize_zone(latitude: float, longitude: float) -> str:
    """Anonymize location to industrial zone"""
    lat_zone = round(latitude, 2)
    lon_zone = round(longitude, 2)
    return f"industrial_zone_{lat_zone}_{lon_zone}"


# ============================================================================
# ENUMS
# ============================================================================

class MaterialCategory(Enum):
    """Categories de materiaux"""
    ORGANIC = "organic"              # Organique (compostable)
    METAL = "metal"                  # Metaux
    PLASTIC = "plastic"              # Plastiques
    GLASS = "glass"                  # Verre
    PAPER = "paper"                  # Papier/carton
    TEXTILE = "textile"              # Textiles
    ELECTRONIC = "electronic"        # Electronique
    CONSTRUCTION = "construction"    # Construction/demolition
    CHEMICAL = "chemical"            # Chimique
    HAZARDOUS = "hazardous"          # Dangereux


class MaterialState(Enum):
    """Etat du materiau"""
    RAW = "raw"                      # Brut
    PROCESSED = "processed"          # Transforme
    PRODUCT = "product"              # Produit fini
    USED = "used"                    # Utilise
    WASTE = "waste"                  # Dechet
    RECYCLED = "recycled"            # Recycle
    COMPOSTED = "composted"          # Composte
    UPCYCLED = "upcycled"            # Surcycle


class FlowType(Enum):
    """Type de flux"""
    INPUT = "input"                  # Entree
    OUTPUT = "output"                # Sortie
    INTERNAL = "internal"            # Interne
    EXCHANGE = "exchange"            # Echange entre acteurs
    RETURN = "return"                # Retour (reverse logistics)


class ProcessType(Enum):
    """Types de processus"""
    COLLECTION = "collection"        # Collecte
    SORTING = "sorting"              # Tri
    CLEANING = "cleaning"            # Nettoyage
    SHREDDING = "shredding"          # Broyage
    MELTING = "melting"              # Fusion
    COMPOSTING = "composting"        # Compostage
    REPAIR = "repair"                # Reparation
    REFURBISHMENT = "refurbishment"  # Reconditionnement
    UPCYCLING = "upcycling"          # Surcyclage


class ActorType(Enum):
    """Types d'acteurs"""
    PRODUCER = "producer"            # Producteur
    CONSUMER = "consumer"            # Consommateur
    COLLECTOR = "collector"          # Collecteur
    RECYCLER = "recycler"            # Recycleur
    REFURBISHER = "refurbisher"      # Reconditionneur
    COMPOSTER = "composter"          # Composteur
    RESELLER = "reseller"            # Revendeur
    EXCHANGE = "exchange"            # Plateforme d'echange


class SymbiosisType(Enum):
    """Types de symbiose industrielle"""
    BYPRODUCT_EXCHANGE = "byproduct_exchange"  # Echange de sous-produits
    ENERGY_CASCADE = "energy_cascade"          # Cascade energetique
    WATER_REUSE = "water_reuse"                # Reutilisation de l'eau
    SHARED_INFRASTRUCTURE = "shared_infrastructure"  # Infrastructure partagee
    LOGISTICS_SHARING = "logistics_sharing"    # Logistique partagee


class CircularityLevel(Enum):
    """Niveau de circularite"""
    LINEAR = "linear"                # Lineaire (extraire-produire-jeter)
    RECYCLING = "recycling"          # Recyclage basique
    EXTENDED = "extended"            # Vie prolongee (reparation)
    REGENERATIVE = "regenerative"    # Regeneratif (upcycling)
    RESTORATIVE = "restorative"      # Restauratif (symbiose complete)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Material:
    """Materiau tracable"""
    id: UUID
    name: str
    category: MaterialCategory
    state: MaterialState

    # Composition
    composition: Dict[str, float]  # element -> percentage
    recyclable: bool
    compostable: bool
    hazardous: bool

    # Circular properties
    recycled_content_pct: float
    recyclability_rate: float
    lifespan_years: float

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MaterialFlow:
    """Flux de materiau"""
    id: UUID
    material_id: UUID
    flow_type: FlowType

    # Quantity
    quantity_kg: Decimal
    timestamp: datetime

    # From/To (anonymized)
    from_actor_anon: str
    to_actor_anon: str
    from_zone: str
    to_zone: str

    # Traceability
    batch_id: str = ""
    origin_verified: bool = False

    # GOVERNANCE
    requires_approval: bool = False  # For hazardous
    approved_by: Optional[str] = None


@dataclass
class Actor:
    """Acteur economique (anonymise)"""
    id: UUID
    anon_id: str
    actor_type: ActorType
    zone_id: str

    # Capabilities
    materials_handled: List[MaterialCategory]
    processes: List[ProcessType]

    # Capacity
    monthly_capacity_kg: Decimal
    current_utilization_pct: float

    # Circularity
    circularity_level: CircularityLevel
    waste_diversion_rate: float  # % detourne de la decharge


@dataclass
class SymbiosisConnection:
    """Connexion de symbiose industrielle"""
    id: UUID
    symbiosis_type: SymbiosisType

    # Partners (anonymized)
    provider_anon: str
    receiver_anon: str

    # Flow
    material_category: MaterialCategory
    monthly_volume_kg: Decimal

    # Benefits
    waste_avoided_kg: Decimal
    cost_savings: Decimal
    co2_avoided_kg: Decimal

    # Status
    active: bool = True
    since: datetime = field(default_factory=datetime.now)


@dataclass
class RecyclingLoop:
    """Boucle de recyclage"""
    id: UUID
    name: str
    material_category: MaterialCategory

    # Chain
    stages: List[ProcessType]
    actors_involved: int

    # Performance
    recovery_rate: float           # % materiau recupere
    quality_retention: float       # % qualite maintenue
    loops_possible: int            # Nombre de cycles possibles

    # Zone
    zone_ids: List[str]
    local_percentage: float        # % traite localement


@dataclass
class WasteAudit:
    """Audit des dechets"""
    id: UUID
    zone_id: str
    period_start: datetime
    period_end: datetime

    # Totals
    total_waste_kg: Decimal
    recycled_kg: Decimal
    composted_kg: Decimal
    landfill_kg: Decimal
    incinerated_kg: Decimal

    # By category
    breakdown_by_category: Dict[str, Decimal]

    # Metrics
    diversion_rate: float          # % detourne
    recycling_rate: float
    composting_rate: float


@dataclass
class CircularMetrics:
    """Metriques de circularite"""
    timestamp: datetime

    # Volume
    total_material_flow_kg: Decimal
    virgin_material_kg: Decimal
    recycled_input_kg: Decimal

    # Outputs
    products_kg: Decimal
    recycled_output_kg: Decimal
    composted_kg: Decimal
    waste_to_landfill_kg: Decimal

    # Actors
    active_actors: int
    symbiosis_connections: int

    # Indices
    circularity_index: float       # 0-1
    waste_diversion_rate: float    # 0-1
    local_loop_rate: float         # 0-1 (% boucle locale)
    material_efficiency: float     # 0-1


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Categories requiring approval for flows
HAZARDOUS_CATEGORIES = {MaterialCategory.HAZARDOUS, MaterialCategory.CHEMICAL}

# Quantity threshold requiring approval (kg)
LARGE_FLOW_THRESHOLD_KG = Decimal("1000")


# ============================================================================
# CIRCULAR ECONOMY AGENT
# ============================================================================

class CircularEconomyAgent:
    """
    Agent d'Economie Circulaire

    Les cycles de la matiere:
    - Rien ne se perd, tout se transforme
    - Le dechet de l'un est la ressource de l'autre
    - La boucle locale est la plus forte

    Mission: Tracer, connecter, boucler
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
        self._materials: Dict[UUID, Material] = {}
        self._flows: Dict[UUID, MaterialFlow] = {}
        self._actors: Dict[UUID, Actor] = {}
        self._symbioses: Dict[UUID, SymbiosisConnection] = {}
        self._loops: Dict[UUID, RecyclingLoop] = {}
        self._audits: Dict[UUID, WasteAudit] = {}

        # Zone tracking
        self._zone_flows: Dict[str, List[UUID]] = {}  # zone_id -> flow_ids

        # Metrics history
        self._metrics_history: List[CircularMetrics] = []

        self._initialized = True
        logger.info("CircularEconomyAgent initialized - Closing the Loop")

        # Initialize common materials
        self._init_materials()

    def _init_materials(self) -> None:
        """Initialize common tracked materials"""
        common_materials = [
            ("PET Plastic", MaterialCategory.PLASTIC, True, False, False, 0.7, 3.0),
            ("HDPE Plastic", MaterialCategory.PLASTIC, True, False, False, 0.8, 5.0),
            ("Aluminum", MaterialCategory.METAL, True, False, False, 0.95, 50.0),
            ("Steel", MaterialCategory.METAL, True, False, False, 0.9, 30.0),
            ("Glass", MaterialCategory.GLASS, True, False, False, 0.99, 100.0),
            ("Cardboard", MaterialCategory.PAPER, True, True, False, 0.7, 1.0),
            ("Organic Waste", MaterialCategory.ORGANIC, False, True, False, 0.0, 0.5),
            ("E-Waste", MaterialCategory.ELECTRONIC, True, False, True, 0.3, 5.0),
            ("Construction Debris", MaterialCategory.CONSTRUCTION, True, False, False, 0.6, 10.0),
            ("Textiles", MaterialCategory.TEXTILE, True, False, False, 0.4, 3.0),
        ]

        for name, category, recyclable, compostable, hazardous, rate, lifespan in common_materials:
            self.register_material(
                name=name,
                category=category,
                composition={},
                recyclable=recyclable,
                compostable=compostable,
                hazardous=hazardous,
                recyclability_rate=rate,
                lifespan_years=lifespan,
            )

    # ========================================================================
    # MATERIAL MANAGEMENT
    # ========================================================================

    def register_material(
        self,
        name: str,
        category: MaterialCategory,
        composition: Dict[str, float],
        recyclable: bool,
        compostable: bool,
        hazardous: bool,
        recyclability_rate: float,
        lifespan_years: float,
        recycled_content_pct: float = 0.0,
    ) -> Material:
        """Register a new material for tracking"""
        material_id = uuid4()

        material = Material(
            id=material_id,
            name=name,
            category=category,
            state=MaterialState.RAW,
            composition=composition,
            recyclable=recyclable,
            compostable=compostable,
            hazardous=hazardous,
            recycled_content_pct=recycled_content_pct,
            recyclability_rate=recyclability_rate,
            lifespan_years=lifespan_years,
        )

        self._materials[material_id] = material

        logger.info(f"Material registered: {name} ({category.value})")

        return material

    # ========================================================================
    # ACTOR MANAGEMENT
    # ========================================================================

    def register_actor(
        self,
        actor_id: UUID,
        actor_type: ActorType,
        latitude: float,
        longitude: float,
        materials_handled: List[MaterialCategory],
        processes: List[ProcessType],
        monthly_capacity_kg: Decimal,
        circularity_level: CircularityLevel = CircularityLevel.RECYCLING,
        waste_diversion_rate: float = 0.5,
    ) -> Actor:
        """Register an economic actor (anonymized)"""
        anon_id = anonymize_actor_id(actor_id)
        zone_id = anonymize_zone(latitude, longitude)

        actor = Actor(
            id=uuid4(),
            anon_id=anon_id,
            actor_type=actor_type,
            zone_id=zone_id,
            materials_handled=materials_handled,
            processes=processes,
            monthly_capacity_kg=monthly_capacity_kg,
            current_utilization_pct=0.0,
            circularity_level=circularity_level,
            waste_diversion_rate=waste_diversion_rate,
        )

        self._actors[actor.id] = actor

        logger.info(f"Actor registered: {actor_type.value} in {zone_id}")

        return actor

    # ========================================================================
    # MATERIAL FLOWS
    # ========================================================================

    def record_flow(
        self,
        material_id: UUID,
        flow_type: FlowType,
        quantity_kg: Decimal,
        from_actor_id: UUID,
        to_actor_id: UUID,
        from_latitude: float,
        from_longitude: float,
        to_latitude: float,
        to_longitude: float,
        batch_id: str = "",
        origin_verified: bool = False,
    ) -> MaterialFlow:
        """
        Record a material flow

        GOVERNANCE: Hazardous or large flows require approval
        """
        if material_id not in self._materials:
            raise ValueError(f"Material {material_id} not found")

        material = self._materials[material_id]

        # PRIVACY: Anonymize actors and locations
        from_anon = anonymize_actor_id(from_actor_id)
        to_anon = anonymize_actor_id(to_actor_id)
        from_zone = anonymize_zone(from_latitude, from_longitude)
        to_zone = anonymize_zone(to_latitude, to_longitude)

        # Check if approval required
        requires_approval = (
            material.category in HAZARDOUS_CATEGORIES
            or material.hazardous
            or quantity_kg > LARGE_FLOW_THRESHOLD_KG
        )

        flow = MaterialFlow(
            id=uuid4(),
            material_id=material_id,
            flow_type=flow_type,
            quantity_kg=quantity_kg,
            timestamp=datetime.now(),
            from_actor_anon=from_anon,
            to_actor_anon=to_anon,
            from_zone=from_zone,
            to_zone=to_zone,
            batch_id=batch_id,
            origin_verified=origin_verified,
            requires_approval=requires_approval,
        )

        self._flows[flow.id] = flow

        # Track by zone
        for zone in [from_zone, to_zone]:
            if zone not in self._zone_flows:
                self._zone_flows[zone] = []
            self._zone_flows[zone].append(flow.id)

        logger.info(
            f"Flow recorded: {material.name} {quantity_kg}kg "
            f"({flow_type.value}, requires_approval: {requires_approval})"
        )

        return flow

    def approve_flow(
        self,
        flow_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> MaterialFlow:
        """
        GOVERNANCE GATE: Approve hazardous/large flow

        RULE #1: Human approval for sensitive materials
        """
        if flow_id not in self._flows:
            raise ValueError(f"Flow {flow_id} not found")

        flow = self._flows[flow_id]

        if not flow.requires_approval:
            raise ValueError("Flow does not require approval")

        flow.approved_by = approver_name

        logger.info(f"GOVERNANCE: Flow {flow_id} approved by {approver_name}")

        return flow

    # ========================================================================
    # SYMBIOSIS
    # ========================================================================

    def create_symbiosis(
        self,
        symbiosis_type: SymbiosisType,
        provider_actor_id: UUID,
        receiver_actor_id: UUID,
        material_category: MaterialCategory,
        monthly_volume_kg: Decimal,
        waste_avoided_kg: Decimal,
        cost_savings: Decimal,
        co2_avoided_kg: Decimal,
    ) -> SymbiosisConnection:
        """Create an industrial symbiosis connection"""
        symbiosis = SymbiosisConnection(
            id=uuid4(),
            symbiosis_type=symbiosis_type,
            provider_anon=anonymize_actor_id(provider_actor_id),
            receiver_anon=anonymize_actor_id(receiver_actor_id),
            material_category=material_category,
            monthly_volume_kg=monthly_volume_kg,
            waste_avoided_kg=waste_avoided_kg,
            cost_savings=cost_savings,
            co2_avoided_kg=co2_avoided_kg,
        )

        self._symbioses[symbiosis.id] = symbiosis

        logger.info(
            f"Symbiosis created: {symbiosis_type.value} - "
            f"{material_category.value} ({monthly_volume_kg}kg/month)"
        )

        return symbiosis

    def register_recycling_loop(
        self,
        name: str,
        material_category: MaterialCategory,
        stages: List[ProcessType],
        actors_involved: int,
        recovery_rate: float,
        quality_retention: float,
        loops_possible: int,
        zone_ids: List[str],
        local_percentage: float,
    ) -> RecyclingLoop:
        """Register a complete recycling loop"""
        loop = RecyclingLoop(
            id=uuid4(),
            name=name,
            material_category=material_category,
            stages=stages,
            actors_involved=actors_involved,
            recovery_rate=recovery_rate,
            quality_retention=quality_retention,
            loops_possible=loops_possible,
            zone_ids=zone_ids,
            local_percentage=local_percentage,
        )

        self._loops[loop.id] = loop

        return loop

    # ========================================================================
    # AUDITS
    # ========================================================================

    def create_waste_audit(
        self,
        zone_id: str,
        period_start: datetime,
        period_end: datetime,
        total_waste_kg: Decimal,
        recycled_kg: Decimal,
        composted_kg: Decimal,
        landfill_kg: Decimal,
        incinerated_kg: Decimal,
        breakdown_by_category: Dict[str, Decimal],
    ) -> WasteAudit:
        """Create a waste audit for a zone"""
        diversion_rate = float(
            (recycled_kg + composted_kg) / total_waste_kg
        ) if total_waste_kg > 0 else 0

        recycling_rate = float(
            recycled_kg / total_waste_kg
        ) if total_waste_kg > 0 else 0

        composting_rate = float(
            composted_kg / total_waste_kg
        ) if total_waste_kg > 0 else 0

        audit = WasteAudit(
            id=uuid4(),
            zone_id=zone_id,
            period_start=period_start,
            period_end=period_end,
            total_waste_kg=total_waste_kg,
            recycled_kg=recycled_kg,
            composted_kg=composted_kg,
            landfill_kg=landfill_kg,
            incinerated_kg=incinerated_kg,
            breakdown_by_category=breakdown_by_category,
            diversion_rate=diversion_rate,
            recycling_rate=recycling_rate,
            composting_rate=composting_rate,
        )

        self._audits[audit.id] = audit

        return audit

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_materials(
        self,
        category: Optional[MaterialCategory] = None,
        recyclable: Optional[bool] = None,
    ) -> List[Material]:
        """
        Get materials with optional filters

        GOVERNANCE RULE #5: ALPHABETICAL by name
        """
        materials = list(self._materials.values())

        if category:
            materials = [m for m in materials if m.category == category]
        if recyclable is not None:
            materials = [m for m in materials if m.recyclable == recyclable]

        # RULE #5: ALPHABETICAL order
        materials.sort(key=lambda m: m.name.lower())

        return materials

    def get_flows(
        self,
        zone_id: Optional[str] = None,
        flow_type: Optional[FlowType] = None,
        since: Optional[datetime] = None,
    ) -> List[MaterialFlow]:
        """
        Get material flows

        GOVERNANCE RULE #5: Chronological order
        """
        if zone_id and zone_id in self._zone_flows:
            flow_ids = self._zone_flows[zone_id]
            flows = [self._flows[fid] for fid in flow_ids if fid in self._flows]
        else:
            flows = list(self._flows.values())

        if flow_type:
            flows = [f for f in flows if f.flow_type == flow_type]
        if since:
            flows = [f for f in flows if f.timestamp >= since]

        # CHRONOLOGICAL order
        flows.sort(key=lambda f: f.timestamp)

        return flows

    def get_actors(
        self,
        actor_type: Optional[ActorType] = None,
        zone_id: Optional[str] = None,
    ) -> List[Actor]:
        """
        Get actors with filters

        GOVERNANCE RULE #5: Alphabetical by zone
        """
        actors = list(self._actors.values())

        if actor_type:
            actors = [a for a in actors if a.actor_type == actor_type]
        if zone_id:
            actors = [a for a in actors if a.zone_id == zone_id]

        # ALPHABETICAL by zone
        actors.sort(key=lambda a: a.zone_id)

        return actors

    def get_symbioses(
        self,
        material_category: Optional[MaterialCategory] = None,
        active_only: bool = True,
    ) -> List[SymbiosisConnection]:
        """Get symbiosis connections"""
        symbioses = list(self._symbioses.values())

        if material_category:
            symbioses = [s for s in symbioses if s.material_category == material_category]
        if active_only:
            symbioses = [s for s in symbioses if s.active]

        return symbioses

    def get_material_journey(self, batch_id: str) -> List[MaterialFlow]:
        """Trace the journey of a material batch"""
        flows = [f for f in self._flows.values() if f.batch_id == batch_id]
        flows.sort(key=lambda f: f.timestamp)
        return flows

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_circular_metrics(self) -> CircularMetrics:
        """Get current circularity metrics"""
        now = datetime.now()
        month_ago = now - timedelta(days=30)

        # Calculate flows
        recent_flows = [f for f in self._flows.values() if f.timestamp >= month_ago]

        total_flow = sum(f.quantity_kg for f in recent_flows)

        # Estimate virgin vs recycled (based on material properties)
        virgin = Decimal("0")
        recycled_input = Decimal("0")
        recycled_output = Decimal("0")
        composted = Decimal("0")
        landfill = Decimal("0")
        products = Decimal("0")

        for flow in recent_flows:
            material = self._materials.get(flow.material_id)
            if not material:
                continue

            if flow.flow_type == FlowType.INPUT:
                if material.state == MaterialState.RECYCLED:
                    recycled_input += flow.quantity_kg
                else:
                    virgin += flow.quantity_kg
            elif flow.flow_type == FlowType.OUTPUT:
                if material.state == MaterialState.PRODUCT:
                    products += flow.quantity_kg
                elif material.state == MaterialState.RECYCLED:
                    recycled_output += flow.quantity_kg
                elif material.state == MaterialState.COMPOSTED:
                    composted += flow.quantity_kg
                elif material.state == MaterialState.WASTE:
                    landfill += flow.quantity_kg

        # Actor counts
        active_actors = len(self._actors)
        symbiosis_count = len([s for s in self._symbioses.values() if s.active])

        # Calculate indices

        # Circularity index
        if total_flow > 0:
            circularity = float(
                (recycled_input + recycled_output + composted) / total_flow
            )
        else:
            circularity = 0

        # Waste diversion
        total_output = recycled_output + composted + landfill
        if total_output > 0:
            diversion = float((recycled_output + composted) / total_output)
        else:
            diversion = 0

        # Local loop rate (from recycling loops)
        loops = list(self._loops.values())
        if loops:
            local_loop = sum(l.local_percentage for l in loops) / len(loops)
        else:
            local_loop = 0

        # Material efficiency
        if virgin + recycled_input > 0:
            efficiency = float(products / (virgin + recycled_input))
        else:
            efficiency = 0

        metrics = CircularMetrics(
            timestamp=now,
            total_material_flow_kg=total_flow,
            virgin_material_kg=virgin,
            recycled_input_kg=recycled_input,
            products_kg=products,
            recycled_output_kg=recycled_output,
            composted_kg=composted,
            waste_to_landfill_kg=landfill,
            active_actors=active_actors,
            symbiosis_connections=symbiosis_count,
            circularity_index=min(circularity, 1.0),
            waste_diversion_rate=min(diversion, 1.0),
            local_loop_rate=local_loop,
            material_efficiency=min(efficiency, 1.0),
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_circular_indices(self) -> Dict[str, float]:
        """Get circularity indices for dashboard"""
        metrics = self.get_circular_metrics()

        return {
            "circularity_index": round(metrics.circularity_index, 3),
            "waste_diversion_rate": round(metrics.waste_diversion_rate, 3),
            "local_loop_rate": round(metrics.local_loop_rate, 3),
            "material_efficiency": round(metrics.material_efficiency, 3),
            "symbiosis_density": round(
                metrics.symbiosis_connections / max(metrics.active_actors, 1), 3
            ),
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_circular_economy_agent() -> CircularEconomyAgent:
    """Get the singleton CircularEconomyAgent instance"""
    return CircularEconomyAgent()
