# CHE·NU™ — CORRECTION DOCUMENT
## Bureau 6 Sections Flexibles — Architecture Canonique
### Version 46 — 23 Décembre 2025

---

# ⚠️ CORRECTION OFFICIELLE

Ce document **REMPLACE** toute documentation antérieure concernant la structure du Bureau.

## Erreur Identifiée

Le Memory Prompt et certains documents mentionnaient **10 sections Bureau**:
```
❌ OBSOLÈTE — NE PLUS UTILISER
1. Dashboard
2. Notes
3. Tasks
4. Projects
5. Threads (.chenu)
6. Meetings
7. Data / Database
8. Agents
9. Reports / History
10. Budget & Governance
```

## Version Canonique (v46)

```
✅ VERSION OFFICIELLE — 6 SECTIONS
1. Quick Capture      📝
2. Resume Workspace   ▶️
3. Threads (.chenu)   💬
4. Data/Files         📁
5. Active Agents      🤖
6. Meetings           📅
```

---

# 📋 LES 6 SECTIONS BUREAU — DÉFINITIONS

## 1. Quick Capture 📝
| Propriété | Valeur |
|-----------|--------|
| **ID** | `quick_capture` |
| **Limite** | 500 caractères max |
| **But** | Capture rapide d'idées, notes vocales, pensées |
| **Destination** | Staging → puis vers DataSpace ou Workspace |

**Fonctionnalités:**
- Texte rapide (500 car. max)
- Note vocale
- Photo/Screenshot
- Lien URL
- "Ouvrir dans Workspace" pour édition complète

---

## 2. Resume Workspace ▶️
| Propriété | Valeur |
|-----------|--------|
| **ID** | `resume_workspace` |
| **But** | Reprendre le travail là où on l'a laissé |
| **Affiche** | Workspaces actifs triés par dernière modification |

**Fonctionnalités:**
- Liste des workspaces en cours
- Preview du dernier état
- Un clic pour reprendre
- Indicateur de temps depuis dernière édition

---

## 3. Threads 💬
| Propriété | Valeur |
|-----------|--------|
| **ID** | `threads` |
| **Format** | Fichiers `.chenu` |
| **But** | Fils de discussion persistants et auditables |

**Fonctionnalités:**
- Conversations par contexte (projet, décision, support)
- Badge unread count
- Statut (actif, résolu, archivé)
- Participants visibles
- Historique des décisions

---

## 4. Data/Files 📁
| Propriété | Valeur |
|-----------|--------|
| **ID** | `data_files` |
| **But** | Accès aux DataSpaces et fichiers |
| **Scope** | Limité à la sphère/identité active |

**Fonctionnalités:**
- Navigation DataSpaces
- Upload fichiers
- Recherche sémantique
- Indicateur stockage utilisé
- Tri par date/type/taille

---

## 5. Active Agents 🤖
| Propriété | Valeur |
|-----------|--------|
| **ID** | `active_agents` |
| **But** | Observation et contrôle des agents actifs |
| **Mode** | Lecture seule (observation) sauf actions explicites |

**Fonctionnalités:**
- Liste agents actifs dans le contexte
- Statut (idle, working, waiting, error)
- Barre de progression tâche
- Badge niveau (L0-L3)
- Bouton pause/stop (si autorisé)

---

## 6. Meetings 📅
| Propriété | Valeur |
|-----------|--------|
| **ID** | `meetings` |
| **But** | Planification et gestion des réunions |
| **Intégration** | Calendrier, XR, Notes automatiques |

**Fonctionnalités:**
- Réunions à venir (avec countdown)
- Réunions passées (avec résumés)
- Création rapide de réunion
- Lancement XR Meeting
- Tâches extraites des réunions

---

# 🔄 FLEXIBILITÉ PAR PRIORISATION

## Principe Fondamental

> **Les 6 sections sont TOUJOURS présentes.**
> **Seul leur ORDRE et leur MISE EN AVANT changent.**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   BUREAU FLEXIBLE = PRIORISATION DYNAMIQUE                     │
│                                                                 │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐                         │
│   │PRIMAIRE │ │PRIMAIRE │ │SECONDAI-│  ← Grandes cartes       │
│   │    1    │ │    2    │ │   RE    │    visibles             │
│   └─────────┘ └─────────┘ └─────────┘                         │
│                                                                 │
│   ┌───┐ ┌───┐ ┌───┐                                           │
│   │ 4 │ │ 5 │ │ 6 │  ← Petites icônes / Menu "Plus"          │
│   └───┘ └───┘ └───┘                                           │
│                                                                 │
│   L'ordre change selon: Sphère, Domaine, Intent, Historique   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# 📊 MATRICES DE PRIORISATION

## Par Sphère

| Sphère | Position 1 | Position 2 | Position 3 | Positions 4-6 |
|--------|------------|------------|------------|---------------|
| **Personal** 🏠 | Quick Capture | Threads | Data/Files | Resume, Agents, Meetings |
| **Business** 💼 | Resume Work | Meetings | Data/Files | Capture, Threads, Agents |
| **Government** 🏛️ | Data/Files | Threads | Meetings | Capture, Resume, Agents |
| **Creative Studio** 🎨 | Quick Capture | Threads | Resume Work | Data, Agents, Meetings |
| **Community** 👥 | Threads | Meetings | Quick Capture | Resume, Data, Agents |
| **Social & Media** 📱 | Quick Capture | Threads | Data/Files | Resume, Agents, Meetings |
| **Entertainment** 🎬 | Quick Capture | Data/Files | Threads | Resume, Agents, Meetings |
| **My Team** 🤝 | Active Agents | Meetings | Resume Work | Capture, Threads, Data |
| **Scholar** 🎓 | Data/Files | Threads | Quick Capture | Resume, Agents, Meetings |

---

## Par Domaine (Override Sphère)

Quand un **domaine spécifique** est actif, il peut **override** la priorisation de la sphère:

| Domaine | Override Position 1 | Override Position 2 | Raison |
|---------|---------------------|---------------------|--------|
| **Construction** | Data/Files | Meetings | Accès plans & coordination |
| **Immobilier** | Data/Files | Threads | Baux & communication locataires |
| **Finance** | Data/Files | Resume Work | Rapports & continuité |
| **Architecture** | Data/Files | Active Agents | Plans & outils IA |
| **RH** | Threads | Meetings | Communication & entretiens |
| **Juridique** | Data/Files | Threads | Documents & correspondance |

---

## Par Intent (Override Temps Réel)

L'intelligence détecte l'intention et ajuste **en temps réel**:

| Intent Détecté | Action Bureau |
|----------------|---------------|
| "Je dois finir mon rapport" | **Resume Workspace** passe en Position 1 |
| "Nouvelle idée!" | **Quick Capture** s'ouvre automatiquement |
| "Réunion dans 5 min" | **Meetings** en surbrillance + notification |
| "Où est le document X?" | **Data/Files** avec recherche pré-remplie |
| "Qu'est-ce que les agents font?" | **Active Agents** en focus |
| "Message de Pierre" | **Threads** avec conversation ouverte |

---

## Par Historique Utilisateur

Le système apprend les préférences:

```
SI utilisateur ouvre toujours Quick Capture en premier dans Personal
ALORS Quick Capture reste en Position 1 pour Personal

SI utilisateur ignore toujours Active Agents dans Creative Studio
ALORS Active Agents passe en Position 6 (menu "Plus")

SI utilisateur accède fréquemment à Meetings le lundi matin
ALORS Meetings en Position 1 le lundi matin
```

---

# 🎨 REPRÉSENTATION VISUELLE

## Layout Desktop (Large Screen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BUREAU — Personal 🏠                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐ │
│  │                     │  │                     │  │                 │ │
│  │   📝 Quick Capture  │  │   💬 Threads        │  │  📁 Data/Files  │ │
│  │                     │  │                     │  │                 │ │
│  │   [+ Nouvelle note] │  │   3 non lus         │  │  12 fichiers    │ │
│  │                     │  │                     │  │                 │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────┘ │
│                                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │
│  │ ▶️ Resume (2) │  │ 🤖 Agents (1) │  │ 📅 Meet (0)   │               │
│  └───────────────┘  └───────────────┘  └───────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Layout Mobile (Small Screen)

```
┌─────────────────────┐
│ BUREAU — Personal 🏠│
├─────────────────────┤
│                     │
│ ┌─────────────────┐ │
│ │ 📝 Quick Capture│ │
│ │ [+ Note rapide] │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ 💬 Threads (3)  │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ 📁 Data/Files   │ │
│ └─────────────────┘ │
│                     │
│ ┌───┐┌───┐┌───┐     │
│ │▶️ ││🤖 ││📅 │     │
│ └───┘└───┘└───┘     │
│                     │
└─────────────────────┘
```

---

# 🔗 RELATION BUREAU → WORKSPACE ENGINE

## Flux de Navigation

```
┌──────────────────────────────────────────────────────────────────┐
│                           BUREAU                                 │
│                                                                  │
│   User clique sur une section                                   │
│           │                                                      │
│           ▼                                                      │
│   ┌───────────────────────────────────────────────────────┐     │
│   │                                                       │     │
│   │   Quick Capture → Workspace (Document mode léger)     │     │
│   │   Resume Work   → Workspace (dernier mode utilisé)    │     │
│   │   Threads       → Workspace (Thread viewer mode)      │     │
│   │   Data/Files    → Workspace (File browser mode)       │     │
│   │   Active Agents → Panel overlay (pas de workspace)    │     │
│   │   Meetings      → Workspace (Meeting mode)            │     │
│   │                                                       │     │
│   └───────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

# 📝 MISE À JOUR MEMORY PROMPT

## Section à Remplacer

**ANCIEN:**
```
BUREAU MODEL (NON-NEGOTIABLE)

Each SPHERE opens a BUREAU containing maximum 6 Flexible by hierarchi SECTIONS:

1. Dashboard
2. Notes
3. Tasks
4. Projects
5. Threads (.chenu)
6. Meetings
7. Data / Database
8. Agents
9. Reports / History
10. Budget & Governance
```

**NOUVEAU:**
```
BUREAU MODEL (NON-NEGOTIABLE)

Each SPHERE opens a BUREAU containing exactly 6 FLEXIBLE SECTIONS:

1. Quick Capture 📝    — Lightweight capture (500 char max)
2. Resume Workspace ▶️ — Continue existing work
3. Threads 💬          — Persistent conversations (.chenu)
4. Data/Files 📁       — DataSpaces and file management
5. Active Agents 🤖    — Agent status and control
6. Meetings 📅         — Meeting management

FLEXIBILITY = PRIORITIZATION
- All 6 sections are ALWAYS available
- Order changes based on: Sphere, Domain, Intent, User history
- Primary sections (1-3) shown as large cards
- Secondary sections (4-6) shown as compact icons or "More" menu
- Sections NEVER disappear, only reorganize
```

---

# ✅ CHECKLIST DE CONFORMITÉ

Pour vérifier qu'un document/code est conforme:

- [ ] Bureau a exactement **6 sections** (pas 10)
- [ ] Sections nommées: Quick Capture, Resume Workspace, Threads, Data/Files, Active Agents, Meetings
- [ ] Aucune section "Dashboard", "Notes", "Tasks", "Projects", "Reports", "Budget" en standalone
- [ ] Flexibilité = priorisation, pas disparition
- [ ] Toutes les sections accessibles (même si en menu "Plus")

---

# 📚 DOCUMENTS À METTRE À JOUR

| Document | Section à corriger | Priorité |
|----------|-------------------|----------|
| **Memory Prompt** | BUREAU MODEL | 🔴 CRITIQUE |
| **CHENU_SYSTEM_MANUAL.md** | Bureau Central section | 🟡 HAUTE |
| **CHENU_MASTER_REFERENCE_v5.md** | Structure bureau | 🟡 HAUTE |
| **Feature Audit** | Section count | 🟢 MOYENNE |
| **Frontend components** | BureauSections.tsx | 🔴 CRITIQUE |
| **SQL Schema** | bureau_sections table | 🟢 MOYENNE |

---

*Document de Correction v46 — CHE·NU™*
*GOVERNANCE > EXECUTION | CLARITY > FEATURES*
