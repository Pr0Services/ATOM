"""
CHE·NU V68 Consensus Liquide Agent
Module Societaire 4/4 - La fin de la politique de confrontation

CONCEPT: Gouvernance par Consensus Liquide
- Les citoyens votent sur des micro-decisions locales
- Les agents synthetisent les besoins pour trouver le JUSTE MILIEU (Balance)
- Auto-gouvernance sans leaders autoritaires
- La ville se gouverne par le code, pas par la force

PRINCIPES:
1. Toute voix compte egalement (pas de poids politique)
2. Les decisions sont locales d'abord, globales ensuite
3. Le consensus n'est pas l'unanimite - c'est le juste milieu
4. Transparence totale des decisions (audit trail)

PRIVACY FIRST:
- Votes anonymises (hash one-way)
- Pas de tracking des opinions politiques
- Synthese par zone, pas par individu

GOVERNANCE COMPLIANCE:
- Rule #1: Decisions haute valeur require APPROVAL HUMAIN
- Rule #5: Propositions CHRONOLOGICAL (pas de ranking)
- Rule #6: Full audit trail (anonymized voters)
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Tuple
from uuid import UUID, uuid4
import logging
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# PRIVACY HELPERS
# ============================================================================

def anonymize_voter_id(voter_id: UUID, proposal_id: UUID) -> str:
    """
    Anonymize voter ID per proposal - prevents vote tracking across proposals
    Each proposal gets different anonymized IDs for same voter
    """
    salt = "CHENU_GOVERNANCE_CONSENSUS_999Hz"
    combined = f"{salt}{str(voter_id)}{str(proposal_id)}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def anonymize_zone(latitude: float, longitude: float) -> str:
    """Anonymize location to zone level (~5km precision)"""
    lat_zone = round(latitude, 1)
    lon_zone = round(longitude, 1)
    return f"zone_{lat_zone}_{lon_zone}"


# ============================================================================
# ENUMS
# ============================================================================

class ProposalCategory(Enum):
    """Categories de propositions"""
    INFRASTRUCTURE = "infrastructure"      # Routes, batiments publics
    ENVIRONMENT = "environment"            # Espaces verts, eau
    TRANSPORT = "transport"                # Mobilite, circulation
    EDUCATION = "education"                # Ecoles, formations
    HEALTH = "health"                      # Sante publique
    COMMERCE = "commerce"                  # Marches, activites
    CULTURE = "culture"                    # Evenements, arts
    SECURITY = "security"                  # Securite publique
    SOCIAL = "social"                      # Aide sociale, solidarite
    BUDGET = "budget"                      # Allocation de ressources


class ProposalScope(Enum):
    """Portee de la proposition"""
    MICRO = "micro"            # Quartier (< 1km)
    LOCAL = "local"            # Zone (~5km)
    DISTRICT = "district"      # District (~20km)
    CITY = "city"              # Ville entiere
    REGIONAL = "regional"      # Region


class ProposalStatus(Enum):
    """Statut de la proposition"""
    DRAFT = "draft"                        # Brouillon
    OPEN = "open"                          # Ouverte aux votes
    DELIBERATION = "deliberation"          # En deliberation
    PENDING_APPROVAL = "pending_approval"  # GOVERNANCE: Attend approbation
    APPROVED = "approved"                  # Approuvee
    REJECTED = "rejected"                  # Rejetee
    IMPLEMENTED = "implemented"            # Implementee
    ARCHIVED = "archived"                  # Archivee


class VoteType(Enum):
    """Type de vote"""
    FOR = "for"                            # Pour
    AGAINST = "against"                    # Contre
    NEUTRAL = "neutral"                    # Neutre/Abstention
    PROPOSAL = "proposal"                  # Contre-proposition


class ConsensusLevel(Enum):
    """Niveau de consensus atteint"""
    NONE = "none"                # Pas de consensus
    WEAK = "weak"                # Faible (<50%)
    MODERATE = "moderate"        # Modere (50-65%)
    STRONG = "strong"            # Fort (65-80%)
    NEAR_UNANIMOUS = "near_unanimous"  # Quasi-unanime (>80%)


class ImpactLevel(Enum):
    """Niveau d'impact de la decision"""
    MINIMAL = "minimal"          # Impact minimal
    LOW = "low"                  # Faible impact
    MEDIUM = "medium"            # Impact moyen
    HIGH = "high"                # Impact eleve - REQUIRES APPROVAL
    CRITICAL = "critical"        # Impact critique - REQUIRES APPROVAL


class ParticipantRole(Enum):
    """Role du participant"""
    CITIZEN = "citizen"          # Citoyen standard
    DELEGATE = "delegate"        # Delegue de zone
    EXPERT = "expert"            # Expert consultatif (no extra vote weight)
    FACILITATOR = "facilitator"  # Facilitateur de debat


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class GeoZone:
    """Zone geographique (precision reduite pour privacy)"""
    zone_id: str
    latitude: float
    longitude: float
    radius_km: float
    name: Optional[str] = None

    def __post_init__(self):
        # PRIVACY: Reduce precision
        self.latitude = round(self.latitude, 1)
        self.longitude = round(self.longitude, 1)


@dataclass
class Proposal:
    """Proposition citoyenne"""
    id: UUID
    title: str
    description: str
    category: ProposalCategory
    scope: ProposalScope
    zone: GeoZone

    # Timing
    created_at: datetime
    voting_opens: datetime
    voting_closes: datetime

    # Status
    status: ProposalStatus = ProposalStatus.DRAFT

    # Impact assessment
    impact_level: ImpactLevel = ImpactLevel.MEDIUM
    budget_required: Decimal = Decimal("0")
    affected_population: int = 0

    # PRIVACY: Creator anonymized
    creator_anon_id: str = ""

    # Options (for multi-choice proposals)
    options: List[str] = field(default_factory=list)

    # Audit
    audit_log: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Vote:
    """Vote sur une proposition (anonymise)"""
    id: UUID
    proposal_id: UUID
    voter_anon_id: str           # PRIVACY: Anonymized
    zone_id: str                  # PRIVACY: Zone-level only

    vote_type: VoteType
    option_index: Optional[int] = None  # For multi-choice
    comment: Optional[str] = None       # Optional reasoning

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CounterProposal:
    """Contre-proposition (alternative)"""
    id: UUID
    parent_proposal_id: UUID
    title: str
    description: str

    creator_anon_id: str         # PRIVACY: Anonymized
    created_at: datetime

    # Merging logic
    merged_elements: List[str] = field(default_factory=list)
    compromise_points: List[str] = field(default_factory=list)


@dataclass
class ConsensusResult:
    """Resultat du consensus"""
    proposal_id: UUID

    # Counts
    total_votes: int
    votes_for: int
    votes_against: int
    votes_neutral: int
    counter_proposals: int

    # Participation
    participation_rate: float    # % de la zone qui a vote
    zone_coverage: float         # % des zones representees

    # Consensus
    consensus_level: ConsensusLevel
    consensus_percentage: float

    # Decision
    decision: str                # FOR, AGAINST, AMENDED, NO_DECISION
    amendments: List[str] = field(default_factory=list)

    # GOVERNANCE
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None


@dataclass
class DeliberationSession:
    """Session de deliberation"""
    id: UUID
    proposal_id: UUID

    scheduled_at: datetime
    duration_minutes: int

    facilitator_anon_id: str
    participants_count: int

    # Results
    key_points: List[str] = field(default_factory=list)
    concerns_raised: List[str] = field(default_factory=list)
    suggested_amendments: List[str] = field(default_factory=list)

    status: str = "scheduled"  # scheduled, in_progress, completed


@dataclass
class GovernanceMetrics:
    """Metriques de gouvernance"""
    timestamp: datetime

    # Participation
    active_proposals: int
    total_votes_today: int
    unique_voters_today: int
    participation_rate: float

    # Consensus health
    avg_consensus_level: float
    decisions_reached: int
    decisions_blocked: int

    # Indices sociaux
    democratic_vitality_index: float   # 0-1, vitality of participation
    deliberation_quality_index: float  # 0-1, quality of debates
    implementation_rate: float         # % of approved proposals implemented


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Impact levels that require human approval
HIGH_IMPACT_LEVELS = {ImpactLevel.HIGH, ImpactLevel.CRITICAL}

# Budget threshold requiring approval (in local currency units)
BUDGET_APPROVAL_THRESHOLD = Decimal("10000")

# Minimum participation for valid decision
MIN_PARTICIPATION_RATE = 0.15  # 15%

# Consensus thresholds
CONSENSUS_THRESHOLDS = {
    ConsensusLevel.NONE: 0.0,
    ConsensusLevel.WEAK: 0.50,
    ConsensusLevel.MODERATE: 0.65,
    ConsensusLevel.STRONG: 0.80,
    ConsensusLevel.NEAR_UNANIMOUS: 0.90,
}


# ============================================================================
# CONSENSUS LIQUIDE AGENT
# ============================================================================

class ConsensusLiquideAgent:
    """
    Agent de Gouvernance par Consensus Liquide

    La fin de la politique de confrontation:
    - Chaque voix compte egalement
    - Les decisions emergent du collectif
    - Le juste milieu (Balance) est recherche
    - Transparence totale, votes anonymes
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
        self._proposals: Dict[UUID, Proposal] = {}
        self._votes: Dict[UUID, List[Vote]] = {}  # proposal_id -> votes
        self._counter_proposals: Dict[UUID, List[CounterProposal]] = {}
        self._results: Dict[UUID, ConsensusResult] = {}
        self._deliberations: Dict[UUID, List[DeliberationSession]] = {}

        # Zone participation tracking (anonymized)
        self._zone_participation: Dict[str, Set[str]] = {}  # zone -> anon_voter_ids

        # Metrics history
        self._metrics_history: List[GovernanceMetrics] = []

        self._initialized = True
        logger.info("ConsensusLiquideAgent initialized - Gouvernance par le peuple, pour le peuple")

    # ========================================================================
    # PROPOSAL MANAGEMENT
    # ========================================================================

    def create_proposal(
        self,
        title: str,
        description: str,
        category: ProposalCategory,
        scope: ProposalScope,
        zone_latitude: float,
        zone_longitude: float,
        zone_radius_km: float,
        creator_id: UUID,
        voting_duration_days: int = 7,
        impact_level: ImpactLevel = ImpactLevel.MEDIUM,
        budget_required: Decimal = Decimal("0"),
        affected_population: int = 0,
        options: Optional[List[str]] = None,
    ) -> Proposal:
        """
        Creer une nouvelle proposition citoyenne

        GOVERNANCE: High impact proposals require approval before going live
        """
        proposal_id = uuid4()

        # PRIVACY: Anonymize creator
        creator_anon = anonymize_voter_id(creator_id, proposal_id)

        # Create zone
        zone = GeoZone(
            zone_id=anonymize_zone(zone_latitude, zone_longitude),
            latitude=zone_latitude,
            longitude=zone_longitude,
            radius_km=zone_radius_km,
        )

        # Determine initial status
        initial_status = ProposalStatus.DRAFT
        if impact_level in HIGH_IMPACT_LEVELS or budget_required > BUDGET_APPROVAL_THRESHOLD:
            # High impact requires review before opening
            initial_status = ProposalStatus.PENDING_APPROVAL

        now = datetime.now()
        proposal = Proposal(
            id=proposal_id,
            title=title,
            description=description,
            category=category,
            scope=scope,
            zone=zone,
            created_at=now,
            voting_opens=now + timedelta(days=1),  # 24h review period
            voting_closes=now + timedelta(days=1 + voting_duration_days),
            status=initial_status,
            impact_level=impact_level,
            budget_required=budget_required,
            affected_population=affected_population,
            creator_anon_id=creator_anon,
            options=options or [],
            audit_log=[{
                "action": "created",
                "timestamp": now.isoformat(),
                "by_anon": creator_anon,
                "status": initial_status.value,
            }],
        )

        self._proposals[proposal_id] = proposal
        self._votes[proposal_id] = []
        self._counter_proposals[proposal_id] = []

        logger.info(
            f"Proposal created: {proposal_id} - {title} "
            f"(status: {initial_status.value}, impact: {impact_level.value})"
        )

        return proposal

    def approve_proposal_opening(
        self,
        proposal_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> Proposal:
        """
        GOVERNANCE GATE: Approve high-impact proposal to open for voting

        RULE #1: Human must approve high-impact decisions
        """
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal = self._proposals[proposal_id]

        if proposal.status != ProposalStatus.PENDING_APPROVAL:
            raise ValueError(
                f"Proposal not pending approval (status: {proposal.status.value})"
            )

        now = datetime.now()
        proposal.status = ProposalStatus.OPEN
        proposal.voting_opens = now
        proposal.voting_closes = now + timedelta(days=7)

        proposal.audit_log.append({
            "action": "approved_for_voting",
            "timestamp": now.isoformat(),
            "by": approver_name,
            "notes": approval_notes,
        })

        logger.info(
            f"GOVERNANCE: Proposal {proposal_id} approved for voting by {approver_name}"
        )

        return proposal

    def open_proposal(self, proposal_id: UUID) -> Proposal:
        """Open a draft proposal for voting (low/medium impact only)"""
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal = self._proposals[proposal_id]

        if proposal.status != ProposalStatus.DRAFT:
            raise ValueError(f"Proposal not in draft (status: {proposal.status.value})")

        if proposal.impact_level in HIGH_IMPACT_LEVELS:
            raise ValueError(
                f"High impact proposal requires approval "
                f"(impact: {proposal.impact_level.value})"
            )

        now = datetime.now()
        proposal.status = ProposalStatus.OPEN
        proposal.voting_opens = now

        proposal.audit_log.append({
            "action": "opened_for_voting",
            "timestamp": now.isoformat(),
        })

        return proposal

    # ========================================================================
    # VOTING
    # ========================================================================

    def cast_vote(
        self,
        proposal_id: UUID,
        voter_id: UUID,
        voter_latitude: float,
        voter_longitude: float,
        vote_type: VoteType,
        option_index: Optional[int] = None,
        comment: Optional[str] = None,
    ) -> Vote:
        """
        Cast a vote on a proposal

        PRIVACY: Voter ID and location are anonymized
        ONE PERSON = ONE VOTE (no weighting)
        """
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal = self._proposals[proposal_id]

        if proposal.status != ProposalStatus.OPEN:
            raise ValueError(f"Proposal not open for voting (status: {proposal.status.value})")

        now = datetime.now()
        if now < proposal.voting_opens or now > proposal.voting_closes:
            raise ValueError("Voting period not active")

        # PRIVACY: Anonymize voter
        voter_anon = anonymize_voter_id(voter_id, proposal_id)
        zone_id = anonymize_zone(voter_latitude, voter_longitude)

        # Check for duplicate vote
        existing_votes = self._votes.get(proposal_id, [])
        for v in existing_votes:
            if v.voter_anon_id == voter_anon:
                raise ValueError("Voter has already voted on this proposal")

        vote = Vote(
            id=uuid4(),
            proposal_id=proposal_id,
            voter_anon_id=voter_anon,
            zone_id=zone_id,
            vote_type=vote_type,
            option_index=option_index,
            comment=comment,
            timestamp=now,
        )

        self._votes[proposal_id].append(vote)

        # Track zone participation
        if zone_id not in self._zone_participation:
            self._zone_participation[zone_id] = set()
        self._zone_participation[zone_id].add(voter_anon)

        logger.debug(f"Vote cast on proposal {proposal_id} from zone {zone_id}")

        return vote

    def submit_counter_proposal(
        self,
        parent_proposal_id: UUID,
        title: str,
        description: str,
        creator_id: UUID,
        merged_elements: Optional[List[str]] = None,
        compromise_points: Optional[List[str]] = None,
    ) -> CounterProposal:
        """
        Submit a counter-proposal (alternative to main proposal)

        This is the "juste milieu" mechanism - finding middle ground
        """
        if parent_proposal_id not in self._proposals:
            raise ValueError(f"Parent proposal {parent_proposal_id} not found")

        parent = self._proposals[parent_proposal_id]
        if parent.status not in {ProposalStatus.OPEN, ProposalStatus.DELIBERATION}:
            raise ValueError("Parent proposal not open for alternatives")

        counter = CounterProposal(
            id=uuid4(),
            parent_proposal_id=parent_proposal_id,
            title=title,
            description=description,
            creator_anon_id=anonymize_voter_id(creator_id, parent_proposal_id),
            created_at=datetime.now(),
            merged_elements=merged_elements or [],
            compromise_points=compromise_points or [],
        )

        self._counter_proposals[parent_proposal_id].append(counter)

        logger.info(
            f"Counter-proposal submitted for {parent_proposal_id}: {title}"
        )

        return counter

    # ========================================================================
    # CONSENSUS CALCULATION
    # ========================================================================

    def calculate_consensus(self, proposal_id: UUID) -> ConsensusResult:
        """
        Calculate consensus result for a proposal

        Consensus is not unanimity - it's finding the JUSTE MILIEU
        The Balance between all voices
        """
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal = self._proposals[proposal_id]
        votes = self._votes.get(proposal_id, [])
        counters = self._counter_proposals.get(proposal_id, [])

        # Count votes
        votes_for = sum(1 for v in votes if v.vote_type == VoteType.FOR)
        votes_against = sum(1 for v in votes if v.vote_type == VoteType.AGAINST)
        votes_neutral = sum(1 for v in votes if v.vote_type == VoteType.NEUTRAL)
        total_votes = len(votes)

        # Calculate participation
        zones_represented = len(set(v.zone_id for v in votes))
        participation_rate = (
            total_votes / proposal.affected_population
            if proposal.affected_population > 0
            else 0.0
        )

        # Calculate consensus percentage
        if total_votes > 0:
            # For binary: % who agree with majority
            majority_votes = max(votes_for, votes_against)
            consensus_pct = majority_votes / total_votes
        else:
            consensus_pct = 0.0

        # Determine consensus level
        consensus_level = ConsensusLevel.NONE
        for level, threshold in sorted(
            CONSENSUS_THRESHOLDS.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            if consensus_pct >= threshold:
                consensus_level = level
                break

        # Determine decision
        if participation_rate < MIN_PARTICIPATION_RATE:
            decision = "INSUFFICIENT_PARTICIPATION"
        elif votes_for > votes_against:
            decision = "FOR"
        elif votes_against > votes_for:
            decision = "AGAINST"
        else:
            decision = "TIE"

        # Check if approval required
        requires_approval = (
            proposal.impact_level in HIGH_IMPACT_LEVELS
            or proposal.budget_required > BUDGET_APPROVAL_THRESHOLD
        )

        # Collect amendments from counter-proposals
        amendments = []
        for counter in counters:
            amendments.extend(counter.compromise_points)

        result = ConsensusResult(
            proposal_id=proposal_id,
            total_votes=total_votes,
            votes_for=votes_for,
            votes_against=votes_against,
            votes_neutral=votes_neutral,
            counter_proposals=len(counters),
            participation_rate=participation_rate,
            zone_coverage=zones_represented / 10.0,  # Rough estimate
            consensus_level=consensus_level,
            consensus_percentage=consensus_pct,
            decision=decision,
            amendments=amendments[:5],  # Top 5 amendments
            requires_approval=requires_approval,
        )

        self._results[proposal_id] = result

        logger.info(
            f"Consensus calculated for {proposal_id}: "
            f"{decision} ({consensus_level.value}, {consensus_pct:.1%})"
        )

        return result

    def approve_decision(
        self,
        proposal_id: UUID,
        approver_name: str,
        approval_notes: str = "",
        with_amendments: Optional[List[str]] = None,
    ) -> ConsensusResult:
        """
        GOVERNANCE GATE: Final approval for high-impact decisions

        RULE #1: Human sovereignty over critical decisions
        """
        if proposal_id not in self._results:
            raise ValueError(f"No consensus result for proposal {proposal_id}")

        result = self._results[proposal_id]
        proposal = self._proposals[proposal_id]

        if not result.requires_approval:
            raise ValueError("This decision does not require approval")

        if result.approved_by is not None:
            raise ValueError("Decision already approved")

        now = datetime.now()
        result.approved_by = approver_name
        result.approved_at = now

        if with_amendments:
            result.amendments.extend(with_amendments)

        # Update proposal status
        proposal.status = ProposalStatus.APPROVED
        proposal.audit_log.append({
            "action": "decision_approved",
            "timestamp": now.isoformat(),
            "by": approver_name,
            "notes": approval_notes,
            "amendments": with_amendments or [],
        })

        logger.info(
            f"GOVERNANCE: Decision approved for {proposal_id} by {approver_name}"
        )

        return result

    # ========================================================================
    # DELIBERATION
    # ========================================================================

    def schedule_deliberation(
        self,
        proposal_id: UUID,
        scheduled_at: datetime,
        duration_minutes: int,
        facilitator_id: UUID,
    ) -> DeliberationSession:
        """Schedule a deliberation session for a proposal"""
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        session = DeliberationSession(
            id=uuid4(),
            proposal_id=proposal_id,
            scheduled_at=scheduled_at,
            duration_minutes=duration_minutes,
            facilitator_anon_id=anonymize_voter_id(facilitator_id, proposal_id),
            participants_count=0,
        )

        if proposal_id not in self._deliberations:
            self._deliberations[proposal_id] = []
        self._deliberations[proposal_id].append(session)

        return session

    def record_deliberation_outcome(
        self,
        session_id: UUID,
        participants_count: int,
        key_points: List[str],
        concerns_raised: List[str],
        suggested_amendments: List[str],
    ) -> DeliberationSession:
        """Record the outcome of a deliberation session"""
        # Find session
        session = None
        for sessions in self._deliberations.values():
            for s in sessions:
                if s.id == session_id:
                    session = s
                    break

        if session is None:
            raise ValueError(f"Session {session_id} not found")

        session.participants_count = participants_count
        session.key_points = key_points
        session.concerns_raised = concerns_raised
        session.suggested_amendments = suggested_amendments
        session.status = "completed"

        return session

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_proposals(
        self,
        status: Optional[ProposalStatus] = None,
        category: Optional[ProposalCategory] = None,
        scope: Optional[ProposalScope] = None,
    ) -> List[Proposal]:
        """
        Get proposals with optional filters

        GOVERNANCE RULE #5: Return in CHRONOLOGICAL order (by creation date)
        NO algorithmic ranking or scoring
        """
        proposals = list(self._proposals.values())

        if status:
            proposals = [p for p in proposals if p.status == status]
        if category:
            proposals = [p for p in proposals if p.category == category]
        if scope:
            proposals = [p for p in proposals if p.scope == scope]

        # RULE #5: CHRONOLOGICAL order only
        proposals.sort(key=lambda p: p.created_at)

        return proposals

    def get_proposal(self, proposal_id: UUID) -> Optional[Proposal]:
        """Get a specific proposal by ID"""
        return self._proposals.get(proposal_id)

    def get_votes(self, proposal_id: UUID) -> List[Vote]:
        """
        Get votes for a proposal

        PRIVACY: Returns anonymized voter IDs only
        GOVERNANCE RULE #5: Chronological order
        """
        votes = self._votes.get(proposal_id, [])
        # CHRONOLOGICAL order
        return sorted(votes, key=lambda v: v.timestamp)

    def get_vote_summary(self, proposal_id: UUID) -> Dict[str, Any]:
        """Get vote summary without individual vote details"""
        votes = self._votes.get(proposal_id, [])

        return {
            "proposal_id": str(proposal_id),
            "total_votes": len(votes),
            "votes_for": sum(1 for v in votes if v.vote_type == VoteType.FOR),
            "votes_against": sum(1 for v in votes if v.vote_type == VoteType.AGAINST),
            "votes_neutral": sum(1 for v in votes if v.vote_type == VoteType.NEUTRAL),
            "zones_represented": len(set(v.zone_id for v in votes)),
            # NO individual vote details for privacy
        }

    def get_result(self, proposal_id: UUID) -> Optional[ConsensusResult]:
        """Get consensus result for a proposal"""
        return self._results.get(proposal_id)

    # ========================================================================
    # METRICS & INDICES
    # ========================================================================

    def get_governance_metrics(self) -> GovernanceMetrics:
        """
        Get current governance health metrics

        INDICES SOCIAUX:
        - Democratic Vitality: How alive is citizen participation?
        - Deliberation Quality: Are debates constructive?
        - Implementation Rate: Are decisions being executed?
        """
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Count active proposals
        active_proposals = sum(
            1 for p in self._proposals.values()
            if p.status in {ProposalStatus.OPEN, ProposalStatus.DELIBERATION}
        )

        # Count today's votes
        total_votes_today = 0
        voters_today = set()
        for votes in self._votes.values():
            for v in votes:
                if v.timestamp >= today_start:
                    total_votes_today += 1
                    voters_today.add(v.voter_anon_id)

        # Calculate participation rate
        total_zones = len(self._zone_participation)
        participation_rate = len(voters_today) / max(total_zones * 100, 1)

        # Calculate consensus health
        results = list(self._results.values())
        if results:
            avg_consensus = sum(
                r.consensus_percentage for r in results
            ) / len(results)
            decisions_reached = sum(
                1 for r in results
                if r.decision in {"FOR", "AGAINST"}
            )
            decisions_blocked = sum(
                1 for r in results
                if r.decision == "INSUFFICIENT_PARTICIPATION"
            )
        else:
            avg_consensus = 0.0
            decisions_reached = 0
            decisions_blocked = 0

        # Calculate implementation rate
        approved = sum(
            1 for p in self._proposals.values()
            if p.status == ProposalStatus.APPROVED
        )
        implemented = sum(
            1 for p in self._proposals.values()
            if p.status == ProposalStatus.IMPLEMENTED
        )
        implementation_rate = implemented / max(approved, 1)

        # Calculate social indices

        # Democratic Vitality Index (0-1)
        # Based on: participation, proposal activity, vote distribution
        vitality_factors = [
            min(participation_rate * 5, 1.0),  # Participation normalized
            min(active_proposals / 10, 1.0),    # Activity normalized
            min(total_votes_today / 100, 1.0),  # Daily engagement
        ]
        democratic_vitality = sum(vitality_factors) / len(vitality_factors)

        # Deliberation Quality Index (0-1)
        # Based on: consensus levels, counter-proposals, amendments
        total_counters = sum(len(c) for c in self._counter_proposals.values())
        quality_factors = [
            avg_consensus,
            min(total_counters / 20, 1.0),  # Counter-proposal activity
            1.0 - (decisions_blocked / max(len(results), 1)),  # Low blockage
        ]
        deliberation_quality = sum(quality_factors) / len(quality_factors)

        metrics = GovernanceMetrics(
            timestamp=now,
            active_proposals=active_proposals,
            total_votes_today=total_votes_today,
            unique_voters_today=len(voters_today),
            participation_rate=participation_rate,
            avg_consensus_level=avg_consensus,
            decisions_reached=decisions_reached,
            decisions_blocked=decisions_blocked,
            democratic_vitality_index=democratic_vitality,
            deliberation_quality_index=deliberation_quality,
            implementation_rate=implementation_rate,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_social_indices(self) -> Dict[str, float]:
        """
        Get aggregated social indices for dashboard

        Returns indices that measure democratic health without
        individual tracking
        """
        metrics = self.get_governance_metrics()

        return {
            "democratic_vitality_index": round(metrics.democratic_vitality_index, 3),
            "deliberation_quality_index": round(metrics.deliberation_quality_index, 3),
            "implementation_rate": round(metrics.implementation_rate, 3),
            "participation_rate": round(metrics.participation_rate, 3),
            "consensus_average": round(metrics.avg_consensus_level, 3),
            # Composite governance health
            "governance_health": round(
                (metrics.democratic_vitality_index +
                 metrics.deliberation_quality_index +
                 metrics.implementation_rate) / 3,
                3
            ),
        }

    # ========================================================================
    # AUDIT
    # ========================================================================

    def get_audit_trail(self, proposal_id: UUID) -> List[Dict[str, Any]]:
        """
        Get full audit trail for a proposal

        GOVERNANCE RULE #6: Full traceability
        PRIVACY: Voter IDs are anonymized
        """
        if proposal_id not in self._proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        proposal = self._proposals[proposal_id]

        return proposal.audit_log.copy()


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_consensus_liquide_agent() -> ConsensusLiquideAgent:
    """Get the singleton ConsensusLiquideAgent instance"""
    return ConsensusLiquideAgent()
