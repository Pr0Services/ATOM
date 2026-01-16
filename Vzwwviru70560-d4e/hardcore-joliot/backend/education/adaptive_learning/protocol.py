"""
============================================================================
CHE·NU™ V69 — EDUCATION ADAPTIVE LEARNING PROTOCOL
============================================================================
Spec: GPT1/CHE-NU_EDU_ADAPTIVE_LEARNING_PROTOCOL.md

Objective: Personalize learning (format, pace, difficulty) with measurable,
governed, and auditable logic.

Principles (per spec):
1. Just-in-Time: learn only what is useful
2. Evidence-Based: adapt on observable signals
3. Safe-by-Design: if high risk → simulation + HITL
4. Audit Trail: each adaptation must be justifiable

State Machine: Onboarding → Baseline Test → Learning Loop → Assessment → Certification
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    Skill,
    SkillCategory,
    LearnerProfile,
    LearnerPreference,
    PerformanceMetrics,
    AdaptationDecision,
    LearningFormat,
    DifficultyLevel,
    generate_id,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# LEARNING STATES
# ============================================================================

class LearningState:
    """Learning state machine states"""
    ONBOARDING = "onboarding"
    BASELINE_TEST = "baseline_test"
    LEARNING_LOOP = "learning_loop"
    ASSESSMENT = "assessment"
    CERTIFICATION = "certification"
    COMPLETED = "completed"


# ============================================================================
# SIGNAL ANALYZER
# ============================================================================

class SignalAnalyzer:
    """
    Analyze learner signals for adaptation.
    
    Per spec: Signaux d'adaptation (Inputs)
    """
    
    def __init__(self):
        # Thresholds for adaptation
        self.success_threshold_up = 0.85  # Increase difficulty
        self.success_threshold_down = 0.30  # Decrease difficulty
        self.repeated_error_threshold = 2
    
    def analyze_performance(
        self,
        metrics: PerformanceMetrics,
    ) -> Dict[str, Any]:
        """Analyze performance metrics"""
        signals = {
            "should_increase_difficulty": False,
            "should_decrease_difficulty": False,
            "struggling_areas": [],
            "strength_areas": [],
        }
        
        # Success rate analysis
        if metrics.quiz_success_rate >= self.success_threshold_up:
            signals["should_increase_difficulty"] = True
            signals["strength_areas"].append("quiz_performance")
        
        if metrics.quiz_success_rate <= self.success_threshold_down:
            signals["should_decrease_difficulty"] = True
        
        # Error pattern analysis
        if metrics.repeated_errors >= self.repeated_error_threshold:
            signals["should_decrease_difficulty"] = True
            
            # Find problem areas
            for error_type, count in metrics.error_types.items():
                if count >= 2:
                    signals["struggling_areas"].append(error_type)
        
        return signals
    
    def analyze_profile(
        self,
        profile: LearnerProfile,
        skill: Skill,
    ) -> Dict[str, Any]:
        """Analyze learner profile for format selection"""
        recommendations = {
            "recommended_format": LearningFormat.TEXT,
            "use_xr": False,
            "needs_hitl": False,
        }
        
        # XR recommendation
        if (
            profile.has_xr_device and
            skill.category in [SkillCategory.CATEGORY_B, SkillCategory.CATEGORY_C] and
            LearningFormat.XR in skill.formats_available
        ):
            recommendations["recommended_format"] = LearningFormat.XR
            recommendations["use_xr"] = True
        
        # Format based on preference
        elif profile.preferred_format == LearnerPreference.VISUAL:
            recommendations["recommended_format"] = LearningFormat.VIDEO
        elif profile.preferred_format == LearnerPreference.AUDITORY:
            recommendations["recommended_format"] = LearningFormat.AUDIO
        elif profile.preferred_format == LearnerPreference.KINESTHETIC:
            recommendations["recommended_format"] = LearningFormat.INTERACTIVE
        
        # HITL for high-risk
        if skill.category == SkillCategory.CATEGORY_C:
            recommendations["needs_hitl"] = True
        
        return recommendations


# ============================================================================
# DIFFICULTY ADAPTER
# ============================================================================

class DifficultyAdapter:
    """
    Adapt difficulty based on performance.
    
    Per spec algorithm:
    - difficulty ↑ if success > 85% on 2 cycles
    - difficulty ↓ if failure > 30% and same error repeated
    """
    
    LEVELS = [
        DifficultyLevel.BEGINNER,
        DifficultyLevel.INTERMEDIATE,
        DifficultyLevel.ADVANCED,
        DifficultyLevel.EXPERT,
    ]
    
    def __init__(self):
        self._user_levels: Dict[str, Dict[str, int]] = {}  # user_id → {skill_id: level_idx}
        self._success_streaks: Dict[str, int] = {}  # user_id:skill_id → streak
    
    def get_current_level(
        self,
        user_id: str,
        skill_id: str,
    ) -> DifficultyLevel:
        """Get current difficulty level"""
        if user_id not in self._user_levels:
            self._user_levels[user_id] = {}
        
        idx = self._user_levels[user_id].get(skill_id, 0)
        return self.LEVELS[idx]
    
    def adapt(
        self,
        user_id: str,
        skill_id: str,
        success_rate: float,
        repeated_errors: int,
    ) -> Tuple[DifficultyLevel, str]:
        """
        Adapt difficulty and return (new_level, reason)
        """
        key = f"{user_id}:{skill_id}"
        
        if user_id not in self._user_levels:
            self._user_levels[user_id] = {}
        
        current_idx = self._user_levels[user_id].get(skill_id, 0)
        new_idx = current_idx
        reason = "no_change"
        
        # Track success streak
        if success_rate >= 0.85:
            self._success_streaks[key] = self._success_streaks.get(key, 0) + 1
        else:
            self._success_streaks[key] = 0
        
        # Increase difficulty
        if self._success_streaks.get(key, 0) >= 2:
            if current_idx < len(self.LEVELS) - 1:
                new_idx = current_idx + 1
                reason = "success_streak_2_cycles"
                self._success_streaks[key] = 0
        
        # Decrease difficulty
        elif success_rate <= 0.30 and repeated_errors >= 2:
            if current_idx > 0:
                new_idx = current_idx - 1
                reason = "high_failure_repeated_errors"
        
        self._user_levels[user_id][skill_id] = new_idx
        return self.LEVELS[new_idx], reason


# ============================================================================
# LEARNING LOOP
# ============================================================================

@dataclass
class LearningLoopStep:
    """
    A step in the learning loop.
    
    Per spec Learning Loop:
    1) mini-explanation
    2) demonstration (video/XR/diagram)
    3) guided exercise
    4) free exercise
    5) micro-quiz
    6) correction + "why" (causal explanation)
    """
    step_id: str
    step_type: str  # explanation, demonstration, guided, free, quiz, correction
    content_ref: str = ""
    completed: bool = False
    score: Optional[float] = None


class LearningLoopManager:
    """
    Manage the learning loop for a skill.
    """
    
    STEP_TYPES = [
        "explanation",
        "demonstration",
        "guided_exercise",
        "free_exercise",
        "micro_quiz",
        "correction",
    ]
    
    def __init__(self):
        self._loops: Dict[str, List[LearningLoopStep]] = {}  # user:skill → steps
    
    def create_loop(
        self,
        user_id: str,
        skill_id: str,
    ) -> List[LearningLoopStep]:
        """Create a learning loop for user/skill"""
        key = f"{user_id}:{skill_id}"
        
        steps = []
        for i, step_type in enumerate(self.STEP_TYPES):
            step = LearningLoopStep(
                step_id=f"{key}_{i}",
                step_type=step_type,
                content_ref=f"content://{skill_id}/{step_type}",
            )
            steps.append(step)
        
        self._loops[key] = steps
        return steps
    
    def get_current_step(
        self,
        user_id: str,
        skill_id: str,
    ) -> Optional[LearningLoopStep]:
        """Get current (incomplete) step"""
        key = f"{user_id}:{skill_id}"
        steps = self._loops.get(key, [])
        
        for step in steps:
            if not step.completed:
                return step
        
        return None
    
    def complete_step(
        self,
        user_id: str,
        skill_id: str,
        step_id: str,
        score: float = None,
    ) -> bool:
        """Mark step as completed"""
        key = f"{user_id}:{skill_id}"
        steps = self._loops.get(key, [])
        
        for step in steps:
            if step.step_id == step_id:
                step.completed = True
                step.score = score
                return True
        
        return False
    
    def is_loop_complete(
        self,
        user_id: str,
        skill_id: str,
    ) -> bool:
        """Check if loop is complete"""
        key = f"{user_id}:{skill_id}"
        steps = self._loops.get(key, [])
        return all(s.completed for s in steps)


# ============================================================================
# ADAPTIVE LEARNING PROTOCOL
# ============================================================================

class AdaptiveLearningProtocol:
    """
    Main adaptive learning protocol.
    
    Per spec: personnaliser l'apprentissage avec logique mesurable, gouvernée, auditable
    """
    
    def __init__(self):
        self.signal_analyzer = SignalAnalyzer()
        self.difficulty_adapter = DifficultyAdapter()
        self.loop_manager = LearningLoopManager()
        
        # User states
        self._user_states: Dict[str, Dict[str, str]] = {}  # user_id → {skill_id: state}
        self._user_profiles: Dict[str, LearnerProfile] = {}
        self._user_metrics: Dict[str, Dict[str, PerformanceMetrics]] = {}
        
        # Decisions (audit trail)
        self._decisions: List[AdaptationDecision] = []
    
    def set_profile(self, profile: LearnerProfile) -> None:
        """Set learner profile"""
        self._user_profiles[profile.user_id] = profile
    
    def get_profile(self, user_id: str) -> Optional[LearnerProfile]:
        """Get learner profile"""
        return self._user_profiles.get(user_id)
    
    def start_learning(
        self,
        user_id: str,
        skill_id: str,
    ) -> str:
        """Start learning a skill (enter state machine)"""
        if user_id not in self._user_states:
            self._user_states[user_id] = {}
        
        self._user_states[user_id][skill_id] = LearningState.ONBOARDING
        
        # Initialize metrics
        if user_id not in self._user_metrics:
            self._user_metrics[user_id] = {}
        
        self._user_metrics[user_id][skill_id] = PerformanceMetrics(
            user_id=user_id,
            skill_id=skill_id,
        )
        
        logger.info(f"User {user_id} started learning skill {skill_id}")
        return LearningState.ONBOARDING
    
    def evaluate(
        self,
        user_id: str,
        skill_id: str,
        skill: Skill,
    ) -> Dict[str, Any]:
        """
        Evaluate current state and recommend adaptations.
        
        Per spec API: POST /edu/adapt/evaluate
        """
        profile = self._user_profiles.get(user_id)
        metrics = self._user_metrics.get(user_id, {}).get(skill_id)
        
        evaluation = {
            "user_id": user_id,
            "skill_id": skill_id,
            "current_state": self._user_states.get(user_id, {}).get(skill_id),
            "recommendations": {},
        }
        
        # Analyze profile
        if profile:
            profile_signals = self.signal_analyzer.analyze_profile(profile, skill)
            evaluation["recommendations"]["format"] = profile_signals["recommended_format"]
            evaluation["recommendations"]["use_xr"] = profile_signals["use_xr"]
            evaluation["recommendations"]["needs_hitl"] = profile_signals["needs_hitl"]
        
        # Analyze performance
        if metrics:
            perf_signals = self.signal_analyzer.analyze_performance(metrics)
            evaluation["performance_signals"] = perf_signals
            
            # Get difficulty recommendation
            level, reason = self.difficulty_adapter.adapt(
                user_id, skill_id,
                metrics.quiz_success_rate,
                metrics.repeated_errors,
            )
            evaluation["recommendations"]["difficulty"] = level
            evaluation["recommendations"]["difficulty_reason"] = reason
        
        return evaluation
    
    def get_next_unit(
        self,
        user_id: str,
        skill_id: str,
        skill: Skill,
    ) -> Dict[str, Any]:
        """
        Get next learning unit.
        
        Per spec API: POST /edu/adapt/next_unit
        """
        state = self._user_states.get(user_id, {}).get(skill_id, LearningState.ONBOARDING)
        
        # State transitions
        if state == LearningState.ONBOARDING:
            # Move to baseline test
            self._user_states[user_id][skill_id] = LearningState.BASELINE_TEST
            return {
                "unit_type": "baseline_test",
                "content_ref": f"test://{skill_id}/baseline",
            }
        
        elif state == LearningState.BASELINE_TEST:
            # Move to learning loop
            self._user_states[user_id][skill_id] = LearningState.LEARNING_LOOP
            self.loop_manager.create_loop(user_id, skill_id)
        
        if state == LearningState.LEARNING_LOOP or state == LearningState.BASELINE_TEST:
            # Get next step in loop
            step = self.loop_manager.get_current_step(user_id, skill_id)
            
            if step:
                # Apply adaptations
                profile = self._user_profiles.get(user_id)
                format_rec = LearningFormat.TEXT
                
                if profile:
                    signals = self.signal_analyzer.analyze_profile(profile, skill)
                    format_rec = signals["recommended_format"]
                
                return {
                    "unit_type": step.step_type,
                    "step_id": step.step_id,
                    "content_ref": step.content_ref,
                    "format": format_rec,
                    "difficulty": self.difficulty_adapter.get_current_level(user_id, skill_id),
                }
            else:
                # Loop complete, move to assessment
                self._user_states[user_id][skill_id] = LearningState.ASSESSMENT
        
        if state == LearningState.ASSESSMENT:
            return {
                "unit_type": "final_assessment",
                "content_ref": f"assessment://{skill_id}/final",
            }
        
        return {"unit_type": "completed", "message": "Learning complete"}
    
    def log_decision(
        self,
        user_id: str,
        skill_id: str,
        new_format: LearningFormat,
        new_difficulty: DifficultyLevel,
        signals_used: List[str],
        justification: str,
    ) -> AdaptationDecision:
        """
        Log an adaptation decision.
        
        Per spec API: POST /edu/adapt/log_decision
        Per spec: Audit Trail - each adaptation must be justifiable
        """
        decision = AdaptationDecision(
            decision_id=generate_id(),
            skill_id=skill_id,
            user_id=user_id,
            new_format=new_format,
            new_difficulty=new_difficulty,
            signals_used=signals_used,
            justification=justification,
        )
        
        # Sign for audit trail
        decision.signature = sign_artifact({
            "decision_id": decision.decision_id,
            "skill_id": skill_id,
            "user_id": user_id,
            "format": new_format.value,
            "difficulty": new_difficulty.value,
            "justification": justification,
        }, "adaptive_learning_protocol")
        
        self._decisions.append(decision)
        
        logger.info(
            f"Logged adaptation decision {decision.decision_id}: "
            f"format={new_format.value}, difficulty={new_difficulty.value}"
        )
        
        return decision
    
    def update_metrics(
        self,
        user_id: str,
        skill_id: str,
        quiz_passed: bool = None,
        error_type: str = None,
        time_spent_seconds: float = None,
    ) -> None:
        """Update performance metrics"""
        if user_id not in self._user_metrics:
            self._user_metrics[user_id] = {}
        
        if skill_id not in self._user_metrics[user_id]:
            self._user_metrics[user_id][skill_id] = PerformanceMetrics(
                user_id=user_id,
                skill_id=skill_id,
            )
        
        metrics = self._user_metrics[user_id][skill_id]
        
        if quiz_passed is not None:
            # Update success rate (rolling average)
            current = metrics.quiz_success_rate
            metrics.quiz_success_rate = (current + (1.0 if quiz_passed else 0.0)) / 2
        
        if error_type:
            metrics.error_count += 1
            if error_type not in metrics.error_types:
                metrics.error_types[error_type] = 0
            else:
                # Repeated error
                metrics.repeated_errors += 1
            metrics.error_types[error_type] += 1
        
        if time_spent_seconds:
            current = metrics.avg_time_per_step_seconds
            metrics.avg_time_per_step_seconds = (current + time_spent_seconds) / 2
    
    def get_audit_trail(
        self,
        user_id: str = None,
        skill_id: str = None,
    ) -> List[AdaptationDecision]:
        """Get audit trail of decisions"""
        results = self._decisions
        
        if user_id:
            results = [d for d in results if d.user_id == user_id]
        
        if skill_id:
            results = [d for d in results if d.skill_id == skill_id]
        
        return results


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_protocol() -> AdaptiveLearningProtocol:
    """Create adaptive learning protocol"""
    return AdaptiveLearningProtocol()


def create_learner_profile(
    user_id: str,
    available_time_minutes: int = 30,
    has_xr: bool = False,
    preference: LearnerPreference = LearnerPreference.VISUAL,
) -> LearnerProfile:
    """Create a learner profile"""
    return LearnerProfile(
        user_id=user_id,
        available_time_minutes=available_time_minutes,
        has_xr_device=has_xr,
        preferred_format=preference,
    )
