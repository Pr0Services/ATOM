# CHE·NU — Guide de Développement

> Guide complet pour développer avec et sur CHE·NU

---

## 📋 Table des Matières

1. [Architecture Globale](#architecture-globale)
2. [Conventions de Code](#conventions-de-code)
3. [Structure des Modules](#structure-des-modules)
4. [SDK Development](#sdk-development)
5. [Frontend Development](#frontend-development)
6. [Backend Development](#backend-development)
7. [Tests](#tests)
8. [Contribution](#contribution)

---

## 🏗️ Architecture Globale

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                        CHE·NU v1                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Frontend   │  │    SDK      │  │   Backend   │         │
│  │  (React)    │──│ (TypeScript)│──│  (Python)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │               │               │                   │
│         ▼               ▼               ▼                   │
│  ┌─────────────────────────────────────────────────┐       │
│  │              Core Layers                         │       │
│  │  • UniverseOS    • ContextLayer    • XR Layer   │       │
│  │  • Orchestrator  • WorkSurface     • DataSpace  │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Couches Principales

| Couche | Rôle | Fichiers |
|--------|------|----------|
| **UniverseOS** | Sphères, domaines, navigation | `sdk/core/universe_os.ts` |
| **Orchestrator** | Routage intelligent | `sdk/core/orchestrator.ts` |
| **ContextLayer** | Snapshot contextuel | `sdk/core/context/` |
| **WorkSurface** | Éditeur universel | `sdk/core/worksurface/` |
| **DataSpace** | Espaces de données | `sdk/core/dataspace/` |
| **XR Layer** | Univers immersifs | `sdk/xr/` |

---

## 📝 Conventions de Code

### TypeScript

```typescript
// ✅ BONNE PRATIQUE
interface WorkspaceConfig {
  id: string;
  name: string;
  sphere: Sphere;
  domain: string;
}

// ✅ Export nommé
export function createWorkspace(config: WorkspaceConfig): Workspace {
  // ...
}

// ✅ Types stricts
type Sphere = 'Personal' | 'Business' | 'Creative' | /* ... */;

// ❌ ÉVITER
// any types
// var declarations
// implicit any
```

### Fichiers

- **Composants React**: `PascalCase.tsx`
- **Modules TypeScript**: `snake_case.ts`
- **Tests**: `*.test.ts` ou `__tests__/`
- **Types**: `*_types.ts` ou dans le fichier

### Imports

```typescript
// 1. External packages
import React, { useState, useEffect } from 'react';

// 2. SDK modules
import { Orchestrator, UniverseOS } from '@chenu/sdk';

// 3. Local modules
import { WorkspacePanel } from './components/WorkspacePanel';

// 4. Types
import type { Workspace, Sphere } from './types';

// 5. Styles
import './styles.css';
```

---

## 📦 Structure des Modules

### SDK Module Standard

```
sdk/core/module_name/
├── index.ts              # Exports publics
├── module_api.ts         # API principale
├── module_types.ts       # Types et interfaces
├── module_utils.ts       # Utilitaires
├── module_profiles.ts    # Profils/Presets
└── module_registry.ts    # Registre (optionnel)
```

### Exemple: WorkSurface

```typescript
// sdk/core/worksurface/index.ts
export { WorkSurfaceEngine } from './worksurface_engine';
export { WorkSurfaceAdaptation } from './worksurface_adaptation';
export { WORKSURFACE_PROFILES } from './worksurface_profiles';
export type * from './worksurface_types';
```

---

## 🔧 SDK Development

### Créer un nouveau Engine

```typescript
// sdk/engines/my_sphere/MyEngine.ts

import type { Engine, EngineInput, EngineOutput } from '../types';

export const SAFE_MARKERS = {
  nonAutonomous: true,
  humanInLoop: true,
  representational: true,
};

export class MyEngine implements Engine {
  readonly id = 'MyEngine';
  readonly sphere = 'MySphere';
  
  async process(input: EngineInput): Promise<EngineOutput> {
    // Logique métier
    return {
      success: true,
      data: { /* ... */ },
      safe: true,
    };
  }
}
```

### Ajouter un Preset XR

```typescript
// sdk/xr/xr_presets.ts

export const MY_ROOM_PRESET: XRPreset = {
  id: 'myRoom',
  name: 'My Custom Room',
  sphere: 'Creative',
  environment: {
    skybox: 'studio',
    lighting: 'balanced',
    floor: 'grid',
  },
  defaultSectors: [
    { name: 'Main', position: { x: 0, y: 0, z: -3 } },
    { name: 'Tools', position: { x: -3, y: 0, z: 0 } },
  ],
};
```

---

## ⚛️ Frontend Development

### Structure des Composants

```typescript
// frontend/src/components/MyComponent.tsx

import React, { useState, useCallback } from 'react';
import type { MyComponentProps } from './types';

/**
 * MyComponent
 * 
 * Description du composant
 * 
 * @example
 * ```tsx
 * <MyComponent title="Hello" onAction={handleAction} />
 * ```
 */
export function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = useState<string>('');

  const handleClick = useCallback(() => {
    onAction(state);
  }, [state, onAction]);

  return (
    <div className="my-component">
      <h2>{title}</h2>
      <button onClick={handleClick}>Action</button>
    </div>
  );
}
```

### Hooks Customs

```typescript
// frontend/src/hooks/useWorkspace.ts

import { useState, useEffect } from 'react';
import type { Workspace } from '@chenu/sdk';

export function useWorkspace(workspaceId: string) {
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Fetch workspace...
  }, [workspaceId]);

  return { workspace, loading, error };
}
```

### Design System

Utiliser les composants du design system:

```typescript
import { Button, Card, StatCard, DataTable } from '@/design-system';

function Dashboard() {
  return (
    <Card>
      <StatCard label="Projets" value={23} />
      <Button variant="primary">Nouveau</Button>
    </Card>
  );
}
```

---

## 🐍 Backend Development

### Structure des Services

```python
# backend/services/my_service.py

from typing import List, Optional
from pydantic import BaseModel

class MyInput(BaseModel):
    name: str
    value: int

class MyOutput(BaseModel):
    success: bool
    result: Optional[str]

class MyService:
    """
    Service pour gérer XYZ
    
    Safe: Non-autonomous, representational only
    """
    
    def __init__(self):
        self.data = []
    
    async def process(self, input: MyInput) -> MyOutput:
        # Logique métier
        return MyOutput(success=True, result="Done")
```

### Routes API

```python
# backend/api/routes/my_routes.py

from fastapi import APIRouter, HTTPException
from ..services.my_service import MyService, MyInput, MyOutput

router = APIRouter(prefix="/api/my", tags=["my"])
service = MyService()

@router.post("/process", response_model=MyOutput)
async def process_request(input: MyInput):
    try:
        return await service.process(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🧪 Tests

### Tests SDK (Vitest)

```typescript
// sdk/tests/my_module.test.ts

import { describe, it, expect, beforeEach } from 'vitest';
import { MyModule } from '../core/my_module';

describe('MyModule', () => {
  let module: MyModule;

  beforeEach(() => {
    module = new MyModule();
  });

  it('should do something', () => {
    const result = module.doSomething();
    expect(result).toBeDefined();
  });

  it('should be safe', () => {
    expect(module.SAFE_MARKERS.nonAutonomous).toBe(true);
  });
});
```

### Tests Frontend (Vitest + React Testing Library)

```typescript
// frontend/src/components/__tests__/MyComponent.test.tsx

import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from '../MyComponent';

describe('MyComponent', () => {
  it('renders title', () => {
    render(<MyComponent title="Hello" onAction={() => {}} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('calls onAction when clicked', () => {
    const onAction = vi.fn();
    render(<MyComponent title="Hello" onAction={onAction} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalled();
  });
});
```

### Tests Backend (Pytest)

```python
# backend/tests/test_my_service.py

import pytest
from services.my_service import MyService, MyInput

@pytest.fixture
def service():
    return MyService()

@pytest.mark.asyncio
async def test_process(service):
    input = MyInput(name="test", value=42)
    result = await service.process(input)
    assert result.success == True
```

---

## 🤝 Contribution

### Workflow Git

1. **Branch** depuis `main`
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Commit** avec messages clairs
   ```bash
   git commit -m "feat(sdk): add new engine for MyDomain"
   ```

3. **Test** avant de push
   ```bash
   npm run test
   ```

4. **Pull Request** avec description

### Commit Messages

Format: `type(scope): description`

Types:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

### Checklist PR

- [ ] Tests ajoutés/mis à jour
- [ ] Documentation mise à jour
- [ ] Types TypeScript corrects
- [ ] Pas de `any` inutiles
- [ ] Safe markers présents (pour SDK)
- [ ] Lint/format passent

---

## 🔒 Sécurité

### Principes CHE·NU

1. **Non-autonome** — Les agents observent et recommandent
2. **Human-in-the-loop** — Validation humaine obligatoire
3. **Représentationnel** — Données conceptuelles uniquement
4. **Traçabilité** — Audit trail complet

### Safe Markers

Chaque module SDK doit exporter:

```typescript
export const SAFE_MARKERS = {
  nonAutonomous: true,
  humanInLoop: true,
  representational: true,
};
```

---

## 📚 Ressources Additionnelles

- [Quickstart](./QUICKSTART.md)
- [API Reference](../sdk/docs/API_REFERENCE.md)
- [SDK Architecture](../sdk/docs/ARCHITECTURE_SDK.md)
- [Design System](../frontend/src/design-system/README.md)

---

**CHE·NU** — *Chez Nous* — Votre OS Cognitif Universel 🏠🧠

*Pro-Service Construction, Brossard, Québec*
