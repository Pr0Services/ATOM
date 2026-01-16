"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — API Routes (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Endpoints for:
- Gematria analysis (Pythagorean numerology)
- Sacred geometry coordinates
- Vibration profiles for visualization
- Guardrails status

⚠️ CREATIVE LAYER: All outputs are INTERPRETIVE, not scientific.

R&D Compliance:
- Rule #1: Human sovereignty (read-only, no autonomous actions)
- Rule #6: Traceability (user_id on all writes)
- Rule #7: Continuity (builds on evidence gating)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

# Import engines
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.atom_vibration_engine import (
    NumerologyEngine,
    AtomVibrationEngine,
    DISCLAIMER,
    MAX_INTERPRETIVE_CONFIDENCE
)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER SETUP
# ═══════════════════════════════════════════════════════════════════════════════

router = APIRouter()

# Initialize engines
numerology_engine = NumerologyEngine()
vibration_engine = AtomVibrationEngine(enabled=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class GematriaRequest(BaseModel):
    """Request for gematria analysis."""
    text: str = Field(..., min_length=1, max_length=500, description="Text to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {"text": "AT-OM"}
        }


class GematriaResponse(BaseModel):
    """Gematria analysis result."""
    text: str
    raw_score: int
    reduced_score: int
    is_master_number: bool
    sacred_geometry: Dict[str, float]
    frequency_hz: float
    disclaimer: str
    is_interpretive: bool = True


class VibrationProfileResponse(BaseModel):
    """Full vibration profile for visualization."""
    text: str
    raw_score: int
    reduced_score: int
    spiral: Dict[str, float]
    waveform: Dict[str, Any]
    mandala: Dict[str, Any]
    disclaimer: str
    is_interpretive: bool = True


class GuardrailsResponse(BaseModel):
    """Active guardrails for AT-OM system."""
    require_sources_for_high_confidence: bool
    max_interpretive_confidence: float
    harmonic_is_creative_only: bool
    disclaimer_required: bool
    store_uncertainty_explicitly: bool
    psycho_requires_counter_signals: bool
    no_absolute_truth_claims: bool


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", response_model=Dict[str, str])
async def atom_health():
    """
    Health check for AT-OM module.
    
    Returns:
        Status and module name
    """
    return {
        "status": "healthy",
        "module": "AT-OM Mapping System",
        "version": "1.0.0"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GEMATRIA ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/gematria/analyze", response_model=GematriaResponse)
async def analyze_gematria(request: GematriaRequest):
    """
    Analyze text using Pythagorean gematria.
    
    ⚠️ CREATIVE LAYER: Results are INTERPRETIVE, not scientific.
    
    Args:
        request: Text to analyze
        
    Returns:
        Gematria result with sacred geometry coordinates
    """
    try:
        # Calculate gematria
        result = numerology_engine.calculate_gematria(request.text)
        
        # Get sacred geometry coordinates
        coords = numerology_engine.get_sacred_geometry_coords(result.reduced_score)
        
        return GematriaResponse(
            text=request.text,
            raw_score=result.raw_score,
            reduced_score=result.reduced_score,
            is_master_number=result.is_master_number,
            sacred_geometry={
                "x": round(coords.x, 4),
                "y": round(coords.y, 4),
                "angle_degrees": round(coords.angle_degrees, 2),
                "radius": round(coords.radius, 4)
            },
            frequency_hz=coords.frequency_hz,
            disclaimer=DISCLAIMER,
            is_interpretive=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gematria/quick")
async def quick_gematria(
    text: str = Query(..., min_length=1, max_length=500, description="Text to analyze")
) -> Dict[str, Any]:
    """
    Quick gematria lookup via query parameter.
    
    Example: /api/v2/atom/gematria/quick?text=AT-OM
    
    Returns:
        Simplified gematria result
    """
    result = numerology_engine.calculate_gematria(text)
    return {
        "text": text,
        "raw": result.raw_score,
        "reduced": result.reduced_score,
        "is_master": result.is_master_number,
        "disclaimer": "Interpretive only"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# VIBRATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/vibration/profile", response_model=VibrationProfileResponse)
async def get_vibration_profile(request: GematriaRequest):
    """
    Generate full vibration profile for visualization.
    
    Includes:
    - Spiral coordinates (Fibonacci/Golden)
    - Waveform data (sinusoidal)
    - Mandala geometry (vertices, edges)
    
    ⚠️ CREATIVE LAYER: For D3.js/Three.js visualization only.
    """
    try:
        profile = vibration_engine.get_full_profile(request.text)
        
        return VibrationProfileResponse(
            text=request.text,
            raw_score=profile.gematria.raw_score,
            reduced_score=profile.gematria.reduced_score,
            spiral={
                "x": round(profile.coordinates.x, 4),
                "y": round(profile.coordinates.y, 4),
                "z": round(profile.coordinates.z, 4),
                "angle": round(profile.coordinates.angle_degrees, 2),
                "radius": round(profile.coordinates.radius, 4)
            },
            waveform={
                "frequency_hz": profile.coordinates.frequency_hz,
                "samples": 100  # Downsample for API response
            },
            mandala={
                "shape": "polygon",
                "vertices": profile.gematria.reduced_score,
                "color": "#228B22" if profile.gematria.reduced_score == 4 else "#000000"
            },
            disclaimer=DISCLAIMER,
            is_interpretive=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vibration/compare")
async def compare_vibrations(texts: List[str]) -> Dict[str, Any]:
    """
    Compare vibration profiles of multiple concepts.
    
    Concepts with the same reduced value will cluster together,
    showing "resonance" connections.
    
    ⚠️ CREATIVE LAYER: Artistic interpretation only.
    """
    if len(texts) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 texts per comparison")
    
    profiles = []
    clusters: Dict[int, List[str]] = {}
    
    for text in texts:
        result = numerology_engine.calculate_gematria(text)
        profiles.append({
            "text": text,
            "raw": result.raw_score,
            "reduced": result.reduced_score
        })
        
        # Cluster by reduced value
        rv = result.reduced_score
        if rv not in clusters:
            clusters[rv] = []
        clusters[rv].append(text)
    
    return {
        "profiles": profiles,
        "clusters": clusters,
        "resonance_groups": len(clusters),
        "disclaimer": DISCLAIMER,
        "is_interpretive": True
    }


# ═══════════════════════════════════════════════════════════════════════════════
# GUARDRAILS ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/guardrails", response_model=GuardrailsResponse)
async def get_guardrails():
    """
    Get active guardrails for AT-OM system.
    
    These guardrails ensure evidence-first posture
    and prevent absolutist truth claims.
    """
    return GuardrailsResponse(
        require_sources_for_high_confidence=True,
        max_interpretive_confidence=MAX_INTERPRETIVE_CONFIDENCE,
        harmonic_is_creative_only=True,
        disclaimer_required=True,
        store_uncertainty_explicitly=True,
        psycho_requires_counter_signals=True,
        no_absolute_truth_claims=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CONSISTENCY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/validate/{text}")
async def validate_consistency(text: str) -> Dict[str, Any]:
    """
    Validate gematria calculation consistency.
    
    Useful for testing cross-language normalization.
    """
    from app.services.atom_vibration_engine import validate_consistency as _validate
    
    result = numerology_engine.calculate_gematria(text)
    is_valid, msg = _validate(text, result.raw_score)
    
    return {
        "text": text,
        "raw_score": result.raw_score,
        "reduced_score": result.reduced_score,
        "is_consistent": is_valid,
        "message": msg,
        "normalized_input": text.lower().replace("-", "").replace(" ", "")
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = ["router"]
