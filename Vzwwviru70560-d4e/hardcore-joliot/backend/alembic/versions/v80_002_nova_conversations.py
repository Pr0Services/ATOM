"""
Add nova_conversations table for chat history persistence.

Revision ID: v80_002_nova_conversations
Revises: v80_001_initial
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'v80_002_nova_conversations'
down_revision = 'v80_001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'nova_conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('identities.id', ondelete='CASCADE'), nullable=False),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('threads.id', ondelete='SET NULL'), nullable=True),
        sa.Column('agent_name', sa.String(50), default='nova'),
        sa.Column('status', sa.String(50), default='active'),
        sa.Column('messages', postgresql.JSONB, default=[]),
        sa.Column('total_tokens', sa.Integer, default=0),
    )

    op.create_index('ix_nova_conversations_owner', 'nova_conversations', ['owner_id'])
    op.create_index('ix_nova_conversations_thread', 'nova_conversations', ['thread_id'])


def downgrade() -> None:
    op.drop_index('ix_nova_conversations_thread')
    op.drop_index('ix_nova_conversations_owner')
    op.drop_table('nova_conversations')
