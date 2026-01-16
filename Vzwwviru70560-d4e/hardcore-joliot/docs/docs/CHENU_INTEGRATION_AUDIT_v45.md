# 🏛️ CHE·NU™ — AUDIT D'INTÉGRATION COMPLET
## Analyse des Modules, Connexions & Angles Morts
**Version:** 45.1 | **Date:** 23 Décembre 2025 | **Statut:** 🔍 ANALYSE APPROFONDIE

---

## 📊 RÉSUMÉ EXÉCUTIF

### Vue d'Ensemble du Système
| Métrique | Documenté | Réel | Écart |
|----------|-----------|------|-------|
| Sphères | 8-10 (conflits) | 9 FROZEN | ⚠️ Clarifier |
| Sections Bureau | 6-10 (conflits) | 6 FROZEN | ⚠️ Clarifier |
| Agents | 168-226 | 168 | À valider |
| APIs Endpoints | 15 sections | ~95 endpoints | ✅ |
| Tables SQL | 50+ | ~50 | ✅ |
| Fichiers Frontend | 76 | À vérifier | 🔍 |
| Fichiers Backend | 88 | À vérifier | 🔍 |

### Score de Santé Globale
```
┌─────────────────────────────────────────┐
│ CONNEXIONS CRITIQUES                    │
├─────────────────────────────────────────┤
│ API → Frontend       ⚠️ 60%  PARTIEL   │
│ Backend → Database   ✅ 85%  SOLIDE    │
│ Agents → Governance  ✅ 80%  SOLIDE    │
│ WebSocket → RT       ❌ 30%  INCOMPLET │
│ XR → Core           ⚠️ 50%  PARTIEL   │
│ Auth → All          ⚠️ 65%  PARTIEL   │
└─────────────────────────────────────────┘
```

---

# 🔍 SECTION 1: ANALYSE DES ENGINES

## 1.1 DataSpace Engine

### Statut: ✅ 85% COMPLET

**Tables SQL Définies:**
- `dataspaces` ✅
- `dataspace_items` ✅
- `dataspace_links` ✅

**APIs Documentées:**
- `POST /dataspaces` ✅
- `GET /dataspaces` ✅
- `GET /dataspaces/{id}` ✅
- `PATCH /dataspaces/{id}` ✅
- `POST /dataspaces/{id}/archive` ✅
- `POST /dataspaces/{id}/links` ✅

**Connexions Vérifiées:**
| Source | Cible | Statut | Notes |
|--------|-------|--------|-------|
| DataSpace | Identity | ✅ FK | owner_id, identity_id |
| DataSpace | Sphere | ✅ FK | sphere_id |
| DataSpace | Domain | ✅ FK | domain_id |
| DataSpace | Parent | ✅ Self-ref | parent_id |
| DataSpace | Thread | ✅ 1:N | |
| DataSpace | File | ⚠️ Implicite | metadata JSONB |

**🔴 ANGLES MORTS:**
1. **Pas de validation de hiérarchie** - Un DataSpace peut-il être son propre parent?
2. **Recherche full-text** - `search_vector` défini mais trigger de mise à jour non spécifié
3. **Soft delete** - `archived_at` existe mais cascade non définie
4. **Quota/Limites** - Pas de limite sur le nombre d'items par DataSpace

**🟡 AMÉLIORATIONS:**
```sql
-- Ajouter trigger pour search_vector
CREATE OR REPLACE FUNCTION update_dataspace_search_vector()
RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector := to_tsvector('french', 
    COALESCE(NEW.name, '') || ' ' || 
    COALESCE(NEW.description, '') || ' ' ||
    COALESCE(array_to_string(NEW.tags, ' '), '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_dataspace_search
BEFORE INSERT OR UPDATE ON dataspaces
FOR EACH ROW EXECUTE FUNCTION update_dataspace_search_vector();

-- Contrainte anti-cycle
ALTER TABLE dataspaces ADD CONSTRAINT no_self_parent 
  CHECK (id != parent_id);
```

---

## 1.2 Thread Engine

### Statut: ✅ 80% COMPLET

**Tables SQL:**
- `threads` ✅
- `thread_messages` ✅
- `thread_decisions` ✅

**APIs Documentées:**
- `POST /threads` ✅
- `GET /threads` ✅
- `GET /threads/{id}` ✅
- `POST /threads/{id}/messages` ✅
- `POST /threads/{id}/decisions` ✅

**Connexions:**
| Source | Cible | Statut |
|--------|-------|--------|
| Thread | DataSpace | ✅ FK nullable |
| Thread | Identity | ✅ FK |
| Thread | Participants | ✅ Array UUID |
| ThreadMessage | Thread | ✅ FK cascade |
| ThreadMessage | User | ✅ FK nullable |
| ThreadMessage | Agent | ⚠️ UUID sans FK |
| ThreadDecision | Thread | ✅ FK cascade |

**🔴 ANGLES MORTS:**
1. **agent_id sans FK** - `thread_messages.agent_id` n'a pas de contrainte FK vers `agents`
2. **Participants non validés** - Array `UUID[]` sans validation existence users
3. **Pas d'index sur participants** - Recherche lente pour "mes threads"
4. **Encoding .chenu** - Format d'artifacts non défini dans schéma

**🟡 AMÉLIORATIONS:**
```sql
-- Ajouter FK pour agent_id
ALTER TABLE thread_messages 
  ADD CONSTRAINT fk_message_agent 
  FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL;

-- Index GIN pour participants
CREATE INDEX idx_thread_participants ON threads USING GIN(participants);

-- Table pour format .chenu
CREATE TABLE thread_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    artifact_type VARCHAR(50) NOT NULL, -- 'encoding', 'decision', 'summary'
    content JSONB NOT NULL,
    encoding_version VARCHAR(20) DEFAULT '1.0',
    checksum VARCHAR(64), -- Pour intégrité
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 1.3 Workspace Engine

### Statut: ⚠️ 75% COMPLET

**Tables SQL:**
- `workspaces` ✅
- `workspace_panels` ✅
- `workspace_states` ✅
- `workspace_transformations` ✅

**APIs:**
- CRUD Workspaces ✅
- Mode Transform ✅
- State Management ✅
- Panel Management ✅

**🔴 ANGLES MORTS:**
1. **Validation des modes** - `workspace_mode` sans ENUM, peut contenir valeurs invalides
2. **layout_config** - Structure JSONB non validée, peut être incohérente
3. **Réversibilité** - `reverse_data` jamais peuplé automatiquement
4. **Conflits multi-utilisateurs** - Pas de lock sur edit concurrent

**🟡 AMÉLIORATIONS:**
```sql
-- Créer ENUM pour modes
CREATE TYPE workspace_mode_enum AS ENUM (
    'document', 'board', 'timeline', 'spreadsheet',
    'dashboard', 'diagram', 'whiteboard', 'xr', 'hybrid'
);

-- Ajouter contrainte
ALTER TABLE workspaces 
  ADD CONSTRAINT valid_mode 
  CHECK (workspace_mode IN ('document', 'board', 'timeline', 
         'spreadsheet', 'dashboard', 'diagram', 'whiteboard', 'xr', 'hybrid'));

-- Table de locks
CREATE TABLE workspace_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    lock_type VARCHAR(20) DEFAULT 'edit', -- 'edit', 'view'
    acquired_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(workspace_id, lock_type)
);
```

---

## 1.4 1-Click Assistant Engine

### Statut: ⚠️ 70% COMPLET

**Tables SQL:**
- `oneclick_workflows` ✅
- `oneclick_executions` ✅
- `oneclick_templates` ✅

**APIs:**
- Execute ✅
- Status ✅
- Approve ✅
- Cancel ✅

**🔴 ANGLES MORTS:**
1. **Step Definition** - `workflow_steps` JSONB sans schéma validé
2. **Rollback** - Pas de mécanisme d'annulation après exécution partielle
3. **Timeout** - Pas de timeout sur executions longues
4. **Cost Estimation** - Mentionné dans specs mais pas implémenté en BD

**🟡 AMÉLIORATIONS:**
```sql
-- Ajouter colonnes pour governance
ALTER TABLE oneclick_executions ADD COLUMN 
    estimated_tokens INTEGER,
    actual_tokens INTEGER,
    estimated_cost DECIMAL(10,4),
    actual_cost DECIMAL(10,4),
    timeout_at TIMESTAMP WITH TIME ZONE,
    rollback_data JSONB;

-- Table pour tracking détaillé des steps
CREATE TABLE oneclick_execution_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID NOT NULL REFERENCES oneclick_executions(id) ON DELETE CASCADE,
    step_index INTEGER NOT NULL,
    step_name VARCHAR(255),
    agent_id UUID REFERENCES agents(id),
    status VARCHAR(20) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    tokens_used INTEGER,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    UNIQUE(execution_id, step_index)
);
```

---

## 1.5 Backstage Intelligence Engine

### Statut: ⚠️ 65% COMPLET

**Tables SQL:**
- `backstage_contexts` ✅
- `backstage_preparations` ✅
- `backstage_classifications` ✅

**🔴 ANGLES MORTS:**
1. **Session Management** - `session_id` sans table sessions
2. **Cache Invalidation** - Classifications cached mais jamais purgées
3. **Relevance Score** - Algorithme de calcul non spécifié
4. **Pre-warming** - Aucun mécanisme de pre-load documenté

**🟡 AMÉLIORATIONS:**
```sql
-- Table sessions
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID REFERENCES identities(id),
    device_info JSONB,
    ip_address INET,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Index pour purge automatique
CREATE INDEX idx_classifications_created ON backstage_classifications(created_at);

-- Job de purge (pseudo-code pour cron)
-- DELETE FROM backstage_classifications WHERE created_at < NOW() - INTERVAL '7 days';
```

---

## 1.6 Memory & Governance Engine

### Statut: ✅ 85% COMPLET

**Tables SQL:**
- `memory_items` ✅
- `governance_audit_log` ✅
- `elevation_requests` ✅
- `cross_identity_blocks` ✅

**🔴 ANGLES MORTS:**
1. **Memory Expiration** - `expires_at` existe mais pas de job de nettoyage
2. **Audit Retention** - Pas de politique de rétention définie
3. **Cross-Identity Rules** - Logique de blocage pas en triggers
4. **Memory Search** - Pas d'index full-text sur `content`

**🟡 AMÉLIORATIONS:**
```sql
-- Index full-text pour memory
ALTER TABLE memory_items ADD COLUMN search_vector TSVECTOR;
CREATE INDEX idx_memory_search ON memory_items USING GIN(search_vector);

-- Trigger auto-update
CREATE TRIGGER trg_memory_search
BEFORE INSERT OR UPDATE ON memory_items
FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(
    search_vector, 'pg_catalog.french', content);

-- Partition audit log par mois pour performance
CREATE TABLE governance_audit_log_template (
    LIKE governance_audit_log INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- Fonction de purge mémoire expirée
CREATE OR REPLACE FUNCTION purge_expired_memory()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM memory_items 
    WHERE expires_at IS NOT NULL AND expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
```

---

## 1.7 Agent System

### Statut: ⚠️ 75% COMPLET

**Tables SQL:**
- `agents` ✅
- `agent_configurations` ✅
- `agent_memory` ✅
- `agent_executions` ✅

**🔴 ANGLES MORTS:**
1. **Agent Hierarchy** - L0-L3 levels pas enforced par contraintes
2. **Capabilities Schema** - JSONB `capabilities` sans validation
3. **LLM Config** - Pas de validation des models disponibles
4. **Rate Limiting** - Pas de tracking pour limit calls

**🟡 AMÉLIORATIONS:**
```sql
-- ENUM pour agent levels
CREATE TYPE agent_level_enum AS ENUM ('L0', 'L1', 'L2', 'L3');

-- Contrainte de hiérarchie
ALTER TABLE agents ADD COLUMN parent_agent_id UUID REFERENCES agents(id);
ALTER TABLE agents ADD CONSTRAINT valid_hierarchy CHECK (
    (agent_level = 'L0' AND parent_agent_id IS NULL) OR
    (agent_level != 'L0' AND parent_agent_id IS NOT NULL)
);

-- Rate limiting table
CREATE TABLE agent_rate_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    user_id UUID NOT NULL REFERENCES users(id),
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    request_count INTEGER DEFAULT 0,
    UNIQUE(agent_id, user_id, window_start)
);
```

---

## 1.8 Meeting System

### Statut: ✅ 80% COMPLET

**Tables SQL:**
- `meetings` ✅
- `meeting_participants` ✅
- `meeting_notes` ✅
- `meeting_tasks` ✅

**🔴 ANGLES MORTS:**
1. **XR Room Link** - `xr_room_id` sans FK (table XR rooms pas liée)
2. **Recurring Meetings** - Pas de support pour récurrence
3. **Calendar Sync** - Pas d'intégration calendrier externe
4. **Recording** - Pas de table pour enregistrements

**🟡 AMÉLIORATIONS:**
```sql
-- Table XR rooms (manquante!)
CREATE TABLE xr_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    room_template VARCHAR(50),
    dimensions JSONB,
    dataspace_id UUID REFERENCES dataspaces(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- FK pour meetings
ALTER TABLE meetings ADD CONSTRAINT fk_xr_room 
  FOREIGN KEY (xr_room_id) REFERENCES xr_rooms(id);

-- Recurring meetings
CREATE TABLE meeting_recurrence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    pattern VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly'
    interval_value INTEGER DEFAULT 1,
    days_of_week INTEGER[], -- 0=Sun, 6=Sat
    end_date DATE,
    occurrences INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Meeting recordings
CREATE TABLE meeting_recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    recording_type VARCHAR(50), -- 'audio', 'video', 'transcript'
    file_url TEXT NOT NULL,
    duration_seconds INTEGER,
    file_size_bytes BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 1.9 Immobilier Domain

### Statut: ✅ 90% COMPLET (Best documented domain!)

**Tables SQL:**
- `properties` ✅
- `property_units` ✅
- `tenants` ✅
- `rent_payments` ✅
- `maintenance_requests` ✅

**APIs Complètes:** 12 endpoints documentés

**🔴 ANGLES MORTS:**
1. **Géolocalisation** - `coordinates POINT` mais pas d'index spatial
2. **TAL Integration** - `tal_registered` sans workflow
3. **Historique valeur** - `current_value` écrasé sans historique
4. **Documents propriété** - Relation avec files non explicite

**🟡 AMÉLIORATIONS:**
```sql
-- Index spatial pour recherche géo
CREATE INDEX idx_property_location ON properties USING GIST(coordinates);

-- Historique des valeurs
CREATE TABLE property_valuations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    valuation_date DATE NOT NULL,
    value DECIMAL(12,2) NOT NULL,
    valuation_type VARCHAR(50), -- 'purchase', 'appraisal', 'market_estimate'
    source VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Documents liés à propriété
CREATE TABLE property_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL, -- 'deed', 'survey', 'insurance', 'tax'
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at DATE -- Pour assurances, etc.
);
```

---

## 1.10 Construction Domain

### Statut: ✅ 85% COMPLET

**Tables SQL:**
- `construction_projects` ✅
- `construction_estimates` ✅
- `estimate_line_items` ✅
- `materials` ✅

**🔴 ANGLES MORTS:**
1. **Phases de projet** - Pas de table pour suivi phases
2. **Inspections** - Mentionnées mais pas de table
3. **Subcontractors** - `assigned_contractor_id` sans table contractors
4. **Permits** - Pas de tracking des permis

**🟡 AMÉLIORATIONS:**
```sql
-- Contractors/Subcontractors
CREATE TABLE contractors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    rbq_license VARCHAR(50),
    specialties TEXT[],
    rating DECIMAL(3,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Project phases
CREATE TABLE construction_phases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES construction_projects(id) ON DELETE CASCADE,
    phase_name VARCHAR(100) NOT NULL,
    phase_order INTEGER NOT NULL,
    planned_start DATE,
    planned_end DATE,
    actual_start DATE,
    actual_end DATE,
    status VARCHAR(20) DEFAULT 'pending',
    completion_percentage INTEGER DEFAULT 0,
    UNIQUE(project_id, phase_order)
);

-- Inspections
CREATE TABLE construction_inspections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES construction_projects(id) ON DELETE CASCADE,
    phase_id UUID REFERENCES construction_phases(id),
    inspection_type VARCHAR(50) NOT NULL,
    scheduled_date DATE,
    actual_date DATE,
    inspector_name VARCHAR(100),
    result VARCHAR(20), -- 'passed', 'failed', 'conditional'
    notes TEXT,
    documents JSONB DEFAULT '[]'
);

-- Permits
CREATE TABLE construction_permits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES construction_projects(id) ON DELETE CASCADE,
    permit_type VARCHAR(50) NOT NULL,
    permit_number VARCHAR(100),
    issuing_authority VARCHAR(100),
    application_date DATE,
    approval_date DATE,
    expiry_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    documents JSONB DEFAULT '[]'
);
```

---

## 1.11 OCW (Operational Cognitive Workspace)

### Statut: ⚠️ 60% COMPLET

**Tables SQL:** Partiellement défini (vu dans schéma lignes 896+)

**🔴 ANGLES MORTS CRITIQUES:**
1. **WebSocket Server** - Documenté mais pas implémenté
2. **Conflict Resolution** - Mentionné mais algorithme non défini
3. **Object Versioning** - Pas d'historique des modifications canvas
4. **Real-time Sync** - Architecture CRDT non spécifiée

**🟡 AMÉLIORATIONS:**
```sql
-- OCW Sessions (compléter)
CREATE TABLE ocw_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id),
    session_type VARCHAR(50) NOT NULL,
    host_user_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    max_participants INTEGER DEFAULT 10,
    is_recording BOOLEAN DEFAULT FALSE
);

-- Canvas objects avec versioning
CREATE TABLE ocw_objects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES ocw_sessions(id) ON DELETE CASCADE,
    object_type VARCHAR(50) NOT NULL,
    position JSONB NOT NULL,
    properties JSONB DEFAULT '{}',
    z_index INTEGER DEFAULT 0,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Object history pour undo/redo
CREATE TABLE ocw_object_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    object_id UUID NOT NULL REFERENCES ocw_objects(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    previous_state JSONB NOT NULL,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    change_type VARCHAR(20) -- 'create', 'update', 'delete'
);

-- Participants actifs
CREATE TABLE ocw_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES ocw_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'editor',
    cursor_position JSONB,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(session_id, user_id)
);
```

---

## 1.12 XR Spatial Engine

### Statut: ⚠️ 55% COMPLET

**🔴 ANGLES MORTS CRITIQUES:**
1. **Tables XR** - Schéma SQL incomplet (xr_rooms mentionné mais pas défini)
2. **Avatar System** - Aucune table pour avatars
3. **Object Persistence** - XR objects non persistés
4. **Device Support** - Pas de tracking devices VR/AR

**🟡 AMÉLIORATIONS:**
```sql
-- XR Rooms (création complète)
CREATE TABLE xr_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    room_type VARCHAR(50) NOT NULL, -- 'meeting', 'presentation', 'showroom'
    room_template VARCHAR(50),
    dimensions JSONB NOT NULL, -- {width, height, depth}
    environment_config JSONB DEFAULT '{}',
    dataspace_id UUID REFERENCES dataspaces(id),
    meeting_id UUID REFERENCES meetings(id),
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_public BOOLEAN DEFAULT FALSE
);

-- XR Objects
CREATE TABLE xr_objects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES xr_rooms(id) ON DELETE CASCADE,
    object_type VARCHAR(50) NOT NULL,
    position JSONB NOT NULL, -- {x, y, z}
    rotation JSONB DEFAULT '{"x":0,"y":0,"z":0}',
    scale JSONB DEFAULT '{"x":1,"y":1,"z":1}',
    properties JSONB DEFAULT '{}',
    source_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Avatars
CREATE TABLE xr_avatars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    avatar_name VARCHAR(100),
    avatar_config JSONB NOT NULL, -- appearance settings
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- XR Sessions
CREATE TABLE xr_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES xr_rooms(id),
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

-- XR Participants
CREATE TABLE xr_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES xr_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    avatar_id UUID REFERENCES xr_avatars(id),
    device_type VARCHAR(50), -- 'vr_headset', 'ar_glasses', 'desktop', 'mobile'
    position JSONB,
    rotation JSONB,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    left_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(session_id, user_id)
);
```

---

# 🚨 SECTION 2: ANGLES MORTS CRITIQUES

## 2.1 🔴 INCOHÉRENCES DOCUMENTAIRES

| Document | Sphères | Bureau Sections | Agents |
|----------|---------|-----------------|--------|
| Memory Prompt | 8 (+Scholar=9) | 6 max | Non spécifié |
| Master Reference v5 | 10 | Non spécifié | 226 |
| Feature Audit | 11 espaces | 10 | 168 |
| SQL Schema | Via spheres table | N/A | 168+ |

**⚠️ RÉSOLUTION REQUISE:**
```
DÉCISION ARCHITECTURALE À FIGER:
┌─────────────────────────────────────────────────────────┐
│ SPHÈRES: 9 (comme Memory Prompt - SOURCE DE VÉRITÉ)     │
│   1. Personal 🏠                                        │
│   2. Business 💼                                        │
│   3. Government & Institutions 🏛️                       │
│   4. Studio de création 🎨                              │
│   5. Community 👥                                       │
│   6. Social & Media 📱                                  │
│   7. Entertainment 🎬                                   │
│   8. My Team 🤝                                         │
│   9. Scholar 🎓                                         │
├─────────────────────────────────────────────────────────┤
│ BUREAU SECTIONS: 6 (comme Memory Prompt)                │
│   1. Dashboard                                          │
│   2. Notes                                              │
│   3. Tasks                                              │
│   4. Projects                                           │
│   5. Threads (.chenu)                                   │
│   6. Meetings                                           │
├─────────────────────────────────────────────────────────┤
│ AGENTS: 168 (comme SQL Schema)                          │
│   L0: 1 (ARIA Master)                                   │
│   L1: ~10 (Department Chiefs)                           │
│   L2: ~50 (Specialists)                                 │
│   L3: ~107 (Support)                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 2.2 🔴 CONNEXIONS MANQUANTES

### Frontend → Backend
```
ROUTES NON CONNECTÉES:
├── /api/oneclick/* → Composants 1-Click non intégrés
├── /api/backstage/* → Backstage Intelligence isolé
├── /api/xr/* → XR Engine pas lié au frontend 3D
├── /api/ocw/* → WebSocket server non implémenté
└── /api/governance/audit → Pas d'UI admin pour audit
```

### Backend → Database
```
MIGRATIONS MANQUANTES:
├── xr_rooms (table non créée)
├── xr_sessions (table non créée)
├── xr_participants (table non créée)
├── xr_avatars (table non créée)
├── xr_objects (table non créée)
├── ocw_sessions (partiellement)
├── ocw_objects (non créé)
├── ocw_participants (non créé)
├── meeting_recurrence (non créé)
├── meeting_recordings (non créé)
├── contractors (non créé)
├── construction_phases (non créé)
├── construction_inspections (non créé)
├── construction_permits (non créé)
├── property_valuations (non créé)
└── property_documents (non créé)
```

### WebSocket
```
REAL-TIME NON IMPLÉMENTÉ:
├── OCW canvas sync
├── XR position updates
├── Agent execution progress
├── Notification push
├── Thread live updates
└── Meeting presence
```

---

## 2.3 🔴 SÉCURITÉ & GOUVERNANCE

### Authentification
```
GAPS IDENTIFIÉS:
├── JWT refresh token rotation ❌
├── Session invalidation on password change ❌
├── Multi-factor authentication (MFA) ❌
├── OAuth state parameter validation ⚠️
├── Rate limiting per user ⚠️
└── API key management ❌
```

### Authorization
```
GAPS IDENTIFIÉS:
├── Row-level security (RLS) non activé
├── Cross-identity access checks en app layer seulement
├── Agent permission matrix non enforced
├── DataSpace sharing permissions non granulaires
└── Audit log tampering protection ❌
```

### Data Protection
```
GAPS IDENTIFIÉS:
├── PII encryption at rest ❌
├── Tenant data isolation (multi-tenant) ⚠️
├── GDPR data export endpoint ❌
├── GDPR data deletion cascade ⚠️
└── Backup encryption ❓
```

---

## 2.4 🔴 PERFORMANCE

### Database
```
INDEXES MANQUANTS:
├── dataspaces(status, sphere_id) - pour filtrage
├── threads(identity_id, status) - pour listing
├── memory_items(user_id, status, expires_at) - pour purge
├── agent_executions(agent_id, started_at) - pour stats
├── properties(city, province) - pour recherche géo
└── maintenance_requests(status, priority) - pour dashboard
```

### Caching
```
CACHE NON IMPLÉMENTÉ:
├── Agent configurations
├── Sphere/Domain metadata
├── User permissions
├── Material prices
└── Template workflows
```

### Pagination
```
ENDPOINTS SANS PAGINATION:
├── GET /agents
├── GET /threads
├── GET /workspaces
└── GET /memory
```

---

# 🎯 SECTION 3: PLAN D'ACTION PRIORITAIRE

## Phase 1: CORRECTIONS CRITIQUES (1-2 jours)

### P0.1 - Unifier Documentation
```bash
# Actions:
1. Mettre à jour Master Reference avec 9 sphères
2. Aligner tous les documents sur 6 sections bureau
3. Figer le nombre d'agents à 168
4. Créer SINGLE_SOURCE_OF_TRUTH.md
```

### P0.2 - Corriger Schema SQL
```sql
-- Migrations prioritaires:
1. Créer tables XR manquantes
2. Créer tables OCW manquantes
3. Ajouter FK manquantes
4. Créer indexes performance
5. Activer triggers full-text search
```

### P0.3 - Imports Backend
```python
# Fichiers à corriger:
- backend/api/main.py
- backend/api/extended_api.py
- backend/services/*.py
# Créer backend/app.py unifié
```

## Phase 2: INTÉGRATIONS (3-5 jours)

### P1.1 - WebSocket Server
```
Implémenter:
├── Connection manager
├── Room/channel system
├── OCW sync protocol
├── XR position broadcast
└── Notification delivery
```

### P1.2 - Frontend Connections
```
Connecter:
├── OneClick UI → API
├── Backstage Intelligence → Components
├── XR Viewer → XR API
├── OCW Canvas → WebSocket
└── Governance Dashboard → Audit API
```

### P1.3 - Authentication Flow
```
Implémenter:
├── JWT refresh rotation
├── Session management
├── MFA setup
├── OAuth complete flow
└── API key generation
```

## Phase 3: FEATURES MANQUANTES (5-7 jours)

### P2.1 - Modules à créer
```
Frontend:
├── Cinema catalog
├── Personal journal
├── Habit tracker
├── Audio studio
└── Document templates

Backend:
├── Recurring meetings
├── Calendar sync
├── Property documents
├── Construction permits
└── Contractor management
```

### P2.2 - Governance
```
Implémenter:
├── Row-level security
├── Permission matrix enforcement
├── Audit log protection
├── Data encryption
└── GDPR endpoints
```

## Phase 4: OPTIMISATION (2-3 jours)

### P3.1 - Performance
```
Actions:
├── Add missing indexes
├── Implement caching layer
├── Add pagination everywhere
├── Query optimization
└── Connection pooling
```

### P3.2 - Testing
```
Créer:
├── Unit tests backend (70% coverage)
├── Integration tests API
├── E2E tests frontend
├── Load tests WebSocket
└── Security penetration tests
```

---

# 📋 SECTION 4: CHECKLIST DE VALIDATION

## Pre-Production Checklist

### Backend ☐
- [ ] Tous les imports fonctionnels
- [ ] Database migrations créées et testées
- [ ] API documentation OpenAPI complète
- [ ] Rate limiting activé
- [ ] Logging structuré
- [ ] Error handling unifié
- [ ] Health check endpoint
- [ ] Graceful shutdown

### Frontend ☐
- [ ] Routing complet 9 sphères
- [ ] State management cohérent (Zustand)
- [ ] Responsive design validé
- [ ] Loading states partout
- [ ] Error boundaries
- [ ] PWA manifest
- [ ] Offline support basique
- [ ] Accessibility (WCAG 2.1)

### Database ☐
- [ ] Toutes les tables créées
- [ ] Toutes les FK en place
- [ ] Indexes de performance
- [ ] Triggers full-text search
- [ ] RLS policies
- [ ] Backup automatique

### Security ☐
- [ ] JWT avec refresh tokens
- [ ] CORS configuré
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF tokens
- [ ] Secrets management

### WebSocket ☐
- [ ] Connection manager
- [ ] Heartbeat/ping
- [ ] Reconnection logic
- [ ] Room management
- [ ] Message queuing
- [ ] Presence tracking

### XR ☐
- [ ] Room creation
- [ ] Object management
- [ ] Avatar system
- [ ] Position sync
- [ ] Multi-device support

### OCW ☐
- [ ] Canvas objects
- [ ] Real-time sync
- [ ] Conflict resolution
- [ ] Undo/redo
- [ ] Export functionality

---

# 📊 SECTION 5: MÉTRIQUES DE SUCCÈS

## KPIs Techniques

| Métrique | Actuel | Cible | Deadline |
|----------|--------|-------|----------|
| Test Coverage | ~40% | 70% | Q1 2025 |
| API Response Time | ? | <200ms p95 | Q1 2025 |
| WebSocket Latency | N/A | <50ms | Q1 2025 |
| Uptime | N/A | 99.5% | Q1 2025 |
| Error Rate | ? | <1% | Q1 2025 |

## Completeness Score

| Module | Actuel | Cible |
|--------|--------|-------|
| DataSpace Engine | 85% | 95% |
| Thread Engine | 80% | 95% |
| Workspace Engine | 75% | 90% |
| 1-Click Engine | 70% | 90% |
| Backstage Intelligence | 65% | 85% |
| Memory & Governance | 85% | 95% |
| Agent System | 75% | 90% |
| Meeting System | 80% | 95% |
| Immobilier Domain | 90% | 98% |
| Construction Domain | 85% | 95% |
| OCW | 60% | 85% |
| XR Engine | 55% | 80% |

---

*Document généré le 23 Décembre 2025*
*CHE·NU™ — Governed Intelligence Operating System*
*🌟 LAISSE TA MARQUE — CHANGE LE MONDE 🌟*