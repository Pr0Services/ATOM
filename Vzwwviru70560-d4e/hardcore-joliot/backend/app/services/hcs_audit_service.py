"""
HCS Audit Service - Immutable Logging via Hedera Consensus Service

This service provides structured, immutable audit logging for all
sovereign system operations. Every significant action is recorded
on Hedera's distributed ledger for permanent transparency.

Log Categories:
- ECONOMIC: Token operations, conversions, disbursements
- GOVERNANCE: Votes, proposals, sovereignty changes
- SECURITY: Sentinel alerts, threat responses
- ACCESS: Module unlocks, sacred knowledge access
- OPERATIONAL: Forge activities, project milestones

Author: AT·OM Collective
Version: 1.0.0
"""

import os
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from decimal import Decimal
from enum import Enum
from dataclasses import dataclass, asdict, field
import asyncio

from app.services.hedera_service import get_hedera_service

logger = logging.getLogger(__name__)


# ==================== ENUMS & TYPES ====================

class AuditCategory(Enum):
    """Categories of audit events"""
    ECONOMIC = "ECONOMIC"
    GOVERNANCE = "GOVERNANCE"
    SECURITY = "SECURITY"
    ACCESS = "ACCESS"
    OPERATIONAL = "OPERATIONAL"
    SYSTEM = "SYSTEM"


class AuditSeverity(Enum):
    """Severity levels for audit events"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


@dataclass
class AuditEntry:
    """Structure for an audit log entry"""
    category: AuditCategory
    severity: AuditSeverity
    action: str
    actor_id: str
    timestamp: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    hedera_tx_id: Optional[str] = None
    hcs_sequence: Optional[int] = None
    signature: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.correlation_id is None:
            self.correlation_id = self._generate_correlation_id()

    def _generate_correlation_id(self) -> str:
        """Generate unique correlation ID"""
        content = f"{self.category.value}:{self.action}:{self.actor_id}:{self.timestamp.isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_hcs_message(self) -> Dict[str, Any]:
        """Convert to HCS message format"""
        return {
            'v': '1.0',  # Schema version
            'cat': self.category.value,
            'sev': self.severity.value,
            'act': self.action,
            'uid': self.actor_id,
            'ts': self.timestamp.isoformat(),
            'cid': self.correlation_id,
            'data': self.data,
            'sig': self.signature
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'category': self.category.value,
            'severity': self.severity.value,
            'action': self.action,
            'actor_id': self.actor_id,
            'timestamp': self.timestamp.isoformat(),
            'correlation_id': self.correlation_id,
            'data': self.data,
            'hedera_tx_id': self.hedera_tx_id,
            'hcs_sequence': self.hcs_sequence
        }


# ==================== AUDIT SERVICE ====================

class HCSAuditService:
    """
    Immutable audit logging service using Hedera Consensus Service.

    Features:
    - Structured log categories
    - Severity-based routing
    - Batch submission for efficiency
    - Local fallback when HCS unavailable
    - Query interface for audit history
    """

    def __init__(self):
        self.hedera = get_hedera_service()
        self._batch_queue: List[AuditEntry] = []
        self._batch_size = 10
        self._batch_timeout = 5.0  # seconds
        self._batch_task: Optional[asyncio.Task] = None
        self._local_buffer: List[AuditEntry] = []
        self._max_local_buffer = 1000

    async def initialize(self):
        """Initialize the audit service"""
        await self.hedera.initialize()

        # Start batch processing task
        if self._batch_task is None or self._batch_task.done():
            self._batch_task = asyncio.create_task(self._batch_processor())

    async def close(self):
        """Close the audit service and flush remaining entries"""
        if self._batch_task:
            self._batch_task.cancel()

        # Flush remaining entries
        await self._flush_batch()

    # ==================== LOGGING METHODS ====================

    async def log(
        self,
        category: AuditCategory,
        action: str,
        actor_id: str,
        data: Dict[str, Any],
        severity: AuditSeverity = AuditSeverity.INFO,
        immediate: bool = False
    ) -> AuditEntry:
        """
        Log an audit entry.

        Args:
            category: Event category
            action: Action identifier
            actor_id: User/system ID performing the action
            data: Additional event data
            severity: Event severity level
            immediate: If True, submit immediately to HCS

        Returns:
            The created audit entry
        """
        entry = AuditEntry(
            category=category,
            severity=severity,
            action=action,
            actor_id=actor_id,
            timestamp=datetime.utcnow(),
            data=data
        )

        if immediate or severity in [AuditSeverity.CRITICAL, AuditSeverity.EMERGENCY]:
            await self._submit_entry(entry)
        else:
            self._batch_queue.append(entry)

        return entry

    # ==================== CATEGORY-SPECIFIC METHODS ====================

    async def log_economic(
        self,
        action: str,
        actor_id: str,
        amount: Optional[Decimal] = None,
        currency: str = 'UR',
        from_account: Optional[str] = None,
        to_account: Optional[str] = None,
        tx_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> AuditEntry:
        """Log an economic event (token operations, conversions)"""
        data = {
            'currency': currency
        }
        if amount is not None:
            data['amount'] = str(amount)
        if from_account:
            data['from'] = from_account
        if to_account:
            data['to'] = to_account
        if tx_id:
            data['tx_id'] = tx_id
        if metadata:
            data['meta'] = metadata

        return await self.log(
            category=AuditCategory.ECONOMIC,
            action=action,
            actor_id=actor_id,
            data=data
        )

    async def log_governance(
        self,
        action: str,
        actor_id: str,
        proposal_id: Optional[str] = None,
        vote: Optional[str] = None,
        result: Optional[str] = None,
        sovereignty_change: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> AuditEntry:
        """Log a governance event (votes, proposals, sovereignty changes)"""
        data = {}
        if proposal_id:
            data['proposal_id'] = proposal_id
        if vote:
            data['vote'] = vote
        if result:
            data['result'] = result
        if sovereignty_change:
            data['sovereignty'] = sovereignty_change
        if metadata:
            data['meta'] = metadata

        severity = AuditSeverity.INFO
        if action in ['SOVEREIGNTY_PROMOTED', 'PROPOSAL_EXECUTED', 'EMERGENCY_VOTE']:
            severity = AuditSeverity.WARNING

        return await self.log(
            category=AuditCategory.GOVERNANCE,
            action=action,
            actor_id=actor_id,
            data=data,
            severity=severity
        )

    async def log_security(
        self,
        action: str,
        actor_id: str,
        threat_id: Optional[str] = None,
        threat_level: Optional[str] = None,
        response: Optional[str] = None,
        coordinates: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        severity: AuditSeverity = AuditSeverity.WARNING
    ) -> AuditEntry:
        """Log a security event (Sentinel alerts, threat responses)"""
        data = {}
        if threat_id:
            data['threat_id'] = threat_id
        if threat_level:
            data['threat_level'] = threat_level
        if response:
            data['response'] = response
        if coordinates:
            data['coordinates'] = coordinates
        if metadata:
            data['meta'] = metadata

        # Escalate severity for high threat levels
        if threat_level in ['RED', 'BLACK']:
            severity = AuditSeverity.CRITICAL

        return await self.log(
            category=AuditCategory.SECURITY,
            action=action,
            actor_id=actor_id,
            data=data,
            severity=severity,
            immediate=(severity == AuditSeverity.CRITICAL)
        )

    async def log_access(
        self,
        action: str,
        actor_id: str,
        resource_type: str,
        resource_id: str,
        granted: bool,
        reason: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> AuditEntry:
        """Log an access event (module unlocks, sacred knowledge access)"""
        data = {
            'resource_type': resource_type,
            'resource_id': resource_id,
            'granted': granted
        }
        if reason:
            data['reason'] = reason
        if metadata:
            data['meta'] = metadata

        severity = AuditSeverity.INFO
        if resource_type == 'sacred_knowledge':
            severity = AuditSeverity.WARNING

        return await self.log(
            category=AuditCategory.ACCESS,
            action=action,
            actor_id=actor_id,
            data=data,
            severity=severity
        )

    async def log_operational(
        self,
        action: str,
        actor_id: str,
        project_id: Optional[str] = None,
        role_id: Optional[str] = None,
        milestone: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> AuditEntry:
        """Log an operational event (Forge activities, milestones)"""
        data = {}
        if project_id:
            data['project_id'] = project_id
        if role_id:
            data['role_id'] = role_id
        if milestone:
            data['milestone'] = milestone
        if metadata:
            data['meta'] = metadata

        return await self.log(
            category=AuditCategory.OPERATIONAL,
            action=action,
            actor_id=actor_id,
            data=data
        )

    async def log_system(
        self,
        action: str,
        component: str,
        status: str,
        metadata: Optional[Dict] = None,
        severity: AuditSeverity = AuditSeverity.INFO
    ) -> AuditEntry:
        """Log a system event (service status, errors)"""
        data = {
            'component': component,
            'status': status
        }
        if metadata:
            data['meta'] = metadata

        return await self.log(
            category=AuditCategory.SYSTEM,
            action=action,
            actor_id='SYSTEM',
            data=data,
            severity=severity
        )

    # ==================== BATCH PROCESSING ====================

    async def _batch_processor(self):
        """Background task to process batched audit entries"""
        while True:
            try:
                await asyncio.sleep(self._batch_timeout)
                await self._flush_batch()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Batch processor error: {e}")

    async def _flush_batch(self):
        """Flush pending batch entries to HCS"""
        if not self._batch_queue:
            return

        # Get entries to process
        entries = self._batch_queue[:self._batch_size]
        self._batch_queue = self._batch_queue[self._batch_size:]

        # Submit batch
        for entry in entries:
            await self._submit_entry(entry)

    async def _submit_entry(self, entry: AuditEntry) -> bool:
        """Submit a single entry to HCS"""
        try:
            message = entry.to_hcs_message()
            success = await self.hedera._log_to_hcs(message)

            if success:
                logger.debug(f"Audit logged to HCS: {entry.action}")
            else:
                # Store locally if HCS fails
                self._store_local(entry)

            return success

        except Exception as e:
            logger.error(f"Failed to submit audit entry: {e}")
            self._store_local(entry)
            return False

    def _store_local(self, entry: AuditEntry):
        """Store entry in local buffer when HCS unavailable"""
        if len(self._local_buffer) >= self._max_local_buffer:
            self._local_buffer.pop(0)  # Remove oldest
        self._local_buffer.append(entry)

    # ==================== QUERY METHODS ====================

    async def get_entries_by_actor(
        self,
        actor_id: str,
        category: Optional[AuditCategory] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Query audit entries by actor.

        Note: In production, this would query the HCS mirror node
        or a local index. For now, returns from local buffer.
        """
        results = []
        for entry in reversed(self._local_buffer):
            if entry.actor_id != actor_id:
                continue
            if category and entry.category != category:
                continue
            if since and entry.timestamp < since:
                continue
            results.append(entry.to_dict())
            if len(results) >= limit:
                break
        return results

    async def get_entries_by_category(
        self,
        category: AuditCategory,
        severity: Optional[AuditSeverity] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Query audit entries by category"""
        results = []
        for entry in reversed(self._local_buffer):
            if entry.category != category:
                continue
            if severity and entry.severity != severity:
                continue
            if since and entry.timestamp < since:
                continue
            results.append(entry.to_dict())
            if len(results) >= limit:
                break
        return results

    async def get_security_alerts(
        self,
        min_severity: AuditSeverity = AuditSeverity.WARNING,
        since: Optional[datetime] = None
    ) -> List[Dict]:
        """Get security alerts above a severity threshold"""
        severity_order = [
            AuditSeverity.INFO,
            AuditSeverity.WARNING,
            AuditSeverity.CRITICAL,
            AuditSeverity.EMERGENCY
        ]
        min_index = severity_order.index(min_severity)

        results = []
        for entry in reversed(self._local_buffer):
            if entry.category != AuditCategory.SECURITY:
                continue
            if severity_order.index(entry.severity) < min_index:
                continue
            if since and entry.timestamp < since:
                continue
            results.append(entry.to_dict())
        return results

    async def get_audit_summary(
        self,
        since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get summary statistics of audit entries"""
        if since is None:
            since = datetime.utcnow() - timedelta(hours=24)

        summary = {
            'period_start': since.isoformat(),
            'period_end': datetime.utcnow().isoformat(),
            'total_entries': 0,
            'by_category': {},
            'by_severity': {},
            'unique_actors': set(),
            'hcs_submitted': 0,
            'local_only': 0
        }

        for entry in self._local_buffer:
            if entry.timestamp < since:
                continue

            summary['total_entries'] += 1
            summary['unique_actors'].add(entry.actor_id)

            cat = entry.category.value
            summary['by_category'][cat] = summary['by_category'].get(cat, 0) + 1

            sev = entry.severity.value
            summary['by_severity'][sev] = summary['by_severity'].get(sev, 0) + 1

            if entry.hcs_sequence:
                summary['hcs_submitted'] += 1
            else:
                summary['local_only'] += 1

        summary['unique_actors'] = len(summary['unique_actors'])
        return summary


# ==================== SINGLETON INSTANCE ====================

_audit_service: Optional[HCSAuditService] = None


def get_audit_service() -> HCSAuditService:
    """Get or create the singleton audit service instance"""
    global _audit_service
    if _audit_service is None:
        _audit_service = HCSAuditService()
    return _audit_service


async def initialize_audit() -> None:
    """Initialize the audit service"""
    service = get_audit_service()
    await service.initialize()


# ==================== CONVENIENCE FUNCTIONS ====================

async def audit_economic(action: str, actor_id: str, **kwargs) -> AuditEntry:
    """Convenience function for economic audit logging"""
    return await get_audit_service().log_economic(action, actor_id, **kwargs)


async def audit_governance(action: str, actor_id: str, **kwargs) -> AuditEntry:
    """Convenience function for governance audit logging"""
    return await get_audit_service().log_governance(action, actor_id, **kwargs)


async def audit_security(action: str, actor_id: str, **kwargs) -> AuditEntry:
    """Convenience function for security audit logging"""
    return await get_audit_service().log_security(action, actor_id, **kwargs)


async def audit_access(action: str, actor_id: str, **kwargs) -> AuditEntry:
    """Convenience function for access audit logging"""
    return await get_audit_service().log_access(action, actor_id, **kwargs)


async def audit_operational(action: str, actor_id: str, **kwargs) -> AuditEntry:
    """Convenience function for operational audit logging"""
    return await get_audit_service().log_operational(action, actor_id, **kwargs)
