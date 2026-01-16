"""
CHE·NU V68 Master Dashboard Agent
AT·OM Vision - Le Tableau de Bord Maitre

CONCEPT: Vision Unifiee
- Agregation de tous les indices
- Heatmap globale de l'ecosysteme
- Alertes croisees entre domaines
- Frequence 999Hz - Bleu cobalt = harmonie

VISUALISATION:
- Vert = Harmonieux, en equilibre
- Jaune = Attention, surveillance
- Rouge = Friction, intervention requise
- Bleu Cobalt 999Hz = Flux optimal

GOVERNANCE COMPLIANCE:
- Rule #1: Cross-domain interventions require APPROVAL
- Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL
- Rule #6: Full audit trail from all sources
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any, Callable
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class DomainType(Enum):
    """Domaines du systeme AT·OM"""
    TRANSPORT = "transport"          # AT·OM Flow
    SOCIETAL = "societal"            # Equilibre, Education, Sante, Gouvernance
    ENVIRONMENT = "environment"      # Regeneration, Energie, Biodiversite, Circulaire
    COMMUNITY = "community"          # Community Pulse
    PRIVACY = "privacy"              # Privacy Guardian
    CONSTRUCTION = "construction"    # Bau·M


class HealthStatus(Enum):
    """Statut de sante global"""
    CRITICAL = "critical"            # Rouge vif
    WARNING = "warning"              # Orange
    ATTENTION = "attention"          # Jaune
    STABLE = "stable"                # Vert clair
    OPTIMAL = "optimal"              # Vert
    FLOW_999 = "flow_999"            # Bleu cobalt - frequence parfaite


class AlertType(Enum):
    """Types d'alertes cross-domain"""
    SINGLE_DOMAIN = "single_domain"
    CROSS_DOMAIN = "cross_domain"
    SYSTEMIC = "systemic"


class TrendDirection(Enum):
    """Direction de tendance"""
    DECLINING_FAST = "declining_fast"
    DECLINING = "declining"
    STABLE = "stable"
    IMPROVING = "improving"
    IMPROVING_FAST = "improving_fast"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class DomainStatus:
    """Statut d'un domaine"""
    domain: DomainType
    name: str

    # Health
    health_index: float          # 0-1
    status: HealthStatus

    # Trend
    trend: TrendDirection
    trend_velocity: float        # Rate of change

    # Key indices from domain
    key_indices: Dict[str, float]

    # Alerts
    active_alerts: int
    pending_approvals: int

    # Last update
    last_update: datetime


@dataclass
class GlobalIndex:
    """Index global calcule"""
    name: str
    value: float                 # 0-1
    status: HealthStatus

    # Components
    component_indices: Dict[str, float]
    weights: Dict[str, float]

    # Trend
    previous_value: float
    trend: TrendDirection

    # Meta
    last_calculated: datetime


@dataclass
class CrossDomainAlert:
    """Alerte cross-domaine"""
    id: UUID
    alert_type: AlertType

    # Domains involved
    domains: List[DomainType]
    primary_domain: DomainType

    # Details
    title: str
    description: str
    severity: str               # info, warning, high, critical

    # Indices triggering
    triggering_indices: Dict[str, float]
    thresholds_crossed: Dict[str, float]

    # Status
    status: str = "active"      # active, acknowledged, investigating, resolved
    created_at: datetime = field(default_factory=datetime.now)

    # GOVERNANCE
    requires_approval: bool = False
    approved_by: Optional[str] = None


@dataclass
class HeatmapCell:
    """Cellule de heatmap"""
    zone_id: str
    zone_name: str

    # Position (for visualization)
    latitude: float
    longitude: float

    # Values by domain
    domain_values: Dict[str, float]

    # Aggregate
    aggregate_score: float
    status: HealthStatus
    color: str                  # Hex color


@dataclass
class SystemMetrics:
    """Metriques systeme globales"""
    timestamp: datetime

    # Domain health
    domains_optimal: int
    domains_stable: int
    domains_attention: int
    domains_warning: int
    domains_critical: int

    # Alerts
    total_active_alerts: int
    cross_domain_alerts: int
    pending_approvals: int

    # Global indices
    global_harmony_index: float
    global_sustainability_index: float
    global_resilience_index: float
    global_privacy_index: float

    # Master index
    atom_frequency: float        # 0-1, 1 = 999Hz optimal


# ============================================================================
# COLOR MAPPING
# ============================================================================

STATUS_COLORS = {
    HealthStatus.CRITICAL: "#FF0000",       # Red
    HealthStatus.WARNING: "#FFA500",        # Orange
    HealthStatus.ATTENTION: "#FFFF00",      # Yellow
    HealthStatus.STABLE: "#90EE90",         # Light green
    HealthStatus.OPTIMAL: "#00FF00",        # Green
    HealthStatus.FLOW_999: "#0047AB",       # Cobalt blue - 999Hz
}


# ============================================================================
# MASTER DASHBOARD AGENT
# ============================================================================

class MasterDashboardAgent:
    """
    Agent du Tableau de Bord Maitre

    AT·OM Vision - Voir l'invisible:
    - Tous les flux convergent ici
    - Toutes les harmonies se revelent
    - Tous les desequilibres s'alertent

    La frequence 999Hz est notre objectif:
    Quand tout est bleu cobalt, le systeme chante.
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

        # Domain status cache
        self._domain_status: Dict[DomainType, DomainStatus] = {}

        # Global indices
        self._global_indices: Dict[str, GlobalIndex] = {}

        # Alerts
        self._alerts: Dict[UUID, CrossDomainAlert] = {}

        # Heatmap data
        self._heatmap: Dict[str, HeatmapCell] = {}

        # Metrics history
        self._metrics_history: List[SystemMetrics] = []

        # Index collectors (functions to call for each domain)
        self._index_collectors: Dict[DomainType, Callable] = {}

        self._initialized = True
        logger.info("MasterDashboardAgent initialized - AT·OM Vision active")

    # ========================================================================
    # DOMAIN REGISTRATION
    # ========================================================================

    def register_domain(
        self,
        domain: DomainType,
        name: str,
        index_collector: Optional[Callable] = None,
    ) -> DomainStatus:
        """Register a domain for monitoring"""
        status = DomainStatus(
            domain=domain,
            name=name,
            health_index=0.5,
            status=HealthStatus.STABLE,
            trend=TrendDirection.STABLE,
            trend_velocity=0.0,
            key_indices={},
            active_alerts=0,
            pending_approvals=0,
            last_update=datetime.now(),
        )

        self._domain_status[domain] = status

        if index_collector:
            self._index_collectors[domain] = index_collector

        logger.info(f"Domain registered: {name} ({domain.value})")

        return status

    # ========================================================================
    # INDEX COLLECTION
    # ========================================================================

    def update_domain_indices(
        self,
        domain: DomainType,
        indices: Dict[str, float],
        active_alerts: int = 0,
        pending_approvals: int = 0,
    ) -> DomainStatus:
        """Update indices for a domain"""
        if domain not in self._domain_status:
            raise ValueError(f"Domain {domain.value} not registered")

        status = self._domain_status[domain]
        old_health = status.health_index

        # Calculate health index from indices
        if indices:
            # Average of all indices
            health = sum(indices.values()) / len(indices)
        else:
            health = 0.5

        # Determine status
        if health >= 0.9:
            new_status = HealthStatus.FLOW_999  # Perfect harmony
        elif health >= 0.75:
            new_status = HealthStatus.OPTIMAL
        elif health >= 0.6:
            new_status = HealthStatus.STABLE
        elif health >= 0.4:
            new_status = HealthStatus.ATTENTION
        elif health >= 0.25:
            new_status = HealthStatus.WARNING
        else:
            new_status = HealthStatus.CRITICAL

        # Calculate trend
        velocity = health - old_health
        if velocity > 0.05:
            trend = TrendDirection.IMPROVING_FAST
        elif velocity > 0.02:
            trend = TrendDirection.IMPROVING
        elif velocity < -0.05:
            trend = TrendDirection.DECLINING_FAST
        elif velocity < -0.02:
            trend = TrendDirection.DECLINING
        else:
            trend = TrendDirection.STABLE

        # Update status
        status.health_index = health
        status.status = new_status
        status.trend = trend
        status.trend_velocity = velocity
        status.key_indices = indices
        status.active_alerts = active_alerts
        status.pending_approvals = pending_approvals
        status.last_update = datetime.now()

        # Check for cross-domain alerts
        self._check_cross_domain_alerts(domain, indices)

        return status

    def collect_all_indices(self) -> Dict[DomainType, Dict[str, float]]:
        """Collect indices from all registered domains"""
        all_indices = {}

        for domain, collector in self._index_collectors.items():
            try:
                indices = collector()
                all_indices[domain] = indices
                self.update_domain_indices(domain, indices)
            except Exception as e:
                logger.error(f"Failed to collect indices from {domain.value}: {e}")
                all_indices[domain] = {}

        return all_indices

    # ========================================================================
    # GLOBAL INDEX CALCULATION
    # ========================================================================

    def calculate_global_indices(self) -> Dict[str, GlobalIndex]:
        """Calculate all global indices"""
        now = datetime.now()

        # Collect current domain health
        domain_health = {
            d: s.health_index
            for d, s in self._domain_status.items()
        }

        # Global Harmony Index
        # Weighted average: Community pulse highest weight
        harmony_weights = {
            DomainType.COMMUNITY: 0.3,
            DomainType.SOCIETAL: 0.25,
            DomainType.ENVIRONMENT: 0.2,
            DomainType.TRANSPORT: 0.15,
            DomainType.PRIVACY: 0.1,
        }
        harmony_value = self._calculate_weighted_index(domain_health, harmony_weights)
        self._global_indices["harmony"] = self._create_global_index(
            "Global Harmony Index", harmony_value, harmony_weights, now
        )

        # Global Sustainability Index
        # Environment and circular economy weighted highest
        sustainability_weights = {
            DomainType.ENVIRONMENT: 0.4,
            DomainType.SOCIETAL: 0.25,
            DomainType.TRANSPORT: 0.2,
            DomainType.COMMUNITY: 0.15,
        }
        sustainability_value = self._calculate_weighted_index(domain_health, sustainability_weights)
        self._global_indices["sustainability"] = self._create_global_index(
            "Global Sustainability Index", sustainability_value, sustainability_weights, now
        )

        # Global Resilience Index
        # Based on trend stability and alert resolution
        resilience_factors = []
        for status in self._domain_status.values():
            # Stable trends contribute to resilience
            if status.trend == TrendDirection.STABLE:
                resilience_factors.append(0.8)
            elif status.trend in {TrendDirection.IMPROVING, TrendDirection.IMPROVING_FAST}:
                resilience_factors.append(1.0)
            else:
                resilience_factors.append(0.5)

        resilience_value = sum(resilience_factors) / max(len(resilience_factors), 1)
        self._global_indices["resilience"] = GlobalIndex(
            name="Global Resilience Index",
            value=resilience_value,
            status=self._value_to_status(resilience_value),
            component_indices={d.value: f for d, f in zip(self._domain_status.keys(), resilience_factors)},
            weights={},
            previous_value=self._global_indices.get("resilience", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value,
            trend=TrendDirection.STABLE,
            last_calculated=now,
        )

        # Global Privacy Index
        privacy_status = self._domain_status.get(DomainType.PRIVACY)
        privacy_value = privacy_status.health_index if privacy_status else 0.5
        self._global_indices["privacy"] = GlobalIndex(
            name="Global Privacy Index",
            value=privacy_value,
            status=self._value_to_status(privacy_value),
            component_indices=privacy_status.key_indices if privacy_status else {},
            weights={},
            previous_value=self._global_indices.get("privacy", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value,
            trend=TrendDirection.STABLE,
            last_calculated=now,
        )

        # AT·OM Frequency (Master Index)
        # When this reaches 1.0, we're at 999Hz
        atom_components = {
            "harmony": harmony_value,
            "sustainability": sustainability_value,
            "resilience": resilience_value,
            "privacy": privacy_value,
        }
        atom_value = sum(atom_components.values()) / len(atom_components)
        self._global_indices["atom_frequency"] = GlobalIndex(
            name="AT·OM Frequency",
            value=atom_value,
            status=HealthStatus.FLOW_999 if atom_value >= 0.9 else self._value_to_status(atom_value),
            component_indices=atom_components,
            weights={"harmony": 0.25, "sustainability": 0.25, "resilience": 0.25, "privacy": 0.25},
            previous_value=self._global_indices.get("atom_frequency", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value,
            trend=TrendDirection.STABLE,
            last_calculated=now,
        )

        return self._global_indices

    def _calculate_weighted_index(
        self,
        values: Dict[DomainType, float],
        weights: Dict[DomainType, float],
    ) -> float:
        """Calculate weighted average index"""
        total = 0.0
        total_weight = 0.0

        for domain, weight in weights.items():
            if domain in values:
                total += values[domain] * weight
                total_weight += weight

        return total / total_weight if total_weight > 0 else 0.5

    def _create_global_index(
        self,
        name: str,
        value: float,
        weights: Dict[DomainType, float],
        timestamp: datetime,
    ) -> GlobalIndex:
        """Create a global index object"""
        existing = self._global_indices.get(name.lower().replace(" ", "_"))
        previous = existing.value if existing else 0.5

        return GlobalIndex(
            name=name,
            value=value,
            status=self._value_to_status(value),
            component_indices={d.value: self._domain_status.get(d, DomainStatus(d, "", 0.5, HealthStatus.STABLE, TrendDirection.STABLE, 0, {}, 0, 0, timestamp)).health_index for d in weights.keys()},
            weights={d.value: w for d, w in weights.items()},
            previous_value=previous,
            trend=self._calculate_trend(previous, value),
            last_calculated=timestamp,
        )

    def _value_to_status(self, value: float) -> HealthStatus:
        """Convert value to health status"""
        if value >= 0.9:
            return HealthStatus.FLOW_999
        elif value >= 0.75:
            return HealthStatus.OPTIMAL
        elif value >= 0.6:
            return HealthStatus.STABLE
        elif value >= 0.4:
            return HealthStatus.ATTENTION
        elif value >= 0.25:
            return HealthStatus.WARNING
        else:
            return HealthStatus.CRITICAL

    def _calculate_trend(self, old: float, new: float) -> TrendDirection:
        """Calculate trend direction"""
        diff = new - old
        if diff > 0.05:
            return TrendDirection.IMPROVING_FAST
        elif diff > 0.02:
            return TrendDirection.IMPROVING
        elif diff < -0.05:
            return TrendDirection.DECLINING_FAST
        elif diff < -0.02:
            return TrendDirection.DECLINING
        else:
            return TrendDirection.STABLE

    # ========================================================================
    # CROSS-DOMAIN ALERTS
    # ========================================================================

    def _check_cross_domain_alerts(
        self,
        updated_domain: DomainType,
        indices: Dict[str, float],
    ) -> None:
        """Check for cross-domain alert conditions"""
        # Example cross-domain rules

        # Rule 1: Transport + Environment correlation
        transport = self._domain_status.get(DomainType.TRANSPORT)
        environment = self._domain_status.get(DomainType.ENVIRONMENT)

        if transport and environment:
            if transport.health_index < 0.4 and environment.health_index < 0.4:
                self._create_cross_domain_alert(
                    domains=[DomainType.TRANSPORT, DomainType.ENVIRONMENT],
                    primary=DomainType.TRANSPORT,
                    title="Transport-Environment Crisis",
                    description="Both transport flow and environmental health are critically low. Systemic intervention needed.",
                    severity="critical",
                    indices={"transport": transport.health_index, "environment": environment.health_index},
                    thresholds={"transport": 0.4, "environment": 0.4},
                )

        # Rule 2: Community + Societal correlation
        community = self._domain_status.get(DomainType.COMMUNITY)
        societal = self._domain_status.get(DomainType.SOCIETAL)

        if community and societal:
            if community.health_index < 0.3:
                self._create_cross_domain_alert(
                    domains=[DomainType.COMMUNITY, DomainType.SOCIETAL],
                    primary=DomainType.COMMUNITY,
                    title="Community Harmony Alert",
                    description="Community harmony is critically low. Societal services should prioritize community support.",
                    severity="high",
                    indices={"community": community.health_index},
                    thresholds={"community": 0.3},
                )

    def _create_cross_domain_alert(
        self,
        domains: List[DomainType],
        primary: DomainType,
        title: str,
        description: str,
        severity: str,
        indices: Dict[str, float],
        thresholds: Dict[str, float],
    ) -> CrossDomainAlert:
        """Create a cross-domain alert"""
        # Check if similar alert already exists
        for alert in self._alerts.values():
            if alert.status == "active" and set(alert.domains) == set(domains):
                return alert  # Don't duplicate

        alert = CrossDomainAlert(
            id=uuid4(),
            alert_type=AlertType.CROSS_DOMAIN if len(domains) > 1 else AlertType.SINGLE_DOMAIN,
            domains=domains,
            primary_domain=primary,
            title=title,
            description=description,
            severity=severity,
            triggering_indices=indices,
            thresholds_crossed=thresholds,
            requires_approval=severity in {"high", "critical"},
        )

        self._alerts[alert.id] = alert

        logger.warning(
            f"CROSS-DOMAIN ALERT: {severity.upper()} - {title} "
            f"(domains: {[d.value for d in domains]})"
        )

        return alert

    def approve_alert_response(
        self,
        alert_id: UUID,
        approver_name: str,
        response_plan: str = "",
    ) -> CrossDomainAlert:
        """
        GOVERNANCE GATE: Approve cross-domain intervention

        RULE #1: Human approval for systemic interventions
        """
        if alert_id not in self._alerts:
            raise ValueError(f"Alert {alert_id} not found")

        alert = self._alerts[alert_id]

        if not alert.requires_approval:
            raise ValueError("Alert does not require approval")

        alert.status = "investigating"
        alert.approved_by = approver_name

        logger.info(f"GOVERNANCE: Cross-domain alert {alert_id} response approved by {approver_name}")

        return alert

    # ========================================================================
    # HEATMAP
    # ========================================================================

    def update_heatmap_cell(
        self,
        zone_id: str,
        zone_name: str,
        latitude: float,
        longitude: float,
        domain_values: Dict[str, float],
    ) -> HeatmapCell:
        """Update a heatmap cell"""
        # Calculate aggregate score
        if domain_values:
            aggregate = sum(domain_values.values()) / len(domain_values)
        else:
            aggregate = 0.5

        status = self._value_to_status(aggregate)
        color = STATUS_COLORS.get(status, "#FFFFFF")

        cell = HeatmapCell(
            zone_id=zone_id,
            zone_name=zone_name,
            latitude=latitude,
            longitude=longitude,
            domain_values=domain_values,
            aggregate_score=aggregate,
            status=status,
            color=color,
        )

        self._heatmap[zone_id] = cell

        return cell

    def get_heatmap(self) -> List[Dict[str, Any]]:
        """Get full heatmap data for visualization"""
        return [
            {
                "zone_id": cell.zone_id,
                "zone_name": cell.zone_name,
                "lat": cell.latitude,
                "lon": cell.longitude,
                "score": round(cell.aggregate_score, 2),
                "status": cell.status.value,
                "color": cell.color,
                "domains": cell.domain_values,
            }
            for cell in self._heatmap.values()
        ]

    # ========================================================================
    # QUERIES
    # ========================================================================

    def get_domain_status(
        self,
        domain: Optional[DomainType] = None,
    ) -> List[DomainStatus]:
        """
        Get domain statuses

        GOVERNANCE RULE #5: Alphabetical by domain name
        """
        if domain:
            status = self._domain_status.get(domain)
            return [status] if status else []

        statuses = list(self._domain_status.values())
        statuses.sort(key=lambda s: s.name.lower())

        return statuses

    def get_global_indices(self) -> Dict[str, GlobalIndex]:
        """Get all global indices"""
        if not self._global_indices:
            self.calculate_global_indices()
        return self._global_indices

    def get_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[CrossDomainAlert]:
        """
        Get alerts

        GOVERNANCE RULE #5: Chronological order
        """
        alerts = list(self._alerts.values())

        if status:
            alerts = [a for a in alerts if a.status == status]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]

        # CHRONOLOGICAL order
        alerts.sort(key=lambda a: a.created_at)

        return alerts

    # ========================================================================
    # METRICS
    # ========================================================================

    def get_system_metrics(self) -> SystemMetrics:
        """Get overall system metrics"""
        now = datetime.now()

        # Calculate global indices first
        self.calculate_global_indices()

        # Domain counts
        statuses = list(self._domain_status.values())
        optimal = sum(1 for s in statuses if s.status in {HealthStatus.OPTIMAL, HealthStatus.FLOW_999})
        stable = sum(1 for s in statuses if s.status == HealthStatus.STABLE)
        attention = sum(1 for s in statuses if s.status == HealthStatus.ATTENTION)
        warning = sum(1 for s in statuses if s.status == HealthStatus.WARNING)
        critical = sum(1 for s in statuses if s.status == HealthStatus.CRITICAL)

        # Alert counts
        alerts = list(self._alerts.values())
        active_alerts = [a for a in alerts if a.status == "active"]
        cross_domain = [a for a in active_alerts if a.alert_type == AlertType.CROSS_DOMAIN]
        pending = sum(s.pending_approvals for s in statuses)

        # Global indices
        indices = self._global_indices
        harmony = indices.get("harmony", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value
        sustainability = indices.get("sustainability", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value
        resilience = indices.get("resilience", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value
        privacy = indices.get("privacy", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value
        atom_freq = indices.get("atom_frequency", GlobalIndex("", 0.5, HealthStatus.STABLE, {}, {}, 0.5, TrendDirection.STABLE, now)).value

        metrics = SystemMetrics(
            timestamp=now,
            domains_optimal=optimal,
            domains_stable=stable,
            domains_attention=attention,
            domains_warning=warning,
            domains_critical=critical,
            total_active_alerts=len(active_alerts),
            cross_domain_alerts=len(cross_domain),
            pending_approvals=pending,
            global_harmony_index=harmony,
            global_sustainability_index=sustainability,
            global_resilience_index=resilience,
            global_privacy_index=privacy,
            atom_frequency=atom_freq,
        )

        self._metrics_history.append(metrics)

        return metrics

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get complete dashboard summary for UI"""
        metrics = self.get_system_metrics()

        return {
            "timestamp": metrics.timestamp.isoformat(),

            # AT·OM Frequency (Master Index)
            "atom_frequency": {
                "value": round(metrics.atom_frequency, 3),
                "status": "FLOW_999" if metrics.atom_frequency >= 0.9 else "normal",
                "color": STATUS_COLORS[HealthStatus.FLOW_999] if metrics.atom_frequency >= 0.9 else STATUS_COLORS[self._value_to_status(metrics.atom_frequency)],
            },

            # Domain health
            "domains": {
                "optimal": metrics.domains_optimal,
                "stable": metrics.domains_stable,
                "attention": metrics.domains_attention,
                "warning": metrics.domains_warning,
                "critical": metrics.domains_critical,
                "total": sum([
                    metrics.domains_optimal,
                    metrics.domains_stable,
                    metrics.domains_attention,
                    metrics.domains_warning,
                    metrics.domains_critical,
                ]),
            },

            # Global indices
            "indices": {
                "harmony": round(metrics.global_harmony_index, 3),
                "sustainability": round(metrics.global_sustainability_index, 3),
                "resilience": round(metrics.global_resilience_index, 3),
                "privacy": round(metrics.global_privacy_index, 3),
            },

            # Alerts
            "alerts": {
                "active": metrics.total_active_alerts,
                "cross_domain": metrics.cross_domain_alerts,
                "pending_approvals": metrics.pending_approvals,
            },

            # Status message
            "status_message": self._generate_status_message(metrics),
        }

    def _generate_status_message(self, metrics: SystemMetrics) -> str:
        """Generate human-readable status message"""
        if metrics.atom_frequency >= 0.9:
            return "🔵 AT·OM Frequency 999Hz - Systeme en harmonie parfaite"
        elif metrics.atom_frequency >= 0.75:
            return "🟢 Systeme optimal - Flux equilibres"
        elif metrics.atom_frequency >= 0.6:
            return "🟢 Systeme stable - Fonctionnement normal"
        elif metrics.atom_frequency >= 0.4:
            return "🟡 Attention requise - Certains domaines necessitent surveillance"
        elif metrics.atom_frequency >= 0.25:
            return "🟠 Alerte - Interventions recommandees"
        else:
            return "🔴 Critique - Intervention immediate requise"


# ============================================================================
# SINGLETON ACCESSOR
# ============================================================================

def get_master_dashboard_agent() -> MasterDashboardAgent:
    """Get the singleton MasterDashboardAgent instance"""
    return MasterDashboardAgent()
