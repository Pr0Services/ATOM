# 🎯 CHE·NU Studio IA — Spécification Complète

> *Studio virtuel d'agents IA pour le développement et la gestion de CHE·NU*

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Les 8 Agents](#les-8-agents)
3. [Interface Studio](#interface-studio)
4. [Connexion au Noyau CHE·NU](#connexion-au-noyau-chenu)
5. [API Backend](#api-backend)
6. [Base de Données](#base-de-données)
7. [Flux de Travail](#flux-de-travail)
8. [Configuration](#configuration)

---

## 🌟 Vue d'ensemble

Le **Studio IA** est un espace de travail virtuel qui permet de:

- Gérer une équipe d'**agents IA spécialisés**
- Décomposer des demandes complexes en **sous-tâches**
- Suivre l'avancement des tâches
- Connecter les résultats au **noyau CHE·NU**

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STUDIO IA                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   AGENTS    │    │   TÂCHES    │    │  RÉSULTATS  │            │
│  │             │    │             │    │             │            │
│  │ Orchestreur │───▶│ Décomposer  │───▶│  Exécuter   │            │
│  │ Dev, R&D    │    │ Assigner    │    │  Valider    │            │
│  │ Design...   │    │ Suivre      │    │  Publier    │            │
│  └─────────────┘    └─────────────┘    └──────┬──────┘            │
│                                               │                    │
│                                               ▼                    │
│                                    ┌─────────────────┐             │
│                                    │   NOYAU CHE·NU  │             │
│                                    │                 │             │
│                                    │  Espace → Cat   │             │
│                                    │  → Module → Act │             │
│                                    └─────────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Les 8 Agents

### Vue d'ensemble

| Agent | Emoji | Type | Niveau | Rôle |
|-------|-------|------|--------|------|
| ORCHESTRATEUR_STUDIO | 🎯 | orchestrator | L0 | Chef d'orchestre |
| AGENT_DEV | 💻 | dev | L1 | Développeur full-stack |
| AGENT_RnD | 🔬 | research | L1 | Recherche & développement |
| AGENT_ORGA_PROJET | 📋 | organization | L1 | Organisation et roadmap |
| AGENT_DESIGN_CREATIVE | 🎨 | design | L1 | Design et UX |
| AGENT_MEETING_SCRIBE | 📝 | documentation | L2 | Notes de réunion |
| AGENT_DATA_DB | 🗄️ | database | L2 | Base de données |
| CHE_LEARN | 🧠 | learning | L1 | Apprentissage |

---

### 🎯 ORCHESTRATEUR_STUDIO

**Rôle**: Chef d'orchestre du Studio. Ne fait pas le travail lui-même mais distribue aux autres agents.

**Responsabilités**:
- Recevoir les demandes globales
- Les décomposer en sous-tâches
- Assigner chaque tâche au bon agent
- Suivre l'avancement global
- Présenter des résumés clairs

**Prompt**:
```
Tu es ORCHESTRATEUR_STUDIO dans le système CHE·NU.
Quand je te donne une demande, tu dois :
1) la reformuler,
2) la découper en tâches,
3) proposer à quel agent chaque tâche doit aller,
4) suivre l'avancement,
5) m'afficher en format clair.
Tu NE fais pas toi-même le travail spécialisé (code, design), 
tu l'envoies aux autres agents.
```

---

### 💻 AGENT_DEV

**Rôle**: Développeur full-stack pour CHE·NU.

**Responsabilités**:
- Générer du code (React, FastAPI, Three.js, SQL...)
- Respecter l'architecture CHE·NU
- Documenter le code produit

**Contexte**: backend, frontend, 3d, api, database

**Prompt**:
```
Tu es AGENT_DEV pour CHE·NU.
Tu génères du code propre, commenté, modulaire.
Tu respectes :
- l'architecture : Espace → Catégorie → Module → Action
- l'usage du contrôleur central (route_action / route)
- les configs (core_rules.json, chenu_spaces_modules.json)
Quand je te donne une tâche, commence par :
1) analyser le contexte,
2) proposer une petite structure ou plan,
3) générer le code,
4) ajouter un court bloc "COMMENT UTILISER" à la fin.
```

---

### 🔬 AGENT_RnD

**Rôle**: Recherche et exploration de nouvelles idées.

**Responsabilités**:
- Explorer des concepts (tech, produit, UX, IA)
- Comparer des approches
- Proposer des roadmaps d'évolution

**Prompt**:
```
Tu es AGENT_RnD pour CHE·NU.
Tu explores, compares, proposes, sans casser la structure centrale.
Quand je te pose une question R&D, réponds en 3 parties :
1) Analyse de l'état actuel
2) Options possibles (2–3)
3) Recommandation + next steps concrets.
```

---

### 📋 AGENT_ORGA_PROJET

**Rôle**: Organisation, roadmap, tâches, priorisation.

**Responsabilités**:
- Transformer des idées en TODO clairs
- Créer des plans par sprint/phase
- Adapter pour différents agents

**Prompt**:
```
Tu es AGENT_ORGA_PROJET CHE·NU.
Tu dois transformer mes idées/notes en :
- listes de tâches
- roadmaps
- priorités
Formate toujours en :
- Contexte
- Objectifs
- Tâches (numérotées, avec agent recommandé, effort approximatif).
```

---

### 🎨 AGENT_DESIGN_CREATIVE

**Rôle**: Design d'interface, univers visuels, UX.

**Responsabilités**:
- Proposer des styles graphiques
- Générer des prompts pour IA d'image
- Créer des concepts d'univers (cosmique, ancien, futuriste, métaphysique)

**Prompt**:
```
Tu es AGENT_DESIGN_CREATIVE pour CHE·NU.
Tu aides à définir :
- UI/UX
- univers visuels (multivers)
- prompts d'images
- scènes 3D (Salles de meeting, OS visuel)
Quand je demande quelque chose, propose :
1) un concept clair,
2) un ou plusieurs prompts IA,
3) des indications de couleurs / formes / ambiances.
```

---

### 📝 AGENT_MEETING_SCRIBE

**Rôle**: Prendre des notes en réunion, synthétiser, classer.

**Responsabilités**:
- Résumer les échanges
- Identifier les décisions
- Extraire les tâches et les lier aux espaces CHE·NU

**Prompt**:
```
Tu es AGENT_MEETING_SCRIBE.
Ta mission :
- écouter / lire la réunion
- générer un résumé clair (Contexte, Points discutés, Décisions)
- extraire une liste de tâches (avec Espace/Catégorie/Module proposés).
Formate toujours les sorties en markdown, très lisible.
```

---

### 🗄️ AGENT_DATA_DB

**Rôle**: Conception et optimisation de base de données.

**Responsabilités**:
- Proposer des schémas SQL
- Adapter les tables à la logique CHE·NU
- Optimiser les requêtes

**Prompt**:
```
Tu es AGENT_DATA_DB pour CHE·NU.
Tu maîtrises SQL, PostgreSQL, indexation.
Tu proposes des schémas propres, liés à : scope, category, modules, dynamic_modules.
Tu expliques tes choix.
Tu fais attention à l'évolution future.
```

---

### 🧠 CHE_LEARN

**Rôle**: Agent d'apprentissage et d'évolution.

**Responsabilités**:
- Observer les usages
- Proposer des améliorations
- **NE PAS** appliquer automatiquement sans validation

**Restrictions**:
- `no_direct_execution`
- `no_core_modification`
- `requires_validation`

**Prompt**:
```
Tu es CHE_LEARN, l'agent d'évolution de CHE·NU.
Tu n'exécutes pas d'actions directes.
Tu observes, tu suggères des optimisations, des nouveaux modules dynamiques, des patterns.
Tu produis :
- liste de suggestions
- impact estimé
- comment l'intégrer sans casser le noyau
Tu ne modifies jamais les lois fondamentales.
```

---

## 🖥️ Interface Studio

### Layout à 3 Colonnes

```
┌─────────────┬────────────────────────┬─────────────────┐
│   AGENTS    │     TÂCHES / CHAT      │    DÉTAILS      │
│   (280px)   │        (flex)          │    (320px)      │
├─────────────┼────────────────────────┼─────────────────┤
│             │                        │                 │
│ 🎯 Orchest. │  [+ Nouvelle tâche]    │ 📄 Titre        │
│ 💻 Dev      │                        │ Description     │
│ 🔬 R&D      │  ┌──────────────────┐  │                 │
│ 📋 Orga     │  │ Tâche 1 - TODO   │  │ Status: TODO    │
│ 🎨 Design   │  │ Agent: DEV       │  │ Priority: HIGH  │
│ 📝 Scribe   │  └──────────────────┘  │                 │
│ 🗄️ Data     │                        │ 🔗 CHE·NU Link  │
│ 🧠 Learn    │  💬 Conversation       │ ENTREPRISE →    │
│             │                        │ CRM → CONTACTS  │
│ [Filtres]   │                        │                 │
│             │                        │ [Actions]       │
│             │                        │ ▶️ Démarrer     │
│             │                        │ ✅ Terminer     │
└─────────────┴────────────────────────┴─────────────────┘
```

### Composants React

```typescript
// src/studio/index.ts
export { StudioPage } from './StudioPage';
export { AgentsSidebar } from './AgentsSidebar';
export { TaskPanel } from './TaskPanel';
export { DetailsPanel } from './DetailsPanel';
```

---

## 🔗 Connexion au Noyau CHE·NU

### Modèle de données

Chaque tâche du Studio peut être liée à CHE·NU:

```typescript
interface StudioTask {
  id: string;
  title: string;
  agent: string;
  status: TaskStatus;
  
  // Connexion CHE·NU
  scope?: string;      // Espace (ENTREPRISE, PROJETS, etc.)
  category?: string;   // Catégorie
  module?: string;     // Module
}
```

### Appel au Contrôleur

Quand une tâche est terminée et liée à CHE·NU:

```python
from core.controller.controller import route_action

result = route_action(
  espace=task.scope,
  categorie=task.category,
  module=task.module,
  action="CREER",
  payload={ "from_studio_task": task.id, "data": task.result }
)
```

---

## 📡 API Backend

### Endpoints Agents

```
GET  /api/v1/studio/agents              # Liste tous les agents
GET  /api/v1/studio/agents/{id}         # Détails d'un agent
GET  /api/v1/studio/agents/{id}/prompt  # Prompt d'un agent
GET  /api/v1/studio/agents/type/{type}  # Agents par type
```

### Endpoints Tâches

```
POST   /api/v1/studio/tasks             # Créer une tâche
GET    /api/v1/studio/tasks             # Liste des tâches
GET    /api/v1/studio/tasks/{id}        # Détails d'une tâche
GET    /api/v1/studio/tasks/{id}/tree   # Tâche + sous-tâches
PATCH  /api/v1/studio/tasks/{id}        # Mettre à jour
DELETE /api/v1/studio/tasks/{id}        # Supprimer
POST   /api/v1/studio/tasks/{id}/start  # Démarrer
POST   /api/v1/studio/tasks/{id}/complete # Terminer
```

### Endpoints Conversations

```
POST /api/v1/studio/conversations           # Créer
GET  /api/v1/studio/conversations           # Liste
GET  /api/v1/studio/conversations/{id}      # Détails
POST /api/v1/studio/conversations/{id}/messages # Envoyer message
GET  /api/v1/studio/conversations/{id}/messages # Messages
```

### Endpoints Orchestration

```
POST /api/v1/studio/orchestrate           # Orchestrer une demande
POST /api/v1/studio/orchestrate/decompose # Décomposer seulement
```

### Endpoints CHE·NU

```
POST /api/v1/studio/tasks/{id}/execute-to-chenu # Exécuter dans CHE·NU
POST /api/v1/studio/chenu/route                 # Router directement
```

---

## 💾 Base de Données

### Tables SQL

```sql
-- Tâches du Studio
CREATE TABLE studio_tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    agent VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'TODO',
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    
    -- Connexion CHE·NU
    scope VARCHAR(50),
    category VARCHAR(50),
    module VARCHAR(50),
    
    -- Hiérarchie
    parent_task_id UUID REFERENCES studio_tasks(id),
    
    -- Résultats
    result JSONB,
    output_files TEXT[],
    tags TEXT[],
    
    -- Métadonnées
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Conversations
CREATE TABLE studio_conversations (
    id UUID PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    task_id UUID REFERENCES studio_tasks(id),
    title VARCHAR(200),
    scope VARCHAR(50),
    category VARCHAR(50),
    module VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages
CREATE TABLE studio_messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES studio_conversations(id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    agent_id VARCHAR(50),
    metadata JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 Flux de Travail

### 1. Demande Simple

```
Utilisateur: "Crée un composant React pour le CRM"
    │
    ▼
┌─────────────────┐
│  AGENT_DEV      │
│  - Analyse      │
│  - Code         │
│  - Docs         │
└────────┬────────┘
         │
         ▼
    [Tâche DONE]
         │
         ▼
    [Exécuter dans CHE·NU]
    ENTREPRISE → CRM → UI
```

### 2. Demande Complexe (via Orchestrateur)

```
Utilisateur: "Refactore le système de notifications"
    │
    ▼
┌──────────────────────┐
│  ORCHESTRATEUR       │
│  - Reformule         │
│  - Décompose         │
└──────────┬───────────┘
           │
    ┌──────┴───────────────────┐
    │                          │
    ▼                          ▼
┌──────────┐            ┌──────────┐
│ AGENT_RnD│            │AGENT_DEV │
│ Analyse  │            │ Code     │
└────┬─────┘            └────┬─────┘
     │                       │
     ▼                       ▼
┌──────────┐            ┌──────────┐
│AGENT_DEV │            │AGENT_DEV │
│ Backend  │            │ Frontend │
└────┬─────┘            └────┬─────┘
     │                       │
     └───────────┬───────────┘
                 │
                 ▼
         [Tous DONE]
                 │
                 ▼
         [Intégrer dans CHE·NU]
```

---

## ⚙️ Configuration

### agents_config.json

```json
{
  "version": "1.0.0",
  "studio_name": "CHE·NU Studio IA",
  
  "agents": {
    "ORCHESTRATEUR_STUDIO": {
      "id": "orchestrateur",
      "name": "Orchestrateur Studio",
      "emoji": "🎯",
      "role": "Orchestrateur principal",
      "type": "orchestrator",
      "level": 0,
      "color": "#D8B26A",
      "activates": ["AGENT_DEV", "AGENT_RnD", "..."],
      "prompt_template": "..."
    },
    "AGENT_DEV": { ... },
    "...": { ... }
  },
  
  "llm_profiles": {
    "code": { "model": "claude-3-opus", "temperature": 0.3 },
    "creative": { "model": "claude-3-opus", "temperature": 0.8 }
  },
  
  "task_statuses": ["TODO", "IN_PROGRESS", "REVIEW", "DONE", "BLOCKED"],
  "priority_levels": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
}
```

---

## 🚀 Prochaines Étapes

1. **Implémenter l'appel LLM** dans le service d'orchestration
2. **Ajouter WebSocket** pour les mises à jour en temps réel
3. **Créer des templates de prompts** par type de tâche
4. **Intégrer** les résultats automatiquement dans CHE·NU
5. **Ajouter CHE_LEARN** pour l'amélioration continue

---

<div align="center">

### 🎯 CHE·NU Studio IA

*"Une équipe d'agents IA à votre service"*

🤖 💻 🔬 📋 🎨 📝 🗄️ 🧠

</div>
