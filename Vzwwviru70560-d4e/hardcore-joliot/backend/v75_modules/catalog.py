"""
CHE·NU V75 - MODULE CATALOG
===========================
Système de catalogage universel pour tous les assets, modules et ressources.
Point central de découverte et navigation dans l'écosystème CHE·NU.

PRINCIPES:
- GOUVERNANCE > EXÉCUTION  
- Traçabilité complète de tous les assets
- Recherche unifiée cross-sphère (avec respect des boundaries)
"""

from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel

# ============================================================================
# ENUMS
# ============================================================================

class CatalogItemType(str, Enum):
    """Types d'items dans le catalogue"""
    # Core
    MODULE = "module"
    SERVICE = "service"
    AGENT = "agent"
    API_ENDPOINT = "api_endpoint"
    
    # Content
    DOCUMENT = "document"
    TEMPLATE = "template"
    ASSET = "asset"
    DATASET = "dataset"
    
    # Learning
    LEARNING_PATH = "learning_path"
    TUTORIAL = "tutorial"
    EXERCISE = "exercise"
    
    # System
    SPHERE = "sphere"
    VERTICAL = "vertical"
    WORKFLOW = "workflow"
    
    # XR
    XR_ENVIRONMENT = "xr_environment"
    XR_COMPONENT = "xr_component"
    XR_TEMPLATE = "xr_template"


class CatalogVisibility(str, Enum):
    """Visibilité des items"""
    PUBLIC = "public"              # Visible par tous
    SPHERE_RESTRICTED = "sphere"   # Visible dans la sphère
    PRIVATE = "private"            # Visible par le propriétaire
    INTERNAL = "internal"          # Système uniquement


class CatalogStatus(str, Enum):
    """Statut des items"""
    DRAFT = "draft"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    LOCKED = "locked"


# ============================================================================
# SCHEMAS
# ============================================================================

class CatalogTag(BaseModel):
    """Tag pour catégorisation"""
    name: str
    category: str  # sphere, feature, domain, etc.
    color: Optional[str] = None


class CatalogMetadata(BaseModel):
    """Métadonnées d'un item catalogue"""
    version: str = "1.0.0"
    author_id: str
    sphere: str
    tags: List[CatalogTag] = []
    dependencies: List[str] = []
    related_items: List[str] = []
    documentation_url: Optional[str] = None
    source_url: Optional[str] = None
    license: str = "CHE·NU Internal"


class CatalogItem(BaseModel):
    """Item du catalogue"""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: CatalogItemType
    name: str
    description: str
    slug: str  # URL-friendly identifier
    visibility: CatalogVisibility = CatalogVisibility.SPHERE_RESTRICTED
    status: CatalogStatus = CatalogStatus.DRAFT
    metadata: CatalogMetadata
    
    # Stats
    views_count: int = 0
    usage_count: int = 0
    rating: float = 0.0
    ratings_count: int = 0
    
    # Audit
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str
    updated_by: Optional[str] = None


class SearchQuery(BaseModel):
    """Requête de recherche"""
    query: str
    types: List[CatalogItemType] = []
    spheres: List[str] = []
    tags: List[str] = []
    status: List[CatalogStatus] = [CatalogStatus.PUBLISHED]
    visibility: Optional[CatalogVisibility] = None
    limit: int = 50
    offset: int = 0


class SearchResult(BaseModel):
    """Résultat de recherche"""
    items: List[CatalogItem]
    total_count: int
    query: str
    facets: Dict[str, Dict[str, int]]  # Aggregations par type, sphère, etc.


# ============================================================================
# CATALOG INDEXES
# ============================================================================

class CatalogIndex:
    """Index de recherche pour le catalogue"""
    
    def __init__(self):
        self.items_by_id: Dict[str, CatalogItem] = {}
        self.items_by_type: Dict[CatalogItemType, Set[str]] = {t: set() for t in CatalogItemType}
        self.items_by_sphere: Dict[str, Set[str]] = {}
        self.items_by_tag: Dict[str, Set[str]] = {}
        self.items_by_slug: Dict[str, str] = {}  # slug -> id
        
    def add_item(self, item: CatalogItem):
        """Ajoute un item à l'index"""
        self.items_by_id[item.id] = item
        self.items_by_type[item.type].add(item.id)
        
        sphere = item.metadata.sphere
        if sphere not in self.items_by_sphere:
            self.items_by_sphere[sphere] = set()
        self.items_by_sphere[sphere].add(item.id)
        
        for tag in item.metadata.tags:
            if tag.name not in self.items_by_tag:
                self.items_by_tag[tag.name] = set()
            self.items_by_tag[tag.name].add(item.id)
        
        self.items_by_slug[item.slug] = item.id
    
    def remove_item(self, item_id: str):
        """Retire un item de l'index"""
        if item_id not in self.items_by_id:
            return
        
        item = self.items_by_id[item_id]
        self.items_by_type[item.type].discard(item_id)
        
        if item.metadata.sphere in self.items_by_sphere:
            self.items_by_sphere[item.metadata.sphere].discard(item_id)
        
        for tag in item.metadata.tags:
            if tag.name in self.items_by_tag:
                self.items_by_tag[tag.name].discard(item_id)
        
        if item.slug in self.items_by_slug:
            del self.items_by_slug[item.slug]
        
        del self.items_by_id[item_id]
    
    def search(self, query: SearchQuery, user_spheres: List[str]) -> List[CatalogItem]:
        """
        Recherche dans l'index.
        Respecte les boundaries de sphères.
        """
        candidates: Set[str] = set(self.items_by_id.keys())
        
        # Filtrer par type
        if query.types:
            type_ids = set()
            for t in query.types:
                type_ids.update(self.items_by_type.get(t, set()))
            candidates &= type_ids
        
        # Filtrer par sphère
        if query.spheres:
            sphere_ids = set()
            for s in query.spheres:
                sphere_ids.update(self.items_by_sphere.get(s, set()))
            candidates &= sphere_ids
        
        # Filtrer par tags
        if query.tags:
            for tag in query.tags:
                candidates &= self.items_by_tag.get(tag, set())
        
        # Récupérer les items et filtrer par visibilité/status
        results = []
        for item_id in candidates:
            item = self.items_by_id[item_id]
            
            # Vérifier status
            if item.status not in query.status:
                continue
            
            # Vérifier visibilité
            if item.visibility == CatalogVisibility.PRIVATE:
                continue  # Filtrage par propriétaire à faire en amont
            elif item.visibility == CatalogVisibility.SPHERE_RESTRICTED:
                if item.metadata.sphere not in user_spheres:
                    continue
            
            # Recherche textuelle
            if query.query:
                query_lower = query.query.lower()
                if not (query_lower in item.name.lower() or 
                        query_lower in item.description.lower()):
                    continue
            
            results.append(item)
        
        # Tri par pertinence (simple: usage count)
        results.sort(key=lambda x: x.usage_count, reverse=True)
        
        # Pagination
        return results[query.offset:query.offset + query.limit]


# ============================================================================
# CATALOG SERVICE
# ============================================================================

class CatalogService:
    """
    Service Catalog V75
    
    Gère le catalogage universel de tous les assets CHE·NU.
    Respecte les principes Canon:
    - Identity boundary (recherche limitée aux sphères autorisées)
    - Traçabilité complète
    - Versioning et historique
    """
    
    def __init__(self):
        self.index = CatalogIndex()
        self.items: Dict[str, CatalogItem] = {}
        self.change_history: List[Dict] = []
        
    # ========================================================================
    # CRUD OPERATIONS
    # ========================================================================
    
    async def register_item(
        self,
        item_type: CatalogItemType,
        name: str,
        description: str,
        sphere: str,
        author_id: str,
        metadata: Dict[str, Any] = None
    ) -> CatalogItem:
        """Enregistre un nouvel item dans le catalogue"""
        # Générer slug unique
        slug = self._generate_slug(name)
        
        # Créer métadonnées
        meta = CatalogMetadata(
            author_id=author_id,
            sphere=sphere,
            **(metadata or {})
        )
        
        item = CatalogItem(
            type=item_type,
            name=name,
            description=description,
            slug=slug,
            metadata=meta,
            created_by=author_id
        )
        
        self.items[item.id] = item
        self.index.add_item(item)
        
        # Log changement
        self._log_change("create", item.id, author_id)
        
        return item
    
    async def get_item(self, item_id: str) -> Optional[CatalogItem]:
        """Récupère un item par ID"""
        return self.items.get(item_id)
    
    async def get_by_slug(self, slug: str) -> Optional[CatalogItem]:
        """Récupère un item par slug"""
        item_id = self.index.items_by_slug.get(slug)
        if item_id:
            return self.items.get(item_id)
        return None
    
    async def update_item(
        self,
        item_id: str,
        updates: Dict[str, Any],
        updated_by: str
    ) -> CatalogItem:
        """Met à jour un item"""
        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        # Retirer de l'index avant modification
        self.index.remove_item(item_id)
        
        # Appliquer les mises à jour
        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)
        
        item.updated_at = datetime.utcnow()
        item.updated_by = updated_by
        
        # Ré-indexer
        self.index.add_item(item)
        
        # Log changement
        self._log_change("update", item_id, updated_by, updates)
        
        return item
    
    async def archive_item(self, item_id: str, archived_by: str) -> CatalogItem:
        """Archive un item"""
        return await self.update_item(
            item_id,
            {"status": CatalogStatus.ARCHIVED},
            archived_by
        )
    
    async def publish_item(self, item_id: str, published_by: str) -> CatalogItem:
        """Publie un item (passe de DRAFT à PUBLISHED)"""
        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        if item.status != CatalogStatus.DRAFT:
            raise ValueError(f"Cannot publish item with status {item.status}")
        
        return await self.update_item(
            item_id,
            {"status": CatalogStatus.PUBLISHED},
            published_by
        )
    
    # ========================================================================
    # SEARCH & DISCOVERY
    # ========================================================================
    
    async def search(
        self,
        query: SearchQuery,
        user_id: str,
        user_spheres: List[str]
    ) -> SearchResult:
        """
        Recherche dans le catalogue.
        Respecte les identity boundaries via user_spheres.
        """
        items = self.index.search(query, user_spheres)
        
        # Incrémenter les vues pour analytics
        for item in items:
            item.views_count += 1
        
        # Calculer facettes
        facets = self._compute_facets(items)
        
        return SearchResult(
            items=items,
            total_count=len(items),
            query=query.query,
            facets=facets
        )
    
    async def browse_by_type(
        self,
        item_type: CatalogItemType,
        user_spheres: List[str],
        limit: int = 50
    ) -> List[CatalogItem]:
        """Parcourt les items par type"""
        query = SearchQuery(
            query="",
            types=[item_type],
            limit=limit
        )
        result = await self.search(query, "", user_spheres)
        return result.items
    
    async def browse_by_sphere(
        self,
        sphere: str,
        user_spheres: List[str],
        limit: int = 50
    ) -> List[CatalogItem]:
        """Parcourt les items par sphère"""
        if sphere not in user_spheres:
            return []  # Identity boundary
        
        query = SearchQuery(
            query="",
            spheres=[sphere],
            limit=limit
        )
        result = await self.search(query, "", user_spheres)
        return result.items
    
    async def get_related_items(
        self,
        item_id: str,
        user_spheres: List[str],
        limit: int = 10
    ) -> List[CatalogItem]:
        """Récupère les items liés"""
        item = self.items.get(item_id)
        if not item:
            return []
        
        related = []
        for related_id in item.metadata.related_items[:limit]:
            related_item = self.items.get(related_id)
            if related_item and related_item.metadata.sphere in user_spheres:
                related.append(related_item)
        
        return related
    
    # ========================================================================
    # STATS & ANALYTICS
    # ========================================================================
    
    async def record_usage(self, item_id: str, user_id: str):
        """Enregistre l'utilisation d'un item"""
        item = self.items.get(item_id)
        if item:
            item.usage_count += 1
            self._log_change("usage", item_id, user_id)
    
    async def rate_item(
        self,
        item_id: str,
        user_id: str,
        rating: float
    ) -> CatalogItem:
        """Note un item (1-5)"""
        item = self.items.get(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Recalculer moyenne
        total_rating = item.rating * item.ratings_count
        item.ratings_count += 1
        item.rating = (total_rating + rating) / item.ratings_count
        
        self._log_change("rate", item_id, user_id, {"rating": rating})
        
        return item
    
    async def get_popular_items(
        self,
        user_spheres: List[str],
        item_type: Optional[CatalogItemType] = None,
        limit: int = 20
    ) -> List[CatalogItem]:
        """Récupère les items les plus populaires"""
        candidates = []
        
        for item in self.items.values():
            if item.status != CatalogStatus.PUBLISHED:
                continue
            if item.metadata.sphere not in user_spheres:
                continue
            if item_type and item.type != item_type:
                continue
            candidates.append(item)
        
        # Trier par score de popularité
        candidates.sort(key=lambda x: x.usage_count * 0.7 + x.rating * 10 * 0.3, reverse=True)
        
        return candidates[:limit]
    
    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================
    
    async def bulk_register(
        self,
        items_data: List[Dict[str, Any]],
        author_id: str
    ) -> List[CatalogItem]:
        """Enregistre plusieurs items en batch"""
        results = []
        for data in items_data:
            item = await self.register_item(
                item_type=CatalogItemType(data["type"]),
                name=data["name"],
                description=data.get("description", ""),
                sphere=data["sphere"],
                author_id=author_id,
                metadata=data.get("metadata")
            )
            results.append(item)
        return results
    
    async def export_catalog(
        self,
        spheres: List[str],
        format: str = "json"
    ) -> Dict[str, Any]:
        """Exporte le catalogue pour une liste de sphères"""
        items = []
        for item in self.items.values():
            if item.metadata.sphere in spheres:
                items.append(item.dict())
        
        return {
            "version": "75",
            "exported_at": datetime.utcnow().isoformat(),
            "spheres": spheres,
            "items_count": len(items),
            "items": items
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _generate_slug(self, name: str) -> str:
        """Génère un slug URL-friendly unique"""
        import re
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        
        # Assurer unicité
        base_slug = slug
        counter = 1
        while slug in self.index.items_by_slug:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def _compute_facets(self, items: List[CatalogItem]) -> Dict[str, Dict[str, int]]:
        """Calcule les facettes pour les résultats de recherche"""
        facets = {
            "types": {},
            "spheres": {},
            "status": {}
        }
        
        for item in items:
            # Type
            type_name = item.type.value
            facets["types"][type_name] = facets["types"].get(type_name, 0) + 1
            
            # Sphère
            sphere = item.metadata.sphere
            facets["spheres"][sphere] = facets["spheres"].get(sphere, 0) + 1
            
            # Status
            status = item.status.value
            facets["status"][status] = facets["status"].get(status, 0) + 1
        
        return facets
    
    def _log_change(
        self,
        action: str,
        item_id: str,
        user_id: str,
        data: Dict = None
    ):
        """Log un changement pour l'audit"""
        self.change_history.append({
            "id": str(uuid4()),
            "action": action,
            "item_id": item_id,
            "user_id": user_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })


# ============================================================================
# PREDEFINED CATALOGS
# ============================================================================

# Modules système pré-enregistrés
SYSTEM_MODULES = [
    {
        "type": "module",
        "name": "Nova Pipeline",
        "description": "Intelligence système multi-lane",
        "sphere": "core"
    },
    {
        "type": "module",
        "name": "Thread Service",
        "description": "Gestion des Threads V2",
        "sphere": "core"
    },
    {
        "type": "module",
        "name": "Checkpoint Service",
        "description": "Système de checkpoints humains",
        "sphere": "governance"
    },
    {
        "type": "module",
        "name": "Stagiaire",
        "description": "Système d'apprentissage et progression",
        "sphere": "education"
    },
    {
        "type": "module",
        "name": "Professeur",
        "description": "Système de mentorat et évaluation",
        "sphere": "education"
    },
    {
        "type": "module",
        "name": "Canon",
        "description": "Source de vérité et règles R&D",
        "sphere": "governance"
    }
]


# ============================================================================
# INSTANCE GLOBALE
# ============================================================================

catalog_service = CatalogService()


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'CatalogService',
    'catalog_service',
    'CatalogItemType',
    'CatalogVisibility',
    'CatalogStatus',
    'CatalogItem',
    'CatalogMetadata',
    'CatalogTag',
    'SearchQuery',
    'SearchResult',
    'SYSTEM_MODULES'
]
