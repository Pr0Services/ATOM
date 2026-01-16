# CHE·NU™ — SKILL & TOOL REGISTRY SERVICE
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**The Skill & Tool Registry is the SINGLE SOURCE OF TRUTH for:**

- **WHAT** an agent can do (skills)
- **WITH WHICH** underlying implementations (tools)
- **UNDER WHICH** constraints (policies, budgets, scopes)
- **IN WHICH** spheres (activation matrix)

**It decouples orchestration planning from concrete implementations.**

---

## 🔐 MANDATORY HEADERS

Every request **MUST** include:
- `x-identity-id`
- `x-context-id`

**Administrative writes require Architect Mode** (policy-governance).

---

## 🧠 CORE CONCEPTS

### SKILL
High-level capability with stable semantic contract:
- Examples: "summarize_text", "extract_entities", "generate_pdf"
- Provider-agnostic
- Defines input/output schema (JSON Schema)
- Versioned

### TOOL
Concrete implementation of a skill:
- Examples: "anthropic/claude-3-haiku", "openai/gpt-4o-mini", "wkhtmltopdf"
- With runtime adapter
- Cost model
- Performance characteristics
- Availability status

### MAPPING
Skill → Tool relationship:
- One skill can map to many tools
- Selection logic: policy + cost + quality + availability
- Priority-based ordering

### SPHERE ACTIVATION
Defines which spheres can use a given skill:
- Per-sphere defaults
- Mode visibility (Discovery, Focus, Power, Architect)
- Enable/disable control

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Skills Table (SEMANTIC CAPABILITIES)

```sql
CREATE TABLE skills (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,      -- e.g., summarize_text
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  input_schema JSONB NOT NULL,    -- JSON Schema describing inputs
  output_schema JSONB NOT NULL,   -- JSON Schema describing outputs
  level TEXT NOT NULL DEFAULT 'L0' 
    CHECK (level IN ('L0','L1','L2')),
  status TEXT NOT NULL DEFAULT 'validated' 
    CHECK (status IN (
      'experimental',
      'tested',
      'validated',
      'deprecated'
    )),
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_skills_code ON skills(code);
CREATE INDEX idx_skills_level ON skills(level);
CREATE INDEX idx_skills_status ON skills(status);
```

**SKILL PROPERTIES:**
- `code`: Unique identifier (snake_case)
- `title`: Human-readable name
- `description`: What the skill does
- `input_schema`: JSON Schema for inputs
- `output_schema`: JSON Schema for outputs
- `level`: Required agent level (L0/L1/L2)
- `status`: Maturity level

**SKILL STATUSES:**
- `experimental`: Under development
- `tested`: Tested but not production-ready
- `validated`: Production-ready
- `deprecated`: No longer recommended

---

### Tools Table (IMPLEMENTATIONS)

```sql
CREATE TABLE tools (
  id UUID PRIMARY KEY,
  provider TEXT NOT NULL,         -- openai|anthropic|mistral|internal|binary
  name TEXT NOT NULL,             -- gpt-4o, claude-3-haiku, wkhtmltopdf
  version TEXT,
  type TEXT NOT NULL 
    CHECK (type IN (
      'llm',
      'function',
      'binary',
      'service'
    )),
  cost_model JSONB NOT NULL,      
    -- { per_token_in, per_token_out, per_call, per_minute, currency }
  constraints JSONB DEFAULT '{}', 
    -- { max_tokens, timeout_ms, memory_mb, network: true|false, ... }
  metadata JSONB DEFAULT '{}',    
    -- freeform (quality score, latency, region, etc.)
  status TEXT NOT NULL DEFAULT 'available' 
    CHECK (status IN (
      'available',
      'limited',
      'disabled'
    )),
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_tools_provider ON tools(provider);
CREATE INDEX idx_tools_type ON tools(type);
CREATE INDEX idx_tools_status ON tools(status);
```

**TOOL TYPES:**
- `llm`: Large Language Model
- `function`: Code function/API
- `binary`: Executable binary
- `service`: External service/API

**COST MODEL EXAMPLE:**
```json
{
  "per_token_in": 0.00003,
  "per_token_out": 0.00006,
  "per_call": 0.001,
  "currency": "USD"
}
```

**CONSTRAINTS EXAMPLE:**
```json
{
  "max_tokens": 4096,
  "timeout_ms": 30000,
  "memory_mb": 512,
  "network": true,
  "rate_limit": {
    "requests_per_minute": 60
  }
}
```

---

### Skill-Tool Mapping Table

```sql
CREATE TABLE skill_tool_map (
  id UUID PRIMARY KEY,
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
  priority INT NOT NULL DEFAULT 100,   -- lower = preferred
  policy JSONB DEFAULT '{}',           
    -- selection rules (modes, budgets, identity constraints)
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE(skill_id, tool_id)
);

CREATE INDEX idx_skilltool_skill ON skill_tool_map(skill_id);
CREATE INDEX idx_skilltool_tool ON skill_tool_map(tool_id);
CREATE INDEX idx_skilltool_priority ON skill_tool_map(priority);
```

**MAPPING PROPERTIES:**
- `priority`: Lower number = higher priority
- `policy`: Selection rules (JSON)
- `enabled`: Can be temporarily disabled

**POLICY EXAMPLE:**
```json
{
  "modes": ["focus", "power", "architect"],
  "max_budget_usd": 0.10,
  "identity_types": ["business", "organization"]
}
```

---

### Sphere Activation Matrix

```sql
CREATE TABLE skill_activation (
  id UUID PRIMARY KEY,
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  sphere TEXT NOT NULL,                
    -- personal|business|government|creative_studio|community|social_media|entertainment|my_team
  default_tool_id UUID NULL REFERENCES tools(id),
  mode_visibility TEXT NOT NULL DEFAULT 'focus' 
    CHECK (mode_visibility IN (
      'discovery',
      'focus',
      'power',
      'architect'
    )),
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE(skill_id, sphere)
);

CREATE INDEX idx_skill_activation_sphere ON skill_activation(sphere);
CREATE INDEX idx_skill_activation_skill ON skill_activation(skill_id);
```

**MODE VISIBILITY:**
- `discovery`: Visible in Discovery mode (beginner)
- `focus`: Visible in Focus mode (intermediate)
- `power`: Visible in Power mode (advanced)
- `architect`: Only visible in Architect mode (expert)

---

### Runtime Profiles Table (OPTIONAL)

```sql
CREATE TABLE runtime_profiles (
  id UUID PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,           
    -- e.g., "low_cost", "balanced", "high_quality"
  selection_policy JSONB NOT NULL,     
    -- ordering weights: { cost: 0.6, quality: 0.2, latency: 0.2 }
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
```

**PROFILE EXAMPLE:**
```json
{
  "cost": 0.6,
  "quality": 0.2,
  "latency": 0.2
}
```

---

## 📜 CANONICAL RULES (NON-NEGOTIABLE)

1. **Skills define the CONTRACT; Tools fulfill it**
2. **Orchestrator picks Tools via this service ONLY**
3. **Sphere activation is authoritative** (no sphere use if disabled)
4. **Agent level (L0/L1/L2) MUST be >= Skill level**
5. **Experimental skills NEVER run in production** without Architect approval
6. **Tool selection MUST respect:** policy-governance, permission-scope, budget-token

---

## 🔍 SELECTION ALGORITHM (HIGH-LEVEL)

### Given:
- `skill_code`
- Active sphere
- User mode
- Budget constraints
- Context/identity policy

### Steps:
1. Fetch Skill by code
   - Reject if status='deprecated'
   - Reject if activation disabled for sphere
2. List candidate Tools via `skill_tool_map` where `enabled=true`
3. Filter by:
   - Policy-governance
   - Permission-scope
   - Constraints (e.g., network=false)
4. Apply runtime profile OR priority ordering
5. Return ordered candidate list with estimated costs

---

## 🌐 REST ENDPOINTS (CANONICAL)

### Skills Management

```
POST   /v1/skills                    # Create skill (Architect only)
GET    /v1/skills                    # List all skills
GET    /v1/skills/:code              # Get skill details
PATCH  /v1/skills/:code              # Update skill (Architect only)
POST   /v1/skills/:code/deprecate    # Deprecate skill (Architect only)
```

### Tools Management

```
POST   /v1/tools                     # Register tool (Architect only)
GET    /v1/tools                     # List all tools
GET    /v1/tools/:id                 # Get tool details
PATCH  /v1/tools/:id                 # Update tool (Architect only)
POST   /v1/tools/:id/disable         # Disable tool
POST   /v1/tools/:id/enable          # Enable tool
```

### Mapping Management

```
POST   /v1/skills/:code/tools/:toolId/map     # Map skill to tool
PATCH  /v1/skills/:code/tools/:toolId         # Update mapping
DELETE /v1/skills/:code/tools/:toolId         # Unmap skill from tool
```

### Activation Management

```
POST   /v1/skills/:code/activation            # Create activation
GET    /v1/skills/:code/activation            # Get activations
PATCH  /v1/skills/:code/activation/:sphere    # Update activation
```

### Selection API (Used by Orchestrator)

```
POST   /v1/select
```

**Request Body:**
```json
{
  "skillCode": "summarize_text",
  "sphere": "business",
  "mode": "focus",
  "constraints": {
    "max_tokens": 4000,
    "network": false
  },
  "runtimeProfile": "low_cost",
  "budgetHint": {
    "max_usd": 0.05
  }
}
```

**Response:**
```json
{
  "skill": {
    "code": "summarize_text",
    "title": "Text Summarization",
    "level": "L0"
  },
  "candidates": [
    {
      "tool": {
        "id": "uuid",
        "provider": "anthropic",
        "name": "claude-3-haiku",
        "type": "llm"
      },
      "score": 0.82,
      "estimated": {
        "usd": 0.012,
        "tokens": 1200
      }
    },
    {
      "tool": {
        "id": "uuid",
        "provider": "openai",
        "name": "gpt-4o-mini",
        "type": "llm"
      },
      "score": 0.78,
      "estimated": {
        "usd": 0.015,
        "tokens": 1500
      }
    }
  ]
}
```

---

## 📋 DTO DEFINITIONS

### CreateSkillDto

```typescript
export class CreateSkillDto {
  @IsString()
  @Matches(/^[a-z0-9_]+$/)
  code: string; // snake_case
  
  @IsString()
  title: string;
  
  @IsString()
  description: string;
  
  @IsObject()
  inputSchema: any; // JSON Schema
  
  @IsObject()
  outputSchema: any; // JSON Schema
  
  @IsEnum(['L0', 'L1', 'L2'])
  level: string = 'L0';
  
  @IsEnum(['experimental', 'tested', 'validated'])
  status: string = 'tested';
}
```

### CreateToolDto

```typescript
export class CreateToolDto {
  @IsString()
  provider: string; // openai|anthropic|mistral|internal|binary
  
  @IsString()
  name: string;
  
  @IsOptional()
  @IsString()
  version?: string;
  
  @IsEnum(['llm', 'function', 'binary', 'service'])
  type: string;
  
  @IsObject()
  costModel: {
    per_token_in?: number;
    per_token_out?: number;
    per_call?: number;
    per_minute?: number;
    currency: string;
  };
  
  @IsOptional()
  @IsObject()
  constraints?: any;
  
  @IsOptional()
  @IsObject()
  metadata?: any;
}
```

---

## 📡 EVENTS (PUB/SUB)

### Published Events

```typescript
SKILL.CREATED
SKILL.UPDATED
SKILL.DEPRECATED
TOOL.REGISTERED
TOOL.UPDATED
TOOL.ENABLED
TOOL.DISABLED
SKILL.MAPPED.TOOL
SKILL.UNMAPPED.TOOL
ACTIVATION.CREATED
ACTIVATION.UPDATED
```

### Event Payload

```typescript
{
  skillCode?: string;
  toolId?: string;
  sphere?: string;
  identityId: string;
  contextId: string;
  timestamp: string;
  action: string;
}
```

---

## 🔒 GOVERNANCE & SAFETY

### Architect Mode Required For:
- Creating skills
- Mapping tools
- Changing activation
- Deprecating skills
- Registering tools

### Registry Responsibilities:
- **NEVER triggers execution** (only informs selection)
- **Returns NO CANDIDATE** if selection is ambiguous or unsafe
- **Enforces sphere boundaries**
- **Validates budget hints** (advisory)

### Budget Authority:
- Registry provides **estimates only**
- Budget & Governance Service is **authoritative at runtime**

---

## 🚨 FAILURE MODES

### Error Responses

- **404 (Not Found)**: Skill does not exist
- **409 (Conflict)**: Skill deprecated or disabled
- **412 (Precondition Failed)**: No tool candidates after filters
- **403 (Forbidden)**: Policy/permission violation
- **422 (Unprocessable)**: Budget hint exceeded (requires approval)

---

## 🎯 SUCCESS CRITERIA

- ✅ All skills have stable contracts (schemas)
- ✅ Tool selection respects policies & budgets
- ✅ Sphere activation is enforced
- ✅ Only Architect can modify registry
- ✅ Complete audit trail of changes
- ✅ Selection is deterministic given same inputs

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** Identity & Context Service  
**Complexity:** High  
**LOC Estimate:** ~4,500 lines  
**Implementation Time:** 6-8 days  

---

## 🚀 IMPLEMENTATION CHECKLIST

- [ ] Set up NestJS module structure
- [ ] Create PostgreSQL schema
- [ ] Implement skill CRUD endpoints
- [ ] Implement tool CRUD endpoints
- [ ] Create mapping logic
- [ ] Implement sphere activation
- [ ] Build selection algorithm
- [ ] Add cost estimation
- [ ] Create runtime profiles
- [ ] Add policy enforcement
- [ ] Set up event publishing
- [ ] Integrate with Audit Service
- [ ] Write unit tests (85% coverage)
- [ ] Write integration tests
- [ ] Performance testing
- [ ] Deploy to staging

---

## 🔐 FINAL RULE

**If a capability cannot be:**
- Described
- Constrained
- Mapped to a governed implementation

**IT MUST NOT BE USED.**

**THE REGISTRY DEFINES WHAT IS POSSIBLE.**  
**ORCHESTRATION DECIDES WHEN.**  
**AGENTS EXECUTE HOW.**

---

**END OF IMPLEMENTATION BLOCK**
