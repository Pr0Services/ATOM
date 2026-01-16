"""
============================================================================
CHE·NU™ V69 — AGENT REGISTRY
============================================================================
Version: 1.0.0
Purpose: Central registry for agent management
Principle: Complete visibility and control over all agents
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Type
import logging
import threading

from ..core.models import (
    Agent,
    AgentLevel,
    AgentStatus,
    AgentCapability,
    AgentContext,
    ActionType,
)
from ..levels.hierarchy import (
    BaseAgent,
    L0SystemAgent,
    L1OrchestratorAgent,
    L2SpecialistAgent,
    L3AssistantAgent,
    create_agent,
)
from ..checkpoints.manager import CheckpointManager, HITLController
from ..communication.messaging import MessageBus

logger = logging.getLogger(__name__)


# ============================================================================
# AGENT REGISTRY
# ============================================================================

class AgentRegistry:
    """
    Central registry for all agents in CHE·NU™.
    
    The registry:
    - Creates and manages agent lifecycles
    - Maintains hierarchy relationships
    - Integrates with governance (checkpoints)
    - Provides inter-agent communication
    - Tracks all agents per tenant
    
    Architecture:
    
        ┌─────────────────────────────────────────────────────────┐
        │                    AGENT REGISTRY                       │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │  ┌─────────────────────────────────────────────────┐   │
        │  │                   L0 (System)                    │   │
        │  │          ┌──────────────────────────┐           │   │
        │  │          │      Nova-System         │           │   │
        │  │          └──────────────────────────┘           │   │
        │  └─────────────────────────────────────────────────┘   │
        │                         │                               │
        │                         ▼                               │
        │  ┌─────────────────────────────────────────────────┐   │
        │  │                  L1 (Orchestrators)              │   │
        │  │    ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
        │  │    │ Personal │  │ Business │  │  Studio  │    │   │
        │  │    └──────────┘  └──────────┘  └──────────┘    │   │
        │  └─────────────────────────────────────────────────┘   │
        │                         │                               │
        │                         ▼                               │
        │  ┌─────────────────────────────────────────────────┐   │
        │  │                  L2 (Specialists)                │   │
        │  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │   │
        │  │  │Finance │ │  Legal │ │   HR   │ │   IT   │   │   │
        │  │  └────────┘ └────────┘ └────────┘ └────────┘   │   │
        │  └─────────────────────────────────────────────────┘   │
        │                         │                               │
        │                         ▼                               │
        │  ┌─────────────────────────────────────────────────┐   │
        │  │                  L3 (Assistants)                 │   │
        │  │         ┌──────────────────────────┐            │   │
        │  │         │     User Assistants      │            │   │
        │  │         └──────────────────────────┘            │   │
        │  └─────────────────────────────────────────────────┘   │
        │                                                         │
        └─────────────────────────────────────────────────────────┘
    
    Usage:
        registry = AgentRegistry()
        
        # Create agents
        nova = registry.create_agent(
            name="Nova-System",
            level=AgentLevel.L0,
        )
        
        personal_orch = registry.create_agent(
            name="Personal-Orchestrator",
            level=AgentLevel.L1,
            parent_id=nova.agent_id,
        )
        
        # Get agents
        all_l2 = registry.get_agents_by_level(AgentLevel.L2)
        tenant_agents = registry.get_agents_by_tenant("acme-corp")
    """
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_models: Dict[str, Agent] = {}
        self._by_level: Dict[AgentLevel, List[str]] = {
            level: [] for level in AgentLevel
        }
        self._by_tenant: Dict[str, List[str]] = {}
        self._by_sphere: Dict[str, List[str]] = {}
        
        # Hierarchy
        self._children: Dict[str, List[str]] = {}  # parent_id -> [child_ids]
        
        # Integration
        self.checkpoint_manager = CheckpointManager()
        self.hitl_controller = HITLController(self.checkpoint_manager)
        self.message_bus = MessageBus()
        
        self._lock = threading.Lock()
    
    def create_agent(
        self,
        name: str,
        level: AgentLevel,
        sphere: Optional[str] = None,
        tenant_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        capabilities: Optional[List[AgentCapability]] = None,
        agent_type: str = "generic",
        requires_hitl: bool = False,
        **metadata,
    ) -> BaseAgent:
        """
        Create and register a new agent.
        
        Args:
            name: Agent name
            level: Agent level (L0-L3)
            sphere: Optional sphere assignment
            tenant_id: Tenant ID
            parent_id: Parent agent ID (for hierarchy)
            capabilities: Agent capabilities
            agent_type: Type of agent
            requires_hitl: Requires HITL for actions
            
        Returns:
            Created agent wrapper
        """
        # Create default capabilities if not provided
        if capabilities is None:
            capabilities = self._default_capabilities(level)
        
        # Create agent model
        agent_model = Agent(
            name=name,
            level=level,
            sphere=sphere,
            tenant_id=tenant_id,
            parent_agent_id=parent_id,
            agent_type=agent_type,
            capabilities=capabilities,
            requires_hitl=requires_hitl,
            metadata=metadata,
        )
        
        # Create appropriate wrapper
        agent = create_agent(
            name=name,
            level=level,
            sphere=sphere,
            tenant_id=tenant_id,
            capabilities=capabilities,
        )
        
        # Set checkpoint handler
        agent.set_checkpoint_handler(
            lambda cp: self.checkpoint_manager.auto_resolve(cp)
        )
        
        with self._lock:
            # Store
            self._agents[agent.agent_id] = agent
            self._agent_models[agent.agent_id] = agent.agent
            
            # Index
            self._by_level[level].append(agent.agent_id)
            
            if tenant_id:
                if tenant_id not in self._by_tenant:
                    self._by_tenant[tenant_id] = []
                self._by_tenant[tenant_id].append(agent.agent_id)
            
            if sphere:
                if sphere not in self._by_sphere:
                    self._by_sphere[sphere] = []
                self._by_sphere[sphere].append(agent.agent_id)
            
            # Hierarchy
            if parent_id:
                if parent_id not in self._children:
                    self._children[parent_id] = []
                self._children[parent_id].append(agent.agent_id)
                
                # Register with L1 orchestrator if parent is L1
                parent = self._agents.get(parent_id)
                if parent and isinstance(parent, L1OrchestratorAgent):
                    parent.register_managed_agent(agent.agent_id)
            
            # Register with message bus
            self.message_bus.register_agent(agent.agent_id)
        
        logger.info(
            f"Created agent: {agent.agent_id} ({name}) "
            f"Level={level.value}, Sphere={sphere}"
        )
        
        return agent
    
    def _default_capabilities(self, level: AgentLevel) -> List[AgentCapability]:
        """Get default capabilities for a level"""
        if level == AgentLevel.L0:
            return [AgentCapability(
                name="System Operations",
                allowed_actions={ActionType.READ, ActionType.EXECUTE},
                max_impact=1.0,
                requires_approval_above=0.8,
                requires_hitl=True,
            )]
        elif level == AgentLevel.L1:
            return [AgentCapability(
                name="Orchestration",
                allowed_actions={ActionType.DELEGATE, ActionType.COMMUNICATE, ActionType.ESCALATE},
                max_impact=0.8,
                requires_approval_above=0.6,
            )]
        elif level == AgentLevel.L2:
            return [AgentCapability(
                name="Specialist Operations",
                allowed_actions={ActionType.READ, ActionType.WRITE, ActionType.EXECUTE},
                max_impact=0.6,
                requires_approval_above=0.4,
            )]
        else:  # L3
            return [AgentCapability(
                name="User Assistance",
                allowed_actions={ActionType.READ, ActionType.COMMUNICATE, ActionType.ESCALATE},
                max_impact=0.3,
                requires_approval_above=0.2,
            )]
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)
    
    def get_agent_model(self, agent_id: str) -> Optional[Agent]:
        """Get agent model by ID"""
        return self._agent_models.get(agent_id)
    
    def get_agents_by_level(self, level: AgentLevel) -> List[BaseAgent]:
        """Get all agents at a level"""
        agent_ids = self._by_level.get(level, [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]
    
    def get_agents_by_tenant(self, tenant_id: str) -> List[BaseAgent]:
        """Get all agents for a tenant"""
        agent_ids = self._by_tenant.get(tenant_id, [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]
    
    def get_agents_by_sphere(self, sphere: str) -> List[BaseAgent]:
        """Get all agents in a sphere"""
        agent_ids = self._by_sphere.get(sphere, [])
        return [self._agents[aid] for aid in agent_ids if aid in self._agents]
    
    def get_children(self, parent_id: str) -> List[BaseAgent]:
        """Get child agents"""
        child_ids = self._children.get(parent_id, [])
        return [self._agents[aid] for aid in child_ids if aid in self._agents]
    
    def activate_agent(self, agent_id: str) -> bool:
        """Activate an agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.activate()
            return True
        return False
    
    def pause_agent(self, agent_id: str) -> bool:
        """Pause an agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.pause()
            return True
        return False
    
    def terminate_agent(self, agent_id: str) -> bool:
        """Terminate an agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.terminate()
            
            # Clean up
            with self._lock:
                self.message_bus.unregister_agent(agent_id)
            
            return True
        return False
    
    def get_hierarchy(self) -> Dict[str, Any]:
        """Get agent hierarchy tree"""
        def build_tree(agent_id: str) -> Dict[str, Any]:
            agent = self._agent_models.get(agent_id)
            if not agent:
                return {}
            
            children = self._children.get(agent_id, [])
            
            return {
                "agent_id": agent_id,
                "name": agent.name,
                "level": agent.level.value,
                "status": agent.status.value,
                "sphere": agent.sphere,
                "children": [build_tree(cid) for cid in children],
            }
        
        # Find root agents (L0 without parents)
        roots = []
        for agent_id, agent in self._agent_models.items():
            if agent.level == AgentLevel.L0 and not agent.parent_agent_id:
                roots.append(build_tree(agent_id))
        
        return {"roots": roots}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_agents": len(self._agents),
            "by_level": {
                level.value: len(ids) for level, ids in self._by_level.items()
            },
            "by_status": self._count_by_status(),
            "tenants": len(self._by_tenant),
            "spheres": len(self._by_sphere),
        }
    
    def _count_by_status(self) -> Dict[str, int]:
        """Count agents by status"""
        counts: Dict[str, int] = {}
        for agent in self._agent_models.values():
            status = agent.status.value
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def list_all(self) -> List[Agent]:
        """List all agent models"""
        return list(self._agent_models.values())


# ============================================================================
# CHE·NU STANDARD AGENTS
# ============================================================================

class CHENUAgentFactory:
    """
    Factory for creating standard CHE·NU™ agents.
    
    Creates the standard agent hierarchy:
    - Nova (L0): System intelligence
    - Sphere Orchestrators (L1): One per sphere
    - Domain Specialists (L2): Domain experts
    - User Assistants (L3): User-facing
    """
    
    # Standard spheres
    SPHERES = [
        "Personal",
        "Business",
        "Government",
        "Studio",
        "Community",
        "Social",
        "Entertainment",
        "MyTeam",
        "Scholar",
    ]
    
    @classmethod
    def create_standard_hierarchy(
        cls,
        registry: AgentRegistry,
        tenant_id: str,
    ) -> Dict[str, BaseAgent]:
        """
        Create the standard CHE·NU™ agent hierarchy.
        
        Returns dict of agent_id -> agent
        """
        agents = {}
        
        # L0: Nova System
        nova = registry.create_agent(
            name="Nova-System",
            level=AgentLevel.L0,
            tenant_id=tenant_id,
            agent_type="system_intelligence",
            requires_hitl=True,
        )
        agents["nova"] = nova
        
        # L1: Sphere Orchestrators
        for sphere in cls.SPHERES:
            orch = registry.create_agent(
                name=f"{sphere}-Orchestrator",
                level=AgentLevel.L1,
                sphere=sphere,
                tenant_id=tenant_id,
                parent_id=nova.agent_id,
                agent_type="orchestrator",
            )
            agents[f"orch_{sphere.lower()}"] = orch
            
            # L2: Domain Specialist for each sphere
            specialist = registry.create_agent(
                name=f"{sphere}-Specialist",
                level=AgentLevel.L2,
                sphere=sphere,
                tenant_id=tenant_id,
                parent_id=orch.agent_id,
                agent_type="specialist",
            )
            agents[f"spec_{sphere.lower()}"] = specialist
        
        # L3: User Assistant
        assistant = registry.create_agent(
            name="User-Assistant",
            level=AgentLevel.L3,
            tenant_id=tenant_id,
            agent_type="assistant",
        )
        agents["assistant"] = assistant
        
        logger.info(
            f"Created standard hierarchy for tenant {tenant_id}: "
            f"{len(agents)} agents"
        )
        
        return agents


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_registry() -> AgentRegistry:
    """Create an agent registry"""
    return AgentRegistry()


def create_standard_agents(
    tenant_id: str,
    registry: Optional[AgentRegistry] = None,
) -> Dict[str, BaseAgent]:
    """Create standard CHE·NU™ agent hierarchy"""
    reg = registry or create_registry()
    return CHENUAgentFactory.create_standard_hierarchy(reg, tenant_id)
