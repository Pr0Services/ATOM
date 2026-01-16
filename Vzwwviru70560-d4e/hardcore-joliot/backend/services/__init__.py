"""
CHE·NU™ Agent Services
======================

Agent system with 350+ sphere agents (L'ESSAIM - The Swarm) + dynamic Thread Agents.

AGENT TYPES:
1. Sphere Agents (350 predefined - Canon AT·OM):
   - 226 original agents (9 spheres)
   - +124 V68 AT·OM ecosystem agents (Transport, Societal, Environment, Privacy, Jeunesse, Dashboard)

2. Extended Agents (+84):
   - Gap Analysis Round 1 additions

3. Thread Agents (dynamic):
   - One per Thread
   - Created automatically with Thread
   - Governed by Thread's identity boundary

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - sensitive actions require human gates
- Rule #4: No AI-to-AI orchestration
- Rule #5: No ranking/engagement optimization (Social)
- Rule #6: Full traceability
"""

from backend.services.agent.agent_registry import (
    AgentRegistryService,
    get_all_predefined_agents,
)
from backend.services.agent.agent_execution import (
    AgentExecutionService,
    requires_human_gate,
    SENSITIVE_CAPABILITIES,
    CONDITIONAL_APPROVAL_CAPABILITIES,
)
from backend.services.agent.extended_agents import (
    get_all_extended_agents,
    EXTENDED_AGENT_COUNTS,
    TOTAL_EXTENDED_AGENTS,
    GRAND_TOTAL_SPHERE_AGENTS,
)
from backend.services.agent.thread_agent_service import (
    ThreadAgentService,
    ThreadAgent,
    ThreadAgentStatus,
    ThreadAgentCapability,
    ThreadAgentCreate,
    ThreadAgentResponse,
    ThreadAgentExecution,
    ThreadAgentExecutionResult,
)

# Original agent distribution (AT·OM L'ESSAIM - The Swarm)
AGENT_DISTRIBUTION = {
    # Original 9 Spheres (226 agents)
    "personal": 28,
    "business": 43,
    "government": 18,
    "creative_studio": 42,
    "community": 12,
    "social_media": 15,
    "entertainment": 8,
    "my_team": 35,
    "scholar": 25,
    # V68 AT·OM Ecosystem (124 agents)
    "transport": 50,       # AT·OM Flow - Division Cinétique Urbaine
    "societal": 20,        # Équilibre, Éducation, Santé, Gouvernance
    "environment": 25,     # Régénération, Énergie, Biodiversité, Circulaire
    "privacy": 8,          # Privacy Guardian
    "jeunesse": 15,        # Génie de Demain
    "dashboard": 6,        # Master Dashboard
}
TOTAL_AGENTS = 350  # L'ESSAIM

# Extended agent distribution (V72)
EXTENDED_AGENT_DISTRIBUTION = {
    "immobilier": 20,
    "scholar_ext": 5,
    "business_ext": 7,
    "government_ext": 4,
    "personal_ext": 4,
    "creative_ext": 3,
    "community_ext": 3,
    "social_ext": 3,
    "entertainment_ext": 2,
    "myteam_ext": 3,
    "core": 30,
}
TOTAL_EXTENDED = 84

# Grand total
GRAND_TOTAL_AGENTS = TOTAL_AGENTS + TOTAL_EXTENDED  # 310

__all__ = [
    # Registry
    "AgentRegistryService",
    "get_all_predefined_agents",
    "AGENT_DISTRIBUTION",
    "TOTAL_AGENTS",
    
    # Execution
    "AgentExecutionService",
    "requires_human_gate",
    "SENSITIVE_CAPABILITIES",
    "CONDITIONAL_APPROVAL_CAPABILITIES",
    
    # Extended Agents
    "get_all_extended_agents",
    "EXTENDED_AGENT_COUNTS",
    "TOTAL_EXTENDED_AGENTS",
    "GRAND_TOTAL_SPHERE_AGENTS",
    "EXTENDED_AGENT_DISTRIBUTION",
    "TOTAL_EXTENDED",
    "GRAND_TOTAL_AGENTS",
    
    # Thread Agents
    "ThreadAgentService",
    "ThreadAgent",
    "ThreadAgentStatus",
    "ThreadAgentCapability",
    "ThreadAgentCreate",
    "ThreadAgentResponse",
    "ThreadAgentExecution",
    "ThreadAgentExecutionResult",
]
