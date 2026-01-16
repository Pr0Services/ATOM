"""
============================================================================
CHE·NU™ V69 — FRONTIERS MODULE TESTS
============================================================================
Tests for all 7 Frontiers specs (Modules 11-16):
1. Neuromorphic Lattice
2. Semantic Agent Communication
3. Synthetic Diplomacy Protocol
4. Bio Digital Storage
5. Haptic Matter Interface
6. Programmable Reality (D2P)
7. Emergency Reconstruction

Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

import unittest
from datetime import datetime

# Import all frontiers modules
from ..models import (
    SpikeType, SpikeEvent, Synapse, NeuroMap,
    ConceptType, StateType, RelationType, SemanticPacket,
    DiplomacyInstance, DiplomacyProposal, DiplomacyScore,
    DNABase, DNAShard, BioCapsule,
    HapticZone, HapticCommand,
    D2PMode, MatterCommand,
    MinimalBootKit, ReconstructionStep, ReconstructionLog,
    generate_id, compute_hash, sign_artifact,
)

from ..neuromorphic.lattice import (
    NeuromorphicLattice, SpikeBus, SynapseMapper, PlasticityWorker,
    create_neuromorphic_lattice,
)

from ..semantic_comm.communication import (
    SemanticCommunicationSystem, CoreOntology, ZLogicCompressor, TruthSync,
    create_semantic_comm,
)

from ..advanced import (
    SyntheticDiplomacyProtocol, BioDigitalStorage, HapticInterface,
    ProgrammableReality, EmergencyReconstruction,
    create_diplomacy, create_bio_storage, create_haptic,
    create_programmable_reality, create_emergency_reconstruction,
)


class TestNeuromorphicLattice(unittest.TestCase):
    """Test Neuromorphic Lattice (Module 11)"""
    
    def setUp(self):
        self.lattice = create_neuromorphic_lattice()
    
    def test_spike_bus_emit(self):
        """Test spike event emission"""
        event = SpikeEvent(
            event_id=generate_id(),
            spike_type=SpikeType.ALERT,
            intensity=0.8,
            source_agent="test_agent",
            trace_id=generate_id(),
        )
        
        self.lattice.bus.emit(event)
        recent = self.lattice.bus.get_recent(10)
        
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0].spike_type, SpikeType.ALERT)
    
    def test_synapse_creation(self):
        """Test synapse mapping between agents"""
        synapse = self.lattice.mapper.create_synapse(
            source_agent="agent_a",
            target_agent="agent_b",
            threshold=0.6,
            inputs=[SpikeType.SLOT_DELTA],
            outputs=[SpikeType.ROUTE],
        )
        
        self.assertIsNotNone(synapse.synapse_id)
        self.assertEqual(synapse.source_agent, "agent_a")
        self.assertEqual(synapse.threshold, 0.6)
    
    def test_anomaly_detection(self):
        """Test anomaly detection with spike generation"""
        # Should detect anomaly (50% deviation > 20% threshold)
        event = self.lattice.detect_anomaly("revenue", 150, 100, threshold=0.2)
        
        self.assertIsNotNone(event)
        self.assertEqual(event.spike_type, SpikeType.ALERT)
        self.assertGreater(event.intensity, 0)
    
    def test_no_anomaly_within_threshold(self):
        """Test no anomaly when within threshold"""
        event = self.lattice.detect_anomaly("revenue", 110, 100, threshold=0.2)
        
        self.assertIsNone(event)
    
    def test_priority_scoring(self):
        """Test quick priority scoring"""
        priority, event = self.lattice.score_priority(
            "critical_kpi",
            risk_level=0.9,
            impact_score=0.8,
        )
        
        # Expected: 0.9 * 0.6 + 0.8 * 0.4 = 0.86
        self.assertAlmostEqual(priority, 0.86, places=2)
        self.assertEqual(event.spike_type, SpikeType.PRIORITY)
    
    def test_plasticity_adjustment(self):
        """Test plasticity worker threshold adjustment"""
        synapse = self.lattice.mapper.create_synapse("a", "b", threshold=0.5)
        
        adjustment = self.lattice.plasticity.propose_adjustment(
            synapse.synapse_id,
            feedback_positive=True,
            delta=0.05,
        )
        
        self.assertIsNotNone(adjustment)
        self.assertEqual(adjustment.old_threshold, 0.5)
        self.assertEqual(adjustment.new_threshold, 0.55)
    
    def test_kpis(self):
        """Test KPI retrieval"""
        kpis = self.lattice.get_kpis()
        
        self.assertIn("propagation_p50_ms", kpis)
        self.assertIn("false_positives", kpis)
        self.assertIn("total_events", kpis)


class TestSemanticCommunication(unittest.TestCase):
    """Test Semantic Agent Communication (Module 14)"""
    
    def setUp(self):
        self.semantic = create_semantic_comm()
    
    def test_packet_creation(self):
        """Test semantic packet creation"""
        packet = self.semantic.create_packet(
            concept=ConceptType.FINANCIAL_RISK,
            state=StateType.WARNING,
            relation=RelationType.IMPACTS,
            scope="finance",
            confidence=0.85,
            evidence_refs=["artifact_001"],
        )
        
        self.assertEqual(packet.concept, ConceptType.FINANCIAL_RISK)
        self.assertEqual(packet.state, StateType.WARNING)
        self.assertFalse(packet.speculative)  # Has evidence
    
    def test_speculative_packet(self):
        """Test speculative packet (no evidence)"""
        packet = self.semantic.create_packet(
            concept=ConceptType.SUPPLY_CHAIN,
            state=StateType.CRITICAL_THRESHOLD,
            relation=RelationType.CAUSES,
            scope="logistics",
            confidence=0.5,
            evidence_refs=[],  # No evidence
        )
        
        self.assertTrue(packet.speculative)
    
    def test_z_logic_compression(self):
        """Test Z-Logic compression (1000 points → 1)"""
        datapoints = [{"value": i} for i in range(1000)]
        
        packet = self.semantic.compressor.compress(
            datapoints,
            ConceptType.OPERATIONAL,
        )
        
        self.assertIsNotNone(packet)
        self.assertEqual(packet.concept, ConceptType.OPERATIONAL)
        self.assertIn("1000", packet.provenance)
    
    def test_truth_sync(self):
        """Test truth synchronization"""
        self.semantic.truth_sync.set_context(
            worldstate={"revenue": 1000},
            causal_graph={"revenue": ["cost"]},
        )
        
        packet = self.semantic.create_packet(
            concept=ConceptType.OPERATIONAL,
            state=StateType.NORMAL,
            relation=RelationType.IMPACTS,
            scope="test",
            confidence=0.9,
        )
        
        self.assertNotEqual(packet.worldstate_hash, "")
        self.assertNotEqual(packet.causal_graph_hash, "")
    
    def test_encode_decode(self):
        """Test encode/decode roundtrip"""
        data = {"risk": "high", "impact": 0.8}
        
        packet = self.semantic.encode(data)
        decoded = self.semantic.decode(packet)
        
        self.assertIn("concept", decoded)
        self.assertEqual(decoded["concept"], "financial_risk")


class TestSyntheticDiplomacy(unittest.TestCase):
    """Test Synthetic Diplomacy Protocol"""
    
    def setUp(self):
        self.diplomacy = create_diplomacy()
    
    def test_instance_management(self):
        """Test adding diplomacy instances"""
        instance = DiplomacyInstance(
            instance_id="corp_a",
            name="Corporation A",
            opa_bundle="bundle_a",
            objectives={"profit": 0.8},
        )
        
        self.diplomacy.add_instance(instance)
        
        self.assertIn("corp_a", self.diplomacy._instances)
    
    def test_proposal_submission(self):
        """Test proposal submission (always draft)"""
        self.diplomacy.add_instance(DiplomacyInstance(
            instance_id="corp_a",
            name="Corp A",
            opa_bundle="bundle",
        ))
        
        proposal = self.diplomacy.submit_proposal("corp_a", {"share": 0.6})
        
        self.assertTrue(proposal.draft)
        self.assertEqual(proposal.instance_id, "corp_a")
    
    def test_negotiation_simulation(self):
        """Test negotiation simulation with game theory"""
        # Add two instances
        self.diplomacy.add_instance(DiplomacyInstance(
            instance_id="a", name="A", opa_bundle="b",
        ))
        self.diplomacy.add_instance(DiplomacyInstance(
            instance_id="b", name="B", opa_bundle="b",
        ))
        
        # Submit proposals
        self.diplomacy.submit_proposal("a", {"share": 0.6})
        self.diplomacy.submit_proposal("b", {"share": 0.4})
        
        score = self.diplomacy.simulate_negotiation()
        
        self.assertIsInstance(score, DiplomacyScore)
        self.assertTrue(score.nash_stable)  # 2 parties = simple
        self.assertGreater(score.trust_score, 0)
    
    def test_export_report(self):
        """Test diplomacy report export"""
        self.diplomacy.add_instance(DiplomacyInstance(
            instance_id="test", name="Test", opa_bundle="b",
        ))
        
        report = self.diplomacy.export_report()
        
        self.assertIn("report_id", report)
        self.assertIn("DRAFT", report["note"])


class TestBioDigitalStorage(unittest.TestCase):
    """Test Bio Digital Storage (1000-10000 years)"""
    
    def setUp(self):
        self.bio = create_bio_storage()
    
    def test_capsule_creation(self):
        """Test bio capsule creation"""
        data = b"CHE-NU Artifact Data"
        
        capsule = self.bio.create_capsule(data, "artifact_001")
        
        self.assertIsNotNone(capsule.capsule_id)
        self.assertEqual(capsule.magic, "CHE_NU_BIO_V1")
        self.assertGreater(len(capsule.shards), 0)
    
    def test_dna_encoding(self):
        """Test DNA encoding (bytes → A/T/C/G)"""
        data = b"Test"
        
        shards = self.bio.encoder.encode(data)
        
        self.assertGreater(len(shards), 0)
        for shard in shards:
            # Verify only valid bases
            for base in shard.sequence:
                self.assertIn(base, "ATCG")
    
    def test_roundtrip_integrity(self):
        """Test encode/decode roundtrip (bit-perfect)"""
        original = b"CHE-NU Proof of Governance 2026"
        
        capsule = self.bio.create_capsule(original, "proof_001")
        retrieved = self.bio.retrieve(capsule.capsule_id)
        
        self.assertEqual(retrieved, original)
    
    def test_verification(self):
        """Test integrity verification"""
        data = b"Important Artifact"
        original_hash = compute_hash(data)
        
        capsule = self.bio.create_capsule(data, "art_001")
        verified = self.bio.verify(capsule.capsule_id, original_hash)
        
        self.assertTrue(verified)
    
    def test_tamper_detection(self):
        """Test tamper detection"""
        data = b"Secure Data"
        
        capsule = self.bio.create_capsule(data, "secure_001")
        
        # Wrong hash should fail verification
        verified = self.bio.verify(capsule.capsule_id, "wrong_hash")
        
        self.assertFalse(verified)


class TestHapticInterface(unittest.TestCase):
    """Test Haptic Matter Interface"""
    
    def setUp(self):
        self.haptic = create_haptic()
    
    def test_zone_creation(self):
        """Test haptic zone creation"""
        zone = self.haptic.create_zone((0.5, 0.5, 0.0), size=0.1)
        
        self.assertIsNotNone(zone.zone_id)
        self.assertEqual(zone.position, (0.5, 0.5, 0.0))
    
    def test_zone_update(self):
        """Test zone feedback update"""
        zone = self.haptic.create_zone((0.5, 0.5, 0.0), size=0.1)
        
        updated = self.haptic.update_zone(
            zone.zone_id,
            vibration=0.7,
            stiffness=0.8,
            thermal=0.5,
        )
        
        self.assertEqual(updated.vibration_intensity, 0.7)
        self.assertEqual(updated.stiffness, 0.8)
        self.assertEqual(updated.thermal, 0.5)
    
    def test_safety_caps(self):
        """Test safety caps enforcement"""
        zone = self.haptic.create_zone((0, 0, 0), size=0.1)
        
        # Try to exceed max vibration
        updated = self.haptic.update_zone(zone.zone_id, vibration=2.0)
        
        self.assertLessEqual(updated.vibration_intensity, 1.0)
    
    def test_command_generation(self):
        """Test haptic command with audit trail"""
        zone = self.haptic.create_zone((0, 0, 0), size=0.1)
        
        cmd = self.haptic.generate_command("device_001", trace_id="trace_123")
        
        self.assertIsNotNone(cmd.command_id)
        self.assertEqual(cmd.device_id, "device_001")
        self.assertEqual(cmd.trace_id, "trace_123")
        self.assertIn("max_vibration", cmd.safety_caps)
        self.assertNotEqual(cmd.signature, "")


class TestProgrammableReality(unittest.TestCase):
    """Test Programmable Reality (D2P)"""
    
    def setUp(self):
        self.d2p = create_programmable_reality()
    
    def test_mode_setting(self):
        """Test D2P mode configuration"""
        self.d2p.set_mode(D2PMode.PROGRAMMABLE_FORM)
        
        self.assertEqual(self.d2p._mode, D2PMode.PROGRAMMABLE_FORM)
    
    def test_command_generation(self):
        """Test matter command generation"""
        geometry = {
            "vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
            "faces": [[0, 1, 2]],
        }
        
        cmd = self.d2p.generate_command("matter_device", geometry)
        
        self.assertIsNotNone(cmd.command_id)
        self.assertGreater(len(cmd.geometry_targets), 0)
        self.assertIn("ED25519", cmd.signatures)
    
    def test_safety_caps(self):
        """Test safety caps in commands"""
        cmd = self.d2p.generate_command("device", {"vertices": []})
        
        self.assertIn("amplitude_max", cmd.safety_caps)
        self.assertIn("force_max", cmd.safety_caps)
        self.assertIn("velocity_max", cmd.safety_caps)
    
    def test_audit_trail(self):
        """Test command audit trail"""
        self.d2p.generate_command("device", {"vertices": []})
        self.d2p.generate_command("device", {"vertices": []})
        
        audit = self.d2p.get_audit_trail()
        
        self.assertEqual(len(audit), 2)
        self.assertIn("timestamp", audit[0])


class TestEmergencyReconstruction(unittest.TestCase):
    """Test Emergency Reconstruction Logic"""
    
    def setUp(self):
        self.emergency = create_emergency_reconstruction()
    
    def test_mbk_creation(self):
        """Test Minimal Boot Kit creation"""
        mbk = self.emergency.create_boot_kit(
            worldengine_spec={"version": "1.0"},
            opa_policies={"core": "governance"},
            semantic_ontology={"concepts": 100},
        )
        
        self.assertIsNotNone(mbk.kit_id)
        self.assertNotEqual(mbk.worldengine_spec_hash, "")
        self.assertGreater(len(mbk.locations), 0)
    
    def test_reconstruction_step(self):
        """Test single reconstruction step"""
        log = self.emergency.execute_step(
            ReconstructionStep.REHYDRATE_POLICIES,
            human_approved=True,
        )
        
        self.assertEqual(log.status, "success")
        self.assertTrue(log.human_approved)
    
    def test_hitl_requirement(self):
        """Test HITL requirement for sensitive steps"""
        log = self.emergency.execute_step(
            ReconstructionStep.SANDBOX_MODE,
            human_approved=False,
        )
        
        self.assertEqual(log.status, "awaiting_human_approval")
    
    def test_cold_start_drill(self):
        """Test cold start drill (quarterly)"""
        self.emergency.create_boot_kit(
            worldengine_spec={},
            opa_policies={},
            semantic_ontology={},
        )
        
        drill = self.emergency.run_cold_start_drill()
        
        self.assertTrue(drill["success"])
        self.assertEqual(drill["final_mode"], "read_only")
        self.assertEqual(len(drill["results"]), 5)
    
    def test_mode_progression(self):
        """Test mode progression during reconstruction"""
        self.assertEqual(self.emergency._mode, "offline")
        
        self.emergency.execute_step(
            ReconstructionStep.READ_ONLY_MODE,
            human_approved=True,
        )
        
        self.assertEqual(self.emergency._mode, "read_only")


class TestGovernanceCompliance(unittest.TestCase):
    """Test governance compliance across all modules"""
    
    def test_all_commands_signed(self):
        """Verify all commands have signatures"""
        haptic = create_haptic()
        haptic.create_zone((0, 0, 0), 0.1)
        cmd = haptic.generate_command("device")
        
        self.assertNotEqual(cmd.signature, "")
        
        d2p = create_programmable_reality()
        matter_cmd = d2p.generate_command("device", {})
        
        self.assertIn("ED25519", matter_cmd.signatures)
    
    def test_bio_storage_integrity(self):
        """Verify bio storage maintains integrity"""
        bio = create_bio_storage()
        
        data = b"Critical Artifact"
        capsule = bio.create_capsule(data, "critical")
        
        # Verify signature present
        self.assertIn("ED25519", capsule.signatures)
        
        # Verify hash present
        self.assertNotEqual(capsule.payload_hash, "")
    
    def test_speculative_routing(self):
        """Verify speculative packets marked correctly"""
        semantic = create_semantic_comm()
        
        # No evidence = speculative
        packet = semantic.create_packet(
            concept=ConceptType.FINANCIAL_RISK,
            state=StateType.WARNING,
            relation=RelationType.IMPACTS,
            scope="test",
            confidence=0.5,
            evidence_refs=[],
        )
        
        self.assertTrue(packet.speculative)
    
    def test_diplomacy_draft_only(self):
        """Verify all diplomacy proposals are draft"""
        diplomacy = create_diplomacy()
        diplomacy.add_instance(DiplomacyInstance(
            instance_id="test", name="Test", opa_bundle="b",
        ))
        
        proposal = diplomacy.submit_proposal("test", {"option": 1})
        
        self.assertTrue(proposal.draft)


if __name__ == "__main__":
    unittest.main()
