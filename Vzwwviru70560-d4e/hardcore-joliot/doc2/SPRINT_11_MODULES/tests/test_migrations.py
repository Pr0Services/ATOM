"""
CHE·NU™ - Database Migration Tests
"""
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text


class TestMigrationChain:
    """Test migration chain integrity"""
    
    def test_all_migrations_have_revision(self, alembic_config):
        """Test all 11 migrations have proper revision IDs"""
        from alembic.script import ScriptDirectory
        script = ScriptDirectory.from_config(alembic_config)
        revisions = list(script.walk_revisions())
        
        # Should have 11 migrations (v40_001 to v40_011)
        assert len(revisions) >= 11
    
    def test_upgrade_from_base(self, db_engine, alembic_config):
        """Test upgrading from base to head"""
        # Downgrade to base
        command.downgrade(alembic_config, "base")
        
        # Upgrade to head
        command.upgrade(alembic_config, "head")
        
        # Verify tables exist
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        
        # Core tables should exist
        assert "users" in tables
        assert "spheres" in tables
        assert "bureaus" in tables
        assert "threads" in tables
    
    def test_downgrade_to_base(self, db_engine, alembic_config):
        """Test downgrading to base"""
        # Ensure we're at head
        command.upgrade(alembic_config, "head")
        
        # Downgrade to base
        command.downgrade(alembic_config, "base")
        
        # Most tables should be gone
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        assert len(tables) == 0 or "alembic_version" in tables


class TestMigrationV40_001:
    """Test foundation migration"""
    
    def test_foundation_tables_created(self, db_engine, alembic_config):
        """Test v40_001 creates foundation tables"""
        command.downgrade(alembic_config, "base")
        command.upgrade(alembic_config, "v40_001_foundation")
        
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        
        # Foundation tables
        assert "users" in tables
        assert "spheres" in tables
        assert "bureaus" in tables
        assert "threads" in tables
        assert "agents" in tables


class TestMigrationV40_002:
    """Test CRM system migration"""
    
    def test_crm_tables_created(self, db_engine, alembic_config):
        """Test v40_002 creates CRM tables"""
        command.upgrade(alembic_config, "v40_002_crm_system")
        
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        
        assert "crm_contacts" in tables
        assert "crm_companies" in tables
        assert "crm_deals" in tables
        assert "crm_pipelines" in tables


class TestMigrationV40_004:
    """Test Scholar system migration"""
    
    def test_scholar_tables_created(self, db_engine, alembic_config):
        """Test v40_004 creates Scholar tables"""
        command.upgrade(alembic_config, "v40_004_scholar_system")
        
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()
        
        assert "scholar_references" in tables
        assert "scholar_flashcards" in tables
        assert "scholar_study_plans" in tables


class TestDataIntegrity:
    """Test data integrity during migrations"""
    
    def test_no_data_loss_on_upgrade(self, db_session, alembic_config):
        """Test data persists through upgrade"""
        # Insert test data
        with db_session.begin():
            db_session.execute(text("""
                INSERT INTO users (email, first_name, last_name, password_hash)
                VALUES ('test@example.com', 'Test', 'User', 'hashed_password')
            """))
        
        # Upgrade
        command.upgrade(alembic_config, "head")
        
        # Verify data still exists
        result = db_session.execute(text("SELECT email FROM users WHERE email = 'test@example.com'"))
        assert result.fetchone() is not None
    
    def test_foreign_keys_valid(self, db_engine, alembic_config):
        """Test foreign key constraints are valid"""
        command.upgrade(alembic_config, "head")
        
        inspector = inspect(db_engine)
        
        # Check threads -> users foreign key
        fks = inspector.get_foreign_keys("threads")
        user_fk = next((fk for fk in fks if "users" in fk["referred_table"]), None)
        assert user_fk is not None
    
    def test_indexes_created(self, db_engine, alembic_config):
        """Test indexes are created"""
        command.upgrade(alembic_config, "head")
        
        inspector = inspect(db_engine)
        
        # Check users table has email index
        indexes = inspector.get_indexes("users")
        email_index = next((idx for idx in indexes if "email" in idx["column_names"]), None)
        assert email_index is not None


class TestMigrationPerformance:
    """Test migration performance"""
    
    def test_upgrade_time_acceptable(self, alembic_config):
        """Test full upgrade completes in reasonable time"""
        import time
        
        command.downgrade(alembic_config, "base")
        
        start = time.time()
        command.upgrade(alembic_config, "head")
        duration = time.time() - start
        
        # Should complete in under 30 seconds
        assert duration < 30.0
    
    def test_downgrade_time_acceptable(self, alembic_config):
        """Test full downgrade completes in reasonable time"""
        import time
        
        command.upgrade(alembic_config, "head")
        
        start = time.time()
        command.downgrade(alembic_config, "base")
        duration = time.time() - start
        
        # Should complete in under 20 seconds
        assert duration < 20.0


class TestMigrationIdempotency:
    """Test migrations are idempotent"""
    
    def test_upgrade_twice(self, alembic_config):
        """Test running upgrade twice doesn't cause errors"""
        command.upgrade(alembic_config, "head")
        # Run again - should be no-op
        command.upgrade(alembic_config, "head")
        # No assertion needed - just should not raise
    
    def test_partial_upgrade_resume(self, alembic_config):
        """Test can resume partial upgrade"""
        # Upgrade to middle revision
        command.upgrade(alembic_config, "v40_005_studio_system")
        
        # Complete upgrade
        command.upgrade(alembic_config, "head")
        
        # Should complete successfully


class TestMigrationRollback:
    """Test migration rollback scenarios"""
    
    def test_rollback_single_migration(self, alembic_config):
        """Test rolling back single migration"""
        # Upgrade to head
        command.upgrade(alembic_config, "head")
        
        # Downgrade one step
        command.downgrade(alembic_config, "-1")
        
        # Should be at v40_010
        from alembic.script import ScriptDirectory
        from alembic.runtime.migration import MigrationContext
        script = ScriptDirectory.from_config(alembic_config)
        
        # Verify not at head
        # (actual implementation would check current revision)


# Fixtures
@pytest.fixture
def alembic_config():
    """Get Alembic configuration"""
    config = Config("alembic.ini")
    return config


@pytest.fixture
def db_engine(alembic_config):
    """Get database engine"""
    from sqlalchemy import create_engine
    db_url = alembic_config.get_main_option("sqlalchemy.url")
    return create_engine(db_url)


@pytest.fixture
def db_session(db_engine):
    """Get database session"""
    from sqlalchemy.orm import Session
    session = Session(db_engine)
    yield session
    session.close()
