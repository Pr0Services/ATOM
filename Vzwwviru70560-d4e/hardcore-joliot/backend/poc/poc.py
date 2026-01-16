"""
============================================================================
CHE·NU™ V69 — POC MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_ONBOARDING_DATA_SYNTHESIS_ACCELERATOR.md
- CHE-NU_POC_CRISIS_GAME_INVESTOR.md

"Ne me dites pas que la stratégie est bonne. Faites‑la survivre à une crise."

Principle: GOUVERNANCE > EXÉCUTION
Value: Fast POC success, Proof by experience
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import hashlib
import json
import copy
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    return str(uuid.uuid4())

def compute_hash(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def sign_artifact(data: Dict[str, Any], signer: str) -> str:
    return compute_hash(f"{json.dumps(data, sort_keys=True, default=str)}:{signer}")


# ============================================================================
# 1. ONBOARDING DATA SYNTHESIS ACCELERATOR
# ============================================================================

class SourceType(str, Enum):
    PDF = "pdf"
    SLIDES = "slides"
    NOTES = "notes"
    INTERVIEW = "interview"


@dataclass
class ExtractedSlot:
    slot_id: str
    name: str
    value: Any
    unit: str = ""
    confidence: float = 0.0
    source: str = ""
    source_type: SourceType = SourceType.NOTES


@dataclass
class AssumptionRecord:
    assumption_id: str
    slot_id: str
    assumption: str
    default_value: Any
    rationale: str


@dataclass
class MissingDataReport:
    report_id: str
    missing_slots: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    completeness_score: float = 0.0


class OnboardingAccelerator:
    """Enable meaningful simulations within 24-48h"""
    
    def __init__(self):
        self._slots: Dict[str, ExtractedSlot] = {}
        self._assumptions: List[AssumptionRecord] = []
        self._required_slots = [
            "revenue", "cost", "margin", "headcount",
            "inventory", "capacity", "growth_rate",
        ]
    
    def ingest_source(
        self,
        source_type: SourceType,
        content: Dict[str, Any],
        source_name: str = "",
    ) -> List[ExtractedSlot]:
        extracted = []
        confidence_map = {
            SourceType.PDF: 0.9,
            SourceType.SLIDES: 0.8,
            SourceType.NOTES: 0.6,
            SourceType.INTERVIEW: 0.7,
        }
        
        for key, value in content.items():
            if isinstance(value, (int, float, str)):
                slot = ExtractedSlot(
                    slot_id=generate_id(),
                    name=key,
                    value=value,
                    confidence=confidence_map.get(source_type, 0.5),
                    source=source_name,
                    source_type=source_type,
                )
                self._slots[key] = slot
                extracted.append(slot)
        
        logger.info(f"Extracted {len(extracted)} slots from {source_type.value}")
        return extracted
    
    def fill_missing_with_assumptions(self) -> List[AssumptionRecord]:
        new_assumptions = []
        defaults = {
            "revenue": (1_000_000, "Industry average"),
            "cost": (600_000, "60% cost ratio"),
            "margin": (0.4, "Standard 40% margin"),
            "headcount": (50, "Mid-size team"),
            "inventory": (100_000, "1 month buffer"),
            "capacity": (0.8, "80% utilization"),
            "growth_rate": (0.1, "10% annual growth"),
        }
        
        for slot_name in self._required_slots:
            if slot_name not in self._slots:
                default_val, rationale = defaults.get(slot_name, (0, "Unknown"))
                assumption = AssumptionRecord(
                    assumption_id=generate_id(),
                    slot_id=slot_name,
                    assumption=f"Default value for {slot_name}",
                    default_value=default_val,
                    rationale=rationale,
                )
                self._assumptions.append(assumption)
                new_assumptions.append(assumption)
                
                self._slots[slot_name] = ExtractedSlot(
                    slot_id=generate_id(),
                    name=slot_name,
                    value=default_val,
                    confidence=0.3,
                    source="assumption",
                    source_type=SourceType.NOTES,
                )
        
        return new_assumptions
    
    def generate_missing_report(self) -> MissingDataReport:
        missing = []
        recommendations = []
        
        for slot_name in self._required_slots:
            slot = self._slots.get(slot_name)
            if not slot or slot.confidence < 0.5:
                missing.append(slot_name)
                recommendations.append(f"Provide verified {slot_name} data")
        
        total = len(self._required_slots)
        found = total - len(missing)
        
        return MissingDataReport(
            report_id=generate_id(),
            missing_slots=missing,
            recommendations=recommendations,
            completeness_score=found / total if total > 0 else 0,
        )
    
    def generate_synthetic_world(self) -> Dict[str, Any]:
        world = {
            "world_id": generate_id(),
            "synthetic": True,
            "generated_at": datetime.utcnow().isoformat(),
            "slots": {name: slot.value for name, slot in self._slots.items()},
            "confidence_scores": {name: slot.confidence for name, slot in self._slots.items()},
        }
        logger.info(f"Generated synthetic world with {len(world['slots'])} slots")
        return world


# ============================================================================
# 2. POC CRISIS GAME (INVESTOR)
# ============================================================================

class CrisisType(str, Enum):
    SUPPLY_SHOCK = "supply_shock"
    ENERGY_SPIKE = "energy_spike"
    DEMAND_CRASH = "demand_crash"
    REGULATION = "regulation"
    STRIKE = "strike"


@dataclass
class InterventionCard:
    card_id: str
    name: str
    description: str
    improves: Dict[str, float] = field(default_factory=dict)
    degrades: Dict[str, float] = field(default_factory=dict)
    cost: float = 0.0


@dataclass
class TrustScore:
    score_id: str
    opa_compliance: float = 0.0
    causal_resilience: float = 0.0
    prediction_accuracy: float = 0.0
    total_score: float = 0.0
    badge: str = ""


@dataclass
class GameArtifacts:
    manifest: Dict[str, Any] = field(default_factory=dict)
    xr_pack_signature: str = ""
    trust_certificate: Dict[str, Any] = field(default_factory=dict)
    audit_merkle_root: str = ""


class CrisisGame:
    """POC Crisis Game - Démontrer CHE·NU en 15 minutes"""
    
    def __init__(self):
        self.game_id = generate_id()
        self._state: Dict[str, float] = {}
        self._decisions: List[Dict] = []
        self._shocks: List[Dict] = []
        self._cards: Dict[str, InterventionCard] = {}
        self._setup_default_cards()
    
    def _setup_default_cards(self) -> None:
        cards = [
            InterventionCard("card_1", "Diversify Suppliers", "Reduce dependency",
                           {"supply_stability": 0.3}, {"cost": 0.1}, 50000),
            InterventionCard("card_2", "Emergency Inventory", "Build safety stock",
                           {"inventory": 0.5}, {"cash_flow": 0.2}, 100000),
            InterventionCard("card_3", "Price Increase", "Pass costs to customers",
                           {"margin": 0.15}, {"demand": 0.1}, 0),
            InterventionCard("card_4", "Cost Cutting", "Reduce expenses",
                           {"cost": -0.2}, {"quality": 0.15}, 0),
        ]
        for card in cards:
            self._cards[card.card_id] = card
    
    def initialize(self, initial_state: Dict[str, float]) -> Dict[str, Any]:
        self._state = copy.deepcopy(initial_state)
        self._state["synthetic"] = True
        return {
            "game_id": self.game_id,
            "initial_state": self._state,
            "available_cards": list(self._cards.keys()),
            "message": "Sandbox / No real impact",
        }
    
    def play_card(self, card_id: str) -> Dict[str, Any]:
        card = self._cards.get(card_id)
        if not card:
            return {"error": "Card not found"}
        
        for key, delta in card.improves.items():
            self._state[key] = self._state.get(key, 0) * (1 + delta)
        for key, delta in card.degrades.items():
            if key in self._state:
                self._state[key] *= (1 - delta)
        
        if "budget" in self._state:
            self._state["budget"] -= card.cost
        
        self._decisions.append({
            "card_id": card_id,
            "card_name": card.name,
            "timestamp": datetime.utcnow().isoformat(),
            "state_after": copy.deepcopy(self._state),
        })
        
        return {"card_played": card.name, "new_state": self._state}
    
    def inject_shock(self, crisis_type: CrisisType) -> Dict[str, Any]:
        shock_effects = {
            CrisisType.SUPPLY_SHOCK: {"inventory": 0.5, "cost": 1.3},
            CrisisType.ENERGY_SPIKE: {"energy_cost": 2.0, "margin": 0.8},
            CrisisType.DEMAND_CRASH: {"revenue": 0.6, "orders": 0.5},
            CrisisType.REGULATION: {"compliance_cost": 1.5, "capacity": 0.9},
            CrisisType.STRIKE: {"production": 0.3, "delivery": 0.4},
        }
        
        effects = shock_effects.get(crisis_type, {})
        for key, factor in effects.items():
            self._state[key] = self._state.get(key, 1.0) * factor
        
        self._shocks.append({
            "crisis_type": crisis_type.value,
            "effects": effects,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        logger.warning(f"Crisis injected: {crisis_type.value}")
        return {"crisis": crisis_type.value, "impact": effects, "new_state": self._state}
    
    def calculate_trust_score(self) -> TrustScore:
        opa_score = 1.0  # All synthetic = OPA compliant
        
        resilience = 0.0
        for metric in ["revenue", "margin", "inventory"]:
            if metric in self._state:
                resilience += min(1.0, self._state[metric] / 1_000_000) / 3
        
        prediction = min(1.0, len(self._decisions) / max(1, len(self._shocks) + 1))
        
        total = (opa_score * 0.3 + resilience * 0.4 + prediction * 0.3) * 100
        
        if total >= 80:
            badge = "🏆 Strategic Leader"
        elif total >= 60:
            badge = "⭐ Resilient Thinker"
        elif total >= 40:
            badge = "📊 Emerging Strategist"
        else:
            badge = "🎯 Learning Mode"
        
        return TrustScore(
            score_id=generate_id(),
            opa_compliance=opa_score * 100,
            causal_resilience=resilience * 100,
            prediction_accuracy=prediction * 100,
            total_score=total,
            badge=badge,
        )
    
    def generate_artifacts(self) -> GameArtifacts:
        trust = self.calculate_trust_score()
        
        manifest = {
            "game_id": self.game_id,
            "completed_at": datetime.utcnow().isoformat(),
            "decisions_count": len(self._decisions),
            "shocks_count": len(self._shocks),
            "final_state": self._state,
            "synthetic": True,
        }
        
        xr_sig = sign_artifact({"game_id": self.game_id}, "crisis_game")
        
        certificate = {
            "certificate_id": generate_id(),
            "game_id": self.game_id,
            "trust_score": trust.total_score,
            "badge": trust.badge,
            "signature": sign_artifact({"score": trust.total_score}, "trust_authority"),
        }
        
        audit_data = [compute_hash(d) for d in self._decisions + self._shocks]
        merkle = compute_hash("".join(audit_data)) if audit_data else "empty"
        
        return GameArtifacts(
            manifest=manifest,
            xr_pack_signature=xr_sig,
            trust_certificate=certificate,
            audit_merkle_root=merkle,
        )
    
    def get_game_summary(self) -> str:
        return "CHE·NU™ ne remplace pas les décideurs. Il révèle ceux qui savent décider sous contrainte."


__all__ = [
    "SourceType", "ExtractedSlot", "AssumptionRecord", "MissingDataReport", "OnboardingAccelerator",
    "CrisisType", "InterventionCard", "TrustScore", "GameArtifacts", "CrisisGame",
    "generate_id", "compute_hash", "sign_artifact",
]
