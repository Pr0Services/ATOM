# SKYVERN MASTER PLAN — AT·OM Infrastructure Automation
## Version 1.0 | Agent-Readable Technical Directives

---

## METADATA
```json
{
  "project": "AT·OM (L'Arche des Résonances Universelles)",
  "codename": "CHE-NU",
  "version": "4.0.0",
  "last_updated": "2026-01-27",
  "automation_agent": "Skyvern",
  "human_operator": "Jonathan Rodrigue (SOUVERAIN)"
}
```

---

## SECTION 1: INFRASTRUCTURE MANIFESTE

### 1.1 Component Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AT·OM INFRASTRUCTURE MAP                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  COMPONENT          │ PLATFORM        │ URL/IDENTIFIER                      │
│  ──────────────────────────────────────────────────────────────────────────│
│  Frontend (React)   │ VERCEL          │ atom-sovereign                      │
│  Backend (FastAPI)  │ DIGITALOCEAN    │ sea-turtle-app-n4vsa               │
│  Database (Primary) │ SUPABASE        │ vzbrhovthpihrhdbbjud               │
│  Database (Backup)  │ DIGITALOCEAN    │ db-postgresql-nyc9                 │
│  Blockchain         │ HEDERA          │ Testnet → 0.0.7730446              │
│  CDN/Assets         │ VERCEL          │ Static via React build             │
│  Real-time          │ SUPABASE        │ WebSocket channels                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Deployment Architecture

```yaml
# DEPLOYMENT FLOW
production:
  frontend:
    platform: vercel
    project_name: atom-sovereign
    build_command: "cd ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app && npm install && npm run build"
    output_dir: "ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/build"
    region: iad1
    auto_deploy: true
    branch: main

  backend:
    platform: digitalocean_app_platform
    app_name: sea-turtle-app-n4vsa
    region: nyc9
    port: 8000
    health_endpoint: /api/v2/health

  database:
    primary:
      platform: supabase
      project_ref: vzbrhovthpihrhdbbjud
      type: postgresql
      rls_enabled: true
    backup:
      platform: digitalocean_managed_db
      cluster: db-postgresql-nyc9

  blockchain:
    network: hedera_testnet
    token_id: "0.0.7730446"
    operator_account: "0.0.7702951"
```

### 1.3 Source Code Locations

| Component | Repository Path | Purpose |
|-----------|-----------------|---------|
| Frontend App | `ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/` | React 18 SPA |
| Backend API | `Vzwwviru70560-d4e/hardcore-joliot/backend/` | FastAPI Server |
| Hedera Service | `services/hedera/` | Token Operations |
| Database Scripts | `services/database/` | SQL Migrations |
| Vercel Config | `/vercel.json` | Deployment Rules |

---

## SECTION 2: SECRETS MAPPING

### 2.1 Environment Variable Registry

**IMPORTANT:** Never store actual values in this file. Reference locations only.

```yaml
# SECRET SOURCES AND DESTINATIONS
secrets_registry:

  # SUPABASE CREDENTIALS
  SUPABASE_URL:
    source: supabase_dashboard
    path: "Settings > API > Project URL"
    inject_to:
      - vercel: "REACT_APP_SUPABASE_URL"
      - digitalocean: "SUPABASE_URL"
    format: "https://{project_ref}.supabase.co"

  SUPABASE_ANON_KEY:
    source: supabase_dashboard
    path: "Settings > API > Project API Keys > anon/public"
    inject_to:
      - vercel: "REACT_APP_SUPABASE_ANON_KEY"
    security: public_safe

  SUPABASE_SERVICE_ROLE_KEY:
    source: supabase_dashboard
    path: "Settings > API > Project API Keys > service_role"
    inject_to:
      - digitalocean: "SUPABASE_SERVICE_ROLE_KEY"
    security: CRITICAL_NEVER_EXPOSE_CLIENT

  # HEDERA CREDENTIALS
  HEDERA_OPERATOR_ID:
    source: hedera_portal
    path: "Account > Account ID"
    inject_to:
      - digitalocean: "HEDERA_OPERATOR_ID"
    format: "0.0.XXXXXXX"

  HEDERA_OPERATOR_KEY:
    source: hedera_portal
    path: "Account > Private Key (ED25519)"
    inject_to:
      - digitalocean: "HEDERA_OPERATOR_KEY"
    security: CRITICAL_PRIVATE_KEY

  HEDERA_TOKEN_ID:
    source: hedera_portal
    path: "Token > Token ID (ZAMA)"
    inject_to:
      - vercel: "REACT_APP_HEDERA_TOKEN_ID"
      - digitalocean: "HEDERA_TOKEN_ID"
    format: "0.0.XXXXXXX"

  # AUTHENTICATION
  JWT_SECRET_KEY:
    source: generate_uuid_v4
    inject_to:
      - digitalocean: "JWT_SECRET_KEY"
    security: CRITICAL_GENERATE_NEW

  # AI PROVIDERS (Optional)
  ANTHROPIC_API_KEY:
    source: anthropic_console
    path: "API Keys"
    inject_to:
      - digitalocean: "ANTHROPIC_API_KEY"
    security: CRITICAL_API_KEY

  OPENAI_API_KEY:
    source: openai_platform
    path: "API Keys"
    inject_to:
      - digitalocean: "OPENAI_API_KEY"
    security: CRITICAL_API_KEY
```

### 2.2 Platform-Specific Injection Points

#### VERCEL Environment Variables
```
Location: vercel.com/[team]/atom-sovereign/settings/environment-variables

REQUIRED:
├── REACT_APP_SUPABASE_URL
├── REACT_APP_SUPABASE_ANON_KEY
├── REACT_APP_HEDERA_TOKEN_ID
├── REACT_APP_HEDERA_NETWORK          (value: "testnet" or "mainnet")
└── REACT_APP_ATOM_* (sacred frequencies - non-secret)

OPTIONAL:
├── REACT_APP_FREQUENCY               (default: 999)
├── REACT_APP_HEARTBEAT               (default: 444)
└── REACT_APP_PHI                     (default: 1.6180339887498949)
```

#### DIGITALOCEAN Environment Variables
```
Location: cloud.digitalocean.com/apps/[app-id]/settings/app

REQUIRED:
├── SUPABASE_URL
├── SUPABASE_SERVICE_ROLE_KEY
├── DATABASE_URL                      (DigitalOcean PostgreSQL connection string)
├── HEDERA_OPERATOR_ID
├── HEDERA_OPERATOR_KEY
├── JWT_SECRET_KEY
├── ENV                               (value: "production")
├── DEBUG                             (value: "false")
└── HOST                              (value: "0.0.0.0")

OPTIONAL:
├── ANTHROPIC_API_KEY
├── OPENAI_API_KEY
└── REDIS_URL
```

---

## SECTION 3: DNS NAMING RULES

### 3.1 Domain Structure

```yaml
# DNS ARCHITECTURE
domain:
  primary: "atom-arche.com"  # OR your chosen domain

  subdomains:
    # Production
    root:
      record: "@"
      type: A
      value: "76.76.21.21"  # Vercel
      purpose: "Main frontend"

    www:
      record: "www"
      type: CNAME
      value: "cname.vercel-dns.com"
      purpose: "WWW redirect"

    api:
      record: "api"
      type: CNAME
      value: "sea-turtle-app-n4vsa.ondigitalocean.app"
      purpose: "Backend API"

    # Future expansion
    docs:
      record: "docs"
      type: CNAME
      value: "cname.vercel-dns.com"
      purpose: "Documentation site"

    testnet:
      record: "testnet"
      type: CNAME
      value: "cname.vercel-dns.com"
      purpose: "Staging environment"
```

### 3.2 DNS Configuration Steps

```bash
# STEP-BY-STEP DNS SETUP

# 1. Add domain to Vercel
vercel domains add atom-arche.com

# 2. Configure DNS at registrar:
#    Type    Name    Value                       TTL
#    A       @       76.76.21.21                 300
#    CNAME   www     cname.vercel-dns.com        300
#    CNAME   api     sea-turtle-app-n4vsa...     300

# 3. Verify SSL certificate (automatic via Vercel)
vercel domains verify atom-arche.com

# 4. Update backend CORS
# In DigitalOcean, add to CORS_ORIGINS:
# "https://atom-arche.com,https://www.atom-arche.com"
```

### 3.3 Current URLs (Pre-Domain)

| Service | Current URL | Future URL |
|---------|-------------|------------|
| Frontend | atom-arche.vercel.app | atom-arche.com |
| Backend | sea-turtle-app-n4vsa.ondigitalocean.app | api.atom-arche.com |
| Supabase | vzbrhovthpihrhdbbjud.supabase.co | (keep as-is) |

---

## SECTION 4: VALIDATION PROTOCOL

### 4.1 Post-Connection Test Checklist

```yaml
# AUTOMATED VALIDATION TESTS
# Run after each service connection

tests:

  # TEST 1: Vercel Frontend
  vercel_frontend:
    name: "Frontend Accessibility"
    method: HTTP_GET
    url: "https://{domain}/"
    expected:
      status_code: 200
      content_contains: "AT·OM"
    timeout: 10s

  # TEST 2: Backend Health
  backend_health:
    name: "Backend API Health"
    method: HTTP_GET
    url: "https://{api_domain}/api/v2/health"
    expected:
      status_code: 200
      json_contains:
        status: "healthy"
    timeout: 15s

  # TEST 3: Supabase Connection
  supabase_connection:
    name: "Database Connectivity"
    method: SUPABASE_QUERY
    query: "SELECT 1"
    expected:
      success: true
    timeout: 5s

  # TEST 4: Supabase Auth
  supabase_auth:
    name: "Authentication Service"
    method: HTTP_POST
    url: "https://{supabase_url}/auth/v1/health"
    headers:
      apikey: "{SUPABASE_ANON_KEY}"
    expected:
      status_code: 200
    timeout: 5s

  # TEST 5: Realtime
  supabase_realtime:
    name: "Realtime WebSocket"
    method: WEBSOCKET_CONNECT
    url: "wss://{supabase_url}/realtime/v1/websocket"
    expected:
      connection: established
    timeout: 10s

  # TEST 6: Hedera Connection
  hedera_connection:
    name: "Blockchain Connectivity"
    method: HEDERA_QUERY
    network: testnet
    query: "account_balance"
    account: "{HEDERA_OPERATOR_ID}"
    expected:
      success: true
      balance_exists: true
    timeout: 15s

  # TEST 7: API Proxy
  api_proxy:
    name: "Vercel → DigitalOcean Proxy"
    method: HTTP_GET
    url: "https://{domain}/api/health"
    expected:
      status_code: 200
    timeout: 10s

  # TEST 8: CORS Verification
  cors_check:
    name: "CORS Headers Present"
    method: HTTP_OPTIONS
    url: "https://{api_domain}/api/v2/health"
    headers:
      Origin: "https://{domain}"
    expected:
      headers_contains:
        - "Access-Control-Allow-Origin"
    timeout: 5s
```

### 4.2 Database Migration Validation

```yaml
# SQL MIGRATION TESTS
# Run after executing each SQL script

database_validation:

  after_grid_tables:
    queries:
      - name: "grid_nodes exists"
        sql: "SELECT COUNT(*) FROM grid_nodes"
        expected: "no error"
      - name: "grid_sectors seeded"
        sql: "SELECT COUNT(*) FROM grid_sectors"
        expected: "result >= 12"
      - name: "grid functions exist"
        sql: "SELECT routine_name FROM information_schema.routines WHERE routine_name = 'create_grid_node'"
        expected: "result count = 1"

  after_founder_features:
    queries:
      - name: "profiles.role column"
        sql: "SELECT column_name FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'role'"
        expected: "result count = 1"
      - name: "underground_videos exists"
        sql: "SELECT COUNT(*) FROM underground_videos"
        expected: "no error"
      - name: "activity_feed exists"
        sql: "SELECT COUNT(*) FROM activity_feed"
        expected: "no error"

  after_agents_tables:
    queries:
      - name: "agents seeded"
        sql: "SELECT COUNT(*) FROM agents"
        expected: "result >= 3"
      - name: "agent_instances exists"
        sql: "SELECT COUNT(*) FROM agent_instances"
        expected: "no error"

  after_adaptive_agents:
    queries:
      - name: "adaptive agents seeded"
        sql: "SELECT COUNT(*) FROM agents WHERE agent_type IN ('ux_observer', 'feedback_analyst')"
        expected: "result >= 2"
      - name: "founder_ux_metrics exists"
        sql: "SELECT COUNT(*) FROM founder_ux_metrics"
        expected: "no error"
```

### 4.3 End-to-End Validation Sequence

```yaml
# COMPLETE VALIDATION WORKFLOW
# Execute in order after all connections

e2e_validation:

  step_1_infrastructure:
    tests:
      - vercel_frontend
      - backend_health
      - supabase_connection
    on_failure: STOP_AND_ALERT

  step_2_authentication:
    tests:
      - supabase_auth
    on_failure: CONTINUE_WITH_WARNING

  step_3_realtime:
    tests:
      - supabase_realtime
    on_failure: CONTINUE_WITH_WARNING

  step_4_blockchain:
    tests:
      - hedera_connection
    on_failure: CONTINUE_WITH_WARNING

  step_5_integration:
    tests:
      - api_proxy
      - cors_check
    on_failure: STOP_AND_ALERT

  step_6_database:
    tests:
      - database_validation.after_grid_tables
      - database_validation.after_founder_features
      - database_validation.after_agents_tables
      - database_validation.after_adaptive_agents
    on_failure: ALERT_BUT_CONTINUE
```

---

## SECTION 5: EXECUTION SEQUENCE

### 5.1 Complete Automation Workflow

```yaml
# SKYVERN EXECUTION PLAN
# Total estimated time: 30-45 minutes

workflow:

  phase_1_verification:
    name: "Verify Existing Infrastructure"
    duration: "5 min"
    steps:
      - action: "Login to Vercel"
        verify: "Project atom-sovereign exists"
      - action: "Login to Supabase"
        verify: "Project vzbrhovthpihrhdbbjud accessible"
      - action: "Login to DigitalOcean"
        verify: "App sea-turtle-app-n4vsa running"
      - action: "Check Hedera"
        verify: "Account 0.0.7702951 has balance"

  phase_2_secrets:
    name: "Verify/Update Environment Variables"
    duration: "10 min"
    steps:
      - action: "Open Vercel Environment Variables"
        verify: "All REACT_APP_* variables present"
        update_if_missing: true
      - action: "Open DigitalOcean Environment Variables"
        verify: "All backend variables present"
        update_if_missing: true

  phase_3_domain:
    name: "Configure Custom Domain"
    duration: "15 min"
    condition: "If domain not yet configured"
    steps:
      - action: "Add domain to Vercel"
        input: "{custom_domain}"
      - action: "Configure DNS records at registrar"
        records:
          - type: A, name: @, value: 76.76.21.21
          - type: CNAME, name: www, value: cname.vercel-dns.com
      - action: "Wait for DNS propagation"
        timeout: "10 min"
        check_interval: "30s"
      - action: "Verify SSL certificate"

  phase_4_database:
    name: "Execute Database Migrations"
    duration: "10 min"
    steps:
      - action: "Open Supabase SQL Editor"
      - action: "Execute 01-fix-existing-policies.sql"
        file: "services/database/01-fix-existing-policies.sql"
        validate: true
      - action: "Execute founder-features.sql"
        file: "services/database/founder-features.sql"
        validate: true
      - action: "Execute agents-tables.sql"
        file: "services/database/agents-tables.sql"
        validate: true
      - action: "Execute founder-adaptive-agents.sql"
        file: "services/database/founder-adaptive-agents.sql"
        validate: true
      - action: "Execute grid-tables.sql"
        file: "services/database/grid-tables.sql"
        validate: true

  phase_5_storage:
    name: "Configure Storage Buckets"
    duration: "5 min"
    steps:
      - action: "Open Supabase Storage"
      - action: "Verify zama-assets bucket exists"
      - action: "Create underground-vault bucket"
        config:
          public: false
          file_size_limit: 52428800
      - action: "Add RLS policies for underground-vault"

  phase_6_deployment:
    name: "Trigger Production Deployment"
    duration: "5 min"
    steps:
      - action: "Commit pending changes"
        commands:
          - "git add ."
          - "git commit -m 'chore: Skyvern automation setup'"
      - action: "Merge to main"
        commands:
          - "git checkout main"
          - "git merge claude/deployment-error-handling-9Ismo"
          - "git push origin main"
      - action: "Monitor Vercel deployment"
        timeout: "5 min"

  phase_7_validation:
    name: "Run Validation Tests"
    duration: "5 min"
    steps:
      - action: "Execute e2e_validation sequence"
      - action: "Generate validation report"
      - action: "Alert human operator on completion"
```

---

## SECTION 6: ERROR HANDLING

### 6.1 Common Issues and Resolutions

```yaml
error_handling:

  vercel_build_failure:
    symptoms:
      - "Build failed"
      - "npm install error"
    resolution:
      - "Check package.json syntax"
      - "Verify node_modules not in .gitignore causing issues"
      - "Check build command path is correct"
    escalate_after: 2_attempts

  supabase_rls_error:
    symptoms:
      - "permission denied for table"
      - "new row violates row-level security policy"
    resolution:
      - "Check RLS policies in SQL Editor"
      - "Verify auth.uid() is available (user logged in)"
      - "Check policy conditions"
    escalate_after: 1_attempt

  hedera_connection_failed:
    symptoms:
      - "INVALID_ACCOUNT_ID"
      - "Network connection failed"
    resolution:
      - "Verify operator ID format (0.0.XXXXXX)"
      - "Check testnet vs mainnet configuration"
      - "Verify account has HBAR for fees"
    escalate_after: 2_attempts

  cors_blocked:
    symptoms:
      - "CORS policy blocked"
      - "No 'Access-Control-Allow-Origin' header"
    resolution:
      - "Add domain to CORS_ORIGINS in backend"
      - "Check vercel.json headers configuration"
      - "Verify API proxy route in vercel.json"
    escalate_after: 1_attempt

  dns_not_propagated:
    symptoms:
      - "DNS_PROBE_FINISHED_NXDOMAIN"
      - "SSL certificate pending"
    resolution:
      - "Wait additional 30 minutes"
      - "Verify DNS records at registrar"
      - "Check Vercel domain verification"
    escalate_after: 60_minutes
```

### 6.2 Escalation Protocol

```yaml
escalation:
  level_1:
    trigger: "Automated resolution failed"
    action: "Log detailed error"
    notify: false

  level_2:
    trigger: "2+ failures on same task"
    action: "Pause workflow"
    notify: "slack_webhook"
    message: "Skyvern automation paused - manual review needed"

  level_3:
    trigger: "Critical infrastructure failure"
    action: "Rollback if possible"
    notify: "email + sms"
    message: "CRITICAL: AT·OM infrastructure issue"
```

---

## SECTION 7: REFERENCE TABLES

### 7.1 Service Credentials Quick Reference

| Service | Dashboard URL | Purpose |
|---------|---------------|---------|
| Vercel | vercel.com/dashboard | Frontend hosting |
| Supabase | supabase.com/dashboard | Database + Auth |
| DigitalOcean | cloud.digitalocean.com | Backend + DB |
| Hedera | portal.hedera.com | Blockchain |
| GitHub | github.com | Source code |

### 7.2 Important File Paths

| File | Path | Purpose |
|------|------|---------|
| Vercel Config | `/vercel.json` | Deployment rules |
| Frontend App | `/ATOM/Vzwwviru70560-d4e/hardcore-joliot/atom/app/` | React source |
| Backend | `/Vzwwviru70560-d4e/hardcore-joliot/backend/` | FastAPI source |
| SQL Scripts | `/services/database/` | Database migrations |
| Hedera Service | `/services/hedera/` | Blockchain ops |

### 7.3 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Frontend app |
| `/api/v2/health` | GET | Backend health |
| `/api/auth/*` | POST | Authentication |
| `/api/profiles/*` | GET/POST | User profiles |
| `/api/grid/*` | GET/POST | Grid operations |

---

## SECTION 8: SACRED FREQUENCIES (Application Constants)

```yaml
# AT·OM SACRED CONSTANTS
# These are non-secret configuration values

frequencies:
  ATOM_M: 44.4       # Manifestation frequency
  ATOM_P: 161.8      # Phi (Golden Ratio approximation)
  ATOM_I: 369        # Tesla Integration frequency
  ATOM_PO: 1728      # Plato's Year

  ANCHOR_FREQUENCY: 444
  SIGNAL_INTERVAL: 4.44
  PHI: 1.6180339887498949

  # Inject to Vercel as:
  # REACT_APP_ATOM_M=44.4
  # REACT_APP_ATOM_P=161.8
  # REACT_APP_ATOM_I=369
  # REACT_APP_ATOM_PO=1728
```

---

## DOCUMENT METADATA

```yaml
document:
  title: "SKYVERN_MASTER_PLAN"
  version: "1.0.0"
  created: "2026-01-27"
  author: "Claude (Opus 4.5)"
  human_reviewer: "Jonathan Rodrigue"

  changelog:
    - version: "1.0.0"
      date: "2026-01-27"
      changes: "Initial creation with full infrastructure mapping"

  next_review: "After first successful Skyvern execution"
```

---

*Generated for AT·OM — L'Arche des Résonances Universelles*
*Phase I: Fondation des 144*
