# 🏠 CHE·NU™ V76 — UNIFIED BACKEND

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                      CHE·NU™ — GOVERNED INTELLIGENCE OPERATING SYSTEM               ║
║                                                                                      ║
║                                    Version 76.0.0                                    ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

> **"Structure precedes intelligence. Visibility precedes power. Human accountability is non-negotiable."**

## 📊 Overview

| Metric | Value |
|--------|-------|
| **Version** | 76.0.0 UNIFIED |
| **Routers** | 18 |
| **Endpoints** | ~220+ |
| **Tests** | ~342 |
| **R&D Rules** | 7/7 ✅ |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and start
cp .env.example .env
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### Option 2: Local Development

```bash
# 1. Start PostgreSQL and Redis (or use Docker)
docker-compose up -d db redis

# 2. Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp ../.env.example .env
# Edit .env with your settings

# 5. Run migrations
alembic upgrade head

# 6. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **R&D Rules**: http://localhost:8000/rd-rules
- **Architecture**: http://localhost:8000/architecture

## 🛡️ R&D Rules (7 Non-Negotiable Rules)

| Rule | Name | Enforcement |
|------|------|-------------|
| **#1** | Human Sovereignty | HTTP 423 LOCKED on sensitive operations |
| **#2** | Autonomy Isolation | Sandbox mode for AI operations |
| **#3** | Identity Boundary | HTTP 403 on cross-identity access |
| **#4** | No AI-to-AI | HTTP 403 on /call-agent endpoints |
| **#5** | No Ranking | ORDER BY created_at DESC only |
| **#6** | Full Traceability | id, created_by, created_at on all entities |
| **#7** | Architecture Frozen | 9 spheres, 6 bureau sections |

## 📁 Project Structure

```
CHENU_V76_UNIFIED/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── core/
│   │   │   ├── config.py        # Settings & configuration
│   │   │   ├── database.py      # PostgreSQL connection
│   │   │   └── cache.py         # Redis cache manager
│   │   ├── models/
│   │   │   └── models.py        # SQLAlchemy models
│   │   ├── routers/             # 18 API routers
│   │   │   ├── threads.py
│   │   │   ├── checkpoints.py   # HTTP 423 governance
│   │   │   ├── nova.py          # Intelligence pipeline
│   │   │   ├── memory.py        # Tri-layer memory
│   │   │   └── ...
│   │   └── schemas/             # Pydantic schemas
│   ├── tests/                   # ~342 tests
│   ├── alembic/                 # Database migrations
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   └── cypress/                 # E2E tests
├── docker/
│   ├── Dockerfile.backend
│   └── init-db.sql
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔌 API Routers (18)

### Core Routers

| Router | Endpoints | Description |
|--------|-----------|-------------|
| `threads` | ~20 | Thread lifecycle & decisions |
| `checkpoints` | 15 | HTTP 423 governance (Rule #1) |
| `nova` | 15 | Multi-lane intelligence pipeline |
| `memory` | 14 | Tri-layer memory system |
| `agents` | 10 | Agent registry (Rule #4) |
| `decisions` | 12 | Decision tracking |

### Entity Routers

| Router | Endpoints | Description |
|--------|-----------|-------------|
| `identities` | 12 | Identity management (9 spheres) |
| `spheres` | 11 | 9 spheres (Rule #7) |
| `workspaces` | 10 | 6 bureau sections |
| `dataspaces` | 11 | Encrypted data containers |
| `dataspace_engine` | 18 | DataSpace operations |
| `meetings` | 11 | Meeting management |
| `notifications` | 10 | Notification system |
| `files` | 13 | File management |
| `xr` | 15 | XR environment generation |

### Engine Routers

| Router | Endpoints | Description |
|--------|-----------|-------------|
| `layout_engine` | 15 | Layout management |
| `oneclick_engine` | 15 | OneClick operations |
| `ocw` | 15 | OCW management |

## 🗄️ Database Schema

### Core Tables

- **identities** - User accounts
- **spheres** - 9 life spheres (frozen)
- **workspaces** - 6 bureau sections per sphere
- **threads** - Core decision units
- **thread_events** - Immutable event log
- **decisions** - Decision records
- **checkpoints** - HTTP 423 governance
- **dataspaces** - Encrypted containers
- **agents** - AI agent registry
- **memory_snapshots** - Tri-layer memory
- **meetings** - Meeting records
- **notifications** - User notifications

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit -v
pytest tests/security -v
pytest tests/performance -v

# Run E2E tests (Cypress)
cd ../frontend
npx cypress run
```

## 🔧 Development

### Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Docker Commands

```bash
# Start all services
docker-compose up -d

# Start with dev tools (pgAdmin, Redis Commander)
docker-compose --profile dev up -d

# View logs
docker-compose logs -f api

# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Environment Variables

Key environment variables (see `.env.example` for full list):

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=chenu
POSTGRES_PASSWORD=chenu_secret
POSTGRES_DB=chenu_v76

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY=your-secret-key

# AI (optional)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

## 📈 Performance

### Benchmarks

| Operation | Target | Actual |
|-----------|--------|--------|
| Health check | <50ms | ~10ms |
| Thread create | <200ms | ~50ms |
| Thread list | <100ms | ~30ms |
| Checkpoint create | <200ms | ~80ms |

### Caching Strategy

- **Hot Memory**: Redis, 5 min TTL (active context)
- **Warm Memory**: Redis + PostgreSQL, 1 hour TTL
- **Cold Memory**: PostgreSQL only (archived)

## 🔒 Security

- JWT authentication
- Identity boundary enforcement (Rule #3)
- HTTP 423 for sensitive operations (Rule #1)
- HTTP 403 for AI-to-AI blocking (Rule #4)
- Full audit trail (Rule #6)
- No ranking algorithms (Rule #5)

## 📚 Documentation

- `/docs` - Swagger UI
- `/redoc` - ReDoc
- `/rd-rules` - R&D Rules reference
- `/architecture` - Architecture overview
- `/stats` - API statistics

## 🤝 Contributing

1. Read the R&D Rules (mandatory)
2. Follow the coding standards
3. Add tests for new features
4. Update documentation
5. Submit PR with description

## 📄 License

Proprietary - CHE·NU™ © 2026

---

```
═══════════════════════════════════════════════════════════════════════════════

              "GOUVERNANCE > EXÉCUTION • HUMANS > AUTOMATION"

                     CHE·NU™ V76 — Built for Decades

═══════════════════════════════════════════════════════════════════════════════
```
