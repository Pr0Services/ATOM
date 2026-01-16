# CHE·NU™ — AUTONOMOUS EXECUTION ENGINE
## Module d'Intégration des Agents Autonomes Gouvernés

**Version:** 1.0.0  
**Date:** 2024-12-26  
**Status:** ARCHITECTURE DÉFINITIVE  
**Auteur:** The CHE·NU Team

---

## ⚠️ AVERTISSEMENT CRITIQUE

```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║   CE MODULE RESPECTE STRICTEMENT LES TREE LAWS DE CHE·NU™              ║
║                                                                        ║
║   • Law 1 (SAFE): Sandbox obligatoire pour toute exécution             ║
║   • Law 2 (NON_AUTONOMOUS): Approbation humaine à chaque checkpoint    ║
║   • Law 3 (REPRESENTATIONAL): Preview avant toute action réelle        ║
║   • Law 4 (PRIVACY): Isolation complète des données                    ║
║   • Law 5 (TRANSPARENCY): Audit trail immutable                        ║
║                                                                        ║
║   AUCUN AGENT AUTONOME NE PEUT CONTOURNER CES RÈGLES                   ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📋 TABLE DES MATIÈRES

1. [Vision & Objectifs](#1-vision--objectifs)
2. [Règles d'Or d'Intégration](#2-règles-dor-dintégration)
3. [Architecture Sandbox](#3-architecture-sandbox)
4. [Agents Supportés](#4-agents-supportés)
5. [Governed Execution Pipeline Étendu](#5-governed-execution-pipeline-étendu)
6. [Protocole de Checkpoints](#6-protocole-de-checkpoints)
7. [Schéma SQL](#7-schéma-sql)
8. [Spécifications API](#8-spécifications-api)
9. [Sécurité & Isolation](#9-sécurité--isolation)
10. [Interface Utilisateur](#10-interface-utilisateur)
11. [Monitoring & Audit](#11-monitoring--audit)
12. [Exemples d'Utilisation](#12-exemples-dutilisation)

---

## 1. VISION & OBJECTIFS

### 1.1 Pourquoi des Agents Autonomes?

Les agents autonomes (Manus, Devin, Browser Use, etc.) permettent d'exécuter des **tâches complexes multi-étapes**:

| Type de Tâche | Exemple | Durée |
|---------------|---------|-------|
| Recherche approfondie | Analyser 50 articles | 2-4h |
| Développement | Créer une app complète | 4-24h |
| Automatisation web | Remplir 100 formulaires | 1-3h |
| Analyse de données | Traiter 10GB de données | 2-8h |

### 1.2 Le Paradoxe Résolu

```
┌─────────────────────────────────────────────────────────────────┐
│                    LE PARADOXE DE L'AUTONOMIE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   AUTONOMIE TOTALE          vs          CONTRÔLE TOTAL          │
│   • Efficacité maximale                 • Sécurité maximale     │
│   • Risques incontrôlés                 • Inefficacité          │
│                                                                 │
│                    SOLUTION CHE·NU                              │
│            ════════════════════════════                         │
│                                                                 │
│            AUTONOMIE GOUVERNÉE PAR CHECKPOINTS                  │
│                                                                 │
│   • Exécution autonome ENTRE les checkpoints                    │
│   • Validation humaine AUX checkpoints                          │
│   • Rollback possible à tout moment                             │
│   • Audit trail complet                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Principe Fondamental

> **"L'agent autonome propose, l'humain dispose — à chaque checkpoint."**

---

## 2. RÈGLES D'OR D'INTÉGRATION

### 2.1 Les 5 Tree Laws Appliquées

#### 🔐 LAW 1: SAFE (Sécurité)

```yaml
safe_rules:
  sandbox_obligatoire: true
  network_isolation: true
  filesystem_isolation: true
  resource_limits:
    cpu: "2 cores max"
    memory: "4GB max"
    disk: "10GB max"
    time: "configurable per task"
  no_system_access: true
  no_credential_storage: true
```

**Implémentation:**
- Chaque agent s'exécute dans un **conteneur Docker isolé**
- Réseau sandbox avec whitelist d'URLs
- Filesystem éphémère détruit après exécution
- Aucun accès aux credentials CHE·NU

#### 🚫 LAW 2: NON_AUTONOMOUS (Approbation Humaine)

```yaml
approval_rules:
  task_start: REQUIRED
  checkpoint_validation: REQUIRED
  external_action: REQUIRED
  data_export: REQUIRED
  cost_threshold_exceeded: REQUIRED
  task_completion: REQUIRED
```

**Points de validation obligatoires:**
1. **Avant démarrage** — Validation du plan
2. **À chaque checkpoint** — Validation résultats intermédiaires
3. **Avant action externe** — Email, API, fichier partagé
4. **Avant export** — Données sortant du sandbox
5. **À la fin** — Validation résultats finaux

#### 👁️ LAW 3: REPRESENTATIONAL (Preview)

```yaml
preview_rules:
  show_plan_before_execution: true
  show_diff_before_commit: true
  show_output_before_export: true
  simulation_mode_available: true
```

**Modes d'exécution:**
- **SIMULATION**: Montre ce qui SERAIT fait sans effets réels
- **SUPERVISED**: Approbation à chaque étape
- **CHECKPOINT**: Libre entre checkpoints définis
- **JAMAIS FULLY_AUTONOMOUS**: Toujours un checkpoint final

#### 🔒 LAW 4: PRIVACY (Isolation Données)

```yaml
privacy_rules:
  data_isolation:
    - "Agents ne voient QUE les données explicitement partagées"
    - "Pas d'accès aux autres sphères"
    - "Pas d'accès aux autres threads"
  data_classification:
    PUBLIC: "Peut être traité"
    INTERNAL: "Requires explicit sharing"
    CONFIDENTIAL: "Jamais partagé avec agents autonomes"
  encryption:
    at_rest: "AES-256"
    in_transit: "TLS 1.3"
```

#### 📝 LAW 5: TRANSPARENCY (Audit Trail)

```yaml
audit_rules:
  log_everything: true
  immutable_logs: true
  log_contents:
    - timestamp
    - agent_id
    - action_type
    - input_hash
    - output_hash
    - approval_status
    - approver_id
    - cost_tokens
  retention: "7 years minimum"
```

---

### 2.2 Matrice de Compatibilité Étendue

```typescript
interface AutonomousAgentDefinition {
  id: string;
  name: string;
  level: 'L2' | 'L3';  // Agents autonomes = L2 ou L3 seulement
  provider: 'manus' | 'devin' | 'browser_use' | 'custom';
  
  // Governance
  max_execution_time: number;
  max_tokens_budget: number;
  max_cost_usd: number;
  checkpoint_frequency: 'per_step' | 'per_minute' | 'custom';
  
  // Sandbox
  sandbox_profile: SandboxProfile;
  network_whitelist: string[];
  
  // Tree Law compliance
  tree_law_compliance: {
    safe: boolean;
    non_autonomous: boolean;
    representational: boolean;
    privacy: boolean;
    transparency: boolean;
  };
}
```

---

## 3. ARCHITECTURE SANDBOX

### 3.1 Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CHE·NU™ CORE                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    NOVA (L0) — Governance                        │   │
│  │              Supervise TOUS les agents autonomes                 │   │
│  └─────────────────────────┬───────────────────────────────────────┘   │
│                            │                                            │
│  ┌─────────────────────────▼───────────────────────────────────────┐   │
│  │              AUTONOMOUS EXECUTION CONTROLLER (L1)                │   │
│  │         Orchestration • Checkpoints • Budget • Audit             │   │
│  └─────────────────────────┬───────────────────────────────────────┘   │
│                            │                                            │
│  ┌─────────────────────────▼───────────────────────────────────────┐   │
│  │                    SANDBOX ORCHESTRATOR                          │   │
│  │              Création • Monitoring • Destruction                 │   │
│  └─────────────────────────┬───────────────────────────────────────┘   │
│                            │                                            │
├────────────────────────────┼────────────────────────────────────────────┤
│         SANDBOX ZONE       │        (Isolée du système principal)       │
│                            │                                            │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │
│   │   SANDBOX   │  │   SANDBOX   │  │   SANDBOX   │                    │
│   │   MANUS     │  │   DEVIN     │  │  BROWSER    │                    │
│   │             │  │             │  │             │                    │
│   │ Container   │  │ Container   │  │ Container   │                    │
│   │ isolé       │  │ isolé       │  │ isolé       │                    │
│   │             │  │             │  │             │                    │
│   │ Network:    │  │ Network:    │  │ Network:    │                    │
│   │ Whitelist   │  │ Whitelist   │  │ Whitelist   │                    │
│   │             │  │             │  │             │                    │
│   │ Filesystem: │  │ Filesystem: │  │ Filesystem: │                    │
│   │ Ephemeral   │  │ Ephemeral   │  │ Ephemeral   │                    │
│   └─────────────┘  └─────────────┘  └─────────────┘                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Profils de Sandbox

```typescript
const SANDBOX_PROFILES = {
  
  // Recherche web seulement
  research_only: {
    resources: { cpu: 1, memory: 2048, disk: 5120, timeout: 7200 },
    network: {
      mode: 'whitelist',
      whitelist: ['google.com', 'wikipedia.org', 'arxiv.org', 'github.com']
    },
    capabilities: { execute_code: false, screenshots: true }
  },
  
  // Développement code
  code_development: {
    resources: { cpu: 2, memory: 4096, disk: 10240, timeout: 14400 },
    network: {
      mode: 'whitelist',
      whitelist: ['github.com', 'npmjs.com', 'pypi.org', 'stackoverflow.com']
    },
    capabilities: { execute_code: true, screenshots: true }
  },
  
  // Automatisation navigateur
  browser_automation: {
    resources: { cpu: 2, memory: 4096, disk: 5120, timeout: 3600 },
    network: { mode: 'filtered' },  // URLs définies par tâche
    capabilities: { execute_code: false, screenshots: true, clipboard: true }
  }
};
```

---

## 4. AGENTS SUPPORTÉS

### 4.1 Manus 1.6

```yaml
agent:
  id: manus_1_6
  name: "Manus 1.6"
  provider: anthropic
  capabilities: [web_browsing, code_execution, research, document_creation]
  
  governance:
    max_execution_time: 14400  # 4h
    max_tokens: 1000000
    max_cost_usd: 50.00
    checkpoint_frequency: "per_major_step"
    
  sandbox_profile: code_development
```

### 4.2 Devin

```yaml
agent:
  id: devin_1
  name: "Devin"
  provider: cognition_ai
  capabilities: [code_execution, testing, deployment_prep]
  
  governance:
    max_execution_time: 28800  # 8h
    max_tokens: 2000000
    max_cost_usd: 100.00
    checkpoint_frequency: "per_file_changed"
```

### 4.3 Browser Agent

```yaml
agent:
  id: browser_agent
  name: "Browser Automation"
  capabilities: [web_browsing, form_filling, data_extraction]
  
  governance:
    max_execution_time: 3600  # 1h
    max_pages: 100
    checkpoint_frequency: "per_page"
    
  safety:
    block_payment_forms: true
    block_login_forms: true
```

---

## 5. GOVERNED EXECUTION PIPELINE ÉTENDU

### 5.1 Pipeline 15 Étapes

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 GOVERNED AUTONOMOUS EXECUTION PIPELINE                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: PRÉPARATION                                                   │
│  ─────────────────────                                                  │
│  1. INTENT CAPTURE          → Utilisateur décrit la tâche              │
│  2. SEMANTIC ENCODING       → Transformation structurée                 │
│  3. TASK DECOMPOSITION      → Découpage en sous-tâches                 │
│  4. AGENT SELECTION (ACM)   → Sélection agent compatible               │
│  5. SANDBOX CONFIGURATION   → Préparation environnement                │
│                                                                         │
│  PHASE 2: VALIDATION                                                    │
│  ────────────────────                                                   │
│  6. COST ESTIMATION         → Calcul tokens, temps, coût               │
│  7. SCOPE LOCKING           → Définition limites                       │
│  8. BUDGET VERIFICATION     → Vérification budget suffisant            │
│  9. 🔴 HUMAN APPROVAL (PLAN) → Utilisateur approuve le plan            │
│                                                                         │
│  PHASE 3: EXÉCUTION                                                     │
│  ──────────────────                                                     │
│  10. SANDBOX SPAWN          → Création conteneur isolé                 │
│  11. AUTONOMOUS EXECUTION   → Agent exécute jusqu'au checkpoint        │
│  12. 🔴 CHECKPOINT VALIDATION → Validation résultats intermédiaires    │
│      (répété jusqu'à completion)                                       │
│  13. OUTPUT COLLECTION      → Collecte résultats                       │
│                                                                         │
│  PHASE 4: FINALISATION                                                  │
│  ─────────────────────                                                  │
│  14. 🔴 HUMAN APPROVAL (RESULTS) → Validation résultats finaux         │
│  15. EXPORT & AUDIT         → Export + destruction sandbox + audit     │
│                                                                         │
│  🔴 = Points de validation humaine OBLIGATOIRES                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 États d'Exécution

```typescript
type ExecutionState =
  | 'DRAFT'              // En définition
  | 'PENDING_APPROVAL'   // Attente approbation plan
  | 'APPROVED'           // Prêt à démarrer
  | 'SPAWNING_SANDBOX'   // Création sandbox
  | 'EXECUTING'          // En cours
  | 'CHECKPOINT_REACHED' // Attente validation
  | 'PAUSED'             // Pausé
  | 'PENDING_EXPORT'     // Attente approbation résultats
  | 'COMPLETED'          // Terminé
  | 'FAILED'             // Échec
  | 'CANCELLED'          // Annulé
  | 'ROLLED_BACK';       // Restauré
```

---

## 6. PROTOCOLE DE CHECKPOINTS

### 6.1 Types de Checkpoints

```typescript
type CheckpointType =
  | 'TIME_BASED'     // Toutes les N minutes
  | 'STEP_BASED'     // À chaque étape majeure
  | 'ACTION_BASED'   // Avant certaines actions
  | 'COST_BASED';    // Quand coût atteint seuil
```

### 6.2 Actions Déclenchant un Checkpoint

```yaml
# TOUJOURS avec checkpoint
always_checkpoint:
  - send_email
  - submit_form
  - make_payment
  - delete_file
  - publish_content
  - database_write

# Configurable
configurable_checkpoint:
  - create_file
  - modify_file
  - navigate_new_domain
  - execute_code

# Monitoring seulement
monitoring_only:
  - read_file
  - search_web
  - take_screenshot
```

### 6.3 Interface Checkpoint

```typescript
interface CheckpointNotification {
  checkpoint_id: string;
  execution_id: string;
  
  // Progression
  current_step: number;
  total_steps: number;
  progress_percent: number;
  
  // Résumé
  summary: string;
  actions_completed: Action[];
  next_actions: Action[];
  
  // Métriques
  tokens_used: number;
  cost_so_far_usd: number;
  time_elapsed: number;
  
  // Outputs
  outputs: Output[];
  screenshots?: string[];
  
  // Options utilisateur
  options: ['approve', 'modify', 'pause', 'rollback', 'cancel'];
  
  // Auto-approve optionnel
  auto_approve_timeout?: number;
}
```

---

## 7. SCHÉMA SQL

```sql
-- Table principale
CREATE TABLE autonomous_executions (
    id UUID PRIMARY KEY,
    thread_id UUID NOT NULL REFERENCES threads(id),
    sphere_id VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL,
    
    -- Agent
    agent_id VARCHAR(100) NOT NULL,
    sandbox_profile_id VARCHAR(100) NOT NULL,
    
    -- Tâche
    task_description TEXT NOT NULL,
    task_encoded JSONB NOT NULL,
    task_plan JSONB NOT NULL,
    
    -- État
    state VARCHAR(50) NOT NULL DEFAULT 'DRAFT',
    progress_percent DECIMAL(5,2) DEFAULT 0,
    
    -- Budget
    budget_tokens INTEGER NOT NULL,
    budget_usd DECIMAL(10,2) NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    cost_usd DECIMAL(10,2) DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    approved_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- Checkpoints
CREATE TABLE autonomous_checkpoints (
    id UUID PRIMARY KEY,
    execution_id UUID NOT NULL REFERENCES autonomous_executions(id),
    checkpoint_number INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    summary TEXT,
    outputs JSONB,
    resolved_at TIMESTAMPTZ,
    resolution VARCHAR(50)  -- APPROVED, MODIFIED, REJECTED
);

-- Audit trail IMMUTABLE
CREATE TABLE autonomous_audit_log (
    id UUID PRIMARY KEY,
    execution_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    actor_type VARCHAR(50) NOT NULL,
    input_hash VARCHAR(64),
    output_hash VARCHAR(64),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger pour empêcher modifications
CREATE TRIGGER audit_immutable
BEFORE UPDATE OR DELETE ON autonomous_audit_log
FOR EACH ROW EXECUTE FUNCTION prevent_modification();
```

---

## 8. SPÉCIFICATIONS API

```yaml
# Création
POST /api/v1/autonomous/executions:
  body: { task_description, agent_id, budget_tokens, budget_usd }
  response: { execution_id, task_plan, estimated_cost }

# Approbation plan
POST /api/v1/autonomous/executions/{id}/approve:
  response: { status: "APPROVED" }

# Démarrage
POST /api/v1/autonomous/executions/{id}/start:
  response: { status: "EXECUTING" }

# Stream temps réel
GET /api/v1/autonomous/executions/{id}/stream:
  response: SSE events [action_started, checkpoint_reached, completed]

# Checkpoint approval
POST /api/v1/autonomous/executions/{id}/checkpoints/{cpid}/approve:
  response: { status: "APPROVED" }

# Contrôles
POST /api/v1/autonomous/executions/{id}/pause
POST /api/v1/autonomous/executions/{id}/resume
POST /api/v1/autonomous/executions/{id}/cancel

# Export résultats
POST /api/v1/autonomous/executions/{id}/export:
  body: { output_ids }

# Audit
GET /api/v1/autonomous/executions/{id}/audit
```

---

## 9. SÉCURITÉ & ISOLATION

### 9.1 Configuration Docker

```yaml
# docker-compose.sandbox.yml
services:
  sandbox:
    network_mode: "none"  # Ou réseau dédié
    read_only: true
    security_opt:
      - no-new-privileges:true
      - seccomp:./seccomp-profile.json
    cap_drop:
      - ALL
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    tmpfs:
      - /tmp:size=100M
    privileged: false
    user: "1000:1000"
```

### 9.2 Modèle de Menaces

| Menace | Mitigation |
|--------|------------|
| Agent malveillant | Sandbox isolé, network whitelist |
| Exfiltration données | Validation avant export, logging réseau |
| Élévation privilèges | Container rootless, capabilities minimales |
| DoS | Limites CPU/mémoire/temps strictes |

---

## 10. INTERFACE UTILISATEUR

### 10.1 Composants Clés

```typescript
// Vue exécution
<AutonomousExecutionView>
  <TaskPlanPanel />        // Plan avec checkpoints
  <ProgressPanel />        // Progression temps réel
  <CheckpointsTimeline />  // Historique checkpoints
  <OutputsPanel />         // Résultats
  <AuditPanel />           // Audit trail
</AutonomousExecutionView>

// Modal checkpoint
<CheckpointModal>
  <Summary />
  <Outputs />
  <Screenshots />
  <NextActions />
  <Metrics cost={} tokens={} time={} />
  <Actions [Approve] [Modify] [Reject] [Pause] />
</CheckpointModal>
```

---

## 11. MONITORING & AUDIT

### 11.1 Métriques

```yaml
metrics:
  execution:
    - duration_seconds
    - tokens_consumed
    - cost_usd
    - checkpoints_reached
    - checkpoints_approved
    - checkpoints_rejected
  sandbox:
    - cpu_usage_percent
    - memory_usage_mb
    - network_requests
  governance:
    - approval_wait_time
    - rollbacks_count
```

---

## 12. EXEMPLES D'UTILISATION

### Exemple 1: Recherche avec Manus

```typescript
const execution = await api.createExecution({
  task: "Recherche sur IA 2024, rapport 10 pages",
  agent: "manus_1_6",
  budget: { tokens: 500000, usd: 25.00 }
});

// Plan généré avec 6 checkpoints
// Utilisateur approuve
// Exécution avec validation à chaque section
// Export final du PDF
```

### Exemple 2: Automatisation Browser

```typescript
const execution = await api.createExecution({
  task: "Scraper 50 prix sur site-x.com",
  agent: "browser_agent",
  budget: { tokens: 50000, usd: 5.00 },
  network_whitelist: ["site-x.com"]
});

// Checkpoints toutes les 10 minutes avec screenshots
// Export Excel final
```

---

## 📋 RÉSUMÉ RÈGLES D'OR

```
╔════════════════════════════════════════════════════════════════════════╗
║                    RÈGLES D'OR - AGENTS AUTONOMES                      ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  1. SANDBOX OBLIGATOIRE — Conteneur Docker isolé                       ║
║  2. CHECKPOINTS HUMAINS — Plan + intermédiaires + final                ║
║  3. PREVIEW AVANT ACTION — Simulation disponible                       ║
║  4. ISOLATION DONNÉES — Accès explicite seulement                      ║
║  5. AUDIT IMMUTABLE — Tout loggé, rien modifiable                      ║
║  6. BUDGET & TIMEOUT — Pas d'exécution illimitée                       ║
║  7. ROLLBACK POSSIBLE — Annulation à tout moment                       ║
║  8. PAS D'ACCÈS CREDENTIALS — Agent isolé du système                   ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

**Version:** 1.0.0  
**Auteur:** The CHE·NU Team  
**Status:** PRÊT POUR IMPLÉMENTATION
