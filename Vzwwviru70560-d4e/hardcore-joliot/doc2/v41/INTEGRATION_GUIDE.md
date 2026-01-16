/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CHE·NU™ V41 — INTEGRATION GUIDE
 * Complete step-by-step guide to integrate PBR Materials into existing project
 * ═══════════════════════════════════════════════════════════════════════════════
 */

# 🚀 CHE·NU™ V41 — PBR MATERIALS INTEGRATION GUIDE

This guide will walk you through integrating the V41 PBR Materials system into your existing CHE·NU V40 project.

**Estimated time:** 30 minutes  
**Difficulty:** Medium  

---

## 📋 PREREQUISITES

- CHE·NU V40 installed and running
- Node.js 18+ and npm/yarn
- React 18+
- Three.js (already in project)
- TypeScript configured

---

## 📦 STEP 1: COPY FILES

### 1.1 Copy Material System Files

Copy the following files to your project:

```bash
# Create materials directory
mkdir -p frontend/src/world3d/materials

# Copy core files
cp world3d_materials_types.ts → frontend/src/world3d/materials/types.ts
cp world3d_materials_PBRMaterials.ts → frontend/src/world3d/materials/PBRMaterials.ts
cp world3d_materials_MaterialPresets.ts → frontend/src/world3d/materials/MaterialPresets.ts
cp world3d_materials_index.ts → frontend/src/world3d/materials/index.ts
cp TextureLoader.ts → frontend/src/world3d/materials/TextureLoader.ts
```

### 1.2 Copy Space Components

```bash
# Replace existing spaces file
cp AllSpaces_V41.tsx → frontend/src/world3d/components/spaces/AllSpaces.tsx
```

### 1.3 Copy Configuration

```bash
# Replace config file
cp spacesConfig_V41.ts → frontend/src/world3d/config/spacesConfig.ts
```

### 1.4 Copy Initialization

```bash
# Add initialization file
cp initPBRMaterials.ts → frontend/src/world3d/initPBRMaterials.ts
```

### 1.5 Copy Tests (Optional)

```bash
# Create tests directory
mkdir -p frontend/src/world3d/materials/__tests__

# Copy test files
cp PBRMaterials.test.ts → frontend/src/world3d/materials/__tests__/PBRMaterials.test.ts
cp PBRValidation.ts → frontend/src/world3d/materials/PBRValidation.ts
```

---

## 🎨 STEP 2: ADD TEXTURE ASSETS

### 2.1 Create Texture Directories

```bash
mkdir -p public/assets/textures/{wood,stone,metal,glass}
```

### 2.2 Add Placeholder Textures (Development)

For development, the system will auto-generate fallback textures. For production, you'll need real PBR texture maps.

**Required textures (72 total):**

```
public/assets/textures/
├── wood/
│   ├── oak_color.webp
│   ├── oak_normal.webp
│   ├── oak_roughness.webp
│   ├── oak_ao.webp
│   ├── pine_color.webp
│   ├── ... (5 wood types × 4 maps = 20 files)
├── stone/
│   ├── ... (5 stone types × 4 maps = 20 files)
├── metal/
│   ├── ... (5 metal types × 4 maps = 20 files)
└── glass/
    └── ... (3 glass types × 4 maps = 12 files)
```

**Where to get textures:**
- [Poly Haven](https://polyhaven.com/textures) (CC0 license)
- [3D Textures](https://3dtextures.me/) (Free)
- [Texture Haven](https://texturehaven.com/) (CC0)

**Recommended specs:**
- Format: WebP (or PNG/JPG fallback)
- Resolution: 1024×1024 or 2048×2048
- Size: <100KB per texture (compressed)

---

## ⚙️ STEP 3: INITIALIZE IN APP

### 3.1 Update App.tsx

```typescript
// frontend/src/App.tsx

import { useEffect } from 'react';
import { initPBRMaterials } from './world3d/initPBRMaterials';

function App() {
  useEffect(() => {
    // Initialize PBR materials on app startup
    initPBRMaterials()
      .then(() => {
        console.log('✅ PBR Materials initialized');
      })
      .catch((error) => {
        console.error('❌ Failed to initialize PBR Materials:', error);
      });
  }, []);

  return (
    <div className="App">
      {/* Your app content */}
    </div>
  );
}

export default App;
```

### 3.2 Update World3D Component (if separate)

```typescript
// frontend/src/world3d/World3D.tsx

import { useEffect, useState } from 'react';
import { isPBRInitialized } from './initPBRMaterials';

export function World3D() {
  const [materialsReady, setMaterialsReady] = useState(false);

  useEffect(() => {
    // Check if materials are ready
    const checkMaterials = setInterval(() => {
      if (isPBRInitialized()) {
        setMaterialsReady(true);
        clearInterval(checkMaterials);
      }
    }, 100);

    return () => clearInterval(checkMaterials);
  }, []);

  if (!materialsReady) {
    return <LoadingScreen message="Loading materials..." />;
  }

  return <Canvas>{/* Your 3D scene */}</Canvas>;
}
```

---

## 🔧 STEP 4: UPDATE IMPORTS

### 4.1 Update existing space imports

If you have other files importing the old spaces, update them:

```typescript
// Before
import { MaisonSpace, EntrepriseSpace } from './components/spaces/OldSpaces';

// After
import { MaisonSpace, EntrepriseSpace } from './components/spaces/AllSpaces';
```

### 4.2 Import PBR utilities where needed

```typescript
// For manual material usage
import { getPBRLibrary } from './materials';

// For texture loading
import { getTextureLoader, loadTexture } from './materials/TextureLoader';

// For validation
import { runCompleteValidation } from './materials/PBRValidation';
```

---

## ✅ STEP 5: VERIFY INSTALLATION

### 5.1 Run Development Server

```bash
cd frontend
npm run dev
```

### 5.2 Check Console

You should see:
```
🎨 Initializing PBR materials system...
📦 Preloading 12 materials for spaces...
✅ PBR Materials System initialized!
   - Load time: XXXms
   - Materials loaded: 12/12
   - Textures cached: XX
   - Errors: 0
```

### 5.3 Test in Browser

1. Navigate to 3D world view
2. Open browser DevTools (F12)
3. Check for errors
4. Verify materials render correctly

---

## 🧪 STEP 6: RUN TESTS (Optional)

### 6.1 Run Unit Tests

```bash
npm run test
```

### 6.2 Run Validation Suite

```typescript
// In browser console or test file
import { runCompleteValidation } from './world3d/materials/PBRValidation';

// Run full validation
runCompleteValidation().then(results => {
  console.log('Validation complete:', results);
});
```

---

## 🎯 STEP 7: PERFORMANCE TUNING

### 7.1 Monitor Performance

```typescript
import { getPBRStats } from './world3d/initPBRMaterials';
import { getTextureStats } from './world3d/materials/TextureLoader';

// Check material stats
const materialStats = getPBRStats();
console.log('Materials:', materialStats);

// Check texture stats
const textureStats = getTextureStats();
console.log('Textures:', textureStats);
```

### 7.2 Optimize for Mobile

If targeting mobile devices:

```typescript
// Reduce texture quality for mobile
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (isMobile) {
  // Use lower resolution textures
  // Reduce anisotropy
  // Disable some advanced features
}
```

---

## 🔍 TROUBLESHOOTING

### Issue: Materials not loading

**Solution:**
1. Check texture paths in browser Network tab
2. Verify textures exist in `/public/assets/textures/`
3. Check console for errors
4. Ensure `initPBRMaterials()` was called

### Issue: Performance issues

**Solution:**
1. Check texture sizes (should be <100KB each)
2. Reduce number of concurrent loads
3. Enable lazy loading
4. Check FPS in stats panel

### Issue: Materials look wrong

**Solution:**
1. Verify texture maps are correct (color, normal, roughness, etc.)
2. Check material configuration
3. Ensure proper lighting in scene
4. Validate with `runCompleteValidation()`

### Issue: Memory leaks

**Solution:**
1. Call `.dispose()` on unused materials
2. Clear texture cache when needed
3. Monitor memory with `getTextureStats()`

---

## 📚 ADVANCED USAGE

### Custom Materials

```typescript
import { getPBRLibrary } from './world3d/materials';

const library = getPBRLibrary();

// Register custom material
await library.registerMaterial({
  id: 'my_custom_material',
  name: 'My Custom Material',
  category: 'custom',
  maps: {
    color: 'custom_color.webp',
    normal: 'custom_normal.webp',
  },
  roughness: 0.5,
  metalness: 0.8,
});

// Use it
const material = library.getMaterial('my_custom_material');
```

### Lazy Loading

```typescript
import { getTextureLoader } from './world3d/materials/TextureLoader';

const loader = getTextureLoader();

// Load with priority
const texture = await loader.load('path/to/texture.webp', {
  lazy: true,
  priority: 8, // Higher = load first
});
```

### Dynamic Material Switching

```typescript
const library = getPBRLibrary();

// Switch material at runtime
function switchMaterial(meshRef, newMaterialId) {
  const newMaterial = library.getMaterial(newMaterialId);
  if (newMaterial && meshRef.current) {
    meshRef.current.material = newMaterial;
  }
}
```

---

## ✅ CHECKLIST

- [ ] Files copied to correct locations
- [ ] Texture directories created
- [ ] App.tsx updated with initialization
- [ ] Development server runs without errors
- [ ] Materials load correctly in browser
- [ ] Console shows success messages
- [ ] 7 spaces render with PBR materials
- [ ] Performance acceptable (>30 FPS)
- [ ] Tests pass (if running)
- [ ] No memory leaks

---

## 🚀 NEXT STEPS

After successful integration:

1. ✅ **Add production textures** (replace placeholders)
2. ✅ **Tune performance** for your target devices
3. ✅ **Customize materials** for your needs
4. 🔜 **Phase 2:** Advanced Shaders
5. 🔜 **Phase 3:** HDR Lighting
6. 🔜 **Phase 4:** Immersive Themes

---

## 💪 SUPPORT

If you encounter issues:
1. Check console for error messages
2. Review troubleshooting section
3. Run validation suite
4. Check documentation in code comments

---

**🎉 Congratulations! You've successfully integrated PBR Materials V41!**

***PHASE 1 COMPLETE! 🔥💪***
