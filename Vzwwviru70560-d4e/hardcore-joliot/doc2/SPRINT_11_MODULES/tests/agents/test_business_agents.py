"""
CHE·NU™ - Business Agents Tests
Tests for CRM Assistant and Invoice Manager (L3 Agents)
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import json


class TestCRMAssistant:
    """Test suite for CRM Assistant agent"""
    
    def test_agent_initialization(self, crm_assistant):
        """Test CRM Assistant initializes correctly"""
        assert crm_assistant.agent_id == "business.crm_assistant"
        assert crm_assistant.level == "L3"
        assert crm_assistant.sphere == "business"
        assert len(crm_assistant.capabilities) == 10
    
    def test_capability_create_contact(self, crm_assistant, mock_db_session):
        """Test create_contact capability"""
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "company": "Acme Corp"
        }
        
        result = crm_assistant.execute_capability(
            "create_contact",
            contact_data,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert result["contact"]["email"] == "john@example.com"
        assert "id" in result["contact"]
    
    def test_capability_search_contacts(self, crm_assistant, mock_db_session, sample_contacts):
        """Test search_contacts capability"""
        search_params = {
            "query": "john",
            "filters": {"company": "Acme"}
        }
        
        result = crm_assistant.execute_capability(
            "search_contacts",
            search_params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert len(result["contacts"]) > 0
        assert all("john" in c["first_name"].lower() for c in result["contacts"])
    
    def test_capability_update_deal_stage(self, crm_assistant, mock_db_session, sample_deal):
        """Test update_deal_stage capability"""
        update_params = {
            "deal_id": sample_deal["id"],
            "new_stage": "negotiation",
            "notes": "Moving to negotiation phase"
        }
        
        result = crm_assistant.execute_capability(
            "update_deal_stage",
            update_params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert result["deal"]["stage"] == "negotiation"
        assert result["stage_changed"] is True
    
    def test_capability_analyze_pipeline(self, crm_assistant, mock_db_session, multiple_deals):
        """Test analyze_pipeline capability"""
        params = {"pipeline_id": 1}
        
        result = crm_assistant.execute_capability(
            "analyze_pipeline",
            params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert "total_value" in result["analysis"]
        assert "conversion_rate" in result["analysis"]
        assert "average_deal_size" in result["analysis"]
        assert "deals_by_stage" in result["analysis"]
    
    def test_capability_suggest_next_action(self, crm_assistant, mock_db_session, sample_deal):
        """Test AI-powered suggest_next_action capability"""
        params = {"deal_id": sample_deal["id"]}
        
        with patch('backend.agents.business.crm_assistant.ai_service') as mock_ai:
            mock_ai.generate.return_value = {
                "suggested_action": "Schedule follow-up call",
                "reasoning": "Deal in proposal stage for 5 days",
                "priority": "high"
            }
            
            result = crm_assistant.execute_capability(
                "suggest_next_action",
                params,
                session=mock_db_session
            )
            
            assert result["success"] is True
            assert "suggested_action" in result
            assert result["priority"] in ["low", "medium", "high"]
    
    def test_capability_generate_email(self, crm_assistant, sample_contact):
        """Test generate_email capability"""
        params = {
            "contact_id": sample_contact["id"],
            "template": "follow_up",
            "context": {
                "last_interaction": "demo_completed",
                "product": "CHE·NU Enterprise"
            }
        }
        
        with patch('backend.agents.business.crm_assistant.ai_service') as mock_ai:
            mock_ai.generate.return_value = {
                "subject": "Following up on CHE·NU Demo",
                "body": "Hi John,\n\nThank you for attending our demo...",
                "tone": "professional"
            }
            
            result = crm_assistant.execute_capability(
                "generate_email",
                params
            )
            
            assert result["success"] is True
            assert "subject" in result["email"]
            assert "body" in result["email"]
            assert len(result["email"]["body"]) > 50
    
    def test_token_consumption_tracking(self, crm_assistant):
        """Test that agent tracks token consumption"""
        initial_tokens = crm_assistant.tokens_consumed
        
        # Execute capability that uses AI
        with patch('backend.agents.business.crm_assistant.ai_service') as mock_ai:
            mock_ai.generate.return_value = {"text": "Generated content"}
            mock_ai.tokens_used = 150
            
            result = crm_assistant.execute_capability(
                "suggest_next_action",
                {"deal_id": 1}
            )
            
            assert crm_assistant.tokens_consumed > initial_tokens
            assert crm_assistant.tokens_consumed == initial_tokens + 150
    
    def test_governance_check_before_execution(self, crm_assistant):
        """Test governance check before capability execution"""
        params = {
            "deal_id": 1,
            "budget_remaining": 0  # No budget
        }
        
        with pytest.raises(Exception) as exc:
            crm_assistant.execute_capability(
                "suggest_next_action",
                params,
                check_governance=True
            )
        
        assert "insufficient budget" in str(exc.value).lower()
    
    def test_agent_manifest(self, crm_assistant):
        """Test agent manifest is complete"""
        manifest = crm_assistant.get_manifest()
        
        assert manifest["agent_id"] == "business.crm_assistant"
        assert manifest["level"] == "L3"
        assert manifest["sphere"] == "business"
        assert "capabilities" in manifest
        assert "permissions" in manifest
        assert "token_costs" in manifest
        
        # Verify all 10 capabilities present
        assert len(manifest["capabilities"]) == 10
        expected_caps = [
            "create_contact",
            "search_contacts",
            "update_contact",
            "create_deal",
            "update_deal_stage",
            "analyze_pipeline",
            "suggest_next_action",
            "generate_email",
            "schedule_follow_up",
            "export_contacts"
        ]
        for cap in expected_caps:
            assert cap in manifest["capabilities"]


class TestInvoiceManager:
    """Test suite for Invoice Manager agent"""
    
    def test_agent_initialization(self, invoice_manager):
        """Test Invoice Manager initializes correctly"""
        assert invoice_manager.agent_id == "business.invoice_manager"
        assert invoice_manager.level == "L3"
        assert invoice_manager.sphere == "business"
        assert len(invoice_manager.capabilities) == 8
    
    def test_capability_generate_invoice(self, invoice_manager, mock_db_session, sample_deal):
        """Test generate_invoice capability"""
        invoice_params = {
            "deal_id": sample_deal["id"],
            "items": [
                {"description": "CHE·NU Enterprise License", "quantity": 1, "unit_price": 50000.00}
            ],
            "due_days": 30
        }
        
        result = invoice_manager.execute_capability(
            "generate_invoice",
            invoice_params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert result["invoice"]["total"] == 50000.00
        assert "invoice_number" in result["invoice"]
        assert "pdf_url" in result["invoice"]
    
    def test_capability_send_invoice(self, invoice_manager, sample_invoice):
        """Test send_invoice capability"""
        send_params = {
            "invoice_id": sample_invoice["id"],
            "recipient_email": "client@example.com",
            "cc": ["accounting@example.com"]
        }
        
        with patch('backend.agents.business.invoice_manager.email_service') as mock_email:
            mock_email.send.return_value = {"success": True, "message_id": "msg_123"}
            
            result = invoice_manager.execute_capability(
                "send_invoice",
                send_params
            )
            
            assert result["success"] is True
            assert "sent_at" in result
            assert mock_email.send.called
    
    def test_capability_process_payment(self, invoice_manager, mock_db_session, sample_invoice):
        """Test process_payment capability"""
        payment_params = {
            "invoice_id": sample_invoice["id"],
            "amount": 50000.00,
            "payment_method": "bank_transfer",
            "reference": "REF123456"
        }
        
        result = invoice_manager.execute_capability(
            "process_payment",
            payment_params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert result["invoice"]["status"] == "paid"
        assert result["invoice"]["paid_at"] is not None
        assert result["payment"]["amount"] == 50000.00
    
    def test_capability_send_reminder(self, invoice_manager, overdue_invoice):
        """Test send_reminder capability"""
        reminder_params = {
            "invoice_id": overdue_invoice["id"],
            "reminder_type": "polite"
        }
        
        with patch('backend.agents.business.invoice_manager.email_service') as mock_email:
            with patch('backend.agents.business.invoice_manager.ai_service') as mock_ai:
                mock_ai.generate.return_value = {
                    "subject": "Friendly Reminder: Invoice Due",
                    "body": "We wanted to remind you about invoice..."
                }
                mock_email.send.return_value = {"success": True}
                
                result = invoice_manager.execute_capability(
                    "send_reminder",
                    reminder_params
                )
                
                assert result["success"] is True
                assert "reminder_sent_at" in result
    
    def test_capability_generate_report(self, invoice_manager, mock_db_session, multiple_invoices):
        """Test generate_report capability"""
        report_params = {
            "period": "Q1_2024",
            "format": "summary"
        }
        
        result = invoice_manager.execute_capability(
            "generate_report",
            report_params,
            session=mock_db_session
        )
        
        assert result["success"] is True
        assert "total_invoiced" in result["report"]
        assert "total_paid" in result["report"]
        assert "total_outstanding" in result["report"]
        assert "invoice_count" in result["report"]
    
    def test_capability_calculate_taxes(self, invoice_manager):
        """Test calculate_taxes capability"""
        tax_params = {
            "amount": 10000.00,
            "region": "CA",  # California
            "tax_type": "sales_tax"
        }
        
        result = invoice_manager.execute_capability(
            "calculate_taxes",
            tax_params
        )
        
        assert result["success"] is True
        assert "tax_amount" in result
        assert "tax_rate" in result
        assert "total_with_tax" in result
        assert result["total_with_tax"] > tax_params["amount"]
    
    def test_integration_stripe_payment(self, invoice_manager, sample_invoice):
        """Test Stripe integration for payment processing"""
        payment_params = {
            "invoice_id": sample_invoice["id"],
            "amount": 50000.00,
            "payment_method": "stripe",
            "stripe_token": "tok_test_123"
        }
        
        with patch('backend.agents.business.invoice_manager.stripe') as mock_stripe:
            mock_stripe.PaymentIntent.create.return_value = {
                "id": "pi_123",
                "status": "succeeded"
            }
            
            result = invoice_manager.execute_capability(
                "process_payment",
                payment_params
            )
            
            assert result["success"] is True
            assert "payment_intent_id" in result["payment"]
    
    def test_pdf_generation(self, invoice_manager, sample_invoice):
        """Test PDF invoice generation"""
        params = {"invoice_id": sample_invoice["id"]}
        
        with patch('backend.agents.business.invoice_manager.pdf_service') as mock_pdf:
            mock_pdf.generate.return_value = {
                "pdf_url": "https://storage.chenu.com/invoices/INV-001.pdf",
                "pdf_size": 125000
            }
            
            result = invoice_manager.execute_capability(
                "generate_pdf",
                params
            )
            
            assert result["success"] is True
            assert result["pdf"]["url"].endswith(".pdf")
    
    def test_agent_manifest(self, invoice_manager):
        """Test Invoice Manager manifest"""
        manifest = invoice_manager.get_manifest()
        
        assert manifest["agent_id"] == "business.invoice_manager"
        assert len(manifest["capabilities"]) == 8
        
        expected_caps = [
            "generate_invoice",
            "send_invoice",
            "process_payment",
            "send_reminder",
            "generate_report",
            "calculate_taxes",
            "generate_pdf",
            "export_data"
        ]
        for cap in expected_caps:
            assert cap in manifest["capabilities"]


class TestAgentGovernance:
    """Test governance rules for agents"""
    
    def test_budget_enforcement(self, crm_assistant):
        """Test budget is enforced before execution"""
        # Set low budget
        crm_assistant.budget_remaining = 10  # Only 10 tokens
        
        # Try expensive operation
        with pytest.raises(Exception) as exc:
            crm_assistant.execute_capability(
                "suggest_next_action",  # Costs ~100 tokens
                {"deal_id": 1},
                check_budget=True
            )
        
        assert "budget" in str(exc.value).lower()
    
    def test_permission_check(self, crm_assistant, unauthorized_user):
        """Test permission check before execution"""
        with pytest.raises(Exception) as exc:
            crm_assistant.execute_capability(
                "export_contacts",
                {},
                user=unauthorized_user,
                check_permissions=True
            )
        
        assert "permission" in str(exc.value).lower()
    
    def test_audit_trail(self, crm_assistant, mock_db_session):
        """Test that all agent actions are audited"""
        result = crm_assistant.execute_capability(
            "create_contact",
            {"first_name": "Test", "email": "test@example.com"},
            session=mock_db_session
        )
        
        # Check audit log created
        audit_logs = mock_db_session.query(AgentAuditLog).all()
        assert len(audit_logs) > 0
        
        latest_log = audit_logs[-1]
        assert latest_log.agent_id == "business.crm_assistant"
        assert latest_log.capability == "create_contact"
        assert latest_log.tokens_consumed > 0


# Fixtures
@pytest.fixture
def crm_assistant():
    """Create CRM Assistant instance"""
    from backend.agents.business.crm_assistant import CRMAssistant
    return CRMAssistant()


@pytest.fixture
def invoice_manager():
    """Create Invoice Manager instance"""
    from backend.agents.business.invoice_manager import InvoiceManager
    return InvoiceManager()


@pytest.fixture
def sample_contacts(mock_db_session):
    """Create sample contacts"""
    contacts = []
    for i in range(5):
        contact = {
            "id": i + 1,
            "first_name": f"John{i}" if i % 2 == 0 else f"Jane{i}",
            "last_name": "Doe",
            "email": f"user{i}@example.com",
            "company": "Acme Corp"
        }
        contacts.append(contact)
    return contacts


@pytest.fixture
def sample_deal():
    """Create sample deal"""
    return {
        "id": 1,
        "title": "Enterprise License",
        "amount": 50000.00,
        "stage": "proposal"
    }


@pytest.fixture
def multiple_deals(mock_db_session):
    """Create multiple deals"""
    stages = ["lead", "proposal", "negotiation", "closed_won"]
    deals = []
    for i, stage in enumerate(stages):
        deal = {
            "id": i + 1,
            "title": f"Deal {i}",
            "amount": 10000.00 * (i + 1),
            "stage": stage
        }
        deals.append(deal)
    return deals


@pytest.fixture
def sample_invoice():
    """Create sample invoice"""
    return {
        "id": 1,
        "invoice_number": "INV-001",
        "total": 50000.00,
        "status": "sent"
    }


@pytest.fixture
def overdue_invoice():
    """Create overdue invoice"""
    from datetime import datetime, timedelta
    return {
        "id": 2,
        "invoice_number": "INV-002",
        "total": 25000.00,
        "status": "sent",
        "due_date": (datetime.now() - timedelta(days=15)).isoformat()
    }


@pytest.fixture
def multiple_invoices(mock_db_session):
    """Create multiple invoices"""
    invoices = []
    statuses = ["draft", "sent", "paid", "overdue"]
    for i, status in enumerate(statuses):
        invoice = {
            "id": i + 1,
            "invoice_number": f"INV-{i+1:03d}",
            "total": 10000.00 * (i + 1),
            "status": status
        }
        invoices.append(invoice)
    return invoices


@pytest.fixture
def unauthorized_user():
    """Create user without permissions"""
    return {
        "id": 999,
        "role": "viewer",
        "permissions": ["read_only"]
    }


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return Mock()
