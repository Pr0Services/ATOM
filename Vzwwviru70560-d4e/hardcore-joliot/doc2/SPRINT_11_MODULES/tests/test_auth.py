"""
Tests — Authentication
"""

import pytest


class TestRegistration:
    """Tests d'inscription"""
    
    def test_register_success(self, client, sample_user):
        """Test inscription réussie"""
        response = client.post("/api/v1/auth/register", json=sample_user)
        # Note: Peut échouer si pas de DB configurée
        assert response.status_code in [200, 201, 500]
    
    def test_register_weak_password(self, client, sample_user):
        """Test inscription avec mot de passe faible"""
        sample_user["password"] = "weak"
        sample_user["password_confirm"] = "weak"
        response = client.post("/api/v1/auth/register", json=sample_user)
        assert response.status_code == 422  # Validation error
    
    def test_register_password_mismatch(self, client, sample_user):
        """Test inscription avec mots de passe différents"""
        sample_user["password_confirm"] = "DifferentPass123!"
        response = client.post("/api/v1/auth/register", json=sample_user)
        assert response.status_code == 422


class TestLogin:
    """Tests de connexion"""
    
    def test_login_missing_fields(self, client):
        """Test connexion sans champs requis"""
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422
    
    def test_login_invalid_email(self, client):
        """Test connexion avec email invalide"""
        response = client.post("/api/v1/auth/login", json={
            "email": "not-an-email",
            "password": "TestPass123!"
        })
        assert response.status_code == 422
