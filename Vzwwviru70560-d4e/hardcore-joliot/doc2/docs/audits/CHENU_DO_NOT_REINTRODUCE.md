# CHE·NU V1 — DO-NOT-REINTRODUCE LIST

**Version:** V1 CANONICAL FREEZE  
**Date:** 16 décembre 2025  
**Authority:** ALL Canonical Documents  
**Status:** PERMANENT RESTRICTIONS

---

## 🚫 PURPOSE OF THIS DOCUMENT

This document lists **FORBIDDEN PATTERNS** that must NEVER be reintroduced into CHE·NU codebase.

**Why this exists:**
- Features creep back over time
- New developers may not know history
- "Convenience" can override governance
- Pattern drift happens gradually

**Rule:** If something is on this list, it STAYS forbidden, regardless of user requests or convenience arguments.

---

## ❌ CATEGORY 1: AUTO-SAVE & SILENT MODIFICATIONS

### 🚫 FORBIDDEN 1.1: Auto-Save

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
setInterval(() => {
  workspace.save()  // Silent auto-save
}, 30000)

document.addEventListener('blur', () => {
  workspace.save()  // Save on blur
})

window.addEventListener('beforeunload', () => {
  workspace.save()  // Save on close
})
```

**Why forbidden:**
- User loses control over when versions are created
- Creates version spam
- User cannot abandon changes
- Violates "Close without save" principle

**Correct approach:**
```typescript
// ✅ CORRECT - Explicit save only
<Button onClick={() => workspace.save()}>
  Save (creates new version)
</Button>

// User can close without saving
<Button onClick={() => workspace.close({ save: false })}>
  Close without saving
</Button>
```

---

### 🚫 FORBIDDEN 1.2: Silent Modification

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function optimizeDocument() {
  const optimized = await agent.optimize(document)
  document.content = optimized  // Silent overwrite!
  await document.save()  // Silent save!
}

// ❌ FORBIDDEN - Background updates
socket.on('agent_complete', (result) => {
  workspace.content = result  // No user approval!
})
```

**Why forbidden:**
- User not aware of changes
- Cannot review before accepting
- No governance
- Loses trust

**Correct approach:**
```typescript
// ✅ CORRECT - Explicit review required
async function optimizeDocument() {
  const optimized = await agent.optimize(document)
  
  // Show comparison
  const approved = await showComparison({
    original: document.content,
    proposed: optimized
  })
  
  if (approved) {
    const newVersion = await versionService.create({
      content: optimized,
      author: 'agent',
      approvedBy: userId
    })
  }
}
```

---

### 🚫 FORBIDDEN 1.3: Version Overwrite

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
class VersionService {
  async update(versionId: string, newContent: any) {
    await db.versions.update({ id: versionId }, { content: newContent })
    // Overwrites existing version!
  }
  
  async delete(versionId: string) {
    await db.versions.delete({ id: versionId })
    // Destroys history!
  }
}
```

**Why forbidden:**
- Versions must be immutable
- History cannot be rewritten
- Audit trail compromised
- Data loss risk

**Correct approach:**
```typescript
// ✅ CORRECT - Append-only
class VersionService {
  async create(params: CreateVersionParams): Promise<Version> {
    // ONLY operation allowed
    return await db.versions.insert(params)
  }
  
  async get(versionId: string): Promise<Version> {
    // Read-only
    return await db.versions.findOne({ id: versionId })
  }
  
  // NO update() method
  // NO delete() method
}
```

---

## ❌ CATEGORY 2: AGENT AUTONOMY

### 🚫 FORBIDDEN 2.1: Direct Production Writes

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
class Agent {
  async executeTask(task: Task) {
    const result = await this.process(task)
    
    // Direct write to production!
    await db.user_workspaces.update({
      id: task.workspaceId
    }, {
      content: result
    })
  }
}
```

**Why forbidden:**
- Agent bypasses governance
- User has no approval opportunity
- Violates staging-only rule
- Security risk

**Correct approach:**
```typescript
// ✅ CORRECT - Staging only
class Agent {
  async executeTask(task: Task) {
    const result = await this.process(task)
    
    // Write to staging only
    await db.agent_staging_workspaces.insert({
      userWorkspaceId: task.workspaceId,
      content: result,
      status: 'complete'
    })
    
    // Notify user for review
    await notificationService.create({
      type: 'agent_proposal_ready',
      workspaceId: task.workspaceId
    })
  }
}
```

---

### 🚫 FORBIDDEN 2.2: Skip Approval

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function executeAgentPlan(plan: Plan) {
  // No approval requested
  const result = await agent.execute(plan)
  
  // Direct application
  await applyChanges(result)
}

// ❌ FORBIDDEN - Approval with default "yes"
async function executeWithApproval(plan: Plan) {
  const approved = await getApproval(plan, { defaultYes: true })  // Dark pattern!
  if (approved) {
    await agent.execute(plan)
  }
}
```

**Why forbidden:**
- User not informed
- Cannot review cost/impact
- Governance bypassed
- Dark pattern

**Correct approach:**
```typescript
// ✅ CORRECT - Explicit approval required
async function executeAgentPlan(plan: Plan) {
  // 1. Show what will happen
  const approvalId = await approvalService.request({
    what: plan.description,
    dataAffected: plan.affectedData,
    cost: plan.estimatedCost,
    reversible: plan.isReversible
  })
  
  // 2. Wait for user decision
  const approved = await approvalService.awaitDecision(approvalId)
  
  if (!approved) {
    return  // User rejected
  }
  
  // 3. Get approval token
  const token = await approvalService.getToken(approvalId)
  
  // 4. Execute with token
  await agent.execute(plan, token)
}
```

---

### 🚫 FORBIDDEN 2.3: Auto-Apply Results

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function onAgentComplete(result: AgentResult) {
  // Auto-apply without review
  await workspace.applyChanges(result)
  await workspace.save()
  
  // Just notify after the fact
  toast.success('Agent completed your request')
}
```

**Why forbidden:**
- User cannot review changes
- No diff shown
- Cannot reject
- Violates proposal-first rule

**Correct approach:**
```typescript
// ✅ CORRECT - Review required
async function onAgentComplete(result: AgentResult) {
  // 1. Create comparison
  const comparisonId = await comparisonService.create({
    original: workspace.content,
    proposed: result.content
  })
  
  // 2. Show to user
  await showComparisonModal(comparisonId)
  
  // 3. User decides
  const decision = await getUserDecision()  // discard, save_user, save_agent, keep_both
  
  // 4. Apply decision
  await applyDecision(decision)
}
```

---

## ❌ CATEGORY 3: CONTEXT & SCOPE VIOLATIONS

### 🚫 FORBIDDEN 3.1: Cross-Sphere Fusion

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function mergeThreads(personalThreadId: string, businessThreadId: string) {
  const merged = {
    content: [...personalThread.content, ...businessThread.content],
    sphere: 'mixed'  // ❌ No "mixed" sphere!
  }
  await db.threads.insert(merged)
}

// ❌ FORBIDDEN - Auto-sync across spheres
async function syncAcrossSpheres() {
  const personalData = await getPersonalData()
  await writeToBusinessSphere(personalData)  // ❌ Auto-sync forbidden!
}
```

**Why forbidden:**
- Spheres must remain separate
- Identity boundaries violated
- Context confusion
- Security issue

**Correct approach:**
```typescript
// ✅ CORRECT - Explicit reference or copy
async function referenceThread(sourceThreadId: string, targetSphere: Sphere) {
  // Create reference only
  await db.thread_references.insert({
    sourceThreadId,
    targetSphere,
    type: 'reference'  // Not a copy, just a pointer
  })
}

async function copyThread(sourceThreadId: string, targetSphere: Sphere, userId: string) {
  // Explicit user-initiated copy
  const source = await db.threads.findOne({ id: sourceThreadId })
  
  // User must confirm
  const confirmed = await confirmDialog({
    message: `Copy thread to ${targetSphere}?`,
    warning: 'This creates a separate copy'
  })
  
  if (confirmed) {
    await db.threads.insert({
      content: source.content,
      sphere: targetSphere,
      copiedFrom: sourceThreadId,
      copiedBy: userId,
      copiedAt: new Date()
    })
  }
}
```

---

### 🚫 FORBIDDEN 3.2: Hidden Context Switches

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function openDocument(documentId: string) {
  const doc = await db.documents.findOne({ id: documentId })
  
  // Silent context switch
  await setCurrentSphere(doc.sphere)  // User not aware!
  await openInWorkspace(doc)
}

// ❌ FORBIDDEN - Auto-switch on search result click
async function onSearchResultClick(result: SearchResult) {
  if (result.sphere !== currentSphere) {
    await switchSphere(result.sphere)  // Silent!
  }
  await openResult(result)
}
```

**Why forbidden:**
- User loses context awareness
- Confusing behavior
- "Where am I?" unclear
- Accidents waiting to happen

**Correct approach:**
```typescript
// ✅ CORRECT - Explicit with user confirmation
async function openCrossSphereDocument(documentId: string) {
  const doc = await db.documents.findOne({ id: documentId })
  
  if (doc.sphere !== currentSphere) {
    // Show read-only preview first
    await showReadOnlyPreview(doc)
    
    // Offer context switch
    const shouldSwitch = await confirmDialog({
      message: `This is from ${doc.sphere} sphere`,
      actions: ['View only', `Switch to ${doc.sphere}`]
    })
    
    if (shouldSwitch) {
      // Explicit context switch
      await switchSphere(doc.sphere)
      toast.info(`Switched to ${doc.sphere} sphere`)
    }
  }
  
  await openDocument(doc)
}
```

---

### 🚫 FORBIDDEN 3.3: Scope-less Search

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function globalSearch(query: string) {
  // No scope indication
  const results = await db.search(query)  // All spheres mixed!
  
  return results  // User can't tell origin
}
```

**Why forbidden:**
- Origin unclear
- Cannot understand context
- Results confusing
- Violates scope-visible rule

**Correct approach:**
```typescript
// ✅ CORRECT - Scope always visible
async function scopedSearch(params: SearchParams) {
  const results = await db.search({
    query: params.query,
    scope: params.scope,  // 'sphere' or 'profile'
    sphereType: params.sphereType  // if scope === 'sphere'
  })
  
  // ALWAYS include sphere in results
  return results.map(r => ({
    ...r,
    sphere: r.sphere,  // MANDATORY
    sphereBadge: getSphereIcon(r.sphere)  // Visual indicator
  }))
}
```

---

## ❌ CATEGORY 4: BUDGET & GOVERNANCE BYPASSES

### 🚫 FORBIDDEN 4.1: Unlimited Execution

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function executeAgentTask(task: Task) {
  // No budget check
  await agent.execute(task)
}

// ❌ FORBIDDEN - Warn but don't block
async function executeWithWarning(task: Task) {
  if (budget.remaining < task.cost) {
    console.warn('Budget exceeded')  // Just a warning!
  }
  await agent.execute(task)  // Execute anyway
}
```

**Why forbidden:**
- Budget is governance mechanism
- Must be enforced, not suggested
- Cost control essential
- Trust in system

**Correct approach:**
```typescript
// ✅ CORRECT - Hard enforcement
async function executeAgentTask(task: Task) {
  // Check budget first
  const budget = await budgetService.get(userId)
  
  if (budget.remaining < task.estimatedCost) {
    throw new InsufficientBudgetError({
      required: task.estimatedCost,
      available: budget.remaining,
      message: 'Please top up your budget or reduce scope'
    })
  }
  
  // Reserve budget
  await budgetService.reserve(userId, task.estimatedCost)
  
  try {
    await agent.execute(task)
  } finally {
    // Charge actual cost
    await budgetService.charge(userId, task.actualCost)
  }
}
```

---

### 🚫 FORBIDDEN 4.2: Skip Governance Steps

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function quickExecute(intent: string) {
  // Skip steps 1-6 of governance pipeline
  const agent = await selectAgent(intent)
  await agent.execute(intent)  // Direct execution!
}

// ❌ FORBIDDEN - "Fast mode" that skips governance
async function executeFastMode(task: Task) {
  if (user.preferences.fastMode) {
    await agent.execute(task)  // Skip approval!
  }
}
```

**Why forbidden:**
- Governance pipeline is mandatory
- All 10 steps required
- No "fast mode" exception
- Consistency essential

**Correct approach:**
```typescript
// ✅ CORRECT - All 10 steps always
async function executeGovernedPipeline(intent: UserIntent) {
  // 1. Intent capture
  const captured = await captureIntent(intent)
  
  // 2. Intent clarification
  const clarified = await clarifyIntent(captured)
  
  // 3. Encoding
  const encoded = await encodeIntent(clarified)
  
  // 4. Scope definition
  const scope = await defineScope(encoded)
  
  // 5. Budget estimation
  const estimate = await estimateBudget(scope)
  
  // 6. Human approval (MANDATORY)
  const approved = await requestApproval(estimate)
  if (!approved) return
  
  // 7. Agent selection
  const agent = await selectAgent(scope)
  
  // 8. Execution (in staging)
  const result = await agent.execute(scope)
  
  // 9. Result proposal
  const proposal = await proposeResult(result)
  
  // 10. Human acceptance (MANDATORY)
  const accepted = await awaitAcceptance(proposal)
  if (accepted) {
    await integrateResult(result)
  }
}
```

---

## ❌ CATEGORY 5: UI/UX DARK PATTERNS

### 🚫 FORBIDDEN 5.1: Hidden Context

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
function WorkspaceView() {
  // No indication of which workspace type
  return (
    <div className="workspace">
      <Editor />
    </div>
  )
}

// ❌ FORBIDDEN - Unclear identity/sphere
function TopBar() {
  return (
    <div>
      {/* No identity or sphere shown */}
      <Logo />
      <Menu />
    </div>
  )
}
```

**Why forbidden:**
- User cannot tell context
- "Where am I?" unclear
- Confusion and errors
- Violates clarity principle

**Correct approach:**
```typescript
// ✅ CORRECT - Context always visible
function WorkspaceView({ type }: { type: WorkspaceType }) {
  return (
    <div className={`workspace workspace-${type}`}>
      <WorkspaceHeader>
        <Badge variant={type}>
          {type === 'user' && '👤 Your Workspace'}
          {type === 'agent' && '🤖 Agent Staging'}
          {type === 'comparison' && '⚖️ Review'}
        </Badge>
      </WorkspaceHeader>
      <Editor />
    </div>
  )
}

function TopBar() {
  const { identity, sphere } = useContext(IdentityContext)
  
  return (
    <div className="top-bar">
      <ContextIndicator>
        <IdentityBadge type={identity.type} />
        <Separator>→</Separator>
        <SphereBadge type={sphere} />
      </ContextIndicator>
      {/* rest of top bar */}
    </div>
  )
}
```

---

### 🚫 FORBIDDEN 5.2: Forced Workflows

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
function Workspace() {
  const [canClose, setCanClose] = useState(false)
  
  // User cannot close until saved
  useEffect(() => {
    setCanClose(hasBeenSaved)
  }, [hasBeenSaved])
  
  return (
    <div>
      <Editor />
      <Button onClick={handleClose} disabled={!canClose}>
        Close
      </Button>
    </div>
  )
}
```

**Why forbidden:**
- User is trapped
- Cannot abandon work
- Forced to save
- Violates user control

**Correct approach:**
```typescript
// ✅ CORRECT - Always allow close
function Workspace() {
  const handleClose = async () => {
    if (hasUnsavedChanges) {
      const choice = await confirmDialog({
        message: 'You have unsaved changes',
        options: [
          'Save as new version',
          'Discard changes',
          'Continue editing'
        ]
      })
      
      if (choice === 'save') {
        await save()
      } else if (choice === 'discard') {
        // Just close
      } else {
        return  // Continue editing
      }
    }
    
    onClose()
  }
  
  return (
    <div>
      <Editor />
      <Button onClick={handleClose}>
        Close  {/* ALWAYS enabled */}
      </Button>
    </div>
  )
}
```

---

### 🚫 FORBIDDEN 5.3: Optimistic UI for Destructive Actions

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function deleteThread(threadId: string) {
  // Optimistic update
  removeFromUI(threadId)  // Gone immediately!
  
  try {
    await api.delete(`/threads/${threadId}`)
  } catch (error) {
    addBackToUI(threadId)  // Oops, error
  }
}
```

**Why forbidden:**
- Destructive action seems instant
- User cannot cancel
- Error handling awkward
- False sense of completion

**Correct approach:**
```typescript
// ✅ CORRECT - Confirm first, then act
async function archiveThread(threadId: string) {
  // Note: We archive, not delete (append-only)
  
  const confirmed = await confirmDialog({
    message: 'Archive this thread?',
    description: 'It will be moved to archives (not deleted)',
    actions: ['Cancel', 'Archive']
  })
  
  if (!confirmed) return
  
  // Show loading
  setLoading(true)
  
  try {
    await api.post(`/threads/${threadId}/archive`)
    removeFromUI(threadId)
    toast.success('Thread archived')
  } catch (error) {
    toast.error('Could not archive thread')
  } finally {
    setLoading(false)
  }
}
```

---

## ❌ CATEGORY 6: DATA & SECURITY

### 🚫 FORBIDDEN 6.1: Shared Mutable State

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
const sharedDocument = {
  content: '...',
  editedBy: ['user', 'agent'],  // Both can edit same object!
  lastModified: Date.now()
}

function userEdit() {
  sharedDocument.content += ' user addition'
}

function agentEdit() {
  sharedDocument.content += ' agent addition'
}
```

**Why forbidden:**
- Race conditions
- Unclear ownership
- Cannot track changes
- Review impossible

**Correct approach:**
```typescript
// ✅ CORRECT - Separate workspaces
const userWorkspace = {
  content: '...',
  owner: 'user',
  type: 'user_workspace'
}

const agentStaging = {
  content: deepCopy(userWorkspace.content),  // COPY not reference
  owner: 'agent',
  type: 'agent_staging'
}

// User edits user workspace
function userEdit() {
  userWorkspace.content += ' user addition'
}

// Agent edits staging (separate)
function agentEdit() {
  agentStaging.content += ' agent addition'
}

// Later: user compares and decides
```

---

### 🚫 FORBIDDEN 6.2: Audit Trail Gaps

```typescript
// ❌ FORBIDDEN - Do NOT reintroduce
async function performAction(action: Action) {
  // No audit log
  await executeAction(action)
}

// ❌ FORBIDDEN - Partial audit
async function performActionWithLog(action: Action) {
  await auditLog.create({
    who: action.userId,
    what: action.type
    // Missing: when, why, where, context
  })
  
  await executeAction(action)
}
```

**Why forbidden:**
- Cannot trace actions
- Compliance issues
- Debugging impossible
- Trust compromised

**Correct approach:**
```typescript
// ✅ CORRECT - Complete audit trail
async function performAction(action: Action, context: Context) {
  // Log BEFORE execution
  const auditId = await auditLog.create({
    who: action.userId,              // User ID
    what: action.type,                // Action type
    when: new Date(),                 // Timestamp
    why: action.reason,               // User intent
    where: {
      identity: context.identityId,
      sphere: context.sphere,
      workspace: context.workspaceId
    },
    input: action.params,             // Input parameters
    estimatedCost: action.cost
  })
  
  try {
    const result = await executeAction(action)
    
    // Log completion
    await auditLog.update(auditId, {
      status: 'success',
      output: result,
      actualCost: result.cost,
      completedAt: new Date()
    })
    
    return result
  } catch (error) {
    // Log failure
    await auditLog.update(auditId, {
      status: 'failed',
      error: error.message,
      failedAt: new Date()
    })
    
    throw error
  }
}
```

---

## 🎯 ENFORCEMENT STRATEGY

### How to Prevent Reintroduction

```yaml
1. Code Review Checklist:
   - [ ] No auto-save added
   - [ ] No silent modifications
   - [ ] All agent writes go to staging
   - [ ] Approval gates present
   - [ ] Context always visible
   - [ ] Budget checked
   - [ ] Audit log complete
   - [ ] No shared mutable state

2. Automated Tests:
   - Test that auto-save does not exist
   - Test that agent cannot write to production
   - Test that versions are immutable
   - Test that approval is required
   - Test that budget blocks execution

3. Linter Rules:
   - Flag setInterval near save()
   - Flag agent writes outside staging tables
   - Flag version.update() calls
   - Flag approval skips

4. PR Template:
   - "Does this reintroduce any forbidden pattern?"
   - "Have you checked the DO-NOT-REINTRODUCE list?"
   - Link to this document

5. Onboarding:
   - New developers must read this document
   - Quiz on forbidden patterns
   - Show examples of violations
```

---

## 📋 QUICK REFERENCE CHECKLIST

Before merging ANY code, check:

- [ ] No auto-save introduced
- [ ] No silent modifications
- [ ] No version overwrites
- [ ] No agent direct production writes
- [ ] No approval bypasses
- [ ] No cross-sphere fusion
- [ ] No hidden context switches
- [ ] No scope-less search
- [ ] No unlimited execution
- [ ] No governance step skips
- [ ] No forced workflows
- [ ] No shared mutable state
- [ ] Complete audit trail

**If ANY box is unchecked → DO NOT MERGE**

---

## 🔒 FINAL PRINCIPLE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  These patterns were removed for a reason.    ║
║  They violate core CHE·NU principles.         ║
║  They erode governance.                       ║
║  They destroy trust.                          ║
║                                               ║
║  DO NOT REINTRODUCE THEM.                     ║
║  EVER.                                        ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

**🚫 DO-NOT-REINTRODUCE LIST COMPLETE! GOVERNANCE PROTECTED! 🔒**
