"""CHE·NU™ - Personal Routes Tests"""
import pytest

class TestGoals:
    def test_create_goal(self, client, auth_headers):
        data = {"title": "Learn Spanish", "target_date": "2026-06-01"}
        resp = client.post("/api/v1/personal/goals", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_update_progress(self, client, auth_headers, sample_goal):
        data = {"progress": 50}
        resp = client.put(f"/api/v1/personal/goals/{sample_goal['id']}", json=data, headers=auth_headers)
        assert resp.status_code == 200

class TestHabits:
    def test_create_habit(self, client, auth_headers):
        data = {"name": "Morning run", "frequency": "daily"}
        resp = client.post("/api/v1/personal/habits", json=data, headers=auth_headers)
        assert resp.status_code == 201

@pytest.fixture
def sample_goal(client, auth_headers):
    data = {"title": "Test Goal", "target_date": "2026-12-31"}
    return client.post("/api/v1/personal/goals", json=data, headers=auth_headers).json()
