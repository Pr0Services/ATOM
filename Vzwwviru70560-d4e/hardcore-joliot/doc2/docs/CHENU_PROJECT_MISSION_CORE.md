############################################################
#                                                          #
#       CHE·NU PROJECT & MISSION LAYER                     #
#       PART 1: CORE ENGINES                               #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 1 — PROJECT ENGINE
============================================================

--- FILE: /che-nu-sdk/core/project.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Project Engine
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents CHE·NU project structures including goals,
 * tasks, milestones, resources, and engine mappings.
 * 
 * NO EXECUTION — representational only.
 * 
 * @module ProjectEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface ProjectGoal {
  id: string;
  title: string;
  description: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  related_engines: string[];
  status: 'pending' | 'active' | 'achieved' | 'deferred';
  meta?: Record<string, unknown>;
}

export interface ProjectTask {
  id: string;
  name: string;
  details: string;
  complexity: 'trivial' | 'simple' | 'moderate' | 'complex' | 'epic';
  dependencies: string[];
  assigned_engine?: string;
  status: 'todo' | 'in_progress' | 'blocked' | 'done';
  meta?: Record<string, unknown>;
}

export interface ProjectMilestone {
  id: string;
  name: string;
  marker: string;
  due: string; // ISO date string (representational)
  criteria: string[];
  status: 'upcoming' | 'reached' | 'missed';
  meta?: Record<string, unknown>;
}

export interface ProjectResource {
  id: string;
  type: 'human' | 'financial' | 'technical' | 'material' | 'knowledge' | 'time';
  name: string;
  quantity?: number;
  unit?: string;
  access_level: 'available' | 'limited' | 'requested' | 'unknown';
  notes?: string;
  meta?: Record<string, unknown>;
}

export interface ProjectContext {
  domain_sphere?: string;
  industry?: string;
  scale?: 'personal' | 'team' | 'organization' | 'enterprise';
  timeline_type?: 'short_term' | 'medium_term' | 'long_term';
  risk_tolerance?: 'conservative' | 'moderate' | 'aggressive';
  stakeholders?: string[];
  constraints?: string[];
  assumptions?: string[];
}

export interface ProjectModel {
  id: string;
  name: string;
  description: string;
  goals: ProjectGoal[];
  tasks: ProjectTask[];
  milestones: ProjectMilestone[];
  resources: ProjectResource[];
  required_engines: string[];
  context: ProjectContext;
  linked_missions: string[];
  meta: {
    created: string;
    version: string;
    status: 'draft' | 'active' | 'paused' | 'completed' | 'archived';
    safe_compliance: boolean;
  };
}

export interface ProjectInput {
  name: string;
  description: string;
  context?: Partial<ProjectContext>;
  initial_goals?: Array<Omit<ProjectGoal, 'id' | 'status'>>;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}`;
}

function getCurrentTimestamp(): string {
  return new Date().toISOString();
}

// ============================================================
// PROJECT ENGINE
// ============================================================

/**
 * Create a new project structure
 * REPRESENTATIONAL ONLY — no actual project execution
 */
export function createProject(input: ProjectInput): ProjectModel {
  const project: ProjectModel = {
    id: generateId('proj'),
    name: input.name,
    description: input.description,
    goals: [],
    tasks: [],
    milestones: [],
    resources: [],
    required_engines: [],
    context: {
      domain_sphere: input.context?.domain_sphere || 'Personal',
      industry: input.context?.industry,
      scale: input.context?.scale || 'personal',
      timeline_type: input.context?.timeline_type || 'medium_term',
      risk_tolerance: input.context?.risk_tolerance || 'moderate',
      stakeholders: input.context?.stakeholders || [],
      constraints: input.context?.constraints || [],
      assumptions: input.context?.assumptions || [],
    },
    linked_missions: [],
    meta: {
      created: getCurrentTimestamp(),
      version: '1.0.0',
      status: 'draft',
      safe_compliance: true,
    },
  };

  // Add initial goals if provided
  if (input.initial_goals) {
    input.initial_goals.forEach(g => {
      addGoal(project, g);
    });
  }

  return project;
}

/**
 * Add a goal to a project
 */
export function addGoal(
  project: ProjectModel,
  goal: Omit<ProjectGoal, 'id' | 'status'>
): ProjectModel {
  const newGoal: ProjectGoal = {
    ...goal,
    id: generateId('goal'),
    status: 'pending',
  };
  
  project.goals.push(newGoal);
  
  // Update required engines based on goal
  goal.related_engines.forEach(engine => {
    if (!project.required_engines.includes(engine)) {
      project.required_engines.push(engine);
    }
  });
  
  return project;
}

/**
 * Add a task to a project
 */
export function addTask(
  project: ProjectModel,
  task: Omit<ProjectTask, 'id' | 'status'>
): ProjectModel {
  const newTask: ProjectTask = {
    ...task,
    id: generateId('task'),
    status: 'todo',
  };
  
  project.tasks.push(newTask);
  
  // Update required engines if task has assigned engine
  if (task.assigned_engine && !project.required_engines.includes(task.assigned_engine)) {
    project.required_engines.push(task.assigned_engine);
  }
  
  return project;
}

/**
 * Add a milestone to a project
 */
export function addMilestone(
  project: ProjectModel,
  milestone: Omit<ProjectMilestone, 'id' | 'status'>
): ProjectModel {
  const newMilestone: ProjectMilestone = {
    ...milestone,
    id: generateId('mile'),
    status: 'upcoming',
  };
  
  project.milestones.push(newMilestone);
  return project;
}

/**
 * Add a resource to a project
 */
export function addResource(
  project: ProjectModel,
  resource: Omit<ProjectResource, 'id'>
): ProjectModel {
  const newResource: ProjectResource = {
    ...resource,
    id: generateId('res'),
  };
  
  project.resources.push(newResource);
  return project;
}

/**
 * Map capabilities to project based on goals and tasks
 * Returns analysis of which engines are needed
 */
export function mapCapabilitiesToProject(project: ProjectModel): {
  engines_needed: string[];
  engine_rationale: Record<string, string>;
  coverage_gaps: string[];
  recommendations: string[];
} {
  const engineRationale: Record<string, string> = {};
  const allEngines = new Set<string>();
  
  // Collect engines from goals
  project.goals.forEach(goal => {
    goal.related_engines.forEach(engine => {
      allEngines.add(engine);
      engineRationale[engine] = engineRationale[engine] 
        ? `${engineRationale[engine]}; Goal: ${goal.title}`
        : `Goal: ${goal.title}`;
    });
  });
  
  // Collect engines from tasks
  project.tasks.forEach(task => {
    if (task.assigned_engine) {
      allEngines.add(task.assigned_engine);
      engineRationale[task.assigned_engine] = engineRationale[task.assigned_engine]
        ? `${engineRationale[task.assigned_engine]}; Task: ${task.name}`
        : `Task: ${task.name}`;
    }
  });
  
  // Analyze coverage gaps based on context
  const coverageGaps: string[] = [];
  const recommendations: string[] = [];
  
  // Domain-based recommendations
  if (project.context.domain_sphere === 'Business' && !allEngines.has('FinanceEngine')) {
    coverageGaps.push('Financial planning not mapped');
    recommendations.push('Consider adding FinanceEngine for budget tracking');
  }
  
  if (project.context.scale === 'team' && !allEngines.has('CollaborationEngine')) {
    coverageGaps.push('Team collaboration not mapped');
    recommendations.push('Consider adding CollaborationEngine for team coordination');
  }
  
  if (project.tasks.length > 5 && !allEngines.has('TaskEngine')) {
    coverageGaps.push('Task management not mapped');
    recommendations.push('Consider adding TaskEngine for task organization');
  }
  
  if (project.milestones.length > 0 && !allEngines.has('SchedulingEngine')) {
    coverageGaps.push('Timeline management not mapped');
    recommendations.push('Consider adding SchedulingEngine for milestone tracking');
  }
  
  return {
    engines_needed: Array.from(allEngines),
    engine_rationale: engineRationale,
    coverage_gaps: coverageGaps,
    recommendations: recommendations,
  };
}

/**
 * Generate project summary
 */
export function summarizeProject(project: ProjectModel): {
  overview: string;
  statistics: Record<string, number>;
  health_indicators: Record<string, string>;
  capability_coverage: number;
} {
  const totalGoals = project.goals.length;
  const achievedGoals = project.goals.filter(g => g.status === 'achieved').length;
  const totalTasks = project.tasks.length;
  const completedTasks = project.tasks.filter(t => t.status === 'done').length;
  const blockedTasks = project.tasks.filter(t => t.status === 'blocked').length;
  const totalMilestones = project.milestones.length;
  const reachedMilestones = project.milestones.filter(m => m.status === 'reached').length;
  
  // Calculate capability coverage
  const capabilityMap = mapCapabilitiesToProject(project);
  const coverage = capabilityMap.coverage_gaps.length === 0 ? 100 : 
    Math.max(0, 100 - (capabilityMap.coverage_gaps.length * 20));
  
  return {
    overview: `Project "${project.name}": ${totalGoals} goals, ${totalTasks} tasks, ${totalMilestones} milestones. Status: ${project.meta.status}.`,
    statistics: {
      total_goals: totalGoals,
      achieved_goals: achievedGoals,
      total_tasks: totalTasks,
      completed_tasks: completedTasks,
      blocked_tasks: blockedTasks,
      total_milestones: totalMilestones,
      reached_milestones: reachedMilestones,
      total_resources: project.resources.length,
      engines_mapped: project.required_engines.length,
    },
    health_indicators: {
      goal_progress: totalGoals > 0 ? `${Math.round((achievedGoals / totalGoals) * 100)}%` : 'N/A',
      task_progress: totalTasks > 0 ? `${Math.round((completedTasks / totalTasks) * 100)}%` : 'N/A',
      milestone_progress: totalMilestones > 0 ? `${Math.round((reachedMilestones / totalMilestones) * 100)}%` : 'N/A',
      blocked_status: blockedTasks > 0 ? `${blockedTasks} tasks blocked` : 'No blockers',
    },
    capability_coverage: coverage,
  };
}

/**
 * Link a mission to this project
 */
export function linkMission(project: ProjectModel, missionId: string): ProjectModel {
  if (!project.linked_missions.includes(missionId)) {
    project.linked_missions.push(missionId);
  }
  return project;
}

/**
 * Clone a project as template
 */
export function cloneAsTemplate(project: ProjectModel): ProjectModel {
  return {
    ...project,
    id: generateId('proj'),
    name: `${project.name} (Template)`,
    goals: project.goals.map(g => ({ ...g, id: generateId('goal'), status: 'pending' as const })),
    tasks: project.tasks.map(t => ({ ...t, id: generateId('task'), status: 'todo' as const })),
    milestones: project.milestones.map(m => ({ ...m, id: generateId('mile'), status: 'upcoming' as const })),
    resources: project.resources.map(r => ({ ...r, id: generateId('res') })),
    linked_missions: [],
    meta: {
      ...project.meta,
      created: getCurrentTimestamp(),
      status: 'draft',
    },
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ProjectEngine',
    version: '1.0.0',
    description: 'Representational project structure engine for CHE·NU',
    category: 'core',
    path: '/che-nu-sdk/core/project.ts',
    methods: [
      'createProject',
      'addGoal',
      'addTask',
      'addMilestone',
      'addResource',
      'mapCapabilitiesToProject',
      'summarizeProject',
      'linkMission',
      'cloneAsTemplate',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
    prohibited: [
      'Real project management advice',
      'Actual deadline calculation',
      'Resource allocation execution',
      'Risk assessment with real consequences',
    ],
    allowed: [
      'Structural project models',
      'Abstract goal/task representations',
      'Capability mapping',
      'Symbolic milestone tracking',
    ],
  };
}

export default {
  createProject,
  addGoal,
  addTask,
  addMilestone,
  addResource,
  mapCapabilitiesToProject,
  summarizeProject,
  linkMission,
  cloneAsTemplate,
  meta,
};

============================================================
SECTION 2 — MISSION ENGINE
============================================================

--- FILE: /che-nu-sdk/core/mission.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Mission Engine
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents focused, time-bound, outcome-driven mission units.
 * Missions are smaller than projects and have clear objectives.
 * 
 * NO EXECUTION — representational only.
 * 
 * @module MissionEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface MissionObjective {
  id: string;
  statement: string;
  success_criteria: string[];
  priority: 'primary' | 'secondary' | 'optional';
  related_engines: string[];
  status: 'pending' | 'in_progress' | 'achieved' | 'abandoned';
  meta?: Record<string, unknown>;
}

export interface MissionStep {
  id: string;
  order: number;
  name: string;
  description: string;
  duration_estimate?: string; // e.g., "2 hours", "1 day" (representational)
  required_engine?: string;
  dependencies: string[];
  outputs: string[];
  status: 'pending' | 'active' | 'completed' | 'skipped';
  meta?: Record<string, unknown>;
}

export interface TimelineEntry {
  id: string;
  phase: string;
  description: string;
  order: number;
  duration_type: 'instant' | 'short' | 'medium' | 'long';
  marker?: string;
  dependencies: string[];
  meta?: Record<string, unknown>;
}

export interface CapabilityRequirement {
  engine: string;
  level: 'essential' | 'important' | 'nice_to_have';
  reason: string;
  used_in_steps: string[];
}

export interface MissionModel {
  id: string;
  name: string;
  objective: string;
  objectives: MissionObjective[];
  steps: MissionStep[];
  timeline: TimelineEntry[];
  capability_map: CapabilityRequirement[];
  project_id: string | null;
  context: {
    urgency: 'critical' | 'high' | 'normal' | 'low';
    scope: 'focused' | 'moderate' | 'broad';
    domain_sphere?: string;
    success_definition?: string;
  };
  meta: {
    created: string;
    version: string;
    status: 'draft' | 'active' | 'paused' | 'completed' | 'cancelled';
    safe_compliance: boolean;
  };
}

export interface MissionInput {
  name: string;
  objective: string;
  urgency?: 'critical' | 'high' | 'normal' | 'low';
  scope?: 'focused' | 'moderate' | 'broad';
  domain_sphere?: string;
  project_id?: string;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}`;
}

function getCurrentTimestamp(): string {
  return new Date().toISOString();
}

// ============================================================
// MISSION ENGINE
// ============================================================

/**
 * Create a new mission structure
 * REPRESENTATIONAL ONLY — no actual mission execution
 */
export function createMission(input: MissionInput): MissionModel {
  return {
    id: generateId('miss'),
    name: input.name,
    objective: input.objective,
    objectives: [],
    steps: [],
    timeline: [],
    capability_map: [],
    project_id: input.project_id || null,
    context: {
      urgency: input.urgency || 'normal',
      scope: input.scope || 'focused',
      domain_sphere: input.domain_sphere,
      success_definition: undefined,
    },
    meta: {
      created: getCurrentTimestamp(),
      version: '1.0.0',
      status: 'draft',
      safe_compliance: true,
    },
  };
}

/**
 * Define objectives for a mission
 */
export function defineObjectives(
  mission: MissionModel,
  objectives: Array<Omit<MissionObjective, 'id' | 'status'>>
): MissionModel {
  const newObjectives: MissionObjective[] = objectives.map((obj, index) => ({
    ...obj,
    id: generateId('obj'),
    status: 'pending',
    priority: obj.priority || (index === 0 ? 'primary' : 'secondary'),
  }));
  
  mission.objectives = [...mission.objectives, ...newObjectives];
  
  // Update capability map based on objectives
  newObjectives.forEach(obj => {
    obj.related_engines.forEach(engine => {
      const existing = mission.capability_map.find(c => c.engine === engine);
      if (!existing) {
        mission.capability_map.push({
          engine,
          level: obj.priority === 'primary' ? 'essential' : 'important',
          reason: `Required for objective: ${obj.statement}`,
          used_in_steps: [],
        });
      }
    });
  });
  
  return mission;
}

/**
 * Define steps for a mission
 */
export function defineSteps(
  mission: MissionModel,
  steps: Array<Omit<MissionStep, 'id' | 'status' | 'order'>>
): MissionModel {
  const startOrder = mission.steps.length;
  
  const newSteps: MissionStep[] = steps.map((step, index) => ({
    ...step,
    id: generateId('step'),
    order: startOrder + index + 1,
    status: 'pending',
  }));
  
  mission.steps = [...mission.steps, ...newSteps];
  
  // Update capability map based on steps
  newSteps.forEach(step => {
    if (step.required_engine) {
      const existing = mission.capability_map.find(c => c.engine === step.required_engine);
      if (existing) {
        existing.used_in_steps.push(step.id);
      } else {
        mission.capability_map.push({
          engine: step.required_engine,
          level: 'important',
          reason: `Required for step: ${step.name}`,
          used_in_steps: [step.id],
        });
      }
    }
  });
  
  return mission;
}

/**
 * Generate mission timeline
 */
export function missionTimeline(mission: MissionModel): MissionModel {
  // Generate timeline entries from steps
  const timelineEntries: TimelineEntry[] = [];
  
  // Add preparation phase
  timelineEntries.push({
    id: generateId('tl'),
    phase: 'Preparation',
    description: 'Mission setup and resource gathering',
    order: 0,
    duration_type: 'short',
    dependencies: [],
  });
  
  // Add execution phases from steps
  mission.steps.forEach((step, index) => {
    timelineEntries.push({
      id: generateId('tl'),
      phase: `Step ${step.order}: ${step.name}`,
      description: step.description,
      order: index + 1,
      duration_type: getDurationType(step.duration_estimate),
      marker: step.outputs.length > 0 ? `Output: ${step.outputs[0]}` : undefined,
      dependencies: step.dependencies,
    });
  });
  
  // Add completion phase
  timelineEntries.push({
    id: generateId('tl'),
    phase: 'Completion',
    description: 'Mission review and outcome assessment',
    order: timelineEntries.length,
    duration_type: 'short',
    dependencies: mission.steps.map(s => s.id),
  });
  
  mission.timeline = timelineEntries;
  return mission;
}

function getDurationType(estimate?: string): TimelineEntry['duration_type'] {
  if (!estimate) return 'short';
  const lower = estimate.toLowerCase();
  if (lower.includes('minute') || lower.includes('instant')) return 'instant';
  if (lower.includes('hour') || lower.includes('short')) return 'short';
  if (lower.includes('day') || lower.includes('medium')) return 'medium';
  return 'long';
}

/**
 * Get mission capabilities analysis
 */
export function missionCapabilities(mission: MissionModel): {
  required: CapabilityRequirement[];
  coverage_score: number;
  gaps: string[];
  suggestions: string[];
} {
  const gaps: string[] = [];
  const suggestions: string[] = [];
  
  // Check for common capability needs based on mission context
  if (mission.context.urgency === 'critical' && !hasEngine(mission, 'TaskEngine')) {
    gaps.push('No task management for critical mission');
    suggestions.push('Add TaskEngine for priority handling');
  }
  
  if (mission.steps.length > 5 && !hasEngine(mission, 'SchedulingEngine')) {
    gaps.push('Multi-step mission without scheduling');
    suggestions.push('Add SchedulingEngine for timeline management');
  }
  
  if (mission.context.scope === 'broad' && !hasEngine(mission, 'ProjectEngine')) {
    gaps.push('Broad scope mission may benefit from project structure');
    suggestions.push('Consider linking to a project');
  }
  
  // Calculate coverage score
  const essentialCount = mission.capability_map.filter(c => c.level === 'essential').length;
  const totalNeeded = mission.capability_map.length;
  const coverage = totalNeeded > 0 
    ? Math.round((essentialCount / Math.max(1, mission.objectives.length)) * 100)
    : 0;
  
  return {
    required: mission.capability_map,
    coverage_score: Math.min(100, coverage),
    gaps,
    suggestions,
  };
}

function hasEngine(mission: MissionModel, engine: string): boolean {
  return mission.capability_map.some(c => c.engine === engine);
}

/**
 * Link mission to a project
 */
export function linkProject(mission: MissionModel, projectId: string): MissionModel {
  mission.project_id = projectId;
  return mission;
}

/**
 * Unlink mission from project
 */
export function unlinkProject(mission: MissionModel): MissionModel {
  mission.project_id = null;
  return mission;
}

/**
 * Get mission summary
 */
export function summarizeMission(mission: MissionModel): {
  overview: string;
  statistics: Record<string, number>;
  status_breakdown: Record<string, number>;
  readiness: string;
} {
  const totalObjectives = mission.objectives.length;
  const achievedObjectives = mission.objectives.filter(o => o.status === 'achieved').length;
  const totalSteps = mission.steps.length;
  const completedSteps = mission.steps.filter(s => s.status === 'completed').length;
  
  // Calculate readiness
  let readiness = 'Not ready';
  if (mission.objectives.length > 0 && mission.steps.length > 0 && mission.capability_map.length > 0) {
    readiness = 'Ready for execution';
  } else if (mission.objectives.length > 0) {
    readiness = 'Needs steps defined';
  } else {
    readiness = 'Needs objectives';
  }
  
  return {
    overview: `Mission "${mission.name}": ${mission.objective}. Status: ${mission.meta.status}. Urgency: ${mission.context.urgency}.`,
    statistics: {
      total_objectives: totalObjectives,
      achieved_objectives: achievedObjectives,
      total_steps: totalSteps,
      completed_steps: completedSteps,
      timeline_entries: mission.timeline.length,
      capabilities_mapped: mission.capability_map.length,
      linked_to_project: mission.project_id ? 1 : 0,
    },
    status_breakdown: {
      objectives_pending: mission.objectives.filter(o => o.status === 'pending').length,
      objectives_in_progress: mission.objectives.filter(o => o.status === 'in_progress').length,
      objectives_achieved: achievedObjectives,
      steps_pending: mission.steps.filter(s => s.status === 'pending').length,
      steps_active: mission.steps.filter(s => s.status === 'active').length,
      steps_completed: completedSteps,
    },
    readiness,
  };
}

/**
 * Clone mission as template
 */
export function cloneAsTemplate(mission: MissionModel): MissionModel {
  return {
    ...mission,
    id: generateId('miss'),
    name: `${mission.name} (Template)`,
    objectives: mission.objectives.map(o => ({ ...o, id: generateId('obj'), status: 'pending' as const })),
    steps: mission.steps.map(s => ({ ...s, id: generateId('step'), status: 'pending' as const })),
    timeline: [],
    project_id: null,
    meta: {
      ...mission.meta,
      created: getCurrentTimestamp(),
      status: 'draft',
    },
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'MissionEngine',
    version: '1.0.0',
    description: 'Representational mission structure engine for CHE·NU',
    category: 'core',
    path: '/che-nu-sdk/core/mission.ts',
    methods: [
      'createMission',
      'defineObjectives',
      'defineSteps',
      'missionTimeline',
      'missionCapabilities',
      'linkProject',
      'unlinkProject',
      'summarizeMission',
      'cloneAsTemplate',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
    prohibited: [
      'Real mission planning advice',
      'Actual timeline calculation',
      'Resource allocation execution',
      'Strategic decision making',
    ],
    allowed: [
      'Structural mission models',
      'Abstract objective representations',
      'Capability mapping',
      'Symbolic timeline generation',
    ],
  };
}

export default {
  createMission,
  defineObjectives,
  defineSteps,
  missionTimeline,
  missionCapabilities,
  linkProject,
  unlinkProject,
  summarizeMission,
  cloneAsTemplate,
  meta,
};
