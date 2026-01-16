"""CHE·NU™ - Government Agents Tests"""
import pytest

class TestGovernmentAdmin:
    def test_init(self, admin):
        assert admin.agent_id == "government.admin"
        assert len(admin.capabilities) == 10
    
    def test_track_deadline(self, admin):
        result = admin.execute_capability("track_deadline", {"deadline_id": 1})
        assert result["success"] is True

@pytest.fixture
def admin():
    from backend.agents.government.admin import GovernmentAdmin
    return GovernmentAdmin()
