"""
============================================================================
CHE·NU™ V69 — AGENT FRAMEWORK
============================================================================
Version: 1.0.0
Purpose: Hierarchical agent system with governance checkpoints
Principle: GOUVERNANCE > EXÉCUTION — Agents NEVER decide, humans do

The Agent Framework provides:
- L0-L3 agent hierarchy
- Governance checkpoints (HITL)
- Inter-agent communication
- Full audit trail
- OPA integration

Agent Hierarchy:
- L0 (System): Core platform operations
- L1 (Orchestrator): Coordinates L2 agents
- L2 (Specialist): Domain-specific expertise
- L3 (Assistant): User-facing interactions

Key Principles:
1. Agents RECOMMEND, humans DECIDE
2. All actions are logged for audit
3. Sensitive actions require checkpoints
4. Governance takes precedence over execution

Usage:
    from agents import create_registry, create_standard_agents
    
    # Create registry
    registry = create_registry()
    
    # Create standard hierarchy
    agents = create_standard_agents("tenant-001", registry)
    
    # Get Nova (L0 system agent)
    nova = agents["nova"]
    nova.activate()
    
    # Create context
    context = AgentContext(agent_id=nova.agent_id)
    nova.set_context(context)
    
    # Perform action (with governance)
    action = nova.create_action(
        ActionType.EXECUTE,
        "system.health_check",
    )
    result = nova.execute_action(action)
============================================================================
"""

# Core Models
from .core import (
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
    Delegation,
)

# Agent Hierarchy
from .levels import (
    BaseAgent,
    L0SystemAgent,
    L1OrchestratorAgent,
    L2SpecialistAgent,
    L3AssistantAgent,
    create_agent,
)

# Checkpoints
from .checkpoints import (
    CheckpointRule,
    CheckpointManager,
    HITLController,
    create_checkpoint_manager,
    create_hitl_controller,
)

# Communication
from .communication import (
    AgentMailbox,
    MessageBus,
    CommunicationChannel,
    MessageProtocol,
    MessageFactory,
    create_message_bus,
    create_channel,
)

# Registry
from .registry import (
    AgentRegistry,
    CHENUAgentFactory,
    create_registry,
    create_standard_agents,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Core Models
    "Agent",
    "AgentLevel",
    "AgentStatus",
    "AgentCapability",
    "AgentAction",
    "ActionType",
    "ActionStatus",
    "Checkpoint",
    "CheckpointType",
    "CheckpointStatus",
    "AgentMessage",
    "MessagePriority",
    "AgentContext",
    "AgentTask",
    "Delegation",
    # Agent Hierarchy
    "BaseAgent",
    "L0SystemAgent",
    "L1OrchestratorAgent",
    "L2SpecialistAgent",
    "L3AssistantAgent",
    "create_agent",
    # Checkpoints
    "CheckpointRule",
    "CheckpointManager",
    "HITLController",
    "create_checkpoint_manager",
    "create_hitl_controller",
    # Communication
    "AgentMailbox",
    "MessageBus",
    "CommunicationChannel",
    "MessageProtocol",
    "MessageFactory",
    "create_message_bus",
    "create_channel",
    # Registry
    "AgentRegistry",
    "CHENUAgentFactory",
    "create_registry",
    "create_standard_agents",
]
