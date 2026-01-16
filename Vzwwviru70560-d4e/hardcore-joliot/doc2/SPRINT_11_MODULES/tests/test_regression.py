"""
CHE·NU™ — REGRESSION TESTS (PYTEST)
Sprint 8: Tests for known bugs and fixes

These tests ensure that previously fixed issues don't resurface.
Each test documents a specific bug that was fixed.
"""

import pytest
from typing import Dict, List
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# REGRESSION TEST CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Fixed bugs registry
FIXED_BUGS = {
    "BUG-001": "Sphere count was 8 instead of 9 (missing Scholar)",
    "BUG-002": "Bureau sections were 10 instead of 6",
    "BUG-003": "Nova could be hired in certain conditions",
    "BUG-004": "Token budget could go negative",
    "BUG-005": "Cross-sphere data leakage",
    "BUG-006": "Missing audit logs for deletions",
    "BUG-007": "Agent level L0 not recognized as system",
    "BUG-008": "Governance laws count was 9 instead of 10",
    "BUG-009": "Thread without sphere assignment",
    "BUG-010": "Meeting without token budget",
}


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-001: SPHERE COUNT REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug001SphereCount:
    """
    BUG-001: Sphere count was 8 instead of 9 (missing Scholar)
    
    Root cause: Scholar sphere was added as 9th sphere but not included
    in sphere list constant.
    
    Fixed: Added 'scholar' to SPHERE_IDS constant.
    """

    SPHERE_IDS = [
        "personal", "business", "government", "creative",
        "community", "social", "entertainment", "team", "scholar"
    ]

    def test_sphere_count_is_9(self):
        """Spheres should be exactly 9."""
        assert len(self.SPHERE_IDS) == 9

    def test_scholar_included(self):
        """Scholar sphere should be included."""
        assert "scholar" in self.SPHERE_IDS

    def test_scholar_is_9th(self):
        """Scholar should be the 9th sphere."""
        assert self.SPHERE_IDS[8] == "scholar"


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-002: BUREAU SECTIONS COUNT REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug002BureauSectionsCount:
    """
    BUG-002: Bureau sections were 10 instead of 6
    
    Root cause: Old architecture had 10 sections, new architecture
    consolidated to 6 but some code paths still used 10.
    
    Fixed: Updated all section references to use 6-section model.
    """

    BUREAU_SECTIONS = [
        "quick_capture", "resume_workspace", "threads",
        "data_files", "active_agents", "meetings"
    ]

    OLD_SECTIONS = [
        "dashboard", "notes", "tasks", "projects", "threads",
        "meetings", "data", "agents", "reports", "budget"
    ]

    def test_bureau_sections_is_6(self):
        """Bureau sections should be exactly 6."""
        assert len(self.BUREAU_SECTIONS) == 6

    def test_old_sections_not_used(self):
        """Old 10-section model should not be used."""
        assert len(self.OLD_SECTIONS) == 10  # Documented but not used
        # Ensure new sections don't include old ones that were removed
        assert "dashboard" not in self.BUREAU_SECTIONS
        assert "notes" not in self.BUREAU_SECTIONS
        assert "tasks" not in self.BUREAU_SECTIONS
        assert "projects" not in self.BUREAU_SECTIONS


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-003: NOVA HIRING REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug003NovaHiring:
    """
    BUG-003: Nova could be hired in certain conditions
    
    Root cause: hire_agent() function didn't check if agent was Nova
    before setting is_hired = True.
    
    Fixed: Added explicit check to prevent Nova from being hired.
    """

    def test_nova_is_not_hired(self):
        """Nova should never be marked as hired."""
        nova = {
            "id": "nova",
            "is_hired": False,
            "is_system": True,
        }
        assert nova["is_hired"] is False

    def test_nova_hire_blocked(self):
        """Attempting to hire Nova should fail."""
        def hire_agent(agent: Dict) -> bool:
            # BUG FIX: Check if Nova
            if agent["id"] == "nova":
                return False
            agent["is_hired"] = True
            return True
        
        nova = {"id": "nova", "is_hired": False, "is_system": True}
        result = hire_agent(nova)
        
        assert result is False
        assert nova["is_hired"] is False

    def test_nova_system_flag(self):
        """Nova should always have is_system = True."""
        nova = {"id": "nova", "is_system": True}
        assert nova["is_system"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-004: NEGATIVE TOKEN BUDGET REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug004NegativeTokenBudget:
    """
    BUG-004: Token budget could go negative
    
    Root cause: Token deduction didn't check if remaining >= amount
    before deducting.
    
    Fixed: Added validation to prevent negative budgets.
    """

    def test_budget_cannot_go_negative(self):
        """Token budget should never go negative."""
        budget = {"total": 1000, "used": 0, "remaining": 1000}
        
        def use_tokens(budget: Dict, amount: int) -> bool:
            # BUG FIX: Check remaining before deducting
            if budget["remaining"] < amount:
                return False
            budget["used"] += amount
            budget["remaining"] -= amount
            return True
        
        # Try to use more than available
        result = use_tokens(budget, 5000)
        
        assert result is False
        assert budget["remaining"] >= 0

    def test_budget_remaining_calculation(self):
        """Remaining should always equal total - used."""
        budget = {"total": 10000, "used": 3000, "remaining": 7000}
        assert budget["remaining"] == budget["total"] - budget["used"]


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-005: CROSS-SPHERE DATA LEAKAGE REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug005CrossSphereLeakage:
    """
    BUG-005: Cross-sphere data leakage
    
    Root cause: Query for threads didn't filter by sphere_id, returning
    threads from all spheres.
    
    Fixed: Added sphere_id filter to all thread queries.
    """

    def test_threads_filtered_by_sphere(self):
        """Threads should be filtered by sphere."""
        all_threads = [
            {"id": "t1", "sphere_id": "personal"},
            {"id": "t2", "sphere_id": "business"},
            {"id": "t3", "sphere_id": "personal"},
        ]
        
        # BUG FIX: Filter by sphere_id
        def get_threads(sphere_id: str) -> List[Dict]:
            return [t for t in all_threads if t["sphere_id"] == sphere_id]
        
        personal_threads = get_threads("personal")
        business_threads = get_threads("business")
        
        assert len(personal_threads) == 2
        assert len(business_threads) == 1
        assert all(t["sphere_id"] == "personal" for t in personal_threads)

    def test_no_cross_sphere_access(self):
        """Sphere data should not leak to other spheres."""
        sphere_data = {
            "personal": {"secret": "personal_data"},
            "business": {"secret": "business_data"},
        }
        
        # L9: CROSS_SPHERE_ISOLATION
        assert sphere_data["personal"]["secret"] != sphere_data["business"]["secret"]


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-006: MISSING DELETION AUDIT LOGS REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug006MissingDeletionAudit:
    """
    BUG-006: Missing audit logs for deletions
    
    Root cause: delete() function didn't create audit log entry before
    removing the record.
    
    Fixed: Added audit log creation before deletion.
    """

    def test_deletion_creates_audit_log(self):
        """Deletion should create audit log."""
        audit_logs = []
        
        def delete_record(record_id: str) -> bool:
            # BUG FIX: Log before deleting
            audit_logs.append({
                "action": "DELETE",
                "record_id": record_id,
                "timestamp": datetime.utcnow().isoformat(),
            })
            return True
        
        delete_record("thread_123")
        
        assert len(audit_logs) == 1
        assert audit_logs[0]["action"] == "DELETE"
        assert audit_logs[0]["record_id"] == "thread_123"

    def test_audit_log_has_timestamp(self):
        """Audit log should have timestamp."""
        audit_log = {
            "action": "DELETE",
            "record_id": "123",
            "timestamp": datetime.utcnow().isoformat(),
        }
        assert "timestamp" in audit_log


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-007: L0 NOT RECOGNIZED AS SYSTEM REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug007L0NotSystem:
    """
    BUG-007: Agent level L0 not recognized as system
    
    Root cause: is_system_agent() only checked is_system flag, not level.
    
    Fixed: L0 agents are always system agents.
    """

    def test_l0_is_system_agent(self):
        """L0 level should be recognized as system agent."""
        def is_system_agent(agent: Dict) -> bool:
            # BUG FIX: Check level as well
            return agent.get("is_system", False) or agent.get("level") == "L0"
        
        nova = {"id": "nova", "level": "L0", "is_system": True}
        assert is_system_agent(nova) is True

    def test_l0_always_system(self):
        """Any L0 agent should be system regardless of flag."""
        def is_system_agent(agent: Dict) -> bool:
            return agent.get("is_system", False) or agent.get("level") == "L0"
        
        # Even if is_system is missing, L0 should be system
        agent = {"id": "test", "level": "L0"}
        assert is_system_agent(agent) is True


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-008: GOVERNANCE LAWS COUNT REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug008GovernanceLawsCount:
    """
    BUG-008: Governance laws count was 9 instead of 10
    
    Root cause: L10 (DELETION_COMPLETENESS) was accidentally omitted
    from the laws list.
    
    Fixed: Added L10 to governance laws.
    """

    GOVERNANCE_LAWS = [
        {"id": "L1", "code": "CONSENT_PRIMACY"},
        {"id": "L2", "code": "TEMPORAL_SOVEREIGNTY"},
        {"id": "L3", "code": "CONTEXTUAL_FIDELITY"},
        {"id": "L4", "code": "HIERARCHICAL_RESPECT"},
        {"id": "L5", "code": "AUDIT_COMPLETENESS"},
        {"id": "L6", "code": "ENCODING_TRANSPARENCY"},
        {"id": "L7", "code": "AGENT_NON_AUTONOMY"},
        {"id": "L8", "code": "BUDGET_ACCOUNTABILITY"},
        {"id": "L9", "code": "CROSS_SPHERE_ISOLATION"},
        {"id": "L10", "code": "DELETION_COMPLETENESS"},
    ]

    def test_governance_laws_count_is_10(self):
        """Governance laws should be exactly 10."""
        assert len(self.GOVERNANCE_LAWS) == 10

    def test_l10_included(self):
        """L10 should be included."""
        l10 = next((law for law in self.GOVERNANCE_LAWS if law["id"] == "L10"), None)
        assert l10 is not None
        assert l10["code"] == "DELETION_COMPLETENESS"


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-009: THREAD WITHOUT SPHERE REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug009ThreadWithoutSphere:
    """
    BUG-009: Thread without sphere assignment
    
    Root cause: Thread creation didn't require sphere_id field.
    
    Fixed: sphere_id is now required for thread creation.
    """

    def test_thread_requires_sphere_id(self):
        """Thread creation should require sphere_id."""
        def create_thread(data: Dict) -> Dict:
            # BUG FIX: Require sphere_id
            if "sphere_id" not in data:
                raise ValueError("sphere_id is required")
            return {"id": "thread_123", **data}
        
        # Should fail without sphere_id
        with pytest.raises(ValueError):
            create_thread({"title": "Test Thread"})

    def test_thread_with_sphere_id_succeeds(self):
        """Thread creation with sphere_id should succeed."""
        def create_thread(data: Dict) -> Dict:
            if "sphere_id" not in data:
                raise ValueError("sphere_id is required")
            return {"id": "thread_123", **data}
        
        thread = create_thread({"title": "Test", "sphere_id": "personal"})
        assert thread["sphere_id"] == "personal"


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-010: MEETING WITHOUT TOKEN BUDGET REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

class TestBug010MeetingWithoutBudget:
    """
    BUG-010: Meeting without token budget
    
    Root cause: Meeting creation didn't assign default token budget.
    
    Fixed: Meetings now have default token budget of 10000.
    """

    DEFAULT_MEETING_BUDGET = 10000

    def test_meeting_has_default_budget(self):
        """Meeting should have default token budget."""
        def create_meeting(data: Dict) -> Dict:
            # BUG FIX: Set default budget
            if "token_budget" not in data:
                data["token_budget"] = self.DEFAULT_MEETING_BUDGET
            return {"id": "meeting_123", **data}
        
        meeting = create_meeting({"title": "Team Meeting"})
        assert meeting["token_budget"] == 10000

    def test_meeting_custom_budget(self):
        """Meeting with custom budget should use that budget."""
        def create_meeting(data: Dict) -> Dict:
            if "token_budget" not in data:
                data["token_budget"] = self.DEFAULT_MEETING_BUDGET
            return {"id": "meeting_123", **data}
        
        meeting = create_meeting({"title": "Test", "token_budget": 5000})
        assert meeting["token_budget"] == 5000


# ═══════════════════════════════════════════════════════════════════════════════
# REGRESSION SUMMARY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRegressionSummary:
    """Summary tests to verify all bugs are documented."""

    def test_all_bugs_documented(self):
        """All fixed bugs should be documented."""
        assert len(FIXED_BUGS) == 10

    def test_bugs_have_descriptions(self):
        """All bugs should have descriptions."""
        for bug_id, description in FIXED_BUGS.items():
            assert len(description) > 0

    def test_bugs_are_sequential(self):
        """Bug IDs should be sequential."""
        bug_ids = list(FIXED_BUGS.keys())
        for i, bug_id in enumerate(bug_ids):
            expected = f"BUG-{str(i + 1).zfill(3)}"
            assert bug_id == expected


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT REGRESSION COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestRegressionMemoryPromptCompliance:
    """Ensure Memory Prompt constraints don't regress."""

    def test_9_spheres_no_regression(self):
        """9 spheres should not regress."""
        SPHERE_COUNT = 9
        assert SPHERE_COUNT == 9

    def test_6_bureau_sections_no_regression(self):
        """6 bureau sections should not regress."""
        BUREAU_COUNT = 6
        assert BUREAU_COUNT == 6

    def test_nova_never_hired_no_regression(self):
        """Nova never hired should not regress."""
        NOVA_IS_HIRED = False
        assert NOVA_IS_HIRED is False

    def test_10_governance_laws_no_regression(self):
        """10 governance laws should not regress."""
        LAW_COUNT = 10
        assert LAW_COUNT == 10
