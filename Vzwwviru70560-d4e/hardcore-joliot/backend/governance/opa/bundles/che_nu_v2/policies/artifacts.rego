# ============================================================================
# CHE·NU™ V69 — ARTIFACTS GOVERNANCE POLICY
# ============================================================================
# Package: che_nu.artifacts
# Version: 2.0.0
# Purpose: Rules for XR packs, documents, and generated artifacts
# Principle: XR READ-ONLY - No writes to XR artifacts
# ============================================================================

package che_nu.artifacts

import data.che_nu.config
import data.che_nu.base

# ============================================================================
# DEFAULT
# ============================================================================

default allow := false

# ============================================================================
# READ ARTIFACT RULES
# ============================================================================

# Allow reading artifacts with XR read-only mode
allow {
    input.request.action.type == "READ_ARTIFACT"
    input.request.context.xr_read_only == true
}

# Allow reading own tenant's artifacts
allow {
    input.request.action.type == "READ_ARTIFACT"
    input.request.tenant.id != ""
    artifact_belongs_to_tenant
}

# Allow reading public artifacts
allow {
    input.request.action.type == "READ_ARTIFACT"
    input.request.resource.visibility == "public"
}

# ============================================================================
# HELPERS
# ============================================================================

artifact_belongs_to_tenant {
    input.request.resource.tenant_id == input.request.tenant.id
}

is_xr_artifact {
    input.request.resource.type == "xr_pack"
}

is_xr_artifact {
    input.request.resource.type == "replay_data"
}

is_xr_artifact {
    input.request.resource.type == "heatmap"
}

is_xr_artifact {
    input.request.resource.type == "diff"
}

# ============================================================================
# XR READ-ONLY ENFORCEMENT
# ============================================================================

deny_reason[msg] {
    is_xr_artifact
    input.request.action.type == "write"
    msg := "XR_ARTIFACT_READ_ONLY_NO_WRITE"
}

deny_reason[msg] {
    is_xr_artifact
    input.request.action.type == "delete"
    msg := "XR_ARTIFACT_READ_ONLY_NO_DELETE"
}

deny_reason[msg] {
    is_xr_artifact
    input.request.action.type == "execute"
    msg := "XR_ARTIFACT_READ_ONLY_NO_EXECUTE"
}

# ============================================================================
# ARTIFACT SIGNATURE VERIFICATION
# ============================================================================

# Unsigned artifacts cannot be trusted
deny_reason[msg] {
    input.request.action.type == "READ_ARTIFACT"
    input.request.resource.signature_required == true
    not input.request.resource.signature_valid
    msg := "ARTIFACT_SIGNATURE_INVALID"
}

# Verify Ed25519 signatures
signature_valid {
    input.request.resource.signature_algorithm == "ed25519"
    input.request.resource.signature_valid == true
}

# Verify hybrid PQC signatures (future)
signature_valid {
    input.request.resource.signature_algorithm == "hybrid_ed25519_dilithium"
    input.request.resource.signature_valid == true
    base.pqc_enabled
}

# ============================================================================
# ARTIFACT INTEGRITY
# ============================================================================

# Checksum verification required for critical artifacts
deny_reason[msg] {
    input.request.resource.integrity_check_required == true
    not input.request.resource.checksum_valid
    msg := "ARTIFACT_CHECKSUM_INVALID"
}

# Version consistency check
deny_reason[msg] {
    input.request.action.type == "READ_ARTIFACT"
    input.request.resource.version_mismatch == true
    msg := "ARTIFACT_VERSION_MISMATCH"
}

# ============================================================================
# XR PACK SPECIFIC RULES
# ============================================================================

# XR packs must have valid manifest
deny_reason[msg] {
    input.request.resource.type == "xr_pack"
    not input.request.resource.manifest_valid
    msg := "XR_PACK_MANIFEST_INVALID"
}

# XR packs must be synthetic
deny_reason[msg] {
    input.request.resource.type == "xr_pack"
    input.request.resource.synthetic == false
    msg := "XR_PACK_MUST_BE_SYNTHETIC"
}

# Heatmap requires valid signals
deny_reason[msg] {
    input.request.resource.type == "heatmap"
    not input.request.resource.signals_valid
    msg := "HEATMAP_REQUIRES_VALID_SIGNALS"
}

# ============================================================================
# EXPLAIN ON-DEMAND
# ============================================================================

# Allow explain requests for visible ranges only
allow {
    input.request.action.type == "REQUEST_EXPLAIN"
    input.request.resource.synthetic == true
    valid_explain_range
}

valid_explain_range {
    input.request.resource.explain_range.start >= 0
    input.request.resource.explain_range.end > input.request.resource.explain_range.start
    range_size := input.request.resource.explain_range.end - input.request.resource.explain_range.start
    range_size <= 1000  # Max 1000 steps per explain request
}

deny_reason[msg] {
    input.request.action.type == "REQUEST_EXPLAIN"
    not valid_explain_range
    msg := "EXPLAIN_RANGE_INVALID_OR_TOO_LARGE"
}

# ============================================================================
# RESULT
# ============================================================================

result := {
    "allow": allow,
    "deny_reasons": deny_reason,
    "artifact_type": input.request.resource.type,
    "signature_valid": signature_valid,
    "trace_id": base.trace_id
}
