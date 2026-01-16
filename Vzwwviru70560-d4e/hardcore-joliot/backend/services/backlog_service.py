"""
SERVICE: backlog_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: Backlog system for governance learning and improvement

DEPENDENCIES:
- Core: orchestrator_service
- Schemas: governance_schemas

R&D COMPLIANCE: ✅
- Rule #1: Human Sovereignty - Policy tuning requires human approval
- Rule #6: Traceability - All backlog items logged as events
- Rule #7: R&D Continuity - Feeds continuous improvement

HUMAN GATES:
- Large threshold changes require human approval
"""

import logging
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime, timedelta
from collections import defaultdict

from ..schemas.governance_schemas import (
    BacklogItem,
    BacklogItemCreate,
    BacklogType,
    BacklogStatus,
    BacklogReferences,
    BacklogMetrics,
    Spec,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# BACKLOG REPOSITORY (In-Memory for now)
# ═══════════════════════════════════════════════════════════════════════════════

class BacklogRepository:
    """
    Repository for backlog items.
    
    In production, this would be backed by PostgreSQL tables:
    - backlog_items
    - backlog_event_links
    """
    
    def __init__(self):
        self.items: Dict[str, BacklogItem] = {}
        self.event_links: Dict[str, List[str]] = defaultdict(list)  # backlog_id -> event_ids
    
    async def create(self, item: BacklogItem) -> BacklogItem:
        """Create a new backlog item."""
        self.items[item.id] = item
        logger.info(f"Created backlog item: {item.id} ({item.backlog_type.value})")
        return item
    
    async def get(self, item_id: str) -> Optional[BacklogItem]:
        """Get a backlog item by ID."""
        return self.items.get(item_id)
    
    async def list_by_type(
        self,
        backlog_type: BacklogType,
        status: Optional[BacklogStatus] = None,
        limit: int = 100
    ) -> List[BacklogItem]:
        """List backlog items by type and optionally status."""
        items = [
            item for item in self.items.values()
            if item.backlog_type == backlog_type
            and (status is None or item.status == status)
        ]
        return sorted(items, key=lambda x: x.created_at, reverse=True)[:limit]
    
    async def list_by_thread(self, thread_id: str) -> List[BacklogItem]:
        """List backlog items for a specific thread."""
        return [
            item for item in self.items.values()
            if item.references and item.references.thread_id == thread_id
        ]
    
    async def update_status(
        self,
        item_id: str,
        status: BacklogStatus,
        resolution: Optional[str] = None
    ) -> Optional[BacklogItem]:
        """Update the status of a backlog item."""
        item = self.items.get(item_id)
        if item:
            item.status = status
            if status == BacklogStatus.RESOLVED:
                item.resolved_at = datetime.utcnow()
            if resolution:
                item.resolution = resolution
            logger.info(f"Updated backlog item {item_id} status to {status.value}")
        return item
    
    async def link_event(self, backlog_id: str, event_id: str) -> None:
        """Link an event to a backlog item."""
        self.event_links[backlog_id].append(event_id)
    
    async def get_linked_events(self, backlog_id: str) -> List[str]:
        """Get events linked to a backlog item."""
        return self.event_links.get(backlog_id, [])


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK METRICS
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackMetrics:
    """
    Computes feedback metrics from backlog items.
    
    Metrics:
    - Escape Rate: % issues found late
    - Fix Cost: median tokens/time per issue
    - Noise Rate: % false alerts
    - Rework Ratio: correction tokens / production tokens
    - Live Smoothness: 95th percentile latency
    """
    
    def __init__(self, repository: BacklogRepository):
        self.repository = repository
    
    async def compute_escape_rate(self, time_window_days: int = 30) -> float:
        """
        Compute escape rate: % of issues found late.
        
        "Late" = escape_depth == "late"
        """
        error_items = await self.repository.list_by_type(BacklogType.ERROR)
        
        # Filter by time window
        cutoff = datetime.utcnow() - timedelta(days=time_window_days)
        recent_items = [i for i in error_items if i.created_at >= cutoff]
        
        if not recent_items:
            return 0.0
        
        late_count = sum(
            1 for i in recent_items
            if i.metrics and i.metrics.escape_depth == "late"
        )
        
        return late_count / len(recent_items)
    
    async def compute_fix_cost_median(self, time_window_days: int = 30) -> float:
        """Compute median fix cost in tokens."""
        error_items = await self.repository.list_by_type(BacklogType.ERROR)
        
        cutoff = datetime.utcnow() - timedelta(days=time_window_days)
        recent_items = [i for i in error_items if i.created_at >= cutoff]
        
        fix_costs = [
            i.metrics.fix_tokens
            for i in recent_items
            if i.metrics and i.metrics.fix_tokens is not None
        ]
        
        if not fix_costs:
            return 0.0
        
        sorted_costs = sorted(fix_costs)
        mid = len(sorted_costs) // 2
        
        if len(sorted_costs) % 2 == 0:
            return (sorted_costs[mid - 1] + sorted_costs[mid]) / 2
        return float(sorted_costs[mid])
    
    async def compute_noise_rate(self, time_window_days: int = 30) -> float:
        """
        Compute noise rate: % of false positive signals.
        """
        signal_items = await self.repository.list_by_type(BacklogType.SIGNAL)
        
        cutoff = datetime.utcnow() - timedelta(days=time_window_days)
        recent_items = [i for i in signal_items if i.created_at >= cutoff]
        
        if not recent_items:
            return 0.0
        
        # Items resolved as won't fix are false positives
        false_positives = sum(
            1 for i in recent_items
            if i.status == BacklogStatus.WONT_FIX
        )
        
        return false_positives / len(recent_items)
    
    async def get_all_metrics(self, time_window_days: int = 30) -> Dict[str, float]:
        """Get all feedback metrics."""
        return {
            "escape_rate": await self.compute_escape_rate(time_window_days),
            "fix_cost_median": await self.compute_fix_cost_median(time_window_days),
            "noise_rate": await self.compute_noise_rate(time_window_days),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# POLICY TUNER
# ═══════════════════════════════════════════════════════════════════════════════

class PolicyTuner:
    """
    Tunes orchestration policies based on backlog feedback.
    
    Safe auto-tuning (bounded):
    - Thresholds (within bounded range)
    - Cooldowns (within bounded range)
    - Routing between cheap vs strong critic
    
    Large changes require human approval.
    """
    
    # Tuning bounds
    THRESHOLD_MIN = 0.1
    THRESHOLD_MAX = 0.9
    THRESHOLD_MAX_DELTA = 0.1
    
    COOLDOWN_MIN = 0
    COOLDOWN_MAX = 600
    COOLDOWN_MAX_DELTA = 60
    
    def __init__(self, metrics: FeedbackMetrics):
        self.metrics = metrics
        self.tuning_history: List[Dict[str, Any]] = []
    
    async def suggest_threshold_adjustment(
        self,
        spec: Spec,
        current_threshold: float
    ) -> Dict[str, Any]:
        """
        Suggest threshold adjustment for a spec based on metrics.
        
        If noise rate is high -> increase threshold (less sensitive)
        If escape rate is high -> decrease threshold (more sensitive)
        
        Returns suggestion that may require human approval if large.
        """
        all_metrics = await self.metrics.get_all_metrics()
        noise_rate = all_metrics["noise_rate"]
        escape_rate = all_metrics["escape_rate"]
        
        # Calculate adjustment
        adjustment = 0.0
        reason = ""
        
        if noise_rate > 0.3:
            # Too many false positives, increase threshold
            adjustment = min(0.05, self.THRESHOLD_MAX_DELTA)
            reason = f"High noise rate ({noise_rate:.1%}), suggesting threshold increase"
        elif escape_rate > 0.2:
            # Missing too many issues, decrease threshold
            adjustment = -min(0.05, self.THRESHOLD_MAX_DELTA)
            reason = f"High escape rate ({escape_rate:.1%}), suggesting threshold decrease"
        else:
            reason = "Metrics within acceptable range, no adjustment needed"
        
        new_threshold = max(
            self.THRESHOLD_MIN,
            min(self.THRESHOLD_MAX, current_threshold + adjustment)
        )
        
        requires_approval = abs(adjustment) >= self.THRESHOLD_MAX_DELTA * 0.8
        
        return {
            "spec_id": spec.id,
            "current_threshold": current_threshold,
            "suggested_threshold": new_threshold,
            "adjustment": adjustment,
            "reason": reason,
            "requires_human_approval": requires_approval,
            "metrics_used": all_metrics,
        }
    
    async def suggest_cooldown_adjustment(
        self,
        spec: Spec,
        current_cooldown: int
    ) -> Dict[str, Any]:
        """
        Suggest cooldown adjustment for a spec.
        
        If spec runs too often with same result -> increase cooldown
        """
        # For now, simple heuristic
        noise_rate = (await self.metrics.get_all_metrics())["noise_rate"]
        
        adjustment = 0
        reason = ""
        
        if noise_rate > 0.4:
            adjustment = min(30, self.COOLDOWN_MAX_DELTA)
            reason = f"High noise rate, suggesting cooldown increase"
        else:
            reason = "Cooldown seems appropriate"
        
        new_cooldown = max(
            self.COOLDOWN_MIN,
            min(self.COOLDOWN_MAX, current_cooldown + adjustment)
        )
        
        return {
            "spec_id": spec.id,
            "current_cooldown": current_cooldown,
            "suggested_cooldown": new_cooldown,
            "adjustment": adjustment,
            "reason": reason,
            "requires_human_approval": adjustment >= self.COOLDOWN_MAX_DELTA * 0.8,
        }
    
    def record_tuning(self, tuning_action: Dict[str, Any]) -> None:
        """Record a tuning action for audit."""
        tuning_action["recorded_at"] = datetime.utcnow().isoformat()
        self.tuning_history.append(tuning_action)


# ═══════════════════════════════════════════════════════════════════════════════
# BACKLOG SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class BacklogService:
    """
    Main service for backlog management.
    
    Captures:
    - Errors that escaped early checks
    - False positive signals
    - Decision outcomes
    - Cost anomalies
    - Governance debt
    
    Feeds:
    - Policy tuning
    - Continuous improvement
    """
    
    def __init__(self):
        self.repository = BacklogRepository()
        self.metrics = FeedbackMetrics(self.repository)
        self.policy_tuner = PolicyTuner(self.metrics)
        
        logger.info("BacklogService initialized")
    
    async def capture_escaped_error(
        self,
        thread_id: str,
        description: str,
        severity: str,
        escape_depth: str,
        fix_tokens: Optional[int] = None,
        event_ids: Optional[List[str]] = None
    ) -> BacklogItem:
        """
        Capture an error that escaped early checks.
        
        Args:
            thread_id: Thread where error occurred
            description: Description of the error
            severity: S1-S5
            escape_depth: early/mid/late
            fix_tokens: Cost to fix in tokens
            event_ids: Related event IDs
        """
        item = BacklogItem(
            id=str(uuid4()),
            backlog_type=BacklogType.ERROR,
            severity=severity,
            title=description[:100],
            description=description,
            references=BacklogReferences(
                thread_id=thread_id,
                event_ids=event_ids or []
            ),
            metrics=BacklogMetrics(
                fix_tokens=fix_tokens,
                escape_depth=escape_depth
            )
        )
        
        return await self.repository.create(item)
    
    async def capture_false_positive(
        self,
        thread_id: str,
        spec_id: str,
        description: str,
        context: Optional[str] = None
    ) -> BacklogItem:
        """
        Capture a false positive signal from a CEA/spec.
        """
        item = BacklogItem(
            id=str(uuid4()),
            backlog_type=BacklogType.SIGNAL,
            title=f"False positive from {spec_id}",
            description=description,
            references=BacklogReferences(
                thread_id=thread_id,
                spec_ids=[spec_id]
            )
        )
        
        return await self.repository.create(item)
    
    async def capture_decision_outcome(
        self,
        thread_id: str,
        decision_id: str,
        outcome: str,
        description: str,
        event_ids: Optional[List[str]] = None
    ) -> BacklogItem:
        """
        Capture the outcome of a decision for learning.
        """
        item = BacklogItem(
            id=str(uuid4()),
            backlog_type=BacklogType.DECISION,
            title=f"Decision outcome: {outcome}",
            description=description,
            references=BacklogReferences(
                thread_id=thread_id,
                event_ids=event_ids or []
            )
        )
        
        return await self.repository.create(item)
    
    async def capture_cost_anomaly(
        self,
        thread_id: str,
        spec_id: str,
        estimated_cost: float,
        actual_cost: float,
        description: str
    ) -> BacklogItem:
        """
        Capture a cost anomaly (estimate vs actual mismatch).
        """
        item = BacklogItem(
            id=str(uuid4()),
            backlog_type=BacklogType.COST,
            title=f"Cost anomaly for {spec_id}",
            description=description,
            references=BacklogReferences(
                thread_id=thread_id,
                spec_ids=[spec_id]
            ),
            metrics=BacklogMetrics(
                cost_estimate_vs_actual={
                    "estimated": estimated_cost,
                    "actual": actual_cost,
                    "delta": actual_cost - estimated_cost
                }
            )
        )
        
        return await self.repository.create(item)
    
    async def capture_governance_debt(
        self,
        thread_id: str,
        debt_type: str,
        description: str
    ) -> BacklogItem:
        """
        Capture governance debt (missing specs, unclear roles, etc.).
        """
        item = BacklogItem(
            id=str(uuid4()),
            backlog_type=BacklogType.GOVERNANCE_DEBT,
            title=f"Governance debt: {debt_type}",
            description=description,
            references=BacklogReferences(thread_id=thread_id)
        )
        
        return await self.repository.create(item)
    
    async def get_metrics(self, time_window_days: int = 30) -> Dict[str, float]:
        """Get current feedback metrics."""
        return await self.metrics.get_all_metrics(time_window_days)
    
    async def suggest_policy_updates(
        self,
        specs: List[Spec]
    ) -> List[Dict[str, Any]]:
        """
        Suggest policy updates based on backlog feedback.
        
        Returns list of suggestions, some may require human approval.
        """
        suggestions = []
        
        for spec in specs:
            # Suggest threshold adjustment
            threshold_suggestion = await self.policy_tuner.suggest_threshold_adjustment(
                spec,
                current_threshold=0.5  # Would come from spec config
            )
            suggestions.append(threshold_suggestion)
            
            # Suggest cooldown adjustment
            cooldown_suggestion = await self.policy_tuner.suggest_cooldown_adjustment(
                spec,
                current_cooldown=spec.cooldown
            )
            suggestions.append(cooldown_suggestion)
        
        return suggestions
    
    async def resolve_item(
        self,
        item_id: str,
        resolution: str,
        resolved_by: str
    ) -> Optional[BacklogItem]:
        """
        Resolve a backlog item.
        
        Resolution should map to one of:
        - new spec
        - threshold change
        - new acceptance test
        - new UI guardrail
        - documentation clarification
        """
        item = await self.repository.update_status(
            item_id,
            BacklogStatus.RESOLVED,
            resolution=resolution
        )
        
        if item:
            logger.info(f"Resolved backlog item {item_id}: {resolution}")
        
        return item


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "BacklogRepository",
    "FeedbackMetrics",
    "PolicyTuner",
    "BacklogService",
]
