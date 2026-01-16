# ============================================================================
# CHE·NU™ V69 — PRODUCTION ENVIRONMENT POLICY
# ============================================================================
# Package: che_nu.env.prod
# Version: 2.0.0
# Purpose: Maximum security and governance
# Principle: DENY BY DEFAULT - Explicit allowlist required
# ============================================================================

package che_nu.env.prod

import data.che_nu.config
import data.che_nu.prod_allowlist

# Production is DENY by default
default allow := false

# ============================================================================
# ALLOWLIST CHECKS
# ============================================================================

# Only allow if everything is explicitly allowlisted
allow {
    config.allow_prod == true
    tenant_allowlisted
    agent_allowlisted
    route_allowlisted_if_applicable
    input.request.resource.synthetic == true
}

tenant_allowlisted {
    input.request.tenant.id == prod_allowlist.tenants[_]
}

agent_allowlisted {
    input.request.agent.blueprint_id == prod_allowlist.agent_blueprints[_]
}

route_allowlisted_if_applicable {
    input.request.action.target != "api"
}

route_allowlisted_if_applicable {
    input.request.action.target == "api"
    input.request.action.resource_id == ""
}

route_allowlisted_if_applicable {
    input.request.action.target == "api"
    input.request.action.resource_id == prod_allowlist.routes[_]
}

# ============================================================================
# DENY REASONS
# ============================================================================

deny_reason[msg] {
    not config.allow_prod
    msg := "PROD_GLOBALLY_DISABLED"
}

deny_reason[msg] {
    config.allow_prod
    not tenant_allowlisted
    msg := "PROD_TENANT_NOT_ALLOWLISTED"
}

deny_reason[msg] {
    config.allow_prod
    not agent_allowlisted
    msg := "PROD_AGENT_NOT_ALLOWLISTED"
}

deny_reason[msg] {
    config.allow_prod
    input.request.action.target == "api"
    input.request.action.resource_id != ""
    not route_allowlisted_if_applicable
    msg := "PROD_ROUTE_NOT_ALLOWLISTED"
}

# AutoGen NEVER allowed in PROD
deny_reason[msg] {
    input.request.agent.is_autogen == true
    msg := "AUTOGEN_NEVER_ALLOWED_IN_PROD"
}

# L3 agents disabled in PROD by default
deny_reason[msg] {
    input.request.agent.level == "L3"
    msg := "L3_AGENTS_DISABLED_IN_PROD"
}

# All mutations require HITL in PROD
deny_reason[msg] {
    mutation_action
    not input.request.hitl.approved
    msg := "PROD_MUTATION_REQUIRES_HITL"
}

mutation_action {
    input.request.action.type == "write"
}
mutation_action {
    input.request.action.type == "delete"
}
mutation_action {
    input.request.action.type == "export"
}
mutation_action {
    input.request.action.type == "connect"
}
mutation_action {
    input.request.action.type == "execute"
}

# XR absolutely read-only in PROD
deny_reason[msg] {
    input.request.action.target == "xr"
    input.request.action.type != "discuss"
    input.request.action.type != "propose"
    input.request.action.type != "plan"
    msg := "PROD_XR_STRICTLY_READ_ONLY"
}

# Real data never allowed
deny_reason[msg] {
    input.request.resource.synthetic == false
    msg := "PROD_REQUIRES_SYNTHETIC_DATA_ONLY"
}

# ============================================================================
# REQUIRED CONTROLS IN PROD
# ============================================================================

required_controls[ctl] {
    ctl := "AUDIT_LOGGING_REQUIRED"
}

required_controls[ctl] {
    ctl := "HITL_APPROVAL_REQUIRED"
}

required_controls[ctl] {
    ctl := "EXPLAINABILITY_REQUIRED"
}

required_controls[ctl] {
    ctl := "SIGNATURE_VERIFICATION_REQUIRED"
}

# ============================================================================
# AUDIT
# ============================================================================

# Everything in PROD is critical audit level
audit_level := "critical"

# ============================================================================
# RESULT
# ============================================================================

result := {
    "allow": allow,
    "deny_reasons": deny_reason,
    "required_controls": required_controls,
    "audit_level": audit_level,
    "environment": "prod"
}
