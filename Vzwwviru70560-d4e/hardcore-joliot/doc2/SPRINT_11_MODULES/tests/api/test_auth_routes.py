"""CHE·NU™ - Auth Routes Tests"""
import pytest

class TestAuth:
    def test_register(self, client):
        data = {"email": "new@test.com", "password": "Pass123!", "first_name": "New", "last_name": "User"}
        resp = client.post("/api/v1/auth/register", json=data)
        assert resp.status_code == 201
    
    def test_login(self, client, sample_user):
        data = {"email": sample_user["email"], "password": "Pass123!"}
        resp = client.post("/api/v1/auth/login", json=data)
        assert resp.status_code == 200
        assert "access_token" in resp.json()
    
    def test_logout(self, client, auth_headers):
        resp = client.post("/api/v1/auth/logout", headers=auth_headers)
        assert resp.status_code == 200

@pytest.fixture
def sample_user(client):
    data = {"email": "user@test.com", "password": "Pass123!", "first_name": "Test", "last_name": "User"}
    return client.post("/api/v1/auth/register", json=data).json()
