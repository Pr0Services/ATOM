"""
============================================================================
CHE·NU™ V69 — EDUCATION SKILL LATTICE
============================================================================
Spec: GPT1/CHE-NU_EDU_SKILL_LATTICE_V1.md

Objective: Eliminate "skill unemployment" by generating immediately useful nano-pathways.

Connections (per spec):
- Tableau Communautaire (local needs)
- Task Atomizer (micro-tasks)
- Trust Score (proof of competence)
- WorldEngine (simulation/validation)
- XR Pack (kinesthetic learning)

Principle: GOUVERNANCE > EXÉCUTION — Just-in-Time learning linked to action
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import logging

from ..models import (
    Skill,
    SkillCategory,
    LessonUnit,
    LearningFormat,
    Pathway,
    Assessment,
    AssessmentMode,
    AssessmentResult,
    NanoCertification,
    MentorSession,
    generate_id,
    compute_hash,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# SKILL REGISTRY
# ============================================================================

class SkillRegistry:
    """
    Registry of all skills.
    """
    
    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._skills_by_domain: Dict[str, Set[str]] = {}
    
    def register(self, skill: Skill) -> str:
        """Register a skill"""
        self._skills[skill.skill_id] = skill
        
        if skill.domain not in self._skills_by_domain:
            self._skills_by_domain[skill.domain] = set()
        self._skills_by_domain[skill.domain].add(skill.skill_id)
        
        return skill.skill_id
    
    def get(self, skill_id: str) -> Optional[Skill]:
        """Get skill by ID"""
        return self._skills.get(skill_id)
    
    def get_by_domain(self, domain: str) -> List[Skill]:
        """Get skills by domain"""
        skill_ids = self._skills_by_domain.get(domain, set())
        return [self._skills[sid] for sid in skill_ids]
    
    def search(
        self,
        query: str = None,
        domain: str = None,
        category: SkillCategory = None,
    ) -> List[Skill]:
        """Search skills"""
        results = list(self._skills.values())
        
        if domain:
            results = [s for s in results if s.domain == domain]
        
        if category:
            results = [s for s in results if s.category == category]
        
        if query:
            q = query.lower()
            results = [s for s in results if q in s.name.lower() or q in s.description.lower()]
        
        return results
    
    def get_prerequisites_tree(self, skill_id: str) -> Dict[str, List[str]]:
        """Get full prerequisite tree for a skill"""
        tree = {}
        visited = set()
        
        def traverse(sid: str):
            if sid in visited:
                return
            visited.add(sid)
            
            skill = self._skills.get(sid)
            if skill:
                tree[sid] = skill.prerequisites
                for prereq in skill.prerequisites:
                    traverse(prereq)
        
        traverse(skill_id)
        return tree


# ============================================================================
# PATHWAY MANAGER
# ============================================================================

class PathwayManager:
    """
    Manages learning pathways.
    """
    
    def __init__(self, skill_registry: SkillRegistry):
        self.skills = skill_registry
        self._pathways: Dict[str, Pathway] = {}
        self._lessons: Dict[str, List[LessonUnit]] = {}  # skill_id → lessons
        self._assessments: Dict[str, Assessment] = {}
    
    def create_pathway(
        self,
        name: str,
        skill_ids: List[str],
        description: str = "",
    ) -> Pathway:
        """Create a learning pathway"""
        # Validate skills exist
        valid_skills = [sid for sid in skill_ids if self.skills.get(sid)]
        
        # Calculate duration
        total_duration = sum(
            self.skills.get(sid).estimated_duration_minutes
            for sid in valid_skills
            if self.skills.get(sid)
        )
        
        pathway = Pathway(
            pathway_id=generate_id(),
            name=name,
            description=description,
            skills=valid_skills,
            estimated_duration_hours=total_duration / 60,
        )
        
        self._pathways[pathway.pathway_id] = pathway
        logger.info(f"Created pathway {pathway.pathway_id}: {name}")
        return pathway
    
    def add_lesson(self, lesson: LessonUnit) -> str:
        """Add a lesson to a skill"""
        if lesson.skill_id not in self._lessons:
            self._lessons[lesson.skill_id] = []
        self._lessons[lesson.skill_id].append(lesson)
        
        # Sort by order
        self._lessons[lesson.skill_id].sort(key=lambda l: l.order)
        
        return lesson.lesson_id
    
    def add_assessment(self, assessment: Assessment) -> str:
        """Add an assessment"""
        self._assessments[assessment.assessment_id] = assessment
        return assessment.assessment_id
    
    def get_lessons_for_skill(self, skill_id: str) -> List[LessonUnit]:
        """Get lessons for a skill"""
        return self._lessons.get(skill_id, [])
    
    def get_pathway(self, pathway_id: str) -> Optional[Pathway]:
        """Get pathway by ID"""
        return self._pathways.get(pathway_id)
    
    def suggest_pathway(
        self,
        need: str,
        available_time_hours: float = 2.0,
        user_skills: List[str] = None,
    ) -> Optional[Pathway]:
        """
        Suggest a pathway based on need.
        
        Per spec: recherche par besoin (besoin → skills → parcours)
        """
        user_skills = user_skills or []
        
        # Find relevant skills
        relevant = self.skills.search(query=need)
        
        if not relevant:
            return None
        
        # Filter out already acquired skills
        new_skills = [s for s in relevant if s.skill_id not in user_skills]
        
        if not new_skills:
            return None
        
        # Select skills that fit time constraint
        selected = []
        total_time = 0
        
        for skill in new_skills:
            if total_time + skill.estimated_duration_minutes <= available_time_hours * 60:
                selected.append(skill.skill_id)
                total_time += skill.estimated_duration_minutes
        
        if not selected:
            # At least one skill
            selected = [new_skills[0].skill_id]
        
        return self.create_pathway(
            name=f"Pathway for: {need}",
            skill_ids=selected,
            description=f"Auto-generated pathway based on need: {need}",
        )


# ============================================================================
# ASSESSMENT ENGINE
# ============================================================================

class AssessmentEngine:
    """
    Runs assessments and issues certifications.
    
    Per spec governance:
    - Category A: auto-learning allowed
    - Category B: simulation validation required
    - Category C: HITL supervision required
    """
    
    def __init__(
        self,
        skill_registry: SkillRegistry,
        simulation_runner: Callable = None,
    ):
        self.skills = skill_registry
        self._simulation_runner = simulation_runner or self._mock_simulation
        
        self._results: Dict[str, List[AssessmentResult]] = {}  # user_id → results
        self._certifications: Dict[str, NanoCertification] = {}
    
    def _mock_simulation(self, skill_id: str, user_id: str) -> Tuple[bool, float]:
        """Mock simulation runner"""
        # Return (passed, score)
        return True, 0.85
    
    def run_assessment(
        self,
        assessment: Assessment,
        user_id: str,
        mode_override: AssessmentMode = None,
    ) -> AssessmentResult:
        """
        Run an assessment.
        
        Per spec: mode=sim|real based on risk category
        """
        skill = self.skills.get(assessment.skill_id)
        actual_mode = mode_override or assessment.mode
        
        # Check if HITL required
        if skill and skill.category == SkillCategory.CATEGORY_C:
            assessment.requires_hitl = True
            logger.warning(f"Assessment {assessment.assessment_id} requires HITL (Category C)")
        
        # Run based on mode
        if actual_mode == AssessmentMode.SIMULATION:
            passed, score = self._simulation_runner(assessment.skill_id, user_id)
        elif actual_mode == AssessmentMode.QUIZ:
            # Mock quiz
            passed, score = True, 0.8
        else:
            # Real task - requires HITL
            assessment.requires_hitl = True
            passed, score = True, 0.9  # Would be set by human evaluator
        
        result = AssessmentResult(
            result_id=generate_id(),
            assessment_id=assessment.assessment_id,
            user_id=user_id,
            passed=passed and score >= assessment.passing_score,
            score=score,
            proof_ref=f"proof://{assessment.assessment_id}/{user_id}",
        )
        
        # Sign result
        result.signature = sign_artifact({
            "result_id": result.result_id,
            "assessment_id": result.assessment_id,
            "passed": result.passed,
            "score": result.score,
        }, "assessment_engine")
        
        # Store
        if user_id not in self._results:
            self._results[user_id] = []
        self._results[user_id].append(result)
        
        logger.info(
            f"Assessment {assessment.assessment_id} for user {user_id}: "
            f"passed={result.passed}, score={result.score:.2f}"
        )
        
        return result
    
    def issue_certification(
        self,
        skill_id: str,
        user_id: str,
        assessment_results: List[AssessmentResult],
    ) -> Optional[NanoCertification]:
        """
        Issue a nano-certification.
        
        Per spec: badge signé (Artifact) + liens de preuve
        """
        # Check all passed
        if not all(r.passed for r in assessment_results):
            logger.warning(f"Cannot issue cert for {skill_id}: not all assessments passed")
            return None
        
        skill = self.skills.get(skill_id)
        if not skill:
            return None
        
        cert = NanoCertification(
            cert_id=generate_id(),
            skill_id=skill_id,
            user_id=user_id,
            name=f"NanoCert: {skill.name}",
            scope=skill.domain,
            assessment_proofs=[r.proof_ref for r in assessment_results],
        )
        
        # Sign
        cert.signature = sign_artifact({
            "cert_id": cert.cert_id,
            "skill_id": skill_id,
            "user_id": user_id,
            "proofs": cert.assessment_proofs,
        }, "certification_authority")
        cert.signed_by = "certification_authority"
        
        self._certifications[cert.cert_id] = cert
        
        logger.info(f"Issued certification {cert.cert_id} for skill {skill_id}")
        return cert
    
    def get_user_certifications(self, user_id: str) -> List[NanoCertification]:
        """Get all certifications for a user"""
        return [c for c in self._certifications.values() if c.user_id == user_id]


# ============================================================================
# MENTOR MATCHING
# ============================================================================

class MentorMatcher:
    """
    Match learners with mentors.
    
    Per spec: mentoring P2P (citoyen ↔ citoyen)
    """
    
    def __init__(self):
        self._mentors: Dict[str, Set[str]] = {}  # skill_id → mentor_ids
        self._sessions: Dict[str, MentorSession] = {}
    
    def register_mentor(self, mentor_id: str, skill_ids: List[str]) -> None:
        """Register a mentor for skills"""
        for sid in skill_ids:
            if sid not in self._mentors:
                self._mentors[sid] = set()
            self._mentors[sid].add(mentor_id)
    
    def find_mentor(self, skill_id: str) -> Optional[str]:
        """Find available mentor for a skill"""
        mentors = self._mentors.get(skill_id, set())
        if mentors:
            return list(mentors)[0]  # Simple selection
        return None
    
    def create_session(
        self,
        mentor_id: str,
        learner_id: str,
        skill_id: str,
        scheduled_at: datetime = None,
    ) -> MentorSession:
        """Create a mentor session"""
        session = MentorSession(
            session_id=generate_id(),
            mentor_id=mentor_id,
            learner_id=learner_id,
            skill_id=skill_id,
            scheduled_at=scheduled_at or datetime.utcnow(),
        )
        
        self._sessions[session.session_id] = session
        return session


# ============================================================================
# SKILL LATTICE (MAIN ENGINE)
# ============================================================================

class SkillLattice:
    """
    Main Skill Lattice engine.
    
    Per spec: moteur d'apprentissage adaptatif
    """
    
    def __init__(self):
        self.skills = SkillRegistry()
        self.pathways = PathwayManager(self.skills)
        self.assessments = AssessmentEngine(self.skills)
        self.mentors = MentorMatcher()
        
        # User progress
        self._user_skills: Dict[str, Set[str]] = {}  # user_id → acquired skills
        self._user_progress: Dict[str, Dict[str, float]] = {}  # user_id → {skill_id: progress}
    
    def suggest_pathway(
        self,
        user_id: str,
        need: str,
        available_time_hours: float = 2.0,
    ) -> Optional[Pathway]:
        """
        Suggest a learning pathway based on need.
        
        Per spec API: POST /edu/pathways/suggest
        """
        user_skills = list(self._user_skills.get(user_id, set()))
        return self.pathways.suggest_pathway(need, available_time_hours, user_skills)
    
    def generate_lesson(
        self,
        skill_id: str,
        format: LearningFormat = LearningFormat.TEXT,
        include_xr_assets: bool = False,
    ) -> Optional[LessonUnit]:
        """
        Generate a lesson for a skill.
        
        Per spec API: POST /edu/lessons/generate
        """
        skill = self.skills.get(skill_id)
        if not skill:
            return None
        
        lesson = LessonUnit(
            lesson_id=generate_id(),
            skill_id=skill_id,
            title=f"Learn: {skill.name}",
            format=format,
            content_ref=f"content://{skill_id}",
            duration_minutes=skill.estimated_duration_minutes,
        )
        
        if include_xr_assets and format == LearningFormat.XR:
            lesson.xr_assets = [f"xr://{skill_id}/ghost_track"]
        
        self.pathways.add_lesson(lesson)
        return lesson
    
    def run_assessment(
        self,
        skill_id: str,
        user_id: str,
        mode: AssessmentMode = AssessmentMode.SIMULATION,
    ) -> AssessmentResult:
        """
        Run an assessment.
        
        Per spec API: POST /edu/assessments/run
        """
        assessment = Assessment(
            assessment_id=generate_id(),
            skill_id=skill_id,
            mode=mode,
        )
        
        return self.assessments.run_assessment(assessment, user_id)
    
    def issue_certification(
        self,
        skill_id: str,
        user_id: str,
    ) -> Optional[NanoCertification]:
        """
        Issue certification if eligible.
        
        Per spec API: POST /edu/certifications/issue
        """
        # Get all passed assessments for this skill
        all_results = self.assessments._results.get(user_id, [])
        skill_results = [r for r in all_results if r.passed]
        
        # Filter to this skill's assessments
        relevant = [r for r in skill_results if self._result_matches_skill(r, skill_id)]
        
        if not relevant:
            logger.warning(f"No passed assessments for skill {skill_id}")
            return None
        
        cert = self.assessments.issue_certification(skill_id, user_id, relevant)
        
        if cert:
            # Update user skills
            if user_id not in self._user_skills:
                self._user_skills[user_id] = set()
            self._user_skills[user_id].add(skill_id)
        
        return cert
    
    def _result_matches_skill(self, result: AssessmentResult, skill_id: str) -> bool:
        """Check if assessment result is for a skill"""
        assessment = self.pathways._assessments.get(result.assessment_id)
        if assessment:
            return assessment.skill_id == skill_id
        # Fallback: check if skill_id in proof_ref
        return skill_id in result.proof_ref
    
    def match_mentor(
        self,
        user_id: str,
        skill_id: str,
    ) -> Optional[MentorSession]:
        """
        Match user with a mentor.
        
        Per spec API: POST /edu/mentors/match
        """
        mentor_id = self.mentors.find_mentor(skill_id)
        if not mentor_id:
            return None
        
        return self.mentors.create_session(mentor_id, user_id, skill_id)
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning progress"""
        return {
            "user_id": user_id,
            "acquired_skills": list(self._user_skills.get(user_id, set())),
            "certifications": [
                c.cert_id for c in self.assessments.get_user_certifications(user_id)
            ],
            "progress": self._user_progress.get(user_id, {}),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_skill_lattice() -> SkillLattice:
    """Create a skill lattice"""
    return SkillLattice()


def create_skill(
    name: str,
    domain: str,
    category: SkillCategory = SkillCategory.CATEGORY_A,
    duration_minutes: int = 15,
) -> Skill:
    """Create a skill"""
    return Skill(
        skill_id=generate_id(),
        name=name,
        domain=domain,
        category=category,
        estimated_duration_minutes=duration_minutes,
    )
