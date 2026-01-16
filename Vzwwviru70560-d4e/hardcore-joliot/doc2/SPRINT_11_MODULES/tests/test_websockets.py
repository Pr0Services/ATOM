"""CHE·NU™ - WebSocket Tests"""
import pytest
from fastapi.testclient import TestClient

class TestWebSocketConnections:
    def test_websocket_connect(self, client):
        with client.websocket_connect("/ws") as websocket:
            data = websocket.receive_json()
            assert data["type"] == "connection_established"
    
    def test_websocket_auth(self, client, auth_token):
        with client.websocket_connect(f"/ws?token={auth_token}") as websocket:
            websocket.send_json({"type": "ping"})
            data = websocket.receive_json()
            assert data["type"] == "pong"
    
    def test_websocket_broadcast(self, client):
        with client.websocket_connect("/ws") as ws1, \
             client.websocket_connect("/ws") as ws2:
            ws1.send_json({"type": "message", "content": "Hello"})
            data = ws2.receive_json()
            assert data["content"] == "Hello"

class TestRealtimeUpdates:
    def test_thread_update_broadcast(self, client, auth_headers):
        with client.websocket_connect("/ws/threads") as websocket:
            # Update thread via API
            client.put("/api/v1/threads/1", 
                      json={"title": "Updated"},
                      headers=auth_headers)
            
            # Should receive update via websocket
            data = websocket.receive_json()
            assert data["type"] == "thread_updated"
            assert data["thread"]["title"] == "Updated"
    
    def test_agent_execution_status(self, client):
        with client.websocket_connect("/ws/agents") as websocket:
            # Start agent execution
            client.post("/api/v1/agents/execute",
                       json={"agent_id": "test"})
            
            # Should receive status updates
            data = websocket.receive_json()
            assert data["type"] == "agent_status"
            assert data["status"] in ["pending", "running", "completed"]
