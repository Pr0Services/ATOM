"""
=============================================================================
CHE-NU Analytics Service
=============================================================================

Version: 1.0.0
Purpose: Backend service for analytics event tracking and funnel analysis

Funnel Steps:
1. landing_view - User views the landing page
2. cta_click - User clicks a call-to-action
3. sceau_activate - User activates their sceau (seal)
4. essaim_view - User views the essaim (swarm)
5. module_enter - User enters a module

R&D Rules Enforced:
- Rule #5: CHRONOLOGICAL ONLY - Events stored in time order
- Rule #6: Full traceability on all operations
=============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from uuid import uuid4
import logging
from collections import defaultdict

from app.schemas.analytics_schemas import (
    FunnelStepName,
    EventCategory,
    AnalyticsEventCreate,
    AnalyticsEventResponse,
    AnalyticsEventBatchResponse,
    FunnelStep,
    FunnelMetrics,
    SessionStats,
    SessionStatsResponse,
    AnalyticsEventInternal,
)

logger = logging.getLogger("chenu.analytics")


# =============================================================================
# CONSTANTS
# =============================================================================

FUNNEL_STEPS: List[str] = [
    FunnelStepName.LANDING_VIEW.value,
    FunnelStepName.CTA_CLICK.value,
    FunnelStepName.SCEAU_ACTIVATE.value,
    FunnelStepName.ESSAIM_VIEW.value,
    FunnelStepName.MODULE_ENTER.value,
]

FUNNEL_STEP_NAMES: Dict[int, str] = {
    1: "Landing View",
    2: "CTA Click",
    3: "Sceau Activate",
    4: "Essaim View",
    5: "Module Enter",
}


# =============================================================================
# IN-MEMORY STORAGE (Replace with database in production)
# =============================================================================

@dataclass
class AnalyticsStore:
    """
    In-memory analytics event store.

    In production, this should be replaced with a database backend
    (PostgreSQL, ClickHouse, or similar analytics database).
    """
    events: List[AnalyticsEventInternal] = field(default_factory=list)
    sessions: Dict[str, List[AnalyticsEventInternal]] = field(default_factory=lambda: defaultdict(list))

    def add_event(self, event: AnalyticsEventInternal) -> None:
        """Add an event to the store."""
        self.events.append(event)
        self.sessions[event.session_id].append(event)

    def get_events_by_session(self, session_id: str) -> List[AnalyticsEventInternal]:
        """Get all events for a session."""
        return self.sessions.get(session_id, [])

    def get_events_in_range(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[AnalyticsEventInternal]:
        """Get events within a date range."""
        filtered = self.events

        if start_date:
            filtered = [e for e in filtered if e.timestamp >= start_date]
        if end_date:
            filtered = [e for e in filtered if e.timestamp <= end_date]

        return filtered

    def get_all_sessions(self) -> Dict[str, List[AnalyticsEventInternal]]:
        """Get all sessions with their events."""
        return dict(self.sessions)


# Global store instance
_analytics_store = AnalyticsStore()


# =============================================================================
# ANALYTICS SERVICE
# =============================================================================

class AnalyticsService:
    """
    Service for tracking and analyzing user events.

    R&D COMPLIANCE:
    - Rule #5: Events stored in chronological order
    - Rule #6: Full traceability with timestamps
    """

    def __init__(self, store: Optional[AnalyticsStore] = None):
        """Initialize the analytics service."""
        self.store = store or _analytics_store

    # =========================================================================
    # EVENT TRACKING
    # =========================================================================

    def _categorize_event(self, event_name: str) -> Tuple[EventCategory, Optional[int]]:
        """
        Categorize an event and determine funnel step if applicable.

        Returns:
            Tuple of (category, funnel_step) where funnel_step is 1-5 or None
        """
        normalized_name = event_name.lower().strip()

        # Check if it's a funnel event
        if normalized_name in FUNNEL_STEPS:
            funnel_step = FUNNEL_STEPS.index(normalized_name) + 1
            return EventCategory.FUNNEL, funnel_step

        # Categorize other events
        if "error" in normalized_name or "exception" in normalized_name:
            return EventCategory.ERROR, None
        elif "navigate" in normalized_name or "page" in normalized_name:
            return EventCategory.NAVIGATION, None
        elif "performance" in normalized_name or "timing" in normalized_name:
            return EventCategory.PERFORMANCE, None
        elif "system" in normalized_name:
            return EventCategory.SYSTEM, None
        else:
            return EventCategory.INTERACTION, None

    def _validate_event(self, event: AnalyticsEventCreate) -> List[str]:
        """
        Validate an analytics event.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not event.name:
            errors.append("Event name is required")
        elif len(event.name) > 100:
            errors.append("Event name must be 100 characters or less")

        if not event.session_id:
            errors.append("Session ID is required")

        if event.timestamp and event.timestamp > datetime.utcnow() + timedelta(hours=1):
            errors.append("Event timestamp cannot be more than 1 hour in the future")

        return errors

    async def track_event(
        self,
        event: AnalyticsEventCreate,
    ) -> AnalyticsEventResponse:
        """
        Track a single analytics event.

        Args:
            event: The event to track

        Returns:
            The tracked event with server-assigned ID and timestamp

        Raises:
            ValueError: If event validation fails
        """
        # Validate event
        errors = self._validate_event(event)
        if errors:
            raise ValueError("; ".join(errors))

        # Categorize event
        category, funnel_step = self._categorize_event(event.name)

        # Create internal event
        event_id = str(uuid4())
        now = datetime.utcnow()

        internal_event = AnalyticsEventInternal(
            id=event_id,
            name=event.name,
            timestamp=event.timestamp or now,
            session_id=event.session_id,
            user_id=event.user_id,
            properties=event.properties or {},
            page=event.page,
            referrer=event.referrer,
            created_at=now,
            category=category,
            funnel_step=funnel_step,
        )

        # Store event
        self.store.add_event(internal_event)

        logger.info(
            f"Event tracked: {event.name} | session={event.session_id} | "
            f"category={category.value} | funnel_step={funnel_step}"
        )

        # Return response
        return AnalyticsEventResponse(
            id=event_id,
            name=internal_event.name,
            timestamp=internal_event.timestamp,
            session_id=internal_event.session_id,
            user_id=internal_event.user_id,
            properties=internal_event.properties,
            page=internal_event.page,
            referrer=internal_event.referrer,
            created_at=internal_event.created_at,
        )

    async def track_batch(
        self,
        events: List[AnalyticsEventCreate],
    ) -> AnalyticsEventBatchResponse:
        """
        Track a batch of analytics events.

        Args:
            events: List of events to track

        Returns:
            Batch response with success/failure counts
        """
        tracked_events: List[AnalyticsEventResponse] = []
        errors: List[str] = []

        for i, event in enumerate(events):
            try:
                tracked = await self.track_event(event)
                tracked_events.append(tracked)
            except Exception as e:
                error_msg = f"Event {i + 1}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Failed to track event: {error_msg}")

        success = len(errors) == 0

        logger.info(
            f"Batch tracking complete: {len(tracked_events)} tracked, "
            f"{len(errors)} failed"
        )

        return AnalyticsEventBatchResponse(
            success=success,
            tracked_count=len(tracked_events),
            failed_count=len(errors),
            events=tracked_events,
            errors=errors,
        )

    # =========================================================================
    # FUNNEL ANALYSIS
    # =========================================================================

    def _get_session_funnel_progress(
        self,
        session_events: List[AnalyticsEventInternal],
    ) -> Tuple[int, Dict[int, datetime]]:
        """
        Calculate funnel progress for a session.

        Returns:
            Tuple of (max_step_reached, step_timestamps)
        """
        step_timestamps: Dict[int, datetime] = {}

        for event in sorted(session_events, key=lambda e: e.timestamp):
            if event.funnel_step and event.funnel_step not in step_timestamps:
                step_timestamps[event.funnel_step] = event.timestamp

        max_step = max(step_timestamps.keys()) if step_timestamps else 0

        return max_step, step_timestamps

    async def get_funnel_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        session_id: Optional[str] = None,
    ) -> FunnelMetrics:
        """
        Calculate funnel metrics.

        Args:
            start_date: Filter events from this date
            end_date: Filter events until this date
            session_id: Filter by specific session

        Returns:
            Complete funnel metrics
        """
        # Get relevant events
        events = self.store.get_events_in_range(start_date, end_date)

        # Filter by session if specified
        if session_id:
            events = [e for e in events if e.session_id == session_id]

        # Group by session
        sessions: Dict[str, List[AnalyticsEventInternal]] = defaultdict(list)
        for event in events:
            sessions[event.session_id].append(event)

        total_sessions = len(sessions)

        if total_sessions == 0:
            return FunnelMetrics(
                steps=[
                    FunnelStep(
                        step=i + 1,
                        name=FUNNEL_STEP_NAMES[i + 1],
                        completed=0,
                        conversion_rate=0.0,
                    )
                    for i in range(5)
                ],
                total_sessions=0,
                completed_sessions=0,
                overall_conversion_rate=0.0,
                start_date=start_date,
                end_date=end_date,
            )

        # Calculate step completions
        step_completions: Dict[int, int] = {i: 0 for i in range(1, 6)}
        step_timestamps: Dict[int, List[datetime]] = {i: [] for i in range(1, 6)}
        step_durations: Dict[int, List[float]] = {i: [] for i in range(2, 6)}  # Duration from previous step
        completed_sessions = 0
        total_duration = 0.0
        duration_count = 0

        for session_id, session_events in sessions.items():
            max_step, timestamps = self._get_session_funnel_progress(session_events)

            # Count completions for each step reached
            for step in range(1, max_step + 1):
                step_completions[step] += 1
                if step in timestamps:
                    step_timestamps[step].append(timestamps[step])

                    # Calculate duration from previous step
                    if step > 1 and (step - 1) in timestamps:
                        duration = (timestamps[step] - timestamps[step - 1]).total_seconds()
                        step_durations[step].append(duration)

            # Track completed sessions
            if max_step == 5:
                completed_sessions += 1
                if 1 in timestamps and 5 in timestamps:
                    total_duration += (timestamps[5] - timestamps[1]).total_seconds()
                    duration_count += 1

        # Build step metrics
        funnel_steps: List[FunnelStep] = []
        prev_completions = total_sessions

        for i in range(1, 6):
            completions = step_completions[i]

            # Calculate conversion rate from previous step
            if i == 1:
                conversion_rate = (completions / total_sessions * 100) if total_sessions > 0 else 0.0
            else:
                conversion_rate = (completions / prev_completions * 100) if prev_completions > 0 else 0.0

            # Calculate average timestamp
            avg_timestamp = None
            if step_timestamps[i]:
                avg_ts = sum(t.timestamp() for t in step_timestamps[i]) / len(step_timestamps[i])
                avg_timestamp = datetime.fromtimestamp(avg_ts)

            # Calculate average duration from previous step
            avg_duration = None
            if i > 1 and step_durations[i]:
                avg_duration = sum(step_durations[i]) / len(step_durations[i])

            funnel_steps.append(FunnelStep(
                step=i,
                name=FUNNEL_STEP_NAMES[i],
                completed=completions,
                timestamp=avg_timestamp,
                duration=avg_duration,
                conversion_rate=round(conversion_rate, 2),
            ))

            prev_completions = completions

        # Calculate overall metrics
        overall_conversion = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0.0
        avg_total_duration = (total_duration / duration_count) if duration_count > 0 else None

        return FunnelMetrics(
            steps=funnel_steps,
            total_sessions=total_sessions,
            completed_sessions=completed_sessions,
            overall_conversion_rate=round(overall_conversion, 2),
            average_duration=avg_total_duration,
            start_date=start_date,
            end_date=end_date,
        )

    # =========================================================================
    # SESSION ANALYSIS
    # =========================================================================

    async def get_session_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_events: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> SessionStatsResponse:
        """
        Get session statistics.

        Args:
            start_date: Filter sessions starting from this date
            end_date: Filter sessions until this date
            min_events: Minimum events per session
            limit: Maximum sessions to return
            offset: Pagination offset

        Returns:
            Session statistics response
        """
        # Get all events in range
        events = self.store.get_events_in_range(start_date, end_date)

        # Group by session
        sessions_dict: Dict[str, List[AnalyticsEventInternal]] = defaultdict(list)
        for event in events:
            sessions_dict[event.session_id].append(event)

        # Filter by minimum events
        if min_events:
            sessions_dict = {
                sid: evts for sid, evts in sessions_dict.items()
                if len(evts) >= min_events
            }

        total_count = len(sessions_dict)

        # Calculate stats for each session
        session_stats_list: List[SessionStats] = []
        total_events = 0
        total_duration = 0.0
        funnel_completions = 0

        # Sort sessions by first event timestamp (R&D Rule #5: Chronological)
        sorted_sessions = sorted(
            sessions_dict.items(),
            key=lambda x: min(e.timestamp for e in x[1]),
            reverse=True,  # Most recent first
        )

        for session_id, session_events in sorted_sessions:
            # Calculate metrics
            events_count = len(session_events)
            total_events += events_count

            sorted_events = sorted(session_events, key=lambda e: e.timestamp)
            first_event = sorted_events[0]
            last_event = sorted_events[-1]

            duration = (last_event.timestamp - first_event.timestamp).total_seconds()
            total_duration += duration

            # Get funnel progress
            funnel_progress, _ = self._get_session_funnel_progress(session_events)
            funnel_completed = funnel_progress >= 5
            if funnel_completed:
                funnel_completions += 1

            # Get unique pages
            pages_viewed = list(set(
                e.page for e in session_events if e.page
            ))

            # Get user_id (take first non-null)
            user_id = next(
                (e.user_id for e in session_events if e.user_id),
                None
            )

            session_stats_list.append(SessionStats(
                session_id=session_id,
                user_id=user_id,
                events_count=events_count,
                funnel_progress=funnel_progress,
                funnel_completed=funnel_completed,
                first_event_at=first_event.timestamp,
                last_event_at=last_event.timestamp,
                duration_seconds=duration,
                pages_viewed=pages_viewed,
            ))

        # Apply pagination
        paginated_sessions = session_stats_list[offset:offset + limit]

        # Calculate averages
        avg_events = (total_events / total_count) if total_count > 0 else 0.0
        avg_duration = (total_duration / total_count) if total_count > 0 else 0.0
        funnel_rate = (funnel_completions / total_count * 100) if total_count > 0 else 0.0

        return SessionStatsResponse(
            sessions=paginated_sessions,
            total_count=total_count,
            average_events_per_session=round(avg_events, 2),
            average_duration=round(avg_duration, 2),
            funnel_completion_rate=round(funnel_rate, 2),
        )

    # =========================================================================
    # UTILITIES
    # =========================================================================

    async def get_event_count(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> int:
        """Get total event count in date range."""
        events = self.store.get_events_in_range(start_date, end_date)
        return len(events)

    async def get_session_count(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> int:
        """Get unique session count in date range."""
        events = self.store.get_events_in_range(start_date, end_date)
        sessions = set(e.session_id for e in events)
        return len(sessions)


# =============================================================================
# SERVICE FACTORY
# =============================================================================

def get_analytics_service() -> AnalyticsService:
    """
    Factory function to get an AnalyticsService instance.

    In production, this would accept a database session parameter.
    """
    return AnalyticsService()


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "AnalyticsService",
    "AnalyticsStore",
    "get_analytics_service",
    "FUNNEL_STEPS",
    "FUNNEL_STEP_NAMES",
]
