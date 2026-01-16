"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM VIBRATION ENGINE — Sacred Geometry Visualization (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

⚠️ CRITICAL DISCLAIMER ⚠️
═══════════════════════════════════════════════════════════════════════════════
This module is PURELY ARTISTIC and INTERPRETIVE.

- NOT scientific evidence
- NOT factual causation
- NOT "truth" or "reality"

This is a CREATIVE LAYER for UX/UI visualization purposes only.
The numerological and geometric outputs are artistic metaphors,
not claims about the nature of reality.

USAGE:
- Feature flag: HARMONICS_ENABLED must be True to activate
- All outputs must display the disclaimer in UI
- confidence values are capped at 0.3 (interpretive layer)
═══════════════════════════════════════════════════════════════════════════════

Purpose:
- Calculate gematria values for AT·OM concepts (artistic interpretation)
- Generate sacred geometry coordinates for visualization
- Provide frequency mappings for sonification (film/game UX)

Integration:
- Frontend uses D3.js or Three.js for 3D rendering
- Coordinates feed into Fibonacci spiral, waveforms, mandalas
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Mandatory disclaimer for all outputs
DISCLAIMER = (
    "This is an artistic interpretation for visualization purposes only. "
    "Not scientific evidence. Not factual causation. "
    "Treat as creative metaphor, not truth."
)

# Golden ratio for sacred geometry calculations
PHI = (1 + 5**0.5) / 2

# Master numbers (not reduced in theosophical reduction)
MASTER_NUMBERS = {11, 22, 33}

# Maximum confidence for interpretive layer
MAX_INTERPRETIVE_CONFIDENCE = 0.3


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GematriaResult:
    """Result of gematria calculation with mandatory disclaimer."""
    input_text: str
    raw_score: int
    reduced_score: int
    is_master_number: bool
    disclaimer: str = field(default=DISCLAIMER)
    confidence: float = field(default=0.2)  # Low by design
    
    def to_dict(self) -> Dict:
        return {
            "input_text": self.input_text,
            "raw_score": self.raw_score,
            "reduced_score": self.reduced_score,
            "is_master_number": self.is_master_number,
            "disclaimer": self.disclaimer,
            "confidence": self.confidence,
            "interpretation": "artistic_only"
        }


@dataclass
class SacredGeometryCoords:
    """Sacred geometry coordinates for visualization."""
    x: float
    y: float
    z: float = 0.0
    frequency_hz: float = 0.0
    angle_degrees: float = 0.0
    radius: float = 0.0
    spiral_position: int = 0
    disclaimer: str = field(default=DISCLAIMER)
    
    def to_dict(self) -> Dict:
        return {
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "z": round(self.z, 4),
            "frequency_hz": round(self.frequency_hz, 2),
            "angle_degrees": round(self.angle_degrees, 2),
            "radius": round(self.radius, 4),
            "spiral_position": self.spiral_position,
            "disclaimer": self.disclaimer,
            "rendering_hint": "fibonacci_spiral"
        }


@dataclass
class VibrationProfile:
    """Complete vibration profile for a concept."""
    concept_name: str
    gematria: GematriaResult
    geometry: SacredGeometryCoords
    waveform: Dict
    mandala_type: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    disclaimer: str = field(default=DISCLAIMER)
    confidence: float = field(default=0.2)
    
    def to_dict(self) -> Dict:
        return {
            "concept_name": self.concept_name,
            "gematria": self.gematria.to_dict(),
            "geometry": self.geometry.to_dict(),
            "waveform": self.waveform,
            "mandala_type": self.mandala_type,
            "created_at": self.created_at.isoformat(),
            "disclaimer": self.disclaimer,
            "confidence": self.confidence,
            "layer_type": "creative_artistic",
            "is_scientific": False
        }


# ═══════════════════════════════════════════════════════════════════════════════
# NUMEROLOGY ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class NumerologyEngine:
    """
    Gematria and numerology calculator for artistic visualization.
    
    ⚠️ This is NOT scientific. Outputs are artistic metaphors.
    """
    
    def __init__(self):
        # Pythagorean/Western alphabet mapping (1-9 cycle)
        self.alphabet_map = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
            'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
            's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
        }
        
        # Extended mappings for accented characters (normalized)
        self.accent_map = {
            'à': 'a', 'â': 'a', 'ä': 'a', 'á': 'a',
            'è': 'e', 'ê': 'e', 'ë': 'e', 'é': 'e',
            'ì': 'i', 'î': 'i', 'ï': 'i', 'í': 'i',
            'ò': 'o', 'ô': 'o', 'ö': 'o', 'ó': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u', 'ú': 'u',
            'ç': 'c', 'ñ': 'n',
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for consistent calculation across languages."""
        text = text.lower().strip()
        
        # Replace accented characters
        for accented, base in self.accent_map.items():
            text = text.replace(accented, base)
        
        # Remove non-alphabetic characters
        text = ''.join(c for c in text if c.isalpha())
        
        return text
    
    def calculate_gematria(self, text: str) -> GematriaResult:
        """
        Calculate gematria value with theosophical reduction.
        
        Example: "AT-OM" -> 49 -> 13 -> 4
        
        Returns GematriaResult with mandatory disclaimer.
        """
        normalized = self.normalize_text(text)
        
        # Calculate raw score
        raw_score = sum(self.alphabet_map.get(char, 0) for char in normalized)
        
        # Theosophical reduction (keep master numbers)
        reduced = raw_score
        while reduced > 9 and reduced not in MASTER_NUMBERS:
            reduced = sum(int(digit) for digit in str(reduced))
        
        return GematriaResult(
            input_text=text,
            raw_score=raw_score,
            reduced_score=reduced,
            is_master_number=reduced in MASTER_NUMBERS,
            disclaimer=DISCLAIMER,
            confidence=0.2  # Always low for interpretive content
        )
    
    def get_sacred_geometry_coords(self, value: int) -> SacredGeometryCoords:
        """
        Generate coordinates based on golden ratio for visualization.
        
        Used for Fibonacci spiral positioning in UI.
        """
        # Angle based on 9-cycle (40° per number)
        angle = value * (360 / 9)
        
        # Radius expands using golden ratio
        radius = math.pow(PHI, value / 3)
        
        # Cartesian coordinates
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        
        # Z for 3D spiral (optional)
        z = value * 0.5
        
        # "Frequency" mapping (artistic, NOT real physics)
        # Base frequency 111.1 Hz * reduced number
        frequency = value * 111.1
        
        return SacredGeometryCoords(
            x=x,
            y=y,
            z=z,
            frequency_hz=frequency,
            angle_degrees=angle,
            radius=radius,
            spiral_position=value,
            disclaimer=DISCLAIMER
        )
    
    def get_mandala_type(self, reduced_value: int) -> str:
        """
        Determine mandala shape based on reduced number.
        
        Artistic mapping for visualization only.
        """
        mandala_map = {
            1: "circle",      # Unity, beginning
            2: "vesica_piscis", # Duality, balance
            3: "triangle",    # Trinity, creation
            4: "square",      # Stability, foundation
            5: "pentagon",    # Change, humanity
            6: "hexagon",     # Harmony, love
            7: "heptagon",    # Mystery, spirituality
            8: "octagon",     # Infinity, power
            9: "enneagram",   # Completion, wisdom
            11: "hendecagon", # Master intuition
            22: "star_of_david", # Master builder
            33: "flower_of_life", # Master teacher
        }
        return mandala_map.get(reduced_value, "circle")
    
    def get_waveform_params(self, reduced_value: int) -> Dict:
        """
        Generate waveform parameters for sonification/visualization.
        
        Artistic mapping for audio/visual UX.
        """
        base_freq = reduced_value * 111.1
        
        return {
            "type": "sine",
            "base_frequency_hz": base_freq,
            "harmonics": [base_freq * 2, base_freq * 3, base_freq * PHI],
            "amplitude": 0.5 + (reduced_value / 20),
            "phase_offset": reduced_value * 40,  # degrees
            "disclaimer": DISCLAIMER,
            "note": "Artistic sonification parameters, not scientific frequencies"
        }


# ═══════════════════════════════════════════════════════════════════════════════
# VIBRATION ENGINE (Main Interface)
# ═══════════════════════════════════════════════════════════════════════════════

class AtomVibrationEngine:
    """
    Main engine for AT·OM vibration calculations.
    
    ⚠️ CREATIVE LAYER ONLY ⚠️
    All outputs include mandatory disclaimers.
    Feature flag HARMONICS_ENABLED must be True.
    """
    
    def __init__(self, enabled: bool = False):
        """
        Initialize engine.
        
        Args:
            enabled: Must be True to activate (default False for safety)
        """
        self.enabled = enabled
        self.numerology = NumerologyEngine()
        self._disclaimer = DISCLAIMER
    
    def calculate_vibration_profile(self, concept_name: str) -> Optional[VibrationProfile]:
        """
        Calculate complete vibration profile for a concept.
        
        Returns None if engine is disabled.
        """
        if not self.enabled:
            return None
        
        # Calculate gematria
        gematria = self.numerology.calculate_gematria(concept_name)
        
        # Get geometry coordinates
        geometry = self.numerology.get_sacred_geometry_coords(gematria.reduced_score)
        
        # Get waveform params
        waveform = self.numerology.get_waveform_params(gematria.reduced_score)
        
        # Get mandala type
        mandala = self.numerology.get_mandala_type(gematria.reduced_score)
        
        return VibrationProfile(
            concept_name=concept_name,
            gematria=gematria,
            geometry=geometry,
            waveform=waveform,
            mandala_type=mandala,
            disclaimer=DISCLAIMER,
            confidence=0.2  # Always low
        )
    
    def batch_calculate(self, concepts: List[str]) -> List[Dict]:
        """
        Calculate vibration profiles for multiple concepts.
        
        Useful for comparing resonance patterns (artistic interpretation).
        """
        if not self.enabled:
            return []
        
        results = []
        for concept in concepts:
            profile = self.calculate_vibration_profile(concept)
            if profile:
                results.append(profile.to_dict())
        
        return results
    
    def find_resonant_concepts(
        self, 
        concepts: List[str]
    ) -> Dict[int, List[str]]:
        """
        Group concepts by their reduced number (same "vibration").
        
        Example: Fire and AI might both reduce to 4.
        Artistic interpretation for visual alignment.
        """
        if not self.enabled:
            return {}
        
        groups: Dict[int, List[str]] = {}
        
        for concept in concepts:
            gematria = self.numerology.calculate_gematria(concept)
            reduced = gematria.reduced_score
            
            if reduced not in groups:
                groups[reduced] = []
            groups[reduced].append(concept)
        
        return groups
    
    @property
    def disclaimer(self) -> str:
        """Get the mandatory disclaimer text."""
        return self._disclaimer


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_engine(enabled: bool = False) -> AtomVibrationEngine:
    """
    Factory function to create vibration engine.
    
    Args:
        enabled: Feature flag (should come from HARMONICS_ENABLED config)
    """
    return AtomVibrationEngine(enabled=enabled)


def validate_consistency(text: str, expected_raw: int) -> Tuple[bool, str]:
    """
    Validate that gematria calculation is consistent.
    
    For Agent A verification across languages.
    """
    engine = NumerologyEngine()
    result = engine.calculate_gematria(text)
    
    if result.raw_score == expected_raw:
        return True, "Calculation consistent"
    else:
        return False, f"Mismatch: expected {expected_raw}, got {result.raw_score}"


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Demo (only runs when script is executed directly)
    engine = AtomVibrationEngine(enabled=True)
    
    # Example: AT-OM
    profile = engine.calculate_vibration_profile("AT-OM")
    if profile:
        print("═" * 60)
        print("AT·OM VIBRATION PROFILE (Artistic Interpretation)")
        print("═" * 60)
        print(f"Raw Score: {profile.gematria.raw_score}")
        print(f"Reduced: {profile.gematria.reduced_score}")
        print(f"Coordinates: ({profile.geometry.x:.2f}, {profile.geometry.y:.2f})")
        print(f"Frequency: {profile.geometry.frequency_hz:.1f} Hz")
        print(f"Mandala: {profile.mandala_type}")
        print("═" * 60)
        print(f"⚠️ {DISCLAIMER}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'AtomVibrationEngine',
    'NumerologyEngine',
    'GematriaResult',
    'SacredGeometryCoords',
    'VibrationProfile',
    'create_engine',
    'validate_consistency',
    'DISCLAIMER',
    'PHI',
    'MASTER_NUMBERS',
]
