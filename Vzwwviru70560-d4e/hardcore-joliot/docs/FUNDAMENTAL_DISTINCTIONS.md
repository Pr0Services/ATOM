# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — FUNDAMENTAL DISTINCTIONS
# Canonical Architecture Clarification Document
# ═══════════════════════════════════════════════════════════════════════════════

**Version**: 1.0.0
**Status**: CANONICAL — APPLIES GLOBALLY
**Priority**: FOUNDATIONAL

---

## OVERVIEW

This document establishes the **essential distinctions** between core CHE·NU concepts.
These distinctions MUST be respected across all components:
- Schema design
- Agent prompts
- UI layout
- Sphere navigation
- Universe view
- Delegation rules
- Orchestration logic

---

## 🌐 1. SPHERES (Sphères)

### Definition
A **Sphere** is a **macro-domain** defined by its **final purpose (télos)**.
It represents a fundamental dimension of human activity.

### What Defines a Sphere

| Attribute | Description |
|-----------|-------------|
| **Objective (Télos)** | The ultimate goal |
| **Data Type** | Nature of information handled |
| **Specialized Agents** | Internal intelligent entities |
| **Tools/APIs** | Required capabilities |
| **Workflows** | Natural cycles and processes |
| **Ethical Constraints** | Privacy, permissions, governance |
| **Internal Hierarchy** | Departments and structure |

### The 11 CHE·NU Spheres

| Sphere | Emoji | Objective | Nature | Key Agents |
|--------|-------|-----------|--------|------------|
| **Personnel** | 👤 | Identity, private data, cognitive health | Intimate | Identity Guardian, Preference Agent |
| **Business** | 💼 | Production, management, revenue | Operational | CRM Agent, Task Manager |
| **Scholar** | 📚 | Learning, training | Cognitive | Tutor Agent, Knowledge Curator |
| **Creative Studio** | 🎨 | Creative production | Creative | Render Agent, Audio/Video Agent |
| **Social & Media** | 📱 | Interaction, expression | Social | Social Poster Agent, Trend Analyzer |
| **Institutions** | 🏛️ | Governance, compliance | Regulatory | Compliance Agent |
| **Methodology** | ⚙️ | Optimization, decisions | Meta | Strategy Agent, Arbiter Agent |
| **XR / Immersive** | 🥽 | Visualization, collaboration | Spatial | XR Meeting Agent, Replay Agent |
| **Divertissement** | 🎮 | Leisure, games, wellbeing | Ludic | Entertainment Flow Agent |
| **IA Lab** | 🧠 | AI experimentation | Technical | Model Trainer, Sandbox Agent |
| **My Team** | 👥 | Human collaboration | Organizational | Team Sync Agent |

### Critical Rule
> **No sphere has the same télos (purpose).**
> This prevents logical conflicts in orchestration.

---

## 🧩 2. DEPARTMENTS (Départements)

### Definition
A **Department** is an **internal functional subdivision** inside a sphere.
It exists **independently of agents**.

### Key Distinction

| Concept | Scope | Example |
|---------|-------|---------|
| **Sphere** | A place in life (macro) | Business |
| **Department** | A function (micro) | Accounting, Sales, R&D |

### Examples per Sphere

#### 💼 Business Sphere
```
Departments:
├── Comptabilité (Accounting)
├── Ventes (Sales)
├── R&D
├── Operations
└── HR
```

#### 👤 Personnel Sphere
```
Departments:
├── Santé (Health)
├── Journal (Journal)
├── Mémoire (Memory)
├── Finance personnelle (Personal Finance)
└── Identité (Identity)
```

#### 📚 Scholar Sphere
```
Departments:
├── Cours (Courses)
├── Notes
├── Exercices (Exercises)
├── Projets (Projects)
└── Références (References)
```

#### 🎨 Creative Studio Sphere
```
Departments:
├── Design
├── Audio
├── Video
├── Photography
└── Writing
```

### Critical Rule
> Each sphere can have **similar department names**,
> but their **role changes according to functional context**.

---

## 🔌 3. APIs (Capacités)

### Definition
**APIs are capabilities, NOT domains.**
They do not belong to any sphere.

### Key Distinction

| Concept | Nature | Example |
|---------|--------|---------|
| **Sphere** | "Why" (purpose) | Creative Studio |
| **API** | "How" (capability) | Image Generation API |

### API Usage Across Spheres

| API | Used By |
|-----|---------|
| Speech-to-Text | XR, Scholar, Business |
| Image Generation | Creative Studio, Social, IA Lab |
| Vector DB | Methodology, Scholar, Business |
| TTS (Text-to-Speech) | XR, Creative, Accessibility |
| Embeddings | All spheres (search) |
| XR Capture | XR, Creative, Business |

### Critical Rule
> An API belongs to **no sphere**,
> but can be **used by multiple departments** according to their mission.

---

## 🛠 4. TASK TYPES (Types de Tâches)

### Universal Task Categories

| Type | Description |
|------|-------------|
| **Analytical** | Analysis, research, evaluation |
| **Creative** | Design, production, invention |
| **Decision-making** | Choices, arbitration, strategy |
| **Operational** | Execution, management, processing |
| **Administrative** | Filing, organization, maintenance |
| **Social** | Communication, interaction, sharing |
| **Immersive (XR)** | Spatial, 3D, virtual presence |

### Sphere-Specific Interpretations

Each sphere **inherits** these types but **re-interprets** them:

| Sphere | Task Examples |
|--------|---------------|
| **Business** | Gestion, planification, pipeline |
| **Scholar** | Résumés, QCM, explication |
| **Creative** | Design, montage, rendu |
| **XR** | Capture de position, replay, spatial mapping |
| **Social** | Post creation, engagement, scheduling |
| **Methodology** | Process optimization, workflow design |

---

## 🎯 5. SPHERE OBJECTIVES (Télos)

### Each Sphere Has a Unique Purpose

| Sphere | Objective (Télos) |
|--------|-------------------|
| **Creative Studio** | Transform an idea into visual/audio production |
| **Scholar** | Transform unknown into mastered knowledge |
| **Methodology** | Optimize how things are done |
| **Social** | Diffuse, connect, express |
| **Personnel** | Stabilize, protect, organize one's life |
| **XR** | Understand and manipulate space |
| **IA Lab** | Develop new AI capabilities |
| **Business** | Produce value and generate revenue |
| **Institutions** | Ensure compliance and governance |
| **My Team** | Coordinate human collaboration |
| **Divertissement** | Provide leisure and wellbeing |

### Critical Rule
> The télos (purpose) **informs orchestration**.
> Conflicts between spheres are resolved by comparing objectives.

---

## 🧠 6. AGENTS vs DEPARTMENTS

### Essential Distinction

| Concept | Definition | Can Exist Without |
|---------|------------|-------------------|
| **Department** | Organizational location | Agents (yes) |
| **Agent** | Intelligent entity executing actions | Department (NO) |

### Example: Business/Sales

```
Department: Sales
├── Sub-departments:
│   ├── Pipeline
│   ├── Contacts
│   └── Prévisions (Forecasts)
│
├── Agents operating here:
│   ├── CRM Agent
│   ├── Follow-Up Agent
│   └── Reporting Agent
```

### Critical Rules
> - A department **can exist with zero agents**
> - An agent **must always belong to exactly one department**
> - Agents are executors, departments are containers

---

## 🧷 7. INTERNAL / EXTERNAL INTERACTIONS

### Interaction Types

| Type | Description | Scope |
|------|-------------|-------|
| **Internal** | Never leaves CHE·NU | Full control |
| **External** | APIs, social networks, exports | Governed access |
| **Semi-external** | XR meetings with other users | Hybrid rules |

### Each Type Has

| Attribute | Internal | External | Semi-External |
|-----------|----------|----------|---------------|
| Permissions | Full | Restricted | Context-based |
| Governance | System | User + Policy | User + Protocol |
| Format | Any | Standardized | Protocol-based |
| Security | Standard | Enhanced | Enhanced |

### Critical Rule
> External operations **must follow governance and permissions**.
> Internal operations remain **fully manipulable** within CHE·NU.

---

## 📦 IMPLEMENTATION BLOCK FOR CLAUDE

```
BEGIN BLOCK FOR CLAUDE

You must integrate a clear structural distinction between spheres, departments, APIs, task types, and objectives. Apply the following definitions globally:

1. A Sphere is a macro-domain defined by its final purpose (télos), type of data, agents, workflows, and ethical constraints. It represents a dimension of human activity (e.g., Business, Scholar, Creative, Social, XR, Institutions, Methodology, IA Lab, My Team, Divertissement, Personnel).

2. A Department is an internal functional subdivision inside a sphere. It exists independently of agents. Examples: Accounting, Sales, R&D (Business). Notes, Courses, Exams (Scholar). Design, Audio, Video (Creative). Agents act inside departments.

3. APIs are capabilities, not domains. They do not belong to any sphere. They are reusable tools activated by agents and departments depending on the context. Examples: STT, TTS, Embeddings, Image generation, Vector DB, XR capture.

4. Tasks differ by operational type: analytical, creative, decision-making, operational, administrative, social, immersive. Each sphere reinterprets these types according to its own purpose.

5. Each sphere must have an explicitly stated objective that informs orchestration. Example: Creative = transform idea to production. Scholar = transform unknown to knowledge. Methodology = optimize processes. Social = diffuse/express. Personnel = organize/protect. XR = understand space. IA Lab = develop IA abilities. My Team = coordinate humans.

6. Agents are intelligent executors. Departments are organizational containers. A department can exist with zero agents. An agent must always belong to exactly one department.

7. Internal operations remain fully inside CHE-NU. External operations (API calls, social media posting, exports) must follow governance and permissions. Semi-external operations (XR meetings) follow hybrid rules.

8. Implement this structure in schema, agent prompts, UI layout, sphere navigation logic, universe view, and delegation rules.

END BLOCK FOR CLAUDE
```

---

## VISUAL HIERARCHY

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CHE·NU UNIVERSE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         🌐 SPHERE                                    │    │
│  │                    (Macro-domain with Télos)                         │    │
│  │                                                                      │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    📁 DEPARTMENT                             │    │    │
│  │  │               (Functional subdivision)                       │    │    │
│  │  │                                                              │    │    │
│  │  │  ┌───────────────────────────────────────────────────────┐  │    │    │
│  │  │  │                   🤖 AGENT                             │  │    │    │
│  │  │  │            (Intelligent executor)                      │  │    │    │
│  │  │  │                                                        │  │    │    │
│  │  │  │  Uses: 🔌 APIs (capabilities)                          │  │    │    │
│  │  │  │  Executes: 📋 Tasks (typed actions)                    │  │    │    │
│  │  │  └───────────────────────────────────────────────────────┘  │    │    │
│  │  │                                                              │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  🔗 CROSS-CUTTING CONCERNS:                                                 │
│  ├── APIs (shared capabilities)                                             │
│  ├── Orchestration (cross-sphere coordination)                              │
│  ├── Memory (cross-sphere context)                                          │
│  └── Governance (permissions & ethics)                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## VALIDATION CHECKLIST

Before any implementation, verify:

- [ ] Sphere has explicit télos (purpose)
- [ ] Departments are containers, not executors
- [ ] Agents belong to exactly one department
- [ ] APIs are sphere-agnostic capabilities
- [ ] Task types are sphere-interpreted
- [ ] Internal/External distinction respected
- [ ] Orchestration uses télos for conflict resolution

---

## DATABASE IMPLICATIONS

### Sphere Table
```sql
CREATE TABLE core.spheres (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    telos TEXT NOT NULL,  -- The purpose
    nature VARCHAR(50),
    ...
);
```

### Department Table
```sql
CREATE TABLE core.departments (
    id UUID PRIMARY KEY,
    sphere_id VARCHAR(50) REFERENCES core.spheres(id),
    code VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    -- No agent_id here! Departments exist independently
    ...
);
```

### Agent Table
```sql
CREATE TABLE core.agents (
    id VARCHAR(100) PRIMARY KEY,
    department_id UUID REFERENCES core.departments(id) NOT NULL,  -- REQUIRED
    -- Agent MUST belong to a department
    ...
);
```

### API Registry (Sphere-Agnostic)
```sql
CREATE TABLE core.api_registry (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    -- NO sphere_id! APIs are capabilities, not domains
    ...
);
```

---

**END OF FUNDAMENTAL DISTINCTIONS**

*CHE·NU Canonical Architecture*
*Pro-Service Construction*
