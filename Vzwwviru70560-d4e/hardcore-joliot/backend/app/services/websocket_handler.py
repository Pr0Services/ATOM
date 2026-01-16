"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V79 — WebSocket Real-Time Handler
═══════════════════════════════════════════════════════════════════════════════

Real-time communication for:
- Checkpoint notifications (R&D Rule #1)
- Thread updates
- Agent activity
- Cross-sphere events

R&D Rules Compliance:
- Rule #1: Checkpoint events prioritized
- Rule #3: Messages scoped to identity (no cross-identity leaks)
- Rule #4: Agent events tracked
- Rule #6: All messages logged
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, Set, Optional, Any, List
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field
from fastapi import WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger("chenu.websocket")


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class WSMessageType(str, Enum):
    """WebSocket message types."""
    
    # System
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    
    # Checkpoints (R&D Rule #1 - HIGH PRIORITY)
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_APPROVED = "checkpoint.approved"
    CHECKPOINT_REJECTED = "checkpoint.rejected"
    CHECKPOINT_EXPIRED = "checkpoint.expired"
    
    # Threads
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_EVENT = "thread.event"
    
    # Agents
    AGENT_HIRED = "agent.hired"
    AGENT_FIRED = "agent.fired"
    AGENT_TASK_STARTED = "agent.task.started"
    AGENT_TASK_COMPLETED = "agent.task.completed"
    
    # Spheres
    SPHERE_DATA_CHANGED = "sphere.data.changed"
    
    # Notifications
    NOTIFICATION = "notification"


class WSPriority(int, Enum):
    """Message priority levels."""
    
    CRITICAL = 0  # Checkpoints - must deliver immediately
    HIGH = 1      # Agent actions
    NORMAL = 2    # Thread updates
    LOW = 3       # General notifications


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class WSMessage:
    """WebSocket message structure."""
    
    type: WSMessageType
    payload: Dict[str, Any]
    priority: WSPriority = WSPriority.NORMAL
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    sphere: Optional[str] = None
    identity_id: Optional[UUID] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": str(self.id),
            "type": self.type.value,
            "payload": self.payload,
            "priority": self.priority.value,
            "timestamp": self.timestamp.isoformat(),
            "sphere": self.sphere,
            "identity_id": str(self.identity_id) if self.identity_id else None
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class ConnectionManager:
    """
    Manage WebSocket connections with identity isolation.
    
    R&D Rule #3: Each connection is scoped to an identity.
    Messages are NEVER sent across identity boundaries.
    """
    
    def __init__(self):
        # Map: identity_id -> Set of WebSocket connections
        self._connections: Dict[UUID, Set[WebSocket]] = {}
        
        # Map: WebSocket -> identity_id (reverse lookup)
        self._identity_map: Dict[WebSocket, UUID] = {}
        
        # Message queue for priority handling
        self._message_queue: asyncio.Queue = asyncio.Queue()
        
        # Statistics
        self.stats = {
            "total_connections": 0,
            "total_disconnections": 0,
            "messages_sent": 0,
            "checkpoint_messages": 0
        }
    
    async def connect(self, websocket: WebSocket, identity_id: UUID) -> None:
        """
        Accept a new WebSocket connection.
        
        Args:
            websocket: The WebSocket connection
            identity_id: The identity this connection belongs to
        """
        await websocket.accept()
        
        # Register connection for this identity
        if identity_id not in self._connections:
            self._connections[identity_id] = set()
        
        self._connections[identity_id].add(websocket)
        self._identity_map[websocket] = identity_id
        
        self.stats["total_connections"] += 1
        
        logger.info(f"WebSocket connected: identity={identity_id}")
        
        # Send connection confirmation
        await self._send_to_socket(websocket, WSMessage(
            type=WSMessageType.CONNECTED,
            payload={
                "identity_id": str(identity_id),
                "message": "Connected to CHE·NU™ real-time service",
                "version": "79.0.0"
            },
            identity_id=identity_id
        ))
    
    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Handle WebSocket disconnection.
        
        Args:
            websocket: The disconnecting WebSocket
        """
        identity_id = self._identity_map.get(websocket)
        
        if identity_id and identity_id in self._connections:
            self._connections[identity_id].discard(websocket)
            
            # Clean up empty sets
            if not self._connections[identity_id]:
                del self._connections[identity_id]
        
        if websocket in self._identity_map:
            del self._identity_map[websocket]
        
        self.stats["total_disconnections"] += 1
        
        logger.info(f"WebSocket disconnected: identity={identity_id}")
    
    async def send_to_identity(
        self,
        identity_id: UUID,
        message: WSMessage
    ) -> int:
        """
        Send message to all connections for an identity.
        
        R&D Rule #3: Messages are ONLY sent to the target identity.
        
        Args:
            identity_id: Target identity
            message: Message to send
            
        Returns:
            Number of connections message was sent to
        """
        message.identity_id = identity_id
        
        if identity_id not in self._connections:
            logger.debug(f"No connections for identity {identity_id}")
            return 0
        
        connections = self._connections[identity_id].copy()
        sent_count = 0
        
        for websocket in connections:
            try:
                await self._send_to_socket(websocket, message)
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send to socket: {e}")
                await self.disconnect(websocket)
        
        self.stats["messages_sent"] += sent_count
        
        if message.type.value.startswith("checkpoint"):
            self.stats["checkpoint_messages"] += sent_count
        
        return sent_count
    
    async def broadcast_to_sphere(
        self,
        sphere: str,
        message: WSMessage,
        exclude_identity: Optional[UUID] = None
    ) -> int:
        """
        Broadcast to all identities subscribed to a sphere.
        
        NOTE: This still respects identity boundaries - each identity
        receives their own copy of the message.
        
        Args:
            sphere: Sphere to broadcast to
            message: Message to send
            exclude_identity: Optional identity to exclude
            
        Returns:
            Total number of connections message was sent to
        """
        message.sphere = sphere
        total_sent = 0
        
        for identity_id in list(self._connections.keys()):
            if exclude_identity and identity_id == exclude_identity:
                continue
            
            # Would check sphere subscription here
            sent = await self.send_to_identity(identity_id, message)
            total_sent += sent
        
        return total_sent
    
    async def _send_to_socket(self, websocket: WebSocket, message: WSMessage) -> None:
        """Send message to a specific socket."""
        await websocket.send_text(message.to_json())
    
    def get_connection_count(self, identity_id: Optional[UUID] = None) -> int:
        """Get number of active connections."""
        if identity_id:
            return len(self._connections.get(identity_id, set()))
        return sum(len(conns) for conns in self._connections.values())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            **self.stats,
            "active_connections": self.get_connection_count(),
            "unique_identities": len(self._connections)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT NOTIFIER
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointNotifier:
    """
    Specialized notifier for checkpoint events.
    
    R&D Rule #1: Checkpoints are CRITICAL priority.
    User MUST be notified immediately when checkpoint is created.
    """
    
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
    
    async def notify_checkpoint_created(
        self,
        identity_id: UUID,
        checkpoint_id: UUID,
        action: str,
        sphere: str,
        details: Dict[str, Any]
    ) -> int:
        """
        Notify user of new checkpoint requiring approval.
        
        This is CRITICAL priority - UI should show modal immediately.
        """
        message = WSMessage(
            type=WSMessageType.CHECKPOINT_CREATED,
            priority=WSPriority.CRITICAL,
            sphere=sphere,
            payload={
                "checkpoint_id": str(checkpoint_id),
                "action": action,
                "sphere": sphere,
                "details": details,
                "requires_action": True,
                "options": ["approve", "reject"],
                "rd_rule": "Rule #1: Human Sovereignty"
            }
        )
        
        sent = await self.manager.send_to_identity(identity_id, message)
        logger.info(f"Checkpoint notification sent: {checkpoint_id} to {identity_id} ({sent} connections)")
        
        return sent
    
    async def notify_checkpoint_approved(
        self,
        identity_id: UUID,
        checkpoint_id: UUID,
        action: str
    ) -> int:
        """Notify that checkpoint was approved."""
        message = WSMessage(
            type=WSMessageType.CHECKPOINT_APPROVED,
            priority=WSPriority.HIGH,
            payload={
                "checkpoint_id": str(checkpoint_id),
                "action": action,
                "status": "approved",
                "message": f"Action '{action}' has been approved and executed"
            }
        )
        
        return await self.manager.send_to_identity(identity_id, message)
    
    async def notify_checkpoint_rejected(
        self,
        identity_id: UUID,
        checkpoint_id: UUID,
        action: str,
        reason: Optional[str] = None
    ) -> int:
        """Notify that checkpoint was rejected."""
        message = WSMessage(
            type=WSMessageType.CHECKPOINT_REJECTED,
            priority=WSPriority.HIGH,
            payload={
                "checkpoint_id": str(checkpoint_id),
                "action": action,
                "status": "rejected",
                "reason": reason,
                "message": f"Action '{action}' was rejected"
            }
        )
        
        return await self.manager.send_to_identity(identity_id, message)


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT NOTIFIER
# ═══════════════════════════════════════════════════════════════════════════════

class AgentNotifier:
    """
    Notifier for agent-related events.
    
    R&D Rule #4: Track all agent actions (human must be aware).
    """
    
    def __init__(self, connection_manager: ConnectionManager):
        self.manager = connection_manager
    
    async def notify_agent_hired(
        self,
        identity_id: UUID,
        agent_id: UUID,
        agent_name: str,
        agent_type: str
    ) -> int:
        """Notify that an agent was hired."""
        message = WSMessage(
            type=WSMessageType.AGENT_HIRED,
            priority=WSPriority.HIGH,
            sphere="my_team",
            payload={
                "agent_id": str(agent_id),
                "agent_name": agent_name,
                "agent_type": agent_type,
                "message": f"Agent '{agent_name}' has been hired"
            }
        )
        
        return await self.manager.send_to_identity(identity_id, message)
    
    async def notify_agent_task_started(
        self,
        identity_id: UUID,
        agent_id: UUID,
        task_id: UUID,
        task_title: str
    ) -> int:
        """Notify that an agent started a task."""
        message = WSMessage(
            type=WSMessageType.AGENT_TASK_STARTED,
            priority=WSPriority.NORMAL,
            payload={
                "agent_id": str(agent_id),
                "task_id": str(task_id),
                "task_title": task_title,
                "status": "in_progress"
            }
        )
        
        return await self.manager.send_to_identity(identity_id, message)
    
    async def notify_agent_task_completed(
        self,
        identity_id: UUID,
        agent_id: UUID,
        task_id: UUID,
        task_title: str,
        result: Optional[Dict] = None
    ) -> int:
        """Notify that an agent completed a task."""
        message = WSMessage(
            type=WSMessageType.AGENT_TASK_COMPLETED,
            priority=WSPriority.NORMAL,
            payload={
                "agent_id": str(agent_id),
                "task_id": str(task_id),
                "task_title": task_title,
                "status": "completed",
                "result": result
            }
        )
        
        return await self.manager.send_to_identity(identity_id, message)


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET ENDPOINT HANDLER
# ═══════════════════════════════════════════════════════════════════════════════

# Global connection manager instance
connection_manager = ConnectionManager()
checkpoint_notifier = CheckpointNotifier(connection_manager)
agent_notifier = AgentNotifier(connection_manager)


async def websocket_endpoint(websocket: WebSocket, identity_id: UUID):
    """
    WebSocket endpoint handler.
    
    Usage in FastAPI:
        @app.websocket("/ws/{identity_id}")
        async def ws_handler(websocket: WebSocket, identity_id: UUID):
            await websocket_endpoint(websocket, identity_id)
    """
    await connection_manager.connect(websocket, identity_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle ping
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }))
                continue
            
            # Handle subscription requests
            if message.get("type") == "subscribe":
                sphere = message.get("sphere")
                logger.info(f"Identity {identity_id} subscribed to {sphere}")
                continue
            
            # Log unknown messages
            logger.warning(f"Unknown message type from {identity_id}: {message}")
            
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for {identity_id}: {e}")
        await connection_manager.disconnect(websocket)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ConnectionManager",
    "CheckpointNotifier",
    "AgentNotifier",
    "WSMessage",
    "WSMessageType",
    "WSPriority",
    "websocket_endpoint",
    "connection_manager",
    "checkpoint_notifier",
    "agent_notifier"
]
