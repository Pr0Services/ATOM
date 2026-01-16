"""
SERVICE: cea_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: Criterion Enforcement Agents (CEAs) that observe and emit signals

DEPENDENCIES:
- Core: orchestrator_service
- Schemas: governance_schemas

R&D COMPLIANCE: ✅
- Rule #1: Human Sovereignty - CEAs emit signals, don't take actions
- Rule #2: Autonomy Isolation - CEAs observe only, no modifications
- Rule #6: Traceability - All signals are logged
- Rule #7: R&D Continuity - Follows governance canon

HUMAN GATES:
- BLOCK signals require human approval to unblock
"""

import logging
import re
from typing import Optional, List, Dict, Any, Protocol, runtime_checkable
from uuid import uuid4
from datetime import datetime
from abc import ABC, abstractmethod

from ..schemas.governance_schemas import (
    GovernanceSignal,
    GovernanceSignalLevel,
    GovernanceCriterion,
    SignalScope,
    CEAContract,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CEA BASE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class BaseCEA(ABC):
    """
    Base class for all Criterion Enforcement Agents.
    
    CEAs are lightweight checkers that:
    1. Observe output and context
    2. Detect drift or violations
    3. Emit GOVERNANCE_SIGNAL to orchestrator
    
    CEAs do NOT:
    - Modify any state
    - Take direct actions
    - Block execution (they signal, orchestrator decides)
    """
    
    def __init__(self, cea_id: str, criterion: GovernanceCriterion):
        self.cea_id = cea_id
        self.criterion = criterion
        self.enabled = True
        logger.info(f"CEA initialized: {cea_id} ({criterion.value})")
    
    @abstractmethod
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        """
        Check content against criterion.
        
        Args:
            content: The content to check
            context: Additional context (thread state, history, etc.)
            scope: Scope of the check (segment, region, etc.)
            
        Returns:
            List of signals (empty if no issues detected)
        """
        pass
    
    def emit_signal(
        self,
        level: GovernanceSignalLevel,
        message: str,
        confidence: float = 0.5,
        scope: Optional[SignalScope] = None
    ) -> GovernanceSignal:
        """Create and return a governance signal."""
        return GovernanceSignal(
            id=str(uuid4()),
            level=level,
            criterion=self.criterion,
            message=message,
            scope=scope,
            confidence=confidence,
            cea_id=self.cea_id
        )
    
    def get_contract(self) -> CEAContract:
        """Get the contract defining this CEA."""
        return CEAContract(
            id=self.cea_id,
            name=self.cea_id.replace("CEA", " Guard").strip(),
            criterion=self.criterion,
            description=f"Enforces {self.criterion.value} integrity",
            specs_owned=[f"{self.criterion.value.upper()}_GUARD"],
            always_on=True,
            cost_level=1
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CANON GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class CanonGuardCEA(BaseCEA):
    """
    Enforces thread canonical rules:
    - Append-only events
    - No duplicate memory stores
    - No permission bypass
    """
    
    def __init__(self):
        super().__init__("CanonGuardCEA", GovernanceCriterion.CANON)
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        # Check for mutation attempts
        if isinstance(content, dict):
            # Check for delete operations
            if content.get("operation") in ["delete", "remove", "clear"]:
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    "Append-only violation: delete operation attempted",
                    confidence=1.0,
                    scope=scope
                ))
            
            # Check for history rewrite
            if content.get("target") == "event_history":
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    "Canon violation: event history modification attempted",
                    confidence=1.0,
                    scope=scope
                ))
            
            # Check for duplicate memory
            if content.get("creates_secondary_memory"):
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    "Canon violation: duplicate memory store creation",
                    confidence=0.95,
                    scope=scope
                ))
        
        return signals


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMA GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class SchemaGuardCEA(BaseCEA):
    """
    Validates JSON/schema output:
    - Required fields present
    - Type correctness
    - Value constraints
    """
    
    def __init__(self):
        super().__init__("SchemaGuardCEA", GovernanceCriterion.SCHEMA)
        self.schemas: Dict[str, Dict[str, Any]] = {}
    
    def register_schema(self, schema_name: str, schema: Dict[str, Any]) -> None:
        """Register a schema for validation."""
        self.schemas[schema_name] = schema
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        if not isinstance(content, dict):
            return signals
        
        schema_name = context.get("expected_schema")
        if not schema_name or schema_name not in self.schemas:
            return signals
        
        schema = self.schemas[schema_name]
        required_fields = schema.get("required", [])
        
        # Check required fields
        for field in required_fields:
            if field not in content:
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.CORRECT,
                    f"Schema violation: missing required field '{field}'",
                    confidence=1.0,
                    scope=scope
                ))
        
        # Check types
        properties = schema.get("properties", {})
        for field, value in content.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type and not self._check_type(value, expected_type):
                    signals.append(self.emit_signal(
                        GovernanceSignalLevel.CORRECT,
                        f"Schema violation: field '{field}' expected {expected_type}",
                        confidence=0.9,
                        scope=scope
                    ))
        
        return signals
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected JSON schema type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        expected = type_map.get(expected_type)
        if expected is None:
            return True
        return isinstance(value, expected)


# ═══════════════════════════════════════════════════════════════════════════════
# SECURITY GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityGuardCEA(BaseCEA):
    """
    Checks security invariants:
    - No injection attacks
    - No unauthorized access patterns
    - No data leakage
    """
    
    # Patterns to detect
    INJECTION_PATTERNS = [
        r"<script[^>]*>",
        r"javascript:",
        r"on\w+\s*=",
        r"eval\s*\(",
        r"exec\s*\(",
        r";\s*DROP\s+TABLE",
        r";\s*DELETE\s+FROM",
        r"UNION\s+SELECT",
    ]
    
    def __init__(self):
        super().__init__("SecurityGuardCEA", GovernanceCriterion.SECURITY)
        self._compiled_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS
        ]
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        # Convert content to string for pattern matching
        content_str = str(content)
        
        # Check for injection patterns
        for pattern in self._compiled_patterns:
            if pattern.search(content_str):
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    f"Security violation: potential injection attack detected",
                    confidence=0.85,
                    scope=scope
                ))
                break  # One signal is enough
        
        # Check for unauthorized access
        if isinstance(content, dict):
            if content.get("target_identity") and content.get("target_identity") != context.get("current_identity"):
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    "Security violation: cross-identity access without workflow",
                    confidence=0.95,
                    scope=scope
                ))
        
        return signals


# ═══════════════════════════════════════════════════════════════════════════════
# COHERENCE GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class CoherenceGuardCEA(BaseCEA):
    """
    Detects contradictions and drift:
    - Intent drift
    - Contradictory statements
    - Context loss
    """
    
    def __init__(self):
        super().__init__("CoherenceGuardCEA", GovernanceCriterion.COHERENCE)
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        if not isinstance(content, dict):
            return signals
        
        founding_intent = context.get("founding_intent", "")
        current_text = str(content.get("text", content.get("content", "")))
        
        # Check for contradiction keywords (simple heuristic)
        contradiction_indicators = [
            "actually, ignore",
            "forget what I said",
            "the opposite is true",
            "completely different",
            "disregard everything",
        ]
        
        for indicator in contradiction_indicators:
            if indicator.lower() in current_text.lower():
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.CORRECT,
                    f"Coherence warning: potential contradiction detected ('{indicator}')",
                    confidence=0.7,
                    scope=scope
                ))
        
        # Check for severe intent drift
        if founding_intent and current_text:
            # Simple keyword overlap check
            intent_words = set(founding_intent.lower().split())
            current_words = set(current_text.lower().split())
            
            if len(intent_words) > 5:
                overlap = len(intent_words & current_words) / len(intent_words)
                if overlap < 0.1:
                    signals.append(self.emit_signal(
                        GovernanceSignalLevel.WARN,
                        "Coherence warning: content may have drifted from founding intent",
                        confidence=0.6,
                        scope=scope
                    ))
        
        return signals


# ═══════════════════════════════════════════════════════════════════════════════
# STYLE GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class StyleGuardCEA(BaseCEA):
    """
    Checks formatting and clarity:
    - Consistent formatting
    - Clear structure
    - Appropriate length
    """
    
    def __init__(self):
        super().__init__("StyleGuardCEA", GovernanceCriterion.STYLE)
        self.max_line_length = 120
        self.max_paragraph_length = 500
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        if not isinstance(content, str):
            content = str(content)
        
        lines = content.split("\n")
        
        # Check line lengths
        long_lines = [i for i, line in enumerate(lines) if len(line) > self.max_line_length]
        if long_lines:
            signals.append(self.emit_signal(
                GovernanceSignalLevel.WARN,
                f"Style warning: {len(long_lines)} lines exceed {self.max_line_length} chars",
                confidence=0.5,
                scope=scope
            ))
        
        # Check for very long paragraphs
        paragraphs = content.split("\n\n")
        long_paragraphs = [i for i, p in enumerate(paragraphs) if len(p) > self.max_paragraph_length]
        if long_paragraphs:
            signals.append(self.emit_signal(
                GovernanceSignalLevel.WARN,
                f"Style warning: {len(long_paragraphs)} paragraphs may be too long",
                confidence=0.4,
                scope=scope
            ))
        
        return signals


# ═══════════════════════════════════════════════════════════════════════════════
# BUDGET GUARD CEA
# ═══════════════════════════════════════════════════════════════════════════════

class BudgetGuardCEA(BaseCEA):
    """
    Monitors budget and latency:
    - Token budget exceeded
    - Latency spikes
    - Cost anomalies
    """
    
    def __init__(self):
        super().__init__("BudgetGuardCEA", GovernanceCriterion.BUDGET)
        self.warning_threshold = 0.8  # Warn at 80% budget
        self.block_threshold = 0.95   # Block at 95% budget
    
    async def check(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        signals = []
        
        budget_used = context.get("budget_used", 0)
        budget_total = context.get("budget_total", float("inf"))
        latency_ms = context.get("latency_ms", 0)
        latency_budget_ms = context.get("latency_budget_ms", float("inf"))
        
        # Check budget
        if budget_total > 0:
            usage_ratio = budget_used / budget_total
            
            if usage_ratio >= self.block_threshold:
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.BLOCK,
                    f"Budget exceeded: {usage_ratio*100:.1f}% of budget used",
                    confidence=1.0,
                    scope=scope
                ))
            elif usage_ratio >= self.warning_threshold:
                signals.append(self.emit_signal(
                    GovernanceSignalLevel.WARN,
                    f"Budget warning: {usage_ratio*100:.1f}% of budget used",
                    confidence=0.9,
                    scope=scope
                ))
        
        # Check latency
        if latency_budget_ms > 0 and latency_ms > latency_budget_ms:
            signals.append(self.emit_signal(
                GovernanceSignalLevel.WARN,
                f"Latency exceeded: {latency_ms}ms > {latency_budget_ms}ms budget",
                confidence=0.9,
                scope=scope
            ))
        
        return signals


# ═══════════════════════════════════════════════════════════════════════════════
# CEA REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

class CEARegistry:
    """
    Registry of all CEAs for the governance system.
    
    Provides:
    - Registration of CEAs
    - Running all applicable CEAs
    - Aggregating signals
    """
    
    def __init__(self):
        self.ceas: Dict[str, BaseCEA] = {}
        self._register_default_ceas()
    
    def _register_default_ceas(self) -> None:
        """Register default CEAs."""
        default_ceas = [
            CanonGuardCEA(),
            SchemaGuardCEA(),
            SecurityGuardCEA(),
            CoherenceGuardCEA(),
            StyleGuardCEA(),
            BudgetGuardCEA(),
        ]
        for cea in default_ceas:
            self.register(cea)
    
    def register(self, cea: BaseCEA) -> None:
        """Register a CEA."""
        self.ceas[cea.cea_id] = cea
        logger.info(f"Registered CEA: {cea.cea_id}")
    
    def get(self, cea_id: str) -> Optional[BaseCEA]:
        """Get a CEA by ID."""
        return self.ceas.get(cea_id)
    
    async def run_all(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None,
        cea_ids: Optional[List[str]] = None
    ) -> List[GovernanceSignal]:
        """
        Run all (or specified) CEAs and aggregate signals.
        
        Args:
            content: Content to check
            context: Context for checks
            scope: Scope of checks
            cea_ids: Optional list of specific CEAs to run
            
        Returns:
            Aggregated list of signals
        """
        all_signals = []
        
        ceas_to_run = cea_ids or list(self.ceas.keys())
        
        for cea_id in ceas_to_run:
            cea = self.ceas.get(cea_id)
            if cea and cea.enabled:
                try:
                    signals = await cea.check(content, context, scope)
                    all_signals.extend(signals)
                except Exception as e:
                    logger.error(f"CEA {cea_id} failed: {e}")
        
        return all_signals
    
    async def run_always_on(
        self,
        content: Any,
        context: Dict[str, Any],
        scope: Optional[SignalScope] = None
    ) -> List[GovernanceSignal]:
        """Run only always-on CEAs (Canon, Security, Budget)."""
        always_on = ["CanonGuardCEA", "SecurityGuardCEA", "BudgetGuardCEA"]
        return await self.run_all(content, context, scope, always_on)
    
    def get_contracts(self) -> List[CEAContract]:
        """Get contracts for all registered CEAs."""
        return [cea.get_contract() for cea in self.ceas.values()]


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "BaseCEA",
    "CanonGuardCEA",
    "SchemaGuardCEA",
    "SecurityGuardCEA",
    "CoherenceGuardCEA",
    "StyleGuardCEA",
    "BudgetGuardCEA",
    "CEARegistry",
]
