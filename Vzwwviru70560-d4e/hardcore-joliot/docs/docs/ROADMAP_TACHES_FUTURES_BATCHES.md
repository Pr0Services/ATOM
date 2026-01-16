# 🚀 CHE·NU™ - ROADMAP COMPLÈTE DES TÂCHES FUTURES

**Document de Planification pour Agents IA**  
**Version:** 1.0  
**Date:** 6 décembre 2025

---

## 🎯 PROMPT SYSTÈME POUR AGENTS

### Contexte du Projet

```
Tu es un Agent Développeur travaillant sur CHE·NU™, une plateforme de gestion 
unifiée pour la construction au Québec. Le projet est à ~85% de complétion.

ARCHITECTURE:
- Frontend: React 18 + Vite + TypeScript + Tailwind
- Backend: Python FastAPI + PostgreSQL + Redis
- Agents IA: 101 agents organisés en 14 départements
- Design: Temple Theme (Sacred Gold #D8B26A, Dark Slate #1A1A1A)

ÉTAT ACTUEL:
- 250+ fichiers consolidés
- 20 pages principales fonctionnelles
- 11 Mondes CHE·NU définis
- Backend complet avec modules B7-B28

OBJECTIF:
Compléter les modules manquants en suivant les patterns existants,
en préparant l'infrastructure pour les effets 3D et graphiques haute gamme.

MÉTHODOLOGIE:
1. Lire la spec de la tâche
2. Examiner les fichiers existants similaires
3. Implémenter en suivant les conventions
4. Tester sur les 3 thèmes (Dark/Light/VR)
5. Documenter le code
```

### Conventions à Suivre

```typescript
// Composants React
const MonComposant: React.FC<Props> = ({ prop1, prop2 }) => {
  // 1. Hooks
  const [state, setState] = useState();
  const { theme } = useTheme();
  
  // 2. Effects
  useEffect(() => { ... }, []);
  
  // 3. Handlers
  const handleClick = () => { ... };
  
  // 4. Render
  return (
    <div className="bg-slate-900 rounded-xl p-6 border border-amber-500/20">
      {/* Temple Theme: Sacred Gold accents */}
    </div>
  );
};
```

```python
# Backend Python
class MonService:
    """
    Description du service.
    
    Attributes:
        attr1: Description
    """
    
    async def ma_methode(self, param: Type) -> ReturnType:
        """Docstring."""
        pass
```

---

## 📋 STRUCTURE DES BATCHES

Les tâches sont organisées en **batches de 5** pour faciliter le travail incrémental.
Chaque batch peut être complété en une session de travail.

```
BATCH STRUCTURE:
├── Batch ID: MOD-XX-BY (Module-Numéro-Batch)
├── 5 tâches numérotées
├── Dépendances listées
├── Estimation temps: 2-4h par batch
└── Fichiers à créer/modifier
```

---

# 📦 MODULE 1: INFRASTRUCTURE 3D & GRAPHIQUES

## Objectif
Préparer l'infrastructure pour les effets 3D, animations avancées et graphiques haute gamme.

---

### BATCH INF-01-B1: Fondations Three.js

**Dépendances:** Aucune  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/lib/three/ThreeProvider.tsx`
- `frontend/lib/three/useThree.ts`
- `frontend/lib/three/SceneManager.ts`
- `frontend/lib/three/MaterialLibrary.ts`
- `frontend/lib/three/LightingSystem.ts`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| INF-01-B1-T1 | ThreeProvider | Context React pour Three.js avec canvas WebGL | 🔴 |
| INF-01-B1-T2 | useThree Hook | Hook pour accéder au renderer, scene, camera | 🔴 |
| INF-01-B1-T3 | SceneManager | Gestion des scènes, objets, cleanup | 🔴 |
| INF-01-B1-T4 | MaterialLibrary | Matériaux PBR, shaders Temple Theme | 🟡 |
| INF-01-B1-T5 | LightingSystem | Éclairage dynamique, ambient occlusion | 🟡 |

**Prompt Agent:**
```
Crée l'infrastructure Three.js pour CHE·NU.

Fichier 1: ThreeProvider.tsx
- Context React avec canvas WebGL
- Resize handler responsive
- RAF loop optimisé
- Cleanup automatique

Fichier 2: useThree.ts
- Accès renderer, scene, camera
- Helper pour ajouter/supprimer objets
- Animation helpers

Fichier 3: SceneManager.ts
- GLTF loader
- Texture manager
- Object pooling
- LOD (Level of Detail)

Couleurs Temple Theme:
- Primary: #D8B26A (Sacred Gold)
- Background: #1A1A1A (Dark Slate)
- Accent: #F5E6D3 (Light Gold)

Optimisations requises:
- Instanced rendering pour objets répétés
- Frustum culling
- Texture atlasing
```

---

### BATCH INF-01-B2: Système de Particules

**Dépendances:** INF-01-B1  
**Estimation:** 3h  
**Fichiers à créer:**
- `frontend/lib/three/particles/ParticleSystem.ts`
- `frontend/lib/three/particles/Emitters.ts`
- `frontend/lib/three/particles/GoldDustEffect.ts`
- `frontend/lib/three/particles/DataFlowEffect.ts`
- `frontend/lib/three/particles/useParticles.ts`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| INF-01-B2-T1 | ParticleSystem | Système base avec GPU particles | 🔴 |
| INF-01-B2-T2 | Emitters | Point, Line, Surface emitters | 🔴 |
| INF-01-B2-T3 | GoldDustEffect | Particules dorées flottantes (ambiance) | 🟡 |
| INF-01-B2-T4 | DataFlowEffect | Visualisation flux de données | 🟡 |
| INF-01-B2-T5 | useParticles | Hook React pour effets particules | 🟡 |

**Prompt Agent:**
```
Crée un système de particules GPU pour effets visuels CHE·NU.

ParticleSystem.ts:
- GPU particles avec transform feedback ou compute shaders
- Pool de particules réutilisables (10K-100K)
- Spawn rate, lifetime, velocity configurable
- Gravity, wind, attractors

GoldDustEffect.ts:
- Particules dorées (#D8B26A) flottant lentement
- Pour background des pages premium
- Interaction avec souris (attraction légère)
- Fade in/out aux bords

DataFlowEffect.ts:
- Lignes de particules représentant flux données
- Entre les nodes d'un graphe
- Couleur selon type de donnée
- Animation fluide Bézier

Performance target: 60fps avec 50K particules
```

---

### BATCH INF-01-B3: Shaders Personnalisés

**Dépendances:** INF-01-B1  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/lib/three/shaders/GoldMetalShader.glsl`
- `frontend/lib/three/shaders/GlassShader.glsl`
- `frontend/lib/three/shaders/HologramShader.glsl`
- `frontend/lib/three/shaders/NoiseShader.glsl`
- `frontend/lib/three/shaders/ShaderLibrary.ts`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| INF-01-B3-T1 | GoldMetalShader | Métal doré réaliste PBR | 🔴 |
| INF-01-B3-T2 | GlassShader | Verre/cristal avec réfraction | 🟡 |
| INF-01-B3-T3 | HologramShader | Effet holographique pour VR mode | 🟡 |
| INF-01-B3-T4 | NoiseShader | Bruit procédural multi-usage | 🟡 |
| INF-01-B3-T5 | ShaderLibrary | Gestionnaire et compilation | 🔴 |

**Prompt Agent:**
```
Crée des shaders GLSL personnalisés pour le Temple Theme.

GoldMetalShader.glsl:
- PBR metallic workflow
- Roughness map support
- Fresnel pour reflets réalistes
- Anisotropic highlights (or brossé)

Vertex:
- Standard MVP transform
- Normal mapping support
- UV pour textures

Fragment:
- Cook-Torrance BRDF
- Image-based lighting ready
- Tone mapping (ACES)

Couleurs:
- Base: #D8B26A
- Highlights: #F5E6D3
- Shadows: #8B7355

HologramShader.glsl:
- Scanlines animées
- Glitch effect subtil
- Fresnel glow cyan/gold
- Alpha transparency
```

---

### BATCH INF-01-B4: Graphiques D3.js Avancés

**Dépendances:** Aucune  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/lib/charts/ChartProvider.tsx`
- `frontend/lib/charts/AnimatedLineChart.tsx`
- `frontend/lib/charts/AnimatedBarChart.tsx`
- `frontend/lib/charts/RadialGauge.tsx`
- `frontend/lib/charts/NetworkGraph.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| INF-01-B4-T1 | ChartProvider | Context avec thème et animations | 🔴 |
| INF-01-B4-T2 | AnimatedLineChart | Line chart avec transitions fluides | 🔴 |
| INF-01-B4-T3 | AnimatedBarChart | Bar chart avec entrée animée | 🔴 |
| INF-01-B4-T4 | RadialGauge | Jauge circulaire style dashboard | 🟡 |
| INF-01-B4-T5 | NetworkGraph | Graphe de réseau force-directed | 🟡 |

**Prompt Agent:**
```
Crée des composants D3.js avec animations haute qualité.

ChartProvider.tsx:
- Context pour thème unifié
- Palette Temple Theme
- Animation config globale
- Responsive breakpoints

AnimatedLineChart.tsx:
- Enter: ligne dessinée progressivement
- Update: morph smooth entre datasets
- Exit: fade out
- Tooltip animé
- Gradient fill
- Area glow effect

Couleurs:
- Primary line: #D8B26A
- Secondary: #8B7355
- Grid: rgba(216, 178, 106, 0.1)
- Tooltip bg: #1A1A1A

Performance:
- Canvas rendering pour gros datasets (>1000 points)
- SVG pour interactivité (<1000 points)
- RequestAnimationFrame pour 60fps
```

---

### BATCH INF-01-B5: Post-Processing & Effects

**Dépendances:** INF-01-B1, INF-01-B3  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/lib/three/postfx/EffectComposer.ts`
- `frontend/lib/three/postfx/BloomPass.ts`
- `frontend/lib/three/postfx/GodRaysPass.ts`
- `frontend/lib/three/postfx/ColorGradingPass.ts`
- `frontend/lib/three/postfx/VignettePass.ts`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| INF-01-B5-T1 | EffectComposer | Pipeline post-processing | 🔴 |
| INF-01-B5-T2 | BloomPass | Glow sur éléments brillants | 🔴 |
| INF-01-B5-T3 | GodRaysPass | Rayons volumétriques | 🟡 |
| INF-01-B5-T4 | ColorGradingPass | LUT et color correction | 🟡 |
| INF-01-B5-T5 | VignettePass | Vignette cinématique | 🟢 |

**Prompt Agent:**
```
Crée le pipeline post-processing pour rendu cinématique.

EffectComposer.ts:
- Multi-pass rendering
- Ping-pong buffers
- Resolution scaling
- Effect toggling

BloomPass.ts:
- Threshold configurable
- Multi-scale blur
- Additive blending
- Gold-tinted bloom pour Temple Theme

GodRaysPass.ts:
- Radial blur from light source
- Occlusion sampling
- Density control
- Subtil, pas overwhelming

ColorGradingPass.ts:
- Lift/Gamma/Gain
- LUT support
- Warm gold tint preset
- Contrast/Saturation

Preset "Temple":
- Warm color temperature
- Slightly lifted blacks
- Gold in highlights
- Subtle vignette
```

---

# 📦 MODULE 2: UI COMPONENTS AVANCÉS

## Objectif
Créer des composants UI premium avec animations et effets visuels.

---

### BATCH UI-02-B1: Composants Glassmorphism

**Dépendances:** Aucune  
**Estimation:** 3h  
**Fichiers à créer:**
- `frontend/components/glass/GlassCard.tsx`
- `frontend/components/glass/GlassModal.tsx`
- `frontend/components/glass/GlassNavbar.tsx`
- `frontend/components/glass/GlassButton.tsx`
- `frontend/components/glass/GlassSidebar.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UI-02-B1-T1 | GlassCard | Card avec backdrop-blur et border glow | 🔴 |
| UI-02-B1-T2 | GlassModal | Modal flottant glassmorphism | 🔴 |
| UI-02-B1-T3 | GlassNavbar | Navigation transparente | 🟡 |
| UI-02-B1-T4 | GlassButton | Bouton avec effet verre | 🟡 |
| UI-02-B1-T5 | GlassSidebar | Sidebar pour VR mode | 🟡 |

**Prompt Agent:**
```
Crée des composants glassmorphism pour le VR mode.

GlassCard.tsx:
```tsx
<div className="
  relative
  bg-slate-900/40
  backdrop-blur-xl
  border border-amber-500/20
  rounded-2xl
  shadow-[0_8px_32px_rgba(216,178,106,0.1)]
  overflow-hidden
">
  {/* Glow effect */}
  <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent" />
  
  {/* Content */}
  <div className="relative z-10 p-6">
    {children}
  </div>
  
  {/* Border glow on hover */}
  <div className="absolute inset-0 rounded-2xl border border-amber-500/0 
                  group-hover:border-amber-500/40 transition-colors duration-500" />
</div>
```

Animations:
- Hover: scale(1.02), border glow
- Focus: ring amber
- Active: scale(0.98)

Props:
- variant: 'default' | 'elevated' | 'sunken'
- glow: boolean
- interactive: boolean
```

---

### BATCH UI-02-B2: Animations Micro-interactions

**Dépendances:** Aucune  
**Estimation:** 3h  
**Fichiers à créer:**
- `frontend/components/animations/FadeIn.tsx`
- `frontend/components/animations/SlideIn.tsx`
- `frontend/components/animations/ScaleIn.tsx`
- `frontend/components/animations/StaggerChildren.tsx`
- `frontend/components/animations/MagneticButton.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UI-02-B2-T1 | FadeIn | Fade avec direction | 🔴 |
| UI-02-B2-T2 | SlideIn | Slide de n'importe quelle direction | 🔴 |
| UI-02-B2-T3 | ScaleIn | Scale avec spring physics | 🟡 |
| UI-02-B2-T4 | StaggerChildren | Animation séquentielle enfants | 🔴 |
| UI-02-B2-T5 | MagneticButton | Bouton qui suit le curseur | 🟡 |

**Prompt Agent:**
```
Crée des composants d'animation réutilisables avec Framer Motion.

FadeIn.tsx:
- direction: 'up' | 'down' | 'left' | 'right' | 'none'
- delay: number (seconds)
- duration: number
- Intersection Observer pour trigger

StaggerChildren.tsx:
```tsx
<StaggerChildren staggerDelay={0.1}>
  <Item /> {/* delay 0 */}
  <Item /> {/* delay 0.1 */}
  <Item /> {/* delay 0.2 */}
</StaggerChildren>
```

MagneticButton.tsx:
- Suit le curseur dans un rayon
- Retour elastic au centre
- Scale subtle au hover
- Effet ripple au click

Spring configs:
- default: { stiffness: 300, damping: 30 }
- bouncy: { stiffness: 400, damping: 10 }
- slow: { stiffness: 100, damping: 20 }
```

---

### BATCH UI-02-B3: Dashboard Widgets Premium

**Dépendances:** INF-01-B4  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/components/widgets/StatCard3D.tsx`
- `frontend/components/widgets/ProgressRing.tsx`
- `frontend/components/widgets/LiveTicker.tsx`
- `frontend/components/widgets/ActivityHeatmap.tsx`
- `frontend/components/widgets/MetricSparkline.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UI-02-B3-T1 | StatCard3D | Card stat avec effet 3D au hover | 🔴 |
| UI-02-B3-T2 | ProgressRing | Anneau de progression animé | 🔴 |
| UI-02-B3-T3 | LiveTicker | Ticker temps réel avec animation | 🟡 |
| UI-02-B3-T4 | ActivityHeatmap | Heatmap style GitHub | 🟡 |
| UI-02-B3-T5 | MetricSparkline | Mini graphique inline | 🟡 |

**Prompt Agent:**
```
Crée des widgets dashboard haute qualité.

StatCard3D.tsx:
- Rotation 3D subtile suivant souris
- Reflet/shadow dynamique
- Icône 3D ou Lottie
- Valeur avec counting animation
- Trend indicator (up/down arrow)

ProgressRing.tsx:
- SVG animé
- Gradient stroke (gold)
- Percentage au centre
- Easing: easeOutExpo
- Configurable: size, strokeWidth, color

LiveTicker.tsx:
- WebSocket ready
- Animation flip ou slide pour changements
- Highlight sur update
- Historique des 5 dernières valeurs

ActivityHeatmap.tsx:
- Grid responsive
- Tooltip avec détails
- Palette gold (light → dark)
- Click pour drill-down
- Légende interactive
```

---

### BATCH UI-02-B4: Navigation Avancée

**Dépendances:** UI-02-B1  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/components/nav/CommandPalette.tsx`
- `frontend/components/nav/BreadcrumbsAnimated.tsx`
- `frontend/components/nav/TabsAnimated.tsx`
- `frontend/components/nav/MegaMenu.tsx`
- `frontend/components/nav/FloatingDock.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UI-02-B4-T1 | CommandPalette | ⌘K avec recherche fuzzy | 🔴 |
| UI-02-B4-T2 | BreadcrumbsAnimated | Breadcrumbs avec transitions | 🟡 |
| UI-02-B4-T3 | TabsAnimated | Tabs avec indicator animé | 🟡 |
| UI-02-B4-T4 | MegaMenu | Menu déroulant riche | 🟡 |
| UI-02-B4-T5 | FloatingDock | Dock style macOS | 🟢 |

**Prompt Agent:**
```
Crée des composants de navigation premium.

CommandPalette.tsx (⌘K):
- Ouverture: ⌘K ou Ctrl+K
- Recherche fuzzy (fuse.js)
- Catégories: Pages, Actions, Agents, Settings
- Récents en premier
- Keyboard navigation (↑↓, Enter, Esc)
- Preview panel optionnel

Sections:
- 📄 Pages: Dashboard, Projects, Calendar...
- ⚡ Actions: Create Project, Send Email...
- 🤖 Agents: Talk to Nova, Ask Analytics...
- ⚙️ Settings: Theme, Language...

Animation:
- Backdrop blur
- Scale from 95% to 100%
- Results stagger in

FloatingDock.tsx:
- Position: bottom center
- Icons scale on hover (like macOS)
- Tooltip avec nom
- Drag to reorder
- Badge notifications
```

---

### BATCH UI-02-B5: Forms & Inputs Premium

**Dépendances:** Aucune  
**Estimation:** 3h  
**Fichiers à créer:**
- `frontend/components/forms/FloatingLabelInput.tsx`
- `frontend/components/forms/AnimatedSelect.tsx`
- `frontend/components/forms/RangeSlider.tsx`
- `frontend/components/forms/TagInput.tsx`
- `frontend/components/forms/DatePickerPremium.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UI-02-B5-T1 | FloatingLabelInput | Label qui flotte au focus | 🔴 |
| UI-02-B5-T2 | AnimatedSelect | Select avec dropdown animé | 🔴 |
| UI-02-B5-T3 | RangeSlider | Slider avec tooltip valeur | 🟡 |
| UI-02-B5-T4 | TagInput | Input multi-tags avec autocomplete | 🟡 |
| UI-02-B5-T5 | DatePickerPremium | Calendrier popup animé | 🟡 |

**Prompt Agent:**
```
Crée des composants de formulaire premium.

FloatingLabelInput.tsx:
- Label: position absolute, translate up on focus/filled
- Border: animate from bottom center outward
- Focus ring: gold glow
- Error state: red with shake animation
- Success state: green checkmark

AnimatedSelect.tsx:
- Dropdown: scale + fade in
- Options: stagger animation
- Selected: checkmark animé
- Search intégré
- Keyboard nav

RangeSlider.tsx:
- Track: gradient gold
- Thumb: draggable, scale on drag
- Tooltip: show value, follows thumb
- Marks: optional tick marks
- Dual range support
```

---

# 📦 MODULE 3: PAGES DES 11 MONDES

## Objectif
Compléter les pages UI pour chaque monde CHE·NU.

---

### BATCH WLD-03-B1: Monde Gouvernement

**Dépendances:** UI-02-B1, UI-02-B3  
**Estimation:** 4h  
**Backend existant:** `chenu-b25-gov-immobilier.py`  
**Fichiers à créer:**
- `frontend/pages/worlds/government/GovernmentDashboard.tsx`
- `frontend/pages/worlds/government/PermitsManager.tsx`
- `frontend/pages/worlds/government/ComplianceTracker.tsx`
- `frontend/pages/worlds/government/TaxCalculator.tsx`
- `frontend/pages/worlds/government/RegulationsLibrary.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| WLD-03-B1-T1 | GovernmentDashboard | Dashboard services gouvernementaux | 🔴 |
| WLD-03-B1-T2 | PermitsManager | Gestion permis construction | 🔴 |
| WLD-03-B1-T3 | ComplianceTracker | Suivi conformité réglementaire | 🔴 |
| WLD-03-B1-T4 | TaxCalculator | Calculateur taxes QC | 🟡 |
| WLD-03-B1-T5 | RegulationsLibrary | Bibliothèque réglementations | 🟡 |

**Prompt Agent:**
```
Crée les pages du Monde Gouvernement pour CHE·NU.

Context: Construction au Québec, intégrations avec:
- CCQ (Commission de la Construction)
- CNESST (Santé et sécurité)
- RBQ (Régie du bâtiment)
- Revenu Québec

GovernmentDashboard.tsx:
- Stats: Permis en cours, Conformité %, Inspections à venir
- Quick actions: Nouveau permis, Déclaration, Vérification
- Timeline: Échéances importantes
- Alerts: Non-conformités

PermitsManager.tsx:
- Liste des permis avec statut
- Formulaire de demande
- Upload documents
- Suivi progression
- Notifications automatiques

Intégration backend:
- GET /api/gov/permits
- POST /api/gov/permits
- GET /api/gov/compliance/{id}
```

---

### BATCH WLD-03-B2: Monde Immobilier

**Dépendances:** UI-02-B1, INF-01-B4  
**Estimation:** 4h  
**Backend existant:** `chenu-b25-gov-immobilier.py`  
**Fichiers à créer:**
- `frontend/pages/worlds/realestate/RealEstateDashboard.tsx`
- `frontend/pages/worlds/realestate/PropertyListings.tsx`
- `frontend/pages/worlds/realestate/PropertyDetail.tsx`
- `frontend/pages/worlds/realestate/MarketAnalytics.tsx`
- `frontend/pages/worlds/realestate/MortgageCalculator.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| WLD-03-B2-T1 | RealEstateDashboard | Dashboard immobilier | 🔴 |
| WLD-03-B2-T2 | PropertyListings | Liste propriétés avec filtres | 🔴 |
| WLD-03-B2-T3 | PropertyDetail | Page détail avec galerie | 🔴 |
| WLD-03-B2-T4 | MarketAnalytics | Analyses marché avec charts | 🟡 |
| WLD-03-B2-T5 | MortgageCalculator | Calculateur hypothécaire | 🟡 |

---

### BATCH WLD-03-B3: Monde Associations

**Dépendances:** UI-02-B1  
**Estimation:** 4h  
**Backend existant:** `chenu-b26-associations-collab.py`  
**Fichiers à créer:**
- `frontend/pages/worlds/associations/AssociationsDashboard.tsx`
- `frontend/pages/worlds/associations/MemberDirectory.tsx`
- `frontend/pages/worlds/associations/EventsCalendar.tsx`
- `frontend/pages/worlds/associations/DonationsTracker.tsx`
- `frontend/pages/worlds/associations/VolunteerManager.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| WLD-03-B3-T1 | AssociationsDashboard | Dashboard OBNL | 🔴 |
| WLD-03-B3-T2 | MemberDirectory | Répertoire membres | 🔴 |
| WLD-03-B3-T3 | EventsCalendar | Calendrier événements | 🟡 |
| WLD-03-B3-T4 | DonationsTracker | Suivi dons | 🟡 |
| WLD-03-B3-T5 | VolunteerManager | Gestion bénévoles | 🟡 |

---

### BATCH WLD-03-B4: Monde Streaming

**Dépendances:** UI-02-B2  
**Estimation:** 4h  
**Backend existant:** `chenu-b21-streaming.py`  
**Fichiers à créer:**
- `frontend/pages/worlds/streaming/StreamingDashboard.tsx`
- `frontend/pages/worlds/streaming/LiveStudio.tsx`
- `frontend/pages/worlds/streaming/VideoLibrary.tsx`
- `frontend/pages/worlds/streaming/AnalyticsPanel.tsx`
- `frontend/pages/worlds/streaming/MonetizationHub.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| WLD-03-B4-T1 | StreamingDashboard | Dashboard streaming | 🔴 |
| WLD-03-B4-T2 | LiveStudio | Interface live avec OBS | 🔴 |
| WLD-03-B4-T3 | VideoLibrary | Bibliothèque VOD | 🟡 |
| WLD-03-B4-T4 | AnalyticsPanel | Stats viewers/engagement | 🟡 |
| WLD-03-B4-T5 | MonetizationHub | Gestion revenus | 🟢 |

---

### BATCH WLD-03-B5: Monde CHE-Learn

**Dépendances:** UI-02-B2, UI-02-B3  
**Estimation:** 4h  
**Backend existant:** `chenu-b17-chelearn.py`  
**Fichiers à créer:**
- `frontend/pages/worlds/chelearn/LearnDashboard.tsx`
- `frontend/pages/worlds/chelearn/CoursePlayer.tsx`
- `frontend/pages/worlds/chelearn/QuizEngine.tsx`
- `frontend/pages/worlds/chelearn/CertificatesGallery.tsx`
- `frontend/pages/worlds/chelearn/LeaderboardPage.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| WLD-03-B5-T1 | LearnDashboard | Dashboard formation | 🔴 |
| WLD-03-B5-T2 | CoursePlayer | Lecteur vidéo avec chapitres | 🔴 |
| WLD-03-B5-T3 | QuizEngine | Moteur de quiz interactif | 🔴 |
| WLD-03-B5-T4 | CertificatesGallery | Galerie certificats | 🟡 |
| WLD-03-B5-T5 | LeaderboardPage | Classement gamifié | 🟡 |

---

# 📦 MODULE 4: BATCHES V4 MANQUANTS (B40-B48)

## Objectif
Compléter les modules avancés du batch V4.

---

### BATCH ADV-04-B1: Smart Contracts UI (B40)

**Dépendances:** INF-01-B1  
**Estimation:** 4h  
**Backend existant:** `chenu-b39-blockchain-core.js`  
**Fichiers à créer:**
- `frontend/pages/blockchain/SmartContractsDashboard.tsx`
- `frontend/pages/blockchain/ContractBuilder.tsx`
- `frontend/pages/blockchain/ContractDeployer.tsx`
- `frontend/pages/blockchain/TransactionHistory.tsx`
- `frontend/pages/blockchain/WalletConnect.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| ADV-04-B1-T1 | SmartContractsDashboard | Dashboard contrats | 🔴 |
| ADV-04-B1-T2 | ContractBuilder | Builder visuel contrats | 🔴 |
| ADV-04-B1-T3 | ContractDeployer | Déploiement sur chain | 🔴 |
| ADV-04-B1-T4 | TransactionHistory | Historique transactions | 🟡 |
| ADV-04-B1-T5 | WalletConnect | Connexion wallets | 🟡 |

---

### BATCH ADV-04-B2: IoT Dashboard (B41-B42)

**Dépendances:** INF-01-B4, UI-02-B3  
**Estimation:** 4h  
**Backend existant:** `chenu-b13-iot.py`  
**Fichiers à créer:**
- `frontend/pages/iot/IoTDashboard.tsx`
- `frontend/pages/iot/SensorGrid.tsx`
- `frontend/pages/iot/DeviceManager.tsx`
- `frontend/pages/iot/AlertsCenter.tsx`
- `frontend/pages/iot/SensorDataCharts.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| ADV-04-B2-T1 | IoTDashboard | Dashboard IoT construction | 🔴 |
| ADV-04-B2-T2 | SensorGrid | Grille capteurs temps réel | 🔴 |
| ADV-04-B2-T3 | DeviceManager | Gestion appareils | 🟡 |
| ADV-04-B2-T4 | AlertsCenter | Centre alertes capteurs | 🟡 |
| ADV-04-B2-T5 | SensorDataCharts | Graphiques données capteurs | 🟡 |

---

### BATCH ADV-04-B3: Plugin Marketplace (B43-B44)

**Dépendances:** UI-02-B1  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/pages/marketplace/MarketplaceDashboard.tsx`
- `frontend/pages/marketplace/PluginBrowser.tsx`
- `frontend/pages/marketplace/PluginDetail.tsx`
- `frontend/pages/marketplace/InstalledPlugins.tsx`
- `frontend/pages/marketplace/PluginDeveloper.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| ADV-04-B3-T1 | MarketplaceDashboard | Dashboard marketplace | 🔴 |
| ADV-04-B3-T2 | PluginBrowser | Navigation plugins | 🔴 |
| ADV-04-B3-T3 | PluginDetail | Page détail plugin | 🟡 |
| ADV-04-B3-T4 | InstalledPlugins | Gestion installés | 🟡 |
| ADV-04-B3-T5 | PluginDeveloper | Kit développeur | 🟢 |

---

### BATCH ADV-04-B4: ML Analytics (B45-B46)

**Dépendances:** INF-01-B4, UI-02-B3  
**Estimation:** 4h  
**Backend existant:** `chenu-v24-sprint13-erp-ml-bi.py`  
**Fichiers à créer:**
- `frontend/pages/ml/MLDashboard.tsx`
- `frontend/pages/ml/PredictiveAnalytics.tsx`
- `frontend/pages/ml/ModelTrainer.tsx`
- `frontend/pages/ml/VisionAIPanel.tsx`
- `frontend/pages/ml/InsightsExplorer.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| ADV-04-B4-T1 | MLDashboard | Dashboard ML/AI | 🔴 |
| ADV-04-B4-T2 | PredictiveAnalytics | Prédictions avec visualisation | 🔴 |
| ADV-04-B4-T3 | ModelTrainer | Interface entraînement modèles | 🟡 |
| ADV-04-B4-T4 | VisionAIPanel | Computer vision construction | 🟡 |
| ADV-04-B4-T5 | InsightsExplorer | Exploration insights IA | 🟡 |

---

### BATCH ADV-04-B5: Multi-Region & Global (B47-B48)

**Dépendances:** Aucune  
**Estimation:** 4h  
**Backend existant:** `multi-tenancy.py`  
**Fichiers à créer:**
- `frontend/pages/global/GlobalDashboard.tsx`
- `frontend/pages/global/RegionSelector.tsx`
- `frontend/pages/global/LocalizationManager.tsx`
- `frontend/pages/global/ComplianceMatrix.tsx`
- `frontend/pages/global/GlobalIntegrations.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| ADV-04-B5-T1 | GlobalDashboard | Vue multi-régions | 🟡 |
| ADV-04-B5-T2 | RegionSelector | Sélecteur région | 🟡 |
| ADV-04-B5-T3 | LocalizationManager | Gestion traductions | 🟡 |
| ADV-04-B5-T4 | ComplianceMatrix | Matrice conformité pays | 🟢 |
| ADV-04-B5-T5 | GlobalIntegrations | Intégrations globales | 🟢 |

---

# 📦 MODULE 5: FEATURES UX MANQUANTES

## Objectif
Implémenter les features UX identifiées dans le rapport d'amélioration.

---

### BATCH UX-05-B1: Onboarding & Tour

**Dépendances:** UI-02-B2  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/components/onboarding/OnboardingProvider.tsx`
- `frontend/components/onboarding/TourStep.tsx`
- `frontend/components/onboarding/TourTooltip.tsx`
- `frontend/components/onboarding/ProgressIndicator.tsx`
- `frontend/components/onboarding/OnboardingModal.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UX-05-B1-T1 | OnboardingProvider | Context pour tour guidé | 🔴 |
| UX-05-B1-T2 | TourStep | Définition étapes tour | 🔴 |
| UX-05-B1-T3 | TourTooltip | Tooltip pointant élément | 🔴 |
| UX-05-B1-T4 | ProgressIndicator | Barre progression tour | 🟡 |
| UX-05-B1-T5 | OnboardingModal | Modal bienvenue nouveaux users | 🟡 |

---

### BATCH UX-05-B2: Voice Navigation

**Dépendances:** Aucune  
**Estimation:** 4h  
**Backend existant:** `chenu-b14-voice-ai.py`  
**Fichiers à créer:**
- `frontend/components/voice/VoiceProvider.tsx`
- `frontend/components/voice/VoiceButton.tsx`
- `frontend/components/voice/VoiceVisualizer.tsx`
- `frontend/components/voice/VoiceCommands.tsx`
- `frontend/components/voice/VoiceFeedback.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UX-05-B2-T1 | VoiceProvider | Context Web Speech API | 🔴 |
| UX-05-B2-T2 | VoiceButton | Bouton activation micro | 🔴 |
| UX-05-B2-T3 | VoiceVisualizer | Visualisation onde audio | 🟡 |
| UX-05-B2-T4 | VoiceCommands | Parser commandes vocales | 🔴 |
| UX-05-B2-T5 | VoiceFeedback | Feedback vocal Nova | 🟡 |

---

### BATCH UX-05-B3: Accessibility Mode

**Dépendances:** Aucune  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/components/a11y/A11yProvider.tsx`
- `frontend/components/a11y/HighContrastTheme.tsx`
- `frontend/components/a11y/ScreenReaderText.tsx`
- `frontend/components/a11y/KeyboardNav.tsx`
- `frontend/components/a11y/FocusManager.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UX-05-B3-T1 | A11yProvider | Context accessibilité | 🔴 |
| UX-05-B3-T2 | HighContrastTheme | Thème haut contraste | 🔴 |
| UX-05-B3-T3 | ScreenReaderText | Texte pour lecteurs écran | 🟡 |
| UX-05-B3-T4 | KeyboardNav | Navigation clavier complète | 🔴 |
| UX-05-B3-T5 | FocusManager | Gestion focus visible | 🟡 |

---

### BATCH UX-05-B4: Notifications Center

**Dépendances:** UI-02-B2  
**Estimation:** 3h  
**Fichiers à créer:**
- `frontend/components/notifications/NotificationCenter.tsx`
- `frontend/components/notifications/NotificationToast.tsx`
- `frontend/components/notifications/NotificationBadge.tsx`
- `frontend/components/notifications/NotificationPreferences.tsx`
- `frontend/components/notifications/NotificationHistory.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UX-05-B4-T1 | NotificationCenter | Panneau notifications | 🔴 |
| UX-05-B4-T2 | NotificationToast | Toast animé | 🔴 |
| UX-05-B4-T3 | NotificationBadge | Badge avec count | 🟡 |
| UX-05-B4-T4 | NotificationPreferences | Settings notifications | 🟡 |
| UX-05-B4-T5 | NotificationHistory | Historique notifications | 🟢 |

---

### BATCH UX-05-B5: Nova Proactif

**Dépendances:** UI-02-B1  
**Estimation:** 4h  
**Fichiers à créer:**
- `frontend/components/nova/NovaProactiveProvider.tsx`
- `frontend/components/nova/NovaSuggestionCard.tsx`
- `frontend/components/nova/NovaInsightPopup.tsx`
- `frontend/components/nova/NovaContextualHelp.tsx`
- `frontend/components/nova/NovaQuickActions.tsx`

| # | Tâche | Description | Priorité |
|---|-------|-------------|----------|
| UX-05-B5-T1 | NovaProactiveProvider | Système suggestions proactives | 🔴 |
| UX-05-B5-T2 | NovaSuggestionCard | Card suggestion contextuelle | 🔴 |
| UX-05-B5-T3 | NovaInsightPopup | Popup insight automatique | 🟡 |
| UX-05-B5-T4 | NovaContextualHelp | Aide contextuelle | 🟡 |
| UX-05-B5-T5 | NovaQuickActions | Actions rapides suggérées | 🟡 |

---

# 📊 RÉSUMÉ DES BATCHES

## Totaux

| Module | Batches | Tâches | Heures Est. |
|--------|---------|--------|-------------|
| MOD-1: Infrastructure 3D | 5 | 25 | 19h |
| MOD-2: UI Components | 5 | 25 | 17h |
| MOD-3: 11 Mondes | 5 | 25 | 20h |
| MOD-4: Batches V4 | 5 | 25 | 20h |
| MOD-5: Features UX | 5 | 25 | 19h |
| **TOTAL** | **25** | **125** | **95h** |

## Ordre de Priorité Recommandé

```
Phase 1 (Fondations):
├── INF-01-B1: Three.js Base ⭐
├── INF-01-B4: D3.js Charts ⭐
└── UI-02-B1: Glassmorphism ⭐

Phase 2 (UI Premium):
├── INF-01-B2: Particles
├── UI-02-B2: Animations
├── UI-02-B3: Widgets
└── UI-02-B4: Navigation

Phase 3 (Mondes):
├── WLD-03-B1: Gouvernement
├── WLD-03-B2: Immobilier
├── WLD-03-B5: CHE-Learn
└── ...autres mondes

Phase 4 (Avancé):
├── ADV-04-B2: IoT
├── ADV-04-B4: ML Analytics
├── INF-01-B3: Shaders
└── INF-01-B5: Post-Processing

Phase 5 (Polish):
├── UX-05-B1: Onboarding
├── UX-05-B2: Voice
├── UX-05-B5: Nova Proactif
└── ...reste
```

---

## 🎯 INSTRUCTIONS POUR AGENTS

### Comment Utiliser Ce Document

1. **Choisir un batch** selon les dépendances et priorités
2. **Lire le prompt agent** associé
3. **Examiner les fichiers existants** similaires dans le projet
4. **Implémenter les 5 tâches** du batch
5. **Tester** sur les 3 thèmes
6. **Documenter** le code
7. **Passer au batch suivant**

### Convention de Nommage des Commits

```
[BATCH-ID] type: description

Exemples:
[INF-01-B1] feat: Add ThreeProvider context
[UI-02-B3] fix: StatCard3D hover animation
[WLD-03-B1] feat: Complete Government dashboard
```

### Checklist par Batch

```
[ ] Toutes les dépendances sont complétées
[ ] 5 fichiers créés
[ ] Code documenté (JSDoc/docstrings)
[ ] Testé sur theme Dark
[ ] Testé sur theme Light
[ ] Testé sur theme VR
[ ] Responsive mobile
[ ] Accessible (ARIA, keyboard)
[ ] Performance OK (60fps)
```

---

*Document de planification CHE·NU™ V25 - Pour agents IA*
