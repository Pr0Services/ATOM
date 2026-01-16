# CHE·NU™ — ORCHESTRATOR SERVICE
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**The Orchestrator Service is the ONLY authority allowed to:**

- Interpret user intent
- Plan actions
- Select agents
- Enforce governance
- Control execution
- Require approvals
- Integrate results

**Nova guides.**  
**Agents execute.**  
**Orchestrator decides IF and HOW.**

---

## 🔐 MANDATORY HEADERS

Every request **MUST** include:
- `x-identity-id`
- `x-context-id`

**If missing → HARD REJECT.**

---

## 🧠 CORE CONCEPTS

### INTENT
High-level user request (natural language or structured)

### PLAN
Ordered list of governed steps. Each step defines:
- Agent
- Skill
- Tool
- Cost
- Output

### EXECUTION
Running a plan step-by-step:
- Always sandboxed
- Always traceable
- Always governed

### APPROVAL
Explicit human validation gate:
- Mandatory for agent-generated outputs
- User can approve, reject, or request regeneration

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Commands Table (USER INTENT)

```sql
CREATE TABLE commands (
  id UUID PRIMARY KEY,
  identity_id UUID NOT NULL,
  context_id UUID NOT NULL,
  sphere TEXT NOT NULL,
  intent TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'created'
    CHECK (status IN (
      'created',
      'planned',
      'awaiting_approval',
      'approved',
      'executing',
      'completed',
      'failed',
      'cancelled'
    )),
  estimated_cost JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_commands_identity ON commands(identity_id);
CREATE INDEX idx_commands_status ON commands(status);
CREATE INDEX idx_commands_sphere ON commands(sphere);
```

**COMMAND STATUSES:**
- `created`: Command received, not yet planned
- `planned`: Execution plan generated
- `awaiting_approval`: Waiting for user approval
- `approved`: User approved, ready to execute
- `executing`: Currently running
- `completed`: Successfully completed
- `failed`: Execution failed
- `cancelled`: User cancelled

---

### Execution Plans Table

```sql
CREATE TABLE execution_plans (
  id UUID PRIMARY KEY,
  command_id UUID NOT NULL REFERENCES commands(id) ON DELETE CASCADE,
  step_index INT NOT NULL,
  agent_id UUID NOT NULL,
  skill TEXT NOT NULL,
  tool TEXT NOT NULL,
  estimated_tokens INT NOT NULL,
  estimated_cost JSONB NOT NULL,
  requires_approval BOOLEAN NOT NULL DEFAULT true,
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN (
      'pending',
      'approved',
      'running',
      'completed',
      'failed',
      'skipped'
    )),
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE(command_id, step_index)
);

CREATE INDEX idx_plans_command ON execution_plans(command_id);
CREATE INDEX idx_plans_status ON execution_plans(status);
```

**PLAN STEP PROPERTIES:**
- `step_index`: Order of execution (0, 1, 2, ...)
- `agent_id`: Which agent will execute
- `skill`: High-level capability (e.g., "summarize_text")
- `tool`: Specific implementation (e.g., "claude-3-haiku")
- `estimated_tokens`: Expected token consumption
- `estimated_cost`: Cost breakdown (JSONB)
- `requires_approval`: Whether user approval is needed

---

### Execution Results Table

```sql
CREATE TABLE execution_results (
  id UUID PRIMARY KEY,
  plan_step_id UUID NOT NULL REFERENCES execution_plans(id) ON DELETE CASCADE,
  agent_type TEXT NOT NULL CHECK (agent_type IN ('llm','tool','hybrid')),
  output_reference JSONB NOT NULL, 
    -- links to files / versions / threads
  token_usage INT NOT NULL,
  cost JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_results_step ON execution_results(plan_step_id);
```

**RESULT PROPERTIES:**
- `agent_type`: Type of agent execution
- `output_reference`: Pointers to outputs (never raw content)
- `token_usage`: Actual tokens consumed
- `cost`: Actual cost incurred

---

## 📜 CANONICAL RULES (NON-NEGOTIABLE)

### ORCHESTRATION RULES

1. **Orchestrator is the ONLY service allowed to invoke Agent Runtime**
2. **No direct user → agent execution is allowed**
3. **Each command MUST have an execution plan before execution**
4. **Budget check MUST pass before plan approval**
5. **Scope MUST be locked before execution**
6. **Agent outputs NEVER auto-integrate into user space**

### APPROVAL RULES

1. **Any agent-generated content requires explicit user approval**
2. **Approval is per step OR per plan** (configurable)
3. **User can reject, edit, or request regeneration**
4. **Approval timeout → automatic rejection**

---

## 🔄 PLAN GENERATION FLOW

```
1. Receive intent
2. Validate identity & context
3. Determine sphere
4. Query Skill & Tool Registry
5. Select agents
6. Estimate tokens & cost
7. Build execution plan
8. Set command status = 'planned'
9. Await approval (if required)
```

---

## ⚙️ EXECUTION FLOW

```
1. Verify approval
2. Lock scope (Identity & Context Service)
3. Execute steps sequentially
4. For each step:
   a. Create sandbox job (Agent Runtime)
   b. Pass context + constraints
   c. Collect output
   d. Record token usage
5. Store outputs as references
6. Set status = 'completed' or 'failed'
7. Unlock scope
8. Emit events
```

---

## 🌐 REST ENDPOINTS (CANONICAL)

```
POST   /v1/commands                  # Create command from intent
GET    /v1/commands/:id              # Get command details

POST   /v1/commands/:id/plan         # Generate execution plan
GET    /v1/commands/:id/plan         # Get plan details

POST   /v1/commands/:id/approve      # Approve plan
POST   /v1/commands/:id/reject       # Reject plan

POST   /v1/commands/:id/execute      # Execute approved plan
POST   /v1/commands/:id/cancel       # Cancel execution

GET    /v1/commands/:id/status       # Get execution status
```

---

## 📋 DTO DEFINITIONS

### CreateCommandDto

```typescript
export class CreateCommandDto {
  @IsString()
  @IsNotEmpty()
  intent: string; // Natural language or structured
  
  @IsOptional()
  @IsString()
  targetSphere?: string; // Default = active context sphere
  
  @IsOptional()
  @IsObject()
  constraints?: {
    maxBudget?: number;
    maxDuration?: number;
    requiredApprovals?: boolean;
  };
  
  @IsOptional()
  @IsObject()
  maxBudget?: {
    usd?: number;
    tokens?: number;
  };
}
```

---

### ApproveCommandDto

```typescript
export class ApproveCommandDto {
  @IsBoolean()
  approved: boolean;
  
  @IsOptional()
  @IsString()
  notes?: string;
  
  @IsOptional()
  @IsObject()
  modifications?: {
    stepIndex?: number;
    newTool?: string;
    newConstraints?: any;
  };
}
```

---

## 📡 EVENTS (PUB/SUB)

### Published Events

```typescript
COMMAND.CREATED
COMMAND.PLANNED
COMMAND.APPROVED
COMMAND.EXECUTION.STARTED
COMMAND.STEP.COMPLETED
COMMAND.EXECUTION.COMPLETED
COMMAND.EXECUTION.FAILED
COMMAND.CANCELLED
```

### Event Payload

```typescript
{
  commandId: string;
  identityId: string;
  contextId: string;
  sphere: string;
  status: string;
  timestamp: string;
  metadata?: {
    stepIndex?: number;
    tokensUsed?: number;
    cost?: any;
  };
}
```

---

## 📝 AUDIT & GOVERNANCE

### Every Step Logs

```typescript
{
  identity_id: string;
  context_id: string;
  agent_id: string;
  skill: string;
  tool: string;
  token_usage: number;
  cost: object;
  timestamp: string;
  status: string;
}
```

### Violations Trigger

- **Hard stop** of execution
- **Audit record** creation
- **User notification** (immediate)
- **Incident report** to governance log

---

## 🚨 FAILURE HANDLING

### If Any Step Fails

1. **Stop execution** immediately
2. **Mark command as 'failed'**
3. **Keep partial outputs isolated** (not integrated)
4. **Require user decision:** retry, modify, or discard
5. **Log failure details** for debugging

### Retry Strategy

```typescript
{
  maxRetries: 3,
  retryDelay: [1000, 5000, 15000], // ms
  retryConditions: [
    'timeout',
    'rate_limit',
    'transient_error'
  ]
}
```

---

## 🔗 INTEGRATION POINTS

### Upstream Dependencies
- **Identity & Context Service**: Validates headers, locks scope
- **Skill & Tool Registry**: Provides capabilities catalog
- **Budget & Governance Service**: Validates budgets

### Downstream Services
- **Agent Runtime Service**: Executes agent jobs
- **Versioning Service**: Creates versions of outputs
- **Thread Service**: Logs execution in threads
- **Audit Service**: Records all actions

---

## 🎯 SUCCESS CRITERIA

- ✅ 100% of executions require approval
- ✅ Zero unauthorized agent invocations
- ✅ Complete audit trail for all commands
- ✅ Budget limits are enforced before execution
- ✅ Scope is locked during execution
- ✅ Outputs never auto-integrate

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** Identity & Context, Skill & Tool Registry, Agent Runtime  
**Complexity:** Very High  
**LOC Estimate:** ~5,000 lines  
**Implementation Time:** 7-10 days  

---

## 🚀 IMPLEMENTATION CHECKLIST

- [ ] Set up NestJS module structure
- [ ] Create PostgreSQL schema
- [ ] Implement command creation endpoint
- [ ] Integrate with Skill & Tool Registry
- [ ] Implement plan generation logic
- [ ] Add approval workflow
- [ ] Integrate with Agent Runtime
- [ ] Implement execution engine
- [ ] Add failure handling & retry logic
- [ ] Set up event publishing
- [ ] Integrate with Audit Service
- [ ] Write unit tests (85% coverage)
- [ ] Write integration tests
- [ ] Performance testing
- [ ] Deploy to staging

---

## 🔐 FINAL RULE

**If an action cannot be:**
- Planned
- Budgeted
- Approved
- Audited
- Rolled back

**IT MUST NOT EXECUTE.**

**THE ORCHESTRATOR IS THE GOVERNOR OF CHE·NU.**

---

**END OF IMPLEMENTATION BLOCK**
