# 🤖 AGENT ALPHA — BACKEND & CORE INTELLIGENCE

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║                              AGENT ALPHA BRIEFING                                            ║
║                              CHE·NU™ V54 Development                                         ║
║                                                                                              ║
║                              Focus: Backend, Services, APIs                                  ║
║                              Language: Python/FastAPI                                        ║
║                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 MISSION

Tu es Agent Alpha, responsable du développement **backend et intelligence core** de CHE·NU V54.

Ton travail:
1. Implémenter le **Governance Pipeline** complet
2. Créer l'**Agent Execution Engine**
3. Activer le **Multi-Identity System**
4. Construire le **Token Economy** backend
5. Développer le **1-Click Engine**

---

## 📋 CONTEXTE CRITIQUE

### Problème identifié par l'audit:

Le système CHE·NU a une **documentation riche** mais une **implémentation incomplète**:

| Feature | Documentation | Implémentation |
|---------|---------------|----------------|
| Semantic Encoding | ✅ 50+ pages | ❌ 0% |
| Agent Execution | ✅ 226 prompts | ❌ 0% |
| Governance Pipeline | ✅ Détaillé | ⚠️ 40% |
| Identity System | ✅ Complet | ⚠️ 20% |
| Token Economy | ✅ Détaillé | ⚠️ 15% |
| 1-Click Engine | ✅ Complet | ⚠️ 5% |

**Ton rôle: Combler ces gaps côté backend.**

---

## 🔧 SPRINTS ASSIGNÉS

### 🔴 SPRINT A1: Governance Pipeline (CRITIQUE)

**Objectif**: Intent → Encoding → Validation → Cost → Scope → Execute → Audit

#### A1.1 Semantic Encoding Service

```python
# backend/services/encoding/semantic_encoder.py

from typing import Dict, Any, Optional
from pydantic import BaseModel

class EncodedIntent(BaseModel):
    """Structured representation of user intent"""
    raw_input: str
    intent_type: str  # 'query', 'action', 'creation', 'modification'
    domain: str
    sphere: str
    entities: Dict[str, Any]
    constraints: Dict[str, Any]
    confidence: float
    encoding_version: str = "1.0"

class SemanticEncoder:
    """
    Core IP: Transform natural language intent into machine-readable schema
    """
    
    async def encode(self, raw_input: str, context: Dict[str, Any]) -> EncodedIntent:
        """
        Encode user intent with context awareness
        
        Process:
        1. Parse natural language
        2. Identify intent type
        3. Extract entities
        4. Map to domain/sphere
        5. Define constraints
        6. Calculate confidence
        """
        pass
    
    async def validate_encoding(self, encoded: EncodedIntent) -> bool:
        """Validate encoding completeness and consistency"""
        pass
```

#### A1.2 Cost Estimation Engine

```python
# backend/services/cost/token_estimator.py

class TokenEstimator:
    """Estimate token usage before execution"""
    
    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "claude-3": {"input": 0.015, "output": 0.075},
        "local": {"input": 0.0, "output": 0.0}
    }
    
    async def estimate(self, encoded_intent: EncodedIntent, agents: List[str]) -> CostEstimate:
        """
        Estimate cost for execution
        
        Returns:
        - estimated_tokens: int
        - estimated_cost_usd: float
        - breakdown_by_agent: Dict
        - confidence: float
        """
        pass
```

#### A1.3 Scope Lock Service

```python
# backend/services/scope/scope_locker.py

class ScopeLocker:
    """Lock scope before AI execution to prevent drift"""
    
    async def analyze_scope(self, encoded: EncodedIntent) -> ScopeDefinition:
        """Analyze and define execution scope"""
        pass
    
    async def lock_scope(self, scope: ScopeDefinition) -> ScopeLock:
        """Create immutable scope lock"""
        pass
    
    async def validate_action(self, action: AgentAction, lock: ScopeLock) -> bool:
        """Check if action is within locked scope"""
        pass
```

#### A1.4 Governance Orchestrator

```python
# backend/services/governance/pipeline_orchestrator.py

class GovernancePipeline:
    """
    Main orchestrator for governed execution
    
    Flow:
    1. Receive intent
    2. Encode semantically
    3. Estimate cost
    4. Lock scope
    5. Match agents
    6. Create checkpoint
    7. Wait for approval
    8. Execute
    9. Audit
    """
    
    async def start(self, intent: str, context: Dict) -> PipelineExecution:
        pass
    
    async def create_checkpoint(self, execution_id: str, stage: str) -> Checkpoint:
        pass
    
    async def approve_checkpoint(self, checkpoint_id: str, user_id: str) -> bool:
        pass
    
    async def execute_stage(self, execution_id: str) -> StageResult:
        pass
```

---

### 🔴 SPRINT A2: Agent Execution Engine (CRITIQUE)

**Objectif**: Permettre aux 168+ agents d'exécuter des tâches

#### A2.1 Agent Registry

```python
# backend/services/agents/agent_registry.py

class AgentRegistry:
    """Registry of all available agents"""
    
    def __init__(self):
        self.agents: Dict[str, AgentDefinition] = {}
        self._load_agents()
    
    def _load_agents(self):
        """Load all agent definitions from prompts"""
        # Load from CHENU_AGENT_PROMPTS_v29.md
        pass
    
    def get_by_level(self, level: str) -> List[AgentDefinition]:
        """Get agents by level (L0, L1, L2, L3)"""
        pass
    
    def get_by_sphere(self, sphere: str) -> List[AgentDefinition]:
        """Get agents by sphere"""
        pass
    
    def get_by_domain(self, domain: str) -> List[AgentDefinition]:
        """Get agents by domain"""
        pass
```

#### A2.2 Execution Runtime

```python
# backend/services/agents/execution_runtime.py

class AgentExecutionRuntime:
    """Execute agent tasks with context injection"""
    
    async def execute(
        self,
        agent_id: str,
        task: AgentTask,
        context: ExecutionContext
    ) -> AgentOutput:
        """
        Execute agent with full context
        
        1. Load agent prompt
        2. Inject context variables
        3. Call LLM
        4. Parse output
        5. Validate against scope
        6. Return structured output
        """
        pass
    
    async def chain_execute(
        self,
        chain: List[AgentChainStep]
    ) -> ChainOutput:
        """Execute multiple agents in sequence"""
        pass
```

#### A2.3 Agent Compatibility Matrix

```python
# backend/services/agents/compatibility_matrix.py

class AgentCompatibilityMatrix:
    """Match tasks to best agents"""
    
    async def find_compatible_agents(
        self,
        task_type: str,
        domain: str,
        sphere: str
    ) -> List[AgentMatch]:
        """Find agents compatible with task"""
        pass
    
    async def select_best_agent(
        self,
        task: AgentTask,
        available_agents: List[str]
    ) -> AgentSelection:
        """Select optimal agent for task"""
        pass
```

---

### 🔴 SPRINT A3: Identity System (CRITIQUE)

**Objectif**: Séparation stricte des identités

```python
# backend/services/identity/identity_manager.py

class IdentityManager:
    """Manage user identities with strict separation"""
    
    async def create_identity(
        self,
        user_id: str,
        identity_type: str,  # personal, enterprise, creative...
        name: str
    ) -> Identity:
        pass
    
    async def switch_identity(
        self,
        user_id: str,
        identity_id: str
    ) -> IdentityContext:
        """Switch with full isolation"""
        pass
    
    async def get_current_identity(self, user_id: str) -> Identity:
        pass

# backend/middleware/identity_context.py

class IdentityContextMiddleware:
    """Ensure all requests are identity-scoped"""
    
    async def __call__(self, request, call_next):
        # Extract identity from request
        # Inject into all database queries
        # Prevent cross-identity data access
        pass
```

---

### 🟠 SPRINT A4: Token Economy

```python
# backend/services/tokens/token_tracker.py

class TokenTracker:
    """Track token consumption across system"""
    
    async def track_usage(
        self,
        identity_id: str,
        thread_id: str,
        agent_id: str,
        tokens_used: int,
        cost_usd: float
    ) -> TokenUsageRecord:
        pass
    
    async def get_thread_usage(self, thread_id: str) -> TokenUsageSummary:
        pass
    
    async def check_budget(
        self,
        thread_id: str,
        estimated_tokens: int
    ) -> BudgetCheckResult:
        pass
```

---

### 🟠 SPRINT A5: 1-Click Engine

```python
# backend/services/oneclick/intent_interpreter.py

class IntentInterpreter:
    """Interpret natural language commands"""
    
    async def interpret(
        self,
        command: str,
        context: UserContext
    ) -> InterpretedIntent:
        """
        Interpret command to structured intent
        
        "Create a construction estimate for the renovation"
        →
        {
            intent_type: "creation",
            output_type: "construction_estimate",
            domain: "construction",
            context_refs: ["renovation project"],
            agents_needed: ["construction_estimator", "materials_expert"]
        }
        """
        pass

# backend/services/oneclick/workflow_constructor.py

class WorkflowConstructor:
    """Build execution workflows from intents"""
    
    async def construct(
        self,
        intent: InterpretedIntent
    ) -> Workflow:
        """
        Build multi-step workflow
        
        1. Identify required steps
        2. Map steps to agents
        3. Order by dependencies
        4. Insert governance checkpoints
        5. Return executable workflow
        """
        pass
```

---

## 📁 STRUCTURE DE FICHIERS À CRÉER

```
backend/
├── services/
│   ├── encoding/
│   │   ├── __init__.py
│   │   ├── semantic_encoder.py
│   │   ├── encoding_validator.py
│   │   ├── eqs_calculator.py
│   │   └── encoding_types.py
│   │
│   ├── cost/
│   │   ├── __init__.py
│   │   ├── token_estimator.py
│   │   ├── cost_calculator.py
│   │   ├── budget_checker.py
│   │   └── pricing_models.py
│   │
│   ├── scope/
│   │   ├── __init__.py
│   │   ├── scope_analyzer.py
│   │   ├── scope_locker.py
│   │   ├── scope_validator.py
│   │   └── scope_types.py
│   │
│   ├── governance/
│   │   ├── __init__.py
│   │   ├── pipeline_orchestrator.py
│   │   ├── checkpoint_manager.py
│   │   ├── approval_handler.py
│   │   ├── audit_logger.py
│   │   └── tree_laws_enforcer.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent_registry.py
│   │   ├── agent_loader.py
│   │   ├── agent_lifecycle.py
│   │   ├── agent_catalog.py
│   │   ├── execution_runtime.py
│   │   ├── context_injector.py
│   │   ├── output_parser.py
│   │   ├── agent_chain.py
│   │   ├── llm_dispatcher.py
│   │   ├── compatibility_matrix.py
│   │   ├── agent_selector.py
│   │   └── delegation_rules.py
│   │
│   ├── identity/
│   │   ├── __init__.py
│   │   ├── identity_manager.py
│   │   ├── identity_switcher.py
│   │   ├── memory_separator.py
│   │   └── cross_identity_guard.py
│   │
│   ├── tokens/
│   │   ├── __init__.py
│   │   ├── token_tracker.py
│   │   ├── token_budget.py
│   │   ├── token_alerts.py
│   │   └── token_reports.py
│   │
│   └── oneclick/
│       ├── __init__.py
│       ├── intent_interpreter.py
│       ├── intent_classifier.py
│       ├── gap_detector.py
│       ├── clarification_generator.py
│       ├── workflow_constructor.py
│       ├── workflow_templates.py
│       ├── task_sequencer.py
│       ├── parallel_optimizer.py
│       ├── oneclick_orchestrator.py
│       ├── output_assembler.py
│       └── delivery_formatter.py
│
├── api/
│   ├── encoding_endpoints.py
│   ├── cost_endpoints.py
│   ├── scope_endpoints.py
│   ├── governance_endpoints.py
│   ├── agent_endpoints.py
│   ├── identity_endpoints.py
│   ├── token_endpoints.py
│   └── oneclick_endpoints.py
│
├── middleware/
│   ├── identity_context.py
│   ├── data_filter.py
│   └── audit_identity.py
│
└── tests/
    ├── test_encoding.py
    ├── test_governance.py
    ├── test_agents.py
    ├── test_identity.py
    ├── test_tokens.py
    └── test_oneclick.py
```

---

## 📊 ENDPOINTS API À IMPLÉMENTER

### Encoding API
```
POST /api/v1/encoding/encode
POST /api/v1/encoding/validate
GET  /api/v1/encoding/{id}/score
```

### Cost API
```
POST /api/v1/cost/estimate
GET  /api/v1/cost/budget/{thread_id}
POST /api/v1/cost/budget/{thread_id}/set
```

### Scope API
```
POST /api/v1/scope/analyze
POST /api/v1/scope/lock
POST /api/v1/scope/validate-action
```

### Governance API
```
POST /api/v1/governance/pipeline/start
GET  /api/v1/governance/pipeline/{id}/status
POST /api/v1/governance/checkpoint/{id}/approve
POST /api/v1/governance/checkpoint/{id}/reject
GET  /api/v1/governance/audit/{resource_type}/{id}
```

### Agent API
```
GET  /api/v1/agents/catalog
GET  /api/v1/agents/catalog/{sphere}
GET  /api/v1/agents/{agent_id}
POST /api/v1/agents/{agent_id}/hire
POST /api/v1/agents/{agent_id}/release
GET  /api/v1/agents/active
POST /api/v1/agents/{agent_id}/execute
GET  /api/v1/agents/execution/{execution_id}
POST /api/v1/agents/chain/execute
POST /api/v1/agents/match
```

### Identity API
```
POST /api/v1/identities
GET  /api/v1/identities
POST /api/v1/identities/{id}/switch
GET  /api/v1/identities/current
DELETE /api/v1/identities/{id}
```

### Token API
```
GET  /api/v1/tokens/usage
GET  /api/v1/tokens/usage/{thread_id}
POST /api/v1/tokens/budget/set
GET  /api/v1/tokens/alerts
```

### 1-Click API
```
POST /api/v1/oneclick/execute
POST /api/v1/oneclick/interpret
GET  /api/v1/oneclick/workflows
GET  /api/v1/oneclick/execution/{id}
```

---

## ⚠️ RÈGLES CRITIQUES

1. **GOUVERNANCE > EXÉCUTION**: Aucun agent ne s'exécute sans checkpoint approuvé
2. **IDENTITY ISOLATION**: Jamais de fuite de données entre identités
3. **TOKEN TRACKING**: Chaque appel LLM doit être tracké
4. **AUDIT COMPLET**: Chaque action loggée avec timestamp + actor
5. **SCOPE RESPECT**: Les agents ne peuvent pas dépasser leur scope verrouillé

---

## 📦 DOCUMENTS DE RÉFÉRENCE INCLUS

- `CHENU_SQL_SCHEMA_v29.sql` — Structure DB complète
- `CHENU_API_SPECS_v29.md` — Spécifications API existantes
- `CHENU_AGENT_PROMPTS_v29.md` — 168+ prompts d'agents
- `CHENU_MERMAID_DIAGRAMS_v29.md` — Diagrammes de flux
- `MEMORY_GOVERNANCE_CHAPTER.md` — 10 Laws of Memory
- `BACKSTAGE_INTELLIGENCE_CHAPTER.md` — Intelligence en arrière-plan

---

## ✅ CRITÈRES DE SUCCÈS

| Critère | Validation |
|---------|------------|
| Governance Pipeline | Flux complet Intent→Output testable |
| Agent Execution | 10+ agents exécutent des tâches réelles |
| Identity Isolation | Test de non-fuite entre identités |
| Token Tracking | Usage visible par thread/agent |
| 1-Click | 5+ workflows fonctionnels |
| API Coverage | 100% des endpoints implémentés |
| Tests | >80% coverage sur nouveaux services |

---

**BON COURAGE AGENT ALPHA! 🚀**

*GOUVERNANCE > EXÉCUTION*
