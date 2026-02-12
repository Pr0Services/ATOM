"""
============================================================================
CHE·NU™ V69 — NEURO FEEDBACK HUB
============================================================================
System 1/5: Centralized signal aggregation

Problem: ThreatAmygdala, DigestiveSystem, NeuromorphicLattice, and
FeedbackLoopEngine all emit signals independently. No system aggregates
them into a global health signal for adaptive decision-making.

Solution: NeuroFeedbackHub subscribes to SpikeBus events, maintains a
rolling window of system-wide signals, computes a global health score,
and exposes it to PlasticityWorker and the orchestrator.

Connects to:
- SpikeBus (consumes events)
- PlasticityWorker (feeds aggregated reward signals)
- OrchestratorService (exposes global health)

Does NOT duplicate:
- ThreatAmygdala (we aggregate, not detect)
- PerformanceMonitor (we focus on neuromorphic signals, not HTTP metrics)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from collections import deque
from enum import Enum
import logging

from ..models import SpikeEvent, SpikeType

logger = logging.getLogger(__name__)


class SystemHealth(str, Enum):
    OPTIMAL = "optimal"         # score > 0.8
    NOMINAL = "nominal"         # 0.5 < score <= 0.8
    DEGRADED = "degraded"       # 0.25 < score <= 0.5
    CRITICAL = "critical"       # score <= 0.25


@dataclass
class AggregatedSignal:
    """A time-windowed aggregate of spike events."""
    window_start: datetime
    window_end: datetime
    event_count: int
    avg_intensity: float
    spike_type_counts: Dict[str, int]
    health: SystemHealth
    health_score: float


class NeuroFeedbackHub:
    """
    Centralized signal aggregation hub.

    Collects spikes from SpikeBus, computes rolling health metrics,
    and exposes a global system health score.
    """

    def __init__(
        self,
        window_seconds: int = 60,
        max_events: int = 1000,
    ):
        self.window_seconds = window_seconds
        self.max_events = max_events

        self._events: deque = deque(maxlen=max_events)
        self._health_score: float = 1.0
        self._listeners: List[Callable[[AggregatedSignal], None]] = []

        # Per-source tracking for reward signals
        self._source_scores: Dict[str, deque] = {}

    def ingest(self, event: SpikeEvent) -> None:
        """Ingest a spike event from SpikeBus."""
        self._events.append(event)
        self._update_source_score(event)

        # Recompute health every 10 events
        if len(self._events) % 10 == 0:
            signal = self.compute_aggregate()
            for listener in self._listeners:
                try:
                    listener(signal)
                except Exception as e:
                    logger.error(f"Feedback listener error: {e}")

    def compute_aggregate(self) -> AggregatedSignal:
        """Compute aggregated signal over the time window."""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.window_seconds)

        window_events = [
            e for e in self._events
            if e.timestamp >= cutoff
        ]

        if not window_events:
            self._health_score = 1.0
            return AggregatedSignal(
                window_start=cutoff,
                window_end=now,
                event_count=0,
                avg_intensity=0.0,
                spike_type_counts={},
                health=SystemHealth.OPTIMAL,
                health_score=1.0,
            )

        # Count by type
        type_counts: Dict[str, int] = {}
        total_intensity = 0.0
        alert_count = 0

        for e in window_events:
            type_name = e.spike_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            total_intensity += e.intensity
            if e.spike_type == SpikeType.ALERT:
                alert_count += 1

        avg_intensity = total_intensity / len(window_events)
        event_count = len(window_events)

        # Health score: penalize alerts and high intensity
        alert_ratio = alert_count / max(event_count, 1)
        score = max(0.0, 1.0 - (alert_ratio * 0.5) - (avg_intensity * 0.3))
        self._health_score = score

        health = self._score_to_health(score)

        signal = AggregatedSignal(
            window_start=cutoff,
            window_end=now,
            event_count=event_count,
            avg_intensity=avg_intensity,
            spike_type_counts=type_counts,
            health=health,
            health_score=score,
        )

        logger.debug(
            f"[NeuroFeedbackHub] {event_count} events, "
            f"health={health.value} ({score:.2f})"
        )

        return signal

    def get_health(self) -> SystemHealth:
        """Get current system health."""
        return self._score_to_health(self._health_score)

    def get_health_score(self) -> float:
        """Get raw health score [0, 1]."""
        return self._health_score

    def get_source_reward(self, agent_id: str) -> float:
        """
        Get reward signal for a specific agent.
        Used by RewardSignalEngine and PlasticityWorker.

        Returns value in [-1.0, 1.0]:
        - Positive = agent's recent spikes were low-intensity (good)
        - Negative = agent's recent spikes were high-intensity alerts (bad)
        """
        scores = self._source_scores.get(agent_id)
        if not scores:
            return 0.0

        recent = list(scores)[-20:]
        if not recent:
            return 0.0

        avg = sum(recent) / len(recent)
        return max(-1.0, min(1.0, 1.0 - avg * 2))

    def on_aggregate(self, listener: Callable[[AggregatedSignal], None]) -> None:
        """Register listener for aggregate signals."""
        self._listeners.append(listener)

    def _update_source_score(self, event: SpikeEvent) -> None:
        """Track per-source intensity for reward computation."""
        source = event.source_agent
        if source not in self._source_scores:
            self._source_scores[source] = deque(maxlen=100)
        self._source_scores[source].append(event.intensity)

    @staticmethod
    def _score_to_health(score: float) -> SystemHealth:
        if score > 0.8:
            return SystemHealth.OPTIMAL
        elif score > 0.5:
            return SystemHealth.NOMINAL
        elif score > 0.25:
            return SystemHealth.DEGRADED
        else:
            return SystemHealth.CRITICAL
