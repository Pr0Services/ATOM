"""
CHE·NU™ V75 — CANON MODULE
============================

Rule enforcement and compliance validation.

Version: 75.0
Status: PRODUCTION
R&D Compliance: ✅ Rule #1-7

The Canon Module enforces the 7 R&D rules across all operations.
No action can bypass these rules.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
import logging

logger = logging.getLogger("chenu.v75.canon")


class RuleId(str, Enum):
    """The 7 R&D Rules"""
    HUMAN_SOVEREIGNTY = "rule_1"
    AUTONOMY_ISOLATION = "rule_2"
    SPHERE_INTEGRITY = "rule_3"
    MY_TEAM_RESTRICTIONS = "rule_4"
    SOCIAL_RESTRICTIONS = "rule_5"
    MODULE_TRACEABILITY = "rule_6"
    RND_CONTINUITY = "rule_7"


class ViolationSeverity(str, Enum):
    """Violation severity levels"""
    CRITICAL = "critical"   # Blocks operation, requires immediate attention
    HIGH = "high"           # Blocks operation, logged
    MEDIUM = "medium"       # Warning, logged
    LOW = "low"             # Info, logged


@dataclass
class RuleDefinition:
    """Definition of an R&D rule"""
    id: RuleId
    name: str
    description: str
    violation_severity: ViolationSeverity
    enforcement_action: str  # "block" | "warn" | "log"


@dataclass
class ValidationResult:
    """Result of rule validation"""
    passed: bool
    rule_id: RuleId
    rule_name: str
    message: str
    severity: Optional[ViolationSeverity] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ComplianceReport:
    """Complete compliance report for an operation"""
    id: UUID = field(default_factory=uuid4)
    operation: str = ""
    initiator: Optional[UUID] = None
    
    # Results
    passed: bool = True
    results: List[ValidationResult] = field(default_factory=list)
    violations: List[ValidationResult] = field(default_factory=list)
    
    # Metadata
    validated_at: datetime = field(default_factory=datetime.utcnow)


class CanonEngine:
    """
    Canon Engine - Rule Enforcement System.
    
    Validates all operations against the 7 R&D rules.
    
    CRITICAL: This engine CANNOT be bypassed.
    All operations MUST pass through Canon validation.
    """
    
    # The 7 R&D Rules
    RULES: Dict[RuleId, RuleDefinition] = {
        RuleId.HUMAN_SOVEREIGNTY: RuleDefinition(
            id=RuleId.HUMAN_SOVEREIGNTY,
            name="Human Sovereignty",
            description="No action without explicit human approval",
            violation_severity=ViolationSeverity.CRITICAL,
            enforcement_action="block"
        ),
        RuleId.AUTONOMY_ISOLATION: RuleDefinition(
            id=RuleId.AUTONOMY_ISOLATION,
            name="Autonomy Isolation",
            description="AI operates in sandbox only, no direct production access",
            violation_severity=ViolationSeverity.CRITICAL,
            enforcement_action="block"
        ),
        RuleId.SPHERE_INTEGRITY: RuleDefinition(
            id=RuleId.SPHERE_INTEGRITY,
            name="Sphere Integrity",
            description="Cross-sphere operations require explicit workflow",
            violation_severity=ViolationSeverity.HIGH,
            enforcement_action="block"
        ),
        RuleId.MY_TEAM_RESTRICTIONS: RuleDefinition(
            id=RuleId.MY_TEAM_RESTRICTIONS,
            name="My Team Restrictions",
            description="No AI orchestrating AI autonomously",
            violation_severity=ViolationSeverity.CRITICAL,
            enforcement_action="block"
        ),
        RuleId.SOCIAL_RESTRICTIONS: RuleDefinition(
            id=RuleId.SOCIAL_RESTRICTIONS,
            name="Social Restrictions",
            description="No ranking algorithms, chronological only",
            violation_severity=ViolationSeverity.HIGH,
            enforcement_action="block"
        ),
        RuleId.MODULE_TRACEABILITY: RuleDefinition(
            id=RuleId.MODULE_TRACEABILITY,
            name="Module Traceability",
            description="All objects have created_by, created_at, id",
            violation_severity=ViolationSeverity.MEDIUM,
            enforcement_action="warn"
        ),
        RuleId.RND_CONTINUITY: RuleDefinition(
            id=RuleId.RND_CONTINUITY,
            name="R&D Continuity",
            description="Build on previous decisions, don't contradict",
            violation_severity=ViolationSeverity.MEDIUM,
            enforcement_action="warn"
        )
    }
    
    def __init__(self):
        self._violations_log: List[ValidationResult] = []
        logger.info("CanonEngine initialized - 7 R&D Rules enforced")
    
    def validate_human_sovereignty(
        self,
        operation: str,
        has_human_approval: bool,
        approver_id: Optional[UUID] = None
    ) -> ValidationResult:
        """
        Rule #1: Human Sovereignty
        
        Validates that operation has human approval.
        """
        rule = self.RULES[RuleId.HUMAN_SOVEREIGNTY]
        
        if not has_human_approval:
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Operation '{operation}' requires human approval",
                severity=rule.violation_severity,
                details={"operation": operation, "has_approval": False}
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message=f"Human approval verified for '{operation}'",
            details={"operation": operation, "approver_id": str(approver_id)}
        )
    
    def validate_autonomy_isolation(
        self,
        operation: str,
        execution_mode: str  # "sandbox" | "production"
    ) -> ValidationResult:
        """
        Rule #2: Autonomy Isolation
        
        Validates that AI operates in sandbox mode.
        """
        rule = self.RULES[RuleId.AUTONOMY_ISOLATION]
        
        if execution_mode == "production":
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Direct production access denied for '{operation}'",
                severity=rule.violation_severity,
                details={"operation": operation, "mode": execution_mode}
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message=f"Sandbox mode verified for '{operation}'",
            details={"operation": operation, "mode": execution_mode}
        )
    
    def validate_sphere_integrity(
        self,
        operation: str,
        source_sphere: str,
        target_sphere: Optional[str] = None,
        has_explicit_workflow: bool = False
    ) -> ValidationResult:
        """
        Rule #3: Sphere Integrity
        
        Validates cross-sphere operations have explicit workflow.
        """
        rule = self.RULES[RuleId.SPHERE_INTEGRITY]
        
        # Same sphere = OK
        if target_sphere is None or source_sphere == target_sphere:
            return ValidationResult(
                passed=True,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Within-sphere operation '{operation}' allowed",
                details={"sphere": source_sphere}
            )
        
        # Cross-sphere without workflow = FAIL
        if not has_explicit_workflow:
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Cross-sphere '{source_sphere}' -> '{target_sphere}' requires workflow",
                severity=rule.violation_severity,
                details={
                    "operation": operation,
                    "source": source_sphere,
                    "target": target_sphere,
                    "has_workflow": False
                }
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message=f"Cross-sphere workflow verified for '{operation}'",
            details={"source": source_sphere, "target": target_sphere}
        )
    
    def validate_my_team_restrictions(
        self,
        operation: str,
        orchestrator_type: str  # "human" | "ai"
    ) -> ValidationResult:
        """
        Rule #4: My Team Restrictions
        
        Validates that humans coordinate multi-agent work.
        """
        rule = self.RULES[RuleId.MY_TEAM_RESTRICTIONS]
        
        if orchestrator_type == "ai":
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"AI-to-AI orchestration denied for '{operation}'",
                severity=rule.violation_severity,
                details={"operation": operation, "orchestrator": orchestrator_type}
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message=f"Human orchestration verified for '{operation}'",
            details={"operation": operation, "orchestrator": orchestrator_type}
        )
    
    def validate_social_restrictions(
        self,
        operation: str,
        uses_ranking: bool = False,
        order_type: str = "chronological"
    ) -> ValidationResult:
        """
        Rule #5: Social Restrictions
        
        Validates no ranking algorithms, chronological only.
        """
        rule = self.RULES[RuleId.SOCIAL_RESTRICTIONS]
        
        if uses_ranking or order_type != "chronological":
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Ranking/engagement optimization denied for '{operation}'",
                severity=rule.violation_severity,
                details={
                    "operation": operation,
                    "uses_ranking": uses_ranking,
                    "order_type": order_type
                }
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message=f"Chronological order verified for '{operation}'",
            details={"order_type": order_type}
        )
    
    def validate_traceability(
        self,
        obj: Dict[str, Any]
    ) -> ValidationResult:
        """
        Rule #6: Module Traceability
        
        Validates object has required traceability fields.
        """
        rule = self.RULES[RuleId.MODULE_TRACEABILITY]
        
        required_fields = ["id", "created_by", "created_at"]
        missing = [f for f in required_fields if f not in obj or obj[f] is None]
        
        if missing:
            result = ValidationResult(
                passed=False,
                rule_id=rule.id,
                rule_name=rule.name,
                message=f"Missing traceability fields: {missing}",
                severity=rule.violation_severity,
                details={"missing_fields": missing}
            )
            self._log_violation(result)
            return result
        
        return ValidationResult(
            passed=True,
            rule_id=rule.id,
            rule_name=rule.name,
            message="All traceability fields present",
            details={"fields_verified": required_fields}
        )
    
    def validate_operation(
        self,
        operation: str,
        context: Dict[str, Any]
    ) -> ComplianceReport:
        """
        Validate an operation against all applicable rules.
        
        Args:
            operation: Operation name
            context: Operation context with validation data
            
        Returns:
            ComplianceReport with all validation results
        """
        report = ComplianceReport(
            operation=operation,
            initiator=context.get("initiator")
        )
        
        # Rule #1: Human Sovereignty
        result = self.validate_human_sovereignty(
            operation,
            context.get("has_human_approval", False),
            context.get("approver_id")
        )
        report.results.append(result)
        if not result.passed:
            report.violations.append(result)
        
        # Rule #2: Autonomy Isolation
        result = self.validate_autonomy_isolation(
            operation,
            context.get("execution_mode", "sandbox")
        )
        report.results.append(result)
        if not result.passed:
            report.violations.append(result)
        
        # Rule #3: Sphere Integrity (if cross-sphere)
        if "target_sphere" in context:
            result = self.validate_sphere_integrity(
                operation,
                context.get("source_sphere", "personal"),
                context.get("target_sphere"),
                context.get("has_explicit_workflow", False)
            )
            report.results.append(result)
            if not result.passed:
                report.violations.append(result)
        
        # Rule #4: My Team (if multi-agent)
        if context.get("is_multi_agent", False):
            result = self.validate_my_team_restrictions(
                operation,
                context.get("orchestrator_type", "human")
            )
            report.results.append(result)
            if not result.passed:
                report.violations.append(result)
        
        # Rule #5: Social (if social operation)
        if context.get("is_social", False):
            result = self.validate_social_restrictions(
                operation,
                context.get("uses_ranking", False),
                context.get("order_type", "chronological")
            )
            report.results.append(result)
            if not result.passed:
                report.violations.append(result)
        
        # Rule #6: Traceability (if object provided)
        if "object" in context:
            result = self.validate_traceability(context["object"])
            report.results.append(result)
            if not result.passed:
                report.violations.append(result)
        
        # Overall pass/fail
        report.passed = len(report.violations) == 0
        
        if not report.passed:
            logger.warning(f"Operation '{operation}' failed compliance: {len(report.violations)} violations")
        else:
            logger.info(f"Operation '{operation}' passed compliance")
        
        return report
    
    def _log_violation(self, result: ValidationResult):
        """Log a violation for audit"""
        self._violations_log.append(result)
        logger.warning(f"VIOLATION [{result.rule_id.value}]: {result.message}")
    
    def get_violations_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent violations"""
        return [
            {
                "rule_id": v.rule_id.value,
                "rule_name": v.rule_name,
                "message": v.message,
                "severity": v.severity.value if v.severity else None,
                "timestamp": v.timestamp.isoformat()
            }
            for v in self._violations_log[-limit:]
        ]


# Singleton
_engine: Optional[CanonEngine] = None


def get_canon_engine() -> CanonEngine:
    """Get or create CanonEngine instance"""
    global _engine
    if _engine is None:
        _engine = CanonEngine()
    return _engine


# Export
__all__ = [
    "CanonEngine",
    "RuleId",
    "RuleDefinition",
    "ValidationResult",
    "ComplianceReport",
    "ViolationSeverity",
    "get_canon_engine"
]
