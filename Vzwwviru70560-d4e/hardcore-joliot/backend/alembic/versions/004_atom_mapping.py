"""AT-OM Mapping System tables

Revision ID: 004_atom_mapping
Revises: 003_origin_triggers
Create Date: 2026-01-08

Tables Created:
- atom_nodes (unified knowledge graph nodes)
- atom_causal_links (directed causal edges)
- atom_encyclopedia (curated entries for rendering)
- atom_sub_modules (generic extension point)
- atom_sensory_profiles (ergonomics, acoustics)
- atom_psycho_emotional_profiles (societal moods)
- atom_resource_footprints (extraction, gaia impact)
- atom_conceptual_drift (etymology, concept evolution)
- atom_logistics_networks (routes, supply chains)
- atom_harmonic_signatures (OPTIONAL creative layer)

R&D Compliance:
- Rule #6: All tables have created_at, created_by
- Evidence-first: provenance + confidence on all profiles
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers
revision = '004_atom_mapping'
down_revision = '003_origin_triggers'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ═══════════════════════════════════════════════════════════════════════════
    # ATOM NODES — Unified Knowledge Graph
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_nodes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(500), nullable=False),
        
        # Dimension classification
        sa.Column('dimension', sa.String(50), nullable=True),
        # PHYSICAL | BIOLOGICAL | SOCIAL | SPIRITUAL | CONCEPTUAL | ECOLOGICAL | LOGISTICAL | SENSORY
        
        # Time metadata
        sa.Column('epoch', sa.String(100), nullable=True),
        sa.Column('date_range', JSONB, nullable=True),  # {from, to, label, confidence}
        sa.Column('location', JSONB, nullable=True),  # {region, lat, lon, confidence}
        
        # Content
        sa.Column('description', sa.Text, nullable=True),
        
        # Multi-dimensional data summaries
        sa.Column('technical_specs', JSONB, nullable=True),
        sa.Column('biological_impact', JSONB, nullable=True),
        sa.Column('social_customs', JSONB, nullable=True),
        sa.Column('planetary_context', JSONB, nullable=True),
        sa.Column('psychology', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_by', UUID(as_uuid=True), nullable=True),
    )
    
    op.create_index('ix_atom_nodes_name', 'atom_nodes', ['name'])
    op.create_index('ix_atom_nodes_dimension', 'atom_nodes', ['dimension'])
    op.create_index('ix_atom_nodes_epoch', 'atom_nodes', ['epoch'])
    op.create_index('ix_atom_nodes_dim_epoch', 'atom_nodes', ['dimension', 'epoch'])

    # ═══════════════════════════════════════════════════════════════════════════
    # ATOM CAUSAL LINKS — Directed Graph Edges
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_causal_links',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('trigger_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('result_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        # Link metadata
        sa.Column('link_type', sa.String(50), nullable=False),
        # BIO | TECH | SOCIAL | SPIRITUAL | ECO | SENSORY | CONCEPT | LOGISTICS
        sa.Column('strength', sa.Float, nullable=False, server_default='1.0'),
        sa.Column('rationale', sa.Text, nullable=True),
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        
        sa.UniqueConstraint('trigger_id', 'result_id', name='uq_atom_causal_link'),
    )
    
    op.create_index('ix_atom_causal_trigger', 'atom_causal_links', ['trigger_id'])
    op.create_index('ix_atom_causal_result', 'atom_causal_links', ['result_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # ENCYCLOPEDIA ENTRIES — Curated Renderable Content
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_encyclopedia',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content_html', sa.Text, nullable=True),
        sa.Column('content_md', sa.Text, nullable=True),
        sa.Column('metadata_tags', JSONB, nullable=True),
        
        # Quality tracking
        sa.Column('completeness', sa.Float, nullable=False, server_default='0.0'),
        sa.Column('review_status', sa.String(50), nullable=False, server_default="'draft'"),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    
    op.create_index('ix_atom_encyclopedia_node', 'atom_encyclopedia', ['node_id'])
    op.create_index('ix_atom_encyclopedia_status', 'atom_encyclopedia', ['review_status'])

    # ═══════════════════════════════════════════════════════════════════════════
    # SENSORY PROFILES — Ergonomics, Acoustics, Other Senses
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_sensory_profiles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('ergonomics', JSONB, nullable=True),  # grip, posture, load, skeletal markers
        sa.Column('acoustics', JSONB, nullable=True),   # soundscape reconstruction
        sa.Column('other_senses', JSONB, nullable=True),# visual/olfactory/tactile hypotheses
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('assumptions', sa.Text, nullable=True),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_sensory_node', 'atom_sensory_profiles', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PSYCHO-EMOTIONAL PROFILES — Societal Moods, Motivations
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_psycho_emotional_profiles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('psycho_emotional', JSONB, nullable=True),
        # {societal_mood:[], drivers:[], counter_signals:[]}
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('assumptions', sa.Text, nullable=True),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_psycho_node', 'atom_psycho_emotional_profiles', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # RESOURCE FOOTPRINTS — Extraction, Gaia Impact
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_resource_footprints',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('resource_footprint', JSONB, nullable=True),
        # {materials:[], extraction:{}, gaia_impact:{}, lifecycle:{}}
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('assumptions', sa.Text, nullable=True),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_resource_node', 'atom_resource_footprints', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # CONCEPTUAL DRIFT — Etymology, Concept Evolution
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_conceptual_drift',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('concept_evolution', JSONB, nullable=True),
        # {etymology:{}, semantic_shifts:[], cultural_contexts:[], modern_meanings:[]}
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('assumptions', sa.Text, nullable=True),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_concept_node', 'atom_conceptual_drift', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # LOGISTICS NETWORKS — Routes, Supply Chains, Infrastructure
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_logistics_networks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        sa.Column('logistics_data', JSONB, nullable=True),
        # {routes:[], nodes:[], cables:[], orbits:[], supply_chains:[], bottlenecks:[]}
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('assumptions', sa.Text, nullable=True),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_logistics_node', 'atom_logistics_networks', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # HARMONIC SIGNATURES — OPTIONAL Creative Layer (disabled by default)
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_harmonic_signatures',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        # Gematria/numeric signatures (creative, NOT scientific)
        sa.Column('numeric_signatures', JSONB, nullable=True),
        sa.Column('vibration_mapping', JSONB, nullable=True),  # UX sonification hints
        
        # MANDATORY disclaimer for UI
        sa.Column('interpretive_note', sa.Text, nullable=True),
        
        # Keep confidence LOW by default (interpretive layer)
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.2'),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_harmonic_node', 'atom_harmonic_signatures', ['node_id'])

    # ═══════════════════════════════════════════════════════════════════════════
    # SUB-MODULES — Generic Extension Point
    # ═══════════════════════════════════════════════════════════════════════════
    op.create_table(
        'atom_sub_modules',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('atom_nodes.id', ondelete='CASCADE'), nullable=False),
        
        # Free-form JSON for specialized data
        sa.Column('sensory_data', JSONB, nullable=True),
        sa.Column('psycho_emotional', JSONB, nullable=True),
        sa.Column('resource_footprint', JSONB, nullable=True),
        sa.Column('conceptual_drift', JSONB, nullable=True),
        sa.Column('logistics_networks', JSONB, nullable=True),
        
        # Evidence tracking
        sa.Column('confidence', sa.Float, nullable=False, server_default='0.5'),
        sa.Column('provenance', JSONB, nullable=True),
        
        # Rule #6: Traceability
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', UUID(as_uuid=True), nullable=False),
    )
    
    op.create_index('ix_atom_submodule_node', 'atom_sub_modules', ['node_id'])


def downgrade() -> None:
    op.drop_table('atom_sub_modules')
    op.drop_table('atom_harmonic_signatures')
    op.drop_table('atom_logistics_networks')
    op.drop_table('atom_conceptual_drift')
    op.drop_table('atom_resource_footprints')
    op.drop_table('atom_psycho_emotional_profiles')
    op.drop_table('atom_sensory_profiles')
    op.drop_table('atom_encyclopedia')
    op.drop_table('atom_causal_links')
    op.drop_table('atom_nodes')
