"""
CHE·NU™ - Community Routes Tests
"""
import pytest


class TestCommunityGroups:
    def test_create_group(self, client, auth_headers):
        data = {"name": "Tech Enthusiasts", "visibility": "public"}
        resp = client.post("/api/v1/community/groups", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_join_group(self, client, auth_headers, sample_group):
        resp = client.post(f"/api/v1/community/groups/{sample_group['id']}/join", headers=auth_headers)
        assert resp.status_code == 200


class TestCommunityEvents:
    def test_create_event(self, client, auth_headers, sample_group):
        data = {
            "title": "Meetup", 
            "group_id": sample_group["id"],
            "date": "2026-01-15T18:00:00Z"
        }
        resp = client.post("/api/v1/community/events", json=data, headers=auth_headers)
        assert resp.status_code == 201


class TestCommunityPosts:
    def test_create_post(self, client, auth_headers, sample_group):
        data = {"content": "Hello community!", "group_id": sample_group["id"]}
        resp = client.post("/api/v1/community/posts", json=data, headers=auth_headers)
        assert resp.status_code == 201


@pytest.fixture
def sample_group(client, auth_headers):
    data = {"name": "Test Group", "visibility": "public"}
    return client.post("/api/v1/community/groups", json=data, headers=auth_headers).json()
