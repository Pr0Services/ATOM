"""
============================================================================
CHE·NU™ V69 — API TESTS
============================================================================
Version: 1.0.0
Purpose: Test API endpoints and middleware
============================================================================
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from ..core.app import create_app
from ..core.config import get_settings, APISettings, Environment


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def test_settings():
    """Test settings"""
    return APISettings(
        environment=Environment.DEVELOPMENT,
        debug=True,
        opa_enabled=False,
        rate_limit_enabled=False,
    )


@pytest.fixture
def app(test_settings):
    """Test app"""
    return create_app(test_settings)


@pytest.fixture
def client(app):
    """Test client"""
    return TestClient(app)


# ============================================================================
# HEALTH TESTS
# ============================================================================

class TestHealth:
    """Test health endpoints"""
    
    def test_health_check(self, client):
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "components" in data
    
    def test_readiness(self, client):
        response = client.get("/api/v1/ready")
        
        assert response.status_code == 200
        assert response.json()["ready"] is True
    
    def test_liveness(self, client):
        response = client.get("/api/v1/live")
        
        assert response.status_code == 200
        assert response.json()["alive"] is True


# ============================================================================
# ROOT TESTS
# ============================================================================

class TestRoot:
    """Test root endpoints"""
    
    def test_root(self, client):
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "CHE·NU™ API"
        assert data["status"] == "operational"
    
    def test_api_info(self, client):
        response = client.get("/api")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "endpoints" in data["data"]


# ============================================================================
# AUTH TESTS
# ============================================================================

class TestAuth:
    """Test authentication endpoints"""
    
    def test_login(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_get_me(self, client):
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
    
    def test_logout(self, client):
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == 200
        assert response.json()["success"] is True


# ============================================================================
# SIMULATION TESTS
# ============================================================================

class TestSimulations:
    """Test simulation endpoints"""
    
    def test_create_simulation(self, client):
        response = client.post(
            "/api/v1/simulations",
            json={
                "name": "Test Simulation",
                "description": "Test description",
                "t_end": 100,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Simulation"
        assert "simulation_id" in data
    
    def test_get_simulation(self, client):
        response = client.get("/api/v1/simulations/sim-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["simulation_id"] == "sim-001"
    
    def test_run_simulation(self, client):
        response = client.post(
            "/api/v1/simulations/sim-001/run",
            json={"sign_artifacts": True},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["chain_valid"] is True
    
    def test_delete_simulation(self, client):
        response = client.delete("/api/v1/simulations/sim-001")
        
        assert response.status_code == 200
        assert response.json()["success"] is True


# ============================================================================
# SCENARIO TESTS
# ============================================================================

class TestScenarios:
    """Test scenario endpoints"""
    
    def test_create_scenario(self, client):
        response = client.post(
            "/api/v1/scenarios",
            json={
                "simulation_id": "sim-001",
                "name": "Test Scenario",
                "initial_values": {"Budget": 1000000},
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Scenario"
    
    def test_compare_scenarios(self, client):
        response = client.post(
            "/api/v1/scenarios/compare",
            json={
                "baseline_id": "baseline-001",
                "scenario_ids": ["scenario-002", "scenario-003"],
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["baseline_id"] == "baseline-001"
        assert len(data["comparisons"]) == 2


# ============================================================================
# AGENT TESTS
# ============================================================================

class TestAgents:
    """Test agent endpoints"""
    
    def test_create_agent(self, client):
        response = client.post(
            "/api/v1/agents",
            json={
                "name": "Test Agent",
                "level": "L2",
                "sphere": "Business",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Agent"
        assert data["level"] == "L2"
    
    def test_get_agent(self, client):
        response = client.get("/api/v1/agents/agent-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == "agent-001"
    
    def test_activate_agent(self, client):
        response = client.post("/api/v1/agents/agent-001/activate")
        
        assert response.status_code == 200
        assert response.json()["status"] == "active"
    
    def test_execute_action(self, client):
        response = client.post(
            "/api/v1/agents/agent-001/actions",
            json={
                "action_type": "read",
                "target": "data.financial",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "action_id" in data
    
    def test_get_hierarchy(self, client):
        response = client.get("/api/v1/agents/hierarchy")
        
        assert response.status_code == 200
        data = response.json()
        assert "roots" in data


# ============================================================================
# CHECKPOINT TESTS
# ============================================================================

class TestCheckpoints:
    """Test checkpoint endpoints"""
    
    def test_list_pending(self, client):
        response = client.get("/api/v1/checkpoints/pending")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_checkpoint(self, client):
        response = client.get("/api/v1/checkpoints/cp-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["checkpoint_id"] == "cp-001"
    
    def test_resolve_checkpoint_approve(self, client):
        response = client.post(
            "/api/v1/checkpoints/cp-001/resolve",
            json={
                "approved": True,
                "notes": "Approved for testing",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
    
    def test_resolve_checkpoint_deny(self, client):
        response = client.post(
            "/api/v1/checkpoints/cp-002/resolve",
            json={
                "approved": False,
                "notes": "Too risky",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "denied"


# ============================================================================
# XR PACK TESTS
# ============================================================================

class TestXRPacks:
    """Test XR Pack endpoints"""
    
    def test_generate_xr_pack(self, client):
        response = client.post(
            "/api/v1/xr-packs/generate",
            json={
                "simulation_id": "sim-001",
                "sign_pack": True,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["simulation_id"] == "sim-001"
        assert data["signed"] is True
    
    def test_get_xr_pack(self, client):
        response = client.get("/api/v1/xr-packs/pack-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["pack_id"] == "pack-001"
    
    def test_get_manifest(self, client):
        response = client.get("/api/v1/xr-packs/pack-001/manifest")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data


# ============================================================================
# CAUSAL TESTS
# ============================================================================

class TestCausal:
    """Test causal inference endpoints"""
    
    def test_create_dag(self, client):
        response = client.post(
            "/api/v1/causal/dags",
            json={
                "name": "Test DAG",
                "description": "Test causal graph",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test DAG"
    
    def test_run_inference(self, client):
        response = client.post(
            "/api/v1/causal/inference",
            json={
                "dag_id": "dag-001",
                "treatment": "Budget",
                "outcome": "Production",
                "data": {},
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "ate" in data
        assert data["identifiable"] is True


# ============================================================================
# AUDIT TESTS
# ============================================================================

class TestAudit:
    """Test audit endpoints"""
    
    def test_list_events(self, client):
        response = client.get("/api/v1/audit/events")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_report(self, client):
        response = client.get("/api/v1/audit/simulations/sim-001/report")
        
        assert response.status_code == 200
        data = response.json()
        assert data["simulation_id"] == "sim-001"
        assert data["chain_valid"] is True
    
    def test_verify_chain(self, client):
        response = client.post(
            "/api/v1/audit/verify",
            json="sim-001",
        )
        
        assert response.status_code == 200
        assert response.json()["valid"] is True


# ============================================================================
# WEBSOCKET TESTS
# ============================================================================

class TestWebSocket:
    """Test WebSocket endpoints"""
    
    def test_ws_stats(self, client):
        response = client.get("/ws/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "active_connections" in data


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
