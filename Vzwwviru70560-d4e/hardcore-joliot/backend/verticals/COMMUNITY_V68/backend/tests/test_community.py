"""
CHE·NU™ V68 — Community & Social Platforms Tests
Discord/Slack/Circle Killer: $9-99/mo → $29/mo with GOVERNANCE

Tests verify:
- Rule #1: Moderation actions require human approval
- Rule #5: ALPHABETICAL/CHRONOLOGICAL listings (NOT by engagement)
- Rule #6: Full audit trail
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.spheres.community.agents.community_agent import (
    CommunityAgent,
    CommunityType,
    CommunityStatus,
    ChannelType,
    MemberRole,
    MemberStatus,
    PostType,
    PostStatus,
    EventStatus,
    PollStatus,
    ModerationAction,
    ModerationStatus
)


@pytest.fixture
def agent():
    """Create fresh agent for each test."""
    return CommunityAgent()


@pytest.fixture
def sample_community(agent):
    """Create a sample community for testing."""
    return agent.create_community(
        name="Test Community",
        description="A test community",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_001",
        created_by="owner_001"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# COMMUNITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_create_community(agent):
    """Test community creation."""
    community = agent.create_community(
        name="Developer Hub",
        description="Community for developers",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_001",
        created_by="owner_001"
    )
    
    assert community.name == "Developer Hub"
    assert community.community_type == CommunityType.PUBLIC
    assert community.status == CommunityStatus.ACTIVE
    assert community.member_count == 1  # Owner auto-added
    assert isinstance(community.id, UUID)
    assert community.created_by == "owner_001"


def test_communities_alphabetical_rule5(agent):
    """Rule #5: Communities listed ALPHABETICALLY by name, NOT by member count."""
    # Create communities with different sizes
    agent.create_community(
        name="Zebra Community",
        description="Large community",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_z",
        created_by="owner_z"
    )
    
    agent.create_community(
        name="Alpha Community",
        description="Small community",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_a",
        created_by="owner_a"
    )
    
    agent.create_community(
        name="Mango Community",
        description="Medium community",
        community_type=CommunityType.PUBLIC,
        owner_id="owner_m",
        created_by="owner_m"
    )
    
    communities = agent.list_communities()
    names = [c.name for c in communities]
    
    # Must be alphabetical
    assert names == ["Alpha Community", "Mango Community", "Zebra Community"]
    # NOT sorted by member count


def test_default_channels_created(agent, sample_community):
    """Test that default channels are created."""
    channels = agent.list_channels(sample_community.id)
    
    # Should have default channels
    assert len(channels) >= 3
    channel_names = [c.name for c in channels]
    assert "general" in channel_names
    assert "announcements" in channel_names


# ═══════════════════════════════════════════════════════════════════════════════
# MEMBER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_add_member(agent, sample_community):
    """Test adding a member."""
    member = agent.add_member(
        community_id=sample_community.id,
        user_id="user_001",
        display_name="Alice Developer",
        invited_by="owner_001"
    )
    
    assert member.display_name == "Alice Developer"
    assert member.role == MemberRole.MEMBER
    assert member.status == MemberStatus.ACTIVE
    assert isinstance(member.id, UUID)


def test_members_alphabetical_rule5(agent, sample_community):
    """Rule #5: Members listed ALPHABETICALLY, NOT by join date or engagement."""
    # Add members in random order
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_z",
        display_name="Zach",
        invited_by="owner_001"
    )
    
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_a",
        display_name="Alice",
        invited_by="owner_001"
    )
    
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_m",
        display_name="Mike",
        invited_by="owner_001"
    )
    
    members = agent.list_members(sample_community.id)
    names = [m.display_name for m in members]
    
    # Must be alphabetical (owner might be in there too)
    sorted_names = sorted(names, key=str.lower)
    assert names == sorted_names


def test_update_member_role(agent, sample_community):
    """Test updating member role."""
    member = agent.add_member(
        community_id=sample_community.id,
        user_id="user_001",
        display_name="Alice",
        invited_by="owner_001"
    )
    
    updated = agent.update_member_role(member.id, MemberRole.MODERATOR, "owner_001")
    assert updated.role == MemberRole.MODERATOR


# ═══════════════════════════════════════════════════════════════════════════════
# CHANNEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_create_channel(agent, sample_community):
    """Test channel creation."""
    channel = agent.create_channel(
        community_id=sample_community.id,
        name="dev-chat",
        description="Developer discussions",
        channel_type=ChannelType.TEXT,
        created_by="owner_001"
    )
    
    assert channel.name == "dev-chat"
    assert channel.channel_type == ChannelType.TEXT
    assert isinstance(channel.id, UUID)


def test_channels_alphabetical_rule5(agent, sample_community):
    """Rule #5: Channels listed ALPHABETICALLY, NOT by activity."""
    # Create additional channels
    agent.create_channel(
        community_id=sample_community.id,
        name="zebra-zone",
        description="Z channel",
        channel_type=ChannelType.TEXT,
        created_by="owner_001"
    )
    
    agent.create_channel(
        community_id=sample_community.id,
        name="alpha-chat",
        description="A channel",
        channel_type=ChannelType.TEXT,
        created_by="owner_001"
    )
    
    channels = agent.list_channels(sample_community.id)
    names = [c.name for c in channels]
    
    # Must be alphabetical
    sorted_names = sorted(names, key=str.lower)
    assert names == sorted_names


# ═══════════════════════════════════════════════════════════════════════════════
# POST TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_create_post(agent, sample_community):
    """Test post creation."""
    channel = agent.list_channels(sample_community.id)[0]
    
    post = agent.create_post(
        community_id=sample_community.id,
        channel_id=channel.id,
        author_id="user_001",
        author_name="Alice",
        content="Hello world!"
    )
    
    assert post.content == "Hello world!"
    assert post.post_number.startswith("P-")
    assert post.status == PostStatus.PUBLISHED
    assert isinstance(post.id, UUID)


def test_posts_chronological_rule5(agent, sample_community):
    """Rule #5: Posts listed CHRONOLOGICALLY, NOT by likes or engagement."""
    channel = agent.list_channels(sample_community.id)[0]
    
    # Create posts
    post1 = agent.create_post(
        community_id=sample_community.id,
        channel_id=channel.id,
        author_id="user_001",
        author_name="Alice",
        content="First post"
    )
    
    post2 = agent.create_post(
        community_id=sample_community.id,
        channel_id=channel.id,
        author_id="user_002",
        author_name="Bob",
        content="Second post"
    )
    
    post3 = agent.create_post(
        community_id=sample_community.id,
        channel_id=channel.id,
        author_id="user_003",
        author_name="Charlie",
        content="Third post"
    )
    
    posts = agent.list_posts(channel.id)
    
    # Most recent first (reverse chronological)
    assert posts[0].content == "Third post"
    assert posts[1].content == "Second post"
    assert posts[2].content == "First post"


# ═══════════════════════════════════════════════════════════════════════════════
# EVENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_create_event(agent, sample_community):
    """Test event creation."""
    event = agent.create_event(
        community_id=sample_community.id,
        title="Developer Meetup",
        description="Monthly meetup",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=7),
        end_time=datetime.utcnow() + timedelta(days=7, hours=2),
        created_by="owner_001"
    )
    
    assert event.title == "Developer Meetup"
    assert event.event_number.startswith("EVT-")
    assert event.status == EventStatus.SCHEDULED
    assert "owner_001" in event.attendee_ids


def test_events_chronological_rule5(agent, sample_community):
    """Rule #5: Events listed CHRONOLOGICALLY by start time."""
    # Create events in random order
    event3 = agent.create_event(
        community_id=sample_community.id,
        title="Event C",
        description="Far future",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=30),
        end_time=datetime.utcnow() + timedelta(days=30, hours=2),
        created_by="owner_001"
    )
    
    event1 = agent.create_event(
        community_id=sample_community.id,
        title="Event A",
        description="Soon",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=1),
        end_time=datetime.utcnow() + timedelta(days=1, hours=2),
        created_by="owner_001"
    )
    
    event2 = agent.create_event(
        community_id=sample_community.id,
        title="Event B",
        description="Later",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=14),
        end_time=datetime.utcnow() + timedelta(days=14, hours=2),
        created_by="owner_001"
    )
    
    events = agent.list_events(sample_community.id)
    titles = [e.title for e in events]
    
    # Chronological order
    assert titles == ["Event A", "Event B", "Event C"]


def test_rsvp_event(agent, sample_community):
    """Test RSVP to event."""
    event = agent.create_event(
        community_id=sample_community.id,
        title="Meetup",
        description="Test",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=7),
        end_time=datetime.utcnow() + timedelta(days=7, hours=2),
        created_by="owner_001"
    )
    
    agent.rsvp_event(event.id, "user_001")
    
    updated_event = agent.events[event.id]
    assert "user_001" in updated_event.attendee_ids


# ═══════════════════════════════════════════════════════════════════════════════
# POLL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_create_poll(agent, sample_community):
    """Test poll creation."""
    channel = agent.list_channels(sample_community.id)[0]
    
    poll = agent.create_poll(
        community_id=sample_community.id,
        channel_id=channel.id,
        question="What's your favorite language?",
        options=["Python", "JavaScript", "Rust", "Go"],
        created_by="owner_001"
    )
    
    assert poll.question == "What's your favorite language?"
    assert poll.poll_number.startswith("POLL-")
    assert poll.status == PollStatus.ACTIVE
    assert len(poll.options) == 4


def test_vote_poll(agent, sample_community):
    """Test voting in a poll."""
    channel = agent.list_channels(sample_community.id)[0]
    
    poll = agent.create_poll(
        community_id=sample_community.id,
        channel_id=channel.id,
        question="A or B?",
        options=["A", "B"],
        created_by="owner_001"
    )
    
    agent.vote_poll(poll.id, "A", "user_001")
    agent.vote_poll(poll.id, "B", "user_002")
    agent.vote_poll(poll.id, "A", "user_003")
    
    results = agent.get_poll_results(poll.id)
    
    assert results["A"] == 2
    assert results["B"] == 1


def test_poll_results_original_order_rule5(agent, sample_community):
    """Rule #5: Poll results in ORIGINAL option order, NOT sorted by votes."""
    channel = agent.list_channels(sample_community.id)[0]
    
    poll = agent.create_poll(
        community_id=sample_community.id,
        channel_id=channel.id,
        question="Choose one",
        options=["Delta", "Alpha", "Gamma", "Beta"],
        created_by="owner_001"
    )
    
    # Vote more for later options
    agent.vote_poll(poll.id, "Beta", "user_1")
    agent.vote_poll(poll.id, "Beta", "user_2")
    agent.vote_poll(poll.id, "Beta", "user_3")
    agent.vote_poll(poll.id, "Delta", "user_4")
    
    results = agent.get_poll_results(poll.id)
    
    # Results should preserve ORIGINAL order, not sort by votes
    result_keys = list(results.keys())
    assert result_keys == ["Delta", "Alpha", "Gamma", "Beta"]


# ═══════════════════════════════════════════════════════════════════════════════
# MODERATION TESTS (GOVERNANCE - Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

def test_moderation_requires_approval_rule1(agent, sample_community):
    """Rule #1: Moderation actions require HUMAN approval."""
    # Add a member to moderate
    member = agent.add_member(
        community_id=sample_community.id,
        user_id="bad_user",
        display_name="Bad User",
        invited_by="owner_001"
    )
    
    # Request ban
    case = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="bad_user",
        target_user_name="Bad User",
        action=ModerationAction.BAN,
        reason="Spam behavior",
        requested_by="mod_001"
    )
    
    assert case.status == ModerationStatus.PENDING_APPROVAL
    assert case.case_number.startswith("MOD-")


def test_moderation_cannot_execute_without_approval_rule1(agent, sample_community):
    """Rule #1: Cannot execute moderation without prior approval."""
    agent.add_member(
        community_id=sample_community.id,
        user_id="bad_user",
        display_name="Bad User",
        invited_by="owner_001"
    )
    
    case = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="bad_user",
        target_user_name="Bad User",
        action=ModerationAction.KICK,
        reason="Disruptive",
        requested_by="mod_001"
    )
    
    # Try to execute without approval
    with pytest.raises(ValueError) as exc_info:
        agent.execute_moderation_action(case.id)
    
    assert "GOVERNANCE VIOLATION" in str(exc_info.value)
    assert "approval" in str(exc_info.value).lower()


def test_moderation_approval_workflow(agent, sample_community):
    """Test complete moderation workflow with approval."""
    agent.add_member(
        community_id=sample_community.id,
        user_id="problem_user",
        display_name="Problem User",
        invited_by="owner_001"
    )
    
    # Request mute
    case = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="problem_user",
        target_user_name="Problem User",
        action=ModerationAction.MUTE,
        reason="Off-topic spam",
        requested_by="mod_001"
    )
    
    assert case.status == ModerationStatus.PENDING_APPROVAL
    
    # Approve
    agent.approve_moderation_action(case.id, "owner_001")
    assert case.status == ModerationStatus.APPROVED
    assert case.approved_by == "owner_001"
    
    # Execute
    executed_case = agent.execute_moderation_action(case.id)
    assert executed_case.status == ModerationStatus.EXECUTED
    
    # Verify member is muted
    members = [m for m in agent.members.values() if m.user_id == "problem_user"]
    assert members[0].status == MemberStatus.MUTED


def test_moderation_cases_chronological_rule5(agent, sample_community):
    """Rule #5: Moderation cases listed CHRONOLOGICALLY, NOT by severity."""
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_a",
        display_name="User A",
        invited_by="owner_001"
    )
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_b",
        display_name="User B",
        invited_by="owner_001"
    )
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_c",
        display_name="User C",
        invited_by="owner_001"
    )
    
    # Create cases with different severities
    case1 = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="user_a",
        target_user_name="User A",
        action=ModerationAction.WARN,  # Low severity
        reason="Minor issue",
        requested_by="mod_001"
    )
    
    case2 = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="user_b",
        target_user_name="User B",
        action=ModerationAction.BAN,  # High severity
        reason="Major violation",
        requested_by="mod_001"
    )
    
    case3 = agent.request_moderation_action(
        community_id=sample_community.id,
        target_user_id="user_c",
        target_user_name="User C",
        action=ModerationAction.MUTE,  # Medium severity
        reason="Spam",
        requested_by="mod_001"
    )
    
    cases = agent.list_moderation_cases(sample_community.id)
    
    # Must be chronological (most recent first)
    # NOT sorted by action severity
    assert cases[0].target_user_name == "User C"  # Most recent
    assert cases[1].target_user_name == "User B"
    assert cases[2].target_user_name == "User A"  # Oldest


# ═══════════════════════════════════════════════════════════════════════════════
# DIRECT MESSAGE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_send_direct_message(agent):
    """Test sending a direct message."""
    dm = agent.send_direct_message(
        sender_id="user_001",
        recipient_id="user_002",
        content="Hello there!"
    )
    
    assert dm.content == "Hello there!"
    assert dm.sender_id == "user_001"
    assert dm.recipient_id == "user_002"
    assert dm.read == False


def test_dms_chronological_rule5(agent):
    """Rule #5: DMs listed CHRONOLOGICALLY."""
    agent.send_direct_message("user_a", "user_b", "First message")
    agent.send_direct_message("user_b", "user_a", "Second message")
    agent.send_direct_message("user_a", "user_b", "Third message")
    
    dms = agent.list_direct_messages("user_a")
    
    # Most recent first
    assert dms[0].content == "Third message"
    assert dms[1].content == "Second message"
    assert dms[2].content == "First message"


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_community_analytics(agent, sample_community):
    """Test community analytics."""
    # Add some data
    agent.add_member(
        community_id=sample_community.id,
        user_id="user_001",
        display_name="Alice",
        invited_by="owner_001"
    )
    
    channel = agent.list_channels(sample_community.id)[0]
    agent.create_post(
        community_id=sample_community.id,
        channel_id=channel.id,
        author_id="user_001",
        author_name="Alice",
        content="Test post"
    )
    
    agent.create_event(
        community_id=sample_community.id,
        title="Meetup",
        description="Test",
        event_type="meetup",
        start_time=datetime.utcnow() + timedelta(days=7),
        end_time=datetime.utcnow() + timedelta(days=7, hours=2),
        created_by="owner_001"
    )
    
    analytics = agent.get_community_analytics(sample_community.id)
    
    assert analytics["community"]["name"] == "Test Community"
    assert analytics["members"]["total"] >= 2
    assert analytics["channels"]["total"] >= 3
    assert analytics["content"]["total_posts"] >= 1
    assert analytics["events"]["upcoming"] >= 1


def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent is not None
    assert isinstance(agent.communities, dict)
    assert isinstance(agent.channels, dict)
    assert isinstance(agent.members, dict)
    assert isinstance(agent.posts, dict)
    assert isinstance(agent.events, dict)
    assert isinstance(agent.polls, dict)
    assert isinstance(agent.moderation_cases, dict)
