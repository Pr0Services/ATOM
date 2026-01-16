"""CHE·NU™ - MyTeam Agents Tests"""
import pytest

class TestOrchestrator:
    def test_init(self, orchestrator):
        assert orchestrator.agent_id == "myteam.orchestrator"
        assert len(orchestrator.capabilities) == 12
    
    def test_assign_task(self, orchestrator):
        result = orchestrator.execute_capability("assign_task", {"task_id": 1, "member_id": 1})
        assert result["success"] is True

@pytest.fixture
def orchestrator():
    from backend.agents.myteam.orchestrator import Orchestrator
    return Orchestrator()
