"""
============================================================================
CHE·NU™ V69 — POST-QUANTUM SECURITY
============================================================================
Spec: GPT1/CHE-NU_POST_QUANTUM_SECURITY.md

Purpose: Prepare CHE·NU™ for the post-quantum cryptography era.

Algorithms:
- CRYSTALS-Dilithium
- Falcon
- Hybrid (Ed25519 + PQ)

Integration:
- XR packs signed twice (classical + PQ)
- Audit logs protected long-term
- Configurable per client sensitivity
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    Signature,
    SignatureAlgorithm,
    SecurityLevel,
    KeyPair,
    generate_id,
    compute_sha256,
    mock_pq_sign,
    mock_pq_verify,
)

logger = logging.getLogger(__name__)


# ============================================================================
# KEY MANAGER
# ============================================================================

class KeyManager:
    """
    Manage cryptographic key pairs.
    
    Per spec: Configurable per client sensitivity
    """
    
    def __init__(self):
        self._keys: Dict[str, KeyPair] = {}
        self._default_algorithm = SignatureAlgorithm.HYBRID
    
    def generate_key_pair(
        self,
        algorithm: SignatureAlgorithm,
        expires_days: int = 365,
    ) -> KeyPair:
        """Generate a new key pair"""
        key_id = generate_id()
        
        # Mock key generation (in production: use actual crypto)
        public_key = f"pub_{algorithm.value}_{key_id[:8]}"
        private_ref = f"priv_{algorithm.value}_{key_id[:8]}"
        
        key_pair = KeyPair(
            key_id=key_id,
            algorithm=algorithm,
            public_key=public_key,
            private_key_ref=private_ref,
            expires_at=datetime.utcnow() + timedelta(days=expires_days),
        )
        
        self._keys[key_id] = key_pair
        logger.info(f"Generated {algorithm.value} key pair: {key_id}")
        return key_pair
    
    def get_key(self, key_id: str) -> Optional[KeyPair]:
        """Get key pair by ID"""
        return self._keys.get(key_id)
    
    def get_keys_by_algorithm(
        self,
        algorithm: SignatureAlgorithm,
    ) -> List[KeyPair]:
        """Get all keys for an algorithm"""
        return [k for k in self._keys.values() if k.algorithm == algorithm]
    
    def is_key_valid(self, key_id: str) -> bool:
        """Check if key is still valid"""
        key = self._keys.get(key_id)
        if not key:
            return False
        if key.expires_at and key.expires_at < datetime.utcnow():
            return False
        return True


# ============================================================================
# SIGNATURE SERVICE
# ============================================================================

class SignatureService:
    """
    Create and verify cryptographic signatures.
    
    Per spec algorithms: CRYSTALS-Dilithium, Falcon, Hybrid
    """
    
    def __init__(self, key_manager: KeyManager):
        self.keys = key_manager
    
    def sign(
        self,
        data: Any,
        key_id: str,
    ) -> Signature:
        """Sign data with specified key"""
        key = self.keys.get_key(key_id)
        if not key:
            raise ValueError(f"Key {key_id} not found")
        
        if not self.keys.is_key_valid(key_id):
            raise ValueError(f"Key {key_id} has expired")
        
        # Serialize data
        data_str = str(data) if not isinstance(data, str) else data
        
        # Create signature based on algorithm
        if key.algorithm == SignatureAlgorithm.HYBRID:
            # Sign with both classical and PQ
            classical_sig = mock_pq_sign(data_str, SignatureAlgorithm.ED25519)
            pq_sig = mock_pq_sign(data_str, SignatureAlgorithm.DILITHIUM)
            combined_sig = f"{classical_sig}:{pq_sig}"
            
            signature = Signature(
                signature_id=generate_id(),
                algorithm=SignatureAlgorithm.HYBRID,
                signature_bytes=combined_sig,
                public_key_ref=key.public_key,
                classical_signature=classical_sig,
                pq_signature=pq_sig,
            )
        else:
            sig_bytes = mock_pq_sign(data_str, key.algorithm)
            
            signature = Signature(
                signature_id=generate_id(),
                algorithm=key.algorithm,
                signature_bytes=sig_bytes,
                public_key_ref=key.public_key,
            )
        
        logger.info(f"Signed with {key.algorithm.value}: {signature.signature_id}")
        return signature
    
    def verify(
        self,
        data: Any,
        signature: Signature,
    ) -> bool:
        """Verify signature"""
        data_str = str(data) if not isinstance(data, str) else data
        
        if signature.algorithm == SignatureAlgorithm.HYBRID:
            # Verify both signatures
            classical_valid = mock_pq_verify(
                data_str,
                signature.classical_signature,
                SignatureAlgorithm.ED25519,
            )
            pq_valid = mock_pq_verify(
                data_str,
                signature.pq_signature,
                SignatureAlgorithm.DILITHIUM,
            )
            return classical_valid and pq_valid
        else:
            return mock_pq_verify(
                data_str,
                signature.signature_bytes,
                signature.algorithm,
            )
    
    def sign_xr_pack(
        self,
        xr_data: Dict[str, Any],
        classical_key_id: str,
        pq_key_id: str,
    ) -> Tuple[Signature, Signature]:
        """
        Sign XR pack with both classical and PQ.
        
        Per spec: XR packs signed twice (classical + PQ)
        """
        classical_sig = self.sign(xr_data, classical_key_id)
        pq_sig = self.sign(xr_data, pq_key_id)
        
        return classical_sig, pq_sig


# ============================================================================
# SECURITY CONFIGURATOR
# ============================================================================

class SecurityConfigurator:
    """
    Configure security level per client.
    
    Per spec: Configurable per client sensitivity
    """
    
    def __init__(self):
        self._client_configs: Dict[str, SecurityLevel] = {}
        self._default_level = SecurityLevel.HIGH
    
    def set_client_level(
        self,
        client_id: str,
        level: SecurityLevel,
    ) -> None:
        """Set security level for a client"""
        self._client_configs[client_id] = level
        logger.info(f"Set security level for {client_id}: {level.value}")
    
    def get_client_level(self, client_id: str) -> SecurityLevel:
        """Get security level for a client"""
        return self._client_configs.get(client_id, self._default_level)
    
    def get_recommended_algorithm(
        self,
        client_id: str,
    ) -> SignatureAlgorithm:
        """Get recommended algorithm for client"""
        level = self.get_client_level(client_id)
        
        if level == SecurityLevel.STANDARD:
            return SignatureAlgorithm.ED25519
        elif level == SecurityLevel.HIGH:
            return SignatureAlgorithm.HYBRID
        else:  # QUANTUM_SAFE
            return SignatureAlgorithm.DILITHIUM


# ============================================================================
# POST-QUANTUM SECURITY SYSTEM
# ============================================================================

class PostQuantumSecuritySystem:
    """
    Main post-quantum security system.
    
    Per spec value: Future-proof security, Strong defense-sector positioning
    """
    
    def __init__(self):
        self.keys = KeyManager()
        self.signatures = SignatureService(self.keys)
        self.config = SecurityConfigurator()
        
        # Generate default keys
        self._setup_default_keys()
    
    def _setup_default_keys(self) -> None:
        """Setup default key pairs"""
        self.keys.generate_key_pair(SignatureAlgorithm.ED25519)
        self.keys.generate_key_pair(SignatureAlgorithm.DILITHIUM)
        self.keys.generate_key_pair(SignatureAlgorithm.FALCON)
        self.keys.generate_key_pair(SignatureAlgorithm.HYBRID)
    
    def sign_artifact(
        self,
        artifact_data: Dict[str, Any],
        client_id: str,
    ) -> Signature:
        """Sign artifact with appropriate algorithm for client"""
        algorithm = self.config.get_recommended_algorithm(client_id)
        
        # Get or generate key
        keys = self.keys.get_keys_by_algorithm(algorithm)
        if not keys:
            key = self.keys.generate_key_pair(algorithm)
        else:
            key = keys[0]
        
        return self.signatures.sign(artifact_data, key.key_id)
    
    def verify_artifact(
        self,
        artifact_data: Dict[str, Any],
        signature: Signature,
    ) -> bool:
        """Verify artifact signature"""
        return self.signatures.verify(artifact_data, signature)
    
    def protect_audit_log(
        self,
        audit_data: Dict[str, Any],
    ) -> Signature:
        """
        Protect audit log with PQ signature.
        
        Per spec: Audit logs protected long-term
        """
        # Use Dilithium for long-term protection
        keys = self.keys.get_keys_by_algorithm(SignatureAlgorithm.DILITHIUM)
        if not keys:
            key = self.keys.generate_key_pair(SignatureAlgorithm.DILITHIUM)
        else:
            key = keys[0]
        
        return self.signatures.sign(audit_data, key.key_id)
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get security status"""
        return {
            "total_keys": len(self.keys._keys),
            "algorithms_available": [a.value for a in SignatureAlgorithm],
            "default_level": self.config._default_level.value,
            "pq_ready": True,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_security_system() -> PostQuantumSecuritySystem:
    """Create post-quantum security system"""
    return PostQuantumSecuritySystem()


def create_key_manager() -> KeyManager:
    """Create key manager"""
    return KeyManager()
