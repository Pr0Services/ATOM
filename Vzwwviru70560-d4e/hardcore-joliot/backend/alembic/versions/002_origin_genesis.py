"""ORIGIN-GENESIS-ULTIMA tables

Revision ID: 002_origin_genesis
Revises: 001_initial
Create Date: 2026-01-08

Tables Created:
- origin_nodes (core technology/discovery/practice)
- origin_causal_links (directed graph edges)
- origin_universal_links (cross-entity typed connections)
- origin_media_assets (film/book/game outputs)
- origin_civilization (language/empire/architecture pillars)
- origin_customs (anthropology & daily life)
- origin_legacy (belief/body/planet adaptation)
- origin_bio_eco (gene-culture + environmental feedback)
- origin_expert_validations (Rule #6 audit trail)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers
revision = '002_origin_genesis'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ═══════════════════════════════════════════════════════════════════════════
    # ORIGIN NODES — Core Technology/Discovery/Practice
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_nodes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        
        # Temporal positioning
        sa.Column('epoch', sa.String(100), nullable=True),
        sa.Column('exact_date', sa.String(100), nullable=True),
        sa.Column('date_start', sa.String(100), nullable=True),
        sa.Column('date_end', sa.String(100), nullable=True),
        sa.Column('date_certainty', sa.Float, nullable=False, server_default='0.8'),
        
        # Content
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('metadata_json', JSONB, nullable=True),
        sa.Column('geopolitical_context', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_by', UUID(as_uuid=True), nullable=True),
        
        # Validation lifecycle
        sa.Column('is_validated', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('validated_by', JSONB, nullable=True),
        sa.Column('validation_status', sa.String(50), nullable=False, server_default='pending'),
    )
    
    op.create_index('ix_origin_nodes_name', 'origin_nodes', ['name'])
    op.create_index('ix_origin_nodes_epoch', 'origin_nodes', ['epoch'])
    op.create_index('ix_origin_nodes_name_epoch', 'origin_nodes', ['name', 'epoch'])
    op.create_index('ix_origin_nodes_validation', 'origin_nodes', ['validation_status'])
    op.create_index('ix_origin_nodes_created_at', 'origin_nodes', ['created_at'])

    # ═══════════════════════════════════════════════════════════════════════════
    # CAUSAL LINKS — Directed Graph Edges
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_causal_links',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('trigger_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('result_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('link_strength', sa.Float, nullable=False, server_default='1.0'),
        sa.Column('link_type', sa.String(100), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('evidence', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
        sa.Column('validation_timestamp', sa.DateTime(timezone=True), nullable=True),
        
        sa.UniqueConstraint('trigger_id', 'result_id', name='uq_causal_link'),
    )
    
    op.create_index('ix_causal_links_trigger', 'origin_causal_links', ['trigger_id'])
    op.create_index('ix_causal_links_result', 'origin_causal_links', ['result_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # UNIVERSAL LINKS — Cross-Entity Typed Connections
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_universal_links',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('from_type', sa.String(50), nullable=False),
        sa.Column('from_id', UUID(as_uuid=True), nullable=False),
        sa.Column('to_type', sa.String(50), nullable=False),
        sa.Column('to_id', UUID(as_uuid=True), nullable=False),
        sa.Column('relation', sa.String(100), nullable=False),
        sa.Column('weight', sa.Float, nullable=False, server_default='1.0'),
        sa.Column('evidence', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
        
        sa.UniqueConstraint('from_type', 'from_id', 'to_type', 'to_id', 'relation', name='uq_universal_link'),
    )
    
    op.create_index('ix_universal_links_from', 'origin_universal_links', ['from_type', 'from_id'])
    op.create_index('ix_universal_links_to', 'origin_universal_links', ['to_type', 'to_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # MEDIA ASSETS — Film/Book/Game Outputs
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_media_assets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('asset_type', sa.String(50), nullable=False),
        sa.Column('format', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('content', JSONB, nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.Column('production_status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('source_node_snapshot', JSONB, nullable=True),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_by', UUID(as_uuid=True), nullable=True),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
    )
    
    op.create_index('ix_origin_media_node_type', 'origin_media_assets', ['node_id', 'asset_type'])
    op.create_index('ix_origin_media_status', 'origin_media_assets', ['production_status'])

    # ═══════════════════════════════════════════════════════════════════════════
    # CIVILIZATION PILLARS — Language/Empire/Architecture
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_civilization',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('migration_flow', JSONB, nullable=True),
        sa.Column('architectural_style', sa.String(200), nullable=True),
        sa.Column('literature_refs', JSONB, nullable=True),
        sa.Column('tools_used', JSONB, nullable=True),
        sa.Column('evidence', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
    )
    
    op.create_index('ix_origin_civilization_node_category', 'origin_civilization', ['node_id', 'category'])

    # ═══════════════════════════════════════════════════════════════════════════
    # CUSTOMS — Anthropology & Daily Life
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_customs',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('custom_name', sa.String(500), nullable=False),
        sa.Column('evolution_stage', sa.String(50), nullable=False),
        sa.Column('impact_on_daily_life', JSONB, nullable=True),
        sa.Column('region', sa.String(200), nullable=True),
        sa.Column('time_period', sa.String(200), nullable=True),
        sa.Column('sources', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
    )
    
    op.create_index('ix_origin_customs_name', 'origin_customs', ['custom_name'])
    op.create_index('ix_origin_customs_node_stage', 'origin_customs', ['node_id', 'evolution_stage'])

    # ═══════════════════════════════════════════════════════════════════════════
    # LEGACY — Belief/Body/Planet Adaptation
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_legacy',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('belief_system', sa.String(200), nullable=True),
        sa.Column('world_mystery_link', sa.String(500), nullable=True),
        sa.Column('human_talents', JSONB, nullable=True),
        sa.Column('sports_and_activities', JSONB, nullable=True),
        sa.Column('planetary_event', sa.String(200), nullable=True),
        sa.Column('adaptation_stage', sa.String(100), nullable=True),
        sa.Column('legacy_score', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('evidence', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
    )
    
    op.create_index('ix_origin_legacy_node_event', 'origin_legacy', ['node_id', 'planetary_event'])

    # ═══════════════════════════════════════════════════════════════════════════
    # BIO-ECO — Gene-Culture + Environmental Feedback
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_bio_eco',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('origin_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('genetic_mutation', sa.String(200), nullable=True),
        sa.Column('biological_impact', sa.Text, nullable=True),
        sa.Column('env_modification', sa.String(200), nullable=True),
        sa.Column('biodiversity_shift', JSONB, nullable=True),
        sa.Column('feedback_loop_description', sa.Text, nullable=True),
        sa.Column('feedback_type', sa.String(100), nullable=True),
        sa.Column('evidence', JSONB, nullable=False, server_default='{}'),
        sa.Column('is_hypothesis', sa.Boolean, nullable=False, server_default='true'),
        sa.Column('confidence_level', sa.Float, nullable=False, server_default='0.3'),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('validated_by_agent', sa.String(100), nullable=True),
        sa.Column('validation_notes', sa.Text, nullable=True),
    )
    
    op.create_index('ix_origin_bioeco_mutation', 'origin_bio_eco', ['genetic_mutation'])
    op.create_index('ix_origin_bioeco_env', 'origin_bio_eco', ['env_modification'])
    op.create_index('ix_origin_bioeco_node_mutation', 'origin_bio_eco', ['node_id', 'genetic_mutation'])

    # ═══════════════════════════════════════════════════════════════════════════
    # EXPERT VALIDATIONS — Rule #6 Audit Trail
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'origin_expert_validations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', UUID(as_uuid=True), nullable=False),
        sa.Column('agent_id', sa.String(100), nullable=False),
        sa.Column('agent_role', sa.String(200), nullable=True),
        sa.Column('validation_type', sa.String(50), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('sources_verified', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_expert_validations_entity', 'origin_expert_validations', ['entity_type', 'entity_id'])
    op.create_index('ix_expert_validations_agent', 'origin_expert_validations', ['agent_id'])
    op.create_index('ix_expert_validations_created', 'origin_expert_validations', ['created_at'])


def downgrade() -> None:
    op.drop_table('origin_expert_validations')
    op.drop_table('origin_bio_eco')
    op.drop_table('origin_legacy')
    op.drop_table('origin_customs')
    op.drop_table('origin_civilization')
    op.drop_table('origin_media_assets')
    op.drop_table('origin_universal_links')
    op.drop_table('origin_causal_links')
    op.drop_table('origin_nodes')
