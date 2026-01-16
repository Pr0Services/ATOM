"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM VIBRATION ENGINE — Visual Rendering for Sacred Geometry (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

This module transforms numerology calculations into visual coordinates for
frontend rendering. It prepares data for D3.js / Three.js visualization.

Components:
- CausalitySpiralRenderer: Fibonacci spiral positioning
- WaveformGenerator: Frequency-based sinusoidal waves  
- MandalaConstructor: Geometric forms based on reduced numbers
- VibrationDashboard: Unified orchestrator for all visual layers

⚠️ CREATIVE LAYER: All visualizations are INTERPRETIVE, not scientific.
   They serve artistic/narrative purposes for film, games, and storytelling.

Usage:
    from app.services.atom_vibration_engine import VibrationDashboard
    
    dashboard = VibrationDashboard()
    visual_data = dashboard.render_node("AT-OM")
    # Returns coordinates for D3.js/Three.js rendering

Frontend Integration:
    - D3.js: 2D spirals, waveforms, SVG mandalas
    - Three.js: 3D sacred geometry, particle systems, immersive XR
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Golden Ratio (Phi)
PHI = (1 + math.sqrt(5)) / 2

# Fibonacci sequence (first 20 terms for spiral)
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

# Master numbers (preserved in reduction)
MASTER_NUMBERS = {11, 22, 33}

# Pythagorean alphabet mapping
PYTHAGOREAN_MAP = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
    'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
    's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
}

# Geometric shapes for mandalas
MANDALA_SHAPES = {
    1: {"name": "point", "vertices": 1, "symbol": "●"},
    2: {"name": "line", "vertices": 2, "symbol": "━"},
    3: {"name": "triangle", "vertices": 3, "symbol": "△"},
    4: {"name": "square", "vertices": 4, "symbol": "□"},
    5: {"name": "pentagon", "vertices": 5, "symbol": "⬠"},
    6: {"name": "hexagon", "vertices": 6, "symbol": "⬡"},
    7: {"name": "heptagon", "vertices": 7, "symbol": "⬢"},
    8: {"name": "octagon", "vertices": 8, "symbol": "⯃"},
    9: {"name": "enneagon", "vertices": 9, "symbol": "⬣"},
    11: {"name": "hendecagon", "vertices": 11, "symbol": "✡", "is_master": True},
    22: {"name": "icosikaidigon", "vertices": 22, "symbol": "✶", "is_master": True},
    33: {"name": "triacontakaitrigon", "vertices": 33, "symbol": "❈", "is_master": True},
}

# Archetype colors (for visualization)
ARCHETYPE_COLORS = {
    1: {"hex": "#FFD700", "name": "Gold", "element": "Fire"},
    2: {"hex": "#C0C0C0", "name": "Silver", "element": "Water"},
    3: {"hex": "#FF4500", "name": "Orange", "element": "Fire"},
    4: {"hex": "#228B22", "name": "Green", "element": "Earth"},
    5: {"hex": "#87CEEB", "name": "Sky Blue", "element": "Air"},
    6: {"hex": "#FF69B4", "name": "Pink", "element": "Earth"},
    7: {"hex": "#9400D3", "name": "Violet", "element": "Water"},
    8: {"hex": "#8B4513", "name": "Brown", "element": "Earth"},
    9: {"hex": "#DC143C", "name": "Crimson", "element": "Fire"},
    11: {"hex": "#FFFFFF", "name": "White", "element": "Air", "is_master": True},
    22: {"hex": "#000000", "name": "Black", "element": "Earth", "is_master": True},
    33: {"hex": "#E6E6FA", "name": "Lavender", "element": "Water", "is_master": True},
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SpiralPoint:
    """A point on the Fibonacci/Golden spiral."""
    x: float
    y: float
    z: float = 0.0  # For 3D rendering
    angle: float = 0.0
    radius: float = 0.0
    fibonacci_index: int = 0
    label: str = ""


@dataclass
class WaveformData:
    """Sinusoidal waveform data for visualization."""
    frequency_hz: float
    amplitude: float
    phase: float
    samples: List[Tuple[float, float]] = field(default_factory=list)
    duration_seconds: float = 2.0


@dataclass
class MandalaGeometry:
    """Geometric mandala construction data."""
    center: Tuple[float, float]
    vertices: List[Tuple[float, float]]
    edges: List[Tuple[int, int]]
    shape_name: str
    symbol: str
    color: str
    layers: int = 3


@dataclass
class VibrationProfile:
    """Complete vibration profile for a concept."""
    text: str
    raw_value: int
    reduced_value: int
    reduction_path: List[int]
    spiral_position: SpiralPoint
    waveform: WaveformData
    mandala: MandalaGeometry
    archetype: Dict[str, Any]
    is_interpretive: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSALITY SPIRAL RENDERER
# ═══════════════════════════════════════════════════════════════════════════════

class CausalitySpiralRenderer:
    """
    Generates Fibonacci/Golden spiral coordinates for causality visualization.
    
    Concepts with the same reduced number align on the same radial axis,
    showing "resonance" across time and domains.
    
    Example:
        Fire (reduced=4) and AI (reduced=4) align on the same ray,
        suggesting a vibrational connection (INTERPRETIVE ONLY).
    """
    
    def __init__(self, scale: float = 50.0, z_lift: float = 10.0):
        self.scale = scale
        self.z_lift = z_lift  # Vertical lift per turn for 3D
    
    def get_spiral_point(
        self, 
        reduced_value: int, 
        sequence_index: int = 0
    ) -> SpiralPoint:
        """
        Calculate position on the golden spiral.
        
        Args:
            reduced_value: Theosophical reduction (1-9 or master)
            sequence_index: Position in the sequence (for multiple items)
            
        Returns:
            SpiralPoint with x, y, z coordinates
        """
        # Angle based on reduced value (40° per number on cycle of 9)
        base_angle = reduced_value * (360 / 9)
        
        # Add offset for sequence position (golden angle ≈ 137.5°)
        golden_angle = 360 / (PHI * PHI)
        angle = base_angle + (sequence_index * golden_angle)
        
        # Radius expands with phi
        radius = self.scale * math.pow(PHI, reduced_value / 3)
        
        # Apply offset for sequence
        radius *= (1 + sequence_index * 0.1)
        
        # Calculate coordinates
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        z = sequence_index * self.z_lift  # 3D lift
        
        return SpiralPoint(
            x=round(x, 4),
            y=round(y, 4),
            z=round(z, 4),
            angle=round(angle % 360, 2),
            radius=round(radius, 4),
            fibonacci_index=self._nearest_fibonacci_index(int(radius))
        )
    
    def _nearest_fibonacci_index(self, value: int) -> int:
        """Find nearest Fibonacci number index."""
        for i, fib in enumerate(FIBONACCI):
            if fib >= value:
                return i
        return len(FIBONACCI) - 1
    
    def generate_spiral_path(
        self, 
        num_points: int = 100,
        turns: float = 3.0
    ) -> List[Tuple[float, float]]:
        """
        Generate a complete spiral path for background rendering.
        
        Returns list of (x, y) coordinates for SVG/Canvas path.
        """
        points = []
        for i in range(num_points):
            t = i / num_points * turns * 2 * math.pi
            r = self.scale * math.exp(t / (2 * math.pi) * math.log(PHI))
            x = r * math.cos(t)
            y = r * math.sin(t)
            points.append((round(x, 2), round(y, 2)))
        return points


# ═══════════════════════════════════════════════════════════════════════════════
# WAVEFORM GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class WaveformGenerator:
    """
    Generates sinusoidal waveform data based on numerology frequencies.
    
    Each reduced number has a "symbolic frequency" (111.1 Hz base).
    This creates visual waves that represent the concept's "vibration".
    
    ⚠️ These are SYMBOLIC frequencies, not physical sound waves.
    """
    
    BASE_FREQUENCY = 111.1  # Hz (symbolic)
    SAMPLE_RATE = 1000  # Samples per second for smooth rendering
    
    def __init__(self, duration: float = 2.0):
        self.duration = duration
    
    def generate_waveform(
        self, 
        reduced_value: int,
        amplitude: float = 1.0,
        phase: float = 0.0
    ) -> WaveformData:
        """
        Generate waveform samples for visualization.
        
        Args:
            reduced_value: Number (1-9 or master)
            amplitude: Wave height (0.0 to 1.0)
            phase: Phase offset in radians
            
        Returns:
            WaveformData with samples for rendering
        """
        frequency = reduced_value * self.BASE_FREQUENCY
        samples = []
        
        num_samples = int(self.duration * self.SAMPLE_RATE)
        for i in range(num_samples):
            t = i / self.SAMPLE_RATE
            y = amplitude * math.sin(2 * math.pi * frequency * t + phase)
            samples.append((round(t, 4), round(y, 4)))
        
        return WaveformData(
            frequency_hz=round(frequency, 1),
            amplitude=amplitude,
            phase=phase,
            samples=samples,
            duration_seconds=self.duration
        )
    
    def generate_harmonic_series(
        self, 
        reduced_value: int,
        num_harmonics: int = 5
    ) -> List[WaveformData]:
        """
        Generate harmonic overtone series.
        
        Returns fundamental + harmonics for richer visualization.
        """
        harmonics = []
        for h in range(1, num_harmonics + 1):
            harmonic_value = reduced_value * h
            # Reduce if exceeds 9
            while harmonic_value > 9 and harmonic_value not in MASTER_NUMBERS:
                harmonic_value = sum(int(d) for d in str(harmonic_value))
            
            waveform = self.generate_waveform(
                harmonic_value,
                amplitude=1.0 / h,  # Decreasing amplitude
                phase=0.0
            )
            harmonics.append(waveform)
        
        return harmonics


# ═══════════════════════════════════════════════════════════════════════════════
# MANDALA CONSTRUCTOR
# ═══════════════════════════════════════════════════════════════════════════════

class MandalaConstructor:
    """
    Constructs geometric mandala shapes based on reduced numbers.
    
    Each number produces a specific polygon:
        1 = Point, 2 = Line, 3 = Triangle, 4 = Square, etc.
    
    Master numbers (11, 22, 33) produce complex multi-layered forms.
    """
    
    def __init__(self, radius: float = 100.0):
        self.radius = radius
    
    def construct_mandala(
        self, 
        reduced_value: int,
        center: Tuple[float, float] = (0.0, 0.0),
        layers: int = 3
    ) -> MandalaGeometry:
        """
        Construct mandala geometry for rendering.
        
        Args:
            reduced_value: Number determining shape
            center: Center point (x, y)
            layers: Number of concentric layers
            
        Returns:
            MandalaGeometry with vertices and edges
        """
        shape_info = MANDALA_SHAPES.get(reduced_value, MANDALA_SHAPES[9])
        color_info = ARCHETYPE_COLORS.get(reduced_value, ARCHETYPE_COLORS[9])
        
        num_vertices = shape_info["vertices"]
        all_vertices = []
        all_edges = []
        
        # Generate concentric layers
        for layer in range(layers):
            layer_radius = self.radius * (layer + 1) / layers
            layer_vertices = self._generate_polygon_vertices(
                num_vertices, 
                layer_radius, 
                center,
                rotation_offset=layer * (360 / num_vertices / 2)  # Alternate rotation
            )
            
            start_idx = len(all_vertices)
            all_vertices.extend(layer_vertices)
            
            # Connect vertices within layer
            for i in range(num_vertices):
                next_i = (i + 1) % num_vertices
                all_edges.append((start_idx + i, start_idx + next_i))
            
            # Connect to previous layer
            if layer > 0:
                prev_start = start_idx - num_vertices
                for i in range(num_vertices):
                    all_edges.append((prev_start + i, start_idx + i))
        
        return MandalaGeometry(
            center=center,
            vertices=all_vertices,
            edges=all_edges,
            shape_name=shape_info["name"],
            symbol=shape_info["symbol"],
            color=color_info["hex"],
            layers=layers
        )
    
    def _generate_polygon_vertices(
        self,
        num_vertices: int,
        radius: float,
        center: Tuple[float, float],
        rotation_offset: float = 0.0
    ) -> List[Tuple[float, float]]:
        """Generate vertices for a regular polygon."""
        vertices = []
        for i in range(num_vertices):
            angle = (360 / num_vertices) * i + rotation_offset - 90  # Start at top
            x = center[0] + radius * math.cos(math.radians(angle))
            y = center[1] + radius * math.sin(math.radians(angle))
            vertices.append((round(x, 4), round(y, 4)))
        return vertices


# ═══════════════════════════════════════════════════════════════════════════════
# VIBRATION DASHBOARD (ORCHESTRATOR)
# ═══════════════════════════════════════════════════════════════════════════════

class VibrationDashboard:
    """
    Unified orchestrator for all vibration visualizations.
    
    Combines:
    - Gematria calculation
    - Spiral positioning
    - Waveform generation
    - Mandala construction
    
    Returns complete data package for frontend rendering.
    
    ⚠️ CREATIVE LAYER: All outputs are INTERPRETIVE.
       This is an "architecture of frequencies" for artistic purposes.
    """
    
    DISCLAIMER = (
        "⚠️ CREATIVE LAYER: This visualization engine is for artistic/narrative "
        "purposes. The 'vibrations' and 'frequencies' are SYMBOLIC, not physical. "
        "All outputs are INTERPRETIVE and require human review."
    )
    
    def __init__(self):
        self.spiral = CausalitySpiralRenderer()
        self.waveform = WaveformGenerator()
        self.mandala = MandalaConstructor()
    
    def calculate_gematria(self, text: str) -> Tuple[int, int, List[int]]:
        """
        Calculate Pythagorean gematria with reduction path.
        
        Returns: (raw_value, reduced_value, reduction_path)
        """
        cleaned = text.lower().replace("-", "").replace(" ", "")
        raw = sum(PYTHAGOREAN_MAP.get(char, 0) for char in cleaned)
        
        reduced = raw
        path = [raw]
        while reduced > 9 and reduced not in MASTER_NUMBERS:
            reduced = sum(int(d) for d in str(reduced))
            path.append(reduced)
        
        return raw, reduced, path
    
    def get_archetype(self, reduced_value: int) -> Dict[str, Any]:
        """Get archetype information for a reduced value."""
        archetypes = {
            1: {"name": "The Beginning", "quality": "Initiative", "planet": "Sun"},
            2: {"name": "The Duality", "quality": "Balance", "planet": "Moon"},
            3: {"name": "The Creation", "quality": "Expression", "planet": "Jupiter"},
            4: {"name": "The Foundation", "quality": "Stability", "planet": "Uranus"},
            5: {"name": "The Change", "quality": "Freedom", "planet": "Mercury"},
            6: {"name": "The Harmony", "quality": "Love", "planet": "Venus"},
            7: {"name": "The Mystery", "quality": "Wisdom", "planet": "Neptune"},
            8: {"name": "The Power", "quality": "Authority", "planet": "Saturn"},
            9: {"name": "The Completion", "quality": "Universality", "planet": "Mars"},
            11: {"name": "The Illumination", "quality": "Vision", "planet": "Pluto", "is_master": True},
            22: {"name": "The Master Builder", "quality": "Mastery", "planet": "Vulcan", "is_master": True},
            33: {"name": "The Master Teacher", "quality": "Compassion", "planet": "Neptune", "is_master": True},
        }
        
        archetype = archetypes.get(reduced_value, archetypes[9])
        color = ARCHETYPE_COLORS.get(reduced_value, ARCHETYPE_COLORS[9])
        
        return {
            **archetype,
            "color": color["hex"],
            "color_name": color["name"],
            "element": color["element"],
            "is_interpretive": True
        }
    
    def render_node(
        self, 
        text: str,
        sequence_index: int = 0,
        include_harmonics: bool = False
    ) -> VibrationProfile:
        """
        Generate complete vibration profile for a concept.
        
        Args:
            text: Concept name (e.g., "AT-OM", "Fire", "Wheel")
            sequence_index: Position in sequence (for multiple items)
            include_harmonics: Include harmonic overtones
            
        Returns:
            VibrationProfile with all visual data
        """
        raw, reduced, path = self.calculate_gematria(text)
        
        return VibrationProfile(
            text=text,
            raw_value=raw,
            reduced_value=reduced,
            reduction_path=path,
            spiral_position=self.spiral.get_spiral_point(reduced, sequence_index),
            waveform=self.waveform.generate_waveform(reduced),
            mandala=self.mandala.construct_mandala(reduced),
            archetype=self.get_archetype(reduced),
            is_interpretive=True
        )
    
    def render_comparison(
        self, 
        texts: List[str]
    ) -> Dict[str, Any]:
        """
        Render multiple concepts for comparison visualization.
        
        Concepts with the same reduced value will cluster together,
        showing "resonance" connections.
        """
        profiles = []
        clusters = {}
        
        for i, text in enumerate(texts):
            profile = self.render_node(text, sequence_index=i)
            profiles.append(profile)
            
            # Cluster by reduced value
            rv = profile.reduced_value
            if rv not in clusters:
                clusters[rv] = []
            clusters[rv].append(text)
        
        return {
            "profiles": profiles,
            "clusters": clusters,
            "spiral_path": self.spiral.generate_spiral_path(),
            "is_interpretive": True,
            "disclaimer": self.DISCLAIMER
        }
    
    def export_for_d3(self, profile: VibrationProfile) -> Dict[str, Any]:
        """
        Export profile in D3.js-friendly format.
        
        Returns flat dictionary ready for JavaScript consumption.
        """
        return {
            "text": profile.text,
            "raw": profile.raw_value,
            "reduced": profile.reduced_value,
            "path": profile.reduction_path,
            # Spiral
            "spiral": {
                "x": profile.spiral_position.x,
                "y": profile.spiral_position.y,
                "angle": profile.spiral_position.angle,
                "radius": profile.spiral_position.radius
            },
            # Waveform (sampled for performance)
            "waveform": {
                "frequency": profile.waveform.frequency_hz,
                "amplitude": profile.waveform.amplitude,
                "samples": profile.waveform.samples[::10]  # Downsample for JS
            },
            # Mandala
            "mandala": {
                "shape": profile.mandala.shape_name,
                "symbol": profile.mandala.symbol,
                "color": profile.mandala.color,
                "vertices": profile.mandala.vertices,
                "edges": profile.mandala.edges
            },
            # Archetype
            "archetype": profile.archetype,
            # Metadata
            "is_interpretive": True
        }
    
    def export_for_threejs(self, profile: VibrationProfile) -> Dict[str, Any]:
        """
        Export profile in Three.js-friendly format with 3D coordinates.
        """
        d3_export = self.export_for_d3(profile)
        
        # Add 3D-specific data
        d3_export["spiral"]["z"] = profile.spiral_position.z
        d3_export["mandala"]["vertices_3d"] = [
            (v[0], v[1], 0.0) for v in profile.mandala.vertices
        ]
        
        return d3_export


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT NOTES
# ═══════════════════════════════════════════════════════════════════════════════

"""
NOTE POUR AGENT B (Integration/Frontend):
=========================================
Le dashboard doit utiliser D3.js ou Three.js pour rendre ces calculs:

1. SPIRALE DE CAUSALITÉ (D3.js / Three.js)
   - Utiliser `spiral_path` pour le fond
   - Placer chaque concept sur sa position `spiral.x`, `spiral.y`
   - Les concepts avec même `reduced` s'alignent sur le même rayon

2. ONDE DE FORME (D3.js / Canvas)
   - Dessiner une sinusoïde avec `waveform.samples`
   - La fréquence `waveform.frequency` donne le "rythme visuel"
   - Animer l'onde pour effet de "vibration"

3. MANDALA DE RÉSONANCE (SVG / Three.js)
   - Utiliser `mandala.vertices` et `mandala.edges`
   - Colorier avec `mandala.color`
   - Ajouter rotations lentes pour effet méditatif

4. ARCHITECTURE GLOBALE
   - L'utilisateur doit sentir que l'encyclopédie est une
     "architecture de fréquences" vivante
   - Chaque entrée "vibre" littéralement à l'écran


NOTE POUR AGENT A (QA/Validation):
==================================
1. Vérifier que les calculs de Gematria sont CONSTANTS
   - Même texte → même résultat (déterministe)
   - Cross-langue: normaliser avant calcul (accents, espaces)

2. Valider les GUARDRAILS:
   - Tous les outputs ont `is_interpretive: True`
   - Le disclaimer est toujours présent
   - Aucune affirmation de vérité scientifique

3. Tests de cohérence:
   - AT-OM → raw=13, reduced=4 (Pythagorean)
   - Frequency = 444.4 Hz
   - Mandala = Square (4 vertices)
   - Color = Green (#228B22)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Constants
    "PHI",
    "FIBONACCI",
    "MASTER_NUMBERS",
    "PYTHAGOREAN_MAP",
    "MANDALA_SHAPES",
    "ARCHETYPE_COLORS",
    # Data classes
    "SpiralPoint",
    "WaveformData",
    "MandalaGeometry",
    "VibrationProfile",
    # Renderers
    "CausalitySpiralRenderer",
    "WaveformGenerator",
    "MandalaConstructor",
    # Main orchestrator
    "VibrationDashboard",
]


# ═══════════════════════════════════════════════════════════════════════════════
# STANDALONE TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    dashboard = VibrationDashboard()
    
    # Test AT-OM
    profile = dashboard.render_node("AT-OM")
    
    print("═" * 60)
    print("AT-OM VIBRATION PROFILE")
    print("═" * 60)
    print(f"Text: {profile.text}")
    print(f"Raw: {profile.raw_value}")
    print(f"Path: {' → '.join(map(str, profile.reduction_path))}")
    print(f"Reduced: {profile.reduced_value}")
    print()
    print("Spiral Position:")
    print(f"  X: {profile.spiral_position.x}")
    print(f"  Y: {profile.spiral_position.y}")
    print(f"  Angle: {profile.spiral_position.angle}°")
    print()
    print("Waveform:")
    print(f"  Frequency: {profile.waveform.frequency_hz} Hz")
    print(f"  Samples: {len(profile.waveform.samples)}")
    print()
    print("Mandala:")
    print(f"  Shape: {profile.mandala.shape_name} ({profile.mandala.symbol})")
    print(f"  Color: {profile.mandala.color}")
    print(f"  Vertices: {len(profile.mandala.vertices)}")
    print()
    print("Archetype:")
    print(f"  Name: {profile.archetype['name']}")
    print(f"  Quality: {profile.archetype['quality']}")
    print(f"  Planet: {profile.archetype['planet']}")
    print()
    print("⚠️", dashboard.DISCLAIMER[:50] + "...")
