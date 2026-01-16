"""
Tests — Health endpoints
"""

import pytest


def test_root(client):
    """Test endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_health(client):
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_health(client):
    """Test API health check"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
