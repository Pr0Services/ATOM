# ============================================================================
# CHE·NU™ V69 — HEALTH SPHERE POLICY (EXTRA STRICT)
# ============================================================================
package che_nu.spheres.health

# Health sphere - maximum restriction
default allow := false

# Health data is always sensitive
sensitive_by_default := true

# Execution is RESTRICTED in health sphere
deny_reason[msg] {
    input.request.agent.sphere == "health"
    input.request.action.type == "execute"
    msg := "HEALTH_EXECUTION_RESTRICTED"
}

# All mutations require HITL
deny_reason[msg] {
    input.request.agent.sphere == "health"
    mutation_action
    not input.request.hitl.approved
    msg := "HEALTH_MUTATION_REQUIRES_HITL"
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

# Allow read-only actions
allow {
    input.request.agent.sphere == "health"
    input.request.action.type == "discuss"
}

allow {
    input.request.agent.sphere == "health"
    input.request.action.type == "propose"
}

allow {
    input.request.agent.sphere == "health"
    input.request.action.type == "plan"
}

# Audit level is always critical for health
audit_level := "critical"
