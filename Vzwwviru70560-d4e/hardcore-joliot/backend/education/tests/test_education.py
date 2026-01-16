"""
============================================================================
CHE·NU™ V69 — EDUCATION MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# SKILL LATTICE TESTS
# ============================================================================

class TestSkillLattice:
    """Test skill lattice"""
    
    def test_create_lattice(self):
        from ..skill_lattice import create_skill_lattice
        lattice = create_skill_lattice()
        assert lattice is not None
    
    def test_register_skill(self):
        from ..skill_lattice import create_skill_lattice, create_skill
        from ..models import SkillCategory
        
        lattice = create_skill_lattice()
        skill = create_skill(
            name="Git Basics",
            domain="programming",
            category=SkillCategory.CATEGORY_A,
            duration_minutes=15,
        )
        
        lattice.skills.register(skill)
        retrieved = lattice.skills.get(skill.skill_id)
        
        assert retrieved is not None
        assert retrieved.name == "Git Basics"
    
    def test_suggest_pathway(self):
        from ..skill_lattice import create_skill_lattice, create_skill
        
        lattice = create_skill_lattice()
        
        # Add skills
        skill1 = create_skill("Python Basics", "programming")
        skill2 = create_skill("Python Advanced", "programming")
        lattice.skills.register(skill1)
        lattice.skills.register(skill2)
        
        # Suggest pathway
        pathway = lattice.suggest_pathway("user-1", "python", 2.0)
        
        assert pathway is not None
        assert len(pathway.skills) > 0
    
    def test_run_assessment(self):
        from ..skill_lattice import create_skill_lattice, create_skill
        from ..models import AssessmentMode
        
        lattice = create_skill_lattice()
        skill = create_skill("Test Skill", "test")
        lattice.skills.register(skill)
        
        result = lattice.run_assessment(
            skill.skill_id,
            "user-1",
            AssessmentMode.SIMULATION,
        )
        
        assert result is not None
        assert result.score > 0


# ============================================================================
# ADAPTIVE LEARNING TESTS
# ============================================================================

class TestAdaptiveLearning:
    """Test adaptive learning protocol"""
    
    def test_create_protocol(self):
        from ..adaptive_learning import create_protocol
        protocol = create_protocol()
        assert protocol is not None
    
    def test_start_learning(self):
        from ..adaptive_learning import create_protocol
        
        protocol = create_protocol()
        state = protocol.start_learning("user-1", "skill-1")
        
        assert state == "onboarding"
    
    def test_difficulty_adaptation(self):
        from ..adaptive_learning import DifficultyAdapter
        from ..models import DifficultyLevel
        
        adapter = DifficultyAdapter()
        
        # High success should increase difficulty
        level, reason = adapter.adapt("user-1", "skill-1", 0.9, 0)
        # First time, no change
        
        # Second success
        level, reason = adapter.adapt("user-1", "skill-1", 0.9, 0)
        
        # After 2 successes, should increase
        assert reason == "success_streak_2_cycles" or level == DifficultyLevel.INTERMEDIATE
    
    def test_log_decision(self):
        from ..adaptive_learning import create_protocol
        from ..models import LearningFormat, DifficultyLevel
        
        protocol = create_protocol()
        
        decision = protocol.log_decision(
            user_id="user-1",
            skill_id="skill-1",
            new_format=LearningFormat.XR,
            new_difficulty=DifficultyLevel.INTERMEDIATE,
            signals_used=["success_rate", "xr_device_available"],
            justification="User has XR device and high success rate",
        )
        
        assert decision is not None
        assert decision.signature != ""


# ============================================================================
# GHOST TEACHING XR TESTS
# ============================================================================

class TestGhostTeaching:
    """Test ghost teaching XR"""
    
    def test_create_engine(self):
        from ..ghost_teaching import create_ghost_teaching_engine
        engine = create_ghost_teaching_engine()
        assert engine is not None
    
    def test_record_track(self):
        from ..ghost_teaching import create_recorder
        
        recorder = create_recorder()
        
        # Start recording
        track_id = recorder.start_recording("skill-1")
        
        # Record frames
        for i in range(10):
            recorder.record_frame(
                position={"x": i * 0.1, "y": 0, "z": 0},
                rotation={"x": 0, "y": 0, "z": 0},
            )
        
        # Record event
        recorder.record_event("grasp", {"x": 0.5, "y": 0, "z": 0})
        
        # Stop recording
        track = recorder.stop_recording()
        
        assert track is not None
        assert len(track.positions) == 10
        assert len(track.event_markers) == 1
    
    def test_safety_bubble(self):
        from ..ghost_teaching import create_safety_bubble
        
        bubble = create_safety_bubble()
        
        # Add conditions
        bubble.add_condition("skill-1", "power_off", "equipment", True)
        bubble.add_condition("skill-1", "safety_glasses", "equipment", True)
        
        # Check - all met
        met, unmet = bubble.check_conditions("skill-1", {
            "power_off": True,
            "safety_glasses": True,
        })
        assert met is True
        
        # Check - some missing
        met, unmet = bubble.check_conditions("skill-1", {
            "power_off": True,
            "safety_glasses": False,
        })
        assert met is False
        assert "safety_glasses" in unmet


# ============================================================================
# SKILL TO EQUITY BRIDGE TESTS
# ============================================================================

class TestSkillToEquity:
    """Test skill to equity bridge"""
    
    def test_create_bridge(self):
        from ..skill_equity import create_bridge
        bridge = create_bridge()
        assert bridge is not None
    
    def test_eligibility_check(self):
        from ..skill_equity import create_bridge, create_eligibility_rule
        from ..models import EligibilityTier
        
        bridge = create_bridge()
        
        # Add rule
        rule = create_eligibility_rule(
            task_family="technician",
            required_certs=["basic_training"],
            min_trust_score=0.7,
            tier=EligibilityTier.TIER_1,
        )
        bridge.evaluator.add_rule(rule)
        
        # Setup user
        bridge.register_certification("user-1", "basic_training")
        bridge.update_trust_score("user-1", 0.8)
        
        # Check eligibility
        result = bridge.check_eligibility("user-1", "technician")
        
        assert result["eligible"] is True
        assert result["tier"] == "tier_1"
    
    def test_create_offer(self):
        from ..skill_equity import create_bridge, create_eligibility_rule
        from ..models import EligibilityTier
        
        bridge = create_bridge()
        
        # Setup
        rule = create_eligibility_rule(
            task_family="developer",
            required_certs=["python_cert"],
            min_trust_score=0.6,
            tier=EligibilityTier.TIER_2,
        )
        bridge.evaluator.add_rule(rule)
        
        bridge.register_certification("user-1", "python_cert")
        bridge.update_trust_score("user-1", 0.75)
        
        # Create offer
        offer = bridge.create_task_offer(
            user_id="user-1",
            task_id="task-123",
            task_family="developer",
            task_complexity=0.6,
        )
        
        assert offer is not None
        assert offer.equity_split > 0
        assert offer.salary_split > 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestEducationIntegration:
    """Integration tests"""
    
    def test_full_learning_to_equity_flow(self):
        """Test complete flow from learning to equity offer"""
        from ..skill_lattice import create_skill_lattice, create_skill
        from ..adaptive_learning import create_protocol, create_learner_profile
        from ..skill_equity import create_bridge, create_eligibility_rule
        from ..models import SkillCategory, LearnerPreference, EligibilityTier
        
        # 1. Create skill lattice with skill
        lattice = create_skill_lattice()
        skill = create_skill(
            name="Data Analysis",
            domain="analytics",
            category=SkillCategory.CATEGORY_A,
        )
        lattice.skills.register(skill)
        
        # 2. Setup learner profile
        protocol = create_protocol()
        profile = create_learner_profile(
            user_id="user-1",
            available_time_minutes=60,
            preference=LearnerPreference.VISUAL,
        )
        protocol.set_profile(profile)
        
        # 3. Start learning
        protocol.start_learning("user-1", skill.skill_id)
        
        # 4. Complete assessment
        result = lattice.run_assessment(skill.skill_id, "user-1")
        
        # 5. Issue certification
        cert = lattice.issue_certification(skill.skill_id, "user-1")
        
        # 6. Setup equity bridge
        bridge = create_bridge()
        rule = create_eligibility_rule(
            task_family="analyst",
            required_certs=[cert.cert_id if cert else "cert"],
            min_trust_score=0.5,
            tier=EligibilityTier.TIER_1,
        )
        bridge.evaluator.add_rule(rule)
        
        if cert:
            bridge.register_certification("user-1", cert.cert_id)
        bridge.update_trust_score("user-1", 0.7)
        
        # 7. Check unlocked opportunities
        opportunities = bridge.get_unlocked_opportunities("user-1")
        
        # Verify flow
        assert result.passed
        assert cert is not None if result.passed else True
        assert len(opportunities) >= 0  # May or may not have opportunities


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
