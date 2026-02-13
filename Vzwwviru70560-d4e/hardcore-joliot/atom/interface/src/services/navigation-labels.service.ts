/**
 * NAVIGATION LABELS - Toggle Symbolique / Clair
 * ================================================
 *
 * Mapping entre noms symboliques (univers AT·OM) et noms clairs
 * pour permettre aux utilisateurs de basculer entre les deux modes.
 *
 * Usage:
 *   const label = getLabel('le-sceau', language);
 *   // symbolique: "Le Sceau de l'Engagement"
 *   // clair: "Accueil"
 */

type Language = 'symbolique' | 'clair';

export interface NavigationLabel {
  symbolique: string;
  clair: string;
  description: {
    symbolique: string;
    clair: string;
  };
}

// =============================================================================
// ROUTE LABELS
// =============================================================================

export const ROUTE_LABELS: Record<string, NavigationLabel> = {
  // Core pages
  '/': {
    symbolique: "Le Sceau de l'Engagement",
    clair: 'Accueil',
    description: {
      symbolique: 'Le portail sacré vers votre espace personnel',
      clair: 'Page principale pour accéder à la plateforme',
    },
  },
  '/essaim': {
    symbolique: "L'Essaim",
    clair: 'Agents IA',
    description: {
      symbolique: 'Les 350 agents organisés en sphères thématiques',
      clair: '350 assistants IA dans 9 domaines',
    },
  },
  '/dashboard': {
    symbolique: 'Le Nexus',
    clair: 'Tableau de bord',
    description: {
      symbolique: "Point central de convergence des sphères",
      clair: 'Vue d\'ensemble de votre activité',
    },
  },

  // Modules
  '/genie': {
    symbolique: 'Génie de Demain',
    clair: 'Éducation',
    description: {
      symbolique: 'Le laboratoire du savoir futur',
      clair: 'Outils d\'apprentissage et formation',
    },
  },
  '/alchimie': {
    symbolique: 'Alchimie',
    clair: 'Transformation',
    description: {
      symbolique: 'Transmutation et métamorphose',
      clair: 'Outils de transformation et conversion',
    },
  },
  '/flux': {
    symbolique: 'Le Flux',
    clair: 'Transport & Économie',
    description: {
      symbolique: 'Les courants qui animent le système',
      clair: 'Gestion logistique et financière',
    },
  },
  '/sante': {
    symbolique: 'La Guérison',
    clair: 'Santé',
    description: {
      symbolique: 'Le temple de la régénération',
      clair: 'Suivi santé et bien-être',
    },
  },

  // Admin
  '/sovereign': {
    symbolique: 'Sovereign',
    clair: 'Monitoring',
    description: {
      symbolique: 'Le regard fréquentiel sur le système',
      clair: 'Surveillance et métriques système',
    },
  },
  '/admin': {
    symbolique: 'Le Cockpit',
    clair: 'Administration',
    description: {
      symbolique: 'Le siège du commandement suprême',
      clair: 'Panneau d\'administration avancé',
    },
  },
  '/protocol-999': {
    symbolique: 'Protocol-999',
    clair: 'Arrêt d\'urgence',
    description: {
      symbolique: "L'ultime recours — le kill-switch",
      clair: 'Bouton d\'arrêt d\'urgence du système',
    },
  },

  // Other
  '/landing': {
    symbolique: 'Le Portail',
    clair: 'Page d\'accueil',
    description: {
      symbolique: 'La porte d\'entrée vers AT·OM',
      clair: 'Page de présentation de la plateforme',
    },
  },
  '/analytics': {
    symbolique: "L'Oracle",
    clair: 'Analytiques',
    description: {
      symbolique: 'La vision omnisciente des parcours',
      clair: 'Dashboard de statistiques et funnels',
    },
  },
  '/register': {
    symbolique: "L'Initiation",
    clair: 'Inscription',
    description: {
      symbolique: 'Le rite de passage pour rejoindre l\'écosystème',
      clair: 'Créer votre compte',
    },
  },
};

// =============================================================================
// SPHERE LABELS
// =============================================================================

export const SPHERE_LABELS: Record<string, NavigationLabel> = {
  health: {
    symbolique: 'Guérison',
    clair: 'Santé',
    description: {
      symbolique: 'La sphère de régénération vitale',
      clair: 'Santé et bien-être personnel',
    },
  },
  finance: {
    symbolique: 'Alchimie Dorée',
    clair: 'Finance',
    description: {
      symbolique: 'La transmutation des ressources',
      clair: 'Gestion financière et patrimoine',
    },
  },
  education: {
    symbolique: 'Génie',
    clair: 'Éducation',
    description: {
      symbolique: 'Le creuset du savoir',
      clair: 'Formation et apprentissage',
    },
  },
  governance: {
    symbolique: 'Souveraineté',
    clair: 'Gouvernance',
    description: {
      symbolique: 'Le trône des décisions',
      clair: 'Administration et documents',
    },
  },
  energy: {
    symbolique: 'Flux Vital',
    clair: 'Énergie',
    description: {
      symbolique: 'Les courants primordiaux',
      clair: 'Gestion énergétique',
    },
  },
  communication: {
    symbolique: 'Écho',
    clair: 'Communication',
    description: {
      symbolique: "Les résonances entre les êtres",
      clair: 'Interactions et réseaux',
    },
  },
  justice: {
    symbolique: 'Balance',
    clair: 'Justice',
    description: {
      symbolique: "L'équilibre sacré",
      clair: 'Aspects légaux et droits',
    },
  },
  logistics: {
    symbolique: 'Les Veines',
    clair: 'Logistique',
    description: {
      symbolique: 'Les artères du mouvement',
      clair: 'Transport et organisation',
    },
  },
  food: {
    symbolique: 'Sustentation',
    clair: 'Alimentation',
    description: {
      symbolique: "La nourriture de l'être",
      clair: 'Nutrition et approvisionnement',
    },
  },
  technology: {
    symbolique: 'La Forge',
    clair: 'Technologie',
    description: {
      symbolique: "L'atelier de création numérique",
      clair: 'Outils et innovation',
    },
  },
};

// =============================================================================
// UI ELEMENT LABELS
// =============================================================================

export const UI_LABELS: Record<string, Record<Language, string>> = {
  // Actions
  'action.start': { symbolique: 'Activer le Sceau', clair: 'Commencer' },
  'action.continue': { symbolique: 'Poursuivre le Rituel', clair: 'Continuer' },
  'action.finish': { symbolique: 'Sceller', clair: 'Terminer' },
  'action.explore': { symbolique: "Entrer dans l'Essaim", clair: 'Explorer les agents' },
  'action.configure': { symbolique: 'Harmoniser', clair: 'Configurer' },
  'action.sync': { symbolique: 'Résonner', clair: 'Synchroniser' },
  'action.export': { symbolique: 'Cristalliser', clair: 'Exporter' },

  // Status
  'status.connected': { symbolique: 'En Résonance', clair: 'Connecté' },
  'status.disconnected': { symbolique: 'Silence', clair: 'Déconnecté' },
  'status.syncing': { symbolique: 'Harmonisation...', clair: 'Synchronisation...' },
  'status.operational': { symbolique: 'Vibration Stable', clair: 'Opérationnel' },
  'status.degraded': { symbolique: 'Perturbation', clair: 'Dégradé' },

  // Sections
  'section.settings': { symbolique: 'Calibrage', clair: 'Paramètres' },
  'section.profile': { symbolique: 'Identité Souveraine', clair: 'Mon profil' },
  'section.notifications': { symbolique: 'Murmures', clair: 'Notifications' },
  'section.help': { symbolique: 'Guidance', clair: 'Aide' },
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get route label for current language
 */
export function getRouteLabel(path: string, language: Language): string {
  return ROUTE_LABELS[path]?.[language] || path;
}

/**
 * Get route description for current language
 */
export function getRouteDescription(path: string, language: Language): string {
  return ROUTE_LABELS[path]?.description[language] || '';
}

/**
 * Get sphere label for current language
 */
export function getSphereLabel(sphereId: string, language: Language): string {
  return SPHERE_LABELS[sphereId]?.[language] || sphereId;
}

/**
 * Get UI label for current language
 */
export function getUILabel(key: string, language: Language): string {
  return UI_LABELS[key]?.[language] || key;
}

/**
 * Get all navigation items formatted for current language
 */
export function getNavigationItems(language: Language): Array<{
  path: string;
  label: string;
  description: string;
}> {
  return Object.entries(ROUTE_LABELS).map(([path, labels]) => ({
    path,
    label: labels[language],
    description: labels.description[language],
  }));
}

export default { getRouteLabel, getRouteDescription, getSphereLabel, getUILabel };
