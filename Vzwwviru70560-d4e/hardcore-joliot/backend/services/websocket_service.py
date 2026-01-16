"""
CHE·NU™ V75 - WebSocket Service
Complete real-time communication service.

GOUVERNANCE > EXÉCUTION
- All events are logged
- Sensitive actions require checkpoint approval
- No autonomous broadcasts

@version 75.0.0
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# ============================================================================
# EVENT TYPES
# ============================================================================

class EventType(str, Enum):
    """WebSocket event types."""
    
    # Connection
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    PING = "ping"
    PONG = "pong"
    
    # Governance (CRITICAL)
    CHECKPOINT_CREATED = "checkpoint.created"
    CHECKPOINT_RESOLVED = "checkpoint.resolved"
    CHECKPOINT_URGENT = "checkpoint.urgent"
    DECISION_REQUIRED = "decision.required"
    
    # Threads
    THREAD_CREATED = "thread.created"
    THREAD_UPDATED = "thread.updated"
    THREAD_ARCHIVED = "thread.archived"
    MESSAGE_ADDED = "message.added"
    
    # Agents
    AGENT_HIRED = "agent.hired"
    AGENT_FIRED = "agent.fired"
    AGENT_STATUS = "agent.status"
    AGENT_ACTION = "agent.action"
    
    # Nova
    NOVA_RESPONSE = "nova.response"
    NOVA_THINKING = "nova.thinking"
    NOVA_COMPLETE = "nova.complete"
    
    # Notifications
    NOTIFICATION = "notification"
    ALERT = "alert"
    
    # Sync
    SYNC_REQUEST = "sync.request"
    SYNC_RESPONSE = "sync.response"
    
    # XR (READ ONLY events)
    XR_UPDATE = "xr.update"
    XR_VERIFIED = "xr.verified"


# ============================================================================
# MESSAGE MODELS
# ============================================================================

class WSMessage(BaseModel):
    """WebSocket message structure."""
    event: EventType
    data: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps({
            "event": self.event.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id or str(uuid4()),
        })


class Connection(BaseModel):
    """Client connection info."""
    id: str
    user_id: str
    connected_at: datetime
    subscriptions: Set[str] = set()
    
    class Config:
        arbitrary_types_allowed = True


# ============================================================================
# CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """
    Manages WebSocket connections.
    
    Features:
    - Per-user connections
    - Room/channel subscriptions
    - Broadcast with filters
    - Connection health checks
    """
    
    def __init__(self):
        # user_id -> list of websockets
        self._connections: Dict[str, List[WebSocket]] = {}
        # connection_id -> Connection info
        self._connection_info: Dict[str, Connection] = {}
        # room -> set of user_ids
        self._rooms: Dict[str, Set[str]] = {}
        # Event handlers
        self._handlers: Dict[EventType, List[Callable]] = {}
        # Lock for thread safety
        self._lock = asyncio.Lock()
    
    # ========================================================================
    # CONNECTION MANAGEMENT
    # ========================================================================
    
    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
    ) -> str:
        """Accept and register a new connection."""
        await websocket.accept()
        
        connection_id = str(uuid4())
        
        async with self._lock:
            if user_id not in self._connections:
                self._connections[user_id] = []
            
            self._connections[user_id].append(websocket)
            self._connection_info[connection_id] = Connection(
                id=connection_id,
                user_id=user_id,
                connected_at=datetime.utcnow(),
            )
        
        logger.info(f"User {user_id} connected (conn: {connection_id})")
        
        # Send connection confirmation
        await self.send_to_user(user_id, WSMessage(
            event=EventType.CONNECTED,
            data={
                "connection_id": connection_id,
                "user_id": user_id,
                "server_time": datetime.utcnow().isoformat(),
            }
        ))
        
        return connection_id
    
    async def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a connection."""
        async with self._lock:
            if user_id in self._connections:
                try:
                    self._connections[user_id].remove(websocket)
                    if not self._connections[user_id]:
                        del self._connections[user_id]
                except ValueError:
                    pass
            
            # Remove from rooms
            for room_users in self._rooms.values():
                room_users.discard(user_id)
        
        logger.info(f"User {user_id} disconnected")
    
    def get_connection_count(self) -> int:
        """Get total number of connections."""
        return sum(len(conns) for conns in self._connections.values())
    
    def get_user_count(self) -> int:
        """Get number of connected users."""
        return len(self._connections)
    
    def is_user_connected(self, user_id: str) -> bool:
        """Check if user has active connections."""
        return user_id in self._connections and len(self._connections[user_id]) > 0
    
    # ========================================================================
    # ROOM MANAGEMENT
    # ========================================================================
    
    async def join_room(self, user_id: str, room: str):
        """Add user to a room."""
        async with self._lock:
            if room not in self._rooms:
                self._rooms[room] = set()
            self._rooms[room].add(user_id)
        
        logger.debug(f"User {user_id} joined room {room}")
    
    async def leave_room(self, user_id: str, room: str):
        """Remove user from a room."""
        async with self._lock:
            if room in self._rooms:
                self._rooms[room].discard(user_id)
        
        logger.debug(f"User {user_id} left room {room}")
    
    def get_room_users(self, room: str) -> Set[str]:
        """Get users in a room."""
        return self._rooms.get(room, set()).copy()
    
    # ========================================================================
    # MESSAGE SENDING
    # ========================================================================
    
    async def send_to_user(self, user_id: str, message: WSMessage):
        """Send message to specific user (all their connections)."""
        if user_id not in self._connections:
            return
        
        json_msg = message.to_json()
        dead_connections = []
        
        for websocket in self._connections[user_id]:
            try:
                await websocket.send_text(json_msg)
            except Exception as e:
                logger.warning(f"Failed to send to {user_id}: {e}")
                dead_connections.append(websocket)
        
        # Clean up dead connections
        for ws in dead_connections:
            await self.disconnect(ws, user_id)
    
    async def send_to_room(self, room: str, message: WSMessage, exclude: Optional[str] = None):
        """Send message to all users in a room."""
        users = self.get_room_users(room)
        
        for user_id in users:
            if user_id != exclude:
                await self.send_to_user(user_id, message)
    
    async def broadcast(
        self,
        message: WSMessage,
        exclude: Optional[Set[str]] = None,
    ):
        """Broadcast to all connected users."""
        exclude = exclude or set()
        
        for user_id in list(self._connections.keys()):
            if user_id not in exclude:
                await self.send_to_user(user_id, message)
    
    # ========================================================================
    # GOVERNANCE EVENTS (CRITICAL)
    # ========================================================================
    
    async def notify_checkpoint_created(
        self,
        checkpoint_id: str,
        checkpoint_type: str,
        title: str,
        urgency: str,
        target_user_id: str,
    ):
        """Notify about new checkpoint requiring human decision."""
        message = WSMessage(
            event=EventType.CHECKPOINT_CREATED,
            data={
                "checkpoint_id": checkpoint_id,
                "type": checkpoint_type,
                "title": title,
                "urgency": urgency,
                "requires_human_action": True,
            }
        )
        await self.send_to_user(target_user_id, message)
        
        # If urgent, also send alert
        if urgency == "urgent":
            await self.send_to_user(target_user_id, WSMessage(
                event=EventType.CHECKPOINT_URGENT,
                data={
                    "checkpoint_id": checkpoint_id,
                    "title": title,
                    "message": "⚠️ Action urgente requise",
                }
            ))
    
    async def notify_decision_required(
        self,
        decision_id: str,
        title: str,
        description: str,
        options: List[Dict],
        target_user_id: str,
    ):
        """Notify that human decision is required."""
        await self.send_to_user(target_user_id, WSMessage(
            event=EventType.DECISION_REQUIRED,
            data={
                "decision_id": decision_id,
                "title": title,
                "description": description,
                "options": options,
                "auto_approve": False,  # NEVER auto approve
            }
        ))
    
    # ========================================================================
    # THREAD EVENTS
    # ========================================================================
    
    async def notify_thread_update(
        self,
        thread_id: str,
        event_type: EventType,
        data: Dict[str, Any],
        room: Optional[str] = None,
    ):
        """Notify about thread updates."""
        message = WSMessage(
            event=event_type,
            data={"thread_id": thread_id, **data}
        )
        
        if room:
            await self.send_to_room(room, message)
        else:
            await self.send_to_room(f"thread:{thread_id}", message)
    
    async def notify_message_added(
        self,
        thread_id: str,
        message_data: Dict[str, Any],
    ):
        """Notify about new message in thread."""
        await self.notify_thread_update(
            thread_id,
            EventType.MESSAGE_ADDED,
            {"message": message_data}
        )
    
    # ========================================================================
    # NOVA EVENTS
    # ========================================================================
    
    async def stream_nova_response(
        self,
        user_id: str,
        conversation_id: str,
        chunk: str,
        is_complete: bool = False,
    ):
        """Stream Nova response to user."""
        event = EventType.NOVA_COMPLETE if is_complete else EventType.NOVA_RESPONSE
        
        await self.send_to_user(user_id, WSMessage(
            event=event,
            data={
                "conversation_id": conversation_id,
                "chunk": chunk,
                "complete": is_complete,
            }
        ))
    
    async def notify_nova_thinking(self, user_id: str, conversation_id: str):
        """Notify that Nova is processing."""
        await self.send_to_user(user_id, WSMessage(
            event=EventType.NOVA_THINKING,
            data={
                "conversation_id": conversation_id,
                "status": "thinking",
            }
        ))
    
    # ========================================================================
    # HEARTBEAT
    # ========================================================================
    
    async def handle_ping(self, websocket: WebSocket, user_id: str):
        """Handle ping and respond with pong."""
        try:
            await websocket.send_text(WSMessage(
                event=EventType.PONG,
                data={"timestamp": datetime.utcnow().isoformat()}
            ).to_json())
        except Exception:
            pass
    
    async def health_check(self):
        """Periodic health check of connections."""
        for user_id in list(self._connections.keys()):
            for ws in self._connections.get(user_id, []):
                try:
                    await ws.send_text(WSMessage(
                        event=EventType.PING,
                        data={}
                    ).to_json())
                except Exception:
                    await self.disconnect(ws, user_id)


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

ws_manager = ConnectionManager()


# ============================================================================
# WEBSOCKET HANDLER
# ============================================================================

async def websocket_handler(
    websocket: WebSocket,
    user_id: str,
    manager: ConnectionManager = ws_manager,
):
    """
    Main WebSocket handler.
    
    Protocol:
    - Connect with user_id
    - Send/receive JSON messages
    - Handle events based on type
    """
    connection_id = await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                event = message.get("event")
                payload = message.get("data", {})
                
                # Handle ping
                if event == "ping":
                    await manager.handle_ping(websocket, user_id)
                
                # Handle room subscription
                elif event == "subscribe":
                    room = payload.get("room")
                    if room:
                        await manager.join_room(user_id, room)
                
                elif event == "unsubscribe":
                    room = payload.get("room")
                    if room:
                        await manager.leave_room(user_id, room)
                
                # Handle sync request
                elif event == "sync":
                    await manager.send_to_user(user_id, WSMessage(
                        event=EventType.SYNC_RESPONSE,
                        data={"status": "synced", "timestamp": datetime.utcnow().isoformat()}
                    ))
                
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from {user_id}: {data[:100]}")
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for {user_id}: {e}")
        await manager.disconnect(websocket, user_id)
