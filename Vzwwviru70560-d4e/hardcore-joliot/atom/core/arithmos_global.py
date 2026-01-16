#!/usr/bin/env python3
"""
AT·OM — Script Arithmos Global v1.0
===================================

Configuration Maître de l'Architecte Jonathan Rodrigue (999 Hz)

Ce script est la SOURCE DE VÉRITÉ pour tous les calculs gématriques
du système AT-OM. Il convertit n'importe quel mot en sa résonance
vibratoire correspondante.

Usage:
    python arithmos_global.py "VOTRE MOT"
    
Exemple:
    python arithmos_global.py "EAU"
    # Résultat: Mot: EAU | Niveau: 9 | Résonance: 999Hz | Couleur: #FFFDD0
"""

import json
import os
from typing import Dict, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION MAÎTRE
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_HEARTBEAT = 444
TUNING_STANDARD = "A=444Hz"

# Matrice de Résonance Officielle
RESONANCE_MATRIX = [
    { "level": 1, "label": "Impulsion/ADN", "hz": 111, "color": "#FF0000", "ratio": 0.25, "delay_ms": 900 },
    { "level": 2, "label": "Dualité/Partage", "hz": 222, "color": "#FF7F00", "ratio": 0.50, "delay_ms": 800 },
    { "level": 3, "label": "Mental/Géométrie", "hz": 333, "color": "#FFFF00", "ratio": 0.75, "delay_ms": 700 },
    { "level": 4, "label": "Structure/Silence", "hz": 444, "color": "#50C878", "ratio": 1.00, "delay_ms": 600 },
    { "level": 5, "label": "Mouvement/Feu", "hz": 555, "color": "#87CEEB", "ratio": 1.25, "delay_ms": 500 },
    { "level": 6, "label": "Harmonie/Protection", "hz": 666, "color": "#4B0082", "ratio": 1.50, "delay_ms": 400 },
    { "level": 7, "label": "Introspection", "hz": 777, "color": "#EE82EE", "ratio": 1.75, "delay_ms": 300 },
    { "level": 8, "label": "Infini/Abondance", "hz": 888, "color": "#FFC0CB", "ratio": 2.00, "delay_ms": 200 },
    { "level": 9, "label": "Unité/Acier", "hz": 999, "color": "#FFFDD0", "ratio": 2.25, "delay_ms": 100 },
]

# Mapping Pythagoricien Simple
PYTHAGOREAN_MAPPING = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

# Pierres de Fondation (détection spéciale)
FOUNDATION_STONES = {
    "FEU": 5,
    "ACIER": 9,
    "IA": 1,
    "ADN": 1,
    "SILENCE": 4,
}

# Nœuds de Transition
TRANSITION_NODES = {
    "DUALITE": 2,
    "DUALITÉ": 2,
    "MENTAL": 3,
    "HARMONIE": 6,
    "SPIRITUALITE": 7,
    "SPIRITUALITÉ": 7,
    "INFINI": 8,
}

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_arithmos(word: str) -> int:
    """
    Calcule l'Arithmos (racine numérique) d'un mot.
    
    Mapping Pythagoricien:
        A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9
        J=1, K=2, L=3, M=4, N=5, O=6, P=7, Q=8, R=9
        S=1, T=2, U=3, V=4, W=5, X=6, Y=7, Z=8
    
    Args:
        word: Le mot à analyser
        
    Returns:
        int: La racine numérique (1-9)
        
    Example:
        >>> calculate_arithmos("EAU")
        9  # E(5) + A(1) + U(3) = 9
    """
    # Calcul de la somme brute
    total = sum(PYTHAGOREAN_MAPPING.get(char.upper(), 0) for char in word)
    
    # Réduction à la racine (1-9)
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    
    return total


def get_resonance_data(level: int) -> Dict:
    """
    Récupère les données de résonance pour un niveau donné.
    
    Args:
        level: Le niveau (1-9)
        
    Returns:
        dict: Les données de résonance (hz, color, delay_ms, etc.)
    """
    for item in RESONANCE_MATRIX:
        if item["level"] == level:
            return item
    return RESONANCE_MATRIX[3]  # Fallback: niveau 4 (ancre)


def get_resonance(word: str) -> str:
    """
    Retourne une description formatée de la résonance d'un mot.
    
    Args:
        word: Le mot à analyser
        
    Returns:
        str: Description formatée
        
    Example:
        >>> get_resonance("EAU")
        "Mot: EAU | Niveau: 9 | Résonance: 999Hz | Couleur: #FFFDD0"
    """
    word_upper = word.upper()
    
    # Vérifier si c'est une Pierre de Fondation
    if word_upper in FOUNDATION_STONES:
        level = FOUNDATION_STONES[word_upper]
        stone_type = "🧱 PIERRE DE FONDATION"
    # Vérifier si c'est un Nœud de Transition
    elif word_upper in TRANSITION_NODES:
        level = TRANSITION_NODES[word_upper]
        stone_type = "🌀 NŒUD DE TRANSITION"
    else:
        level = calculate_arithmos(word)
        stone_type = "📝 MOT STANDARD"
    
    data = get_resonance_data(level)
    
    return (
        f"{stone_type}\n"
        f"Mot: {word_upper} | "
        f"Niveau: {level} | "
        f"Résonance: {data['hz']}Hz | "
        f"Couleur: {data['color']} | "
        f"Delay: {data['delay_ms']}ms"
    )


def get_full_analysis(word: str) -> Dict:
    """
    Analyse complète d'un mot avec tous ses paramètres vibratoires.
    
    Args:
        word: Le mot à analyser
        
    Returns:
        dict: Analyse complète
    """
    word_upper = word.upper()
    
    # Déterminer le type et le niveau
    if word_upper in FOUNDATION_STONES:
        level = FOUNDATION_STONES[word_upper]
        word_type = "foundation_stone"
    elif word_upper in TRANSITION_NODES:
        level = TRANSITION_NODES[word_upper]
        word_type = "transition_node"
    else:
        level = calculate_arithmos(word)
        word_type = "standard"
    
    data = get_resonance_data(level)
    
    # Calcul détaillé lettre par lettre
    letter_values = []
    for char in word_upper:
        if char in PYTHAGOREAN_MAPPING:
            letter_values.append({
                "letter": char,
                "value": PYTHAGOREAN_MAPPING[char]
            })
    
    raw_sum = sum(lv["value"] for lv in letter_values)
    
    return {
        "word": word_upper,
        "type": word_type,
        "letter_breakdown": letter_values,
        "raw_sum": raw_sum,
        "arithmos": level,
        "resonance": {
            "hz": data["hz"],
            "color": data["color"],
            "label": data["label"],
            "ratio": data["ratio"],
            "delay_ms": data["delay_ms"]
        },
        "formulas": {
            "hz_formula": f"{level} × 111 = {level * 111}",
            "ratio_formula": f"{level} × 0.25 = {level * 0.25}",
            "delay_formula": f"1000 - ({level} × 100) = {1000 - (level * 100)}"
        }
    }


def batch_analyze(words: list) -> list:
    """
    Analyse un lot de mots.
    
    Args:
        words: Liste de mots à analyser
        
    Returns:
        list: Liste des analyses
    """
    return [get_full_analysis(word) for word in words]


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def hz_from_level(level: int) -> int:
    """Calcule la fréquence Hz à partir du niveau."""
    return level * 111


def delay_from_level(level: int) -> int:
    """Calcule le delay en ms à partir du niveau."""
    return 1000 - (level * 100)


def ratio_from_level(level: int) -> float:
    """Calcule le ratio à partir du niveau."""
    return level * 0.25


def color_from_level(level: int) -> str:
    """Récupère la couleur hex pour un niveau."""
    data = get_resonance_data(level)
    return data["color"]


def is_foundation_stone(word: str) -> bool:
    """Vérifie si un mot est une Pierre de Fondation."""
    return word.upper() in FOUNDATION_STONES


def is_transition_node(word: str) -> bool:
    """Vérifie si un mot est un Nœud de Transition."""
    return word.upper() in TRANSITION_NODES


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS JSON
# ═══════════════════════════════════════════════════════════════════════════════

def export_config_json() -> str:
    """Exporte la configuration maître en JSON."""
    config = {
        "system_heartbeat": SYSTEM_HEARTBEAT,
        "tuning_standard": TUNING_STANDARD,
        "resonance_matrix": RESONANCE_MATRIX,
        "foundation_stones": FOUNDATION_STONES,
        "transition_nodes": TRANSITION_NODES,
        "pythagorean_mapping": PYTHAGOREAN_MAPPING
    }
    return json.dumps(config, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("AT·OM — Script Arithmos Global v1.0")
    print("Architecte: Jonathan Rodrigue (999 Hz)")
    print("=" * 60)
    print()
    
    # Tests des 5 Pierres de Fondation
    print("🧱 PIERRES DE FONDATION:")
    print("-" * 40)
    for stone in ["FEU", "ACIER", "IA", "ADN", "SILENCE"]:
        print(get_resonance(stone))
        print()
    
    # Tests des 5 Nœuds de Transition
    print("🌀 NŒUDS DE TRANSITION:")
    print("-" * 40)
    for node in ["DUALITE", "MENTAL", "HARMONIE", "SPIRITUALITE", "INFINI"]:
        print(get_resonance(node))
        print()
    
    # Tests de mots standards
    print("📝 MOTS STANDARDS:")
    print("-" * 40)
    test_words = ["EAU", "AMOUR", "LUMIERE", "PAIX", "VIE", "JONATHAN"]
    for word in test_words:
        print(get_resonance(word))
        print()
    
    # Si un argument est passé en ligne de commande
    if len(sys.argv) > 1:
        print("=" * 60)
        print("VOTRE MOT:")
        print("-" * 40)
        user_word = " ".join(sys.argv[1:])
        print(get_resonance(user_word))
        print()
        print("ANALYSE COMPLÈTE:")
        analysis = get_full_analysis(user_word)
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
