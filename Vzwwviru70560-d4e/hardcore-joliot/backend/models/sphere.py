"""
CHE·NU™ V75 Backend - Sphere & Bureau Models

RÈGLE ABSOLUE: ARCHITECTURE GELÉE
- Exactement 9 sphères canoniques
- Exactement 6 bureaux par sphère
- Aucune modification de structure autorisée

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ARRAY, event
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


# ============================================================================
# CANONICAL DEFINITIONS (FROZEN)
# ============================================================================

CANONICAL_SPHERE_IDS = [
    "personal",
    "business",
    "government",
    "studio",
    "community",
    "social",
    "entertainment",
    "team",
    "scholar",
]

CANONICAL_BUREAU_IDS = [
    "quick_capture",
    "resume_workspace",
    "threads",
    "data_files",
    "active_agents",
    "meetings",
]


class Sphere(Base):
    """
    Sphere entity (9 canonical - FROZEN).
    
    RÈGLE: Exactement 9 sphères, aucune création/suppression autorisée.
    """
    
    __tablename__ = "spheres"
    
    id = Column(String(50), primary_key=True)  # Canonical ID
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(10), nullable=True)  # Emoji
    color = Column(String(7), nullable=True)  # Hex color
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    threads = relationship("Thread", back_populates="sphere")
    decisions = relationship("Decision", back_populates="sphere")
    dataspaces = relationship("DataSpace", back_populates="sphere")
    
    def __repr__(self):
        return f"<Sphere {self.name}>"
    
    @classmethod
    def is_valid_id(cls, sphere_id: str) -> bool:
        """Check if sphere ID is canonical."""
        return sphere_id in CANONICAL_SPHERE_IDS


class Bureau(Base):
    """
    Bureau entity (6 per sphere - FROZEN).
    
    RÈGLE: Exactement 6 bureaux par sphère, structure fixe.
    """
    
    __tablename__ = "bureaus"
    
    id = Column(String(50), primary_key=True)  # Canonical ID
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    capabilities = Column(ARRAY(String), default=[])
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    threads = relationship("Thread", back_populates="bureau")
    
    def __repr__(self):
        return f"<Bureau {self.name}>"
    
    @classmethod
    def is_valid_id(cls, bureau_id: str) -> bool:
        """Check if bureau ID is canonical."""
        return bureau_id in CANONICAL_BUREAU_IDS


# ============================================================================
# FROZEN ARCHITECTURE ENFORCEMENT
# ============================================================================

@event.listens_for(Sphere, 'before_insert')
def validate_sphere_creation(mapper, connection, target):
    """Validate sphere creation against canonical list."""
    if target.id not in CANONICAL_SPHERE_IDS:
        raise ValueError(
            f"Invalid sphere ID '{target.id}'. "
            f"Only canonical spheres allowed: {CANONICAL_SPHERE_IDS}"
        )


@event.listens_for(Sphere, 'before_delete')
def prevent_sphere_deletion(mapper, connection, target):
    """Prevent deletion of canonical spheres."""
    raise ValueError(
        f"Cannot delete sphere '{target.id}'. "
        f"Sphere architecture is FROZEN."
    )


@event.listens_for(Bureau, 'before_insert')
def validate_bureau_creation(mapper, connection, target):
    """Validate bureau creation against canonical list."""
    if target.id not in CANONICAL_BUREAU_IDS:
        raise ValueError(
            f"Invalid bureau ID '{target.id}'. "
            f"Only canonical bureaus allowed: {CANONICAL_BUREAU_IDS}"
        )


@event.listens_for(Bureau, 'before_delete')
def prevent_bureau_deletion(mapper, connection, target):
    """Prevent deletion of canonical bureaus."""
    raise ValueError(
        f"Cannot delete bureau '{target.id}'. "
        f"Bureau architecture is FROZEN."
    )


# ============================================================================
# SEED DATA
# ============================================================================

SPHERE_SEED_DATA = [
    {"id": "personal", "name": "Personnel", "description": "Votre espace personnel et vie quotidienne", "icon": "👤", "color": "#D8B26A"},
    {"id": "business", "name": "Business", "description": "Gestion d'entreprise et activités professionnelles", "icon": "💼", "color": "#3F7249"},
    {"id": "government", "name": "Gouvernement & Institutions", "description": "Interactions avec les institutions gouvernementales", "icon": "🏛️", "color": "#8D8371"},
    {"id": "studio", "name": "Studio de création", "description": "Création artistique et design", "icon": "🎨", "color": "#3EB4A2"},
    {"id": "community", "name": "Communauté", "description": "Associations et groupes communautaires", "icon": "🤝", "color": "#2F4C39"},
    {"id": "social", "name": "Social & Médias", "description": "Réseaux sociaux et communication", "icon": "📱", "color": "#7A593A"},
    {"id": "entertainment", "name": "Divertissement", "description": "Loisirs et divertissement", "icon": "🎬", "color": "#D8B26A"},
    {"id": "team", "name": "Mon équipe", "description": "Collaboration et gestion d'équipe", "icon": "👥", "color": "#3F7249"},
    {"id": "scholar", "name": "Scholar", "description": "Éducation et recherche académique", "icon": "🎓", "color": "#3EB4A2"},
]

BUREAU_SEED_DATA = [
    {"id": "quick_capture", "name": "Quick Capture", "description": "Capture rapide d'idées et notes", "capabilities": ["notes", "voice", "images", "links"]},
    {"id": "resume_workspace", "name": "Resume Workspace", "description": "Reprendre là où vous avez arrêté", "capabilities": ["recent", "pinned", "drafts"]},
    {"id": "threads", "name": "Threads", "description": "Conversations et discussions continues", "capabilities": ["conversations", "decisions", "history"]},
    {"id": "data_files", "name": "Data Files", "description": "Documents et fichiers", "capabilities": ["upload", "organize", "search", "share"]},
    {"id": "active_agents", "name": "Active Agents", "description": "Agents IA assignés", "capabilities": ["manage", "assign", "monitor"]},
    {"id": "meetings", "name": "Meetings", "description": "Réunions et calendrier", "capabilities": ["schedule", "notes", "recordings"]},
]
