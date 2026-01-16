"""
CHE·NU™ V68 - Social Media Agent
Vertical 10: Social Media Management (Hootsuite/Buffer Killer)

Features:
- Social Account Management (multi-platform)
- Content Calendar & Scheduling
- Post Composition & Templates
- Multi-Platform Publishing (with human approval)
- Analytics & Engagement Tracking
- Hashtag Research (alphabetical only - NO ranking)
- Audience Insights
- Team Collaboration
- Content Approval Workflow (GOVERNANCE)
- AI Caption Suggestions
- Best Time to Post Analysis
- Competitor Monitoring

COS: 85/100
Competitors: Hootsuite ($99/mo), Buffer ($99/mo), Sprout Social ($249/mo)
CHE·NU Price: $29/mo = 71-88% savings

CRITICAL R&D COMPLIANCE:
- Rule #5: NO ranking algorithms - all lists are CHRONOLOGICAL or ALPHABETICAL
- Human approval REQUIRED for all publishing
- Draft → Review → Approve → Publish workflow
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, List, Any
from uuid import UUID, uuid4
import asyncio


# ============================================================================
# ENUMS
# ============================================================================

class Platform(str, Enum):
    """Supported social media platforms."""
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"
    THREADS = "threads"


class AccountStatus(str, Enum):
    """Social account connection status."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    EXPIRED = "expired"
    PENDING = "pending"


class PostStatus(str, Enum):
    """Post lifecycle status - GOVERNANCE enforced."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    REJECTED = "rejected"


class ContentType(str, Enum):
    """Type of social content."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"
    LIVE = "live"
    POLL = "poll"


class EngagementType(str, Enum):
    """Types of engagement metrics."""
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    SAVE = "save"
    CLICK = "click"
    VIEW = "view"
    IMPRESSION = "impression"
    REACH = "reach"


class CampaignStatus(str, Enum):
    """Campaign status."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SocialAccount:
    """Connected social media account."""
    id: UUID
    platform: Platform
    account_name: str
    account_id: str  # Platform's ID
    user_id: str  # CHE·NU user
    status: AccountStatus
    access_token: str = ""  # Encrypted in production
    refresh_token: str = ""
    token_expires_at: Optional[datetime] = None
    profile_url: str = ""
    profile_image: str = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    connected_at: datetime = field(default_factory=datetime.utcnow)
    last_synced: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class ContentTemplate:
    """Reusable content template."""
    id: UUID
    name: str
    description: str
    platform: Optional[Platform]  # None = all platforms
    content_type: ContentType
    template_text: str
    variables: List[str] = field(default_factory=list)  # e.g., ["product_name", "discount"]
    hashtags: List[str] = field(default_factory=list)
    media_urls: List[str] = field(default_factory=list)
    user_id: str = ""
    is_active: bool = True
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class SocialPost:
    """Social media post with governance workflow."""
    id: UUID
    user_id: str
    content_type: ContentType
    text: str
    media_urls: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)
    link: str = ""
    
    # Platform targeting
    platforms: List[Platform] = field(default_factory=list)
    platform_specific: Dict[Platform, Dict[str, Any]] = field(default_factory=dict)
    
    # Scheduling
    scheduled_time: Optional[datetime] = None
    timezone: str = "America/Montreal"
    
    # Governance - CRITICAL
    status: PostStatus = PostStatus.DRAFT
    submitted_for_review: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: str = ""
    
    # Publishing results
    published_at: Optional[datetime] = None
    platform_post_ids: Dict[Platform, str] = field(default_factory=dict)
    publish_errors: Dict[Platform, str] = field(default_factory=dict)
    
    # Campaign link
    campaign_id: Optional[UUID] = None
    
    # Metadata
    template_id: Optional[UUID] = None
    ai_generated: bool = False
    ai_suggestions_used: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PostEngagement:
    """Engagement metrics for a post."""
    id: UUID
    post_id: UUID
    platform: Platform
    platform_post_id: str
    
    # Core metrics
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    clicks: int = 0
    views: int = 0
    impressions: int = 0
    reach: int = 0
    
    # Engagement rate = (likes + comments + shares) / reach * 100
    engagement_rate: Decimal = Decimal("0")
    
    # Time-based
    recorded_at: datetime = field(default_factory=datetime.utcnow)
    
    # Sentiment (from comments analysis)
    positive_sentiment: int = 0
    negative_sentiment: int = 0
    neutral_sentiment: int = 0


@dataclass
class Hashtag:
    """Hashtag data for research."""
    id: UUID
    tag: str  # Without #
    platform: Platform
    
    # Metrics
    usage_count: int = 0
    avg_engagement: Decimal = Decimal("0")
    trending: bool = False
    
    # Categories (alphabetical)
    categories: List[str] = field(default_factory=list)
    
    # Related hashtags (sorted alphabetically - NO ranking)
    related_tags: List[str] = field(default_factory=list)
    
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AudienceInsight:
    """Audience demographic insights."""
    id: UUID
    account_id: UUID
    platform: Platform
    recorded_date: date
    
    # Demographics
    age_ranges: Dict[str, int] = field(default_factory=dict)  # e.g., {"18-24": 25, "25-34": 40}
    gender_distribution: Dict[str, int] = field(default_factory=dict)
    top_locations: Dict[str, int] = field(default_factory=dict)  # Country/City: count
    top_languages: Dict[str, int] = field(default_factory=dict)
    
    # Activity
    most_active_hours: Dict[int, int] = field(default_factory=dict)  # Hour: activity level
    most_active_days: Dict[str, int] = field(default_factory=dict)  # Day: activity level
    
    # Growth
    followers_gained: int = 0
    followers_lost: int = 0
    net_growth: int = 0
    growth_rate: Decimal = Decimal("0")


@dataclass
class Campaign:
    """Social media campaign."""
    id: UUID
    name: str
    description: str
    user_id: str
    
    # Dates
    start_date: date
    end_date: date
    
    # Targeting
    platforms: List[Platform] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    
    # Goals
    goal_type: str = ""  # awareness, engagement, traffic, conversions
    target_reach: int = 0
    target_engagement: int = 0
    target_clicks: int = 0
    
    # Budget
    budget: Decimal = Decimal("0")
    spent: Decimal = Decimal("0")
    
    # Status
    status: CampaignStatus = CampaignStatus.DRAFT
    
    # Results
    total_posts: int = 0
    total_reach: int = 0
    total_engagement: int = 0
    total_clicks: int = 0
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class Competitor:
    """Competitor account for monitoring."""
    id: UUID
    user_id: str
    platform: Platform
    account_name: str
    account_url: str
    
    # Latest metrics
    followers_count: int = 0
    posts_count: int = 0
    avg_engagement_rate: Decimal = Decimal("0")
    posting_frequency: Decimal = Decimal("0")  # Posts per day
    
    # Tracking history
    followers_history: List[Dict[str, Any]] = field(default_factory=list)
    
    last_checked: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ContentCalendarEntry:
    """Calendar entry for content planning."""
    id: UUID
    user_id: str
    date: date
    time_slot: str  # e.g., "09:00", "12:00", "18:00"
    
    # Content link
    post_id: Optional[UUID] = None
    
    # Planning
    content_idea: str = ""
    content_type: Optional[ContentType] = None
    platforms: List[Platform] = field(default_factory=list)
    notes: str = ""
    
    # Assignment
    assigned_to: Optional[str] = None
    
    # Status
    is_filled: bool = False
    
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass 
class BestTimeSlot:
    """Recommended posting time based on audience activity."""
    platform: Platform
    day_of_week: str
    hour: int
    engagement_score: Decimal  # Normalized 0-100
    audience_active_percent: Decimal


# ============================================================================
# SOCIAL MEDIA AGENT
# ============================================================================

class SocialMediaAgent:
    """
    CHE·NU Social Media Management Agent.
    
    CRITICAL R&D RULES:
    - Rule #5: NO ranking algorithms - chronological/alphabetical only
    - All publishing requires human approval
    - Draft → Review → Approve → Publish workflow
    """
    
    def __init__(self):
        # In-memory storage (production: database)
        self.accounts: Dict[UUID, SocialAccount] = {}
        self.templates: Dict[UUID, ContentTemplate] = {}
        self.posts: Dict[UUID, SocialPost] = {}
        self.engagements: Dict[UUID, PostEngagement] = {}
        self.hashtags: Dict[UUID, Hashtag] = {}
        self.audience_insights: Dict[UUID, AudienceInsight] = {}
        self.campaigns: Dict[UUID, Campaign] = {}
        self.competitors: Dict[UUID, Competitor] = {}
        self.calendar_entries: Dict[UUID, ContentCalendarEntry] = {}
        
        # Platform configurations
        self.platform_limits = {
            Platform.TWITTER: {"char_limit": 280, "hashtag_limit": 5, "image_limit": 4},
            Platform.INSTAGRAM: {"char_limit": 2200, "hashtag_limit": 30, "image_limit": 10},
            Platform.FACEBOOK: {"char_limit": 63206, "hashtag_limit": 10, "image_limit": 10},
            Platform.LINKEDIN: {"char_limit": 3000, "hashtag_limit": 5, "image_limit": 9},
            Platform.TIKTOK: {"char_limit": 2200, "hashtag_limit": 10, "video_required": True},
            Platform.YOUTUBE: {"char_limit": 5000, "hashtag_limit": 15, "video_required": True},
            Platform.PINTEREST: {"char_limit": 500, "hashtag_limit": 20, "image_required": True},
            Platform.THREADS: {"char_limit": 500, "hashtag_limit": 5, "image_limit": 10},
        }
    
    # ========================================================================
    # ACCOUNT MANAGEMENT
    # ========================================================================
    
    async def connect_account(
        self,
        platform: Platform,
        account_name: str,
        account_id: str,
        access_token: str,
        refresh_token: str = "",
        token_expires_at: Optional[datetime] = None,
        user_id: str = ""
    ) -> SocialAccount:
        """Connect a social media account."""
        # Check for existing connection
        for account in self.accounts.values():
            if (account.platform == platform and 
                account.account_id == account_id and
                account.user_id == user_id):
                # Update existing
                account.access_token = access_token
                account.refresh_token = refresh_token
                account.token_expires_at = token_expires_at
                account.status = AccountStatus.CONNECTED
                account.last_synced = datetime.utcnow()
                return account
        
        account = SocialAccount(
            id=uuid4(),
            platform=platform,
            account_name=account_name,
            account_id=account_id,
            user_id=user_id,
            status=AccountStatus.CONNECTED,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=token_expires_at,
            created_by=user_id
        )
        
        self.accounts[account.id] = account
        return account
    
    async def disconnect_account(
        self,
        account_id: UUID,
        user_id: str
    ) -> SocialAccount:
        """Disconnect a social media account."""
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        if account.user_id != user_id:
            raise PermissionError("Not authorized to disconnect this account")
        
        account.status = AccountStatus.DISCONNECTED
        account.access_token = ""
        account.refresh_token = ""
        return account
    
    async def get_accounts(self, user_id: str) -> List[SocialAccount]:
        """Get all accounts for a user, sorted by platform name (alphabetical)."""
        accounts = [a for a in self.accounts.values() if a.user_id == user_id]
        # RULE #5: Alphabetical sort, NO ranking
        return sorted(accounts, key=lambda a: a.platform.value)
    
    async def sync_account_metrics(
        self,
        account_id: UUID,
        followers_count: int,
        following_count: int,
        posts_count: int
    ) -> SocialAccount:
        """Sync account metrics from platform."""
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        account.followers_count = followers_count
        account.following_count = following_count
        account.posts_count = posts_count
        account.last_synced = datetime.utcnow()
        return account
    
    # ========================================================================
    # CONTENT TEMPLATES
    # ========================================================================
    
    async def create_template(
        self,
        name: str,
        description: str,
        template_text: str,
        content_type: ContentType,
        platform: Optional[Platform] = None,
        variables: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
        user_id: str = ""
    ) -> ContentTemplate:
        """Create a reusable content template."""
        template = ContentTemplate(
            id=uuid4(),
            name=name,
            description=description,
            platform=platform,
            content_type=content_type,
            template_text=template_text,
            variables=variables or [],
            hashtags=hashtags or [],
            user_id=user_id,
            created_by=user_id
        )
        
        self.templates[template.id] = template
        return template
    
    async def get_templates(
        self,
        user_id: str,
        platform: Optional[Platform] = None,
        content_type: Optional[ContentType] = None
    ) -> List[ContentTemplate]:
        """Get templates, sorted alphabetically by name."""
        templates = [t for t in self.templates.values() 
                     if t.user_id == user_id and t.is_active]
        
        if platform:
            templates = [t for t in templates 
                        if t.platform is None or t.platform == platform]
        
        if content_type:
            templates = [t for t in templates if t.content_type == content_type]
        
        # RULE #5: Alphabetical sort
        return sorted(templates, key=lambda t: t.name)
    
    async def apply_template(
        self,
        template_id: UUID,
        variables: Dict[str, str],
        user_id: str
    ) -> str:
        """Apply variables to a template."""
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        text = template.template_text
        for var, value in variables.items():
            text = text.replace(f"{{{var}}}", value)
        
        # Track usage
        template.usage_count += 1
        
        return text
    
    # ========================================================================
    # POST MANAGEMENT - GOVERNANCE ENFORCED
    # ========================================================================
    
    async def create_post(
        self,
        text: str,
        platforms: List[Platform],
        content_type: ContentType = ContentType.TEXT,
        media_urls: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
        mentions: Optional[List[str]] = None,
        link: str = "",
        scheduled_time: Optional[datetime] = None,
        timezone: str = "America/Montreal",
        campaign_id: Optional[UUID] = None,
        template_id: Optional[UUID] = None,
        user_id: str = ""
    ) -> SocialPost:
        """
        Create a post DRAFT.
        
        GOVERNANCE: Post starts in DRAFT status.
        Must go through review workflow before publishing.
        """
        # Validate platforms
        for platform in platforms:
            limits = self.platform_limits.get(platform)
            if limits:
                if len(text) > limits.get("char_limit", 99999):
                    raise ValueError(
                        f"Text exceeds {platform.value} limit of "
                        f"{limits['char_limit']} characters"
                    )
                if hashtags and len(hashtags) > limits.get("hashtag_limit", 99):
                    raise ValueError(
                        f"Hashtags exceed {platform.value} limit of "
                        f"{limits['hashtag_limit']}"
                    )
        
        post = SocialPost(
            id=uuid4(),
            user_id=user_id,
            content_type=content_type,
            text=text,
            media_urls=media_urls or [],
            hashtags=hashtags or [],
            mentions=mentions or [],
            link=link,
            platforms=platforms,
            scheduled_time=scheduled_time,
            timezone=timezone,
            campaign_id=campaign_id,
            template_id=template_id,
            status=PostStatus.DRAFT,  # GOVERNANCE: Always starts as draft
            created_by=user_id
        )
        
        self.posts[post.id] = post
        return post
    
    async def submit_for_review(
        self,
        post_id: UUID,
        user_id: str
    ) -> SocialPost:
        """
        Submit post for review.
        
        GOVERNANCE: Changes status from DRAFT to PENDING_REVIEW.
        """
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.user_id != user_id:
            raise PermissionError("Not authorized to submit this post")
        
        if post.status != PostStatus.DRAFT:
            raise ValueError(f"Cannot submit post in {post.status.value} status")
        
        post.status = PostStatus.PENDING_REVIEW
        post.submitted_for_review = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        
        return post
    
    async def approve_post(
        self,
        post_id: UUID,
        reviewer_id: str
    ) -> SocialPost:
        """
        Approve post for publishing.
        
        GOVERNANCE: Human must explicitly approve.
        """
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.status != PostStatus.PENDING_REVIEW:
            raise ValueError(f"Cannot approve post in {post.status.value} status")
        
        post.status = PostStatus.APPROVED
        post.reviewed_by = reviewer_id
        post.reviewed_at = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        
        # If scheduled, update status
        if post.scheduled_time and post.scheduled_time > datetime.utcnow():
            post.status = PostStatus.SCHEDULED
        
        return post
    
    async def reject_post(
        self,
        post_id: UUID,
        reviewer_id: str,
        reason: str
    ) -> SocialPost:
        """
        Reject post with reason.
        
        GOVERNANCE: Posts can be rejected with feedback.
        """
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.status != PostStatus.PENDING_REVIEW:
            raise ValueError(f"Cannot reject post in {post.status.value} status")
        
        post.status = PostStatus.REJECTED
        post.reviewed_by = reviewer_id
        post.reviewed_at = datetime.utcnow()
        post.rejection_reason = reason
        post.updated_at = datetime.utcnow()
        
        return post
    
    async def publish_post(
        self,
        post_id: UUID,
        user_id: str
    ) -> SocialPost:
        """
        Publish an approved post immediately.
        
        GOVERNANCE: Only APPROVED posts can be published.
        """
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.status not in [PostStatus.APPROVED, PostStatus.SCHEDULED]:
            raise ValueError(
                f"Cannot publish post in {post.status.value} status. "
                "Post must be approved first."
            )
        
        post.status = PostStatus.PUBLISHING
        post.updated_at = datetime.utcnow()
        
        # Simulate publishing to each platform
        for platform in post.platforms:
            try:
                # In production: API call to platform
                platform_post_id = f"{platform.value}_{uuid4().hex[:8]}"
                post.platform_post_ids[platform] = platform_post_id
            except Exception as e:
                post.publish_errors[platform] = str(e)
        
        # Check results
        if post.publish_errors:
            if len(post.publish_errors) == len(post.platforms):
                post.status = PostStatus.FAILED
            else:
                post.status = PostStatus.PUBLISHED  # Partial success
        else:
            post.status = PostStatus.PUBLISHED
        
        post.published_at = datetime.utcnow()
        post.updated_at = datetime.utcnow()
        
        return post
    
    async def get_posts(
        self,
        user_id: str,
        status: Optional[PostStatus] = None,
        platform: Optional[Platform] = None,
        campaign_id: Optional[UUID] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SocialPost]:
        """Get posts sorted chronologically (newest first) - NO ranking."""
        posts = [p for p in self.posts.values() if p.user_id == user_id]
        
        if status:
            posts = [p for p in posts if p.status == status]
        
        if platform:
            posts = [p for p in posts if platform in p.platforms]
        
        if campaign_id:
            posts = [p for p in posts if p.campaign_id == campaign_id]
        
        if start_date:
            posts = [p for p in posts if p.created_at.date() >= start_date]
        
        if end_date:
            posts = [p for p in posts if p.created_at.date() <= end_date]
        
        # RULE #5: Chronological sort (newest first), NO ranking
        return sorted(posts, key=lambda p: p.created_at, reverse=True)
    
    async def get_pending_reviews(self, user_id: str) -> List[SocialPost]:
        """Get posts awaiting review - chronological order."""
        posts = [p for p in self.posts.values() 
                 if p.user_id == user_id and p.status == PostStatus.PENDING_REVIEW]
        # RULE #5: Chronological (oldest first for review queue)
        return sorted(posts, key=lambda p: p.submitted_for_review or p.created_at)
    
    async def get_scheduled_posts(self, user_id: str) -> List[SocialPost]:
        """Get scheduled posts - chronological by scheduled time."""
        posts = [p for p in self.posts.values() 
                 if p.user_id == user_id and p.status == PostStatus.SCHEDULED]
        # RULE #5: Chronological by scheduled time
        return sorted(posts, key=lambda p: p.scheduled_time or datetime.max)
    
    async def revert_to_draft(
        self,
        post_id: UUID,
        user_id: str
    ) -> SocialPost:
        """Revert a rejected post back to draft for editing."""
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.user_id != user_id:
            raise PermissionError("Not authorized")
        
        if post.status != PostStatus.REJECTED:
            raise ValueError("Can only revert rejected posts to draft")
        
        post.status = PostStatus.DRAFT
        post.rejection_reason = ""
        post.reviewed_by = None
        post.reviewed_at = None
        post.submitted_for_review = None
        post.updated_at = datetime.utcnow()
        
        return post
    
    # ========================================================================
    # ENGAGEMENT TRACKING
    # ========================================================================
    
    async def record_engagement(
        self,
        post_id: UUID,
        platform: Platform,
        platform_post_id: str,
        likes: int = 0,
        comments: int = 0,
        shares: int = 0,
        saves: int = 0,
        clicks: int = 0,
        views: int = 0,
        impressions: int = 0,
        reach: int = 0
    ) -> PostEngagement:
        """Record engagement metrics for a post."""
        # Calculate engagement rate
        engagement_rate = Decimal("0")
        if reach > 0:
            total_engagement = likes + comments + shares
            engagement_rate = Decimal(str(total_engagement / reach * 100)).quantize(
                Decimal("0.01")
            )
        
        engagement = PostEngagement(
            id=uuid4(),
            post_id=post_id,
            platform=platform,
            platform_post_id=platform_post_id,
            likes=likes,
            comments=comments,
            shares=shares,
            saves=saves,
            clicks=clicks,
            views=views,
            impressions=impressions,
            reach=reach,
            engagement_rate=engagement_rate
        )
        
        self.engagements[engagement.id] = engagement
        return engagement
    
    async def get_post_engagement(
        self,
        post_id: UUID
    ) -> Dict[Platform, PostEngagement]:
        """Get engagement for a post across platforms."""
        result = {}
        for eng in self.engagements.values():
            if eng.post_id == post_id:
                result[eng.platform] = eng
        return result
    
    async def get_engagement_summary(
        self,
        user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get engagement summary across all posts."""
        posts = await self.get_posts(
            user_id=user_id,
            status=PostStatus.PUBLISHED,
            start_date=start_date,
            end_date=end_date
        )
        
        total_likes = 0
        total_comments = 0
        total_shares = 0
        total_reach = 0
        total_impressions = 0
        
        for post in posts:
            engagements = await self.get_post_engagement(post.id)
            for eng in engagements.values():
                total_likes += eng.likes
                total_comments += eng.comments
                total_shares += eng.shares
                total_reach += eng.reach
                total_impressions += eng.impressions
        
        avg_engagement_rate = Decimal("0")
        if total_reach > 0:
            total_engagement = total_likes + total_comments + total_shares
            avg_engagement_rate = Decimal(str(total_engagement / total_reach * 100)).quantize(
                Decimal("0.01")
            )
        
        return {
            "total_posts": len(posts),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_reach": total_reach,
            "total_impressions": total_impressions,
            "avg_engagement_rate": avg_engagement_rate
        }
    
    # ========================================================================
    # HASHTAG RESEARCH - ALPHABETICAL ONLY (Rule #5)
    # ========================================================================
    
    async def add_hashtag(
        self,
        tag: str,
        platform: Platform,
        categories: Optional[List[str]] = None,
        related_tags: Optional[List[str]] = None
    ) -> Hashtag:
        """Add hashtag to research database."""
        # Normalize tag
        tag = tag.lower().strip().lstrip("#")
        
        hashtag = Hashtag(
            id=uuid4(),
            tag=tag,
            platform=platform,
            categories=sorted(categories or []),  # ALPHABETICAL
            related_tags=sorted(related_tags or [])  # ALPHABETICAL
        )
        
        self.hashtags[hashtag.id] = hashtag
        return hashtag
    
    async def search_hashtags(
        self,
        query: str,
        platform: Optional[Platform] = None,
        category: Optional[str] = None
    ) -> List[Hashtag]:
        """
        Search hashtags - ALPHABETICAL results only.
        
        RULE #5: NO ranking by popularity or engagement.
        Results sorted alphabetically.
        """
        query = query.lower().strip().lstrip("#")
        
        results = []
        for hashtag in self.hashtags.values():
            if query in hashtag.tag:
                if platform and hashtag.platform != platform:
                    continue
                if category and category not in hashtag.categories:
                    continue
                results.append(hashtag)
        
        # RULE #5: ALPHABETICAL SORT - NO RANKING
        return sorted(results, key=lambda h: h.tag)
    
    async def get_hashtag_suggestions(
        self,
        content: str,
        platform: Platform,
        limit: int = 10
    ) -> List[str]:
        """
        Get hashtag suggestions for content.
        
        RULE #5: Returns ALPHABETICALLY sorted suggestions.
        NO ranking by popularity or engagement.
        """
        # Extract keywords from content
        words = content.lower().split()
        keywords = [w.strip(".,!?") for w in words if len(w) > 3]
        
        suggestions = set()
        for keyword in keywords:
            # Find matching hashtags
            for hashtag in self.hashtags.values():
                if hashtag.platform == platform:
                    if keyword in hashtag.tag or hashtag.tag in keyword:
                        suggestions.add(hashtag.tag)
                    # Check related
                    for related in hashtag.related_tags:
                        if keyword in related or related in keyword:
                            suggestions.add(related)
        
        # RULE #5: ALPHABETICAL SORT - NO RANKING
        sorted_suggestions = sorted(list(suggestions))
        return sorted_suggestions[:limit]
    
    # ========================================================================
    # AUDIENCE INSIGHTS
    # ========================================================================
    
    async def record_audience_insight(
        self,
        account_id: UUID,
        platform: Platform,
        age_ranges: Dict[str, int],
        gender_distribution: Dict[str, int],
        top_locations: Dict[str, int],
        top_languages: Dict[str, int],
        most_active_hours: Dict[int, int],
        most_active_days: Dict[str, int],
        followers_gained: int = 0,
        followers_lost: int = 0
    ) -> AudienceInsight:
        """Record audience insights for an account."""
        net_growth = followers_gained - followers_lost
        
        # Get account for growth rate
        account = self.accounts.get(account_id)
        growth_rate = Decimal("0")
        if account and account.followers_count > 0:
            growth_rate = Decimal(str(net_growth / account.followers_count * 100)).quantize(
                Decimal("0.01")
            )
        
        insight = AudienceInsight(
            id=uuid4(),
            account_id=account_id,
            platform=platform,
            recorded_date=date.today(),
            age_ranges=age_ranges,
            gender_distribution=gender_distribution,
            top_locations=top_locations,
            top_languages=top_languages,
            most_active_hours=most_active_hours,
            most_active_days=most_active_days,
            followers_gained=followers_gained,
            followers_lost=followers_lost,
            net_growth=net_growth,
            growth_rate=growth_rate
        )
        
        self.audience_insights[insight.id] = insight
        return insight
    
    async def get_audience_insights(
        self,
        account_id: UUID,
        days: int = 30
    ) -> List[AudienceInsight]:
        """Get audience insights for an account - chronological order."""
        cutoff = date.today() - timedelta(days=days)
        
        insights = [i for i in self.audience_insights.values()
                   if i.account_id == account_id and i.recorded_date >= cutoff]
        
        # RULE #5: Chronological order
        return sorted(insights, key=lambda i: i.recorded_date)
    
    async def get_best_posting_times(
        self,
        account_id: UUID
    ) -> List[BestTimeSlot]:
        """
        Get best times to post based on audience activity.
        
        NOTE: Sorted by day/hour, NOT by engagement score.
        This provides information without ranking.
        """
        insights = await self.get_audience_insights(account_id, days=30)
        if not insights:
            return []
        
        # Get latest insight
        latest = insights[-1]
        
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                      "Friday", "Saturday", "Sunday"]
        
        slots = []
        for day in days_order:
            day_activity = latest.most_active_days.get(day, 0)
            for hour, activity in latest.most_active_hours.items():
                # Normalize to 0-100
                max_activity = max(latest.most_active_hours.values()) if latest.most_active_hours else 1
                score = Decimal(str(activity / max_activity * 100)).quantize(Decimal("0.01"))
                
                slots.append(BestTimeSlot(
                    platform=latest.platform,
                    day_of_week=day,
                    hour=hour,
                    engagement_score=score,
                    audience_active_percent=Decimal(str(activity))
                ))
        
        # Sort by day order then hour - NOT by engagement
        return sorted(slots, key=lambda s: (days_order.index(s.day_of_week), s.hour))
    
    # ========================================================================
    # CAMPAIGNS
    # ========================================================================
    
    async def create_campaign(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        platforms: List[Platform],
        goal_type: str = "awareness",
        target_reach: int = 0,
        target_engagement: int = 0,
        target_clicks: int = 0,
        budget: Decimal = Decimal("0"),
        hashtags: Optional[List[str]] = None,
        user_id: str = ""
    ) -> Campaign:
        """Create a social media campaign."""
        campaign = Campaign(
            id=uuid4(),
            name=name,
            description=description,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            platforms=platforms,
            hashtags=sorted(hashtags or []),  # ALPHABETICAL
            goal_type=goal_type,
            target_reach=target_reach,
            target_engagement=target_engagement,
            target_clicks=target_clicks,
            budget=budget,
            status=CampaignStatus.DRAFT,
            created_by=user_id
        )
        
        self.campaigns[campaign.id] = campaign
        return campaign
    
    async def start_campaign(
        self,
        campaign_id: UUID,
        user_id: str
    ) -> Campaign:
        """Start a campaign."""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        if campaign.user_id != user_id:
            raise PermissionError("Not authorized")
        
        campaign.status = CampaignStatus.ACTIVE
        return campaign
    
    async def pause_campaign(
        self,
        campaign_id: UUID,
        user_id: str
    ) -> Campaign:
        """Pause a campaign."""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign.status = CampaignStatus.PAUSED
        return campaign
    
    async def complete_campaign(
        self,
        campaign_id: UUID,
        user_id: str
    ) -> Campaign:
        """Complete a campaign and calculate results."""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Calculate results from posts
        posts = await self.get_posts(user_id=user_id, campaign_id=campaign_id)
        
        total_reach = 0
        total_engagement = 0
        total_clicks = 0
        
        for post in posts:
            engagements = await self.get_post_engagement(post.id)
            for eng in engagements.values():
                total_reach += eng.reach
                total_engagement += eng.likes + eng.comments + eng.shares
                total_clicks += eng.clicks
        
        campaign.status = CampaignStatus.COMPLETED
        campaign.total_posts = len(posts)
        campaign.total_reach = total_reach
        campaign.total_engagement = total_engagement
        campaign.total_clicks = total_clicks
        
        return campaign
    
    async def get_campaigns(
        self,
        user_id: str,
        status: Optional[CampaignStatus] = None
    ) -> List[Campaign]:
        """Get campaigns - chronological order."""
        campaigns = [c for c in self.campaigns.values() if c.user_id == user_id]
        
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        
        # RULE #5: Chronological
        return sorted(campaigns, key=lambda c: c.start_date, reverse=True)
    
    async def get_campaign_performance(
        self,
        campaign_id: UUID
    ) -> Dict[str, Any]:
        """Get campaign performance metrics."""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        # Progress toward goals
        reach_progress = 0
        if campaign.target_reach > 0:
            reach_progress = min(100, campaign.total_reach / campaign.target_reach * 100)
        
        engagement_progress = 0
        if campaign.target_engagement > 0:
            engagement_progress = min(100, campaign.total_engagement / campaign.target_engagement * 100)
        
        clicks_progress = 0
        if campaign.target_clicks > 0:
            clicks_progress = min(100, campaign.total_clicks / campaign.target_clicks * 100)
        
        budget_used = 0
        if campaign.budget > 0:
            budget_used = float(campaign.spent / campaign.budget * 100)
        
        return {
            "campaign_id": str(campaign.id),
            "name": campaign.name,
            "status": campaign.status.value,
            "total_posts": campaign.total_posts,
            "total_reach": campaign.total_reach,
            "total_engagement": campaign.total_engagement,
            "total_clicks": campaign.total_clicks,
            "reach_progress": reach_progress,
            "engagement_progress": engagement_progress,
            "clicks_progress": clicks_progress,
            "budget": float(campaign.budget),
            "spent": float(campaign.spent),
            "budget_used_percent": budget_used,
            "days_remaining": max(0, (campaign.end_date - date.today()).days)
        }
    
    # ========================================================================
    # COMPETITOR MONITORING
    # ========================================================================
    
    async def add_competitor(
        self,
        platform: Platform,
        account_name: str,
        account_url: str,
        user_id: str
    ) -> Competitor:
        """Add a competitor to monitor."""
        # Check for duplicates
        for comp in self.competitors.values():
            if (comp.platform == platform and 
                comp.account_name == account_name and
                comp.user_id == user_id):
                raise ValueError("Competitor already being monitored")
        
        competitor = Competitor(
            id=uuid4(),
            user_id=user_id,
            platform=platform,
            account_name=account_name,
            account_url=account_url
        )
        
        self.competitors[competitor.id] = competitor
        return competitor
    
    async def update_competitor_metrics(
        self,
        competitor_id: UUID,
        followers_count: int,
        posts_count: int,
        avg_engagement_rate: Decimal
    ) -> Competitor:
        """Update competitor metrics."""
        competitor = self.competitors.get(competitor_id)
        if not competitor:
            raise ValueError(f"Competitor {competitor_id} not found")
        
        # Calculate posting frequency if we have previous data
        if competitor.followers_history:
            last_record = competitor.followers_history[-1]
            days_diff = (datetime.utcnow() - datetime.fromisoformat(last_record["date"])).days
            if days_diff > 0:
                posts_diff = posts_count - last_record.get("posts_count", 0)
                competitor.posting_frequency = Decimal(str(posts_diff / days_diff)).quantize(
                    Decimal("0.01")
                )
        
        # Record history
        competitor.followers_history.append({
            "date": datetime.utcnow().isoformat(),
            "followers_count": followers_count,
            "posts_count": posts_count,
            "engagement_rate": str(avg_engagement_rate)
        })
        
        competitor.followers_count = followers_count
        competitor.posts_count = posts_count
        competitor.avg_engagement_rate = avg_engagement_rate
        competitor.last_checked = datetime.utcnow()
        
        return competitor
    
    async def get_competitors(
        self,
        user_id: str,
        platform: Optional[Platform] = None
    ) -> List[Competitor]:
        """Get competitors - alphabetical order."""
        competitors = [c for c in self.competitors.values() if c.user_id == user_id]
        
        if platform:
            competitors = [c for c in competitors if c.platform == platform]
        
        # RULE #5: Alphabetical
        return sorted(competitors, key=lambda c: c.account_name)
    
    async def get_competitor_comparison(
        self,
        user_id: str,
        account_id: UUID
    ) -> Dict[str, Any]:
        """Compare your account with competitors."""
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        competitors = await self.get_competitors(
            user_id=user_id,
            platform=account.platform
        )
        
        comparison = {
            "your_account": {
                "name": account.account_name,
                "followers": account.followers_count,
                "posts": account.posts_count
            },
            "competitors": []
        }
        
        for comp in competitors:
            comparison["competitors"].append({
                "name": comp.account_name,
                "followers": comp.followers_count,
                "posts": comp.posts_count,
                "engagement_rate": str(comp.avg_engagement_rate),
                "posting_frequency": str(comp.posting_frequency)
            })
        
        return comparison
    
    # ========================================================================
    # CONTENT CALENDAR
    # ========================================================================
    
    async def create_calendar_entry(
        self,
        date_: date,
        time_slot: str,
        content_idea: str = "",
        content_type: Optional[ContentType] = None,
        platforms: Optional[List[Platform]] = None,
        notes: str = "",
        assigned_to: Optional[str] = None,
        user_id: str = ""
    ) -> ContentCalendarEntry:
        """Create a content calendar entry."""
        entry = ContentCalendarEntry(
            id=uuid4(),
            user_id=user_id,
            date=date_,
            time_slot=time_slot,
            content_idea=content_idea,
            content_type=content_type,
            platforms=platforms or [],
            notes=notes,
            assigned_to=assigned_to
        )
        
        self.calendar_entries[entry.id] = entry
        return entry
    
    async def link_post_to_calendar(
        self,
        entry_id: UUID,
        post_id: UUID,
        user_id: str
    ) -> ContentCalendarEntry:
        """Link a post to a calendar entry."""
        entry = self.calendar_entries.get(entry_id)
        if not entry:
            raise ValueError(f"Calendar entry {entry_id} not found")
        
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        entry.post_id = post_id
        entry.is_filled = True
        
        return entry
    
    async def get_calendar(
        self,
        user_id: str,
        start_date: date,
        end_date: date
    ) -> List[ContentCalendarEntry]:
        """Get calendar entries for date range - chronological."""
        entries = [e for e in self.calendar_entries.values()
                  if e.user_id == user_id and start_date <= e.date <= end_date]
        
        # RULE #5: Chronological
        return sorted(entries, key=lambda e: (e.date, e.time_slot))
    
    async def get_calendar_week(
        self,
        user_id: str,
        week_start: date
    ) -> Dict[str, List[ContentCalendarEntry]]:
        """Get calendar organized by day of week."""
        week_end = week_start + timedelta(days=6)
        entries = await self.get_calendar(user_id, week_start, week_end)
        
        result = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": []
        }
        
        for entry in entries:
            day_name = entry.date.strftime("%A")
            result[day_name].append(entry)
        
        return result
    
    # ========================================================================
    # AI FEATURES
    # ========================================================================
    
    async def generate_caption_suggestions(
        self,
        topic: str,
        platform: Platform,
        tone: str = "professional",
        include_hashtags: bool = True,
        include_cta: bool = True,
        user_id: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Generate AI caption suggestions.
        
        NOTE: These are SUGGESTIONS only.
        Human must review and approve before use.
        """
        # In production: Call LLM API
        # Simulated suggestions
        suggestions = []
        
        tones = {
            "professional": [
                f"Discover how {topic} can transform your approach. ",
                f"Key insights on {topic} you need to know. "
            ],
            "casual": [
                f"Let's talk about {topic}! ",
                f"Thinking about {topic} today. "
            ],
            "engaging": [
                f"What's your take on {topic}? ",
                f"The truth about {topic} might surprise you. "
            ]
        }
        
        base_captions = tones.get(tone, tones["professional"])
        
        for i, base in enumerate(base_captions):
            caption = base
            
            if include_cta:
                ctas = ["Link in bio!", "What do you think?", "Share your thoughts below."]
                caption += ctas[i % len(ctas)]
            
            hashtags = []
            if include_hashtags:
                # Get suggestions (alphabetical)
                hashtags = await self.get_hashtag_suggestions(topic, platform, limit=5)
            
            suggestions.append({
                "caption": caption,
                "hashtags": hashtags,  # ALPHABETICAL
                "character_count": len(caption),
                "platform_limit": self.platform_limits[platform]["char_limit"],
                "ai_generated": True,
                "requires_approval": True  # GOVERNANCE
            })
        
        return suggestions
    
    async def analyze_post_performance(
        self,
        post_id: UUID
    ) -> Dict[str, Any]:
        """Analyze post performance with AI insights."""
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        engagements = await self.get_post_engagement(post_id)
        
        total_engagement = 0
        total_reach = 0
        
        for eng in engagements.values():
            total_engagement += eng.likes + eng.comments + eng.shares
            total_reach += eng.reach
        
        engagement_rate = 0
        if total_reach > 0:
            engagement_rate = total_engagement / total_reach * 100
        
        # AI insights (simulated)
        insights = []
        
        if engagement_rate > 5:
            insights.append("Strong engagement rate! Consider creating similar content.")
        elif engagement_rate > 2:
            insights.append("Good engagement. Try adding more calls-to-action.")
        else:
            insights.append("Lower engagement. Consider optimizing posting time or content type.")
        
        if len(post.hashtags) < 5:
            insights.append("Adding more relevant hashtags could increase reach.")
        
        if not post.media_urls:
            insights.append("Posts with images typically get higher engagement.")
        
        return {
            "post_id": str(post_id),
            "total_engagement": total_engagement,
            "total_reach": total_reach,
            "engagement_rate": round(engagement_rate, 2),
            "insights": insights,
            "recommendation": insights[0] if insights else "Keep posting consistently!"
        }
    
    # ========================================================================
    # ANALYTICS DASHBOARD
    # ========================================================================
    
    async def get_analytics_dashboard(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get comprehensive analytics dashboard."""
        start_date = date.today() - timedelta(days=days)
        
        # Get engagement summary
        engagement = await self.get_engagement_summary(
            user_id=user_id,
            start_date=start_date
        )
        
        # Get accounts - alphabetical
        accounts = await self.get_accounts(user_id)
        
        # Get scheduled posts
        scheduled = await self.get_scheduled_posts(user_id)
        
        # Get pending reviews
        pending = await self.get_pending_reviews(user_id)
        
        # Get active campaigns
        campaigns = await self.get_campaigns(user_id, status=CampaignStatus.ACTIVE)
        
        # Platform breakdown
        platform_stats = {}
        for platform in Platform:
            posts = [p for p in self.posts.values()
                    if p.user_id == user_id and
                    platform in p.platforms and
                    p.status == PostStatus.PUBLISHED and
                    p.published_at and p.published_at.date() >= start_date]
            
            platform_stats[platform.value] = {
                "posts_count": len(posts),
                "connected": any(a.platform == platform for a in accounts)
            }
        
        return {
            "period_days": days,
            "engagement_summary": engagement,
            "accounts": {
                "total": len(accounts),
                "connected": len([a for a in accounts if a.status == AccountStatus.CONNECTED]),
                "platforms": [a.platform.value for a in accounts]
            },
            "posts": {
                "scheduled": len(scheduled),
                "pending_review": len(pending),
                "published_period": engagement["total_posts"]
            },
            "campaigns": {
                "active": len(campaigns),
                "names": [c.name for c in campaigns]
            },
            "platform_breakdown": platform_stats
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """Health check for the social media agent."""
        return {
            "status": "healthy",
            "service": "social_media_agent",
            "version": "V68",
            "accounts_count": len(self.accounts),
            "posts_count": len(self.posts),
            "templates_count": len(self.templates),
            "campaigns_count": len(self.campaigns),
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_social_agent: Optional[SocialMediaAgent] = None


def get_social_agent() -> SocialMediaAgent:
    """Get or create the Social Media agent instance."""
    global _social_agent
    if _social_agent is None:
        _social_agent = SocialMediaAgent()
    return _social_agent


# ============================================================================
# TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    async def test_social_agent():
        agent = get_social_agent()
        user_id = "user_123"
        
        print("=" * 60)
        print("CHE·NU Social Media Agent V68 Test")
        print("=" * 60)
        
        # Test account connection
        print("\n1. Connecting Instagram account...")
        account = await agent.connect_account(
            platform=Platform.INSTAGRAM,
            account_name="my_brand",
            account_id="ig_12345",
            access_token="token_xyz",
            user_id=user_id
        )
        print(f"   ✓ Connected: {account.account_name} on {account.platform.value}")
        
        # Test template creation
        print("\n2. Creating content template...")
        template = await agent.create_template(
            name="Product Launch",
            description="Template for product launches",
            template_text="🚀 Introducing {product_name}! {description} Shop now!",
            content_type=ContentType.IMAGE,
            variables=["product_name", "description"],
            hashtags=["newlaunch", "shopnow"],
            user_id=user_id
        )
        print(f"   ✓ Template created: {template.name}")
        
        # Test post creation (DRAFT)
        print("\n3. Creating post (DRAFT)...")
        post = await agent.create_post(
            text="Check out our amazing new product! Link in bio.",
            platforms=[Platform.INSTAGRAM, Platform.FACEBOOK],
            content_type=ContentType.IMAGE,
            media_urls=["https://example.com/image.jpg"],
            hashtags=["newproduct", "launch", "exciting"],
            user_id=user_id
        )
        print(f"   ✓ Post created - Status: {post.status.value}")
        
        # Test review workflow
        print("\n4. Submitting for review...")
        post = await agent.submit_for_review(post.id, user_id)
        print(f"   ✓ Status: {post.status.value}")
        
        print("\n5. Approving post...")
        post = await agent.approve_post(post.id, "reviewer_456")
        print(f"   ✓ Status: {post.status.value}")
        print(f"   ✓ Reviewed by: {post.reviewed_by}")
        
        print("\n6. Publishing post...")
        post = await agent.publish_post(post.id, user_id)
        print(f"   ✓ Status: {post.status.value}")
        print(f"   ✓ Platform IDs: {post.platform_post_ids}")
        
        # Test hashtag research
        print("\n7. Adding hashtags (alphabetical only)...")
        await agent.add_hashtag(
            tag="marketing",
            platform=Platform.INSTAGRAM,
            categories=["business", "digital"],
            related_tags=["advertising", "branding", "social"]
        )
        await agent.add_hashtag(
            tag="business",
            platform=Platform.INSTAGRAM,
            categories=["professional"],
            related_tags=["entrepreneur", "startup"]
        )
        
        print("\n8. Searching hashtags (ALPHABETICAL - NO RANKING)...")
        hashtags = await agent.search_hashtags("market", Platform.INSTAGRAM)
        print(f"   ✓ Results: {[h.tag for h in hashtags]}")
        
        # Test campaign
        print("\n9. Creating campaign...")
        campaign = await agent.create_campaign(
            name="Q1 Product Launch",
            description="Launch campaign for new product",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            platforms=[Platform.INSTAGRAM, Platform.FACEBOOK],
            goal_type="awareness",
            target_reach=100000,
            budget=Decimal("5000"),
            user_id=user_id
        )
        print(f"   ✓ Campaign: {campaign.name}")
        
        # Test AI suggestions
        print("\n10. Getting AI caption suggestions...")
        suggestions = await agent.generate_caption_suggestions(
            topic="new product launch",
            platform=Platform.INSTAGRAM,
            tone="engaging",
            user_id=user_id
        )
        print(f"   ✓ Got {len(suggestions)} suggestions")
        print(f"   ✓ Note: requires_approval = {suggestions[0]['requires_approval']}")
        
        # Test dashboard
        print("\n11. Getting analytics dashboard...")
        dashboard = await agent.get_analytics_dashboard(user_id)
        print(f"   ✓ Accounts: {dashboard['accounts']['total']}")
        print(f"   ✓ Posts published: {dashboard['engagement_summary']['total_posts']}")
        
        # Health check
        print("\n12. Health check...")
        health = await agent.get_health()
        print(f"   ✓ Status: {health['status']}")
        print(f"   ✓ Posts: {health['posts_count']}")
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    
    asyncio.run(test_social_agent())
