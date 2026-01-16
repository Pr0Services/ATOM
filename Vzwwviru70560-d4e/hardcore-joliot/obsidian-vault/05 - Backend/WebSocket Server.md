# WebSocket Server

> Serveur real-time pour L'Essaim (350 agents @ 60fps)

---

## Vue d'Ensemble

Le serveur WebSocket gere les connexions real-time pour:
- Streaming des positions de 350 agents
- Updates a 60fps (16ms interval)
- Maximum 500 connexions simultanees

---

## Configuration

### Fichier: `backend/websocket_server.py`

```python
# Constants
ESSAIM_SIZE = 350
TARGET_FREQUENCY = 999  # Hz
UPDATE_INTERVAL = 1 / 60  # 60fps
MAX_CONNECTIONS = 500
```

### Docker: `backend/Dockerfile.websocket`

```dockerfile
EXPOSE 8001
CMD ["uvicorn", "websocket_server:app",
     "--host", "0.0.0.0",
     "--port", "8001",
     "--ws", "websockets",
     "--loop", "uvloop"]
```

---

## Endpoints WebSocket

### /ws/swarm

Streaming des 350 agents en temps reel.

**Connection**
```javascript
const ws = new WebSocket('wss://api.domain.com/ws/swarm');
```

**Message Initial**
```json
{
  "type": "connected",
  "frequency": 999,
  "agent_count": 350
}
```

**Update Frame (60fps)**
```json
{
  "type": "swarm_update",
  "timestamp": "2025-01-16T10:00:00Z",
  "frequency": 999,
  "agent_count": 350,
  "agents": [
    {
      "id": 0,
      "sphere": "personal",
      "x": 0.5234,
      "y": -0.1234,
      "z": 0.8765,
      "frequency": 987.3
    },
    // ... 349 more agents
  ]
}
```

**Heartbeat (every 30s)**
```json
{
  "type": "heartbeat",
  "frequency": 999,
  "connections": 42
}
```

### /ws/frequency

Monitoring de la frequence globale.

**Update (10/sec)**
```json
{
  "type": "frequency_update",
  "frequency": 993.45,
  "target": 999,
  "harmony": true,
  "timestamp": "2025-01-16T10:00:00Z"
}
```

---

## Connection Manager

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> bool:
        """Accept connection if under limit."""
        if len(self.active_connections) >= MAX_CONNECTIONS:
            return False
        await websocket.accept()
        self.active_connections.add(websocket)
        return True

    async def disconnect(self, websocket: WebSocket):
        """Remove connection."""
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast to all connections."""
        data = json.dumps(message)
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(data)
            except:
                await self.disconnect(connection)
```

---

## Swarm Generator

Generation des positions avec mouvement organique:

```python
class SwarmGenerator:
    def update(self, dt: float) -> list:
        for agent in self.agents:
            # Perlin-like noise
            noise_x = math.sin(time * 0.5 + agent["id"] * 0.1)
            noise_y = math.cos(time * 0.3 + agent["id"] * 0.15)
            noise_z = math.sin(time * 0.4 + agent["id"] * 0.12)

            # Update velocity with smoothing
            agent["vx"] = agent["vx"] * 0.98 + noise_x * 0.002
            agent["vy"] = agent["vy"] * 0.98 + noise_y * 0.002
            agent["vz"] = agent["vz"] * 0.98 + noise_z * 0.002

            # Update position
            agent["x"] += agent["vx"]
            agent["y"] += agent["vy"]
            agent["z"] += agent["vz"]

            # Sphere constraint
            if distance > 1.0:
                normalize()

        return self.agents
```

---

## Performance

### Optimisations
- uvloop pour async IO
- Single worker (async efficace)
- Batch broadcasts
- Connection pooling

### Metriques
| Metrique | Valeur |
|----------|--------|
| Latence cible | < 50ms |
| Frame rate | 60fps |
| Bandwidth/client | ~100KB/s |
| Max connections | 500 |

---

## Nginx Configuration

```nginx
location /ws/ {
    proxy_pass http://atom-websocket:8001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 7d;
    proxy_send_timeout 7d;
}
```

---

## Health Check

```
GET /health

Response:
{
  "status": "healthy",
  "frequency": 999,
  "essaim_size": 350,
  "connections": 42,
  "max_connections": 500
}
```

---

## Liens

- [[Backend Structure]]
- [[350 Agents]]
- [[Deployment Guide]]

#websocket #realtime #essaim #streaming
