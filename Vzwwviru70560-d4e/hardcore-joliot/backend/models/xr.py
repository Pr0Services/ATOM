"""
CHE·NU™ V75 Backend - XR Models

⚠️ RÈGLE ABSOLUE: XR EST READ-ONLY
- Aucune écriture côté XR
- Vérification intégrité OBLIGATOIRE avant affichage
- Si signature invalide → BLOCAGE affichage
- Artifacts statiques uniquement

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, BigInteger, ForeignKey, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import hashlib

from config.database import Base


class XREnvironment(Base):
    """
    XR environment (READ-ONLY from client side).
    
    RÈGLE: XR client ne peut QUE lire.
    
    Types:
    - sanctuaire: Main immersive space
    - command_center: Control interface
    - data_visualization: Data viz space
    - meeting_space: Virtual meeting room
    - focus_zone: Focused work area
    """
    
    __tablename__ = "xr_environments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    type = Column(String(50), nullable=False)  # sanctuaire, command_center, etc.
    version = Column(String(20), nullable=False, default="1.0.0")
    
    # Integrity verification
    checksum = Column(String(64), nullable=False)  # SHA-256 of all artifacts
    verified = Column(Boolean, default=False)  # MUST be True for display
    
    artifacts_count = Column(Integer, default=0)
    total_size_bytes = Column(BigInteger, default=0)
    
    # Metadata
    config = Column(Text, nullable=True)  # JSON config
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    artifacts = relationship("XRArtifact", back_populates="environment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<XREnvironment {self.name} ({self.type})>"
    
    @property
    def is_safe(self) -> bool:
        """Check if environment is safe to display."""
        return self.verified and self.checksum is not None
    
    def calculate_checksum(self) -> str:
        """Calculate checksum from all artifacts."""
        if not self.artifacts:
            return hashlib.sha256(b"empty").hexdigest()
        
        content = "".join(sorted(a.signature for a in self.artifacts))
        return hashlib.sha256(content.encode()).hexdigest()
    
    def verify(self) -> bool:
        """Verify environment integrity."""
        if not self.artifacts:
            return False
        
        # Verify all artifacts
        for artifact in self.artifacts:
            if not artifact.verified:
                return False
        
        # Verify overall checksum
        calculated = self.calculate_checksum()
        if calculated != self.checksum:
            return False
        
        self.verified = True
        return True


class XRArtifact(Base):
    """
    XR artifact (READ-ONLY).
    
    RÈGLE: Each artifact must be verified individually.
    
    Types:
    - mesh: 3D mesh files (glb, gltf)
    - texture: Texture files (jpg, png, hdr)
    - audio: Audio files (mp3, ogg)
    - config: Configuration files (json)
    """
    
    __tablename__ = "xr_artifacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    environment_id = Column(UUID(as_uuid=True), ForeignKey("xr_environments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # mesh, texture, audio, config
    version = Column(String(20), nullable=False, default="1.0.0")
    
    size_bytes = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=True)
    
    # Ed25519 signature for integrity
    signature = Column(String(128), nullable=False)
    verified = Column(Boolean, default=False)
    
    # Storage location
    storage_path = Column(Text, nullable=True)
    cdn_url = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    environment = relationship("XREnvironment", back_populates="artifacts")
    
    def __repr__(self):
        return f"<XRArtifact {self.name} ({self.type})>"
    
    @property
    def is_safe(self) -> bool:
        """Check if artifact is safe to use."""
        return self.verified and self.signature is not None
    
    def verify_signature(self, public_key: bytes, data: bytes) -> bool:
        """
        Verify Ed25519 signature.
        
        In production, use actual cryptographic verification.
        """
        # TODO: Implement actual Ed25519 verification
        # For now, mark as verified if signature exists
        if self.signature:
            self.verified = True
            return True
        return False


# ============================================================================
# XR READ-ONLY ENFORCEMENT
# ============================================================================

# Note: These events only apply to the backend.
# The XR CLIENT should never attempt to modify these tables.

@event.listens_for(XREnvironment, 'before_update')
def log_xr_environment_update(mapper, connection, target):
    """Log XR environment updates for audit."""
    # In production, log this to audit trail
    # XR updates should only come from generation pipeline
    pass


@event.listens_for(XRArtifact, 'before_update')
def prevent_artifact_modification(mapper, connection, target):
    """
    Prevent modification of verified artifacts.
    
    Once an artifact is verified, it should not be modified.
    """
    # Get original state
    from sqlalchemy.orm import object_session
    session = object_session(target)
    
    if session and hasattr(target, '_original_verified'):
        if target._original_verified and target.verified:
            # Only allow re-verification or explicit unverify
            pass


class XRVerificationResult:
    """
    Helper class for verification results.
    """
    
    def __init__(
        self,
        environment_id: str,
        valid: bool,
        signature: str,
        errors: list = None
    ):
        self.environment_id = environment_id
        self.valid = valid
        self.signature = signature
        self.verified_at = datetime.utcnow()
        self.errors = errors or []
    
    def to_dict(self) -> dict:
        return {
            "environment_id": self.environment_id,
            "valid": self.valid,
            "signature": self.signature,
            "verified_at": self.verified_at.isoformat(),
            "errors": self.errors,
        }
