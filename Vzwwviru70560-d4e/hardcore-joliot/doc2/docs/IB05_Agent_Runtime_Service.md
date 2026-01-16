# CHE·NU™ — AGENT RUNTIME SERVICE
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**The Agent Runtime Service is responsible for:**

- Executing agent jobs in isolated sandboxes
- Managing agent workspaces (files, memory, outputs)
- Interfacing with LLMs and tools
- Enforcing execution constraints
- Reporting results back to the Orchestrator

**Agents NEVER act on their own.**  
**Agents NEVER write directly to user space.**

---

## 🔐 MANDATORY HEADERS

Every execution request **MUST** include:
- `x-identity-id`
- `x-context-id`
- `x-command-id`
- `x-plan-step-id`

**Missing any header → HARD REJECT.**

---

## 🧠 CORE CONCEPTS

### AGENT
A configured execution profile:
- LLM model + provider
- Skills allowed
- Resource limits
- Constraints

### JOB
One execution instance created by the Orchestrator:
- Bound to a specific plan step
- Has a unique sandbox
- Reports back to Orchestrator

### SANDBOX
Isolated execution environment:
- Isolated filesystem
- Isolated memory
- Resource quotas enforced
- Destroyed or archived after execution

### OUTPUT
Files, data, or references produced by the agent:
- Never auto-integrated
- Stored as references only
- Require user approval before integration

---

## 📁 FILESYSTEM LAYOUT (SANDBOX)

```
/agent-space/{job_id}/
  /input/        # Immutable inputs from orchestrator
  /work/         # Temporary agent work area
  /output/       # Generated files (read-only post-run)
  /memory/       # Agent internal notes (isolated)
  /logs/         # Execution logs
```

**RULES:**
- `/input/` is READ-ONLY for the agent
- `/work/` is READ-WRITE during execution
- `/output/` becomes READ-ONLY after execution
- `/memory/` is private to the agent instance
- `/logs/` captures all execution traces

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Agents Table (CONFIGURATION)

```sql
CREATE TABLE agents (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  agent_level TEXT NOT NULL
    CHECK (agent_level IN ('L0','L1','L2')),
  llm_provider TEXT NOT NULL,
  llm_model TEXT NOT NULL,
  max_tokens INT NOT NULL,
  temperature NUMERIC NOT NULL DEFAULT 0.2,
  allowed_skills TEXT[] NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_agents_level ON agents(agent_level);
CREATE INDEX idx_agents_provider ON agents(llm_provider);
```

**AGENT PROPERTIES:**
- `agent_level`: L0 (basic), L1 (intermediate), L2 (advanced)
- `llm_provider`: openai, anthropic, mistral, local
- `llm_model`: specific model (e.g., gpt-4o, claude-3-sonnet)
- `max_tokens`: Hard limit for this agent
- `temperature`: Model temperature setting
- `allowed_skills`: Array of skill codes this agent can use

---

### Agent Jobs Table (EXECUTION)

```sql
CREATE TABLE agent_jobs (
  id UUID PRIMARY KEY,
  command_id UUID NOT NULL,
  plan_step_id UUID NOT NULL,
  agent_id UUID NOT NULL REFERENCES agents(id),
  identity_id UUID NOT NULL,
  context_id UUID NOT NULL,
  status TEXT NOT NULL DEFAULT 'created'
    CHECK (status IN (
      'created',
      'running',
      'completed',
      'failed',
      'cancelled'
    )),
  token_limit INT NOT NULL,
  tokens_used INT DEFAULT 0,
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_jobs_command ON agent_jobs(command_id);
CREATE INDEX idx_jobs_status ON agent_jobs(status);
CREATE INDEX idx_jobs_agent ON agent_jobs(agent_id);
```

**JOB STATUSES:**
- `created`: Job initialized, not started
- `running`: Currently executing
- `completed`: Successfully finished
- `failed`: Execution failed
- `cancelled`: Manually cancelled

---

### Agent Outputs Table (REFERENCES ONLY)

```sql
CREATE TABLE agent_outputs (
  id UUID PRIMARY KEY,
  job_id UUID NOT NULL REFERENCES agent_jobs(id) ON DELETE CASCADE,
  output_type TEXT NOT NULL
    CHECK (output_type IN (
      'file',
      'version',
      'thread',
      'dataset',
      'log'
    )),
  reference JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_outputs_job ON agent_outputs(job_id);
CREATE INDEX idx_outputs_type ON agent_outputs(output_type);
```

**OUTPUT TYPES:**
- `file`: Reference to file in sandbox
- `version`: Reference to version in Versioning Service
- `thread`: Reference to thread entry
- `dataset`: Reference to database records
- `log`: Execution log reference

---

## 📜 CANONICAL RULES (NON-NEGOTIABLE)

### AGENT RULES

1. **Agent Runtime can ONLY be invoked by Orchestrator Service**
2. **Each job is bound to exactly ONE plan step**
3. **Agents cannot escalate privileges**
4. **Agents cannot change identity or context**
5. **Agents cannot see data outside their sandbox**
6. **Outputs are references only, never injected**

---

## ⚙️ EXECUTION FLOW

```
1. Orchestrator sends job request
2. Validate headers and plan step
3. Create sandbox filesystem
4. Inject input data (read-only)
5. Start job
6. Stream logs
7. Track token usage
8. Save outputs to /output
9. Mark job completed or failed
10. Report results to Orchestrator
11. Lock sandbox (read-only)
```

---

## 🤖 LLM EXECUTION ABSTRACTION

### LLM Provider Interface

**Supported Providers:**
- OpenAI
- Anthropic (Claude)
- Mistral
- Local (future)

### Each Call Must

- Enforce token limits
- Respect temperature settings
- Return usage metrics
- Timeout safely (max 5 minutes default)
- Handle rate limits gracefully

### Provider Configuration

```typescript
interface LLMProvider {
  name: string;
  apiKey: string;
  baseUrl?: string;
  timeout: number;
  retryConfig: {
    maxRetries: number;
    backoff: 'exponential' | 'linear';
  };
}
```

---

## 🌐 REST ENDPOINTS (INTERNAL ONLY)

**These endpoints are INTERNAL** — only accessible by Orchestrator Service.

```
POST   /internal/jobs               # Create and start job
GET    /internal/jobs/:id           # Get job status
GET    /internal/jobs/:id/logs      # Stream job logs
GET    /internal/jobs/:id/outputs   # Get job outputs
POST   /internal/jobs/:id/cancel    # Cancel running job
```

---

## 📋 DTO DEFINITIONS

### CreateJobDto

```typescript
export class CreateJobDto {
  @IsUUID()
  commandId: string;
  
  @IsUUID()
  planStepId: string;
  
  @IsUUID()
  agentId: string;
  
  @IsUUID()
  identityId: string;
  
  @IsUUID()
  contextId: string;
  
  @IsInt()
  @Min(1)
  tokenLimit: number;
  
  @IsObject()
  inputData: any; // Data to inject into /input
  
  @IsOptional()
  @IsObject()
  constraints?: {
    timeout?: number;
    memory?: number;
    network?: boolean;
  };
}
```

---

## 📡 EVENTS (PUB/SUB)

### Published Events

```typescript
AGENT.JOB.CREATED
AGENT.JOB.STARTED
AGENT.JOB.OUTPUT.GENERATED
AGENT.JOB.COMPLETED
AGENT.JOB.FAILED
AGENT.JOB.CANCELLED
```

### Event Payload

```typescript
{
  jobId: string;
  commandId: string;
  agentId: string;
  identityId: string;
  contextId: string;
  status: string;
  timestamp: string;
  metadata?: {
    tokensUsed?: number;
    outputs?: number;
    duration?: number;
  };
}
```

---

## 🚨 FAILURE & SAFETY

### If Job Fails

1. **Stop execution immediately**
2. **Preserve logs** (complete execution trace)
3. **Preserve outputs** (isolated, not integrated)
4. **Notify orchestrator** with failure details
5. **Require explicit user action** to retry

### Failure Categories

- **Timeout**: Job exceeded time limit
- **Token Limit**: Exceeded token budget
- **Memory Limit**: Out of memory
- **Rate Limit**: Provider rate limiting
- **Crash**: Agent code crashed
- **Policy Violation**: Attempted unauthorized action

---

## 🔒 SECURITY & ISOLATION

### Sandbox Security

- **No network access** unless explicitly allowed
- **No cross-job filesystem access**
- **No shared memory** between agents
- **Resource quotas enforced:**
  - CPU limit (e.g., 2 cores)
  - RAM limit (e.g., 4GB)
  - Token limit (from plan)
  - Timeout limit (from plan)

### Privilege Constraints

- **Agent cannot read:**
  - Other agents' sandboxes
  - User data outside /input
  - System files
  
- **Agent cannot write:**
  - Outside /work and /output
  - To user space directly
  - To system directories

---

## 📊 RESOURCE MONITORING

### Per-Job Tracking

```typescript
{
  cpuUsage: number;      // % of allocated CPU
  memoryUsage: number;   // MB used
  tokensUsed: number;    // LLM tokens consumed
  duration: number;      // milliseconds
  filesCreated: number;  // count in /output
  logsSize: number;      // bytes
}
```

### Alerts

- Token usage > 90% of limit
- Memory usage > 80% of limit
- Execution time > 80% of timeout
- Rate limit approaching

---

## 🎯 SUCCESS CRITERIA

- ✅ All jobs execute in isolated sandboxes
- ✅ Zero cross-job data leaks
- ✅ Resource limits are enforced
- ✅ Outputs never auto-integrate
- ✅ Complete execution logs preserved
- ✅ Only Orchestrator can invoke

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** Orchestrator Service  
**Complexity:** Very High  
**LOC Estimate:** ~6,000 lines  
**Implementation Time:** 8-10 days  

---

## 🚀 IMPLEMENTATION CHECKLIST

- [ ] Set up NestJS module structure
- [ ] Create PostgreSQL schema
- [ ] Implement sandbox filesystem management
- [ ] Create LLM provider abstraction
- [ ] Implement OpenAI provider
- [ ] Implement Anthropic provider
- [ ] Add resource monitoring
- [ ] Implement token tracking
- [ ] Add timeout handling
- [ ] Create log streaming
- [ ] Implement output collection
- [ ] Add failure handling
- [ ] Set up event publishing
- [ ] Write unit tests (80% coverage)
- [ ] Write integration tests
- [ ] Security audit
- [ ] Performance testing
- [ ] Deploy to staging

---

## 🔐 FINAL RULE

**Agents WORK.**  
**They do NOT DECIDE.**  
**They do NOT INTEGRATE.**  
**They do NOT GOVERN.**

**THE AGENT RUNTIME IS A SAFE ENGINE, NOT A BRAIN.**

---

**END OF IMPLEMENTATION BLOCK**
