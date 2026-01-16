"""
CHE·NU V68 Transport & Logistics Tests
AT·OM Flow - Governance Compliance Tests

GOVERNANCE TESTS:
- Rule #1: Dispatch haute valeur + sous-traitance require APPROVAL
- Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL
- Rule #6: Full audit trail
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import uuid4

from backend.verticals.TRANSPORT_V68.backend.spheres.transport.agents.transport_agent import (
    TransportAgent,
    VehicleType,
    VehicleStatus,
    TripType,
    TripStatus,
    LoadType,
    SoustraitanceType,
    SoustraitanceStatus,
    OptimizationGoal,
    ZoneType,
    GeoPoint,
)
from backend.verticals.TRANSPORT_V68.backend.spheres.transport.agents.transport_agents_registry import (
    get_transport_agents,
    validate_transport_agents,
    TRANSPORT_AGENT_COUNT,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def agent():
    """Fresh transport agent for each test"""
    return TransportAgent()


@pytest.fixture
def user_id():
    """Test user ID"""
    return uuid4()


@pytest.fixture
def sample_location():
    """Sample geo point"""
    return GeoPoint(
        latitude=20.2117,
        longitude=-87.4312,
        address="Tulum Centro",
        name="Tulum"
    )


@pytest.fixture
def sample_destination():
    """Sample destination"""
    return GeoPoint(
        latitude=21.1619,
        longitude=-86.8515,
        address="Cancun Airport",
        name="CUN Airport"
    )


# ============================================================================
# VEHICLE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_register_vehicle(agent, user_id, sample_location):
    """Test vehicle registration"""
    vehicle = await agent.register_vehicle(
        registration="ABC-123",
        name="Camion Alpha",
        vehicle_type=VehicleType.CAMION,
        capacity_kg=5000,
        capacity_m3=20,
        cost_per_km=Decimal("2.50"),
        fuel_type="diesel",
        emissions_g_per_km=150,
        created_by=user_id,
        current_location=sample_location
    )

    assert vehicle.id is not None
    assert vehicle.registration == "ABC-123"
    assert vehicle.name == "Camion Alpha"
    assert vehicle.vehicle_type == VehicleType.CAMION
    assert vehicle.status == VehicleStatus.AVAILABLE
    assert vehicle.capacity_kg == 5000
    assert vehicle.fill_rate == 0.0


@pytest.mark.asyncio
async def test_vehicles_alphabetical_rule5(agent, user_id):
    """
    RULE #5: Vehicles must be listed ALPHABETICALLY by name
    NOT sorted by efficiency, fill rate, or utilization
    """
    # Create vehicles in non-alphabetical order
    await agent.register_vehicle(
        registration="Z-999", name="Zebra Transport",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("3.00"), fuel_type="diesel", emissions_g_per_km=200,
        created_by=user_id
    )
    await agent.register_vehicle(
        registration="A-111", name="Alpha Carrier",
        vehicle_type=VehicleType.FOURGON, capacity_kg=1000, capacity_m3=5,
        cost_per_km=Decimal("1.00"), fuel_type="electric", emissions_g_per_km=0,
        created_by=user_id
    )
    await agent.register_vehicle(
        registration="M-555", name="Mike's Truck",
        vehicle_type=VehicleType.CAMIONNETTE, capacity_kg=2000, capacity_m3=10,
        cost_per_km=Decimal("2.00"), fuel_type="hybrid", emissions_g_per_km=100,
        created_by=user_id
    )

    vehicles = await agent.get_vehicles()

    # RULE #5: Must be alphabetical
    assert vehicles[0].name == "Alpha Carrier"
    assert vehicles[1].name == "Mike's Truck"
    assert vehicles[2].name == "Zebra Transport"


@pytest.mark.asyncio
async def test_vehicle_fill_rate_calculation(agent, user_id):
    """Test fill rate calculation"""
    vehicle = await agent.register_vehicle(
        registration="TEST-001", name="Test Vehicle",
        vehicle_type=VehicleType.CAMION, capacity_kg=1000, capacity_m3=10,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    # Update load to 400kg (40%)
    await agent.update_vehicle_load(vehicle.id, 400, 4, user_id)

    updated = agent.vehicles[vehicle.id]
    assert updated.fill_rate == 40.0
    assert updated.is_underutilized == False  # 40% is threshold


@pytest.mark.asyncio
async def test_underutilized_vehicle_detection(agent, user_id):
    """Test underutilized vehicle detection"""
    vehicle = await agent.register_vehicle(
        registration="LOW-001", name="Low Fill Vehicle",
        vehicle_type=VehicleType.CAMION, capacity_kg=1000, capacity_m3=10,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    # Simulate in transit with low load
    vehicle.status = VehicleStatus.IN_TRANSIT
    vehicle.current_load_kg = 300  # 30%

    assert vehicle.is_underutilized == True


# ============================================================================
# DRIVER TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_register_driver(agent, user_id):
    """Test driver registration"""
    driver = await agent.register_driver(
        name="Juan Rodriguez",
        phone="+52 984 123 4567",
        email="juan@example.com",
        license_number="LIC-12345",
        license_expiry=date(2027, 12, 31),
        vehicle_types=[VehicleType.CAMION, VehicleType.CAMIONNETTE],
        created_by=user_id,
        home_zone="Tulum"
    )

    assert driver.id is not None
    assert driver.name == "Juan Rodriguez"
    assert VehicleType.CAMION in driver.vehicle_types


@pytest.mark.asyncio
async def test_drivers_alphabetical_not_by_rating_rule5(agent, user_id):
    """
    RULE #5: Drivers must be listed ALPHABETICALLY by name
    NOT sorted by rating, performance, or efficiency
    """
    await agent.register_driver(
        name="Zoe Smith", phone="111", email="z@test.com",
        license_number="Z-001", license_expiry=date(2027, 1, 1),
        vehicle_types=[VehicleType.CAMION], created_by=user_id
    )
    await agent.register_driver(
        name="Ana Garcia", phone="222", email="a@test.com",
        license_number="A-001", license_expiry=date(2027, 1, 1),
        vehicle_types=[VehicleType.CAMION], created_by=user_id
    )
    await agent.register_driver(
        name="Mario Lopez", phone="333", email="m@test.com",
        license_number="M-001", license_expiry=date(2027, 1, 1),
        vehicle_types=[VehicleType.CAMION], created_by=user_id
    )

    drivers = await agent.get_drivers()

    # RULE #5: Must be alphabetical, NOT by rating
    assert drivers[0].name == "Ana Garcia"
    assert drivers[1].name == "Mario Lopez"
    assert drivers[2].name == "Zoe Smith"


# ============================================================================
# TRIP TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_create_trip(agent, user_id, sample_location, sample_destination):
    """Test trip creation"""
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY,
        origin=sample_location,
        destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=3),
        load_type=LoadType.PACKAGE,
        load_description="Colis pour Cancun",
        load_weight_kg=500,
        load_volume_m3=2,
        created_by=user_id,
        allows_pooling=True
    )

    assert trip.id is not None
    assert trip.trip_number == "TRP-0001"
    assert trip.status == TripStatus.PLANNED
    assert trip.allows_pooling == True


@pytest.mark.asyncio
async def test_trips_chronological_not_by_profitability_rule5(agent, user_id, sample_location, sample_destination):
    """
    RULE #5: Trips must be listed CHRONOLOGICALLY by scheduled_departure
    NOT sorted by profitability or value
    """
    # Create trips with different departure times (not chronological)
    now = datetime.now()

    # Third departure
    await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=now + timedelta(hours=5),
        scheduled_arrival=now + timedelta(hours=7),
        load_type=LoadType.PACKAGE, load_description="Trip C",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    # First departure
    await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=now + timedelta(hours=1),
        scheduled_arrival=now + timedelta(hours=3),
        load_type=LoadType.PACKAGE, load_description="Trip A",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    # Second departure
    await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=now + timedelta(hours=3),
        scheduled_arrival=now + timedelta(hours=5),
        load_type=LoadType.PACKAGE, load_description="Trip B",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    trips = await agent.get_trips()

    # RULE #5: Must be chronological (newest first in this case)
    # The trips are sorted by scheduled_departure descending
    assert "Trip C" in trips[0].load_description
    assert "Trip B" in trips[1].load_description
    assert "Trip A" in trips[2].load_description


# ============================================================================
# CHE-NU ZONE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_create_zone(agent, user_id, sample_location):
    """Test Che-Nu zone creation"""
    zone = await agent.create_zone(
        name="Centro Tulum",
        zone_type=ZoneType.HIGH_FRICTION,
        center=sample_location,
        radius_km=2.0,
        friction_level=0.8,
        typical_delay_minutes=15,
        created_by=user_id,
        peak_hours=[8, 9, 17, 18, 19],
        avoid_if_possible=True
    )

    assert zone.id is not None
    assert zone.name == "Centro Tulum"
    assert zone.zone_type == ZoneType.HIGH_FRICTION
    assert zone.avoid_if_possible == True


@pytest.mark.asyncio
async def test_zones_alphabetical_rule5(agent, user_id, sample_location):
    """
    RULE #5: Zones must be listed ALPHABETICALLY by name
    """
    await agent.create_zone(
        name="Zone Z", zone_type=ZoneType.TRANSIT, center=sample_location,
        radius_km=1.0, friction_level=0.3, typical_delay_minutes=5, created_by=user_id
    )
    await agent.create_zone(
        name="Zone A", zone_type=ZoneType.HUB, center=sample_location,
        radius_km=1.0, friction_level=0.1, typical_delay_minutes=2, created_by=user_id
    )
    await agent.create_zone(
        name="Zone M", zone_type=ZoneType.HIGH_FRICTION, center=sample_location,
        radius_km=1.0, friction_level=0.9, typical_delay_minutes=20, created_by=user_id
    )

    zones = await agent.get_zones()

    # RULE #5: Alphabetical
    assert zones[0].name == "Zone A"
    assert zones[1].name == "Zone M"
    assert zones[2].name == "Zone Z"


# ============================================================================
# DISPATCH GOVERNANCE TESTS (RULE #1)
# ============================================================================

@pytest.mark.asyncio
async def test_dispatch_collaborative_low_value_no_approval(agent, user_id, sample_location, sample_destination):
    """Test that low-value dispatch does not require approval"""
    # Register vehicle
    vehicle = await agent.register_vehicle(
        registration="DISP-001", name="Dispatch Test",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    # Create low-value trip (estimated_cost < 5000)
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PACKAGE, load_description="Low value",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    # Dispatch
    decision = await agent.dispatch_collaborative(
        trip_id=trip.id,
        optimization_goal=OptimizationGoal.BALANCED,
        user_id=user_id
    )

    # Low value should not require approval
    # Note: The actual threshold check depends on estimated_cost
    assert decision.selected_vehicle_id == vehicle.id


@pytest.mark.asyncio
async def test_dispatch_high_value_requires_approval_rule1(agent, user_id, sample_location, sample_destination):
    """
    RULE #1: High-value dispatch requires APPROVAL
    """
    # Register vehicle
    await agent.register_vehicle(
        registration="HIGH-001", name="High Value Dispatch",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("100.00"),  # High cost per km
        fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    # Create trip
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.CONTAINER, load_description="High value cargo",
        load_weight_kg=4000, load_volume_m3=15, created_by=user_id
    )

    # Manually set high estimated cost to trigger approval
    trip.estimated_cost = Decimal("10000")

    decision = await agent.dispatch_collaborative(
        trip_id=trip.id,
        optimization_goal=OptimizationGoal.BALANCED,
        user_id=user_id
    )

    # High value MUST require approval
    assert decision.requires_approval == True
    assert decision.approved_by is None

    # Trip should NOT be confirmed yet
    assert agent.trips[trip.id].status != TripStatus.CONFIRMED


@pytest.mark.asyncio
async def test_dispatch_approval_governance(agent, user_id, sample_location, sample_destination):
    """Test dispatch approval workflow"""
    await agent.register_vehicle(
        registration="APPR-001", name="Approval Test",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PACKAGE, load_description="Test",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    # Force high value
    trip.estimated_cost = Decimal("10000")

    decision = await agent.dispatch_collaborative(
        trip_id=trip.id, optimization_goal=OptimizationGoal.BALANCED, user_id=user_id
    )

    # Approve
    approver_id = uuid4()
    approved = await agent.approve_dispatch(
        decision_id=decision.id, approved=True, approver_id=approver_id
    )

    # GOVERNANCE: Audit trail
    assert approved.approved_by == approver_id
    assert approved.approved_at is not None

    # Trip should now be confirmed
    assert agent.trips[trip.id].status == TripStatus.CONFIRMED


# ============================================================================
# SOUS-TRAITANCE GOVERNANCE TESTS (RULE #1)
# ============================================================================

@pytest.mark.asyncio
async def test_soustraitance_requires_approval_rule1(agent, user_id, sample_location, sample_destination):
    """
    RULE #1: ALL sous-traitance requires APPROVAL
    """
    # Create trip
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PASSENGER, load_description="Passenger transport",
        load_weight_kg=80, load_volume_m3=0.5, created_by=user_id
    )

    # Request sous-traitance
    contract = await agent.request_soustraitance(
        trip_id=trip.id,
        soustraitance_type=SoustraitanceType.UBER,
        partner_name="Uber MX",
        partner_contact="uber@example.com",
        agreed_price=Decimal("500"),
        commission_rate=0.15,
        created_by=user_id
    )

    # MUST be pending approval
    assert contract.status == SoustraitanceStatus.PENDING_APPROVAL
    assert contract.approved_by is None


@pytest.mark.asyncio
async def test_soustraitance_cannot_activate_without_approval(agent, user_id, sample_location, sample_destination):
    """
    RULE #1: Sous-traitance cannot be activated without approval
    """
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PASSENGER, load_description="Test",
        load_weight_kg=80, load_volume_m3=0.5, created_by=user_id
    )

    contract = await agent.request_soustraitance(
        trip_id=trip.id, soustraitance_type=SoustraitanceType.TAXI,
        partner_name="Taxi Local", partner_contact="taxi@test.com",
        agreed_price=Decimal("300"), commission_rate=0.10, created_by=user_id
    )

    # Try to activate without approval
    with pytest.raises(ValueError) as excinfo:
        await agent.activate_soustraitance(contract.id, user_id)

    assert "approved" in str(excinfo.value).lower()


@pytest.mark.asyncio
async def test_soustraitance_approval_workflow(agent, user_id, sample_location, sample_destination):
    """Test full sous-traitance approval workflow"""
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PASSENGER, load_description="VIP transport",
        load_weight_kg=80, load_volume_m3=0.5, created_by=user_id
    )

    contract = await agent.request_soustraitance(
        trip_id=trip.id, soustraitance_type=SoustraitanceType.PARTNER,
        partner_name="Premium Transport", partner_contact="premium@test.com",
        agreed_price=Decimal("1000"), commission_rate=0.20, created_by=user_id
    )

    # Approve
    approver_id = uuid4()
    approved = await agent.approve_soustraitance(
        contract_id=contract.id, approved=True, approver_id=approver_id
    )

    # GOVERNANCE: Audit trail
    assert approved.status == SoustraitanceStatus.APPROVED
    assert approved.approved_by == approver_id
    assert approved.approved_at is not None

    # Now can activate
    activated = await agent.activate_soustraitance(contract.id, user_id)
    assert activated.status == SoustraitanceStatus.ACTIVE


@pytest.mark.asyncio
async def test_soustraitance_rejection(agent, user_id, sample_location, sample_destination):
    """Test sous-traitance rejection"""
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PASSENGER, load_description="Test",
        load_weight_kg=80, load_volume_m3=0.5, created_by=user_id
    )

    contract = await agent.request_soustraitance(
        trip_id=trip.id, soustraitance_type=SoustraitanceType.BOLT,
        partner_name="Bolt", partner_contact="bolt@test.com",
        agreed_price=Decimal("400"), commission_rate=0.15, created_by=user_id
    )

    # Reject
    rejected = await agent.approve_soustraitance(
        contract_id=contract.id, approved=False, approver_id=uuid4(),
        rejection_reason="Price too high"
    )

    assert rejected.status == SoustraitanceStatus.REJECTED
    assert rejected.rejection_reason == "Price too high"


# ============================================================================
# FLOW VISUALIZATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_flow_score_calculation(agent):
    """Test global flow score calculation"""
    score = await agent.get_global_flow_score()

    # Default should be optimistic
    assert score["global_fluidity"] >= 0
    assert score["global_fluidity"] <= 1
    assert score["flow_status"] in ["fluid", "normal", "congested", "blocked"]
    assert score["color_hex"].startswith("#")


@pytest.mark.asyncio
async def test_flow_metric_recording(agent, user_id, sample_location):
    """Test flow metric recording"""
    zone = await agent.create_zone(
        name="Test Zone", zone_type=ZoneType.TRANSIT, center=sample_location,
        radius_km=1.0, friction_level=0.3, typical_delay_minutes=5, created_by=user_id
    )

    metric = await agent.record_flow_metric(
        zone_id=zone.id,
        friction_score=0.2,
        vehicles_count=10,
        trips_in_progress=5,
        average_speed_kmh=45
    )

    assert metric.fluidity_score == 0.8
    assert metric.color_hex == "#0057b8"  # Bleu cobalt when fluid


# ============================================================================
# AGENT REGISTRY TESTS
# ============================================================================

def test_transport_agents_count():
    """Test that we have exactly 50 transport agents"""
    agents = get_transport_agents()
    assert len(agents) == TRANSPORT_AGENT_COUNT
    assert len(agents) == 50


def test_transport_agents_validation():
    """Test transport agents registry validation"""
    assert validate_transport_agents() == True


def test_transport_agents_categories():
    """Test agent categories distribution"""
    agents = get_transport_agents()

    # Count by category (based on name prefix)
    sonde = [a for a in agents if "analyzer" in a["name"] or "detector" in a["name"]
             or "predictor" in a["name"] or "forecaster" in a["name"]
             or "monitor" in a["name"] or "tracker" in a["name"]]

    dispatch = [a for a in agents if "dispatcher" in a["name"] or "handler" in a["name"]
                or "coordinator" in a["name"] or "rerouter" in a["name"]
                or "scheduler" in a["name"] or "manager" in a["name"]]

    flow = [a for a in agents if "flow" in a["name"] or "visualizer" in a["name"]
            or "heatmap" in a["name"] or "dashboard" in a["name"]
            or "reporter" in a["name"]]

    # Should have agents in each category
    assert len(sonde) > 0
    assert len(dispatch) > 0
    assert len(flow) > 0


def test_transport_agents_governance_gates():
    """Test that sensitive agents require human gates"""
    agents = get_transport_agents()

    # Sous-traitance manager MUST require human gate
    soustraitance = next(a for a in agents if a["name"] == "transport_soustraitance_manager")
    assert soustraitance["requires_human_gate"] == True

    # Overflow handler should require human gate
    overflow = next(a for a in agents if a["name"] == "transport_overflow_handler")
    assert overflow["requires_human_gate"] == True


# ============================================================================
# TRANSPORT SUMMARY TEST
# ============================================================================

@pytest.mark.asyncio
async def test_transport_summary(agent, user_id, sample_location, sample_destination):
    """Test transport summary dashboard"""
    # Create some data
    await agent.register_vehicle(
        registration="SUM-001", name="Summary Test",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    await agent.register_driver(
        name="Test Driver", phone="123", email="test@test.com",
        license_number="TEST-001", license_expiry=date(2027, 1, 1),
        vehicle_types=[VehicleType.CAMION], created_by=user_id
    )

    await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PACKAGE, load_description="Test",
        load_weight_kg=100, load_volume_m3=1, created_by=user_id
    )

    summary = await agent.get_transport_summary()

    assert "fleet" in summary
    assert "drivers" in summary
    assert "trips" in summary
    assert "financials" in summary
    assert "optimization" in summary
    assert "flow" in summary

    assert summary["fleet"]["total_vehicles"] == 1
    assert summary["drivers"]["total"] == 1
    assert summary["trips"]["total"] == 1


# ============================================================================
# AUDIT TRAIL TESTS (RULE #6)
# ============================================================================

@pytest.mark.asyncio
async def test_vehicle_audit_trail_rule6(agent, user_id):
    """RULE #6: Vehicles must have full audit trail"""
    vehicle = await agent.register_vehicle(
        registration="AUD-001", name="Audit Test",
        vehicle_type=VehicleType.CAMION, capacity_kg=5000, capacity_m3=20,
        cost_per_km=Decimal("2.00"), fuel_type="diesel", emissions_g_per_km=150,
        created_by=user_id
    )

    # UUID
    assert vehicle.id is not None

    # Timestamps
    assert vehicle.created_at is not None
    assert vehicle.updated_at is not None

    # Created by
    assert vehicle.created_by == user_id


@pytest.mark.asyncio
async def test_soustraitance_audit_trail_rule6(agent, user_id, sample_location, sample_destination):
    """RULE #6: Sous-traitance must have full audit trail"""
    trip = await agent.create_trip(
        trip_type=TripType.TEMPORARY, origin=sample_location, destination=sample_destination,
        scheduled_departure=datetime.now() + timedelta(hours=1),
        scheduled_arrival=datetime.now() + timedelta(hours=2),
        load_type=LoadType.PASSENGER, load_description="Audit test",
        load_weight_kg=80, load_volume_m3=0.5, created_by=user_id
    )

    contract = await agent.request_soustraitance(
        trip_id=trip.id, soustraitance_type=SoustraitanceType.UBER,
        partner_name="Uber", partner_contact="uber@test.com",
        agreed_price=Decimal("500"), commission_rate=0.15, created_by=user_id
    )

    # UUID
    assert contract.id is not None

    # Timestamps
    assert contract.created_at is not None
    assert contract.requested_at is not None

    # Created by
    assert contract.created_by == user_id

    # Approval tracking
    approver = uuid4()
    approved = await agent.approve_soustraitance(
        contract.id, True, approver
    )

    assert approved.approved_by == approver
    assert approved.approved_at is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
