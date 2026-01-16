# Backend Structure

> Architecture backend AT·OM (FastAPI + Python)

---

## Structure des Dossiers

```
backend/
├── main.py                     # Point d'entree FastAPI
├── requirements.txt            # Dependances Python
├── Dockerfile                  # Container API
├── Dockerfile.websocket        # Container WebSocket
├── websocket_server.py         # Serveur L'Essaim
│
├── api/
│   └── v1/
│       ├── __init__.py
│       └── routes/
│           ├── atom/
│           │   ├── swarm_routes.py    # Endpoints L'Essaim
│           │   └── sceau_routes.py    # Activation Sceau
│           ├── health.py              # Health checks
│           └── modules/               # Routes par module
│
├── core/
│   ├── config/
│   │   └── settings.py         # Configuration
│   └── security/
│       └── ethical_safeguard.py # Brise-Circuit
│
├── models/
│   ├── agent.py                # Modele Agent
│   ├── sphere.py               # Modele Sphere
│   └── session.py              # Modele Session
│
├── schemas/
│   ├── agent_schemas.py        # Schemas Pydantic
│   └── response_schemas.py     # Responses API
│
└── services/
    ├── swarm_service.py        # Logique L'Essaim
    └── frequency_service.py    # Gestion frequences
```

---

## Configuration

### Settings (core/config/settings.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AT·OM Canon
    FREQUENCY: int = 999
    ESSAIM_SIZE: int = 350
    SCEAU_DURATION: int = 2000  # ms
    ZERO_LOG: bool = True

    # Security
    SECRET_KEY: str
    CORS_ORIGINS: list[str] = ["https://atom-interface.vercel.app"]

    class Config:
        env_file = ".env"
```

---

## Modeles

### Agent (models/agent.py)

```python
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    sphere = Column(String, nullable=False)
    name = Column(String, nullable=False)
    function = Column(String, nullable=False)
    frequency = Column(Float, default=999.0)
    status = Column(String, default="active")

    # Position 3D
    pos_x = Column(Float, default=0.0)
    pos_y = Column(Float, default=0.0)
    pos_z = Column(Float, default=0.0)
```

### Session (models/session.py)

```python
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    sceau_validated = Column(Boolean, default=False)
    frequency = Column(Float, default=999.0)
    # ZERO LOG: Pas de donnees personnelles
```

---

## Schemas Pydantic

### Agent Distribution (schemas/agent_schemas.py)

```python
from enum import Enum

class SphereType(str, Enum):
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"
    # V68 Expansions
    TRANSPORT = "transport"
    SOCIETAL = "societal"
    ENVIRONMENT = "environment"
    PRIVACY = "privacy"
    JEUNESSE = "jeunesse"
    DASHBOARD = "dashboard"

AGENT_DISTRIBUTION = {
    SphereType.PERSONAL: 28,
    SphereType.BUSINESS: 43,
    SphereType.GOVERNMENT: 18,
    SphereType.CREATIVE_STUDIO: 42,
    SphereType.COMMUNITY: 12,
    SphereType.SOCIAL_MEDIA: 15,
    SphereType.ENTERTAINMENT: 8,
    SphereType.MY_TEAM: 35,
    SphereType.SCHOLAR: 25,
    SphereType.TRANSPORT: 50,
    SphereType.SOCIETAL: 20,
    SphereType.ENVIRONMENT: 25,
    SphereType.PRIVACY: 8,
    SphereType.JEUNESSE: 15,
    SphereType.DASHBOARD: 6,
}

TOTAL_AGENTS = 350  # Sum of all spheres
```

---

## Services

### Swarm Service

```python
class SwarmService:
    def __init__(self):
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> list[Agent]:
        """Initialize 350 agents from distribution."""
        agents = []
        agent_id = 0
        for sphere, count in AGENT_DISTRIBUTION.items():
            for i in range(count):
                agents.append(Agent(
                    id=agent_id,
                    sphere=sphere,
                    frequency=random.uniform(432, 999),
                ))
                agent_id += 1
        return agents

    def get_all_agents(self) -> list[dict]:
        """Return all 350 agents state."""
        return [a.to_dict() for a in self.agents]

    def disperse(self, level: str) -> int:
        """Disperse agents based on level."""
        count = {
            "partial": int(350 * 0.2),
            "sectoral": int(350 * 0.5),
            "total": 350
        }[level]
        # Mark agents as dispersed
        return count
```

---

## Middlewares

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Session Validation

```python
async def validate_sceau_session(request: Request):
    """Validate X-Sceau-Session header."""
    session_id = request.headers.get("X-Sceau-Session")
    if not session_id:
        raise HTTPException(401, "Sceau session required")
    # Validate session
    return session_id
```

---

## Liens

- [[WebSocket Server]]
- [[API Reference]]
- [[Security Protocol]]

#backend #fastapi #python #structure
