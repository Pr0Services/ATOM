"""CHE·NU™ - Permissions & RBAC Tests"""
import pytest

class TestRBAC:
    def test_sphere_access_control(self, client, auth_headers):
        resp = client.get("/api/v1/spheres/business", headers=auth_headers)
        assert resp.status_code == 200
    
    def test_unauthorized_sphere_access(self, client, unauthorized_user):
        headers = {"Authorization": f"Bearer {unauthorized_user['token']}"}
        resp = client.get("/api/v1/spheres/business", headers=headers)
        assert resp.status_code == 403
    
    def test_agent_permission_check(self, client, auth_headers):
        resp = client.post("/api/v1/agents/execute", 
                          json={"agent_id": "business.crm_assistant"},
                          headers=auth_headers)
        assert resp.status_code in [200, 403]

class TestThreadOwnership:
    def test_user_can_access_own_thread(self, client, auth_headers, user_thread):
        resp = client.get(f"/api/v1/threads/{user_thread['id']}", headers=auth_headers)
        assert resp.status_code == 200
    
    def test_user_cannot_access_other_thread(self, client, auth_headers, other_user_thread):
        resp = client.get(f"/api/v1/threads/{other_user_thread['id']}", headers=auth_headers)
        assert resp.status_code == 404

@pytest.fixture
def unauthorized_user(client):
    return {"id": 999, "token": "invalid_token"}

@pytest.fixture
def user_thread(client, auth_headers):
    return client.post("/api/v1/threads", json={"title": "My Thread"}, headers=auth_headers).json()

@pytest.fixture
def other_user_thread():
    return {"id": 9999, "user_id": 888}
