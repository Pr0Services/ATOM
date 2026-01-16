"""
CHE·NU™ V68 — Community & Social Platforms API Routes
Discord/Slack/Circle Killer: $9-99/mo → $29/mo with GOVERNANCE

GOVERNANCE COMPLIANCE:
- Rule #1: Moderation actions require HUMAN approval
- Rule #5: ALPHABETICAL/CHRONOLOGICAL listings (NOT by engagement)
- Rule #6: Full audit trail
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.spheres.community.agents.community_agent import (
    CommunityAgent, CommunityType, ChannelType, MemberRole,
    PostType, ModerationAction, ModerationStatus
)

router = APIRouter(prefix="/api/v2/community", tags=["Community & Social"])

agent = CommunityAgent()

# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class CommunityCreateRequest(BaseModel):
    name: str
    description: str
    community_type: str = "public"
    owner_id: str
    created_by: str

class ChannelCreateRequest(BaseModel):
    name: str
    description: str
    channel_type: str = "text"
    is_private: bool = False
    created_by: str

class MemberAddRequest(BaseModel):
    user_id: str
    display_name: str
    invited_by: str
    role: str = "member"

class PostCreateRequest(BaseModel):
    channel_id: str
    author_id: str
    author_name: str
    content: str
    post_type: str = "text"

class EventCreateRequest(BaseModel):
    title: str
    description: str
    event_type: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_virtual: bool = True
    max_attendees: Optional[int] = None
    created_by: str

class PollCreateRequest(BaseModel):
    channel_id: str
    question: str
    options: List[str]
    duration_hours: Optional[int] = None
    created_by: str

class ModerationRequest(BaseModel):
    target_user_id: str
    target_user_name: str
    action: str
    reason: str
    evidence: List[str] = []
    requested_by: str

class DMRequest(BaseModel):
    recipient_id: str
    content: str

# ═══════════════════════════════════════════════════════════════════════════════
# COMMUNITY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities", status_code=201)
async def create_community(request: CommunityCreateRequest):
    """Create a new community."""
    community = agent.create_community(
        name=request.name,
        description=request.description,
        community_type=CommunityType(request.community_type),
        owner_id=request.owner_id,
        created_by=request.created_by
    )
    return {"id": str(community.id), "name": community.name, "member_count": community.member_count}

@router.get("/communities")
async def list_communities(
    owner_id: Optional[str] = None,
    community_type: Optional[str] = None
):
    """
    List communities - ALPHABETICAL by name (Rule #5).
    NOT sorted by member count or activity.
    """
    ct = CommunityType(community_type) if community_type else None
    communities = agent.list_communities(owner_id=owner_id, community_type=ct)
    return [{"id": str(c.id), "name": c.name, "type": c.community_type.value, "members": c.member_count} for c in communities]

@router.get("/communities/{community_id}")
async def get_community(community_id: str):
    """Get community details."""
    community = agent.get_community(UUID(community_id))
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return {
        "id": str(community.id),
        "name": community.name,
        "description": community.description,
        "type": community.community_type.value,
        "status": community.status.value,
        "member_count": community.member_count,
        "owner_id": community.owner_id
    }

# ═══════════════════════════════════════════════════════════════════════════════
# CHANNEL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/channels", status_code=201)
async def create_channel(community_id: str, request: ChannelCreateRequest):
    """Create a new channel."""
    channel = agent.create_channel(
        community_id=UUID(community_id),
        name=request.name,
        description=request.description,
        channel_type=ChannelType(request.channel_type),
        is_private=request.is_private,
        created_by=request.created_by
    )
    return {"id": str(channel.id), "name": channel.name}

@router.get("/communities/{community_id}/channels")
async def list_channels(community_id: str, channel_type: Optional[str] = None):
    """
    List channels - ALPHABETICAL by name (Rule #5).
    NOT sorted by activity or message count.
    """
    ct = ChannelType(channel_type) if channel_type else None
    channels = agent.list_channels(UUID(community_id), channel_type=ct)
    return [{"id": str(c.id), "name": c.name, "type": c.channel_type.value} for c in channels]

# ═══════════════════════════════════════════════════════════════════════════════
# MEMBER ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/members", status_code=201)
async def add_member(community_id: str, request: MemberAddRequest):
    """Add a member to community."""
    member = agent.add_member(
        community_id=UUID(community_id),
        user_id=request.user_id,
        display_name=request.display_name,
        invited_by=request.invited_by,
        role=MemberRole(request.role)
    )
    return {"id": str(member.id), "display_name": member.display_name, "role": member.role.value}

@router.get("/communities/{community_id}/members")
async def list_members(community_id: str, role: Optional[str] = None):
    """
    List members - ALPHABETICAL by display_name (Rule #5).
    NOT sorted by join date or engagement.
    """
    r = MemberRole(role) if role else None
    members = agent.list_members(UUID(community_id), role=r)
    return [{"id": str(m.id), "display_name": m.display_name, "role": m.role.value, "status": m.status.value} for m in members]

@router.put("/communities/{community_id}/members/{member_id}/role")
async def update_member_role(community_id: str, member_id: str, role: str, updated_by: str):
    """Update member role."""
    member = agent.update_member_role(UUID(member_id), MemberRole(role), updated_by)
    return {"id": str(member.id), "role": member.role.value}

# ═══════════════════════════════════════════════════════════════════════════════
# POST ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/posts", status_code=201)
async def create_post(community_id: str, request: PostCreateRequest):
    """Create a post."""
    post = agent.create_post(
        community_id=UUID(community_id),
        channel_id=UUID(request.channel_id),
        author_id=request.author_id,
        author_name=request.author_name,
        content=request.content,
        post_type=PostType(request.post_type)
    )
    return {"id": str(post.id), "post_number": post.post_number}

@router.get("/channels/{channel_id}/posts")
async def list_posts(channel_id: str, limit: int = 50):
    """
    List posts - CHRONOLOGICAL by created_at (Rule #5).
    NOT sorted by likes or engagement.
    """
    posts = agent.list_posts(UUID(channel_id), limit=limit)
    return [{"id": str(p.id), "post_number": p.post_number, "author": p.author_name, "content": p.content[:100]} for p in posts]

# ═══════════════════════════════════════════════════════════════════════════════
# EVENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/events", status_code=201)
async def create_event(community_id: str, request: EventCreateRequest):
    """Create an event."""
    event = agent.create_event(
        community_id=UUID(community_id),
        title=request.title,
        description=request.description,
        event_type=request.event_type,
        start_time=request.start_time,
        end_time=request.end_time,
        location=request.location,
        is_virtual=request.is_virtual,
        max_attendees=request.max_attendees,
        created_by=request.created_by
    )
    return {"id": str(event.id), "event_number": event.event_number, "title": event.title}

@router.get("/communities/{community_id}/events")
async def list_events(community_id: str):
    """
    List events - CHRONOLOGICAL by start_time (Rule #5).
    Upcoming events first.
    """
    events = agent.list_events(UUID(community_id))
    return [{"id": str(e.id), "event_number": e.event_number, "title": e.title, "start": e.start_time.isoformat()} for e in events]

@router.post("/events/{event_id}/rsvp")
async def rsvp_event(event_id: str, user_id: str):
    """RSVP to an event."""
    event = agent.rsvp_event(UUID(event_id), user_id)
    return {"status": "rsvped", "attendees": len(event.attendee_ids)}

# ═══════════════════════════════════════════════════════════════════════════════
# POLL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/polls", status_code=201)
async def create_poll(community_id: str, request: PollCreateRequest):
    """Create a poll."""
    poll = agent.create_poll(
        community_id=UUID(community_id),
        channel_id=UUID(request.channel_id),
        question=request.question,
        options=request.options,
        duration_hours=request.duration_hours,
        created_by=request.created_by
    )
    return {"id": str(poll.id), "poll_number": poll.poll_number}

@router.post("/polls/{poll_id}/vote")
async def vote_poll(poll_id: str, option: str, voter_id: str):
    """Vote in a poll."""
    poll = agent.vote_poll(UUID(poll_id), option, voter_id)
    return {"status": "voted"}

@router.get("/polls/{poll_id}/results")
async def get_poll_results(poll_id: str):
    """
    Get poll results - ORIGINAL option order (Rule #5).
    NOT sorted by vote count.
    """
    results = agent.get_poll_results(UUID(poll_id))
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# MODERATION ENDPOINTS (GOVERNANCE - Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/communities/{community_id}/moderation", status_code=201)
async def request_moderation(community_id: str, request: ModerationRequest):
    """
    Request moderation action - REQUIRES APPROVAL (Rule #1).
    Actions cannot be executed without human approval.
    """
    case = agent.request_moderation_action(
        community_id=UUID(community_id),
        target_user_id=request.target_user_id,
        target_user_name=request.target_user_name,
        action=ModerationAction(request.action),
        reason=request.reason,
        evidence=request.evidence,
        requested_by=request.requested_by
    )
    return {
        "id": str(case.id),
        "case_number": case.case_number,
        "status": case.status.value,
        "governance": "Rule #1 - Requires human approval before execution"
    }

@router.get("/communities/{community_id}/moderation")
async def list_moderation_cases(community_id: str, status: Optional[str] = None):
    """
    List moderation cases - CHRONOLOGICAL (Rule #5).
    NOT sorted by severity.
    """
    s = ModerationStatus(status) if status else None
    cases = agent.list_moderation_cases(UUID(community_id), status=s)
    return [{
        "id": str(c.id),
        "case_number": c.case_number,
        "target": c.target_user_name,
        "action": c.action.value,
        "status": c.status.value
    } for c in cases]

@router.post("/moderation/{case_id}/approve")
async def approve_moderation(case_id: str, approved_by: str):
    """
    GOVERNANCE CHECKPOINT: Approve moderation action (Rule #1).
    """
    case = agent.approve_moderation_action(UUID(case_id), approved_by)
    return {
        "status": case.status.value,
        "approved_by": approved_by,
        "governance": "Approved - ready for execution"
    }

@router.post("/moderation/{case_id}/reject")
async def reject_moderation(case_id: str, rejected_by: str, reason: str = ""):
    """Reject moderation action."""
    case = agent.reject_moderation_action(UUID(case_id), rejected_by, reason)
    return {"status": case.status.value}

@router.post("/moderation/{case_id}/execute")
async def execute_moderation(case_id: str):
    """
    Execute approved moderation action.
    CANNOT execute without prior approval (Rule #1).
    """
    try:
        case = agent.execute_moderation_action(UUID(case_id))
        return {"status": case.status.value, "executed_at": case.executed_at.isoformat()}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# DIRECT MESSAGE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/dm", status_code=201)
async def send_dm(sender_id: str, request: DMRequest):
    """Send a direct message."""
    dm = agent.send_direct_message(sender_id, request.recipient_id, request.content)
    return {"id": str(dm.id)}

@router.get("/dm/{user_id}")
async def list_dms(user_id: str, other_user_id: Optional[str] = None):
    """
    List direct messages - CHRONOLOGICAL (Rule #5).
    """
    dms = agent.list_direct_messages(user_id, other_user_id)
    return [{"id": str(dm.id), "from": dm.sender_id, "content": dm.content[:100], "read": dm.read} for dm in dms]

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/communities/{community_id}/analytics")
async def get_analytics(community_id: str):
    """Get community analytics."""
    return agent.get_community_analytics(UUID(community_id))

@router.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy", "service": "community", "version": "v68", "governance": "Rules #1, #5, #6 enforced"}
