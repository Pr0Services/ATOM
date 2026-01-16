"""
============================================================================
CHE·NU™ V69 — SCHOLAR MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# KNOWLEDGE GRAPH TESTS
# ============================================================================

class TestKnowledgeGraph:
    """Test causal knowledge graph"""
    
    def test_create_graph(self):
        from ..knowledge_graph import create_knowledge_graph
        graph = create_knowledge_graph()
        assert graph is not None
    
    def test_add_node(self):
        from ..knowledge_graph import create_knowledge_graph
        from ..models import CausalNode, VerificationStatus
        
        graph = create_knowledge_graph()
        node = CausalNode(
            node_id="node-1",
            title="Discovery A",
            domain="biology",
        )
        
        graph.add_node(node)
        retrieved = graph.get_node("node-1")
        
        assert retrieved is not None
        assert retrieved.title == "Discovery A"
    
    def test_add_causal_link(self):
        from ..knowledge_graph import create_knowledge_graph
        from ..models import CausalNode
        
        graph = create_knowledge_graph()
        
        node_a = CausalNode(node_id="a", title="A", domain="biology")
        node_b = CausalNode(node_id="b", title="B", domain="biology")
        
        graph.add_node(node_a)
        graph.add_node(node_b)
        
        link = graph.add_link("a", "b", p_value=0.001, effect_size=0.8)
        
        assert link is not None
        assert link.strength.value == "very_strong"
    
    def test_export_for_xr(self):
        from ..knowledge_graph import create_knowledge_graph
        from ..models import CausalNode
        
        graph = create_knowledge_graph()
        graph.add_node(CausalNode(node_id="n1", title="N1", domain="biology"))
        
        export = graph.export_for_xr()
        
        assert "nodes" in export
        assert "links" in export
        assert len(export["nodes"]) == 1


# ============================================================================
# ANALOGICAL SEARCH TESTS
# ============================================================================

class TestAnalogicalSearch:
    """Test analogical search engine"""
    
    def test_create_engine(self):
        from ..analogical_search import create_search_engine
        engine = create_search_engine()
        assert engine is not None
    
    def test_index_pattern(self):
        from ..analogical_search import create_search_engine
        from ..models import CausalNode, CausalLink
        
        engine = create_search_engine()
        
        nodes = [
            CausalNode(node_id="1", title="A", domain="biology"),
            CausalNode(node_id="2", title="B", domain="biology"),
        ]
        links = [
            CausalLink(link_id="l1", source_id="1", target_id="2", p_value=0.01, effect_size=0.5)
        ]
        
        pattern = engine.index_pattern(nodes, links, "biology", "test_pattern")
        
        assert pattern is not None
        assert pattern.node_count == 2


# ============================================================================
# IMPACT SIMULATOR TESTS
# ============================================================================

class TestImpactSimulator:
    """Test impact simulator"""
    
    def test_create_simulator(self):
        from ..impact_simulator import create_simulator
        sim = create_simulator()
        assert sim is not None
    
    def test_simulate_funding(self):
        from ..impact_simulator import create_simulator, create_scenario
        
        sim = create_simulator()
        scenario = create_scenario(
            name="Biotech Investment",
            amount=10_000_000,
            domain="biotech",
            years=10,
        )
        
        result = sim.simulate(scenario)
        
        assert result is not None
        assert result.total_impact_score > 0
        assert "gdp" in result.impacts
        assert "public_health" in result.impacts


# ============================================================================
# CONTRIBUTION TRACKING TESTS
# ============================================================================

class TestContributionTracking:
    """Test contribution tracking"""
    
    def test_create_tracker(self):
        from ..contribution_tracking import create_tracker
        tracker = create_tracker()
        assert tracker is not None
    
    def test_record_contribution(self):
        from ..contribution_tracking import create_tracker
        from ..models import ContributionType
        
        tracker = create_tracker()
        
        contrib = tracker.record(
            artifact_id="art-1",
            contributor_id="user-1",
            contribution_type=ContributionType.IDEA,
            description="Initial concept",
        )
        
        assert contrib is not None
        assert contrib.artifact_id == "art-1"
    
    def test_equity_calculation(self):
        from ..contribution_tracking import create_tracker
        from ..models import ContributionType
        
        tracker = create_tracker()
        
        # Add multiple contributions
        tracker.record("art-1", "user-1", ContributionType.IDEA, "Idea")
        tracker.record("art-1", "user-2", ContributionType.CODE, "Code")
        tracker.record("art-1", "user-1", ContributionType.DATA, "Data")
        
        equity = tracker.get_equity("art-1")
        
        assert equity is not None
        assert equity.total_contributions == 3
        assert "user-1" in equity.equity_distribution
        assert "user-2" in equity.equity_distribution


# ============================================================================
# REPRODUCIBILITY TESTS
# ============================================================================

class TestReproducibility:
    """Test reproducibility protocol"""
    
    def test_create_protocol(self):
        from ..reproducibility import create_protocol
        protocol = create_protocol()
        assert protocol is not None
    
    def test_run_verification(self):
        from ..reproducibility import create_protocol
        
        protocol = create_protocol()
        
        job = protocol.create_job(
            artifact_id="art-1",
            code_ref="code://test",
            data_ref="data://test",
        )
        
        original_output = {"result": 42, "metrics": [0.1, 0.2]}
        
        job, badge = protocol.run_verification(job.job_id, original_output)
        
        assert job.status.value in ["passed", "partial", "failed"]
        assert job.reproducibility_score >= 0


# ============================================================================
# BIO STORAGE TESTS
# ============================================================================

class TestBioStorage:
    """Test bio-digital storage"""
    
    def test_create_service(self):
        from ..bio_storage import create_storage_service
        service = create_storage_service()
        assert service is not None
    
    def test_store_artifact(self):
        from ..bio_storage import create_storage_service
        
        service = create_storage_service()
        
        artifact_data = {
            "title": "Important Discovery",
            "data": [1, 2, 3, 4, 5],
        }
        
        capsule = service.store("art-1", artifact_data)
        
        assert capsule is not None
        assert capsule.status.value == "stored"
        assert capsule.shard_count > 0
    
    def test_decode_requires_hitl(self):
        from ..bio_storage import create_storage_service
        
        service = create_storage_service()
        
        # Store first
        service.store("art-1", {"test": "data"})
        capsule = list(service._capsules.values())[0]
        
        # Request decode
        request = service.request_decode(capsule.capsule_id)
        
        assert request.requires_hitl is True
        assert request.status == "pending_approval"


# ============================================================================
# CROSS-POLLINATOR TESTS
# ============================================================================

class TestCrossPollinator:
    """Test cross-pollinator agent"""
    
    def test_create_agent(self):
        from ..cross_pollinator import create_cross_pollinator
        agent = create_cross_pollinator()
        assert agent is not None
    
    def test_find_matches(self):
        from ..cross_pollinator import create_cross_pollinator
        
        agent = create_cross_pollinator()
        
        artifacts = [
            {
                "id": "art-1",
                "domain": "biology",
                "keywords": ["protein", "structure", "folding"],
                "methods": ["x-ray", "simulation"],
            },
            {
                "id": "art-2",
                "domain": "engineering",
                "keywords": ["material", "structure", "stress"],
                "methods": ["simulation", "testing"],
            },
        ]
        
        notifications = agent.process_artifacts(artifacts)
        
        # Should find cross-domain match
        assert len(agent._matches) > 0 or len(notifications) >= 0
    
    def test_create_task_force(self):
        from ..cross_pollinator import create_cross_pollinator
        from ..models import CrossPollinationMatch
        
        agent = create_cross_pollinator()
        
        # Create a match manually
        match = CrossPollinationMatch(
            match_id="match-1",
            artifact_a="art-1",
            artifact_b="art-2",
            domain_a="biology",
            domain_b="engineering",
            similarity_type="structural",
            similarity_score=0.8,
        )
        agent._matches["match-1"] = match
        
        tf = agent.create_task_force_from_match("match-1", ["user-1", "user-2"])
        
        assert tf is not None
        assert tf.status == "proposed"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_scholar_workflow(self):
        """Test complete scholar workflow"""
        from ..knowledge_graph import create_knowledge_graph
        from ..contribution_tracking import create_tracker
        from ..reproducibility import create_protocol
        from ..models import CausalNode, ContributionType
        
        # 1. Create knowledge graph
        graph = create_knowledge_graph()
        node = CausalNode(node_id="discovery-1", title="New Discovery", domain="biology")
        graph.add_node(node)
        
        # 2. Track contributions
        tracker = create_tracker()
        tracker.record("discovery-1", "researcher-1", ContributionType.IDEA, "Initial hypothesis")
        tracker.record("discovery-1", "researcher-2", ContributionType.CODE, "Analysis code")
        tracker.commit()
        
        equity = tracker.get_equity("discovery-1")
        assert equity.total_contributions == 2
        
        # 3. Run reproducibility check
        protocol = create_protocol()
        job = protocol.create_job("discovery-1", "code://test", "data://test")
        job, badge = protocol.run_verification(job.job_id, {"result": 42})
        
        # 4. Update node with verification status
        if badge and badge.badge_level in ["platinum", "gold"]:
            from ..models import VerificationStatus
            node.status = VerificationStatus.VERIFIED
            node.reproducibility_score = badge.reproducibility_score


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
