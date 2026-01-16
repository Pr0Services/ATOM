"""
============================================================================
CHE·NU™ V69 — SECURITY MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_POST_QUANTUM_SECURITY.md
- CHE-NU_IMMUTABLE_AUDIT_LOGS.md
- CHE-NU_XR_BLOCKCHAIN_VERIFICATION.md

"Every meaningful event produces an immutable trace."

Principle: GOUVERNANCE > EXÉCUTION
Value: Future-proof security, Investor trust, Regulatory readiness
============================================================================
"""

# Models
from .models import (
    Signature,
    SignatureAlgorithm,
    SecurityLevel,
    KeyPair,
    AuditEvent,
    EventType,
    MerkleNode,
    MerkleTree,
    AuditProof,
    XRChunk,
    XRIntegrityProof,
    generate_id,
    compute_sha256,
    compute_merkle_hash,
    mock_pq_sign,
    mock_pq_verify,
)

# Post-Quantum Security
from .post_quantum import (
    PostQuantumSecuritySystem,
    KeyManager,
    SignatureService,
    SecurityConfigurator,
    create_security_system,
    create_key_manager,
)

# Audit Logs
from .audit_logs import (
    ImmutableAuditSystem,
    EventLogger,
    MerkleTreeBuilder,
    create_audit_system,
)

# XR Verification
from .xr_verification import (
    XRBlockchainVerificationSystem,
    LightweightLedger,
    XRChunkHasher,
    XRIntegrityVerifier,
    create_xr_verification_system,
    create_ledger,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "Signature", "SignatureAlgorithm", "SecurityLevel", "KeyPair",
    "AuditEvent", "EventType", "MerkleNode", "MerkleTree", "AuditProof",
    "XRChunk", "XRIntegrityProof",
    "generate_id", "compute_sha256", "compute_merkle_hash",
    "mock_pq_sign", "mock_pq_verify",
    # Post-Quantum
    "PostQuantumSecuritySystem", "KeyManager", "SignatureService",
    "SecurityConfigurator", "create_security_system", "create_key_manager",
    # Audit
    "ImmutableAuditSystem", "EventLogger", "MerkleTreeBuilder",
    "create_audit_system",
    # XR Verification
    "XRBlockchainVerificationSystem", "LightweightLedger",
    "XRChunkHasher", "XRIntegrityVerifier",
    "create_xr_verification_system", "create_ledger",
]
