"""
============================================================================
CHE·NU™ V69 — CHECKPOINT SYSTEM
============================================================================
Version: 1.0.0
Purpose: Governance checkpoints for agent actions
Principle: GOUVERNANCE > EXÉCUTION — Human approval for sensitive actions
============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
import logging
import threading
import uuid

from ..core.models import (
    Checkpoint,
    CheckpointType,
    CheckpointStatus,
    AgentAction,
    ActionType,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CHECKPOINT RULE
# ============================================================================

class CheckpointRule:
    """
    Rule that determines when a checkpoint is required.
    """
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        checkpoint_type: CheckpointType,
        condition: Callable[[AgentAction], bool],
        priority: int = 100,
    ):
        self.rule_id = rule_id
        self.name = name
        self.checkpoint_type = checkpoint_type
        self.condition = condition
        self.priority = priority
    
    def applies(self, action: AgentAction) -> bool:
        """Check if this rule applies to the action"""
        try:
            return self.condition(action)
        except Exception as e:
            logger.error(f"Rule {self.rule_id} evaluation failed: {e}")
            return True  # Fail safe: require checkpoint


# ============================================================================
# CHECKPOINT MANAGER
# ============================================================================

class CheckpointManager:
    """
    Manages governance checkpoints for agent actions.
    
    The CheckpointManager:
    - Evaluates rules to determine checkpoint requirements
    - Creates and tracks checkpoints
    - Handles resolution (approval/denial)
    - Supports HITL (Human-In-The-Loop)
    - Logs all decisions for audit
    
    Architecture:
    
        ┌─────────────────────────────────────────────────────────┐
        │                  CHECKPOINT MANAGER                     │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │  Action ──▶ Rules ──▶ Checkpoint? ──▶ Resolution       │
        │                          │                              │
        │                          ▼                              │
        │              ┌───────────────────────┐                 │
        │              │  HITL / OPA / AUTO    │                 │
        │              └───────────────────────┘                 │
        │                          │                              │
        │                          ▼                              │
        │              ┌───────────────────────┐                 │
        │              │  APPROVE / DENY       │                 │
        │              └───────────────────────┘                 │
        │                                                         │
        └─────────────────────────────────────────────────────────┘
    
    Usage:
        manager = CheckpointManager()
        
        # Add rules
        manager.add_rule(CheckpointRule(
            rule_id="high_impact",
            name="High Impact Actions",
            checkpoint_type=CheckpointType.HITL,
            condition=lambda a: a.estimated_impact > 0.5,
        ))
        
        # Check if checkpoint needed
        checkpoint = manager.create_if_needed(action)
        
        if checkpoint:
            # Wait for resolution
            status = manager.wait_for_resolution(checkpoint.checkpoint_id)
    """
    
    def __init__(self):
        self._rules: List[CheckpointRule] = []
        self._checkpoints: Dict[str, Checkpoint] = {}
        self._pending: Dict[str, Checkpoint] = {}
        self._lock = threading.Lock()
        
        # Resolution handlers
        self._hitl_handler: Optional[Callable[[Checkpoint], CheckpointStatus]] = None
        self._opa_handler: Optional[Callable[[Checkpoint], CheckpointStatus]] = None
        
        # Add default rules
        self._add_default_rules()
    
    def _add_default_rules(self) -> None:
        """Add default checkpoint rules"""
        # High impact actions require HITL
        self.add_rule(CheckpointRule(
            rule_id="high_impact",
            name="High Impact Actions",
            checkpoint_type=CheckpointType.HITL,
            condition=lambda a: a.estimated_impact > 0.7,
            priority=10,
        ))
        
        # Write actions require approval
        self.add_rule(CheckpointRule(
            rule_id="write_actions",
            name="Write Actions",
            checkpoint_type=CheckpointType.APPROVAL,
            condition=lambda a: a.action_type == ActionType.WRITE,
            priority=50,
        ))
        
        # Execute actions require OPA check
        self.add_rule(CheckpointRule(
            rule_id="execute_actions",
            name="Execute Actions",
            checkpoint_type=CheckpointType.OPA,
            condition=lambda a: a.action_type == ActionType.EXECUTE,
            priority=30,
        ))
    
    def add_rule(self, rule: CheckpointRule) -> None:
        """Add a checkpoint rule"""
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)
    
    def set_hitl_handler(
        self,
        handler: Callable[[Checkpoint], CheckpointStatus],
    ) -> None:
        """Set handler for HITL checkpoints"""
        self._hitl_handler = handler
    
    def set_opa_handler(
        self,
        handler: Callable[[Checkpoint], CheckpointStatus],
    ) -> None:
        """Set handler for OPA checkpoints"""
        self._opa_handler = handler
    
    def evaluate_rules(self, action: AgentAction) -> Optional[CheckpointRule]:
        """
        Evaluate rules for an action.
        
        Returns the highest priority matching rule, or None.
        """
        for rule in self._rules:
            if rule.applies(action):
                return rule
        return None
    
    def needs_checkpoint(self, action: AgentAction) -> bool:
        """Check if action needs a checkpoint"""
        return self.evaluate_rules(action) is not None
    
    def create_if_needed(self, action: AgentAction) -> Optional[Checkpoint]:
        """
        Create a checkpoint if needed for this action.
        
        Returns the checkpoint or None if not needed.
        """
        rule = self.evaluate_rules(action)
        
        if rule is None:
            return None
        
        checkpoint = self.create_checkpoint(
            agent_id=action.agent_id,
            action_id=action.action_id,
            checkpoint_type=rule.checkpoint_type,
            reason=f"Rule '{rule.name}' triggered",
            details={
                "rule_id": rule.rule_id,
                "action_type": action.action_type.value,
                "target": action.target,
                "estimated_impact": action.estimated_impact,
            },
        )
        
        return checkpoint
    
    def create_checkpoint(
        self,
        agent_id: str,
        action_id: str,
        checkpoint_type: CheckpointType,
        reason: str,
        details: Optional[Dict[str, Any]] = None,
        timeout_minutes: int = 60,
    ) -> Checkpoint:
        """Create a new checkpoint"""
        checkpoint = Checkpoint(
            agent_id=agent_id,
            action_id=action_id,
            checkpoint_type=checkpoint_type,
            reason=reason,
            details=details or {},
            timeout_at=datetime.utcnow() + timedelta(minutes=timeout_minutes),
        )
        
        with self._lock:
            self._checkpoints[checkpoint.checkpoint_id] = checkpoint
            self._pending[checkpoint.checkpoint_id] = checkpoint
        
        logger.info(
            f"Checkpoint created: {checkpoint.checkpoint_id} "
            f"({checkpoint_type.value}) for action {action_id}"
        )
        
        return checkpoint
    
    def resolve(
        self,
        checkpoint_id: str,
        status: CheckpointStatus,
        resolved_by: str = "system",
        notes: Optional[str] = None,
    ) -> Checkpoint:
        """Resolve a checkpoint"""
        with self._lock:
            if checkpoint_id not in self._checkpoints:
                raise ValueError(f"Checkpoint not found: {checkpoint_id}")
            
            checkpoint = self._checkpoints[checkpoint_id]
            
            checkpoint.status = status
            checkpoint.resolved_at = datetime.utcnow()
            checkpoint.resolved_by = resolved_by
            checkpoint.resolution_notes = notes
            
            if checkpoint_id in self._pending:
                del self._pending[checkpoint_id]
        
        logger.info(
            f"Checkpoint resolved: {checkpoint_id} -> {status.value} "
            f"by {resolved_by}"
        )
        
        return checkpoint
    
    def approve(
        self,
        checkpoint_id: str,
        approved_by: str,
        notes: Optional[str] = None,
    ) -> Checkpoint:
        """Approve a checkpoint"""
        return self.resolve(
            checkpoint_id,
            CheckpointStatus.APPROVED,
            resolved_by=approved_by,
            notes=notes,
        )
    
    def deny(
        self,
        checkpoint_id: str,
        denied_by: str,
        reason: str,
    ) -> Checkpoint:
        """Deny a checkpoint"""
        return self.resolve(
            checkpoint_id,
            CheckpointStatus.DENIED,
            resolved_by=denied_by,
            notes=reason,
        )
    
    def escalate(
        self,
        checkpoint_id: str,
        escalated_to: str,
    ) -> Checkpoint:
        """Escalate a checkpoint to higher level"""
        with self._lock:
            if checkpoint_id not in self._checkpoints:
                raise ValueError(f"Checkpoint not found: {checkpoint_id}")
            
            checkpoint = self._checkpoints[checkpoint_id]
            checkpoint.escalated_to = escalated_to
            checkpoint.escalation_level += 1
            checkpoint.status = CheckpointStatus.ESCALATED
            checkpoint.resolved_at = datetime.utcnow()
            
            if checkpoint_id in self._pending:
                del self._pending[checkpoint_id]
        
        logger.info(f"Checkpoint escalated: {checkpoint_id} -> {escalated_to}")
        
        return checkpoint
    
    def auto_resolve(self, checkpoint: Checkpoint) -> CheckpointStatus:
        """
        Automatically resolve a checkpoint based on type.
        
        This is used for non-HITL checkpoints or when HITL times out.
        """
        if checkpoint.checkpoint_type == CheckpointType.OPA:
            # Use OPA handler if available
            if self._opa_handler:
                status = self._opa_handler(checkpoint)
            else:
                # Default: approve (in production, would call OPA)
                status = CheckpointStatus.APPROVED
            
        elif checkpoint.checkpoint_type == CheckpointType.THRESHOLD:
            # Check threshold
            impact = checkpoint.details.get("estimated_impact", 0)
            status = CheckpointStatus.APPROVED if impact < 0.8 else CheckpointStatus.DENIED
            
        elif checkpoint.checkpoint_type == CheckpointType.HITL:
            # Use HITL handler if available
            if self._hitl_handler:
                status = self._hitl_handler(checkpoint)
            else:
                # Default: deny (require actual human)
                status = CheckpointStatus.DENIED
                
        else:
            # Default: approve
            status = CheckpointStatus.APPROVED
        
        self.resolve(checkpoint.checkpoint_id, status, "auto")
        return status
    
    def wait_for_resolution(
        self,
        checkpoint_id: str,
        timeout_seconds: float = 60,
    ) -> CheckpointStatus:
        """
        Wait for a checkpoint to be resolved.
        
        In production, this would be async with webhooks/polling.
        """
        checkpoint = self._checkpoints.get(checkpoint_id)
        if checkpoint is None:
            raise ValueError(f"Checkpoint not found: {checkpoint_id}")
        
        if checkpoint.is_resolved:
            return checkpoint.status
        
        # For now, auto-resolve
        return self.auto_resolve(checkpoint)
    
    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Get checkpoint by ID"""
        return self._checkpoints.get(checkpoint_id)
    
    def get_pending(self) -> List[Checkpoint]:
        """Get all pending checkpoints"""
        return list(self._pending.values())
    
    def get_pending_for_agent(self, agent_id: str) -> List[Checkpoint]:
        """Get pending checkpoints for an agent"""
        return [c for c in self._pending.values() if c.agent_id == agent_id]
    
    def check_timeout(self) -> List[Checkpoint]:
        """Check for timed out checkpoints"""
        now = datetime.utcnow()
        timed_out = []
        
        with self._lock:
            for checkpoint_id, checkpoint in list(self._pending.items()):
                if checkpoint.timeout_at and checkpoint.timeout_at < now:
                    checkpoint.status = CheckpointStatus.TIMEOUT
                    checkpoint.resolved_at = now
                    checkpoint.resolved_by = "system"
                    checkpoint.resolution_notes = "Timeout"
                    del self._pending[checkpoint_id]
                    timed_out.append(checkpoint)
        
        return timed_out


# ============================================================================
# HITL CONTROLLER
# ============================================================================

class HITLController:
    """
    Human-In-The-Loop controller.
    
    Manages human approval workflow for sensitive actions.
    
    In production, this would integrate with:
    - Web UI for approval
    - Mobile notifications
    - Email/Slack alerts
    - SSO/MFA for approval
    """
    
    def __init__(self, checkpoint_manager: CheckpointManager):
        self.checkpoint_manager = checkpoint_manager
        self._approval_queue: List[Checkpoint] = []
        
        # Register as HITL handler
        checkpoint_manager.set_hitl_handler(self._handle_hitl)
    
    def _handle_hitl(self, checkpoint: Checkpoint) -> CheckpointStatus:
        """Handle HITL checkpoint (mock implementation)"""
        # Add to queue
        self._approval_queue.append(checkpoint)
        
        # In production: send notification, wait for response
        # For now: auto-approve if impact < 0.9
        impact = checkpoint.details.get("estimated_impact", 1.0)
        
        if impact < 0.9:
            return CheckpointStatus.APPROVED
        else:
            return CheckpointStatus.DENIED
    
    def get_pending_approvals(self) -> List[Checkpoint]:
        """Get checkpoints pending human approval"""
        return list(self._approval_queue)
    
    def approve(
        self,
        checkpoint_id: str,
        user_id: str,
        notes: Optional[str] = None,
    ) -> Checkpoint:
        """Human approves a checkpoint"""
        checkpoint = self.checkpoint_manager.approve(
            checkpoint_id,
            approved_by=user_id,
            notes=notes,
        )
        
        # Remove from queue
        self._approval_queue = [
            c for c in self._approval_queue
            if c.checkpoint_id != checkpoint_id
        ]
        
        return checkpoint
    
    def deny(
        self,
        checkpoint_id: str,
        user_id: str,
        reason: str,
    ) -> Checkpoint:
        """Human denies a checkpoint"""
        checkpoint = self.checkpoint_manager.deny(
            checkpoint_id,
            denied_by=user_id,
            reason=reason,
        )
        
        # Remove from queue
        self._approval_queue = [
            c for c in self._approval_queue
            if c.checkpoint_id != checkpoint_id
        ]
        
        return checkpoint


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_checkpoint_manager() -> CheckpointManager:
    """Create a checkpoint manager with default rules"""
    return CheckpointManager()


def create_hitl_controller(
    checkpoint_manager: Optional[CheckpointManager] = None,
) -> HITLController:
    """Create a HITL controller"""
    manager = checkpoint_manager or create_checkpoint_manager()
    return HITLController(manager)
