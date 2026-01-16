"""
AT·OM — ARITHMOS ENGINE v2.0 (Harmonisé 444Hz)

Convertisseur Gematria → Fréquence → Résonance Complète

Ce module est le CŒUR du système AT-OM. Il transforme n'importe quel
mot/concept en un objet de résonance complet, ancré sur 444Hz.

Flux:
    INPUT: "FEU"
    → Normalisation
    → Gematria Pythagoricienne (F=6, E=5, U=3 = 14)
    → Réduction théosophique (1+4 = 5)
    → Lookup dans la Matrice Sacrée
    → OUTPUT: Objet JSON structuré complet

Auteur: AT-OM System
Version: 2.0.0 (Harmonisé)
Ancre: 444 Hz
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

ANCHOR_FREQUENCY = 444
MASTER_NUMBERS = {11, 22, 33}

# Mapping Pythagoricien
PYTHAGOREAN_MAP: Dict[str, int] = {
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

# Chemin vers la matrice sacrée
CONSTANTS_PATH = Path(__file__).parent / "constants.json"


# ═══════════════════════════════════════════════════════════════════════════════
# CHARGEMENT DE LA MATRICE SACRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def load_sacred_matrix() -> Dict[str, Any]:
    """Charge la matrice des fréquences sacrées depuis constants.json."""
    if CONSTANTS_PATH.exists():
        with open(CONSTANTS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return _get_default_matrix()


def _get_default_matrix() -> Dict[str, Any]:
    """Matrice par défaut si constants.json n'est pas disponible."""
    return {
        "anchor_frequency": 444,
        "matrix": {
            "1": {"name": "Impulsion", "frequency_hz": 111, "color_hex": "#FF0000", "color_name": "Rouge", "animation_delay_ms": 900},
            "2": {"name": "Dualité", "frequency_hz": 222, "color_hex": "#FF7F00", "color_name": "Orange", "animation_delay_ms": 800},
            "3": {"name": "Mental", "frequency_hz": 333, "color_hex": "#FFFF00", "color_name": "Jaune", "animation_delay_ms": 700},
            "4": {"name": "Structure", "frequency_hz": 444, "color_hex": "#50C878", "color_name": "Vert Émeraude", "animation_delay_ms": 600, "is_home_frequency": True},
            "5": {"name": "Mouvement", "frequency_hz": 555, "color_hex": "#87CEEB", "color_name": "Bleu Ciel", "animation_delay_ms": 500},
            "6": {"name": "Harmonie", "frequency_hz": 666, "color_hex": "#4B0082", "color_name": "Indigo", "animation_delay_ms": 400},
            "7": {"name": "Silence", "frequency_hz": 777, "color_hex": "#EE82EE", "color_name": "Violet", "animation_delay_ms": 300},
            "8": {"name": "Infini", "frequency_hz": 888, "color_hex": "#FFC0CB", "color_name": "Rose", "animation_delay_ms": 200},
            "9": {"name": "Unité", "frequency_hz": 999, "color_hex": "#FFFDD0", "color_name": "Blanc-Or", "animation_delay_ms": 100},
        },
        "master_numbers": {
            "11": {"name": "Maître Illuminateur", "frequency_hz": 1111, "color_hex": "#FFFFFF"},
            "22": {"name": "Maître Bâtisseur", "frequency_hz": 2222, "color_hex": "#FFD700"},
            "33": {"name": "Maître Enseignant", "frequency_hz": 3333, "color_hex": "#E6E6FA"},
        }
    }


# Charger la matrice au démarrage
SACRED_MATRIX = load_sacred_matrix()


# ═══════════════════════════════════════════════════════════════════════════════
# DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class ResonanceResult:
    """Résultat complet d'une analyse de résonance."""
    
    # Input
    word: str
    normalized: str
    
    # Gematria
    letter_values: Tuple[int, ...]
    arithmos_raw: int
    arithmos_value: int
    is_master_number: bool
    
    # Fréquence
    frequency: int
    resonance_name: str
    
    # Couleur
    color_hex: str
    color_name: str
    color_rgb: Tuple[int, int, int]
    
    # Ratio et position
    resonance_ratio: float
    distance_from_444: int
    harmonic_position: str
    
    # Animation
    animation_delay_ms: int
    animation_speed: str
    
    # Audio
    audio_tone: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire JSON-serializable."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convertit en JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE NORMALISATION
# ═══════════════════════════════════════════════════════════════════════════════

def normalize_text(text: str) -> str:
    """Normalise le texte pour l'analyse gématrique."""
    if not isinstance(text, str):
        raise TypeError("Le texte doit être une chaîne de caractères")
    
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^A-Za-z]", "", text)
    
    return text.upper()


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE CALCUL GÉMATRIQUE
# ═══════════════════════════════════════════════════════════════════════════════

def get_letter_values(text: str) -> Tuple[int, ...]:
    """Retourne les valeurs Pythagoriciennes de chaque lettre."""
    normalized = normalize_text(text)
    return tuple(PYTHAGOREAN_MAP.get(ch, 0) for ch in normalized)


def calculate_raw_gematria(text: str) -> int:
    """Calcule la somme gématrique brute."""
    return sum(get_letter_values(text))


def reduce_theosophic(value: int, preserve_masters: bool = True) -> int:
    """Réduit un nombre à un chiffre (1-9) ou nombre maître (11, 22, 33)."""
    if value < 0:
        raise ValueError("La valeur doit être positive")
    
    if value == 0:
        return 0
    
    while True:
        if preserve_masters and value in MASTER_NUMBERS:
            return value
        if 1 <= value <= 9:
            return value
        value = sum(int(d) for d in str(value))


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE LOOKUP MATRICE
# ═══════════════════════════════════════════════════════════════════════════════

def get_resonance_data(arithmos_value: int) -> Dict[str, Any]:
    """Récupère les données de résonance depuis la matrice sacrée."""
    
    if arithmos_value in MASTER_NUMBERS:
        master_data = SACRED_MATRIX.get("master_numbers", {}).get(str(arithmos_value), {})
        if master_data:
            return {
                **master_data,
                "is_master": True,
                "animation_delay_ms": 50,
                "animation_speed": "transcendent"
            }
    
    matrix = SACRED_MATRIX.get("matrix", {})
    return matrix.get(str(arithmos_value), matrix.get("1", {}))


def calculate_harmonic_position(frequency: int) -> str:
    """Détermine la position par rapport à l'ancre 444Hz."""
    if frequency < ANCHOR_FREQUENCY:
        return "below_anchor"
    elif frequency == ANCHOR_FREQUENCY:
        return "at_anchor"
    else:
        return "above_anchor"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convertit une couleur hex en RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTION PRINCIPALE D'ANALYSE
# ═══════════════════════════════════════════════════════════════════════════════

def analyze(text: str, preserve_masters: bool = True) -> ResonanceResult:
    """
    Analyse complète d'un mot/concept.
    
    Retourne un objet ResonanceResult avec toutes les données de résonance.
    
    Example:
        >>> result = analyze("FEU")
        >>> print(result.to_json())
        {
          "word": "FEU",
          "arithmos_value": 5,
          "frequency": 555,
          "color_hex": "#87CEEB",
          "resonance_ratio": 1.25,
          ...
        }
    """
    normalized = normalize_text(text)
    letter_values = get_letter_values(text)
    arithmos_raw = sum(letter_values)
    arithmos_value = reduce_theosophic(arithmos_raw, preserve_masters)
    is_master = arithmos_value in MASTER_NUMBERS
    
    resonance_data = get_resonance_data(arithmos_value)
    
    frequency = resonance_data.get("frequency_hz", 444)
    color_hex = resonance_data.get("color_hex", "#50C878")
    color_name = resonance_data.get("color_name", "Inconnu")
    resonance_name = resonance_data.get("name", "Inconnu")
    animation_delay = resonance_data.get("animation_delay_ms", 600)
    animation_speed = resonance_data.get("animation_speed", "reference")
    
    resonance_ratio = round(frequency / ANCHOR_FREQUENCY, 4)
    distance = frequency - ANCHOR_FREQUENCY
    harmonic_position = calculate_harmonic_position(frequency)
    
    try:
        color_rgb = hex_to_rgb(color_hex)
    except:
        color_rgb = (80, 200, 120)
    
    audio_tone = {
        "hz": frequency,
        "duration_ms": max(200, 1000 - (frequency // 2)),
        "waveform": "sine",
        "volume": 0.7
    }
    
    return ResonanceResult(
        word=text,
        normalized=normalized,
        letter_values=letter_values,
        arithmos_raw=arithmos_raw,
        arithmos_value=arithmos_value,
        is_master_number=is_master,
        frequency=frequency,
        resonance_name=resonance_name,
        color_hex=color_hex,
        color_name=color_name,
        color_rgb=color_rgb,
        resonance_ratio=resonance_ratio,
        distance_from_444=distance,
        harmonic_position=harmonic_position,
        animation_delay_ms=animation_delay,
        animation_speed=animation_speed,
        audio_tone=audio_tone
    )


def analyze_to_dict(text: str, preserve_masters: bool = True) -> Dict[str, Any]:
    """Raccourci pour obtenir directement un dictionnaire."""
    return analyze(text, preserve_masters).to_dict()


def analyze_to_json(text: str, preserve_masters: bool = True, indent: int = 2) -> str:
    """Raccourci pour obtenir directement du JSON."""
    return analyze(text, preserve_masters).to_json(indent)


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_batch(words: List[str]) -> List[ResonanceResult]:
    """Analyse plusieurs mots en batch."""
    return [analyze(word) for word in words]


def compare_resonance(word1: str, word2: str) -> Dict[str, Any]:
    """Compare la résonance de deux mots."""
    r1 = analyze(word1)
    r2 = analyze(word2)
    
    return {
        "word1": {"word": word1, "value": r1.arithmos_value, "frequency": r1.frequency},
        "word2": {"word": word2, "value": r2.arithmos_value, "frequency": r2.frequency},
        "same_resonance": r1.arithmos_value == r2.arithmos_value,
        "frequency_difference": abs(r1.frequency - r2.frequency),
        "harmonic_interval": round(max(r1.frequency, r2.frequency) / min(r1.frequency, r2.frequency), 4)
    }


def get_words_by_resonance(words: List[str], target_value: int) -> List[str]:
    """Filtre les mots par valeur de résonance."""
    return [w for w in words if analyze(w).arithmos_value == target_value]


# ═══════════════════════════════════════════════════════════════════════════════
# CLI / TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    test_words = ["FEU", "ACIER", "INTELLIGENCE ARTIFICIELLE", "ADN", "SILENCE"]
    
    print("=" * 80)
    print("AT·OM ARITHMOS ENGINE v2.0 — Test des 5 Pierres de Fondation")
    print("=" * 80)
    print()
    
    for word in test_words:
        result = analyze(word)
        print(f"📿 {word}")
        print(f"   Arithmos: {result.arithmos_value} | Fréquence: {result.frequency} Hz")
        print(f"   Couleur: {result.color_name} ({result.color_hex})")
        print(f"   Ratio: {result.resonance_ratio} | Distance: {result.distance_from_444:+d} Hz")
        print(f"   Position: {result.harmonic_position}")
        print()
    
    print("=" * 80)
    print("Output JSON complet pour 'FEU':")
    print("=" * 80)
    print(analyze_to_json("FEU"))
