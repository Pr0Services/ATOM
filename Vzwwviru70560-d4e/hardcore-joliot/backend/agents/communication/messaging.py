"""
============================================================================
CHE·NU™ V69 — AGENT COMMUNICATION
============================================================================
Version: 1.0.0
Purpose: Inter-agent messaging and coordination
Principle: Structured communication with full traceability
============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from collections import defaultdict
import logging
import threading
import queue
import uuid

from ..core.models import (
    AgentMessage,
    MessagePriority,
)

logger = logging.getLogger(__name__)


# ============================================================================
# MESSAGE QUEUE
# ============================================================================

class AgentMailbox:
    """
    Mailbox for an individual agent.
    
    Stores incoming messages and tracks delivery/read status.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self._inbox: List[AgentMessage] = []
        self._outbox: List[AgentMessage] = []
        self._lock = threading.Lock()
    
    def receive(self, message: AgentMessage) -> None:
        """Receive a message"""
        with self._lock:
            message.delivered = True
            message.delivered_at = datetime.utcnow()
            self._inbox.append(message)
    
    def send(self, message: AgentMessage) -> None:
        """Record sent message"""
        with self._lock:
            self._outbox.append(message)
    
    def get_unread(self) -> List[AgentMessage]:
        """Get unread messages"""
        with self._lock:
            return [m for m in self._inbox if not m.read]
    
    def get_by_priority(self, priority: MessagePriority) -> List[AgentMessage]:
        """Get messages by priority"""
        with self._lock:
            return [m for m in self._inbox if m.priority == priority and not m.read]
    
    def mark_read(self, message_id: str) -> None:
        """Mark a message as read"""
        with self._lock:
            for msg in self._inbox:
                if msg.message_id == message_id:
                    msg.read = True
                    msg.read_at = datetime.utcnow()
                    break
    
    def get_message(self, message_id: str) -> Optional[AgentMessage]:
        """Get a specific message"""
        with self._lock:
            for msg in self._inbox + self._outbox:
                if msg.message_id == message_id:
                    return msg
        return None
    
    @property
    def unread_count(self) -> int:
        return len(self.get_unread())


# ============================================================================
# MESSAGE BUS
# ============================================================================

class MessageBus:
    """
    Central message bus for agent communication.
    
    Features:
    - Point-to-point messaging
    - Broadcast to groups
    - Priority queuing
    - Message persistence
    - Delivery tracking
    
    Architecture:
    
        ┌─────────────────────────────────────────────────────────┐
        │                     MESSAGE BUS                         │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │  Agent A ──▶ ┌─────────┐ ──▶ Agent B                   │
        │              │  ROUTER │                                │
        │  Agent C ◀── └─────────┘ ◀── Agent D                   │
        │                   │                                     │
        │                   ▼                                     │
        │           ┌─────────────┐                              │
        │           │  MAILBOXES  │                              │
        │           └─────────────┘                              │
        │                                                         │
        └─────────────────────────────────────────────────────────┘
    
    Usage:
        bus = MessageBus()
        
        # Register agents
        bus.register_agent("agent-001")
        bus.register_agent("agent-002")
        
        # Send message
        msg = AgentMessage(
            from_agent_id="agent-001",
            to_agent_id="agent-002",
            message_type="request",
            subject="Task assignment",
            body={"task_id": "task-001"},
        )
        bus.send(msg)
        
        # Receive messages
        messages = bus.get_messages("agent-002")
    """
    
    def __init__(self):
        self._mailboxes: Dict[str, AgentMailbox] = {}
        self._subscriptions: Dict[str, Set[str]] = defaultdict(set)  # topic -> agents
        self._message_handlers: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._all_messages: List[AgentMessage] = []
    
    def register_agent(self, agent_id: str) -> AgentMailbox:
        """Register an agent with the message bus"""
        with self._lock:
            if agent_id not in self._mailboxes:
                self._mailboxes[agent_id] = AgentMailbox(agent_id)
        return self._mailboxes[agent_id]
    
    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent"""
        with self._lock:
            if agent_id in self._mailboxes:
                del self._mailboxes[agent_id]
            
            # Remove from subscriptions
            for topic in self._subscriptions:
                self._subscriptions[topic].discard(agent_id)
    
    def subscribe(self, agent_id: str, topic: str) -> None:
        """Subscribe an agent to a topic"""
        with self._lock:
            self._subscriptions[topic].add(agent_id)
    
    def unsubscribe(self, agent_id: str, topic: str) -> None:
        """Unsubscribe an agent from a topic"""
        with self._lock:
            self._subscriptions[topic].discard(agent_id)
    
    def send(self, message: AgentMessage) -> bool:
        """
        Send a message to an agent.
        
        Returns True if delivered, False otherwise.
        """
        with self._lock:
            # Store message
            self._all_messages.append(message)
            
            # Record in sender's outbox
            if message.from_agent_id in self._mailboxes:
                self._mailboxes[message.from_agent_id].send(message)
            
            # Deliver to recipient
            if message.to_agent_id in self._mailboxes:
                self._mailboxes[message.to_agent_id].receive(message)
                
                logger.debug(
                    f"Message {message.message_id} delivered: "
                    f"{message.from_agent_id} -> {message.to_agent_id}"
                )
                
                return True
            else:
                logger.warning(f"Agent not found: {message.to_agent_id}")
                return False
    
    def broadcast(self, message: AgentMessage, topic: str) -> int:
        """
        Broadcast a message to all subscribers of a topic.
        
        Returns number of recipients.
        """
        subscribers = self._subscriptions.get(topic, set())
        delivered = 0
        
        for agent_id in subscribers:
            if agent_id != message.from_agent_id:
                # Create copy for each recipient
                msg_copy = message.model_copy(update={
                    "message_id": str(uuid.uuid4()),
                    "to_agent_id": agent_id,
                })
                if self.send(msg_copy):
                    delivered += 1
        
        logger.debug(f"Broadcast to topic '{topic}': {delivered} recipients")
        
        return delivered
    
    def get_messages(
        self,
        agent_id: str,
        unread_only: bool = True,
        priority: Optional[MessagePriority] = None,
    ) -> List[AgentMessage]:
        """Get messages for an agent"""
        mailbox = self._mailboxes.get(agent_id)
        if mailbox is None:
            return []
        
        if priority:
            return mailbox.get_by_priority(priority)
        elif unread_only:
            return mailbox.get_unread()
        else:
            return mailbox._inbox
    
    def mark_read(self, agent_id: str, message_id: str) -> None:
        """Mark a message as read"""
        mailbox = self._mailboxes.get(agent_id)
        if mailbox:
            mailbox.mark_read(message_id)
    
    def get_mailbox(self, agent_id: str) -> Optional[AgentMailbox]:
        """Get an agent's mailbox"""
        return self._mailboxes.get(agent_id)
    
    def send_and_wait_reply(
        self,
        message: AgentMessage,
        timeout_seconds: float = 30,
    ) -> Optional[AgentMessage]:
        """
        Send a message and wait for a reply.
        
        In production, this would be async.
        """
        # Set correlation ID
        correlation_id = message.correlation_id or str(uuid.uuid4())
        message.correlation_id = correlation_id
        
        self.send(message)
        
        # Wait for reply (simplified)
        # In production: use async/await or callbacks
        return None  # Mock


# ============================================================================
# COMMUNICATION CHANNELS
# ============================================================================

class CommunicationChannel:
    """
    Named communication channel between agents.
    """
    
    def __init__(
        self,
        channel_id: str,
        name: str,
        participants: Set[str],
        message_bus: MessageBus,
    ):
        self.channel_id = channel_id
        self.name = name
        self.participants = participants
        self._bus = message_bus
        self._history: List[AgentMessage] = []
    
    def send(
        self,
        from_agent_id: str,
        message_type: str,
        subject: str,
        body: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> int:
        """Send message to all channel participants"""
        delivered = 0
        
        for participant in self.participants:
            if participant != from_agent_id:
                msg = AgentMessage(
                    from_agent_id=from_agent_id,
                    to_agent_id=participant,
                    message_type=message_type,
                    subject=subject,
                    body=body,
                    priority=priority,
                    correlation_id=self.channel_id,
                )
                
                if self._bus.send(msg):
                    delivered += 1
                    self._history.append(msg)
        
        return delivered
    
    def add_participant(self, agent_id: str) -> None:
        """Add a participant to the channel"""
        self.participants.add(agent_id)
    
    def remove_participant(self, agent_id: str) -> None:
        """Remove a participant from the channel"""
        self.participants.discard(agent_id)
    
    @property
    def history(self) -> List[AgentMessage]:
        """Get channel message history"""
        return list(self._history)


# ============================================================================
# PROTOCOL DEFINITIONS
# ============================================================================

class MessageProtocol:
    """
    Standard message types for agent communication.
    """
    
    # Request/Response
    REQUEST = "request"
    RESPONSE = "response"
    
    # Commands
    COMMAND = "command"
    COMMAND_ACK = "command_ack"
    
    # Events
    EVENT = "event"
    NOTIFICATION = "notification"
    
    # Delegation
    DELEGATE = "delegate"
    DELEGATE_ACCEPT = "delegate_accept"
    DELEGATE_REJECT = "delegate_reject"
    DELEGATE_COMPLETE = "delegate_complete"
    
    # Escalation
    ESCALATE = "escalate"
    ESCALATE_ACK = "escalate_ack"
    
    # Status
    STATUS_UPDATE = "status_update"
    HEARTBEAT = "heartbeat"
    
    # Checkpoints
    CHECKPOINT_REQUEST = "checkpoint_request"
    CHECKPOINT_RESPONSE = "checkpoint_response"


class MessageFactory:
    """
    Factory for creating standard messages.
    """
    
    @staticmethod
    def create_request(
        from_agent: str,
        to_agent: str,
        subject: str,
        body: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> AgentMessage:
        """Create a request message"""
        return AgentMessage(
            from_agent_id=from_agent,
            to_agent_id=to_agent,
            message_type=MessageProtocol.REQUEST,
            subject=subject,
            body=body,
            priority=priority,
        )
    
    @staticmethod
    def create_response(
        request: AgentMessage,
        body: Dict[str, Any],
        success: bool = True,
    ) -> AgentMessage:
        """Create a response to a request"""
        return AgentMessage(
            from_agent_id=request.to_agent_id,
            to_agent_id=request.from_agent_id,
            message_type=MessageProtocol.RESPONSE,
            subject=f"Re: {request.subject}",
            body={
                "success": success,
                **body,
            },
            correlation_id=request.correlation_id or request.message_id,
            reply_to=request.message_id,
        )
    
    @staticmethod
    def create_delegation(
        from_agent: str,
        to_agent: str,
        task: Dict[str, Any],
    ) -> AgentMessage:
        """Create a delegation message"""
        return AgentMessage(
            from_agent_id=from_agent,
            to_agent_id=to_agent,
            message_type=MessageProtocol.DELEGATE,
            subject="Task Delegation",
            body={"task": task},
            priority=MessagePriority.HIGH,
        )
    
    @staticmethod
    def create_event(
        from_agent: str,
        to_agent: str,
        event_type: str,
        data: Dict[str, Any],
    ) -> AgentMessage:
        """Create an event notification"""
        return AgentMessage(
            from_agent_id=from_agent,
            to_agent_id=to_agent,
            message_type=MessageProtocol.EVENT,
            subject=event_type,
            body={"event_type": event_type, "data": data},
        )


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_message_bus() -> MessageBus:
    """Create a message bus"""
    return MessageBus()


def create_channel(
    name: str,
    participants: Set[str],
    message_bus: MessageBus,
) -> CommunicationChannel:
    """Create a communication channel"""
    return CommunicationChannel(
        channel_id=str(uuid.uuid4()),
        name=name,
        participants=participants,
        message_bus=message_bus,
    )
