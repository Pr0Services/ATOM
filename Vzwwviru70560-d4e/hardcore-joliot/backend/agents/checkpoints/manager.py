"""
============================================================================
CHE-NU V69 - CHECKPOINT SYSTEM
============================================================================
Version: 1.1.0
Purpose: Governance checkpoints for agent actions with database persistence
Principle: GOUVERNANCE > EXECUTION - Human approval for sensitive actions

Features:
- In-memory checkpoint management for fast access
- Database persistence for durability (survives restarts)
- Recovery on startup from database
- Fail-closed mode for critical operations
- Full audit trail
============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
import logging
import threading
import uuid
import os

from ..core.models import (
    Checkpoint,
    CheckpointType,
    CheckpointStatus,
    AgentAction,
    ActionType,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class CheckpointConfig:
    """
    Configuration for checkpoint system behavior.

    Environment variables:
    - GOVERNANCE_FAIL_CLOSED: If true, operations fail when governance unavailable
    - GOVERNANCE_PERSISTENCE_ENABLED: If true, checkpoints are persisted to database
    - GOVERNANCE_RECOVERY_ON_STARTUP: If true, pending checkpoints loaded on startup
    """

    def __init__(self):
        self.fail_closed = os.getenv("GOVERNANCE_FAIL_CLOSED", "false").lower() == "true"
        self.persistence_enabled = os.getenv("GOVERNANCE_PERSISTENCE_ENABLED", "true").lower() == "true"
        self.recovery_on_startup = os.getenv("GOVERNANCE_RECOVERY_ON_STARTUP", "true").lower() == "true"
        self.default_timeout_minutes = int(os.getenv("CHECKPOINT_DEFAULT_TIMEOUT_MINUTES", "60"))

    def __repr__(self):
        return (
            f"CheckpointConfig(fail_closed={self.fail_closed}, "
            f"persistence_enabled={self.persistence_enabled}, "
            f"recovery_on_startup={self.recovery_on_startup})"
        )


# Global configuration instance
checkpoint_config = CheckpointConfig()


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
    - Persists checkpoints to database for durability
    - Recovers pending checkpoints on startup

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
        │                          │                              │
        │                          ▼                              │
        │              ┌───────────────────────┐                 │
        │              │  DATABASE PERSIST     │                 │
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

    def __init__(self, db_session=None, config: Optional[CheckpointConfig] = None):
        self._rules: List[CheckpointRule] = []
        self._checkpoints: Dict[str, Checkpoint] = {}
        self._pending: Dict[str, Checkpoint] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

        # Configuration
        self._config = config or checkpoint_config

        # Database session for persistence
        self._db_session = db_session

        # Resolution handlers
        self._hitl_handler: Optional[Callable[[Checkpoint], CheckpointStatus]] = None
        self._opa_handler: Optional[Callable[[Checkpoint], CheckpointStatus]] = None

        # Add default rules
        self._add_default_rules()

        # Recovery: Load pending checkpoints from database on startup
        if self._config.recovery_on_startup and self._db_session is not None:
            self._recover_pending_checkpoints()
    
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
        timeout_minutes: Optional[int] = None,
    ) -> Checkpoint:
        """Create a new checkpoint"""
        # Use configured default timeout if not specified
        if timeout_minutes is None:
            timeout_minutes = self._config.default_timeout_minutes

        # Fail-closed check
        if self._config.fail_closed and not self.check_governance_available():
            logger.error("FAIL-CLOSED: Cannot create checkpoint - governance unavailable")
            raise RuntimeError("Governance system unavailable (fail-closed mode)")

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

        # Persist to database
        self._persist_checkpoint(checkpoint)

        # Audit log
        self._add_audit_event({
            "type": "CHECKPOINT_CREATED",
            "checkpoint_id": checkpoint.checkpoint_id,
            "checkpoint_type": checkpoint_type.value,
            "agent_id": agent_id,
            "action_id": action_id,
            "reason": reason,
        })

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

        # Persist update to database
        event_type = f"CHECKPOINT_{status.value.upper()}"
        self._persist_checkpoint_update(checkpoint, event_type, resolved_by)

        # Audit log
        self._add_audit_event({
            "type": event_type,
            "checkpoint_id": checkpoint_id,
            "resolved_by": resolved_by,
            "notes": notes,
        })

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

        # Persist update to database
        self._persist_checkpoint_update(checkpoint, "CHECKPOINT_ESCALATED", escalated_to)

        # Audit log
        self._add_audit_event({
            "type": "CHECKPOINT_ESCALATED",
            "checkpoint_id": checkpoint_id,
            "escalated_to": escalated_to,
            "escalation_level": checkpoint.escalation_level,
        })

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

                    # Persist timeout to database
                    self._persist_checkpoint_update(checkpoint, "TIMEOUT")

        return timed_out

    # ========================================================================
    # DATABASE PERSISTENCE
    # ========================================================================

    def _recover_pending_checkpoints(self) -> int:
        """
        Recover pending checkpoints from database on startup.

        Returns number of checkpoints recovered.
        """
        if not self._db_session:
            logger.warning("No database session - skipping checkpoint recovery")
            return 0

        try:
            from .models import PersistedCheckpoint, PersistedCheckpointStatus

            # Query pending checkpoints
            pending = self._db_session.query(PersistedCheckpoint).filter(
                PersistedCheckpoint.status == PersistedCheckpointStatus.PENDING
            ).all()

            recovered = 0
            for persisted in pending:
                # Convert to in-memory Checkpoint
                checkpoint = Checkpoint(
                    checkpoint_id=str(persisted.id),
                    agent_id=persisted.agent_id,
                    action_id=persisted.action_id,
                    checkpoint_type=CheckpointType(persisted.checkpoint_type.value),
                    reason=persisted.reason,
                    status=CheckpointStatus(persisted.status.value),
                    details=persisted.details or {},
                    resolved_by=persisted.resolved_by,
                    resolution_notes=persisted.resolution_notes,
                    resolved_at=persisted.resolved_at,
                    timeout_at=persisted.timeout_at,
                    escalated_to=persisted.escalated_to,
                    escalation_level=persisted.escalation_level,
                    created_at=persisted.created_at,
                )

                with self._lock:
                    self._checkpoints[checkpoint.checkpoint_id] = checkpoint
                    self._pending[checkpoint.checkpoint_id] = checkpoint

                recovered += 1

            if recovered > 0:
                logger.info(f"Recovered {recovered} pending checkpoints from database")

            # Log audit event
            self._add_audit_event({
                "type": "RECOVERY_COMPLETED",
                "checkpoints_recovered": recovered,
                "timestamp": datetime.utcnow().isoformat(),
            })

            return recovered

        except ImportError:
            logger.warning("Checkpoint models not available - skipping recovery")
            return 0
        except Exception as e:
            logger.error(f"Failed to recover checkpoints: {e}")
            return 0

    def _persist_checkpoint(self, checkpoint: Checkpoint) -> bool:
        """
        Persist a checkpoint to the database.

        Returns True if successful, False otherwise.
        """
        if not self._config.persistence_enabled:
            return True

        if not self._db_session:
            logger.warning("No database session - checkpoint not persisted")
            return False

        try:
            from .models import (
                PersistedCheckpoint,
                PersistedCheckpointType,
                PersistedCheckpointStatus,
                CheckpointAuditLog,
            )

            # Create persisted checkpoint
            persisted = PersistedCheckpoint(
                id=uuid.UUID(checkpoint.checkpoint_id),
                agent_id=checkpoint.agent_id,
                action_id=checkpoint.action_id,
                checkpoint_type=PersistedCheckpointType(checkpoint.checkpoint_type.value),
                reason=checkpoint.reason,
                status=PersistedCheckpointStatus(checkpoint.status.value),
                details=checkpoint.details,
                timeout_at=checkpoint.timeout_at,
                created_by="system",
            )

            self._db_session.add(persisted)

            # Create audit log entry
            audit_entry = CheckpointAuditLog(
                checkpoint_id=persisted.id,
                event_type="CHECKPOINT_CREATED",
                event_data={
                    "checkpoint_type": checkpoint.checkpoint_type.value,
                    "reason": checkpoint.reason,
                    "agent_id": checkpoint.agent_id,
                    "action_id": checkpoint.action_id,
                },
                actor_type="system",
            )
            self._db_session.add(audit_entry)

            self._db_session.commit()

            logger.debug(f"Checkpoint {checkpoint.checkpoint_id} persisted to database")
            return True

        except ImportError:
            logger.warning("Checkpoint models not available - persistence disabled")
            return False
        except Exception as e:
            logger.error(f"Failed to persist checkpoint: {e}")
            if self._db_session:
                self._db_session.rollback()
            return False

    def _persist_checkpoint_update(
        self,
        checkpoint: Checkpoint,
        event_type: str,
        actor_id: Optional[str] = None,
    ) -> bool:
        """
        Persist a checkpoint status update to the database.

        Returns True if successful, False otherwise.
        """
        if not self._config.persistence_enabled:
            return True

        if not self._db_session:
            return False

        try:
            from .models import (
                PersistedCheckpoint,
                PersistedCheckpointStatus,
                CheckpointAuditLog,
            )

            # Update persisted checkpoint
            persisted = self._db_session.query(PersistedCheckpoint).filter(
                PersistedCheckpoint.id == uuid.UUID(checkpoint.checkpoint_id)
            ).first()

            if not persisted:
                logger.warning(f"Checkpoint {checkpoint.checkpoint_id} not found in database")
                return False

            # Update fields
            persisted.status = PersistedCheckpointStatus(checkpoint.status.value)
            persisted.resolved_by = checkpoint.resolved_by
            persisted.resolution_notes = checkpoint.resolution_notes
            persisted.resolved_at = checkpoint.resolved_at
            persisted.escalated_to = checkpoint.escalated_to
            persisted.escalation_level = checkpoint.escalation_level

            # Create audit log entry
            audit_entry = CheckpointAuditLog(
                checkpoint_id=persisted.id,
                event_type=event_type,
                event_data={
                    "new_status": checkpoint.status.value,
                    "resolved_by": checkpoint.resolved_by,
                    "notes": checkpoint.resolution_notes,
                },
                actor_id=actor_id,
                actor_type="user" if actor_id else "system",
            )
            self._db_session.add(audit_entry)

            self._db_session.commit()

            logger.debug(f"Checkpoint {checkpoint.checkpoint_id} updated in database")
            return True

        except ImportError:
            return False
        except Exception as e:
            logger.error(f"Failed to update checkpoint in database: {e}")
            if self._db_session:
                self._db_session.rollback()
            return False

    def _add_audit_event(self, event: Dict[str, Any]) -> None:
        """Add an event to the in-memory audit log."""
        with self._lock:
            self._audit_log.append({
                **event,
                "recorded_at": datetime.utcnow().isoformat(),
            })
            # Keep only last 1000 events in memory
            if len(self._audit_log) > 1000:
                self._audit_log = self._audit_log[-1000:]

    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit log entries."""
        with self._lock:
            return list(reversed(self._audit_log[-limit:]))

    def check_governance_available(self) -> bool:
        """
        Check if governance system is available for operations.

        In fail-closed mode, returns False if critical components unavailable.
        """
        try:
            # Check basic functionality
            if not self._rules:
                return False

            # If persistence required, check database
            if self._config.persistence_enabled and self._config.fail_closed:
                if self._db_session is None:
                    logger.error("FAIL-CLOSED: Database session unavailable")
                    return False

            return True

        except Exception as e:
            logger.error(f"Governance availability check failed: {e}")
            return not self._config.fail_closed


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
