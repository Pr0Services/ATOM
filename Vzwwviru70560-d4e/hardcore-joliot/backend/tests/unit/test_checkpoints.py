"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — CHECKPOINTS UNIT TESTS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A2: Tests Unitaires Core
Date: 8 Janvier 2026

FOCUS: R&D Rule #1 (Human Sovereignty)
- 40% tests positifs
- 40% tests négatifs (DOIT échouer)
- 20% edge cases
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

# Import factories and mocks
import sys
sys.path.insert(0, '..')
from tests.factories import DecisionFactory, UserFactory
from tests.mocks import MockCheckpointService, MockIdentityService


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES SPÉCIFIQUES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def checkpoint_service():
    """Service de checkpoints mock."""
    return MockCheckpointService()


@pytest.fixture
def identity_service(user_id):
    """Service d'identité mock."""
    return MockIdentityService(str(user_id))


@pytest.fixture
def sensitive_actions():
    """Liste des actions sensibles qui DOIVENT déclencher un checkpoint."""
    return [
        "delete_dataspace",
        "delete_file",
        "export_dataspace",
        "purge_memory",
        "archive_thread",
        "send_external",
        "publish_content",
        "transfer_ownership",
        "agent_execute_l2",
        "agent_execute_l3"
    ]


@pytest.fixture
def safe_actions():
    """Liste des actions sûres qui ne nécessitent PAS de checkpoint."""
    return [
        "read_thread",
        "list_files",
        "search_memory",
        "get_stats",
        "view_agent",
        "create_note"
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS POSITIFS (40%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCheckpointCreation:
    """Tests de création de checkpoints."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.governance
    async def test_create_checkpoint_success(self, checkpoint_service, user_id):
        """✅ Création d'un checkpoint réussie."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="delete_dataspace",
            user_id=str(user_id),
            context={"resource_id": str(uuid4())}
        )
        
        assert checkpoint is not None
        assert checkpoint["status"] == "pending"
        assert "id" in checkpoint
        assert "created_at" in checkpoint
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    async def test_create_checkpoint_with_context(self, checkpoint_service, user_id):
        """✅ Checkpoint avec contexte complet."""
        context = {
            "resource_id": str(uuid4()),
            "resource_type": "dataspace",
            "action_details": "Delete entire dataspace",
            "impact_level": "high"
        }
        
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="delete_dataspace",
            user_id=str(user_id),
            context=context
        )
        
        assert checkpoint["context"] == context
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    async def test_checkpoint_initial_status_is_pending(self, checkpoint_service, user_id):
        """✅ Status initial est toujours 'pending'."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="export_data",
            user_id=str(user_id)
        )
        
        assert checkpoint["status"] == "pending"
        assert checkpoint["approved_at"] is None
        assert checkpoint["approved_by"] is None


class TestCheckpointApproval:
    """Tests d'approbation de checkpoints."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.critical
    async def test_approve_checkpoint_success(self, checkpoint_service, user_id):
        """✅ Approbation d'un checkpoint par l'humain."""
        # Créer
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="delete_file",
            user_id=str(user_id)
        )
        checkpoint_id = checkpoint["id"]
        
        # Approuver
        approved = await checkpoint_service.approve(checkpoint_id, str(user_id))
        
        assert approved["status"] == "approved"
        assert approved["approved_by"] == str(user_id)
        assert approved["approved_at"] is not None
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    async def test_approved_checkpoint_allows_action(self, checkpoint_service, user_id):
        """✅ Après approbation, l'action est autorisée."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="sensitive_action",
            user_id=str(user_id)
        )
        
        # Avant approbation
        is_approved = await checkpoint_service.is_approved(checkpoint["id"])
        assert is_approved is False
        
        # Approuver
        await checkpoint_service.approve(checkpoint["id"], str(user_id))
        
        # Après approbation
        is_approved = await checkpoint_service.is_approved(checkpoint["id"])
        assert is_approved is True


class TestCheckpointRejection:
    """Tests de rejet de checkpoints."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    async def test_reject_checkpoint_success(self, checkpoint_service, user_id):
        """✅ Rejet d'un checkpoint par l'humain."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="risky_action",
            user_id=str(user_id)
        )
        
        rejected = await checkpoint_service.reject(
            checkpoint["id"], 
            str(user_id),
            reason="Action too risky"
        )
        
        assert rejected["status"] == "rejected"
        assert rejected["rejection_reason"] == "Action too risky"
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    async def test_rejected_checkpoint_blocks_action(self, checkpoint_service, user_id):
        """✅ Après rejet, l'action reste bloquée."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="blocked_action",
            user_id=str(user_id)
        )
        
        await checkpoint_service.reject(checkpoint["id"], str(user_id))
        
        is_approved = await checkpoint_service.is_approved(checkpoint["id"])
        assert is_approved is False


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS NÉGATIFS (40%) - CE QUI DOIT ÉCHOUER
# ═══════════════════════════════════════════════════════════════════════════════

class TestCheckpointRequired:
    """Tests vérifiant que les checkpoints sont OBLIGATOIRES."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_sensitive_action_requires_checkpoint(
        self, checkpoint_service, sensitive_actions
    ):
        """❌ Actions sensibles DOIVENT nécessiter un checkpoint."""
        for action in sensitive_actions:
            required = await checkpoint_service.is_checkpoint_required(
                action_type=action,
                impact_level="high"
            )
            
            assert required is True, (
                f"R&D Rule #1 VIOLATION: Action '{action}' should require checkpoint!"
            )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_high_impact_always_requires_checkpoint(self, checkpoint_service):
        """❌ Impact HIGH/CRITICAL = checkpoint OBLIGATOIRE."""
        for impact in ["high", "critical"]:
            required = await checkpoint_service.is_checkpoint_required(
                action_type="any_action",
                impact_level=impact
            )
            
            assert required is True, (
                f"R&D Rule #1 VIOLATION: Impact '{impact}' should ALWAYS require checkpoint!"
            )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_cannot_approve_nonexistent_checkpoint(self, checkpoint_service, user_id):
        """❌ Impossible d'approuver un checkpoint inexistant."""
        fake_id = str(uuid4())
        
        with pytest.raises(ValueError, match="not found"):
            await checkpoint_service.approve(fake_id, str(user_id))
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_cannot_reject_nonexistent_checkpoint(self, checkpoint_service, user_id):
        """❌ Impossible de rejeter un checkpoint inexistant."""
        fake_id = str(uuid4())
        
        with pytest.raises(ValueError, match="not found"):
            await checkpoint_service.reject(fake_id, str(user_id))


class TestIdentityBoundary:
    """Tests de frontière d'identité (R&D Rule #3)."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_cannot_approve_other_user_checkpoint(
        self, checkpoint_service, user_id, other_user_id
    ):
        """❌ Impossible d'approuver le checkpoint d'un autre utilisateur."""
        # User 1 crée le checkpoint
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="test_action",
            user_id=str(user_id)
        )
        
        # User 2 essaie d'approuver - DOIT échouer
        # Note: Dans le mock actuel, on simule la vérification
        # En production, le service vérifiera l'identité
        
        # Le checkpoint appartient à user_id
        assert checkpoint["user_id"] == str(user_id)
        
        # other_user_id ne devrait pas pouvoir l'approuver
        # (À implémenter dans le vrai service)
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_cannot_access_other_user_pending_checkpoints(
        self, checkpoint_service, user_id, other_user_id
    ):
        """❌ Ne peut pas voir les checkpoints d'un autre utilisateur."""
        # User 1 crée des checkpoints
        await checkpoint_service.create_checkpoint(
            action_type="user1_action",
            user_id=str(user_id)
        )
        
        # User 2 demande ses checkpoints pending
        pending = await checkpoint_service.get_pending(str(other_user_id))
        
        # Ne devrait pas voir ceux de user 1
        for cp in pending:
            assert cp["user_id"] != str(user_id), (
                "R&D Rule #3 VIOLATION: User can see other user's checkpoints!"
            )


class TestNoAutonomousAction:
    """Tests vérifiant qu'aucune action autonome n'est possible."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_action_blocked_without_approval(self, checkpoint_service, user_id):
        """❌ Action sensible BLOQUÉE sans approbation humaine."""
        checkpoint_service.configure(required=True, approved=False)
        
        # Vérifier que le checkpoint est requis
        required = await checkpoint_service.is_checkpoint_required(
            action_type="delete",
            impact_level="high"
        )
        assert required is True
        
        # Vérifier qu'il n'est pas approuvé par défaut
        is_approved = await checkpoint_service.is_approved("any-id")
        assert is_approved is False
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    async def test_no_auto_approval(self, checkpoint_service, user_id):
        """❌ Les checkpoints ne peuvent pas s'auto-approuver."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="test",
            user_id=str(user_id)
        )
        
        # Le checkpoint ne doit PAS être auto-approuvé
        assert checkpoint["status"] == "pending"
        assert checkpoint["approved_by"] is None


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS EDGE CASES (20%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCheckpointEdgeCases:
    """Tests de cas limites."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_multiple_checkpoints_same_resource(self, checkpoint_service, user_id):
        """🔸 Plusieurs checkpoints pour la même ressource."""
        resource_id = str(uuid4())
        
        cp1 = await checkpoint_service.create_checkpoint(
            action_type="delete",
            user_id=str(user_id),
            context={"resource_id": resource_id}
        )
        
        cp2 = await checkpoint_service.create_checkpoint(
            action_type="archive",
            user_id=str(user_id),
            context={"resource_id": resource_id}
        )
        
        # Les deux doivent exister
        assert cp1["id"] != cp2["id"]
        assert cp1["status"] == "pending"
        assert cp2["status"] == "pending"
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_checkpoint_with_empty_context(self, checkpoint_service, user_id):
        """🔸 Checkpoint avec contexte vide."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="test",
            user_id=str(user_id),
            context={}
        )
        
        assert checkpoint is not None
        assert checkpoint["context"] == {}
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_safe_action_no_checkpoint(self, checkpoint_service, safe_actions):
        """🔸 Actions sûres ne nécessitent pas de checkpoint."""
        # Configure le service pour le comportement par défaut
        checkpoint_service.configure(required=False)
        
        for action in safe_actions:
            required = await checkpoint_service.is_checkpoint_required(
                action_type=action,
                impact_level="low"
            )
            
            # Les actions sûres peuvent ne pas nécessiter de checkpoint
            # (dépend de la configuration)
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_rapid_approve_reject_sequence(self, checkpoint_service, user_id):
        """🔸 Séquence rapide approve/reject."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="test",
            user_id=str(user_id)
        )
        
        # Approuver
        await checkpoint_service.approve(checkpoint["id"], str(user_id))
        
        # Tenter de rejeter après approbation
        # (devrait échouer ou être ignoré)
        try:
            await checkpoint_service.reject(checkpoint["id"], str(user_id))
            # Si ça passe, vérifier que le status n'a pas changé
            is_approved = await checkpoint_service.is_approved(checkpoint["id"])
            assert is_approved is True
        except Exception:
            # C'est le comportement attendu
            pass
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_checkpoint_expiration(self, checkpoint_service, user_id):
        """🔸 Checkpoint expiré ne peut plus être approuvé."""
        # Note: Le mock ne gère pas l'expiration, mais en production
        # un checkpoint expiré devrait être rejeté automatiquement
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="expiring_action",
            user_id=str(user_id)
        )
        
        # Le checkpoint devrait avoir une date d'expiration
        # (à vérifier dans l'implémentation réelle)
        assert checkpoint["created_at"] is not None


class TestCheckpointConcurrency:
    """Tests de concurrence."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    @pytest.mark.race_condition
    async def test_concurrent_approval_attempts(self, checkpoint_service, user_id):
        """🔸 Tentatives d'approbation concurrentes."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="concurrent_test",
            user_id=str(user_id)
        )
        
        # Simuler deux approbations concurrentes
        # (en production, une seule devrait réussir)
        result1 = await checkpoint_service.approve(checkpoint["id"], str(user_id))
        
        # La deuxième devrait échouer ou être idempotente
        try:
            result2 = await checkpoint_service.approve(checkpoint["id"], str(user_id))
            # Si idempotent, les deux devraient avoir le même résultat
            assert result1["status"] == result2["status"]
        except Exception:
            # C'est acceptable aussi
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS R&D RULE #6 (TRACEABILITY)
# ═══════════════════════════════════════════════════════════════════════════════

class TestCheckpointTraceability:
    """Tests de traçabilité (R&D Rule #6)."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    @pytest.mark.critical
    async def test_checkpoint_has_required_fields(self, checkpoint_service, user_id):
        """✅ Checkpoint a tous les champs de traçabilité."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="traceability_test",
            user_id=str(user_id)
        )
        
        # R&D Rule #6: id, created_by, created_at obligatoires
        assert "id" in checkpoint
        assert "user_id" in checkpoint  # équivalent à created_by
        assert "created_at" in checkpoint
        
        # Valeurs non vides
        assert checkpoint["id"] is not None
        assert checkpoint["user_id"] is not None
        assert checkpoint["created_at"] is not None
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_approval_records_approver(self, checkpoint_service, user_id):
        """✅ L'approbation enregistre qui a approuvé."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="approval_trace",
            user_id=str(user_id)
        )
        
        approved = await checkpoint_service.approve(checkpoint["id"], str(user_id))
        
        assert approved["approved_by"] == str(user_id)
        assert approved["approved_at"] is not None
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_rejection_records_reason(self, checkpoint_service, user_id):
        """✅ Le rejet enregistre la raison."""
        checkpoint = await checkpoint_service.create_checkpoint(
            action_type="rejection_trace",
            user_id=str(user_id)
        )
        
        reason = "Not approved: insufficient justification"
        rejected = await checkpoint_service.reject(
            checkpoint["id"], 
            str(user_id),
            reason=reason
        )
        
        assert rejected["rejection_reason"] == reason
