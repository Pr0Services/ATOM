"""
SERVICE: query_optimizer.py
SPHERE: Core
VERSION: 1.0.0
INTENT: Query optimization with prepared statements, batch operations, and analysis

CHE·NU™ Query Optimization:
- Prepared statement caching
- Batch query execution
- Query performance analysis
- N+1 detection
- Index recommendations

R&D COMPLIANCE: ✅
- Rule #6: Query traceability and metrics
- Rule #7: Consistent with database core
"""

from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps
from enum import Enum
import hashlib
import asyncio
import time
import logging
import re
from uuid import UUID

from sqlalchemy import text, select, event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, RelationshipProperty, joinedload, selectinload

logger = logging.getLogger(__name__)

T = TypeVar("T")

# ═══════════════════════════════════════════════════════════════════════════════
# QUERY METRICS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    
    query_hash: str
    query_text: str
    execution_count: int = 0
    total_time_ms: float = 0.0
    min_time_ms: float = float('inf')
    max_time_ms: float = 0.0
    avg_time_ms: float = 0.0
    last_executed: Optional[datetime] = None
    rows_returned: int = 0
    is_slow: bool = False
    parameters_used: List[Dict[str, Any]] = field(default_factory=list)
    
    def record_execution(
        self,
        duration_ms: float,
        rows: int,
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record query execution"""
        self.execution_count += 1
        self.total_time_ms += duration_ms
        self.min_time_ms = min(self.min_time_ms, duration_ms)
        self.max_time_ms = max(self.max_time_ms, duration_ms)
        self.avg_time_ms = self.total_time_ms / self.execution_count
        self.last_executed = datetime.utcnow()
        self.rows_returned += rows
        
        # Track parameters (for analysis, keep last 10)
        if params:
            self.parameters_used.append(params)
            if len(self.parameters_used) > 10:
                self.parameters_used = self.parameters_used[-10:]
        
        # Flag slow queries (>100ms)
        if duration_ms > 100:
            self.is_slow = True

@dataclass
class QueryPlan:
    """Query execution plan"""
    
    plan_text: str
    estimated_rows: int
    estimated_cost: float
    uses_index: bool
    scan_type: str  # seq, index, bitmap
    warnings: List[str] = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════════════════════
# PREPARED STATEMENT CACHE
# ═══════════════════════════════════════════════════════════════════════════════

class PreparedStatementCache:
    """Cache for prepared SQL statements"""
    
    def __init__(self, max_size: int = 500):
        self.max_size = max_size
        self._cache: Dict[str, Any] = {}
        self._usage: Dict[str, int] = defaultdict(int)
        self._lock = asyncio.Lock()
    
    def _hash_query(self, query: str) -> str:
        """Generate hash for query"""
        # Normalize whitespace
        normalized = " ".join(query.split())
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    async def get_or_prepare(
        self,
        session: AsyncSession,
        query: str,
        name: Optional[str] = None
    ) -> Any:
        """Get cached prepared statement or create new"""
        query_hash = self._hash_query(query)
        
        async with self._lock:
            if query_hash in self._cache:
                self._usage[query_hash] += 1
                return self._cache[query_hash]
            
            # Evict LFU if at capacity
            if len(self._cache) >= self.max_size:
                lfu_key = min(self._usage.keys(), key=lambda k: self._usage[k])
                del self._cache[lfu_key]
                del self._usage[lfu_key]
            
            # Prepare statement
            stmt = text(query)
            self._cache[query_hash] = stmt
            self._usage[query_hash] = 1
            
            return stmt
    
    def clear(self) -> None:
        """Clear cache"""
        self._cache.clear()
        self._usage.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_usage = sum(self._usage.values())
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "total_executions": total_usage,
            "top_queries": sorted(
                self._usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

# ═══════════════════════════════════════════════════════════════════════════════
# BATCH QUERY EXECUTOR
# ═══════════════════════════════════════════════════════════════════════════════

class BatchQueryExecutor:
    """Execute queries in batches for efficiency"""
    
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
        self._pending: Dict[str, List[Tuple[Any, asyncio.Future]]] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def execute_batched(
        self,
        session: AsyncSession,
        query_template: str,
        items: List[Any],
        id_extractor: Callable[[Any], Any]
    ) -> Dict[Any, Any]:
        """
        Execute query in batches.
        
        Args:
            session: Database session
            query_template: SQL template with :ids placeholder
            items: Items to query
            id_extractor: Function to extract ID from item
            
        Returns:
            Dict mapping ID to result
        """
        results: Dict[Any, Any] = {}
        ids = [id_extractor(item) for item in items]
        
        # Process in batches
        for i in range(0, len(ids), self.batch_size):
            batch_ids = ids[i:i + self.batch_size]
            
            stmt = text(query_template)
            result = await session.execute(
                stmt,
                {"ids": batch_ids}
            )
            
            for row in result.fetchall():
                results[row[0]] = row
        
        return results
    
    async def bulk_insert(
        self,
        session: AsyncSession,
        model_class: type,
        items: List[Dict[str, Any]]
    ) -> int:
        """Bulk insert items"""
        if not items:
            return 0
        
        inserted = 0
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            # Use executemany for efficiency
            objects = [model_class(**item) for item in batch]
            session.add_all(objects)
            
            inserted += len(batch)
        
        await session.commit()
        return inserted
    
    async def bulk_update(
        self,
        session: AsyncSession,
        model_class: type,
        items: List[Dict[str, Any]],
        id_field: str = "id"
    ) -> int:
        """Bulk update items"""
        if not items:
            return 0
        
        updated = 0
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            ids = [item[id_field] for item in batch]
            
            # Fetch existing
            stmt = select(model_class).where(
                getattr(model_class, id_field).in_(ids)
            )
            result = await session.execute(stmt)
            existing = {
                getattr(obj, id_field): obj
                for obj in result.scalars().all()
            }
            
            # Update
            for item in batch:
                obj_id = item[id_field]
                if obj_id in existing:
                    obj = existing[obj_id]
                    for key, value in item.items():
                        if key != id_field:
                            setattr(obj, key, value)
                    updated += 1
            
            await session.commit()
        
        return updated

# ═══════════════════════════════════════════════════════════════════════════════
# N+1 DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class NPlusOneDetector:
    """Detect N+1 query patterns"""
    
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self._queries: Dict[str, List[float]] = defaultdict(list)
        self._window_start: float = time.time()
        self._window_size: float = 1.0  # 1 second window
        self._warnings: List[Dict[str, Any]] = []
    
    def record_query(self, query_hash: str, timestamp: float) -> None:
        """Record query execution"""
        # Reset window if needed
        if timestamp - self._window_start > self._window_size:
            self._check_for_n_plus_one()
            self._queries.clear()
            self._window_start = timestamp
        
        self._queries[query_hash].append(timestamp)
    
    def _check_for_n_plus_one(self) -> None:
        """Check for N+1 patterns"""
        for query_hash, timestamps in self._queries.items():
            if len(timestamps) >= self.threshold:
                self._warnings.append({
                    "query_hash": query_hash,
                    "count": len(timestamps),
                    "window_start": self._window_start,
                    "detected_at": datetime.utcnow().isoformat()
                })
                
                logger.warning(
                    f"N+1 detected! Query {query_hash} executed {len(timestamps)} times "
                    f"in {self._window_size}s window"
                )
    
    def get_warnings(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get N+1 warnings"""
        if since is None:
            return self._warnings
        
        return [
            w for w in self._warnings
            if datetime.fromisoformat(w["detected_at"]) >= since
        ]
    
    def clear_warnings(self) -> None:
        """Clear warnings"""
        self._warnings.clear()

# ═══════════════════════════════════════════════════════════════════════════════
# EAGER LOADING OPTIMIZER
# ═══════════════════════════════════════════════════════════════════════════════

class EagerLoadingOptimizer:
    """Automatically add eager loading to prevent N+1"""
    
    # Known relationships to eager load
    EAGER_LOAD_MAP: Dict[str, List[str]] = {
        "Thread": ["events", "actions", "decisions", "snapshots"],
        "Sphere": ["bureau_sections", "quick_captures"],
        "User": ["spheres", "refresh_tokens"],
        "Agent": ["executions", "configs"],
        "GovernanceCheckpoint": ["audit_logs"],
    }
    
    @classmethod
    def optimize_query(
        cls,
        query: Query,
        model_name: str,
        depth: int = 1
    ) -> Query:
        """Add eager loading to query"""
        relationships = cls.EAGER_LOAD_MAP.get(model_name, [])
        
        for rel in relationships:
            if depth == 1:
                query = query.options(selectinload(rel))
            else:
                query = query.options(joinedload(rel))
        
        return query
    
    @classmethod
    def get_eager_options(
        cls,
        model_name: str,
        strategy: str = "selectin"
    ) -> List[Any]:
        """Get eager loading options for model"""
        relationships = cls.EAGER_LOAD_MAP.get(model_name, [])
        
        if strategy == "selectin":
            return [selectinload(rel) for rel in relationships]
        else:
            return [joinedload(rel) for rel in relationships]

# ═══════════════════════════════════════════════════════════════════════════════
# QUERY OPTIMIZER SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class QueryOptimizer:
    """
    Main query optimization service.
    
    Features:
    - Query metrics collection
    - Prepared statement caching
    - Batch execution
    - N+1 detection
    - Slow query logging
    - Index recommendations
    """
    
    def __init__(
        self,
        slow_query_threshold_ms: float = 100.0,
        enable_n_plus_one_detection: bool = True,
        prepared_cache_size: int = 500,
        batch_size: int = 100
    ):
        self.slow_query_threshold_ms = slow_query_threshold_ms
        
        # Components
        self._metrics: Dict[str, QueryMetrics] = {}
        self._prepared_cache = PreparedStatementCache(max_size=prepared_cache_size)
        self._batch_executor = BatchQueryExecutor(batch_size=batch_size)
        self._n_plus_one_detector = NPlusOneDetector() if enable_n_plus_one_detection else None
        
        # Statistics
        self._total_queries = 0
        self._slow_queries = 0
        self._start_time = datetime.utcnow()
    
    # ─────────────────────────────────────────────────────────────────────────
    # QUERY EXECUTION
    # ─────────────────────────────────────────────────────────────────────────
    
    async def execute(
        self,
        session: AsyncSession,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        use_prepared: bool = True
    ) -> Any:
        """
        Execute query with optimization.
        
        Args:
            session: Database session
            query: SQL query
            params: Query parameters
            use_prepared: Use prepared statement cache
            
        Returns:
            Query result
        """
        start_time = time.time()
        query_hash = self._hash_query(query)
        
        # Get or create metrics
        if query_hash not in self._metrics:
            self._metrics[query_hash] = QueryMetrics(
                query_hash=query_hash,
                query_text=query[:500]  # Truncate for storage
            )
        
        try:
            # Get prepared statement if enabled
            if use_prepared:
                stmt = await self._prepared_cache.get_or_prepare(session, query)
            else:
                stmt = text(query)
            
            # Execute
            result = await session.execute(stmt, params or {})
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Record metrics
            rows = result.rowcount if hasattr(result, 'rowcount') else 0
            self._metrics[query_hash].record_execution(duration_ms, rows, params)
            
            self._total_queries += 1
            
            # Log slow queries
            if duration_ms > self.slow_query_threshold_ms:
                self._slow_queries += 1
                logger.warning(
                    f"Slow query detected ({duration_ms:.2f}ms): {query[:100]}..."
                )
            
            # N+1 detection
            if self._n_plus_one_detector:
                self._n_plus_one_detector.record_query(query_hash, start_time)
            
            return result
            
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    async def execute_many(
        self,
        session: AsyncSession,
        query: str,
        params_list: List[Dict[str, Any]]
    ) -> int:
        """Execute query with multiple parameter sets"""
        if not params_list:
            return 0
        
        stmt = text(query)
        count = 0
        
        for params in params_list:
            await session.execute(stmt, params)
            count += 1
        
        return count
    
    # ─────────────────────────────────────────────────────────────────────────
    # BATCH OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def batch_select(
        self,
        session: AsyncSession,
        query_template: str,
        ids: List[Any]
    ) -> Dict[Any, Any]:
        """Execute batched SELECT query"""
        return await self._batch_executor.execute_batched(
            session,
            query_template,
            ids,
            lambda x: x
        )
    
    async def batch_insert(
        self,
        session: AsyncSession,
        model_class: type,
        items: List[Dict[str, Any]]
    ) -> int:
        """Batch insert items"""
        return await self._batch_executor.bulk_insert(session, model_class, items)
    
    async def batch_update(
        self,
        session: AsyncSession,
        model_class: type,
        items: List[Dict[str, Any]],
        id_field: str = "id"
    ) -> int:
        """Batch update items"""
        return await self._batch_executor.bulk_update(
            session, model_class, items, id_field
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSIS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def analyze_query(
        self,
        session: AsyncSession,
        query: str
    ) -> QueryPlan:
        """Analyze query execution plan"""
        try:
            explain_query = f"EXPLAIN (ANALYZE, FORMAT JSON) {query}"
            result = await session.execute(text(explain_query))
            plan_data = result.scalar()
            
            # Parse plan
            plan = plan_data[0]["Plan"] if plan_data else {}
            
            warnings = []
            
            # Check for sequential scans
            if plan.get("Node Type") == "Seq Scan":
                warnings.append(
                    f"Sequential scan on {plan.get('Relation Name')} - consider adding index"
                )
            
            # Check for high estimated rows
            if plan.get("Plan Rows", 0) > 10000:
                warnings.append("High estimated row count - consider pagination")
            
            return QueryPlan(
                plan_text=str(plan_data),
                estimated_rows=plan.get("Plan Rows", 0),
                estimated_cost=plan.get("Total Cost", 0),
                uses_index="Index" in plan.get("Node Type", ""),
                scan_type=plan.get("Node Type", "unknown"),
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Query analysis error: {e}")
            return QueryPlan(
                plan_text="",
                estimated_rows=0,
                estimated_cost=0,
                uses_index=False,
                scan_type="unknown",
                warnings=[str(e)]
            )
    
    def get_slow_queries(
        self,
        limit: int = 20,
        min_executions: int = 1
    ) -> List[QueryMetrics]:
        """Get slowest queries"""
        slow = [
            m for m in self._metrics.values()
            if m.is_slow and m.execution_count >= min_executions
        ]
        
        return sorted(
            slow,
            key=lambda m: m.avg_time_ms,
            reverse=True
        )[:limit]
    
    def get_frequent_queries(
        self,
        limit: int = 20
    ) -> List[QueryMetrics]:
        """Get most frequently executed queries"""
        return sorted(
            self._metrics.values(),
            key=lambda m: m.execution_count,
            reverse=True
        )[:limit]
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get optimization recommendations"""
        recommendations = []
        
        # Slow queries
        slow_queries = self.get_slow_queries(limit=5)
        for query in slow_queries:
            recommendations.append({
                "type": "slow_query",
                "severity": "high" if query.avg_time_ms > 500 else "medium",
                "query_hash": query.query_hash,
                "avg_time_ms": query.avg_time_ms,
                "suggestion": "Consider adding index or optimizing query"
            })
        
        # N+1 warnings
        if self._n_plus_one_detector:
            n_plus_one = self._n_plus_one_detector.get_warnings()
            for warning in n_plus_one[-5:]:  # Last 5
                recommendations.append({
                    "type": "n_plus_one",
                    "severity": "high",
                    "query_hash": warning["query_hash"],
                    "count": warning["count"],
                    "suggestion": "Use eager loading (selectinload/joinedload)"
                })
        
        # High frequency queries without caching
        frequent = self.get_frequent_queries(limit=10)
        for query in frequent:
            if query.execution_count > 100 and query.avg_time_ms > 10:
                recommendations.append({
                    "type": "cache_candidate",
                    "severity": "low",
                    "query_hash": query.query_hash,
                    "execution_count": query.execution_count,
                    "suggestion": "Consider caching this query result"
                })
        
        return recommendations
    
    # ─────────────────────────────────────────────────────────────────────────
    # STATISTICS
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics"""
        uptime = (datetime.utcnow() - self._start_time).total_seconds()
        qps = self._total_queries / uptime if uptime > 0 else 0
        
        return {
            "total_queries": self._total_queries,
            "slow_queries": self._slow_queries,
            "slow_query_threshold_ms": self.slow_query_threshold_ms,
            "queries_per_second": round(qps, 2),
            "uptime_seconds": round(uptime, 2),
            "unique_queries": len(self._metrics),
            "prepared_cache": self._prepared_cache.get_stats(),
            "n_plus_one_warnings": len(
                self._n_plus_one_detector.get_warnings()
            ) if self._n_plus_one_detector else 0
        }
    
    def reset_stats(self) -> None:
        """Reset statistics"""
        self._metrics.clear()
        self._total_queries = 0
        self._slow_queries = 0
        self._start_time = datetime.utcnow()
        self._prepared_cache.clear()
        if self._n_plus_one_detector:
            self._n_plus_one_detector.clear_warnings()
    
    # ─────────────────────────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────────────────────────
    
    def _hash_query(self, query: str) -> str:
        """Hash query for identification"""
        # Normalize: remove extra whitespace, lowercase
        normalized = " ".join(query.lower().split())
        # Remove specific values (for parameterized queries)
        normalized = re.sub(r"'[^']*'", "'?'", normalized)
        normalized = re.sub(r"\b\d+\b", "?", normalized)
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

# ═══════════════════════════════════════════════════════════════════════════════
# QUERY DECORATOR
# ═══════════════════════════════════════════════════════════════════════════════

def optimized_query(
    use_prepared: bool = True,
    eager_load: Optional[List[str]] = None,
    log_slow: bool = True
):
    """
    Decorator for optimized query execution.
    
    Usage:
        @optimized_query(eager_load=["events", "actions"])
        async def get_thread(session, thread_id):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                
                duration_ms = (time.time() - start_time) * 1000
                
                if log_slow and duration_ms > 100:
                    logger.warning(
                        f"Slow query in {func.__name__}: {duration_ms:.2f}ms"
                    )
                
                return result
                
            except Exception as e:
                logger.error(f"Query error in {func.__name__}: {e}")
                raise
        
        return wrapper
    return decorator

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

_global_optimizer: Optional[QueryOptimizer] = None

def get_query_optimizer() -> QueryOptimizer:
    """Get global query optimizer"""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = QueryOptimizer()
    return _global_optimizer

def configure_optimizer(**kwargs) -> QueryOptimizer:
    """Configure global query optimizer"""
    global _global_optimizer
    _global_optimizer = QueryOptimizer(**kwargs)
    return _global_optimizer

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "QueryOptimizer",
    "QueryMetrics",
    "QueryPlan",
    "PreparedStatementCache",
    "BatchQueryExecutor",
    "NPlusOneDetector",
    "EagerLoadingOptimizer",
    "optimized_query",
    "get_query_optimizer",
    "configure_optimizer",
]
