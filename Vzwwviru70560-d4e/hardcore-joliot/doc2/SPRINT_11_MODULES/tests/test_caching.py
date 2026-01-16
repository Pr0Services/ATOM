"""CHE·NU™ - Caching Tests"""
import pytest
import time

class TestRedisCache:
    def test_cache_hit(self, client, auth_headers):
        # First request (cache miss)
        resp1 = client.get("/api/v1/spheres", headers=auth_headers)
        
        # Second request (cache hit)
        resp2 = client.get("/api/v1/spheres", headers=auth_headers)
        
        assert resp1.json() == resp2.json()
    
    def test_cache_invalidation(self, client, auth_headers):
        # Get cached data
        resp1 = client.get("/api/v1/spheres", headers=auth_headers)
        
        # Modify data
        client.post("/api/v1/spheres", json={"name": "New"}, headers=auth_headers)
        
        # Cache should be invalidated
        resp2 = client.get("/api/v1/spheres", headers=auth_headers)
        assert resp1.json() != resp2.json()
    
    def test_cache_ttl(self, client, auth_headers):
        # Get cached data
        resp1 = client.get("/api/v1/spheres", headers=auth_headers)
        
        # Wait for TTL expiry
        time.sleep(301)  # 5 minutes + 1 second
        
        # Should fetch fresh data
        resp2 = client.get("/api/v1/spheres", headers=auth_headers)
        # Response should trigger new DB query
