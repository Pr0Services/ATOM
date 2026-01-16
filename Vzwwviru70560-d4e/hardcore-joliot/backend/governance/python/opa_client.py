"""
============================================================================
CHE·NU™ V69 — OPA CLIENT
============================================================================
Version: 2.0.0
Purpose: Python client for OPA governance decisions
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel

from .models import (
    OPARequest,
    OPADecision,
    AuditDecision,
    AuditLevel,
)

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

class OPAConfig(BaseModel):
    """OPA client configuration"""
    url: str = "http://localhost:8181"
    timeout: float = 5.0
    retry_count: int = 3
    retry_delay: float = 0.5
    bundle_name: str = "che_nu_v2"
    policy_path: str = "che_nu/core/result"
    enable_audit_logging: bool = True
    audit_storage_path: Optional[str] = None


# ============================================================================
# OPA CLIENT
# ============================================================================

class OPAClient:
    """
    OPA Client for CHE·NU™ governance decisions.
    
    Usage:
        client = OPAClient()
        decision = await client.decide(request)
        if decision.allow:
            # proceed
        else:
            # handle denial
    """

    def __init__(self, config: Optional[OPAConfig] = None):
        self.config = config or OPAConfig()
        self._client: Optional[httpx.AsyncClient] = None
        self._sync_client: Optional[httpx.Client] = None

    @property
    def policy_endpoint(self) -> str:
        """Get the full policy endpoint URL"""
        return f"{self.config.url}/v1/data/{self.config.policy_path}"

    @property
    def health_endpoint(self) -> str:
        """Get the health check endpoint"""
        return f"{self.config.url}/health"

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client"""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self._client

    def _get_sync_client(self) -> httpx.Client:
        """Get or create sync HTTP client"""
        if self._sync_client is None:
            self._sync_client = httpx.Client(timeout=self.config.timeout)
        return self._sync_client

    async def close(self):
        """Close HTTP clients"""
        if self._client:
            await self._client.aclose()
            self._client = None
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None

    async def health_check(self) -> bool:
        """Check if OPA is healthy"""
        try:
            client = await self._get_client()
            response = await client.get(self.health_endpoint)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"OPA health check failed: {e}")
            return False

    def health_check_sync(self) -> bool:
        """Synchronous health check"""
        try:
            client = self._get_sync_client()
            response = client.get(self.health_endpoint)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"OPA health check failed: {e}")
            return False

    async def decide(
        self,
        request: OPARequest,
        audit: bool = True,
    ) -> OPADecision:
        """
        Make a governance decision via OPA.
        
        Args:
            request: The OPA request
            audit: Whether to log the decision
            
        Returns:
            OPADecision with allow/deny and reasons
        """
        client = await self._get_client()
        input_data = {"input": request.to_opa_input()["request"]}
        
        # Calculate request hash for audit
        request_hash = hashlib.sha256(
            json.dumps(input_data, sort_keys=True, default=str).encode()
        ).hexdigest()

        # Retry logic
        last_error: Optional[Exception] = None
        for attempt in range(self.config.retry_count):
            try:
                response = await client.post(
                    self.policy_endpoint,
                    json=input_data,
                )
                response.raise_for_status()
                result = response.json()
                
                # Parse OPA response
                decision = self._parse_decision(result)
                
                # Audit logging
                if audit and self.config.enable_audit_logging:
                    await self._log_audit(request, decision, request_hash)
                
                return decision

            except httpx.HTTPStatusError as e:
                last_error = e
                logger.error(f"OPA HTTP error (attempt {attempt + 1}): {e}")
            except httpx.RequestError as e:
                last_error = e
                logger.error(f"OPA request error (attempt {attempt + 1}): {e}")
            except Exception as e:
                last_error = e
                logger.error(f"OPA unexpected error (attempt {attempt + 1}): {e}")

            if attempt < self.config.retry_count - 1:
                await asyncio.sleep(self.config.retry_delay * (attempt + 1))

        # All retries failed - deny by default (GOUVERNANCE > EXÉCUTION)
        logger.error(f"OPA decision failed after {self.config.retry_count} attempts: {last_error}")
        return OPADecision(
            allow=False,
            deny_reasons=["OPA_UNAVAILABLE_DENY_BY_DEFAULT"],
            audit_level=AuditLevel.CRITICAL,
            trace_id=request.trace_id,
        )

    def decide_sync(
        self,
        request: OPARequest,
        audit: bool = True,
    ) -> OPADecision:
        """Synchronous version of decide()"""
        client = self._get_sync_client()
        input_data = {"input": request.to_opa_input()["request"]}
        
        request_hash = hashlib.sha256(
            json.dumps(input_data, sort_keys=True, default=str).encode()
        ).hexdigest()

        last_error: Optional[Exception] = None
        for attempt in range(self.config.retry_count):
            try:
                response = client.post(
                    self.policy_endpoint,
                    json=input_data,
                )
                response.raise_for_status()
                result = response.json()
                decision = self._parse_decision(result)
                
                if audit and self.config.enable_audit_logging:
                    self._log_audit_sync(request, decision, request_hash)
                
                return decision

            except Exception as e:
                last_error = e
                logger.error(f"OPA error (attempt {attempt + 1}): {e}")

            if attempt < self.config.retry_count - 1:
                import time
                time.sleep(self.config.retry_delay * (attempt + 1))

        logger.error(f"OPA decision failed after {self.config.retry_count} attempts: {last_error}")
        return OPADecision(
            allow=False,
            deny_reasons=["OPA_UNAVAILABLE_DENY_BY_DEFAULT"],
            audit_level=AuditLevel.CRITICAL,
            trace_id=request.trace_id,
        )

    def _parse_decision(self, result: Dict[str, Any]) -> OPADecision:
        """Parse OPA response into OPADecision"""
        # Handle nested result structure
        if "result" in result:
            data = result["result"]
        else:
            data = result

        return OPADecision(
            allow=data.get("allow", False),
            require_human_approval=data.get("require_human_approval", False),
            deny_reasons=list(data.get("deny_reasons", [])),
            required_controls=list(data.get("required_controls", [])),
            audit_level=AuditLevel(data.get("audit_level", "standard")),
            synthetic=data.get("synthetic", True),
            trace_id=data.get("trace_id"),
            redactions=data.get("redactions", []),
        )

    async def _log_audit(
        self,
        request: OPARequest,
        decision: OPADecision,
        request_hash: str,
    ):
        """Log decision to audit trail"""
        audit = AuditDecision(
            trace_id=request.trace_id,
            tenant_id=request.tenant.id,
            user_id=request.actor.id,
            agent_id=request.agent.blueprint_id,
            agent_level=request.agent.level,
            environment=request.environment,
            action_type=request.action.type,
            action_target=request.action.target,
            decision=decision,
            request_hash=request_hash,
        )
        
        logger.info(
            f"OPA Decision: {audit.decision_id} | "
            f"trace={audit.trace_id} | "
            f"allow={decision.allow} | "
            f"reasons={decision.deny_reasons}"
        )
        
        # TODO: Store to persistent audit log
        if self.config.audit_storage_path:
            # Would write to file/database
            pass

    def _log_audit_sync(
        self,
        request: OPARequest,
        decision: OPADecision,
        request_hash: str,
    ):
        """Synchronous audit logging"""
        audit = AuditDecision(
            trace_id=request.trace_id,
            tenant_id=request.tenant.id,
            user_id=request.actor.id,
            agent_id=request.agent.blueprint_id,
            agent_level=request.agent.level,
            environment=request.environment,
            action_type=request.action.type,
            action_target=request.action.target,
            decision=decision,
            request_hash=request_hash,
        )
        
        logger.info(
            f"OPA Decision: {audit.decision_id} | "
            f"trace={audit.trace_id} | "
            f"allow={decision.allow} | "
            f"reasons={decision.deny_reasons}"
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

_default_client: Optional[OPAClient] = None


def get_opa_client(config: Optional[OPAConfig] = None) -> OPAClient:
    """Get or create default OPA client"""
    global _default_client
    if _default_client is None:
        _default_client = OPAClient(config)
    return _default_client


async def opa_decide(request: OPARequest) -> OPADecision:
    """Quick decision helper"""
    client = get_opa_client()
    return await client.decide(request)


def opa_decide_sync(request: OPARequest) -> OPADecision:
    """Synchronous quick decision helper"""
    client = get_opa_client()
    return client.decide_sync(request)


# ============================================================================
# DECORATORS
# ============================================================================

def require_governance(
    action_type: str,
    action_target: str,
    sphere: str = "business",
):
    """
    Decorator to require OPA governance check before function execution.
    
    Usage:
        @require_governance(action_type="execute", action_target="simulation")
        async def run_simulation(tenant_id: str, ...):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract tenant and user from kwargs or args
            tenant_id = kwargs.get("tenant_id", "unknown")
            user_id = kwargs.get("user_id", "unknown")
            agent_id = kwargs.get("agent_id", "default")
            
            # Build request
            from .models import (
                OPARequest, Tenant, Actor, Agent, Action,
                ActionType, ActionTarget, Sphere, AgentLevel,
                Autonomy, RiskLevel, DataClassification,
            )
            
            request = OPARequest(
                tenant=Tenant(id=tenant_id),
                actor=Actor(type="user", id=user_id),
                agent=Agent(
                    blueprint_id=agent_id,
                    level=AgentLevel.L1,
                    sphere=Sphere(sphere),
                    autonomy=Autonomy.ASSISTED,
                    risk_level=RiskLevel.LOW,
                ),
                action=Action(
                    type=ActionType(action_type),
                    target=ActionTarget(action_target),
                    data_classification=DataClassification.INTERNAL,
                ),
            )
            
            # Check governance
            decision = await opa_decide(request)
            
            if not decision.allow:
                raise PermissionError(
                    f"Governance denied: {decision.deny_reasons}"
                )
            
            # Proceed with function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
