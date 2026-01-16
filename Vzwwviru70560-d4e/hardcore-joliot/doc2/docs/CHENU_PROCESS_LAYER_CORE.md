############################################################
#                                                          #
#       CHE·NU PROCESS LAYER (PIPELINE SYSTEM)             #
#       PART 1: CORE ENGINE + SUB-ENGINES                  #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION 1 — CORE MODULE: ProcessEngine
============================================================

--- FILE: /che-nu-sdk/core/process.ts

/**
 * CHE·NU SDK — Process Engine
 * ============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents process structures, pipelines, and workflows.
 * NO real execution — structure only.
 * 
 * CLASSIFICATION: REPRESENTATIONAL ONLY
 * - No actual task execution
 * - No real automation
 * - No actionable workflows
 * - Structures describe process models only
 * 
 * @module ProcessEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Process step status
 */
export type StepStatus = 'pending' | 'in_progress' | 'complete' | 'blocked' | 'skipped';

/**
 * Process model status
 */
export type ProcessStatus = 'draft' | 'active' | 'paused' | 'complete' | 'archived';

/**
 * Process step definition
 */
export interface ProcessStep {
  id: string;
  name: string;
  description: string;
  order: number;
  required_engines: string[];
  suggested_agents: string[];
  inputs: StepIO[];
  outputs: StepIO[];
  estimated_duration?: string;  // representational only
  dependencies: string[];       // step IDs
  tags: string[];
  metadata: Record<string, unknown>;
}

/**
 * Step input/output definition
 */
export interface StepIO {
  name: string;
  type: string;       // 'data', 'document', 'object', 'decision', 'approval'
  description: string;
  required: boolean;
  schema?: string;    // optional schema reference
}

/**
 * Process transition definition
 */
export interface ProcessTransition {
  id: string;
  from: string;       // step ID or 'START'
  to: string;         // step ID or 'END'
  condition: string;  // representational condition description
  type: 'sequential' | 'conditional' | 'parallel' | 'loop';
  weight: number;     // probability/priority (representational)
  metadata: Record<string, unknown>;
}

/**
 * Process state representation
 */
export interface ProcessState {
  id: string;
  step_id: string;
  description: string;
  status: StepStatus;
  entered_at: string;  // representational timestamp
  context: Record<string, unknown>;
  metadata: Record<string, unknown>;
}

/**
 * Complete process model
 */
export interface ProcessModel {
  id: string;
  name: string;
  description: string;
  version: string;
  category: string;
  steps: ProcessStep[];
  transitions: ProcessTransition[];
  states: ProcessState[];
  context: ProcessContext;
  metadata: {
    created_at: string;
    updated_at: string;
    author?: string;
    template_source?: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
    noPersistence: true;
  };
}

/**
 * Process execution context (representational)
 */
export interface ProcessContext {
  sphere?: string;
  project_id?: string;
  mission_id?: string;
  owner_agent?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  tags: string[];
  variables: Record<string, unknown>;
}

/**
 * Process creation input
 */
export interface CreateProcessInput {
  name: string;
  description?: string;
  category?: string;
  context?: Partial<ProcessContext>;
}

/**
 * Process summary
 */
export interface ProcessSummary {
  id: string;
  name: string;
  category: string;
  status: ProcessStatus;
  total_steps: number;
  total_transitions: number;
  engines_required: string[];
  estimated_complexity: 'simple' | 'moderate' | 'complex';
}

/**
 * Engine mapping result
 */
export interface EngineMapping {
  process_id: string;
  engines: {
    engine_name: string;
    used_in_steps: string[];
    count: number;
  }[];
  total_engines: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateProcessId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `proc_${timestamp}_${random}`;
}

function generateStepId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `step_${timestamp}_${random}`;
}

function generateTransitionId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `trans_${timestamp}_${random}`;
}

function generateStateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `state_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Create a new process model
 * REPRESENTATIONAL ONLY — no actual process execution
 */
export function createProcess(input: CreateProcessInput): ProcessModel {
  const timestamp = now();
  
  const process: ProcessModel = {
    id: generateProcessId(),
    name: input.name,
    description: input.description || '',
    version: '1.0.0',
    category: input.category || 'general',
    steps: [],
    transitions: [],
    states: [],
    context: {
      sphere: input.context?.sphere,
      project_id: input.context?.project_id,
      mission_id: input.context?.mission_id,
      owner_agent: input.context?.owner_agent,
      priority: input.context?.priority || 'medium',
      tags: input.context?.tags || [],
      variables: input.context?.variables || {},
    },
    metadata: {
      created_at: timestamp,
      updated_at: timestamp,
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
  };
  
  return process;
}

/**
 * Add a step to the process
 */
export function addStep(
  process: ProcessModel,
  step: Omit<ProcessStep, 'id' | 'order'>
): ProcessModel {
  const newStep: ProcessStep = {
    ...step,
    id: generateStepId(),
    order: process.steps.length + 1,
  };
  
  process.steps.push(newStep);
  process.metadata.updated_at = now();
  
  return process;
}

/**
 * Remove a step from the process
 */
export function removeStep(process: ProcessModel, stepId: string): ProcessModel {
  process.steps = process.steps.filter(s => s.id !== stepId);
  
  // Remove related transitions
  process.transitions = process.transitions.filter(
    t => t.from !== stepId && t.to !== stepId
  );
  
  // Remove related states
  process.states = process.states.filter(s => s.step_id !== stepId);
  
  // Reorder remaining steps
  process.steps.forEach((step, index) => {
    step.order = index + 1;
  });
  
  process.metadata.updated_at = now();
  
  return process;
}

/**
 * Update a step
 */
export function updateStep(
  process: ProcessModel,
  stepId: string,
  updates: Partial<ProcessStep>
): ProcessModel {
  const stepIndex = process.steps.findIndex(s => s.id === stepId);
  
  if (stepIndex !== -1) {
    process.steps[stepIndex] = {
      ...process.steps[stepIndex],
      ...updates,
      id: stepId, // preserve ID
    };
    process.metadata.updated_at = now();
  }
  
  return process;
}

/**
 * Add a transition between steps
 */
export function addTransition(
  process: ProcessModel,
  transition: Omit<ProcessTransition, 'id'>
): ProcessModel {
  const newTransition: ProcessTransition = {
    ...transition,
    id: generateTransitionId(),
  };
  
  process.transitions.push(newTransition);
  process.metadata.updated_at = now();
  
  return process;
}

/**
 * Remove a transition
 */
export function removeTransition(process: ProcessModel, transitionId: string): ProcessModel {
  process.transitions = process.transitions.filter(t => t.id !== transitionId);
  process.metadata.updated_at = now();
  return process;
}

/**
 * Initialize process states from steps
 * REPRESENTATIONAL — creates state structure only
 */
export function initializeStates(process: ProcessModel): ProcessState[] {
  const states: ProcessState[] = process.steps.map(step => ({
    id: generateStateId(),
    step_id: step.id,
    description: `State for: ${step.name}`,
    status: 'pending',
    entered_at: now(),
    context: {},
    metadata: {},
  }));
  
  process.states = states;
  process.metadata.updated_at = now();
  
  return states;
}

/**
 * Update a state (representational only)
 */
export function updateState(
  process: ProcessModel,
  stateId: string,
  newStatus: StepStatus,
  context?: Record<string, unknown>
): ProcessModel {
  const stateIndex = process.states.findIndex(s => s.id === stateId);
  
  if (stateIndex !== -1) {
    process.states[stateIndex].status = newStatus;
    process.states[stateIndex].entered_at = now();
    if (context) {
      process.states[stateIndex].context = {
        ...process.states[stateIndex].context,
        ...context,
      };
    }
    process.metadata.updated_at = now();
  }
  
  return process;
}

/**
 * Get process status based on states
 */
export function getProcessStatus(process: ProcessModel): ProcessStatus {
  if (process.states.length === 0) return 'draft';
  
  const allComplete = process.states.every(s => s.status === 'complete');
  if (allComplete) return 'complete';
  
  const anyInProgress = process.states.some(s => s.status === 'in_progress');
  if (anyInProgress) return 'active';
  
  const anyBlocked = process.states.some(s => s.status === 'blocked');
  if (anyBlocked) return 'paused';
  
  return 'active';
}

/**
 * Summarize process
 */
export function summarizeProcess(process: ProcessModel): ProcessSummary {
  // Collect all required engines
  const enginesSet = new Set<string>();
  process.steps.forEach(step => {
    step.required_engines.forEach(e => enginesSet.add(e));
  });
  
  // Estimate complexity
  let complexity: 'simple' | 'moderate' | 'complex' = 'simple';
  if (process.steps.length > 10 || process.transitions.length > 15) {
    complexity = 'complex';
  } else if (process.steps.length > 5 || process.transitions.length > 7) {
    complexity = 'moderate';
  }
  
  return {
    id: process.id,
    name: process.name,
    category: process.category,
    status: getProcessStatus(process),
    total_steps: process.steps.length,
    total_transitions: process.transitions.length,
    engines_required: Array.from(enginesSet),
    estimated_complexity: complexity,
  };
}

/**
 * Map engines used in process
 */
export function mapEngines(process: ProcessModel): EngineMapping {
  const engineMap = new Map<string, string[]>();
  
  process.steps.forEach(step => {
    step.required_engines.forEach(engine => {
      const steps = engineMap.get(engine) || [];
      steps.push(step.id);
      engineMap.set(engine, steps);
    });
  });
  
  return {
    process_id: process.id,
    engines: Array.from(engineMap.entries()).map(([engine_name, used_in_steps]) => ({
      engine_name,
      used_in_steps,
      count: used_in_steps.length,
    })),
    total_engines: engineMap.size,
  };
}

/**
 * Get step dependencies graph
 */
export function getDependencyGraph(process: ProcessModel): {
  nodes: { id: string; label: string }[];
  edges: { from: string; to: string; type: string }[];
} {
  const nodes = process.steps.map(step => ({
    id: step.id,
    label: step.name,
  }));
  
  const edges: { from: string; to: string; type: string }[] = [];
  
  // Add dependency edges
  process.steps.forEach(step => {
    step.dependencies.forEach(depId => {
      edges.push({
        from: depId,
        to: step.id,
        type: 'dependency',
      });
    });
  });
  
  // Add transition edges
  process.transitions.forEach(trans => {
    if (trans.from !== 'START' && trans.to !== 'END') {
      edges.push({
        from: trans.from,
        to: trans.to,
        type: trans.type,
      });
    }
  });
  
  return { nodes, edges };
}

/**
 * Clone process as template
 */
export function cloneProcess(process: ProcessModel, newName: string): ProcessModel {
  const cloned = createProcess({
    name: newName,
    description: `Cloned from: ${process.name}`,
    category: process.category,
    context: { ...process.context },
  });
  
  // Clone steps with new IDs
  const stepIdMap = new Map<string, string>();
  
  process.steps.forEach(step => {
    const newStepId = generateStepId();
    stepIdMap.set(step.id, newStepId);
    
    cloned.steps.push({
      ...step,
      id: newStepId,
      dependencies: [], // will be remapped below
    });
  });
  
  // Remap dependencies
  cloned.steps.forEach(step => {
    const originalStep = process.steps.find(s => stepIdMap.get(s.id) === step.id);
    if (originalStep) {
      step.dependencies = originalStep.dependencies
        .map(depId => stepIdMap.get(depId))
        .filter((id): id is string => id !== undefined);
    }
  });
  
  // Clone transitions with remapped IDs
  process.transitions.forEach(trans => {
    const newFrom = trans.from === 'START' ? 'START' : stepIdMap.get(trans.from) || trans.from;
    const newTo = trans.to === 'END' ? 'END' : stepIdMap.get(trans.to) || trans.to;
    
    cloned.transitions.push({
      ...trans,
      id: generateTransitionId(),
      from: newFrom,
      to: newTo,
    });
  });
  
  cloned.metadata.template_source = process.id;
  
  return cloned;
}

/**
 * Validate process structure
 */
export function validateProcess(process: ProcessModel): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  // Check for steps
  if (process.steps.length === 0) {
    warnings.push('Process has no steps defined');
  }
  
  // Check for orphan steps (no transitions)
  const stepsInTransitions = new Set<string>();
  process.transitions.forEach(t => {
    stepsInTransitions.add(t.from);
    stepsInTransitions.add(t.to);
  });
  
  process.steps.forEach(step => {
    if (!stepsInTransitions.has(step.id)) {
      warnings.push(`Step "${step.name}" has no transitions`);
    }
  });
  
  // Check for circular dependencies
  // (simplified check - just look for self-references)
  process.steps.forEach(step => {
    if (step.dependencies.includes(step.id)) {
      errors.push(`Step "${step.name}" has circular self-dependency`);
    }
  });
  
  // Check SAFE compliance
  if (!process.safe?.isRepresentational) {
    errors.push('Process must be marked as representational');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ProcessEngine',
    version: '1.0.0',
    description: 'Representational process/pipeline modeling for CHE·NU',
    subModules: [
      'StepEngine',
      'TransitionEngine',
      'StateEngine',
      'PipelineEngine',
      'ProcessTemplateEngine',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPersistence: true,
    },
  };
}

export default {
  createProcess,
  addStep,
  removeStep,
  updateStep,
  addTransition,
  removeTransition,
  initializeStates,
  updateState,
  getProcessStatus,
  summarizeProcess,
  mapEngines,
  getDependencyGraph,
  cloneProcess,
  validateProcess,
  meta,
};

============================================================
SECTION 2 — SUB-MODULES
============================================================

--- FILE: /che-nu-sdk/core/process/step.engine.ts

/**
 * CHE·NU SDK — Step Engine
 * =========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Creates and manages process step structures.
 * 
 * @module StepEngine
 * @version 1.0.0
 */

import type { ProcessStep, StepIO } from '../process';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Step template for common patterns
 */
export interface StepTemplate {
  name: string;
  description: string;
  required_engines: string[];
  suggested_agents: string[];
  typical_inputs: StepIO[];
  typical_outputs: StepIO[];
  tags: string[];
}

/**
 * Step category
 */
export type StepCategory = 
  | 'input'
  | 'processing'
  | 'analysis'
  | 'decision'
  | 'output'
  | 'review'
  | 'approval'
  | 'notification';

// ============================================================
// STEP TEMPLATES
// ============================================================

const STEP_TEMPLATES: Record<string, StepTemplate> = {
  data_collection: {
    name: 'Data Collection',
    description: 'Gather and collect required data inputs',
    required_engines: ['DataEngine', 'ContentEngine'],
    suggested_agents: ['DataAnalyst'],
    typical_inputs: [],
    typical_outputs: [
      { name: 'collected_data', type: 'data', description: 'Collected data set', required: true },
    ],
    tags: ['input', 'data'],
  },
  analysis: {
    name: 'Analysis',
    description: 'Analyze collected data and extract insights',
    required_engines: ['AnalysisEngine', 'KnowledgeEngine'],
    suggested_agents: ['Analyst', 'StrategicAdvisor'],
    typical_inputs: [
      { name: 'input_data', type: 'data', description: 'Data to analyze', required: true },
    ],
    typical_outputs: [
      { name: 'analysis_results', type: 'document', description: 'Analysis findings', required: true },
    ],
    tags: ['processing', 'analysis'],
  },
  decision: {
    name: 'Decision Point',
    description: 'Evaluate options and make a decision',
    required_engines: ['DecisionEngine', 'MethodologyEngine'],
    suggested_agents: ['StrategicAdvisor', 'DecisionMaker'],
    typical_inputs: [
      { name: 'options', type: 'data', description: 'Options to evaluate', required: true },
      { name: 'criteria', type: 'data', description: 'Decision criteria', required: false },
    ],
    typical_outputs: [
      { name: 'decision', type: 'decision', description: 'Selected option', required: true },
    ],
    tags: ['decision', 'gate'],
  },
  content_creation: {
    name: 'Content Creation',
    description: 'Create or generate content',
    required_engines: ['ContentEngine', 'CreativityEngine'],
    suggested_agents: ['ContentCreator', 'CreativeDirector'],
    typical_inputs: [
      { name: 'brief', type: 'document', description: 'Content brief', required: true },
    ],
    typical_outputs: [
      { name: 'content', type: 'document', description: 'Created content', required: true },
    ],
    tags: ['creation', 'content'],
  },
  review: {
    name: 'Review',
    description: 'Review and provide feedback',
    required_engines: ['ContentEngine'],
    suggested_agents: ['Reviewer', 'QualityAssurance'],
    typical_inputs: [
      { name: 'item_to_review', type: 'object', description: 'Item for review', required: true },
    ],
    typical_outputs: [
      { name: 'feedback', type: 'document', description: 'Review feedback', required: true },
      { name: 'approval_status', type: 'decision', description: 'Approved/Rejected', required: true },
    ],
    tags: ['review', 'quality'],
  },
  approval: {
    name: 'Approval Gate',
    description: 'Formal approval checkpoint',
    required_engines: [],
    suggested_agents: ['Approver', 'Manager'],
    typical_inputs: [
      { name: 'submission', type: 'object', description: 'Item for approval', required: true },
    ],
    typical_outputs: [
      { name: 'approval', type: 'approval', description: 'Approval decision', required: true },
    ],
    tags: ['approval', 'gate'],
  },
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

function generateStepId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `step_${timestamp}_${random}`;
}

/**
 * Create a new step
 */
export function makeStep(
  name: string,
  description: string,
  required_engines: string[] = [],
  options?: {
    suggested_agents?: string[];
    inputs?: StepIO[];
    outputs?: StepIO[];
    dependencies?: string[];
    tags?: string[];
    metadata?: Record<string, unknown>;
  }
): Omit<ProcessStep, 'id' | 'order'> {
  return {
    name,
    description,
    required_engines,
    suggested_agents: options?.suggested_agents || [],
    inputs: options?.inputs || [],
    outputs: options?.outputs || [],
    dependencies: options?.dependencies || [],
    tags: options?.tags || [],
    metadata: options?.metadata || {},
  };
}

/**
 * Create step from template
 */
export function makeStepFromTemplate(
  templateName: string,
  customizations?: Partial<Omit<ProcessStep, 'id' | 'order'>>
): Omit<ProcessStep, 'id' | 'order'> | null {
  const template = STEP_TEMPLATES[templateName];
  if (!template) return null;
  
  return {
    name: customizations?.name || template.name,
    description: customizations?.description || template.description,
    required_engines: customizations?.required_engines || template.required_engines,
    suggested_agents: customizations?.suggested_agents || template.suggested_agents,
    inputs: customizations?.inputs || template.typical_inputs,
    outputs: customizations?.outputs || template.typical_outputs,
    dependencies: customizations?.dependencies || [],
    tags: [...template.tags, ...(customizations?.tags || [])],
    metadata: customizations?.metadata || {},
  };
}

/**
 * Describe a step
 */
export function describeStep(step: ProcessStep): {
  summary: string;
  engines: string;
  io: { inputs: number; outputs: number };
  complexity: 'simple' | 'moderate' | 'complex';
} {
  let complexity: 'simple' | 'moderate' | 'complex' = 'simple';
  
  const factors = 
    step.required_engines.length + 
    step.inputs.length + 
    step.outputs.length + 
    step.dependencies.length;
  
  if (factors > 8) complexity = 'complex';
  else if (factors > 4) complexity = 'moderate';
  
  return {
    summary: `Step "${step.name}": ${step.description}`,
    engines: step.required_engines.join(', ') || 'None',
    io: {
      inputs: step.inputs.length,
      outputs: step.outputs.length,
    },
    complexity,
  };
}

/**
 * List available step templates
 */
export function listTemplates(): string[] {
  return Object.keys(STEP_TEMPLATES);
}

/**
 * Get template details
 */
export function getTemplate(name: string): StepTemplate | null {
  return STEP_TEMPLATES[name] || null;
}

/**
 * Categorize a step
 */
export function categorizeStep(step: ProcessStep): StepCategory {
  const tags = step.tags.map(t => t.toLowerCase());
  
  if (tags.includes('input') || tags.includes('collection')) return 'input';
  if (tags.includes('analysis') || tags.includes('processing')) return 'analysis';
  if (tags.includes('decision') || tags.includes('gate')) return 'decision';
  if (tags.includes('output') || tags.includes('delivery')) return 'output';
  if (tags.includes('review')) return 'review';
  if (tags.includes('approval')) return 'approval';
  if (tags.includes('notification')) return 'notification';
  
  return 'processing';
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'StepEngine',
    version: '1.0.0',
    description: 'Process step creation and management',
    parent: 'ProcessEngine',
    templateCount: Object.keys(STEP_TEMPLATES).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  makeStep,
  makeStepFromTemplate,
  describeStep,
  listTemplates,
  getTemplate,
  categorizeStep,
  meta,
};

--- FILE: /che-nu-sdk/core/process/transition.engine.ts

/**
 * CHE·NU SDK — Transition Engine
 * ===============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Creates and manages process transitions between steps.
 * 
 * @module TransitionEngine
 * @version 1.0.0
 */

import type { ProcessTransition } from '../process';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Transition condition type
 */
export type ConditionType = 
  | 'always'
  | 'on_success'
  | 'on_failure'
  | 'on_approval'
  | 'on_rejection'
  | 'conditional'
  | 'timeout';

/**
 * Transition validation result
 */
export interface TransitionValidation {
  valid: boolean;
  errors: string[];
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

function generateTransitionId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `trans_${timestamp}_${random}`;
}

/**
 * Create a transition
 */
export function createTransition(
  from: string,
  to: string,
  condition: string,
  options?: {
    type?: ProcessTransition['type'];
    weight?: number;
    metadata?: Record<string, unknown>;
  }
): Omit<ProcessTransition, 'id'> {
  return {
    from,
    to,
    condition,
    type: options?.type || 'sequential',
    weight: options?.weight ?? 1.0,
    metadata: options?.metadata || {},
  };
}

/**
 * Create sequential transition (always proceeds)
 */
export function createSequentialTransition(
  from: string,
  to: string
): Omit<ProcessTransition, 'id'> {
  return createTransition(from, to, 'always', { type: 'sequential' });
}

/**
 * Create conditional transition
 */
export function createConditionalTransition(
  from: string,
  to: string,
  condition: string,
  weight: number = 0.5
): Omit<ProcessTransition, 'id'> {
  return createTransition(from, to, condition, { 
    type: 'conditional',
    weight,
  });
}

/**
 * Create parallel split transition
 */
export function createParallelTransition(
  from: string,
  targets: string[]
): Omit<ProcessTransition, 'id'>[] {
  return targets.map(to => createTransition(from, to, 'parallel_split', {
    type: 'parallel',
    weight: 1 / targets.length,
  }));
}

/**
 * Create loop transition
 */
export function createLoopTransition(
  from: string,
  to: string,
  exitCondition: string
): Omit<ProcessTransition, 'id'> {
  return createTransition(from, to, `loop_until: ${exitCondition}`, {
    type: 'loop',
  });
}

/**
 * Summarize a transition
 */
export function summarizeTransition(transition: ProcessTransition): string {
  const arrow = transition.bidirectional ? '↔' : '→';
  return `[${transition.from}] ${arrow} [${transition.to}] (${transition.type}: ${transition.condition})`;
}

/**
 * Describe transition path
 */
export function describeTransitionPath(transitions: ProcessTransition[]): string[] {
  return transitions.map(summarizeTransition);
}

/**
 * Validate transition
 */
export function validateTransition(
  transition: ProcessTransition,
  validStepIds: string[]
): TransitionValidation {
  const errors: string[] = [];
  
  // Check source
  if (transition.from !== 'START' && !validStepIds.includes(transition.from)) {
    errors.push(`Invalid source step: ${transition.from}`);
  }
  
  // Check target
  if (transition.to !== 'END' && !validStepIds.includes(transition.to)) {
    errors.push(`Invalid target step: ${transition.to}`);
  }
  
  // Check weight
  if (transition.weight < 0 || transition.weight > 1) {
    errors.push('Weight must be between 0 and 1');
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Find transitions from a step
 */
export function findTransitionsFrom(
  transitions: ProcessTransition[],
  stepId: string
): ProcessTransition[] {
  return transitions.filter(t => t.from === stepId);
}

/**
 * Find transitions to a step
 */
export function findTransitionsTo(
  transitions: ProcessTransition[],
  stepId: string
): ProcessTransition[] {
  return transitions.filter(t => t.to === stepId);
}

/**
 * Calculate branching factor
 */
export function calculateBranchingFactor(
  transitions: ProcessTransition[],
  stepId: string
): number {
  return findTransitionsFrom(transitions, stepId).length;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'TransitionEngine',
    version: '1.0.0',
    description: 'Process transition creation and management',
    parent: 'ProcessEngine',
    transitionTypes: ['sequential', 'conditional', 'parallel', 'loop'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  createTransition,
  createSequentialTransition,
  createConditionalTransition,
  createParallelTransition,
  createLoopTransition,
  summarizeTransition,
  describeTransitionPath,
  validateTransition,
  findTransitionsFrom,
  findTransitionsTo,
  calculateBranchingFactor,
  meta,
};

--- FILE: /che-nu-sdk/core/process/state.engine.ts

/**
 * CHE·NU SDK — State Engine
 * ==========================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Models process states (representational only).
 * NO actual state tracking or execution.
 * 
 * @module StateEngine
 * @version 1.0.0
 */

import type { ProcessStep, ProcessState, StepStatus } from '../process';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * State snapshot
 */
export interface StateSnapshot {
  timestamp: string;
  states: ProcessState[];
  active_step_ids: string[];
  completed_step_ids: string[];
  blocked_step_ids: string[];
}

/**
 * State progression
 */
export interface StateProgression {
  from_status: StepStatus;
  to_status: StepStatus;
  step_id: string;
  timestamp: string;
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

function generateStateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `state_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

/**
 * Create initial states for all steps
 */
export function createInitialStates(steps: ProcessStep[]): ProcessState[] {
  return steps.map(step => ({
    id: generateStateId(),
    step_id: step.id,
    description: `Initial state for: ${step.name}`,
    status: 'pending',
    entered_at: now(),
    context: {},
    metadata: {
      step_order: step.order,
    },
  }));
}

/**
 * Update state representationally
 * DOES NOT execute anything — just updates the structure
 */
export function updateStateRepresentationally(
  state: ProcessState,
  newStatus: StepStatus,
  context?: Record<string, unknown>
): ProcessState {
  return {
    ...state,
    status: newStatus,
    entered_at: now(),
    context: context ? { ...state.context, ...context } : state.context,
    metadata: {
      ...state.metadata,
      previous_status: state.status,
    },
  };
}

/**
 * Describe a state
 */
export function describeState(state: ProcessState): string {
  return `State [${state.id}] for step ${state.step_id}: ${state.status} (entered: ${state.entered_at})`;
}

/**
 * Create state snapshot
 */
export function createSnapshot(states: ProcessState[]): StateSnapshot {
  return {
    timestamp: now(),
    states: states.map(s => ({ ...s })),
    active_step_ids: states.filter(s => s.status === 'in_progress').map(s => s.step_id),
    completed_step_ids: states.filter(s => s.status === 'complete').map(s => s.step_id),
    blocked_step_ids: states.filter(s => s.status === 'blocked').map(s => s.step_id),
  };
}

/**
 * Calculate progress percentage
 */
export function calculateProgress(states: ProcessState[]): number {
  if (states.length === 0) return 0;
  
  const completed = states.filter(s => s.status === 'complete').length;
  return Math.round((completed / states.length) * 100);
}

/**
 * Get active states
 */
export function getActiveStates(states: ProcessState[]): ProcessState[] {
  return states.filter(s => s.status === 'in_progress');
}

/**
 * Get blocked states
 */
export function getBlockedStates(states: ProcessState[]): ProcessState[] {
  return states.filter(s => s.status === 'blocked');
}

/**
 * Get pending states
 */
export function getPendingStates(states: ProcessState[]): ProcessState[] {
  return states.filter(s => s.status === 'pending');
}

/**
 * Check if all states complete
 */
export function isAllComplete(states: ProcessState[]): boolean {
  return states.length > 0 && states.every(s => s.status === 'complete');
}

/**
 * Find state by step ID
 */
export function findStateByStep(states: ProcessState[], stepId: string): ProcessState | undefined {
  return states.find(s => s.step_id === stepId);
}

/**
 * Get state summary
 */
export function getStateSummary(states: ProcessState[]): {
  total: number;
  pending: number;
  in_progress: number;
  complete: number;
  blocked: number;
  skipped: number;
  progress: number;
} {
  return {
    total: states.length,
    pending: states.filter(s => s.status === 'pending').length,
    in_progress: states.filter(s => s.status === 'in_progress').length,
    complete: states.filter(s => s.status === 'complete').length,
    blocked: states.filter(s => s.status === 'blocked').length,
    skipped: states.filter(s => s.status === 'skipped').length,
    progress: calculateProgress(states),
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'StateEngine',
    version: '1.0.0',
    description: 'Process state modeling (representational)',
    parent: 'ProcessEngine',
    statuses: ['pending', 'in_progress', 'complete', 'blocked', 'skipped'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  createInitialStates,
  updateStateRepresentationally,
  describeState,
  createSnapshot,
  calculateProgress,
  getActiveStates,
  getBlockedStates,
  getPendingStates,
  isAllComplete,
  findStateByStep,
  getStateSummary,
  meta,
};

--- FILE: /che-nu-sdk/core/process/pipeline.engine.ts

/**
 * CHE·NU SDK — Pipeline Engine
 * =============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Links processes with projects, missions, objects, and engines.
 * Creates representational pipeline structures.
 * 
 * @module PipelineEngine
 * @version 1.0.0
 */

import type { ProcessModel } from '../process';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Pipeline structure
 */
export interface Pipeline {
  id: string;
  name: string;
  description: string;
  process: ProcessModel;
  project_id?: string;
  mission_id?: string;
  linked_objects: string[];
  linked_engines: string[];
  linked_agents: string[];
  metadata: {
    created_at: string;
    updated_at: string;
  };
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
  };
}

/**
 * Pipeline map (visual representation data)
 */
export interface PipelineMap {
  pipeline_id: string;
  nodes: PipelineMapNode[];
  connections: PipelineMapConnection[];
  layers: {
    processes: string[];
    engines: string[];
    agents: string[];
    objects: string[];
  };
}

/**
 * Pipeline map node
 */
export interface PipelineMapNode {
  id: string;
  type: 'step' | 'engine' | 'agent' | 'object' | 'start' | 'end';
  label: string;
  layer: number;
  x?: number;
  y?: number;
}

/**
 * Pipeline map connection
 */
export interface PipelineMapConnection {
  from: string;
  to: string;
  type: 'flow' | 'uses' | 'produces' | 'managed_by';
  label?: string;
}

/**
 * Pipeline context for building
 */
export interface PipelineContext {
  project_id?: string;
  mission_id?: string;
  objects?: string[];
  agents?: string[];
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

function generatePipelineId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `pipe_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

/**
 * Build a pipeline from process and context
 */
export function buildPipeline(
  process: ProcessModel,
  context: PipelineContext
): Pipeline {
  // Collect all engines from process steps
  const linkedEngines = new Set<string>();
  const linkedAgents = new Set<string>();
  
  process.steps.forEach(step => {
    step.required_engines.forEach(e => linkedEngines.add(e));
    step.suggested_agents.forEach(a => linkedAgents.add(a));
  });
  
  // Add context agents
  context.agents?.forEach(a => linkedAgents.add(a));
  
  return {
    id: generatePipelineId(),
    name: `Pipeline: ${process.name}`,
    description: `Pipeline for process "${process.name}"`,
    process,
    project_id: context.project_id,
    mission_id: context.mission_id,
    linked_objects: context.objects || [],
    linked_engines: Array.from(linkedEngines),
    linked_agents: Array.from(linkedAgents),
    metadata: {
      created_at: now(),
      updated_at: now(),
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

/**
 * Generate pipeline map (for visualization)
 */
export function pipelineMap(pipeline: Pipeline): PipelineMap {
  const nodes: PipelineMapNode[] = [];
  const connections: PipelineMapConnection[] = [];
  
  // Add start node
  nodes.push({
    id: 'START',
    type: 'start',
    label: 'Start',
    layer: 0,
  });
  
  // Add step nodes
  pipeline.process.steps.forEach((step, index) => {
    nodes.push({
      id: step.id,
      type: 'step',
      label: step.name,
      layer: 1,
      x: 200 + index * 150,
      y: 100,
    });
  });
  
  // Add end node
  nodes.push({
    id: 'END',
    type: 'end',
    label: 'End',
    layer: 0,
  });
  
  // Add engine nodes
  pipeline.linked_engines.forEach((engine, index) => {
    nodes.push({
      id: `engine_${engine}`,
      type: 'engine',
      label: engine,
      layer: 2,
      x: 100 + index * 120,
      y: 250,
    });
  });
  
  // Add agent nodes
  pipeline.linked_agents.forEach((agent, index) => {
    nodes.push({
      id: `agent_${agent}`,
      type: 'agent',
      label: agent,
      layer: 3,
      x: 100 + index * 120,
      y: 350,
    });
  });
  
  // Add flow connections from transitions
  pipeline.process.transitions.forEach(trans => {
    connections.push({
      from: trans.from,
      to: trans.to,
      type: 'flow',
      label: trans.condition,
    });
  });
  
  // Add engine usage connections
  pipeline.process.steps.forEach(step => {
    step.required_engines.forEach(engine => {
      connections.push({
        from: step.id,
        to: `engine_${engine}`,
        type: 'uses',
      });
    });
    
    step.suggested_agents.forEach(agent => {
      connections.push({
        from: step.id,
        to: `agent_${agent}`,
        type: 'managed_by',
      });
    });
  });
  
  return {
    pipeline_id: pipeline.id,
    nodes,
    connections,
    layers: {
      processes: pipeline.process.steps.map(s => s.id),
      engines: pipeline.linked_engines,
      agents: pipeline.linked_agents,
      objects: pipeline.linked_objects,
    },
  };
}

/**
 * Link object to pipeline
 */
export function linkObject(pipeline: Pipeline, objectId: string): Pipeline {
  if (!pipeline.linked_objects.includes(objectId)) {
    pipeline.linked_objects.push(objectId);
    pipeline.metadata.updated_at = now();
  }
  return pipeline;
}

/**
 * Unlink object from pipeline
 */
export function unlinkObject(pipeline: Pipeline, objectId: string): Pipeline {
  pipeline.linked_objects = pipeline.linked_objects.filter(o => o !== objectId);
  pipeline.metadata.updated_at = now();
  return pipeline;
}

/**
 * Get pipeline summary
 */
export function summarizePipeline(pipeline: Pipeline): {
  id: string;
  name: string;
  steps: number;
  engines: number;
  agents: number;
  objects: number;
  has_project: boolean;
  has_mission: boolean;
} {
  return {
    id: pipeline.id,
    name: pipeline.name,
    steps: pipeline.process.steps.length,
    engines: pipeline.linked_engines.length,
    agents: pipeline.linked_agents.length,
    objects: pipeline.linked_objects.length,
    has_project: !!pipeline.project_id,
    has_mission: !!pipeline.mission_id,
  };
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'PipelineEngine',
    version: '1.0.0',
    description: 'Process-project-mission-engine pipeline linking',
    parent: 'ProcessEngine',
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
    },
  };
}

export default {
  buildPipeline,
  pipelineMap,
  linkObject,
  unlinkObject,
  summarizePipeline,
  meta,
};

--- FILE: /che-nu-sdk/core/process/template.engine.ts

/**
 * CHE·NU SDK — Process Template Engine
 * =====================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Provides predefined process templates.
 * 
 * @module ProcessTemplateEngine
 * @version 1.0.0
 */

import type { ProcessModel, ProcessStep, ProcessTransition } from '../process';
import { createProcess, addStep, addTransition } from '../process';

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Template metadata
 */
export interface TemplateInfo {
  id: string;
  name: string;
  description: string;
  category: string;
  steps_count: number;
  complexity: 'simple' | 'moderate' | 'complex';
  suggested_for: string[];
}

// ============================================================
// TEMPLATE DEFINITIONS
// ============================================================

/**
 * Research Pipeline Template
 */
function createResearchPipelineTemplate(): ProcessModel {
  let process = createProcess({
    name: 'Research Pipeline',
    description: 'Standard research process from question to findings',
    category: 'research',
  });
  
  // Steps
  process = addStep(process, {
    name: 'Define Research Question',
    description: 'Clearly articulate the research question or hypothesis',
    required_engines: ['KnowledgeEngine'],
    suggested_agents: ['ResearchLead'],
    inputs: [],
    outputs: [{ name: 'research_question', type: 'document', description: 'Defined research question', required: true }],
    dependencies: [],
    tags: ['input', 'planning'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Literature Review',
    description: 'Review existing research and literature',
    required_engines: ['KnowledgeEngine', 'ContentEngine'],
    suggested_agents: ['Researcher'],
    inputs: [{ name: 'research_question', type: 'document', description: 'Research question', required: true }],
    outputs: [{ name: 'literature_review', type: 'document', description: 'Literature review summary', required: true }],
    dependencies: [process.steps[0].id],
    tags: ['research', 'analysis'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Data Collection',
    description: 'Collect relevant data for analysis',
    required_engines: ['DataEngine'],
    suggested_agents: ['DataAnalyst'],
    inputs: [{ name: 'methodology', type: 'document', description: 'Data collection methodology', required: true }],
    outputs: [{ name: 'raw_data', type: 'data', description: 'Collected data set', required: true }],
    dependencies: [process.steps[1].id],
    tags: ['data', 'collection'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Analysis',
    description: 'Analyze collected data',
    required_engines: ['AnalysisEngine', 'DataEngine'],
    suggested_agents: ['DataAnalyst', 'Researcher'],
    inputs: [{ name: 'raw_data', type: 'data', description: 'Data to analyze', required: true }],
    outputs: [{ name: 'analysis_results', type: 'document', description: 'Analysis findings', required: true }],
    dependencies: [process.steps[2].id],
    tags: ['analysis'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Synthesize Findings',
    description: 'Compile and synthesize research findings',
    required_engines: ['ContentEngine', 'KnowledgeEngine'],
    suggested_agents: ['ResearchLead'],
    inputs: [
      { name: 'analysis_results', type: 'document', description: 'Analysis results', required: true },
      { name: 'literature_review', type: 'document', description: 'Literature context', required: true },
    ],
    outputs: [{ name: 'research_findings', type: 'document', description: 'Final research findings', required: true }],
    dependencies: [process.steps[3].id],
    tags: ['synthesis', 'output'],
    metadata: {},
  });
  
  // Transitions
  process = addTransition(process, { from: 'START', to: process.steps[0].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[0].id, to: process.steps[1].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[1].id, to: process.steps[2].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[2].id, to: process.steps[3].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[3].id, to: process.steps[4].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[4].id, to: 'END', condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  
  process.metadata.template_source = 'research_pipeline';
  
  return process;
}

/**
 * Creative Pipeline Template
 */
function createCreativePipelineTemplate(): ProcessModel {
  let process = createProcess({
    name: 'Creative Pipeline',
    description: 'Creative content development process',
    category: 'creative',
  });
  
  // Steps
  process = addStep(process, {
    name: 'Brief & Inspiration',
    description: 'Define creative brief and gather inspiration',
    required_engines: ['CreativityEngine', 'ContentEngine'],
    suggested_agents: ['CreativeDirector'],
    inputs: [],
    outputs: [
      { name: 'creative_brief', type: 'document', description: 'Creative brief', required: true },
      { name: 'inspiration_board', type: 'object', description: 'Inspiration collection', required: false },
    ],
    dependencies: [],
    tags: ['input', 'creative', 'brief'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Concept Development',
    description: 'Develop creative concepts',
    required_engines: ['CreativityEngine'],
    suggested_agents: ['CreativeDirector', 'Designer'],
    inputs: [{ name: 'creative_brief', type: 'document', description: 'Brief', required: true }],
    outputs: [{ name: 'concepts', type: 'document', description: 'Creative concepts', required: true }],
    dependencies: [process.steps[0].id],
    tags: ['creative', 'concept'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Production',
    description: 'Create the actual content/asset',
    required_engines: ['CreativityEngine', 'ContentEngine'],
    suggested_agents: ['ContentCreator', 'Designer'],
    inputs: [{ name: 'approved_concept', type: 'document', description: 'Selected concept', required: true }],
    outputs: [{ name: 'draft_content', type: 'object', description: 'Draft content', required: true }],
    dependencies: [process.steps[1].id],
    tags: ['production', 'creation'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Review & Refinement',
    description: 'Review and refine the content',
    required_engines: ['ContentEngine'],
    suggested_agents: ['CreativeDirector', 'Reviewer'],
    inputs: [{ name: 'draft_content', type: 'object', description: 'Draft to review', required: true }],
    outputs: [
      { name: 'feedback', type: 'document', description: 'Review feedback', required: true },
      { name: 'refined_content', type: 'object', description: 'Refined content', required: true },
    ],
    dependencies: [process.steps[2].id],
    tags: ['review', 'refinement'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Final Delivery',
    description: 'Finalize and deliver the content',
    required_engines: ['ContentEngine'],
    suggested_agents: ['ContentCreator'],
    inputs: [{ name: 'refined_content', type: 'object', description: 'Approved content', required: true }],
    outputs: [{ name: 'final_deliverable', type: 'object', description: 'Final content', required: true }],
    dependencies: [process.steps[3].id],
    tags: ['output', 'delivery'],
    metadata: {},
  });
  
  // Transitions with review loop
  process = addTransition(process, { from: 'START', to: process.steps[0].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[0].id, to: process.steps[1].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[1].id, to: process.steps[2].id, condition: 'concept_approved', type: 'conditional', weight: 0.7, metadata: {} });
  process = addTransition(process, { from: process.steps[2].id, to: process.steps[3].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[3].id, to: process.steps[2].id, condition: 'needs_revision', type: 'loop', weight: 0.3, metadata: {} });
  process = addTransition(process, { from: process.steps[3].id, to: process.steps[4].id, condition: 'approved', type: 'conditional', weight: 0.7, metadata: {} });
  process = addTransition(process, { from: process.steps[4].id, to: 'END', condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  
  process.metadata.template_source = 'creative_pipeline';
  
  return process;
}

/**
 * XR Production Pipeline Template
 */
function createXRProductionPipelineTemplate(): ProcessModel {
  let process = createProcess({
    name: 'XR Production Pipeline',
    description: 'Extended Reality content production process',
    category: 'xr',
  });
  
  process = addStep(process, {
    name: 'XR Concept Design',
    description: 'Define XR experience concept',
    required_engines: ['XRSceneEngine', 'CreativityEngine'],
    suggested_agents: ['XRSceneBuilder', 'CreativeDirector'],
    inputs: [],
    outputs: [{ name: 'xr_concept', type: 'document', description: 'XR concept document', required: true }],
    dependencies: [],
    tags: ['xr', 'concept', 'design'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Environment Design',
    description: 'Design the XR environment and spaces',
    required_engines: ['XRSceneEngine', 'CartographyEngine'],
    suggested_agents: ['XRSceneBuilder', 'EnvironmentArtist'],
    inputs: [{ name: 'xr_concept', type: 'document', description: 'Concept', required: true }],
    outputs: [{ name: 'environment_design', type: 'object', description: 'Environment design', required: true }],
    dependencies: [process.steps[0].id],
    tags: ['xr', 'environment'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Asset Creation',
    description: 'Create 3D assets and objects',
    required_engines: ['XRSceneEngine', 'CreativityEngine'],
    suggested_agents: ['3DArtist', 'XRSceneBuilder'],
    inputs: [{ name: 'asset_list', type: 'document', description: 'Required assets', required: true }],
    outputs: [{ name: 'xr_assets', type: 'object', description: '3D assets', required: true }],
    dependencies: [process.steps[1].id],
    tags: ['xr', 'assets', '3d'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Scene Assembly',
    description: 'Assemble XR scene from assets',
    required_engines: ['XRSceneEngine', 'HyperFabricEngine'],
    suggested_agents: ['XRSceneBuilder'],
    inputs: [
      { name: 'environment_design', type: 'object', description: 'Environment', required: true },
      { name: 'xr_assets', type: 'object', description: 'Assets', required: true },
    ],
    outputs: [{ name: 'xr_scene', type: 'object', description: 'Assembled scene', required: true }],
    dependencies: [process.steps[2].id],
    tags: ['xr', 'scene', 'assembly'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Interaction Design',
    description: 'Design user interactions',
    required_engines: ['XRSceneEngine'],
    suggested_agents: ['UXDesigner', 'XRSceneBuilder'],
    inputs: [{ name: 'xr_scene', type: 'object', description: 'Scene', required: true }],
    outputs: [{ name: 'interaction_design', type: 'document', description: 'Interaction specifications', required: true }],
    dependencies: [process.steps[3].id],
    tags: ['xr', 'interaction', 'ux'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Testing & Optimization',
    description: 'Test and optimize XR experience',
    required_engines: ['XRSceneEngine'],
    suggested_agents: ['QA', 'XRSceneBuilder'],
    inputs: [{ name: 'xr_experience', type: 'object', description: 'Complete experience', required: true }],
    outputs: [{ name: 'test_results', type: 'document', description: 'Test results', required: true }],
    dependencies: [process.steps[4].id],
    tags: ['xr', 'testing', 'qa'],
    metadata: {},
  });
  
  // Transitions
  process = addTransition(process, { from: 'START', to: process.steps[0].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[0].id, to: process.steps[1].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[1].id, to: process.steps[2].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[2].id, to: process.steps[3].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[3].id, to: process.steps[4].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[4].id, to: process.steps[5].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[5].id, to: process.steps[3].id, condition: 'needs_fixes', type: 'loop', weight: 0.3, metadata: {} });
  process = addTransition(process, { from: process.steps[5].id, to: 'END', condition: 'passed', type: 'conditional', weight: 0.7, metadata: {} });
  
  process.metadata.template_source = 'xr_production_pipeline';
  
  return process;
}

/**
 * Personal Development Pipeline Template
 */
function createPersonalDevelopmentPipelineTemplate(): ProcessModel {
  let process = createProcess({
    name: 'Personal Development Pipeline',
    description: 'Self-improvement and growth process',
    category: 'personal',
  });
  
  process = addStep(process, {
    name: 'Self Assessment',
    description: 'Assess current state and identify areas for growth',
    required_engines: ['ReflectionEngine', 'KnowledgeEngine'],
    suggested_agents: ['PersonalAdvisor'],
    inputs: [],
    outputs: [{ name: 'assessment', type: 'document', description: 'Self-assessment results', required: true }],
    dependencies: [],
    tags: ['personal', 'assessment'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Goal Setting',
    description: 'Define clear development goals',
    required_engines: ['MethodologyEngine'],
    suggested_agents: ['PersonalAdvisor', 'StrategicAdvisor'],
    inputs: [{ name: 'assessment', type: 'document', description: 'Assessment', required: true }],
    outputs: [{ name: 'goals', type: 'document', description: 'Development goals', required: true }],
    dependencies: [process.steps[0].id],
    tags: ['personal', 'goals'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Learning Path Design',
    description: 'Design learning activities and resources',
    required_engines: ['KnowledgeEngine', 'ContentEngine'],
    suggested_agents: ['LearningAdvisor'],
    inputs: [{ name: 'goals', type: 'document', description: 'Goals', required: true }],
    outputs: [{ name: 'learning_path', type: 'document', description: 'Learning path', required: true }],
    dependencies: [process.steps[1].id],
    tags: ['personal', 'learning'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Practice & Application',
    description: 'Apply learning through practice',
    required_engines: [],
    suggested_agents: [],
    inputs: [{ name: 'learning_path', type: 'document', description: 'Path to follow', required: true }],
    outputs: [{ name: 'practice_log', type: 'document', description: 'Practice records', required: true }],
    dependencies: [process.steps[2].id],
    tags: ['personal', 'practice'],
    metadata: {},
  });
  
  process = addStep(process, {
    name: 'Progress Review',
    description: 'Review progress and adjust approach',
    required_engines: ['ReflectionEngine', 'AnalysisEngine'],
    suggested_agents: ['PersonalAdvisor'],
    inputs: [
      { name: 'practice_log', type: 'document', description: 'Practice records', required: true },
      { name: 'goals', type: 'document', description: 'Original goals', required: true },
    ],
    outputs: [{ name: 'progress_report', type: 'document', description: 'Progress report', required: true }],
    dependencies: [process.steps[3].id],
    tags: ['personal', 'review'],
    metadata: {},
  });
  
  // Transitions with iterative loop
  process = addTransition(process, { from: 'START', to: process.steps[0].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[0].id, to: process.steps[1].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[1].id, to: process.steps[2].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[2].id, to: process.steps[3].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[3].id, to: process.steps[4].id, condition: 'always', type: 'sequential', weight: 1, metadata: {} });
  process = addTransition(process, { from: process.steps[4].id, to: process.steps[2].id, condition: 'continue_learning', type: 'loop', weight: 0.6, metadata: {} });
  process = addTransition(process, { from: process.steps[4].id, to: 'END', condition: 'goals_achieved', type: 'conditional', weight: 0.4, metadata: {} });
  
  process.metadata.template_source = 'personal_development_pipeline';
  
  return process;
}

// ============================================================
// TEMPLATE REGISTRY
// ============================================================

const TEMPLATES: Record<string, () => ProcessModel> = {
  research_pipeline: createResearchPipelineTemplate,
  creative_pipeline: createCreativePipelineTemplate,
  xr_production_pipeline: createXRProductionPipelineTemplate,
  personal_development_pipeline: createPersonalDevelopmentPipelineTemplate,
};

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * List available templates
 */
export function listTemplates(): TemplateInfo[] {
  return [
    {
      id: 'research_pipeline',
      name: 'Research Pipeline',
      description: 'Standard research process from question to findings',
      category: 'research',
      steps_count: 5,
      complexity: 'moderate',
      suggested_for: ['Scholar sphere', 'Academic projects'],
    },
    {
      id: 'creative_pipeline',
      name: 'Creative Pipeline',
      description: 'Creative content development process',
      category: 'creative',
      steps_count: 5,
      complexity: 'moderate',
      suggested_for: ['Creative Studio sphere', 'Design projects'],
    },
    {
      id: 'xr_production_pipeline',
      name: 'XR Production Pipeline',
      description: 'Extended Reality content production',
      category: 'xr',
      steps_count: 6,
      complexity: 'complex',
      suggested_for: ['XR projects', 'Immersive experiences'],
    },
    {
      id: 'personal_development_pipeline',
      name: 'Personal Development Pipeline',
      description: 'Self-improvement and growth process',
      category: 'personal',
      steps_count: 5,
      complexity: 'simple',
      suggested_for: ['Maison sphere', 'Personal goals'],
    },
  ];
}

/**
 * Load a template by name
 */
export function loadTemplate(templateName: string): ProcessModel | null {
  const templateFn = TEMPLATES[templateName];
  if (!templateFn) return null;
  return templateFn();
}

/**
 * Get template by category
 */
export function getTemplatesByCategory(category: string): TemplateInfo[] {
  return listTemplates().filter(t => t.category === category);
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'ProcessTemplateEngine',
    version: '1.0.0',
    description: 'Predefined process templates',
    parent: 'ProcessEngine',
    templateCount: Object.keys(TEMPLATES).length,
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  listTemplates,
  loadTemplate,
  getTemplatesByCategory,
  meta,
};
