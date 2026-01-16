"""
CHE·NU V68 Education Native Agent
Module Societaire 2/4 - L'Ecole qui ne s'arrete jamais

CONCEPT: Apprentissage par projet, adapte a la frequence de l'individu
- Connecter mentors (ceux qui savent) aux apprentis (ceux qui veulent apprendre)
- En temps reel, selon localisation
- De-cloisonner le savoir - fluide comme le signal 999Hz

PRIVACY FIRST:
- Profils d'apprentissage anonymises
- Pas de ranking des apprenants
- Match par competences, pas par identite

GOVERNANCE COMPLIANCE:
- Rule #1: Mentorat haute valeur require APPROVAL
- Rule #5: Mentors/Apprentis ALPHABETICAL, Sessions CHRONOLOGICAL
- Rule #6: Full audit trail (anonymized)
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set
from uuid import UUID, uuid4
import logging
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY HELPER
# ============================================================================

def anonymize_learner_id(learner_id: UUID) -> str:
    """Anonymize learner ID for tracking without identification"""
    salt = "CHENU_EDUCATION_SALT_999Hz"
    combined = f"{salt}{str(learner_id)}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


# ============================================================================
# ENUMS
# ============================================================================

class SkillCategory(Enum):
    """Categories de competences"""
    TECH = "tech"                    # Technologie, programmation
    CRAFT = "craft"                  # Artisanat, construction
    LANGUAGE = "language"            # Langues
    ARTS = "arts"                    # Arts, musique, dessin
    SCIENCE = "science"              # Sciences, mathematiques
    HEALTH = "health"                # Sante, bien-etre
    AGRICULTURE = "agriculture"      # Agriculture, jardinage
    BUSINESS = "business"            # Commerce, gestion
    COOKING = "cooking"              # Cuisine, nutrition
    NATURE = "nature"                # Ecologie, survie
    SPIRITUAL = "spiritual"          # Spiritualite, meditation
    SOCIAL = "social"                # Communication, leadership


class SkillLevel(Enum):
    """Niveau de competence"""
    BEGINNER = "beginner"            # Debutant
    INTERMEDIATE = "intermediate"    # Intermediaire
    ADVANCED = "advanced"            # Avance
    EXPERT = "expert"                # Expert
    MASTER = "master"                # Maitre (peut former)


class LearningStyle(Enum):
    """Style d'apprentissage prefere"""
    VISUAL = "visual"                # Apprend en voyant
    AUDITORY = "auditory"            # Apprend en ecoutant
    KINESTHETIC = "kinesthetic"      # Apprend en faisant
    READING = "reading"              # Apprend en lisant
    SOCIAL = "social"                # Apprend en groupe
    SOLITARY = "solitary"            # Apprend seul


class SessionType(Enum):
    """Type de session d'apprentissage"""
    ONE_ON_ONE = "one_on_one"        # Individuel
    SMALL_GROUP = "small_group"      # Petit groupe (2-5)
    WORKSHOP = "workshop"            # Atelier (6-20)
    PROJECT = "project"              # Projet pratique
    IMMERSION = "immersion"          # Immersion complete
    ONLINE = "online"                # En ligne


class SessionStatus(Enum):
    """Statut de la session"""
    PROPOSED = "proposed"
    PENDING_MENTOR = "pending_mentor"
    PENDING_APPROVAL = "pending_approval"  # GOVERNANCE
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MentorStatus(Enum):
    """Statut du mentor"""
    AVAILABLE = "available"
    BUSY = "busy"
    INACTIVE = "inactive"


class LearnerStatus(Enum):
    """Statut de l'apprenant"""
    SEEKING = "seeking"              # Cherche un mentor
    LEARNING = "learning"            # En apprentissage
    PAUSED = "paused"                # Pause
    GRADUATED = "graduated"          # A complete une formation


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoPoint:
    """Point geographique (precision reduite)"""
    latitude: float
    longitude: float
    name: Optional[str] = None

    def __post_init__(self):
        # PRIVACY: Reduce precision
        self.latitude = round(self.latitude, 2)
        self.longitude = round(self.longitude, 2)


@dataclass
class Skill:
    """Competence"""
    id: UUID
    category: SkillCategory
    name: str
    description: str
    level_required: SkillLevel      # Niveau requis pour enseigner
    practical: bool                  # Necessite pratique?
    tools_needed: List[str]


@dataclass
class MentorProfile:
    """Profil de mentor (anonymise)"""
    id: UUID
    mentor_hash: str                 # Anonymized ID
    status: MentorStatus

    # Competences
    skills: List[UUID]               # IDs des skills
    skill_levels: Dict[str, SkillLevel]  # skill_id -> level
    years_experience: Dict[str, int]  # skill_id -> years

    # Preferences
    teaching_styles: List[SessionType]
    max_group_size: int
    availability_hours_per_week: int

    # Localisation (anonymisee)
    area: GeoPoint
    can_travel_km: float
    can_teach_online: bool

    # Stats (pas de ranking)
    sessions_given: int
    total_hours: float

    # Audit
    created_at: datetime
    updated_at: datetime


@dataclass
class LearnerProfile:
    """Profil d'apprenant (anonymise)"""
    id: UUID
    learner_hash: str                # Anonymized ID
    status: LearnerStatus

    # Apprentissage
    learning_goals: List[UUID]       # Skills a apprendre
    current_levels: Dict[str, SkillLevel]  # skill_id -> current level
    learning_styles: List[LearningStyle]

    # Preferences
    preferred_session_types: List[SessionType]
    availability_hours_per_week: int

    # Localisation (anonymisee)
    area: GeoPoint
    can_travel_km: float
    can_learn_online: bool

    # Stats
    sessions_attended: int
    skills_acquired: int

    # Audit
    created_at: datetime
    updated_at: datetime


@dataclass
class LearningSession:
    """Session d'apprentissage"""
    id: UUID
    session_number: str              # SES-001
    status: SessionStatus

    # Participants (anonymises)
    mentor_hash: str
    learner_hashes: List[str]

    # Contenu
    skill_id: UUID
    skill_name: str
    session_type: SessionType
    topic: str
    description: str

    # Timing
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]

    # Location
    location: GeoPoint
    is_online: bool
    online_link: Optional[str]

    # Project-based (si applicable)
    project_name: Optional[str]
    project_deliverable: Optional[str]

    # GOVERNANCE
    requires_approval: bool          # High-value sessions
    approved_by_hash: Optional[str]
    approved_at: Optional[datetime]

    # Feedback (anonyme, pas de notes)
    completed_successfully: Optional[bool]
    knowledge_transferred: Optional[bool]

    # Audit
    created_at: datetime
    updated_at: datetime


@dataclass
class LearningPath:
    """Parcours d'apprentissage"""
    id: UUID
    path_number: str                 # PTH-001
    name: str
    description: str

    # Progression
    skills_sequence: List[UUID]      # Skills dans l'ordre
    estimated_hours: int
    estimated_sessions: int

    # Stats
    learners_enrolled: int
    learners_completed: int

    created_at: datetime


@dataclass
class MentorMatch:
    """Match mentor-apprenant suggere"""
    id: UUID
    mentor_hash: str
    learner_hash: str
    skill_id: UUID

    # Compatibilite
    compatibility_score: float       # 0-1
    distance_km: float
    shared_availability_hours: int

    # Statut
    status: str                      # suggested, accepted, rejected

    created_at: datetime


# ============================================================================
# EDUCATION NATIVE AGENT
# ============================================================================

class EducationNativeAgent:
    """
    CHE·NU V68 Education Native Agent
    L'ecole qui ne s'arrete jamais

    CONCEPT:
    - Le savoir est fluide comme le signal 999Hz
    - Mentors et apprentis connectes en temps reel
    - Apprentissage par projet

    PRIVACY FIRST:
    - Toutes les identites anonymisees
    - Pas de ranking des apprenants
    - Match par competences, pas par identite

    GOVERNANCE:
    - Rule #1: Mentorat haute valeur require APPROVAL
    - Rule #5: ALPHABETICAL listings
    - Rule #6: Audit trail anonymise
    """

    def __init__(self):
        self.skills: Dict[UUID, Skill] = {}
        self.mentors: Dict[UUID, MentorProfile] = {}
        self.learners: Dict[UUID, LearnerProfile] = {}
        self.sessions: Dict[UUID, LearningSession] = {}
        self.paths: Dict[UUID, LearningPath] = {}
        self.matches: Dict[UUID, MentorMatch] = {}

        # Counters
        self._session_counter = 0
        self._path_counter = 0

        # Config
        self.high_value_hours_threshold = 20  # Sessions > 20h need approval

        # Initialize default skills
        self._init_default_skills()

    def _init_default_skills(self):
        """Initialize default skill catalog"""
        default_skills = [
            (SkillCategory.TECH, "Python Programming", "Programmation Python", SkillLevel.BEGINNER, True, ["computer"]),
            (SkillCategory.TECH, "Web Development", "Developpement web", SkillLevel.BEGINNER, True, ["computer"]),
            (SkillCategory.CRAFT, "Woodworking", "Travail du bois", SkillLevel.INTERMEDIATE, True, ["tools", "wood"]),
            (SkillCategory.CRAFT, "Pottery", "Poterie", SkillLevel.BEGINNER, True, ["clay", "wheel"]),
            (SkillCategory.LANGUAGE, "Spanish", "Espagnol", SkillLevel.BEGINNER, False, []),
            (SkillCategory.LANGUAGE, "Maya", "Langue Maya", SkillLevel.BEGINNER, False, []),
            (SkillCategory.ARTS, "Painting", "Peinture", SkillLevel.BEGINNER, True, ["canvas", "paints"]),
            (SkillCategory.ARTS, "Music", "Musique", SkillLevel.BEGINNER, True, ["instrument"]),
            (SkillCategory.AGRICULTURE, "Permaculture", "Permaculture", SkillLevel.BEGINNER, True, ["land"]),
            (SkillCategory.AGRICULTURE, "Beekeeping", "Apiculture", SkillLevel.INTERMEDIATE, True, ["hives", "equipment"]),
            (SkillCategory.COOKING, "Traditional Cuisine", "Cuisine traditionnelle", SkillLevel.BEGINNER, True, ["kitchen"]),
            (SkillCategory.HEALTH, "Yoga", "Yoga", SkillLevel.BEGINNER, True, ["mat"]),
            (SkillCategory.HEALTH, "Herbalism", "Herboristerie", SkillLevel.INTERMEDIATE, True, ["herbs"]),
            (SkillCategory.NATURE, "Survival Skills", "Survie en nature", SkillLevel.INTERMEDIATE, True, []),
            (SkillCategory.SPIRITUAL, "Meditation", "Meditation", SkillLevel.BEGINNER, False, []),
        ]

        for cat, name, desc, level, practical, tools in default_skills:
            skill = Skill(
                id=uuid4(),
                category=cat,
                name=name,
                description=desc,
                level_required=level,
                practical=practical,
                tools_needed=tools
            )
            self.skills[skill.id] = skill

    # ========================================================================
    # SKILL MANAGEMENT
    # ========================================================================

    async def register_skill(
        self,
        category: SkillCategory,
        name: str,
        description: str,
        level_required: SkillLevel,
        practical: bool,
        tools_needed: List[str]
    ) -> Skill:
        """Register a new skill"""
        skill = Skill(
            id=uuid4(),
            category=category,
            name=name,
            description=description,
            level_required=level_required,
            practical=practical,
            tools_needed=tools_needed
        )

        self.skills[skill.id] = skill
        logger.info(f"Skill registered: {name} ({category.value})")
        return skill

    async def get_skills(
        self,
        category: Optional[SkillCategory] = None
    ) -> List[Skill]:
        """
        Get skills - ALPHABETICAL by name (Rule #5)
        """
        skills = list(self.skills.values())

        if category:
            skills = [s for s in skills if s.category == category]

        return sorted(skills, key=lambda s: s.name.lower())

    # ========================================================================
    # MENTOR MANAGEMENT
    # ========================================================================

    async def register_mentor(
        self,
        mentor_id: UUID,  # Will be anonymized
        skills: List[UUID],
        skill_levels: Dict[str, SkillLevel],
        years_experience: Dict[str, int],
        teaching_styles: List[SessionType],
        max_group_size: int,
        availability_hours: int,
        latitude: float,
        longitude: float,
        area_name: str,
        can_travel_km: float,
        can_teach_online: bool
    ) -> MentorProfile:
        """
        Register a mentor
        PRIVACY: ID is anonymized immediately
        """
        now = datetime.utcnow()

        mentor = MentorProfile(
            id=uuid4(),
            mentor_hash=anonymize_learner_id(mentor_id),  # PRIVACY
            status=MentorStatus.AVAILABLE,
            skills=skills,
            skill_levels=skill_levels,
            years_experience=years_experience,
            teaching_styles=teaching_styles,
            max_group_size=max_group_size,
            availability_hours_per_week=availability_hours,
            area=GeoPoint(latitude, longitude, area_name),
            can_travel_km=can_travel_km,
            can_teach_online=can_teach_online,
            sessions_given=0,
            total_hours=0,
            created_at=now,
            updated_at=now
        )

        self.mentors[mentor.id] = mentor
        logger.info(f"Mentor registered with {len(skills)} skills")
        return mentor

    async def get_mentors(
        self,
        skill_id: Optional[UUID] = None,
        category: Optional[SkillCategory] = None
    ) -> List[MentorProfile]:
        """
        Get available mentors - ALPHABETICAL by hash (Rule #5)
        NOT sorted by rating or experience
        """
        mentors = [m for m in self.mentors.values()
                  if m.status == MentorStatus.AVAILABLE]

        if skill_id:
            mentors = [m for m in mentors if skill_id in m.skills]

        if category:
            category_skills = [s.id for s in self.skills.values()
                              if s.category == category]
            mentors = [m for m in mentors
                      if any(s in m.skills for s in category_skills)]

        # RULE #5: ALPHABETICAL by hash (not by experience/rating)
        return sorted(mentors, key=lambda m: m.mentor_hash)

    # ========================================================================
    # LEARNER MANAGEMENT
    # ========================================================================

    async def register_learner(
        self,
        learner_id: UUID,  # Will be anonymized
        learning_goals: List[UUID],
        current_levels: Dict[str, SkillLevel],
        learning_styles: List[LearningStyle],
        preferred_sessions: List[SessionType],
        availability_hours: int,
        latitude: float,
        longitude: float,
        area_name: str,
        can_travel_km: float,
        can_learn_online: bool
    ) -> LearnerProfile:
        """
        Register a learner
        PRIVACY: ID is anonymized immediately
        """
        now = datetime.utcnow()

        learner = LearnerProfile(
            id=uuid4(),
            learner_hash=anonymize_learner_id(learner_id),  # PRIVACY
            status=LearnerStatus.SEEKING,
            learning_goals=learning_goals,
            current_levels=current_levels,
            learning_styles=learning_styles,
            preferred_session_types=preferred_sessions,
            availability_hours_per_week=availability_hours,
            area=GeoPoint(latitude, longitude, area_name),
            can_travel_km=can_travel_km,
            can_learn_online=can_learn_online,
            sessions_attended=0,
            skills_acquired=0,
            created_at=now,
            updated_at=now
        )

        self.learners[learner.id] = learner
        logger.info(f"Learner registered with {len(learning_goals)} goals")

        # Auto-match with mentors
        await self._auto_match_learner(learner.id)

        return learner

    async def get_learners(
        self,
        skill_id: Optional[UUID] = None
    ) -> List[LearnerProfile]:
        """
        Get learners seeking - ALPHABETICAL by hash (Rule #5)
        """
        learners = [l for l in self.learners.values()
                   if l.status == LearnerStatus.SEEKING]

        if skill_id:
            learners = [l for l in learners if skill_id in l.learning_goals]

        # RULE #5: ALPHABETICAL
        return sorted(learners, key=lambda l: l.learner_hash)

    # ========================================================================
    # MATCHING
    # ========================================================================

    async def _calculate_compatibility(
        self,
        mentor: MentorProfile,
        learner: LearnerProfile,
        skill_id: UUID
    ) -> float:
        """Calculate mentor-learner compatibility score"""
        score = 0.0

        # Location compatibility
        if mentor.can_teach_online and learner.can_learn_online:
            score += 0.2
        else:
            # Check distance
            import math
            R = 6371
            lat1, lon1 = math.radians(mentor.area.latitude), math.radians(mentor.area.longitude)
            lat2, lon2 = math.radians(learner.area.latitude), math.radians(learner.area.longitude)
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            distance = R * 2 * math.asin(math.sqrt(a))

            if distance <= min(mentor.can_travel_km, learner.can_travel_km):
                score += 0.2

        # Session type compatibility
        common_types = set(mentor.teaching_styles) & set(learner.preferred_session_types)
        if common_types:
            score += 0.2

        # Availability overlap
        overlap = min(mentor.availability_hours_per_week, learner.availability_hours_per_week)
        if overlap >= 2:
            score += 0.2

        # Skill match
        if skill_id in mentor.skills:
            mentor_level = mentor.skill_levels.get(str(skill_id))
            learner_level = learner.current_levels.get(str(skill_id), SkillLevel.BEGINNER)

            if mentor_level and mentor_level.value > learner_level.value:
                score += 0.2

        return min(1.0, score)

    async def _auto_match_learner(self, learner_id: UUID) -> List[MentorMatch]:
        """Auto-find matching mentors for a learner"""
        if learner_id not in self.learners:
            return []

        learner = self.learners[learner_id]
        matches = []

        for goal_skill in learner.learning_goals:
            for mentor in self.mentors.values():
                if mentor.status != MentorStatus.AVAILABLE:
                    continue

                if goal_skill not in mentor.skills:
                    continue

                compatibility = await self._calculate_compatibility(
                    mentor, learner, goal_skill
                )

                if compatibility >= 0.4:  # Threshold
                    match = MentorMatch(
                        id=uuid4(),
                        mentor_hash=mentor.mentor_hash,
                        learner_hash=learner.learner_hash,
                        skill_id=goal_skill,
                        compatibility_score=compatibility,
                        distance_km=0,  # Simplified
                        shared_availability_hours=min(
                            mentor.availability_hours_per_week,
                            learner.availability_hours_per_week
                        ),
                        status="suggested",
                        created_at=datetime.utcnow()
                    )

                    self.matches[match.id] = match
                    matches.append(match)

        return matches

    async def get_mentor_matches(
        self,
        learner_id: Optional[UUID] = None
    ) -> List[MentorMatch]:
        """Get suggested matches - CHRONOLOGICAL (Rule #5)"""
        matches = [m for m in self.matches.values() if m.status == "suggested"]

        if learner_id and learner_id in self.learners:
            learner = self.learners[learner_id]
            matches = [m for m in matches if m.learner_hash == learner.learner_hash]

        return sorted(matches, key=lambda m: m.created_at, reverse=True)

    # ========================================================================
    # SESSION MANAGEMENT
    # ========================================================================

    async def propose_session(
        self,
        mentor_id: UUID,
        learner_ids: List[UUID],
        skill_id: UUID,
        session_type: SessionType,
        topic: str,
        description: str,
        scheduled_start: datetime,
        scheduled_end: datetime,
        latitude: float,
        longitude: float,
        location_name: str,
        is_online: bool = False,
        online_link: Optional[str] = None,
        project_name: Optional[str] = None,
        project_deliverable: Optional[str] = None
    ) -> LearningSession:
        """Propose a learning session"""
        self._session_counter += 1
        session_number = f"SES-{self._session_counter:04d}"

        # Get skill name
        skill = self.skills.get(skill_id)
        skill_name = skill.name if skill else "Unknown"

        # Calculate duration
        duration_hours = (scheduled_end - scheduled_start).total_seconds() / 3600

        # High value if many hours or many learners
        requires_approval = (
            duration_hours >= self.high_value_hours_threshold or
            len(learner_ids) > 5
        )

        # Anonymize IDs
        mentor_hash = anonymize_learner_id(mentor_id)
        learner_hashes = [anonymize_learner_id(lid) for lid in learner_ids]

        now = datetime.utcnow()

        session = LearningSession(
            id=uuid4(),
            session_number=session_number,
            status=SessionStatus.PROPOSED,
            mentor_hash=mentor_hash,
            learner_hashes=learner_hashes,
            skill_id=skill_id,
            skill_name=skill_name,
            session_type=session_type,
            topic=topic,
            description=description,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            actual_start=None,
            actual_end=None,
            location=GeoPoint(latitude, longitude, location_name),
            is_online=is_online,
            online_link=online_link,
            project_name=project_name,
            project_deliverable=project_deliverable,
            requires_approval=requires_approval,
            approved_by_hash=None,
            approved_at=None,
            completed_successfully=None,
            knowledge_transferred=None,
            created_at=now,
            updated_at=now
        )

        self.sessions[session.id] = session

        if requires_approval:
            logger.info(f"GOVERNANCE: Session {session_number} requires approval")
        else:
            logger.info(f"Session proposed: {session_number} - {skill_name}")

        return session

    async def confirm_session(
        self,
        session_id: UUID
    ) -> LearningSession:
        """Confirm a session (after mentor accepts)"""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")

        session = self.sessions[session_id]

        if session.requires_approval:
            session.status = SessionStatus.PENDING_APPROVAL
        else:
            session.status = SessionStatus.CONFIRMED

        session.updated_at = datetime.utcnow()
        return session

    async def approve_session(
        self,
        session_id: UUID,
        approved: bool,
        approver_id: UUID
    ) -> LearningSession:
        """
        GOVERNANCE - Rule #1: Approve high-value session
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")

        session = self.sessions[session_id]

        if not session.requires_approval:
            raise ValueError("Session does not require approval")

        session.approved_by_hash = anonymize_learner_id(approver_id)
        session.approved_at = datetime.utcnow()

        if approved:
            session.status = SessionStatus.CONFIRMED
            logger.info(f"GOVERNANCE: Session {session.session_number} APPROVED")
        else:
            session.status = SessionStatus.CANCELLED
            logger.info(f"GOVERNANCE: Session {session.session_number} REJECTED")

        session.updated_at = datetime.utcnow()
        return session

    async def start_session(
        self,
        session_id: UUID
    ) -> LearningSession:
        """Start a session"""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")

        session = self.sessions[session_id]
        session.status = SessionStatus.IN_PROGRESS
        session.actual_start = datetime.utcnow()
        session.updated_at = datetime.utcnow()

        logger.info(f"Session {session.session_number} started")
        return session

    async def complete_session(
        self,
        session_id: UUID,
        successful: bool,
        knowledge_transferred: bool
    ) -> LearningSession:
        """Complete a session"""
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")

        session = self.sessions[session_id]
        session.status = SessionStatus.COMPLETED
        session.actual_end = datetime.utcnow()
        session.completed_successfully = successful
        session.knowledge_transferred = knowledge_transferred
        session.updated_at = datetime.utcnow()

        # Update mentor stats
        for mentor in self.mentors.values():
            if mentor.mentor_hash == session.mentor_hash:
                mentor.sessions_given += 1
                duration = (session.actual_end - session.actual_start).total_seconds() / 3600
                mentor.total_hours += duration
                break

        # Update learner stats
        for learner in self.learners.values():
            if learner.learner_hash in session.learner_hashes:
                learner.sessions_attended += 1
                if knowledge_transferred:
                    learner.skills_acquired += 1

        logger.info(f"Session {session.session_number} completed")
        return session

    async def get_sessions(
        self,
        status: Optional[SessionStatus] = None
    ) -> List[LearningSession]:
        """
        Get sessions - CHRONOLOGICAL (Rule #5)
        """
        sessions = list(self.sessions.values())

        if status:
            sessions = [s for s in sessions if s.status == status]

        # RULE #5: CHRONOLOGICAL
        return sorted(sessions, key=lambda s: s.scheduled_start, reverse=True)

    # ========================================================================
    # LEARNING PATHS
    # ========================================================================

    async def create_learning_path(
        self,
        name: str,
        description: str,
        skills_sequence: List[UUID],
        estimated_hours: int
    ) -> LearningPath:
        """Create a learning path"""
        self._path_counter += 1
        path_number = f"PTH-{self._path_counter:04d}"

        path = LearningPath(
            id=uuid4(),
            path_number=path_number,
            name=name,
            description=description,
            skills_sequence=skills_sequence,
            estimated_hours=estimated_hours,
            estimated_sessions=len(skills_sequence) * 3,  # ~3 sessions per skill
            learners_enrolled=0,
            learners_completed=0,
            created_at=datetime.utcnow()
        )

        self.paths[path.id] = path
        logger.info(f"Learning path created: {name}")
        return path

    async def get_learning_paths(self) -> List[LearningPath]:
        """Get learning paths - ALPHABETICAL (Rule #5)"""
        return sorted(self.paths.values(), key=lambda p: p.name.lower())

    # ========================================================================
    # METRICS
    # ========================================================================

    async def get_education_metrics(self) -> Dict[str, Any]:
        """Get education system metrics"""
        active_mentors = len([m for m in self.mentors.values()
                             if m.status == MentorStatus.AVAILABLE])
        active_learners = len([l for l in self.learners.values()
                              if l.status in [LearnerStatus.SEEKING, LearnerStatus.LEARNING]])

        completed_sessions = [s for s in self.sessions.values()
                             if s.status == SessionStatus.COMPLETED]

        total_hours = sum(
            (s.actual_end - s.actual_start).total_seconds() / 3600
            for s in completed_sessions
            if s.actual_end and s.actual_start
        )

        knowledge_rate = (
            len([s for s in completed_sessions if s.knowledge_transferred]) /
            len(completed_sessions) if completed_sessions else 0
        )

        # Knowledge fluidity index
        fluidity = 0.0
        if active_mentors > 0 and active_learners > 0:
            matches_made = len([m for m in self.matches.values() if m.status == "accepted"])
            potential = active_mentors * active_learners
            fluidity = min(1.0, matches_made / potential * 10)

        # Color based on fluidity
        if fluidity > 0.8:
            color = "#0057b8"
            status = "optimal"
        elif fluidity > 0.5:
            color = "#28a745"
            status = "good"
        elif fluidity > 0.2:
            color = "#fd7e14"
            status = "needs_mentors"
        else:
            color = "#dc3545"
            status = "critical"

        return {
            "fluidity_index": round(fluidity, 2),
            "status": status,
            "color_hex": color,
            "message": self._get_education_message(fluidity),
            "mentors": {
                "total": len(self.mentors),
                "available": active_mentors
            },
            "learners": {
                "total": len(self.learners),
                "active": active_learners
            },
            "sessions": {
                "total": len(self.sessions),
                "completed": len(completed_sessions),
                "total_hours": round(total_hours, 1),
                "knowledge_transfer_rate": round(knowledge_rate * 100, 1)
            },
            "skills": {
                "available": len(self.skills),
                "categories": len(set(s.category for s in self.skills.values()))
            },
            "privacy": {
                "all_identities_anonymized": True,
                "no_learner_ranking": True
            }
        }

    def _get_education_message(self, fluidity: float) -> str:
        """Get message for education fluidity"""
        if fluidity > 0.8:
            return "Le savoir circule librement - 999Hz atteint"
        elif fluidity > 0.5:
            return "Bonne transmission - Plus de mentors augmenterait le flux"
        elif fluidity > 0.2:
            return "Des apprenants cherchent - Mentors necessaires"
        else:
            return "Le savoir est bloque - Intervention requise"


# Singleton
_education_agent: Optional[EducationNativeAgent] = None


def get_education_native_agent() -> EducationNativeAgent:
    """Get or create education agent singleton"""
    global _education_agent
    if _education_agent is None:
        _education_agent = EducationNativeAgent()
    return _education_agent
