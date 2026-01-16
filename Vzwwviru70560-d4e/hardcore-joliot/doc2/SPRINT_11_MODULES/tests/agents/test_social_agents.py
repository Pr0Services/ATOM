"""CHE·NU™ - Social Agents Tests"""
import pytest

class TestMediaManager:
    def test_init(self, media_manager):
        assert media_manager.agent_id == "social.media_manager"
        assert len(media_manager.capabilities) == 12
    
    def test_schedule_post(self, media_manager):
        result = media_manager.execute_capability("schedule_post", {"content": "Test"})
        assert result["success"] is True

@pytest.fixture
def media_manager():
    from backend.agents.social.media_manager import MediaManager
    return MediaManager()
