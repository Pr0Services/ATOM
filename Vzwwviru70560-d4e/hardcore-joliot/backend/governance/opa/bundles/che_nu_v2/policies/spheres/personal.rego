# ============================================================================
# CHE·NU™ V69 — PERSONAL SPHERE POLICY
# ============================================================================
package che_nu.spheres.personal

# Personal sphere - sensitive data is common
default allow := true

# Personal data is sensitive by default - rely on core RULE 3
sensitive_by_default := true

deny_reason[msg] {
    input.request.agent.sphere == "personal"
    input.request.action.data_classification == "sensitive"
    not input.request.hitl.approved
    msg := "PERSONAL_SENSITIVE_REQUIRES_HITL"
}
