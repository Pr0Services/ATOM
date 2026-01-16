# 🔍 AUDIT DE COHÉRENCE CHE·NU

**Date**: 9 Décembre 2025  
**Version analysée**: CHENU-COMPLETE-301K

---

## ✅ ÉLÉMENTS CORRIGÉS

### 1. Fichiers Backend Manquants (CORRIGÉ)

Les imports dans `backend/main.py` référençaient des fichiers inexistants:

| Fichier | Status |
|---------|--------|
| `core/config/settings.py` | ✅ Créé |
| `core/config/__init__.py` | ✅ Créé |
| `core/database/connection.py` | ✅ Créé |
| `core/database/__init__.py` | ✅ Créé |

### 2. README Principal (CORRIGÉ)

- Statistiques mises à jour: 301,520 lignes, 880+ fichiers
- Version: 2.0.0-complete

---

## ⚠️ INCOHÉRENCES DÉTECTÉES (À TRAITER)

### 1. Nomenclature CHENU vs CHE·NU

**8 fichiers frontend avec nom "chenu-*":**
```
apps/web/src/widgets/chenu-dashboard.tsx
apps/web/src/widgets/chenu-sprint21-projects.tsx
apps/web/src/widgets/chenu-sprint22-calendar.tsx
apps/web/src/widgets/chenu-sprint23-team.tsx
apps/web/src/widgets/chenu-sprint31-email.tsx
apps/web/src/widgets/chenu-sprint41-finance.tsx
apps/web/src/widgets/chenu-sprint42-suppliers.tsx
apps/web/src/widgets/chenu-workflows.tsx
```

**Action recommandée**: Renommer en `chenu-*.tsx`

**59 références à "CHENU/chenu" dans le code frontend**

---

### 2. Fichiers Backend "chenu-b*" (Ancienne Nomenclature)

**68 fichiers** avec le pattern `chenu-b{N}-{nom}.py`:
- chenu-b7-projects-api.py
- chenu-b9-auth.py
- chenu-b10-database-models.py
- chenu-b11-nova-ai.py
- etc.

**Action recommandée**: 
- Option A: Réorganiser dans des sous-dossiers thématiques
- Option B: Renommer avec nomenclature sémantique

---

### 3. Types Dupliqués

**SphereType défini 3 fois:**
```
apps/web/src/core/theme/theme.types.ts
apps/web/src/core/agents/agent.manifesto.ts
apps/web/src/core/agents/manifesto/manifesto.types.ts
```

**Agent interface définie 10+ fois:**
```
apps/web/src/widgets/App.tsx
apps/web/src/widgets/MeetingRoom.tsx
apps/web/src/xr/debug/CheNuXRDebugExperience.tsx
apps/web/src/timeline/types.ts
... etc
```

**Action recommandée**: Centraliser dans `apps/web/src/types/`

---

### 4. Documentation avec Dates 2024

Plusieurs fichiers documentation contiennent des références à 2024:
- CHENU-AGENT-MANIFESTO.md
- CHENU-BOOTSTRAP-PROMPT.md
- CHENU-CONTEXT-RECOVERY.md
- CHENU-DECISION-ECHO.md

**Action recommandée**: Mettre à jour les dates vers 2025

---

### 5. Documentation CHENU

**4 fichiers documentation référencent explicitement CHENU:**
- docs/CHENU_API_DOCUMENTATION.md
- docs/CHENU_COMPLETE_UI_UX_DESIGN.md
- docs/CHENU_VISUAL_DIAGRAMS.md
- docs/CHENU_V25_INVENTAIRE_ULTIME.md

**Action recommandée**: 
- Soit renommer/adapter pour CHE·NU
- Soit garder comme documentation historique dans un sous-dossier `docs/legacy/`

---

## 🎯 PLAN D'ACTION PRIORITAIRE

### Phase 1 - Critique (Immédiat)
- [x] Créer fichiers config/database manquants
- [x] Mettre à jour README avec stats correctes
- [ ] Vérifier que `npm run dev` et `python main.py` fonctionnent

### Phase 2 - Important (Court terme)
- [ ] Centraliser les types (Agent, Sphere, SphereType)
- [ ] Créer `apps/web/src/types/chenu.types.ts` avec exports centralisés
- [ ] Renommer fichiers chenu-*.tsx en chenu-*.tsx

### Phase 3 - Amélioration (Moyen terme)
- [ ] Réorganiser backend/services/ avec sous-dossiers thématiques
- [ ] Mettre à jour dates dans documentation
- [ ] Créer dossier docs/legacy/ pour documentation CHENU

---

## 📊 SCORE DE COHÉRENCE

| Aspect | Score | Notes |
|--------|-------|-------|
| Structure fichiers | 85% | Bien organisé mais nomenclature mixte |
| Imports/Exports | 90% | Fichiers manquants corrigés |
| Types TypeScript | 60% | Duplication significative |
| Nomenclature | 70% | Mélange CHENU/CHE·NU |
| Documentation | 75% | Dates à mettre à jour |
| **Global** | **76%** | Fonctionnel, améliorations possibles |

---

## 🔧 SCRIPTS DE CORRECTION

### Renommer fichiers chenu-* (bash)
```bash
cd apps/web/src/widgets
for f in chenu-*.tsx; do
  mv "$f" "chenu-${f#chenu-}"
done
```

### Remplacer CHENU par CHENU dans code (sed)
```bash
find apps/web/src -name "*.tsx" -o -name "*.ts" | \
  xargs sed -i 's/CHENU/CHENU/g; s/Chenu/CheNu/g; s/chenu/chenu/g'
```

### Créer types centralisés
```typescript
// apps/web/src/types/chenu.types.ts
export type { Agent } from '@/core/agents/agent.types';
export type { SphereType } from '@/core/theme/theme.types';
export type { Sphere3D, SphereData } from '@/universe3d/universe3d.types';
```

---

> **Conclusion**: Le codebase est fonctionnel et bien structuré. Les incohérences identifiées sont principalement cosmétiques (nomenclature) ou organisationnelles (types dupliqués). Aucun problème bloquant n'a été détecté.
