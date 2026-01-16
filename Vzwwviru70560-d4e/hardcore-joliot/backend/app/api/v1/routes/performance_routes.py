"""
CHE·NU™ Performance API Routes
===============================

API endpoints for performance monitoring, health checks, 
and cache management.

Endpoints:
- GET /health - Basic health check
- GET /health/detailed - Detailed health status
- GET /metrics - Performance metrics
- GET /metrics/dashboard - Dashboard data
- GET /cache/stats - Cache statistics
- POST /cache/invalidate - Cache invalidation
- GET /queries/stats - Query statistics

Author: CHE·NU Backend Team
Version: 1.0.0
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from pydantic import BaseModel, Field

from ..core.cache import (
    cache_service,
    CacheKeyBuilder,
    CacheRegion,
    query_profiler,
    index_analyzer,
    performance_monitor,
    HealthStatus,
)

router = APIRouter(tags=["Performance & Monitoring"])


# ==========================================================================
# Request/Response Schemas
# ==========================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str = "1.0.0"


class DetailedHealthResponse(BaseModel):
    """Detailed health response."""
    status: str
    timestamp: str
    version: str
    checks: Dict[str, Any]
    resources: Dict[str, Any]


class MetricsResponse(BaseModel):
    """Metrics response."""
    histograms: Dict[str, Any]
    counters: Dict[str, Any]
    gauges: Dict[str, Any]


class DashboardResponse(BaseModel):
    """Dashboard data response."""
    timestamp: str
    requests: Dict[str, Any]
    governance: Dict[str, Any]
    connections: Dict[str, Any]
    resources: Dict[str, Any]
    health: Dict[str, Any]
    alerts: List[Dict[str, Any]]


class CacheStatsResponse(BaseModel):
    """Cache statistics response."""
    hits: int
    misses: int
    sets: int
    deletes: int
    hit_rate: float
    bytes_stored: int
    mode: str


class CacheInvalidateRequest(BaseModel):
    """Cache invalidation request."""
    pattern: Optional[str] = Field(None, description="Pattern to invalidate (e.g., 'chenu:thread:*')")
    tag: Optional[str] = Field(None, description="Tag to invalidate")
    key: Optional[str] = Field(None, description="Specific key to invalidate")


class CacheInvalidateResponse(BaseModel):
    """Cache invalidation response."""
    success: bool
    keys_invalidated: int
    message: str


class QueryStatsResponse(BaseModel):
    """Query statistics response."""
    total_queries: int
    avg_query_time_ms: float
    slow_queries: int
    n_plus_1_detected: int
    full_scans: int
    queries_by_complexity: Dict[str, int]
    slowest_queries: List[Dict[str, Any]]


class IndexRecommendationResponse(BaseModel):
    """Index recommendation response."""
    table: str
    columns: List[str]
    reason: str
    estimated_improvement: str
    create_statement: str
    priority: str


# ==========================================================================
# Health Endpoints
# ==========================================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Basic Health Check",
    description="Returns basic health status. Use for load balancer health checks.",
)
async def health_check():
    """
    Basic health check endpoint.
    
    Returns 200 if service is running.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    summary="Detailed Health Check",
    description="Returns detailed health status including all subsystem checks.",
)
async def detailed_health_check():
    """
    Detailed health check with subsystem status.
    
    Checks:
    - Database connection
    - Redis connection
    - Cache health
    - System resources
    """
    # Run all health checks
    check_results = await performance_monitor.run_health_checks()
    overall_status = await performance_monitor.get_overall_health()
    
    # Get system resources
    resources = performance_monitor.get_system_resources()
    
    return DetailedHealthResponse(
        status=overall_status.value,
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        checks={
            name: {
                "status": check.status.value,
                "message": check.message,
                "latency_ms": check.latency_ms,
                "details": check.details,
            }
            for name, check in check_results.items()
        },
        resources=resources,
    )


@router.get(
    "/health/ready",
    summary="Readiness Check",
    description="Returns 200 if service is ready to accept traffic.",
)
async def readiness_check():
    """
    Kubernetes-style readiness check.
    
    Returns 503 if not ready to accept traffic.
    """
    overall = await performance_monitor.get_overall_health()
    
    if overall == HealthStatus.UNHEALTHY:
        raise HTTPException(
            status_code=503,
            detail="Service not ready",
        )
    
    return {"status": "ready"}


@router.get(
    "/health/live",
    summary="Liveness Check",
    description="Returns 200 if service is alive.",
)
async def liveness_check():
    """
    Kubernetes-style liveness check.
    
    Simple check that service is responding.
    """
    return {"status": "alive"}


# ==========================================================================
# Metrics Endpoints
# ==========================================================================

@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="Get All Metrics",
    description="Returns all performance metrics.",
)
async def get_metrics():
    """
    Get all performance metrics.
    
    Includes histograms, counters, and gauges.
    """
    return performance_monitor.get_metrics_summary()


@router.get(
    "/metrics/dashboard",
    response_model=DashboardResponse,
    summary="Get Dashboard Data",
    description="Returns aggregated data for performance dashboard.",
)
async def get_dashboard_data():
    """
    Get dashboard data for monitoring UI.
    
    Includes:
    - Request statistics
    - Governance events
    - Active connections
    - System resources
    - Health status
    - Active alerts
    """
    return performance_monitor.get_dashboard_data()


@router.get(
    "/metrics/alerts",
    summary="Get Active Alerts",
    description="Returns current performance alerts.",
)
async def get_alerts():
    """
    Get current performance alerts.
    
    Alerts are triggered when metrics exceed thresholds.
    """
    return {
        "alerts": performance_monitor.check_alerts(),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post(
    "/metrics/reset",
    summary="Reset Metrics",
    description="Reset all performance metrics. Use with caution.",
)
async def reset_metrics():
    """
    Reset all performance metrics.
    
    ⚠️ This clears all collected metrics data.
    """
    performance_monitor.reset_metrics()
    
    return {
        "success": True,
        "message": "Metrics reset",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==========================================================================
# Cache Endpoints
# ==========================================================================

@router.get(
    "/cache/stats",
    response_model=CacheStatsResponse,
    summary="Get Cache Statistics",
    description="Returns cache hit/miss statistics.",
)
async def get_cache_stats():
    """
    Get cache statistics.
    
    Includes hit rate, total operations, and memory usage.
    """
    stats = cache_service.get_stats()
    info = await cache_service.get_info()
    
    return CacheStatsResponse(
        hits=stats["hits"],
        misses=stats["misses"],
        sets=stats["sets"],
        deletes=stats["deletes"],
        hit_rate=stats["hit_rate"],
        bytes_stored=stats["bytes_stored"],
        mode=info["mode"],
    )


@router.get(
    "/cache/info",
    summary="Get Cache Info",
    description="Returns detailed cache information.",
)
async def get_cache_info():
    """
    Get detailed cache information.
    
    Includes tags, key counts, and mode.
    """
    return await cache_service.get_info()


@router.post(
    "/cache/invalidate",
    response_model=CacheInvalidateResponse,
    summary="Invalidate Cache",
    description="Invalidate cache entries by pattern, tag, or key.",
)
async def invalidate_cache(
    request: CacheInvalidateRequest,
):
    """
    Invalidate cache entries.
    
    Methods:
    - By pattern: Use wildcards like 'chenu:thread:*'
    - By tag: Invalidate all entries with specific tag
    - By key: Invalidate single key
    """
    if request.key:
        # Single key
        await cache_service.delete(request.key)
        return CacheInvalidateResponse(
            success=True,
            keys_invalidated=1,
            message=f"Deleted key: {request.key}",
        )
    
    if request.tag:
        # By tag
        count = await cache_service.invalidate_by_tag(request.tag)
        return CacheInvalidateResponse(
            success=True,
            keys_invalidated=count,
            message=f"Invalidated {count} keys with tag: {request.tag}",
        )
    
    if request.pattern:
        # By pattern
        count = await cache_service.invalidate_by_pattern(request.pattern)
        return CacheInvalidateResponse(
            success=True,
            keys_invalidated=count,
            message=f"Invalidated {count} keys matching: {request.pattern}",
        )
    
    raise HTTPException(
        status_code=400,
        detail="Must provide pattern, tag, or key",
    )


@router.post(
    "/cache/invalidate/thread/{thread_id}",
    response_model=CacheInvalidateResponse,
    summary="Invalidate Thread Cache",
    description="Invalidate all cache entries for a specific thread.",
)
async def invalidate_thread_cache(thread_id: UUID):
    """
    Invalidate all cache entries for a thread.
    
    Useful when thread is updated and cache needs refresh.
    """
    count = await cache_service.invalidate_thread(thread_id)
    
    return CacheInvalidateResponse(
        success=True,
        keys_invalidated=count,
        message=f"Invalidated {count} keys for thread {thread_id}",
    )


@router.post(
    "/cache/invalidate/user/{user_id}",
    response_model=CacheInvalidateResponse,
    summary="Invalidate User Cache",
    description="Invalidate all cache entries for a specific user.",
)
async def invalidate_user_cache(user_id: UUID):
    """
    Invalidate all cache entries for a user.
    
    Useful when user preferences or permissions change.
    """
    count = await cache_service.invalidate_user(user_id)
    
    return CacheInvalidateResponse(
        success=True,
        keys_invalidated=count,
        message=f"Invalidated {count} keys for user {user_id}",
    )


@router.post(
    "/cache/clear",
    summary="Clear All Cache",
    description="⚠️ Clear entire cache. Use with extreme caution.",
)
async def clear_cache():
    """
    Clear entire cache.
    
    ⚠️ WARNING: This will clear ALL cached data.
    Only use in emergencies or testing.
    """
    await cache_service.clear()
    
    return {
        "success": True,
        "message": "Cache cleared",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==========================================================================
# Query Statistics Endpoints
# ==========================================================================

@router.get(
    "/queries/stats",
    response_model=QueryStatsResponse,
    summary="Get Query Statistics",
    description="Returns database query statistics.",
)
async def get_query_stats():
    """
    Get database query statistics.
    
    Includes:
    - Query counts and timing
    - Slow query detection
    - N+1 query detection
    - Query complexity distribution
    """
    stats = query_profiler.get_stats()
    
    return QueryStatsResponse(
        total_queries=stats["total_queries"],
        avg_query_time_ms=stats["avg_query_time_ms"],
        slow_queries=stats["slow_queries"],
        n_plus_1_detected=stats["n_plus_1_detected"],
        full_scans=stats["full_scans"],
        queries_by_complexity=stats["queries_by_complexity"],
        slowest_queries=stats.get("slowest_queries", []),
    )


@router.get(
    "/queries/n-plus-1",
    summary="Get N+1 Detections",
    description="Returns detected N+1 query patterns.",
)
async def get_n_plus_1_detections():
    """
    Get detected N+1 query patterns.
    
    N+1 queries are a common performance anti-pattern.
    """
    stats = query_profiler.get_stats()
    
    return {
        "detections": stats.get("n_plus_1_detections", []),
        "count": stats["n_plus_1_detected"],
    }


@router.get(
    "/queries/slow",
    summary="Get Slow Queries",
    description="Returns the slowest queries.",
)
async def get_slow_queries(
    limit: int = Query(10, ge=1, le=50),
):
    """
    Get slowest queries.
    
    Args:
        limit: Maximum number of queries to return
    """
    stats = query_profiler.get_stats()
    
    return {
        "slow_queries": stats.get("slowest_queries", [])[:limit],
        "threshold_ms": query_profiler.slow_threshold_ms,
    }


@router.get(
    "/queries/index-recommendations",
    summary="Get Index Recommendations",
    description="Returns recommended database indexes.",
)
async def get_index_recommendations(
    min_usage: int = Query(5, ge=1),
):
    """
    Get database index recommendations.
    
    Based on query analysis, suggests indexes that could improve performance.
    
    Args:
        min_usage: Minimum column usage count to recommend
    """
    recommendations = index_analyzer.get_recommendations(min_usage=min_usage)
    
    return {
        "recommendations": [
            {
                "table": r.table,
                "columns": r.columns,
                "reason": r.reason,
                "estimated_improvement": r.estimated_improvement,
                "create_statement": r.create_statement,
                "priority": r.priority,
            }
            for r in recommendations
        ],
        "count": len(recommendations),
    }


@router.post(
    "/queries/reset",
    summary="Reset Query Statistics",
    description="Reset all query statistics.",
)
async def reset_query_stats():
    """
    Reset query statistics.
    
    Clears all collected query profiling data.
    """
    query_profiler.reset()
    index_analyzer.clear()
    
    return {
        "success": True,
        "message": "Query statistics reset",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==========================================================================
# Exports
# ==========================================================================

__all__ = ["router"]
