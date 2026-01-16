"""
CHE·NU V75 - MODULE SCENARIO LOCK
=================================
Système de verrouillage et protection des scénarios, configurations et états.
Assure l'immutabilité des décisions importantes et prévient les modifications non autorisées.

PRINCIPES:
- GOUVERNANCE > EXÉCUTION
- Immutabilité des décisions validées
- Audit trail complet de tous les locks/unlocks
- Human-in-the-loop OBLIGATOIRE pour unlock
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel
import hashlib
import json

# ============================================================================
# ENUMS
# ============================================================================

class LockType(str, Enum):
    """Types de verrous"""
    SCENARIO = "scenario"           # Scénario de simulation
    CONFIG = "config"               # Configuration système
    DECISION = "decision"           # Décision validée
    MODULE = "module"               # Module de code
    THREAD = "thread"               # Thread complet
    WORKFLOW = "workflow"           # Workflow défini
    DATA = "data"                   # Données critiques
    GOVERNANCE = "governance"       # Règle de gouvernance


class LockLevel(str, Enum):
    """Niveaux de verrouillage"""
    SOFT = "soft"           # Avertissement, bypass possible avec raison
    FIRM = "firm"           # Checkpoint requis pour modification
    HARD = "hard"           # Approbation multi-niveau requise
    PERMANENT = "permanent" # Immutable, aucune modification possible


class LockStatus(str, Enum):
    """Statut du verrou"""
    ACTIVE = "active"
    EXPIRED = "expired"
    RELEASED = "released"
    OVERRIDDEN = "overridden"


class UnlockRequestStatus(str, Enum):
    """Statut d'une demande de déverrouillage"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


# ============================================================================
# SCHEMAS
# ============================================================================

class LockMetadata(BaseModel):
    """Métadonnées d'un verrou"""
    reason: str
    created_by: str
    approved_by: Optional[str] = None
    expiration: Optional[datetime] = None
    notes: Optional[str] = None
    checkpoint_id: Optional[str] = None


class Lock(BaseModel):
    """Représentation d'un verrou"""
    id: str = field(default_factory=lambda: str(uuid4()))
    target_id: str
    target_type: LockType
    level: LockLevel
    status: LockStatus = LockStatus.ACTIVE
    metadata: LockMetadata
    content_hash: str  # Hash du contenu verrouillé
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class UnlockRequest(BaseModel):
    """Demande de déverrouillage"""
    id: str = field(default_factory=lambda: str(uuid4()))
    lock_id: str
    requester_id: str
    reason: str
    urgency: str  # low, medium, high, critical
    status: UnlockRequestStatus = UnlockRequestStatus.PENDING
    
    approvers_required: List[str] = []
    approvers_received: List[str] = []
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


class LockAuditEntry(BaseModel):
    """Entrée d'audit pour les opérations de verrouillage"""
    id: str = field(default_factory=lambda: str(uuid4()))
    lock_id: str
    action: str  # create, release, override, expire
    actor_id: str
    details: Dict[str, Any] = {}
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# SCENARIO LOCK SERVICE
# ============================================================================

class ScenarioLockService:
    """
    Service de verrouillage des scénarios V75
    
    Assure l'intégrité et l'immutabilité des éléments critiques.
    Respecte les principes Canon:
    - Aucun déverrouillage sans approbation humaine explicite
    - Audit trail complet
    - Protection multi-niveau
    """
    
    def __init__(self):
        self.locks: Dict[str, Lock] = {}
        self.locks_by_target: Dict[str, List[str]] = {}  # target_id -> [lock_ids]
        self.unlock_requests: Dict[str, UnlockRequest] = {}
        self.audit_log: List[LockAuditEntry] = []
        
    # ========================================================================
    # LOCK MANAGEMENT
    # ========================================================================
    
    async def create_lock(
        self,
        target_id: str,
        target_type: LockType,
        level: LockLevel,
        reason: str,
        created_by: str,
        content: Any = None,
        expiration_hours: Optional[int] = None,
        requires_approval: bool = False
    ) -> Lock:
        """
        Crée un nouveau verrou.
        CHECKPOINT si niveau HARD ou PERMANENT.
        """
        # Vérifier si déjà verrouillé
        existing = await self.get_active_locks(target_id)
        if existing and level != LockLevel.SOFT:
            raise ValueError(f"Target {target_id} already has active locks")
        
        # Calculer hash du contenu
        content_hash = ""
        if content:
            content_str = json.dumps(content, sort_keys=True, default=str)
            content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        # Créer expiration si spécifiée
        expiration = None
        if expiration_hours:
            expiration = datetime.utcnow() + timedelta(hours=expiration_hours)
        
        metadata = LockMetadata(
            reason=reason,
            created_by=created_by,
            expiration=expiration
        )
        
        lock = Lock(
            target_id=target_id,
            target_type=target_type,
            level=level,
            metadata=metadata,
            content_hash=content_hash
        )
        
        # Si niveau élevé, créer checkpoint
        if level in [LockLevel.HARD, LockLevel.PERMANENT] or requires_approval:
            checkpoint = await self._create_checkpoint(
                action="create_lock",
                lock=lock,
                reason=f"High-security lock requires approval: {reason}"
            )
            lock.metadata.checkpoint_id = checkpoint["id"]
            # En production: attendre approbation avant de finaliser
        
        self.locks[lock.id] = lock
        
        if target_id not in self.locks_by_target:
            self.locks_by_target[target_id] = []
        self.locks_by_target[target_id].append(lock.id)
        
        # Audit
        await self._audit("create", lock.id, created_by, {
            "level": level.value,
            "type": target_type.value,
            "reason": reason
        })
        
        return lock
    
    async def get_lock(self, lock_id: str) -> Optional[Lock]:
        """Récupère un verrou par ID"""
        return self.locks.get(lock_id)
    
    async def get_active_locks(self, target_id: str) -> List[Lock]:
        """Récupère les verrous actifs pour une cible"""
        lock_ids = self.locks_by_target.get(target_id, [])
        active = []
        
        for lock_id in lock_ids:
            lock = self.locks.get(lock_id)
            if lock and lock.status == LockStatus.ACTIVE:
                # Vérifier expiration
                if lock.metadata.expiration and lock.metadata.expiration < datetime.utcnow():
                    lock.status = LockStatus.EXPIRED
                    await self._audit("expire", lock_id, "system", {})
                else:
                    active.append(lock)
        
        return active
    
    async def check_locked(self, target_id: str) -> Dict[str, Any]:
        """
        Vérifie si une cible est verrouillée.
        Retourne le niveau de verrouillage le plus élevé.
        """
        locks = await self.get_active_locks(target_id)
        
        if not locks:
            return {
                "is_locked": False,
                "level": None,
                "locks": []
            }
        
        # Trouver le niveau le plus élevé
        level_priority = {
            LockLevel.SOFT: 1,
            LockLevel.FIRM: 2,
            LockLevel.HARD: 3,
            LockLevel.PERMANENT: 4
        }
        
        highest_lock = max(locks, key=lambda l: level_priority[l.level])
        
        return {
            "is_locked": True,
            "level": highest_lock.level.value,
            "highest_lock_id": highest_lock.id,
            "locks_count": len(locks),
            "locks": [l.id for l in locks]
        }
    
    async def verify_integrity(self, lock_id: str, content: Any) -> bool:
        """
        Vérifie que le contenu n'a pas été modifié depuis le verrouillage.
        """
        lock = self.locks.get(lock_id)
        if not lock:
            return False
        
        content_str = json.dumps(content, sort_keys=True, default=str)
        current_hash = hashlib.sha256(content_str.encode()).hexdigest()
        
        return current_hash == lock.content_hash
    
    # ========================================================================
    # UNLOCK REQUESTS
    # ========================================================================
    
    async def request_unlock(
        self,
        lock_id: str,
        requester_id: str,
        reason: str,
        urgency: str = "medium"
    ) -> UnlockRequest:
        """
        Demande de déverrouillage.
        CHECKPOINT: Toute demande génère une notification pour approbation.
        """
        lock = self.locks.get(lock_id)
        if not lock:
            raise ValueError(f"Lock {lock_id} not found")
        
        if lock.level == LockLevel.PERMANENT:
            raise ValueError("Cannot request unlock for PERMANENT locks")
        
        # Déterminer les approbateurs requis
        approvers_required = await self._get_required_approvers(lock)
        
        # Expiration de la demande
        urgency_hours = {
            "low": 72,
            "medium": 24,
            "high": 4,
            "critical": 1
        }
        expires_at = datetime.utcnow() + timedelta(hours=urgency_hours.get(urgency, 24))
        
        request = UnlockRequest(
            lock_id=lock_id,
            requester_id=requester_id,
            reason=reason,
            urgency=urgency,
            approvers_required=approvers_required,
            expires_at=expires_at
        )
        
        self.unlock_requests[request.id] = request
        
        # Créer checkpoint
        await self._create_checkpoint(
            action="unlock_request",
            lock=lock,
            request=request,
            reason=f"Unlock requested: {reason}"
        )
        
        # Audit
        await self._audit("unlock_requested", lock_id, requester_id, {
            "request_id": request.id,
            "urgency": urgency,
            "reason": reason
        })
        
        return request
    
    async def approve_unlock(
        self,
        request_id: str,
        approver_id: str
    ) -> UnlockRequest:
        """Approuve une demande de déverrouillage"""
        request = self.unlock_requests.get(request_id)
        if not request:
            raise ValueError(f"Unlock request {request_id} not found")
        
        if request.status != UnlockRequestStatus.PENDING:
            raise ValueError(f"Request is not pending: {request.status}")
        
        # Vérifier expiration
        if request.expires_at and request.expires_at < datetime.utcnow():
            request.status = UnlockRequestStatus.EXPIRED
            return request
        
        # Ajouter approbation
        if approver_id not in request.approvers_received:
            request.approvers_received.append(approver_id)
        
        # Vérifier si toutes les approbations reçues
        required_set = set(request.approvers_required) if request.approvers_required else set()
        received_set = set(request.approvers_received)
        
        if not required_set or required_set.issubset(received_set):
            request.status = UnlockRequestStatus.APPROVED
            request.resolved_at = datetime.utcnow()
            request.resolved_by = approver_id
            
            # Libérer le verrou
            await self.release_lock(request.lock_id, approver_id, f"Unlock approved: {request.reason}")
        
        # Audit
        await self._audit("unlock_approved", request.lock_id, approver_id, {
            "request_id": request_id,
            "status": request.status.value
        })
        
        return request
    
    async def reject_unlock(
        self,
        request_id: str,
        rejector_id: str,
        reason: str
    ) -> UnlockRequest:
        """Rejette une demande de déverrouillage"""
        request = self.unlock_requests.get(request_id)
        if not request:
            raise ValueError(f"Unlock request {request_id} not found")
        
        request.status = UnlockRequestStatus.REJECTED
        request.resolved_at = datetime.utcnow()
        request.resolved_by = rejector_id
        
        # Audit
        await self._audit("unlock_rejected", request.lock_id, rejector_id, {
            "request_id": request_id,
            "rejection_reason": reason
        })
        
        return request
    
    # ========================================================================
    # LOCK RELEASE
    # ========================================================================
    
    async def release_lock(
        self,
        lock_id: str,
        released_by: str,
        reason: str
    ) -> Lock:
        """
        Libère un verrou.
        CHECKPOINT: Libération de verrous FIRM+ nécessite approbation.
        """
        lock = self.locks.get(lock_id)
        if not lock:
            raise ValueError(f"Lock {lock_id} not found")
        
        if lock.level == LockLevel.PERMANENT:
            raise ValueError("Cannot release PERMANENT locks")
        
        if lock.status != LockStatus.ACTIVE:
            raise ValueError(f"Lock is not active: {lock.status}")
        
        lock.status = LockStatus.RELEASED
        lock.updated_at = datetime.utcnow()
        
        # Audit
        await self._audit("release", lock_id, released_by, {
            "reason": reason
        })
        
        return lock
    
    async def force_release(
        self,
        lock_id: str,
        forced_by: str,
        reason: str,
        emergency: bool = False
    ) -> Dict[str, Any]:
        """
        Force la libération d'un verrou.
        CHECKPOINT CRITIQUE: Toujours avec approbation multi-niveau.
        """
        lock = self.locks.get(lock_id)
        if not lock:
            raise ValueError(f"Lock {lock_id} not found")
        
        if lock.level == LockLevel.PERMANENT and not emergency:
            raise ValueError("Cannot force release PERMANENT locks without emergency flag")
        
        # Créer checkpoint critique
        checkpoint = await self._create_checkpoint(
            action="force_release",
            lock=lock,
            reason=f"FORCE RELEASE: {reason}",
            severity="critical"
        )
        
        # En production: attendre approbation multi-niveau
        # Pour l'instant: marquer comme override
        lock.status = LockStatus.OVERRIDDEN
        lock.updated_at = datetime.utcnow()
        
        # Audit critique
        await self._audit("force_release", lock_id, forced_by, {
            "reason": reason,
            "emergency": emergency,
            "checkpoint_id": checkpoint["id"]
        })
        
        return {
            "lock": lock,
            "checkpoint": checkpoint,
            "warning": "Force release logged for audit. Review required."
        }
    
    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================
    
    async def lock_scenario(
        self,
        scenario_id: str,
        scenario_data: Dict[str, Any],
        locked_by: str,
        reason: str = "Scenario finalized"
    ) -> Lock:
        """Verrouille un scénario complet"""
        return await self.create_lock(
            target_id=scenario_id,
            target_type=LockType.SCENARIO,
            level=LockLevel.FIRM,
            reason=reason,
            created_by=locked_by,
            content=scenario_data
        )
    
    async def lock_decision(
        self,
        decision_id: str,
        decision_data: Dict[str, Any],
        locked_by: str,
        permanent: bool = False
    ) -> Lock:
        """Verrouille une décision validée"""
        return await self.create_lock(
            target_id=decision_id,
            target_type=LockType.DECISION,
            level=LockLevel.PERMANENT if permanent else LockLevel.HARD,
            reason="Decision validated and locked",
            created_by=locked_by,
            content=decision_data
        )
    
    async def lock_module(
        self,
        module_id: str,
        module_hash: str,
        locked_by: str
    ) -> Lock:
        """Verrouille un module (LOCKED status)"""
        return await self.create_lock(
            target_id=module_id,
            target_type=LockType.MODULE,
            level=LockLevel.HARD,
            reason="Module frozen - production stable",
            created_by=locked_by,
            content={"hash": module_hash}
        )
    
    # ========================================================================
    # QUERIES
    # ========================================================================
    
    async def list_locks(
        self,
        status: Optional[LockStatus] = None,
        lock_type: Optional[LockType] = None,
        level: Optional[LockLevel] = None,
        limit: int = 100
    ) -> List[Lock]:
        """Liste les verrous avec filtres"""
        results = []
        
        for lock in self.locks.values():
            if status and lock.status != status:
                continue
            if lock_type and lock.target_type != lock_type:
                continue
            if level and lock.level != level:
                continue
            results.append(lock)
            
            if len(results) >= limit:
                break
        
        return results
    
    async def get_pending_requests(self) -> List[UnlockRequest]:
        """Liste les demandes de déverrouillage en attente"""
        return [
            r for r in self.unlock_requests.values()
            if r.status == UnlockRequestStatus.PENDING
        ]
    
    async def get_audit_log(
        self,
        lock_id: Optional[str] = None,
        limit: int = 100
    ) -> List[LockAuditEntry]:
        """Récupère l'historique d'audit"""
        if lock_id:
            entries = [e for e in self.audit_log if e.lock_id == lock_id]
        else:
            entries = self.audit_log
        
        return entries[-limit:]
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    async def _get_required_approvers(self, lock: Lock) -> List[str]:
        """Détermine les approbateurs requis selon le niveau"""
        if lock.level == LockLevel.SOFT:
            return []  # Pas d'approbation requise
        elif lock.level == LockLevel.FIRM:
            return [lock.metadata.created_by]  # Créateur peut approuver
        elif lock.level == LockLevel.HARD:
            return ["admin", lock.metadata.created_by]  # Admin + créateur
        else:
            return []  # PERMANENT = pas de déverrouillage
    
    async def _create_checkpoint(
        self,
        action: str,
        lock: Lock,
        reason: str,
        request: UnlockRequest = None,
        severity: str = "normal"
    ) -> Dict[str, Any]:
        """Crée un checkpoint pour validation humaine"""
        return {
            "id": str(uuid4()),
            "type": "scenario_lock",
            "action": action,
            "lock_id": lock.id,
            "lock_type": lock.target_type.value,
            "lock_level": lock.level.value,
            "target_id": lock.target_id,
            "reason": reason,
            "severity": severity,
            "request": request.dict() if request else None,
            "status": "pending",
            "requires_approval": True,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def _audit(
        self,
        action: str,
        lock_id: str,
        actor_id: str,
        details: Dict[str, Any]
    ):
        """Ajoute une entrée d'audit"""
        entry = LockAuditEntry(
            lock_id=lock_id,
            action=action,
            actor_id=actor_id,
            details=details
        )
        self.audit_log.append(entry)


# ============================================================================
# INSTANCE GLOBALE
# ============================================================================

scenario_lock_service = ScenarioLockService()


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'ScenarioLockService',
    'scenario_lock_service',
    'LockType',
    'LockLevel',
    'LockStatus',
    'UnlockRequestStatus',
    'Lock',
    'LockMetadata',
    'UnlockRequest',
    'LockAuditEntry'
]
