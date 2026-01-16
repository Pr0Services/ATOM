# CHE·NU™ — UNIVERSE VIEW STRATEGY (CANONICAL)

## 🎯 Principe Fondamental

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   CHE·NU has ONE canonical spatial map of its 8 spheres.   │
│   This map is NEVER modified.                               │
│                                                             │
│   Universe Views are SKINS, not STRUCTURES.                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗺️ La Carte Unique (Structure)

```
                           ╔═══════════════╗
                           ║   ◆ DIAMOND   ║
                           ║     HUB       ║
                           ╚═══════╤═══════╝
                                   │
        ┌──────────┬───────────┬───┴───┬───────────┬──────────┐
        │          │           │       │           │          │
        ▼          ▼           ▼       ▼           ▼          ▼
     ┌──────┐  ┌──────┐   ┌──────┐ ┌──────┐   ┌──────┐  ┌──────┐
     │  🏠  │  │  💼  │   │  🏛️  │ │  🎨  │   │  👥  │  │  📱  │
     │PERSON│  │ BIZ  │   │ GOV  │ │CREATE│   │COMMUN│  │SOCIAL│
     └──────┘  └──────┘   └──────┘ └──────┘   └──────┘  └──────┘
        │          │                              │          │
        └──────────┼──────────────────────────────┼──────────┘
                   │                              │
                   ▼                              ▼
              ┌──────┐                       ┌──────┐
              │  🎬  │                       │  🤝  │
              │ENTERT│                       │ TEAM │
              └──────┘                       └──────┘
```

**Cette topologie est GELÉE.**

---

## 🎨 Les 4 Universe Views

| # | View | Style | Ambiance |
|---|------|-------|----------|
| 1 | **Regular / Professional** | Clean, corporate | Bureau moderne, verre, acier |
| 2 | **Futuristic** | Sci-fi, neon | Cyberpunk, hologrammes, tech |
| 3 | **Natural / Human** | Organique, chaleureux | Bois, nature, lumière douce |
| 4 | **Astral / Abstract** | Cosmique, mystique | Étoiles, nébuleuses, géométrie sacrée |

---

## 🔄 Même Structure, 4 Rendus

### 1️⃣ Regular / Professional

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ╭───────╮    ╭───────╮    ╭───────╮    ╭───────╮         │
│   │ Glass │    │ Glass │    │ Glass │    │ Glass │         │
│   │ Panel │    │ Panel │    │ Panel │    │ Panel │         │
│   ╰───────╯    ╰───────╯    ╰───────╯    ╰───────╯         │
│                                                             │
│   Matériaux: Verre, acier brossé, béton poli                │
│   Éclairage: LED blanc neutre                               │
│   Ambiance: Sérieux, efficace, corporate                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2️⃣ Futuristic

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ◢███████◣  ◢███████◣  ◢███████◣  ◢███████◣               │
│   ║ NEON  ║  ║ NEON  ║  ║ NEON  ║  ║ NEON  ║               │
│   ◥███████◤  ◥███████◤  ◥███████◤  ◥███████◤               │
│                                                             │
│   Matériaux: Hologrammes, grilles laser, surfaces réactives │
│   Éclairage: Neon cyan/magenta, particules                  │
│   Ambiance: Cyberpunk, high-tech, immersif                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3️⃣ Natural / Human

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🌳        🌿        🌸        🌻                          │
│   ╭─────╮  ╭─────╮  ╭─────╮  ╭─────╮                        │
│   │Wood │  │Stone│  │Moss │  │Light│                        │
│   ╰─────╯  ╰─────╯  ╰─────╯  ╰─────╯                        │
│                                                             │
│   Matériaux: Bois, pierre, végétation, eau                  │
│   Éclairage: Lumière dorée, soleil filtré                   │
│   Ambiance: Chaleureux, organique, apaisant                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4️⃣ Astral / Abstract

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│      ✧  ·  ✦    ·    ✧  ·  ✦    ·    ✧  ·  ✦              │
│         ○           ○           ○           ○               │
│      ✧  ·  ✦    ·    ✧  ·  ✦    ·    ✧  ·  ✦              │
│                                                             │
│   Matériaux: Nébuleuses, géométrie sacrée, cristaux         │
│   Éclairage: Lueurs cosmiques, aurores                      │
│   Ambiance: Mystique, transcendant, méditatif               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Architecture Modulaire des Sphères

Chaque sphère est un **module spatial** avec:

```typescript
interface SphereModule {
  // Identité (FROZEN)
  id: SphereKey;
  position: Vector3;        // Position dans la carte canonique
  connections: SphereKey[]; // Connexions aux autres sphères
  
  // Sub-spaces (10 sections du Bureau)
  subSpaces: {
    dashboard: SubSpace;
    notes: SubSpace;
    tasks: SubSpace;
    projects: SubSpace;
    threads: SubSpace;
    meetings: SubSpace;
    data: SubSpace;
    agents: SubSpace;
    reports: SubSpace;
    budget: SubSpace;
  };
  
  // Connection Points (standard)
  connectionPoints: {
    north: ConnectionPoint;
    south: ConnectionPoint;
    east: ConnectionPoint;
    west: ConnectionPoint;
    up: ConnectionPoint;    // Vers Diamond Hub
    down: ConnectionPoint;  // Vers sub-spaces
  };
}
```

---

## 🎨 Universe View = Skin

```typescript
interface UniverseView {
  id: "regular" | "futuristic" | "natural" | "astral";
  name: string;
  
  // Visual Theme
  theme: {
    materials: MaterialPalette;
    lighting: LightingConfig;
    particles: ParticleSystem;
    sounds: SoundscapeConfig;
  };
  
  // Sphere Skins (same structure, different look)
  sphereSkins: Record<SphereKey, SphereSkin>;
  
  // Connection Visuals
  connectionStyle: ConnectionVisualStyle;
  
  // Diamond Hub Variant
  diamondSkin: DiamondSkin;
}

interface SphereSkin {
  // Geometry stays the same, only visuals change
  materials: Material[];
  textures: Texture[];
  emissive: EmissiveConfig;
  animations: Animation[];
}
```

---

## 🔐 Règles Canoniques

| Règle | Description |
|-------|-------------|
| **Structure = Gelée** | La carte spatiale ne change JAMAIS |
| **Positions = Fixes** | Chaque sphère a une position définie |
| **Connexions = Standard** | Points de connexion identiques partout |
| **Views = Skins** | Uniquement l'apparence change |
| **Sub-spaces = 10** | Toujours les 10 sections du Bureau |

---

## 🎛️ Sélection de View

```typescript
// User preference
interface UserUniversePreference {
  defaultView: UniverseViewId;
  perSphereOverrides?: Partial<Record<SphereKey, UniverseViewId>>;
  transitionSpeed: "instant" | "smooth" | "cinematic";
}

// System applies view
function applyUniverseView(
  canonicalMap: CanonicalSphereMap,
  view: UniverseView
): RenderedUniverse {
  // Structure stays identical
  // Only visual skin changes
  return canonicalMap.spheres.map(sphere => ({
    ...sphere,
    visual: view.sphereSkins[sphere.id],
    connections: sphere.connections.map(conn => ({
      ...conn,
      visual: view.connectionStyle
    }))
  }));
}
```

---

## 📊 Comparaison Visuelle

| Aspect | Regular | Futuristic | Natural | Astral |
|--------|---------|------------|---------|--------|
| **Couleurs** | Neutres | Neon | Terre | Cosmique |
| **Lumière** | Froide | Électrique | Chaude | Éthérée |
| **Textures** | Lisses | Grilles | Organiques | Abstraites |
| **Particules** | Aucune | Pixels | Pollen | Étoiles |
| **Son** | Minimal | Synthétique | Nature | Ambient |
| **Animation** | Subtile | Dynamique | Fluide | Lente |

---

## 🏗️ Implémentation Three.js

```typescript
// Universe View Registry
const UNIVERSE_VIEWS: Record<UniverseViewId, UniverseView> = {
  regular: {
    id: "regular",
    name: "Professional",
    theme: {
      materials: {
        primary: new MeshStandardMaterial({ 
          color: 0x2a2a2a, 
          metalness: 0.8 
        }),
        accent: new MeshStandardMaterial({ 
          color: 0x3EB4A2 
        }),
      },
      lighting: {
        ambient: 0x404040,
        directional: 0xffffff,
        intensity: 1.0
      }
    }
  },
  futuristic: {
    id: "futuristic",
    name: "Futuristic",
    theme: {
      materials: {
        primary: new MeshStandardMaterial({ 
          color: 0x0a0a0a, 
          emissive: 0x001122 
        }),
        accent: new MeshStandardMaterial({ 
          color: 0x00ffff, 
          emissive: 0x00ffff 
        }),
      },
      lighting: {
        ambient: 0x000033,
        directional: 0x00ffff,
        intensity: 1.5
      }
    }
  },
  natural: {
    id: "natural",
    name: "Natural",
    theme: {
      materials: {
        primary: new MeshStandardMaterial({ 
          color: 0x8B4513, 
          roughness: 0.9 
        }),
        accent: new MeshStandardMaterial({ 
          color: 0x228B22 
        }),
      },
      lighting: {
        ambient: 0x3d2817,
        directional: 0xffd700,
        intensity: 0.8
      }
    }
  },
  astral: {
    id: "astral",
    name: "Astral",
    theme: {
      materials: {
        primary: new MeshStandardMaterial({ 
          color: 0x1a0033, 
          transparent: true, 
          opacity: 0.8 
        }),
        accent: new MeshStandardMaterial({ 
          color: 0xD8B26A, 
          emissive: 0xD8B26A 
        }),
      },
      lighting: {
        ambient: 0x110022,
        directional: 0x8844ff,
        intensity: 0.6
      }
    }
  }
};
```

---

## 🔒 Statut

| Badge | Signification |
|-------|---------------|
| 🔒 **CANONICAL** | Stratégie officielle |
| 🧊 **FROZEN** | Structure gelée |
| 🎨 **FLEXIBLE** | Skins personnalisables |

---

## 📘 Résumé

```
STRUCTURE = UNE (gelée, canonique)
VIEWS = QUATRE (skins, personnalisables)

La carte ne change jamais.
Seule l'apparence s'adapte.
```

---

*CHE·NU™ — Governed Intelligence Operating System*
*Une Structure • Quatre Visions*
