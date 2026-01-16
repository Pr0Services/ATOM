# CHE·NU V1 — INTEGRATION ROADMAP + SHIP SEQUENCE

**Version:** V1 MVP FREEZE  
**Date:** 16 décembre 2025  
**Status:** Production Implementation Plan  
**Timeline:** 21 Days to Launch

---

## 🎯 MISSION

Transform scattered codebase into production-ready CHE·NU V1 MVP following ALL canonical documents.

**Target:** Governed Intelligence OS ready to launch in 3 weeks

---

## 1️⃣ INFRASTRUCTURE REQUIREMENTS (Complete List)

### 🧠 A. LLM & AI (Multi-Provider, Governed)

#### Obligatoire (MVP)

```yaml
OpenAI API:
  - GPT-4.1 (reasoning, orchestration)
  - GPT-4.1-mini (fast operations)
  - Usage: Orchestrator, L0/L1 agents
  - Monthly cost estimate: $500-2000
  - Governance: All calls via approval pipeline

Anthropic Claude:
  - Claude Sonnet 4.5 (analysis, structuring)
  - Claude Haiku 4.5 (fast tasks)
  - Usage: Consolidation, encoding, staging work
  - Monthly cost estimate: $300-1500
  - Governance: Staging only, human approval required
```

#### Optionnel / Recommandé

```yaml
Local LLM:
  - Ollama / LM Studio
  - For: tests, privacy, offline mode
  - Cost: Infrastructure only
  
Embedding API:
  - OpenAI text-embedding-3 OR
  - Cohere embed-v3 OR
  - Local: sentence-transformers
  - Usage: Search indexing, semantic similarity
  - Monthly cost: $50-300
```

---

### 🗄️ B. Databases (Strict Separation)

#### 1. Base Principale (Append-Only, Canonical)

```yaml
PostgreSQL:
  Version: 15+
  Extensions:
    - uuid-ossp
    - pgcrypto
    - pg_trgm (search)
  
  Tables:
    - threads (immutable)
    - decisions (immutable)
    - versions (immutable)
    - audit_logs (append-only)
    - identities
    - spheres
    - contexts
    - user_workspaces
    - agent_staging_workspaces
    - comparison_sessions
  
  Rules:
    - NO DELETE operations
    - Only INSERT and SELECT
    - UPDATE only for status fields
    - All content = append/archive only
  
  Hosting Options:
    - AWS RDS
    - Google Cloud SQL
    - Digital Ocean Managed PostgreSQL
    - Self-hosted (Docker)
  
  Monthly Cost: $25-200 (depending on scale)
```

#### 2. Object Storage (Document Versions)

```yaml
Object Storage:
  Options:
    - AWS S3 (recommended)
    - Google Cloud Storage
    - Cloudflare R2 (cost-effective)
  
  Structure:
    /{identity_id}/{sphere}/{content_id}/{version_id}
  
  Rules:
    - Each version = immutable object
    - Versioning enabled at storage level
    - No overwrites ever
  
  Monthly Cost: $10-100 (depending on usage)
```

#### 3. Search Index (Scoped, Metadata Only)

```yaml
Search Engine:
  Options:
    - Meilisearch (recommended for MVP)
    - OpenSearch
    - Typesense
  
  Index Structure:
    - Metadata only (titles, snippets)
    - Sphere-scoped
    - Identity-scoped
    - Read-only for cross-sphere
  
  Monthly Cost: $20-100
```

---

### 🌐 C. Servers & Infrastructure

#### Backend Services

```yaml
API Gateway:
  Tech: Node.js + Express OR FastAPI
  
  Required Middleware:
    - Identity header enforcement
    - Sphere context enforcement
    - Approval token validation
    - Rate limiting
    - Audit logging
  
  Hosting:
    - AWS ECS/Fargate
    - Google Cloud Run
    - Digital Ocean App Platform
    - Self-hosted (Docker Compose)
  
  Monthly Cost: $50-300

Agent Runtime:
  Tech: Docker containers
  Isolation: Full sandbox per agent
  Access: Staging workspaces only (DB-level enforcement)
  
  Monthly Cost: Included in compute
```

#### Frontend Services

```yaml
Web App:
  Tech: React + Next.js
  Hosting:
    - Vercel (recommended)
    - Netlify
    - CloudFlare Pages
  
  Monthly Cost: $0-100 (Vercel free tier sufficient for MVP)

Mobile App (Post-MVP):
  Tech: React Native + Expo
  Distribution: App Store + Google Play
  
  Monthly Cost: $100 (developer accounts)
```

#### Infrastructure

```yaml
Container Orchestration:
  MVP: Docker Compose
  Production: Kubernetes (post-MVP)
  
  Hosting Options:
    - AWS ECS
    - Google GKE
    - Digital Ocean Kubernetes
  
  Monthly Cost: $100-500

Cloud Provider (Full Stack):
  Recommended: AWS OR Google Cloud OR Digital Ocean
  
  Estimated Total Monthly Cost (MVP):
    - Compute: $50-200
    - Database: $25-200
    - Storage: $10-100
    - AI APIs: $800-3500
    - Other services: $50-200
    ──────────────────────────
    TOTAL: $935-4200/month
```

---

### 🔐 D. Security & Governance

```yaml
Authentication:
  Service: Auth0 OR Supabase Auth OR Custom OAuth2
  Features:
    - Multi-identity support
    - Social logins
    - MFA support
  
  Monthly Cost: $0-100 (Auth0 free tier sufficient for MVP)

Secrets Management:
  Options:
    - HashiCorp Vault
    - AWS Secrets Manager
    - Google Secret Manager
  
  Monthly Cost: $10-50

Rate Limiting:
  Service: Redis + rate-limiter-flexible
  Monthly Cost: $10-30

Audit & Monitoring:
  Logging: CloudWatch OR DataDog OR Self-hosted
  Monitoring: Prometheus + Grafana OR DataDog
  
  Monthly Cost: $50-200
```

---

### 🌍 E. Browser & External Platforms

```yaml
Embedded Browser:
  Tech: Electron WebView OR Chromium embedded
  
  Features:
    - Multi-profile support (Facebook, Google, etc)
    - Manual extraction only
    - No auto-ingestion
  
  Monthly Cost: Infrastructure only

Browser Automation (Optional):
  Service: Playwright OR Puppeteer
  Usage: Controlled extraction only
  
  Monthly Cost: Infrastructure only
```

---

### 🎥 F. Media & XR (Progressive Activation)

```yaml
Media Services:
  Video Streaming:
    - Mux (recommended)
    - Cloudflare Stream
    Monthly Cost: $10-100
  
  Audio/Voice (Post-MVP):
    - ElevenLabs
    - OpenAI Voice API
    Monthly Cost: $50-200

XR/3D Services:
  Libraries:
    - Three.js (free)
    - Babylon.js (free)
    - React Three Fiber (free)
  
  WebXR:
    - Native browser support (free)
  
  3D Assets (Optional):
    - Sketchfab
    - Poly Haven
  
  Monthly Cost: $0-100 (depending on asset needs)

Unity/Unreal (Future):
  For native VR apps
  Monthly Cost: Variable
```

---

## 📊 TOTAL COST SUMMARY

### MVP Phase (3 months)

```
Development Infrastructure: $200-500/month
AI API Usage: $800-3500/month
Database & Storage: $50-400/month
Authentication & Security: $50-150/month
Monitoring & Tools: $50-200/month
─────────────────────────────────────
TOTAL MVP: $1,150-4,750/month

Recommended Budget: $2,500/month for comfortable MVP
```

### Production Phase (6+ months)

```
Scale factor: 2-5x MVP costs
Expected: $5,000-20,000/month depending on user growth
```

---

## 2️⃣ SPHERES AS PLACES — DEEP ARCHITECTURE

### 🧭 FUNDAMENTAL PRINCIPLE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  A sphere is not a menu.                      ║
║  A sphere is a PLACE.                         ║
║                                               ║
║  Each CHE·NU sphere is:                       ║
║  - A conceptual space                         ║
║  - A functional space                         ║
║  - A visual space                             ║
║  - A potential XR space                       ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

### 🏛️ CANONICAL SPHERE STRUCTURE

Every sphere contains:

```
1. ENTRANCE HALL
   - Welcome area
   - Navigation hub
   - Nova presence
   - Context reminder

2. BUREAUX / OFFICES
   - Threads display
   - Documents area
   - Active workspaces
   
3. ARCHIVES
   - Version history
   - Audit logs
   - Old decisions

4. ATELIER / WORKSPACE
   - Active editing area
   - Agent staging zone
   - Review/comparison space

5. MEETING ROOM
   - Collaboration space
   - Multi-user (post-MVP)
   
6. AGENT BACKSTAGE
   - Where agents work
   - Not directly visible to user
   - Observable via status indicators
```

---

### 🎨 4 VISUAL THEMES (Transversal)

Every sphere can be rendered in 4 interchangeable themes:

#### 1️⃣ FUTURISTIC

```yaml
Materials:
  - Glass (frosted, transparent)
  - Soft metal (brushed aluminum)
  - Glowing edges
  
Colors:
  Primary: Electric Blue (#3B82F6)
  Accent: Cyan (#06B6D4)
  Background: Deep Navy (#0F172A)
  
Lighting:
  - Neon accents
  - Floating holograms
  - Soft blue ambient

Best For:
  - IA Labs
  - Business
  - Tech projects
  
Mood: Innovative, professional, cutting-edge
```

#### 2️⃣ NATURAL

```yaml
Materials:
  - Wood (oak, walnut)
  - Stone (warm)
  - Plants/greenery
  - Linen textures
  
Colors:
  Primary: Forest Green (#22C55E)
  Accent: Warm Brown (#78350F)
  Background: Cream (#FAFAF9)
  
Lighting:
  - Warm sunlight
  - Natural shadows
  - Soft ambient

Best For:
  - Personal
  - Community
  - Creative work
  
Mood: Calm, organic, grounded
```

#### 3️⃣ ASTRAL

```yaml
Materials:
  - Space void
  - Constellation patterns
  - Mystical symbols
  - Ethereal glow
  
Colors:
  Primary: Deep Purple (#8B5CF6)
  Accent: Star White (#FFFFFF)
  Background: Cosmic Black (#000000)
  
Lighting:
  - Starlight
  - Data as constellations
  - Glowing connections

Best For:
  - Strategy
  - Reflection
  - Long-term planning
  
Mood: Contemplative, mysterious, vast
```

#### 4️⃣ NEUTRAL PROFESSIONAL

```yaml
Materials:
  - Clean surfaces
  - Minimal texture
  - Matte finishes
  
Colors:
  Primary: Slate Gray (#64748B)
  Accent: Neutral Blue (#3B82F6)
  Background: White (#FFFFFF)
  
Lighting:
  - Even, soft
  - No drama
  - Clear visibility

Best For:
  - Enterprise
  - Government
  - Long-term daily use
  
Mood: Professional, focused, timeless
```

**CRITICAL RULE:** Theme does NOT change data. Theme changes perception.

---

### 🏠 SPHERE INTERIORS (Detailed Examples)

#### Personal Sphere 🏠

```
ENTRANCE HALL:
- Welcome message from Nova
- Today's priorities widget
- Active thread count
- Budget indicator

PERSONAL OFFICE:
- Writing desk (notes)
- Task board
- Calendar
- Personal threads

LIBRARY:
- All threads organized by topic
- Search within personal only
- Version history visible

WORKSPACE:
- Active document editor
- Agent staging area (when active)
- Version switcher

ARCHIVES:
- Old threads
- Completed tasks
- Decision history
```

#### Business Sphere 💼

```
ENTRANCE HALL:
- Company context reminder
- Active projects overview
- Team status (post-MVP)
- Budget dashboard

OPEN SPACE:
- Project boards
- Active workstreams
- Departmental threads

MEETING ROOM:
- Collaboration workspace
- Shared documents
- Decision records

ARCHIVES:
- Quarterly reports
- Past decisions
- Audit trail

WORKSPACE:
- Business documents
- Agent proposals
- Budget tracking
```

#### Government & Institutions 🏛️

```
ENTRANCE HALL:
- Formal reception
- Current matters
- Regulatory context

COUNCIL CHAMBER:
- Policy documents
- Legal threads
- Compliance records

ARCHIVES:
- Historical decisions
- Public records
- Audit logs (full)

WORKSPACE:
- Formal documents
- Multi-level approval chains
- Full governance visible
```

#### Community 👥

```
ENTRANCE HALL:
- Community dashboard
- Active discussions
- Event calendar

AGORA:
- Public threads
- Discussion spaces
- Community decisions

NOTICE BOARD:
- Announcements
- Shared resources
- Member directory

WORKSPACE:
- Collaborative documents
- Group projects
- Shared archives
```

---

### 🧩 INTERACTIVE OBJECTS (Standard Library)

In XR/Advanced UI, every entity is an object:

```yaml
Document Object:
  - Visual: Paper/File/Hologram
  - Actions: Open, Edit, Version, Share
  - States: Draft, Final, Archived
  
Thread Object:
  - Visual: Folder/Constellation/Stream
  - Actions: Open, Add, Search
  - States: Active, Paused, Archived
  
Decision Object:
  - Visual: Seal/Badge/Monument
  - Actions: View, Reference, Audit
  - States: Proposed, Approved, Enacted
  
Agent Object:
  - Visual: Avatar/Light/Presence
  - Actions: Assign, Monitor, Review
  - States: Idle, Working, Complete
  
Version Object:
  - Visual: Ghost/Echo/Branch
  - Actions: View, Compare, Restore
  - States: Current, Historical, Parallel
```

**Interaction Modes:**
- **2D UI:** Click, drag, drop
- **XR:** Grab, place, observe, walk around

---

### 🥽 XR PROJECTION (Without Breaking MVP)

#### MVP (2D Web)

```
- Traditional UI
- Light spatial metaphors
- Icons/badges for objects
- Hover states suggest depth
```

#### XR MODE (Post-MVP)

```
Same Logic:
  - Same data model
  - Same governance
  - Same approval flows
  
Different Rendering:
  - 3D spaces instead of panels
  - Spatial navigation
  - Object manipulation
  - Voice interaction
  
Technologies:
  - WebXR
  - Three.js / React Three Fiber
  - VR headsets (Quest, Vision Pro)
```

**Golden Rule:** XR is just another VIEW of the same OS.

---

### 🔒 SPHERES & XR GOLDEN RULE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  Spheres are governed places.                 ║
║  Themes are perceptual filters.               ║
║  XR is a projection, not a separate system.   ║
║                                               ║
║  Data → Sphere → Theme → Rendering            ║
║         ↓         ↓         ↓                 ║
║      Location  Style    2D or XR              ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

## 3️⃣ SPHERE → PLACE → COMPONENT MAPPING

### Personal Sphere (Complete Mapping)

```typescript
// Conceptual Structure
const PersonalSphere = {
  metadata: {
    id: 'personal',
    icon: '🏠',
    name: 'Personal',
    theme: 'natural'  // default, user can change
  },
  
  places: {
    entranceHall: {
      components: [
        'WelcomeMessage',
        'TodayWidget',
        'QuickStats',
        'NovaPresence'
      ],
      xrGeometry: 'entrance_hall_natural.glb'
    },
    
    office: {
      components: [
        'NotesBoard',
        'TaskList',
        'PersonalThreads',
        'Calendar'
      ],
      xrGeometry: 'office_natural.glb'
    },
    
    library: {
      components: [
        'ThreadList',
        'SearchBar (sphere-scoped)',
        'VersionHistory',
        'ArchiveExplorer'
      ],
      xrGeometry: 'library_natural.glb'
    },
    
    workspace: {
      components: [
        'UserWorkspaceEditor',
        'AgentStagingView (when active)',
        'VersionPanel',
        'ComparisonView (when active)'
      ],
      xrGeometry: 'workspace_natural.glb'
    },
    
    archives: {
      components: [
        'OldThreads',
        'CompletedTasks',
        'DecisionHistory',
        'AuditLog (personal only)'
      ],
      xrGeometry: 'archives_natural.glb'
    }
  },
  
  objects: {
    note: { type: 'Document', icon: '📝', xrModel: 'note.glb' },
    task: { type: 'Task', icon: '✓', xrModel: 'task.glb' },
    thread: { type: 'Thread', icon: '🧵', xrModel: 'thread.glb' }
  }
}
```

### Business Sphere (Complete Mapping)

```typescript
const BusinessSphere = {
  metadata: {
    id: 'business',
    icon: '💼',
    name: 'Business',
    theme: 'futuristic'  // default
  },
  
  places: {
    entranceHall: {
      components: [
        'CompanyContextBanner',
        'ActiveProjectsWidget',
        'BudgetDashboard',
        'TeamStatus'
      ],
      xrGeometry: 'entrance_hall_futuristic.glb'
    },
    
    openSpace: {
      components: [
        'ProjectBoards',
        'DepartmentalThreads',
        'ActiveWorkstreams',
        'CollaborationZones'
      ],
      xrGeometry: 'open_space_futuristic.glb'
    },
    
    meetingRoom: {
      components: [
        'CollaborativeWorkspace',
        'SharedDocuments',
        'DecisionRecords',
        'MeetingHistory'
      ],
      xrGeometry: 'meeting_room_futuristic.glb'
    },
    
    workspace: {
      components: [
        'BusinessDocumentEditor',
        'AgentProposalReview',
        'BudgetTracker',
        'ApprovalPipeline'
      ],
      xrGeometry: 'workspace_futuristic.glb'
    },
    
    archives: {
      components: [
        'QuarterlyReports',
        'PastDecisions',
        'FullAuditTrail',
        'ComplianceRecords'
      ],
      xrGeometry: 'archives_futuristic.glb'
    }
  },
  
  objects: {
    project: { type: 'Project', icon: '📊', xrModel: 'project.glb' },
    report: { type: 'Report', icon: '📈', xrModel: 'report.glb' },
    decision: { type: 'Decision', icon: '⚖️', xrModel: 'decision.glb' }
  }
}
```

---

## 4️⃣ IMPLEMENTATION PRIORITY

### Phase 1: MVP (2D, 2 Spheres)

```
Week 1-3: Core Architecture
- ✅ 3-workspace system
- ✅ Governance pipeline
- ✅ Version system
- ✅ Approval gates

Week 4-5: Basic UI
- □ Implement Personal + Business spheres
- □ Light spatial metaphors (entrance, office, workspace)
- □ Theme switcher (4 themes, CSS-based)
- □ Standard components

Week 6: Polish
- □ Smooth transitions
- □ Hover effects suggesting depth
- □ Icon system for objects
```

### Phase 2: 8 Spheres Activation

```
Week 7-10: Add Remaining 6 Spheres
- Government & Institutions
- Studio de création
- Community
- Social & Media
- Entertainment
- My Team

Each sphere gets:
- Same place structure (entrance, office, workspace, archives)
- Theme default (user can change)
- Appropriate object types
```

### Phase 3: XR Foundation

```
Week 11-14: WebXR Infrastructure
- Three.js scene setup
- Basic 3D navigation
- Object interaction (grab, place)
- Theme-to-3D-material mapping

Week 15-18: Full Sphere XR
- 3D models for each place type
- 4 theme variants per model
- VR headset support
- Hand tracking
```

---

## ✅ SHIP SEQUENCE (CANONICAL)

### 1️⃣ VALIDATION TECHNIQUE (GO / NO-GO)

**All tests MUST pass before proceeding:**

- [ ] Headers obligatoires présents sur 100% des endpoints
- [ ] Aucun write sans approval token
- [ ] Aucune écriture agent hors staging
- [ ] Versioning append-only vérifié
- [ ] Global search = read-only + scope visible
- [ ] Inter-sphere = références / copies explicites seulement
- [ ] Workspace: close sans save OK
- [ ] Workspace: save = nouvelle version
- [ ] Workspace: comparaison/diff OK
- [ ] Budget bloque réellement l'exécution
- [ ] Audit log complet (who/what/when/why)

**Decision:** Un seul FAIL = correctif avant suite.

---

### 2️⃣ QA FONCTIONNEL (Scénarios Clés)

**5 Key User Flows:**

1. Créer thread → workspace → agent → review → garder 2 versions
2. Global search profil → ouvrir cross-sphere (read-only) → switch context
3. Encodage en staging → refuser → rien n'est modifié
4. Budget dépassé → exécution bloquée avec message clair
5. Browser multi-compte → extraction manuelle → version créée

**Acceptance:** All scenarios complete successfully, user feedback positive.

---

### 3️⃣ FREEZE OFFICIEL V1

```bash
git tag -a v1.0.0-governed -m "CHE·NU V1 MVP"
git push origin v1.0.0-governed
```

**Frozen Documents:**
- MEMORY PROMPT
- CANONICAL CLARIFICATION
- GOVERNANCE REFINEMENT
- CANONICAL WORKSPACE MODEL
- UI COMPONENTS SPEC
- SPHERES AS PLACES SPEC

**Rule:** Interdiction d'ajout feature hors hotfix

---

### 4️⃣ DEMO / PITCH READY

**7-Minute Demo Script:**

```
Minute 1: The Problem
Minute 2: The Solution (show 3-hub layout, spheres as places)
Minute 3: Workspace Architecture (demo isolation)
Minute 4: Review & Decision (diff, 4 choices)
Minute 5: Governance Visible (approval, cost, budget)
Minute 6: Global Search (scoped, origin clear)
Minute 7: The Difference ("Autonomy in staging, authority with humans")
```

**Key Message:** "Spheres aren't menus. They're governed places where intelligence serves you."

---

### 5️⃣ SOFT LAUNCH

```
- Private access (invited users)
- Feedback collection (qualitative)
- No A/B testing
- No vanity metrics
- Focus: Trust, Clarity, Control
```

---

## 🎖️ WHAT YOU'VE ACHIEVED

✅ Un OS gouverné cohérent  
✅ Une IA puissante mais observable  
✅ Une UX calme et réversible  
✅ Un modèle enterprise-safe  
✅ Une base brevetable (governance architecture + spheres as places)  
✅ Une projection XR sans complexité additionnelle  

**Status:** ARCHITECTURE COMPLETE, READY TO BUILD 🚀

---

**🔥 INTEGRATION ROADMAP COMPLETE! NOW FINISHING FIGMA! 💪**
