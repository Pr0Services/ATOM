"""
CHE·NU V68 - Construction & Field Services Tests
Vertical 13: Procore Killer

Tests governance compliance:
- Rule #1: Safety inspections and change orders require approval
- Rule #5: Projects ALPHABETICAL, RFIs CHRONOLOGICAL, subcontractors ALPHABETICAL (NOT by rating)
- Rule #6: Full audit trail with UUID, timestamps
"""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, date
from decimal import Decimal

import sys
sys.path.insert(0, '/home/claude/CONSTRUCTION_V68/backend')

from spheres.construction.agents.construction_agent import (
    ConstructionAgent,
    ProjectStatus,
    RFIStatus,
    PunchItemStatus,
    SafetyStatus,
    ChangeOrderStatus,
    EquipmentStatus,
    TaskPriority,
    WeatherCondition
)


@pytest.fixture
def agent():
    """Create fresh Construction agent for each test."""
    return ConstructionAgent()


@pytest.fixture
def user_id():
    return uuid4()


# ============================================================
# PROJECT MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_project(agent, user_id):
    """Test project creation."""
    project = await agent.create_project(
        name="Office Tower Phase 1",
        description="New commercial office building",
        client_name="ABC Corporation",
        location="123 Main St, Montreal",
        budget=Decimal("5000000.00"),
        start_date=date(2026, 2, 1),
        end_date=date(2027, 6, 30),
        created_by=user_id
    )
    
    assert project is not None
    assert isinstance(project.id, UUID)
    assert project.name == "Office Tower Phase 1"
    assert project.status == ProjectStatus.PLANNING
    assert project.created_by == user_id
    assert project.project_number == "PRJ-001"


@pytest.mark.asyncio
async def test_projects_alphabetical_rule5(agent, user_id):
    """RULE #5: Projects must be listed ALPHABETICALLY, not by budget."""
    await agent.create_project(
        name="Zebra Plaza", description="D1", client_name="C1",
        location="L1", budget=Decimal("1000000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    await agent.create_project(
        name="Alpha Center", description="D2", client_name="C2",
        location="L2", budget=Decimal("5000000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    await agent.create_project(
        name="Metro Tower", description="D3", client_name="C3",
        location="L3", budget=Decimal("3000000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    projects = await agent.get_projects(user_id=user_id)
    
    assert len(projects) >= 3
    names = [p.name for p in projects]
    assert names == sorted(names), "RULE #5 VIOLATION: Projects must be ALPHABETICAL"


# ============================================================
# RFI MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_rfi(agent, user_id):
    """Test RFI creation with sequential numbering."""
    project = await agent.create_project(
        name="Test Project", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    rfi = await agent.create_rfi(
        project_id=project.id,
        subject="Structural beam specifications",
        question="What are the load requirements for Level 3?",
        submitted_by=user_id
    )
    
    assert rfi is not None
    assert rfi.rfi_number == "RFI-001"
    assert rfi.status == RFIStatus.DRAFT


# ============================================================
# DAILY LOG TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_daily_log(agent, user_id):
    """Test daily log creation."""
    project = await agent.create_project(
        name="Log Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    log = await agent.create_daily_log(
        project_id=project.id,
        log_date=date(2026, 1, 15),
        weather=WeatherCondition.SUNNY,
        temperature_high=72,
        temperature_low=55,
        workers_onsite=45,
        work_completed="Foundation pour complete",
        created_by=user_id
    )
    
    assert log is not None
    assert log.weather == WeatherCondition.SUNNY
    assert log.workers_onsite == 45
    assert log.created_by == user_id


# ============================================================
# PUNCH LIST TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_punch_item(agent, user_id):
    """Test punch list item creation."""
    project = await agent.create_project(
        name="Punch Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    item = await agent.create_punch_item(
        project_id=project.id,
        location="Level 2, Room 201",
        description="Paint touch-up required on wall",
        trade="Painting",
        created_by=user_id
    )
    
    assert item is not None
    assert item.location == "Level 2, Room 201"
    assert item.status == PunchItemStatus.OPEN
    assert item.created_by == user_id


@pytest.mark.asyncio
async def test_punch_items_alphabetical_by_location_rule5(agent, user_id):
    """RULE #5: Punch items ALPHABETICAL by location."""
    project = await agent.create_project(
        name="Punch Sort Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    await agent.create_punch_item(
        project_id=project.id, location="Zone C",
        description="Item 1", trade="T1", created_by=user_id
    )
    await agent.create_punch_item(
        project_id=project.id, location="Zone A",
        description="Item 2", trade="T2", created_by=user_id
    )
    await agent.create_punch_item(
        project_id=project.id, location="Zone B",
        description="Item 3", trade="T3", created_by=user_id
    )
    
    items = await agent.get_project_punch_items(project_id=project.id)
    
    locations = [i.location for i in items]
    assert locations == sorted(locations), \
        "RULE #5 VIOLATION: Punch items must be ALPHABETICAL by location"


# ============================================================
# SAFETY INSPECTION TESTS - GOVERNANCE
# ============================================================

@pytest.mark.asyncio
async def test_safety_inspection_requires_approval_rule1(agent, user_id):
    """RULE #1: Safety inspections require GOVERNANCE approval."""
    project = await agent.create_project(
        name="Safety Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    # Create inspection
    inspection = await agent.create_safety_inspection(
        project_id=project.id,
        inspection_type="Weekly Safety Walkthrough",
        inspector_name="John Smith",
        inspection_date=date(2026, 1, 20),
        created_by=user_id
    )
    
    assert inspection.status == SafetyStatus.SCHEDULED
    
    # Submit for approval
    submitted = await agent.submit_inspection_for_approval(
        inspection_id=inspection.id,
        findings=["All safety measures in compliance"],
        corrective_actions=[],
        user_id=user_id
    )
    
    assert submitted.status == SafetyStatus.PENDING_APPROVAL
    
    # GOVERNANCE: Approve inspection
    approved = await agent.approve_safety_inspection(
        inspection_id=inspection.id,
        passed=True,
        approver_id=uuid4()  # Safety manager
    )
    
    assert approved.status == SafetyStatus.PASSED
    assert approved.approved_by is not None


@pytest.mark.asyncio
async def test_safety_inspection_fail_governance(agent, user_id):
    """Test safety inspection failure with governance."""
    project = await agent.create_project(
        name="Safety Fail Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    inspection = await agent.create_safety_inspection(
        project_id=project.id,
        inspection_type="Daily Safety Check",
        inspector_name="Jane Doe",
        inspection_date=date(2026, 1, 20),
        created_by=user_id
    )
    
    await agent.submit_inspection_for_approval(
        inspection_id=inspection.id,
        findings=["Missing guardrails on Level 2"],
        corrective_actions=["Install guardrails immediately"],
        user_id=user_id
    )
    
    # GOVERNANCE: Fail inspection
    failed = await agent.approve_safety_inspection(
        inspection_id=inspection.id,
        passed=False,
        approver_id=uuid4(),
        notes="Critical safety violations found"
    )
    
    assert failed.status == SafetyStatus.FAILED


# ============================================================
# CHANGE ORDER TESTS - GOVERNANCE
# ============================================================

@pytest.mark.asyncio
async def test_change_order_requires_approval_rule1(agent, user_id):
    """RULE #1: Change orders require GOVERNANCE approval before execution."""
    project = await agent.create_project(
        name="CO Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("1000000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    # Create change order
    co = await agent.create_change_order(
        project_id=project.id,
        title="Emergency Exit Addition",
        description="Add emergency exit on Level 2",
        reason="Code compliance requirement",
        cost_impact=Decimal("75000.00"),
        schedule_impact_days=14,
        submitted_by=user_id
    )
    
    assert co.status == ChangeOrderStatus.DRAFT
    assert co.co_number == "CO-001"
    
    # Submit for approval
    submitted = await agent.submit_change_order(
        co_id=co.id,
        user_id=user_id
    )
    
    assert submitted.status == ChangeOrderStatus.SUBMITTED
    
    # GOVERNANCE: Approve
    approved = await agent.approve_change_order(
        co_id=co.id,
        approved=True,
        approver_id=uuid4()
    )
    
    assert approved.status == ChangeOrderStatus.APPROVED
    assert approved.approved_by is not None
    
    # Now can execute
    executed = await agent.execute_change_order(
        co_id=co.id,
        user_id=user_id
    )
    
    assert executed.status == ChangeOrderStatus.EXECUTED


@pytest.mark.asyncio
async def test_change_order_cannot_execute_without_approval(agent, user_id):
    """RULE #1: Cannot execute change order without approval."""
    project = await agent.create_project(
        name="CO Block Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("1000000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    co = await agent.create_change_order(
        project_id=project.id,
        title="Unapproved Change",
        description="Unapproved change",
        reason="Testing",
        cost_impact=Decimal("50000.00"),
        schedule_impact_days=7,
        submitted_by=user_id
    )
    
    # Try to execute without approval - should fail
    with pytest.raises(ValueError):
        await agent.execute_change_order(
            co_id=co.id,
            user_id=user_id
        )


# ============================================================
# EQUIPMENT MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_add_equipment(agent, user_id):
    """Test equipment addition."""
    equipment = await agent.add_equipment(
        name="Excavator CAT 320",
        equipment_type="Heavy Machinery",
        daily_rate=Decimal("1500.00"),
        created_by=user_id
    )
    
    assert equipment is not None
    assert equipment.name == "Excavator CAT 320"
    assert equipment.status == EquipmentStatus.AVAILABLE


@pytest.mark.asyncio
async def test_equipment_alphabetical_rule5(agent, user_id):
    """RULE #5: Equipment listed ALPHABETICALLY."""
    await agent.add_equipment(
        name="Crane Tower", equipment_type="Heavy",
        daily_rate=Decimal("2000.00"), created_by=user_id
    )
    await agent.add_equipment(
        name="Air Compressor", equipment_type="Tools",
        daily_rate=Decimal("200.00"), created_by=user_id
    )
    await agent.add_equipment(
        name="Bulldozer D9", equipment_type="Heavy",
        daily_rate=Decimal("1800.00"), created_by=user_id
    )
    
    equipment = await agent.get_equipment()
    
    names = [e.name for e in equipment]
    assert names == sorted(names), \
        "RULE #5 VIOLATION: Equipment must be ALPHABETICAL"


# ============================================================
# SUBCONTRACTOR MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_add_subcontractor(agent, user_id):
    """Test subcontractor addition."""
    sub = await agent.add_subcontractor(
        company_name="ABC Electrical",
        contact_name="John Smith",
        email="john@abcelectrical.com",
        phone="555-1234",
        trade="Electrical",
        created_by=user_id,
        license_number="EL-12345"
    )
    
    assert sub is not None
    assert sub.company_name == "ABC Electrical"
    assert sub.trade == "Electrical"


@pytest.mark.asyncio
async def test_subcontractors_alphabetical_not_by_rating_rule5(agent, user_id):
    """RULE #5: Subcontractors ALPHABETICAL by company name, NOT by rating."""
    await agent.add_subcontractor(
        company_name="Zephyr HVAC", contact_name="Z",
        email="z@z.com", phone="555-1111", trade="HVAC",
        created_by=user_id, license_number="H1"
    )
    await agent.add_subcontractor(
        company_name="Alpha Plumbing", contact_name="A",
        email="a@a.com", phone="555-2222", trade="Plumbing",
        created_by=user_id, license_number="P1"
    )
    await agent.add_subcontractor(
        company_name="Metro Electric", contact_name="M",
        email="m@m.com", phone="555-3333", trade="Electrical",
        created_by=user_id, license_number="E1"
    )
    
    subs = await agent.get_subcontractors()
    
    names = [s.company_name for s in subs]
    assert names == sorted(names), \
        "RULE #5 VIOLATION: Subcontractors must be ALPHABETICAL by company name"


# ============================================================
# TASK MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_task(agent, user_id):
    """Test task creation."""
    project = await agent.create_project(
        name="Task Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("100000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    task = await agent.create_task(
        project_id=project.id,
        title="Install electrical conduits Level 1",
        description="Run conduits for main power distribution",
        priority=TaskPriority.HIGH,
        due_date=date(2026, 2, 15),
        created_by=user_id
    )
    
    assert task is not None
    assert task.title == "Install electrical conduits Level 1"
    assert task.priority == TaskPriority.HIGH


# ============================================================
# ANALYTICS TESTS
# ============================================================

@pytest.mark.asyncio
async def test_project_analytics(agent, user_id):
    """Test project analytics."""
    project = await agent.create_project(
        name="Analytics Test", description="Test", client_name="Test",
        location="Test", budget=Decimal("500000.00"),
        start_date=date(2026, 1, 1), created_by=user_id
    )
    
    # Add some items
    await agent.create_rfi(
        project_id=project.id, subject="RFI 1",
        question="Q1", submitted_by=user_id
    )
    await agent.create_change_order(
        project_id=project.id, title="CO 1",
        description="Test", reason="Reason",
        cost_impact=Decimal("10000.00"),
        schedule_impact_days=5, submitted_by=user_id
    )
    
    stats = await agent.get_project_summary(project_id=project.id)
    
    assert stats is not None
    assert "counts" in stats
    assert "open_rfis" in stats["counts"]


# ============================================================
# AGENT INITIALIZATION TEST
# ============================================================

def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent is not None
    assert hasattr(agent, 'projects')
    assert hasattr(agent, 'rfis')
    assert hasattr(agent, 'change_orders')
    assert hasattr(agent, 'equipment')
    assert hasattr(agent, 'subcontractors')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
