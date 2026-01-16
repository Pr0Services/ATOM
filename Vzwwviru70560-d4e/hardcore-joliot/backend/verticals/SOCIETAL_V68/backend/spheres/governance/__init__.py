"""
CHE·NU V68 Governance Module
Consensus Liquide - La fin de la politique de confrontation

La democratie comme un flux:
- Chaque voix est une goutte
- Ensemble, elles forment le courant
- Le consensus emerge naturellement

GOVERNANCE COMPLIANCE:
- Rule #1: High impact decisions require APPROVAL
- Rule #5: Proposals CHRONOLOGICAL, no ranking
- Rule #6: Full audit trail (anonymized)
"""

from .agents.consensus_liquide_agent import (
    ConsensusLiquideAgent,
    get_consensus_liquide_agent,
    # Enums
    ProposalCategory,
    ProposalScope,
    ProposalStatus,
    VoteType,
    ConsensusLevel,
    ImpactLevel,
    ParticipantRole,
    # Data models
    GeoZone,
    Proposal,
    Vote,
    CounterProposal,
    ConsensusResult,
    DeliberationSession,
    GovernanceMetrics,
)

__all__ = [
    # Main agent
    "ConsensusLiquideAgent",
    "get_consensus_liquide_agent",
    # Enums
    "ProposalCategory",
    "ProposalScope",
    "ProposalStatus",
    "VoteType",
    "ConsensusLevel",
    "ImpactLevel",
    "ParticipantRole",
    # Data models
    "GeoZone",
    "Proposal",
    "Vote",
    "CounterProposal",
    "ConsensusResult",
    "DeliberationSession",
    "GovernanceMetrics",
]

__version__ = "68.0.0"
__module__ = "Consensus Liquide"
