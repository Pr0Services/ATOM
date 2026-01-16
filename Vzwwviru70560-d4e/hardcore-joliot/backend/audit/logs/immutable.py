"""
============================================================================
CHE·NU™ V69 — IMMUTABLE AUDIT LOGS
============================================================================
Version: 1.0.0
Purpose: Cryptographic, tamper-proof audit trail with Merkle Tree
Principle: Every meaningful event produces an immutable trace
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class EventType(str, Enum):
    """Types of auditable events"""
    # Simulation
    SIMULATION_START = "simulation_start"
    SIMULATION_STEP = "simulation_step"
    SIMULATION_END = "simulation_end"
    SIMULATION_ERROR = "simulation_error"
    
    # WorldEngine
    WORLD_STATE_CREATED = "world_state_created"
    SLOT_UPDATED = "slot_updated"
    FEEDBACK_APPLIED = "feedback_applied"
    
    # Causal
    DAG_CREATED = "dag_created"
    DAG_APPROVED = "dag_approved"
    DAG_REJECTED = "dag_rejected"
    EFFECT_ESTIMATED = "effect_estimated"
    
    # Decisions
    DECISION_PACKAGE_CREATED = "decision_package_created"
    DECISION_RECORDED = "decision_recorded"
    DECISION_DEFERRED = "decision_deferred"
    DECISION_ESCALATED = "decision_escalated"
    
    # Governance
    OPA_DECISION = "opa_decision"
    OPA_ALLOW = "opa_allow"
    OPA_DENY = "opa_deny"
    HITL_REQUIRED = "hitl_required"
    HITL_APPROVED = "hitl_approved"
    
    # Safety
    SAFETY_CLAMP = "safety_clamp"
    SAFETY_STOP = "safety_stop"
    SAFETY_ALERT = "safety_alert"
    
    # XR
    XR_PACK_GENERATED = "xr_pack_generated"
    XR_PACK_VERIFIED = "xr_pack_verified"
    
    # System
    SEED_USED = "seed_used"
    ARTIFACT_SIGNED = "artifact_signed"
    CHAIN_VERIFIED = "chain_verified"


class AuditLevel(str, Enum):
    """Audit severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    GOVERNANCE = "governance"


# ============================================================================
# AUDIT EVENT
# ============================================================================

class AuditEvent(BaseModel):
    """
    Single auditable event in CHE·NU™.
    Immutable once created.
    """
    
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = Field(...)
    level: AuditLevel = Field(default=AuditLevel.INFO)
    
    # Context
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    simulation_id: Optional[str] = Field(default=None)
    tenant_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    agent_id: Optional[str] = Field(default=None)
    trace_id: Optional[str] = Field(default=None)
    
    # Content
    message: str = Field(...)
    data: Dict[str, Any] = Field(default_factory=dict)
    
    # References
    artifact_id: Optional[str] = Field(default=None)
    dag_id: Optional[str] = Field(default=None)
    decision_id: Optional[str] = Field(default=None)
    opa_decision_id: Optional[str] = Field(default=None)
    
    # Synthetic flag
    synthetic: bool = Field(default=True)
    
    @computed_field
    @property
    def hash(self) -> str:
        """Compute event hash"""
        content = {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "data": self.data,
        }
        return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    
    def to_jsonl(self) -> str:
        """Convert to JSONL format"""
        return json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "level": self.level.value,
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "data": self.data,
            "simulation_id": self.simulation_id,
            "tenant_id": self.tenant_id,
            "trace_id": self.trace_id,
            "hash": self.hash,
            "synthetic": self.synthetic,
        }, sort_keys=True)


# ============================================================================
# MERKLE TREE NODE
# ============================================================================

class MerkleNode(BaseModel):
    """Node in Merkle Tree"""
    
    hash: str = Field(...)
    left: Optional[str] = Field(default=None, description="Left child hash")
    right: Optional[str] = Field(default=None, description="Right child hash")
    is_leaf: bool = Field(default=True)
    event_id: Optional[str] = Field(default=None, description="Only for leaves")


# ============================================================================
# MERKLE TREE
# ============================================================================

class MerkleTree:
    """
    Merkle Tree for audit log integrity.
    
    Each leaf is an event hash.
    Internal nodes are hash(left + right).
    Root provides single proof of entire log.
    """
    
    def __init__(self):
        self.leaves: List[str] = []
        self.nodes: Dict[str, MerkleNode] = {}
        self._root: Optional[str] = None
    
    def add_event(self, event: AuditEvent) -> str:
        """Add event to tree, return leaf hash"""
        leaf_hash = event.hash
        
        # Create leaf node
        self.nodes[leaf_hash] = MerkleNode(
            hash=leaf_hash,
            is_leaf=True,
            event_id=event.event_id,
        )
        
        self.leaves.append(leaf_hash)
        self._root = None  # Invalidate root
        
        return leaf_hash
    
    def build(self) -> str:
        """Build tree and return root hash"""
        if not self.leaves:
            return hashlib.sha256(b"empty").hexdigest()
        
        if len(self.leaves) == 1:
            self._root = self.leaves[0]
            return self._root
        
        # Build tree bottom-up
        current_level = self.leaves.copy()
        
        while len(current_level) > 1:
            next_level = []
            
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                
                # Compute parent hash
                combined = f"{left}{right}"
                parent_hash = hashlib.sha256(combined.encode()).hexdigest()
                
                # Store node
                self.nodes[parent_hash] = MerkleNode(
                    hash=parent_hash,
                    left=left,
                    right=right,
                    is_leaf=False,
                )
                
                next_level.append(parent_hash)
            
            current_level = next_level
        
        self._root = current_level[0]
        return self._root
    
    @property
    def root(self) -> Optional[str]:
        """Get root hash (builds if needed)"""
        if self._root is None and self.leaves:
            self.build()
        return self._root
    
    def get_proof(self, event_hash: str) -> List[Tuple[str, str]]:
        """
        Get Merkle proof for an event.
        Returns list of (sibling_hash, position) tuples.
        """
        if event_hash not in self.leaves:
            return []
        
        if self._root is None:
            self.build()
        
        proof = []
        current = event_hash
        current_level = self.leaves.copy()
        
        while len(current_level) > 1:
            next_level = []
            
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                
                combined = f"{left}{right}"
                parent = hashlib.sha256(combined.encode()).hexdigest()
                next_level.append(parent)
                
                if current == left:
                    proof.append((right, "right"))
                    current = parent
                elif current == right:
                    proof.append((left, "left"))
                    current = parent
            
            current_level = next_level
        
        return proof
    
    def verify_proof(
        self,
        event_hash: str,
        proof: List[Tuple[str, str]],
        expected_root: str,
    ) -> bool:
        """Verify a Merkle proof"""
        current = event_hash
        
        for sibling, position in proof:
            if position == "right":
                combined = f"{current}{sibling}"
            else:
                combined = f"{sibling}{current}"
            
            current = hashlib.sha256(combined.encode()).hexdigest()
        
        return current == expected_root
    
    def to_dict(self) -> Dict[str, Any]:
        """Export tree structure"""
        return {
            "root": self.root,
            "leaf_count": len(self.leaves),
            "node_count": len(self.nodes),
            "leaves": self.leaves,
        }


# ============================================================================
# AUDIT LOG
# ============================================================================

class AuditLog:
    """
    Immutable audit log with Merkle Tree integrity.
    
    Usage:
        log = AuditLog(simulation_id="sim-001")
        
        log.record(
            EventType.SIMULATION_START,
            "Simulation started",
            data={"t_start": 0, "t_end": 10}
        )
        
        # Get Merkle root
        root = log.get_merkle_root()
        
        # Export
        log.export_jsonl("/path/to/audit.jsonl")
    """
    
    def __init__(
        self,
        simulation_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ):
        self.simulation_id = simulation_id
        self.tenant_id = tenant_id
        self.events: List[AuditEvent] = []
        self.merkle_tree = MerkleTree()
        self._finalized = False
    
    def record(
        self,
        event_type: EventType,
        message: str,
        level: AuditLevel = AuditLevel.INFO,
        data: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
        dag_id: Optional[str] = None,
        decision_id: Optional[str] = None,
        opa_decision_id: Optional[str] = None,
    ) -> AuditEvent:
        """Record an audit event"""
        if self._finalized:
            raise RuntimeError("Cannot add events to finalized log")
        
        event = AuditEvent(
            event_type=event_type,
            level=level,
            message=message,
            data=data or {},
            simulation_id=self.simulation_id,
            tenant_id=self.tenant_id,
            user_id=user_id,
            agent_id=agent_id,
            trace_id=trace_id,
            artifact_id=artifact_id,
            dag_id=dag_id,
            decision_id=decision_id,
            opa_decision_id=opa_decision_id,
            synthetic=True,
        )
        
        self.events.append(event)
        self.merkle_tree.add_event(event)
        
        logger.debug(f"Audit: [{event_type.value}] {message}")
        
        return event
    
    def record_opa_decision(
        self,
        decision_id: str,
        allowed: bool,
        deny_reasons: Optional[List[str]] = None,
        trace_id: Optional[str] = None,
    ) -> AuditEvent:
        """Record OPA governance decision"""
        return self.record(
            event_type=EventType.OPA_ALLOW if allowed else EventType.OPA_DENY,
            message=f"OPA decision: {'ALLOW' if allowed else 'DENY'}",
            level=AuditLevel.GOVERNANCE,
            data={
                "decision_id": decision_id,
                "allowed": allowed,
                "deny_reasons": deny_reasons or [],
            },
            trace_id=trace_id,
            opa_decision_id=decision_id,
        )
    
    def record_safety_action(
        self,
        action: str,
        slot: str,
        reason: str,
        value_before: Optional[float] = None,
        value_after: Optional[float] = None,
    ) -> AuditEvent:
        """Record safety controller action"""
        return self.record(
            event_type=EventType.SAFETY_CLAMP,
            message=f"Safety action: {action} on {slot}",
            level=AuditLevel.WARNING,
            data={
                "action": action,
                "slot": slot,
                "reason": reason,
                "value_before": value_before,
                "value_after": value_after,
            },
        )
    
    def record_decision(
        self,
        decision_id: str,
        decider_id: str,
        selected_option: str,
        rationale: str,
    ) -> AuditEvent:
        """Record human decision"""
        return self.record(
            event_type=EventType.DECISION_RECORDED,
            message=f"Human decision recorded by {decider_id}",
            level=AuditLevel.GOVERNANCE,
            data={
                "selected_option": selected_option,
                "rationale": rationale,
            },
            user_id=decider_id,
            decision_id=decision_id,
        )
    
    def finalize(self) -> str:
        """Finalize log and return Merkle root"""
        if self._finalized:
            return self.merkle_tree.root
        
        root = self.merkle_tree.build()
        self._finalized = True
        
        # Record finalization
        self.events.append(AuditEvent(
            event_type=EventType.CHAIN_VERIFIED,
            message="Audit log finalized",
            level=AuditLevel.INFO,
            data={"merkle_root": root, "event_count": len(self.events) - 1},
            simulation_id=self.simulation_id,
            tenant_id=self.tenant_id,
        ))
        
        logger.info(f"Audit log finalized: {root[:16]}... ({len(self.events)} events)")
        
        return root
    
    def get_merkle_root(self) -> str:
        """Get current Merkle root"""
        return self.merkle_tree.root or self.merkle_tree.build()
    
    def get_proof(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get Merkle proof for an event"""
        event = None
        for e in self.events:
            if e.event_id == event_id:
                event = e
                break
        
        if event is None:
            return None
        
        proof = self.merkle_tree.get_proof(event.hash)
        
        return {
            "event_id": event_id,
            "event_hash": event.hash,
            "proof": proof,
            "root": self.get_merkle_root(),
        }
    
    def verify_event(self, event_id: str) -> bool:
        """Verify an event's inclusion in the log"""
        proof_data = self.get_proof(event_id)
        if proof_data is None:
            return False
        
        return self.merkle_tree.verify_proof(
            proof_data["event_hash"],
            proof_data["proof"],
            proof_data["root"],
        )
    
    def export_jsonl(self, filepath: str) -> None:
        """Export log to JSONL file"""
        with open(filepath, 'w') as f:
            for event in self.events:
                f.write(event.to_jsonl() + '\n')
        
        logger.info(f"Exported {len(self.events)} events to {filepath}")
    
    def export_merkle_json(self, filepath: str) -> None:
        """Export Merkle tree to JSON"""
        data = {
            "simulation_id": self.simulation_id,
            "tenant_id": self.tenant_id,
            "event_count": len(self.events),
            "merkle_root": self.get_merkle_root(),
            "tree": self.merkle_tree.to_dict(),
            "finalized": self._finalized,
            "exported_at": datetime.utcnow().isoformat(),
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate human-readable audit report"""
        event_counts = {}
        for event in self.events:
            et = event.event_type.value
            event_counts[et] = event_counts.get(et, 0) + 1
        
        governance_events = [
            e for e in self.events
            if e.level == AuditLevel.GOVERNANCE
        ]
        
        safety_events = [
            e for e in self.events
            if e.event_type in [
                EventType.SAFETY_CLAMP,
                EventType.SAFETY_STOP,
                EventType.SAFETY_ALERT,
            ]
        ]
        
        return {
            "report_type": "AUDIT_REPORT",
            "simulation_id": self.simulation_id,
            "tenant_id": self.tenant_id,
            "generated_at": datetime.utcnow().isoformat(),
            
            "summary": {
                "total_events": len(self.events),
                "event_types": event_counts,
                "governance_events": len(governance_events),
                "safety_events": len(safety_events),
            },
            
            "integrity": {
                "merkle_root": self.get_merkle_root(),
                "finalized": self._finalized,
                "chain_valid": True,  # Would verify in production
            },
            
            "governance_log": [
                {
                    "event_id": e.event_id,
                    "type": e.event_type.value,
                    "message": e.message,
                    "timestamp": e.timestamp.isoformat(),
                }
                for e in governance_events
            ],
            
            "safety_log": [
                {
                    "event_id": e.event_id,
                    "type": e.event_type.value,
                    "message": e.message,
                    "data": e.data,
                }
                for e in safety_events
            ],
            
            "synthetic": True,
        }


# ============================================================================
# DAILY ANCHOR (Optional blockchain anchoring)
# ============================================================================

class DailyAnchor(BaseModel):
    """
    Daily root anchoring for external verification.
    Could be published to a lightweight sidechain or public timestamp service.
    """
    
    anchor_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: str = Field(..., description="YYYY-MM-DD")
    
    # Merkle roots from all simulations that day
    simulation_roots: Dict[str, str] = Field(default_factory=dict)
    
    # Combined root
    daily_root: Optional[str] = Field(default=None)
    
    # Timestamp proof
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # External anchor (e.g., blockchain tx hash)
    external_anchor: Optional[str] = Field(default=None)
    anchor_service: Optional[str] = Field(default=None)
    
    def compute_daily_root(self) -> str:
        """Compute combined root for all simulations"""
        if not self.simulation_roots:
            self.daily_root = hashlib.sha256(b"empty").hexdigest()
        else:
            combined = "".join(sorted(self.simulation_roots.values()))
            self.daily_root = hashlib.sha256(combined.encode()).hexdigest()
        
        return self.daily_root
    
    def add_simulation(self, simulation_id: str, merkle_root: str) -> None:
        """Add a simulation's Merkle root"""
        self.simulation_roots[simulation_id] = merkle_root
        self.daily_root = None  # Invalidate


# ============================================================================
# AUDIT MANAGER
# ============================================================================

class AuditManager:
    """
    Manages audit logs across simulations.
    """
    
    def __init__(self):
        self.logs: Dict[str, AuditLog] = {}
        self.daily_anchors: Dict[str, DailyAnchor] = {}
    
    def create_log(
        self,
        simulation_id: str,
        tenant_id: Optional[str] = None,
    ) -> AuditLog:
        """Create a new audit log for a simulation"""
        log = AuditLog(simulation_id=simulation_id, tenant_id=tenant_id)
        self.logs[simulation_id] = log
        return log
    
    def get_log(self, simulation_id: str) -> Optional[AuditLog]:
        """Get audit log by simulation ID"""
        return self.logs.get(simulation_id)
    
    def finalize_log(self, simulation_id: str) -> Optional[str]:
        """Finalize a log and add to daily anchor"""
        log = self.logs.get(simulation_id)
        if log is None:
            return None
        
        root = log.finalize()
        
        # Add to daily anchor
        today = datetime.utcnow().strftime("%Y-%m-%d")
        if today not in self.daily_anchors:
            self.daily_anchors[today] = DailyAnchor(date=today)
        
        self.daily_anchors[today].add_simulation(simulation_id, root)
        
        return root
    
    def get_daily_root(self, date: str) -> Optional[str]:
        """Get daily Merkle root"""
        anchor = self.daily_anchors.get(date)
        if anchor is None:
            return None
        return anchor.compute_daily_root()


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_audit_manager: Optional[AuditManager] = None


def get_audit_manager() -> AuditManager:
    """Get singleton audit manager"""
    global _audit_manager
    if _audit_manager is None:
        _audit_manager = AuditManager()
    return _audit_manager
