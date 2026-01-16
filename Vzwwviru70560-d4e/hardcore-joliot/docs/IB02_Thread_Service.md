# CHE·NU™ — THREAD SERVICE (.chenu)
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**The Thread Service manages .chenu threads as the SINGLE UNIT OF TRUTH.**

A thread:
- Belongs to exactly ONE sphere
- Belongs to exactly ONE context
- Never merges with another thread
- May reference other threads
- Records decisions immutably

**Threads connect meaning.**  
**They never mix contexts.**

---

## 🔐 MANDATORY HEADERS

Every request **MUST** include:
- `x-identity-id`
- `x-context-id`

**Requests without both MUST be rejected.**

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Threads Table (CORE)

```sql
CREATE TABLE threads (
  id UUID PRIMARY KEY,
  identity_id UUID NOT NULL,
  context_id UUID NOT NULL,
  sphere TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open'
    CHECK (status IN ('open','active','decision_recorded','closed','archived')),
  intent TEXT DEFAULT NULL,
  topic_tags TEXT[] DEFAULT '{}',
  geo JSONB DEFAULT NULL,
  visibility TEXT NOT NULL DEFAULT 'private'
    CHECK (visibility IN ('private','shared','public')),
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_threads_identity ON threads(identity_id);
CREATE INDEX idx_threads_context ON threads(context_id);
CREATE INDEX idx_threads_sphere ON threads(sphere);
CREATE INDEX idx_threads_visibility ON threads(visibility);
CREATE INDEX idx_threads_tags ON threads USING GIN (topic_tags);
```

**THREAD PROPERTIES:**
- `sphere`: Must match active context sphere
- `status`: Lifecycle state (open → closed → archived)
- `intent`: Purpose classification (debate, request, announcement, collaboration)
- `topic_tags`: Semantic categorization
- `geo`: Optional geographic context (country, region, city, coordinates)
- `visibility`: Sharing scope (private, shared within context, public)

---

### Thread Entries Table (MESSAGES/CONTENT)

```sql
CREATE TABLE thread_entries (
  id UUID PRIMARY KEY,
  thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  author_type TEXT NOT NULL CHECK (author_type IN ('user','agent')),
  author_id UUID,
  content TEXT NOT NULL,
  content_format TEXT NOT NULL DEFAULT 'text'
    CHECK (content_format IN ('text','markdown','json')),
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_entries_thread ON thread_entries(thread_id);
```

**ENTRY RULES:**
- `author_type`: Distinguishes user vs agent contributions
- `author_id`: References identity or agent ID
- `content_format`: Allows rich formatting and structured data
- Entries are append-only (no updates/deletes)

---

### Thread Links Table (REFERENCE GRAPH)

```sql
CREATE TABLE thread_links (
  id UUID PRIMARY KEY,
  from_thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  to_thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  link_type TEXT NOT NULL
    CHECK (link_type IN ('reference','related','depends_on','duplicates','parent','child')),
  note TEXT DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE(from_thread_id, to_thread_id, link_type)
);
```

**LINK TYPES:**
- `reference`: General citation
- `related`: Thematic connection
- `depends_on`: Prerequisite relationship
- `duplicates`: Marks duplicate threads
- `parent/child`: Hierarchical organization

---

### Thread Decisions Table (IMMUTABLE)

```sql
CREATE TABLE thread_decisions (
  id UUID PRIMARY KEY,
  thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
  decision_title TEXT NOT NULL,
  decision_text TEXT NOT NULL,
  decided_by UUID NOT NULL,
  referenced_version_ids UUID[] DEFAULT '{}',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_decisions_thread ON thread_decisions(thread_id);
```

**DECISION RULES:**
- Decisions are **APPEND-ONLY**
- Editing or deleting decisions is **FORBIDDEN**
- Decisions may reference specific version IDs (from Versioning Service)
- Once a decision is recorded, thread status can transition to `decision_recorded`

---

## 📜 CANONICAL RULES (NON-NEGOTIABLE)

### THREAD RULES

1. **A thread belongs to exactly ONE sphere.**
2. **Sphere MUST match the active context sphere.**
3. **A thread never merges with another thread.**
4. **Cross-sphere access is READ-ONLY unless explicitly shared.**
5. **Decisions are APPEND-ONLY.**
6. **Editing or deleting decisions is forbidden.**
7. **Closing or archiving a thread makes it READ-ONLY.**

---

## 🌐 REST ENDPOINTS (CANONICAL)

```
POST   /v1/threads                    # Create new thread
GET    /v1/threads/:id                # Get thread details
PATCH  /v1/threads/:id                # Update thread metadata
GET    /v1/threads                    # List threads (filtered)

POST   /v1/threads/:id/entries        # Add entry to thread
GET    /v1/threads/:id/entries        # Get thread entries

POST   /v1/threads/:id/link           # Link to another thread
GET    /v1/threads/:id/links          # Get thread links

POST   /v1/threads/:id/decision       # Record decision
GET    /v1/threads/:id/decisions      # Get thread decisions
```

---

## 📋 DTO DEFINITIONS

### CreateThreadDto

```typescript
export class CreateThreadDto {
  @IsString()
  @IsNotEmpty()
  title: string;
  
  @IsString()
  @IsNotEmpty()
  sphere: string; // Must match context sphere
  
  @IsEnum(['private', 'shared', 'public'])
  visibility: string = 'private';
  
  @IsOptional()
  @IsEnum(['debate', 'request', 'announcement', 'collaboration'])
  intent?: string;
  
  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  topicTags?: string[];
  
  @IsOptional()
  @IsObject()
  geo?: {
    country?: string;
    region?: string;
    city?: string;
    lat?: number;
    lng?: number;
  };
}
```

---

### LinkThreadDto

```typescript
export class LinkThreadDto {
  @IsUUID()
  toThreadId: string;
  
  @IsEnum(['reference', 'related', 'depends_on', 'duplicates', 'parent', 'child'])
  linkType: string;
  
  @IsOptional()
  @IsString()
  note?: string;
}
```

---

### RecordDecisionDto

```typescript
export class RecordDecisionDto {
  @IsString()
  @IsNotEmpty()
  decisionTitle: string;
  
  @IsString()
  @IsNotEmpty()
  decisionText: string;
  
  @IsOptional()
  @IsArray()
  @IsUUID('4', { each: true })
  referencedVersionIds?: string[];
}
```

---

## ♻️ LIFECYCLE ENFORCEMENT

### Thread Status Flow

```
open → active → decision_recorded → closed → archived
```

**Invalid transitions MUST be rejected.**

### Status Definitions

- **open**: Thread created, awaiting activity
- **active**: Thread has active discussion/work
- **decision_recorded**: A decision has been recorded
- **closed**: Thread is complete, READ-ONLY
- **archived**: Thread is historical, READ-ONLY

---

## 📡 EVENTS (PUB/SUB)

### Published Events

```typescript
THREAD.CREATED
THREAD.UPDATED
THREAD.ENTRY.ADDED
THREAD.LINK.CREATED
THREAD.DECISION.RECORDED
```

### Event Payload

```typescript
{
  threadId: string;
  identityId: string;
  contextId: string;
  sphere: string;
  timestamp: string;
  action: string;
  metadata?: any;
}
```

---

## 📝 AUDIT & VERSIONING

### Audit Integration

- **All write actions** are logged to Audit Log Service
- Includes: who, what, when, where (sphere/context)
- Immutable audit trail for compliance

### Versioning Integration

- **Decisions may reference Versioning Service IDs**
- Links thread decisions to specific document/note versions
- Enables traceability from decision to artifact

### History

- **Thread history is immutable and reviewable**
- Users can view complete thread evolution
- Agents can analyze decision patterns

---

## 🚨 VALIDATION & SECURITY

### Pre-Creation Validation

```typescript
// Validate sphere matches context
if (dto.sphere !== activeContext.sphere) {
  throw new ForbiddenException('Sphere mismatch with active context');
}

// Validate identity has permission
if (!hasPermission(identityId, contextId, 'thread.create')) {
  throw new ForbiddenException('No permission to create thread');
}
```

### Cross-Sphere Access

```typescript
// Read-only access for threads in different spheres
if (thread.sphere !== activeContext.sphere) {
  if (thread.visibility === 'private') {
    throw new ForbiddenException('Thread not accessible');
  }
  return { ...thread, readonly: true };
}
```

---

## 🎯 SUCCESS CRITERIA

- ✅ Threads never mix contexts
- ✅ Decisions are immutable
- ✅ Thread links form valid graph (no cycles)
- ✅ Status transitions are enforced
- ✅ All modifications are audited
- ✅ Cross-sphere access is read-only unless shared

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** Identity & Context Service  
**Complexity:** High  
**LOC Estimate:** ~3,500 lines  
**Implementation Time:** 4-5 days  

---

## 🔜 INTEGRATION POINTS

### Upstream Dependencies
- **Identity & Context Service**: Validates headers
- **Audit Log Service**: Records all actions

### Downstream Consumers
- **Orchestrator Service**: Uses threads for task tracking
- **Agent Runtime**: Logs agent interactions in threads
- **UI Components**: Displays threads per sphere
- **Versioning Service**: Links decisions to versions

---

## 🚀 IMPLEMENTATION CHECKLIST

- [ ] Set up NestJS module structure
- [ ] Create PostgreSQL schema
- [ ] Implement guards (identity/context validation)
- [ ] Create DTO classes with validation
- [ ] Implement CRUD endpoints
- [ ] Add lifecycle state machine
- [ ] Implement linking logic
- [ ] Add decision recording
- [ ] Set up event publishing
- [ ] Integrate with Audit Service
- [ ] Write unit tests (80% coverage)
- [ ] Write integration tests
- [ ] Deploy to staging
- [ ] Performance testing (1000+ threads)

---

## 🔐 FINAL RULE

**If a thread's context, sphere, or identity is ambiguous,  
THE THREAD MUST NOT BE CREATED OR MODIFIED.**

**THREADS ARE THE SPINE OF CHE·NU.**

---

**END OF IMPLEMENTATION BLOCK**
