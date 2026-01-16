"""
============================================================================
CHE·NU™ V69 — API GATEWAY & SERVICE MESH REGISTRY
============================================================================
Spec: CHE-NU_V52_Gateway_Mesh_Registry_Internal_Spec.md

Role of API Gateway:
- Front door for all external and internal API calls
- Authentication & authorization
- Rate limiting & quotas
- Routing & versioning
- Request/response logging
- Tracing propagation

Non-negotiable: No direct external API calls bypassing the gateway
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    Environment, AuthMethod, RiskCategory,
    RateLimit, APIRoute, ServiceMeshPolicy,
    generate_id, compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """
    Rate limiter for API Gateway.
    
    Per spec: rate_limiting, quotas, retries_with_backoff
    """
    
    def __init__(self):
        self._counters: Dict[str, Dict] = {}  # tenant_id -> {count, window_start}
    
    def check(
        self,
        tenant_id: str,
        route: APIRoute,
    ) -> Tuple[bool, str]:
        """Check if request is within rate limits"""
        now = datetime.utcnow()
        limit = route.rate_limit
        
        if tenant_id not in self._counters:
            self._counters[tenant_id] = {
                "count": 0,
                "window_start": now,
            }
        
        counter = self._counters[tenant_id]
        
        # Reset window if expired
        window_elapsed = (now - counter["window_start"]).total_seconds()
        if window_elapsed > limit.window_seconds:
            counter["count"] = 0
            counter["window_start"] = now
        
        # Check limit
        if counter["count"] >= limit.rps * limit.window_seconds:
            return False, f"Rate limit exceeded: {limit.rps} RPS"
        
        # Increment
        counter["count"] += 1
        return True, "OK"


# ============================================================================
# AUTHENTICATION HANDLER
# ============================================================================

class AuthenticationHandler:
    """
    Authentication handler.
    
    Per spec: oauth2_oidc, api_keys, mTLS_optional
    """
    
    def __init__(self):
        self._api_keys: Dict[str, str] = {}  # key -> tenant_id
        self._tokens: Dict[str, Dict] = {}  # token -> user info
    
    def register_api_key(self, api_key: str, tenant_id: str) -> None:
        """Register an API key"""
        self._api_keys[api_key] = tenant_id
    
    def authenticate(
        self,
        method: AuthMethod,
        credentials: Dict[str, str],
    ) -> Tuple[bool, Dict[str, Any]]:
        """Authenticate request"""
        if method == AuthMethod.API_KEY:
            key = credentials.get("api_key", "")
            if key in self._api_keys:
                return True, {"tenant_id": self._api_keys[key]}
            return False, {"error": "Invalid API key"}
        
        elif method == AuthMethod.OAUTH2_OIDC:
            token = credentials.get("token", "")
            if token in self._tokens:
                return True, self._tokens[token]
            return False, {"error": "Invalid token"}
        
        elif method == AuthMethod.MTLS:
            # Mock mTLS validation
            cert = credentials.get("client_cert", "")
            if cert:
                return True, {"tenant_id": "mtls_tenant", "method": "mTLS"}
            return False, {"error": "No client certificate"}
        
        return False, {"error": "Unknown auth method"}


# ============================================================================
# API GATEWAY
# ============================================================================

class APIGateway:
    """
    API Gateway.
    
    Per spec: Front door for all API calls
    """
    
    def __init__(self):
        self._routes: Dict[str, APIRoute] = {}
        self.rate_limiter = RateLimiter()
        self.auth_handler = AuthenticationHandler()
        self._request_log: List[Dict] = []
    
    def register_route(self, route: APIRoute) -> None:
        """Register an API route"""
        self._routes[route.route_id] = route
        logger.info(f"Registered route: {route.route_id} -> {route.service_name}")
    
    def process_request(
        self,
        route_id: str,
        tenant_id: str,
        request_data: Dict[str, Any],
        auth_credentials: Dict[str, str] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Process incoming request.
        
        Per spec: authn, authz, rate limiting, logging, tracing
        """
        route = self._routes.get(route_id)
        if not route:
            return False, {"error": "Route not found"}
        
        if not route.enabled:
            return False, {"error": "Route disabled"}
        
        # Log request
        trace_id = generate_id()
        log_entry = {
            "trace_id": trace_id,
            "route_id": route_id,
            "tenant_id": tenant_id,
            "timestamp": datetime.utcnow().isoformat(),
            "environment": route.environment.value,
        }
        
        # Authentication
        if route.auth_required and auth_credentials:
            auth_method = AuthMethod.API_KEY  # Default
            if "token" in auth_credentials:
                auth_method = AuthMethod.OAUTH2_OIDC
            
            auth_ok, auth_info = self.auth_handler.authenticate(auth_method, auth_credentials)
            if not auth_ok:
                log_entry["status"] = "auth_failed"
                self._request_log.append(log_entry)
                return False, {"error": "Authentication failed", "trace_id": trace_id}
        
        # Rate limiting
        allowed, reason = self.rate_limiter.check(tenant_id, route)
        if not allowed:
            log_entry["status"] = "rate_limited"
            self._request_log.append(log_entry)
            return False, {"error": reason, "trace_id": trace_id}
        
        # Process (mock - would route to service)
        log_entry["status"] = "success"
        self._request_log.append(log_entry)
        
        return True, {
            "trace_id": trace_id,
            "service": route.service_name,
            "environment": route.environment.value,
            "data": request_data,
        }
    
    def get_request_log(self, n: int = 100) -> List[Dict]:
        """Get recent request log"""
        return self._request_log[-n:]


# ============================================================================
# SERVICE MESH
# ============================================================================

class ServiceMesh:
    """
    Service Mesh (Istio-style).
    
    Per spec: Reliability, policy, observability
    """
    
    def __init__(self):
        self._policies: Dict[str, ServiceMeshPolicy] = {}
        self._circuit_breakers: Dict[str, Dict] = {}
    
    def register_policy(self, policy: ServiceMeshPolicy) -> None:
        """Register mesh policy"""
        self._policies[policy.policy_id] = policy
        
        if policy.circuit_breaker_enabled:
            self._circuit_breakers[policy.service_name] = {
                "failures": 0,
                "state": "closed",  # closed, open, half-open
                "last_failure": None,
            }
    
    def check_circuit_breaker(self, service_name: str) -> Tuple[bool, str]:
        """Check circuit breaker state"""
        cb = self._circuit_breakers.get(service_name)
        if not cb:
            return True, "No circuit breaker"
        
        if cb["state"] == "open":
            return False, "Circuit breaker open"
        
        return True, "OK"
    
    def record_failure(self, service_name: str) -> None:
        """Record service failure"""
        cb = self._circuit_breakers.get(service_name)
        if not cb:
            return
        
        cb["failures"] += 1
        cb["last_failure"] = datetime.utcnow()
        
        # Open circuit breaker after 5 failures
        if cb["failures"] >= 5:
            cb["state"] = "open"
            logger.warning(f"Circuit breaker opened for {service_name}")
    
    def record_success(self, service_name: str) -> None:
        """Record service success"""
        cb = self._circuit_breakers.get(service_name)
        if not cb:
            return
        
        cb["failures"] = 0
        cb["state"] = "closed"


# ============================================================================
# AGENT REGISTRY
# ============================================================================

@dataclass
class RegisteredAgent:
    """Registered agent in the registry"""
    agent_id: str
    blueprint_id: str
    level: str
    sphere: str
    
    api_endpoint: str = ""
    enabled: bool = True
    
    created_at: datetime = field(default_factory=datetime.utcnow)


class AgentRegistry:
    """
    Agent Registry - Central control plane.
    
    Per spec: 287 agents + API wrappers
    """
    
    def __init__(self):
        self._agents: Dict[str, RegisteredAgent] = {}
    
    def register(self, agent: RegisteredAgent) -> None:
        """Register an agent"""
        self._agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id} ({agent.blueprint_id})")
    
    def get(self, agent_id: str) -> Optional[RegisteredAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)
    
    def list_by_level(self, level: str) -> List[RegisteredAgent]:
        """List agents by level"""
        return [a for a in self._agents.values() if a.level == level]
    
    def list_by_sphere(self, sphere: str) -> List[RegisteredAgent]:
        """List agents by sphere"""
        return [a for a in self._agents.values() if a.sphere == sphere]
    
    def enable(self, agent_id: str) -> bool:
        """Enable agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.enabled = True
            return True
        return False
    
    def disable(self, agent_id: str) -> bool:
        """Disable agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.enabled = False
            return True
        return False


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_gateway() -> APIGateway:
    return APIGateway()

def create_service_mesh() -> ServiceMesh:
    return ServiceMesh()

def create_agent_registry() -> AgentRegistry:
    return AgentRegistry()
