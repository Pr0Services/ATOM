"""
CHE·NU V68 Resource Balance Agent (Equilibre des Ressources)
Module Societaire 1/4 - Le Don & Le Partage

CONCEPT: Economie de flux, pas de manque
- Scanner les surplus (nourriture, materiaux, competences)
- Connecter instantanement aux besoins locaux
- Zero gaspillage

PRIVACY FIRST (Agents Gardiens):
- Les agents voient le "besoin", pas "l'identite"
- Donnees anonymisees par defaut
- Pas de tracking individuel - seulement flux agreges

GOVERNANCE COMPLIANCE:
- Rule #1: Redistribution haute valeur require APPROVAL
- Rule #5: Resources ALPHABETICAL, Needs CHRONOLOGICAL
- Rule #6: Full audit trail (anonymized)

Objectif: Si un hotel a Tulum a un surplus, l'agent le redirige
vers un centre communautaire avant que cela devienne un dechet.
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
# ENUMS
# ============================================================================

class ResourceCategory(Enum):
    """Categories de ressources"""
    FOOD = "food"                    # Nourriture
    MATERIALS = "materials"          # Materiaux de construction
    EQUIPMENT = "equipment"          # Equipements, outils
    CLOTHING = "clothing"            # Vetements
    FURNITURE = "furniture"          # Meubles
    ELECTRONICS = "electronics"      # Electronique
    SKILLS = "skills"                # Competences humaines
    TIME = "time"                    # Temps benevole
    SPACE = "space"                  # Espaces disponibles
    TRANSPORT = "transport"          # Capacite de transport


class ResourceCondition(Enum):
    """Condition de la ressource"""
    NEW = "new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_REPAIR = "needs_repair"


class ResourceStatus(Enum):
    """Statut de la ressource"""
    AVAILABLE = "available"          # Disponible
    RESERVED = "reserved"            # Reserve pour un besoin
    IN_TRANSIT = "in_transit"        # En cours de transfert
    DELIVERED = "delivered"          # Livre
    EXPIRED = "expired"              # Expire (nourriture)
    WITHDRAWN = "withdrawn"          # Retire par le donateur


class NeedUrgency(Enum):
    """Urgence du besoin"""
    CRITICAL = "critical"            # Besoin immediat vital
    HIGH = "high"                    # Besoin urgent
    MEDIUM = "medium"                # Besoin modere
    LOW = "low"                      # Besoin non urgent


class NeedStatus(Enum):
    """Statut du besoin"""
    OPEN = "open"                    # Ouvert, cherche ressource
    MATCHED = "matched"              # Match trouve
    PENDING_APPROVAL = "pending_approval"  # GOVERNANCE
    FULFILLED = "fulfilled"          # Satisfait
    CANCELLED = "cancelled"          # Annule
    EXPIRED = "expired"              # Expire sans match


class MatchStatus(Enum):
    """Statut du match ressource-besoin"""
    SUGGESTED = "suggested"          # Suggere par l'agent
    PENDING_DONOR = "pending_donor"  # En attente confirmation donateur
    PENDING_RECEIVER = "pending_receiver"  # En attente confirmation receveur
    PENDING_APPROVAL = "pending_approval"  # GOVERNANCE pour haute valeur
    CONFIRMED = "confirmed"          # Confirme des deux cotes
    IN_TRANSIT = "in_transit"        # Transfert en cours
    COMPLETED = "completed"          # Termine
    CANCELLED = "cancelled"          # Annule


class DonorType(Enum):
    """Type de donateur (anonymise)"""
    BUSINESS = "business"            # Hotel, restaurant, entreprise
    COMMUNITY_ORG = "community_org"  # Organisation communautaire
    INDIVIDUAL = "individual"        # Particulier (anonyme)
    GOVERNMENT = "government"        # Institution publique
    FARM = "farm"                    # Ferme, producteur


class ReceiverType(Enum):
    """Type de receveur (anonymise)"""
    COMMUNITY_CENTER = "community_center"
    SHELTER = "shelter"
    FOOD_BANK = "food_bank"
    SCHOOL = "school"
    FAMILY = "family"                # Anonyme
    INDIVIDUAL = "individual"        # Anonyme
    NGO = "ngo"


# ============================================================================
# PRIVACY HELPERS
# ============================================================================

def anonymize_id(original_id: UUID) -> str:
    """
    PRIVACY: Anonymize ID for tracking without identification
    Returns a hash that cannot be reversed to original ID
    """
    # Add salt for extra security
    salt = "CHENU_PRIVACY_SALT_999Hz"
    combined = f"{salt}{str(original_id)}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def anonymize_location(lat: float, lon: float, precision: int = 2) -> tuple:
    """
    PRIVACY: Reduce location precision to area level
    precision=2 gives ~1km accuracy
    """
    return (round(lat, precision), round(lon, precision))


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoArea:
    """Zone geographique (precision reduite pour privacy)"""
    latitude: float
    longitude: float
    radius_km: float
    name: Optional[str] = None

    def __post_init__(self):
        # PRIVACY: Reduce precision automatically
        self.latitude, self.longitude = anonymize_location(
            self.latitude, self.longitude
        )


@dataclass
class Resource:
    """Ressource disponible (surplus)"""
    id: UUID
    resource_number: str              # RES-001
    category: ResourceCategory
    subcategory: str                  # Ex: "pain", "legumes"
    description: str
    quantity: float
    unit: str                         # kg, pieces, hours
    condition: ResourceCondition
    status: ResourceStatus

    # Localisation (anonymisee)
    area: GeoArea

    # Donateur (anonymise)
    donor_type: DonorType
    donor_hash: str                   # Anonymized ID

    # Validite
    available_from: datetime
    available_until: Optional[datetime]  # Expiration
    perishable: bool

    # Valeur estimee (pour governance haute valeur)
    estimated_value: Decimal

    # Audit (sans identite)
    created_at: datetime
    updated_at: datetime


@dataclass
class Need:
    """Besoin identifie"""
    id: UUID
    need_number: str                  # NED-001
    category: ResourceCategory
    subcategory: Optional[str]
    description: str
    quantity_needed: float
    quantity_fulfilled: float
    unit: str
    urgency: NeedUrgency
    status: NeedStatus

    # Localisation (anonymisee)
    area: GeoArea

    # Receveur (anonymise)
    receiver_type: ReceiverType
    receiver_hash: str                # Anonymized ID

    # Timing
    needed_by: Optional[datetime]

    # Audit
    created_at: datetime
    updated_at: datetime


@dataclass
class ResourceMatch:
    """Match entre ressource et besoin"""
    id: UUID
    match_number: str                 # MAT-001
    resource_id: UUID
    need_id: UUID
    status: MatchStatus

    # Quantite matchee
    quantity_matched: float
    unit: str

    # Valeur (pour governance)
    estimated_value: Decimal
    requires_approval: bool

    # Transport
    distance_km: float
    transport_needed: bool
    transport_arranged: bool

    # GOVERNANCE
    approved_by_hash: Optional[str]   # Anonymized approver
    approved_at: Optional[datetime]

    # Confirmation
    donor_confirmed: bool
    donor_confirmed_at: Optional[datetime]
    receiver_confirmed: bool
    receiver_confirmed_at: Optional[datetime]

    # Completion
    delivered_at: Optional[datetime]
    delivery_notes: Optional[str]

    # Audit
    created_at: datetime
    updated_at: datetime


@dataclass
class FlowMetric:
    """Metrique de flux pour le dashboard"""
    id: UUID
    timestamp: datetime
    area: GeoArea

    # Metriques de flux
    resources_available: int
    needs_open: int
    matches_pending: int
    matches_completed_today: int

    # Indices societaires
    fluidity_index: float            # 0-1 (ressources qui circulent)
    waste_prevented_kg: float        # Gaspillage evite
    value_redistributed: Decimal     # Valeur redistribuee

    # Sante du systeme
    avg_match_time_hours: float      # Temps moyen pour matcher
    fulfillment_rate: float          # Taux de satisfaction des besoins


# ============================================================================
# RESOURCE BALANCE AGENT
# ============================================================================

class ResourceBalanceAgent:
    """
    CHE·NU V68 Resource Balance Agent
    Equilibre des Ressources - Zero Gaspillage

    PRIVACY FIRST:
    - Toutes les identites sont anonymisees
    - Le systeme voit le "besoin", pas "l'identite"
    - Pas de tracking individuel

    GOVERNANCE COMPLIANCE:
    - Rule #1: Redistribution haute valeur (>$1000) require APPROVAL
    - Rule #5: Resources ALPHABETICAL, Needs CHRONOLOGICAL
    - Rule #6: Audit trail anonymise
    """

    def __init__(self):
        self.resources: Dict[UUID, Resource] = {}
        self.needs: Dict[UUID, Need] = {}
        self.matches: Dict[UUID, ResourceMatch] = {}
        self.flow_metrics: Dict[UUID, FlowMetric] = {}

        # Counters
        self._resource_counter = 0
        self._need_counter = 0
        self._match_counter = 0

        # Configuration
        self.high_value_threshold = Decimal("1000")  # Seuil pour approbation
        self.auto_match_radius_km = 15.0  # Rayon de recherche automatique

    # ========================================================================
    # PRIVACY UTILITIES
    # ========================================================================

    def _anonymize_donor(self, donor_id: UUID) -> str:
        """Anonymize donor ID"""
        return anonymize_id(donor_id)

    def _anonymize_receiver(self, receiver_id: UUID) -> str:
        """Anonymize receiver ID"""
        return anonymize_id(receiver_id)

    # ========================================================================
    # RESOURCE MANAGEMENT (Surplus)
    # ========================================================================

    async def register_resource(
        self,
        category: ResourceCategory,
        subcategory: str,
        description: str,
        quantity: float,
        unit: str,
        condition: ResourceCondition,
        latitude: float,
        longitude: float,
        area_name: str,
        donor_type: DonorType,
        donor_id: UUID,  # Will be anonymized
        estimated_value: Decimal,
        available_from: Optional[datetime] = None,
        available_until: Optional[datetime] = None,
        perishable: bool = False
    ) -> Resource:
        """
        Register a surplus resource
        PRIVACY: Donor ID is anonymized immediately
        """
        self._resource_counter += 1
        resource_number = f"RES-{self._resource_counter:04d}"

        now = datetime.utcnow()

        resource = Resource(
            id=uuid4(),
            resource_number=resource_number,
            category=category,
            subcategory=subcategory,
            description=description,
            quantity=quantity,
            unit=unit,
            condition=condition,
            status=ResourceStatus.AVAILABLE,
            area=GeoArea(
                latitude=latitude,
                longitude=longitude,
                radius_km=2.0,
                name=area_name
            ),
            donor_type=donor_type,
            donor_hash=self._anonymize_donor(donor_id),  # PRIVACY
            available_from=available_from or now,
            available_until=available_until,
            perishable=perishable,
            estimated_value=estimated_value,
            created_at=now,
            updated_at=now
        )

        self.resources[resource.id] = resource
        logger.info(f"Resource registered: {resource_number} - {category.value}/{subcategory}")

        # Auto-search for matching needs
        await self._auto_match_resource(resource.id)

        return resource

    async def get_resources(
        self,
        category: Optional[ResourceCategory] = None,
        area_name: Optional[str] = None
    ) -> List[Resource]:
        """
        Get available resources - ALPHABETICAL by category (Rule #5)
        NOT sorted by value or quantity
        """
        resources = [r for r in self.resources.values()
                    if r.status == ResourceStatus.AVAILABLE]

        if category:
            resources = [r for r in resources if r.category == category]

        if area_name:
            resources = [r for r in resources
                        if r.area.name and area_name.lower() in r.area.name.lower()]

        # RULE #5: ALPHABETICAL by category, then subcategory
        return sorted(resources, key=lambda r: (r.category.value, r.subcategory.lower()))

    async def withdraw_resource(
        self,
        resource_id: UUID,
        reason: str = "Donor withdrew"
    ) -> Resource:
        """Withdraw a resource (donor decision)"""
        if resource_id not in self.resources:
            raise ValueError(f"Resource not found: {resource_id}")

        resource = self.resources[resource_id]
        resource.status = ResourceStatus.WITHDRAWN
        resource.updated_at = datetime.utcnow()

        logger.info(f"Resource {resource.resource_number} withdrawn: {reason}")
        return resource

    # ========================================================================
    # NEED MANAGEMENT
    # ========================================================================

    async def register_need(
        self,
        category: ResourceCategory,
        description: str,
        quantity_needed: float,
        unit: str,
        urgency: NeedUrgency,
        latitude: float,
        longitude: float,
        area_name: str,
        receiver_type: ReceiverType,
        receiver_id: UUID,  # Will be anonymized
        subcategory: Optional[str] = None,
        needed_by: Optional[datetime] = None
    ) -> Need:
        """
        Register a need
        PRIVACY: Receiver ID is anonymized immediately
        """
        self._need_counter += 1
        need_number = f"NED-{self._need_counter:04d}"

        now = datetime.utcnow()

        need = Need(
            id=uuid4(),
            need_number=need_number,
            category=category,
            subcategory=subcategory,
            description=description,
            quantity_needed=quantity_needed,
            quantity_fulfilled=0,
            unit=unit,
            urgency=urgency,
            status=NeedStatus.OPEN,
            area=GeoArea(
                latitude=latitude,
                longitude=longitude,
                radius_km=5.0,
                name=area_name
            ),
            receiver_type=receiver_type,
            receiver_hash=self._anonymize_receiver(receiver_id),  # PRIVACY
            needed_by=needed_by,
            created_at=now,
            updated_at=now
        )

        self.needs[need.id] = need
        logger.info(f"Need registered: {need_number} - {category.value} - {urgency.value}")

        # Auto-search for matching resources
        await self._auto_match_need(need.id)

        return need

    async def get_needs(
        self,
        category: Optional[ResourceCategory] = None,
        urgency: Optional[NeedUrgency] = None,
        area_name: Optional[str] = None
    ) -> List[Need]:
        """
        Get open needs - CHRONOLOGICAL by created_at (Rule #5)
        NOT sorted by urgency (to avoid algorithmic prioritization)
        """
        needs = [n for n in self.needs.values()
                if n.status == NeedStatus.OPEN]

        if category:
            needs = [n for n in needs if n.category == category]

        if urgency:
            needs = [n for n in needs if n.urgency == urgency]

        if area_name:
            needs = [n for n in needs
                    if n.area.name and area_name.lower() in n.area.name.lower()]

        # RULE #5: CHRONOLOGICAL (oldest first - FIFO)
        return sorted(needs, key=lambda n: n.created_at)

    # ========================================================================
    # MATCHING ENGINE
    # ========================================================================

    async def _calculate_distance(self, area1: GeoArea, area2: GeoArea) -> float:
        """Calculate approximate distance between two areas"""
        # Simplified calculation (Haversine would be more accurate)
        import math
        R = 6371  # Earth radius in km

        lat1, lon1 = math.radians(area1.latitude), math.radians(area1.longitude)
        lat2, lon2 = math.radians(area2.latitude), math.radians(area2.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    async def _auto_match_resource(self, resource_id: UUID) -> List[ResourceMatch]:
        """Auto-find matching needs for a new resource"""
        if resource_id not in self.resources:
            return []

        resource = self.resources[resource_id]
        matches_created = []

        # Find compatible needs
        for need in self.needs.values():
            if need.status != NeedStatus.OPEN:
                continue

            if need.category != resource.category:
                continue

            # Check distance
            distance = await self._calculate_distance(resource.area, need.area)
            if distance > self.auto_match_radius_km:
                continue

            # Check quantity
            remaining_need = need.quantity_needed - need.quantity_fulfilled
            if remaining_need <= 0:
                continue

            # Create match suggestion
            match = await self._create_match(
                resource_id=resource_id,
                need_id=need.id,
                quantity=min(resource.quantity, remaining_need),
                distance=distance
            )
            matches_created.append(match)

        return matches_created

    async def _auto_match_need(self, need_id: UUID) -> List[ResourceMatch]:
        """Auto-find matching resources for a new need"""
        if need_id not in self.needs:
            return []

        need = self.needs[need_id]
        matches_created = []

        # Find compatible resources
        for resource in self.resources.values():
            if resource.status != ResourceStatus.AVAILABLE:
                continue

            if resource.category != need.category:
                continue

            # Check distance
            distance = await self._calculate_distance(resource.area, need.area)
            if distance > self.auto_match_radius_km:
                continue

            # Create match suggestion
            remaining_need = need.quantity_needed - need.quantity_fulfilled
            match = await self._create_match(
                resource_id=resource.id,
                need_id=need_id,
                quantity=min(resource.quantity, remaining_need),
                distance=distance
            )
            matches_created.append(match)

        return matches_created

    async def _create_match(
        self,
        resource_id: UUID,
        need_id: UUID,
        quantity: float,
        distance: float
    ) -> ResourceMatch:
        """Create a match between resource and need"""
        resource = self.resources[resource_id]
        need = self.needs[need_id]

        self._match_counter += 1
        match_number = f"MAT-{self._match_counter:04d}"

        # Calculate value
        unit_value = resource.estimated_value / Decimal(str(resource.quantity)) if resource.quantity > 0 else Decimal("0")
        match_value = unit_value * Decimal(str(quantity))

        # Determine if approval needed (high value)
        requires_approval = match_value >= self.high_value_threshold

        now = datetime.utcnow()

        match = ResourceMatch(
            id=uuid4(),
            match_number=match_number,
            resource_id=resource_id,
            need_id=need_id,
            status=MatchStatus.SUGGESTED,
            quantity_matched=quantity,
            unit=resource.unit,
            estimated_value=match_value,
            requires_approval=requires_approval,
            distance_km=distance,
            transport_needed=distance > 2.0,
            transport_arranged=False,
            approved_by_hash=None,
            approved_at=None,
            donor_confirmed=False,
            donor_confirmed_at=None,
            receiver_confirmed=False,
            receiver_confirmed_at=None,
            delivered_at=None,
            delivery_notes=None,
            created_at=now,
            updated_at=now
        )

        self.matches[match.id] = match

        if requires_approval:
            logger.info(f"GOVERNANCE: Match {match_number} requires approval (value: ${match_value})")
        else:
            logger.info(f"Match suggested: {match_number} - {resource.resource_number} -> {need.need_number}")

        return match

    async def get_matches(
        self,
        status: Optional[MatchStatus] = None
    ) -> List[ResourceMatch]:
        """
        Get matches - CHRONOLOGICAL (Rule #5)
        """
        matches = list(self.matches.values())

        if status:
            matches = [m for m in matches if m.status == status]

        # RULE #5: CHRONOLOGICAL
        return sorted(matches, key=lambda m: m.created_at, reverse=True)

    async def get_pending_approval_matches(self) -> List[ResourceMatch]:
        """Get matches pending governance approval"""
        return [m for m in self.matches.values()
                if m.requires_approval and m.status == MatchStatus.SUGGESTED]

    # ========================================================================
    # CONFIRMATION FLOW
    # ========================================================================

    async def confirm_match_donor(
        self,
        match_id: UUID
    ) -> ResourceMatch:
        """Donor confirms the match"""
        if match_id not in self.matches:
            raise ValueError(f"Match not found: {match_id}")

        match = self.matches[match_id]
        match.donor_confirmed = True
        match.donor_confirmed_at = datetime.utcnow()

        # Check if both confirmed
        await self._check_match_confirmation(match_id)

        logger.info(f"Match {match.match_number} confirmed by donor")
        return match

    async def confirm_match_receiver(
        self,
        match_id: UUID
    ) -> ResourceMatch:
        """Receiver confirms the match"""
        if match_id not in self.matches:
            raise ValueError(f"Match not found: {match_id}")

        match = self.matches[match_id]
        match.receiver_confirmed = True
        match.receiver_confirmed_at = datetime.utcnow()

        # Check if both confirmed
        await self._check_match_confirmation(match_id)

        logger.info(f"Match {match.match_number} confirmed by receiver")
        return match

    async def _check_match_confirmation(self, match_id: UUID) -> None:
        """Check if match is fully confirmed and update status"""
        match = self.matches[match_id]

        if match.donor_confirmed and match.receiver_confirmed:
            if match.requires_approval:
                match.status = MatchStatus.PENDING_APPROVAL
                logger.info(f"GOVERNANCE: Match {match.match_number} awaiting approval")
            else:
                match.status = MatchStatus.CONFIRMED
                # Update resource and need
                await self._apply_match(match_id)

    # ========================================================================
    # GOVERNANCE (Rule #1)
    # ========================================================================

    async def approve_match(
        self,
        match_id: UUID,
        approved: bool,
        approver_id: UUID
    ) -> ResourceMatch:
        """
        GOVERNANCE - Rule #1: Approve or reject high-value match
        """
        if match_id not in self.matches:
            raise ValueError(f"Match not found: {match_id}")

        match = self.matches[match_id]

        if not match.requires_approval:
            raise ValueError("This match does not require approval")

        if match.status != MatchStatus.PENDING_APPROVAL:
            raise ValueError(f"Match is not pending approval: {match.status.value}")

        match.approved_by_hash = anonymize_id(approver_id)  # PRIVACY
        match.approved_at = datetime.utcnow()

        if approved:
            match.status = MatchStatus.CONFIRMED
            await self._apply_match(match_id)
            logger.info(f"GOVERNANCE: Match {match.match_number} APPROVED")
        else:
            match.status = MatchStatus.CANCELLED
            logger.info(f"GOVERNANCE: Match {match.match_number} REJECTED")

        return match

    async def _apply_match(self, match_id: UUID) -> None:
        """Apply a confirmed match - update resource and need"""
        match = self.matches[match_id]
        resource = self.resources[match.resource_id]
        need = self.needs[match.need_id]

        # Update resource
        resource.quantity -= match.quantity_matched
        if resource.quantity <= 0:
            resource.status = ResourceStatus.RESERVED
        resource.updated_at = datetime.utcnow()

        # Update need
        need.quantity_fulfilled += match.quantity_matched
        if need.quantity_fulfilled >= need.quantity_needed:
            need.status = NeedStatus.FULFILLED
        else:
            need.status = NeedStatus.MATCHED
        need.updated_at = datetime.utcnow()

    # ========================================================================
    # DELIVERY
    # ========================================================================

    async def mark_in_transit(
        self,
        match_id: UUID
    ) -> ResourceMatch:
        """Mark match as in transit"""
        if match_id not in self.matches:
            raise ValueError(f"Match not found: {match_id}")

        match = self.matches[match_id]
        match.status = MatchStatus.IN_TRANSIT
        match.updated_at = datetime.utcnow()

        # Update resource status
        resource = self.resources[match.resource_id]
        resource.status = ResourceStatus.IN_TRANSIT
        resource.updated_at = datetime.utcnow()

        logger.info(f"Match {match.match_number} in transit")
        return match

    async def complete_delivery(
        self,
        match_id: UUID,
        notes: Optional[str] = None
    ) -> ResourceMatch:
        """Mark delivery as completed"""
        if match_id not in self.matches:
            raise ValueError(f"Match not found: {match_id}")

        match = self.matches[match_id]
        match.status = MatchStatus.COMPLETED
        match.delivered_at = datetime.utcnow()
        match.delivery_notes = notes
        match.updated_at = datetime.utcnow()

        # Update resource status
        resource = self.resources[match.resource_id]
        resource.status = ResourceStatus.DELIVERED
        resource.updated_at = datetime.utcnow()

        logger.info(f"Match {match.match_number} completed - resource delivered")
        return match

    # ========================================================================
    # FLOW METRICS (Dashboard Societaire)
    # ========================================================================

    async def record_flow_metric(
        self,
        latitude: float,
        longitude: float,
        area_name: str
    ) -> FlowMetric:
        """Record flow metrics for an area"""
        area = GeoArea(latitude, longitude, 10.0, area_name)

        # Calculate metrics
        resources_in_area = [r for r in self.resources.values()
                           if r.status == ResourceStatus.AVAILABLE]
        needs_in_area = [n for n in self.needs.values()
                        if n.status == NeedStatus.OPEN]

        completed_today = [m for m in self.matches.values()
                         if m.status == MatchStatus.COMPLETED
                         and m.delivered_at
                         and m.delivered_at.date() == datetime.utcnow().date()]

        # Calculate fluidity index
        total_resources = len(resources_in_area)
        total_needs = len(needs_in_area)
        total_matches = len(completed_today)

        if total_resources + total_needs > 0:
            fluidity = total_matches / (total_resources + total_needs)
        else:
            fluidity = 1.0  # No resources/needs = perfect fluidity

        # Calculate waste prevented (simplified)
        waste_prevented = sum(
            m.quantity_matched
            for m in completed_today
            if self.resources[m.resource_id].category == ResourceCategory.FOOD
        )

        # Calculate value redistributed
        value_redistributed = sum(
            m.estimated_value for m in completed_today
        )

        # Average match time
        matched = [m for m in self.matches.values()
                  if m.status == MatchStatus.COMPLETED and m.delivered_at]
        if matched:
            avg_time = sum(
                (m.delivered_at - m.created_at).total_seconds() / 3600
                for m in matched
            ) / len(matched)
        else:
            avg_time = 0

        # Fulfillment rate
        total_needs_ever = len(self.needs)
        fulfilled = len([n for n in self.needs.values() if n.status == NeedStatus.FULFILLED])
        fulfillment_rate = fulfilled / total_needs_ever if total_needs_ever > 0 else 1.0

        metric = FlowMetric(
            id=uuid4(),
            timestamp=datetime.utcnow(),
            area=area,
            resources_available=len(resources_in_area),
            needs_open=len(needs_in_area),
            matches_pending=len([m for m in self.matches.values()
                                if m.status in [MatchStatus.SUGGESTED, MatchStatus.PENDING_APPROVAL]]),
            matches_completed_today=len(completed_today),
            fluidity_index=min(1.0, fluidity),
            waste_prevented_kg=waste_prevented,
            value_redistributed=value_redistributed,
            avg_match_time_hours=avg_time,
            fulfillment_rate=fulfillment_rate
        )

        self.flow_metrics[metric.id] = metric
        return metric

    async def get_social_indices(self) -> Dict[str, Any]:
        """
        Get social indices for the iPad dashboard
        Indice de Cohesion & Indice de Fluidite
        """
        # Get recent metrics
        recent = [m for m in self.flow_metrics.values()
                 if (datetime.utcnow() - m.timestamp).total_seconds() < 86400]  # Last 24h

        if not recent:
            # Calculate live
            total_resources = len([r for r in self.resources.values()
                                  if r.status == ResourceStatus.AVAILABLE])
            total_needs = len([n for n in self.needs.values()
                              if n.status == NeedStatus.OPEN])
            completed = len([m for m in self.matches.values()
                            if m.status == MatchStatus.COMPLETED])

            fluidity = completed / max(1, total_resources + total_needs)
            cohesion = len(self.matches) / max(1, len(self.resources) + len(self.needs))

            waste_prevented = sum(
                self.resources[m.resource_id].quantity
                for m in self.matches.values()
                if m.status == MatchStatus.COMPLETED
                and self.resources[m.resource_id].category == ResourceCategory.FOOD
            )

            value_redistributed = sum(
                float(m.estimated_value)
                for m in self.matches.values()
                if m.status == MatchStatus.COMPLETED
            )
        else:
            fluidity = sum(m.fluidity_index for m in recent) / len(recent)
            cohesion = sum(m.fulfillment_rate for m in recent) / len(recent)
            waste_prevented = sum(m.waste_prevented_kg for m in recent)
            value_redistributed = sum(float(m.value_redistributed) for m in recent)

        # Determine color (999Hz inspiration)
        if fluidity > 0.8:
            color = "#0057b8"  # Bleu cobalt - excellent
            status = "optimal"
        elif fluidity > 0.5:
            color = "#28a745"  # Vert
            status = "good"
        elif fluidity > 0.2:
            color = "#fd7e14"  # Orange
            status = "needs_attention"
        else:
            color = "#dc3545"  # Rouge
            status = "critical"

        return {
            "fluidity_index": round(fluidity, 2),
            "cohesion_index": round(cohesion, 2),
            "status": status,
            "color_hex": color,
            "message": self._get_fluidity_message(fluidity),
            "metrics": {
                "resources_available": len([r for r in self.resources.values()
                                           if r.status == ResourceStatus.AVAILABLE]),
                "needs_open": len([n for n in self.needs.values()
                                  if n.status == NeedStatus.OPEN]),
                "matches_active": len([m for m in self.matches.values()
                                      if m.status not in [MatchStatus.COMPLETED, MatchStatus.CANCELLED]]),
                "waste_prevented_kg": round(waste_prevented, 1),
                "value_redistributed": round(value_redistributed, 2)
            }
        }

    def _get_fluidity_message(self, fluidity: float) -> str:
        """Get message for fluidity level"""
        if fluidity > 0.8:
            return "Les ressources circulent librement - Zero gaspillage"
        elif fluidity > 0.5:
            return "Bonne circulation - Quelques surplus a redistribuer"
        elif fluidity > 0.2:
            return "Circulation ralentie - Besoins en attente"
        else:
            return "Blocage detecte - Intervention recommandee"

    # ========================================================================
    # SUMMARY
    # ========================================================================

    async def get_summary(self) -> Dict[str, Any]:
        """Get resource balance summary"""
        indices = await self.get_social_indices()

        return {
            "resources": {
                "total": len(self.resources),
                "available": len([r for r in self.resources.values()
                                 if r.status == ResourceStatus.AVAILABLE]),
                "by_category": self._count_by_category(self.resources.values(), "category")
            },
            "needs": {
                "total": len(self.needs),
                "open": len([n for n in self.needs.values()
                           if n.status == NeedStatus.OPEN]),
                "fulfilled": len([n for n in self.needs.values()
                                 if n.status == NeedStatus.FULFILLED])
            },
            "matches": {
                "total": len(self.matches),
                "completed": len([m for m in self.matches.values()
                                 if m.status == MatchStatus.COMPLETED]),
                "pending_approval": len([m for m in self.matches.values()
                                        if m.status == MatchStatus.PENDING_APPROVAL])
            },
            "social_indices": indices,
            "privacy": {
                "all_identities_anonymized": True,
                "no_individual_tracking": True
            }
        }

    def _count_by_category(self, items, attr: str) -> Dict[str, int]:
        """Count items by category"""
        counts = {}
        for item in items:
            cat = getattr(item, attr).value
            counts[cat] = counts.get(cat, 0) + 1
        return counts


# Singleton instance
_resource_agent: Optional[ResourceBalanceAgent] = None


def get_resource_balance_agent() -> ResourceBalanceAgent:
    """Get or create resource balance agent singleton"""
    global _resource_agent
    if _resource_agent is None:
        _resource_agent = ResourceBalanceAgent()
    return _resource_agent
