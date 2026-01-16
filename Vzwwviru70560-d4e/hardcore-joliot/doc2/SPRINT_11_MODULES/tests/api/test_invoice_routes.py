"""
CHE·NU™ - Invoice Routes Tests
"""
import pytest
from datetime import datetime, timedelta


class TestInvoices:
    """Invoice CRUD operations"""
    
    def test_create_invoice(self, client, auth_headers, sample_deal):
        """Test creating invoice"""
        data = {
            "deal_id": sample_deal["id"],
            "items": [
                {"description": "License", "quantity": 1, "unit_price": 50000.00}
            ],
            "due_days": 30,
            "notes": "Net 30 payment terms"
        }
        resp = client.post("/api/v1/invoices", json=data, headers=auth_headers)
        assert resp.status_code == 201
        invoice = resp.json()
        assert invoice["total"] == 50000.00
        assert "invoice_number" in invoice
    
    def test_list_invoices(self, client, auth_headers, multiple_invoices):
        """Test listing invoices"""
        resp = client.get("/api/v1/invoices", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert len(data["items"]) > 0
    
    def test_get_invoice(self, client, auth_headers, sample_invoice):
        """Test get invoice by ID"""
        resp = client.get(f"/api/v1/invoices/{sample_invoice['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == sample_invoice["id"]
    
    def test_update_invoice(self, client, auth_headers, sample_invoice):
        """Test updating invoice"""
        update = {"notes": "Updated payment terms"}
        resp = client.put(f"/api/v1/invoices/{sample_invoice['id']}", json=update, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["notes"] == "Updated payment terms"
    
    def test_send_invoice(self, client, auth_headers, sample_invoice):
        """Test sending invoice via email"""
        data = {"recipient": "client@example.com"}
        resp = client.post(f"/api/v1/invoices/{sample_invoice['id']}/send", json=data, headers=auth_headers)
        assert resp.status_code == 200
        assert "sent_at" in resp.json()
    
    def test_process_payment(self, client, auth_headers, sample_invoice):
        """Test processing payment"""
        payment = {
            "amount": sample_invoice["total"],
            "method": "bank_transfer",
            "reference": "REF123"
        }
        resp = client.post(f"/api/v1/invoices/{sample_invoice['id']}/payment", json=payment, headers=auth_headers)
        assert resp.status_code == 200
        invoice = resp.json()
        assert invoice["status"] == "paid"
    
    def test_filter_overdue(self, client, auth_headers, overdue_invoice):
        """Test filtering overdue invoices"""
        resp = client.get("/api/v1/invoices?status=overdue", headers=auth_headers)
        assert resp.status_code == 200
        for inv in resp.json()["items"]:
            assert inv["status"] == "overdue"


class TestInvoiceTemplates:
    """Invoice templates"""
    
    def test_list_templates(self, client, auth_headers):
        """Test listing templates"""
        resp = client.get("/api/v1/invoice-templates", headers=auth_headers)
        assert resp.status_code == 200
        assert "items" in resp.json()
    
    def test_create_template(self, client, auth_headers):
        """Test creating template"""
        data = {
            "name": "Standard Invoice",
            "items": [{"description": "Service", "unit_price": 1000.00}]
        }
        resp = client.post("/api/v1/invoice-templates", json=data, headers=auth_headers)
        assert resp.status_code == 201


@pytest.fixture
def sample_invoice(client, auth_headers):
    data = {
        "items": [{"description": "Test", "quantity": 1, "unit_price": 1000.00}],
        "due_days": 30
    }
    return client.post("/api/v1/invoices", json=data, headers=auth_headers).json()

@pytest.fixture
def overdue_invoice(client, auth_headers):
    data = {
        "items": [{"description": "Test", "quantity": 1, "unit_price": 500.00}],
        "due_date": (datetime.now() - timedelta(days=10)).isoformat(),
        "status": "sent"
    }
    return client.post("/api/v1/invoices", json=data, headers=auth_headers).json()

@pytest.fixture
def multiple_invoices(client, auth_headers):
    invoices = []
    for i in range(5):
        data = {
            "items": [{"description": f"Item {i}", "quantity": 1, "unit_price": 100.00 * i}],
            "due_days": 30
        }
        invoices.append(client.post("/api/v1/invoices", json=data, headers=auth_headers).json())
    return invoices
