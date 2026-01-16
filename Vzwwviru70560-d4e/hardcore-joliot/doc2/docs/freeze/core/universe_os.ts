/* =====================================================
   CHE·NU — UNIVERSE OS (FREEZE 1.5 — VERSION FINALE)
   
   🔒 CANONICAL REFERENCE — 10 OFFICIAL SPHERES ONLY
   
   This file defines the root spheres of CHE·NU.
   DO NOT modify without creating a new FREEZE version.
   
   SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
   ===================================================== */

// ─────────────────────────────────────────────────────
// OFFICIAL 10 SPHERES (FREEZE 1.5 FINAL)
// ─────────────────────────────────────────────────────

/**
 * The 10 official root spheres of CHE·NU.
 * This is the CANONICAL list - no additions, no removals.
 */
export const OFFICIAL_SPHERES = [
  'Personal',
  'Business',
  'Creative',
  'Scholar',
  'SocialNetworkMedia',
  'Community',
  'XR',
  'MyTeam',
  'AILab',
  'Entertainment',
] as const;

export type OfficialSphere = typeof OFFICIAL_SPHERES[number];

/**
 * Sphere count - MUST be 10
 */
export const SPHERE_COUNT = 10;

// ─────────────────────────────────────────────────────
// UNIVERSE OS CLASS
// ─────────────────────────────────────────────────────

/**
 * UniverseOS - Core operating system for CHE·NU
 * Manages sphere navigation, context, and routing
 */
export class UniverseOS {
  private static instance: UniverseOS;
  private currentSphere: OfficialSphere | null = null;
  private currentSubSphere: string | null = null;

  private constructor() {}

  /**
   * Singleton instance
   */
  static getInstance(): UniverseOS {
    if (!UniverseOS.instance) {
      UniverseOS.instance = new UniverseOS();
    }
    return UniverseOS.instance;
  }

  /**
   * 🔒 CANONICAL METHOD
   * Returns the 10 official root spheres.
   * DO NOT MODIFY without new FREEZE version.
   */
  static getRootSpheres(): readonly OfficialSphere[] {
    return OFFICIAL_SPHERES;
  }

  /**
   * Validate if a domain is an official sphere
   */
  static isSphere(domain: string): domain is OfficialSphere {
    return OFFICIAL_SPHERES.includes(domain as OfficialSphere);
  }

  /**
   * Get sphere by index (1-based for human readability)
   */
  static getSphereByIndex(index: number): OfficialSphere | null {
    if (index < 1 || index > 10) return null;
    return OFFICIAL_SPHERES[index - 1];
  }

  /**
   * Navigate to a sphere
   */
  navigateTo(sphere: OfficialSphere, subSphere?: string): void {
    if (!UniverseOS.isSphere(sphere)) {
      throw new Error(`Invalid sphere: ${sphere}. Must be one of the 10 official spheres.`);
    }
    this.currentSphere = sphere;
    this.currentSubSphere = subSphere ?? null;
  }

  /**
   * Get current location
   */
  getCurrentLocation(): { sphere: OfficialSphere | null; subSphere: string | null } {
    return {
      sphere: this.currentSphere,
      subSphere: this.currentSubSphere,
    };
  }

  /**
   * Get sphere info
   */
  static getSphereInfo(sphere: OfficialSphere): SphereInfo {
    return SPHERE_INFO[sphere];
  }
}

// ─────────────────────────────────────────────────────
// SPHERE METADATA
// ─────────────────────────────────────────────────────

export interface SphereInfo {
  id: OfficialSphere;
  name: string;
  emoji: string;
  description: string;
  subSpheres: SubSphereDefinition[];
}

export interface SubSphereDefinition {
  id: string;
  name: string;
  primary: OfficialSphere;
  secondary: OfficialSphere[];
  description?: string;
}

/**
 * Complete sphere information (FREEZE 1.5 FINAL)
 */
export const SPHERE_INFO: Record<OfficialSphere, SphereInfo> = {
  Personal: {
    id: 'Personal',
    name: 'Personal',
    emoji: '👤',
    description: 'Espace privé de l\'individu',
    subSpheres: [
      { id: 'health_wellbeing', name: 'Health & Wellbeing', primary: 'Personal', secondary: ['Business', 'MyTeam', 'Community'] },
      { id: 'habits_lifestyle', name: 'Habits & Lifestyle', primary: 'Personal', secondary: ['Creative', 'Scholar'] },
      { id: 'personal_finance', name: 'Personal Finance', primary: 'Personal', secondary: ['Business'] },
      { id: 'personal_development', name: 'Personal Development', primary: 'Personal', secondary: ['Scholar', 'Creative'] },
      { id: 'life_organization', name: 'Life Organization', primary: 'Personal', secondary: ['MyTeam'] },
    ],
  },
  Business: {
    id: 'Business',
    name: 'Business',
    emoji: '💼',
    description: 'Opérations commerciales et professionnelles',
    subSpheres: [
      { id: 'business_finance', name: 'Business Finance', primary: 'Business', secondary: ['Personal'] },
      { id: 'operations', name: 'Operations', primary: 'Business', secondary: ['MyTeam'] },
      { id: 'supply_logistics', name: 'Supply & Logistics', primary: 'Business', secondary: ['Community'] },
      { id: 'construction_industrial', name: 'Construction / Industrial', primary: 'Business', secondary: ['Community', 'XR'] },
      { id: 'commerce', name: 'Commerce', primary: 'Business', secondary: ['SocialNetworkMedia', 'Community'] },
    ],
  },
  Creative: {
    id: 'Creative',
    name: 'Creative',
    emoji: '🎨',
    description: 'Expression artistique et création',
    subSpheres: [
      { id: 'art_media_creation', name: 'Art & Media Creation', primary: 'Creative', secondary: ['SocialNetworkMedia', 'Entertainment'] },
      { id: 'design', name: 'Design', primary: 'Creative', secondary: ['XR', 'Business'] },
      { id: 'imagination_concepts', name: 'Imagination / Concept Worlds', primary: 'Creative', secondary: ['XR', 'AILab'] },
      { id: 'creative_expression', name: 'Creative Expression', primary: 'Creative', secondary: ['SocialNetworkMedia', 'Entertainment'] },
    ],
  },
  Scholar: {
    id: 'Scholar',
    name: 'Scholar',
    emoji: '📚',
    description: 'Apprentissage et recherche',
    subSpheres: [
      { id: 'study', name: 'Study', primary: 'Scholar', secondary: ['Personal'] },
      { id: 'research', name: 'Research', primary: 'Scholar', secondary: ['AILab'] },
      { id: 'documentation', name: 'Documentation', primary: 'Scholar', secondary: ['Business'] },
      { id: 'information_architecture', name: 'Information Architecture', primary: 'Scholar', secondary: ['AILab', 'Creative'] },
    ],
  },
  SocialNetworkMedia: {
    id: 'SocialNetworkMedia',
    name: 'Social Network & Media',
    emoji: '📱',
    description: 'Plateformes sociales et médias',
    subSpheres: [
      { id: 'social_media_platform', name: 'Social Media Platform', primary: 'SocialNetworkMedia', secondary: ['Entertainment', 'Community'], description: 'Posts, media sharing, profiles' },
      { id: 'messaging_interaction', name: 'Messaging & Interaction', primary: 'SocialNetworkMedia', secondary: ['MyTeam'] },
      { id: 'content_feed', name: 'Content Feed', primary: 'SocialNetworkMedia', secondary: ['Creative'], description: 'Non-predictive content feeds' },
      { id: 'media_creation_tools', name: 'Media Creation Tools', primary: 'SocialNetworkMedia', secondary: ['Creative'] },
    ],
  },
  Community: {
    id: 'Community',
    name: 'Community',
    emoji: '🏘️',
    description: 'Communautés, groupes et espaces publics',
    subSpheres: [
      { id: 'groups_pages', name: 'Community Groups & Pages', primary: 'Community', secondary: ['SocialNetworkMedia'], description: 'Linked to social platforms' },
      { id: 'public_announcements', name: 'Public Announcements', primary: 'Community', secondary: ['Personal', 'Business', 'SocialNetworkMedia'] },
      { id: 'forum_reddit_style', name: 'Forum / Reddit-style Space', primary: 'Community', secondary: ['SocialNetworkMedia', 'Scholar'], description: 'Shared identity with social' },
      { id: 'civic_public_services', name: 'Civic Culture & Public Services', primary: 'Community', secondary: ['Business'] },
    ],
  },
  XR: {
    id: 'XR',
    name: 'XR / Spatial',
    emoji: '🥽',
    description: 'Réalité étendue et spatial',
    subSpheres: [
      { id: 'xr_scenes', name: 'XR Scenes', primary: 'XR', secondary: ['Creative', 'AILab'] },
      { id: 'spatial_interaction', name: 'Spatial Interaction', primary: 'XR', secondary: ['MyTeam', 'Entertainment'] },
      { id: 'world_building', name: 'World Building', primary: 'XR', secondary: ['Creative', 'Scholar'] },
    ],
  },
  MyTeam: {
    id: 'MyTeam',
    name: 'MyTeam',
    emoji: '👥',
    description: 'Gestion d\'équipe et collaboration',
    subSpheres: [
      { id: 'team_roles', name: 'Team Roles', primary: 'MyTeam', secondary: ['Business', 'AILab'] },
      { id: 'collaboration', name: 'Collaboration', primary: 'MyTeam', secondary: ['SocialNetworkMedia'] },
      { id: 'delegation', name: 'Delegation', primary: 'MyTeam', secondary: ['Business'] },
      { id: 'coordination_tools', name: 'Coordination Tools', primary: 'MyTeam', secondary: ['Personal', 'Business'] },
    ],
  },
  AILab: {
    id: 'AILab',
    name: 'AI Lab',
    emoji: '🤖',
    description: 'Laboratoire IA (SAFE, non-autonome)',
    subSpheres: [
      { id: 'ai_sandbox', name: 'AI Sandbox (SAFE)', primary: 'AILab', secondary: ['Scholar'], description: 'No autonomy, representational only' },
      { id: 'cognitive_tools', name: 'Cognitive Tools', primary: 'AILab', secondary: ['Creative'] },
      { id: 'concept_simulation', name: 'Concept Simulation', primary: 'AILab', secondary: ['XR', 'Scholar'], description: 'Representational simulations' },
      { id: 'structural_intelligence', name: 'Structural Intelligence Research', primary: 'AILab', secondary: ['Scholar'] },
    ],
  },
  Entertainment: {
    id: 'Entertainment',
    name: 'Entertainment',
    emoji: '🎮',
    description: 'Divertissement, streaming et jeux',
    subSpheres: [
      { id: 'video_streaming', name: 'Video Streaming Platform', primary: 'Entertainment', secondary: ['SocialNetworkMedia'], description: 'Primary streaming service' },
      { id: 'interactive_experiences', name: 'Interactive Experiences', primary: 'Entertainment', secondary: ['XR'] },
      { id: 'games_play', name: 'Games & Play', primary: 'Entertainment', secondary: ['MyTeam', 'SocialNetworkMedia'] },
      { id: 'audience_experience', name: 'Audience Experience', primary: 'Entertainment', secondary: ['Creative'] },
      { id: 'immersion_media', name: 'Immersion Media', primary: 'Entertainment', secondary: ['XR', 'Creative'] },
    ],
  },
};

// ─────────────────────────────────────────────────────
// INVALID SPHERES (MUST BE TREATED AS MODULES/ENGINES)
// ─────────────────────────────────────────────────────

/**
 * These are NOT spheres - they are internal modules/engines.
 * Any code treating these as spheres MUST be corrected.
 */
export const INVALID_SPHERE_NAMES = [
  'Methodology',
  'MethodologySphere',
  'Skill',
  'SkillSphere',
  'Finance',
  'FinanceSphere',
  'Health',
  'HealthSphere',
  'Productivity',
  'ProductivitySphere',
  'Tools',
  'ToolsSphere',
  'Context',
  'ContextSphere',
  'Simulation',
  'SimulationSphere',
  'Persona',
  'PersonaSphere',
  'Process',
  'ProcessSphere',
  'Template',
  'TemplateSphere',
  'Object',
  'ObjectSphere',
  'Knowledge',
  'KnowledgeSphere',
] as const;

/**
 * Check if a name is an invalid sphere (should be module/engine)
 */
export function isInvalidSphereName(name: string): boolean {
  return INVALID_SPHERE_NAMES.includes(name as any);
}

// ─────────────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────────────

/**
 * Get all sub-spheres across all spheres
 */
export function getAllSubSpheres(): SubSphereDefinition[] {
  return Object.values(SPHERE_INFO).flatMap(s => s.subSpheres);
}

/**
 * Find which sphere a sub-sphere belongs to
 */
export function findPrimarySphere(subSphereId: string): OfficialSphere | null {
  for (const sphere of OFFICIAL_SPHERES) {
    const info = SPHERE_INFO[sphere];
    if (info.subSpheres.some(ss => ss.id === subSphereId)) {
      return sphere;
    }
  }
  return null;
}

/**
 * Get sub-spheres that serve a specific sphere (as secondary)
 */
export function getServingSubSpheres(sphere: OfficialSphere): SubSphereDefinition[] {
  return getAllSubSpheres().filter(ss => ss.secondary.includes(sphere));
}

// ─────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────

export default UniverseOS;
