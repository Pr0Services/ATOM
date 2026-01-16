# CHE·NU™ v31 — COMPLETE BACKEND API

**Governed Intelligence Operating System**  
Complete implementation with all engines, 57 tables, 226 agents

---

## 📦 WHAT'S INCLUDED

### DATABASE (57 tables)
- ✅ Core Identity (users, identities, permissions)
- ✅ Spheres & Domains (8 spheres)
- ✅ Dataspaces (3 tables)
- ✅ Threads (3 tables)
- ✅ Workspaces (4 tables)
- ✅ OneClick (3 tables)
- ✅ Backstage Intelligence (3 tables)
- ✅ Memory Governance (1 table)
- ✅ Governance & Audit (3 tables)
- ✅ Agents System (4 tables)
- ✅ Meetings (4 tables)
- ✅ Properties/Immobilier (5 tables)
- ✅ Construction (4 tables)
- ✅ OCW - Online Collaborative Whiteboard (4 tables)
- ✅ XR Rooms (4 tables)
- ✅ Files (2 tables)
- ✅ Notifications, Metrics, Config (3 tables)

### API ROUTES (62 endpoints)
```
/api/auth/*           - Authentication (3)
/api/identities/*     - Identity management (2)
/api/spheres/*        - Sphere navigation (1)
/api/dataspaces/*     - DataSpace containers (3)
/api/threads/*        - Thread artifacts (2)
/api/agents/*         - Agent orchestration (1)
/api/governance/*     - Governed execution (3)
/api/meetings/*       - Meeting system (6)
/api/workspaces/*     - Workspace engine (6)
/api/oneclick/*       - 1-Click assistant (3)
/api/properties/*     - Real estate (6)
/api/construction/*   - Construction projects (6)
/api/ocw/*            - Collaborative whiteboard (6)
/api/xr/*             - XR/VR rooms (5)
/api/backstage/*      - Backstage intelligence (3)
/api/memory/*         - Memory governance (2)
/api/files/*          - File management (2)
/api/notifications/*  - Notifications (2)
```

### AGENTS (226 total)
```
L0: Nova (System Guide)           - 1 agent
L1: Sphere Orchestrators          - 8 agents
L2: Domain Specialists            - 50 agents
L3: Task Executors                - 167 agents
```

### MIDDLEWARE
- ✅ **Governed Execution Pipeline** (10 steps, 626 lines)
- ✅ **Tree Laws Enforcement** (8 laws, 295 lines)
- ✅ JWT Authentication
- ✅ Request validation
- ✅ Error handling

### CORE FEATURES
- ✅ **Semantic Encoding Layer** — Transform intent to structured format
- ✅ **Governed Execution Pipeline** — 10-step validation before execution
- ✅ **Thread Artifacts (.chenu)** — Persistent audit trail
- ✅ **Agent Compatibility Matrix** — Smart agent selection
- ✅ **Tree Laws** — 8 governance rules
- ✅ **Token Budget System** — Cost control & transparency
- ✅ **Multi-Hub Architecture** — Communication/Navigation/Execution

---

## 🚀 QUICK START

### 1. Database Setup
```bash
# Create database
createdb chenu

# Run schema
psql chenu < ../database/CHENU_SQL_SCHEMA_v29.sql
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Start Server
```bash
# Development
npm run dev

# Production
npm start
```

Server runs on `http://localhost:3000`

---

## 📚 API DOCUMENTATION

### Authentication

**Register**
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Returns JWT token for authentication.

### Using the API

All protected routes require:
```http
Authorization: Bearer <jwt_token>
X-Identity-ID: <identity_uuid>
```

### Example: Create Thread with Governed Execution

```http
POST /api/threads
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Market Analysis",
  "thread_type": "analysis",
  "dataspace_id": "uuid",
  "budget_tokens": 10000
}
```

---

## 🏗️ PROJECT STRUCTURE

```
api/
├── server.js                    # Main server (896 lines)
├── package.json                 # Dependencies
├── .env.example                 # Environment template
├── routes/                      # API routes (832 lines)
│   ├── meetings.js
│   ├── workspaces.js
│   ├── oneclick.js
│   ├── properties.js
│   ├── construction.js
│   ├── ocw.js
│   ├── xr.js
│   ├── backstage.js
│   ├── memory.js
│   ├── files.js
│   └── notifications.js
├── middleware/                  # Middleware (921 lines)
│   ├── governed_execution.js    # 10-step pipeline
│   └── tree_laws.js             # 8 governance laws
├── agents/                      # Agent definitions
│   └── AGENTS_226_COMPLETE.md   # All 226 agents (765 lines)
└── config/                      # Configuration
    ├── database.js
    └── jwt.js
```

---

## 🔐 SECURITY

- ✅ JWT-based authentication
- ✅ bcrypt password hashing (12 rounds)
- ✅ Helmet.js security headers
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention (parameterized queries)
- ✅ Governance audit logging

---

## 🎯 8 SPHERES (Modified Structure)

1. **Personal** 🏠 — Private life, health, goals
2. **Business** 💼 — Multi-enterprise, multi-identity
3. **Government & Institutions** 🏛️ — Admin, compliance
4. **Studio de création** 🎨 — Creative expression
5. **Community** 👥 — Local relations
6. **Social & Media** 📱 — Online presence
7. **Entertainment** 🎬 — Leisure activities
8. **My Team** 🤝 — Team management + IA Labs + Skills & Tools

---

## 🧠 GOVERNED EXECUTION PIPELINE

All AI executions pass through 10 mandatory steps:

1. **Intent Capture** — Capture raw human intent
2. **Semantic Encoding** — Transform to structured format
3. **Encoding Validation** — Verify quality thresholds
4. **Token & Cost Estimation** — Predict computational cost
5. **Scope Locking** — Define immutable boundaries
6. **Budget Verification** — Check token availability
7. **Agent Compatibility Check** — Match compatible agents
8. **Controlled Execution** — Execute with monitoring
9. **Result Capture** — Validate outputs
10. **Thread Update** — Create audit trail

---

## 📊 STATISTICS

```
Database Schema:     1,379 lines SQL
API Server:            896 lines JS
Routes:                832 lines JS
Middleware:            921 lines JS
Agents:                765 lines MD
Config:                 45 lines JS
───────────────────────────────
TOTAL BACKEND:       4,838 lines
```

**Coverage:**
- ✅ 57/57 tables (100%)
- ✅ 62 API endpoints
- ✅ 226 agents documented
- ✅ 10-step pipeline implemented
- ✅ 8 Tree Laws enforced

---

## 🔬 TESTING

```bash
# Run tests (when available)
npm test

# Health check
curl http://localhost:3000/health
```

---

## 📝 LICENSE

Proprietary — All rights reserved  
CHE·NU™ © 2025 Pro Service

---

## 🤝 SUPPORT

For issues or questions, contact the development team.

---

**Built with ❤️ for governed intelligence.**
