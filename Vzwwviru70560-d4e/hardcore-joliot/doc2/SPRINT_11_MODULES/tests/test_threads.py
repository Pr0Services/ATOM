"""
Tests — Threads/Chat
"""

import pytest


class TestModels:
    """Tests liste des modèles"""
    
    def test_list_models(self, client):
        """Test récupération des modèles LLM"""
        response = client.get("/api/v1/threads/models")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Vérifier structure
        model = data[0]
        assert "id" in model
        assert "name" in model
        assert "provider" in model
        assert "tier" in model


class TestThreads:
    """Tests CRUD threads"""
    
    def test_list_threads_unauthorized(self, client):
        """Test liste threads sans auth"""
        response = client.get("/api/v1/threads")
        assert response.status_code == 401
    
    def test_create_thread_unauthorized(self, client, sample_thread):
        """Test création thread sans auth"""
        response = client.post("/api/v1/threads", json=sample_thread)
        assert response.status_code == 401
