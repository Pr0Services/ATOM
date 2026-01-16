# 🎨 CHE·NU™ THEME CUSTOMIZATION SYSTEM
## Système de Personnalisation Visuelle des Sphères & Entités

---

# 📐 VUE D'ENSEMBLE

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU THEME ARCHITECTURE                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   NIVEAU 1: UNIVERS (Map Globale)                                        ║
║   └── Thème par défaut de l'utilisateur                                  ║
║                                                                           ║
║   NIVEAU 2: SPHÈRE (8 domaines)                                          ║
║   └── Chaque sphère peut avoir son propre thème                          ║
║   └── Hérite du thème Univers si non spécifié                            ║
║                                                                           ║
║   NIVEAU 3: ENTITÉ (Sous-identités)                                      ║
║   └── Chaque entité peut avoir son propre thème                          ║
║   └── Hérite du thème Sphère parent si non spécifié                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

# 🎭 LES 4 THÈMES DISPONIBLES

| ID | Thème | Icône | Description | Ambiance |
|----|-------|-------|-------------|----------|
| `natural` | 🌿 Natural | 🍃 | Bois, plantes, organique | Chaleureux, vivant |
| `atlantis` | 🏛️ Atlantis | 🏺 | Pierre, bronze, ancien | Mystique, majestueux |
| `futuristic` | 🚀 Futuristic | 💠 | Tech, holo, néon | Moderne, innovant |
| `astral` | ✨ Astral | ⭐ | Cosmique, cristal, lumière | Transcendant, spirituel |

---

# 🔷 SYMBOLES DES 8 SPHÈRES

## Définition des Symboles

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                         SPHERE SYMBOLS                                    ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   🏠 PERSONAL          💼 BUSINESS          🏛️ GOVERNMENT                ║
║                                                                           ║
║       ◇                    ⬡                    ⫏⫐                       ║
║                                                                           ║
║   Diamant              Hexagone              Colonnes                     ║
║   (Intimité)           (Structure)           (Institution)                ║
║   #3EB4A2              #5BA9FF               #9B8FD0                      ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   🎨 CREATIVE          👥 COMMUNITY          📱 SOCIAL                    ║
║                                                                           ║
║       ✦                    ◉                    ⊛                        ║
║                                                                           ║
║   Étoile               Cercle Uni            Nodes                        ║
║   (Inspiration)        (Ensemble)            (Connexion)                  ║
║   #FF8BAA              #22C55E               #1DA1F2                      ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   🎬 ENTERTAINMENT     🤝 MY TEAM                                         ║
║                                                                           ║
║       ▷                    ⎔                                             ║
║                                                                           ║
║   Play                 Hex Liés                                           ║
║   (Média/Fun)          (Collaboration)                                    ║
║   #F39C12              #8B5CF6                                            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Table de Référence Symboles

| Sphère | Symbol | Unicode | Couleur | Hex |
|--------|--------|---------|---------|-----|
| Personal | ◇ | U+25C7 | Turquoise | `#3EB4A2` |
| Business | ⬡ | U+2B21 | Bleu | `#5BA9FF` |
| Government | ⫏⫐ | U+2ACF+2AD0 | Lavande | `#9B8FD0` |
| Creative | ✦ | U+2726 | Rose | `#FF8BAA` |
| Community | ◉ | U+25C9 | Vert | `#22C55E` |
| Social | ⊛ | U+229B | Cyan | `#1DA1F2` |
| Entertainment | ▷ | U+25B7 | Orange | `#F39C12` |
| My Team | ⎔ | U+2394 | Violet | `#8B5CF6` |

---

# 🗃️ MODÈLE DE DONNÉES

## Schema TypeScript

```typescript
// ═══════════════════════════════════════════════════════════
// TYPES DE BASE
// ═══════════════════════════════════════════════════════════

type ThemeId = 'natural' | 'atlantis' | 'futuristic' | 'astral';

type SphereId = 
  | 'personal' 
  | 'business' 
  | 'government' 
  | 'creative' 
  | 'community' 
  | 'social' 
  | 'entertainment' 
  | 'team';

interface SphereSymbol {
  id: SphereId;
  name: string;
  emoji: string;
  symbol: string;
  unicode: string;
  color: string;
  description: string;
}

// ═══════════════════════════════════════════════════════════
// THÈMES
// ═══════════════════════════════════════════════════════════

interface Theme {
  id: ThemeId;
  name: string;
  icon: string;
  description: string;
  palette: ThemePalette;
  assets: ThemeAssets;
}

interface ThemePalette {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
}

interface ThemeAssets {
  mapImage: string;           // URL de la map globale
  roomImages: string[];       // URLs des pièces disponibles
  symbolVariants: Record<SphereId, string>; // Symboles stylisés par thème
}

// ═══════════════════════════════════════════════════════════
// CONFIGURATION UTILISATEUR
// ═══════════════════════════════════════════════════════════

interface UserThemeConfig {
  userId: string;
  defaultTheme: ThemeId;      // Thème par défaut (univers)
  sphereThemes: SphereThemeConfig[];
  entities: EntityThemeConfig[];
}

interface SphereThemeConfig {
  sphereId: SphereId;
  theme: ThemeId | null;      // null = hérite du defaultTheme
  roomVariant: number;        // Index de la pièce choisie (0-19)
  symbolPosition: SymbolPosition;
  symbolSize: 'small' | 'medium' | 'large';
  symbolOpacity: number;      // 0.3 - 1.0
}

interface EntityThemeConfig {
  entityId: string;
  parentSphereId: SphereId;
  name: string;
  theme: ThemeId | null;      // null = hérite de la sphère parent
  roomVariant: number;
  symbolOverride?: string;    // Symbole personnalisé optionnel
}

type SymbolPosition = 
  | 'top-left' 
  | 'top-right' 
  | 'top-center'
  | 'bottom-left' 
  | 'bottom-right' 
  | 'bottom-center'
  | 'floating';               // Flottant subtil dans la pièce

// ═══════════════════════════════════════════════════════════
// RÉSOLUTION DE THÈME
// ═══════════════════════════════════════════════════════════

interface ResolvedVisualConfig {
  mapImage: string;
  roomImage: string;
  symbol: {
    character: string;
    color: string;
    position: SymbolPosition;
    size: 'small' | 'medium' | 'large';
    opacity: number;
    themedVariant: string;    // Symbole stylisé selon le thème
  };
  palette: ThemePalette;
}
```

## Schema SQL

```sql
-- ═══════════════════════════════════════════════════════════
-- TABLES THÈMES & SYMBOLES
-- ═══════════════════════════════════════════════════════════

-- Définition des thèmes disponibles
CREATE TABLE themes (
    id VARCHAR(20) PRIMARY KEY,           -- 'natural', 'atlantis', etc.
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(10),
    description TEXT,
    
    -- Palette couleurs
    color_primary VARCHAR(7),
    color_secondary VARCHAR(7),
    color_accent VARCHAR(7),
    color_background VARCHAR(7),
    color_surface VARCHAR(7),
    color_text VARCHAR(7),
    
    -- Assets
    map_image_url TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pièces disponibles par thème
CREATE TABLE theme_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    theme_id VARCHAR(20) REFERENCES themes(id),
    variant_index INTEGER,                -- 0-19
    image_url TEXT NOT NULL,
    tags VARCHAR(50)[],                   -- ['cozy', 'executive', 'creative', etc.]
    recommended_spheres VARCHAR(20)[],    -- Sphères recommandées
    
    UNIQUE(theme_id, variant_index)
);

-- Définition des symboles de sphères
CREATE TABLE sphere_symbols (
    sphere_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    emoji VARCHAR(10),
    symbol_char VARCHAR(5),
    unicode VARCHAR(20),
    default_color VARCHAR(7),
    description TEXT
);

-- Variantes de symboles par thème
CREATE TABLE symbol_theme_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(20) REFERENCES sphere_symbols(sphere_id),
    theme_id VARCHAR(20) REFERENCES themes(id),
    variant_image_url TEXT,               -- Image du symbole stylisé
    variant_description TEXT,
    
    UNIQUE(sphere_id, theme_id)
);

-- ═══════════════════════════════════════════════════════════
-- CONFIGURATION UTILISATEUR
-- ═══════════════════════════════════════════════════════════

-- Configuration thème par défaut utilisateur
CREATE TABLE user_theme_config (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    default_theme VARCHAR(20) REFERENCES themes(id) DEFAULT 'natural',
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Configuration thème par sphère
CREATE TABLE user_sphere_themes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    sphere_id VARCHAR(20) REFERENCES sphere_symbols(sphere_id),
    
    -- Thème (null = hérite du défaut)
    theme_override VARCHAR(20) REFERENCES themes(id),
    
    -- Pièce choisie
    room_variant INTEGER DEFAULT 0,
    
    -- Configuration symbole
    symbol_position VARCHAR(20) DEFAULT 'top-right',
    symbol_size VARCHAR(10) DEFAULT 'small',
    symbol_opacity DECIMAL(3,2) DEFAULT 0.7,
    
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, sphere_id)
);

-- Configuration thème par entité (sous-sphère)
CREATE TABLE user_entity_themes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    entity_id UUID NOT NULL,              -- ID de l'entité
    parent_sphere_id VARCHAR(20) REFERENCES sphere_symbols(sphere_id),
    entity_name VARCHAR(100),
    
    -- Thème (null = hérite de la sphère parent)
    theme_override VARCHAR(20) REFERENCES themes(id),
    
    -- Pièce choisie
    room_variant INTEGER DEFAULT 0,
    
    -- Symbole personnalisé optionnel
    custom_symbol VARCHAR(10),
    
    -- Configuration symbole
    symbol_position VARCHAR(20) DEFAULT 'top-right',
    symbol_size VARCHAR(10) DEFAULT 'small',
    symbol_opacity DECIMAL(3,2) DEFAULT 0.6,
    
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, entity_id)
);

-- ═══════════════════════════════════════════════════════════
-- DONNÉES INITIALES
-- ═══════════════════════════════════════════════════════════

-- Insert Themes
INSERT INTO themes (id, name, icon, description, color_primary, color_secondary, color_accent) VALUES
('natural', 'Natural', '🌿', 'Organic wood and nature', '#3EB4A2', '#3F7249', '#D8B26A'),
('atlantis', 'Atlantis', '🏛️', 'Ancient stone builders', '#D8B26A', '#8D8371', '#3EB4A2'),
('futuristic', 'Futuristic', '🚀', 'High-tech and holographic', '#00D4FF', '#FFFFFF', '#D8B26A'),
('astral', 'Astral', '✨', 'Cosmic and ethereal', '#D8B26A', '#8B5CF6', '#3EB4A2');

-- Insert Sphere Symbols
INSERT INTO sphere_symbols (sphere_id, name, emoji, symbol_char, unicode, default_color, description) VALUES
('personal', 'Personal', '🏠', '◇', 'U+25C7', '#3EB4A2', 'Diamond - Intimacy & Self'),
('business', 'Business', '💼', '⬡', 'U+2B21', '#5BA9FF', 'Hexagon - Structure & Network'),
('government', 'Government', '🏛️', '⫏⫐', 'U+2ACF', '#9B8FD0', 'Pillars - Institution & Law'),
('creative', 'Creative', '🎨', '✦', 'U+2726', '#FF8BAA', 'Star - Inspiration & Art'),
('community', 'Community', '👥', '◉', 'U+25C9', '#22C55E', 'Circle - Unity & Together'),
('social', 'Social', '📱', '⊛', 'U+229B', '#1DA1F2', 'Nodes - Connection & Network'),
('entertainment', 'Entertainment', '🎬', '▷', 'U+25B7', '#F39C12', 'Play - Media & Fun'),
('team', 'My Team', '🤝', '⎔', 'U+2394', '#8B5CF6', 'Linked Hex - Collaboration & AI');
```

---

# 🎨 INTERFACE UTILISATEUR

## Écran de Sélection de Thème Global

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     🎨 CHOISIR VOTRE UNIVERS                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   Sélectionnez le thème par défaut de votre espace CHE·NU                ║
║                                                                           ║
║   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    ║
║   │             │  │             │  │             │  │             │    ║
║   │   [Image]   │  │   [Image]   │  │   [Image]   │  │   [Image]   │    ║
║   │   Preview   │  │   Preview   │  │   Preview   │  │   Preview   │    ║
║   │             │  │             │  │             │  │             │    ║
║   ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤    ║
║   │ 🌿 Natural  │  │🏛️ Atlantis │  │🚀 Futuristic│  │ ✨ Astral   │    ║
║   │             │  │             │  │             │  │             │    ║
║   │ Chaleureux  │  │  Mystique   │  │   Moderne   │  │ Transcendant│    ║
║   │  Organique  │  │  Majestueux │  │   Innovant  │  │  Spirituel  │    ║
║   │             │  │             │  │             │  │             │    ║
║   │   [  ●  ]   │  │   [  ○  ]   │  │   [  ○  ]   │  │   [  ○  ]   │    ║
║   └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    ║
║                                                                           ║
║   ℹ️ Ce thème sera appliqué à toutes vos sphères par défaut.             ║
║      Vous pourrez personnaliser chaque sphère individuellement.          ║
║                                                                           ║
║                              [ Continuer → ]                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Écran de Personnalisation par Sphère

```
╔═══════════════════════════════════════════════════════════════════════════╗
║              🎨 PERSONNALISER: 💼 BUSINESS                                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ┌─────────────────────────────────┐  ┌─────────────────────────────┐  ║
║   │                                 │  │  THÈME                      │  ║
║   │                                 │  │                             │  ║
║   │         [PREVIEW IMAGE]        │  │  ○ 🌿 Natural               │  ║
║   │                                 │  │  ● 🏛️ Atlantis (sélectionné)│  ║
║   │         Aperçu en direct       │  │  ○ 🚀 Futuristic            │  ║
║   │                                 │  │  ○ ✨ Astral                │  ║
║   │              ⬡                  │  │  ○ ↩️ Hériter (Natural)     │  ║
║   │         (symbole visible)      │  │                             │  ║
║   │                                 │  ├─────────────────────────────┤  ║
║   └─────────────────────────────────┘  │  PIÈCE                      │  ║
║                                        │                             │  ║
║   SYMBOLE: ⬡                           │  ◀ Variante 3/15 ▶          │  ║
║   ├── Position: [Top-Right ▼]          │                             │  ║
║   ├── Taille:   [Small ▼]              │  [Thumbnail] [Thumb] [Thumb]│  ║
║   └── Opacité:  [====●====] 70%        │                             │  ║
║                                        ├─────────────────────────────┤  ║
║                                        │  ENTITÉS (sous-sphères)     │  ║
║   ┌─────────────────────────────────┐  │                             │  ║
║   │ Entités dans cette sphère:      │  │  + Ajouter une entité       │  ║
║   │                                 │  │                             │  ║
║   │ • Client ABC     [🏛️] [Éditer]  │  │  Les entités peuvent avoir  │  ║
║   │ • Projet XYZ     [🚀] [Éditer]  │  │  leur propre thème.        │  ║
║   │ • Partenaire Co  [↩️] [Éditer]  │  │                             │  ║
║   └─────────────────────────────────┘  └─────────────────────────────┘  ║
║                                                                           ║
║            [ Annuler ]                    [ Appliquer ✓ ]                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Écran de Personnalisation d'Entité

```
╔═══════════════════════════════════════════════════════════════════════════╗
║           🎨 PERSONNALISER ENTITÉ: Client ABC                             ║
║           Parent: 💼 Business                                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ┌─────────────────────────────────┐  ┌─────────────────────────────┐  ║
║   │                                 │  │  THÈME                      │  ║
║   │         [PREVIEW IMAGE]        │  │                             │  ║
║   │                                 │  │  ○ 🌿 Natural               │  ║
║   │         Pièce assignée         │  │  ○ 🏛️ Atlantis              │  ║
║   │                                 │  │  ● 🚀 Futuristic (choisi)   │  ║
║   │              ⬡                  │  │  ○ ✨ Astral                │  ║
║   │         (symbole Business)     │  │  ○ ↩️ Hériter (Atlantis)    │  ║
║   │                                 │  │                             │  ║
║   └─────────────────────────────────┘  ├─────────────────────────────┤  ║
║                                        │  PIÈCE                      │  ║
║   SYMBOLE HÉRITÉ: ⬡ (Business)         │                             │  ║
║                                        │  ◀ Variante 7/15 ▶          │  ║
║   □ Utiliser symbole personnalisé      │                             │  ║
║     [________________]                 │  [Thumbnail] [Thumb] [Thumb]│  ║
║                                        │                             │  ║
║   Position: [Top-Right ▼]              └─────────────────────────────┘  ║
║   Opacité:  [===●=====] 60%                                             ║
║                                                                           ║
║            [ Annuler ]                    [ Appliquer ✓ ]                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

# 🖼️ INTÉGRATION VISUELLE DU SYMBOLE

## Positions du Symbole dans la Pièce

```
┌─────────────────────────────────────────────────────────────┐
│ TOP-LEFT          TOP-CENTER           TOP-RIGHT            │
│    ◇                  ◇                    ◇                │
│                                                             │
│                                                             │
│                    [ROOM IMAGE]                             │
│                                                             │
│                         ◇ (FLOATING)                        │
│                                                             │
│                                                             │
│ BOTTOM-LEFT      BOTTOM-CENTER       BOTTOM-RIGHT           │
│    ◇                  ◇                    ◇                │
└─────────────────────────────────────────────────────────────┘
```

## Styles de Symbole par Thème

### 🌿 Natural
```
Symbole gravé dans le bois
- Texture: Wood grain visible
- Effet: Subtle emboss
- Couleur: Légèrement plus foncé que le bois ambiant
- Opacité recommandée: 60-80%
```

### 🏛️ Atlantis
```
Symbole sculpté dans la pierre
- Texture: Stone carved relief
- Effet: Gold inlay accent
- Couleur: Pierre avec trace d'or
- Opacité recommandée: 70-90%
```

### 🚀 Futuristic
```
Symbole holographique flottant
- Texture: Transparent glow
- Effet: Subtle scan lines, pulse animation
- Couleur: Cyan glow with white core
- Opacité recommandée: 50-70%
```

### ✨ Astral
```
Symbole en constellation lumineuse
- Texture: Star points connected
- Effet: Gentle twinkle, nebula background
- Couleur: Gold stars with turquoise connections
- Opacité recommandée: 60-80%
```

---

# 🔧 COMPOSANTS REACT

## ThemeSelector Component

```tsx
// components/theme/ThemeSelector.tsx

import React from 'react';

interface ThemeSelectorProps {
  currentTheme: ThemeId;
  inheritedTheme?: ThemeId;
  onChange: (theme: ThemeId | null) => void;
  showInheritOption?: boolean;
}

const THEMES: Theme[] = [
  { id: 'natural', name: 'Natural', icon: '🌿', description: 'Chaleureux & Organique' },
  { id: 'atlantis', name: 'Atlantis', icon: '🏛️', description: 'Mystique & Majestueux' },
  { id: 'futuristic', name: 'Futuristic', icon: '🚀', description: 'Moderne & Innovant' },
  { id: 'astral', name: 'Astral', icon: '✨', description: 'Transcendant & Spirituel' },
];

export const ThemeSelector: React.FC<ThemeSelectorProps> = ({
  currentTheme,
  inheritedTheme,
  onChange,
  showInheritOption = false,
}) => {
  return (
    <div className="theme-selector">
      {showInheritOption && inheritedTheme && (
        <div 
          className={`theme-option inherit ${currentTheme === null ? 'selected' : ''}`}
          onClick={() => onChange(null)}
        >
          <span className="icon">↩️</span>
          <span className="name">Hériter ({THEMES.find(t => t.id === inheritedTheme)?.name})</span>
        </div>
      )}
      
      {THEMES.map((theme) => (
        <div
          key={theme.id}
          className={`theme-option ${currentTheme === theme.id ? 'selected' : ''}`}
          onClick={() => onChange(theme.id)}
        >
          <div className="theme-preview">
            <img src={`/assets/themes/${theme.id}/preview.jpg`} alt={theme.name} />
          </div>
          <span className="icon">{theme.icon}</span>
          <span className="name">{theme.name}</span>
          <span className="description">{theme.description}</span>
        </div>
      ))}
    </div>
  );
};
```

## SphereSymbol Component

```tsx
// components/sphere/SphereSymbol.tsx

import React from 'react';

interface SphereSymbolProps {
  sphereId: SphereId;
  theme: ThemeId;
  position: SymbolPosition;
  size: 'small' | 'medium' | 'large';
  opacity: number;
  customSymbol?: string;
}

const SPHERE_SYMBOLS: Record<SphereId, SphereSymbol> = {
  personal: { symbol: '◇', color: '#3EB4A2', name: 'Personal' },
  business: { symbol: '⬡', color: '#5BA9FF', name: 'Business' },
  government: { symbol: '⫏⫐', color: '#9B8FD0', name: 'Government' },
  creative: { symbol: '✦', color: '#FF8BAA', name: 'Creative' },
  community: { symbol: '◉', color: '#22C55E', name: 'Community' },
  social: { symbol: '⊛', color: '#1DA1F2', name: 'Social' },
  entertainment: { symbol: '▷', color: '#F39C12', name: 'Entertainment' },
  team: { symbol: '⎔', color: '#8B5CF6', name: 'My Team' },
};

const SIZE_MAP = {
  small: { fontSize: '1.5rem', padding: '0.5rem' },
  medium: { fontSize: '2rem', padding: '0.75rem' },
  large: { fontSize: '3rem', padding: '1rem' },
};

const POSITION_MAP: Record<SymbolPosition, React.CSSProperties> = {
  'top-left': { top: '1rem', left: '1rem' },
  'top-center': { top: '1rem', left: '50%', transform: 'translateX(-50%)' },
  'top-right': { top: '1rem', right: '1rem' },
  'bottom-left': { bottom: '1rem', left: '1rem' },
  'bottom-center': { bottom: '1rem', left: '50%', transform: 'translateX(-50%)' },
  'bottom-right': { bottom: '1rem', right: '1rem' },
  'floating': { top: '50%', right: '2rem', transform: 'translateY(-50%)' },
};

export const SphereSymbol: React.FC<SphereSymbolProps> = ({
  sphereId,
  theme,
  position,
  size,
  opacity,
  customSymbol,
}) => {
  const sphereData = SPHERE_SYMBOLS[sphereId];
  const symbol = customSymbol || sphereData.symbol;
  
  const themeStyles = getThemeSymbolStyle(theme, sphereData.color);
  
  return (
    <div
      className={`sphere-symbol theme-${theme}`}
      style={{
        position: 'absolute',
        ...POSITION_MAP[position],
        ...SIZE_MAP[size],
        opacity,
        ...themeStyles,
      }}
      title={sphereData.name}
    >
      {symbol}
    </div>
  );
};

function getThemeSymbolStyle(theme: ThemeId, baseColor: string): React.CSSProperties {
  switch (theme) {
    case 'natural':
      return {
        color: baseColor,
        textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
        filter: 'drop-shadow(0 2px 4px rgba(139, 90, 43, 0.4))',
      };
    case 'atlantis':
      return {
        color: '#D8B26A',
        textShadow: `0 0 10px ${baseColor}, 0 0 20px rgba(216, 178, 106, 0.5)`,
        filter: 'drop-shadow(0 2px 8px rgba(216, 178, 106, 0.6))',
      };
    case 'futuristic':
      return {
        color: baseColor,
        textShadow: `0 0 15px ${baseColor}, 0 0 30px ${baseColor}`,
        filter: 'drop-shadow(0 0 10px rgba(0, 212, 255, 0.8))',
        animation: 'pulse 2s infinite',
      };
    case 'astral':
      return {
        color: '#D8B26A',
        textShadow: `0 0 20px #D8B26A, 0 0 40px ${baseColor}`,
        filter: 'drop-shadow(0 0 15px rgba(216, 178, 106, 0.9))',
        animation: 'twinkle 3s infinite',
      };
  }
}
```

## RoomViewer Component

```tsx
// components/room/RoomViewer.tsx

import React from 'react';
import { SphereSymbol } from '../sphere/SphereSymbol';

interface RoomViewerProps {
  sphereId: SphereId;
  theme: ThemeId;
  roomVariant: number;
  symbolConfig: {
    position: SymbolPosition;
    size: 'small' | 'medium' | 'large';
    opacity: number;
    customSymbol?: string;
  };
  entityName?: string;
}

export const RoomViewer: React.FC<RoomViewerProps> = ({
  sphereId,
  theme,
  roomVariant,
  symbolConfig,
  entityName,
}) => {
  const roomImageUrl = `/assets/themes/${theme}/rooms/room_${roomVariant.toString().padStart(2, '0')}.jpg`;
  
  return (
    <div className="room-viewer">
      {/* Image de fond de la pièce */}
      <img 
        src={roomImageUrl} 
        alt={`${theme} room variant ${roomVariant}`}
        className="room-background"
      />
      
      {/* Symbole de la sphère */}
      <SphereSymbol
        sphereId={sphereId}
        theme={theme}
        position={symbolConfig.position}
        size={symbolConfig.size}
        opacity={symbolConfig.opacity}
        customSymbol={symbolConfig.customSymbol}
      />
      
      {/* Nom de l'entité si applicable */}
      {entityName && (
        <div className="entity-label">
          {entityName}
        </div>
      )}
    </div>
  );
};
```

---

# 🗺️ LOGIQUE DE RÉSOLUTION DE THÈME

```typescript
// services/themeResolver.ts

export class ThemeResolver {
  
  /**
   * Résout le thème effectif pour une sphère ou entité
   * en suivant la chaîne d'héritage
   */
  static resolveTheme(
    userConfig: UserThemeConfig,
    sphereId: SphereId,
    entityId?: string
  ): ThemeId {
    
    // Si c'est une entité, vérifier son override
    if (entityId) {
      const entityConfig = userConfig.entities.find(e => e.entityId === entityId);
      if (entityConfig?.theme) {
        return entityConfig.theme;
      }
      // Sinon, hérite de la sphère parent
    }
    
    // Vérifier l'override de la sphère
    const sphereConfig = userConfig.sphereThemes.find(s => s.sphereId === sphereId);
    if (sphereConfig?.theme) {
      return sphereConfig.theme;
    }
    
    // Sinon, utiliser le thème par défaut
    return userConfig.defaultTheme;
  }
  
  /**
   * Résout la configuration visuelle complète
   */
  static resolveVisualConfig(
    userConfig: UserThemeConfig,
    sphereId: SphereId,
    entityId?: string
  ): ResolvedVisualConfig {
    
    const theme = this.resolveTheme(userConfig, sphereId, entityId);
    const themeData = THEMES[theme];
    const sphereData = SPHERE_SYMBOLS[sphereId];
    
    // Déterminer la config du symbole
    let symbolConfig: SphereThemeConfig | EntityThemeConfig;
    
    if (entityId) {
      const entityConfig = userConfig.entities.find(e => e.entityId === entityId);
      symbolConfig = entityConfig || this.getDefaultEntityConfig(sphereId);
    } else {
      const sphereConfig = userConfig.sphereThemes.find(s => s.sphereId === sphereId);
      symbolConfig = sphereConfig || this.getDefaultSphereConfig(sphereId);
    }
    
    return {
      mapImage: themeData.assets.mapImage,
      roomImage: themeData.assets.roomImages[symbolConfig.roomVariant],
      symbol: {
        character: sphereData.symbol,
        color: sphereData.color,
        position: symbolConfig.symbolPosition,
        size: symbolConfig.symbolSize,
        opacity: symbolConfig.symbolOpacity,
        themedVariant: themeData.assets.symbolVariants[sphereId],
      },
      palette: themeData.palette,
    };
  }
  
  private static getDefaultSphereConfig(sphereId: SphereId): SphereThemeConfig {
    return {
      sphereId,
      theme: null,
      roomVariant: 0,
      symbolPosition: 'top-right',
      symbolSize: 'small',
      symbolOpacity: 0.7,
    };
  }
  
  private static getDefaultEntityConfig(sphereId: SphereId): EntityThemeConfig {
    return {
      entityId: '',
      parentSphereId: sphereId,
      name: '',
      theme: null,
      roomVariant: 0,
      symbolPosition: 'top-right',
      symbolSize: 'small',
      symbolOpacity: 0.6,
    };
  }
}
```

---

# 📊 EXEMPLE DE CONFIGURATION UTILISATEUR

```json
{
  "userId": "user_12345",
  "defaultTheme": "natural",
  "sphereThemes": [
    {
      "sphereId": "personal",
      "theme": null,
      "roomVariant": 3,
      "symbolPosition": "top-right",
      "symbolSize": "small",
      "symbolOpacity": 0.7
    },
    {
      "sphereId": "business",
      "theme": "atlantis",
      "roomVariant": 7,
      "symbolPosition": "top-right",
      "symbolSize": "medium",
      "symbolOpacity": 0.8
    },
    {
      "sphereId": "creative",
      "theme": "astral",
      "roomVariant": 12,
      "symbolPosition": "floating",
      "symbolSize": "small",
      "symbolOpacity": 0.6
    },
    {
      "sphereId": "team",
      "theme": "futuristic",
      "roomVariant": 5,
      "symbolPosition": "top-left",
      "symbolSize": "small",
      "symbolOpacity": 0.7
    }
  ],
  "entities": [
    {
      "entityId": "entity_client_abc",
      "parentSphereId": "business",
      "name": "Client ABC",
      "theme": "futuristic",
      "roomVariant": 2,
      "symbolPosition": "top-right",
      "symbolSize": "small",
      "symbolOpacity": 0.6
    },
    {
      "entityId": "entity_project_xyz",
      "parentSphereId": "business",
      "name": "Projet XYZ",
      "theme": null,
      "roomVariant": 9,
      "symbolPosition": "bottom-right",
      "symbolSize": "small",
      "symbolOpacity": 0.5
    }
  ]
}
```

## Résultat Visuel de cette Config

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    RÉSULTAT CONFIGURATION                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  UNIVERS MAP: Natural (défaut)                                           ║
║                                                                           ║
║  SPHÈRES:                                                                 ║
║  ├── 🏠 Personal    → Natural (hérité)   [Pièce 3]   ◇ top-right        ║
║  ├── 💼 Business    → Atlantis           [Pièce 7]   ⬡ top-right        ║
║  │   ├── Client ABC → Futuristic        [Pièce 2]   ⬡ top-right        ║
║  │   └── Projet XYZ → Atlantis (hérité) [Pièce 9]   ⬡ bottom-right     ║
║  ├── 🏛️ Government → Natural (hérité)   [Pièce 0]   ⫏⫐ top-right       ║
║  ├── 🎨 Creative    → Astral             [Pièce 12]  ✦ floating         ║
║  ├── 👥 Community   → Natural (hérité)   [Pièce 0]   ◉ top-right        ║
║  ├── 📱 Social      → Natural (hérité)   [Pièce 0]   ⊛ top-right        ║
║  ├── 🎬 Entertainment→ Natural (hérité)  [Pièce 0]   ▷ top-right        ║
║  └── 🤝 My Team     → Futuristic         [Pièce 5]   ⎔ top-left         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

# 🎯 RÉSUMÉ DU SYSTÈME

```
╔═══════════════════════════════════════════════════════════════════════════╗
║               CHE·NU THEME CUSTOMIZATION SYSTEM                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ✅ 4 THÈMES: Natural, Atlantis, Futuristic, Astral                      ║
║                                                                           ║
║  ✅ 8 SYMBOLES UNIQUES (un par sphère)                                   ║
║     ◇ ⬡ ⫏⫐ ✦ ◉ ⊛ ▷ ⎔                                                   ║
║                                                                           ║
║  ✅ HÉRITAGE DE THÈME                                                     ║
║     Univers → Sphère → Entité                                            ║
║                                                                           ║
║  ✅ PERSONNALISATION SYMBOLE                                              ║
║     Position, Taille, Opacité, Style par thème                           ║
║                                                                           ║
║  ✅ ~15-20 PIÈCES PAR THÈME                                               ║
║     Interchangeables, assignables                                        ║
║                                                                           ║
║  ✅ SYMBOLE COMME RAPPEL MÉMOIRE                                          ║
║     Subtil, non-encombrant, toujours présent                             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

*CHE·NU™ Theme Customization System v1.0*
*Complete Specification*
