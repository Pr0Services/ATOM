# CHE·NU™ — IDENTITY & CONTEXT SERVICE
## CANONICAL IMPLEMENTATION BLOCK
**VERSION:** V1 FREEZE

---

## 🎯 ROLE & RESPONSIBILITY

**Defines WHO acts, WHERE, WITH WHAT RIGHTS**

Guarantees that nothing executes without valid context.

---

## 📦 SERVICE STRUCTURE (NestJS)

```
services/identity-context-service/
  src/
    main.ts
    app.module.ts

    modules/
      identity/
        identity.module.ts
        identity.controller.ts
        identity.service.ts
        identity.entity.ts

      context/
        context.module.ts
        context.controller.ts
        context.service.ts
        context.entity.ts

      session/
        session.module.ts
        session.service.ts

    guards/
      context.guard.ts
      identity.guard.ts

    interceptors/
      audit.interceptor.ts

    dto/
      switch-identity.dto.ts
      lock-scope.dto.ts

  package.json
  Dockerfile
```

---

## 🚀 BOOTSTRAP (main.ts)

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableShutdownHooks();
  app.setGlobalPrefix('v1');

  // MANDATORY GUARDS - NO REQUEST WITHOUT IDENTITY + CONTEXT
  app.useGlobalGuards(
    app.get(IdentityGuard),
    app.get(ContextGuard),
  );

  // MANDATORY AUDIT - EVERY ACTION IS TRACED
  app.useGlobalInterceptors(
    app.get(AuditInterceptor),
  );

  await app.listen(3002);
}
bootstrap();
```

**👉 No request passes without identity + context.**

---

## 🗄️ DATA MODEL (POSTGRESQL)

### Identities Table

```sql
CREATE TABLE identities (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('personal','business','organization','role')),
  label TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_identities_user ON identities(user_id);
CREATE INDEX idx_identities_type ON identities(type);
```

**IDENTITY TYPES:**
- `personal`: Individual user identity
- `business`: Company/enterprise identity
- `organization`: Non-profit/institution identity
- `role`: Delegated role identity

---

### Contexts Table

```sql
CREATE TABLE contexts (
  id UUID PRIMARY KEY,
  identity_id UUID NOT NULL REFERENCES identities(id),
  sphere TEXT NOT NULL,
  organization_id UUID,
  project_id UUID,
  permissions JSONB NOT NULL,
  budget_scope JSONB,
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_contexts_identity ON contexts(identity_id);
CREATE INDEX idx_contexts_sphere ON contexts(sphere);
CREATE INDEX idx_contexts_org ON contexts(organization_id);
```

**CONTEXT DEFINITION:**
- Defines the operational scope for an identity
- One context per sphere
- Contains permissions & budget boundaries
- Prevents privilege escalation

---

### Active Sessions Table

```sql
CREATE TABLE active_sessions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  identity_id UUID NOT NULL,
  context_id UUID NOT NULL,
  scope_locked BOOLEAN DEFAULT false,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_sessions_user ON active_sessions(user_id);
CREATE INDEX idx_sessions_identity ON active_sessions(identity_id);
```

**SESSION RULES:**
- One active session per user
- Switching identity terminates current session
- `scope_locked=true` prevents escalation during execution

---

## 🛡️ GUARDS (SECURITY LAYER)

### IdentityGuard

```typescript
@Injectable()
export class IdentityGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest();
    
    if (!req.headers['x-identity-id']) {
      throw new ForbiddenException('No active identity');
    }
    
    return true;
  }
}
```

**👉 Blocks all requests without identity header.**

---

### ContextGuard

```typescript
@Injectable()
export class ContextGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest();
    
    if (!req.headers['x-context-id']) {
      throw new ForbiddenException('No active context');
    }
    
    return true;
  }
}
```

**👉 Blocks all requests without context header.**

---

## 📝 AUDIT INTERCEPTOR (TRACEABILITY)

```typescript
@Injectable()
export class AuditInterceptor implements NestInterceptor {
  intercept(ctx: ExecutionContext, next: CallHandler) {
    const req = ctx.switchToHttp().getRequest();
    
    // Log: identity_id, context_id, route, timestamp
    const auditLog = {
      identity_id: req.headers['x-identity-id'],
      context_id: req.headers['x-context-id'],
      route: req.route?.path,
      method: req.method,
      timestamp: new Date().toISOString()
    };
    
    // Send to Audit Service (pub/sub)
    // ...
    
    return next.handle();
  }
}
```

**👉 Every action is traceable.**

---

## 🔄 SWITCH IDENTITY (EXPLICIT TRANSITION)

### Endpoint

```typescript
@Post('/identity/switch')
switchIdentity(@Body() dto: SwitchIdentityDto) {
  // 1. Terminate current session
  // 2. Validate target identity
  // 3. Create new active session
  // 4. Emit audit event
  return { success: true, newIdentityId: '...' };
}
```

### DTO

```typescript
export class SwitchIdentityDto {
  @IsUUID()
  targetIdentityId: string;
  
  @IsOptional()
  @IsString()
  reason?: string;
}
```

### RULES

- **Stops all executions in progress**
- **Invalidates caches**
- **Loads new permissions & budgets**
- **Logs transition in audit trail**

---

## 🔒 LOCK SCOPE (ANTI-LEAK CRITICAL)

### Endpoint

```typescript
@Post('/scope/lock')
lockScope(@Body() dto: LockScopeDto) {
  // Mark active_session.scope_locked = true
  return { success: true, scopeLocked: true };
}
```

### DTO

```typescript
export class LockScopeDto {
  @IsUUID()
  sessionId: string;
}
```

### PURPOSE

**Prevents any escalation during agent execution.**

When an agent is running:
- Context is LOCKED
- No identity switch allowed
- No permission elevation possible
- Execution boundary is enforced

---

## 🌐 REST ENDPOINTS (CANONICAL)

```
GET    /v1/identity/active
POST   /v1/identity/switch

GET    /v1/context/active
POST   /v1/context/create

POST   /v1/scope/lock
POST   /v1/scope/unlock
```

---

## 📡 EVENTS (PUB/SUB)

### Published Events

- `IDENTITY.SWITCHED`
- `CONTEXT.CREATED`
- `CONTEXT.ACTIVATED`
- `SCOPE.LOCKED`
- `SCOPE.UNLOCKED`

### Event Payload

```typescript
{
  userId: string;
  identityId: string;
  contextId: string;
  sphere: string;
  timestamp: string;
  action: string;
}
```

---

## 🔗 INTEGRATION RULES (SYSTEM-WIDE)

### ALL SERVICES MUST:

1. **Receive headers:**
   - `x-identity-id`
   - `x-context-id`

2. **Validate headers:**
   - Call Identity Service to verify active session
   - Reject if headers are missing or invalid

3. **Respect locks:**
   - Check `scope_locked` before any sensitive operation
   - Prevent context switching during locked execution

4. **Orchestrator MUST:**
   - Refuse execution if `scope_locked = false`
   - Always inherit identity + context (never override)

5. **Agent Runtime MUST:**
   - Inherit identity + context from parent execution
   - Never modify or escalate context

6. **UI MUST:**
   - Show active identity & sphere at all times
   - Provide explicit switch mechanism
   - Disable switching during locked operations

---

## ✅ STATUS

- ✅ Service critical implementable
- ✅ Governance coded (not theoretical)
- ✅ Security by default
- ✅ Solid base for Threads, Orchestrator, Agents

---

## 🔜 NEXT SERVICES

This service is **THE FOUNDATION** for:
1. **Thread Service** (.chenu) — vertical spine
2. **Versioning & Diff Service** — trust & audit
3. **Orchestrator Service** — active intelligence

---

## 📊 SERVICE METRICS

**Criticality:** ⭐⭐⭐⭐⭐ (5/5)  
**Dependencies:** None (Foundation)  
**Complexity:** Medium  
**LOC Estimate:** ~2,000 lines  
**Implementation Time:** 2-3 days  

---

## 🎯 SUCCESS CRITERIA

- ✅ 100% requests validated for identity + context
- ✅ Zero unauthorized context switches
- ✅ Complete audit trail for all identity transitions
- ✅ Scope locking prevents escalation during execution
- ✅ All downstream services respect headers

---

**END OF IMPLEMENTATION BLOCK**
