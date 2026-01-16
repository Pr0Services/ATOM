# 🔧 CHE·NU™ MODULE INTEGRATION PROCESS V1.0

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                  PROCESSUS D'INTÉGRATION DE MODULES                          ║
║                         OFFICIEL & OBLIGATOIRE                               ║
║                                                                               ║
║                        Version: 1.0 | Date: 21 Décembre 2025                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Status:** MANDATORY PROCESS  
**Scope:** All new module development and integration  
**Authority:** R&D + Architect approval required  
**Violation:** Module rejected, code reverted

---

## 🎯 OBJECTIF

Ce processus garantit que **TOUS les nouveaux modules**:
1. Sont correctement classifiés
2. N'introduisent PAS de logique parallèle
3. Respectent les frontières sphères
4. Sont documentés dans le MODULE REGISTRY
5. Obtiennent l'approbation R&D avant intégration

---

## 🚫 RÈGLES ABSOLUES

### RÈGLE #1: NO MODULE WITHOUT REGISTRY ENTRY
**AUCUN** module ne peut être codé sans entrée préalable dans le MODULE REGISTRY.

### RÈGLE #2: NO DUPLICATE LOGIC
**AUCUN** module ne peut dupliquer la logique d'un module existant INTEGRATED.

### RÈGLE #3: NO CROSS-SPHERE WITHOUT VALIDATION
**AUCUN** module sphère-spécifique ne peut accéder à une autre sphère sans validation R&D.

### RÈGLE #4: NO AUTO-INTEGRATION
**AUCUN** module ne peut être marqué INTEGRATED sans test et approbation R&D.

### RÈGLE #5: LOCKED MODULES ARE FROZEN
**AUCUN** module LOCKED ne peut être modifié sans revue architecturale complète.

---

## 📋 PROCESSUS EN 8 ÉTAPES

### ÉTAPE 1: PRE-INTEGRATION CHECKLIST

**AVANT** de coder quoi que ce soit, compléter:

```markdown
☐ Nom du module: ___________________________
☐ Sphère propriétaire: ___________________________
☐ Intent original: ___________________________
☐ Module équivalent existant? (si oui → STOP, utiliser existant)
☐ Logique parallèle détectée? (si oui → STOP, revoir design)
☐ Approbation R&D obtenue? (si non → STOP, demander approbation)
```

**Si TOUS les critères passent → Continuer ÉTAPE 2**  
**Si UN critère échoue → ARRÊTER, revoir design**

---

### ÉTAPE 2: REGISTRY ENTRY CREATION

**AVANT** de coder, créer l'entrée MODULE REGISTRY:

**Template:**

```markdown
| Module Name | Original Sphere | Current Status | Current Equivalent | LOCKED Eligible | Notes |
|-------------|-----------------|----------------|-------------------|-----------------|-------|
| module_name.py | SPHERE_NAME | PLANNED | N/A | TBD | Intent: [description] |
```

**Exemples:**

```markdown
| personal_budget_advanced.py | Personal | PLANNED | N/A | TBD | Intent: Budget personnel avec prédictions IA |
| creative_voice_synthesis.py | Creative Studio | PLANNED | N/A | TBD | Intent: Synthèse vocale multi-langues |
| gov_tax_automation.py | Government | PLANNED | N/A | TBD | Intent: Automatisation déclarations fiscales |
```

**Ajouter l'entrée au fichier:**  
`CHENU_MODULE_REGISTRY_V1_0_SOURCE_OF_TRUTH.md`

**Section:** Ajouter dans section appropriée (CORE, SPHERE-SPECIFIC, etc.)

---

### ÉTAPE 3: DEPENDENCY MAPPING

**Identifier TOUTES les dépendances:**

```python
# Template de documentation module
"""
MODULE: module_name.py
SPHERE: [Sphere Name]
INTENT: [Description]

DEPENDENCIES:
- Core: [list core modules used]
- Sphere: [list sphere modules used]
- External: [list external APIs/services]

INTEGRATIONS:
- Calls to: [modules this calls]
- Called by: [modules that call this]

LOCKED STATUS: [TBD / YES / NO]
"""
```

**Exemple:**

```python
"""
MODULE: personal_budget_advanced.py
SPHERE: Personal
INTENT: Advanced budget tracking with AI predictions

DEPENDENCIES:
- Core: memory_engine.py, thread_service.py, ai_service.py
- Sphere: (none - Personal sphere only)
- External: Plaid API (bank connections)

INTEGRATIONS:
- Calls to: ai_service.predict(), memory_engine.store()
- Called by: personal_dashboard.py, personal_agents/

LOCKED STATUS: NO (new development)
"""
```

---

### ÉTAPE 4: CODE DEVELOPMENT

**Standards de codage:**

1. **Fichier location:**
   - Services: `/backend/services/[module_name].py`
   - Agents: `/backend/agents/[sphere]/[agent_name].py`
   - API Routes: `/backend/api/[resource]_routes.py`

2. **Naming convention:**
   - Services: `[purpose]_service.py` (ex: `budget_service.py`)
   - Agents: `[role]_agent.py` (ex: `budget_advisor_agent.py`)
   - Routes: `[resource]_routes.py` (ex: `budget_routes.py`)

3. **Code structure:**

```python
"""
[MODULE DOCSTRING - see ÉTAPE 3]
"""

# Imports
from typing import Optional, Dict, Any
from backend.services.core_service import CoreService
# ... autres imports

# Constants
MODULE_VERSION = "1.0.0"
SPHERE = "Personal"  # ou autre

# Main class/functions
class BudgetService:
    """Service pour gestion budget personnel."""
    
    def __init__(self):
        self.sphere = SPHERE
        self.locked = False  # Nouveau module
        
    async def predict_expenses(self, user_id: str) -> Dict[str, Any]:
        """Prédit dépenses futures avec IA."""
        # Implementation
        pass

# Exports
__all__ = ['BudgetService']
```

4. **Tests REQUIS:**
   - Unit tests: `/backend/tests/test_[module_name].py`
   - Couverture minimum: 70%
   - Tests d'intégration pour dépendances

---

### ÉTAPE 5: INTEGRATION TESTING

**Tests obligatoires:**

```python
# /backend/tests/test_budget_service.py

import pytest
from backend.services.budget_service import BudgetService

class TestBudgetService:
    
    @pytest.fixture
    def service(self):
        return BudgetService()
    
    def test_initialization(self, service):
        assert service.sphere == "Personal"
        assert service.locked == False
    
    def test_predict_expenses(self, service):
        # Test logic
        result = await service.predict_expenses("user_123")
        assert "predictions" in result
        assert len(result["predictions"]) > 0
    
    def test_sphere_isolation(self, service):
        # Verify no cross-sphere access without validation
        # ... test logic
        pass
```

**Exécuter:**

```bash
pytest backend/tests/test_budget_service.py -v --cov
```

**Critères de passage:**
- ✅ Tous tests passent
- ✅ Couverture ≥ 70%
- ✅ Aucune régression détectée
- ✅ Performance acceptable (<500ms response time)

---

### ÉTAPE 6: REGISTRY UPDATE - INTEGRATED

**Mettre à jour l'entrée MODULE REGISTRY:**

**AVANT:**
```markdown
| personal_budget_advanced.py | Personal | PLANNED | N/A | TBD | Intent: Budget personnel avec prédictions IA |
```

**APRÈS:**
```markdown
| personal_budget_advanced.py | Personal | INTEGRATED | main_v42_unified.py budget | YES | Active depuis v42.1, tests 85% coverage |
```

**Changements:**
- `Current Status`: PLANNED → **INTEGRATED**
- `Current Equivalent`: N/A → **main_v42_unified.py budget**
- `LOCKED Eligible`: TBD → **YES** (si applicable)
- `Notes`: Ajouter version, coverage, date activation

---

### ÉTAPE 7: DOCUMENTATION UPDATE

**Mettre à jour documentation:**

1. **API Documentation** (si applicable):
   - Ajouter endpoints dans `CHENU_API_SPECS_v29.md`
   - Format OpenAPI/Swagger

2. **System Manual**:
   - Ajouter section dans `CHENU_SYSTEM_MANUAL.md`
   - Expliquer usage, configuration, limites

3. **Agent Prompts** (si agent):
   - Ajouter template dans `CHENU_AGENT_PROMPTS_v29.md`
   - Définir personnalité, capacités, limites

4. **Diagrams** (si flux complexe):
   - Ajouter diagramme Mermaid dans `CHENU_MERMAID_DIAGRAMS_v29.md`
   - Montrer flux de données, interactions

**Exemple API doc:**

```markdown
## Budget Prediction Endpoint

**POST** `/api/v1/personal/budget/predict`

**Description:** Génère prédictions de dépenses futures basées sur historique.

**Request:**
```json
{
  "user_id": "uuid",
  "months_ahead": 3,
  "categories": ["food", "transport", "housing"]
}
```

**Response:**
```json
{
  "predictions": [
    {"month": "2025-01", "category": "food", "amount": 450.50},
    {"month": "2025-02", "category": "food", "amount": 460.20}
  ],
  "confidence": 0.85
}
```
```

---

### ÉTAPE 8: R&D APPROVAL & DEPLOYMENT

**Soumettre pour approbation R&D:**

**Checklist finale:**

```markdown
☑ Module codé et testé (coverage ≥70%)
☑ Registry entry INTEGRATED créée
☑ Documentation complète ajoutée
☑ Aucune logique parallèle détectée
☑ Aucune violation frontières sphères
☑ Performance validée (<500ms)
☑ Security review passée (si données sensibles)
☑ LOCKED status déterminé

Approuvé par:
- Dev Lead: ___________________________
- Architect (Jo): ___________________________
- Date: ___________________________
```

**Déployement:**

1. Merge vers `main` branch
2. Mise à jour version: `v42.X` → `v42.X+1`
3. Deploy staging → test → production
4. Monitoring 24h post-deploy
5. Rollback plan activé si issues

---

## 🔄 PROCESSUS POUR MODIFICATIONS DE MODULES LOCKED

**RÈGLE SPÉCIALE:** Modules LOCKED (236 modules) ne peuvent être modifiés sans:

### 1. IMPACT ANALYSIS REQUIRED

```markdown
Module à modifier: ___________________________
LOCKED Status: YES
Raison modification: ___________________________

IMPACT ANALYSIS:
☐ Modules dépendants identifiés: [liste]
☐ Agents affectés: [liste]
☐ APIs affectés: [liste]
☐ Risque régression: [LOW / MEDIUM / HIGH]
☐ Plan rollback défini: [oui/non]
☐ Tests régression préparés: [oui/non]
```

### 2. ARCHITECTURAL REVIEW

**Requis:**
- Revue Jo (Architect)
- Revue équipe R&D complète
- Discussion alternatives (éviter modification si possible)
- Documentation changement breaking

### 3. VERSIONING

**Modification LOCKED module = MAJOR VERSION BUMP**

- v42.1 → **v43.0** (breaking change)
- Changelog détaillé
- Migration guide pour utilisateurs
- Deprecation notice (si applicable)

---

## 📊 TEMPLATE NOUVEAU MODULE - QUICK START

**Copier/Coller ce template pour démarrer:**

```python
"""
MODULE: [nom_module].py
SPHERE: [Sphere Name]
VERSION: 1.0.0
INTENT: [Description détaillée]

DEPENDENCIES:
- Core: [list]
- Sphere: [list]
- External: [list]

INTEGRATIONS:
- Calls to: [list]
- Called by: [list]

LOCKED STATUS: NO (new development)

CREATED: [Date]
AUTHOR: [Name]
REGISTRY ENTRY: Line [X] in CHENU_MODULE_REGISTRY_V1_0_SOURCE_OF_TRUTH.md
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import asyncio
import logging

# Module configuration
MODULE_VERSION = "1.0.0"
SPHERE = "[Sphere Name]"
LOCKED = False

logger = logging.getLogger(__name__)

# Models (if applicable)
class [Resource]Model(BaseModel):
    """Model for [resource]."""
    id: str
    name: str
    # ... autres champs

# Main service class
class [ModuleName]Service:
    """
    Service pour [description].
    
    Attributes:
        sphere (str): Sphère propriétaire
        locked (bool): Status LOCKED
    """
    
    def __init__(self):
        self.sphere = SPHERE
        self.locked = LOCKED
        logger.info(f"[ModuleName]Service initialized for sphere: {SPHERE}")
    
    async def main_function(self, param: str) -> Dict[str, Any]:
        """
        Fonction principale du service.
        
        Args:
            param: Description paramètre
        
        Returns:
            Dict contenant résultats
        
        Raises:
            ValueError: Si param invalide
        """
        try:
            # Implementation
            result = {}
            return result
        except Exception as e:
            logger.error(f"Error in main_function: {e}")
            raise
    
    async def validate_sphere_access(self, target_sphere: str) -> bool:
        """
        Valide accès cross-sphere (si applicable).
        
        Args:
            target_sphere: Sphère cible
        
        Returns:
            True si accès autorisé, False sinon
        """
        if target_sphere == self.sphere:
            return True
        
        # Cross-sphere requires validation
        logger.warning(f"Cross-sphere access requested: {self.sphere} -> {target_sphere}")
        # TODO: Implement governance check
        return False

# Exports
__all__ = ['[ModuleName]Service', '[Resource]Model']
```

**Tests template:**

```python
"""
TESTS: test_[nom_module].py
MODULE: [nom_module].py
COVERAGE TARGET: ≥70%
"""

import pytest
from backend.services.[nom_module] import [ModuleName]Service

class Test[ModuleName]Service:
    
    @pytest.fixture
    def service(self):
        return [ModuleName]Service()
    
    def test_initialization(self, service):
        """Test service initialization."""
        assert service.sphere == "[Sphere Name]"
        assert service.locked == False
    
    @pytest.mark.asyncio
    async def test_main_function(self, service):
        """Test main function."""
        result = await service.main_function("test_param")
        assert result is not None
        # ... autres assertions
    
    @pytest.mark.asyncio
    async def test_sphere_isolation(self, service):
        """Test sphere boundary enforcement."""
        # Verify same sphere access allowed
        assert await service.validate_sphere_access("[Sphere Name]") == True
        
        # Verify cross-sphere requires validation
        assert await service.validate_sphere_access("Other Sphere") == False
    
    def test_error_handling(self, service):
        """Test error handling."""
        with pytest.raises(ValueError):
            # Test error case
            pass
```

---

## 🎯 EXEMPLES CONCRETS

### Exemple 1: Nouveau Service Personal Sphere

**Étape 1 - Pre-Integration:**
```markdown
☑ Nom: personal_habit_tracker.py
☑ Sphère: Personal
☑ Intent: Track daily habits with AI insights
☑ Équivalent existant: NONE
☑ Logique parallèle: NONE
☑ Approbation R&D: [Jo - 2025-12-21]
```

**Étape 2 - Registry Entry:**
```markdown
| personal_habit_tracker.py | Personal | PLANNED | N/A | TBD | Intent: Track daily habits with AI insights |
```

**Étapes 3-5:** Coder, tester (voir templates ci-dessus)

**Étape 6 - Registry Update:**
```markdown
| personal_habit_tracker.py | Personal | INTEGRATED | main_v42_unified.py personal | YES | Active v42.2, 78% coverage |
```

**Étape 7:** Documentation ajoutée

**Étape 8:** Approuvé → Deployed v42.2

---

### Exemple 2: Nouveau Agent Creative Sphere

**Étape 1 - Pre-Integration:**
```markdown
☑ Nom: music_composer_agent.py
☑ Sphère: Creative Studio
☑ Intent: AI music composition assistant
☑ Équivalent existant: NONE (42 creative agents, aucun musique)
☑ Logique parallèle: NONE
☑ Approbation R&D: [Jo - 2025-12-21]
```

**Registry Entry:**
```markdown
| music_composer_agent.py | Creative Studio | INTEGRATED | backend/agents/creative/ | YES | Agent #43, Suno API integration |
```

---

## 📋 CHECKLIST FINALE PRE-COMMIT

**AVANT de commit TOUT nouveau module:**

```markdown
MODULE INTEGRATION CHECKLIST

☐ 1. Pre-integration checklist complétée
☐ 2. Registry entry créée (PLANNED status)
☐ 3. Dependencies documentées
☐ 4. Code développé selon standards
☐ 5. Tests écrits (coverage ≥70%)
☐ 6. Tests passent (pytest -v --cov)
☐ 7. Registry updated (INTEGRATED status)
☐ 8. Documentation complète ajoutée
☐ 9. R&D approval obtenue
☐ 10. Performance validée (<500ms)
☐ 11. Security review passée
☐ 12. LOCKED status déterminé
☐ 13. Version bumped appropriately
☐ 14. Changelog updated
☐ 15. Deploy plan confirmé

Approvals:
- Dev: ___________________________
- Architect: ___________________________
- Date: ___________________________

READY TO COMMIT: YES / NO
```

---

## 🚨 VIOLATIONS & CONSÉQUENCES

**Violation du processus d'intégration:**

1. **Module non-documenté dans Registry:** Code rejeté, revert immédiat
2. **Logique parallèle détectée:** Refactoring obligatoire avant merge
3. **Tests insuffisants (<70%):** Merge bloqué jusqu'à coverage atteint
4. **Modification LOCKED sans approval:** Revert immédiat + incident report
5. **Cross-sphere sans validation:** Code rejeté, design review requis

**Processus de résolution:**
1. Violation détectée → CI/CD bloque merge
2. Notification dev + architect
3. Fix required avec timeline
4. Re-review après fix
5. Post-mortem si violation majeure

---

## 📞 SUPPORT & QUESTIONS

**Questions processus d'intégration:**
- Contact: Jo (Architect)
- Documentation: Ce fichier + MODULE REGISTRY
- Updates: Processus mis à jour quarterly

**Changements au processus:**
- Proposer via: GitHub issue avec label "process-improvement"
- Review: Monthly R&D meeting
- Approval: R&D + Architect consensus

---

╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                      🔒 PROCESSUS OFFICIEL 🔒                                ║
║                                                                               ║
║  Ce processus est OBLIGATOIRE pour tout développement de module.              ║
║  AUCUNE exception sans approbation explicite Architect.                       ║
║                                                                               ║
║  Violations = Code rejected + Incident report                                 ║
║                                                                               ║
║  Version: 1.0                                                                 ║
║  Effective Date: 21 Décembre 2025                                            ║
║  Authority: R&D + Architect                                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

© 2025 CHE·NU™
MODULE INTEGRATION PROCESS V1.0

"PROCESS BEFORE CODE. GOVERNANCE BEFORE EXECUTION."

🔧 PROCESSUS COMPLET ✅
