# CHE·NU V1 — CANONICAL STRUCTURE PROPOSAL

**Version:** 1.0 FINAL  
**Date:** 16 décembre 2025  
**Status:** PROPOSAL - Requires Approval  
**Authority:** MEMORY PROMPT + Technical Best Practices

---

## 🎯 DESIGN PRINCIPLES

### 1. Clarity Over Complexity
- Every folder has ONE clear purpose
- No deep nesting (max 3-4 levels)
- Naming is explicit and unambiguous

### 2. Separation of Concerns
- MVP code separate from POST-MVP
- Backend services logically grouped
- Frontend by feature, not by type

### 3. Scale-Ready
- Structure supports adding spheres later
- Services can be deployed independently
- Frontend can be code-split

### 4. Governance-First
- Governance logic is centralized
- Audit/compliance easy to locate
- Security policies enforceable

---

## 📦 MONOREPO ROOT STRUCTURE

```
chenu-v1/
├── README.md                          # Project overview (UPDATED)
├── ARCHITECTURE.md                    # System architecture (NEW)
├── SECURITY.md                        # Security model (NEW)
├── CONTRIBUTING.md                    # Dev guidelines (NEW)
├── LICENSE                            # Proprietary license
├── .gitignore                         # Git exclusions
├── .env.example                       # Environment template
├── package.json                       # Root workspace config
├── tsconfig.json                      # TypeScript root config
├── docker-compose.yml                 # Infrastructure
├── docker-compose.prod.yml            # Production config (NEW)
├──

 Makefile                            # Common commands (NEW)
│
├── docs/                              # 📚 DOCUMENTATION
│   ├── canonical/                     # Frozen specs (MEMORY-aligned)
│   │   ├── 00_MEMORY_PROMPT.md        # ← Authoritative source
│   │   ├── 01_IDENTITY_CONTEXT.md     # Identity & Context spec
│   │   ├── 02_SPHERES_BUREAUS.md      # 8 Spheres + 10 Bureaus
│   │   ├── 03_THREADS.md              # .chenu thread system
│   │   ├── 04_GOVERNANCE_PIPELINE.md  # 10-step pipeline
│   │   ├── 05_TOKENS_BUDGET.md        # Token system
│   │   ├── 06_AGENTS.md               # Agent architecture
│   │   ├── 07_VERSIONING.md           # Append-only versioning
│   │   ├── 08_SECURITY.md             # Zero-trust model
│   │   └── 09_UI_3HUB.md              # 3-Hub layout
│   │
│   ├── api/                           # API documentation
│   │   ├── openapi.yaml               # OpenAPI 3.0 spec
│   │   ├── endpoints/                 # Per-service endpoints
│   │   └── examples/                  # Request/response examples
│   │
│   ├── guides/                        # User & dev guides
│   │   ├── quickstart.md              # Getting started
│   │   ├── development.md             # Dev setup
│   │   ├── deployment.md              # Deploy guide
│   │   └── investor-demo.md           # 7-min demo script
│   │
│   └── adr/                           # Architecture Decision Records
│       ├── 001-8-spheres.md           # Why 8 spheres
│       ├── 002-governance-first.md    # Why governance-first
│       └── [future decisions]
│
├── backend/                           # 🔧 BACKEND SERVICES
│   ├── README.md                      # Backend overview
│   ├── shared/                        # Shared utilities
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── types/                 # TypeScript types
│   │   │   │   ├── identity.types.ts
│   │   │   │   ├── sphere.types.ts
│   │   │   │   ├── thread.types.ts
│   │   │   │   ├── agent.types.ts
│   │   │   │   ├── governance.types.ts
│   │   │   │   └── index.ts
│   │   │   ├── dtos/                  # Data Transfer Objects
│   │   │   ├── guards/                # Auth/validation guards
│   │   │   ├── utils/                 # Shared utilities
│   │   │   └── index.ts
│   │   └── dist/                      # Compiled output
│   │
│   ├── services/                      # 🎯 MVP MICROSERVICES
│   │   ├── identity-context/          # Service 1: Identity & Context
│   │   │   ├── package.json
│   │   │   ├── Dockerfile
│   │   │   ├── src/
│   │   │   │   ├── main.ts            # Service entry
│   │   │   │   ├── identity/          # Identity module
│   │   │   │   ├── context/           # Context module
│   │   │   │   ├── isolation/         # Isolation logic
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── thread/                    # Service 2: Thread Management
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── thread/            # Thread CRUD
│   │   │   │   ├── entry/             # Thread entries
│   │   │   │   ├── permissions/       # Access control
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── versioning/                # Service 3: Versioning
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── version/           # Version management
│   │   │   │   ├── diff/              # Diff calculation
│   │   │   │   ├── rollback/          # Rollback via new version
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── governance/                # Service 4: Governance Engine
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── pipeline/          # 10-step pipeline
│   │   │   │   ├── approval/          # Approval gates
│   │   │   │   ├── encoding/          # Encoding engine
│   │   │   │   ├── budget/            # Budget checks
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── orchestrator/              # Service 5: Agent Orchestrator
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── orchestrator/      # Orchestration logic
│   │   │   │   ├── agent-selector/    # Agent selection
│   │   │   │   ├── sandbox/           # Agent sandboxing
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── agent-runtime/             # Service 6: Agent Runtime
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── runtime/           # Execution environment
│   │   │   │   ├── monitoring/        # Agent monitoring
│   │   │   │   ├── result-handler/    # Result processing
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   ├── nova/                      # Service 7: Nova (Guide/Assistant)
│   │   │   ├── package.json
│   │   │   ├── src/
│   │   │   │   ├── main.ts
│   │   │   │   ├── chat/              # Chat interface
│   │   │   │   ├── guidance/          # User guidance
│   │   │   │   ├── clarification/     # Intent clarification
│   │   │   │   └── __tests__/
│   │   │   └── README.md
│   │   │
│   │   └── auth/                      # Service 8: Authentication
│   │       ├── package.json
│   │       ├── src/
│   │       │   ├── main.ts
│   │       │   ├── auth/              # Auth logic
│   │       │   ├── session/           # Session management
│   │       │   ├── rbac/              # Role-based access
│   │       │   └── __tests__/
│   │       └── README.md
│   │
│   ├── api-gateway/                   # 🚪 API GATEWAY
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── main.ts
│   │   │   ├── routes/                # Route definitions
│   │   │   ├── middleware/            # Auth, CORS, rate-limit
│   │   │   ├── proxy/                 # Service proxy logic
│   │   │   └── __tests__/
│   │   └── README.md
│   │
│   ├── database/                      # 💾 DATABASE
│   │   ├── README.md
│   │   ├── schema/                    # PostgreSQL schemas
│   │   │   ├── 00_core.sql            # Core tables (users, identities)
│   │   │   ├── 01_threads.sql         # Thread system
│   │   │   ├── 02_versions.sql        # Versioning
│   │   │   ├── 03_governance.sql      # Governance logs
│   │   │   ├── 04_agents.sql          # Agent definitions
│   │   │   ├── 05_budget.sql          # Token/budget system
│   │   │   └── 06_audit.sql           # Audit trail
│   │   │
│   │   ├── migrations/                # Database migrations
│   │   │   ├── 001_initial_schema.sql
│   │   │   ├── 002_add_encoding.sql
│   │   │   └── [future migrations]
│   │   │
│   │   ├── seeds/                     # Test/dev data
│   │   │   ├── dev_users.sql
│   │   │   ├── dev_identities.sql
│   │   │   └── demo_threads.sql
│   │   │
│   │   └── scripts/                   # DB utilities
│   │       ├── backup.sh
│   │       ├── restore.sh
│   │       └── reset-dev.sh
│   │
│   └── post-mvp/                      # 📦 POST-MVP CODE (Archived)
│       ├── README.md                  # "Not for MVP" notice
│       ├── community/                 # Community sphere code
│       ├── government/                # Government sphere code
│       ├── studio/                    # Studio sphere code
│       ├── social/                    # Social sphere code
│       ├── entertainment/             # Entertainment sphere code
│       ├── team/                      # Team sphere code
│       └── advanced-features/         # Other post-MVP features
│
├── frontend/                          # 🎨 FRONTEND APPLICATION
│   ├── README.md                      # Frontend overview
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts                 # Vite config (or Next if chosen)
│   ├── tailwind.config.js             # Tailwind CSS
│   ├── index.html
│   │
│   ├── public/                        # Static assets
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── main.tsx                   # App entry point
│   │   ├── App.tsx                    # Root component
│   │   │
│   │   ├── core/                      # 🔧 CORE SYSTEMS
│   │   │   ├── auth/                  # Authentication
│   │   │   ├── routing/               # React Router setup
│   │   │   ├── api/                   # API client
│   │   │   ├── state/                 # Global state (Zustand/Redux)
│   │   │   └── websocket/             # WebSocket client
│   │   │
│   │   ├── features/                  # 🎯 FEATURE MODULES
│   │   │   ├── identity/              # Identity management
│   │   │   │   ├── components/
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   ├── spheres/               # Sphere navigation
│   │   │   │   ├── components/
│   │   │   │   │   ├── SphereSelector.tsx
│   │   │   │   │   └── SphereCard.tsx
│   │   │   │   ├── hooks/
│   │   │   │   └── constants.ts       # 8 spheres definition
│   │   │   │
│   │   │   ├── bureau/                # Universal Bureau
│   │   │   │   ├── components/
│   │   │   │   │   ├── Bureau.tsx              # Main container
│   │   │   │   │   ├── BureauSection.tsx       # Section wrapper
│   │   │   │   │   ├── Dashboard.tsx           # Section 1
│   │   │   │   │   ├── Notes.tsx               # Section 2
│   │   │   │   │   ├── Tasks.tsx               # Section 3
│   │   │   │   │   ├── Projects.tsx            # Section 4
│   │   │   │   │   ├── Threads.tsx             # Section 5
│   │   │   │   │   ├── Meetings.tsx            # Section 6
│   │   │   │   │   ├── Database.tsx            # Section 7
│   │   │   │   │   ├── Agents.tsx              # Section 8
│   │   │   │   │   ├── Reports.tsx             # Section 9
│   │   │   │   │   └── BudgetGovernance.tsx    # Section 10
│   │   │   │   ├── hooks/
│   │   │   │   └── types.ts
│   │   │   │
│   │   │   ├── threads/               # Thread management
│   │   │   │   ├── components/
│   │   │   │   │   ├── ThreadList.tsx
│   │   │   │   │   ├── ThreadDetail.tsx
│   │   │   │   │   ├── ThreadEntry.tsx
│   │   │   │   │   └── CreateThreadModal.tsx
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   ├── governance/            # Governance UI
│   │   │   │   ├── components/
│   │   │   │   │   ├── GovernancePipeline.tsx  # Pipeline visualizer
│   │   │   │   │   ├── ApprovalModal.tsx       # Approval gate
│   │   │   │   │   ├── BudgetIndicator.tsx     # Budget display
│   │   │   │   │   └── IntentClarification.tsx # Intent capture
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   ├── nova/                  # Nova chat interface
│   │   │   │   ├── components/
│   │   │   │   │   ├── NovaChat.tsx
│   │   │   │   │   ├── NovaMessage.tsx
│   │   │   │   │   └── NovaInput.tsx
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   ├── agents/                # Agent management
│   │   │   │   ├── components/
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   ├── versioning/            # Version history UI
│   │   │   │   ├── components/
│   │   │   │   ├── hooks/
│   │   │   │   └── api/
│   │   │   │
│   │   │   └── workspace/             # Workspace (transversal)
│   │   │       ├── components/
│   │   │       ├── hooks/
│   │   │       └── api/
│   │   │
│   │   ├── layouts/                   # 🏗️ LAYOUT COMPONENTS
│   │   │   ├── ThreeHubLayout.tsx     # Main 3-Hub layout
│   │   │   ├── CenterHub.tsx          # Center: CHE·NU core
│   │   │   ├── LeftHub.tsx            # Left: Communication
│   │   │   ├── BottomHub.tsx          # Bottom: Navigation
│   │   │   └── RightHub.tsx           # Right: (future)
│   │   │
│   │   ├── components/                # 🧩 SHARED COMPONENTS
│   │   │   ├── ui/                    # Base UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── [other primitives]
│   │   │   │
│   │   │   ├── forms/                 # Form components
│   │   │   │   ├── FormField.tsx
│   │   │   │   ├── FormValidation.tsx
│   │   │   │   └── FormSubmit.tsx
│   │   │   │
│   │   │   └── feedback/              # Feedback components
│   │   │       ├── Toast.tsx
│   │   │       ├── Loading.tsx
│   │   │       └── ErrorBoundary.tsx
│   │   │
│   │   ├── hooks/                     # 🪝 SHARED HOOKS
│   │   │   ├── useAuth.ts
│   │   │   ├── useIdentity.ts
│   │   │   ├── useContext.ts
│   │   │   ├── useSphere.ts
│   │   │   ├── useThread.ts
│   │   │   └── useGovernance.ts
│   │   │
│   │   ├── utils/                     # 🛠️ UTILITIES
│   │   │   ├── formatting.ts
│   │   │   ├── validation.ts
│   │   │   ├── datetime.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── types/                     # 📘 TYPES (Frontend-specific)
│   │   │   ├── ui.types.ts
│   │   │   ├── form.types.ts
│   │   │   └── component.types.ts
│   │   │
│   │   ├── styles/                    # 🎨 GLOBAL STYLES
│   │   │   ├── index.css              # Tailwind imports
│   │   │   ├── variables.css          # CSS variables
│   │   │   └── themes/                # Theme definitions
│   │   │       ├── light.css
│   │   │       └── dark.css
│   │   │
│   │   └── assets/                    # 📦 ASSETS
│   │       ├── images/
│   │       ├── icons/
│   │       └── fonts/
│   │
│   └── post-mvp/                      # 📦 POST-MVP UI CODE
│       ├── README.md
│       ├── community-ui/
│       ├── government-ui/
│       ├── studio-ui/
│       ├── social-ui/
│       ├── entertainment-ui/
│       └── team-ui/
│
├── infrastructure/                    # 🏗️ INFRASTRUCTURE
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.nginx
│   │
│   ├── kubernetes/                    # K8s manifests (future)
│   │   ├── deployments/
│   │   ├── services/
│   │   └── ingress/
│   │
│   ├── terraform/                     # IaC (future)
│   │   ├── aws/
│   │   └── gcp/
│   │
│   └── scripts/                       # Utility scripts
│       ├── deploy.sh
│       ├── backup.sh
│       └── monitoring.sh
│
├── tests/                             # 🧪 INTEGRATION TESTS
│   ├── e2e/                           # End-to-end tests
│   │   ├── identity-context.spec.ts
│   │   ├── thread-lifecycle.spec.ts
│   │   ├── governance-pipeline.spec.ts
│   │   └── budget-enforcement.spec.ts
│   │
│   ├── integration/                   # Integration tests
│   │   ├── api/
│   │   └── database/
│   │
│   └── performance/                   # Performance tests
│       ├── load-tests/
│       └── benchmarks/
│
└── tools/                             # 🔧 DEVELOPMENT TOOLS
    ├── generators/                    # Code generators
    │   ├── service-generator.js
    │   └── component-generator.js
    │
    ├── linting/                       # Linting configs
    │   ├── .eslintrc.js
    │   ├── .prettierrc
    │   └── .stylelintrc
    │
    └── ci-cd/                         # CI/CD configs
        ├── github-actions/
        └── gitlab-ci/
```

---

## 📝 NAMING CONVENTIONS

### Services
```
Format: [domain]-[subdomain]
Examples:
- identity-context
- thread
- governance
- agent-runtime

NOT: identityService, Identity_Context, IdentityAndContext
```

### Components
```
Format: PascalCase
Examples:
- ThreeHubLayout.tsx
- SphereSelector.tsx
- ApprovalModal.tsx

NOT: three-hub-layout.tsx, threeHubLayout.tsx, sphere_selector.tsx
```

### Hooks
```
Format: useCamelCase
Examples:
- useAuth.ts
- useIdentity.ts
- useSphere.ts

NOT: UseAuth.ts, use_auth.ts, auth-hook.ts
```

### Files (non-component)
```
Format: kebab-case
Examples:
- identity.types.ts
- governance.service.ts
- api-client.ts

NOT: identityTypes.ts, Identity_Types.ts, IdentityTypes.ts
```

### Database Tables
```
Format: snake_case, plural
Examples:
- users
- identities
- threads
- thread_entries
- governance_logs

NOT: Users, user, User, identity
```

### Environment Variables
```
Format: SCREAMING_SNAKE_CASE
Examples:
- DATABASE_URL
- JWT_SECRET
- API_GATEWAY_PORT

NOT: databaseUrl, database-url, DatabaseURL
```

---

## 🗂️ WHAT BELONGS WHERE

### Backend Service Responsibilities

| Service | Owns | Does NOT Own |
|---------|------|--------------|
| **identity-context** | User identities, context switching, isolation rules | Authentication (auth service), Spheres (domain logic) |
| **thread** | Thread CRUD, entries, permissions | Thread content rendering (frontend), Versioning (versioning service) |
| **versioning** | Version storage, diff calculation, rollback logic | What to version (each service decides), UI for version history |
| **governance** | Pipeline orchestration, approval gates, encoding, budget checks | Agent execution (agent-runtime), User decisions (frontend) |
| **orchestrator** | Agent selection, task routing, result assembly | Agent code execution (agent-runtime), Budget tracking (governance) |
| **agent-runtime** | Sandboxed execution, monitoring, result handling | Which agent to run (orchestrator), Approval decisions (governance) |
| **nova** | Chat interface, guidance, clarification | Task execution (agents), Decision-making (always human) |
| **auth** | Login, sessions, tokens, RBAC | Identity management (identity-context), Business logic authorization |

### Frontend Feature Responsibilities

| Feature | Owns | Does NOT Own |
|---------|------|--------------|
| **identity** | Identity selector UI, context indicator | Authentication (core/auth), Backend identity logic |
| **spheres** | Sphere selector, navigation | Bureau content (bureau feature), Sphere-specific business logic |
| **bureau** | Universal 10-section layout, section routing | Section content (each section component), Business logic |
| **threads** | Thread UI, creation, viewing | Thread storage (backend), Versioning UI (versioning feature) |
| **governance** | Pipeline UI, approval modals, budget indicator | Pipeline logic (backend), Agent execution |
| **nova** | Chat UI, message display | Nova AI logic (backend), Tool execution |
| **agents** | Agent list, status, hiring UI | Agent execution (backend), Agent code |
| **versioning** | Version history UI, diff viewer | Version storage (backend), Rollback logic |
| **workspace** | Document editor, collaboration UI | File storage (backend), Real-time sync (future) |

---

## 🔄 MIGRATION PLAN FROM v30 TO CANONICAL

### Phase 1: Structure Setup (Week 1)

```bash
# 1. Create canonical structure
mkdir -p chenu-v1/{docs,backend,frontend,infrastructure,tests,tools}

# 2. Move existing code to canonical locations
# Backend:
mv v30/backend/services → chenu-v1/backend/services (review each)
mv v30/backend/app → chenu-v1/backend/services (consolidate)

# Frontend:
mv v30/web → chenu-v1/frontend (if Next.js chosen)
OR
mv v30/frontend → chenu-v1/frontend (if React/Vite chosen)

# Archive the other:
mv v30/[unused-frontend] → chenu-v1/frontend/post-mvp/legacy-ui

# Database:
mv v30/backend/sql → chenu-v1/backend/database/schema
mv v30/database → chenu-v1/backend/database/migrations

# 3. Archive non-MVP code
mkdir -p chenu-v1/backend/post-mvp
mv [community, government, studio, social, entertainment, team services] → post-mvp/

# 4. Create documentation
cp MEMORY_PROMPT.md → chenu-v1/docs/canonical/00_MEMORY_PROMPT.md
# Create other canonical docs based on MEMORY
```

### Phase 2: Code Refactoring (Week 2-3)

```bash
# 1. Rename services
mv backend/services/enterprise → backend/services/business
mv backend/services/creative-studio → backend/services/studio

# 2. Consolidate duplicates
# Merge backend/services/X and backend/app/X into single service

# 3. Update imports
# Run automated refactoring to update all import paths

# 4. Extract shared code
# Move common code to backend/shared/

# 5. Standardize naming
# Rename files to follow conventions
```

### Phase 3: Testing & Validation (Week 4)

```bash
# 1. Verify all imports work
npm run build

# 2. Run existing tests
npm run test

# 3. Fix broken tests
# Update test paths and logic

# 4. Add missing tests
# Especially for refactored code

# 5. Integration tests
# Test end-to-end flows
```

---

## ✅ STRUCTURE VALIDATION CHECKLIST

### Must Have (Before Development)

- [ ] Root README.md updated with canonical structure
- [ ] ARCHITECTURE.md created with system overview
- [ ] docs/canonical/ has all 10 frozen specs
- [ ] backend/services/ has exactly 8 services (MVP)
- [ ] backend/shared/ has core types
- [ ] backend/database/schema/ has all SQL files
- [ ] frontend/src/features/ matches MEMORY features
- [ ] frontend/src/layouts/ has ThreeHubLayout
- [ ] All MVP code in main folders
- [ ] All non-MVP code in post-mvp/
- [ ] docker-compose.yml updated for new structure
- [ ] .gitignore covers all generated files

### Nice to Have (Can Be Added Later)

- [ ] tools/generators/ for scaffolding
- [ ] infrastructure/kubernetes/ for cloud deployment
- [ ] tests/performance/ benchmarks
- [ ] Monorepo scripts (turborepo/nx)
- [ ] Automated code splitting
- [ ] Advanced monitoring setup

---

## 🎯 BENEFITS OF CANONICAL STRUCTURE

### For Developers

1. **Clear Navigation**: Know where everything is
2. **Reduced Confusion**: One place for each concern
3. **Easy Onboarding**: Structure is self-documenting
4. **Safe Refactoring**: Clear boundaries

### For Project Management

1. **Scope Control**: MVP vs POST-MVP visually separated
2. **Progress Tracking**: Can count completed services/features
3. **Risk Management**: Dependencies are clear
4. **Resource Allocation**: Can assign folders to teams

### For Investors/Stakeholders

1. **Understandable**: Non-technical can navigate
2. **Credible**: Professional structure signals maturity
3. **Scalable**: Can see how system grows
4. **Governable**: Audit/compliance folders visible

---

## 🚀 NEXT STEPS

1. **Get Approval** on this structure
2. **Create Migration Script** to automate v30 → canonical
3. **Update All Documentation** to reference new paths
4. **Run Migration** on a copy first (test)
5. **Validate** that everything still works
6. **Commit Canonical** as new baseline

---

**📋 [View Gaps & Risks Analysis](./CHENU_GAPS_RISKS_ANALYSIS.md)**  
**📋 [View Analysis Report](./CHENU_ANALYSE_EXISTANT_ET_PLAN.md)**

---

**🎯 THIS STRUCTURE IS READY FOR APPROVAL AND IMPLEMENTATION! 🚀**
