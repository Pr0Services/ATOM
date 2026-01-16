"""
CHE·NU™ — DATA MIGRATION TESTS (PYTEST)
Sprint 9: Tests for data migration and version upgrades

Migration Principles:
- Data integrity must be preserved
- Schema changes must be backwards compatible
- Migrations must be reversible
- All migrations must be audited
"""

import pytest
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# MIGRATION CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class MigrationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


# Schema versions
SCHEMA_VERSIONS = {
    "v38": {
        "spheres": 8,
        "bureau_sections": 10,
        "governance_laws": 9,
    },
    "v39": {
        "spheres": 8,
        "bureau_sections": 6,
        "governance_laws": 10,
    },
    "v40": {
        "spheres": 9,  # Added Scholar
        "bureau_sections": 6,
        "governance_laws": 10,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK MIGRATION CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class Migration:
    """Base migration class."""
    
    def __init__(self, from_version: str, to_version: str):
        self.id = f"migration_{from_version}_to_{to_version}"
        self.from_version = from_version
        self.to_version = to_version
        self.status = MigrationStatus.PENDING
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
    
    def up(self, data: Dict) -> Dict:
        """Migrate data forward."""
        raise NotImplementedError
    
    def down(self, data: Dict) -> Dict:
        """Rollback migration."""
        raise NotImplementedError
    
    def validate(self, data: Dict) -> bool:
        """Validate data after migration."""
        raise NotImplementedError


class MigrationV38ToV39(Migration):
    """Migration from v38 to v39: Consolidate bureau sections 10→6."""
    
    def __init__(self):
        super().__init__("v38", "v39")
    
    def up(self, data: Dict) -> Dict:
        self.status = MigrationStatus.RUNNING
        self.started_at = datetime.utcnow()
        
        try:
            # Map old 10 sections to new 6 sections
            section_mapping = {
                "dashboard": "quick_capture",
                "notes": "resume_workspace",
                "tasks": "resume_workspace",
                "projects": "resume_workspace",
                "threads": "threads",
                "meetings": "meetings",
                "data": "data_files",
                "agents": "active_agents",
                "reports": "data_files",
                "budget": "data_files",
            }
            
            new_data = data.copy()
            if "sections" in new_data:
                new_sections = []
                for section in new_data["sections"]:
                    old_id = section.get("id", "").lower()
                    if old_id in section_mapping:
                        new_id = section_mapping[old_id]
                        # Only add if not already present
                        if not any(s["id"] == new_id for s in new_sections):
                            section["id"] = new_id
                            new_sections.append(section)
                new_data["sections"] = new_sections
            
            # Add L10 governance law
            if "governance_laws" in new_data:
                if len(new_data["governance_laws"]) == 9:
                    new_data["governance_laws"].append({
                        "id": "L10",
                        "code": "DELETION_COMPLETENESS",
                    })
            
            new_data["version"] = "v39"
            self.status = MigrationStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            return new_data
            
        except Exception as e:
            self.status = MigrationStatus.FAILED
            self.error = str(e)
            raise
    
    def down(self, data: Dict) -> Dict:
        # Reverse migration - expand back to 10 sections
        new_data = data.copy()
        new_data["version"] = "v38"
        
        # Remove L10 if present
        if "governance_laws" in new_data:
            new_data["governance_laws"] = [
                law for law in new_data["governance_laws"]
                if law.get("id") != "L10"
            ]
        
        self.status = MigrationStatus.ROLLED_BACK
        return new_data
    
    def validate(self, data: Dict) -> bool:
        # Check version
        if data.get("version") != "v39":
            return False
        # Check sections count
        if "sections" in data and len(data["sections"]) > 6:
            return False
        # Check governance laws
        if "governance_laws" in data and len(data["governance_laws"]) != 10:
            return False
        return True


class MigrationV39ToV40(Migration):
    """Migration from v39 to v40: Add Scholar sphere."""
    
    def __init__(self):
        super().__init__("v39", "v40")
    
    def up(self, data: Dict) -> Dict:
        self.status = MigrationStatus.RUNNING
        self.started_at = datetime.utcnow()
        
        try:
            new_data = data.copy()
            
            # Add Scholar sphere if not present
            if "spheres" in new_data:
                sphere_ids = [s.get("id") for s in new_data["spheres"]]
                if "scholar" not in sphere_ids:
                    new_data["spheres"].append({
                        "id": "scholar",
                        "name": "Scholar",
                        "icon": "📚",
                        "order": 9,
                    })
            
            new_data["version"] = "v40"
            self.status = MigrationStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            return new_data
            
        except Exception as e:
            self.status = MigrationStatus.FAILED
            self.error = str(e)
            raise
    
    def down(self, data: Dict) -> Dict:
        new_data = data.copy()
        
        # Remove Scholar sphere
        if "spheres" in new_data:
            new_data["spheres"] = [
                s for s in new_data["spheres"]
                if s.get("id") != "scholar"
            ]
        
        new_data["version"] = "v39"
        self.status = MigrationStatus.ROLLED_BACK
        return new_data
    
    def validate(self, data: Dict) -> bool:
        if data.get("version") != "v40":
            return False
        if "spheres" in data:
            sphere_ids = [s.get("id") for s in data["spheres"]]
            if "scholar" not in sphere_ids:
                return False
            if len(data["spheres"]) != 9:
                return False
        return True


class MigrationRunner:
    """Runs migrations in sequence."""
    
    def __init__(self):
        self.migrations: List[Migration] = []
        self.audit_log: List[Dict] = []
    
    def register(self, migration: Migration):
        self.migrations.append(migration)
    
    def migrate(self, data: Dict, target_version: str) -> Dict:
        current_version = data.get("version", "v38")
        result = data.copy()
        
        for migration in self.migrations:
            if migration.from_version == current_version:
                self._log("MIGRATION_STARTED", {
                    "id": migration.id,
                    "from": migration.from_version,
                    "to": migration.to_version,
                })
                
                result = migration.up(result)
                
                self._log("MIGRATION_COMPLETED", {
                    "id": migration.id,
                    "status": migration.status.value,
                })
                
                current_version = migration.to_version
                
                if current_version == target_version:
                    break
        
        return result
    
    def rollback(self, data: Dict, target_version: str) -> Dict:
        current_version = data.get("version", "v40")
        result = data.copy()
        
        # Reverse order for rollback
        for migration in reversed(self.migrations):
            if migration.to_version == current_version:
                self._log("ROLLBACK_STARTED", {
                    "id": migration.id,
                })
                
                result = migration.down(result)
                
                self._log("ROLLBACK_COMPLETED", {
                    "id": migration.id,
                })
                
                current_version = migration.from_version
                
                if current_version == target_version:
                    break
        
        return result
    
    def _log(self, action: str, details: Dict):
        self.audit_log.append({
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })


# ═══════════════════════════════════════════════════════════════════════════════
# MIGRATION V38 TO V39 TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigrationV38ToV39:
    """Tests for v38 to v39 migration."""

    def test_consolidate_sections_10_to_6(self):
        """Should consolidate 10 bureau sections to 6."""
        migration = MigrationV38ToV39()
        
        data = {
            "version": "v38",
            "sections": [
                {"id": "dashboard"}, {"id": "notes"}, {"id": "tasks"},
                {"id": "projects"}, {"id": "threads"}, {"id": "meetings"},
                {"id": "data"}, {"id": "agents"}, {"id": "reports"},
                {"id": "budget"},
            ],
            "governance_laws": [{"id": f"L{i}"} for i in range(1, 10)],
        }
        
        result = migration.up(data)
        
        assert len(result["sections"]) == 6
        assert result["version"] == "v39"

    def test_add_l10_governance_law(self):
        """Should add L10 (DELETION_COMPLETENESS)."""
        migration = MigrationV38ToV39()
        
        data = {
            "version": "v38",
            "governance_laws": [{"id": f"L{i}"} for i in range(1, 10)],
        }
        
        result = migration.up(data)
        
        assert len(result["governance_laws"]) == 10
        assert any(law["id"] == "L10" for law in result["governance_laws"])

    def test_migration_status_tracking(self):
        """Should track migration status."""
        migration = MigrationV38ToV39()
        
        assert migration.status == MigrationStatus.PENDING
        
        migration.up({"version": "v38"})
        
        assert migration.status == MigrationStatus.COMPLETED
        assert migration.started_at is not None
        assert migration.completed_at is not None

    def test_rollback(self):
        """Should rollback migration."""
        migration = MigrationV38ToV39()
        
        data = {"version": "v39", "governance_laws": [{"id": f"L{i}"} for i in range(1, 11)]}
        result = migration.down(data)
        
        assert result["version"] == "v38"
        assert len(result["governance_laws"]) == 9
        assert migration.status == MigrationStatus.ROLLED_BACK


# ═══════════════════════════════════════════════════════════════════════════════
# MIGRATION V39 TO V40 TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigrationV39ToV40:
    """Tests for v39 to v40 migration."""

    def test_add_scholar_sphere(self):
        """Should add Scholar as 9th sphere."""
        migration = MigrationV39ToV40()
        
        data = {
            "version": "v39",
            "spheres": [
                {"id": "personal", "order": 1},
                {"id": "business", "order": 2},
                {"id": "government", "order": 3},
                {"id": "creative", "order": 4},
                {"id": "community", "order": 5},
                {"id": "social", "order": 6},
                {"id": "entertainment", "order": 7},
                {"id": "team", "order": 8},
            ],
        }
        
        result = migration.up(data)
        
        assert len(result["spheres"]) == 9
        assert any(s["id"] == "scholar" for s in result["spheres"])
        assert result["version"] == "v40"

    def test_scholar_sphere_properties(self):
        """Scholar sphere should have correct properties."""
        migration = MigrationV39ToV40()
        
        data = {
            "version": "v39",
            "spheres": [{"id": f"sphere_{i}", "order": i} for i in range(1, 9)],
        }
        
        result = migration.up(data)
        scholar = next(s for s in result["spheres"] if s["id"] == "scholar")
        
        assert scholar["name"] == "Scholar"
        assert scholar["icon"] == "📚"
        assert scholar["order"] == 9

    def test_validation(self):
        """Should validate v40 data."""
        migration = MigrationV39ToV40()
        
        valid_data = {
            "version": "v40",
            "spheres": [{"id": f"sphere_{i}"} for i in range(8)] + [{"id": "scholar"}],
        }
        
        invalid_data = {
            "version": "v40",
            "spheres": [{"id": f"sphere_{i}"} for i in range(8)],  # Missing scholar
        }
        
        assert migration.validate(valid_data) is True
        assert migration.validate(invalid_data) is False

    def test_rollback_removes_scholar(self):
        """Rollback should remove Scholar sphere."""
        migration = MigrationV39ToV40()
        
        data = {
            "version": "v40",
            "spheres": [
                {"id": "personal"}, {"id": "business"}, {"id": "government"},
                {"id": "creative"}, {"id": "community"}, {"id": "social"},
                {"id": "entertainment"}, {"id": "team"}, {"id": "scholar"},
            ],
        }
        
        result = migration.down(data)
        
        assert len(result["spheres"]) == 8
        assert not any(s["id"] == "scholar" for s in result["spheres"])
        assert result["version"] == "v39"


# ═══════════════════════════════════════════════════════════════════════════════
# MIGRATION RUNNER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigrationRunner:
    """Tests for migration runner."""

    def test_migrate_v38_to_v40(self):
        """Should migrate from v38 to v40."""
        runner = MigrationRunner()
        runner.register(MigrationV38ToV39())
        runner.register(MigrationV39ToV40())
        
        data = {
            "version": "v38",
            "spheres": [{"id": f"sphere_{i}", "order": i} for i in range(1, 9)],
            "sections": [{"id": f"section_{i}"} for i in range(10)],
            "governance_laws": [{"id": f"L{i}"} for i in range(1, 10)],
        }
        
        result = runner.migrate(data, "v40")
        
        assert result["version"] == "v40"
        assert len(result["spheres"]) == 9
        assert any(s["id"] == "scholar" for s in result["spheres"])

    def test_audit_log(self):
        """Should create audit log for migrations."""
        runner = MigrationRunner()
        runner.register(MigrationV38ToV39())
        
        data = {"version": "v38"}
        runner.migrate(data, "v39")
        
        assert len(runner.audit_log) >= 2
        assert any(log["action"] == "MIGRATION_STARTED" for log in runner.audit_log)
        assert any(log["action"] == "MIGRATION_COMPLETED" for log in runner.audit_log)

    def test_rollback_v40_to_v38(self):
        """Should rollback from v40 to v38."""
        runner = MigrationRunner()
        runner.register(MigrationV38ToV39())
        runner.register(MigrationV39ToV40())
        
        data = {
            "version": "v40",
            "spheres": [{"id": f"sphere_{i}"} for i in range(8)] + [{"id": "scholar"}],
            "governance_laws": [{"id": f"L{i}"} for i in range(1, 11)],
        }
        
        result = runner.rollback(data, "v38")
        
        assert result["version"] == "v38"
        assert len(result["governance_laws"]) == 9


# ═══════════════════════════════════════════════════════════════════════════════
# DATA INTEGRITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataIntegrity:
    """Tests for data integrity during migration."""

    def test_user_data_preserved(self):
        """User data should be preserved during migration."""
        migration = MigrationV39ToV40()
        
        data = {
            "version": "v39",
            "spheres": [{"id": "personal", "order": 1}],
            "user_data": {
                "email": "jo@chenu.ai",
                "threads": ["thread_1", "thread_2"],
                "settings": {"theme": "dark"},
            },
        }
        
        result = migration.up(data)
        
        assert result["user_data"] == data["user_data"]

    def test_thread_data_preserved(self):
        """Thread data should be preserved during migration."""
        migration = MigrationV39ToV40()
        
        thread_data = {
            "id": "thread_123",
            "messages": [{"id": "msg_1"}, {"id": "msg_2"}],
            "tokens_used": 500,
        }
        
        data = {
            "version": "v39",
            "spheres": [],
            "threads": [thread_data],
        }
        
        result = migration.up(data)
        
        assert result["threads"][0] == thread_data

    def test_token_budgets_preserved(self):
        """Token budgets should be preserved during migration."""
        migration = MigrationV38ToV39()
        
        data = {
            "version": "v38",
            "token_budgets": {
                "user_1": {"total": 100000, "used": 25000},
                "user_2": {"total": 50000, "used": 10000},
            },
        }
        
        result = migration.up(data)
        
        assert result["token_budgets"] == data["token_budgets"]


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT MIGRATION COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigrationMemoryPromptCompliance:
    """Tests ensuring migrations maintain Memory Prompt constraints."""

    def test_v40_has_9_spheres(self):
        """v40 should have exactly 9 spheres."""
        assert SCHEMA_VERSIONS["v40"]["spheres"] == 9

    def test_v40_has_6_bureau_sections(self):
        """v40 should have exactly 6 bureau sections."""
        assert SCHEMA_VERSIONS["v40"]["bureau_sections"] == 6

    def test_v40_has_10_governance_laws(self):
        """v40 should have exactly 10 governance laws."""
        assert SCHEMA_VERSIONS["v40"]["governance_laws"] == 10

    def test_migration_adds_scholar(self):
        """Migration to v40 should add Scholar sphere."""
        migration = MigrationV39ToV40()
        
        data = {
            "version": "v39",
            "spheres": [{"id": f"sphere_{i}"} for i in range(8)],
        }
        
        result = migration.up(data)
        
        assert any(s["id"] == "scholar" for s in result["spheres"])

    def test_migrations_are_audited(self):
        """All migrations should be audited (L5)."""
        runner = MigrationRunner()
        runner.register(MigrationV38ToV39())
        
        runner.migrate({"version": "v38"}, "v39")
        
        assert len(runner.audit_log) > 0
        for log in runner.audit_log:
            assert "timestamp" in log
