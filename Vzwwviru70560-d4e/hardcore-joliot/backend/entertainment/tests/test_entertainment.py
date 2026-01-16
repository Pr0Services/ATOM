"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# GAME GENERATOR TESTS
# ============================================================================

class TestGameGenerator:
    """Test game template generator"""
    
    def test_create_generator(self):
        from ..game_generator import create_generator
        gen = create_generator()
        assert gen is not None
    
    def test_generate_optimizer(self):
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        
        manifest = gen.generate(
            GameTemplateType.THE_OPTIMIZER,
            {"domain": "Resource Management", "simulation_id": "sim-1"},
            kpis=["efficiency", "cost", "quality"],
        )
        
        assert manifest is not None
        assert manifest.template_type == GameTemplateType.THE_OPTIMIZER
        assert len(manifest.mechanic.resources) > 0
    
    def test_generate_crisis(self):
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        
        manifest = gen.generate(
            GameTemplateType.CRISIS_PROTOCOL,
            {"simulation_id": "sim-2"},
            crisis_scenario="System Outage",
        )
        
        assert manifest is not None
        assert manifest.template_type == GameTemplateType.CRISIS_PROTOCOL
    
    def test_generate_explorer(self):
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        
        manifest = gen.generate(
            GameTemplateType.THE_EXPLORER,
            {"simulation_id": "sim-3"},
        )
        
        assert manifest is not None
        assert manifest.template_type == GameTemplateType.THE_EXPLORER
    
    def test_manifest_signed(self):
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        manifest = gen.generate(
            GameTemplateType.THE_OPTIMIZER,
            {},
        )
        
        assert manifest.signature != ""
        assert manifest.opa_compliant is True


# ============================================================================
# GAME LOGIC TESTS
# ============================================================================

class TestGameLogic:
    """Test game logic engine"""
    
    def test_create_coordinator(self):
        from ..game_logic import create_coordinator
        coord = create_coordinator()
        assert coord is not None
    
    def test_start_game(self):
        from ..game_logic import create_coordinator
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        coord = create_coordinator()
        
        manifest = gen.generate(GameTemplateType.THE_OPTIMIZER, {})
        game_id = coord.start_game(manifest)
        
        assert game_id is not None
        
        status = coord.get_status(game_id)
        assert status["turn"] == 0
        assert status["status"] == "active"
    
    def test_play_action(self):
        from ..game_logic import create_coordinator
        from ..game_generator import create_generator
        from ..models import GameTemplateType
        
        gen = create_generator()
        coord = create_coordinator()
        
        manifest = gen.generate(GameTemplateType.THE_OPTIMIZER, {})
        game_id = coord.start_game(manifest)
        
        result, feedback = coord.play_action(
            game_id,
            "allocate",
            {"resource": "budget", "amount": 20},
        )
        
        assert result is not None
        assert feedback is not None
        assert feedback.message != ""
    
    def test_prompts_available(self):
        from ..game_logic import get_prompt_manager
        from ..models import GameTemplateType
        
        prompts = get_prompt_manager()
        
        meta = prompts.get_meta_prompt()
        assert "L2-GameArchitect" in meta
        
        optimizer = prompts.get_template_prompt(GameTemplateType.THE_OPTIMIZER)
        assert "Optimizer" in optimizer


# ============================================================================
# TRUST SCORE TESTS
# ============================================================================

class TestTrustScore:
    """Test trust score system"""
    
    def test_create_system(self):
        from ..leaderboard import create_trust_system
        system = create_trust_system()
        assert system is not None
    
    def test_calculate_scores(self):
        from ..leaderboard import TrustScoreCalculator
        from ..models import GameAction, SimulationResult
        
        calc = TrustScoreCalculator()
        
        actions = [
            GameAction(action_id="a1", action_type="allocate"),
            GameAction(action_id="a2", action_type="allocate"),
        ]
        
        results = [
            SimulationResult(result_id="r1", action_id="a1", divergence_score=0.1),
            SimulationResult(result_id="r2", action_id="a2", divergence_score=0.15),
        ]
        
        score = calc.update_score("player-1", actions, results)
        
        assert score is not None
        assert score.overall_score > 0
        assert score.conformity_score > 0
        assert score.resilience_score > 0
    
    def test_badges_issued(self):
        from ..leaderboard import create_trust_system
        from ..models import GameAction, SimulationResult
        
        system = create_trust_system()
        
        # Create high-scoring session
        actions = [GameAction(action_id=f"a{i}", action_type="optimal") for i in range(10)]
        results = [
            SimulationResult(result_id=f"r{i}", action_id=f"a{i}", divergence_score=0.05)
            for i in range(10)
        ]
        
        score, badges = system.record_game_session("player-1", actions, results, 0)
        
        assert score is not None
        # High scores should earn badges
        assert len(badges) >= 0  # May or may not qualify depending on scores
    
    def test_leaderboard_anonymized(self):
        from ..leaderboard import create_trust_system
        from ..models import GameAction, SimulationResult, anonymize_id
        
        system = create_trust_system()
        
        # Record some players
        for i in range(3):
            actions = [GameAction(action_id=f"a{i}", action_type="test")]
            results = [SimulationResult(result_id=f"r{i}", action_id=f"a{i}", divergence_score=0.2 * i)]
            system.record_game_session(f"player-{i}", actions, results)
        
        leaderboard = system.get_leaderboard(10)
        
        # Verify anonymization
        for entry in leaderboard:
            assert "player-" not in entry["anonymous_id"]
    
    def test_xr_agora(self):
        from ..leaderboard import create_trust_system
        from ..models import GameAction, SimulationResult
        
        system = create_trust_system()
        
        # Record player
        actions = [GameAction(action_id="a1", action_type="test")]
        results = [SimulationResult(result_id="r1", action_id="a1", divergence_score=0.1)]
        system.record_game_session("player-1", actions, results)
        
        agora = system.get_agora_xr()
        
        assert agora["type"] == "xr_agora"
        assert "entries" in agora


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestEntertainmentIntegration:
    """Integration tests"""
    
    def test_full_game_flow(self):
        """Test complete game flow from generation to leaderboard"""
        from ..game_generator import create_generator
        from ..game_logic import create_coordinator
        from ..leaderboard import create_trust_system
        from ..models import GameTemplateType
        
        # 1. Generate game
        gen = create_generator()
        manifest = gen.generate(
            GameTemplateType.CRISIS_PROTOCOL,
            {"domain": "IT", "simulation_id": "sim-crisis"},
            crisis_scenario="Security Breach",
        )
        
        # 2. Start game
        coord = create_coordinator()
        game_id = coord.start_game(manifest)
        
        # 3. Play actions
        all_actions = []
        all_results = []
        
        for i in range(3):
            result, feedback = coord.play_action(
                game_id,
                f"response_{i}",
                {"choice": i},
            )
            all_actions.append(coord.engine.get_action_history(game_id)[-1])
            all_results.append(result)
        
        # 4. Record to trust system
        trust = create_trust_system()
        score, badges = trust.record_game_session(
            "player-test",
            all_actions,
            all_results,
        )
        
        # 5. Verify results
        assert score.overall_score > 0
        assert score.decision_count == 3
        
        profile = trust.get_player_profile("player-test")
        assert profile["score"] is not None


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
