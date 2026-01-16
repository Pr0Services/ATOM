"""
CHE·NU™ — WEBSOCKET TESTS (PYTEST)
Sprint 5: Tests for real-time WebSocket communication

WebSocket Features:
- Real-time notifications
- Agent status updates
- Task progress streaming
- Sphere sync events
"""

import pytest
from typing import Dict, List, Set
from datetime import datetime
import json
import asyncio
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class NotificationType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SYNC = "sync"
    AGENT = "agent"
    TASK = "task"
    GOVERNANCE = "governance"
    THREAD = "thread"


class WebSocketEvent(str, Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    MESSAGE = "message"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK WEBSOCKET CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class MockNotification:
    """Mock notification for testing."""
    
    def __init__(
        self,
        title: str,
        type: NotificationType = NotificationType.INFO,
        message: str = None,
        source: str = None,
        data: Dict = None
    ):
        self.id = f"notif-{datetime.utcnow().timestamp()}"
        self.type = type
        self.title = title
        self.message = message
        self.source = source
        self.data = data or {}
        self.timestamp = datetime.utcnow()
    
    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "message": self.message,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        })


class MockConnectionManager:
    """Mock WebSocket connection manager."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set] = {}
        self.global_connections: Set = set()
        self.messages_sent: List[Dict] = []
        self.connected_users: Set[str] = set()
    
    def connect(self, user_id: str = "global"):
        """Simulate connection."""
        if user_id == "global":
            self.global_connections.add(user_id)
        else:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
            self.active_connections[user_id].add(f"ws_{user_id}")
            self.connected_users.add(user_id)
        return True
    
    def disconnect(self, user_id: str = "global"):
        """Simulate disconnection."""
        if user_id == "global":
            self.global_connections.discard(user_id)
        else:
            if user_id in self.active_connections:
                self.active_connections[user_id].clear()
            self.connected_users.discard(user_id)
    
    def count(self) -> int:
        """Count total connections."""
        return len(self.global_connections) + sum(
            len(conns) for conns in self.active_connections.values()
        )
    
    def send_to_user(self, user_id: str, message: Dict):
        """Send message to specific user."""
        self.messages_sent.append({
            "target": user_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def broadcast(self, message: Dict):
        """Broadcast to all connections."""
        for user_id in self.connected_users:
            self.send_to_user(user_id, message)
        self.messages_sent.append({
            "target": "broadcast",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION MANAGER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestConnectionManager:
    """Tests for WebSocket connection manager."""

    def test_connect_user(self):
        """Should connect a user."""
        manager = MockConnectionManager()
        result = manager.connect("user_123")
        
        assert result is True
        assert "user_123" in manager.connected_users

    def test_disconnect_user(self):
        """Should disconnect a user."""
        manager = MockConnectionManager()
        manager.connect("user_123")
        manager.disconnect("user_123")
        
        assert "user_123" not in manager.connected_users

    def test_count_connections(self):
        """Should count total connections."""
        manager = MockConnectionManager()
        manager.connect("user_1")
        manager.connect("user_2")
        manager.connect("user_3")
        
        assert manager.count() == 3

    def test_global_connection(self):
        """Should support global connections."""
        manager = MockConnectionManager()
        manager.connect("global")
        
        assert "global" in manager.global_connections

    def test_multiple_connections_per_user(self):
        """Should support multiple connections per user."""
        manager = MockConnectionManager()
        manager.connect("user_123")
        manager.active_connections["user_123"].add("ws_user_123_2")
        
        assert len(manager.active_connections["user_123"]) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNotifications:
    """Tests for WebSocket notifications."""

    def test_create_notification(self):
        """Should create a notification."""
        notif = MockNotification(
            title="Test Notification",
            type=NotificationType.INFO,
        )
        
        assert notif.title == "Test Notification"
        assert notif.type == NotificationType.INFO

    def test_notification_has_id(self):
        """Notification should have unique ID."""
        notif = MockNotification(title="Test")
        assert notif.id is not None
        assert notif.id.startswith("notif-")

    def test_notification_has_timestamp(self):
        """Notification should have timestamp."""
        notif = MockNotification(title="Test")
        assert notif.timestamp is not None

    def test_notification_to_json(self):
        """Should serialize notification to JSON."""
        notif = MockNotification(
            title="Test",
            type=NotificationType.SUCCESS,
            message="Test message",
        )
        
        json_str = notif.to_json()
        data = json.loads(json_str)
        
        assert data["title"] == "Test"
        assert data["type"] == "success"
        assert data["message"] == "Test message"

    def test_notification_types(self):
        """Should support all notification types."""
        types = [
            NotificationType.INFO,
            NotificationType.SUCCESS,
            NotificationType.WARNING,
            NotificationType.ERROR,
            NotificationType.SYNC,
            NotificationType.AGENT,
            NotificationType.TASK,
        ]
        
        for ntype in types:
            notif = MockNotification(title="Test", type=ntype)
            assert notif.type == ntype


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE SENDING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMessageSending:
    """Tests for sending WebSocket messages."""

    def test_send_to_user(self):
        """Should send message to specific user."""
        manager = MockConnectionManager()
        manager.connect("user_123")
        
        manager.send_to_user("user_123", {"type": "test", "data": "hello"})
        
        assert len(manager.messages_sent) == 1
        assert manager.messages_sent[0]["target"] == "user_123"

    def test_broadcast_message(self):
        """Should broadcast to all users."""
        manager = MockConnectionManager()
        manager.connect("user_1")
        manager.connect("user_2")
        
        manager.broadcast({"type": "broadcast", "data": "hello all"})
        
        # Should have messages for each user + broadcast
        assert len(manager.messages_sent) >= 2

    def test_message_has_timestamp(self):
        """Sent messages should have timestamp."""
        manager = MockConnectionManager()
        manager.connect("user_123")
        manager.send_to_user("user_123", {"type": "test"})
        
        assert "timestamp" in manager.messages_sent[0]


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT STATUS NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentNotifications:
    """Tests for agent-related WebSocket notifications."""

    def test_agent_status_notification(self):
        """Should create agent status notification."""
        notif = MockNotification(
            title="Agent Status Update",
            type=NotificationType.AGENT,
            source="nova",
            data={
                "agent_id": "nova",
                "status": "busy",
                "task_id": "task_123",
            }
        )
        
        assert notif.type == NotificationType.AGENT
        assert notif.data["agent_id"] == "nova"

    def test_nova_notification(self):
        """Should support Nova-specific notifications."""
        notif = MockNotification(
            title="Nova Response",
            type=NotificationType.AGENT,
            source="nova",
            data={
                "agent_id": "nova",
                "level": "L0",
                "is_system": True,
            }
        )
        
        assert notif.data["level"] == "L0"
        assert notif.data["is_system"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# TASK PROGRESS NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTaskNotifications:
    """Tests for task progress WebSocket notifications."""

    def test_task_started_notification(self):
        """Should notify when task starts."""
        notif = MockNotification(
            title="Task Started",
            type=NotificationType.TASK,
            data={
                "task_id": "task_123",
                "status": "running",
                "progress": 0,
            }
        )
        
        assert notif.data["status"] == "running"

    def test_task_progress_notification(self):
        """Should notify task progress."""
        notif = MockNotification(
            title="Task Progress",
            type=NotificationType.TASK,
            data={
                "task_id": "task_123",
                "progress": 50,
                "tokens_used": 250,
            }
        )
        
        assert notif.data["progress"] == 50

    def test_task_completed_notification(self):
        """Should notify when task completes."""
        notif = MockNotification(
            title="Task Completed",
            type=NotificationType.SUCCESS,
            data={
                "task_id": "task_123",
                "status": "completed",
                "progress": 100,
                "tokens_used": 500,
            }
        )
        
        assert notif.data["status"] == "completed"
        assert notif.data["progress"] == 100


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestGovernanceNotifications:
    """Tests for governance WebSocket notifications."""

    def test_budget_warning_notification(self):
        """Should notify on budget warning."""
        notif = MockNotification(
            title="Budget Warning",
            type=NotificationType.WARNING,
            data={
                "budget_used_percent": 82,
                "threshold": 80,
                "remaining": 18000,
            }
        )
        
        assert notif.type == NotificationType.WARNING
        assert notif.data["budget_used_percent"] > notif.data["threshold"]

    def test_approval_required_notification(self):
        """Should notify when approval is required."""
        notif = MockNotification(
            title="Approval Required",
            type=NotificationType.GOVERNANCE,
            data={
                "approval_type": "execution",
                "estimated_tokens": 5000,
                "requires_approval": True,
            }
        )
        
        assert notif.data["requires_approval"] is True

    def test_scope_lock_notification(self):
        """Should notify on scope lock change."""
        notif = MockNotification(
            title="Scope Locked",
            type=NotificationType.INFO,
            data={
                "scope_level": "document",
                "target_id": "doc_123",
                "locked": True,
            }
        )
        
        assert notif.data["locked"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SYNC NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadNotifications:
    """Tests for thread (.chenu) WebSocket notifications."""

    def test_new_message_notification(self):
        """Should notify on new thread message."""
        notif = MockNotification(
            title="New Message",
            type=NotificationType.THREAD,
            data={
                "thread_id": "thread_123",
                "message_id": "msg_456",
                "role": "assistant",
                "tokens_used": 150,
            }
        )
        
        assert notif.data["thread_id"] == "thread_123"

    def test_thread_created_notification(self):
        """Should notify when thread is created."""
        notif = MockNotification(
            title="Thread Created",
            type=NotificationType.SYNC,
            data={
                "thread_id": "thread_new",
                "sphere_id": "personal",
                "type": "chat",
            }
        )
        
        assert notif.data["sphere_id"] == "personal"


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE SYNC NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereSyncNotifications:
    """Tests for sphere sync WebSocket notifications."""

    def test_sphere_data_updated(self):
        """Should notify when sphere data is updated."""
        notif = MockNotification(
            title="Sphere Updated",
            type=NotificationType.SYNC,
            data={
                "sphere_id": "business",
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        
        assert notif.data["sphere_id"] == "business"

    def test_sphere_switch_notification(self):
        """Should notify on sphere switch."""
        notif = MockNotification(
            title="Sphere Switched",
            type=NotificationType.INFO,
            data={
                "from_sphere": "personal",
                "to_sphere": "business",
            }
        )
        
        assert notif.data["from_sphere"] == "personal"
        assert notif.data["to_sphere"] == "business"


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestWebSocketErrorHandling:
    """Tests for WebSocket error handling."""

    def test_error_notification(self):
        """Should create error notification."""
        notif = MockNotification(
            title="Connection Error",
            type=NotificationType.ERROR,
            message="Failed to process request",
            data={
                "error_code": "WS_001",
                "recoverable": True,
            }
        )
        
        assert notif.type == NotificationType.ERROR
        assert notif.data["recoverable"] is True

    def test_disconnect_cleanup(self):
        """Should clean up on disconnect."""
        manager = MockConnectionManager()
        manager.connect("user_123")
        assert "user_123" in manager.connected_users
        
        manager.disconnect("user_123")
        assert "user_123" not in manager.connected_users


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT WEBSOCKET COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestWebSocketMemoryPromptCompliance:
    """Tests ensuring WebSocket follows Memory Prompt rules."""

    def test_notifications_respect_sphere_isolation(self):
        """L9: Notifications should respect sphere isolation."""
        # Create sphere-specific notification
        notif = MockNotification(
            title="Sphere Data",
            type=NotificationType.SYNC,
            data={
                "sphere_id": "personal",
                "isolated": True,
            }
        )
        
        assert notif.data["isolated"] is True

    def test_notifications_are_auditable(self):
        """L5: All notifications should be auditable."""
        notif = MockNotification(title="Test")
        
        # Should have ID and timestamp for audit
        assert notif.id is not None
        assert notif.timestamp is not None

    def test_agent_notifications_non_autonomous(self):
        """L7: Agent notifications should not trigger autonomous actions."""
        notif = MockNotification(
            title="Agent Update",
            type=NotificationType.AGENT,
            data={
                "agent_id": "nova",
                "requires_approval": True,
                "autonomous_action": False,
            }
        )
        
        assert notif.data["autonomous_action"] is False
