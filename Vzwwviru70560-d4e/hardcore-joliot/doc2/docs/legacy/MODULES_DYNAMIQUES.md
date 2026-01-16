# CHE·NU — Modules Dynamiques & Évolution Contrôlée (V1)

## 1. Objectif

Permettre aux IA et aux utilisateurs de créer de nouveaux modules ("plugins") sans casser le noyau.

---

## 2. Modules Noyau vs Dynamiques

### 2.1 Comparaison

| Aspect | Module Noyau | Module Dynamique |
|--------|--------------|------------------|
| **Définition** | `chenu_spaces_modules.json` | Table `dynamic_modules` |
| **Modification** | Intervention Architecte | Via Creation Room |
| **Suppression** | Impossible | Possible |
| **Validation** | Pre-intégré | Validation requise |
| **Statut** | Toujours actif | Activable/Désactivable |

### 2.2 Modules Noyau (Intouchables)

```json
{
  "core_modules": [
    "auth",
    "controller", 
    "types",
    "spaces",
    "config",
    "security",
    "session",
    "cache"
  ]
}
```

### 2.3 Modules Dynamiques

Les modules dynamiques sont des extensions créées par:
- Les utilisateurs (via Creation Room)
- Les agents IA (avec validation)
- L'équipe CHE·NU (modules officiels optionnels)

---

## 3. Schéma de Données

### 3.1 SQL Schema

```sql
-- Table principale des modules dynamiques
CREATE TABLE dynamic_modules (
  id SERIAL PRIMARY KEY,
  uuid UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
  
  -- Identification
  scope VARCHAR(32) NOT NULL,         -- Espace cible
  category VARCHAR(64) NOT NULL,      -- Catégorie dans l'espace
  key VARCHAR(64) NOT NULL,           -- Clé unique du module
  label TEXT NOT NULL,                -- Nom affiché
  description TEXT,                   -- Description
  version VARCHAR(20) DEFAULT '1.0.0',
  
  -- Origine
  created_by_agent BOOLEAN DEFAULT FALSE,
  created_by_user BOOLEAN DEFAULT FALSE,
  creator_id UUID,                    -- ID du créateur
  
  -- Statut
  is_enabled BOOLEAN DEFAULT FALSE,   -- Actif ou non
  is_validated BOOLEAN DEFAULT FALSE, -- Validé ou non
  is_official BOOLEAN DEFAULT FALSE,  -- Module officiel
  
  -- Visibilité
  visibility VARCHAR(20) DEFAULT 'private',
  
  -- Métadonnées
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  validated_at TIMESTAMP,
  validated_by UUID,
  
  -- Contenu
  config JSONB DEFAULT '{}',          -- Configuration
  components JSONB DEFAULT '{}',      -- Composants (frontend, backend)
  dependencies JSONB DEFAULT '[]',    -- Dépendances
  permissions JSONB DEFAULT '[]',     -- Permissions requises
  
  -- Contraintes
  UNIQUE(scope, category, key)
);

-- Index pour la recherche
CREATE INDEX idx_dynamic_modules_scope ON dynamic_modules(scope);
CREATE INDEX idx_dynamic_modules_enabled ON dynamic_modules(is_enabled);
CREATE INDEX idx_dynamic_modules_creator ON dynamic_modules(creator_id);

-- Table de l'historique des versions
CREATE TABLE dynamic_module_versions (
  id SERIAL PRIMARY KEY,
  module_id INTEGER REFERENCES dynamic_modules(id),
  version VARCHAR(20) NOT NULL,
  changelog TEXT,
  config JSONB,
  components JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  created_by UUID
);

-- Table des reviews
CREATE TABLE dynamic_module_reviews (
  id SERIAL PRIMARY KEY,
  module_id INTEGER REFERENCES dynamic_modules(id),
  reviewer_id UUID NOT NULL,
  status VARCHAR(20) NOT NULL,        -- 'pending', 'approved', 'rejected'
  notes TEXT,
  criteria_results JSONB,
  reviewed_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 Pydantic Schema

```python
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class ModuleVisibility(str, Enum):
    PRIVATE = "private"
    TEAM = "team"
    COMMUNITY = "community"
    OFFICIAL = "official"

class DynamicModuleBase(BaseModel):
    scope: str
    category: str
    key: str
    label: str
    description: Optional[str] = None
    version: str = "1.0.0"

class DynamicModuleCreate(DynamicModuleBase):
    config: Dict[str, Any] = {}
    components: Dict[str, List[str]] = {
        "frontend": [],
        "backend": [],
        "api": []
    }
    dependencies: List[str] = []
    permissions: List[str] = []

class DynamicModule(DynamicModuleBase):
    id: int
    uuid: UUID
    created_by_agent: bool
    created_by_user: bool
    creator_id: Optional[UUID]
    is_enabled: bool
    is_validated: bool
    is_official: bool
    visibility: ModuleVisibility
    created_at: datetime
    updated_at: datetime
    validated_at: Optional[datetime]
    validated_by: Optional[UUID]
    config: Dict[str, Any]
    components: Dict[str, List[str]]
    dependencies: List[str]
    permissions: List[str]
```

---

## 4. Cycle de Vie d'un Module Dynamique

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 CYCLE DE VIE D'UN MODULE DYNAMIQUE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. 📝 CRÉATION                                                         │
│     │  • Via Creation Room                                             │
│     │  • Par utilisateur ou agent IA                                   │
│     │                                                                   │
│     ▼                                                                   │
│  2. 💾 DRAFT                                                            │
│     │  • Sauvegardé mais non actif                                     │
│     │  • Modifiable librement                                          │
│     │                                                                   │
│     ▼                                                                   │
│  3. 📤 SOUMISSION                                                       │
│     │  • Soumis pour validation                                        │
│     │  • Tests automatiques lancés                                     │
│     │                                                                   │
│     ▼                                                                   │
│  4. 🔍 VALIDATION                                                       │
│     │  ├── Privé → Auto-validé                                         │
│     │  ├── Équipe → Review Agent                                       │
│     │  └── Public → Review Architecte                                  │
│     │                                                                   │
│     ▼                                                                   │
│  5. ✅ ACTIVATION                                                       │
│     │  • Module activé                                                 │
│     │  • Disponible dans CHE·NU                                        │
│     │                                                                   │
│     ▼                                                                   │
│  6. 🔄 MISE À JOUR (optionnel)                                          │
│     │  • Nouvelle version                                              │
│     │  • Re-validation si nécessaire                                   │
│     │                                                                   │
│     ▼                                                                   │
│  7. 🗑️ DÉSACTIVATION / SUPPRESSION (optionnel)                         │
│        • Désactivable par le créateur                                  │
│        • Supprimable (sauf si dépendances)                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Validation des Modules

### 5.1 Critères de Validation

| Critère | Description | Auto-Check |
|---------|-------------|------------|
| **Structure** | Conforme à ESPACE → CATÉGORIE → MODULE | ✅ |
| **Unicité** | Nom unique dans l'espace | ✅ |
| **Conflits** | Pas de conflit avec modules existants | ✅ |
| **Syntaxe** | Code valide | ✅ |
| **Sécurité** | Pas de code malveillant | ✅ |
| **Documentation** | Documentation minimale | ⚠️ |
| **Tests** | Tests passent | ⚠️ |
| **Performance** | Pas d'impact négatif | ❌ |

### 5.2 Process par Visibilité

| Visibilité | Validateur | Délai |
|------------|------------|-------|
| **Privé** | Auto | Immédiat |
| **Équipe** | Agent L2 | Minutes |
| **Communauté** | Architecte | Heures |
| **Officiel** | Architecte + Nova | Jours |

---

## 6. Gestion des Dépendances

### 6.1 Types de Dépendances

```python
class DependencyType(str, Enum):
    REQUIRED = "required"       # Obligatoire
    OPTIONAL = "optional"       # Optionnel
    PEER = "peer"               # Version compatible
    DEV = "dev"                 # Développement uniquement
```

### 6.2 Résolution

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RÉSOLUTION DES DÉPENDANCES                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Module A veut être installé                                           │
│      │                                                                  │
│      ▼                                                                  │
│  Analyse des dépendances:                                              │
│  • Module B (required) → Vérifie si présent et compatible              │
│  • Module C (optional) → Note si absent                                │
│      │                                                                  │
│      ▼                                                                  │
│  Si dépendance manquante:                                              │
│  • Propose d'installer                                                 │
│  • Ou refuse l'installation                                            │
│      │                                                                  │
│      ▼                                                                  │
│  Installation dans l'ordre:                                            │
│  1. Dépendances required                                               │
│  2. Module A                                                           │
│  3. Dépendances optional (si demandé)                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API des Modules Dynamiques

### 7.1 Endpoints

```python
# CRUD
POST   /api/v1/modules/dynamic           # Créer
GET    /api/v1/modules/dynamic           # Lister
GET    /api/v1/modules/dynamic/{id}      # Détail
PUT    /api/v1/modules/dynamic/{id}      # Modifier
DELETE /api/v1/modules/dynamic/{id}      # Supprimer

# Lifecycle
POST   /api/v1/modules/dynamic/{id}/submit     # Soumettre
POST   /api/v1/modules/dynamic/{id}/validate   # Valider (review)
POST   /api/v1/modules/dynamic/{id}/activate   # Activer
POST   /api/v1/modules/dynamic/{id}/deactivate # Désactiver

# Versions
GET    /api/v1/modules/dynamic/{id}/versions   # Historique
POST   /api/v1/modules/dynamic/{id}/versions   # Nouvelle version
POST   /api/v1/modules/dynamic/{id}/rollback   # Rollback

# Recherche
GET    /api/v1/modules/dynamic/search          # Rechercher
GET    /api/v1/modules/dynamic/by-space/{space} # Par espace
```

### 7.2 Exemple de Création

```python
# POST /api/v1/modules/dynamic

{
  "scope": "ENTREPRISE",
  "category": "Finance",
  "key": "stock_management",
  "label": "Gestion des Stocks",
  "description": "Module de gestion d'inventaire",
  "version": "1.0.0",
  "config": {
    "default_warehouse": "main",
    "alert_threshold": 10
  },
  "components": {
    "frontend": ["StockDashboard.tsx", "StockForm.tsx"],
    "backend": ["stock_service.py", "stock_models.py"],
    "api": ["GET /stocks", "POST /stocks", "PUT /stocks/{id}"]
  },
  "dependencies": ["core_auth", "core_database"],
  "permissions": ["read:stocks", "write:stocks"]
}
```

---

## 8. Évolution Contrôlée

### 8.1 Principe

L'évolution de CHE·NU est **contrôlée** :

```
┌────────────────────────────────────────────────────────────────────────┐
│               ÉVOLUTION CONTRÔLÉE CHE·NU                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  IMMUABLE (jamais modifié):                                           │
│  ├── 10 Espaces                                                        │
│  ├── 6 Actions universelles                                           │
│  ├── Règles A, B, C                                                   │
│  └── Modules noyau                                                    │
│                                                                        │
│  ÉVOLUTIF (avec validation):                                          │
│  ├── Catégories (ajout possible)                                      │
│  ├── Modules dynamiques                                               │
│  ├── Agents personnalisés                                             │
│  └── Univers personnalisés                                            │
│                                                                        │
│  LIBRE (sans validation):                                             │
│  ├── Contenu utilisateur                                              │
│  ├── Préférences personnelles                                         │
│  └── Monde personnel                                                  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Rôle de CHE-Learn

CHE-Learn propose des évolutions basées sur:

1. **Analyse des usages**: Détecte les patterns répétitifs
2. **Identification des manques**: Repère les besoins non couverts
3. **Proposition de modules**: Suggère de nouveaux modules
4. **Optimisation**: Propose des améliorations

**Exemple:**

```
CHE-Learn: "J'ai remarqué que vous créez souvent des tâches
liées à la gestion de stocks. Voulez-vous que je crée un
module dédié 'Gestion des Stocks' dans ENTREPRISE/Finance?"

[Approuver] [Refuser] [Personnaliser]
```

---

## 9. Sécurité

### 9.1 Sandbox

Les modules dynamiques s'exécutent dans un environnement isolé:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SANDBOX MODULE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Module Dynamique                                                       │
│  ├── Accès limité aux API autorisées                                   │
│  ├── Ressources limitées (CPU, mémoire)                                │
│  ├── Pas d'accès direct à la DB                                        │
│  ├── Pas d'accès au système de fichiers                                │
│  └── Timeout sur les opérations                                        │
│                                                                         │
│  Communication via:                                                     │
│  ├── API CHE·NU (avec permissions)                                     │
│  ├── Events (publication/souscription)                                 │
│  └── Storage dédié (key-value)                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Permissions

Chaque module déclare ses permissions:

```python
permissions = [
    "read:tasks",          # Lire les tâches
    "write:tasks",         # Écrire les tâches
    "read:projects",       # Lire les projets
    "notify:user",         # Envoyer des notifications
    "call:external_api",   # Appeler APIs externes
]
```

---

## 10. Règles des Modules Dynamiques

```
┌────────────────────────────────────────────────────────────────────────┐
│               RÈGLES DES MODULES DYNAMIQUES                            │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  D.1  Un module dynamique ne peut PAS modifier le noyau               │
│                                                                        │
│  D.2  Un module dynamique appartient à UN SEUL espace                 │
│                                                                        │
│  D.3  Les dépendances doivent être explicitement déclarées            │
│                                                                        │
│  D.4  La validation est obligatoire pour visibilité > privé           │
│                                                                        │
│  D.5  Le créateur peut désactiver/supprimer (sauf si dépendances)     │
│                                                                        │
│  D.6  Les modules officiels sont maintenus par l'équipe CHE·NU        │
│                                                                        │
│  D.7  Rollback possible sur toute version précédente                  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

**CHE·NU V25** — *"Évoluer sans casser."* 🔧
