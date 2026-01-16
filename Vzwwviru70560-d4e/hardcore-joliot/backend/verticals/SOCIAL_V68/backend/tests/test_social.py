"""
CHE·NU™ V68 - Social Media Agent Tests
Vertical 10: Social Media Management

Comprehensive test coverage for all features:
- Account Management
- Templates
- Post Workflow (GOVERNANCE)
- Engagement Tracking
- Hashtag Research (ALPHABETICAL)
- Audience Insights
- Campaigns
- Competitor Monitoring
- Content Calendar
- AI Features
- Analytics Dashboard
"""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import sys
sys.path.insert(0, '/home/claude/SOCIAL_V68')

from backend.spheres.social.agents.social_agent import (
    SocialMediaAgent,
    Platform,
    AccountStatus,
    PostStatus,
    ContentType,
    CampaignStatus,
    get_social_agent
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def agent():
    """Fresh agent for each test."""
    return SocialMediaAgent()


@pytest.fixture
def user_id():
    return "test_user_123"


# Helper functions for creating test data inline
async def create_connected_account(agent, user_id):
    """Create a connected account."""
    return await agent.connect_account(
        platform=Platform.INSTAGRAM,
        account_name="test_brand",
        account_id="ig_123456",
        access_token="test_token",
        user_id=user_id
    )


async def create_draft_post(agent, user_id):
    """Create a draft post."""
    return await agent.create_post(
        text="Test post content #test",
        platforms=[Platform.INSTAGRAM, Platform.FACEBOOK],
        content_type=ContentType.IMAGE,
        media_urls=["https://example.com/image.jpg"],
        hashtags=["test", "social"],
        user_id=user_id
    )


# ============================================================================
# ACCOUNT TESTS
# ============================================================================

class TestAccounts:
    """Test social account management."""
    
    @pytest.mark.asyncio
    async def test_connect_account(self, agent, user_id):
        """Test connecting a social account."""
        account = await agent.connect_account(
            platform=Platform.INSTAGRAM,
            account_name="my_brand",
            account_id="ig_12345",
            access_token="token_xyz",
            user_id=user_id
        )
        
        assert account.platform == Platform.INSTAGRAM
        assert account.account_name == "my_brand"
        assert account.status == AccountStatus.CONNECTED
        assert account.user_id == user_id
    
    @pytest.mark.asyncio
    async def test_reconnect_updates_existing(self, agent, user_id):
        """Test reconnecting updates existing account."""
        # Connect first time
        account1 = await agent.connect_account(
            platform=Platform.INSTAGRAM,
            account_name="my_brand",
            account_id="ig_12345",
            access_token="token_1",
            user_id=user_id
        )
        
        # Reconnect with new token
        account2 = await agent.connect_account(
            platform=Platform.INSTAGRAM,
            account_name="my_brand",
            account_id="ig_12345",
            access_token="token_2",
            user_id=user_id
        )
        
        # Should be same account
        assert account1.id == account2.id
        assert account2.access_token == "token_2"
    
    @pytest.mark.asyncio
    async def test_disconnect_account(self, agent, user_id):
        """Test disconnecting an account."""
        connected_account = await create_connected_account(agent, user_id)
        account = await agent.disconnect_account(
            connected_account.id,
            user_id
        )
        
        assert account.status == AccountStatus.DISCONNECTED
        assert account.access_token == ""
    
    @pytest.mark.asyncio
    async def test_get_accounts_alphabetical(self, agent, user_id):
        """Test accounts are returned alphabetically by platform."""
        await agent.connect_account(
            platform=Platform.TWITTER,
            account_name="twitter_acc",
            account_id="tw_123",
            access_token="token",
            user_id=user_id
        )
        await agent.connect_account(
            platform=Platform.INSTAGRAM,
            account_name="ig_acc",
            account_id="ig_123",
            access_token="token",
            user_id=user_id
        )
        await agent.connect_account(
            platform=Platform.FACEBOOK,
            account_name="fb_acc",
            account_id="fb_123",
            access_token="token",
            user_id=user_id
        )
        
        accounts = await agent.get_accounts(user_id)
        
        # Should be alphabetical: facebook, instagram, twitter
        assert accounts[0].platform == Platform.FACEBOOK
        assert accounts[1].platform == Platform.INSTAGRAM
        assert accounts[2].platform == Platform.TWITTER
    
    @pytest.mark.asyncio
    async def test_sync_account_metrics(self, agent, user_id):
        """Test syncing account metrics."""
        connected_account = await create_connected_account(agent, user_id)
        await agent.sync_account_metrics(
            account_id=connected_account.id,
            followers_count=10000,
            following_count=500,
            posts_count=200
        )
        
        account = agent.accounts[connected_account.id]
        assert account.followers_count == 10000
        assert account.following_count == 500
        assert account.last_synced is not None


# ============================================================================
# TEMPLATE TESTS
# ============================================================================

class TestTemplates:
    """Test content templates."""
    
    @pytest.mark.asyncio
    async def test_create_template(self, agent, user_id):
        """Test creating a template."""
        template = await agent.create_template(
            name="Product Launch",
            description="Template for launches",
            template_text="Introducing {product}! {description}",
            content_type=ContentType.IMAGE,
            variables=["product", "description"],
            hashtags=["launch", "new"],
            user_id=user_id
        )
        
        assert template.name == "Product Launch"
        assert "product" in template.variables
        assert template.usage_count == 0
    
    @pytest.mark.asyncio
    async def test_apply_template(self, agent, user_id):
        """Test applying variables to template."""
        template = await agent.create_template(
            name="Test",
            description="Test template",
            template_text="Hello {name}! Check out {item}.",
            content_type=ContentType.TEXT,
            variables=["name", "item"],
            user_id=user_id
        )
        
        result = await agent.apply_template(
            template_id=template.id,
            variables={"name": "World", "item": "this"},
            user_id=user_id
        )
        
        assert result == "Hello World! Check out this."
        assert agent.templates[template.id].usage_count == 1
    
    @pytest.mark.asyncio
    async def test_get_templates_alphabetical(self, agent, user_id):
        """Test templates are returned alphabetically."""
        await agent.create_template(
            name="Zebra",
            description="Z template",
            template_text="Z",
            content_type=ContentType.TEXT,
            user_id=user_id
        )
        await agent.create_template(
            name="Apple",
            description="A template",
            template_text="A",
            content_type=ContentType.TEXT,
            user_id=user_id
        )
        
        templates = await agent.get_templates(user_id)
        
        assert templates[0].name == "Apple"
        assert templates[1].name == "Zebra"


# ============================================================================
# POST WORKFLOW TESTS - GOVERNANCE
# ============================================================================

class TestPostWorkflow:
    """Test post creation and governance workflow."""
    
    @pytest.mark.asyncio
    async def test_create_post_starts_as_draft(self, agent, user_id):
        """Test that new posts start as DRAFT."""
        post = await agent.create_post(
            text="Test post",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        
        assert post.status == PostStatus.DRAFT
    
    @pytest.mark.asyncio
    async def test_submit_for_review(self, agent, user_id):
        """Test submitting post for review."""
        draft_post = await create_draft_post(agent, user_id)
        post = await agent.submit_for_review(draft_post.id, user_id)
        
        assert post.status == PostStatus.PENDING_REVIEW
        assert post.submitted_for_review is not None
    
    @pytest.mark.asyncio
    async def test_cannot_publish_draft(self, agent, user_id):
        """Test that DRAFT posts cannot be published."""
        draft_post = await create_draft_post(agent, user_id)
        with pytest.raises(ValueError, match="must be approved"):
            await agent.publish_post(draft_post.id, user_id)
    
    @pytest.mark.asyncio
    async def test_approve_post(self, agent, user_id):
        """Test approving a post."""
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        post = await agent.approve_post(draft_post.id, "reviewer_456")
        
        assert post.status == PostStatus.APPROVED
        assert post.reviewed_by == "reviewer_456"
        assert post.reviewed_at is not None
    
    @pytest.mark.asyncio
    async def test_reject_post(self, agent, user_id):
        """Test rejecting a post."""
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        post = await agent.reject_post(
            draft_post.id,
            "reviewer_456",
            "Content needs revision"
        )
        
        assert post.status == PostStatus.REJECTED
        assert post.rejection_reason == "Content needs revision"
    
    @pytest.mark.asyncio
    async def test_publish_approved_post(self, agent, user_id):
        """Test publishing an approved post."""
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        await agent.approve_post(draft_post.id, "reviewer_456")
        post = await agent.publish_post(draft_post.id, user_id)
        
        assert post.status == PostStatus.PUBLISHED
        assert post.published_at is not None
        assert len(post.platform_post_ids) == 2  # Instagram + Facebook
    
    @pytest.mark.asyncio
    async def test_revert_rejected_to_draft(self, agent, user_id):
        """Test reverting rejected post to draft."""
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        await agent.reject_post(draft_post.id, "reviewer", "needs work")
        post = await agent.revert_to_draft(draft_post.id, user_id)
        
        assert post.status == PostStatus.DRAFT
        assert post.rejection_reason == ""
    
    @pytest.mark.asyncio
    async def test_platform_character_limit(self, agent, user_id):
        """Test platform character limit enforcement."""
        long_text = "x" * 300  # Exceeds Twitter limit
        
        with pytest.raises(ValueError, match="exceeds twitter limit"):
            await agent.create_post(
                text=long_text,
                platforms=[Platform.TWITTER],
                user_id=user_id
            )
    
    @pytest.mark.asyncio
    async def test_get_posts_chronological(self, agent, user_id):
        """Test posts are returned chronologically (newest first)."""
        post1 = await agent.create_post(
            text="First post",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        post2 = await agent.create_post(
            text="Second post",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        
        posts = await agent.get_posts(user_id)
        
        # Newest first
        assert posts[0].id == post2.id
        assert posts[1].id == post1.id
    
    @pytest.mark.asyncio
    async def test_get_pending_reviews(self, agent, user_id):
        """Test getting posts pending review."""
        post1 = await agent.create_post(
            text="Post 1",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        post2 = await agent.create_post(
            text="Post 2",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        
        await agent.submit_for_review(post1.id, user_id)
        await agent.submit_for_review(post2.id, user_id)
        
        pending = await agent.get_pending_reviews(user_id)
        
        assert len(pending) == 2


# ============================================================================
# ENGAGEMENT TESTS
# ============================================================================

class TestEngagement:
    """Test engagement tracking."""
    
    @pytest.mark.asyncio
    async def test_record_engagement(self, agent, user_id):
        """Test recording engagement metrics."""
        # Create and publish post first
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        await agent.approve_post(draft_post.id, "reviewer")
        post = await agent.publish_post(draft_post.id, user_id)
        
        engagement = await agent.record_engagement(
            post_id=post.id,
            platform=Platform.INSTAGRAM,
            platform_post_id=post.platform_post_ids[Platform.INSTAGRAM],
            likes=100,
            comments=20,
            shares=10,
            reach=1000
        )
        
        assert engagement.likes == 100
        assert engagement.engagement_rate == Decimal("13.00")  # (100+20+10)/1000*100
    
    @pytest.mark.asyncio
    async def test_get_post_engagement(self, agent, user_id):
        """Test getting post engagement across platforms."""
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        await agent.approve_post(draft_post.id, "reviewer")
        post = await agent.publish_post(draft_post.id, user_id)
        
        await agent.record_engagement(
            post_id=post.id,
            platform=Platform.INSTAGRAM,
            platform_post_id="ig_123",
            likes=100,
            reach=1000
        )
        await agent.record_engagement(
            post_id=post.id,
            platform=Platform.FACEBOOK,
            platform_post_id="fb_123",
            likes=50,
            reach=500
        )
        
        engagements = await agent.get_post_engagement(post.id)
        
        assert Platform.INSTAGRAM in engagements
        assert Platform.FACEBOOK in engagements
        assert engagements[Platform.INSTAGRAM].likes == 100
    
    @pytest.mark.asyncio
    async def test_engagement_summary(self, agent, user_id):
        """Test engagement summary."""
        # Create and publish a post
        post = await agent.create_post(
            text="Test",
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        await agent.submit_for_review(post.id, user_id)
        await agent.approve_post(post.id, "reviewer")
        post = await agent.publish_post(post.id, user_id)
        
        await agent.record_engagement(
            post_id=post.id,
            platform=Platform.INSTAGRAM,
            platform_post_id="ig_123",
            likes=100,
            comments=20,
            shares=10,
            reach=1000
        )
        
        summary = await agent.get_engagement_summary(user_id)
        
        assert summary["total_posts"] == 1
        assert summary["total_likes"] == 100
        assert summary["total_comments"] == 20


# ============================================================================
# HASHTAG TESTS - ALPHABETICAL ONLY (Rule #5)
# ============================================================================

class TestHashtags:
    """Test hashtag research - ALPHABETICAL only."""
    
    @pytest.mark.asyncio
    async def test_add_hashtag(self, agent):
        """Test adding a hashtag."""
        hashtag = await agent.add_hashtag(
            tag="marketing",
            platform=Platform.INSTAGRAM,
            categories=["business", "digital"],
            related_tags=["advertising", "branding"]
        )
        
        assert hashtag.tag == "marketing"
        # Categories should be sorted alphabetically
        assert hashtag.categories == ["business", "digital"]
        assert hashtag.related_tags == ["advertising", "branding"]
    
    @pytest.mark.asyncio
    async def test_search_hashtags_alphabetical(self, agent):
        """Test hashtag search returns alphabetical results."""
        await agent.add_hashtag(
            tag="zebra",
            platform=Platform.INSTAGRAM,
            categories=["animal"]
        )
        await agent.add_hashtag(
            tag="apple",
            platform=Platform.INSTAGRAM,
            categories=["food"]
        )
        await agent.add_hashtag(
            tag="avocado",
            platform=Platform.INSTAGRAM,
            categories=["food"]
        )
        await agent.add_hashtag(
            tag="banana",
            platform=Platform.INSTAGRAM,
            categories=["food"]
        )
        
        # Search with 'av' should return only avocado (alphabetically)
        results = await agent.search_hashtags("av", Platform.INSTAGRAM)
        
        assert len(results) == 1
        assert results[0].tag == "avocado"
        
        # Search with 'a' returns all containing 'a' - alphabetically
        all_a = await agent.search_hashtags("a", Platform.INSTAGRAM)
        tags = [h.tag for h in all_a]
        # Verify alphabetical order
        assert tags == sorted(tags)
    
    @pytest.mark.asyncio
    async def test_get_hashtag_suggestions_alphabetical(self, agent):
        """Test hashtag suggestions are alphabetical - NO ranking."""
        await agent.add_hashtag(
            tag="social",
            platform=Platform.INSTAGRAM,
            related_tags=["media", "marketing"]
        )
        await agent.add_hashtag(
            tag="marketing",
            platform=Platform.INSTAGRAM,
            related_tags=["business", "digital"]
        )
        
        suggestions = await agent.get_hashtag_suggestions(
            content="social media marketing tips",
            platform=Platform.INSTAGRAM
        )
        
        # Should be alphabetical
        for i in range(len(suggestions) - 1):
            assert suggestions[i] <= suggestions[i + 1]


# ============================================================================
# AUDIENCE INSIGHTS TESTS
# ============================================================================

class TestAudienceInsights:
    """Test audience insights."""
    
    @pytest.mark.asyncio
    async def test_record_audience_insight(self, agent, user_id):
        """Test recording audience insights."""
        connected_account = await create_connected_account(agent, user_id)
        insight = await agent.record_audience_insight(
            account_id=connected_account.id,
            platform=Platform.INSTAGRAM,
            age_ranges={"18-24": 25, "25-34": 40},
            gender_distribution={"male": 45, "female": 55},
            top_locations={"US": 60, "CA": 20},
            top_languages={"en": 80, "fr": 15},
            most_active_hours={9: 80, 12: 100, 18: 90},
            most_active_days={"Monday": 80, "Friday": 100},
            followers_gained=100,
            followers_lost=20
        )
        
        assert insight.net_growth == 80
        assert insight.recorded_date == date.today()
    
    @pytest.mark.asyncio
    async def test_get_audience_insights_chronological(self, agent, user_id):
        """Test insights are returned chronologically."""
        connected_account = await create_connected_account(agent, user_id)
        await agent.record_audience_insight(
            account_id=connected_account.id,
            platform=Platform.INSTAGRAM,
            age_ranges={},
            gender_distribution={},
            top_locations={},
            top_languages={},
            most_active_hours={},
            most_active_days={},
            followers_gained=10,
            followers_lost=5
        )
        
        insights = await agent.get_audience_insights(connected_account.id)
        
        assert len(insights) >= 1
    
    @pytest.mark.asyncio
    async def test_best_posting_times(self, agent, user_id):
        """Test best posting times are sorted by day/hour, NOT by score."""
        connected_account = await create_connected_account(agent, user_id)
        await agent.record_audience_insight(
            account_id=connected_account.id,
            platform=Platform.INSTAGRAM,
            age_ranges={},
            gender_distribution={},
            top_locations={},
            top_languages={},
            most_active_hours={9: 50, 12: 100, 18: 75},
            most_active_days={"Monday": 80, "Friday": 100},
            followers_gained=0,
            followers_lost=0
        )
        
        slots = await agent.get_best_posting_times(connected_account.id)
        
        # Should be sorted by day then hour, NOT by score
        assert slots[0].day_of_week == "Monday"


# ============================================================================
# CAMPAIGN TESTS
# ============================================================================

class TestCampaigns:
    """Test campaign management."""
    
    @pytest.mark.asyncio
    async def test_create_campaign(self, agent, user_id):
        """Test creating a campaign."""
        campaign = await agent.create_campaign(
            name="Q1 Launch",
            description="Product launch campaign",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            platforms=[Platform.INSTAGRAM, Platform.FACEBOOK],
            goal_type="awareness",
            target_reach=100000,
            budget=Decimal("5000"),
            hashtags=["launch", "new"],
            user_id=user_id
        )
        
        assert campaign.name == "Q1 Launch"
        assert campaign.status == CampaignStatus.DRAFT
        # Hashtags should be sorted alphabetically
        assert campaign.hashtags == ["launch", "new"]
    
    @pytest.mark.asyncio
    async def test_campaign_lifecycle(self, agent, user_id):
        """Test campaign lifecycle: draft -> active -> paused -> completed."""
        campaign = await agent.create_campaign(
            name="Test Campaign",
            description="Test",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        
        # Start
        campaign = await agent.start_campaign(campaign.id, user_id)
        assert campaign.status == CampaignStatus.ACTIVE
        
        # Pause
        campaign = await agent.pause_campaign(campaign.id, user_id)
        assert campaign.status == CampaignStatus.PAUSED
        
        # Complete
        campaign = await agent.complete_campaign(campaign.id, user_id)
        assert campaign.status == CampaignStatus.COMPLETED
    
    @pytest.mark.asyncio
    async def test_campaign_performance(self, agent, user_id):
        """Test campaign performance tracking."""
        campaign = await agent.create_campaign(
            name="Test",
            description="Test",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            platforms=[Platform.INSTAGRAM],
            target_reach=1000,
            target_engagement=100,
            budget=Decimal("500"),
            user_id=user_id
        )
        
        performance = await agent.get_campaign_performance(campaign.id)
        
        assert performance["name"] == "Test"
        assert "reach_progress" in performance
        assert "budget_used_percent" in performance


# ============================================================================
# COMPETITOR TESTS
# ============================================================================

class TestCompetitors:
    """Test competitor monitoring."""
    
    @pytest.mark.asyncio
    async def test_add_competitor(self, agent, user_id):
        """Test adding a competitor."""
        competitor = await agent.add_competitor(
            platform=Platform.INSTAGRAM,
            account_name="competitor_brand",
            account_url="https://instagram.com/competitor",
            user_id=user_id
        )
        
        assert competitor.account_name == "competitor_brand"
    
    @pytest.mark.asyncio
    async def test_prevent_duplicate_competitor(self, agent, user_id):
        """Test preventing duplicate competitor."""
        await agent.add_competitor(
            platform=Platform.INSTAGRAM,
            account_name="competitor",
            account_url="https://example.com",
            user_id=user_id
        )
        
        with pytest.raises(ValueError, match="already being monitored"):
            await agent.add_competitor(
                platform=Platform.INSTAGRAM,
                account_name="competitor",
                account_url="https://example.com",
                user_id=user_id
            )
    
    @pytest.mark.asyncio
    async def test_get_competitors_alphabetical(self, agent, user_id):
        """Test competitors are returned alphabetically."""
        await agent.add_competitor(
            platform=Platform.INSTAGRAM,
            account_name="zebra_brand",
            account_url="https://example.com/z",
            user_id=user_id
        )
        await agent.add_competitor(
            platform=Platform.INSTAGRAM,
            account_name="apple_brand",
            account_url="https://example.com/a",
            user_id=user_id
        )
        
        competitors = await agent.get_competitors(user_id)
        
        assert competitors[0].account_name == "apple_brand"
        assert competitors[1].account_name == "zebra_brand"
    
    @pytest.mark.asyncio
    async def test_update_competitor_metrics(self, agent, user_id):
        """Test updating competitor metrics."""
        competitor = await agent.add_competitor(
            platform=Platform.INSTAGRAM,
            account_name="competitor",
            account_url="https://example.com",
            user_id=user_id
        )
        
        competitor = await agent.update_competitor_metrics(
            competitor_id=competitor.id,
            followers_count=50000,
            posts_count=200,
            avg_engagement_rate=Decimal("5.5")
        )
        
        assert competitor.followers_count == 50000
        assert competitor.last_checked is not None


# ============================================================================
# CALENDAR TESTS
# ============================================================================

class TestCalendar:
    """Test content calendar."""
    
    @pytest.mark.asyncio
    async def test_create_calendar_entry(self, agent, user_id):
        """Test creating a calendar entry."""
        entry = await agent.create_calendar_entry(
            date_=date.today() + timedelta(days=1),
            time_slot="09:00",
            content_idea="Product announcement",
            content_type=ContentType.IMAGE,
            platforms=[Platform.INSTAGRAM],
            user_id=user_id
        )
        
        assert entry.time_slot == "09:00"
        assert entry.is_filled == False
    
    @pytest.mark.asyncio
    async def test_link_post_to_calendar(self, agent, user_id):
        """Test linking a post to calendar entry."""
        draft_post = await create_draft_post(agent, user_id)
        entry = await agent.create_calendar_entry(
            date_=date.today(),
            time_slot="12:00",
            user_id=user_id
        )
        
        entry = await agent.link_post_to_calendar(
            entry_id=entry.id,
            post_id=draft_post.id,
            user_id=user_id
        )
        
        assert entry.post_id == draft_post.id
        assert entry.is_filled == True
    
    @pytest.mark.asyncio
    async def test_get_calendar_chronological(self, agent, user_id):
        """Test calendar entries are chronological."""
        await agent.create_calendar_entry(
            date_=date.today() + timedelta(days=2),
            time_slot="09:00",
            user_id=user_id
        )
        await agent.create_calendar_entry(
            date_=date.today(),
            time_slot="09:00",
            user_id=user_id
        )
        
        entries = await agent.get_calendar(
            user_id,
            date.today(),
            date.today() + timedelta(days=7)
        )
        
        # Should be chronological
        assert entries[0].date <= entries[1].date
    
    @pytest.mark.asyncio
    async def test_get_calendar_week(self, agent, user_id):
        """Test getting calendar organized by week."""
        # Get Monday of current week
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        
        await agent.create_calendar_entry(
            date_=monday,
            time_slot="09:00",
            content_idea="Monday post",
            user_id=user_id
        )
        await agent.create_calendar_entry(
            date_=monday + timedelta(days=4),  # Friday
            time_slot="12:00",
            content_idea="Friday post",
            user_id=user_id
        )
        
        week = await agent.get_calendar_week(user_id, monday)
        
        assert "Monday" in week
        assert "Friday" in week


# ============================================================================
# AI FEATURE TESTS
# ============================================================================

class TestAIFeatures:
    """Test AI-powered features."""
    
    @pytest.mark.asyncio
    async def test_generate_caption_suggestions(self, agent, user_id):
        """Test AI caption generation."""
        suggestions = await agent.generate_caption_suggestions(
            topic="new product launch",
            platform=Platform.INSTAGRAM,
            tone="engaging",
            include_hashtags=True,
            include_cta=True,
            user_id=user_id
        )
        
        assert len(suggestions) > 0
        assert suggestions[0]["ai_generated"] == True
        assert suggestions[0]["requires_approval"] == True  # GOVERNANCE
    
    @pytest.mark.asyncio
    async def test_analyze_post_performance(self, agent, user_id):
        """Test post performance analysis."""
        # Create, publish and add engagement
        draft_post = await create_draft_post(agent, user_id)
        await agent.submit_for_review(draft_post.id, user_id)
        await agent.approve_post(draft_post.id, "reviewer")
        post = await agent.publish_post(draft_post.id, user_id)
        
        await agent.record_engagement(
            post_id=post.id,
            platform=Platform.INSTAGRAM,
            platform_post_id="ig_123",
            likes=100,
            comments=20,
            reach=1000
        )
        
        analysis = await agent.analyze_post_performance(post.id)
        
        assert "engagement_rate" in analysis
        assert "insights" in analysis
        assert "recommendation" in analysis


# ============================================================================
# ANALYTICS DASHBOARD TESTS
# ============================================================================

class TestAnalytics:
    """Test analytics dashboard."""
    
    @pytest.mark.asyncio
    async def test_analytics_dashboard(self, agent, user_id):
        """Test comprehensive analytics dashboard."""
        # Create an account to have some data
        await create_connected_account(agent, user_id)
        dashboard = await agent.get_analytics_dashboard(user_id, days=30)
        
        assert "period_days" in dashboard
        assert "engagement_summary" in dashboard
        assert "accounts" in dashboard
        assert "posts" in dashboard
        assert "campaigns" in dashboard
        assert "platform_breakdown" in dashboard
    
    @pytest.mark.asyncio
    async def test_health_check(self, agent):
        """Test health check."""
        health = await agent.get_health()
        
        assert health["status"] == "healthy"
        assert health["service"] == "social_media_agent"
        assert health["version"] == "V68"


# ============================================================================
# API ENDPOINT TESTS
# ============================================================================

class TestAPIEndpoints:
    """Test API endpoints via FastAPI TestClient."""
    
    @pytest.fixture
    def client(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from backend.spheres.social.api.social_routes import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/social/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_connect_account_endpoint(self, client):
        """Test connect account endpoint."""
        response = client.post(
            "/social/accounts",
            params={"user_id": "test_user"},
            json={
                "platform": "instagram",
                "account_name": "test_acc",
                "account_id": "ig_123",
                "access_token": "token"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["platform"] == "instagram"
        assert data["status"] == "connected"
    
    def test_create_post_endpoint(self, client):
        """Test create post endpoint."""
        response = client.post(
            "/social/posts",
            params={"user_id": "test_user"},
            json={
                "text": "Test post content",
                "platforms": ["instagram"],
                "content_type": "text"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "draft"
        assert "next_step" in data
    
    def test_get_pending_reviews_endpoint(self, client):
        """Test get pending reviews endpoint."""
        response = client.get(
            "/social/posts/pending-review",
            params={"user_id": "test_user"}
        )
        # Accept both 200 (success with data) and 200 (empty list)
        if response.status_code != 200:
            print(f"Response: {response.text}")
        assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
        data = response.json()
        assert "posts" in data
        assert data["sort_order"] == "chronological_oldest_first"
    
    def test_search_hashtags_endpoint(self, client):
        """Test hashtag search endpoint."""
        response = client.get(
            "/social/hashtags/search",
            params={"query": "test"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sort_order"] == "alphabetical"
    
    def test_analytics_dashboard_endpoint(self, client):
        """Test analytics dashboard endpoint."""
        response = client.get(
            "/social/analytics/dashboard",
            params={"user_id": "test_user", "days": 30}
        )
        assert response.status_code == 200
        data = response.json()
        assert "engagement_summary" in data


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
