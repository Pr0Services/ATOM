############################################################
#                                                          #
#       CHE·NU PROJECT & MISSION LAYER                     #
#       PART 2: PROJECT SUB-MODULES                        #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 3 — PROJECT SUB-MODULES
============================================================

--- FILE: /che-nu-sdk/core/project/goals.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Goals Sub-Engine
 * ==============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles goal structure creation and analysis for projects.
 * 
 * @module GoalsEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface GoalStructure {
  id: string;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  category: GoalCategory;
  related_engines: string[];
  success_criteria: string[];
  dependencies: string[];
  timeframe: 'immediate' | 'short_term' | 'medium_term' | 'long_term';
  measurable: boolean;
  alignment: string[];
  status: 'pending' | 'active' | 'achieved' | 'deferred' | 'abandoned';
  meta?: Record<string, unknown>;
}

export type GoalCategory = 
  | 'strategic'
  | 'operational'
  | 'financial'
  | 'growth'
  | 'learning'
  | 'health'
  | 'relationship'
  | 'creative'
  | 'technical'
  | 'other';

export interface GoalInput {
  title: string;
  description: string;
  priority?: GoalStructure['priority'];
  category?: GoalCategory;
  related_engines?: string[];
  success_criteria?: string[];
  timeframe?: GoalStructure['timeframe'];
}

export interface GoalAnalysis {
  total: number;
  by_priority: Record<string, number>;
  by_category: Record<string, number>;
  by_status: Record<string, number>;
  engines_involved: string[];
  alignment_score: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `goal_${timestamp}_${random}`;
}

// ============================================================
// GOALS ENGINE
// ============================================================

/**
 * Create a goal structure
 */
export function createGoal(input: GoalInput): GoalStructure {
  return {
    id: generateId(),
    title: input.title,
    description: input.description,
    priority: input.priority || 'medium',
    category: input.category || 'operational',
    related_engines: input.related_engines || [],
    success_criteria: input.success_criteria || [],
    dependencies: [],
    timeframe: input.timeframe || 'medium_term',
    measurable: input.success_criteria && input.success_criteria.length > 0,
    alignment: [],
    status: 'pending',
  };
}

/**
 * Add success criteria to goal
 */
export function addSuccessCriteria(
  goal: GoalStructure,
  criteria: string[]
): GoalStructure {
  goal.success_criteria = [...goal.success_criteria, ...criteria];
  goal.measurable = goal.success_criteria.length > 0;
  return goal;
}

/**
 * Add dependency between goals
 */
export function addDependency(
  goal: GoalStructure,
  dependsOnGoalId: string
): GoalStructure {
  if (!goal.dependencies.includes(dependsOnGoalId)) {
    goal.dependencies.push(dependsOnGoalId);
  }
  return goal;
}

/**
 * Map goal to engines
 */
export function mapToEngines(
  goal: GoalStructure,
  engines: string[]
): GoalStructure {
  engines.forEach(engine => {
    if (!goal.related_engines.includes(engine)) {
      goal.related_engines.push(engine);
    }
  });
  return goal;
}

/**
 * Analyze goals collection
 */
export function analyzeGoals(goals: GoalStructure[]): GoalAnalysis {
  const byPriority: Record<string, number> = {};
  const byCategory: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  const enginesSet = new Set<string>();
  
  goals.forEach(g => {
    byPriority[g.priority] = (byPriority[g.priority] || 0) + 1;
    byCategory[g.category] = (byCategory[g.category] || 0) + 1;
    byStatus[g.status] = (byStatus[g.status] || 0) + 1;
    g.related_engines.forEach(e => enginesSet.add(e));
  });
  
  // Calculate alignment score based on measurability and engine mapping
  const measurableGoals = goals.filter(g => g.measurable).length;
  const mappedGoals = goals.filter(g => g.related_engines.length > 0).length;
  const alignmentScore = goals.length > 0
    ? Math.round(((measurableGoals + mappedGoals) / (goals.length * 2)) * 100)
    : 0;
  
  return {
    total: goals.length,
    by_priority: byPriority,
    by_category: byCategory,
    by_status: byStatus,
    engines_involved: Array.from(enginesSet),
    alignment_score: alignmentScore,
  };
}

/**
 * Suggest engines based on goal category
 */
export function suggestEngines(category: GoalCategory): string[] {
  const suggestions: Record<GoalCategory, string[]> = {
    strategic: ['StrategyEngine', 'AnalysisEngine', 'DecisionEngine'],
    operational: ['TaskEngine', 'SchedulingEngine', 'ProductivityEngine'],
    financial: ['FinanceEngine', 'AnalysisEngine', 'DecisionEngine'],
    growth: ['SkillEngine', 'LearningEngine', 'GoalEngine'],
    learning: ['LearningEngine', 'KnowledgeEngine', 'SkillEngine'],
    health: ['HealthEngine', 'HabitEngine', 'EmotionEngine'],
    relationship: ['RelationshipEngine', 'CommunicationEngine', 'CollaborationEngine'],
    creative: ['CreativityEngine', 'ContentEngine', 'IdeationEngine'],
    technical: ['DataEngine', 'AnalysisEngine', 'ResearchEngine'],
    other: ['GoalEngine', 'TaskEngine'],
  };
  
  return suggestions[category] || suggestions.other;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'GoalsEngine',
    version: '1.0.0',
    description: 'Goal structure management for ProjectEngine',
    parent: 'ProjectEngine',
    path: '/che-nu-sdk/core/project/goals.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createGoal,
  addSuccessCriteria,
  addDependency,
  mapToEngines,
  analyzeGoals,
  suggestEngines,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/project/tasks.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Tasks Sub-Engine
 * ==============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles task structure creation and analysis for projects.
 * 
 * @module TasksEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface TaskStructure {
  id: string;
  name: string;
  details: string;
  complexity: 'trivial' | 'simple' | 'moderate' | 'complex' | 'epic';
  type: TaskType;
  dependencies: string[];
  blockers: string[];
  assigned_engine?: string;
  estimated_effort: EffortEstimate;
  deliverables: string[];
  acceptance_criteria: string[];
  tags: string[];
  status: 'todo' | 'in_progress' | 'blocked' | 'review' | 'done';
  meta?: Record<string, unknown>;
}

export type TaskType = 
  | 'research'
  | 'analysis'
  | 'creation'
  | 'review'
  | 'communication'
  | 'coordination'
  | 'technical'
  | 'administrative'
  | 'other';

export interface EffortEstimate {
  size: 'xs' | 's' | 'm' | 'l' | 'xl';
  confidence: 'low' | 'medium' | 'high';
  notes?: string;
}

export interface TaskInput {
  name: string;
  details: string;
  complexity?: TaskStructure['complexity'];
  type?: TaskType;
  deliverables?: string[];
  estimated_effort?: Partial<EffortEstimate>;
}

export interface TaskAnalysis {
  total: number;
  by_complexity: Record<string, number>;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  blocked_count: number;
  dependency_depth: number;
  completion_rate: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `task_${timestamp}_${random}`;
}

// ============================================================
// TASKS ENGINE
// ============================================================

/**
 * Create a task structure
 */
export function createTask(input: TaskInput): TaskStructure {
  return {
    id: generateId(),
    name: input.name,
    details: input.details,
    complexity: input.complexity || 'moderate',
    type: input.type || 'other',
    dependencies: [],
    blockers: [],
    estimated_effort: {
      size: input.estimated_effort?.size || 'm',
      confidence: input.estimated_effort?.confidence || 'medium',
      notes: input.estimated_effort?.notes,
    },
    deliverables: input.deliverables || [],
    acceptance_criteria: [],
    tags: [],
    status: 'todo',
  };
}

/**
 * Add dependency to task
 */
export function addDependency(
  task: TaskStructure,
  dependsOnTaskId: string
): TaskStructure {
  if (!task.dependencies.includes(dependsOnTaskId)) {
    task.dependencies.push(dependsOnTaskId);
  }
  return task;
}

/**
 * Add blocker to task
 */
export function addBlocker(
  task: TaskStructure,
  blockerDescription: string
): TaskStructure {
  task.blockers.push(blockerDescription);
  if (task.status !== 'done') {
    task.status = 'blocked';
  }
  return task;
}

/**
 * Remove blocker from task
 */
export function removeBlocker(
  task: TaskStructure,
  blockerIndex: number
): TaskStructure {
  if (blockerIndex >= 0 && blockerIndex < task.blockers.length) {
    task.blockers.splice(blockerIndex, 1);
    if (task.blockers.length === 0 && task.status === 'blocked') {
      task.status = 'todo';
    }
  }
  return task;
}

/**
 * Add acceptance criteria
 */
export function addAcceptanceCriteria(
  task: TaskStructure,
  criteria: string[]
): TaskStructure {
  task.acceptance_criteria = [...task.acceptance_criteria, ...criteria];
  return task;
}

/**
 * Map task to engine
 */
export function assignEngine(
  task: TaskStructure,
  engine: string
): TaskStructure {
  task.assigned_engine = engine;
  return task;
}

/**
 * Analyze tasks collection
 */
export function analyzeTasks(tasks: TaskStructure[]): TaskAnalysis {
  const byComplexity: Record<string, number> = {};
  const byType: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  let maxDepth = 0;
  
  tasks.forEach(t => {
    byComplexity[t.complexity] = (byComplexity[t.complexity] || 0) + 1;
    byType[t.type] = (byType[t.type] || 0) + 1;
    byStatus[t.status] = (byStatus[t.status] || 0) + 1;
    maxDepth = Math.max(maxDepth, t.dependencies.length);
  });
  
  const done = tasks.filter(t => t.status === 'done').length;
  const blocked = tasks.filter(t => t.status === 'blocked').length;
  
  return {
    total: tasks.length,
    by_complexity: byComplexity,
    by_type: byType,
    by_status: byStatus,
    blocked_count: blocked,
    dependency_depth: maxDepth,
    completion_rate: tasks.length > 0 ? Math.round((done / tasks.length) * 100) : 0,
  };
}

/**
 * Suggest engine based on task type
 */
export function suggestEngine(type: TaskType): string {
  const suggestions: Record<TaskType, string> = {
    research: 'ResearchEngine',
    analysis: 'AnalysisEngine',
    creation: 'CreativityEngine',
    review: 'CollaborationEngine',
    communication: 'CommunicationEngine',
    coordination: 'CollaborationEngine',
    technical: 'DataEngine',
    administrative: 'TaskEngine',
    other: 'TaskEngine',
  };
  
  return suggestions[type];
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'TasksEngine',
    version: '1.0.0',
    description: 'Task structure management for ProjectEngine',
    parent: 'ProjectEngine',
    path: '/che-nu-sdk/core/project/tasks.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createTask,
  addDependency,
  addBlocker,
  removeBlocker,
  addAcceptanceCriteria,
  assignEngine,
  analyzeTasks,
  suggestEngine,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/project/milestone.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Milestone Sub-Engine
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles milestone structure creation for projects.
 * 
 * @module MilestoneEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface MilestoneStructure {
  id: string;
  name: string;
  description: string;
  marker: string;
  due: string; // ISO date string (representational)
  criteria: string[];
  deliverables: string[];
  dependencies: string[];
  stakeholders: string[];
  type: MilestoneType;
  importance: 'critical' | 'major' | 'minor';
  status: 'upcoming' | 'at_risk' | 'reached' | 'missed';
  meta?: Record<string, unknown>;
}

export type MilestoneType = 
  | 'phase_completion'
  | 'deliverable'
  | 'decision_point'
  | 'review'
  | 'launch'
  | 'checkpoint'
  | 'other';

export interface MilestoneInput {
  name: string;
  description?: string;
  marker: string;
  due: string;
  criteria?: string[];
  type?: MilestoneType;
  importance?: MilestoneStructure['importance'];
}

export interface MilestoneTimeline {
  milestones: MilestoneStructure[];
  phases: { name: string; milestones: string[] }[];
  critical_path: string[];
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `mile_${timestamp}_${random}`;
}

// ============================================================
// MILESTONE ENGINE
// ============================================================

/**
 * Create a milestone structure
 */
export function createMilestone(input: MilestoneInput): MilestoneStructure {
  return {
    id: generateId(),
    name: input.name,
    description: input.description || '',
    marker: input.marker,
    due: input.due,
    criteria: input.criteria || [],
    deliverables: [],
    dependencies: [],
    stakeholders: [],
    type: input.type || 'checkpoint',
    importance: input.importance || 'major',
    status: 'upcoming',
  };
}

/**
 * Add criteria to milestone
 */
export function addCriteria(
  milestone: MilestoneStructure,
  criteria: string[]
): MilestoneStructure {
  milestone.criteria = [...milestone.criteria, ...criteria];
  return milestone;
}

/**
 * Add deliverable to milestone
 */
export function addDeliverable(
  milestone: MilestoneStructure,
  deliverable: string
): MilestoneStructure {
  milestone.deliverables.push(deliverable);
  return milestone;
}

/**
 * Add dependency between milestones
 */
export function addDependency(
  milestone: MilestoneStructure,
  dependsOnMilestoneId: string
): MilestoneStructure {
  if (!milestone.dependencies.includes(dependsOnMilestoneId)) {
    milestone.dependencies.push(dependsOnMilestoneId);
  }
  return milestone;
}

/**
 * Generate timeline from milestones
 */
export function generateTimeline(milestones: MilestoneStructure[]): MilestoneTimeline {
  // Sort by due date
  const sorted = [...milestones].sort((a, b) => a.due.localeCompare(b.due));
  
  // Group into phases
  const phases: { name: string; milestones: string[] }[] = [];
  let currentPhase: { name: string; milestones: string[] } | null = null;
  
  sorted.forEach(m => {
    if (m.type === 'phase_completion') {
      if (currentPhase) {
        currentPhase.milestones.push(m.id);
        phases.push(currentPhase);
      }
      currentPhase = { name: m.name, milestones: [] };
    } else if (currentPhase) {
      currentPhase.milestones.push(m.id);
    }
  });
  
  if (currentPhase && currentPhase.milestones.length > 0) {
    phases.push(currentPhase);
  }
  
  // Identify critical path (critical milestones)
  const criticalPath = sorted
    .filter(m => m.importance === 'critical')
    .map(m => m.id);
  
  return {
    milestones: sorted,
    phases,
    critical_path: criticalPath,
  };
}

/**
 * Analyze milestone health
 */
export function analyzeMilestones(milestones: MilestoneStructure[]): {
  total: number;
  by_status: Record<string, number>;
  by_importance: Record<string, number>;
  by_type: Record<string, number>;
  at_risk_count: number;
  upcoming_critical: number;
} {
  const byStatus: Record<string, number> = {};
  const byImportance: Record<string, number> = {};
  const byType: Record<string, number> = {};
  
  milestones.forEach(m => {
    byStatus[m.status] = (byStatus[m.status] || 0) + 1;
    byImportance[m.importance] = (byImportance[m.importance] || 0) + 1;
    byType[m.type] = (byType[m.type] || 0) + 1;
  });
  
  return {
    total: milestones.length,
    by_status: byStatus,
    by_importance: byImportance,
    by_type: byType,
    at_risk_count: milestones.filter(m => m.status === 'at_risk').length,
    upcoming_critical: milestones.filter(m => m.status === 'upcoming' && m.importance === 'critical').length,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'MilestoneEngine',
    version: '1.0.0',
    description: 'Milestone structure management for ProjectEngine',
    parent: 'ProjectEngine',
    path: '/che-nu-sdk/core/project/milestone.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createMilestone,
  addCriteria,
  addDeliverable,
  addDependency,
  generateTimeline,
  analyzeMilestones,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/project/resources.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Resources Sub-Engine
 * ==================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles resource structure representation for projects.
 * 
 * @module ResourcesEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface ResourceStructure {
  id: string;
  type: ResourceType;
  name: string;
  description?: string;
  quantity?: number;
  unit?: string;
  access_level: 'available' | 'limited' | 'requested' | 'unavailable' | 'unknown';
  allocation: ResourceAllocation;
  constraints: string[];
  alternatives?: string[];
  notes?: string;
  meta?: Record<string, unknown>;
}

export type ResourceType = 
  | 'human'
  | 'financial'
  | 'technical'
  | 'material'
  | 'knowledge'
  | 'time'
  | 'space'
  | 'equipment'
  | 'data'
  | 'other';

export interface ResourceAllocation {
  status: 'unallocated' | 'partial' | 'full' | 'over_allocated';
  assigned_to?: string[];
  percentage?: number;
}

export interface ResourceInput {
  type: ResourceType;
  name: string;
  description?: string;
  quantity?: number;
  unit?: string;
  access_level?: ResourceStructure['access_level'];
}

export interface ResourceAnalysis {
  total: number;
  by_type: Record<string, number>;
  by_access: Record<string, number>;
  gaps: string[];
  allocation_health: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `res_${timestamp}_${random}`;
}

// ============================================================
// RESOURCES ENGINE
// ============================================================

/**
 * Create a resource structure
 */
export function createResource(input: ResourceInput): ResourceStructure {
  return {
    id: generateId(),
    type: input.type,
    name: input.name,
    description: input.description,
    quantity: input.quantity,
    unit: input.unit,
    access_level: input.access_level || 'unknown',
    allocation: {
      status: 'unallocated',
    },
    constraints: [],
  };
}

/**
 * Set resource allocation
 */
export function setAllocation(
  resource: ResourceStructure,
  allocation: Partial<ResourceAllocation>
): ResourceStructure {
  resource.allocation = {
    ...resource.allocation,
    ...allocation,
  };
  return resource;
}

/**
 * Add constraint to resource
 */
export function addConstraint(
  resource: ResourceStructure,
  constraint: string
): ResourceStructure {
  resource.constraints.push(constraint);
  return resource;
}

/**
 * Add alternative to resource
 */
export function addAlternative(
  resource: ResourceStructure,
  alternative: string
): ResourceStructure {
  if (!resource.alternatives) {
    resource.alternatives = [];
  }
  resource.alternatives.push(alternative);
  return resource;
}

/**
 * Analyze resources collection
 */
export function analyzeResources(resources: ResourceStructure[]): ResourceAnalysis {
  const byType: Record<string, number> = {};
  const byAccess: Record<string, number> = {};
  const gaps: string[] = [];
  
  resources.forEach(r => {
    byType[r.type] = (byType[r.type] || 0) + 1;
    byAccess[r.access_level] = (byAccess[r.access_level] || 0) + 1;
    
    if (r.access_level === 'unavailable' || r.access_level === 'unknown') {
      gaps.push(`${r.type}: ${r.name}`);
    }
  });
  
  // Calculate allocation health
  const allocated = resources.filter(r => 
    r.allocation.status === 'full' || r.allocation.status === 'partial'
  ).length;
  const allocationHealth = resources.length > 0
    ? Math.round((allocated / resources.length) * 100)
    : 0;
  
  return {
    total: resources.length,
    by_type: byType,
    by_access: byAccess,
    gaps,
    allocation_health: allocationHealth,
  };
}

/**
 * Get resource requirements template
 */
export function getRequirementsTemplate(projectType: string): ResourceType[] {
  const templates: Record<string, ResourceType[]> = {
    software: ['human', 'technical', 'time', 'knowledge'],
    business: ['human', 'financial', 'time', 'data'],
    creative: ['human', 'material', 'equipment', 'space'],
    research: ['human', 'knowledge', 'data', 'time'],
    default: ['human', 'time', 'knowledge'],
  };
  
  return templates[projectType] || templates.default;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ResourcesEngine',
    version: '1.0.0',
    description: 'Resource structure management for ProjectEngine',
    parent: 'ProjectEngine',
    path: '/che-nu-sdk/core/project/resources.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createResource,
  setAllocation,
  addConstraint,
  addAlternative,
  analyzeResources,
  getRequirementsTemplate,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/project/capability.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Capability Sub-Engine
 * ===================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Maps project needs to CHE·NU engines and capabilities.
 * 
 * @module CapabilityEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface CapabilityMapping {
  project_id: string;
  engines_needed: string[];
  rationale: Record<string, EngineRationale>;
  coverage_analysis: CoverageAnalysis;
  recommendations: string[];
  gaps: string[];
}

export interface EngineRationale {
  engine: string;
  need_level: 'essential' | 'important' | 'helpful' | 'optional';
  reasons: string[];
  mapped_from: MappingSource[];
}

export interface MappingSource {
  type: 'goal' | 'task' | 'milestone' | 'context';
  id: string;
  name: string;
}

export interface CoverageAnalysis {
  total_capabilities_needed: number;
  capabilities_mapped: number;
  coverage_percentage: number;
  unmapped_areas: string[];
}

export interface CapabilityInput {
  project_id: string;
  goals: Array<{ id: string; name: string; related_engines: string[] }>;
  tasks: Array<{ id: string; name: string; assigned_engine?: string }>;
  context: {
    domain_sphere?: string;
    scale?: string;
    timeline_type?: string;
  };
}

// ============================================================
// ENGINE MAPPING DATABASE (representational)
// ============================================================

const ENGINE_CAPABILITIES: Record<string, string[]> = {
  FinanceEngine: ['budget', 'investment', 'financial planning', 'cost analysis'],
  HealthEngine: ['fitness', 'nutrition', 'wellness', 'health tracking'],
  SkillEngine: ['learning', 'skill development', 'competency mapping'],
  EmotionEngine: ['emotional awareness', 'stress management', 'resilience'],
  ProductivityEngine: ['time management', 'focus', 'habit tracking'],
  TaskEngine: ['task management', 'prioritization', 'workflow'],
  SchedulingEngine: ['calendar', 'timeline', 'scheduling'],
  CollaborationEngine: ['team coordination', 'meetings', 'handoffs'],
  CommunicationEngine: ['messaging', 'presentations', 'stakeholder engagement'],
  StrategyEngine: ['strategic planning', 'vision', 'positioning'],
  ProjectEngine: ['project planning', 'milestone tracking', 'resource management'],
  MissionEngine: ['mission planning', 'objectives', 'outcome tracking'],
  AnalysisEngine: ['data analysis', 'pattern recognition', 'insights'],
  ResearchEngine: ['research', 'source management', 'synthesis'],
  KnowledgeEngine: ['knowledge organization', 'concept mapping'],
  CreativityEngine: ['ideation', 'brainstorming', 'creative process'],
  ContentEngine: ['content creation', 'storytelling', 'editorial'],
  DataEngine: ['data processing', 'visualization', 'pipelines'],
  GoalEngine: ['goal setting', 'OKRs', 'milestone tracking'],
  XRSceneEngine: ['XR design', 'spatial interfaces', 'immersive experiences'],
};

const DOMAIN_ENGINE_MAP: Record<string, string[]> = {
  Personal: ['ProductivityEngine', 'HealthEngine', 'GoalEngine', 'HabitEngine'],
  Business: ['FinanceEngine', 'StrategyEngine', 'CollaborationEngine', 'ProjectEngine'],
  Scholar: ['ResearchEngine', 'KnowledgeEngine', 'LearningEngine', 'AnalysisEngine'],
  Creative: ['CreativityEngine', 'ContentEngine', 'XRSceneEngine'],
  Projets: ['ProjectEngine', 'TaskEngine', 'SchedulingEngine', 'CollaborationEngine'],
  MyTeam: ['CollaborationEngine', 'CommunicationEngine', 'TaskEngine'],
};

// ============================================================
// CAPABILITY ENGINE
// ============================================================

/**
 * Generate capability mapping for a project
 */
export function mapCapabilities(input: CapabilityInput): CapabilityMapping {
  const enginesNeeded = new Set<string>();
  const rationale: Record<string, EngineRationale> = {};
  
  // Map from goals
  input.goals.forEach(goal => {
    goal.related_engines.forEach(engine => {
      enginesNeeded.add(engine);
      if (!rationale[engine]) {
        rationale[engine] = {
          engine,
          need_level: 'important',
          reasons: [],
          mapped_from: [],
        };
      }
      rationale[engine].reasons.push(`Required for goal: ${goal.name}`);
      rationale[engine].mapped_from.push({
        type: 'goal',
        id: goal.id,
        name: goal.name,
      });
    });
  });
  
  // Map from tasks
  input.tasks.forEach(task => {
    if (task.assigned_engine) {
      enginesNeeded.add(task.assigned_engine);
      if (!rationale[task.assigned_engine]) {
        rationale[task.assigned_engine] = {
          engine: task.assigned_engine,
          need_level: 'important',
          reasons: [],
          mapped_from: [],
        };
      }
      rationale[task.assigned_engine].reasons.push(`Assigned to task: ${task.name}`);
      rationale[task.assigned_engine].mapped_from.push({
        type: 'task',
        id: task.id,
        name: task.name,
      });
    }
  });
  
  // Add domain-based recommendations
  const domainEngines = DOMAIN_ENGINE_MAP[input.context.domain_sphere || 'Personal'] || [];
  const recommendations: string[] = [];
  const gaps: string[] = [];
  
  domainEngines.forEach(engine => {
    if (!enginesNeeded.has(engine)) {
      recommendations.push(`Consider ${engine} for ${input.context.domain_sphere} domain`);
    }
  });
  
  // Always suggest core engines for projects
  if (!enginesNeeded.has('TaskEngine')) {
    gaps.push('Task management not covered');
    recommendations.push('Add TaskEngine for task organization');
  }
  
  if (!enginesNeeded.has('GoalEngine') && input.goals.length > 0) {
    gaps.push('Goal tracking not explicitly mapped');
    recommendations.push('Add GoalEngine for goal management');
  }
  
  // Calculate coverage
  const coverageAnalysis: CoverageAnalysis = {
    total_capabilities_needed: input.goals.length + input.tasks.length,
    capabilities_mapped: enginesNeeded.size,
    coverage_percentage: calculateCoverage(input, enginesNeeded),
    unmapped_areas: gaps,
  };
  
  return {
    project_id: input.project_id,
    engines_needed: Array.from(enginesNeeded),
    rationale,
    coverage_analysis: coverageAnalysis,
    recommendations,
    gaps,
  };
}

function calculateCoverage(input: CapabilityInput, engines: Set<string>): number {
  const totalItems = input.goals.length + input.tasks.length;
  if (totalItems === 0) return 0;
  
  let mappedItems = 0;
  input.goals.forEach(g => {
    if (g.related_engines.some(e => engines.has(e))) mappedItems++;
  });
  input.tasks.forEach(t => {
    if (t.assigned_engine && engines.has(t.assigned_engine)) mappedItems++;
  });
  
  return Math.round((mappedItems / totalItems) * 100);
}

/**
 * Get engine suggestions for a capability need
 */
export function suggestEngines(capability: string): string[] {
  const suggestions: string[] = [];
  const lowerCapability = capability.toLowerCase();
  
  Object.entries(ENGINE_CAPABILITIES).forEach(([engine, capabilities]) => {
    if (capabilities.some(c => lowerCapability.includes(c) || c.includes(lowerCapability))) {
      suggestions.push(engine);
    }
  });
  
  return suggestions;
}

/**
 * Get capabilities provided by an engine
 */
export function getEngineCapabilities(engine: string): string[] {
  return ENGINE_CAPABILITIES[engine] || [];
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'CapabilityEngine',
    version: '1.0.0',
    description: 'Capability mapping for ProjectEngine',
    parent: 'ProjectEngine',
    path: '/che-nu-sdk/core/project/capability.engine.ts',
    engines_catalogued: Object.keys(ENGINE_CAPABILITIES).length,
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  mapCapabilities,
  suggestEngines,
  getEngineCapabilities,
  meta,
};
