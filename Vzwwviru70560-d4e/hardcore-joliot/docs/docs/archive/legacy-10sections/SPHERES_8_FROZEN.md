# 🌐 CHE·NU™ — 8 SPHÈRES FROZEN

## ⚠️ RÈGLE ABSOLUE — NE PAS MODIFIER

Cette structure est **GELÉE** selon le MEMORY PROMPT.

---

## 📊 LES 8 SPHÈRES OFFICIELLES

| # | ID | Nom | Emoji | Couleur | Description |
|---|-----|-----|-------|---------|-------------|
| 1 | `personal` | Personal | 🏠 | #3EB4A2 | Vie personnelle, santé, famille |
| 2 | `business` | Business | 💼 | #D8B26A | Opérations professionnelles |
| 3 | `government` | Government & Institutions | 🏛️ | #8D8371 | Administratif, légal, gouvernemental |
| 4 | `studio` | Creative Studio | 🎨 | #7A593A | Design, écriture, musique, vidéo |
| 5 | `community` | Community | 👥 | #3F7249 | Forums, groupes, associations |
| 6 | `social` | Social & Media | 📱 | #2F4C39 | Réseaux sociaux, messagerie |
| 7 | `entertainment` | Entertainment | 🎬 | #E9E4D6 | Médias, streaming, jeux |
| 8 | `team` | My Team | 🤝 | #5ED8FF | Collaboration, **IA Labs**, **Skills & Tools** |

---

## ⚠️ CE QUI A CHANGÉ

### AVANT (10 sphères - INCORRECT):
```
❌ ia_labs (sphère séparée)
❌ skills_tools (sphère séparée)
❌ xr-immersive (sphère)
❌ scholar (sphère)
❌ methodology (sphère)
```

### APRÈS (8 sphères - CORRECT):
```
✅ ia_labs → INCLUS dans "My Team"
✅ skills_tools → INCLUS dans "My Team"
✅ xr-immersive → C'est un MODE, pas une sphère
✅ scholar → Fusionné dans "Studio"
✅ methodology → Fusionné dans "My Team"
```

---

## 📁 FICHIERS SOURCE DE VÉRITÉ

```
/ui/src/config/spheres.config.ts       ← SOURCE PRINCIPALE
/sdk/core/spheres.config.ts            ← Copie SDK
/sdk_v30/core/spheres.config.ts        ← Copie SDK v30
/frontend/src/config/spheres.config.ts ← Copie Frontend
/frontend/src/constants/spheres.ts     ← Anciennes constantes (OK)
/web_v30/config/spheres.config.ts      ← Copie Web v30
```

---

## 🔧 MAPPING LEGACY → OFFICIEL

Pour le code existant qui utilise les anciennes sphères:

```typescript
import { mapLegacyToOfficial } from './spheres.config';

// Exemples
mapLegacyToOfficial('ia_labs')      // → 'team'
mapLegacyToOfficial('skills_tools') // → 'team'
mapLegacyToOfficial('creative')     // → 'studio'
mapLegacyToOfficial('institutional')// → 'government'
mapLegacyToOfficial('xr-immersive') // → 'personal'
mapLegacyToOfficial('scholar')      // → 'studio'
mapLegacyToOfficial('methodology')  // → 'team'
```

---

## 📋 10 SECTIONS BUREAU (FROZEN)

Chaque sphère a **exactement** ces 10 sections:

| # | ID | Nom | Emoji |
|---|-----|-----|-------|
| 1 | `dashboard` | Dashboard | 📊 |
| 2 | `notes` | Notes | 📝 |
| 3 | `tasks` | Tasks | ✅ |
| 4 | `projects` | Projects | 📁 |
| 5 | `threads` | Threads (.chenu) | 🧵 |
| 6 | `meetings` | Meetings | 📅 |
| 7 | `data` | Data / Database | 🗄️ |
| 8 | `agents` | Agents | 🤖 |
| 9 | `reports` | Reports / History | 📈 |
| 10 | `budget` | Budget & Governance | 💰 |

---

## 🚫 CONTRAINTES ABSOLUES

- **NE PAS** ajouter de nouvelles sphères
- **NE PAS** renommer les sphères
- **NE PAS** fusionner les sections bureau
- **NE PAS** contourner la gouvernance
- **NE PAS** traiter CHE·NU comme une app générique

---

*Document créé le 18 décembre 2024*
*CHE·NU™ — Governed Intelligence Operating System*
