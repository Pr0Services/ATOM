"""
CHE·NU V68 Privacy Guardian Agent
Les Gardiens de la Vie Privee

CONCEPT: Privacy by Design
- Protection des donnees personnelles a tous les niveaux
- Anonymisation systematique
- Audit des acces
- Detection des violations

PRINCIPES FONDAMENTAUX:
1. MINIMISATION: Ne collecter que le strict necessaire
2. ANONYMISATION: Toujours anonymiser par defaut
3. CONSENTEMENT: Explicit opt-in uniquement
4. TRANSPARENCE: L'utilisateur sait ce qu'on sait
5. EFFACEMENT: Droit a l'oubli garanti

GOVERNANCE COMPLIANCE:
- Rule #1: Acces aux donnees sensibles require APPROVAL
- Rule #4: NO AI-to-AI data sharing without human gate
- Rule #6: Full audit trail
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any, Set, Callable
from uuid import UUID, uuid4
import logging
import hashlib
import re

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class DataCategory(Enum):
    """Categories de donnees selon sensibilite"""
    PUBLIC = "public"                # Donnees publiques
    INTERNAL = "internal"            # Usage interne
    CONFIDENTIAL = "confidential"    # Confidentiel
    SENSITIVE = "sensitive"          # Sensible (sante, finances)
    CRITICAL = "critical"            # Critique (identite, biometrie)


class DataType(Enum):
    """Types de donnees personnelles"""
    IDENTITY = "identity"            # Nom, prenom
    CONTACT = "contact"              # Email, telephone
    LOCATION = "location"            # Localisation
    FINANCIAL = "financial"          # Donnees financieres
    HEALTH = "health"                # Donnees de sante
    BIOMETRIC = "biometric"          # Donnees biometriques
    BEHAVIORAL = "behavioral"        # Comportement
    PREFERENCES = "preferences"      # Preferences
    SOCIAL = "social"                # Reseau social
    PROFESSIONAL = "professional"    # Professionnel


class ProcessingPurpose(Enum):
    """Finalites de traitement"""
    SERVICE_DELIVERY = "service_delivery"    # Fourniture du service
    ANALYTICS = "analytics"                  # Analytique (anonymise)
    IMPROVEMENT = "improvement"              # Amelioration
    SAFETY = "safety"                        # Securite
    LEGAL = "legal"                          # Obligation legale
    RESEARCH = "research"                    # Recherche (anonymise)


class ConsentStatus(Enum):
    """Statut du consentement"""
    NOT_REQUESTED = "not_requested"
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"


class ViolationType(Enum):
    """Types de violations"""
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    EXCESSIVE_COLLECTION = "excessive_collection"
    PURPOSE_DEVIATION = "purpose_deviation"
    RETENTION_EXCEEDED = "retention_exceeded"
    MISSING_CONSENT = "missing_consent"
    ANONYMIZATION_FAILURE = "anonymization_failure"
    DATA_LEAK = "data_leak"


class AlertLevel(Enum):
    """Niveau d'alerte"""
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DataAccessRequest:
    """Demande d'acces aux donnees"""
    id: UUID
    requester_type: str          # agent, service, human
    requester_id: str
    data_type: DataType
    data_category: DataCategory
    purpose: ProcessingPurpose

    # Scope
    scope: str                   # Description de ce qui est demande
    retention_hours: int         # Duree de retention demandee

    # Status
    status: str = "pending"      # pending, approved, denied
    timestamp: datetime = field(default_factory=datetime.now)

    # GOVERNANCE
    requires_approval: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    denial_reason: Optional[str] = None


@dataclass
class DataSubjectRecord:
    """Enregistrement d'un sujet de donnees (anonymise)"""
    id: UUID
    subject_hash: str            # Hash du sujet (JAMAIS l'ID reel)

    # Consents
    consents: Dict[str, ConsentStatus]  # purpose -> status
    consent_dates: Dict[str, datetime]

    # Data holdings
    data_types_held: Set[DataType]
    data_categories: Dict[str, DataCategory]

    # Rights exercised
    access_requests: int = 0
    rectification_requests: int = 0
    erasure_requests: int = 0

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)


@dataclass
class PrivacyViolation:
    """Violation de vie privee detectee"""
    id: UUID
    violation_type: ViolationType
    alert_level: AlertLevel

    # Details
    description: str
    affected_data_type: DataType
    affected_subjects_count: int  # Nombre approximatif

    # Source
    source_service: str
    detected_by: str             # Scanner, audit, report

    # Status
    status: str = "open"         # open, investigating, mitigated, closed
    detected_at: datetime = field(default_factory=datetime.now)

    # Response
    remediation_actions: List[str] = field(default_factory=list)
    closed_at: Optional[datetime] = None


@dataclass
class AnonymizationRule:
    """Regle d'anonymisation"""
    id: UUID
    name: str
    data_type: DataType

    # Rule
    pattern: str                 # Regex pattern to detect
    method: str                  # hash, mask, generalize, suppress
    parameters: Dict[str, Any]

    # Scope
    applies_to_services: List[str]
    active: bool = True


@dataclass
class RetentionPolicy:
    """Politique de retention"""
    id: UUID
    data_type: DataType
    data_category: DataCategory

    # Retention
    retention_days: int
    archive_days: int            # After retention, before deletion
    auto_delete: bool

    # Legal basis
    legal_basis: str
    notes: str = ""


@dataclass
class PrivacyMetrics:
    """Metriques de vie privee"""
    timestamp: datetime

    # Data subjects
    total_subjects: int
    subjects_with_full_consent: int
    pending_consent_requests: int

    # Access
    access_requests_today: int
    access_denied_today: int
    approval_rate: float

    # Violations
    open_violations: int
    violations_resolved_month: int

    # Compliance
    consent_coverage: float      # % with valid consent
    anonymization_coverage: float  # % data anonymized
    retention_compliance: float  # % within retention limits

    # Index
    privacy_health_index: float  # 0-1


# ============================================================================
# GOVERNANCE THRESHOLDS
# ============================================================================

# Data categories requiring approval
APPROVAL_REQUIRED_CATEGORIES = {DataCategory.SENSITIVE, DataCategory.CRITICAL}

# Data types always requiring approval
APPROVAL_REQUIRED_TYPES = {DataType.HEALTH, DataType.BIOMETRIC, DataType.FINANCIAL}

# Maximum retention without justification (days)
MAX_DEFAULT_RETENTION = 30


# ============================================================================
# PRIVACY GUARDIAN AGENT
# ============================================================================

class PrivacyGuardianAgent:
    """
    Agent Gardien de la Vie Privee

    Les yeux qui veillent sans voir:
    - Proteger sans controler
    - Anonymiser sans perdre
    - Tracer sans identifier

    Mission: La vie privee est un droit, pas un privilege
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
        self._access_requests: Dict[UUID, DataAccessRequest] = {}
        self._subjects: Dict[str, DataSubjectRecord] = {}  # hash -> record
        self._violations: Dict[UUID, PrivacyViolation] = {}
        self._anonymization_rules: Dict[UUID, AnonymizationRule] = {}
        self._retention_policies: Dict[UUID, RetentionPolicy] = {}

        # Audit log
        self._audit_log: List[Dict[str, Any]] = []

        # Metrics history
        self._metrics_history: List[PrivacyMetrics] = []

        self._initialized = True
        logger.info("PrivacyGuardianAgent initialized - Protecting privacy rights")

        # Initialize default rules
        self._init_default_rules()

    def _init_default_rules(self) -> None:
        """Initialize default anonymization rules"""
        default_rules = [
            ("Email Anonymization", DataType.CONTACT,
             r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
             "hash", {"prefix_length": 3}),
            ("Phone Anonymization", DataType.CONTACT,
             r"\+?[0-9]{10,15}",
             "mask", {"visible_digits": 4}),
            ("Location Reduction", DataType.LOCATION,
             r"[-]?[0-9]+\.[0-9]{3,}",
             "generalize", {"precision": 2}),
            ("Name Pseudonymization", DataType.IDENTITY,
             r"[A-Z][a-z]+ [A-Z][a-z]+",
             "hash", {"preserve_format": False}),
        ]

        for name, dtype, pattern, method, params in default_rules:
            self.add_anonymization_rule(
                name=name,
                data_type=dtype,
                pattern=pattern,
                method=method,
                parameters=params,
            )

        # Default retention policies
        default_retention = [
            (DataType.LOCATION, DataCategory.INTERNAL, 7, 0, True),
            (DataType.BEHAVIORAL, DataCategory.INTERNAL, 30, 30, True),
            (DataType.PREFERENCES, DataCategory.CONFIDENTIAL, 365, 90, False),
            (DataType.HEALTH, DataCategory.SENSITIVE, 730, 365, False),
        ]

        for dtype, dcat, retention, archive, auto_del in default_retention:
            self.add_retention_policy(
                data_type=dtype,
                data_category=dcat,
                retention_days=retention,
                archive_days=archive,
                auto_delete=auto_del,
                legal_basis="Default policy",
            )

    # ========================================================================
    # ANONYMIZATION
    # ========================================================================

    def add_anonymization_rule(
        self,
        name: str,
        data_type: DataType,
        pattern: str,
        method: str,
        parameters: Dict[str, Any],
        applies_to_services: Optional[List[str]] = None,
    ) -> AnonymizationRule:
        """Add an anonymization rule"""
        rule = AnonymizationRule(
            id=uuid4(),
            name=name,
            data_type=data_type,
            pattern=pattern,
            method=method,
            parameters=parameters,
            applies_to_services=applies_to_services or ["*"],
        )

        self._anonymization_rules[rule.id] = rule

        return rule

    def anonymize(
        self,
        data: str,
        data_type: DataType,
        service: str = "*",
    ) -> str:
        """
        Anonymize data according to rules

        Returns anonymized version or original if no rule applies
        """
        # Find applicable rules
        for rule in self._anonymization_rules.values():
            if not rule.active:
                continue
            if rule.data_type != data_type:
                continue
            if "*" not in rule.applies_to_services and service not in rule.applies_to_services:
                continue

            # Check if pattern matches
            if not re.search(rule.pattern, data):
                continue

            # Apply anonymization method
            if rule.method == "hash":
                return self._hash_anonymize(data, rule.parameters)
            elif rule.method == "mask":
                return self._mask_anonymize(data, rule.parameters)
            elif rule.method == "generalize":
                return self._generalize_anonymize(data, rule.parameters)
            elif rule.method == "suppress":
                return "[REDACTED]"

        return data  # No rule matched

    def _hash_anonymize(self, data: str, params: Dict[str, Any]) -> str:
        """Hash-based anonymization"""
        salt = "CHENU_PRIVACY_SALT_999Hz"
        hashed = hashlib.sha256(f"{salt}{data}{salt}".encode()).hexdigest()[:16]

        if params.get("prefix_length", 0) > 0:
            prefix = data[:params["prefix_length"]]
            return f"{prefix}***{hashed[:8]}"

        return f"anon_{hashed}"

    def _mask_anonymize(self, data: str, params: Dict[str, Any]) -> str:
        """Mask-based anonymization"""
        visible = params.get("visible_digits", 4)
        if len(data) <= visible:
            return "*" * len(data)
        return "*" * (len(data) - visible) + data[-visible:]

    def _generalize_anonymize(self, data: str, params: Dict[str, Any]) -> str:
        """Generalization-based anonymization"""
        precision = params.get("precision", 2)
        try:
            value = float(data)
            return str(round(value, precision))
        except ValueError:
            return data

    # ========================================================================
    # DATA ACCESS CONTROL
    # ========================================================================

    def request_data_access(
        self,
        requester_type: str,
        requester_id: str,
        data_type: DataType,
        data_category: DataCategory,
        purpose: ProcessingPurpose,
        scope: str,
        retention_hours: int = 24,
    ) -> DataAccessRequest:
        """
        Request access to data

        GOVERNANCE: Sensitive/Critical data requires human approval
        """
        requires_approval = (
            data_category in APPROVAL_REQUIRED_CATEGORIES
            or data_type in APPROVAL_REQUIRED_TYPES
        )

        request = DataAccessRequest(
            id=uuid4(),
            requester_type=requester_type,
            requester_id=requester_id,
            data_type=data_type,
            data_category=data_category,
            purpose=purpose,
            scope=scope,
            retention_hours=retention_hours,
            requires_approval=requires_approval,
            status="pending" if requires_approval else "auto_approved",
        )

        self._access_requests[request.id] = request

        # Audit log
        self._log_audit(
            action="data_access_request",
            request_id=str(request.id),
            requester=requester_id,
            data_type=data_type.value,
            requires_approval=requires_approval,
        )

        if not requires_approval:
            logger.info(
                f"Data access auto-approved: {data_type.value} for {requester_id}"
            )

        return request

    def approve_access(
        self,
        request_id: UUID,
        approver_name: str,
        approval_notes: str = "",
    ) -> DataAccessRequest:
        """
        GOVERNANCE GATE: Approve data access request

        RULE #1: Human approval for sensitive data
        """
        if request_id not in self._access_requests:
            raise ValueError(f"Request {request_id} not found")

        request = self._access_requests[request_id]

        if request.status != "pending":
            raise ValueError(f"Request not pending (status: {request.status})")

        request.status = "approved"
        request.approved_by = approver_name
        request.approved_at = datetime.now()

        self._log_audit(
            action="data_access_approved",
            request_id=str(request_id),
            approved_by=approver_name,
            notes=approval_notes,
        )

        logger.info(f"GOVERNANCE: Data access {request_id} approved by {approver_name}")

        return request

    def deny_access(
        self,
        request_id: UUID,
        reason: str,
    ) -> DataAccessRequest:
        """Deny a data access request"""
        if request_id not in self._access_requests:
            raise ValueError(f"Request {request_id} not found")

        request = self._access_requests[request_id]
        request.status = "denied"
        request.denial_reason = reason

        self._log_audit(
            action="data_access_denied",
            request_id=str(request_id),
            reason=reason,
        )

        return request

    # ========================================================================
    # CONSENT MANAGEMENT
    # ========================================================================

    def register_subject(
        self,
        subject_id: UUID,
        initial_data_types: Optional[Set[DataType]] = None,
    ) -> DataSubjectRecord:
        """Register a data subject (anonymized)"""
        subject_hash = self._hash_subject_id(subject_id)

        if subject_hash in self._subjects:
            return self._subjects[subject_hash]

        record = DataSubjectRecord(
            id=uuid4(),
            subject_hash=subject_hash,
            consents={},
            consent_dates={},
            data_types_held=initial_data_types or set(),
            data_categories={},
        )

        self._subjects[subject_hash] = record

        return record

    def _hash_subject_id(self, subject_id: UUID) -> str:
        """Hash subject ID for privacy"""
        salt = "CHENU_SUBJECT_HASH_999Hz"
        return hashlib.sha256(f"{salt}{str(subject_id)}{salt}".encode()).hexdigest()[:24]

    def record_consent(
        self,
        subject_id: UUID,
        purpose: ProcessingPurpose,
        granted: bool,
    ) -> DataSubjectRecord:
        """Record consent decision"""
        subject_hash = self._hash_subject_id(subject_id)

        if subject_hash not in self._subjects:
            self.register_subject(subject_id)

        record = self._subjects[subject_hash]

        record.consents[purpose.value] = (
            ConsentStatus.GRANTED if granted else ConsentStatus.DENIED
        )
        record.consent_dates[purpose.value] = datetime.now()
        record.last_activity = datetime.now()

        self._log_audit(
            action="consent_recorded",
            subject_hash=subject_hash[:8],  # Truncated for log
            purpose=purpose.value,
            granted=granted,
        )

        return record

    def check_consent(
        self,
        subject_id: UUID,
        purpose: ProcessingPurpose,
    ) -> bool:
        """Check if subject has valid consent for purpose"""
        subject_hash = self._hash_subject_id(subject_id)

        if subject_hash not in self._subjects:
            return False

        record = self._subjects[subject_hash]

        status = record.consents.get(purpose.value)
        return status == ConsentStatus.GRANTED

    # ========================================================================
    # VIOLATION DETECTION
    # ========================================================================

    def report_violation(
        self,
        violation_type: ViolationType,
        description: str,
        affected_data_type: DataType,
        affected_subjects_count: int,
        source_service: str,
        detected_by: str = "manual_report",
        alert_level: Optional[AlertLevel] = None,
    ) -> PrivacyViolation:
        """Report a privacy violation"""
        # Auto-determine alert level if not provided
        if alert_level is None:
            if affected_subjects_count > 100:
                alert_level = AlertLevel.CRITICAL
            elif affected_subjects_count > 10:
                alert_level = AlertLevel.HIGH
            elif violation_type in {ViolationType.DATA_LEAK, ViolationType.UNAUTHORIZED_ACCESS}:
                alert_level = AlertLevel.HIGH
            else:
                alert_level = AlertLevel.WARNING

        violation = PrivacyViolation(
            id=uuid4(),
            violation_type=violation_type,
            alert_level=alert_level,
            description=description,
            affected_data_type=affected_data_type,
            affected_subjects_count=affected_subjects_count,
            source_service=source_service,
            detected_by=detected_by,
        )

        self._violations[violation.id] = violation

        self._log_audit(
            action="violation_reported",
            violation_id=str(violation.id),
            type=violation_type.value,
            level=alert_level.value,
            affected_count=affected_subjects_count,
        )

        logger.warning(
            f"PRIVACY VIOLATION: {alert_level.value.upper()} - {violation_type.value} "
            f"({affected_subjects_count} subjects affected)"
        )

        return violation

    def mitigate_violation(
        self,
        violation_id: UUID,
        remediation_actions: List[str],
        mitigator_name: str,
    ) -> PrivacyViolation:
        """Record mitigation of a violation"""
        if violation_id not in self._violations:
            raise ValueError(f"Violation {violation_id} not found")

        violation = self._violations[violation_id]
        violation.status = "mitigated"
        violation.remediation_actions = remediation_actions
        violation.closed_at = datetime.now()

        self._log_audit(
            action="violation_mitigated",
            violation_id=str(violation_id),
            mitigated_by=mitigator_name,
            actions=remediation_actions,
        )

        return violation

    # ========================================================================
    # RETENTION POLICIES
    # ========================================================================

    def add_retention_policy(
        self,
        data_type: DataType,
        data_category: DataCategory,
        retention_days: int,
        archive_days: int,
        auto_delete: bool,
        legal_basis: str,
        notes: str = "",
    ) -> RetentionPolicy:
        """Add a data retention policy"""
        policy = RetentionPolicy(
            id=uuid4(),
            data_type=data_type,
            data_category=data_category,
            retention_days=retention_days,
            archive_days=archive_days,
            auto_delete=auto_delete,
            legal_basis=legal_basis,
            notes=notes,
        )

        self._retention_policies[policy.id] = policy

        return policy

    def check_retention_compliance(
        self,
        data_type: DataType,
        data_category: DataCategory,
        data_age_days: int,
    ) -> Dict[str, Any]:
        """Check if data is within retention limits"""
        # Find applicable policy
        for policy in self._retention_policies.values():
            if policy.data_type == data_type and policy.data_category == data_category:
                total_allowed = policy.retention_days + policy.archive_days
                return {
                    "compliant": data_age_days <= total_allowed,
                    "in_retention": data_age_days <= policy.retention_days,
                    "in_archive": (
                        policy.retention_days < data_age_days <= total_allowed
                    ),
                    "should_delete": data_age_days > total_allowed,
                    "days_until_archive": max(0, policy.retention_days - data_age_days),
                    "days_until_delete": max(0, total_allowed - data_age_days),
                }

        # No policy found, use defaults
        return {
            "compliant": data_age_days <= MAX_DEFAULT_RETENTION,
            "in_retention": data_age_days <= MAX_DEFAULT_RETENTION,
            "in_archive": False,
            "should_delete": data_age_days > MAX_DEFAULT_RETENTION,
            "policy_found": False,
        }

    # ========================================================================
    # AUDIT
    # ========================================================================

    def _log_audit(self, **kwargs) -> None:
        """Add entry to audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        }
        self._audit_log.append(entry)

        # Keep only last 10000 entries
        if len(self._audit_log) > 10000:
            self._audit_log = self._audit_log[-10000:]

    def get_audit_log(
        self,
        since: Optional[datetime] = None,
        action: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get audit log entries

        GOVERNANCE RULE #6: Full audit trail
        """
        entries = self._audit_log.copy()

        if since:
            since_str = since.isoformat()
            entries = [e for e in entries if e["timestamp"] >= since_str]

        if action:
            entries = [e for e in entries if e.get("action") == action]

        # Chronological order, most recent last
        entries.sort(key=lambda e: e["timestamp"])

        return entries[-limit:]

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_access_requests(
        self,
        status: Optional[str] = None,
    ) -> List[DataAccessRequest]:
        """Get data access requests"""
        requests = list(self._access_requests.values())

        if status:
            requests = [r for r in requests if r.status == status]

        # Chronological order
        requests.sort(key=lambda r: r.timestamp)

        return requests

    def get_violations(
        self,
        status: Optional[str] = None,
        alert_level: Optional[AlertLevel] = None,
    ) -> List[PrivacyViolation]:
        """Get violations"""
        violations = list(self._violations.values())

        if status:
            violations = [v for v in violations if v.status == status]
        if alert_level:
            violations = [v for v in violations if v.alert_level == alert_level]

        # Chronological order
        violations.sort(key=lambda v: v.detected_at)

        return violations

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_privacy_metrics(self) -> PrivacyMetrics:
        """Get privacy health metrics"""
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_ago = now - timedelta(days=30)

        # Subject counts
        subjects = list(self._subjects.values())
        total = len(subjects)

        # Consent coverage
        full_consent = sum(
            1 for s in subjects
            if all(
                c == ConsentStatus.GRANTED
                for c in s.consents.values()
            ) and s.consents
        )

        pending_consents = sum(
            1 for s in subjects
            if any(c == ConsentStatus.PENDING for c in s.consents.values())
        )

        # Access requests
        requests = list(self._access_requests.values())
        today_requests = [r for r in requests if r.timestamp >= today_start]
        today_denied = [r for r in today_requests if r.status == "denied"]
        approval_rate = (
            (len(today_requests) - len(today_denied)) / len(today_requests)
            if today_requests else 1.0
        )

        # Violations
        violations = list(self._violations.values())
        open_violations = sum(1 for v in violations if v.status == "open")
        resolved_month = sum(
            1 for v in violations
            if v.status in {"mitigated", "closed"} and v.detected_at >= month_ago
        )

        # Calculate indices

        # Consent coverage
        consent_coverage = full_consent / max(total, 1)

        # Anonymization coverage (estimate based on rules)
        anonymization_coverage = min(len(self._anonymization_rules) / 10, 1.0)

        # Retention compliance (estimate)
        retention_compliance = 1.0 - (open_violations * 0.1)
        retention_compliance = max(0, retention_compliance)

        # Privacy health index
        privacy_health = (
            consent_coverage * 0.3 +
            anonymization_coverage * 0.2 +
            retention_compliance * 0.2 +
            approval_rate * 0.15 +
            (1 - min(open_violations / 10, 1)) * 0.15
        )

        metrics = PrivacyMetrics(
            timestamp=now,
            total_subjects=total,
            subjects_with_full_consent=full_consent,
            pending_consent_requests=pending_consents,
            access_requests_today=len(today_requests),
            access_denied_today=len(today_denied),
            approval_rate=approval_rate,
            open_violations=open_violations,
            violations_resolved_month=resolved_month,
            consent_coverage=consent_coverage,
            anonymization_coverage=anonymization_coverage,
            retention_compliance=retention_compliance,
            privacy_health_index=privacy_health,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_privacy_indices(self) -> Dict[str, float]:
        """Get privacy indices for master dashboard"""
        metrics = self.get_privacy_metrics()

        return {
            "privacy_health_index": round(metrics.privacy_health_index, 3),
            "consent_coverage": round(metrics.consent_coverage, 3),
            "anonymization_coverage": round(metrics.anonymization_coverage, 3),
            "retention_compliance": round(metrics.retention_compliance, 3),
            "open_violations": metrics.open_violations,
        }


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_privacy_guardian_agent() -> PrivacyGuardianAgent:
    """Get the singleton PrivacyGuardianAgent instance"""
    return PrivacyGuardianAgent()
