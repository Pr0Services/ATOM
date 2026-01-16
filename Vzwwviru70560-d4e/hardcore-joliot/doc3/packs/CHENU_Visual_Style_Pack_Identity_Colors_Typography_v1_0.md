# CHEÂ·NU â€” VISUAL STYLE PACK: Identity, Colors, Typography (v1.0 Canonical)
**VERSION:** VISUAL.v1.0-canonical  
**MODE:** PRODUCTION / DESIGN SYSTEM / UNIVERSAL

---

## 1) PRINCIPES ESTHÃ‰TIQUES âš¡

```yaml
CHE-NU_VISUAL_STYLE_PACK:
  version: "1.0-canonical"
  description: "Official CHEÂ·NU visual identity and styling framework. Universal across 2D, 3D, XR."

  principles:
    - clarity_over_decoration
    - luminosity_as_state_indicator
    - spheres_as_color_identities
    - gradients_for_transition_not_flash
    - minimalism_with_depth
    - black_neutral_space_environment
    - soft_edges_everywhere
    - functional_glow (not gaming glow)
    - physics_aware_UI_in_XR (occlusion, parallax)
    - UI_calm_XR_presence_never_overwhelming
```

---

## 2) PALETTE DE COULEURS âš¡

### 2.1 Base Colors âš¡

```yaml
palette_base:
  black: "#0A0B0D"
  dark_gray: "#1A1C20"
  medium_gray: "#2C2F33"
  light_gray: "#C8C8C8"
  white: "#FFFFFF"
```

### 2.2 Semantic Colors âš¡

```yaml
palette_semantic:
  info: "#5BA9FF"
  success: "#6FE8A3"
  warning: "#FFBE55"
  error: "#FF5A5A"
```

### 2.3 Sphere Colors (Official) âš¡

```yaml
sphere_colors:
  personal: "#76E6C7"      # Vert menthe
  business: "#5BA9FF"      # Bleu corporate
  scholar: "#E0C46B"       # Or savoir
  creative: "#FF8BAA"      # Rose crÃ©atif
  social: "#66D06F"        # Vert social
  institutions: "#D08FFF"  # Violet institutionnel
  methodology: "#59D0C6"   # Cyan mÃ©thodique
  xr: "#8EC8FF"            # Bleu XR
  entertainment: "#FFB04D" # Orange divertissement
  ai_lab: "#FF5FFF"        # Magenta IA
  my_team: "#5ED8FF"       # Bleu Ã©quipe
```

---

## 3) GRADIENTS âš¡

### 3.1 Sphere Base Gradient âš¡

```yaml
gradient_sphere_base:
  from: "rgba(255,255,255,0.04)"
  to: "rgba(255,255,255,0.00)"
  angle: 180
```

### 3.2 Luminous Gradients âš¡

```yaml
gradient_luminous:
  white_aura:
    from: "rgba(255,255,255,0.3)"
    to: "rgba(255,255,255,0.0)"
    
  trust_high:
    from: "rgba(120,255,180,0.4)"
    to: "rgba(120,255,180,0.0)"
    
  trust_low:
    from: "rgba(255,150,50,0.35)"
    to: "rgba(255,150,50,0.0)"
```

### 3.3 Sphere Zoom Transition âš¡

```yaml
gradient_sphere_zoom:
  type: "radial"
  center: "50% 50%"
  inner: "rgba(255,255,255,0.10)"
  outer: "rgba(0,0,0,0.75)"
```

---

## 4) TEXTURES âš¡

### 4.1 Surface Textures âš¡

```yaml
textures_surface:
  micrograin_dark: "subtle noise at 3% opacity, neutral dark gray"
  holographic_panel: "light scanlines + 2% blur"
  card_satin: "soft specular reflection at 10Â° angle"
```

### 4.2 XR Textures âš¡

```yaml
textures_xr:
  volumetric_glow: "low-density particle haze"
  aurora_streams: "dynamic gradient ribbons used for threads"
  grid_floor: "10% opacity white lines, 1m spacing"
```

---

## 5) SHADOWS & DEPTH âš¡

### 5.1 Shadow Styles âš¡

```yaml
shadows:
  panel_default: "0px 8px 22px rgba(0,0,0,0.45)"
  card_default: "0px 4px 12px rgba(0,0,0,0.30)"
  floating_button: "0px 10px 24px rgba(0,0,0,0.6)"
  xr_hologram: "glow-shadow: 0 0 25px rgba(120,200,255,0.6)"
```

### 5.2 Depth Layers âš¡

```yaml
depth_layers:
  layer_0: "background"
  layer_1: "navigation"
  layer_2: "content cards"
  layer_3: "panels"
  layer_4: "modals"
  layer_5: "overlays / auras"
  layer_6: "XR portal entry"
```

---

## 6) ICONOGRAPHY âš¡

### 6.1 Icon Style âš¡

```yaml
icon_style:
  style: "thin-line + microglow"
  line_width: 1.75px
  corner_radius: 4px
  glow: "rgba(255,255,255,0.12)"
```

### 6.2 Icon Categories âš¡

```yaml
icon_categories:
  system:
    - home
    - search
    - settings
    - notifications
    - help
    
  content:
    - document
    - note
    - task
    - calendar
    - bookmark
    
  spheres:
    - personal_heart
    - business_briefcase
    - scholar_book
    - creative_palette
    - social_network
    - institutions_gavel
    - methodology_gear
    - xr_cubes
    - entertainment_star
    - ai_lab_chip
    - team_group
    
  agents:
    - nova_orb
    - architect_sigma
    - thread_weaver
    - drift_detector
    - memory_manager
    - ethics_guard
    
  interaction:
    - gesture_hand
    - portal
    - timeline
    - branch
```

---

## 7) SPHERE THEMES âš¡

### 7.1 Application Rules âš¡

```yaml
sphere_theme_rules:
  - primary_color: "sphere_color"
  - soft_glow_on_headers: true
  - gradient_background: "sphere_base_gradient"
  - card_accent_border: "sphere_color at 10% opacity"
```

### 7.2 Theme Examples âš¡

```yaml
theme_personal:
  primary: "#76E6C7"
  accent: "#9FF2DC"
  background_overlay: "rgba(118,230,199,0.05)"

theme_business:
  primary: "#5BA9FF"
  accent: "#82C2FF"
  background_overlay: "rgba(91,169,255,0.05)"

theme_scholar:
  primary: "#E0C46B"
  accent: "#F0D98D"
  background_overlay: "rgba(224,196,107,0.05)"

theme_xr:
  primary: "#8EC8FF"
  accent: "#BDE0FF"
  hologram_glow: "rgba(180,220,255,0.3)"
```

---

## 8) XR VISUAL COMPONENTS âš¡

### 8.1 Ambient Colors âš¡

```yaml
xr_ambient:
  dim: "#0A0B0D"
  neutral: "#111317"
  bright: "#1C1F24"
```

### 8.2 Holograms âš¡

```yaml
xr_holograms:
  color: "#8EC8FF"
  opacity: 0.75
  scanline_intensity: 0.1
```

### 8.3 Portals âš¡

```yaml
xr_portals:
  entry_portal:
    shape: "circular"
    ring_color: "#8EC8FF"
    inner_glow: "rgba(140,200,255,0.35)"
    
  replay_portal:
    shape: "elliptical"
    color: "#FF5FFF"
    distortion: "subtle refractive warp"
```

### 8.4 Threads âš¡

```yaml
xr_threads:
  default_color: "#FF5FFF"
  pulse_speed: "medium"
  thickness: "adaptive"
```

### 8.5 Agent Auras âš¡

```yaml
xr_agent_auras:
  nova:
    color: "#FFFFFF"
    level_glow: [0.3, 0.5, 0.8]
    
  architect_sigma:
    color: "#5BA9FF"
    pattern: "grid_lines"
    
  thread_weaver:
    color: "#FF5FFF"
    pattern: "flowing_ribbons"
```

---

## 9) BUTTONS & COMPONENTS âš¡

### 9.1 Buttons âš¡

```yaml
buttons:
  primary:
    bg: "#5BA9FF"
    text: "#FFFFFF"
    radius: 10
    shadow: "0px 4px 12px rgba(91,169,255,0.45)"
    hover_glow: "0 0 12px rgba(91,169,255,0.5)"
    
  ghost:
    bg: "transparent"
    border: "1px solid rgba(255,255,255,0.15)"
    hover_bg: "rgba(255,255,255,0.04)"
    
  caution:
    bg: "#FF5A5A"
    text: "#FFFFFF"
    hover_bg: "#FF7373"
```

### 9.2 Cards âš¡

```yaml
cards:
  base:
    bg: "#1A1C20"
    radius: 16
    border: "1px solid rgba(255,255,255,0.05)"
    padding: 16
    shadow: "0px 4px 14px rgba(0,0,0,0.35)"
```

---

## 10) MOTION & ANIMATION âš¡

### 10.1 Easing âš¡

```yaml
motion_easing:
  ease_out: "cubic-bezier(.16,1,.3,1)"
  ease_in_out: "cubic-bezier(.4,0,.2,1)"
```

### 10.2 Durations âš¡

```yaml
motion_durations:
  fast: 120ms
  medium: 240ms
  slow: 450ms
```

### 10.3 Effects âš¡

```yaml
motion_effects:
  zoom_in_sphere: "scale 0.92 â†’ 1.00"
  panel_slide_up: "translateY(20px) â†’ 0px"
  aura_pulse: "opacity oscillation slow"
```

---

## 11) TYPOGRAPHY âš¡

### 11.1 Fonts âš¡

```yaml
typography_fonts:
  primary: "Inter"
  fallback: ["SF Pro", "Roboto"]
```

### 11.2 Sizes âš¡

```yaml
typography_sizes:
  h1: 32
  h2: 24
  h3: 18
  body: 15
  small: 13
```

### 11.3 Weights âš¡

```yaml
typography_weights:
  light: 300
  regular: 400
  medium: 500
  semibold: 600
  bold: 700
```

---

## 12) 3D / XR MATERIALS âš¡

```yaml
xr_materials:
  hologram_material:
    base_color: "#8EC8FF"
    transmission: 0.75
    thickness: 0.05
    scatter: 0.1
    fresnel: 0.4
    
  avatar_material:
    base_color: "sphere_color"
    emission_intensity: 1.2
    smoothness: 0.85
    
  portal_material:
    color: "#8EC8FF"
    emission: 1.4
    distortion: 0.15
```

---

## 13) COLOR SUMMARY TABLE âš¡

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      CHEÂ·NU SPHERE COLORS                                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                           â”‚
â”‚  SPHERE           â”‚ HEX       â”‚ DESCRIPTION                              â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚
â”‚  PERSONAL         â”‚ #76E6C7   â”‚ Vert menthe - Vie personnelle            â”‚
â”‚  BUSINESS         â”‚ #5BA9FF   â”‚ Bleu corporate - Affaires                â”‚
â”‚  SCHOLAR          â”‚ #E0C46B   â”‚ Or savoir - Apprentissage                â”‚
â”‚  CREATIVE         â”‚ #FF8BAA   â”‚ Rose crÃ©atif - CrÃ©ativitÃ©                â”‚
â”‚  SOCIAL           â”‚ #66D06F   â”‚ Vert social - Relations                  â”‚
â”‚  INSTITUTIONS     â”‚ #D08FFF   â”‚ Violet institutionnel - Gouvernement     â”‚
â”‚  METHODOLOGY      â”‚ #59D0C6   â”‚ Cyan mÃ©thodique - SystÃ¨mes               â”‚
â”‚  XR               â”‚ #8EC8FF   â”‚ Bleu XR - Immersif                       â”‚
â”‚  ENTERTAINMENT    â”‚ #FFB04D   â”‚ Orange divertissement - Loisirs          â”‚
â”‚  AI_LAB           â”‚ #FF5FFF   â”‚ Magenta IA - ExpÃ©rimentation             â”‚
â”‚  MY_TEAM          â”‚ #5ED8FF   â”‚ Bleu Ã©quipe - Collaboration              â”‚
â”‚                                                                           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 14) CSS VARIABLES (READY TO USE) âš¡

```css
:root {
  /* Base */
  --che-black: #0A0B0D;
  --che-dark-gray: #1A1C20;
  --che-medium-gray: #2C2F33;
  --che-light-gray: #C8C8C8;
  --che-white: #FFFFFF;
  
  /* Semantic */
  --che-info: #5BA9FF;
  --che-success: #6FE8A3;
  --che-warning: #FFBE55;
  --che-error: #FF5A5A;
  
  /* Spheres */
  --sphere-personal: #76E6C7;
  --sphere-business: #5BA9FF;
  --sphere-scholar: #E0C46B;
  --sphere-creative: #FF8BAA;
  --sphere-social: #66D06F;
  --sphere-institutions: #D08FFF;
  --sphere-methodology: #59D0C6;
  --sphere-xr: #8EC8FF;
  --sphere-entertainment: #FFB04D;
  --sphere-ai-lab: #FF5FFF;
  --sphere-my-team: #5ED8FF;
  
  /* Shadows */
  --shadow-panel: 0px 8px 22px rgba(0,0,0,0.45);
  --shadow-card: 0px 4px 12px rgba(0,0,0,0.30);
  --shadow-button: 0px 10px 24px rgba(0,0,0,0.6);
  
  /* Motion */
  --ease-out: cubic-bezier(.16,1,.3,1);
  --ease-in-out: cubic-bezier(.4,0,.2,1);
  --duration-fast: 120ms;
  --duration-medium: 240ms;
  --duration-slow: 450ms;
  
  /* Typography */
  --font-primary: "Inter", "SF Pro", "Roboto", sans-serif;
  --font-size-h1: 32px;
  --font-size-h2: 24px;
  --font-size-h3: 18px;
  --font-size-body: 15px;
  --font-size-small: 13px;
}
```

---

**END â€” VISUAL STYLE PACK v1.0**
