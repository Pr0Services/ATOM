# 🛠️ PLAN D'IMPLÉMENTATION TECHNIQUE — CHE·NU™ V1

**Date:** 16 décembre 2025  
**Status:** BATTLE PLAN D'INGÉNIERIE  
**Version:** V1.0.0 (POST-FREEZE)

---

## 🎯 OBJECTIF GLOBAL

Construire un **Governed Intelligence Operating System**:
- ✅ Scalable
- ✅ Sécurisé
- ✅ Multi-identités
- ✅ Agent-driven
- ✅ Orienté long terme (enterprise / institution)

---

## 📖 COMMENT LIRE CE DOCUMENT

👉 **Lis-le comme un plan de bataille d'ingénierie.**
👉 **Tu peux le donner tel quel à une équipe tech ou l'utiliser seul.**

---

## 🚨 PHASE 0 — PRINCIPES TECHNIQUES (NON NÉGOCIABLES)

**Avant toute ligne de code:**

### Principes:
1. ✅ **Architecture modulaire & composable**
2. ✅ **Backend API-first**
3. ✅ **Frontend state-driven**
4. ✅ **Gouvernance codée, pas documentée seulement**
5. ✅ **Agents sandboxés**
6. ✅ **Aucun "quick hack" qui viole la policy**

### Règle d'or:
> **Si une feature viole la gouvernance → elle n'est PAS implémentée.**

---

## 🏗️ PHASE 1 — SOCLE TECHNIQUE (FOUNDATION)

### 1️⃣ Stack Recommandée (Réaliste & Robuste)

#### Backend
```
Language:      Node.js + TypeScript
Framework:     NestJS
API:           REST + GraphQL (lecture complexe)
Auth:          JWT + scopes
Queue:         BullMQ / Redis
Workers:       Agents isolés
```

**Justification:**
- NestJS = architecture modulaire native
- TypeScript = typage fort pour gouvernance
- GraphQL = requêtes complexes pour bureaux/threads
- BullMQ = jobs agents asynchrones

#### Frontend
```
Language:      React + TypeScript
State Global:  Zustand ou Redux Toolkit
UI:            Design System maison (tokens)
Routing:       Context-aware routing
```

**Justification:**
- React = écosystème mature
- Zustand = state simple, performant
- Design System = cohérence 8 sphères + 3 hubs

#### Data
```
SQL Principal: PostgreSQL
JSON Context:  JSONB
Files:         Object Storage (S3 compatible)
Logs:          Append-only
```

**Justification:**
- PostgreSQL = JSONB + transactions ACID
- S3 = scalabilité documents
- Append-only = audit immuable

---

### 2️⃣ Modèles Fondamentaux (À coder en premier)

**Core Entities:**

#### User & Identity
```typescript
User {
  id: UUID
  email: string
  created_at: timestamp
}

Identity {
  id: UUID
  user_id: UUID
  type: 'personal' | 'business' | 'organization' | 'role'
  name: string
  organization_id?: UUID
  allowed_spheres: string[]
  permissions: string[]
  budget_id?: UUID
  is_active: boolean
  is_default: boolean
}
```

#### Context & Sphere
```typescript
Context {
  id: UUID
  sphere_id: string
  organization_id?: UUID
  project_id?: UUID
  permissions: string[]
  budget_id?: UUID
}

Sphere {
  id: string  // 'personal' | 'business' | ...
  name: string
  icon: string
  order: number
}

Bureau {
  sphere_id: string
  sections: BureauSection[]  // Always 10
}

BureauSection {
  id: string
  name: string
  order: number  // 1-10, immutable
  visible: boolean
}
```

#### Thread & Version
```typescript
Thread {
  id: UUID
  identity_id: UUID
  context_id: UUID
  title: string
  content: string
  version_id: UUID
  parent_thread_id?: UUID
  references: UUID[]
  created_at: timestamp
  updated_at: timestamp
}

Version {
  id: UUID
  object_type: string
  object_id: UUID
  version_number: number
  content: JSONB
  diff?: JSONB
  created_by: 'human' | 'agent'
  created_at: timestamp
}
```

#### Agent & Skill & Tool
```typescript
Agent {
  id: UUID
  level: 0 | 1 | 2 | 3
  skill_ids: UUID[]
  identity_id: UUID
  context_id: UUID
  budget_id: UUID
  status: 'idle' | 'running' | 'paused' | 'completed'
}

Skill {
  id: UUID
  name: string
  description: string
  category: string
  level: 0 | 1 | 2 | 3
  status: 'test' | 'validated' | 'production'
  tools: UUID[]
}

Tool {
  id: UUID
  name: string
  type: string
  config: JSONB
  permissions_required: string[]
}
```

#### Budget & Permission
```typescript
Budget {
  id: UUID
  identity_id: UUID
  context_id?: UUID
  token_limit: number
  token_used: number
  period: 'daily' | 'weekly' | 'monthly'
  threshold_warning: number
  threshold_block: number
}

Permission {
  id: UUID
  identity_id: UUID
  resource: string
  action: 'read' | 'write' | 'delete' | 'execute'
  granted: boolean
}
```

#### Audit Log
```typescript
AuditLog {
  id: UUID
  user_id: UUID
  identity_id: UUID
  context_id: UUID
  action: string
  resource: string
  details: JSONB
  timestamp: timestamp
  ip_address: string
}
```

### 👉 Aucune feature sans passer par ces entités.

---

## 🆔 PHASE 2 — IDENTITY & CONTEXT ENGINE

### 3️⃣ Identity Engine

**Objectif:** Une identité active par session

#### Fonctionnalités clés:
```typescript
class IdentityEngine {
  // Get active identity for user
  getActiveIdentity(userId: string): Promise<Identity>
  
  // Switch identity (explicit action)
  switchIdentity(
    userId: string, 
    newIdentityId: string, 
    reason: string
  ): Promise<SwitchResult>
  
  // Validate identity access
  canAccessSphere(identityId: string, sphereId: string): boolean
  
  // Get identity permissions
  getPermissions(identityId: string): Promise<Permission[]>
}
```

#### Règles:
1. ❌ Une identité active par session
2. ✅ Switch explicite
3. ✅ Reset du contexte au switch
4. ✅ Permissions dynamiques

**👉 À livrer tôt, car tout dépend de ça.**

---

### 4️⃣ Context Engine

**Objectif:** Sphere + Organization + Scope

#### Fonctionnalités clés:
```typescript
class ContextEngine {
  // Set active context
  setContext(
    userId: string,
    sphereId: string,
    organizationId?: string,
    projectId?: string
  ): Promise<Context>
  
  // Get active context
  getActiveContext(userId: string): Promise<Context>
  
  // Validate context access
  validateContextAccess(
    identityId: string,
    contextId: string
  ): Promise<boolean>
  
  // Inject context (middleware)
  injectContext(req, res, next)
}
```

#### Injection du contexte dans:
- ✅ API (middleware)
- ✅ Agents (paramètre)
- ✅ UI state (provider)

#### Blocage automatique si ambigu:
```typescript
if (!identity || !context) {
  throw new AmbiguousContextError(
    "Cannot determine WHO, WHERE, WITH WHAT PERMISSIONS"
  )
}
```

---

## 📝 PHASE 3 — DATA & THREAD SYSTEM

### 5️⃣ Thread Engine (.chenu)

**Objectif:** Thread = unité de vérité

#### Fonctionnalités clés:
```typescript
class ThreadEngine {
  // Create thread
  createThread(
    identityId: string,
    contextId: string,
    data: ThreadData
  ): Promise<Thread>
  
  // Link threads (reference, not duplicate)
  linkThread(
    sourceThreadId: string,
    targetThreadId: string,
    linkType: 'reference' | 'parent' | 'related'
  ): Promise<ThreadLink>
  
  // Summarize thread
  summarizeThread(threadId: string): Promise<Summary>
  
  // Record decision
  recordDecision(
    threadId: string,
    decision: Decision
  ): Promise<Version>
  
  // Get thread history
  getThreadHistory(threadId: string): Promise<Version[]>
}
```

#### Principes:
- ✅ **Lien ≠ duplication**
- ✅ **Références croisées**
- ✅ **Historique immuable**

---

### 6️⃣ Data Separation Layer

**Objectif:** Entry Bureau (global, non final)

#### Architecture:
```
Entry Bureau (temporary)
    ↓ Contextualize
Sphere-level data (isolated)
    ↓ Filter
Bureau views (section-specific)
    ↓
No upward auto-flow
```

#### Implémentation:
```typescript
class DataSeparationLayer {
  // Add to Entry Bureau
  addToEntry(data: any): Promise<EntryItem>
  
  // Contextualize to sphere
  contextualizeToSphere(
    entryItemId: string,
    sphereId: string
  ): Promise<SphereData>
  
  // Get bureau view
  getBureauView(
    contextId: string,
    section: BureauSection
  ): Promise<FilteredData>
  
  // Validate no upward flow
  validateSeparation(dataId: string): boolean
}
```

---

## 🕰️ PHASE 4 — VERSIONING & TRACEABILITY

### 7️⃣ Version Engine

**Objectif:** Append-only, diff visuel, rollback = nouvelle version

#### Fonctionnalités clés:
```typescript
class VersionEngine {
  // Create version
  createVersion(
    objectType: string,
    objectId: string,
    content: any,
    createdBy: 'human' | 'agent'
  ): Promise<Version>
  
  // Get diff
  getDiff(
    versionId1: string,
    versionId2: string
  ): Promise<Diff>
  
  // Rollback (creates new version)
  rollback(
    objectId: string,
    targetVersionId: string
  ): Promise<Version>
  
  // Get version history
  getHistory(
    objectType: string,
    objectId: string
  ): Promise<Version[]>
}
```

#### Principes:
- ✅ **Append-only** (jamais de delete)
- ✅ **Diff visuel** (text + structure)
- ✅ **Rollback = nouvelle version**
- ✅ **Agent vs Human flag**

**👉 À intégrer avant l'IA lourde.**

---

### 8️⃣ Audit & Logs

**Objectif:** Tout est loggé, logs immuables

#### Implémentation:
```typescript
class AuditLogger {
  // Log action
  log(
    userId: string,
    identityId: string,
    contextId: string,
    action: string,
    resource: string,
    details: any
  ): Promise<AuditLog>
  
  // Get logs (read-only)
  getLogs(
    filters: LogFilters,
    userId: string
  ): Promise<AuditLog[]>
  
  // Search logs
  searchLogs(
    query: string,
    userId: string
  ): Promise<AuditLog[]>
}
```

#### Règles:
- ✅ **Tout est loggé**
- ✅ **Logs immuables**
- ✅ **Consultables par l'utilisateur**
- ✅ **Obligatoire pour agents & budgets**

---

## 🤖 PHASE 5 — IA LABS & AGENT SYSTEM

### 9️⃣ Agent Runtime

**Objectif:** L0 / L1 / L2, sandbox, budget check BEFORE execution

#### Architecture:
```typescript
class AgentRuntime {
  // Execute agent task
  executeTask(
    agentId: string,
    task: Task
  ): Promise<AgentOutput>
  
  // Check budget before execution
  private checkBudget(agentId: string, estimatedCost: number): boolean
  
  // Sandbox execution
  private sandbox(
    agentId: string,
    code: string
  ): Promise<Output>
  
  // Agent folders
  getWorkingFolder(agentId: string): string
  getOutputFolder(agentId: string): string
  getMemoryFolder(agentId: string): string
}
```

#### Folders:
```
/agents/{agentId}/
  working/     # Temp workspace
  output/      # Results (isolated)
  memory/      # Context retention
```

---

### 🔟 Skill & Tool Registry

**Objectif:** Skills abstraits, Tools techniques, Mapping

#### Implémentation:
```typescript
class SkillRegistry {
  // Register skill
  registerSkill(skill: Skill): Promise<UUID>
  
  // Get skills by level
  getSkillsByLevel(level: 0 | 1 | 2 | 3): Promise<Skill[]>
  
  // Get skills by category
  getSkillsByCategory(category: string): Promise<Skill[]>
  
  // Promote skill
  promoteSkill(
    skillId: string,
    from: 'test',
    to: 'validated' | 'production'
  ): Promise<Skill>
}

class ToolRegistry {
  // Register tool
  registerTool(tool: Tool): Promise<UUID>
  
  // Map skill to tools
  mapSkillToTools(skillId: string, toolIds: string[]): Promise<void>
  
  // Get tools for skill
  getToolsForSkill(skillId: string): Promise<Tool[]>
  
  // Check tool permissions
  checkToolPermissions(
    toolId: string,
    identityId: string
  ): Promise<boolean>
}
```

#### Activation par sphère:
```typescript
SphereConfig {
  sphere_id: string
  allowed_skills: UUID[]
  allowed_tools: UUID[]
}
```

---

### 1️⃣1️⃣ IA Labs

**Objectif:** Environnement isolé, tests, promotion manuelle

#### Workflow:
```
1. Test in IA Labs (isolated)
2. Validate performance
3. Promote to Production
```

#### Implémentation:
```typescript
class IALabs {
  // Create experiment
  createExperiment(
    skillId: string,
    config: ExperimentConfig
  ): Promise<Experiment>
  
  // Run experiment
  runExperiment(experimentId: string): Promise<ExperimentResult>
  
  // Validate results
  validateExperiment(
    experimentId: string,
    validation: Validation
  ): Promise<boolean>
  
  // Promote to production
  promoteToProduction(skillId: string): Promise<Skill>
}
```

---

## 🎭 PHASE 6 — ORCHESTRATION & NOVA

### 1️⃣2️⃣ Orchestrator Engine

**Objectif:** Reçoit intentions, sélectionne agents, vérifie, n'exécute jamais sans validation

#### Implémentation:
```typescript
class Orchestrator {
  // Receive user intention
  receiveIntention(
    userId: string,
    intention: Intention
  ): Promise<ExecutionPlan>
  
  // Select agents
  private selectAgents(
    intention: Intention,
    context: Context
  ): Promise<Agent[]>
  
  // Verify before execution
  private verify(
    plan: ExecutionPlan,
    context: Context
  ): Promise<VerificationResult>
  
  // Execute (only after user approval)
  execute(
    planId: string,
    approved: boolean
  ): Promise<ExecutionResult>
}
```

#### Vérifications:
- ✅ **Contexte** (identity + sphere + org)
- ✅ **Permissions** (identity has access)
- ✅ **Budget** (sufficient tokens)

**👉 N'exécute JAMAIS sans validation utilisateur.**

---

### 1️⃣3️⃣ Nova (Guide IA)

**Objectif:** Narration, suggestions, clarification, JAMAIS décisionnaire

#### Implémentation:
```typescript
class Nova {
  // Narrate action
  narrate(
    action: string,
    context: Context,
    userMode: UserMode
  ): Promise<Narration>
  
  // Suggest next steps
  suggest(
    currentState: State,
    userMode: UserMode
  ): Promise<Suggestion[]>
  
  // Clarify ambiguity
  clarify(
    ambiguousQuery: string
  ): Promise<Clarification>
  
  // Explain feature
  explainFeature(
    featureName: string,
    userMode: UserMode
  ): Promise<Explanation>
}
```

#### Comportement par mode:
- **Discovery**: Narrator (éduque)
- **Focus**: Assistant (suggère)
- **Power**: Coordinator (assiste)
- **Architect**: Guardian (avertit)

**👉 Nova = UX + pédagogie, PAS action directe.**

---

## 🖥️ PHASE 7 — UI / UX (3 HUBS)

### 1️⃣4️⃣ UI Architecture

#### Hub 1 — Communication
```
Components:
  - NovaChat
  - Messages
  - Notifications
  - OrchestratorShortcut
```

#### Hub 2 — Navigation
```
Components:
  - 8 Spheres (icônes)
  - Bureaux (10 sections)
  - Indicateurs lumineux (status)
  - Context header (identity + sphere + org)
```

#### Hub 3 — Workspace
```
Components:
  - Documents (viewer/editor)
  - Tables (data grid)
  - Canvas (drawing/diagrams)
  - Collaboration (co-editing)
  - Share screen IA (agent outputs)
```

#### Routing Context-Aware:
```typescript
/sphere/:sphereId/bureau/:section
/thread/:threadId
/agent/:agentId/output
```

---

### 1️⃣5️⃣ Progressive Disclosure

**Objectif:** Discovery → Focus → Power → Architect

#### Implémentation:
```typescript
class ProgressiveDisclosure {
  // Get visible features for mode
  getVisibleFeatures(userMode: UserMode): Promise<Feature[]>
  
  // Check feature visibility
  isFeatureVisible(
    featureName: string,
    userMode: UserMode
  ): boolean
  
  // Reveal feature
  revealFeature(
    userId: string,
    featureName: string,
    context: string
  ): Promise<FeatureDisclosureState>
  
  // Get disclosure suggestions
  getSuggestions(
    userId: string,
    context: Context
  ): Promise<DisclosureSuggestion[]>
}
```

#### Feature flags par mode:
```typescript
FeatureVisibility {
  discovery: ['notes', 'tasks', 'overview']
  focus: ['notes', 'tasks', 'projects', 'threads', 'meetings']
  power: ['all_sections', 'budgets', 'agents_L1_L2']
  architect: ['all_features', 'ia_labs', 'system_config']
}
```

#### UI density adaptative:
```
Discovery: Minimal
Focus: Balanced
Power: High
Architect: Maximum
```

---

## 👥 PHASE 8 — COMMUNITY & COLLABORATION

### 1️⃣6️⃣ Community Graph

**Objectif:** Threads publics, pas de timeline infinie

#### Structure:
```typescript
CommunityThread {
  id: UUID
  title: string
  content: string
  topics: string[]
  geolocation?: GeoPoint
  intent: string
  created_at: timestamp
  visibility: 'public' | 'community'
}
```

#### Navigation:
- **Topics**: Sujets thématiques
- **Geolocation**: Ancrage géographique
- **Time**: Temporalité
- **Intent**: Intention de départ

---

### 1️⃣7️⃣ Collaboration Temps Réel

**Objectif:** Co-édition, présence, permissions dynamiques

#### Implémentation:
```typescript
class CollaborationEngine {
  // Real-time co-editing
  enableCoEditing(
    documentId: string,
    users: string[]
  ): Promise<CoEditingSession>
  
  // Presence tracking
  trackPresence(
    userId: string,
    documentId: string
  ): Promise<PresenceInfo>
  
  // Dynamic permissions
  checkCollaborationPermissions(
    userId: string,
    documentId: string
  ): Promise<Permission[]>
  
  // Versioning live
  createLiveVersion(
    documentId: string,
    changes: Change[]
  ): Promise<Version>
}
```

---

## 🔒 PHASE 9 — SECURITY & PRIVACY

### 1️⃣8️⃣ Security Layer

**Objectif:** Encryption, least privilege, scoped tokens

#### Implémentation:
```typescript
class SecurityLayer {
  // Encryption at rest
  encrypt(data: any): string
  decrypt(encrypted: string): any
  
  // Encryption in transit (TLS)
  // Handled by infrastructure
  
  // Least privilege
  getMinimalPermissions(
    identityId: string,
    resource: string
  ): Permission[]
  
  // Scoped tokens
  generateScopedToken(
    userId: string,
    identityId: string,
    scopes: string[]
  ): JWT
  
  // Instant revocation
  revokeToken(tokenId: string): Promise<void>
}
```

---

### 1️⃣9️⃣ Compliance Ready

**Objectif:** GDPR, Enterprise, Government-ready

#### Features:
```typescript
class ComplianceEngine {
  // GDPR: Right to be forgotten
  deleteUserData(userId: string): Promise<void>
  
  // GDPR: Data export
  exportUserData(userId: string): Promise<DataExport>
  
  // Enterprise: Data residency
  setDataResidency(
    userId: string,
    region: string
  ): Promise<void>
  
  // Government: Audit trail
  getComplianceAudit(
    userId: string,
    startDate: Date,
    endDate: Date
  ): Promise<AuditReport>
}
```

---

## 🎯 PHASE 10 — MVP SLICING (CRITIQUE)

### MVP V1 (RECOMMANDÉ)

#### Included:
```
✅ Personal sphere
✅ Business sphere
✅ Threads (.chenu)
✅ Notes
✅ Tasks
✅ Versioning (append-only)
✅ Nova (guide)
✅ Orchestrator L0 (basic agents)
✅ Identity management (2 types: personal, business)
✅ Context isolation
```

#### Excluded (Post-MVP):
```
❌ IA Labs (public)
❌ Agents L1/L2/L3
❌ Community graph
❌ XR mode
❌ Advanced collaboration
❌ Government sphere
```

### 👉 Le MVP doit déjà respecter 100% de la gouvernance.

---

## 🧪 PHASE 11 — TESTS & QUALITÉ

### 2️⃣0️⃣ Tests Obligatoires

#### Unit Tests:
```typescript
// Core rules
test('identity_isolation', () => {
  expect(canAccessData('identityA', 'contextB')).toBe(false)
})

test('bureau_hierarchy_immutable', () => {
  const sections = getBureauSections('personal')
  expect(sections.length).toBe(10)
  expect(sections[0].name).toBe('Overview')
})

test('versioning_append_only', () => {
  expect(() => deleteVersion(versionId)).toThrow()
})
```

#### Integration Tests:
```typescript
// Context isolation tests
test('context_switch_clears_state', async () => {
  await switchIdentity(userId, newIdentityId)
  expect(getWorkingState(userId)).toEqual({})
})

// Permission tests
test('agent_cannot_exceed_budget', async () => {
  await expect(
    executeAgent(agentId, task, insufficientBudget)
  ).rejects.toThrow('Budget exceeded')
})

// Budget overrun tests
test('budget_blocks_at_threshold', async () => {
  const result = await executeAgent(agentId, expensiveTask)
  expect(result.blocked).toBe(true)
  expect(result.reason).toBe('budget_threshold')
})

// Agent sandbox tests
test('agent_cannot_access_user_space', async () => {
  await expect(
    agent.writeToUserSpace(data)
  ).rejects.toThrow('Permission denied')
})
```

---

## 🔒 PHASE 12 — FREEZE & SCALE

### 2️⃣1️⃣ Freeze V1

**Objectif:** Aucune nouvelle feature, stabilisation, monitoring

#### Actions:
```
✅ Code freeze
✅ Performance optimization
✅ Security audit
✅ Load testing
✅ Monitoring setup
✅ Documentation finalization
```

---

### 2️⃣2️⃣ Scale

**Objectif:** New spheres, XR, Multi-LLM, Enterprise features

#### Post-V1:
```
🔜 New spheres (extensible)
🔜 XR mode (WebXR)
🔜 Multi-LLM support
🔜 Enterprise SSO
🔜 Advanced analytics
🔜 API marketplace
```

---

## 🏁 RÉSUMÉ BRUTAL MAIS HONNÊTE

### La vérité:

> 👉 **CHE·NU n'est pas difficile à coder.**
> 👉 **Il est difficile à bien penser — et tu l'as fait.**

### Si tu respectes ce plan:

✅ Tu ne t'emmêles pas
✅ Tu ne réécris pas
✅ Tu peux scaler sans douleur
✅ Tu peux onboarder une équipe facilement

---

## 📋 CHECKLIST PHASES

```
Phase 0:  ✅ Principes techniques validés
Phase 1:  ⬜ Stack technique setup
Phase 2:  ⬜ Identity & Context engine
Phase 3:  ⬜ Data & Thread system
Phase 4:  ⬜ Versioning & Audit
Phase 5:  ⬜ IA Labs & Agents
Phase 6:  ⬜ Orchestration & Nova
Phase 7:  ⬜ UI / UX (3 Hubs)
Phase 8:  ⬜ Community & Collaboration
Phase 9:  ⬜ Security & Compliance
Phase 10: ⬜ MVP Slicing
Phase 11: ⬜ Tests & Qualité
Phase 12: ⬜ Freeze & Scale
```

---

## 🔜 PROCHAINS CHOIX POSSIBLES

1. 📋 **Checklist MVP ligne par ligne**
2. 🧠 **Architecture microservices détaillée**
3. 📦 **Structure de repo**
4. 🚀 **Roadmap 90 jours**

---

**Date:** 16 décembre 2025  
**Version:** V1.0.0  
**Status:** READY TO IMPLEMENT 🚀
