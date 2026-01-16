"""
CHE·NU™ — Quantum Orchestrator
==============================
Extension of Module 22 (Orchestration) that routes computation to:
- Classical compute (default, always available)
- Photonic acceleration (when available)
- Quantum compute (rare, high-security only)

Core Principle: User NEVER asks for quantum.
The system uses it ONLY when necessary, invisibly.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable, Awaitable
from enum import Enum
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import asyncio
import logging
import random

logger = logging.getLogger(__name__)


class ComputeType(str, Enum):
    """Types of computation available"""
    CLASSICAL = "classical"       # Standard CPU/GPU
    PHOTONIC = "photonic"        # Silicon photonics acceleration
    QUANTUM = "quantum"          # Quantum computer (rare)
    HYBRID = "hybrid"            # Mix of above


class ComputePriority(str, Enum):
    """Priority levels for compute routing"""
    SECURITY = "security"        # Highest - cryptographic operations
    SURVIVAL = "survival"        # Emergency/safety critical
    PRODUCTION = "production"    # Normal business operations
    BACKGROUND = "background"    # Low priority batch jobs


class HubIntegration(str, Enum):
    """Hubs that quantum orchestrator integrates with"""
    COMMUNICATION = "communication"  # QKD encryption
    NAVIGATION = "navigation"        # Sensor synchronization
    EXECUTION = "execution"          # Compute acceleration


@dataclass
class ComputeCapability:
    """Capability of a compute resource"""
    compute_type: ComputeType
    is_available: bool = True
    latency_ms: float = 10.0
    throughput_ops: int = 1000
    current_load: float = 0.0  # 0-1
    error_rate: float = 0.001
    cost_per_op: float = 0.001
    
    # Quantum-specific
    qubit_count: int = 0
    coherence_time_us: float = 0
    
    # Photonic-specific
    wavelength_nm: int = 0
    bandwidth_ghz: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "compute_type": self.compute_type.value,
            "is_available": self.is_available,
            "latency_ms": self.latency_ms,
            "throughput_ops": self.throughput_ops,
            "current_load": self.current_load,
            "error_rate": self.error_rate,
            "cost_per_op": self.cost_per_op,
            "qubit_count": self.qubit_count,
            "coherence_time_us": self.coherence_time_us,
            "wavelength_nm": self.wavelength_nm,
            "bandwidth_ghz": self.bandwidth_ghz
        }


@dataclass
class ComputeRequest:
    """Request for computation"""
    request_id: UUID = field(default_factory=uuid4)
    operation: str = ""
    priority: ComputePriority = ComputePriority.PRODUCTION
    hub_target: Optional[HubIntegration] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # Requirements
    requires_encryption: bool = False
    requires_low_latency: bool = False
    requires_high_throughput: bool = False
    max_error_rate: float = 0.01
    max_cost: float = 1.0
    timeout_ms: int = 5000
    
    # User/context
    user_id: str = ""
    context_id: Optional[UUID] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": str(self.request_id),
            "operation": self.operation,
            "priority": self.priority.value,
            "hub_target": self.hub_target.value if self.hub_target else None,
            "requires_encryption": self.requires_encryption,
            "requires_low_latency": self.requires_low_latency,
            "requires_high_throughput": self.requires_high_throughput,
            "max_error_rate": self.max_error_rate,
            "max_cost": self.max_cost,
            "timeout_ms": self.timeout_ms,
            "user_id": self.user_id
        }


@dataclass
class RoutingDecision:
    """Decision made by quantum orchestrator"""
    decision_id: UUID = field(default_factory=uuid4)
    request_id: UUID = None
    selected_compute: ComputeType = ComputeType.CLASSICAL
    reason: str = ""
    fallback_chain: List[ComputeType] = field(default_factory=list)
    estimated_latency_ms: float = 0
    estimated_cost: float = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": str(self.decision_id),
            "request_id": str(self.request_id) if self.request_id else None,
            "selected_compute": self.selected_compute.value,
            "reason": self.reason,
            "fallback_chain": [c.value for c in self.fallback_chain],
            "estimated_latency_ms": self.estimated_latency_ms,
            "estimated_cost": self.estimated_cost,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class ComputeResult:
    """Result of computation"""
    result_id: UUID = field(default_factory=uuid4)
    request_id: UUID = None
    compute_used: ComputeType = ComputeType.CLASSICAL
    status: str = "completed"
    result: Any = None
    error: Optional[str] = None
    actual_latency_ms: float = 0
    actual_cost: float = 0
    fallbacks_used: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": str(self.result_id),
            "request_id": str(self.request_id) if self.request_id else None,
            "compute_used": self.compute_used.value,
            "status": self.status,
            "error": self.error,
            "actual_latency_ms": self.actual_latency_ms,
            "actual_cost": self.actual_cost,
            "fallbacks_used": self.fallbacks_used,
            "timestamp": self.timestamp.isoformat()
        }


class ComputeBackend:
    """Abstract compute backend"""
    
    def __init__(self, compute_type: ComputeType):
        self.compute_type = compute_type
        self.capability = self._init_capability()
    
    def _init_capability(self) -> ComputeCapability:
        """Initialize capability based on type"""
        if self.compute_type == ComputeType.CLASSICAL:
            return ComputeCapability(
                compute_type=ComputeType.CLASSICAL,
                is_available=True,
                latency_ms=5.0,
                throughput_ops=10000,
                error_rate=0.0001
            )
        elif self.compute_type == ComputeType.PHOTONIC:
            return ComputeCapability(
                compute_type=ComputeType.PHOTONIC,
                is_available=False,  # Requires setup
                latency_ms=0.5,
                throughput_ops=100000,
                error_rate=0.001,
                wavelength_nm=1550,
                bandwidth_ghz=100
            )
        elif self.compute_type == ComputeType.QUANTUM:
            return ComputeCapability(
                compute_type=ComputeType.QUANTUM,
                is_available=False,  # Rare
                latency_ms=100.0,  # Slower but powerful
                throughput_ops=10,
                error_rate=0.01,
                cost_per_op=1.0,
                qubit_count=127,
                coherence_time_us=100
            )
        return ComputeCapability(compute_type=self.compute_type)
    
    async def execute(self, payload: Dict[str, Any]) -> Any:
        """Execute computation"""
        # Simulate computation
        await asyncio.sleep(self.capability.latency_ms / 1000)
        
        # Simulate error based on rate
        if random.random() < self.capability.error_rate:
            raise RuntimeError(f"{self.compute_type.value} computation error")
        
        logger.info(f"{self.compute_type.value} compute executed: {payload.get('operation', 'unknown')}")
        
        return {"computed": True, "backend": self.compute_type.value}
    
    async def health_check(self) -> bool:
        """Check backend health"""
        return self.capability.is_available


class QKDKeyManager:
    """Quantum Key Distribution manager for Hub Communication"""
    
    def __init__(self):
        self._keys: Dict[str, bytes] = {}
        self._key_ttl: Dict[str, datetime] = {}
    
    async def generate_key(self, channel_id: str) -> bytes:
        """Generate QKD key for channel"""
        # Simulated QKD key generation
        key = bytes(random.getrandbits(8) for _ in range(32))
        self._keys[channel_id] = key
        self._key_ttl[channel_id] = datetime.utcnow() + timedelta(hours=1)
        
        logger.info(f"QKD key generated for channel {channel_id}")
        return key
    
    async def get_key(self, channel_id: str) -> Optional[bytes]:
        """Get existing key or generate new"""
        if channel_id in self._keys:
            if datetime.utcnow() < self._key_ttl.get(channel_id, datetime.min):
                return self._keys[channel_id]
        return await self.generate_key(channel_id)
    
    async def rotate_key(self, channel_id: str) -> bytes:
        """Force key rotation"""
        return await self.generate_key(channel_id)


class SensorSynchronizer:
    """Photonic sensor synchronization for Hub Navigation"""
    
    def __init__(self):
        self._sync_state: Dict[str, datetime] = {}
    
    async def sync_sensors(self, location_id: str, sensors: List[str]) -> Dict[str, Any]:
        """Synchronize sensors for location"""
        # Simulated photonic sensor sync
        sync_time = datetime.utcnow()
        self._sync_state[location_id] = sync_time
        
        logger.info(f"Sensors synced for location {location_id}: {sensors}")
        
        return {
            "location_id": location_id,
            "synced_sensors": sensors,
            "sync_time": sync_time.isoformat(),
            "precision_ns": 10  # Nanosecond precision with photonics
        }


class QuantumOrchestrator:
    """
    Routes computation dynamically between classical, photonic, and quantum.
    
    Core Principle: Invisible to user. System decides based on:
    1. Security requirements (encryption → quantum/QKD)
    2. Survival priority (emergency → fastest available)
    3. Production needs (normal → cost-optimized)
    
    Always falls back to classical if advanced compute unavailable.
    """
    
    def __init__(self):
        # Compute backends
        self._backends: Dict[ComputeType, ComputeBackend] = {
            ComputeType.CLASSICAL: ComputeBackend(ComputeType.CLASSICAL),
            ComputeType.PHOTONIC: ComputeBackend(ComputeType.PHOTONIC),
            ComputeType.QUANTUM: ComputeBackend(ComputeType.QUANTUM)
        }
        
        # Hub integrations
        self._qkd_manager = QKDKeyManager()
        self._sensor_sync = SensorSynchronizer()
        
        # State sync (multi-hub)
        self._hub_states: Dict[HubIntegration, Dict[str, Any]] = {
            hub: {} for hub in HubIntegration
        }
        
        # Stats
        self._total_requests = 0
        self._compute_usage: Dict[ComputeType, int] = {c: 0 for c in ComputeType}
    
    def route(self, request: ComputeRequest) -> RoutingDecision:
        """
        Determine optimal compute type for request.
        
        Priority: Security > Survival > Production > Background
        """
        decision = RoutingDecision(request_id=request.request_id)
        
        # Priority-based routing
        if request.priority == ComputePriority.SECURITY:
            # Security operations prefer quantum/photonic
            if request.requires_encryption:
                if self._backends[ComputeType.QUANTUM].capability.is_available:
                    decision.selected_compute = ComputeType.QUANTUM
                    decision.reason = "Security priority with encryption: quantum selected"
                else:
                    decision.selected_compute = ComputeType.CLASSICAL
                    decision.reason = "Security priority: quantum unavailable, classical with PQC"
            else:
                decision.selected_compute = ComputeType.CLASSICAL
                decision.reason = "Security priority without encryption: classical sufficient"
        
        elif request.priority == ComputePriority.SURVIVAL:
            # Survival needs fastest available
            if request.requires_low_latency:
                if self._backends[ComputeType.PHOTONIC].capability.is_available:
                    decision.selected_compute = ComputeType.PHOTONIC
                    decision.reason = "Survival priority: photonic for low latency"
                else:
                    decision.selected_compute = ComputeType.CLASSICAL
                    decision.reason = "Survival priority: classical (photonic unavailable)"
            else:
                decision.selected_compute = ComputeType.CLASSICAL
                decision.reason = "Survival priority: classical for reliability"
        
        elif request.priority == ComputePriority.PRODUCTION:
            # Production optimizes cost/performance
            if request.requires_high_throughput:
                if self._backends[ComputeType.PHOTONIC].capability.is_available:
                    decision.selected_compute = ComputeType.PHOTONIC
                    decision.reason = "Production: photonic for high throughput"
                else:
                    decision.selected_compute = ComputeType.CLASSICAL
                    decision.reason = "Production: classical (optimal cost)"
            else:
                decision.selected_compute = ComputeType.CLASSICAL
                decision.reason = "Production: classical (default)"
        
        else:  # BACKGROUND
            decision.selected_compute = ComputeType.CLASSICAL
            decision.reason = "Background: classical (lowest cost)"
        
        # Build fallback chain (always ends with classical)
        if decision.selected_compute == ComputeType.QUANTUM:
            decision.fallback_chain = [ComputeType.PHOTONIC, ComputeType.CLASSICAL]
        elif decision.selected_compute == ComputeType.PHOTONIC:
            decision.fallback_chain = [ComputeType.CLASSICAL]
        else:
            decision.fallback_chain = []
        
        # Estimate latency and cost
        backend = self._backends[decision.selected_compute]
        decision.estimated_latency_ms = backend.capability.latency_ms
        decision.estimated_cost = backend.capability.cost_per_op
        
        return decision
    
    async def execute(self, request: ComputeRequest) -> ComputeResult:
        """
        Execute computation with automatic fallback.
        """
        import time
        start_time = time.time()
        
        self._total_requests += 1
        
        # Get routing decision
        decision = self.route(request)
        
        # Try selected compute, fall back if needed
        compute_chain = [decision.selected_compute] + decision.fallback_chain
        fallbacks_used = 0
        
        for compute_type in compute_chain:
            backend = self._backends[compute_type]
            
            if not backend.capability.is_available:
                fallbacks_used += 1
                continue
            
            try:
                result = await asyncio.wait_for(
                    backend.execute(request.payload),
                    timeout=request.timeout_ms / 1000
                )
                
                self._compute_usage[compute_type] += 1
                
                return ComputeResult(
                    request_id=request.request_id,
                    compute_used=compute_type,
                    status="completed",
                    result=result,
                    actual_latency_ms=(time.time() - start_time) * 1000,
                    actual_cost=backend.capability.cost_per_op,
                    fallbacks_used=fallbacks_used
                )
                
            except asyncio.TimeoutError:
                logger.warning(f"{compute_type.value} timed out, falling back")
                fallbacks_used += 1
                
            except Exception as e:
                logger.warning(f"{compute_type.value} error: {e}, falling back")
                fallbacks_used += 1
        
        # All backends failed
        return ComputeResult(
            request_id=request.request_id,
            compute_used=ComputeType.CLASSICAL,
            status="error",
            error="All compute backends failed",
            actual_latency_ms=(time.time() - start_time) * 1000,
            fallbacks_used=fallbacks_used
        )
    
    async def execute_hub_operation(
        self,
        hub: HubIntegration,
        operation: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute hub-specific operation.
        """
        if hub == HubIntegration.COMMUNICATION:
            # QKD encryption
            if operation == "encrypt":
                key = await self._qkd_manager.get_key(payload.get("channel_id", "default"))
                return {"key_available": True, "key_size": len(key)}
            elif operation == "rotate_key":
                key = await self._qkd_manager.rotate_key(payload.get("channel_id", "default"))
                return {"key_rotated": True}
        
        elif hub == HubIntegration.NAVIGATION:
            # Sensor synchronization
            if operation == "sync_sensors":
                return await self._sensor_sync.sync_sensors(
                    payload.get("location_id", "default"),
                    payload.get("sensors", [])
                )
        
        elif hub == HubIntegration.EXECUTION:
            # Compute acceleration
            request = ComputeRequest(
                operation=operation,
                priority=ComputePriority.PRODUCTION,
                hub_target=hub,
                payload=payload,
                requires_high_throughput=payload.get("high_throughput", False)
            )
            result = await self.execute(request)
            return result.to_dict()
        
        return {"status": "unknown_operation"}
    
    async def sync_hub_states(self) -> Dict[str, Any]:
        """
        Synchronize state across all hubs.
        Called by orchestrator to ensure consistency.
        """
        sync_time = datetime.utcnow()
        
        for hub in HubIntegration:
            self._hub_states[hub]["last_sync"] = sync_time.isoformat()
        
        return {
            "sync_time": sync_time.isoformat(),
            "hubs_synced": [h.value for h in HubIntegration]
        }
    
    def set_backend_availability(self, compute_type: ComputeType, available: bool) -> None:
        """Set backend availability (for testing/config)"""
        self._backends[compute_type].capability.is_available = available
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get all backend capabilities"""
        return {
            ct.value: self._backends[ct].capability.to_dict()
            for ct in ComputeType
            if ct in self._backends
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "total_requests": self._total_requests,
            "compute_usage": {
                ct.value: count for ct, count in self._compute_usage.items()
            },
            "backends": {
                ct.value: {
                    "available": self._backends[ct].capability.is_available,
                    "load": self._backends[ct].capability.current_load
                }
                for ct in ComputeType
                if ct in self._backends
            }
        }


# Singleton instance
_quantum_orchestrator: Optional[QuantumOrchestrator] = None

def get_quantum_orchestrator() -> QuantumOrchestrator:
    """Get singleton quantum orchestrator instance"""
    global _quantum_orchestrator
    if _quantum_orchestrator is None:
        _quantum_orchestrator = QuantumOrchestrator()
    return _quantum_orchestrator
