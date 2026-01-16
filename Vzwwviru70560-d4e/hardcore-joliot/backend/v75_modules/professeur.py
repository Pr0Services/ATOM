"""
CHE·NU V75 - MODULE PROFESSEUR
==============================
Système de mentorat et validation des connaissances.
Complémente le module Stagiaire avec des capacités d'évaluation et guidage.

PRINCIPES:
- GOUVERNANCE > EXÉCUTION
- Human Sovereignty (toute évaluation = checkpoint)
- Traçabilité complète des évaluations
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel

# ============================================================================
# ENUMS
# ============================================================================

class EvaluationType(str, Enum):
    """Types d'évaluation"""
    SKILL_ASSESSMENT = "skill_assessment"
    CODE_REVIEW = "code_review"
    DOCUMENT_REVIEW = "document_review"
    PROGRESS_CHECK = "progress_check"
    FINAL_VALIDATION = "final_validation"
    KNOWLEDGE_TEST = "knowledge_test"


class MentorshipLevel(str, Enum):
    """Niveaux de mentorat"""
    OBSERVER = "observer"          # Observe seulement
    GUIDE = "guide"                # Guide avec suggestions
    INSTRUCTOR = "instructor"      # Instruit activement
    EVALUATOR = "evaluator"        # Évalue et valide
    MASTER = "master"              # Autorité finale


class FeedbackSeverity(str, Enum):
    """Sévérité du feedback"""
    PRAISE = "praise"              # Félicitation
    SUGGESTION = "suggestion"       # Suggestion d'amélioration
    CORRECTION = "correction"       # Correction nécessaire
    BLOCKER = "blocker"            # Bloqueur - checkpoint requis


# ============================================================================
# SCHEMAS
# ============================================================================

class EvaluationCriteria(BaseModel):
    """Critères d'évaluation"""
    name: str
    weight: float  # 0.0 - 1.0
    description: str
    min_score: float = 0.0
    max_score: float = 100.0
    required: bool = True


class FeedbackItem(BaseModel):
    """Item de feedback individuel"""
    id: str = field(default_factory=lambda: str(uuid4()))
    criterion: str
    score: float
    severity: FeedbackSeverity
    comment: str
    suggestions: List[str] = []
    code_references: List[str] = []  # Références au code si applicable
    created_at: datetime = field(default_factory=datetime.utcnow)


class EvaluationResult(BaseModel):
    """Résultat d'une évaluation"""
    id: str = field(default_factory=lambda: str(uuid4()))
    evaluation_type: EvaluationType
    subject_id: str  # ID de ce qui est évalué (stagiaire, document, code)
    evaluator_id: str
    criteria_scores: Dict[str, float]
    overall_score: float
    passed: bool
    feedback_items: List[FeedbackItem]
    next_steps: List[str]
    requires_checkpoint: bool = False
    checkpoint_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class MentorProfile(BaseModel):
    """Profil d'un mentor/professeur"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str
    level: MentorshipLevel
    specializations: List[str]
    spheres: List[str]  # Sphères autorisées
    evaluations_count: int = 0
    average_rating: float = 0.0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


class LearningPath(BaseModel):
    """Parcours d'apprentissage défini par un professeur"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    mentor_id: str
    sphere: str
    stages: List[Dict[str, Any]]  # Étapes du parcours
    prerequisites: List[str]
    estimated_duration_hours: int
    difficulty_level: int  # 1-10
    is_published: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# SERVICE PROFESSEUR
# ============================================================================

class ProfesseurService:
    """
    Service Professeur V75
    
    Gère le mentorat, l'évaluation et la validation des apprentissages.
    Respecte les principes Canon:
    - Toute évaluation finale = checkpoint humain
    - Feedback tracé intégralement
    - NO autonomous grading without human oversight
    """
    
    def __init__(self):
        self.mentors: Dict[str, MentorProfile] = {}
        self.evaluations: Dict[str, EvaluationResult] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        self.pending_checkpoints: Dict[str, Dict] = {}
        
    # ========================================================================
    # MENTOR MANAGEMENT
    # ========================================================================
    
    async def register_mentor(
        self,
        user_id: str,
        level: MentorshipLevel,
        specializations: List[str],
        spheres: List[str],
        approved_by: str
    ) -> MentorProfile:
        """
        Enregistre un nouveau mentor.
        CHECKPOINT: Registration nécessite approbation.
        """
        # Vérifier niveau approprié
        if level in [MentorshipLevel.EVALUATOR, MentorshipLevel.MASTER]:
            # Niveau supérieur = checkpoint obligatoire
            checkpoint = await self._create_checkpoint(
                action="register_mentor",
                data={
                    "user_id": user_id,
                    "level": level.value,
                    "specializations": specializations
                },
                reason="High-level mentor registration requires approval"
            )
            self.pending_checkpoints[checkpoint["id"]] = checkpoint
            return checkpoint
        
        mentor = MentorProfile(
            user_id=user_id,
            level=level,
            specializations=specializations,
            spheres=spheres
        )
        self.mentors[mentor.id] = mentor
        
        return mentor
    
    async def get_mentor(self, mentor_id: str) -> Optional[MentorProfile]:
        """Récupère un profil mentor"""
        return self.mentors.get(mentor_id)
    
    async def list_mentors_by_sphere(self, sphere: str) -> List[MentorProfile]:
        """Liste les mentors disponibles pour une sphère"""
        return [
            m for m in self.mentors.values()
            if sphere in m.spheres and m.is_active
        ]
    
    # ========================================================================
    # EVALUATION SYSTEM
    # ========================================================================
    
    async def create_evaluation(
        self,
        evaluation_type: EvaluationType,
        subject_id: str,
        evaluator_id: str,
        criteria: List[EvaluationCriteria]
    ) -> Dict[str, Any]:
        """
        Crée une nouvelle évaluation.
        Retourne les critères à évaluer.
        """
        evaluation_id = str(uuid4())
        
        return {
            "evaluation_id": evaluation_id,
            "type": evaluation_type.value,
            "subject_id": subject_id,
            "evaluator_id": evaluator_id,
            "criteria": [c.dict() for c in criteria],
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def submit_evaluation(
        self,
        evaluation_id: str,
        evaluator_id: str,
        scores: Dict[str, float],
        feedback_items: List[FeedbackItem],
        recommendation: str
    ) -> EvaluationResult:
        """
        Soumet une évaluation complète.
        CHECKPOINT si évaluation finale ou score faible.
        """
        # Calculer score global
        if scores:
            overall_score = sum(scores.values()) / len(scores)
        else:
            overall_score = 0.0
        
        passed = overall_score >= 70.0  # Seuil de passage
        
        # Déterminer si checkpoint requis
        requires_checkpoint = False
        blocker_feedback = [f for f in feedback_items if f.severity == FeedbackSeverity.BLOCKER]
        
        if blocker_feedback or overall_score < 50.0:
            requires_checkpoint = True
        
        result = EvaluationResult(
            id=evaluation_id,
            evaluation_type=EvaluationType.PROGRESS_CHECK,  # À ajuster
            subject_id="",  # À remplir
            evaluator_id=evaluator_id,
            criteria_scores=scores,
            overall_score=overall_score,
            passed=passed,
            feedback_items=feedback_items,
            next_steps=self._generate_next_steps(scores, passed),
            requires_checkpoint=requires_checkpoint
        )
        
        if requires_checkpoint:
            checkpoint = await self._create_checkpoint(
                action="submit_evaluation",
                data=result.dict(),
                reason="Evaluation requires human review before finalization"
            )
            result.checkpoint_id = checkpoint["id"]
            self.pending_checkpoints[checkpoint["id"]] = checkpoint
        
        self.evaluations[result.id] = result
        return result
    
    async def review_code(
        self,
        code_content: str,
        language: str,
        mentor_id: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Review de code par un professeur.
        Analyse qualité, bonnes pratiques, sécurité.
        """
        review = {
            "id": str(uuid4()),
            "mentor_id": mentor_id,
            "language": language,
            "analysis": {
                "lines_count": len(code_content.split('\n')),
                "structure": "analyzed",
                "quality_score": 0,
                "security_issues": [],
                "best_practices": [],
                "suggestions": []
            },
            "feedback": [],
            "status": "draft",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Analyse basique
        lines = code_content.split('\n')
        
        # Vérifications de base
        issues = []
        suggestions = []
        
        # Check docstrings (Python)
        if language.lower() == "python":
            if '"""' not in code_content and "'''" not in code_content:
                suggestions.append("Ajouter des docstrings pour documenter le code")
            
            # Check type hints
            if "def " in code_content and "->" not in code_content:
                suggestions.append("Ajouter des type hints pour les fonctions")
            
            # Security checks
            if "eval(" in code_content or "exec(" in code_content:
                issues.append({
                    "type": "security",
                    "severity": "high",
                    "message": "Utilisation de eval/exec détectée - risque de sécurité"
                })
        
        review["analysis"]["security_issues"] = issues
        review["analysis"]["suggestions"] = suggestions
        review["analysis"]["quality_score"] = 85 - (len(issues) * 10)
        
        return review
    
    # ========================================================================
    # LEARNING PATHS
    # ========================================================================
    
    async def create_learning_path(
        self,
        name: str,
        description: str,
        mentor_id: str,
        sphere: str,
        stages: List[Dict[str, Any]],
        difficulty: int = 5
    ) -> LearningPath:
        """Crée un nouveau parcours d'apprentissage"""
        path = LearningPath(
            name=name,
            description=description,
            mentor_id=mentor_id,
            sphere=sphere,
            stages=stages,
            difficulty_level=difficulty,
            estimated_duration_hours=len(stages) * 4  # Estimation
        )
        self.learning_paths[path.id] = path
        return path
    
    async def assign_learning_path(
        self,
        path_id: str,
        stagiaire_id: str,
        mentor_id: str
    ) -> Dict[str, Any]:
        """Assigne un parcours d'apprentissage à un stagiaire"""
        path = self.learning_paths.get(path_id)
        if not path:
            raise ValueError(f"Learning path {path_id} not found")
        
        return {
            "assignment_id": str(uuid4()),
            "path_id": path_id,
            "path_name": path.name,
            "stagiaire_id": stagiaire_id,
            "mentor_id": mentor_id,
            "stages_total": len(path.stages),
            "stages_completed": 0,
            "progress_percentage": 0,
            "started_at": datetime.utcnow().isoformat(),
            "status": "in_progress"
        }
    
    async def validate_stage_completion(
        self,
        assignment_id: str,
        stage_index: int,
        mentor_id: str,
        passed: bool,
        feedback: str
    ) -> Dict[str, Any]:
        """
        Valide la complétion d'une étape par le mentor.
        CHECKPOINT si étape finale.
        """
        result = {
            "assignment_id": assignment_id,
            "stage_index": stage_index,
            "validated_by": mentor_id,
            "passed": passed,
            "feedback": feedback,
            "validated_at": datetime.utcnow().isoformat()
        }
        
        # TODO: Ajouter checkpoint si étape finale
        
        return result
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _generate_next_steps(self, scores: Dict[str, float], passed: bool) -> List[str]:
        """Génère les prochaines étapes basées sur les scores"""
        next_steps = []
        
        if not passed:
            # Identifier les critères faibles
            weak_areas = [k for k, v in scores.items() if v < 70]
            if weak_areas:
                next_steps.append(f"Renforcer les compétences: {', '.join(weak_areas)}")
            next_steps.append("Revoir le matériel de formation")
            next_steps.append("Planifier une session avec le mentor")
        else:
            if all(v >= 90 for v in scores.values()):
                next_steps.append("Excellent travail! Prêt pour le niveau suivant")
            else:
                next_steps.append("Continuer la pratique sur les points à améliorer")
                next_steps.append("Progresser vers les modules avancés")
        
        return next_steps
    
    async def _create_checkpoint(
        self,
        action: str,
        data: Dict,
        reason: str
    ) -> Dict[str, Any]:
        """Crée un checkpoint pour validation humaine"""
        return {
            "id": str(uuid4()),
            "type": "professeur_validation",
            "action": action,
            "data": data,
            "reason": reason,
            "status": "pending",
            "requires_approval": True,
            "created_at": datetime.utcnow().isoformat()
        }


# ============================================================================
# INSTANCE GLOBALE
# ============================================================================

professeur_service = ProfesseurService()


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'ProfesseurService',
    'professeur_service',
    'EvaluationType',
    'MentorshipLevel',
    'FeedbackSeverity',
    'EvaluationCriteria',
    'FeedbackItem',
    'EvaluationResult',
    'MentorProfile',
    'LearningPath'
]
