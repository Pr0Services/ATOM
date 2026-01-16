"""
============================================================================
CHE·NU™ V69 — AGENT LEVELS (L0-L3)
============================================================================
Version: 1.0.0
Purpose: Hierarchical agent implementations
Principle: Each level has specific responsibilities and constraints
============================================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
import logging

from ..core.models import (
    Agent,
    AgentLevel,
    AgentStatus,
    AgentCapability,
    AgentAction,
    ActionType,
    ActionStatus,
    AgentContext,
    AgentTask,
    Checkpoint,
    CheckpointType,
    CheckpointStatus,
    Delegation,
)

logger = logging.getLogger(__name__)


# ============================================================================
# BASE AGENT
# ============================================================================

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    All agents must:
    - Check governance before actions
    - Log all operations
    - Support checkpoints
    - Handle delegation
    """
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self._context: Optional[AgentContext] = None
        self._pending_actions: List[AgentAction] = []
        self._completed_actions: List[AgentAction] = []
        self._checkpoints: List[Checkpoint] = []
        
        # Callbacks
        self._on_checkpoint: Optional[Callable[[Checkpoint], CheckpointStatus]] = None
        self._on_action_complete: Optional[Callable[[AgentAction], None]] = None
    
    @property
    def agent_id(self) -> str:
        return self.agent.agent_id
    
    @property
    def level(self) -> AgentLevel:
        return self.agent.level
    
    @property
    def is_active(self) -> bool:
        return self.agent.is_active
    
    def set_context(self, context: AgentContext) -> None:
        """Set execution context"""
        self._context = context
    
    def set_checkpoint_handler(
        self,
        handler: Callable[[Checkpoint], CheckpointStatus],
    ) -> None:
        """Set checkpoint resolution handler"""
        self._on_checkpoint = handler
    
    def create_action(
        self,
        action_type: ActionType,
        target: str,
        parameters: Optional[Dict[str, Any]] = None,
        estimated_impact: float = 0.0,
    ) -> AgentAction:
        """Create a new action"""
        action = AgentAction(
            agent_id=self.agent_id,
            action_type=action_type,
            target=target,
            parameters=parameters or {},
            estimated_impact=estimated_impact,
            sphere=self._context.current_sphere if self._context else None,
            simulation_id=self._context.current_simulation_id if self._context else None,
        )
        
        # Check if checkpoint required
        if estimated_impact > self.agent.auto_checkpoint_threshold:
            action.requires_checkpoint = True
        
        return action
    
    def execute_action(self, action: AgentAction) -> AgentAction:
        """
        Execute an action with governance checks.
        
        Returns the action with updated status.
        """
        # Check if agent can perform this action
        if not self.agent.can_perform(action.action_type, action.sphere):
            action.status = ActionStatus.DENIED
            action.error_message = "Agent lacks capability for this action"
            return action
        
        # Check if checkpoint required
        if action.requires_checkpoint or self.agent.needs_checkpoint:
            checkpoint = self._create_checkpoint(action)
            action.checkpoint_id = checkpoint.checkpoint_id
            
            # Wait for checkpoint resolution
            status = self._resolve_checkpoint(checkpoint)
            
            if status != CheckpointStatus.APPROVED:
                action.status = ActionStatus.DENIED
                action.error_message = f"Checkpoint {status.value}"
                return action
            
            # Reset counter after checkpoint
            self.agent.actions_since_checkpoint = 0
        
        # Execute
        action.status = ActionStatus.EXECUTING
        action.started_at = datetime.utcnow()
        
        try:
            result = self._do_execute(action)
            action.result = result
            action.status = ActionStatus.COMPLETED
            
        except Exception as e:
            action.status = ActionStatus.FAILED
            action.error_message = str(e)
            logger.error(f"Action {action.action_id} failed: {e}")
        
        action.completed_at = datetime.utcnow()
        
        # Update stats
        self.agent.actions_since_checkpoint += 1
        self.agent.total_actions += 1
        self.agent.last_active_at = datetime.utcnow()
        
        # Store completed action
        self._completed_actions.append(action)
        
        # Callback
        if self._on_action_complete:
            self._on_action_complete(action)
        
        return action
    
    @abstractmethod
    def _do_execute(self, action: AgentAction) -> Dict[str, Any]:
        """Actually execute the action (implemented by subclass)"""
        pass
    
    def _create_checkpoint(self, action: AgentAction) -> Checkpoint:
        """Create a governance checkpoint"""
        checkpoint = Checkpoint(
            agent_id=self.agent_id,
            action_id=action.action_id,
            checkpoint_type=CheckpointType.HITL if self.agent.requires_hitl else CheckpointType.THRESHOLD,
            reason=f"Action {action.action_type.value} on {action.target} (impact: {action.estimated_impact})",
            details={
                "action_type": action.action_type.value,
                "target": action.target,
                "estimated_impact": action.estimated_impact,
            },
            timeout_at=datetime.utcnow() + timedelta(hours=1),
        )
        
        self._checkpoints.append(checkpoint)
        self.agent.total_checkpoints += 1
        
        return checkpoint
    
    def _resolve_checkpoint(self, checkpoint: Checkpoint) -> CheckpointStatus:
        """Resolve a checkpoint"""
        if self._on_checkpoint:
            status = self._on_checkpoint(checkpoint)
            checkpoint.status = status
            checkpoint.resolved_at = datetime.utcnow()
            return status
        
        # Default: approve (in production, would wait for human)
        checkpoint.status = CheckpointStatus.APPROVED
        checkpoint.resolved_at = datetime.utcnow()
        checkpoint.resolved_by = "system"
        return CheckpointStatus.APPROVED
    
    def activate(self) -> None:
        """Activate the agent"""
        self.agent.status = AgentStatus.ACTIVE
        logger.info(f"Agent {self.agent_id} activated")
    
    def pause(self) -> None:
        """Pause the agent"""
        self.agent.status = AgentStatus.PAUSED
        logger.info(f"Agent {self.agent_id} paused")
    
    def terminate(self) -> None:
        """Terminate the agent"""
        self.agent.status = AgentStatus.TERMINATED
        logger.info(f"Agent {self.agent_id} terminated")


# ============================================================================
# L0: SYSTEM AGENT
# ============================================================================

class L0SystemAgent(BaseAgent):
    """
    Level 0: System/Infrastructure Agent
    
    Responsibilities:
    - Core platform operations
    - Monitoring and health checks
    - Resource management
    - System-level governance
    
    Constraints:
    - Highest privileges
    - Cannot interact with users directly
    - Always requires HITL for critical operations
    """
    
    def __init__(self, agent: Agent):
        if agent.level != AgentLevel.L0:
            raise ValueError("L0SystemAgent requires L0 agent")
        super().__init__(agent)
    
    def _do_execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute L0 action"""
        if action.action_type == ActionType.EXECUTE:
            return self._execute_system_operation(action)
        elif action.action_type == ActionType.READ:
            return self._read_system_state(action)
        else:
            raise ValueError(f"L0 cannot perform {action.action_type}")
    
    def _execute_system_operation(self, action: AgentAction) -> Dict[str, Any]:
        """Execute a system operation"""
        operation = action.parameters.get("operation", "unknown")
        
        # Log system operation
        logger.info(f"L0 executing system operation: {operation}")
        
        return {
            "operation": operation,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def _read_system_state(self, action: AgentAction) -> Dict[str, Any]:
        """Read system state"""
        return {
            "target": action.target,
            "state": "operational",
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        action = self.create_action(
            ActionType.READ,
            "system.health",
            estimated_impact=0.0,
        )
        result = self.execute_action(action)
        return result.result or {"status": "unknown"}


# ============================================================================
# L1: ORCHESTRATOR AGENT
# ============================================================================

class L1OrchestratorAgent(BaseAgent):
    """
    Level 1: Orchestrator Agent
    
    Responsibilities:
    - Coordinate L2 specialist agents
    - Task distribution and load balancing
    - Cross-domain coordination
    - Escalation handling
    
    Constraints:
    - Cannot perform domain-specific work
    - Must delegate to L2s
    - Reports to L0
    """
    
    def __init__(self, agent: Agent):
        if agent.level != AgentLevel.L1:
            raise ValueError("L1OrchestratorAgent requires L1 agent")
        super().__init__(agent)
        self._delegations: List[Delegation] = []
        self._managed_agents: List[str] = []
    
    def register_managed_agent(self, agent_id: str) -> None:
        """Register an L2 agent under this orchestrator"""
        if agent_id not in self._managed_agents:
            self._managed_agents.append(agent_id)
    
    def _do_execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute L1 action"""
        if action.action_type == ActionType.DELEGATE:
            return self._delegate_task(action)
        elif action.action_type == ActionType.ESCALATE:
            return self._escalate_issue(action)
        elif action.action_type == ActionType.COMMUNICATE:
            return self._coordinate(action)
        else:
            raise ValueError(f"L1 should delegate, not execute {action.action_type}")
    
    def _delegate_task(self, action: AgentAction) -> Dict[str, Any]:
        """Delegate a task to an L2 agent"""
        delegate_id = action.parameters.get("delegate_id")
        task = action.parameters.get("task")
        
        if not delegate_id or delegate_id not in self._managed_agents:
            raise ValueError(f"Invalid delegate: {delegate_id}")
        
        delegation = Delegation(
            delegator_id=self.agent_id,
            delegate_id=delegate_id,
            task_id=task.get("task_id", str(uuid.uuid4())) if task else str(uuid.uuid4()),
            scope=task or {},
        )
        
        self._delegations.append(delegation)
        
        logger.info(f"L1 {self.agent_id} delegated to L2 {delegate_id}")
        
        return {
            "delegation_id": delegation.delegation_id,
            "delegate_id": delegate_id,
            "status": "delegated",
        }
    
    def _escalate_issue(self, action: AgentAction) -> Dict[str, Any]:
        """Escalate an issue to L0"""
        issue = action.parameters.get("issue", "Unknown issue")
        
        logger.warning(f"L1 {self.agent_id} escalating: {issue}")
        
        return {
            "escalated": True,
            "issue": issue,
            "escalated_to": "L0",
        }
    
    def _coordinate(self, action: AgentAction) -> Dict[str, Any]:
        """Coordinate between L2 agents"""
        return {
            "coordinated": True,
            "agents": self._managed_agents,
        }
    
    def delegate_to(
        self,
        delegate_id: str,
        task: AgentTask,
    ) -> Delegation:
        """Delegate a task to an L2 agent"""
        action = self.create_action(
            ActionType.DELEGATE,
            delegate_id,
            parameters={
                "delegate_id": delegate_id,
                "task": task.model_dump(),
            },
        )
        
        result = self.execute_action(action)
        
        return self._delegations[-1] if self._delegations else None


# ============================================================================
# L2: SPECIALIST AGENT
# ============================================================================

class L2SpecialistAgent(BaseAgent):
    """
    Level 2: Specialist Agent
    
    Responsibilities:
    - Domain-specific expertise
    - Execute delegated tasks
    - Provide recommendations (NOT decisions)
    - Report back to L1
    
    Constraints:
    - Limited to specific domain/sphere
    - Cannot delegate to other L2s
    - Must report progress to L1
    """
    
    def __init__(self, agent: Agent, domain: str = "general"):
        if agent.level != AgentLevel.L2:
            raise ValueError("L2SpecialistAgent requires L2 agent")
        super().__init__(agent)
        self.domain = domain
        self._current_task: Optional[AgentTask] = None
    
    def _do_execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute L2 action"""
        if action.action_type == ActionType.READ:
            return self._analyze(action)
        elif action.action_type == ActionType.WRITE:
            return self._recommend(action)
        elif action.action_type == ActionType.EXECUTE:
            return self._perform_task(action)
        else:
            raise ValueError(f"L2 cannot perform {action.action_type}")
    
    def _analyze(self, action: AgentAction) -> Dict[str, Any]:
        """Analyze data in domain"""
        target = action.target
        
        logger.info(f"L2 {self.agent_id} analyzing {target} in domain {self.domain}")
        
        return {
            "domain": self.domain,
            "target": target,
            "analysis": "Analysis results here",
            "confidence": 0.85,
        }
    
    def _recommend(self, action: AgentAction) -> Dict[str, Any]:
        """
        Provide a recommendation (NOT a decision).
        
        CHE·NU™ principle: Agents recommend, humans decide.
        """
        recommendation = action.parameters.get("recommendation", {})
        
        logger.info(f"L2 {self.agent_id} recommending in domain {self.domain}")
        
        return {
            "domain": self.domain,
            "recommendation": recommendation,
            "rationale": "Based on analysis...",
            "confidence": 0.8,
            "requires_human_decision": True,  # ALWAYS
        }
    
    def _perform_task(self, action: AgentAction) -> Dict[str, Any]:
        """Perform a delegated task"""
        if self._current_task is None:
            raise ValueError("No task assigned")
        
        self._current_task.progress = 1.0
        self._current_task.status = ActionStatus.COMPLETED
        self._current_task.completed_at = datetime.utcnow()
        
        return {
            "task_id": self._current_task.task_id,
            "status": "completed",
            "domain": self.domain,
        }
    
    def accept_task(self, task: AgentTask) -> None:
        """Accept a delegated task"""
        self._current_task = task
        task.status = ActionStatus.EXECUTING
        task.started_at = datetime.utcnow()
        
        logger.info(f"L2 {self.agent_id} accepted task {task.task_id}")
    
    def analyze(self, target: str) -> Dict[str, Any]:
        """Analyze a target in this domain"""
        action = self.create_action(
            ActionType.READ,
            target,
            estimated_impact=0.1,
        )
        result = self.execute_action(action)
        return result.result or {}
    
    def recommend(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Provide a recommendation"""
        action = self.create_action(
            ActionType.WRITE,
            "recommendation",
            parameters={"recommendation": recommendation},
            estimated_impact=0.3,
        )
        result = self.execute_action(action)
        return result.result or {}


# ============================================================================
# L3: ASSISTANT AGENT
# ============================================================================

class L3AssistantAgent(BaseAgent):
    """
    Level 3: Assistant Agent
    
    Responsibilities:
    - User-facing interactions
    - Translate user intent to tasks
    - Present information clearly
    - Handle user requests
    
    Constraints:
    - Most restricted privileges
    - Cannot access sensitive data directly
    - Must escalate complex requests
    """
    
    def __init__(self, agent: Agent):
        if agent.level != AgentLevel.L3:
            raise ValueError("L3AssistantAgent requires L3 agent")
        super().__init__(agent)
        self._conversation_history: List[Dict[str, Any]] = []
    
    def _do_execute(self, action: AgentAction) -> Dict[str, Any]:
        """Execute L3 action"""
        if action.action_type == ActionType.COMMUNICATE:
            return self._respond(action)
        elif action.action_type == ActionType.READ:
            return self._fetch_info(action)
        elif action.action_type == ActionType.ESCALATE:
            return self._escalate_request(action)
        else:
            raise ValueError(f"L3 cannot perform {action.action_type}")
    
    def _respond(self, action: AgentAction) -> Dict[str, Any]:
        """Respond to user"""
        message = action.parameters.get("message", "")
        
        self._conversation_history.append({
            "role": "assistant",
            "content": message,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        return {
            "message": message,
            "delivered": True,
        }
    
    def _fetch_info(self, action: AgentAction) -> Dict[str, Any]:
        """Fetch information for user"""
        return {
            "target": action.target,
            "info": "Information fetched",
            "source": "L2 specialist",
        }
    
    def _escalate_request(self, action: AgentAction) -> Dict[str, Any]:
        """Escalate complex request to L2"""
        request = action.parameters.get("request", "")
        
        logger.info(f"L3 {self.agent_id} escalating request to L2")
        
        return {
            "escalated": True,
            "request": request,
            "escalated_to": "L2",
        }
    
    def respond_to_user(self, message: str) -> Dict[str, Any]:
        """Send response to user"""
        action = self.create_action(
            ActionType.COMMUNICATE,
            "user",
            parameters={"message": message},
            estimated_impact=0.0,
        )
        result = self.execute_action(action)
        return result.result or {}
    
    def handle_user_request(self, request: str) -> Dict[str, Any]:
        """Handle a user request"""
        # Log user message
        self._conversation_history.append({
            "role": "user",
            "content": request,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        # For complex requests, escalate
        if len(request) > 100 or "analyze" in request.lower():
            action = self.create_action(
                ActionType.ESCALATE,
                "L2",
                parameters={"request": request},
                estimated_impact=0.2,
            )
            return self.execute_action(action).result or {}
        
        # Simple request, respond directly
        return self.respond_to_user(f"I understand your request: {request[:50]}...")


# ============================================================================
# AGENT FACTORY
# ============================================================================

import uuid

def create_agent(
    name: str,
    level: AgentLevel,
    sphere: Optional[str] = None,
    tenant_id: Optional[str] = None,
    capabilities: Optional[List[AgentCapability]] = None,
) -> BaseAgent:
    """
    Factory function to create the appropriate agent type.
    """
    agent = Agent(
        name=name,
        level=level,
        sphere=sphere,
        tenant_id=tenant_id,
        capabilities=capabilities or [],
    )
    
    if level == AgentLevel.L0:
        return L0SystemAgent(agent)
    elif level == AgentLevel.L1:
        return L1OrchestratorAgent(agent)
    elif level == AgentLevel.L2:
        return L2SpecialistAgent(agent, domain=sphere or "general")
    elif level == AgentLevel.L3:
        return L3AssistantAgent(agent)
    else:
        raise ValueError(f"Unknown agent level: {level}")
