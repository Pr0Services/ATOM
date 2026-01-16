############################################################
#                                                          #
#       CHE·NU PROJECT & MISSION LAYER                     #
#       PART 3: MISSION SUB-MODULES & SCHEMAS              #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 4 — MISSION SUB-MODULES
============================================================

--- FILE: /che-nu-sdk/core/mission/objectives.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Objectives Sub-Engine
 * ===================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles objective structure creation for missions.
 * 
 * @module ObjectivesEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface ObjectiveStructure {
  id: string;
  statement: string;
  description?: string;
  type: ObjectiveType;
  priority: 'primary' | 'secondary' | 'optional';
  success_criteria: SuccessCriterion[];
  key_results: KeyResult[];
  related_engines: string[];
  dependencies: string[];
  alignment: string[];
  status: 'pending' | 'in_progress' | 'achieved' | 'abandoned';
  meta?: Record<string, unknown>;
}

export type ObjectiveType = 
  | 'outcome'      // Desired end state
  | 'output'       // Specific deliverable
  | 'learning'     // Knowledge/skill gain
  | 'milestone'    // Point in time achievement
  | 'maintenance'  // Sustain current state
  | 'improvement'  // Enhance existing capability
  | 'other';

export interface SuccessCriterion {
  id: string;
  criterion: string;
  measurable: boolean;
  metric?: string;
  target?: string;
  verified: boolean;
}

export interface KeyResult {
  id: string;
  description: string;
  metric: string;
  baseline?: string;
  target: string;
  current?: string;
  confidence: 'low' | 'medium' | 'high';
}

export interface ObjectiveInput {
  statement: string;
  description?: string;
  type?: ObjectiveType;
  priority?: ObjectiveStructure['priority'];
  success_criteria?: string[];
  related_engines?: string[];
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}`;
}

// ============================================================
// OBJECTIVES ENGINE
// ============================================================

/**
 * Create an objective structure
 */
export function createObjective(input: ObjectiveInput): ObjectiveStructure {
  const successCriteria: SuccessCriterion[] = (input.success_criteria || []).map(c => ({
    id: generateId('sc'),
    criterion: c,
    measurable: c.includes('%') || c.includes('number') || /\d/.test(c),
    verified: false,
  }));
  
  return {
    id: generateId('obj'),
    statement: input.statement,
    description: input.description,
    type: input.type || 'outcome',
    priority: input.priority || 'secondary',
    success_criteria: successCriteria,
    key_results: [],
    related_engines: input.related_engines || [],
    dependencies: [],
    alignment: [],
    status: 'pending',
  };
}

/**
 * Add key result to objective (OKR style)
 */
export function addKeyResult(
  objective: ObjectiveStructure,
  keyResult: Omit<KeyResult, 'id'>
): ObjectiveStructure {
  objective.key_results.push({
    ...keyResult,
    id: generateId('kr'),
  });
  return objective;
}

/**
 * Add success criterion
 */
export function addSuccessCriterion(
  objective: ObjectiveStructure,
  criterion: string,
  metric?: string
): ObjectiveStructure {
  objective.success_criteria.push({
    id: generateId('sc'),
    criterion,
    measurable: !!metric,
    metric,
    verified: false,
  });
  return objective;
}

/**
 * Map objective to engines
 */
export function mapToEngines(
  objective: ObjectiveStructure,
  engines: string[]
): ObjectiveStructure {
  engines.forEach(engine => {
    if (!objective.related_engines.includes(engine)) {
      objective.related_engines.push(engine);
    }
  });
  return objective;
}

/**
 * Analyze objectives collection
 */
export function analyzeObjectives(objectives: ObjectiveStructure[]): {
  total: number;
  by_type: Record<string, number>;
  by_priority: Record<string, number>;
  by_status: Record<string, number>;
  measurability_score: number;
  engines_involved: string[];
} {
  const byType: Record<string, number> = {};
  const byPriority: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  const enginesSet = new Set<string>();
  let measurableCount = 0;
  
  objectives.forEach(o => {
    byType[o.type] = (byType[o.type] || 0) + 1;
    byPriority[o.priority] = (byPriority[o.priority] || 0) + 1;
    byStatus[o.status] = (byStatus[o.status] || 0) + 1;
    o.related_engines.forEach(e => enginesSet.add(e));
    
    const hasMeasurable = o.success_criteria.some(sc => sc.measurable) || o.key_results.length > 0;
    if (hasMeasurable) measurableCount++;
  });
  
  return {
    total: objectives.length,
    by_type: byType,
    by_priority: byPriority,
    by_status: byStatus,
    measurability_score: objectives.length > 0 
      ? Math.round((measurableCount / objectives.length) * 100) 
      : 0,
    engines_involved: Array.from(enginesSet),
  };
}

/**
 * Suggest engines based on objective type
 */
export function suggestEngines(type: ObjectiveType): string[] {
  const suggestions: Record<ObjectiveType, string[]> = {
    outcome: ['GoalEngine', 'StrategyEngine', 'AnalysisEngine'],
    output: ['TaskEngine', 'CreativityEngine', 'ContentEngine'],
    learning: ['LearningEngine', 'SkillEngine', 'KnowledgeEngine'],
    milestone: ['SchedulingEngine', 'ProjectEngine', 'GoalEngine'],
    maintenance: ['HabitEngine', 'ProductivityEngine', 'TaskEngine'],
    improvement: ['AnalysisEngine', 'StrategyEngine', 'SkillEngine'],
    other: ['GoalEngine', 'TaskEngine'],
  };
  
  return suggestions[type] || suggestions.other;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ObjectivesEngine',
    version: '1.0.0',
    description: 'Objective structure management for MissionEngine',
    parent: 'MissionEngine',
    path: '/che-nu-sdk/core/mission/objectives.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createObjective,
  addKeyResult,
  addSuccessCriterion,
  mapToEngines,
  analyzeObjectives,
  suggestEngines,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/mission/steps.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Steps Sub-Engine
 * ==============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Handles sequential step structures for missions.
 * 
 * @module StepsEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface StepStructure {
  id: string;
  order: number;
  name: string;
  description: string;
  type: StepType;
  duration_estimate?: string;
  required_engine?: string;
  inputs: string[];
  outputs: string[];
  dependencies: string[];
  checkpoints: string[];
  decision_points: DecisionPoint[];
  status: 'pending' | 'active' | 'completed' | 'skipped' | 'blocked';
  meta?: Record<string, unknown>;
}

export type StepType = 
  | 'action'
  | 'decision'
  | 'review'
  | 'handoff'
  | 'checkpoint'
  | 'parallel'
  | 'wait'
  | 'other';

export interface DecisionPoint {
  question: string;
  options: string[];
  default_path?: string;
}

export interface StepInput {
  name: string;
  description: string;
  type?: StepType;
  duration_estimate?: string;
  required_engine?: string;
  inputs?: string[];
  outputs?: string[];
}

export interface StepSequence {
  steps: StepStructure[];
  parallel_groups: { name: string; step_ids: string[] }[];
  critical_path: string[];
  total_duration_estimate: string;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `step_${timestamp}_${random}`;
}

// ============================================================
// STEPS ENGINE
// ============================================================

/**
 * Create a step structure
 */
export function createStep(input: StepInput, order: number): StepStructure {
  return {
    id: generateId(),
    order,
    name: input.name,
    description: input.description,
    type: input.type || 'action',
    duration_estimate: input.duration_estimate,
    required_engine: input.required_engine,
    inputs: input.inputs || [],
    outputs: input.outputs || [],
    dependencies: [],
    checkpoints: [],
    decision_points: [],
    status: 'pending',
  };
}

/**
 * Create multiple steps in sequence
 */
export function createSequence(
  inputs: StepInput[],
  linkDependencies: boolean = true
): StepStructure[] {
  const steps = inputs.map((input, index) => createStep(input, index + 1));
  
  if (linkDependencies) {
    steps.forEach((step, index) => {
      if (index > 0) {
        step.dependencies.push(steps[index - 1].id);
      }
    });
  }
  
  return steps;
}

/**
 * Add dependency between steps
 */
export function addDependency(
  step: StepStructure,
  dependsOnStepId: string
): StepStructure {
  if (!step.dependencies.includes(dependsOnStepId)) {
    step.dependencies.push(dependsOnStepId);
  }
  return step;
}

/**
 * Add checkpoint to step
 */
export function addCheckpoint(
  step: StepStructure,
  checkpoint: string
): StepStructure {
  step.checkpoints.push(checkpoint);
  return step;
}

/**
 * Add decision point to step
 */
export function addDecisionPoint(
  step: StepStructure,
  decision: DecisionPoint
): StepStructure {
  step.decision_points.push(decision);
  if (step.type === 'action') {
    step.type = 'decision';
  }
  return step;
}

/**
 * Set required engine for step
 */
export function setEngine(
  step: StepStructure,
  engine: string
): StepStructure {
  step.required_engine = engine;
  return step;
}

/**
 * Generate step sequence analysis
 */
export function analyzeSequence(steps: StepStructure[]): StepSequence {
  // Sort by order
  const sorted = [...steps].sort((a, b) => a.order - b.order);
  
  // Find parallel groups (steps with same dependencies)
  const parallelGroups: { name: string; step_ids: string[] }[] = [];
  const depMap = new Map<string, string[]>();
  
  sorted.forEach(step => {
    const depKey = step.dependencies.sort().join(',');
    if (!depMap.has(depKey)) {
      depMap.set(depKey, []);
    }
    depMap.get(depKey)!.push(step.id);
  });
  
  depMap.forEach((stepIds, depKey) => {
    if (stepIds.length > 1) {
      parallelGroups.push({
        name: `Parallel after: ${depKey || 'start'}`,
        step_ids: stepIds,
      });
    }
  });
  
  // Calculate critical path (longest dependency chain)
  const criticalPath = findCriticalPath(sorted);
  
  // Estimate total duration
  const totalDuration = estimateTotalDuration(sorted);
  
  return {
    steps: sorted,
    parallel_groups: parallelGroups,
    critical_path: criticalPath,
    total_duration_estimate: totalDuration,
  };
}

function findCriticalPath(steps: StepStructure[]): string[] {
  // Simple implementation: find the longest chain
  const stepMap = new Map(steps.map(s => [s.id, s]));
  let longestPath: string[] = [];
  
  function traverse(stepId: string, path: string[]): void {
    const step = stepMap.get(stepId);
    if (!step) return;
    
    const newPath = [...path, stepId];
    if (newPath.length > longestPath.length) {
      longestPath = newPath;
    }
    
    // Find steps that depend on this one
    steps.forEach(s => {
      if (s.dependencies.includes(stepId)) {
        traverse(s.id, newPath);
      }
    });
  }
  
  // Start from steps with no dependencies
  steps
    .filter(s => s.dependencies.length === 0)
    .forEach(s => traverse(s.id, []));
  
  return longestPath;
}

function estimateTotalDuration(steps: StepStructure[]): string {
  // Sum up duration estimates (simplified)
  let totalMinutes = 0;
  
  steps.forEach(s => {
    if (s.duration_estimate) {
      const lower = s.duration_estimate.toLowerCase();
      if (lower.includes('minute')) {
        const num = parseInt(lower) || 30;
        totalMinutes += num;
      } else if (lower.includes('hour')) {
        const num = parseInt(lower) || 1;
        totalMinutes += num * 60;
      } else if (lower.includes('day')) {
        const num = parseInt(lower) || 1;
        totalMinutes += num * 480; // 8-hour day
      }
    } else {
      totalMinutes += 60; // Default 1 hour
    }
  });
  
  if (totalMinutes < 60) {
    return `${totalMinutes} minutes`;
  } else if (totalMinutes < 480) {
    return `${Math.round(totalMinutes / 60)} hours`;
  } else {
    return `${Math.round(totalMinutes / 480)} days`;
  }
}

/**
 * Suggest engine based on step type
 */
export function suggestEngine(type: StepType): string {
  const suggestions: Record<StepType, string> = {
    action: 'TaskEngine',
    decision: 'DecisionEngine',
    review: 'CollaborationEngine',
    handoff: 'CollaborationEngine',
    checkpoint: 'GoalEngine',
    parallel: 'TaskEngine',
    wait: 'SchedulingEngine',
    other: 'TaskEngine',
  };
  
  return suggestions[type];
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'StepsEngine',
    version: '1.0.0',
    description: 'Sequential step management for MissionEngine',
    parent: 'MissionEngine',
    path: '/che-nu-sdk/core/mission/steps.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  createStep,
  createSequence,
  addDependency,
  addCheckpoint,
  addDecisionPoint,
  setEngine,
  analyzeSequence,
  suggestEngine,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/mission/timeline.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Timeline Sub-Engine
 * =================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Generates mission timeline representations.
 * 
 * @module MissionTimelineEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface TimelinePhase {
  id: string;
  name: string;
  description: string;
  order: number;
  type: PhaseType;
  duration_type: 'instant' | 'short' | 'medium' | 'long';
  markers: TimelineMarker[];
  dependencies: string[];
  entries: string[]; // Step IDs in this phase
  status: 'not_started' | 'active' | 'completed';
  meta?: Record<string, unknown>;
}

export type PhaseType = 
  | 'preparation'
  | 'execution'
  | 'review'
  | 'iteration'
  | 'completion'
  | 'transition';

export interface TimelineMarker {
  id: string;
  label: string;
  type: 'start' | 'checkpoint' | 'decision' | 'deliverable' | 'end';
  position: number; // 0-100 percentage through phase
}

export interface TimelineView {
  phases: TimelinePhase[];
  total_phases: number;
  current_phase?: string;
  progress_percentage: number;
  markers: TimelineMarker[];
}

export interface TimelineInput {
  mission_name: string;
  objectives_count: number;
  steps_count: number;
  urgency: 'critical' | 'high' | 'normal' | 'low';
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}`;
}

// ============================================================
// TIMELINE ENGINE
// ============================================================

/**
 * Generate standard mission timeline
 */
export function generateTimeline(input: TimelineInput): TimelineView {
  const phases: TimelinePhase[] = [];
  
  // Phase 1: Preparation
  phases.push({
    id: generateId('phase'),
    name: 'Preparation',
    description: 'Mission setup and resource gathering',
    order: 1,
    type: 'preparation',
    duration_type: input.urgency === 'critical' ? 'instant' : 'short',
    markers: [
      { id: generateId('mk'), label: 'Mission Start', type: 'start', position: 0 },
      { id: generateId('mk'), label: 'Resources Ready', type: 'checkpoint', position: 100 },
    ],
    dependencies: [],
    entries: [],
    status: 'not_started',
  });
  
  // Phase 2: Execution (split based on steps count)
  const executionPhases = Math.ceil(input.steps_count / 3);
  for (let i = 0; i < executionPhases; i++) {
    phases.push({
      id: generateId('phase'),
      name: `Execution Phase ${i + 1}`,
      description: `Core mission activities - batch ${i + 1}`,
      order: 2 + i,
      type: 'execution',
      duration_type: 'medium',
      markers: [
        { id: generateId('mk'), label: `Phase ${i + 1} Start`, type: 'checkpoint', position: 0 },
        { id: generateId('mk'), label: `Phase ${i + 1} Complete`, type: 'deliverable', position: 100 },
      ],
      dependencies: phases.length > 0 ? [phases[phases.length - 1].id] : [],
      entries: [],
      status: 'not_started',
    });
  }
  
  // Phase 3: Review
  phases.push({
    id: generateId('phase'),
    name: 'Review',
    description: 'Assess outcomes against objectives',
    order: phases.length + 1,
    type: 'review',
    duration_type: 'short',
    markers: [
      { id: generateId('mk'), label: 'Review Start', type: 'checkpoint', position: 0 },
      { id: generateId('mk'), label: 'Outcomes Assessed', type: 'decision', position: 50 },
      { id: generateId('mk'), label: 'Review Complete', type: 'checkpoint', position: 100 },
    ],
    dependencies: [phases[phases.length - 1].id],
    entries: [],
    status: 'not_started',
  });
  
  // Phase 4: Completion
  phases.push({
    id: generateId('phase'),
    name: 'Completion',
    description: 'Mission wrap-up and documentation',
    order: phases.length + 1,
    type: 'completion',
    duration_type: 'short',
    markers: [
      { id: generateId('mk'), label: 'Completion Start', type: 'checkpoint', position: 0 },
      { id: generateId('mk'), label: 'Mission Complete', type: 'end', position: 100 },
    ],
    dependencies: [phases[phases.length - 1].id],
    entries: [],
    status: 'not_started',
  });
  
  // Collect all markers
  const allMarkers = phases.flatMap(p => p.markers);
  
  return {
    phases,
    total_phases: phases.length,
    current_phase: undefined,
    progress_percentage: 0,
    markers: allMarkers,
  };
}

/**
 * Create custom phase
 */
export function createPhase(
  name: string,
  type: PhaseType,
  order: number,
  durationTypeOverride?: TimelinePhase['duration_type']
): TimelinePhase {
  const durationMap: Record<PhaseType, TimelinePhase['duration_type']> = {
    preparation: 'short',
    execution: 'medium',
    review: 'short',
    iteration: 'medium',
    completion: 'short',
    transition: 'instant',
  };
  
  return {
    id: generateId('phase'),
    name,
    description: `${type} phase`,
    order,
    type,
    duration_type: durationTypeOverride || durationMap[type],
    markers: [],
    dependencies: [],
    entries: [],
    status: 'not_started',
  };
}

/**
 * Add marker to phase
 */
export function addMarker(
  phase: TimelinePhase,
  label: string,
  type: TimelineMarker['type'],
  position: number
): TimelinePhase {
  phase.markers.push({
    id: generateId('mk'),
    label,
    type,
    position: Math.max(0, Math.min(100, position)),
  });
  return phase;
}

/**
 * Calculate timeline progress
 */
export function calculateProgress(timeline: TimelineView): number {
  const completedPhases = timeline.phases.filter(p => p.status === 'completed').length;
  const activePhase = timeline.phases.find(p => p.status === 'active');
  
  let progress = (completedPhases / timeline.total_phases) * 100;
  
  // Add partial progress for active phase
  if (activePhase) {
    const phaseProgress = 50; // Assume 50% for active phase
    progress += (phaseProgress / 100) * (100 / timeline.total_phases);
  }
  
  return Math.round(progress);
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'MissionTimelineEngine',
    version: '1.0.0',
    description: 'Timeline generation for MissionEngine',
    parent: 'MissionEngine',
    path: '/che-nu-sdk/core/mission/timeline.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  generateTimeline,
  createPhase,
  addMarker,
  calculateProgress,
  meta,
};

============================================================

--- FILE: /che-nu-sdk/core/mission/capability_map.engine.ts
--- ACTION: CREATE NEW FILE

/**
 * CHE·NU SDK — Capability Map Sub-Engine
 * =======================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Maps mission requirements to CHE·NU engines.
 * 
 * @module MissionCapabilityMapEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

export interface MissionCapabilityMap {
  mission_id: string;
  requirements: CapabilityRequirement[];
  coverage: CoverageAssessment;
  gaps: CapabilityGap[];
  recommendations: string[];
}

export interface CapabilityRequirement {
  id: string;
  capability: string;
  engine: string;
  level: 'essential' | 'important' | 'helpful';
  source: RequirementSource;
  status: 'available' | 'limited' | 'missing';
}

export interface RequirementSource {
  type: 'objective' | 'step' | 'context';
  id: string;
  name: string;
}

export interface CoverageAssessment {
  total_requirements: number;
  covered: number;
  partially_covered: number;
  uncovered: number;
  coverage_percentage: number;
  readiness_level: 'ready' | 'needs_work' | 'not_ready';
}

export interface CapabilityGap {
  capability: string;
  severity: 'critical' | 'major' | 'minor';
  mitigation?: string;
}

export interface CapabilityMapInput {
  mission_id: string;
  objectives: Array<{ id: string; name: string; related_engines: string[] }>;
  steps: Array<{ id: string; name: string; required_engine?: string }>;
  context: {
    urgency?: string;
    scope?: string;
    domain_sphere?: string;
  };
}

// ============================================================
// CAPABILITY MAPPING DATABASE
// ============================================================

const URGENCY_ENGINE_MAP: Record<string, string[]> = {
  critical: ['TaskEngine', 'CommunicationEngine', 'DecisionEngine'],
  high: ['TaskEngine', 'SchedulingEngine'],
  normal: ['TaskEngine'],
  low: [],
};

const SCOPE_ENGINE_MAP: Record<string, string[]> = {
  focused: ['GoalEngine'],
  moderate: ['GoalEngine', 'TaskEngine'],
  broad: ['ProjectEngine', 'StrategyEngine'],
};

// ============================================================
// CAPABILITY MAP ENGINE
// ============================================================

/**
 * Generate capability map for mission
 */
export function generateCapabilityMap(input: CapabilityMapInput): MissionCapabilityMap {
  const requirements: CapabilityRequirement[] = [];
  const enginesUsed = new Set<string>();
  
  // Map from objectives
  input.objectives.forEach(obj => {
    obj.related_engines.forEach(engine => {
      enginesUsed.add(engine);
      requirements.push({
        id: `req_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 4)}`,
        capability: `Support for ${obj.name}`,
        engine,
        level: 'essential',
        source: { type: 'objective', id: obj.id, name: obj.name },
        status: 'available',
      });
    });
  });
  
  // Map from steps
  input.steps.forEach(step => {
    if (step.required_engine) {
      enginesUsed.add(step.required_engine);
      requirements.push({
        id: `req_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 4)}`,
        capability: `Execute ${step.name}`,
        engine: step.required_engine,
        level: 'important',
        source: { type: 'step', id: step.id, name: step.name },
        status: 'available',
      });
    }
  });
  
  // Add context-based requirements
  const urgencyEngines = URGENCY_ENGINE_MAP[input.context.urgency || 'normal'] || [];
  const scopeEngines = SCOPE_ENGINE_MAP[input.context.scope || 'focused'] || [];
  
  [...urgencyEngines, ...scopeEngines].forEach(engine => {
    if (!enginesUsed.has(engine)) {
      requirements.push({
        id: `req_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 4)}`,
        capability: `Context support`,
        engine,
        level: 'helpful',
        source: { type: 'context', id: 'context', name: 'Mission context' },
        status: 'available',
      });
    }
  });
  
  // Assess coverage
  const coverage = assessCoverage(requirements);
  
  // Identify gaps
  const gaps = identifyGaps(requirements, input);
  
  // Generate recommendations
  const recommendations = generateRecommendations(requirements, gaps, input);
  
  return {
    mission_id: input.mission_id,
    requirements,
    coverage,
    gaps,
    recommendations,
  };
}

function assessCoverage(requirements: CapabilityRequirement[]): CoverageAssessment {
  const total = requirements.length;
  const covered = requirements.filter(r => r.status === 'available').length;
  const partially = requirements.filter(r => r.status === 'limited').length;
  const uncovered = requirements.filter(r => r.status === 'missing').length;
  
  const percentage = total > 0 ? Math.round((covered / total) * 100) : 0;
  
  let readiness: CoverageAssessment['readiness_level'] = 'ready';
  if (percentage < 50) readiness = 'not_ready';
  else if (percentage < 80) readiness = 'needs_work';
  
  return {
    total_requirements: total,
    covered,
    partially_covered: partially,
    uncovered,
    coverage_percentage: percentage,
    readiness_level: readiness,
  };
}

function identifyGaps(
  requirements: CapabilityRequirement[],
  input: CapabilityMapInput
): CapabilityGap[] {
  const gaps: CapabilityGap[] = [];
  
  // Check for essential requirements without engines
  const essentialEngines = requirements
    .filter(r => r.level === 'essential')
    .map(r => r.engine);
  
  if (essentialEngines.length === 0 && input.objectives.length > 0) {
    gaps.push({
      capability: 'No engines mapped to objectives',
      severity: 'critical',
      mitigation: 'Map required engines to each objective',
    });
  }
  
  // Check for task execution capability
  const hasTaskEngine = requirements.some(r => r.engine === 'TaskEngine');
  if (!hasTaskEngine && input.steps.length > 3) {
    gaps.push({
      capability: 'Task management for multi-step mission',
      severity: 'major',
      mitigation: 'Add TaskEngine for step orchestration',
    });
  }
  
  return gaps;
}

function generateRecommendations(
  requirements: CapabilityRequirement[],
  gaps: CapabilityGap[],
  input: CapabilityMapInput
): string[] {
  const recommendations: string[] = [];
  
  // Based on gaps
  gaps.forEach(gap => {
    if (gap.mitigation) {
      recommendations.push(gap.mitigation);
    }
  });
  
  // Context-based recommendations
  if (input.context.urgency === 'critical') {
    recommendations.push('Consider adding DecisionEngine for rapid decision support');
  }
  
  if (input.context.scope === 'broad') {
    recommendations.push('Consider linking mission to a project for better organization');
  }
  
  return recommendations;
}

/**
 * Check if specific capability is covered
 */
export function isCapabilityCovered(
  capabilityMap: MissionCapabilityMap,
  engine: string
): boolean {
  return capabilityMap.requirements.some(
    r => r.engine === engine && r.status === 'available'
  );
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'MissionCapabilityMapEngine',
    version: '1.0.0',
    description: 'Capability mapping for MissionEngine',
    parent: 'MissionEngine',
    path: '/che-nu-sdk/core/mission/capability_map.engine.ts',
    safe: { isRepresentational: true, noAutonomy: true },
  };
}

export default {
  generateCapabilityMap,
  isCapabilityCovered,
  meta,
};

============================================================
SECTION 5 — JSON SCHEMAS
============================================================

--- FILE: /che-nu-sdk/schemas/project.schema.json
--- ACTION: CREATE NEW FILE

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.dev/schemas/project.schema.json",
  "title": "CHE·NU Project Schema",
  "description": "SAFE · REPRESENTATIONAL project structure schema",
  "type": "object",
  "required": ["id", "name", "description", "meta"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^proj_[a-z0-9]+_[a-z0-9]+$",
      "description": "Unique project identifier"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Project name"
    },
    "description": {
      "type": "string",
      "maxLength": 2000,
      "description": "Project description"
    },
    "goals": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/goal"
      },
      "description": "Project goals"
    },
    "tasks": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/task"
      },
      "description": "Project tasks"
    },
    "milestones": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/milestone"
      },
      "description": "Project milestones"
    },
    "resources": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/resource"
      },
      "description": "Project resources"
    },
    "required_engines": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Engines needed for this project"
    },
    "context": {
      "$ref": "#/definitions/context"
    },
    "linked_missions": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "IDs of linked missions"
    },
    "meta": {
      "$ref": "#/definitions/meta"
    }
  },
  "definitions": {
    "goal": {
      "type": "object",
      "required": ["id", "title", "priority", "status"],
      "properties": {
        "id": { "type": "string" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "priority": {
          "type": "string",
          "enum": ["critical", "high", "medium", "low"]
        },
        "related_engines": {
          "type": "array",
          "items": { "type": "string" }
        },
        "status": {
          "type": "string",
          "enum": ["pending", "active", "achieved", "deferred"]
        }
      }
    },
    "task": {
      "type": "object",
      "required": ["id", "name", "complexity", "status"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "details": { "type": "string" },
        "complexity": {
          "type": "string",
          "enum": ["trivial", "simple", "moderate", "complex", "epic"]
        },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assigned_engine": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["todo", "in_progress", "blocked", "done"]
        }
      }
    },
    "milestone": {
      "type": "object",
      "required": ["id", "name", "marker", "status"],
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "marker": { "type": "string" },
        "due": { "type": "string", "format": "date" },
        "criteria": {
          "type": "array",
          "items": { "type": "string" }
        },
        "status": {
          "type": "string",
          "enum": ["upcoming", "reached", "missed"]
        }
      }
    },
    "resource": {
      "type": "object",
      "required": ["id", "type", "name", "access_level"],
      "properties": {
        "id": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["human", "financial", "technical", "material", "knowledge", "time"]
        },
        "name": { "type": "string" },
        "quantity": { "type": "number" },
        "unit": { "type": "string" },
        "access_level": {
          "type": "string",
          "enum": ["available", "limited", "requested", "unknown"]
        },
        "notes": { "type": "string" }
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "domain_sphere": { "type": "string" },
        "industry": { "type": "string" },
        "scale": {
          "type": "string",
          "enum": ["personal", "team", "organization", "enterprise"]
        },
        "timeline_type": {
          "type": "string",
          "enum": ["short_term", "medium_term", "long_term"]
        },
        "risk_tolerance": {
          "type": "string",
          "enum": ["conservative", "moderate", "aggressive"]
        },
        "stakeholders": {
          "type": "array",
          "items": { "type": "string" }
        },
        "constraints": {
          "type": "array",
          "items": { "type": "string" }
        },
        "assumptions": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "meta": {
      "type": "object",
      "required": ["created", "version", "status", "safe_compliance"],
      "properties": {
        "created": { "type": "string", "format": "date-time" },
        "version": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["draft", "active", "paused", "completed", "archived"]
        },
        "safe_compliance": {
          "type": "boolean",
          "const": true
        }
      }
    }
  },
  "additionalProperties": false
}

============================================================

--- FILE: /che-nu-sdk/schemas/mission.schema.json
--- ACTION: CREATE NEW FILE

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.dev/schemas/mission.schema.json",
  "title": "CHE·NU Mission Schema",
  "description": "SAFE · REPRESENTATIONAL mission structure schema",
  "type": "object",
  "required": ["id", "name", "objective", "meta"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^miss_[a-z0-9]+_[a-z0-9]+$",
      "description": "Unique mission identifier"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Mission name"
    },
    "objective": {
      "type": "string",
      "maxLength": 1000,
      "description": "Primary mission objective"
    },
    "objectives": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/objective"
      },
      "description": "Detailed objectives"
    },
    "steps": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/step"
      },
      "description": "Sequential mission steps"
    },
    "timeline": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/timeline_entry"
      },
      "description": "Mission timeline"
    },
    "capability_map": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/capability_requirement"
      },
      "description": "Required capabilities"
    },
    "project_id": {
      "type": ["string", "null"],
      "description": "ID of linked project (if any)"
    },
    "context": {
      "$ref": "#/definitions/mission_context"
    },
    "meta": {
      "$ref": "#/definitions/meta"
    }
  },
  "definitions": {
    "objective": {
      "type": "object",
      "required": ["id", "statement", "priority", "status"],
      "properties": {
        "id": { "type": "string" },
        "statement": { "type": "string" },
        "success_criteria": {
          "type": "array",
          "items": { "type": "string" }
        },
        "priority": {
          "type": "string",
          "enum": ["primary", "secondary", "optional"]
        },
        "related_engines": {
          "type": "array",
          "items": { "type": "string" }
        },
        "status": {
          "type": "string",
          "enum": ["pending", "in_progress", "achieved", "abandoned"]
        }
      }
    },
    "step": {
      "type": "object",
      "required": ["id", "order", "name", "status"],
      "properties": {
        "id": { "type": "string" },
        "order": { "type": "integer", "minimum": 1 },
        "name": { "type": "string" },
        "description": { "type": "string" },
        "duration_estimate": { "type": "string" },
        "required_engine": { "type": "string" },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" }
        },
        "outputs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "status": {
          "type": "string",
          "enum": ["pending", "active", "completed", "skipped"]
        }
      }
    },
    "timeline_entry": {
      "type": "object",
      "required": ["id", "phase", "order", "duration_type"],
      "properties": {
        "id": { "type": "string" },
        "phase": { "type": "string" },
        "description": { "type": "string" },
        "order": { "type": "integer" },
        "duration_type": {
          "type": "string",
          "enum": ["instant", "short", "medium", "long"]
        },
        "marker": { "type": "string" },
        "dependencies": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "capability_requirement": {
      "type": "object",
      "required": ["engine", "level", "reason"],
      "properties": {
        "engine": { "type": "string" },
        "level": {
          "type": "string",
          "enum": ["essential", "important", "nice_to_have"]
        },
        "reason": { "type": "string" },
        "used_in_steps": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "mission_context": {
      "type": "object",
      "properties": {
        "urgency": {
          "type": "string",
          "enum": ["critical", "high", "normal", "low"]
        },
        "scope": {
          "type": "string",
          "enum": ["focused", "moderate", "broad"]
        },
        "domain_sphere": { "type": "string" },
        "success_definition": { "type": "string" }
      }
    },
    "meta": {
      "type": "object",
      "required": ["created", "version", "status", "safe_compliance"],
      "properties": {
        "created": { "type": "string", "format": "date-time" },
        "version": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["draft", "active", "paused", "completed", "cancelled"]
        },
        "safe_compliance": {
          "type": "boolean",
          "const": true
        }
      }
    }
  },
  "additionalProperties": false
}
