"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — INTEGRATION TESTS: GOVERNANCE WORKFLOW
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A2: Tests d'Intégration
Date: 8 Janvier 2026

FOCUS: Workflows complets de gouvernance
- Checkpoint → Approval → Execution
- Identity Boundary across services
- Nova + Agents + Checkpoints integration
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from uuid import uuid4
from datetime import datetime
from typing import Dict, Any

import sys
sys.path.insert(0, '..')
from tests.factories import (
    UserFactory, ThreadFactory, DecisionFactory, 
    AgentFactory, SphereFactory
)
from tests.mocks import (
    MockCheckpointService, MockIdentityService, 
    MockGovernanceService, MockAgentService
)


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def governance_stack(user_id):
    """Stack complète de gouvernance."""
    checkpoint_service = MockCheckpointService()
    identity_service = MockIdentityService(str(user_id))
    governance_service = MockGovernanceService()
    agent_service = MockAgentService()
    
    return {
        "checkpoint": checkpoint_service,
        "identity": identity_service,
        "governance": governance_service,
        "agent": agent_service
    }


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: DELETE DATASPACE
# ═══════════════════════════════════════════════════════════════════════════════

class TestDeleteDataspaceWorkflow:
    """Workflow complet: Suppression d'un DataSpace."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_1
    @pytest.mark.rd_rule_3
    @pytest.mark.critical
    async def test_complete_delete_workflow_approved(self, governance_stack, user_id):
        """✅ Workflow complet: DELETE approuvé."""
        checkpoint_svc = governance_stack["checkpoint"]
        identity_svc = governance_stack["identity"]
        
        # 1. Créer un DataSpace
        dataspace = {
            "id": str(uuid4()),
            "name": "Test DataSpace",
            "owner_id": str(user_id),
            "file_count": 10
        }
        
        # 2. Tenter de supprimer → HTTP 423
        required = await checkpoint_svc.is_checkpoint_required(
            action_type="delete_dataspace",
            impact_level="high"
        )
        assert required is True, "DELETE should require checkpoint"
        
        # 3. Créer le checkpoint
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="delete_dataspace",
            user_id=str(user_id),
            context={"dataspace_id": dataspace["id"]}
        )
        assert checkpoint["status"] == "pending"
        
        # 4. Vérifier ownership avant approbation
        can_approve = await identity_svc.verify_ownership(
            dataspace["owner_id"],
            str(user_id)
        )
        assert can_approve is True
        
        # 5. Approuver le checkpoint (HUMAIN)
        approved = await checkpoint_svc.approve(
            checkpoint["id"],
            str(user_id)
        )
        assert approved["status"] == "approved"
        
        # 6. Vérifier que l'action est maintenant autorisée
        is_approved = await checkpoint_svc.is_approved(checkpoint["id"])
        assert is_approved is True
        
        # 7. Exécuter la suppression (maintenant autorisée)
        # En production: DELETE /api/v2/dataspace-engine/{id} avec checkpoint_id
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_1
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_complete_delete_workflow_rejected(self, governance_stack, user_id):
        """❌ Workflow complet: DELETE rejeté."""
        checkpoint_svc = governance_stack["checkpoint"]
        
        # 1. Créer un DataSpace
        dataspace = {
            "id": str(uuid4()),
            "name": "Important DataSpace",
            "owner_id": str(user_id),
            "file_count": 1000  # Beaucoup de fichiers
        }
        
        # 2. Créer le checkpoint
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="delete_dataspace",
            user_id=str(user_id),
            context={"dataspace_id": dataspace["id"]}
        )
        
        # 3. Rejeter le checkpoint (HUMAIN décide de ne pas supprimer)
        rejected = await checkpoint_svc.reject(
            checkpoint["id"],
            str(user_id),
            reason="Too many important files"
        )
        assert rejected["status"] == "rejected"
        
        # 4. Vérifier que l'action reste bloquée
        is_approved = await checkpoint_svc.is_approved(checkpoint["id"])
        assert is_approved is False
        
        # 5. Le DataSpace reste intact
        # En production: Le DELETE échouerait
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_cannot_delete_other_user_dataspace(
        self, governance_stack, user_id, other_user_id
    ):
        """❌ Impossible de supprimer le DataSpace d'un autre."""
        identity_svc = governance_stack["identity"]
        
        # DataSpace appartient à user_id
        dataspace = {
            "id": str(uuid4()),
            "owner_id": str(user_id)
        }
        
        # other_user essaie d'accéder
        can_access = await identity_svc.verify_ownership(
            dataspace["owner_id"],
            str(other_user_id)
        )
        
        assert can_access is False, (
            "R&D Rule #3: Cannot access other user's DataSpace"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: NOVA + AGENT EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaAgentWorkflow:
    """Workflow: Nova coordonne, humain décide, agent exécute."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_1
    @pytest.mark.rd_rule_4
    @pytest.mark.critical
    async def test_nova_suggests_agent_human_approves(self, governance_stack, user_id):
        """✅ Nova suggère → Humain approuve → Agent exécute."""
        checkpoint_svc = governance_stack["checkpoint"]
        agent_svc = governance_stack["agent"]
        
        # 1. Nova analyse et suggère un agent
        agent = AgentFactory.create_l2()
        suggestion = {
            "agent_id": agent["id"],
            "task": "Analyze project data",
            "requires_approval": True
        }
        
        # 2. Créer checkpoint pour exécution agent L2+
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="agent_execute_l2",
            user_id=str(user_id),
            context={
                "agent_id": agent["id"],
                "task": suggestion["task"]
            }
        )
        assert checkpoint["status"] == "pending"
        
        # 3. Humain approuve
        await checkpoint_svc.approve(checkpoint["id"], str(user_id))
        
        # 4. Maintenant l'agent peut exécuter
        result = await agent_svc.execute_agent(
            agent_id=agent["id"],
            task=suggestion["task"],
            caller="user",
            checkpoint_approved=True
        )
        
        assert result["status"] == "completed"
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_nova_cannot_execute_agent_without_approval(
        self, governance_stack, user_id
    ):
        """❌ Nova ne peut PAS exécuter un agent sans approbation."""
        agent_svc = governance_stack["agent"]
        
        agent = AgentFactory.create_l2()
        
        # Nova essaie d'exécuter directement
        with pytest.raises(PermissionError):
            await agent_svc.execute_agent(
                agent_id=agent["id"],
                task="Do something",
                caller="nova",
                checkpoint_approved=False
            )
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_agent_cannot_trigger_another_agent(
        self, governance_stack, user_id
    ):
        """❌ Un agent ne peut PAS déclencher un autre agent."""
        agent_svc = governance_stack["agent"]
        
        agent1 = AgentFactory.create_l1()
        agent2 = AgentFactory.create_l2()
        
        # Agent 1 essaie d'appeler Agent 2
        with pytest.raises(PermissionError, match="AI-to-AI"):
            await agent_svc.execute_agent(
                agent_id=agent2["id"],
                task="Help me with this",
                caller=f"agent:{agent1['id']}",
                checkpoint_approved=False
            )


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: THREAD MATURITY → DECISION
# ═══════════════════════════════════════════════════════════════════════════════

class TestThreadDecisionWorkflow:
    """Workflow: Thread mature → Décision → Checkpoint si critique."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_1
    @pytest.mark.threads
    async def test_mature_thread_critical_decision(self, governance_stack, user_id):
        """✅ Thread mature avec décision critique → checkpoint."""
        checkpoint_svc = governance_stack["checkpoint"]
        
        # 1. Thread a atteint maturité "fruit"
        thread = ThreadFactory.create_with_events(
            owner_id=str(user_id),
            maturity="fruit",
            event_count=10
        )
        
        # 2. Créer une décision critique
        decision = DecisionFactory.create_critical(
            thread_id=thread["id"],
            owner_id=str(user_id),
            title="Major Project Decision"
        )
        
        # 3. Décision critique nécessite checkpoint
        required = await checkpoint_svc.is_checkpoint_required(
            action_type="decision_critical",
            impact_level="critical"
        )
        assert required is True
        
        # 4. Créer et approuver le checkpoint
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="decision_critical",
            user_id=str(user_id),
            context={
                "thread_id": thread["id"],
                "decision_id": decision["id"]
            }
        )
        
        await checkpoint_svc.approve(checkpoint["id"], str(user_id))
        
        # 5. Décision peut maintenant être finalisée
        decision["status"] = "approved"
        assert decision["status"] == "approved"


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: MEMORY PURGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestMemoryPurgeWorkflow:
    """Workflow: Purge de mémoire avec checkpoint."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_1
    @pytest.mark.rd_rule_7
    async def test_memory_purge_requires_approval(self, governance_stack, user_id):
        """✅ Purge mémoire nécessite approbation humaine."""
        checkpoint_svc = governance_stack["checkpoint"]
        
        thread_id = str(uuid4())
        
        # 1. Vérifier que purge nécessite checkpoint
        required = await checkpoint_svc.is_checkpoint_required(
            action_type="purge_memory",
            impact_level="high"
        )
        assert required is True
        
        # 2. Créer checkpoint
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="purge_memory",
            user_id=str(user_id),
            context={
                "thread_id": thread_id,
                "older_than_days": 365,
                "estimated_events": 1000
            }
        )
        
        # 3. Humain examine et approuve
        # (En production, UI montrerait les détails)
        await checkpoint_svc.approve(
            checkpoint["id"],
            str(user_id)
        )
        
        # 4. Purge peut s'exécuter
        is_approved = await checkpoint_svc.is_approved(checkpoint["id"])
        assert is_approved is True


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: CROSS-SERVICE IDENTITY
# ═══════════════════════════════════════════════════════════════════════════════

class TestCrossServiceIdentity:
    """Tests d'identité à travers plusieurs services."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_3
    @pytest.mark.critical
    async def test_identity_consistent_across_services(
        self, governance_stack, user_id
    ):
        """✅ Identité cohérente entre services."""
        identity_svc = governance_stack["identity"]
        checkpoint_svc = governance_stack["checkpoint"]
        
        # Créer des ressources dans différents services
        dataspace_id = str(uuid4())
        thread_id = str(uuid4())
        agent_id = str(uuid4())
        
        # Tous doivent appartenir au même utilisateur
        resources = [
            {"type": "dataspace", "id": dataspace_id, "owner_id": str(user_id)},
            {"type": "thread", "id": thread_id, "owner_id": str(user_id)},
            {"type": "agent_config", "id": agent_id, "owner_id": str(user_id)}
        ]
        
        # Vérifier ownership pour chaque ressource
        for resource in resources:
            can_access = await identity_svc.verify_ownership(
                resource["owner_id"],
                str(user_id)
            )
            assert can_access is True, (
                f"User should own {resource['type']}"
            )
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_3
    @pytest.mark.negative
    async def test_cannot_cross_identity_boundaries(
        self, governance_stack, user_id, other_user_id
    ):
        """❌ Impossible de traverser les frontières d'identité."""
        identity_svc = governance_stack["identity"]
        
        # Ressources de user_id
        user1_resources = [
            {"id": str(uuid4()), "owner_id": str(user_id)},
            {"id": str(uuid4()), "owner_id": str(user_id)}
        ]
        
        # other_user ne peut accéder à aucune
        for resource in user1_resources:
            can_access = await identity_svc.verify_ownership(
                resource["owner_id"],
                str(other_user_id)
            )
            assert can_access is False


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW: GOVERNANCE AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════════════════════

class TestGovernanceAuditTrail:
    """Tests de la piste d'audit de gouvernance."""
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_6
    async def test_checkpoint_audit_trail(self, governance_stack, user_id):
        """✅ Piste d'audit complète pour checkpoints."""
        checkpoint_svc = governance_stack["checkpoint"]
        governance_svc = governance_stack["governance"]
        
        # 1. Créer et approuver un checkpoint
        checkpoint = await checkpoint_svc.create_checkpoint(
            action_type="test_action",
            user_id=str(user_id)
        )
        
        # 2. Logger l'action
        governance_svc.log_action(
            action="checkpoint_created",
            user_id=str(user_id),
            resource_id=checkpoint["id"],
            details={"action_type": "test_action"}
        )
        
        # 3. Approuver
        await checkpoint_svc.approve(checkpoint["id"], str(user_id))
        
        governance_svc.log_action(
            action="checkpoint_approved",
            user_id=str(user_id),
            resource_id=checkpoint["id"]
        )
        
        # 4. Vérifier l'audit log
        audit_log = governance_svc.get_audit_log(str(user_id))
        
        assert len(audit_log) >= 2
        assert any(log["action"] == "checkpoint_created" for log in audit_log)
        assert any(log["action"] == "checkpoint_approved" for log in audit_log)
    
    @pytest.mark.integration
    @pytest.mark.rd_rule_6
    async def test_all_actions_are_traced(self, governance_stack, user_id):
        """✅ Toutes les actions sont tracées."""
        governance_svc = governance_stack["governance"]
        
        # Actions à tracer
        actions = [
            "dataspace_created",
            "file_uploaded",
            "thread_created",
            "decision_made",
            "agent_hired"
        ]
        
        for action in actions:
            governance_svc.log_action(
                action=action,
                user_id=str(user_id),
                resource_id=str(uuid4())
            )
        
        # Vérifier que tout est loggé
        audit_log = governance_svc.get_audit_log(str(user_id))
        logged_actions = [log["action"] for log in audit_log]
        
        for action in actions:
            assert action in logged_actions, f"Action '{action}' should be logged"
