# 🎯 CHE·NU™ — GUIDE DES LAYOUTS & VERSIONS FLEXIBLES

## Vue d'ensemble

Ce document répertorie les **MEILLEURES VERSIONS** des composants layout trouvées dans le codebase.

---

## 📊 STATISTIQUES TOTALES

| Métrique | Valeur |
|----------|--------|
| **Fichiers code** | 2,411 |
| **Lignes code** | 842,383 |

---

## 🏗️ A) WORKSURFACE (7 Modes Flexibles)

**Location:** `/ui/src/worksurface/`

### Fichiers (13 composants):
| Fichier | Lignes | Description |
|---------|--------|-------------|
| WorkSurfaceShell.tsx | 513 | Shell principal avec tous les modes |
| WorkSurfaceModeSwitcher.tsx | 446 | Switcher entre les 7 modes |
| WorkSurfaceDiagramView.tsx | 444 | Mode diagramme interactif |
| WorkSurfaceArchitecture.tsx | 415 | Vue architecture |
| WorkSurfaceXRLayoutView.tsx | 395 | Mode XR/VR |
| WorkSurfaceBlocksView.tsx | 373 | Mode blocks éditables |
| WorkSurfaceTableView.tsx | 369 | Mode table de données |
| WorkSurfaceSummaryView.tsx | 340 | Mode résumé |
| WorkSurfaceToolbar.tsx | 322 | Toolbar contextuel |
| WorkSurfaceFinalView.tsx | 316 | Mode document final |
| WorkSurfaceTextView.tsx | 307 | Mode éditeur texte |
| WorkSurfaceStatusBar.tsx | 280 | Barre de statut |
| WorkSurfacePage.tsx | 192 | Page wrapper |
| worksurfaceStyles.ts | - | Styles partagés |

### 7 Modes disponibles:
1. **Text** 📝 — Éditeur de texte
2. **Table** 📊 — Vue tableau de données
3. **Blocks** 🧱 — Éditeur de blocs
4. **Diagram** 🔗 — Vue diagramme
5. **Summary** 📋 — Résumé automatique
6. **XR Layout** 🌀 — Mode XR/VR
7. **Final** 📄 — Document final

---

## 🔷 B) DIAMOND LAYOUT (4 Hubs)

**Location:** `/ui/src/components/hubs/`

### Architecture:
```
┌─────────────────────────────────────────────────────────────────┐
│                        HUB CENTER                                │
│              Logo, Contexte actuel, Gouvernance                  │
├────────────────────┬────────────────────────────────────────────┤
│  HUB COMMUNICATION │              HUB WORKSPACE                  │
│  (280px)           │              (flex-1)                       │
│  Nova, Agents,     │    Documents, Browser, Canvas,              │
│  Messages, Email   │    Projets, AI Execution                    │
├────────────────────┴────────────────────────────────────────────┤
│                      HUB NAVIGATION                              │
│          10 Sphères, Explorer, Search, History, XR               │
└─────────────────────────────────────────────────────────────────┘
```

### Fichiers:
| Fichier | Description |
|---------|-------------|
| HubCenter.tsx | Top bar avec logo, contexte, gouvernance |
| HubCommunication.tsx | Hub gauche - Nova, Chat, Email, Meetings |
| HubNavigation.tsx | Hub bottom - Sphères, Search, History |
| HubWorkspace.tsx | Hub droite - Documents, Canvas, AI |

---

## 🔶 C) HUBS V30 COMPLETS

**Location:** `/web_v30/components/layout/`

### Fichiers (17 composants, 4,270 lignes):
| Fichier | Lignes | Description |
|---------|--------|-------------|
| HubCommunication.tsx | 428 | Hub gauche complet |
| HubWorkspace.tsx | 421 | Hub droite complet |
| HubLeft.tsx | 404 | Version alternative hub gauche |
| HubRight.tsx | 375 | Version alternative hub droite |
| HubNavigation.tsx | 276 | Hub navigation complet |
| NovaCommandModal.tsx | 234 | Modal commande Nova |
| HubCommunication.backup.tsx | 217 | Backup |
| HubWorkspace.backup.tsx | 215 | Backup |
| CallOverlay.tsx | 209 | Overlay d'appel |
| NotificationPanel.tsx | 174 | Panel notifications |
| ChenuLayout.tsx | 148 | Layout principal 3 hubs |
| TopBar.tsx | 113 | Top bar |
| AccountPanel.tsx | 111 | Panel compte |
| Breadcrumb.tsx | 96 | Fil d'Ariane |

### Features:
- ✅ 4 tabs Communication (Nova, Chat, Email, Meetings)
- ✅ 4 modes Workspace (Document, Canvas, Table, Browser)
- ✅ Largeurs dynamiques selon la page
- ✅ Collapse/Expand des hubs

---

## 🔺 D) LAYOUTS AVANCÉS

**Location:** `/frontend/src/components/layout/advanced/`

### Fichiers:
| Fichier | Lignes | Description |
|---------|--------|-------------|
| NavigationLayout.tsx | 957 | Layout navigation complet avec 8 sphères |
| WorkspaceLayout.tsx | 493 | Layout workspace avec sidebar sphères |
| DiamondLayoutAdvanced.tsx | 410 | Version avancée du Diamond |

---

## ⭐ E) UNIFIED NAVIGATION HUB PRO

**Location:** `/frontend/src/modules/construction/`

### Fichiers:
| Fichier | Lignes | Description |
|---------|--------|-------------|
| UnifiedNavigationHubPro.tsx | 1,748 | Command palette PRO |
| UnifiedNavigationHubProV2.tsx | 1,203 | Version 2 |

### Features PRO:
- 🧠 AI Smart Suggestions — Nova apprend vos patterns
- 🎤 Voice Input — Commandes vocales
- 📊 Activity Timeline — Activités récentes
- ⭐ Smart Favorites — Favoris auto-organisés
- 🕐 Command History — Historique commandes
- 🔗 Quick Links — Raccourcis personnalisés
- 📋 Clipboard Integration — Copier/coller
- 🎨 Theme Switcher — Changement thème
- 📱 Calculator Mode — Calculatrice rapide
- 🌐 Multi-language — FR/EN/ES
- ⌨️ Vim-style Navigation — Power users
- 🔄 Live Preview — Aperçu en temps réel
- 📈 Usage Analytics — Statistiques usage
- 🎯 Context Awareness — Suggestions contextuelles

---

## 📱 F) MOBILE LAYOUTS

**Location:** `/frontend/src/components/mobile/`

| Fichier | Lignes | Description |
|---------|--------|-------------|
| MobileLayouts.tsx | 800 | Layouts mobile complets |
| MobileLayout.tsx | 526 | Layout mobile basique |

---

## 🎮 UTILISATION

### Pour un layout 3 hubs basique:
```tsx
import ChenuLayout from '@/web_v30/components/layout/ChenuLayout';

export default function App() {
  return <ChenuLayout />;
}
```

### Pour WorkSurface avec 7 modes:
```tsx
import { WorkSurfaceShell } from '@/ui/src/worksurface';

export default function Editor() {
  return (
    <WorkSurfaceShell
      worksurface={worksurfaceData}
      onModeChange={handleModeChange}
    />
  );
}
```

### Pour Navigation Hub Pro:
```tsx
import UnifiedNavigationHubPro from '@/frontend/src/modules/construction/UnifiedNavigationHubPro';

// Trigger with ⌘+K (or Ctrl+K)
export default function CommandPalette() {
  return <UnifiedNavigationHubPro />;
}
```

---

## 📋 RECOMMANDATION

**Pour la version la plus complète et flexible:**

1. Utiliser `ChenuLayout.tsx` de `/web_v30/` comme base
2. Intégrer `WorkSurfaceShell.tsx` dans le HubWorkspace
3. Ajouter `UnifiedNavigationHubPro.tsx` pour la command palette
4. Utiliser `MobileLayouts.tsx` pour le responsive

---

*Document généré le 18 décembre 2024*
*CHE·NU™ — Governed Intelligence Operating System*
