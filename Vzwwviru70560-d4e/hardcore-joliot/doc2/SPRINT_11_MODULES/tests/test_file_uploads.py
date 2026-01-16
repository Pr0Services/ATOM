"""CHE·NU™ - File Upload Tests"""
import pytest
from io import BytesIO

class TestFileUploads:
    def test_upload_document(self, client, auth_headers):
        file_data = BytesIO(b"Test document content")
        files = {"file": ("test.pdf", file_data, "application/pdf")}
        
        resp = client.post("/api/v1/documents/upload",
                          files=files,
                          headers=auth_headers)
        assert resp.status_code == 201
        assert "url" in resp.json()
    
    def test_upload_size_limit(self, client, auth_headers):
        # 10MB file
        large_file = BytesIO(b"x" * 10 * 1024 * 1024)
        files = {"file": ("large.pdf", large_file, "application/pdf")}
        
        resp = client.post("/api/v1/documents/upload",
                          files=files,
                          headers=auth_headers)
        assert resp.status_code == 413  # Payload too large
    
    def test_upload_invalid_type(self, client, auth_headers):
        file_data = BytesIO(b"malicious content")
        files = {"file": ("virus.exe", file_data, "application/exe")}
        
        resp = client.post("/api/v1/documents/upload",
                          files=files,
                          headers=auth_headers)
        assert resp.status_code == 400  # Bad request
    
    def test_bulk_upload(self, client, auth_headers):
        files = [
            ("files", ("doc1.pdf", BytesIO(b"content1"), "application/pdf")),
            ("files", ("doc2.pdf", BytesIO(b"content2"), "application/pdf")),
        ]
        
        resp = client.post("/api/v1/documents/bulk-upload",
                          files=files,
                          headers=auth_headers)
        assert resp.status_code == 201
        assert len(resp.json()["uploaded"]) == 2
