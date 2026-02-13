/**
 * AT·OM DESIGN TOKENS
 * ===================
 *
 * Unified design system for the entire AT·OM interface.
 * All colors, spacing, typography, and animations in one place.
 *
 * PHILOSOPHY:
 * Coherence in diversity - each module has its accent,
 * but shares the same foundation.
 */

// =============================================================================
// COLOR PALETTE
// =============================================================================

export const COLORS = {
  // Core palette - Used everywhere
  black: '#000000',
  white: '#FFFFFF',
  gold: '#D4AF37',      // Primary accent - AT·OM signature
  cobalt: '#0047AB',    // Secondary accent - Trust/stability

  // Module accents
  modules: {
    genie: '#FFD700',      // Education - Warm gold/yellow
    alchimie: '#9B59B6',   // Transmutation - Purple/mystical
    flux: '#00CED1',       // Economy - Cyan/flow
    sante: '#E74C3C',      // Health - Red/vitality
  },

  // Sphere colors
  spheres: {
    personal: '#4A90D9',
    business: '#D4AF37',
    government: '#8B4513',
    creative: '#9B59B6',
    community: '#27AE60',
    social: '#3498DB',
    entertainment: '#F39C12',
    team: '#E74C3C',
    scholar: '#1ABC9C',
  },

  // Semantic colors
  success: '#27AE60',
  warning: '#F39C12',
  error: '#E74C3C',
  info: '#3498DB',

  // Text colors with proper contrast (WCAG AA compliant)
  text: {
    primary: '#FFFFFF',
    secondary: 'rgba(255, 255, 255, 0.7)',   // 4.5:1 contrast on black
    tertiary: 'rgba(255, 255, 255, 0.5)',    // For less important info
    muted: 'rgba(255, 255, 255, 0.3)',       // Hints only
  },

  // Background variations
  background: {
    primary: '#000000',
    elevated: 'rgba(255, 255, 255, 0.05)',
    overlay: 'rgba(0, 0, 0, 0.9)',
  },

  // Border colors
  border: {
    subtle: 'rgba(255, 255, 255, 0.1)',
    default: 'rgba(255, 255, 255, 0.2)',
    strong: 'rgba(255, 255, 255, 0.4)',
  },
} as const;

// =============================================================================
// SPACING SCALE (4px base)
// =============================================================================

export const SPACING = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  xxl: '48px',
  xxxl: '64px',
} as const;

// =============================================================================
// TYPOGRAPHY
// =============================================================================

export const TYPOGRAPHY = {
  fontFamily: {
    mono: '"Courier New", Courier, monospace',
    system: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },

  fontSize: {
    xs: '10px',
    sm: '12px',
    md: '14px',
    lg: '16px',
    xl: '18px',
    xxl: '24px',
    xxxl: '36px',
    display: '48px',
  },

  fontWeight: {
    normal: 400,
    medium: 500,
    bold: 700,
  },

  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.8,
  },

  letterSpacing: {
    tight: '-0.02em',
    normal: '0',
    wide: '0.1em',
    wider: '0.2em',
    widest: '0.3em',
  },
} as const;

// =============================================================================
// TOUCH TARGETS (Accessibility)
// =============================================================================

export const TOUCH = {
  minTarget: '44px',      // iOS minimum
  comfortable: '48px',    // Recommended
  large: '56px',          // For primary actions
} as const;

// =============================================================================
// BORDERS & RADIUS
// =============================================================================

export const BORDERS = {
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },

  width: {
    thin: '1px',
    default: '2px',
    thick: '3px',
  },
} as const;

// =============================================================================
// ANIMATIONS & TRANSITIONS
// =============================================================================

export const ANIMATION = {
  duration: {
    instant: '0ms',
    fast: '100ms',
    normal: '200ms',
    slow: '300ms',
    verySlow: '500ms',
  },

  easing: {
    linear: 'linear',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
    spring: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

// =============================================================================
// BREAKPOINTS (Mobile-first)
// =============================================================================

export const BREAKPOINTS = {
  xs: '320px',
  sm: '480px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  xxl: '1536px',
} as const;

// =============================================================================
// Z-INDEX SCALE
// =============================================================================

export const Z_INDEX = {
  base: 0,
  dropdown: 100,
  sticky: 200,
  overlay: 300,
  modal: 400,
  popover: 500,
  tooltip: 600,
  toast: 700,
  maximum: 9999,
} as const;

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Check if user prefers reduced motion
 */
export const prefersReducedMotion = (): boolean => {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

/**
 * Check if device supports hover
 */
export const supportsHover = (): boolean => {
  if (typeof window === 'undefined') return true;
  return window.matchMedia('(hover: hover)').matches;
};

/**
 * Check if device is touch-primary
 */
export const isTouchDevice = (): boolean => {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(hover: none)').matches;
};

/**
 * Get current breakpoint
 */
export const getCurrentBreakpoint = (): string => {
  if (typeof window === 'undefined') return 'lg';
  const width = window.innerWidth;
  if (width < 480) return 'xs';
  if (width < 768) return 'sm';
  if (width < 1024) return 'md';
  if (width < 1280) return 'lg';
  if (width < 1536) return 'xl';
  return 'xxl';
};

/**
 * Get animation duration based on user preference
 */
export const getAnimationDuration = (duration: keyof typeof ANIMATION.duration): string => {
  if (prefersReducedMotion()) return ANIMATION.duration.instant;
  return ANIMATION.duration[duration];
};

// =============================================================================
// CSS CUSTOM PROPERTIES (for use in CSS-in-JS)
// =============================================================================

export const cssVariables = `
  :root {
    /* Colors */
    --color-black: ${COLORS.black};
    --color-white: ${COLORS.white};
    --color-gold: ${COLORS.gold};
    --color-cobalt: ${COLORS.cobalt};
    --color-success: ${COLORS.success};
    --color-warning: ${COLORS.warning};
    --color-error: ${COLORS.error};

    /* Text */
    --text-primary: ${COLORS.text.primary};
    --text-secondary: ${COLORS.text.secondary};
    --text-tertiary: ${COLORS.text.tertiary};

    /* Spacing */
    --space-xs: ${SPACING.xs};
    --space-sm: ${SPACING.sm};
    --space-md: ${SPACING.md};
    --space-lg: ${SPACING.lg};
    --space-xl: ${SPACING.xl};

    /* Typography */
    --font-mono: ${TYPOGRAPHY.fontFamily.mono};
    --font-system: ${TYPOGRAPHY.fontFamily.system};

    /* Animation */
    --duration-fast: ${ANIMATION.duration.fast};
    --duration-normal: ${ANIMATION.duration.normal};
    --duration-slow: ${ANIMATION.duration.slow};

    /* Touch */
    --touch-target: ${TOUCH.minTarget};

    /* Borders */
    --radius-sm: ${BORDERS.radius.sm};
    --radius-md: ${BORDERS.radius.md};
    --radius-lg: ${BORDERS.radius.lg};
  }

  /* Reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    :root {
      --duration-fast: 0ms;
      --duration-normal: 0ms;
      --duration-slow: 0ms;
    }

    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
`;

export default {
  COLORS,
  SPACING,
  TYPOGRAPHY,
  TOUCH,
  BORDERS,
  ANIMATION,
  BREAKPOINTS,
  Z_INDEX,
  prefersReducedMotion,
  supportsHover,
  isTouchDevice,
  getCurrentBreakpoint,
  getAnimationDuration,
  cssVariables,
};
