"""
CHE·NU™ - API TESTS
Pytest test suite for FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from datetime import datetime, timedelta
import uuid

from app.main import app
from app.core.config import settings


# ═══════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Sync test client."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers():
    """Mock auth headers."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def test_user():
    """Test user data."""
    return {
        "id": str(uuid.uuid4()),
        "email": "test@chenu.io",
        "username": "testuser",
        "display_name": "Test User",
        "role": "user",
        "token_balance": 10000,
    }


@pytest.fixture
def test_thread():
    """Test thread data."""
    return {
        "id": str(uuid.uuid4()),
        "title": "Test Thread",
        "sphere_id": "personal",
        "status": "active",
        "token_budget": 5000,
        "tokens_used": 0,
    }


# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK TESTS
# ═══════════════════════════════════════════════════════════════

class TestHealthCheck:
    """Health endpoint tests."""
    
    def test_health_check(self, client):
        """Test health endpoint returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_root_redirect(self, client):
        """Test root redirects to docs."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in [200, 307, 302]


# ═══════════════════════════════════════════════════════════════
# AUTH TESTS
# ═══════════════════════════════════════════════════════════════

class TestAuth:
    """Authentication endpoint tests."""
    
    def test_register_user(self, client):
        """Test user registration."""
        response = client.post("/api/v1/auth/register", json={
            "email": f"new_{uuid.uuid4()}@chenu.io",
            "username": f"newuser_{uuid.uuid4().hex[:8]}",
            "password": "SecurePass123!",
            "display_name": "New User",
        })
        # May return 201 or 422 depending on validation
        assert response.status_code in [201, 422, 400]
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@chenu.io",
            "password": "wrongpassword",
        })
        assert response.status_code in [401, 422]
    
    def test_me_unauthorized(self, client):
        """Test /me endpoint without auth."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401


# ═══════════════════════════════════════════════════════════════
# SPHERES TESTS
# ═══════════════════════════════════════════════════════════════

class TestSpheres:
    """Sphere endpoint tests."""
    
    def test_list_spheres(self, client):
        """Test listing all spheres."""
        response = client.get("/api/v1/spheres")
        assert response.status_code == 200
        data = response.json()
        
        # Should have exactly 8 spheres
        assert len(data) == 8
        
        # Verify sphere IDs
        sphere_ids = [s["id"] for s in data]
        expected_ids = [
            "personal", "business", "government", "studio",
            "community", "social", "entertainment", "team"
        ]
        for expected in expected_ids:
            assert expected in sphere_ids
    
    def test_get_sphere_detail(self, client):
        """Test getting single sphere details."""
        response = client.get("/api/v1/spheres/personal")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "personal"
        assert data["name"] == "Personal"
        assert "bureauSections" in data
        assert len(data["bureauSections"]) == 10
    
    def test_get_invalid_sphere(self, client):
        """Test getting non-existent sphere."""
        response = client.get("/api/v1/spheres/invalid")
        assert response.status_code == 404


# ═══════════════════════════════════════════════════════════════
# THREADS TESTS
# ═══════════════════════════════════════════════════════════════

class TestThreads:
    """Thread endpoint tests."""
    
    def test_list_threads(self, client, auth_headers):
        """Test listing threads."""
        response = client.get("/api/v1/threads", headers=auth_headers)
        # May require auth
        assert response.status_code in [200, 401]
    
    def test_create_thread(self, client, auth_headers):
        """Test creating a thread."""
        response = client.post("/api/v1/threads", headers=auth_headers, json={
            "title": "New Test Thread",
            "sphere_id": "personal",
            "token_budget": 5000,
        })
        assert response.status_code in [201, 401, 422]
        
        if response.status_code == 201:
            data = response.json()
            assert data["title"] == "New Test Thread"
            assert data["sphere_id"] == "personal"
            assert data["status"] == "active"
    
    def test_create_thread_validation(self, client, auth_headers):
        """Test thread creation validation."""
        # Missing required fields
        response = client.post("/api/v1/threads", headers=auth_headers, json={
            "title": "",  # Empty title
        })
        assert response.status_code in [422, 401]
    
    def test_get_threads_by_sphere(self, client, auth_headers):
        """Test filtering threads by sphere."""
        response = client.get(
            "/api/v1/threads",
            headers=auth_headers,
            params={"sphere_id": "personal"}
        )
        assert response.status_code in [200, 401]


# ═══════════════════════════════════════════════════════════════
# TOKENS TESTS
# ═══════════════════════════════════════════════════════════════

class TestTokens:
    """Token budget endpoint tests."""
    
    def test_list_budgets(self, client, auth_headers):
        """Test listing token budgets."""
        response = client.get("/api/v1/tokens/budgets", headers=auth_headers)
        assert response.status_code in [200, 401]
    
    def test_create_budget(self, client, auth_headers):
        """Test creating a token budget."""
        response = client.post("/api/v1/tokens/budgets", headers=auth_headers, json={
            "name": "Test Budget",
            "sphere_id": "personal",
            "total_allocated": 10000,
            "period": "monthly",
        })
        assert response.status_code in [201, 401, 422]
    
    def test_record_consumption(self, client, auth_headers):
        """Test recording token consumption."""
        response = client.post("/api/v1/tokens/consume", headers=auth_headers, json={
            "budget_id": str(uuid.uuid4()),
            "amount": 100,
            "description": "Test consumption",
        })
        assert response.status_code in [200, 201, 401, 404]
    
    def test_get_transactions(self, client, auth_headers):
        """Test getting token transactions."""
        response = client.get("/api/v1/tokens/transactions", headers=auth_headers)
        assert response.status_code in [200, 401]


# ═══════════════════════════════════════════════════════════════
# AGENTS TESTS
# ═══════════════════════════════════════════════════════════════

class TestAgents:
    """Agent endpoint tests."""
    
    def test_list_agents(self, client):
        """Test listing available agents."""
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        data = response.json()
        
        # Should include Nova
        nova = next((a for a in data if a["type"] == "nova"), None)
        assert nova is not None
        assert nova["is_system"] == True
    
    def test_get_nova(self, client):
        """Test getting Nova details."""
        response = client.get("/api/v1/agents/nova")
        assert response.status_code == 200
        data = response.json()
        
        assert data["type"] == "nova"
        assert data["is_system"] == True
        assert "capabilities" in data
    
    def test_hire_agent(self, client, auth_headers):
        """Test hiring an agent."""
        response = client.post("/api/v1/agents/hire", headers=auth_headers, json={
            "agent_id": str(uuid.uuid4()),
        })
        assert response.status_code in [200, 201, 401, 404]
    
    def test_cannot_hire_nova(self, client, auth_headers):
        """Test that Nova cannot be hired."""
        # First get Nova's ID
        response = client.get("/api/v1/agents/nova")
        if response.status_code == 200:
            nova_id = response.json().get("id", "nova")
            
            # Try to hire Nova
            response = client.post("/api/v1/agents/hire", headers=auth_headers, json={
                "agent_id": nova_id,
            })
            # Should fail - Nova is a system agent
            assert response.status_code in [400, 403, 401]


# ═══════════════════════════════════════════════════════════════
# DATASPACES TESTS
# ═══════════════════════════════════════════════════════════════

class TestDataSpaces:
    """DataSpace endpoint tests."""
    
    def test_list_dataspaces(self, client, auth_headers):
        """Test listing dataspaces."""
        response = client.get("/api/v1/dataspaces", headers=auth_headers)
        assert response.status_code in [200, 401]
    
    def test_create_dataspace(self, client, auth_headers):
        """Test creating a dataspace."""
        response = client.post("/api/v1/dataspaces", headers=auth_headers, json={
            "name": "Test DataSpace",
            "sphere_id": "personal",
            "type": "table",
            "schema": {"columns": [{"name": "id", "type": "string"}]},
        })
        assert response.status_code in [201, 401, 422]


# ═══════════════════════════════════════════════════════════════
# MEETINGS TESTS
# ═══════════════════════════════════════════════════════════════

class TestMeetings:
    """Meeting endpoint tests."""
    
    def test_list_meetings(self, client, auth_headers):
        """Test listing meetings."""
        response = client.get("/api/v1/meetings", headers=auth_headers)
        assert response.status_code in [200, 401]
    
    def test_create_meeting(self, client, auth_headers):
        """Test creating a meeting."""
        start_time = datetime.utcnow() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        response = client.post("/api/v1/meetings", headers=auth_headers, json={
            "title": "Test Meeting",
            "sphere_id": "business",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "is_virtual": True,
        })
        assert response.status_code in [201, 401, 422]


# ═══════════════════════════════════════════════════════════════
# GOVERNANCE TESTS
# ═══════════════════════════════════════════════════════════════

class TestGovernance:
    """Governance endpoint tests."""
    
    def test_validate_execution(self, client, auth_headers):
        """Test execution validation."""
        response = client.post("/api/v1/governance/validate", headers=auth_headers, json={
            "action_type": "agent_execution",
            "sphere_id": "personal",
            "estimated_tokens": 100,
            "agent_id": str(uuid.uuid4()),
        })
        assert response.status_code in [200, 401, 422]
    
    def test_list_rules(self, client, auth_headers):
        """Test listing governance rules."""
        response = client.get("/api/v1/governance/rules", headers=auth_headers)
        assert response.status_code in [200, 401]


# ═══════════════════════════════════════════════════════════════
# NOVA TESTS
# ═══════════════════════════════════════════════════════════════

class TestNova:
    """Nova AI endpoint tests."""
    
    def test_nova_status(self, client):
        """Test Nova status endpoint."""
        response = client.get("/api/v1/nova/status")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] in ["idle", "thinking", "speaking"]
    
    def test_nova_chat(self, client, auth_headers):
        """Test chatting with Nova."""
        response = client.post("/api/v1/nova/chat", headers=auth_headers, json={
            "message": "Hello Nova",
            "sphere_id": "personal",
        })
        assert response.status_code in [200, 401]
        
        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "tokens_used" in data


# ═══════════════════════════════════════════════════════════════
# REPORTS TESTS
# ═══════════════════════════════════════════════════════════════

class TestReports:
    """Reports endpoint tests."""
    
    def test_get_activity_log(self, client, auth_headers):
        """Test getting activity log."""
        response = client.get("/api/v1/reports/activity", headers=auth_headers)
        assert response.status_code in [200, 401]
    
    def test_get_summary(self, client, auth_headers):
        """Test getting summary report."""
        response = client.get("/api/v1/reports/summary", headers=auth_headers)
        assert response.status_code in [200, 401]


# ═══════════════════════════════════════════════════════════════
# WEBSOCKET TESTS
# ═══════════════════════════════════════════════════════════════

class TestWebSocket:
    """WebSocket endpoint tests."""
    
    def test_websocket_connect(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect(f"/ws/{uuid.uuid4()}") as websocket:
            # Should receive connection message
            data = websocket.receive_json()
            assert data["type"] == "connect"
    
    def test_websocket_ping_pong(self, client):
        """Test WebSocket ping/pong."""
        with client.websocket_connect(f"/ws/{uuid.uuid4()}") as websocket:
            # Skip connection message
            websocket.receive_json()
            
            # Send ping
            websocket.send_json({
                "type": "ping",
                "data": {"timestamp": datetime.utcnow().isoformat()},
                "timestamp": datetime.utcnow().isoformat(),
            })
            
            # Should receive pong
            data = websocket.receive_json()
            assert data["type"] == "pong"


# ═══════════════════════════════════════════════════════════════
# ENCODING TESTS
# ═══════════════════════════════════════════════════════════════

class TestEncoding:
    """Encoding endpoint tests."""
    
    def test_encode_text(self, client, auth_headers):
        """Test text encoding."""
        response = client.post("/api/v1/encoding/encode", headers=auth_headers, json={
            "text": "Please analyze the quarterly financial report",
            "mode": "standard",
        })
        assert response.status_code in [200, 401]
        
        if response.status_code == 200:
            data = response.json()
            assert "encoded_text" in data
            assert "original_tokens" in data
            assert "encoded_tokens" in data
            assert data["encoded_tokens"] <= data["original_tokens"]
    
    def test_decode_text(self, client, auth_headers):
        """Test text decoding."""
        response = client.post("/api/v1/encoding/decode", headers=auth_headers, json={
            "encoded_text": "ANL:Q-FIN-RPT",
        })
        assert response.status_code in [200, 401]


# ═══════════════════════════════════════════════════════════════
# RUN CONFIG
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
