# ============================================================================
# CHE·NU™ V69 — BASE HELPERS & UTILITIES
# ============================================================================
# Package: che_nu.base
# Version: 2.0.0
# Purpose: Common helpers and utility functions for all policies
# ============================================================================

package che_nu.base

import data.che_nu.config

# ============================================================================
# TIME HELPERS
# ============================================================================

# Current timestamp from input or default
current_time := input.request.timestamp {
    input.request.timestamp
}

current_time := time.now_ns() {
    not input.request.timestamp
}

# Check if request is within business hours (example)
is_business_hours {
    hour := time.clock(current_time)[0]
    hour >= 9
    hour < 18
}

# ============================================================================
# TENANT HELPERS
# ============================================================================

# Get tenant plan with default
tenant_plan := input.request.tenant.plan {
    input.request.tenant.plan
}

tenant_plan := "free" {
    not input.request.tenant.plan
}

is_enterprise_tenant {
    tenant_plan == "enterprise"
}

is_pro_tenant {
    tenant_plan == "pro"
}

is_free_tenant {
    tenant_plan == "free"
}

# ============================================================================
# AGENT HELPERS
# ============================================================================

# Agent level numeric (for comparisons)
agent_level_num := 0 {
    input.request.agent.level == "L0"
}

agent_level_num := 1 {
    input.request.agent.level == "L1"
}

agent_level_num := 2 {
    input.request.agent.level == "L2"
}

agent_level_num := 3 {
    input.request.agent.level == "L3"
}

# Agent autonomy levels
autonomy_level := input.request.agent.autonomy {
    input.request.agent.autonomy
}

autonomy_level := "restricted" {
    not input.request.agent.autonomy
}

is_informational_autonomy {
    autonomy_level == "informational"
}

is_assisted_autonomy {
    autonomy_level == "assisted"
}

is_governed_autonomy {
    autonomy_level == "governed"
}

is_restricted_autonomy {
    autonomy_level == "restricted"
}

# ============================================================================
# SPHERE HELPERS
# ============================================================================

# Get sphere configuration
sphere_config := data.che_nu.spheres[sphere_name] {
    sphere_name := input.request.agent.sphere
}

sphere_enabled {
    sphere_config.enabled == true
}

sphere_sensitive_by_default {
    sphere_config.sensitive_by_default == true
}

# ============================================================================
# ACTION CLASSIFICATION
# ============================================================================

# Read-only actions
is_read_only_action {
    input.request.action.type == "discuss"
}

is_read_only_action {
    input.request.action.type == "propose"
}

is_read_only_action {
    input.request.action.type == "plan"
}

# Mutation actions
is_mutation_action {
    input.request.action.type == "write"
}

is_mutation_action {
    input.request.action.type == "delete"
}

is_mutation_action {
    input.request.action.type == "export"
}

is_mutation_action {
    input.request.action.type == "connect"
}

# Execution action
is_execution_action {
    input.request.action.type == "execute"
}

# ============================================================================
# RISK SCORING
# ============================================================================

# Calculate risk score (0-100)
risk_score := score {
    base := 0
    
    # Add for high-risk agent
    agent_risk := 30 { input.request.agent.risk_level == "high" }
    agent_risk := 15 { input.request.agent.risk_level == "medium" }
    agent_risk := 0 { input.request.agent.risk_level == "low" }
    
    # Add for sensitive data
    data_risk := 25 { input.request.action.data_classification == "sensitive" }
    data_risk := 10 { input.request.action.data_classification == "internal" }
    data_risk := 0 { input.request.action.data_classification == "public" }
    
    # Add for mutations
    action_risk := 25 { is_mutation_action }
    action_risk := 20 { is_execution_action }
    action_risk := 0 { is_read_only_action }
    
    # Add for PROD
    env_risk := 20 { input.request.environment == "prod" }
    env_risk := 10 { input.request.environment == "pilot" }
    env_risk := 0 { input.request.environment == "labs" }
    
    score := base + agent_risk + data_risk + action_risk + env_risk
}

is_high_risk_score {
    risk_score >= 50
}

is_medium_risk_score {
    risk_score >= 25
    risk_score < 50
}

is_low_risk_score {
    risk_score < 25
}

# ============================================================================
# TRACE & AUDIT HELPERS
# ============================================================================

# Get trace ID with fallback
trace_id := input.request.trace_id {
    input.request.trace_id
}

trace_id := input.request.request_id {
    not input.request.trace_id
    input.request.request_id
}

trace_id := "unknown" {
    not input.request.trace_id
    not input.request.request_id
}

# Build audit entry
audit_entry := {
    "trace_id": trace_id,
    "timestamp": current_time,
    "tenant_id": input.request.tenant.id,
    "user_id": input.request.actor.id,
    "agent_id": input.request.agent.blueprint_id,
    "agent_level": input.request.agent.level,
    "action_type": input.request.action.type,
    "action_target": input.request.action.target,
    "environment": input.request.environment,
    "risk_score": risk_score
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

feature_enabled(feature_name) {
    data.che_nu.feature_flags[feature_name] == true
}

pqc_enabled {
    feature_enabled("enable_pqc_signatures")
}

causal_engine_enabled {
    feature_enabled("enable_causal_engine")
}

immutable_audit_enabled {
    feature_enabled("enable_immutable_audit")
}

xr_wasm_verify_enabled {
    feature_enabled("enable_xr_wasm_verify")
}
