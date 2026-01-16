# ============================================================================
# CHE·NU™ V69 — CREATIVE SPHERE POLICY
# ============================================================================
package che_nu.spheres.creative

# Creative sphere - more permissive for experimentation
default allow := true

# Still enforce XR read-only
deny_reason[msg] {
    input.request.agent.sphere == "creative"
    input.request.action.target == "xr"
    input.request.action.type == "write"
    msg := "CREATIVE_XR_STILL_READ_ONLY"
}
