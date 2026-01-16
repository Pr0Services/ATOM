"""
CHE·NU V68 Privacy Guardian Module
Les Gardiens de la Vie Privee

GOVERNANCE COMPLIANCE:
- Rule #1: Sensitive data access requires APPROVAL
- Rule #4: NO AI-to-AI data sharing without human gate
- Rule #6: Full audit trail
"""

from .agents.privacy_guardian_agent import (
    PrivacyGuardianAgent,
    get_privacy_guardian_agent,
    DataCategory,
    DataType,
    ProcessingPurpose,
    ConsentStatus,
    ViolationType,
    AlertLevel,
    DataAccessRequest,
    DataSubjectRecord,
    PrivacyViolation,
    AnonymizationRule,
    RetentionPolicy,
    PrivacyMetrics,
)

__all__ = [
    "PrivacyGuardianAgent",
    "get_privacy_guardian_agent",
    "DataCategory",
    "DataType",
    "ProcessingPurpose",
    "ConsentStatus",
    "ViolationType",
    "AlertLevel",
    "DataAccessRequest",
    "DataSubjectRecord",
    "PrivacyViolation",
    "AnonymizationRule",
    "RetentionPolicy",
    "PrivacyMetrics",
]

__version__ = "68.0.0"
__module__ = "Privacy Guardian"
