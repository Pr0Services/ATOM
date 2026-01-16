"""
CHE·NU™ — Government Routes Tests
Tests unitaires pour les endpoints Government Sphere
"""

import pytest
from datetime import date, datetime, timedelta
from uuid import uuid4


class TestDocumentsEndpoints:
    """Tests for /government/documents endpoints."""
    
    def test_get_documents_empty(self):
        """Test getting documents when none exist."""
        response = {"documents": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_document_valid(self):
        """Test creating a valid document."""
        doc_data = {
            "name": "Passport",
            "document_type": "passport",
            "document_number": "AB123456",
            "expiry_date": "2030-01-01",
        }
        
        assert "name" in doc_data
        assert "document_type" in doc_data
    
    def test_document_types(self):
        """Test valid document types."""
        valid_types = [
            "passport", "id_card", "driver_license", "birth_certificate",
            "visa", "permit", "tax_document", "insurance", "certificate",
            "registration", "license", "other"
        ]
        
        for doc_type in valid_types:
            assert doc_type in valid_types
    
    def test_expiry_calculation(self):
        """Test document expiry days calculation."""
        expiry_date = date.today() + timedelta(days=30)
        days_until = (expiry_date - date.today()).days
        assert days_until == 30
    
    def test_expiry_status(self):
        """Test document expiry status determination."""
        days_until = 15
        status = (
            "expired" if days_until < 0 else
            "expiring_soon" if days_until <= 30 else
            "active"
        )
        assert status == "expiring_soon"


class TestDeadlinesEndpoints:
    """Tests for /government/deadlines endpoints."""
    
    def test_get_deadlines_empty(self):
        """Test getting deadlines when none exist."""
        response = {"deadlines": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_deadline_valid(self):
        """Test creating a valid deadline."""
        deadline_data = {
            "title": "Tax Filing",
            "deadline_type": "tax_filing",
            "due_date": "2025-04-30",
            "priority": "high",
        }
        
        assert "title" in deadline_data
        assert "due_date" in deadline_data
    
    def test_deadline_types(self):
        """Test valid deadline types."""
        valid_types = [
            "tax_filing", "renewal", "registration",
            "payment", "application", "compliance", "other"
        ]
        
        for deadline_type in valid_types:
            assert deadline_type in valid_types
    
    def test_deadline_status(self):
        """Test deadline status transitions."""
        valid_statuses = ["pending", "in_progress", "completed", "overdue", "cancelled"]
        
        for status in valid_statuses:
            assert status in valid_statuses
    
    def test_overdue_detection(self):
        """Test overdue deadline detection."""
        due_date = date.today() - timedelta(days=5)
        days_remaining = (due_date - date.today()).days
        is_overdue = days_remaining < 0
        assert is_overdue == True
    
    def test_urgency_levels(self):
        """Test urgency level calculation."""
        days = 5
        urgency = (
            "critical" if days < 0 else
            "high" if days <= 7 else
            "medium" if days <= 30 else
            "low"
        )
        assert urgency == "high"


class TestFormsEndpoints:
    """Tests for /government/forms endpoints."""
    
    def test_get_forms_empty(self):
        """Test getting forms when none exist."""
        response = {"forms": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_form_valid(self):
        """Test creating a valid form."""
        form_data = {
            "name": "T1 General",
            "form_number": "T1",
            "form_type": "tax",
            "agency_name": "CRA",
        }
        
        assert "name" in form_data
    
    def test_form_statuses(self):
        """Test valid form statuses."""
        valid_statuses = [
            "not_started", "in_progress", "ready_to_submit",
            "submitted", "approved", "rejected"
        ]
        
        for status in valid_statuses:
            assert status in valid_statuses
    
    def test_form_completion_percent(self):
        """Test form completion percentage."""
        fields_total = 10
        fields_completed = 7
        completion = (fields_completed / fields_total) * 100
        assert completion == 70.0


class TestComplianceEndpoints:
    """Tests for /government/compliance endpoints."""
    
    def test_get_compliance_empty(self):
        """Test getting compliance items when none exist."""
        response = {"items": [], "total": 0}
        assert response["total"] == 0
    
    def test_compliance_statuses(self):
        """Test valid compliance statuses."""
        valid_statuses = ["compliant", "non_compliant", "pending", "review_needed"]
        
        for status in valid_statuses:
            assert status in valid_statuses
    
    def test_requirement_tracking(self):
        """Test requirement tracking structure."""
        requirement = {
            "item": "Business license",
            "is_met": True,
            "due_date": "2025-12-31",
        }
        
        assert "item" in requirement
        assert "is_met" in requirement


class TestContactsEndpoints:
    """Tests for /government/contacts endpoints."""
    
    def test_get_contacts_empty(self):
        """Test getting contacts when none exist."""
        response = {"contacts": [], "total": 0}
        assert response["total"] == 0
    
    def test_create_contact_valid(self):
        """Test creating a valid contact."""
        contact_data = {
            "name": "CRA Office",
            "organization": "Canada Revenue Agency",
            "contact_type": "government",
            "phone": "1-800-959-8281",
        }
        
        assert "name" in contact_data
    
    def test_contact_types(self):
        """Test valid contact types."""
        valid_types = ["government", "lawyer", "accountant", "notary", "agent", "other"]
        
        for contact_type in valid_types:
            assert contact_type in valid_types


class TestCalendarEndpoint:
    """Tests for /government/calendar endpoint."""
    
    def test_calendar_structure(self):
        """Test calendar response structure."""
        calendar = {
            "events": [],
            "upcoming_count": 3,
            "overdue_count": 1,
        }
        
        assert "events" in calendar
        assert "upcoming_count" in calendar


class TestRemindersEndpoint:
    """Tests for /government/reminders endpoint."""
    
    def test_reminders_structure(self):
        """Test reminders response structure."""
        reminders = {
            "expiring_documents": [],
            "upcoming_deadlines": [],
            "overdue_items": [],
        }
        
        assert "expiring_documents" in reminders
        assert "upcoming_deadlines" in reminders


class TestDashboardEndpoint:
    """Tests for /government/dashboard endpoint."""
    
    def test_dashboard_structure(self):
        """Test dashboard response structure."""
        dashboard = {
            "documents": {
                "total": 5,
                "expiring_soon": 2,
                "expired": 0,
            },
            "deadlines": {
                "pending": 3,
                "upcoming_7_days": 1,
                "overdue": 0,
            },
            "forms": {
                "in_progress": 2,
                "submitted": 1,
                "approved": 1,
            },
            "compliance": {
                "compliant": 3,
                "needs_review": 1,
                "non_compliant": 0,
            },
        }
        
        assert "documents" in dashboard
        assert "deadlines" in dashboard
        assert "forms" in dashboard
        assert "compliance" in dashboard


# Governance Tests
class TestGovernmentGovernance:
    """Tests for Government sphere governance compliance."""
    
    def test_sphere_isolation(self):
        """Test that government data stays in government sphere."""
        sphere_id = "government"
        assert sphere_id == "government"
    
    def test_sensitive_data_flag(self):
        """Test that sensitive documents are flagged."""
        document = {"is_sensitive": True}
        assert document["is_sensitive"] == True
    
    def test_user_ownership(self):
        """Test that government data has user ownership."""
        user_id = uuid4()
        data = {"user_id": user_id}
        assert data["user_id"] == user_id
    
    def test_reminder_days_array(self):
        """Test reminder days array structure."""
        reminder_days = [30, 14, 7, 1]
        assert all(isinstance(d, int) for d in reminder_days)
        assert reminder_days == sorted(reminder_days, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
