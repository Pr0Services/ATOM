"""
AT·OM — HARMONIZER ENGINE v1.0

Moteur central qui lit le master_config.json et applique automatiquement
les valeurs de résonance à tous les calculs du système.

Ce script est la "moelle épinière" qui connecte:
- Arithmos (calcul gématrique)
- Visual (animations CSS/JS)
- Audio (oscillateur 444Hz)
- Nexus (graphe causal)

Usage:
    from harmonizer import Harmonizer
    
    h = Harmonizer()
    result = h.harmonize("FEU")
    
    # Appliquer un delay
    await h.resonant_sleep(5)  # Sleep basé sur niveau 5 (500ms)
    
    # Obtenir la vitesse de rotation
    rpm = h.get_rotation_speed(9)  # Niveau 9 = très rapide

Auteur: AT-OM System
Version: 1.0.0
Ancre: 444 Hz
"""

from __future__ import annotations

import asyncio
import json
import re
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG_PATH = Path(__file__).parent / "master_config.json"
PYTHAGOREAN_MAP = {
    **{c: 1 for c in "AJS"},
    **{c: 2 for c in "BKT"},
    **{c: 3 for c in "CLU"},
    **{c: 4 for c in "DMV"},
    **{c: 5 for c in "ENW"},
    **{c: 6 for c in "FOX"},
    **{c: 7 for c in "GPY"},
    **{c: 8 for c in "HQZ"},
    **{c: 9 for c in "IR"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATACLASS OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class HarmonizedResult:
    """Résultat complet d'une harmonisation."""
    
    # Input
    word: str
    normalized: str
    
    # Arithmos
    raw_sum: int
    level: int
    is_master: bool
    
    # Résonance (depuis master_config)
    label: str
    hz: int
    color: str
    ratio: float
    delay_ms: int
    density: str
    element: str
    chakra: str
    description: str
    
    # Dérivés
    rotation_rpm: float
    pulse_interval_ms: float
    is_anchor: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return {
            "word": self.word,
            "normalized": self.normalized,
            "raw_sum": self.raw_sum,
            "level": self.level,
            "is_master": self.is_master,
            "label": self.label,
            "hz": self.hz,
            "color": self.color,
            "ratio": self.ratio,
            "delay_ms": self.delay_ms,
            "density": self.density,
            "element": self.element,
            "chakra": self.chakra,
            "description": self.description,
            "rotation_rpm": self.rotation_rpm,
            "pulse_interval_ms": self.pulse_interval_ms,
            "is_anchor": self.is_anchor,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convertit en JSON."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPALE: Harmonizer
# ═══════════════════════════════════════════════════════════════════════════════

class Harmonizer:
    """
    Moteur central d'harmonisation AT-OM.
    
    Lit le master_config.json et applique les valeurs de résonance
    à tous les calculs du système.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise le Harmonizer.
        
        Args:
            config_path: Chemin vers master_config.json (optionnel)
        """
        self.config_path = config_path or CONFIG_PATH
        self.config = self._load_config()
        self._build_lookup_tables()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge le master_config.json."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"master_config.json non trouvé: {self.config_path}")
    
    def _build_lookup_tables(self) -> None:
        """Construit les tables de lookup pour accès rapide."""
        # Table niveau → données
        self.level_lookup: Dict[int, Dict] = {}
        
        for item in self.config.get("resonance_matrix", []):
            self.level_lookup[item["level"]] = item
        
        for item in self.config.get("master_numbers", []):
            self.level_lookup[item["level"]] = item
        
        # Extraire les constantes
        self.heartbeat = self.config.get("system_heartbeat", 444)
        self.base_rpm = self.config.get("animation_config", {}).get("base_rpm", 60)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCUL ARITHMOS
    # ─────────────────────────────────────────────────────────────────────────
    
    def normalize(self, text: str) -> str:
        """Normalise le texte pour calcul gématrique."""
        text = unicodedata.normalize("NFKD", text)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        text = re.sub(r"[^A-Za-z]", "", text)
        return text.upper()
    
    def calculate_raw(self, text: str) -> int:
        """Calcule la somme gématrique brute."""
        normalized = self.normalize(text)
        return sum(PYTHAGOREAN_MAP.get(ch, 0) for ch in normalized)
    
    def reduce(self, value: int, preserve_masters: bool = True) -> int:
        """Réduit à un niveau (1-9 ou 11/22/33)."""
        master_numbers = {11, 22, 33}
        
        while True:
            if preserve_masters and value in master_numbers:
                return value
            if 1 <= value <= 9:
                return value
            if value == 0:
                return 0
            value = sum(int(d) for d in str(value))
    
    def get_level(self, text: str) -> int:
        """Obtient le niveau de résonance d'un mot."""
        raw = self.calculate_raw(text)
        return self.reduce(raw)
    
    # ─────────────────────────────────────────────────────────────────────────
    # LOOKUP RÉSONANCE
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_resonance(self, level: int) -> Dict[str, Any]:
        """
        Obtient les données de résonance pour un niveau.
        
        Args:
            level: Niveau arithmos (1-9 ou 11/22/33)
            
        Returns:
            Dict avec hz, color, ratio, delay_ms, etc.
        """
        if level in self.level_lookup:
            return self.level_lookup[level]
        
        # Fallback vers niveau 4 (ancre)
        return self.level_lookup.get(4, {
            "level": 4,
            "label": "Structure",
            "hz": 444,
            "color": "#50C878",
            "ratio": 1.0,
            "delay_ms": 600
        })
    
    def get_hz(self, level: int) -> int:
        """Obtient la fréquence Hz pour un niveau."""
        return self.get_resonance(level).get("hz", 444)
    
    def get_color(self, level: int) -> str:
        """Obtient la couleur hex pour un niveau."""
        return self.get_resonance(level).get("color", "#50C878")
    
    def get_delay(self, level: int) -> int:
        """Obtient le delay en ms pour un niveau."""
        return self.get_resonance(level).get("delay_ms", 600)
    
    def get_ratio(self, level: int) -> float:
        """Obtient le ratio par rapport à 444Hz."""
        return self.get_resonance(level).get("ratio", 1.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # HARMONISATION COMPLÈTE
    # ─────────────────────────────────────────────────────────────────────────
    
    def harmonize(self, text: str) -> HarmonizedResult:
        """
        Harmonise un mot/concept complet.
        
        C'est la fonction principale qui retourne toutes les données
        de résonance pour un mot.
        
        Args:
            text: Mot ou concept à harmoniser
            
        Returns:
            HarmonizedResult avec toutes les données
        """
        normalized = self.normalize(text)
        raw_sum = self.calculate_raw(text)
        level = self.reduce(raw_sum)
        
        resonance = self.get_resonance(level)
        is_master = level in {11, 22, 33}
        
        # Calculs dérivés
        ratio = resonance.get("ratio", 1.0)
        hz = resonance.get("hz", 444)
        rotation_rpm = ratio * self.base_rpm
        pulse_interval = 1000 / (hz / 100) if hz > 0 else 1000
        
        return HarmonizedResult(
            word=text,
            normalized=normalized,
            raw_sum=raw_sum,
            level=level,
            is_master=is_master,
            label=resonance.get("label", "Inconnu"),
            hz=hz,
            color=resonance.get("color", "#50C878"),
            ratio=ratio,
            delay_ms=resonance.get("delay_ms", 600),
            density=resonance.get("density", "balanced"),
            element=resonance.get("element", ""),
            chakra=resonance.get("chakra", ""),
            description=resonance.get("description", ""),
            rotation_rpm=rotation_rpm,
            pulse_interval_ms=pulse_interval,
            is_anchor=resonance.get("is_anchor", False),
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # FONCTIONS DE TIMING
    # ─────────────────────────────────────────────────────────────────────────
    
    def sleep(self, level: int, multiplier: float = 1.0) -> None:
        """
        Sleep synchrone basé sur le niveau de résonance.
        
        Args:
            level: Niveau arithmos (1-9)
            multiplier: Multiplicateur optionnel
        """
        delay = self.get_delay(level) * multiplier / 1000
        time.sleep(delay)
    
    async def resonant_sleep(self, level: int, multiplier: float = 1.0) -> None:
        """
        Sleep asynchrone basé sur le niveau de résonance.
        
        Args:
            level: Niveau arithmos (1-9)
            multiplier: Multiplicateur optionnel
        """
        delay = self.get_delay(level) * multiplier / 1000
        await asyncio.sleep(delay)
    
    def get_rotation_speed(self, level: int) -> float:
        """
        Obtient la vitesse de rotation du mandala en RPM.
        
        Plus le ratio est élevé, plus ça tourne vite.
        
        Args:
            level: Niveau arithmos
            
        Returns:
            Vitesse en RPM
        """
        ratio = self.get_ratio(level)
        return ratio * self.base_rpm
    
    def get_css_transition(self, level: int) -> str:
        """
        Génère une transition CSS basée sur le niveau.
        
        Args:
            level: Niveau arithmos
            
        Returns:
            String CSS (ex: "all 600ms ease-out")
        """
        delay = self.get_delay(level)
        ease = self.config.get("animation_config", {}).get("glyph_ease", "ease-out")
        return f"all {delay}ms {ease}"
    
    def get_css_variables(self, level: int) -> Dict[str, str]:
        """
        Génère les CSS custom properties pour un niveau.
        
        Args:
            level: Niveau arithmos
            
        Returns:
            Dict de CSS variables
        """
        resonance = self.get_resonance(level)
        
        return {
            "--atom-hz": f"{resonance.get('hz', 444)}",
            "--atom-color": resonance.get("color", "#50C878"),
            "--atom-delay": f"{resonance.get('delay_ms', 600)}ms",
            "--atom-ratio": f"{resonance.get('ratio', 1.0)}",
            "--atom-rpm": f"{self.get_rotation_speed(level)}",
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────────────────────────────────────
    
    def harmonize_batch(self, words: List[str]) -> List[HarmonizedResult]:
        """Harmonise plusieurs mots."""
        return [self.harmonize(word) for word in words]
    
    def compare(self, word1: str, word2: str) -> Dict[str, Any]:
        """Compare deux mots."""
        h1 = self.harmonize(word1)
        h2 = self.harmonize(word2)
        
        return {
            "word1": h1.to_dict(),
            "word2": h2.to_dict(),
            "same_level": h1.level == h2.level,
            "hz_difference": abs(h1.hz - h2.hz),
            "ratio_difference": abs(h1.ratio - h2.ratio),
            "harmonic_interval": max(h1.hz, h2.hz) / min(h1.hz, h2.hz) if min(h1.hz, h2.hz) > 0 else 0,
        }
    
    def get_all_levels(self) -> List[Dict[str, Any]]:
        """Retourne la matrice complète."""
        return self.config.get("resonance_matrix", [])
    
    def get_anchor(self) -> Dict[str, Any]:
        """Retourne les données de l'ancre (niveau 4)."""
        return self.get_resonance(4)


# ═══════════════════════════════════════════════════════════════════════════════
# INSTANCE SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_harmonizer_instance: Optional[Harmonizer] = None


def get_harmonizer() -> Harmonizer:
    """Obtient l'instance singleton du Harmonizer."""
    global _harmonizer_instance
    if _harmonizer_instance is None:
        _harmonizer_instance = Harmonizer()
    return _harmonizer_instance


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS RACCOURCIS
# ═══════════════════════════════════════════════════════════════════════════════

def harmonize(text: str) -> HarmonizedResult:
    """Raccourci pour harmoniser un mot."""
    return get_harmonizer().harmonize(text)


def get_delay(level_or_word: Union[int, str]) -> int:
    """Raccourci pour obtenir un delay."""
    h = get_harmonizer()
    if isinstance(level_or_word, str):
        level = h.get_level(level_or_word)
    else:
        level = level_or_word
    return h.get_delay(level)


def get_color(level_or_word: Union[int, str]) -> str:
    """Raccourci pour obtenir une couleur."""
    h = get_harmonizer()
    if isinstance(level_or_word, str):
        level = h.get_level(level_or_word)
    else:
        level = level_or_word
    return h.get_color(level)


def get_hz(level_or_word: Union[int, str]) -> int:
    """Raccourci pour obtenir une fréquence."""
    h = get_harmonizer()
    if isinstance(level_or_word, str):
        level = h.get_level(level_or_word)
    else:
        level = level_or_word
    return h.get_hz(level)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI / TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("AT·OM HARMONIZER ENGINE v1.0")
    print("=" * 80)
    print()
    
    h = Harmonizer()
    
    # Test des 5 Pierres de Fondation
    test_words = ["FEU", "ACIER", "INTELLIGENCE ARTIFICIELLE", "ADN", "SILENCE"]
    
    print("🔮 HARMONISATION DES 5 PIERRES DE FONDATION")
    print("-" * 80)
    
    for word in test_words:
        result = h.harmonize(word)
        print(f"\n📿 {word}")
        print(f"   Niveau: {result.level} ({result.label})")
        print(f"   Fréquence: {result.hz} Hz")
        print(f"   Couleur: {result.color}")
        print(f"   Ratio: {result.ratio}")
        print(f"   Delay: {result.delay_ms}ms")
        print(f"   Rotation: {result.rotation_rpm:.1f} RPM")
        print(f"   Élément: {result.element}")
    
    print()
    print("=" * 80)
    print("📊 MATRICE COMPLÈTE")
    print("-" * 80)
    
    for level_data in h.get_all_levels():
        print(f"  {level_data['level']} | {level_data['label']:12} | {level_data['hz']:4}Hz | {level_data['color']} | {level_data['delay_ms']}ms")
    
    print()
    print("=" * 80)
    print("🎯 TEST OUTPUT JSON (FEU)")
    print("-" * 80)
    print(h.harmonize("FEU").to_json())
