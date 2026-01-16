"""
============================================================================
CHE·NU™ V69 — XR BLOCKCHAIN VERIFICATION LAYER
============================================================================
Spec: GPT1/CHE-NU_XR_BLOCKCHAIN_VERIFICATION.md

Purpose: Guarantee the integrity of XR visualizations.

Core Concept: Each XR frame/chunk is cryptographically anchored using
a lightweight blockchain or ledger.

Capabilities:
- Frame-level integrity proofs
- Post-render tamper detection
- Verifiable replay history

Integration:
- Hash XR chunks
- Anchor Merkle roots to ledger
- XR client verifies before rendering

Value: Investor-grade trust, Common Operating Picture
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    XRChunk,
    XRIntegrityProof,
    MerkleTree,
    MerkleNode,
    generate_id,
    compute_sha256,
    compute_merkle_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# LIGHTWEIGHT LEDGER
# ============================================================================

@dataclass
class LedgerBlock:
    """A block in the lightweight ledger"""
    block_id: str
    block_number: int
    
    # Content
    merkle_root: str
    session_id: str
    chunk_count: int
    
    # Chain
    previous_hash: str
    block_hash: str
    
    # Timestamp
    timestamp: datetime = field(default_factory=datetime.utcnow)


class LightweightLedger:
    """
    A lightweight blockchain for XR integrity.
    
    Per spec: Lightweight blockchain or ledger
    """
    
    def __init__(self):
        self._blocks: List[LedgerBlock] = []
        self._genesis_hash = compute_sha256("CHE-NU-XR-GENESIS")
    
    def add_block(
        self,
        merkle_root: str,
        session_id: str,
        chunk_count: int,
    ) -> LedgerBlock:
        """Add a new block to the ledger"""
        block_number = len(self._blocks)
        previous_hash = (
            self._blocks[-1].block_hash
            if self._blocks
            else self._genesis_hash
        )
        
        block = LedgerBlock(
            block_id=generate_id(),
            block_number=block_number,
            merkle_root=merkle_root,
            session_id=session_id,
            chunk_count=chunk_count,
            previous_hash=previous_hash,
            block_hash="",  # Will compute
        )
        
        # Compute block hash
        block.block_hash = compute_sha256({
            "number": block.block_number,
            "root": block.merkle_root,
            "session": block.session_id,
            "previous": block.previous_hash,
            "timestamp": block.timestamp.isoformat(),
        })
        
        self._blocks.append(block)
        logger.info(f"Added ledger block {block.block_number}: {block.block_hash[:16]}...")
        return block
    
    def get_block(self, block_number: int) -> Optional[LedgerBlock]:
        """Get block by number"""
        if 0 <= block_number < len(self._blocks):
            return self._blocks[block_number]
        return None
    
    def verify_chain(self) -> bool:
        """Verify the entire chain integrity"""
        if not self._blocks:
            return True
        
        # Check first block
        if self._blocks[0].previous_hash != self._genesis_hash:
            return False
        
        # Check chain
        for i in range(1, len(self._blocks)):
            if self._blocks[i].previous_hash != self._blocks[i-1].block_hash:
                return False
        
        return True
    
    def get_chain_length(self) -> int:
        """Get chain length"""
        return len(self._blocks)


# ============================================================================
# XR CHUNK HASHER
# ============================================================================

class XRChunkHasher:
    """
    Hash XR chunks for integrity.
    
    Per spec: Hash XR chunks
    """
    
    def hash_chunk(
        self,
        frame_number: int,
        content: Dict[str, Any],
    ) -> XRChunk:
        """Hash an XR chunk"""
        content_hash = compute_sha256({
            "frame": frame_number,
            "content": content,
        })
        
        chunk = XRChunk(
            chunk_id=generate_id(),
            frame_number=frame_number,
            content_hash=content_hash,
        )
        
        return chunk
    
    def hash_frame_sequence(
        self,
        frames: List[Dict[str, Any]],
    ) -> List[XRChunk]:
        """Hash a sequence of frames"""
        chunks = []
        for i, frame in enumerate(frames):
            chunk = self.hash_chunk(i, frame)
            chunks.append(chunk)
        return chunks


# ============================================================================
# XR INTEGRITY VERIFIER
# ============================================================================

class XRIntegrityVerifier:
    """
    Verify XR visualization integrity.
    
    Per spec capabilities:
    - Frame-level integrity proofs
    - Post-render tamper detection
    - Verifiable replay history
    """
    
    def __init__(self, ledger: LightweightLedger):
        self.ledger = ledger
        self._proofs: Dict[str, XRIntegrityProof] = {}
    
    def create_proof(
        self,
        session_id: str,
        chunks: List[XRChunk],
    ) -> XRIntegrityProof:
        """
        Create integrity proof for XR session.
        
        Per spec: Frame-level integrity proofs
        """
        # Build Merkle tree from chunks
        chunk_hashes = [c.content_hash for c in chunks]
        merkle_root = self._build_merkle_root(chunk_hashes)
        
        # Anchor to ledger
        block = self.ledger.add_block(
            merkle_root=merkle_root,
            session_id=session_id,
            chunk_count=len(chunks),
        )
        
        proof = XRIntegrityProof(
            proof_id=generate_id(),
            session_id=session_id,
            chunk_hashes=chunk_hashes,
            merkle_root=merkle_root,
            anchored_at=datetime.utcnow(),
            ledger_ref=block.block_id,
        )
        
        # Sign proof
        proof.signature = compute_sha256({
            "proof_id": proof.proof_id,
            "root": proof.merkle_root,
            "ledger": proof.ledger_ref,
        })
        
        self._proofs[session_id] = proof
        
        logger.info(f"Created XR integrity proof for session {session_id}")
        return proof
    
    def _build_merkle_root(self, hashes: List[str]) -> str:
        """Build Merkle root from hashes"""
        if not hashes:
            return compute_sha256("empty")
        
        if len(hashes) == 1:
            return hashes[0]
        
        # Pad to power of 2
        while len(hashes) & (len(hashes) - 1) != 0:
            hashes.append(compute_sha256("padding"))
        
        # Build tree
        while len(hashes) > 1:
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = compute_merkle_hash(hashes[i], hashes[i+1])
                new_level.append(combined)
            hashes = new_level
        
        return hashes[0]
    
    def verify_chunk(
        self,
        session_id: str,
        chunk: XRChunk,
    ) -> bool:
        """
        Verify a single chunk.
        
        Per spec: XR client verifies before rendering
        """
        proof = self._proofs.get(session_id)
        if not proof:
            return False
        
        # Check if chunk hash is in proof
        return chunk.content_hash in proof.chunk_hashes
    
    def detect_tamper(
        self,
        session_id: str,
        rendered_chunks: List[XRChunk],
    ) -> List[int]:
        """
        Detect tampered frames.
        
        Per spec: Post-render tamper detection
        """
        proof = self._proofs.get(session_id)
        if not proof:
            return list(range(len(rendered_chunks)))  # All suspect
        
        tampered = []
        for chunk in rendered_chunks:
            if chunk.content_hash not in proof.chunk_hashes:
                tampered.append(chunk.frame_number)
        
        if tampered:
            logger.warning(f"Tamper detected in frames: {tampered}")
        
        return tampered
    
    def verify_replay(
        self,
        session_id: str,
        replay_chunks: List[XRChunk],
    ) -> Tuple[bool, str]:
        """
        Verify replay history.
        
        Per spec: Verifiable replay history
        """
        proof = self._proofs.get(session_id)
        if not proof:
            return False, "No proof found for session"
        
        # Check all chunks match
        replay_hashes = [c.content_hash for c in replay_chunks]
        
        if set(replay_hashes) != set(proof.chunk_hashes):
            return False, "Chunk hashes do not match"
        
        # Verify order
        if replay_hashes != proof.chunk_hashes:
            return False, "Chunk order does not match"
        
        # Verify Merkle root
        computed_root = self._build_merkle_root(replay_hashes)
        if computed_root != proof.merkle_root:
            return False, "Merkle root mismatch"
        
        return True, "Replay verified"


# ============================================================================
# XR BLOCKCHAIN VERIFICATION SYSTEM
# ============================================================================

class XRBlockchainVerificationSystem:
    """
    Main XR blockchain verification system.
    
    Per spec value: Investor-grade trust, Common Operating Picture,
    Differentiation vs traditional XR dashboards
    """
    
    def __init__(self):
        self.ledger = LightweightLedger()
        self.hasher = XRChunkHasher()
        self.verifier = XRIntegrityVerifier(self.ledger)
    
    def process_xr_session(
        self,
        session_id: str,
        frames: List[Dict[str, Any]],
    ) -> XRIntegrityProof:
        """Process an XR session and create integrity proof"""
        # Hash all frames
        chunks = self.hasher.hash_frame_sequence(frames)
        
        # Create proof and anchor
        proof = self.verifier.create_proof(session_id, chunks)
        
        return proof
    
    def verify_before_render(
        self,
        session_id: str,
        frame_number: int,
        content: Dict[str, Any],
    ) -> bool:
        """
        Verify frame before rendering.
        
        Per spec: XR client verifies before rendering
        """
        chunk = self.hasher.hash_chunk(frame_number, content)
        return self.verifier.verify_chunk(session_id, chunk)
    
    def verify_replay(
        self,
        session_id: str,
        frames: List[Dict[str, Any]],
    ) -> Tuple[bool, str]:
        """Verify a replay session"""
        chunks = self.hasher.hash_frame_sequence(frames)
        return self.verifier.verify_replay(session_id, chunks)
    
    def get_ledger_status(self) -> Dict[str, Any]:
        """Get ledger status"""
        return {
            "chain_length": self.ledger.get_chain_length(),
            "chain_valid": self.ledger.verify_chain(),
            "genesis_hash": self.ledger._genesis_hash[:16] + "...",
        }
    
    def export_proof(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Export proof for external verification"""
        proof = self.verifier._proofs.get(session_id)
        if not proof:
            return None
        
        return {
            "proof_id": proof.proof_id,
            "session_id": proof.session_id,
            "merkle_root": proof.merkle_root,
            "chunk_count": len(proof.chunk_hashes),
            "ledger_ref": proof.ledger_ref,
            "anchored_at": proof.anchored_at.isoformat() if proof.anchored_at else None,
            "signature": proof.signature,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_xr_verification_system() -> XRBlockchainVerificationSystem:
    """Create XR blockchain verification system"""
    return XRBlockchainVerificationSystem()


def create_ledger() -> LightweightLedger:
    """Create lightweight ledger"""
    return LightweightLedger()
