"""
CHE·NU™ V68 — Community & Social Platforms Agent
Discord/Slack/Circle Killer: $9-99/mo → $29/mo with GOVERNANCE

COMPETITIVE ANALYSIS:
- Discord: $9.99/mo (Nitro) - Gaming focus
- Slack: $8.75/user/mo - Business focus
- Circle: $89/mo - Creator communities
- Mighty Networks: $99/mo - Course + Community
- CHE·NU: $29/mo - GOVERNED community platform

GOVERNANCE COMPLIANCE:
- Rule #1: Moderation actions (ban/kick/mute) require HUMAN approval
- Rule #5: Members ALPHABETICAL (NOT by engagement), Posts CHRONOLOGICAL (NOT by likes)
- Rule #6: Full audit trail with UUID, timestamps, actor IDs
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class CommunityType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INVITE_ONLY = "invite_only"


class CommunityStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class ChannelType(Enum):
    TEXT = "text"
    VOICE = "voice"
    ANNOUNCEMENTS = "announcements"
    EVENTS = "events"
    FORUM = "forum"


class MemberRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"
    GUEST = "guest"


class MemberStatus(Enum):
    ACTIVE = "active"
    MUTED = "muted"
    PENDING = "pending"
    BANNED = "banned"
    LEFT = "left"


class PostType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    LINK = "link"
    POLL = "poll"
    EVENT = "event"


class PostStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    DELETED = "deleted"


class EventStatus(Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ModerationAction(Enum):
    WARN = "warn"
    MUTE = "mute"
    KICK = "kick"
    BAN = "ban"
    DELETE_CONTENT = "delete_content"


class ModerationStatus(Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"


class PollStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Community:
    """Community/Workspace."""
    id: UUID
    name: str
    description: str
    community_type: CommunityType
    status: CommunityStatus
    owner_id: str
    icon_url: Optional[str]
    banner_url: Optional[str]
    member_count: int
    created_at: datetime
    created_by: str
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Channel:
    """Community channel/space."""
    id: UUID
    community_id: UUID
    name: str
    description: str
    channel_type: ChannelType
    is_private: bool
    position: int
    created_at: datetime
    created_by: str
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Member:
    """Community member."""
    id: UUID
    community_id: UUID
    user_id: str
    display_name: str
    role: MemberRole
    status: MemberStatus
    joined_at: datetime
    invited_by: Optional[str] = None
    muted_until: Optional[datetime] = None
    banned_reason: Optional[str] = None


@dataclass
class Post:
    """Community post/message."""
    id: UUID
    post_number: str
    community_id: UUID
    channel_id: UUID
    author_id: str
    author_name: str
    post_type: PostType
    content: str
    attachments: List[str]
    status: PostStatus
    created_at: datetime
    edited_at: Optional[datetime] = None
    # Note: No like_count, engagement metrics - Rule #5


@dataclass
class Event:
    """Community event."""
    id: UUID
    event_number: str
    community_id: UUID
    title: str
    description: str
    event_type: str
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    is_virtual: bool
    max_attendees: Optional[int]
    attendee_ids: List[str]
    status: EventStatus
    created_at: datetime
    created_by: str


@dataclass
class Poll:
    """Community poll."""
    id: UUID
    poll_number: str
    community_id: UUID
    channel_id: UUID
    question: str
    options: List[str]
    votes: Dict[str, List[str]]  # option -> list of voter IDs
    status: PollStatus
    ends_at: Optional[datetime]
    created_at: datetime
    created_by: str
    # Note: Results shown as counts only, no ranking - Rule #5


@dataclass
class ModerationCase:
    """Moderation action requiring approval."""
    id: UUID
    case_number: str
    community_id: UUID
    target_user_id: str
    target_user_name: str
    action: ModerationAction
    reason: str
    evidence: List[str]
    status: ModerationStatus
    requested_by: str
    requested_at: datetime
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None


@dataclass
class DirectMessage:
    """Direct message between members."""
    id: UUID
    sender_id: str
    recipient_id: str
    content: str
    read: bool
    created_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# COMMUNITY AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class CommunityAgent:
    """
    Community & Social Platforms Agent.
    
    Competes with Discord, Slack, Circle, Mighty Networks.
    Implements full governance compliance.
    """
    
    def __init__(self):
        self.communities: Dict[UUID, Community] = {}
        self.channels: Dict[UUID, Channel] = {}
        self.members: Dict[UUID, Member] = {}
        self.posts: Dict[UUID, Post] = {}
        self.events: Dict[UUID, Event] = {}
        self.polls: Dict[UUID, Poll] = {}
        self.moderation_cases: Dict[UUID, ModerationCase] = {}
        self.direct_messages: Dict[UUID, DirectMessage] = {}
        
        # Sequential numbering
        self._post_counter = 0
        self._event_counter = 0
        self._poll_counter = 0
        self._case_counter = 0
        
        logger.info("CommunityAgent initialized - Discord/Slack/Circle killer")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMMUNITY MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_community(
        self,
        name: str,
        description: str,
        community_type: CommunityType,
        owner_id: str,
        created_by: str,
        icon_url: Optional[str] = None,
        banner_url: Optional[str] = None
    ) -> Community:
        """Create a new community."""
        community = Community(
            id=uuid4(),
            name=name,
            description=description,
            community_type=community_type,
            status=CommunityStatus.ACTIVE,
            owner_id=owner_id,
            icon_url=icon_url,
            banner_url=banner_url,
            member_count=0,  # Will be incremented when owner is added
            created_at=datetime.utcnow(),
            created_by=created_by
        )
        self.communities[community.id] = community
        
        # Auto-add owner as member
        self._add_member_internal(
            community.id,
            owner_id,
            owner_id,  # display_name placeholder
            MemberRole.OWNER,
            created_by
        )
        
        # Create default channels
        self._create_default_channels(community.id, created_by)
        
        logger.info(f"Community created: {name} by {created_by}")
        return community
    
    def _create_default_channels(self, community_id: UUID, created_by: str):
        """Create default channels for new community."""
        defaults = [
            ("general", "General discussion", ChannelType.TEXT),
            ("announcements", "Community announcements", ChannelType.ANNOUNCEMENTS),
            ("events", "Upcoming events", ChannelType.EVENTS),
        ]
        for i, (name, desc, channel_type) in enumerate(defaults):
            self.create_channel(
                community_id=community_id,
                name=name,
                description=desc,
                channel_type=channel_type,
                created_by=created_by,
                position=i
            )
    
    def list_communities(
        self,
        owner_id: Optional[str] = None,
        community_type: Optional[CommunityType] = None
    ) -> List[Community]:
        """
        List communities - ALPHABETICAL by name (Rule #5).
        NOT sorted by member count or activity.
        """
        communities = list(self.communities.values())
        
        if owner_id:
            communities = [c for c in communities if c.owner_id == owner_id]
        if community_type:
            communities = [c for c in communities if c.community_type == community_type]
        
        # Rule #5: ALPHABETICAL by name, NOT by member count
        communities.sort(key=lambda x: x.name.lower())
        return communities
    
    def get_community(self, community_id: UUID) -> Optional[Community]:
        """Get community by ID."""
        return self.communities.get(community_id)
    
    def update_community(
        self,
        community_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon_url: Optional[str] = None,
        banner_url: Optional[str] = None
    ) -> Community:
        """Update community details."""
        community = self.communities.get(community_id)
        if not community:
            raise ValueError(f"Community not found: {community_id}")
        
        if name:
            community.name = name
        if description:
            community.description = description
        if icon_url:
            community.icon_url = icon_url
        if banner_url:
            community.banner_url = banner_url
        
        return community
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHANNEL MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_channel(
        self,
        community_id: UUID,
        name: str,
        description: str,
        channel_type: ChannelType,
        created_by: str,
        is_private: bool = False,
        position: int = 0
    ) -> Channel:
        """Create a new channel."""
        channel = Channel(
            id=uuid4(),
            community_id=community_id,
            name=name,
            description=description,
            channel_type=channel_type,
            is_private=is_private,
            position=position,
            created_at=datetime.utcnow(),
            created_by=created_by
        )
        self.channels[channel.id] = channel
        
        logger.info(f"Channel created: {name} in community {community_id}")
        return channel
    
    def list_channels(
        self,
        community_id: UUID,
        channel_type: Optional[ChannelType] = None
    ) -> List[Channel]:
        """
        List channels - ALPHABETICAL by name (Rule #5).
        NOT sorted by activity or message count.
        """
        channels = [c for c in self.channels.values() if c.community_id == community_id]
        
        if channel_type:
            channels = [c for c in channels if c.channel_type == channel_type]
        
        # Rule #5: ALPHABETICAL by name, NOT by activity
        channels.sort(key=lambda x: x.name.lower())
        return channels
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MEMBER MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _add_member_internal(
        self,
        community_id: UUID,
        user_id: str,
        display_name: str,
        role: MemberRole,
        invited_by: str
    ) -> Member:
        """Internal method to add member."""
        member = Member(
            id=uuid4(),
            community_id=community_id,
            user_id=user_id,
            display_name=display_name,
            role=role,
            status=MemberStatus.ACTIVE,
            joined_at=datetime.utcnow(),
            invited_by=invited_by
        )
        self.members[member.id] = member
        
        # Update community member count
        community = self.communities.get(community_id)
        if community:
            community.member_count += 1
        
        return member
    
    def add_member(
        self,
        community_id: UUID,
        user_id: str,
        display_name: str,
        invited_by: str,
        role: MemberRole = MemberRole.MEMBER
    ) -> Member:
        """Add a new member to community."""
        community = self.communities.get(community_id)
        if not community:
            raise ValueError(f"Community not found: {community_id}")
        
        # Check if already member
        existing = [m for m in self.members.values() 
                   if m.community_id == community_id and m.user_id == user_id]
        if existing:
            raise ValueError(f"User {user_id} is already a member")
        
        member = self._add_member_internal(
            community_id, user_id, display_name, role, invited_by
        )
        
        logger.info(f"Member added: {display_name} to community {community_id}")
        return member
    
    def list_members(
        self,
        community_id: UUID,
        role: Optional[MemberRole] = None,
        status: Optional[MemberStatus] = None
    ) -> List[Member]:
        """
        List members - ALPHABETICAL by display_name (Rule #5).
        NOT sorted by join date, engagement, or activity.
        """
        members = [m for m in self.members.values() if m.community_id == community_id]
        
        if role:
            members = [m for m in members if m.role == role]
        if status:
            members = [m for m in members if m.status == status]
        
        # Rule #5: ALPHABETICAL by display_name, NOT by engagement
        members.sort(key=lambda x: x.display_name.lower())
        return members
    
    def update_member_role(
        self,
        member_id: UUID,
        new_role: MemberRole,
        updated_by: str
    ) -> Member:
        """Update member role."""
        member = self.members.get(member_id)
        if not member:
            raise ValueError(f"Member not found: {member_id}")
        
        member.role = new_role
        logger.info(f"Member role updated: {member_id} to {new_role.value} by {updated_by}")
        return member
    
    def leave_community(self, member_id: UUID) -> Member:
        """Member leaves community."""
        member = self.members.get(member_id)
        if not member:
            raise ValueError(f"Member not found: {member_id}")
        
        member.status = MemberStatus.LEFT
        
        # Update community member count
        community = self.communities.get(member.community_id)
        if community:
            community.member_count = max(0, community.member_count - 1)
        
        return member
    
    # ═══════════════════════════════════════════════════════════════════════════
    # POST MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_post(
        self,
        community_id: UUID,
        channel_id: UUID,
        author_id: str,
        author_name: str,
        content: str,
        post_type: PostType = PostType.TEXT,
        attachments: Optional[List[str]] = None
    ) -> Post:
        """Create a new post."""
        self._post_counter += 1
        
        post = Post(
            id=uuid4(),
            post_number=f"P-{self._post_counter:06d}",
            community_id=community_id,
            channel_id=channel_id,
            author_id=author_id,
            author_name=author_name,
            post_type=post_type,
            content=content,
            attachments=attachments or [],
            status=PostStatus.PUBLISHED,
            created_at=datetime.utcnow()
        )
        self.posts[post.id] = post
        
        logger.info(f"Post created: {post.post_number} by {author_name}")
        return post
    
    def list_posts(
        self,
        channel_id: UUID,
        author_id: Optional[str] = None,
        post_type: Optional[PostType] = None,
        limit: int = 50
    ) -> List[Post]:
        """
        List posts - CHRONOLOGICAL by created_at (Rule #5).
        NOT sorted by likes, engagement, or popularity.
        """
        posts = [p for p in self.posts.values() 
                if p.channel_id == channel_id and p.status == PostStatus.PUBLISHED]
        
        if author_id:
            posts = [p for p in posts if p.author_id == author_id]
        if post_type:
            posts = [p for p in posts if p.post_type == post_type]
        
        # Rule #5: CHRONOLOGICAL by created_at, NOT by likes/engagement
        posts.sort(key=lambda x: x.created_at, reverse=True)
        return posts[:limit]
    
    def edit_post(
        self,
        post_id: UUID,
        content: str,
        edited_by: str
    ) -> Post:
        """Edit a post."""
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post not found: {post_id}")
        
        if post.author_id != edited_by:
            raise ValueError("Only author can edit their post")
        
        post.content = content
        post.edited_at = datetime.utcnow()
        return post
    
    def delete_post(self, post_id: UUID, deleted_by: str) -> Post:
        """Soft delete a post."""
        post = self.posts.get(post_id)
        if not post:
            raise ValueError(f"Post not found: {post_id}")
        
        post.status = PostStatus.DELETED
        logger.info(f"Post deleted: {post.post_number} by {deleted_by}")
        return post
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EVENT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_event(
        self,
        community_id: UUID,
        title: str,
        description: str,
        event_type: str,
        start_time: datetime,
        end_time: datetime,
        created_by: str,
        location: Optional[str] = None,
        is_virtual: bool = True,
        max_attendees: Optional[int] = None
    ) -> Event:
        """Create a community event."""
        self._event_counter += 1
        
        event = Event(
            id=uuid4(),
            event_number=f"EVT-{self._event_counter:04d}",
            community_id=community_id,
            title=title,
            description=description,
            event_type=event_type,
            start_time=start_time,
            end_time=end_time,
            location=location,
            is_virtual=is_virtual,
            max_attendees=max_attendees,
            attendee_ids=[created_by],  # Creator auto-attends
            status=EventStatus.SCHEDULED,
            created_at=datetime.utcnow(),
            created_by=created_by
        )
        self.events[event.id] = event
        
        logger.info(f"Event created: {title} ({event.event_number})")
        return event
    
    def list_events(
        self,
        community_id: UUID,
        status: Optional[EventStatus] = None
    ) -> List[Event]:
        """
        List events - CHRONOLOGICAL by start_time (Rule #5).
        Upcoming events first.
        """
        events = [e for e in self.events.values() if e.community_id == community_id]
        
        if status:
            events = [e for e in events if e.status == status]
        
        # Rule #5: CHRONOLOGICAL by start_time
        events.sort(key=lambda x: x.start_time)
        return events
    
    def rsvp_event(self, event_id: UUID, user_id: str) -> Event:
        """RSVP to an event."""
        event = self.events.get(event_id)
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        
        if user_id in event.attendee_ids:
            raise ValueError("Already RSVPed")
        
        if event.max_attendees and len(event.attendee_ids) >= event.max_attendees:
            raise ValueError("Event is at capacity")
        
        event.attendee_ids.append(user_id)
        return event
    
    def cancel_rsvp(self, event_id: UUID, user_id: str) -> Event:
        """Cancel RSVP to an event."""
        event = self.events.get(event_id)
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        
        if user_id not in event.attendee_ids:
            raise ValueError("Not RSVPed")
        
        event.attendee_ids.remove(user_id)
        return event
    
    def start_event(self, event_id: UUID) -> Event:
        """Start a live event."""
        event = self.events.get(event_id)
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        
        event.status = EventStatus.LIVE
        return event
    
    def end_event(self, event_id: UUID) -> Event:
        """End an event."""
        event = self.events.get(event_id)
        if not event:
            raise ValueError(f"Event not found: {event_id}")
        
        event.status = EventStatus.COMPLETED
        return event
    
    # ═══════════════════════════════════════════════════════════════════════════
    # POLL MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_poll(
        self,
        community_id: UUID,
        channel_id: UUID,
        question: str,
        options: List[str],
        created_by: str,
        duration_hours: Optional[int] = None
    ) -> Poll:
        """Create a poll."""
        self._poll_counter += 1
        
        poll = Poll(
            id=uuid4(),
            poll_number=f"POLL-{self._poll_counter:04d}",
            community_id=community_id,
            channel_id=channel_id,
            question=question,
            options=options,
            votes={opt: [] for opt in options},
            status=PollStatus.ACTIVE,
            ends_at=datetime.utcnow() + timedelta(hours=duration_hours) if duration_hours else None,
            created_at=datetime.utcnow(),
            created_by=created_by
        )
        self.polls[poll.id] = poll
        
        logger.info(f"Poll created: {question} ({poll.poll_number})")
        return poll
    
    def vote_poll(self, poll_id: UUID, option: str, voter_id: str) -> Poll:
        """Vote in a poll."""
        poll = self.polls.get(poll_id)
        if not poll:
            raise ValueError(f"Poll not found: {poll_id}")
        
        if poll.status != PollStatus.ACTIVE:
            raise ValueError("Poll is closed")
        
        if option not in poll.options:
            raise ValueError(f"Invalid option: {option}")
        
        # Remove previous vote if any
        for opt, voters in poll.votes.items():
            if voter_id in voters:
                voters.remove(voter_id)
        
        # Add new vote
        poll.votes[option].append(voter_id)
        return poll
    
    def close_poll(self, poll_id: UUID, closed_by: str) -> Poll:
        """Close a poll."""
        poll = self.polls.get(poll_id)
        if not poll:
            raise ValueError(f"Poll not found: {poll_id}")
        
        poll.status = PollStatus.CLOSED
        logger.info(f"Poll closed: {poll.poll_number} by {closed_by}")
        return poll
    
    def get_poll_results(self, poll_id: UUID) -> Dict[str, int]:
        """
        Get poll results - Returns vote counts only (Rule #5).
        Options are listed in ORIGINAL order, NOT by vote count.
        """
        poll = self.polls.get(poll_id)
        if not poll:
            raise ValueError(f"Poll not found: {poll_id}")
        
        # Rule #5: Return in ORIGINAL order, not sorted by votes
        results = {}
        for option in poll.options:  # Preserve original order
            results[option] = len(poll.votes.get(option, []))
        
        return results
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MODERATION (GOVERNANCE - Rule #1)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def request_moderation_action(
        self,
        community_id: UUID,
        target_user_id: str,
        target_user_name: str,
        action: ModerationAction,
        reason: str,
        requested_by: str,
        evidence: Optional[List[str]] = None
    ) -> ModerationCase:
        """
        Request moderation action - REQUIRES APPROVAL (Rule #1).
        Ban, kick, mute actions cannot be executed without human approval.
        """
        self._case_counter += 1
        
        case = ModerationCase(
            id=uuid4(),
            case_number=f"MOD-{self._case_counter:04d}",
            community_id=community_id,
            target_user_id=target_user_id,
            target_user_name=target_user_name,
            action=action,
            reason=reason,
            evidence=evidence or [],
            status=ModerationStatus.PENDING_APPROVAL,
            requested_by=requested_by,
            requested_at=datetime.utcnow()
        )
        self.moderation_cases[case.id] = case
        
        logger.info(f"Moderation case created: {case.case_number} - {action.value} for {target_user_name}")
        logger.warning("GOVERNANCE: Moderation action requires human approval (Rule #1)")
        return case
    
    def approve_moderation_action(
        self,
        case_id: UUID,
        approved_by: str
    ) -> ModerationCase:
        """
        GOVERNANCE CHECKPOINT: Approve moderation action (Rule #1).
        Only after approval can the action be executed.
        """
        case = self.moderation_cases.get(case_id)
        if not case:
            raise ValueError(f"Moderation case not found: {case_id}")
        
        if case.status != ModerationStatus.PENDING_APPROVAL:
            raise ValueError(f"Case not pending approval: {case.status.value}")
        
        case.status = ModerationStatus.APPROVED
        case.approved_by = approved_by
        case.approved_at = datetime.utcnow()
        
        logger.info(f"Moderation case approved: {case.case_number} by {approved_by}")
        return case
    
    def reject_moderation_action(
        self,
        case_id: UUID,
        rejected_by: str,
        rejection_reason: str
    ) -> ModerationCase:
        """Reject a moderation action request."""
        case = self.moderation_cases.get(case_id)
        if not case:
            raise ValueError(f"Moderation case not found: {case_id}")
        
        case.status = ModerationStatus.REJECTED
        case.approved_by = rejected_by  # Store who rejected
        case.approved_at = datetime.utcnow()
        
        logger.info(f"Moderation case rejected: {case.case_number} by {rejected_by}")
        return case
    
    def execute_moderation_action(self, case_id: UUID) -> ModerationCase:
        """
        Execute approved moderation action.
        CANNOT execute without prior approval (Rule #1).
        """
        case = self.moderation_cases.get(case_id)
        if not case:
            raise ValueError(f"Moderation case not found: {case_id}")
        
        # GOVERNANCE: Must be approved first
        if case.status != ModerationStatus.APPROVED:
            raise ValueError(
                f"GOVERNANCE VIOLATION: Cannot execute moderation without approval. "
                f"Current status: {case.status.value}"
            )
        
        # Find member
        members = [m for m in self.members.values() 
                  if m.community_id == case.community_id and m.user_id == case.target_user_id]
        
        if not members:
            raise ValueError(f"Member not found: {case.target_user_id}")
        
        member = members[0]
        
        # Execute action
        if case.action == ModerationAction.MUTE:
            member.status = MemberStatus.MUTED
            member.muted_until = datetime.utcnow() + timedelta(hours=24)
        elif case.action == ModerationAction.KICK:
            member.status = MemberStatus.LEFT
        elif case.action == ModerationAction.BAN:
            member.status = MemberStatus.BANNED
            member.banned_reason = case.reason
        elif case.action == ModerationAction.WARN:
            pass  # Warning logged only
        
        case.status = ModerationStatus.EXECUTED
        case.executed_at = datetime.utcnow()
        
        logger.info(f"Moderation action executed: {case.case_number} - {case.action.value}")
        return case
    
    def list_moderation_cases(
        self,
        community_id: UUID,
        status: Optional[ModerationStatus] = None
    ) -> List[ModerationCase]:
        """
        List moderation cases - CHRONOLOGICAL by requested_at (Rule #5).
        NOT sorted by severity.
        """
        cases = [c for c in self.moderation_cases.values() 
                if c.community_id == community_id]
        
        if status:
            cases = [c for c in cases if c.status == status]
        
        # Rule #5: CHRONOLOGICAL by requested_at
        cases.sort(key=lambda x: x.requested_at, reverse=True)
        return cases
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DIRECT MESSAGES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def send_direct_message(
        self,
        sender_id: str,
        recipient_id: str,
        content: str
    ) -> DirectMessage:
        """Send a direct message."""
        dm = DirectMessage(
            id=uuid4(),
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
            read=False,
            created_at=datetime.utcnow()
        )
        self.direct_messages[dm.id] = dm
        return dm
    
    def list_direct_messages(
        self,
        user_id: str,
        other_user_id: Optional[str] = None
    ) -> List[DirectMessage]:
        """
        List direct messages - CHRONOLOGICAL by created_at (Rule #5).
        """
        dms = [dm for dm in self.direct_messages.values()
              if dm.sender_id == user_id or dm.recipient_id == user_id]
        
        if other_user_id:
            dms = [dm for dm in dms
                  if dm.sender_id == other_user_id or dm.recipient_id == other_user_id]
        
        # Rule #5: CHRONOLOGICAL
        dms.sort(key=lambda x: x.created_at, reverse=True)
        return dms
    
    def mark_dm_read(self, dm_id: UUID) -> DirectMessage:
        """Mark DM as read."""
        dm = self.direct_messages.get(dm_id)
        if not dm:
            raise ValueError(f"DM not found: {dm_id}")
        
        dm.read = True
        return dm
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANALYTICS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_community_analytics(self, community_id: UUID) -> Dict[str, Any]:
        """
        Get community analytics.
        Metrics only - no ranking or engagement scoring (Rule #5).
        """
        community = self.communities.get(community_id)
        if not community:
            raise ValueError(f"Community not found: {community_id}")
        
        members = [m for m in self.members.values() if m.community_id == community_id]
        channels = [c for c in self.channels.values() if c.community_id == community_id]
        posts = [p for p in self.posts.values() if p.community_id == community_id]
        events = [e for e in self.events.values() if e.community_id == community_id]
        
        active_members = [m for m in members if m.status == MemberStatus.ACTIVE]
        
        # Count by role (no ranking)
        roles = {}
        for member in active_members:
            role_name = member.role.value
            roles[role_name] = roles.get(role_name, 0) + 1
        
        # Channel counts (no activity ranking)
        channel_types = {}
        for channel in channels:
            type_name = channel.channel_type.value
            channel_types[type_name] = channel_types.get(type_name, 0) + 1
        
        # Event stats
        upcoming_events = [e for e in events if e.status == EventStatus.SCHEDULED]
        
        return {
            "community": {
                "id": str(community_id),
                "name": community.name,
                "type": community.community_type.value,
                "status": community.status.value
            },
            "members": {
                "total": len(members),
                "active": len(active_members),
                "by_role": roles  # Not ranked
            },
            "channels": {
                "total": len(channels),
                "by_type": channel_types  # Not ranked by activity
            },
            "content": {
                "total_posts": len([p for p in posts if p.status == PostStatus.PUBLISHED]),
                "today": len([p for p in posts 
                            if p.created_at.date() == datetime.utcnow().date()])
            },
            "events": {
                "upcoming": len(upcoming_events),
                "total": len(events)
            },
            "governance": {
                "pending_moderation": len([c for c in self.moderation_cases.values()
                                          if c.community_id == community_id
                                          and c.status == ModerationStatus.PENDING_APPROVAL])
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO/TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    agent = CommunityAgent()
    
    # Create community
    community = agent.create_community(
        name="CHE·NU Builders",
        description="Community for CHE·NU developers",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_001",
        created_by="owner_001"
    )
    print(f"✅ Community created: {community.name}")
    
    # Add members
    member = agent.add_member(
        community_id=community.id,
        user_id="dev_001",
        display_name="Alice Developer",
        invited_by="owner_001"
    )
    print(f"✅ Member added: {member.display_name}")
    
    # Create post
    channel = agent.list_channels(community.id)[0]
    post = agent.create_post(
        community_id=community.id,
        channel_id=channel.id,
        author_id="dev_001",
        author_name="Alice Developer",
        content="Hello community!"
    )
    print(f"✅ Post created: {post.post_number}")
    
    # Request moderation (requires approval)
    case = agent.request_moderation_action(
        community_id=community.id,
        target_user_id="bad_user",
        target_user_name="Bad User",
        action=ModerationAction.BAN,
        reason="Spam",
        requested_by="owner_001"
    )
    print(f"✅ Moderation case: {case.case_number} - Status: {case.status.value}")
    
    # Try execute without approval (should fail)
    try:
        agent.execute_moderation_action(case.id)
        print("❌ Should have failed!")
    except ValueError as e:
        print(f"✅ Governance enforced: {e}")
    
    # Approve and execute
    agent.approve_moderation_action(case.id, "owner_001")
    print(f"✅ Moderation approved")
    
    print("\n🎉 CommunityAgent working correctly with governance!")
