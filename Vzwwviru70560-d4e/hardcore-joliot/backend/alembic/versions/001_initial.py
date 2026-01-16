"""CHE·NU V76 Initial Schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-08

R&D Rules Compliance:
- Rule #6: All tables have id, created_by, created_at
- Rule #7: 9 spheres, 6 bureau sections enforced via enums
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ═══════════════════════════════════════════════════════════════════════════
    # ENUMS
    # ═══════════════════════════════════════════════════════════════════════════
    
    sphere_type = postgresql.ENUM(
        'personal', 'business', 'government', 'creative_studio',
        'community', 'social_media', 'entertainment', 'my_team', 'scholar',
        name='spheretype'
    )
    sphere_type.create(op.get_bind())
    
    bureau_section = postgresql.ENUM(
        'quick_capture', 'resume_workspace', 'threads',
        'data_files', 'active_agents', 'meetings',
        name='bureausection'
    )
    bureau_section.create(op.get_bind())
    
    thread_status = postgresql.ENUM(
        'draft', 'active', 'maturing', 'decision_ready', 'decided', 'archived',
        name='threadstatus'
    )
    thread_status.create(op.get_bind())
    
    checkpoint_status = postgresql.ENUM(
        'pending', 'approved', 'rejected', 'expired',
        name='checkpointstatus'
    )
    checkpoint_status.create(op.get_bind())
    
    checkpoint_type = postgresql.ENUM(
        'delete', 'archive', 'critical_decision', 'transfer', 'external_action',
        name='checkpointtype'
    )
    checkpoint_type.create(op.get_bind())
    
    decision_severity = postgresql.ENUM(
        'informational', 'minor', 'major', 'critical',
        name='decisionseverity'
    )
    decision_severity.create(op.get_bind())
    
    memory_layer = postgresql.ENUM(
        'hot', 'warm', 'cold',
        name='memorylayer'
    )
    memory_layer.create(op.get_bind())
    
    # ═══════════════════════════════════════════════════════════════════════════
    # IDENTITIES
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'identities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('avatar_url', sa.String(500)),
        sa.Column('preferences', postgresql.JSONB(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_identities_email', 'identities', ['email'])
    op.create_index('ix_identities_created_by', 'identities', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SPHERES (Rule #7)
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'spheres',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sphere_type', sphere_type, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.String(50)),
        sa.Column('color', sa.String(20)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('settings', postgresql.JSONB(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.UniqueConstraint('owner_id', 'sphere_type', name='uq_sphere_per_owner'),
    )
    op.create_index('ix_spheres_owner_type', 'spheres', ['owner_id', 'sphere_type'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # WORKSPACES (Rule #7 - 6 sections)
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'workspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('sphere_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('spheres.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('sections', postgresql.JSONB(), default={}),
        sa.Column('is_default', sa.Boolean(), default=False),
        sa.Column('settings', postgresql.JSONB(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_workspaces_sphere', 'workspaces', ['sphere_id'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECKPOINTS (Rule #1 - Human Sovereignty)
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'checkpoints',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('checkpoint_type', checkpoint_type, nullable=False),
        sa.Column('status', checkpoint_status, default='pending'),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action_type', sa.String(100), nullable=False),
        sa.Column('action_data', postgresql.JSONB(), nullable=False),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True)),
        sa.Column('approved_at', sa.DateTime(timezone=True)),
        sa.Column('rejection_reason', sa.Text()),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_checkpoints_status', 'checkpoints', ['status'])
    op.create_index('ix_checkpoints_resource', 'checkpoints', ['resource_type', 'resource_id'])
    op.create_index('ix_checkpoints_expires', 'checkpoints', ['expires_at'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREADS
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'threads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('sphere_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('spheres.id', ondelete='SET NULL')),
        sa.Column('parent_thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id', ondelete='SET NULL')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('founding_intent', sa.Text(), nullable=False),
        sa.Column('status', thread_status, default='draft'),
        sa.Column('maturity_score', sa.Integer(), default=0),
        sa.Column('tags', postgresql.JSONB(), default=[]),
        sa.Column('metadata', postgresql.JSONB(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_threads_owner', 'threads', ['owner_id'])
    op.create_index('ix_threads_sphere', 'threads', ['sphere_id'])
    op.create_index('ix_threads_status', 'threads', ['status'])
    op.create_index('ix_threads_created_at', 'threads', ['created_at'])  # Rule #5
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREAD EVENTS (Immutable Event Log)
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'thread_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('event_data', postgresql.JSONB(), nullable=False),
        sa.Column('parent_event_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('thread_events.id')),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_thread_events_thread', 'thread_events', ['thread_id'])
    op.create_index('ix_thread_events_type', 'thread_events', ['event_type'])
    op.create_index('ix_thread_events_sequence', 'thread_events', ['thread_id', 'sequence_number'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DECISIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('severity', decision_severity, default='informational'),
        sa.Column('checkpoint_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('checkpoints.id')),
        sa.Column('rationale', sa.Text()),
        sa.Column('outcome', sa.Text()),
        sa.Column('is_final', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_decisions_thread', 'decisions', ['thread_id'])
    op.create_index('ix_decisions_severity', 'decisions', ['severity'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DATASPACES
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'dataspaces',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_encrypted', sa.Boolean(), default=True),
        sa.Column('encryption_key_id', sa.String(255)),
        sa.Column('storage_bytes', sa.Integer(), default=0),
        sa.Column('file_count', sa.Integer(), default=0),
        sa.Column('metadata', postgresql.JSONB(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_dataspaces_owner', 'dataspaces', ['owner_id'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AGENTS (Rule #4)
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('agent_type', sa.String(100), nullable=False),
        sa.Column('sphere_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('spheres.id', ondelete='SET NULL')),
        sa.Column('capabilities', postgresql.JSONB(), default=[]),
        sa.Column('can_call_other_agents', sa.Boolean(), default=False),  # Rule #4
        sa.Column('token_budget', sa.Integer(), default=10000),
        sa.Column('tokens_used', sa.Integer(), default=0),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_hired', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_agents_owner', 'agents', ['owner_id'])
    op.create_index('ix_agents_type', 'agents', ['agent_type'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MEMORY SNAPSHOTS
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'memory_snapshots',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('layer', memory_layer, default='warm'),
        sa.Column('snapshot_data', postgresql.JSONB(), nullable=False),
        sa.Column('compression_ratio', sa.Float()),
        sa.Column('events_included', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_memory_snapshots_thread', 'memory_snapshots', ['thread_id'])
    op.create_index('ix_memory_snapshots_layer', 'memory_snapshots', ['layer'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MEETINGS
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'meetings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('workspace_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('workspaces.id', ondelete='SET NULL')),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('scheduled_at', sa.DateTime(timezone=True)),
        sa.Column('duration_minutes', sa.Integer(), default=30),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('notes', sa.Text()),
        sa.Column('action_items', postgresql.JSONB(), default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_meetings_owner', 'meetings', ['owner_id'])
    op.create_index('ix_meetings_scheduled', 'meetings', ['scheduled_at'])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('notification_type', sa.String(100), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('message', sa.Text()),
        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('read_at', sa.DateTime(timezone=True)),
        sa.Column('resource_type', sa.String(100)),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index('ix_notifications_owner', 'notifications', ['owner_id'])
    op.create_index('ix_notifications_unread', 'notifications', ['owner_id', 'is_read'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('notifications')
    op.drop_table('meetings')
    op.drop_table('memory_snapshots')
    op.drop_table('agents')
    op.drop_table('dataspaces')
    op.drop_table('decisions')
    op.drop_table('thread_events')
    op.drop_table('threads')
    op.drop_table('checkpoints')
    op.drop_table('workspaces')
    op.drop_table('spheres')
    op.drop_table('identities')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS memorylayer')
    op.execute('DROP TYPE IF EXISTS decisionseverity')
    op.execute('DROP TYPE IF EXISTS checkpointtype')
    op.execute('DROP TYPE IF EXISTS checkpointstatus')
    op.execute('DROP TYPE IF EXISTS threadstatus')
    op.execute('DROP TYPE IF EXISTS bureausection')
    op.execute('DROP TYPE IF EXISTS spheretype')
