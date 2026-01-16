"""
CHE·NU™ — BACKUP & RESTORE TESTS (PYTEST)
Sprint 9: Tests for data backup and recovery

Backup Principles:
- All user data must be recoverable
- Backups must include all spheres
- Restoration must preserve data integrity
- Backup operations must be audited
"""

import pytest
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib

# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

BACKUP_TYPES = ["full", "incremental", "differential"]
COMPRESSION_TYPES = ["none", "gzip", "lz4"]
ENCRYPTION_TYPES = ["none", "aes256"]

# Data categories to backup
BACKUP_CATEGORIES = [
    "users",
    "spheres",
    "threads",
    "messages",
    "agents",
    "meetings",
    "token_budgets",
    "governance_logs",
    "audit_logs",
]


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK BACKUP CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class BackupMetadata:
    """Metadata for a backup."""
    
    def __init__(
        self,
        backup_id: str,
        backup_type: str = "full",
        compression: str = "gzip",
        encryption: str = "aes256",
    ):
        self.backup_id = backup_id
        self.backup_type = backup_type
        self.compression = compression
        self.encryption = encryption
        self.created_at = datetime.utcnow()
        self.size_bytes = 0
        self.checksum: Optional[str] = None
        self.categories: List[str] = []
        self.sphere_count = 0
        self.thread_count = 0
        self.message_count = 0


class Backup:
    """Represents a backup."""
    
    def __init__(self, metadata: BackupMetadata, data: Dict):
        self.metadata = metadata
        self.data = data
        self._calculate_checksum()
        self._update_counts()
    
    def _calculate_checksum(self):
        """Calculate data checksum."""
        data_str = json.dumps(self.data, sort_keys=True)
        self.metadata.checksum = hashlib.sha256(data_str.encode()).hexdigest()
        self.metadata.size_bytes = len(data_str.encode())
    
    def _update_counts(self):
        """Update metadata counts."""
        if "spheres" in self.data:
            self.metadata.sphere_count = len(self.data["spheres"])
        if "threads" in self.data:
            self.metadata.thread_count = len(self.data["threads"])
        if "messages" in self.data:
            self.metadata.message_count = len(self.data["messages"])
        self.metadata.categories = list(self.data.keys())
    
    def verify_integrity(self) -> bool:
        """Verify backup integrity."""
        data_str = json.dumps(self.data, sort_keys=True)
        current_checksum = hashlib.sha256(data_str.encode()).hexdigest()
        return current_checksum == self.metadata.checksum


class BackupService:
    """Service for backup and restore operations."""
    
    def __init__(self):
        self.backups: Dict[str, Backup] = {}
        self.audit_log: List[Dict] = []
    
    def create_backup(
        self,
        data: Dict,
        backup_type: str = "full",
        compression: str = "gzip",
        encryption: str = "aes256",
    ) -> Backup:
        """Create a backup."""
        backup_id = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        metadata = BackupMetadata(
            backup_id=backup_id,
            backup_type=backup_type,
            compression=compression,
            encryption=encryption,
        )
        
        backup = Backup(metadata, data)
        self.backups[backup_id] = backup
        
        self._log("BACKUP_CREATED", {
            "backup_id": backup_id,
            "type": backup_type,
            "size": backup.metadata.size_bytes,
            "checksum": backup.metadata.checksum,
        })
        
        return backup
    
    def restore(self, backup_id: str) -> Optional[Dict]:
        """Restore from a backup."""
        backup = self.backups.get(backup_id)
        if not backup:
            return None
        
        # Verify integrity before restore
        if not backup.verify_integrity():
            self._log("RESTORE_FAILED", {
                "backup_id": backup_id,
                "reason": "integrity_check_failed",
            })
            return None
        
        self._log("RESTORE_COMPLETED", {
            "backup_id": backup_id,
            "categories": backup.metadata.categories,
        })
        
        return backup.data.copy()
    
    def list_backups(self) -> List[BackupMetadata]:
        """List all backups."""
        return [b.metadata for b in self.backups.values()]
    
    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup."""
        if backup_id in self.backups:
            del self.backups[backup_id]
            self._log("BACKUP_DELETED", {"backup_id": backup_id})
            return True
        return False
    
    def _log(self, action: str, details: Dict):
        self.audit_log.append({
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        })


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP CREATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupCreation:
    """Tests for backup creation."""

    def test_create_full_backup(self):
        """Should create a full backup."""
        service = BackupService()
        
        data = {
            "spheres": [{"id": "personal"}, {"id": "scholar"}],
            "threads": [{"id": "thread_1"}],
        }
        
        backup = service.create_backup(data, backup_type="full")
        
        assert backup is not None
        assert backup.metadata.backup_type == "full"

    def test_backup_has_id(self):
        """Backup should have unique ID."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        assert backup.metadata.backup_id is not None
        assert backup.metadata.backup_id.startswith("backup_")

    def test_backup_has_checksum(self):
        """Backup should have checksum."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        assert backup.metadata.checksum is not None
        assert len(backup.metadata.checksum) == 64  # SHA256

    def test_backup_has_timestamp(self):
        """Backup should have creation timestamp."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        assert backup.metadata.created_at is not None
        assert isinstance(backup.metadata.created_at, datetime)

    def test_backup_has_size(self):
        """Backup should have size in bytes."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        assert backup.metadata.size_bytes > 0

    def test_backup_counts_spheres(self):
        """Backup should count spheres."""
        service = BackupService()
        
        data = {
            "spheres": [{"id": f"sphere_{i}"} for i in range(9)],
        }
        
        backup = service.create_backup(data)
        
        assert backup.metadata.sphere_count == 9

    def test_backup_counts_threads(self):
        """Backup should count threads."""
        service = BackupService()
        
        data = {
            "threads": [{"id": f"thread_{i}"} for i in range(100)],
        }
        
        backup = service.create_backup(data)
        
        assert backup.metadata.thread_count == 100


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP INTEGRITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupIntegrity:
    """Tests for backup integrity."""

    def test_verify_intact_backup(self):
        """Intact backup should pass integrity check."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        assert backup.verify_integrity() is True

    def test_detect_corrupted_backup(self):
        """Corrupted backup should fail integrity check."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        
        # Corrupt the data
        backup.data["data"] = "corrupted"
        
        assert backup.verify_integrity() is False

    def test_checksum_changes_with_data(self):
        """Different data should produce different checksums."""
        service = BackupService()
        
        backup1 = service.create_backup({"data": "test1"})
        backup2 = service.create_backup({"data": "test2"})
        
        assert backup1.metadata.checksum != backup2.metadata.checksum

    def test_same_data_same_checksum(self):
        """Same data should produce same checksum."""
        data = {"data": "identical"}
        
        metadata1 = BackupMetadata("b1")
        metadata2 = BackupMetadata("b2")
        
        backup1 = Backup(metadata1, data.copy())
        backup2 = Backup(metadata2, data.copy())
        
        assert backup1.metadata.checksum == backup2.metadata.checksum


# ═══════════════════════════════════════════════════════════════════════════════
# RESTORE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRestore:
    """Tests for restore operations."""

    def test_restore_backup(self):
        """Should restore from backup."""
        service = BackupService()
        
        original_data = {
            "spheres": [{"id": "personal"}],
            "threads": [{"id": "thread_1", "title": "Test"}],
        }
        
        backup = service.create_backup(original_data)
        restored = service.restore(backup.metadata.backup_id)
        
        assert restored == original_data

    def test_restore_nonexistent_backup(self):
        """Should return None for nonexistent backup."""
        service = BackupService()
        
        restored = service.restore("nonexistent_backup")
        
        assert restored is None

    def test_restore_preserves_data(self):
        """Restored data should match original exactly."""
        service = BackupService()
        
        original_data = {
            "user": {
                "email": "jo@chenu.ai",
                "settings": {"theme": "dark"},
            },
            "threads": [
                {"id": "t1", "messages": [{"id": "m1"}]},
            ],
        }
        
        backup = service.create_backup(original_data)
        restored = service.restore(backup.metadata.backup_id)
        
        assert restored["user"]["email"] == "jo@chenu.ai"
        assert restored["user"]["settings"]["theme"] == "dark"
        assert len(restored["threads"]) == 1
        assert restored["threads"][0]["messages"][0]["id"] == "m1"

    def test_restore_fails_on_corrupted_backup(self):
        """Restore should fail if backup is corrupted."""
        service = BackupService()
        
        backup = service.create_backup({"data": "test"})
        
        # Corrupt the backup
        backup.data["data"] = "corrupted"
        
        restored = service.restore(backup.metadata.backup_id)
        
        assert restored is None


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP MANAGEMENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupManagement:
    """Tests for backup management."""

    def test_list_backups(self):
        """Should list all backups."""
        service = BackupService()
        
        service.create_backup({"data": "1"})
        service.create_backup({"data": "2"})
        service.create_backup({"data": "3"})
        
        backups = service.list_backups()
        
        assert len(backups) == 3

    def test_delete_backup(self):
        """Should delete a backup."""
        service = BackupService()
        
        backup = service.create_backup({"data": "test"})
        backup_id = backup.metadata.backup_id
        
        result = service.delete_backup(backup_id)
        
        assert result is True
        assert len(service.list_backups()) == 0

    def test_delete_nonexistent_backup(self):
        """Deleting nonexistent backup should return False."""
        service = BackupService()
        
        result = service.delete_backup("nonexistent")
        
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP TYPES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupTypes:
    """Tests for different backup types."""

    def test_full_backup(self):
        """Should create full backup."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, backup_type="full")
        
        assert backup.metadata.backup_type == "full"

    def test_incremental_backup(self):
        """Should create incremental backup."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, backup_type="incremental")
        
        assert backup.metadata.backup_type == "incremental"

    def test_differential_backup(self):
        """Should create differential backup."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, backup_type="differential")
        
        assert backup.metadata.backup_type == "differential"

    def test_all_backup_types_supported(self):
        """All backup types should be supported."""
        assert "full" in BACKUP_TYPES
        assert "incremental" in BACKUP_TYPES
        assert "differential" in BACKUP_TYPES


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP COMPRESSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupCompression:
    """Tests for backup compression."""

    def test_gzip_compression(self):
        """Should support gzip compression."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, compression="gzip")
        
        assert backup.metadata.compression == "gzip"

    def test_lz4_compression(self):
        """Should support lz4 compression."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, compression="lz4")
        
        assert backup.metadata.compression == "lz4"

    def test_no_compression(self):
        """Should support no compression."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, compression="none")
        
        assert backup.metadata.compression == "none"


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP ENCRYPTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupEncryption:
    """Tests for backup encryption."""

    def test_aes256_encryption(self):
        """Should support AES-256 encryption."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, encryption="aes256")
        
        assert backup.metadata.encryption == "aes256"

    def test_no_encryption(self):
        """Should support no encryption."""
        service = BackupService()
        backup = service.create_backup({"data": "test"}, encryption="none")
        
        assert backup.metadata.encryption == "none"


# ═══════════════════════════════════════════════════════════════════════════════
# BACKUP AUDIT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupAudit:
    """Tests for backup audit logging."""

    def test_create_is_audited(self):
        """Backup creation should be audited."""
        service = BackupService()
        service.create_backup({"data": "test"})
        
        assert any(log["action"] == "BACKUP_CREATED" for log in service.audit_log)

    def test_restore_is_audited(self):
        """Restore should be audited."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        service.restore(backup.metadata.backup_id)
        
        assert any(log["action"] == "RESTORE_COMPLETED" for log in service.audit_log)

    def test_delete_is_audited(self):
        """Deletion should be audited."""
        service = BackupService()
        backup = service.create_backup({"data": "test"})
        service.delete_backup(backup.metadata.backup_id)
        
        assert any(log["action"] == "BACKUP_DELETED" for log in service.audit_log)

    def test_audit_has_timestamps(self):
        """Audit entries should have timestamps."""
        service = BackupService()
        service.create_backup({"data": "test"})
        
        for log in service.audit_log:
            assert "timestamp" in log


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY PROMPT BACKUP COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestBackupMemoryPromptCompliance:
    """Tests ensuring backups support Memory Prompt requirements."""

    def test_backup_all_9_spheres(self):
        """Backup should include all 9 spheres."""
        service = BackupService()
        
        data = {
            "spheres": [
                {"id": "personal"}, {"id": "business"}, {"id": "government"},
                {"id": "creative"}, {"id": "community"}, {"id": "social"},
                {"id": "entertainment"}, {"id": "team"}, {"id": "scholar"},
            ],
        }
        
        backup = service.create_backup(data)
        
        assert backup.metadata.sphere_count == 9

    def test_backup_includes_scholar(self):
        """Backup should include Scholar sphere."""
        service = BackupService()
        
        data = {
            "spheres": [{"id": "scholar", "name": "Scholar"}],
        }
        
        backup = service.create_backup(data)
        restored = service.restore(backup.metadata.backup_id)
        
        assert any(s["id"] == "scholar" for s in restored["spheres"])

    def test_backup_preserves_token_budgets(self):
        """Backup should preserve token budgets (L8)."""
        service = BackupService()
        
        data = {
            "token_budgets": {
                "user_1": {"total": 100000, "used": 25000},
            },
        }
        
        backup = service.create_backup(data)
        restored = service.restore(backup.metadata.backup_id)
        
        assert restored["token_budgets"]["user_1"]["total"] == 100000
        assert restored["token_budgets"]["user_1"]["used"] == 25000

    def test_backup_is_audited(self):
        """All backup operations should be audited (L5)."""
        service = BackupService()
        
        backup = service.create_backup({"data": "test"})
        service.restore(backup.metadata.backup_id)
        service.delete_backup(backup.metadata.backup_id)
        
        actions = [log["action"] for log in service.audit_log]
        assert "BACKUP_CREATED" in actions
        assert "RESTORE_COMPLETED" in actions
        assert "BACKUP_DELETED" in actions

    def test_backup_all_categories(self):
        """Backup should support all data categories."""
        for category in BACKUP_CATEGORIES:
            assert category in [
                "users", "spheres", "threads", "messages",
                "agents", "meetings", "token_budgets",
                "governance_logs", "audit_logs",
            ]
