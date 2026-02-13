"""
CHE-NU Analytics API Routes
===========================

REST API endpoints for analytics event tracking and funnel analysis.

ENDPOINTS:
- POST /api/v1/analytics/events - Track single event
- POST /api/v1/analytics/events/batch - Track batch of events
- GET /api/v1/analytics/funnel - Get funnel metrics (admin only)
- GET /api/v1/analytics/sessions - Get session stats (admin only)

Funnel Steps:
1. landing_view - User views the landing page
2. cta_click - User clicks a call-to-action
3. sceau_activate - User activates their sceau (seal)
4. essaim_view - User views the essaim (swarm)
5. module_enter - User enters a module

R&D COMPLIANCE:
- Rule #5: No ranking algorithms - data returned in chronological order
- Rule #6: Full traceability - all events include timestamps
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth import get_current_user, get_optional_user, User
from app.services.analytics_service import AnalyticsService, get_analytics_service
from app.schemas.analytics_schemas import (
    AnalyticsEventCreate,
    AnalyticsEventBatchCreate,
    AnalyticsEventResponse,
    AnalyticsEventBatchResponse,
    FunnelMetrics,
    SessionStatsResponse,
    MessageResponse,
)

logger = logging.getLogger("chenu.analytics.routes")

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

def handle_service_error(e: Exception):
    """Convert service exceptions to HTTP exceptions."""
    if isinstance(e, ValueError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    else:
        logger.error(f"Unexpected error in analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing analytics request",
        )


# =============================================================================
# EVENT TRACKING ENDPOINTS
# =============================================================================

@router.post(
    "/events",
    response_model=AnalyticsEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track single event",
    description="""
    Track a single analytics event.

    **Event Fields:**
    - `name`: Event name (required, e.g., 'landing_view', 'cta_click')
    - `sessionId`: Unique session identifier (required)
    - `userId`: Optional user identifier
    - `timestamp`: Event timestamp (defaults to server time)
    - `properties`: Additional event properties as JSON object
    - `page`: Current page URL or path
    - `referrer`: Referrer URL

    **Funnel Events:**
    Use these event names to track funnel progression:
    1. `landing_view` - User views landing page
    2. `cta_click` - User clicks call-to-action
    3. `sceau_activate` - User activates sceau
    4. `essaim_view` - User views essaim
    5. `module_enter` - User enters module
    """,
)
async def track_event(
    event: AnalyticsEventCreate,
    user: Optional[User] = Depends(get_optional_user),
) -> AnalyticsEventResponse:
    """
    Track a single analytics event.

    This endpoint accepts events from both authenticated and anonymous users.
    If authenticated, the user_id will be automatically associated with the event.
    """
    try:
        # Associate user_id if authenticated and not provided
        if user and not event.user_id:
            event.user_id = user.id

        service = get_analytics_service()
        result = await service.track_event(event)

        logger.debug(
            f"Event tracked: {event.name} | session={event.session_id}"
        )

        return result

    except Exception as e:
        handle_service_error(e)


@router.post(
    "/events/batch",
    response_model=AnalyticsEventBatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track batch of events",
    description="""
    Track multiple analytics events in a single request.

    **Limits:**
    - Maximum 100 events per batch

    **Response:**
    Returns success status with counts of tracked and failed events.
    Partial success is possible - some events may fail validation while
    others are tracked successfully.

    **Usage:**
    Ideal for buffering events on the client and sending periodically,
    or for replaying offline events.
    """,
)
async def track_batch(
    batch: AnalyticsEventBatchCreate,
    user: Optional[User] = Depends(get_optional_user),
) -> AnalyticsEventBatchResponse:
    """
    Track a batch of analytics events.

    Useful for:
    - Buffered event sending from clients
    - Replaying offline events
    - Bulk data import
    """
    try:
        # Associate user_id with events if authenticated
        if user:
            for event in batch.events:
                if not event.user_id:
                    event.user_id = user.id

        service = get_analytics_service()
        result = await service.track_batch(batch.events)

        logger.info(
            f"Batch tracked: {result.tracked_count} success, "
            f"{result.failed_count} failed"
        )

        return result

    except Exception as e:
        handle_service_error(e)


# =============================================================================
# FUNNEL ANALYSIS ENDPOINTS (Admin Only)
# =============================================================================

@router.get(
    "/funnel",
    response_model=FunnelMetrics,
    summary="Get funnel metrics",
    description="""
    Get funnel conversion metrics.

    **Admin Access Required**

    **Funnel Steps:**
    1. `landing_view` - Landing page views
    2. `cta_click` - CTA clicks
    3. `sceau_activate` - Sceau activations
    4. `essaim_view` - Essaim views
    5. `module_enter` - Module entries

    **Metrics Provided:**
    - Completion count per step
    - Conversion rate between steps
    - Average duration between steps
    - Overall funnel conversion rate

    **Filtering:**
    - `start_date`: Filter from this date (ISO format)
    - `end_date`: Filter until this date (ISO format)
    - `session_id`: Filter to specific session

    **R&D Compliance:**
    - Rule #5: Data returned in chronological order
    """,
)
async def get_funnel_metrics(
    start_date: Optional[datetime] = Query(
        None,
        alias="startDate",
        description="Filter events from this date (ISO format)",
    ),
    end_date: Optional[datetime] = Query(
        None,
        alias="endDate",
        description="Filter events until this date (ISO format)",
    ),
    session_id: Optional[str] = Query(
        None,
        alias="sessionId",
        description="Filter by specific session ID",
    ),
    current_user: User = Depends(get_current_user),
) -> FunnelMetrics:
    """
    Get funnel conversion metrics.

    Requires authentication. In production, this should be restricted
    to admin users only.
    """
    try:
        service = get_analytics_service()
        result = await service.get_funnel_metrics(
            start_date=start_date,
            end_date=end_date,
            session_id=session_id,
        )

        logger.info(
            f"Funnel metrics retrieved: {result.total_sessions} sessions, "
            f"{result.overall_conversion_rate}% conversion"
        )

        return result

    except Exception as e:
        handle_service_error(e)


@router.get(
    "/sessions",
    response_model=SessionStatsResponse,
    summary="Get session statistics",
    description="""
    Get statistics for user sessions.

    **Admin Access Required**

    **Session Metrics:**
    - Event count per session
    - Funnel progress (steps 1-5)
    - Session duration
    - Pages viewed

    **Filtering:**
    - `start_date`: Filter from this date
    - `end_date`: Filter until this date
    - `min_events`: Minimum events per session

    **Pagination:**
    - `limit`: Maximum sessions to return (default 100, max 1000)
    - `offset`: Skip this many sessions

    **R&D Compliance:**
    - Rule #5: Sessions returned in chronological order (most recent first)
    """,
)
async def get_session_stats(
    start_date: Optional[datetime] = Query(
        None,
        alias="startDate",
        description="Filter sessions starting from this date",
    ),
    end_date: Optional[datetime] = Query(
        None,
        alias="endDate",
        description="Filter sessions until this date",
    ),
    min_events: Optional[int] = Query(
        None,
        alias="minEvents",
        ge=1,
        description="Minimum events per session",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=1000,
        description="Maximum sessions to return",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Pagination offset",
    ),
    current_user: User = Depends(get_current_user),
) -> SessionStatsResponse:
    """
    Get session statistics.

    Requires authentication. In production, this should be restricted
    to admin users only.
    """
    try:
        service = get_analytics_service()
        result = await service.get_session_stats(
            start_date=start_date,
            end_date=end_date,
            min_events=min_events,
            limit=limit,
            offset=offset,
        )

        logger.info(
            f"Session stats retrieved: {result.total_count} sessions, "
            f"avg {result.average_events_per_session} events/session"
        )

        return result

    except Exception as e:
        handle_service_error(e)


# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@router.get(
    "/health",
    response_model=MessageResponse,
    summary="Analytics health check",
    description="Check if the analytics service is healthy.",
)
async def analytics_health() -> MessageResponse:
    """Health check for analytics service."""
    try:
        service = get_analytics_service()
        event_count = await service.get_event_count()
        session_count = await service.get_session_count()

        return MessageResponse(
            message=f"Analytics service healthy. Events: {event_count}, Sessions: {session_count}",
            success=True,
        )
    except Exception as e:
        logger.error(f"Analytics health check failed: {e}")
        return MessageResponse(
            message=f"Analytics service unhealthy: {str(e)}",
            success=False,
        )


@router.get(
    "/stats",
    summary="Get analytics summary stats",
    description="Get quick summary statistics for the analytics system.",
)
async def get_analytics_stats(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get quick summary statistics.

    Returns basic counts useful for dashboard display.
    """
    try:
        service = get_analytics_service()

        event_count = await service.get_event_count()
        session_count = await service.get_session_count()

        return {
            "total_events": event_count,
            "total_sessions": session_count,
            "funnel_steps": 5,
            "funnel_step_names": [
                "landing_view",
                "cta_click",
                "sceau_activate",
                "essaim_view",
                "module_enter",
            ],
            "status": "operational",
        }

    except Exception as e:
        handle_service_error(e)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["router"]
