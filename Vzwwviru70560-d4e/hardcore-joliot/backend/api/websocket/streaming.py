"""
============================================================================
CHE·NU™ V69 — WEBSOCKET STREAMING
============================================================================
Version: 1.0.0
Purpose: Real-time streaming for simulations and agent events
Principle: Live updates with governance
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import asyncio
import json
import logging
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ============================================================================
# MESSAGE TYPES
# ============================================================================

class WSMessageType(str, Enum):
    """WebSocket message types"""
    # Client -> Server
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    PING = "ping"
    
    # Server -> Client
    CONNECTED = "connected"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    PONG = "pong"
    ERROR = "error"
    
    # Events - Simulations
    SIMULATION_UPDATE = "simulation_update"
    
    # Events - Agents
    AGENT_EVENT = "agent_event"
    AGENT_HIRED = "agent_hired"
    AGENT_DISMISSED = "agent_dismissed"
    
    # Events - Checkpoints/Governance
    CHECKPOINT_CREATED = "checkpoint_created"
    CHECKPOINT_RESOLVED = "checkpoint_resolved"
    GOVERNANCE_ALERT = "governance_alert"
    
    # Events - Threads
    THREAD_CREATED = "thread_created"
    THREAD_UPDATED = "thread_updated"
    THREAD_ARCHIVED = "thread_archived"
    THREAD_EVENT = "thread_event"
    
    # Events - Decisions
    DECISION_CREATED = "decision_created"
    DECISION_RESOLVED = "decision_resolved"
    DECISION_DEFERRED = "decision_deferred"
    
    # Events - Notifications
    NOTIFICATION = "notification"
    NOTIFICATION_COUNT = "notification_count"
    
    # Events - Nova
    NOVA_RESPONSE = "nova_response"
    NOVA_TYPING = "nova_typing"
    
    # Events - XR
    XR_PACK_READY = "xr_pack_ready"


class WSMessage(BaseModel):
    """WebSocket message"""
    type: str
    payload: Dict[str, Any] = {}
    timestamp: datetime = None
    
    def __init__(self, **data):
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow()
        super().__init__(**data)
    
    def to_json(self) -> str:
        return json.dumps({
            "type": self.type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
        })


# ============================================================================
# CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """
    Manages WebSocket connections and subscriptions.
    
    Features:
    - Connection tracking
    - Channel subscriptions
    - Broadcast capabilities
    - Heartbeat monitoring
    """
    
    def __init__(self):
        self._connections: Dict[str, WebSocket] = {}
        self._subscriptions: Dict[str, Set[str]] = {}  # channel -> connection_ids
        self._connection_channels: Dict[str, Set[str]] = {}  # connection_id -> channels
    
    async def connect(self, websocket: WebSocket, connection_id: str) -> None:
        """Accept a new connection"""
        await websocket.accept()
        self._connections[connection_id] = websocket
        self._connection_channels[connection_id] = set()
        
        logger.info(f"WebSocket connected: {connection_id}")
        
        # Send connected message
        await self.send_message(
            connection_id,
            WSMessage(
                type=WSMessageType.CONNECTED,
                payload={"connection_id": connection_id},
            ),
        )
    
    async def disconnect(self, connection_id: str) -> None:
        """Handle disconnection"""
        # Unsubscribe from all channels
        channels = self._connection_channels.get(connection_id, set())
        for channel in channels:
            if channel in self._subscriptions:
                self._subscriptions[channel].discard(connection_id)
        
        # Remove connection
        if connection_id in self._connections:
            del self._connections[connection_id]
        if connection_id in self._connection_channels:
            del self._connection_channels[connection_id]
        
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def subscribe(self, connection_id: str, channel: str) -> None:
        """Subscribe connection to a channel"""
        if channel not in self._subscriptions:
            self._subscriptions[channel] = set()
        
        self._subscriptions[channel].add(connection_id)
        self._connection_channels[connection_id].add(channel)
        
        logger.debug(f"Connection {connection_id} subscribed to {channel}")
        
        await self.send_message(
            connection_id,
            WSMessage(
                type=WSMessageType.SUBSCRIBED,
                payload={"channel": channel},
            ),
        )
    
    async def unsubscribe(self, connection_id: str, channel: str) -> None:
        """Unsubscribe connection from a channel"""
        if channel in self._subscriptions:
            self._subscriptions[channel].discard(connection_id)
        
        if connection_id in self._connection_channels:
            self._connection_channels[connection_id].discard(channel)
        
        await self.send_message(
            connection_id,
            WSMessage(
                type=WSMessageType.UNSUBSCRIBED,
                payload={"channel": channel},
            ),
        )
    
    async def send_message(self, connection_id: str, message: WSMessage) -> bool:
        """Send message to a specific connection"""
        websocket = self._connections.get(connection_id)
        if websocket:
            try:
                await websocket.send_text(message.to_json())
                return True
            except Exception as e:
                logger.error(f"Failed to send message to {connection_id}: {e}")
                return False
        return False
    
    async def broadcast_to_channel(self, channel: str, message: WSMessage) -> int:
        """Broadcast message to all subscribers of a channel"""
        subscribers = self._subscriptions.get(channel, set())
        sent = 0
        
        for connection_id in subscribers:
            if await self.send_message(connection_id, message):
                sent += 1
        
        return sent
    
    async def broadcast_all(self, message: WSMessage) -> int:
        """Broadcast message to all connections"""
        sent = 0
        
        for connection_id in self._connections:
            if await self.send_message(connection_id, message):
                sent += 1
        
        return sent
    
    @property
    def connection_count(self) -> int:
        return len(self._connections)
    
    def get_channel_subscribers(self, channel: str) -> int:
        return len(self._subscriptions.get(channel, set()))


# ============================================================================
# WEBSOCKET ROUTER
# ============================================================================

ws_router = APIRouter()
manager = ConnectionManager()


@ws_router.websocket("/stream")
async def websocket_stream(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    """
    Main WebSocket endpoint for real-time streaming.
    
    Supports:
    - Simulation updates
    - Agent events
    - Checkpoint notifications
    - XR Pack ready notifications
    
    Message format:
    ```json
    {
        "type": "subscribe",
        "payload": {
            "channel": "simulation:sim-001"
        }
    }
    ```
    
    Channels:
    - `simulation:{id}` - Simulation updates
    - `agent:{id}` - Agent events
    - `checkpoints` - All checkpoint events
    - `checkpoints:{agent_id}` - Agent-specific checkpoints
    - `xr-packs` - XR Pack notifications
    """
    connection_id = str(uuid.uuid4())
    
    await manager.connect(websocket, connection_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                msg_type = message.get("type")
                payload = message.get("payload", {})
                
                if msg_type == WSMessageType.PING:
                    await manager.send_message(
                        connection_id,
                        WSMessage(type=WSMessageType.PONG),
                    )
                
                elif msg_type == WSMessageType.SUBSCRIBE:
                    channel = payload.get("channel")
                    if channel:
                        await manager.subscribe(connection_id, channel)
                
                elif msg_type == WSMessageType.UNSUBSCRIBE:
                    channel = payload.get("channel")
                    if channel:
                        await manager.unsubscribe(connection_id, channel)
                
                else:
                    await manager.send_message(
                        connection_id,
                        WSMessage(
                            type=WSMessageType.ERROR,
                            payload={"error": f"Unknown message type: {msg_type}"},
                        ),
                    )
            
            except json.JSONDecodeError:
                await manager.send_message(
                    connection_id,
                    WSMessage(
                        type=WSMessageType.ERROR,
                        payload={"error": "Invalid JSON"},
                    ),
                )
    
    except WebSocketDisconnect:
        await manager.disconnect(connection_id)


@ws_router.websocket("/simulation/{simulation_id}")
async def websocket_simulation(
    websocket: WebSocket,
    simulation_id: str,
):
    """
    WebSocket for a specific simulation.
    
    Automatically subscribes to simulation updates.
    """
    connection_id = str(uuid.uuid4())
    channel = f"simulation:{simulation_id}"
    
    await manager.connect(websocket, connection_id)
    await manager.subscribe(connection_id, channel)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Handle messages
            message = json.loads(data)
            
            if message.get("type") == WSMessageType.PING:
                await manager.send_message(
                    connection_id,
                    WSMessage(type=WSMessageType.PONG),
                )
    
    except WebSocketDisconnect:
        await manager.disconnect(connection_id)


# ============================================================================
# EVENT EMITTERS (for other modules to use)
# ============================================================================

async def emit_simulation_update(
    simulation_id: str,
    status: str,
    progress: float,
    data: Dict[str, Any] = None,
) -> int:
    """Emit simulation update event"""
    message = WSMessage(
        type=WSMessageType.SIMULATION_UPDATE,
        payload={
            "simulation_id": simulation_id,
            "status": status,
            "progress": progress,
            "data": data or {},
        },
    )
    
    return await manager.broadcast_to_channel(
        f"simulation:{simulation_id}",
        message,
    )


async def emit_agent_event(
    agent_id: str,
    event_type: str,
    data: Dict[str, Any] = None,
) -> int:
    """Emit agent event"""
    message = WSMessage(
        type=WSMessageType.AGENT_EVENT,
        payload={
            "agent_id": agent_id,
            "event_type": event_type,
            "data": data or {},
        },
    )
    
    return await manager.broadcast_to_channel(
        f"agent:{agent_id}",
        message,
    )


async def emit_checkpoint_created(
    checkpoint_id: str,
    agent_id: str,
    action_id: str,
    checkpoint_type: str,
    reason: str,
) -> int:
    """Emit checkpoint created event"""
    message = WSMessage(
        type=WSMessageType.CHECKPOINT_CREATED,
        payload={
            "checkpoint_id": checkpoint_id,
            "agent_id": agent_id,
            "action_id": action_id,
            "checkpoint_type": checkpoint_type,
            "reason": reason,
        },
    )
    
    # Broadcast to both general and agent-specific channels
    sent = await manager.broadcast_to_channel("checkpoints", message)
    sent += await manager.broadcast_to_channel(f"checkpoints:{agent_id}", message)
    
    return sent


async def emit_checkpoint_resolved(
    checkpoint_id: str,
    status: str,
    resolved_by: str,
) -> int:
    """Emit checkpoint resolved event"""
    message = WSMessage(
        type=WSMessageType.CHECKPOINT_RESOLVED,
        payload={
            "checkpoint_id": checkpoint_id,
            "status": status,
            "resolved_by": resolved_by,
        },
    )
    
    return await manager.broadcast_to_channel("checkpoints", message)


async def emit_xr_pack_ready(
    pack_id: str,
    simulation_id: str,
) -> int:
    """Emit XR Pack ready event"""
    message = WSMessage(
        type=WSMessageType.XR_PACK_READY,
        payload={
            "pack_id": pack_id,
            "simulation_id": simulation_id,
        },
    )
    
    sent = await manager.broadcast_to_channel("xr-packs", message)
    sent += await manager.broadcast_to_channel(f"simulation:{simulation_id}", message)
    
    return sent


# ============================================================================
# THREAD EVENT EMITTERS
# ============================================================================

async def emit_thread_created(
    thread_id: str,
    title: str,
    sphere_id: str,
    owner_id: str,
) -> int:
    """Emit thread created event"""
    message = WSMessage(
        type=WSMessageType.THREAD_CREATED,
        payload={
            "thread_id": thread_id,
            "title": title,
            "sphere_id": sphere_id,
            "owner_id": owner_id,
        },
    )
    
    sent = await manager.broadcast_to_channel(f"user:{owner_id}", message)
    sent += await manager.broadcast_to_channel(f"sphere:{sphere_id}", message)
    return sent


async def emit_thread_updated(
    thread_id: str,
    changes: Dict[str, Any],
    owner_id: str,
) -> int:
    """Emit thread updated event"""
    message = WSMessage(
        type=WSMessageType.THREAD_UPDATED,
        payload={
            "thread_id": thread_id,
            "changes": changes,
        },
    )
    
    sent = await manager.broadcast_to_channel(f"thread:{thread_id}", message)
    sent += await manager.broadcast_to_channel(f"user:{owner_id}", message)
    return sent


async def emit_thread_event(
    thread_id: str,
    event_type: str,
    payload: Dict[str, Any],
) -> int:
    """Emit thread event"""
    message = WSMessage(
        type=WSMessageType.THREAD_EVENT,
        payload={
            "thread_id": thread_id,
            "event_type": event_type,
            **payload,
        },
    )
    
    return await manager.broadcast_to_channel(f"thread:{thread_id}", message)


# ============================================================================
# DECISION EVENT EMITTERS
# ============================================================================

async def emit_decision_created(
    decision_id: str,
    title: str,
    thread_id: str,
    owner_id: str,
    priority: str,
) -> int:
    """Emit decision created event"""
    message = WSMessage(
        type=WSMessageType.DECISION_CREATED,
        payload={
            "decision_id": decision_id,
            "title": title,
            "thread_id": thread_id,
            "priority": priority,
        },
    )
    
    sent = await manager.broadcast_to_channel(f"user:{owner_id}", message)
    sent += await manager.broadcast_to_channel("decisions", message)
    return sent


async def emit_decision_resolved(
    decision_id: str,
    selected_option: Dict[str, Any],
    owner_id: str,
) -> int:
    """Emit decision resolved event"""
    message = WSMessage(
        type=WSMessageType.DECISION_RESOLVED,
        payload={
            "decision_id": decision_id,
            "selected_option": selected_option,
        },
    )
    
    sent = await manager.broadcast_to_channel(f"user:{owner_id}", message)
    sent += await manager.broadcast_to_channel("decisions", message)
    return sent


# ============================================================================
# NOTIFICATION EVENT EMITTERS
# ============================================================================

async def emit_notification(
    user_id: str,
    notification_id: str,
    title: str,
    message_text: str,
    notification_type: str,
    action_url: str = None,
) -> int:
    """Emit notification event"""
    message = WSMessage(
        type=WSMessageType.NOTIFICATION,
        payload={
            "notification_id": notification_id,
            "title": title,
            "message": message_text,
            "type": notification_type,
            "action_url": action_url,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


async def emit_notification_count(
    user_id: str,
    unread_count: int,
) -> int:
    """Emit notification count update"""
    message = WSMessage(
        type=WSMessageType.NOTIFICATION_COUNT,
        payload={
            "unread_count": unread_count,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


# ============================================================================
# AGENT EVENT EMITTERS
# ============================================================================

async def emit_agent_hired(
    agent_id: str,
    agent_name: str,
    user_id: str,
) -> int:
    """Emit agent hired event"""
    message = WSMessage(
        type=WSMessageType.AGENT_HIRED,
        payload={
            "agent_id": agent_id,
            "agent_name": agent_name,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


async def emit_agent_dismissed(
    agent_id: str,
    agent_name: str,
    user_id: str,
) -> int:
    """Emit agent dismissed event"""
    message = WSMessage(
        type=WSMessageType.AGENT_DISMISSED,
        payload={
            "agent_id": agent_id,
            "agent_name": agent_name,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


# ============================================================================
# NOVA EVENT EMITTERS
# ============================================================================

async def emit_nova_typing(user_id: str) -> int:
    """Emit Nova typing indicator"""
    message = WSMessage(
        type=WSMessageType.NOVA_TYPING,
        payload={"typing": True},
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


async def emit_nova_response(
    user_id: str,
    response: str,
    pipeline_status: Dict[str, str] = None,
) -> int:
    """Emit Nova response"""
    message = WSMessage(
        type=WSMessageType.NOVA_RESPONSE,
        payload={
            "response": response,
            "pipeline_status": pipeline_status,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


# ============================================================================
# GOVERNANCE EVENT EMITTERS
# ============================================================================

async def emit_governance_alert(
    user_id: str,
    alert_type: str,
    message_text: str,
    severity: str = "warning",
) -> int:
    """Emit governance alert"""
    message = WSMessage(
        type=WSMessageType.GOVERNANCE_ALERT,
        payload={
            "alert_type": alert_type,
            "message": message_text,
            "severity": severity,
        },
    )
    
    return await manager.broadcast_to_channel(f"user:{user_id}", message)


# ============================================================================
# STATS ENDPOINT
# ============================================================================

@ws_router.get("/stats")
async def websocket_stats():
    """Get WebSocket statistics"""
    return {
        "active_connections": manager.connection_count,
        "channels": {
            "checkpoints": manager.get_channel_subscribers("checkpoints"),
            "xr-packs": manager.get_channel_subscribers("xr-packs"),
        },
    }
