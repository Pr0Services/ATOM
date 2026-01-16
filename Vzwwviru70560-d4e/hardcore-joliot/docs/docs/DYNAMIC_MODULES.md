# CHE·NU - Documentation Modules Dynamiques

## Vue d'ensemble

Le système de modules dynamiques permet aux **agents IA** de créer des modules personnalisés pour les utilisateurs, sans modifier les modules noyau de CHE·NU.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTRÔLEUR CENTRAL                       │
├─────────────────────────────────────────────────────────────┤
│                          │                                  │
│    ┌─────────────┐       │       ┌─────────────────┐       │
│    │   MODULES   │       │       │     MODULES     │       │
│    │    NOYAU    │◄──────┼──────►│   DYNAMIQUES    │       │
│    │             │       │       │                 │       │
│    │ (read-only) │       │       │ (créés par IA)  │       │
│    └─────────────┘       │       └─────────────────┘       │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    │   FUSION    │
                    │  & ROUTING  │
                    └─────────────┘
```

## Règles Fondamentales

### 1. Protection des Modules Noyau
```
⚠️ L'IA ne modifie JAMAIS les modules noyau
```
- Les modules noyau sont définis dans `chenu_config.json`
- Ils sont en lecture seule
- Seuls les administrateurs peuvent les modifier via le code

### 2. Validation des Scopes
```
⚠️ L'IA ne crée un module que dans un scope+category valide
```

**Scopes valides (10 espaces):**
| Scope | Label |
|-------|-------|
| `personal` | Personnel |
| `social` | Social & Divertissement |
| `scholar` | Scholar |
| `home` | Maison |
| `enterprise` | Entreprise |
| `projects` | Projets |
| `creative_studio` | Creative Studio |
| `government` | Gouvernement |
| `immobilier` | Immobilier |
| `associations` | Associations |

### 3. Nomenclature
```
⚠️ Chaque module dynamique a un nom machine (key) + label humain
```
- **key**: snake_case, unique par scope (ex: `budget_tracker`)
- **label**: Nom affiché (ex: "Suivi de Budget")

## Flux de Création

### A. Création Directe (Utilisateur)
```
Utilisateur → POST /api/v1/modules/dynamic → Module Créé
```

### B. Proposition IA (Recommandé)
```
Agent IA → POST /api/v1/modules/proposals → Proposition en attente
                                                    ↓
                                          Notification User
                                                    ↓
                                    User approuve/rejette
                                                    ↓
                               Module créé (si approuvé)
```

## API Reference

### Endpoints Principaux

#### Lister les modules
```http
GET /api/v1/modules/dynamic
GET /api/v1/modules/dynamic/{scope}
```

#### Créer un module
```http
POST /api/v1/modules/dynamic
Content-Type: application/json

{
  "scope": "personal",
  "category": "custom",
  "key": "meditation_tracker",
  "label": "Suivi Méditation",
  "description": "Suivez vos séances de méditation",
  "icon": "brain",
  "color": "#3EB4A2",
  "actions": [
    {"key": "log_session", "label": "Enregistrer une séance"},
    {"key": "view_stats", "label": "Voir les statistiques"}
  ]
}
```

#### Proposer un module (IA)
```http
POST /api/v1/modules/proposals
Content-Type: application/json

{
  "scope": "personal",
  "category": "health",
  "key": "sleep_tracker",
  "label": "Suivi du Sommeil",
  "description": "Analysez votre qualité de sommeil",
  "reason": "J'ai remarqué que vous mentionnez souvent des problèmes de sommeil. Ce module pourrait vous aider à mieux comprendre vos habitudes.",
  "conversation_context": {"last_topic": "fatigue"}
}
```

#### Approuver/Rejeter une proposition
```http
POST /api/v1/modules/proposals/{id}/approve
POST /api/v1/modules/proposals/{id}/reject
```

#### Désactiver/Réactiver un module
```http
DELETE /api/v1/modules/dynamic/{id}
POST /api/v1/modules/dynamic/{id}/enable
```

### Obtenir tous les modules (fusion)
```http
GET /api/v1/modules/merged/{scope}

Response:
{
  "scope": "personal",
  "core": [...],      // Modules noyau
  "dynamic": [...],   // Modules dynamiques
  "total_count": 15
}
```

## Base de Données

### Table `dynamic_modules`
```sql
id UUID PRIMARY KEY
scope VARCHAR(50)           -- Espace CHE·NU
category VARCHAR(100)       -- Catégorie dans l'espace
key VARCHAR(100)            -- Nom machine (unique/scope)
label VARCHAR(200)          -- Nom affiché
description TEXT
icon VARCHAR(50)
color VARCHAR(7)
config JSONB                -- Configuration flexible
actions JSONB               -- Actions disponibles
created_by_agent VARCHAR    -- Agent IA créateur
created_by_user UUID        -- Utilisateur propriétaire
is_enabled BOOLEAN
is_approved BOOLEAN
usage_count INTEGER
```

### Table `dynamic_module_proposals`
```sql
id UUID PRIMARY KEY
scope, category, key, label, description, icon, color
proposed_by_agent VARCHAR   -- ID de l'agent
proposed_for_user UUID      -- Utilisateur cible
reason TEXT                 -- Justification de l'IA
conversation_context JSONB  -- Contexte de conversation
status VARCHAR(20)          -- pending/approved/rejected/expired
expires_at TIMESTAMP        -- Expiration (7 jours)
```

## Intégration Frontend

### Composant Principal
```tsx
import { DynamicModulesSection } from '@/components/DynamicModules';

// Dans le dashboard d'un espace
<DynamicModulesSection
  currentScope="personal"
  scopeLabel="Personnel"
/>
```

### Affichage
- Section "Modules personnalisés" par espace
- Badge "IA" sur les modules créés par un agent
- Notifications pour les propositions en attente
- Actions: Approuver/Rejeter/Activer/Désactiver

## Bonnes Pratiques pour les Agents IA

### DO ✅
- Proposer des modules pertinents basés sur le contexte
- Inclure une raison claire et utile
- Utiliser des catégories existantes quand possible
- Suggérer des actions concrètes

### DON'T ❌
- Créer des modules sans raison
- Dupliquer des fonctionnalités noyau
- Utiliser des catégories invalides
- Proposer des modules trop génériques

### Exemple de Proposition Contextuelle
```python
# L'utilisateur parle de son budget
if "budget" in conversation_topics and not has_budget_module(user):
    await propose_module(
        scope="personal",
        category="finance",
        key="budget_analyzer",
        label="Analyseur de Budget",
        reason="Vous avez mentionné vouloir mieux gérer votre budget. "
               "Ce module vous permettra de suivre vos dépenses et "
               "visualiser où va votre argent.",
        actions=[
            {"key": "add_expense", "label": "Ajouter une dépense"},
            {"key": "view_chart", "label": "Voir le graphique"},
            {"key": "set_limit", "label": "Définir un plafond"}
        ]
    )
```

## Sécurité

- Les propositions expirent après 7 jours
- Validation stricte des scopes/catégories
- Logs de toutes les actions
- Soft delete (désactivation) uniquement

---

**Version:** 1.0  
**Dernière mise à jour:** 5 décembre 2025
