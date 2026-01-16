"""
============================================================================
CHE·NU™ V69 — FRONTIERS MODULE (Modules 11-16)
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_ENG_NEUROMORPHIC_LATTICE_V1.md
- CHE-NU_ENG_SEMANTIC_AGENT_COMMUNICATION.md
- CHE-NU_GOV_SYNTHETIC_DIPLOMACY_PROTOCOL.md
- CHE-NU_SCH_BIO_DIGITAL_STORAGE_V1.md
- CHE-NU_LAB_M_HAPTIC_MATTER_INTERFACE.md
- CHE-NU_LAB_M_PROGRAMMABLE_REALITY_V1.md
- CHE-NU_SYS_EMERGENCY_RECONSTRUCTION_LOGIC.md

"Artifacts de civilisation archivés sur 1000-10000 ans"

Principle: GOUVERNANCE > EXÉCUTION, READ-ONLY ON REAL
============================================================================
"""

# Models
from .models import (
    # Neuromorphic
    SpikeType, SpikeEvent, Synapse, NeuroMap,
    # Semantic
    ConceptType, StateType, RelationType, SemanticPacket,
    # Diplomacy
    DiplomacyInstance, DiplomacyProposal, DiplomacyScore,
    # Bio Storage
    DNABase, DNAShard, BioCapsule,
    # Haptic
    HapticZone, HapticCommand,
    # D2P
    D2PMode, MatterCommand,
    # Emergency
    MinimalBootKit, ReconstructionStep, ReconstructionLog,
    # Utils
    generate_id, compute_hash, sign_artifact,
)

# Neuromorphic Lattice
from .neuromorphic import (
    NeuromorphicLattice,
    SpikeBus,
    SynapseMapper,
    PlasticityWorker,
    create_neuromorphic_lattice,
)

# Semantic Communication
from .semantic_comm import (
    SemanticCommunicationSystem,
    CoreOntology,
    ZLogicCompressor,
    TruthSync,
    create_semantic_comm,
)

# Advanced modules
from .advanced import (
    SyntheticDiplomacyProtocol,
    BioDigitalStorage,
    HapticInterface,
    ProgrammableReality,
    EmergencyReconstruction,
    create_diplomacy,
    create_bio_storage,
    create_haptic,
    create_programmable_reality,
    create_emergency_reconstruction,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "SpikeType", "SpikeEvent", "Synapse", "NeuroMap",
    "ConceptType", "StateType", "RelationType", "SemanticPacket",
    "DiplomacyInstance", "DiplomacyProposal", "DiplomacyScore",
    "DNABase", "DNAShard", "BioCapsule",
    "HapticZone", "HapticCommand",
    "D2PMode", "MatterCommand",
    "MinimalBootKit", "ReconstructionStep", "ReconstructionLog",
    "generate_id", "compute_hash", "sign_artifact",
    # Neuromorphic
    "NeuromorphicLattice", "SpikeBus", "SynapseMapper",
    "PlasticityWorker", "create_neuromorphic_lattice",
    # Semantic
    "SemanticCommunicationSystem", "CoreOntology",
    "ZLogicCompressor", "TruthSync", "create_semantic_comm",
    # Diplomacy
    "SyntheticDiplomacyProtocol", "create_diplomacy",
    # Bio Storage
    "BioDigitalStorage", "create_bio_storage",
    # Haptic
    "HapticInterface", "create_haptic",
    # D2P
    "ProgrammableReality", "create_programmable_reality",
    # Emergency
    "EmergencyReconstruction", "create_emergency_reconstruction",
]
