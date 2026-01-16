# ============================================================================
# CHE·NU™ V69 — LEGAL COMPLIANCE SPHERE POLICY
# ============================================================================
package che_nu.spheres.legal_compliance

# Legal/Compliance - ALL mutations require HITL
default allow := false

# All mutations and executions require HITL
deny_reason[msg] {
    input.request.agent.sphere == "legal_compliance"
    mutation_or_exec
    not input.request.hitl.approved
    msg := "LEGAL_COMPLIANCE_REQUIRES_HITL"
}

mutation_or_exec {
    input.request.action.type == "write"
}
mutation_or_exec {
    input.request.action.type == "delete"
}
mutation_or_exec {
    input.request.action.type == "export"
}
mutation_or_exec {
    input.request.action.type == "connect"
}
mutation_or_exec {
    input.request.action.type == "execute"
}

# Allow read-only actions
allow {
    input.request.agent.sphere == "legal_compliance"
    input.request.action.type == "discuss"
}

allow {
    input.request.agent.sphere == "legal_compliance"
    input.request.action.type == "propose"
}

allow {
    input.request.agent.sphere == "legal_compliance"
    input.request.action.type == "plan"
}

# Allow mutations with HITL
allow {
    input.request.agent.sphere == "legal_compliance"
    mutation_or_exec
    input.request.hitl.approved == true
}

# Explainability always required
deny_reason[msg] {
    input.request.agent.sphere == "legal_compliance"
    not input.request.explainability.provided
    msg := "LEGAL_COMPLIANCE_EXPLAINABILITY_MANDATORY"
}

# Audit level is always critical
audit_level := "critical"
