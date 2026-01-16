"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — PYTEST CONFTEST (FIXTURES GLOBALES)
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A1: Test Framework Setup
Date: 8 Janvier 2026

Ce fichier contient toutes les fixtures globales pour les tests CHE·NU.
Respecte les 7 Règles R&D et la philosophie GOUVERNANCE > EXÉCUTION.
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator, Dict, Any, Optional
from datetime import datetime, timezone
from uuid import uuid4, UUID
from unittest.mock import MagicMock, AsyncMock, patch
from contextlib import asynccontextmanager
import json
import os

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION ASYNC
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def event_loop():
    """Crée un event loop pour toute la session de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: UTILISATEURS & IDENTITÉS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def user_id() -> UUID:
    """ID utilisateur de test standard."""
    return uuid4()


@pytest.fixture
def other_user_id() -> UUID:
    """ID d'un AUTRE utilisateur (pour tests identity boundary)."""
    return uuid4()


@pytest.fixture
def mock_user(user_id: UUID) -> Dict[str, Any]:
    """Utilisateur de test complet."""
    return {
        "id": str(user_id),
        "email": "test@chenu.io",
        "name": "Test User",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True,
        "roles": ["user"],
        "spheres": ["Personal", "Business"],
        "preferences": {
            "theme": "dark",
            "language": "fr"
        }
    }


@pytest.fixture
def mock_admin_user(user_id: UUID) -> Dict[str, Any]:
    """Utilisateur admin de test."""
    return {
        "id": str(user_id),
        "email": "admin@chenu.io",
        "name": "Admin User",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True,
        "roles": ["user", "admin"],
        "spheres": ["Personal", "Business", "Government & Institutions"],
        "preferences": {}
    }


@pytest.fixture
def mock_other_user(other_user_id: UUID) -> Dict[str, Any]:
    """Autre utilisateur pour tests de boundary."""
    return {
        "id": str(other_user_id),
        "email": "other@chenu.io",
        "name": "Other User",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "is_active": True,
        "roles": ["user"],
        "spheres": ["Personal"],
        "preferences": {}
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: THREADS (avec Maturity Levels)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def thread_id() -> UUID:
    """ID thread de test."""
    return uuid4()


@pytest.fixture
def mock_thread(thread_id: UUID, user_id: UUID) -> Dict[str, Any]:
    """Thread de test avec tous les champs R&D compliant."""
    now = datetime.now(timezone.utc)
    return {
        # Identifiants
        "id": str(thread_id),
        "title": "Test Thread",
        "description": "Thread de test pour validation",
        
        # R&D Rule #6: Traceability
        "created_by": str(user_id),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        
        # Ownership
        "owner_id": str(user_id),
        "sphere": "Personal",
        "bureau_section": "Threads",
        
        # Maturity (🌱→🌿→🌳→🍎)
        "maturity_level": "seed",  # seed, sprout, tree, fruit
        "maturity_score": 0.0,
        
        # Status
        "status": "active",
        "is_archived": False,
        "is_pinned": False,
        
        # Founding Intent (immuable)
        "founding_intent": "Objectif initial du thread",
        
        # Relations
        "parent_thread_id": None,
        "tags": ["test"],
        "events_count": 0
    }


@pytest.fixture
def mock_thread_event(thread_id: UUID, user_id: UUID) -> Dict[str, Any]:
    """Event de thread (IMMUTABLE par design)."""
    now = datetime.now(timezone.utc)
    return {
        "id": str(uuid4()),
        "thread_id": str(thread_id),
        "event_type": "message",
        "content": "Test event content",
        
        # R&D Rule #6: Traceability
        "created_by": str(user_id),
        "created_at": now.isoformat(),
        
        # Les events sont IMMUTABLES - pas de updated_at
        "is_immutable": True,
        
        "metadata": {}
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: DÉCISIONS & CHECKPOINTS (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def decision_id() -> UUID:
    """ID décision de test."""
    return uuid4()


@pytest.fixture
def checkpoint_id() -> UUID:
    """ID checkpoint de test."""
    return uuid4()


@pytest.fixture
def mock_pending_decision(decision_id: UUID, user_id: UUID) -> Dict[str, Any]:
    """Décision en attente d'approbation humaine (R&D Rule #1)."""
    now = datetime.now(timezone.utc)
    return {
        "id": str(decision_id),
        "title": "Action Sensible Requiert Approbation",
        "description": "Cette action nécessite une validation humaine",
        
        # R&D Rule #6: Traceability
        "created_by": str(user_id),
        "created_at": now.isoformat(),
        
        # Status checkpoint
        "status": "pending",  # pending, approved, rejected, expired
        "requires_human_approval": True,
        
        # Aging system (Decision Points)
        "aging_status": "green",  # green, yellow, orange, red, blink
        "expires_at": None,
        
        # Context
        "action_type": "sensitive_action",
        "impact_level": "high",  # low, medium, high, critical
        "sphere": "Business",
        
        # Approbation
        "approved_by": None,
        "approved_at": None,
        "rejection_reason": None
    }


@pytest.fixture
def mock_approved_decision(decision_id: UUID, user_id: UUID) -> Dict[str, Any]:
    """Décision approuvée par un humain."""
    now = datetime.now(timezone.utc)
    return {
        "id": str(decision_id),
        "title": "Action Approuvée",
        "description": "Cette action a été validée",
        
        "created_by": str(user_id),
        "created_at": now.isoformat(),
        
        "status": "approved",
        "requires_human_approval": True,
        
        "aging_status": "green",
        
        "action_type": "sensitive_action",
        "impact_level": "high",
        "sphere": "Business",
        
        # Approbation complète
        "approved_by": str(user_id),
        "approved_at": now.isoformat(),
        "rejection_reason": None
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: AGENTS (L0-L3 Hierarchy)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def agent_id() -> UUID:
    """ID agent de test."""
    return uuid4()


@pytest.fixture
def mock_agent_l0(agent_id: UUID) -> Dict[str, Any]:
    """Agent Level 0 (Utilitaire simple)."""
    return {
        "id": str(agent_id),
        "name": "Summarizer",
        "description": "Agent de résumé de texte",
        "level": 0,  # L0: Utilitaire
        "category": "utility",
        "is_system": False,
        "is_active": True,
        
        # Capabilities
        "capabilities": ["summarize", "extract_keywords"],
        "requires_checkpoint": False,  # L0 n'a pas besoin de checkpoint
        
        # R&D Rule #4: No AI-to-AI orchestration
        "can_call_other_agents": False,
        
        # Pricing
        "token_cost": 10,
        "is_free": True
    }


@pytest.fixture
def mock_agent_l3(agent_id: UUID) -> Dict[str, Any]:
    """Agent Level 3 (Orchestrateur - REQUIRES checkpoint)."""
    return {
        "id": str(agent_id),
        "name": "Business Strategist",
        "description": "Agent stratégique complexe",
        "level": 3,  # L3: Orchestrateur
        "category": "strategic",
        "is_system": False,
        "is_active": True,
        
        "capabilities": ["analyze", "recommend", "plan"],
        "requires_checkpoint": True,  # L3 DOIT avoir un checkpoint
        
        # R&D Rule #4: Même L3 ne peut pas appeler directement d'autres agents
        "can_call_other_agents": False,
        
        "token_cost": 100,
        "is_free": False
    }


@pytest.fixture
def mock_nova() -> Dict[str, Any]:
    """Nova - L'assistant système (jamais un agent hired)."""
    return {
        "id": "nova-system-001",
        "name": "Nova",
        "description": "Assistant système CHE·NU",
        "level": "system",  # Nova est SYSTÈME, pas L0-L3
        "category": "system",
        "is_system": True,  # IMPORTANT: Nova est TOUJOURS système
        "is_active": True,
        
        "capabilities": ["assist", "guide", "checkpoint_create"],
        "requires_checkpoint": False,  # Nova CRÉE les checkpoints
        
        "can_call_other_agents": False,
        
        "token_cost": 0,
        "is_free": True
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: SPHÈRES & BUREAUX
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def all_spheres() -> list[str]:
    """Les 9 sphères CHE·NU (frozen architecture)."""
    return [
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


@pytest.fixture
def bureau_sections() -> list[str]:
    """Les 6 sections de bureau (frozen architecture)."""
    return [
        "QuickCapture",
        "ResumeWorkspace",
        "Threads",
        "DataFiles",
        "ActiveAgents",
        "Meetings"
    ]


@pytest.fixture
def mock_sphere(user_id: UUID) -> Dict[str, Any]:
    """Sphère de test."""
    return {
        "id": str(uuid4()),
        "name": "Personal",
        "owner_id": str(user_id),
        "is_active": True,
        "bureau_sections": [
            "QuickCapture",
            "ResumeWorkspace", 
            "Threads",
            "DataFiles",
            "ActiveAgents",
            "Meetings"
        ],
        "settings": {},
        "created_at": datetime.now(timezone.utc).isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: GOVERNANCE & AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_audit_log(user_id: UUID) -> Dict[str, Any]:
    """Entry d'audit log (R&D Rule #6)."""
    now = datetime.now(timezone.utc)
    return {
        "id": str(uuid4()),
        "timestamp": now.isoformat(),
        "user_id": str(user_id),
        "action": "thread.create",
        "resource_type": "thread",
        "resource_id": str(uuid4()),
        "details": {"title": "New Thread"},
        "ip_address": "127.0.0.1",
        "user_agent": "pytest"
    }


@pytest.fixture
def mock_cea_metrics() -> Dict[str, Any]:
    """Métriques CEA (Cognitive-Economic Alignment)."""
    return {
        "total_decisions": 150,
        "pending_decisions": 12,
        "approved_decisions": 130,
        "rejected_decisions": 8,
        "avg_decision_time_hours": 2.5,
        "checkpoint_compliance_rate": 0.98,
        "human_override_rate": 0.15
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: MOCKS SERVICES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_db_session():
    """Mock de session database."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.add = MagicMock()
    session.delete = MagicMock()
    return session


@pytest.fixture
def mock_redis():
    """Mock de client Redis."""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=1)
    redis.exists = AsyncMock(return_value=0)
    redis.expire = AsyncMock(return_value=True)
    return redis


@pytest.fixture
def mock_checkpoint_service():
    """Mock du service de checkpoints (R&D Rule #1)."""
    service = AsyncMock()
    
    # Par défaut: checkpoint requis mais pas encore approuvé
    service.is_checkpoint_required = AsyncMock(return_value=True)
    service.is_approved = AsyncMock(return_value=False)
    service.create_checkpoint = AsyncMock(return_value={
        "id": str(uuid4()),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    service.approve = AsyncMock()
    service.reject = AsyncMock()
    
    return service


@pytest.fixture
def mock_identity_service(user_id: UUID):
    """Mock du service d'identité (R&D Rule #3)."""
    service = AsyncMock()
    
    # Vérifie que l'utilisateur accède à SES données
    async def verify_ownership(resource_owner_id: str, requesting_user_id: str):
        return resource_owner_id == requesting_user_id
    
    service.verify_ownership = AsyncMock(side_effect=verify_ownership)
    service.get_current_user_id = AsyncMock(return_value=str(user_id))
    
    return service


@pytest.fixture
def mock_governance_service():
    """Mock du service de gouvernance."""
    service = AsyncMock()
    service.check_action_allowed = AsyncMock(return_value=True)
    service.log_action = AsyncMock()
    service.get_cea_metrics = AsyncMock(return_value={
        "compliance_rate": 0.98
    })
    return service


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: HTTP CLIENT (FastAPI TestClient)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def auth_headers(user_id: UUID) -> Dict[str, str]:
    """Headers d'authentification pour les requêtes API."""
    # En test, on utilise un token simplifié
    return {
        "Authorization": f"Bearer test-token-{user_id}",
        "X-User-ID": str(user_id),
        "Content-Type": "application/json"
    }


@pytest.fixture
def other_user_auth_headers(other_user_id: UUID) -> Dict[str, str]:
    """Headers d'un AUTRE utilisateur (pour tests boundary)."""
    return {
        "Authorization": f"Bearer test-token-{other_user_id}",
        "X-User-ID": str(other_user_id),
        "Content-Type": "application/json"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: HELPERS DE TEST
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def assert_r6_compliance():
    """Helper pour vérifier R&D Rule #6 (Traceability)."""
    def _check(obj: Dict[str, Any]):
        assert "id" in obj, "Missing 'id' field (R&D Rule #6)"
        assert "created_by" in obj, "Missing 'created_by' field (R&D Rule #6)"
        assert "created_at" in obj, "Missing 'created_at' field (R&D Rule #6)"
        
        # Valider le format
        assert obj["id"], "ID cannot be empty"
        assert obj["created_by"], "created_by cannot be empty"
        assert obj["created_at"], "created_at cannot be empty"
        
        return True
    
    return _check


@pytest.fixture
def assert_chronological_order():
    """Helper pour vérifier R&D Rule #5 (No Ranking - chronological only)."""
    def _check(items: list[Dict[str, Any]], field: str = "created_at"):
        if len(items) < 2:
            return True
        
        for i in range(1, len(items)):
            prev_time = items[i-1].get(field)
            curr_time = items[i].get(field)
            
            # DESC order (newest first)
            assert prev_time >= curr_time, (
                f"Items not in chronological order at index {i}. "
                f"R&D Rule #5 violation: No ranking algorithm allowed!"
            )
        
        return True
    
    return _check


@pytest.fixture
def assert_no_cross_identity():
    """Helper pour vérifier R&D Rule #3 (Identity Boundary)."""
    def _check(response_owner_id: str, requesting_user_id: str):
        assert response_owner_id == requesting_user_id, (
            f"Cross-identity access detected! "
            f"Owner: {response_owner_id}, Requester: {requesting_user_id}. "
            f"R&D Rule #3 violation!"
        )
        return True
    
    return _check


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES: DONNÉES DE TEST (SYNTHETIC ONLY)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def synthetic_data_marker() -> Dict[str, Any]:
    """Marque les données comme synthétiques (jamais réelles)."""
    return {
        "synthetic": True,
        "environment": "test",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "warning": "DO NOT USE IN PRODUCTION"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS PYTEST
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Configuration au démarrage de pytest."""
    # Créer le dossier de logs si nécessaire
    os.makedirs("tests/logs", exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modifier l'ordre des tests si nécessaire."""
    # Les tests critiques en premier
    critical_tests = []
    other_tests = []
    
    for item in items:
        if "critical" in item.keywords:
            critical_tests.append(item)
        else:
            other_tests.append(item)
    
    items[:] = critical_tests + other_tests


def pytest_runtest_makereport(item, call):
    """Hook pour rapport de test personnalisé."""
    if call.when == "call" and call.excinfo is not None:
        # Log les échecs avec contexte R&D
        markers = [m.name for m in item.iter_markers()]
        rd_markers = [m for m in markers if m.startswith("rd_rule_")]
        
        if rd_markers:
            print(f"\n⚠️  R&D COMPLIANCE TEST FAILED: {rd_markers}")
            print(f"    Test: {item.name}")
            print(f"    This may indicate a governance violation!")
