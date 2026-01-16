"""
============================================================================
CHE·NU™ V69 — SECURITY MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_POST_QUANTUM_SECURITY.md, CHE-NU_IMMUTABLE_AUDIT_LOGS.md,
       CHE-NU_XR_BLOCKCHAIN_VERIFICATION.md
Principle: GOUVERNANCE > EXÉCUTION

"Every meaningful event produces an immutable trace."
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import uuid
import hashlib
import json


# ============================================================================
# CRYPTOGRAPHY ENUMS
# ============================================================================

class SignatureAlgorithm(str, Enum):
    """
    Signature algorithms.
    
    Per spec: Ed25519, CRYSTALS-Dilithium, Falcon, Hybrid
    """
    ED25519 = "ed25519"  # Classical
    DILITHIUM = "dilithium"  # Post-quantum
    FALCON = "falcon"  # Post-quantum
    HYBRID = "hybrid"  # Ed25519 + PQ


class SecurityLevel(str, Enum):
    """Security levels for client configuration"""
    STANDARD = "standard"  # Classical only
    HIGH = "high"  # Hybrid
    QUANTUM_SAFE = "quantum_safe"  # PQ only


# ============================================================================
# SIGNATURE MODELS
# ============================================================================

@dataclass
class Signature:
    """A cryptographic signature"""
    signature_id: str
    algorithm: SignatureAlgorithm
    
    # Signature data
    signature_bytes: str  # Base64 encoded
    public_key_ref: str
    
    # Metadata
    signed_at: datetime = field(default_factory=datetime.utcnow)
    
    # For hybrid
    classical_signature: Optional[str] = None
    pq_signature: Optional[str] = None


@dataclass
class KeyPair:
    """A cryptographic key pair"""
    key_id: str
    algorithm: SignatureAlgorithm
    
    # Keys (mock - in production use actual crypto)
    public_key: str
    private_key_ref: str  # Reference only, never exposed
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


# ============================================================================
# AUDIT LOG MODELS
# ============================================================================

class EventType(str, Enum):
    """
    Types of logged events.
    
    Per spec logged events
    """
    WORLD_ENGINE_STEP = "world_engine_step"
    RANDOM_SEED = "random_seed"
    SCENARIO_BRANCH = "scenario_branch"
    OPA_DECISION = "opa_decision"
    XR_PACK_GENERATION = "xr_pack_generation"
    SIGNATURE = "signature"
    ARTIFACT_CREATION = "artifact_creation"
    INTERVENTION = "intervention"


@dataclass
class AuditEvent:
    """
    An audit event.
    
    Per spec: Every meaningful event produces an immutable trace
    """
    event_id: str
    event_type: EventType
    
    # Event data
    timestamp: datetime
    actor_id: str
    action: str
    
    # Payload
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # Hash
    event_hash: str = ""
    previous_hash: str = ""


@dataclass
class MerkleNode:
    """A node in a Merkle tree"""
    node_hash: str
    left_hash: Optional[str] = None
    right_hash: Optional[str] = None
    is_leaf: bool = False
    data_ref: Optional[str] = None


@dataclass
class MerkleTree:
    """
    Merkle tree for audit log integrity.
    
    Per spec: Merkle Tree per Simulation Run
    """
    tree_id: str
    root_hash: str
    
    # Nodes
    nodes: List[MerkleNode] = field(default_factory=list)
    leaf_count: int = 0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    anchored: bool = False
    anchor_ref: str = ""


@dataclass
class AuditProof:
    """
    Proof for audit verification.
    
    Per spec outputs: audit_proof.pdf (human-readable)
    """
    proof_id: str
    simulation_id: str
    
    # Merkle proof
    merkle_root: str
    proof_path: List[str] = field(default_factory=list)
    
    # Summary
    event_count: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Signature
    signature: str = ""


# ============================================================================
# XR VERIFICATION MODELS
# ============================================================================

@dataclass
class XRChunk:
    """
    An XR chunk for verification.
    
    Per spec: Each XR frame/chunk is cryptographically anchored
    """
    chunk_id: str
    frame_number: int
    
    # Content hash
    content_hash: str
    
    # Verification
    merkle_proof: List[str] = field(default_factory=list)
    verified: bool = False


@dataclass
class XRIntegrityProof:
    """
    Integrity proof for XR visualization.
    
    Per spec: Frame-level integrity proofs
    """
    proof_id: str
    session_id: str
    
    # Chunks
    chunk_hashes: List[str] = field(default_factory=list)
    merkle_root: str = ""
    
    # Anchor
    anchored_at: Optional[datetime] = None
    ledger_ref: str = ""
    
    # Signature
    signature: str = ""


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def compute_sha256(data: Any) -> str:
    """
    Compute SHA-256 hash.
    
    Per spec: Event Hashing (SHA-256)
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def compute_merkle_hash(left: str, right: str) -> str:
    """Compute Merkle node hash from children"""
    combined = left + right
    return compute_sha256(combined)


def mock_pq_sign(data: str, algorithm: SignatureAlgorithm) -> str:
    """
    Mock post-quantum signature.
    
    In production: Use actual PQ crypto library
    """
    prefix = {
        SignatureAlgorithm.DILITHIUM: "DIL",
        SignatureAlgorithm.FALCON: "FAL",
        SignatureAlgorithm.ED25519: "ED2",
        SignatureAlgorithm.HYBRID: "HYB",
    }
    return f"{prefix.get(algorithm, 'UNK')}_{compute_sha256(data)[:32]}"


def mock_pq_verify(data: str, signature: str, algorithm: SignatureAlgorithm) -> bool:
    """Mock post-quantum verification"""
    expected = mock_pq_sign(data, algorithm)
    return signature == expected
