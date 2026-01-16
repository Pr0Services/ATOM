"""CHE·NU™ - Government Routes Tests"""
import pytest

class TestOfficialDocuments:
    def test_upload_document(self, client, auth_headers):
        data = {"type": "tax_return", "year": 2024, "url": "https://storage/doc.pdf"}
        resp = client.post("/api/v1/government/documents", json=data, headers=auth_headers)
        assert resp.status_code == 201
    
    def test_list_documents(self, client, auth_headers):
        resp = client.get("/api/v1/government/documents", headers=auth_headers)
        assert resp.status_code == 200

class TestDeadlines:
    def test_create_deadline(self, client, auth_headers):
        data = {"title": "Tax Filing", "due_date": "2026-04-15", "category": "tax"}
        resp = client.post("/api/v1/government/deadlines", json=data, headers=auth_headers)
        assert resp.status_code == 201

class TestForms:
    def test_fill_form(self, client, auth_headers):
        data = {"form_type": "w9", "data": {"name": "John Doe", "ssn": "XXX-XX-1234"}}
        resp = client.post("/api/v1/government/forms", json=data, headers=auth_headers)
        assert resp.status_code == 201
