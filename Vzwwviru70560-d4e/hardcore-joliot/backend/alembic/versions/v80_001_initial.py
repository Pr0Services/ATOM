"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Initial Database Migration
═══════════════════════════════════════════════════════════════════════════════

Creates all tables for:
- Identity & Authentication
- Threads & Event Sourcing
- Checkpoints (R&D Rule #1)
- Audit Logs (R&D Rule #6)
- All 9 Sphere Tables

Revision ID: v80_001_initial
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = 'v80_001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all CHE·NU tables."""
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENUMS
    # ═══════════════════════════════════════════════════════════════════════
    
    sphere_type = postgresql.ENUM(
        'personal', 'business', 'creative_studio', 'entertainment',
        'community', 'social', 'scholar', 'government', 'my_team',
        name='spheretype'
    )
    sphere_type.create(op.get_bind())
    
    thread_status = postgresql.ENUM(
        'active', 'paused', 'completed', 'archived',
        name='threadstatus'
    )
    thread_status.create(op.get_bind())
    
    thread_type = postgresql.ENUM(
        'personal', 'collective', 'institutional',
        name='threadtype'
    )
    thread_type.create(op.get_bind())
    
    visibility = postgresql.ENUM(
        'private', 'semi_private', 'public',
        name='visibility'
    )
    visibility.create(op.get_bind())
    
    checkpoint_status = postgresql.ENUM(
        'pending', 'approved', 'rejected', 'expired',
        name='checkpointstatus'
    )
    checkpoint_status.create(op.get_bind())
    
    checkpoint_type = postgresql.ENUM(
        'governance', 'cost', 'identity', 'sensitive', 'cross_sphere',
        name='checkpointtype'
    )
    checkpoint_type.create(op.get_bind())
    
    thread_event_type = postgresql.ENUM(
        'thread.created', 'thread.updated', 'thread.archived',
        'intent.declared', 'intent.refined',
        'decision.recorded', 'decision.revised',
        'action.created', 'action.updated', 'action.completed',
        'note.added', 'summary.snapshot', 'memory.compressed',
        'link.added', 'thread.referenced',
        'checkpoint.triggered', 'checkpoint.approved', 'checkpoint.rejected',
        name='threadeventtype'
    )
    thread_event_type.create(op.get_bind())
    
    audit_action = postgresql.ENUM(
        'login', 'logout',
        'create', 'read', 'update', 'delete',
        'checkpoint.created', 'checkpoint.approved', 'checkpoint.rejected',
        'agent.hired', 'agent.fired', 'agent.task',
        'cross_sphere.access', 'cross_sphere.transfer',
        name='auditlogaction'
    )
    audit_action.create(op.get_bind())
    
    # ═══════════════════════════════════════════════════════════════════════
    # IDENTITIES
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'identities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('settings', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_identities_email', 'identities', ['email'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # THREADS (Event Sourcing)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'threads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('owner_identity_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('founding_intent', sa.Text(), nullable=False),
        sa.Column('title', sa.String(500)),
        sa.Column('description', sa.Text()),
        sa.Column('sphere', sphere_type, nullable=False),
        sa.Column('thread_type', thread_type, default='personal'),
        sa.Column('status', thread_status, default='active'),
        sa.Column('visibility', visibility, default='private'),
        sa.Column('parent_thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id')),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('metadata', postgresql.JSON(), default={}),
        sa.Column('event_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_threads_owner_sphere', 'threads', ['owner_identity_id', 'sphere'])
    op.create_index('ix_threads_owner_status', 'threads', ['owner_identity_id', 'status'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # THREAD EVENTS (Append-Only)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'thread_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id'), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('parent_event_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('thread_events.id')),
        sa.Column('event_type', thread_event_type, nullable=False),
        sa.Column('payload', postgresql.JSON(), default={}),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('actor_type', sa.String(50), default='human'),
        sa.Column('actor_id', postgresql.UUID(as_uuid=True)),
    )
    op.create_index('ix_thread_events_thread_seq', 'thread_events', ['thread_id', 'sequence_number'])
    op.create_index('ix_thread_events_type', 'thread_events', ['event_type'])
    op.create_index('uq_thread_events_thread_seq', 'thread_events', 
                    ['thread_id', 'sequence_number'], unique=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CHECKPOINTS (R&D Rule #1)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'checkpoints',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('identity_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('sphere', sphere_type, nullable=False),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('threads.id')),
        sa.Column('checkpoint_type', checkpoint_type, nullable=False),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('payload', postgresql.JSON(), default={}),
        sa.Column('status', checkpoint_status, default='pending'),
        sa.Column('resolved_at', sa.DateTime(timezone=True)),
        sa.Column('resolved_by', postgresql.UUID(as_uuid=True)),
        sa.Column('resolution_reason', sa.Text()),
        sa.Column('expires_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_checkpoints_identity_status', 'checkpoints', ['identity_id', 'status'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # AUDIT LOGS (R&D Rule #6)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('identity_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('actor_type', sa.String(50), default='human'),
        sa.Column('actor_id', postgresql.UUID(as_uuid=True)),
        sa.Column('action', audit_action, nullable=False),
        sa.Column('resource_type', sa.String(100), nullable=False),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True)),
        sa.Column('sphere', sphere_type),
        sa.Column('details', postgresql.JSON(), default={}),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('user_agent', sa.String(500)),
        sa.Column('request_id', postgresql.UUID(as_uuid=True)),
    )
    op.create_index('ix_audit_logs_identity_time', 'audit_logs', ['identity_id', 'timestamp'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_resource', 'audit_logs', ['resource_type', 'resource_id'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🏠 PERSONAL SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'personal_notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('folder', sa.String(255)),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('is_pinned', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_personal_notes_owner', 'personal_notes', ['created_by'])
    op.create_index('ix_personal_notes_folder', 'personal_notes', ['created_by', 'folder'])
    
    op.create_table(
        'personal_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('priority', sa.String(20), default='medium'),
        sa.Column('due_date', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_personal_tasks_owner_status', 'personal_tasks', ['created_by', 'status'])
    
    op.create_table(
        'personal_habits',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('frequency', sa.String(50), default='daily'),
        sa.Column('streak', sa.Integer(), default=0),
        sa.Column('last_completed', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_personal_habits_owner', 'personal_habits', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 💼 BUSINESS SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'business_contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(50)),
        sa.Column('company', sa.String(255)),
        sa.Column('title', sa.String(255)),
        sa.Column('lead_score', sa.Integer(), default=0),
        sa.Column('lead_status', sa.String(50), default='new'),
        sa.Column('source', sa.String(100)),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('custom_fields', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_business_contacts_owner', 'business_contacts', ['created_by'])
    op.create_index('ix_business_contacts_company', 'business_contacts', ['created_by', 'company'])
    
    op.create_table(
        'business_invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('invoice_number', sa.String(50), nullable=False),
        sa.Column('contact_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('business_contacts.id')),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False),
        sa.Column('tax_rate', sa.Numeric(5, 4), default=0),
        sa.Column('tax_amount', sa.Numeric(12, 2), default=0),
        sa.Column('total', sa.Numeric(12, 2), nullable=False),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('due_date', sa.Date()),
        sa.Column('paid_at', sa.DateTime(timezone=True)),
        sa.Column('line_items', postgresql.JSON(), default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_business_invoices_owner', 'business_invoices', ['created_by'])
    op.create_index('ix_business_invoices_status', 'business_invoices', ['created_by', 'status'])
    
    op.create_table(
        'business_projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(50), default='planning'),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('budget', sa.Numeric(12, 2)),
        sa.Column('progress', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_business_projects_owner', 'business_projects', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎨 CREATIVE STUDIO SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'creative_assets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('asset_type', sa.String(50), nullable=False),
        sa.Column('file_url', sa.String(1000)),
        sa.Column('thumbnail_url', sa.String(1000)),
        sa.Column('file_size', sa.Integer()),
        sa.Column('generation_engine', sa.String(100)),
        sa.Column('prompt', sa.Text()),
        sa.Column('generation_params', postgresql.JSON(), default={}),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('metadata', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_creative_assets_owner', 'creative_assets', ['created_by'])
    op.create_index('ix_creative_assets_type', 'creative_assets', ['created_by', 'asset_type'])
    
    op.create_table(
        'creative_projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('project_type', sa.String(100)),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_creative_projects_owner', 'creative_projects', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🎬 ENTERTAINMENT SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'entertainment_playlists',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('playlist_type', sa.String(50)),
        sa.Column('is_public', sa.Boolean(), default=False),
        sa.Column('items', postgresql.JSON(), default=[]),
        sa.Column('item_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_entertainment_playlists_owner', 'entertainment_playlists', ['created_by'])
    
    op.create_table(
        'entertainment_stream_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('content_type', sa.String(50), nullable=False),
        sa.Column('content_id', sa.String(255), nullable=False),
        sa.Column('content_title', sa.String(500)),
        sa.Column('watched_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('duration_watched', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # CHRONOLOGICAL ordering (R&D Rule #5)
    op.create_index('ix_entertainment_history_chrono', 'entertainment_stream_history', 
                    ['created_by', 'watched_at'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 👥 COMMUNITY SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'community_groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('group_type', sa.String(50), default='general'),
        sa.Column('is_public', sa.Boolean(), default=False),
        sa.Column('member_count', sa.Integer(), default=1),
        sa.Column('settings', postgresql.JSON(), default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_community_groups_owner', 'community_groups', ['created_by'])
    
    op.create_table(
        'community_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('group_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('community_groups.id')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('event_type', sa.String(50), default='meetup'),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True)),
        sa.Column('location', sa.String(500)),
        sa.Column('is_virtual', sa.Boolean(), default=False),
        sa.Column('virtual_url', sa.String(500)),
        sa.Column('rsvp_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_community_events_owner', 'community_events', ['created_by'])
    op.create_index('ix_community_events_time', 'community_events', ['start_time'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📱 SOCIAL SPHERE (NO RANKING - R&D Rule #5)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'social_posts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('media_urls', postgresql.JSON(), default=[]),
        sa.Column('media_type', sa.String(50)),
        sa.Column('visibility', sa.String(50), default='public'),
        # Engagement counters (display only, NOT for ranking)
        sa.Column('like_count', sa.Integer(), default=0),
        sa.Column('comment_count', sa.Integer(), default=0),
        sa.Column('share_count', sa.Integer(), default=0),
        sa.Column('scheduled_for', sa.DateTime(timezone=True)),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # CHRONOLOGICAL index (R&D Rule #5 - NO engagement ranking)
    op.create_index('ix_social_posts_chrono', 'social_posts', ['created_by', 'created_at'])
    op.create_index('ix_social_posts_published', 'social_posts', ['published_at'])
    
    op.create_table(
        'social_schedules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('post_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('social_posts.id')),
        sa.Column('platform', sa.String(50), nullable=False),
        sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(50), default='scheduled'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_social_schedules_time', 'social_schedules', ['scheduled_time'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 📚 SCHOLAR SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'scholar_references',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('title', sa.String(1000), nullable=False),
        sa.Column('authors', postgresql.JSON(), default=[]),
        sa.Column('year', sa.Integer()),
        sa.Column('source_type', sa.String(50)),
        sa.Column('journal', sa.String(500)),
        sa.Column('volume', sa.String(50)),
        sa.Column('pages', sa.String(50)),
        sa.Column('doi', sa.String(255)),
        sa.Column('url', sa.String(1000)),
        sa.Column('abstract', sa.Text()),
        sa.Column('pdf_url', sa.String(1000)),
        sa.Column('tags', postgresql.JSON(), default=[]),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_scholar_references_owner', 'scholar_references', ['created_by'])
    op.create_index('ix_scholar_references_doi', 'scholar_references', ['doi'])
    
    op.create_table(
        'scholar_manuscripts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('title', sa.String(1000), nullable=False),
        sa.Column('abstract', sa.Text()),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('sections', postgresql.JSON(), default=[]),
        sa.Column('target_journal', sa.String(500)),
        sa.Column('submitted_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_scholar_manuscripts_owner', 'scholar_manuscripts', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🏛️ GOVERNMENT SPHERE
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'government_compliance',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('compliance_type', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('effective_date', sa.Date()),
        sa.Column('expiry_date', sa.Date()),
        sa.Column('license_number', sa.String(100)),
        sa.Column('issuing_authority', sa.String(255)),
        sa.Column('documents', postgresql.JSON(), default=[]),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_government_compliance_owner', 'government_compliance', ['created_by'])
    op.create_index('ix_government_compliance_expiry', 'government_compliance', ['expiry_date'])
    
    op.create_table(
        'government_clinical_trials',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('trial_id', sa.String(100), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('phase', sa.String(20)),
        sa.Column('status', sa.String(50), default='planning'),
        sa.Column('start_date', sa.Date()),
        sa.Column('end_date', sa.Date()),
        sa.Column('target_enrollment', sa.Integer()),
        sa.Column('current_enrollment', sa.Integer(), default=0),
        sa.Column('reb_approval', sa.Boolean(), default=False),
        sa.Column('reb_approval_date', sa.Date()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_government_trials_owner', 'government_clinical_trials', ['created_by'])
    
    # ═══════════════════════════════════════════════════════════════════════
    # 🤝 MY TEAM SPHERE (R&D Rule #4)
    # ═══════════════════════════════════════════════════════════════════════
    
    op.create_table(
        'team_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255)),
        sa.Column('role', sa.String(100)),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('sort_name', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_team_members_owner', 'team_members', ['created_by'])
    # Alphabetical ordering (R&D Rule #5)
    op.create_index('ix_team_members_alpha', 'team_members', ['created_by', 'sort_name'])
    
    op.create_table(
        'team_agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('agent_type', sa.String(100), nullable=False),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('capabilities', postgresql.JSON(), default=[]),
        sa.Column('token_budget', sa.Integer(), default=10000),
        sa.Column('tokens_used', sa.Integer(), default=0),
        # R&D Rule #4 audit: track who hired (must be human)
        sa.Column('hired_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('hired_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('hire_checkpoint_id', postgresql.UUID(as_uuid=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_team_agents_owner', 'team_agents', ['created_by'])
    
    op.create_table(
        'team_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('identities.id'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('priority', sa.String(20), default='medium'),
        sa.Column('assignee_type', sa.String(50)),
        sa.Column('assignee_id', postgresql.UUID(as_uuid=True)),
        sa.Column('due_date', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_team_tasks_owner', 'team_tasks', ['created_by'])
    # Chronological ordering (R&D Rule #5)
    op.create_index('ix_team_tasks_chrono', 'team_tasks', ['created_by', 'created_at'])


def downgrade() -> None:
    """Drop all tables."""
    
    # My Team
    op.drop_table('team_tasks')
    op.drop_table('team_agents')
    op.drop_table('team_members')
    
    # Government
    op.drop_table('government_clinical_trials')
    op.drop_table('government_compliance')
    
    # Scholar
    op.drop_table('scholar_manuscripts')
    op.drop_table('scholar_references')
    
    # Social
    op.drop_table('social_schedules')
    op.drop_table('social_posts')
    
    # Community
    op.drop_table('community_events')
    op.drop_table('community_groups')
    
    # Entertainment
    op.drop_table('entertainment_stream_history')
    op.drop_table('entertainment_playlists')
    
    # Creative
    op.drop_table('creative_projects')
    op.drop_table('creative_assets')
    
    # Business
    op.drop_table('business_projects')
    op.drop_table('business_invoices')
    op.drop_table('business_contacts')
    
    # Personal
    op.drop_table('personal_habits')
    op.drop_table('personal_tasks')
    op.drop_table('personal_notes')
    
    # Core
    op.drop_table('audit_logs')
    op.drop_table('checkpoints')
    op.drop_table('thread_events')
    op.drop_table('threads')
    op.drop_table('identities')
    
    # Enums
    op.execute('DROP TYPE IF EXISTS auditlogaction')
    op.execute('DROP TYPE IF EXISTS threadeventtype')
    op.execute('DROP TYPE IF EXISTS checkpointtype')
    op.execute('DROP TYPE IF EXISTS checkpointstatus')
    op.execute('DROP TYPE IF EXISTS visibility')
    op.execute('DROP TYPE IF EXISTS threadtype')
    op.execute('DROP TYPE IF EXISTS threadstatus')
    op.execute('DROP TYPE IF EXISTS spheretype')
