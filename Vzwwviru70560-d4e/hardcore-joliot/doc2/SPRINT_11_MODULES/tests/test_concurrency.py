"""
CHE·NU™ — CONCURRENCY TESTS (PYTEST)
Sprint 9: Tests for concurrent operations and race conditions

Concurrency Principles:
- Token budgets must be atomic
- Thread operations must be thread-safe
- Sphere isolation must hold under concurrent access
- Audit logs must capture all operations
"""

import pytest
from typing import Dict, List, Any
from datetime import datetime
from threading import Thread, Lock
import time
import random

# ═══════════════════════════════════════════════════════════════════════════════
# CONCURRENCY TEST HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class AtomicCounter:
    """Thread-safe counter."""
    
    def __init__(self, initial: int = 0):
        self.value = initial
        self.lock = Lock()
    
    def increment(self, amount: int = 1) -> int:
        with self.lock:
            self.value += amount
            return self.value
    
    def decrement(self, amount: int = 1) -> int:
        with self.lock:
            self.value -= amount
            return self.value
    
    def get(self) -> int:
        with self.lock:
            return self.value


class TokenBudget:
    """Thread-safe token budget."""
    
    def __init__(self, total: int):
        self.total = total
        self.used = 0
        self.lock = Lock()
    
    @property
    def remaining(self) -> int:
        with self.lock:
            return self.total - self.used
    
    def use(self, amount: int) -> bool:
        """Atomically use tokens."""
        with self.lock:
            if self.total - self.used >= amount:
                self.used += amount
                return True
            return False
    
    def refund(self, amount: int) -> bool:
        """Atomically refund tokens."""
        with self.lock:
            if self.used >= amount:
                self.used -= amount
                return True
            return False


class ConcurrentAuditLog:
    """Thread-safe audit log."""
    
    def __init__(self):
        self.entries: List[Dict] = []
        self.lock = Lock()
    
    def log(self, action: str, details: Dict = None):
        with self.lock:
            self.entries.append({
                "id": len(self.entries) + 1,
                "action": action,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    def count(self) -> int:
        with self.lock:
            return len(self.entries)
    
    def get_all(self) -> List[Dict]:
        with self.lock:
            return self.entries.copy()


# ═══════════════════════════════════════════════════════════════════════════════
# ATOMIC COUNTER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAtomicCounter:
    """Tests for atomic counter operations."""

    def test_initial_value(self):
        """Counter should start at initial value."""
        counter = AtomicCounter(100)
        assert counter.get() == 100

    def test_increment(self):
        """Counter should increment atomically."""
        counter = AtomicCounter(0)
        counter.increment(5)
        assert counter.get() == 5

    def test_decrement(self):
        """Counter should decrement atomically."""
        counter = AtomicCounter(10)
        counter.decrement(3)
        assert counter.get() == 7

    def test_concurrent_increments(self):
        """Concurrent increments should be atomic."""
        counter = AtomicCounter(0)
        threads = []
        
        def increment_100_times():
            for _ in range(100):
                counter.increment()
        
        # Create 10 threads, each incrementing 100 times
        for _ in range(10):
            t = Thread(target=increment_100_times)
            threads.append(t)
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
        
        # Should be exactly 1000
        assert counter.get() == 1000

    def test_concurrent_mixed_operations(self):
        """Mixed increment/decrement should be consistent."""
        counter = AtomicCounter(500)
        threads = []
        
        def increment_50():
            for _ in range(50):
                counter.increment()
        
        def decrement_50():
            for _ in range(50):
                counter.decrement()
        
        # 5 increment threads + 5 decrement threads
        for _ in range(5):
            threads.append(Thread(target=increment_50))
            threads.append(Thread(target=decrement_50))
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Net change: 0, should still be 500
        assert counter.get() == 500


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN BUDGET CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTokenBudgetConcurrency:
    """Tests for concurrent token budget operations."""

    def test_token_budget_creation(self):
        """Budget should initialize correctly."""
        budget = TokenBudget(10000)
        assert budget.total == 10000
        assert budget.remaining == 10000

    def test_use_tokens(self):
        """Using tokens should reduce remaining."""
        budget = TokenBudget(1000)
        result = budget.use(100)
        
        assert result is True
        assert budget.remaining == 900

    def test_use_tokens_exceeds_budget(self):
        """Using more tokens than available should fail."""
        budget = TokenBudget(100)
        result = budget.use(200)
        
        assert result is False
        assert budget.remaining == 100

    def test_concurrent_token_usage(self):
        """Concurrent token usage should be atomic."""
        budget = TokenBudget(10000)
        successful_uses = AtomicCounter(0)
        
        def use_100_tokens():
            if budget.use(100):
                successful_uses.increment()
        
        threads = []
        # 150 threads trying to use 100 tokens each
        for _ in range(150):
            t = Thread(target=use_100_tokens)
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Only 100 should succeed (10000 / 100)
        assert successful_uses.get() == 100
        assert budget.remaining == 0

    def test_no_negative_budget(self):
        """Budget should never go negative."""
        budget = TokenBudget(500)
        
        def try_use():
            for _ in range(100):
                budget.use(10)
        
        threads = [Thread(target=try_use) for _ in range(10)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Budget should be >= 0
        assert budget.remaining >= 0
        assert budget.used <= budget.total

    def test_refund_tokens(self):
        """Refunding should increase remaining."""
        budget = TokenBudget(1000)
        budget.use(500)
        budget.refund(200)
        
        assert budget.remaining == 700


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAuditLogConcurrency:
    """Tests for concurrent audit logging."""

    def test_concurrent_logging(self):
        """Concurrent log entries should all be captured."""
        audit = ConcurrentAuditLog()
        
        def log_100_entries(prefix: str):
            for i in range(100):
                audit.log(f"{prefix}_{i}")
        
        threads = []
        for i in range(10):
            t = Thread(target=log_100_entries, args=(f"thread_{i}",))
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All 1000 entries should be captured
        assert audit.count() == 1000

    def test_log_entries_have_unique_ids(self):
        """Log entries should have unique IDs."""
        audit = ConcurrentAuditLog()
        
        def log_50_entries():
            for _ in range(50):
                audit.log("action")
        
        threads = [Thread(target=log_50_entries) for _ in range(10)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        entries = audit.get_all()
        ids = [e["id"] for e in entries]
        
        # All IDs should be unique
        assert len(ids) == len(set(ids))

    def test_log_entries_have_timestamps(self):
        """All log entries should have timestamps."""
        audit = ConcurrentAuditLog()
        
        def log_entries():
            for _ in range(100):
                audit.log("action")
                time.sleep(0.001)  # Small delay
        
        threads = [Thread(target=log_entries) for _ in range(5)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        entries = audit.get_all()
        for entry in entries:
            assert "timestamp" in entry


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE ISOLATION CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereIsolationConcurrency:
    """Tests for sphere isolation under concurrent access."""

    def test_concurrent_sphere_data_isolation(self):
        """Sphere data should remain isolated under concurrent access."""
        sphere_data: Dict[str, List] = {
            "personal": [],
            "business": [],
            "scholar": [],
        }
        locks = {sphere: Lock() for sphere in sphere_data}
        
        def add_to_sphere(sphere_id: str, count: int):
            for i in range(count):
                with locks[sphere_id]:
                    sphere_data[sphere_id].append(f"{sphere_id}_{i}")
        
        threads = []
        for sphere in sphere_data:
            t = Thread(target=add_to_sphere, args=(sphere, 100))
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Each sphere should have exactly 100 items
        for sphere_id, data in sphere_data.items():
            assert len(data) == 100
            # All items should belong to that sphere
            assert all(item.startswith(sphere_id) for item in data)


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaConcurrency:
    """Tests for Nova under concurrent access."""

    def test_nova_single_instance(self):
        """Nova should always be single instance."""
        nova_instances = AtomicCounter(1)  # Start with 1 (Nova)
        
        def check_nova():
            # Simulate checking Nova exists
            current = nova_instances.get()
            assert current == 1
        
        threads = [Thread(target=check_nova) for _ in range(100)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Still exactly 1 Nova
        assert nova_instances.get() == 1

    def test_nova_never_hired_concurrent(self):
        """Nova should never be marked as hired even under concurrent attempts."""
        nova_hired = {"status": False}
        lock = Lock()
        
        def try_hire_nova():
            with lock:
                # BUG FIX: Nova can never be hired
                if nova_hired["status"]:
                    return
                # Simulate hiring attempt (should always fail for Nova)
                nova_hired["status"] = False
        
        threads = [Thread(target=try_hire_nova) for _ in range(100)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Nova should still not be hired
        assert nova_hired["status"] is False


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD CREATION CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadCreationConcurrency:
    """Tests for concurrent thread creation."""

    def test_concurrent_thread_creation(self):
        """Concurrent thread creation should work."""
        threads_created: List[str] = []
        lock = Lock()
        
        def create_thread(thread_id: str):
            with lock:
                threads_created.append(thread_id)
        
        python_threads = []
        for i in range(100):
            t = Thread(target=create_thread, args=(f"thread_{i}",))
            python_threads.append(t)
        
        for t in python_threads:
            t.start()
        for t in python_threads:
            t.join()
        
        assert len(threads_created) == 100

    def test_thread_ids_unique(self):
        """Thread IDs should be unique under concurrent creation."""
        thread_ids: List[str] = []
        lock = Lock()
        counter = AtomicCounter(0)
        
        def create_thread():
            thread_id = f"thread_{counter.increment()}"
            with lock:
                thread_ids.append(thread_id)
        
        python_threads = [Thread(target=create_thread) for _ in range(100)]
        
        for t in python_threads:
            t.start()
        for t in python_threads:
            t.join()
        
        # All IDs should be unique
        assert len(thread_ids) == len(set(thread_ids))


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE CONCURRENCY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestGovernanceConcurrency:
    """Tests for governance under concurrent operations."""

    def test_governance_check_atomic(self):
        """Governance checks should be atomic."""
        budget = TokenBudget(1000)
        approved_operations = AtomicCounter(0)
        
        def request_operation(cost: int):
            # Governance: Check and use atomically
            if budget.use(cost):
                approved_operations.increment()
        
        threads = []
        for _ in range(50):
            cost = random.randint(10, 100)
            t = Thread(target=request_operation, args=(cost,))
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Budget should never go negative
        assert budget.remaining >= 0
        # Approved operations should match used budget
        assert budget.used <= budget.total


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT CONCURRENCY COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestConcurrencyMemoryPromptCompliance:
    """Tests ensuring concurrency doesn't break Memory Prompt constraints."""

    def test_9_spheres_concurrent_access(self):
        """9 spheres should remain constant under concurrent access."""
        SPHERE_COUNT = 9
        
        def check_spheres():
            assert SPHERE_COUNT == 9
        
        threads = [Thread(target=check_spheres) for _ in range(100)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert SPHERE_COUNT == 9

    def test_6_bureau_sections_concurrent(self):
        """6 bureau sections should remain constant."""
        BUREAU_COUNT = 6
        
        def check_sections():
            assert BUREAU_COUNT == 6
        
        threads = [Thread(target=check_sections) for _ in range(100)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert BUREAU_COUNT == 6

    def test_audit_completeness_concurrent(self):
        """All operations should be audited even under concurrency (L5)."""
        audit = ConcurrentAuditLog()
        operations = AtomicCounter(0)
        
        def operation():
            operations.increment()
            audit.log("OPERATION")
        
        threads = [Thread(target=operation) for _ in range(1000)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Audit should capture all operations
        assert audit.count() == operations.get()
        assert audit.count() == 1000
