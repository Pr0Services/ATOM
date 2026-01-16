"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — SERVICE MOCKS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A1: Test Framework Setup
Date: 8 Janvier 2026

Mocks pour tous les services externes utilisés par CHE·NU.
Permet des tests isolés sans dépendances réelles.
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import MagicMock, AsyncMock, PropertyMock
from contextlib import asynccontextmanager


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE MOCK
# ═══════════════════════════════════════════════════════════════════════════════

class MockDatabaseSession:
    """Mock complet d'une session SQLAlchemy async."""
    
    def __init__(self):
        self._data_store: Dict[str, Dict[str, Any]] = {}
        self._pending: List[Any] = []
        self._deleted: List[Any] = []
        self._committed = False
        self._rolled_back = False
    
    async def execute(self, query, params=None):
        """Mock execute - retourne un result mock."""
        result = MockResult()
        return result
    
    def add(self, obj):
        """Mock add - stocke l'objet en pending."""
        self._pending.append(obj)
    
    def add_all(self, objs):
        """Mock add_all."""
        self._pending.extend(objs)
    
    def delete(self, obj):
        """Mock delete."""
        self._deleted.append(obj)
    
    async def commit(self):
        """Mock commit."""
        self._committed = True
        # Move pending to data store
        for obj in self._pending:
            table = obj.__class__.__name__
            if table not in self._data_store:
                self._data_store[table] = {}
            obj_id = getattr(obj, 'id', str(uuid4()))
            self._data_store[table][str(obj_id)] = obj
        self._pending = []
    
    async def rollback(self):
        """Mock rollback."""
        self._rolled_back = True
        self._pending = []
        self._deleted = []
    
    async def close(self):
        """Mock close."""
        pass
    
    async def refresh(self, obj):
        """Mock refresh."""
        pass
    
    async def flush(self):
        """Mock flush."""
        pass
    
    def expire_all(self):
        """Mock expire_all."""
        pass
    
    # Context manager support
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.close()


class MockResult:
    """Mock d'un résultat de requête SQLAlchemy."""
    
    def __init__(self, data: List[Any] = None):
        self._data = data or []
        self._index = 0
    
    def scalars(self):
        """Retourne self pour chaînage."""
        return self
    
    def all(self) -> List[Any]:
        """Retourne toutes les données."""
        return self._data
    
    def first(self) -> Optional[Any]:
        """Retourne le premier élément."""
        return self._data[0] if self._data else None
    
    def one(self) -> Any:
        """Retourne exactement un élément."""
        if len(self._data) != 1:
            raise Exception("Expected exactly one result")
        return self._data[0]
    
    def one_or_none(self) -> Optional[Any]:
        """Retourne un élément ou None."""
        if len(self._data) > 1:
            raise Exception("Expected at most one result")
        return self._data[0] if self._data else None
    
    def __iter__(self):
        return iter(self._data)


@asynccontextmanager
async def mock_get_db_session():
    """Context manager pour obtenir une session mock."""
    session = MockDatabaseSession()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# ═══════════════════════════════════════════════════════════════════════════════
# REDIS MOCK
# ═══════════════════════════════════════════════════════════════════════════════

class MockRedis:
    """Mock complet d'un client Redis async."""
    
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, datetime] = {}
    
    async def get(self, key: str) -> Optional[str]:
        """Get a value."""
        self._check_expiry(key)
        value = self._store.get(key)
        return value.encode() if isinstance(value, str) else value
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ex: int = None,
        px: int = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """Set a value."""
        if nx and key in self._store:
            return False
        if xx and key not in self._store:
            return False
        
        self._store[key] = value
        
        if ex:
            from datetime import timedelta
            self._expiry[key] = datetime.now(timezone.utc) + timedelta(seconds=ex)
        elif px:
            from datetime import timedelta
            self._expiry[key] = datetime.now(timezone.utc) + timedelta(milliseconds=px)
        
        return True
    
    async def delete(self, *keys: str) -> int:
        """Delete keys."""
        count = 0
        for key in keys:
            if key in self._store:
                del self._store[key]
                self._expiry.pop(key, None)
                count += 1
        return count
    
    async def exists(self, *keys: str) -> int:
        """Check if keys exist."""
        count = 0
        for key in keys:
            self._check_expiry(key)
            if key in self._store:
                count += 1
        return count
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiry on a key."""
        if key not in self._store:
            return False
        from datetime import timedelta
        self._expiry[key] = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        return True
    
    async def ttl(self, key: str) -> int:
        """Get TTL of a key."""
        if key not in self._store:
            return -2
        if key not in self._expiry:
            return -1
        
        remaining = (self._expiry[key] - datetime.now(timezone.utc)).total_seconds()
        return max(0, int(remaining))
    
    async def incr(self, key: str) -> int:
        """Increment a key."""
        self._store[key] = int(self._store.get(key, 0)) + 1
        return self._store[key]
    
    async def decr(self, key: str) -> int:
        """Decrement a key."""
        self._store[key] = int(self._store.get(key, 0)) - 1
        return self._store[key]
    
    async def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field."""
        hash_data = self._store.get(name, {})
        return hash_data.get(key)
    
    async def hset(self, name: str, key: str = None, value: Any = None, mapping: Dict = None) -> int:
        """Set hash field(s)."""
        if name not in self._store:
            self._store[name] = {}
        
        count = 0
        if key is not None:
            self._store[name][key] = value
            count = 1
        if mapping:
            self._store[name].update(mapping)
            count = len(mapping)
        
        return count
    
    async def hgetall(self, name: str) -> Dict[str, Any]:
        """Get all hash fields."""
        return self._store.get(name, {})
    
    async def lpush(self, key: str, *values) -> int:
        """Push to list."""
        if key not in self._store:
            self._store[key] = []
        self._store[key] = list(values) + self._store[key]
        return len(self._store[key])
    
    async def rpush(self, key: str, *values) -> int:
        """Push to end of list."""
        if key not in self._store:
            self._store[key] = []
        self._store[key].extend(values)
        return len(self._store[key])
    
    async def lrange(self, key: str, start: int, stop: int) -> List[Any]:
        """Get list range."""
        data = self._store.get(key, [])
        if stop == -1:
            return data[start:]
        return data[start:stop + 1]
    
    async def publish(self, channel: str, message: str) -> int:
        """Publish message (mock)."""
        return 1
    
    async def close(self):
        """Close connection."""
        pass
    
    def _check_expiry(self, key: str):
        """Check and remove expired keys."""
        if key in self._expiry:
            if datetime.now(timezone.utc) > self._expiry[key]:
                del self._store[key]
                del self._expiry[key]


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT SERVICE MOCK (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

class MockCheckpointService:
    """
    Mock du service de checkpoints.
    
    CRITICAL pour tester R&D Rule #1: Human Sovereignty.
    Ce service contrôle si une action sensible peut s'exécuter.
    """
    
    def __init__(self):
        self._checkpoints: Dict[str, Dict[str, Any]] = {}
        self._default_required = True
        self._default_approved = False
    
    def configure(self, required: bool = True, approved: bool = False):
        """Configure le comportement par défaut."""
        self._default_required = required
        self._default_approved = approved
    
    async def is_checkpoint_required(
        self, 
        action_type: str,
        impact_level: str = "medium"
    ) -> bool:
        """Vérifie si un checkpoint est requis pour cette action."""
        # Actions critiques = toujours checkpoint
        critical_actions = [
            "delete", "archive", "transfer", "payment",
            "agent_execute_l2", "agent_execute_l3",
            "cross_sphere", "external_api"
        ]
        
        if action_type in critical_actions:
            return True
        
        if impact_level in ["high", "critical"]:
            return True
        
        return self._default_required
    
    async def is_approved(self, checkpoint_id: str) -> bool:
        """Vérifie si un checkpoint est approuvé."""
        checkpoint = self._checkpoints.get(checkpoint_id)
        if checkpoint:
            return checkpoint.get("status") == "approved"
        return self._default_approved
    
    async def create_checkpoint(
        self,
        action_type: str,
        user_id: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Crée un nouveau checkpoint (en attente)."""
        checkpoint_id = str(uuid4())
        checkpoint = {
            "id": checkpoint_id,
            "action_type": action_type,
            "user_id": user_id,
            "status": "pending",
            "context": context or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "approved_at": None,
            "approved_by": None
        }
        self._checkpoints[checkpoint_id] = checkpoint
        return checkpoint
    
    async def approve(
        self, 
        checkpoint_id: str, 
        approver_id: str
    ) -> Dict[str, Any]:
        """Approuve un checkpoint."""
        if checkpoint_id not in self._checkpoints:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        checkpoint = self._checkpoints[checkpoint_id]
        checkpoint["status"] = "approved"
        checkpoint["approved_at"] = datetime.now(timezone.utc).isoformat()
        checkpoint["approved_by"] = approver_id
        
        return checkpoint
    
    async def reject(
        self, 
        checkpoint_id: str, 
        rejector_id: str,
        reason: str = None
    ) -> Dict[str, Any]:
        """Rejette un checkpoint."""
        if checkpoint_id not in self._checkpoints:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")
        
        checkpoint = self._checkpoints[checkpoint_id]
        checkpoint["status"] = "rejected"
        checkpoint["rejected_at"] = datetime.now(timezone.utc).isoformat()
        checkpoint["rejected_by"] = rejector_id
        checkpoint["rejection_reason"] = reason
        
        return checkpoint
    
    async def get_pending(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupère les checkpoints en attente pour un utilisateur."""
        return [
            cp for cp in self._checkpoints.values()
            if cp["user_id"] == user_id and cp["status"] == "pending"
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY SERVICE MOCK (R&D Rule #3)
# ═══════════════════════════════════════════════════════════════════════════════

class MockIdentityService:
    """
    Mock du service d'identité.
    
    CRITICAL pour tester R&D Rule #3: Identity Boundary.
    Ce service vérifie qu'un utilisateur n'accède qu'à SES données.
    """
    
    def __init__(self, current_user_id: str = None):
        self._current_user_id = current_user_id or str(uuid4())
        self._resource_owners: Dict[str, str] = {}
    
    def set_current_user(self, user_id: str):
        """Configure l'utilisateur actuel."""
        self._current_user_id = user_id
    
    def register_resource(self, resource_id: str, owner_id: str):
        """Enregistre le propriétaire d'une ressource."""
        self._resource_owners[resource_id] = owner_id
    
    async def get_current_user_id(self) -> str:
        """Retourne l'ID de l'utilisateur actuel."""
        return self._current_user_id
    
    async def verify_ownership(
        self, 
        resource_owner_id: str, 
        requesting_user_id: str = None
    ) -> bool:
        """
        Vérifie que l'utilisateur est propriétaire de la ressource.
        
        Retourne True si propriétaire, False sinon.
        NE LÈVE PAS d'exception - c'est au service appelant de décider.
        """
        requester = requesting_user_id or self._current_user_id
        return resource_owner_id == requester
    
    async def verify_access(
        self,
        resource_id: str,
        requesting_user_id: str = None
    ) -> bool:
        """Vérifie l'accès à une ressource par son ID."""
        owner = self._resource_owners.get(resource_id)
        if not owner:
            return False
        
        requester = requesting_user_id or self._current_user_id
        return owner == requester
    
    async def assert_ownership(
        self,
        resource_owner_id: str,
        requesting_user_id: str = None
    ):
        """
        Asserte la propriété - LÈVE une exception si pas propriétaire.
        
        Utilisé quand l'accès non autorisé doit être bloqué.
        """
        if not await self.verify_ownership(resource_owner_id, requesting_user_id):
            raise PermissionError(
                f"Identity boundary violation: User {requesting_user_id or self._current_user_id} "
                f"cannot access resource owned by {resource_owner_id}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE SERVICE MOCK
# ═══════════════════════════════════════════════════════════════════════════════

class MockGovernanceService:
    """Mock du service de gouvernance."""
    
    def __init__(self):
        self._audit_log: List[Dict[str, Any]] = []
        self._blocked_actions: set = set()
    
    def block_action(self, action: str):
        """Bloque une action spécifique."""
        self._blocked_actions.add(action)
    
    def unblock_action(self, action: str):
        """Débloque une action."""
        self._blocked_actions.discard(action)
    
    async def check_action_allowed(
        self,
        action: str,
        user_id: str,
        context: Dict[str, Any] = None
    ) -> bool:
        """Vérifie si une action est autorisée."""
        if action in self._blocked_actions:
            return False
        return True
    
    async def log_action(
        self,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Dict[str, Any] = None
    ):
        """Log une action dans l'audit trail."""
        entry = {
            "id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {}
        }
        self._audit_log.append(entry)
        return entry
    
    async def get_audit_log(
        self,
        user_id: str = None,
        action: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Récupère l'audit log filtré."""
        logs = self._audit_log
        
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        if action:
            logs = [l for l in logs if l["action"] == action]
        
        return logs[-limit:]
    
    async def get_cea_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques CEA."""
        return {
            "total_actions": len(self._audit_log),
            "compliance_rate": 0.98,
            "pending_checkpoints": 5,
            "approved_checkpoints": 145,
            "rejected_checkpoints": 3
        }


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT SERVICE MOCK (R&D Rule #4)
# ═══════════════════════════════════════════════════════════════════════════════

class MockAgentService:
    """
    Mock du service d'agents.
    
    CRITICAL pour tester R&D Rule #4: My Team Restrictions.
    Aucun agent ne peut appeler directement un autre agent.
    """
    
    def __init__(self):
        self._agents: Dict[str, Dict[str, Any]] = {}
        self._hired_agents: Dict[str, List[str]] = {}  # user_id -> [agent_ids]
    
    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Récupère un agent."""
        return self._agents.get(agent_id)
    
    async def list_marketplace(
        self,
        category: str = None,
        level: int = None
    ) -> List[Dict[str, Any]]:
        """Liste les agents du marketplace."""
        agents = list(self._agents.values())
        
        if category:
            agents = [a for a in agents if a.get("category") == category]
        if level is not None:
            agents = [a for a in agents if a.get("level") == level]
        
        return agents
    
    async def hire_agent(
        self,
        agent_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Engage un agent pour un utilisateur."""
        if user_id not in self._hired_agents:
            self._hired_agents[user_id] = []
        
        if agent_id not in self._hired_agents[user_id]:
            self._hired_agents[user_id].append(agent_id)
        
        return {"agent_id": agent_id, "user_id": user_id, "status": "hired"}
    
    async def fire_agent(
        self,
        agent_id: str,
        user_id: str
    ) -> bool:
        """Renvoie un agent."""
        if user_id in self._hired_agents:
            if agent_id in self._hired_agents[user_id]:
                self._hired_agents[user_id].remove(agent_id)
                return True
        return False
    
    async def execute_agent(
        self,
        agent_id: str,
        user_id: str,
        input_data: Dict[str, Any],
        checkpoint_approved: bool = False
    ) -> Dict[str, Any]:
        """
        Exécute un agent.
        
        R&D Rule #4: Un agent NE PEUT PAS appeler un autre agent.
        Si input_data contient "call_agent", on REFUSE.
        """
        agent = self._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # R&D Rule #4: Bloquer les appels inter-agents
        if "call_agent" in input_data or "agent_chain" in input_data:
            raise PermissionError(
                "R&D Rule #4 violation: AI-to-AI orchestration is forbidden"
            )
        
        # R&D Rule #1: Vérifier checkpoint pour L2/L3
        if agent.get("level", 0) >= 2 and not checkpoint_approved:
            raise PermissionError(
                "R&D Rule #1 violation: Agent L2/L3 requires checkpoint approval"
            )
        
        return {
            "agent_id": agent_id,
            "status": "completed",
            "output": f"Mock output from {agent.get('name', 'Unknown')}",
            "synthetic": True
        }


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP CLIENT MOCK (FastAPI TestClient helper)
# ═══════════════════════════════════════════════════════════════════════════════

class MockHTTPResponse:
    """Mock d'une réponse HTTP."""
    
    def __init__(
        self,
        status_code: int = 200,
        json_data: Any = None,
        headers: Dict[str, str] = None
    ):
        self.status_code = status_code
        self._json_data = json_data
        self.headers = headers or {}
    
    def json(self) -> Any:
        return self._json_data
    
    @property
    def text(self) -> str:
        import json
        return json.dumps(self._json_data) if self._json_data else ""
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT ALL MOCKS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "MockDatabaseSession",
    "MockResult",
    "mock_get_db_session",
    "MockRedis",
    "MockCheckpointService",
    "MockIdentityService",
    "MockGovernanceService",
    "MockAgentService",
    "MockHTTPResponse"
]
