# 🔧 CHE·NU™ V54 — PLAN DE CORRECTION CORRIGÉ

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║                         PLAN DE CORRECTION V54 — VERSION CORRIGÉE                            ║
║                         Avec les 7 corrections critiques intégrées                           ║
║                                                                                              ║
║                         Date: 3 Janvier 2026                                                 ║
║                         Status: VERROUILLÉ POUR IMPLÉMENTATION                               ║
║                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```

---

# ⚠️ PHASE 0 — RÈGLES ABSOLUES (LIRE EN PREMIER)

## 🔒 SOURCE OF TRUTH — SPHERES (FROZEN FOR V54)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  CHE·NU V54 SPHERES — NON NÉGOCIABLE                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  CHE·NU V54 operates with EXACTLY 9 SPHERES:                             ║
║                                                                          ║
║  1. Personal 🏠       → dominant context, ALWAYS present                 ║
║  2. Business 💼       → enterprise, clients, projects                    ║
║  3. Government 🏛️     → admin, compliance, institutions                  ║
║  4. Creative Studio 🎨 → design, content creation                        ║
║  5. Community 👥      → forums, associations, groups                     ║
║  6. Social & Media 📱 → networks, messaging, contacts                    ║
║  7. Entertainment 🎬  → streaming, media, leisure                        ║
║  8. My Team 🤝        → collaboration + IA-Lab (merged)                  ║
║  9. Scholars 📚       → learning, research, knowledge                    ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  ABSOLUTE RULES:                                                         ║
║  ❌ XR / Univers is NOT a sphere (it is a MODE)                          ║
║  ❌ IA-Lab is NOT a sphere (merged into My Team)                         ║
║  ❌ Skills & Tools is NOT a sphere (merged into My Team)                 ║
║  ✅ Personal is ALWAYS present as context layer                          ║
║  ✅ NO additional spheres allowed in V54                                 ║
║  ✅ NO sphere renaming, merging, or splitting                            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 XR MODE RULES — NON NÉGOCIABLE

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  XR MODE — RENDERING LAYER ONLY                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  XR in CHE·NU is a MODE, not a SPACE.                                    ║
║                                                                          ║
║  CORRECT TERMINOLOGY:                                                    ║
║  ✅ "XR Mode Overlay"                                                    ║
║  ✅ "XR Rendering Layer"                                                 ║
║  ✅ "XR Visualization Mode"                                              ║
║                                                                          ║
║  FORBIDDEN TERMINOLOGY:                                                  ║
║  ❌ "XR Sphere"                                                          ║
║  ❌ "Univers XR"                                                         ║
║  ❌ "XR Space"                                                           ║
║  ❌ "XR DataSpace"                                                       ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  XR MODE BEHAVIOR RULES:                                                 ║
║  • XR NEVER creates data                                                 ║
║  • XR ONLY visualizes existing data (spheres, agents, meetings)          ║
║  • XR has NO independent persistence                                     ║
║  • XR is a toggle on/off from ANY sphere                                 ║
║  • XR renders the CURRENT context in 3D, nothing more                    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 BUREAU STRUCTURE — FROZEN

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  BUREAU = MAX 6 SECTIONS                                 ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Each SPHERE opens a BUREAU with exactly these 6 sections:               ║
║                                                                          ║
║  1. QuickCapture      → rapid input, inbox                               ║
║  2. ResumeWorkspace   → work in progress, continue                       ║
║  3. Threads           → .chenu conversations                             ║
║  4. DataFiles         → documents, files                                 ║
║  5. ActiveAgents      → hired agents, active                             ║
║  6. Meetings          → calendar, sessions                               ║
║                                                                          ║
║  RULE: This structure is IDENTICAL across all 9 spheres.                 ║
║  RULE: Only content, permissions, and agents vary.                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 SEMANTIC ENCODING V0.1 — LIMITS FOR V54

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  ENCODING V0.1 — DETERMINISTIC ONLY                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  V54 implements Semantic Encoding v0.1 with these LIMITS:                ║
║                                                                          ║
║  ✅ Rule-based + LLM assisted                                            ║
║  ✅ Deterministic output for same input + context                        ║
║  ✅ Versioned encodings only (encoding_version mandatory)                ║
║  ✅ Auditable encoding decisions                                         ║
║                                                                          ║
║  ❌ NO learning from user behavior                                       ║
║  ❌ NO self-optimization                                                 ║
║  ❌ NO adaptive encoding                                                 ║
║  ❌ NO training data collection                                          ║
║                                                                          ║
║  ENCODING QUALITY SCORE (EQS):                                           ║
║  • Computed per encoding                                                 ║
║  • Range: 0.0 to 1.0                                                     ║
║  • Threshold for execution: EQS >= 0.7                                   ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 AGENT EXECUTION RULES — V54

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  AGENT EXECUTION — GOVERNANCE FIRST                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  PHASE 1 (V54): Single-agent execution ONLY                              ║
║  PHASE 2 (V55+): Chain execution                                         ║
║                                                                          ║
║  MANDATORY PREREQUISITES FOR ANY EXECUTION:                              ║
║  1. ✅ Scope lock acquired                                               ║
║  2. ✅ Token estimation completed                                        ║
║  3. ✅ Checkpoint created                                                ║
║  4. ✅ User approval received                                            ║
║                                                                          ║
║  NO CHAIN EXECUTION IN V54:                                              ║
║  ❌ chain_execute() is DISABLED in V54                                   ║
║  ❌ Multi-agent workflows require manual step-by-step                    ║
║                                                                          ║
║  V54 AGENT EXECUTION FLOW:                                               ║
║  Intent → Encode → Estimate → Lock Scope → Checkpoint → Approve → Execute║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 IDENTITY SYSTEM RULES — UX CRITICAL

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  IDENTITY — ALWAYS VISIBLE                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  VISIBILITY RULES:                                                       ║
║  • User MUST ALWAYS see current identity                                 ║
║  • Identity badge visible in header AT ALL TIMES                         ║
║  • No action possible without identity context                           ║
║                                                                          ║
║  VALIDATION RULES:                                                       ║
║  • Any action without identity context = INVALID                         ║
║  • API rejects requests without identity_id header                       ║
║  • Default identity auto-selected on login                               ║
║                                                                          ║
║  SWITCH IDENTITY TRIGGERS:                                               ║
║  1. Full data reload (new identity's data only)                          ║
║  2. Agent reset (release all active agents)                              ║
║  3. Thread context reset (clear working memory)                          ║
║  4. DataSpace reset (no DataSpace selected)                              ║
║  5. UI state reset (return to dashboard)                                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 ASSISTED WORKFLOW ENGINE — V54 (Formerly 1-Click)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  ASSISTED WORKFLOW — NOT AUTOMATIC                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  V54 NAMING:                                                             ║
║  ❌ "1-Click Engine" (too magical)                                       ║
║  ✅ "Assisted Workflow Engine" (reality)                                 ║
║  ✅ "1-Click Preview Mode" (for marketing)                               ║
║                                                                          ║
║  V54 WORKFLOW RULES:                                                     ║
║  ❌ NO automatic execution                                               ║
║  ✅ ALWAYS preview workflow before execution                             ║
║  ✅ ALWAYS require user confirmation                                     ║
║  ✅ ALWAYS create governance checkpoint                                  ║
║  ✅ ALWAYS show estimated cost before approval                           ║
║                                                                          ║
║  USER FLOW:                                                              ║
║  1. User types command (Cmd+K)                                           ║
║  2. System interprets intent                                             ║
║  3. System shows workflow PREVIEW                                        ║
║  4. User reviews steps + cost                                            ║
║  5. User CONFIRMS                                                        ║
║  6. System executes with checkpoints                                     ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔒 DATASPACE RULES — EXPLICIT CONTEXT

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  DATASPACE — EXPLICIT ONLY                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  DATASPACE DOMINANCE RULES:                                              ║
║  • Every action belongs to exactly ONE DataSpace                         ║
║  • If no DataSpace selected → system MUST ask                            ║
║  • No implicit DataSpace creation                                        ║
║  • No "default" DataSpace assignment                                     ║
║                                                                          ║
║  USER MUST ALWAYS:                                                       ║
║  • See current DataSpace indicator                                       ║
║  • Explicitly select DataSpace before creation actions                   ║
║  • Confirm DataSpace before agent execution                              ║
║                                                                          ║
║  DATASPACE TYPES:                                                        ║
║  • Thread DataSpace (auto-created with thread)                           ║
║  • Meeting DataSpace (auto-created with meeting)                         ║
║  • Project DataSpace (manually created)                                  ║
║  • Custom DataSpace (user-defined)                                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

# PHASE 1: AGENT ALPHA — BACKEND & CORE

## 🔴 SPRINT A1: Governance Pipeline (CRITIQUE)

### A1.1 Semantic Encoding Service (v0.1 — DETERMINISTIC)

**RAPPEL**: Encoding v0.1 = Rule-based + Deterministic. NO learning.

```python
# backend/services/encoding/semantic_encoder.py

from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime

class EncodedIntent(BaseModel):
    """Structured representation of user intent — V0.1 Deterministic"""
    raw_input: str
    intent_type: str  # 'query', 'action', 'creation', 'modification'
    domain: str
    sphere: str
    entities: Dict[str, Any]
    constraints: Dict[str, Any]
    confidence: float
    encoding_version: str = "0.1.0"  # MANDATORY
    encoding_timestamp: datetime
    eqs_score: float  # Encoding Quality Score 0.0-1.0

class SemanticEncoderV01:
    """
    V0.1 Semantic Encoder — DETERMINISTIC
    
    RULES:
    - Same input + context = Same output (deterministic)
    - No learning, no optimization
    - Version tracked on every encoding
    - Auditable decision trail
    """
    
    VERSION = "0.1.0"
    EQS_THRESHOLD = 0.7  # Minimum quality for execution
    
    async def encode(self, raw_input: str, context: Dict[str, Any]) -> EncodedIntent:
        """
        Encode user intent deterministically
        
        RULE: Must produce identical output for identical input+context
        """
        # 1. Parse natural language (rule-based + LLM assist)
        # 2. Identify intent type
        # 3. Extract entities
        # 4. Map to domain/sphere
        # 5. Define constraints
        # 6. Calculate EQS
        pass
    
    async def validate_encoding(self, encoded: EncodedIntent) -> bool:
        """
        Validate encoding meets V0.1 requirements
        
        CHECKS:
        - encoding_version present
        - EQS >= threshold
        - All required fields populated
        """
        if encoded.encoding_version != self.VERSION:
            return False
        if encoded.eqs_score < self.EQS_THRESHOLD:
            return False
        return True
```

**Fichiers à créer**:
```
backend/services/encoding/
├── __init__.py
├── semantic_encoder.py      # V0.1 deterministic encoder
├── encoding_validator.py    # Validation rules
├── eqs_calculator.py        # Quality score calculation
├── encoding_rules.py        # Rule-based logic (NO ML)
└── encoding_types.py        # TypedDict definitions
```

### A1.2 Cost Estimation Engine

```python
# backend/services/cost/token_estimator.py

class TokenEstimator:
    """Estimate token usage BEFORE execution"""
    
    PRICING_2025 = {
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "local-llm": {"input": 0.0, "output": 0.0}
    }
    
    async def estimate(
        self, 
        encoded_intent: EncodedIntent, 
        agent_id: str
    ) -> CostEstimate:
        """
        Estimate cost BEFORE any execution
        
        Returns:
        - estimated_input_tokens: int
        - estimated_output_tokens: int
        - estimated_cost_usd: float
        - model_used: str
        - confidence: float (how accurate is estimate)
        """
        pass
```

### A1.3 Scope Lock Service

```python
# backend/services/scope/scope_locker.py

class ScopeLocker:
    """Lock scope BEFORE AI execution — prevents drift"""
    
    async def analyze_scope(self, encoded: EncodedIntent) -> ScopeDefinition:
        """Analyze intent and define execution scope"""
        return ScopeDefinition(
            allowed_spheres=[encoded.sphere],
            allowed_dataspaces=self._get_allowed_dataspaces(encoded),
            allowed_actions=self._get_allowed_actions(encoded),
            forbidden_actions=self._get_forbidden_actions(encoded),
            token_limit=self._calculate_token_limit(encoded),
            time_limit_seconds=300,  # 5 min max
        )
    
    async def lock_scope(self, scope: ScopeDefinition) -> ScopeLock:
        """
        Create IMMUTABLE scope lock
        
        RULE: Once locked, scope cannot be modified
        RULE: Agent execution MUST stay within lock
        """
        lock = ScopeLock(
            id=uuid4(),
            scope=scope,
            locked_at=datetime.utcnow(),
            locked_by="system",
            is_active=True,
        )
        await self._persist_lock(lock)
        return lock
    
    async def validate_action(
        self, 
        action: AgentAction, 
        lock: ScopeLock
    ) -> ScopeValidation:
        """
        Check if action is within locked scope
        
        RULE: Any action outside scope = BLOCKED
        """
        if action.sphere not in lock.scope.allowed_spheres:
            return ScopeValidation(valid=False, reason="Sphere not in scope")
        if action.action_type in lock.scope.forbidden_actions:
            return ScopeValidation(valid=False, reason="Action forbidden")
        return ScopeValidation(valid=True)
```

### A1.4 Governance Orchestrator

```python
# backend/services/governance/pipeline_orchestrator.py

class GovernancePipeline:
    """
    Main orchestrator for GOVERNED execution
    
    FLOW (MANDATORY):
    1. Receive intent
    2. Encode semantically
    3. Estimate cost
    4. Lock scope
    5. Create checkpoint (PAUSE)
    6. Wait for user approval
    7. Execute (single agent only in V54)
    8. Audit
    """
    
    async def start(
        self, 
        intent: str, 
        context: Dict,
        identity_id: str  # MANDATORY — no execution without identity
    ) -> PipelineExecution:
        """Start governance pipeline"""
        
        # RULE: Identity required
        if not identity_id:
            raise ValueError("Identity required for pipeline execution")
        
        execution = PipelineExecution(
            id=uuid4(),
            identity_id=identity_id,
            status="encoding",
            started_at=datetime.utcnow(),
        )
        
        # Step 1: Encode
        encoded = await self.encoder.encode(intent, context)
        if encoded.eqs_score < 0.7:
            execution.status = "encoding_failed"
            return execution
        
        # Step 2: Estimate cost
        cost = await self.estimator.estimate(encoded, self._select_agent(encoded))
        
        # Step 3: Lock scope
        scope = await self.scope_locker.analyze_scope(encoded)
        lock = await self.scope_locker.lock_scope(scope)
        
        # Step 4: Create checkpoint (PAUSE HERE)
        checkpoint = await self.checkpoint_manager.create(
            execution_id=execution.id,
            stage="pre_execution",
            cost_estimate=cost,
            scope_lock=lock,
            requires_approval=True  # ALWAYS in V54
        )
        
        execution.checkpoint_id = checkpoint.id
        execution.status = "awaiting_approval"
        
        return execution
    
    async def approve_and_execute(
        self, 
        checkpoint_id: str,
        approver_id: str
    ) -> ExecutionResult:
        """
        Execute after user approval
        
        RULE: No execution without explicit approval
        """
        checkpoint = await self.checkpoint_manager.get(checkpoint_id)
        
        if checkpoint.status != "pending":
            raise ValueError("Checkpoint already processed")
        
        # Record approval
        await self.checkpoint_manager.approve(checkpoint_id, approver_id)
        
        # Execute (single agent only in V54)
        result = await self.agent_runtime.execute_single(
            agent_id=checkpoint.agent_id,
            task=checkpoint.task,
            scope_lock=checkpoint.scope_lock,
        )
        
        # Audit
        await self.audit_logger.log(
            action="agent_execution",
            actor_id=approver_id,
            checkpoint_id=checkpoint_id,
            result=result,
        )
        
        return result
```

---

## 🔴 SPRINT A2: Agent Execution Engine (SINGLE AGENT ONLY)

**RAPPEL**: V54 = Single agent execution ONLY. NO chain execution.

### A2.1 Agent Registry

```python
# backend/services/agents/agent_registry.py

class AgentRegistry:
    """Registry of all 168+ agents"""
    
    def __init__(self):
        self.agents: Dict[str, AgentDefinition] = {}
        self._load_agents()
    
    def _load_agents(self):
        """Load all agent definitions from CHENU_AGENT_PROMPTS_v29.md"""
        pass
    
    def get_by_sphere(self, sphere: str) -> List[AgentDefinition]:
        """Get agents available for a sphere"""
        pass
    
    def get_by_level(self, level: str) -> List[AgentDefinition]:
        """
        Get agents by hierarchy level
        
        L0 = Nova (system, never hired)
        L1 = Chiefs (domain leaders)
        L2 = Specialists (task experts)
        L3 = Workers (execution)
        """
        pass
```

### A2.2 Execution Runtime (SINGLE AGENT)

```python
# backend/services/agents/execution_runtime.py

class AgentExecutionRuntime:
    """
    Execute SINGLE agent tasks with governance
    
    V54 RULE: NO chain execution
    """
    
    async def execute_single(
        self,
        agent_id: str,
        task: AgentTask,
        scope_lock: ScopeLock,
    ) -> AgentOutput:
        """
        Execute ONE agent with governance checks
        
        MANDATORY CHECKS:
        1. Scope lock valid
        2. Token budget available
        3. Agent compatible with task
        """
        
        # Validate scope lock
        if not scope_lock.is_active:
            raise ScopeLockExpired()
        
        # Load agent
        agent = await self.registry.get(agent_id)
        
        # Inject context
        prompt = await self.context_injector.inject(
            agent.base_prompt,
            task,
            scope_lock.scope,
        )
        
        # Execute with token tracking
        start_tokens = await self.token_tracker.get_usage()
        
        response = await self.llm_dispatcher.call(
            model=agent.preferred_model,
            prompt=prompt,
            max_tokens=scope_lock.scope.token_limit,
        )
        
        end_tokens = await self.token_tracker.get_usage()
        tokens_used = end_tokens - start_tokens
        
        # Validate output against scope
        output = await self.output_parser.parse(response, task.expected_output_type)
        
        scope_valid = await self.scope_locker.validate_action(
            AgentAction(type="output", content=output),
            scope_lock
        )
        
        if not scope_valid.valid:
            raise ScopeViolation(scope_valid.reason)
        
        return AgentOutput(
            agent_id=agent_id,
            task_id=task.id,
            content=output,
            tokens_used=tokens_used,
            scope_lock_id=scope_lock.id,
        )
    
    # V54: DISABLED
    async def chain_execute(self, *args, **kwargs):
        """
        DISABLED IN V54
        
        Chain execution requires V55+ with:
        - Multi-checkpoint approval
        - Inter-agent governance
        - Rollback capabilities
        """
        raise NotImplementedError(
            "Chain execution disabled in V54. "
            "Use single agent execution with manual orchestration."
        )
```

---

## 🔴 SPRINT A3: Identity System (CRITICAL)

### A3.1 Identity Manager

```python
# backend/services/identity/identity_manager.py

class IdentityManager:
    """
    Manage user identities with STRICT separation
    
    RULES:
    - Every request MUST have identity context
    - Data isolation between identities is ABSOLUTE
    - Switch triggers full context reset
    """
    
    async def create_identity(
        self,
        user_id: str,
        identity_type: str,  # 'personal', 'enterprise', 'creative'...
        name: str,
    ) -> Identity:
        """Create new identity for user"""
        identity = Identity(
            id=uuid4(),
            user_id=user_id,
            type=identity_type,
            name=name,
            created_at=datetime.utcnow(),
            is_default=False,
        )
        await self._persist(identity)
        return identity
    
    async def switch_identity(
        self,
        user_id: str,
        target_identity_id: str,
    ) -> IdentitySwitchResult:
        """
        Switch identity with FULL reset
        
        TRIGGERS:
        1. Data reload (new identity's data only)
        2. Agent reset (release all active agents)
        3. Thread context reset (clear working memory)
        4. DataSpace reset (no DataSpace selected)
        """
        
        # Verify identity belongs to user
        identity = await self.get(target_identity_id)
        if identity.user_id != user_id:
            raise IdentityAccessDenied()
        
        # Release all agents
        await self.agent_service.release_all(user_id)
        
        # Clear thread context
        await self.thread_service.clear_context(user_id)
        
        # Reset DataSpace selection
        await self.dataspace_service.reset_selection(user_id)
        
        # Update current identity
        await self._set_current(user_id, target_identity_id)
        
        return IdentitySwitchResult(
            identity=identity,
            agents_released=True,
            context_reset=True,
            dataspace_reset=True,
        )
    
    async def get_current(self, user_id: str) -> Identity:
        """Get current active identity — ALWAYS required"""
        identity_id = await self._get_current_id(user_id)
        if not identity_id:
            raise NoIdentitySelected("User must have active identity")
        return await self.get(identity_id)
```

### A3.2 Identity Middleware

```python
# backend/middleware/identity_context.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class IdentityContextMiddleware(BaseHTTPMiddleware):
    """
    Ensure ALL requests have identity context
    
    RULE: No request processed without identity
    """
    
    EXEMPT_PATHS = ['/auth/login', '/auth/register', '/health']
    
    async def dispatch(self, request: Request, call_next):
        # Skip for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)
        
        # Extract identity from header
        identity_id = request.headers.get('X-Identity-Id')
        
        if not identity_id:
            raise HTTPException(
                status_code=400,
                detail="X-Identity-Id header required"
            )
        
        # Validate identity exists and belongs to user
        user = request.state.user
        identity = await self.identity_manager.get(identity_id)
        
        if identity.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Identity does not belong to user"
            )
        
        # Inject identity into request state
        request.state.identity = identity
        request.state.identity_id = identity_id
        
        return await call_next(request)
```

---

## 🟠 SPRINT A4: Token Economy

```python
# backend/services/tokens/token_tracker.py

class TokenTracker:
    """Track token consumption with full visibility"""
    
    async def track_usage(
        self,
        identity_id: str,
        thread_id: str,
        agent_id: str,
        input_tokens: int,
        output_tokens: int,
        model: str,
    ) -> TokenUsageRecord:
        """Record token usage for auditing"""
        cost = self._calculate_cost(input_tokens, output_tokens, model)
        
        record = TokenUsageRecord(
            id=uuid4(),
            identity_id=identity_id,
            thread_id=thread_id,
            agent_id=agent_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=cost,
            model=model,
            timestamp=datetime.utcnow(),
        )
        
        await self._persist(record)
        await self._update_budget_used(thread_id, record.total_tokens)
        
        return record
    
    async def check_budget(
        self,
        thread_id: str,
        estimated_tokens: int,
    ) -> BudgetCheckResult:
        """Check if budget allows execution"""
        budget = await self.get_thread_budget(thread_id)
        used = await self.get_thread_usage(thread_id)
        remaining = budget.limit - used.total_tokens
        
        return BudgetCheckResult(
            allowed=remaining >= estimated_tokens,
            budget_limit=budget.limit,
            used=used.total_tokens,
            remaining=remaining,
            requested=estimated_tokens,
        )
```

---

## 🟠 SPRINT A5: Assisted Workflow Engine (formerly 1-Click)

**RAPPEL**: V54 = Preview mode only. ALWAYS confirmation required.

```python
# backend/services/workflow/workflow_engine.py

class AssistedWorkflowEngine:
    """
    Assisted Workflow Engine (1-Click Preview Mode)
    
    V54 RULES:
    - NO automatic execution
    - ALWAYS preview
    - ALWAYS confirmation
    - ALWAYS governance checkpoint
    """
    
    async def interpret_command(
        self,
        command: str,
        context: UserContext,
    ) -> InterpretedIntent:
        """
        Interpret natural language command
        
        Returns structured intent for preview
        """
        pass
    
    async def construct_workflow(
        self,
        intent: InterpretedIntent,
    ) -> WorkflowPreview:
        """
        Build workflow preview for user review
        
        RULE: NEVER auto-execute
        """
        steps = await self._plan_steps(intent)
        cost = await self._estimate_total_cost(steps)
        
        return WorkflowPreview(
            intent=intent,
            steps=steps,
            estimated_cost=cost,
            requires_confirmation=True,  # ALWAYS in V54
            checkpoints=self._identify_checkpoints(steps),
        )
    
    async def execute_with_governance(
        self,
        workflow: WorkflowPreview,
        user_confirmation: UserConfirmation,
    ) -> WorkflowExecution:
        """
        Execute workflow with full governance
        
        RULE: User must have explicitly confirmed
        """
        if not user_confirmation.confirmed:
            raise WorkflowNotConfirmed()
        
        # Execute step by step with checkpoints
        results = []
        for step in workflow.steps:
            # Create checkpoint for each step
            checkpoint = await self.governance.create_checkpoint(step)
            
            # Wait for approval if required
            if step in workflow.checkpoints:
                await self._wait_for_approval(checkpoint)
            
            # Execute single agent
            result = await self.agent_runtime.execute_single(
                agent_id=step.agent_id,
                task=step.task,
                scope_lock=step.scope_lock,
            )
            results.append(result)
        
        return WorkflowExecution(
            workflow_id=workflow.id,
            results=results,
            status="completed",
        )
```

---

# PHASE 2: AGENT BETA — FRONTEND & UX

## 🔴 SPRINT B1: Identity UI (CRITICAL)

**RAPPEL**: User MUST ALWAYS see current identity.

### B1.1 Identity Selector (Always Visible)

```tsx
// frontend/src/components/identity/IdentitySelector.tsx

import React from 'react';
import { useIdentityStore } from '@/stores/identityStore';

export const IdentitySelector: React.FC = () => {
  const { currentIdentity, identities, switchIdentity, isLoading } = useIdentityStore();
  const [isOpen, setIsOpen] = useState(false);

  // RULE: Must always show current identity
  if (!currentIdentity && !isLoading) {
    return <IdentityRequired onSelect={(id) => switchIdentity(id)} />;
  }

  return (
    <div className="identity-selector">
      {/* Current Identity Badge — ALWAYS VISIBLE */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="identity-badge"
        style={{ borderColor: currentIdentity?.color }}
        aria-label="Switch identity"
      >
        <span className="identity-icon">{getIdentityIcon(currentIdentity?.type)}</span>
        <span className="identity-name">{currentIdentity?.name}</span>
        <ChevronDown className={isOpen ? 'rotate-180' : ''} />
      </button>

      {/* Switch Warning Modal */}
      {isOpen && (
        <IdentitySwitchModal
          currentIdentity={currentIdentity}
          identities={identities}
          onSwitch={async (id) => {
            // WARN: Switching resets context
            const confirmed = await confirmSwitch();
            if (confirmed) {
              await switchIdentity(id);
              setIsOpen(false);
            }
          }}
          onClose={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

// CRITICAL: Show when no identity selected
const IdentityRequired: React.FC<{ onSelect: (id: string) => void }> = ({ onSelect }) => (
  <div className="identity-required-overlay">
    <div className="identity-required-modal">
      <h2>Sélectionnez une identité</h2>
      <p>Une identité est requise pour continuer</p>
      <IdentityList onSelect={onSelect} />
    </div>
  </div>
);
```

### B1.2 Identity Store

```tsx
// frontend/src/stores/identityStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface IdentityState {
  currentIdentity: Identity | null;
  identities: Identity[];
  isLoading: boolean;
  
  fetchIdentities: () => Promise<void>;
  switchIdentity: (identityId: string) => Promise<void>;
  createIdentity: (data: CreateIdentityInput) => Promise<Identity>;
}

export const useIdentityStore = create<IdentityState>()(
  persist(
    (set, get) => ({
      currentIdentity: null,
      identities: [],
      isLoading: false,

      switchIdentity: async (identityId: string) => {
        set({ isLoading: true });
        
        try {
          // Call backend switch (triggers full reset)
          await identityApi.switch(identityId);
          
          const identity = get().identities.find(i => i.id === identityId);
          set({ currentIdentity: identity });
          
          // CRITICAL: Trigger full data reload
          // This resets agents, threads, dataspaces
          window.dispatchEvent(new CustomEvent('identity-switched', {
            detail: { identityId }
          }));
          
          // Reset other stores
          useAgentStore.getState().reset();
          useThreadStore.getState().reset();
          useDataSpaceStore.getState().reset();
          
        } finally {
          set({ isLoading: false });
        }
      },
    }),
    { name: 'chenu-identity' }
  )
);
```

---

## 🔴 SPRINT B2: Agent Marketplace

```tsx
// frontend/src/components/agents/AgentCatalog.tsx

export const AgentCatalog: React.FC = () => {
  const { agents, loading } = useAgentCatalog();
  const { currentIdentity } = useIdentityStore();

  // RULE: Can't browse agents without identity
  if (!currentIdentity) {
    return <IdentityRequiredMessage />;
  }

  return (
    <div className="agent-catalog">
      <header className="catalog-header">
        <h2>Agent Marketplace</h2>
        <p>168+ agents disponibles pour {currentIdentity.name}</p>
      </header>
      
      <AgentFilters />
      
      <div className="agent-grid">
        {agents.map(agent => (
          <AgentCard 
            key={agent.id}
            agent={agent}
            onHire={() => openHireFlow(agent)}
          />
        ))}
      </div>
    </div>
  );
};
```

---

## 🔴 SPRINT B3: Governance UI

```tsx
// frontend/src/components/governance/GovernanceDashboard.tsx

export const GovernanceDashboard: React.FC = () => {
  const { pendingCheckpoints, approveCheckpoint, rejectCheckpoint } = useGovernance();

  return (
    <div className="governance-dashboard">
      <header>
        <h2>Gouvernance</h2>
        <Badge variant="warning">
          {pendingCheckpoints.length} en attente
        </Badge>
      </header>

      {pendingCheckpoints.length === 0 ? (
        <EmptyState 
          icon="✅"
          title="Aucune approbation en attente"
          description="Vos agents sont en attente de vos instructions"
        />
      ) : (
        <div className="checkpoints-list">
          {pendingCheckpoints.map(checkpoint => (
            <CheckpointCard
              key={checkpoint.id}
              checkpoint={checkpoint}
              onApprove={() => approveCheckpoint(checkpoint.id)}
              onReject={() => rejectCheckpoint(checkpoint.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## 🔴 SPRINT B4: Token Economy UI

```tsx
// frontend/src/components/tokens/TokenBalance.tsx

export const TokenBalance: React.FC = () => {
  const { balance, usage } = useTokenStore();
  const { currentIdentity } = useIdentityStore();

  const percentage = (usage.used / balance.limit) * 100;
  const statusColor = 
    percentage > 90 ? 'red' :
    percentage > 70 ? 'amber' :
    'green';

  return (
    <div className="token-balance">
      <div className="balance-display">
        <TokenIcon />
        <span className="balance-amount">
          {formatNumber(balance.available)}
        </span>
        <span className="balance-label">tokens</span>
      </div>

      <div className="usage-bar">
        <div 
          className={`usage-fill bg-${statusColor}`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {percentage > 80 && (
        <Alert variant="warning">
          Budget presque épuisé ({Math.round(100 - percentage)}% restant)
        </Alert>
      )}
    </div>
  );
};
```

---

## 🟠 SPRINT B5: Assisted Workflow Command Bar

**RAPPEL**: ALWAYS preview, ALWAYS confirmation.

```tsx
// frontend/src/components/workflow/AssistedWorkflowBar.tsx

export const AssistedWorkflowBar: React.FC = () => {
  const [command, setCommand] = useState('');
  const [preview, setPreview] = useState<WorkflowPreview | null>(null);
  const [isConfirming, setIsConfirming] = useState(false);

  const handleSubmit = async () => {
    // Step 1: Interpret (never execute directly)
    const interpreted = await workflowApi.interpret(command);
    
    // Step 2: Show preview (ALWAYS)
    const workflowPreview = await workflowApi.constructWorkflow(interpreted);
    setPreview(workflowPreview);
  };

  const handleConfirm = async () => {
    setIsConfirming(true);
    
    // RULE: Explicit confirmation required
    await workflowApi.executeWithGovernance(preview!.id, {
      confirmed: true,
      confirmedBy: currentUser.id,
      confirmedAt: new Date(),
    });
    
    setPreview(null);
    setCommand('');
    setIsConfirming(false);
  };

  return (
    <>
      <CommandInput
        value={command}
        onChange={setCommand}
        onSubmit={handleSubmit}
        placeholder="Que voulez-vous faire? (Prévisualisation avant exécution)"
      />

      {/* ALWAYS show preview before execution */}
      {preview && (
        <WorkflowPreviewModal
          preview={preview}
          onConfirm={handleConfirm}
          onCancel={() => setPreview(null)}
          isLoading={isConfirming}
        />
      )}
    </>
  );
};
```

---

## 🟠 SPRINT B6: DataSpace UI (Explicit Context)

**RAPPEL**: Every action belongs to exactly ONE DataSpace.

```tsx
// frontend/src/components/dataspace/DataSpaceIndicator.tsx

export const DataSpaceIndicator: React.FC = () => {
  const { currentDataSpace, selectDataSpace } = useDataSpaceStore();
  const [showSelector, setShowSelector] = useState(false);

  // RULE: Must show when no DataSpace selected
  if (!currentDataSpace) {
    return (
      <DataSpaceRequired 
        onSelect={(ds) => {
          selectDataSpace(ds.id);
          setShowSelector(false);
        }}
      />
    );
  }

  return (
    <div className="dataspace-indicator">
      <div 
        className="dataspace-badge"
        onClick={() => setShowSelector(true)}
      >
        <FolderIcon />
        <span className="dataspace-name">{currentDataSpace.name}</span>
        <span className="dataspace-type">{currentDataSpace.type}</span>
      </div>
    </div>
  );
};

// RULE: Force selection when none active
const DataSpaceRequired: React.FC<{ onSelect: (ds: DataSpace) => void }> = ({ onSelect }) => (
  <div className="dataspace-required">
    <AlertTriangle className="text-amber-500" />
    <span>Sélectionnez un DataSpace</span>
    <button onClick={() => openDataSpaceSelector(onSelect)}>
      Choisir
    </button>
  </div>
);
```

---

## 🟠 SPRINT B7: XR Mode Toggle (Rendering Layer Only)

**RAPPEL**: XR = Mode, not Space. Never creates data.

```tsx
// frontend/src/components/xr/XRModeToggle.tsx

export const XRModeToggle: React.FC = () => {
  const { isXRSupported, isXRActive, toggleXR, xrCapabilities } = useXRStore();
  
  // Don't show if device doesn't support XR
  if (!isXRSupported) {
    return null;
  }

  return (
    <button 
      className={`xr-toggle ${isXRActive ? 'active' : ''}`}
      onClick={toggleXR}
      title={isXRActive ? 'Quitter le mode XR' : 'Activer le mode XR'}
      aria-pressed={isXRActive}
    >
      <VRIcon />
      <span className="sr-only">
        {isXRActive ? 'Mode XR actif' : 'Activer mode XR'}
      </span>
      {isXRActive && <span className="xr-active-indicator" />}
    </button>
  );
};

// XR Store
export const useXRStore = create<XRState>((set) => ({
  isXRActive: false,
  isXRSupported: false,
  
  toggleXR: () => {
    set(state => {
      // XR only visualizes, never modifies data
      // Switching XR mode doesn't affect any state
      return { isXRActive: !state.isXRActive };
    });
  },
  
  checkSupport: async () => {
    const supported = await navigator.xr?.isSessionSupported('immersive-vr');
    set({ isXRSupported: !!supported });
  },
}));
```

---

# 📊 RÉPARTITION FINALE

## AGENT ALPHA — 58 fichiers backend
| Sprint | Focus | Fichiers |
|--------|-------|----------|
| A1 | Governance Pipeline | 16 |
| A2 | Agent Execution (Single) | 12 |
| A3 | Identity System | 8 |
| A4 | Token Economy | 6 |
| A5 | Assisted Workflow | 10 |
| A6 | Meeting Intelligence | 6 |

## AGENT BETA — 64 fichiers frontend
| Sprint | Focus | Fichiers |
|--------|-------|----------|
| B1 | Identity UI | 10 |
| B2 | Agent Marketplace | 12 |
| B3 | Governance UI | 10 |
| B4 | Token Economy UI | 8 |
| B5 | Assisted Workflow Bar | 8 |
| B6 | DataSpace UI | 6 |
| B7 | XR Mode Toggle | 6 |
| B8 | Meeting UI | 4 |

---

# ✅ CRITÈRES DE SUCCÈS V54

| Critère | Validation |
|---------|------------|
| 9 Spheres | Structure verrouillée, pas de dérive |
| XR as Mode | Jamais une sphère, visualisation only |
| Encoding v0.1 | Deterministic, versioned |
| Single Agent | NO chain execution |
| Identity Always Visible | UI + API enforcement |
| Assisted Workflow | ALWAYS preview, ALWAYS confirm |
| DataSpace Explicit | Force selection, no implicit |

---

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║                         V54 PLAN — VERROUILLÉ ET CORRIGÉ                                    ║
║                         7 corrections critiques intégrées                                    ║
║                         Prêt pour implémentation                                             ║
║                                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```
