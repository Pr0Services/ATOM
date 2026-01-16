############################################################
#                                                          #
#       CHE·NU TEMPLATE FACTORY LAYER                      #
#       CORE ENGINE + ALL SUB-GENERATORS                   #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION B1 — CORE MODULE: TemplateFactoryEngine
============================================================

--- FILE: /che-nu-sdk/core/template_factory.ts

/**
 * CHE·NU Template Factory Engine
 * ===============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Universal template generator for CHE·NU structures.
 * Generates representational templates for projects, missions,
 * processes, personas, objects, simulations, and XR scenes.
 * 
 * SAFE COMPLIANCE:
 * - No real plan templates
 * - No actionable strategies
 * - Structural representations only
 * - No execution capability
 * 
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export type TemplateType = 
  | 'project'
  | 'mission'
  | 'process'
  | 'persona'
  | 'object'
  | 'simulation'
  | 'xr-scene';

/**
 * Base template model
 */
export interface TemplateModel {
  id: string;
  name: string;
  type: TemplateType;
  description: string;
  structure: TemplateStructure;
  recommended_engines: string[];
  compatible_spheres: string[];
  metadata: {
    created_at: string;
    updated_at: string;
    generator_version: string;
    category?: string;
    tags?: string[];
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
    noRealPlans: true;
  };
}

/**
 * Template structure (varies by type)
 */
export interface TemplateStructure {
  sections: TemplateSection[];
  fields: TemplateField[];
  relationships: TemplateRelationship[];
  placeholders: string[];
}

export interface TemplateSection {
  id: string;
  name: string;
  description: string;
  order: number;
  required: boolean;
}

export interface TemplateField {
  id: string;
  name: string;
  type: 'text' | 'number' | 'date' | 'list' | 'reference' | 'enum';
  section_id: string;
  required: boolean;
  default_value?: any;
  placeholder?: string;
}

export interface TemplateRelationship {
  id: string;
  source_section: string;
  target_section: string;
  relationship_type: 'parent' | 'child' | 'sibling' | 'reference';
}

/**
 * Template generation input
 */
export interface TemplateInput {
  type: TemplateType;
  name?: string;
  category?: string;
  customizations?: Record<string, any>;
}

/**
 * Template listing
 */
export interface TemplateInfo {
  id: string;
  name: string;
  type: TemplateType;
  description: string;
  category: string;
  engine_count: number;
  sphere_count: number;
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
// TEMPLATE FACTORY ENGINE
// ============================================================

export const TemplateFactoryEngine = {
  name: 'TemplateFactoryEngine',
  version: '1.0.0',
  
  /**
   * Generate a template based on type
   */
  generateTemplate(input: TemplateInput): TemplateModel {
    const now = timestamp();
    const templateId = generateId('tpl');
    
    // Get type-specific structure
    const structure = this._getStructureForType(input.type, input.customizations);
    const engines = this._getEnginesForType(input.type);
    const spheres = this._getSpheresForType(input.type);
    
    return {
      id: templateId,
      name: input.name || `${input.type.charAt(0).toUpperCase() + input.type.slice(1)} Template`,
      type: input.type,
      description: `Representational template for ${input.type}`,
      structure,
      recommended_engines: engines,
      compatible_spheres: spheres,
      metadata: {
        created_at: now,
        updated_at: now,
        generator_version: this.version,
        category: input.category,
        tags: [],
      },
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
        noRealPlans: true,
      },
    };
  },
  
  /**
   * List available template types
   */
  listAvailableTemplates(): TemplateInfo[] {
    const types: TemplateType[] = ['project', 'mission', 'process', 'persona', 'object', 'simulation', 'xr-scene'];
    
    return types.map(type => ({
      id: `tpl_type_${type}`,
      name: `${type.charAt(0).toUpperCase() + type.slice(1)} Template`,
      type,
      description: this._getDescriptionForType(type),
      category: this._getCategoryForType(type),
      engine_count: this._getEnginesForType(type).length,
      sphere_count: this._getSpheresForType(type).length,
    }));
  },
  
  /**
   * Apply template to target (representational mapping)
   */
  applyTemplate(template: TemplateModel, targetId: string): {
    template_id: string;
    target_id: string;
    applied_sections: string[];
    applied_fields: string[];
  } {
    return {
      template_id: template.id,
      target_id: targetId,
      applied_sections: template.structure.sections.map(s => s.id),
      applied_fields: template.structure.fields.map(f => f.id),
    };
  },
  
  /**
   * Get structure for type (internal)
   */
  _getStructureForType(type: TemplateType, customizations?: Record<string, any>): TemplateStructure {
    const structures: Record<TemplateType, TemplateStructure> = {
      project: {
        sections: [
          { id: 'overview', name: 'Overview', description: 'Project overview', order: 1, required: true },
          { id: 'objectives', name: 'Objectives', description: 'Project objectives', order: 2, required: true },
          { id: 'scope', name: 'Scope', description: 'Project scope', order: 3, required: true },
          { id: 'timeline', name: 'Timeline', description: 'Project timeline', order: 4, required: false },
          { id: 'resources', name: 'Resources', description: 'Required resources', order: 5, required: false },
        ],
        fields: [
          { id: 'name', name: 'Project Name', type: 'text', section_id: 'overview', required: true },
          { id: 'description', name: 'Description', type: 'text', section_id: 'overview', required: true },
          { id: 'start_date', name: 'Start Date', type: 'date', section_id: 'timeline', required: false },
          { id: 'end_date', name: 'End Date', type: 'date', section_id: 'timeline', required: false },
        ],
        relationships: [
          { id: 'rel_1', source_section: 'objectives', target_section: 'scope', relationship_type: 'parent' },
        ],
        placeholders: ['[PROJECT_NAME]', '[START_DATE]', '[END_DATE]', '[TEAM_SIZE]'],
      },
      mission: {
        sections: [
          { id: 'brief', name: 'Mission Brief', description: 'Mission overview', order: 1, required: true },
          { id: 'objectives', name: 'Objectives', description: 'Mission objectives', order: 2, required: true },
          { id: 'criteria', name: 'Success Criteria', description: 'Success metrics', order: 3, required: true },
          { id: 'constraints', name: 'Constraints', description: 'Mission constraints', order: 4, required: false },
        ],
        fields: [
          { id: 'name', name: 'Mission Name', type: 'text', section_id: 'brief', required: true },
          { id: 'type', name: 'Mission Type', type: 'enum', section_id: 'brief', required: true },
          { id: 'priority', name: 'Priority', type: 'enum', section_id: 'brief', required: false },
        ],
        relationships: [],
        placeholders: ['[MISSION_NAME]', '[MISSION_TYPE]', '[PRIORITY]'],
      },
      process: {
        sections: [
          { id: 'definition', name: 'Process Definition', description: 'Process overview', order: 1, required: true },
          { id: 'steps', name: 'Process Steps', description: 'Ordered steps', order: 2, required: true },
          { id: 'inputs', name: 'Inputs', description: 'Process inputs', order: 3, required: false },
          { id: 'outputs', name: 'Outputs', description: 'Process outputs', order: 4, required: false },
        ],
        fields: [
          { id: 'name', name: 'Process Name', type: 'text', section_id: 'definition', required: true },
          { id: 'type', name: 'Process Type', type: 'enum', section_id: 'definition', required: true },
        ],
        relationships: [
          { id: 'rel_1', source_section: 'inputs', target_section: 'steps', relationship_type: 'parent' },
          { id: 'rel_2', source_section: 'steps', target_section: 'outputs', relationship_type: 'parent' },
        ],
        placeholders: ['[PROCESS_NAME]', '[STEP_COUNT]'],
      },
      persona: {
        sections: [
          { id: 'identity', name: 'Identity', description: 'Persona identity', order: 1, required: true },
          { id: 'traits', name: 'Traits', description: 'Persona traits', order: 2, required: false },
          { id: 'styles', name: 'Styles', description: 'Work styles', order: 3, required: false },
          { id: 'affinities', name: 'Affinities', description: 'Domain/engine affinities', order: 4, required: false },
        ],
        fields: [
          { id: 'name', name: 'Persona Name', type: 'text', section_id: 'identity', required: true },
          { id: 'category', name: 'Category', type: 'enum', section_id: 'identity', required: true },
        ],
        relationships: [],
        placeholders: ['[PERSONA_NAME]', '[CATEGORY]'],
      },
      object: {
        sections: [
          { id: 'definition', name: 'Object Definition', description: 'Object overview', order: 1, required: true },
          { id: 'properties', name: 'Properties', description: 'Object properties', order: 2, required: false },
          { id: 'relationships', name: 'Relationships', description: 'Object relationships', order: 3, required: false },
        ],
        fields: [
          { id: 'name', name: 'Object Name', type: 'text', section_id: 'definition', required: true },
          { id: 'type', name: 'Object Type', type: 'enum', section_id: 'definition', required: true },
        ],
        relationships: [],
        placeholders: ['[OBJECT_NAME]', '[OBJECT_TYPE]'],
      },
      simulation: {
        sections: [
          { id: 'setup', name: 'Simulation Setup', description: 'Initial configuration', order: 1, required: true },
          { id: 'subject', name: 'Subject', description: 'Simulation subject', order: 2, required: true },
          { id: 'parameters', name: 'Parameters', description: 'Simulation parameters', order: 3, required: false },
          { id: 'timeline', name: 'Timeline', description: 'Simulation timeline', order: 4, required: false },
        ],
        fields: [
          { id: 'name', name: 'Simulation Name', type: 'text', section_id: 'setup', required: true },
          { id: 'type', name: 'Simulation Type', type: 'enum', section_id: 'setup', required: true },
        ],
        relationships: [],
        placeholders: ['[SIMULATION_NAME]', '[FRAME_COUNT]'],
      },
      'xr-scene': {
        sections: [
          { id: 'scene_setup', name: 'Scene Setup', description: 'Scene configuration', order: 1, required: true },
          { id: 'environment', name: 'Environment', description: 'Scene environment', order: 2, required: true },
          { id: 'objects', name: 'Objects', description: 'Scene objects', order: 3, required: false },
          { id: 'interactions', name: 'Interactions', description: 'Scene interactions', order: 4, required: false },
        ],
        fields: [
          { id: 'name', name: 'Scene Name', type: 'text', section_id: 'scene_setup', required: true },
          { id: 'type', name: 'Scene Type', type: 'enum', section_id: 'scene_setup', required: true },
        ],
        relationships: [],
        placeholders: ['[SCENE_NAME]', '[SCENE_TYPE]'],
      },
    };
    
    return structures[type] || structures.project;
  },
  
  /**
   * Get recommended engines for type (internal)
   */
  _getEnginesForType(type: TemplateType): string[] {
    const engines: Record<TemplateType, string[]> = {
      project: ['ProjectEngine', 'MissionEngine', 'ProcessEngine'],
      mission: ['MissionEngine', 'ProcessEngine'],
      process: ['ProcessEngine'],
      persona: ['PersonaEngine'],
      object: ['KnowledgeEngine'],
      simulation: ['SimulationEngine'],
      'xr-scene': ['XREngine'],
    };
    return engines[type] || [];
  },
  
  /**
   * Get compatible spheres for type (internal)
   */
  _getSpheresForType(type: TemplateType): string[] {
    const spheres: Record<TemplateType, string[]> = {
      project: ['project', 'business', 'creative'],
      mission: ['mission', 'project'],
      process: ['process', 'workflow'],
      persona: ['personal', 'team'],
      object: ['knowledge', 'creative'],
      simulation: ['analysis', 'strategy'],
      'xr-scene': ['xr', 'creative', 'immersive'],
    };
    return spheres[type] || [];
  },
  
  /**
   * Get description for type (internal)
   */
  _getDescriptionForType(type: TemplateType): string {
    const descriptions: Record<TemplateType, string> = {
      project: 'Template for project structures',
      mission: 'Template for mission definitions',
      process: 'Template for process workflows',
      persona: 'Template for persona modeling',
      object: 'Template for object definitions',
      simulation: 'Template for simulation setup',
      'xr-scene': 'Template for XR scene creation',
    };
    return descriptions[type] || 'Generic template';
  },
  
  /**
   * Get category for type (internal)
   */
  _getCategoryForType(type: TemplateType): string {
    const categories: Record<TemplateType, string> = {
      project: 'planning',
      mission: 'execution',
      process: 'workflow',
      persona: 'modeling',
      object: 'definition',
      simulation: 'analysis',
      'xr-scene': 'immersive',
    };
    return categories[type] || 'general';
  },
  
  /**
   * Get engine metadata
   */
  meta() {
    return {
      name: this.name,
      version: this.version,
      description: 'Universal template generator for CHE·NU',
      supported_types: ['project', 'mission', 'process', 'persona', 'object', 'simulation', 'xr-scene'],
      safe: {
        isRepresentational: true,
        noAutonomy: true,
        noExecution: true,
        noRealPlans: true,
      },
    };
  },
};

export default TemplateFactoryEngine;

============================================================
SECTION B2 — SUB-MODULE: ProjectTemplateGenerator
============================================================

--- FILE: /che-nu-sdk/core/template_factory/project_template.engine.ts

/**
 * CHE·NU Project Template Generator
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

export type ProjectTemplateType = 
  | 'research'
  | 'xr_production'
  | 'business_initiative'
  | 'personal_development'
  | 'creative_production'
  | 'technical_implementation';

export interface ProjectTemplate {
  id: string;
  name: string;
  type: ProjectTemplateType;
  description: string;
  icon: string;
  sections: string[];
  recommended_phases: string[];
  suggested_engines: string[];
}

const PROJECT_TEMPLATES: Record<ProjectTemplateType, ProjectTemplate> = {
  research: {
    id: 'proj_tpl_research',
    name: 'Research Project',
    type: 'research',
    description: 'Template for research and discovery projects',
    icon: '🔬',
    sections: ['Research Question', 'Methodology', 'Data Collection', 'Analysis', 'Findings'],
    recommended_phases: ['Definition', 'Research', 'Analysis', 'Documentation'],
    suggested_engines: ['KnowledgeEngine', 'SimulationEngine'],
  },
  xr_production: {
    id: 'proj_tpl_xr',
    name: 'XR Production Project',
    type: 'xr_production',
    description: 'Template for XR/immersive content production',
    icon: '🥽',
    sections: ['Concept', 'Design', 'Asset Creation', 'Integration', 'Testing'],
    recommended_phases: ['Concept', 'Pre-production', 'Production', 'Post-production'],
    suggested_engines: ['XREngine', 'TemplateFactoryEngine'],
  },
  business_initiative: {
    id: 'proj_tpl_business',
    name: 'Business Initiative Project',
    type: 'business_initiative',
    description: 'Template for business-focused projects',
    icon: '💼',
    sections: ['Executive Summary', 'Objectives', 'Strategy', 'Resources', 'Metrics'],
    recommended_phases: ['Planning', 'Execution', 'Monitoring', 'Closure'],
    suggested_engines: ['ProjectEngine', 'MissionEngine'],
  },
  personal_development: {
    id: 'proj_tpl_personal',
    name: 'Personal Development Project',
    type: 'personal_development',
    description: 'Template for personal growth projects',
    icon: '🌱',
    sections: ['Goals', 'Current State', 'Action Plan', 'Milestones', 'Reflection'],
    recommended_phases: ['Assessment', 'Planning', 'Action', 'Review'],
    suggested_engines: ['PersonaEngine'],
  },
  creative_production: {
    id: 'proj_tpl_creative',
    name: 'Creative Production Project',
    type: 'creative_production',
    description: 'Template for creative content production',
    icon: '🎨',
    sections: ['Concept', 'Inspiration', 'Creation', 'Iteration', 'Delivery'],
    recommended_phases: ['Ideation', 'Creation', 'Refinement', 'Delivery'],
    suggested_engines: ['TemplateFactoryEngine', 'XREngine'],
  },
  technical_implementation: {
    id: 'proj_tpl_technical',
    name: 'Technical Implementation Project',
    type: 'technical_implementation',
    description: 'Template for technical/development projects',
    icon: '⚙️',
    sections: ['Requirements', 'Architecture', 'Implementation', 'Testing', 'Deployment'],
    recommended_phases: ['Design', 'Development', 'Testing', 'Release'],
    suggested_engines: ['ProcessEngine', 'KnowledgeEngine'],
  },
};

export const ProjectTemplateGenerator = {
  name: 'ProjectTemplateGenerator',
  version: '1.0.0',
  
  listTemplates(): ProjectTemplate[] {
    return Object.values(PROJECT_TEMPLATES);
  },
  
  getTemplate(type: ProjectTemplateType): ProjectTemplate | null {
    return PROJECT_TEMPLATES[type] || null;
  },
  
  generateProjectStructure(type: ProjectTemplateType, name: string): {
    id: string;
    name: string;
    template_type: ProjectTemplateType;
    sections: Array<{ id: string; name: string; content: string }>;
  } {
    const template = PROJECT_TEMPLATES[type];
    if (!template) throw new Error(`Unknown project template type: ${type}`);
    
    return {
      id: `proj_${Date.now().toString(36)}`,
      name,
      template_type: type,
      sections: template.sections.map((section, i) => ({
        id: `section_${i + 1}`,
        name: section,
        content: `[${section} placeholder]`,
      })),
    };
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      template_count: Object.keys(PROJECT_TEMPLATES).length,
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default ProjectTemplateGenerator;

============================================================
SECTION B3 — SUB-MODULE: MissionTemplateGenerator
============================================================

--- FILE: /che-nu-sdk/core/template_factory/mission_template.engine.ts

/**
 * CHE·NU Mission Template Generator
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

export type MissionTemplateType = 
  | 'investigation'
  | 'creation'
  | 'optimization'
  | 'exploration'
  | 'transformation'
  | 'integration';

export interface MissionTemplate {
  id: string;
  name: string;
  type: MissionTemplateType;
  description: string;
  icon: string;
  objectives_structure: string[];
  success_criteria_types: string[];
  suggested_engines: string[];
}

const MISSION_TEMPLATES: Record<MissionTemplateType, MissionTemplate> = {
  investigation: {
    id: 'msn_tpl_investigation',
    name: 'Investigation Mission',
    type: 'investigation',
    description: 'Template for investigative/research missions',
    icon: '🔍',
    objectives_structure: ['Define Scope', 'Gather Evidence', 'Analyze Findings', 'Report Conclusions'],
    success_criteria_types: ['Completeness', 'Accuracy', 'Timeliness'],
    suggested_engines: ['KnowledgeEngine', 'SimulationEngine'],
  },
  creation: {
    id: 'msn_tpl_creation',
    name: 'Creation Mission',
    type: 'creation',
    description: 'Template for creative/production missions',
    icon: '🎨',
    objectives_structure: ['Conceptualize', 'Design', 'Build', 'Deliver'],
    success_criteria_types: ['Quality', 'Originality', 'Completion'],
    suggested_engines: ['TemplateFactoryEngine', 'XREngine'],
  },
  optimization: {
    id: 'msn_tpl_optimization',
    name: 'Optimization Mission',
    type: 'optimization',
    description: 'Template for improvement/optimization missions',
    icon: '📈',
    objectives_structure: ['Baseline', 'Identify Opportunities', 'Implement Changes', 'Measure Results'],
    success_criteria_types: ['Improvement %', 'Efficiency', 'Sustainability'],
    suggested_engines: ['SimulationEngine', 'ProcessEngine'],
  },
  exploration: {
    id: 'msn_tpl_exploration',
    name: 'Exploration Mission',
    type: 'exploration',
    description: 'Template for discovery/exploration missions',
    icon: '🧭',
    objectives_structure: ['Define Territory', 'Explore', 'Document', 'Map'],
    success_criteria_types: ['Coverage', 'Discoveries', 'Documentation'],
    suggested_engines: ['KnowledgeEngine', 'XREngine'],
  },
  transformation: {
    id: 'msn_tpl_transformation',
    name: 'Transformation Mission',
    type: 'transformation',
    description: 'Template for change/transformation missions',
    icon: '🔄',
    objectives_structure: ['Current State', 'Vision', 'Transition Plan', 'Execute'],
    success_criteria_types: ['Adoption', 'Impact', 'Sustainability'],
    suggested_engines: ['ProcessEngine', 'SimulationEngine'],
  },
  integration: {
    id: 'msn_tpl_integration',
    name: 'Integration Mission',
    type: 'integration',
    description: 'Template for integration/connection missions',
    icon: '🔗',
    objectives_structure: ['Identify Components', 'Design Interfaces', 'Connect', 'Validate'],
    success_criteria_types: ['Connectivity', 'Stability', 'Performance'],
    suggested_engines: ['ProcessEngine', 'KnowledgeEngine'],
  },
};

export const MissionTemplateGenerator = {
  name: 'MissionTemplateGenerator',
  version: '1.0.0',
  
  listTemplates(): MissionTemplate[] {
    return Object.values(MISSION_TEMPLATES);
  },
  
  getTemplate(type: MissionTemplateType): MissionTemplate | null {
    return MISSION_TEMPLATES[type] || null;
  },
  
  generateMissionStructure(type: MissionTemplateType, name: string): {
    id: string;
    name: string;
    template_type: MissionTemplateType;
    objectives: Array<{ id: string; name: string; status: string }>;
    success_criteria: Array<{ id: string; type: string; target: string }>;
  } {
    const template = MISSION_TEMPLATES[type];
    if (!template) throw new Error(`Unknown mission template type: ${type}`);
    
    return {
      id: `msn_${Date.now().toString(36)}`,
      name,
      template_type: type,
      objectives: template.objectives_structure.map((obj, i) => ({
        id: `obj_${i + 1}`,
        name: obj,
        status: 'pending',
      })),
      success_criteria: template.success_criteria_types.map((crit, i) => ({
        id: `crit_${i + 1}`,
        type: crit,
        target: '[Define target]',
      })),
    };
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      template_count: Object.keys(MISSION_TEMPLATES).length,
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default MissionTemplateGenerator;

============================================================
SECTION B4 — SUB-MODULE: ProcessTemplateGenerator
============================================================

--- FILE: /che-nu-sdk/core/template_factory/process_template.engine.ts

/**
 * CHE·NU Process Template Generator
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

export type ProcessTemplateType = 
  | 'linear'
  | 'iterative_cycle'
  | 'double_diamond'
  | 'branching'
  | 'parallel'
  | 'staged';

export interface ProcessTemplate {
  id: string;
  name: string;
  type: ProcessTemplateType;
  description: string;
  icon: string;
  step_structure: Array<{ name: string; type: string }>;
  flow_type: 'sequential' | 'cyclical' | 'divergent' | 'convergent' | 'parallel';
  suggested_engines: string[];
}

const PROCESS_TEMPLATES: Record<ProcessTemplateType, ProcessTemplate> = {
  linear: {
    id: 'proc_tpl_linear',
    name: 'Linear Process',
    type: 'linear',
    description: 'Simple sequential process flow',
    icon: '➡️',
    step_structure: [
      { name: 'Start', type: 'entry' },
      { name: 'Step 1', type: 'action' },
      { name: 'Step 2', type: 'action' },
      { name: 'Step 3', type: 'action' },
      { name: 'End', type: 'exit' },
    ],
    flow_type: 'sequential',
    suggested_engines: ['ProcessEngine'],
  },
  iterative_cycle: {
    id: 'proc_tpl_iterative',
    name: 'Iterative Cycle',
    type: 'iterative_cycle',
    description: 'Cyclical iterative process',
    icon: '🔄',
    step_structure: [
      { name: 'Plan', type: 'action' },
      { name: 'Do', type: 'action' },
      { name: 'Check', type: 'evaluation' },
      { name: 'Act', type: 'action' },
    ],
    flow_type: 'cyclical',
    suggested_engines: ['ProcessEngine', 'SimulationEngine'],
  },
  double_diamond: {
    id: 'proc_tpl_double_diamond',
    name: 'Double Diamond',
    type: 'double_diamond',
    description: 'Diverge-converge design thinking process',
    icon: '💎',
    step_structure: [
      { name: 'Discover', type: 'divergent' },
      { name: 'Define', type: 'convergent' },
      { name: 'Develop', type: 'divergent' },
      { name: 'Deliver', type: 'convergent' },
    ],
    flow_type: 'divergent',
    suggested_engines: ['ProcessEngine', 'TemplateFactoryEngine'],
  },
  branching: {
    id: 'proc_tpl_branching',
    name: 'Branching Process',
    type: 'branching',
    description: 'Decision-based branching process',
    icon: '🌿',
    step_structure: [
      { name: 'Entry', type: 'entry' },
      { name: 'Decision Point', type: 'decision' },
      { name: 'Branch A', type: 'branch' },
      { name: 'Branch B', type: 'branch' },
      { name: 'Merge', type: 'merge' },
    ],
    flow_type: 'divergent',
    suggested_engines: ['ProcessEngine', 'SimulationEngine'],
  },
  parallel: {
    id: 'proc_tpl_parallel',
    name: 'Parallel Process',
    type: 'parallel',
    description: 'Concurrent parallel execution',
    icon: '⚡',
    step_structure: [
      { name: 'Start', type: 'entry' },
      { name: 'Fork', type: 'fork' },
      { name: 'Track A', type: 'parallel' },
      { name: 'Track B', type: 'parallel' },
      { name: 'Join', type: 'join' },
      { name: 'End', type: 'exit' },
    ],
    flow_type: 'parallel',
    suggested_engines: ['ProcessEngine'],
  },
  staged: {
    id: 'proc_tpl_staged',
    name: 'Staged Process',
    type: 'staged',
    description: 'Gate-based staged process',
    icon: '🚦',
    step_structure: [
      { name: 'Stage 1', type: 'stage' },
      { name: 'Gate 1', type: 'gate' },
      { name: 'Stage 2', type: 'stage' },
      { name: 'Gate 2', type: 'gate' },
      { name: 'Stage 3', type: 'stage' },
    ],
    flow_type: 'sequential',
    suggested_engines: ['ProcessEngine', 'MissionEngine'],
  },
};

export const ProcessTemplateGenerator = {
  name: 'ProcessTemplateGenerator',
  version: '1.0.0',
  
  listTemplates(): ProcessTemplate[] {
    return Object.values(PROCESS_TEMPLATES);
  },
  
  getTemplate(type: ProcessTemplateType): ProcessTemplate | null {
    return PROCESS_TEMPLATES[type] || null;
  },
  
  generateProcessStructure(type: ProcessTemplateType, name: string): {
    id: string;
    name: string;
    template_type: ProcessTemplateType;
    flow_type: string;
    steps: Array<{ id: string; name: string; type: string; order: number }>;
  } {
    const template = PROCESS_TEMPLATES[type];
    if (!template) throw new Error(`Unknown process template type: ${type}`);
    
    return {
      id: `proc_${Date.now().toString(36)}`,
      name,
      template_type: type,
      flow_type: template.flow_type,
      steps: template.step_structure.map((step, i) => ({
        id: `step_${i + 1}`,
        name: step.name,
        type: step.type,
        order: i + 1,
      })),
    };
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      template_count: Object.keys(PROCESS_TEMPLATES).length,
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default ProcessTemplateGenerator;

============================================================
SECTION B5 — SUB-MODULE: XRSceneTemplateGenerator
============================================================

--- FILE: /che-nu-sdk/core/template_factory/xr_scene_template.engine.ts

/**
 * CHE·NU XR Scene Template Generator
 * ====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * @version 1.0.0
 */

export type XRSceneTemplateType = 
  | 'studio'
  | 'research_lab'
  | 'landscape'
  | 'abstract_conceptual'
  | 'gallery'
  | 'workshop_space';

export interface XRSceneTemplate {
  id: string;
  name: string;
  type: XRSceneTemplateType;
  description: string;
  icon: string;
  default_environment: {
    lighting: string;
    atmosphere: string;
    scale: string;
  };
  suggested_objects: string[];
  interaction_types: string[];
}

const XR_SCENE_TEMPLATES: Record<XRSceneTemplateType, XRSceneTemplate> = {
  studio: {
    id: 'xr_tpl_studio',
    name: 'Studio Scene',
    type: 'studio',
    description: 'Creative studio environment',
    icon: '🎨',
    default_environment: {
      lighting: 'soft_ambient',
      atmosphere: 'creative',
      scale: 'room',
    },
    suggested_objects: ['Canvas', 'Tools', 'Display', 'Workspace'],
    interaction_types: ['grab', 'draw', 'manipulate'],
  },
  research_lab: {
    id: 'xr_tpl_research_lab',
    name: 'Research Lab Scene',
    type: 'research_lab',
    description: 'Research and analysis environment',
    icon: '🔬',
    default_environment: {
      lighting: 'clinical',
      atmosphere: 'analytical',
      scale: 'room',
    },
    suggested_objects: ['Data Displays', 'Analysis Tools', 'Documentation'],
    interaction_types: ['inspect', 'analyze', 'annotate'],
  },
  landscape: {
    id: 'xr_tpl_landscape',
    name: 'Landscape Scene',
    type: 'landscape',
    description: 'Open landscape environment',
    icon: '🏞️',
    default_environment: {
      lighting: 'natural_daylight',
      atmosphere: 'open',
      scale: 'vast',
    },
    suggested_objects: ['Terrain', 'Vegetation', 'Sky', 'Landmarks'],
    interaction_types: ['navigate', 'explore', 'observe'],
  },
  abstract_conceptual: {
    id: 'xr_tpl_abstract',
    name: 'Abstract Conceptual Scene',
    type: 'abstract_conceptual',
    description: 'Abstract conceptual space',
    icon: '🔮',
    default_environment: {
      lighting: 'ethereal',
      atmosphere: 'conceptual',
      scale: 'infinite',
    },
    suggested_objects: ['Nodes', 'Connections', 'Symbols', 'Flows'],
    interaction_types: ['connect', 'transform', 'navigate'],
  },
  gallery: {
    id: 'xr_tpl_gallery',
    name: 'Gallery Scene',
    type: 'gallery',
    description: 'Exhibition gallery space',
    icon: '🖼️',
    default_environment: {
      lighting: 'spotlight',
      atmosphere: 'exhibition',
      scale: 'large_room',
    },
    suggested_objects: ['Displays', 'Artworks', 'Information Panels'],
    interaction_types: ['view', 'inspect', 'navigate'],
  },
  workshop_space: {
    id: 'xr_tpl_workshop',
    name: 'Workshop Space Scene',
    type: 'workshop_space',
    description: 'Hands-on workshop environment',
    icon: '🛠️',
    default_environment: {
      lighting: 'work_lighting',
      atmosphere: 'practical',
      scale: 'room',
    },
    suggested_objects: ['Workbenches', 'Tools', 'Materials', 'Instructions'],
    interaction_types: ['grab', 'use', 'assemble'],
  },
};

export const XRSceneTemplateGenerator = {
  name: 'XRSceneTemplateGenerator',
  version: '1.0.0',
  
  listTemplates(): XRSceneTemplate[] {
    return Object.values(XR_SCENE_TEMPLATES);
  },
  
  getTemplate(type: XRSceneTemplateType): XRSceneTemplate | null {
    return XR_SCENE_TEMPLATES[type] || null;
  },
  
  generateSceneStructure(type: XRSceneTemplateType, name: string): {
    id: string;
    name: string;
    template_type: XRSceneTemplateType;
    environment: object;
    objects: Array<{ id: string; name: string; type: string }>;
    interactions: string[];
  } {
    const template = XR_SCENE_TEMPLATES[type];
    if (!template) throw new Error(`Unknown XR scene template type: ${type}`);
    
    return {
      id: `xr_${Date.now().toString(36)}`,
      name,
      template_type: type,
      environment: template.default_environment,
      objects: template.suggested_objects.map((obj, i) => ({
        id: `xr_obj_${i + 1}`,
        name: obj,
        type: 'placeholder',
      })),
      interactions: template.interaction_types,
    };
  },
  
  meta() {
    return {
      name: this.name,
      version: this.version,
      template_count: Object.keys(XR_SCENE_TEMPLATES).length,
      safe: { isRepresentational: true, noAutonomy: true },
    };
  },
};

export default XRSceneTemplateGenerator;

============================================================
SECTION B6 — SUB-MODULE: Additional Generators (Persona, Object, Simulation)
============================================================

--- FILE: /che-nu-sdk/core/template_factory/persona_template.engine.ts

/**
 * CHE·NU Persona Template Generator
 * ==================================
 */

export type PersonaTemplateType = 'explorer' | 'architect' | 'analyst' | 'creative' | 'strategist' | 'maker';

export interface PersonaTemplate {
  id: string;
  name: string;
  type: PersonaTemplateType;
  icon: string;
  default_traits: string[];
  default_styles: string[];
  suggested_engines: string[];
}

const PERSONA_TEMPLATES: Record<PersonaTemplateType, PersonaTemplate> = {
  explorer: { id: 'pers_tpl_explorer', name: 'Explorer Persona', type: 'explorer', icon: '🧭', default_traits: ['Curious', 'Adaptable', 'Open-minded'], default_styles: ['Exploratory', 'Iterative'], suggested_engines: ['KnowledgeEngine'] },
  architect: { id: 'pers_tpl_architect', name: 'Architect Persona', type: 'architect', icon: '🏗️', default_traits: ['Systematic', 'Visionary', 'Detail-oriented'], default_styles: ['Structured', 'Methodical'], suggested_engines: ['ProcessEngine'] },
  analyst: { id: 'pers_tpl_analyst', name: 'Analyst Persona', type: 'analyst', icon: '📊', default_traits: ['Analytical', 'Logical', 'Thorough'], default_styles: ['Data-driven', 'Systematic'], suggested_engines: ['SimulationEngine'] },
  creative: { id: 'pers_tpl_creative', name: 'Creative Persona', type: 'creative', icon: '🎨', default_traits: ['Imaginative', 'Intuitive', 'Expressive'], default_styles: ['Free-form', 'Experimental'], suggested_engines: ['TemplateFactoryEngine'] },
  strategist: { id: 'pers_tpl_strategist', name: 'Strategist Persona', type: 'strategist', icon: '♟️', default_traits: ['Strategic', 'Forward-thinking', 'Decisive'], default_styles: ['Goal-oriented', 'Planned'], suggested_engines: ['MissionEngine'] },
  maker: { id: 'pers_tpl_maker', name: 'Maker Persona', type: 'maker', icon: '🛠️', default_traits: ['Practical', 'Hands-on', 'Results-oriented'], default_styles: ['Action-oriented', 'Iterative'], suggested_engines: ['ProcessEngine'] },
};

export const PersonaTemplateGenerator = {
  name: 'PersonaTemplateGenerator',
  version: '1.0.0',
  listTemplates: () => Object.values(PERSONA_TEMPLATES),
  getTemplate: (type: PersonaTemplateType) => PERSONA_TEMPLATES[type] || null,
  meta() { return { name: this.name, version: this.version, template_count: Object.keys(PERSONA_TEMPLATES).length }; },
};

--- FILE: /che-nu-sdk/core/template_factory/object_template.engine.ts

/**
 * CHE·NU Object Template Generator
 * =================================
 */

export type ObjectTemplateType = 'xr_object' | 'document' | 'abstract_concept' | 'resource_pack' | 'data_entity';

export interface ObjectTemplate {
  id: string;
  name: string;
  type: ObjectTemplateType;
  icon: string;
  properties: string[];
  relationships: string[];
}

const OBJECT_TEMPLATES: Record<ObjectTemplateType, ObjectTemplate> = {
  xr_object: { id: 'obj_tpl_xr', name: 'XR Object', type: 'xr_object', icon: '🥽', properties: ['position', 'scale', 'material', 'interaction'], relationships: ['parent', 'children'] },
  document: { id: 'obj_tpl_doc', name: 'Document', type: 'document', icon: '📄', properties: ['title', 'content', 'author', 'version'], relationships: ['references', 'linked_to'] },
  abstract_concept: { id: 'obj_tpl_concept', name: 'Abstract Concept', type: 'abstract_concept', icon: '💡', properties: ['definition', 'attributes', 'examples'], relationships: ['parent_concept', 'child_concepts', 'related'] },
  resource_pack: { id: 'obj_tpl_resource', name: 'Resource Pack', type: 'resource_pack', icon: '📦', properties: ['contents', 'format', 'size'], relationships: ['contained_in', 'contains'] },
  data_entity: { id: 'obj_tpl_data', name: 'Data Entity', type: 'data_entity', icon: '🗃️', properties: ['schema', 'fields', 'validations'], relationships: ['foreign_keys', 'indexes'] },
};

export const ObjectTemplateGenerator = {
  name: 'ObjectTemplateGenerator',
  version: '1.0.0',
  listTemplates: () => Object.values(OBJECT_TEMPLATES),
  getTemplate: (type: ObjectTemplateType) => OBJECT_TEMPLATES[type] || null,
  meta() { return { name: this.name, version: this.version, template_count: Object.keys(OBJECT_TEMPLATES).length }; },
};

--- FILE: /che-nu-sdk/core/template_factory/simulation_template.engine.ts

/**
 * CHE·NU Simulation Template Generator
 * =====================================
 */

export type SimulationTemplateType = 'linear_replay' | 'branch_replay' | 'layered_replay' | 'what_if' | 'comparative';

export interface SimulationTemplate {
  id: string;
  name: string;
  type: SimulationTemplateType;
  icon: string;
  timeline_type: string;
  branch_support: boolean;
  analysis_types: string[];
}

const SIMULATION_TEMPLATES: Record<SimulationTemplateType, SimulationTemplate> = {
  linear_replay: { id: 'sim_tpl_linear', name: 'Linear Replay', type: 'linear_replay', icon: '▶️', timeline_type: 'linear', branch_support: false, analysis_types: ['sequence', 'timing'] },
  branch_replay: { id: 'sim_tpl_branch', name: 'Branch Replay', type: 'branch_replay', icon: '🌿', timeline_type: 'branching', branch_support: true, analysis_types: ['paths', 'decisions'] },
  layered_replay: { id: 'sim_tpl_layered', name: 'Layered Replay', type: 'layered_replay', icon: '📚', timeline_type: 'layered', branch_support: false, analysis_types: ['depth', 'complexity'] },
  what_if: { id: 'sim_tpl_whatif', name: 'What-If Simulation', type: 'what_if', icon: '❓', timeline_type: 'variation', branch_support: true, analysis_types: ['comparison', 'impact'] },
  comparative: { id: 'sim_tpl_comparative', name: 'Comparative Simulation', type: 'comparative', icon: '⚖️', timeline_type: 'parallel', branch_support: true, analysis_types: ['comparison', 'metrics'] },
};

export const SimulationTemplateGenerator = {
  name: 'SimulationTemplateGenerator',
  version: '1.0.0',
  listTemplates: () => Object.values(SIMULATION_TEMPLATES),
  getTemplate: (type: SimulationTemplateType) => SIMULATION_TEMPLATES[type] || null,
  meta() { return { name: this.name, version: this.version, template_count: Object.keys(SIMULATION_TEMPLATES).length }; },
};

============================================================
END OF TEMPLATE FACTORY LAYER CORE + SUB-GENERATORS
============================================================
