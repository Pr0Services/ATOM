"""
CHE·NU V68 Génie de Demain Agent
Module Jeunesse - L'Allumage du Feu Intérieur

═══════════════════════════════════════════════════════════════════════════════
"L'éducation n'est pas un remplissage de vase, mais l'allumage d'un feu."
                                        - Plutarque, repris par Yeats
═══════════════════════════════════════════════════════════════════════════════

PHILOSOPHIE FONDAMENTALE:
L'école standardisée produit des suiveurs. Nous cultivons des créateurs souverains.
- Pas de classes par âge → Des CLANS par passion
- Pas de notes → Des ACCOMPLISSEMENTS
- Pas de cours magistraux → L'APPRENTISSAGE PAR LE RÉEL
- Pas de conformité → Le GÉNIE INDIVIDUEL

LES 3 PILIERS:

1. LE CLAN (L'Éducation en Équipe)
   - Groupes formés par INTÉRÊT, pas par âge
   - Un enfant de 8 ans peut collaborer avec un ado de 15 ans
   - Projets réels sur les modules AT·OM (Énergie, Construction, Transport)
   - Rotation des rôles: apprenti → contributeur → mentor

2. L'AGENT MENTOR (Intelligence Adaptative)
   - Analyse des forces, passions, rythme d'apprentissage
   - Parcours sur mesure pour chaque enfant
   - Détection du génie unique (pas des lacunes)
   - Jamais de comparaison entre enfants

3. L'APPRENTISSAGE PAR LE RÉEL
   - Simulation d'abord, réel ensuite
   - Participation aux vrais projets AT·OM
   - Le monde est la salle de classe
   - Pas de murs, pas de pupitres - la nature et la technologie

ANTI-PATTERNS (Ce que nous NE faisons JAMAIS):
- JAMAIS de classement des enfants
- JAMAIS de notes numériques
- JAMAIS de comparaison entre pairs
- JAMAIS d'apprentissage purement théorique
- JAMAIS de punition pour l'échec (l'échec est apprentissage)

PRIVACY ULTRA-STRICT (Protection des Mineurs):
- Données minimales, anonymisées
- Pas de profil comportemental détaillé
- Consentement parental explicite
- Droit à l'oubli total à la majorité

GOVERNANCE COMPLIANCE:
- Rule #1: Toute participation à un projet réel require APPROVAL PARENTAL
- Rule #5: Clans ALPHABETICAL, Accomplissements CHRONOLOGICAL
- Rule #6: Audit trail complet mais anonymisé
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Tuple
from uuid import UUID, uuid4
import logging
import hashlib
import random

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY ULTRA-STRICT (Protection des Mineurs)
# ============================================================================

def anonymize_young_learner(learner_id: UUID, clan_id: UUID) -> str:
    """
    Anonymisation renforcée pour les mineurs
    Double-hash avec rotation par clan pour empêcher le tracking cross-clan
    """
    salt = "CHENU_GENIE_DEMAIN_PROTECTION_999Hz"
    combined = f"{salt}{str(learner_id)}{str(clan_id)}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()[:12]


def anonymize_passion_profile(passions: List[str]) -> str:
    """
    Anonymise le profil de passions en catégories génériques
    Ne jamais stocker les passions exactes
    """
    categories = set()
    passion_map = {
        "tech": ["code", "robot", "ia", "ordinateur", "jeux video", "electronique"],
        "nature": ["animaux", "plantes", "ocean", "foret", "ecologie", "climat"],
        "art": ["dessin", "musique", "danse", "theatre", "sculpture", "photo"],
        "science": ["espace", "chimie", "physique", "biologie", "maths", "experience"],
        "social": ["aide", "communaute", "leadership", "communication", "politique"],
        "craft": ["construction", "menuiserie", "couture", "cuisine", "mecanique"],
    }

    for passion in passions:
        passion_lower = passion.lower()
        for category, keywords in passion_map.items():
            if any(kw in passion_lower for kw in keywords):
                categories.add(category)

    return ",".join(sorted(categories)) if categories else "explorateur"


# ============================================================================
# ENUMS
# ============================================================================

class PassionDomain(Enum):
    """Domaines de passion (pas des matières scolaires!)"""
    CREATION_TECH = "creation_tech"          # Créer avec la technologie
    EXPLORATION_NATURE = "exploration_nature"  # Explorer la nature
    EXPRESSION_ART = "expression_art"        # S'exprimer par l'art
    DECOUVERTE_SCIENCE = "decouverte_science"  # Découvrir par la science
    CONNECTION_SOCIAL = "connection_social"   # Connecter les humains
    CONSTRUCTION_CRAFT = "construction_craft"  # Construire de ses mains
    MOUVEMENT_CORPS = "mouvement_corps"       # Maîtriser son corps
    NARRATION_STORY = "narration_story"       # Raconter des histoires


class LearningRhythm(Enum):
    """Rythme d'apprentissage naturel (pas rapide/lent - différent!)"""
    EXPLORATEUR = "explorateur"      # Touche à tout, papillonne, synthétise
    PLONGEUR = "plongeur"            # S'immerge profondément dans un sujet
    CYCLIQUE = "cyclique"            # Alterne intensité et repos
    CONSTANT = "constant"            # Progression régulière
    EXPLOSIF = "explosif"            # Sprints d'apprentissage intenses


class GeniusType(Enum):
    """Types de génie (chaque enfant en a un!)"""
    INVENTEUR = "inventeur"          # Crée des solutions nouvelles
    CONNECTEUR = "connecteur"        # Relie les idées et les gens
    ARTISAN = "artisan"              # Maîtrise technique parfaite
    VISIONNAIRE = "visionnaire"      # Voit ce que d'autres ne voient pas
    GUERISSEUR = "guerisseur"        # Prend soin des autres
    EXPLORATEUR = "explorateur"      # Découvre l'inconnu
    NARRATEUR = "narrateur"          # Donne du sens par les histoires
    HARMONISEUR = "harmoniseur"      # Crée l'équilibre et la beauté


class ClanRole(Enum):
    """Rôles dans un Clan (rotation obligatoire)"""
    APPRENTI = "apprenti"            # Apprend activement
    CONTRIBUTEUR = "contributeur"    # Apporte sa pierre
    FACILITATEUR = "facilitateur"    # Aide les autres
    MENTOR_PAIR = "mentor_pair"      # Guide un plus jeune
    INITIATEUR = "initiateur"        # Propose des projets


class ProjectPhase(Enum):
    """Phases d'un projet réel"""
    SIMULATION = "simulation"        # Environnement simulé (sécurisé)
    OBSERVATION = "observation"      # Observer le réel
    ASSISTANCE = "assistance"        # Assister un adulte
    CONTRIBUTION = "contribution"    # Contribuer sous supervision
    AUTONOMIE = "autonomie"          # Autonomie supervisée


class AccomplishmentType(Enum):
    """Types d'accomplissements (pas des notes!)"""
    DECOUVERTE = "decouverte"        # A découvert quelque chose
    CREATION = "creation"            # A créé quelque chose
    COLLABORATION = "collaboration"  # A collaboré efficacement
    PERSEVERANCE = "perseverance"    # A surmonté un obstacle
    MENTORAT = "mentorat"            # A aidé un autre
    INITIATIVE = "initiative"        # A pris une initiative
    MAITRISE = "maitrise"            # A maîtrisé une compétence


class ATOMModule(Enum):
    """Modules AT·OM où les jeunes peuvent contribuer"""
    TRANSPORT = "transport"          # AT·OM Flow
    ENERGIE = "energie"              # Énergie Symbiotique
    BIODIVERSITE = "biodiversite"    # Sentinelles Biodiversité
    REGENERATION = "regeneration"    # Régénération Active
    CIRCULAIRE = "circulaire"        # Économie Circulaire
    COMMUNAUTE = "communaute"        # Community Pulse
    CONSTRUCTION = "construction"    # Bau·M Construction


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class YoungLearner:
    """
    Profil d'un jeune apprenant

    ATTENTION: Données MINIMALES par design
    Pas de tracking comportemental détaillé
    """
    id: UUID
    anon_id: str                     # ID anonymisé (jamais l'ID réel exposé)

    # Âge approximatif (pas la date de naissance exacte)
    age_range: str                   # "6-8", "9-11", "12-14", "15-17"

    # Passions (catégories, pas détails)
    passion_domains: List[PassionDomain]
    passion_profile_hash: str        # Hash anonymisé des passions

    # Rythme naturel
    learning_rhythm: LearningRhythm

    # Génie détecté (toujours positif!)
    genius_type: Optional[GeniusType] = None
    genius_observed_in: List[str] = field(default_factory=list)

    # Clans actuels
    current_clan_ids: List[UUID] = field(default_factory=list)

    # Consentement parental
    parental_consent: bool = False
    consent_date: Optional[datetime] = None
    real_project_authorized: bool = False

    # Timestamps
    joined_at: datetime = field(default_factory=datetime.now)


@dataclass
class Clan:
    """
    Un Clan = Un groupe par PASSION, pas par âge

    "Un enfant de 8 ans passionné par l'énergie peut travailler
    avec un adolescent de 15 ans sur un module AT·OM."
    """
    id: UUID
    name: str

    # Focus
    passion_domain: PassionDomain
    atom_module: Optional[ATOMModule] = None  # Module AT·OM associé

    # Description inspirante (pas un syllabus!)
    quest: str                       # La quête du clan
    current_challenge: str           # Le défi actuel

    # Membres (anonymisés)
    member_anon_ids: List[str] = field(default_factory=list)
    age_ranges_represented: Set[str] = field(default_factory=set)

    # Capacité
    min_members: int = 3
    max_members: int = 12

    # Projet actuel
    current_project_id: Optional[UUID] = None

    # Mentors adultes associés
    adult_mentor_ids: List[UUID] = field(default_factory=list)

    # Statut
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RealWorldProject:
    """
    Projet d'apprentissage par le réel

    Progression: Simulation → Observation → Assistance → Contribution → Autonomie
    """
    id: UUID
    title: str
    description: str

    # Lien AT·OM
    atom_module: ATOMModule
    real_system_component: str       # Composant réel du système

    # Clan
    clan_id: UUID

    # Phases
    current_phase: ProjectPhase
    phases_completed: List[ProjectPhase] = field(default_factory=list)

    # Objectifs d'apprentissage (pas des notes!)
    learning_discoveries: List[str] = field(default_factory=list)
    skills_developing: List[str] = field(default_factory=list)

    # Supervision
    supervisor_id: UUID = field(default_factory=uuid4)
    requires_parental_approval: bool = True
    parental_approvals_received: int = 0

    # GOVERNANCE
    approved_for_real: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    # Timestamps
    started_at: datetime = field(default_factory=datetime.now)
    target_completion: Optional[datetime] = None


@dataclass
class Accomplishment:
    """
    Accomplissement (PAS une note!)

    Célèbre ce que l'enfant A FAIT, pas où il se "situe"
    """
    id: UUID
    learner_anon_id: str
    clan_id: Optional[UUID] = None
    project_id: Optional[UUID] = None

    # Type
    accomplishment_type: AccomplishmentType

    # Description (toujours positive!)
    title: str
    story: str                       # L'histoire de l'accomplissement

    # Impact
    skills_demonstrated: List[str] = field(default_factory=list)
    genius_expressed: Optional[GeniusType] = None

    # Validation
    witnessed_by: str = "clan"       # clan, mentor, peer, self

    # Timestamp
    achieved_at: datetime = field(default_factory=datetime.now)


@dataclass
class MentorProfile:
    """
    Profil d'un Agent Mentor (IA ou humain)

    L'Agent Mentor ne juge JAMAIS, il RÉVÈLE le génie
    """
    id: UUID
    mentor_type: str                 # "ai_agent" ou "human"

    # Spécialités
    passion_domains: List[PassionDomain]
    genius_types_recognized: List[GeniusType]

    # Approche
    mentoring_style: str             # "socratique", "demonstratif", "collaboratif"

    # Pour les mentors IA: paramètres
    ai_parameters: Dict[str, Any] = field(default_factory=dict)

    # Éthique
    never_compares_children: bool = True  # TOUJOURS True
    focuses_on_strengths: bool = True     # TOUJOURS True

    active: bool = True


@dataclass
class GeniusObservation:
    """
    Observation du génie d'un enfant

    On ne cherche pas les LACUNES, on cherche le GÉNIE
    """
    id: UUID
    learner_anon_id: str
    observer_type: str               # "ai_mentor", "human_mentor", "peer", "self"

    # Observation (toujours positive!)
    context: str                     # Situation où le génie s'est manifesté
    genius_type: GeniusType
    description: str                 # Ce qui a été observé

    # Patterns
    recurring_pattern: bool = False  # Observé plusieurs fois?

    # Timestamp
    observed_at: datetime = field(default_factory=datetime.now)


@dataclass
class JeunesseMetrics:
    """Métriques du module Jeunesse"""
    timestamp: datetime

    # Participation
    active_learners: int
    active_clans: int
    projects_in_progress: int

    # Diversité des âges dans les clans
    avg_age_range_diversity: float   # Plus c'est haut, plus les âges sont mélangés

    # Accomplissements
    accomplishments_this_week: int
    genius_observations_this_week: int

    # Projets réels
    projects_in_simulation: int
    projects_in_real: int

    # Index
    sovereignty_index: float         # 0-1: développement de la souveraineté
    collaboration_index: float       # 0-1: qualité de collaboration inter-âges
    genius_discovery_index: float    # 0-1: taux de découverte de génie


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Phases de projet nécessitant approbation parentale
PARENTAL_APPROVAL_PHASES = {ProjectPhase.ASSISTANCE, ProjectPhase.CONTRIBUTION, ProjectPhase.AUTONOMIE}

# Âge minimum pour certaines phases
MIN_AGE_FOR_REAL_PROJECT = "9-11"


# ============================================================================
# GÉNIE DE DEMAIN AGENT
# ============================================================================

class GenieDemainAgent:
    """
    Agent Génie de Demain

    ═══════════════════════════════════════════════════════════════════════════
    "Si on formate les enfants, on ne peut pas avoir d'adultes souverains."
    ═══════════════════════════════════════════════════════════════════════════

    Notre mission:
    - Allumer le feu, pas remplir le vase
    - Révéler le génie, pas mesurer les lacunes
    - Créer des souverains, pas des suiveurs

    Les 3 piliers:
    1. LE CLAN - Apprentissage par passion, pas par âge
    2. L'AGENT MENTOR - Révélateur de génie, pas évaluateur
    3. LE RÉEL - Le monde est la salle de classe
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Storage
        self._learners: Dict[str, YoungLearner] = {}  # anon_id -> learner
        self._clans: Dict[UUID, Clan] = {}
        self._projects: Dict[UUID, RealWorldProject] = {}
        self._accomplishments: Dict[UUID, Accomplishment] = {}
        self._mentors: Dict[UUID, MentorProfile] = {}
        self._genius_observations: Dict[UUID, GeniusObservation] = {}

        # Metrics history
        self._metrics_history: List[JeunesseMetrics] = []

        self._initialized = True
        logger.info("GenieDemainAgent initialized - Allumeurs de feu, révélateurs de génie")

        # Initialiser les mentors IA par défaut
        self._init_ai_mentors()

    def _init_ai_mentors(self) -> None:
        """Initialiser les agents mentors IA de la Division Mentorat"""
        mentor_specs = [
            ("Mentor Créateur", [PassionDomain.CREATION_TECH, PassionDomain.CONSTRUCTION_CRAFT],
             [GeniusType.INVENTEUR, GeniusType.ARTISAN], "demonstratif"),
            ("Mentor Explorateur", [PassionDomain.EXPLORATION_NATURE, PassionDomain.DECOUVERTE_SCIENCE],
             [GeniusType.EXPLORATEUR, GeniusType.VISIONNAIRE], "socratique"),
            ("Mentor Expressif", [PassionDomain.EXPRESSION_ART, PassionDomain.NARRATION_STORY],
             [GeniusType.NARRATEUR, GeniusType.HARMONISEUR], "collaboratif"),
            ("Mentor Connecteur", [PassionDomain.CONNECTION_SOCIAL, PassionDomain.MOUVEMENT_CORPS],
             [GeniusType.CONNECTEUR, GeniusType.GUERISSEUR], "collaboratif"),
        ]

        for name, domains, genius_types, style in mentor_specs:
            mentor = MentorProfile(
                id=uuid4(),
                mentor_type="ai_agent",
                passion_domains=domains,
                genius_types_recognized=genius_types,
                mentoring_style=style,
                ai_parameters={"model": "mentor_v68", "focus": "genius_revelation"},
            )
            self._mentors[mentor.id] = mentor

    # ========================================================================
    # INSCRIPTION DES JEUNES APPRENANTS
    # ========================================================================

    def register_young_learner(
        self,
        learner_id: UUID,
        age_range: str,
        passions: List[str],
        learning_rhythm: LearningRhythm,
        parental_consent: bool,
    ) -> YoungLearner:
        """
        Inscrire un jeune apprenant

        PRIVACY: Données minimales, consentement parental obligatoire
        """
        if age_range not in ["6-8", "9-11", "12-14", "15-17"]:
            raise ValueError("Invalid age range")

        if not parental_consent:
            raise ValueError("Parental consent required for registration")

        # Créer un ID anonyme (jamais exposer l'ID réel)
        clan_placeholder = uuid4()  # Temporaire pour l'anonymisation
        anon_id = anonymize_young_learner(learner_id, clan_placeholder)

        # Convertir les passions en domaines
        passion_domains = self._passions_to_domains(passions)
        passion_hash = anonymize_passion_profile(passions)

        learner = YoungLearner(
            id=learner_id,
            anon_id=anon_id,
            age_range=age_range,
            passion_domains=passion_domains,
            passion_profile_hash=passion_hash,
            learning_rhythm=learning_rhythm,
            parental_consent=True,
            consent_date=datetime.now(),
        )

        self._learners[anon_id] = learner

        logger.info(f"Young learner registered (anon): {anon_id[:8]}... age: {age_range}")

        # Suggérer un clan basé sur les passions
        self._suggest_clan_for_learner(learner)

        return learner

    def _passions_to_domains(self, passions: List[str]) -> List[PassionDomain]:
        """Convertir les passions libres en domaines"""
        domain_keywords = {
            PassionDomain.CREATION_TECH: ["code", "robot", "ia", "ordinateur", "jeux", "electronique", "tech"],
            PassionDomain.EXPLORATION_NATURE: ["animaux", "plantes", "ocean", "foret", "nature", "ecologie"],
            PassionDomain.EXPRESSION_ART: ["dessin", "musique", "danse", "theatre", "art", "peinture"],
            PassionDomain.DECOUVERTE_SCIENCE: ["espace", "chimie", "physique", "experience", "science", "maths"],
            PassionDomain.CONNECTION_SOCIAL: ["aide", "amis", "equipe", "communaute", "social"],
            PassionDomain.CONSTRUCTION_CRAFT: ["construction", "bricolage", "menuiserie", "mecanique", "cuisine"],
            PassionDomain.MOUVEMENT_CORPS: ["sport", "yoga", "danse", "natation", "course", "escalade"],
            PassionDomain.NARRATION_STORY: ["histoire", "livre", "ecriture", "conte", "film", "video"],
        }

        domains = set()
        for passion in passions:
            passion_lower = passion.lower()
            for domain, keywords in domain_keywords.items():
                if any(kw in passion_lower for kw in keywords):
                    domains.add(domain)

        return list(domains) if domains else [PassionDomain.EXPLORATION_NATURE]  # Default

    # ========================================================================
    # GESTION DES CLANS
    # ========================================================================

    def create_clan(
        self,
        name: str,
        passion_domain: PassionDomain,
        quest: str,
        current_challenge: str,
        atom_module: Optional[ATOMModule] = None,
        adult_mentor_id: Optional[UUID] = None,
    ) -> Clan:
        """
        Créer un nouveau Clan

        Un Clan n'est pas une classe - c'est une équipe de quêteurs
        """
        clan = Clan(
            id=uuid4(),
            name=name,
            passion_domain=passion_domain,
            atom_module=atom_module,
            quest=quest,
            current_challenge=current_challenge,
        )

        if adult_mentor_id:
            clan.adult_mentor_ids.append(adult_mentor_id)

        self._clans[clan.id] = clan

        logger.info(f"Clan created: '{name}' - Quest: {quest[:50]}...")

        return clan

    def join_clan(
        self,
        learner_anon_id: str,
        clan_id: UUID,
    ) -> Clan:
        """
        Rejoindre un Clan

        Un jeune peut être dans plusieurs clans (multi-passions)
        """
        if learner_anon_id not in self._learners:
            raise ValueError("Learner not found")
        if clan_id not in self._clans:
            raise ValueError("Clan not found")

        learner = self._learners[learner_anon_id]
        clan = self._clans[clan_id]

        if len(clan.member_anon_ids) >= clan.max_members:
            raise ValueError("Clan is full")

        if learner_anon_id not in clan.member_anon_ids:
            clan.member_anon_ids.append(learner_anon_id)
            clan.age_ranges_represented.add(learner.age_range)
            learner.current_clan_ids.append(clan_id)

        logger.info(f"Learner joined clan '{clan.name}' (diversity: {len(clan.age_ranges_represented)} age groups)")

        return clan

    def _suggest_clan_for_learner(self, learner: YoungLearner) -> Optional[Clan]:
        """Suggérer un clan basé sur les passions"""
        for clan in self._clans.values():
            if clan.passion_domain in learner.passion_domains:
                if len(clan.member_anon_ids) < clan.max_members:
                    return clan
        return None

    # ========================================================================
    # PROJETS D'APPRENTISSAGE PAR LE RÉEL
    # ========================================================================

    def create_real_world_project(
        self,
        title: str,
        description: str,
        atom_module: ATOMModule,
        real_system_component: str,
        clan_id: UUID,
        supervisor_id: UUID,
        learning_discoveries: List[str],
        skills_developing: List[str],
    ) -> RealWorldProject:
        """
        Créer un projet d'apprentissage par le réel

        Tout projet commence en SIMULATION
        """
        if clan_id not in self._clans:
            raise ValueError("Clan not found")

        project = RealWorldProject(
            id=uuid4(),
            title=title,
            description=description,
            atom_module=atom_module,
            real_system_component=real_system_component,
            clan_id=clan_id,
            current_phase=ProjectPhase.SIMULATION,  # Toujours commencer ici
            supervisor_id=supervisor_id,
            learning_discoveries=learning_discoveries,
            skills_developing=skills_developing,
        )

        self._projects[project.id] = project

        # Lier au clan
        clan = self._clans[clan_id]
        clan.current_project_id = project.id

        logger.info(f"Real-world project created: '{title}' (module: {atom_module.value})")

        return project

    def advance_project_phase(
        self,
        project_id: UUID,
    ) -> RealWorldProject:
        """
        Avancer à la phase suivante du projet

        GOVERNANCE: Certaines phases nécessitent approbation parentale
        """
        if project_id not in self._projects:
            raise ValueError("Project not found")

        project = self._projects[project_id]

        # Ordre des phases
        phase_order = [
            ProjectPhase.SIMULATION,
            ProjectPhase.OBSERVATION,
            ProjectPhase.ASSISTANCE,
            ProjectPhase.CONTRIBUTION,
            ProjectPhase.AUTONOMIE,
        ]

        current_idx = phase_order.index(project.current_phase)
        if current_idx >= len(phase_order) - 1:
            raise ValueError("Project already at final phase")

        next_phase = phase_order[current_idx + 1]

        # Vérifier si approbation nécessaire
        if next_phase in PARENTAL_APPROVAL_PHASES:
            if not project.approved_for_real:
                raise ValueError(
                    f"Phase {next_phase.value} requires parental approval. "
                    f"Use approve_real_project_phase() first."
                )

        project.phases_completed.append(project.current_phase)
        project.current_phase = next_phase

        logger.info(f"Project '{project.title}' advanced to phase: {next_phase.value}")

        return project

    def approve_real_project_phase(
        self,
        project_id: UUID,
        approver_name: str,
        parental_approvals: int,
        approval_notes: str = "",
    ) -> RealWorldProject:
        """
        GOVERNANCE GATE: Approuver la participation à un projet réel

        RULE #1: Participation réelle REQUIERT approbation parentale
        """
        if project_id not in self._projects:
            raise ValueError("Project not found")

        project = self._projects[project_id]
        clan = self._clans.get(project.clan_id)

        if not clan:
            raise ValueError("Clan not found")

        # Vérifier que suffisamment de parents ont approuvé
        members_count = len(clan.member_anon_ids)
        required_approvals = max(1, int(members_count * 0.8))  # 80% des parents

        if parental_approvals < required_approvals:
            raise ValueError(
                f"Insufficient parental approvals. "
                f"Got {parental_approvals}, need {required_approvals}"
            )

        project.approved_for_real = True
        project.approved_by = approver_name
        project.approved_at = datetime.now()
        project.parental_approvals_received = parental_approvals

        logger.info(
            f"GOVERNANCE: Real project '{project.title}' approved by {approver_name} "
            f"({parental_approvals} parental approvals)"
        )

        return project

    # ========================================================================
    # RÉVÉLATION DU GÉNIE
    # ========================================================================

    def observe_genius(
        self,
        learner_anon_id: str,
        observer_type: str,
        context: str,
        genius_type: GeniusType,
        description: str,
    ) -> GeniusObservation:
        """
        Observer et enregistrer une manifestation du génie

        On ne cherche pas les LACUNES, on cherche le GÉNIE
        Chaque enfant a un génie unique - notre travail est de le révéler
        """
        if learner_anon_id not in self._learners:
            raise ValueError("Learner not found")

        observation = GeniusObservation(
            id=uuid4(),
            learner_anon_id=learner_anon_id,
            observer_type=observer_type,
            context=context,
            genius_type=genius_type,
            description=description,
        )

        self._genius_observations[observation.id] = observation

        # Mettre à jour le profil de l'apprenant
        learner = self._learners[learner_anon_id]
        if learner.genius_type is None:
            learner.genius_type = genius_type
        learner.genius_observed_in.append(context)

        # Vérifier si c'est un pattern récurrent
        similar_observations = [
            obs for obs in self._genius_observations.values()
            if obs.learner_anon_id == learner_anon_id
            and obs.genius_type == genius_type
        ]
        if len(similar_observations) >= 3:
            observation.recurring_pattern = True

        logger.info(
            f"Genius observed: {genius_type.value} in context '{context[:30]}...' "
            f"(recurring: {observation.recurring_pattern})"
        )

        return observation

    def get_learner_genius_profile(
        self,
        learner_anon_id: str,
    ) -> Dict[str, Any]:
        """
        Obtenir le profil de génie d'un apprenant

        JAMAIS de comparaison, JAMAIS de classement
        Seulement la célébration du génie unique
        """
        if learner_anon_id not in self._learners:
            raise ValueError("Learner not found")

        learner = self._learners[learner_anon_id]

        # Collecter les observations
        observations = [
            obs for obs in self._genius_observations.values()
            if obs.learner_anon_id == learner_anon_id
        ]

        # Compter les types de génie observés
        genius_counts: Dict[GeniusType, int] = {}
        for obs in observations:
            genius_counts[obs.genius_type] = genius_counts.get(obs.genius_type, 0) + 1

        # Trouver le génie dominant
        dominant_genius = None
        if genius_counts:
            dominant_genius = max(genius_counts.items(), key=lambda x: x[1])[0]

        return {
            "anon_id": learner_anon_id[:8] + "...",
            "passion_domains": [d.value for d in learner.passion_domains],
            "learning_rhythm": learner.learning_rhythm.value,
            "genius_type": dominant_genius.value if dominant_genius else "en découverte",
            "genius_observations_count": len(observations),
            "genius_manifestations": [
                {
                    "type": obs.genius_type.value,
                    "context": obs.context,
                    "recurring": obs.recurring_pattern,
                }
                for obs in observations[-5:]  # 5 dernières observations
            ],
            "message": self._generate_genius_message(dominant_genius),
            # JAMAIS de comparaison, JAMAIS de classement
        }

    def _generate_genius_message(self, genius_type: Optional[GeniusType]) -> str:
        """Générer un message positif sur le génie"""
        messages = {
            GeniusType.INVENTEUR: "Un créateur de solutions nouvelles - le monde a besoin de tes inventions!",
            GeniusType.CONNECTEUR: "Un tisseur de liens - tu rapproches les idées et les gens!",
            GeniusType.ARTISAN: "Un maître de la précision - ta technique inspire!",
            GeniusType.VISIONNAIRE: "Un voyant du possible - tu vois ce que d'autres ne voient pas encore!",
            GeniusType.GUERISSEUR: "Un gardien du bien-être - ta présence apaise et répare!",
            GeniusType.EXPLORATEUR: "Un découvreur d'horizons - l'inconnu t'appelle!",
            GeniusType.NARRATEUR: "Un donneur de sens - tes histoires éclairent le monde!",
            GeniusType.HARMONISEUR: "Un créateur d'équilibre - tu apportes la beauté!",
        }

        if genius_type:
            return messages.get(genius_type, "Un génie en révélation - continue d'explorer!")
        return "Ton génie unique se révèle peu à peu - chaque expérience t'en rapproche!"

    # ========================================================================
    # ACCOMPLISSEMENTS
    # ========================================================================

    def record_accomplishment(
        self,
        learner_anon_id: str,
        accomplishment_type: AccomplishmentType,
        title: str,
        story: str,
        skills_demonstrated: List[str],
        clan_id: Optional[UUID] = None,
        project_id: Optional[UUID] = None,
        genius_expressed: Optional[GeniusType] = None,
        witnessed_by: str = "clan",
    ) -> Accomplishment:
        """
        Enregistrer un accomplissement

        PAS une note! Une célébration de ce que l'enfant A FAIT
        """
        if learner_anon_id not in self._learners:
            raise ValueError("Learner not found")

        accomplishment = Accomplishment(
            id=uuid4(),
            learner_anon_id=learner_anon_id,
            clan_id=clan_id,
            project_id=project_id,
            accomplishment_type=accomplishment_type,
            title=title,
            story=story,
            skills_demonstrated=skills_demonstrated,
            genius_expressed=genius_expressed,
            witnessed_by=witnessed_by,
        )

        self._accomplishments[accomplishment.id] = accomplishment

        logger.info(f"Accomplishment recorded: '{title}' ({accomplishment_type.value})")

        return accomplishment

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_clans(
        self,
        passion_domain: Optional[PassionDomain] = None,
        atom_module: Optional[ATOMModule] = None,
    ) -> List[Clan]:
        """
        Obtenir les clans

        GOVERNANCE RULE #5: ALPHABETICAL par nom
        """
        clans = list(self._clans.values())

        if passion_domain:
            clans = [c for c in clans if c.passion_domain == passion_domain]
        if atom_module:
            clans = [c for c in clans if c.atom_module == atom_module]

        # ALPHABETICAL
        clans.sort(key=lambda c: c.name.lower())

        return clans

    def get_accomplishments(
        self,
        learner_anon_id: Optional[str] = None,
        clan_id: Optional[UUID] = None,
    ) -> List[Accomplishment]:
        """
        Obtenir les accomplissements

        GOVERNANCE RULE #5: CHRONOLOGICAL
        """
        accomplishments = list(self._accomplishments.values())

        if learner_anon_id:
            accomplishments = [a for a in accomplishments if a.learner_anon_id == learner_anon_id]
        if clan_id:
            accomplishments = [a for a in accomplishments if a.clan_id == clan_id]

        # CHRONOLOGICAL
        accomplishments.sort(key=lambda a: a.achieved_at)

        return accomplishments

    def get_projects(
        self,
        atom_module: Optional[ATOMModule] = None,
        phase: Optional[ProjectPhase] = None,
    ) -> List[RealWorldProject]:
        """
        Obtenir les projets

        GOVERNANCE RULE #5: CHRONOLOGICAL
        """
        projects = list(self._projects.values())

        if atom_module:
            projects = [p for p in projects if p.atom_module == atom_module]
        if phase:
            projects = [p for p in projects if p.current_phase == phase]

        # CHRONOLOGICAL
        projects.sort(key=lambda p: p.started_at)

        return projects

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_jeunesse_metrics(self) -> JeunesseMetrics:
        """Obtenir les métriques du module Jeunesse"""
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        learners = list(self._learners.values())
        clans = list(self._clans.values())
        projects = list(self._projects.values())

        # Participation
        active_learners = len([l for l in learners if l.current_clan_ids])
        active_clans = len([c for c in clans if c.active and c.member_anon_ids])
        projects_in_progress = len([
            p for p in projects
            if p.current_phase not in {ProjectPhase.SIMULATION}
        ])

        # Diversité des âges
        age_diversities = []
        for clan in clans:
            if clan.member_anon_ids:
                age_diversities.append(len(clan.age_ranges_represented))
        avg_diversity = sum(age_diversities) / max(len(age_diversities), 1)

        # Accomplissements récents
        accomplishments = list(self._accomplishments.values())
        recent_accomplishments = [a for a in accomplishments if a.achieved_at >= week_ago]

        # Observations de génie récentes
        observations = list(self._genius_observations.values())
        recent_observations = [o for o in observations if o.observed_at >= week_ago]

        # Projets par phase
        simulation_projects = len([p for p in projects if p.current_phase == ProjectPhase.SIMULATION])
        real_projects = len([p for p in projects if p.current_phase in PARENTAL_APPROVAL_PHASES])

        # Indices

        # Sovereignty Index: basé sur l'autonomie et la diversité
        if active_learners > 0:
            learners_with_genius = len([l for l in learners if l.genius_type])
            sovereignty = learners_with_genius / active_learners
        else:
            sovereignty = 0

        # Collaboration Index: basé sur la diversité inter-âges
        collaboration = min(avg_diversity / 4, 1.0)  # Max 4 tranches d'âge

        # Genius Discovery Index
        if active_learners > 0:
            genius_rate = len(recent_observations) / active_learners
            genius_discovery = min(genius_rate, 1.0)
        else:
            genius_discovery = 0

        metrics = JeunesseMetrics(
            timestamp=now,
            active_learners=active_learners,
            active_clans=active_clans,
            projects_in_progress=projects_in_progress,
            avg_age_range_diversity=avg_diversity,
            accomplishments_this_week=len(recent_accomplishments),
            genius_observations_this_week=len(recent_observations),
            projects_in_simulation=simulation_projects,
            projects_in_real=real_projects,
            sovereignty_index=sovereignty,
            collaboration_index=collaboration,
            genius_discovery_index=genius_discovery,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_jeunesse_indices(self) -> Dict[str, float]:
        """Obtenir les indices pour le dashboard"""
        metrics = self.get_jeunesse_metrics()

        return {
            "sovereignty_index": round(metrics.sovereignty_index, 3),
            "collaboration_index": round(metrics.collaboration_index, 3),
            "genius_discovery_index": round(metrics.genius_discovery_index, 3),
            "age_diversity": round(metrics.avg_age_range_diversity / 4, 3),
            "real_project_engagement": round(
                metrics.projects_in_real / max(metrics.projects_in_progress, 1), 3
            ),
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_genie_demain_agent() -> GenieDemainAgent:
    """Get the singleton GenieDemainAgent instance"""
    return GenieDemainAgent()
