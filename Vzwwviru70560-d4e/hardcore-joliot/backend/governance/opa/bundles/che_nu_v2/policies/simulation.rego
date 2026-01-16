# ============================================================================
# CHE·NU™ V69 — SIMULATION GOVERNANCE POLICY
# ============================================================================
# Package: che_nu.simulation
# Version: 2.0.0
# Purpose: Rules specific to WorldEngine simulations
# Principle: SYNTHETIC ONLY - No real data execution
# ============================================================================

package che_nu.simulation

import data.che_nu.config
import data.che_nu.base

# ============================================================================
# DEFAULT
# ============================================================================

default allow := false

# ============================================================================
# SIMULATION-SPECIFIC RULES
# ============================================================================

# Allow synthetic simulations in LABS
allow {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.synthetic == true
    input.request.environment == "labs"
    within_step_limit
}

# Allow synthetic simulations in PILOT with restrictions
allow {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.synthetic == true
    input.request.environment == "pilot"
    within_step_limit
    not is_autogen_simulation
}

# Allow synthetic simulations in PROD only if allowlisted
allow {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.synthetic == true
    input.request.environment == "prod"
    config.allow_prod == true
    within_step_limit
    tenant_in_prod_allowlist
}

# ============================================================================
# HELPERS
# ============================================================================

within_step_limit {
    input.request.resource.steps <= config.max_simulation_steps
}

is_autogen_simulation {
    input.request.agent.is_autogen == true
}

tenant_in_prod_allowlist {
    input.request.tenant.id == data.che_nu.prod_allowlist.tenants[_]
}

# ============================================================================
# DENY REASONS
# ============================================================================

deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.synthetic == false
    msg := "SIMULATION_MUST_BE_SYNTHETIC"
}

deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    not within_step_limit
    msg := sprintf("SIMULATION_EXCEEDS_MAX_STEPS_%d", [config.max_simulation_steps])
}

deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    input.request.environment == "pilot"
    is_autogen_simulation
    msg := "AUTOGEN_SIMULATION_NOT_ALLOWED_IN_PILOT"
}

deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    input.request.environment == "prod"
    not config.allow_prod
    msg := "PROD_SIMULATIONS_DISABLED"
}

# ============================================================================
# SIMULATION MODES
# ============================================================================

# Deterministic mode required for reproducibility
deny_reason[msg] {
    input.request.action.type == "RUN_SIMULATION"
    input.request.resource.mode == "non_deterministic"
    not input.request.resource.allow_non_deterministic
    msg := "NON_DETERMINISTIC_MODE_REQUIRES_EXPLICIT_APPROVAL"
}

# Scenario comparison rules
allow_scenario_comparison {
    input.request.action.type == "COMPARE_SCENARIOS"
    input.request.resource.synthetic == true
    count(input.request.resource.scenario_ids) <= 10
}

deny_reason[msg] {
    input.request.action.type == "COMPARE_SCENARIOS"
    count(input.request.resource.scenario_ids) > 10
    msg := "TOO_MANY_SCENARIOS_FOR_COMPARISON_MAX_10"
}

# ============================================================================
# CAUSAL ENGINE INTEGRATION
# ============================================================================

# Causal interventions require explicit approval
deny_reason[msg] {
    input.request.action.type == "CAUSAL_INTERVENTION"
    not input.request.hitl.approved
    msg := "CAUSAL_INTERVENTION_REQUIRES_HITL"
}

# Counterfactual analysis allowed in read mode
allow {
    input.request.action.type == "COUNTERFACTUAL_ANALYSIS"
    input.request.resource.synthetic == true
    base.is_read_only_action
}

# ============================================================================
# RESULT
# ============================================================================

result := {
    "allow": allow,
    "deny_reasons": deny_reason,
    "simulation_mode": input.request.resource.mode,
    "synthetic": input.request.resource.synthetic,
    "trace_id": base.trace_id
}
