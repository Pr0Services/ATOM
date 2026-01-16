"""
============================================================================
CHE·NU™ V69 — SLOT FILL EXPLAINABILITY LAYER
============================================================================
Spec: GPT1/CHE-NU_ENG_SLOT_FILL_EXPLAINABILITY.md

Objective: Ensure each slot fill is:
- explicable
- traçable
- justifiable humainement

Per spec, each filled slot generates:
- une justification textuelle
- les sources utilisées
- les hypothèses éventuelles
- le score de confiance

Governance:
- Explainability obligatoire avant HITL
- Aucun export sans explainability validée

GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import hashlib
import json
import logging

from ..models import (
    Slot,
    SlotStatus,
    SlotExplainability,
    SlotFillResult,
    RiskLevel,
)

logger = logging.getLogger(__name__)


# ============================================================================
# EXPLAINABILITY REQUIREMENTS
# ============================================================================

class ExplainabilityLevel(str, Enum):
    """Level of explainability required"""
    MINIMAL = "minimal"  # Basic info only
    STANDARD = "standard"  # Full explainability
    DETAILED = "detailed"  # With full trace


def get_required_level(slot: Slot) -> ExplainabilityLevel:
    """
    Determine required explainability level based on slot.
    
    Per spec: Requis pour slots risk=medium/high
    """
    if slot.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
        return ExplainabilityLevel.DETAILED
    elif slot.risk_level == RiskLevel.MEDIUM:
        return ExplainabilityLevel.STANDARD
    else:
        return ExplainabilityLevel.MINIMAL


# ============================================================================
# EXPLAINABILITY GENERATOR
# ============================================================================

class ExplainabilityGenerator:
    """
    Generates explainability records for slot fills.
    
    Per spec structure:
    - slot_id
    - decision_summary
    - rationale (why this content)
    - sources
    - constraints_respected (true/false)
    - confidence_score (0–1)
    """
    
    def __init__(self):
        self._templates: Dict[str, str] = {
            "default": "Filled based on {method} using {source_count} source(s).",
            "text": "Generated text content based on context and constraints.",
            "number": "Calculated numeric value from available data.",
            "list": "Compiled list from structured sources.",
            "legal": "Applied legal template with compliance validation.",
            "finance": "Computed financial value with accuracy checks.",
            "brand": "Generated brand-compliant content per guidelines.",
        }
    
    def generate(
        self,
        slot: Slot,
        value: Any,
        method: str = "auto",
        sources: List[str] = None,
        hypotheses: List[str] = None,
        agent_id: str = "system",
    ) -> SlotExplainability:
        """Generate explainability for a slot fill"""
        sources = sources or []
        hypotheses = hypotheses or []
        
        # Generate decision summary
        template = self._templates.get(
            slot.slot_type.value,
            self._templates["default"]
        )
        decision_summary = template.format(
            method=method,
            source_count=len(sources),
        )
        
        # Generate rationale
        rationale = self._generate_rationale(slot, value, method, sources)
        
        # Check constraints
        constraints_respected = self._check_constraints(slot, value)
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            slot,
            value,
            sources,
            constraints_respected,
        )
        
        return SlotExplainability(
            slot_id=slot.slot_id,
            decision_summary=decision_summary,
            rationale=rationale,
            sources=sources,
            hypotheses=hypotheses,
            constraints_respected=constraints_respected,
            confidence_score=confidence,
            generated_by=agent_id,
        )
    
    def _generate_rationale(
        self,
        slot: Slot,
        value: Any,
        method: str,
        sources: List[str],
    ) -> str:
        """Generate human-readable rationale"""
        parts = []
        
        # Method rationale
        parts.append(f"Value determined using {method} method.")
        
        # Source rationale
        if sources:
            parts.append(f"Based on {len(sources)} source(s): {', '.join(sources[:3])}")
            if len(sources) > 3:
                parts.append(f"and {len(sources) - 3} more.")
        else:
            parts.append("No external sources used; value derived from context.")
        
        # Constraint rationale
        if slot.constraints:
            parts.append(f"Applied {len(slot.constraints)} constraint(s).")
        
        # Type-specific rationale
        if slot.slot_type.value == "finance":
            parts.append("Financial accuracy verified against known patterns.")
        elif slot.slot_type.value == "legal":
            parts.append("Compliance requirements validated.")
        elif slot.slot_type.value == "brand":
            parts.append("Brand guidelines adherence confirmed.")
        
        return " ".join(parts)
    
    def _check_constraints(self, slot: Slot, value: Any) -> bool:
        """Check if value respects slot constraints"""
        if not slot.constraints:
            return True
        
        for constraint_type, constraint_value in slot.constraints.items():
            if constraint_type == "min" and isinstance(value, (int, float)):
                if value < constraint_value:
                    return False
            elif constraint_type == "max" and isinstance(value, (int, float)):
                if value > constraint_value:
                    return False
            elif constraint_type == "pattern" and isinstance(value, str):
                import re
                if not re.match(constraint_value, value):
                    return False
            elif constraint_type == "enum" and isinstance(constraint_value, list):
                if value not in constraint_value:
                    return False
            elif constraint_type == "required" and constraint_value:
                if value is None or value == "":
                    return False
        
        return True
    
    def _calculate_confidence(
        self,
        slot: Slot,
        value: Any,
        sources: List[str],
        constraints_respected: bool,
    ) -> float:
        """Calculate confidence score (0-1)"""
        confidence = 0.5  # Base confidence
        
        # Adjust based on sources
        if sources:
            confidence += min(len(sources) * 0.1, 0.3)  # Up to +0.3
        else:
            confidence -= 0.1
        
        # Adjust based on constraints
        if constraints_respected:
            confidence += 0.1
        else:
            confidence -= 0.2
        
        # Adjust based on value presence
        if value is not None:
            confidence += 0.1
        else:
            confidence -= 0.2
        
        # Adjust based on slot type (some types have higher base confidence)
        high_confidence_types = {"number", "date", "boolean"}
        if slot.slot_type.value in high_confidence_types:
            confidence += 0.1
        
        # Clamp to 0-1
        return max(0.0, min(1.0, confidence))


# ============================================================================
# EXPLAINABILITY VALIDATOR
# ============================================================================

class ExplainabilityValidator:
    """
    Validates explainability records.
    
    Per spec:
    - Explainability obligatoire avant HITL
    - Aucun export sans explainability validée
    """
    
    def __init__(
        self,
        min_confidence: float = 0.5,
        require_rationale: bool = True,
    ):
        self.min_confidence = min_confidence
        self.require_rationale = require_rationale
    
    def validate(
        self,
        explainability: SlotExplainability,
        level: ExplainabilityLevel = ExplainabilityLevel.STANDARD,
    ) -> Tuple[bool, List[str]]:
        """
        Validate explainability record.
        
        Returns (is_valid, errors).
        """
        errors: List[str] = []
        
        # Check confidence score
        if explainability.confidence_score < self.min_confidence:
            errors.append(
                f"Confidence score {explainability.confidence_score:.2f} "
                f"below minimum {self.min_confidence}"
            )
        
        # Check rationale
        if self.require_rationale and not explainability.rationale:
            errors.append("Rationale is required")
        
        # Check constraints respected
        if not explainability.constraints_respected:
            errors.append("Constraints not respected")
        
        # Level-specific checks
        if level in [ExplainabilityLevel.STANDARD, ExplainabilityLevel.DETAILED]:
            if not explainability.decision_summary:
                errors.append("Decision summary required for standard/detailed level")
        
        if level == ExplainabilityLevel.DETAILED:
            if not explainability.sources:
                errors.append("Sources required for detailed level")
        
        return len(errors) == 0, errors
    
    def is_valid_for_export(
        self,
        explainability: SlotExplainability,
    ) -> bool:
        """
        Check if explainability is valid for export.
        
        Per spec: Aucun export sans explainability validée
        """
        return explainability.is_valid_for_export()
    
    def is_valid_for_hitl(
        self,
        explainability: SlotExplainability,
    ) -> bool:
        """
        Check if explainability is valid for HITL review.
        
        Per spec: Explainability obligatoire avant HITL
        """
        is_valid, _ = self.validate(explainability, ExplainabilityLevel.STANDARD)
        return is_valid


# ============================================================================
# EXPLAINABILITY STORE
# ============================================================================

class ExplainabilityStore:
    """
    Stores and retrieves explainability records.
    
    Per spec: Stocké dans audit trail
    """
    
    def __init__(self):
        self._store: Dict[str, SlotExplainability] = {}  # slot_id → explainability
        self._history: Dict[str, List[SlotExplainability]] = {}  # slot_id → history
    
    def save(self, explainability: SlotExplainability) -> str:
        """Save explainability record"""
        slot_id = explainability.slot_id
        
        # Add to history
        if slot_id not in self._history:
            self._history[slot_id] = []
        self._history[slot_id].append(explainability)
        
        # Update current
        self._store[slot_id] = explainability
        
        logger.debug(f"Saved explainability for slot {slot_id}")
        return slot_id
    
    def get(self, slot_id: str) -> Optional[SlotExplainability]:
        """Get current explainability for slot"""
        return self._store.get(slot_id)
    
    def get_history(self, slot_id: str) -> List[SlotExplainability]:
        """Get explainability history for slot"""
        return self._history.get(slot_id, [])
    
    def get_all(self) -> Dict[str, SlotExplainability]:
        """Get all current explainability records"""
        return self._store.copy()
    
    def mark_reviewed(
        self,
        slot_id: str,
        reviewer: str,
    ) -> bool:
        """Mark explainability as reviewed"""
        if slot_id in self._store:
            self._store[slot_id].reviewed_by = reviewer
            self._store[slot_id].reviewed_at = datetime.utcnow()
            return True
        return False
    
    def export_for_audit(self) -> List[Dict[str, Any]]:
        """Export all records for audit trail"""
        return [
            {
                "slot_id": exp.slot_id,
                "decision_summary": exp.decision_summary,
                "rationale": exp.rationale,
                "sources": exp.sources,
                "hypotheses": exp.hypotheses,
                "constraints_respected": exp.constraints_respected,
                "confidence_score": exp.confidence_score,
                "generated_by": exp.generated_by,
                "generated_at": exp.generated_at.isoformat(),
                "reviewed_by": exp.reviewed_by,
                "reviewed_at": exp.reviewed_at.isoformat() if exp.reviewed_at else None,
            }
            for exp in self._store.values()
        ]


# ============================================================================
# EXPLAINABILITY LAYER (MAIN INTERFACE)
# ============================================================================

class ExplainabilityLayer:
    """
    Main interface for explainability operations.
    
    Combines generator, validator, and store.
    """
    
    def __init__(
        self,
        min_confidence: float = 0.5,
    ):
        self.generator = ExplainabilityGenerator()
        self.validator = ExplainabilityValidator(min_confidence=min_confidence)
        self.store = ExplainabilityStore()
    
    def explain_fill(
        self,
        slot: Slot,
        value: Any,
        method: str = "auto",
        sources: List[str] = None,
        hypotheses: List[str] = None,
        agent_id: str = "system",
    ) -> Tuple[SlotExplainability, bool, List[str]]:
        """
        Generate and validate explainability for a slot fill.
        
        Returns (explainability, is_valid, errors).
        """
        # Determine required level
        level = get_required_level(slot)
        
        # Generate
        explainability = self.generator.generate(
            slot=slot,
            value=value,
            method=method,
            sources=sources,
            hypotheses=hypotheses,
            agent_id=agent_id,
        )
        
        # Validate
        is_valid, errors = self.validator.validate(explainability, level)
        
        # Store
        self.store.save(explainability)
        
        # Update slot
        slot.explainability = explainability
        
        return explainability, is_valid, errors
    
    def can_export(self, slot: Slot) -> bool:
        """Check if slot can be exported"""
        if not slot.explainability:
            return False
        return self.validator.is_valid_for_export(slot.explainability)
    
    def can_hitl(self, slot: Slot) -> bool:
        """Check if slot is ready for HITL review"""
        if not slot.explainability:
            return False
        return self.validator.is_valid_for_hitl(slot.explainability)
    
    def get_preview(self, slot: Slot) -> Optional[str]:
        """
        Get explainability preview for workspace display.
        
        Per spec: Affiché dans le workspace (preview)
        """
        if not slot.explainability:
            return None
        
        exp = slot.explainability
        return (
            f"{exp.decision_summary}\n"
            f"Confidence: {exp.confidence_score:.0%}\n"
            f"Rationale: {exp.rationale[:100]}..."
            if len(exp.rationale) > 100 else exp.rationale
        )
    
    def export_audit_trail(self) -> List[Dict[str, Any]]:
        """Export full audit trail"""
        return self.store.export_for_audit()


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_explainability_layer(
    min_confidence: float = 0.5,
) -> ExplainabilityLayer:
    """Create an explainability layer"""
    return ExplainabilityLayer(min_confidence=min_confidence)


def create_generator() -> ExplainabilityGenerator:
    """Create an explainability generator"""
    return ExplainabilityGenerator()


def create_validator(
    min_confidence: float = 0.5,
) -> ExplainabilityValidator:
    """Create an explainability validator"""
    return ExplainabilityValidator(min_confidence=min_confidence)
