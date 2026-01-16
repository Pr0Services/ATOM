"""
============================================================================
CHE·NU™ V69 — IMMUTABLE AUDIT LOGS
============================================================================
Spec: GPT1/CHE-NU_IMMUTABLE_AUDIT_LOGS.md

Purpose: Provide cryptographic, tamper-proof proof that all simulations
and decisions are governed, deterministic, and non-manipulated.

Core Principle: Every meaningful event produces an immutable trace.

Architecture:
- Event Hashing (SHA-256)
- Merkle Tree per Simulation Run
- Daily Root Anchoring
- Read-only verification for auditors

Outputs: audit_log.jsonl, merkle_root.json, audit_proof.pdf
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import json
import math

from ..models import (
    AuditEvent,
    EventType,
    MerkleNode,
    MerkleTree,
    AuditProof,
    generate_id,
    compute_sha256,
    compute_merkle_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# EVENT LOGGER
# ============================================================================

class EventLogger:
    """
    Log audit events.
    
    Per spec: Every meaningful event produces an immutable trace
    """
    
    def __init__(self):
        self._events: List[AuditEvent] = []
        self._previous_hash = "genesis"
    
    def log_event(
        self,
        event_type: EventType,
        actor_id: str,
        action: str,
        payload: Dict[str, Any] = None,
    ) -> AuditEvent:
        """Log a new event"""
        event = AuditEvent(
            event_id=generate_id(),
            event_type=event_type,
            timestamp=datetime.utcnow(),
            actor_id=actor_id,
            action=action,
            payload=payload or {},
            previous_hash=self._previous_hash,
        )
        
        # Compute event hash (chain)
        event.event_hash = compute_sha256({
            "event_id": event.event_id,
            "type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "actor": event.actor_id,
            "action": event.action,
            "payload": event.payload,
            "previous": event.previous_hash,
        })
        
        self._previous_hash = event.event_hash
        self._events.append(event)
        
        logger.debug(f"Logged event {event.event_id}: {event.event_type.value}")
        return event
    
    def log_world_engine_step(
        self,
        step_id: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
    ) -> AuditEvent:
        """
        Log WorldEngine step execution.
        
        Per spec logged event: WorldEngine step execution
        """
        return self.log_event(
            EventType.WORLD_ENGINE_STEP,
            "world_engine",
            f"step_{step_id}",
            {"inputs": inputs, "outputs": outputs},
        )
    
    def log_random_seed(
        self,
        seed: int,
        purpose: str,
    ) -> AuditEvent:
        """
        Log random seed usage.
        
        Per spec logged event: Random seed usage
        """
        return self.log_event(
            EventType.RANDOM_SEED,
            "system",
            "seed_usage",
            {"seed": seed, "purpose": purpose},
        )
    
    def log_scenario_branch(
        self,
        branch_id: str,
        parent_id: str,
        condition: str,
    ) -> AuditEvent:
        """
        Log scenario branching.
        
        Per spec logged event: Scenario branching
        """
        return self.log_event(
            EventType.SCENARIO_BRANCH,
            "scenario_engine",
            f"branch_{branch_id}",
            {"parent": parent_id, "condition": condition},
        )
    
    def log_opa_decision(
        self,
        policy: str,
        decision: str,
        reason: str,
    ) -> AuditEvent:
        """
        Log OPA decisions.
        
        Per spec logged event: OPA decisions (allow/deny)
        """
        return self.log_event(
            EventType.OPA_DECISION,
            "opa",
            decision,
            {"policy": policy, "reason": reason},
        )
    
    def log_xr_pack(
        self,
        pack_id: str,
        signature: str,
    ) -> AuditEvent:
        """
        Log XR pack generation.
        
        Per spec logged event: XR pack generation & signature
        """
        return self.log_event(
            EventType.XR_PACK_GENERATION,
            "xr_engine",
            f"pack_{pack_id}",
            {"signature": signature},
        )
    
    def get_events(self) -> List[AuditEvent]:
        """Get all events"""
        return self._events
    
    def get_events_by_type(
        self,
        event_type: EventType,
    ) -> List[AuditEvent]:
        """Get events by type"""
        return [e for e in self._events if e.event_type == event_type]
    
    def export_jsonl(self) -> str:
        """
        Export to JSONL format.
        
        Per spec output: audit_log.jsonl
        """
        lines = []
        for event in self._events:
            line = json.dumps({
                "event_id": event.event_id,
                "type": event.event_type.value,
                "timestamp": event.timestamp.isoformat(),
                "actor": event.actor_id,
                "action": event.action,
                "payload": event.payload,
                "hash": event.event_hash,
                "previous": event.previous_hash,
            }, sort_keys=True)
            lines.append(line)
        return "\n".join(lines)


# ============================================================================
# MERKLE TREE BUILDER
# ============================================================================

class MerkleTreeBuilder:
    """
    Build Merkle trees for audit integrity.
    
    Per spec: Merkle Tree per Simulation Run
    """
    
    def build_tree(
        self,
        events: List[AuditEvent],
    ) -> MerkleTree:
        """Build Merkle tree from events"""
        if not events:
            return MerkleTree(
                tree_id=generate_id(),
                root_hash="empty",
            )
        
        # Create leaf nodes
        leaves = []
        for event in events:
            node = MerkleNode(
                node_hash=event.event_hash,
                is_leaf=True,
                data_ref=event.event_id,
            )
            leaves.append(node)
        
        # Pad to power of 2
        while len(leaves) & (len(leaves) - 1) != 0:
            leaves.append(MerkleNode(
                node_hash=compute_sha256("padding"),
                is_leaf=True,
            ))
        
        # Build tree bottom-up
        all_nodes = leaves.copy()
        current_level = leaves
        
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                
                parent = MerkleNode(
                    node_hash=compute_merkle_hash(left.node_hash, right.node_hash),
                    left_hash=left.node_hash,
                    right_hash=right.node_hash,
                )
                next_level.append(parent)
                all_nodes.append(parent)
            
            current_level = next_level
        
        root_hash = current_level[0].node_hash if current_level else "empty"
        
        tree = MerkleTree(
            tree_id=generate_id(),
            root_hash=root_hash,
            nodes=all_nodes,
            leaf_count=len(events),
        )
        
        logger.info(f"Built Merkle tree {tree.tree_id} with {len(events)} events")
        return tree
    
    def get_proof_path(
        self,
        tree: MerkleTree,
        event_hash: str,
    ) -> List[str]:
        """Get Merkle proof path for an event"""
        # Find the leaf
        leaf_idx = None
        leaves = [n for n in tree.nodes if n.is_leaf]
        
        for i, node in enumerate(leaves):
            if node.node_hash == event_hash:
                leaf_idx = i
                break
        
        if leaf_idx is None:
            return []
        
        # Build proof path
        proof = []
        idx = leaf_idx
        level_size = len(leaves)
        
        while level_size > 1:
            sibling_idx = idx ^ 1  # XOR to get sibling
            if sibling_idx < level_size:
                proof.append(leaves[sibling_idx].node_hash)
            
            idx //= 2
            level_size //= 2
        
        return proof
    
    def verify_proof(
        self,
        event_hash: str,
        proof_path: List[str],
        root_hash: str,
    ) -> bool:
        """Verify a Merkle proof"""
        current = event_hash
        
        for sibling in proof_path:
            # Try both orderings
            hash1 = compute_merkle_hash(current, sibling)
            hash2 = compute_merkle_hash(sibling, current)
            
            if hash1 == root_hash or hash2 == root_hash:
                return True
            
            # Use lexicographic ordering
            if current < sibling:
                current = compute_merkle_hash(current, sibling)
            else:
                current = compute_merkle_hash(sibling, current)
        
        return current == root_hash


# ============================================================================
# AUDIT SYSTEM
# ============================================================================

class ImmutableAuditSystem:
    """
    Main immutable audit system.
    
    Per spec value: Investor trust, Regulatory readiness, Proof of non-manipulation
    """
    
    def __init__(self):
        self.logger = EventLogger()
        self.merkle = MerkleTreeBuilder()
        self._trees: Dict[str, MerkleTree] = {}
        self._anchors: List[Dict[str, Any]] = []
    
    def log(
        self,
        event_type: EventType,
        actor_id: str,
        action: str,
        payload: Dict[str, Any] = None,
    ) -> AuditEvent:
        """Log an event"""
        return self.logger.log_event(event_type, actor_id, action, payload)
    
    def finalize_simulation(
        self,
        simulation_id: str,
    ) -> MerkleTree:
        """
        Finalize simulation and build Merkle tree.
        
        Per spec: Merkle Tree per Simulation Run
        """
        events = self.logger.get_events()
        tree = self.merkle.build_tree(events)
        self._trees[simulation_id] = tree
        
        logger.info(f"Finalized simulation {simulation_id}: root={tree.root_hash[:16]}...")
        return tree
    
    def anchor_daily(self) -> Dict[str, Any]:
        """
        Anchor daily roots.
        
        Per spec: Daily Root Anchoring
        """
        anchor = {
            "anchor_id": generate_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "roots": {sid: tree.root_hash for sid, tree in self._trees.items()},
            "master_root": compute_sha256(
                "".join(sorted(t.root_hash for t in self._trees.values()))
            ),
        }
        
        self._anchors.append(anchor)
        
        # Mark trees as anchored
        for tree in self._trees.values():
            tree.anchored = True
            tree.anchor_ref = anchor["anchor_id"]
        
        logger.info(f"Daily anchor created: {anchor['anchor_id']}")
        return anchor
    
    def generate_proof(
        self,
        simulation_id: str,
    ) -> AuditProof:
        """
        Generate audit proof.
        
        Per spec output: audit_proof.pdf (human-readable)
        """
        tree = self._trees.get(simulation_id)
        if not tree:
            raise ValueError(f"No tree for simulation {simulation_id}")
        
        events = self.logger.get_events()
        
        proof = AuditProof(
            proof_id=generate_id(),
            simulation_id=simulation_id,
            merkle_root=tree.root_hash,
            event_count=len(events),
            start_time=events[0].timestamp if events else None,
            end_time=events[-1].timestamp if events else None,
        )
        
        # Sign proof
        proof.signature = compute_sha256({
            "proof_id": proof.proof_id,
            "root": proof.merkle_root,
            "count": proof.event_count,
        })
        
        return proof
    
    def verify_event(
        self,
        simulation_id: str,
        event_hash: str,
    ) -> bool:
        """
        Verify an event is in the audit log.
        
        Per spec: Read-only verification for auditors
        """
        tree = self._trees.get(simulation_id)
        if not tree:
            return False
        
        proof_path = self.merkle.get_proof_path(tree, event_hash)
        return self.merkle.verify_proof(event_hash, proof_path, tree.root_hash)
    
    def export_audit_log(self) -> str:
        """Export audit log to JSONL"""
        return self.logger.export_jsonl()
    
    def export_merkle_root(
        self,
        simulation_id: str,
    ) -> Dict[str, Any]:
        """
        Export Merkle root.
        
        Per spec output: merkle_root.json
        """
        tree = self._trees.get(simulation_id)
        if not tree:
            return {}
        
        return {
            "simulation_id": simulation_id,
            "tree_id": tree.tree_id,
            "root_hash": tree.root_hash,
            "leaf_count": tree.leaf_count,
            "created_at": tree.created_at.isoformat(),
            "anchored": tree.anchored,
            "anchor_ref": tree.anchor_ref,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_audit_system() -> ImmutableAuditSystem:
    """Create immutable audit system"""
    return ImmutableAuditSystem()
