"""
SERVICE: performance_monitor.py
SPHERE: Core
VERSION: 1.0.0
INTENT: Real-time performance monitoring with metrics, alerts, and profiling

CHE·NU™ Performance Monitoring:
- Request timing and percentiles
- Resource utilization tracking
- Memory profiling
- Alert thresholds
- Health scoring

R&D COMPLIANCE: ✅
- Rule #6: Full observability and traceability
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque, defaultdict
from contextlib import asynccontextmanager
from functools import wraps
from enum import Enum
import statistics
import asyncio
import psutil
import time
import logging
import gc
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# METRICS TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class MetricType(str, Enum):
    """Types of metrics"""
    COUNTER = "counter"         # Monotonic increasing
    GAUGE = "gauge"             # Point-in-time value
    HISTOGRAM = "histogram"     # Distribution
    TIMER = "timer"             # Duration measurement

class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class MetricPoint:
    """Single metric data point"""
    
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class Alert:
    """Performance alert"""
    
    id: str
    severity: AlertSeverity
    metric_name: str
    message: str
    value: float
    threshold: float
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged: bool = False

@dataclass
class HealthScore:
    """System health score"""
    
    overall: float              # 0-100
    api_latency: float          # 0-100
    error_rate: float           # 0-100
    memory_usage: float         # 0-100
    cpu_usage: float            # 0-100
    cache_hit_rate: float       # 0-100
    database_health: float      # 0-100
    calculated_at: datetime = field(default_factory=datetime.utcnow)

# ═══════════════════════════════════════════════════════════════════════════════
# HISTOGRAM
# ═══════════════════════════════════════════════════════════════════════════════

class Histogram:
    """
    Histogram for tracking value distributions.
    
    Features:
    - Rolling window
    - Percentile calculation
    - Min/max/avg tracking
    """
    
    def __init__(self, window_size: int = 1000, window_seconds: int = 300):
        self.window_size = window_size
        self.window_seconds = window_seconds
        self._values: deque = deque(maxlen=window_size)
        self._timestamps: deque = deque(maxlen=window_size)
        self._count = 0
        self._sum = 0.0
        self._min = float('inf')
        self._max = float('-inf')
    
    def observe(self, value: float) -> None:
        """Record observation"""
        now = datetime.utcnow()
        
        self._values.append(value)
        self._timestamps.append(now)
        self._count += 1
        self._sum += value
        self._min = min(self._min, value)
        self._max = max(self._max, value)
        
        # Remove old values outside window
        self._cleanup()
    
    def _cleanup(self) -> None:
        """Remove values outside time window"""
        cutoff = datetime.utcnow() - timedelta(seconds=self.window_seconds)
        
        while self._timestamps and self._timestamps[0] < cutoff:
            old_value = self._values.popleft()
            self._timestamps.popleft()
            self._sum -= old_value
    
    def percentile(self, p: float) -> float:
        """Calculate percentile (0-100)"""
        if not self._values:
            return 0.0
        
        sorted_values = sorted(self._values)
        idx = int((p / 100) * len(sorted_values))
        idx = min(idx, len(sorted_values) - 1)
        return sorted_values[idx]
    
    @property
    def count(self) -> int:
        return len(self._values)
    
    @property
    def mean(self) -> float:
        if not self._values:
            return 0.0
        return statistics.mean(self._values)
    
    @property
    def median(self) -> float:
        if not self._values:
            return 0.0
        return statistics.median(self._values)
    
    @property
    def stddev(self) -> float:
        if len(self._values) < 2:
            return 0.0
        return statistics.stdev(self._values)
    
    @property
    def min(self) -> float:
        if not self._values:
            return 0.0
        return min(self._values)
    
    @property
    def max(self) -> float:
        if not self._values:
            return 0.0
        return max(self._values)
    
    def summary(self) -> Dict[str, float]:
        """Get histogram summary"""
        return {
            "count": self.count,
            "mean": round(self.mean, 3),
            "median": round(self.median, 3),
            "stddev": round(self.stddev, 3),
            "min": round(self.min, 3),
            "max": round(self.max, 3),
            "p50": round(self.percentile(50), 3),
            "p90": round(self.percentile(90), 3),
            "p95": round(self.percentile(95), 3),
            "p99": round(self.percentile(99), 3),
        }

# ═══════════════════════════════════════════════════════════════════════════════
# RATE CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════

class RateCalculator:
    """Calculate rates over time windows"""
    
    def __init__(self, window_seconds: int = 60):
        self.window_seconds = window_seconds
        self._events: deque = deque()
    
    def record(self) -> None:
        """Record event"""
        now = time.time()
        self._events.append(now)
        self._cleanup(now)
    
    def _cleanup(self, now: float) -> None:
        """Remove old events"""
        cutoff = now - self.window_seconds
        while self._events and self._events[0] < cutoff:
            self._events.popleft()
    
    @property
    def rate(self) -> float:
        """Events per second"""
        self._cleanup(time.time())
        if not self._events or self.window_seconds == 0:
            return 0.0
        return len(self._events) / self.window_seconds
    
    @property
    def count(self) -> int:
        """Events in window"""
        self._cleanup(time.time())
        return len(self._events)

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE MONITOR
# ═══════════════════════════════════════════════════════════════════════════════

class PerformanceMonitor:
    """
    Comprehensive performance monitoring service.
    
    Features:
    - Request timing with percentiles
    - Error rate tracking
    - Resource monitoring (CPU, memory)
    - Cache performance
    - Alert thresholds
    - Health scoring
    """
    
    def __init__(
        self,
        alert_latency_p99_ms: float = 500.0,
        alert_error_rate_percent: float = 5.0,
        alert_memory_percent: float = 85.0,
        alert_cpu_percent: float = 80.0,
        histogram_window_seconds: int = 300
    ):
        # Thresholds
        self.alert_latency_p99_ms = alert_latency_p99_ms
        self.alert_error_rate_percent = alert_error_rate_percent
        self.alert_memory_percent = alert_memory_percent
        self.alert_cpu_percent = alert_cpu_percent
        
        # Histograms
        self._request_times: Dict[str, Histogram] = defaultdict(
            lambda: Histogram(window_seconds=histogram_window_seconds)
        )
        self._global_request_times = Histogram(window_seconds=histogram_window_seconds)
        
        # Counters
        self._request_counts: Dict[str, int] = defaultdict(int)
        self._error_counts: Dict[str, int] = defaultdict(int)
        self._status_counts: Dict[int, int] = defaultdict(int)
        
        # Rates
        self._request_rate = RateCalculator()
        self._error_rate = RateCalculator()
        
        # Alerts
        self._alerts: List[Alert] = []
        self._active_alerts: Dict[str, Alert] = {}
        
        # State
        self._start_time = datetime.utcnow()
        self._lock = asyncio.Lock()
    
    # ─────────────────────────────────────────────────────────────────────────
    # REQUEST TRACKING
    # ─────────────────────────────────────────────────────────────────────────
    
    async def record_request(
        self,
        endpoint: str,
        method: str,
        duration_ms: float,
        status_code: int,
        request_id: Optional[str] = None
    ) -> None:
        """Record request metrics"""
        async with self._lock:
            # Key for endpoint metrics
            key = f"{method}:{endpoint}"
            
            # Record timing
            self._request_times[key].observe(duration_ms)
            self._global_request_times.observe(duration_ms)
            
            # Update counters
            self._request_counts[key] += 1
            self._status_counts[status_code] += 1
            
            # Record rates
            self._request_rate.record()
            
            # Track errors
            if status_code >= 400:
                self._error_counts[key] += 1
                self._error_rate.record()
            
            # Check alerts
            await self._check_alerts(key, duration_ms, status_code)
    
    @asynccontextmanager
    async def track_request(
        self,
        endpoint: str,
        method: str = "GET"
    ):
        """
        Context manager to track request timing.
        
        Usage:
            async with monitor.track_request("/api/threads", "GET") as tracker:
                result = await process_request()
                tracker.set_status(200)
        """
        start = time.time()
        status_code = 200
        
        class Tracker:
            def set_status(self, code: int):
                nonlocal status_code
                status_code = code
        
        tracker = Tracker()
        
        try:
            yield tracker
        except Exception:
            status_code = 500
            raise
        finally:
            duration_ms = (time.time() - start) * 1000
            await self.record_request(endpoint, method, duration_ms, status_code)
    
    # ─────────────────────────────────────────────────────────────────────────
    # ALERTS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def _check_alerts(
        self,
        endpoint: str,
        duration_ms: float,
        status_code: int
    ) -> None:
        """Check for alert conditions"""
        now = datetime.utcnow()
        
        # Latency alert
        p99 = self._global_request_times.percentile(99)
        if p99 > self.alert_latency_p99_ms:
            alert_key = "latency_p99"
            if alert_key not in self._active_alerts:
                alert = Alert(
                    id=str(uuid4()),
                    severity=AlertSeverity.WARNING,
                    metric_name="request_latency_p99_ms",
                    message=f"P99 latency {p99:.2f}ms exceeds threshold {self.alert_latency_p99_ms}ms",
                    value=p99,
                    threshold=self.alert_latency_p99_ms,
                    triggered_at=now
                )
                self._active_alerts[alert_key] = alert
                self._alerts.append(alert)
                logger.warning(f"Alert: {alert.message}")
        else:
            # Resolve if below threshold
            if "latency_p99" in self._active_alerts:
                self._active_alerts["latency_p99"].resolved_at = now
                del self._active_alerts["latency_p99"]
        
        # Error rate alert
        total = self._request_rate.count
        errors = self._error_rate.count
        error_rate = (errors / total * 100) if total > 0 else 0
        
        if error_rate > self.alert_error_rate_percent:
            alert_key = "error_rate"
            if alert_key not in self._active_alerts:
                alert = Alert(
                    id=str(uuid4()),
                    severity=AlertSeverity.CRITICAL,
                    metric_name="error_rate_percent",
                    message=f"Error rate {error_rate:.2f}% exceeds threshold {self.alert_error_rate_percent}%",
                    value=error_rate,
                    threshold=self.alert_error_rate_percent,
                    triggered_at=now
                )
                self._active_alerts[alert_key] = alert
                self._alerts.append(alert)
                logger.error(f"Alert: {alert.message}")
        else:
            if "error_rate" in self._active_alerts:
                self._active_alerts["error_rate"].resolved_at = now
                del self._active_alerts["error_rate"]
    
    async def check_resource_alerts(self) -> None:
        """Check resource utilization alerts"""
        now = datetime.utcnow()
        resources = self.get_resource_usage()
        
        # Memory alert
        if resources["memory_percent"] > self.alert_memory_percent:
            alert_key = "memory"
            if alert_key not in self._active_alerts:
                alert = Alert(
                    id=str(uuid4()),
                    severity=AlertSeverity.CRITICAL,
                    metric_name="memory_percent",
                    message=f"Memory usage {resources['memory_percent']:.1f}% exceeds threshold {self.alert_memory_percent}%",
                    value=resources["memory_percent"],
                    threshold=self.alert_memory_percent,
                    triggered_at=now
                )
                self._active_alerts[alert_key] = alert
                self._alerts.append(alert)
                logger.error(f"Alert: {alert.message}")
        else:
            if "memory" in self._active_alerts:
                self._active_alerts["memory"].resolved_at = now
                del self._active_alerts["memory"]
        
        # CPU alert
        if resources["cpu_percent"] > self.alert_cpu_percent:
            alert_key = "cpu"
            if alert_key not in self._active_alerts:
                alert = Alert(
                    id=str(uuid4()),
                    severity=AlertSeverity.WARNING,
                    metric_name="cpu_percent",
                    message=f"CPU usage {resources['cpu_percent']:.1f}% exceeds threshold {self.alert_cpu_percent}%",
                    value=resources["cpu_percent"],
                    threshold=self.alert_cpu_percent,
                    triggered_at=now
                )
                self._active_alerts[alert_key] = alert
                self._alerts.append(alert)
                logger.warning(f"Alert: {alert.message}")
        else:
            if "cpu" in self._active_alerts:
                self._active_alerts["cpu"].resolved_at = now
                del self._active_alerts["cpu"]
    
    def get_active_alerts(self) -> List[Alert]:
        """Get currently active alerts"""
        return list(self._active_alerts.values())
    
    def get_alerts(
        self,
        since: Optional[datetime] = None,
        severity: Optional[AlertSeverity] = None
    ) -> List[Alert]:
        """Get alerts with optional filters"""
        alerts = self._alerts
        
        if since:
            alerts = [a for a in alerts if a.triggered_at >= since]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        return alerts
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self._alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # METRICS
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_request_metrics(self, endpoint: Optional[str] = None) -> Dict[str, Any]:
        """Get request timing metrics"""
        if endpoint:
            histogram = self._request_times.get(endpoint)
            if histogram:
                return histogram.summary()
            return {}
        
        return self._global_request_times.summary()
    
    def get_endpoint_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics per endpoint"""
        result = {}
        
        for endpoint, histogram in self._request_times.items():
            result[endpoint] = {
                "timing": histogram.summary(),
                "requests": self._request_counts.get(endpoint, 0),
                "errors": self._error_counts.get(endpoint, 0),
                "error_rate": (
                    self._error_counts.get(endpoint, 0) / 
                    max(self._request_counts.get(endpoint, 1), 1) * 100
                )
            }
        
        return result
    
    def get_status_distribution(self) -> Dict[int, int]:
        """Get response status code distribution"""
        return dict(self._status_counts)
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage"""
        process = psutil.Process()
        
        return {
            "memory_percent": process.memory_percent(),
            "memory_rss_mb": process.memory_info().rss / (1024 * 1024),
            "memory_vms_mb": process.memory_info().vms / (1024 * 1024),
            "cpu_percent": process.cpu_percent(),
            "threads": process.num_threads(),
            "open_files": len(process.open_files()),
            "connections": len(process.connections()),
        }
    
    def get_gc_stats(self) -> Dict[str, Any]:
        """Get garbage collection statistics"""
        return {
            "collections": gc.get_count(),
            "thresholds": gc.get_threshold(),
            "objects_tracked": len(gc.get_objects()),
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # HEALTH SCORE
    # ─────────────────────────────────────────────────────────────────────────
    
    def calculate_health_score(
        self,
        cache_hit_rate: float = 100.0,
        database_healthy: bool = True
    ) -> HealthScore:
        """Calculate overall system health score"""
        resources = self.get_resource_usage()
        request_metrics = self.get_request_metrics()
        
        # API Latency score (100 = fast, 0 = slow)
        p99 = request_metrics.get("p99", 0)
        if p99 <= 100:
            latency_score = 100
        elif p99 <= 500:
            latency_score = 100 - ((p99 - 100) / 400 * 50)
        else:
            latency_score = max(0, 50 - ((p99 - 500) / 500 * 50))
        
        # Error rate score (100 = no errors)
        total = self._request_rate.count
        errors = self._error_rate.count
        error_rate = (errors / total * 100) if total > 0 else 0
        error_score = max(0, 100 - error_rate * 10)  # -10 per 1% error rate
        
        # Memory score (100 = low usage)
        memory_score = max(0, 100 - resources["memory_percent"])
        
        # CPU score (100 = low usage)
        cpu_score = max(0, 100 - resources["cpu_percent"])
        
        # Cache score
        cache_score = cache_hit_rate
        
        # Database score
        db_score = 100 if database_healthy else 0
        
        # Weighted overall score
        overall = (
            latency_score * 0.25 +
            error_score * 0.25 +
            memory_score * 0.15 +
            cpu_score * 0.10 +
            cache_score * 0.15 +
            db_score * 0.10
        )
        
        return HealthScore(
            overall=round(overall, 1),
            api_latency=round(latency_score, 1),
            error_rate=round(error_score, 1),
            memory_usage=round(memory_score, 1),
            cpu_usage=round(cpu_score, 1),
            cache_hit_rate=round(cache_score, 1),
            database_health=round(db_score, 1)
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        uptime = (datetime.utcnow() - self._start_time).total_seconds()
        
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": sum(self._request_counts.values()),
            "total_errors": sum(self._error_counts.values()),
            "requests_per_second": round(self._request_rate.rate, 2),
            "errors_per_second": round(self._error_rate.rate, 2),
            "timing": self.get_request_metrics(),
            "status_distribution": self.get_status_distribution(),
            "resources": self.get_resource_usage(),
            "active_alerts": len(self._active_alerts),
            "health": self.calculate_health_score().__dict__
        }
    
    def reset(self) -> None:
        """Reset all metrics"""
        self._request_times.clear()
        self._global_request_times = Histogram()
        self._request_counts.clear()
        self._error_counts.clear()
        self._status_counts.clear()
        self._request_rate = RateCalculator()
        self._error_rate = RateCalculator()
        self._alerts.clear()
        self._active_alerts.clear()
        self._start_time = datetime.utcnow()

# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST TIMING DECORATOR
# ═══════════════════════════════════════════════════════════════════════════════

def track_performance(
    endpoint: Optional[str] = None,
    method: str = "GET"
):
    """
    Decorator to track function performance.
    
    Usage:
        @track_performance("/api/threads/create", "POST")
        async def create_thread(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            ep = endpoint or func.__name__
            
            start = time.time()
            status = 200
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception:
                status = 500
                raise
            finally:
                duration_ms = (time.time() - start) * 1000
                await monitor.record_request(ep, method, duration_ms, status)
        
        return wrapper
    return decorator

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

_global_monitor: Optional[PerformanceMonitor] = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor

def configure_monitor(**kwargs) -> PerformanceMonitor:
    """Configure global performance monitor"""
    global _global_monitor
    _global_monitor = PerformanceMonitor(**kwargs)
    return _global_monitor

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "PerformanceMonitor",
    "Histogram",
    "RateCalculator",
    "MetricType",
    "MetricPoint",
    "Alert",
    "AlertSeverity",
    "HealthScore",
    "track_performance",
    "get_performance_monitor",
    "configure_monitor",
]
