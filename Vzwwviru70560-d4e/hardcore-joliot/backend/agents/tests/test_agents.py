"""
============================================================================
CHE·NU™ V69 — AGENT FRAMEWORK TESTS
============================================================================
Version: 1.0.0
Purpose: Test agent hierarchy, checkpoints, and communication
============================================================================
"""

import pytest
from datetime import datetime

from ..core.models import (
    Agent,
    AgentLevel,
    AgentStatus,
    AgentCapability,
    AgentAction,
    ActionType,
    ActionStatus,
    Checkpoint,
    CheckpointType,
    CheckpointStatus,
    AgentMessage,
    MessagePriority,
    AgentContext,
    AgentTask,
)
from ..levels.hierarchy import (
    BaseAgent,
    L0SystemAgent,
    L1OrchestratorAgent,
    L2SpecialistAgent,
    L3AssistantAgent,
    create_agent,
)
from ..checkpoints.manager import (
    CheckpointManager,
    CheckpointRule,
    HITLController,
)
from ..communication.messaging import (
    MessageBus,
    MessageFactory,
    MessageProtocol,
)
from ..registry.registry import (
    AgentRegistry,
    CHENUAgentFactory,
    create_standard_agents,
)


# ============================================================================
# MODEL TESTS
# ============================================================================

class TestModels:
    """Test core agent models"""
    
    def test_create_agent(self):
        agent = Agent(
            name="Test Agent",
            level=AgentLevel.L2,
            sphere="Business",
        )
        
        assert agent.name == "Test Agent"
        assert agent.level == AgentLevel.L2
        assert agent.status == AgentStatus.INITIALIZING
    
    def test_agent_capability(self):
        cap = AgentCapability(
            name="Read Operations",
            allowed_actions={ActionType.READ},
            allowed_spheres={"Business", "Finance"},
            max_impact=0.5,
        )
        
        assert ActionType.READ in cap.allowed_actions
        assert "Business" in cap.allowed_spheres
    
    def test_agent_action(self):
        action = AgentAction(
            agent_id="agent-001",
            action_type=ActionType.READ,
            target="data.financial",
            estimated_impact=0.3,
        )
        
        assert action.status == ActionStatus.PENDING
        assert action.estimated_impact == 0.3
    
    def test_checkpoint(self):
        checkpoint = Checkpoint(
            agent_id="agent-001",
            action_id="action-001",
            checkpoint_type=CheckpointType.HITL,
            reason="High impact action",
        )
        
        assert checkpoint.status == CheckpointStatus.PENDING
        assert not checkpoint.is_resolved
    
    def test_agent_message(self):
        msg = AgentMessage(
            from_agent_id="agent-001",
            to_agent_id="agent-002",
            message_type="request",
            subject="Task Assignment",
            body={"task_id": "task-001"},
        )
        
        assert msg.priority == MessagePriority.NORMAL
        assert not msg.delivered


# ============================================================================
# AGENT HIERARCHY TESTS
# ============================================================================

class TestAgentHierarchy:
    """Test L0-L3 agent hierarchy"""
    
    def test_create_l0_agent(self):
        agent_model = Agent(
            name="Nova-System",
            level=AgentLevel.L0,
        )
        agent = L0SystemAgent(agent_model)
        
        assert agent.level == AgentLevel.L0
        assert agent_model.name == "Nova-System"
    
    def test_create_l1_agent(self):
        agent_model = Agent(
            name="Orchestrator",
            level=AgentLevel.L1,
        )
        agent = L1OrchestratorAgent(agent_model)
        
        assert agent.level == AgentLevel.L1
    
    def test_create_l2_agent(self):
        agent_model = Agent(
            name="Finance Specialist",
            level=AgentLevel.L2,
            sphere="Finance",
        )
        agent = L2SpecialistAgent(agent_model, domain="Finance")
        
        assert agent.level == AgentLevel.L2
        assert agent.domain == "Finance"
    
    def test_create_l3_agent(self):
        agent_model = Agent(
            name="User Assistant",
            level=AgentLevel.L3,
        )
        agent = L3AssistantAgent(agent_model)
        
        assert agent.level == AgentLevel.L3
    
    def test_factory_function(self):
        agent = create_agent(
            name="Test Agent",
            level=AgentLevel.L2,
            sphere="Business",
        )
        
        assert isinstance(agent, L2SpecialistAgent)
        assert agent.level == AgentLevel.L2
    
    def test_agent_activation(self):
        agent = create_agent("Test", AgentLevel.L3)
        
        assert agent.agent.status == AgentStatus.INITIALIZING
        
        agent.activate()
        assert agent.agent.status == AgentStatus.ACTIVE
        
        agent.pause()
        assert agent.agent.status == AgentStatus.PAUSED
        
        agent.terminate()
        assert agent.agent.status == AgentStatus.TERMINATED


# ============================================================================
# ACTION EXECUTION TESTS
# ============================================================================

class TestActionExecution:
    """Test agent action execution"""
    
    def test_l0_health_check(self):
        agent_model = Agent(
            name="Nova",
            level=AgentLevel.L0,
            capabilities=[AgentCapability(
                name="System",
                allowed_actions={ActionType.READ, ActionType.EXECUTE},
            )],
        )
        agent = L0SystemAgent(agent_model)
        agent.activate()
        
        result = agent.health_check()
        
        assert "status" in result
    
    def test_l2_analysis(self):
        agent_model = Agent(
            name="Analyst",
            level=AgentLevel.L2,
            capabilities=[AgentCapability(
                name="Analysis",
                allowed_actions={ActionType.READ, ActionType.WRITE},
            )],
        )
        agent = L2SpecialistAgent(agent_model, domain="Finance")
        agent.activate()
        
        result = agent.analyze("financial_data")
        
        assert "domain" in result
        assert result["domain"] == "Finance"
    
    def test_l3_user_response(self):
        agent_model = Agent(
            name="Assistant",
            level=AgentLevel.L3,
            capabilities=[AgentCapability(
                name="Communication",
                allowed_actions={ActionType.COMMUNICATE, ActionType.READ},
            )],
        )
        agent = L3AssistantAgent(agent_model)
        agent.activate()
        
        result = agent.respond_to_user("Hello!")
        
        assert "message" in result
        assert result["delivered"]


# ============================================================================
# CHECKPOINT TESTS
# ============================================================================

class TestCheckpoints:
    """Test checkpoint system"""
    
    def test_checkpoint_manager(self):
        manager = CheckpointManager()
        
        action = AgentAction(
            agent_id="agent-001",
            action_type=ActionType.EXECUTE,
            target="sensitive_operation",
            estimated_impact=0.9,  # High impact
        )
        
        checkpoint = manager.create_if_needed(action)
        
        assert checkpoint is not None
        assert checkpoint.status == CheckpointStatus.PENDING
    
    def test_checkpoint_approval(self):
        manager = CheckpointManager()
        
        checkpoint = manager.create_checkpoint(
            agent_id="agent-001",
            action_id="action-001",
            checkpoint_type=CheckpointType.APPROVAL,
            reason="Test checkpoint",
        )
        
        manager.approve(checkpoint.checkpoint_id, "admin", "Approved for testing")
        
        updated = manager.get_checkpoint(checkpoint.checkpoint_id)
        assert updated.status == CheckpointStatus.APPROVED
        assert updated.resolved_by == "admin"
    
    def test_checkpoint_denial(self):
        manager = CheckpointManager()
        
        checkpoint = manager.create_checkpoint(
            agent_id="agent-001",
            action_id="action-001",
            checkpoint_type=CheckpointType.HITL,
            reason="High risk action",
        )
        
        manager.deny(checkpoint.checkpoint_id, "admin", "Too risky")
        
        updated = manager.get_checkpoint(checkpoint.checkpoint_id)
        assert updated.status == CheckpointStatus.DENIED
    
    def test_hitl_controller(self):
        manager = CheckpointManager()
        hitl = HITLController(manager)
        
        checkpoint = manager.create_checkpoint(
            agent_id="agent-001",
            action_id="action-001",
            checkpoint_type=CheckpointType.HITL,
            reason="Requires human approval",
        )
        
        pending = hitl.get_pending_approvals()
        assert len(pending) >= 1
        
        hitl.approve(checkpoint.checkpoint_id, "human_user")
        
        updated = manager.get_checkpoint(checkpoint.checkpoint_id)
        assert updated.status == CheckpointStatus.APPROVED


# ============================================================================
# COMMUNICATION TESTS
# ============================================================================

class TestCommunication:
    """Test inter-agent communication"""
    
    def test_message_bus(self):
        bus = MessageBus()
        
        bus.register_agent("agent-001")
        bus.register_agent("agent-002")
        
        msg = AgentMessage(
            from_agent_id="agent-001",
            to_agent_id="agent-002",
            message_type="request",
            subject="Hello",
            body={"greeting": "Hi there!"},
        )
        
        delivered = bus.send(msg)
        
        assert delivered
        
        messages = bus.get_messages("agent-002")
        assert len(messages) == 1
        assert messages[0].subject == "Hello"
    
    def test_message_broadcast(self):
        bus = MessageBus()
        
        bus.register_agent("sender")
        bus.register_agent("sub-1")
        bus.register_agent("sub-2")
        bus.register_agent("sub-3")
        
        bus.subscribe("sub-1", "events")
        bus.subscribe("sub-2", "events")
        bus.subscribe("sub-3", "events")
        
        msg = AgentMessage(
            from_agent_id="sender",
            to_agent_id="",
            message_type="event",
            subject="Broadcast",
            body={"data": "Hello everyone!"},
        )
        
        count = bus.broadcast(msg, "events")
        
        assert count == 3
    
    def test_message_factory(self):
        request = MessageFactory.create_request(
            "agent-001",
            "agent-002",
            "Task Request",
            {"task": "analyze"},
        )
        
        assert request.message_type == MessageProtocol.REQUEST
        
        response = MessageFactory.create_response(
            request,
            {"result": "success"},
        )
        
        assert response.message_type == MessageProtocol.RESPONSE
        assert response.reply_to == request.message_id


# ============================================================================
# REGISTRY TESTS
# ============================================================================

class TestRegistry:
    """Test agent registry"""
    
    def test_create_registry(self):
        registry = AgentRegistry()
        
        agent = registry.create_agent(
            name="Test Agent",
            level=AgentLevel.L2,
            sphere="Business",
            tenant_id="tenant-001",
        )
        
        assert agent is not None
        assert registry.get_agent(agent.agent_id) is not None
    
    def test_agent_hierarchy(self):
        registry = AgentRegistry()
        
        parent = registry.create_agent(
            name="Parent",
            level=AgentLevel.L1,
        )
        
        child = registry.create_agent(
            name="Child",
            level=AgentLevel.L2,
            parent_id=parent.agent_id,
        )
        
        children = registry.get_children(parent.agent_id)
        assert len(children) == 1
        assert children[0].agent_id == child.agent_id
    
    def test_get_by_level(self):
        registry = AgentRegistry()
        
        registry.create_agent("L2-1", AgentLevel.L2)
        registry.create_agent("L2-2", AgentLevel.L2)
        registry.create_agent("L3-1", AgentLevel.L3)
        
        l2_agents = registry.get_agents_by_level(AgentLevel.L2)
        assert len(l2_agents) == 2
    
    def test_standard_hierarchy(self):
        agents = create_standard_agents("test-tenant")
        
        assert "nova" in agents
        assert "assistant" in agents
        
        # Check Nova is L0
        nova = agents["nova"]
        assert nova.level == AgentLevel.L0
    
    def test_registry_stats(self):
        registry = AgentRegistry()
        
        CHENUAgentFactory.create_standard_hierarchy(registry, "tenant-001")
        
        stats = registry.get_stats()
        
        assert stats["total_agents"] > 0
        assert stats["by_level"]["L0"] >= 1
        assert stats["by_level"]["L1"] >= 1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete agent workflow"""
        # 1. Create registry
        registry = AgentRegistry()
        
        # 2. Create standard hierarchy
        agents = CHENUAgentFactory.create_standard_hierarchy(
            registry, "enterprise"
        )
        
        # 3. Get agents
        nova = agents["nova"]
        assistant = agents["assistant"]
        
        # 4. Activate agents
        nova.activate()
        assistant.activate()
        
        # 5. Create context
        context = AgentContext(
            agent_id=assistant.agent_id,
            user_id="user-001",
            tenant_id="enterprise",
        )
        assistant.set_context(context)
        
        # 6. Handle user request
        result = assistant.handle_user_request("Help me analyze data")
        
        assert result is not None
        
        # 7. Check stats
        stats = registry.get_stats()
        assert stats["total_agents"] > 10
    
    def test_delegation_workflow(self):
        """Test L1 to L2 delegation"""
        registry = AgentRegistry()
        
        # Create L1 orchestrator
        orchestrator = registry.create_agent(
            name="Orchestrator",
            level=AgentLevel.L1,
            capabilities=[AgentCapability(
                name="Orchestration",
                allowed_actions={ActionType.DELEGATE, ActionType.COMMUNICATE},
            )],
        )
        
        # Create L2 specialist
        specialist = registry.create_agent(
            name="Specialist",
            level=AgentLevel.L2,
            parent_id=orchestrator.agent_id,
            capabilities=[AgentCapability(
                name="Analysis",
                allowed_actions={ActionType.READ, ActionType.WRITE, ActionType.EXECUTE},
            )],
        )
        
        # Activate
        orchestrator.activate()
        specialist.activate()
        
        # Create task
        task = AgentTask(
            agent_id=specialist.agent_id,
            name="Analyze Data",
            instructions=["Read data", "Process", "Report"],
        )
        
        # Delegate
        if isinstance(orchestrator, L1OrchestratorAgent):
            delegation = orchestrator.delegate_to(specialist.agent_id, task)
            assert delegation is not None
    
    def test_checkpoint_in_action(self):
        """Test that high-impact actions trigger checkpoints"""
        registry = AgentRegistry()
        
        # Create agent with low threshold
        agent = registry.create_agent(
            name="Careful Agent",
            level=AgentLevel.L2,
            capabilities=[AgentCapability(
                name="Operations",
                allowed_actions={ActionType.READ, ActionType.WRITE, ActionType.EXECUTE},
                requires_approval_above=0.3,
            )],
        )
        
        # Set auto_checkpoint_threshold low
        agent.agent.auto_checkpoint_threshold = 0.3
        
        agent.activate()
        
        # Create high-impact action
        action = agent.create_action(
            ActionType.EXECUTE,
            "critical_operation",
            estimated_impact=0.8,
        )
        
        # Should require checkpoint
        assert action.requires_checkpoint


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
