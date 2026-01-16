"""
CHE·NU™ — THREAD SYSTEM TESTS (PYTEST)
Sprint 6: Tests for Thread (.chenu) first-class objects

Thread System (Memory Prompt):
- Threads (.chenu) are FIRST-CLASS OBJECTS
- A thread represents a persistent line of thought
- Has an owner and scope
- Has a token budget
- Has encoding rules
- Records decisions and history
- Is auditable
- Exists across all spheres
"""

import pytest
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import uuid

# ═══════════════════════════════════════════════════════════════════════════════
# THREAD CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadType(str, Enum):
    CHAT = "chat"
    AGENT = "agent"
    TASK = "task"
    MEETING = "meeting"


class ThreadStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PAUSED = "paused"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


VALID_SPHERE_IDS = [
    "personal", "business", "government", "creative",
    "community", "social", "entertainment", "team", "scholar"
]

ENCODING_MODES = ["standard", "compressed", "minimal", "custom"]


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK THREAD CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class MockThread:
    """Mock Thread (.chenu) for testing."""
    
    def __init__(
        self,
        title: str,
        type: ThreadType = ThreadType.CHAT,
        sphere_id: str = "personal",
        owner_id: str = None,
        token_budget: int = 5000,
        encoding_mode: str = "standard",
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.type = type
        self.sphere_id = sphere_id
        self.owner_id = owner_id or str(uuid.uuid4())
        self.status = ThreadStatus.ACTIVE
        self.token_budget = token_budget
        self.tokens_used = 0
        self.encoding_mode = encoding_mode
        self.messages: List[Dict] = []
        self.decisions: List[Dict] = []
        self.history: List[Dict] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_auditable = True
    
    @property
    def tokens_remaining(self) -> int:
        return self.token_budget - self.tokens_used
    
    def add_message(self, role: MessageRole, content: str, tokens: int = 0):
        """Add a message to the thread."""
        message = {
            "id": str(uuid.uuid4()),
            "role": role.value,
            "content": content,
            "tokens_used": tokens,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.messages.append(message)
        self.tokens_used += tokens
        self.updated_at = datetime.utcnow()
        
        # Record in history for audit
        self.history.append({
            "action": "message_added",
            "message_id": message["id"],
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        return message
    
    def record_decision(self, decision: str, context: Dict = None):
        """Record a decision in the thread."""
        decision_record = {
            "id": str(uuid.uuid4()),
            "decision": decision,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.decisions.append(decision_record)
        self.history.append({
            "action": "decision_recorded",
            "decision_id": decision_record["id"],
            "timestamp": datetime.utcnow().isoformat(),
        })
        return decision_record
    
    def archive(self):
        """Archive the thread."""
        self.status = ThreadStatus.ARCHIVED
        self.updated_at = datetime.utcnow()
        self.history.append({
            "action": "archived",
            "timestamp": datetime.utcnow().isoformat(),
        })


class MockThreadManager:
    """Mock Thread manager for testing."""
    
    def __init__(self):
        self.threads: Dict[str, MockThread] = {}
    
    def create_thread(self, **kwargs) -> MockThread:
        """Create a new thread."""
        thread = MockThread(**kwargs)
        self.threads[thread.id] = thread
        return thread
    
    def get_thread(self, thread_id: str) -> Optional[MockThread]:
        """Get a thread by ID."""
        return self.threads.get(thread_id)
    
    def get_threads_by_sphere(self, sphere_id: str) -> List[MockThread]:
        """Get all threads in a sphere."""
        return [t for t in self.threads.values() if t.sphere_id == sphere_id]
    
    def get_threads_by_owner(self, owner_id: str) -> List[MockThread]:
        """Get all threads owned by a user."""
        return [t for t in self.threads.values() if t.owner_id == owner_id]
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread (L10: DELETION_COMPLETENESS)."""
        if thread_id in self.threads:
            del self.threads[thread_id]
            return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD CREATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadCreation:
    """Tests for thread creation."""

    def test_create_thread(self):
        """Should create a thread."""
        thread = MockThread(title="Test Thread")
        assert thread is not None
        assert thread.title == "Test Thread"

    def test_thread_has_uuid(self):
        """Thread should have UUID."""
        thread = MockThread(title="Test")
        assert thread.id is not None
        # Validate UUID format
        uuid.UUID(thread.id)

    def test_thread_has_owner(self):
        """Thread should have owner."""
        thread = MockThread(title="Test", owner_id="user_123")
        assert thread.owner_id == "user_123"

    def test_thread_has_scope(self):
        """Thread should have scope (sphere_id)."""
        thread = MockThread(title="Test", sphere_id="business")
        assert thread.sphere_id == "business"

    def test_thread_has_token_budget(self):
        """Thread should have token budget."""
        thread = MockThread(title="Test", token_budget=10000)
        assert thread.token_budget == 10000

    def test_thread_has_encoding_rules(self):
        """Thread should have encoding rules."""
        thread = MockThread(title="Test", encoding_mode="compressed")
        assert thread.encoding_mode == "compressed"

    def test_thread_default_status_active(self):
        """Thread should default to active status."""
        thread = MockThread(title="Test")
        assert thread.status == ThreadStatus.ACTIVE

    def test_thread_has_timestamps(self):
        """Thread should have creation timestamps."""
        thread = MockThread(title="Test")
        assert thread.created_at is not None
        assert thread.updated_at is not None


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD TYPES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadTypes:
    """Tests for thread types."""

    def test_chat_thread_type(self):
        """Should support chat thread type."""
        thread = MockThread(title="Test", type=ThreadType.CHAT)
        assert thread.type == ThreadType.CHAT

    def test_agent_thread_type(self):
        """Should support agent thread type."""
        thread = MockThread(title="Test", type=ThreadType.AGENT)
        assert thread.type == ThreadType.AGENT

    def test_task_thread_type(self):
        """Should support task thread type."""
        thread = MockThread(title="Test", type=ThreadType.TASK)
        assert thread.type == ThreadType.TASK

    def test_meeting_thread_type(self):
        """Should support meeting thread type."""
        thread = MockThread(title="Test", type=ThreadType.MEETING)
        assert thread.type == ThreadType.MEETING


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD MESSAGES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadMessages:
    """Tests for thread messages."""

    def test_add_user_message(self):
        """Should add user message."""
        thread = MockThread(title="Test")
        msg = thread.add_message(MessageRole.USER, "Hello", tokens=10)
        
        assert len(thread.messages) == 1
        assert msg["role"] == "user"

    def test_add_assistant_message(self):
        """Should add assistant message."""
        thread = MockThread(title="Test")
        msg = thread.add_message(MessageRole.ASSISTANT, "Hi there", tokens=15)
        
        assert msg["role"] == "assistant"

    def test_add_system_message(self):
        """Should add system message."""
        thread = MockThread(title="Test")
        msg = thread.add_message(MessageRole.SYSTEM, "Context info", tokens=5)
        
        assert msg["role"] == "system"

    def test_message_tracks_tokens(self):
        """Message should track tokens used."""
        thread = MockThread(title="Test")
        thread.add_message(MessageRole.USER, "Hello", tokens=50)
        
        assert thread.tokens_used == 50

    def test_multiple_messages_accumulate_tokens(self):
        """Multiple messages should accumulate tokens."""
        thread = MockThread(title="Test")
        thread.add_message(MessageRole.USER, "Hello", tokens=50)
        thread.add_message(MessageRole.ASSISTANT, "Hi", tokens=30)
        
        assert thread.tokens_used == 80

    def test_tokens_remaining_calculation(self):
        """Should calculate remaining tokens."""
        thread = MockThread(title="Test", token_budget=1000)
        thread.add_message(MessageRole.USER, "Hello", tokens=200)
        
        assert thread.tokens_remaining == 800

    def test_message_has_uuid(self):
        """Message should have UUID."""
        thread = MockThread(title="Test")
        msg = thread.add_message(MessageRole.USER, "Hello")
        
        assert msg["id"] is not None
        uuid.UUID(msg["id"])


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD DECISIONS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadDecisions:
    """Tests for thread decision recording."""

    def test_record_decision(self):
        """Should record a decision."""
        thread = MockThread(title="Test")
        decision = thread.record_decision("Approved project budget")
        
        assert len(thread.decisions) == 1
        assert decision["decision"] == "Approved project budget"

    def test_decision_has_context(self):
        """Decision should have context."""
        thread = MockThread(title="Test")
        decision = thread.record_decision(
            "Selected vendor",
            context={"vendor_id": "v_123", "amount": 5000}
        )
        
        assert decision["context"]["vendor_id"] == "v_123"

    def test_decision_has_timestamp(self):
        """Decision should have timestamp."""
        thread = MockThread(title="Test")
        decision = thread.record_decision("Test decision")
        
        assert "timestamp" in decision

    def test_decision_recorded_in_history(self):
        """Decision should be recorded in history."""
        thread = MockThread(title="Test")
        thread.record_decision("Test decision")
        
        assert any(h["action"] == "decision_recorded" for h in thread.history)


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD HISTORY TESTS (AUDIT)
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadHistory:
    """Tests for thread history (audit trail)."""

    def test_thread_is_auditable(self):
        """Thread should be auditable (per Memory Prompt)."""
        thread = MockThread(title="Test")
        assert thread.is_auditable is True

    def test_messages_recorded_in_history(self):
        """Messages should be recorded in history."""
        thread = MockThread(title="Test")
        thread.add_message(MessageRole.USER, "Hello")
        
        assert any(h["action"] == "message_added" for h in thread.history)

    def test_archive_recorded_in_history(self):
        """Archive should be recorded in history."""
        thread = MockThread(title="Test")
        thread.archive()
        
        assert any(h["action"] == "archived" for h in thread.history)

    def test_history_has_timestamps(self):
        """History entries should have timestamps."""
        thread = MockThread(title="Test")
        thread.add_message(MessageRole.USER, "Hello")
        
        assert "timestamp" in thread.history[0]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SPHERE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadSpheres:
    """Tests for threads across spheres."""

    def test_thread_in_personal_sphere(self):
        """Thread should work in personal sphere."""
        thread = MockThread(title="Test", sphere_id="personal")
        assert thread.sphere_id == "personal"

    def test_thread_in_business_sphere(self):
        """Thread should work in business sphere."""
        thread = MockThread(title="Test", sphere_id="business")
        assert thread.sphere_id == "business"

    def test_thread_in_scholar_sphere(self):
        """Thread should work in scholar sphere (9th sphere)."""
        thread = MockThread(title="Test", sphere_id="scholar")
        assert thread.sphere_id == "scholar"

    def test_threads_exist_across_all_spheres(self):
        """Threads should exist across all 9 spheres."""
        manager = MockThreadManager()
        
        for sphere_id in VALID_SPHERE_IDS:
            thread = manager.create_thread(
                title=f"Thread in {sphere_id}",
                sphere_id=sphere_id
            )
            assert thread.sphere_id == sphere_id
        
        assert len(manager.threads) == 9


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD MANAGER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadManager:
    """Tests for thread manager."""

    def test_create_thread_via_manager(self):
        """Should create thread via manager."""
        manager = MockThreadManager()
        thread = manager.create_thread(title="Test Thread")
        
        assert thread.id in manager.threads

    def test_get_thread_by_id(self):
        """Should get thread by ID."""
        manager = MockThreadManager()
        created = manager.create_thread(title="Test")
        
        retrieved = manager.get_thread(created.id)
        assert retrieved.id == created.id

    def test_get_threads_by_sphere(self):
        """Should get threads by sphere."""
        manager = MockThreadManager()
        manager.create_thread(title="Business 1", sphere_id="business")
        manager.create_thread(title="Business 2", sphere_id="business")
        manager.create_thread(title="Personal", sphere_id="personal")
        
        business_threads = manager.get_threads_by_sphere("business")
        assert len(business_threads) == 2

    def test_get_threads_by_owner(self):
        """Should get threads by owner."""
        manager = MockThreadManager()
        manager.create_thread(title="Thread 1", owner_id="user_123")
        manager.create_thread(title="Thread 2", owner_id="user_123")
        manager.create_thread(title="Thread 3", owner_id="user_456")
        
        user_threads = manager.get_threads_by_owner("user_123")
        assert len(user_threads) == 2

    def test_delete_thread(self):
        """Should delete thread (L10: DELETION_COMPLETENESS)."""
        manager = MockThreadManager()
        thread = manager.create_thread(title="To Delete")
        thread_id = thread.id
        
        result = manager.delete_thread(thread_id)
        assert result is True
        assert manager.get_thread(thread_id) is None


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD ENCODING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadEncoding:
    """Tests for thread encoding rules."""

    def test_standard_encoding_mode(self):
        """Should support standard encoding mode."""
        thread = MockThread(title="Test", encoding_mode="standard")
        assert thread.encoding_mode == "standard"

    def test_compressed_encoding_mode(self):
        """Should support compressed encoding mode."""
        thread = MockThread(title="Test", encoding_mode="compressed")
        assert thread.encoding_mode == "compressed"

    def test_minimal_encoding_mode(self):
        """Should support minimal encoding mode."""
        thread = MockThread(title="Test", encoding_mode="minimal")
        assert thread.encoding_mode == "minimal"

    def test_all_encoding_modes_supported(self):
        """Should support all encoding modes."""
        for mode in ENCODING_MODES:
            thread = MockThread(title="Test", encoding_mode=mode)
            assert thread.encoding_mode == mode


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD TOKEN BUDGET TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadTokenBudget:
    """Tests for thread token budget."""

    def test_default_token_budget(self):
        """Should have default token budget."""
        thread = MockThread(title="Test")
        assert thread.token_budget > 0

    def test_custom_token_budget(self):
        """Should support custom token budget."""
        thread = MockThread(title="Test", token_budget=25000)
        assert thread.token_budget == 25000

    def test_tokens_used_starts_at_zero(self):
        """Tokens used should start at zero."""
        thread = MockThread(title="Test")
        assert thread.tokens_used == 0

    def test_tokens_remaining_equals_budget_initially(self):
        """Initially, remaining should equal budget."""
        thread = MockThread(title="Test", token_budget=10000)
        assert thread.tokens_remaining == 10000


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT THREAD COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadMemoryPromptCompliance:
    """Tests ensuring thread compliance with Memory Prompt."""

    def test_threads_are_first_class_objects(self):
        """Threads (.chenu) are FIRST-CLASS OBJECTS."""
        thread = MockThread(title="Test")
        
        # Should have all first-class properties
        assert thread.id is not None
        assert thread.owner_id is not None
        assert thread.sphere_id is not None
        assert thread.token_budget is not None
        assert thread.encoding_mode is not None

    def test_thread_represents_persistent_thought(self):
        """Thread represents a persistent line of thought."""
        thread = MockThread(title="Project Planning")
        thread.add_message(MessageRole.USER, "Let's plan the project")
        thread.add_message(MessageRole.ASSISTANT, "I'll help you plan")
        
        # Messages persist
        assert len(thread.messages) == 2

    def test_thread_has_owner_and_scope(self):
        """Thread has an owner and scope."""
        thread = MockThread(
            title="Test",
            owner_id="user_123",
            sphere_id="business"
        )
        
        assert thread.owner_id == "user_123"
        assert thread.sphere_id == "business"

    def test_thread_has_token_budget(self):
        """Thread has a token budget."""
        thread = MockThread(title="Test", token_budget=15000)
        assert thread.token_budget == 15000

    def test_thread_has_encoding_rules(self):
        """Thread has encoding rules."""
        thread = MockThread(title="Test", encoding_mode="compressed")
        assert thread.encoding_mode in ENCODING_MODES

    def test_thread_records_decisions(self):
        """Thread records decisions."""
        thread = MockThread(title="Test")
        thread.record_decision("Approved budget")
        
        assert len(thread.decisions) == 1

    def test_thread_records_history(self):
        """Thread records history."""
        thread = MockThread(title="Test")
        thread.add_message(MessageRole.USER, "Hello")
        
        assert len(thread.history) > 0

    def test_thread_is_auditable(self):
        """Thread is auditable."""
        thread = MockThread(title="Test")
        assert thread.is_auditable is True

    def test_threads_exist_across_all_9_spheres(self):
        """Threads exist across all 9 spheres."""
        assert len(VALID_SPHERE_IDS) == 9
        
        for sphere_id in VALID_SPHERE_IDS:
            thread = MockThread(title="Test", sphere_id=sphere_id)
            assert thread.sphere_id == sphere_id
