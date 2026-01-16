# CHE·NU — CANONICAL BUREAU STRUCTURE

## 🎯 RÈGLE FONDAMENTALE

```
❌ NE PAS skip les niveaux de hiérarchie invisiblement
✅ PRÉ-REMPLIR visiblement le Context Bureau
```

**L'intelligence SUGGÈRE, l'utilisateur CONFIRME.**

---

## 🏗️ DEUX BUREAUX DISTINCTS

### 1️⃣ Context Bureau
```
┌─────────────────────────────────────┐
│  📍 CONTEXT BUREAU                  │
│                                     │
│  Identity:  🏠 Jo Bouchard  [Auto]  │
│             [Change]                │
│                                     │
│  Sphere:    💼 Business    [Auto]   │
│             [Change]                │
│                                     │
│  Project:   📁 CHE·NU Dev           │
│             [Clear]                 │
│                                     │
│  ✓ Context ready                    │
└─────────────────────────────────────┘
```

**Responsabilités:**
- Montre identité, sphère, projet
- Permet pré-sélection quand unique
- **TOUJOURS visible et éditable**
- Pas d'exécution lourde

---

### 2️⃣ Action Bureau
```
┌─────────────────────────────────────┐
│  ⚡ ACTION BUREAU                   │
│                                     │
│  Quick Actions:                     │
│  [➕ New Workspace]                 │
│  [📝 Quick Note]                    │
│  [✅ New Task]                      │
│                                     │
│  📌 Pinned:                         │
│  ┌─────────────────────────┐        │
│  │ Main Workspace          │        │
│  └─────────────────────────┘        │
│                                     │
│  🕐 Recent:                         │
│  ┌─────────────────────────┐        │
│  │ Dev Session             │        │
│  └─────────────────────────┘        │
└─────────────────────────────────────┘
```

**Responsabilités:**
- Point d'entrée pour le travail
- Raccourcis vers workspaces
- Actions récentes et suggérées

---

## 🔄 FLOW

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  CONTEXT BUREAU  │────▶│  ACTION BUREAU   │────▶│    WORKSPACE     │
│                  │     │                  │     │                  │
│  • Identity      │     │  • Quick Actions │     │  • Execution     │
│  • Sphere        │     │  • Workspaces    │     │  • Canvas        │
│  • Project       │     │  • Suggestions   │     │  • Review        │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   PRÉ-REMPLI              SHORTCUTS                EXECUTION
   par IA                  par IA                   GOUVERNÉE
```

---

## 🧠 INTELLIGENCE = PRÉ-REMPLIR, PAS BYPASS

### Mode AUTO
```typescript
// L'IA pré-remplit si une seule option
if (identities.length === 1) {
  sel.identityId = identities[0].id;
  skipped.push("identity");  // Marqué "Auto" dans l'UI
}
```

**L'utilisateur VOIT ce qui a été pré-rempli et peut CHANGER.**

### Mode MANUAL
```typescript
// Aucun pré-remplissage
// L'utilisateur sélectionne tout manuellement
```

---

## 📐 LAYOUT FINAL

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────┐   ┌───────────────────────────────┐   ┌─────────┐ │
│  │         │   │         ◆ DIAMOND HUB         │   │         │ │
│  │  COMM   │   │     Business • Pro Service    │   │  WORK   │ │
│  │  HUB    │   │   [Comm] [Nav] [Workspace]    │   │  SPACE  │ │
│  │         │   └───────────────────────────────┘   │  HUB    │ │
│  │  Nova   │                                       │         │ │
│  │  Chat   │   ┌─────────────┐ ┌─────────────┐    │  Active │ │
│  │         │   │   CONTEXT   │ │   ACTION    │    │  Work   │ │
│  │  Notifs │   │   BUREAU    │ │   BUREAU    │    │         │ │
│  │         │   │             │ │             │    │  Tools  │ │
│  │         │   │  Identity   │ │  Quick Acts │    │         │ │
│  │         │   │  Sphere     │ │  Workspaces │    │         │ │
│  │         │   │  Project    │ │  Suggested  │    │         │ │
│  │         │   │             │ │             │    │         │ │
│  └─────────┘   └─────────────┘ └─────────────┘    └─────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ PRINCIPES PRÉSERVÉS

| Principe | Implementation |
|----------|----------------|
| **Clarté** | Context Bureau toujours visible |
| **Gouvernance** | User confirme les sélections |
| **Compréhension** | "Auto" badge quand pré-rempli |
| **Contrôle** | Bouton "Change" sur chaque niveau |
| **Séparation** | Context ≠ Action ≠ Workspace |

---

## 📁 FICHIERS

| Fichier | Description |
|---------|-------------|
| `navMachine.ts` | State machine XState (8 spheres) |
| `AppShell.tsx` | UI avec Context + Action Bureaux |

---

*CHE·NU — Governed Intelligence Operating System*
*Clarity over Features • Governance before Execution*
