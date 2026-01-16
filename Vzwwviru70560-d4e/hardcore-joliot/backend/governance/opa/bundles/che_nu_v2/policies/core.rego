# ============================================================================
# CHE·NU™ V69 — CORE GOVERNANCE POLICY (7 RULES)
# ============================================================================
# Package: che_nu.core
# Version: 2.0.0
# Principles: GOUVERNANCE > EXÉCUTION
#
# THE 7 RULES:
# 1. AutoGen sandbox-only (LABS only by default)
# 2. No PROD access unless explicitly allowlisted
# 3. Sensitive data requires HITL approval + allowlist
# 4. High-impact actions require HITL approval
# 5. Explainability required for all decisions
# 6. XR is read-only (no write/execute/mutate)
# 7. Audit logging is mandatory
# ============================================================================

package che_nu.core

import data.che_nu.config
import data.che_nu.prod_allowlist
import data.che_nu.sensitive_data_allowlist

# ============================================================================
# DEFAULT DECISIONS
# ============================================================================

default allow := false
default require_human_approval := false
default audit_level := "standard"

# ============================================================================
# OUTPUT STRUCTURE
# ============================================================================

# Collect all deny reasons
deny_reasons[msg] {
    not allow
    count(deny_reason) == 0
    msg := "DENY_BY_DEFAULT"
}

deny_reasons[msg] {
    msg := deny_reason[_]
}

# Required controls to enforce
required_controls[ctl] {
    ctl := "AUDIT_LOGGING_REQUIRED"
}

required_controls[ctl] {
    is_sensitive
    ctl := "HITL_APPROVAL_REQUIRED"
}

required_controls[ctl] {
    is_high_risk
    is_mutation_or_exec
    ctl := "HITL_APPROVAL_REQUIRED"
}

# Final result object (for API response)
result := {
    "allow": allow,
    "require_human_approval": require_human_approval,
    "deny_reasons": deny_reasons,
    "required_controls": required_controls,
    "audit_level": audit_level,
    "synthetic": config.synthetic_only,
    "trace_id": input.request.trace_id
}

# ============================================================================
# INPUT HELPERS
# ============================================================================

# Environment
env := input.request.environment
is_labs { env == "labs" }
is_pilot { env == "pilot" }
is_prod { env == "prod" }

# Agent attributes
agent := input.request.agent
agent_level := agent.level
agent_sphere := agent.sphere
agent_blueprint := agent.blueprint_id
is_autogen { agent.is_autogen == true }
is_high_risk { agent.risk_level == "high" }

# Action attributes
action := input.request.action
action_type := action.type
action_target := action.target
resource_id := action.resource_id

# Data classification
is_sensitive { action.data_classification == "sensitive" }
is_xr { action_target == "xr" }

# Action types
is_discuss { action_type == "discuss" }
is_propose { action_type == "propose" }
is_plan { action_type == "plan" }
is_execute { action_type == "execute" }
is_write { action_type == "write" }
is_delete { action_type == "delete" }
is_export { action_type == "export" }
is_connect { action_type == "connect" }

is_mutation_or_exec {
    is_execute
}
is_mutation_or_exec {
    is_write
}
is_mutation_or_exec {
    is_delete
}
is_mutation_or_exec {
    is_export
}
is_mutation_or_exec {
    is_connect
}

# HITL
hitl := input.request.hitl
hitl_approved { hitl.approved == true }

# Explainability
exp := input.request.explainability
explainability_required { exp.required == true }
explainability_provided { exp.provided == true }

# Controls
ctrl := input.request.controls
audit_logging_enabled { ctrl.audit_logging == true }

# Tenant
tenant_id := input.request.tenant.id

# ============================================================================
# RULE 7: AUDIT LOGGING REQUIRED (checked first)
# ============================================================================

deny_reason[msg] {
    not audit_logging_enabled
    msg := "AUDIT_LOGGING_MISSING"
}

# ============================================================================
# RULE 5: EXPLAINABILITY REQUIRED
# ============================================================================

deny_reason[msg] {
    explainability_required
    not explainability_provided
    msg := "EXPLAINABILITY_NOT_PROVIDED"
}

# ============================================================================
# RULE 1: AUTOGEN SANDBOX-ONLY (LABS by default)
# ============================================================================

# AutoGen only allowed in LABS
deny_reason[msg] {
    is_autogen
    not is_labs
    not config.allow_autogen_in_pilot
    msg := "AUTOGEN_LABS_ONLY"
}

# AutoGen in PILOT cannot execute
deny_reason[msg] {
    is_autogen
    is_pilot
    config.allow_autogen_in_pilot
    is_execute
    msg := "AUTOGEN_NO_EXECUTION_IN_PILOT"
}

# AutoGen never in PROD
deny_reason[msg] {
    is_autogen
    is_prod
    msg := "AUTOGEN_NEVER_IN_PROD"
}

# ============================================================================
# RULE 2: PROD ACCESS REQUIRES ALLOWLIST
# ============================================================================

# PROD globally disabled
deny_reason[msg] {
    is_prod
    not config.allow_prod
    msg := "PROD_DISABLED_GLOBAL"
}

# Tenant not in PROD allowlist
deny_reason[msg] {
    is_prod
    config.allow_prod
    not tenant_in_prod_allowlist
    msg := "PROD_TENANT_NOT_ALLOWLISTED"
}

tenant_in_prod_allowlist {
    tenant_id == prod_allowlist.tenants[_]
}

# Route not in PROD allowlist (for API targets)
deny_reason[msg] {
    is_prod
    config.allow_prod
    action_target == "api"
    resource_id != ""
    not route_in_prod_allowlist
    msg := "PROD_ROUTE_NOT_ALLOWLISTED"
}

route_in_prod_allowlist {
    resource_id == prod_allowlist.routes[_]
}

# Agent blueprint not in PROD allowlist
deny_reason[msg] {
    is_prod
    config.allow_prod
    not blueprint_in_prod_allowlist
    msg := "PROD_AGENT_BLUEPRINT_NOT_ALLOWLISTED"
}

blueprint_in_prod_allowlist {
    agent_blueprint == prod_allowlist.agent_blueprints[_]
}

# ============================================================================
# RULE 3: SENSITIVE DATA REQUIRES HITL + ALLOWLIST
# ============================================================================

require_human_approval {
    is_sensitive
}

deny_reason[msg] {
    is_sensitive
    not hitl_approved
    msg := "SENSITIVE_DATA_REQUIRES_HITL"
}

# Tenant not in sensitive data allowlist (if allowlist has entries)
deny_reason[msg] {
    is_sensitive
    hitl_approved
    count(sensitive_data_allowlist.tenants) > 0
    not tenant_in_sensitive_allowlist
    msg := "SENSITIVE_DATA_TENANT_NOT_ALLOWLISTED"
}

tenant_in_sensitive_allowlist {
    tenant_id == sensitive_data_allowlist.tenants[_]
}

# Agent not in sensitive data allowlist (if allowlist has entries)
deny_reason[msg] {
    is_sensitive
    hitl_approved
    count(sensitive_data_allowlist.agent_blueprints) > 0
    not blueprint_in_sensitive_allowlist
    msg := "SENSITIVE_DATA_AGENT_NOT_ALLOWLISTED"
}

blueprint_in_sensitive_allowlist {
    agent_blueprint == sensitive_data_allowlist.agent_blueprints[_]
}

# ============================================================================
# RULE 4: HIGH-IMPACT ACTIONS REQUIRE HITL
# ============================================================================

require_human_approval {
    is_high_risk
    is_mutation_or_exec
}

deny_reason[msg] {
    is_high_risk
    is_mutation_or_exec
    not hitl_approved
    msg := "HIGH_IMPACT_REQUIRES_HITL"
}

# ============================================================================
# RULE 6: XR READ-ONLY (CRITICAL - NON-NEGOTIABLE)
# ============================================================================

deny_reason[msg] {
    is_xr
    is_execute
    msg := "XR_READ_ONLY_NO_EXECUTE"
}

deny_reason[msg] {
    is_xr
    is_write
    msg := "XR_READ_ONLY_NO_WRITE"
}

deny_reason[msg] {
    is_xr
    is_delete
    msg := "XR_READ_ONLY_NO_DELETE"
}

deny_reason[msg] {
    is_xr
    is_export
    msg := "XR_READ_ONLY_NO_EXPORT"
}

deny_reason[msg] {
    is_xr
    is_connect
    msg := "XR_READ_ONLY_NO_CONNECT"
}

# ============================================================================
# SYNTHETIC-ONLY ENFORCEMENT
# ============================================================================

deny_reason[msg] {
    config.synthetic_only
    input.request.resource.synthetic == false
    msg := "REAL_DATA_NOT_ALLOWED_SYNTHETIC_ONLY"
}

# ============================================================================
# SIMULATION STEP LIMIT
# ============================================================================

deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.steps > config.max_simulation_steps
    msg := sprintf("SIMULATION_STEPS_EXCEED_LIMIT_%d", [config.max_simulation_steps])
}

# ============================================================================
# FINAL ALLOW (only if no deny reasons)
# ============================================================================

allow {
    count(deny_reason) == 0
}

# ============================================================================
# AUDIT LEVEL DETERMINATION
# ============================================================================

audit_level := "critical" {
    is_sensitive
}

audit_level := "critical" {
    is_high_risk
}

audit_level := "elevated" {
    is_mutation_or_exec
}

audit_level := "elevated" {
    is_prod
}
