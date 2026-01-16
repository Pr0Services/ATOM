# System Architecture

> Vue d'ensemble technique de l'ecosysteme AT·OM

---

## Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Vercel (CDN)                        │    │
│  │  React + TypeScript + Vite + TailwindCSS            │    │
│  │  PWA iPad Fullscreen                                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Nginx     │  │  FastAPI    │  │  WebSocket  │         │
│  │  SSL/Proxy  │──│   API       │  │   Server    │         │
│  └─────────────┘  └──────┬──────┘  └──────┬──────┘         │
│                          │                 │                 │
│                          ▼                 ▼                 │
│                    ┌─────────────────────────┐              │
│                    │        Redis            │              │
│                    │      (Pub/Sub)          │              │
│                    └─────────────────────────┘              │
│                          │                                   │
│                          ▼                                   │
│                    ┌─────────────────────────┐              │
│                    │      Supabase           │              │
│                    │   (PostgreSQL + Auth)   │              │
│                    └─────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Stack Technique

### Frontend
| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type Safety |
| Vite | 5.x | Build Tool |
| TailwindCSS | 3.x | Styling |
| Framer Motion | 11.x | Animations |
| Three.js | 0.160+ | 3D Rendering |

### Backend
| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11 | Runtime |
| FastAPI | 0.109+ | API Framework |
| Uvicorn | 0.27+ | ASGI Server |
| Pydantic | 2.x | Validation |
| SQLAlchemy | 2.x | ORM |
| Redis | 7.x | Cache/Pub-Sub |

### Infrastructure
| Service | Provider | Usage |
|---------|----------|-------|
| Frontend Hosting | Vercel | CDN + Edge |
| Backend Hosting | DigitalOcean | Droplet |
| Database | Supabase | PostgreSQL |
| Cache | Redis | Session/Pub-Sub |

---

## Structure des Dossiers

```
hardcore-joliot/
├── atom/
│   └── interface/              # Frontend React
│       ├── src/
│       │   ├── components/     # Composants reutilisables
│       │   ├── pages/          # Pages Canon AT·OM
│       │   ├── hooks/          # Custom hooks
│       │   ├── stores/         # State management
│       │   └── utils/          # Utilitaires
│       └── public/             # Assets statiques
│
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── routes/         # Endpoints API
│   ├── core/
│   │   ├── security/           # Ethical Safeguard
│   │   └── config/             # Configuration
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas
│   └── services/               # Business logic
│
├── deployment/
│   ├── docker-compose.yml      # Orchestration
│   ├── nginx/                  # Reverse proxy
│   └── .env.production         # Env vars
│
└── obsidian-vault/             # Documentation
```

---

## Flux de Donnees

### Activation du Sceau
```
1. User: Touch 2s on screen
2. Frontend: POST /api/v1/sceau/activate
3. Backend: Validate duration >= 2s
4. Backend: Create session token
5. Frontend: Store X-Sceau-Session header
6. Frontend: Navigate to /essaim
```

### L'Essaim Real-Time
```
1. Frontend: Connect WebSocket /ws/swarm
2. Backend: Accept connection (max 500)
3. Backend: Broadcast 350 agents @ 60fps
4. Frontend: Render Three.js particles
5. Loop: Update positions every 16ms
```

---

## Services Docker

| Service | Port | Description |
|---------|------|-------------|
| atom-api | 8000 | FastAPI REST API |
| atom-websocket | 8001 | WebSocket L'Essaim |
| atom-redis | 6379 | Cache + Pub/Sub |
| atom-nginx | 80/443 | SSL + Proxy |

---

## Liens

- [[16 Spheres]]
- [[350 Agents]]
- [[WebSocket Server]]
- [[Deployment Guide]]

#architecture #technical #system #infrastructure
