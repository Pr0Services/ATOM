# ============================================================================
# CHE·NU™ V69 — BUSINESS SPHERE POLICY
# ============================================================================
package che_nu.spheres.business

default allow := true

# Business sphere - standard governance
deny_reason[msg] {
    input.request.agent.sphere == "business"
    input.request.action.type == "export"
    input.request.action.data_classification == "internal"
    not input.request.hitl.approved
    msg := "BUSINESS_INTERNAL_EXPORT_REQUIRES_HITL"
}
