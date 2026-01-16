# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — DOMAIN ARCHITECTURE
# Domain → Department → Sphere Differentiation
# ═══════════════════════════════════════════════════════════════════════════════

**Version**: 1.0.0
**Status**: CANONICAL
**Priority**: FOUNDATIONAL — SUPERSEDES IMPLICIT ASSUMPTIONS

---

## OVERVIEW

This document establishes explicit differentiation between DOMAINS, DEPARTMENTS, and SPHERES.
**No concept may be merged implicitly.**
Every distinction must be enforceable in code, data models, agents, UI, and orchestration.

---

## SECTION 1 — THE THREE LAYERS

### 🌍 DOMAIN (Layer 1 — Fundamental Reality)

**Definition**: A domain is a **fundamental reality layer** with its own purpose, ethics, data types, and interaction rules.

| Property | Description |
|----------|-------------|
| **Nature** | Ontological category of human activity |
| **Ethics** | Inherent moral constraints |
| **Data Types** | Types of information that exist here |
| **Interaction Rules** | How entities relate within |
| **Boundaries** | Hard walls between domains |

**DOMAINS NEVER OVERLAP IMPLICITLY.**
Cross-domain access requires **explicit bridges**.

#### CHE·NU Domains

| Domain | Code | Purpose | Nature |
|--------|------|---------|--------|
| **Personal** | `PERSONAL` | Identity, privacy, wellbeing | Intimate |
| **Business** | `BUSINESS` | Production, commerce, management | Operational |
| **Scholar** | `SCHOLAR` | Learning, research, knowledge | Cognitive |
| **Creative** | `CREATIVE` | Artistic creation, generation | Generative |
| **Social** | `SOCIAL` | Interaction, expression, community | Relational |
| **Institutional** | `INSTITUTIONAL` | Governance, compliance, regulations | Regulatory |
| **Methodology** | `METHODOLOGY` | Process evaluation, optimization | Meta |
| **XR** | `XR` | Spatial experience, immersion | Experiential |

---

### 🏢 DEPARTMENT (Layer 2 — Operational Subdivision)

**Definition**: A department is an **operational subdivision** inside a domain. It defines workflows, APIs, KPIs, and specialized agents.

| Property | Description |
|----------|-------------|
| **Parent** | Always belongs to exactly ONE domain |
| **Workflows** | Specific operational processes |
| **APIs** | Available capabilities |
| **KPIs** | Measurable objectives |
| **Agents** | Specialized agents assigned here |

**Departments inherit domain laws but can add constraints.**
Departments CANNOT relax domain constraints.

#### Example: Business Domain Departments

```
BUSINESS Domain
├── Department: Sales
│   ├── Workflows: Lead capture, Pipeline, Closing
│   ├── APIs: CRM, Calendar, Communication
│   ├── KPIs: Conversion rate, Revenue, Cycle time
│   └── Agents: Sales_Agent, CRM_Agent
│
├── Department: Accounting
│   ├── Workflows: Invoicing, Reconciliation, Reporting
│   ├── APIs: Banking, Tax, Invoicing
│   ├── KPIs: Cash flow, AR days, Accuracy
│   └── Agents: Accounting_Agent, Invoice_Agent
│
├── Department: Operations
│   ├── Workflows: Scheduling, Resource allocation, QC
│   ├── APIs: Project management, Inventory
│   ├── KPIs: Efficiency, Utilization, Delivery
│   └── Agents: Project_Agent, Resource_Agent
│
└── Department: HR
    ├── Workflows: Hiring, Onboarding, Performance
    ├── APIs: Recruitment, Payroll
    ├── KPIs: Retention, Time-to-hire, Satisfaction
    └── Agents: HR_Agent, Onboarding_Agent
```

---

### 🔮 SPHERE (Layer 3 — User Instance)

**Definition**: A sphere is a **user-instantiated instance** of a domain (or combination of departments).

| Property | Description |
|----------|-------------|
| **Parent Domain** | Inherits from exactly ONE domain |
| **Active Departments** | Which departments are enabled |
| **Data** | Concrete user data |
| **Agents** | Active agent instances |
| **Meetings** | Meeting room instances |
| **Memory** | Sphere-specific memory context |
| **UI State** | Layout, preferences, organization |

**Each sphere has its own:**
- Database namespace
- Organizer agent instance
- Memory context
- UI configuration

---

## SECTION 2 — LAYER HIERARCHY ENFORCEMENT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHE·NU LAYER HIERARCHY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   DOMAIN (Reality Layer)                                                    │
│   ══════════════════════                                                    │
│   │ Purpose, Ethics, Data Types, Boundaries                                 │
│   │ HARD WALLS — No implicit crossing                                       │
│   │                                                                         │
│   ├──► DEPARTMENT (Operational Layer)                                       │
│   │    ════════════════════════════════                                     │
│   │    │ Workflows, APIs, KPIs, Constraints                                 │
│   │    │ Inherits domain laws + can add restrictions                        │
│   │    │                                                                    │
│   │    └──► SPHERE (User Instance Layer)                                    │
│   │         ═══════════════════════════════                                 │
│   │         │ Concrete data, agents, meetings, memory                       │
│   │         │ One namespace per sphere                                      │
│   │         │ User-customizable within constraints                          │
│   │                                                                         │
│   CROSS-DOMAIN BRIDGE (Explicit Only)                                       │
│   ════════════════════════════════════                                      │
│   │ Requires: Source auth + Target auth + Audit log                         │
│   │ Cannot: Transfer forbidden data types                                   │
│   │ Must: Log every crossing                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## SECTION 3 — CANONICAL DIFFERENTIATION MATRIX

### 🌍 PERSONAL Domain

| Property | Value |
|----------|-------|
| **Code** | `PERSONAL` |
| **Primary Objective** | Protect identity, privacy, wellbeing |
| **Allowed Tasks** | Self-reflection, journaling, health tracking, personal finance, preferences |
| **Forbidden Tasks** | External sharing without consent, monetization of personal data |
| **Primary APIs** | Identity, Health, Memory, Preferences |
| **Secondary APIs** | Calendar (personal), Notes |
| **Data Sensitivity** | **CRITICAL** — Maximum protection |
| **Default Agents** | Identity_Guardian, Preference_Agent, Health_Monitor |
| **Meeting Types** | Self-reflection, Personal planning |
| **Export Permissions** | **RESTRICTED** — User explicit approval required |

---

### 💼 BUSINESS Domain

| Property | Value |
|----------|-------|
| **Code** | `BUSINESS` |
| **Primary Objective** | Generate value, manage operations, ensure profitability |
| **Allowed Tasks** | CRM, forecasting, project management, invoicing, reporting |
| **Forbidden Tasks** | Personal data exploitation, non-compliant practices |
| **Primary APIs** | CRM, Project_Management, Invoicing, Analytics |
| **Secondary APIs** | Calendar, Communication, Document_Management |
| **Data Sensitivity** | **HIGH** — Business confidential |
| **Default Agents** | CRM_Agent, Project_Agent, Finance_Agent, Sales_Agent |
| **Meeting Types** | Strategy, Planning, Review, Decision, Negotiation |
| **Export Permissions** | **CONTROLLED** — Role-based |

---

### 📚 SCHOLAR Domain

| Property | Value |
|----------|-------|
| **Code** | `SCHOLAR` |
| **Primary Objective** | Learning, knowledge acquisition, research |
| **Allowed Tasks** | Learning paths, exploration, citation, research, tutoring |
| **Forbidden Tasks** | Plagiarism, credential falsification |
| **Primary APIs** | Knowledge_Graph, Citation, Learning_Path, Quiz |
| **Secondary APIs** | Document_Analysis, Search |
| **Data Sensitivity** | **MEDIUM** — Educational context |
| **Default Agents** | Tutor_Agent, Knowledge_Curator, Research_Agent |
| **Meeting Types** | Learning session, Study group, Research discussion |
| **Export Permissions** | **OPEN** — With attribution |

---

### 🎨 CREATIVE Domain

| Property | Value |
|----------|-------|
| **Code** | `CREATIVE` |
| **Primary Objective** | Artistic creation, divergent thinking, generation |
| **Allowed Tasks** | Ideation, generation, rendering, composition, exploration |
| **Forbidden Tasks** | Copyright infringement, unauthorized reproduction |
| **Primary APIs** | Image_Gen, Audio_Gen, Video_Gen, Text_Gen |
| **Secondary APIs** | Asset_Management, Versioning |
| **Data Sensitivity** | **MEDIUM** — IP protection |
| **Default Agents** | Render_Agent, Audio_Agent, Video_Agent, Ideation_Agent |
| **Meeting Types** | Brainstorm, Creative review, Critique |
| **Export Permissions** | **FLEXIBLE** — With IP tracking |

---

### 📱 SOCIAL Domain

| Property | Value |
|----------|-------|
| **Code** | `SOCIAL` |
| **Primary Objective** | Human connection, expression, community building |
| **Allowed Tasks** | Posting, engagement, trend analysis, community management |
| **Forbidden Tasks** | Harassment, manipulation, misinformation |
| **Primary APIs** | Social_Platforms, Analytics, Scheduling, Messaging |
| **Secondary APIs** | Content_Creation, Audience_Analysis |
| **Data Sensitivity** | **VARIABLE** — Context dependent |
| **Default Agents** | Social_Poster, Trend_Analyzer, Community_Agent |
| **Meeting Types** | Content planning, Community sync, Campaign review |
| **Export Permissions** | **PUBLIC-READY** — Designed for sharing |

---

### 🏛️ INSTITUTIONAL Domain

| Property | Value |
|----------|-------|
| **Code** | `INSTITUTIONAL` |
| **Primary Objective** | Compliance, governance, regulatory adherence |
| **Allowed Tasks** | Compliance checking, audit trails, certification, reporting |
| **Forbidden Tasks** | Circumventing regulations, falsifying records |
| **Primary APIs** | Compliance_Check, Audit_Log, Certification, Reporting |
| **Secondary APIs** | Document_Management, Workflow |
| **Data Sensitivity** | **CRITICAL** — Legal implications |
| **Default Agents** | Compliance_Agent, Audit_Agent, Regulatory_Agent |
| **Meeting Types** | Audit, Compliance review, Governance, Board meeting |
| **Export Permissions** | **STRICT** — Full audit trail required |

---

### ⚙️ METHODOLOGY Domain

| Property | Value |
|----------|-------|
| **Code** | `METHODOLOGY` |
| **Primary Objective** | Process evaluation, optimization, decision quality |
| **Allowed Tasks** | Framework application, process analysis, methodology selection |
| **Forbidden Tasks** | None specific — meta-domain |
| **Primary APIs** | Framework_Library, Process_Analysis, Quality_Metrics |
| **Secondary APIs** | All domain APIs (read-only for evaluation) |
| **Data Sensitivity** | **LOW** — Process metadata |
| **Default Agents** | Methodology_Agent, Strategy_Agent, Arbiter_Agent |
| **Meeting Types** | Process review, Methodology selection, Retrospective |
| **Export Permissions** | **OPEN** — Process documentation |

**Special Property**: Methodology domain has **read-only cross-domain access** for evaluation purposes.

---

### 🥽 XR Domain

| Property | Value |
|----------|-------|
| **Code** | `XR` |
| **Primary Objective** | Spatial experience, immersive collaboration |
| **Allowed Tasks** | Spatial visualization, immersive meetings, presence-based work |
| **Forbidden Tasks** | Authoritative decisions without 2D backup |
| **Primary APIs** | XR_Rendering, Spatial_Audio, Hand_Tracking, Replay |
| **Secondary APIs** | Sync_with_2D, Session_Recording |
| **Data Sensitivity** | **MEDIUM** — Experiential data |
| **Default Agents** | XR_Meeting_Agent, Spatial_Agent, Replay_Agent |
| **Meeting Types** | Immersive review, Spatial brainstorm, Presence session |
| **Export Permissions** | **DERIVED** — Must sync to MR-2D |

**CRITICAL RULE**: XR domain is **experiential only** and **NEVER authoritative alone**.
All XR sessions MUST be reconstructable in Meeting Room 2D.

---

## SECTION 4 — CROSS-DOMAIN BRIDGE PROTOCOL

### When Cross-Domain Access is Needed

| Scenario | Bridge Type |
|----------|-------------|
| Business needs personal calendar | Explicit read bridge |
| Creative uses business assets | Asset licensing bridge |
| Scholar accesses institutional records | Compliance bridge |
| XR session needs business data | Sync bridge |

### Bridge Requirements

```json
{
  "bridge_id": "uuid",
  "source_domain": "string",
  "target_domain": "string",
  "access_type": "read|write|sync",
  "data_scope": ["specific_types"],
  "authorized_by": "user_id",
  "authorized_at": "datetime",
  "expires_at": "datetime|null",
  "audit_all": true
}
```

### Bridge Constraints

1. **Source domain must authorize export**
2. **Target domain must authorize import**
3. **Forbidden data types cannot cross**
4. **Every crossing is logged**
5. **Bridges can be revoked instantly**

---

## SECTION 5 — DATABASE SCHEMA

### Domain Registry

```sql
CREATE TABLE core.domains (
    code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    
    primary_objective TEXT NOT NULL,
    allowed_tasks TEXT[] NOT NULL,
    forbidden_tasks TEXT[] NOT NULL,
    
    primary_apis TEXT[] NOT NULL,
    secondary_apis TEXT[],
    
    data_sensitivity VARCHAR(20) NOT NULL 
        CHECK (data_sensitivity IN ('low', 'medium', 'high', 'critical')),
    
    default_agents TEXT[] NOT NULL,
    allowed_meeting_types TEXT[] NOT NULL,
    export_permissions VARCHAR(30) NOT NULL,
    
    special_properties JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Department Registry

```sql
CREATE TABLE core.departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_code VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    code VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    name_fr VARCHAR(200) NOT NULL,
    
    workflows TEXT[] NOT NULL,
    available_apis TEXT[] NOT NULL,
    kpis JSONB,
    
    additional_constraints JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(domain_code, code)
);
```

### Sphere Instance

```sql
CREATE TABLE core.spheres (
    id VARCHAR(50) PRIMARY KEY,
    user_id UUID NOT NULL,
    domain_code VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    name VARCHAR(200) NOT NULL,
    active_departments UUID[],
    
    database_namespace VARCHAR(100) NOT NULL UNIQUE,
    
    organizer_agent_id VARCHAR(100),
    memory_context_id UUID,
    
    ui_state JSONB,
    preferences JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Cross-Domain Bridge

```sql
CREATE TABLE core.domain_bridges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    source_domain VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    target_domain VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    access_type VARCHAR(20) NOT NULL CHECK (access_type IN ('read', 'write', 'sync')),
    data_scope TEXT[] NOT NULL,
    
    authorized_by UUID NOT NULL,
    authorized_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    is_active BOOLEAN DEFAULT TRUE,
    revoked_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(source_domain, target_domain, access_type)
);

CREATE TABLE core.bridge_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bridge_id UUID NOT NULL REFERENCES core.domain_bridges(id),
    
    operation VARCHAR(50) NOT NULL,
    data_transferred JSONB,
    
    source_sphere_id VARCHAR(50),
    target_sphere_id VARCHAR(50),
    
    performed_by UUID,
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## SECTION 6 — ENFORCEMENT RULES

### Rule 1: Domain Isolation
- No implicit data sharing between domains
- No agent can operate across domains without bridge

### Rule 2: Department Inheritance
- Departments MUST inherit all domain constraints
- Departments CAN add stricter constraints
- Departments CANNOT relax domain constraints

### Rule 3: Sphere Instantiation
- Each sphere belongs to exactly ONE domain
- Sphere inherits domain + selected departments
- Sphere has isolated namespace

### Rule 4: API Scoping
- Primary APIs are domain-guaranteed
- Secondary APIs are domain-available
- Cross-domain APIs require explicit bridge

### Rule 5: Agent Assignment
- Agents belong to ONE department
- Agents operate within department scope
- Cross-department operation requires orchestration

---

## VALIDATION TESTS

```python
def test_domain_isolation():
    """Verify no implicit cross-domain data access"""
    pass

def test_department_inheritance():
    """Verify departments inherit domain constraints"""
    pass

def test_sphere_namespace():
    """Verify sphere has isolated namespace"""
    pass

def test_bridge_audit():
    """Verify all bridge crossings are logged"""
    pass

def test_forbidden_crossing():
    """Verify forbidden data cannot cross domains"""
    pass
```

---

**END OF DOMAIN ARCHITECTURE**

*CHE·NU Canonical Architecture*
*Pro-Service Construction*
