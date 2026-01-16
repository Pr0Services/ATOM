"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — TEST FACTORIES
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A1: Test Framework Setup
Date: 8 Janvier 2026

Factories pour générer des objets de test cohérents avec l'architecture CHE·NU.
Toutes les données sont SYNTHETIC (jamais de données réelles).
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone, timedelta
from uuid import uuid4, UUID
import random
import string


# ═══════════════════════════════════════════════════════════════════════════════
# BASE FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class BaseFactory:
    """Factory de base avec méthodes communes."""
    
    @staticmethod
    def generate_id() -> str:
        """Génère un UUID unique."""
        return str(uuid4())
    
    @staticmethod
    def generate_timestamp(offset_hours: int = 0) -> str:
        """Génère un timestamp ISO."""
        dt = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
        return dt.isoformat()
    
    @staticmethod
    def generate_email(prefix: str = "user") -> str:
        """Génère un email de test."""
        suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
        return f"{prefix}_{suffix}@test.chenu.io"
    
    @staticmethod
    def generate_name() -> str:
        """Génère un nom de test."""
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"


# ═══════════════════════════════════════════════════════════════════════════════
# USER FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class UserFactory(BaseFactory):
    """Factory pour créer des utilisateurs de test."""
    
    DEFAULT_SPHERES = ["Personal", "Business"]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        roles: Optional[List[str]] = None,
        spheres: Optional[List[str]] = None,
        is_active: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée un utilisateur de test."""
        return {
            "id": id or cls.generate_id(),
            "email": email or cls.generate_email(),
            "name": name or cls.generate_name(),
            "created_at": cls.generate_timestamp(),
            "is_active": is_active,
            "roles": roles or ["user"],
            "spheres": spheres or cls.DEFAULT_SPHERES,
            "preferences": kwargs.get("preferences", {}),
            "synthetic": True  # TOUJOURS marquer comme synthétique
        }
    
    @classmethod
    def create_admin(cls, **kwargs) -> Dict[str, Any]:
        """Crée un admin de test."""
        return cls.create(
            roles=["user", "admin"],
            spheres=[
                "Personal", "Business", "Government & Institutions",
                "Studio de création", "Community", "Social & Media",
                "Entertainment", "My Team", "Scholar"
            ],
            **kwargs
        )
    
    @classmethod
    def create_batch(cls, count: int, **kwargs) -> List[Dict[str, Any]]:
        """Crée plusieurs utilisateurs."""
        return [cls.create(**kwargs) for _ in range(count)]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadFactory(BaseFactory):
    """Factory pour créer des threads de test."""
    
    MATURITY_LEVELS = ["seed", "sprout", "tree", "fruit"]
    MATURITY_EMOJIS = {"seed": "🌱", "sprout": "🌿", "tree": "🌳", "fruit": "🍎"}
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        owner_id: Optional[str] = None,
        title: Optional[str] = None,
        sphere: str = "Personal",
        maturity_level: str = "seed",
        status: str = "active",
        founding_intent: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée un thread de test R&D compliant."""
        thread_id = id or cls.generate_id()
        owner = owner_id or cls.generate_id()
        now = cls.generate_timestamp()
        
        return {
            # Identifiants
            "id": thread_id,
            "title": title or f"Test Thread {thread_id[:8]}",
            "description": kwargs.get("description", "Thread de test"),
            
            # R&D Rule #6: Traceability (OBLIGATOIRE)
            "created_by": owner,
            "created_at": now,
            "updated_at": now,
            
            # Ownership
            "owner_id": owner,
            "sphere": sphere,
            "bureau_section": "Threads",
            
            # Maturity
            "maturity_level": maturity_level,
            "maturity_score": cls._maturity_score(maturity_level),
            "maturity_emoji": cls.MATURITY_EMOJIS.get(maturity_level, "🌱"),
            
            # Status
            "status": status,
            "is_archived": kwargs.get("is_archived", False),
            "is_pinned": kwargs.get("is_pinned", False),
            
            # Founding Intent (IMMUTABLE)
            "founding_intent": founding_intent or "Objectif initial du thread",
            
            # Relations
            "parent_thread_id": kwargs.get("parent_thread_id"),
            "tags": kwargs.get("tags", []),
            "events_count": kwargs.get("events_count", 0),
            
            # Marker
            "synthetic": True
        }
    
    @classmethod
    def _maturity_score(cls, level: str) -> float:
        """Calcule le score de maturité."""
        scores = {"seed": 0.0, "sprout": 0.33, "tree": 0.66, "fruit": 1.0}
        return scores.get(level, 0.0)
    
    @classmethod
    def create_with_events(
        cls,
        event_count: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée un thread avec des events."""
        thread = cls.create(**kwargs)
        thread["events_count"] = event_count
        thread["events"] = [
            ThreadEventFactory.create(
                thread_id=thread["id"],
                created_by=thread["owner_id"]
            )
            for _ in range(event_count)
        ]
        return thread
    
    @classmethod
    def create_batch_chronological(
        cls,
        count: int,
        owner_id: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Crée des threads en ordre chronologique (R&D Rule #5)."""
        threads = []
        for i in range(count):
            thread = cls.create(
                owner_id=owner_id,
                **kwargs
            )
            # Ajuster le timestamp pour ordre chronologique
            thread["created_at"] = cls.generate_timestamp(offset_hours=-i)
            threads.append(thread)
        return threads


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENT FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadEventFactory(BaseFactory):
    """Factory pour créer des events de thread (IMMUTABLES)."""
    
    EVENT_TYPES = ["message", "decision", "file_upload", "status_change", "checkpoint"]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        thread_id: Optional[str] = None,
        created_by: Optional[str] = None,
        event_type: str = "message",
        content: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée un event de thread (IMMUTABLE by design)."""
        return {
            "id": id or cls.generate_id(),
            "thread_id": thread_id or cls.generate_id(),
            "event_type": event_type,
            "content": content or f"Event content {cls.generate_id()[:8]}",
            
            # R&D Rule #6: Traceability
            "created_by": created_by or cls.generate_id(),
            "created_at": cls.generate_timestamp(),
            
            # IMPORTANT: Les events sont IMMUTABLES
            # PAS de updated_at car ils ne peuvent pas être modifiés
            "is_immutable": True,
            
            "metadata": kwargs.get("metadata", {}),
            "synthetic": True
        }
    
    @classmethod
    def create_batch(
        cls,
        count: int,
        thread_id: str,
        created_by: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Crée plusieurs events pour un thread."""
        events = []
        for i in range(count):
            event = cls.create(
                thread_id=thread_id,
                created_by=created_by,
                **kwargs
            )
            # Ordre chronologique
            event["created_at"] = cls.generate_timestamp(offset_hours=-i)
            events.append(event)
        return events


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION FACTORY (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionFactory(BaseFactory):
    """Factory pour créer des décisions/checkpoints."""
    
    STATUSES = ["pending", "approved", "rejected", "expired"]
    AGING_STATUSES = ["green", "yellow", "orange", "red", "blink"]
    IMPACT_LEVELS = ["low", "medium", "high", "critical"]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        created_by: Optional[str] = None,
        status: str = "pending",
        impact_level: str = "high",
        aging_status: str = "green",
        requires_human_approval: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée une décision de test."""
        decision_id = id or cls.generate_id()
        now = cls.generate_timestamp()
        
        decision = {
            "id": decision_id,
            "title": kwargs.get("title", f"Decision {decision_id[:8]}"),
            "description": kwargs.get("description", "Test decision"),
            
            # R&D Rule #6: Traceability
            "created_by": created_by or cls.generate_id(),
            "created_at": now,
            
            # Status
            "status": status,
            "requires_human_approval": requires_human_approval,
            
            # Aging (Decision Points)
            "aging_status": aging_status,
            "expires_at": kwargs.get("expires_at"),
            
            # Context
            "action_type": kwargs.get("action_type", "sensitive_action"),
            "impact_level": impact_level,
            "sphere": kwargs.get("sphere", "Business"),
            "thread_id": kwargs.get("thread_id"),
            
            # Approval
            "approved_by": None,
            "approved_at": None,
            "rejection_reason": None,
            
            "synthetic": True
        }
        
        # Si approuvé, ajouter les infos d'approbation
        if status == "approved":
            decision["approved_by"] = kwargs.get("approved_by", decision["created_by"])
            decision["approved_at"] = now
        
        # Si rejeté, ajouter la raison
        if status == "rejected":
            decision["rejection_reason"] = kwargs.get(
                "rejection_reason", 
                "Rejected during testing"
            )
        
        return decision
    
    @classmethod
    def create_pending(cls, **kwargs) -> Dict[str, Any]:
        """Crée une décision en attente."""
        return cls.create(status="pending", **kwargs)
    
    @classmethod
    def create_approved(cls, **kwargs) -> Dict[str, Any]:
        """Crée une décision approuvée."""
        return cls.create(status="approved", **kwargs)
    
    @classmethod
    def create_critical(cls, **kwargs) -> Dict[str, Any]:
        """Crée une décision critique (requires checkpoint)."""
        return cls.create(
            impact_level="critical",
            requires_human_approval=True,
            **kwargs
        )


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class AgentFactory(BaseFactory):
    """Factory pour créer des agents de test."""
    
    LEVELS = {
        0: {"name": "Utility", "requires_checkpoint": False, "token_cost": 10},
        1: {"name": "Specialist", "requires_checkpoint": False, "token_cost": 25},
        2: {"name": "Advisor", "requires_checkpoint": True, "token_cost": 50},
        3: {"name": "Orchestrator", "requires_checkpoint": True, "token_cost": 100}
    }
    
    CATEGORIES = ["utility", "analysis", "creation", "strategic", "communication"]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        name: Optional[str] = None,
        level: int = 0,
        category: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée un agent de test."""
        agent_id = id or cls.generate_id()
        level_info = cls.LEVELS.get(level, cls.LEVELS[0])
        
        return {
            "id": agent_id,
            "name": name or f"Agent {agent_id[:8]}",
            "description": kwargs.get("description", f"Test agent level {level}"),
            "level": level,
            "level_name": level_info["name"],
            "category": category or random.choice(cls.CATEGORIES),
            
            "is_system": kwargs.get("is_system", False),
            "is_active": kwargs.get("is_active", True),
            
            "capabilities": kwargs.get("capabilities", ["default"]),
            "requires_checkpoint": level_info["requires_checkpoint"],
            
            # R&D Rule #4: NO AI-to-AI orchestration
            "can_call_other_agents": False,  # TOUJOURS False
            
            "token_cost": level_info["token_cost"],
            "is_free": level == 0,
            
            "synthetic": True
        }
    
    @classmethod
    def create_nova(cls) -> Dict[str, Any]:
        """Crée Nova (assistant système)."""
        return {
            "id": "nova-system-001",
            "name": "Nova",
            "description": "Assistant système CHE·NU",
            "level": "system",
            "level_name": "System",
            "category": "system",
            
            "is_system": True,  # Nova est TOUJOURS système
            "is_active": True,
            
            "capabilities": ["assist", "guide", "checkpoint_create", "explain"],
            "requires_checkpoint": False,  # Nova CRÉE les checkpoints
            
            "can_call_other_agents": False,
            
            "token_cost": 0,
            "is_free": True,
            
            "synthetic": True
        }
    
    @classmethod
    def create_l0(cls, **kwargs) -> Dict[str, Any]:
        """Crée un agent L0 (Utilitaire)."""
        return cls.create(level=0, **kwargs)
    
    @classmethod
    def create_l3(cls, **kwargs) -> Dict[str, Any]:
        """Crée un agent L3 (Orchestrateur - requires checkpoint)."""
        return cls.create(level=3, **kwargs)
    
    @classmethod
    def create_marketplace(cls, count: int = 10) -> List[Dict[str, Any]]:
        """Crée un ensemble d'agents pour le marketplace."""
        agents = [cls.create_nova()]  # Nova toujours présent
        
        for _ in range(count):
            level = random.choice([0, 1, 2, 3])
            agents.append(cls.create(level=level))
        
        return agents


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class SphereFactory(BaseFactory):
    """Factory pour créer des sphères de test."""
    
    ALL_SPHERES = [
        "Personal",
        "Business", 
        "Government & Institutions",
        "Studio de création",
        "Community",
        "Social & Media",
        "Entertainment",
        "My Team",
        "Scholar"
    ]
    
    BUREAU_SECTIONS = [
        "QuickCapture",
        "ResumeWorkspace",
        "Threads",
        "DataFiles",
        "ActiveAgents",
        "Meetings"
    ]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        name: Optional[str] = None,
        owner_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée une sphère de test."""
        return {
            "id": id or cls.generate_id(),
            "name": name or random.choice(cls.ALL_SPHERES),
            "owner_id": owner_id or cls.generate_id(),
            "is_active": kwargs.get("is_active", True),
            "bureau_sections": cls.BUREAU_SECTIONS.copy(),  # Toujours 6 sections
            "settings": kwargs.get("settings", {}),
            "created_at": cls.generate_timestamp(),
            "synthetic": True
        }
    
    @classmethod
    def create_all_for_user(cls, owner_id: str) -> List[Dict[str, Any]]:
        """Crée les 9 sphères pour un utilisateur."""
        return [
            cls.create(name=sphere, owner_id=owner_id)
            for sphere in cls.ALL_SPHERES
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

class AuditLogFactory(BaseFactory):
    """Factory pour créer des logs d'audit (R&D Rule #6)."""
    
    ACTIONS = [
        "thread.create", "thread.update", "thread.archive",
        "decision.create", "decision.approve", "decision.reject",
        "agent.hire", "agent.fire",
        "sphere.access", "sphere.settings_update",
        "checkpoint.create", "checkpoint.approve"
    ]
    
    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Crée une entrée d'audit log."""
        return {
            "id": id or cls.generate_id(),
            "timestamp": cls.generate_timestamp(),
            "user_id": user_id or cls.generate_id(),
            "action": action or random.choice(cls.ACTIONS),
            "resource_type": kwargs.get("resource_type", "thread"),
            "resource_id": kwargs.get("resource_id", cls.generate_id()),
            "details": kwargs.get("details", {}),
            "ip_address": kwargs.get("ip_address", "127.0.0.1"),
            "user_agent": kwargs.get("user_agent", "pytest"),
            "synthetic": True
        }
    
    @classmethod
    def create_batch(
        cls,
        count: int,
        user_id: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Crée plusieurs entrées d'audit."""
        logs = []
        for i in range(count):
            log = cls.create(user_id=user_id, **kwargs)
            log["timestamp"] = cls.generate_timestamp(offset_hours=-i)
            logs.append(log)
        return logs


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT ALL FACTORIES
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "BaseFactory",
    "UserFactory",
    "ThreadFactory",
    "ThreadEventFactory",
    "DecisionFactory",
    "AgentFactory",
    "SphereFactory",
    "AuditLogFactory"
]
