"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                         CHE·NU™ V75 - STAGIAIRE ENGINE                               ║
║                                                                                      ║
║  Système d'onboarding intelligent pour agents et utilisateurs                        ║
║  Garantit la compréhension des principes CHE·NU avant accès système                 ║
║                                                                                      ║
║  Version: 75.0 | Status: CANON | License: Proprietary                               ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

MODULE_VERSION = "75.0"
MODULE_STATUS = "CANON"
MODULE_NAME = "StagiaireEngine"

class StagiaireLevel(str, Enum):
    """Niveaux de progression du stagiaire"""
    NOVICE = "novice"           # Début - Principes de base
    APPRENTI = "apprenti"       # Comprend la gouvernance
    COMPAGNON = "compagnon"     # Maîtrise les 7 règles R&D
    MAITRE = "maitre"           # Peut former d'autres
    EXPERT = "expert"           # Contribution au système

class ValidationStatus(str, Enum):
    """Status de validation des connaissances"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class KnowledgeModule:
    """Module de connaissance à valider"""
    id: str
    name: str
    description: str
    required_for_level: StagiaireLevel
    prerequisites: List[str] = field(default_factory=list)
    validation_criteria: List[str] = field(default_factory=list)
    estimated_duration_minutes: int = 30

@dataclass
class StagiaireProgress:
    """Progression d'un stagiaire"""
    id: UUID
    entity_id: UUID  # User ou Agent ID
    entity_type: str  # "user" ou "agent"
    current_level: StagiaireLevel
    completed_modules: List[str]
    current_module: Optional[str]
    validation_scores: Dict[str, float]
    created_at: datetime
    updated_at: datetime
    promoted_at: Optional[datetime] = None
    promoted_by: Optional[UUID] = None

@dataclass
class ValidationResult:
    """Résultat d'une validation de connaissance"""
    module_id: str
    score: float
    passed: bool
    feedback: str
    timestamp: datetime
    validated_by: Optional[UUID] = None

# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE - LES 7 RÈGLES R&D
# ═══════════════════════════════════════════════════════════════════════════════

CHENU_KNOWLEDGE_MODULES = [
    KnowledgeModule(
        id="RD_RULE_1",
        name="Human Sovereignty",
        description="Aucune action sans approbation humaine explicite",
        required_for_level=StagiaireLevel.NOVICE,
        validation_criteria=[
            "Comprend que l'humain décide TOUJOURS",
            "Sait identifier les actions nécessitant approbation",
            "Peut expliquer le concept de Human Gate"
        ],
        estimated_duration_minutes=20
    ),
    KnowledgeModule(
        id="RD_RULE_2",
        name="Autonomy Isolation",
        description="AI opère en sandbox uniquement",
        required_for_level=StagiaireLevel.NOVICE,
        prerequisites=["RD_RULE_1"],
        validation_criteria=[
            "Comprend les 4 modes: Analysis, Simulation, Draft, Proposal",
            "Sait que jamais d'accès direct production",
            "Peut expliquer HTTP 423 checkpoint"
        ],
        estimated_duration_minutes=25
    ),
    KnowledgeModule(
        id="RD_RULE_3",
        name="Sphere Integrity",
        description="Cross-sphere requiert workflow explicite",
        required_for_level=StagiaireLevel.APPRENTI,
        prerequisites=["RD_RULE_1", "RD_RULE_2"],
        validation_criteria=[
            "Connaît les 9 sphères CHE·NU",
            "Comprend les limites des transferts cross-sphere",
            "Sait créer un workflow d'autorisation"
        ],
        estimated_duration_minutes=30
    ),
    KnowledgeModule(
        id="RD_RULE_4",
        name="My Team Restrictions",
        description="Aucune orchestration AI-to-AI",
        required_for_level=StagiaireLevel.APPRENTI,
        prerequisites=["RD_RULE_3"],
        validation_criteria=[
            "Comprend que l'humain coordonne les multi-agents",
            "Sait pourquoi pas d'orchestration AI autonome",
            "Peut expliquer le pattern de coordination humaine"
        ],
        estimated_duration_minutes=20
    ),
    KnowledgeModule(
        id="RD_RULE_5",
        name="Social Restrictions",
        description="AUCUN algorithme de ranking",
        required_for_level=StagiaireLevel.COMPAGNON,
        prerequisites=["RD_RULE_4"],
        validation_criteria=[
            "Comprend pourquoi ordre chronologique seulement",
            "Sait identifier les patterns de ranking interdits",
            "Peut expliquer les dangers de l'optimisation engagement"
        ],
        estimated_duration_minutes=25
    ),
    KnowledgeModule(
        id="RD_RULE_6",
        name="Module Traceability",
        description="Tous modules ont traçabilité complète",
        required_for_level=StagiaireLevel.COMPAGNON,
        prerequisites=["RD_RULE_5"],
        validation_criteria=[
            "Connaît les champs obligatoires (created_by, id, etc.)",
            "Comprend le MODULE_REGISTRY",
            "Sait documenter un nouveau module"
        ],
        estimated_duration_minutes=30
    ),
    KnowledgeModule(
        id="RD_RULE_7",
        name="R&D Continuity",
        description="Construire sur les décisions précédentes",
        required_for_level=StagiaireLevel.MAITRE,
        prerequisites=["RD_RULE_6"],
        validation_criteria=[
            "Sait référencer la documentation existante",
            "Ne contredit jamais les règles établies",
            "Peut assurer la continuité entre sessions"
        ],
        estimated_duration_minutes=35
    ),
    KnowledgeModule(
        id="GOVERNANCE_PRINCIPLES",
        name="Governance > Execution",
        description="Principes fondamentaux de gouvernance CHE·NU",
        required_for_level=StagiaireLevel.NOVICE,
        validation_criteria=[
            "Comprend: L'interface structure la pensée",
            "Comprend: Les agents illuminent la complexité",
            "Comprend: Les HUMAINS prennent TOUTES les décisions"
        ],
        estimated_duration_minutes=15
    ),
    KnowledgeModule(
        id="THREAD_SYSTEM",
        name="Thread V2 System",
        description="Le Thread comme source de vérité unique",
        required_for_level=StagiaireLevel.APPRENTI,
        prerequisites=["GOVERNANCE_PRINCIPLES"],
        validation_criteria=[
            "Comprend Event Sourcing append-only",
            "Connaît les types d'événements Thread",
            "Sait que Thread = unique source de vérité"
        ],
        estimated_duration_minutes=40
    ),
    KnowledgeModule(
        id="HUMAN_GATES",
        name="Human Gates & Checkpoints",
        description="Système de validation humaine",
        required_for_level=StagiaireLevel.COMPAGNON,
        prerequisites=["THREAD_SYSTEM"],
        validation_criteria=[
            "Connaît les 4 stratégies de sécurisation",
            "Sait implémenter HTTP 423 checkpoint",
            "Comprend Identity Boundary (HTTP 403)"
        ],
        estimated_duration_minutes=35
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# STAGIAIRE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class StagiaireEngine:
    """
    Moteur d'onboarding et de validation des connaissances CHE·NU.
    
    Garantit que tout agent ou utilisateur comprend les principes
    fondamentaux avant d'avoir accès au système.
    """
    
    def __init__(self):
        self.knowledge_modules = {m.id: m for m in CHENU_KNOWLEDGE_MODULES}
        self.progress_store: Dict[UUID, StagiaireProgress] = {}
        logger.info(f"StagiaireEngine V{MODULE_VERSION} initialized with {len(self.knowledge_modules)} modules")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENROLLMENT
    # ═══════════════════════════════════════════════════════════════════════
    
    async def enroll(
        self,
        entity_id: UUID,
        entity_type: str,
        enrolled_by: UUID
    ) -> StagiaireProgress:
        """
        Inscrit une nouvelle entité (user ou agent) au programme stagiaire.
        
        Args:
            entity_id: ID de l'entité à inscrire
            entity_type: "user" ou "agent"
            enrolled_by: ID de l'utilisateur qui inscrit
            
        Returns:
            StagiaireProgress initialisé
        """
        now = datetime.utcnow()
        
        progress = StagiaireProgress(
            id=uuid4(),
            entity_id=entity_id,
            entity_type=entity_type,
            current_level=StagiaireLevel.NOVICE,
            completed_modules=[],
            current_module="GOVERNANCE_PRINCIPLES",
            validation_scores={},
            created_at=now,
            updated_at=now
        )
        
        self.progress_store[entity_id] = progress
        
        logger.info(
            f"Enrolled {entity_type} {entity_id} as Stagiaire by {enrolled_by}"
        )
        
        return progress
    
    # ═══════════════════════════════════════════════════════════════════════
    # VALIDATION
    # ═══════════════════════════════════════════════════════════════════════
    
    async def validate_knowledge(
        self,
        entity_id: UUID,
        module_id: str,
        responses: Dict[str, Any],
        validated_by: Optional[UUID] = None
    ) -> ValidationResult:
        """
        Valide la connaissance d'un module pour une entité.
        
        Args:
            entity_id: ID de l'entité
            module_id: ID du module à valider
            responses: Réponses aux questions de validation
            validated_by: ID du validateur (si validation humaine)
            
        Returns:
            ValidationResult avec score et feedback
        """
        if entity_id not in self.progress_store:
            raise ValueError(f"Entity {entity_id} not enrolled")
        
        if module_id not in self.knowledge_modules:
            raise ValueError(f"Unknown module: {module_id}")
        
        module = self.knowledge_modules[module_id]
        progress = self.progress_store[entity_id]
        
        # Vérifier prérequis
        for prereq in module.prerequisites:
            if prereq not in progress.completed_modules:
                return ValidationResult(
                    module_id=module_id,
                    score=0.0,
                    passed=False,
                    feedback=f"Prerequisite not completed: {prereq}",
                    timestamp=datetime.utcnow()
                )
        
        # Calculer score (simplifié - en production utiliserait LLM)
        score = self._calculate_validation_score(module, responses)
        passed = score >= 0.8  # 80% minimum
        
        feedback = self._generate_feedback(module, score, passed)
        
        result = ValidationResult(
            module_id=module_id,
            score=score,
            passed=passed,
            feedback=feedback,
            timestamp=datetime.utcnow(),
            validated_by=validated_by
        )
        
        # Mettre à jour progression si validé
        if passed:
            progress.completed_modules.append(module_id)
            progress.validation_scores[module_id] = score
            progress.updated_at = datetime.utcnow()
            
            # Vérifier promotion de niveau
            await self._check_level_promotion(entity_id)
        
        logger.info(
            f"Validation {module_id} for {entity_id}: "
            f"score={score:.2f}, passed={passed}"
        )
        
        return result
    
    def _calculate_validation_score(
        self,
        module: KnowledgeModule,
        responses: Dict[str, Any]
    ) -> float:
        """Calcule le score de validation basé sur les réponses."""
        if not responses:
            return 0.0
        
        # Score basé sur critères validés
        criteria_count = len(module.validation_criteria)
        validated_count = sum(
            1 for i, criterion in enumerate(module.validation_criteria)
            if responses.get(f"criterion_{i}", False)
        )
        
        return validated_count / criteria_count if criteria_count > 0 else 0.0
    
    def _generate_feedback(
        self,
        module: KnowledgeModule,
        score: float,
        passed: bool
    ) -> str:
        """Génère un feedback personnalisé."""
        if passed:
            return f"Félicitations! Module '{module.name}' validé avec {score*100:.0f}%."
        elif score >= 0.6:
            return f"Presque! Score: {score*100:.0f}%. Revoyez les critères non validés."
        else:
            return f"Score: {score*100:.0f}%. Relisez attentivement la documentation du module."
    
    # ═══════════════════════════════════════════════════════════════════════
    # PROMOTION
    # ═══════════════════════════════════════════════════════════════════════
    
    async def _check_level_promotion(self, entity_id: UUID) -> Optional[StagiaireLevel]:
        """Vérifie si l'entité peut être promue au niveau suivant."""
        progress = self.progress_store[entity_id]
        
        # Modules requis par niveau
        level_requirements = {
            StagiaireLevel.NOVICE: ["GOVERNANCE_PRINCIPLES", "RD_RULE_1", "RD_RULE_2"],
            StagiaireLevel.APPRENTI: ["RD_RULE_3", "RD_RULE_4", "THREAD_SYSTEM"],
            StagiaireLevel.COMPAGNON: ["RD_RULE_5", "RD_RULE_6", "HUMAN_GATES"],
            StagiaireLevel.MAITRE: ["RD_RULE_7"],
        }
        
        current_level = progress.current_level
        levels = list(StagiaireLevel)
        current_index = levels.index(current_level)
        
        # Vérifier si peut passer au niveau suivant
        if current_index < len(levels) - 1:
            next_level = levels[current_index + 1]
            required = level_requirements.get(current_level, [])
            
            if all(m in progress.completed_modules for m in required):
                progress.current_level = next_level
                progress.updated_at = datetime.utcnow()
                
                logger.info(
                    f"Entity {entity_id} promoted from {current_level} to {next_level}"
                )
                
                return next_level
        
        return None
    
    async def promote_manually(
        self,
        entity_id: UUID,
        new_level: StagiaireLevel,
        promoted_by: UUID,
        reason: str
    ) -> StagiaireProgress:
        """
        Promotion manuelle par un humain autorisé.
        
        Utilisé pour des cas exceptionnels où la validation
        automatique n'est pas suffisante.
        """
        if entity_id not in self.progress_store:
            raise ValueError(f"Entity {entity_id} not enrolled")
        
        progress = self.progress_store[entity_id]
        old_level = progress.current_level
        
        progress.current_level = new_level
        progress.promoted_at = datetime.utcnow()
        progress.promoted_by = promoted_by
        progress.updated_at = datetime.utcnow()
        
        logger.info(
            f"Manual promotion {entity_id}: {old_level} -> {new_level} "
            f"by {promoted_by}. Reason: {reason}"
        )
        
        return progress
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_progress(self, entity_id: UUID) -> Optional[StagiaireProgress]:
        """Récupère la progression d'une entité."""
        return self.progress_store.get(entity_id)
    
    async def get_next_module(self, entity_id: UUID) -> Optional[KnowledgeModule]:
        """Récupère le prochain module à compléter."""
        progress = self.progress_store.get(entity_id)
        if not progress:
            return None
        
        # Trouver le premier module non complété dont les prérequis sont satisfaits
        for module_id, module in self.knowledge_modules.items():
            if module_id not in progress.completed_modules:
                prereqs_ok = all(
                    p in progress.completed_modules 
                    for p in module.prerequisites
                )
                if prereqs_ok:
                    return module
        
        return None
    
    async def is_authorized(
        self,
        entity_id: UUID,
        required_level: StagiaireLevel
    ) -> bool:
        """
        Vérifie si une entité a le niveau requis.
        
        Utilisé pour contrôler l'accès aux fonctionnalités
        basé sur le niveau de compréhension CHE·NU.
        """
        progress = self.progress_store.get(entity_id)
        if not progress:
            return False
        
        levels = list(StagiaireLevel)
        current_index = levels.index(progress.current_level)
        required_index = levels.index(required_level)
        
        return current_index >= required_index
    
    async def get_completion_stats(self) -> Dict[str, Any]:
        """Statistiques globales de complétion."""
        total = len(self.progress_store)
        if total == 0:
            return {"total": 0, "by_level": {}, "avg_score": 0}
        
        by_level = {}
        total_scores = []
        
        for progress in self.progress_store.values():
            level = progress.current_level.value
            by_level[level] = by_level.get(level, 0) + 1
            total_scores.extend(progress.validation_scores.values())
        
        return {
            "total": total,
            "by_level": by_level,
            "avg_score": sum(total_scores) / len(total_scores) if total_scores else 0
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'StagiaireEngine',
    'StagiaireLevel',
    'ValidationStatus',
    'KnowledgeModule',
    'StagiaireProgress',
    'ValidationResult',
    'CHENU_KNOWLEDGE_MODULES',
    'MODULE_VERSION',
]
