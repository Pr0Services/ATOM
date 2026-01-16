"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ REAL ESTATE TESTS — V68                           ║
║                                                                              ║
║  Comprehensive test suite for property management with RBQ compliance.       ║
║  Target: 95%+ pass rate                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import sys
sys.path.insert(0, '/home/claude/REAL_ESTATE_V68/backend')

from spheres.immobilier.agents.real_estate_agent import (
    RealEstateAgent,
    RealEstateAIEngine,
    RBQVerificationService,
    Property,
    Tenant,
    Lease,
    MaintenanceRequest,
    Contractor,
    Payment,
    PropertyType,
    PropertyStatus,
    LeaseStatus,
    MaintenanceStatus,
    MaintenancePriority,
    RBQCategory,
    get_real_estate_agent,
)


# ═══════════════════════════════════════════════════════════════════════════════
# AI ENGINE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRealEstateAIEngine:
    """Tests for RealEstateAIEngine."""
    
    @pytest.fixture
    def engine(self):
        return RealEstateAIEngine()
    
    @pytest.fixture
    def sample_property(self):
        return Property(
            id="prop_001",
            name="Test Duplex",
            address="123 Test St",
            city="Montréal",
            province="QC",
            postal_code="H2X 1X1",
            property_type=PropertyType.DUPLEX,
            status=PropertyStatus.RENTED,
            units=2,
            bedrooms=4,
            bathrooms=2.0,
            square_feet=2400,
            year_built=1975,
            purchase_price=Decimal("500000"),
            current_value=Decimal("650000"),
            monthly_rent=Decimal("3000"),
            monthly_expenses=Decimal("500"),
            municipal_tax=Decimal("4000"),
            school_tax=Decimal("500"),
            user_id="test_user",
        )
    
    @pytest.mark.asyncio
    async def test_analyze_property_positive_cash_flow(self, engine, sample_property):
        """Test property analysis with positive cash flow."""
        analysis = await engine.analyze_property(sample_property)
        
        assert analysis is not None
        assert analysis.property_id == "prop_001"
        assert analysis.cap_rate > 0
        assert analysis.monthly_cash_flow > 0  # Should be positive
        assert len(analysis.insights) > 0
        assert analysis.market_position in ["above_market", "at_market", "below_market"]
    
    @pytest.mark.asyncio
    async def test_analyze_property_cap_rate_calculation(self, engine, sample_property):
        """Test cap rate calculation accuracy."""
        analysis = await engine.analyze_property(sample_property)
        
        # Manual calculation: (3000 * 12) / 650000 * 100 = 5.54%
        expected_cap_rate = (float(sample_property.monthly_rent) * 12 / float(sample_property.current_value)) * 100
        assert abs(analysis.cap_rate - expected_cap_rate) < 0.01
    
    @pytest.mark.asyncio
    async def test_analyze_property_old_building_risk(self, engine, sample_property):
        """Test that old buildings generate risk warnings."""
        sample_property.year_built = 1960  # Over 50 years old
        analysis = await engine.analyze_property(sample_property)
        
        # Should have risk about old building
        has_age_risk = any("50 years" in risk.lower() or "repairs" in risk.lower() for risk in analysis.risks)
        assert has_age_risk or len(analysis.risks) > 0
    
    def test_rent_increase_calculation_2024(self, engine):
        """Test TAL rent increase calculation for 2024."""
        result = engine.calculate_rent_increase(Decimal("1500"), 2024)
        
        assert result is not None
        assert result["current_rent"] == 1500
        assert result["allowed_increase_percent"] == 2.8
        assert result["new_rent"] > 1500
        assert "TAL" in result["source"]
    
    def test_rent_increase_calculation_2025(self, engine):
        """Test TAL rent increase calculation for 2025."""
        result = engine.calculate_rent_increase(Decimal("1200"), 2025)
        
        assert result["year"] == 2025
        assert result["allowed_increase_percent"] == 3.0
        assert result["increase_amount"] == pytest.approx(36, rel=0.01)  # 1200 * 3%


# ═══════════════════════════════════════════════════════════════════════════════
# RBQ VERIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRBQVerificationService:
    """Tests for RBQ license verification."""
    
    @pytest.fixture
    def service(self):
        return RBQVerificationService()
    
    @pytest.mark.asyncio
    async def test_verify_valid_license(self, service):
        """Test verification of valid RBQ license."""
        result = await service.verify_license("1234-5678-90")
        
        assert result.is_valid == True
        assert result.license_number == "1234-5678-90"
        assert result.holder_name == "Construction ABC Inc."
        assert len(result.categories) > 0
        assert result.status == "Active"
    
    @pytest.mark.asyncio
    async def test_verify_expired_license(self, service):
        """Test verification of expired RBQ license."""
        result = await service.verify_license("9999-0000-00")
        
        assert result.is_valid == False
        assert result.status == "Expired"
        assert len(result.restrictions) > 0
    
    @pytest.mark.asyncio
    async def test_verify_unknown_license(self, service):
        """Test verification of unknown RBQ license."""
        result = await service.verify_license("5555-1234-56")
        
        assert result.is_valid == True  # Default mock returns valid
        assert result.license_number == "5555-1234-56"
    
    def test_get_category_name(self, service):
        """Test RBQ category name lookup."""
        assert "général" in service.get_category_name("1.1").lower()
        assert "résidentiel" in service.get_category_name("1.2").lower()
        assert "plomberie" in service.get_category_name("15").lower() or "mécanique" in service.get_category_name("15").lower()


# ═══════════════════════════════════════════════════════════════════════════════
# PROPERTY OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPropertyOperations:
    """Tests for property CRUD operations."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    def test_create_property(self, agent):
        """Test property creation."""
        prop = agent.create_property(
            name="Test Property",
            address="456 Test Ave",
            city="Québec",
            user_id="test_user",
            property_type=PropertyType.CONDO,
            units=1,
            bedrooms=2,
        )
        
        assert prop.id is not None
        assert prop.name == "Test Property"
        assert prop.city == "Québec"
        assert prop.province == "QC"
        assert prop.property_type == PropertyType.CONDO
        assert prop.status == PropertyStatus.AVAILABLE
        assert prop.user_id == "test_user"
    
    def test_get_property(self, agent):
        """Test property retrieval."""
        created = agent.create_property(
            name="Retrieve Test",
            address="789 Get St",
            city="Laval",
            user_id="test_user",
        )
        
        retrieved = agent.get_property(created.id, "test_user")
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "Retrieve Test"
    
    def test_get_property_wrong_user(self, agent):
        """Test that users can only access their own properties."""
        created = agent.create_property(
            name="Private Property",
            address="Secret St",
            city="Montréal",
            user_id="user_a",
        )
        
        # Different user should not find it
        retrieved = agent.get_property(created.id, "user_b")
        assert retrieved is None
    
    def test_update_property(self, agent):
        """Test property update."""
        prop = agent.create_property(
            name="Update Test",
            address="Update St",
            city="Gatineau",
            user_id="test_user",
        )
        
        updated = agent.update_property(
            prop.id,
            "test_user",
            name="Updated Name",
            status=PropertyStatus.RENTED,
            monthly_rent=Decimal("1500"),
        )
        
        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.status == PropertyStatus.RENTED
        assert updated.monthly_rent == Decimal("1500")
    
    def test_list_properties_by_type(self, agent):
        """Test property listing with type filter."""
        agent.create_property(name="Condo 1", address="A", city="MTL", user_id="user", property_type=PropertyType.CONDO)
        agent.create_property(name="Duplex 1", address="B", city="MTL", user_id="user", property_type=PropertyType.DUPLEX)
        agent.create_property(name="Condo 2", address="C", city="MTL", user_id="user", property_type=PropertyType.CONDO)
        
        condos = agent.list_properties("user", property_type=PropertyType.CONDO)
        assert len(condos) == 2
        assert all(p.property_type == PropertyType.CONDO for p in condos)
    
    def test_list_properties_by_city(self, agent):
        """Test property listing with city filter."""
        agent.create_property(name="P1", address="A", city="Montréal", user_id="user")
        agent.create_property(name="P2", address="B", city="Québec", user_id="user")
        agent.create_property(name="P3", address="C", city="montréal", user_id="user")  # lowercase
        
        montreal = agent.list_properties("user", city="Montréal")
        assert len(montreal) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# TENANT OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTenantOperations:
    """Tests for tenant CRUD operations."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    def test_create_tenant(self, agent):
        """Test tenant creation."""
        tenant = agent.create_tenant(
            first_name="Jean",
            last_name="Tremblay",
            email="jean@example.com",
            phone="514-555-1234",
            user_id="test_user",
        )
        
        assert tenant.id is not None
        assert tenant.first_name == "Jean"
        assert tenant.last_name == "Tremblay"
        assert tenant.email == "jean@example.com"
        assert tenant.is_active == True
        assert tenant.balance == Decimal("0")
    
    def test_get_tenant(self, agent):
        """Test tenant retrieval."""
        created = agent.create_tenant(
            first_name="Marie",
            last_name="Lavoie",
            email="marie@example.com",
            user_id="test_user",
        )
        
        retrieved = agent.get_tenant(created.id, "test_user")
        assert retrieved is not None
        assert retrieved.first_name == "Marie"
    
    def test_list_tenants_by_activity(self, agent):
        """Test tenant listing by activity status."""
        t1 = agent.create_tenant(first_name="A", last_name="A", email="a@a.com", user_id="user")
        t2 = agent.create_tenant(first_name="B", last_name="B", email="b@b.com", user_id="user")
        t2.is_active = False
        
        active = agent.list_tenants("user", is_active=True)
        assert all(t.is_active for t in active)


# ═══════════════════════════════════════════════════════════════════════════════
# LEASE OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestLeaseOperations:
    """Tests for lease operations."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    def test_create_lease(self, agent):
        """Test lease creation."""
        prop = agent.create_property(name="Lease Prop", address="A", city="MTL", user_id="user")
        tenant = agent.create_tenant(first_name="Test", last_name="Tenant", email="t@t.com", user_id="user")
        
        lease = agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1500"),
            security_deposit=Decimal("1500"),
            unit_number="1",
            user_id="user",
        )
        
        assert lease.id is not None
        assert lease.property_id == prop.id
        assert lease.tenant_id == tenant.id
        assert lease.status == LeaseStatus.ACTIVE
        assert lease.monthly_rent == Decimal("1500")
    
    def test_lease_updates_tenant(self, agent):
        """Test that lease creation updates tenant details."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user", monthly_rent=Decimal("0"))
        tenant = agent.create_tenant(first_name="T", last_name="T", email="t@t.com", user_id="user")
        
        agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1200"),
            security_deposit=Decimal("1200"),
            user_id="user",
        )
        
        updated_tenant = agent.get_tenant(tenant.id, "user")
        assert updated_tenant.property_id == prop.id
        assert updated_tenant.monthly_rent == Decimal("1200")
    
    def test_lease_updates_property_status(self, agent):
        """Test that lease creation updates property status to rented."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        tenant = agent.create_tenant(first_name="T", last_name="T", email="t@t.com", user_id="user")
        
        assert prop.status == PropertyStatus.AVAILABLE
        
        agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1000"),
            security_deposit=Decimal("1000"),
            user_id="user",
        )
        
        updated_prop = agent.get_property(prop.id, "user")
        assert updated_prop.status == PropertyStatus.RENTED
    
    def test_rent_increase_calculation(self, agent):
        """Test TAL-compliant rent increase calculation."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        tenant = agent.create_tenant(first_name="T", last_name="T", email="t@t.com", user_id="user")
        
        lease = agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1500"),
            security_deposit=Decimal("1500"),
            user_id="user",
        )
        
        result = agent.calculate_rent_increase(lease.id, "user", 2025)
        
        assert result is not None
        assert result["current_rent"] == 1500
        assert result["new_rent"] > 1500
        assert "TAL" in result["source"]


# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMaintenanceOperations:
    """Tests for maintenance operations."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    def test_create_maintenance_request(self, agent):
        """Test maintenance request creation."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        
        request = agent.create_maintenance_request(
            property_id=prop.id,
            title="Broken faucet",
            description="Kitchen faucet leaking",
            category="plumbing",
            priority=MaintenancePriority.HIGH,
            user_id="user",
        )
        
        assert request.id is not None
        assert request.title == "Broken faucet"
        assert request.status == MaintenanceStatus.OPEN
        assert request.priority == MaintenancePriority.HIGH
    
    def test_update_maintenance_status(self, agent):
        """Test maintenance status update."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        
        request = agent.create_maintenance_request(
            property_id=prop.id,
            title="Test",
            description="Test desc",
            category="other",
            priority=MaintenancePriority.MEDIUM,
            user_id="user",
        )
        
        updated = agent.update_maintenance_status(
            request.id,
            "user",
            MaintenanceStatus.IN_PROGRESS,
        )
        
        assert updated.status == MaintenanceStatus.IN_PROGRESS
    
    def test_complete_maintenance_sets_date(self, agent):
        """Test that completing maintenance sets completion date."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        
        request = agent.create_maintenance_request(
            property_id=prop.id,
            title="Test",
            description="Test desc",
            category="other",
            priority=MaintenancePriority.LOW,
            user_id="user",
        )
        
        updated = agent.update_maintenance_status(
            request.id,
            "user",
            MaintenanceStatus.COMPLETED,
        )
        
        assert updated.completed_date is not None
    
    def test_list_maintenance_sorted_by_priority(self, agent):
        """Test maintenance listing sorted by priority."""
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        
        agent.create_maintenance_request(prop.id, "Low", "D", "other", MaintenancePriority.LOW, "user")
        agent.create_maintenance_request(prop.id, "Emergency", "D", "other", MaintenancePriority.EMERGENCY, "user")
        agent.create_maintenance_request(prop.id, "High", "D", "other", MaintenancePriority.HIGH, "user")
        
        requests = agent.list_maintenance("user")
        
        assert requests[0].priority == MaintenancePriority.EMERGENCY
        assert requests[1].priority == MaintenancePriority.HIGH
        assert requests[2].priority == MaintenancePriority.LOW


# ═══════════════════════════════════════════════════════════════════════════════
# CONTRACTOR OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestContractorOperations:
    """Tests for contractor operations with RBQ compliance."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    @pytest.mark.asyncio
    async def test_create_contractor_with_rbq(self, agent):
        """Test contractor creation with RBQ verification."""
        contractor = await agent.create_contractor(
            name="Jean Plombier",
            phone="514-555-9999",
            company="JP Plomberie Inc",
            rbq_license="1234-5678-90",
            categories=["plumbing"],
            user_id="user",
        )
        
        assert contractor.id is not None
        assert contractor.name == "Jean Plombier"
        assert contractor.rbq_license == "1234-5678-90"
        assert contractor.rbq_verified == True
    
    @pytest.mark.asyncio
    async def test_create_contractor_with_invalid_rbq(self, agent):
        """Test contractor creation with invalid RBQ."""
        contractor = await agent.create_contractor(
            name="Bad Contractor",
            phone="514-555-0000",
            rbq_license="9999-0000-00",  # Expired license
            user_id="user",
        )
        
        assert contractor.rbq_verified == False
    
    @pytest.mark.asyncio
    async def test_verify_contractor_rbq(self, agent):
        """Test RBQ verification for existing contractor."""
        contractor = await agent.create_contractor(
            name="Verify Test",
            phone="514-555-1111",
            rbq_license="1234-0000-00",
            user_id="user",
        )
        
        result = await agent.verify_contractor_rbq(contractor.id, "user")
        
        assert result is not None
        assert result.license_number == "1234-0000-00"
    
    def test_list_contractors_rbq_verified_only(self, agent):
        """Test listing only RBQ-verified contractors."""
        # Create contractors with different verification status
        import asyncio
        loop = asyncio.new_event_loop()
        
        loop.run_until_complete(agent.create_contractor(
            name="Verified",
            phone="514-1",
            rbq_license="1234-1111-11",
            user_id="user",
        ))
        
        loop.run_until_complete(agent.create_contractor(
            name="Not Verified",
            phone="514-2",
            rbq_license="9999-2222-22",  # Will be invalid
            user_id="user",
        ))
        
        loop.close()
        
        verified = agent.list_contractors("user", rbq_verified_only=True)
        assert all(c.rbq_verified for c in verified)


# ═══════════════════════════════════════════════════════════════════════════════
# PAYMENT OPERATIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPaymentOperations:
    """Tests for payment operations."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    @pytest.fixture
    def setup_lease(self, agent):
        prop = agent.create_property(name="P", address="A", city="MTL", user_id="user")
        tenant = agent.create_tenant(first_name="T", last_name="T", email="t@t.com", user_id="user")
        lease = agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1500"),
            security_deposit=Decimal("1500"),
            user_id="user",
        )
        return prop, tenant, lease
    
    def test_record_payment_on_time(self, agent, setup_lease):
        """Test recording on-time payment."""
        prop, tenant, lease = setup_lease
        
        payment = agent.record_payment(
            property_id=prop.id,
            tenant_id=tenant.id,
            lease_id=lease.id,
            amount=Decimal("1500"),
            payment_date=date(2024, 8, 1),  # 1st of month = on time
            period_start=date(2024, 8, 1),
            period_end=date(2024, 8, 31),
            user_id="user",
        )
        
        assert payment.id is not None
        assert payment.is_late == False
        assert payment.late_fee == Decimal("0")
    
    def test_record_payment_late(self, agent, setup_lease):
        """Test recording late payment."""
        prop, tenant, lease = setup_lease
        
        payment = agent.record_payment(
            property_id=prop.id,
            tenant_id=tenant.id,
            lease_id=lease.id,
            amount=Decimal("1500"),
            payment_date=date(2024, 8, 5),  # 5th of month = late
            period_start=date(2024, 8, 1),
            period_end=date(2024, 8, 31),
            user_id="user",
        )
        
        assert payment.is_late == True
        assert payment.late_fee == Decimal("50")
    
    def test_list_payments_by_date_range(self, agent, setup_lease):
        """Test listing payments by date range."""
        prop, tenant, lease = setup_lease
        
        agent.record_payment(prop.id, tenant.id, lease.id, Decimal("1500"), 
                           date(2024, 7, 1), date(2024, 7, 1), date(2024, 7, 31), "user")
        agent.record_payment(prop.id, tenant.id, lease.id, Decimal("1500"),
                           date(2024, 8, 1), date(2024, 8, 1), date(2024, 8, 31), "user")
        agent.record_payment(prop.id, tenant.id, lease.id, Decimal("1500"),
                           date(2024, 9, 1), date(2024, 9, 1), date(2024, 9, 30), "user")
        
        filtered = agent.list_payments(
            "user",
            start_date=date(2024, 7, 15),
            end_date=date(2024, 8, 15),
        )
        
        assert len(filtered) == 1  # Only August payment


# ═══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO STATISTICS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPortfolioStatistics:
    """Tests for portfolio statistics."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    def test_empty_portfolio_stats(self, agent):
        """Test stats for empty portfolio."""
        stats = agent.get_portfolio_stats("new_user")
        
        assert stats["properties"]["total"] == 0
        assert stats["tenants"]["total"] == 0
        assert stats["financials"]["total_portfolio_value"] == 0
    
    def test_portfolio_stats_with_data(self, agent):
        """Test comprehensive portfolio statistics."""
        # Create properties
        p1 = agent.create_property(
            name="P1", address="A", city="MTL", user_id="user",
            current_value=Decimal("500000"),
            monthly_rent=Decimal("2000"),
            monthly_expenses=Decimal("500"),
        )
        p1.status = PropertyStatus.RENTED
        
        p2 = agent.create_property(
            name="P2", address="B", city="MTL", user_id="user",
            current_value=Decimal("300000"),
            monthly_rent=Decimal("1500"),
            monthly_expenses=Decimal("300"),
        )
        p2.status = PropertyStatus.RENTED
        
        # Create tenants
        t1 = agent.create_tenant(first_name="T1", last_name="T", email="t1@t.com", user_id="user")
        t2 = agent.create_tenant(first_name="T2", last_name="T", email="t2@t.com", user_id="user")
        
        stats = agent.get_portfolio_stats("user")
        
        assert stats["properties"]["total"] == 2
        assert stats["financials"]["total_portfolio_value"] == 800000
        assert stats["financials"]["monthly_income"] == 3500
        assert stats["financials"]["monthly_expenses"] == 800
        assert stats["financials"]["monthly_cash_flow"] == 2700
        assert stats["tenants"]["total"] == 2


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Integration tests for complete workflows."""
    
    @pytest.fixture
    def agent(self):
        return RealEstateAgent()
    
    @pytest.mark.asyncio
    async def test_full_rental_workflow(self, agent):
        """Test complete rental workflow from property to payment."""
        # 1. Create property
        prop = agent.create_property(
            name="Integration Test Property",
            address="100 Integration St",
            city="Montréal",
            user_id="user",
            property_type=PropertyType.DUPLEX,
            units=2,
            current_value=Decimal("600000"),
            monthly_rent=Decimal("2500"),
            monthly_expenses=Decimal("600"),
        )
        assert prop.status == PropertyStatus.AVAILABLE
        
        # 2. Analyze property
        analysis = await agent.analyze_property(prop.id, "user")
        assert analysis is not None
        assert analysis.cap_rate > 0
        
        # 3. Create tenant
        tenant = agent.create_tenant(
            first_name="Integration",
            last_name="Tenant",
            email="integration@test.com",
            phone="514-123-4567",
            user_id="user",
        )
        assert tenant.is_active == True
        
        # 4. Create lease
        lease = agent.create_lease(
            property_id=prop.id,
            tenant_id=tenant.id,
            start_date=date(2024, 7, 1),
            end_date=date(2025, 6, 30),
            monthly_rent=Decimal("1250"),  # Per unit
            security_deposit=Decimal("1250"),
            unit_number="1",
            user_id="user",
        )
        assert lease.status == LeaseStatus.ACTIVE
        
        # 5. Verify property is now rented
        updated_prop = agent.get_property(prop.id, "user")
        assert updated_prop.status == PropertyStatus.RENTED
        
        # 6. Create contractor with RBQ
        contractor = await agent.create_contractor(
            name="Test Plumber",
            phone="514-999-9999",
            rbq_license="1234-5678-90",
            categories=["plumbing"],
            user_id="user",
        )
        assert contractor.rbq_verified == True
        
        # 7. Create maintenance request
        maint = agent.create_maintenance_request(
            property_id=prop.id,
            tenant_id=tenant.id,
            title="Leaky pipe",
            description="Pipe under sink is leaking",
            category="plumbing",
            priority=MaintenancePriority.HIGH,
            user_id="user",
        )
        assert maint.status == MaintenanceStatus.OPEN
        
        # 8. Complete maintenance
        agent.update_maintenance_status(maint.id, "user", MaintenanceStatus.COMPLETED)
        updated_maint = agent.list_maintenance("user")[0]
        assert updated_maint.status == MaintenanceStatus.COMPLETED
        
        # 9. Record payment
        payment = agent.record_payment(
            property_id=prop.id,
            tenant_id=tenant.id,
            lease_id=lease.id,
            amount=Decimal("1250"),
            payment_date=date(2024, 8, 1),
            period_start=date(2024, 8, 1),
            period_end=date(2024, 8, 31),
            user_id="user",
        )
        assert payment.is_late == False
        
        # 10. Check portfolio stats
        stats = agent.get_portfolio_stats("user")
        assert stats["properties"]["total"] == 1
        assert stats["tenants"]["active"] == 1
        assert stats["leases"]["active"] == 1
        assert stats["maintenance"]["open_requests"] == 0  # Completed


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
