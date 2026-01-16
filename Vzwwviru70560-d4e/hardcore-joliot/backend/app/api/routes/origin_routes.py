"""
═══════════════════════════════════════════════════════════════════════════════
ORIGIN-GENESIS-ULTIMA — API Routes (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

REST API endpoints for ORIGIN system.
All endpoints enforce Rule #6 traceability.
"""

from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.master_origin import (
    OriginNode,
    OriginMediaAsset,
    OriginCivilizationPillar,
    OriginCustomEvolution,
    OriginHumanLegacy,
    OriginBioEvolution,
    OriginExpertValidation,
)
from app.schemas.origin_schemas import (
    # Node
    OriginNodeCreate, OriginNodeUpdate, OriginNodeResponse, OriginNodeList,
    # Links
    CausalLinkCreate, CausalLinkResponse,
    UniversalLinkCreate, UniversalLinkResponse,
    # Media
    MediaAssetCreate, MediaAssetUpdate, MediaAssetResponse,
    # Civilization
    CivilizationPillarCreate, CivilizationPillarResponse,
    # Customs
    CustomEvolutionCreate, CustomEvolutionResponse,
    # Legacy
    HumanLegacyCreate, HumanLegacyResponse,
    # Bio-Eco
    BioEvolutionCreate, BioEvolutionResponse,
    # Validation
    ExpertValidationCreate, ExpertValidationResponse,
    # Nexus
    NexusCandidateResponse, CausalChainResponse, NodeFullContextResponse,
)
from app.services.causal_nexus_service import CausalNexusService


router = APIRouter(prefix="/origin", tags=["ORIGIN-GENESIS"])


# ═══════════════════════════════════════════════════════════════════════════════
# ORIGIN NODES
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/nodes", response_model=OriginNodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node(
    data: OriginNodeCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new Origin Node.
    
    Rule #6: created_by is MANDATORY in request body.
    """
    service = CausalNexusService(db)
    node = await service.create_node(
        name=data.name,
        created_by=data.created_by,
        epoch=data.epoch,
        exact_date=data.exact_date,
        description=data.description,
        metadata_json=data.metadata_json,
        geopolitical_context=data.geopolitical_context,
    )
    await db.commit()
    await db.refresh(node)
    return node


@router.get("/nodes", response_model=OriginNodeList)
async def list_nodes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    epoch: Optional[str] = None,
    validation_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List origin nodes with pagination and filters."""
    query = select(OriginNode)
    
    if epoch:
        query = query.where(OriginNode.epoch == epoch)
    if validation_status:
        query = query.where(OriginNode.validation_status == validation_status)
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginate
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = list(result.scalars().all())
    
    return OriginNodeList(items=items, total=total, page=page, page_size=page_size)


@router.get("/nodes/{node_id}", response_model=OriginNodeResponse)
async def get_node(
    node_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a single origin node by ID."""
    service = CausalNexusService(db)
    node = await service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return node


@router.put("/nodes/{node_id}", response_model=OriginNodeResponse)
async def update_node(
    node_id: UUID,
    data: OriginNodeUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an origin node.
    
    Rule #6: updated_by is MANDATORY.
    """
    service = CausalNexusService(db)
    node = await service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    
    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "updated_by":
            setattr(node, field, value)
    
    node.updated_by = data.updated_by
    
    await db.commit()
    await db.refresh(node)
    return node


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL LINKS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/links/causal", response_model=CausalLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_causal_link(
    data: CausalLinkCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a causal link between two nodes.
    
    Should only be called AFTER expert validation.
    """
    service = CausalNexusService(db)
    
    # Verify both nodes exist
    trigger = await service.get_node(data.trigger_id)
    result = await service.get_node(data.result_id)
    
    if not trigger:
        raise HTTPException(status_code=404, detail=f"Trigger node {data.trigger_id} not found")
    if not result:
        raise HTTPException(status_code=404, detail=f"Result node {data.result_id} not found")
    
    link_id = await service.create_causal_link(
        trigger_id=data.trigger_id,
        result_id=data.result_id,
        created_by=data.created_by,
        link_type=data.link_type.value,
        link_strength=data.link_strength,
        description=data.description,
        evidence=data.evidence,
        validated_by_agent=data.validated_by_agent,
    )
    
    await db.commit()
    
    # Fetch created link
    from app.models.master_origin import origin_causal_links
    result = await db.execute(
        select(origin_causal_links).where(origin_causal_links.c.id == link_id)
    )
    link = result.fetchone()
    
    return CausalLinkResponse(
        id=link.id,
        trigger_id=link.trigger_id,
        result_id=link.result_id,
        link_type=link.link_type,
        link_strength=link.link_strength,
        description=link.description,
        evidence=link.evidence,
        created_at=link.created_at,
        created_by=link.created_by,
        validated_by_agent=link.validated_by_agent,
        validation_timestamp=link.validation_timestamp,
    )


@router.post("/links/universal", response_model=UniversalLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_universal_link(
    data: UniversalLinkCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a universal cross-entity link."""
    service = CausalNexusService(db)
    
    link_id = await service.create_universal_link(
        from_type=data.from_type,
        from_id=data.from_id,
        to_type=data.to_type,
        to_id=data.to_id,
        relation=data.relation,
        created_by=data.created_by,
        weight=data.weight,
        evidence=data.evidence,
        validated_by_agent=data.validated_by_agent,
    )
    
    await db.commit()
    
    # Fetch created link
    from app.models.master_origin import origin_universal_links
    result = await db.execute(
        select(origin_universal_links).where(origin_universal_links.c.id == link_id)
    )
    link = result.fetchone()
    
    return UniversalLinkResponse(
        id=link.id,
        from_type=link.from_type,
        from_id=link.from_id,
        to_type=link.to_type,
        to_id=link.to_id,
        relation=link.relation,
        weight=link.weight,
        evidence=link.evidence,
        created_at=link.created_at,
        created_by=link.created_by,
        validated_by_agent=link.validated_by_agent,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA ASSETS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/media", response_model=MediaAssetResponse, status_code=status.HTTP_201_CREATED)
async def create_media_asset(
    data: MediaAssetCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a media asset linked to a node."""
    from uuid import uuid4
    from datetime import datetime
    
    # Verify node exists
    service = CausalNexusService(db)
    node = await service.get_node(data.node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {data.node_id} not found")
    
    asset = OriginMediaAsset(
        id=uuid4(),
        node_id=data.node_id,
        asset_type=data.asset_type.value,
        format=data.format.value,
        title=data.title,
        content=data.content,
        production_status=data.production_status,
        created_at=datetime.utcnow(),
        created_by=data.created_by,
        updated_at=datetime.utcnow(),
    )
    
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    
    return asset


@router.get("/nodes/{node_id}/media", response_model=List[MediaAssetResponse])
async def list_node_media(
    node_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List all media assets for a node."""
    result = await db.execute(
        select(OriginMediaAsset).where(OriginMediaAsset.node_id == node_id)
    )
    return list(result.scalars().all())


# ═══════════════════════════════════════════════════════════════════════════════
# CIVILIZATION PILLARS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/civilization", response_model=CivilizationPillarResponse, status_code=status.HTTP_201_CREATED)
async def create_civilization_pillar(
    data: CivilizationPillarCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a civilization pillar linked to a node."""
    from uuid import uuid4
    from datetime import datetime
    
    pillar = OriginCivilizationPillar(
        id=uuid4(),
        node_id=data.node_id,
        category=data.category.value,
        title=data.title,
        description=data.description,
        migration_flow=data.migration_flow,
        architectural_style=data.architectural_style,
        literature_refs=data.literature_refs,
        tools_used=data.tools_used,
        evidence=data.evidence,
        created_at=datetime.utcnow(),
        created_by=data.created_by,
    )
    
    db.add(pillar)
    await db.commit()
    await db.refresh(pillar)
    
    return pillar


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOMS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/customs", response_model=CustomEvolutionResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_evolution(
    data: CustomEvolutionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a custom evolution record."""
    from uuid import uuid4
    from datetime import datetime
    
    custom = OriginCustomEvolution(
        id=uuid4(),
        node_id=data.node_id,
        custom_name=data.custom_name,
        evolution_stage=data.evolution_stage.value,
        impact_on_daily_life=data.impact_on_daily_life,
        region=data.region,
        time_period=data.time_period,
        sources=data.sources,
        created_at=datetime.utcnow(),
        created_by=data.created_by,
    )
    
    db.add(custom)
    await db.commit()
    await db.refresh(custom)
    
    return custom


# ═══════════════════════════════════════════════════════════════════════════════
# HUMAN LEGACY
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/legacy", response_model=HumanLegacyResponse, status_code=status.HTTP_201_CREATED)
async def create_human_legacy(
    data: HumanLegacyCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a human legacy record."""
    from uuid import uuid4
    from datetime import datetime
    
    legacy = OriginHumanLegacy(
        id=uuid4(),
        node_id=data.node_id,
        belief_system=data.belief_system,
        world_mystery_link=data.world_mystery_link,
        human_talents=data.human_talents,
        sports_and_activities=data.sports_and_activities,
        planetary_event=data.planetary_event,
        adaptation_stage=data.adaptation_stage.value if data.adaptation_stage else None,
        legacy_score=data.legacy_score,
        evidence=data.evidence,
        created_at=datetime.utcnow(),
        created_by=data.created_by,
    )
    
    db.add(legacy)
    await db.commit()
    await db.refresh(legacy)
    
    return legacy


# ═══════════════════════════════════════════════════════════════════════════════
# BIO-EVOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/bio-eco", response_model=BioEvolutionResponse, status_code=status.HTTP_201_CREATED)
async def create_bio_evolution(
    data: BioEvolutionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a bio-evolution record.
    
    REQUIRES evidence field with sources.
    """
    service = CausalNexusService(db)
    
    # Verify node exists
    node = await service.get_node(data.node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {data.node_id} not found")
    
    bio_evo = await service.create_bio_evolution(
        node_id=data.node_id,
        created_by=data.created_by,
        genetic_mutation=data.genetic_mutation,
        biological_impact=data.biological_impact,
        env_modification=data.env_modification,
        biodiversity_shift=data.biodiversity_shift,
        feedback_loop_description=data.feedback_loop_description,
        feedback_type=data.feedback_type.value if data.feedback_type else None,
        evidence=data.evidence,
        is_hypothesis=data.is_hypothesis,
        confidence_level=data.confidence_level,
    )
    
    await db.commit()
    await db.refresh(bio_evo)
    
    return bio_evo


@router.get("/nodes/{node_id}/bio-eco", response_model=List[BioEvolutionResponse])
async def list_node_bio_evolutions(
    node_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List all bio-evolution records for a node."""
    service = CausalNexusService(db)
    return await service.find_related_bio_evolutions(node_id)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERT VALIDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/validations", response_model=ExpertValidationResponse, status_code=status.HTTP_201_CREATED)
async def record_expert_validation(
    data: ExpertValidationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Record an expert agent's validation decision.
    
    This is the core of Rule #6 compliance.
    """
    service = CausalNexusService(db)
    
    validation = await service.record_expert_validation(
        entity_type=data.entity_type,
        entity_id=data.entity_id,
        agent_id=data.agent_id,
        validation_type=data.validation_type.value,
        created_by=data.created_by,
        agent_role=data.agent_role,
        confidence=data.confidence,
        notes=data.notes,
        sources_verified=data.sources_verified,
    )
    
    await db.commit()
    await db.refresh(validation)
    
    return validation


@router.get("/validations/{entity_type}/{entity_id}", response_model=List[ExpertValidationResponse])
async def get_entity_validations(
    entity_type: str,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get all validations for a specific entity."""
    result = await db.execute(
        select(OriginExpertValidation).where(
            OriginExpertValidation.entity_type == entity_type,
            OriginExpertValidation.entity_id == entity_id,
        ).order_by(OriginExpertValidation.created_at.desc())
    )
    return list(result.scalars().all())


# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/nodes/{node_id}/nexus-candidates", response_model=NexusCandidateResponse)
async def build_nexus_candidates(
    node_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Build candidate causal connections for a node.
    
    IMPORTANT: These are HYPOTHESES requiring expert validation.
    """
    service = CausalNexusService(db)
    
    try:
        candidates = await service.build_nexus_candidates(node_id)
        return candidates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/nodes/{node_id}/causal-chain", response_model=CausalChainResponse)
async def get_causal_chain(
    node_id: UUID,
    max_depth: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """Traverse the causal graph from a node."""
    service = CausalNexusService(db)
    
    # Verify node exists
    node = await service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    
    chain = await service.get_causal_chain(node_id, max_depth)
    
    return CausalChainResponse(
        start_node_id=str(node_id),
        chain=chain,
        total_links=len(chain),
        max_depth_reached=max(c["depth"] for c in chain) if chain else 0,
    )


@router.get("/nodes/{node_id}/full-context", response_model=NodeFullContextResponse)
async def get_node_full_context(
    node_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get complete context for a node including all related entities."""
    service = CausalNexusService(db)
    
    try:
        context = await service.get_node_full_context(node_id)
        return context
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/agents")
async def list_expert_agents():
    """List all available expert agents."""
    from app.agents.templates.origin_experts import AGENT_REGISTRY
    
    return {
        "total": len(AGENT_REGISTRY),
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "category": agent.category.value,
                "role_description": agent.role_description,
                "can_validate_facts": agent.can_validate_facts,
                "can_generate_content": agent.can_generate_content,
            }
            for agent in AGENT_REGISTRY.values()
        ]
    }


@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    """Get details for a specific expert agent."""
    from app.agents.templates.origin_experts import get_agent
    
    agent = get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return {
        "id": agent.id,
        "name": agent.name,
        "category": agent.category.value,
        "role_description": agent.role_description,
        "expertise_domains": [d.value for d in agent.expertise_domains],
        "validation_scope": agent.validation_scope,
        "constraints": agent.constraints,
        "required_sources": agent.required_sources,
        "can_validate_facts": agent.can_validate_facts,
        "can_generate_content": agent.can_generate_content,
        "prompt_template": agent.prompt_template,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def origin_health():
    """Health check for ORIGIN module."""
    return {
        "status": "healthy",
        "module": "ORIGIN-GENESIS-ULTIMA",
        "version": "V76",
        "tables": [
            "origin_nodes",
            "origin_causal_links",
            "origin_universal_links",
            "origin_media_assets",
            "origin_civilization",
            "origin_customs",
            "origin_legacy",
            "origin_bio_eco",
            "origin_expert_validations",
        ],
        "expert_agents": 21,
    }
