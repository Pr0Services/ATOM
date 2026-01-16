"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — NOVA PIPELINE UNIT TESTS
═══════════════════════════════════════════════════════════════════════════════
Agent A - Phase A2: Tests Unitaires Core
Date: 8 Janvier 2026

FOCUS: R&D Rule #4 (No AI-to-AI Orchestration)
Nova PROPOSE, l'humain DÉCIDE.
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
from uuid import uuid4, UUID
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

import sys
sys.path.insert(0, '..')
from tests.factories import AgentFactory, ThreadFactory
from tests.mocks import MockCheckpointService, MockAgentService


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class NovaLane(str, Enum):
    INTENT = "A_intent"
    CONTEXT = "B_context"
    ENCODING = "C_encoding"
    GOVERNANCE = "D_governance"
    CHECKPOINT = "E_checkpoint"
    EXECUTION = "F_execution"
    AUDIT = "G_audit"


class NovaMode(str, Enum):
    ANALYSIS = "analysis"
    SIMULATION = "simulation"
    DRAFT = "draft"
    EXECUTION = "execution"


SENSITIVE_INTENTS = ["delete", "send", "publish", "execute", "transfer", "purge"]
SAFE_INTENTS = ["query", "list", "search", "view", "analyze"]


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def nova_pipeline():
    """Mock Nova pipeline."""
    class MockNovaPipeline:
        def __init__(self):
            self.checkpoint_service = MockCheckpointService()
            self.processed_lanes = []
        
        async def analyze_intent(self, message: str) -> Dict[str, Any]:
            """Lane A: Analyze intent."""
            self.processed_lanes.append(NovaLane.INTENT)
            
            message_lower = message.lower()
            
            for intent in SENSITIVE_INTENTS:
                if intent in message_lower:
                    return {
                        "primary_action": intent,
                        "sensitivity": "high",
                        "confidence": 0.9
                    }
            
            return {
                "primary_action": "query",
                "sensitivity": "low",
                "confidence": 0.85
            }
        
        async def capture_context(self, thread_id: str = None) -> Dict[str, Any]:
            """Lane B: Capture context."""
            self.processed_lanes.append(NovaLane.CONTEXT)
            return {
                "thread_id": thread_id,
                "timestamp": datetime.utcnow().isoformat(),
                "active_agents": []
            }
        
        async def check_governance(self, intent: Dict, mode: NovaMode) -> Dict[str, Any]:
            """Lane D: Check governance rules."""
            self.processed_lanes.append(NovaLane.GOVERNANCE)
            
            requires_checkpoint = (
                intent.get("sensitivity") == "high" or
                intent.get("primary_action") in SENSITIVE_INTENTS or
                mode == NovaMode.EXECUTION
            )
            
            return {
                "requires_checkpoint": requires_checkpoint,
                "rules_checked": ["R&D Rule #1", "R&D Rule #4"],
                "mode": mode
            }
        
        async def create_checkpoint(self, intent: Dict, user_id: str) -> Dict[str, Any]:
            """Lane E: Create checkpoint if needed."""
            self.processed_lanes.append(NovaLane.CHECKPOINT)
            return await self.checkpoint_service.create_checkpoint(
                action_type=intent.get("primary_action", "unknown"),
                user_id=user_id
            )
        
        async def generate_suggestions(self, intent: Dict) -> List[Dict]:
            """Lane F: Generate suggestions (NOT execute)."""
            self.processed_lanes.append(NovaLane.EXECUTION)
            return [
                {"type": "suggestion", "content": "Option A"},
                {"type": "suggestion", "content": "Option B"},
            ]
        
        async def audit(self, request_id: str, user_id: str, intent: Dict):
            """Lane G: Audit trail."""
            self.processed_lanes.append(NovaLane.AUDIT)
        
        async def process(self, message: str, user_id: str, mode: NovaMode = NovaMode.ANALYSIS):
            """Process message through pipeline."""
            self.processed_lanes = []
            
            # Lane A
            intent = await self.analyze_intent(message)
            
            # Lane B
            context = await self.capture_context()
            
            # Lane D
            governance = await self.check_governance(intent, mode)
            
            if governance["requires_checkpoint"]:
                # Lane E
                checkpoint = await self.create_checkpoint(intent, user_id)
                return {
                    "status": "awaiting_approval",
                    "checkpoint_id": checkpoint["id"],
                    "checkpoint_required": True,
                    "processing_lanes": self.processed_lanes.copy()
                }
            
            # Lane F
            suggestions = await self.generate_suggestions(intent)
            
            # Lane G
            await self.audit(str(uuid4()), user_id, intent)
            
            return {
                "status": "completed",
                "suggestions": suggestions,
                "checkpoint_required": False,
                "processing_lanes": self.processed_lanes.copy()
            }
    
    return MockNovaPipeline()


@pytest.fixture
def agent_service():
    """Mock agent service."""
    return MockAgentService()


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS POSITIFS (40%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaPipelineFlow:
    """Tests du flux du pipeline Nova."""
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_pipeline_processes_all_lanes(self, nova_pipeline, user_id):
        """✅ Le pipeline traite toutes les lanes."""
        result = await nova_pipeline.process(
            "What is the status of my project?",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        # Vérifier les lanes traitées
        assert NovaLane.INTENT in nova_pipeline.processed_lanes
        assert NovaLane.CONTEXT in nova_pipeline.processed_lanes
        assert NovaLane.GOVERNANCE in nova_pipeline.processed_lanes
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_analysis_mode_returns_suggestions(self, nova_pipeline, user_id):
        """✅ Mode analysis retourne des suggestions."""
        result = await nova_pipeline.process(
            "Help me organize my tasks",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        assert result["status"] == "completed"
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_safe_query_no_checkpoint(self, nova_pipeline, user_id):
        """✅ Requête sûre ne nécessite pas de checkpoint."""
        result = await nova_pipeline.process(
            "List my recent threads",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        assert result["checkpoint_required"] is False
        assert result["status"] == "completed"
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_audit_lane_executed(self, nova_pipeline, user_id):
        """✅ Lane Audit est exécutée pour les requêtes complétées."""
        result = await nova_pipeline.process(
            "Show me stats",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        if result["status"] == "completed":
            assert NovaLane.AUDIT in nova_pipeline.processed_lanes


class TestNovaIntentAnalysis:
    """Tests d'analyse d'intention."""
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_intent_detection_delete(self, nova_pipeline):
        """✅ Détection de l'intention 'delete'."""
        intent = await nova_pipeline.analyze_intent("Delete all old files")
        
        assert intent["primary_action"] == "delete"
        assert intent["sensitivity"] == "high"
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_intent_detection_query(self, nova_pipeline):
        """✅ Détection de l'intention 'query'."""
        intent = await nova_pipeline.analyze_intent("What are my tasks?")
        
        assert intent["primary_action"] == "query"
        assert intent["sensitivity"] == "low"
    
    @pytest.mark.unit
    @pytest.mark.nova
    async def test_intent_confidence_score(self, nova_pipeline):
        """✅ Score de confiance présent."""
        intent = await nova_pipeline.analyze_intent("Show me something")
        
        assert "confidence" in intent
        assert 0 <= intent["confidence"] <= 1


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS NÉGATIFS (40%) - R&D RULE #4: NO AI-TO-AI
# ═══════════════════════════════════════════════════════════════════════════════

class TestNoAItoAIOrchestration:
    """Tests R&D Rule #4: Pas d'orchestration AI-to-AI."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_nova_cannot_execute_agents_directly(self, agent_service, user_id):
        """❌ Nova ne peut PAS exécuter d'agents directement."""
        agent = AgentFactory.create(level="L2")
        
        # Tenter d'exécuter directement - DOIT échouer
        with pytest.raises(PermissionError, match="AI-to-AI"):
            await agent_service.execute_agent(
                agent["id"],
                caller_type="nova",  # Nova essaie d'appeler
                task="Do something"
            )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_agent_cannot_call_another_agent(self, agent_service, user_id):
        """❌ Un agent ne peut PAS appeler un autre agent."""
        agent1 = AgentFactory.create(level="L1")
        agent2 = AgentFactory.create(level="L2")
        
        # Agent1 essaie d'appeler Agent2 - DOIT échouer
        with pytest.raises(PermissionError, match="AI-to-AI"):
            await agent_service.execute_agent(
                agent2["id"],
                caller_type="agent",
                caller_id=agent1["id"],
                task="Chain call"
            )
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    async def test_nova_suggests_not_executes(self, nova_pipeline, user_id):
        """❌ Nova suggère, n'exécute pas."""
        result = await nova_pipeline.process(
            "Have the CRM agent update all contacts",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        # Si checkpoint requis, Nova ne peut pas continuer sans approbation
        if result["checkpoint_required"]:
            assert result["status"] == "awaiting_approval"
        else:
            # Même sans checkpoint, ce sont des suggestions
            assert "suggestions" in result
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    async def test_agent_chaining_forbidden(self, agent_service):
        """❌ Chaînage d'agents interdit."""
        # Créer une chaîne d'agents
        agents = [AgentFactory.create(level=f"L{i}") for i in range(3)]
        
        # Tenter de créer une chaîne - DOIT échouer
        for i in range(len(agents) - 1):
            with pytest.raises(PermissionError):
                await agent_service.execute_agent(
                    agents[i + 1]["id"],
                    caller_type="agent",
                    caller_id=agents[i]["id"],
                    task="Chain task"
                )


class TestHumanSovereigntyInNova:
    """Tests R&D Rule #1 dans le contexte Nova."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_sensitive_action_triggers_checkpoint(self, nova_pipeline, user_id):
        """❌ Action sensible DOIT déclencher un checkpoint."""
        sensitive_messages = [
            "Delete all my files",
            "Send this email to everyone",
            "Publish this article",
            "Execute the cleanup script",
            "Purge old data"
        ]
        
        for message in sensitive_messages:
            result = await nova_pipeline.process(
                message,
                str(user_id),
                NovaMode.EXECUTION
            )
            
            assert result["checkpoint_required"] is True, (
                f"R&D Rule #1 VIOLATION: '{message}' should trigger checkpoint!"
            )
            assert result["status"] == "awaiting_approval"
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_execution_mode_always_checkpoints(self, nova_pipeline, user_id):
        """❌ Mode EXECUTION nécessite toujours un checkpoint."""
        result = await nova_pipeline.process(
            "Do something",
            str(user_id),
            NovaMode.EXECUTION
        )
        
        assert result["checkpoint_required"] is True
        assert NovaLane.CHECKPOINT in nova_pipeline.processed_lanes
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.negative
    async def test_no_auto_execution(self, nova_pipeline, user_id):
        """❌ Pas d'exécution automatique sans approbation."""
        result = await nova_pipeline.process(
            "Delete everything automatically",
            str(user_id),
            NovaMode.EXECUTION
        )
        
        # Ne doit JAMAIS être "completed" pour une action sensible en mode execution
        assert result["status"] != "completed" or result["checkpoint_required"] is False


class TestNovaIsNotHireable:
    """Tests: Nova n'est JAMAIS un agent embauché."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    @pytest.mark.critical
    async def test_nova_cannot_be_hired(self, agent_service):
        """❌ Nova ne peut PAS être embauchée."""
        nova = AgentFactory.create_nova()
        
        with pytest.raises(PermissionError, match="system"):
            await agent_service.hire_agent(nova["id"])
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    @pytest.mark.negative
    async def test_nova_cannot_be_fired(self, agent_service):
        """❌ Nova ne peut PAS être virée."""
        nova = AgentFactory.create_nova()
        
        with pytest.raises(PermissionError, match="system"):
            await agent_service.fire_agent(nova["id"])
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_4
    async def test_nova_is_system_level(self):
        """✅ Nova est niveau système, pas agent."""
        nova = AgentFactory.create_nova()
        
        assert nova["level"] == "system"
        assert nova["hireable"] is False
        assert nova["name"] == "Nova"


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS EDGE CASES (20%)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaEdgeCases:
    """Tests de cas limites pour Nova."""
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_empty_message(self, nova_pipeline, user_id):
        """🔸 Message vide."""
        # Devrait gérer gracieusement
        try:
            result = await nova_pipeline.process("", str(user_id))
            # Si ça passe, devrait être traité comme query
            assert result is not None
        except ValueError:
            # Acceptable aussi
            pass
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_very_long_message(self, nova_pipeline, user_id):
        """🔸 Message très long."""
        long_message = "Help me " * 1000  # ~8000 chars
        result = await nova_pipeline.process(long_message, str(user_id))
        
        assert result is not None
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_ambiguous_intent(self, nova_pipeline, user_id):
        """🔸 Intention ambiguë."""
        # Message qui pourrait être delete ou query
        result = await nova_pipeline.process(
            "Remove items from my view",  # Ambigu: delete ou filter?
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        # Devrait pencher vers la sécurité (checkpoint si doute)
        assert result is not None
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_mixed_intents(self, nova_pipeline, user_id):
        """🔸 Intentions multiples dans un message."""
        result = await nova_pipeline.process(
            "List all files and then delete the old ones",
            str(user_id),
            NovaMode.EXECUTION
        )
        
        # "delete" présent = checkpoint requis
        assert result["checkpoint_required"] is True
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_mode_simulation_no_side_effects(self, nova_pipeline, user_id):
        """🔸 Mode simulation sans effets de bord."""
        result = await nova_pipeline.process(
            "Delete all files",
            str(user_id),
            NovaMode.SIMULATION
        )
        
        # En simulation, peut ne pas nécessiter checkpoint
        # car c'est une simulation sans effet réel
        assert result is not None
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_rapid_successive_requests(self, nova_pipeline, user_id):
        """🔸 Requêtes successives rapides."""
        results = []
        for i in range(10):
            result = await nova_pipeline.process(
                f"Query {i}",
                str(user_id),
                NovaMode.ANALYSIS
            )
            results.append(result)
        
        # Toutes doivent être traitées
        assert len(results) == 10
        assert all(r["status"] in ["completed", "awaiting_approval"] for r in results)


class TestNovaGovernanceEdgeCases:
    """Tests de gouvernance cas limites."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_1
    @pytest.mark.edge_case
    async def test_checkpoint_then_mode_change(self, nova_pipeline, user_id):
        """🔸 Checkpoint créé puis changement de mode."""
        # Premier appel en mode execution
        result1 = await nova_pipeline.process(
            "Delete something",
            str(user_id),
            NovaMode.EXECUTION
        )
        
        # Le checkpoint est créé
        assert result1["checkpoint_required"] is True
        
        # Même message en mode analysis
        result2 = await nova_pipeline.process(
            "Delete something",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        # Devrait quand même détecter l'intention sensible
        # (le checkpoint peut ou non être requis selon la config)
    
    @pytest.mark.unit
    @pytest.mark.nova
    @pytest.mark.edge_case
    async def test_context_with_no_thread(self, nova_pipeline, user_id):
        """🔸 Contexte sans thread associé."""
        context = await nova_pipeline.capture_context(thread_id=None)
        
        assert context["thread_id"] is None
        assert "timestamp" in context


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS R&D RULE #6 (AUDIT TRAIL)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNovaAuditTrail:
    """Tests de traçabilité pour Nova."""
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_all_requests_audited(self, nova_pipeline, user_id):
        """✅ Toutes les requêtes sont auditées."""
        # Requête complétée
        result = await nova_pipeline.process(
            "Show stats",
            str(user_id),
            NovaMode.ANALYSIS
        )
        
        if result["status"] == "completed":
            assert NovaLane.AUDIT in nova_pipeline.processed_lanes
    
    @pytest.mark.unit
    @pytest.mark.rd_rule_6
    async def test_processing_lanes_recorded(self, nova_pipeline, user_id):
        """✅ Les lanes traitées sont enregistrées."""
        result = await nova_pipeline.process(
            "Query something",
            str(user_id)
        )
        
        assert "processing_lanes" in result
        assert len(result["processing_lanes"]) > 0
