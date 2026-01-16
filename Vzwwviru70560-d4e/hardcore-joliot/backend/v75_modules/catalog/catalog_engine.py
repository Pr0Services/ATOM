"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                          CHE·NU™ V75 - CATALOG ENGINE                                ║
║                                                                                      ║
║  Registry centralisé de tous les modules CHE·NU                                     ║
║  Source de vérité pour l'état et les dépendances des modules                        ║
║                                                                                      ║
║  Version: 75.0 | Status: CANON | License: Proprietary                               ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import logging
import json

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

MODULE_VERSION = "75.0"
MODULE_STATUS = "CANON"
MODULE_NAME = "CatalogEngine"

class ModuleStatus(str, Enum):
    """Status d'un module dans le catalogue"""
    INTEGRATED = "integrated"   # Module actif et testé
    PLANNED = "planned"         # En développement
    ARCHIVED = "archived"       # Déprécié, ne pas utiliser
    FLAGGED = "flagged"         # Nécessite clarification
    MERGED = "merged"           # Fusionné dans un autre
    LOCKED = "locked"           # Ne peut être modifié

class ModuleCategory(str, Enum):
    """Catégories de modules"""
    CORE = "core"               # Modules système critiques
    GOVERNANCE = "governance"   # Modules de gouvernance
    SPHERE = "sphere"           # Modules spécifiques à une sphère
    VERTICAL = "vertical"       # Modules verticaux (industries)
    AGENT = "agent"             # Agents spécialisés
    API = "api"                 # Routes et endpoints
    FRONTEND = "frontend"       # Composants frontend
    TEST = "test"               # Modules de test
    V75 = "v75"                 # Nouveaux modules V75

class SphereType(str, Enum):
    """Les 9 sphères CHE·NU"""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"
    CORE = "core"  # Cross-sphere

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ModuleEntry:
    """Entrée d'un module dans le catalogue"""
    id: str
    name: str
    path: str
    category: ModuleCategory
    status: ModuleStatus
    sphere: Optional[SphereType]
    version: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    replaces: Optional[str] = None
    replaced_by: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: UUID = field(default_factory=uuid4)
    locked_at: Optional[datetime] = None
    locked_reason: Optional[str] = None
    test_coverage: float = 0.0
    lines_of_code: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DependencyGraph:
    """Graphe des dépendances entre modules"""
    nodes: Set[str]
    edges: Dict[str, Set[str]]  # module_id -> set of dependencies
    reverse_edges: Dict[str, Set[str]]  # module_id -> set of dependents

@dataclass
class CatalogStats:
    """Statistiques du catalogue"""
    total_modules: int
    by_status: Dict[str, int]
    by_category: Dict[str, int]
    by_sphere: Dict[str, int]
    total_lines_of_code: int
    average_coverage: float
    timestamp: datetime

# ═══════════════════════════════════════════════════════════════════════════════
# V75 MODULES REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

V75_MODULES = [
    ModuleEntry(
        id="STAG_001",
        name="StagiaireEngine",
        path="backend/v75_modules/stagiaire/stagiaire_engine.py",
        category=ModuleCategory.V75,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CORE,
        version="75.0",
        description="Système d'onboarding et validation des connaissances CHE·NU",
        lines_of_code=450,
        metadata={"criticality": "high", "human_gates": True}
    ),
    ModuleEntry(
        id="PROF_001",
        name="ProfesseurEngine",
        path="backend/v75_modules/professeur/professeur_engine.py",
        category=ModuleCategory.V75,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CORE,
        version="75.0",
        description="Système d'évaluation et formation des agents",
        dependencies=["STAG_001"],
        lines_of_code=520,
        metadata={"criticality": "high", "human_gates": True}
    ),
    ModuleEntry(
        id="CANON_001",
        name="CanonEngine",
        path="backend/v75_modules/canon/canon_engine.py",
        category=ModuleCategory.V75,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CORE,
        version="75.0",
        description="Validation source de vérité canonique",
        lines_of_code=480,
        metadata={"criticality": "critical", "locked_content": True}
    ),
    ModuleEntry(
        id="CATALOG_001",
        name="CatalogEngine",
        path="backend/v75_modules/catalog/catalog_engine.py",
        category=ModuleCategory.V75,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CORE,
        version="75.0",
        description="Registry centralisé des modules CHE·NU",
        lines_of_code=500,
        metadata={"criticality": "critical"}
    ),
    ModuleEntry(
        id="SCENLOCK_001",
        name="ScenarioLockEngine",
        path="backend/v75_modules/scenario_lock/scenario_lock_engine.py",
        category=ModuleCategory.V75,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CORE,
        version="75.0",
        description="Verrouillage de scénarios pour tests déterministes",
        lines_of_code=400,
        metadata={"criticality": "high", "testing": True}
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# VERTICALS REGISTRY (14 Verticals V68)
# ═══════════════════════════════════════════════════════════════════════════════

VERTICAL_MODULES = [
    ModuleEntry(
        id="VERT_BIZ_001",
        name="Business CRM Vertical",
        path="backend/verticals/BUSINESS_CRM_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.BUSINESS,
        version="68.0",
        description="Vertical CRM et gestion d'entreprise",
        metadata={"vertical_id": "BUSINESS_CRM"}
    ),
    ModuleEntry(
        id="VERT_COMM_001",
        name="Community Vertical",
        path="backend/verticals/COMMUNITY_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.COMMUNITY,
        version="68.0",
        description="Vertical communautaire"
    ),
    ModuleEntry(
        id="VERT_COMP_001",
        name="Compliance Vertical",
        path="backend/verticals/COMPLIANCE_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.GOVERNMENT,
        version="68.0",
        description="Vertical conformité et gouvernance"
    ),
    ModuleEntry(
        id="VERT_CONS_001",
        name="Construction Vertical",
        path="backend/verticals/CONSTRUCTION_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.BUSINESS,
        version="68.0",
        description="Vertical construction et AEC"
    ),
    ModuleEntry(
        id="VERT_CREAT_001",
        name="Creative Studio Vertical",
        path="backend/verticals/CREATIVE_STUDIO_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.CREATIVE_STUDIO,
        version="68.0",
        description="Vertical création et design"
    ),
    ModuleEntry(
        id="VERT_EDU_001",
        name="Education Vertical",
        path="backend/verticals/EDUCATION_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.SCHOLAR,
        version="68.0",
        description="Vertical éducation et formation"
    ),
    ModuleEntry(
        id="VERT_ENT_001",
        name="Entertainment Vertical",
        path="backend/verticals/ENTERTAINMENT_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.ENTERTAINMENT,
        version="68.0",
        description="Vertical divertissement et médias"
    ),
    ModuleEntry(
        id="VERT_HR_001",
        name="HR Vertical",
        path="backend/verticals/HR_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.MY_TEAM,
        version="68.0",
        description="Vertical ressources humaines"
    ),
    ModuleEntry(
        id="VERT_MKT_001",
        name="Marketing Vertical",
        path="backend/verticals/MARKETING_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.BUSINESS,
        version="68.0",
        description="Vertical marketing automation"
    ),
    ModuleEntry(
        id="VERT_PERS_001",
        name="Personal Productivity Vertical",
        path="backend/verticals/PERSONAL_PRODUCTIVITY_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.PERSONAL,
        version="68.0",
        description="Vertical productivité personnelle"
    ),
    ModuleEntry(
        id="VERT_PROJ_001",
        name="Project Management Vertical",
        path="backend/verticals/PROJECT_MGMT_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.BUSINESS,
        version="68.0",
        description="Vertical gestion de projets"
    ),
    ModuleEntry(
        id="VERT_RE_001",
        name="Real Estate Vertical",
        path="backend/verticals/REAL_ESTATE_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.BUSINESS,
        version="68.0",
        description="Vertical immobilier"
    ),
    ModuleEntry(
        id="VERT_SOC_001",
        name="Social Vertical",
        path="backend/verticals/SOCIAL_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.SOCIAL_MEDIA,
        version="68.0",
        description="Vertical social media (NO RANKING!)"
    ),
    ModuleEntry(
        id="VERT_TEAM_001",
        name="Team Collaboration Vertical",
        path="backend/verticals/TEAM_COLLAB_V68",
        category=ModuleCategory.VERTICAL,
        status=ModuleStatus.INTEGRATED,
        sphere=SphereType.MY_TEAM,
        version="68.0",
        description="Vertical collaboration d'équipe"
    ),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CATALOG ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class CatalogEngine:
    """
    Registry centralisé de tous les modules CHE·NU.
    
    Le Catalog Engine maintient l'inventaire complet des modules,
    leurs dépendances, et leur état de santé.
    """
    
    def __init__(self):
        self.modules: Dict[str, ModuleEntry] = {}
        self.dependency_graph: DependencyGraph = DependencyGraph(
            nodes=set(),
            edges={},
            reverse_edges={}
        )
        
        self._initialize_modules()
        self._build_dependency_graph()
        
        logger.info(
            f"CatalogEngine V{MODULE_VERSION} initialized with "
            f"{len(self.modules)} modules"
        )
    
    def _initialize_modules(self):
        """Charge tous les modules dans le catalogue."""
        # Charger modules V75
        for module in V75_MODULES:
            self.modules[module.id] = module
        
        # Charger verticals
        for module in VERTICAL_MODULES:
            self.modules[module.id] = module
    
    def _build_dependency_graph(self):
        """Construit le graphe de dépendances."""
        for module_id in self.modules:
            self.dependency_graph.nodes.add(module_id)
            self.dependency_graph.edges[module_id] = set()
            self.dependency_graph.reverse_edges[module_id] = set()
        
        for module_id, module in self.modules.items():
            for dep_id in module.dependencies:
                if dep_id in self.modules:
                    self.dependency_graph.edges[module_id].add(dep_id)
                    self.dependency_graph.reverse_edges[dep_id].add(module_id)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CRUD OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    async def register_module(
        self,
        module: ModuleEntry,
        registered_by: UUID
    ) -> ModuleEntry:
        """
        Enregistre un nouveau module dans le catalogue.
        
        Vérifie les dépendances et l'unicité avant enregistrement.
        """
        # Vérifier unicité
        if module.id in self.modules:
            raise ValueError(f"Module {module.id} already exists")
        
        # Vérifier nom unique
        existing_names = {m.name for m in self.modules.values()}
        if module.name in existing_names:
            raise ValueError(f"Module name '{module.name}' already exists")
        
        # Vérifier dépendances existent
        for dep_id in module.dependencies:
            if dep_id not in self.modules:
                raise ValueError(f"Dependency {dep_id} not found")
        
        # Enregistrer
        module.created_by = registered_by
        module.created_at = datetime.utcnow()
        self.modules[module.id] = module
        
        # Mettre à jour graphe
        self.dependency_graph.nodes.add(module.id)
        self.dependency_graph.edges[module.id] = set(module.dependencies)
        self.dependency_graph.reverse_edges[module.id] = set()
        
        for dep_id in module.dependencies:
            self.dependency_graph.reverse_edges[dep_id].add(module.id)
        
        logger.info(f"Module {module.id} registered by {registered_by}")
        
        return module
    
    async def update_module_status(
        self,
        module_id: str,
        new_status: ModuleStatus,
        updated_by: UUID,
        reason: str
    ) -> ModuleEntry:
        """
        Met à jour le status d'un module.
        
        Les modules LOCKED ne peuvent pas être modifiés.
        """
        if module_id not in self.modules:
            raise ValueError(f"Module {module_id} not found")
        
        module = self.modules[module_id]
        
        if module.status == ModuleStatus.LOCKED:
            raise ValueError(f"Cannot modify LOCKED module {module_id}")
        
        old_status = module.status
        module.status = new_status
        
        if new_status == ModuleStatus.LOCKED:
            module.locked_at = datetime.utcnow()
            module.locked_reason = reason
        
        logger.info(
            f"Module {module_id} status changed: {old_status} -> {new_status} "
            f"by {updated_by}. Reason: {reason}"
        )
        
        return module
    
    async def archive_module(
        self,
        module_id: str,
        replaced_by: Optional[str],
        archived_by: UUID,
        reason: str
    ) -> ModuleEntry:
        """
        Archive un module (le marque comme déprécié).
        
        Vérifie qu'aucun autre module ne dépend de lui
        ou qu'un remplacement est fourni.
        """
        if module_id not in self.modules:
            raise ValueError(f"Module {module_id} not found")
        
        module = self.modules[module_id]
        
        # Vérifier dépendants
        dependents = self.dependency_graph.reverse_edges.get(module_id, set())
        if dependents and not replaced_by:
            raise ValueError(
                f"Cannot archive {module_id}: has dependents {dependents}. "
                f"Provide replacement module."
            )
        
        module.status = ModuleStatus.ARCHIVED
        module.replaced_by = replaced_by
        
        # Mettre à jour le module de remplacement
        if replaced_by and replaced_by in self.modules:
            self.modules[replaced_by].replaces = module_id
        
        logger.info(
            f"Module {module_id} archived by {archived_by}. "
            f"Replaced by: {replaced_by}. Reason: {reason}"
        )
        
        return module
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_module(self, module_id: str) -> Optional[ModuleEntry]:
        """Récupère un module par ID."""
        return self.modules.get(module_id)
    
    async def search_modules(
        self,
        query: str,
        status: Optional[ModuleStatus] = None,
        category: Optional[ModuleCategory] = None,
        sphere: Optional[SphereType] = None
    ) -> List[ModuleEntry]:
        """Recherche des modules avec filtres."""
        results = list(self.modules.values())
        
        # Filtre texte
        if query:
            query_lower = query.lower()
            results = [
                m for m in results
                if query_lower in m.name.lower() or 
                   query_lower in m.description.lower()
            ]
        
        # Filtres
        if status:
            results = [m for m in results if m.status == status]
        if category:
            results = [m for m in results if m.category == category]
        if sphere:
            results = [m for m in results if m.sphere == sphere]
        
        return results
    
    async def get_dependencies(
        self,
        module_id: str,
        recursive: bool = False
    ) -> List[ModuleEntry]:
        """
        Récupère les dépendances d'un module.
        
        Si recursive=True, inclut toutes les dépendances transitives.
        """
        if module_id not in self.modules:
            return []
        
        if not recursive:
            dep_ids = self.dependency_graph.edges.get(module_id, set())
            return [self.modules[d] for d in dep_ids if d in self.modules]
        
        # Récursif - BFS
        all_deps = set()
        to_visit = list(self.dependency_graph.edges.get(module_id, set()))
        
        while to_visit:
            dep_id = to_visit.pop(0)
            if dep_id not in all_deps and dep_id in self.modules:
                all_deps.add(dep_id)
                to_visit.extend(
                    self.dependency_graph.edges.get(dep_id, set())
                )
        
        return [self.modules[d] for d in all_deps]
    
    async def get_dependents(
        self,
        module_id: str
    ) -> List[ModuleEntry]:
        """Récupère les modules qui dépendent de celui-ci."""
        dep_ids = self.dependency_graph.reverse_edges.get(module_id, set())
        return [self.modules[d] for d in dep_ids if d in self.modules]
    
    # ═══════════════════════════════════════════════════════════════════════
    # STATS & REPORTS
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_stats(self) -> CatalogStats:
        """Génère les statistiques du catalogue."""
        by_status = {}
        by_category = {}
        by_sphere = {}
        total_loc = 0
        coverages = []
        
        for module in self.modules.values():
            # By status
            status = module.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            # By category
            cat = module.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
            
            # By sphere
            if module.sphere:
                sph = module.sphere.value
                by_sphere[sph] = by_sphere.get(sph, 0) + 1
            
            # Totals
            total_loc += module.lines_of_code
            if module.test_coverage > 0:
                coverages.append(module.test_coverage)
        
        return CatalogStats(
            total_modules=len(self.modules),
            by_status=by_status,
            by_category=by_category,
            by_sphere=by_sphere,
            total_lines_of_code=total_loc,
            average_coverage=sum(coverages) / len(coverages) if coverages else 0,
            timestamp=datetime.utcnow()
        )
    
    async def generate_report(self) -> Dict[str, Any]:
        """Génère un rapport complet du catalogue."""
        stats = await self.get_stats()
        
        # Modules problématiques
        flagged = [
            {"id": m.id, "name": m.name, "reason": m.metadata.get("flag_reason", "Unknown")}
            for m in self.modules.values()
            if m.status == ModuleStatus.FLAGGED
        ]
        
        # Modules sans dépendants (potentiellement inutilisés)
        orphans = [
            m.id for m in self.modules.values()
            if len(self.dependency_graph.reverse_edges.get(m.id, set())) == 0
            and m.category not in [ModuleCategory.V75, ModuleCategory.VERTICAL]
        ]
        
        # Vérifier cycles
        cycles = await self._detect_cycles()
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "version": MODULE_VERSION,
            "stats": {
                "total_modules": stats.total_modules,
                "by_status": stats.by_status,
                "by_category": stats.by_category,
                "by_sphere": stats.by_sphere,
                "total_lines_of_code": stats.total_lines_of_code,
                "average_coverage": round(stats.average_coverage, 2)
            },
            "health": {
                "flagged_modules": flagged,
                "potential_orphans": orphans[:10],
                "circular_dependencies": cycles,
                "health_score": self._calculate_health_score(stats, flagged, cycles)
            },
            "v75_modules": [
                {"id": m.id, "name": m.name, "status": m.status.value}
                for m in self.modules.values()
                if m.category == ModuleCategory.V75
            ],
            "verticals": [
                {"id": m.id, "name": m.name, "sphere": m.sphere.value if m.sphere else None}
                for m in self.modules.values()
                if m.category == ModuleCategory.VERTICAL
            ]
        }
    
    async def _detect_cycles(self) -> List[str]:
        """Détecte les dépendances circulaires."""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(module_id: str, path: List[str]) -> bool:
            visited.add(module_id)
            rec_stack.add(module_id)
            path.append(module_id)
            
            for dep_id in self.dependency_graph.edges.get(module_id, set()):
                if dep_id not in visited:
                    if dfs(dep_id, path):
                        return True
                elif dep_id in rec_stack:
                    cycle_start = path.index(dep_id)
                    cycles.append(" -> ".join(path[cycle_start:] + [dep_id]))
                    return True
            
            path.pop()
            rec_stack.remove(module_id)
            return False
        
        for module_id in self.modules:
            if module_id not in visited:
                dfs(module_id, [])
        
        return cycles
    
    def _calculate_health_score(
        self,
        stats: CatalogStats,
        flagged: List,
        cycles: List
    ) -> float:
        """Calcule un score de santé du catalogue (0-100)."""
        score = 100.0
        
        # Pénalités
        flagged_penalty = len(flagged) * 5  # -5 par module flagged
        cycle_penalty = len(cycles) * 10    # -10 par cycle
        coverage_penalty = max(0, (70 - stats.average_coverage)) * 0.5  # Si < 70%
        
        # Ratio archived/total
        archived = stats.by_status.get("archived", 0)
        if stats.total_modules > 0:
            archived_ratio = archived / stats.total_modules
            if archived_ratio > 0.2:  # Plus de 20% archivés
                score -= 10
        
        score -= flagged_penalty
        score -= cycle_penalty
        score -= coverage_penalty
        
        return max(0, min(100, score))


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'CatalogEngine',
    'ModuleStatus',
    'ModuleCategory',
    'SphereType',
    'ModuleEntry',
    'DependencyGraph',
    'CatalogStats',
    'V75_MODULES',
    'VERTICAL_MODULES',
    'MODULE_VERSION',
]
