############################################################
#                                                          #
#       CHE·NU PERSONA LAYER                               #
#       PART 1: CORE ENGINE + SUB-ENGINES + TEMPLATES      #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION B1 — MAIN MODULE: PersonaEngine
============================================================

--- FILE: /che-nu-sdk/core/persona.ts

/**
 * CHE·NU SDK — Persona Engine
 * =============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Structural model of user/agent personas:
 * - Characteristics
 * - Work styles
 * - Cognitive/emotional attributes (SAFE, abstract)
 * - Engine affinity
 * - Domain expertise profiles
 * - Representational behavior patterns
 * - Process preferences
 * 
 * NOT real psychology, NOT advice — purely STRUCTURAL.
 * 
 * @module PersonaEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Abstract trait (structural, not psychological)
 */
export interface PersonaTrait {
  id: string;
  name: string;
  category: 'cognitive' | 'behavioral' | 'communicative' | 'organizational';
  description: string;
  intensity: number; // 0-1 representational scale
  metadata: Record<string, unknown>;
}

/**
 * Work style
 */
export interface PersonaStyle {
  id: string;
  name: string;
  type: 'workflow' | 'communication' | 'decision_making' | 'collaboration';
  description: string;
  preferences: string[];
  metadata: Record<string, unknown>;
}

/**
 * Domain affinity
 */
export interface DomainAffinity {
  domain: string;           // CHE·NU sphere or domain
  affinity_level: number;   // 0-1 representational
  expertise_tags: string[];
  notes: string;
}

/**
 * Engine affinity
 */
export interface EngineAffinity {
  engine: string;           // CHE·NU engine name
  affinity_level: number;   // 0-1 representational
  usage_frequency: 'rare' | 'occasional' | 'frequent' | 'primary';
  notes: string;
}

/**
 * Capability influence (abstract)
 */
export interface CapabilityInfluence {
  capability: string;
  influence_type: 'enhances' | 'challenges' | 'neutral';
  strength: number; // 0-1 representational
  description: string;
}

/**
 * Complete persona model
 */
export interface PersonaModel {
  id: string;
  name: string;
  description: string;
  avatar_icon: string;
  category: 'user' | 'work' | 'creative' | 'analytical' | 'collaborative';
  traits: PersonaTrait[];
  styles: PersonaStyle[];
  domain_affinities: DomainAffinity[];
  engine_affinities: EngineAffinity[];
  capability_influences: CapabilityInfluence[];
  process_preferences: {
    preferred_complexity: 'simple' | 'moderate' | 'complex';
    preferred_pace: 'slow' | 'moderate' | 'fast';
    iteration_preference: 'minimal' | 'moderate' | 'extensive';
  };
  metadata: {
    created_at: string;
    updated_at: string;
    template_source?: string;
    version: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noPsychology: true;
    noAdvice: true;
  };
}

/**
 * Persona creation input
 */
export interface CreatePersonaInput {
  name: string;
  description?: string;
  category?: PersonaModel['category'];
  avatar_icon?: string;
}

/**
 * Persona summary
 */
export interface PersonaSummary {
  id: string;
  name: string;
  category: string;
  trait_count: number;
  style_count: number;
  primary_domains: string[];
  primary_engines: string[];
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generatePersonaId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `persona_${timestamp}_${random}`;
}

function generateTraitId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `trait_${timestamp}_${random}`;
}

function generateStyleId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `style_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a new persona
 */
export function createPersona(input: CreatePersonaInput): PersonaModel {
  const timestamp = now();
  
  return {
    id: generatePersonaId(),
    name: input.name,
    description: input.description || '',
    avatar_icon: input.avatar_icon || '👤',
    category: input.category || 'user',
    traits: [],
    styles: [],
    domain_affinities: [],
    engine_affinities: [],
    capability_influences: [],
    process_preferences: {
      preferred_complexity: 'moderate',
      preferred_pace: 'moderate',
      iteration_preference: 'moderate',
    },
    metadata: {
      created_at: timestamp,
      updated_at: timestamp,
      version: '1.0.0',
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPsychology: true,
      noAdvice: true,
    },
  };
}

/**
 * Attach a trait to persona
 */
export function attachTrait(
  persona: PersonaModel,
  trait: Omit<PersonaTrait, 'id'>
): PersonaModel {
  const newTrait: PersonaTrait = {
    ...trait,
    id: generateTraitId(),
  };
  
  persona.traits.push(newTrait);
  persona.metadata.updated_at = now();
  
  return persona;
}

/**
 * Remove a trait from persona
 */
export function removeTrait(persona: PersonaModel, traitId: string): PersonaModel {
  persona.traits = persona.traits.filter(t => t.id !== traitId);
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Attach a style to persona
 */
export function attachStyle(
  persona: PersonaModel,
  style: Omit<PersonaStyle, 'id'>
): PersonaModel {
  const newStyle: PersonaStyle = {
    ...style,
    id: generateStyleId(),
  };
  
  persona.styles.push(newStyle);
  persona.metadata.updated_at = now();
  
  return persona;
}

/**
 * Remove a style from persona
 */
export function removeStyle(persona: PersonaModel, styleId: string): PersonaModel {
  persona.styles = persona.styles.filter(s => s.id !== styleId);
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Assign domain affinity
 */
export function assignDomainAffinity(
  persona: PersonaModel,
  affinity: DomainAffinity
): PersonaModel {
  // Update existing or add new
  const existingIndex = persona.domain_affinities.findIndex(
    a => a.domain === affinity.domain
  );
  
  if (existingIndex >= 0) {
    persona.domain_affinities[existingIndex] = affinity;
  } else {
    persona.domain_affinities.push(affinity);
  }
  
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Remove domain affinity
 */
export function removeDomainAffinity(persona: PersonaModel, domain: string): PersonaModel {
  persona.domain_affinities = persona.domain_affinities.filter(a => a.domain !== domain);
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Assign engine affinity
 */
export function assignEngineAffinity(
  persona: PersonaModel,
  affinity: EngineAffinity
): PersonaModel {
  const existingIndex = persona.engine_affinities.findIndex(
    a => a.engine === affinity.engine
  );
  
  if (existingIndex >= 0) {
    persona.engine_affinities[existingIndex] = affinity;
  } else {
    persona.engine_affinities.push(affinity);
  }
  
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Remove engine affinity
 */
export function removeEngineAffinity(persona: PersonaModel, engine: string): PersonaModel {
  persona.engine_affinities = persona.engine_affinities.filter(a => a.engine !== engine);
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Add capability influence
 */
export function addCapabilityInfluence(
  persona: PersonaModel,
  influence: CapabilityInfluence
): PersonaModel {
  persona.capability_influences.push(influence);
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Update process preferences
 */
export function updateProcessPreferences(
  persona: PersonaModel,
  preferences: Partial<PersonaModel['process_preferences']>
): PersonaModel {
  persona.process_preferences = {
    ...persona.process_preferences,
    ...preferences,
  };
  persona.metadata.updated_at = now();
  return persona;
}

/**
 * Summarize persona
 */
export function summarizePersona(persona: PersonaModel): PersonaSummary {
  const primaryDomains = persona.domain_affinities
    .filter(a => a.affinity_level >= 0.7)
    .map(a => a.domain);
  
  const primaryEngines = persona.engine_affinities
    .filter(a => a.usage_frequency === 'primary' || a.usage_frequency === 'frequent')
    .map(a => a.engine);
  
  return {
    id: persona.id,
    name: persona.name,
    category: persona.category,
    trait_count: persona.traits.length,
    style_count: persona.styles.length,
    primary_domains: primaryDomains,
    primary_engines: primaryEngines,
  };
}

/**
 * Clone persona
 */
export function clonePersona(persona: PersonaModel, newName: string): PersonaModel {
  const cloned = createPersona({
    name: newName,
    description: `Cloned from: ${persona.name}`,
    category: persona.category,
    avatar_icon: persona.avatar_icon,
  });
  
  cloned.traits = persona.traits.map(t => ({ ...t, id: generateTraitId() }));
  cloned.styles = persona.styles.map(s => ({ ...s, id: generateStyleId() }));
  cloned.domain_affinities = [...persona.domain_affinities];
  cloned.engine_affinities = [...persona.engine_affinities];
  cloned.capability_influences = [...persona.capability_influences];
  cloned.process_preferences = { ...persona.process_preferences };
  cloned.metadata.template_source = persona.id;
  
  return cloned;
}

/**
 * Get persona compatibility score (representational)
 */
export function getCompatibilityScore(
  persona: PersonaModel,
  requirements: {
    domains?: string[];
    engines?: string[];
    complexity?: string;
  }
): number {
  let score = 0;
  let factors = 0;
  
  if (requirements.domains && requirements.domains.length > 0) {
    const matchingDomains = persona.domain_affinities.filter(
      a => requirements.domains!.includes(a.domain)
    );
    score += matchingDomains.reduce((sum, a) => sum + a.affinity_level, 0) / requirements.domains.length;
    factors++;
  }
  
  if (requirements.engines && requirements.engines.length > 0) {
    const matchingEngines = persona.engine_affinities.filter(
      a => requirements.engines!.includes(a.engine)
    );
    score += matchingEngines.reduce((sum, a) => sum + a.affinity_level, 0) / requirements.engines.length;
    factors++;
  }
  
  if (requirements.complexity) {
    if (persona.process_preferences.preferred_complexity === requirements.complexity) {
      score += 1;
    } else {
      score += 0.5; // Partial match
    }
    factors++;
  }
  
  return factors > 0 ? score / factors : 0;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'PersonaEngine',
    version: '1.0.0',
    description: 'Representational persona modeling for CHE·NU',
    subModules: [
      'TraitEngine',
      'StyleEngine',
      'DomainAffinityEngine',
      'EngineAffinityEngine',
      'CapabilityInfluenceEngine',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPsychology: true,
      noAdvice: true,
    },
  };
}

export default {
  createPersona,
  attachTrait,
  removeTrait,
  attachStyle,
  removeStyle,
  assignDomainAffinity,
  removeDomainAffinity,
  assignEngineAffinity,
  removeEngineAffinity,
  addCapabilityInfluence,
  updateProcessPreferences,
  summarizePersona,
  clonePersona,
  getCompatibilityScore,
  meta,
};

============================================================
SECTION B2 — SUB-MODULES
============================================================

--- FILE: /che-nu-sdk/core/persona/trait.engine.ts

/**
 * CHE·NU SDK — Trait Engine
 * ==========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Abstract structural traits (not psychological).
 * 
 * @module TraitEngine
 * @version 1.0.0
 */

import type { PersonaTrait } from '../persona';

// ============================================================
// TRAIT DEFINITIONS
// ============================================================

export const TRAIT_CATALOG: Record<string, Omit<PersonaTrait, 'id' | 'intensity'>> = {
  // Cognitive traits
  analytical: {
    name: 'Analytical',
    category: 'cognitive',
    description: 'Preference for data-driven, systematic analysis',
    metadata: { keywords: ['data', 'logic', 'systematic'] },
  },
  creative: {
    name: 'Creative',
    category: 'cognitive',
    description: 'Preference for novel approaches and ideation',
    metadata: { keywords: ['innovation', 'ideas', 'imagination'] },
  },
  systematic: {
    name: 'Systematic',
    category: 'cognitive',
    description: 'Preference for structured, methodical approaches',
    metadata: { keywords: ['order', 'process', 'structure'] },
  },
  exploratory: {
    name: 'Exploratory',
    category: 'cognitive',
    description: 'Preference for discovery and open-ended investigation',
    metadata: { keywords: ['discovery', 'curiosity', 'exploration'] },
  },
  intuitive: {
    name: 'Intuitive',
    category: 'cognitive',
    description: 'Preference for pattern recognition and synthesis',
    metadata: { keywords: ['patterns', 'synthesis', 'insight'] },
  },
  
  // Behavioral traits
  focused: {
    name: 'Focused',
    category: 'behavioral',
    description: 'Tendency toward deep concentration on single tasks',
    metadata: { keywords: ['concentration', 'depth', 'single-task'] },
  },
  multitasking: {
    name: 'Multitasking',
    category: 'behavioral',
    description: 'Comfort with parallel task management',
    metadata: { keywords: ['parallel', 'context-switch', 'breadth'] },
  },
  proactive: {
    name: 'Proactive',
    category: 'behavioral',
    description: 'Tendency to initiate and anticipate',
    metadata: { keywords: ['initiative', 'anticipation', 'forward'] },
  },
  reactive: {
    name: 'Reactive',
    category: 'behavioral',
    description: 'Preference for responding to inputs and situations',
    metadata: { keywords: ['response', 'adaptation', 'flexibility'] },
  },
  
  // Communicative traits
  verbose: {
    name: 'Verbose',
    category: 'communicative',
    description: 'Preference for detailed, comprehensive communication',
    metadata: { keywords: ['detail', 'thorough', 'comprehensive'] },
  },
  concise: {
    name: 'Concise',
    category: 'communicative',
    description: 'Preference for brief, to-the-point communication',
    metadata: { keywords: ['brief', 'essential', 'succinct'] },
  },
  visual: {
    name: 'Visual',
    category: 'communicative',
    description: 'Preference for visual representation and diagrams',
    metadata: { keywords: ['diagrams', 'charts', 'visual'] },
  },
  textual: {
    name: 'Textual',
    category: 'communicative',
    description: 'Preference for text-based information',
    metadata: { keywords: ['text', 'written', 'documentation'] },
  },
  
  // Organizational traits
  structured: {
    name: 'Structured',
    category: 'organizational',
    description: 'Preference for organized, hierarchical approaches',
    metadata: { keywords: ['hierarchy', 'organization', 'planned'] },
  },
  flexible: {
    name: 'Flexible',
    category: 'organizational',
    description: 'Preference for adaptable, fluid approaches',
    metadata: { keywords: ['adaptable', 'fluid', 'agile'] },
  },
  deadline_driven: {
    name: 'Deadline-Driven',
    category: 'organizational',
    description: 'Strong orientation toward time constraints',
    metadata: { keywords: ['time', 'deadlines', 'schedules'] },
  },
  quality_driven: {
    name: 'Quality-Driven',
    category: 'organizational',
    description: 'Strong orientation toward output quality',
    metadata: { keywords: ['quality', 'excellence', 'standards'] },
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List all available traits
 */
export function listTraits(): string[] {
  return Object.keys(TRAIT_CATALOG);
}

/**
 * List traits by category
 */
export function listTraitsByCategory(category: PersonaTrait['category']): string[] {
  return Object.entries(TRAIT_CATALOG)
    .filter(([_, trait]) => trait.category === category)
    .map(([key, _]) => key);
}

/**
 * Get trait definition
 */
export function getTrait(traitKey: string): Omit<PersonaTrait, 'id' | 'intensity'> | null {
  return TRAIT_CATALOG[traitKey] || null;
}

/**
 * Describe a trait
 */
export function describeTrait(traitKey: string): string {
  const trait = TRAIT_CATALOG[traitKey];
  if (!trait) return `Unknown trait: ${traitKey}`;
  return `${trait.name} (${trait.category}): ${trait.description}`;
}

/**
 * Create trait with intensity
 */
export function createTrait(
  traitKey: string,
  intensity: number = 0.5
): Omit<PersonaTrait, 'id'> | null {
  const trait = TRAIT_CATALOG[traitKey];
  if (!trait) return null;
  
  return {
    ...trait,
    intensity: Math.max(0, Math.min(1, intensity)),
  };
}

/**
 * Get trait categories
 */
export function getCategories(): PersonaTrait['category'][] {
  return ['cognitive', 'behavioral', 'communicative', 'organizational'];
}

/**
 * Find complementary traits
 */
export function findComplementaryTraits(traitKey: string): string[] {
  const complementary: Record<string, string[]> = {
    analytical: ['systematic', 'focused', 'structured'],
    creative: ['exploratory', 'intuitive', 'flexible'],
    systematic: ['analytical', 'structured', 'deadline_driven'],
    exploratory: ['creative', 'flexible', 'multitasking'],
    focused: ['analytical', 'quality_driven', 'structured'],
    multitasking: ['flexible', 'reactive', 'exploratory'],
    proactive: ['creative', 'structured', 'deadline_driven'],
    concise: ['focused', 'deadline_driven', 'systematic'],
    verbose: ['analytical', 'quality_driven', 'textual'],
  };
  
  return complementary[traitKey] || [];
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'TraitEngine',
    version: '1.0.0',
    description: 'Abstract structural traits for personas',
    parent: 'PersonaEngine',
    traitCount: Object.keys(TRAIT_CATALOG).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPsychology: true,
    },
  };
}

export default {
  listTraits,
  listTraitsByCategory,
  getTrait,
  describeTrait,
  createTrait,
  getCategories,
  findComplementaryTraits,
  meta,
};

--- FILE: /che-nu-sdk/core/persona/style.engine.ts

/**
 * CHE·NU SDK — Style Engine
 * ==========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Work styles for personas.
 * 
 * @module StyleEngine
 * @version 1.0.0
 */

import type { PersonaStyle } from '../persona';

// ============================================================
// STYLE DEFINITIONS
// ============================================================

export const STYLE_CATALOG: Record<string, Omit<PersonaStyle, 'id'>> = {
  // Workflow styles
  linear: {
    name: 'Linear',
    type: 'workflow',
    description: 'Sequential, step-by-step progression',
    preferences: ['Clear milestones', 'One task at a time', 'Sequential dependencies'],
    metadata: {},
  },
  iterative: {
    name: 'Iterative',
    type: 'workflow',
    description: 'Cyclic refinement and improvement',
    preferences: ['Multiple passes', 'Continuous improvement', 'Feedback loops'],
    metadata: {},
  },
  branching: {
    name: 'Branching',
    type: 'workflow',
    description: 'Parallel exploration of multiple paths',
    preferences: ['Options exploration', 'Parallel tracks', 'Compare alternatives'],
    metadata: {},
  },
  agile: {
    name: 'Agile',
    type: 'workflow',
    description: 'Short cycles with frequent adaptation',
    preferences: ['Sprints', 'Retrospectives', 'Adaptive planning'],
    metadata: {},
  },
  
  // Communication styles
  formal: {
    name: 'Formal',
    type: 'communication',
    description: 'Structured, professional communication',
    preferences: ['Documentation', 'Clear protocols', 'Official channels'],
    metadata: {},
  },
  informal: {
    name: 'Informal',
    type: 'communication',
    description: 'Casual, direct communication',
    preferences: ['Quick chats', 'Direct messages', 'Flexible formats'],
    metadata: {},
  },
  visual_communicator: {
    name: 'Visual Communicator',
    type: 'communication',
    description: 'Preference for visual aids and diagrams',
    preferences: ['Diagrams', 'Charts', 'Visual presentations'],
    metadata: {},
  },
  written_communicator: {
    name: 'Written Communicator',
    type: 'communication',
    description: 'Preference for written documentation',
    preferences: ['Documents', 'Email', 'Detailed notes'],
    metadata: {},
  },
  
  // Decision-making styles
  data_driven: {
    name: 'Data-Driven',
    type: 'decision_making',
    description: 'Decisions based on data and evidence',
    preferences: ['Metrics', 'Analysis', 'Quantitative reasoning'],
    metadata: {},
  },
  intuition_based: {
    name: 'Intuition-Based',
    type: 'decision_making',
    description: 'Decisions guided by experience and instinct',
    preferences: ['Experience', 'Pattern recognition', 'Gut feeling'],
    metadata: {},
  },
  consensus_seeking: {
    name: 'Consensus-Seeking',
    type: 'decision_making',
    description: 'Collaborative decision-making',
    preferences: ['Group input', 'Alignment', 'Stakeholder buy-in'],
    metadata: {},
  },
  decisive: {
    name: 'Decisive',
    type: 'decision_making',
    description: 'Quick, confident decision-making',
    preferences: ['Speed', 'Commitment', 'Clear direction'],
    metadata: {},
  },
  
  // Collaboration styles
  independent: {
    name: 'Independent',
    type: 'collaboration',
    description: 'Preference for solo work',
    preferences: ['Autonomy', 'Self-direction', 'Individual ownership'],
    metadata: {},
  },
  collaborative: {
    name: 'Collaborative',
    type: 'collaboration',
    description: 'Preference for team work',
    preferences: ['Teamwork', 'Shared ownership', 'Joint problem-solving'],
    metadata: {},
  },
  mentoring: {
    name: 'Mentoring',
    type: 'collaboration',
    description: 'Knowledge sharing and guidance',
    preferences: ['Teaching', 'Guidance', 'Knowledge transfer'],
    metadata: {},
  },
  delegating: {
    name: 'Delegating',
    type: 'collaboration',
    description: 'Task distribution and oversight',
    preferences: ['Task assignment', 'Oversight', 'Empowerment'],
    metadata: {},
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List all styles
 */
export function listStyles(): string[] {
  return Object.keys(STYLE_CATALOG);
}

/**
 * List styles by type
 */
export function listStylesByType(type: PersonaStyle['type']): string[] {
  return Object.entries(STYLE_CATALOG)
    .filter(([_, style]) => style.type === type)
    .map(([key, _]) => key);
}

/**
 * Get style definition
 */
export function getStyle(styleKey: string): Omit<PersonaStyle, 'id'> | null {
  return STYLE_CATALOG[styleKey] || null;
}

/**
 * Describe a style
 */
export function describeStyle(styleKey: string): string {
  const style = STYLE_CATALOG[styleKey];
  if (!style) return `Unknown style: ${styleKey}`;
  return `${style.name} (${style.type}): ${style.description}. Preferences: ${style.preferences.join(', ')}`;
}

/**
 * Create style
 */
export function createStyle(styleKey: string): Omit<PersonaStyle, 'id'> | null {
  return STYLE_CATALOG[styleKey] || null;
}

/**
 * Get style types
 */
export function getTypes(): PersonaStyle['type'][] {
  return ['workflow', 'communication', 'decision_making', 'collaboration'];
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'StyleEngine',
    version: '1.0.0',
    description: 'Work styles for personas',
    parent: 'PersonaEngine',
    styleCount: Object.keys(STYLE_CATALOG).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  listStyles,
  listStylesByType,
  getStyle,
  describeStyle,
  createStyle,
  getTypes,
  meta,
};

--- FILE: /che-nu-sdk/core/persona/domain_affinity.engine.ts

/**
 * CHE·NU SDK — Domain Affinity Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Maps persona affinity to CHE·NU spheres (abstract).
 * 
 * @module DomainAffinityEngine
 * @version 1.0.0
 */

import type { DomainAffinity } from '../persona';

// ============================================================
// DOMAIN DEFINITIONS
// ============================================================

export const DOMAIN_CATALOG: Record<string, {
  name: string;
  sphere: string;
  description: string;
  related_engines: string[];
  expertise_examples: string[];
}> = {
  personal: {
    name: 'Personal',
    sphere: 'Maison',
    description: 'Personal life management and self-improvement',
    related_engines: ['ReflectionEngine', 'KnowledgeEngine'],
    expertise_examples: ['Productivity', 'Wellness', 'Finance', 'Learning'],
  },
  business: {
    name: 'Business',
    sphere: 'Entreprise',
    description: 'Professional and enterprise activities',
    related_engines: ['ProjectEngine', 'AnalysisEngine', 'DataEngine'],
    expertise_examples: ['Strategy', 'Operations', 'Management', 'Growth'],
  },
  projects: {
    name: 'Projects',
    sphere: 'Projets',
    description: 'Project planning and execution',
    related_engines: ['ProjectEngine', 'ProcessEngine', 'MethodologyEngine'],
    expertise_examples: ['Planning', 'Execution', 'Tracking', 'Delivery'],
  },
  creative: {
    name: 'Creative',
    sphere: 'Creative Studio',
    description: 'Creative and artistic endeavors',
    related_engines: ['CreativityEngine', 'ContentEngine', 'XRSceneEngine'],
    expertise_examples: ['Design', 'Art', 'Writing', 'Media'],
  },
  government: {
    name: 'Government',
    sphere: 'Gouvernement',
    description: 'Administrative and civic activities',
    related_engines: ['KnowledgeEngine', 'ContentEngine'],
    expertise_examples: ['Policy', 'Administration', 'Civic', 'Compliance'],
  },
  real_estate: {
    name: 'Real Estate',
    sphere: 'Immobilier',
    description: 'Property and real estate management',
    related_engines: ['DataEngine', 'ProjectEngine'],
    expertise_examples: ['Properties', 'Investments', 'Development', 'Management'],
  },
  associations: {
    name: 'Associations',
    sphere: 'Associations',
    description: 'Collaborative organizations and communities',
    related_engines: ['KnowledgeEngine', 'ContentEngine'],
    expertise_examples: ['Community', 'Events', 'Membership', 'Collaboration'],
  },
  knowledge: {
    name: 'Knowledge',
    sphere: 'Scholar',
    description: 'Research and knowledge management',
    related_engines: ['KnowledgeEngine', 'AnalysisEngine', 'ContentEngine'],
    expertise_examples: ['Research', 'Learning', 'Documentation', 'Analysis'],
  },
  technology: {
    name: 'Technology',
    sphere: 'Various',
    description: 'Technical and engineering domains',
    related_engines: ['DataEngine', 'AnalysisEngine'],
    expertise_examples: ['Development', 'Architecture', 'Infrastructure', 'AI'],
  },
  xr_immersive: {
    name: 'XR/Immersive',
    sphere: 'Creative Studio',
    description: 'Extended reality and immersive experiences',
    related_engines: ['XRSceneEngine', 'HyperFabricEngine', 'CartographyEngine'],
    expertise_examples: ['VR', 'AR', '3D', 'Immersive Design'],
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List all domains
 */
export function affinityList(): string[] {
  return Object.keys(DOMAIN_CATALOG);
}

/**
 * Get domain info
 */
export function getDomainInfo(domainKey: string): typeof DOMAIN_CATALOG[string] | null {
  return DOMAIN_CATALOG[domainKey] || null;
}

/**
 * Create domain affinity
 */
export function createAffinity(
  domainKey: string,
  level: number,
  expertiseTags?: string[]
): DomainAffinity | null {
  const domain = DOMAIN_CATALOG[domainKey];
  if (!domain) return null;
  
  return {
    domain: domainKey,
    affinity_level: Math.max(0, Math.min(1, level)),
    expertise_tags: expertiseTags || [],
    notes: '',
  };
}

/**
 * Link domain to sphere
 */
export function linkSphere(domainKey: string): string | null {
  const domain = DOMAIN_CATALOG[domainKey];
  return domain?.sphere || null;
}

/**
 * Get related engines for domain
 */
export function getRelatedEngines(domainKey: string): string[] {
  const domain = DOMAIN_CATALOG[domainKey];
  return domain?.related_engines || [];
}

/**
 * Find domains by sphere
 */
export function findDomainsBySphere(sphere: string): string[] {
  return Object.entries(DOMAIN_CATALOG)
    .filter(([_, info]) => info.sphere === sphere)
    .map(([key, _]) => key);
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'DomainAffinityEngine',
    version: '1.0.0',
    description: 'Domain affinity mapping for personas',
    parent: 'PersonaEngine',
    domainCount: Object.keys(DOMAIN_CATALOG).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  affinityList,
  getDomainInfo,
  createAffinity,
  linkSphere,
  getRelatedEngines,
  findDomainsBySphere,
  meta,
};

--- FILE: /che-nu-sdk/core/persona/engine_affinity.engine.ts

/**
 * CHE·NU SDK — Engine Affinity Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Links persona to CHE·NU engines.
 * 
 * @module EngineAffinityEngine
 * @version 1.0.0
 */

import type { EngineAffinity } from '../persona';

// ============================================================
// ENGINE CATALOG
// ============================================================

export const ENGINE_CATALOG: Record<string, {
  name: string;
  category: string;
  description: string;
  typical_users: string[];
}> = {
  KnowledgeEngine: {
    name: 'Knowledge Engine',
    category: 'core',
    description: 'Knowledge management and retrieval',
    typical_users: ['Researchers', 'Analysts', 'Learners'],
  },
  ProjectEngine: {
    name: 'Project Engine',
    category: 'core',
    description: 'Project planning and tracking',
    typical_users: ['Project Managers', 'Team Leads', 'Coordinators'],
  },
  MissionEngine: {
    name: 'Mission Engine',
    category: 'core',
    description: 'Mission and objective management',
    typical_users: ['Strategists', 'Leaders', 'Goal-setters'],
  },
  ContentEngine: {
    name: 'Content Engine',
    category: 'core',
    description: 'Content creation and management',
    typical_users: ['Writers', 'Creators', 'Documenters'],
  },
  AnalysisEngine: {
    name: 'Analysis Engine',
    category: 'core',
    description: 'Data analysis and insights',
    typical_users: ['Analysts', 'Researchers', 'Decision-makers'],
  },
  DataEngine: {
    name: 'Data Engine',
    category: 'core',
    description: 'Data processing and management',
    typical_users: ['Data specialists', 'Engineers', 'Analysts'],
  },
  CreativityEngine: {
    name: 'Creativity Engine',
    category: 'creative',
    description: 'Creative ideation and exploration',
    typical_users: ['Creatives', 'Designers', 'Innovators'],
  },
  XRSceneEngine: {
    name: 'XR Scene Engine',
    category: 'xr',
    description: 'Extended reality scene building',
    typical_users: ['XR developers', '3D artists', 'Experience designers'],
  },
  ProcessEngine: {
    name: 'Process Engine',
    category: 'core',
    description: 'Process and workflow modeling',
    typical_users: ['Process designers', 'Operations', 'Managers'],
  },
  SimulationEngine: {
    name: 'Simulation Engine',
    category: 'advanced',
    description: 'Representational simulations',
    typical_users: ['Strategists', 'Planners', 'Analysts'],
  },
  ObjectEngine: {
    name: 'Object Engine',
    category: 'core',
    description: 'Object and resource management',
    typical_users: ['Asset managers', 'Organizers', 'Cataloguers'],
  },
  MethodologyEngine: {
    name: 'Methodology Engine',
    category: 'core',
    description: 'Framework and methodology application',
    typical_users: ['Consultants', 'Strategists', 'Process designers'],
  },
  ReflectionEngine: {
    name: 'Reflection Engine',
    category: 'personal',
    description: 'Self-reflection and review',
    typical_users: ['Individuals', 'Coaches', 'Learners'],
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List all engines
 */
export function preferredEngines(): string[] {
  return Object.keys(ENGINE_CATALOG);
}

/**
 * List engines by category
 */
export function listEnginesByCategory(category: string): string[] {
  return Object.entries(ENGINE_CATALOG)
    .filter(([_, info]) => info.category === category)
    .map(([key, _]) => key);
}

/**
 * Get engine info
 */
export function getEngineInfo(engineKey: string): typeof ENGINE_CATALOG[string] | null {
  return ENGINE_CATALOG[engineKey] || null;
}

/**
 * Create engine affinity
 */
export function createAffinity(
  engineKey: string,
  level: number,
  frequency: EngineAffinity['usage_frequency'] = 'occasional'
): EngineAffinity | null {
  if (!ENGINE_CATALOG[engineKey]) return null;
  
  return {
    engine: engineKey,
    affinity_level: Math.max(0, Math.min(1, level)),
    usage_frequency: frequency,
    notes: '',
  };
}

/**
 * Evaluate affinity based on traits
 */
export function evaluateAffinity(
  traits: string[],
  engineKey: string
): number {
  const traitToEngine: Record<string, string[]> = {
    analytical: ['AnalysisEngine', 'DataEngine', 'KnowledgeEngine'],
    creative: ['CreativityEngine', 'ContentEngine', 'XRSceneEngine'],
    systematic: ['ProcessEngine', 'ProjectEngine', 'MethodologyEngine'],
    exploratory: ['KnowledgeEngine', 'SimulationEngine', 'CreativityEngine'],
    focused: ['AnalysisEngine', 'ContentEngine'],
    visual: ['XRSceneEngine', 'CreativityEngine'],
  };
  
  let score = 0;
  traits.forEach(trait => {
    const engines = traitToEngine[trait] || [];
    if (engines.includes(engineKey)) {
      score += 0.3;
    }
  });
  
  return Math.min(1, score);
}

/**
 * Get engine categories
 */
export function getCategories(): string[] {
  const categories = new Set<string>();
  Object.values(ENGINE_CATALOG).forEach(e => categories.add(e.category));
  return Array.from(categories);
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'EngineAffinityEngine',
    version: '1.0.0',
    description: 'Engine affinity mapping for personas',
    parent: 'PersonaEngine',
    engineCount: Object.keys(ENGINE_CATALOG).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  preferredEngines,
  listEnginesByCategory,
  getEngineInfo,
  createAffinity,
  evaluateAffinity,
  getCategories,
  meta,
};

--- FILE: /che-nu-sdk/core/persona/capability_influence.engine.ts

/**
 * CHE·NU SDK — Capability Influence Engine
 * ==========================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Abstract influence of persona on capabilities (structural only).
 * 
 * @module CapabilityInfluenceEngine
 * @version 1.0.0
 */

import type { CapabilityInfluence, PersonaModel } from '../persona';

// ============================================================
// CAPABILITY DEFINITIONS
// ============================================================

export const CAPABILITY_CATALOG: string[] = [
  'research',
  'analysis',
  'creation',
  'planning',
  'execution',
  'communication',
  'collaboration',
  'decision_making',
  'problem_solving',
  'learning',
  'teaching',
  'organizing',
  'innovating',
  'reviewing',
  'synthesizing',
];

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List capabilities
 */
export function listCapabilities(): string[] {
  return [...CAPABILITY_CATALOG];
}

/**
 * Create influence map
 */
export function influenceMap(
  persona: PersonaModel
): Map<string, CapabilityInfluence> {
  const map = new Map<string, CapabilityInfluence>();
  
  // Map traits to capability influences
  const traitInfluences: Record<string, { capability: string; type: CapabilityInfluence['influence_type']; strength: number }[]> = {
    analytical: [
      { capability: 'analysis', type: 'enhances', strength: 0.8 },
      { capability: 'research', type: 'enhances', strength: 0.6 },
      { capability: 'decision_making', type: 'enhances', strength: 0.5 },
    ],
    creative: [
      { capability: 'creation', type: 'enhances', strength: 0.8 },
      { capability: 'innovating', type: 'enhances', strength: 0.7 },
      { capability: 'problem_solving', type: 'enhances', strength: 0.5 },
    ],
    systematic: [
      { capability: 'planning', type: 'enhances', strength: 0.8 },
      { capability: 'organizing', type: 'enhances', strength: 0.7 },
      { capability: 'execution', type: 'enhances', strength: 0.6 },
    ],
    exploratory: [
      { capability: 'research', type: 'enhances', strength: 0.7 },
      { capability: 'learning', type: 'enhances', strength: 0.7 },
      { capability: 'innovating', type: 'enhances', strength: 0.5 },
    ],
    focused: [
      { capability: 'execution', type: 'enhances', strength: 0.7 },
      { capability: 'analysis', type: 'enhances', strength: 0.5 },
      { capability: 'collaboration', type: 'challenges', strength: 0.3 },
    ],
    concise: [
      { capability: 'communication', type: 'enhances', strength: 0.6 },
      { capability: 'synthesizing', type: 'enhances', strength: 0.5 },
    ],
    verbose: [
      { capability: 'teaching', type: 'enhances', strength: 0.6 },
      { capability: 'communication', type: 'enhances', strength: 0.5 },
    ],
  };
  
  persona.traits.forEach(trait => {
    const influences = traitInfluences[trait.name.toLowerCase()] || [];
    influences.forEach(inf => {
      const existing = map.get(inf.capability);
      const adjustedStrength = inf.strength * trait.intensity;
      
      if (!existing || adjustedStrength > existing.strength) {
        map.set(inf.capability, {
          capability: inf.capability,
          influence_type: inf.type,
          strength: adjustedStrength,
          description: `Influenced by ${trait.name} trait`,
        });
      }
    });
  });
  
  return map;
}

/**
 * Describe influence
 */
export function describeInfluence(influence: CapabilityInfluence): string {
  const verb = influence.influence_type === 'enhances' 
    ? 'enhances' 
    : influence.influence_type === 'challenges' 
      ? 'challenges' 
      : 'is neutral toward';
  
  return `Persona ${verb} ${influence.capability} (strength: ${(influence.strength * 100).toFixed(0)}%)`;
}

/**
 * Get enhanced capabilities
 */
export function getEnhancedCapabilities(
  persona: PersonaModel
): string[] {
  const map = influenceMap(persona);
  const enhanced: string[] = [];
  
  map.forEach((influence, capability) => {
    if (influence.influence_type === 'enhances' && influence.strength >= 0.5) {
      enhanced.push(capability);
    }
  });
  
  return enhanced;
}

/**
 * Get challenged capabilities
 */
export function getChallengedCapabilities(
  persona: PersonaModel
): string[] {
  const map = influenceMap(persona);
  const challenged: string[] = [];
  
  map.forEach((influence, capability) => {
    if (influence.influence_type === 'challenges') {
      challenged.push(capability);
    }
  });
  
  return challenged;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'CapabilityInfluenceEngine',
    version: '1.0.0',
    description: 'Abstract capability influence modeling',
    parent: 'PersonaEngine',
    capabilityCount: CAPABILITY_CATALOG.length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPsychology: true,
    },
  };
}

export default {
  listCapabilities,
  influenceMap,
  describeInfluence,
  getEnhancedCapabilities,
  getChallengedCapabilities,
  meta,
};

============================================================
SECTION B3 — PERSONA TEMPLATES
============================================================

--- FILE: /che-nu-sdk/core/persona/persona_templates.ts

/**
 * CHE·NU SDK — Persona Templates
 * ================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Predefined persona templates.
 * 
 * @module PersonaTemplates
 * @version 1.0.0
 */

import type { PersonaModel } from '../persona';
import { createPersona, attachTrait, attachStyle, assignDomainAffinity, assignEngineAffinity } from '../persona';
import { createTrait } from './trait.engine';
import { createStyle } from './style.engine';

// ============================================================
// TEMPLATE DEFINITIONS
// ============================================================

/**
 * Explorer Persona
 */
export function createExplorerPersona(): PersonaModel {
  let persona = createPersona({
    name: 'Explorer',
    description: 'Curious, discovery-oriented persona focused on exploration and learning',
    category: 'creative',
    avatar_icon: '🧭',
  });
  
  // Traits
  const exploratoryTrait = createTrait('exploratory', 0.9);
  const creativeTrait = createTrait('creative', 0.7);
  const flexibleTrait = createTrait('flexible', 0.8);
  
  if (exploratoryTrait) persona = attachTrait(persona, exploratoryTrait);
  if (creativeTrait) persona = attachTrait(persona, creativeTrait);
  if (flexibleTrait) persona = attachTrait(persona, flexibleTrait);
  
  // Styles
  const branchingStyle = createStyle('branching');
  const informalStyle = createStyle('informal');
  
  if (branchingStyle) persona = attachStyle(persona, branchingStyle);
  if (informalStyle) persona = attachStyle(persona, informalStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'knowledge',
    affinity_level: 0.9,
    expertise_tags: ['Research', 'Discovery', 'Learning'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'creative',
    affinity_level: 0.7,
    expertise_tags: ['Ideation', 'Experimentation'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'KnowledgeEngine',
    affinity_level: 0.9,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'SimulationEngine',
    affinity_level: 0.7,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'moderate',
    preferred_pace: 'moderate',
    iteration_preference: 'extensive',
  };
  
  persona.metadata.template_source = 'explorer_persona';
  
  return persona;
}

/**
 * Architect Persona
 */
export function createArchitectPersona(): PersonaModel {
  let persona = createPersona({
    name: 'Architect',
    description: 'Systematic, structure-oriented persona focused on design and planning',
    category: 'analytical',
    avatar_icon: '🏗️',
  });
  
  // Traits
  const systematicTrait = createTrait('systematic', 0.9);
  const structuredTrait = createTrait('structured', 0.85);
  const analyticalTrait = createTrait('analytical', 0.7);
  
  if (systematicTrait) persona = attachTrait(persona, systematicTrait);
  if (structuredTrait) persona = attachTrait(persona, structuredTrait);
  if (analyticalTrait) persona = attachTrait(persona, analyticalTrait);
  
  // Styles
  const linearStyle = createStyle('linear');
  const formalStyle = createStyle('formal');
  const dataStyle = createStyle('data_driven');
  
  if (linearStyle) persona = attachStyle(persona, linearStyle);
  if (formalStyle) persona = attachStyle(persona, formalStyle);
  if (dataStyle) persona = attachStyle(persona, dataStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'projects',
    affinity_level: 0.9,
    expertise_tags: ['Architecture', 'Planning', 'Structure'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'technology',
    affinity_level: 0.8,
    expertise_tags: ['Systems', 'Design', 'Infrastructure'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'ProcessEngine',
    affinity_level: 0.9,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'ProjectEngine',
    affinity_level: 0.85,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'MethodologyEngine',
    affinity_level: 0.8,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'complex',
    preferred_pace: 'moderate',
    iteration_preference: 'moderate',
  };
  
  persona.metadata.template_source = 'architect_persona';
  
  return persona;
}

/**
 * Analyst Persona
 */
export function createAnalystPersona(): PersonaModel {
  let persona = createPersona({
    name: 'Analyst',
    description: 'Data-driven, analytical persona focused on insights and evidence',
    category: 'analytical',
    avatar_icon: '📊',
  });
  
  // Traits
  const analyticalTrait = createTrait('analytical', 0.95);
  const focusedTrait = createTrait('focused', 0.8);
  const conciseTrait = createTrait('concise', 0.7);
  
  if (analyticalTrait) persona = attachTrait(persona, analyticalTrait);
  if (focusedTrait) persona = attachTrait(persona, focusedTrait);
  if (conciseTrait) persona = attachTrait(persona, conciseTrait);
  
  // Styles
  const dataDrivenStyle = createStyle('data_driven');
  const writtenStyle = createStyle('written_communicator');
  
  if (dataDrivenStyle) persona = attachStyle(persona, dataDrivenStyle);
  if (writtenStyle) persona = attachStyle(persona, writtenStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'knowledge',
    affinity_level: 0.85,
    expertise_tags: ['Research', 'Analysis', 'Data'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'business',
    affinity_level: 0.75,
    expertise_tags: ['Metrics', 'Performance', 'Insights'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'AnalysisEngine',
    affinity_level: 0.95,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'DataEngine',
    affinity_level: 0.9,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'KnowledgeEngine',
    affinity_level: 0.8,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'moderate',
    preferred_pace: 'moderate',
    iteration_preference: 'moderate',
  };
  
  persona.metadata.template_source = 'analyst_persona';
  
  return persona;
}

/**
 * Creative Persona
 */
export function createCreativePersona(): PersonaModel {
  let persona = createPersona({
    name: 'Creative',
    description: 'Innovation-focused persona oriented toward creation and expression',
    category: 'creative',
    avatar_icon: '🎨',
  });
  
  // Traits
  const creativeTrait = createTrait('creative', 0.95);
  const exploratoryTrait = createTrait('exploratory', 0.8);
  const visualTrait = createTrait('visual', 0.85);
  const flexibleTrait = createTrait('flexible', 0.75);
  
  if (creativeTrait) persona = attachTrait(persona, creativeTrait);
  if (exploratoryTrait) persona = attachTrait(persona, exploratoryTrait);
  if (visualTrait) persona = attachTrait(persona, visualTrait);
  if (flexibleTrait) persona = attachTrait(persona, flexibleTrait);
  
  // Styles
  const iterativeStyle = createStyle('iterative');
  const visualStyle = createStyle('visual_communicator');
  const intuitionStyle = createStyle('intuition_based');
  
  if (iterativeStyle) persona = attachStyle(persona, iterativeStyle);
  if (visualStyle) persona = attachStyle(persona, visualStyle);
  if (intuitionStyle) persona = attachStyle(persona, intuitionStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'creative',
    affinity_level: 0.95,
    expertise_tags: ['Design', 'Art', 'Innovation'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'xr_immersive',
    affinity_level: 0.8,
    expertise_tags: ['Visual', '3D', 'Immersive'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'CreativityEngine',
    affinity_level: 0.95,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'ContentEngine',
    affinity_level: 0.85,
    usage_frequency: 'frequent',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'XRSceneEngine',
    affinity_level: 0.8,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'moderate',
    preferred_pace: 'fast',
    iteration_preference: 'extensive',
  };
  
  persona.metadata.template_source = 'creative_persona';
  
  return persona;
}

/**
 * Strategist Persona
 */
export function createStrategistPersona(): PersonaModel {
  let persona = createPersona({
    name: 'Strategist',
    description: 'Vision-oriented persona focused on planning and direction',
    category: 'analytical',
    avatar_icon: '♟️',
  });
  
  // Traits
  const systematicTrait = createTrait('systematic', 0.8);
  const analyticalTrait = createTrait('analytical', 0.85);
  const proactiveTrait = createTrait('proactive', 0.9);
  const intuitiveTrait = createTrait('intuitive', 0.7);
  
  if (systematicTrait) persona = attachTrait(persona, systematicTrait);
  if (analyticalTrait) persona = attachTrait(persona, analyticalTrait);
  if (proactiveTrait) persona = attachTrait(persona, proactiveTrait);
  if (intuitiveTrait) persona = attachTrait(persona, intuitiveTrait);
  
  // Styles
  const branchingStyle = createStyle('branching');
  const decisiveStyle = createStyle('decisive');
  const consensusStyle = createStyle('consensus_seeking');
  
  if (branchingStyle) persona = attachStyle(persona, branchingStyle);
  if (decisiveStyle) persona = attachStyle(persona, decisiveStyle);
  if (consensusStyle) persona = attachStyle(persona, consensusStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'business',
    affinity_level: 0.9,
    expertise_tags: ['Strategy', 'Planning', 'Vision'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'projects',
    affinity_level: 0.8,
    expertise_tags: ['Roadmapping', 'Direction', 'Goals'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'MethodologyEngine',
    affinity_level: 0.9,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'SimulationEngine',
    affinity_level: 0.85,
    usage_frequency: 'frequent',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'AnalysisEngine',
    affinity_level: 0.75,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'complex',
    preferred_pace: 'moderate',
    iteration_preference: 'moderate',
  };
  
  persona.metadata.template_source = 'strategist_persona';
  
  return persona;
}

/**
 * Maker Persona
 */
export function createMakerPersona(): PersonaModel {
  let persona = createPersona({
    name: 'Maker',
    description: 'Hands-on, execution-focused persona oriented toward building and doing',
    category: 'work',
    avatar_icon: '🛠️',
  });
  
  // Traits
  const focusedTrait = createTrait('focused', 0.9);
  const proactiveTrait = createTrait('proactive', 0.85);
  const qualityTrait = createTrait('quality_driven', 0.8);
  const structuredTrait = createTrait('structured', 0.7);
  
  if (focusedTrait) persona = attachTrait(persona, focusedTrait);
  if (proactiveTrait) persona = attachTrait(persona, proactiveTrait);
  if (qualityTrait) persona = attachTrait(persona, qualityTrait);
  if (structuredTrait) persona = attachTrait(persona, structuredTrait);
  
  // Styles
  const linearStyle = createStyle('linear');
  const independentStyle = createStyle('independent');
  
  if (linearStyle) persona = attachStyle(persona, linearStyle);
  if (independentStyle) persona = attachStyle(persona, independentStyle);
  
  // Domain affinities
  persona = assignDomainAffinity(persona, {
    domain: 'projects',
    affinity_level: 0.9,
    expertise_tags: ['Execution', 'Building', 'Delivery'],
    notes: '',
  });
  persona = assignDomainAffinity(persona, {
    domain: 'technology',
    affinity_level: 0.85,
    expertise_tags: ['Development', 'Implementation'],
    notes: '',
  });
  
  // Engine affinities
  persona = assignEngineAffinity(persona, {
    engine: 'ProjectEngine',
    affinity_level: 0.9,
    usage_frequency: 'primary',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'ObjectEngine',
    affinity_level: 0.8,
    usage_frequency: 'frequent',
    notes: '',
  });
  persona = assignEngineAffinity(persona, {
    engine: 'ContentEngine',
    affinity_level: 0.75,
    usage_frequency: 'frequent',
    notes: '',
  });
  
  persona.process_preferences = {
    preferred_complexity: 'moderate',
    preferred_pace: 'fast',
    iteration_preference: 'minimal',
  };
  
  persona.metadata.template_source = 'maker_persona';
  
  return persona;
}

// ============================================================
// TEMPLATE REGISTRY
// ============================================================

const TEMPLATES: Record<string, () => PersonaModel> = {
  explorer: createExplorerPersona,
  architect: createArchitectPersona,
  analyst: createAnalystPersona,
  creative: createCreativePersona,
  strategist: createStrategistPersona,
  maker: createMakerPersona,
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List available templates
 */
export function listTemplates(): Array<{
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
}> {
  return [
    { id: 'explorer', name: 'Explorer', description: 'Discovery and learning focused', category: 'creative', icon: '🧭' },
    { id: 'architect', name: 'Architect', description: 'Structure and design focused', category: 'analytical', icon: '🏗️' },
    { id: 'analyst', name: 'Analyst', description: 'Data and insights focused', category: 'analytical', icon: '📊' },
    { id: 'creative', name: 'Creative', description: 'Innovation and expression focused', category: 'creative', icon: '🎨' },
    { id: 'strategist', name: 'Strategist', description: 'Vision and planning focused', category: 'analytical', icon: '♟️' },
    { id: 'maker', name: 'Maker', description: 'Building and execution focused', category: 'work', icon: '🛠️' },
  ];
}

/**
 * Load a template
 */
export function loadTemplate(templateId: string): PersonaModel | null {
  const templateFn = TEMPLATES[templateId];
  if (!templateFn) return null;
  return templateFn();
}

/**
 * Get templates by category
 */
export function getTemplatesByCategory(category: string): string[] {
  return listTemplates()
    .filter(t => t.category === category)
    .map(t => t.id);
}

export default {
  listTemplates,
  loadTemplate,
  getTemplatesByCategory,
  createExplorerPersona,
  createArchitectPersona,
  createAnalystPersona,
  createCreativePersona,
  createStrategistPersona,
  createMakerPersona,
};
