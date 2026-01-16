# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║                           CHE·NU™                                            ║
# ║                                                                              ║
# ║                    TOOLING & CLI                                             ║
# ║                                                                              ║
# ║                         VERSION 1.0                                          ║
# ║                                                                              ║
# ║              🔴 PRIVATE — INTERNAL ONLY                                      ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

---

# 1. Vue d'ensemble

CHE·NU dispose d'un ensemble d'outils pour :
- Protéger le Design System
- Enforcer la gouvernance
- Faciliter l'onboarding
- Détecter les régressions

## Outils principaux

| Outil | Fonction |
|-------|----------|
| **Design Kit** | Source de vérité design |
| **Storybook** | Documentation + tests visuels |
| **CLI `che-nu`** | Initialisation + validation |
| **Lint** | Gouvernance automatisée |

---

# 2. Design Kit

## Structure

```
design-system/
├─ tokens.json        # Source de vérité
├─ theme.css          # Variables CSS
├─ components/        # Composants UI
│  ├─ Button.tsx
│  ├─ Surface.tsx
│  ├─ DecisionBlock.tsx
│  └─ ...
└─ index.ts           # Export central
```

## tokens.json

Source unique pour toutes les valeurs de design.

```json
{
  "color": {
    "bg": {
      "root": { "value": "#1F2429" },
      "dashboard": { "value": "#242A30" }
    },
    "surface": {
      "dashboard": { "value": "#2A3138" }
    },
    "text": {
      "primary": { "value": "#E2E5E8" }
    }
  },
  "font": {
    "size": {
      "xl": { "value": "22px" },
      "base": { "value": "14px" }
    }
  },
  "spacing": {
    "md": { "value": "16px" }
  }
}
```

## Règle d'or

> Toute modification visuelle commence par `tokens.json`.

Jamais de valeur en dur dans les composants.

---

# 3. Storybook

## Installation

```bash
npm install -D @storybook/react-vite @storybook/addon-essentials
npm install -D @storybook/test-runner playwright
npx playwright install
```

## Configuration

`.storybook/main.ts`

```typescript
const config = {
  stories: ["../src/design-system/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-essentials"],
  framework: {
    name: "@storybook/react-vite",
    options: {}
  },
  test: {
    runner: "@storybook/test-runner"
  }
};
export default config;
```

## Structure d'une story

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Design System/Button',
  component: Button,
  parameters: {
    layout: 'centered'
  }
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button'
  }
};
```

## Tests visuels

```bash
# Lancer Storybook
npm run storybook

# Lancer les tests
npm run test-storybook
```

### Ce que ça vérifie

- Snapshot de chaque composant
- Si un padding change → fail
- Si une couleur change → fail
- Si une typo change → fail

### Résultat

Le Design System est **protégé** contre les régressions involontaires.

---

# 4. CLI `che-nu`

## Installation

```bash
npm install -g che-nu
# ou
npx che-nu [command]
```

## Commandes

### `che-nu init`

Initialise un nouveau projet CHE·NU.

```bash
che-nu init my-project
che-nu init my-project --template default
```

**Ce qui est créé** :

```
my-project/
├─ src/
│  ├─ app/
│  ├─ design-system/
│  │  ├─ tokens.json
│  │  ├─ theme.css
│  │  └─ components/
│  ├─ features/
│  ├─ agents/
│  │  └─ permissions.ts
│  └─ styles/
├─ tailwind.config.js
├─ package.json
└─ README.md
```

### `che-nu lint`

Valide les règles de gouvernance et de design.

```bash
che-nu lint
che-nu lint --verbose
che-nu lint --fix
```

### `che-nu validate`

Valide la configuration design/agents.

```bash
che-nu validate
```

### `che-nu generate`

Génère des composants depuis le Design System.

```bash
che-nu generate component MyComponent
che-nu generate page MyPage
```

---

# 5. `che-nu lint` — Règles

## Catégorie : Design

| Règle | Sévérité | Description |
|-------|----------|-------------|
| `inline-color` | Error | Couleur hex inline |
| `inline-rgb` | Error | RGB/RGBA inline |
| `custom-font-size` | Error | Font-size non standard |
| `custom-spacing` | Warning | Spacing non standard |

### Exemples

```css
/* ❌ Error: inline-color */
.component { background: #2A3138; }

/* ❌ Error: inline-rgb */
.component { color: rgba(255,255,255,0.5); }

/* ❌ Error: custom-font-size */
.component { font-size: 15px; }

/* ✅ Correct */
.component {
  background: var(--surface-dashboard);
  color: var(--text-primary);
  font-size: var(--font-size-base);
}
```

## Catégorie : Gouvernance

| Règle | Sévérité | Description |
|-------|----------|-------------|
| `global-agent` | Error | Agent avec permissions `*` |
| `decision-outside-meeting` | Warning | Décision sans meeting ID |
| `uncontextualized-agent` | Error | Agent sans espace déclaré |

### Exemples

```typescript
// ❌ Error: global-agent
const agent = new Agent({ permissions: ['*'] });

// ❌ Error: uncontextualized-agent
const agent = new Agent({ name: 'helper' });

// ✅ Correct
const agent = new Agent({
  space: 'collaboration',
  permissions: AgentPermissions['collaboration']
});
```

## Catégorie : Structure

| Règle | Sévérité | Description |
|-------|----------|-------------|
| `required-directory` | Error | Dossier requis manquant |
| `required-file` | Warning | Fichier requis manquant |
| `missing-story` | Warning | Composant sans story |

### Dossiers requis

```
src/design-system/
src/agents/
```

### Fichiers requis

```
src/design-system/tokens.json
src/agents/permissions.ts
```

---

# 6. Implémentation du lint

## Structure

```
cli/
├─ src/
│  ├─ index.ts           # Entry point
│  └─ commands/
│     ├─ init.ts         # Init command
│     └─ lint.ts         # Lint command
└─ package.json
```

## Logique de lint

```typescript
export async function lintProject(options: LintOptions): Promise<void> {
  const results: LintResult[] = [];

  // 1. Check design rules
  const styleFiles = await glob('**/*.{css,tsx}');
  for (const file of styleFiles) {
    results.push(...checkDesignRules(file));
  }

  // 2. Check governance rules
  const codeFiles = await glob('**/*.{ts,tsx}');
  for (const file of codeFiles) {
    results.push(...checkGovernanceRules(file));
  }

  // 3. Check structure
  results.push(...checkStructure());

  // 4. Report
  const errors = results.filter(r => r.severity === 'error');
  if (errors.length > 0) {
    process.exit(1);
  }
}
```

## Règles de design

```typescript
const DESIGN_RULES = {
  inlineColors: {
    pattern: /#[0-9A-Fa-f]{3,8}/g,
    message: 'Inline hex color. Use CSS variable.',
    severity: 'error'
  },
  customFontSize: {
    pattern: /font-size:\s*\d+px(?!.*var\()/g,
    message: 'Custom font-size. Use --font-size-* variable.',
    severity: 'error'
  }
};
```

---

# 7. CI/CD Integration

## GitHub Actions

```yaml
name: CHE·NU Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npx che-nu lint
      - run: npm run test-storybook
```

## Pre-commit hook

```bash
# .husky/pre-commit
npx che-nu lint
```

---

# 8. Publication CLI

## Build

```bash
cd cli
npm run build
```

## Publish (privé)

```bash
npm publish --access restricted
```

## Publish (public)

```bash
npm publish --access public
```

## Usage après publication

```bash
npx che-nu init my-project
npx che-nu lint
```

---

# 9. Contribution aux outils

## Ajouter une règle de lint

1. Définir le pattern dans `DESIGN_RULES` ou `GOVERNANCE_RULES`
2. Ajouter les tests
3. Documenter dans ce fichier
4. Ouvrir une PR

## Ajouter une commande CLI

1. Créer le fichier dans `src/commands/`
2. Enregistrer dans `src/index.ts`
3. Documenter
4. Tester

---

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                              CHE·NU™                                         ║
║                                                                              ║
║                    TOOLING & CLI v1.0                                        ║
║                                                                              ║
║              🔴 PRIVATE — DO NOT SHARE                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
