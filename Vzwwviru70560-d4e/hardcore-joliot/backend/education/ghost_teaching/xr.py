"""
============================================================================
CHE·NU™ V69 — EDUCATION GHOST TEACHING XR
============================================================================
Spec: GPT1/CHE-NU_EDU_GHOST_TEACHING_XR.md

Objective: Transform complex procedures into kinesthetic learning (learning by doing)
with proof and safety.

Concepts (per spec):
- Ghost Overlay: phantom hands/tools, ideal trajectory
- Shadow Replay: play back validated execution
- Safety Bubble: prevent validation if safety conditions not met

Pipeline:
1. Capture validated run
2. Normalization
3. XR Playback (ghost)
4. Live scoring (trajectory, time, step order)
5. Validation artifact (proof)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import math

from ..models import (
    GhostTrack,
    InteractionEvent,
    GhostTeachingSession,
    SkillCategory,
    generate_id,
    compute_hash,
    sign_artifact,
)

logger = logging.getLogger(__name__)


# ============================================================================
# GHOST TRACK RECORDER
# ============================================================================

class GhostTrackRecorder:
    """
    Record ghost tracks from expert runs.
    
    Per spec pipeline step 1: Capture d'un run validé
    """
    
    def __init__(self):
        self._recordings: Dict[str, GhostTrack] = {}
        self._current_recording: Optional[GhostTrack] = None
    
    def start_recording(self, skill_id: str) -> str:
        """Start recording a new track"""
        track = GhostTrack(
            track_id=generate_id(),
            skill_id=skill_id,
        )
        self._current_recording = track
        logger.info(f"Started recording track {track.track_id} for skill {skill_id}")
        return track.track_id
    
    def record_frame(
        self,
        position: Dict[str, float],
        rotation: Dict[str, float],
        tool_state: Dict[str, Any] = None,
    ) -> None:
        """Record a single frame"""
        if not self._current_recording:
            return
        
        self._current_recording.positions.append(position)
        self._current_recording.rotations.append(rotation)
        self._current_recording.tool_states.append(tool_state or {})
    
    def record_event(
        self,
        event_type: str,
        position: Dict[str, float] = None,
        data: Dict[str, Any] = None,
    ) -> None:
        """Record an interaction event"""
        if not self._current_recording:
            return
        
        event = InteractionEvent(
            event_id=generate_id(),
            event_type=event_type,
            timestamp_ms=len(self._current_recording.positions) * (1000 // 60),
            position=position or {},
            data=data or {},
        )
        
        self._current_recording.event_markers.append({
            "event_id": event.event_id,
            "type": event.event_type,
            "timestamp_ms": event.timestamp_ms,
            "position": event.position,
            "data": event.data,
        })
    
    def stop_recording(self) -> Optional[GhostTrack]:
        """Stop recording and finalize track"""
        if not self._current_recording:
            return None
        
        track = self._current_recording
        
        # Calculate duration
        track.duration_seconds = len(track.positions) / track.frame_rate
        
        # Compute hash
        track.track_hash = compute_hash({
            "positions": track.positions,
            "rotations": track.rotations,
            "events": track.event_markers,
        })
        
        self._recordings[track.track_id] = track
        self._current_recording = None
        
        logger.info(f"Finished recording track {track.track_id}: {track.duration_seconds:.1f}s")
        return track
    
    def validate_as_gold(
        self,
        track_id: str,
        validator_id: str,
    ) -> bool:
        """Mark track as gold run"""
        track = self._recordings.get(track_id)
        if not track:
            return False
        
        track.is_gold_run = True
        track.validated_by = validator_id
        
        logger.info(f"Track {track_id} validated as gold run by {validator_id}")
        return True
    
    def get_track(self, track_id: str) -> Optional[GhostTrack]:
        """Get track by ID"""
        return self._recordings.get(track_id)
    
    def get_gold_tracks(self, skill_id: str) -> List[GhostTrack]:
        """Get all gold tracks for a skill"""
        return [
            t for t in self._recordings.values()
            if t.skill_id == skill_id and t.is_gold_run
        ]


# ============================================================================
# TRACK NORMALIZER
# ============================================================================

class TrackNormalizer:
    """
    Normalize tracks for comparison.
    
    Per spec pipeline step 2: Normalisation (unités, référentiels, calibration)
    """
    
    def normalize(self, track: GhostTrack) -> GhostTrack:
        """Normalize a track"""
        if not track.positions:
            return track
        
        # Find bounds
        min_pos = {"x": float("inf"), "y": float("inf"), "z": float("inf")}
        max_pos = {"x": float("-inf"), "y": float("-inf"), "z": float("-inf")}
        
        for pos in track.positions:
            for axis in ["x", "y", "z"]:
                if axis in pos:
                    min_pos[axis] = min(min_pos[axis], pos[axis])
                    max_pos[axis] = max(max_pos[axis], pos[axis])
        
        # Normalize to [0, 1] range
        normalized_positions = []
        for pos in track.positions:
            norm_pos = {}
            for axis in ["x", "y", "z"]:
                if axis in pos:
                    range_val = max_pos[axis] - min_pos[axis]
                    if range_val > 0:
                        norm_pos[axis] = (pos[axis] - min_pos[axis]) / range_val
                    else:
                        norm_pos[axis] = 0.5
            normalized_positions.append(norm_pos)
        
        track.positions = normalized_positions
        return track


# ============================================================================
# SAFETY BUBBLE
# ============================================================================

@dataclass
class SafetyCondition:
    """A safety condition that must be met"""
    condition_id: str
    name: str
    check_type: str  # equipment, environment, prerequisite
    required_value: Any = True
    current_value: Any = None
    
    @property
    def is_met(self) -> bool:
        return self.current_value == self.required_value


class SafetyBubble:
    """
    Safety zone that prevents validation if conditions not met.
    
    Per spec: zone XR qui empêche de valider une action si conditions
    de sécurité non satisfaites
    """
    
    def __init__(self):
        self._conditions: Dict[str, List[SafetyCondition]] = {}  # skill_id → conditions
    
    def add_condition(
        self,
        skill_id: str,
        name: str,
        check_type: str,
        required_value: Any = True,
    ) -> SafetyCondition:
        """Add a safety condition for a skill"""
        if skill_id not in self._conditions:
            self._conditions[skill_id] = []
        
        condition = SafetyCondition(
            condition_id=generate_id(),
            name=name,
            check_type=check_type,
            required_value=required_value,
        )
        
        self._conditions[skill_id].append(condition)
        return condition
    
    def check_conditions(
        self,
        skill_id: str,
        current_state: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """
        Check all safety conditions.
        
        Returns (all_met, list of unmet condition names)
        """
        conditions = self._conditions.get(skill_id, [])
        unmet = []
        
        for cond in conditions:
            cond.current_value = current_state.get(cond.name)
            if not cond.is_met:
                unmet.append(cond.name)
        
        return len(unmet) == 0, unmet
    
    def get_conditions(self, skill_id: str) -> List[SafetyCondition]:
        """Get safety conditions for a skill"""
        return self._conditions.get(skill_id, [])


# ============================================================================
# SCORING ENGINE
# ============================================================================

class ScoringEngine:
    """
    Score learner performance against gold track.
    
    Per spec pipeline step 4: Scoring en live (écart trajectoire, temps, ordre des étapes)
    """
    
    def __init__(
        self,
        trajectory_weight: float = 0.4,
        timing_weight: float = 0.3,
        order_weight: float = 0.3,
    ):
        self.trajectory_weight = trajectory_weight
        self.timing_weight = timing_weight
        self.order_weight = order_weight
    
    def score_trajectory(
        self,
        gold_positions: List[Dict[str, float]],
        learner_positions: List[Dict[str, float]],
    ) -> float:
        """Score trajectory similarity"""
        if not gold_positions or not learner_positions:
            return 0.0
        
        # Resample to same length
        min_len = min(len(gold_positions), len(learner_positions))
        
        total_distance = 0.0
        for i in range(min_len):
            gold = gold_positions[i]
            learner = learner_positions[i]
            
            # Euclidean distance
            dist = math.sqrt(
                (gold.get("x", 0) - learner.get("x", 0)) ** 2 +
                (gold.get("y", 0) - learner.get("y", 0)) ** 2 +
                (gold.get("z", 0) - learner.get("z", 0)) ** 2
            )
            total_distance += dist
        
        avg_distance = total_distance / min_len
        
        # Convert to score (closer = higher)
        # Assuming normalized positions, max distance ~ sqrt(3) ≈ 1.73
        score = max(0, 1 - avg_distance / 1.73)
        return score
    
    def score_timing(
        self,
        gold_duration: float,
        learner_duration: float,
        tolerance: float = 0.2,
    ) -> float:
        """Score timing similarity"""
        if gold_duration == 0:
            return 0.0
        
        ratio = learner_duration / gold_duration
        
        # Perfect if within tolerance of 1.0
        if 1 - tolerance <= ratio <= 1 + tolerance:
            return 1.0
        
        # Score decreases with deviation
        deviation = abs(ratio - 1.0)
        return max(0, 1 - deviation)
    
    def score_order(
        self,
        gold_events: List[Dict],
        learner_events: List[Dict],
    ) -> float:
        """Score event order similarity"""
        if not gold_events:
            return 1.0 if not learner_events else 0.0
        
        # Extract event types
        gold_types = [e.get("type") for e in gold_events]
        learner_types = [e.get("type") for e in learner_events]
        
        # Count matching sequence
        matches = 0
        for i, gt in enumerate(gold_types):
            if i < len(learner_types) and learner_types[i] == gt:
                matches += 1
        
        return matches / len(gold_types) if gold_types else 0.0
    
    def calculate_overall(
        self,
        trajectory_score: float,
        timing_score: float,
        order_score: float,
    ) -> float:
        """Calculate overall score"""
        return (
            trajectory_score * self.trajectory_weight +
            timing_score * self.timing_weight +
            order_score * self.order_weight
        )


# ============================================================================
# GHOST TEACHING ENGINE
# ============================================================================

class GhostTeachingEngine:
    """
    Main Ghost Teaching XR engine.
    """
    
    def __init__(self):
        self.recorder = GhostTrackRecorder()
        self.normalizer = TrackNormalizer()
        self.safety = SafetyBubble()
        self.scorer = ScoringEngine()
        
        # Sessions
        self._sessions: Dict[str, GhostTeachingSession] = {}
        
        # Artifacts
        self._artifacts: Dict[str, Dict] = {}
    
    def get_gold_track(self, skill_id: str) -> Optional[GhostTrack]:
        """Get a gold track for a skill"""
        tracks = self.recorder.get_gold_tracks(skill_id)
        return tracks[0] if tracks else None
    
    def start_session(
        self,
        user_id: str,
        skill_id: str,
        mode: str = "guided",
    ) -> Optional[GhostTeachingSession]:
        """
        Start a ghost teaching session.
        
        Per spec modes: guided, practice, exam
        """
        gold_track = self.get_gold_track(skill_id)
        if not gold_track:
            logger.warning(f"No gold track available for skill {skill_id}")
            return None
        
        session = GhostTeachingSession(
            session_id=generate_id(),
            user_id=user_id,
            skill_id=skill_id,
            track_id=gold_track.track_id,
            mode=mode,
        )
        
        self._sessions[session.session_id] = session
        logger.info(f"Started ghost teaching session {session.session_id} in {mode} mode")
        return session
    
    def check_safety(
        self,
        session_id: str,
        current_state: Dict[str, Any],
    ) -> Tuple[bool, List[str]]:
        """Check safety conditions for session"""
        session = self._sessions.get(session_id)
        if not session:
            return False, ["session_not_found"]
        
        return self.safety.check_conditions(session.skill_id, current_state)
    
    def score_session(
        self,
        session_id: str,
        learner_positions: List[Dict[str, float]],
        learner_events: List[Dict],
        learner_duration: float,
    ) -> GhostTeachingSession:
        """Score a session against gold track"""
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        gold_track = self.recorder.get_track(session.track_id)
        if not gold_track:
            raise ValueError(f"Gold track {session.track_id} not found")
        
        # Score components
        session.trajectory_score = self.scorer.score_trajectory(
            gold_track.positions,
            learner_positions,
        )
        
        session.timing_score = self.scorer.score_timing(
            gold_track.duration_seconds,
            learner_duration,
        )
        
        session.order_score = self.scorer.score_order(
            gold_track.event_markers,
            learner_events,
        )
        
        session.overall_score = self.scorer.calculate_overall(
            session.trajectory_score,
            session.timing_score,
            session.order_score,
        )
        
        # Determine pass/fail
        session.passed = session.overall_score >= 0.7
        session.completed = True
        
        logger.info(
            f"Session {session_id} scored: "
            f"trajectory={session.trajectory_score:.2f}, "
            f"timing={session.timing_score:.2f}, "
            f"order={session.order_score:.2f}, "
            f"overall={session.overall_score:.2f}, "
            f"passed={session.passed}"
        )
        
        return session
    
    def generate_artifact(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """
        Generate validation artifact.
        
        Per spec pipeline step 5: Artifact de validation (preuve)
        """
        session = self._sessions.get(session_id)
        if not session or not session.completed:
            return {}
        
        artifact = {
            "type": "GHOST_TEACHING_VALIDATION",
            "schema_version": "1.0",
            "session_id": session.session_id,
            "user_id": session.user_id,
            "skill_id": session.skill_id,
            "gold_track_id": session.track_id,
            "mode": session.mode,
            "scores": {
                "trajectory": session.trajectory_score,
                "timing": session.timing_score,
                "order": session.order_score,
                "overall": session.overall_score,
            },
            "passed": session.passed,
            "completed_at": datetime.utcnow().isoformat(),
        }
        
        # Sign artifact
        artifact["signature"] = sign_artifact(artifact, "ghost_teaching_engine")
        
        self._artifacts[session_id] = artifact
        return artifact
    
    def export_for_xr(
        self,
        track_id: str,
        playback_speed: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Export track for XR playback.
        
        Per spec: Shadow Replay - vitesse variable (0.25×, 1×, 2×)
        """
        track = self.recorder.get_track(track_id)
        if not track:
            return {}
        
        return {
            "type": "ghost_track_xr",
            "track_id": track.track_id,
            "skill_id": track.skill_id,
            "positions": track.positions,
            "rotations": track.rotations,
            "tool_states": track.tool_states,
            "event_markers": track.event_markers,
            "duration_seconds": track.duration_seconds,
            "frame_rate": track.frame_rate,
            "playback_speed": playback_speed,
            "is_gold_run": track.is_gold_run,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_ghost_teaching_engine() -> GhostTeachingEngine:
    """Create ghost teaching engine"""
    return GhostTeachingEngine()


def create_recorder() -> GhostTrackRecorder:
    """Create ghost track recorder"""
    return GhostTrackRecorder()


def create_safety_bubble() -> SafetyBubble:
    """Create safety bubble"""
    return SafetyBubble()
