"""CHE·NU™ - Personal Agents Tests"""
import pytest

class TestPersonalAssistant:
    def test_init(self, assistant):
        assert assistant.agent_id == "personal.assistant"
        assert len(assistant.capabilities) == 12
    
    def test_track_habit(self, assistant):
        result = assistant.execute_capability("track_habit", {"habit_id": 1})
        assert result["success"] is True

@pytest.fixture
def assistant():
    from backend.agents.personal.assistant import PersonalAssistant
    return PersonalAssistant()
