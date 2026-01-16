"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — API Routes (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

REST endpoints for:
- ATOM Nodes (CRUD + validation)
- Causal Links (create, query, suggestions)
- Dimension Profiles (sensory, psychology, resources, concepts, logistics, harmonics)
- Encyclopedia Entries
- Global Synapse (unified suggestions)
- Gematria (creative layer)

All endpoints enforce Rule #6 traceability.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_session
from app.models.atom_models import (
    ATOMNode, EncyclopediaEntry, atom_causal_links,
    AtomSensoryProfile, AtomPsychoEmotionalProfile,
    AtomResourceFootprint, AtomConceptualDrift,
    AtomLogisticsNetwork, AtomHarmonicSignature
)
from app.schemas.atom_schemas import (
    ATOMNodeCreate, ATOMNodeUpdate, ATOMNodeResponse, ATOMNodeFull,
    CausalLinkCreate, CausalLinkResponse, CausalLinkCandidate,
    EncyclopediaEntryCreate, EncyclopediaEntryUpdate, EncyclopediaEntryResponse,
    SensoryProfileCreate, SensoryProfileResponse,
    PsychoEmotionalProfileCreate, PsychoEmotionalProfileResponse,
    ResourceFootprintCreate, ResourceFootprintResponse,
    ConceptualDriftCreate, ConceptualDriftResponse,
    LogisticsNetworkCreate, LogisticsNetworkResponse,
    HarmonicSignatureCreate, HarmonicSignatureResponse,
    UnifiedSuggestions, GematriaResult, GoldNodeCandidate, Guardrails,
    PaginatedNodes
)
from app.services.atom_services import (
    CausalNexusService, ResonanceEngine, GlobalSynapse, 
    GematriaService, HarmonicSynchronizer
)

router = APIRouter(prefix="/api/v2/atom", tags=["AT-OM Mapping"])


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH & GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AT-OM Mapping System",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/guardrails", response_model=Guardrails)
async def get_guardrails():
    """Get static guardrails for UI & agents."""
    return Guardrails()


# ═══════════════════════════════════════════════════════════════════════════════
# ATOM NODES
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/nodes", response_model=ATOMNodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node(
    data: ATOMNodeCreate,
    created_by: Optional[UUID] = Query(None, description="User ID for Rule #6 traceability"),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new ATOM node."""
    node = ATOMNode(
        name=data.name,
        dimension=data.dimension.value if data.dimension else None,
        epoch=data.epoch,
        date_range=data.date_range.model_dump() if data.date_range else None,
        location=data.location.model_dump() if data.location else None,
        description=data.description,
        technical_specs=data.technical_specs,
        biological_impact=data.biological_impact,
        social_customs=data.social_customs,
        planetary_context=data.planetary_context,
        psychology=data.psychology,
        validation_status="pending",
        created_by=created_by,
        created_at=datetime.utcnow()
    )
    
    session.add(node)
    await session.commit()
    await session.refresh(node)
    
    return node


@router.get("/nodes", response_model=PaginatedNodes)
async def list_nodes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    dimension: Optional[str] = None,
    epoch: Optional[str] = None,
    validation_status: Optional[str] = None,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """List ATOM nodes with pagination and filtering."""
    query = select(ATOMNode)
    
    # Apply filters
    if dimension:
        query = query.where(ATOMNode.dimension == dimension)
    if epoch:
        query = query.where(ATOMNode.epoch == epoch)
    if validation_status:
        query = query.where(ATOMNode.validation_status == validation_status)
    if search:
        query = query.where(
            or_(
                ATOMNode.name.ilike(f"%{search}%"),
                ATOMNode.description.ilike(f"%{search}%")
            )
        )
    
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar()
    
    # Paginate
    query = query.offset((page - 1) * size).limit(size)
    result = await session.execute(query)
    nodes = result.scalars().all()
    
    return PaginatedNodes(
        items=nodes,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/nodes/{node_id}", response_model=ATOMNodeResponse)
async def get_node(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a single ATOM node."""
    result = await session.execute(
        select(ATOMNode).where(ATOMNode.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return node


@router.get("/nodes/{node_id}/full")
async def get_node_full(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a node with all dimension profiles."""
    synapse = GlobalSynapse(session)
    result = await synapse.get_full_node(node_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return result


@router.put("/nodes/{node_id}", response_model=ATOMNodeResponse)
async def update_node(
    node_id: UUID,
    data: ATOMNodeUpdate,
    modified_by: Optional[UUID] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    """Update an ATOM node."""
    result = await session.execute(
        select(ATOMNode).where(ATOMNode.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "date_range" and value:
            value = value.model_dump() if hasattr(value, "model_dump") else value
        if field == "location" and value:
            value = value.model_dump() if hasattr(value, "model_dump") else value
        if field == "dimension" and value:
            value = value.value if hasattr(value, "value") else value
        setattr(node, field, value)
    
    node.modified_by = modified_by
    node.modified_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(node)
    
    return node


@router.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete an ATOM node (cascades to all profiles)."""
    result = await session.execute(
        select(ATOMNode).where(ATOMNode.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    await session.delete(node)
    await session.commit()


@router.post("/nodes/{node_id}/validate", response_model=ATOMNodeResponse)
async def validate_node(
    node_id: UUID,
    validated_by: UUID = Query(..., description="Validator user ID"),
    session: AsyncSession = Depends(get_async_session)
):
    """Mark a node as validated (human review gate)."""
    result = await session.execute(
        select(ATOMNode).where(ATOMNode.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node.validation_status = "validated"
    node.validated_by = validated_by
    node.validated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(node)
    
    return node


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL LINKS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/links", response_model=CausalLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    data: CausalLinkCreate,
    created_by: Optional[UUID] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a causal link between nodes."""
    nexus = CausalNexusService(session)
    
    try:
        result = await nexus.create_link(
            trigger_id=data.trigger_id,
            result_id=data.result_id,
            link_type=data.link_type.value,
            strength=data.strength,
            confidence=data.confidence,
            rationale=data.rationale,
            provenance=[p.model_dump() for p in data.provenance] if data.provenance else None,
            created_by=created_by
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/links/node/{node_id}")
async def get_links_for_node(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get all causal links involving a node."""
    nexus = CausalNexusService(session)
    return await nexus.get_links_for_node(node_id)


@router.get("/links/suggestions/{node_id}")
async def get_link_suggestions(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get suggested causal links for a node.
    
    These are CANDIDATES requiring human review.
    """
    nexus = CausalNexusService(session)
    candidates = await nexus.suggest_links(node_id)
    
    # Apply evidence gating
    gated = []
    for c in candidates:
        ok, reason = nexus.validate_link_evidence(c)
        gated.append({
            "trigger_id": c.trigger_id,
            "result_id": c.result_id,
            "link_type": c.link_type,
            "strength": c.strength,
            "confidence": c.confidence,
            "rationale": c.rationale,
            "provenance": c.provenance,
            "is_validated": ok,
            "gate_reason": reason if not ok else None
        })
    
    return {"node_id": str(node_id), "suggestions": gated}


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSION PROFILES
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/profiles/sensory", response_model=SensoryProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_sensory_profile(
    data: SensoryProfileCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a sensory profile for a node."""
    profile = AtomSensoryProfile(
        node_id=data.node_id,
        ergonomics=data.ergonomics,
        acoustics=data.acoustics,
        other_senses=data.other_senses,
        confidence=data.confidence,
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


@router.post("/profiles/psychology", response_model=PsychoEmotionalProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_psychology_profile(
    data: PsychoEmotionalProfileCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a psycho-emotional profile for a node.
    
    ⚠️ Requires counter_signals and uncertainty_notes for balance.
    """
    profile = AtomPsychoEmotionalProfile(
        node_id=data.node_id,
        psycho_emotional=data.psycho_emotional,
        confidence=data.confidence,
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


@router.post("/profiles/resources", response_model=ResourceFootprintResponse, status_code=status.HTTP_201_CREATED)
async def create_resource_profile(
    data: ResourceFootprintCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a resource footprint profile for a node."""
    profile = AtomResourceFootprint(
        node_id=data.node_id,
        resource_footprint=data.resource_footprint,
        confidence=data.confidence,
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


@router.post("/profiles/concepts", response_model=ConceptualDriftResponse, status_code=status.HTTP_201_CREATED)
async def create_concept_profile(
    data: ConceptualDriftCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a conceptual drift profile for a node."""
    profile = AtomConceptualDrift(
        node_id=data.node_id,
        conceptual_drift=data.conceptual_drift,
        confidence=data.confidence,
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


@router.post("/profiles/logistics", response_model=LogisticsNetworkResponse, status_code=status.HTTP_201_CREATED)
async def create_logistics_profile(
    data: LogisticsNetworkCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a logistics network profile for a node."""
    profile = AtomLogisticsNetwork(
        node_id=data.node_id,
        logistics_networks=data.logistics_networks,
        confidence=data.confidence,
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


@router.post("/profiles/harmonics", response_model=HarmonicSignatureResponse, status_code=status.HTTP_201_CREATED)
async def create_harmonic_profile(
    data: HarmonicSignatureCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a harmonic signature profile for a node.
    
    ⚠️ CREATIVE LAYER: Not scientific, interpretive only.
    """
    profile = AtomHarmonicSignature(
        node_id=data.node_id,
        numeric_signatures=data.numeric_signatures,
        vibration_mapping=data.vibration_mapping,
        is_interpretive=True,  # Always True
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None
    )
    
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    
    return profile


# ═══════════════════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/encyclopedia", response_model=EncyclopediaEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_encyclopedia_entry(
    data: EncyclopediaEntryCreate,
    created_by: Optional[UUID] = Query(None),
    session: AsyncSession = Depends(get_async_session)
):
    """Create an encyclopedia entry for a node."""
    entry = EncyclopediaEntry(
        node_id=data.node_id,
        title=data.title,
        content_html=data.content_html,
        content_md=data.content_md,
        metadata_tags=data.metadata_tags,
        completeness=data.completeness,
        review_status=data.review_status.value if data.review_status else "draft",
        provenance=[p.model_dump() for p in data.provenance] if data.provenance else None,
        created_by=created_by
    )
    
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    
    return entry


@router.get("/encyclopedia/node/{node_id}")
async def get_encyclopedia_entries(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get all encyclopedia entries for a node."""
    result = await session.execute(
        select(EncyclopediaEntry).where(EncyclopediaEntry.node_id == node_id)
    )
    entries = result.scalars().all()
    
    return {"node_id": str(node_id), "entries": entries}


@router.put("/encyclopedia/{entry_id}", response_model=EncyclopediaEntryResponse)
async def update_encyclopedia_entry(
    entry_id: UUID,
    data: EncyclopediaEntryUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Update an encyclopedia entry."""
    result = await session.execute(
        select(EncyclopediaEntry).where(EncyclopediaEntry.id == entry_id)
    )
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Encyclopedia entry not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "review_status" and value:
            value = value.value if hasattr(value, "value") else value
        if field == "provenance" and value:
            value = [p.model_dump() if hasattr(p, "model_dump") else p for p in value]
        setattr(entry, field, value)
    
    entry.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(entry)
    
    return entry


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL SYNAPSE
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/synapse/{node_id}/suggestions", response_model=UnifiedSuggestions)
async def get_unified_suggestions(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all suggestions for a node from causal nexus and resonance engine.
    
    Returns suggestions with evidence gating applied.
    """
    synapse = GlobalSynapse(session)
    return await synapse.build_unified_suggestions(node_id)


@router.get("/synapse/{node_id}/resonance")
async def get_resonance_suggestions(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """Get dimension resonance suggestions for a node."""
    engine = ResonanceEngine(session)
    suggestions = await engine.suggest(node_id)
    
    return {
        "node_id": str(node_id),
        "suggestions": [
            {
                "module": s.module,
                "payload": s.payload,
                "confidence": s.confidence,
                "rationale": s.rationale
            }
            for s in suggestions
        ],
        "minimum_fields": engine.minimum_fields()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GEMATRIA (CREATIVE LAYER)
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/gematria/analyze", response_model=GematriaResult)
async def analyze_gematria(
    text: str = Query(..., description="Text to analyze")
):
    """
    Analyze text using gematria methods.
    
    ⚠️ CREATIVE LAYER: This is interpretive, not scientific.
    """
    service = GematriaService()
    result = service.analyze(text)
    return result


@router.get("/gematria/node/{node_id}")
async def get_node_gematria(
    node_id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get gematria analysis for a node's name.
    
    ⚠️ CREATIVE LAYER: This is interpretive, not scientific.
    """
    result = await session.execute(
        select(ATOMNode).where(ATOMNode.id == node_id)
    )
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    service = GematriaService()
    analysis = service.analyze(node.name)
    
    return {
        "node_id": str(node_id),
        "node_name": node.name,
        "gematria": analysis
    }


# ═══════════════════════════════════════════════════════════════════════════════
# HARMONIC SYNCHRONIZER (CREATIVE LAYER)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/harmonics/gold-nodes")
async def scan_gold_nodes(
    limit: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Scan for "gold nodes" with multi-dimensional alignment.
    
    ⚠️ CREATIVE LAYER: These are storytelling hooks, not scientific findings.
    """
    synchronizer = HarmonicSynchronizer(session)
    candidates = await synchronizer.scan(limit=limit)
    
    return {
        "candidates": [
            {
                "node_id": c.node_id,
                "score": c.score,
                "reasons": c.reasons,
                "artifacts": c.artifacts
            }
            for c in candidates
        ],
        "disclaimer": "These are interpretive results for creative/media use only.",
        "is_interpretive": True
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats")
async def get_statistics(
    session: AsyncSession = Depends(get_async_session)
):
    """Get AT-OM system statistics."""
    # Count nodes
    nodes_result = await session.execute(select(func.count(ATOMNode.id)))
    nodes_count = nodes_result.scalar()
    
    # Count links
    links_result = await session.execute(select(func.count(atom_causal_links.c.id)))
    links_count = links_result.scalar()
    
    # Count by dimension
    dim_result = await session.execute(
        select(ATOMNode.dimension, func.count(ATOMNode.id))
        .group_by(ATOMNode.dimension)
    )
    by_dimension = {row[0]: row[1] for row in dim_result.fetchall()}
    
    # Count by validation status
    status_result = await session.execute(
        select(ATOMNode.validation_status, func.count(ATOMNode.id))
        .group_by(ATOMNode.validation_status)
    )
    by_status = {row[0]: row[1] for row in status_result.fetchall()}
    
    return {
        "total_nodes": nodes_count,
        "total_links": links_count,
        "by_dimension": by_dimension,
        "by_validation_status": by_status,
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = ["router"]
