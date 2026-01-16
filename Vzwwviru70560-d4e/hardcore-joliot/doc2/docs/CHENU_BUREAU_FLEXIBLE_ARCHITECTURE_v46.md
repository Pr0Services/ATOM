# CHE·NU™ — BUREAU & WORKSPACE FLEXIBLE ARCHITECTURE
## Document Canonique v46 — 23 Décembre 2025

---

# 🔐 ARCHITECTURE CANONIQUE (FROZEN)

## Vue d'Ensemble

CHE·NU utilise une architecture à **DEUX COUCHES** pour l'interface utilisateur:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COUCHE 1: BUREAU                                  │
│                    (Navigation & Points d'Entrée)                           │
│                                                                             │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   │ Quick    │ │ Resume   │ │ Threads  │ │ Data     │ │ Active   │ │ Meetings │
│   │ Capture  │ │ Workspace│ │ (.chenu) │ │ Files    │ │ Agents   │ │          │
│   └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
│        │            │            │            │            │            │
│        └────────────┴────────────┴─────┬──────┴────────────┴────────────┘
│                                        │
│                                        ▼
├─────────────────────────────────────────────────────────────────────────────┤
│                        COUCHE 2: WORKSPACE ENGINE                           │
│                      (Surface Adaptative & Flexible)                        │
│                                                                             │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│   │Document │ │ Board   │ │Timeline │ │Spread-  │ │Dashboard│              │
│   │  Mode   │ │  Mode   │ │  Mode   │ │sheet    │ │  Mode   │              │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘              │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                          │
│   │ Diagram │ │White-   │ │ XR Mode │ │ Hybrid  │                          │
│   │  Mode   │ │board    │ │         │ │  Mode   │                          │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘                          │
│                                                                             │
│              ↕ TRANSFORMATIONS SEAMLESS ↕                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 📋 COUCHE 1: BUREAU (6 Sections)

## Définition

Le **Bureau** est l'interface de navigation et les **points d'entrée** vers le travail. Il présente **6 sections** qui s'adaptent au contexte (sphère, domaine, utilisateur).

## Les 6 Sections Bureau (CANONICAL)

| # | Section | ID | Icon | Description |
|---|---------|-----|------|-------------|
| 1 | **Quick Capture** | `quick_capture` | 📝 | Capture rapide (500 car. max), notes vocales |
| 2 | **Resume Workspace** | `resume_workspace` | ▶️ | Reprendre le travail en cours |
| 3 | **Threads** | `threads` | 💬 | Fils de discussion persistants (.chenu) |
| 4 | **Data/Files** | `data_files` | 📁 | DataSpaces et gestion de fichiers |
| 5 | **Active Agents** | `active_agents` | 🤖 | Statut et contrôle des agents |
| 6 | **Meetings** | `meetings` | 📅 | Planification et gestion des réunions |

## Flexibilité du Bureau

### Adaptation par Sphère

Chaque sphère peut **prioriser différemment** les sections:

| Sphère | Sections Prioritaires | Sections Secondaires |
|--------|----------------------|---------------------|
| **Personal** | Quick Capture, Threads | Meetings, Active Agents |
| **Business** | Resume Workspace, Meetings | Active Agents, Data/Files |
| **Government** | Data/Files, Threads | Meetings, Quick Capture |
| **Creative Studio** | Quick Capture, Threads | Data/Files, Agents |
| **Community** | Threads, Meetings | Quick Capture, Data/Files |
| **Social & Media** | Quick Capture, Threads | Resume Workspace |
| **Entertainment** | Quick Capture, Data/Files | Threads, Meetings |
| **My Team** | Active Agents, Meetings | Resume Workspace |
| **Scholar** | Data/Files, Threads | Quick Capture |

### Adaptation par Domaine

| Domaine | Sections Mises en Avant | Configuration Spéciale |
|---------|------------------------|------------------------|
| **Construction** | Data/Files (plans), Meetings | Templates estimation |
| **Immobilier** | Data/Files (baux), Threads | Widget loyers |
| **Finance** | Data/Files, Resume Work | Dashboard budgets |
| **Architecture** | Data/Files, Agents | Mode XR rapide |

### Adaptation par Intent

L'intelligence détecte l'intention et réorganise:

```
"Je dois terminer mon rapport"
  → Resume Workspace en premier plan
  → Document Mode auto-sélectionné

"Nouvelle idée pour le projet"
  → Quick Capture s'ouvre
  → Suggestion vers Whiteboard Mode

"Réunion avec l'équipe dans 10 min"
  → Meetings en surbrillance
  → Préparation contexte automatique
```

---

# ⚙️ COUCHE 2: WORKSPACE ENGINE (Modes Adaptatifs)

## Définition

Le **Workspace Engine** est la surface de travail **adaptative** qui se transforme selon le contexte, l'intention et le type de données.

## Les 9 Modes du Workspace Engine

### A. Document Mode
```
┌─────────────────────────────────────────────────────────────┐
│ ┌───────────────────────────┐  ┌─────────────────────────┐ │
│ │                           │  │   AI Side Panel         │ │
│ │   Document Column         │  │  ┌─────────────────┐    │ │
│ │                           │  │  │ Suggestions     │    │ │
│ │   - Rich text editing     │  │  └─────────────────┘    │ │
│ │   - Templates domaine     │  │  ┌─────────────────┐    │ │
│ │   - Version control       │  │  │ Analysis        │    │ │
│ │                           │  │  └─────────────────┘    │ │
│ └───────────────────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Rédige un rapport", "Écris un document", upload .docx

### B. Board Mode (Kanban)
```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ À faire │  │En cours │  │ Review  │  │  Done   │        │
│  │─────────│  │─────────│  │─────────│  │─────────│        │
│  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │        │
│  │ │Task │ │  │ │Task │ │  │ │Task │ │  │ │Task │ │        │
│  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │        │
│  │ ┌─────┐ │  │         │  │         │  │         │        │
│  │ │Task │ │  │         │  │         │  │         │        │
│  │ └─────┘ │  │         │  │         │  │         │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Organise mes tâches", "Projet management", ouvre TaskList

### C. Timeline Mode (Gantt)
```
┌─────────────────────────────────────────────────────────────┐
│     Lun    Mar    Mer    Jeu    Ven    Sam    Dim          │
│  ┌──────────────────────────┐                              │
│  │  Phase 1: Planification  │                              │
│  └──────────────────────────┘                              │
│          ┌────────────────────────────────┐                │
│          │  Phase 2: Exécution           │                │
│          └────────────────────────────────┘                │
│                                  ┌───────────────┐         │
│                                  │ Phase 3: QA   │         │
│                                  └───────────────┘         │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Planifie ma semaine", "Montre le calendrier projet"

### D. Spreadsheet Mode
```
┌─────────────────────────────────────────────────────────────┐
│     A         B           C          D           E          │
│ ┌──────┬──────────┬──────────┬──────────┬──────────┐       │
│1│Item  │ Quantité │ Prix Unit│ Total    │ Notes    │       │
│ ├──────┼──────────┼──────────┼──────────┼──────────┤       │
│2│Bois  │    50    │  25.00   │ =B2*C2   │ Pin      │       │
│ ├──────┼──────────┼──────────┼──────────┼──────────┤       │
│3│Vis   │   200    │   0.15   │ =B3*C3   │ M6x40    │       │
│ └──────┴──────────┴──────────┴──────────┴──────────┘       │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Fais une estimation", "Calcule les coûts", upload .xlsx

### E. Dashboard Mode
```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  💰 Revenue  │  │  📊 Tasks    │  │  ⏱️ Time     │      │
│  │   $125,000   │  │   23/50      │  │   45h        │      │
│  │   +15% ↑     │  │   46%        │  │   -10% ↓     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    📈 Trend Chart                   │   │
│  │            ╱╲                                       │   │
│  │          ╱    ╲                  ╱                  │   │
│  │        ╱        ╲              ╱                    │   │
│  │  ─────╱          ╲────────────╱                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "État du projet", "KPIs", "Vue d'ensemble"

### F. Diagram Mode
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│        ┌─────────┐                                          │
│        │  Start  │                                          │
│        └────┬────┘                                          │
│             │                                               │
│             ▼                                               │
│        ┌─────────┐     Oui      ┌─────────┐                │
│        │Decision?├─────────────►│ Action A│                │
│        └────┬────┘              └─────────┘                │
│             │ Non                                           │
│             ▼                                               │
│        ┌─────────┐                                          │
│        │ Action B│                                          │
│        └─────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Dessine le flux", "Architecture système", "Diagramme"

### G. Whiteboard Mode
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌─────────┐                       ╭─────────╮            │
│   │ Sticky  │     ┌──────────┐     │ Free    │            │
│   │  Note   │     │  Shape   │     │ Drawing │            │
│   └─────────┘     └──────────┘     ╰─────────╯            │
│                                                             │
│        ✏️ Free drawing                  ┌──────────┐       │
│           ～～～～                       │  Frame   │       │
│                                        │  Group   │       │
│                                        └──────────┘       │
│                                                             │
│   [Agent Annotation Layer - toggleable]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
**Déclencheurs**: "Brainstorm", "Idées pour...", "Esquisse"

### H. XR Mode
```
                    ╱▓▓▓▓▓╲
                   ╱  3D   ╲
                  ╱  Space  ╲
                 ╱___________╲
                 
   • Property walkthrough
   • Meeting spatial
   • Design review
   • Construction visualization
```
**Déclencheurs**: "Visite virtuelle", "Mode VR", "Entrons dans..."

### I. Hybrid Mode
```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │                         │  │                         │  │
│  │    Document Mode        │  │      Board Mode         │  │
│  │                         │  │                         │  │
│  │  - Writing report       │  │  - Related tasks        │  │
│  │  - AI suggestions       │  │  - Progress tracking    │  │
│  │                         │  │                         │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```
**Configurations hybrides**:
- Document + Board: Rédaction avec suivi tâches
- Timeline + Spreadsheet: Planning avec ressources
- Dashboard + Board: Métriques avec actions
- Whiteboard + Document: Brainstorm vers formalisation

---

# 🔄 SYSTÈME DE TRANSFORMATION

## Déclencheurs de Transformation

Le Workspace Engine détecte l'intention via:

| Signal | Exemple | Action |
|--------|---------|--------|
| **Verbal/Texte** | "Planifie ma semaine" | → Timeline Mode |
| **Type fichier** | Upload .xlsx | → Spreadsheet Mode |
| **Domaine** | Termes construction | → Activer outils construction |
| **Context Thread** | Discussion projet | → Charger contexte |
| **Agent Suggestion** | "Serait mieux en Board" | → Proposer transformation |

## Exemples de Transformation Automatique

```
INTENT: "Plan my week"
RESULT: Timeline Mode
CONFIG: Week scale, personal calendar integrated, goals visible

INTENT: "Build construction estimation"  
RESULT: Spreadsheet Mode
CONFIG: Material tables, unit pricing, labor calculations pre-loaded

INTENT: "Review the property"
RESULT: Hybrid Mode  
CONFIG: Immobilier dashboard + document viewer + XR launcher ready

INTENT: "Brainstorm renovation ideas"
RESULT: Whiteboard Mode
CONFIG: Infinite canvas, sticky notes, sketch tools
```

## Transitions Seamless

| De | Vers | Type Transition |
|----|------|-----------------|
| Board | Timeline | Horizontal morph |
| Document | Board | Split expansion |
| Whiteboard | XR | Depth projection |
| Diagram | Dashboard | Node-to-card morph |
| Spreadsheet | Document | Row-to-paragraph |

### Règles de Transition

1. **Smooth**: Pas de changements visuels brusques
2. **Informative**: L'utilisateur comprend ce qui change
3. **Reversible**: Peut revenir au mode précédent
4. **Data Preserved**: Les données restent intactes

---

# 🎛️ GOUVERNANCE DE LA FLEXIBILITÉ

## Permissions des Agents

| Permission | Autorisé | Non autorisé |
|------------|----------|--------------|
| Suggérer transformation | ✅ | |
| Transformer automatiquement | ❌ | Sans approbation |
| Modifier layout | ✅ (avec approbation) | |
| Changer sphère | ❌ | Jamais |

## Logs et Audit

Chaque transformation est loguée:
```json
{
  "transformation_id": "uuid",
  "from_mode": "document",
  "to_mode": "board",
  "triggered_by": "user_intent",
  "intent_text": "organize my tasks",
  "timestamp": "2025-12-23T10:30:00Z",
  "user_id": "uuid",
  "identity_id": "uuid",
  "sphere_id": "business",
  "reversible": true
}
```

---

# 📊 INTÉGRATION AVEC LES 9 SPHÈRES

## Configuration par Sphère

| Sphère | Mode Default | Modes Fréquents |
|--------|--------------|-----------------|
| **Personal** | Dashboard | Document, Timeline |
| **Business** | Board | Document, Spreadsheet, Dashboard |
| **Government** | Document | Timeline, Dashboard |
| **Creative Studio** | Whiteboard | Document, Diagram |
| **Community** | Board | Document, Timeline |
| **Social & Media** | Dashboard | Whiteboard, Timeline |
| **Entertainment** | Dashboard | Timeline, Whiteboard |
| **My Team** | Board | Document, Dashboard |
| **Scholar** | Document | Diagram, Spreadsheet |

---

# 🧩 RÉSUMÉ TECHNIQUE

## Architecture Finale

```typescript
// BUREAU - 6 Sections (Fixed Entry Points)
const BUREAU_SECTIONS = [
  'quick_capture',     // 📝
  'resume_workspace',  // ▶️
  'threads',           // 💬
  'data_files',        // 📁
  'active_agents',     // 🤖
  'meetings',          // 📅
] as const;

// WORKSPACE ENGINE - 9 Modes (Adaptive)
const WORKSPACE_MODES = [
  'document',    // Rich text
  'board',       // Kanban
  'timeline',    // Gantt
  'spreadsheet', // Tables
  'dashboard',   // KPIs
  'diagram',     // Flowcharts
  'whiteboard',  // Freeform
  'xr',          // Immersive
  'hybrid',      // Multi-mode
] as const;

// SPHERES - 9 (FROZEN)
const SPHERES = [
  'personal',       // 🏠
  'business',       // 💼
  'government',     // 🏛️
  'creative_studio',// 🎨
  'community',      // 👥
  'social_media',   // 📱
  'entertainment',  // 🎬
  'my_team',        // 🤝
  'scholar',        // 🎓
] as const;
```

## Flux Utilisateur

```
1. User → Sélectionne SPHÈRE
2. Sphère → Ouvre BUREAU (6 sections adaptées)
3. Bureau → User clique section (ex: Resume Workspace)
4. Section → Ouvre WORKSPACE ENGINE
5. Workspace → Détecte INTENT
6. Intent → TRANSFORMATION vers mode optimal
7. User → Travaille dans mode adapté
8. User → Peut transformer manuellement
9. Workspace → Sauvegarde dans DATASPACE
```

---

*Document Canonique v46 — CHE·NU™*
*GOVERNANCE > EXECUTION | CLARITY > FEATURES*
*🌟 CHANGE LE MONDE 🌟*
