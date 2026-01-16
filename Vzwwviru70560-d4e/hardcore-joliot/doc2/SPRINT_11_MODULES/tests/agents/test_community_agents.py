"""CHE·NU™ - Community Agents Tests"""
import pytest

class TestCommunityManager:
    def test_init(self, community_manager):
        assert community_manager.agent_id == "community.manager"
        assert len(community_manager.capabilities) == 8
    
    def test_moderate_post(self, community_manager):
        result = community_manager.execute_capability("moderate_post", {"post_id": 1})
        assert result["success"] is True

@pytest.fixture
def community_manager():
    from backend.agents.community.community_manager import CommunityManager
    return CommunityManager()
