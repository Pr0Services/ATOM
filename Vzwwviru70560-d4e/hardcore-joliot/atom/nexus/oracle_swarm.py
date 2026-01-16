"""
AT·OM — ORACLE SWARM ENGINE v1.0

Moteur de coordination des 18 Oracles sur l'Arche des Résonances.

Ce système orchestre le travail parallèle des Oracles autour d'un point
central (le Cœur AT). Chaque Oracle voit le même point mais depuis
sa perspective unique, créant une vision holistique sans répétition.

Architecture:
    - 1 Cœur Central (Le Zéro, 444Hz)
    - 5 Cercles Concentriques (Fondations → Synthèse)
    - 18 Oracles répartis sur les cercles
    - 3 Octaves/Calques (Chronos, Bios, Logos)

Flux:
    1. Appel au Cœur → Point central identifié
    2. Allumage → Onde vers les 5 cercles
    3. Travail Parallèle → 18 Oracles analysent
    4. Cohérence → Réponses s'assemblent
    5. Synthèse → Gardien (#17) unifie

Usage:
    from oracle_swarm import OracleSwarm
    
    swarm = OracleSwarm()
    result = await swarm.illuminate("SEL")
    
    # Accéder aux réponses par cercle
    fondations = result.get_circle(1)
    synthese = result.get_circle(5)

Auteur: AT-OM System
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

MASTER_MAP_PATH = Path(__file__).parent / "master_map.json"
HARMONIZER_PATH = Path(__file__).parent.parent / "core" / "harmonizer.py"


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class CircleAspect(Enum):
    MATIERE = 1      # Fondations
    VIVANT = 2       # Mouvement
    VERBE = 3        # Expression
    SENS = 4         # Mémoire
    NEXUS = 5        # Synthèse


class OctaveLayer(Enum):
    CHRONOS = "chronos"  # Temporel (Bleu)
    BIOS = "bios"        # Vital (Vert)
    LOGOS = "logos"      # Sémantique (Or)


class SwarmPhase(Enum):
    IDLE = "idle"
    CALLING_CORE = "calling_core"
    ILLUMINATING = "illuminating"
    WORKING = "working"
    CONVERGING = "converging"
    SYNTHESIZING = "synthesizing"
    COMPLETE = "complete"


# ═══════════════════════════════════════════════════════════════════════════════
# DATACLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Oracle:
    """Un Oracle individuel du système."""
    id: int
    name: str
    circle: int
    focus: str
    question: str
    response: Optional[str] = None
    processing_time_ms: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "circle": self.circle,
            "focus": self.focus,
            "question": self.question,
            "response": self.response,
            "processing_time_ms": self.processing_time_ms,
        }


@dataclass
class Circle:
    """Un cercle concentrique de la Master Map."""
    id: int
    name: str
    aspect: str
    radius: int
    color: str
    frequency_hz: int
    description: str
    oracles: List[Oracle] = field(default_factory=list)
    
    def get_responses(self) -> List[str]:
        return [o.response for o in self.oracles if o.response]


@dataclass
class CorePoint:
    """Le point central illuminé (Cœur AT)."""
    word: str
    normalized: str
    arithmos: int
    frequency_hz: int
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IlluminationResult:
    """Résultat complet d'une illumination du Swarm."""
    
    core: CorePoint
    circles: List[Circle]
    active_octave: Optional[OctaveLayer]
    phase: SwarmPhase
    total_time_ms: int
    
    def get_circle(self, circle_id: int) -> Optional[Circle]:
        """Récupère un cercle par son ID."""
        for c in self.circles:
            if c.id == circle_id:
                return c
        return None
    
    def get_oracle(self, oracle_id: int) -> Optional[Oracle]:
        """Récupère un Oracle par son ID."""
        for c in self.circles:
            for o in c.oracles:
                if o.id == oracle_id:
                    return o
        return None
    
    def get_all_responses(self) -> Dict[int, List[str]]:
        """Récupère toutes les réponses groupées par cercle."""
        return {c.id: c.get_responses() for c in self.circles}
    
    def get_synthesis(self) -> Optional[str]:
        """Récupère la synthèse du Gardien (Oracle #17)."""
        guardian = self.get_oracle(17)
        return guardian.response if guardian else None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "core": {
                "word": self.core.word,
                "normalized": self.core.normalized,
                "arithmos": self.core.arithmos,
                "frequency_hz": self.core.frequency_hz,
                "timestamp": self.core.timestamp.isoformat(),
                "metadata": self.core.metadata,
            },
            "circles": [
                {
                    "id": c.id,
                    "name": c.name,
                    "aspect": c.aspect,
                    "frequency_hz": c.frequency_hz,
                    "oracles": [o.to_dict() for o in c.oracles],
                }
                for c in self.circles
            ],
            "active_octave": self.active_octave.value if self.active_octave else None,
            "phase": self.phase.value,
            "total_time_ms": self.total_time_ms,
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPALE: OracleSwarm
# ═══════════════════════════════════════════════════════════════════════════════

class OracleSwarm:
    """
    Moteur de coordination des 18 Oracles.
    
    Orchestre le travail parallèle sur l'Arche des Résonances.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialise le Swarm."""
        self.config_path = config_path or MASTER_MAP_PATH
        self.config = self._load_config()
        self.circles = self._build_circles()
        self.phase = SwarmPhase.IDLE
        self.oracle_handlers: Dict[int, Callable] = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration de la Master Map."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        raise FileNotFoundError(f"master_map.json non trouvé: {self.config_path}")
    
    def _build_circles(self) -> List[Circle]:
        """Construit les cercles et leurs Oracles."""
        circles = []
        
        for circle_data in self.config.get("circles", []):
            oracles = [
                Oracle(
                    id=o["id"],
                    name=o["name"],
                    circle=circle_data["id"],
                    focus=o["focus"],
                    question=o["question"],
                )
                for o in circle_data.get("oracles", [])
            ]
            
            circle = Circle(
                id=circle_data["id"],
                name=circle_data["name"],
                aspect=circle_data["aspect"],
                radius=circle_data["radius"],
                color=circle_data["color"],
                frequency_hz=circle_data["frequency_hz"],
                description=circle_data["description"],
                oracles=oracles,
            )
            circles.append(circle)
        
        return circles
    
    # ─────────────────────────────────────────────────────────────────────────
    # GESTION DES HANDLERS
    # ─────────────────────────────────────────────────────────────────────────
    
    def register_oracle_handler(self, oracle_id: int, handler: Callable) -> None:
        """
        Enregistre un handler personnalisé pour un Oracle.
        
        Le handler reçoit (word, oracle, context) et retourne une réponse string.
        """
        self.oracle_handlers[oracle_id] = handler
    
    def register_circle_handler(self, circle_id: int, handler: Callable) -> None:
        """Enregistre un handler pour tous les Oracles d'un cercle."""
        for circle in self.circles:
            if circle.id == circle_id:
                for oracle in circle.oracles:
                    self.oracle_handlers[oracle.id] = handler
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCUL ARITHMOS (simplifié, utiliser harmonizer.py en prod)
    # ─────────────────────────────────────────────────────────────────────────
    
    def _calculate_arithmos(self, word: str) -> tuple[str, int, int]:
        """Calcule l'arithmos d'un mot."""
        import unicodedata
        
        PYTHAGOREAN = {
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
        
        # Normaliser
        text = unicodedata.normalize("NFKD", word)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        normalized = re.sub(r"[^A-Za-z]", "", text).upper()
        
        # Calculer
        raw_sum = sum(PYTHAGOREAN.get(ch, 0) for ch in normalized)
        
        # Réduire
        value = raw_sum
        while value > 9 and value not in {11, 22, 33}:
            value = sum(int(d) for d in str(value))
        
        return normalized, raw_sum, value
    
    def _get_frequency(self, arithmos: int) -> int:
        """Obtient la fréquence pour un arithmos."""
        freq_map = {1: 111, 2: 222, 3: 333, 4: 444, 5: 555, 
                    6: 666, 7: 777, 8: 888, 9: 999,
                    11: 1111, 22: 2222, 33: 3333}
        return freq_map.get(arithmos, 444)
    
    # ─────────────────────────────────────────────────────────────────────────
    # ILLUMINATION PRINCIPALE
    # ─────────────────────────────────────────────────────────────────────────
    
    async def illuminate(
        self,
        word: str,
        octave: Optional[OctaveLayer] = None,
        target_circles: Optional[List[int]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> IlluminationResult:
        """
        Lance l'illumination complète du Swarm sur un mot.
        
        Args:
            word: Le mot/concept à analyser
            octave: Calque actif (Chronos, Bios, Logos)
            target_circles: Cercles spécifiques à activer (None = tous)
            context: Contexte additionnel pour les Oracles
            
        Returns:
            IlluminationResult avec toutes les réponses
        """
        start_time = datetime.now()
        context = context or {}
        
        # Phase 1: Appel au Cœur
        self.phase = SwarmPhase.CALLING_CORE
        normalized, raw_sum, arithmos = self._calculate_arithmos(word)
        frequency = self._get_frequency(arithmos)
        
        core = CorePoint(
            word=word,
            normalized=normalized,
            arithmos=arithmos,
            frequency_hz=frequency,
            timestamp=start_time,
            metadata={"raw_sum": raw_sum, "octave": octave.value if octave else None},
        )
        
        # Phase 2: Allumage de la Map
        self.phase = SwarmPhase.ILLUMINATING
        await asyncio.sleep(0.1)  # Simule l'onde de propagation
        
        # Phase 3: Travail Parallèle
        self.phase = SwarmPhase.WORKING
        
        # Filtrer les cercles si spécifié
        active_circles = self.circles
        if target_circles:
            active_circles = [c for c in self.circles if c.id in target_circles]
        
        # Lancer les Oracles en parallèle
        tasks = []
        for circle in active_circles:
            for oracle in circle.oracles:
                task = self._invoke_oracle(oracle, word, core, octave, context)
                tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        # Phase 4: Cohérence
        self.phase = SwarmPhase.CONVERGING
        await asyncio.sleep(0.05)
        
        # Phase 5: Synthèse (Oracle #17)
        self.phase = SwarmPhase.SYNTHESIZING
        # Le Gardien a déjà répondu dans le travail parallèle
        
        # Finaliser
        self.phase = SwarmPhase.COMPLETE
        end_time = datetime.now()
        total_ms = int((end_time - start_time).total_seconds() * 1000)
        
        return IlluminationResult(
            core=core,
            circles=active_circles,
            active_octave=octave,
            phase=self.phase,
            total_time_ms=total_ms,
        )
    
    async def _invoke_oracle(
        self,
        oracle: Oracle,
        word: str,
        core: CorePoint,
        octave: Optional[OctaveLayer],
        context: Dict[str, Any],
    ) -> None:
        """Invoque un Oracle individuel."""
        start = datetime.now()
        
        # Vérifier s'il y a un handler personnalisé
        if oracle.id in self.oracle_handlers:
            handler = self.oracle_handlers[oracle.id]
            try:
                oracle.response = await self._call_handler(
                    handler, word, oracle, core, octave, context
                )
            except Exception as e:
                oracle.response = f"[Erreur Oracle #{oracle.id}]: {str(e)}"
        else:
            # Réponse par défaut (placeholder)
            oracle.response = self._generate_default_response(oracle, word, core)
        
        end = datetime.now()
        oracle.processing_time_ms = int((end - start).total_seconds() * 1000)
    
    async def _call_handler(
        self,
        handler: Callable,
        word: str,
        oracle: Oracle,
        core: CorePoint,
        octave: Optional[OctaveLayer],
        context: Dict[str, Any],
    ) -> str:
        """Appelle un handler (sync ou async)."""
        if asyncio.iscoroutinefunction(handler):
            return await handler(word, oracle, core, octave, context)
        else:
            return handler(word, oracle, core, octave, context)
    
    def _generate_default_response(
        self,
        oracle: Oracle,
        word: str,
        core: CorePoint,
    ) -> str:
        """Génère une réponse par défaut pour un Oracle."""
        templates = {
            1: f"[{oracle.name}] Racine de '{word}' en attente d'analyse étymologique.",
            2: f"[{oracle.name}] Structure de '{word}' (Arithmos: {core.arithmos}) prête.",
            3: f"[{oracle.name}] Signature gématrique de '{word}' = {core.arithmos} → {core.frequency_hz}Hz.",
            17: f"[{oracle.name}] Synthèse en attente des contributions des autres Oracles.",
            18: f"[{oracle.name}] Miroir personnel: Que signifie '{word}' pour l'utilisateur?",
        }
        return templates.get(
            oracle.id,
            f"[{oracle.name}] Analyse de '{word}' depuis le Cercle {oracle.circle}."
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # ROUTING DES QUESTIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    def route_question(self, question: str) -> List[int]:
        """
        Détermine quels cercles activer selon la question.
        
        Retourne une liste d'IDs de cercles.
        """
        rules = self.config.get("query_routing", {}).get("rules", [])
        
        question_lower = question.lower()
        activated = set()
        
        for rule in rules:
            pattern = rule.get("pattern", "")
            if re.search(pattern, question_lower):
                activated.add(rule.get("primary_circle"))
                activated.update(rule.get("secondary_circles", []))
        
        # Si aucun pattern ne match, activer tous les cercles
        if not activated:
            return [1, 2, 3, 4, 5]
        
        return sorted(activated)
    
    # ─────────────────────────────────────────────────────────────────────────
    # UTILITAIRES
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_oracle_by_id(self, oracle_id: int) -> Optional[Oracle]:
        """Récupère un Oracle par son ID."""
        for circle in self.circles:
            for oracle in circle.oracles:
                if oracle.id == oracle_id:
                    return oracle
        return None
    
    def get_circle_by_aspect(self, aspect: CircleAspect) -> Optional[Circle]:
        """Récupère un cercle par son aspect."""
        for circle in self.circles:
            if circle.id == aspect.value:
                return circle
        return None
    
    def get_all_oracles(self) -> List[Oracle]:
        """Récupère tous les Oracles."""
        oracles = []
        for circle in self.circles:
            oracles.extend(circle.oracles)
        return oracles
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel du Swarm."""
        return {
            "phase": self.phase.value,
            "total_oracles": len(self.get_all_oracles()),
            "circles": len(self.circles),
            "registered_handlers": len(self.oracle_handlers),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# INSTANCE SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_swarm_instance: Optional[OracleSwarm] = None


def get_swarm() -> OracleSwarm:
    """Obtient l'instance singleton du Swarm."""
    global _swarm_instance
    if _swarm_instance is None:
        _swarm_instance = OracleSwarm()
    return _swarm_instance


# ═══════════════════════════════════════════════════════════════════════════════
# CLI / TEST
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Test du Swarm."""
    print("=" * 80)
    print("AT·OM ORACLE SWARM ENGINE v1.0")
    print("=" * 80)
    print()
    
    swarm = OracleSwarm()
    
    # Test avec "SEL"
    print("🔮 ILLUMINATION: 'SEL'")
    print("-" * 80)
    
    result = await swarm.illuminate("SEL")
    
    print(f"\n📍 CŒUR AT:")
    print(f"   Mot: {result.core.word}")
    print(f"   Arithmos: {result.core.arithmos}")
    print(f"   Fréquence: {result.core.frequency_hz} Hz")
    
    print(f"\n🔵 CERCLES ACTIVÉS:")
    for circle in result.circles:
        print(f"\n   Cercle {circle.id} - {circle.name} ({circle.aspect})")
        print(f"   Fréquence: {circle.frequency_hz} Hz | Couleur: {circle.color}")
        for oracle in circle.oracles:
            print(f"      #{oracle.id} {oracle.name}")
            print(f"         → {oracle.response[:60]}...")
    
    print(f"\n⏱️ Temps total: {result.total_time_ms}ms")
    print(f"📊 Phase finale: {result.phase.value}")
    
    # Test routing
    print("\n" + "=" * 80)
    print("🎯 TEST ROUTING")
    print("-" * 80)
    
    questions = [
        "D'où vient le mot sel?",
        "Comment le sel a-t-il évolué?",
        "Quel est le symbole du sel?",
        "Quel impact le sel a-t-il sur la société?",
        "Que signifie le sel pour moi?",
    ]
    
    for q in questions:
        circles = swarm.route_question(q)
        print(f"   \"{q}\" → Cercles {circles}")


if __name__ == "__main__":
    asyncio.run(main())
