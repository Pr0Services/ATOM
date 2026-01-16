"""
============================================================================
CHE·NU™ V69 — V52 INFRASTRUCTURE MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_V52_Gateway_Mesh_Registry_Internal_Spec.md
- CHE-NU_V52_OPA_7_Rules_Complete_Pack.md
- CHE-NU_V52_Agent_Learning_From_Backlogs.md
- CHE-NU_AutoGen_Integration.md
- CHE-NU_Prompt_System.md
- CHE-NU_Intelligence_Control_Layer.md

"Default deny, explicit allowlists, human approval for high-impact"

Principle: GOUVERNANCE > EXÉCUTION, Nova = Authority
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # Gateway
    Environment, AuthMethod, RiskCategory,
    RateLimit, APIRoute, ServiceMeshPolicy,
    # OPA
    ActorType, ActionType, AutonomyLevel,
    OPARequest, OPAPolicyResult,
    # Learning
    LearningTechnique, BacklogEntry, LearningSession, KnowledgeThread,
    # AutoGen
    AutoGenUseCase, AutoGenSessionStatus, AutoGenSession,
    # Prompt
    PromptLayer, Prompt, PromptComposition,
    # Intelligence
    SelfTestCategory, SelfTestResult, SelfTestSuite, AuditEntry,
)

# Gateway
from .gateway import (
    APIGateway, ServiceMesh, AgentRegistry, RegisteredAgent,
    create_gateway, create_service_mesh, create_agent_registry,
)

# Systems
from .systems import (
    OPA7RulesEngine,
    PromptSystem,
    AutoGenIntegration,
    AgentLearningSystem,
    IntelligenceControlLayer,
    create_opa_engine,
    create_prompt_system,
    create_autogen_integration,
    create_agent_learning,
    create_intelligence_control,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash",
    # Gateway Models
    "Environment", "AuthMethod", "RiskCategory",
    "RateLimit", "APIRoute", "ServiceMeshPolicy",
    # OPA Models
    "ActorType", "ActionType", "AutonomyLevel",
    "OPARequest", "OPAPolicyResult",
    # Learning Models
    "LearningTechnique", "BacklogEntry", "LearningSession", "KnowledgeThread",
    # AutoGen Models
    "AutoGenUseCase", "AutoGenSessionStatus", "AutoGenSession",
    # Prompt Models
    "PromptLayer", "Prompt", "PromptComposition",
    # Intelligence Models
    "SelfTestCategory", "SelfTestResult", "SelfTestSuite", "AuditEntry",
    # Gateway
    "APIGateway", "ServiceMesh", "AgentRegistry", "RegisteredAgent",
    "create_gateway", "create_service_mesh", "create_agent_registry",
    # Systems
    "OPA7RulesEngine", "PromptSystem", "AutoGenIntegration",
    "AgentLearningSystem", "IntelligenceControlLayer",
    "create_opa_engine", "create_prompt_system", "create_autogen_integration",
    "create_agent_learning", "create_intelligence_control",
]
