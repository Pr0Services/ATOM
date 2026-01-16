"""
============================================================================
CHE·NU™ V69 — AUDITED FEEDBACK ENGINE
============================================================================
Version: 1.0.0
Purpose: Feedback simulation with full audit trail
Principle: GOUVERNANCE > EXÉCUTION - Every step is audited
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

from ..models import (
    Slot,
    WorldState,
    FeedbackEdge,
    TransferFunction,
    FeedbackParams,
    SimulationConfig,
    StabilityStatus,
)
from .engine import FeedbackLoopEngine, L2SafetyController
from ...audit.logs.immutable import (
    AuditLog,
    AuditEvent,
    EventType,
    AuditLevel,
    get_audit_manager,
)

logger = logging.getLogger(__name__)


# ============================================================================
# AUDITED FEEDBACK ENGINE
# ============================================================================

class AuditedFeedbackEngine:
    """
    Feedback simulation with integrated audit logging.
    
    Every meaningful event is recorded in an immutable audit log
    with Merkle Tree integrity.
    
    Usage:
        engine = AuditedFeedbackEngine(config)
        results = engine.run()
        
        # Get audit report
        report = engine.get_audit_report()
        
        # Verify event
        is_valid = engine.verify_event(event_id)
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.inner_engine = FeedbackLoopEngine(config)
        
        # Create audit log
        self.audit_log = AuditLog(
            simulation_id=config.simulation_id,
            tenant_id=config.tenant_id,
        )
        
        # Record initialization
        self.audit_log.record(
            EventType.SIMULATION_START,
            f"Simulation '{config.name}' initialized",
            data={
                "t_start": config.t_start,
                "t_end": config.t_end,
                "slot_count": len(config.initial_slots),
                "transfer_count": len(config.transfer_functions),
                "feedback_count": len(config.feedback_edges),
                "seed": config.seed,
            },
        )
        
        # Record seed usage
        if config.seed is not None:
            self.audit_log.record(
                EventType.SEED_USED,
                f"Deterministic seed set: {config.seed}",
                level=AuditLevel.GOVERNANCE,
                data={"seed": config.seed},
            )
    
    def run(self) -> Dict[str, Any]:
        """Run simulation with full audit trail"""
        logger.info(f"Starting audited simulation: {self.config.name}")
        
        while self.inner_engine.current_tick < self.config.t_end:
            result = self._audited_step()
            
            if result.get("stopped"):
                self.audit_log.record(
                    EventType.SAFETY_STOP,
                    f"Simulation stopped at T={self.inner_engine.current_tick}",
                    level=AuditLevel.CRITICAL,
                    data={"reason": result.get("reason", "stability_issue")},
                )
                break
            
            self.inner_engine.current_tick += 1
        
        # Record completion
        self.audit_log.record(
            EventType.SIMULATION_END,
            f"Simulation completed at T={self.inner_engine.current_tick}",
            data={
                "final_tick": self.inner_engine.current_tick,
                "artifacts_generated": len(self.inner_engine.artifacts),
            },
        )
        
        # Finalize audit log
        merkle_root = self.audit_log.finalize()
        
        # Generate summary
        summary = self.inner_engine._generate_summary()
        summary["audit"] = {
            "merkle_root": merkle_root,
            "event_count": len(self.audit_log.events),
            "finalized": True,
        }
        
        return summary
    
    def _audited_step(self) -> Dict[str, Any]:
        """Execute single step with audit logging"""
        current_state = self.inner_engine.states[-1]
        t_from = current_state.tick
        t_to = t_from + 1
        
        # Record step start
        self.audit_log.record(
            EventType.SIMULATION_STEP,
            f"Executing step T={t_from} -> T={t_to}",
            data={
                "t_from": t_from,
                "t_to": t_to,
                "state_hash": current_state.hash[:16],
            },
        )
        
        # Execute step
        result = self.inner_engine.step()
        
        # Record artifact
        if result.get("artifact_id"):
            artifact = self.inner_engine.artifacts[-1]
            self.audit_log.record(
                EventType.ARTIFACT_SIGNED,
                f"Artifact signed: {artifact.artifact_id[:16]}",
                artifact_id=artifact.artifact_id,
                data={
                    "inputs_hash": artifact.inputs_hash[:16],
                    "outputs_hash": artifact.outputs_hash[:16],
                    "signature_valid": artifact.verify(),
                },
            )
        
        # Record safety actions
        for action in result.get("safety_actions", []):
            self.audit_log.record_safety_action(
                action=action.get("action", "unknown"),
                slot=action.get("slot", "unknown"),
                reason=action.get("reason", ""),
                value_before=action.get("value_before"),
                value_after=action.get("value_after"),
            )
        
        # Record stability status
        if result.get("stability") not in ["stable", "converging"]:
            self.audit_log.record(
                EventType.SAFETY_ALERT,
                f"Stability warning: {result.get('stability')}",
                level=AuditLevel.WARNING,
                data={"stability_status": result.get("stability")},
            )
        
        return result
    
    def get_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        return self.audit_log.generate_audit_report()
    
    def get_merkle_root(self) -> str:
        """Get current Merkle root"""
        return self.audit_log.get_merkle_root()
    
    def verify_event(self, event_id: str) -> bool:
        """Verify an event's integrity"""
        return self.audit_log.verify_event(event_id)
    
    def get_proof(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get Merkle proof for an event"""
        return self.audit_log.get_proof(event_id)
    
    def export_audit_log(self, filepath: str) -> None:
        """Export audit log to JSONL"""
        self.audit_log.export_jsonl(filepath)
    
    def export_merkle_tree(self, filepath: str) -> None:
        """Export Merkle tree to JSON"""
        self.audit_log.export_merkle_json(filepath)
    
    @property
    def states(self) -> List[WorldState]:
        """Access simulation states"""
        return self.inner_engine.states
    
    @property
    def artifacts(self):
        """Access simulation artifacts"""
        return self.inner_engine.artifacts


# ============================================================================
# QUICK AUDITED SIMULATION
# ============================================================================

def create_audited_simulation(
    name: str,
    initial_values: Dict[str, float],
    feedback_rules: Dict[str, Dict[str, float]],
    transfer_rules: Optional[Dict[str, Dict[str, float]]] = None,
    num_ticks: int = 10,
    params: Optional[FeedbackParams] = None,
) -> AuditedFeedbackEngine:
    """
    Create an audited feedback simulation.
    
    Usage:
        engine = create_audited_simulation(
            name="Budget Model",
            initial_values={"Budget": 1000000, "Efficiency": 0.85},
            feedback_rules={
                "Budget": {"Budget": 0.95, "Production": 0.1}
            },
            transfer_rules={
                "Production": {"Budget": 0.85}
            },
            num_ticks=10,
        )
        
        results = engine.run()
        print(f"Merkle Root: {engine.get_merkle_root()}")
    """
    # Create slots
    slots = [
        Slot(name=name, value=value)
        for name, value in initial_values.items()
    ]
    
    # Create transfer functions
    transfers = []
    if transfer_rules:
        for output, coeffs in transfer_rules.items():
            transfers.append(TransferFunction(
                name=f"compute_{output}",
                output_slot=output,
                input_slots=list(coeffs.keys()),
                coefficients=coeffs,
            ))
    
    # Create feedback edges
    edges = []
    for target, coeffs in feedback_rules.items():
        edges.append(FeedbackEdge(
            name=f"feedback_{target}",
            target_slot=target,
            source_slots=list(coeffs.keys()),
            coefficients=coeffs,
        ))
    
    # Create config
    config = SimulationConfig(
        name=name,
        t_start=0,
        t_end=num_ticks,
        initial_slots=slots,
        transfer_functions=transfers,
        feedback_edges=edges,
        params=params or FeedbackParams(),
    )
    
    return AuditedFeedbackEngine(config)
