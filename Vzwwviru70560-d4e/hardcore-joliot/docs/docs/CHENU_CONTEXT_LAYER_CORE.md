############################################################
#                                                          #
#       CHE·NU CONTEXT LAYER                               #
#       CORE ENGINE + SUB-ENGINES                          #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A1 — CORE MODULE: ContextEngine
============================================================

--- FILE: /che-nu-sdk/core/context.ts

/**
 * CHE·NU Context Engine
 * ======================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * The Context Engine provides representational context modeling
 * for CHE·NU structures. It describes scenes, environments,
 * situations, conditions, and constraints WITHOUT execution.
 * 
 * SAFE COMPLIANCE:
 * - No real environment detection
 * - No autonomous decisions
 * - No system integration
 * - Representational structures only
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Environment representation
 */
export interface EnvironmentModel {
  id: string;
  name: string;
  category: 'indoor' | 'outdoor' | 'digital' | 'abstract' | 'workshop';
  description: string;
  attributes: Record<string, any>;
  metadata: {
    created_at?: string;
    template_source?: string;
  };
}

/**
 * Situation representation
 */
export interface SituationModel {
  id: string;
  name: string;
  type: 'collaborative' | 'exploratory' | 'analytical' | 'creative' | 'operational';
  description: string;
  participants: string[];
  objectives: string[];
  metadata: Record<string, any>;
}

/**
 * Scene representation (actors, objects, focal points)
 */
export interface SceneModel {
  id: string;
  name: string;
  description: string;
  actors: SceneActor[];
  objects: SceneObject[];
  focal_points: FocalPoint[];
  energy: 'low' | 'medium' | 'high' | 'dynamic';
  topology: 'linear' | 'radial' | 'clustered' | 'distributed' | 'hierarchical';
  metadata: Record<string, any>;
}

export interface SceneActor {
  id: string;
  name: string;
  role: string;
  position?: string;
}

export interface SceneObject {
  id: string;
  name: string;
  type: string;
  significance: 'primary' | 'secondary' | 'background';
}

export interface FocalPoint {
  id: string;
  name: string;
  description: string;
  priority: number;
}

/**
 * Condition representation
 */
export interface ConditionModel {
  id: string;
  name: string;
  state: 'stable' | 'unstable' | 'dynamic' | 'neutral' | 'transitional';
  description: string;
  factors: ConditionFactor[];
  metadata: Record<string, any>;
}

export interface ConditionFactor {
  name: string;
  value: string;
  impact: 'positive' | 'negative' | 'neutral';
}

/**
 * Constraint representation
 */
export interface ConstraintModel {
  id: string;
  name: string;
  type: 'time' | 'resources' | 'complexity' | 'clarity' | 'scope' | 'dependency';
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  impact_areas: string[];
  metadata: Record<string, any>;
}

/**
 * Complete Context Model
 */
export interface ContextModel {
  id: string;
  name: string;
  description: string;
  environment: EnvironmentModel | null;
  situation: SituationModel | null;
  scene: SceneModel | null;
  conditions: ConditionModel[];
  constraints: ConstraintModel[];
  sphere_links: string[];
  engine_links: string[];
  metadata: {
    created_at: string;
    updated_at: string;
    template_source?: string;
    version: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
  };
}

/**
 * Context creation input
 */
export interface ContextInput {
  name: string;
  description?: string;
  environment?: Partial<EnvironmentModel>;
  situation?: Partial<SituationModel>;
  scene?: Partial<SceneModel>;
  conditions?: Partial<ConditionModel>[];
  constraints?: Partial<ConstraintModel>[];
  sphere_links?: string[];
  engine_links?: string[];
}

/**
 * Context summary
 */
export interface ContextSummary {
  id: string;
  name: string;
  environment_type: string | null;
  situation_type: string | null;
  scene_energy: string | null;
  condition_count: number;
  constraint_count: number;
  engine_count: number;
  sphere_count: number;
}

/**
 * Engine mapping result
 */
export interface EngineMapping {
  context_id: string;
  recommended_engines: string[];
  mapping_rationale: Record<string, string>;
}

/**
 * Context classification
 */
export interface ContextClassification {
  primary_domain: string;
  secondary_domains: string[];
  complexity: 'simple' | 'moderate' | 'complex';
  collaboration_level: 'individual' | 'team' | 'organization';
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(prefix: string): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

function timestamp(): string {
  return new Date().toISOString();
}

// ============================================================
// CONTEXT ENGINE
// ============================================================

export const ContextEngine = {
  /**
   * Engine name
   */
  name: 'ContextEngine',
  
  /**
   * Engine version
   */
  version: '1.0.0',
  
  /**
   * Create a new context
   */
  createContext(input: ContextInput): ContextModel {
    const now = timestamp();
    
    return {
      id: generateId('ctx'),
      name: input.name,
      description: input.description || '',
      environment: input.environment ? {
        id: generateId('env'),
        name: input.environment.name || 'Unnamed Environment',
        category: input.environment.category || 'abstract',
        description: input.environment.description || '',
        attributes: input.environment.attributes || {},
        metadata: { created_at: now },
      } : null,
      situation: input.situation ? {
        id: generateId('sit'),
        name: input.situation.name || 'Unnamed Situation',
        type: input.situation.type || 'exploratory',
        description: input.situation.description || '',
        participants: input.situation.participants || [],
        objectives: input.situation.objectives || [],
        metadata: {},
      } : null,
      scene: input.scene ? {
        id: generateId('scn'),
        name: input.scene.name || 'Unnamed Scene',
        description: input.scene.description || '',
        actors: input.scene.actors || [],
        objects: input.scene.objects || [],
        focal_points: input.scene.focal_points || [],
        energy: input.scene.energy || 'medium',
        topology: input.scene.topology || 'distributed',
        metadata: {},
      } : null,
      conditions: (input.conditions || []).map(c => ({
        id: generateId('cond'),
        name: c.name || 'Unnamed Condition',
        state: c.state || 'neutral',
        description: c.description || '',
        factors: c.factors || [],
        metadata: {},
      })),
      constraints: (input.constraints || []).map(c => ({
        id: generateId('const'),
        name: c.name || 'Unnamed Constraint',
        type: c.type || 'scope',
        severity: c.severity || 'medium',
        description: c.description || '',
        impact_areas: c.impact_areas || [],
        metadata: {},
      })),
      sphere_links: input.sphere_links || [],
      engine_links: input.engine_links || [],
      metadata: {
        created_at: now,
        updated_at: now,
        version: '1.0.0',
      },
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
      },
    };
  },
  
  /**
   * Summarize a context
   */
  summarizeContext(ctx: ContextModel): ContextSummary {
    return {
      id: ctx.id,
      name: ctx.name,
      environment_type: ctx.environment?.category || null,
      situation_type: ctx.situation?.type || null,
      scene_energy: ctx.scene?.energy || null,
      condition_count: ctx.conditions.length,
      constraint_count: ctx.constraints.length,
      engine_count: ctx.engine_links.length,
      sphere_count: ctx.sphere_links.length,
    };
  },
  
  /**
   * Map context to recommended engines
   * REPRESENTATIONAL ONLY — no real recommendations
   */
  mapToEngines(ctx: ContextModel): EngineMapping {
    const engines: string[] = [];
    const rationale: Record<string, string> = {};
    
    // Environment-based mapping
    if (ctx.environment) {
      switch (ctx.environment.category) {
        case 'digital':
          engines.push('XREngine');
          rationale['XREngine'] = 'Digital environment suggests XR capabilities';
          break;
        case 'workshop':
          engines.push('ProcessEngine');
          rationale['ProcessEngine'] = 'Workshop environment suggests process focus';
          break;
        case 'abstract':
          engines.push('KnowledgeEngine');
          rationale['KnowledgeEngine'] = 'Abstract environment suggests knowledge focus';
          break;
      }
    }
    
    // Situation-based mapping
    if (ctx.situation) {
      switch (ctx.situation.type) {
        case 'collaborative':
          engines.push('ProjectEngine');
          rationale['ProjectEngine'] = 'Collaborative situation suggests project structure';
          break;
        case 'analytical':
          engines.push('SimulationEngine');
          rationale['SimulationEngine'] = 'Analytical situation suggests simulation';
          break;
        case 'creative':
          engines.push('TemplateFactoryEngine');
          rationale['TemplateFactoryEngine'] = 'Creative situation suggests template generation';
          break;
      }
    }
    
    // Scene-based mapping
    if (ctx.scene) {
      if (ctx.scene.energy === 'high' || ctx.scene.energy === 'dynamic') {
        engines.push('MissionEngine');
        rationale['MissionEngine'] = 'High energy scene suggests mission focus';
      }
    }
    
    return {
      context_id: ctx.id,
      recommended_engines: [...new Set(engines)],
      mapping_rationale: rationale,
    };
  },
  
  /**
   * Classify a context
   * REPRESENTATIONAL ONLY
   */
  classifyContext(ctx: ContextModel): ContextClassification {
    // Determine primary domain
    let primary = 'general';
    if (ctx.situation) {
      primary = ctx.situation.type;
    } else if (ctx.environment) {
      primary = ctx.environment.category;
    }
    
    // Determine secondary domains
    const secondary: string[] = [];
    if (ctx.scene?.energy === 'high') secondary.push('mission');
    if (ctx.constraints.length > 3) secondary.push('constrained');
    if (ctx.conditions.some(c => c.state === 'dynamic')) secondary.push('dynamic');
    
    // Determine complexity
    let complexity: 'simple' | 'moderate' | 'complex' = 'simple';
    const totalElements = ctx.conditions.length + ctx.constraints.length + ctx.engine_links.length;
    if (totalElements > 10) complexity = 'complex';
    else if (totalElements > 5) complexity = 'moderate';
    
    // Determine collaboration level
    let collaboration: 'individual' | 'team' | 'organization' = 'individual';
    if (ctx.situation?.participants) {
      if (ctx.situation.participants.length > 10) collaboration = 'organization';
      else if (ctx.situation.participants.length > 1) collaboration = 'team';
    }
    
    return {
      primary_domain: primary,
      secondary_domains: secondary,
      complexity,
      collaboration_level: collaboration,
    };
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      description: 'Context modeling engine for CHE·NU',
      capabilities: [
        'context_creation',
        'context_summary',
        'engine_mapping',
        'context_classification',
      ],
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
      },
    };
  },
};

export default ContextEngine;

============================================================
SECTION A2 — SUB-MODULE: SituationEngine
============================================================

--- FILE: /che-nu-sdk/core/context/situation.engine.ts

/**
 * CHE·NU Situation Engine
 * ========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models situation types and structures.
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPES
// ============================================================

export type SituationType = 
  | 'collaborative'
  | 'exploratory'
  | 'analytical'
  | 'creative'
  | 'operational'
  | 'strategic'
  | 'learning'
  | 'review';

export interface SituationModel {
  id: string;
  name: string;
  type: SituationType;
  description: string;
  participants: string[];
  objectives: string[];
  dynamics: SituationDynamics;
  metadata: Record<string, any>;
}

export interface SituationDynamics {
  interaction_mode: 'synchronous' | 'asynchronous' | 'hybrid';
  pace: 'slow' | 'moderate' | 'fast' | 'variable';
  formality: 'informal' | 'semi-formal' | 'formal';
}

export interface SituationInput {
  name: string;
  type: SituationType;
  description?: string;
  participants?: string[];
  objectives?: string[];
  dynamics?: Partial<SituationDynamics>;
}

// ============================================================
// SITUATION TEMPLATES
// ============================================================

const SITUATION_TEMPLATES: Record<SituationType, Partial<SituationModel>> = {
  collaborative: {
    type: 'collaborative',
    description: 'Team-based collaborative work situation',
    dynamics: {
      interaction_mode: 'synchronous',
      pace: 'moderate',
      formality: 'semi-formal',
    },
  },
  exploratory: {
    type: 'exploratory',
    description: 'Discovery and exploration situation',
    dynamics: {
      interaction_mode: 'asynchronous',
      pace: 'variable',
      formality: 'informal',
    },
  },
  analytical: {
    type: 'analytical',
    description: 'Data analysis and insight generation situation',
    dynamics: {
      interaction_mode: 'asynchronous',
      pace: 'slow',
      formality: 'formal',
    },
  },
  creative: {
    type: 'creative',
    description: 'Creative ideation and design situation',
    dynamics: {
      interaction_mode: 'hybrid',
      pace: 'variable',
      formality: 'informal',
    },
  },
  operational: {
    type: 'operational',
    description: 'Day-to-day operational work situation',
    dynamics: {
      interaction_mode: 'synchronous',
      pace: 'fast',
      formality: 'semi-formal',
    },
  },
  strategic: {
    type: 'strategic',
    description: 'Strategic planning and decision-making situation',
    dynamics: {
      interaction_mode: 'synchronous',
      pace: 'slow',
      formality: 'formal',
    },
  },
  learning: {
    type: 'learning',
    description: 'Educational and skill development situation',
    dynamics: {
      interaction_mode: 'hybrid',
      pace: 'moderate',
      formality: 'semi-formal',
    },
  },
  review: {
    type: 'review',
    description: 'Review and evaluation situation',
    dynamics: {
      interaction_mode: 'synchronous',
      pace: 'moderate',
      formality: 'formal',
    },
  },
};

// ============================================================
// UTILITY
// ============================================================

function generateId(): string {
  return `sit_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

// ============================================================
// SITUATION ENGINE
// ============================================================

export const SituationEngine = {
  name: 'SituationEngine',
  version: '1.0.0',
  
  /**
   * List available situation types
   */
  listTypes(): SituationType[] {
    return Object.keys(SITUATION_TEMPLATES) as SituationType[];
  },
  
  /**
   * Build a situation
   */
  buildSituation(input: SituationInput): SituationModel {
    const template = SITUATION_TEMPLATES[input.type] || {};
    
    return {
      id: generateId(),
      name: input.name,
      type: input.type,
      description: input.description || template.description || '',
      participants: input.participants || [],
      objectives: input.objectives || [],
      dynamics: {
        interaction_mode: input.dynamics?.interaction_mode || template.dynamics?.interaction_mode || 'hybrid',
        pace: input.dynamics?.pace || template.dynamics?.pace || 'moderate',
        formality: input.dynamics?.formality || template.dynamics?.formality || 'semi-formal',
      },
      metadata: {},
    };
  },
  
  /**
   * Describe a situation type
   */
  describeSituation(type: SituationType): string {
    const template = SITUATION_TEMPLATES[type];
    return template?.description || 'Unknown situation type';
  },
  
  /**
   * Get template for situation type
   */
  getTemplate(type: SituationType): Partial<SituationModel> | null {
    return SITUATION_TEMPLATES[type] || null;
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      types: this.listTypes(),
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default SituationEngine;

============================================================
SECTION A3 — SUB-MODULE: EnvironmentEngine
============================================================

--- FILE: /che-nu-sdk/core/context/environment.engine.ts

/**
 * CHE·NU Environment Engine
 * ==========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models environment categories and attributes.
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPES
// ============================================================

export type EnvironmentCategory = 
  | 'indoor'
  | 'outdoor'
  | 'digital'
  | 'abstract'
  | 'workshop'
  | 'hybrid';

export interface EnvironmentModel {
  id: string;
  name: string;
  category: EnvironmentCategory;
  description: string;
  attributes: EnvironmentAttributes;
  spatial: SpatialAttributes;
  metadata: Record<string, any>;
}

export interface EnvironmentAttributes {
  lighting: 'natural' | 'artificial' | 'mixed' | 'none';
  noise_level: 'silent' | 'quiet' | 'moderate' | 'loud';
  accessibility: 'open' | 'restricted' | 'private';
  connectivity: 'online' | 'offline' | 'hybrid';
}

export interface SpatialAttributes {
  layout: 'open' | 'partitioned' | 'modular' | 'fixed';
  scale: 'intimate' | 'small' | 'medium' | 'large' | 'vast';
  flexibility: 'rigid' | 'semi-flexible' | 'fully-flexible';
}

export interface EnvironmentInput {
  name: string;
  category: EnvironmentCategory;
  description?: string;
  attributes?: Partial<EnvironmentAttributes>;
  spatial?: Partial<SpatialAttributes>;
}

// ============================================================
// ENVIRONMENT TEMPLATES
// ============================================================

const ENVIRONMENT_TEMPLATES: Record<EnvironmentCategory, Partial<EnvironmentModel>> = {
  indoor: {
    category: 'indoor',
    description: 'Indoor physical space',
    attributes: {
      lighting: 'artificial',
      noise_level: 'quiet',
      accessibility: 'restricted',
      connectivity: 'online',
    },
    spatial: {
      layout: 'partitioned',
      scale: 'medium',
      flexibility: 'semi-flexible',
    },
  },
  outdoor: {
    category: 'outdoor',
    description: 'Outdoor physical space',
    attributes: {
      lighting: 'natural',
      noise_level: 'moderate',
      accessibility: 'open',
      connectivity: 'hybrid',
    },
    spatial: {
      layout: 'open',
      scale: 'large',
      flexibility: 'fully-flexible',
    },
  },
  digital: {
    category: 'digital',
    description: 'Digital/virtual environment',
    attributes: {
      lighting: 'artificial',
      noise_level: 'silent',
      accessibility: 'restricted',
      connectivity: 'online',
    },
    spatial: {
      layout: 'modular',
      scale: 'vast',
      flexibility: 'fully-flexible',
    },
  },
  abstract: {
    category: 'abstract',
    description: 'Conceptual/abstract space',
    attributes: {
      lighting: 'none',
      noise_level: 'silent',
      accessibility: 'open',
      connectivity: 'offline',
    },
    spatial: {
      layout: 'modular',
      scale: 'vast',
      flexibility: 'fully-flexible',
    },
  },
  workshop: {
    category: 'workshop',
    description: 'Hands-on workshop environment',
    attributes: {
      lighting: 'mixed',
      noise_level: 'moderate',
      accessibility: 'restricted',
      connectivity: 'hybrid',
    },
    spatial: {
      layout: 'modular',
      scale: 'medium',
      flexibility: 'semi-flexible',
    },
  },
  hybrid: {
    category: 'hybrid',
    description: 'Hybrid physical-digital environment',
    attributes: {
      lighting: 'mixed',
      noise_level: 'quiet',
      accessibility: 'restricted',
      connectivity: 'hybrid',
    },
    spatial: {
      layout: 'modular',
      scale: 'medium',
      flexibility: 'semi-flexible',
    },
  },
};

// ============================================================
// UTILITY
// ============================================================

function generateId(): string {
  return `env_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

// ============================================================
// ENVIRONMENT ENGINE
// ============================================================

export const EnvironmentEngine = {
  name: 'EnvironmentEngine',
  version: '1.0.0',
  
  /**
   * List available environment categories
   */
  listCategories(): EnvironmentCategory[] {
    return Object.keys(ENVIRONMENT_TEMPLATES) as EnvironmentCategory[];
  },
  
  /**
   * Build an environment
   */
  buildEnvironment(input: EnvironmentInput): EnvironmentModel {
    const template = ENVIRONMENT_TEMPLATES[input.category] || {};
    
    return {
      id: generateId(),
      name: input.name,
      category: input.category,
      description: input.description || template.description || '',
      attributes: {
        lighting: input.attributes?.lighting || template.attributes?.lighting || 'mixed',
        noise_level: input.attributes?.noise_level || template.attributes?.noise_level || 'moderate',
        accessibility: input.attributes?.accessibility || template.attributes?.accessibility || 'restricted',
        connectivity: input.attributes?.connectivity || template.attributes?.connectivity || 'hybrid',
      },
      spatial: {
        layout: input.spatial?.layout || template.spatial?.layout || 'modular',
        scale: input.spatial?.scale || template.spatial?.scale || 'medium',
        flexibility: input.spatial?.flexibility || template.spatial?.flexibility || 'semi-flexible',
      },
      metadata: {},
    };
  },
  
  /**
   * Get environment map (all categories with descriptions)
   */
  environmentMap(): Record<EnvironmentCategory, string> {
    const map: Record<string, string> = {};
    for (const [key, template] of Object.entries(ENVIRONMENT_TEMPLATES)) {
      map[key] = template.description || '';
    }
    return map as Record<EnvironmentCategory, string>;
  },
  
  /**
   * Get template for category
   */
  getTemplate(category: EnvironmentCategory): Partial<EnvironmentModel> | null {
    return ENVIRONMENT_TEMPLATES[category] || null;
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      categories: this.listCategories(),
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default EnvironmentEngine;

============================================================
SECTION A4 — SUB-MODULE: SceneEngine
============================================================

--- FILE: /che-nu-sdk/core/context/scene.engine.ts

/**
 * CHE·NU Scene Engine
 * ====================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models scene structures with actors, objects, and focal points.
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPES
// ============================================================

export type SceneEnergy = 'low' | 'medium' | 'high' | 'dynamic';
export type SceneTopology = 'linear' | 'radial' | 'clustered' | 'distributed' | 'hierarchical';
export type ActorRole = 'protagonist' | 'supporting' | 'observer' | 'facilitator';
export type ObjectSignificance = 'primary' | 'secondary' | 'background';

export interface SceneActor {
  id: string;
  name: string;
  role: ActorRole;
  description: string;
  position?: string;
}

export interface SceneObject {
  id: string;
  name: string;
  type: string;
  significance: ObjectSignificance;
  description: string;
}

export interface FocalPoint {
  id: string;
  name: string;
  description: string;
  priority: number; // 1-10
}

export interface SceneModel {
  id: string;
  name: string;
  description: string;
  actors: SceneActor[];
  objects: SceneObject[];
  focal_points: FocalPoint[];
  energy: SceneEnergy;
  topology: SceneTopology;
  atmosphere: string;
  metadata: Record<string, any>;
}

export interface SceneInput {
  name: string;
  description?: string;
  actors?: Partial<SceneActor>[];
  objects?: Partial<SceneObject>[];
  focal_points?: Partial<FocalPoint>[];
  energy?: SceneEnergy;
  topology?: SceneTopology;
  atmosphere?: string;
}

export interface SceneSummary {
  id: string;
  name: string;
  actor_count: number;
  object_count: number;
  focal_point_count: number;
  energy: SceneEnergy;
  topology: SceneTopology;
  primary_actors: string[];
  primary_objects: string[];
}

// ============================================================
// UTILITY
// ============================================================

function generateId(prefix: string): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

// ============================================================
// SCENE ENGINE
// ============================================================

export const SceneEngine = {
  name: 'SceneEngine',
  version: '1.0.0',
  
  /**
   * Build a scene
   */
  buildScene(input: SceneInput): SceneModel {
    return {
      id: generateId('scn'),
      name: input.name,
      description: input.description || '',
      actors: (input.actors || []).map((a, i) => ({
        id: generateId('actor'),
        name: a.name || `Actor ${i + 1}`,
        role: a.role || 'supporting',
        description: a.description || '',
        position: a.position,
      })),
      objects: (input.objects || []).map((o, i) => ({
        id: generateId('obj'),
        name: o.name || `Object ${i + 1}`,
        type: o.type || 'generic',
        significance: o.significance || 'secondary',
        description: o.description || '',
      })),
      focal_points: (input.focal_points || []).map((f, i) => ({
        id: generateId('fp'),
        name: f.name || `Focal Point ${i + 1}`,
        description: f.description || '',
        priority: f.priority || 5,
      })),
      energy: input.energy || 'medium',
      topology: input.topology || 'distributed',
      atmosphere: input.atmosphere || 'neutral',
      metadata: {},
    };
  },
  
  /**
   * Get scene summary
   */
  sceneSummary(scene: SceneModel): SceneSummary {
    return {
      id: scene.id,
      name: scene.name,
      actor_count: scene.actors.length,
      object_count: scene.objects.length,
      focal_point_count: scene.focal_points.length,
      energy: scene.energy,
      topology: scene.topology,
      primary_actors: scene.actors
        .filter(a => a.role === 'protagonist')
        .map(a => a.name),
      primary_objects: scene.objects
        .filter(o => o.significance === 'primary')
        .map(o => o.name),
    };
  },
  
  /**
   * Add actor to scene
   */
  addActor(scene: SceneModel, actor: Partial<SceneActor>): SceneModel {
    return {
      ...scene,
      actors: [
        ...scene.actors,
        {
          id: generateId('actor'),
          name: actor.name || 'New Actor',
          role: actor.role || 'supporting',
          description: actor.description || '',
          position: actor.position,
        },
      ],
    };
  },
  
  /**
   * Add object to scene
   */
  addObject(scene: SceneModel, obj: Partial<SceneObject>): SceneModel {
    return {
      ...scene,
      objects: [
        ...scene.objects,
        {
          id: generateId('obj'),
          name: obj.name || 'New Object',
          type: obj.type || 'generic',
          significance: obj.significance || 'secondary',
          description: obj.description || '',
        },
      ],
    };
  },
  
  /**
   * Add focal point to scene
   */
  addFocalPoint(scene: SceneModel, fp: Partial<FocalPoint>): SceneModel {
    return {
      ...scene,
      focal_points: [
        ...scene.focal_points,
        {
          id: generateId('fp'),
          name: fp.name || 'New Focal Point',
          description: fp.description || '',
          priority: fp.priority || 5,
        },
      ],
    };
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      energy_levels: ['low', 'medium', 'high', 'dynamic'],
      topologies: ['linear', 'radial', 'clustered', 'distributed', 'hierarchical'],
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default SceneEngine;

============================================================
SECTION A5 — SUB-MODULE: ConditionEngine
============================================================

--- FILE: /che-nu-sdk/core/context/condition.engine.ts

/**
 * CHE·NU Condition Engine
 * ========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models condition states and factors.
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPES
// ============================================================

export type ConditionState = 'stable' | 'unstable' | 'dynamic' | 'neutral' | 'transitional';
export type FactorImpact = 'positive' | 'negative' | 'neutral';

export interface ConditionFactor {
  id: string;
  name: string;
  value: string;
  impact: FactorImpact;
  weight: number; // 0-1
}

export interface ConditionModel {
  id: string;
  name: string;
  state: ConditionState;
  description: string;
  factors: ConditionFactor[];
  overall_sentiment: 'favorable' | 'unfavorable' | 'neutral';
  metadata: Record<string, any>;
}

export interface ConditionInput {
  name: string;
  state?: ConditionState;
  description?: string;
  factors?: Partial<ConditionFactor>[];
}

export interface ConditionEvaluation {
  condition_id: string;
  state: ConditionState;
  factor_count: number;
  positive_factors: number;
  negative_factors: number;
  neutral_factors: number;
  overall_sentiment: 'favorable' | 'unfavorable' | 'neutral';
}

// ============================================================
// UTILITY
// ============================================================

function generateId(prefix: string): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

// ============================================================
// CONDITION ENGINE
// ============================================================

export const ConditionEngine = {
  name: 'ConditionEngine',
  version: '1.0.0',
  
  /**
   * List available condition states
   */
  listStates(): ConditionState[] {
    return ['stable', 'unstable', 'dynamic', 'neutral', 'transitional'];
  },
  
  /**
   * Build a condition
   */
  buildCondition(input: ConditionInput): ConditionModel {
    const factors: ConditionFactor[] = (input.factors || []).map((f, i) => ({
      id: generateId('factor'),
      name: f.name || `Factor ${i + 1}`,
      value: f.value || '',
      impact: f.impact || 'neutral',
      weight: f.weight || 0.5,
    }));
    
    // Calculate overall sentiment
    const positive = factors.filter(f => f.impact === 'positive').length;
    const negative = factors.filter(f => f.impact === 'negative').length;
    let sentiment: 'favorable' | 'unfavorable' | 'neutral' = 'neutral';
    if (positive > negative) sentiment = 'favorable';
    else if (negative > positive) sentiment = 'unfavorable';
    
    return {
      id: generateId('cond'),
      name: input.name,
      state: input.state || 'neutral',
      description: input.description || '',
      factors,
      overall_sentiment: sentiment,
      metadata: {},
    };
  },
  
  /**
   * Evaluate conditions (representational analysis)
   */
  evaluateConditions(conditions: ConditionModel[]): ConditionEvaluation[] {
    return conditions.map(c => ({
      condition_id: c.id,
      state: c.state,
      factor_count: c.factors.length,
      positive_factors: c.factors.filter(f => f.impact === 'positive').length,
      negative_factors: c.factors.filter(f => f.impact === 'negative').length,
      neutral_factors: c.factors.filter(f => f.impact === 'neutral').length,
      overall_sentiment: c.overall_sentiment,
    }));
  },
  
  /**
   * Add factor to condition
   */
  addFactor(condition: ConditionModel, factor: Partial<ConditionFactor>): ConditionModel {
    const newFactors = [
      ...condition.factors,
      {
        id: generateId('factor'),
        name: factor.name || 'New Factor',
        value: factor.value || '',
        impact: factor.impact || 'neutral',
        weight: factor.weight || 0.5,
      },
    ];
    
    // Recalculate sentiment
    const positive = newFactors.filter(f => f.impact === 'positive').length;
    const negative = newFactors.filter(f => f.impact === 'negative').length;
    let sentiment: 'favorable' | 'unfavorable' | 'neutral' = 'neutral';
    if (positive > negative) sentiment = 'favorable';
    else if (negative > positive) sentiment = 'unfavorable';
    
    return {
      ...condition,
      factors: newFactors,
      overall_sentiment: sentiment,
    };
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      states: this.listStates(),
      impacts: ['positive', 'negative', 'neutral'],
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default ConditionEngine;

============================================================
SECTION A6 — SUB-MODULE: ConstraintEngine
============================================================

--- FILE: /che-nu-sdk/core/context/constraint.engine.ts

/**
 * CHE·NU Constraint Engine
 * =========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models constraints and their impacts.
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPES
// ============================================================

export type ConstraintType = 
  | 'time'
  | 'resources'
  | 'complexity'
  | 'clarity'
  | 'scope'
  | 'dependency'
  | 'technical'
  | 'organizational';

export type ConstraintSeverity = 'low' | 'medium' | 'high' | 'critical';

export interface ConstraintModel {
  id: string;
  name: string;
  type: ConstraintType;
  severity: ConstraintSeverity;
  description: string;
  impact_areas: string[];
  mitigation_notes: string;
  metadata: Record<string, any>;
}

export interface ConstraintInput {
  name: string;
  type: ConstraintType;
  severity?: ConstraintSeverity;
  description?: string;
  impact_areas?: string[];
  mitigation_notes?: string;
}

export interface ConstraintImpactAnalysis {
  constraint_id: string;
  type: ConstraintType;
  severity: ConstraintSeverity;
  impact_score: number; // 1-10
  affected_areas: string[];
  blocking: boolean;
}

// ============================================================
// CONSTRAINT TEMPLATES
// ============================================================

const CONSTRAINT_TEMPLATES: Record<ConstraintType, Partial<ConstraintModel>> = {
  time: {
    type: 'time',
    description: 'Time-related constraint',
    impact_areas: ['schedule', 'delivery', 'planning'],
  },
  resources: {
    type: 'resources',
    description: 'Resource availability constraint',
    impact_areas: ['budget', 'personnel', 'tools'],
  },
  complexity: {
    type: 'complexity',
    description: 'Complexity-related constraint',
    impact_areas: ['design', 'implementation', 'testing'],
  },
  clarity: {
    type: 'clarity',
    description: 'Requirements clarity constraint',
    impact_areas: ['scope', 'design', 'communication'],
  },
  scope: {
    type: 'scope',
    description: 'Scope boundary constraint',
    impact_areas: ['features', 'timeline', 'resources'],
  },
  dependency: {
    type: 'dependency',
    description: 'External dependency constraint',
    impact_areas: ['schedule', 'integration', 'risk'],
  },
  technical: {
    type: 'technical',
    description: 'Technical limitation constraint',
    impact_areas: ['architecture', 'performance', 'scalability'],
  },
  organizational: {
    type: 'organizational',
    description: 'Organizational constraint',
    impact_areas: ['process', 'approval', 'communication'],
  },
};

// ============================================================
// UTILITY
// ============================================================

function generateId(): string {
  return `const_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 8)}`;
}

// ============================================================
// CONSTRAINT ENGINE
// ============================================================

export const ConstraintEngine = {
  name: 'ConstraintEngine',
  version: '1.0.0',
  
  /**
   * List available constraint types
   */
  listTypes(): ConstraintType[] {
    return Object.keys(CONSTRAINT_TEMPLATES) as ConstraintType[];
  },
  
  /**
   * Build a constraint
   */
  buildConstraints(input: ConstraintInput): ConstraintModel {
    const template = CONSTRAINT_TEMPLATES[input.type] || {};
    
    return {
      id: generateId(),
      name: input.name,
      type: input.type,
      severity: input.severity || 'medium',
      description: input.description || template.description || '',
      impact_areas: input.impact_areas || template.impact_areas || [],
      mitigation_notes: input.mitigation_notes || '',
      metadata: {},
    };
  },
  
  /**
   * Analyze constraint impact (representational)
   */
  constraintImpact(constraints: ConstraintModel[]): ConstraintImpactAnalysis[] {
    const severityScores: Record<ConstraintSeverity, number> = {
      low: 2,
      medium: 5,
      high: 8,
      critical: 10,
    };
    
    return constraints.map(c => ({
      constraint_id: c.id,
      type: c.type,
      severity: c.severity,
      impact_score: severityScores[c.severity],
      affected_areas: c.impact_areas,
      blocking: c.severity === 'critical',
    }));
  },
  
  /**
   * Get template for constraint type
   */
  getTemplate(type: ConstraintType): Partial<ConstraintModel> | null {
    return CONSTRAINT_TEMPLATES[type] || null;
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      types: this.listTypes(),
      severities: ['low', 'medium', 'high', 'critical'],
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default ConstraintEngine;

============================================================
END OF CONTEXT LAYER CORE
============================================================
