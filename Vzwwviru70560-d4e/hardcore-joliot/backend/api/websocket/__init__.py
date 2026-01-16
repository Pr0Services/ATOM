"""CHE·NU™ V82 — WebSocket"""
from .streaming import (
    ws_router,
    manager,
    ConnectionManager,
    WSMessage,
    WSMessageType,
    emit_simulation_update,
    emit_agent_event,
    emit_checkpoint_created,
    emit_checkpoint_resolved,
    emit_xr_pack_ready,
)

# Alias for backward compatibility with main.py
websocket_router = ws_router

__all__ = [
    "ws_router", "websocket_router", "manager", "ConnectionManager",
    "WSMessage", "WSMessageType",
    "emit_simulation_update", "emit_agent_event",
    "emit_checkpoint_created", "emit_checkpoint_resolved",
    "emit_xr_pack_ready",
]
