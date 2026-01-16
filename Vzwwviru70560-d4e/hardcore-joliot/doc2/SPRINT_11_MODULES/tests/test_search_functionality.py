"""CHE·NU™ - Search Functionality Tests"""
import pytest

class TestFullTextSearch:
    def test_search_contacts(self, client, auth_headers, multiple_contacts):
        resp = client.get("/api/v1/search?q=john&entity=contacts",
                         headers=auth_headers)
        assert resp.status_code == 200
        results = resp.json()["results"]
        assert all("john" in r["name"].lower() for r in results)
    
    def test_search_across_entities(self, client, auth_headers):
        resp = client.get("/api/v1/search?q=project",
                         headers=auth_headers)
        assert resp.status_code == 200
        results = resp.json()
        
        # Should search contacts, deals, threads, etc.
        assert "contacts" in results
        assert "deals" in results
        assert "threads" in results
    
    def test_search_with_filters(self, client, auth_headers):
        resp = client.get("/api/v1/search?q=test&sphere=business&date_from=2024-01-01",
                         headers=auth_headers)
        assert resp.status_code == 200
    
    def test_search_pagination(self, client, auth_headers):
        resp = client.get("/api/v1/search?q=test&page=1&per_page=10",
                         headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "page" in data

class TestAutocomple:
    def test_autocomplete_contacts(self, client, auth_headers):
        resp = client.get("/api/v1/autocomplete/contacts?q=jo",
                         headers=auth_headers)
        assert resp.status_code == 200
        suggestions = resp.json()["suggestions"]
        assert len(suggestions) <= 10  # Limit results
