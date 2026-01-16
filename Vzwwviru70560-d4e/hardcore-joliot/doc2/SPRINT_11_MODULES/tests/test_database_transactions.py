"""CHE·NU™ - Database Transaction Tests"""
import pytest
from sqlalchemy import text

class TestTransactions:
    def test_rollback_on_error(self, db_session):
        try:
            db_session.execute(text("INSERT INTO users (email) VALUES ('test@test.com')"))
            db_session.execute(text("INSERT INTO users (email) VALUES ('test@test.com')"))  # Duplicate
            db_session.commit()
        except Exception:
            db_session.rollback()
        
        result = db_session.execute(text("SELECT COUNT(*) FROM users WHERE email='test@test.com'"))
        assert result.scalar() == 0  # No rows inserted
    
    def test_atomic_operations(self, client, auth_headers):
        # Create contact and deal in one transaction
        resp = client.post("/api/v1/crm/contact-with-deal",
                          json={
                              "contact": {"email": "test@test.com"},
                              "deal": {"amount": 1000}
                          },
                          headers=auth_headers)
        assert resp.status_code == 201
        
        # Both should exist or neither
        contact_exists = client.get("/api/v1/crm/contacts", headers=auth_headers)
        deal_exists = client.get("/api/v1/crm/deals", headers=auth_headers)
        
        if resp.status_code == 201:
            assert len(contact_exists.json()["items"]) > 0
            assert len(deal_exists.json()["items"]) > 0

class TestConcurrency:
    def test_concurrent_updates(self, client, auth_headers):
        import threading
        results = []
        
        def update_thread(thread_id):
            resp = client.put(f"/api/v1/threads/{thread_id}",
                             json={"title": f"Update {threading.current_thread().name}"},
                             headers=auth_headers)
            results.append(resp.status_code)
        
        threads = [threading.Thread(target=update_thread, args=(1,)) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # All should succeed or handle optimistic locking
        assert all(r in [200, 409] for r in results)
    
    def test_deadlock_prevention(self, db_session):
        # Simulate potential deadlock scenario
        # Implementation depends on specific deadlock risks
        pass
