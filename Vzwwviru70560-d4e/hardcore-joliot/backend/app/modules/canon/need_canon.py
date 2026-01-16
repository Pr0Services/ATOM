"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ — NEED CANON V1                                   ║
║                                                                              ║
║  "Needs are stable; implementations evolve."                                 ║
║                                                                              ║
║  A scenario maps to 1–3 primary needs and optional secondary needs.         ║
║  A module must declare which needs it serves.                               ║
║  Governance is a need, not a feature.                                       ║
║                                                                              ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
import yaml

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class UrgencyLevel(str, Enum):
    """Urgency levels for needs."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RiskIfUnmet(str, Enum):
    """Risks if a need is not met."""
    # Clarity risks
    DRIFT = "drift"
    PARALYSIS = "paralysis"
    SCOPE_CREEP = "scope_creep"
    
    # Execution risks
    DELAY = "delay"
    ABANDONMENT = "abandonment"
    MISSED_DEADLINES = "missed_deadlines"
    
    # Memory risks
    CONTEXT_LOSS = "context_loss"
    REWORK = "rework"
    DUPLICATED_EFFORT = "duplicated_effort"
    
    # Governance risks
    SYSTEM_FAILURE = "system_failure"
    SECURITY_INCIDENT = "security_incident"
    IRREVERSIBLE_DAMAGE = "irreversible_damage"
    
    # Safety risks
    BREACH = "breach"
    HARM = "harm"
    TRUST_LOSS = "trust_loss"
    
    # Trust risks
    ABANDON = "abandon"
    FEAR = "fear"
    AVOIDANCE = "avoidance"
    
    # Learning risks
    STAGNATION = "stagnation"
    REPEAT_MISTAKES = "repeat_mistakes"
    
    # Coordination risks
    CONFLICT = "conflict"
    DUPLICATION = "duplication"
    MISALIGNMENT = "misalignment"
    
    # Communication risks
    SILENCE = "silence"
    CONFUSION = "confusion"
    MISSED_CONTEXT = "missed_context"
    
    # Discovery risks
    POOR_DECISIONS = "poor_decisions"
    MISSED_OPPORTUNITIES = "missed_opportunities"
    
    # Organization risks
    MESS = "mess"
    SLOWDOWN = "slowdown"
    LOSS_OF_CONTROL = "loss_of_control"
    
    # Identity risks
    CROSS_TENANT_LEAK = "cross_tenant_leak"
    LEGAL_RISK = "legal_risk"
    
    # Presence risks
    DISENGAGEMENT = "disengagement"
    COGNITIVE_OVERLOAD = "cognitive_overload"
    
    # Resilience risks
    DOWNTIME = "downtime"
    DATA_LOSS = "data_loss"
    FRAGILITY = "fragility"
    
    # Performance risks
    LAG = "lag"
    COST_SPIKE = "cost_spike"
    USER_FRUSTRATION = "user_frustration"

# ═══════════════════════════════════════════════════════════════════════════════
# NEED MODEL
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Need:
    """
    A fundamental human/system need.
    
    Needs are STABLE; implementations evolve.
    """
    id: str
    label: str
    description: str
    urgency_levels: List[UrgencyLevel]
    risks_if_unmet: List[RiskIfUnmet]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "urgency_levels": [u.value for u in self.urgency_levels],
            "risks_if_unmet": [r.value for r in self.risks_if_unmet],
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Need":
        return cls(
            id=data["id"],
            label=data["label"],
            description=data["description"],
            urgency_levels=[UrgencyLevel(u) for u in data.get("urgency_levels", [])],
            risks_if_unmet=[RiskIfUnmet(r) for r in data.get("risks_if_unmet", [])],
        )

# ═══════════════════════════════════════════════════════════════════════════════
# NEED CANON (The 15 Fundamental Needs)
# ═══════════════════════════════════════════════════════════════════════════════

class NeedCanon:
    """
    The canonical list of human/system needs.
    
    Version: v1
    """
    
    VERSION = "v1"
    NAMESPACE = "need"
    
    # Principles
    PRINCIPLES = [
        "Needs are stable; implementations evolve.",
        "A scenario maps to 1–3 primary needs and optional secondary needs.",
        "A module must declare which needs it serves; otherwise it is not activable in simulation.",
        "Governance is a need, not a feature: it must be triggered by circumstance and risk.",
    ]
    
    # The 15 Fundamental Needs
    NEEDS: Dict[str, Need] = {
        "need.clarity": Need(
            id="need.clarity",
            label="Clarity",
            description="Clarify intent, goals, scope, decisions.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.DRIFT, RiskIfUnmet.PARALYSIS, RiskIfUnmet.SCOPE_CREEP],
        ),
        "need.execution": Need(
            id="need.execution",
            label="Execution",
            description="Produce deliverables and take actions.",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.DELAY, RiskIfUnmet.ABANDONMENT, RiskIfUnmet.MISSED_DEADLINES],
        ),
        "need.memory": Need(
            id="need.memory",
            label="Memory",
            description="Keep context, records, and continuity over time.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.CONTEXT_LOSS, RiskIfUnmet.REWORK, RiskIfUnmet.DUPLICATED_EFFORT],
        ),
        "need.governance": Need(
            id="need.governance",
            label="Governance",
            description="Reduce error, enforce invariants, prevent irreversible mistakes.",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.SYSTEM_FAILURE, RiskIfUnmet.SECURITY_INCIDENT, RiskIfUnmet.IRREVERSIBLE_DAMAGE],
        ),
        "need.safety": Need(
            id="need.safety",
            label="Safety",
            description="Protect users, identities, data, and permissions.",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.BREACH, RiskIfUnmet.HARM, RiskIfUnmet.TRUST_LOSS],
        ),
        "need.trust": Need(
            id="need.trust",
            label="Trust",
            description="Make the system understandable, auditable, predictable.",
            urgency_levels=[UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.ABANDON, RiskIfUnmet.FEAR, RiskIfUnmet.AVOIDANCE],
        ),
        "need.learning": Need(
            id="need.learning",
            label="Learning",
            description="Teach users and improve system behavior over time.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.STAGNATION, RiskIfUnmet.REPEAT_MISTAKES],
        ),
        "need.coordination": Need(
            id="need.coordination",
            label="Coordination",
            description="Coordinate people, agents, and tasks across time.",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.CONFLICT, RiskIfUnmet.DUPLICATION, RiskIfUnmet.MISALIGNMENT],
        ),
        "need.communication": Need(
            id="need.communication",
            label="Communication",
            description="Exchange information across channels (chat, email, calls, meetings).",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.SILENCE, RiskIfUnmet.CONFUSION, RiskIfUnmet.MISSED_CONTEXT],
        ),
        "need.discovery": Need(
            id="need.discovery",
            label="Discovery",
            description="Find resources, information, tools, and opportunities.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.POOR_DECISIONS, RiskIfUnmet.MISSED_OPPORTUNITIES],
        ),
        "need.organization": Need(
            id="need.organization",
            label="Organization",
            description="Structure information, files, workflows, and projects.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.MESS, RiskIfUnmet.SLOWDOWN, RiskIfUnmet.LOSS_OF_CONTROL],
        ),
        "need.identity": Need(
            id="need.identity",
            label="Identity Boundary",
            description="Keep strict separation between identities/tenants/data realms.",
            urgency_levels=[UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.CROSS_TENANT_LEAK, RiskIfUnmet.LEGAL_RISK, RiskIfUnmet.TRUST_LOSS],
        ),
        "need.presence": Need(
            id="need.presence",
            label="Presence",
            description="Feel situated (XR/rooms), maintain engagement and spatial understanding.",
            urgency_levels=[UrgencyLevel.LOW, UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.DISENGAGEMENT, RiskIfUnmet.COGNITIVE_OVERLOAD],
        ),
        "need.resilience": Need(
            id="need.resilience",
            label="Resilience",
            description="Operate under failure, latency, partial connectivity.",
            urgency_levels=[UrgencyLevel.MEDIUM],
            risks_if_unmet=[RiskIfUnmet.DOWNTIME, RiskIfUnmet.DATA_LOSS, RiskIfUnmet.FRAGILITY],
        ),
        "need.performance": Need(
            id="need.performance",
            label="Performance",
            description="Control cost/latency; keep live experience smooth.",
            urgency_levels=[UrgencyLevel.MEDIUM, UrgencyLevel.HIGH],
            risks_if_unmet=[RiskIfUnmet.LAG, RiskIfUnmet.COST_SPIKE, RiskIfUnmet.USER_FRUSTRATION],
        ),
    }
    
    @classmethod
    def get(cls, need_id: str) -> Optional[Need]:
        """Get a need by ID."""
        return cls.NEEDS.get(need_id)
    
    @classmethod
    def all(cls) -> List[Need]:
        """Get all needs."""
        return list(cls.NEEDS.values())
    
    @classmethod
    def by_urgency(cls, urgency: UrgencyLevel) -> List[Need]:
        """Get needs that support a specific urgency level."""
        return [n for n in cls.NEEDS.values() if urgency in n.urgency_levels]
    
    @classmethod
    def validate_needs_served(cls, need_ids: List[str]) -> List[str]:
        """Validate that need IDs exist. Returns invalid IDs."""
        invalid = []
        for need_id in need_ids:
            if need_id not in cls.NEEDS:
                invalid.append(need_id)
        return invalid
    
    @classmethod
    def to_yaml(cls) -> str:
        """Export as YAML."""
        data = {
            "version": cls.VERSION,
            "namespace": cls.NAMESPACE,
            "principles": cls.PRINCIPLES,
            "needs": [n.to_dict() for n in cls.NEEDS.values()],
        }
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)

# ═══════════════════════════════════════════════════════════════════════════════
# NEED MAPPING (For scenarios and modules)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NeedMapping:
    """Maps an entity (scenario, step, module) to needs."""
    primary_needs: List[str]
    secondary_needs: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate that all need IDs exist."""
        all_needs = self.primary_needs + self.secondary_needs
        return NeedCanon.validate_needs_served(all_needs)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_needs": self.primary_needs,
            "secondary_needs": self.secondary_needs,
        }

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "Need",
    "NeedCanon",
    "NeedMapping",
    "UrgencyLevel",
    "RiskIfUnmet",
]
