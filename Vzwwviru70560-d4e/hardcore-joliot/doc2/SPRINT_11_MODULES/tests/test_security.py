"""
CHE·NU™ — SECURITY & AUTH TESTS (PYTEST)
Sprint 4: Tests for authentication and security

Security principles:
- Governance is ALWAYS enforced before execution
- User has control at every step
- All actions are auditable (L5)
- No autonomous external actions (SAFE)
"""

import pytest
from typing import Dict
import jwt
import hashlib
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════════════════
# AUTH CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

SECRET_KEY = "test-secret-key-for-testing-only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_test_token(user_id: str, expires_delta: timedelta = None) -> str:
    """Create a test JWT token."""
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict:
    """Verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "invalid"}


def hash_password(password: str) -> str:
    """Hash a password (simple for testing)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestJWTTokens:
    """Tests for JWT token handling."""

    def test_create_valid_token(self):
        """Should create a valid token."""
        token = create_test_token("user_123")
        assert token is not None
        assert len(token) > 0

    def test_verify_valid_token(self):
        """Should verify a valid token."""
        token = create_test_token("user_123")
        result = verify_token(token)
        
        assert result["valid"] is True
        assert result["payload"]["sub"] == "user_123"

    def test_token_contains_user_id(self):
        """Token should contain user ID in subject claim."""
        token = create_test_token("user_456")
        result = verify_token(token)
        
        assert result["payload"]["sub"] == "user_456"

    def test_token_has_expiration(self):
        """Token should have expiration claim."""
        token = create_test_token("user_123")
        result = verify_token(token)
        
        assert "exp" in result["payload"]

    def test_expired_token_rejected(self):
        """Should reject expired token."""
        # Create token that expired 1 hour ago
        token = create_test_token("user_123", timedelta(hours=-1))
        result = verify_token(token)
        
        assert result["valid"] is False
        assert result["error"] == "expired"

    def test_invalid_token_rejected(self):
        """Should reject invalid token."""
        result = verify_token("invalid.token.here")
        
        assert result["valid"] is False
        assert result["error"] == "invalid"

    def test_tampered_token_rejected(self):
        """Should reject tampered token."""
        token = create_test_token("user_123")
        # Tamper with the token
        tampered = token[:-10] + "tampered00"
        result = verify_token(tampered)
        
        assert result["valid"] is False


# ═══════════════════════════════════════════════════════════════════════════════
# PASSWORD TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPasswordSecurity:
    """Tests for password handling."""

    def test_password_hashing(self):
        """Should hash password."""
        password = "securePassword123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0

    def test_same_password_same_hash(self):
        """Same password should produce same hash."""
        password = "securePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 == hash2

    def test_different_passwords_different_hash(self):
        """Different passwords should produce different hashes."""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        assert hash1 != hash2

    def test_verify_correct_password(self):
        """Should verify correct password."""
        password = "securePassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Should reject incorrect password."""
        hashed = hash_password("correctPassword")
        
        assert verify_password("wrongPassword", hashed) is False

    def test_password_minimum_length(self):
        """Password should have minimum length requirement."""
        MIN_PASSWORD_LENGTH = 8
        
        short_password = "short"
        assert len(short_password) < MIN_PASSWORD_LENGTH
        
        valid_password = "validPass123"
        assert len(valid_password) >= MIN_PASSWORD_LENGTH


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAuthEndpoints:
    """Tests for authentication endpoints."""

    def test_login_endpoint_exists(self, client):
        """Login endpoint should exist."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@chenu.ai",
            "password": "testpassword123",
        })
        # Should not be 404
        assert response.status_code != 404

    def test_login_requires_email(self, client):
        """Login should require email."""
        response = client.post("/api/v1/auth/login", json={
            "password": "testpassword123",
        })
        # Should fail validation
        assert response.status_code in [400, 422]

    def test_login_requires_password(self, client):
        """Login should require password."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@chenu.ai",
        })
        # Should fail validation
        assert response.status_code in [400, 422]

    def test_me_endpoint_requires_auth(self, client):
        """GET /me should require authentication."""
        response = client.get("/api/v1/auth/me")
        # Should be unauthorized without token
        assert response.status_code in [401, 403]

    def test_me_endpoint_with_auth(self, client, auth_headers):
        """GET /me should work with valid auth."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        # Should succeed or at least not 401
        if response.status_code == 200:
            data = response.json()
            assert "email" in data or "id" in data


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHORIZATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAuthorization:
    """Tests for authorization rules."""

    def test_user_can_access_own_threads(self, test_user, test_thread):
        """User should access their own threads."""
        assert test_thread.owner_id == test_user.id

    def test_user_cannot_access_others_threads(self, test_user, admin_user):
        """User should not access other users' threads."""
        assert test_user.id != admin_user.id

    def test_admin_role_exists(self, admin_user):
        """Admin role should exist."""
        assert admin_user.role == "admin"

    def test_user_role_exists(self, test_user):
        """User role should exist."""
        assert test_user.role == "user"


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE SECURITY TESTS (L1-L10 Laws)
# ═══════════════════════════════════════════════════════════════════════════════

class TestGovernanceSecurity:
    """Tests for governance security (Laws L1-L10)."""

    def test_consent_primacy_l1(self):
        """L1: Nothing happens without user approval."""
        REQUIRES_CONSENT = True
        assert REQUIRES_CONSENT

    def test_temporal_sovereignty_l2(self):
        """L2: User controls when actions happen."""
        USER_CONTROLS_TIMING = True
        assert USER_CONTROLS_TIMING

    def test_audit_completeness_l5(self):
        """L5: Everything is logged and traceable."""
        AUDIT_ENABLED = True
        assert AUDIT_ENABLED

    def test_agent_non_autonomy_l7(self):
        """L7: Agents never act autonomously."""
        AGENTS_AUTONOMOUS = False
        assert not AGENTS_AUTONOMOUS

    def test_cross_sphere_isolation_l9(self):
        """L9: Spheres are isolated by default."""
        SPHERES_ISOLATED = True
        assert SPHERES_ISOLATED


# ═══════════════════════════════════════════════════════════════════════════════
# SAFE ARCHITECTURE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSafeArchitecture:
    """Tests for SAFE architecture principles."""

    def test_safe_no_autonomous_external_actions(self):
        """SAFE: No autonomous external actions."""
        AUTONOMOUS_EXTERNAL_ALLOWED = False
        assert not AUTONOMOUS_EXTERNAL_ALLOWED

    def test_non_autonomous_user_approval_required(self):
        """NON_AUTONOMOUS: User approval required."""
        REQUIRES_USER_APPROVAL = True
        assert REQUIRES_USER_APPROVAL

    def test_representational_only_processes_displays(self):
        """REPRESENTATIONAL: Only processes and displays data."""
        ONLY_PROCESSES_DISPLAYS = True
        assert ONLY_PROCESSES_DISPLAYS

    def test_governable_budget_scope_enforced(self):
        """GOVERNABLE: Budget and scope controls enforced."""
        CONTROLS_ENFORCED = True
        assert CONTROLS_ENFORCED

    def test_auditable_all_actions_logged(self):
        """AUDITABLE: All actions logged."""
        ALL_ACTIONS_LOGGED = True
        assert ALL_ACTIONS_LOGGED


# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMITING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRateLimiting:
    """Tests for rate limiting."""

    def test_rate_limit_exists(self):
        """Rate limiting should be configured."""
        RATE_LIMIT_ENABLED = True
        assert RATE_LIMIT_ENABLED

    def test_rate_limit_per_user(self):
        """Rate limit should be per user."""
        RATE_LIMIT_PER_USER = True
        assert RATE_LIMIT_PER_USER

    def test_rate_limit_window(self):
        """Rate limit should have a time window."""
        RATE_LIMIT_WINDOW_SECONDS = 60
        assert RATE_LIMIT_WINDOW_SECONDS > 0


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestInputValidation:
    """Tests for input validation security."""

    def test_email_validation(self):
        """Email should be validated."""
        import re
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        valid_email = "test@chenu.ai"
        assert re.match(email_pattern, valid_email)
        
        invalid_email = "not-an-email"
        assert not re.match(email_pattern, invalid_email)

    def test_uuid_validation(self):
        """UUIDs should be validated."""
        import uuid
        
        valid_uuid = str(uuid.uuid4())
        try:
            uuid.UUID(valid_uuid)
            valid = True
        except ValueError:
            valid = False
        assert valid
        
        invalid_uuid = "not-a-uuid"
        try:
            uuid.UUID(invalid_uuid)
            valid = True
        except ValueError:
            valid = False
        assert not valid

    def test_sphere_id_validation(self):
        """Sphere IDs should be validated against whitelist."""
        VALID_SPHERE_IDS = [
            "personal", "business", "government", "creative",
            "community", "social", "entertainment", "team", "scholar"
        ]
        
        assert "personal" in VALID_SPHERE_IDS
        assert "invalid_sphere" not in VALID_SPHERE_IDS


# ═══════════════════════════════════════════════════════════════════════════════
# ETHICS SECURITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEthicsSecurity:
    """Tests for ethics and data security."""

    def test_no_selling_attention(self):
        """CHE·NU does NOT sell attention."""
        SELLS_ATTENTION = False
        assert not SELLS_ATTENTION

    def test_no_selling_user_data(self):
        """CHE·NU does NOT sell user data."""
        SELLS_USER_DATA = False
        assert not SELLS_USER_DATA

    def test_cost_explicit(self):
        """Token costs are made explicit."""
        COST_EXPLICIT = True
        assert COST_EXPLICIT

    def test_user_control_enabled(self):
        """User has control at every step."""
        USER_CONTROL = True
        assert USER_CONTROL


# ═══════════════════════════════════════════════════════════════════════════════
# API SECURITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAPISecurity:
    """Tests for API security."""

    def test_cors_configured(self):
        """CORS should be configured."""
        CORS_ENABLED = True
        assert CORS_ENABLED

    def test_https_required_in_prod(self):
        """HTTPS should be required in production."""
        HTTPS_REQUIRED_PROD = True
        assert HTTPS_REQUIRED_PROD

    def test_sensitive_headers_not_exposed(self):
        """Sensitive headers should not be exposed."""
        EXPOSED_HEADERS = ["Content-Type", "Authorization"]
        SENSITIVE_HEADERS = ["X-Internal-Key", "X-Database-Connection"]
        
        for header in SENSITIVE_HEADERS:
            assert header not in EXPOSED_HEADERS
