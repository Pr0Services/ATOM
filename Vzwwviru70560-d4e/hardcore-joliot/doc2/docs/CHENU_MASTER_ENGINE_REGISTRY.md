############################################################
#                                                          #
#       CHE·NU MASTER ENGINE REGISTRY                      #
#       COMPLETE LIST OF 28 ENGINES + 67 SUB-ENGINES       #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
OVERVIEW
============================================================

Total Engines:      28
Total Sub-Engines:  67
Agent Templates:    12
Domain Spheres:     12

All engines are OPERATIONAL MODULES (not spheres).
All engines are REPRESENTATIONAL ONLY (no execution).

============================================================
MASTER ENGINE LIST
============================================================

--- FILE: /che-nu-sdk/registry/engine_registry.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Master Engine Registry
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Complete catalog of all operational engines.
 * 
 * @module EngineRegistry
 * @version 1.0.0
 */

// ============================================================
// ENGINE METADATA TYPES
// ============================================================

export interface EngineInfo {
  id: string;
  name: string;
  description: string;
  category: EngineCategory;
  path: string;
  version: string;
  subEngines: SubEngineInfo[];
  usedByAgents: string[];
  domainSpheres: string[];
  status: 'stable' | 'beta' | 'experimental';
}

export interface SubEngineInfo {
  id: string;
  name: string;
  description: string;
  parentEngine: string;
}

export type EngineCategory = 
  | 'personal'
  | 'business'
  | 'knowledge'
  | 'creative'
  | 'operational'
  | 'support';

// ============================================================
// COMPLETE ENGINE REGISTRY
// ============================================================

export const ENGINE_REGISTRY: EngineInfo[] = [

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: PERSONAL (5 engines, 13 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'health-engine',
    name: 'HealthEngine',
    description: 'Health and wellness management including fitness, nutrition, sleep, and vital tracking',
    category: 'personal',
    path: '/che-nu-sdk/engines/health.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'fitness', name: 'FitnessEngine', description: 'Exercise and workout planning', parentEngine: 'HealthEngine' },
      { id: 'nutrition', name: 'NutritionEngine', description: 'Diet and nutrition tracking', parentEngine: 'HealthEngine' },
      { id: 'sleep', name: 'SleepEngine', description: 'Sleep quality and patterns', parentEngine: 'HealthEngine' },
      { id: 'wellness', name: 'WellnessEngine', description: 'Overall wellness metrics', parentEngine: 'HealthEngine' },
      { id: 'vital', name: 'VitalEngine', description: 'Vital signs monitoring', parentEngine: 'HealthEngine' },
    ],
    usedByAgents: ['Health Overview Agent'],
    domainSpheres: ['Personal'],
    status: 'stable',
  },

  {
    id: 'emotion-engine',
    name: 'EmotionEngine',
    description: 'Emotional awareness, regulation, and resilience frameworks',
    category: 'personal',
    path: '/che-nu-sdk/engines/emotion.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'awareness', name: 'AwarenessEngine', description: 'Emotional awareness tracking', parentEngine: 'EmotionEngine' },
      { id: 'regulation', name: 'RegulationEngine', description: 'Emotion regulation strategies', parentEngine: 'EmotionEngine' },
      { id: 'resilience', name: 'ResilienceEngine', description: 'Resilience building frameworks', parentEngine: 'EmotionEngine' },
    ],
    usedByAgents: ['Health Overview Agent', 'Wellbeing Mentor Agent'],
    domainSpheres: ['Personal', 'Social'],
    status: 'stable',
  },

  {
    id: 'productivity-engine',
    name: 'ProductivityEngine',
    description: 'Personal productivity optimization including time blocking, focus, and energy management',
    category: 'personal',
    path: '/che-nu-sdk/engines/productivity.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'timeblock', name: 'TimeBlockEngine', description: 'Time blocking strategies', parentEngine: 'ProductivityEngine' },
      { id: 'focus', name: 'FocusEngine', description: 'Focus and deep work management', parentEngine: 'ProductivityEngine' },
      { id: 'habit', name: 'HabitEngine', description: 'Habit tracking and formation', parentEngine: 'ProductivityEngine' },
      { id: 'energy', name: 'EnergyEngine', description: 'Energy level optimization', parentEngine: 'ProductivityEngine' },
    ],
    usedByAgents: ['Productivity Coach', 'XR Scene Architect'],
    domainSpheres: ['Personal', 'Business', 'MyTeam'],
    status: 'stable',
  },

  {
    id: 'reflection-engine',
    name: 'ReflectionEngine',
    description: 'Journaling, gratitude practices, and self-reflection workflows',
    category: 'personal',
    path: '/che-nu-sdk/engines/reflection.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Wellbeing Mentor Agent', 'Productivity Coach'],
    domainSpheres: ['Personal'],
    status: 'stable',
  },

  {
    id: 'habit-engine',
    name: 'HabitEngine',
    description: 'Habit formation, tracking, and behavior change frameworks',
    category: 'personal',
    path: '/che-nu-sdk/engines/habit.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Health Overview Agent', 'Productivity Coach'],
    domainSpheres: ['Personal'],
    status: 'stable',
  },

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: BUSINESS (6 engines, 19 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'finance-engine',
    name: 'FinanceEngine',
    description: 'Financial planning, budgeting, investment analysis, and wealth management',
    category: 'business',
    path: '/che-nu-sdk/engines/finance.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'budget', name: 'BudgetEngine', description: 'Budget planning and tracking', parentEngine: 'FinanceEngine' },
      { id: 'investment', name: 'InvestmentEngine', description: 'Investment analysis frameworks', parentEngine: 'FinanceEngine' },
      { id: 'tax', name: 'TaxEngine', description: 'Tax planning structures', parentEngine: 'FinanceEngine' },
      { id: 'retirement', name: 'RetirementEngine', description: 'Retirement planning', parentEngine: 'FinanceEngine' },
      { id: 'debt', name: 'DebtEngine', description: 'Debt management strategies', parentEngine: 'FinanceEngine' },
    ],
    usedByAgents: ['Finance Overview Agent'],
    domainSpheres: ['Personal', 'Business'],
    status: 'stable',
  },

  {
    id: 'strategy-engine',
    name: 'StrategyEngine',
    description: 'Strategic planning, positioning, and execution frameworks',
    category: 'business',
    path: '/che-nu-sdk/engines/strategy.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'vision', name: 'VisionEngine', description: 'Vision and mission development', parentEngine: 'StrategyEngine' },
      { id: 'analysis-sub', name: 'AnalysisEngine', description: 'Strategic analysis (SWOT, etc.)', parentEngine: 'StrategyEngine' },
      { id: 'positioning', name: 'PositioningEngine', description: 'Market positioning', parentEngine: 'StrategyEngine' },
      { id: 'roadmap', name: 'RoadmapEngine', description: 'Strategic roadmap planning', parentEngine: 'StrategyEngine' },
      { id: 'execution', name: 'ExecutionEngine', description: 'Strategy execution tracking', parentEngine: 'StrategyEngine' },
    ],
    usedByAgents: ['Strategy Agent', 'Finance Overview Agent'],
    domainSpheres: ['Business', 'Personal', 'Projets'],
    status: 'stable',
  },

  {
    id: 'project-engine',
    name: 'ProjectEngine',
    description: 'Project planning, resource management, and delivery tracking',
    category: 'business',
    path: '/che-nu-sdk/engines/project.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'planning', name: 'PlanningEngine', description: 'Project planning structures', parentEngine: 'ProjectEngine' },
      { id: 'tracking', name: 'TrackingEngine', description: 'Progress tracking', parentEngine: 'ProjectEngine' },
      { id: 'resource', name: 'ResourceEngine', description: 'Resource allocation', parentEngine: 'ProjectEngine' },
      { id: 'risk', name: 'RiskEngine', description: 'Risk management', parentEngine: 'ProjectEngine' },
    ],
    usedByAgents: ['Project Manager Agent'],
    domainSpheres: ['Business', 'Projets', 'MyTeam'],
    status: 'stable',
  },

  {
    id: 'collaboration-engine',
    name: 'CollaborationEngine',
    description: 'Team coordination, meetings, status updates, and handoffs',
    category: 'business',
    path: '/che-nu-sdk/engines/collaboration.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'team', name: 'TeamEngine', description: 'Team structure and roles', parentEngine: 'CollaborationEngine' },
      { id: 'meeting', name: 'MeetingEngine', description: 'Meeting planning and templates', parentEngine: 'CollaborationEngine' },
      { id: 'status', name: 'StatusEngine', description: 'Status update frameworks', parentEngine: 'CollaborationEngine' },
      { id: 'handoff', name: 'HandoffEngine', description: 'Task handoff workflows', parentEngine: 'CollaborationEngine' },
      { id: 'feedback-collab', name: 'FeedbackCollabEngine', description: 'Feedback collection', parentEngine: 'CollaborationEngine' },
    ],
    usedByAgents: ['Project Manager Agent', 'XR Scene Architect'],
    domainSpheres: ['Business', 'MyTeam', 'Projets'],
    status: 'stable',
  },

  {
    id: 'communication-engine',
    name: 'CommunicationEngine',
    description: 'Communication strategy, messaging, and stakeholder engagement',
    category: 'business',
    path: '/che-nu-sdk/engines/communication.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'messaging', name: 'MessagingEngine', description: 'Message crafting and tone', parentEngine: 'CommunicationEngine' },
      { id: 'channel', name: 'ChannelEngine', description: 'Communication channel selection', parentEngine: 'CommunicationEngine' },
      { id: 'presentation', name: 'PresentationEngine', description: 'Presentation structuring', parentEngine: 'CommunicationEngine' },
      { id: 'negotiation', name: 'NegotiationEngine', description: 'Negotiation frameworks', parentEngine: 'CommunicationEngine' },
    ],
    usedByAgents: ['Communication Specialist Agent'],
    domainSpheres: ['Business', 'Personal', 'Community'],
    status: 'stable',
  },

  {
    id: 'relationship-engine',
    name: 'RelationshipEngine',
    description: 'Relationship management, networking, and stakeholder mapping',
    category: 'business',
    path: '/che-nu-sdk/engines/relationship.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Communication Specialist Agent', 'Wellbeing Mentor Agent'],
    domainSpheres: ['Business', 'Personal', 'Social'],
    status: 'stable',
  },

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: KNOWLEDGE (6 engines, 12 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'knowledge-engine',
    name: 'KnowledgeEngine',
    description: 'Knowledge organization, mapping, and connection discovery',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/knowledge.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'taxonomy', name: 'TaxonomyEngine', description: 'Knowledge taxonomy building', parentEngine: 'KnowledgeEngine' },
      { id: 'connection', name: 'ConnectionEngine', description: 'Concept connection mapping', parentEngine: 'KnowledgeEngine' },
      { id: 'visualization-k', name: 'VisualizationEngine', description: 'Knowledge visualization', parentEngine: 'KnowledgeEngine' },
    ],
    usedByAgents: ['Research Agent', 'Knowledge Map Agent', 'Finance Overview Agent'],
    domainSpheres: ['Scholar', 'Personal', 'Business'],
    status: 'stable',
  },

  {
    id: 'research-engine',
    name: 'ResearchEngine',
    description: 'Research process structuring, source management, and synthesis',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/research.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'source', name: 'SourceManagementEngine', description: 'Source collection and evaluation', parentEngine: 'ResearchEngine' },
      { id: 'synthesis', name: 'SynthesisEngine', description: 'Finding synthesis', parentEngine: 'ResearchEngine' },
      { id: 'citation', name: 'CitationEngine', description: 'Citation generation', parentEngine: 'ResearchEngine' },
      { id: 'literature', name: 'LiteratureEngine', description: 'Literature review planning', parentEngine: 'ResearchEngine' },
      { id: 'methodology-research', name: 'MethodologyResearchEngine', description: 'Research methodology frameworks', parentEngine: 'ResearchEngine' },
    ],
    usedByAgents: ['Research Agent'],
    domainSpheres: ['Scholar', 'Business', 'Personal'],
    status: 'stable',
  },

  {
    id: 'skill-engine',
    name: 'SkillEngine',
    description: 'Skill development, gap analysis, and learning path design',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/skill.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'taxonomy-skill', name: 'TaxonomyEngine', description: 'Skill taxonomy', parentEngine: 'SkillEngine' },
      { id: 'gap', name: 'GapAnalysisEngine', description: 'Skill gap identification', parentEngine: 'SkillEngine' },
      { id: 'roadmap-skill', name: 'RoadmapEngine', description: 'Learning roadmap creation', parentEngine: 'SkillEngine' },
      { id: 'assessment', name: 'AssessmentEngine', description: 'Skill assessment frameworks', parentEngine: 'SkillEngine' },
    ],
    usedByAgents: ['Knowledge Map Agent'],
    domainSpheres: ['Scholar', 'Personal', 'Business'],
    status: 'stable',
  },

  {
    id: 'learning-engine',
    name: 'LearningEngine',
    description: 'Learning design, curriculum planning, and educational frameworks',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/learning.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Knowledge Map Agent'],
    domainSpheres: ['Scholar', 'Personal'],
    status: 'stable',
  },

  {
    id: 'analysis-engine',
    name: 'AnalysisEngine',
    description: 'Data analysis, pattern recognition, and insight synthesis',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/analysis.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'data', name: 'DataEngine', description: 'Data processing structures', parentEngine: 'AnalysisEngine' },
      { id: 'pattern', name: 'PatternEngine', description: 'Pattern recognition frameworks', parentEngine: 'AnalysisEngine' },
      { id: 'synthesis-a', name: 'SynthesisEngine', description: 'Insight synthesis', parentEngine: 'AnalysisEngine' },
    ],
    usedByAgents: ['Finance Overview Agent', 'Strategy Agent', 'Data Analyst Agent', 'Research Agent'],
    domainSpheres: ['Business', 'Scholar', 'Personal'],
    status: 'stable',
  },

  {
    id: 'methodology-engine',
    name: 'MethodologyEngine',
    description: 'Methodology frameworks and operational approaches',
    category: 'knowledge',
    path: '/che-nu-sdk/engines/methodology.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Research Agent', 'XR Scene Architect', 'Productivity Coach', 'Creative Director Agent', 'Knowledge Map Agent'],
    domainSpheres: ['Scholar', 'Business', 'Creative'],
    status: 'stable',
  },

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: CREATIVE (3 engines, 14 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'creativity-engine',
    name: 'CreativityEngine',
    description: 'Creative process management, ideation, and iteration workflows',
    category: 'creative',
    path: '/che-nu-sdk/engines/creativity.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'ideation', name: 'IdeationEngine', description: 'Idea generation frameworks', parentEngine: 'CreativityEngine' },
      { id: 'brainstorm', name: 'BrainstormEngine', description: 'Brainstorming facilitation', parentEngine: 'CreativityEngine' },
      { id: 'iteration', name: 'IterationEngine', description: 'Creative iteration cycles', parentEngine: 'CreativityEngine' },
      { id: 'evaluation', name: 'EvaluationEngine', description: 'Creative evaluation criteria', parentEngine: 'CreativityEngine' },
    ],
    usedByAgents: ['Creative Director Agent', 'XR Scene Architect'],
    domainSpheres: ['Creative', 'Business', 'Personal'],
    status: 'stable',
  },

  {
    id: 'content-engine',
    name: 'ContentEngine',
    description: 'Content creation, strategy, storytelling, and editorial planning',
    category: 'creative',
    path: '/che-nu-sdk/engines/content.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'story', name: 'StoryEngine', description: 'Storytelling frameworks', parentEngine: 'ContentEngine' },
      { id: 'brand', name: 'BrandVoiceEngine', description: 'Brand voice definition', parentEngine: 'ContentEngine' },
      { id: 'media', name: 'MediaPlanningEngine', description: 'Media distribution planning', parentEngine: 'ContentEngine' },
      { id: 'editorial', name: 'EditorialEngine', description: 'Editorial calendar management', parentEngine: 'ContentEngine' },
      { id: 'content-strategy', name: 'ContentStrategyEngine', description: 'Content strategy frameworks', parentEngine: 'ContentEngine' },
    ],
    usedByAgents: ['Creative Director Agent', 'Communication Specialist Agent'],
    domainSpheres: ['Creative', 'Business', 'Personal'],
    status: 'stable',
  },

  {
    id: 'xr-scene-engine',
    name: 'XRSceneEngine',
    description: 'XR scene design, spatial interfaces, and immersive experience blueprinting',
    category: 'creative',
    path: '/che-nu-sdk/engines/xr-scene.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'environment', name: 'EnvironmentEngine', description: '3D environment design', parentEngine: 'XRSceneEngine' },
      { id: 'avatar', name: 'AvatarDesignEngine', description: 'Avatar customization systems', parentEngine: 'XRSceneEngine' },
      { id: 'interaction', name: 'InteractionDesignEngine', description: 'XR interaction patterns', parentEngine: 'XRSceneEngine' },
      { id: 'lighting', name: 'LightingDesignEngine', description: 'Scene lighting design', parentEngine: 'XRSceneEngine' },
      { id: 'spatial-ui', name: 'SpatialUIEngine', description: 'Spatial UI/UX design', parentEngine: 'XRSceneEngine' },
    ],
    usedByAgents: ['XR Scene Architect'],
    domainSpheres: ['XR', 'Creative', 'Business'],
    status: 'stable',
  },

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: OPERATIONAL (5 engines, 15 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'task-engine',
    name: 'TaskEngine',
    description: 'Task management, prioritization, delegation, and dependency tracking',
    category: 'operational',
    path: '/che-nu-sdk/engines/task.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'priority', name: 'PriorityEngine', description: 'Task prioritization frameworks', parentEngine: 'TaskEngine' },
      { id: 'deadline', name: 'DeadlineEngine', description: 'Deadline management', parentEngine: 'TaskEngine' },
      { id: 'delegation', name: 'DelegationEngine', description: 'Task delegation workflows', parentEngine: 'TaskEngine' },
      { id: 'dependency', name: 'DependencyEngine', description: 'Dependency tracking', parentEngine: 'TaskEngine' },
      { id: 'batching', name: 'BatchingEngine', description: 'Task batching optimization', parentEngine: 'TaskEngine' },
    ],
    usedByAgents: ['Productivity Coach', 'Project Manager Agent'],
    domainSpheres: ['Personal', 'Business', 'Projets'],
    status: 'stable',
  },

  {
    id: 'scheduling-engine',
    name: 'SchedulingEngine',
    description: 'Time management, calendar planning, and schedule optimization',
    category: 'operational',
    path: '/che-nu-sdk/engines/scheduling.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'timeblock-s', name: 'TimeBlockEngine', description: 'Time block creation', parentEngine: 'SchedulingEngine' },
      { id: 'availability', name: 'AvailabilityEngine', description: 'Availability tracking', parentEngine: 'SchedulingEngine' },
      { id: 'recurrence', name: 'RecurrenceEngine', description: 'Recurring event management', parentEngine: 'SchedulingEngine' },
      { id: 'conflict', name: 'ConflictEngine', description: 'Schedule conflict detection', parentEngine: 'SchedulingEngine' },
      { id: 'optimization-s', name: 'OptimizationEngine', description: 'Schedule optimization', parentEngine: 'SchedulingEngine' },
    ],
    usedByAgents: ['Productivity Coach', 'Project Manager Agent', 'Health Overview Agent'],
    domainSpheres: ['Personal', 'Business'],
    status: 'stable',
  },

  {
    id: 'data-engine-main',
    name: 'DataEngine',
    description: 'Data processing, transformation, quality assessment, and visualization planning',
    category: 'operational',
    path: '/che-nu-sdk/engines/data.ts',
    version: '1.0.0',
    subEngines: [
      { id: 'processing', name: 'ProcessingEngine', description: 'Data processing workflows', parentEngine: 'DataEngine' },
      { id: 'transform', name: 'TransformEngine', description: 'Data transformation logic', parentEngine: 'DataEngine' },
      { id: 'quality', name: 'QualityEngine', description: 'Data quality assessment', parentEngine: 'DataEngine' },
      { id: 'visualization-d', name: 'VisualizationEngine', description: 'Visualization design', parentEngine: 'DataEngine' },
      { id: 'pipeline', name: 'PipelineEngine', description: 'Data pipeline structuring', parentEngine: 'DataEngine' },
    ],
    usedByAgents: ['Data Analyst Agent'],
    domainSpheres: ['Business', 'Scholar', 'Personal'],
    status: 'stable',
  },

  {
    id: 'decision-engine',
    name: 'DecisionEngine',
    description: 'Decision frameworks, risk assessment, and trade-off analysis',
    category: 'operational',
    path: '/che-nu-sdk/engines/decision.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Strategy Agent', 'Finance Overview Agent'],
    domainSpheres: ['Business', 'Personal'],
    status: 'stable',
  },

  {
    id: 'goal-engine',
    name: 'GoalEngine',
    description: 'Goal setting, tracking, milestone management, and OKR frameworks',
    category: 'operational',
    path: '/che-nu-sdk/engines/goal.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Productivity Coach', 'Health Overview Agent', 'Finance Overview Agent', 'Strategy Agent', 'Knowledge Map Agent', 'Wellbeing Mentor Agent'],
    domainSpheres: ['Personal', 'Business'],
    status: 'stable',
  },

  // ═══════════════════════════════════════════════════════════
  // CATEGORY: SUPPORT (3 engines, 0 sub-engines)
  // ═══════════════════════════════════════════════════════════

  {
    id: 'memory-manager',
    name: 'MemoryManager',
    description: 'External documentary memory system for context storage',
    category: 'support',
    path: '/che-nu-sdk/engines/memory.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Research Agent'],
    domainSpheres: ['Personal', 'Business', 'Scholar'],
    status: 'stable',
  },

  {
    id: 'replay-engine',
    name: 'ReplayEngine',
    description: 'Decision replay and historical analysis',
    category: 'support',
    path: '/che-nu-sdk/engines/replay.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: [],
    domainSpheres: ['Personal', 'Business'],
    status: 'stable',
  },

  {
    id: 'document-format-engine',
    name: 'DocumentFormatEngine',
    description: 'Document formatting, export, and presentation structuring',
    category: 'support',
    path: '/che-nu-sdk/engines/document-format.ts',
    version: '1.0.0',
    subEngines: [],
    usedByAgents: ['Research Agent', 'Creative Director Agent', 'Data Analyst Agent', 'Communication Specialist Agent'],
    domainSpheres: ['Business', 'Scholar', 'Creative'],
    status: 'stable',
  },

];

// ============================================================
// REGISTRY QUERY FUNCTIONS
// ============================================================

/**
 * Get all engines
 */
export function getAllEngines(): EngineInfo[] {
  return ENGINE_REGISTRY;
}

/**
 * Get engine by ID
 */
export function getEngineById(id: string): EngineInfo | undefined {
  return ENGINE_REGISTRY.find(e => e.id === id);
}

/**
 * Get engine by name
 */
export function getEngineByName(name: string): EngineInfo | undefined {
  return ENGINE_REGISTRY.find(e => e.name === name);
}

/**
 * Get engines by category
 */
export function getEnginesByCategory(category: EngineCategory): EngineInfo[] {
  return ENGINE_REGISTRY.filter(e => e.category === category);
}

/**
 * Get engines used by a specific agent
 */
export function getEnginesForAgent(agentName: string): EngineInfo[] {
  return ENGINE_REGISTRY.filter(e => e.usedByAgents.includes(agentName));
}

/**
 * Get engines for a domain sphere
 */
export function getEnginesForSphere(sphere: string): EngineInfo[] {
  return ENGINE_REGISTRY.filter(e => e.domainSpheres.includes(sphere));
}

/**
 * Get all sub-engines
 */
export function getAllSubEngines(): SubEngineInfo[] {
  return ENGINE_REGISTRY.flatMap(e => e.subEngines);
}

/**
 * Get registry statistics
 */
export function getRegistryStats(): {
  totalEngines: number;
  totalSubEngines: number;
  byCategory: Record<string, number>;
  bySphere: Record<string, number>;
} {
  const byCategory: Record<string, number> = {};
  const bySphere: Record<string, number> = {};

  ENGINE_REGISTRY.forEach(e => {
    byCategory[e.category] = (byCategory[e.category] || 0) + 1;
    e.domainSpheres.forEach(s => {
      bySphere[s] = (bySphere[s] || 0) + 1;
    });
  });

  return {
    totalEngines: ENGINE_REGISTRY.length,
    totalSubEngines: getAllSubEngines().length,
    byCategory,
    bySphere,
  };
}

// ============================================================
// MODULE METADATA
// ============================================================

export function meta(): Record<string, unknown> {
  const stats = getRegistryStats();
  return {
    name: 'EngineRegistry',
    version: '1.0.0',
    description: 'Master registry of all CHE·NU operational engines',
    statistics: stats,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default ENGINE_REGISTRY;

============================================================
SUMMARY TABLE
============================================================

| # | Engine | Category | Sub-Engines | Agents Using |
|---|--------|----------|-------------|--------------|
| 1 | HealthEngine | personal | 5 | 1 |
| 2 | EmotionEngine | personal | 3 | 2 |
| 3 | ProductivityEngine | personal | 4 | 2 |
| 4 | ReflectionEngine | personal | 0 | 2 |
| 5 | HabitEngine | personal | 0 | 2 |
| 6 | FinanceEngine | business | 5 | 1 |
| 7 | StrategyEngine | business | 5 | 2 |
| 8 | ProjectEngine | business | 4 | 1 |
| 9 | CollaborationEngine | business | 5 | 2 |
| 10 | CommunicationEngine | business | 4 | 1 |
| 11 | RelationshipEngine | business | 0 | 2 |
| 12 | KnowledgeEngine | knowledge | 3 | 3 |
| 13 | ResearchEngine | knowledge | 5 | 1 |
| 14 | SkillEngine | knowledge | 4 | 1 |
| 15 | LearningEngine | knowledge | 0 | 1 |
| 16 | AnalysisEngine | knowledge | 3 | 4 |
| 17 | MethodologyEngine | knowledge | 0 | 5 |
| 18 | CreativityEngine | creative | 4 | 2 |
| 19 | ContentEngine | creative | 5 | 2 |
| 20 | XRSceneEngine | creative | 5 | 1 |
| 21 | TaskEngine | operational | 5 | 2 |
| 22 | SchedulingEngine | operational | 5 | 3 |
| 23 | DataEngine | operational | 5 | 1 |
| 24 | DecisionEngine | operational | 0 | 2 |
| 25 | GoalEngine | operational | 0 | 6 |
| 26 | MemoryManager | support | 0 | 1 |
| 27 | ReplayEngine | support | 0 | 0 |
| 28 | DocumentFormatEngine | support | 0 | 4 |

TOTALS:
- Engines: 28
- Sub-Engines: 67
- Categories: 6

============================================================
END OF MASTER ENGINE REGISTRY
============================================================
