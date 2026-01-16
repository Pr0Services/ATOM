"""
CHE·NU™ V68 - Team Collaboration Tests
Comprehensive test coverage for Slack/Teams killer

Test Categories:
- Workspaces (6 tests)
- Channels (10 tests)
- Messages (12 tests)
- Threads (4 tests)
- Reactions (3 tests)
- DMs (4 tests)
- Members (5 tests)
- Notifications (3 tests)
- Polls (4 tests)
- AI Features (6 tests)
- Dashboard (2 tests)
- Integration (3 tests)

Total: 62 tests
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from backend.spheres.collaboration.agents.collaboration_agent import (
    TeamCollaborationService,
    CollaborationAIEngine,
    Workspace,
    Channel,
    Message,
    DirectConversation,
    Thread,
    WorkspaceMember,
    Notification,
    Poll,
    ChannelType,
    MessageType,
    ConversationType,
    MemberRole,
    UserStatus,
    MessagePriority,
    SentimentType
)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def service():
    """Fresh service instance for each test"""
    return TeamCollaborationService()


@pytest.fixture
def ai_engine():
    """AI engine instance"""
    return CollaborationAIEngine()


@pytest.fixture
def workspace_with_data(service):
    """Workspace with channels, members, and messages"""
    # Create workspace
    ws = service.create_workspace("Test Corp", "owner_001", "Test workspace")
    
    # Add members
    service.add_member(ws.id, "user_002", "owner_001", "Alice")
    service.add_member(ws.id, "user_003", "owner_001", "Bob")
    
    # Create additional channel
    dev = service.create_channel(
        workspace_id=ws.id,
        name="development",
        created_by="owner_001",
        description="Dev discussions"
    )
    
    # Add messages
    msg1 = service.send_message(
        workspace_id=ws.id,
        channel_id=dev.id,
        sender_id="owner_001",
        content="Hello team!"
    )
    
    msg2 = service.send_message(
        workspace_id=ws.id,
        channel_id=dev.id,
        sender_id="user_002",
        content="Hi! Ready to work."
    )
    
    return {
        "workspace": ws,
        "channel": dev,
        "messages": [msg1, msg2],
        "members": ["owner_001", "user_002", "user_003"]
    }


# ============================================================
# WORKSPACE TESTS
# ============================================================

class TestWorkspaces:
    
    def test_create_workspace(self, service):
        """Test workspace creation"""
        ws = service.create_workspace(
            name="Acme Corp",
            owner_id="user_001",
            description="Main workspace"
        )
        
        assert ws.name == "Acme Corp"
        assert ws.owner_id == "user_001"
        assert ws.description == "Main workspace"
        assert ws.id is not None
    
    def test_workspace_creates_default_channel(self, service):
        """Test that workspace creates general channel"""
        ws = service.create_workspace("Test", "user_001")
        
        channels = service.list_channels(ws.id, "user_001")
        general = [c for c in channels if c.name == "general"]
        
        assert len(general) == 1
        assert general[0].is_default == True
    
    def test_workspace_adds_owner_as_member(self, service):
        """Test owner is automatically member"""
        ws = service.create_workspace("Test", "user_001")
        
        member = service.get_member(ws.id, "user_001")
        
        assert member is not None
        assert member.role == MemberRole.OWNER
    
    def test_get_workspace(self, service):
        """Test getting workspace by ID"""
        ws = service.create_workspace("Test", "user_001")
        
        retrieved = service.get_workspace(ws.id)
        
        assert retrieved.id == ws.id
        assert retrieved.name == "Test"
    
    def test_list_user_workspaces(self, service):
        """Test listing workspaces for user"""
        ws1 = service.create_workspace("Workspace 1", "user_001")
        ws2 = service.create_workspace("Workspace 2", "user_001")
        ws3 = service.create_workspace("Workspace 3", "user_002")
        
        user_workspaces = service.list_workspaces("user_001")
        
        assert len(user_workspaces) == 2
    
    def test_get_nonexistent_workspace(self, service):
        """Test getting workspace that doesn't exist"""
        ws = service.get_workspace("nonexistent")
        assert ws is None


# ============================================================
# CHANNEL TESTS
# ============================================================

class TestChannels:
    
    def test_create_public_channel(self, service, workspace_with_data):
        """Test creating public channel"""
        ws = workspace_with_data["workspace"]
        
        channel = service.create_channel(
            workspace_id=ws.id,
            name="Marketing",
            created_by="owner_001",
            channel_type=ChannelType.PUBLIC
        )
        
        assert channel.name == "marketing"  # Normalized
        assert channel.channel_type == ChannelType.PUBLIC
    
    def test_create_private_channel(self, service, workspace_with_data):
        """Test creating private channel"""
        ws = workspace_with_data["workspace"]
        
        channel = service.create_channel(
            workspace_id=ws.id,
            name="Secret Project",
            created_by="owner_001",
            channel_type=ChannelType.PRIVATE
        )
        
        assert channel.channel_type == ChannelType.PRIVATE
    
    def test_join_public_channel(self, service, workspace_with_data):
        """Test joining public channel"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        success = service.join_channel(channel.id, "user_003")
        
        assert success == True
        assert "user_003" in channel.member_ids
    
    def test_cannot_join_private_channel(self, service, workspace_with_data):
        """Test cannot join private channel directly"""
        ws = workspace_with_data["workspace"]
        
        private = service.create_channel(
            workspace_id=ws.id,
            name="private",
            created_by="owner_001",
            channel_type=ChannelType.PRIVATE
        )
        
        success = service.join_channel(private.id, "user_003")
        
        assert success == False
    
    def test_invite_to_private_channel(self, service, workspace_with_data):
        """Test inviting to private channel"""
        ws = workspace_with_data["workspace"]
        
        private = service.create_channel(
            workspace_id=ws.id,
            name="private",
            created_by="owner_001",
            channel_type=ChannelType.PRIVATE
        )
        
        success = service.invite_to_channel(private.id, "user_002", "owner_001")
        
        assert success == True
        assert "user_002" in private.member_ids
    
    def test_leave_channel(self, service, workspace_with_data):
        """Test leaving channel"""
        channel = workspace_with_data["channel"]
        
        service.join_channel(channel.id, "user_002")
        success = service.leave_channel(channel.id, "user_002")
        
        assert success == True
        assert "user_002" not in channel.member_ids
    
    def test_archive_channel(self, service, workspace_with_data):
        """Test archiving channel"""
        channel = workspace_with_data["channel"]
        
        success = service.archive_channel(channel.id, "owner_001")
        
        assert success == True
        assert channel.channel_type == ChannelType.ARCHIVED
    
    def test_cannot_archive_default_channel(self, service, workspace_with_data):
        """Test cannot archive default channel"""
        ws = workspace_with_data["workspace"]
        
        channels = service.list_channels(ws.id, "owner_001")
        general = [c for c in channels if c.name == "general"][0]
        
        success = service.archive_channel(general.id, "owner_001")
        
        assert success == False
    
    def test_set_channel_topic(self, service, workspace_with_data):
        """Test setting channel topic"""
        channel = workspace_with_data["channel"]
        
        success = service.set_channel_topic(channel.id, "Sprint 5 planning", "owner_001")
        
        assert success == True
        assert channel.topic == "Sprint 5 planning"
    
    def test_list_channels_respects_visibility(self, service, workspace_with_data):
        """Test listing channels respects private visibility"""
        ws = workspace_with_data["workspace"]
        
        # Create private channel without user_003
        private = service.create_channel(
            workspace_id=ws.id,
            name="private",
            created_by="owner_001",
            channel_type=ChannelType.PRIVATE
        )
        
        # user_003's view
        channels = service.list_channels(ws.id, "user_003")
        private_channels = [c for c in channels if c.name == "private"]
        
        assert len(private_channels) == 0


# ============================================================
# MESSAGE TESTS
# ============================================================

class TestMessages:
    
    def test_send_message(self, service, workspace_with_data):
        """Test sending message"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Test message"
        )
        
        assert msg.content == "Test message"
        assert msg.sender_id == "user_002"
        assert msg.channel_id == channel.id
    
    def test_message_extracts_mentions(self, service, workspace_with_data):
        """Test message extracts @mentions"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Hey <@user_001> and <@user_003>, check this!"
        )
        
        assert "user_001" in msg.mentions
        assert "user_003" in msg.mentions
    
    def test_edit_message(self, service, workspace_with_data):
        """Test editing message"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        edited = service.edit_message(msg.id, "Updated content", "owner_001")
        
        assert edited.content == "Updated content"
        assert edited.is_edited == True
    
    def test_cannot_edit_others_message(self, service, workspace_with_data):
        """Test cannot edit someone else's message"""
        messages = workspace_with_data["messages"]
        msg = messages[0]  # Sent by owner_001
        
        edited = service.edit_message(msg.id, "Hacked!", "user_002")
        
        assert edited is None
    
    def test_delete_message(self, service, workspace_with_data):
        """Test deleting message"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        success = service.delete_message(msg.id, "owner_001")
        
        assert success == True
        assert msg.is_deleted == True
    
    def test_list_messages(self, service, workspace_with_data):
        """Test listing messages"""
        channel = workspace_with_data["channel"]
        
        messages = service.list_messages(channel_id=channel.id, limit=10)
        
        assert len(messages) >= 2
    
    def test_pin_message(self, service, workspace_with_data):
        """Test pinning message"""
        messages = workspace_with_data["messages"]
        channel = workspace_with_data["channel"]
        msg = messages[0]
        
        success = service.pin_message(msg.id, "owner_001")
        
        assert success == True
        assert msg.is_pinned == True
        assert msg.id in channel.pinned_message_ids
    
    def test_unpin_message(self, service, workspace_with_data):
        """Test unpinning message"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        service.pin_message(msg.id, "owner_001")
        success = service.unpin_message(msg.id)
        
        assert success == True
        assert msg.is_pinned == False
    
    def test_search_messages(self, service, workspace_with_data):
        """Test searching messages"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        # Add searchable message
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="The deployment is scheduled for tomorrow"
        )
        
        results = service.search_messages(ws.id, "deployment", "owner_001")
        
        assert len(results) >= 1
    
    def test_search_respects_private_channels(self, service, workspace_with_data):
        """Test search respects private channel access"""
        ws = workspace_with_data["workspace"]
        
        # Create private channel
        private = service.create_channel(
            workspace_id=ws.id,
            name="secret",
            created_by="owner_001",
            channel_type=ChannelType.PRIVATE
        )
        
        # Message in private channel
        service.send_message(
            workspace_id=ws.id,
            channel_id=private.id,
            sender_id="owner_001",
            content="Secret deployment plan"
        )
        
        # user_003 cannot see it
        results = service.search_messages(ws.id, "Secret", "user_003")
        
        assert len(results) == 0
    
    def test_message_with_attachments(self, service, workspace_with_data):
        """Test message with attachments"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Here's the file",
            attachments=[{"filename": "report.pdf", "url": "https://example.com/report.pdf"}]
        )
        
        assert len(msg.attachments) == 1
        assert msg.attachments[0]["filename"] == "report.pdf"
    
    def test_get_message(self, service, workspace_with_data):
        """Test getting message by ID"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        retrieved = service.get_message(msg.id)
        
        assert retrieved.id == msg.id
        assert retrieved.content == msg.content


# ============================================================
# THREAD TESTS
# ============================================================

class TestThreads:
    
    def test_thread_created_on_reply(self, service, workspace_with_data):
        """Test thread created when replying"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        messages = workspace_with_data["messages"]
        parent = messages[0]
        
        reply = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="This is a reply",
            thread_id=parent.id
        )
        
        thread = service.get_thread(parent.id)
        
        assert thread is not None
        assert thread.reply_count == 1
        assert parent.reply_count == 1
    
    def test_thread_tracks_participants(self, service, workspace_with_data):
        """Test thread tracks participants"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        messages = workspace_with_data["messages"]
        parent = messages[0]
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Reply 1",
            thread_id=parent.id
        )
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_003",
            content="Reply 2",
            thread_id=parent.id
        )
        
        thread = service.get_thread(parent.id)
        
        assert "user_002" in thread.participant_ids
        assert "user_003" in thread.participant_ids
    
    def test_get_thread_replies(self, service, workspace_with_data):
        """Test getting thread replies"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        messages = workspace_with_data["messages"]
        parent = messages[0]
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Reply 1",
            thread_id=parent.id
        )
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_003",
            content="Reply 2",
            thread_id=parent.id
        )
        
        replies = service.get_thread_replies(parent.id)
        
        assert len(replies) == 2
    
    def test_thread_replies_excluded_from_channel(self, service, workspace_with_data):
        """Test thread replies not in main channel listing"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        messages = workspace_with_data["messages"]
        parent = messages[0]
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="user_002",
            content="Thread reply",
            thread_id=parent.id
        )
        
        channel_messages = service.list_messages(channel_id=channel.id)
        thread_replies = [m for m in channel_messages if m.thread_id == parent.id]
        
        assert len(thread_replies) == 0


# ============================================================
# REACTION TESTS
# ============================================================

class TestReactions:
    
    def test_add_reaction(self, service, workspace_with_data):
        """Test adding reaction"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        success = service.add_reaction(msg.id, "user_002", "👍")
        
        assert success == True
        assert "👍" in msg.reactions
        assert "user_002" in msg.reactions["👍"]
    
    def test_multiple_reactions_same_emoji(self, service, workspace_with_data):
        """Test multiple users can react with same emoji"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        service.add_reaction(msg.id, "user_002", "👍")
        service.add_reaction(msg.id, "user_003", "👍")
        
        assert len(msg.reactions["👍"]) == 2
    
    def test_remove_reaction(self, service, workspace_with_data):
        """Test removing reaction"""
        messages = workspace_with_data["messages"]
        msg = messages[0]
        
        service.add_reaction(msg.id, "user_002", "👍")
        success = service.remove_reaction(msg.id, "user_002", "👍")
        
        assert success == True
        assert "👍" not in msg.reactions


# ============================================================
# DM TESTS
# ============================================================

class TestDirectMessages:
    
    def test_create_dm(self, service, workspace_with_data):
        """Test creating DM conversation"""
        ws = workspace_with_data["workspace"]
        
        dm = service.create_dm(ws.id, ["owner_001", "user_002"])
        
        assert dm.conversation_type == ConversationType.DIRECT
        assert len(dm.participant_ids) == 2
    
    def test_create_group_dm(self, service, workspace_with_data):
        """Test creating group DM"""
        ws = workspace_with_data["workspace"]
        
        dm = service.create_dm(ws.id, ["owner_001", "user_002", "user_003"])
        
        assert dm.conversation_type == ConversationType.GROUP_DM
        assert len(dm.participant_ids) == 3
    
    def test_dm_deduplication(self, service, workspace_with_data):
        """Test DM with same participants returns existing"""
        ws = workspace_with_data["workspace"]
        
        dm1 = service.create_dm(ws.id, ["owner_001", "user_002"])
        dm2 = service.create_dm(ws.id, ["user_002", "owner_001"])  # Same, different order
        
        assert dm1.id == dm2.id
    
    def test_send_dm(self, service, workspace_with_data):
        """Test sending DM"""
        ws = workspace_with_data["workspace"]
        
        dm = service.create_dm(ws.id, ["owner_001", "user_002"])
        msg = service.send_message(
            workspace_id=ws.id,
            conversation_id=dm.id,
            sender_id="owner_001",
            content="Hey, quick question"
        )
        
        assert msg.conversation_id == dm.id


# ============================================================
# MEMBER TESTS
# ============================================================

class TestMembers:
    
    def test_add_member(self, service, workspace_with_data):
        """Test adding member"""
        ws = workspace_with_data["workspace"]
        
        member = service.add_member(
            workspace_id=ws.id,
            user_id="new_user",
            added_by="owner_001",
            display_name="New User"
        )
        
        assert member.display_name == "New User"
        assert member.role == MemberRole.MEMBER
    
    def test_new_member_joins_default_channels(self, service, workspace_with_data):
        """Test new member auto-joins default channels"""
        ws = workspace_with_data["workspace"]
        
        service.add_member(ws.id, "new_user", "owner_001")
        
        channels = service.list_channels(ws.id, "new_user")
        general = [c for c in channels if c.name == "general"]
        
        assert len(general) == 1
    
    def test_update_member_status(self, service, workspace_with_data):
        """Test updating member status"""
        ws = workspace_with_data["workspace"]
        
        member = service.update_member_status(
            workspace_id=ws.id,
            user_id="owner_001",
            status=UserStatus.DND,
            status_text="In a meeting",
            status_emoji="🔴"
        )
        
        assert member.status == UserStatus.DND
        assert member.status_text == "In a meeting"
    
    def test_list_members(self, service, workspace_with_data):
        """Test listing members"""
        ws = workspace_with_data["workspace"]
        
        members = service.list_members(ws.id)
        
        assert len(members) == 3  # owner + 2 added
    
    def test_remove_member(self, service, workspace_with_data):
        """Test removing member"""
        ws = workspace_with_data["workspace"]
        
        success = service.remove_member(ws.id, "user_002", "owner_001")
        
        assert success == True
        assert service.get_member(ws.id, "user_002") is None


# ============================================================
# NOTIFICATION TESTS
# ============================================================

class TestNotifications:
    
    def test_mention_creates_notification(self, service, workspace_with_data):
        """Test @mention creates notification"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="owner_001",
            content="Hey <@user_002> check this!"
        )
        
        notifications = service.get_notifications("user_002")
        mention_notifications = [n for n in notifications if n.notification_type == "mention"]
        
        assert len(mention_notifications) >= 1
    
    def test_mark_notification_read(self, service, workspace_with_data):
        """Test marking notification as read"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="owner_001",
            content="<@user_002> important!"
        )
        
        notifications = service.get_notifications("user_002")
        notification = notifications[0]
        
        success = service.mark_notification_read(notification.id, "user_002")
        
        assert success == True
        assert notification.is_read == True
    
    def test_mark_all_notifications_read(self, service, workspace_with_data):
        """Test marking all notifications as read"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        # Create multiple notifications
        service.send_message(ws.id, channel_id=channel.id, sender_id="owner_001", content="<@user_002> msg 1")
        service.send_message(ws.id, channel_id=channel.id, sender_id="owner_001", content="<@user_002> msg 2")
        
        count = service.mark_all_notifications_read("user_002")
        
        assert count >= 2
        
        unread = service.get_notifications("user_002", unread_only=True)
        assert len(unread) == 0


# ============================================================
# POLL TESTS
# ============================================================

class TestPolls:
    
    def test_create_poll(self, service, workspace_with_data):
        """Test creating poll"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="owner_001",
            content="Vote time!"
        )
        
        poll = service.create_poll(
            message_id=msg.id,
            question="Best framework?",
            options=["React", "Vue", "Angular"]
        )
        
        assert poll.question == "Best framework?"
        assert len(poll.options) == 3
    
    def test_vote_in_poll(self, service, workspace_with_data):
        """Test voting in poll"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(ws.id, channel_id=channel.id, sender_id="owner_001", content="Poll")
        poll = service.create_poll(msg.id, "Favorite?", ["A", "B", "C"])
        
        success = service.vote_poll(poll.id, "user_002", "B")
        
        assert success == True
        assert "user_002" in poll.votes["B"]
    
    def test_single_vote_poll(self, service, workspace_with_data):
        """Test single choice poll replaces vote"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(ws.id, channel_id=channel.id, sender_id="owner_001", content="Poll")
        poll = service.create_poll(msg.id, "Pick one", ["A", "B", "C"], is_multiple_choice=False)
        
        service.vote_poll(poll.id, "user_002", "A")
        service.vote_poll(poll.id, "user_002", "B")
        
        assert "user_002" not in poll.votes["A"]
        assert "user_002" in poll.votes["B"]
    
    def test_get_poll_results(self, service, workspace_with_data):
        """Test getting poll results"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        msg = service.send_message(ws.id, channel_id=channel.id, sender_id="owner_001", content="Poll")
        poll = service.create_poll(msg.id, "Vote", ["X", "Y", "Z"])
        
        service.vote_poll(poll.id, "owner_001", "X")
        service.vote_poll(poll.id, "user_002", "X")
        service.vote_poll(poll.id, "user_003", "Y")
        
        results = service.get_poll_results(poll.id)
        
        assert results["options"]["X"]["count"] == 2
        assert results["options"]["Y"]["count"] == 1
        assert results["total_votes"] == 3


# ============================================================
# AI FEATURE TESTS
# ============================================================

class TestAIFeatures:
    
    def test_analyze_message_priority(self, ai_engine):
        """Test AI detects message priority"""
        msg = Message(
            workspace_id="ws_001",
            channel_id="ch_001",
            sender_id="user_001",
            content="URGENT: We need to fix the production bug ASAP!"
        )
        
        analysis = ai_engine.analyze_message(msg)
        
        assert analysis.priority == MessagePriority.URGENT
    
    def test_analyze_message_sentiment(self, ai_engine):
        """Test AI detects sentiment"""
        positive_msg = Message(
            workspace_id="ws_001",
            channel_id="ch_001",
            sender_id="user_001",
            content="Great job team! The launch was awesome and the results are excellent!"
        )
        
        negative_msg = Message(
            workspace_id="ws_001",
            channel_id="ch_001",
            sender_id="user_001",
            content="We have a serious problem. The deployment failed and everything is broken."
        )
        
        pos_analysis = ai_engine.analyze_message(positive_msg)
        neg_analysis = ai_engine.analyze_message(negative_msg)
        
        assert pos_analysis.sentiment == SentimentType.POSITIVE
        assert neg_analysis.sentiment == SentimentType.NEGATIVE
    
    def test_extract_action_items(self, ai_engine):
        """Test AI extracts action items"""
        msg = Message(
            workspace_id="ws_001",
            channel_id="ch_001",
            sender_id="user_001",
            content="Please review the PR before end of day. Can you update the docs too?"
        )
        
        analysis = ai_engine.analyze_message(msg)
        
        assert len(analysis.action_items) > 0
    
    def test_extract_questions(self, ai_engine):
        """Test AI extracts questions"""
        msg = Message(
            workspace_id="ws_001",
            channel_id="ch_001",
            sender_id="user_001",
            content="What time is the meeting? Who should I talk to about this?"
        )
        
        analysis = ai_engine.analyze_message(msg)
        
        assert len(analysis.questions) >= 1  # At least 1 question detected
    
    def test_channel_summary(self, service, workspace_with_data):
        """Test AI channel summary"""
        channel = workspace_with_data["channel"]
        
        summary = service.get_channel_summary(channel.id, period_hours=24)
        
        assert summary is not None
        assert summary.message_count >= 2
    
    def test_smart_replies(self, service, workspace_with_data):
        """Test AI smart replies"""
        messages = workspace_with_data["messages"]
        
        replies = service.get_smart_replies(messages[0].id)
        
        assert len(replies) > 0
        assert all(r.suggestion != "" for r in replies)


# ============================================================
# DASHBOARD TESTS
# ============================================================

class TestDashboard:
    
    def test_get_dashboard(self, service, workspace_with_data):
        """Test getting dashboard data"""
        ws = workspace_with_data["workspace"]
        
        dashboard = service.get_dashboard(ws.id, "owner_001")
        
        assert dashboard["workspace_id"] == ws.id
        assert dashboard["channels_count"] >= 2
        assert dashboard["members_count"] == 3
    
    def test_dashboard_recent_activity(self, service, workspace_with_data):
        """Test dashboard includes recent activity"""
        ws = workspace_with_data["workspace"]
        
        dashboard = service.get_dashboard(ws.id, "owner_001")
        
        assert "recent_activity" in dashboard
        assert len(dashboard["recent_activity"]) > 0


# ============================================================
# INTEGRATION TESTS
# ============================================================

class TestIntegration:
    
    def test_full_conversation_flow(self, service):
        """Test complete conversation flow"""
        # Create workspace
        ws = service.create_workspace("Test Company", "ceo_001")
        
        # Add team
        service.add_member(ws.id, "dev_001", "ceo_001", "Developer")
        service.add_member(ws.id, "pm_001", "ceo_001", "PM")
        
        # Create channel
        channel = service.create_channel(
            workspace_id=ws.id,
            name="project-x",
            created_by="pm_001"
        )
        
        # Start conversation
        msg1 = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="pm_001",
            content="Hey team, we have an urgent deadline! <@dev_001> can you help?"
        )
        
        # Developer replies
        msg2 = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="dev_001",
            content="Sure! I'm on it."
        )
        
        # Thread discussion
        reply1 = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="pm_001",
            content="Great! Here are the specs...",
            thread_id=msg1.id
        )
        
        # Add reactions
        service.add_reaction(msg2.id, "pm_001", "🙏")
        
        # Verify state
        messages = service.list_messages(channel_id=channel.id)
        # Filter out system messages for assertion
        user_messages = [m for m in messages if m.message_type != MessageType.SYSTEM]
        thread = service.get_thread(msg1.id)
        notifications = service.get_notifications("dev_001")
        
        assert len(user_messages) == 2  # Thread replies not in main (excludes system msgs)
        assert thread.reply_count == 1
        assert len(notifications) >= 1  # Got mentioned
    
    def test_dm_to_channel_workflow(self, service, workspace_with_data):
        """Test DM leading to channel message"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        # Private DM discussion
        dm = service.create_dm(ws.id, ["owner_001", "user_002"])
        service.send_message(
            workspace_id=ws.id,
            conversation_id=dm.id,
            sender_id="owner_001",
            content="Should we announce this in the channel?"
        )
        
        # Then announce in channel
        announcement = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="owner_001",
            content="Team announcement: Big news coming!"
        )
        
        # Pin announcement
        service.pin_message(announcement.id, "owner_001")
        
        # Verify
        assert announcement.is_pinned == True
        assert dm.conversation_type == ConversationType.DIRECT
    
    def test_ai_workflow(self, service, workspace_with_data):
        """Test AI features in workflow"""
        ws = workspace_with_data["workspace"]
        channel = workspace_with_data["channel"]
        
        # Send urgent message
        urgent = service.send_message(
            workspace_id=ws.id,
            channel_id=channel.id,
            sender_id="owner_001",
            content="URGENT: Production is down! We need to fix this immediately!"
        )
        
        # AI analysis
        analysis = service.analyze_message(urgent.id)
        
        # Get important messages
        important = service.get_important_messages(channel.id)
        
        # Get summary
        summary = service.get_channel_summary(channel.id)
        
        assert analysis.priority == MessagePriority.URGENT
        assert any(m.id == urgent.id for m in important)
        assert summary.message_count > 0


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
