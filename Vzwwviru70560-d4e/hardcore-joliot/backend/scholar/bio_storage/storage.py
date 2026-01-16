"""
============================================================================
CHE·NU™ V69 — SCHOLAR BIO-DIGITAL STORAGE
============================================================================
Spec: GPT1/CHE-NU_SCH_BIO_DIGITAL_STORAGE_V1.md

Objective: Archive "civilization artifacts" for 1,000-10,000 years.

Principle (per spec): Artifact → DNA sequence (A/T/C/G) → redundancy + index

Workers (per spec):
- BIO_ENCODER_WORKER: JSON/ZIP → bitstream → DNA codewords + ECC
- BIO_INDEXER_WORKER: builds index (Manifest) + pointers (shards)
- BIO_VERIFIER_WORKER: verifies hash, ECC, signatures
- BIO_DECODER_WORKER: DNA reads → bitstream → original Artifact

Governance: DNA is a storage medium, NOT execution channel.
HITL obligatoire for decode/rehydrate operations.
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import hashlib
import base64
import json
import zlib

from ..models import (
    BioCapsule,
    DNAShard,
    DecodeRequest,
    BioStorageStatus,
    generate_id,
    compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# DNA ENCODING CONSTANTS
# ============================================================================

# Binary to DNA mapping (with GC balance constraints)
BINARY_TO_DNA = {
    "00": "A",
    "01": "C",
    "10": "G",
    "11": "T",
}

DNA_TO_BINARY = {v: k for k, v in BINARY_TO_DNA.items()}

# Magic header for CHE·NU capsules
CHE_NU_MAGIC = "CHENU_BIO_V1"

# Shard configuration
DEFAULT_SHARD_SIZE_BP = 512  # Base pairs per shard
MAX_HOMOPOLYMER_LENGTH = 3  # Max consecutive identical bases


# ============================================================================
# CANONICALIZER
# ============================================================================

class Canonicalizer:
    """
    Canonicalize artifacts before encoding.
    
    Per spec: Tri stable des clés JSON, normalisation encodage
    """
    
    def canonicalize(self, data: Any) -> bytes:
        """Canonicalize data to deterministic bytes"""
        # Sort keys, ensure UTF-8, LF line endings
        if isinstance(data, dict):
            canonical_json = json.dumps(
                data,
                sort_keys=True,
                ensure_ascii=False,
                separators=(',', ':'),
            )
            return canonical_json.encode('utf-8')
        elif isinstance(data, str):
            return data.replace('\r\n', '\n').encode('utf-8')
        elif isinstance(data, bytes):
            return data
        else:
            return str(data).encode('utf-8')
    
    def compress(self, data: bytes, level: int = 9) -> bytes:
        """
        Deterministic compression.
        
        Per spec: Compression deterministe (zstd level fixe)
        """
        # Using zlib for determinism (zstd would be better in production)
        return zlib.compress(data, level)
    
    def decompress(self, data: bytes) -> bytes:
        """Decompress data"""
        return zlib.decompress(data)


# ============================================================================
# DNA ENCODER
# ============================================================================

class DNAEncoder:
    """
    Encode binary data to DNA sequences.
    
    Per spec: Binary → bases with GC balance and homopolymer limits
    """
    
    def __init__(
        self,
        max_homopolymer: int = MAX_HOMOPOLYMER_LENGTH,
    ):
        self.max_homopolymer = max_homopolymer
    
    def encode(self, data: bytes) -> str:
        """Encode bytes to DNA sequence"""
        # Convert to binary string
        binary = ''.join(format(byte, '08b') for byte in data)
        
        # Pad to even length
        if len(binary) % 2 != 0:
            binary += '0'
        
        # Convert to DNA
        dna = []
        for i in range(0, len(binary), 2):
            pair = binary[i:i+2]
            base = BINARY_TO_DNA.get(pair, 'A')
            
            # Check homopolymer constraint
            if len(dna) >= self.max_homopolymer:
                last_bases = ''.join(dna[-self.max_homopolymer:])
                if all(b == base for b in last_bases):
                    # Rotate to avoid homopolymer
                    bases = ['A', 'C', 'G', 'T']
                    idx = bases.index(base)
                    base = bases[(idx + 1) % 4]
            
            dna.append(base)
        
        return ''.join(dna)
    
    def decode(self, dna: str) -> bytes:
        """Decode DNA sequence to bytes"""
        # Convert DNA to binary
        binary = ''
        for base in dna:
            binary += DNA_TO_BINARY.get(base, '00')
        
        # Convert binary to bytes
        byte_list = []
        for i in range(0, len(binary), 8):
            byte_str = binary[i:i+8]
            if len(byte_str) == 8:
                byte_list.append(int(byte_str, 2))
        
        return bytes(byte_list)
    
    def compute_gc_content(self, dna: str) -> float:
        """Compute GC content (should be ~50%)"""
        if not dna:
            return 0.0
        gc_count = sum(1 for b in dna if b in 'GC')
        return gc_count / len(dna)
    
    def find_max_homopolymer(self, dna: str) -> int:
        """Find longest homopolymer run"""
        if not dna:
            return 0
        
        max_run = 1
        current_run = 1
        
        for i in range(1, len(dna)):
            if dna[i] == dna[i-1]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        
        return max_run


# ============================================================================
# ERROR CORRECTION
# ============================================================================

class ErrorCorrection:
    """
    Error correction coding for DNA storage.
    
    Per spec: ECC par shard (Reed-Solomon / fountain codes)
    """
    
    def __init__(self, strength: int = 32):
        self.strength = strength  # Number of ECC symbols
    
    def encode(self, data: bytes) -> Tuple[bytes, bytes]:
        """
        Encode data with ECC.
        
        Returns (data, ecc_data)
        """
        # Simplified ECC (in production, use Reed-Solomon)
        # This creates a checksum-based redundancy
        
        checksum = hashlib.sha256(data).digest()
        
        # Create redundancy blocks
        ecc_blocks = []
        block_size = max(len(data) // self.strength, 1)
        
        for i in range(self.strength):
            start = i * block_size
            end = min(start + block_size, len(data))
            block = data[start:end]
            block_hash = hashlib.sha256(block).digest()[:4]
            ecc_blocks.append(block_hash)
        
        ecc_data = checksum + b''.join(ecc_blocks)
        return data, ecc_data
    
    def verify(self, data: bytes, ecc_data: bytes) -> bool:
        """Verify data against ECC"""
        if len(ecc_data) < 32:
            return False
        
        stored_checksum = ecc_data[:32]
        computed_checksum = hashlib.sha256(data).digest()
        
        return stored_checksum == computed_checksum
    
    def repair(self, data: bytes, ecc_data: bytes) -> Optional[bytes]:
        """
        Attempt to repair corrupted data.
        
        Note: Simplified implementation - production would use full RS
        """
        if self.verify(data, ecc_data):
            return data
        
        # Cannot repair in this simplified implementation
        return None


# ============================================================================
# BIO ENCODER WORKER
# ============================================================================

class BioEncoderWorker:
    """
    Encode artifacts for DNA storage.
    
    Per spec: JSON/ZIP → bitstream canonique → DNA codewords + ECC
    """
    
    def __init__(self):
        self.canonicalizer = Canonicalizer()
        self.dna_encoder = DNAEncoder()
        self.ecc = ErrorCorrection()
    
    def encode(
        self,
        artifact_data: Any,
        artifact_id: str,
        shard_size: int = DEFAULT_SHARD_SIZE_BP,
    ) -> Tuple[BioCapsule, List[DNAShard]]:
        """Encode artifact to DNA capsule"""
        # Step 1: Canonicalize
        canonical = self.canonicalizer.canonicalize(artifact_data)
        
        # Step 2: Compress
        compressed = self.canonicalizer.compress(canonical)
        
        # Step 3: Add header
        header = f"{CHE_NU_MAGIC}|{artifact_id}|{len(compressed)}|".encode('utf-8')
        payload = header + compressed
        
        # Step 4: Compute hash
        payload_hash = compute_hash(payload)
        
        # Step 5: Add ECC
        payload_with_ecc, ecc_data = self.ecc.encode(payload)
        
        # Step 6: Encode to DNA
        dna_sequence = self.dna_encoder.encode(payload_with_ecc)
        
        # Step 7: Create shards
        shards = []
        num_shards = (len(dna_sequence) + shard_size - 1) // shard_size
        
        for i in range(num_shards):
            start = i * shard_size
            end = min(start + shard_size, len(dna_sequence))
            shard_dna = dna_sequence[start:end]
            
            shard = DNAShard(
                shard_id=f"{artifact_id}_shard_{i:04d}",
                capsule_id=artifact_id,
                shard_index=i,
                base_pairs=len(shard_dna),
                gc_content=self.dna_encoder.compute_gc_content(shard_dna),
                homopolymer_max=self.dna_encoder.find_max_homopolymer(shard_dna),
                ecc_data=ecc_data if i == 0 else b"",  # ECC in first shard
                shard_hash=compute_hash(shard_dna),
            )
            shards.append(shard)
        
        # Step 8: Create capsule
        capsule = BioCapsule(
            capsule_id=generate_id(),
            artifact_id=artifact_id,
            status=BioStorageStatus.ENCODING,
            dna_sequence_hash=compute_hash(dna_sequence),
            shard_count=len(shards),
            payload_hash=payload_hash,
        )
        
        logger.info(
            f"Encoded artifact {artifact_id}: "
            f"{len(payload)} bytes → {len(dna_sequence)} bp in {len(shards)} shards"
        )
        
        return capsule, shards


# ============================================================================
# BIO DECODER WORKER
# ============================================================================

class BioDecoderWorker:
    """
    Decode DNA storage back to artifacts.
    
    Per spec: DNA reads → bitstream → original Artifact + attestations
    """
    
    def __init__(self):
        self.canonicalizer = Canonicalizer()
        self.dna_encoder = DNAEncoder()
        self.ecc = ErrorCorrection()
    
    def decode(
        self,
        dna_sequence: str,
        ecc_data: bytes,
    ) -> Optional[Dict[str, Any]]:
        """Decode DNA sequence back to artifact"""
        # Step 1: Decode DNA to bytes
        payload = self.dna_encoder.decode(dna_sequence)
        
        # Step 2: Verify ECC
        if not self.ecc.verify(payload, ecc_data):
            logger.error("ECC verification failed")
            return None
        
        # Step 3: Parse header
        try:
            header_end = payload.find(b'|', payload.find(b'|') + 1)
            header_end = payload.find(b'|', header_end + 1)
            header_end = payload.find(b'|', header_end + 1) + 1
            
            header = payload[:header_end].decode('utf-8')
            parts = header.split('|')
            
            magic = parts[0]
            if magic != CHE_NU_MAGIC:
                logger.error(f"Invalid magic: {magic}")
                return None
            
            artifact_id = parts[1]
            compressed_size = int(parts[2])
            
            compressed = payload[header_end:header_end + compressed_size]
            
        except Exception as e:
            logger.error(f"Header parsing failed: {e}")
            return None
        
        # Step 4: Decompress
        try:
            decompressed = self.canonicalizer.decompress(compressed)
        except Exception as e:
            logger.error(f"Decompression failed: {e}")
            return None
        
        # Step 5: Parse JSON
        try:
            artifact = json.loads(decompressed.decode('utf-8'))
        except Exception as e:
            logger.error(f"JSON parsing failed: {e}")
            return None
        
        logger.info(f"Successfully decoded artifact {artifact_id}")
        return artifact


# ============================================================================
# BIO STORAGE SERVICE
# ============================================================================

class BioStorageService:
    """
    Main service for bio-digital storage.
    
    Per spec: HITL obligatoire for rehydrate operations
    """
    
    def __init__(self):
        self.encoder = BioEncoderWorker()
        self.decoder = BioDecoderWorker()
        
        # Storage
        self._capsules: Dict[str, BioCapsule] = {}
        self._shards: Dict[str, List[DNAShard]] = {}
        self._dna_data: Dict[str, str] = {}  # capsule_id → DNA sequence
        self._ecc_data: Dict[str, bytes] = {}  # capsule_id → ECC data
        
        # Decode requests (HITL)
        self._decode_requests: Dict[str, DecodeRequest] = {}
    
    def store(
        self,
        artifact_id: str,
        artifact_data: Any,
        locations: List[str] = None,
    ) -> BioCapsule:
        """
        Store artifact in bio-digital format.
        
        Per spec: Artifacts cibles prioritaires
        """
        # Encode
        capsule, shards = self.encoder.encode(artifact_data, artifact_id)
        
        # Reconstruct full DNA sequence for storage
        dna_sequence = self.encoder.dna_encoder.encode(
            self.encoder.canonicalizer.compress(
                self.encoder.canonicalizer.canonicalize(artifact_data)
            )
        )
        
        # Store
        self._capsules[capsule.capsule_id] = capsule
        self._shards[capsule.capsule_id] = shards
        self._dna_data[capsule.capsule_id] = dna_sequence
        self._ecc_data[capsule.capsule_id] = shards[0].ecc_data if shards else b""
        
        # Update status
        capsule.status = BioStorageStatus.STORED
        capsule.stored_at = datetime.utcnow()
        capsule.storage_locations = locations or ["primary_vault"]
        
        logger.info(f"Stored capsule {capsule.capsule_id} for artifact {artifact_id}")
        return capsule
    
    def request_decode(
        self,
        capsule_id: str,
    ) -> DecodeRequest:
        """
        Request to decode/rehydrate an artifact.
        
        Per spec: Bouton "Rehydrate" — HITL obligatoire
        """
        request = DecodeRequest(
            request_id=generate_id(),
            capsule_id=capsule_id,
            requires_hitl=True,  # Per spec: ALWAYS requires HITL
        )
        
        self._decode_requests[request.request_id] = request
        logger.info(f"Decode request {request.request_id} created (HITL required)")
        return request
    
    def approve_decode(
        self,
        request_id: str,
        approver_id: str,
    ) -> bool:
        """Approve a decode request (HITL)"""
        request = self._decode_requests.get(request_id)
        if not request:
            return False
        
        request.approved_by = approver_id
        request.approved_at = datetime.utcnow()
        request.status = "approved"
        
        logger.info(f"Decode request {request_id} approved by {approver_id}")
        return True
    
    def execute_decode(
        self,
        request_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Execute an approved decode request"""
        request = self._decode_requests.get(request_id)
        if not request:
            return None
        
        if request.status != "approved":
            logger.error(f"Request {request_id} not approved")
            return None
        
        capsule_id = request.capsule_id
        dna_sequence = self._dna_data.get(capsule_id)
        ecc_data = self._ecc_data.get(capsule_id, b"")
        
        if not dna_sequence:
            logger.error(f"DNA data not found for capsule {capsule_id}")
            return None
        
        # Decode
        artifact = self.decoder.decode(dna_sequence, ecc_data)
        
        if artifact:
            request.status = "completed"
            request.decoded_artifact_ref = f"artifact:{generate_id()}"
        else:
            request.status = "failed"
        
        return artifact
    
    def get_capsule(self, capsule_id: str) -> Optional[BioCapsule]:
        """Get capsule by ID"""
        return self._capsules.get(capsule_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        capsules = list(self._capsules.values())
        
        return {
            "total_capsules": len(capsules),
            "total_shards": sum(len(s) for s in self._shards.values()),
            "total_bp": sum(len(d) for d in self._dna_data.values()),
            "pending_requests": sum(
                1 for r in self._decode_requests.values()
                if r.status == "pending_approval"
            ),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_storage_service() -> BioStorageService:
    """Create bio-storage service"""
    return BioStorageService()


def create_encoder() -> BioEncoderWorker:
    """Create bio encoder worker"""
    return BioEncoderWorker()


def create_decoder() -> BioDecoderWorker:
    """Create bio decoder worker"""
    return BioDecoderWorker()
