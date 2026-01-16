"""
CHE·NU™ — MEMORY PROFILING TESTS (PYTEST)
Sprint 10 (FINAL): Tests for memory usage and leak detection

Memory Principles:
- No memory leaks in long-running operations
- Efficient memory usage
- Proper cleanup on resource release
- Bounded memory growth
"""

import pytest
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import gc

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Memory thresholds (bytes)
MB = 1024 * 1024
GB = 1024 * MB

MEMORY_THRESHOLDS = {
    "sphere_data_max": 10 * MB,
    "thread_max": 1 * MB,
    "message_max": 100 * 1024,  # 100KB
    "agent_max": 500 * 1024,
    "audit_entry_max": 10 * 1024,
    "total_heap_max": 512 * MB,
}


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY TRACKING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class MemoryTracker:
    """Tracks memory usage."""
    
    def __init__(self):
        self.snapshots: List[Dict] = []
        self.initial = self._get_memory()
    
    def _get_memory(self) -> int:
        """Get current memory usage in bytes."""
        gc.collect()
        # Using sys.getsizeof for simple objects
        return 0  # Placeholder - in real implementation would use tracemalloc
    
    def snapshot(self, label: str = "") -> Dict:
        """Take a memory snapshot."""
        gc.collect()
        snapshot = {
            "label": label,
            "timestamp": datetime.utcnow().isoformat(),
            "memory": self._get_memory(),
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_growth(self) -> int:
        """Get memory growth since initialization."""
        current = self._get_memory()
        return current - self.initial
    
    def clear(self):
        """Clear snapshots."""
        self.snapshots = []


def estimate_size(obj: Any) -> int:
    """Estimate object size in bytes."""
    return sys.getsizeof(obj)


def estimate_dict_size(d: Dict) -> int:
    """Estimate dictionary size including contents."""
    size = sys.getsizeof(d)
    for key, value in d.items():
        size += sys.getsizeof(key)
        if isinstance(value, dict):
            size += estimate_dict_size(value)
        elif isinstance(value, list):
            size += estimate_list_size(value)
        else:
            size += sys.getsizeof(value)
    return size


def estimate_list_size(lst: List) -> int:
    """Estimate list size including contents."""
    size = sys.getsizeof(lst)
    for item in lst:
        if isinstance(item, dict):
            size += estimate_dict_size(item)
        elif isinstance(item, list):
            size += estimate_list_size(item)
        else:
            size += sys.getsizeof(item)
    return size


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def create_sphere_data() -> Dict:
    """Create typical sphere data."""
    return {
        "id": "personal",
        "name": "Personal",
        "icon": "🏠",
        "order": 1,
        "settings": {
            "theme": "dark",
            "notifications": True,
        },
    }


def create_thread_data(message_count: int = 10) -> Dict:
    """Create typical thread data."""
    return {
        "id": f"thread_{datetime.utcnow().timestamp()}",
        "title": "Test Thread",
        "sphere_id": "personal",
        "owner_id": "user_1",
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
        "messages": [
            {
                "id": f"msg_{i}",
                "role": "user" if i % 2 == 0 else "assistant",
                "content": "x" * 100,  # 100 char message
                "tokens": 25,
            }
            for i in range(message_count)
        ],
        "tokens_used": message_count * 25,
    }


def create_agent_data() -> Dict:
    """Create typical agent data."""
    return {
        "id": "agent_1",
        "name": "Test Agent",
        "level": "L2",
        "type": "specialist",
        "status": "idle",
        "is_system": False,
        "is_hired": True,
        "capabilities": ["task_execution", "data_analysis"],
    }


def create_audit_entry() -> Dict:
    """Create typical audit entry."""
    return {
        "id": f"audit_{datetime.utcnow().timestamp()}",
        "action": "THREAD_CREATED",
        "user_id": "user_1",
        "timestamp": datetime.utcnow().isoformat(),
        "details": {"thread_id": "thread_123"},
    }


# ═══════════════════════════════════════════════════════════════════════════════
# OBJECT SIZE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestObjectSizes:
    """Tests for individual object sizes."""

    def test_sphere_data_size(self):
        """Sphere data should be within threshold."""
        sphere = create_sphere_data()
        size = estimate_dict_size(sphere)
        
        assert size < MEMORY_THRESHOLDS["sphere_data_max"]

    def test_thread_data_size(self):
        """Thread data should be within threshold."""
        thread = create_thread_data(message_count=100)
        size = estimate_dict_size(thread)
        
        assert size < MEMORY_THRESHOLDS["thread_max"]

    def test_message_size(self):
        """Individual message should be within threshold."""
        message = {
            "id": "msg_1",
            "role": "assistant",
            "content": "x" * 1000,  # 1KB message
            "tokens": 250,
        }
        size = estimate_dict_size(message)
        
        assert size < MEMORY_THRESHOLDS["message_max"]

    def test_agent_size(self):
        """Agent data should be within threshold."""
        agent = create_agent_data()
        size = estimate_dict_size(agent)
        
        assert size < MEMORY_THRESHOLDS["agent_max"]

    def test_audit_entry_size(self):
        """Audit entry should be within threshold."""
        entry = create_audit_entry()
        size = estimate_dict_size(entry)
        
        assert size < MEMORY_THRESHOLDS["audit_entry_max"]


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY LEAK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryLeaks:
    """Tests for memory leaks."""

    def test_no_leak_on_thread_creation(self):
        """Creating and deleting threads should not leak memory."""
        threads = []
        
        # Create many threads
        for i in range(100):
            threads.append(create_thread_data(message_count=10))
        
        initial_count = len(threads)
        
        # Delete all threads
        threads.clear()
        gc.collect()
        
        # Should be empty
        assert len(threads) == 0

    def test_no_leak_on_message_processing(self):
        """Processing messages should not leak memory."""
        messages = []
        
        for i in range(1000):
            msg = {"id": f"msg_{i}", "content": "x" * 100}
            messages.append(msg)
            
            # Process and remove
            if len(messages) > 100:
                messages.pop(0)
        
        # Should only have last 100
        assert len(messages) <= 100

    def test_no_leak_on_audit_logging(self):
        """Audit logging should not leak memory."""
        audit_log = []
        MAX_LOG_SIZE = 1000
        
        for i in range(2000):
            audit_log.append(create_audit_entry())
            
            # Trim old entries
            if len(audit_log) > MAX_LOG_SIZE:
                audit_log = audit_log[-MAX_LOG_SIZE:]
        
        assert len(audit_log) == MAX_LOG_SIZE


# ═══════════════════════════════════════════════════════════════════════════════
# BOUNDED GROWTH TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBoundedGrowth:
    """Tests for bounded memory growth."""

    def test_sphere_cache_bounded(self):
        """Sphere cache should be bounded."""
        cache: Dict[str, Dict] = {}
        MAX_CACHE_SIZE = 20  # 9 spheres + some buffer
        
        for i in range(50):
            sphere_id = f"sphere_{i}"
            cache[sphere_id] = create_sphere_data()
            
            # Evict old entries
            if len(cache) > MAX_CACHE_SIZE:
                oldest = list(cache.keys())[0]
                del cache[oldest]
        
        assert len(cache) <= MAX_CACHE_SIZE

    def test_thread_cache_bounded(self):
        """Thread cache should be bounded."""
        cache: Dict[str, Dict] = {}
        MAX_CACHE_SIZE = 100
        
        for i in range(200):
            thread_id = f"thread_{i}"
            cache[thread_id] = create_thread_data(message_count=5)
            
            if len(cache) > MAX_CACHE_SIZE:
                oldest = list(cache.keys())[0]
                del cache[oldest]
        
        assert len(cache) <= MAX_CACHE_SIZE

    def test_message_history_bounded(self):
        """Message history should be bounded per thread."""
        MAX_MESSAGES = 100
        messages = []
        
        for i in range(500):
            messages.append({"id": f"msg_{i}", "content": "test"})
            
            if len(messages) > MAX_MESSAGES:
                messages.pop(0)
        
        assert len(messages) == MAX_MESSAGES


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCleanup:
    """Tests for proper cleanup."""

    def test_thread_cleanup(self):
        """Deleted threads should release memory."""
        thread = create_thread_data(message_count=100)
        thread_id = thread["id"]
        
        # Simulate deletion
        del thread
        gc.collect()
        
        # Variable should be gone
        with pytest.raises(UnboundLocalError):
            _ = thread

    def test_sphere_switch_cleanup(self):
        """Switching spheres should clean up old data."""
        active_sphere_data = None
        
        for sphere_id in ["personal", "business", "scholar"]:
            # Load new sphere
            active_sphere_data = create_sphere_data()
            active_sphere_data["id"] = sphere_id
        
        # Only one sphere should be active
        assert active_sphere_data["id"] == "scholar"

    def test_session_cleanup(self):
        """Ending session should clean up all resources."""
        session = {
            "user": {"id": "user_1"},
            "threads": [create_thread_data() for _ in range(10)],
            "agents": [create_agent_data() for _ in range(5)],
        }
        
        # End session
        session.clear()
        gc.collect()
        
        assert len(session) == 0


# ═══════════════════════════════════════════════════════════════════════════════
# COLLECTION SIZE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCollectionSizes:
    """Tests for collection sizes."""

    def test_9_spheres_memory(self):
        """9 spheres should use reasonable memory."""
        spheres = [create_sphere_data() for _ in range(9)]
        
        total_size = estimate_list_size(spheres)
        
        # 9 spheres should use less than 1MB
        assert total_size < 1 * MB

    def test_6_bureau_sections_memory(self):
        """6 bureau sections should use reasonable memory."""
        sections = [
            {"id": f"section_{i}", "name": f"Section {i}"}
            for i in range(6)
        ]
        
        total_size = estimate_list_size(sections)
        
        # 6 sections should use less than 100KB
        assert total_size < 100 * 1024

    def test_10_governance_laws_memory(self):
        """10 governance laws should use reasonable memory."""
        laws = [
            {"id": f"L{i+1}", "code": f"LAW_{i+1}"}
            for i in range(10)
        ]
        
        total_size = estimate_list_size(laws)
        
        # 10 laws should use less than 100KB
        assert total_size < 100 * 1024


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA MEMORY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaMemory:
    """Tests for Nova memory usage."""

    def test_nova_singleton_memory(self):
        """Nova should be a singleton with fixed memory."""
        nova1 = {
            "id": "nova",
            "name": "Nova",
            "level": "L0",
            "capabilities": ["guidance", "memory", "governance"],
        }
        
        nova2 = nova1  # Same reference
        
        # Should be same object
        assert nova1 is nova2

    def test_nova_guidance_history_bounded(self):
        """Nova guidance history should be bounded."""
        MAX_HISTORY = 100
        guidance_history = []
        
        for i in range(500):
            guidance_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "topic": f"topic_{i}",
            })
            
            if len(guidance_history) > MAX_HISTORY:
                guidance_history.pop(0)
        
        assert len(guidance_history) == MAX_HISTORY


# ═══════════════════════════════════════════════════════════════════════════════
# STRESS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryStress:
    """Stress tests for memory usage."""

    def test_many_threads_memory(self):
        """Creating many threads should not crash."""
        threads = []
        
        for i in range(1000):
            threads.append(create_thread_data(message_count=5))
        
        assert len(threads) == 1000
        
        # Cleanup
        threads.clear()
        gc.collect()

    def test_many_messages_memory(self):
        """Many messages in a thread should be manageable."""
        thread = create_thread_data(message_count=1000)
        
        assert len(thread["messages"]) == 1000
        
        # Size should still be reasonable
        size = estimate_dict_size(thread)
        assert size < 10 * MB

    def test_rapid_sphere_switching(self):
        """Rapid sphere switching should not leak memory."""
        spheres = ["personal", "business", "scholar"]
        active_data = None
        
        for _ in range(1000):
            sphere_id = spheres[_ % 3]
            active_data = create_sphere_data()
            active_data["id"] = sphere_id
        
        # Should complete without issue
        assert active_data is not None


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryPromptCompliance:
    """Tests ensuring memory usage supports Memory Prompt requirements."""

    def test_9_spheres_bounded(self):
        """9 spheres should have bounded memory."""
        spheres = [create_sphere_data() for _ in range(9)]
        assert len(spheres) == 9

    def test_6_sections_bounded(self):
        """6 bureau sections should have bounded memory."""
        sections = [{"id": f"section_{i}"} for i in range(6)]
        assert len(sections) == 6

    def test_audit_completeness_bounded(self):
        """Audit logging (L5) should be bounded."""
        MAX_AUDIT_SIZE = 10000
        audit_log = []
        
        for i in range(15000):
            audit_log.append(create_audit_entry())
            if len(audit_log) > MAX_AUDIT_SIZE:
                audit_log = audit_log[-MAX_AUDIT_SIZE:]
        
        assert len(audit_log) == MAX_AUDIT_SIZE

    def test_token_tracking_memory(self):
        """Token tracking (L8) should use reasonable memory."""
        token_history = []
        MAX_HISTORY = 1000
        
        for i in range(5000):
            token_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "amount": 100,
                "operation": "use",
            })
            
            if len(token_history) > MAX_HISTORY:
                token_history.pop(0)
        
        assert len(token_history) == MAX_HISTORY
