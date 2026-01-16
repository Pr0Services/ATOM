"""
CHE·NU™ V68 - Social Media API Routes
Vertical 10: Social Media Management

60+ endpoints for complete social media management.

GOVERNANCE ENFORCED:
- All publishing requires approval workflow
- Draft → Review → Approve → Publish
- NO ranking algorithms (Rule #5)
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field

from ..agents.social_agent import (
    get_social_agent,
    Platform,
    AccountStatus,
    PostStatus,
    ContentType,
    CampaignStatus
)


router = APIRouter(prefix="/social", tags=["Social Media"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

# Account Models
class ConnectAccountRequest(BaseModel):
    platform: Platform
    account_name: str
    account_id: str
    access_token: str
    refresh_token: str = ""
    token_expires_at: Optional[datetime] = None


class SyncAccountMetricsRequest(BaseModel):
    followers_count: int
    following_count: int
    posts_count: int


# Template Models
class CreateTemplateRequest(BaseModel):
    name: str
    description: str
    template_text: str
    content_type: ContentType
    platform: Optional[Platform] = None
    variables: List[str] = []
    hashtags: List[str] = []


class ApplyTemplateRequest(BaseModel):
    variables: Dict[str, str]


# Post Models
class CreatePostRequest(BaseModel):
    text: str
    platforms: List[Platform]
    content_type: ContentType = ContentType.TEXT
    media_urls: List[str] = []
    hashtags: List[str] = []
    mentions: List[str] = []
    link: str = ""
    scheduled_time: Optional[datetime] = None
    timezone: str = "America/Montreal"
    campaign_id: Optional[UUID] = None
    template_id: Optional[UUID] = None


class RejectPostRequest(BaseModel):
    reason: str


# Engagement Models
class RecordEngagementRequest(BaseModel):
    platform: Platform
    platform_post_id: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    clicks: int = 0
    views: int = 0
    impressions: int = 0
    reach: int = 0


# Hashtag Models
class AddHashtagRequest(BaseModel):
    tag: str
    platform: Platform
    categories: List[str] = []
    related_tags: List[str] = []


# Audience Models
class RecordAudienceInsightRequest(BaseModel):
    platform: Platform
    age_ranges: Dict[str, int] = {}
    gender_distribution: Dict[str, int] = {}
    top_locations: Dict[str, int] = {}
    top_languages: Dict[str, int] = {}
    most_active_hours: Dict[int, int] = {}
    most_active_days: Dict[str, int] = {}
    followers_gained: int = 0
    followers_lost: int = 0


# Campaign Models
class CreateCampaignRequest(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    platforms: List[Platform]
    goal_type: str = "awareness"
    target_reach: int = 0
    target_engagement: int = 0
    target_clicks: int = 0
    budget: float = 0
    hashtags: List[str] = []


# Competitor Models
class AddCompetitorRequest(BaseModel):
    platform: Platform
    account_name: str
    account_url: str


class UpdateCompetitorMetricsRequest(BaseModel):
    followers_count: int
    posts_count: int
    avg_engagement_rate: float


# Calendar Models
class CreateCalendarEntryRequest(BaseModel):
    date: date
    time_slot: str
    content_idea: str = ""
    content_type: Optional[ContentType] = None
    platforms: List[Platform] = []
    notes: str = ""
    assigned_to: Optional[str] = None


class LinkPostToCalendarRequest(BaseModel):
    post_id: UUID


# AI Models
class GenerateCaptionRequest(BaseModel):
    topic: str
    platform: Platform
    tone: str = "professional"
    include_hashtags: bool = True
    include_cta: bool = True


# ============================================================================
# ACCOUNT ENDPOINTS
# ============================================================================

@router.post("/accounts")
async def connect_account(
    request: ConnectAccountRequest,
    user_id: str = Query(..., description="User ID")
):
    """Connect a social media account."""
    agent = get_social_agent()
    account = await agent.connect_account(
        platform=request.platform,
        account_name=request.account_name,
        account_id=request.account_id,
        access_token=request.access_token,
        refresh_token=request.refresh_token,
        token_expires_at=request.token_expires_at,
        user_id=user_id
    )
    return {
        "id": str(account.id),
        "platform": account.platform.value,
        "account_name": account.account_name,
        "status": account.status.value,
        "connected_at": account.connected_at.isoformat()
    }


@router.get("/accounts")
async def get_accounts(user_id: str = Query(...)):
    """Get all connected accounts - alphabetical by platform."""
    agent = get_social_agent()
    accounts = await agent.get_accounts(user_id)
    return {
        "accounts": [
            {
                "id": str(a.id),
                "platform": a.platform.value,
                "account_name": a.account_name,
                "status": a.status.value,
                "followers_count": a.followers_count,
                "following_count": a.following_count,
                "posts_count": a.posts_count,
                "last_synced": a.last_synced.isoformat() if a.last_synced else None
            }
            for a in accounts
        ],
        "total": len(accounts)
    }


@router.delete("/accounts/{account_id}")
async def disconnect_account(
    account_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Disconnect a social media account."""
    agent = get_social_agent()
    try:
        account = await agent.disconnect_account(account_id, user_id)
        return {
            "id": str(account.id),
            "status": account.status.value,
            "message": "Account disconnected successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/accounts/{account_id}/sync")
async def sync_account_metrics(
    request: SyncAccountMetricsRequest,
    account_id: UUID = Path(...)
):
    """Sync account metrics from platform."""
    agent = get_social_agent()
    try:
        account = await agent.sync_account_metrics(
            account_id=account_id,
            followers_count=request.followers_count,
            following_count=request.following_count,
            posts_count=request.posts_count
        )
        return {
            "id": str(account.id),
            "followers_count": account.followers_count,
            "following_count": account.following_count,
            "posts_count": account.posts_count,
            "last_synced": account.last_synced.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# TEMPLATE ENDPOINTS
# ============================================================================

@router.post("/templates")
async def create_template(
    request: CreateTemplateRequest,
    user_id: str = Query(...)
):
    """Create a content template."""
    agent = get_social_agent()
    template = await agent.create_template(
        name=request.name,
        description=request.description,
        template_text=request.template_text,
        content_type=request.content_type,
        platform=request.platform,
        variables=request.variables,
        hashtags=request.hashtags,
        user_id=user_id
    )
    return {
        "id": str(template.id),
        "name": template.name,
        "content_type": template.content_type.value,
        "variables": template.variables,
        "created_at": template.created_at.isoformat()
    }


@router.get("/templates")
async def get_templates(
    user_id: str = Query(...),
    platform: Optional[Platform] = None,
    content_type: Optional[ContentType] = None
):
    """Get templates - alphabetical order."""
    agent = get_social_agent()
    templates = await agent.get_templates(
        user_id=user_id,
        platform=platform,
        content_type=content_type
    )
    return {
        "templates": [
            {
                "id": str(t.id),
                "name": t.name,
                "description": t.description,
                "content_type": t.content_type.value,
                "platform": t.platform.value if t.platform else None,
                "variables": t.variables,
                "usage_count": t.usage_count
            }
            for t in templates
        ],
        "total": len(templates)
    }


@router.post("/templates/{template_id}/apply")
async def apply_template(
    request: ApplyTemplateRequest,
    template_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Apply variables to a template."""
    agent = get_social_agent()
    try:
        text = await agent.apply_template(
            template_id=template_id,
            variables=request.variables,
            user_id=user_id
        )
        return {
            "template_id": str(template_id),
            "result": text
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# POST ENDPOINTS - GOVERNANCE ENFORCED
# ============================================================================

@router.post("/posts")
async def create_post(
    request: CreatePostRequest,
    user_id: str = Query(...)
):
    """
    Create a post DRAFT.
    
    GOVERNANCE: Post starts in DRAFT status.
    Must go through review workflow before publishing.
    """
    agent = get_social_agent()
    try:
        post = await agent.create_post(
            text=request.text,
            platforms=request.platforms,
            content_type=request.content_type,
            media_urls=request.media_urls,
            hashtags=request.hashtags,
            mentions=request.mentions,
            link=request.link,
            scheduled_time=request.scheduled_time,
            timezone=request.timezone,
            campaign_id=request.campaign_id,
            template_id=request.template_id,
            user_id=user_id
        )
        return {
            "id": str(post.id),
            "status": post.status.value,
            "text": post.text,
            "platforms": [p.value for p in post.platforms],
            "scheduled_time": post.scheduled_time.isoformat() if post.scheduled_time else None,
            "message": "Post created as DRAFT. Submit for review before publishing.",
            "next_step": "POST /posts/{id}/submit-review"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/posts")
async def get_posts(
    user_id: str = Query(...),
    status: Optional[PostStatus] = None,
    platform: Optional[Platform] = None,
    campaign_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get posts - chronological order (NO ranking)."""
    agent = get_social_agent()
    posts = await agent.get_posts(
        user_id=user_id,
        status=status,
        platform=platform,
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date
    )
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text[:100] + "..." if len(p.text) > 100 else p.text,
                "platforms": [pl.value for pl in p.platforms],
                "content_type": p.content_type.value,
                "status": p.status.value,
                "scheduled_time": p.scheduled_time.isoformat() if p.scheduled_time else None,
                "published_at": p.published_at.isoformat() if p.published_at else None,
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ],
        "total": len(posts),
        "sort_order": "chronological"  # RULE #5
    }


# NOTE: These specific routes MUST come BEFORE /posts/{post_id}
@router.get("/posts/pending-review")
async def get_pending_reviews(user_id: str = Query(...)):
    """Get posts awaiting review - chronological order."""
    agent = get_social_agent()
    posts = await agent.get_pending_reviews(user_id)
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text[:100] + "..." if len(p.text) > 100 else p.text,
                "platforms": [pl.value for pl in p.platforms],
                "submitted_at": p.submitted_for_review.isoformat() if p.submitted_for_review else None,
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ],
        "total": len(posts),
        "sort_order": "chronological_oldest_first"
    }


@router.get("/posts/scheduled")
async def get_scheduled_posts_early(user_id: str = Query(...)):
    """Get scheduled posts - chronological by scheduled time."""
    agent = get_social_agent()
    posts = await agent.get_scheduled_posts(user_id)
    return {
        "posts": [
            {
                "id": str(p.id),
                "text": p.text[:100] + "..." if len(p.text) > 100 else p.text,
                "platforms": [pl.value for pl in p.platforms],
                "scheduled_time": p.scheduled_time.isoformat() if p.scheduled_time else None
            }
            for p in posts
        ],
        "total": len(posts)
    }


@router.get("/posts/{post_id}")
async def get_post(post_id: UUID = Path(...)):
    """Get post details."""
    agent = get_social_agent()
    post = agent.posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "id": str(post.id),
        "text": post.text,
        "platforms": [p.value for p in post.platforms],
        "content_type": post.content_type.value,
        "media_urls": post.media_urls,
        "hashtags": post.hashtags,
        "mentions": post.mentions,
        "link": post.link,
        "status": post.status.value,
        "scheduled_time": post.scheduled_time.isoformat() if post.scheduled_time else None,
        "submitted_for_review": post.submitted_for_review.isoformat() if post.submitted_for_review else None,
        "reviewed_by": post.reviewed_by,
        "reviewed_at": post.reviewed_at.isoformat() if post.reviewed_at else None,
        "rejection_reason": post.rejection_reason,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "platform_post_ids": {k.value: v for k, v in post.platform_post_ids.items()},
        "created_at": post.created_at.isoformat()
    }


@router.post("/posts/{post_id}/submit-review")
async def submit_for_review(
    post_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """
    Submit post for review.
    
    GOVERNANCE: Changes status from DRAFT to PENDING_REVIEW.
    """
    agent = get_social_agent()
    try:
        post = await agent.submit_for_review(post_id, user_id)
        return {
            "id": str(post.id),
            "status": post.status.value,
            "submitted_at": post.submitted_for_review.isoformat(),
            "message": "Post submitted for review",
            "next_step": "POST /posts/{id}/approve or POST /posts/{id}/reject"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/posts/{post_id}/approve")
async def approve_post(
    post_id: UUID = Path(...),
    reviewer_id: str = Query(...)
):
    """
    Approve post for publishing.
    
    GOVERNANCE: Human must explicitly approve before publishing.
    """
    agent = get_social_agent()
    try:
        post = await agent.approve_post(post_id, reviewer_id)
        return {
            "id": str(post.id),
            "status": post.status.value,
            "reviewed_by": post.reviewed_by,
            "reviewed_at": post.reviewed_at.isoformat(),
            "message": "Post approved",
            "next_step": "POST /posts/{id}/publish"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/posts/{post_id}/reject")
async def reject_post(
    request: RejectPostRequest,
    post_id: UUID = Path(...),
    reviewer_id: str = Query(...)
):
    """
    Reject post with feedback.
    
    GOVERNANCE: Reviewer provides reason for rejection.
    """
    agent = get_social_agent()
    try:
        post = await agent.reject_post(post_id, reviewer_id, request.reason)
        return {
            "id": str(post.id),
            "status": post.status.value,
            "rejection_reason": post.rejection_reason,
            "message": "Post rejected",
            "next_step": "POST /posts/{id}/revert-to-draft to edit and resubmit"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/posts/{post_id}/publish")
async def publish_post(
    post_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """
    Publish an approved post.
    
    GOVERNANCE: Only APPROVED posts can be published.
    """
    agent = get_social_agent()
    try:
        post = await agent.publish_post(post_id, user_id)
        return {
            "id": str(post.id),
            "status": post.status.value,
            "published_at": post.published_at.isoformat() if post.published_at else None,
            "platform_post_ids": {k.value: v for k, v in post.platform_post_ids.items()},
            "errors": {k.value: v for k, v in post.publish_errors.items()} if post.publish_errors else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/posts/{post_id}/revert-to-draft")
async def revert_to_draft(
    post_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Revert a rejected post to draft for editing."""
    agent = get_social_agent()
    try:
        post = await agent.revert_to_draft(post_id, user_id)
        return {
            "id": str(post.id),
            "status": post.status.value,
            "message": "Post reverted to draft for editing"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# ============================================================================
# ENGAGEMENT ENDPOINTS
# ============================================================================

@router.post("/posts/{post_id}/engagement")
async def record_engagement(
    request: RecordEngagementRequest,
    post_id: UUID = Path(...)
):
    """Record engagement metrics for a post."""
    agent = get_social_agent()
    engagement = await agent.record_engagement(
        post_id=post_id,
        platform=request.platform,
        platform_post_id=request.platform_post_id,
        likes=request.likes,
        comments=request.comments,
        shares=request.shares,
        saves=request.saves,
        clicks=request.clicks,
        views=request.views,
        impressions=request.impressions,
        reach=request.reach
    )
    return {
        "id": str(engagement.id),
        "post_id": str(engagement.post_id),
        "platform": engagement.platform.value,
        "engagement_rate": str(engagement.engagement_rate),
        "recorded_at": engagement.recorded_at.isoformat()
    }


@router.get("/posts/{post_id}/engagement")
async def get_post_engagement(post_id: UUID = Path(...)):
    """Get engagement for a post across platforms."""
    agent = get_social_agent()
    engagements = await agent.get_post_engagement(post_id)
    return {
        "post_id": str(post_id),
        "platforms": {
            platform.value: {
                "likes": eng.likes,
                "comments": eng.comments,
                "shares": eng.shares,
                "saves": eng.saves,
                "clicks": eng.clicks,
                "views": eng.views,
                "impressions": eng.impressions,
                "reach": eng.reach,
                "engagement_rate": str(eng.engagement_rate)
            }
            for platform, eng in engagements.items()
        }
    }


@router.get("/engagement/summary")
async def get_engagement_summary(
    user_id: str = Query(...),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get engagement summary across all posts."""
    agent = get_social_agent()
    summary = await agent.get_engagement_summary(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    return summary


# ============================================================================
# HASHTAG ENDPOINTS - ALPHABETICAL ONLY (Rule #5)
# ============================================================================

@router.post("/hashtags")
async def add_hashtag(request: AddHashtagRequest):
    """Add hashtag to research database."""
    agent = get_social_agent()
    hashtag = await agent.add_hashtag(
        tag=request.tag,
        platform=request.platform,
        categories=request.categories,
        related_tags=request.related_tags
    )
    return {
        "id": str(hashtag.id),
        "tag": hashtag.tag,
        "platform": hashtag.platform.value,
        "categories": hashtag.categories,  # ALPHABETICAL
        "related_tags": hashtag.related_tags  # ALPHABETICAL
    }


@router.get("/hashtags/search")
async def search_hashtags(
    query: str = Query(...),
    platform: Optional[Platform] = None,
    category: Optional[str] = None
):
    """
    Search hashtags - ALPHABETICAL results.
    
    RULE #5: NO ranking by popularity or engagement.
    """
    agent = get_social_agent()
    hashtags = await agent.search_hashtags(
        query=query,
        platform=platform,
        category=category
    )
    return {
        "hashtags": [
            {
                "tag": h.tag,
                "platform": h.platform.value,
                "categories": h.categories
            }
            for h in hashtags
        ],
        "total": len(hashtags),
        "sort_order": "alphabetical"  # RULE #5
    }


@router.get("/hashtags/suggestions")
async def get_hashtag_suggestions(
    content: str = Query(...),
    platform: Platform = Query(...),
    limit: int = Query(10, le=30)
):
    """
    Get hashtag suggestions - ALPHABETICAL.
    
    RULE #5: NO ranking by popularity.
    """
    agent = get_social_agent()
    suggestions = await agent.get_hashtag_suggestions(
        content=content,
        platform=platform,
        limit=limit
    )
    return {
        "suggestions": suggestions,
        "total": len(suggestions),
        "sort_order": "alphabetical"  # RULE #5
    }


# ============================================================================
# AUDIENCE INSIGHTS ENDPOINTS
# ============================================================================

@router.post("/accounts/{account_id}/audience")
async def record_audience_insight(
    request: RecordAudienceInsightRequest,
    account_id: UUID = Path(...)
):
    """Record audience insights for an account."""
    agent = get_social_agent()
    insight = await agent.record_audience_insight(
        account_id=account_id,
        platform=request.platform,
        age_ranges=request.age_ranges,
        gender_distribution=request.gender_distribution,
        top_locations=request.top_locations,
        top_languages=request.top_languages,
        most_active_hours=request.most_active_hours,
        most_active_days=request.most_active_days,
        followers_gained=request.followers_gained,
        followers_lost=request.followers_lost
    )
    return {
        "id": str(insight.id),
        "recorded_date": insight.recorded_date.isoformat(),
        "net_growth": insight.net_growth,
        "growth_rate": str(insight.growth_rate)
    }


@router.get("/accounts/{account_id}/audience")
async def get_audience_insights(
    account_id: UUID = Path(...),
    days: int = Query(30, le=365)
):
    """Get audience insights - chronological order."""
    agent = get_social_agent()
    insights = await agent.get_audience_insights(account_id, days)
    return {
        "account_id": str(account_id),
        "insights": [
            {
                "date": i.recorded_date.isoformat(),
                "age_ranges": i.age_ranges,
                "gender_distribution": i.gender_distribution,
                "top_locations": i.top_locations,
                "net_growth": i.net_growth,
                "growth_rate": str(i.growth_rate)
            }
            for i in insights
        ],
        "total": len(insights)
    }


@router.get("/accounts/{account_id}/best-times")
async def get_best_posting_times(account_id: UUID = Path(...)):
    """
    Get best times to post based on audience activity.
    
    NOTE: Sorted by day/hour, NOT by engagement score.
    """
    agent = get_social_agent()
    slots = await agent.get_best_posting_times(account_id)
    return {
        "account_id": str(account_id),
        "time_slots": [
            {
                "day": s.day_of_week,
                "hour": s.hour,
                "engagement_score": str(s.engagement_score),
                "audience_active_percent": str(s.audience_active_percent)
            }
            for s in slots
        ],
        "sort_order": "chronological_by_day_hour"
    }


# ============================================================================
# CAMPAIGN ENDPOINTS
# ============================================================================

@router.post("/campaigns")
async def create_campaign(
    request: CreateCampaignRequest,
    user_id: str = Query(...)
):
    """Create a social media campaign."""
    agent = get_social_agent()
    campaign = await agent.create_campaign(
        name=request.name,
        description=request.description,
        start_date=request.start_date,
        end_date=request.end_date,
        platforms=request.platforms,
        goal_type=request.goal_type,
        target_reach=request.target_reach,
        target_engagement=request.target_engagement,
        target_clicks=request.target_clicks,
        budget=Decimal(str(request.budget)),
        hashtags=request.hashtags,
        user_id=user_id
    )
    return {
        "id": str(campaign.id),
        "name": campaign.name,
        "status": campaign.status.value,
        "start_date": campaign.start_date.isoformat(),
        "end_date": campaign.end_date.isoformat(),
        "created_at": campaign.created_at.isoformat()
    }


@router.get("/campaigns")
async def get_campaigns(
    user_id: str = Query(...),
    status: Optional[CampaignStatus] = None
):
    """Get campaigns - chronological order."""
    agent = get_social_agent()
    campaigns = await agent.get_campaigns(user_id, status)
    return {
        "campaigns": [
            {
                "id": str(c.id),
                "name": c.name,
                "status": c.status.value,
                "start_date": c.start_date.isoformat(),
                "end_date": c.end_date.isoformat(),
                "platforms": [p.value for p in c.platforms],
                "budget": float(c.budget),
                "spent": float(c.spent)
            }
            for c in campaigns
        ],
        "total": len(campaigns)
    }


@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: UUID = Path(...)):
    """Get campaign details."""
    agent = get_social_agent()
    campaign = agent.campaigns.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "id": str(campaign.id),
        "name": campaign.name,
        "description": campaign.description,
        "status": campaign.status.value,
        "start_date": campaign.start_date.isoformat(),
        "end_date": campaign.end_date.isoformat(),
        "platforms": [p.value for p in campaign.platforms],
        "hashtags": campaign.hashtags,
        "goal_type": campaign.goal_type,
        "target_reach": campaign.target_reach,
        "target_engagement": campaign.target_engagement,
        "target_clicks": campaign.target_clicks,
        "budget": float(campaign.budget),
        "spent": float(campaign.spent),
        "total_posts": campaign.total_posts,
        "total_reach": campaign.total_reach,
        "total_engagement": campaign.total_engagement,
        "total_clicks": campaign.total_clicks
    }


@router.post("/campaigns/{campaign_id}/start")
async def start_campaign(
    campaign_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Start a campaign."""
    agent = get_social_agent()
    try:
        campaign = await agent.start_campaign(campaign_id, user_id)
        return {
            "id": str(campaign.id),
            "status": campaign.status.value,
            "message": "Campaign started"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/campaigns/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Pause a campaign."""
    agent = get_social_agent()
    try:
        campaign = await agent.pause_campaign(campaign_id, user_id)
        return {
            "id": str(campaign.id),
            "status": campaign.status.value,
            "message": "Campaign paused"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/campaigns/{campaign_id}/complete")
async def complete_campaign(
    campaign_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Complete a campaign and calculate results."""
    agent = get_social_agent()
    try:
        campaign = await agent.complete_campaign(campaign_id, user_id)
        return {
            "id": str(campaign.id),
            "status": campaign.status.value,
            "total_posts": campaign.total_posts,
            "total_reach": campaign.total_reach,
            "total_engagement": campaign.total_engagement,
            "total_clicks": campaign.total_clicks,
            "message": "Campaign completed"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/campaigns/{campaign_id}/performance")
async def get_campaign_performance(campaign_id: UUID = Path(...)):
    """Get campaign performance metrics."""
    agent = get_social_agent()
    try:
        performance = await agent.get_campaign_performance(campaign_id)
        return performance
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# COMPETITOR ENDPOINTS
# ============================================================================

@router.post("/competitors")
async def add_competitor(
    request: AddCompetitorRequest,
    user_id: str = Query(...)
):
    """Add a competitor to monitor."""
    agent = get_social_agent()
    try:
        competitor = await agent.add_competitor(
            platform=request.platform,
            account_name=request.account_name,
            account_url=request.account_url,
            user_id=user_id
        )
        return {
            "id": str(competitor.id),
            "platform": competitor.platform.value,
            "account_name": competitor.account_name,
            "created_at": competitor.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/competitors")
async def get_competitors(
    user_id: str = Query(...),
    platform: Optional[Platform] = None
):
    """Get competitors - alphabetical order."""
    agent = get_social_agent()
    competitors = await agent.get_competitors(user_id, platform)
    return {
        "competitors": [
            {
                "id": str(c.id),
                "platform": c.platform.value,
                "account_name": c.account_name,
                "account_url": c.account_url,
                "followers_count": c.followers_count,
                "avg_engagement_rate": str(c.avg_engagement_rate),
                "posting_frequency": str(c.posting_frequency),
                "last_checked": c.last_checked.isoformat() if c.last_checked else None
            }
            for c in competitors
        ],
        "total": len(competitors),
        "sort_order": "alphabetical"
    }


@router.post("/competitors/{competitor_id}/metrics")
async def update_competitor_metrics(
    request: UpdateCompetitorMetricsRequest,
    competitor_id: UUID = Path(...)
):
    """Update competitor metrics."""
    agent = get_social_agent()
    try:
        competitor = await agent.update_competitor_metrics(
            competitor_id=competitor_id,
            followers_count=request.followers_count,
            posts_count=request.posts_count,
            avg_engagement_rate=Decimal(str(request.avg_engagement_rate))
        )
        return {
            "id": str(competitor.id),
            "followers_count": competitor.followers_count,
            "posts_count": competitor.posts_count,
            "avg_engagement_rate": str(competitor.avg_engagement_rate),
            "posting_frequency": str(competitor.posting_frequency),
            "last_checked": competitor.last_checked.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/competitors/comparison")
async def get_competitor_comparison(
    user_id: str = Query(...),
    account_id: UUID = Query(...)
):
    """Compare your account with competitors."""
    agent = get_social_agent()
    try:
        comparison = await agent.get_competitor_comparison(user_id, account_id)
        return comparison
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# CALENDAR ENDPOINTS
# ============================================================================

@router.post("/calendar")
async def create_calendar_entry(
    request: CreateCalendarEntryRequest,
    user_id: str = Query(...)
):
    """Create a content calendar entry."""
    agent = get_social_agent()
    entry = await agent.create_calendar_entry(
        date_=request.date,
        time_slot=request.time_slot,
        content_idea=request.content_idea,
        content_type=request.content_type,
        platforms=request.platforms,
        notes=request.notes,
        assigned_to=request.assigned_to,
        user_id=user_id
    )
    return {
        "id": str(entry.id),
        "date": entry.date.isoformat(),
        "time_slot": entry.time_slot,
        "is_filled": entry.is_filled,
        "created_at": entry.created_at.isoformat()
    }


@router.post("/calendar/{entry_id}/link-post")
async def link_post_to_calendar(
    request: LinkPostToCalendarRequest,
    entry_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Link a post to a calendar entry."""
    agent = get_social_agent()
    try:
        entry = await agent.link_post_to_calendar(
            entry_id=entry_id,
            post_id=request.post_id,
            user_id=user_id
        )
        return {
            "id": str(entry.id),
            "post_id": str(entry.post_id),
            "is_filled": entry.is_filled,
            "message": "Post linked to calendar"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/calendar")
async def get_calendar(
    user_id: str = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...)
):
    """Get calendar entries - chronological order."""
    agent = get_social_agent()
    entries = await agent.get_calendar(user_id, start_date, end_date)
    return {
        "entries": [
            {
                "id": str(e.id),
                "date": e.date.isoformat(),
                "time_slot": e.time_slot,
                "content_idea": e.content_idea,
                "content_type": e.content_type.value if e.content_type else None,
                "platforms": [p.value for p in e.platforms],
                "is_filled": e.is_filled,
                "post_id": str(e.post_id) if e.post_id else None
            }
            for e in entries
        ],
        "total": len(entries)
    }


@router.get("/calendar/week")
async def get_calendar_week(
    user_id: str = Query(...),
    week_start: date = Query(...)
):
    """Get calendar organized by day of week."""
    agent = get_social_agent()
    calendar = await agent.get_calendar_week(user_id, week_start)
    return {
        "week_start": week_start.isoformat(),
        "days": {
            day: [
                {
                    "id": str(e.id),
                    "time_slot": e.time_slot,
                    "content_idea": e.content_idea,
                    "is_filled": e.is_filled
                }
                for e in entries
            ]
            for day, entries in calendar.items()
        }
    }


# ============================================================================
# AI ENDPOINTS
# ============================================================================

@router.post("/ai/caption-suggestions")
async def generate_caption_suggestions(
    request: GenerateCaptionRequest,
    user_id: str = Query(...)
):
    """
    Generate AI caption suggestions.
    
    GOVERNANCE: All suggestions require human approval before use.
    """
    agent = get_social_agent()
    suggestions = await agent.generate_caption_suggestions(
        topic=request.topic,
        platform=request.platform,
        tone=request.tone,
        include_hashtags=request.include_hashtags,
        include_cta=request.include_cta,
        user_id=user_id
    )
    return {
        "suggestions": suggestions,
        "total": len(suggestions),
        "notice": "These are AI suggestions. Human approval required before publishing."
    }


@router.get("/ai/post-analysis/{post_id}")
async def analyze_post_performance(post_id: UUID = Path(...)):
    """Analyze post performance with AI insights."""
    agent = get_social_agent()
    try:
        analysis = await agent.analyze_post_performance(post_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    user_id: str = Query(...),
    days: int = Query(30, le=365)
):
    """Get comprehensive analytics dashboard."""
    agent = get_social_agent()
    dashboard = await agent.get_analytics_dashboard(user_id, days)
    return dashboard


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check for the social media service."""
    agent = get_social_agent()
    return await agent.get_health()
