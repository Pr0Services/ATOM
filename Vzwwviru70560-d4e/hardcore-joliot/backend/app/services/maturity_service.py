"""
SERVICE: maturity_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: Thread Maturity computation service (derived, not canonical)

DEPENDENCIES:
- Core: thread_service (for event counts)
- Schemas: xr_schemas

R&D COMPLIANCE: ✅
- Rule #3: Sphere Integrity - Maturity is DERIVED, never authoritative
- Rule #6: Traceability - Maturity stored as snapshot with references
- Rule #7: R&D Continuity - Follows maturity model spec

HUMAN GATES: None (read-only service)
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from uuid import uuid4

from ..schemas.xr_schemas import (
    MaturityLevel,
    MaturitySignals,
    MaturityResult,
    EnvironmentEvolutionRule,
    ZoneType,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# MATURITY SCORER
# ═══════════════════════════════════════════════════════════════════════════════

class MaturityScorer:
    """
    Computes thread maturity score from event log.
    
    Scoring (simple + deterministic):
    - +10 if ≥ 1 SUMMARY_SNAPSHOT
    - +10 if ≥ 1 DECISION_RECORDED
    - +10 if ≥ 5 ACTION_* events
    - +10 if ≥ 3 participants
    - +10 if ≥ 1 LIVE segment
    - +10 if ≥ 3 LINK_ADDED
    - +10 if ≥ 20 MESSAGE_POSTED
    - +10 if ≥ 5 learning events (CORRECTION_APPENDED, etc.)
    - +10 if thread age ≥ 30 days and still active
    - +10 if ≥ 3 linked threads (portals)
    
    Total possible: 100 points
    """
    
    # Scoring thresholds
    SUMMARY_THRESHOLD = 1
    DECISION_THRESHOLD = 1
    ACTION_THRESHOLD = 5
    PARTICIPANT_THRESHOLD = 3
    LIVE_THRESHOLD = 1
    LINK_THRESHOLD = 3
    MESSAGE_THRESHOLD = 20
    LEARNING_THRESHOLD = 5
    AGE_THRESHOLD_DAYS = 30
    PORTAL_THRESHOLD = 3
    
    @staticmethod
    def compute_signals(event_counts: Dict[str, int], thread_metadata: Dict[str, Any]) -> MaturitySignals:
        """
        Extract maturity signals from event counts and metadata.
        
        Args:
            event_counts: Dict mapping event type to count
            thread_metadata: Thread metadata (created_at, last_active, participants, etc.)
        
        Returns:
            MaturitySignals with all indicators
        """
        return MaturitySignals(
            has_summary=event_counts.get("SUMMARY_SNAPSHOT", 0) >= MaturityScorer.SUMMARY_THRESHOLD,
            has_decisions=event_counts.get("DECISION_RECORDED", 0) >= MaturityScorer.DECISION_THRESHOLD,
            action_count=sum([
                event_counts.get("ACTION_CREATED", 0),
                event_counts.get("ACTION_UPDATED", 0),
                event_counts.get("ACTION_COMPLETED", 0),
            ]),
            participant_count=thread_metadata.get("participant_count", 1),
            has_live_segments=(
                event_counts.get("LIVE_STARTED", 0) >= MaturityScorer.LIVE_THRESHOLD
            ),
            link_count=event_counts.get("LINK_ADDED", 0),
            message_count=event_counts.get("MESSAGE_POSTED", 0),
            learning_event_count=sum([
                event_counts.get("CORRECTION_APPENDED", 0),
                event_counts.get("ERROR_RECORDED", 0),
                event_counts.get("LEARNING_RECORDED", 0),
            ]),
            thread_age_days=thread_metadata.get("age_days", 0),
            linked_thread_count=thread_metadata.get("linked_thread_count", 0),
        )
    
    @staticmethod
    def compute_score(signals: MaturitySignals) -> int:
        """
        Compute maturity score from signals.
        
        Returns:
            Score from 0 to 100
        """
        score = 0
        
        if signals.has_summary:
            score += 10
        
        if signals.has_decisions:
            score += 10
        
        if signals.action_count >= MaturityScorer.ACTION_THRESHOLD:
            score += 10
        
        if signals.participant_count >= MaturityScorer.PARTICIPANT_THRESHOLD:
            score += 10
        
        if signals.has_live_segments:
            score += 10
        
        if signals.link_count >= MaturityScorer.LINK_THRESHOLD:
            score += 10
        
        if signals.message_count >= MaturityScorer.MESSAGE_THRESHOLD:
            score += 10
        
        if signals.learning_event_count >= MaturityScorer.LEARNING_THRESHOLD:
            score += 10
        
        if signals.thread_age_days >= MaturityScorer.AGE_THRESHOLD_DAYS:
            score += 10
        
        if signals.linked_thread_count >= MaturityScorer.PORTAL_THRESHOLD:
            score += 10
        
        return min(100, max(0, score))
    
    @staticmethod
    def score_to_level(score: int) -> MaturityLevel:
        """
        Map score to maturity level.
        
        - 0-9: Level 0 (Seed)
        - 10-24: Level 1 (Sprout)
        - 25-44: Level 2 (Workshop)
        - 45-64: Level 3 (Studio)
        - 65-84: Level 4 (Org)
        - 85-100: Level 5 (Ecosystem)
        """
        if score < 10:
            return MaturityLevel.SEED
        elif score < 25:
            return MaturityLevel.SPROUT
        elif score < 45:
            return MaturityLevel.WORKSHOP
        elif score < 65:
            return MaturityLevel.STUDIO
        elif score < 85:
            return MaturityLevel.ORG
        else:
            return MaturityLevel.ECOSYSTEM
    
    @staticmethod
    def level_to_label(level: MaturityLevel) -> str:
        """Map level to human-readable label."""
        labels = {
            MaturityLevel.SEED: "Seed",
            MaturityLevel.SPROUT: "Sprout",
            MaturityLevel.WORKSHOP: "Workshop",
            MaturityLevel.STUDIO: "Studio",
            MaturityLevel.ORG: "Org",
            MaturityLevel.ECOSYSTEM: "Ecosystem",
        }
        return labels[level]


# ═══════════════════════════════════════════════════════════════════════════════
# MATURITY SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class MaturityService:
    """
    Thread Maturity computation service.
    
    Maturity is DERIVED from events/snapshots, never authoritative.
    It controls:
    - Which XR template is chosen
    - How dense/complex the room becomes
    - Which UI prompts are shown at entry
    - Which automation triggers are allowed
    """
    
    def __init__(self):
        self.scorer = MaturityScorer()
        self._cache: Dict[str, MaturityResult] = {}
        logger.info("MaturityService initialized")
    
    async def compute_maturity(
        self,
        thread_id: str,
        event_counts: Dict[str, int],
        thread_metadata: Dict[str, Any]
    ) -> MaturityResult:
        """
        Compute maturity for a thread.
        
        Args:
            thread_id: Thread ID
            event_counts: Dict mapping event type to count
            thread_metadata: Thread metadata
            
        Returns:
            MaturityResult with score, level, label, and signals
        """
        # Compute signals
        signals = self.scorer.compute_signals(event_counts, thread_metadata)
        
        # Compute score
        score = self.scorer.compute_score(signals)
        
        # Map to level
        level = self.scorer.score_to_level(score)
        label = self.scorer.level_to_label(level)
        
        result = MaturityResult(
            thread_id=thread_id,
            score=score,
            level=level,
            label=label,
            signals=signals
        )
        
        # Cache result
        self._cache[thread_id] = result
        
        logger.info(f"Computed maturity for {thread_id}: {score} ({label})")
        return result
    
    async def get_cached_maturity(self, thread_id: str) -> Optional[MaturityResult]:
        """Get cached maturity result if available."""
        return self._cache.get(thread_id)
    
    def get_zones_for_maturity(self, level: MaturityLevel) -> List[ZoneType]:
        """
        Get which zones should be visible at a maturity level.
        
        Environment evolution rules:
        - Level 0: wall + kiosk (simple)
        - Level 1: add action table + basic decision wall
        - Level 2: add resource shelf + timeline strip
        - Level 3: add portals + live corner
        - Level 4: add governance board + metrics shelf
        - Level 5: add multi-room navigation
        """
        return EnvironmentEvolutionRule.get_zones_for_level(level)
    
    def get_environment_features(self, level: MaturityLevel) -> List[str]:
        """Get features enabled at a maturity level."""
        features_by_level = {
            MaturityLevel.SEED: ["basic_intent_display", "memory_kiosk"],
            MaturityLevel.SPROUT: ["action_table", "decision_wall", "basic_timeline"],
            MaturityLevel.WORKSHOP: ["resource_shelf", "full_timeline", "filtering"],
            MaturityLevel.STUDIO: ["portals", "live_corner", "roles_signage", "collaboration"],
            MaturityLevel.ORG: ["governance_board", "metrics_shelf", "dependencies"],
            MaturityLevel.ECOSYSTEM: ["multi_room_nav", "thread_atlas", "advanced_analytics"],
        }
        
        # Accumulate features from lower levels
        all_features = []
        for lvl in MaturityLevel:
            all_features.extend(features_by_level.get(lvl, []))
            if lvl == level:
                break
        
        return all_features
    
    async def should_recompute(
        self,
        thread_id: str,
        last_computed: datetime,
        recent_events: List[str]
    ) -> bool:
        """
        Determine if maturity should be recomputed.
        
        Recompute when:
        - Threshold-triggering events happen
        - Cache is stale (> 1 hour)
        """
        # Threshold-triggering events
        threshold_events = [
            "SUMMARY_SNAPSHOT",
            "DECISION_RECORDED",
            "ACTION_CREATED",
            "LIVE_STARTED",
            "LINK_ADDED",
        ]
        
        for event in recent_events:
            if event in threshold_events:
                return True
        
        # Cache staleness
        age = datetime.utcnow() - last_computed
        if age > timedelta(hours=1):
            return True
        
        return False
    
    def create_maturity_snapshot_payload(self, result: MaturityResult) -> Dict[str, Any]:
        """
        Create payload for storing maturity as a thread snapshot.
        
        Snapshot type: 'thread_maturity'
        """
        return {
            "snapshot_type": "thread_maturity",
            "content": {
                "score": result.score,
                "level": result.level.value,
                "label": result.label,
                "signals": result.signals.model_dump(),
            },
            "computed_at": result.computed_at.isoformat(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK EVENT COUNTER (for testing)
# ═══════════════════════════════════════════════════════════════════════════════

class MockEventCounter:
    """
    Mock event counter for testing maturity computation.
    
    In production, this would query the thread event store.
    """
    
    @staticmethod
    def get_event_counts(thread_id: str) -> Dict[str, int]:
        """Get mock event counts for a thread."""
        # This would be replaced with actual database queries
        return {
            "THREAD_CREATED": 1,
            "MESSAGE_POSTED": 25,
            "SUMMARY_SNAPSHOT": 2,
            "DECISION_RECORDED": 3,
            "ACTION_CREATED": 8,
            "ACTION_UPDATED": 4,
            "ACTION_COMPLETED": 3,
            "LINK_ADDED": 5,
            "LIVE_STARTED": 1,
            "LIVE_ENDED": 1,
            "CORRECTION_APPENDED": 2,
        }
    
    @staticmethod
    def get_thread_metadata(thread_id: str) -> Dict[str, Any]:
        """Get mock thread metadata."""
        return {
            "participant_count": 4,
            "age_days": 45,
            "linked_thread_count": 2,
            "created_at": datetime.utcnow() - timedelta(days=45),
            "last_active": datetime.utcnow() - timedelta(hours=2),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "MaturityScorer",
    "MaturityService",
    "MockEventCounter",
]
