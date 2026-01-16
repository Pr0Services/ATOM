# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║                           CHE·NU™                                            ║
# ║                                                                              ║
# ║                    DESIGN SYSTEM v1                                          ║
# ║                                                                              ║
# ║                         VERSION 1.0                                          ║
# ║                                                                              ║
# ║              🔴 PRIVATE — INTERNAL ONLY                                      ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

---

# 1. Principes fondateurs

## Un seul thème

CHE·NU n'a **qu'un seul thème**. Pas de mode clair. Pas de variations.
Pas de personnalisation utilisateur.

Cette contrainte est délibérée :
- Cohérence absolue entre utilisateurs
- Pas de fragmentation d'équipe
- Design maintenable à long terme

## Calme visuel

L'interface réduit la charge cognitive :
- Contraste suffisant, jamais agressif
- Pas de couleurs vives ou saturées
- Espace négatif généreux
- Hiérarchie claire par espacement et poids

## Token-based

Toutes les valeurs visuelles passent par des tokens :
- Couleurs
- Typographie
- Espacement
- Rayons
- Ombres

**Règle absolue** : Aucune valeur en dur dans le code.

---

# 2. Couleurs

## Tokens de couleur

### Backgrounds

| Token | Valeur | Usage |
|-------|--------|-------|
| `--bg-root` | #1F2429 | Fond global |
| `--bg-dashboard` | #242A30 | Espace Dashboard |
| `--bg-collaboration` | #20262C | Espace Collaboration |
| `--bg-workspace` | #1F2429 | Espace Workspace |

### Surfaces

| Token | Valeur | Usage |
|-------|--------|-------|
| `--surface-dashboard` | #2A3138 | Cartes Dashboard |
| `--surface-collaboration` | #2D343C | Cartes Collaboration |
| `--surface-workspace` | #323A42 | Cartes Workspace |
| `--surface-focus` | #39424A | Éléments en focus |

### Texte

| Token | Valeur | Usage |
|-------|--------|-------|
| `--text-primary` | #E2E5E8 | Texte principal |
| `--text-secondary` | #B5BBC2 | Texte secondaire |
| `--text-muted` | #8E949B | Texte atténué |

### Accent & Bordures

| Token | Valeur | Usage |
|-------|--------|-------|
| `--accent-soft` | rgba(191,174,122,0.35) | Accent (rare) |
| `--border-subtle` | rgba(255,255,255,0.04) | Bordures subtiles |

## Règles de couleur

| ✅ Correct | ❌ Interdit |
|------------|-------------|
| `var(--text-primary)` | `#E2E5E8` |
| `var(--surface-dashboard)` | `background: #2A3138` |
| Nouvelle variable si besoin | Valeur en dur |

---

# 3. Typographie

## Familles

| Token | Valeur |
|-------|--------|
| `--font-primary` | Inter, SF Pro, Source Sans 3, system-ui |
| `--font-mono` | JetBrains Mono, SF Mono, monospace |

## Échelle

| Style | Taille | Poids | Line Height | Usage |
|-------|--------|-------|-------------|-------|
| Title XL | 22px | Medium (500) | 1.3 | Titres principaux |
| Title | 18px | Medium (500) | 1.35 | Titres de section |
| Section | 16px | Medium (500) | 1.4 | Sous-sections |
| Body | 14px | Regular (400) | 1.6 | Texte courant |
| Meta | 12px | Regular (400) | 1.45 | Métadonnées |

## Poids

| Token | Valeur | Usage |
|-------|--------|-------|
| `--font-weight-regular` | 400 | Texte courant |
| `--font-weight-medium` | 500 | Titres |
| `--font-weight-semibold` | 600 | Décisions |

## Règles typographiques

| ✅ Correct | ❌ Interdit |
|------------|-------------|
| Poids via token | `font-weight: bold` |
| Taille de l'échelle | `font-size: 15px` |
| Line-height du token | Line-height arbitraire |

---

# 4. Micro-typographie

## Notes vs Décisions

La différenciation est **ressentie, pas vue** :

| Élément | Notes | Décisions |
|---------|-------|-----------|
| Weight titre | Regular (400) | Semibold (600) |
| Spacing vertical | Standard | +8% |
| Contraste | Normal | Légèrement plus marqué |

L'utilisateur ne doit pas pouvoir pointer une différence précise,
mais il perçoit que les décisions sont "plus importantes".

## Blocs de texte

- Maximum **65 caractères** par ligne
- Pas de justification
- Meta-info en `text.muted` avec opacity 0.7

## Listes

- Espacement vertical généreux entre items
- Pas de bullets décoratifs complexes
- Hiérarchie par indentation, pas par style

---

# 5. Espacement

## Échelle

| Token | Valeur | Usage |
|-------|--------|-------|
| `--space-xs` | 4px | Micro gaps |
| `--space-sm` | 8px | Petits espaces |
| `--space-md` | 16px | Padding standard |
| `--space-lg` | 24px | Séparation sections |
| `--space-xl` | 32px | Respiration layout |

## Règles

- Auto-layout uniquement (pas de spacing manuel)
- Multiple de 4px obligatoire
- Aucune valeur arbitraire

---

# 6. Rayons & Ombres

## Rayons

| Token | Valeur | Usage |
|-------|--------|-------|
| `--radius-sm` | 8px | Petits éléments |
| `--radius-md` | 12px | Cartes |
| `--radius-lg` | 16px | Modales |

## Ombres

| Token | Valeur |
|-------|--------|
| `--shadow-soft` | inset 0 1px 0 rgba(255,255,255,0.03), 0 8px 24px rgba(0,0,0,0.28) |

---

# 7. Composants

## Surface / Card

```css
.card {
  background: var(--surface-*);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft);
  padding: var(--space-md);
}
```

## Buttons

| Variant | Usage | Fréquence |
|---------|-------|-----------|
| Primary | Action principale | Rare |
| Secondary | Actions courantes | Fréquent |
| Ghost | Actions tertiaires | Fréquent |

## Decision Block

```
┌────────────────────────────────────────────┐
│ Titre de la décision                        │  ← semibold
│                                             │
│ Corps de la décision avec le contexte       │  ← regular
│ et les détails pertinents.                  │
│                                             │
│ Created: 2024-01-15                         │  ← muted
└────────────────────────────────────────────┘
```

**Interdit** : border-left coloré, badges, icônes décoratives

## Timeline Item

```
● Active Decision Title        ← opacity 1.0
○ Superseded Decision Title    ← opacity 0.55
```

Le point utilise `text.muted`, jamais `accent`.

---

# 8. États

## Hover

```css
.hoverable:hover {
  background: var(--surface-focus);
}
```

## Focus

```css
.focusable:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(110, 175, 196, 0.3);
}
```

## Disabled

```css
.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## Read-only

```css
.readonly {
  opacity: 0.9;
  cursor: default;
}
```

---

# 9. Anti-patterns

## Interdit absolument

| Anti-pattern | Pourquoi |
|--------------|----------|
| Couleurs vives | Agressif, fatiguant |
| Animations décoratives | Distrait |
| Badges colorés | Crée de l'anxiété |
| Icônes sans fonction | Bruit visuel |
| Ombres lourdes | Lourd, daté |
| Gradients | Incohérent avec le thème |
| Border-left colorés | Effet "alerte" non voulu |

---

# 10. Fichiers de référence

| Fichier | Contenu |
|---------|---------|
| `tokens.json` | Source de vérité |
| `theme.css` | Variables CSS |
| `tailwind.config.js` | Config Tailwind |

## Hiérarchie

```
tokens.json (source)
     ↓
theme.css + tailwind.config.js (dérivés)
     ↓
Composants (consommateurs)
```

Toute modification commence par `tokens.json`.

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                              CHE·NU™                                         ║
║                                                                              ║
║                    DESIGN SYSTEM v1.0                                        ║
║                                                                              ║
║              🔴 PRIVATE — DO NOT SHARE                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
