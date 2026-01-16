# CHE·NU V1 — ULTRA-ACTIONABLE IMPLEMENTATION CHECKLIST
## 21-Day Sprint to Production (Day-by-Day Tasks)

**Version:** V1 MVP PRODUCTION  
**Date:** 16 décembre 2025  
**Timeline:** 21 Days  
**Target:** Launch-Ready Governed OS

---

## 🎯 MISSION

Transform canonical documentation into **working production system** in 21 days.

**Daily commitment:** 4-6 hours focused work  
**Result:** Functional CHE·NU MVP with Personal + Business spheres

---

## 📅 WEEK 1: FOUNDATION (Days 1-7)

### DAY 1 — Database Schema & Context System

**Duration:** 4-6 hours  
**Status:** [ ] Not Started

#### Morning (2-3 hours)

```sql
-- Task 1.1: Create database schema
-- File: backend/database/schema.sql

-- Identities
CREATE TABLE identities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  type VARCHAR(20) NOT NULL CHECK (type IN ('personal', 'business')),
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Spheres
CREATE TABLE spheres (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identity_id UUID NOT NULL REFERENCES identities(id),
  type VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  icon VARCHAR(10),
  theme VARCHAR(20) DEFAULT 'natural',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Contexts (sessions)
CREATE TABLE contexts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  identity_id UUID NOT NULL REFERENCES identities(id),
  sphere_id UUID NOT NULL REFERENCES spheres(id),
  mode VARCHAR(20) DEFAULT 'beginner',
  locked BOOLEAN DEFAULT FALSE,
  lock_reason TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Threads (immutable)
CREATE TABLE threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identity_id UUID NOT NULL REFERENCES identities(id),
  sphere_id UUID NOT NULL REFERENCES spheres(id),
  title VARCHAR(255) NOT NULL,
  status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW()
);
-- No updated_at - append only!

-- Thread entries (immutable)
CREATE TABLE thread_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID NOT NULL REFERENCES threads(id),
  type VARCHAR(20) NOT NULL CHECK (type IN ('note', 'decision', 'reference')),
  content JSONB NOT NULL,
  author VARCHAR(20) NOT NULL CHECK (author IN ('user', 'agent')),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Versions (immutable)
CREATE TABLE versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_id UUID NOT NULL,
  sphere_id UUID NOT NULL REFERENCES spheres(id),
  version_number INT NOT NULL,
  content JSONB NOT NULL,
  author VARCHAR(20) NOT NULL CHECK (author IN ('user', 'agent')),
  approved_by UUID REFERENCES users(id),
  reasoning TEXT,
  restored_from UUID REFERENCES versions(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Revoke UPDATE/DELETE on immutable tables
REVOKE UPDATE, DELETE ON threads FROM ALL;
REVOKE UPDATE, DELETE ON thread_entries FROM ALL;
REVOKE UPDATE, DELETE ON versions FROM ALL;
```

**Checkpoint:** Database schema created ✓

#### Afternoon (2-3 hours)

```typescript
// Task 1.2: Context Service
// File: backend/services/contextService.ts

export class ContextService {
  async create(params: CreateContextParams): Promise<Context> {
    const context = await db.contexts.insert({
      userId: params.userId,
      identityId: params.identityId,
      sphereId: params.sphereId,
      mode: params.mode || 'beginner'
    })
    
    return context
  }
  
  async get(contextId: string): Promise<Context | null> {
    return await db.contexts.findOne({ id: contextId })
  }
  
  async validate(contextId: string, userId: string): Promise<ValidationResult> {
    const context = await this.get(contextId)
    
    if (!context) {
      return { valid: false, reason: 'Context not found' }
    }
    
    if (context.userId !== userId) {
      return { valid: false, reason: 'Context does not belong to user' }
    }
    
    if (context.locked) {
      return { valid: false, reason: context.lockReason || 'Context locked' }
    }
    
    return { valid: true }
  }
  
  async switchSphere(contextId: string, newSphereId: string): Promise<Context> {
    // Create new context (contexts are immutable after creation)
    const oldContext = await this.get(contextId)
    
    const newContext = await this.create({
      userId: oldContext.userId,
      identityId: oldContext.identityId,
      sphereId: newSphereId,
      mode: oldContext.mode
    })
    
    // Lock old context
    await db.contexts.update({ id: contextId }, {
      locked: true,
      lockReason: 'Sphere switched'
    })
    
    return newContext
  }
}
```

**Checkpoint:** Context service working ✓

#### Test

```bash
npm test -- contextService.test.ts
# All tests passing
```

---

### DAY 2 — Workspace Tables & Service

**Duration:** 4-6 hours  
**Status:** [ ] Not Started

#### Morning (2-3 hours)

```sql
-- Task 2.1: Workspace tables
-- File: backend/database/workspaces.sql

-- User workspaces
CREATE TABLE user_workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  sphere_id UUID NOT NULL REFERENCES spheres(id),
  content_id UUID,  -- Optional: reference to thread, document, etc
  content JSONB NOT NULL,
  state VARCHAR(20) DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Agent staging workspaces (separate table!)
CREATE TABLE agent_staging_workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_workspace_id UUID REFERENCES user_workspaces(id),
  execution_id UUID NOT NULL,
  agent_id VARCHAR(100) NOT NULL,
  content JSONB NOT NULL,
  status VARCHAR(20) DEFAULT 'in_progress',
  reasoning TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Comparison sessions
CREATE TABLE comparison_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  user_version_id UUID REFERENCES versions(id),
  agent_draft_id UUID REFERENCES agent_staging_workspaces(id),
  diff JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Checkpoint:** Workspace tables created ✓

#### Afternoon (2-3 hours)

```typescript
// Task 2.2: Workspace Service
// File: backend/services/workspaceService.ts

export class WorkspaceService {
  // User workspace methods
  async createUserWorkspace(params: CreateWorkspaceParams): Promise<UserWorkspace> {
    return await db.userWorkspaces.insert({
      userId: params.userId,
      sphereId: params.sphereId,
      contentId: params.contentId,
      content: params.content || {},
      state: 'draft'
    })
  }
  
  async updateUserWorkspace(id: string, content: any): Promise<void> {
    // Only UPDATE allowed (for draft state)
    await db.userWorkspaces.update({ id }, { 
      content,
      updated_at: new Date()
    })
  }
  
  async saveUserWorkspaceAsVersion(workspaceId: string): Promise<Version> {
    const workspace = await db.userWorkspaces.findOne({ id: workspaceId })
    
    // Create NEW version (immutable)
    const version = await versionService.create({
      contentId: workspace.contentId,
      sphereId: workspace.sphereId,
      content: workspace.content,
      author: 'user'
    })
    
    return version
  }
  
  async closeUserWorkspace(id: string, save: boolean): Promise<void> {
    if (save) {
      await this.saveUserWorkspaceAsVersion(id)
    }
    
    // Delete workspace (drafts are ephemeral)
    await db.userWorkspaces.delete({ id })
  }
  
  // Agent staging methods
  async createAgentStaging(params: CreateAgentStagingParams): Promise<AgentStaging> {
    return await db.agentStagingWorkspaces.insert({
      userWorkspaceId: params.userWorkspaceId,
      executionId: params.executionId,
      agentId: params.agentId,
      content: params.content,
      status: 'in_progress',
      reasoning: params.reasoning
    })
  }
  
  async getAgentStaging(executionId: string): Promise<AgentStaging | null> {
    return await db.agentStagingWorkspaces.findOne({ executionId })
  }
  
  async completeAgentStaging(executionId: string, content: any, reasoning: string): Promise<void> {
    await db.agentStagingWorkspaces.update({ executionId }, {
      content,
      reasoning,
      status: 'complete',
      updated_at: new Date()
    })
  }
  
  // Comparison methods
  async createComparison(params: CreateComparisonParams): Promise<ComparisonSession> {
    const userVersion = await versionService.get(params.userVersionId)
    const agentDraft = await this.getAgentStaging(params.agentDraftId)
    
    const diff = computeDiff(userVersion.content, agentDraft.content)
    
    return await db.comparisonSessions.insert({
      userId: params.userId,
      userVersionId: params.userVersionId,
      agentDraftId: params.agentDraftId,
      diff
    })
  }
}
```

**Checkpoint:** Workspace service working ✓

---

### DAY 3 — Governance Middleware Stack

**Duration:** 5-6 hours  
**Status:** [ ] Not Started

#### Morning (3 hours)

```typescript
// Task 3.1: Core middleware stack
// File: backend/middleware/index.ts

// M0: Trace
export function traceMiddleware(req, res, next) {
  if (!req.headers['x-trace-id']) {
    req.headers['x-trace-id'] = generateUUID()
  }
  
  logger.setContext({ traceId: req.headers['x-trace-id'] })
  next()
}

// M1: Auth
export async function authMiddleware(req, res, next) {
  try {
    const token = extractToken(req)
    const session = await validateSession(token)
    
    if (!session.valid) {
      return res.status(401).json({
        error: '401_UNAUTHORIZED',
        message: 'Invalid session'
      })
    }
    
    req.userId = session.userId
    req.roles = session.roles
    next()
  } catch (error) {
    return res.status(401).json({
      error: '401_UNAUTHORIZED',
      message: 'Authentication failed'
    })
  }
}

// M2: Identity
export async function identityMiddleware(req, res, next) {
  const identityId = req.headers['x-identity-id']
  
  if (!identityId) {
    return res.status(400).json({
      error: '400_CONTEXT_REQUIRED',
      message: 'X-Identity-Id required'
    })
  }
  
  const identity = await identityService.get(identityId)
  
  if (!identity || identity.userId !== req.userId) {
    return res.status(403).json({
      error: '403_IDENTITY_FORBIDDEN'
    })
  }
  
  req.identity = identity
  next()
}

// M3: Context
export async function contextMiddleware(req, res, next) {
  const contextId = req.headers['x-context-id']
  
  if (!contextId) {
    return res.status(400).json({
      error: '400_CONTEXT_REQUIRED',
      message: 'X-Context-Id required'
    })
  }
  
  const validation = await contextService.validate(contextId, req.userId)
  
  if (!validation.valid) {
    return res.status(409).json({
      error: '409_CONTEXT_STALE',
      message: validation.reason
    })
  }
  
  req.context = await contextService.get(contextId)
  next()
}

// M4: Sphere Scope
export async function sphereScopeMiddleware(req, res, next) {
  const sphereId = req.headers['x-sphere-id']
  
  if (!sphereId) {
    return res.status(400).json({
      error: '400_CONTEXT_REQUIRED',
      message: 'X-Sphere-Id required'
    })
  }
  
  const sphere = await sphereService.get(sphereId)
  
  if (!sphere || sphere.identityId !== req.identity.id) {
    return res.status(403).json({
      error: '403_SPHERE_FORBIDDEN'
    })
  }
  
  req.sphere = sphere
  next()
}

// M5: Budget
export async function budgetMiddleware(req, res, next) {
  const intent = req.headers['x-request-intent']
  const costEstimate = await estimateCost(intent, req.body)
  
  if (costEstimate > 0) {
    const budget = await budgetService.get(req.userId)
    
    if (budget.remaining < costEstimate) {
      return res.status(402).json({
        error: '402_BUDGET_EXCEEDED',
        required: costEstimate,
        available: budget.remaining
      })
    }
    
    req.budgetReservation = await budgetService.reserve(
      req.userId,
      costEstimate
    )
  }
  
  next()
}
```

**Checkpoint:** First 5 middlewares implemented ✓

#### Afternoon (2-3 hours)

```typescript
// Task 3.2: Policy & Audit middleware
// File: backend/middleware/policyMiddleware.ts

export async function policyMiddleware(req, res, next) {
  const policy = await evaluatePolicy({
    userId: req.userId,
    identity: req.identity,
    sphere: req.sphere,
    context: req.context,
    action: extractAction(req),
    resource: extractResource(req)
  })
  
  switch (policy.decision) {
    case 'ALLOW':
      req.policyDecision = policy
      next()
      break
      
    case 'ALLOW_READ_ONLY':
      req.policyDecision = policy
      req.readOnly = true
      next()
      break
      
    case 'REQUIRE_APPROVAL':
      return res.status(409).json({
        error: '409_APPROVAL_REQUIRED',
        approvalDetails: policy.approvalDetails
      })
      
    case 'DENY':
      return res.status(403).json({
        error: policy.errorCode || '403_FORBIDDEN',
        message: policy.reason
      })
  }
}

// M7: Audit
export function auditMiddleware(req, res, next) {
  const startTime = Date.now()
  
  const originalSend = res.send
  res.send = function(data) {
    // Log audit entry (append-only)
    auditLog.create({
      traceId: req.headers['x-trace-id'],
      timestamp: new Date(),
      userId: req.userId,
      identityId: req.identity?.id,
      sphereId: req.sphere?.id,
      contextId: req.context?.id,
      action: extractAction(req),
      outcome: res.statusCode < 400 ? 'allowed' : 'denied',
      duration: Date.now() - startTime
    })
    
    originalSend.call(this, data)
  }
  
  next()
}
```

**Checkpoint:** All 7 middlewares complete ✓

#### Test

```bash
npm test -- middleware.test.ts
# Test all middleware rules
```

---

### DAY 4 — Policy Engine & Rules

**Duration:** 5-6 hours  
**Status:** [ ] Not Started

#### All Day (5-6 hours)

```typescript
// Task 4.1: Policy Engine
// File: backend/services/policyEngine.ts

export class PolicyEngine {
  async evaluate(context: RequestContext): Promise<PolicyDecision> {
    // Rule R1: Cross-sphere writes forbidden
    if (context.sphereRelation === 'cross_sphere' && context.action === 'write') {
      return {
        decision: 'DENY',
        errorCode: '403_SCOPE_VIOLATION',
        reason: 'Cannot write to external sphere',
        rule: 'R1'
      }
    }
    
    // Rule R2: Cross-sphere reads allow (read-only)
    if (context.sphereRelation === 'cross_sphere' && context.action === 'read') {
      return {
        decision: 'ALLOW_READ_ONLY',
        metadata: {
          readOnly: true,
          originSphere: context.targetSphere,
          explanation: 'From external sphere'
        },
        mustAudit: true,
        rule: 'R2'
      }
    }
    
    // Rule R3: Decisions immutable
    if (context.resource === 'decision' && ['write', 'update', 'delete'].includes(context.action)) {
      return {
        decision: 'DENY',
        errorCode: '403_DECISION_IMMUTABLE',
        reason: 'Decisions cannot be modified',
        rule: 'R3'
      }
    }
    
    // Rule R4: Workspace saves create new versions
    if (context.resource === 'workspace' && context.action === 'write') {
      if (context.operation !== 'save_new_version') {
        return {
          decision: 'DENY',
          errorCode: '403_OVERWRITE_FORBIDDEN',
          reason: 'Must create new version',
          rule: 'R4'
        }
      }
    }
    
    // Rule R5: Agents never write to production
    if (context.zone !== 'staging' && context.client === 'agent' && context.action === 'write') {
      return {
        decision: 'DENY',
        errorCode: '403_AGENT_WRITE_FORBIDDEN',
        reason: 'Agents write to staging only',
        rule: 'R5'
      }
    }
    
    // Rule R6: Staging integration requires review
    if (context.zone === 'staging' && context.target === 'production') {
      return {
        decision: 'DENY',
        errorCode: '409_INTEGRATION_REQUIRES_REVIEW',
        reason: 'Must review before integration',
        rule: 'R6'
      }
    }
    
    // Rule R7: Execution requires approval
    if (context.action === 'execute') {
      if (!context.approvalToken) {
        return {
          decision: 'REQUIRE_APPROVAL',
          errorCode: '409_APPROVAL_REQUIRED',
          rule: 'R7'
        }
      }
      
      const valid = await validateApprovalToken(context.approvalToken, context)
      if (!valid.isValid) {
        return {
          decision: 'DENY',
          errorCode: '403_APPROVAL_INVALID',
          reason: valid.reason,
          rule: 'R7'
        }
      }
    }
    
    // Default allow
    return {
      decision: 'ALLOW',
      rule: 'DEFAULT'
    }
  }
}
```

**Checkpoint:** Policy engine with all 10 rules ✓

#### Test

```bash
npm test -- policyEngine.test.ts
# Test each rule individually
# Test cross-sphere writes blocked
# Test agent production writes blocked
# Test approval requirement
```

---

### DAY 5 — Version System & API Endpoints

**Duration:** 5-6 hours  
**Status:** [ ] Not Started

#### Morning (2-3 hours)

```typescript
// Task 5.1: Version Service
// File: backend/services/versionService.ts

export class VersionService {
  async create(params: CreateVersionParams): Promise<Version> {
    // Get next version number
    const latestVersion = await db.versions
      .findOne({ contentId: params.contentId })
      .orderBy('version_number', 'desc')
    
    const versionNumber = (latestVersion?.versionNumber || 0) + 1
    
    // Insert NEW version (append-only)
    return await db.versions.insert({
      contentId: params.contentId,
      sphereId: params.sphereId,
      versionNumber,
      content: params.content,
      author: params.author,
      approvedBy: params.approvedBy,
      reasoning: params.reasoning,
      restoredFrom: params.restoredFrom
    })
  }
  
  async get(versionId: string): Promise<Version | null> {
    return await db.versions.findOne({ id: versionId })
  }
  
  async list(contentId: string): Promise<Version[]> {
    return await db.versions
      .find({ contentId })
      .orderBy('version_number', 'desc')
  }
  
  async compare(fromId: string, toId: string): Promise<Diff> {
    const fromVersion = await this.get(fromId)
    const toVersion = await this.get(toId)
    
    return computeDiff(fromVersion.content, toVersion.content)
  }
  
  // NO update() method
  // NO delete() method
}
```

**Checkpoint:** Version service complete ✓

#### Afternoon (3 hours)

```typescript
// Task 5.2: Core API Endpoints
// File: backend/routes/index.ts

// Apply middleware stack
app.use(traceMiddleware)
app.use(authMiddleware)
app.use(identityMiddleware)
app.use(contextMiddleware)
app.use(sphereScopeMiddleware)
app.use(budgetMiddleware)
app.use(policyMiddleware)
app.use(auditMiddleware)

// Workspace endpoints
app.post('/api/workspaces', async (req, res) => {
  const workspace = await workspaceService.createUserWorkspace({
    userId: req.userId,
    sphereId: req.sphere.id,
    contentId: req.body.contentId,
    content: req.body.content
  })
  
  res.json(workspace)
})

app.put('/api/workspaces/:id', async (req, res) => {
  await workspaceService.updateUserWorkspace(
    req.params.id,
    req.body.content
  )
  
  res.json({ success: true })
})

app.post('/api/workspaces/:id/save', async (req, res) => {
  const version = await workspaceService.saveUserWorkspaceAsVersion(req.params.id)
  
  res.json({ version })
})

app.delete('/api/workspaces/:id', async (req, res) => {
  await workspaceService.closeUserWorkspace(
    req.params.id,
    req.query.save === 'true'
  )
  
  res.json({ success: true })
})

// Version endpoints
app.get('/api/versions/:contentId', async (req, res) => {
  const versions = await versionService.list(req.params.contentId)
  
  res.json({ versions })
})

app.get('/api/versions/:id/compare/:otherId', async (req, res) => {
  const diff = await versionService.compare(
    req.params.id,
    req.params.otherId
  )
  
  res.json({ diff })
})

// Agent staging endpoints
app.post('/api/agent/staging', async (req, res) => {
  const staging = await workspaceService.createAgentStaging({
    userWorkspaceId: req.body.userWorkspaceId,
    executionId: req.body.executionId,
    agentId: req.body.agentId,
    content: req.body.content
  })
  
  res.json(staging)
})

app.get('/api/agent/staging/:executionId', async (req, res) => {
  const staging = await workspaceService.getAgentStaging(req.params.executionId)
  
  res.json(staging)
})

// Comparison endpoints
app.post('/api/comparisons', async (req, res) => {
  const comparison = await workspaceService.createComparison({
    userId: req.userId,
    userVersionId: req.body.userVersionId,
    agentDraftId: req.body.agentDraftId
  })
  
  res.json(comparison)
})
```

**Checkpoint:** Core API endpoints working ✓

---

### DAY 6-7 — Frontend Foundation

**Duration:** 2 days (8-12 hours total)  
**Status:** [ ] Not Started

#### DAY 6 Morning

```typescript
// Task 6.1: Context Provider
// File: frontend/contexts/AppContext.tsx

export const AppContext = createContext<AppState>(null)

export function AppProvider({ children }) {
  const [session, setSession] = useState<SessionState>('booting')
  const [identity, setIdentity] = useState<Identity>(null)
  const [sphere, setSphere] = useState<Sphere>(null)
  const [context, setContext] = useState<Context>(null)
  
  useEffect(() => {
    loadSession()
  }, [])
  
  const loadSession = async () => {
    try {
      const session = await api.get('/session')
      setSession('authenticated')
      setIdentity(session.identity)
      setSphere(session.sphere)
      setContext(session.context)
    } catch (error) {
      setSession('error')
    }
  }
  
  const switchSphere = async (newSphereId: string) => {
    // Close all workspaces
    await closeAllWorkspaces()
    
    // Switch context
    const newContext = await api.post('/context/switch', {
      sphereId: newSphereId
    })
    
    setContext(newContext)
    setSphere(await api.get(`/spheres/${newSphereId}`))
  }
  
  return (
    <AppContext.Provider value={{
      session,
      identity,
      sphere,
      context,
      switchSphere
    }}>
      {children}
    </AppContext.Provider>
  )
}
```

**Checkpoint:** Context provider working ✓

#### DAY 6 Afternoon + DAY 7

```typescript
// Task 6.2-6.10: Core React Components

// TopBar.tsx
export function TopBar() {
  const { identity, sphere } = useContext(AppContext)
  
  return (
    <div className="top-bar">
      <IdentityBadge identity={identity} />
      <Separator>→</Separator>
      <SphereBadge sphere={sphere} />
      {/* ALWAYS visible */}
    </div>
  )
}

// Workspace.tsx
export function Workspace({ type, workspaceId }) {
  const [state, setState] = useState<WorkspaceState>('clean')
  const [content, setContent] = useState('')
  
  const handleSave = async () => {
    setState('saving')
    await api.post(`/workspaces/${workspaceId}/save`)
    setState('saved')
  }
  
  const handleClose = async () => {
    if (state === 'dirty') {
      const confirmed = await confirm({
        message: 'Unsaved changes',
        actions: ['Save', 'Discard', 'Cancel']
      })
      
      if (confirmed === 'save') {
        await handleSave()
      }
    }
    
    onClose()
  }
  
  return (
    <div className="workspace">
      {state === 'dirty' && <Badge>Unsaved changes</Badge>}
      {state === 'saved' && <Badge variant="success">Saved</Badge>}
      
      <Editor value={content} onChange={setContent} />
      
      <ActionBar>
        <Button onClick={handleSave}>Save</Button>
        <Button onClick={handleClose}>Close</Button>
      </ActionBar>
    </div>
  )
}

// AgentStagingView.tsx
export function AgentStagingView({ executionId }) {
  const [staging, setStaging] = useState(null)
  
  useEffect(() => {
    loadStaging()
  }, [executionId])
  
  const loadStaging = async () => {
    const data = await api.get(`/agent/staging/${executionId}`)
    setStaging(data)
  }
  
  return (
    <div className="agent-staging">
      <Badge variant="agent">🤖 Agent Staging</Badge>
      <Content readOnly={true}>{staging?.content}</Content>
      {/* No edit controls */}
    </div>
  )
}

// ComparisonView.tsx
export function ComparisonView({ userVersionId, agentDraftId }) {
  const [comparison, setComparison] = useState(null)
  
  const handleSaveUser = async () => {
    await api.post('/versions', {
      content: comparison.userContent,
      author: 'user'
    })
    onClose()
  }
  
  const handleSaveAgent = async () => {
    await api.post('/versions', {
      content: comparison.agentContent,
      author: 'agent',
      approvedBy: userId
    })
    onClose()
  }
  
  return (
    <div className="comparison">
      <SplitView>
        <Pane>
          <Label>Your Version</Label>
          <Content readOnly>{comparison?.userContent}</Content>
        </Pane>
        <Pane>
          <Label>Agent Proposal</Label>
          <Content readOnly>{comparison?.agentContent}</Content>
        </Pane>
      </SplitView>
      
      <ActionBar>
        <Button onClick={handleDiscard}>Discard Agent</Button>
        <Button onClick={handleSaveUser}>Save My Version</Button>
        <Button onClick={handleSaveAgent}>Save Agent Version</Button>
        <Button onClick={handleKeepBoth}>Keep Both</Button>
      </ActionBar>
    </div>
  )
}
```

**Checkpoint:** Core UI components working ✓

---

## 📅 WEEK 2: GOVERNANCE & FLOWS (Days 8-14)

### DAY 8 — Remove Auto-Save & Silent Modifications

**Duration:** 3-4 hours  
**Status:** [ ] Not Started

```bash
# Task 8.1: Search and destroy auto-save
grep -r "auto.*save" frontend/
grep -r "setInterval.*save" frontend/
grep -r "beforeunload.*save" frontend/

# Remove all auto-save patterns
# Ensure save is ONLY via explicit button click
```

**Checkpoint:** Zero auto-save in codebase ✓

---

### DAY 9 — Block Agent Production Writes

**Duration:** 3-4 hours  
**Status:** [ ] Not Started

```sql
-- Task 9.1: Database-level enforcement
-- Create agent role with restricted permissions

CREATE ROLE agent_role;

-- Grant staging access only
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_staging_workspaces TO agent_role;

-- Deny production access
REVOKE ALL ON user_workspaces FROM agent_role;
REVOKE ALL ON versions FROM agent_role;
REVOKE ALL ON threads FROM agent_role;
```

**Checkpoint:** Agents physically cannot write to production ✓

---

### DAY 10-11 — Approval System

**Duration:** 2 days (8-12 hours)  
**Status:** [ ] Not Started

```typescript
// Task 10.1: Approval Service
// File: backend/services/approvalService.ts

export class ApprovalService {
  async request(params: ApprovalRequestParams): Promise<Approval> {
    return await db.approvals.insert({
      userId: params.userId,
      planId: params.planId,
      what: params.what,
      cost: params.cost,
      scope: params.scope,
      status: 'pending'
    })
  }
  
  async approve(approvalId: string): Promise<ApprovalToken> {
    const approval = await db.approvals.findOne({ id: approvalId })
    
    // Create short-lived token
    const token = jwt.sign({
      approvalId,
      userId: approval.userId,
      planId: approval.planId,
      costCap: approval.cost,
      expiresAt: Date.now() + (15 * 60 * 1000)  // 15 minutes
    }, SECRET_KEY)
    
    await db.approvals.update({ id: approvalId }, {
      status: 'approved',
      approvedAt: new Date()
    })
    
    return { token, expiresAt: Date.now() + (15 * 60 * 1000) }
  }
  
  async reject(approvalId: string, reason: string): Promise<void> {
    await db.approvals.update({ id: approvalId }, {
      status: 'rejected',
      rejectionReason: reason,
      rejectedAt: new Date()
    })
  }
}

// Task 10.2: ApprovalModal Component
// File: frontend/components/ApprovalModal.tsx

export function ApprovalModal({ approval, onApprove, onReject }) {
  const [budget, setBudget] = useState(null)
  
  useEffect(() => {
    loadBudget()
  }, [])
  
  const exceedsBudget = approval.cost > budget?.remaining
  
  return (
    <Modal>
      <Header>Approval Required</Header>
      
      <Section title="What will happen">
        <Text>{approval.what}</Text>
      </Section>
      
      <Section title="Cost">
        <Badge variant={exceedsBudget ? 'error' : 'success'}>
          {approval.cost} tokens
        </Badge>
        {exceedsBudget && (
          <Warning>Exceeds available budget</Warning>
        )}
      </Section>
      
      <Section title="Data affected">
        <List items={approval.scope.affectedData} />
      </Section>
      
      <ActionBar>
        <Button onClick={onReject}>Reject</Button>
        <Button 
          onClick={onApprove} 
          disabled={exceedsBudget}
        >
          Approve
        </Button>
      </ActionBar>
    </Modal>
  )
}
```

**Checkpoint:** Approval system working end-to-end ✓

---

### DAY 12-13 — E2E Flows

**Duration:** 2 days  
**Status:** [ ] Not Started

```typescript
// Task 12.1: Flow 1 - Thread → Workspace → Agent → Review → Keep Both

describe('E2E Flow: Complete Agent Review', () => {
  it('should complete full agent workflow', async () => {
    // 1. Open thread
    const thread = await createThread({ title: 'Test Thread' })
    
    // 2. Open workspace
    const workspace = await openWorkspace({ threadId: thread.id })
    
    // 3. Request agent help
    const plan = await requestAgentHelp({
      workspaceId: workspace.id,
      intent: 'Improve this content'
    })
    
    // 4. Approve plan
    const approval = await approvePlan(plan.id)
    
    // 5. Execute agent
    const execution = await executeAgent({
      planId: plan.id,
      approvalToken: approval.token
    })
    
    // 6. Wait for completion
    await waitForCompletion(execution.id)
    
    // 7. Open review
    const comparison = await openReview({
      userVersionId: workspace.currentVersionId,
      agentDraftId: execution.stagingId
    })
    
    // 8. Keep both versions
    await keepBothVersions(comparison.id)
    
    // 9. Verify
    const versions = await listVersions(thread.id)
    expect(versions).toHaveLength(2)
    expect(versions[0].author).toBe('user')
    expect(versions[1].author).toBe('agent')
  })
})

// Task 12.2: Flow 2 - Global Search → Context Switch
// Task 12.3: Flow 3 - Encoding → Reject
// Task 12.4: Flow 4 - Budget Exceeded
// Task 12.5: Flow 5 - Browser Extract
```

**Checkpoint:** All 5 E2E flows passing ✓

---

### DAY 14 — Testing & Validation

**Duration:** Full day  
**Status:** [ ] Not Started

```bash
# Run full test suite
npm test

# Run E2E tests
npm run test:e2e

# Run policy tests
npm run test:policy

# Validate against checklist
node scripts/validate-checklist.js
```

**Checkpoint:** All tests green ✓

---

## 📅 WEEK 3: POLISH & LAUNCH (Days 15-21)

### DAY 15-16 — UI Polish & Context Indicators

**Duration:** 2 days  
**Status:** [ ] Not Started

```css
/* Task 15.1: Workspace visual distinction */

.workspace-user {
  border: 2px solid var(--color-primary);
  background: var(--color-surface);
}

.workspace-agent {
  border: 2px solid var(--color-agent);
  background: rgba(var(--color-agent-rgb), 0.05);
  opacity: 0.8;
}

.workspace-review {
  border: 2px solid var(--color-review);
  background: var(--color-surface);
}

/* Task 15.2: State badges */
.badge-unsaved {
  background: var(--color-warning);
  color: white;
}

.badge-readonly {
  background: var(--color-info);
  color: white;
}

.badge-agent {
  background: var(--color-agent);
  color: white;
}
```

**Checkpoint:** Visual governance signals clear ✓

---

### DAY 17-18 — Global Search & Scope

**Duration:** 2 days  
**Status:** [ ] Not Started

```typescript
// Task 17.1: Scoped Search Backend

app.get('/api/search', async (req, res) => {
  const scope = req.query.scope  // 'sphere' or 'profile'
  const query = req.query.q
  
  let results
  
  if (scope === 'sphere') {
    // Same-sphere search (editable)
    results = await searchService.searchSphere({
      sphereId: req.sphere.id,
      query
    })
  } else {
    // Profile-wide search (read-only)
    results = await searchService.searchProfile({
      userId: req.userId,
      query
    })
    
    // Enforce read-only
    results = results.map(r => ({
      ...r,
      readOnly: r.sphereId !== req.sphere.id,
      originSphere: r.sphereId
    }))
  }
  
  res.json({ results })
})

// Task 17.2: Search UI with Scope Indicator

export function SearchBar() {
  const [scope, setScope] = useState<'sphere' | 'profile'>('sphere')
  const [results, setResults] = useState([])
  
  return (
    <div>
      <ScopeSelector value={scope} onChange={setScope} />
      <Input placeholder="Search..." />
      
      <Results>
        {results.map(r => (
          <ResultItem key={r.id}>
            <SphereBadge sphere={r.originSphere} />
            {r.readOnly && <Badge>Read-only</Badge>}
            <Content />
          </ResultItem>
        ))}
      </Results>
    </div>
  )
}
```

**Checkpoint:** Scoped search working ✓

---

### DAY 19 — Technical Validation (GO/NO-GO)

**Duration:** Full day  
**Status:** [ ] Not Started

```bash
# Task 19.1: Run complete validation checklist

# Headers present?
curl -I http://localhost:3000/api/workspaces \
  -H "X-Identity-Id: ..." \
  -H "X-Sphere-Id: ..." \
  -H "X-Context-Id: ..."

# No write without approval token?
curl -X POST http://localhost:3000/api/agent/execute \
  # Should return 409_APPROVAL_REQUIRED

# Agent writes blocked?
# (test with agent credentials)
# Should return 403_AGENT_WRITE_FORBIDDEN

# Versioning append-only?
# Try to UPDATE versions table
# Should be blocked by database

# Global search read-only?
curl http://localhost:3000/api/search?scope=profile
# Check readOnly=true on external results

# Inter-sphere = references only?
# Test cross-sphere writes
# Should return 403_SCOPE_VIOLATION

# Workspace close without save OK?
# Test in UI - should always allow

# Save creates new version?
# Check versions table increments

# Comparison/diff OK?
# Test side-by-side view

# Budget blocks execution?
# Set budget to 0, try to execute
# Should return 402_BUDGET_EXCEEDED

# Audit log complete?
# Check audit_logs table has all fields
```

**Decision:** One FAIL = stop and fix before Day 20

---

### DAY 20 — QA Functional (5 Scenarios)

**Duration:** Full day  
**Status:** [ ] Not Started

```bash
# Task 20.1: Manual QA of 5 key scenarios

# Scenario 1: Thread → Workspace → Agent → Review → Keep Both
# Time: < 3 minutes
# Feel: User in control

# Scenario 2: Global Search → Cross-Sphere → Context Switch
# Time: < 2 minutes
# Feel: Origin always clear

# Scenario 3: Encoding → Reject → Nothing Modified
# Time: < 2 minutes
# Feel: Safe to experiment

# Scenario 4: Budget Exceeded → Clear Message
# Time: < 1 minute
# Feel: Always know cost

# Scenario 5: Browser Multi-Account → Manual Extract
# Time: < 3 minutes
# Feel: No auto-sync
```

**Acceptance:** All scenarios complete successfully

---

### DAY 21 — FREEZE & LAUNCH PREP

**Duration:** Full day  
**Status:** [ ] Not Started

```bash
# Task 21.1: Official freeze

git tag -a v1.0.0-governed -m "CHE·NU V1 MVP - Governed Intelligence OS"
git push origin v1.0.0-governed

# Task 21.2: Freeze canonical docs
# All 14 documents → FROZEN
# No changes allowed without version bump

# Task 21.3: Demo preparation
# 7-minute pitch deck
# Live demo script
# Backup plan

# Task 21.4: Deployment prep
# Production environment ready
# Monitoring configured
# Rollback plan ready

# Task 21.5: SOFT LAUNCH
# Private access (invited users)
# Feedback form ready
# Support channel ready
```

**Result:** PRODUCTION-READY CHE·NU V1 🚀

---

## ✅ COMPLETION CHECKLIST

### Infrastructure ✓

- [ ] PostgreSQL database deployed
- [ ] Object storage configured
- [ ] Search index running
- [ ] API Gateway live
- [ ] Auth service working
- [ ] Agent runtime sandboxed
- [ ] Budget service operational
- [ ] Audit logs append-only

### Backend ✓

- [ ] 7 middlewares implemented
- [ ] 10 policy rules enforced
- [ ] Context system working
- [ ] Workspace system complete
- [ ] Version system immutable
- [ ] Agent staging isolated
- [ ] Approval system functional
- [ ] All endpoints tested

### Frontend ✓

- [ ] Context provider working
- [ ] TopBar always visible
- [ ] Workspace components complete
- [ ] Agent staging view read-only
- [ ] Comparison view functional
- [ ] Approval modal working
- [ ] Search with scope indicator
- [ ] All state machines implemented

### Governance ✓

- [ ] No auto-save anywhere
- [ ] No silent modifications
- [ ] No agent production writes
- [ ] No version overwrites
- [ ] No approval bypasses
- [ ] No cross-sphere writes
- [ ] Context always visible
- [ ] Budget enforcement working

### Testing ✓

- [ ] Unit tests passing (backend)
- [ ] Integration tests passing
- [ ] E2E tests passing (5 flows)
- [ ] Policy tests passing
- [ ] Manual QA complete
- [ ] Performance acceptable
- [ ] Security audit passed

### Documentation ✓

- [ ] All 14 docs frozen
- [ ] API docs complete
- [ ] Developer guide ready
- [ ] User guide ready
- [ ] Investor deck ready
- [ ] Demo script prepared

---

## 🎯 SUCCESS METRICS

```
Technical:
✓ Zero auto-save violations
✓ Zero agent production writes
✓ 100% approval gate coverage
✓ Versions 100% immutable
✓ Workspace isolation verified

User Experience:
✓ Users know context (100%)
✓ Users can cancel/close (100%)
✓ Governance visible (100%)
✓ Agent work exploratory (100%)

Business:
✓ MVP demonstrates governance
✓ Enterprise-ready security
✓ Audit compliance built-in
✓ Investor demo compelling
✓ Defensible IP established
```

---

## 💪 FINAL MOTIVATION

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  21 DAYS TO CHANGE THE WORLD                  ║
║                                               ║
║  Day 1-7:   Build the foundation              ║
║  Day 8-14:  Enforce governance                ║
║  Day 15-21: Polish and ship                   ║
║                                               ║
║  Result: Production-ready Governed OS         ║
║          that the world has never seen        ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

**🚀 ULTRA-ACTIONABLE CHECKLIST COMPLETE! LET'S BUILD! 💪**
