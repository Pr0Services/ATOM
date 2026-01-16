# ðŸ¤– CHENU v8.0 - CONTEXT POUR LE PROCHAIN AGENT

> **IMPORTANT**: Ce document contient tout le contexte nÃ©cessaire pour continuer le dÃ©veloppement de CHENU sans avoir Ã  relire l'historique complet.

---

## ðŸ“‹ RÃ‰SUMÃ‰ EXÃ‰CUTIF

**CHENU** est une plateforme de gestion de construction avec agents IA hiÃ©rarchiques. Le projet est actuellement Ã  la version 8.0 "Natural Edition" avec un frontend React complet et un backend FastAPI fonctionnel.

### Ã‰tat Actuel
- âœ… Backend: 59 fichiers Python, architecture complÃ¨te
- âœ… Frontend: 14 fichiers React/TypeScript
- âœ… Design: ThÃ¨me "Natural" Ã©lÃ©gant (tons verts/dorÃ©s)
- âœ… IntÃ©grations: 60+ clients API (Shopify, QuickBooks, etc.)
- âœ… OAuth: 12 providers supportÃ©s
- âœ… WebSocket: Notifications temps rÃ©el
- â³ Non fait: Base de donnÃ©es, Auth utilisateur, DÃ©ploiement

---

## ðŸ—ï¸ ARCHITECTURE

### Structure des Fichiers
```
chenu_unified/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”œâ”€â”€ main.py                    # FastAPI app principale
â”‚   â”‚   â”œâ”€â”€ integration_endpoints.py   # Endpoints donnÃ©es
â”‚   â”‚   â”œâ”€â”€ oauth_endpoints.py         # OAuth endpoints
â”‚   â”‚   â””â”€â”€ websocket_notifications.py # WebSocket
â”‚   â”‚
â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â”œâ”€â”€ master_mind.py             # Orchestrateur central (L0)
â”‚   â”‚   â”œâ”€â”€ task_decomposer.py         # DÃ©composition de tÃ¢ches
â”‚   â”‚   â”œâ”€â”€ result_assembler.py        # Assemblage des rÃ©sultats
â”‚   â”‚   â”œâ”€â”€ routing_engine.py          # Routage intelligent
â”‚   â”‚   â”œâ”€â”€ execution_planner.py       # Planning d'exÃ©cution
â”‚   â”‚   â””â”€â”€ llm_router.py              # Multi-LLM support
â”‚   â”‚
â”‚   â”œâ”€â”€ agents/
â”‚   â”‚   â”œâ”€â”€ registry.py                # Registre des agents
â”‚   â”‚   â”œâ”€â”€ base_agent.py              # Classe de base
â”‚   â”‚   â”œâ”€â”€ nova.py                    # Agent frontend (Nova)
â”‚   â”‚   â”œâ”€â”€ directors.py               # Directeurs (L1)
â”‚   â”‚   â””â”€â”€ specialists.py             # SpÃ©cialistes (L2)
â”‚   â”‚
â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â”œâ”€â”€ integrations/              # 60+ clients API
â”‚   â”‚   â”‚   â”œâ”€â”€ ecommerce/             # Shopify, WooCommerce...
â”‚   â”‚   â”‚   â”œâ”€â”€ accounting/            # QuickBooks, Xero...
â”‚   â”‚   â”‚   â”œâ”€â”€ crm/                   # HubSpot, Salesforce...
â”‚   â”‚   â”‚   â””â”€â”€ ...
â”‚   â”‚   â””â”€â”€ oauth/
â”‚   â”‚       â””â”€â”€ oauth_manager.py       # Gestion OAuth
â”‚   â”‚
â”‚   â””â”€â”€ schemas/
â”‚       â”œâ”€â”€ task_schema.py             # Schemas de tÃ¢ches
â”‚       â””â”€â”€ message_schema.py          # Schemas de messages
â”‚
â””â”€â”€ frontend/
    â””â”€â”€ src/
        â”œâ”€â”€ components/
        â”‚   â”œâ”€â”€ dashboard/
        â”‚   â”‚   â”œâ”€â”€ NaturalDashboard.tsx  # Dashboard principal
        â”‚   â”‚   â””â”€â”€ LiveDataDashboard.tsx
        â”‚   â”œâ”€â”€ charts/
        â”‚   â”‚   â””â”€â”€ Charts.tsx            # 7 composants de graphiques
        â”‚   â”œâ”€â”€ chat/
        â”‚   â”‚   â””â”€â”€ NovaChat.tsx          # Interface chat
        â”‚   â”œâ”€â”€ data/
        â”‚   â”‚   â””â”€â”€ DataManager.tsx       # CRUD manager
        â”‚   â”œâ”€â”€ notifications/
        â”‚   â”‚   â””â”€â”€ NotificationSystem.tsx
        â”‚   â””â”€â”€ integrations/
        â”‚       â””â”€â”€ IntegrationHub.tsx
        â”‚
        â”œâ”€â”€ hooks/
        â”‚   â”œâ”€â”€ useIntegrations.ts        # Hook donnÃ©es
        â”‚   â””â”€â”€ useOAuth.ts               # Hook OAuth
        â”‚
        â””â”€â”€ styles/
            â”œâ”€â”€ globals.css               # Styles globaux
            â””â”€â”€ natural-theme.css         # ThÃ¨me naturel
```

### HiÃ©rarchie des Agents IA
```
Level 0 (L0): MasterMind
    â”‚
Level 1 (L1): Directeurs
    â”œâ”€â”€ DirecteurConstruction
    â”œâ”€â”€ DirecteurFinances
    â”œâ”€â”€ DirecteurMarketing
    â””â”€â”€ DirecteurRH
    â”‚
Level 2 (L2): SpÃ©cialistes
    â”œâ”€â”€ Pierre BÃ¢tisseur (Construction)
    â”œâ”€â”€ Marie Architecte
    â”œâ”€â”€ Victoria Comptable
    â”œâ”€â”€ Alexandre TrÃ©sorier
    â”œâ”€â”€ Sophie Marketing
    â””â”€â”€ ... (94 agents au total)
```

---

## ðŸŽ¨ DESIGN SYSTEM

### Palette Natural Theme
```css
/* Backgrounds */
--bg-primary: #1a1d1a;     /* Dark forest */
--bg-secondary: #232823;    /* Deep green-gray */
--bg-card: #252a25;         /* Card background */
--bg-hover: #2d332d;        /* Hover state */

/* Accents */
--accent-sage: #9caf88;     /* Sage green - PRIMARY */
--accent-gold: #c9a962;     /* Warm gold - SECONDARY */
--accent-copper: #b87a56;   /* Copper/terracotta */
--accent-teal: #7da8b8;     /* Sage blue */

/* Text */
--text-primary: #e8e4df;    /* Warm white */
--text-secondary: #b5ada3;  /* Soft beige */
--text-muted: #8a8378;      /* Muted brown */

/* Status */
--status-success: #7db87d;
--status-warning: #d4a84b;
--status-error: #c47d6d;
--status-info: #7da8b8;
```

### Composants Charts Disponibles
1. `Sparkline` - Mini graphique inline
2. `AreaChart` - Graphique en aires avec dÃ©gradÃ©
3. `BarChart` - Barres (horizontal/vertical)
4. `DonutChart` - Anneau avec lÃ©gende
5. `StatCardWithChart` - Card avec sparkline
6. `MultiLineChart` - Lignes multiples
7. `GaugeChart` - Jauge semi-circulaire

---

## ðŸ”Œ INTÃ‰GRATIONS

### Providers OAuth ConfigurÃ©s
| Provider | Status | Scopes |
|----------|--------|--------|
| Shopify | âœ… Ready | orders, products, customers |
| QuickBooks | âœ… Ready | accounting |
| HubSpot | âœ… Ready | crm, contacts |
| Stripe | âœ… Ready | read_write |
| Slack | âœ… Ready | chat, channels |
| Salesforce | âœ… Ready | api |
| Xero | âœ… Ready | accounting |
| Google | âœ… Ready | email, profile |
| Microsoft | âœ… Ready | User.Read |
| Asana | âœ… Ready | default |
| Zendesk | âœ… Ready | read, write |
| Mailchimp | âœ… Ready | - |

### Endpoints API Existants
```
GET  /                              # Health check
GET  /health                        # Detailed health
GET  /api/v1/info                   # System info

# Integrations
GET  /api/integrations/status       # All integrations status
GET  /api/integrations/dashboard    # Unified dashboard data
GET  /api/integrations/data/{prov}  # Provider data
POST /api/integrations/sync         # Trigger sync

# OAuth
GET  /oauth/providers               # List providers
GET  /oauth/status/{provider}       # Check connection
GET  /oauth/connected               # Connected providers
POST /oauth/initiate                # Start OAuth flow
GET  /oauth/callback/{provider}     # OAuth callback
DELETE /oauth/disconnect/{provider} # Disconnect

# Chat
POST /api/v1/chat                   # Send message to Nova

# Tasks
POST /api/v1/tasks                  # Create task
GET  /api/v1/tasks/active          # Active tasks

# Agents
GET  /api/v1/agents                 # List agents
GET  /api/v1/agents/{id}           # Agent details

# WebSocket
WS   /ws/notifications             # Real-time notifications
```

---

## ðŸš€ PROCHAINES Ã‰TAPES PRIORITAIRES

### 1. Base de DonnÃ©es PostgreSQL
**Fichiers Ã  crÃ©er:**
- `backend/db/database.py` - Connection & session
- `backend/db/models.py` - SQLAlchemy models
- `backend/db/migrations/` - Alembic migrations

**Tables nÃ©cessaires:**
```sql
users (id, email, password_hash, name, role, org_id)
organizations (id, name, settings)
projects (id, name, status, budget, org_id)
tasks (id, title, status, priority, project_id, assignee_id)
invoices (id, number, amount, status, client_id)
integrations (id, provider, user_id, config, status)
oauth_tokens (id, provider, user_id, access_token_enc, refresh_token_enc, expires_at)
notifications (id, user_id, type, title, message, read, created_at)
```

### 2. Authentification JWT
**Fichiers Ã  crÃ©er:**
- `backend/auth/jwt.py` - JWT utils
- `backend/auth/dependencies.py` - FastAPI dependencies
- `backend/api/auth_endpoints.py` - Login/Register

**Endpoints:**
```
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET  /auth/me
```

### 3. Docker Setup
**Fichiers Ã  crÃ©er:**
- `Dockerfile` (backend)
- `frontend/Dockerfile`
- `docker-compose.yml`
- `nginx.conf`

---

## ðŸ’¡ CONSEILS TECHNIQUES

### Pour DÃ©marrer
```bash
# Backend
cd chenu_unified
pip install -r requirements.txt
uvicorn backend.api.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Patterns UtilisÃ©s
1. **Repository Pattern** pour les accÃ¨s DB
2. **Service Layer** pour la logique mÃ©tier
3. **Dependency Injection** avec FastAPI
4. **Factory Pattern** pour crÃ©er les agents
5. **Observer Pattern** pour les notifications

### Conventions de Code
- Backend: Python avec type hints, docstrings
- Frontend: TypeScript strict, hooks personnalisÃ©s
- Naming: snake_case (Python), camelCase (TS)
- Components: Un fichier = un composant exportÃ© par dÃ©faut

---

## ðŸŽ¯ CE QUE TU DOIS FAIRE

En fonction de ce que l'utilisateur demande, voici les prioritÃ©s:

### Si "continuer le dÃ©veloppement":
1. ImplÃ©menter PostgreSQL + SQLAlchemy
2. Ajouter JWT Authentication
3. CrÃ©er les endpoints CRUD complets
4. Dockeriser l'application

### Si "amÃ©liorer le frontend":
1. Connecter vraiment aux APIs (retirer les mocks)
2. Ajouter plus de pages (Projets, Factures, etc.)
3. ImplÃ©menter le state management (Zustand)
4. Ajouter des animations (Framer Motion)

### Si "activer les agents IA":
1. Configurer les clÃ©s API LLM
2. ImplÃ©menter les workflows MasterMind
3. Connecter Nova au vrai LLM
4. Activer les agents spÃ©cialisÃ©s

### Si "dÃ©ployer":
1. CrÃ©er les Dockerfiles
2. Setup docker-compose
3. Configurer CI/CD GitHub Actions
4. DÃ©ployer sur cloud (Railway/Render simple)

---

## ðŸ“ FICHIERS IMPORTANTS Ã€ LIRE

Si tu as besoin de comprendre le code:

1. **Architecture globale**: `backend/api/main.py`
2. **Agents**: `backend/agents/registry.py`, `backend/core/master_mind.py`
3. **IntÃ©grations**: `backend/api/integration_endpoints.py`
4. **Frontend principal**: `frontend/src/components/dashboard/NaturalDashboard.tsx`
5. **Hooks data**: `frontend/src/hooks/useIntegrations.ts`

---

## âš ï¸ POINTS D'ATTENTION

1. **Pas de DB**: Actuellement tout est en mÃ©moire (mock data)
2. **Pas d'auth**: Pas de login/password implÃ©mentÃ©
3. **Agents inactifs**: Les agents IA sont dÃ©finis mais pas connectÃ©s aux LLM
4. **OAuth simulÃ©**: Le flow OAuth est mockup, pas de vraies connexions API

---

## ðŸ”‘ VARIABLES D'ENVIRONNEMENT REQUISES

```env
# API Keys (Ã  ajouter pour activer les agents)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Database (Ã  ajouter pour PostgreSQL)
DATABASE_URL=postgresql://user:pass@localhost:5432/chenu

# Redis (Ã  ajouter pour cache)
REDIS_URL=redis://localhost:6379

# JWT (Ã  ajouter pour auth)
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256

# OAuth (par provider)
SHOPIFY_CLIENT_ID=...
SHOPIFY_CLIENT_SECRET=...
HUBSPOT_CLIENT_ID=...
# etc...
```

---

## ðŸ“ž CONTACT & RESSOURCES

- **Code Source**: Dans les fichiers du projet
- **Preview HTML**: `/mnt/user-data/outputs/CHENU_Dashboard_Preview.html`
- **Roadmap**: `/mnt/user-data/outputs/CHENU_ROADMAP.md`
- **Package**: `/mnt/user-data/outputs/chenu_unified_v8_natural.zip`

---

*Ce document doit permettre Ã  n'importe quel agent de continuer le travail immÃ©diatement.*

**Version**: 8.0 Natural
**Date**: DÃ©cembre 2024
**Fichiers**: 87 total, 1.8 MB
