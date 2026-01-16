"""
============================================================================
CHE·NU™ V69 — IMMUTABLE AUDIT SYSTEM
============================================================================
Version: 1.0.0
Purpose: Cryptographic, tamper-proof audit trail with Merkle Tree
Principle: Every meaningful event produces an immutable trace

The Audit System provides:
- Event logging with cryptographic hashing
- Merkle Tree for efficient integrity verification
- Daily root anchoring for external verification
- Proof generation for individual events

Usage:
    from audit import AuditLog, EventType
    
    log = AuditLog(simulation_id="sim-001")
    
    log.record(
        EventType.SIMULATION_START,
        "Simulation started",
        data={"t_start": 0, "t_end": 10}
    )
    
    # Finalize and get Merkle root
    root = log.finalize()
    
    # Generate audit report
    report = log.generate_audit_report()
    
    # Verify event inclusion
    is_valid = log.verify_event(event_id)
============================================================================
"""

# Logs
from .logs import (
    # Enums
    EventType,
    AuditLevel,
    # Models
    AuditEvent,
    MerkleNode,
    MerkleTree,
    AuditLog,
    DailyAnchor,
    AuditManager,
    get_audit_manager,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Enums
    "EventType",
    "AuditLevel",
    # Models
    "AuditEvent",
    "MerkleNode",
    "MerkleTree",
    "AuditLog",
    "DailyAnchor",
    "AuditManager",
    "get_audit_manager",
]
