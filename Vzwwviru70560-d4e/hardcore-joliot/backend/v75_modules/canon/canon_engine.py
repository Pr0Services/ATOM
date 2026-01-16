"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                           CHE·NU™ V75 - CANON ENGINE                                 ║
║                                                                                      ║
║  Système de validation de la source de vérité canonique                             ║
║  Garantit l'intégrité et la cohérence des données CHE·NU                            ║
║                                                                                      ║
║  Version: 75.0 | Status: CANON | License: Proprietary                               ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

MODULE_VERSION = "75.0"
MODULE_STATUS = "CANON"
MODULE_NAME = "CanonEngine"

class CanonStatus(str, Enum):
    """Status d'un élément canonique"""
    CANONICAL = "canonical"       # Source de vérité officielle
    DRAFT = "draft"               # En cours d'élaboration
    DEPRECATED = "deprecated"     # Remplacé par nouvelle version
    SUPERSEDED = "superseded"     # Remplacé par autre élément
    ARCHIVED = "archived"         # Conservé pour historique
    LOCKED = "locked"             # Ne peut plus être modifié

class CanonType(str, Enum):
    """Types d'éléments canoniques"""
    PRINCIPLE = "principle"       # Principe fondamental
    RULE = "rule"                 # Règle R&D
    SPECIFICATION = "spec"        # Spécification technique
    ARCHITECTURE = "architecture" # Décision architecturale
    SCHEMA = "schema"             # Schéma de données
    API = "api"                   # Contrat API
    MODULE = "module"             # Module système
    PROCESS = "process"           # Processus métier

class ValidationLevel(str, Enum):
    """Niveaux de validation"""
    STRICT = "strict"             # Aucune déviation tolérée
    STANDARD = "standard"         # Déviations mineures OK
    FLEXIBLE = "flexible"         # Interprétation permise

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CanonicalElement:
    """Élément canonique du système"""
    id: str
    name: str
    type: CanonType
    status: CanonStatus
    version: str
    content: str
    hash: str
    validation_level: ValidationLevel
    dependencies: List[str] = field(default_factory=list)
    supersedes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: UUID = field(default_factory=uuid4)
    locked_at: Optional[datetime] = None
    locked_by: Optional[UUID] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Résultat de validation canonique"""
    valid: bool
    element_id: str
    checked_against: str  # ID de l'élément canon de référence
    violations: List[str]
    warnings: List[str]
    timestamp: datetime
    validator_id: UUID

@dataclass
class CanonicalChange:
    """Changement proposé à un élément canonique"""
    id: UUID
    element_id: str
    change_type: str  # "create", "update", "deprecate", "lock"
    proposed_content: Optional[str]
    rationale: str
    proposed_by: UUID
    proposed_at: datetime
    status: str = "pending"  # pending, approved, rejected
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL ELEMENTS - LES FONDAMENTAUX CHE·NU
# ═══════════════════════════════════════════════════════════════════════════════

CORE_CANONICAL_ELEMENTS = {
    # ─────────────────────────────────────────────────────────────────────────
    # PRINCIPES FONDAMENTAUX
    # ─────────────────────────────────────────────────────────────────────────
    "PRINCIPLE_GOVERNANCE": CanonicalElement(
        id="PRINCIPLE_GOVERNANCE",
        name="Governance > Execution",
        type=CanonType.PRINCIPLE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        L'interface STRUCTURE la pensée.
        Les agents ILLUMINENT la complexité.
        Les HUMAINS prennent TOUTES les décisions.
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        metadata={"criticality": "absolute"}
    ),
    
    "PRINCIPLE_HUMAN_SOVEREIGNTY": CanonicalElement(
        id="PRINCIPLE_HUMAN_SOVEREIGNTY",
        name="Human Sovereignty",
        type=CanonType.PRINCIPLE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        Aucune action AI sans approbation humaine explicite.
        Aucune décision autonome par les agents.
        Aucune suppression de données sans confirmation.
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        metadata={"criticality": "absolute"}
    ),
    
    "PRINCIPLE_THREAD_SOT": CanonicalElement(
        id="PRINCIPLE_THREAD_SOT",
        name="Thread = Source of Truth",
        type=CanonType.PRINCIPLE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        Le Thread est l'UNIQUE source de vérité.
        Toute projection dérive du Thread.
        Aucune seconde source de vérité tolérée.
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        metadata={"criticality": "absolute"}
    ),
    
    # ─────────────────────────────────────────────────────────────────────────
    # RÈGLES R&D (7 RÈGLES)
    # ─────────────────────────────────────────────────────────────────────────
    "RD_RULE_1": CanonicalElement(
        id="RD_RULE_1",
        name="Human Sovereignty Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="Aucune action sans approbation humaine explicite. Human gates OBLIGATOIRES.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["PRINCIPLE_HUMAN_SOVEREIGNTY"]
    ),
    
    "RD_RULE_2": CanonicalElement(
        id="RD_RULE_2",
        name="Autonomy Isolation Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="AI opère en sandbox UNIQUEMENT. Modes: Analysis, Simulation, Draft, Proposal.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_1"]
    ),
    
    "RD_RULE_3": CanonicalElement(
        id="RD_RULE_3",
        name="Sphere Integrity Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="Cross-sphere requiert workflow EXPLICITE. Aucun partage implicite.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_2"]
    ),
    
    "RD_RULE_4": CanonicalElement(
        id="RD_RULE_4",
        name="My Team Restrictions Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="Aucune orchestration AI-to-AI. L'humain coordonne les multi-agents.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_3"]
    ),
    
    "RD_RULE_5": CanonicalElement(
        id="RD_RULE_5",
        name="Social Restrictions Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="AUCUN algorithme de ranking. Ordre CHRONOLOGIQUE uniquement.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_4"]
    ),
    
    "RD_RULE_6": CanonicalElement(
        id="RD_RULE_6",
        name="Module Traceability Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="Tous modules ont: created_by, created_at, id. Status dans MODULE_REGISTRY.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_5"]
    ),
    
    "RD_RULE_7": CanonicalElement(
        id="RD_RULE_7",
        name="R&D Continuity Rule",
        type=CanonType.RULE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="Construire sur décisions précédentes. Ne JAMAIS contredire règles établies.",
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_6"]
    ),
    
    # ─────────────────────────────────────────────────────────────────────────
    # ARCHITECTURE
    # ─────────────────────────────────────────────────────────────────────────
    "ARCH_9_SPHERES": CanonicalElement(
        id="ARCH_9_SPHERES",
        name="9 Spheres Architecture",
        type=CanonType.ARCHITECTURE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        9 Sphères EXACTEMENT (FROZEN):
        Personal, Business, Government, Creative Studio, Community,
        Social & Media, Entertainment, My Team, Scholar
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        metadata={"frozen": True}
    ),
    
    "ARCH_HTTP_423": CanonicalElement(
        id="ARCH_HTTP_423",
        name="HTTP 423 Checkpoint Protocol",
        type=CanonType.ARCHITECTURE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        Actions sensibles retournent HTTP 423 LOCKED.
        UI DOIT bloquer et attendre approbation humaine.
        POST /checkpoint/{id}/approve ou /reject.
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_1", "RD_RULE_2"]
    ),
    
    "ARCH_HTTP_403": CanonicalElement(
        id="ARCH_HTTP_403",
        name="HTTP 403 Identity Boundary",
        type=CanonType.ARCHITECTURE,
        status=CanonStatus.LOCKED,
        version="1.0.0",
        content="""
        Toute tentative cross-identity retourne HTTP 403 FORBIDDEN.
        Aucun accès cross-identity sans workflow explicite.
        """,
        hash="",
        validation_level=ValidationLevel.STRICT,
        dependencies=["RD_RULE_3"]
    ),
}

# ═══════════════════════════════════════════════════════════════════════════════
# CANON ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class CanonEngine:
    """
    Moteur de gestion et validation de la source de vérité canonique CHE·NU.
    
    Le Canon Engine maintient l'intégrité des principes, règles et
    décisions architecturales qui définissent CHE·NU.
    """
    
    def __init__(self):
        self.elements: Dict[str, CanonicalElement] = {}
        self.pending_changes: Dict[UUID, CanonicalChange] = {}
        
        # Charger les éléments canoniques de base
        self._initialize_core_elements()
        
        logger.info(
            f"CanonEngine V{MODULE_VERSION} initialized with "
            f"{len(self.elements)} canonical elements"
        )
    
    def _initialize_core_elements(self):
        """Initialise les éléments canoniques de base."""
        for element_id, element in CORE_CANONICAL_ELEMENTS.items():
            # Calculer hash du contenu
            element.hash = self._compute_hash(element.content)
            self.elements[element_id] = element
    
    def _compute_hash(self, content: str) -> str:
        """Calcule le hash SHA-256 du contenu."""
        return hashlib.sha256(content.strip().encode()).hexdigest()[:16]
    
    # ═══════════════════════════════════════════════════════════════════════
    # VALIDATION
    # ═══════════════════════════════════════════════════════════════════════
    
    async def validate_against_canon(
        self,
        element_id: str,
        content: str,
        validator_id: UUID
    ) -> ValidationResult:
        """
        Valide un contenu contre un élément canonique.
        
        Args:
            element_id: ID de l'élément canon de référence
            content: Contenu à valider
            validator_id: ID du validateur
            
        Returns:
            ValidationResult avec violations et warnings
        """
        if element_id not in self.elements:
            return ValidationResult(
                valid=False,
                element_id="unknown",
                checked_against=element_id,
                violations=[f"Unknown canonical element: {element_id}"],
                warnings=[],
                timestamp=datetime.utcnow(),
                validator_id=validator_id
            )
        
        canon = self.elements[element_id]
        violations = []
        warnings = []
        
        # Validation selon le type
        if canon.type == CanonType.PRINCIPLE:
            violations, warnings = self._validate_principle(canon, content)
        elif canon.type == CanonType.RULE:
            violations, warnings = self._validate_rule(canon, content)
        elif canon.type == CanonType.ARCHITECTURE:
            violations, warnings = self._validate_architecture(canon, content)
        
        valid = len(violations) == 0 or (
            canon.validation_level == ValidationLevel.FLEXIBLE and 
            not any("CRITICAL" in v for v in violations)
        )
        
        result = ValidationResult(
            valid=valid,
            element_id=element_id,
            checked_against=canon.id,
            violations=violations,
            warnings=warnings,
            timestamp=datetime.utcnow(),
            validator_id=validator_id
        )
        
        logger.info(
            f"Validation against {element_id}: valid={valid}, "
            f"violations={len(violations)}, warnings={len(warnings)}"
        )
        
        return result
    
    def _validate_principle(
        self,
        canon: CanonicalElement,
        content: str
    ) -> Tuple[List[str], List[str]]:
        """Valide contre un principe canonique."""
        violations = []
        warnings = []
        
        content_lower = content.lower()
        
        # Vérifications spécifiques par principe
        if canon.id == "PRINCIPLE_HUMAN_SOVEREIGNTY":
            if "autonomous" in content_lower and "decision" in content_lower:
                violations.append("CRITICAL: Mention of autonomous decision violates Human Sovereignty")
            if "auto-execute" in content_lower or "auto-approve" in content_lower:
                violations.append("CRITICAL: Auto-execution pattern violates Human Sovereignty")
        
        elif canon.id == "PRINCIPLE_GOVERNANCE":
            if "execute before" in content_lower and "approval" not in content_lower:
                warnings.append("Pattern suggests execution before approval")
        
        elif canon.id == "PRINCIPLE_THREAD_SOT":
            if "secondary source" in content_lower or "alternate truth" in content_lower:
                violations.append("CRITICAL: Multiple sources of truth violates Thread SOT")
        
        return violations, warnings
    
    def _validate_rule(
        self,
        canon: CanonicalElement,
        content: str
    ) -> Tuple[List[str], List[str]]:
        """Valide contre une règle R&D."""
        violations = []
        warnings = []
        
        content_lower = content.lower()
        
        # Vérifications par règle
        if canon.id == "RD_RULE_5":  # Social Restrictions
            if "ranking" in content_lower or "engagement score" in content_lower:
                violations.append("CRITICAL: Ranking algorithm detected - violates RD_RULE_5")
            if "optimize" in content_lower and "engagement" in content_lower:
                violations.append("CRITICAL: Engagement optimization violates RD_RULE_5")
        
        elif canon.id == "RD_RULE_4":  # My Team
            if "agent orchestrat" in content_lower and "ai" in content_lower:
                violations.append("CRITICAL: AI-to-AI orchestration violates RD_RULE_4")
        
        elif canon.id == "RD_RULE_6":  # Traceability
            if "created_by" not in content_lower and "traceability" not in content_lower:
                warnings.append("Traceability fields may be missing")
        
        return violations, warnings
    
    def _validate_architecture(
        self,
        canon: CanonicalElement,
        content: str
    ) -> Tuple[List[str], List[str]]:
        """Valide contre une décision architecturale."""
        violations = []
        warnings = []
        
        content_lower = content.lower()
        
        if canon.id == "ARCH_9_SPHERES":
            # Vérifier qu'on ne propose pas de nouvelles sphères
            if "new sphere" in content_lower or "10th sphere" in content_lower:
                violations.append("CRITICAL: Cannot add new spheres - architecture is FROZEN")
        
        elif canon.id == "ARCH_HTTP_423":
            if "skip checkpoint" in content_lower or "bypass" in content_lower:
                violations.append("CRITICAL: Cannot bypass checkpoint protocol")
        
        return violations, warnings
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_element(self, element_id: str) -> Optional[CanonicalElement]:
        """Récupère un élément canonique."""
        return self.elements.get(element_id)
    
    async def list_elements(
        self,
        type_filter: Optional[CanonType] = None,
        status_filter: Optional[CanonStatus] = None
    ) -> List[CanonicalElement]:
        """Liste les éléments canoniques avec filtres optionnels."""
        elements = list(self.elements.values())
        
        if type_filter:
            elements = [e for e in elements if e.type == type_filter]
        
        if status_filter:
            elements = [e for e in elements if e.status == status_filter]
        
        return elements
    
    async def get_dependencies(
        self,
        element_id: str
    ) -> List[CanonicalElement]:
        """Récupère les dépendances d'un élément."""
        element = self.elements.get(element_id)
        if not element:
            return []
        
        return [
            self.elements[dep_id]
            for dep_id in element.dependencies
            if dep_id in self.elements
        ]
    
    async def get_dependents(
        self,
        element_id: str
    ) -> List[CanonicalElement]:
        """Récupère les éléments qui dépendent de celui-ci."""
        return [
            e for e in self.elements.values()
            if element_id in e.dependencies
        ]
    
    # ═══════════════════════════════════════════════════════════════════════
    # CHANGE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    async def propose_change(
        self,
        element_id: str,
        change_type: str,
        proposed_content: Optional[str],
        rationale: str,
        proposed_by: UUID
    ) -> CanonicalChange:
        """
        Propose un changement à un élément canonique.
        
        Les éléments LOCKED ne peuvent pas être modifiés.
        Tous les changements nécessitent une review humaine.
        """
        element = self.elements.get(element_id)
        
        if element and element.status == CanonStatus.LOCKED:
            raise ValueError(
                f"Cannot modify LOCKED canonical element: {element_id}"
            )
        
        change = CanonicalChange(
            id=uuid4(),
            element_id=element_id,
            change_type=change_type,
            proposed_content=proposed_content,
            rationale=rationale,
            proposed_by=proposed_by,
            proposed_at=datetime.utcnow()
        )
        
        self.pending_changes[change.id] = change
        
        logger.info(
            f"Change proposed for {element_id}: {change_type} by {proposed_by}"
        )
        
        return change
    
    async def review_change(
        self,
        change_id: UUID,
        approved: bool,
        reviewed_by: UUID,
        notes: str
    ) -> CanonicalChange:
        """
        Review d'un changement proposé par un humain autorisé.
        """
        if change_id not in self.pending_changes:
            raise ValueError(f"Unknown change: {change_id}")
        
        change = self.pending_changes[change_id]
        change.status = "approved" if approved else "rejected"
        change.reviewed_by = reviewed_by
        change.reviewed_at = datetime.utcnow()
        change.review_notes = notes
        
        if approved:
            await self._apply_change(change)
        
        logger.info(
            f"Change {change_id} {'approved' if approved else 'rejected'} "
            f"by {reviewed_by}"
        )
        
        return change
    
    async def _apply_change(self, change: CanonicalChange):
        """Applique un changement approuvé."""
        if change.change_type == "create":
            # Créer nouvel élément (à implémenter avec validation complète)
            pass
        elif change.change_type == "update":
            element = self.elements.get(change.element_id)
            if element and change.proposed_content:
                element.content = change.proposed_content
                element.hash = self._compute_hash(change.proposed_content)
        elif change.change_type == "deprecate":
            element = self.elements.get(change.element_id)
            if element:
                element.status = CanonStatus.DEPRECATED
        elif change.change_type == "lock":
            element = self.elements.get(change.element_id)
            if element:
                element.status = CanonStatus.LOCKED
                element.locked_at = datetime.utcnow()
                element.locked_by = change.reviewed_by
    
    # ═══════════════════════════════════════════════════════════════════════
    # INTEGRITY CHECK
    # ═══════════════════════════════════════════════════════════════════════
    
    async def verify_integrity(self) -> Dict[str, Any]:
        """
        Vérifie l'intégrité de tous les éléments canoniques.
        
        Détecte les corruptions de hash, dépendances manquantes,
        et incohérences.
        """
        results = {
            "total_elements": len(self.elements),
            "locked_elements": 0,
            "hash_verified": 0,
            "hash_corrupted": [],
            "missing_dependencies": [],
            "circular_dependencies": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for element_id, element in self.elements.items():
            # Vérifier hash
            computed_hash = self._compute_hash(element.content)
            if computed_hash == element.hash:
                results["hash_verified"] += 1
            else:
                results["hash_corrupted"].append(element_id)
            
            # Compter locked
            if element.status == CanonStatus.LOCKED:
                results["locked_elements"] += 1
            
            # Vérifier dépendances
            for dep_id in element.dependencies:
                if dep_id not in self.elements:
                    results["missing_dependencies"].append(
                        f"{element_id} -> {dep_id}"
                    )
        
        # Détecter cycles (simplifié)
        results["circular_dependencies"] = await self._detect_cycles()
        
        results["integrity_ok"] = (
            len(results["hash_corrupted"]) == 0 and
            len(results["missing_dependencies"]) == 0 and
            len(results["circular_dependencies"]) == 0
        )
        
        return results
    
    async def _detect_cycles(self) -> List[str]:
        """Détecte les dépendances circulaires."""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(element_id: str, path: List[str]) -> bool:
            visited.add(element_id)
            rec_stack.add(element_id)
            path.append(element_id)
            
            element = self.elements.get(element_id)
            if element:
                for dep_id in element.dependencies:
                    if dep_id not in visited:
                        if dfs(dep_id, path):
                            return True
                    elif dep_id in rec_stack:
                        cycle_start = path.index(dep_id)
                        cycles.append(" -> ".join(path[cycle_start:] + [dep_id]))
                        return True
            
            path.pop()
            rec_stack.remove(element_id)
            return False
        
        for element_id in self.elements:
            if element_id not in visited:
                dfs(element_id, [])
        
        return cycles


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'CanonEngine',
    'CanonStatus',
    'CanonType',
    'ValidationLevel',
    'CanonicalElement',
    'ValidationResult',
    'CanonicalChange',
    'CORE_CANONICAL_ELEMENTS',
    'MODULE_VERSION',
]
