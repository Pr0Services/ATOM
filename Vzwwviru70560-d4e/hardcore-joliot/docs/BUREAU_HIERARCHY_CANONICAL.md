# 🏢 CHE·NU™ — BUREAU HIERARCHY
## Documentation Canonique v33 — FROZEN
## ⚠️ NE JAMAIS MODIFIER CETTE STRUCTURE

---

## 🎯 DÉFINITION

> **Bureau = Espace d'ORIENTATION (pas d'exécution)**
> 
> Les Bureaux guident. Les Workspaces exécutent.

---

## 📐 HIÉRARCHIE DES 5 NIVEAUX (FROZEN)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│   NIVEAU 0: GLOBAL BUREAU (1 seul)                                              │
│   ├── 5 sections                                                                │
│   │                                                                              │
│   └──► NIVEAU 1: IDENTITY BUREAU (1 par identité)                               │
│        ├── 4 sections                                                           │
│        │                                                                         │
│        └──► NIVEAU 2: SPHERE BUREAU (8 par identité) ◄── MAX 6 SECTIONS        │
│             ├── 6 sections (HARD LIMIT)                                         │
│             │                                                                    │
│             └──► NIVEAU 3: PROJECT BUREAU (optionnel)                           │
│                  ├── 4 sections                                                 │
│                  │                                                               │
│                  └──► NIVEAU 4: AGENT BUREAU (observationnel)                   │
│                       └── 4 sections                                            │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔷 L0: GLOBAL BUREAU (5 sections)

**But:** Point d'entrée unique, sélection d'identité

| # | Section | Type | Description |
|---|---------|------|-------------|
| 1 | Identity Selector | `identity_selector` | Choisir l'identité active |
| 2 | Recent Activity | `recent_activity` | Activité récente globale |
| 3 | Pinned Workspaces | `pinned_workspaces` | Espaces épinglés |
| 4 | Notifications | `notifications` | Alertes système |
| 5 | Nova Entry | `nova_entry` | Point d'entrée Nova |

---

## 🔷 L1: IDENTITY BUREAU (4 sections)

**But:** Vue d'ensemble d'une identité

| # | Section | Type | Description |
|---|---------|------|-------------|
| 1 | Identity Summary | `identity_summary` | Résumé de l'identité |
| 2 | Active Spheres | `active_spheres` | Sphères actives |
| 3 | Identity Threads | `identity_threads` | Threads de l'identité |
| 4 | Budget Overview | `budget_overview` | Vue budget/tokens |

---

## 🔷 L2: SPHERE BUREAU — MAX 6 SECTIONS (HARD LIMIT) ⚠️

**But:** Orientation dans une sphère spécifique

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SPHERE BUREAU (ex: Business 💼)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ 1. Quick Capture │  │ 2. Resume Work   │  │ 3. Threads       │              │
│  │       📝         │  │       ▶️         │  │       💬         │              │
│  │  500 char max    │  │  Continue work   │  │  .chenu files    │              │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘              │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ 4. Data/Files    │  │ 5. Active Agents │  │ 6. Meetings      │              │
│  │       📁         │  │       🤖         │  │       📅         │              │
│  │  Documents       │  │  Agent status    │  │  Calendar        │              │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘              │
│                                                                                  │
│                    ⚠️ MAXIMUM 6 SECTIONS — JAMAIS PLUS                         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Les 6 Sections Détaillées

| # | Section | Type | Description | Limite |
|---|---------|------|-------------|--------|
| 1 | **Quick Capture** | `quick_capture` | Prise rapide de notes/idées | 500 char max |
| 2 | **Resume Workspace** | `resume_workspace` | Reprendre travail en cours | Liste workspaces actifs |
| 3 | **Threads** | `threads` | Conversations sphere-scoped | Fichiers .chenu |
| 4 | **Data/Files** | `data_files` | Fichiers et documents | Storage indicator |
| 5 | **Active Agents** | `active_agents` | Agents actifs dans la sphère | Status + progress |
| 6 | **Meetings** | `meetings` | Réunions et calendrier | Upcoming + recent |

---

## 🔷 L3: PROJECT BUREAU (4 sections)

**But:** Vue projet spécifique (optionnel)

| # | Section | Type | Description |
|---|---------|------|-------------|
| 1 | Project Overview | `project_overview` | Vue d'ensemble projet |
| 2 | Linked Workspaces | `linked_workspaces` | Workspaces liés |
| 3 | Project Timeline | `project_timeline` | Timeline projet |
| 4 | Assigned Agents | `assigned_agents` | Agents assignés |

---

## 🔷 L4: AGENT BUREAU (4 sections)

**But:** Observation des agents (JAMAIS d'exécution directe)

| # | Section | Type | Description |
|---|---------|------|-------------|
| 1 | Agent Status | `agent_status` | État de l'agent |
| 2 | Agent Plans | `agent_plans` | Plans en cours |
| 3 | Staging Outputs | `staging_outputs` | Outputs en staging |
| 4 | Agent History | `agent_history` | Historique agent |

---

## 🌐 LES 8 SPHÈRES (FROZEN)

Chaque identité a accès à 8 Sphere Bureaux:

| # | Sphère | Code | Emoji |
|---|--------|------|-------|
| 1 | Personal | `personal` | 🏠 |
| 2 | Business | `business` | 💼 |
| 3 | Government & Institutions | `government` | 🏛️ |
| 4 | Studio de création | `creative_studio` | 🎨 |
| 5 | Community | `community` | 👥 |
| 6 | Social & Media | `social_media` | 📱 |
| 7 | Entertainment | `entertainment` | 🎬 |
| 8 | My Team | `my_team` | 🤝 |

---

## 📊 COMPTAGE TOTAL

Pour 1 utilisateur avec 1 identité:

```
L0 Global Bureau:     1 bureau  ×  5 sections =   5 sections
L1 Identity Bureau:   1 bureau  ×  4 sections =   4 sections
L2 Sphere Bureaux:    8 bureaux ×  6 sections =  48 sections
─────────────────────────────────────────────────────────────
TOTAL:               10 bureaux × ~57 sections
```

---

## 🔒 RÈGLES STRICTES

### ✅ DO
- Utiliser les bureaux pour l'ORIENTATION
- Lier vers les Workspaces pour le TRAVAIL
- Auto-créer à la première visite
- Traquer la navigation

### ❌ DON'T
- **JAMAIS** éditer directement dans un Bureau
- **JAMAIS** fusionner Bureau & Workspace
- **JAMAIS** dépasser 6 sections (Sphere Bureau)
- **JAMAIS** accéder aux données cross-identité

---

## 💻 CODE REFERENCE

### Enum BureauLevel
```python
class BureauLevel(str, Enum):
    GLOBAL = "global"      # L0
    IDENTITY = "identity"  # L1
    SPHERE = "sphere"      # L2
    PROJECT = "project"    # L3
    AGENT = "agent"        # L4
```

### Enum BureauSectionType
```python
class BureauSectionType(str, Enum):
    # SPHERE BUREAU SECTIONS (L2) - MAX 6
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"
    
    # IDENTITY BUREAU SECTIONS (L1)
    IDENTITY_SUMMARY = "identity_summary"
    ACTIVE_SPHERES = "active_spheres"
    IDENTITY_THREADS = "identity_threads"
    BUDGET_OVERVIEW = "budget_overview"
    
    # GLOBAL BUREAU SECTIONS (L0)
    IDENTITY_SELECTOR = "identity_selector"
    RECENT_ACTIVITY = "recent_activity"
    PINNED_WORKSPACES = "pinned_workspaces"
    NOTIFICATIONS = "notifications"
    NOVA_ENTRY = "nova_entry"
    
    # PROJECT BUREAU SECTIONS (L3)
    PROJECT_OVERVIEW = "project_overview"
    LINKED_WORKSPACES = "linked_workspaces"
    PROJECT_TIMELINE = "project_timeline"
    ASSIGNED_AGENTS = "assigned_agents"
    
    # AGENT BUREAU SECTIONS (L4) - OBSERVATIONAL ONLY
    AGENT_STATUS = "agent_status"
    AGENT_PLANS = "agent_plans"
    STAGING_OUTPUTS = "staging_outputs"
    AGENT_HISTORY = "agent_history"
```

### API Response Example
```json
{
  "id": "uuid",
  "level": "sphere",
  "name": "Business Bureau",
  "sphere_id": "business",
  "sections": [
    { "section_type": "quick_capture", "title": "Quick Capture", "position": 0 },
    { "section_type": "resume_workspace", "title": "Resume Work", "position": 1 },
    { "section_type": "threads", "title": "Threads", "position": 2 },
    { "section_type": "data_files", "title": "Files", "position": 3 },
    { "section_type": "active_agents", "title": "Agents", "position": 4 },
    { "section_type": "meetings", "title": "Meetings", "position": 5 }
  ]
}
```

---

## 📅 HISTORIQUE

| Version | Date | Changement |
|---------|------|------------|
| v1.0 | 2025-12-17 | Structure 5 niveaux établie |
| v33 | 2025-12-18 | Documentation canonique créée |

---

## ⚠️ AVERTISSEMENT FINAL

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   CETTE STRUCTURE EST FIGÉE (FROZEN)                                          ║
║                                                                                ║
║   • 5 niveaux de bureaux                                                       ║
║   • Sphere Bureau = MAX 6 sections                                             ║
║   • 8 sphères par identité                                                     ║
║                                                                                ║
║   TOUTE MODIFICATION NÉCESSITE APPROBATION EXPLICITE DU FONDATEUR             ║
║                                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

*CHE·NU™ — Bureaux guide. Workspaces execute.*
*"Orientation before Execution"*
