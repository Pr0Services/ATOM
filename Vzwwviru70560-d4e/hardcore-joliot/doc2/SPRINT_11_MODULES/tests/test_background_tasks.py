"""CHE·NU™ - Background Tasks Tests"""
import pytest
from unittest.mock import patch, Mock

class TestBackgroundTasks:
    def test_email_task(self, client, auth_headers):
        with patch('backend.tasks.send_email') as mock_send:
            resp = client.post("/api/v1/invoices/1/send",
                              headers=auth_headers)
            assert resp.status_code == 200
            mock_send.assert_called_once()
    
    def test_report_generation(self, client, auth_headers):
        resp = client.post("/api/v1/reports/generate",
                          json={"type": "monthly"},
                          headers=auth_headers)
        assert resp.status_code == 202  # Accepted
        
        # Check task status
        task_id = resp.json()["task_id"]
        status_resp = client.get(f"/api/v1/tasks/{task_id}",
                                headers=auth_headers)
        assert status_resp.json()["status"] in ["pending", "running", "completed"]
    
    def test_bulk_operation(self, client, auth_headers):
        resp = client.post("/api/v1/contacts/bulk-import",
                          json={"contacts": [{"email": f"user{i}@test.com"} for i in range(100)]},
                          headers=auth_headers)
        assert resp.status_code == 202

class TestScheduledTasks:
    def test_daily_digest(self):
        from backend.tasks import daily_digest
        result = daily_digest.apply()
        assert result.successful()
    
    def test_cleanup_old_data(self):
        from backend.tasks import cleanup_old_data
        result = cleanup_old_data.apply()
        assert result.successful()
