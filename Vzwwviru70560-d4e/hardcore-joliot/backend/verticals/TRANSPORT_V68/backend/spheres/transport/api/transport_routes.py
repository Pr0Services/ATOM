"""
CHE·NU V68 Transport & Logistics API Routes
AT·OM Flow - Gestion Intelligente des Transports

GOVERNANCE COMPLIANCE:
- Rule #1: Approval endpoints for dispatch haute valeur + sous-traitance
- Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL
- Rule #6: Full audit trail

Endpoints:
- /vehicles - Gestion de la flotte
- /drivers - Gestion des chauffeurs
- /trips - Gestion des trajets
- /zones - Zones Che-Nu
- /dispatch - Dispatch collaboratif
- /soustraitance - Partenaires externes
- /pooling - Covoiturage et mutualisation
- /flow - Metriques de flux
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from backend.verticals.TRANSPORT_V68.backend.spheres.transport.agents.transport_agent import (
    get_transport_agent,
    VehicleType,
    VehicleStatus,
    TripType,
    TripStatus,
    LoadType,
    DispatchMode,
    SoustraitanceType,
    OptimizationGoal,
    ZoneType,
    GeoPoint,
)


router = APIRouter(prefix="/api/v2/transport", tags=["Transport & Logistics"])


# ============================================================================
# SCHEMAS
# ============================================================================

class GeoPointSchema(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    name: Optional[str] = None


class VehicleCreate(BaseModel):
    registration: str
    name: str
    vehicle_type: VehicleType
    capacity_kg: float = Field(gt=0)
    capacity_m3: float = Field(gt=0)
    cost_per_km: float = Field(gt=0)
    fuel_type: str
    emissions_g_per_km: float = Field(ge=0)
    current_location: Optional[GeoPointSchema] = None


class VehicleResponse(BaseModel):
    id: UUID
    registration: str
    name: str
    vehicle_type: str
    status: str
    capacity_kg: float
    capacity_m3: float
    current_load_kg: float
    current_load_m3: float
    fill_rate: float
    is_underutilized: bool
    cost_per_km: float
    fuel_type: str
    emissions_g_per_km: float
    driver_name: Optional[str]
    created_at: datetime


class DriverCreate(BaseModel):
    name: str
    phone: str
    email: str
    license_number: str
    license_expiry: date
    vehicle_types: List[VehicleType]
    home_zone: Optional[str] = None


class DriverResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    email: str
    license_number: str
    license_expiry: date
    vehicle_types: List[str]
    status: str
    current_vehicle_id: Optional[UUID]
    home_zone: Optional[str]
    created_at: datetime


class TripCreate(BaseModel):
    trip_type: TripType
    origin: GeoPointSchema
    destination: GeoPointSchema
    scheduled_departure: datetime
    scheduled_arrival: datetime
    load_type: LoadType
    load_description: str
    load_weight_kg: float = Field(gt=0)
    load_volume_m3: float = Field(gt=0)
    vehicle_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    waypoints: Optional[List[GeoPointSchema]] = None
    recurrence_pattern: Optional[str] = None
    recurrence_days: Optional[List[int]] = None
    allows_pooling: bool = True
    client_id: Optional[UUID] = None
    client_name: Optional[str] = None


class TripResponse(BaseModel):
    id: UUID
    trip_number: str
    trip_type: str
    status: str
    origin: dict
    destination: dict
    scheduled_departure: datetime
    scheduled_arrival: datetime
    actual_departure: Optional[datetime]
    actual_arrival: Optional[datetime]
    load_type: str
    load_description: str
    load_weight_kg: float
    estimated_distance_km: float
    estimated_cost: float
    actual_distance_km: Optional[float]
    actual_cost: Optional[float]
    allows_pooling: bool
    vehicle_id: Optional[UUID]
    driver_id: Optional[UUID]
    client_name: Optional[str]
    pooled_loads: List[UUID]
    created_at: datetime


class ZoneCreate(BaseModel):
    name: str
    zone_type: ZoneType
    center: GeoPointSchema
    radius_km: float = Field(gt=0)
    friction_level: float = Field(ge=0, le=1)
    typical_delay_minutes: int = Field(ge=0)
    peak_hours: Optional[List[int]] = None
    avoid_if_possible: bool = False
    alternative_zones: Optional[List[UUID]] = None


class ZoneResponse(BaseModel):
    id: UUID
    name: str
    zone_type: str
    center: dict
    radius_km: float
    friction_level: float
    typical_delay_minutes: int
    peak_hours: List[int]
    avoid_if_possible: bool
    alternative_zones: List[UUID]
    created_at: datetime


class DispatchRequest(BaseModel):
    trip_id: UUID
    optimization_goal: OptimizationGoal = OptimizationGoal.BALANCED


class DispatchResponse(BaseModel):
    id: UUID
    trip_id: UUID
    dispatch_mode: str
    selected_vehicle_id: UUID
    selected_driver_id: Optional[UUID]
    optimization_score: float
    fill_rate_before: float
    fill_rate_after: float
    requires_approval: bool
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    alternatives: List[dict]
    created_at: datetime


class SoustraitanceRequest(BaseModel):
    trip_id: UUID
    soustraitance_type: SoustraitanceType
    partner_name: str
    partner_contact: str
    agreed_price: float = Field(gt=0)
    commission_rate: float = Field(ge=0, le=1)


class SoustraitanceResponse(BaseModel):
    id: UUID
    contract_number: str
    soustraitance_type: str
    status: str
    trip_id: UUID
    partner_name: str
    partner_contact: str
    agreed_price: float
    commission_rate: float
    requested_at: datetime
    confirmed_at: Optional[datetime]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    created_at: datetime


class ApprovalRequest(BaseModel):
    approved: bool
    rejection_reason: Optional[str] = None


class FlowScoreResponse(BaseModel):
    global_fluidity: float
    global_friction: float
    flow_status: str
    color_hex: str
    message: str
    zones_monitored: Optional[int] = None
    vehicles_active: Optional[int] = None


# ============================================================================
# VEHICLE ENDPOINTS
# ============================================================================

@router.post("/vehicles", response_model=VehicleResponse)
async def register_vehicle(
    data: VehicleCreate,
    user_id: UUID = Query(default_factory=uuid4)  # In production: from auth
):
    """Register a new vehicle"""
    agent = get_transport_agent()

    location = None
    if data.current_location:
        location = GeoPoint(
            latitude=data.current_location.latitude,
            longitude=data.current_location.longitude,
            address=data.current_location.address,
            name=data.current_location.name
        )

    vehicle = await agent.register_vehicle(
        registration=data.registration,
        name=data.name,
        vehicle_type=data.vehicle_type,
        capacity_kg=data.capacity_kg,
        capacity_m3=data.capacity_m3,
        cost_per_km=Decimal(str(data.cost_per_km)),
        fuel_type=data.fuel_type,
        emissions_g_per_km=data.emissions_g_per_km,
        created_by=user_id,
        current_location=location
    )

    return VehicleResponse(
        id=vehicle.id,
        registration=vehicle.registration,
        name=vehicle.name,
        vehicle_type=vehicle.vehicle_type.value,
        status=vehicle.status.value,
        capacity_kg=vehicle.capacity_kg,
        capacity_m3=vehicle.capacity_m3,
        current_load_kg=vehicle.current_load_kg,
        current_load_m3=vehicle.current_load_m3,
        fill_rate=vehicle.fill_rate,
        is_underutilized=vehicle.is_underutilized,
        cost_per_km=float(vehicle.cost_per_km),
        fuel_type=vehicle.fuel_type,
        emissions_g_per_km=vehicle.emissions_g_per_km,
        driver_name=vehicle.driver_name,
        created_at=vehicle.created_at
    )


@router.get("/vehicles", response_model=List[VehicleResponse])
async def list_vehicles():
    """
    List all vehicles - ALPHABETICAL by name (Rule #5)
    NOT sorted by efficiency or fill rate
    """
    agent = get_transport_agent()
    vehicles = await agent.get_vehicles()

    return [
        VehicleResponse(
            id=v.id,
            registration=v.registration,
            name=v.name,
            vehicle_type=v.vehicle_type.value,
            status=v.status.value,
            capacity_kg=v.capacity_kg,
            capacity_m3=v.capacity_m3,
            current_load_kg=v.current_load_kg,
            current_load_m3=v.current_load_m3,
            fill_rate=v.fill_rate,
            is_underutilized=v.is_underutilized,
            cost_per_km=float(v.cost_per_km),
            fuel_type=v.fuel_type,
            emissions_g_per_km=v.emissions_g_per_km,
            driver_name=v.driver_name,
            created_at=v.created_at
        )
        for v in vehicles
    ]


@router.get("/vehicles/underutilized", response_model=List[VehicleResponse])
async def list_underutilized_vehicles():
    """
    List underutilized vehicles (<40% fill rate) - ALPHABETICAL (Rule #5)
    For collaborative optimization suggestions
    """
    agent = get_transport_agent()
    vehicles = await agent.get_underutilized_vehicles()

    return [
        VehicleResponse(
            id=v.id,
            registration=v.registration,
            name=v.name,
            vehicle_type=v.vehicle_type.value,
            status=v.status.value,
            capacity_kg=v.capacity_kg,
            capacity_m3=v.capacity_m3,
            current_load_kg=v.current_load_kg,
            current_load_m3=v.current_load_m3,
            fill_rate=v.fill_rate,
            is_underutilized=v.is_underutilized,
            cost_per_km=float(v.cost_per_km),
            fuel_type=v.fuel_type,
            emissions_g_per_km=v.emissions_g_per_km,
            driver_name=v.driver_name,
            created_at=v.created_at
        )
        for v in vehicles
    ]


# ============================================================================
# DRIVER ENDPOINTS
# ============================================================================

@router.post("/drivers", response_model=DriverResponse)
async def register_driver(
    data: DriverCreate,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Register a new driver"""
    agent = get_transport_agent()

    driver = await agent.register_driver(
        name=data.name,
        phone=data.phone,
        email=data.email,
        license_number=data.license_number,
        license_expiry=data.license_expiry,
        vehicle_types=data.vehicle_types,
        created_by=user_id,
        home_zone=data.home_zone
    )

    return DriverResponse(
        id=driver.id,
        name=driver.name,
        phone=driver.phone,
        email=driver.email,
        license_number=driver.license_number,
        license_expiry=driver.license_expiry,
        vehicle_types=[vt.value for vt in driver.vehicle_types],
        status=driver.status,
        current_vehicle_id=driver.current_vehicle_id,
        home_zone=driver.home_zone,
        created_at=driver.created_at
    )


@router.get("/drivers", response_model=List[DriverResponse])
async def list_drivers():
    """
    List all drivers - ALPHABETICAL by name (Rule #5)
    NOT sorted by rating or performance
    """
    agent = get_transport_agent()
    drivers = await agent.get_drivers()

    return [
        DriverResponse(
            id=d.id,
            name=d.name,
            phone=d.phone,
            email=d.email,
            license_number=d.license_number,
            license_expiry=d.license_expiry,
            vehicle_types=[vt.value for vt in d.vehicle_types],
            status=d.status,
            current_vehicle_id=d.current_vehicle_id,
            home_zone=d.home_zone,
            created_at=d.created_at
        )
        for d in drivers
    ]


@router.post("/drivers/{driver_id}/assign/{vehicle_id}")
async def assign_driver_to_vehicle(
    driver_id: UUID,
    vehicle_id: UUID,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Assign a driver to a vehicle"""
    agent = get_transport_agent()

    try:
        driver, vehicle = await agent.assign_driver_to_vehicle(
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            user_id=user_id
        )
        return {
            "status": "success",
            "message": f"Driver {driver.name} assigned to {vehicle.name}",
            "driver_id": str(driver.id),
            "vehicle_id": str(vehicle.id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# TRIP ENDPOINTS
# ============================================================================

@router.post("/trips", response_model=TripResponse)
async def create_trip(
    data: TripCreate,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Create a new trip"""
    agent = get_transport_agent()

    origin = GeoPoint(
        latitude=data.origin.latitude,
        longitude=data.origin.longitude,
        address=data.origin.address,
        name=data.origin.name
    )

    destination = GeoPoint(
        latitude=data.destination.latitude,
        longitude=data.destination.longitude,
        address=data.destination.address,
        name=data.destination.name
    )

    waypoints = None
    if data.waypoints:
        waypoints = [
            GeoPoint(
                latitude=wp.latitude,
                longitude=wp.longitude,
                address=wp.address,
                name=wp.name
            )
            for wp in data.waypoints
        ]

    trip = await agent.create_trip(
        trip_type=data.trip_type,
        origin=origin,
        destination=destination,
        scheduled_departure=data.scheduled_departure,
        scheduled_arrival=data.scheduled_arrival,
        load_type=data.load_type,
        load_description=data.load_description,
        load_weight_kg=data.load_weight_kg,
        load_volume_m3=data.load_volume_m3,
        created_by=user_id,
        vehicle_id=data.vehicle_id,
        driver_id=data.driver_id,
        waypoints=waypoints,
        recurrence_pattern=data.recurrence_pattern,
        recurrence_days=data.recurrence_days,
        allows_pooling=data.allows_pooling,
        client_id=data.client_id,
        client_name=data.client_name
    )

    return _trip_to_response(trip)


@router.get("/trips", response_model=List[TripResponse])
async def list_trips():
    """
    List all trips - CHRONOLOGICAL by scheduled_departure (Rule #5)
    NOT sorted by profitability
    """
    agent = get_transport_agent()
    trips = await agent.get_trips()
    return [_trip_to_response(t) for t in trips]


@router.get("/trips/active", response_model=List[TripResponse])
async def list_active_trips():
    """List active trips - CHRONOLOGICAL (Rule #5)"""
    agent = get_transport_agent()
    trips = await agent.get_active_trips()
    return [_trip_to_response(t) for t in trips]


@router.post("/trips/{trip_id}/start")
async def start_trip(
    trip_id: UUID,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Start a trip"""
    agent = get_transport_agent()

    try:
        trip = await agent.start_trip(trip_id, user_id)
        return {
            "status": "success",
            "message": f"Trip {trip.trip_number} started",
            "trip_id": str(trip.id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trips/{trip_id}/complete")
async def complete_trip(
    trip_id: UUID,
    actual_distance_km: float = Query(..., gt=0),
    actual_cost: float = Query(..., gt=0),
    user_id: UUID = Query(default_factory=uuid4)
):
    """Complete a trip"""
    agent = get_transport_agent()

    try:
        trip = await agent.complete_trip(
            trip_id=trip_id,
            actual_distance_km=actual_distance_km,
            actual_cost=Decimal(str(actual_cost)),
            user_id=user_id
        )
        return {
            "status": "success",
            "message": f"Trip {trip.trip_number} completed",
            "trip_id": str(trip.id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def _trip_to_response(trip) -> TripResponse:
    """Convert Trip to TripResponse"""
    return TripResponse(
        id=trip.id,
        trip_number=trip.trip_number,
        trip_type=trip.trip_type.value,
        status=trip.status.value,
        origin={
            "latitude": trip.origin.latitude,
            "longitude": trip.origin.longitude,
            "address": trip.origin.address,
            "name": trip.origin.name
        },
        destination={
            "latitude": trip.destination.latitude,
            "longitude": trip.destination.longitude,
            "address": trip.destination.address,
            "name": trip.destination.name
        },
        scheduled_departure=trip.scheduled_departure,
        scheduled_arrival=trip.scheduled_arrival,
        actual_departure=trip.actual_departure,
        actual_arrival=trip.actual_arrival,
        load_type=trip.load_type.value,
        load_description=trip.load_description,
        load_weight_kg=trip.load_weight_kg,
        estimated_distance_km=trip.estimated_distance_km,
        estimated_cost=float(trip.estimated_cost),
        actual_distance_km=trip.actual_distance_km,
        actual_cost=float(trip.actual_cost) if trip.actual_cost else None,
        allows_pooling=trip.allows_pooling,
        vehicle_id=trip.vehicle_id,
        driver_id=trip.driver_id,
        client_name=trip.client_name,
        pooled_loads=trip.pooled_loads,
        created_at=trip.created_at
    )


# ============================================================================
# CHE-NU ZONE ENDPOINTS
# ============================================================================

@router.post("/zones", response_model=ZoneResponse)
async def create_zone(
    data: ZoneCreate,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Create a Che-Nu zone"""
    agent = get_transport_agent()

    center = GeoPoint(
        latitude=data.center.latitude,
        longitude=data.center.longitude,
        address=data.center.address,
        name=data.center.name
    )

    zone = await agent.create_zone(
        name=data.name,
        zone_type=data.zone_type,
        center=center,
        radius_km=data.radius_km,
        friction_level=data.friction_level,
        typical_delay_minutes=data.typical_delay_minutes,
        created_by=user_id,
        peak_hours=data.peak_hours,
        avoid_if_possible=data.avoid_if_possible,
        alternative_zones=data.alternative_zones
    )

    return ZoneResponse(
        id=zone.id,
        name=zone.name,
        zone_type=zone.zone_type.value,
        center={
            "latitude": zone.center.latitude,
            "longitude": zone.center.longitude,
            "address": zone.center.address,
            "name": zone.center.name
        },
        radius_km=zone.radius_km,
        friction_level=zone.friction_level,
        typical_delay_minutes=zone.typical_delay_minutes,
        peak_hours=zone.peak_hours,
        avoid_if_possible=zone.avoid_if_possible,
        alternative_zones=zone.alternative_zones,
        created_at=zone.created_at
    )


@router.get("/zones", response_model=List[ZoneResponse])
async def list_zones():
    """List all Che-Nu zones - ALPHABETICAL (Rule #5)"""
    agent = get_transport_agent()
    zones = await agent.get_zones()

    return [
        ZoneResponse(
            id=z.id,
            name=z.name,
            zone_type=z.zone_type.value,
            center={
                "latitude": z.center.latitude,
                "longitude": z.center.longitude,
                "address": z.center.address,
                "name": z.center.name
            },
            radius_km=z.radius_km,
            friction_level=z.friction_level,
            typical_delay_minutes=z.typical_delay_minutes,
            peak_hours=z.peak_hours,
            avoid_if_possible=z.avoid_if_possible,
            alternative_zones=z.alternative_zones,
            created_at=z.created_at
        )
        for z in zones
    ]


@router.get("/zones/avoid")
async def get_zones_to_avoid(
    hour: Optional[int] = Query(default=None, ge=0, le=23)
):
    """Get high-friction zones to avoid"""
    agent = get_transport_agent()
    current_hour = hour if hour is not None else datetime.now().hour
    zones = await agent.find_zones_to_avoid(current_hour)

    return {
        "hour": current_hour,
        "zones_to_avoid": [
            {
                "id": str(z.id),
                "name": z.name,
                "friction_level": z.friction_level,
                "typical_delay_minutes": z.typical_delay_minutes
            }
            for z in zones
        ],
        "total_potential_delay_minutes": sum(z.typical_delay_minutes for z in zones)
    }


# ============================================================================
# DISPATCH ENDPOINTS (GOVERNANCE - Rule #1)
# ============================================================================

@router.post("/dispatch/collaborative", response_model=DispatchResponse)
async def dispatch_collaborative(
    data: DispatchRequest,
    user_id: UUID = Query(default_factory=uuid4)
):
    """
    Collaborative dispatch - Intelligence collective
    GOVERNANCE: High-value dispatches require approval (Rule #1)
    """
    agent = get_transport_agent()

    try:
        decision = await agent.dispatch_collaborative(
            trip_id=data.trip_id,
            optimization_goal=data.optimization_goal,
            user_id=user_id
        )

        return DispatchResponse(
            id=decision.id,
            trip_id=decision.trip_id,
            dispatch_mode=decision.dispatch_mode.value,
            selected_vehicle_id=decision.selected_vehicle_id,
            selected_driver_id=decision.selected_driver_id,
            optimization_score=decision.optimization_score,
            fill_rate_before=decision.fill_rate_before,
            fill_rate_after=decision.fill_rate_after,
            requires_approval=decision.requires_approval,
            approved_by=decision.approved_by,
            approved_at=decision.approved_at,
            alternatives=decision.alternatives,
            created_at=decision.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/dispatch/{decision_id}/approve", response_model=DispatchResponse)
async def approve_dispatch(
    decision_id: UUID,
    data: ApprovalRequest,
    user_id: UUID = Query(default_factory=uuid4)
):
    """
    GOVERNANCE - Rule #1: Approve or reject a dispatch decision
    Required for high-value loads
    """
    agent = get_transport_agent()

    try:
        decision = await agent.approve_dispatch(
            decision_id=decision_id,
            approved=data.approved,
            approver_id=user_id
        )

        return DispatchResponse(
            id=decision.id,
            trip_id=decision.trip_id,
            dispatch_mode=decision.dispatch_mode.value,
            selected_vehicle_id=decision.selected_vehicle_id,
            selected_driver_id=decision.selected_driver_id,
            optimization_score=decision.optimization_score,
            fill_rate_before=decision.fill_rate_before,
            fill_rate_after=decision.fill_rate_after,
            requires_approval=decision.requires_approval,
            approved_by=decision.approved_by,
            approved_at=decision.approved_at,
            alternatives=decision.alternatives,
            created_at=decision.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# SOUS-TRAITANCE ENDPOINTS (GOVERNANCE - Rule #1)
# ============================================================================

@router.post("/soustraitance", response_model=SoustraitanceResponse)
async def request_soustraitance(
    data: SoustraitanceRequest,
    user_id: UUID = Query(default_factory=uuid4)
):
    """
    Request sous-traitance (Uber, Taxi, Partner)
    GOVERNANCE: ALL sous-traitance requires approval (Rule #1)
    """
    agent = get_transport_agent()

    try:
        contract = await agent.request_soustraitance(
            trip_id=data.trip_id,
            soustraitance_type=data.soustraitance_type,
            partner_name=data.partner_name,
            partner_contact=data.partner_contact,
            agreed_price=Decimal(str(data.agreed_price)),
            commission_rate=data.commission_rate,
            created_by=user_id
        )

        return _soustraitance_to_response(contract)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/soustraitance/{contract_id}/approve", response_model=SoustraitanceResponse)
async def approve_soustraitance(
    contract_id: UUID,
    data: ApprovalRequest,
    user_id: UUID = Query(default_factory=uuid4)
):
    """
    GOVERNANCE - Rule #1: Approve or reject sous-traitance contract
    """
    agent = get_transport_agent()

    try:
        contract = await agent.approve_soustraitance(
            contract_id=contract_id,
            approved=data.approved,
            approver_id=user_id,
            rejection_reason=data.rejection_reason
        )

        return _soustraitance_to_response(contract)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/soustraitance/{contract_id}/activate", response_model=SoustraitanceResponse)
async def activate_soustraitance(
    contract_id: UUID,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Activate an approved sous-traitance contract"""
    agent = get_transport_agent()

    try:
        contract = await agent.activate_soustraitance(
            contract_id=contract_id,
            user_id=user_id
        )

        return _soustraitance_to_response(contract)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/soustraitance", response_model=List[SoustraitanceResponse])
async def list_soustraitance():
    """List all sous-traitance contracts - CHRONOLOGICAL (Rule #5)"""
    agent = get_transport_agent()
    contracts = await agent.get_soustraitance_contracts()
    return [_soustraitance_to_response(c) for c in contracts]


def _soustraitance_to_response(contract) -> SoustraitanceResponse:
    """Convert SoustraitanceContract to response"""
    return SoustraitanceResponse(
        id=contract.id,
        contract_number=contract.contract_number,
        soustraitance_type=contract.soustraitance_type.value,
        status=contract.status.value,
        trip_id=contract.trip_id,
        partner_name=contract.partner_name,
        partner_contact=contract.partner_contact,
        agreed_price=float(contract.agreed_price),
        commission_rate=contract.commission_rate,
        requested_at=contract.requested_at,
        confirmed_at=contract.confirmed_at,
        approved_by=contract.approved_by,
        approved_at=contract.approved_at,
        rejection_reason=contract.rejection_reason,
        created_at=contract.created_at
    )


# ============================================================================
# POOLING / COVOITURAGE ENDPOINTS
# ============================================================================

@router.get("/pooling/opportunities")
async def get_pooling_opportunities():
    """Get pooling/covoiturage opportunities - CHRONOLOGICAL (Rule #5)"""
    agent = get_transport_agent()
    opportunities = await agent.get_pooling_opportunities()

    return [
        {
            "id": str(o.id),
            "opportunity_type": o.opportunity_type,
            "base_trip_id": str(o.base_trip_id),
            "candidate_trip_ids": [str(tid) for tid in o.candidate_trip_ids],
            "estimated_savings_percent": o.estimated_savings_percent,
            "estimated_emissions_saved_kg": o.estimated_emissions_saved_kg,
            "feasibility_score": o.feasibility_score,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
            "expires_at": o.expires_at.isoformat()
        }
        for o in opportunities
    ]


@router.post("/pooling/{opportunity_id}/accept")
async def accept_pooling_opportunity(
    opportunity_id: UUID,
    user_id: UUID = Query(default_factory=uuid4)
):
    """Accept a pooling opportunity"""
    agent = get_transport_agent()

    try:
        opportunity = await agent.accept_pooling_opportunity(
            opportunity_id=opportunity_id,
            user_id=user_id
        )
        return {
            "status": "success",
            "message": "Pooling opportunity accepted - trips combined",
            "opportunity_id": str(opportunity.id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# FLOW ENDPOINTS (Visualisation iPad Beach)
# ============================================================================

@router.get("/flow/score", response_model=FlowScoreResponse)
async def get_flow_score():
    """
    Get global flow score (Friction vs Fluidite)
    For iPad beach visualization - 999Hz inspiration
    """
    agent = get_transport_agent()
    score = await agent.get_global_flow_score()

    return FlowScoreResponse(
        global_fluidity=score["global_fluidity"],
        global_friction=score["global_friction"],
        flow_status=score["flow_status"],
        color_hex=score["color_hex"],
        message=score["message"],
        zones_monitored=score.get("zones_monitored"),
        vehicles_active=score.get("vehicles_active")
    )


@router.get("/summary")
async def get_transport_summary():
    """Get transport dashboard summary"""
    agent = get_transport_agent()
    summary = await agent.get_transport_summary()
    return summary


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check for transport service"""
    return {
        "status": "healthy",
        "service": "transport",
        "version": "V68",
        "module": "AT·OM Flow",
        "governance": {
            "rule_1": "Dispatch haute valeur + sous-traitance require APPROVAL",
            "rule_5": "All listings ALPHABETICAL or CHRONOLOGICAL",
            "rule_6": "Full audit trail"
        }
    }


@router.get("/info")
async def service_info():
    """Service information"""
    return {
        "name": "CHE·NU Transport & Logistics",
        "module": "AT·OM Flow",
        "version": "V68",
        "description": "Gestion intelligente des transports - Dispatch collaboratif",
        "features": [
            "Fleet Management",
            "Dispatch Collaboratif",
            "Che-Nu Zones (Placement Intelligent)",
            "Covoiturage & Pooling",
            "Sous-traitance Integration (Uber, Taxi)",
            "Flow Map Visualization (999Hz)",
            "Governance Compliance"
        ],
        "agent_count": 50,
        "agent_categories": {
            "sonde": 10,
            "optimiseurs": 15,
            "dispatch": 15,
            "flow": 10
        },
        "governance_compliance": {
            "rule_1": True,
            "rule_5": True,
            "rule_6": True
        }
    }
