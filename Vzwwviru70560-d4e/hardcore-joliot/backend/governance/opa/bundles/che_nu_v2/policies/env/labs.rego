# ============================================================================
# CHE·NU™ V69 — LABS ENVIRONMENT POLICY
# ============================================================================
# Package: che_nu.env.labs
# Version: 2.0.0
# Purpose: Maximum flexibility for experimentation
# ============================================================================

package che_nu.env.labs

# Labs is permissive by default - most restrictions come from core
default allow := true

# Labs-specific relaxations
allow_autogen := true
allow_non_deterministic := true
allow_experimental_features := true

# But still enforce critical rules
deny_reason[msg] {
    input.request.action.target == "xr"
    input.request.action.type == "write"
    msg := "XR_WRITE_DENIED_EVEN_IN_LABS"
}

deny_reason[msg] {
    input.request.action.target == "xr"
    input.request.action.type == "execute"
    msg := "XR_EXECUTE_DENIED_EVEN_IN_LABS"
}

# Labs must still be synthetic
deny_reason[msg] {
    input.request.resource.synthetic == false
    msg := "LABS_REQUIRES_SYNTHETIC_DATA"
}
