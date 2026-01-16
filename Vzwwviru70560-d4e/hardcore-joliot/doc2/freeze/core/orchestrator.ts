/* =====================================================
   CHE·NU — ORCHESTRATOR (FREEZE 1.5 — VERSION FINALE)
   
   🔒 Routes requests to the 10 official spheres ONLY
   
   SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
   ===================================================== */

import {
  UniverseOS,
  OfficialSphere,
  OFFICIAL_SPHERES,
  SPHERE_INFO,
  isInvalidSphereName,
  SubSphereDefinition,
} from './universe_os';

// ─────────────────────────────────────────────────────
// ORCHESTRATOR TYPES
// ─────────────────────────────────────────────────────

export interface OrchestratorRequest {
  input: string;
  context?: OrchestratorContext;
  targetSphere?: OfficialSphere;
  userId?: string;
}

export interface OrchestratorContext {
  currentSphere?: OfficialSphere;
  currentSubSphere?: string;
  userPreferences?: Record<string, unknown>;
  sessionId?: string;
}

export interface OrchestratorResponse {
  targetSphere: OfficialSphere;
  targetSubSphere?: string;
  confidence: number;
  reasoning: string;
  suggestedEngines: string[];
  requiresIdentity: boolean;
}

export interface SphereRoute {
  sphere: OfficialSphere;
  subSphere?: string;
  engines: string[];
}

// ─────────────────────────────────────────────────────
// VALID SPHERES CONSTANT
// ─────────────────────────────────────────────────────

/**
 * 🔒 CANONICAL LIST - DO NOT MODIFY
 * The orchestrator ONLY routes to these 10 spheres.
 */
const VALID_SPHERES: readonly OfficialSphere[] = OFFICIAL_SPHERES;

// ─────────────────────────────────────────────────────
// ORCHESTRATOR CLASS
// ─────────────────────────────────────────────────────

/**
 * CHE·NU Orchestrator
 * Routes user requests to the appropriate sphere and sub-sphere.
 * 
 * IMPORTANT:
 * - Only routes to the 10 official spheres
 * - Does NOT treat Methodology, Skill, Finance, Health as spheres
 * - Those are internal engines/modules invoked WITHIN spheres
 */
export class Orchestrator {
  private static instance: Orchestrator;
  private universeOS: UniverseOS;

  private constructor() {
    this.universeOS = UniverseOS.getInstance();
  }

  static getInstance(): Orchestrator {
    if (!Orchestrator.instance) {
      Orchestrator.instance = new Orchestrator();
    }
    return Orchestrator.instance;
  }

  /**
   * Validate if a domain is a valid sphere for routing
   */
  isSphere(domain: string): domain is OfficialSphere {
    return VALID_SPHERES.includes(domain as OfficialSphere);
  }

  /**
   * Route a request to the appropriate sphere
   */
  route(request: OrchestratorRequest): OrchestratorResponse {
    // If target sphere is specified and valid, use it
    if (request.targetSphere && this.isSphere(request.targetSphere)) {
      return this.buildResponse(request.targetSphere, request.input);
    }

    // Detect sphere from input
    const detected = this.detectSphere(request.input, request.context);
    return detected;
  }

  /**
   * Detect which sphere an input belongs to
   */
  private detectSphere(input: string, context?: OrchestratorContext): OrchestratorResponse {
    const normalizedInput = input.toLowerCase();

    // Check each sphere's keywords
    for (const sphere of VALID_SPHERES) {
      const keywords = SPHERE_KEYWORDS[sphere];
      const matchCount = keywords.filter(kw => normalizedInput.includes(kw)).length;
      
      if (matchCount > 0) {
        const confidence = Math.min(0.9, 0.5 + (matchCount * 0.1));
        return this.buildResponse(sphere, input, confidence);
      }
    }

    // Default to Personal if no match
    return this.buildResponse('Personal', input, 0.3);
  }

  /**
   * Build orchestrator response
   */
  private buildResponse(
    sphere: OfficialSphere,
    input: string,
    confidence: number = 0.8
  ): OrchestratorResponse {
    const sphereInfo = SPHERE_INFO[sphere];
    const subSphere = this.detectSubSphere(sphere, input);
    const engines = this.getSuggestedEngines(sphere, subSphere);
    const requiresIdentity = this.checkIdentityRequired(sphere);

    return {
      targetSphere: sphere,
      targetSubSphere: subSphere?.id,
      confidence,
      reasoning: `Routed to ${sphere} based on input analysis`,
      suggestedEngines: engines,
      requiresIdentity,
    };
  }

  /**
   * Detect sub-sphere within a sphere
   */
  private detectSubSphere(sphere: OfficialSphere, input: string): SubSphereDefinition | null {
    const sphereInfo = SPHERE_INFO[sphere];
    const normalizedInput = input.toLowerCase();

    for (const subSphere of sphereInfo.subSpheres) {
      const keywords = subSphere.name.toLowerCase().split(/[\s\/&]+/);
      if (keywords.some(kw => normalizedInput.includes(kw))) {
        return subSphere;
      }
    }

    return null;
  }

  /**
   * Get suggested engines for a sphere/sub-sphere
   */
  private getSuggestedEngines(sphere: OfficialSphere, subSphere?: SubSphereDefinition | null): string[] {
    const engines: string[] = [];

    // Base engines per sphere
    const baseEngines = SPHERE_ENGINES[sphere] || [];
    engines.push(...baseEngines);

    // Sub-sphere specific engines
    if (subSphere) {
      const subEngines = SUB_SPHERE_ENGINES[subSphere.id] || [];
      engines.push(...subEngines);
    }

    return [...new Set(engines)]; // Remove duplicates
  }

  /**
   * Check if sphere requires unified identity
   */
  private checkIdentityRequired(sphere: OfficialSphere): boolean {
    // These spheres share the unified identity system
    const identitySpheres: OfficialSphere[] = [
      'SocialNetworkMedia',
      'Community',
      'Entertainment',
      'MyTeam',
      'XR',
    ];
    return identitySpheres.includes(sphere);
  }

  /**
   * Get all valid routes
   */
  getValidRoutes(): SphereRoute[] {
    const routes: SphereRoute[] = [];

    for (const sphere of VALID_SPHERES) {
      const info = SPHERE_INFO[sphere];
      
      // Root sphere route
      routes.push({
        sphere,
        engines: SPHERE_ENGINES[sphere] || [],
      });

      // Sub-sphere routes
      for (const subSphere of info.subSpheres) {
        routes.push({
          sphere,
          subSphere: subSphere.id,
          engines: [...(SPHERE_ENGINES[sphere] || []), ...(SUB_SPHERE_ENGINES[subSphere.id] || [])],
        });
      }
    }

    return routes;
  }

  /**
   * Validate that a domain should NOT be treated as a sphere
   */
  validateNotSphere(domain: string): { valid: boolean; message: string } {
    if (isInvalidSphereName(domain)) {
      return {
        valid: false,
        message: `"${domain}" is NOT a sphere. It is an internal module/engine. Use the appropriate sphere and invoke ${domain}Engine within it.`,
      };
    }
    return { valid: true, message: 'Valid' };
  }
}

// ─────────────────────────────────────────────────────
// SPHERE KEYWORDS (for detection)
// ─────────────────────────────────────────────────────

const SPHERE_KEYWORDS: Record<OfficialSphere, string[]> = {
  Personal: [
    'personal', 'myself', 'my life', 'health', 'wellbeing', 'wellness',
    'habits', 'lifestyle', 'self', 'private', 'journal', 'diary',
    'my finances', 'personal finance', 'development', 'growth',
  ],
  Business: [
    'business', 'company', 'startup', 'enterprise', 'commerce',
    'operations', 'logistics', 'supply', 'construction', 'industrial',
    'client', 'customer', 'revenue', 'profit', 'b2b',
  ],
  Creative: [
    'creative', 'art', 'design', 'music', 'video', 'photo',
    'imagination', 'concept', 'expression', 'artistic', 'create',
    'draw', 'paint', 'compose', 'craft',
  ],
  Scholar: [
    'study', 'research', 'learn', 'knowledge', 'education',
    'documentation', 'information', 'academic', 'science',
    'paper', 'thesis', 'course', 'lecture',
  ],
  SocialNetworkMedia: [
    'social media', 'social network', 'post', 'share', 'followers',
    'feed', 'profile', 'like', 'comment', 'message', 'dm',
    'timeline', 'stories', 'reels', 'tweet',
  ],
  Community: [
    'community', 'group', 'forum', 'reddit', 'discussion',
    'announcement', 'public', 'civic', 'neighborhood', 'local',
    'pages', 'members', 'moderator',
  ],
  XR: [
    'vr', 'ar', 'xr', 'virtual reality', 'augmented',
    '3d', 'spatial', 'immersive', 'metaverse', 'avatar',
    'scene', 'world building',
  ],
  MyTeam: [
    'team', 'collaboration', 'colleague', 'coworker',
    'delegate', 'coordinate', 'roles', 'project team',
    'teamwork', 'sprint', 'standup',
  ],
  AILab: [
    'ai', 'artificial intelligence', 'machine learning', 'ml',
    'sandbox', 'experiment', 'cognitive', 'neural',
    'model', 'training', 'simulation', 'lab',
  ],
  Entertainment: [
    'entertainment', 'fun', 'game', 'play', 'streaming',
    'video', 'watch', 'movie', 'show', 'series',
    'audience', 'immersion', 'interactive',
  ],
};

// ─────────────────────────────────────────────────────
// SPHERE ENGINES MAPPING
// ─────────────────────────────────────────────────────

/**
 * Base engines per sphere
 * NOTE: These are ENGINES, not spheres!
 */
const SPHERE_ENGINES: Record<OfficialSphere, string[]> = {
  Personal: ['HealthEngine', 'HabitEngine', 'PersonalFinanceEngine', 'DevelopmentEngine'],
  Business: ['BusinessFinanceEngine', 'OperationsEngine', 'ConstructionEngine', 'CommerceEngine'],
  Creative: ['ArtEngine', 'DesignEngine', 'MediaCreationEngine', 'ConceptEngine'],
  Scholar: ['ResearchEngine', 'StudyEngine', 'DocumentationEngine', 'KnowledgeEngine'],
  SocialNetworkMedia: ['SocialEngine', 'MessagingEngine', 'FeedEngine', 'ProfileEngine'],
  Community: ['GroupEngine', 'ForumEngine', 'AnnouncementEngine', 'CivicEngine'],
  XR: ['XRSceneEngine', 'SpatialEngine', 'WorldBuildingEngine', 'AvatarEngine'],
  MyTeam: ['TeamEngine', 'CollaborationEngine', 'DelegationEngine', 'CoordinationEngine'],
  AILab: ['SandboxEngine', 'CognitiveEngine', 'SimulationEngine', 'IntelligenceEngine'],
  Entertainment: ['StreamingEngine', 'GameEngine', 'ImmersionEngine', 'AudienceEngine'],
};

/**
 * Sub-sphere specific engines
 */
const SUB_SPHERE_ENGINES: Record<string, string[]> = {
  // Personal
  health_wellbeing: ['HealthEngine', 'WellnessEngine', 'MentalHealthEngine'],
  habits_lifestyle: ['HabitEngine', 'RoutineEngine', 'LifestyleEngine'],
  personal_finance: ['PersonalFinanceEngine', 'BudgetEngine', 'SavingsEngine'],
  personal_development: ['DevelopmentEngine', 'GrowthEngine', 'SkillEngine'],
  life_organization: ['OrganizationEngine', 'PlanningEngine'],
  
  // Business
  business_finance: ['BusinessFinanceEngine', 'AccountingEngine', 'InvoiceEngine'],
  operations: ['OperationsEngine', 'WorkflowEngine', 'ProcessEngine'],
  supply_logistics: ['SupplyEngine', 'LogisticsEngine', 'InventoryEngine'],
  construction_industrial: ['ConstructionEngine', 'IndustrialEngine', 'SafetyEngine'],
  commerce: ['CommerceEngine', 'SalesEngine', 'CRMEngine'],
  
  // Creative
  art_media_creation: ['ArtEngine', 'MediaCreationEngine', 'CanvasEngine'],
  design: ['DesignEngine', 'UIEngine', 'PrototypeEngine'],
  imagination_concepts: ['ConceptEngine', 'IdeationEngine'],
  creative_expression: ['ExpressionEngine', 'StyleEngine'],
  
  // Scholar
  study: ['StudyEngine', 'LearningEngine', 'FlashcardEngine'],
  research: ['ResearchEngine', 'CitationEngine', 'BibliographyEngine'],
  documentation: ['DocumentationEngine', 'WikiEngine'],
  information_architecture: ['ArchitectureEngine', 'TaxonomyEngine'],
  
  // SocialNetworkMedia
  social_media_platform: ['SocialEngine', 'PostEngine', 'MediaShareEngine'],
  messaging_interaction: ['MessagingEngine', 'ChatEngine', 'NotificationEngine'],
  content_feed: ['FeedEngine', 'CurationEngine'],
  media_creation_tools: ['MediaCreationEngine', 'EditorEngine'],
  
  // Community
  groups_pages: ['GroupEngine', 'PageEngine', 'MembershipEngine'],
  public_announcements: ['AnnouncementEngine', 'BroadcastEngine'],
  forum_reddit_style: ['ForumEngine', 'ThreadEngine', 'VotingEngine'],
  civic_public_services: ['CivicEngine', 'ServiceEngine'],
  
  // XR
  xr_scenes: ['XRSceneEngine', 'RenderEngine', 'LightingEngine'],
  spatial_interaction: ['SpatialEngine', 'InteractionEngine', 'PhysicsEngine'],
  world_building: ['WorldBuildingEngine', 'TerrainEngine', 'AssetEngine'],
  
  // MyTeam
  team_roles: ['TeamEngine', 'RoleEngine', 'PermissionEngine'],
  collaboration: ['CollaborationEngine', 'SharedSpaceEngine'],
  delegation: ['DelegationEngine', 'TaskEngine'],
  coordination_tools: ['CoordinationEngine', 'ScheduleEngine', 'MeetingEngine'],
  
  // AILab
  ai_sandbox: ['SandboxEngine', 'ExperimentEngine'],
  cognitive_tools: ['CognitiveEngine', 'ReasoningEngine'],
  concept_simulation: ['SimulationEngine', 'ModelEngine'],
  structural_intelligence: ['IntelligenceEngine', 'PatternEngine'],
  
  // Entertainment
  video_streaming: ['StreamingEngine', 'VideoEngine', 'PlaybackEngine'],
  interactive_experiences: ['InteractiveEngine', 'ExperienceEngine'],
  games_play: ['GameEngine', 'PlayEngine', 'ScoreEngine'],
  audience_experience: ['AudienceEngine', 'EngagementEngine'],
  immersion_media: ['ImmersionEngine', 'SurroundEngine'],
};

// ─────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────

export default Orchestrator;
