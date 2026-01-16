# CHE·NU — Agents IA & CHE-Learn (V1)

## 1. Objectif

Définir le système d'agents IA de CHE·NU:
- Hiérarchie des agents
- Rôles et responsabilités
- CHE-Learn (apprentissage contrôlé)
- Intégration avec le système

---

## 2. Hiérarchie des Agents

```
                              ⭐ NOVA (L-1)
                         Superviseur Omniscient
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
        🏛️ ARCHITECTE        🧠 MASTER-MIND        📚 CHE-LEARN
           (L0)                 (L0)                 (Global)
            │                     │
    ┌───────┼───────┐     ┌──────┼──────┐
    │       │       │     │      │      │
  🎯      👁️      🌍    💼    🏠    📊
DIRECTEUR VISION  COMMUN  ENTREPRISE MAISON PROJETS
  (L1)    (L1)    (L1)     (L1)    (L1)   (L1)
    │
┌───┴───┐
│       │
🔧     📝
BUILDER DOCU
(L2)   (L2)
    │
┌───┴───┐
│       │
💬     📋
CHAT  TÂCHES
(L3)   (L3)
    │
    │
   🔌
PLUGINS
 (L4)
```

---

## 3. Description des Niveaux

### L-1: Superviseur Omniscient

| Agent | Description |
|-------|-------------|
| ⭐ **Nova** | Intelligence suprême, supervise tout le système |

**Responsabilités:**
- Surveillance globale
- Coordination inter-agents
- Décisions stratégiques
- Résolution de conflits

---

### L0: Architectes du Système

| Agent | Rôle |
|-------|------|
| 🏛️ **Architecte** | Valide les structures, maintient les règles |
| 🧠 **Master-Mind** | Orchestre les tâches complexes |
| 📚 **CHE-Learn** | Apprentissage et évolution contrôlée |

---

### L1: Directeurs de Domaine

| Agent | Domaine | Responsabilités |
|-------|---------|-----------------|
| 🎯 **Directeur** | Coordination | Dirige les équipes d'agents |
| 👁️ **Visionnaire** | Création | Interprète les intentions utilisateur |
| 🌍 **Gardien Commun** | Monde Commun | Maintient les espaces partagés |
| 💼 **Agent Entreprise** | Business | Gère les modules entreprise |
| 🏠 **Agent Maison** | Personnel | Gère les modules maison |
| 📊 **Agent Projets** | Projets | Gère les projets et tâches |

---

### L2: Spécialistes

| Agent | Spécialité | Actions |
|-------|------------|---------|
| 🔧 **Builder** | Construction | Génère code, assets, structures |
| 📝 **Documentor** | Documentation | Documente automatiquement |
| ✅ **Validator** | Validation | Tests et vérifications |
| 🎨 **Designer** | Design | Crée interfaces et visuels |

---

### L3: Opérationnels

| Agent | Fonction | Interface |
|-------|----------|-----------|
| 💬 **Chat** | Conversation | Dialogue avec utilisateur |
| 📋 **Tâches** | Gestion tâches | Crée, assigne, suit |
| 📧 **Email** | Communications | Rédige, envoie, trie |
| 📅 **Calendrier** | Planning | Planifie, rappelle |

---

### L4: Plugins

| Agent | Type | Description |
|-------|------|-------------|
| 🔌 **Plugin** | Extension | Agents créés dynamiquement |
| 🤖 **Custom** | Personnalisé | Agents utilisateur |

---

## 4. CHE-Learn: Le Système d'Apprentissage

### 4.1 Concept

CHE-Learn est le système d'apprentissage contrôlé de CHE·NU:

```
┌─────────────────────────────────────────────────────────────────┐
│                      CHE-LEARN                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📥 COLLECTE                                                    │
│  │  • Actions utilisateur                                      │
│  │  • Créations (modules, mondes, agents)                      │
│  │  • Patterns d'utilisation                                   │
│  │                                                              │
│  ▼                                                              │
│  🧠 ANALYSE                                                     │
│  │  • Détection de patterns                                    │
│  │  • Identification des besoins                               │
│  │  • Évaluation des performances                              │
│  │                                                              │
│  ▼                                                              │
│  💡 PROPOSITION                                                 │
│  │  • Suggère des améliorations                                │
│  │  • Propose de nouveaux modules                              │
│  │  • Recommande des optimisations                             │
│  │                                                              │
│  ▼                                                              │
│  ✅ VALIDATION (par utilisateur/Architecte)                    │
│  │                                                              │
│  ▼                                                              │
│  📦 INTÉGRATION                                                 │
│     • Module créé et activé                                    │
│     • Documentation générée                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Règles CHE-Learn

```
┌────────────────────────────────────────────────────────────────────────┐
│                   RÈGLES CHE-LEARN                                     │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  CL.1  CHE-Learn n'agit JAMAIS sans validation utilisateur            │
│                                                                        │
│  CL.2  Les propositions sont TOUJOURS explicites et documentées       │
│                                                                        │
│  CL.3  L'utilisateur peut REFUSER toute proposition                   │
│                                                                        │
│  CL.4  Les modifications du noyau requièrent validation Architecte    │
│                                                                        │
│  CL.5  Tout apprentissage est TRAÇABLE et RÉVERSIBLE                  │
│                                                                        │
│  CL.6  CHE-Learn ne collecte QUE les données nécessaires              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Types d'Apprentissage

| Type | Description | Exemple |
|------|-------------|---------|
| **Comportemental** | Patterns d'utilisation | "Vous créez souvent des tâches le lundi" |
| **Structurel** | Organisation des données | "Suggère une nouvelle catégorie" |
| **Prédictif** | Anticipation | "Vous pourriez avoir besoin de X" |
| **Optimisation** | Performance | "Ce workflow peut être simplifié" |

---

## 5. Agents Spécialisés par Espace

### 5.1 Mapping Espace → Agents

| Espace | Agent Principal | Agents Secondaires |
|--------|-----------------|-------------------|
| 👤 PERSONNEL | Agent Personnel | Chat, Calendrier |
| 🎉 SOCIAL | Agent Social | Notifications, Partage |
| 📚 SCHOLAR | Agent Éducation | Quiz, Progression |
| 🏠 MAISON | Agent Maison | IoT, Météo |
| 🏢 ENTREPRISE | Agent Business | CRM, Finance, RH |
| 📁 PROJETS | Agent Projets | Tâches, Gantt |
| 🎨 CREATIVE | Agent Créatif | Design, 3D |
| 🏛️ GOUVERNEMENT | Agent Gouv | Formulaires, Docs |
| 🏘️ IMMOBILIER | Agent Immo | Biens, Calculs |
| 🤝 ASSOCIATIONS | Agent Asso | Membres, Events |

---

## 6. Communication Inter-Agents

### 6.1 Protocole

Les agents communiquent via un système de messages:

```python
class AgentMessage:
    sender: str           # ID de l'agent émetteur
    receiver: str         # ID de l'agent destinataire
    type: MessageType     # REQUEST, RESPONSE, EVENT, COMMAND
    priority: Priority    # LOW, NORMAL, HIGH, CRITICAL
    payload: dict         # Données du message
    context: dict         # Contexte (user_id, space, etc.)
    timestamp: datetime
```

### 6.2 Exemple de Flux

```
┌─────────────────────────────────────────────────────────────────┐
│           EXEMPLE: Création d'un module                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 👤 Utilisateur: "Crée un module de gestion de stocks"      │
│     │                                                          │
│     ▼                                                          │
│  2. 💬 Agent Chat → 👁️ Visionnaire                             │
│     │  "Interprète cette demande"                              │
│     │                                                          │
│     ▼                                                          │
│  3. 👁️ Visionnaire → 🏛️ Architecte                             │
│     │  "Valide cette structure: ENTREPRISE/Stock/Module"       │
│     │                                                          │
│     ▼                                                          │
│  4. 🏛️ Architecte → 🔧 Builder                                  │
│     │  "Construis le module validé"                            │
│     │                                                          │
│     ▼                                                          │
│  5. 🔧 Builder → 📝 Documentor                                  │
│     │  "Documente ce nouveau module"                           │
│     │                                                          │
│     ▼                                                          │
│  6. 📝 Documentor → 📚 CHE-Learn                                │
│     │  "Enregistre cette création"                             │
│     │                                                          │
│     ▼                                                          │
│  7. 💬 Agent Chat → 👤 Utilisateur                              │
│        "Module créé avec succès!"                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Intégration Technique

### 7.1 Backend Structure

```
backend/agents/
├── __init__.py
├── base_agent.py           # Classe de base
├── orchestrator/
│   ├── nova.py             # L-1: Superviseur
│   ├── master_mind.py      # L0: Orchestrateur
│   └── architect.py        # L0: Architecte
├── directors/
│   ├── visionnaire.py      # L1
│   ├── enterprise.py       # L1
│   ├── projects.py         # L1
│   └── ...
├── specialists/
│   ├── builder.py          # L2
│   ├── documentor.py       # L2
│   ├── validator.py        # L2
│   └── designer.py         # L2
├── operators/
│   ├── chat.py             # L3
│   ├── tasks.py            # L3
│   ├── email.py            # L3
│   └── calendar.py         # L3
├── che_learn/
│   ├── collector.py        # Collecte données
│   ├── analyzer.py         # Analyse patterns
│   ├── proposer.py         # Génère propositions
│   └── integrator.py       # Intègre changements
└── message_bus.py          # Communication
```

### 7.2 Schemas

```python
from enum import Enum
from pydantic import BaseModel

class AgentLevel(str, Enum):
    L_MINUS_1 = "L-1"  # Superviseur
    L0 = "L0"          # Architecte
    L1 = "L1"          # Directeur
    L2 = "L2"          # Spécialiste
    L3 = "L3"          # Opérationnel
    L4 = "L4"          # Plugin

class AgentStatus(str, Enum):
    ACTIVE = "active"
    BUSY = "busy"
    IDLE = "idle"
    OFFLINE = "offline"

class Agent(BaseModel):
    id: str
    name: str
    level: AgentLevel
    role: str
    status: AgentStatus
    skills: List[str]
    parent_id: Optional[str]
    children_ids: List[str]
```

### 7.3 API Endpoints

```python
# Agents
GET    /api/v1/agents                  # Liste des agents
GET    /api/v1/agents/{id}             # Détail d'un agent
GET    /api/v1/agents/hierarchy        # Arbre hiérarchique
POST   /api/v1/agents/{id}/message     # Envoyer un message

# CHE-Learn
GET    /api/v1/che-learn/suggestions   # Suggestions actives
POST   /api/v1/che-learn/approve/{id}  # Approuver suggestion
POST   /api/v1/che-learn/reject/{id}   # Rejeter suggestion
GET    /api/v1/che-learn/history       # Historique
```

---

## 8. Personnalisation des Agents

### 8.1 Personnalité

Chaque agent peut avoir une personnalité configurable:

```python
class AgentPersonality(BaseModel):
    tone: str           # "professional", "friendly", "formal"
    verbosity: str      # "concise", "detailed", "balanced"
    proactivity: float  # 0.0 à 1.0
    creativity: float   # 0.0 à 1.0
    emoji_usage: bool   # Utilise des emojis ou non
```

### 8.2 Création d'Agent Personnalisé

Via la Creation Room, les utilisateurs peuvent créer des agents:

```yaml
name: "Mon Agent Stock"
level: L4
role: "Gestion des stocks"
skills:
  - inventory_management
  - alerts
  - reporting
personality:
  tone: professional
  verbosity: concise
  proactivity: 0.8
prompts:
  greeting: "Bonjour, je suis votre assistant stocks."
  help: "Je peux vous aider avec l'inventaire..."
```

---

## 9. Sécurité des Agents

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SÉCURITÉ DES AGENTS                                  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  S.1  Les agents ne peuvent accéder qu'aux données de leur scope      │
│                                                                        │
│  S.2  Les actions critiques requièrent validation utilisateur         │
│                                                                        │
│  S.3  Tous les messages sont loggés et auditables                     │
│                                                                        │
│  S.4  Les agents L4 (plugins) sont sandboxés                          │
│                                                                        │
│  S.5  Les agents ne peuvent pas modifier les règles A, B, C           │
│                                                                        │
│  S.6  Rate limiting sur les actions automatiques                      │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Roadmap Agents

| Phase | Fonctionnalité | Status |
|-------|----------------|--------|
| **V1.0** | Agents de base (L1-L3) | 🟡 En cours |
| **V1.1** | Communication inter-agents | ⚪ Planifié |
| **V1.2** | CHE-Learn basique | ⚪ Planifié |
| **V2.0** | Agents personnalisés (L4) | ⚪ Planifié |
| **V2.5** | Apprentissage avancé | ⚪ Planifié |
| **V3.0** | Agents autonomes | ⚪ Planifié |

---

**CHE·NU V25** — *"Des agents intelligents au service de votre vie."* 🤖
