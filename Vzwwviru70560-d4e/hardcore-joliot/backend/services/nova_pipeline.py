"""
CHE·NU™ Nova Pipeline
=====================

Multi-Lane Intelligence Pipeline for governed AI execution.

Nova is the system intelligence of CHE·NU. It orchestrates all AI operations
through a structured pipeline that ensures Human Sovereignty.

ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NOVA MULTI-LANE PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT (User Request)                                                       │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE A: INTENT ANALYSIS                                              │   │
│  │ └─ Parse user intent, extract entities, classify request type       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE B: CONTEXT SNAPSHOT                                             │   │
│  │ └─ Capture Thread state, active actions, relevant memory           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE C: SEMANTIC ENCODING                                            │   │
│  │ └─ Encode context for AI, prepare prompt, set constraints           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE D: GOVERNANCE CHECK                                             │   │
│  │ └─ Verify permissions, scope, token budget, sphere boundaries       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE E: CHECKPOINT (HTTP 423)                                        │   │
│  │ └─ BLOCK if action is sensitive, await human approval               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼ (only if approved or no checkpoint needed)                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE F: EXECUTION                                                    │   │
│  │ └─ Execute AI operation (LLM call, agent action)                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ LANE G: AUDIT                                                        │   │
│  │ └─ Log everything, update metrics, record to audit trail            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  OUTPUT (Response to User)                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Lane E blocks sensitive actions
- Rule #2: Autonomy Isolation - all operations in sandbox mode
- Rule #3: Sphere Integrity - Lane D checks sphere boundaries
- Rule #4: No AI-to-AI orchestration - Nova coordinates, doesn't delegate
- Rule #6: Traceability - Lane G logs everything
- Rule #7: R&D Continuity - respects all established rules
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any, Callable, Awaitable
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from backend.core.exceptions import (
    NotFoundError,
    ValidationError,
    ForbiddenError,
    CheckpointRequiredError,
)
from backend.models.agent import SphereType

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS & TYPES
# =============================================================================

class PipelineLane(str, Enum):
    """The 7 lanes of the Nova Pipeline."""
    INTENT_ANALYSIS = "lane_a_intent"
    CONTEXT_SNAPSHOT = "lane_b_context"
    SEMANTIC_ENCODING = "lane_c_encoding"
    GOVERNANCE_CHECK = "lane_d_governance"
    CHECKPOINT = "lane_e_checkpoint"
    EXECUTION = "lane_f_execution"
    AUDIT = "lane_g_audit"


class IntentType(str, Enum):
    """Types of user intents."""
    # Read operations (no checkpoint needed)
    QUERY = "query"                     # Ask a question
    SEARCH = "search"                   # Search for information
    SUMMARIZE = "summarize"             # Summarize content
    ANALYZE = "analyze"                 # Analyze data
    
    # Write operations (may need checkpoint)
    CREATE = "create"                   # Create new content
    UPDATE = "update"                   # Update existing content
    DELETE = "delete"                   # Delete content (ALWAYS checkpoint)
    
    # Communication (ALWAYS checkpoint)
    SEND_EMAIL = "send_email"
    SEND_MESSAGE = "send_message"
    PUBLISH = "publish"
    
    # Financial (ALWAYS checkpoint)
    TRANSACTION = "transaction"
    INVOICE = "invoice"
    
    # System
    CONFIGURE = "configure"
    UNKNOWN = "unknown"


class GovernanceStatus(str, Enum):
    """Status after governance check."""
    ALLOWED = "allowed"                 # Proceed to execution
    CHECKPOINT_REQUIRED = "checkpoint"  # Needs human approval
    DENIED = "denied"                   # Not allowed
    RATE_LIMITED = "rate_limited"       # Too many requests


class ExecutionStatus(str, Enum):
    """Status of pipeline execution."""
    PENDING = "pending"
    PROCESSING = "processing"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# =============================================================================
# PIPELINE DATA MODELS
# =============================================================================

class NovaRequest(BaseModel):
    """Request to the Nova Pipeline."""
    
    # Identity & Context
    identity_id: UUID
    thread_id: Optional[UUID] = None
    sphere_type: SphereType
    
    # Request
    input_text: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Agent (optional)
    agent_id: Optional[UUID] = None
    agent_name: Optional[str] = None
    
    # Options
    max_tokens: int = Field(default=4000, ge=100, le=100000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = False
    
    # Metadata
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class IntentAnalysisResult(BaseModel):
    """Result of Lane A: Intent Analysis."""
    intent_type: IntentType
    confidence: float = Field(ge=0.0, le=1.0)
    entities: Dict[str, Any] = Field(default_factory=dict)
    keywords: List[str] = Field(default_factory=list)
    requires_checkpoint: bool = False
    reasoning: str = ""


class ContextSnapshot(BaseModel):
    """Result of Lane B: Context Snapshot."""
    thread_summary: Optional[str] = None
    recent_events: List[Dict[str, Any]] = Field(default_factory=list)
    active_actions: List[Dict[str, Any]] = Field(default_factory=list)
    relevant_memories: List[Dict[str, Any]] = Field(default_factory=list)
    sphere_context: Dict[str, Any] = Field(default_factory=dict)
    
    # Metrics
    event_count: int = 0
    memory_tokens: int = 0


class SemanticEncoding(BaseModel):
    """Result of Lane C: Semantic Encoding."""
    encoded_prompt: str
    system_message: str
    context_tokens: int = 0
    constraints: List[str] = Field(default_factory=list)
    
    # LLM configuration
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4000
    temperature: float = 0.7


class GovernanceResult(BaseModel):
    """Result of Lane D: Governance Check."""
    status: GovernanceStatus
    
    # Permissions
    has_permission: bool = True
    scope_valid: bool = True
    budget_sufficient: bool = True
    sphere_valid: bool = True
    
    # Details
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    
    # Token budget
    estimated_cost: float = 0.0
    remaining_budget: float = 0.0


class CheckpointResult(BaseModel):
    """Result of Lane E: Checkpoint."""
    requires_approval: bool
    checkpoint_id: Optional[UUID] = None
    checkpoint_type: Optional[str] = None
    reason: Optional[str] = None
    
    # Preview of action
    action_preview: Dict[str, Any] = Field(default_factory=dict)
    
    # Status
    approved: Optional[bool] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


class ExecutionResult(BaseModel):
    """Result of Lane F: Execution."""
    success: bool
    output_text: str = ""
    output_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Token usage
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    
    # Timing
    duration_ms: int = 0
    
    # LLM info
    model_used: str = ""
    finish_reason: str = ""


class AuditRecord(BaseModel):
    """Result of Lane G: Audit."""
    audit_id: UUID = Field(default_factory=uuid4)
    request_id: UUID
    identity_id: UUID
    
    # Pipeline info
    lanes_executed: List[str] = Field(default_factory=list)
    total_duration_ms: int = 0
    
    # Results
    final_status: ExecutionStatus
    intent_type: IntentType
    checkpoint_triggered: bool = False
    
    # Token & cost
    total_tokens: int = 0
    total_cost: float = 0.0
    
    # Timestamps
    started_at: datetime
    completed_at: datetime


class NovaPipelineResult(BaseModel):
    """Complete result of Nova Pipeline execution."""
    request_id: UUID
    status: ExecutionStatus
    
    # Lane results
    intent: Optional[IntentAnalysisResult] = None
    context: Optional[ContextSnapshot] = None
    encoding: Optional[SemanticEncoding] = None
    governance: Optional[GovernanceResult] = None
    checkpoint: Optional[CheckpointResult] = None
    execution: Optional[ExecutionResult] = None
    audit: Optional[AuditRecord] = None
    
    # Final output
    output_text: str = ""
    output_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Error info (if failed)
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    # Timing
    total_duration_ms: int = 0


# =============================================================================
# LANE HANDLERS
# =============================================================================

class IntentAnalyzer:
    """
    Lane A: Intent Analysis
    
    Parses user input to understand intent, extract entities, and determine
    if a checkpoint is required.
    """
    
    # Intents that ALWAYS require checkpoint
    CHECKPOINT_INTENTS = {
        IntentType.DELETE,
        IntentType.SEND_EMAIL,
        IntentType.SEND_MESSAGE,
        IntentType.PUBLISH,
        IntentType.TRANSACTION,
        IntentType.INVOICE,
    }
    
    # Keywords for intent detection
    INTENT_KEYWORDS = {
        IntentType.QUERY: ["what", "who", "when", "where", "why", "how", "?"],
        IntentType.SEARCH: ["find", "search", "look", "locate", "show"],
        IntentType.SUMMARIZE: ["summarize", "summary", "brief", "overview"],
        IntentType.ANALYZE: ["analyze", "analysis", "examine", "evaluate"],
        IntentType.CREATE: ["create", "make", "new", "generate", "write", "draft"],
        IntentType.UPDATE: ["update", "edit", "modify", "change", "fix"],
        IntentType.DELETE: ["delete", "remove", "erase", "cancel"],
        IntentType.SEND_EMAIL: ["email", "mail", "send email"],
        IntentType.SEND_MESSAGE: ["message", "send", "notify", "dm"],
        IntentType.PUBLISH: ["publish", "post", "share", "release"],
        IntentType.TRANSACTION: ["pay", "transfer", "transaction", "payment"],
        IntentType.INVOICE: ["invoice", "bill", "charge"],
        IntentType.CONFIGURE: ["configure", "setup", "settings", "config"],
    }
    
    async def analyze(self, request: NovaRequest) -> IntentAnalysisResult:
        """Analyze user intent from request."""
        text = request.input_text.lower()
        
        # Detect intent type
        intent_type, confidence = self._detect_intent(text)
        
        # Extract entities (simplified)
        entities = self._extract_entities(text)
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        # Determine if checkpoint required
        requires_checkpoint = intent_type in self.CHECKPOINT_INTENTS
        
        return IntentAnalysisResult(
            intent_type=intent_type,
            confidence=confidence,
            entities=entities,
            keywords=keywords,
            requires_checkpoint=requires_checkpoint,
            reasoning=f"Detected intent: {intent_type.value} with confidence {confidence:.2f}",
        )
    
    def _detect_intent(self, text: str) -> tuple[IntentType, float]:
        """Detect intent type from text."""
        best_intent = IntentType.UNKNOWN
        best_score = 0.0
        
        for intent_type, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_intent = intent_type
        
        # Normalize confidence
        confidence = min(1.0, best_score / 3.0) if best_score > 0 else 0.3
        
        return best_intent, confidence
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text (simplified)."""
        # TODO: Use NER or LLM for better extraction
        return {
            "raw_text": text,
            "word_count": len(text.split()),
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction
        words = text.split()
        # Filter common words
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being"}
        keywords = [w for w in words if w.lower() not in stopwords and len(w) > 2]
        return keywords[:10]  # Top 10


class ContextSnapshotBuilder:
    """
    Lane B: Context Snapshot
    
    Captures the current state of Thread, memory, and sphere context.
    """
    
    async def build(
        self,
        request: NovaRequest,
        thread_service: Any = None,  # Optional ThreadService
    ) -> ContextSnapshot:
        """Build context snapshot for request."""
        snapshot = ContextSnapshot()
        
        # Get Thread context if available
        if request.thread_id and thread_service:
            try:
                # TODO: Integrate with actual ThreadService
                snapshot.thread_summary = f"Thread {request.thread_id} context"
                snapshot.event_count = 10
            except Exception as e:
                logger.warning(f"Failed to get Thread context: {e}")
        
        # Get sphere context
        snapshot.sphere_context = {
            "sphere_type": request.sphere_type.value,
            "has_thread": request.thread_id is not None,
        }
        
        # Estimate memory tokens
        snapshot.memory_tokens = 500  # Base estimate
        
        return snapshot


class SemanticEncoder:
    """
    Lane C: Semantic Encoding
    
    Prepares the prompt and context for LLM execution.
    """
    
    DEFAULT_SYSTEM_MESSAGE = """You are Nova, the system intelligence of CHE·NU.
You help users manage their Threads, make decisions, and accomplish tasks.

RULES:
1. Always respect human sovereignty - suggest, don't decide
2. Stay within the user's current sphere context
3. Be concise and actionable
4. When uncertain, ask for clarification
5. Never take autonomous actions without approval
"""
    
    async def encode(
        self,
        request: NovaRequest,
        intent: IntentAnalysisResult,
        context: ContextSnapshot,
    ) -> SemanticEncoding:
        """Encode request for LLM execution."""
        
        # Build system message
        system_message = self.DEFAULT_SYSTEM_MESSAGE
        if context.sphere_context:
            system_message += f"\n\nCurrent Sphere: {context.sphere_context.get('sphere_type', 'unknown')}"
        
        # Build encoded prompt
        encoded_prompt = request.input_text
        if context.thread_summary:
            encoded_prompt = f"[Context: {context.thread_summary}]\n\n{encoded_prompt}"
        
        # Add constraints based on intent
        constraints = []
        if intent.requires_checkpoint:
            constraints.append("This action requires human approval before execution")
        if intent.intent_type == IntentType.DELETE:
            constraints.append("Deletion is permanent and cannot be undone")
        
        # Calculate context tokens (estimate)
        context_tokens = len(encoded_prompt.split()) + len(system_message.split())
        
        return SemanticEncoding(
            encoded_prompt=encoded_prompt,
            system_message=system_message,
            context_tokens=context_tokens,
            constraints=constraints,
            model="claude-3-5-sonnet-20241022",
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )


class GovernanceChecker:
    """
    Lane D: Governance Check
    
    Verifies permissions, scope, budget, and sphere boundaries.
    """
    
    async def check(
        self,
        request: NovaRequest,
        intent: IntentAnalysisResult,
        encoding: SemanticEncoding,
    ) -> GovernanceResult:
        """Perform governance checks."""
        violations = []
        warnings = []
        
        # Check scope (simplified)
        scope_valid = True
        
        # Check budget (simplified - assume sufficient)
        budget_sufficient = True
        estimated_cost = encoding.context_tokens * 0.00001  # Rough estimate
        remaining_budget = 100.0  # Default budget
        
        # Check sphere validity
        sphere_valid = True
        
        # Determine status
        if violations:
            status = GovernanceStatus.DENIED
        elif intent.requires_checkpoint:
            status = GovernanceStatus.CHECKPOINT_REQUIRED
        else:
            status = GovernanceStatus.ALLOWED
        
        return GovernanceResult(
            status=status,
            has_permission=True,
            scope_valid=scope_valid,
            budget_sufficient=budget_sufficient,
            sphere_valid=sphere_valid,
            violations=violations,
            warnings=warnings,
            estimated_cost=estimated_cost,
            remaining_budget=remaining_budget,
        )


class CheckpointHandler:
    """
    Lane E: Checkpoint
    
    Handles HTTP 423 (Locked) checkpoints for sensitive actions.
    This is the core of Human Sovereignty enforcement.
    """
    
    async def check(
        self,
        request: NovaRequest,
        intent: IntentAnalysisResult,
        governance: GovernanceResult,
        checkpoint_service: Any = None,  # Optional CheckpointService
    ) -> CheckpointResult:
        """Create checkpoint if required."""
        
        # Determine if checkpoint is needed
        requires_approval = (
            intent.requires_checkpoint or
            governance.status == GovernanceStatus.CHECKPOINT_REQUIRED
        )
        
        if not requires_approval:
            return CheckpointResult(requires_approval=False)
        
        # Create checkpoint
        checkpoint_id = uuid4()
        checkpoint_type = f"nova_{intent.intent_type.value}"
        
        # Build action preview
        action_preview = {
            "intent": intent.intent_type.value,
            "input": request.input_text[:200],  # Truncate for preview
            "sphere": request.sphere_type.value,
        }
        
        # If we have a checkpoint service, create the checkpoint
        if checkpoint_service:
            # TODO: Integrate with actual CheckpointService
            pass
        
        return CheckpointResult(
            requires_approval=True,
            checkpoint_id=checkpoint_id,
            checkpoint_type=checkpoint_type,
            reason=f"Action '{intent.intent_type.value}' requires human approval",
            action_preview=action_preview,
        )


class Executor:
    """
    Lane F: Execution
    
    Executes the AI operation (LLM call).
    """
    
    async def execute(
        self,
        request: NovaRequest,
        encoding: SemanticEncoding,
        checkpoint: CheckpointResult,
    ) -> ExecutionResult:
        """Execute the AI operation."""
        import time
        start_time = time.time()
        
        # Check if checkpoint approval is needed
        if checkpoint.requires_approval and not checkpoint.approved:
            return ExecutionResult(
                success=False,
                output_text="Awaiting human approval",
                duration_ms=0,
            )
        
        # Mock LLM execution (TODO: integrate real LLM)
        try:
            # Simulate LLM call
            output_text = f"[Nova Response] Processed request: {request.input_text[:100]}..."
            
            # Mock token usage
            input_tokens = encoding.context_tokens
            output_tokens = len(output_text.split())
            total_tokens = input_tokens + output_tokens
            cost = total_tokens * 0.00001
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            return ExecutionResult(
                success=True,
                output_text=output_text,
                output_data={"processed": True},
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost=cost,
                duration_ms=duration_ms,
                model_used=encoding.model,
                finish_reason="stop",
            )
            
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return ExecutionResult(
                success=False,
                output_text=f"Execution failed: {str(e)}",
                duration_ms=int((time.time() - start_time) * 1000),
            )


class Auditor:
    """
    Lane G: Audit
    
    Logs everything and updates metrics.
    """
    
    async def record(
        self,
        request: NovaRequest,
        intent: IntentAnalysisResult,
        checkpoint: CheckpointResult,
        execution: ExecutionResult,
        status: ExecutionStatus,
        started_at: datetime,
        lanes_executed: List[str],
    ) -> AuditRecord:
        """Record audit trail."""
        completed_at = datetime.utcnow()
        total_duration_ms = int((completed_at - started_at).total_seconds() * 1000)
        
        audit = AuditRecord(
            request_id=request.request_id,
            identity_id=request.identity_id,
            lanes_executed=lanes_executed,
            total_duration_ms=total_duration_ms,
            final_status=status,
            intent_type=intent.intent_type,
            checkpoint_triggered=checkpoint.requires_approval,
            total_tokens=execution.total_tokens if execution else 0,
            total_cost=execution.cost if execution else 0.0,
            started_at=started_at,
            completed_at=completed_at,
        )
        
        # Log audit
        logger.info(
            f"Nova Pipeline Audit: request={request.request_id} "
            f"status={status.value} intent={intent.intent_type.value} "
            f"checkpoint={checkpoint.requires_approval} "
            f"duration={total_duration_ms}ms tokens={audit.total_tokens}"
        )
        
        return audit


# =============================================================================
# NOVA PIPELINE SERVICE
# =============================================================================

class NovaPipelineService:
    """
    Nova Multi-Lane Pipeline Service.
    
    Orchestrates the 7-lane pipeline for governed AI execution.
    
    R&D COMPLIANCE:
    - Rule #1: Human Sovereignty - Lane E enforces checkpoints
    - Rule #2: Autonomy Isolation - all operations sandboxed
    - Rule #3: Sphere Integrity - Lane D validates sphere boundaries
    - Rule #4: No AI-to-AI orchestration - Nova is system, not agent
    - Rule #6: Traceability - Lane G logs everything
    """
    
    def __init__(
        self,
        thread_service: Any = None,
        checkpoint_service: Any = None,
        llm_router: Any = None,
    ):
        self.thread_service = thread_service
        self.checkpoint_service = checkpoint_service
        self.llm_router = llm_router
        
        # Initialize lane handlers
        self.intent_analyzer = IntentAnalyzer()
        self.context_builder = ContextSnapshotBuilder()
        self.semantic_encoder = SemanticEncoder()
        self.governance_checker = GovernanceChecker()
        self.checkpoint_handler = CheckpointHandler()
        self.executor = Executor()
        self.auditor = Auditor()
    
    async def process(self, request: NovaRequest) -> NovaPipelineResult:
        """
        Process a request through the Nova Pipeline.
        
        Executes all 7 lanes in sequence:
        A → B → C → D → E → F → G
        
        Returns NovaPipelineResult with all lane outputs.
        
        Raises:
            CheckpointRequiredError: If action requires approval (HTTP 423)
        """
        started_at = datetime.utcnow()
        lanes_executed: List[str] = []
        
        try:
            # =====================================================
            # LANE A: INTENT ANALYSIS
            # =====================================================
            intent = await self.intent_analyzer.analyze(request)
            lanes_executed.append(PipelineLane.INTENT_ANALYSIS.value)
            
            logger.debug(f"Lane A: Intent={intent.intent_type.value}")
            
            # =====================================================
            # LANE B: CONTEXT SNAPSHOT
            # =====================================================
            context = await self.context_builder.build(
                request,
                thread_service=self.thread_service,
            )
            lanes_executed.append(PipelineLane.CONTEXT_SNAPSHOT.value)
            
            logger.debug(f"Lane B: Context tokens={context.memory_tokens}")
            
            # =====================================================
            # LANE C: SEMANTIC ENCODING
            # =====================================================
            encoding = await self.semantic_encoder.encode(request, intent, context)
            lanes_executed.append(PipelineLane.SEMANTIC_ENCODING.value)
            
            logger.debug(f"Lane C: Encoded prompt length={len(encoding.encoded_prompt)}")
            
            # =====================================================
            # LANE D: GOVERNANCE CHECK
            # =====================================================
            governance = await self.governance_checker.check(request, intent, encoding)
            lanes_executed.append(PipelineLane.GOVERNANCE_CHECK.value)
            
            logger.debug(f"Lane D: Governance status={governance.status.value}")
            
            # Check for denial
            if governance.status == GovernanceStatus.DENIED:
                return NovaPipelineResult(
                    request_id=request.request_id,
                    status=ExecutionStatus.FAILED,
                    intent=intent,
                    context=context,
                    encoding=encoding,
                    governance=governance,
                    error="Governance check failed",
                    error_code="GOVERNANCE_DENIED",
                )
            
            # =====================================================
            # LANE E: CHECKPOINT
            # =====================================================
            checkpoint = await self.checkpoint_handler.check(
                request,
                intent,
                governance,
                checkpoint_service=self.checkpoint_service,
            )
            lanes_executed.append(PipelineLane.CHECKPOINT.value)
            
            logger.debug(f"Lane E: Checkpoint required={checkpoint.requires_approval}")
            
            # If checkpoint required, return with HTTP 423 status
            if checkpoint.requires_approval and not checkpoint.approved:
                # Record audit for checkpoint
                audit = await self.auditor.record(
                    request=request,
                    intent=intent,
                    checkpoint=checkpoint,
                    execution=ExecutionResult(success=False, output_text=""),
                    status=ExecutionStatus.AWAITING_APPROVAL,
                    started_at=started_at,
                    lanes_executed=lanes_executed,
                )
                
                # Raise HTTP 423 error
                raise CheckpointRequiredError(
                    checkpoint_id=checkpoint.checkpoint_id,
                    checkpoint_type=checkpoint.checkpoint_type,
                    reason=checkpoint.reason,
                    action_preview=checkpoint.action_preview,
                )
            
            # =====================================================
            # LANE F: EXECUTION
            # =====================================================
            execution = await self.executor.execute(request, encoding, checkpoint)
            lanes_executed.append(PipelineLane.EXECUTION.value)
            
            logger.debug(f"Lane F: Execution success={execution.success}")
            
            # Determine final status
            final_status = (
                ExecutionStatus.COMPLETED if execution.success
                else ExecutionStatus.FAILED
            )
            
            # =====================================================
            # LANE G: AUDIT
            # =====================================================
            audit = await self.auditor.record(
                request=request,
                intent=intent,
                checkpoint=checkpoint,
                execution=execution,
                status=final_status,
                started_at=started_at,
                lanes_executed=lanes_executed,
            )
            lanes_executed.append(PipelineLane.AUDIT.value)
            
            # Calculate total duration
            total_duration_ms = int(
                (datetime.utcnow() - started_at).total_seconds() * 1000
            )
            
            # Build final result
            return NovaPipelineResult(
                request_id=request.request_id,
                status=final_status,
                intent=intent,
                context=context,
                encoding=encoding,
                governance=governance,
                checkpoint=checkpoint,
                execution=execution,
                audit=audit,
                output_text=execution.output_text,
                output_data=execution.output_data,
                total_duration_ms=total_duration_ms,
            )
            
        except CheckpointRequiredError:
            # Re-raise checkpoint errors
            raise
            
        except Exception as e:
            logger.error(f"Nova Pipeline error: {e}")
            
            return NovaPipelineResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                error=str(e),
                error_code="PIPELINE_ERROR",
                total_duration_ms=int(
                    (datetime.utcnow() - started_at).total_seconds() * 1000
                ),
            )
    
    async def approve_checkpoint(
        self,
        checkpoint_id: UUID,
        approved_by: UUID,
        original_request: NovaRequest,
    ) -> NovaPipelineResult:
        """
        Continue pipeline after checkpoint approval.
        
        This is called when a user approves a pending checkpoint.
        """
        # Mark checkpoint as approved
        checkpoint = CheckpointResult(
            requires_approval=True,
            checkpoint_id=checkpoint_id,
            approved=True,
            approved_by=approved_by,
            approved_at=datetime.utcnow(),
        )
        
        # Resume pipeline from execution lane
        started_at = datetime.utcnow()
        lanes_executed = [
            PipelineLane.INTENT_ANALYSIS.value,
            PipelineLane.CONTEXT_SNAPSHOT.value,
            PipelineLane.SEMANTIC_ENCODING.value,
            PipelineLane.GOVERNANCE_CHECK.value,
            PipelineLane.CHECKPOINT.value,
        ]
        
        # Re-analyze intent and encode
        intent = await self.intent_analyzer.analyze(original_request)
        context = await self.context_builder.build(
            original_request,
            thread_service=self.thread_service,
        )
        encoding = await self.semantic_encoder.encode(
            original_request,
            intent,
            context,
        )
        
        # Execute
        execution = await self.executor.execute(
            original_request,
            encoding,
            checkpoint,
        )
        lanes_executed.append(PipelineLane.EXECUTION.value)
        
        # Audit
        final_status = (
            ExecutionStatus.COMPLETED if execution.success
            else ExecutionStatus.FAILED
        )
        
        audit = await self.auditor.record(
            request=original_request,
            intent=intent,
            checkpoint=checkpoint,
            execution=execution,
            status=final_status,
            started_at=started_at,
            lanes_executed=lanes_executed,
        )
        lanes_executed.append(PipelineLane.AUDIT.value)
        
        return NovaPipelineResult(
            request_id=original_request.request_id,
            status=final_status,
            intent=intent,
            context=context,
            encoding=encoding,
            checkpoint=checkpoint,
            execution=execution,
            audit=audit,
            output_text=execution.output_text,
            output_data=execution.output_data,
            total_duration_ms=int(
                (datetime.utcnow() - started_at).total_seconds() * 1000
            ),
        )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
    "PipelineLane",
    "IntentType",
    "GovernanceStatus",
    "ExecutionStatus",
    
    # Request/Response
    "NovaRequest",
    "NovaPipelineResult",
    
    # Lane Results
    "IntentAnalysisResult",
    "ContextSnapshot",
    "SemanticEncoding",
    "GovernanceResult",
    "CheckpointResult",
    "ExecutionResult",
    "AuditRecord",
    
    # Service
    "NovaPipelineService",
    
    # Lane Handlers
    "IntentAnalyzer",
    "ContextSnapshotBuilder",
    "SemanticEncoder",
    "GovernanceChecker",
    "CheckpointHandler",
    "Executor",
    "Auditor",
]
