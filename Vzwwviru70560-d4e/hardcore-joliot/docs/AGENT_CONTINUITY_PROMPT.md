# CHE·NU™ — AGENT CONTINUITY PROMPT
## Complete Handoff Document for Next Development Session

> **Version:** 2024-12-17  
> **Status:** ACTIVE DEVELOPMENT  
> **Purpose:** Enable seamless continuation of CHE·NU development

---

# ⚠️ READ THIS ENTIRE DOCUMENT BEFORE ANY ACTION ⚠️

This document contains everything you need to continue developing CHE·NU™.
Failure to follow these rules will result in architectural violations.

---

# PART 1: CANONICAL MEMORY (NON-NEGOTIABLE)

## 1.1 CORE IDENTITY

**CHE·NU™ is a GOVERNED INTELLIGENCE OPERATING SYSTEM.**

It is:
- ❌ NOT a chatbot
- ❌ NOT a productivity app
- ❌ NOT a crypto platform
- ❌ NOT a social network

CHE·NU governs:
- ✅ Intelligence
- ✅ Intent
- ✅ Data
- ✅ AI agents
- ✅ Cost (tokens)
- ✅ Collaboration
- ✅ Ethics

**CHE·NU prioritizes CLARITY over FEATURES.**

---

## 1.2 THE 8 SPHERES (FROZEN - DO NOT MODIFY)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHE·NU 8 SPHERES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Personal 🏠              5. Community 👥                    │
│  2. Business 💼              6. Social & Media 📱               │
│  3. Government 🏛️            7. Entertainment 🎬                │
│  4. Studio de création 🎨    8. My Team 🤝                      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ⚠️ NO additional spheres allowed                               │
│  ⚠️ NO sphere may be split or merged                            │
│  ⚠️ IA Labs and Skills & Tools are INSIDE "My Team"             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1.3 THE 10 BUREAU SECTIONS (FROZEN - DO NOT MODIFY)

Each SPHERE opens a BUREAU containing EXACTLY these 10 sections:

| # | Section | Description |
|---|---------|-------------|
| 1 | **Dashboard** | Overview, KPIs, quick actions |
| 2 | **Notes** | Rich text notes, organization |
| 3 | **Tasks** | Task management, assignments |
| 4 | **Projects** | Project tracking, milestones |
| 5 | **Threads (.chenu)** | Persistent lines of thought |
| 6 | **Meetings** | Scheduling, notes, follow-ups |
| 7 | **Data / Database** | DataSpaces, structured data |
| 8 | **Agents** | Agent management, hiring |
| 9 | **Reports / History** | Analytics, audit trails |
| 10 | **Budget & Governance** | Token budgets, rules |

**This structure NEVER changes. Only content, permissions, and agents vary.**

---

## 1.4 AGENT HIERARCHY (CRITICAL)

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT HIERARCHY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NOVA (System Intelligence)                                     │
│  ├── Type: SYSTEM                                               │
│  ├── Hireable: ❌ NEVER                                         │
│  ├── Always present: ✅ YES                                     │
│  ├── Role: Guidance, memory, governance, supervision            │
│  └── Cannot be replaced or customized                           │
│                                                                 │
│  ORCHESTRATOR (User's Main Agent)                               │
│  ├── Type: HIRED                                                │
│  ├── Hireable: ✅ YES (by user)                                 │
│  ├── Role: Execute tasks, manage other agents                   │
│  ├── Respects: Scope, budget, governance                        │
│  └── Can be replaced or customized                              │
│                                                                 │
│  SPECIALIST AGENTS                                              │
│  ├── Type: HIRED                                                │
│  ├── Have: Costs, scopes, encoding compatibility                │
│  └── Act: Only when authorized                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1.5 TOKEN SYSTEM (CRITICAL - DO NOT MISREPRESENT)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHE·NU TOKENS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tokens ARE:                     Tokens are NOT:                │
│  ✅ Internal utility credits     ❌ Cryptocurrency              │
│  ✅ Intelligence energy          ❌ Speculative                 │
│  ✅ Budgeted                      ❌ Market-based               │
│  ✅ Traceable                     ❌ Tradeable on exchanges     │
│  ✅ Governed                                                    │
│  ✅ Transferable (with rules)                                   │
│                                                                 │
│  Used for:                                                      │
│  • Fund threads                                                 │
│  • Fund agents                                                  │
│  • Fund meetings                                                │
│  • Govern AI execution                                          │
│  • Make cost visible and controllable                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1.6 ABSOLUTE CONSTRAINTS (DO NOT VIOLATE)

```yaml
DO NOT:
  - Add new spheres
  - Rename spheres
  - Merge bureau sections
  - Bypass governance
  - Treat CHE·NU as a generic AI app
  - Convert tokens into speculative crypto
  - Make Nova a hired agent
  - Skip governance before execution

IF UNSURE, ALWAYS FAVOR:
  - Clarity over features
  - Separation over fusion
  - Governance over automation
```

---

# PART 2: CURRENT PROJECT STATE

## 2.1 DOCUMENTATION STATUS ✅

The canonical documentation structure is **100% COMPLETE**:

```
CHENU_MEGA_FINAL/
├── README.md                          ✅
├── CANONICAL_MEMORY.md                ✅
├── GOVERNANCE_POLICY.md               ✅
├── MVP_SCOPE_FREEZE.md                ✅
├── SYSTEM_OVERVIEW.md                 ✅
├── CHANGELOG.md                       ✅
│
├── architecture/
│   ├── ARCHITECTURE_OVERVIEW.md       ✅
│   ├── MICROSERVICES_MAP.md           ✅
│   ├── API_CONTRACT_OPENAPI.yaml      ✅
│   ├── DATA_MODEL.md                  ✅
│   └── SECURITY_PRIVACY.md            ✅
│
├── product/
│   ├── UI_STRUCTURE.md                ✅
│   ├── SPHERE_PLACE_MAPPING.md        ✅
│   ├── WORKSPACE_SPEC.md              ✅
│   ├── ONBOARDING_PROGRESSIVE.md      ✅
│   └── DESIGN_TOKENS.json             ✅
│
├── agents/
│   ├── AGENT_GOVERNANCE.md            ✅
│   ├── ORCHESTRATOR_SPEC.md           ✅
│   ├── AGENT_PERMISSIONS.md           ✅
│   └── COST_BUDGETING.md              ✅
│
├── xr/
│   ├── XR_PRINCIPLES.md               ✅
│   ├── XR_UI_MAPPING.md               ✅
│   └── AVATAR_SYSTEM.md               ✅
│
├── validation/
│   ├── COMPLIANCE_CHECKLIST.yaml      ✅
│   ├── RELEASE_CHECKLIST.md           ✅
│   └── AUDIT_TEMPLATE.md              ✅
│
├── frontend/                          ✅ ~25,000 lines
├── backend/                           ✅ ~20,000 lines
├── mobile/                            ✅ Basic structure
└── database/                          ✅ SQL Schema v29
```

---

## 2.2 CODEBASE STATUS

### Frontend (React/TypeScript)
- **Location:** `/frontend/`
- **Status:** Functional MVP
- **Key files:**
  - `src/components/` - All UI components
  - `src/stores/` - Zustand state management
  - `src/services/` - API clients
  - `src/pages/` - Route pages
  - `src/config/spheres.config.ts` - Sphere definitions

### Backend (Python/FastAPI + Node.js Services)
- **Location:** `/backend/`
- **Status:** Functional MVP
- **Key files:**
  - `app/main.py` - FastAPI main app
  - `services/` - Microservices (26 services)
  - `app/api/endpoints/` - API routes

### Database
- **Location:** `/database/CHENU_SQL_SCHEMA_v29.sql`
- **Status:** Complete schema
- **Tables:** 50+ tables covering all domains

---

## 2.3 STATISTICS

| Metric | Value |
|--------|-------|
| Total Documentation Files | 100+ |
| Total Lines of Code | ~77,000+ |
| Frontend Components | 80+ |
| Backend Services | 26 |
| API Endpoints | 150+ |
| Database Tables | 50+ |

---

# PART 3: TECHNICAL SPECIFICATIONS

## 3.1 TECH STACK

```yaml
Frontend:
  framework: React 18
  language: TypeScript
  state: Zustand
  styling: TailwindCSS
  routing: React Router v6
  testing: Vitest, Playwright

Backend:
  primary: Python 3.11 + FastAPI
  services: Node.js + Express
  auth: JWT + OAuth2
  validation: Pydantic

Database:
  primary: PostgreSQL 15
  cache: Redis
  search: PostgreSQL FTS (future: Elasticsearch)

Infrastructure:
  containers: Docker
  orchestration: Docker Compose (dev), Kubernetes (prod)
  monitoring: Prometheus + Grafana
  ci_cd: GitHub Actions

XR:
  3d: Three.js + React Three Fiber
  vr: WebXR API
```

---

## 3.2 COLOR PALETTE (BRAND)

```json
{
  "sacred_gold": "#D8B26A",
  "ancient_stone": "#8D8371",
  "jungle_emerald": "#3F7249",
  "cenote_turquoise": "#3EB4A2",
  "shadow_moss": "#2F4C39",
  "earth_ember": "#7A593A",
  "ui_slate": "#1E1F22",
  "soft_sand": "#E9E4D6"
}
```

---

## 3.3 API STRUCTURE

```
/api/v1/
├── /auth/
│   ├── POST /login
│   ├── POST /register
│   └── POST /refresh
│
├── /spheres/
│   ├── GET /
│   └── GET /{sphere_id}
│
├── /bureaus/
│   ├── GET /{sphere_id}/sections
│   └── GET /{sphere_id}/{section}
│
├── /threads/
│   ├── GET /
│   ├── POST /
│   ├── GET /{thread_id}
│   └── PUT /{thread_id}
│
├── /agents/
│   ├── GET /
│   ├── POST /hire
│   └── DELETE /{agent_id}
│
├── /nova/
│   ├── POST /chat
│   └── GET /suggestions
│
├── /tokens/
│   ├── GET /balance
│   ├── POST /allocate
│   └── GET /history
│
└── /governance/
    ├── POST /validate
    └── GET /rules
```

---

## 3.4 KEY PATTERNS

### State Management (Zustand)
```typescript
// Example store pattern
export const useSphereStore = create<SphereState>((set) => ({
  currentSphere: null,
  spheres: SPHERES_CONFIG,
  setCurrentSphere: (sphere) => set({ currentSphere: sphere }),
}));
```

### API Calls
```typescript
// Example API pattern
const apiClient = {
  get: async <T>(url: string): Promise<T> => {
    const response = await fetch(`${API_BASE}${url}`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    return response.json();
  },
};
```

### Component Structure
```typescript
// Example component pattern
interface BureauSectionProps {
  sphereId: string;
  sectionId: SectionType;
}

export const BureauSection: FC<BureauSectionProps> = ({ sphereId, sectionId }) => {
  // ... component logic
};
```

---

# PART 4: WHAT NEEDS TO BE DONE

## 4.1 IMMEDIATE PRIORITIES

### Priority 1: API Integration
- [ ] Connect frontend to backend APIs
- [ ] Implement authentication flow
- [ ] Wire up sphere/bureau navigation
- [ ] Connect Nova chat interface

### Priority 2: Core Features
- [ ] Thread creation and management
- [ ] Notes CRUD operations
- [ ] Tasks CRUD operations
- [ ] Token balance display

### Priority 3: Governance
- [ ] Pre-execution validation UI
- [ ] Budget alerts
- [ ] Approval workflows

---

## 4.2 FEATURE COMPLETION STATUS

| Feature | Backend | Frontend | Integration |
|---------|---------|----------|-------------|
| Auth | ✅ | ✅ | ⚠️ Needs testing |
| Spheres | ✅ | ✅ | ⚠️ Needs testing |
| Bureau sections | ✅ | ✅ | ⚠️ Needs testing |
| Notes | ✅ | ✅ | ❌ Not connected |
| Tasks | ✅ | ✅ | ❌ Not connected |
| Threads | ✅ | ⚠️ Basic | ❌ Not connected |
| Nova chat | ⚠️ Basic | ✅ | ❌ Not connected |
| Tokens | ✅ | ⚠️ Display only | ❌ Not connected |
| Agents | ✅ | ⚠️ Basic | ❌ Not connected |
| Governance | ✅ | ❌ | ❌ |
| XR/VR | ⚠️ Basic | ⚠️ Basic | ❌ |

---

## 4.3 KNOWN ISSUES

1. **Frontend-Backend Integration**
   - API calls not fully wired
   - Some endpoints need CORS config
   - WebSocket connection needs work

2. **Missing UI Components**
   - Governance approval modal
   - Token allocation dialog
   - Agent hiring wizard

3. **Testing**
   - E2E tests need completion
   - API integration tests needed

---

# PART 5: DEVELOPMENT GUIDELINES

## 5.1 BEFORE WRITING ANY CODE

1. **Read the relevant documentation**
   - Check `/architecture/` for system design
   - Check `/product/` for UI specs
   - Check `/agents/` for agent behavior

2. **Verify compliance**
   - Does this add a sphere? ❌ NOT ALLOWED
   - Does this bypass governance? ❌ NOT ALLOWED
   - Does this make Nova hireable? ❌ NOT ALLOWED

3. **Follow existing patterns**
   - Use existing component structures
   - Use existing store patterns
   - Use existing API patterns

---

## 5.2 CODING STANDARDS

### TypeScript
```typescript
// ✅ Good: Typed, clear, documented
interface ThreadCreateDTO {
  title: string;
  sphereId: string;
  budget: number;
}

// ❌ Bad: Untyped, unclear
const createThread = (data: any) => { ... }
```

### React Components
```typescript
// ✅ Good: Functional, typed, clean
export const BureauSection: FC<Props> = ({ sphereId }) => {
  const { data, isLoading } = useQuery(...);
  
  if (isLoading) return <LoadingSpinner />;
  
  return <div className="bureau-section">...</div>;
};

// ❌ Bad: Class components, no types
class BureauSection extends Component { ... }
```

### API Endpoints
```python
# ✅ Good: Typed, validated, documented
@router.post("/threads", response_model=ThreadResponse)
async def create_thread(
    data: ThreadCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ThreadResponse:
    """Create a new thread with budget allocation."""
    ...

# ❌ Bad: No types, no validation
@router.post("/threads")
def create_thread(data: dict):
    ...
```

---

## 5.3 FILE ORGANIZATION

```
When adding new features:

1. Components go in: /frontend/src/components/{domain}/
2. Pages go in: /frontend/src/pages/{domain}/
3. Stores go in: /frontend/src/stores/{domain}Store.ts
4. API endpoints go in: /backend/app/api/endpoints/{domain}.py
5. Services go in: /backend/services/{domain}/

Always export from index.ts files!
```

---

## 5.4 COMMIT MESSAGES

```
Format: type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructure
- test: Tests
- chore: Maintenance

Examples:
- feat(threads): add thread creation flow
- fix(auth): resolve token refresh issue
- docs(api): update OpenAPI specs
```

---

# PART 6: QUICK REFERENCE

## 6.1 SPHERE IDS

```typescript
const SPHERE_IDS = {
  personal: 'sphere_personal',
  business: 'sphere_business',
  government: 'sphere_government',
  studio: 'sphere_studio',
  community: 'sphere_community',
  social: 'sphere_social',
  entertainment: 'sphere_entertainment',
  team: 'sphere_team',
};
```

## 6.2 BUREAU SECTION IDS

```typescript
const SECTION_IDS = {
  dashboard: 'section_dashboard',
  notes: 'section_notes',
  tasks: 'section_tasks',
  projects: 'section_projects',
  threads: 'section_threads',
  meetings: 'section_meetings',
  data: 'section_data',
  agents: 'section_agents',
  reports: 'section_reports',
  budget: 'section_budget',
};
```

## 6.3 API ENDPOINTS QUICK REFERENCE

```
Auth:     POST /api/v1/auth/login
Spheres:  GET  /api/v1/spheres
Bureau:   GET  /api/v1/bureaus/{sphere}/sections
Threads:  POST /api/v1/threads
Nova:     POST /api/v1/nova/chat
Tokens:   GET  /api/v1/tokens/balance
```

---

# PART 7: STARTING A SESSION

## 7.1 SESSION CHECKLIST

```yaml
Before coding:
  - [ ] Read this document completely
  - [ ] Check current state of relevant files
  - [ ] Identify what needs to be done
  - [ ] Plan approach before implementing

During coding:
  - [ ] Follow existing patterns
  - [ ] Add types to everything
  - [ ] Test as you go
  - [ ] Commit frequently

After coding:
  - [ ] Update documentation if needed
  - [ ] Run tests
  - [ ] Verify compliance with rules
```

## 7.2 COMMON TASKS

### "Add a new component"
1. Create file in `/frontend/src/components/{domain}/`
2. Add types interface
3. Implement component
4. Export from index.ts
5. Use in page

### "Add a new API endpoint"
1. Create route in `/backend/app/api/endpoints/`
2. Add Pydantic models
3. Implement logic
4. Add to router
5. Update OpenAPI docs

### "Fix a bug"
1. Reproduce the bug
2. Find root cause
3. Fix with minimal changes
4. Test fix
5. Commit with `fix(scope): description`

---

# PART 8: CONTACTS & RESOURCES

## 8.1 PROJECT RESOURCES

| Resource | Location |
|----------|----------|
| Full Documentation | `/CHENU_MEGA_FINAL/` |
| SQL Schema | `/database/CHENU_SQL_SCHEMA_v29.sql` |
| API Specs | `/architecture/API_CONTRACT_OPENAPI.yaml` |
| Design Tokens | `/product/DESIGN_TOKENS.json` |
| Component Library | `/frontend/src/components/` |

## 8.2 KEY FILES TO KNOW

```
Must read before working on:

UI Layout     → /product/UI_STRUCTURE.md
Spheres       → /product/SPHERE_PLACE_MAPPING.md
Agents        → /agents/AGENT_GOVERNANCE.md
Tokens        → /agents/COST_BUDGETING.md
API           → /architecture/API_CONTRACT_OPENAPI.yaml
Data Model    → /architecture/DATA_MODEL.md
XR/VR         → /xr/XR_PRINCIPLES.md
```

---

# PART 9: FINAL REMINDERS

## ⚠️ NEVER DO THESE THINGS ⚠️

```
1. ❌ Add a 9th sphere
2. ❌ Remove or rename a sphere
3. ❌ Add an 11th bureau section
4. ❌ Make Nova a hired agent
5. ❌ Call tokens "cryptocurrency"
6. ❌ Skip governance validation
7. ❌ Bypass budget checks
8. ❌ Delete audit logs
```

## ✅ ALWAYS DO THESE THINGS ✅

```
1. ✅ Follow the 8 sphere structure
2. ✅ Follow the 10 bureau sections
3. ✅ Enforce governance before execution
4. ✅ Track token costs
5. ✅ Maintain audit trails
6. ✅ Use existing patterns
7. ✅ Add types to code
8. ✅ Test your changes
```

---

# 🚀 YOU'RE READY TO CONTINUE!

Remember: **Clarity over features. Governance over automation.**

Good luck with the next session!

---

*CHE·NU™ — Governed Intelligence Operating System*
*Document generated: 2024-12-17*
