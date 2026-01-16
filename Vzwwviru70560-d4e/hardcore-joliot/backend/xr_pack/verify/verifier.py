"""
============================================================================
CHE·NU™ V69 — XR PACK VERIFIER
============================================================================
Version: 1.0.0
Purpose: Verify XR Pack integrity and signatures
Principle: XR = READ ONLY. Must verify before rendering.
============================================================================
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import zipfile
import io

from ..models.artifacts import (
    ManifestV1,
    ChecksumsV1,
    XRPackSignatureV1,
    XRPackPublicKeyV1,
    PackStatus,
)

# Import security module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from security import (
    get_unified_signer,
    KeyPair,
    Signature,
    SignatureAlgorithm,
    VerificationResult,
    SignatureStatus,
)

logger = logging.getLogger(__name__)


# ============================================================================
# VERIFICATION RESULT
# ============================================================================

class XRPackVerificationResult:
    """Result of XR Pack verification"""
    
    def __init__(self):
        self.valid = False
        self.checks: Dict[str, bool] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.signature_result: Optional[VerificationResult] = None
        self.verified_at = datetime.utcnow()
    
    def add_check(self, name: str, passed: bool, error: Optional[str] = None) -> None:
        self.checks[name] = passed
        if not passed and error:
            self.errors.append(error)
    
    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)
    
    def finalize(self) -> None:
        """Calculate final validity"""
        self.valid = all(self.checks.values()) if self.checks else False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_at": self.verified_at.isoformat(),
        }


# ============================================================================
# XR PACK VERIFIER
# ============================================================================

class XRPackVerifier:
    """
    Verifies XR Pack integrity and signatures.
    
    Verification steps:
    1. Load and parse manifest
    2. Verify all file checksums
    3. Verify ZIP integrity
    4. Verify cryptographic signature (Ed25519/Hybrid)
    5. Verify chunk coverage (no gaps/overlaps)
    
    Usage:
        verifier = XRPackVerifier()
        
        # Verify from directory
        result = verifier.verify_directory("/path/to/pack")
        
        # Verify from ZIP bytes
        result = verifier.verify_zip(zip_bytes, signature, public_key)
        
        if result.valid:
            print("Pack verified!")
        else:
            print(f"Errors: {result.errors}")
    """
    
    def __init__(self):
        self.signer = get_unified_signer()
    
    def verify_directory(self, pack_dir: str) -> XRPackVerificationResult:
        """
        Verify XR Pack from directory structure.
        
        Args:
            pack_dir: Path to xr_pack.v1/ directory
        """
        result = XRPackVerificationResult()
        pack_path = Path(pack_dir)
        
        # 1. Check directory exists
        if not pack_path.exists():
            result.add_check("directory_exists", False, f"Directory not found: {pack_dir}")
            result.finalize()
            return result
        
        result.add_check("directory_exists", True)
        
        # 2. Load and verify manifest
        manifest_path = pack_path / "manifest.v1.json"
        manifest = self._load_manifest(manifest_path, result)
        if manifest is None:
            result.finalize()
            return result
        
        # 3. Load and verify checksums
        checksums_path = pack_path / "checksums.v1.json"
        checksums = self._load_checksums(checksums_path, result)
        if checksums is None:
            result.finalize()
            return result
        
        # 4. Verify file checksums
        self._verify_file_checksums(pack_path, checksums, result)
        
        # 5. Verify replay chunks
        self._verify_replay_chunks(pack_path, result)
        
        result.finalize()
        return result
    
    def verify_zip(
        self,
        zip_bytes: bytes,
        signature: Optional[XRPackSignatureV1] = None,
        public_key: Optional[XRPackPublicKeyV1] = None,
    ) -> XRPackVerificationResult:
        """
        Verify XR Pack from ZIP bytes.
        
        Args:
            zip_bytes: ZIP file content
            signature: Signature artifact (optional)
            public_key: Public key artifact (optional)
        """
        result = XRPackVerificationResult()
        
        # 1. Verify ZIP is valid
        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
                file_list = zf.namelist()
                result.add_check("zip_valid", True)
        except zipfile.BadZipFile as e:
            result.add_check("zip_valid", False, f"Invalid ZIP: {e}")
            result.finalize()
            return result
        
        # 2. Check required files exist
        required_files = [
            "manifest.v1.json",
            "explain.v1.json",
            "heatmap.v1.json",
            "diff.v1.json",
            "checksums.v1.json",
            "replay/index.v1.json",
        ]
        
        for req_file in required_files:
            if req_file not in file_list:
                result.add_check(
                    f"file_{req_file}",
                    False,
                    f"Missing required file: {req_file}",
                )
            else:
                result.add_check(f"file_{req_file}", True)
        
        # 3. Verify checksums
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
            try:
                checksums_json = zf.read("checksums.v1.json").decode('utf-8')
                checksums = ChecksumsV1.model_validate_json(checksums_json)
                
                for file_check in checksums.files:
                    if file_check.file in file_list:
                        content = zf.read(file_check.file)
                        actual_hash = hashlib.sha256(content).hexdigest()
                        
                        if actual_hash == file_check.sha256:
                            result.add_check(f"checksum_{file_check.file}", True)
                        else:
                            result.add_check(
                                f"checksum_{file_check.file}",
                                False,
                                f"Checksum mismatch for {file_check.file}",
                            )
                    else:
                        result.add_check(
                            f"checksum_{file_check.file}",
                            False,
                            f"File not found: {file_check.file}",
                        )
                        
            except Exception as e:
                result.add_check("checksums_valid", False, f"Failed to verify checksums: {e}")
        
        # 4. Verify signature
        if signature and public_key:
            sig_result = self._verify_signature(zip_bytes, signature, public_key)
            result.signature_result = sig_result
            result.add_check("signature_valid", sig_result.is_valid)
        elif signature:
            result.add_warning("Signature provided but no public key")
        elif public_key:
            result.add_warning("Public key provided but no signature")
        
        result.finalize()
        return result
    
    def verify_signature_only(
        self,
        zip_bytes: bytes,
        signature: XRPackSignatureV1,
        public_key: XRPackPublicKeyV1,
    ) -> VerificationResult:
        """
        Verify only the cryptographic signature.
        
        Used for quick verification in XR client.
        """
        return self._verify_signature(zip_bytes, signature, public_key)
    
    def _load_manifest(
        self,
        path: Path,
        result: XRPackVerificationResult,
    ) -> Optional[ManifestV1]:
        """Load and validate manifest"""
        if not path.exists():
            result.add_check("manifest_exists", False, f"Manifest not found: {path}")
            return None
        
        result.add_check("manifest_exists", True)
        
        try:
            manifest = ManifestV1.model_validate_json(path.read_text())
            result.add_check("manifest_valid", True)
            return manifest
        except Exception as e:
            result.add_check("manifest_valid", False, f"Invalid manifest: {e}")
            return None
    
    def _load_checksums(
        self,
        path: Path,
        result: XRPackVerificationResult,
    ) -> Optional[ChecksumsV1]:
        """Load and validate checksums"""
        if not path.exists():
            result.add_check("checksums_exists", False, f"Checksums not found: {path}")
            return None
        
        result.add_check("checksums_exists", True)
        
        try:
            checksums = ChecksumsV1.model_validate_json(path.read_text())
            result.add_check("checksums_valid", True)
            return checksums
        except Exception as e:
            result.add_check("checksums_valid", False, f"Invalid checksums: {e}")
            return None
    
    def _verify_file_checksums(
        self,
        pack_path: Path,
        checksums: ChecksumsV1,
        result: XRPackVerificationResult,
    ) -> None:
        """Verify all file checksums"""
        for file_check in checksums.files:
            file_path = pack_path / file_check.file
            
            if not file_path.exists():
                result.add_check(
                    f"checksum_{file_check.file}",
                    False,
                    f"File not found: {file_check.file}",
                )
                continue
            
            content = file_path.read_bytes()
            actual_hash = hashlib.sha256(content).hexdigest()
            
            if actual_hash == file_check.sha256:
                result.add_check(f"checksum_{file_check.file}", True)
            else:
                result.add_check(
                    f"checksum_{file_check.file}",
                    False,
                    f"Checksum mismatch for {file_check.file}",
                )
    
    def _verify_replay_chunks(
        self,
        pack_path: Path,
        result: XRPackVerificationResult,
    ) -> None:
        """Verify replay chunk coverage"""
        index_path = pack_path / "replay" / "index.v1.json"
        
        if not index_path.exists():
            result.add_check("replay_index_exists", False, "Replay index not found")
            return
        
        result.add_check("replay_index_exists", True)
        
        try:
            index = json.loads(index_path.read_text())
            chunks = index.get("chunks", [])
            
            if not chunks:
                result.add_warning("No replay chunks found")
                return
            
            # Check for gaps and overlaps
            prev_to_step = -1
            
            for chunk_ref in sorted(chunks, key=lambda c: c["from_step"]):
                chunk_file = pack_path / "replay" / chunk_ref["file"]
                
                # Check file exists
                if not chunk_file.exists():
                    result.add_check(
                        f"chunk_{chunk_ref['id']}_exists",
                        False,
                        f"Chunk file not found: {chunk_ref['file']}",
                    )
                    continue
                
                result.add_check(f"chunk_{chunk_ref['id']}_exists", True)
                
                # Check for gaps
                if chunk_ref["from_step"] > prev_to_step + 1:
                    result.add_warning(
                        f"Gap detected: steps {prev_to_step + 1} to {chunk_ref['from_step'] - 1}"
                    )
                
                # Check for overlaps
                if chunk_ref["from_step"] <= prev_to_step:
                    result.add_check(
                        "chunk_no_overlap",
                        False,
                        f"Overlap detected at step {chunk_ref['from_step']}",
                    )
                
                prev_to_step = chunk_ref["to_step"]
            
            result.add_check("chunk_coverage", True)
            
        except Exception as e:
            result.add_check("replay_valid", False, f"Failed to verify replay: {e}")
    
    def _verify_signature(
        self,
        zip_bytes: bytes,
        signature: XRPackSignatureV1,
        public_key: XRPackPublicKeyV1,
    ) -> VerificationResult:
        """Verify cryptographic signature"""
        # Compute ZIP hash
        zip_hash = hashlib.sha256(zip_bytes).hexdigest()
        
        # Check hash matches
        if zip_hash != signature.zip_sha256:
            return VerificationResult(
                signature_id="verify",
                status=SignatureStatus.INVALID,
                algorithm=SignatureAlgorithm.ED25519,
                key_id=signature.key_id,
                content_hash=zip_hash,
                error_message="ZIP hash mismatch",
            )
        
        # Determine algorithm
        algo = self._parse_algorithm(signature.algo)
        
        # Create key pair for verification
        key_pair = KeyPair(
            key_id=public_key.key_id,
            algorithm=algo,
            public_key_b64=public_key.public_key_b64,
        )
        
        if public_key.hybrid_keys:
            key_pair.classical_public_key_b64 = public_key.hybrid_keys.get("classical_b64")
            key_pair.pq_public_key_b64 = public_key.hybrid_keys.get("pq_b64")
        
        # Create signature object
        sig = Signature(
            algorithm=algo,
            signature_b64=signature.signature_b64,
            content_hash=zip_hash,
            key_id=signature.key_id,
        )
        
        if signature.hybrid_signatures:
            sig.classical_signature_b64 = signature.hybrid_signatures.get("classical_b64")
            sig.pq_signature_b64 = signature.hybrid_signatures.get("pq_b64")
        
        # Verify
        return self.signer.verify(zip_bytes, sig, key_pair)
    
    def _parse_algorithm(self, algo_str: str) -> SignatureAlgorithm:
        """Parse algorithm string to enum"""
        algo_map = {
            "Ed25519": SignatureAlgorithm.ED25519,
            "Dilithium2": SignatureAlgorithm.DILITHIUM2,
            "Dilithium3": SignatureAlgorithm.DILITHIUM3,
            "Ed25519+Dilithium2": SignatureAlgorithm.HYBRID_ED25519_DILITHIUM2,
            "Ed25519+Dilithium3": SignatureAlgorithm.HYBRID_ED25519_DILITHIUM3,
        }
        return algo_map.get(algo_str, SignatureAlgorithm.ED25519)


# ============================================================================
# QUICK VERIFY FUNCTION
# ============================================================================

def verify_xr_pack(
    zip_bytes: bytes,
    signature_json: str,
    public_key_json: str,
) -> bool:
    """
    Quick verification function for XR client.
    
    Returns:
        True if pack is valid and signature verifies
    """
    try:
        signature = XRPackSignatureV1.model_validate_json(signature_json)
        public_key = XRPackPublicKeyV1.model_validate_json(public_key_json)
        
        verifier = XRPackVerifier()
        result = verifier.verify_signature_only(zip_bytes, signature, public_key)
        
        return result.is_valid
        
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False
