# CHE·NU™ — VERSIONING & DIFF SERVICE
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**The Versioning & Diff Service guarantees:**

- Append-only versions (no overwrites)
- Human-readable diff
- Rollback via new version creation
- Traceability (who/when/context)
- Clear separation: user vs agent changes

**Versioning is mandatory for trust.**  
**Nothing is silently modified.**

---

## 🔐 MANDATORY HEADERS

Every request **MUST** include:
- `x-identity-id`
- `x-context-id`

**Requests without both MUST be rejected.**

---

## 🧠 CORE CONCEPTS

### OBJECT
- A stable entity being versioned
- Types: document, note, dataset, thread snapshot, config, etc.
- Identified by: `object_id` (UUID) + `object_type`

### VERSION
- Immutable snapshot of an object at a point in time
- Identified by: `version_id` (UUID)
- Always append-only (no updates/deletes)

### DIFF
- Computed comparison between two versions
- Includes structural + semantic summary
- Machine-readable + human-friendly

### ROLLBACK
- Creates a **new version** that reverts content to a previous state
- Rollback **never deletes** any version
- Maintains complete history

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Versioned Objects Table (CATALOG)

```sql
CREATE TABLE versioned_objects (
  object_id UUID PRIMARY KEY,
  object_type TEXT NOT NULL, 
    -- document|note|table|thread|project|config|budget|etc
  identity_id UUID NOT NULL,
  context_id UUID NOT NULL,
  sphere TEXT NOT NULL,
  visibility TEXT NOT NULL DEFAULT 'private'
    CHECK (visibility IN ('private','shared','public')),
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_vobj_identity ON versioned_objects(identity_id);
CREATE INDEX idx_vobj_context ON versioned_objects(context_id);
CREATE INDEX idx_vobj_type ON versioned_objects(object_type);
```

**OBJECT CATALOG:**
- Registers all versionable entities
- Binds object to identity + context + sphere
- Defines visibility scope

---

### Object Versions Table (APPEND-ONLY)

```sql
CREATE TABLE object_versions (
  version_id UUID PRIMARY KEY,
  object_id UUID NOT NULL REFERENCES versioned_objects(object_id) ON DELETE CASCADE,
  parent_version_id UUID NULL, 
    -- allows linear chain; can support branching later
  state TEXT NOT NULL DEFAULT 'draft'
    CHECK (state IN ('draft','proposed','reviewed','approved','active','deprecated','archived')),
  author_type TEXT NOT NULL CHECK (author_type IN ('user','agent')),
  author_id UUID,
  change_type TEXT NOT NULL
    CHECK (change_type IN ('create','edit','agent_generate','agent_assist','rollback','merge','archive')),
  content_format TEXT NOT NULL DEFAULT 'json'
    CHECK (content_format IN ('text','markdown','json')),
  content_payload JSONB NOT NULL, 
    -- canonical content storage (for text store in {"text":""})
  content_hash TEXT NOT NULL,
  summary TEXT DEFAULT NULL, 
    -- short human-readable change summary
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_versions_object ON object_versions(object_id);
CREATE INDEX idx_versions_parent ON object_versions(parent_version_id);
CREATE INDEX idx_versions_state ON object_versions(state);
CREATE UNIQUE INDEX idx_versions_hash_unique ON object_versions(object_id, content_hash);
```

**VERSION PROPERTIES:**
- `parent_version_id`: Forms version chain (linear or branching)
- `state`: Workflow state (draft → approved → active)
- `author_type`: Distinguishes user vs agent modifications
- `change_type`: Categorizes the nature of change
- `content_payload`: JSONB allows flexible content storage
- `content_hash`: Deduplication (same content = same hash)
- `summary`: Optional human-readable change description

---

### Active Version Pointer

```sql
CREATE TABLE object_active_version (
  object_id UUID PRIMARY KEY REFERENCES versioned_objects(object_id) ON DELETE CASCADE,
  version_id UUID NOT NULL REFERENCES object_versions(version_id) ON DELETE RESTRICT,
  updated_at TIMESTAMP NOT NULL DEFAULT now()
);
```

**ACTIVE VERSION:**
- **One active version per object**
- Represents the "current" or "published" state
- Only user-approved versions can become active

---

### Diff Cache (OPTIONAL, FOR PERFORMANCE)

```sql
CREATE TABLE version_diffs (
  diff_id UUID PRIMARY KEY,
  object_id UUID NOT NULL REFERENCES versioned_objects(object_id) ON DELETE CASCADE,
  from_version_id UUID NOT NULL REFERENCES object_versions(version_id),
  to_version_id UUID NOT NULL REFERENCES object_versions(version_id),
  diff_payload JSONB NOT NULL, 
    -- { added:[], removed:[], changed:[] } or text patches
  semantic_summary TEXT DEFAULT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE(object_id, from_version_id, to_version_id)
);
```

**DIFF CACHE:**
- Pre-computed diffs for performance
- Optional (can compute on-the-fly)
- Stores both structural diff and semantic summary

---

## 📜 CANONICAL RULES (NON-NEGOTIABLE)

### VERSION RULES

1. **Versions are append-only** (no update/delete on `object_versions`)
2. **Only one ACTIVE version per object** (`object_active_version`)
3. **Any "edit" creates a NEW version** referencing `parent_version_id`
4. **Rollback creates a NEW version** with `change_type='rollback'`
5. **Agent-generated versions may never become ACTIVE without explicit user approval**

---

### STATE RULES

**Workflow States:**
- `draft` / `proposed` / `reviewed` / `approved`: Workflow states
- `active`: Current published/used version
- `deprecated`: Remains readable but superseded
- `archived`: Immutable and locked

**Transitions:**
```
draft → proposed → reviewed → approved → active
active → deprecated
active → archived
```

---

### CONTEXT RULES

- **Object `identity_id/context_id/sphere` define the governance boundary**
- **Cross-context versioning is forbidden** unless explicit share action exists
- **Agent versions default to `state='proposed'`** and cannot auto-activate

---

## 🌐 REST ENDPOINTS (CANONICAL)

### Objects

```
POST   /v1/objects                    # Create versionable object
GET    /v1/objects/:objectId          # Get object metadata
```

### Versions

```
POST   /v1/objects/:objectId/versions # Create new version
GET    /v1/objects/:objectId/versions # List versions
GET    /v1/versions/:versionId        # Get specific version
```

### Activate & Workflow

```
POST   /v1/objects/:objectId/activate # Set active version
POST   /v1/objects/:objectId/state    # Change version state
```

### Diff

```
GET    /v1/diff?objectId=&from=&to=   # Compute or retrieve diff
```

### Rollback

```
POST   /v1/objects/:objectId/rollback # Create rollback version
```

---

## 📋 DTO DEFINITIONS (MINIMAL)

### CreateObjectDto

```typescript
export class CreateObjectDto {
  @IsString()
  @IsNotEmpty()
  objectType: string; // document|note|table|thread|config|etc
  
  @IsString()
  @IsNotEmpty()
  sphere: string; // Must match active context sphere
  
  @IsEnum(['private', 'shared', 'public'])
  visibility: string = 'private';
}
```

---

### CreateVersionDto

```typescript
export class CreateVersionDto {
  @IsOptional()
  @IsUUID()
  parentVersionId?: string; // Required if object already has versions
  
  @IsEnum(['draft', 'proposed', 'reviewed', 'approved'])
  state: string = 'draft';
  
  @IsEnum(['user', 'agent'])
  authorType: string;
  
  @IsOptional()
  @IsUUID()
  authorId?: string;
  
  @IsEnum(['create', 'edit', 'agent_generate', 'agent_assist', 'rollback', 'merge', 'archive'])
  changeType: string;
  
  @IsEnum(['text', 'markdown', 'json'])
  contentFormat: string = 'json';
  
  @IsObject()
  @IsNotEmpty()
  contentPayload: any; // For text: { "text": "..." }
  
  @IsOptional()
  @IsString()
  summary?: string; // Human-readable change description
}
```

---

### ActivateVersionDto

```typescript
export class ActivateVersionDto {
  @IsUUID()
  versionId: string;
  
  @IsOptional()
  @IsBoolean()
  confirmAgentGenerated?: boolean; 
    // Required if authorType=agent
}
```

**RULE:** If `authorType=agent`, activation requires explicit confirmation flag.

---

### SetStateDto

```typescript
export class SetStateDto {
  @IsUUID()
  versionId: string;
  
  @IsEnum(['draft', 'proposed', 'reviewed', 'approved', 'active', 'deprecated', 'archived'])
  state: string;
}
```

---

### RollbackDto

```typescript
export class RollbackDto {
  @IsUUID()
  targetVersionId: string; // The version to revert to
  
  @IsOptional()
  @IsString()
  summary?: string; // Reason for rollback
}
```

---

## 🔍 DIFF BEHAVIOR (CANONICAL)

### Diff Output Structure

Diff output must be:
- **Human-readable**
- **Machine-usable**
- **Explainable**

**Minimum `diff_payload` structure:**

```json
{
  "type": "text|json",
  "added": [],
  "removed": [],
  "changed": [],
  "meta": {
    "from": "version_id_1",
    "to": "version_id_2"
  }
}
```

### Text Diff Example

```json
{
  "type": "text",
  "added": [
    { "line": 15, "text": "New paragraph added here" }
  ],
  "removed": [
    { "line": 8, "text": "Old text removed" }
  ],
  "changed": [
    {
      "line": 3,
      "from": "Original sentence",
      "to": "Modified sentence"
    }
  ],
  "meta": {
    "from": "v1-uuid",
    "to": "v2-uuid",
    "totalLines": 50
  }
}
```

### JSON Diff Example

```json
{
  "type": "json",
  "added": [
    { "path": "$.config.newFeature", "value": true }
  ],
  "removed": [
    { "path": "$.config.oldFeature" }
  ],
  "changed": [
    {
      "path": "$.settings.theme",
      "from": "light",
      "to": "dark"
    }
  ],
  "meta": {
    "from": "v1-uuid",
    "to": "v2-uuid"
  }
}
```

---

### Semantic Summary

**Optional field, can be generated by Nova:**

```typescript
semanticSummary: "Updated theme settings and added new feature flag. Removed deprecated configuration option."
```

---

## ✅ ACTIVATION & APPROVAL (GOVERNED)

### Activation Rules

1. **Only user-approved versions may become ACTIVE**
2. **Agent-generated content defaults to `state='proposed'`**
3. **Agent content cannot auto-activate**
4. **Activation always logs an audit event**
5. **Activation updates `object_active_version` table**

### Approval Workflow

```typescript
// Agent generates version
POST /v1/objects/{id}/versions
{
  authorType: "agent",
  state: "proposed",
  ...
}

// User reviews and approves
POST /v1/objects/{id}/state
{
  versionId: "agent-version-uuid",
  state: "approved"
}

// User activates (or rejects)
POST /v1/objects/{id}/activate
{
  versionId: "agent-version-uuid"
}
```

---

## 📡 EVENTS (PUB/SUB)

### Published Events

```typescript
VERSION.OBJECT.CREATED
VERSION.CREATED
VERSION.STATE.CHANGED
VERSION.ACTIVATED
VERSION.DIFF.GENERATED
VERSION.ROLLBACK.CREATED
```

### Event Payload

```typescript
{
  objectId: string;
  versionId: string;
  identityId: string;
  contextId: string;
  sphere: string;
  timestamp: string;
  action: string;
  metadata?: any;
}
```

---

## 🚨 FAILURE & SAFETY

### Rejection Conditions

If any of the following occur:
- `identity/context` headers missing
- `sphere` mismatch with active context
- Invalid `parent` chain (broken lineage)
- Attempt to modify existing version rows

**THEN:**
- Reject request
- Log attempt to Audit Service
- Return governed error response

---

## 🔐 ROLLBACK MECHANICS

### How Rollback Works

1. **User selects target version** (version to revert to)
2. **System creates NEW version:**
   - `parent_version_id`: Current active version
   - `change_type`: `'rollback'`
   - `content_payload`: Copy of target version content
   - `summary`: "Rollback to version {target_version_id}"
3. **New version goes through approval** (if needed)
4. **New version can be activated**
5. **Complete history is preserved**

### Example Rollback Flow

```
v1 (active) → v2 (buggy) → v3 (rollback to v1)
                              ↑
                     copies content from v1
```

**Result:** v3 becomes active, v2 remains in history but deprecated.

---

## 🎯 SUCCESS CRITERIA

- ✅ All changes are versioned and traceable
- ✅ No silent modifications (all tracked)
- ✅ Agent changes require user approval before activation
- ✅ Rollback creates new version (history preserved)
- ✅ Diff is human-readable and machine-usable
- ✅ Complete audit trail for all versions

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** Identity & Context Service  
**Complexity:** High  
**LOC Estimate:** ~4,000 lines  
**Implementation Time:** 5-6 days  

---

## 🔜 INTEGRATION POINTS

### Upstream Dependencies
- **Identity & Context Service**: Validates headers
- **Audit Log Service**: Records all versioning actions

### Downstream Consumers
- **Thread Service**: References versions in decisions
- **Note Service**: Versions all note content
- **Document Service**: Versions documents
- **Agent Runtime**: Creates proposed versions
- **UI Components**: Displays version history, diffs, rollback

---

## 🚀 IMPLEMENTATION CHECKLIST

- [ ] Set up NestJS module structure
- [ ] Create PostgreSQL schema with indexes
- [ ] Implement version creation logic
- [ ] Add content hashing for deduplication
- [ ] Implement state machine transitions
- [ ] Create diff computation engine
- [ ] Add rollback mechanism
- [ ] Implement activation workflow
- [ ] Set up event publishing
- [ ] Integrate with Audit Service
- [ ] Write unit tests (85% coverage)
- [ ] Write integration tests
- [ ] Performance testing (10,000+ versions)
- [ ] Deploy to staging

---

## 🔐 FINAL RULE

**If a change cannot be compared, traced, and rolled back,  
IT MUST NOT BE APPLIED.**

**VERSIONING IS THE MEMORY OF CHE·NU.**

---

**END OF IMPLEMENTATION BLOCK**
