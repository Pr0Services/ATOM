"""
============================================================================
CHE·NU™ V69 — NEUROMORPHIC HUB (5 Complementary Systems)
============================================================================
Fills the gaps between existing bio-inspired systems:

1. NeuroFeedbackHub  — Centralized signal aggregation
2. AdaptivePriorityQueue — Learning-based request ordering
3. AgentConsensusProtocol — Multi-agent negotiation
4. RewardSignalEngine — Incentive learning for agents
5. RosettaBridge — TypeScript↔Python signal bridge

These systems DO NOT duplicate existing:
- NeuromorphicLattice (spike propagation) → we CONSUME its events
- SynapticGraph (module connections) → we READ its topology
- FeedbackLoopEngine (temporal simulation) → we EXTEND with real-time signals
- PlasticityWorker (threshold adjustment) → we FEED it reward data
- ThreatAmygdala (threat detection) → we AGGREGATE its alerts

Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from .feedback_hub import NeuroFeedbackHub
from .adaptive_queue import AdaptivePriorityQueue
from .consensus import AgentConsensusProtocol
from .reward_engine import RewardSignalEngine
from .rosetta_bridge import RosettaBridge

__all__ = [
    "NeuroFeedbackHub",
    "AdaptivePriorityQueue",
    "AgentConsensusProtocol",
    "RewardSignalEngine",
    "RosettaBridge",
]
