"""CHE·NU™ - Scholar Agents Tests"""
import pytest

class TestResearchAssistant:
    def test_init(self, research_assistant):
        assert research_assistant.agent_id == "scholar.research_assistant"
        assert research_assistant.level == "L3"
        assert len(research_assistant.capabilities) == 12
    
    def test_search_papers(self, research_assistant):
        result = research_assistant.execute_capability("search_papers", {"query": "machine learning"})
        assert result["success"] is True
        assert "papers" in result
    
    def test_cite_source(self, research_assistant):
        result = research_assistant.execute_capability("cite_source", {"format": "apa"})
        assert result["success"] is True

@pytest.fixture
def research_assistant():
    from backend.agents.scholar.research_assistant import ResearchAssistant
    return ResearchAssistant()
