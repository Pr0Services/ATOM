"""
CHE·NU™ — Quantum Module
========================
Quantum orchestration for intelligent compute routing.

Components:
- QuantumOrchestrator: Routes between classical/photonic/quantum
- QKDKeyManager: Quantum key distribution for secure channels
- SensorSynchronizer: Photonic sensor synchronization

Principle: User never asks for quantum.
System uses it only when necessary, invisibly.
"""

from .quantum_orchestrator import (
    QuantumOrchestrator,
    ComputeType,
    ComputePriority,
    HubIntegration,
    ComputeCapability,
    ComputeRequest,
    ComputeResult,
    RoutingDecision,
    ComputeBackend,
    QKDKeyManager,
    SensorSynchronizer,
    get_quantum_orchestrator
)

__all__ = [
    "QuantumOrchestrator",
    "ComputeType",
    "ComputePriority",
    "HubIntegration",
    "ComputeCapability",
    "ComputeRequest",
    "ComputeResult",
    "RoutingDecision",
    "ComputeBackend",
    "QKDKeyManager",
    "SensorSynchronizer",
    "get_quantum_orchestrator"
]
