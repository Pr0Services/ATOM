"""AT-OM / CHE-NU — Resonator

Purpose
-------
Take the Arithmos output (raw + reduced) and assign:
- a *core frequency* (Hz)
- a *chromotherapy color* (hex)
- optional harmonic series metadata

Design goals
------------
- Deterministic, auditable mapping (no hidden magic).
- Defaults centered on the AT-OM heartbeat: 444 Hz.

Implementation notes
--------------------
We keep two layers:
1) Foundation tone: 444 Hz
2) Derived tone: depends on reduced number

You can choose any musical/psychoacoustic mapping later; here we provide a
simple, explainable mapping that matches your "structure" concept.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .arithmos import ArithmosResult

CORE_HEARTBEAT_HZ = 444.0

# Chromotherapy / number -> color (hex)
# Provided base palette (you can tune later). "RoseGold" is approximate.
NUMBER_COLOR: Dict[int, str] = {
    1: "#FF0000",  # Red
    2: "#FFA500",  # Orange
    3: "#FFFF00",  # Yellow
    4: "#00FF00",  # Green
    5: "#0000FF",  # Blue
    6: "#4B0082",  # Indigo
    7: "#8A2BE2",  # Violet
    8: "#B76E79",  # Rose Gold
    9: "#FFD700",  # Gold
    11: "#FFFFFF", # Master 11
    22: "#FFFFFF", # Master 22
    33: "#FFFFFF", # Master 33
}

# Reduced number -> multiplier for CORE_HEARTBEAT_HZ
# Keep close to 444 so the system feels consistent.
NUMBER_MULTIPLIER: Dict[int, float] = {
    1: 1.000,  # 444
    2: 1.125,  # 499.5
    3: 1.250,  # 555
    4: 1.000,  # 444 (foundation)
    5: 1.333,  # 592
    6: 1.500,  # 666
    7: 1.575,  # 699.3
    8: 1.666,  # 740.9
    9: 1.777,  # 788.0
    11: 2.000, # 888
    22: 3.000, # 1332
    33: 4.000, # 1776
}


@dataclass(frozen=True)
class Resonance:
    reduced: int
    color_hex: str
    frequency_hz: float
    heartbeat_hz: float
    explanation: str


def to_resonance(arithmos: ArithmosResult) -> Resonance:
    r = arithmos.reduced

    color = NUMBER_COLOR.get(r, "#FFFFFF")
    mult = NUMBER_MULTIPLIER.get(r, 1.0)

    freq = CORE_HEARTBEAT_HZ * mult

    explanation = (
        f"AT-OM Resonance: reduced={r}; color={color}; "
        f"frequency={freq:.1f} Hz derived from heartbeat {CORE_HEARTBEAT_HZ:.1f} Hz * {mult:.3f}."
    )

    return Resonance(
        reduced=r,
        color_hex=color,
        frequency_hz=freq,
        heartbeat_hz=CORE_HEARTBEAT_HZ,
        explanation=explanation,
    )


if __name__ == "__main__":
    from .arithmos import analyze

    for concept in ["AT-OM", "CHE-NU", "FIRE", "AI"]:
        a = analyze(concept)
        res = to_resonance(a)
        print(concept, "=>", res)
