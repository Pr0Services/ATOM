"""
============================================================================
CHE·NU™ V69 — SLOT FILL AGENT ASSIGNMENT
============================================================================
Spec: GPT1/CHE-NU_ENG_SLOT_FILL_AGENT_ASSIGNMENT.md

Rules (per spec):
- 1 slot = 1 agent principal
- Aucun agent ne contrôle tout le document
- Les agents ne se parlent pas sans orchestrateur user-hired
- Si slot échoue 2 fois → humain requis
- Si risk=high → HITL immédiat

Principle:
- Un agent remplit.
- Un autre vérifie.
- Un humain décide.
============================================================================
"""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set
from enum import Enum
import logging

from ..models import (
    Slot,
    SlotType,
    SlotStatus,
    RiskLevel,
    AgentType,
    SlotFillRequest,
    SlotFillResult,
    SlotExplainability,
    Document,
    SLOT_TO_AGENT_MAPPING,
)

logger = logging.getLogger(__name__)


# ============================================================================
# ASSIGNMENT RULES
# ============================================================================

class AssignmentRule:
    """Rule for agent assignment"""
    
    def __init__(
        self,
        name: str,
        condition: Callable[[Slot], bool],
        agent: AgentType,
        priority: int = 0,
    ):
        self.name = name
        self.condition = condition
        self.agent = agent
        self.priority = priority
    
    def applies(self, slot: Slot) -> bool:
        """Check if rule applies to slot"""
        return self.condition(slot)


class AssignmentResult(Enum):
    """Result of assignment attempt"""
    SUCCESS = "success"
    REQUIRES_HITL = "requires_hitl"
    BLOCKED = "blocked"
    NO_AGENT = "no_agent"


# ============================================================================
# SLOT ASSIGNER
# ============================================================================

class SlotAssigner:
    """
    Assigns slots to specialized agents.
    
    Per spec:
    - 1 slot = 1 agent principal
    - Assignation auditée
    - Historique conservé
    """
    
    def __init__(self):
        self._rules: List[AssignmentRule] = []
        self._assignment_history: List[Dict[str, Any]] = []
        self._active_assignments: Dict[str, AgentType] = {}  # slot_id → agent
        
        # Add default rules
        self._add_default_rules()
    
    def _add_default_rules(self) -> None:
        """Add default assignment rules based on slot type"""
        for slot_type, agent_type in SLOT_TO_AGENT_MAPPING.items():
            self._rules.append(
                AssignmentRule(
                    name=f"default_{slot_type.value}",
                    condition=lambda s, st=slot_type: s.slot_type == st,
                    agent=agent_type,
                    priority=0,
                )
            )
    
    def add_rule(self, rule: AssignmentRule) -> None:
        """Add custom assignment rule"""
        self._rules.append(rule)
        # Sort by priority (higher first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
    
    def assign(self, slot: Slot) -> tuple[AssignmentResult, Optional[AgentType]]:
        """
        Assign a slot to an agent.
        
        Returns:
            Tuple of (result, agent_type)
        """
        # Check HITL requirements first (per spec)
        if slot.requires_hitl():
            self._record_assignment(slot, None, AssignmentResult.REQUIRES_HITL)
            return AssignmentResult.REQUIRES_HITL, None
        
        # Check risk level (per spec: risk=high → HITL immédiat)
        if slot.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            self._record_assignment(slot, None, AssignmentResult.REQUIRES_HITL)
            return AssignmentResult.REQUIRES_HITL, None
        
        # Find matching rule
        for rule in self._rules:
            if rule.applies(slot):
                slot.assigned_agent = rule.agent
                self._active_assignments[slot.slot_id] = rule.agent
                self._record_assignment(slot, rule.agent, AssignmentResult.SUCCESS)
                
                logger.info(f"Assigned slot {slot.slot_id} to {rule.agent.value}")
                return AssignmentResult.SUCCESS, rule.agent
        
        # No matching rule - use auto-assign
        agent = slot.auto_assign_agent()
        self._active_assignments[slot.slot_id] = agent
        self._record_assignment(slot, agent, AssignmentResult.SUCCESS)
        
        return AssignmentResult.SUCCESS, agent
    
    def assign_document(self, document: Document) -> Dict[str, AssignmentResult]:
        """
        Assign all slots in a document.
        
        Per spec: Aucun agent ne contrôle tout le document
        """
        results: Dict[str, AssignmentResult] = {}
        agent_counts: Dict[AgentType, int] = {}
        
        for slot_id, slot in document.slots.items():
            result, agent = self.assign(slot)
            results[slot_id] = result
            
            if agent:
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        # Verify no single agent controls too much
        total_slots = len(document.slots)
        if total_slots > 0:
            max_percentage = max(agent_counts.values(), default=0) / total_slots
            if max_percentage > 0.8:  # No agent should control > 80%
                logger.warning(
                    f"Document {document.document_id} has agent concentration issue: "
                    f"max {max_percentage:.1%}"
                )
        
        return results
    
    def get_verifier(self, filler_agent: AgentType) -> AgentType:
        """
        Get verification agent (different from filler).
        
        Per spec: Un agent remplit. Un autre vérifie.
        """
        # Verification agent should be different from filler
        verifier_map = {
            AgentType.WRITING_AGENT: AgentType.COMPLIANCE_AGENT,
            AgentType.DATA_AGENT: AgentType.VERIFICATION_AGENT,
            AgentType.PLANNING_AGENT: AgentType.VERIFICATION_AGENT,
            AgentType.COMPLIANCE_AGENT: AgentType.VERIFICATION_AGENT,
            AgentType.FINANCE_AGENT: AgentType.COMPLIANCE_AGENT,
            AgentType.BRAND_GUARD_AGENT: AgentType.VERIFICATION_AGENT,
            AgentType.VERIFICATION_AGENT: AgentType.COMPLIANCE_AGENT,
        }
        return verifier_map.get(filler_agent, AgentType.VERIFICATION_AGENT)
    
    def record_fill_attempt(self, slot: Slot, success: bool) -> bool:
        """
        Record a fill attempt.
        
        Returns True if HITL is now required.
        """
        slot.fill_attempts += 1
        
        if success:
            slot.status = SlotStatus.FILLED
            slot.filled_at = datetime.utcnow()
            return False
        else:
            # Per spec: Si slot échoue 2 fois → humain requis
            if slot.fill_attempts >= slot.max_attempts:
                slot.status = SlotStatus.BLOCKED
                logger.warning(f"Slot {slot.slot_id} blocked after {slot.fill_attempts} failed attempts")
                return True
            return False
    
    def _record_assignment(
        self,
        slot: Slot,
        agent: Optional[AgentType],
        result: AssignmentResult,
    ) -> None:
        """Record assignment for audit"""
        self._assignment_history.append({
            "slot_id": slot.slot_id,
            "slot_type": slot.slot_type.value,
            "agent": agent.value if agent else None,
            "result": result.value,
            "risk_level": slot.risk_level.value,
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def get_assignment_history(self) -> List[Dict[str, Any]]:
        """Get assignment history for audit"""
        return self._assignment_history.copy()
    
    def get_agent_workload(self) -> Dict[AgentType, int]:
        """Get current workload per agent"""
        workload: Dict[AgentType, int] = {}
        for agent in self._active_assignments.values():
            workload[agent] = workload.get(agent, 0) + 1
        return workload


# ============================================================================
# ORCHESTRATOR
# ============================================================================

class SlotFillOrchestrator:
    """
    Orchestrates slot filling workflow.
    
    Per spec: Les agents ne se parlent pas sans orchestrateur user-hired
    """
    
    def __init__(self, assigner: SlotAssigner = None):
        self.assigner = assigner or SlotAssigner()
        self._pending_hitl: List[Slot] = []
        self._fill_handlers: Dict[AgentType, Callable] = {}
        self._verify_handlers: Dict[AgentType, Callable] = {}
    
    def register_fill_handler(
        self,
        agent: AgentType,
        handler: Callable[[Slot, Dict[str, Any]], SlotFillResult],
    ) -> None:
        """Register a fill handler for an agent type"""
        self._fill_handlers[agent] = handler
    
    def register_verify_handler(
        self,
        agent: AgentType,
        handler: Callable[[Slot, Any], bool],
    ) -> None:
        """Register a verify handler for an agent type"""
        self._verify_handlers[agent] = handler
    
    def fill_slot(
        self,
        slot: Slot,
        context: Dict[str, Any] = None,
    ) -> SlotFillResult:
        """
        Fill a single slot through the full workflow.
        
        Workflow:
        1. Assign agent
        2. Fill via agent
        3. Verify via different agent
        4. Return result with explainability
        """
        context = context or {}
        trace_id = context.get("trace_id", str(datetime.utcnow().timestamp()))
        
        # Step 1: Assign agent
        result, filler_agent = self.assigner.assign(slot)
        
        if result == AssignmentResult.REQUIRES_HITL:
            self._pending_hitl.append(slot)
            return SlotFillResult(
                slot_id=slot.slot_id,
                success=False,
                requires_hitl=True,
                trace_id=trace_id,
                error_message="Human-in-the-loop required",
            )
        
        if not filler_agent:
            return SlotFillResult(
                slot_id=slot.slot_id,
                success=False,
                trace_id=trace_id,
                error_message="No agent available",
            )
        
        # Step 2: Fill via agent
        handler = self._fill_handlers.get(filler_agent)
        if handler:
            fill_result = handler(slot, context)
        else:
            # Default mock fill
            fill_result = self._mock_fill(slot, filler_agent, trace_id)
        
        # Step 3: Verify via different agent
        verifier_agent = self.assigner.get_verifier(filler_agent)
        verify_handler = self._verify_handlers.get(verifier_agent)
        
        verified = True
        if verify_handler and fill_result.value is not None:
            verified = verify_handler(slot, fill_result.value)
        
        if not verified:
            fill_result.success = False
            fill_result.error_message = "Verification failed"
        
        fill_result.verified_by_agent = verifier_agent
        
        # Record attempt
        requires_hitl = self.assigner.record_fill_attempt(slot, fill_result.success)
        fill_result.requires_hitl = requires_hitl
        
        if requires_hitl:
            self._pending_hitl.append(slot)
        
        return fill_result
    
    def fill_document(
        self,
        document: Document,
        context: Dict[str, Any] = None,
    ) -> List[SlotFillResult]:
        """Fill all slots in a document"""
        context = context or {}
        results: List[SlotFillResult] = []
        
        # Get priority-ordered slots
        ordered_slots = document.get_priority_ordered_slots()
        
        for slot in ordered_slots:
            if slot.status not in [SlotStatus.VALIDATED, SlotStatus.BLOCKED]:
                result = self.fill_slot(slot, context)
                results.append(result)
        
        document.update_counts()
        return results
    
    def _mock_fill(
        self,
        slot: Slot,
        agent: AgentType,
        trace_id: str,
    ) -> SlotFillResult:
        """Mock fill for testing"""
        # Generate mock value based on type
        mock_values = {
            SlotType.TEXT: "Sample text content",
            SlotType.NUMBER: 42,
            SlotType.LIST: ["item1", "item2", "item3"],
            SlotType.LEGAL: "Legal clause placeholder",
            SlotType.FINANCE: 1000.00,
            SlotType.BRAND: "Brand-compliant content",
            SlotType.DATE: datetime.utcnow().isoformat(),
            SlotType.BOOLEAN: True,
            SlotType.REFERENCE: "ref-001",
            SlotType.CUSTOM: "Custom value",
        }
        
        value = mock_values.get(slot.slot_type, "default")
        
        # Generate explainability (required per spec)
        explainability = SlotExplainability(
            slot_id=slot.slot_id,
            decision_summary=f"Filled by {agent.value}",
            rationale=f"Based on slot type {slot.slot_type.value}",
            sources=["system_default"],
            confidence_score=0.8,
            generated_by=agent.value,
        )
        
        return SlotFillResult(
            slot_id=slot.slot_id,
            success=True,
            value=value,
            filled_by_agent=agent,
            explainability=explainability,
            trace_id=trace_id,
        )
    
    def get_pending_hitl(self) -> List[Slot]:
        """Get slots pending human approval"""
        return self._pending_hitl.copy()
    
    def resolve_hitl(
        self,
        slot_id: str,
        approved: bool,
        value: Any = None,
        resolved_by: str = "human",
    ) -> bool:
        """Resolve a HITL request"""
        for slot in self._pending_hitl:
            if slot.slot_id == slot_id:
                if approved:
                    slot.status = SlotStatus.VALIDATED
                    slot.value = value
                    slot.validated_at = datetime.utcnow()
                else:
                    slot.status = SlotStatus.FAILED
                
                self._pending_hitl.remove(slot)
                return True
        return False


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_assigner() -> SlotAssigner:
    """Create a slot assigner with default rules"""
    return SlotAssigner()


def create_orchestrator(assigner: SlotAssigner = None) -> SlotFillOrchestrator:
    """Create a slot fill orchestrator"""
    return SlotFillOrchestrator(assigner)
