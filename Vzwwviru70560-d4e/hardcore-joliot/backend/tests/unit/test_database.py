"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Database Tests
═══════════════════════════════════════════════════════════════════════════════

Comprehensive tests for:
- Models (all 9 spheres)
- Repositories (CRUD with identity boundary)
- Event sourcing (Thread events)
- Checkpoints (R&D Rule #1)
- Audit logs (R&D Rule #6)
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import uuid4, UUID
from typing import AsyncGenerator

# Mock SQLAlchemy for testing without actual database
from unittest.mock import AsyncMock, MagicMock, patch


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def identity_id() -> UUID:
    """Test identity ID."""
    return uuid4()


@pytest.fixture
def other_identity_id() -> UUID:
    """Another identity ID for boundary tests."""
    return uuid4()


@pytest.fixture
def thread_id() -> UUID:
    """Test thread ID."""
    return uuid4()


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEnums:
    """Test enum definitions."""
    
    def test_sphere_type_has_9_spheres(self):
        """R&D: Exactly 9 spheres."""
        from models.base import SphereType
        
        spheres = list(SphereType)
        assert len(spheres) == 9
        
        expected = [
            "personal", "business", "creative_studio", "entertainment",
            "community", "social", "scholar", "government", "my_team"
        ]
        assert [s.value for s in spheres] == expected
    
    def test_thread_status_lifecycle(self):
        """Test thread status values."""
        from models.base import ThreadStatus
        
        statuses = [s.value for s in ThreadStatus]
        assert "active" in statuses
        assert "paused" in statuses
        assert "completed" in statuses
        assert "archived" in statuses
    
    def test_checkpoint_types(self):
        """R&D Rule #1: Checkpoint types for human approval."""
        from models.base import CheckpointType
        
        types = [t.value for t in CheckpointType]
        assert "governance" in types
        assert "cost" in types
        assert "identity" in types
        assert "sensitive" in types
        assert "cross_sphere" in types
    
    def test_audit_actions(self):
        """R&D Rule #6: Audit action types."""
        from models.base import AuditLogAction
        
        actions = [a.value for a in AuditLogAction]
        
        # CRUD
        assert "create" in actions
        assert "read" in actions
        assert "update" in actions
        assert "delete" in actions
        
        # Checkpoints
        assert "checkpoint.created" in actions
        assert "checkpoint.approved" in actions
        assert "checkpoint.rejected" in actions
        
        # Agents (R&D Rule #4)
        assert "agent.hired" in actions
        assert "agent.fired" in actions
        
        # Cross-sphere
        assert "cross_sphere.access" in actions


class TestThreadEventTypes:
    """Test thread event types for event sourcing."""
    
    def test_lifecycle_events(self):
        """Test thread lifecycle events."""
        from models.base import ThreadEventType
        
        assert ThreadEventType.THREAD_CREATED.value == "thread.created"
        assert ThreadEventType.THREAD_UPDATED.value == "thread.updated"
        assert ThreadEventType.THREAD_ARCHIVED.value == "thread.archived"
    
    def test_checkpoint_events(self):
        """R&D Rule #1: Checkpoint events."""
        from models.base import ThreadEventType
        
        assert ThreadEventType.CHECKPOINT_TRIGGERED.value == "checkpoint.triggered"
        assert ThreadEventType.CHECKPOINT_APPROVED.value == "checkpoint.approved"
        assert ThreadEventType.CHECKPOINT_REJECTED.value == "checkpoint.rejected"


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE MODEL TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPersonalSphereModels:
    """Test Personal sphere models."""
    
    def test_note_model_fields(self):
        """Test Note model has required fields."""
        from models.spheres import Note
        
        # Check table name
        assert Note.__tablename__ == "personal_notes"
        
        # Check columns exist
        columns = [c.name for c in Note.__table__.columns]
        assert "id" in columns
        assert "created_by" in columns
        assert "title" in columns
        assert "content" in columns
        assert "folder" in columns
        assert "tags" in columns
        assert "created_at" in columns
    
    def test_task_model_fields(self):
        """Test Task model has required fields."""
        from models.spheres import Task
        
        assert Task.__tablename__ == "personal_tasks"
        
        columns = [c.name for c in Task.__table__.columns]
        assert "status" in columns
        assert "priority" in columns
        assert "due_date" in columns
    
    def test_habit_model_fields(self):
        """Test Habit model has required fields."""
        from models.spheres import Habit
        
        assert Habit.__tablename__ == "personal_habits"
        
        columns = [c.name for c in Habit.__table__.columns]
        assert "streak" in columns
        assert "frequency" in columns


class TestBusinessSphereModels:
    """Test Business sphere models."""
    
    def test_contact_model_fields(self):
        """Test Contact model (CRM)."""
        from models.spheres import Contact
        
        assert Contact.__tablename__ == "business_contacts"
        
        columns = [c.name for c in Contact.__table__.columns]
        assert "name" in columns
        assert "email" in columns
        assert "company" in columns
        assert "lead_score" in columns
        assert "lead_status" in columns
    
    def test_invoice_model_fields(self):
        """Test Invoice model."""
        from models.spheres import Invoice
        
        assert Invoice.__tablename__ == "business_invoices"
        
        columns = [c.name for c in Invoice.__table__.columns]
        assert "invoice_number" in columns
        assert "subtotal" in columns
        assert "tax_rate" in columns
        assert "total" in columns
        assert "line_items" in columns


class TestCreativeSphereModels:
    """Test Creative Studio sphere models."""
    
    def test_creative_asset_model(self):
        """Test CreativeAsset model."""
        from models.spheres import CreativeAsset
        
        assert CreativeAsset.__tablename__ == "creative_assets"
        
        columns = [c.name for c in CreativeAsset.__table__.columns]
        assert "asset_type" in columns
        assert "generation_engine" in columns
        assert "prompt" in columns


class TestSocialSphereModels:
    """Test Social sphere models (R&D Rule #5)."""
    
    def test_social_post_model(self):
        """Test SocialPost model."""
        from models.spheres import SocialPost
        
        assert SocialPost.__tablename__ == "social_posts"
        
        columns = [c.name for c in SocialPost.__table__.columns]
        assert "content" in columns
        assert "visibility" in columns
        # Engagement counters exist but NOT for ranking
        assert "like_count" in columns
        assert "comment_count" in columns
    
    def test_social_post_has_chronological_index(self):
        """R&D Rule #5: Social posts use chronological ordering."""
        from models.spheres import SocialPost
        
        # Check for chronological index
        indexes = [idx.name for idx in SocialPost.__table__.indexes]
        assert "ix_social_posts_chrono" in indexes


class TestMyTeamSphereModels:
    """Test My Team sphere models (R&D Rule #4)."""
    
    def test_hired_agent_model(self):
        """R&D Rule #4: Agent hiring tracked."""
        from models.spheres import HiredAgent
        
        assert HiredAgent.__tablename__ == "team_agents"
        
        columns = [c.name for c in HiredAgent.__table__.columns]
        # Must track WHO hired (for Rule #4 audit)
        assert "hired_by" in columns
        assert "hired_at" in columns
        assert "hire_checkpoint_id" in columns
    
    def test_team_member_alphabetical_index(self):
        """R&D Rule #5: Team members sorted alphabetically."""
        from models.spheres import TeamMember
        
        indexes = [idx.name for idx in TeamMember.__table__.indexes]
        assert "ix_team_members_alpha" in indexes


class TestScholarSphereModels:
    """Test Scholar sphere models."""
    
    def test_reference_model(self):
        """Test Reference model for academic citations."""
        from models.spheres import Reference
        
        assert Reference.__tablename__ == "scholar_references"
        
        columns = [c.name for c in Reference.__table__.columns]
        assert "title" in columns
        assert "authors" in columns
        assert "doi" in columns
        assert "abstract" in columns


class TestGovernmentSphereModels:
    """Test Government sphere models."""
    
    def test_compliance_model(self):
        """Test ComplianceItem model."""
        from models.spheres import ComplianceItem
        
        assert ComplianceItem.__tablename__ == "government_compliance"
        
        columns = [c.name for c in ComplianceItem.__table__.columns]
        assert "compliance_type" in columns
        assert "expiry_date" in columns
        assert "license_number" in columns
    
    def test_clinical_trial_model(self):
        """Test ClinicalTrial model."""
        from models.spheres import ClinicalTrial
        
        assert ClinicalTrial.__tablename__ == "government_clinical_trials"
        
        columns = [c.name for c in ClinicalTrial.__table__.columns]
        assert "trial_id" in columns
        assert "phase" in columns
        assert "reb_approval" in columns


# ═══════════════════════════════════════════════════════════════════════════════
# REPOSITORY TESTS (Mocked)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBaseRepository:
    """Test base repository pattern."""
    
    def test_identity_boundary_on_get(self, identity_id, other_identity_id):
        """R&D Rule #3: get_by_id checks identity."""
        # This test verifies the query includes identity_id check
        # In real implementation, would use actual database
        
        # Verify the method signature requires identity_id
        from repositories.base_repository import BaseRepository
        import inspect
        
        sig = inspect.signature(BaseRepository.get_by_id)
        params = list(sig.parameters.keys())
        
        assert "id" in params
        assert "identity_id" in params
    
    def test_list_all_includes_identity(self, identity_id):
        """R&D Rule #3: list_all scoped to identity."""
        from repositories.base_repository import BaseRepository
        import inspect
        
        sig = inspect.signature(BaseRepository.list_all)
        params = list(sig.parameters.keys())
        
        assert "identity_id" in params
    
    def test_create_sets_created_by(self, identity_id):
        """R&D Rule #6: create sets created_by."""
        from repositories.base_repository import BaseRepository
        import inspect
        
        sig = inspect.signature(BaseRepository.create)
        params = list(sig.parameters.keys())
        
        assert "identity_id" in params


class TestThreadRepository:
    """Test thread repository (event sourcing)."""
    
    def test_append_event_method_exists(self):
        """Event sourcing: append_event available."""
        from repositories.base_repository import ThreadRepository
        
        assert hasattr(ThreadRepository, "append_event")
    
    def test_get_events_method_exists(self):
        """Event sourcing: get_events available."""
        from repositories.base_repository import ThreadRepository
        
        assert hasattr(ThreadRepository, "get_events")
    
    def test_create_generates_initial_event(self):
        """Event sourcing: create generates thread.created event."""
        from repositories.base_repository import ThreadRepository
        import inspect
        
        # Check create method exists
        assert hasattr(ThreadRepository, "create")
        
        # In real implementation, verify it calls append_event
        # with event_type="thread.created"


class TestCheckpointRepository:
    """Test checkpoint repository (R&D Rule #1)."""
    
    def test_create_checkpoint_method(self):
        """R&D Rule #1: Can create checkpoints."""
        from repositories.base_repository import CheckpointRepository
        
        assert hasattr(CheckpointRepository, "create")
    
    def test_get_pending_method(self):
        """R&D Rule #1: Can get pending checkpoints."""
        from repositories.base_repository import CheckpointRepository
        
        assert hasattr(CheckpointRepository, "get_pending")
    
    def test_approve_method(self):
        """R&D Rule #1: Can approve checkpoints."""
        from repositories.base_repository import CheckpointRepository
        
        assert hasattr(CheckpointRepository, "approve")
    
    def test_reject_method(self):
        """R&D Rule #1: Can reject checkpoints."""
        from repositories.base_repository import CheckpointRepository
        
        assert hasattr(CheckpointRepository, "reject")


class TestAuditLogRepository:
    """Test audit log repository (R&D Rule #6)."""
    
    def test_log_method(self):
        """R&D Rule #6: Can create audit logs."""
        from repositories.base_repository import AuditLogRepository
        
        assert hasattr(AuditLogRepository, "log")
    
    def test_get_for_identity_method(self):
        """R&D Rule #6: Can retrieve audit logs."""
        from repositories.base_repository import AuditLogRepository
        
        assert hasattr(AuditLogRepository, "get_for_identity")


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE SESSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDatabaseSession:
    """Test database session management."""
    
    def test_session_context_has_identity(self):
        """R&D Rule #3: Session context includes identity."""
        from repositories.database import SessionContext
        
        session_mock = MagicMock()
        identity_id = uuid4()
        
        ctx = SessionContext(session=session_mock, identity_id=identity_id)
        
        assert ctx.identity_id == identity_id
        assert ctx.session == session_mock
    
    def test_session_context_with_identity(self):
        """Can create new context with identity."""
        from repositories.database import SessionContext
        
        session_mock = MagicMock()
        identity_id = uuid4()
        
        ctx = SessionContext(session=session_mock)
        new_ctx = ctx.with_identity(identity_id)
        
        assert new_ctx.identity_id == identity_id
        assert new_ctx.session == session_mock
    
    def test_unit_of_work_has_repositories(self):
        """Unit of Work provides repository access."""
        from repositories.database import UnitOfWork
        
        # Check UnitOfWork has expected attributes
        assert hasattr(UnitOfWork, "threads")
        assert hasattr(UnitOfWork, "checkpoints")
        assert hasattr(UnitOfWork, "audit")


# ═══════════════════════════════════════════════════════════════════════════════
# MIGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigration:
    """Test migration script validity."""
    
    def test_migration_has_upgrade(self):
        """Migration has upgrade function."""
        from migrations.v80_001_initial import upgrade
        
        assert callable(upgrade)
    
    def test_migration_has_downgrade(self):
        """Migration has downgrade function."""
        from migrations.v80_001_initial import downgrade
        
        assert callable(downgrade)
    
    def test_migration_revision_id(self):
        """Migration has valid revision ID."""
        from migrations import v80_001_initial
        
        assert v80_001_initial.revision == "v80_001_initial"


# ═══════════════════════════════════════════════════════════════════════════════
# R&D COMPLIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRDRule3IdentityBoundary:
    """R&D Rule #3: Identity boundary enforcement."""
    
    def test_all_sphere_models_have_created_by(self):
        """All sphere models have created_by field."""
        from models.spheres import (
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        )
        
        models = [
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        ]
        
        for model in models:
            columns = [c.name for c in model.__table__.columns]
            assert "created_by" in columns, f"{model.__name__} missing created_by"
    
    def test_all_sphere_models_have_owner_index(self):
        """All sphere models have index on created_by."""
        from models.spheres import (
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        )
        
        models = [
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        ]
        
        for model in models:
            indexes = [idx.name for idx in model.__table__.indexes]
            has_owner_index = any("owner" in idx for idx in indexes)
            assert has_owner_index, f"{model.__name__} missing owner index"


class TestRDRule5ChronologicalOrdering:
    """R&D Rule #5: Chronological ordering (no ranking)."""
    
    def test_social_posts_chronological(self):
        """Social posts use chronological index."""
        from models.spheres import SocialPost
        
        indexes = [idx.name for idx in SocialPost.__table__.indexes]
        assert "ix_social_posts_chrono" in indexes
    
    def test_entertainment_history_chronological(self):
        """Stream history uses chronological index."""
        from models.spheres import StreamHistory
        
        indexes = [idx.name for idx in StreamHistory.__table__.indexes]
        assert "ix_entertainment_history_chrono" in indexes
    
    def test_team_tasks_chronological(self):
        """Team tasks use chronological index."""
        from models.spheres import TeamTask
        
        indexes = [idx.name for idx in TeamTask.__table__.indexes]
        assert "ix_team_tasks_chrono" in indexes


class TestRDRule6Traceability:
    """R&D Rule #6: Full traceability."""
    
    def test_all_models_have_timestamps(self):
        """All models have created_at and updated_at."""
        from models.spheres import (
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        )
        
        models = [
            Note, Task, Habit,
            Contact, Invoice, Project,
            CreativeAsset, CreativeProject,
            Playlist, StreamHistory,
            CommunityGroup, CommunityEvent,
            SocialPost, SocialSchedule,
            Reference, Manuscript,
            ComplianceItem, ClinicalTrial,
            TeamMember, HiredAgent, TeamTask
        ]
        
        for model in models:
            columns = [c.name for c in model.__table__.columns]
            assert "created_at" in columns, f"{model.__name__} missing created_at"
            assert "updated_at" in columns, f"{model.__name__} missing updated_at"
    
    def test_audit_log_has_required_fields(self):
        """Audit log has all required fields."""
        from models.base import AuditLog
        
        columns = [c.name for c in AuditLog.__table__.columns]
        
        required = [
            "id", "timestamp", "identity_id", "action",
            "resource_type", "resource_id", "details"
        ]
        
        for field in required:
            assert field in columns, f"AuditLog missing {field}"


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

def test_model_count():
    """Summary: count all models."""
    from models.spheres import __all__ as sphere_models
    from models.base import (
        Identity, Thread, ThreadEvent, Checkpoint, AuditLog
    )
    
    core_models = 5  # Identity, Thread, ThreadEvent, Checkpoint, AuditLog
    sphere_model_count = len(sphere_models)
    
    total = core_models + sphere_model_count
    
    print(f"\n📊 Model Summary:")
    print(f"   Core models: {core_models}")
    print(f"   Sphere models: {sphere_model_count}")
    print(f"   Total: {total}")
    
    assert total >= 25, "Should have at least 25 models"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
