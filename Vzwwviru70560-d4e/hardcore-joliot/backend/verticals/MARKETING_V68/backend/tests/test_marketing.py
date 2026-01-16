"""
CHE·NU™ V68 - Marketing Automation Tests
55+ comprehensive tests covering all features
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

import sys
sys.path.insert(0, '/home/claude/MARKETING_V68/backend/spheres/marketing/agents')

from marketing_agent import (
    MarketingAutomationService,
    Contact, Segment, Campaign, Automation, Form,
    CampaignStatus, CampaignType, ContactStatus,
    AutomationTrigger, AutomationAction, LeadScoreCategory
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def service():
    return MarketingAutomationService()


@pytest.fixture
def workspace_id():
    return "workspace_test"


@pytest.fixture
def user_id():
    return "user_test"


@pytest.fixture
def sample_contact(service, user_id):
    return service.create_contact(
        email="test@example.com",
        created_by=user_id,
        first_name="Test",
        last_name="User",
        company="Test Corp",
        tags=["customer", "newsletter"],
        source="organic"
    )


@pytest.fixture
def sample_segment(service, workspace_id, user_id, sample_contact):
    return service.create_segment(
        name="Active Customers",
        workspace_id=workspace_id,
        created_by=user_id,
        conditions=[{"field": "tag", "operator": "contains", "value": "customer"}]
    )


@pytest.fixture
def sample_template(service, workspace_id, user_id):
    return service.create_template(
        name="Welcome Template",
        workspace_id=workspace_id,
        created_by=user_id,
        subject="Welcome {{first_name}}!",
        html_content="<h1>Hello {{first_name}}</h1><p>Welcome aboard!</p>"
    )


@pytest.fixture
def sample_campaign(service, workspace_id, user_id, sample_segment):
    return service.create_campaign(
        name="Test Campaign",
        workspace_id=workspace_id,
        created_by=user_id,
        subject="Test Subject",
        from_name="Test Sender",
        from_email="sender@example.com",
        html_content="<p>Test content</p>",
        segment_ids=[sample_segment.id]
    )


# ============================================================================
# CONTACT TESTS
# ============================================================================

class TestContacts:
    """Contact management tests"""
    
    def test_create_contact(self, service, user_id):
        """Test contact creation"""
        contact = service.create_contact(
            email="new@example.com",
            created_by=user_id,
            first_name="New"
        )
        
        assert contact.id is not None
        assert contact.email == "new@example.com"
        assert contact.first_name == "New"
        assert contact.status == ContactStatus.ACTIVE
    
    def test_create_duplicate_contact_fails(self, service, user_id, sample_contact):
        """Test that duplicate emails are rejected"""
        with pytest.raises(ValueError, match="already exists"):
            service.create_contact(
                email="test@example.com",  # Same as sample_contact
                created_by=user_id
            )
    
    def test_email_normalization(self, service, user_id):
        """Test email is lowercased"""
        contact = service.create_contact(
            email="TEST@EXAMPLE.COM",
            created_by=user_id
        )
        assert contact.email == "test@example.com"
    
    def test_get_contact(self, service, sample_contact):
        """Test retrieving contact by ID"""
        retrieved = service.get_contact(sample_contact.id)
        assert retrieved is not None
        assert retrieved.id == sample_contact.id
    
    def test_get_contact_by_email(self, service, sample_contact):
        """Test retrieving contact by email"""
        retrieved = service.get_contact_by_email("test@example.com")
        assert retrieved is not None
        assert retrieved.id == sample_contact.id
    
    def test_update_contact(self, service, sample_contact, user_id):
        """Test updating contact"""
        updated = service.update_contact(
            sample_contact.id,
            {"first_name": "Updated", "company": "New Corp"},
            user_id
        )
        
        assert updated.first_name == "Updated"
        assert updated.company == "New Corp"
    
    def test_add_tags(self, service, sample_contact):
        """Test adding tags to contact"""
        initial_tags = len(sample_contact.tags)
        updated = service.add_tags(sample_contact.id, ["vip", "premium"])
        
        assert "vip" in updated.tags
        assert "premium" in updated.tags
        assert len(updated.tags) == initial_tags + 2
    
    def test_add_duplicate_tags(self, service, sample_contact):
        """Test that duplicate tags are not added"""
        initial_tags = len(sample_contact.tags)
        updated = service.add_tags(sample_contact.id, ["customer"])  # Already exists
        
        assert len(updated.tags) == initial_tags
    
    def test_remove_tags(self, service, sample_contact):
        """Test removing tags from contact"""
        updated = service.remove_tags(sample_contact.id, ["newsletter"])
        
        assert "newsletter" not in updated.tags
        assert "customer" in updated.tags
    
    def test_list_contacts_with_filter(self, service, user_id, sample_contact):
        """Test listing contacts with tag filter"""
        # Create another contact
        service.create_contact(email="other@example.com", created_by=user_id, tags=["other"])
        
        results = service.list_contacts(tag="customer")
        assert len(results) == 1
        assert results[0].id == sample_contact.id
    
    def test_list_contacts_with_search(self, service, user_id, sample_contact):
        """Test searching contacts"""
        results = service.list_contacts(search="test")
        assert len(results) == 1
        assert results[0].id == sample_contact.id
    
    def test_unsubscribe_contact(self, service, sample_contact):
        """Test unsubscribing contact"""
        updated = service.unsubscribe_contact(sample_contact.id)
        
        assert updated.status == ContactStatus.UNSUBSCRIBED


# ============================================================================
# SEGMENT TESTS
# ============================================================================

class TestSegments:
    """Segment management tests"""
    
    def test_create_segment(self, service, workspace_id, user_id):
        """Test segment creation"""
        segment = service.create_segment(
            name="New Segment",
            workspace_id=workspace_id,
            created_by=user_id,
            conditions=[{"field": "tag", "operator": "contains", "value": "test"}]
        )
        
        assert segment.id is not None
        assert segment.name == "New Segment"
        assert segment.is_dynamic == True
    
    def test_segment_contact_count(self, service, workspace_id, user_id, sample_contact):
        """Test segment calculates contact count"""
        segment = service.create_segment(
            name="Customer Segment",
            workspace_id=workspace_id,
            created_by=user_id,
            conditions=[{"field": "tag", "operator": "contains", "value": "customer"}]
        )
        
        assert segment.contact_count == 1
    
    def test_segment_with_no_matches(self, service, workspace_id, user_id):
        """Test segment with no matching contacts"""
        segment = service.create_segment(
            name="Empty Segment",
            workspace_id=workspace_id,
            created_by=user_id,
            conditions=[{"field": "tag", "operator": "contains", "value": "nonexistent"}]
        )
        
        assert segment.contact_count == 0
    
    def test_list_segments(self, service, workspace_id, user_id, sample_segment):
        """Test listing segments"""
        segments = service.list_segments(workspace_id)
        
        assert len(segments) == 1
        assert segments[0].id == sample_segment.id


# ============================================================================
# TEMPLATE TESTS
# ============================================================================

class TestTemplates:
    """Email template tests"""
    
    def test_create_template(self, service, workspace_id, user_id):
        """Test template creation"""
        template = service.create_template(
            name="Test Template",
            workspace_id=workspace_id,
            created_by=user_id,
            subject="Hello {{first_name}}",
            html_content="<p>Hi {{first_name}}, from {{company}}!</p>"
        )
        
        assert template.id is not None
        assert "first_name" in template.variables
        assert "company" in template.variables
    
    def test_template_variable_extraction(self, service, workspace_id, user_id):
        """Test template extracts variables correctly"""
        template = service.create_template(
            name="Multi Variable",
            workspace_id=workspace_id,
            created_by=user_id,
            subject="{{greeting}} {{first_name}}",
            html_content="{{body}} {{signature}}"
        )
        
        assert len(template.variables) == 4
    
    def test_list_templates_by_category(self, service, workspace_id, user_id):
        """Test listing templates by category"""
        service.create_template(
            name="Welcome",
            workspace_id=workspace_id,
            created_by=user_id,
            category="onboarding"
        )
        service.create_template(
            name="Newsletter",
            workspace_id=workspace_id,
            created_by=user_id,
            category="marketing"
        )
        
        onboarding = service.list_templates(workspace_id, "onboarding")
        assert len(onboarding) == 1
        assert onboarding[0].name == "Welcome"


# ============================================================================
# CAMPAIGN TESTS
# ============================================================================

class TestCampaigns:
    """Campaign management tests"""
    
    def test_create_campaign(self, service, workspace_id, user_id):
        """Test campaign creation"""
        campaign = service.create_campaign(
            name="New Campaign",
            workspace_id=workspace_id,
            created_by=user_id,
            subject="Test Subject"
        )
        
        assert campaign.id is not None
        assert campaign.status == CampaignStatus.DRAFT
        assert campaign.campaign_type == CampaignType.EMAIL
    
    def test_update_draft_campaign(self, service, sample_campaign):
        """Test updating draft campaign"""
        updated = service.update_campaign(
            sample_campaign.id,
            {"subject": "Updated Subject", "from_name": "Updated Sender"}
        )
        
        assert updated.subject == "Updated Subject"
        assert updated.from_name == "Updated Sender"
    
    def test_schedule_campaign(self, service, sample_campaign, user_id):
        """Test scheduling campaign"""
        scheduled_time = datetime.utcnow() + timedelta(hours=2)
        
        scheduled = service.schedule_campaign(
            sample_campaign.id,
            scheduled_time,
            user_id
        )
        
        assert scheduled.status == CampaignStatus.SCHEDULED
        assert scheduled.stats["recipients"] > 0
    
    def test_schedule_campaign_without_subject_fails(self, service, workspace_id, user_id, sample_segment):
        """Test scheduling campaign without required fields fails"""
        campaign = service.create_campaign(
            name="Empty Campaign",
            workspace_id=workspace_id,
            created_by=user_id,
            segment_ids=[sample_segment.id]
        )
        
        with pytest.raises(ValueError, match="Subject is required"):
            service.schedule_campaign(
                campaign.id,
                datetime.utcnow() + timedelta(hours=1),
                user_id
            )
    
    def test_send_campaign(self, service, sample_campaign, user_id):
        """Test sending campaign"""
        # Schedule first
        service.schedule_campaign(
            sample_campaign.id,
            datetime.utcnow() + timedelta(hours=1),
            user_id
        )
        
        sent = service.send_campaign(sample_campaign.id, user_id)
        
        assert sent.status == CampaignStatus.SENT
        assert sent.sent_at is not None
        assert sent.stats["sent"] > 0
    
    def test_pause_scheduled_campaign(self, service, sample_campaign, user_id):
        """Test pausing scheduled campaign"""
        service.schedule_campaign(
            sample_campaign.id,
            datetime.utcnow() + timedelta(hours=1),
            user_id
        )
        
        paused = service.pause_campaign(sample_campaign.id)
        
        assert paused.status == CampaignStatus.PAUSED
    
    def test_campaign_stats(self, service, sample_campaign, user_id):
        """Test getting campaign statistics"""
        service.schedule_campaign(
            sample_campaign.id,
            datetime.utcnow() + timedelta(hours=1),
            user_id
        )
        service.send_campaign(sample_campaign.id, user_id)
        
        stats = service.get_campaign_stats(sample_campaign.id)
        
        assert "sent" in stats
        assert "delivery_rate" in stats
    
    def test_list_campaigns_by_status(self, service, workspace_id, user_id, sample_segment):
        """Test listing campaigns by status"""
        # Create draft
        service.create_campaign(
            name="Draft",
            workspace_id=workspace_id,
            created_by=user_id,
            segment_ids=[sample_segment.id]
        )
        
        drafts = service.list_campaigns(workspace_id, status=CampaignStatus.DRAFT)
        assert len(drafts) >= 1


# ============================================================================
# A/B TESTING TESTS
# ============================================================================

class TestABTesting:
    """A/B testing tests"""
    
    def test_create_ab_test(self, service, sample_campaign, user_id):
        """Test creating A/B test"""
        ab_test = service.create_ab_test(
            campaign_id=sample_campaign.id,
            created_by=user_id,
            test_type="subject",
            variants=[
                {"name": "A", "value": "Subject A"},
                {"name": "B", "value": "Subject B"}
            ]
        )
        
        assert ab_test.id is not None
        assert len(ab_test.variants) == 2
        assert ab_test.status == "pending"
    
    def test_ab_test_results(self, service, sample_campaign, user_id):
        """Test getting A/B test results"""
        ab_test = service.create_ab_test(
            campaign_id=sample_campaign.id,
            created_by=user_id,
            variants=[
                {"name": "A", "value": "Subject A"},
                {"name": "B", "value": "Subject B"}
            ]
        )
        
        results = service.get_ab_test_results(ab_test.id)
        
        assert "variants" in results
        assert "winner" in results


# ============================================================================
# AUTOMATION TESTS
# ============================================================================

class TestAutomations:
    """Automation workflow tests"""
    
    def test_create_automation(self, service, workspace_id, user_id):
        """Test automation creation"""
        automation = service.create_automation(
            name="Welcome Series",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP,
            description="Onboarding emails"
        )
        
        assert automation.id is not None
        assert automation.trigger == AutomationTrigger.SIGNUP
        assert automation.is_active == False
    
    def test_add_automation_steps(self, service, workspace_id, user_id):
        """Test adding steps to automation"""
        automation = service.create_automation(
            name="Test Automation",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        
        # Add steps
        service.add_automation_step(
            automation.id,
            AutomationAction.SEND_EMAIL,
            {"template_id": "template_1"}
        )
        service.add_automation_step(
            automation.id,
            AutomationAction.WAIT,
            {"days": 3}
        )
        service.add_automation_step(
            automation.id,
            AutomationAction.ADD_TAG,
            {"tag": "onboarded"}
        )
        
        updated = service.get_automation(automation.id)
        assert len(updated.steps) == 3
    
    def test_activate_automation(self, service, workspace_id, user_id):
        """Test activating automation"""
        automation = service.create_automation(
            name="Test",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        
        activated = service.activate_automation(automation.id)
        
        assert activated.is_active == True
    
    def test_deactivate_automation(self, service, workspace_id, user_id):
        """Test deactivating automation"""
        automation = service.create_automation(
            name="Test",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        service.activate_automation(automation.id)
        
        deactivated = service.deactivate_automation(automation.id)
        
        assert deactivated.is_active == False
    
    def test_trigger_automation(self, service, workspace_id, user_id, sample_contact):
        """Test manually triggering automation"""
        automation = service.create_automation(
            name="Manual Trigger",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.CUSTOM
        )
        service.activate_automation(automation.id)
        
        enrollment = service.trigger_automation(automation.id, sample_contact.id)
        
        assert enrollment is not None
        assert enrollment.status == "active"
        assert enrollment.contact_id == sample_contact.id
    
    def test_duplicate_enrollment_prevented(self, service, workspace_id, user_id, sample_contact):
        """Test that duplicate enrollments are prevented"""
        automation = service.create_automation(
            name="Test",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.CUSTOM
        )
        service.activate_automation(automation.id)
        
        first = service.trigger_automation(automation.id, sample_contact.id)
        second = service.trigger_automation(automation.id, sample_contact.id)
        
        assert first is not None
        assert second is None  # Should not create duplicate
    
    def test_list_active_automations(self, service, workspace_id, user_id):
        """Test listing only active automations"""
        auto1 = service.create_automation(
            name="Active",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        service.activate_automation(auto1.id)
        
        service.create_automation(
            name="Inactive",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        
        active = service.list_automations(workspace_id, active_only=True)
        assert len(active) == 1
        assert active[0].name == "Active"


# ============================================================================
# LANDING PAGE TESTS
# ============================================================================

class TestLandingPages:
    """Landing page tests"""
    
    def test_create_landing_page(self, service, workspace_id, user_id):
        """Test landing page creation"""
        page = service.create_landing_page(
            name="Promo Page",
            workspace_id=workspace_id,
            created_by=user_id,
            slug="promo-2024",
            html_content="<h1>Promo!</h1>",
            meta_title="Special Promo"
        )
        
        assert page.id is not None
        assert page.slug == "promo-2024"
        assert page.is_published == False
    
    def test_duplicate_slug_fails(self, service, workspace_id, user_id):
        """Test that duplicate slugs are rejected"""
        service.create_landing_page(
            name="Page 1",
            workspace_id=workspace_id,
            created_by=user_id,
            slug="test-page"
        )
        
        with pytest.raises(ValueError, match="already exists"):
            service.create_landing_page(
                name="Page 2",
                workspace_id=workspace_id,
                created_by=user_id,
                slug="test-page"
            )
    
    def test_publish_landing_page(self, service, workspace_id, user_id):
        """Test publishing landing page"""
        page = service.create_landing_page(
            name="Test",
            workspace_id=workspace_id,
            created_by=user_id,
            slug="test"
        )
        
        published = service.publish_landing_page(page.id)
        
        assert published.is_published == True
        assert published.published_at is not None
    
    def test_record_page_view(self, service, workspace_id, user_id):
        """Test recording page views"""
        page = service.create_landing_page(
            name="Test",
            workspace_id=workspace_id,
            created_by=user_id,
            slug="test"
        )
        
        service.record_page_view(page.id, is_unique=True)
        service.record_page_view(page.id, is_unique=False)
        
        assert page.stats["views"] == 2
        assert page.stats["unique_visitors"] == 1


# ============================================================================
# FORM TESTS
# ============================================================================

class TestForms:
    """Form tests"""
    
    def test_create_form(self, service, workspace_id, user_id):
        """Test form creation"""
        form = service.create_form(
            name="Newsletter Signup",
            workspace_id=workspace_id,
            created_by=user_id,
            fields=[
                {"name": "email", "type": "email", "required": True},
                {"name": "name", "type": "text", "required": False}
            ],
            tags_to_add=["newsletter"]
        )
        
        assert form.id is not None
        assert len(form.fields) == 2
        assert "newsletter" in form.tags_to_add
    
    def test_submit_form_creates_contact(self, service, workspace_id, user_id):
        """Test form submission creates new contact"""
        form = service.create_form(
            name="Signup",
            workspace_id=workspace_id,
            created_by=user_id,
            tags_to_add=["signup"]
        )
        
        submission = service.submit_form(
            form_id=form.id,
            data={"email": "newcontact@example.com", "first_name": "New"}
        )
        
        assert submission.contact_id is not None
        
        contact = service.get_contact(submission.contact_id)
        assert contact.email == "newcontact@example.com"
        assert "signup" in contact.tags
    
    def test_submit_form_updates_existing_contact(self, service, workspace_id, user_id, sample_contact):
        """Test form submission updates existing contact tags"""
        form = service.create_form(
            name="Upgrade",
            workspace_id=workspace_id,
            created_by=user_id,
            tags_to_add=["upgraded"]
        )
        
        submission = service.submit_form(
            form_id=form.id,
            data={"email": sample_contact.email}
        )
        
        updated = service.get_contact(sample_contact.id)
        assert "upgraded" in updated.tags
    
    def test_submit_form_triggers_automation(self, service, workspace_id, user_id):
        """Test form submission triggers linked automation"""
        automation = service.create_automation(
            name="Form Automation",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.FORM_SUBMIT
        )
        service.activate_automation(automation.id)
        
        form = service.create_form(
            name="Signup",
            workspace_id=workspace_id,
            created_by=user_id,
            automation_id=automation.id
        )
        
        service.submit_form(
            form_id=form.id,
            data={"email": "auto@example.com"}
        )
        
        assert automation.stats["enrolled"] == 1
    
    def test_submit_form_required_field_validation(self, service, workspace_id, user_id):
        """Test form validates required fields"""
        form = service.create_form(
            name="Contact",
            workspace_id=workspace_id,
            created_by=user_id,
            fields=[
                {"name": "email", "type": "email", "required": True},
                {"name": "message", "type": "textarea", "required": True}
            ]
        )
        
        with pytest.raises(ValueError, match="Required field"):
            service.submit_form(
                form_id=form.id,
                data={"email": "test@example.com"}  # Missing message
            )


# ============================================================================
# AI FEATURE TESTS
# ============================================================================

class TestAIFeatures:
    """AI feature tests"""
    
    def test_subject_optimization(self, service):
        """Test AI subject line optimization"""
        result = service.optimize_subject("Check out our products")
        
        assert "original" in result
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0
        assert "best_practices" in result
    
    def test_subject_with_personalization_scores_higher(self, service):
        """Test that personalized subjects score higher"""
        result = service.optimize_subject("Check out our products")
        
        # Find personalization suggestion
        personalized = next(
            (s for s in result["suggestions"] if "{{" in s["subject"]),
            None
        )
        
        assert personalized is not None
        assert personalized["predicted_open_rate"] > result["original"]["predicted_open_rate"]
    
    def test_send_time_recommendation(self, service):
        """Test AI send time recommendation"""
        result = service.get_send_time_recommendation()
        
        assert "recommended" in result
        assert "day" in result["recommended"]
        assert "time" in result["recommended"]
        assert "avoid" in result
    
    def test_content_suggestions(self, service):
        """Test AI content suggestions"""
        result = service.get_content_suggestions("new product launch", "professional")
        
        assert "opening_hooks" in result
        assert "suggested_ctas" in result
        assert "structure_tips" in result
    
    def test_lead_scoring(self, service, user_id):
        """Test AI lead scoring"""
        contact = service.create_contact(
            email="scored@example.com",
            created_by=user_id,
            first_name="Scored",
            company="Test Corp",
            source="organic"
        )
        # Simulate some engagement
        contact.email_stats["opened"] = 5
        contact.email_stats["clicked"] = 2
        
        score = service.calculate_lead_score(contact.id)
        
        assert "score" in score
        assert "category" in score
        assert "breakdown" in score
        assert "recommendations" in score
    
    def test_lead_score_categories(self, service, user_id):
        """Test lead score category assignment"""
        # Minimal lead (recent but minimal profile)
        minimal = service.create_contact(email="minimal@example.com", created_by=user_id)
        minimal_score = service.calculate_lead_score(minimal.id)
        # Recent contacts get recency bonus, so might be warm
        assert minimal_score["score"] > 0
        
        # Engaged lead with full profile
        engaged = service.create_contact(
            email="engaged@example.com",
            created_by=user_id,
            first_name="Engaged",
            company="Corp",
            phone="123",
            source="organic"
        )
        engaged.email_stats["opened"] = 10
        engaged.email_stats["clicked"] = 5
        engaged_score = service.calculate_lead_score(engaged.id)
        
        # Engaged should score significantly higher
        assert engaged_score["score"] > minimal_score["score"]
        assert engaged_score["category"] in ["hot", "qualified"]
    
    def test_auto_segment(self, service, user_id, workspace_id):
        """Test AI auto-segmentation"""
        # Create contacts with different behaviors
        for i in range(5):
            contact = service.create_contact(
                email=f"user{i}@example.com",
                created_by=user_id
            )
            if i < 2:
                contact.email_stats["opened"] = 10
                contact.email_stats["clicked"] = 5
        
        segments = service.auto_segment_contacts(workspace_id)
        
        assert "highly_engaged" in segments
        assert "active" in segments
        assert "at_risk" in segments
        assert "dormant" in segments
        assert "new_subscribers" in segments


# ============================================================================
# DASHBOARD TESTS
# ============================================================================

class TestDashboard:
    """Dashboard and analytics tests"""
    
    def test_get_dashboard_stats(self, service, workspace_id, user_id, sample_contact, sample_segment):
        """Test dashboard statistics"""
        # Create some data
        campaign = service.create_campaign(
            name="Dashboard Test",
            workspace_id=workspace_id,
            created_by=user_id,
            subject="Test",
            from_name="Test",
            from_email="test@example.com",
            html_content="<p>Test</p>",
            segment_ids=[sample_segment.id]
        )
        
        automation = service.create_automation(
            name="Test Auto",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.SIGNUP
        )
        service.activate_automation(automation.id)
        
        form = service.create_form(
            name="Test Form",
            workspace_id=workspace_id,
            created_by=user_id
        )
        
        dashboard = service.get_dashboard_stats(workspace_id)
        
        assert "contacts" in dashboard
        assert "campaigns" in dashboard
        assert "automations" in dashboard
        assert "segments" in dashboard
        assert "forms" in dashboard
        assert dashboard["automations"]["active"] == 1
    
    def test_dashboard_contact_growth(self, service, workspace_id, user_id, sample_contact):
        """Test dashboard shows new contacts"""
        dashboard = service.get_dashboard_stats(workspace_id)
        
        assert dashboard["contacts"]["total"] >= 1
        assert dashboard["contacts"]["new_this_month"] >= 1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_full_campaign_workflow(self, service, workspace_id, user_id):
        """Test complete campaign workflow: create → schedule → send"""
        # Create contact
        contact = service.create_contact(
            email="campaign_test@example.com",
            created_by=user_id,
            tags=["test"]
        )
        
        # Create segment
        segment = service.create_segment(
            name="Test Segment",
            workspace_id=workspace_id,
            created_by=user_id,
            conditions=[{"field": "tag", "operator": "contains", "value": "test"}]
        )
        
        # Create campaign
        campaign = service.create_campaign(
            name="Full Workflow Test",
            workspace_id=workspace_id,
            created_by=user_id,
            subject="Test Email",
            from_name="Test",
            from_email="test@example.com",
            html_content="<p>Content</p>",
            segment_ids=[segment.id]
        )
        
        assert campaign.status == CampaignStatus.DRAFT
        
        # Schedule
        scheduled = service.schedule_campaign(
            campaign.id,
            datetime.utcnow() + timedelta(hours=1),
            user_id
        )
        assert scheduled.status == CampaignStatus.SCHEDULED
        assert scheduled.stats["recipients"] == 1
        
        # Send
        sent = service.send_campaign(campaign.id, user_id)
        assert sent.status == CampaignStatus.SENT
        assert sent.stats["sent"] == 1
        
        # Verify contact was updated
        updated_contact = service.get_contact(contact.id)
        assert updated_contact.email_stats["sent"] == 1
    
    def test_full_automation_workflow(self, service, workspace_id, user_id):
        """Test complete automation workflow: form → automation → contact"""
        # Create automation
        automation = service.create_automation(
            name="Welcome Flow",
            workspace_id=workspace_id,
            created_by=user_id,
            trigger=AutomationTrigger.FORM_SUBMIT
        )
        
        service.add_automation_step(
            automation.id,
            AutomationAction.ADD_TAG,
            {"tag": "welcomed"}
        )
        service.add_automation_step(
            automation.id,
            AutomationAction.SEND_EMAIL,
            {"template_id": "welcome"}
        )
        
        service.activate_automation(automation.id)
        
        # Create form linked to automation
        form = service.create_form(
            name="Welcome Form",
            workspace_id=workspace_id,
            created_by=user_id,
            tags_to_add=["form_signup"],
            automation_id=automation.id
        )
        
        # Submit form
        submission = service.submit_form(
            form_id=form.id,
            data={"email": "workflow@example.com", "first_name": "Workflow"}
        )
        
        # Verify
        contact = service.get_contact(submission.contact_id)
        assert "form_signup" in contact.tags
        
        automation_updated = service.get_automation(automation.id)
        assert automation_updated.stats["enrolled"] == 1
    
    def test_landing_page_conversion_tracking(self, service, workspace_id, user_id):
        """Test landing page conversion tracking"""
        # Create landing page
        page = service.create_landing_page(
            name="Conversion Test",
            workspace_id=workspace_id,
            created_by=user_id,
            slug="convert"
        )
        service.publish_landing_page(page.id)
        
        # Create form
        form = service.create_form(
            name="Page Form",
            workspace_id=workspace_id,
            created_by=user_id
        )
        
        # Record views
        service.record_page_view(page.id, is_unique=True)
        service.record_page_view(page.id, is_unique=True)
        service.record_page_view(page.id, is_unique=False)
        
        # Submit form (simulating conversion)
        service.submit_form(
            form_id=form.id,
            data={"email": "convert@example.com"},
            page_url="/convert"
        )
        
        # Verify stats
        assert page.stats["views"] == 3
        assert page.stats["unique_visitors"] == 2
        assert page.stats["conversions"] == 1


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
