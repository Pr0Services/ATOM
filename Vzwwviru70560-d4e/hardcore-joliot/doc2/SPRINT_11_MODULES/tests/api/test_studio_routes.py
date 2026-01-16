"""
CHE·NU™ - Studio Routes Tests
"""
import pytest


class TestStudioProjects:
    """Creative projects CRUD"""
    
    def test_create_project(self, client, auth_headers):
        data = {
            "title": "Website Redesign",
            "type": "design",
            "status": "active"
        }
        resp = client.post("/api/v1/studio/projects", json=data, headers=auth_headers)
        assert resp.status_code == 201
        assert resp.json()["title"] == "Website Redesign"
    
    def test_list_projects(self, client, auth_headers, sample_project):
        resp = client.get("/api/v1/studio/projects", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()["items"]) > 0
    
    def test_update_project(self, client, auth_headers, sample_project):
        update = {"status": "completed"}
        resp = client.put(f"/api/v1/studio/projects/{sample_project['id']}", json=update, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"


class TestStudioAssets:
    """Asset management"""
    
    def test_upload_asset(self, client, auth_headers, sample_project):
        data = {
            "project_id": sample_project["id"],
            "name": "logo.png",
            "type": "image",
            "url": "https://storage.example.com/logo.png"
        }
        resp = client.post("/api/v1/studio/assets", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_list_assets(self, client, auth_headers, sample_project):
        resp = client.get(f"/api/v1/studio/projects/{sample_project['id']}/assets", headers=auth_headers)
        assert resp.status_code == 200


@pytest.fixture
def sample_project(client, auth_headers):
    data = {"title": "Test Project", "type": "design"}
    return client.post("/api/v1/studio/projects", json=data, headers=auth_headers).json()
