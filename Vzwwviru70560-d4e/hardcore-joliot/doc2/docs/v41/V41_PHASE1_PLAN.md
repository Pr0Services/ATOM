# 🎨 CHE·NU™ V41 — PHASE 1: PBR MATERIALS

**Durée estimée:** 6-8h  
**Objectif:** Implémenter Physically Based Rendering pour réalisme photographique  
**Status:** 🚀 EN COURS  

---

## 🎯 OBJECTIF PHASE 1

Transformer les 7 espaces 3D existants (Maison, Entreprise, Projets, Gouvernement, Immobilier, Associations, Creative) avec des matériaux PBR réalistes.

**Avant (V40):**
```typescript
<meshStandardMaterial color="#FF5733" roughness={0.6} />
```

**Après (V41):**
```typescript
<meshStandardMaterial
  map={colorTexture}
  normalMap={normalTexture}
  roughnessMap={roughnessTexture}
  metalnessMap={metalnessTexture}
  aoMap={aoTexture}
  envMap={environmentMap}
  envMapIntensity={1.0}
/>
```

---

## 📋 TASKS PHASE 1

### Task 1.1: Créer PBRMaterials.ts (2h)
- [ ] Définir interface `PBRMaterialConfig`
- [ ] Créer classe `PBRMaterialLibrary`
- [ ] Implémenter 4 presets de base (wood, stone, metal, glass)
- [ ] Texture loader optimisé (WebP/basis compression)
- [ ] Cache système pour textures

### Task 1.2: Créer MaterialPresets.ts (1.5h)
- [ ] **Wood materials** (5 variations)
  - Oak (chêne)
  - Pine (pin)
  - Walnut (noyer)
  - Bamboo
  - Weathered wood
- [ ] **Stone materials** (5 variations)
  - Granite
  - Marble
  - Limestone
  - Concrete
  - Sandstone
- [ ] **Metal materials** (5 variations)
  - Brushed aluminum
  - Polished steel
  - Copper (oxidized)
  - Gold
  - Iron (rusty)
- [ ] **Glass materials** (3 variations)
  - Clear glass
  - Frosted glass
  - Colored glass

### Task 1.3: Appliquer aux 7 espaces (2h)
- [ ] MaisonSpace → Wood + Stone
- [ ] EntrepriseSpace → Metal + Glass
- [ ] ProjetsSpace → Mixed materials
- [ ] GouvernementSpace → Stone + Metal (prestige)
- [ ] ImmobilierSpace → Realistic building materials
- [ ] AssociationsSpace → Warm wood
- [ ] CreativeSpace → Vibrant + experimental

### Task 1.4: Texture Management (1h)
- [ ] Setup texture loader (TextureLoader)
- [ ] Implement compression (basis/WebP)
- [ ] Texture cache system
- [ ] Fallback textures (si load fail)
- [ ] Performance monitoring

### Task 1.5: Tests & Validation (0.5h)
- [ ] Visual regression tests
- [ ] Performance benchmarks (FPS)
- [ ] Memory usage check
- [ ] Mobile compatibility

---

## 📁 FICHIERS À CRÉER

```
world3d/materials/
├── PBRMaterials.ts ⭐ NEW
├── MaterialPresets.ts ⭐ NEW
├── TextureLoader.ts ⭐ NEW
└── types.ts ⭐ NEW

world3d/assets/textures/
├── wood/
│   ├── oak_color.webp
│   ├── oak_normal.webp
│   ├── oak_roughness.webp
│   ├── oak_ao.webp
│   └── ... (5 wood types × 4 maps = 20 textures)
├── stone/
│   └── ... (5 stone types × 4 maps = 20 textures)
├── metal/
│   └── ... (5 metal types × 4 maps = 20 textures)
└── glass/
    └── ... (3 glass types × 4 maps = 12 textures)

Total textures: 72 fichiers (optimisés WebP, ~50KB each = 3.6MB)
```

---

## 🔧 FICHIERS À MODIFIER

```
world3d/components/spaces/AllSpaces.tsx
├── Import PBRMaterialLibrary
├── Remplacer meshStandardMaterial basiques
└── Appliquer matériaux réalistes

world3d/config/spacesConfig.ts
├── Ajouter materialConfig par espace
└── Définir presets par défaut
```

---

## 📊 MÉTRIQUES SUCCESS

```
✅ 72 textures PBR créées/intégrées
✅ 7 espaces avec matériaux réalistes
✅ Performance: >60fps sur desktop
✅ Performance: >30fps sur mobile
✅ Bundle impact: <5MB (textures compressées)
✅ Tests visuels: Passed
```

---

## 🎨 EXEMPLE CONCRET: MaisonSpace

**Avant:**
```typescript
<mesh position={[0, 0.75, 0]} castShadow>
  <boxGeometry args={[2.5, 1.5, 2]} />
  <meshStandardMaterial color="#FF5733" roughness={0.6} />
</mesh>
```

**Après:**
```typescript
<mesh position={[0, 0.75, 0]} castShadow>
  <boxGeometry args={[2.5, 1.5, 2]} />
  <primitive object={PBRMaterials.getPreset('oak_wood')} />
</mesh>
```

---

## 🚀 NEXT STEPS

Après Phase 1 complète:
→ Phase 2: Advanced Shaders (SSS, hair, cloth)
→ Phase 3: HDR Lighting + Post-processing

---

**Prêt à coder Jo?** 💪🔥
