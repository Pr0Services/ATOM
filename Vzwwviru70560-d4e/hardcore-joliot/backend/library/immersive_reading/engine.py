"""
============================================================================
CHE·NU™ V69 — LIBRARY IMMERSIVE READING ENGINE
============================================================================
Spec: GPT1/CHE-NU_LIB_IMMERSIVE_READING_ENGINE.md

Objective: Transform text into XR ambiance (visual + audio + haptic)
in a governed way.

Inputs (per spec):
- ChapterChunk (text)
- reader_profile (preferences, sensitivity)
- scene_budget (performance limits)
- opa_policy_ref

Outputs (per spec):
- XR Scene Manifest (XRS)
- Live Controls

Generation: Guided, not hallucinated (assets from controlled library)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import re

from ..models import (
    ChapterChunk,
    ReaderProfile,
    XRSceneManifest,
    ReadingMode,
    IntensityLevel,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# EMOTION EXTRACTION
# ============================================================================

class EmotionExtractor:
    """
    Extract emotions and themes from text.
    
    Per spec: Extraction d'émotions / thèmes / lieux
    """
    
    # Emotion keywords
    EMOTIONS = {
        "joy": ["heureux", "joie", "rire", "sourire", "bonheur", "happy", "joy"],
        "sadness": ["triste", "pleure", "larme", "chagrin", "sad", "tears"],
        "fear": ["peur", "effroi", "terreur", "angoisse", "fear", "terror"],
        "anger": ["colère", "rage", "fureur", "angry", "rage", "fury"],
        "surprise": ["surprise", "étonnement", "stupeur", "amazed", "shocked"],
        "calm": ["calme", "serein", "paisible", "tranquille", "calm", "peaceful"],
        "tension": ["tension", "suspense", "attente", "menace", "tense"],
        "romance": ["amour", "passion", "désir", "tendresse", "love", "romance"],
    }
    
    # Setting keywords
    SETTINGS = {
        "nature": ["forêt", "montagne", "mer", "plage", "rivière", "forest", "mountain"],
        "urban": ["ville", "rue", "bâtiment", "gratte-ciel", "city", "street"],
        "interior": ["maison", "chambre", "salon", "bureau", "room", "house"],
        "fantasy": ["château", "royaume", "dragon", "magie", "castle", "magic"],
        "scifi": ["vaisseau", "espace", "planète", "robot", "ship", "space"],
    }
    
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract emotions and settings from text"""
        text_lower = text.lower()
        
        # Extract emotions
        emotions = {}
        for emotion, keywords in self.EMOTIONS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                emotions[emotion] = count
        
        # Dominant emotion
        dominant_emotion = max(emotions.keys(), key=lambda e: emotions[e]) if emotions else "neutral"
        
        # Extract settings
        settings = {}
        for setting, keywords in self.SETTINGS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                settings[setting] = count
        
        # Dominant setting
        dominant_setting = max(settings.keys(), key=lambda s: settings[s]) if settings else "interior"
        
        return {
            "emotions": emotions,
            "dominant_emotion": dominant_emotion,
            "settings": settings,
            "dominant_setting": dominant_setting,
        }


# ============================================================================
# ASSET LIBRARY
# ============================================================================

class AssetLibrary:
    """
    Controlled asset library for XR scenes.
    
    Per spec: Les "assets" doivent venir d'une bibliothèque contrôlée
    """
    
    # Environment themes
    ENVIRONMENTS = {
        "library": {
            "skybox": "library_warm",
            "floor": "wood_parquet",
            "ambient": "soft_light",
        },
        "nature": {
            "skybox": "forest_day",
            "floor": "grass",
            "ambient": "natural_light",
        },
        "urban": {
            "skybox": "city_dusk",
            "floor": "concrete",
            "ambient": "street_light",
        },
        "fantasy": {
            "skybox": "castle_night",
            "floor": "stone",
            "ambient": "torch_light",
        },
        "scifi": {
            "skybox": "space_stars",
            "floor": "metal_grid",
            "ambient": "neon_blue",
        },
    }
    
    # Lighting profiles
    LIGHTING = {
        "calm": {"intensity": 0.6, "color_temp": 4500, "shadows": "soft"},
        "neutral": {"intensity": 0.8, "color_temp": 5500, "shadows": "medium"},
        "dramatic": {"intensity": 1.0, "color_temp": 3500, "shadows": "hard"},
        "intense": {"intensity": 1.2, "color_temp": 6500, "shadows": "sharp"},
    }
    
    # Soundscapes
    SOUNDSCAPES = {
        "calm": {"music": "ambient_soft", "sfx": [], "volume": 0.3},
        "neutral": {"music": "background_neutral", "sfx": [], "volume": 0.4},
        "dramatic": {"music": "orchestral_tension", "sfx": ["heartbeat"], "volume": 0.6},
        "intense": {"music": "action_score", "sfx": ["wind", "thunder"], "volume": 0.8},
    }
    
    # Haptic profiles
    HAPTICS = {
        "calm": {"pulse_rate": 0, "intensity": 0},
        "neutral": {"pulse_rate": 0, "intensity": 0.1},
        "dramatic": {"pulse_rate": 60, "intensity": 0.3},
        "intense": {"pulse_rate": 120, "intensity": 0.6},
    }
    
    def get_environment(self, setting: str) -> Dict[str, str]:
        """Get environment assets for a setting"""
        return self.ENVIRONMENTS.get(setting, self.ENVIRONMENTS["library"])
    
    def get_lighting(self, intensity: IntensityLevel) -> Dict[str, Any]:
        """Get lighting profile for intensity"""
        return self.LIGHTING.get(intensity.value, self.LIGHTING["neutral"])
    
    def get_soundscape(self, intensity: IntensityLevel) -> Dict[str, Any]:
        """Get soundscape for intensity"""
        return self.SOUNDSCAPES.get(intensity.value, self.SOUNDSCAPES["neutral"])
    
    def get_haptic(self, intensity: IntensityLevel) -> Dict[str, Any]:
        """Get haptic profile for intensity"""
        return self.HAPTICS.get(intensity.value, self.HAPTICS["neutral"])


# ============================================================================
# SCENE GENERATOR
# ============================================================================

class SceneGenerator:
    """
    Generate XR scenes from text.
    
    Per spec: Synchronisation sémantique
    """
    
    def __init__(self):
        self.emotion_extractor = EmotionExtractor()
        self.asset_library = AssetLibrary()
    
    def generate(
        self,
        chunk: ChapterChunk,
        reader_profile: ReaderProfile,
        scene_budget: int = 5,
    ) -> XRSceneManifest:
        """Generate XR scene manifest for a chunk"""
        # Extract semantic info
        semantics = self.emotion_extractor.extract(chunk.text)
        
        # Determine intensity from emotions and preferences
        intensity = self._determine_intensity(
            semantics["dominant_emotion"],
            reader_profile.intensity_preference,
        )
        
        # Get setting
        setting = semantics["dominant_setting"]
        
        # Check reader sensitivities
        if any(theme in reader_profile.avoid_themes for theme in semantics["emotions"].keys()):
            intensity = IntensityLevel.CALM
        
        # Get assets
        environment = self.asset_library.get_environment(setting)
        lighting = self.asset_library.get_lighting(intensity)
        soundscape = self.asset_library.get_soundscape(intensity)
        haptic = self.asset_library.get_haptic(intensity)
        
        # Apply scene budget
        if scene_budget < 3:
            soundscape = {"music": "none", "sfx": [], "volume": 0}
            haptic = {"pulse_rate": 0, "intensity": 0}
        
        # Create markers for key moments
        markers = self._create_semantic_markers(chunk.text, semantics)
        
        manifest = XRSceneManifest(
            manifest_id=generate_id(),
            chunk_id=chunk.chunk_id,
            environment_theme=setting,
            lighting_profile=lighting,
            soundscape_profile=soundscape,
            haptic_profile=haptic,
            semantic_markers=markers,
            intensity=intensity,
            mode=reader_profile.preferred_mode,
        )
        
        # Sign manifest
        manifest.signature = sign_artifact({
            "manifest_id": manifest.manifest_id,
            "chunk_id": chunk.chunk_id,
            "setting": setting,
        }, "scene_generator")
        
        return manifest
    
    def _determine_intensity(
        self,
        emotion: str,
        preference: IntensityLevel,
    ) -> IntensityLevel:
        """Determine scene intensity from emotion and preference"""
        # Emotion to intensity mapping
        emotion_intensity = {
            "joy": IntensityLevel.NEUTRAL,
            "sadness": IntensityLevel.CALM,
            "fear": IntensityLevel.DRAMATIC,
            "anger": IntensityLevel.INTENSE,
            "surprise": IntensityLevel.DRAMATIC,
            "calm": IntensityLevel.CALM,
            "tension": IntensityLevel.DRAMATIC,
            "romance": IntensityLevel.NEUTRAL,
            "neutral": IntensityLevel.NEUTRAL,
        }
        
        content_intensity = emotion_intensity.get(emotion, IntensityLevel.NEUTRAL)
        
        # Balance with preference (weighted average)
        intensity_order = [IntensityLevel.CALM, IntensityLevel.NEUTRAL, 
                         IntensityLevel.DRAMATIC, IntensityLevel.INTENSE]
        
        content_idx = intensity_order.index(content_intensity)
        pref_idx = intensity_order.index(preference)
        
        # Weighted: 60% content, 40% preference
        final_idx = int(content_idx * 0.6 + pref_idx * 0.4)
        final_idx = max(0, min(final_idx, len(intensity_order) - 1))
        
        return intensity_order[final_idx]
    
    def _create_semantic_markers(
        self,
        text: str,
        semantics: Dict,
    ) -> List[Dict[str, Any]]:
        """Create semantic markers for key moments"""
        markers = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
            
            # Extract sentence emotion
            sent_semantics = self.emotion_extractor.extract(sentence)
            
            if sent_semantics["dominant_emotion"] != "neutral":
                markers.append({
                    "position": i,
                    "type": "emotion_shift",
                    "emotion": sent_semantics["dominant_emotion"],
                    "text_preview": sentence[:50] + "...",
                })
        
        return markers


# ============================================================================
# IMMERSIVE READING ENGINE
# ============================================================================

class ImmersiveReadingEngine:
    """
    Main engine for immersive reading.
    
    Per spec: Transformer un texte en ambiance XR
    """
    
    def __init__(self):
        self.scene_generator = SceneGenerator()
        
        # Manifests cache
        self._manifests: Dict[str, XRSceneManifest] = {}
        
        # Reader profiles
        self._profiles: Dict[str, ReaderProfile] = {}
    
    def set_reader_profile(self, profile: ReaderProfile) -> None:
        """Set reader profile"""
        self._profiles[profile.reader_id] = profile
    
    def get_reader_profile(self, reader_id: str) -> Optional[ReaderProfile]:
        """Get reader profile"""
        return self._profiles.get(reader_id)
    
    def generate_scene(
        self,
        chunk: ChapterChunk,
        reader_id: str,
        scene_budget: int = 5,
    ) -> XRSceneManifest:
        """
        Generate XR scene for reading.
        
        Per spec inputs: ChapterChunk, reader_profile, scene_budget
        """
        profile = self._profiles.get(reader_id)
        if not profile:
            profile = ReaderProfile(reader_id=reader_id)
        
        manifest = self.scene_generator.generate(chunk, profile, scene_budget)
        
        self._manifests[manifest.manifest_id] = manifest
        
        logger.info(
            f"Generated scene {manifest.manifest_id} for chunk {chunk.chunk_id}: "
            f"theme={manifest.environment_theme}, intensity={manifest.intensity.value}"
        )
        
        return manifest
    
    def adjust_intensity(
        self,
        manifest_id: str,
        new_intensity: IntensityLevel,
    ) -> Optional[XRSceneManifest]:
        """
        Adjust scene intensity.
        
        Per spec live controls: intensité (calme ↔ dramatique)
        """
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            return None
        
        # Update intensity
        manifest.intensity = new_intensity
        
        # Update profiles
        manifest.lighting_profile = self.scene_generator.asset_library.get_lighting(new_intensity)
        manifest.soundscape_profile = self.scene_generator.asset_library.get_soundscape(new_intensity)
        manifest.haptic_profile = self.scene_generator.asset_library.get_haptic(new_intensity)
        
        return manifest
    
    def change_mode(
        self,
        manifest_id: str,
        new_mode: ReadingMode,
    ) -> Optional[XRSceneManifest]:
        """
        Change reading mode.
        
        Per spec: mode (Read-only ↔ Guided)
        """
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            return None
        
        manifest.mode = new_mode
        return manifest
    
    def export_manifest(self, manifest_id: str) -> Dict[str, Any]:
        """Export manifest as signed artifact"""
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            return {}
        
        return {
            "type": "xr_scene_manifest",
            "manifest_id": manifest.manifest_id,
            "chunk_id": manifest.chunk_id,
            "environment_theme": manifest.environment_theme,
            "lighting_profile": manifest.lighting_profile,
            "soundscape_profile": manifest.soundscape_profile,
            "haptic_profile": manifest.haptic_profile,
            "semantic_markers": manifest.semantic_markers,
            "intensity": manifest.intensity.value,
            "mode": manifest.mode.value,
            "signature": manifest.signature,
        }
    
    def get_performance_metrics(self, manifest_id: str) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Per spec observability: mesures perf (latency, fps)
        """
        manifest = self._manifests.get(manifest_id)
        if not manifest:
            return {}
        
        # Mock metrics
        return {
            "manifest_id": manifest_id,
            "latency_ms": 45,
            "fps": 60,
            "asset_load_time_ms": 120,
            "memory_mb": 256,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_engine() -> ImmersiveReadingEngine:
    """Create immersive reading engine"""
    return ImmersiveReadingEngine()


def create_reader_profile(
    reader_id: str,
    mode: ReadingMode = ReadingMode.READ_ONLY,
    intensity: IntensityLevel = IntensityLevel.NEUTRAL,
) -> ReaderProfile:
    """Create reader profile"""
    return ReaderProfile(
        reader_id=reader_id,
        preferred_mode=mode,
        intensity_preference=intensity,
    )
