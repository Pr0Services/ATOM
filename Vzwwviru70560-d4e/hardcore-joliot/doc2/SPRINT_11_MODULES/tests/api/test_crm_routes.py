"""
CHE·NU™ - CRM Routes Tests
Tests for Business Sphere CRM functionality
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestCRMContacts:
    """Test suite for CRM contacts endpoints"""
    
    def test_list_contacts_empty(self, client, auth_headers):
        """Test listing contacts when empty"""
        response = client.get("/api/v1/crm/contacts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 0
    
    def test_create_contact_success(self, client, auth_headers):
        """Test creating a new contact"""
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "company": "Acme Corp",
            "position": "CEO",
            "tags": ["vip", "decision-maker"]
        }
        response = client.post(
            "/api/v1/crm/contacts",
            json=contact_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["email"] == "john.doe@example.com"
        assert "id" in data
        assert "created_at" in data
    
    def test_create_contact_invalid_email(self, client, auth_headers):
        """Test creating contact with invalid email"""
        contact_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email",
        }
        response = client.post(
            "/api/v1/crm/contacts",
            json=contact_data,
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_contact_duplicate_email(self, client, auth_headers, sample_contact):
        """Test creating contact with duplicate email"""
        contact_data = {
            "first_name": "Another",
            "last_name": "Person",
            "email": sample_contact["email"],
        }
        response = client.post(
            "/api/v1/crm/contacts",
            json=contact_data,
            headers=auth_headers
        )
        assert response.status_code == 409
    
    def test_get_contact_by_id(self, client, auth_headers, sample_contact):
        """Test retrieving a specific contact"""
        contact_id = sample_contact["id"]
        response = client.get(
            f"/api/v1/crm/contacts/{contact_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contact_id
        assert data["email"] == sample_contact["email"]
    
    def test_get_contact_not_found(self, client, auth_headers):
        """Test retrieving non-existent contact"""
        response = client.get(
            "/api/v1/crm/contacts/99999",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_update_contact(self, client, auth_headers, sample_contact):
        """Test updating a contact"""
        contact_id = sample_contact["id"]
        update_data = {
            "phone": "+9876543210",
            "position": "CTO"
        }
        response = client.put(
            f"/api/v1/crm/contacts/{contact_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == "+9876543210"
        assert data["position"] == "CTO"
    
    def test_delete_contact(self, client, auth_headers, sample_contact):
        """Test deleting a contact"""
        contact_id = sample_contact["id"]
        response = client.delete(
            f"/api/v1/crm/contacts/{contact_id}",
            headers=auth_headers
        )
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(
            f"/api/v1/crm/contacts/{contact_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    def test_list_contacts_pagination(self, client, auth_headers, multiple_contacts):
        """Test contact list pagination"""
        response = client.get(
            "/api/v1/crm/contacts?page=1&per_page=5",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 5
        assert "total" in data
        assert "page" in data
        assert "pages" in data
    
    def test_list_contacts_filter_by_company(self, client, auth_headers, multiple_contacts):
        """Test filtering contacts by company"""
        response = client.get(
            "/api/v1/crm/contacts?company=Acme",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for contact in data["items"]:
            assert "Acme" in contact.get("company", "")
    
    def test_search_contacts(self, client, auth_headers, multiple_contacts):
        """Test searching contacts"""
        response = client.get(
            "/api/v1/crm/contacts?search=John",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0


class TestCRMCompanies:
    """Test suite for CRM companies endpoints"""
    
    def test_create_company(self, client, auth_headers):
        """Test creating a company"""
        company_data = {
            "name": "Tech Innovations Inc",
            "industry": "Technology",
            "size": "50-200",
            "website": "https://techinnovations.com",
            "address": "123 Tech Street, Silicon Valley"
        }
        response = client.post(
            "/api/v1/crm/companies",
            json=company_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Tech Innovations Inc"
        assert data["industry"] == "Technology"
        assert "id" in data
    
    def test_list_companies(self, client, auth_headers, sample_company):
        """Test listing companies"""
        response = client.get("/api/v1/crm/companies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
    
    def test_get_company_by_id(self, client, auth_headers, sample_company):
        """Test retrieving a specific company"""
        company_id = sample_company["id"]
        response = client.get(
            f"/api/v1/crm/companies/{company_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company_id


class TestCRMDeals:
    """Test suite for CRM deals endpoints"""
    
    def test_create_deal(self, client, auth_headers, sample_contact, sample_company):
        """Test creating a deal"""
        deal_data = {
            "title": "Q1 Software License",
            "amount": 50000.00,
            "currency": "USD",
            "stage": "proposal",
            "probability": 60,
            "contact_id": sample_contact["id"],
            "company_id": sample_company["id"],
            "expected_close_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        response = client.post(
            "/api/v1/crm/deals",
            json=deal_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Q1 Software License"
        assert data["amount"] == 50000.00
        assert data["stage"] == "proposal"
    
    def test_list_deals(self, client, auth_headers, sample_deal):
        """Test listing deals"""
        response = client.get("/api/v1/crm/deals", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0
    
    def test_update_deal_stage(self, client, auth_headers, sample_deal):
        """Test updating deal stage"""
        deal_id = sample_deal["id"]
        update_data = {
            "stage": "negotiation",
            "probability": 80
        }
        response = client.put(
            f"/api/v1/crm/deals/{deal_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stage"] == "negotiation"
        assert data["probability"] == 80
    
    def test_close_deal_won(self, client, auth_headers, sample_deal):
        """Test closing deal as won"""
        deal_id = sample_deal["id"]
        update_data = {
            "stage": "closed_won",
            "closed_at": datetime.now().isoformat()
        }
        response = client.put(
            f"/api/v1/crm/deals/{deal_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["stage"] == "closed_won"
        assert data["closed_at"] is not None
    
    def test_filter_deals_by_stage(self, client, auth_headers, multiple_deals):
        """Test filtering deals by stage"""
        response = client.get(
            "/api/v1/crm/deals?stage=proposal",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        for deal in data["items"]:
            assert deal["stage"] == "proposal"


class TestCRMPipelines:
    """Test suite for CRM pipelines endpoints"""
    
    def test_get_default_pipeline(self, client, auth_headers):
        """Test retrieving default pipeline"""
        response = client.get("/api/v1/crm/pipelines", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        # Should have at least default pipeline
        assert len(data["items"]) >= 1
    
    def test_create_custom_pipeline(self, client, auth_headers):
        """Test creating a custom pipeline"""
        pipeline_data = {
            "name": "Enterprise Sales",
            "stages": [
                {"name": "Discovery", "order": 1},
                {"name": "Demo", "order": 2},
                {"name": "Proposal", "order": 3},
                {"name": "Negotiation", "order": 4},
                {"name": "Closed Won", "order": 5},
                {"name": "Closed Lost", "order": 6}
            ]
        }
        response = client.post(
            "/api/v1/crm/pipelines",
            json=pipeline_data,
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Enterprise Sales"
        assert len(data["stages"]) == 6
    
    def test_update_pipeline_stages(self, client, auth_headers, sample_pipeline):
        """Test updating pipeline stages"""
        pipeline_id = sample_pipeline["id"]
        update_data = {
            "stages": [
                {"name": "Lead", "order": 1},
                {"name": "Qualified", "order": 2},
                {"name": "Proposal", "order": 3},
                {"name": "Won", "order": 4}
            ]
        }
        response = client.put(
            f"/api/v1/crm/pipelines/{pipeline_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["stages"]) == 4


class TestCRMIntegration:
    """Integration tests for CRM workflows"""
    
    def test_complete_sales_flow(self, client, auth_headers):
        """Test complete sales flow: contact → company → deal → close"""
        # 1. Create contact
        contact_data = {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.j@bigcorp.com",
            "position": "VP Sales"
        }
        contact_resp = client.post(
            "/api/v1/crm/contacts",
            json=contact_data,
            headers=auth_headers
        )
        assert contact_resp.status_code == 201
        contact = contact_resp.json()
        
        # 2. Create company
        company_data = {
            "name": "BigCorp Industries",
            "industry": "Manufacturing"
        }
        company_resp = client.post(
            "/api/v1/crm/companies",
            json=company_data,
            headers=auth_headers
        )
        assert company_resp.status_code == 201
        company = company_resp.json()
        
        # 3. Create deal
        deal_data = {
            "title": "Annual Contract",
            "amount": 100000.00,
            "currency": "USD",
            "stage": "proposal",
            "contact_id": contact["id"],
            "company_id": company["id"]
        }
        deal_resp = client.post(
            "/api/v1/crm/deals",
            json=deal_data,
            headers=auth_headers
        )
        assert deal_resp.status_code == 201
        deal = deal_resp.json()
        
        # 4. Move through stages
        stages = ["negotiation", "closed_won"]
        for stage in stages:
            update_resp = client.put(
                f"/api/v1/crm/deals/{deal['id']}",
                json={"stage": stage},
                headers=auth_headers
            )
            assert update_resp.status_code == 200
        
        # 5. Verify final state
        final_deal = client.get(
            f"/api/v1/crm/deals/{deal['id']}",
            headers=auth_headers
        ).json()
        assert final_deal["stage"] == "closed_won"
    
    def test_unauthorized_access(self, client):
        """Test that CRM routes require authentication"""
        endpoints = [
            "/api/v1/crm/contacts",
            "/api/v1/crm/companies",
            "/api/v1/crm/deals",
            "/api/v1/crm/pipelines"
        ]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 401


# Fixtures
@pytest.fixture
def sample_contact(client, auth_headers):
    """Create and return a sample contact"""
    contact_data = {
        "first_name": "Test",
        "last_name": "Contact",
        "email": "test.contact@example.com"
    }
    response = client.post(
        "/api/v1/crm/contacts",
        json=contact_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_company(client, auth_headers):
    """Create and return a sample company"""
    company_data = {
        "name": "Test Company Ltd",
        "industry": "Testing"
    }
    response = client.post(
        "/api/v1/crm/companies",
        json=company_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_deal(client, auth_headers, sample_contact, sample_company):
    """Create and return a sample deal"""
    deal_data = {
        "title": "Test Deal",
        "amount": 10000.00,
        "currency": "USD",
        "stage": "proposal",
        "contact_id": sample_contact["id"],
        "company_id": sample_company["id"]
    }
    response = client.post(
        "/api/v1/crm/deals",
        json=deal_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def sample_pipeline(client, auth_headers):
    """Create and return a sample pipeline"""
    pipeline_data = {
        "name": "Test Pipeline",
        "stages": [
            {"name": "Stage 1", "order": 1},
            {"name": "Stage 2", "order": 2}
        ]
    }
    response = client.post(
        "/api/v1/crm/pipelines",
        json=pipeline_data,
        headers=auth_headers
    )
    return response.json()


@pytest.fixture
def multiple_contacts(client, auth_headers):
    """Create multiple test contacts"""
    contacts = []
    for i in range(10):
        contact_data = {
            "first_name": f"Contact{i}",
            "last_name": f"Test{i}",
            "email": f"contact{i}@example.com",
            "company": "Acme Corp" if i % 2 == 0 else "Other Corp"
        }
        response = client.post(
            "/api/v1/crm/contacts",
            json=contact_data,
            headers=auth_headers
        )
        contacts.append(response.json())
    return contacts


@pytest.fixture
def multiple_deals(client, auth_headers, sample_contact, sample_company):
    """Create multiple test deals"""
    deals = []
    stages = ["lead", "proposal", "negotiation"]
    for i, stage in enumerate(stages):
        deal_data = {
            "title": f"Deal {i}",
            "amount": 1000.00 * (i + 1),
            "currency": "USD",
            "stage": stage,
            "contact_id": sample_contact["id"],
            "company_id": sample_company["id"]
        }
        response = client.post(
            "/api/v1/crm/deals",
            json=deal_data,
            headers=auth_headers
        )
        deals.append(response.json())
    return deals
