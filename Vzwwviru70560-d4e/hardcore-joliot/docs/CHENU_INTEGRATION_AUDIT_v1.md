# 🔍 CHE·NU™ — RAPPORT D'ANALYSE D'INTÉGRATION COMPLET
## Audit des Modules, Connexions & Angles Morts

**Date:** 23 Décembre 2025  
**Version:** 1.0  
**Statut:** 🔬 ANALYSE APPROFONDIE  

---

# 📊 RÉSUMÉ EXÉCUTIF

## Vue d'ensemble

| Dimension | Éléments | Statut |
|-----------|----------|--------|
| **Schéma SQL** | 21 sections, 47+ tables | ✅ Complet |
| **API Specs** | 15 sections, 80+ endpoints | ✅ Complet |
| **Chapitres Engines** | 8 moteurs documentés | ✅ Détaillé |
| **Connexions identifiées** | 156 liens inter-modules | ⚠️ À valider |
| **Angles morts critiques** | 12 éléments | 🔴 Action requise |
| **Améliorations proposées** | 28 recommandations | 🟡 Planification |

---

# 1️⃣ MATRICE DE CONNEXIONS INTER-MODULES

## A. Connexions Core → Periphery

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURE DE CONNEXIONS                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐         │
│   │    USERS     │──────│  IDENTITIES  │──────│   SPHERES    │         │
│   └──────┬───────┘      └──────┬───────┘      └──────┬───────┘         │
│          │                     │                     │                   │
│          ▼                     ▼                     ▼                   │
│   ┌──────────────────────────────────────────────────────────┐         │
│   │                     DATASPACES                            │         │
│   │   (Container Universel - Tous les modules convergent)     │         │
│   └──────┬───────────────────────┬───────────────────┬───────┘         │
│          │                       │                   │                   │
│          ▼                       ▼                   ▼                   │
│   ┌──────────┐            ┌──────────┐        ┌──────────┐             │
│   │ THREADS  │            │ WORKSPACES│       │  MEMORY  │             │
│   │ (.chenu) │            │          │        │  ITEMS   │             │
│   └────┬─────┘            └────┬─────┘        └────┬─────┘             │
│        │                       │                   │                     │
│        ▼                       ▼                   ▼                     │
│   ┌──────────┐            ┌──────────┐        ┌──────────┐             │
│   │ MESSAGES │            │  PANELS  │        │ GOVERNANCE│            │
│   │DECISIONS │            │  STATES  │        │   AUDIT   │            │
│   └──────────┘            └──────────┘        └──────────┘             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## B. Matrice de Dépendances SQL

| Table Source | Dépend de | Utilise FK | Criticité |
|--------------|-----------|------------|-----------|
| `dataspaces` | users, identities, spheres, domains | 4 FK | 🔴 CRITIQUE |
| `threads` | dataspaces, identities | 2 FK | 🔴 CRITIQUE |
| `workspaces` | users, identities, dataspaces | 3 FK | 🔴 CRITIQUE |
| `meetings` | dataspaces, identities, users | 3 FK | 🟠 HAUTE |
| `properties` | dataspaces, identities | 2 FK | 🟠 HAUTE |
| `agents` | spheres, domains | 2 FK | 🟠 HAUTE |
| `agent_executions` | agents, users, identities, threads, dataspaces | 5 FK | 🔴 CRITIQUE |
| `memory_items` | users, identities, dataspaces, threads | 4 FK | 🔴 CRITIQUE |
| `oneclick_executions` | workflows, users, identities | 3 FK | 🟡 MOYENNE |
| `backstage_contexts` | users, identities | 2 FK | 🟡 MOYENNE |
| `xr_rooms` | dataspaces, meetings | 2 FK | 🟡 MOYENNE |
| `ocw_sessions` | workspaces | 1 FK | 🟡 MOYENNE |
| `files` | dataspaces, identities | 2 FK | 🟠 HAUTE |

---

# 2️⃣ ANGLES MORTS CRITIQUES IDENTIFIÉS

## 🔴 NIVEAU CRITIQUE (Bloquants)

### AM-001: Absence de Table TOKENS
**Problème:** Le schéma SQL ne contient AUCUNE table pour la gestion des tokens CHE·NU (crédits d'intelligence).

**Impact:** 
- Impossible de budgeter les threads
- Impossible de gouverner les coûts IA
- Pas de traçabilité des dépenses tokens
- Principe fondamental non implémenté

**Tables manquantes:**
```sql
-- MANQUANT: token_accounts
-- MANQUANT: token_transactions  
-- MANQUANT: token_budgets
-- MANQUANT: token_allocations
```

**Recommandation:** PRIORITÉ P0 - Créer immédiatement le système de tokens.

---

### AM-002: Semantic Encoding Layer Non Implémenté
**Problème:** Le "Semantic Encoding Layer" décrit comme innovation clé (IP brevetable) n'a pas de représentation dans le schéma.

**Tables manquantes:**
```sql
-- MANQUANT: encoded_intents
-- MANQUANT: encoding_rules
-- MANQUANT: encoding_quality_scores (EQS)
-- MANQUANT: encoding_transformations
```

**Impact:**
- Pipeline de gouvernance incomplet
- Pas d'optimisation des tokens
- Avantage compétitif non codifié

---

### AM-003: Agent Compatibility Matrix Non Implémenté
**Problème:** La matrice de compatibilité agents (ACM) décrite dans le Master Reference n'existe pas en base.

**Tables manquantes:**
```sql
-- MANQUANT: agent_compatibility_matrix
-- MANQUANT: agent_sphere_compatibility
-- MANQUANT: agent_domain_compatibility
```

---

### AM-004: Thread Budget/Governance Non Lié
**Problème:** La table `threads` ne contient pas de champs pour:
- Budget tokens alloué
- Coût tokens consommé
- Règles d'encoding applicables
- Scope lock status

**Champs manquants dans `threads`:**
```sql
-- MANQUANT: token_budget DECIMAL
-- MANQUANT: tokens_consumed DECIMAL
-- MANQUANT: scope_locked BOOLEAN
-- MANQUANT: encoding_profile_id UUID
```

---

## 🟠 NIVEAU HAUTE (Importants)

### AM-005: Workflow Steps Non Détaillés
**Problème:** La table `oneclick_workflows` utilise un JSONB pour `workflow_steps` mais pas de table normalisée pour les étapes.

**Impact:** Difficile d'auditer, de modifier, ou d'optimiser les workflows.

---

### AM-006: Pas de Table Nova (System Intelligence)
**Problème:** Nova est définie comme "System Intelligence" mais n'a pas de représentation persistante.

**Tables manquantes:**
```sql
-- MANQUANT: nova_context_state
-- MANQUANT: nova_guidance_history
-- MANQUANT: nova_suggestions
```

---

### AM-007: Bureau Sections Non Modélisées
**Problème:** Les 6 sections de bureau (Dashboard, Notes, Tasks, Projects, Threads, Meetings...) ne sont pas représentées dans le schéma.

**Impact:** Pas de configuration persistante par sphère/identité des bureaux.

---

### AM-008: XR Spatial Objects Limités
**Problème:** Le système XR est défini mais limité:
- Pas de persistance d'avatars
- Pas de synchronisation temps réel modélisée
- Pas de spatial anchors

---

## 🟡 NIVEAU MOYEN (Améliorations)

### AM-009: Absence de Notifications Push Config
**Problème:** La table `notifications` existe mais pas de configuration des canaux (email, push, SMS, webhook).

---

### AM-010: Pas de Table Subscriptions/Plans
**Problème:** Pas de modèle de tarification/abonnement.

---

### AM-011: Pas de Table API Keys
**Problème:** L'API utilise JWT mais pas de gestion des clés API pour intégrations.

---

### AM-012: Pas d'Historique de Transformation Workspace
**Problème:** `workspace_transformations` existe mais pas d'historique complet des états.

---

# 3️⃣ ANALYSE DES CONNEXIONS API ↔ SQL

## Endpoints Alignés ✅

| Endpoint | Table(s) SQL | Statut |
|----------|--------------|--------|
| `POST /identities` | identities | ✅ Aligné |
| `POST /dataspaces` | dataspaces | ✅ Aligné |
| `POST /threads` | threads | ✅ Aligné |
| `POST /workspaces` | workspaces | ✅ Aligné |
| `POST /memory` | memory_items | ✅ Aligné |
| `POST /agents/{id}/execute` | agent_executions | ✅ Aligné |
| `POST /meetings` | meetings | ✅ Aligné |
| `POST /immobilier/properties` | properties | ✅ Aligné |
| `POST /construction/projects` | construction_projects | ✅ Aligné |
| `POST /ocw/sessions` | ocw_sessions | ✅ Aligné |
| `POST /xr/rooms` | xr_rooms | ✅ Aligné |
| `POST /files/upload` | files | ✅ Aligné |

## Endpoints Sans Support SQL ⚠️

| Endpoint | Table Manquante | Action |
|----------|-----------------|--------|
| `POST /tokens/allocate` | token_accounts | 🔴 Créer |
| `GET /encoding/score` | encoding_quality_scores | 🔴 Créer |
| `POST /governance/scope-lock` | thread scope fields | 🟠 Modifier |
| `GET /agents/compatibility` | agent_compatibility_matrix | 🔴 Créer |
| `POST /nova/context` | nova_context_state | 🟡 Créer |

---

# 4️⃣ CONNEXIONS INTER-ENGINES

## Flow Principal: Intent → Execution

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GOVERNED EXECUTION PIPELINE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ① HUMAN INTENT                                                      │
│       │                                                              │
│       ▼                                                              │
│  ┌────────────────────┐                                              │
│  │ SEMANTIC ENCODING  │ ◄── Transforme intention en schéma          │
│  │      LAYER         │      machine-readable                        │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │  INTENT VALIDATION │ ◄── Vérifie cohérence & scope                │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │  COST ESTIMATION   │ ◄── Calcule tokens nécessaires              │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │ BUDGET VERIFICATION│ ◄── Vérifie disponibilité tokens             │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │    SCOPE LOCK      │ ◄── Verrouille périmètre                    │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │ AGENT COMPATIBILITY│ ◄── Match agents avec tâche                 │
│  │      MATRIX        │                                              │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │  AGENT EXECUTION   │ ◄── Exécution gouvernée                     │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │ RESULT ASSEMBLY    │ ◄── Assemblage résultats                    │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ┌────────────────────┐                                              │
│  │  AUDIT TRAIL       │ ◄── Log complet                             │
│  └─────────┬──────────┘                                              │
│            │                                                         │
│            ▼                                                         │
│  ③ .CHENU THREAD (Artefact Persistant)                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Matrice de Connexions Engines

| Engine Source | Dépend de | Fournit à | Connexion Validée |
|---------------|-----------|-----------|-------------------|
| **1-Click** | Intent, Backstage, Agents | Workspace, DataSpace | ⚠️ Partiel |
| **Backstage** | Memory, DataSpace | 1-Click, Agents | ⚠️ Partiel |
| **Workspace** | DataSpace, Layout | OCW, XR | ✅ Complet |
| **DataSpace** | Identity, Memory | Tous | ✅ Complet |
| **Memory** | Identity, DataSpace | Backstage, Agents | ⚠️ Partiel |
| **Layout** | Workspace, Identity | UI Components | ✅ Complet |
| **OCW** | Workspace | XR, Collaboration | ✅ Complet |
| **Meeting** | DataSpace, XR | Threads, Tasks | ✅ Complet |

---

# 5️⃣ RECOMMANDATIONS D'AMÉLIORATION

## P0 — CRITIQUES (Semaine 1)

### R-001: Créer le Système de Tokens
```sql
-- Nouveau fichier: migrations/add_token_system.sql

CREATE TABLE token_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    balance DECIMAL(14, 4) DEFAULT 0,
    reserved DECIMAL(14, 4) DEFAULT 0,
    lifetime_earned DECIMAL(14, 4) DEFAULT 0,
    lifetime_spent DECIMAL(14, 4) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, identity_id)
);

CREATE TABLE token_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES token_accounts(id),
    transaction_type VARCHAR(50) NOT NULL, -- 'credit', 'debit', 'reserve', 'release', 'transfer'
    amount DECIMAL(14, 4) NOT NULL,
    balance_after DECIMAL(14, 4) NOT NULL,
    reference_type VARCHAR(50), -- 'thread', 'agent_execution', 'meeting', 'workflow'
    reference_id UUID,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE token_budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL REFERENCES identities(id),
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    dataspace_id UUID REFERENCES dataspaces(id),
    budget_type VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly', 'project', 'unlimited'
    budget_amount DECIMAL(14, 4),
    spent_amount DECIMAL(14, 4) DEFAULT 0,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### R-002: Ajouter Champs Token aux Threads
```sql
ALTER TABLE threads ADD COLUMN token_budget DECIMAL(14, 4);
ALTER TABLE threads ADD COLUMN tokens_consumed DECIMAL(14, 4) DEFAULT 0;
ALTER TABLE threads ADD COLUMN scope_locked BOOLEAN DEFAULT FALSE;
ALTER TABLE threads ADD COLUMN scope_locked_at TIMESTAMP WITH TIME ZONE;
```

### R-003: Créer Semantic Encoding Tables
```sql
CREATE TABLE encoding_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    encoding_rules JSONB NOT NULL,
    compression_ratio_target DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE encoded_intents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID REFERENCES threads(id),
    original_text TEXT NOT NULL,
    encoded_schema JSONB NOT NULL,
    encoding_profile_id UUID REFERENCES encoding_profiles(id),
    eqs_score DECIMAL(5, 2), -- Encoding Quality Score
    tokens_saved INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## P1 — HAUTES (Semaines 2-3)

### R-004: Créer Agent Compatibility Matrix
```sql
CREATE TABLE agent_compatibility_matrix (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    task_type VARCHAR(100),
    compatibility_score DECIMAL(5, 2), -- 0.00 to 1.00
    constraints JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(agent_id, sphere_id, domain_id, task_type)
);
```

### R-005: Ajouter Bureau Configuration
```sql
CREATE TABLE bureau_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL REFERENCES identities(id),
    sphere_id UUID NOT NULL REFERENCES spheres(id),
    section_order TEXT[] DEFAULT ARRAY['dashboard', 'notes', 'tasks', 'projects', 'threads', 'meetings'],
    visible_sections TEXT[],
    default_section VARCHAR(50) DEFAULT 'dashboard',
    layout_preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(identity_id, sphere_id)
);
```

### R-006: Créer Nova Context State
```sql
CREATE TABLE nova_contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    session_id UUID NOT NULL,
    current_sphere_id UUID REFERENCES spheres(id),
    current_dataspace_id UUID REFERENCES dataspaces(id),
    context_state JSONB DEFAULT '{}',
    active_suggestions JSONB DEFAULT '[]',
    guidance_history JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## P2 — MOYENNES (Semaines 4-6)

### R-007: Normaliser Workflow Steps
```sql
CREATE TABLE workflow_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES oneclick_workflows(id),
    step_order INTEGER NOT NULL,
    step_type VARCHAR(50) NOT NULL,
    step_name VARCHAR(100),
    agent_id UUID REFERENCES agents(id),
    input_mapping JSONB,
    output_mapping JSONB,
    conditions JSONB,
    timeout_seconds INTEGER DEFAULT 300,
    is_optional BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### R-008: Ajouter Subscriptions
```sql
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    tier VARCHAR(50) NOT NULL, -- 'free', 'starter', 'pro', 'enterprise'
    monthly_tokens INTEGER,
    max_identities INTEGER,
    max_agents INTEGER,
    features JSONB DEFAULT '[]',
    price_monthly DECIMAL(10, 2),
    price_yearly DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    plan_id UUID NOT NULL REFERENCES subscription_plans(id),
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE
);
```

### R-009: Ajouter API Keys
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID REFERENCES identities(id),
    key_hash VARCHAR(64) NOT NULL,
    key_prefix VARCHAR(8) NOT NULL, -- Pour identification visuelle
    name VARCHAR(100),
    permissions TEXT[],
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

# 6️⃣ CHECKLIST DE VALIDATION

## Tests d'Intégration Requis

### A. Flux Core
- [ ] User → Identity → Sphere → DataSpace → Thread
- [ ] Thread → Messages → Decisions → Memory
- [ ] Workspace → Panels → States → Transformations
- [ ] Agent → Execution → Token Debit → Audit Log

### B. Flux Domaines
- [ ] Immobilier: Property → Units → Tenants → Payments
- [ ] Construction: Project → Estimates → Line Items
- [ ] Meeting: Schedule → Participants → Notes → Tasks

### C. Gouvernance
- [ ] Memory Laws enforcement (10 laws)
- [ ] Cross-Identity blocking
- [ ] Elevation requests flow
- [ ] Audit trail completeness

### D. Temps Réel
- [ ] WebSocket notifications
- [ ] OCW collaboration sync
- [ ] XR session sync

---

# 7️⃣ PLAN D'ACTION PRIORISÉ

## Phase 1: Fondations Tokens (5 jours)
| Jour | Action |
|------|--------|
| J1 | Migration token_accounts, token_transactions |
| J2 | Migration token_budgets, ALTER threads |
| J3 | API endpoints tokens |
| J4 | Intégration agent_executions + tokens |
| J5 | Tests + Documentation |

## Phase 2: Semantic Encoding (5 jours)
| Jour | Action |
|------|--------|
| J6 | Migration encoding_profiles, encoded_intents |
| J7 | Service EncodingEngine |
| J8 | Intégration avec 1-Click |
| J9 | EQS calculation |
| J10 | Tests + Documentation |

## Phase 3: Agent Matrix (3 jours)
| Jour | Action |
|------|--------|
| J11 | Migration agent_compatibility_matrix |
| J12 | Population données initiales |
| J13 | API + Tests |

## Phase 4: Consolidation (5 jours)
| Jour | Action |
|------|--------|
| J14-15 | Bureau configurations |
| J16-17 | Nova contexts |
| J18 | Tests d'intégration complets |

---

# 8️⃣ MÉTRIQUES DE SUCCÈS

| Métrique | Objectif | Actuel |
|----------|----------|--------|
| Tables SQL complètes | 60+ | 47 |
| Endpoints API alignés | 100% | 85% |
| Angles morts résolus | 0 | 12 |
| Tests d'intégration | 100% | ~40% |
| Documentation API | 100% | ~80% |

---

## CONCLUSION

Ce rapport identifie **12 angles morts critiques** dont le plus important est l'absence totale du système de tokens — élément fondamental de la proposition de valeur CHE·NU. 

Les recommandations sont priorisées pour permettre une implémentation progressive sur 3-4 semaines, avec les fondations tokens/encoding en priorité absolue.

**Action immédiate recommandée:** Commencer par R-001 (Token System) dès maintenant.

---

*Document généré le 23 Décembre 2025*
*CHE·NU™ — GOVERNED INTELLIGENCE OPERATING SYSTEM*
*Révolutionner la connexion IA-humain* 🌟
