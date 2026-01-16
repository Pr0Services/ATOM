"""CHE·NU™ - Social Routes Tests"""
import pytest

class TestSocialPosts:
    def test_create_post(self, client, auth_headers):
        data = {"content": "Hello world!", "visibility": "public"}
        resp = client.post("/api/v1/social/posts", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_like_post(self, client, auth_headers, sample_post):
        resp = client.post(f"/api/v1/social/posts/{sample_post['id']}/like", headers=auth_headers)
        assert resp.status_code == 200

class TestSocialStories:
    def test_create_story(self, client, auth_headers):
        data = {"media_url": "https://example.com/story.jpg"}
        resp = client.post("/api/v1/social/stories", json=data, headers=auth_headers)
        assert resp.status_code == 201

@pytest.fixture
def sample_post(client, auth_headers):
    data = {"content": "Test post"}
    return client.post("/api/v1/social/posts", json=data, headers=auth_headers).json()
