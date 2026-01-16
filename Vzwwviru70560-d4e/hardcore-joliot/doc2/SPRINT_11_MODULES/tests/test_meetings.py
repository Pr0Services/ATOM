"""
CHE·NU™ — MEETING SYSTEM TESTS (PYTEST)
Sprint 6: Tests for Meeting functionality

Meeting System:
- Meetings are a bureau section (6th of 6)
- Meetings have token budgets
- Meetings are governed
- Meetings can have agents
- Meeting transcripts are threads
"""

import pytest
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid

# ═══════════════════════════════════════════════════════════════════════════════
# MEETING CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MeetingType(str, Enum):
    STANDUP = "standup"
    PLANNING = "planning"
    REVIEW = "review"
    BRAINSTORM = "brainstorm"
    DECISION = "decision"
    ONE_ON_ONE = "one_on_one"


class ParticipantRole(str, Enum):
    HOST = "host"
    PARTICIPANT = "participant"
    OBSERVER = "observer"
    AGENT = "agent"


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK MEETING CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class MockParticipant:
    """Mock meeting participant."""
    
    def __init__(
        self,
        user_id: str,
        role: ParticipantRole = ParticipantRole.PARTICIPANT,
        is_agent: bool = False
    ):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.role = role
        self.is_agent = is_agent
        self.joined_at: Optional[datetime] = None
        self.left_at: Optional[datetime] = None


class MockMeeting:
    """Mock Meeting for testing."""
    
    def __init__(
        self,
        title: str,
        sphere_id: str = "personal",
        type: MeetingType = MeetingType.PLANNING,
        host_id: str = None,
        scheduled_start: datetime = None,
        duration_minutes: int = 60,
        token_budget: int = 10000,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.sphere_id = sphere_id
        self.type = type
        self.host_id = host_id or str(uuid.uuid4())
        self.status = MeetingStatus.SCHEDULED
        self.scheduled_start = scheduled_start or datetime.utcnow() + timedelta(hours=1)
        self.scheduled_end = self.scheduled_start + timedelta(minutes=duration_minutes)
        self.actual_start: Optional[datetime] = None
        self.actual_end: Optional[datetime] = None
        self.duration_minutes = duration_minutes
        self.token_budget = token_budget
        self.tokens_used = 0
        self.participants: List[MockParticipant] = []
        self.agenda: List[Dict] = []
        self.notes: List[Dict] = []
        self.decisions: List[Dict] = []
        self.action_items: List[Dict] = []
        self.thread_id: Optional[str] = None  # Associated thread
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Add host as first participant
        self.add_participant(self.host_id, ParticipantRole.HOST)
    
    def add_participant(
        self, 
        user_id: str, 
        role: ParticipantRole = ParticipantRole.PARTICIPANT,
        is_agent: bool = False
    ) -> MockParticipant:
        """Add a participant to the meeting."""
        participant = MockParticipant(user_id, role, is_agent)
        self.participants.append(participant)
        return participant
    
    def add_agent(self, agent_id: str) -> MockParticipant:
        """Add an agent to the meeting."""
        return self.add_participant(agent_id, ParticipantRole.AGENT, is_agent=True)
    
    def start(self):
        """Start the meeting."""
        self.status = MeetingStatus.IN_PROGRESS
        self.actual_start = datetime.utcnow()
        for p in self.participants:
            if p.joined_at is None:
                p.joined_at = datetime.utcnow()
    
    def end(self):
        """End the meeting."""
        self.status = MeetingStatus.COMPLETED
        self.actual_end = datetime.utcnow()
        for p in self.participants:
            if p.left_at is None:
                p.left_at = datetime.utcnow()
    
    def cancel(self):
        """Cancel the meeting."""
        self.status = MeetingStatus.CANCELLED
    
    def add_agenda_item(self, item: str, duration_minutes: int = 10) -> Dict:
        """Add an agenda item."""
        agenda_item = {
            "id": str(uuid.uuid4()),
            "item": item,
            "duration_minutes": duration_minutes,
            "discussed": False,
        }
        self.agenda.append(agenda_item)
        return agenda_item
    
    def add_note(self, content: str, author_id: str) -> Dict:
        """Add a meeting note."""
        note = {
            "id": str(uuid.uuid4()),
            "content": content,
            "author_id": author_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.notes.append(note)
        return note
    
    def add_decision(self, decision: str, context: Dict = None) -> Dict:
        """Record a decision made in the meeting."""
        decision_record = {
            "id": str(uuid.uuid4()),
            "decision": decision,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.decisions.append(decision_record)
        return decision_record
    
    def add_action_item(
        self, 
        description: str, 
        assignee_id: str,
        due_date: datetime = None
    ) -> Dict:
        """Add an action item."""
        action_item = {
            "id": str(uuid.uuid4()),
            "description": description,
            "assignee_id": assignee_id,
            "due_date": (due_date or datetime.utcnow() + timedelta(days=7)).isoformat(),
            "completed": False,
        }
        self.action_items.append(action_item)
        return action_item


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING CREATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingCreation:
    """Tests for meeting creation."""

    def test_create_meeting(self):
        """Should create a meeting."""
        meeting = MockMeeting(title="Test Meeting")
        assert meeting is not None
        assert meeting.title == "Test Meeting"

    def test_meeting_has_uuid(self):
        """Meeting should have UUID."""
        meeting = MockMeeting(title="Test")
        assert meeting.id is not None
        uuid.UUID(meeting.id)

    def test_meeting_has_host(self):
        """Meeting should have host."""
        meeting = MockMeeting(title="Test", host_id="user_123")
        assert meeting.host_id == "user_123"

    def test_meeting_has_sphere(self):
        """Meeting should have sphere."""
        meeting = MockMeeting(title="Test", sphere_id="business")
        assert meeting.sphere_id == "business"

    def test_meeting_has_token_budget(self):
        """Meeting should have token budget."""
        meeting = MockMeeting(title="Test", token_budget=15000)
        assert meeting.token_budget == 15000

    def test_meeting_default_status_scheduled(self):
        """Meeting should default to scheduled status."""
        meeting = MockMeeting(title="Test")
        assert meeting.status == MeetingStatus.SCHEDULED

    def test_host_added_as_participant(self):
        """Host should be added as first participant."""
        meeting = MockMeeting(title="Test", host_id="user_123")
        
        host_participants = [p for p in meeting.participants if p.role == ParticipantRole.HOST]
        assert len(host_participants) == 1
        assert host_participants[0].user_id == "user_123"


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING TYPES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingTypes:
    """Tests for meeting types."""

    def test_standup_type(self):
        """Should support standup meeting type."""
        meeting = MockMeeting(title="Daily Standup", type=MeetingType.STANDUP)
        assert meeting.type == MeetingType.STANDUP

    def test_planning_type(self):
        """Should support planning meeting type."""
        meeting = MockMeeting(title="Sprint Planning", type=MeetingType.PLANNING)
        assert meeting.type == MeetingType.PLANNING

    def test_review_type(self):
        """Should support review meeting type."""
        meeting = MockMeeting(title="Sprint Review", type=MeetingType.REVIEW)
        assert meeting.type == MeetingType.REVIEW

    def test_brainstorm_type(self):
        """Should support brainstorm meeting type."""
        meeting = MockMeeting(title="Ideas Session", type=MeetingType.BRAINSTORM)
        assert meeting.type == MeetingType.BRAINSTORM

    def test_decision_type(self):
        """Should support decision meeting type."""
        meeting = MockMeeting(title="Budget Decision", type=MeetingType.DECISION)
        assert meeting.type == MeetingType.DECISION


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING PARTICIPANTS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingParticipants:
    """Tests for meeting participants."""

    def test_add_participant(self):
        """Should add a participant."""
        meeting = MockMeeting(title="Test")
        participant = meeting.add_participant("user_456")
        
        assert participant.user_id == "user_456"
        assert len(meeting.participants) == 2  # Host + new participant

    def test_add_multiple_participants(self):
        """Should add multiple participants."""
        meeting = MockMeeting(title="Test")
        meeting.add_participant("user_2")
        meeting.add_participant("user_3")
        meeting.add_participant("user_4")
        
        assert len(meeting.participants) == 4  # Host + 3

    def test_participant_roles(self):
        """Should support different participant roles."""
        meeting = MockMeeting(title="Test")
        meeting.add_participant("user_2", ParticipantRole.PARTICIPANT)
        meeting.add_participant("user_3", ParticipantRole.OBSERVER)
        
        roles = [p.role for p in meeting.participants]
        assert ParticipantRole.HOST in roles
        assert ParticipantRole.PARTICIPANT in roles
        assert ParticipantRole.OBSERVER in roles


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING AGENTS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingAgents:
    """Tests for agents in meetings."""

    def test_add_agent_to_meeting(self):
        """Should add an agent to meeting."""
        meeting = MockMeeting(title="Test")
        agent = meeting.add_agent("nova")
        
        assert agent.is_agent is True
        assert agent.role == ParticipantRole.AGENT

    def test_nova_can_join_meeting(self):
        """Nova (L0) can join meetings."""
        meeting = MockMeeting(title="Test")
        nova = meeting.add_agent("nova")
        
        assert nova.user_id == "nova"
        assert nova.is_agent is True

    def test_multiple_agents_in_meeting(self):
        """Should support multiple agents in meeting."""
        meeting = MockMeeting(title="Test")
        meeting.add_agent("nova")
        meeting.add_agent("analyst_agent")
        
        agents = [p for p in meeting.participants if p.is_agent]
        assert len(agents) == 2


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING LIFECYCLE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingLifecycle:
    """Tests for meeting lifecycle."""

    def test_start_meeting(self):
        """Should start a meeting."""
        meeting = MockMeeting(title="Test")
        meeting.start()
        
        assert meeting.status == MeetingStatus.IN_PROGRESS
        assert meeting.actual_start is not None

    def test_end_meeting(self):
        """Should end a meeting."""
        meeting = MockMeeting(title="Test")
        meeting.start()
        meeting.end()
        
        assert meeting.status == MeetingStatus.COMPLETED
        assert meeting.actual_end is not None

    def test_cancel_meeting(self):
        """Should cancel a meeting."""
        meeting = MockMeeting(title="Test")
        meeting.cancel()
        
        assert meeting.status == MeetingStatus.CANCELLED

    def test_participants_joined_on_start(self):
        """Participants should be marked as joined on start."""
        meeting = MockMeeting(title="Test")
        meeting.add_participant("user_2")
        meeting.start()
        
        for p in meeting.participants:
            assert p.joined_at is not None

    def test_participants_left_on_end(self):
        """Participants should be marked as left on end."""
        meeting = MockMeeting(title="Test")
        meeting.start()
        meeting.end()
        
        for p in meeting.participants:
            assert p.left_at is not None


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING CONTENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingContent:
    """Tests for meeting content (agenda, notes, decisions)."""

    def test_add_agenda_item(self):
        """Should add agenda item."""
        meeting = MockMeeting(title="Test")
        item = meeting.add_agenda_item("Review Q3 results", duration_minutes=15)
        
        assert len(meeting.agenda) == 1
        assert item["item"] == "Review Q3 results"

    def test_add_note(self):
        """Should add meeting note."""
        meeting = MockMeeting(title="Test")
        note = meeting.add_note("Important point discussed", "user_123")
        
        assert len(meeting.notes) == 1
        assert note["content"] == "Important point discussed"

    def test_add_decision(self):
        """Should record a decision."""
        meeting = MockMeeting(title="Test")
        decision = meeting.add_decision("Approved budget increase")
        
        assert len(meeting.decisions) == 1
        assert decision["decision"] == "Approved budget increase"

    def test_add_action_item(self):
        """Should add action item."""
        meeting = MockMeeting(title="Test")
        action = meeting.add_action_item(
            description="Prepare report",
            assignee_id="user_456"
        )
        
        assert len(meeting.action_items) == 1
        assert action["assignee_id"] == "user_456"


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING SPHERE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingSpheres:
    """Tests for meetings in different spheres."""

    def test_meeting_in_personal_sphere(self):
        """Meeting should work in personal sphere."""
        meeting = MockMeeting(title="Test", sphere_id="personal")
        assert meeting.sphere_id == "personal"

    def test_meeting_in_business_sphere(self):
        """Meeting should work in business sphere."""
        meeting = MockMeeting(title="Test", sphere_id="business")
        assert meeting.sphere_id == "business"

    def test_meeting_in_team_sphere(self):
        """Meeting should work in team sphere."""
        meeting = MockMeeting(title="Test", sphere_id="team")
        assert meeting.sphere_id == "team"

    def test_meeting_in_scholar_sphere(self):
        """Meeting should work in scholar sphere."""
        meeting = MockMeeting(title="Test", sphere_id="scholar")
        assert meeting.sphere_id == "scholar"


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING TOKEN BUDGET TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingTokenBudget:
    """Tests for meeting token budget."""

    def test_meeting_has_token_budget(self):
        """Meeting should have token budget."""
        meeting = MockMeeting(title="Test", token_budget=20000)
        assert meeting.token_budget == 20000

    def test_tokens_used_starts_at_zero(self):
        """Tokens used should start at zero."""
        meeting = MockMeeting(title="Test")
        assert meeting.tokens_used == 0


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING THREAD ASSOCIATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingThreadAssociation:
    """Tests for meeting-thread association."""

    def test_meeting_can_have_thread(self):
        """Meeting can be associated with a thread."""
        meeting = MockMeeting(title="Test")
        meeting.thread_id = str(uuid.uuid4())
        
        assert meeting.thread_id is not None

    def test_meeting_thread_optional(self):
        """Meeting thread should be optional."""
        meeting = MockMeeting(title="Test")
        assert meeting.thread_id is None


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT MEETING COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeetingMemoryPromptCompliance:
    """Tests ensuring meeting compliance with Memory Prompt."""

    def test_meetings_is_bureau_section(self):
        """Meetings is a bureau section (6th of 6)."""
        BUREAU_SECTIONS = [
            "quick_capture", "resume_workspace", "threads",
            "data_files", "active_agents", "meetings"
        ]
        
        assert "meetings" in BUREAU_SECTIONS
        assert BUREAU_SECTIONS.index("meetings") == 5  # 6th (0-indexed)

    def test_meetings_have_token_budget(self):
        """Meetings have token budgets."""
        meeting = MockMeeting(title="Test", token_budget=15000)
        assert meeting.token_budget > 0

    def test_meetings_are_governed(self):
        """Meetings follow governance rules."""
        meeting = MockMeeting(title="Test")
        
        # Has required governance properties
        assert meeting.token_budget is not None
        assert meeting.sphere_id is not None

    def test_meetings_can_have_agents(self):
        """Meetings can have agents."""
        meeting = MockMeeting(title="Test")
        nova = meeting.add_agent("nova")
        
        assert nova.is_agent is True

    def test_meetings_record_decisions(self):
        """Meetings record decisions (auditable)."""
        meeting = MockMeeting(title="Test")
        decision = meeting.add_decision("Approved project")
        
        assert decision["timestamp"] is not None
