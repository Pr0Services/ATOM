"""
============================================================================
CHE·NU™ V69 — AGENT CONSENSUS PROTOCOL
============================================================================
System 3/5: Multi-agent negotiation

Problem: When multiple agents propose conflicting actions for the same
task, no system exists to negotiate and select the best action. The
orchestrator just takes the first response.

Solution: AgentConsensusProtocol implements a weighted voting mechanism
where agents propose actions, vote on each other's proposals, and the
system selects the best via confidence-weighted consensus.

Connects to:
- OrchestratorService (receives competing proposals)
- NeuroFeedbackHub (uses health context for tie-breaking)
- RewardSignalEngine (winning proposals feed back as positive reward)

Does NOT duplicate:
- SyntheticDiplomacyProtocol (that's inter-instance negotiation)
- NeuromorphicLattice.route_event (that's event routing, not decision)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum
import logging

from ..models import generate_id

logger = logging.getLogger(__name__)


class ConsensusStatus(str, Enum):
    OPEN = "open"              # Accepting proposals
    VOTING = "voting"          # Proposals locked, voting active
    RESOLVED = "resolved"      # Winner selected
    DEADLOCKED = "deadlocked"  # No clear winner, needs escalation


@dataclass
class Proposal:
    """An agent's proposed action."""
    proposal_id: str
    agent_id: str
    action: str
    confidence: float  # [0.0, 1.0]
    rationale: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Vote:
    """An agent's vote on a proposal."""
    voter_id: str
    proposal_id: str
    score: float  # [-1.0, 1.0] where negative = oppose
    reason: str = ""


@dataclass
class ConsensusRound:
    """A complete negotiation round."""
    round_id: str
    task_id: str
    sphere_id: str
    status: ConsensusStatus
    proposals: List[Proposal] = field(default_factory=list)
    votes: List[Vote] = field(default_factory=list)
    winner: Optional[Proposal] = None
    final_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None


class AgentConsensusProtocol:
    """
    Multi-agent negotiation via weighted voting.

    Flow:
    1. Open round for a task
    2. Agents submit proposals
    3. Agents vote on each other's proposals
    4. Resolve: confidence-weighted vote tally picks winner
    """

    def __init__(
        self,
        quorum_ratio: float = 0.5,
        deadlock_threshold: float = 0.1,
    ):
        self._rounds: Dict[str, ConsensusRound] = {}
        self._quorum_ratio = quorum_ratio
        self._deadlock_threshold = deadlock_threshold

        # Agent reputation (learned over time)
        self._reputation: Dict[str, float] = {}

        # Callbacks for resolution
        self._on_resolved: List[Callable[[ConsensusRound], None]] = []

    def open_round(
        self,
        task_id: str,
        sphere_id: str = "",
    ) -> ConsensusRound:
        """Open a new consensus round for a task."""
        round_id = generate_id()
        consensus_round = ConsensusRound(
            round_id=round_id,
            task_id=task_id,
            sphere_id=sphere_id,
            status=ConsensusStatus.OPEN,
        )
        self._rounds[round_id] = consensus_round
        logger.debug(f"[Consensus] Opened round {round_id} for task {task_id}")
        return consensus_round

    def submit_proposal(
        self,
        round_id: str,
        agent_id: str,
        action: str,
        confidence: float,
        rationale: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[Proposal]:
        """Submit a proposal to an open round."""
        consensus_round = self._rounds.get(round_id)
        if not consensus_round or consensus_round.status != ConsensusStatus.OPEN:
            logger.warning(f"[Consensus] Cannot submit to round {round_id}")
            return None

        proposal = Proposal(
            proposal_id=generate_id(),
            agent_id=agent_id,
            action=action,
            confidence=max(0.0, min(1.0, confidence)),
            rationale=rationale,
            payload=payload or {},
        )
        consensus_round.proposals.append(proposal)
        logger.debug(
            f"[Consensus] Agent {agent_id} proposed '{action}' "
            f"(confidence={confidence:.2f})"
        )
        return proposal

    def start_voting(self, round_id: str) -> bool:
        """Lock proposals and start voting phase."""
        consensus_round = self._rounds.get(round_id)
        if not consensus_round or consensus_round.status != ConsensusStatus.OPEN:
            return False

        if len(consensus_round.proposals) < 2:
            # Single proposal = auto-win
            if consensus_round.proposals:
                consensus_round.winner = consensus_round.proposals[0]
                consensus_round.final_score = consensus_round.proposals[0].confidence
                consensus_round.status = ConsensusStatus.RESOLVED
                consensus_round.resolved_at = datetime.utcnow()
                self._notify_resolved(consensus_round)
            return True

        consensus_round.status = ConsensusStatus.VOTING
        logger.debug(
            f"[Consensus] Voting started for round {round_id} "
            f"({len(consensus_round.proposals)} proposals)"
        )
        return True

    def cast_vote(
        self,
        round_id: str,
        voter_id: str,
        proposal_id: str,
        score: float,
        reason: str = "",
    ) -> bool:
        """Cast a vote on a proposal."""
        consensus_round = self._rounds.get(round_id)
        if not consensus_round or consensus_round.status != ConsensusStatus.VOTING:
            return False

        # Agents cannot vote on their own proposals
        proposal = next(
            (p for p in consensus_round.proposals if p.proposal_id == proposal_id),
            None,
        )
        if proposal and proposal.agent_id == voter_id:
            logger.debug(f"[Consensus] Agent {voter_id} cannot self-vote")
            return False

        vote = Vote(
            voter_id=voter_id,
            proposal_id=proposal_id,
            score=max(-1.0, min(1.0, score)),
            reason=reason,
        )
        consensus_round.votes.append(vote)
        return True

    def resolve(self, round_id: str) -> Optional[ConsensusRound]:
        """
        Resolve voting and select winner.

        Score = proposal.confidence * author_reputation + sum(vote.score * voter_reputation)
        """
        consensus_round = self._rounds.get(round_id)
        if not consensus_round:
            return None

        if consensus_round.status == ConsensusStatus.RESOLVED:
            return consensus_round

        # Tally scores
        scores: Dict[str, float] = {}

        for proposal in consensus_round.proposals:
            # Base score: confidence * author reputation
            rep = self._reputation.get(proposal.agent_id, 0.5)
            base = proposal.confidence * rep
            scores[proposal.proposal_id] = base

        # Add vote scores weighted by voter reputation
        for vote in consensus_round.votes:
            voter_rep = self._reputation.get(vote.voter_id, 0.5)
            scores[vote.proposal_id] = scores.get(vote.proposal_id, 0.0) + (
                vote.score * voter_rep
            )

        if not scores:
            consensus_round.status = ConsensusStatus.DEADLOCKED
            return consensus_round

        # Find winner
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_id, best_score = sorted_scores[0]

        # Check for deadlock (top two too close)
        if len(sorted_scores) > 1:
            second_score = sorted_scores[1][1]
            if best_score - second_score < self._deadlock_threshold:
                consensus_round.status = ConsensusStatus.DEADLOCKED
                logger.debug(
                    f"[Consensus] Deadlock in round {round_id}: "
                    f"gap={best_score - second_score:.3f}"
                )
                return consensus_round

        # Select winner
        winner = next(
            (p for p in consensus_round.proposals if p.proposal_id == best_id),
            None,
        )
        consensus_round.winner = winner
        consensus_round.final_score = best_score
        consensus_round.status = ConsensusStatus.RESOLVED
        consensus_round.resolved_at = datetime.utcnow()

        logger.debug(
            f"[Consensus] Round {round_id} resolved: "
            f"winner={winner.agent_id if winner else 'none'} "
            f"score={best_score:.3f}"
        )

        self._notify_resolved(consensus_round)
        return consensus_round

    def update_reputation(self, agent_id: str, delta: float) -> None:
        """
        Update agent reputation based on outcome quality.
        Called by RewardSignalEngine after task completion.
        """
        current = self._reputation.get(agent_id, 0.5)
        updated = max(0.1, min(1.0, current + delta))
        self._reputation[agent_id] = updated

    def get_reputation(self, agent_id: str) -> float:
        """Get agent's current reputation score."""
        return self._reputation.get(agent_id, 0.5)

    def on_resolved(self, callback: Callable[[ConsensusRound], None]) -> None:
        """Register callback for when a round resolves."""
        self._on_resolved.append(callback)

    def get_round(self, round_id: str) -> Optional[ConsensusRound]:
        """Get a consensus round by ID."""
        return self._rounds.get(round_id)

    def _notify_resolved(self, consensus_round: ConsensusRound) -> None:
        """Notify listeners of resolution."""
        for callback in self._on_resolved:
            try:
                callback(consensus_round)
            except Exception as e:
                logger.error(f"[Consensus] Listener error: {e}")
