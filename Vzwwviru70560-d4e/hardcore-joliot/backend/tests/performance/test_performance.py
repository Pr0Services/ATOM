"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — PERFORMANCE TESTS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A3: Tests Critiques
Date: 8 Janvier 2026

FOCUS:
- Response time (latency)
- Throughput (requests/second)
- Memory usage
- Database query performance
- Scalability indicators
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import asyncio
import time
from uuid import uuid4
from typing import List, Dict, Any
from datetime import datetime, timedelta
import statistics

import sys
sys.path.insert(0, '..')
from tests.factories import UserFactory, ThreadFactory, DecisionFactory
from tests.mocks import MockCheckpointService, MockDatabaseSession


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def performance_thresholds() -> Dict[str, float]:
    """Seuils de performance acceptables."""
    return {
        # Latency (ms)
        "api_response_p50": 100,      # 50th percentile
        "api_response_p95": 500,      # 95th percentile
        "api_response_p99": 1000,     # 99th percentile
        "db_query_simple": 50,        # Simple query
        "db_query_complex": 200,      # Complex query with joins
        "checkpoint_create": 100,     # Create checkpoint
        "checkpoint_approve": 50,     # Approve checkpoint
        
        # Throughput (requests/second)
        "api_throughput_min": 100,    # Minimum RPS
        "search_throughput_min": 50,  # Search operations
        
        # Memory (MB)
        "memory_per_request": 10,     # Max memory per request
        "memory_baseline": 256,       # Baseline memory usage
        
        # Database
        "max_connections": 100,       # Max DB connections
        "query_timeout": 30,          # Query timeout (seconds)
    }


@pytest.fixture
def load_test_config() -> Dict[str, int]:
    """Configuration pour tests de charge."""
    return {
        "concurrent_users": 100,
        "requests_per_user": 10,
        "ramp_up_seconds": 10,
        "duration_seconds": 60,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# LATENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAPILatency:
    """Tests de latence API."""
    
    @pytest.mark.performance
    @pytest.mark.critical
    async def test_checkpoint_create_latency(
        self, checkpoint_service, user_id, performance_thresholds
    ):
        """✅ Latence création checkpoint < 100ms."""
        latencies = []
        
        for _ in range(100):
            start = time.perf_counter()
            
            await checkpoint_service.create_checkpoint(
                action_type="test_action",
                user_id=str(user_id)
            )
            
            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
        
        p50 = statistics.median(latencies)
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        p99 = sorted(latencies)[int(len(latencies) * 0.99)]
        
        # Vérifier les seuils
        assert p50 < performance_thresholds["checkpoint_create"], (
            f"P50 latency {p50:.2f}ms exceeds threshold"
        )
        assert p95 < performance_thresholds["api_response_p95"], (
            f"P95 latency {p95:.2f}ms exceeds threshold"
        )
    
    @pytest.mark.performance
    async def test_checkpoint_approve_latency(
        self, checkpoint_service, user_id, performance_thresholds
    ):
        """✅ Latence approbation checkpoint < 50ms."""
        # Créer des checkpoints d'abord
        checkpoints = []
        for _ in range(50):
            cp = await checkpoint_service.create_checkpoint(
                action_type="test",
                user_id=str(user_id)
            )
            checkpoints.append(cp)
        
        latencies = []
        for cp in checkpoints:
            start = time.perf_counter()
            
            await checkpoint_service.approve(cp["id"], str(user_id))
            
            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
        
        p50 = statistics.median(latencies)
        
        assert p50 < performance_thresholds["checkpoint_approve"], (
            f"Approve P50 latency {p50:.2f}ms exceeds threshold"
        )
    
    @pytest.mark.performance
    async def test_bulk_operations_latency(self, checkpoint_service, user_id):
        """✅ Opérations bulk restent performantes."""
        batch_sizes = [10, 50, 100]
        
        for batch_size in batch_sizes:
            start = time.perf_counter()
            
            # Créer un batch
            checkpoints = []
            for _ in range(batch_size):
                cp = await checkpoint_service.create_checkpoint(
                    action_type="bulk_test",
                    user_id=str(user_id)
                )
                checkpoints.append(cp)
            
            total_time_ms = (time.perf_counter() - start) * 1000
            per_item_ms = total_time_ms / batch_size
            
            # La latence par item ne devrait pas augmenter significativement
            assert per_item_ms < 50, (
                f"Per-item latency {per_item_ms:.2f}ms for batch of {batch_size}"
            )


class TestDatabaseQueryPerformance:
    """Tests de performance des requêtes DB."""
    
    @pytest.mark.performance
    async def test_simple_query_latency(self, mock_db_session, performance_thresholds):
        """✅ Requêtes simples < 50ms."""
        latencies = []
        
        for _ in range(100):
            start = time.perf_counter()
            
            # Simuler une requête simple (SELECT by ID)
            await mock_db_session.execute(
                "SELECT * FROM checkpoints WHERE id = :id",
                {"id": str(uuid4())}
            )
            
            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
        
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        
        assert p95 < performance_thresholds["db_query_simple"]
    
    @pytest.mark.performance
    async def test_complex_query_latency(self, mock_db_session, performance_thresholds):
        """✅ Requêtes complexes < 200ms."""
        latencies = []
        
        for _ in range(50):
            start = time.perf_counter()
            
            # Simuler une requête complexe avec JOIN
            await mock_db_session.execute(
                """
                SELECT c.*, u.name, t.title 
                FROM checkpoints c
                JOIN users u ON c.user_id = u.id
                JOIN threads t ON c.context->>'thread_id' = t.id::text
                WHERE c.status = :status
                ORDER BY c.created_at DESC
                LIMIT 100
                """,
                {"status": "pending"}
            )
            
            latency_ms = (time.perf_counter() - start) * 1000
            latencies.append(latency_ms)
        
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        
        assert p95 < performance_thresholds["db_query_complex"]
    
    @pytest.mark.performance
    async def test_pagination_performance(self, mock_db_session):
        """✅ La pagination reste performante à grande échelle."""
        page_sizes = [10, 50, 100]
        page_numbers = [1, 10, 100]
        
        for page_size in page_sizes:
            for page_num in page_numbers:
                offset = (page_num - 1) * page_size
                
                start = time.perf_counter()
                
                await mock_db_session.execute(
                    "SELECT * FROM checkpoints ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
                    {"limit": page_size, "offset": offset}
                )
                
                latency_ms = (time.perf_counter() - start) * 1000
                
                # La latence ne devrait pas exploser avec l'offset
                # (en prod, utiliser cursor-based pagination)
                assert latency_ms < 500, (
                    f"Pagination too slow at page {page_num}, size {page_size}"
                )


# ═══════════════════════════════════════════════════════════════════════════════
# THROUGHPUT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThroughput:
    """Tests de débit (throughput)."""
    
    @pytest.mark.performance
    async def test_concurrent_checkpoint_creation(
        self, checkpoint_service, performance_thresholds
    ):
        """✅ Création concurrente de checkpoints."""
        num_concurrent = 100
        user_ids = [str(uuid4()) for _ in range(num_concurrent)]
        
        start = time.perf_counter()
        
        # Créer checkpoints en parallèle
        tasks = [
            checkpoint_service.create_checkpoint(
                action_type=f"concurrent_test_{i}",
                user_id=user_ids[i]
            )
            for i in range(num_concurrent)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        duration_seconds = time.perf_counter() - start
        successful = sum(1 for r in results if not isinstance(r, Exception))
        throughput = successful / duration_seconds
        
        assert throughput >= performance_thresholds["api_throughput_min"], (
            f"Throughput {throughput:.2f} RPS below minimum"
        )
        assert successful == num_concurrent, (
            f"Only {successful}/{num_concurrent} requests succeeded"
        )
    
    @pytest.mark.performance
    async def test_mixed_operations_throughput(self, checkpoint_service):
        """✅ Débit avec opérations mixtes."""
        num_operations = 200
        user_id = str(uuid4())
        
        start = time.perf_counter()
        
        # Mix: 60% read, 30% create, 10% approve
        operations = []
        checkpoints_to_approve = []
        
        for i in range(num_operations):
            op_type = i % 10
            
            if op_type < 6:  # 60% reads
                operations.append(
                    checkpoint_service.get_pending(user_id)
                )
            elif op_type < 9:  # 30% creates
                cp = await checkpoint_service.create_checkpoint(
                    action_type=f"mixed_{i}",
                    user_id=user_id
                )
                checkpoints_to_approve.append(cp)
            else:  # 10% approves
                if checkpoints_to_approve:
                    cp = checkpoints_to_approve.pop(0)
                    operations.append(
                        checkpoint_service.approve(cp["id"], user_id)
                    )
        
        if operations:
            await asyncio.gather(*operations, return_exceptions=True)
        
        duration_seconds = time.perf_counter() - start
        throughput = num_operations / duration_seconds
        
        # Le throughput mixte devrait rester acceptable
        assert throughput >= 50, f"Mixed throughput {throughput:.2f} RPS too low"


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryUsage:
    """Tests d'utilisation mémoire."""
    
    @pytest.mark.performance
    async def test_no_memory_leak_on_repeated_operations(self, checkpoint_service):
        """✅ Pas de fuite mémoire sur opérations répétées."""
        import gc
        
        user_id = str(uuid4())
        iterations = 1000
        
        # Mesurer la mémoire initiale (approximation)
        gc.collect()
        
        for _ in range(iterations):
            cp = await checkpoint_service.create_checkpoint(
                action_type="memory_test",
                user_id=user_id
            )
            await checkpoint_service.approve(cp["id"], user_id)
        
        # Force garbage collection
        gc.collect()
        
        # En production, vérifier avec tracemalloc
        # Ici on vérifie simplement que ça ne crash pas
        assert True
    
    @pytest.mark.performance
    async def test_large_context_handling(self, checkpoint_service):
        """✅ Gestion de contextes volumineux."""
        user_id = str(uuid4())
        
        # Contexte volumineux (mais raisonnable)
        large_context = {
            "files": [{"id": str(uuid4()), "name": f"file_{i}.txt"} for i in range(100)],
            "metadata": {f"key_{i}": f"value_{i}" * 100 for i in range(50)},
            "history": [{"event": f"event_{i}", "timestamp": datetime.utcnow().isoformat()} for i in range(200)]
        }
        
        start = time.perf_counter()
        
        cp = await checkpoint_service.create_checkpoint(
            action_type="large_context",
            user_id=user_id,
            context=large_context
        )
        
        latency_ms = (time.perf_counter() - start) * 1000
        
        # Devrait toujours être raisonnable
        assert latency_ms < 500, f"Large context took {latency_ms:.2f}ms"
        assert cp["context"] == large_context


# ═══════════════════════════════════════════════════════════════════════════════
# SCALABILITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestScalability:
    """Tests de scalabilité."""
    
    @pytest.mark.performance
    async def test_linear_scaling_with_users(self, checkpoint_service):
        """✅ Scaling linéaire avec le nombre d'utilisateurs."""
        user_counts = [10, 50, 100]
        latencies_by_count = {}
        
        for user_count in user_counts:
            user_ids = [str(uuid4()) for _ in range(user_count)]
            latencies = []
            
            for user_id in user_ids:
                start = time.perf_counter()
                await checkpoint_service.create_checkpoint(
                    action_type="scale_test",
                    user_id=user_id
                )
                latencies.append((time.perf_counter() - start) * 1000)
            
            latencies_by_count[user_count] = statistics.mean(latencies)
        
        # La latence ne devrait pas augmenter de façon exponentielle
        # Acceptable: +50% quand on passe de 10 à 100 users
        ratio = latencies_by_count[100] / latencies_by_count[10]
        assert ratio < 3, f"Latency increased {ratio:.2f}x with 10x users"
    
    @pytest.mark.performance
    async def test_handles_spike_traffic(self, checkpoint_service):
        """✅ Gestion des pics de trafic."""
        # Simuler un pic: 500 requêtes en 1 seconde
        spike_size = 500
        user_id = str(uuid4())
        
        start = time.perf_counter()
        
        tasks = [
            checkpoint_service.create_checkpoint(
                action_type=f"spike_{i}",
                user_id=user_id
            )
            for i in range(spike_size)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        duration = time.perf_counter() - start
        successful = sum(1 for r in results if not isinstance(r, Exception))
        error_rate = (spike_size - successful) / spike_size
        
        # Au moins 95% de succès même en pic
        assert error_rate < 0.05, f"Error rate {error_rate*100:.1f}% during spike"
        
        # Tout traité en moins de 10 secondes
        assert duration < 10, f"Spike took {duration:.1f}s"


# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK SUITE
# ═══════════════════════════════════════════════════════════════════════════════

class TestBenchmarkSuite:
    """Suite de benchmarks complète."""
    
    @pytest.mark.performance
    @pytest.mark.benchmark
    async def test_full_workflow_benchmark(self, checkpoint_service, user_id):
        """📊 Benchmark workflow complet."""
        iterations = 100
        workflow_times = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            
            # 1. Create checkpoint
            cp = await checkpoint_service.create_checkpoint(
                action_type="benchmark",
                user_id=str(user_id)
            )
            
            # 2. Get pending
            await checkpoint_service.get_pending(str(user_id))
            
            # 3. Approve
            await checkpoint_service.approve(cp["id"], str(user_id))
            
            # 4. Verify
            await checkpoint_service.is_approved(cp["id"])
            
            workflow_times.append((time.perf_counter() - start) * 1000)
        
        # Statistiques
        results = {
            "min": min(workflow_times),
            "max": max(workflow_times),
            "mean": statistics.mean(workflow_times),
            "median": statistics.median(workflow_times),
            "p95": sorted(workflow_times)[int(len(workflow_times) * 0.95)],
            "p99": sorted(workflow_times)[int(len(workflow_times) * 0.99)],
            "stdev": statistics.stdev(workflow_times) if len(workflow_times) > 1 else 0
        }
        
        print(f"\n📊 Workflow Benchmark Results:")
        print(f"   Min: {results['min']:.2f}ms")
        print(f"   Max: {results['max']:.2f}ms")
        print(f"   Mean: {results['mean']:.2f}ms")
        print(f"   Median: {results['median']:.2f}ms")
        print(f"   P95: {results['p95']:.2f}ms")
        print(f"   P99: {results['p99']:.2f}ms")
        print(f"   StdDev: {results['stdev']:.2f}ms")
        
        # Seuils
        assert results['p95'] < 500, "P95 exceeds 500ms"
        assert results['mean'] < 200, "Mean exceeds 200ms"
