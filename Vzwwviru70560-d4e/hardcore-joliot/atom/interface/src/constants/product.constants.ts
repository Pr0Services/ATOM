/**
 * PRODUCT CONSTANTS - Single Source of Truth
 * ==========================================
 *
 * Référentiel centralisé pour toutes les données produit:
 * - Nombre d'agents (350, pas 287 ou 400+)
 * - Nombre de sphères
 * - URLs API/WS
 * - Version, statut bêta
 *
 * Usage: Importez ce fichier partout où ces données sont affichées
 * pour garantir la cohérence à travers l'application.
 */

// =============================================================================
// PRODUCT METRICS
// =============================================================================

export const PRODUCT = {
  // Agent counts - SINGLE SOURCE OF TRUTH
  agents: {
    total: 350,
    display: '350+',
    byCategory: {
      personal: 42,
      business: 38,
      creative: 35,
      scholar: 40,
      social: 32,
      health: 38,
      tech: 45,
      meta: 40,
      sovereign: 40,
    },
  },

  // Spheres
  spheres: {
    total: 9,
    list: [
      'Personal',
      'Business',
      'Creative',
      'Scholar',
      'Social',
      'Health',
      'Tech',
      'Meta',
      'Sovereign',
    ],
  },

  // Version & Status
  version: {
    current: '1.0.0-beta',
    stage: 'beta' as const,
    isProduction: false,
  },

  // Timing guarantees
  timing: {
    signupDuration: '2 minutes',
    firstValueTarget: '5 minutes',
    onboardingSteps: 3,
  },
} as const;

// =============================================================================
// API CONFIGURATION
// =============================================================================

export const API_CONFIG = {
  // Base URLs
  baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',

  // Endpoints
  endpoints: {
    health: '/api/v1/health',
    agents: '/api/v1/agents',
    spheres: '/api/v1/spheres',
    auth: '/api/v1/auth',
    waitlist: '/api/v1/waitlist',
    analytics: '/api/v1/analytics',
  },

  // Timeouts (ms)
  timeouts: {
    default: 10000,
    upload: 60000,
    download: 30000,
  },

  // Retry config
  retry: {
    maxAttempts: 3,
    baseDelay: 1000,
    maxDelay: 10000,
  },
} as const;

// =============================================================================
// FEATURE FLAGS
// =============================================================================

export const FEATURES = {
  // Core features
  enableWaitlist: true,
  enableAnalytics: true,
  enableABTesting: true,
  enableOfflineMode: true,

  // Beta features
  enableAgentWorkspaces: true,
  enableAdvancedGovernance: false,
  enableTokenomics: false, // Simulation mode

  // Debug features
  enableDevTools: import.meta.env.DEV,
  enableMockData: import.meta.env.DEV,
  showSystemStatus: true,
} as const;

// =============================================================================
// BRANDING
// =============================================================================

export const BRANDING = {
  name: 'AT·OM',
  tagline: "L'Intelligence Collective à Votre Service",
  creator: 'Jonathan Rodrigue',
  year: 2026,
  frequency: '999 Hz',

  // Legal
  legal: {
    company: 'AT·OM Platform',
    address: '', // To be filled
    email: 'contact@atom-platform.io',
  },

  // Social
  social: {
    twitter: '@atom_platform',
    github: 'atom-platform',
  },
} as const;

// =============================================================================
// COPY TEMPLATES
// =============================================================================

export const COPY = {
  // Value propositions
  valueProps: {
    main: `${PRODUCT.agents.display} agents IA prêts à vous assister`,
    sub: `${PRODUCT.spheres.total} domaines de vie couverts`,
    cta: 'Aucun compte requis pour commencer',
  },

  // Time estimates (for reassurance)
  timeEstimates: {
    signup: PRODUCT.timing.signupDuration,
    firstValue: PRODUCT.timing.firstValueTarget,
    exploration: '30 secondes',
  },

  // Error messages (user-friendly)
  errors: {
    networkError: 'Connexion temporairement indisponible. Vos données sont sauvegardées localement.',
    authError: 'Session expirée. Veuillez vous reconnecter.',
    serverError: 'Un problème technique est survenu. Notre équipe est prévenue.',
    retryMessage: 'Réessayer',
  },
} as const;

// =============================================================================
// SYSTEM STATUS
// =============================================================================

export type SystemMode = 'production' | 'beta' | 'simulation' | 'maintenance';

export const SYSTEM_STATUS = {
  currentMode: 'beta' as SystemMode,

  // Status messages per mode
  messages: {
    production: null,
    beta: 'Version bêta — Certaines fonctionnalités sont en développement',
    simulation: 'Mode simulation — Les données ne sont pas persistées',
    maintenance: 'Maintenance en cours — Retour prévu dans quelques minutes',
  },

  // Degraded state thresholds
  thresholds: {
    latencyWarning: 500,   // ms
    latencyCritical: 2000, // ms
    errorRateWarning: 0.01,
    errorRateCritical: 0.05,
  },
} as const;

// =============================================================================
// EXPORTS
// =============================================================================

export default {
  PRODUCT,
  API_CONFIG,
  FEATURES,
  BRANDING,
  COPY,
  SYSTEM_STATUS,
};
