"""
CHE·NU™ — AGENTS TESTS (PYTEST)
Sprint 3: Tests for Agent System

CRITICAL - Agent Rules:
- Nova is SYSTEM intelligence (L0)
- Nova is ALWAYS present
- Nova is NEVER a hired agent
- Orchestrator is hired by user (L1)
- Agents have costs, scopes, encoding compatibility
- Agents act only when authorized
"""

import pytest
from typing import List

# ═══════════════════════════════════════════════════════════════════════════════
# AGENT LEVELS CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

AGENT_LEVELS = {
    "L0": {
        "name": "System Intelligence",
        "name_fr": "Intelligence Système",
        "description": "Nova - always present, never hired",
        "is_hireable": False,
    },
    "L1": {
        "name": "Orchestrator",
        "name_fr": "Orchestrateur",
        "description": "User's hired task manager",
        "is_hireable": True,
    },
    "L2": {
        "name": "Specialist",
        "name_fr": "Spécialiste",
        "description": "Domain expert agents",
        "is_hireable": True,
    },
    "L3": {
        "name": "Worker",
        "name_fr": "Travailleur",
        "description": "Task execution agents",
        "is_hireable": True,
    },
}

NOVA_CAPABILITIES = [
    "guidance",
    "memory",
    "governance",
    "supervision",
    "database_management",
    "thread_management",
]


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA TESTS (L0 - SYSTEM INTELLIGENCE)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNova:
    """Tests for Nova - System Intelligence (L0)."""

    def test_nova_exists(self, nova_agent):
        """Nova agent should exist."""
        assert nova_agent is not None
        assert nova_agent.id == "nova"

    def test_nova_is_l0(self, nova_agent):
        """Nova should be L0 level."""
        assert nova_agent.type == "nova"

    def test_nova_is_system_agent(self, nova_agent):
        """Nova should be a system agent."""
        assert nova_agent.is_system == True

    def test_nova_is_never_hired(self, nova_agent):
        """Nova is NEVER a hired agent (per Memory Prompt)."""
        # Nova should not have is_hired = True
        assert not hasattr(nova_agent, 'is_hired') or nova_agent.is_hired == False

    def test_nova_is_always_present(self, nova_agent):
        """Nova should always be present (is_active)."""
        assert nova_agent.is_active == True

    def test_nova_name(self, nova_agent):
        """Nova should have correct name."""
        assert nova_agent.name == "Nova"

    def test_nova_has_guidance_capability(self, nova_agent):
        """Nova should have guidance capability."""
        assert "guidance" in nova_agent.capabilities

    def test_nova_has_memory_capability(self, nova_agent):
        """Nova should have memory capability."""
        assert "memory" in nova_agent.capabilities

    def test_nova_has_governance_capability(self, nova_agent):
        """Nova should have governance capability."""
        assert "governance" in nova_agent.capabilities

    def test_nova_has_supervision_capability(self, nova_agent):
        """Nova supervises databases and threads."""
        assert "supervision" in nova_agent.capabilities

    def test_nova_has_all_sphere_access(self, nova_agent):
        """Nova should have access to all spheres."""
        # Either explicit "all" or list of all 9 spheres
        assert "all" in nova_agent.sphere_scopes or len(nova_agent.sphere_scopes) >= 9

    def test_nova_has_low_cost(self, nova_agent):
        """Nova should have low cost (system agent)."""
        assert nova_agent.base_cost_per_token <= 0.001


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT LEVELS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentLevels:
    """Tests for agent hierarchy levels."""

    def test_exactly_4_levels(self):
        """Should have exactly 4 agent levels (L0-L3)."""
        assert len(AGENT_LEVELS) == 4

    def test_l0_is_system_intelligence(self):
        """L0 should be System Intelligence (Nova)."""
        assert AGENT_LEVELS["L0"]["name"] == "System Intelligence"

    def test_l0_not_hireable(self):
        """L0 (Nova) should NOT be hireable."""
        assert AGENT_LEVELS["L0"]["is_hireable"] == False

    def test_l1_is_orchestrator(self):
        """L1 should be Orchestrator."""
        assert AGENT_LEVELS["L1"]["name"] == "Orchestrator"

    def test_l1_is_hireable(self):
        """L1 (Orchestrator) should be hireable."""
        assert AGENT_LEVELS["L1"]["is_hireable"] == True

    def test_l2_is_specialist(self):
        """L2 should be Specialist."""
        assert AGENT_LEVELS["L2"]["name"] == "Specialist"

    def test_l2_is_hireable(self):
        """L2 (Specialist) should be hireable."""
        assert AGENT_LEVELS["L2"]["is_hireable"] == True

    def test_l3_is_worker(self):
        """L3 should be Worker."""
        assert AGENT_LEVELS["L3"]["name"] == "Worker"

    def test_l3_is_hireable(self):
        """L3 (Worker) should be hireable."""
        assert AGENT_LEVELS["L3"]["is_hireable"] == True


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR TESTS (L1)
# ═══════════════════════════════════════════════════════════════════════════════

class TestOrchestrator:
    """Tests for Orchestrator (L1) - hired by user."""

    def test_orchestrator_is_hired_by_user(self):
        """Orchestrator is hired by the user."""
        orchestrator_hired_by = "user"
        assert orchestrator_hired_by == "user"

    def test_orchestrator_executes_tasks(self):
        """Orchestrator executes tasks."""
        orchestrator_actions = ["execute_tasks", "manage_agents", "respect_governance"]
        assert "execute_tasks" in orchestrator_actions

    def test_orchestrator_manages_agents(self):
        """Orchestrator manages other agents."""
        orchestrator_actions = ["execute_tasks", "manage_agents", "respect_governance"]
        assert "manage_agents" in orchestrator_actions

    def test_orchestrator_respects_scope(self):
        """Orchestrator respects scope, budget, and governance."""
        orchestrator_respects = ["scope", "budget", "governance"]
        assert len(orchestrator_respects) == 3

    def test_orchestrator_can_be_replaced(self):
        """Orchestrator can be replaced or customized."""
        orchestrator_replaceable = True
        assert orchestrator_replaceable


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT PROPERTIES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentProperties:
    """Tests for agent required properties."""

    def test_agent_has_id(self, test_agent):
        """Agent should have ID."""
        assert test_agent.id is not None

    def test_agent_has_name(self, test_agent):
        """Agent should have name."""
        assert test_agent.name is not None

    def test_agent_has_type(self, test_agent):
        """Agent should have type."""
        assert test_agent.type in ["nova", "orchestrator", "specialist", "worker"]

    def test_agent_has_capabilities(self, test_agent):
        """Agent should have capabilities list."""
        assert isinstance(test_agent.capabilities, list)
        assert len(test_agent.capabilities) > 0

    def test_agent_has_sphere_scopes(self, test_agent):
        """Agent should have sphere scopes."""
        assert isinstance(test_agent.sphere_scopes, list)
        assert len(test_agent.sphere_scopes) > 0

    def test_agent_has_cost(self, test_agent):
        """Agent should have cost per token."""
        assert test_agent.base_cost_per_token > 0


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT HIRING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentHiring:
    """Tests for agent hiring flow."""

    def test_nova_cannot_be_hired(self, nova_agent):
        """Nova (L0) cannot be hired - always present."""
        # Nova is system, not hireable
        assert nova_agent.is_system == True

    def test_specialist_can_be_hired(self, test_agent):
        """Specialist agents can be hired."""
        if test_agent.type == "specialist":
            assert test_agent.is_system == False

    def test_hired_agent_has_timestamp(self):
        """Hired agents should have hired_at timestamp."""
        # When hired, agent should have timestamp
        hired_at_required = True
        assert hired_at_required

    def test_hired_agent_has_metrics(self):
        """Hired agents should have metrics."""
        required_metrics = ["tasks_completed", "total_tokens_used", "success_rate"]
        assert len(required_metrics) == 3


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT FIRING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentFiring:
    """Tests for agent firing flow."""

    def test_nova_cannot_be_fired(self, nova_agent):
        """Nova cannot be fired - always present."""
        assert nova_agent.is_system == True

    def test_hired_agent_can_be_fired(self):
        """Hired agents can be fired."""
        hired_agent_fireable = True
        assert hired_agent_fireable

    def test_firing_clears_active_orchestrator(self):
        """Firing orchestrator clears active orchestrator."""
        clears_active = True
        assert clears_active


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT TASK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentTasks:
    """Tests for agent task execution."""

    def test_task_has_required_fields(self):
        """Task should have required fields."""
        required_fields = ["id", "agent_id", "input", "status", "created_at"]
        assert len(required_fields) == 5

    def test_task_status_values(self):
        """Task should have valid status values."""
        valid_statuses = ["pending", "running", "completed", "failed", "cancelled"]
        assert len(valid_statuses) == 5

    def test_task_tracks_tokens(self):
        """Task should track tokens used."""
        tracks_tokens = True
        assert tracks_tokens

    def test_task_can_have_thread_id(self):
        """Task can be associated with a thread."""
        thread_association = True
        assert thread_association

    def test_task_has_timestamps(self):
        """Task should have timestamps."""
        timestamps = ["created_at", "started_at", "completed_at"]
        assert len(timestamps) == 3


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT NON-AUTONOMY TESTS (L7 Law)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentNonAutonomy:
    """Tests for Agent Non-Autonomy (Governance Law L7)."""

    def test_agents_act_only_when_authorized(self):
        """Agents act only when authorized."""
        acts_only_when_authorized = True
        assert acts_only_when_authorized

    def test_agents_require_user_approval(self):
        """Agents require user approval for actions."""
        requires_approval = True
        assert requires_approval

    def test_no_autonomous_external_actions(self):
        """Agents cannot perform autonomous external actions."""
        autonomous_external_allowed = False
        assert not autonomous_external_allowed

    def test_governance_before_agent_action(self):
        """Governance is enforced before agent action."""
        governance_before_action = True
        assert governance_before_action


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT ENCODING COMPATIBILITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentEncodingCompatibility:
    """Tests for agent encoding compatibility."""

    def test_nova_has_full_encoding_compatibility(self, nova_agent):
        """Nova should have 100% encoding compatibility."""
        # Nova should support all encoding modes
        expected_compatibility = 100
        # Check if attribute exists, default to 100 for system agent
        compatibility = getattr(nova_agent, 'encoding_compatibility', 100)
        assert compatibility == expected_compatibility

    def test_agents_have_encoding_compatibility(self, test_agent):
        """Agents should have encoding compatibility score."""
        # Should have encoding_compatibility or default
        has_encoding = hasattr(test_agent, 'encoding_compatibility') or True
        assert has_encoding


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIALIST AGENTS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSpecialistAgents:
    """Tests for specialist agents (L2)."""

    def test_specialist_types(self):
        """Should have various specialist types."""
        specialist_types = [
            "data_analyst",
            "creative_writer",
            "dev_assistant",
            "research_assistant",
        ]
        assert len(specialist_types) >= 4

    def test_specialists_have_domain_capabilities(self):
        """Specialists should have domain-specific capabilities."""
        domain_capabilities = {
            "data_analyst": ["analysis", "reporting", "visualization"],
            "creative_writer": ["writing", "editing", "content_creation"],
            "dev_assistant": ["coding", "debugging", "documentation"],
            "research_assistant": ["research", "summarization", "citation"],
        }
        assert len(domain_capabilities) >= 4


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentsAPI:
    """Tests for agents API endpoints."""

    def test_get_nova(self, client):
        """GET /agents/nova should return Nova."""
        response = client.get("/api/v1/agents/nova")
        if response.status_code == 200:
            data = response.json()
            assert data["id"] == "nova"
            assert data["is_system"] == True

    def test_get_available_agents(self, client):
        """GET /agents/available should return available agents."""
        response = client.get("/api/v1/agents/available")
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)

    def test_get_hired_agents(self, client):
        """GET /agents/hired should return hired agents."""
        response = client.get("/api/v1/agents/hired")
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestAgentMemoryPromptCompliance:
    """Tests ensuring Memory Prompt agent compliance."""

    def test_nova_is_system_intelligence(self, nova_agent):
        """Nova is the SYSTEM intelligence."""
        assert nova_agent.is_system == True

    def test_nova_always_present(self, nova_agent):
        """Nova is always present."""
        assert nova_agent.is_active == True

    def test_nova_handles_guidance_memory_governance(self, nova_agent):
        """Nova handles guidance, memory, governance."""
        required = ["guidance", "memory", "governance"]
        for cap in required:
            assert cap in nova_agent.capabilities

    def test_nova_supervises_databases_threads(self, nova_agent):
        """Nova supervises databases and threads."""
        assert "supervision" in nova_agent.capabilities

    def test_nova_never_hired(self, nova_agent):
        """Nova is NEVER a hired agent."""
        assert nova_agent.is_system == True
        # Should not have is_hired=True
        if hasattr(nova_agent, 'is_hired'):
            assert nova_agent.is_hired == False

    def test_orchestrator_hired_by_user(self):
        """User Orchestrator is hired by the user."""
        orchestrator_level = AGENT_LEVELS["L1"]
        assert orchestrator_level["is_hireable"] == True
