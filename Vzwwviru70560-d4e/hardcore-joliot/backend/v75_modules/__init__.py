"""
CHE·NU™ V75 - MODULES PACKAGE

Modules:
- StagiaireEngine: Onboarding et validation
- ProfesseurEngine: Évaluation et formation
- CanonEngine: Source de vérité canonique
- CatalogEngine: Registry des modules
- ScenarioLockEngine: Tests déterministes
"""

from .stagiaire.stagiaire_engine import StagiaireEngine, StagiaireLevel
from .professeur.professeur_engine import ProfesseurEngine, EvaluationCategory
from .canon.canon_engine import CanonEngine, CanonStatus, CanonType
from .catalog.catalog_engine import CatalogEngine, ModuleStatus, ModuleCategory
from .scenario_lock.scenario_lock_engine import ScenarioLockEngine, ScenarioType

__version__ = "75.0"
__status__ = "CANON"

__all__ = [
    'StagiaireEngine', 'StagiaireLevel',
    'ProfesseurEngine', 'EvaluationCategory',
    'CanonEngine', 'CanonStatus', 'CanonType',
    'CatalogEngine', 'ModuleStatus', 'ModuleCategory',
    'ScenarioLockEngine', 'ScenarioType',
    '__version__', '__status__',
]
