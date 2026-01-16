"""CHE·NU™ - Entertainment Agents Tests"""
import pytest

class TestCurator:
    def test_init(self, curator):
        assert curator.agent_id == "entertainment.curator"
        assert len(curator.capabilities) == 12
    
    def test_recommend_media(self, curator):
        result = curator.execute_capability("recommend_media", {"preferences": ["sci-fi"]})
        assert result["success"] is True

@pytest.fixture
def curator():
    from backend.agents.entertainment.curator import Curator
    return Curator()
