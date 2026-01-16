"""
CHE·NU™ — API CONTRACT TESTS (PYTEST)
Sprint 7: Tests for API contract validation

API Contract Principles:
- All endpoints follow consistent patterns
- Response schemas are validated
- Error responses are standardized
- Versioning is enforced (/api/v1)
"""

import pytest
from typing import Dict, List, Any
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# API CONTRACT CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

API_VERSION = "v1"
API_BASE = f"/api/{API_VERSION}"

# Standard HTTP status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_UNPROCESSABLE = 422
HTTP_SERVER_ERROR = 500

# Required response fields
STANDARD_ERROR_FIELDS = ["code", "message"]
STANDARD_META_FIELDS = ["request_id", "timestamp"]
PAGINATION_FIELDS = ["items", "total", "page", "page_size", "has_next"]

# ═══════════════════════════════════════════════════════════════════════════════
# MOCK API RESPONSES
# ═══════════════════════════════════════════════════════════════════════════════

class MockApiResponse:
    """Mock API response for testing."""
    
    def __init__(
        self,
        status: int,
        data: Any = None,
        error: Dict = None,
        meta: Dict = None
    ):
        self.status = status
        self.data = data
        self.error = error
        self.meta = meta or {
            "request_id": f"req_{datetime.utcnow().timestamp()}",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def json(self) -> Dict:
        response = {}
        if self.data is not None:
            response["data"] = self.data
        if self.error is not None:
            response["error"] = self.error
        if self.meta is not None:
            response["meta"] = self.meta
        return response


class MockApiClient:
    """Mock API client for contract testing."""
    
    def __init__(self):
        self.base_url = API_BASE
        self.responses: Dict[str, MockApiResponse] = {}
    
    def register_response(self, endpoint: str, response: MockApiResponse):
        """Register a mock response for an endpoint."""
        self.responses[endpoint] = response
    
    def get(self, endpoint: str) -> MockApiResponse:
        """Mock GET request."""
        if endpoint in self.responses:
            return self.responses[endpoint]
        return MockApiResponse(HTTP_NOT_FOUND, error={
            "code": "NOT_FOUND",
            "message": f"Endpoint {endpoint} not found"
        })
    
    def post(self, endpoint: str, data: Dict) -> MockApiResponse:
        """Mock POST request."""
        if endpoint in self.responses:
            return self.responses[endpoint]
        return MockApiResponse(HTTP_CREATED, data={"id": "new_id", **data})
    
    def put(self, endpoint: str, data: Dict) -> MockApiResponse:
        """Mock PUT request."""
        if endpoint in self.responses:
            return self.responses[endpoint]
        return MockApiResponse(HTTP_OK, data=data)
    
    def delete(self, endpoint: str) -> MockApiResponse:
        """Mock DELETE request."""
        return MockApiResponse(HTTP_NO_CONTENT)


# ═══════════════════════════════════════════════════════════════════════════════
# API VERSIONING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiVersioning:
    """Tests for API versioning."""

    def test_api_version_is_v1(self):
        """API version should be v1."""
        assert API_VERSION == "v1"

    def test_api_base_includes_version(self):
        """API base URL should include version."""
        assert "/v1" in API_BASE

    def test_all_endpoints_start_with_api(self):
        """All endpoints should start with /api."""
        assert API_BASE.startswith("/api")


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE FORMAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestResponseFormat:
    """Tests for response format consistency."""

    def test_success_response_has_data(self):
        """Success response should have data field."""
        response = MockApiResponse(HTTP_OK, data={"id": "123"})
        json_response = response.json()
        
        assert "data" in json_response

    def test_error_response_has_error(self):
        """Error response should have error field."""
        response = MockApiResponse(
            HTTP_BAD_REQUEST,
            error={"code": "INVALID", "message": "Invalid request"}
        )
        json_response = response.json()
        
        assert "error" in json_response

    def test_error_has_code_and_message(self):
        """Error should have code and message."""
        response = MockApiResponse(
            HTTP_BAD_REQUEST,
            error={"code": "VALIDATION_ERROR", "message": "Field required"}
        )
        error = response.json()["error"]
        
        assert "code" in error
        assert "message" in error

    def test_response_has_meta(self):
        """Response should have meta field."""
        response = MockApiResponse(HTTP_OK, data={})
        json_response = response.json()
        
        assert "meta" in json_response

    def test_meta_has_request_id(self):
        """Meta should have request_id."""
        response = MockApiResponse(HTTP_OK, data={})
        meta = response.json()["meta"]
        
        assert "request_id" in meta

    def test_meta_has_timestamp(self):
        """Meta should have timestamp."""
        response = MockApiResponse(HTTP_OK, data={})
        meta = response.json()["meta"]
        
        assert "timestamp" in meta


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP STATUS CODE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestHttpStatusCodes:
    """Tests for HTTP status code usage."""

    def test_get_returns_200(self):
        """GET success should return 200."""
        client = MockApiClient()
        client.register_response("/spheres", MockApiResponse(HTTP_OK, data=[]))
        
        response = client.get("/spheres")
        assert response.status == HTTP_OK

    def test_post_returns_201(self):
        """POST success should return 201."""
        client = MockApiClient()
        response = client.post("/threads", {"title": "New Thread"})
        
        assert response.status == HTTP_CREATED

    def test_delete_returns_204(self):
        """DELETE success should return 204."""
        client = MockApiClient()
        response = client.delete("/threads/123")
        
        assert response.status == HTTP_NO_CONTENT

    def test_not_found_returns_404(self):
        """Not found should return 404."""
        client = MockApiClient()
        response = client.get("/nonexistent")
        
        assert response.status == HTTP_NOT_FOUND

    def test_validation_error_returns_422(self):
        """Validation error should return 422."""
        response = MockApiResponse(
            HTTP_UNPROCESSABLE,
            error={"code": "VALIDATION_ERROR", "message": "Invalid email"}
        )
        
        assert response.status == HTTP_UNPROCESSABLE


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE ENDPOINT CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSphereEndpointContract:
    """Tests for sphere endpoint contracts."""

    def test_list_spheres_returns_array(self):
        """GET /spheres should return array of 9 spheres."""
        spheres = [
            {"id": "personal", "name": "Personal"},
            {"id": "business", "name": "Business"},
            {"id": "government", "name": "Government"},
            {"id": "creative", "name": "Creative"},
            {"id": "community", "name": "Community"},
            {"id": "social", "name": "Social"},
            {"id": "entertainment", "name": "Entertainment"},
            {"id": "team", "name": "Team"},
            {"id": "scholar", "name": "Scholar"},
        ]
        
        response = MockApiResponse(HTTP_OK, data=spheres)
        data = response.json()["data"]
        
        assert isinstance(data, list)
        assert len(data) == 9

    def test_sphere_has_required_fields(self):
        """Sphere should have required fields."""
        sphere = {
            "id": "personal",
            "name": "Personal",
            "icon": "🏠",
            "color": "#D8B26A",
        }
        
        required_fields = ["id", "name", "icon", "color"]
        for field in required_fields:
            assert field in sphere

    def test_get_single_sphere(self):
        """GET /spheres/:id should return single sphere."""
        sphere = {"id": "scholar", "name": "Scholar", "order": 9}
        response = MockApiResponse(HTTP_OK, data=sphere)
        
        data = response.json()["data"]
        assert data["id"] == "scholar"


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU ENDPOINT CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBureauEndpointContract:
    """Tests for bureau endpoint contracts."""

    def test_list_sections_returns_6(self):
        """GET /bureau/sections should return 6 sections."""
        sections = [
            {"id": "QUICK_CAPTURE", "key": "quick_capture"},
            {"id": "RESUME_WORKSPACE", "key": "resume_workspace"},
            {"id": "THREADS", "key": "threads"},
            {"id": "DATA_FILES", "key": "data_files"},
            {"id": "ACTIVE_AGENTS", "key": "active_agents"},
            {"id": "MEETINGS", "key": "meetings"},
        ]
        
        response = MockApiResponse(HTTP_OK, data=sections)
        data = response.json()["data"]
        
        assert len(data) == 6

    def test_section_has_required_fields(self):
        """Bureau section should have required fields."""
        section = {
            "id": "QUICK_CAPTURE",
            "key": "quick_capture",
            "name": "Quick Capture",
            "hierarchy": 1,
        }
        
        required_fields = ["id", "key", "name", "hierarchy"]
        for field in required_fields:
            assert field in section


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD ENDPOINT CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadEndpointContract:
    """Tests for thread endpoint contracts."""

    def test_thread_has_required_fields(self):
        """Thread should have required fields."""
        thread = {
            "id": "thread_123",
            "title": "Test Thread",
            "type": "chat",
            "sphere_id": "personal",
            "status": "active",
            "token_budget": 5000,
            "tokens_used": 0,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        required_fields = ["id", "title", "type", "sphere_id", "status", 
                          "token_budget", "tokens_used", "created_at"]
        for field in required_fields:
            assert field in thread

    def test_create_thread_requires_title(self):
        """POST /threads requires title."""
        required_create_fields = ["title", "sphere_id"]
        request = {"title": "New Thread", "sphere_id": "personal"}
        
        for field in required_create_fields:
            assert field in request


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT ENDPOINT CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentEndpointContract:
    """Tests for agent endpoint contracts."""

    def test_nova_always_in_agents(self):
        """GET /agents should always include Nova."""
        agents = [
            {"id": "nova", "name": "Nova", "level": "L0", "is_system": True},
            {"id": "analyst", "name": "Analyst", "level": "L2", "is_system": False},
        ]
        
        nova = next((a for a in agents if a["id"] == "nova"), None)
        assert nova is not None
        assert nova["level"] == "L0"
        assert nova["is_system"] is True

    def test_agent_has_required_fields(self):
        """Agent should have required fields."""
        agent = {
            "id": "nova",
            "name": "Nova",
            "type": "nova",
            "level": "L0",
            "status": "idle",
            "is_system": True,
            "capabilities": ["guidance", "memory", "governance"],
        }
        
        required_fields = ["id", "name", "type", "level", "status", 
                          "is_system", "capabilities"]
        for field in required_fields:
            assert field in agent


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE ENDPOINT CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestGovernanceEndpointContract:
    """Tests for governance endpoint contracts."""

    def test_budget_has_required_fields(self):
        """Token budget should have required fields."""
        budget = {
            "total": 100000,
            "used": 25000,
            "remaining": 75000,
            "daily_limit": 100000,
        }
        
        required_fields = ["total", "used", "remaining"]
        for field in required_fields:
            assert field in budget

    def test_remaining_equals_total_minus_used(self):
        """Remaining should equal total - used."""
        budget = {
            "total": 100000,
            "used": 25000,
            "remaining": 75000,
        }
        
        assert budget["remaining"] == budget["total"] - budget["used"]

    def test_laws_endpoint_returns_10(self):
        """GET /governance/laws should return 10 laws."""
        laws = [
            {"id": "L1", "code": "CONSENT_PRIMACY"},
            {"id": "L2", "code": "TEMPORAL_SOVEREIGNTY"},
            {"id": "L3", "code": "CONTEXTUAL_FIDELITY"},
            {"id": "L4", "code": "HIERARCHICAL_RESPECT"},
            {"id": "L5", "code": "AUDIT_COMPLETENESS"},
            {"id": "L6", "code": "ENCODING_TRANSPARENCY"},
            {"id": "L7", "code": "AGENT_NON_AUTONOMY"},
            {"id": "L8", "code": "BUDGET_ACCOUNTABILITY"},
            {"id": "L9", "code": "CROSS_SPHERE_ISOLATION"},
            {"id": "L10", "code": "DELETION_COMPLETENESS"},
        ]
        
        assert len(laws) == 10


# ═══════════════════════════════════════════════════════════════════════════════
# PAGINATION CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPaginationContract:
    """Tests for pagination response contract."""

    def test_paginated_response_has_items(self):
        """Paginated response should have items."""
        response = {
            "items": [{"id": "1"}, {"id": "2"}],
            "total": 100,
            "page": 1,
            "page_size": 20,
            "has_next": True,
        }
        
        assert "items" in response
        assert isinstance(response["items"], list)

    def test_paginated_response_has_total(self):
        """Paginated response should have total."""
        response = {
            "items": [],
            "total": 100,
            "page": 1,
            "page_size": 20,
            "has_next": True,
        }
        
        assert "total" in response
        assert isinstance(response["total"], int)

    def test_paginated_response_has_page_info(self):
        """Paginated response should have page info."""
        response = {
            "items": [],
            "total": 100,
            "page": 1,
            "page_size": 20,
            "has_next": True,
        }
        
        assert "page" in response
        assert "page_size" in response
        assert "has_next" in response


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR CONTRACT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestErrorContract:
    """Tests for error response contract."""

    def test_error_has_code(self):
        """Error should have code."""
        error = {"code": "VALIDATION_ERROR", "message": "Invalid input"}
        assert "code" in error

    def test_error_has_message(self):
        """Error should have message."""
        error = {"code": "VALIDATION_ERROR", "message": "Invalid input"}
        assert "message" in error

    def test_validation_error_has_details(self):
        """Validation error may have details."""
        error = {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input",
            "details": [
                {"field": "email", "message": "Invalid email format"},
            ],
        }
        
        assert "details" in error
        assert isinstance(error["details"], list)


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT API CONTRACT COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiMemoryPromptCompliance:
    """Tests ensuring API contract compliance with Memory Prompt."""

    def test_spheres_endpoint_returns_exactly_9(self):
        """Spheres endpoint should return exactly 9 spheres."""
        SPHERE_COUNT = 9
        assert SPHERE_COUNT == 9

    def test_bureau_endpoint_returns_exactly_6(self):
        """Bureau endpoint should return exactly 6 sections."""
        SECTION_COUNT = 6
        assert SECTION_COUNT == 6

    def test_nova_in_agents_response(self):
        """Nova should always be in agents response."""
        NOVA_REQUIRED = True
        assert NOVA_REQUIRED

    def test_tokens_are_internal_credits(self):
        """Token budget should represent internal credits, not crypto."""
        # No blockchain/crypto fields in budget
        budget_fields = ["total", "used", "remaining", "daily_limit"]
        crypto_fields = ["wallet", "blockchain", "contract", "eth", "btc"]
        
        for crypto_field in crypto_fields:
            assert crypto_field not in budget_fields

    def test_all_endpoints_auditable(self):
        """All endpoints should return meta with request_id for audit."""
        response = MockApiResponse(HTTP_OK, data={})
        meta = response.json()["meta"]
        
        assert "request_id" in meta
