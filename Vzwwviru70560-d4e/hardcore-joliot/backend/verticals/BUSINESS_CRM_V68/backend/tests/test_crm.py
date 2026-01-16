"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ BUSINESS CRM — TESTS                              ║
║                                                                              ║
║  Comprehensive test suite for CRM Agent and API.                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pytest
import asyncio
from decimal import Decimal
from datetime import datetime, timezone, timedelta

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spheres.business.agents.crm_agent import (
    CRMAgent,
    CRMAIEngine,
    LeadStatus,
    LeadSource,
    DealStage,
    ActivityType,
    ContactType,
    Company,
    Contact,
    Deal,
    Activity,
)


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def agent():
    """Fresh CRM agent for each test."""
    return CRMAgent()


@pytest.fixture
def ai_engine():
    """AI engine for testing."""
    return CRMAIEngine()


@pytest.fixture
def sample_company(agent):
    """Sample company for testing."""
    return agent.create_company(
        name="TechCorp Inc",
        user_id="test_user",
        industry="Technology",
        size="51-200",
        annual_revenue=Decimal("5000000"),
        website="https://techcorp.com",
    )


@pytest.fixture
def sample_contact(agent, sample_company):
    """Sample contact for testing."""
    async def create():
        return await agent.create_contact(
            first_name="John",
            last_name="Smith",
            email="john@techcorp.com",
            user_id="test_user",
            title="VP of Engineering",
            company_id=sample_company.id,
            company_name=sample_company.name,
            lead_source=LeadSource.LINKEDIN,
            tags=["decision-maker", "tech"],
            auto_score=False,
        )
    return asyncio.get_event_loop().run_until_complete(create())


# ═══════════════════════════════════════════════════════════════════════════════
# AI ENGINE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCRMAIEngine:
    """Tests for CRM AI Engine."""
    
    def test_local_scoring_decision_maker(self, ai_engine):
        """Test local scoring for decision maker."""
        contact = Contact(
            id="test_id",
            first_name="Jane",
            last_name="Doe",
            email="jane@corp.com",
            phone=None,
            title="CEO",
            company_id=None,
            company_name="Corp Inc",
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.QUALIFIED,
            lead_source=LeadSource.REFERRAL,
            lead_score=0,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=None,
            tags=[],
            owner_id="user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        result = ai_engine._local_scoring(contact, None)
        
        assert result.total_score >= 50  # CEO should score high
        assert result.breakdown["fit"] == 25  # Max fit for CEO
        assert result.grade in ["A", "B"]
        assert len(result.insights) >= 1
        assert len(result.next_actions) >= 1
    
    def test_local_scoring_new_lead(self, ai_engine):
        """Test local scoring for new lead."""
        contact = Contact(
            id="test_id",
            first_name="Bob",
            last_name="Test",
            email="bob@test.com",
            phone=None,
            title=None,
            company_id=None,
            company_name=None,
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.NEW,
            lead_source=LeadSource.WEBSITE,
            lead_score=0,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=None,
            tags=[],
            owner_id="user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        result = ai_engine._local_scoring(contact, None)
        
        assert result.total_score < 50  # New lead with no info should score lower
        assert result.breakdown["fit"] == 5  # No title = low fit
        assert "Make initial contact" in result.next_actions
    
    def test_local_scoring_with_company(self, ai_engine):
        """Test scoring with enterprise company."""
        contact = Contact(
            id="test_id",
            first_name="Sarah",
            last_name="Manager",
            email="sarah@big.com",
            phone=None,
            title="Director of IT",
            company_id="comp_id",
            company_name="Big Corp",
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.CONTACTED,
            lead_source=LeadSource.EVENT,
            lead_score=0,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=None,
            tags=[],
            owner_id="user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        company = Company(
            id="comp_id",
            name="Big Corp",
            domain="big.com",
            industry="Enterprise",
            size="500+",
            annual_revenue=Decimal("50000000"),
            website="https://big.com",
            linkedin_url=None,
            address=None,
            city=None,
            country=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        result = ai_engine._local_scoring(contact, company)
        
        assert result.total_score >= 60  # Director at enterprise should score well
        assert result.breakdown["budget"] == 25  # High revenue = max budget
        assert "Enterprise-size company" in result.insights
    
    def test_local_email_draft_follow_up(self, ai_engine):
        """Test local email draft generation."""
        contact = Contact(
            id="test_id",
            first_name="Mike",
            last_name="Client",
            email="mike@client.com",
            phone=None,
            title="CTO",
            company_id=None,
            company_name="Client Co",
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.CONTACTED,
            lead_source=LeadSource.REFERRAL,
            lead_score=50,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=None,
            tags=[],
            owner_id="user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        draft = ai_engine._local_email_draft(contact, "follow_up", None)
        
        assert "Mike" in draft.body
        assert "Client Co" in draft.body
        assert draft.subject
        assert draft.cta
        assert draft.tone == "professional"
    
    def test_local_email_draft_introduction(self, ai_engine):
        """Test introduction email."""
        contact = Contact(
            id="test_id",
            first_name="Lisa",
            last_name="New",
            email="lisa@new.com",
            phone=None,
            title="VP Sales",
            company_id=None,
            company_name="New Corp",
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.NEW,
            lead_source=LeadSource.COLD_OUTREACH,
            lead_score=30,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=None,
            tags=[],
            owner_id="user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id="user",
        )
        
        draft = ai_engine._local_email_draft(contact, "introduction", None)
        
        assert "Lisa" in draft.body
        assert "New Corp" in draft.body


# ═══════════════════════════════════════════════════════════════════════════════
# COMPANY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCompanyOperations:
    """Tests for company operations."""
    
    def test_create_company(self, agent):
        """Test company creation."""
        company = agent.create_company(
            name="Test Corp",
            user_id="test_user",
            industry="Software",
            size="11-50",
        )
        
        assert company.id
        assert company.name == "Test Corp"
        assert company.industry == "Software"
        assert company.size == "11-50"
        assert company.contact_count == 0
        assert company.deal_count == 0
    
    def test_get_company(self, agent, sample_company):
        """Test getting a company."""
        retrieved = agent.get_company(sample_company.id, "test_user")
        
        assert retrieved is not None
        assert retrieved.id == sample_company.id
        assert retrieved.name == sample_company.name
    
    def test_get_company_not_found(self, agent):
        """Test getting non-existent company."""
        retrieved = agent.get_company("fake_id", "test_user")
        assert retrieved is None
    
    def test_list_companies(self, agent):
        """Test listing companies."""
        agent.create_company(name="Alpha Corp", user_id="test_user", industry="Tech")
        agent.create_company(name="Beta Inc", user_id="test_user", industry="Finance")
        agent.create_company(name="Gamma Ltd", user_id="test_user", industry="Tech")
        
        all_companies = agent.list_companies("test_user")
        assert len(all_companies) == 3
        
        tech_companies = agent.list_companies("test_user", industry="Tech")
        assert len(tech_companies) == 2
        
        search_results = agent.list_companies("test_user", search="Alpha")
        assert len(search_results) == 1
        assert search_results[0].name == "Alpha Corp"


# ═══════════════════════════════════════════════════════════════════════════════
# CONTACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestContactOperations:
    """Tests for contact operations."""
    
    @pytest.mark.asyncio
    async def test_create_contact(self, agent):
        """Test contact creation."""
        contact = await agent.create_contact(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            user_id="test_user",
            auto_score=False,
        )
        
        assert contact.id
        assert contact.first_name == "Test"
        assert contact.last_name == "User"
        assert contact.email == "test@example.com"
        assert contact.lead_status == LeadStatus.NEW
        assert contact.contact_type == ContactType.LEAD
    
    @pytest.mark.asyncio
    async def test_create_contact_with_scoring(self, agent):
        """Test contact creation with auto-scoring."""
        contact = await agent.create_contact(
            first_name="VP",
            last_name="Test",
            email="vp@corp.com",
            user_id="test_user",
            title="VP of Sales",
            auto_score=True,
        )
        
        assert contact.lead_score > 0
        assert len(contact.lead_score_breakdown) > 0
    
    def test_get_contact(self, agent, sample_contact):
        """Test getting a contact."""
        retrieved = agent.get_contact(sample_contact.id, "test_user")
        
        assert retrieved is not None
        assert retrieved.id == sample_contact.id
        assert retrieved.email == sample_contact.email
    
    @pytest.mark.asyncio
    async def test_update_contact(self, agent, sample_contact):
        """Test updating a contact."""
        updated = await agent.update_contact(
            sample_contact.id,
            "test_user",
            title="CTO",
            lead_status=LeadStatus.QUALIFIED,
        )
        
        assert updated.title == "CTO"
        assert updated.lead_status == LeadStatus.QUALIFIED
    
    def test_delete_contact(self, agent, sample_contact):
        """Test deleting a contact."""
        result = agent.delete_contact(sample_contact.id, "test_user")
        assert result is True
        
        retrieved = agent.get_contact(sample_contact.id, "test_user")
        assert retrieved is None
    
    @pytest.mark.asyncio
    async def test_list_contacts_with_filters(self, agent):
        """Test listing contacts with various filters."""
        await agent.create_contact(
            first_name="Hot", last_name="Lead",
            email="hot@test.com", user_id="test_user",
            title="CEO", lead_source=LeadSource.REFERRAL,
            auto_score=True
        )
        await agent.create_contact(
            first_name="Cold", last_name="Lead",
            email="cold@test.com", user_id="test_user",
            lead_source=LeadSource.WEBSITE,
            auto_score=True
        )
        
        all_contacts = agent.list_contacts("test_user")
        assert len(all_contacts) == 2
        
        referral_contacts = agent.list_contacts("test_user", lead_source=LeadSource.REFERRAL)
        assert len(referral_contacts) == 1
        assert referral_contacts[0].first_name == "Hot"
    
    @pytest.mark.asyncio
    async def test_score_contact(self, agent, sample_contact):
        """Test AI scoring of contact."""
        result = await agent.score_contact(sample_contact.id, "test_user")
        
        assert result is not None
        assert result.total_score >= 0
        assert result.grade in ["A", "B", "C", "D", "F"]
        
        # Check contact was updated
        contact = agent.get_contact(sample_contact.id, "test_user")
        assert contact.lead_score == result.total_score


# ═══════════════════════════════════════════════════════════════════════════════
# DEAL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDealOperations:
    """Tests for deal operations."""
    
    def test_create_deal(self, agent, sample_contact):
        """Test deal creation."""
        deal = agent.create_deal(
            name="Enterprise License",
            contact_id=sample_contact.id,
            amount=Decimal("50000"),
            user_id="test_user",
        )
        
        assert deal.id
        assert deal.name == "Enterprise License"
        assert deal.amount == Decimal("50000")
        assert deal.stage == DealStage.DISCOVERY
        assert deal.probability == 10
    
    def test_create_deal_with_stage(self, agent, sample_contact):
        """Test deal creation with specific stage."""
        deal = agent.create_deal(
            name="Hot Deal",
            contact_id=sample_contact.id,
            amount=Decimal("100000"),
            user_id="test_user",
            stage=DealStage.NEGOTIATION,
        )
        
        assert deal.stage == DealStage.NEGOTIATION
        assert deal.probability == 75
    
    def test_update_deal_stage(self, agent, sample_contact):
        """Test updating deal stage."""
        deal = agent.create_deal(
            name="Test Deal",
            contact_id=sample_contact.id,
            amount=Decimal("25000"),
            user_id="test_user",
        )
        
        updated = agent.update_deal_stage(deal.id, "test_user", DealStage.PROPOSAL)
        
        assert updated.stage == DealStage.PROPOSAL
        assert updated.probability == 50
    
    def test_close_deal_won(self, agent, sample_contact):
        """Test closing a deal as won."""
        deal = agent.create_deal(
            name="Winning Deal",
            contact_id=sample_contact.id,
            amount=Decimal("75000"),
            user_id="test_user",
        )
        
        closed = agent.update_deal_stage(deal.id, "test_user", DealStage.CLOSED_WON)
        
        assert closed.stage == DealStage.CLOSED_WON
        assert closed.probability == 100
        assert closed.actual_close_date is not None
    
    def test_close_deal_lost(self, agent, sample_contact):
        """Test closing a deal as lost."""
        deal = agent.create_deal(
            name="Lost Deal",
            contact_id=sample_contact.id,
            amount=Decimal("30000"),
            user_id="test_user",
        )
        
        closed = agent.update_deal_stage(
            deal.id, "test_user",
            DealStage.CLOSED_LOST,
            lost_reason="Budget constraints"
        )
        
        assert closed.stage == DealStage.CLOSED_LOST
        assert closed.probability == 0
        assert closed.lost_reason == "Budget constraints"
    
    def test_list_deals(self, agent, sample_contact):
        """Test listing deals."""
        agent.create_deal(
            name="Deal 1",
            contact_id=sample_contact.id,
            amount=Decimal("10000"),
            user_id="test_user",
            stage=DealStage.DISCOVERY,
        )
        agent.create_deal(
            name="Deal 2",
            contact_id=sample_contact.id,
            amount=Decimal("50000"),
            user_id="test_user",
            stage=DealStage.PROPOSAL,
        )
        
        all_deals = agent.list_deals("test_user")
        assert len(all_deals) == 2
        
        proposal_deals = agent.list_deals("test_user", stage=DealStage.PROPOSAL)
        assert len(proposal_deals) == 1
        assert proposal_deals[0].name == "Deal 2"
    
    def test_pipeline_summary(self, agent, sample_contact):
        """Test pipeline summary calculation."""
        agent.create_deal(
            name="Discovery Deal",
            contact_id=sample_contact.id,
            amount=Decimal("10000"),
            user_id="test_user",
            stage=DealStage.DISCOVERY,
        )
        agent.create_deal(
            name="Proposal Deal",
            contact_id=sample_contact.id,
            amount=Decimal("50000"),
            user_id="test_user",
            stage=DealStage.PROPOSAL,
        )
        
        summary = agent.get_pipeline_summary("test_user")
        
        assert summary["total_pipeline_value"] == 60000
        assert summary["open_deals"] == 2
        assert "discovery" in summary["by_stage"]
        assert "proposal" in summary["by_stage"]


# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestActivityOperations:
    """Tests for activity operations."""
    
    def test_log_activity(self, agent, sample_contact):
        """Test logging an activity."""
        activity = agent.log_activity(
            activity_type=ActivityType.CALL,
            subject="Discovery call",
            user_id="test_user",
            contact_id=sample_contact.id,
            duration_minutes=30,
            outcome="Interested",
        )
        
        assert activity.id
        assert activity.activity_type == ActivityType.CALL
        assert activity.subject == "Discovery call"
        assert activity.duration_minutes == 30
        assert activity.outcome == "Interested"
    
    def test_log_activity_updates_contact(self, agent, sample_contact):
        """Test that logging activity updates contact."""
        agent.log_activity(
            activity_type=ActivityType.EMAIL,
            subject="Follow-up email",
            user_id="test_user",
            contact_id=sample_contact.id,
        )
        
        contact = agent.get_contact(sample_contact.id, "test_user")
        assert contact.last_activity is not None
        assert contact.last_contacted is not None
    
    def test_list_activities(self, agent, sample_contact):
        """Test listing activities."""
        agent.log_activity(
            activity_type=ActivityType.CALL,
            subject="Call 1",
            user_id="test_user",
            contact_id=sample_contact.id,
        )
        agent.log_activity(
            activity_type=ActivityType.EMAIL,
            subject="Email 1",
            user_id="test_user",
            contact_id=sample_contact.id,
        )
        agent.log_activity(
            activity_type=ActivityType.NOTE,
            subject="Note 1",
            user_id="test_user",
        )
        
        all_activities = agent.list_activities("test_user")
        assert len(all_activities) == 3
        
        contact_activities = agent.list_activities("test_user", contact_id=sample_contact.id)
        assert len(contact_activities) == 2
        
        call_activities = agent.list_activities("test_user", activity_type=ActivityType.CALL)
        assert len(call_activities) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL GENERATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmailGeneration:
    """Tests for email generation."""
    
    @pytest.mark.asyncio
    async def test_generate_email(self, agent, sample_contact):
        """Test email draft generation."""
        draft = await agent.generate_email(
            sample_contact.id,
            "test_user",
            purpose="follow_up",
        )
        
        assert draft is not None
        assert draft.subject
        assert draft.body
        assert sample_contact.first_name in draft.body
    
    @pytest.mark.asyncio
    async def test_generate_email_not_found(self, agent):
        """Test email generation for non-existent contact."""
        draft = await agent.generate_email(
            "fake_id",
            "test_user",
            purpose="follow_up",
        )
        
        assert draft is None


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestStatistics:
    """Tests for CRM statistics."""
    
    @pytest.mark.asyncio
    async def test_get_stats(self, agent):
        """Test getting CRM statistics."""
        # Create some data
        company = agent.create_company(name="Stats Corp", user_id="test_user")
        
        contact1 = await agent.create_contact(
            first_name="Hot", last_name="Lead",
            email="hot@stats.com", user_id="test_user",
            title="CEO", auto_score=True
        )
        contact2 = await agent.create_contact(
            first_name="Cold", last_name="Lead",
            email="cold@stats.com", user_id="test_user",
            auto_score=True
        )
        
        agent.create_deal(
            name="Deal 1",
            contact_id=contact1.id,
            amount=Decimal("10000"),
            user_id="test_user",
        )
        
        agent.log_activity(
            activity_type=ActivityType.CALL,
            subject="Test call",
            user_id="test_user",
        )
        
        stats = agent.get_stats("test_user")
        
        assert stats["contacts"]["total"] == 2
        assert stats["companies"]["total"] == 1
        assert stats["deals"]["open_deals"] == 1
        assert stats["activities"]["total"] == 1


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Integration tests for complete CRM workflows."""
    
    @pytest.mark.asyncio
    async def test_full_sales_workflow(self, agent):
        """Test complete sales workflow."""
        # 1. Create company
        company = agent.create_company(
            name="Big Enterprise",
            user_id="sales_rep",
            industry="Enterprise Software",
            size="500+",
            annual_revenue=Decimal("100000000"),
        )
        
        # 2. Create contact
        contact = await agent.create_contact(
            first_name="Decision",
            last_name="Maker",
            email="dm@bigent.com",
            user_id="sales_rep",
            title="CTO",
            company_id=company.id,
            company_name=company.name,
            lead_source=LeadSource.REFERRAL,
            auto_score=True,
        )
        
        assert contact.lead_score > 50  # Should be high score
        
        # 3. Log discovery call
        agent.log_activity(
            activity_type=ActivityType.CALL,
            subject="Initial discovery",
            user_id="sales_rep",
            contact_id=contact.id,
            duration_minutes=45,
            outcome="Very interested, scheduling demo",
        )
        
        # 4. Update status
        await agent.update_contact(
            contact.id,
            "sales_rep",
            lead_status=LeadStatus.QUALIFIED,
        )
        
        # 5. Create deal
        deal = agent.create_deal(
            name="Big Enterprise - Annual License",
            contact_id=contact.id,
            company_id=company.id,
            amount=Decimal("250000"),
            user_id="sales_rep",
            stage=DealStage.DISCOVERY,
        )
        
        # 6. Progress deal through stages
        agent.update_deal_stage(deal.id, "sales_rep", DealStage.QUALIFICATION)
        agent.update_deal_stage(deal.id, "sales_rep", DealStage.PROPOSAL)
        agent.update_deal_stage(deal.id, "sales_rep", DealStage.NEGOTIATION)
        
        # 7. Close won!
        closed_deal = agent.update_deal_stage(deal.id, "sales_rep", DealStage.CLOSED_WON)
        
        assert closed_deal.stage == DealStage.CLOSED_WON
        assert closed_deal.probability == 100
        
        # 8. Check stats
        stats = agent.get_stats("sales_rep")
        assert stats["deals"]["won_deals"] == 1
        assert stats["deals"]["won_value"] == 250000


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
