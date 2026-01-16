"""
CHE·NU™ V75 Backend - DataSpace Model

DataSpace management for files, documents, and data organization.

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, BigInteger, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base


class DataSpace(Base):
    """
    DataSpace entity.
    
    Types:
    - project: Project-related files
    - property: Real estate property
    - client: Client documents
    - meeting: Meeting-related files
    - document: Single document space
    - custom: User-defined
    """
    
    __tablename__ = "dataspaces"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    dataspace_type = Column(String(50), default="custom")  # project, property, client, meeting, document, custom
    
    sphere_id = Column(String(50), ForeignKey("spheres.id"), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id"), nullable=True)
    
    status = Column(String(20), default="active")  # active, archived
    
    tags = Column(ARRAY(String), default=[])
    metadata = Column(JSONB, default={})
    
    # Computed fields (updated by triggers)
    files_count = Column(Integer, default=0)
    size_bytes = Column(BigInteger, default=0)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="dataspaces")
    sphere = relationship("Sphere", back_populates="dataspaces")
    parent = relationship("DataSpace", remote_side=[id], backref="children")
    files = relationship("DataSpaceFile", back_populates="dataspace", cascade="all, delete-orphan")
    links_from = relationship("DataSpaceLink", foreign_keys="DataSpaceLink.source_id", back_populates="source")
    links_to = relationship("DataSpaceLink", foreign_keys="DataSpaceLink.target_id", back_populates="target")
    
    def __repr__(self):
        return f"<DataSpace {self.name} ({self.dataspace_type})>"
    
    @property
    def is_archived(self) -> bool:
        """Check if dataspace is archived."""
        return self.status == "archived"
    
    def archive(self):
        """Archive the dataspace."""
        self.status = "archived"
        self.updated_at = datetime.utcnow()
    
    def unarchive(self):
        """Unarchive the dataspace."""
        self.status = "active"
        self.updated_at = datetime.utcnow()


class DataSpaceFile(Base):
    """
    File in a DataSpace.
    """
    
    __tablename__ = "dataspace_files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataspace_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, xlsx, image, etc.
    mime_type = Column(String(100), nullable=True)
    
    size_bytes = Column(BigInteger, nullable=False)
    
    # Storage
    storage_path = Column(Text, nullable=True)
    storage_type = Column(String(20), default="local")  # local, s3
    
    # Metadata
    checksum = Column(String(64), nullable=True)  # SHA-256
    metadata = Column(JSONB, default={})
    
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    dataspace = relationship("DataSpace", back_populates="files")
    
    def __repr__(self):
        return f"<DataSpaceFile {self.name}>"


class DataSpaceLink(Base):
    """
    Link between DataSpaces.
    
    Link types:
    - reference: Simple reference
    - parent: Parent-child relationship
    - related: Related content
    - derived: Derived from source
    """
    
    __tablename__ = "dataspace_links"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    source_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    target_id = Column(UUID(as_uuid=True), ForeignKey("dataspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    link_type = Column(String(50), default="reference")  # reference, parent, related, derived
    
    metadata = Column(JSONB, default={})
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    source = relationship("DataSpace", foreign_keys=[source_id], back_populates="links_from")
    target = relationship("DataSpace", foreign_keys=[target_id], back_populates="links_to")
    
    def __repr__(self):
        return f"<DataSpaceLink {self.source_id} -> {self.target_id}>"
