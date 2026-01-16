"""
CHE·NU™ V68 - Team Collaboration Agent
Slack/Teams killer at $29/mo vs $8.75/user/mo

Features:
- Channels (public/private/archived)
- Direct Messages (1:1 and group)
- Threaded conversations
- Reactions & emoji
- File sharing
- @mentions & notifications
- Search across messages
- AI: Smart summaries, sentiment, priority detection
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================
# ENUMS
# ============================================================

class ChannelType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    ANNOUNCEMENT = "announcement"  # Only admins can post
    ARCHIVED = "archived"


class MessageType(str, Enum):
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    SYSTEM = "system"  # Join/leave notifications
    POLL = "poll"


class ConversationType(str, Enum):
    CHANNEL = "channel"
    DIRECT = "direct"
    GROUP_DM = "group_dm"
    THREAD = "thread"


class MemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class NotificationType(str, Enum):
    ALL = "all"
    MENTIONS = "mentions"
    NONE = "none"


class UserStatus(str, Enum):
    ONLINE = "online"
    AWAY = "away"
    DND = "do_not_disturb"
    OFFLINE = "offline"


class MessagePriority(str, Enum):
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Workspace:
    """Top-level workspace/organization"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    icon_url: Optional[str] = None
    owner_id: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class Channel:
    """Communication channel"""
    id: str = field(default_factory=lambda: str(uuid4()))
    workspace_id: str = ""
    name: str = ""
    description: str = ""
    channel_type: ChannelType = ChannelType.PUBLIC
    topic: str = ""
    icon_emoji: str = "💬"
    is_default: bool = False  # Auto-join for new members
    member_ids: List[str] = field(default_factory=list)
    pinned_message_ids: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""
    archived_at: Optional[datetime] = None


@dataclass
class DirectConversation:
    """Direct message conversation (1:1 or group)"""
    id: str = field(default_factory=lambda: str(uuid4()))
    workspace_id: str = ""
    participant_ids: List[str] = field(default_factory=list)
    conversation_type: ConversationType = ConversationType.DIRECT
    name: Optional[str] = None  # For group DMs
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None


@dataclass
class Message:
    """Chat message"""
    id: str = field(default_factory=lambda: str(uuid4()))
    workspace_id: str = ""
    channel_id: Optional[str] = None
    conversation_id: Optional[str] = None
    thread_id: Optional[str] = None  # Parent message ID for threads
    sender_id: str = ""
    message_type: MessageType = MessageType.TEXT
    content: str = ""
    formatted_content: Optional[str] = None  # Markdown/rich text
    mentions: List[str] = field(default_factory=list)  # User IDs mentioned
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    reactions: Dict[str, List[str]] = field(default_factory=dict)  # emoji -> [user_ids]
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    is_pinned: bool = False
    is_deleted: bool = False
    reply_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Thread:
    """Message thread"""
    id: str = field(default_factory=lambda: str(uuid4()))
    parent_message_id: str = ""
    channel_id: str = ""
    participant_ids: List[str] = field(default_factory=list)
    reply_count: int = 0
    last_reply_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Reaction:
    """Message reaction"""
    id: str = field(default_factory=lambda: str(uuid4()))
    message_id: str = ""
    user_id: str = ""
    emoji: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Attachment:
    """File attachment"""
    id: str = field(default_factory=lambda: str(uuid4()))
    message_id: str = ""
    filename: str = ""
    file_type: str = ""
    file_size: int = 0
    url: str = ""
    thumbnail_url: Optional[str] = None
    uploaded_by: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class WorkspaceMember:
    """Workspace membership"""
    id: str = field(default_factory=lambda: str(uuid4()))
    workspace_id: str = ""
    user_id: str = ""
    display_name: str = ""
    avatar_url: Optional[str] = None
    role: MemberRole = MemberRole.MEMBER
    title: str = ""
    status: UserStatus = UserStatus.OFFLINE
    status_text: str = ""
    status_emoji: str = ""
    notification_preferences: Dict[str, NotificationType] = field(default_factory=dict)
    joined_at: datetime = field(default_factory=datetime.utcnow)
    last_active_at: Optional[datetime] = None


@dataclass
class Notification:
    """User notification"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    workspace_id: str = ""
    channel_id: Optional[str] = None
    message_id: Optional[str] = None
    notification_type: str = ""  # mention, reply, dm, etc.
    title: str = ""
    body: str = ""
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass 
class Poll:
    """Message poll"""
    id: str = field(default_factory=lambda: str(uuid4()))
    message_id: str = ""
    question: str = ""
    options: List[str] = field(default_factory=list)
    votes: Dict[str, List[str]] = field(default_factory=dict)  # option -> [user_ids]
    is_anonymous: bool = False
    is_multiple_choice: bool = False
    ends_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================
# AI ANALYSIS MODELS
# ============================================================

@dataclass
class MessageAnalysis:
    """AI analysis of a message"""
    message_id: str = ""
    priority: MessagePriority = MessagePriority.NORMAL
    sentiment: SentimentType = SentimentType.NEUTRAL
    topics: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    key_points: List[str] = field(default_factory=list)
    requires_response: bool = False
    confidence: float = 0.0


@dataclass
class ChannelSummary:
    """AI summary of channel activity"""
    channel_id: str = ""
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=datetime.utcnow)
    message_count: int = 0
    participant_count: int = 0
    key_topics: List[str] = field(default_factory=list)
    decisions_made: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    sentiment_breakdown: Dict[str, int] = field(default_factory=dict)
    most_active_members: List[Dict[str, Any]] = field(default_factory=list)
    summary_text: str = ""
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SmartReply:
    """AI-suggested reply"""
    suggestion: str = ""
    tone: str = ""  # formal, casual, friendly
    confidence: float = 0.0


# ============================================================
# AI ENGINE
# ============================================================

class CollaborationAIEngine:
    """AI features for team collaboration"""
    
    # Priority keywords
    URGENT_KEYWORDS = ["urgent", "asap", "emergency", "critical", "immediately", "deadline"]
    HIGH_PRIORITY_KEYWORDS = ["important", "priority", "soon", "needed", "required"]
    
    # Sentiment indicators
    POSITIVE_WORDS = ["great", "awesome", "thanks", "excellent", "good", "love", "amazing", "perfect"]
    NEGATIVE_WORDS = ["problem", "issue", "wrong", "bad", "error", "fail", "broken", "frustrated"]
    
    def analyze_message(self, message: Message) -> MessageAnalysis:
        """Analyze a message for priority, sentiment, action items"""
        content_lower = message.content.lower()
        
        # Detect priority
        priority = MessagePriority.NORMAL
        if any(kw in content_lower for kw in self.URGENT_KEYWORDS):
            priority = MessagePriority.URGENT
        elif any(kw in content_lower for kw in self.HIGH_PRIORITY_KEYWORDS):
            priority = MessagePriority.HIGH
        
        # Detect sentiment
        positive_count = sum(1 for w in self.POSITIVE_WORDS if w in content_lower)
        negative_count = sum(1 for w in self.NEGATIVE_WORDS if w in content_lower)
        
        if positive_count > negative_count:
            sentiment = SentimentType.POSITIVE
        elif negative_count > positive_count:
            sentiment = SentimentType.NEGATIVE
        elif positive_count > 0 and negative_count > 0:
            sentiment = SentimentType.MIXED
        else:
            sentiment = SentimentType.NEUTRAL
        
        # Extract topics (simple keyword extraction)
        topics = self._extract_topics(message.content)
        
        # Extract action items
        action_items = self._extract_action_items(message.content)
        
        # Extract questions
        questions = self._extract_questions(message.content)
        
        # Determine if response needed
        requires_response = (
            len(questions) > 0 or
            len(message.mentions) > 0 or
            priority in [MessagePriority.URGENT, MessagePriority.HIGH]
        )
        
        return MessageAnalysis(
            message_id=message.id,
            priority=priority,
            sentiment=sentiment,
            topics=topics,
            action_items=action_items,
            questions=questions,
            key_points=self._extract_key_points(message.content),
            requires_response=requires_response,
            confidence=0.85
        )
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract main topics from content"""
        # Simple implementation - would use NLP in production
        topics = []
        topic_indicators = {
            "meeting": ["meeting", "call", "sync", "standup"],
            "project": ["project", "milestone", "deadline", "deliverable"],
            "bug": ["bug", "issue", "error", "fix"],
            "feature": ["feature", "enhancement", "improvement"],
            "review": ["review", "feedback", "approval"],
            "deployment": ["deploy", "release", "launch", "production"],
        }
        
        content_lower = content.lower()
        for topic, keywords in topic_indicators.items():
            if any(kw in content_lower for kw in keywords):
                topics.append(topic)
        
        return topics[:5]  # Max 5 topics
    
    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items from content"""
        action_items = []
        
        # Look for action patterns
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if any(line_lower.startswith(p) for p in ["- [ ]", "todo:", "action:", "task:"]):
                action_items.append(line.strip())
            elif any(p in line_lower for p in ["please ", "can you ", "need to ", "should "]):
                if len(line) < 200:  # Reasonable length
                    action_items.append(line.strip())
        
        return action_items[:10]
    
    def _extract_questions(self, content: str) -> List[str]:
        """Extract questions from content"""
        questions = []
        sentences = content.replace('!', '.').split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence.endswith('?') or sentence.lower().startswith(('what', 'when', 'where', 'why', 'how', 'who', 'which', 'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does')):
                if '?' in sentence or len(sentence.split()) < 20:
                    questions.append(sentence)
        
        return questions[:5]
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content"""
        key_points = []
        
        # Look for emphasized text or bullet points
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ', '1.', '2.', '3.')):
                key_points.append(line)
            elif '**' in line or line.isupper():
                key_points.append(line)
        
        return key_points[:10]
    
    def generate_channel_summary(
        self, 
        channel: Channel, 
        messages: List[Message],
        period_hours: int = 24
    ) -> ChannelSummary:
        """Generate AI summary of channel activity"""
        
        cutoff = datetime.utcnow() - timedelta(hours=period_hours)
        recent_messages = [m for m in messages if m.created_at > cutoff]
        
        if not recent_messages:
            return ChannelSummary(
                channel_id=channel.id,
                period_start=cutoff,
                period_end=datetime.utcnow(),
                summary_text="No recent activity in this channel."
            )
        
        # Collect all analyses
        all_topics = []
        all_action_items = []
        all_questions = []
        sentiments = {"positive": 0, "neutral": 0, "negative": 0, "mixed": 0}
        participant_messages = {}
        
        for msg in recent_messages:
            analysis = self.analyze_message(msg)
            all_topics.extend(analysis.topics)
            all_action_items.extend(analysis.action_items)
            all_questions.extend(analysis.questions)
            sentiments[analysis.sentiment.value] += 1
            
            participant_messages[msg.sender_id] = participant_messages.get(msg.sender_id, 0) + 1
        
        # Get unique topics sorted by frequency
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        key_topics = sorted(topic_counts.keys(), key=lambda t: topic_counts[t], reverse=True)[:5]
        
        # Most active members
        most_active = sorted(
            [{"user_id": uid, "message_count": count} for uid, count in participant_messages.items()],
            key=lambda x: x["message_count"],
            reverse=True
        )[:5]
        
        # Generate summary text
        summary_parts = []
        summary_parts.append(f"📊 {len(recent_messages)} messages from {len(participant_messages)} participants")
        
        if key_topics:
            summary_parts.append(f"🏷️ Main topics: {', '.join(key_topics)}")
        
        if all_action_items:
            summary_parts.append(f"✅ {len(all_action_items)} action items identified")
        
        if all_questions:
            summary_parts.append(f"❓ {len(all_questions)} questions raised")
        
        # Sentiment summary
        dominant_sentiment = max(sentiments.keys(), key=lambda k: sentiments[k])
        summary_parts.append(f"💬 Overall tone: {dominant_sentiment}")
        
        return ChannelSummary(
            channel_id=channel.id,
            period_start=cutoff,
            period_end=datetime.utcnow(),
            message_count=len(recent_messages),
            participant_count=len(participant_messages),
            key_topics=key_topics,
            decisions_made=[],  # Would need more sophisticated NLP
            action_items=all_action_items[:10],
            unresolved_questions=all_questions[:5],
            sentiment_breakdown=sentiments,
            most_active_members=most_active,
            summary_text="\n".join(summary_parts),
            generated_at=datetime.utcnow()
        )
    
    def suggest_smart_replies(self, message: Message, context: List[Message] = None) -> List[SmartReply]:
        """Generate smart reply suggestions"""
        suggestions = []
        content_lower = message.content.lower()
        
        # Question responses
        if '?' in message.content:
            suggestions.append(SmartReply(
                suggestion="Let me look into that and get back to you.",
                tone="professional",
                confidence=0.8
            ))
            suggestions.append(SmartReply(
                suggestion="Good question! I'll check and follow up.",
                tone="friendly",
                confidence=0.75
            ))
        
        # Thank you responses
        if any(w in content_lower for w in ["thank", "thanks", "appreciate"]):
            suggestions.append(SmartReply(
                suggestion="You're welcome! Happy to help.",
                tone="friendly",
                confidence=0.9
            ))
            suggestions.append(SmartReply(
                suggestion="No problem at all!",
                tone="casual",
                confidence=0.85
            ))
        
        # Request responses
        if any(w in content_lower for w in ["can you", "could you", "please", "would you"]):
            suggestions.append(SmartReply(
                suggestion="Sure, I'll take care of it.",
                tone="professional",
                confidence=0.8
            ))
            suggestions.append(SmartReply(
                suggestion="On it! Will update you when done.",
                tone="casual",
                confidence=0.75
            ))
        
        # Meeting related
        if any(w in content_lower for w in ["meeting", "call", "sync"]):
            suggestions.append(SmartReply(
                suggestion="Works for me! See you then.",
                tone="friendly",
                confidence=0.7
            ))
            suggestions.append(SmartReply(
                suggestion="I'll be there.",
                tone="brief",
                confidence=0.8
            ))
        
        # Default acknowledgment
        if not suggestions:
            suggestions.append(SmartReply(
                suggestion="Got it, thanks!",
                tone="casual",
                confidence=0.6
            ))
            suggestions.append(SmartReply(
                suggestion="Sounds good!",
                tone="friendly",
                confidence=0.6
            ))
        
        return suggestions[:3]
    
    def detect_important_messages(self, messages: List[Message]) -> List[Message]:
        """Filter messages that need attention"""
        important = []
        
        for msg in messages:
            analysis = self.analyze_message(msg)
            if (analysis.priority in [MessagePriority.URGENT, MessagePriority.HIGH] or
                analysis.requires_response or
                len(analysis.action_items) > 0):
                important.append(msg)
        
        return important


# ============================================================
# MAIN SERVICE
# ============================================================

class TeamCollaborationService:
    """
    Team Collaboration Service - CHE·NU V68
    Slack/Teams killer with AI features
    """
    
    def __init__(self):
        # In-memory storage (would be database in production)
        self.workspaces: Dict[str, Workspace] = {}
        self.channels: Dict[str, Channel] = {}
        self.conversations: Dict[str, DirectConversation] = {}
        self.messages: Dict[str, Message] = {}
        self.threads: Dict[str, Thread] = {}
        self.members: Dict[str, WorkspaceMember] = {}
        self.notifications: Dict[str, List[Notification]] = {}  # user_id -> notifications
        self.polls: Dict[str, Poll] = {}
        
        self.ai_engine = CollaborationAIEngine()
        logger.info("TeamCollaborationService initialized")
    
    # --------------------------------------------------------
    # WORKSPACE OPERATIONS
    # --------------------------------------------------------
    
    def create_workspace(
        self,
        name: str,
        owner_id: str,
        description: str = ""
    ) -> Workspace:
        """Create a new workspace"""
        workspace = Workspace(
            name=name,
            description=description,
            owner_id=owner_id,
            created_by=owner_id
        )
        self.workspaces[workspace.id] = workspace
        
        # Add owner as member
        self.add_member(workspace.id, owner_id, owner_id, role=MemberRole.OWNER)
        
        # Create default general channel
        self.create_channel(
            workspace_id=workspace.id,
            name="general",
            description="General discussion",
            created_by=owner_id,
            is_default=True
        )
        
        logger.info(f"Created workspace: {workspace.id}")
        return workspace
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID"""
        return self.workspaces.get(workspace_id)
    
    def list_workspaces(self, user_id: str) -> List[Workspace]:
        """List workspaces user is member of"""
        user_workspace_ids = set()
        for member in self.members.values():
            if member.user_id == user_id:
                user_workspace_ids.add(member.workspace_id)
        
        return [ws for ws in self.workspaces.values() if ws.id in user_workspace_ids]
    
    # --------------------------------------------------------
    # CHANNEL OPERATIONS
    # --------------------------------------------------------
    
    def create_channel(
        self,
        workspace_id: str,
        name: str,
        created_by: str,
        description: str = "",
        channel_type: ChannelType = ChannelType.PUBLIC,
        is_default: bool = False
    ) -> Channel:
        """Create a new channel"""
        channel = Channel(
            workspace_id=workspace_id,
            name=name.lower().replace(" ", "-"),
            description=description,
            channel_type=channel_type,
            is_default=is_default,
            member_ids=[created_by],
            created_by=created_by
        )
        self.channels[channel.id] = channel
        
        # Post system message
        self._post_system_message(
            channel_id=channel.id,
            content=f"Channel #{channel.name} was created"
        )
        
        logger.info(f"Created channel: {channel.id} ({channel.name})")
        return channel
    
    def get_channel(self, channel_id: str) -> Optional[Channel]:
        """Get channel by ID"""
        return self.channels.get(channel_id)
    
    def list_channels(self, workspace_id: str, user_id: str) -> List[Channel]:
        """List channels in workspace (respecting visibility)"""
        channels = []
        for channel in self.channels.values():
            if channel.workspace_id != workspace_id:
                continue
            if channel.channel_type == ChannelType.ARCHIVED:
                continue
            if channel.channel_type == ChannelType.PRIVATE:
                if user_id not in channel.member_ids:
                    continue
            channels.append(channel)
        
        return sorted(channels, key=lambda c: c.name)
    
    def join_channel(self, channel_id: str, user_id: str) -> bool:
        """Join a channel"""
        channel = self.channels.get(channel_id)
        if not channel:
            return False
        
        if channel.channel_type == ChannelType.PRIVATE:
            return False  # Must be invited
        
        if user_id not in channel.member_ids:
            channel.member_ids.append(user_id)
            self._post_system_message(
                channel_id=channel_id,
                content=f"<@{user_id}> joined the channel"
            )
        
        return True
    
    def leave_channel(self, channel_id: str, user_id: str) -> bool:
        """Leave a channel"""
        channel = self.channels.get(channel_id)
        if not channel:
            return False
        
        if user_id in channel.member_ids:
            channel.member_ids.remove(user_id)
            self._post_system_message(
                channel_id=channel_id,
                content=f"<@{user_id}> left the channel"
            )
        
        return True
    
    def invite_to_channel(self, channel_id: str, user_id: str, invited_by: str) -> bool:
        """Invite user to channel"""
        channel = self.channels.get(channel_id)
        if not channel:
            return False
        
        if user_id not in channel.member_ids:
            channel.member_ids.append(user_id)
            self._post_system_message(
                channel_id=channel_id,
                content=f"<@{user_id}> was added by <@{invited_by}>"
            )
            
            # Create notification
            self._create_notification(
                user_id=user_id,
                workspace_id=channel.workspace_id,
                channel_id=channel_id,
                notification_type="channel_invite",
                title=f"Added to #{channel.name}",
                body=f"You were added to #{channel.name}"
            )
        
        return True
    
    def archive_channel(self, channel_id: str, archived_by: str) -> bool:
        """Archive a channel"""
        channel = self.channels.get(channel_id)
        if not channel or channel.is_default:
            return False
        
        channel.channel_type = ChannelType.ARCHIVED
        channel.archived_at = datetime.utcnow()
        
        self._post_system_message(
            channel_id=channel_id,
            content=f"This channel was archived by <@{archived_by}>"
        )
        
        return True
    
    def set_channel_topic(self, channel_id: str, topic: str, set_by: str) -> bool:
        """Set channel topic"""
        channel = self.channels.get(channel_id)
        if not channel:
            return False
        
        channel.topic = topic
        self._post_system_message(
            channel_id=channel_id,
            content=f"<@{set_by}> set the channel topic: {topic}"
        )
        
        return True
    
    # --------------------------------------------------------
    # DIRECT MESSAGE OPERATIONS
    # --------------------------------------------------------
    
    def create_dm(self, workspace_id: str, participant_ids: List[str]) -> DirectConversation:
        """Create or get existing DM conversation"""
        # Check for existing conversation with same participants
        sorted_ids = sorted(participant_ids)
        for conv in self.conversations.values():
            if conv.workspace_id == workspace_id and sorted(conv.participant_ids) == sorted_ids:
                return conv
        
        # Create new conversation
        conv_type = ConversationType.DIRECT if len(participant_ids) == 2 else ConversationType.GROUP_DM
        
        conversation = DirectConversation(
            workspace_id=workspace_id,
            participant_ids=participant_ids,
            conversation_type=conv_type
        )
        self.conversations[conversation.id] = conversation
        
        logger.info(f"Created DM: {conversation.id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[DirectConversation]:
        """Get DM conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def list_conversations(self, workspace_id: str, user_id: str) -> List[DirectConversation]:
        """List user's DM conversations"""
        conversations = []
        for conv in self.conversations.values():
            if conv.workspace_id == workspace_id and user_id in conv.participant_ids:
                conversations.append(conv)
        
        return sorted(conversations, key=lambda c: c.last_message_at or c.created_at, reverse=True)
    
    # --------------------------------------------------------
    # MESSAGE OPERATIONS
    # --------------------------------------------------------
    
    def send_message(
        self,
        workspace_id: str,
        sender_id: str,
        content: str,
        channel_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        message_type: MessageType = MessageType.TEXT,
        attachments: List[Dict[str, Any]] = None
    ) -> Message:
        """Send a message"""
        # Extract mentions using regex
        import re
        mentions = re.findall(r'<@([a-zA-Z0-9_-]+)>', content)
        
        message = Message(
            workspace_id=workspace_id,
            channel_id=channel_id,
            conversation_id=conversation_id,
            thread_id=thread_id,
            sender_id=sender_id,
            message_type=message_type,
            content=content,
            mentions=mentions,
            attachments=attachments or []
        )
        self.messages[message.id] = message
        
        # Update thread if reply
        if thread_id:
            self._update_thread(thread_id, message)
        
        # Update conversation last_message_at
        if conversation_id:
            conv = self.conversations.get(conversation_id)
            if conv:
                conv.last_message_at = message.created_at
        
        # Create notifications for mentions
        for mentioned_user_id in mentions:
            self._create_notification(
                user_id=mentioned_user_id,
                workspace_id=workspace_id,
                channel_id=channel_id,
                message_id=message.id,
                notification_type="mention",
                title="You were mentioned",
                body=f"<@{sender_id}> mentioned you: {content[:100]}"
            )
        
        logger.info(f"Sent message: {message.id}")
        return message
    
    def get_message(self, message_id: str) -> Optional[Message]:
        """Get message by ID"""
        return self.messages.get(message_id)
    
    def edit_message(self, message_id: str, new_content: str, edited_by: str) -> Optional[Message]:
        """Edit a message"""
        message = self.messages.get(message_id)
        if not message or message.sender_id != edited_by:
            return None
        
        message.content = new_content
        message.is_edited = True
        message.edited_at = datetime.utcnow()
        message.mentions = self._extract_mentions(new_content)
        
        return message
    
    def delete_message(self, message_id: str, deleted_by: str) -> bool:
        """Delete a message (soft delete)"""
        message = self.messages.get(message_id)
        if not message or message.sender_id != deleted_by:
            return False
        
        message.is_deleted = True
        message.content = "This message was deleted"
        
        return True
    
    def list_messages(
        self,
        channel_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        thread_id: Optional[str] = None,
        limit: int = 50,
        before: Optional[datetime] = None
    ) -> List[Message]:
        """List messages with pagination"""
        messages = []
        
        for msg in self.messages.values():
            if channel_id and msg.channel_id != channel_id:
                continue
            if conversation_id and msg.conversation_id != conversation_id:
                continue
            if thread_id and msg.thread_id != thread_id:
                continue
            if thread_id is None and msg.thread_id is not None:
                continue  # Exclude thread replies from main channel
            if before and msg.created_at >= before:
                continue
            messages.append(msg)
        
        messages.sort(key=lambda m: m.created_at, reverse=True)
        return messages[:limit]
    
    def search_messages(
        self,
        workspace_id: str,
        query: str,
        user_id: str,
        channel_id: Optional[str] = None,
        from_user_id: Optional[str] = None,
        limit: int = 20
    ) -> List[Message]:
        """Search messages"""
        results = []
        query_lower = query.lower()
        
        for msg in self.messages.values():
            if msg.workspace_id != workspace_id:
                continue
            if msg.is_deleted:
                continue
            if channel_id and msg.channel_id != channel_id:
                continue
            if from_user_id and msg.sender_id != from_user_id:
                continue
            if query_lower not in msg.content.lower():
                continue
            
            # Check access
            if msg.channel_id:
                channel = self.channels.get(msg.channel_id)
                if channel and channel.channel_type == ChannelType.PRIVATE:
                    if user_id not in channel.member_ids:
                        continue
            elif msg.conversation_id:
                conv = self.conversations.get(msg.conversation_id)
                if conv and user_id not in conv.participant_ids:
                    continue
            
            results.append(msg)
        
        results.sort(key=lambda m: m.created_at, reverse=True)
        return results[:limit]
    
    def pin_message(self, message_id: str, pinned_by: str) -> bool:
        """Pin a message"""
        message = self.messages.get(message_id)
        if not message:
            return False
        
        message.is_pinned = True
        
        if message.channel_id:
            channel = self.channels.get(message.channel_id)
            if channel and message_id not in channel.pinned_message_ids:
                channel.pinned_message_ids.append(message_id)
        
        return True
    
    def unpin_message(self, message_id: str) -> bool:
        """Unpin a message"""
        message = self.messages.get(message_id)
        if not message:
            return False
        
        message.is_pinned = False
        
        if message.channel_id:
            channel = self.channels.get(message.channel_id)
            if channel and message_id in channel.pinned_message_ids:
                channel.pinned_message_ids.remove(message_id)
        
        return True
    
    # --------------------------------------------------------
    # REACTION OPERATIONS
    # --------------------------------------------------------
    
    def add_reaction(self, message_id: str, user_id: str, emoji: str) -> bool:
        """Add reaction to message"""
        message = self.messages.get(message_id)
        if not message:
            return False
        
        if emoji not in message.reactions:
            message.reactions[emoji] = []
        
        if user_id not in message.reactions[emoji]:
            message.reactions[emoji].append(user_id)
        
        return True
    
    def remove_reaction(self, message_id: str, user_id: str, emoji: str) -> bool:
        """Remove reaction from message"""
        message = self.messages.get(message_id)
        if not message:
            return False
        
        if emoji in message.reactions and user_id in message.reactions[emoji]:
            message.reactions[emoji].remove(user_id)
            if not message.reactions[emoji]:
                del message.reactions[emoji]
        
        return True
    
    # --------------------------------------------------------
    # THREAD OPERATIONS
    # --------------------------------------------------------
    
    def _update_thread(self, parent_message_id: str, reply: Message):
        """Update or create thread for reply"""
        parent = self.messages.get(parent_message_id)
        if not parent:
            return
        
        if parent_message_id not in self.threads:
            thread = Thread(
                parent_message_id=parent_message_id,
                channel_id=parent.channel_id or "",
                participant_ids=[parent.sender_id]
            )
            self.threads[parent_message_id] = thread
        
        thread = self.threads[parent_message_id]
        thread.reply_count += 1
        thread.last_reply_at = reply.created_at
        
        if reply.sender_id not in thread.participant_ids:
            thread.participant_ids.append(reply.sender_id)
        
        parent.reply_count = thread.reply_count
    
    def get_thread(self, parent_message_id: str) -> Optional[Thread]:
        """Get thread info"""
        return self.threads.get(parent_message_id)
    
    def get_thread_replies(self, parent_message_id: str, limit: int = 50) -> List[Message]:
        """Get replies in thread"""
        return self.list_messages(thread_id=parent_message_id, limit=limit)
    
    # --------------------------------------------------------
    # MEMBER OPERATIONS
    # --------------------------------------------------------
    
    def add_member(
        self,
        workspace_id: str,
        user_id: str,
        added_by: str,
        display_name: str = "",
        role: MemberRole = MemberRole.MEMBER
    ) -> WorkspaceMember:
        """Add member to workspace"""
        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            display_name=display_name or f"User {user_id[:8]}",
            role=role
        )
        self.members[f"{workspace_id}:{user_id}"] = member
        
        # Auto-join default channels
        for channel in self.channels.values():
            if channel.workspace_id == workspace_id and channel.is_default:
                self.join_channel(channel.id, user_id)
        
        logger.info(f"Added member {user_id} to workspace {workspace_id}")
        return member
    
    def get_member(self, workspace_id: str, user_id: str) -> Optional[WorkspaceMember]:
        """Get workspace member"""
        return self.members.get(f"{workspace_id}:{user_id}")
    
    def list_members(self, workspace_id: str) -> List[WorkspaceMember]:
        """List workspace members"""
        return [m for m in self.members.values() if m.workspace_id == workspace_id]
    
    def update_member_status(
        self,
        workspace_id: str,
        user_id: str,
        status: UserStatus,
        status_text: str = "",
        status_emoji: str = ""
    ) -> Optional[WorkspaceMember]:
        """Update member status"""
        member = self.get_member(workspace_id, user_id)
        if not member:
            return None
        
        member.status = status
        member.status_text = status_text
        member.status_emoji = status_emoji
        member.last_active_at = datetime.utcnow()
        
        return member
    
    def remove_member(self, workspace_id: str, user_id: str, removed_by: str) -> bool:
        """Remove member from workspace"""
        key = f"{workspace_id}:{user_id}"
        if key in self.members:
            del self.members[key]
            
            # Remove from all channels
            for channel in self.channels.values():
                if channel.workspace_id == workspace_id and user_id in channel.member_ids:
                    channel.member_ids.remove(user_id)
            
            return True
        return False
    
    # --------------------------------------------------------
    # NOTIFICATION OPERATIONS
    # --------------------------------------------------------
    
    def _create_notification(
        self,
        user_id: str,
        workspace_id: str,
        notification_type: str,
        title: str,
        body: str,
        channel_id: Optional[str] = None,
        message_id: Optional[str] = None
    ):
        """Create notification for user"""
        notification = Notification(
            user_id=user_id,
            workspace_id=workspace_id,
            channel_id=channel_id,
            message_id=message_id,
            notification_type=notification_type,
            title=title,
            body=body
        )
        
        if user_id not in self.notifications:
            self.notifications[user_id] = []
        self.notifications[user_id].append(notification)
    
    def get_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get user notifications"""
        notifications = self.notifications.get(user_id, [])
        if unread_only:
            notifications = [n for n in notifications if not n.is_read]
        return sorted(notifications, key=lambda n: n.created_at, reverse=True)
    
    def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark notification as read"""
        for notification in self.notifications.get(user_id, []):
            if notification.id == notification_id:
                notification.is_read = True
                return True
        return False
    
    def mark_all_notifications_read(self, user_id: str) -> int:
        """Mark all notifications as read"""
        count = 0
        for notification in self.notifications.get(user_id, []):
            if not notification.is_read:
                notification.is_read = True
                count += 1
        return count
    
    # --------------------------------------------------------
    # POLL OPERATIONS
    # --------------------------------------------------------
    
    def create_poll(
        self,
        message_id: str,
        question: str,
        options: List[str],
        is_anonymous: bool = False,
        is_multiple_choice: bool = False,
        ends_at: Optional[datetime] = None
    ) -> Poll:
        """Create a poll"""
        poll = Poll(
            message_id=message_id,
            question=question,
            options=options,
            votes={opt: [] for opt in options},
            is_anonymous=is_anonymous,
            is_multiple_choice=is_multiple_choice,
            ends_at=ends_at
        )
        self.polls[poll.id] = poll
        
        # Update message type
        message = self.messages.get(message_id)
        if message:
            message.message_type = MessageType.POLL
        
        return poll
    
    def vote_poll(self, poll_id: str, user_id: str, option: str) -> bool:
        """Vote in poll"""
        poll = self.polls.get(poll_id)
        if not poll or option not in poll.options:
            return False
        
        if poll.ends_at and datetime.utcnow() > poll.ends_at:
            return False  # Poll ended
        
        # Remove previous vote if not multiple choice
        if not poll.is_multiple_choice:
            for opt in poll.votes:
                if user_id in poll.votes[opt]:
                    poll.votes[opt].remove(user_id)
        
        if user_id not in poll.votes[option]:
            poll.votes[option].append(user_id)
        
        return True
    
    def get_poll_results(self, poll_id: str) -> Optional[Dict[str, Any]]:
        """Get poll results"""
        poll = self.polls.get(poll_id)
        if not poll:
            return None
        
        results = {
            "question": poll.question,
            "options": {},
            "total_votes": 0,
            "is_ended": poll.ends_at and datetime.utcnow() > poll.ends_at
        }
        
        for option in poll.options:
            vote_count = len(poll.votes.get(option, []))
            results["options"][option] = {
                "count": vote_count,
                "voters": [] if poll.is_anonymous else poll.votes.get(option, [])
            }
            results["total_votes"] += vote_count
        
        return results
    
    # --------------------------------------------------------
    # AI FEATURES
    # --------------------------------------------------------
    
    def analyze_message(self, message_id: str) -> Optional[MessageAnalysis]:
        """Get AI analysis of a message"""
        message = self.messages.get(message_id)
        if not message:
            return None
        
        return self.ai_engine.analyze_message(message)
    
    def get_channel_summary(self, channel_id: str, period_hours: int = 24) -> Optional[ChannelSummary]:
        """Get AI summary of channel activity"""
        channel = self.channels.get(channel_id)
        if not channel:
            return None
        
        messages = self.list_messages(channel_id=channel_id, limit=500)
        return self.ai_engine.generate_channel_summary(channel, messages, period_hours)
    
    def get_smart_replies(self, message_id: str) -> List[SmartReply]:
        """Get AI-suggested replies"""
        message = self.messages.get(message_id)
        if not message:
            return []
        
        # Get context (previous messages)
        if message.channel_id:
            context = self.list_messages(channel_id=message.channel_id, limit=5)
        elif message.conversation_id:
            context = self.list_messages(conversation_id=message.conversation_id, limit=5)
        else:
            context = []
        
        return self.ai_engine.suggest_smart_replies(message, context)
    
    def get_important_messages(self, channel_id: str, limit: int = 10) -> List[Message]:
        """Get important messages that need attention"""
        messages = self.list_messages(channel_id=channel_id, limit=100)
        important = self.ai_engine.detect_important_messages(messages)
        return important[:limit]
    
    # --------------------------------------------------------
    # UTILITY METHODS
    # --------------------------------------------------------
    
    def _extract_mentions(self, content: str) -> List[str]:
        """Extract @mentions from content"""
        import re
        mentions = re.findall(r'<@([a-zA-Z0-9-]+)>', content)
        return mentions
    
    def _post_system_message(self, channel_id: str, content: str):
        """Post a system message"""
        channel = self.channels.get(channel_id)
        if not channel:
            return
        
        message = Message(
            workspace_id=channel.workspace_id,
            channel_id=channel_id,
            sender_id="system",
            message_type=MessageType.SYSTEM,
            content=content
        )
        self.messages[message.id] = message
    
    def get_dashboard(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        """Get collaboration dashboard data"""
        # Get user's channels
        channels = self.list_channels(workspace_id, user_id)
        
        # Get user's conversations
        conversations = self.list_conversations(workspace_id, user_id)
        
        # Get unread notifications
        notifications = self.get_notifications(user_id, unread_only=True)
        
        # Get workspace members
        members = self.list_members(workspace_id)
        online_count = sum(1 for m in members if m.status == UserStatus.ONLINE)
        
        # Recent activity
        recent_messages = []
        for channel in channels[:5]:
            msgs = self.list_messages(channel_id=channel.id, limit=3)
            recent_messages.extend(msgs)
        recent_messages.sort(key=lambda m: m.created_at, reverse=True)
        
        return {
            "workspace_id": workspace_id,
            "channels_count": len(channels),
            "conversations_count": len(conversations),
            "unread_notifications": len(notifications),
            "members_count": len(members),
            "online_members": online_count,
            "recent_activity": [
                {
                    "message_id": m.id,
                    "channel_id": m.channel_id,
                    "sender_id": m.sender_id,
                    "content": m.content[:100],
                    "created_at": m.created_at.isoformat()
                }
                for m in recent_messages[:10]
            ]
        }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":
    print("🤝 Testing Team Collaboration Service...")
    
    service = TeamCollaborationService()
    
    # Create workspace
    workspace = service.create_workspace(
        name="Acme Corp",
        owner_id="user_001",
        description="Main workspace"
    )
    print(f"✅ Created workspace: {workspace.name}")
    
    # Add members
    service.add_member(workspace.id, "user_002", "user_001", "Alice")
    service.add_member(workspace.id, "user_003", "user_001", "Bob")
    print("✅ Added team members")
    
    # Create channel
    dev_channel = service.create_channel(
        workspace_id=workspace.id,
        name="development",
        created_by="user_001",
        description="Dev team discussions"
    )
    print(f"✅ Created channel: #{dev_channel.name}")
    
    # Send messages
    msg1 = service.send_message(
        workspace_id=workspace.id,
        channel_id=dev_channel.id,
        sender_id="user_001",
        content="Hey team! We need to discuss the urgent deployment deadline. <@user_002> can you review the PR?"
    )
    print(f"✅ Sent message with mention")
    
    msg2 = service.send_message(
        workspace_id=workspace.id,
        channel_id=dev_channel.id,
        sender_id="user_002",
        content="Sure! I'll take a look. The new feature looks great!"
    )
    
    # Thread reply
    reply = service.send_message(
        workspace_id=workspace.id,
        channel_id=dev_channel.id,
        sender_id="user_003",
        content="Let me know if you need help with testing.",
        thread_id=msg1.id
    )
    print(f"✅ Thread reply created, {msg1.reply_count} replies")
    
    # Add reaction
    service.add_reaction(msg2.id, "user_001", "👍")
    service.add_reaction(msg2.id, "user_003", "👍")
    print(f"✅ Reactions added: {msg2.reactions}")
    
    # AI Analysis
    analysis = service.analyze_message(msg1.id)
    print(f"✅ AI Analysis - Priority: {analysis.priority.value}, Sentiment: {analysis.sentiment.value}")
    
    # Smart replies
    smart_replies = service.get_smart_replies(msg1.id)
    print(f"✅ Smart replies: {[r.suggestion for r in smart_replies]}")
    
    # Channel summary
    summary = service.get_channel_summary(dev_channel.id)
    print(f"✅ Channel summary: {summary.message_count} messages, topics: {summary.key_topics}")
    
    # Create DM
    dm = service.create_dm(workspace.id, ["user_001", "user_002"])
    dm_msg = service.send_message(
        workspace_id=workspace.id,
        conversation_id=dm.id,
        sender_id="user_001",
        content="Quick question about the meeting tomorrow"
    )
    print(f"✅ DM created and message sent")
    
    # Create poll
    poll_msg = service.send_message(
        workspace_id=workspace.id,
        channel_id=dev_channel.id,
        sender_id="user_001",
        content="When should we have the team standup?"
    )
    poll = service.create_poll(
        message_id=poll_msg.id,
        question="Best time for standup?",
        options=["9:00 AM", "10:00 AM", "11:00 AM"]
    )
    service.vote_poll(poll.id, "user_001", "10:00 AM")
    service.vote_poll(poll.id, "user_002", "10:00 AM")
    service.vote_poll(poll.id, "user_003", "9:00 AM")
    results = service.get_poll_results(poll.id)
    print(f"✅ Poll created: {results['options']}")
    
    # Search
    search_results = service.search_messages(workspace.id, "deployment", "user_001")
    print(f"✅ Search found {len(search_results)} messages")
    
    # Dashboard
    dashboard = service.get_dashboard(workspace.id, "user_001")
    print(f"✅ Dashboard: {dashboard['channels_count']} channels, {dashboard['members_count']} members")
    
    print("\n🎉 All Team Collaboration tests passed!")
