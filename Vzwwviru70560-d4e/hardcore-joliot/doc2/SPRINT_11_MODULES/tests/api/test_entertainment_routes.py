"""CHE·NU™ - Entertainment Routes Tests"""
import pytest

class TestMediaCatalog:
    def test_add_media(self, client, auth_headers):
        data = {"title": "Movie Title", "type": "movie", "rating": 8.5}
        resp = client.post("/api/v1/entertainment/media", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_list_media(self, client, auth_headers):
        resp = client.get("/api/v1/entertainment/media", headers=auth_headers)
        assert resp.status_code == 200

class TestPlaylists:
    def test_create_playlist(self, client, auth_headers):
        data = {"name": "Watch Later", "type": "movies"}
        resp = client.post("/api/v1/entertainment/playlists", json=data, headers=auth_headers)
        assert resp.status_code == 201

class TestWatchParties:
    def test_create_party(self, client, auth_headers, sample_media):
        data = {"media_id": sample_media["id"], "scheduled_at": "2026-01-20T20:00:00Z"}
        resp = client.post("/api/v1/entertainment/watch-parties", json=data, headers=auth_headers)
        assert resp.status_code == 201

@pytest.fixture
def sample_media(client, auth_headers):
    data = {"title": "Test Movie", "type": "movie"}
    return client.post("/api/v1/entertainment/media", json=data, headers=auth_headers).json()
