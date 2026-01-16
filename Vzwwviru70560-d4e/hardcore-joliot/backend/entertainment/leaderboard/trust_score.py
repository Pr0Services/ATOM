"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT TRUST SCORE & LEADERBOARD
============================================================================
Spec: GPT1/CHE-NU_ENT_TRUST_SCORE_LEADERBOARD.md

Objective: Measure human decision quality.

Three Pillars:
1. Conformité (OPA Alignment)
2. Résilience (Causal Stability)
3. Précision (Prediction Gap)

Features:
- Scores anonymisés
- Artifacts signés
- Badges Trust-Certified
- XR Visualization: Agora des stratégies, Replay immersif
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    TrustScore,
    TrustPillar,
    LeaderboardEntry,
    TrustBadge,
    GameAction,
    SimulationResult,
    generate_id,
    sign_artifact,
    anonymize_id,
)

logger = logging.getLogger(__name__)


# ============================================================================
# TRUST SCORE CALCULATOR
# ============================================================================

class TrustScoreCalculator:
    """
    Calculate trust scores based on player decisions.
    
    Per spec: Mesurer la qualité décisionnelle humaine
    """
    
    # Pillar weights
    CONFORMITY_WEIGHT = 0.35
    RESILIENCE_WEIGHT = 0.35
    PRECISION_WEIGHT = 0.30
    
    def __init__(self):
        self._scores: Dict[str, TrustScore] = {}
        self._decision_history: Dict[str, List[Dict]] = {}
    
    def calculate_conformity(
        self,
        actions: List[GameAction],
        opa_violations: int = 0,
    ) -> float:
        """
        Calculate OPA Alignment score.
        
        Per spec pillar: Conformité (OPA Alignment)
        """
        if not actions:
            return 50.0
        
        total_actions = len(actions)
        compliant_actions = total_actions - opa_violations
        
        # Base score from compliance ratio
        compliance_ratio = compliant_actions / total_actions
        
        # Scale to 0-100
        score = compliance_ratio * 100
        
        return min(100, max(0, score))
    
    def calculate_resilience(
        self,
        results: List[SimulationResult],
    ) -> float:
        """
        Calculate Causal Stability score.
        
        Per spec pillar: Résilience (Causal Stability)
        """
        if not results:
            return 50.0
        
        # Average divergence (lower is better)
        avg_divergence = sum(r.divergence_score for r in results) / len(results)
        
        # Calculate stability (inverse of divergence)
        stability = 1 - min(1, avg_divergence)
        
        # Bonus for consistent low divergence
        low_divergence_count = sum(1 for r in results if r.divergence_score < 0.2)
        consistency_bonus = (low_divergence_count / len(results)) * 20
        
        score = stability * 80 + consistency_bonus
        
        return min(100, max(0, score))
    
    def calculate_precision(
        self,
        predictions: List[Dict[str, float]],
        actuals: List[Dict[str, float]],
    ) -> float:
        """
        Calculate Prediction Gap score.
        
        Per spec pillar: Précision (Prediction Gap)
        """
        if not predictions or not actuals:
            return 50.0
        
        total_gap = 0
        count = 0
        
        for pred, actual in zip(predictions, actuals):
            for key in pred:
                if key in actual:
                    gap = abs(pred[key] - actual[key])
                    total_gap += gap
                    count += 1
        
        if count == 0:
            return 50.0
        
        avg_gap = total_gap / count
        
        # Lower gap = higher score
        # Assume gap is normalized 0-1
        score = (1 - min(1, avg_gap)) * 100
        
        return min(100, max(0, score))
    
    def calculate_overall(
        self,
        conformity: float,
        resilience: float,
        precision: float,
    ) -> float:
        """Calculate weighted overall score"""
        return (
            conformity * self.CONFORMITY_WEIGHT +
            resilience * self.RESILIENCE_WEIGHT +
            precision * self.PRECISION_WEIGHT
        )
    
    def update_score(
        self,
        player_id: str,
        actions: List[GameAction],
        results: List[SimulationResult],
        opa_violations: int = 0,
        predictions: List[Dict] = None,
        actuals: List[Dict] = None,
    ) -> TrustScore:
        """Update player trust score"""
        predictions = predictions or []
        actuals = actuals or []
        
        # Calculate pillars
        conformity = self.calculate_conformity(actions, opa_violations)
        resilience = self.calculate_resilience(results)
        precision = self.calculate_precision(predictions, actuals)
        overall = self.calculate_overall(conformity, resilience, precision)
        
        # Get or create score
        if player_id in self._scores:
            score = self._scores[player_id]
            # Rolling average with existing score
            score.conformity_score = (score.conformity_score + conformity) / 2
            score.resilience_score = (score.resilience_score + resilience) / 2
            score.precision_score = (score.precision_score + precision) / 2
            score.overall_score = self.calculate_overall(
                score.conformity_score,
                score.resilience_score,
                score.precision_score,
            )
            score.decision_count += len(actions)
            score.updated_at = datetime.utcnow()
        else:
            score = TrustScore(
                score_id=generate_id(),
                player_id=player_id,
                conformity_score=conformity,
                resilience_score=resilience,
                precision_score=precision,
                overall_score=overall,
                decision_count=len(actions),
            )
            self._scores[player_id] = score
        
        logger.info(
            f"Updated trust score for {player_id}: "
            f"conformity={score.conformity_score:.1f}, "
            f"resilience={score.resilience_score:.1f}, "
            f"precision={score.precision_score:.1f}, "
            f"overall={score.overall_score:.1f}"
        )
        
        return score
    
    def get_score(self, player_id: str) -> Optional[TrustScore]:
        """Get player score"""
        return self._scores.get(player_id)


# ============================================================================
# LEADERBOARD MANAGER
# ============================================================================

class LeaderboardManager:
    """
    Manage anonymized leaderboard.
    
    Per spec: Scores anonymisés, Artifacts signés
    """
    
    def __init__(self, calculator: TrustScoreCalculator):
        self.calculator = calculator
        self._entries: List[LeaderboardEntry] = []
    
    def refresh(self) -> List[LeaderboardEntry]:
        """Refresh leaderboard from current scores"""
        self._entries = []
        
        # Get all scores
        scores = list(self.calculator._scores.values())
        
        # Sort by overall score
        scores.sort(key=lambda s: s.overall_score, reverse=True)
        
        # Create anonymized entries
        for rank, score in enumerate(scores, 1):
            entry = LeaderboardEntry(
                entry_id=generate_id(),
                anonymous_id=anonymize_id(score.player_id),
                score=score.overall_score,
                rank=rank,
                badge=self._determine_badge(score.overall_score),
                artifact_ref=f"artifact://trust_score/{score.score_id}",
            )
            
            # Sign entry
            entry.signature = sign_artifact({
                "entry_id": entry.entry_id,
                "anonymous_id": entry.anonymous_id,
                "score": entry.score,
                "rank": entry.rank,
            }, "leaderboard_authority")
            
            self._entries.append(entry)
        
        return self._entries
    
    def _determine_badge(self, score: float) -> str:
        """Determine badge level from score"""
        if score >= 90:
            return "platinum"
        elif score >= 75:
            return "gold"
        elif score >= 60:
            return "silver"
        elif score >= 40:
            return "bronze"
        else:
            return "none"
    
    def get_top(self, n: int = 10) -> List[LeaderboardEntry]:
        """Get top N entries"""
        return self._entries[:n]
    
    def get_player_rank(self, player_id: str) -> Optional[LeaderboardEntry]:
        """Get player's leaderboard entry"""
        anonymous_id = anonymize_id(player_id)
        
        for entry in self._entries:
            if entry.anonymous_id == anonymous_id:
                return entry
        
        return None


# ============================================================================
# BADGE ISSUER
# ============================================================================

class BadgeIssuer:
    """
    Issue Trust-Certified badges.
    
    Per spec: Badges Trust-Certified
    """
    
    BADGE_THRESHOLDS = {
        "trust_certified_platinum": 90,
        "trust_certified_gold": 75,
        "trust_certified_silver": 60,
        "trust_certified_bronze": 40,
    }
    
    CATEGORY_BADGES = {
        "conformity_expert": ("conformity", 85),
        "resilience_master": ("resilience", 85),
        "precision_ace": ("precision", 85),
    }
    
    def __init__(self):
        self._badges: Dict[str, List[TrustBadge]] = {}  # player_id → badges
    
    def check_and_issue(
        self,
        score: TrustScore,
    ) -> List[TrustBadge]:
        """Check eligibility and issue badges"""
        new_badges = []
        player_id = score.player_id
        
        if player_id not in self._badges:
            self._badges[player_id] = []
        
        existing = {b.level for b in self._badges[player_id]}
        
        # Check overall badges
        for badge_type, threshold in self.BADGE_THRESHOLDS.items():
            level = badge_type.split("_")[-1]
            
            if score.overall_score >= threshold and level not in existing:
                badge = TrustBadge(
                    badge_id=generate_id(),
                    player_id=player_id,
                    level=level,
                    category="overall",
                    artifact_ref=f"artifact://badge/{generate_id()}",
                )
                
                badge.signature = sign_artifact({
                    "badge_id": badge.badge_id,
                    "player_id": player_id,
                    "level": level,
                }, "badge_authority")
                
                self._badges[player_id].append(badge)
                new_badges.append(badge)
                
                logger.info(f"Issued {level} badge to player {player_id}")
        
        # Check category badges
        pillar_scores = {
            "conformity": score.conformity_score,
            "resilience": score.resilience_score,
            "precision": score.precision_score,
        }
        
        existing_categories = {b.category for b in self._badges[player_id]}
        
        for badge_name, (pillar, threshold) in self.CATEGORY_BADGES.items():
            if pillar_scores[pillar] >= threshold and badge_name not in existing_categories:
                badge = TrustBadge(
                    badge_id=generate_id(),
                    player_id=player_id,
                    level="specialist",
                    category=badge_name,
                    artifact_ref=f"artifact://badge/{generate_id()}",
                )
                
                badge.signature = sign_artifact({
                    "badge_id": badge.badge_id,
                    "category": badge_name,
                }, "badge_authority")
                
                self._badges[player_id].append(badge)
                new_badges.append(badge)
        
        return new_badges
    
    def get_player_badges(self, player_id: str) -> List[TrustBadge]:
        """Get all badges for a player"""
        return self._badges.get(player_id, [])


# ============================================================================
# XR VISUALIZATION
# ============================================================================

class XRVisualization:
    """
    XR visualization for leaderboard and strategies.
    
    Per spec: Agora des stratégies, Replay immersif
    """
    
    def generate_agora_manifest(
        self,
        leaderboard: List[LeaderboardEntry],
    ) -> Dict[str, Any]:
        """
        Generate Agora des stratégies visualization.
        
        Per spec: Agora des stratégies
        """
        return {
            "type": "xr_agora",
            "schema_version": "1.0",
            "environment": "strategy_agora",
            "entries": [
                {
                    "position": self._calculate_position(e.rank, len(leaderboard)),
                    "anonymous_id": e.anonymous_id,
                    "score": e.score,
                    "badge": e.badge,
                    "glow_color": self._badge_to_color(e.badge),
                }
                for e in leaderboard[:20]  # Top 20 in agora
            ],
            "assets": ["pedestal_3d", "badge_display", "score_particles"],
        }
    
    def generate_replay_manifest(
        self,
        player_id: str,
        actions: List[Dict],
        results: List[Dict],
    ) -> Dict[str, Any]:
        """
        Generate immersive replay visualization.
        
        Per spec: Replay immersif
        """
        return {
            "type": "xr_replay",
            "schema_version": "1.0",
            "player_id_anonymous": anonymize_id(player_id),
            "timeline": [
                {
                    "timestamp": i,
                    "action": action,
                    "result": results[i] if i < len(results) else {},
                    "visualization": "causal_chain_3d",
                }
                for i, action in enumerate(actions)
            ],
            "controls": {
                "playback_speed": [0.5, 1.0, 2.0],
                "pause_on_divergence": True,
                "highlight_causal_links": True,
            },
        }
    
    def _calculate_position(self, rank: int, total: int) -> Dict[str, float]:
        """Calculate 3D position in agora"""
        import math
        
        # Circular arrangement with height based on rank
        angle = (rank / min(total, 20)) * 2 * math.pi
        radius = 5 + (rank - 1) * 0.5
        
        return {
            "x": math.cos(angle) * radius,
            "y": 2.0 - (rank - 1) * 0.1,  # Higher ranks = higher position
            "z": math.sin(angle) * radius,
        }
    
    def _badge_to_color(self, badge: str) -> str:
        """Get color for badge"""
        colors = {
            "platinum": "#E5E4E2",
            "gold": "#FFD700",
            "silver": "#C0C0C0",
            "bronze": "#CD7F32",
            "none": "#808080",
        }
        return colors.get(badge, "#808080")


# ============================================================================
# TRUST SCORE SYSTEM (MAIN)
# ============================================================================

class TrustScoreSystem:
    """
    Main trust score and leaderboard system.
    """
    
    def __init__(self):
        self.calculator = TrustScoreCalculator()
        self.leaderboard = LeaderboardManager(self.calculator)
        self.badges = BadgeIssuer()
        self.xr = XRVisualization()
    
    def record_game_session(
        self,
        player_id: str,
        actions: List[GameAction],
        results: List[SimulationResult],
        opa_violations: int = 0,
    ) -> Tuple[TrustScore, List[TrustBadge]]:
        """Record a game session and update scores"""
        # Update score
        score = self.calculator.update_score(
            player_id,
            actions,
            results,
            opa_violations,
        )
        
        # Check for new badges
        new_badges = self.badges.check_and_issue(score)
        
        # Refresh leaderboard
        self.leaderboard.refresh()
        
        return score, new_badges
    
    def get_player_profile(self, player_id: str) -> Dict[str, Any]:
        """Get complete player profile"""
        score = self.calculator.get_score(player_id)
        rank_entry = self.leaderboard.get_player_rank(player_id)
        badges = self.badges.get_player_badges(player_id)
        
        return {
            "player_id_anonymous": anonymize_id(player_id),
            "score": {
                "overall": score.overall_score if score else 0,
                "conformity": score.conformity_score if score else 0,
                "resilience": score.resilience_score if score else 0,
                "precision": score.precision_score if score else 0,
                "decision_count": score.decision_count if score else 0,
            } if score else None,
            "rank": rank_entry.rank if rank_entry else None,
            "badges": [
                {"level": b.level, "category": b.category}
                for b in badges
            ],
        }
    
    def get_leaderboard(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard"""
        entries = self.leaderboard.get_top(top_n)
        return [
            {
                "rank": e.rank,
                "anonymous_id": e.anonymous_id,
                "score": e.score,
                "badge": e.badge,
            }
            for e in entries
        ]
    
    def get_agora_xr(self) -> Dict[str, Any]:
        """Get XR agora visualization"""
        return self.xr.generate_agora_manifest(self.leaderboard._entries)


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_trust_system() -> TrustScoreSystem:
    """Create trust score system"""
    return TrustScoreSystem()
