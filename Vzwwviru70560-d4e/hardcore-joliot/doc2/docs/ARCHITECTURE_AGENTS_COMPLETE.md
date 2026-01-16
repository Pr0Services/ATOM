# 🧠 CHE·NU™ - ARCHITECTURE COMPLÈTE DES AGENTS

**Document de Référence Technique**  
**Version:** 1.0  
**Date:** 6 décembre 2025

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Hiérarchie des Agents](#2-hiérarchie-des-agents)
3. [Registre Complet des Agents](#3-registre-complet-des-agents)
4. [Protocoles de Communication](#4-protocoles-de-communication)
5. [Optimisation des Tokens](#5-optimisation-des-tokens)
6. [Gestion de la Mémoire](#6-gestion-de-la-mémoire)
7. [Patterns d'Implémentation](#7-patterns-dimplémentation)

---

## 1. VUE D'ENSEMBLE

### 1.1 Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         🌟 NOVA (L-1)                                   │
│                    Agent Personnel Universel                            │
│              Interface utilisateur principale                           │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      🧠 MASTER MIND (L0)                                │
│                    Orchestrateur Central                                │
│         Routing · Décomposition · Planification · Assemblage            │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  DIRECTOR 1   │     │  DIRECTOR 2   │     │  DIRECTOR N   │
│     (L1)      │     │     (L1)      │     │     (L1)      │
│  Département  │     │  Département  │     │  Département  │
└───────┬───────┘     └───────┬───────┘     └───────┬───────┘
        │                     │                     │
   ┌────┼────┐           ┌────┼────┐           ┌────┼────┐
   ▼    ▼    ▼           ▼    ▼    ▼           ▼    ▼    ▼
┌────┐┌────┐┌────┐   ┌────┐┌────┐┌────┐   ┌────┐┌────┐┌────┐
│ S1 ││ S2 ││ S3 │   │ S1 ││ S2 ││ S3 │   │ S1 ││ S2 ││ S3 │
│L2  ││L2  ││L2  │   │L2  ││L2  ││L2  │   │L2  ││L2  ││L2  │
└────┘└────┘└────┘   └────┘└────┘└────┘   └────┘└────┘└────┘
   Specialists          Specialists          Specialists
```

### 1.2 Flux de Communication

```
User Request
     │
     ▼
┌─────────┐     ┌──────────────┐     ┌─────────────┐
│  NOVA   │────▶│  MASTER MIND │────▶│  DIRECTORS  │
│  (L-1)  │◀────│     (L0)     │◀────│    (L1)     │
└─────────┘     └──────────────┘     └─────────────┘
                       │                    │
                       ▼                    ▼
              ┌────────────────┐    ┌─────────────┐
              │  LLM ROUTER    │    │ SPECIALISTS │
              │ Multi-Provider │    │    (L2)     │
              └────────────────┘    └─────────────┘
```

---

## 2. HIÉRARCHIE DES AGENTS

### 2.1 Niveaux Hiérarchiques

| Niveau | Nom | Rôle | Quantité |
|--------|-----|------|----------|
| **L-1** | Nova | Agent Personnel, Interface User | 1 |
| **L0** | MasterMind | Orchestrateur Central | 1 |
| **L1** | Directors | Chefs de Département | 14 |
| **L2** | Specialists | Exécutants Spécialisés | 101 |
| **L3** | Tools | Outils & Intégrations | 80+ |

### 2.2 Responsabilités par Niveau

#### L-1: NOVA
```python
class Nova:
    """Agent Personnel Universel"""
    responsibilities = [
        "Interface conversationnelle utilisateur",
        "Interprétation des intentions",
        "Personnalisation des réponses",
        "Gestion du contexte utilisateur",
        "Délégation vers MasterMind",
        "Présentation des résultats"
    ]
    
    capabilities = [
        "voice_input",      # Entrée vocale
        "voice_output",     # Sortie vocale
        "context_memory",   # Mémoire contextuelle
        "user_preferences", # Préférences utilisateur
        "proactive_suggestions"  # Suggestions proactives
    ]
```

#### L0: MASTER MIND
```python
class MasterMind:
    """Orchestrateur Central"""
    responsibilities = [
        "Analyse et routage des requêtes",
        "Décomposition des tâches complexes",
        "Planification d'exécution",
        "Coordination des Directors",
        "Assemblage des résultats",
        "Gestion des erreurs globales"
    ]
    
    components = [
        "RoutingEngine",      # Routage intelligent
        "TaskDecomposer",     # Décomposition
        "ExecutionPlanner",   # Planification
        "ResultAssembler",    # Assemblage
        "CacheManager",       # Cache
        "ErrorHandler"        # Erreurs
    ]
```

#### L1: DIRECTORS
```python
class Director:
    """Chef de Département"""
    responsibilities = [
        "Gestion d'un domaine métier",
        "Coordination des Specialists",
        "Décisions tactiques",
        "Reporting vers MasterMind",
        "Optimisation des ressources département"
    ]
```

#### L2: SPECIALISTS
```python
class Specialist:
    """Agent Spécialisé"""
    responsibilities = [
        "Exécution de tâches spécifiques",
        "Expertise pointue",
        "Utilisation des outils (L3)",
        "Reporting vers Director"
    ]
```

---

## 3. REGISTRE COMPLET DES AGENTS

### 3.1 NOVA (L-1)

| ID | Nom | Description |
|----|-----|-------------|
| NOVA_001 | Nova | Agent Personnel Universel |

**Configuration:**
```python
NovaConfig = {
    "id": "NOVA_001",
    "name": "Nova",
    "level": "L-1",
    "llm_model": "claude-sonnet-4-20250514",
    "context_window": 200000,
    "max_tokens": 8192,
    "temperature": 0.7,
    "capabilities": [
        "conversation",
        "voice",
        "delegation",
        "memory",
        "proactive"
    ]
}
```

### 3.2 MASTER MIND (L0)

| ID | Nom | Description |
|----|-----|-------------|
| MM_001 | MasterMind | Orchestrateur Central |

**Configuration:**
```python
MasterMindConfig = {
    "id": "MM_001",
    "name": "MasterMind",
    "level": "L0",
    "llm_model": "claude-sonnet-4-20250514",
    "max_parallel_tasks": 10,
    "timeout_seconds": 300,
    "auto_decompose_threshold": 0.5,
    "enable_cache": True,
    "cache_ttl": 3600
}
```

### 3.3 DIRECTORS (L1) - 14 Départements

| # | ID | Nom | Département | Specialists |
|---|-----|-----|-------------|-------------|
| 1 | DIR_ANALYTICS | Dana Data | 📊 Analytics | 7 |
| 2 | DIR_SALES | Steve Sales | 💼 Sales | 8 |
| 3 | DIR_MARKETING | Mark Marketing | 📣 Marketing | 8 |
| 4 | DIR_HR | Helen Human | 👥 HR | 7 |
| 5 | DIR_FINANCE | Frank Finance | 💰 Finance | 8 |
| 6 | DIR_OPS | Olivia Operations | 🛠️ Operations | 8 |
| 7 | DIR_IT | Ian IT | 💻 IT | 8 |
| 8 | DIR_CREATIVE | Carla Creative | 🎨 Creative | 7 |
| 9 | DIR_LEGAL | Larry Legal | ⚖️ Legal | 6 |
| 10 | DIR_CONSTRUCT | Carl Construction | 🏗️ Construction | 9 |
| 11 | DIR_ADMIN | Amy Admin | 📁 Administration | 7 |
| 12 | DIR_SUPPORT | Sophie Support | 📞 Support | 7 |
| 13 | DIR_INTEGR | Isaac Integration | 🔌 Integrations | 6 |
| 14 | DIR_RD | Rita Research | 🔬 R&D | 7 |

### 3.4 SPECIALISTS (L2) - 101 Agents

#### 📊 Analytics Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| ANA_001 | Report Rachel | Rapports | reporting, visualization |
| ANA_002 | Dashboard Dave | Tableaux de bord | dashboards, kpi |
| ANA_003 | Metric Mike | Métriques | metrics, tracking |
| ANA_004 | Insight Iris | Insights | analysis, patterns |
| ANA_005 | Forecast Fred | Prévisions | forecasting, ml |
| ANA_006 | Query Quinn | Requêtes | sql, data_extraction |
| ANA_007 | Visual Vera | Visualisation | charts, graphs |

#### 💼 Sales Department (8 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| SAL_001 | Lead Larry | Leads | lead_gen, qualification |
| SAL_002 | Pipeline Pete | Pipeline | pipeline, forecasting |
| SAL_003 | Quote Quincy | Devis | quotes, pricing |
| SAL_004 | Contract Carla | Contrats | contracts, negotiation |
| SAL_005 | CRM Craig | CRM | crm, data_entry |
| SAL_006 | Proposal Paula | Propositions | proposals, presentations |
| SAL_007 | Follow Fred | Suivi | follow_up, nurturing |
| SAL_008 | Close Clara | Closing | closing, deals |

#### 📣 Marketing Department (8 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| MKT_001 | Content Chris | Contenu | content, copywriting |
| MKT_002 | SEO Sam | SEO | seo, keywords |
| MKT_003 | Social Sarah | Social Media | social, community |
| MKT_004 | Email Emma | Email | email, automation |
| MKT_005 | Ads Adam | Publicité | ads, ppc |
| MKT_006 | Brand Betty | Branding | brand, identity |
| MKT_007 | Event Eric | Événements | events, webinars |
| MKT_008 | Analytics Andy | Analytics Mkt | analytics, attribution |

#### 👥 HR Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| HR_001 | Recruit Rita | Recrutement | recruiting, sourcing |
| HR_002 | Onboard Oscar | Onboarding | onboarding, training |
| HR_003 | Payroll Patty | Paie | payroll, benefits |
| HR_004 | Performance Paul | Performance | reviews, feedback |
| HR_005 | Culture Cathy | Culture | culture, engagement |
| HR_006 | Compliance Carl | Conformité | compliance, policies |
| HR_007 | Learning Lucy | Formation | learning, development |

#### 💰 Finance Department (8 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| FIN_001 | Budget Bob | Budget | budgeting, planning |
| FIN_002 | Invoice Ivy | Facturation | invoicing, ar |
| FIN_003 | Expense Ed | Dépenses | expenses, ap |
| FIN_004 | Tax Tina | Taxes | tax, compliance |
| FIN_005 | Audit Alex | Audit | audit, controls |
| FIN_006 | Treasury Tom | Trésorerie | treasury, cash |
| FIN_007 | Report Rosa | Rapports fin. | reporting, statements |
| FIN_008 | Forecast Fiona | Prévisions | forecasting, modeling |

#### 🛠️ Operations Department (8 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| OPS_001 | Process Pete | Processus | process, optimization |
| OPS_002 | Quality Quinn | Qualité | qa, testing |
| OPS_003 | Inventory Iris | Inventaire | inventory, stock |
| OPS_004 | Logistics Lou | Logistique | logistics, shipping |
| OPS_005 | Vendor Vince | Fournisseurs | vendors, procurement |
| OPS_006 | Facility Fran | Installations | facilities, maintenance |
| OPS_007 | Safety Sam | Sécurité | safety, compliance |
| OPS_008 | Scheduler Scott | Planification | scheduling, resources |

#### 💻 IT Department (8 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| IT_001 | Dev Diana | Développement | coding, architecture |
| IT_002 | Infra Ian | Infrastructure | servers, cloud |
| IT_003 | Security Steve | Sécurité IT | security, encryption |
| IT_004 | Network Nancy | Réseau | networking, vpn |
| IT_005 | Database Dan | Base de données | databases, sql |
| IT_006 | Support Susan | Support IT | helpdesk, troubleshooting |
| IT_007 | DevOps Derek | DevOps | ci_cd, automation |
| IT_008 | Cloud Clara | Cloud | aws, azure, gcp |

#### 🎨 Creative Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| CRE_001 | Design Doug | Design | ui_ux, graphic |
| CRE_002 | Video Vera | Vidéo | video, editing |
| CRE_003 | Photo Phil | Photo | photography, retouching |
| CRE_004 | Copy Carol | Copywriting | writing, storytelling |
| CRE_005 | Brand Brian | Branding | brand, identity |
| CRE_006 | Motion Max | Animation | motion, animation |
| CRE_007 | Audio Anna | Audio | audio, music |

#### ⚖️ Legal Department (6 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| LEG_001 | Contract Carl | Contrats | contracts, review |
| LEG_002 | Compliance Cora | Conformité | compliance, regulations |
| LEG_003 | IP Ivan | Propriété intel. | ip, patents |
| LEG_004 | Litigation Lisa | Litiges | litigation, disputes |
| LEG_005 | Privacy Paul | Vie privée | privacy, gdpr |
| LEG_006 | Corporate Cathy | Corporate | corporate, governance |

#### 🏗️ Construction Department (9 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| CON_001 | Estimate Ed | Estimation | estimating, takeoff |
| CON_002 | Plan Paula | Plans | blueprints, cad |
| CON_003 | Schedule Sam | Planification | scheduling, gantt |
| CON_004 | Safety Steve | Sécurité chantier | safety, osha |
| CON_005 | Quality Quinn | Contrôle qualité | qc, inspections |
| CON_006 | Material Mike | Matériaux | materials, procurement |
| CON_007 | Labor Larry | Main d'oeuvre | labor, crews |
| CON_008 | Equipment Eric | Équipement | equipment, fleet |
| CON_009 | Permit Pete | Permis | permits, regulations |

#### 📁 Administration Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| ADM_001 | Document Dana | Documents | documents, filing |
| ADM_002 | Calendar Cal | Calendrier | scheduling, meetings |
| ADM_003 | Travel Tina | Voyages | travel, bookings |
| ADM_004 | Office Oscar | Bureau | office, supplies |
| ADM_005 | Reception Rita | Réception | reception, calls |
| ADM_006 | Archive Andy | Archives | archiving, records |
| ADM_007 | Coordinator Cora | Coordination | coordination, tasks |

#### 📞 Support Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| SUP_001 | Ticket Tom | Tickets | tickets, triage |
| SUP_002 | Chat Chloe | Chat | live_chat, messaging |
| SUP_003 | Phone Phil | Téléphone | calls, voip |
| SUP_004 | Email Eve | Email support | email, templates |
| SUP_005 | Escalation Ed | Escalades | escalation, priority |
| SUP_006 | Knowledge Kate | Base connais. | kb, documentation |
| SUP_007 | Feedback Fred | Feedback | feedback, surveys |

#### 🔌 Integrations Department (6 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| INT_001 | API Alex | APIs | api, rest, graphql |
| INT_002 | Webhook Wendy | Webhooks | webhooks, events |
| INT_003 | Sync Sam | Sync | sync, etl |
| INT_004 | OAuth Oscar | Auth | oauth, sso |
| INT_005 | Transform Tina | Transform | data_transform, mapping |
| INT_006 | Monitor Mike | Monitoring | monitoring, alerts |

#### 🔬 R&D Department (7 specialists)
| ID | Nom | Spécialité | Skills |
|----|-----|------------|--------|
| RD_001 | Prototype Paul | Prototypage | prototyping, poc |
| RD_002 | Research Rita | Recherche | research, analysis |
| RD_003 | Innovation Ivy | Innovation | innovation, ideation |
| RD_004 | Data Dana | Data Science | ml, ai, data |
| RD_005 | Lab Lucas | Labo | testing, experiments |
| RD_006 | Patent Patty | Brevets | patents, ip |
| RD_007 | Tech Trends Tom | Veille techno | trends, emerging_tech |

---

## 4. PROTOCOLES DE COMMUNICATION

### 4.1 Format de Message Standard

```python
class AgentMessage:
    """Message inter-agents standardisé"""
    
    # Identifiants
    message_id: str          # UUID unique
    conversation_id: str     # ID conversation
    parent_id: Optional[str] # ID message parent
    
    # Routing
    from_agent: str          # ID agent source
    to_agent: str            # ID agent destination
    routing_path: List[str]  # Chemin parcouru
    
    # Contenu
    type: MessageType        # TEXT, TASK, RESULT, ERROR, STATUS
    content: MessageContent  # Contenu structuré
    
    # Metadata
    priority: Priority       # LOW, NORMAL, HIGH, URGENT
    timestamp: datetime
    ttl_seconds: int         # Time to live
    
    # Context
    context: Dict[str, Any]  # Contexte partagé
    user_context: Dict       # Contexte utilisateur
    
    # Tokens
    token_budget: int        # Budget tokens alloué
    tokens_used: int         # Tokens utilisés
```

### 4.2 Types de Messages

```python
class MessageType(Enum):
    # Communication
    TEXT = "text"              # Message texte simple
    QUERY = "query"            # Question/requête
    RESPONSE = "response"      # Réponse
    
    # Tâches
    TASK_REQUEST = "task_request"      # Demande de tâche
    TASK_ACCEPT = "task_accept"        # Acceptation
    TASK_REJECT = "task_reject"        # Rejet
    TASK_PROGRESS = "task_progress"    # Progression
    TASK_COMPLETE = "task_complete"    # Complétion
    TASK_FAILED = "task_failed"        # Échec
    
    # Délégation
    DELEGATE = "delegate"              # Délégation
    ESCALATE = "escalate"              # Escalade
    
    # Système
    HEARTBEAT = "heartbeat"            # Alive check
    STATUS = "status"                  # Status update
    ERROR = "error"                    # Erreur
    
    # Données
    DATA_REQUEST = "data_request"      # Demande données
    DATA_RESPONSE = "data_response"    # Réponse données
```

### 4.3 Protocole de Délégation

```
┌─────────────────────────────────────────────────────────────┐
│                    DÉLÉGATION HIÉRARCHIQUE                  │
└─────────────────────────────────────────────────────────────┘

User: "Génère un rapport financier Q4 avec graphiques"
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. NOVA reçoit la requête                                   │
│    - Analyse l'intention                                     │
│    - Identifie: finance + creative                          │
│    - Délègue à MasterMind                                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. MASTER MIND analyse et décompose                         │
│    - Tâche 1: Extraire données Q4 (Finance)                 │
│    - Tâche 2: Calculer métriques (Analytics)                │
│    - Tâche 3: Créer graphiques (Creative)                   │
│    - Tâche 4: Assembler rapport (Finance)                   │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ DIR_FINANCE │   │DIR_ANALYTICS│   │DIR_CREATIVE │
│  Frank      │   │   Dana      │   │   Carla     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Report Rosa │   │ Metric Mike │   │ Visual Vera │
│   FIN_007   │   │   ANA_003   │   │   ANA_007   │
└─────────────┘   └─────────────┘   └─────────────┘
```

### 4.4 Patterns de Communication

#### Pattern 1: Request-Response
```python
# Synchrone, simple
async def request_response(from_agent, to_agent, request):
    message = AgentMessage(
        type=MessageType.QUERY,
        from_agent=from_agent,
        to_agent=to_agent,
        content=request
    )
    response = await send_and_wait(message, timeout=30)
    return response
```

#### Pattern 2: Fire-and-Forget
```python
# Asynchrone, notifications
async def fire_and_forget(from_agent, to_agent, notification):
    message = AgentMessage(
        type=MessageType.STATUS,
        from_agent=from_agent,
        to_agent=to_agent,
        content=notification
    )
    await send_async(message)  # No wait
```

#### Pattern 3: Publish-Subscribe
```python
# Événements broadcast
async def publish_event(from_agent, event_type, data):
    subscribers = get_subscribers(event_type)
    for subscriber in subscribers:
        message = AgentMessage(
            type=MessageType.DATA_RESPONSE,
            from_agent=from_agent,
            to_agent=subscriber,
            content=data
        )
        await send_async(message)
```

#### Pattern 4: Chain of Responsibility
```python
# Pipeline de traitement
async def chain_process(task, agent_chain):
    result = task
    for agent in agent_chain:
        result = await agent.process(result)
        if result.is_complete:
            break
    return result
```

---

## 5. OPTIMISATION DES TOKENS

### 5.1 Context Window par Provider

| Provider | Modèle | Context Window | Max Output | Coût Input/1K | Coût Output/1K |
|----------|--------|----------------|------------|---------------|----------------|
| Anthropic | Claude Sonnet 4 | 200K | 8K | $0.003 | $0.015 |
| Anthropic | Claude Opus 4 | 200K | 8K | $0.015 | $0.075 |
| Anthropic | Claude Haiku 4 | 200K | 8K | $0.00025 | $0.00125 |
| OpenAI | GPT-4o | 128K | 4K | $0.005 | $0.015 |
| OpenAI | GPT-4o-mini | 128K | 4K | $0.00015 | $0.0006 |
| OpenAI | o1 | 200K | 100K | $0.015 | $0.060 |
| Google | Gemini 1.5 Pro | 2M | 8K | $0.00125 | $0.005 |
| Google | Gemini 1.5 Flash | 1M | 8K | $0.000075 | $0.0003 |

### 5.2 Budget Tokens par Niveau

```python
TOKEN_BUDGETS = {
    "L-1_NOVA": {
        "per_turn": 4000,        # Par interaction
        "context_reserve": 50000, # Réserve contexte
        "max_conversation": 150000  # Max conversation
    },
    "L0_MASTERMIND": {
        "per_task": 8000,        # Par tâche
        "routing": 1000,         # Pour routing
        "decomposition": 2000,   # Pour décomposition
        "assembly": 2000         # Pour assemblage
    },
    "L1_DIRECTOR": {
        "per_task": 4000,        # Par tâche
        "coordination": 1000,    # Coordination
        "max_parallel": 3        # Tâches parallèles
    },
    "L2_SPECIALIST": {
        "per_task": 2000,        # Par tâche
        "tool_calls": 500,       # Appels outils
        "max_iterations": 5      # Itérations max
    }
}
```

### 5.3 Techniques d'Optimisation

#### 5.3.1 Compression de Contexte
```python
class ContextCompressor:
    """Compresse le contexte pour économiser des tokens"""
    
    def compress_conversation(self, messages: List[Message]) -> List[Message]:
        """
        Stratégies:
        1. Summarize old messages (keep last 5 full)
        2. Remove redundant info
        3. Extract key entities
        """
        if len(messages) <= 5:
            return messages
        
        # Keep last 5 full
        recent = messages[-5:]
        
        # Summarize older ones
        old = messages[:-5]
        summary = self.summarize_messages(old)
        
        return [summary] + recent
    
    def summarize_messages(self, messages: List[Message]) -> Message:
        """Crée un résumé compact des anciens messages"""
        key_points = self.extract_key_points(messages)
        entities = self.extract_entities(messages)
        decisions = self.extract_decisions(messages)
        
        return Message(
            role="system",
            content=f"""
            Context Summary:
            - Key points: {key_points}
            - Entities: {entities}
            - Decisions: {decisions}
            """
        )
```

#### 5.3.2 Prompt Templates Optimisés
```python
OPTIMIZED_PROMPTS = {
    "task_routing": """
    Route: {task_summary}
    Ctx: {context_key_points}
    Options: {department_list}
    → Department + confidence
    """,  # ~50 tokens vs ~200 verbose
    
    "task_execution": """
    Task: {task}
    Input: {input_summary}
    Tools: {available_tools}
    Budget: {token_budget}
    → Execute + result
    """,  # ~40 tokens
    
    "result_assembly": """
    Results: {results_summary}
    Format: {output_format}
    → Assembled output
    """  # ~30 tokens
}
```

#### 5.3.3 Caching Intelligent
```python
class TokenAwareCache:
    """Cache qui économise des tokens"""
    
    def __init__(self):
        self.l1_cache = {}  # Memory (fast, small)
        self.l2_cache = None  # Redis (slower, large)
        
    async def get_or_compute(
        self,
        key: str,
        compute_fn: Callable,
        ttl: int = 3600,
        token_cost: int = 0
    ):
        # Check L1
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # Check L2
        if self.l2_cache:
            cached = await self.l2_cache.get(key)
            if cached:
                self.l1_cache[key] = cached  # Promote
                return cached
        
        # Compute (costs tokens)
        result = await compute_fn()
        
        # Store
        self.l1_cache[key] = result
        if self.l2_cache:
            await self.l2_cache.setex(key, ttl, result)
        
        return result
```

#### 5.3.4 Streaming pour Réponses Longues
```python
async def stream_response(
    prompt: str,
    max_tokens: int,
    callback: Callable
):
    """
    Stream au lieu de tout générer:
    - Réduit latence perçue
    - Permet early stopping
    - Meilleure UX
    """
    async for chunk in llm.stream(prompt, max_tokens):
        await callback(chunk)
        
        # Early stopping si suffisant
        if is_complete_response(accumulated):
            break
```

### 5.4 Sélection de Modèle Intelligente

```python
class ModelSelector:
    """Sélectionne le modèle optimal selon la tâche"""
    
    def select_model(self, task: Task) -> str:
        complexity = task.complexity  # 0-1
        token_budget = task.token_budget
        required_caps = task.required_capabilities
        
        # Tâche simple → Haiku (cheap, fast)
        if complexity < 0.3 and "complex_reasoning" not in required_caps:
            return "claude-haiku-4-20250514"
        
        # Tâche moyenne → Sonnet (balanced)
        if complexity < 0.7:
            return "claude-sonnet-4-20250514"
        
        # Tâche complexe → Opus (powerful)
        if "complex_reasoning" in required_caps:
            return "claude-opus-4-20250514"
        
        # Code heavy → Consider alternatives
        if "code" in required_caps and token_budget > 50000:
            return "gpt-4o"  # Good for code
        
        # Default
        return "claude-sonnet-4-20250514"
```

---

## 6. GESTION DE LA MÉMOIRE

### 6.1 Types de Mémoire

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE MÉMOIRE                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  SHORT-TERM │    │  WORKING    │    │  LONG-TERM  │
│   MEMORY    │    │   MEMORY    │    │   MEMORY    │
│  (Context)  │    │  (Session)  │    │    (DB)     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 200K tokens      │ Redis            │ PostgreSQL
       │ Current turn     │ 24h TTL          │ Permanent
       │                  │                  │
       └──────────────────┴──────────────────┘
```

### 6.2 Short-Term Memory (Contexte LLM)
```python
class ShortTermMemory:
    """Mémoire dans le context window LLM"""
    
    def __init__(self, max_tokens: int = 150000):
        self.messages: List[Message] = []
        self.max_tokens = max_tokens
        self.current_tokens = 0
    
    def add_message(self, message: Message):
        tokens = count_tokens(message)
        
        # Evict old if needed
        while self.current_tokens + tokens > self.max_tokens:
            removed = self.messages.pop(0)
            self.current_tokens -= count_tokens(removed)
        
        self.messages.append(message)
        self.current_tokens += tokens
    
    def get_context(self) -> List[Message]:
        return self.messages
```

### 6.3 Working Memory (Session)
```python
class WorkingMemory:
    """Mémoire de session dans Redis"""
    
    def __init__(self, redis_client, session_id: str):
        self.redis = redis_client
        self.session_id = session_id
        self.prefix = f"wm:{session_id}:"
    
    async def store(self, key: str, value: Any, ttl: int = 86400):
        """Store with 24h default TTL"""
        await self.redis.setex(
            f"{self.prefix}{key}",
            ttl,
            json.dumps(value)
        )
    
    async def retrieve(self, key: str) -> Optional[Any]:
        data = await self.redis.get(f"{self.prefix}{key}")
        return json.loads(data) if data else None
    
    async def get_conversation_state(self) -> Dict:
        """Get full conversation state"""
        return {
            "entities": await self.retrieve("entities"),
            "decisions": await self.retrieve("decisions"),
            "pending_tasks": await self.retrieve("pending_tasks"),
            "user_preferences": await self.retrieve("user_prefs")
        }
```

### 6.4 Long-Term Memory (Base de données)
```python
class LongTermMemory:
    """Mémoire persistante dans PostgreSQL"""
    
    async def store_interaction(self, interaction: Interaction):
        """Store une interaction complète"""
        await self.db.execute("""
            INSERT INTO interactions 
            (user_id, session_id, query, response, agents_used, 
             tokens_used, duration_ms, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """, interaction.to_tuple())
    
    async def get_user_history(
        self, 
        user_id: str, 
        limit: int = 100
    ) -> List[Interaction]:
        """Récupère l'historique utilisateur"""
        rows = await self.db.fetch("""
            SELECT * FROM interactions
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        """, user_id, limit)
        return [Interaction.from_row(r) for r in rows]
    
    async def get_similar_queries(
        self,
        query_embedding: List[float],
        limit: int = 5
    ) -> List[Interaction]:
        """Trouve des requêtes similaires (RAG)"""
        rows = await self.db.fetch("""
            SELECT *, embedding <-> $1 AS distance
            FROM interactions
            WHERE embedding IS NOT NULL
            ORDER BY distance
            LIMIT $2
        """, query_embedding, limit)
        return [Interaction.from_row(r) for r in rows]
```

### 6.5 Shared Context entre Agents
```python
class SharedContext:
    """Contexte partagé entre agents pour une tâche"""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.data = {}
        self.lock = asyncio.Lock()
    
    async def update(self, agent_id: str, key: str, value: Any):
        """Update thread-safe"""
        async with self.lock:
            if agent_id not in self.data:
                self.data[agent_id] = {}
            self.data[agent_id][key] = value
    
    async def get(self, key: str, from_agent: str = None) -> Any:
        """Get from specific agent or merged"""
        if from_agent:
            return self.data.get(from_agent, {}).get(key)
        
        # Merge all agents' data for this key
        merged = {}
        for agent_data in self.data.values():
            if key in agent_data:
                merged.update(agent_data[key])
        return merged
    
    def to_prompt_context(self) -> str:
        """Convertit en contexte pour prompt"""
        return json.dumps(self.data, indent=2)
```

---

## 7. PATTERNS D'IMPLÉMENTATION

### 7.1 Pattern: Agent Base Class
```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Classe de base pour tous les agents"""
    
    def __init__(self, config: AgentConfig):
        self.id = config.id
        self.name = config.name
        self.level = config.level
        self.department = config.department
        self.llm_model = config.llm_model
        self.capabilities = config.capabilities
        
        # Metrics
        self.tasks_completed = 0
        self.tokens_used = 0
        self.avg_response_time = 0
    
    @abstractmethod
    async def process(self, task: Task) -> TaskResult:
        """Traite une tâche - à implémenter"""
        pass
    
    async def delegate(self, task: Task, to_agent: str) -> TaskResult:
        """Délègue à un autre agent"""
        message = AgentMessage(
            type=MessageType.DELEGATE,
            from_agent=self.id,
            to_agent=to_agent,
            content=task
        )
        return await self.send_and_wait(message)
    
    async def report(self, to_supervisor: str, result: TaskResult):
        """Rapporte au superviseur"""
        message = AgentMessage(
            type=MessageType.TASK_COMPLETE,
            from_agent=self.id,
            to_agent=to_supervisor,
            content=result
        )
        await self.send_async(message)
```

### 7.2 Pattern: Task Decomposition
```python
class TaskDecomposer:
    """Décompose les tâches complexes"""
    
    async def decompose(self, task: Task) -> List[SubTask]:
        # Analyze complexity
        complexity = await self.analyze_complexity(task)
        
        if complexity.score < 0.3:
            # Simple task, no decomposition
            return [task.as_subtask()]
        
        # Use LLM to decompose
        prompt = f"""
        Decompose this task into subtasks:
        Task: {task.description}
        Context: {task.context}
        
        Output JSON:
        [
            {{"id": "1", "description": "...", "department": "...", "depends_on": []}},
            ...
        ]
        """
        
        result = await self.llm.complete(prompt, max_tokens=1000)
        subtasks = json.loads(result)
        
        return [SubTask(**st) for st in subtasks]
```

### 7.3 Pattern: Result Assembly
```python
class ResultAssembler:
    """Assemble les résultats de plusieurs agents"""
    
    async def assemble(
        self, 
        results: List[TaskResult],
        strategy: AssemblyStrategy
    ) -> AssembledResult:
        
        if strategy == AssemblyStrategy.MERGE:
            return await self.merge_results(results)
        
        elif strategy == AssemblyStrategy.SYNTHESIZE:
            return await self.synthesize_with_llm(results)
        
        elif strategy == AssemblyStrategy.BEST_OF:
            return await self.select_best(results)
        
        elif strategy == AssemblyStrategy.CONCATENATE:
            return self.concatenate(results)
    
    async def synthesize_with_llm(self, results: List[TaskResult]) -> AssembledResult:
        """Utilise LLM pour synthétiser"""
        prompt = f"""
        Synthesize these results into a coherent response:
        
        {[r.to_summary() for r in results]}
        
        Provide a unified, well-structured response.
        """
        
        synthesis = await self.llm.complete(prompt, max_tokens=2000)
        return AssembledResult(content=synthesis, sources=results)
```

### 7.4 Pattern: Error Handling & Recovery
```python
class AgentErrorHandler:
    """Gestion des erreurs avec recovery"""
    
    async def handle_error(
        self,
        error: Exception,
        task: Task,
        agent: BaseAgent
    ) -> RecoveryAction:
        
        error_type = type(error).__name__
        
        # Timeout → Retry with longer timeout
        if isinstance(error, TimeoutError):
            return RecoveryAction(
                action="retry",
                modifications={"timeout": task.timeout * 2}
            )
        
        # Rate limit → Wait and retry
        if "rate_limit" in str(error).lower():
            return RecoveryAction(
                action="wait_retry",
                wait_seconds=60
            )
        
        # Token limit → Compress and retry
        if "token" in str(error).lower():
            return RecoveryAction(
                action="compress_retry",
                modifications={"compress_context": True}
            )
        
        # Agent failure → Escalate
        if isinstance(error, AgentError):
            return RecoveryAction(
                action="escalate",
                to_agent=agent.supervisor_id
            )
        
        # Unknown → Log and fail gracefully
        return RecoveryAction(
            action="fail_graceful",
            error_message=str(error)
        )
```

---

## ANNEXE: QUICK REFERENCE

### Agent Hierarchy
```
L-1: NOVA (1)
L0:  MASTERMIND (1)
L1:  DIRECTORS (14)
L2:  SPECIALISTS (101)
L3:  TOOLS (80+)
```

### Communication Flow
```
User → Nova → MasterMind → Director → Specialist → Tool
                    ↓
              LLM Router
```

### Token Budgets
```
Nova: 4K/turn, 150K/conv
MasterMind: 8K/task
Director: 4K/task
Specialist: 2K/task
```

### Cache Layers
```
L1: Memory (1000 items, 5min TTL)
L2: Redis (unlimited, 1h TTL)
L3: PostgreSQL (permanent)
```

---

*Document technique CHE·NU™ V25 - Architecture Agents*
