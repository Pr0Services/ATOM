# CHE·NU™ — IMPLEMENTATION BLOCKS
## CRITICAL MICROSERVICES — READY TO CODE

**VERSION:** V1 FREEZE  
**STATUS:** CANONICAL & FROZEN

---

## 🎯 PURPOSE

This directory contains **IMPLEMENTATION-READY** specifications for the **3 MOST CRITICAL** CHE·NU microservices:

1. **Identity & Context Service** — Foundation
2. **Thread Service** (.chenu) — Vertical Spine
3. **Versioning & Diff Service** — Trust & Memory

These services form the **IMMUTABLE CORE** upon which all other CHE·NU services depend.

---

## 📦 IMPLEMENTATION BLOCKS

### IB01 — Identity & Context Service
**File:** `IB01_Identity_Context_Service.md`

**Purpose:** Defines WHO acts, WHERE, WITH WHAT RIGHTS

**Key Features:**
- Identity management (personal, business, organization, role)
- Context isolation per sphere
- Active session tracking
- Scope locking (anti-escalation)
- Global guards & audit interceptors

**Dependencies:** None (Foundation)  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~2,000 lines  
**Implementation Time:** 2-3 days

---

### IB02 — Thread Service
**File:** `IB02_Thread_Service.md`

**Purpose:** Manages .chenu threads as SINGLE UNIT OF TRUTH

**Key Features:**
- Thread lifecycle (open → active → closed → archived)
- Thread entries (user & agent messages)
- Thread links (reference graph)
- Thread decisions (immutable)
- Cross-sphere read-only access

**Dependencies:** Identity & Context Service  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~3,500 lines  
**Implementation Time:** 4-5 days

---

### IB03 — Versioning & Diff Service
**File:** `IB03_Versioning_Diff_Service.md`

**Purpose:** Guarantees append-only versions, diffs, and traceability

**Key Features:**
- Append-only versioning
- Active version pointer (one per object)
- Human-readable diffs
- Rollback via new version creation
- Agent approval workflow
- State machine (draft → approved → active)

**Dependencies:** Identity & Context Service  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~4,000 lines  
**Implementation Time:** 5-6 days

---

### IB04 — Orchestrator Service
**File:** `IB04_Orchestrator_Service.md`

**Purpose:** ONLY authority to interpret intent, plan, and govern execution

**Key Features:**
- Intent interpretation & planning
- Agent selection via Skill & Tool Registry
- Execution governance & approval workflow
- Budget enforcement before execution
- Step-by-step execution control
- Result integration control

**Dependencies:** Identity & Context, Skill & Tool Registry, Agent Runtime  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~5,000 lines  
**Implementation Time:** 7-10 days

---

### IB05 — Agent Runtime Service
**File:** `IB05_Agent_Runtime_Service.md`

**Purpose:** Executes agent jobs in isolated sandboxes

**Key Features:**
- Isolated sandbox execution (filesystem, memory)
- LLM provider abstraction (OpenAI, Anthropic, Mistral)
- Resource quotas & constraints enforcement
- Token usage tracking
- Output collection (references only)
- Job lifecycle management

**Dependencies:** Orchestrator Service  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~6,000 lines  
**Implementation Time:** 8-10 days

---

### IB06 — Skill & Tool Registry Service
**File:** `IB06_Skill_Tool_Registry.md`

**Purpose:** Single source of truth for capabilities and implementations

**Key Features:**
- Skill definitions (semantic contracts with schemas)
- Tool implementations (LLM, function, binary, service)
- Skill-to-tool mapping with policies
- Sphere activation matrix
- Selection algorithm (cost, quality, policy)
- Runtime profiles (low_cost, balanced, high_quality)

**Dependencies:** Identity & Context Service  
**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**LOC Estimate:** ~4,500 lines  
**Implementation Time:** 6-8 days

---

## 🏗️ IMPLEMENTATION ORDER

### Phase 1: Foundation (2-3 days)
**Identity & Context Service**
- Set up NestJS project
- Create PostgreSQL schema
- Implement guards & interceptors
- Deploy to staging

### Phase 2: Vertical Spine (4-5 days)
**Thread Service**
- Set up service structure
- Implement thread CRUD
- Add lifecycle state machine
- Integrate with Identity Service

### Phase 3: Memory & Trust (5-6 days)
**Versioning & Diff Service**
- Create versioning schema
- Implement version creation
- Add diff computation
- Integrate with Thread Service

### Phase 4: Capability Registry (6-8 days)
**Skill & Tool Registry Service**
- Define skill & tool schemas
- Implement mapping logic
- Build selection algorithm
- Add sphere activation matrix

### Phase 5: Execution Engine (8-10 days)
**Agent Runtime Service**
- Create sandbox infrastructure
- Implement LLM provider abstraction
- Add resource monitoring
- Integrate with Orchestrator

### Phase 6: Intelligence Governor (7-10 days)
**Orchestrator Service**
- Implement intent interpretation
- Build execution planning
- Add approval workflow
- Integrate all dependencies

**Total Serial Time:** 32-42 days (1 developer)  
**Total Parallel Time:** 10-15 days (with 6 developers, 1 per service)

---

## 📊 TECHNICAL STACK

### Backend
- **Framework:** NestJS (TypeScript)
- **Database:** PostgreSQL 14+
- **ORM:** TypeORM or Prisma
- **Validation:** class-validator, class-transformer
- **API:** REST + OpenAPI/Swagger

### Infrastructure
- **Container:** Docker
- **Orchestration:** Kubernetes (optional for MVP)
- **Message Bus:** RabbitMQ or Kafka (for events)
- **Cache:** Redis (optional)

### Testing
- **Unit Tests:** Jest (80%+ coverage)
- **Integration Tests:** Supertest
- **E2E Tests:** Playwright or Cypress

---

## 🔐 SECURITY & GOVERNANCE

### Mandatory Headers
**ALL services MUST require:**
- `x-identity-id`
- `x-context-id`

**Requests without both MUST be rejected.**

### Audit Trail
**ALL write operations MUST:**
- Log to Audit Service
- Include identity + context + timestamp
- Be traceable and immutable

### Approval Workflow
**Agent-generated content MUST:**
- Default to `state='proposed'`
- Require explicit user approval
- Never auto-activate

---

## 🎯 SUCCESS CRITERIA

### Identity & Context Service
- ✅ 100% requests validated for identity + context
- ✅ Zero unauthorized context switches
- ✅ Complete audit trail for all identity transitions
- ✅ Scope locking prevents escalation during execution

### Thread Service
- ✅ Threads never mix contexts
- ✅ Decisions are immutable
- ✅ Thread links form valid graph (no cycles)
- ✅ Status transitions are enforced
- ✅ Cross-sphere access is read-only unless shared

### Versioning & Diff Service
- ✅ All changes are versioned and traceable
- ✅ No silent modifications (all tracked)
- ✅ Agent changes require user approval before activation
- ✅ Rollback creates new version (history preserved)
- ✅ Diff is human-readable and machine-usable

---

## 📈 PERFORMANCE TARGETS

### Identity & Context Service
- Response time: < 50ms (p95)
- Throughput: 10,000+ req/sec
- Concurrent sessions: 100,000+

### Thread Service
- Response time: < 100ms (p95)
- Thread creation: < 200ms
- Concurrent threads: 1,000,000+

### Versioning & Diff Service
- Version creation: < 150ms
- Diff computation: < 500ms (1MB content)
- Concurrent versions: 10,000,000+

---

## 🔗 INTEGRATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│               IDENTITY & CONTEXT SERVICE                │
│          (Foundation - All services depend on)          │
│                                                         │
└────────────┬──────────────────────────────┬─────────────┘
             │                              │
             │                              │
    ┌────────▼────────┐          ┌─────────▼─────────┐
    │                 │          │                   │
    │ THREAD SERVICE  │◄────────►│  VERSIONING &     │
    │    (.chenu)     │          │  DIFF SERVICE     │
    │                 │          │                   │
    └─────────────────┘          └───────────────────┘
             │                              │
             │                              │
             └──────────┬───────────────────┘
                        │
                        ▼
             ┌──────────────────┐
             │                  │
             │  AUDIT SERVICE   │
             │   (Log Sink)     │
             │                  │
             └──────────────────┘
```

---

## 🚀 QUICK START

### 1. Clone Implementation Templates

```bash
git clone https://github.com/your-org/chenu-services.git
cd chenu-services
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 3. Install Dependencies

```bash
npm install
```

### 4. Run Database Migrations

```bash
npm run migration:run
```

### 5. Start Services

```bash
# Identity & Context Service (port 3002)
npm run start:identity-context

# Thread Service (port 3003)
npm run start:threads

# Versioning Service (port 3004)
npm run start:versioning
```

---

## 📚 DOCUMENTATION LINKS

- **API Documentation:** `/docs` endpoint on each service (Swagger UI)
- **System Manual:** `../01_SYSTEM_MANUAL/CHENU_SYSTEM_MANUAL.md`
- **Microservices Architecture:** `../07_MICROSERVICES/CHENU_MICROSERVICES_ARCHITECTURE.md`

---

## 🔜 NEXT SERVICES

After implementing these 6 critical services, the next priorities are:

1. **Audit Log Service** — Centralized logging & compliance
2. **Budget & Governance Service** — Token budget enforcement
3. **Note Service** — Sphere-specific note management
4. **Document Service** — Document management with versioning
5. **Meeting Service** — Meeting lifecycle & recordings

**These 6 services form the IMMUTABLE CORE of CHE·NU execution.**

---

## 📝 NOTES

### Design Principles
- **Separation of Concerns**: Each service has ONE clear responsibility
- **Governed by Default**: Security and audit are built-in, not added later
- **Append-Only Philosophy**: Never delete, always version
- **Explicit Over Implicit**: All actions require explicit identity + context

### Common Patterns
- **Guards**: Validate identity + context on every request
- **Interceptors**: Audit every write operation
- **Events**: Publish state changes to message bus
- **DTOs**: Strict validation with class-validator

---

## ⚠️ CRITICAL REMINDERS

1. **NEVER skip identity/context validation**
2. **NEVER allow silent modifications**
3. **NEVER auto-activate agent content**
4. **NEVER delete versions (append-only)**
5. **ALWAYS audit write operations**
6. **ALWAYS enforce state transitions**
7. **ALWAYS validate sphere boundaries**

---

## 🎯 FINAL RULE

**These 6 services are the IMMUTABLE EXECUTION CORE of CHE·NU.**

**Any deviation from these specifications must be approved by the architecture team.**

**Once implemented, these services form the FROZEN FOUNDATION.**

---

**Core Services:**
1. Identity & Context — WHO/WHERE/RIGHTS
2. Thread — MEMORY SPINE
3. Versioning — TRUST & HISTORY
4. Skill & Tool Registry — CAPABILITIES
5. Agent Runtime — EXECUTION ENGINE
6. Orchestrator — INTELLIGENCE GOVERNOR

---

**END OF IMPLEMENTATION BLOCKS README**
