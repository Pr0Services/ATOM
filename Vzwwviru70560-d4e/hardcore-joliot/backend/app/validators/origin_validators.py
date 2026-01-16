"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — ORIGIN MODULE VALIDATORS
═══════════════════════════════════════════════════════════════════════════════
Agent A: Validation functions ready for Agent B integration

VALIDATORS:
1. parse_date_to_int()      - Parse flexible dates to integers
2. detect_causal_cycle()    - Prevent causal loops
3. validate_chronology()    - Prevent anachronisms
4. validate_evidence()      - Enforce source requirements
5. requires_checkpoint()    - Determine R&D Rule #1 compliance
6. CausalGraphValidator     - Complete graph validation class
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ClaimStrength(str, Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class ValidationResult(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    REQUIRES_CHECKPOINT = "requires_checkpoint"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ValidationError:
    """Validation error details."""
    code: str
    message: str
    field: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationResponse:
    """Complete validation response."""
    is_valid: bool
    requires_checkpoint: bool
    errors: List[ValidationError]
    warnings: List[str]
    
    @classmethod
    def success(cls, requires_checkpoint: bool = False, warnings: List[str] = None):
        return cls(
            is_valid=True,
            requires_checkpoint=requires_checkpoint,
            errors=[],
            warnings=warnings or []
        )
    
    @classmethod
    def failure(cls, errors: List[ValidationError], warnings: List[str] = None):
        return cls(
            is_valid=False,
            requires_checkpoint=False,
            errors=errors,
            warnings=warnings or []
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DATE PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_date_to_int(date_str: Optional[str]) -> Optional[int]:
    """
    Parse flexible date string to integer year.
    
    Handles:
    - Simple years: "1769" → 1769
    - Negative years: "-3000" → -3000
    - Circa dates: "c.1450", "circa 1450" → 1450
    - Ranges: "1939-1945" → 1939 (takes start)
    - BCE notation: "3000 BCE" → -3000
    
    Returns:
        Integer year or None if unparseable.
    """
    if not date_str:
        return None
    
    original = date_str
    date_str = date_str.strip().lower()
    
    # Handle BCE/BC notation
    is_negative = False
    if "bce" in date_str or "bc" in date_str:
        is_negative = True
        date_str = re.sub(r'\s*(bce|bc)\s*', '', date_str)
    
    # Remove common prefixes
    date_str = re.sub(r'^(c\.|circa|ca\.?|approx\.?)\s*', '', date_str)
    
    # Handle explicit negative
    if date_str.startswith("-"):
        is_negative = True
        date_str = date_str[1:]
    
    # Handle ranges (take start)
    if "-" in date_str and not date_str.startswith("-"):
        parts = date_str.split("-")
        date_str = parts[0].strip()
    
    # Extract digits
    digits = re.sub(r'[^\d]', '', date_str)
    
    if not digits:
        return None
    
    try:
        year = int(digits[:4]) if len(digits) >= 4 else int(digits)
        return -year if is_negative else year
    except ValueError:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# CYCLE DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def detect_causal_cycle(
    trigger_id: str,
    result_id: str,
    existing_links: List[Dict[str, str]],
    max_depth: int = 100
) -> Tuple[bool, Optional[List[str]]]:
    """
    Detect if adding trigger_id → result_id would create a cycle.
    
    Args:
        trigger_id: Source node ID
        result_id: Target node ID
        existing_links: List of {"trigger_id": str, "result_id": str}
        max_depth: Maximum recursion depth
    
    Returns:
        Tuple of (cycle_detected: bool, cycle_path: Optional[List[str]])
        If cycle detected, returns the path that forms the cycle.
    """
    # Self-loop is always a cycle
    if trigger_id == result_id:
        return True, [trigger_id, result_id]
    
    # Build adjacency map
    adj: Dict[str, List[str]] = {}
    for link in existing_links:
        t = link["trigger_id"]
        r = link["result_id"]
        if t not in adj:
            adj[t] = []
        adj[t].append(r)
    
    # Add proposed link
    if trigger_id not in adj:
        adj[trigger_id] = []
    adj[trigger_id].append(result_id)
    
    # DFS with path tracking
    visited: Set[str] = set()
    path: List[str] = []
    
    def dfs(node: str, target: str, depth: int) -> Optional[List[str]]:
        if depth > max_depth:
            return None
        if node == target:
            return path + [node]
        if node in visited:
            return None
        
        visited.add(node)
        path.append(node)
        
        for neighbor in adj.get(node, []):
            result = dfs(neighbor, target, depth + 1)
            if result:
                return result
        
        path.pop()
        return None
    
    # Start from result_id, try to reach trigger_id
    cycle_path = dfs(result_id, trigger_id, 0)
    
    if cycle_path:
        # Prepend trigger_id to show full cycle
        return True, [trigger_id] + cycle_path
    
    return False, None


# ═══════════════════════════════════════════════════════════════════════════════
# CHRONOLOGY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NodeDateInfo:
    """Node date information for chronology validation."""
    id: str
    name: str
    date_start: Optional[str]
    date_start_int: Optional[int]


def validate_chronology(
    trigger: NodeDateInfo,
    result: NodeDateInfo,
    allow_contemporary: bool = True
) -> ValidationResponse:
    """
    Validate that trigger precedes or is contemporary with result.
    
    Args:
        trigger: Trigger node info
        result: Result node info
        allow_contemporary: If True, same year is valid
    
    Returns:
        ValidationResponse with status and any errors.
    """
    warnings = []
    
    # Get integer dates
    trigger_date = trigger.date_start_int
    result_date = result.date_start_int
    
    # If dates not pre-parsed, try parsing
    if trigger_date is None and trigger.date_start:
        trigger_date = parse_date_to_int(trigger.date_start)
    if result_date is None and result.date_start:
        result_date = parse_date_to_int(result.date_start)
    
    # Cannot validate if dates unknown
    if trigger_date is None:
        warnings.append(f"Trigger '{trigger.name}' has no parseable date - chronology not validated")
        return ValidationResponse.success(warnings=warnings)
    
    if result_date is None:
        warnings.append(f"Result '{result.name}' has no parseable date - chronology not validated")
        return ValidationResponse.success(warnings=warnings)
    
    # Check chronology
    if allow_contemporary:
        if result_date < trigger_date:
            return ValidationResponse.failure(
                errors=[ValidationError(
                    code="ANACHRONISM",
                    message=f"Chronology violation: result '{result.name}' ({result_date}) precedes trigger '{trigger.name}' ({trigger_date})",
                    field="result_id",
                    details={
                        "trigger_date": trigger_date,
                        "result_date": result_date,
                        "difference_years": trigger_date - result_date
                    }
                )]
            )
    else:
        if result_date <= trigger_date:
            return ValidationResponse.failure(
                errors=[ValidationError(
                    code="ANACHRONISM_STRICT",
                    message=f"Strict chronology violation: result must be after trigger",
                    field="result_id",
                    details={
                        "trigger_date": trigger_date,
                        "result_date": result_date
                    }
                )]
            )
    
    return ValidationResponse.success(warnings=warnings)


# ═══════════════════════════════════════════════════════════════════════════════
# EVIDENCE VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_evidence(
    claim_strength: str,
    sources: Optional[List[str]],
    confidence: Optional[float] = None
) -> ValidationResponse:
    """
    Validate evidence requirements based on claim strength.
    
    Rules:
    - "weak": 0 sources OK
    - "medium": minimum 1 source required
    - "strong": minimum 2 independent sources required
    
    Args:
        claim_strength: weak|medium|strong
        sources: List of source references
        confidence: Optional confidence score (0.0-1.0)
    
    Returns:
        ValidationResponse with checkpoint requirement if needed.
    """
    warnings = []
    sources = sources or []
    count = len(sources)
    
    # Validate confidence if provided
    if confidence is not None:
        if not 0.0 <= confidence <= 1.0:
            return ValidationResponse.failure(
                errors=[ValidationError(
                    code="INVALID_CONFIDENCE",
                    message=f"Confidence must be between 0.0 and 1.0, got {confidence}",
                    field="confidence"
                )]
            )
        
        # High confidence with few sources is suspicious
        if confidence > 0.8 and count < 2:
            warnings.append(f"High confidence ({confidence}) with only {count} source(s) - consider adding more sources")
    
    # Validate based on claim strength
    if claim_strength == ClaimStrength.WEAK or claim_strength == "weak":
        return ValidationResponse.success(
            requires_checkpoint=False,
            warnings=warnings
        )
    
    elif claim_strength == ClaimStrength.MEDIUM or claim_strength == "medium":
        if count < 1:
            return ValidationResponse.failure(
                errors=[ValidationError(
                    code="INSUFFICIENT_SOURCES",
                    message="Medium claims require at least 1 source",
                    field="evidence.sources",
                    details={"required": 1, "provided": count}
                )]
            )
        return ValidationResponse.success(
            requires_checkpoint=True,  # Medium claims need checkpoint
            warnings=warnings
        )
    
    elif claim_strength == ClaimStrength.STRONG or claim_strength == "strong":
        if count < 2:
            return ValidationResponse.failure(
                errors=[ValidationError(
                    code="INSUFFICIENT_SOURCES",
                    message="Strong claims require at least 2 independent sources",
                    field="evidence.sources",
                    details={"required": 2, "provided": count}
                )]
            )
        return ValidationResponse.success(
            requires_checkpoint=True,  # Strong claims need checkpoint
            warnings=warnings
        )
    
    else:
        # Unknown claim strength
        warnings.append(f"Unknown claim_strength '{claim_strength}' - defaulting to weak")
        return ValidationResponse.success(
            requires_checkpoint=False,
            warnings=warnings
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT REQUIREMENTS (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

def requires_checkpoint(entity_type: str, entity_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Determine if entity creation requires checkpoint approval (R&D Rule #1).
    
    Args:
        entity_type: Type of entity (bio_evolution, human_legacy, causal_link, etc.)
        entity_data: Entity data dictionary
    
    Returns:
        Tuple of (requires_checkpoint: bool, reason: str)
    """
    if entity_type == "bio_evolution":
        evidence = entity_data.get("evidence", {})
        claim_strength = evidence.get("claim_strength", "weak")
        
        if claim_strength in ["medium", "strong"]:
            return True, f"Bio-evolution with {claim_strength} claim requires human approval"
        return False, ""
    
    if entity_type == "human_legacy":
        mystery = entity_data.get("world_mystery_link")
        if mystery and mystery.strip():
            return True, "World mystery link requires human approval"
        return False, ""
    
    if entity_type == "causal_link":
        return True, "All causal links require human approval"
    
    if entity_type == "origin_node":
        # Validated nodes require checkpoint
        if entity_data.get("is_validated"):
            return True, "Node validation requires human approval"
        return False, ""
    
    return False, ""


# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETE VALIDATOR CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class CausalGraphValidator:
    """
    Complete validator for the ORIGIN causal graph.
    
    Usage:
        validator = CausalGraphValidator()
        result = validator.validate_new_link(trigger, result, existing_links)
        if not result.is_valid:
            raise HTTPException(status_code=400, detail=result.errors)
        if result.requires_checkpoint:
            raise HTTPException(status_code=423, detail="Checkpoint required")
    """
    
    def __init__(
        self,
        max_cycle_depth: int = 100,
        allow_contemporary: bool = True,
        strict_evidence: bool = True
    ):
        self.max_cycle_depth = max_cycle_depth
        self.allow_contemporary = allow_contemporary
        self.strict_evidence = strict_evidence
    
    def validate_new_link(
        self,
        trigger: NodeDateInfo,
        result: NodeDateInfo,
        existing_links: List[Dict[str, str]],
        checkpoint_id: Optional[str] = None
    ) -> ValidationResponse:
        """
        Validate a new causal link.
        
        Checks:
        1. No self-loop
        2. No cycle
        3. Valid chronology
        4. Checkpoint required
        """
        errors = []
        warnings = []
        
        # Check self-loop
        if trigger.id == result.id:
            errors.append(ValidationError(
                code="SELF_LOOP",
                message="Cannot create causal link from node to itself",
                field="trigger_id"
            ))
            return ValidationResponse.failure(errors)
        
        # Check cycle
        has_cycle, cycle_path = detect_causal_cycle(
            trigger.id,
            result.id,
            existing_links,
            self.max_cycle_depth
        )
        
        if has_cycle:
            errors.append(ValidationError(
                code="CAUSAL_CYCLE",
                message="Adding this link would create a causal cycle",
                details={"cycle_path": cycle_path}
            ))
            return ValidationResponse.failure(errors)
        
        # Check chronology
        chrono_result = validate_chronology(
            trigger,
            result,
            self.allow_contemporary
        )
        
        if not chrono_result.is_valid:
            return chrono_result
        
        warnings.extend(chrono_result.warnings)
        
        # Checkpoint is always required for causal links
        if not checkpoint_id:
            return ValidationResponse(
                is_valid=True,
                requires_checkpoint=True,
                errors=[],
                warnings=warnings + ["Causal links require checkpoint approval (R&D Rule #1)"]
            )
        
        return ValidationResponse.success(
            requires_checkpoint=False,
            warnings=warnings
        )
    
    def validate_bio_evolution(
        self,
        data: Dict[str, Any],
        checkpoint_id: Optional[str] = None
    ) -> ValidationResponse:
        """
        Validate a bio-evolution record.
        
        Checks:
        1. Evidence requirements
        2. Checkpoint for medium/strong claims
        """
        evidence = data.get("evidence", {})
        claim_strength = evidence.get("claim_strength", "weak")
        sources = evidence.get("sources", [])
        confidence = evidence.get("confidence")
        
        # Validate evidence
        evidence_result = validate_evidence(claim_strength, sources, confidence)
        
        if not evidence_result.is_valid:
            return evidence_result
        
        # Check checkpoint requirement
        if evidence_result.requires_checkpoint and not checkpoint_id:
            return ValidationResponse(
                is_valid=True,
                requires_checkpoint=True,
                errors=[],
                warnings=evidence_result.warnings + [
                    f"Bio-evolution with {claim_strength} claim requires checkpoint approval"
                ]
            )
        
        return ValidationResponse.success(
            requires_checkpoint=False,
            warnings=evidence_result.warnings
        )
    
    def validate_human_legacy(
        self,
        data: Dict[str, Any],
        checkpoint_id: Optional[str] = None
    ) -> ValidationResponse:
        """
        Validate a human legacy record.
        
        Checks:
        1. Mystery link checkpoint requirement
        """
        warnings = []
        
        mystery = data.get("world_mystery_link")
        
        if mystery and mystery.strip():
            if not checkpoint_id:
                return ValidationResponse(
                    is_valid=True,
                    requires_checkpoint=True,
                    errors=[],
                    warnings=["World mystery links require checkpoint approval (R&D Rule #1)"]
                )
            warnings.append("World mystery link approved via checkpoint")
        
        return ValidationResponse.success(
            requires_checkpoint=False,
            warnings=warnings
        )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "ClaimStrength",
    "ValidationResult",
    
    # Data classes
    "ValidationError",
    "ValidationResponse",
    "NodeDateInfo",
    
    # Functions
    "parse_date_to_int",
    "detect_causal_cycle",
    "validate_chronology",
    "validate_evidence",
    "requires_checkpoint",
    
    # Classes
    "CausalGraphValidator",
]
