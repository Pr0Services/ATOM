# ============================================================================
# CHE·NU™ V69 — EXPORTS GOVERNANCE POLICY
# ============================================================================
# Package: che_nu.exports
# Version: 2.0.0
# Purpose: Rules for data exports and external transfers
# Principle: HUMAN APPROVAL REQUIRED - No automated exports
# ============================================================================

package che_nu.exports

import data.che_nu.config
import data.che_nu.base

# ============================================================================
# DEFAULT
# ============================================================================

default allow := false
default require_human_approval := false

# ============================================================================
# EXPORT RULES
# ============================================================================

# Exports ALWAYS require human approval by default
require_human_approval {
    input.request.action.type == "EXPORT_ARTIFACT"
    config.exports_require_human == true
}

require_human_approval {
    input.request.action.type == "export"
    config.exports_require_human == true
}

# Allow export only with valid HITL approval token
allow {
    input.request.action.type == "EXPORT_ARTIFACT"
    require_human_approval
    valid_human_approval
}

allow {
    input.request.action.type == "export"
    require_human_approval
    valid_human_approval
}

# Allow export if human approval not required (rare config)
allow {
    input.request.action.type == "EXPORT_ARTIFACT"
    not config.exports_require_human
    input.request.resource.synthetic == true
}

# ============================================================================
# HUMAN APPROVAL VALIDATION
# ============================================================================

valid_human_approval {
    input.request.hitl.approved == true
    input.request.hitl.approver_id != ""
    approval_not_expired
}

approval_not_expired {
    not input.request.hitl.expires_at
}

approval_not_expired {
    input.request.hitl.expires_at > time.now_ns()
}

# ============================================================================
# DENY REASONS
# ============================================================================

deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    require_human_approval
    not valid_human_approval
    msg := "EXPORT_REQUIRES_HUMAN_APPROVAL"
}

deny_reason[msg] {
    input.request.action.type == "export"
    require_human_approval
    not valid_human_approval
    msg := "EXPORT_REQUIRES_HUMAN_APPROVAL"
}

deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.resource.synthetic == false
    msg := "CANNOT_EXPORT_REAL_DATA"
}

# ============================================================================
# EXPORT DESTINATION RULES
# ============================================================================

# Block exports to unknown destinations
deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.resource.destination != ""
    not destination_allowed
    msg := "EXPORT_DESTINATION_NOT_ALLOWED"
}

destination_allowed {
    allowed_destinations := ["local", "signed_download", "erp_connector", "pm_connector"]
    input.request.resource.destination == allowed_destinations[_]
}

# External destinations require additional approval
deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.resource.destination == "external"
    not input.request.hitl.external_approved
    msg := "EXTERNAL_EXPORT_REQUIRES_ADDITIONAL_APPROVAL"
}

# ============================================================================
# EXPORT FORMAT RULES
# ============================================================================

# Supported export formats
supported_format {
    formats := ["json", "pdf", "csv", "xlsx", "xr_pack"]
    input.request.resource.format == formats[_]
}

deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    not supported_format
    msg := sprintf("UNSUPPORTED_EXPORT_FORMAT_%s", [input.request.resource.format])
}

# ============================================================================
# EXPORT SIZE LIMITS
# ============================================================================

# Max export size (configurable, default 100MB)
max_export_size := config.max_export_size_bytes {
    config.max_export_size_bytes
}

max_export_size := 104857600 {  # 100MB default
    not config.max_export_size_bytes
}

deny_reason[msg] {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.resource.size_bytes > max_export_size
    msg := sprintf("EXPORT_SIZE_EXCEEDS_LIMIT_%d_BYTES", [max_export_size])
}

# ============================================================================
# EXPORT AUDIT REQUIREMENTS
# ============================================================================

# All exports must be audited
required_controls[ctl] {
    input.request.action.type == "EXPORT_ARTIFACT"
    ctl := "AUDIT_EXPORT_REQUIRED"
}

required_controls[ctl] {
    input.request.action.type == "export"
    ctl := "AUDIT_EXPORT_REQUIRED"
}

# Sensitive exports require elevated audit
audit_level := "critical" {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.action.data_classification == "sensitive"
}

audit_level := "elevated" {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.action.data_classification != "sensitive"
}

# ============================================================================
# EXPORT WATERMARKING
# ============================================================================

# Watermarking required for non-internal exports
require_watermark {
    input.request.action.type == "EXPORT_ARTIFACT"
    input.request.resource.visibility != "internal"
}

deny_reason[msg] {
    require_watermark
    not input.request.resource.watermark_applied
    msg := "EXPORT_REQUIRES_WATERMARK"
}

# ============================================================================
# RESULT
# ============================================================================

result := {
    "allow": allow,
    "require_human_approval": require_human_approval,
    "deny_reasons": deny_reason,
    "required_controls": required_controls,
    "audit_level": audit_level,
    "export_format": input.request.resource.format,
    "destination": input.request.resource.destination,
    "trace_id": base.trace_id
}
