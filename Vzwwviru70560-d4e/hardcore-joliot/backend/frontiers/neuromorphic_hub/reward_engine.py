"""
============================================================================
CHE·NU™ V69 — REWARD SIGNAL ENGINE
============================================================================
System 4/5: Incentive learning for agents

Problem: PlasticityWorker adjusts thresholds mechanically (±delta). No
system evaluates whether an agent's OUTCOMES were good or bad and feeds
that back as a reward signal for long-term behavioral improvement.

Solution: RewardSignalEngine tracks task→outcome pairs per agent,
computes reward signals from multiple sources (NeuroFeedbackHub health,
consensus win rate, task completion quality), and feeds them to
PlasticityWorker and AdaptivePriorityQueue.

Connects to:
- NeuroFeedbackHub (gets per-agent health signals)
- AgentConsensusProtocol (gets win/loss data)
- PlasticityWorker (feeds reward for threshold adjustment)
- AdaptivePriorityQueue (feeds outcome for weight learning)

Does NOT duplicate:
- PlasticityWorker (that adjusts thresholds, we provide the signal)
- FeedbackLoopEngine (that simulates temporal loops, not reward)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from collections import deque
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class OutcomeQuality(str, Enum):
    EXCELLENT = "excellent"    # reward > 0.7
    GOOD = "good"              # 0.3 < reward <= 0.7
    NEUTRAL = "neutral"        # -0.3 <= reward <= 0.3
    POOR = "poor"              # -0.7 <= reward < -0.3
    FAILURE = "failure"        # reward < -0.7


@dataclass
class TaskOutcome:
    """Recorded outcome for a completed task."""
    task_id: str
    agent_id: str
    sphere_id: str
    reward: float  # [-1.0, 1.0]
    quality: OutcomeQuality
    completion_time_ms: int = 0
    consensus_winner: bool = False
    health_impact: float = 0.0  # change in health score
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentProfile:
    """Accumulated reward profile for an agent."""
    agent_id: str
    total_tasks: int = 0
    total_reward: float = 0.0
    avg_reward: float = 0.0
    win_rate: float = 0.0  # consensus wins / total proposals
    recent_trend: float = 0.0  # reward trend (positive = improving)
    outcomes: deque = field(default_factory=lambda: deque(maxlen=200))


class RewardSignalEngine:
    """
    Computes and distributes reward signals for agent learning.

    Reward composition:
    - Task quality (direct outcome measurement)
    - Health contribution (from NeuroFeedbackHub)
    - Consensus performance (from AgentConsensusProtocol)
    - Time efficiency bonus

    These signals flow to:
    - PlasticityWorker: for synapse threshold adjustment
    - AdaptivePriorityQueue: for weight learning
    - AgentConsensusProtocol: for reputation updates
    """

    def __init__(
        self,
        decay_factor: float = 0.95,
        time_bonus_threshold_ms: int = 5000,
    ):
        self._profiles: Dict[str, AgentProfile] = {}
        self._decay_factor = decay_factor
        self._time_bonus_threshold_ms = time_bonus_threshold_ms
        self._global_outcomes: deque = deque(maxlen=1000)

        # Reward distribution callbacks
        self._reward_listeners: List[Callable[[str, float], None]] = []

    def record_outcome(
        self,
        task_id: str,
        agent_id: str,
        raw_quality: float,
        sphere_id: str = "",
        completion_time_ms: int = 0,
        consensus_winner: bool = False,
        health_delta: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TaskOutcome:
        """
        Record a task outcome and compute composite reward.

        raw_quality: [-1.0, 1.0] direct task quality assessment
        health_delta: change in system health after this task
        consensus_winner: whether this agent won consensus for this task
        """
        # Composite reward from multiple signals
        reward = self._compute_reward(
            raw_quality=raw_quality,
            completion_time_ms=completion_time_ms,
            consensus_winner=consensus_winner,
            health_delta=health_delta,
        )

        quality = self._reward_to_quality(reward)

        outcome = TaskOutcome(
            task_id=task_id,
            agent_id=agent_id,
            sphere_id=sphere_id,
            reward=reward,
            quality=quality,
            completion_time_ms=completion_time_ms,
            consensus_winner=consensus_winner,
            health_impact=health_delta,
            metadata=metadata or {},
        )

        # Update agent profile
        self._update_profile(agent_id, outcome)

        # Store globally
        self._global_outcomes.append(outcome)

        # Distribute reward signal
        self._distribute_reward(agent_id, reward)

        logger.debug(
            f"[RewardEngine] Agent {agent_id}: reward={reward:.3f} "
            f"quality={quality.value}"
        )

        return outcome

    def get_agent_reward(self, agent_id: str) -> float:
        """Get current aggregate reward signal for an agent."""
        profile = self._profiles.get(agent_id)
        if not profile or not profile.outcomes:
            return 0.0

        # Exponentially-weighted recent reward
        rewards = [o.reward for o in profile.outcomes]
        weighted_sum = 0.0
        weight_total = 0.0
        factor = 1.0

        for r in reversed(rewards):
            weighted_sum += r * factor
            weight_total += factor
            factor *= self._decay_factor

        return weighted_sum / max(weight_total, 1.0)

    def get_agent_profile(self, agent_id: str) -> Optional[AgentProfile]:
        """Get full agent profile."""
        return self._profiles.get(agent_id)

    def get_top_agents(self, n: int = 10) -> List[AgentProfile]:
        """Get top N agents by average reward."""
        profiles = sorted(
            self._profiles.values(),
            key=lambda p: p.avg_reward,
            reverse=True,
        )
        return profiles[:n]

    def get_global_avg_reward(self) -> float:
        """Get global average reward across all recent outcomes."""
        if not self._global_outcomes:
            return 0.0
        return sum(o.reward for o in self._global_outcomes) / len(
            self._global_outcomes
        )

    def on_reward(self, listener: Callable[[str, float], None]) -> None:
        """Register listener for reward signals. Receives (agent_id, reward)."""
        self._reward_listeners.append(listener)

    def _compute_reward(
        self,
        raw_quality: float,
        completion_time_ms: int,
        consensus_winner: bool,
        health_delta: float,
    ) -> float:
        """
        Composite reward from multiple signals.

        Components:
        - 60% raw quality
        - 15% health contribution
        - 15% consensus bonus
        - 10% time efficiency
        """
        # Raw quality (clamped)
        quality_component = max(-1.0, min(1.0, raw_quality)) * 0.6

        # Health contribution
        health_component = max(-1.0, min(1.0, health_delta)) * 0.15

        # Consensus bonus
        consensus_component = (0.5 if consensus_winner else -0.1) * 0.15

        # Time efficiency bonus
        time_component = 0.0
        if completion_time_ms > 0:
            if completion_time_ms < self._time_bonus_threshold_ms:
                time_component = 0.5 * 0.1  # fast bonus
            elif completion_time_ms > self._time_bonus_threshold_ms * 4:
                time_component = -0.3 * 0.1  # slow penalty

        reward = quality_component + health_component + consensus_component + time_component
        return max(-1.0, min(1.0, reward))

    def _update_profile(self, agent_id: str, outcome: TaskOutcome) -> None:
        """Update agent's accumulated profile."""
        if agent_id not in self._profiles:
            self._profiles[agent_id] = AgentProfile(agent_id=agent_id)

        profile = self._profiles[agent_id]
        profile.total_tasks += 1
        profile.total_reward += outcome.reward
        profile.avg_reward = profile.total_reward / profile.total_tasks
        profile.outcomes.append(outcome)

        # Compute trend from last 20 outcomes
        recent = list(profile.outcomes)[-20:]
        if len(recent) >= 4:
            first_half = sum(o.reward for o in recent[: len(recent) // 2])
            second_half = sum(o.reward for o in recent[len(recent) // 2 :])
            profile.recent_trend = second_half - first_half

        # Win rate
        wins = sum(1 for o in profile.outcomes if o.consensus_winner)
        profile.win_rate = wins / max(len(profile.outcomes), 1)

    def _distribute_reward(self, agent_id: str, reward: float) -> None:
        """Distribute reward signal to listeners."""
        for listener in self._reward_listeners:
            try:
                listener(agent_id, reward)
            except Exception as e:
                logger.error(f"[RewardEngine] Listener error: {e}")

    @staticmethod
    def _reward_to_quality(reward: float) -> OutcomeQuality:
        if reward > 0.7:
            return OutcomeQuality.EXCELLENT
        elif reward > 0.3:
            return OutcomeQuality.GOOD
        elif reward >= -0.3:
            return OutcomeQuality.NEUTRAL
        elif reward >= -0.7:
            return OutcomeQuality.POOR
        else:
            return OutcomeQuality.FAILURE
