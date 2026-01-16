# CHE·NU™ MIGRATION GUIDE
## De 10 sphères → 8 sphères + Bureaux max 6 flexibles

---

## ⚠️ CHANGEMENTS CRITIQUES

### AVANT (Ancien)
- **10 sphères** (avec Scholar, Methodology, IA Lab, XR Immersive séparées)
- **10 sections bureau fixes** (Dashboard, Notes, Tasks, Projects, Threads, Meetings, Data, Agents, Reports, Budget)

### APRÈS (Nouveau - OFFICIEL)
- **8 sphères** uniquement
- **MAX 6 sections bureau FLEXIBLES** (l'utilisateur choisit parmi 10 disponibles)

---

## 📋 LES 8 SPHÈRES OFFICIELLES

| # | ID | Nom | Emoji | Ce qui est inclus |
|---|-----|-----|-------|-------------------|
| 1 | `personal` | Personal | 🏠 | Vie privée, santé, famille |
| 2 | `business` | Business | 💼 | Travail, projets, clients |
| 3 | `government` | Government & Institutions | 🏛️ | Gouvernement, conformité, légal |
| 4 | `studio` | Creative Studio | 🎨 | Art, design, contenu, **+ Scholar** |
| 5 | `community` | Community | 👥 | Relations locales, associations |
| 6 | `social` | Social & Media | 📱 | Médias sociaux, présence en ligne |
| 7 | `entertainment` | Entertainment | 🎬 | Loisirs, films, jeux, voyage |
| 8 | `team` | My Team | 🤝 | Équipe, **+ IA Labs + Skills & Tools + Methodology** |

---

## 🔄 MAPPING DES ANCIENNES SPHÈRES

| Ancienne sphère | → | Nouvelle sphère | Raison |
|-----------------|---|-----------------|--------|
| `scholar` | → | `studio` | La recherche est création intellectuelle |
| `methodology` | → | `team` | Méthodes = outils d'équipe |
| `ia-lab` | → | `team` | IA Labs fait partie de My Team |
| `ia_labs` | → | `team` | (alias) |
| `skills_tools` | → | `team` | Skills & Tools fait partie de My Team |
| `xr-immersive` | → | **MODE** | XR n'est PAS une sphère, c'est un mode |
| `institutions` | → | `government` | (alias) |
| `creative-studio` | → | `studio` | (alias) |
| `social-media` | → | `social` | (alias) |
| `my-team` | → | `team` | (alias) |

---

## 📊 BUREAUX — MAX 6 FLEXIBLES

### Catalogue des sections disponibles (10)
L'utilisateur peut choisir **MAXIMUM 6** parmi:

| ID | Nom | Emoji |
|----|-----|-------|
| `dashboard` | Dashboard | 📊 |
| `notes` | Notes | 📝 |
| `tasks` | Tasks | ✅ |
| `projects` | Projects | 📁 |
| `threads` | Threads (.chenu) | 🧵 |
| `meetings` | Meetings | 📅 |
| `data` | Data | 💾 |
| `agents` | Agents | 🤖 |
| `reports` | Reports | 📈 |
| `budget` | Budget | 💰 |

### Configuration par défaut
```typescript
const DEFAULT_BUREAU_SECTIONS = [
  'dashboard',
  'notes',
  'tasks',
  'projects',
  'threads',
  'agents'
];
```

---

## 🔧 FICHIERS À MIGRER

### Fichiers avec 10 sphères (à corriger)
```
/frontend/src/config/spheres.config.ts
/ui/src/config/spheres.config.ts
/sdk/core/spheres.config.ts
/sdk_v30/core/spheres.config.ts
/api/services/chenu.service.ts
/ui/src/xr/pages/*.tsx
/ui/src/xr/components/*.tsx
```

### Fichiers avec 10 sections bureau (à corriger)
```
/ui/src/components/bureau/BureauContent.tsx
/frontend/src/constants/spheres.ts
/frontend/src/constants/system.ts
```

---

## 🛠️ COMMENT MIGRER LE CODE

### 1. Importer la nouvelle config
```typescript
// ❌ ANCIEN
import { SPHERE_CONFIGS } from './spheres.config';

// ✅ NOUVEAU
import { SPHERES, mapLegacySphere, MAX_BUREAU_SECTIONS } from './SPHERES_BUREAUX_CANONICAL';
```

### 2. Utiliser le mapping legacy
```typescript
// Si vous recevez un ancien ID de sphère
const oldSphereId = 'ia-lab';
const newSphereId = mapLegacySphere(oldSphereId); // → 'team'
```

### 3. Valider les bureaux
```typescript
import { validateBureauSections, MAX_BUREAU_SECTIONS } from './SPHERES_BUREAUX_CANONICAL';

const userSections = ['dashboard', 'notes', 'tasks', 'projects', 'threads', 'agents', 'budget'];
// ❌ 7 sections = INVALIDE

if (!validateBureauSections(userSections)) {
  // Tronquer à 6
  const validSections = userSections.slice(0, MAX_BUREAU_SECTIONS);
}
```

### 4. Supprimer les références XR comme sphère
```typescript
// ❌ ANCIEN - XR comme sphère
const spheres = ['personal', 'business', 'xr-immersive'];

// ✅ NOUVEAU - XR est un MODE
const spheres = ['personal', 'business'];
const viewMode = 'xr'; // Mode de visualisation séparé
```

---

## ⚠️ ERREURS COURANTES À ÉVITER

### ❌ NE PAS FAIRE
```typescript
// Ajouter de nouvelles sphères
const SPHERES = [...existingSpheres, { id: 'new-sphere' }];

// Plus de 6 sections bureau
const bureauSections = ['a', 'b', 'c', 'd', 'e', 'f', 'g']; // 7 = INVALIDE

// Traiter XR comme une sphère
if (sphereId === 'xr-immersive') { ... }
```

### ✅ FAIRE
```typescript
// Utiliser les 8 sphères officielles
import { SPHERES } from './SPHERES_BUREAUX_CANONICAL';

// Limiter à 6 sections
const bureauSections = userSections.slice(0, 6);

// XR est un mode
const isXRMode = viewMode === 'xr';
const currentSphere = SPHERES[sphereId];
```

---

## 📁 SOURCE DE VÉRITÉ

Le fichier `SPHERES_BUREAUX_CANONICAL.ts` est la **source de vérité unique**.

Locations:
- `/config/SPHERES_BUREAUX_CANONICAL.ts` (principal)
- `/ui/src/config/SPHERES_BUREAUX_CANONICAL.ts`
- `/sdk/core/SPHERES_BUREAUX_CANONICAL.ts`
- `/sdk_v30/core/SPHERES_BUREAUX_CANONICAL.ts`
- `/frontend/src/config/SPHERES_BUREAUX_CANONICAL.ts`

---

## ✅ CHECKLIST DE MIGRATION

- [ ] Remplacer imports de l'ancienne config par la nouvelle
- [ ] Utiliser `mapLegacySphere()` pour les IDs legacy
- [ ] Limiter les bureaux à MAX 6 sections
- [ ] Supprimer les références à `scholar`, `methodology`, `ia-lab`, `xr-immersive` comme sphères
- [ ] Traiter XR comme un MODE, pas une sphère
- [ ] Tester que toutes les sphères fonctionnent

---

**Date de migration:** Décembre 2024
**Version:** 2.0 FINAL
