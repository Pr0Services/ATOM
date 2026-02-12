"""
============================================================================
CHE·NU™ V69 — ADAPTIVE PRIORITY QUEUE
============================================================================
System 2/5: Learning-based request ordering

Problem: NeuromorphicLattice.score_priority() does static scoring
(risk*0.6 + impact*0.4). No system learns from historical outcomes
to reorder future requests.

Solution: AdaptivePriorityQueue wraps priority scoring with a
feedback-adjusted weight vector. When outcomes are observed (via
RewardSignalEngine), weights shift to prioritize patterns that
produced better results.

Connects to:
- NeuromorphicLattice.score_priority() (we extend, not replace)
- RewardSignalEngine (receives outcome feedback)
- OrchestratorService (provides ordered task queue)

Does NOT duplicate:
- NeuromorphicLattice.score_priority (we add learning on top)
- FeedbackLoopEngine (that's temporal simulation, not task ordering)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from collections import deque
import heapq
import logging

logger = logging.getLogger(__name__)


@dataclass(order=True)
class PrioritizedTask:
    """A task with adaptive priority score."""
    priority: float  # negative for max-heap behavior
    task_id: str = field(compare=False)
    sphere_id: str = field(compare=False, default="")
    agent_id: str = field(compare=False, default="")
    payload: Dict[str, Any] = field(compare=False, default_factory=dict)
    created_at: datetime = field(compare=False, default_factory=datetime.utcnow)
    base_risk: float = field(compare=False, default=0.0)
    base_impact: float = field(compare=False, default=0.0)


class AdaptivePriorityQueue:
    """
    Priority queue that learns from outcomes.

    Weight vector: [risk_weight, impact_weight, sphere_boost, recency_weight]
    These weights adapt based on reward signals from completed tasks.
    """

    def __init__(self, learning_rate: float = 0.01):
        self._heap: List[PrioritizedTask] = []
        self._learning_rate = learning_rate

        # Adaptive weights (start at NeuromorphicLattice defaults)
        self._weights = {
            "risk": 0.6,
            "impact": 0.4,
            "sphere_boost": 0.0,
            "recency": 0.0,
        }

        # Sphere-specific boosts (learned)
        self._sphere_boosts: Dict[str, float] = {}

        # History for learning
        self._outcomes: deque = deque(maxlen=500)

    def enqueue(
        self,
        task_id: str,
        risk_level: float,
        impact_score: float,
        sphere_id: str = "",
        agent_id: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> PrioritizedTask:
        """Add task with adaptively computed priority."""
        priority = self._compute_priority(risk_level, impact_score, sphere_id)

        task = PrioritizedTask(
            priority=-priority,  # negative for max-heap
            task_id=task_id,
            sphere_id=sphere_id,
            agent_id=agent_id,
            payload=payload or {},
            base_risk=risk_level,
            base_impact=impact_score,
        )

        heapq.heappush(self._heap, task)
        logger.debug(f"[AdaptiveQueue] Enqueued {task_id} priority={priority:.3f}")
        return task

    def dequeue(self) -> Optional[PrioritizedTask]:
        """Get highest priority task."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[PrioritizedTask]:
        """Peek at highest priority task without removing."""
        if not self._heap:
            return None
        return self._heap[0]

    def record_outcome(
        self,
        task_id: str,
        reward: float,
        sphere_id: str = "",
        risk_level: float = 0.0,
        impact_score: float = 0.0,
    ) -> None:
        """
        Record task outcome for weight adjustment.
        reward: [-1.0, 1.0] where positive = good outcome
        """
        self._outcomes.append({
            "task_id": task_id,
            "reward": reward,
            "sphere_id": sphere_id,
            "risk": risk_level,
            "impact": impact_score,
        })

        # Adjust weights based on outcome
        self._adjust_weights(reward, risk_level, impact_score, sphere_id)

    def get_weights(self) -> Dict[str, float]:
        """Get current adaptive weights."""
        return dict(self._weights)

    @property
    def size(self) -> int:
        return len(self._heap)

    def _compute_priority(
        self,
        risk: float,
        impact: float,
        sphere_id: str,
    ) -> float:
        """Compute priority using adaptive weights."""
        score = (
            self._weights["risk"] * risk
            + self._weights["impact"] * impact
            + self._sphere_boosts.get(sphere_id, 0.0)
        )
        return max(0.0, min(1.0, score))

    def _adjust_weights(
        self,
        reward: float,
        risk: float,
        impact: float,
        sphere_id: str,
    ) -> None:
        """
        Adjust weights toward features correlated with positive outcomes.

        If a high-risk task had a positive outcome, increase risk weight.
        If a high-impact task had a negative outcome, decrease impact weight.
        """
        lr = self._learning_rate

        # Gradient-like update: weight += lr * reward * feature_value
        self._weights["risk"] += lr * reward * risk
        self._weights["impact"] += lr * reward * impact

        # Clamp weights to [0.1, 0.9]
        for key in ["risk", "impact"]:
            self._weights[key] = max(0.1, min(0.9, self._weights[key]))

        # Normalize so risk + impact = 1.0
        total = self._weights["risk"] + self._weights["impact"]
        if total > 0:
            self._weights["risk"] /= total
            self._weights["impact"] /= total

        # Sphere boost
        if sphere_id:
            current = self._sphere_boosts.get(sphere_id, 0.0)
            self._sphere_boosts[sphere_id] = max(
                -0.2, min(0.2, current + lr * reward)
            )

        logger.debug(
            f"[AdaptiveQueue] Weights adjusted: "
            f"risk={self._weights['risk']:.3f} "
            f"impact={self._weights['impact']:.3f}"
        )
