"""CHE·NU™ - Rate Limiting Tests"""
import pytest
import time

class TestRateLimiting:
    def test_api_rate_limit(self, client, auth_headers):
        # Make 100 requests
        responses = []
        for i in range(100):
            resp = client.get("/api/v1/health", headers=auth_headers)
            responses.append(resp.status_code)
        
        # Some should be rate limited (429)
        assert 429 in responses
    
    def test_auth_rate_limit(self, client):
        for i in range(10):
            resp = client.post("/api/v1/auth/login", 
                              json={"email": "test@test.com", "password": "wrong"})
        
        # Should be rate limited
        assert resp.status_code == 429
    
    def test_rate_limit_reset(self, client, auth_headers):
        # Hit rate limit
        for i in range(100):
            client.get("/api/v1/health", headers=auth_headers)
        
        # Wait for reset (e.g., 60 seconds)
        time.sleep(61)
        
        # Should work again
        resp = client.get("/api/v1/health", headers=auth_headers)
        assert resp.status_code == 200
