"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              CHE·NU™ PERSONAL PRODUCTIVITY — TEST SUITE                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta

# Import modules
import sys
sys.path.insert(0, '/home/claude/PERSONAL_PRODUCTIVITY_V68/backend')

from spheres.personal.agents.note_assistant import (
    NoteAssistantAgent, NoteAIEngine, NoteType, NoteStatus, Note, NoteEnhancement
)
from spheres.personal.agents.task_manager import (
    TaskManagerAgent, TaskAIEngine, TaskPriority, TaskStatus, RecurrenceType, Task
)


# ═══════════════════════════════════════════════════════════════════════════════
# NOTE ASSISTANT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNoteAIEngine:
    """Tests for NoteAIEngine."""
    
    def test_local_enhancement_basic(self):
        """Test local enhancement without API."""
        engine = NoteAIEngine()
        
        result = engine._local_enhancement("This is a test note about Python programming")
        
        assert isinstance(result, NoteEnhancement)
        assert result.suggested_title
        assert isinstance(result.extracted_tags, list)
        assert result.note_type == NoteType.NOTE
    
    def test_local_enhancement_meeting(self):
        """Test meeting detection."""
        engine = NoteAIEngine()
        
        content = """Meeting Notes
        Attendees: John, Sarah
        Discussion points..."""
        
        result = engine._local_enhancement(content)
        assert result.note_type == NoteType.MEETING
    
    def test_local_enhancement_todo(self):
        """Test todo detection."""
        engine = NoteAIEngine()
        
        content = """TODO List
        - [ ] Task 1
        - [ ] Task 2"""
        
        result = engine._local_enhancement(content)
        assert result.note_type == NoteType.TODO
    
    def test_local_enhancement_idea(self):
        """Test idea detection."""
        engine = NoteAIEngine()
        
        content = "Idea for a new app: brainstorm about features"
        
        result = engine._local_enhancement(content)
        assert result.note_type == NoteType.IDEA


class TestNoteAssistantAgent:
    """Tests for NoteAssistantAgent."""
    
    @pytest.fixture
    def agent(self):
        return NoteAssistantAgent()
    
    @pytest.mark.asyncio
    async def test_create_note_basic(self, agent):
        """Test basic note creation."""
        note = await agent.create_note(
            content="Test note content",
            user_id="test_user",
            auto_enhance=False,
        )
        
        assert note.id
        assert note.content == "Test note content"
        assert note.user_id == "test_user"
        assert note.status == NoteStatus.ACTIVE
        assert note.word_count == 3
    
    @pytest.mark.asyncio
    async def test_create_note_with_metadata(self, agent):
        """Test note creation with metadata."""
        note = await agent.create_note(
            content="Test note",
            user_id="test_user",
            title="My Title",
            tags=["tag1", "tag2"],
            folder="Work",
            auto_enhance=False,
        )
        
        assert note.title == "My Title"
        assert note.tags == ["tag1", "tag2"]
        assert note.folder == "Work"
    
    @pytest.mark.asyncio
    async def test_get_note(self, agent):
        """Test getting a note."""
        created = await agent.create_note(
            content="Findable note",
            user_id="test_user",
            auto_enhance=False,
        )
        
        found = agent.get_note(created.id, "test_user")
        assert found is not None
        assert found.id == created.id
        
        not_found = agent.get_note("nonexistent", "test_user")
        assert not_found is None
    
    @pytest.mark.asyncio
    async def test_update_note(self, agent):
        """Test updating a note."""
        note = await agent.create_note(
            content="Original",
            user_id="test_user",
            auto_enhance=False,
        )
        
        updated = await agent.update_note(
            note_id=note.id,
            user_id="test_user",
            content="Updated content",
            tags=["new_tag"],
        )
        
        assert updated.content == "Updated content"
        assert updated.tags == ["new_tag"]
        assert updated.updated_at > note.created_at
    
    @pytest.mark.asyncio
    async def test_delete_note(self, agent):
        """Test deleting a note."""
        note = await agent.create_note(
            content="Delete me",
            user_id="test_user",
            auto_enhance=False,
        )
        
        result = agent.delete_note(note.id, "test_user")
        assert result is True
        
        found = agent.get_note(note.id, "test_user")
        assert found is None
    
    @pytest.mark.asyncio
    async def test_list_notes_filter_folder(self, agent):
        """Test listing notes with folder filter."""
        await agent.create_note(content="Work note", user_id="test_user", folder="Work", auto_enhance=False)
        await agent.create_note(content="Personal note", user_id="test_user", folder="Personal", auto_enhance=False)
        
        work_notes = agent.list_notes("test_user", folder="Work")
        assert len(work_notes) == 1
        assert work_notes[0].folder == "Work"
    
    @pytest.mark.asyncio
    async def test_list_notes_filter_tag(self, agent):
        """Test listing notes with tag filter."""
        await agent.create_note(content="Tagged", user_id="test_user", tags=["important"], auto_enhance=False)
        await agent.create_note(content="Not tagged", user_id="test_user", tags=[], auto_enhance=False)
        
        tagged = agent.list_notes("test_user", tag="important")
        assert len(tagged) == 1
    
    @pytest.mark.asyncio
    async def test_list_notes_search(self, agent):
        """Test listing notes with search."""
        await agent.create_note(content="Python programming guide", user_id="test_user", auto_enhance=False)
        await agent.create_note(content="JavaScript tutorial", user_id="test_user", auto_enhance=False)
        
        results = agent.list_notes("test_user", search="Python")
        assert len(results) == 1
        assert "Python" in results[0].content
    
    @pytest.mark.asyncio
    async def test_get_folders(self, agent):
        """Test getting folders."""
        await agent.create_note(content="Note 1", user_id="test_user", folder="Work", auto_enhance=False)
        await agent.create_note(content="Note 2", user_id="test_user", folder="Work", auto_enhance=False)
        await agent.create_note(content="Note 3", user_id="test_user", folder="Personal", auto_enhance=False)
        
        folders = agent.get_folders("test_user")
        work_folder = next((f for f in folders if f["name"] == "Work"), None)
        assert work_folder is not None
        assert work_folder["count"] == 2
    
    @pytest.mark.asyncio
    async def test_get_stats(self, agent):
        """Test getting statistics."""
        await agent.create_note(content="Note one two three", user_id="test_user", auto_enhance=False)
        await agent.create_note(content="Note four five", user_id="test_user", auto_enhance=False)
        
        stats = agent.get_stats("test_user")
        assert stats["total_notes"] == 2
        assert stats["total_words"] == 7


# ═══════════════════════════════════════════════════════════════════════════════
# TASK MANAGER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTaskAIEngine:
    """Tests for TaskAIEngine."""
    
    def test_local_analysis_urgent(self):
        """Test urgent detection."""
        engine = TaskAIEngine()
        
        result = engine._local_analysis("URGENT: Fix production bug", "Critical issue")
        assert result.suggested_priority == TaskPriority.URGENT
    
    def test_local_analysis_high(self):
        """Test high priority detection."""
        engine = TaskAIEngine()
        
        result = engine._local_analysis("Important deadline tomorrow", "")
        assert result.suggested_priority == TaskPriority.HIGH
    
    def test_local_analysis_someday(self):
        """Test someday detection."""
        engine = TaskAIEngine()
        
        result = engine._local_analysis("Someday learn guitar", "")
        assert result.suggested_priority == TaskPriority.SOMEDAY
    
    def test_local_analysis_due_today(self):
        """Test due today detection."""
        engine = TaskAIEngine()
        
        result = engine._local_analysis("Submit report today", "")
        assert result.suggested_due_date is not None
        assert result.suggested_due_date.date() == datetime.now(timezone.utc).date()
    
    def test_local_analysis_project_detection(self):
        """Test project detection."""
        engine = TaskAIEngine()
        
        result = engine._local_analysis("Go to gym for workout", "")
        assert result.suggested_project == "Health"
        
        result = engine._local_analysis("Client meeting at 2pm", "")
        assert result.suggested_project == "Work"


class TestTaskManagerAgent:
    """Tests for TaskManagerAgent."""
    
    @pytest.fixture
    def agent(self):
        return TaskManagerAgent()
    
    @pytest.mark.asyncio
    async def test_create_task_basic(self, agent):
        """Test basic task creation."""
        task = await agent.create_task(
            title="Test task",
            user_id="test_user",
            auto_suggest=False,
        )
        
        assert task.id
        assert task.title == "Test task"
        assert task.user_id == "test_user"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.MEDIUM
    
    @pytest.mark.asyncio
    async def test_create_task_with_priority(self, agent):
        """Test task creation with priority."""
        task = await agent.create_task(
            title="High priority task",
            user_id="test_user",
            priority=TaskPriority.HIGH,
            auto_suggest=False,
        )
        
        assert task.priority == TaskPriority.HIGH
        assert task.ai_score > 50  # High priority should have higher score
    
    @pytest.mark.asyncio
    async def test_create_task_with_due_date(self, agent):
        """Test task creation with due date."""
        due = datetime.now(timezone.utc) + timedelta(days=1)
        
        task = await agent.create_task(
            title="Due tomorrow",
            user_id="test_user",
            due_date=due,
            auto_suggest=False,
        )
        
        assert task.due_date == due
    
    @pytest.mark.asyncio
    async def test_complete_task(self, agent):
        """Test completing a task."""
        task = await agent.create_task(
            title="Complete me",
            user_id="test_user",
            auto_suggest=False,
        )
        
        completed = await agent.complete_task(task.id, "test_user", actual_minutes=30)
        
        assert completed.status == TaskStatus.DONE
        assert completed.completed_at is not None
        assert completed.actual_minutes == 30
    
    @pytest.mark.asyncio
    async def test_delete_task(self, agent):
        """Test deleting a task."""
        task = await agent.create_task(
            title="Delete me",
            user_id="test_user",
            auto_suggest=False,
        )
        
        result = agent.delete_task(task.id, "test_user")
        assert result is True
        
        found = agent.get_task(task.id, "test_user")
        assert found is None
    
    @pytest.mark.asyncio
    async def test_list_tasks_filter_status(self, agent):
        """Test listing tasks with status filter."""
        task1 = await agent.create_task(title="Active", user_id="test_user", auto_suggest=False)
        task2 = await agent.create_task(title="Completed", user_id="test_user", auto_suggest=False)
        await agent.complete_task(task2.id, "test_user")
        
        active = agent.list_tasks("test_user", status=TaskStatus.TODO)
        assert len(active) == 1
        
        done = agent.list_tasks("test_user", status=TaskStatus.DONE)
        assert len(done) == 1
    
    @pytest.mark.asyncio
    async def test_list_tasks_filter_priority(self, agent):
        """Test listing tasks with priority filter."""
        await agent.create_task(title="High", user_id="test_user", priority=TaskPriority.HIGH, auto_suggest=False)
        await agent.create_task(title="Low", user_id="test_user", priority=TaskPriority.LOW, auto_suggest=False)
        
        high = agent.list_tasks("test_user", priority=TaskPriority.HIGH)
        assert len(high) == 1
        assert high[0].priority == TaskPriority.HIGH
    
    @pytest.mark.asyncio
    async def test_list_tasks_overdue(self, agent):
        """Test listing overdue tasks."""
        past = datetime.now(timezone.utc) - timedelta(days=1)
        future = datetime.now(timezone.utc) + timedelta(days=1)
        
        await agent.create_task(title="Overdue", user_id="test_user", due_date=past, auto_suggest=False)
        await agent.create_task(title="Future", user_id="test_user", due_date=future, auto_suggest=False)
        
        overdue = agent.list_tasks("test_user", overdue=True)
        assert len(overdue) == 1
        assert overdue[0].title == "Overdue"
    
    @pytest.mark.asyncio
    async def test_get_today_view(self, agent):
        """Test getting today view."""
        today = datetime.now(timezone.utc).replace(hour=12)
        past = datetime.now(timezone.utc) - timedelta(days=1)
        
        await agent.create_task(title="Today", user_id="test_user", due_date=today, auto_suggest=False)
        await agent.create_task(title="Overdue", user_id="test_user", due_date=past, auto_suggest=False)
        await agent.create_task(title="Urgent", user_id="test_user", priority=TaskPriority.URGENT, auto_suggest=False)
        
        view = agent.get_today_view("test_user")
        
        assert "date" in view
        assert "overdue" in view
        assert "due_today" in view
        assert "high_priority" in view
        assert "stats" in view
    
    @pytest.mark.asyncio
    async def test_create_project(self, agent):
        """Test creating a project."""
        project = agent.create_project(
            name="Work",
            user_id="test_user",
            color="#3B82F6",
        )
        
        assert project.id
        assert project.name == "Work"
        assert project.color == "#3B82F6"
        assert project.task_count == 0
    
    @pytest.mark.asyncio
    async def test_task_project_association(self, agent):
        """Test task-project association."""
        project = agent.create_project(name="Work", user_id="test_user")
        
        task = await agent.create_task(
            title="Work task",
            user_id="test_user",
            project_id=project.id,
            auto_suggest=False,
        )
        
        assert task.project_id == project.id
        
        # Check project task count
        projects = agent.get_projects("test_user")
        work_project = next((p for p in projects if p.id == project.id), None)
        assert work_project.task_count == 1
    
    @pytest.mark.asyncio
    async def test_get_stats(self, agent):
        """Test getting statistics."""
        await agent.create_task(title="Task 1", user_id="test_user", auto_suggest=False)
        task2 = await agent.create_task(title="Task 2", user_id="test_user", auto_suggest=False)
        await agent.complete_task(task2.id, "test_user")
        
        stats = agent.get_stats("test_user")
        
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["completion_rate"] == 50.0


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.asyncio
    async def test_note_and_task_workflow(self):
        """Test combined note and task workflow."""
        note_agent = NoteAssistantAgent()
        task_agent = TaskManagerAgent()
        
        # Create a meeting note
        note = await note_agent.create_note(
            content="""Meeting Notes
            - Discussed Q1 goals
            - Action: Review budget
            - Action: Schedule follow-up""",
            user_id="test_user",
            auto_enhance=False,
        )
        
        # Create tasks from meeting
        task1 = await task_agent.create_task(
            title="Review Q1 budget",
            user_id="test_user",
            auto_suggest=False,
        )
        task2 = await task_agent.create_task(
            title="Schedule follow-up meeting",
            user_id="test_user",
            auto_suggest=False,
        )
        
        # Complete one task
        await task_agent.complete_task(task1.id, "test_user")
        
        # Check stats
        note_stats = note_agent.get_stats("test_user")
        task_stats = task_agent.get_stats("test_user")
        
        assert note_stats["total_notes"] == 1
        assert task_stats["total"] == 2
        assert task_stats["completed"] == 1


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧪 Running Personal Productivity Tests...")
    print("=" * 60)
    
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
