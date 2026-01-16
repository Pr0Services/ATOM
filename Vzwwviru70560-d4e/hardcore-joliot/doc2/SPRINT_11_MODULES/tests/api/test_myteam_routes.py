"""CHE·NU™ - MyTeam Routes Tests"""
import pytest

class TestTeams:
    def test_create_team(self, client, auth_headers):
        data = {"name": "Dev Team", "description": "Engineering team"}
        resp = client.post("/api/v1/myteam/teams", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_add_member(self, client, auth_headers, sample_team):
        data = {"email": "member@example.com", "role": "developer"}
        resp = client.post(f"/api/v1/myteam/teams/{sample_team['id']}/members", json=data, headers=auth_headers)
        assert resp.status_code == 201

class TestSkills:
    def test_add_skill(self, client, auth_headers):
        data = {"name": "Python", "level": "expert"}
        resp = client.post("/api/v1/myteam/skills", json=data, headers=auth_headers)
        assert resp.status_code == 201

@pytest.fixture
def sample_team(client, auth_headers):
    data = {"name": "Test Team"}
    return client.post("/api/v1/myteam/teams", json=data, headers=auth_headers).json()
