"""
CHE·NU™ V76 — Integration Tests
Agent A - Phase A2

Tests d'intégration pour workflows complets:
- Governance workflows (checkpoint → approval → execution)
- Cross-service identity boundary
- Nova + Agents coordination
"""

from .test_governance_workflows import (
    TestDeleteDataspaceWorkflow,
    TestNovaAgentWorkflow,
    TestThreadDecisionWorkflow,
    TestMemoryPurgeWorkflow,
    TestCrossServiceIdentity,
    TestGovernanceAuditTrail
)

__all__ = [
    "TestDeleteDataspaceWorkflow",
    "TestNovaAgentWorkflow",
    "TestThreadDecisionWorkflow",
    "TestMemoryPurgeWorkflow",
    "TestCrossServiceIdentity",
    "TestGovernanceAuditTrail"
]
