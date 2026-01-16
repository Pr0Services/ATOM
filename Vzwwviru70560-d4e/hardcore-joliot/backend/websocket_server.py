"""
AT·OM WEBSOCKET SERVER
======================

Canon AT·OM - L'Essaim Real-Time Server
Optimized for 350+ simultaneous WebSocket connections.

ZERO LOG: No personal data stored.
Only technical health metrics for 999Hz frequency.
"""

from __future__ import annotations

import asyncio
import json
import math
import random
import time
from datetime import datetime
from typing import Dict, Set, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

# =============================================================================
# CONSTANTS - Canon AT·OM
# =============================================================================

ESSAIM_SIZE = 350
TARGET_FREQUENCY = 999  # Hz
UPDATE_INTERVAL = 1 / 60  # 60fps
MAX_CONNECTIONS = 500

# =============================================================================
# CONNECTION MANAGER
# =============================================================================

class ConnectionManager:
    """Manages WebSocket connections for L'Essaim."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> bool:
        """Accept new connection if under limit."""
        if len(self.active_connections) >= MAX_CONNECTIONS:
            return False

        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)
        return True

    async def disconnect(self, websocket: WebSocket):
        """Remove connection."""
        async with self._lock:
            self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast to all connections."""
        if not self.active_connections:
            return

        data = json.dumps(message)
        disconnected = []

        for connection in self.active_connections.copy():
            try:
                await connection.send_text(data)
            except Exception:
                disconnected.append(connection)

        # Clean up disconnected
        for conn in disconnected:
            await self.disconnect(conn)

    @property
    def connection_count(self) -> int:
        return len(self.active_connections)


manager = ConnectionManager()

# =============================================================================
# AGENT POSITION GENERATOR
# =============================================================================

class SwarmGenerator:
    """Generates positions for 350 agents in L'Essaim."""

    def __init__(self):
        self.agents = self._initialize_agents()
        self.time_offset = 0

    def _initialize_agents(self) -> list:
        """Initialize 350 agents with random positions."""
        agents = []

        # Sphere distribution (Canon AT·OM)
        spheres = [
            ("personal", 28),
            ("business", 43),
            ("government", 18),
            ("creative_studio", 42),
            ("community", 12),
            ("social_media", 15),
            ("entertainment", 8),
            ("my_team", 35),
            ("scholar", 25),
            ("transport", 50),
            ("societal", 20),
            ("environment", 25),
            ("privacy", 8),
            ("jeunesse", 15),
            ("dashboard", 6),
        ]

        agent_id = 0
        for sphere, count in spheres:
            for i in range(count):
                # Random starting position in normalized space
                theta = random.uniform(0, 2 * math.pi)
                phi = random.uniform(0, math.pi)
                r = random.uniform(0.3, 1.0)

                agents.append({
                    "id": agent_id,
                    "sphere": sphere,
                    "x": r * math.sin(phi) * math.cos(theta),
                    "y": r * math.sin(phi) * math.sin(theta),
                    "z": r * math.cos(phi),
                    "vx": random.uniform(-0.01, 0.01),
                    "vy": random.uniform(-0.01, 0.01),
                    "vz": random.uniform(-0.01, 0.01),
                    "frequency": random.uniform(432, TARGET_FREQUENCY),
                })
                agent_id += 1

        return agents

    def update(self, dt: float) -> list:
        """Update agent positions with organic movement."""
        self.time_offset += dt

        for agent in self.agents:
            # Organic movement using Perlin-like noise
            noise_x = math.sin(self.time_offset * 0.5 + agent["id"] * 0.1)
            noise_y = math.cos(self.time_offset * 0.3 + agent["id"] * 0.15)
            noise_z = math.sin(self.time_offset * 0.4 + agent["id"] * 0.12)

            # Update velocity with noise
            agent["vx"] = agent["vx"] * 0.98 + noise_x * 0.002
            agent["vy"] = agent["vy"] * 0.98 + noise_y * 0.002
            agent["vz"] = agent["vz"] * 0.98 + noise_z * 0.002

            # Update position
            agent["x"] += agent["vx"]
            agent["y"] += agent["vy"]
            agent["z"] += agent["vz"]

            # Keep within bounds (sphere constraint)
            distance = math.sqrt(
                agent["x"]**2 + agent["y"]**2 + agent["z"]**2
            )
            if distance > 1.0:
                factor = 0.99 / distance
                agent["x"] *= factor
                agent["y"] *= factor
                agent["z"] *= factor

            # Frequency oscillation toward 999Hz
            agent["frequency"] += (TARGET_FREQUENCY - agent["frequency"]) * 0.01
            agent["frequency"] += random.uniform(-1, 1)
            agent["frequency"] = max(432, min(TARGET_FREQUENCY, agent["frequency"]))

        return self.agents

    def get_state(self) -> dict:
        """Get current swarm state."""
        return {
            "type": "swarm_update",
            "timestamp": datetime.utcnow().isoformat(),
            "frequency": TARGET_FREQUENCY,
            "agent_count": len(self.agents),
            "agents": [
                {
                    "id": a["id"],
                    "sphere": a["sphere"],
                    "x": round(a["x"], 4),
                    "y": round(a["y"], 4),
                    "z": round(a["z"], 4),
                    "frequency": round(a["frequency"], 1),
                }
                for a in self.agents
            ]
        }


swarm = SwarmGenerator()

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def swarm_broadcast_loop():
    """Continuously broadcast swarm positions at 60fps."""
    last_time = time.time()

    while True:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        if manager.connection_count > 0:
            swarm.update(dt)
            state = swarm.get_state()
            await manager.broadcast(state)

        # Maintain 60fps
        elapsed = time.time() - current_time
        sleep_time = max(0, UPDATE_INTERVAL - elapsed)
        await asyncio.sleep(sleep_time)


# =============================================================================
# FASTAPI APP
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Start broadcast loop
    broadcast_task = asyncio.create_task(swarm_broadcast_loop())
    yield
    # Cleanup
    broadcast_task.cancel()
    try:
        await broadcast_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="AT·OM WebSocket Server",
    description="L'Essaim Real-Time - 350 Agents",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://atom-interface.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """Technical health check - ZERO LOG."""
    return {
        "status": "healthy",
        "frequency": TARGET_FREQUENCY,
        "essaim_size": ESSAIM_SIZE,
        "connections": manager.connection_count,
        "max_connections": MAX_CONNECTIONS,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.websocket("/ws/swarm")
async def websocket_swarm(
    websocket: WebSocket,
    session_id: Optional[str] = Query(None, alias="session")
):
    """
    WebSocket endpoint for L'Essaim real-time updates.

    Streams 350 agent positions at 60fps.
    ZERO LOG: No personal data transmitted.
    """
    # Note: Session validation should be done by checking with API
    # For now, accept all connections up to limit

    connected = await manager.connect(websocket)
    if not connected:
        await websocket.close(code=1013, reason="Max connections reached")
        return

    try:
        # Send initial state
        await websocket.send_json({
            "type": "connected",
            "frequency": TARGET_FREQUENCY,
            "agent_count": ESSAIM_SIZE,
        })

        # Keep connection alive, receive any client messages
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )

                # Handle client messages
                message = json.loads(data)

                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat(),
                    })

            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    "type": "heartbeat",
                    "frequency": TARGET_FREQUENCY,
                    "connections": manager.connection_count,
                })

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        await manager.disconnect(websocket)


@app.websocket("/ws/frequency")
async def websocket_frequency(websocket: WebSocket):
    """
    WebSocket endpoint for frequency monitoring.

    Streams 999Hz resonance status.
    """
    connected = await manager.connect(websocket)
    if not connected:
        await websocket.close(code=1013, reason="Max connections reached")
        return

    try:
        while True:
            # Calculate average frequency across swarm
            avg_freq = sum(a["frequency"] for a in swarm.agents) / len(swarm.agents)

            await websocket.send_json({
                "type": "frequency_update",
                "frequency": round(avg_freq, 2),
                "target": TARGET_FREQUENCY,
                "harmony": avg_freq >= TARGET_FREQUENCY - 10,
                "timestamp": datetime.utcnow().isoformat(),
            })

            await asyncio.sleep(0.1)  # 10 updates per second

    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(websocket)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "websocket_server:app",
        host="0.0.0.0",
        port=8001,
        ws="websockets",
        loop="uvloop",
    )
