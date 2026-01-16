# API Reference

> Reference complete des endpoints API AT·OM

---

## Base URL

```
Production: https://api.your-domain.com/api/v1
Development: http://localhost:8000/api/v1
```

---

## Authentication

### Sceau Session

Toutes les requetes (sauf activation) necessitent le header:

```
X-Sceau-Session: <session_id>
```

Le session_id est obtenu apres activation du Sceau (2s touch).

---

## Endpoints

### Health Check

```http
GET /health
```

**Response**
```json
{
  "status": "healthy",
  "frequency": 999,
  "essaim_size": 350,
  "timestamp": "2025-01-16T10:00:00Z"
}
```

---

### Sceau (Activation)

#### POST /sceau/activate

Active une nouvelle session souveraine.

**Request**
```json
{
  "duration_ms": 2000,
  "frequency_reached": 999
}
```

**Response**
```json
{
  "success": true,
  "session_id": "uuid-v4",
  "frequency": 999,
  "expires_at": "2025-01-16T11:00:00Z"
}
```

**Errors**
| Code | Message |
|------|---------|
| 400 | Duration must be >= 2000ms |
| 400 | Frequency must reach 999Hz |

---

### Swarm (L'Essaim)

#### POST /swarm/activate

Declenche l'explosion de L'Essaim (apres Sceau).

**Headers**
```
X-Sceau-Session: <session_id>
```

**Response**
```json
{
  "success": true,
  "agent_count": 350,
  "spheres": 16,
  "frequency": 999,
  "ws_url": "wss://api.domain.com/ws/swarm"
}
```

#### GET /swarm/status

Retourne l'etat actuel de L'Essaim.

**Response**
```json
{
  "active": true,
  "agent_count": 350,
  "frequency": 993.45,
  "harmony": true,
  "spheres": {
    "personal": { "count": 28, "active": 28 },
    "business": { "count": 43, "active": 43 },
    // ... autres spheres
  }
}
```

---

### Modules

#### GET /modules/status

Retourne la sante de tous les modules.

**Response**
```json
{
  "modules": {
    "genie": { "status": "active", "agents": 15 },
    "alchimie": { "status": "active", "agents": 8 },
    "flux": { "status": "active", "agents": 12 },
    "sante": { "status": "active", "agents": 10 }
  },
  "total_agents": 350,
  "system_frequency": 999
}
```

---

### Protocol-999 (Kill-Switch)

#### DELETE /protocol-999

Active le Brise-Circuit (dispersion).

**Headers**
```
X-Sceau-Session: <session_id>
X-Confirmation-Code: <code>
```

**Request**
```json
{
  "level": "partial|sectoral|total",
  "reason": "string (optional)",
  "sphere": "string (required if sectoral)"
}
```

**Response**
```json
{
  "success": true,
  "level": "partial",
  "dispersed_count": 70,
  "remaining_count": 280,
  "timestamp": "2025-01-16T10:00:00Z"
}
```

**Levels**
| Level | Dispersed |
|-------|-----------|
| partial | 20% (70 agents) |
| sectoral | 50% (175 agents) |
| total | 100% (350 agents) |

---

### Security

#### GET /security/status

Retourne l'etat de securite systeme.

**Response**
```json
{
  "state": "nominal",
  "frequency": 999,
  "violations": 0,
  "last_check": "2025-01-16T10:00:00Z"
}
```

#### POST /security/verify

Verifie une signature de frequence.

**Request**
```json
{
  "signature": {
    "timestamp": "2025-01-16T10:00:00Z",
    "frequency": 999,
    "duration_ms": 2000,
    "harmony_level": 0.98
  }
}
```

**Response**
```json
{
  "valid": true,
  "harmony": true,
  "confidence": 0.98
}
```

---

## WebSocket Endpoints

### /ws/swarm

Streaming real-time des 350 agents.

**URL**: `wss://api.domain.com/ws/swarm`

**Query Parameters**
| Param | Description |
|-------|-------------|
| session | Session ID from Sceau |

**Messages**

*Connected*
```json
{ "type": "connected", "agent_count": 350 }
```

*Update (60fps)*
```json
{
  "type": "swarm_update",
  "agents": [
    { "id": 0, "sphere": "personal", "x": 0.5, "y": -0.2, "z": 0.8, "frequency": 987 }
  ]
}
```

*Heartbeat (30s)*
```json
{ "type": "heartbeat", "connections": 42 }
```

### /ws/frequency

Monitoring frequence globale.

**URL**: `wss://api.domain.com/ws/frequency`

**Messages (10/sec)**
```json
{
  "type": "frequency_update",
  "frequency": 993.45,
  "target": 999,
  "harmony": true
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing/invalid session |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Server Error |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| /sceau/activate | 10/minute |
| /swarm/* | 100/minute |
| /protocol-999 | 1/hour |
| WebSocket | 500 connections |

---

## Liens

- [[Backend Structure]]
- [[WebSocket Server]]
- [[Security Protocol]]

#api #reference #endpoints #rest
