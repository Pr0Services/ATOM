"""
AT·OM — Gematria / Numerology Utilities (OPTIONAL, CREATIVE LAYER)

⚠️ IMPORTANT
- This module is NOT a scientific validation tool.
- Treat outputs as *interpretive/creative metadata* useful for film/game UX.
- Do not present results as factual causation or "truth".
- Provide disclaimers in UI and always allow users to disable this layer.

Supported:
- Simple alphanumeric mappings (A1Z26, ASCII sum)
- Custom alphabets (latin, french accented normalized)
- Word/phrase normalization utilities

If you want Hebrew/Greek gematria variants, add explicit alphabets and document them.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


def normalize_text(s: str) -> str:
    """Lowercase + strip accents + keep alphanumerics/spaces."""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


A1Z26: Dict[str, int] = {chr(ord("a") + i): i + 1 for i in range(26)}


def a1z26_sum(text: str) -> int:
    t = normalize_text(text).replace(" ", "")
    return sum(A1Z26.get(ch, 0) for ch in t)


def ascii_sum(text: str) -> int:
    t = normalize_text(text)
    return sum(ord(ch) for ch in t)


def token_sums(text: str) -> Dict[str, int]:
    """Return per-token A1Z26 sums to help interpret patterns without overclaiming."""
    t = normalize_text(text)
    out = {}
    for tok in t.split():
        out[tok] = a1z26_sum(tok)
    return out


@dataclass
class GematriaResult:
    input_text: str
    normalized: str
    method: str
    total: int
    per_token: Optional[Dict[str, int]] = None


def analyze(text: str, methods: Optional[List[str]] = None, include_tokens: bool = True) -> List[GematriaResult]:
    methods = methods or ["A1Z26", "ASCII"]
    norm = normalize_text(text)
    results: List[GematriaResult] = []
    for m in methods:
        if m.upper() == "A1Z26":
            results.append(GematriaResult(text, norm, "A1Z26", a1z26_sum(text), token_sums(text) if include_tokens else None))
        elif m.upper() == "ASCII":
            results.append(GematriaResult(text, norm, "ASCII", ascii_sum(text), None if not include_tokens else None))
        else:
            # Unknown method: skip to avoid silent wrongness
            continue
    return results
