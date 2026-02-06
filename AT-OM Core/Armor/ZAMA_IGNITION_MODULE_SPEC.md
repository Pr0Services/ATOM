# MODULE SPEC: ZAMA IGNITION
## CHE·NU™ / Sphère AT·OM Mapping / Interface RA

**Version:** 1.0  
**Statut:** Conception  
**Sphère:** AT·OM (Systèmes Symboliques & Bio-Résonance)

---

## 1. POSITION ARCHITECTURALE

### 1.1 Intégration dans CHE·NU
```
CHE·NU™
└── Sphères (8 + Scholar)
    └── AT·OM Mapping (Encyclopédie symbolique)
        └── Modules Actifs
            ├── Historical Mapping
            ├── Sacred Geometry Engine
            └── **ZAMA IGNITION** ← Module RA Bio-Résonance
```

### 1.2 Principe de Gouvernance
- **GOUVERNANCE > EXÉCUTION** : L'utilisateur contrôle toutes les activations
- **Human-in-the-Loop** : Aucune modification automatique du profil énergétique
- **Read-Only XR** : La RA observe et affiche, ne modifie pas

---

## 2. WORKFLOW MULTI-AGENTS

### Agent 1: LE SCRIBE (L3 - Spécialiste)
```yaml
role: "Extraction de données et contextualisation"
level: L3
sphere: AT·OM
bureau: DataFiles

input:
  - user_intent: string  # "Protection/Amplification/Ancrage"
  - biometrics:
      thumb_width_cm: float
      palm_width_cm: float
      index_length_cm: float
      fist_width_cm: float
  - energy_profile: enum  # "Subtle" | "High-Resonance" | "Grounded"

action:
  - query: "sacred_geometry_db"
  - query: "lithotherapy_matrix"
  - query: "symbol_frequency_map"
  - calculate: "phi_ratios"

output:
  type: JSON
  schema:
    core_intent: string
    biometrics: object
    selected_nodes: array[SymbolNode]
    energy_frequency: string
    calculated_dimensions: object
    color_palette: array[HexColor]
```

### Agent 2: L'ARCHITECTE (L2 - Coordinateur)
```yaml
role: "Blueprint opérationnel et rendu RA"
level: L2
sphere: AT·OM
bureau: ActiveAgents

input:
  - scribe_output: JSON

action:
  - apply_phi_ratios: "biometrics → dimensions"
  - define_anatomical_coords: ["C7", "Sternum", "Sacrum", "Wrists", "Ankles"]
  - select_technical_palette: ["Grey_Wash", "Ethereal_Blue", "Sacred_Gold"]
  - generate_ar_shaders: ShaderConfig
  - compile_activation_sequence: AnimationTimeline

output:
  type: BlueprintPackage
  contains:
    - ar_overlay_config.json
    - shader_definitions.glsl
    - animation_sequence.json
    - pdf_directive.pdf
```

---

## 3. INTERFACE RA "ZAMA IGNITION"

### 3.1 Écrans Principaux

#### ÉCRAN 1: CALIBRATION (Scanning)
```
┌─────────────────────────────────┐
│  ◉ ZAMA IGNITION               │
│  ─────────────────────────────  │
│                                 │
│      [CAMERA FEED]              │
│                                 │
│    ○ ← Anchor Point: Nuque     │
│    ○ ← Anchor Point: Plexus    │
│    ○ ← Anchor Point: Poignets  │
│                                 │
│  STATUS: Scanning...            │
│  ████████░░░░░░░ 62%           │
│                                 │
│  [ ANNULER ]                    │
└─────────────────────────────────┘
```

#### ÉCRAN 2: ACTIVATION SÉQUENCÉE
```
┌─────────────────────────────────┐
│  ◉ ACTIVATION EN COURS         │
│  ─────────────────────────────  │
│                                 │
│      [BODY OVERLAY 3D]          │
│                                 │
│   ⬡ CUBE MÉTATRON    [████] ✓  │
│   ◎ NADI CONNEXION   [███░]    │
│   ❀ FLEUR DE VIE     [██░░]    │
│   ∞ SCEAUX           [█░░░]    │
│   ☯ TRISKELS         [░░░░]    │
│                                 │
│  ♡ BPM: 72  |  SYNC: Active    │
│                                 │
│  [ PAUSE ]  [ SKIP ]           │
└─────────────────────────────────┘
```

#### ÉCRAN 3: DASHBOARD ACTIF
```
┌─────────────────────────────────┐
│  ◉ ARMURE ZAMA - ACTIVE        │
│  ─────────────────────────────  │
│                                 │
│      [3D OVERLAY LIVE]          │
│                                 │
│  MODE: ○ Combat  ● Repos       │
│                                 │
│  CHARGE ÉNERGÉTIQUE            │
│  ████████████░░░░ 78%          │
│                                 │
│  PIERRES DÉTECTÉES:            │
│  ✓ Œil de Tigre (Plexus)       │
│  ✓ Tourmaline (Poignets)       │
│  ○ Hématite (Non détectée)     │
│                                 │
│  [ DÉSACTIVER ]  [ PARAMÈTRES ]│
└─────────────────────────────────┘
```

### 3.2 Éléments Visuels RA

| Élément | Couleur | Effet | Trigger |
|---------|---------|-------|---------|
| Cube Métatron | #8A2BE2 (Violet) | Halo pulsant | Détection C7 |
| Fleur de Vie | #D4AF37 (Or) | Pulse sync BPM | Détection Sternum |
| Lignes Nadi | #A8C5D8 (Bleu) | Flow animé | Connexion établie |
| Triskels | #2F4C39 (Vert sombre) | Rotation lente | Détection Chevilles |
| Bouclier Combat | #FF4500 (Rouge) | Particules | Mode Combat ON |
| Aura Repos | #E6E6FA (Lavande) | Diffusion douce | Mode Repos ON |

---

## 4. DONNÉES TECHNIQUES

### 4.1 Schema JSON - Scribe Output
```json
{
  "armor_id": "ZAMA-2025-001",
  "timestamp": "2025-01-24T12:00:00Z",
  "core_intent": "Protection/Amplification",
  "biometrics": {
    "thumb_width_cm": 2.1,
    "palm_width_cm": 8.5,
    "index_length_cm": 7.2,
    "fist_width_cm": 9.5
  },
  "calculated_dimensions": {
    "small_symbol_cm": 3.4,
    "medium_symbol_cm": 5.5,
    "large_symbol_cm": 8.9
  },
  "selected_nodes": [
    {
      "id": "metatron_cube",
      "placement": "C7_vertebra",
      "dimension_cm": 4.5,
      "color": "#2D2D2D",
      "frequency_hz": 432
    },
    {
      "id": "flower_of_life",
      "placement": "sternum_plexus",
      "dimension_cm": 9.5,
      "color": "#D4AF37",
      "frequency_hz": 528
    }
  ],
  "external_elements": {
    "metals": ["silver", "gold", "copper"],
    "stones": ["tigers_eye", "black_tourmaline", "hematite"]
  },
  "energy_frequency": "Subtle/High-Resonance"
}
```

### 4.2 Shader Config (GLSL Pseudo)
```glsl
// Zama Ignition - Metatron Cube Shader
uniform float u_time;
uniform float u_bpm_sync;
uniform vec3 u_color_violet;

void main() {
    // Pulse based on heart rate
    float pulse = sin(u_time * u_bpm_sync * 0.1) * 0.5 + 0.5;
    
    // Halo effect
    float glow = smoothstep(0.4, 0.0, length(uv - 0.5));
    
    // Final color with opacity
    vec4 finalColor = vec4(u_color_violet, glow * pulse * 0.6);
    gl_FragColor = finalColor;
}
```

### 4.3 Animation Timeline
```json
{
  "sequence": "ignition",
  "total_duration_ms": 8000,
  "phases": [
    {
      "name": "core_activation",
      "target": "metatron_cube",
      "start_ms": 0,
      "duration_ms": 2000,
      "effect": "fade_in_pulse",
      "audio": "432hz_tone.mp3"
    },
    {
      "name": "nadi_flow",
      "target": "connection_lines",
      "start_ms": 2000,
      "duration_ms": 2500,
      "effect": "progressive_glow",
      "audio": "flow_ambient.mp3"
    },
    {
      "name": "heart_sync",
      "target": "flower_of_life",
      "start_ms": 4500,
      "duration_ms": 2000,
      "effect": "bpm_pulse",
      "audio": "528hz_tone.mp3"
    },
    {
      "name": "full_armor",
      "target": "all_nodes",
      "start_ms": 6500,
      "duration_ms": 1500,
      "effect": "stabilize",
      "audio": "completion_chime.mp3"
    }
  ]
}
```

---

## 5. INTÉGRATION TECHNIQUE

### 5.1 Stack Recommandé
- **Frontend RA:** React Three Fiber + AR.js / 8th Wall
- **Body Tracking:** MediaPipe Pose Detection
- **BPM Detection:** Camera-based PPG (rPPG) ou Apple HealthKit
- **Shaders:** Three.js ShaderMaterial + GLSL
- **Audio:** Tone.js pour les fréquences de résonance

### 5.2 API Endpoints (CHE·NU Backend)
```
POST /api/v1/atom/zama/calibrate
POST /api/v1/atom/zama/activate
GET  /api/v1/atom/zama/status/{armor_id}
PUT  /api/v1/atom/zama/mode/{armor_id}
POST /api/v1/atom/zama/generate-pdf
```

### 5.3 Dépendances Agent
```yaml
scribe_agent:
  requires:
    - sacred_geometry_db
    - lithotherapy_matrix
    - phi_calculator_service
  
architect_agent:
  requires:
    - scribe_agent.output
    - ar_shader_generator
    - pdf_generator_service
    - body_tracking_service
```

---

## 6. GOUVERNANCE & SÉCURITÉ

### 6.1 Checkpoints Humains
- [ ] Validation des mesures biométriques avant calcul
- [ ] Confirmation de l'intention avant génération
- [ ] Approbation du blueprint avant export PDF
- [ ] Consentement explicite pour l'activation RA

### 6.2 Limites du Système
- La RA est **Read-Only** : affichage uniquement
- Aucune donnée médicale n'est stockée sans consentement
- Les fréquences audio sont limitées à des niveaux sûrs
- Le mode "Combat" est purement visuel (pas d'effets physiologiques)

---

## 7. ROADMAP

| Phase | Livrable | Sprint |
|-------|----------|--------|
| v0.1 | Spec + Storyboard | S11 |
| v0.2 | Agent Scribe (JSON output) | S12 |
| v0.3 | Agent Architecte (PDF gen) | S13 |
| v0.4 | Prototype RA (body tracking) | S14 |
| v0.5 | Shaders + Animation | S15 |
| v1.0 | Module complet intégré | S16 |

---

*Document généré par CHE·NU™ System*  
*Sphère: AT·OM Mapping | Module: Zama Ignition*
