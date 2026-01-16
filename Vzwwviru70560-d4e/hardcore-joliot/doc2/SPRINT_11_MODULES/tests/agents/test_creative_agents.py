"""CHE·NU™ - Creative Agents Tests"""
import pytest

class TestCreativeAssistant:
    def test_init(self, creative_assistant):
        assert creative_assistant.agent_id == "studio.creative_assistant"
        assert len(creative_assistant.capabilities) == 11
    
    def test_generate_idea(self, creative_assistant):
        result = creative_assistant.execute_capability("generate_idea", {"theme": "futuristic"})
        assert result["success"] is True

@pytest.fixture
def creative_assistant():
    from backend.agents.studio.creative_assistant import CreativeAssistant
    return CreativeAssistant()
