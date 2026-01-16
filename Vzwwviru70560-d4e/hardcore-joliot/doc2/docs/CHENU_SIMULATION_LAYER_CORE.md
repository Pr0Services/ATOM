############################################################
#                                                          #
#       CHE·NU SIMULATION LAYER                            #
#       PART 1: CORE ENGINE + SUB-ENGINES                  #
#       SAFE · REPRESENTATIONAL · NON-AUTONOMOUS           #
#                                                          #
############################################################

============================================================
SECTION A1 — MAIN MODULE: SimulationEngine
============================================================

--- FILE: /che-nu-sdk/core/simulation.ts

/**
 * CHE·NU SDK — Simulation Engine
 * ================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Produces REPRESENTATIONAL simulation outputs such as:
 * - Symbolic state transitions
 * - Conceptual timelines
 * - Abstract state flows
 * - Divergence/variation branching
 * 
 * NO REAL EXECUTION — only conceptual/structural simulation.
 * NO PREDICTION — no forecasting or optimization.
 * 
 * @module SimulationEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Subject types that can be simulated
 */
export type SimulationSubjectType = 
  | 'project'
  | 'mission'
  | 'process'
  | 'persona'
  | 'workflow'
  | 'pipeline';

/**
 * Simulation frame — a single point in the simulation
 */
export interface SimulationFrame {
  id: string;
  timestamp: number;          // Conceptual timestamp (step number)
  state_id: string;
  description: string;
  involved_engines: string[];
  involved_agents: string[];
  inputs: string[];
  outputs: string[];
  metadata: Record<string, unknown>;
}

/**
 * Simulation branch — an alternative path
 */
export interface SimulationBranch {
  id: string;
  name: string;
  description: string;
  branch_point: number;       // Frame timestamp where branch occurs
  condition: string;          // Conceptual condition for this branch
  frames: SimulationFrame[];
  probability_weight: number; // Representational weight (not prediction)
  metadata: Record<string, unknown>;
}

/**
 * Complete simulation run
 */
export interface SimulationRun {
  id: string;
  name: string;
  subject_type: SimulationSubjectType;
  subject_id: string;
  subject_name: string;
  main_timeline: SimulationFrame[];
  branches: SimulationBranch[];
  total_frames: number;
  total_branches: number;
  engines_involved: string[];
  agents_involved: string[];
  created_at: string;
  metadata: Record<string, unknown>;
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noExecution: true;
    noPrediction: true;
  };
}

/**
 * Simulation configuration
 */
export interface SimulationConfig {
  include_branches: boolean;
  max_frames: number;
  max_branches: number;
  detail_level: 'minimal' | 'standard' | 'detailed';
}

/**
 * Input structure for simulation (generic)
 */
export interface SimulationInput {
  type: SimulationSubjectType;
  id: string;
  name: string;
  steps?: Array<{
    id: string;
    name: string;
    description: string;
    required_engines?: string[];
    suggested_agents?: string[];
  }>;
  transitions?: Array<{
    from: string;
    to: string;
    condition: string;
    type: string;
  }>;
  traits?: string[];
  metadata?: Record<string, unknown>;
}

/**
 * Simulation summary
 */
export interface SimulationSummary {
  id: string;
  subject: string;
  total_frames: number;
  total_branches: number;
  main_path_length: number;
  branch_points: number;
  engines_count: number;
  complexity: 'simple' | 'moderate' | 'complex';
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateSimulationId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 6);
  return `sim_${timestamp}_${random}`;
}

function generateFrameId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `frame_${timestamp}_${random}`;
}

function generateBranchId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `branch_${timestamp}_${random}`;
}

function now(): string {
  return new Date().toISOString();
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Run a simulation on an input structure
 * REPRESENTATIONAL ONLY — produces conceptual state transitions
 */
export function simulate(
  input: SimulationInput,
  config: Partial<SimulationConfig> = {}
): SimulationRun {
  const fullConfig: SimulationConfig = {
    include_branches: config.include_branches ?? true,
    max_frames: config.max_frames ?? 20,
    max_branches: config.max_branches ?? 5,
    detail_level: config.detail_level ?? 'standard',
  };
  
  // Generate main timeline frames
  const mainTimeline = simulateMainTimeline(input, fullConfig);
  
  // Generate branches if enabled
  const branches = fullConfig.include_branches 
    ? generateBranches(input, mainTimeline, fullConfig)
    : [];
  
  // Collect all engines and agents
  const enginesSet = new Set<string>();
  const agentsSet = new Set<string>();
  
  mainTimeline.forEach(frame => {
    frame.involved_engines.forEach(e => enginesSet.add(e));
    frame.involved_agents.forEach(a => agentsSet.add(a));
  });
  
  branches.forEach(branch => {
    branch.frames.forEach(frame => {
      frame.involved_engines.forEach(e => enginesSet.add(e));
      frame.involved_agents.forEach(a => agentsSet.add(a));
    });
  });
  
  return {
    id: generateSimulationId(),
    name: `Simulation: ${input.name}`,
    subject_type: input.type,
    subject_id: input.id,
    subject_name: input.name,
    main_timeline: mainTimeline,
    branches,
    total_frames: mainTimeline.length + branches.reduce((sum, b) => sum + b.frames.length, 0),
    total_branches: branches.length,
    engines_involved: Array.from(enginesSet),
    agents_involved: Array.from(agentsSet),
    created_at: now(),
    metadata: {
      config: fullConfig,
      input_type: input.type,
    },
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPrediction: true,
    },
  };
}

/**
 * Simulate main timeline from steps
 */
function simulateMainTimeline(
  input: SimulationInput,
  config: SimulationConfig
): SimulationFrame[] {
  const frames: SimulationFrame[] = [];
  
  // Start frame
  frames.push({
    id: generateFrameId(),
    timestamp: 0,
    state_id: 'START',
    description: `Begin ${input.type}: ${input.name}`,
    involved_engines: [],
    involved_agents: [],
    inputs: [],
    outputs: [],
    metadata: { phase: 'initialization' },
  });
  
  // Process steps if available
  if (input.steps && input.steps.length > 0) {
    input.steps.slice(0, config.max_frames - 2).forEach((step, index) => {
      frames.push({
        id: generateFrameId(),
        timestamp: index + 1,
        state_id: step.id,
        description: step.description || `Execute: ${step.name}`,
        involved_engines: step.required_engines || [],
        involved_agents: step.suggested_agents || [],
        inputs: [`input_${index}`],
        outputs: [`output_${index}`],
        metadata: {
          step_name: step.name,
          step_order: index + 1,
        },
      });
    });
  } else {
    // Generate generic frames for non-step-based subjects
    const genericPhases = ['initialization', 'processing', 'refinement', 'completion'];
    genericPhases.forEach((phase, index) => {
      frames.push({
        id: generateFrameId(),
        timestamp: index + 1,
        state_id: `phase_${index}`,
        description: `${phase.charAt(0).toUpperCase() + phase.slice(1)} phase`,
        involved_engines: [],
        involved_agents: [],
        inputs: [],
        outputs: [],
        metadata: { phase },
      });
    });
  }
  
  // End frame
  frames.push({
    id: generateFrameId(),
    timestamp: frames.length,
    state_id: 'END',
    description: `Complete ${input.type}: ${input.name}`,
    involved_engines: [],
    involved_agents: [],
    inputs: [],
    outputs: ['final_output'],
    metadata: { phase: 'completion' },
  });
  
  return frames;
}

/**
 * Simulate a sequence of steps
 */
export function simulateSteps(
  steps: Array<{ id: string; name: string; description: string; required_engines?: string[] }>
): SimulationFrame[] {
  return steps.map((step, index) => ({
    id: generateFrameId(),
    timestamp: index,
    state_id: step.id,
    description: step.description,
    involved_engines: step.required_engines || [],
    involved_agents: [],
    inputs: index > 0 ? [`output_${index - 1}`] : [],
    outputs: [`output_${index}`],
    metadata: { step_name: step.name },
  }));
}

/**
 * Simulate a timeline
 */
export function simulateTimeline(
  timeline: Array<{ id: string; description: string; timestamp: number }>
): SimulationFrame[] {
  return timeline.map(item => ({
    id: generateFrameId(),
    timestamp: item.timestamp,
    state_id: item.id,
    description: item.description,
    involved_engines: [],
    involved_agents: [],
    inputs: [],
    outputs: [],
    metadata: {},
  }));
}

/**
 * Generate conceptual branches (what-if variations)
 * NO PREDICTION — only structural alternatives
 */
export function generateBranches(
  input: SimulationInput,
  mainTimeline: SimulationFrame[],
  config: SimulationConfig
): SimulationBranch[] {
  const branches: SimulationBranch[] = [];
  
  if (!input.transitions || input.transitions.length === 0) {
    return branches;
  }
  
  // Find conditional transitions (potential branch points)
  const conditionalTransitions = input.transitions.filter(
    t => t.type === 'conditional' || t.type === 'loop'
  );
  
  conditionalTransitions.slice(0, config.max_branches).forEach((trans, index) => {
    // Find the frame where this transition applies
    const branchPointFrame = mainTimeline.find(f => f.state_id === trans.from);
    const branchPoint = branchPointFrame?.timestamp ?? index + 1;
    
    // Create alternative branch
    const branchFrames: SimulationFrame[] = [
      {
        id: generateFrameId(),
        timestamp: branchPoint,
        state_id: `alt_${trans.from}_${index}`,
        description: `Alternative path: ${trans.condition}`,
        involved_engines: branchPointFrame?.involved_engines || [],
        involved_agents: branchPointFrame?.involved_agents || [],
        inputs: [],
        outputs: [],
        metadata: { branch_reason: trans.condition },
      },
      {
        id: generateFrameId(),
        timestamp: branchPoint + 1,
        state_id: `alt_${trans.to}_${index}`,
        description: `Continue alternative: toward ${trans.to}`,
        involved_engines: [],
        involved_agents: [],
        inputs: [],
        outputs: [],
        metadata: {},
      },
    ];
    
    branches.push({
      id: generateBranchId(),
      name: `Branch: ${trans.condition}`,
      description: `Alternative path when ${trans.condition}`,
      branch_point: branchPoint,
      condition: trans.condition,
      frames: branchFrames,
      probability_weight: 0.3, // Representational weight, not prediction
      metadata: {
        source_transition: trans,
      },
    });
  });
  
  return branches;
}

/**
 * Summarize a simulation run
 */
export function summarize(run: SimulationRun): SimulationSummary {
  // Count branch points (unique timestamps where branches occur)
  const branchPoints = new Set(run.branches.map(b => b.branch_point)).size;
  
  // Determine complexity
  let complexity: 'simple' | 'moderate' | 'complex' = 'simple';
  if (run.total_frames > 15 || run.total_branches > 3) {
    complexity = 'complex';
  } else if (run.total_frames > 8 || run.total_branches > 1) {
    complexity = 'moderate';
  }
  
  return {
    id: run.id,
    subject: `${run.subject_type}: ${run.subject_name}`,
    total_frames: run.total_frames,
    total_branches: run.total_branches,
    main_path_length: run.main_timeline.length,
    branch_points: branchPoints,
    engines_count: run.engines_involved.length,
    complexity,
  };
}

/**
 * Get frames at a specific timestamp
 */
export function getFramesAtTimestamp(run: SimulationRun, timestamp: number): SimulationFrame[] {
  const frames: SimulationFrame[] = [];
  
  // Check main timeline
  const mainFrame = run.main_timeline.find(f => f.timestamp === timestamp);
  if (mainFrame) frames.push(mainFrame);
  
  // Check branches
  run.branches.forEach(branch => {
    const branchFrame = branch.frames.find(f => f.timestamp === timestamp);
    if (branchFrame) frames.push(branchFrame);
  });
  
  return frames;
}

/**
 * Get all possible paths through the simulation
 */
export function getAllPaths(run: SimulationRun): Array<{ name: string; frames: SimulationFrame[] }> {
  const paths: Array<{ name: string; frames: SimulationFrame[] }> = [];
  
  // Main path
  paths.push({
    name: 'Main Timeline',
    frames: run.main_timeline,
  });
  
  // Branch paths (simplified — branch + continuation)
  run.branches.forEach(branch => {
    const beforeBranch = run.main_timeline.filter(f => f.timestamp < branch.branch_point);
    paths.push({
      name: branch.name,
      frames: [...beforeBranch, ...branch.frames],
    });
  });
  
  return paths;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'SimulationEngine',
    version: '1.0.0',
    description: 'Representational simulation of CHE·NU structures',
    subModules: ['StateFlowEngine', 'VariationEngine'],
    subjectTypes: ['project', 'mission', 'process', 'persona', 'workflow', 'pipeline'],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noExecution: true,
      noPrediction: true,
    },
  };
}

export default {
  simulate,
  simulateSteps,
  simulateTimeline,
  generateBranches,
  summarize,
  getFramesAtTimestamp,
  getAllPaths,
  meta,
};

============================================================
SECTION A2 — SUB-MODULE: StateFlowEngine
============================================================

--- FILE: /che-nu-sdk/core/simulation/stateflow.engine.ts

/**
 * CHE·NU SDK — State Flow Engine
 * ================================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents conceptual progression from state to state.
 * NO real execution — structure only.
 * 
 * @module StateFlowEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * State in the flow
 */
export interface FlowState {
  id: string;
  name: string;
  description: string;
  type: 'start' | 'intermediate' | 'decision' | 'parallel' | 'end';
  metadata: Record<string, unknown>;
}

/**
 * Flow connection
 */
export interface FlowConnection {
  from: string;
  to: string;
  condition?: string;
  type: 'sequential' | 'conditional' | 'parallel_split' | 'parallel_join';
}

/**
 * Complete state flow
 */
export interface StateFlow {
  id: string;
  name: string;
  description: string;
  states: FlowState[];
  connections: FlowConnection[];
  entry_state: string;
  exit_states: string[];
  metadata: Record<string, unknown>;
  safe: {
    isRepresentational: true;
    noAutonomy: true;
  };
}

/**
 * Flow analysis result
 */
export interface FlowAnalysis {
  total_states: number;
  total_connections: number;
  has_cycles: boolean;
  parallel_sections: number;
  decision_points: number;
  max_depth: number;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateFlowId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `flow_${timestamp}_${random}`;
}

function generateStateId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `fstate_${timestamp}_${random}`;
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Build a state flow from a process or mission structure
 */
export function buildStateFlow(
  input: {
    name: string;
    steps?: Array<{ id: string; name: string; description?: string }>;
    transitions?: Array<{ from: string; to: string; condition?: string; type?: string }>;
  }
): StateFlow {
  const states: FlowState[] = [];
  const connections: FlowConnection[] = [];
  
  // Add start state
  const startId = generateStateId();
  states.push({
    id: startId,
    name: 'Start',
    description: 'Flow entry point',
    type: 'start',
    metadata: {},
  });
  
  // Add states from steps
  const stepStateMap = new Map<string, string>();
  
  if (input.steps) {
    input.steps.forEach(step => {
      const stateId = generateStateId();
      stepStateMap.set(step.id, stateId);
      
      states.push({
        id: stateId,
        name: step.name,
        description: step.description || '',
        type: 'intermediate',
        metadata: { original_step_id: step.id },
      });
    });
  }
  
  // Add end state
  const endId = generateStateId();
  states.push({
    id: endId,
    name: 'End',
    description: 'Flow exit point',
    type: 'end',
    metadata: {},
  });
  
  // Build connections from transitions
  if (input.transitions) {
    input.transitions.forEach(trans => {
      const fromId = trans.from === 'START' ? startId : stepStateMap.get(trans.from);
      const toId = trans.to === 'END' ? endId : stepStateMap.get(trans.to);
      
      if (fromId && toId) {
        let connectionType: FlowConnection['type'] = 'sequential';
        if (trans.type === 'conditional') connectionType = 'conditional';
        if (trans.type === 'parallel') connectionType = 'parallel_split';
        
        connections.push({
          from: fromId,
          to: toId,
          condition: trans.condition,
          type: connectionType,
        });
      }
    });
  } else if (input.steps && input.steps.length > 0) {
    // Create sequential connections if no transitions defined
    const stateIds = Array.from(stepStateMap.values());
    
    // Start to first step
    connections.push({
      from: startId,
      to: stateIds[0],
      type: 'sequential',
    });
    
    // Between steps
    for (let i = 0; i < stateIds.length - 1; i++) {
      connections.push({
        from: stateIds[i],
        to: stateIds[i + 1],
        type: 'sequential',
      });
    }
    
    // Last step to end
    connections.push({
      from: stateIds[stateIds.length - 1],
      to: endId,
      type: 'sequential',
    });
  }
  
  return {
    id: generateFlowId(),
    name: `Flow: ${input.name}`,
    description: `State flow for ${input.name}`,
    states,
    connections,
    entry_state: startId,
    exit_states: [endId],
    metadata: {},
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

/**
 * Get next possible states from a given state
 */
export function nextStates(flow: StateFlow, stateId: string): FlowState[] {
  const outgoingConnections = flow.connections.filter(c => c.from === stateId);
  const nextStateIds = outgoingConnections.map(c => c.to);
  return flow.states.filter(s => nextStateIds.includes(s.id));
}

/**
 * Get previous states that lead to a given state
 */
export function previousStates(flow: StateFlow, stateId: string): FlowState[] {
  const incomingConnections = flow.connections.filter(c => c.to === stateId);
  const prevStateIds = incomingConnections.map(c => c.from);
  return flow.states.filter(s => prevStateIds.includes(s.id));
}

/**
 * Describe a state flow
 */
export function describeFlow(flow: StateFlow): string {
  const lines: string[] = [
    `Flow: ${flow.name}`,
    `States: ${flow.states.length}`,
    `Connections: ${flow.connections.length}`,
    '',
    'States:',
  ];
  
  flow.states.forEach(state => {
    const next = nextStates(flow, state.id);
    const nextNames = next.map(s => s.name).join(', ') || 'none';
    lines.push(`  [${state.type}] ${state.name} → ${nextNames}`);
  });
  
  return lines.join('\n');
}

/**
 * Analyze flow structure
 */
export function analyzeFlow(flow: StateFlow): FlowAnalysis {
  // Check for cycles (simplified — check if any state can reach itself)
  const hasCycles = flow.connections.some(c => c.from === c.to);
  
  // Count decision points
  const decisionPoints = flow.states.filter(s => s.type === 'decision').length;
  
  // Count parallel sections
  const parallelSplits = flow.connections.filter(c => c.type === 'parallel_split').length;
  
  // Calculate max depth (simplified — longest path from start)
  let maxDepth = 0;
  const visited = new Set<string>();
  
  function traverse(stateId: string, depth: number) {
    if (visited.has(stateId)) return;
    visited.add(stateId);
    maxDepth = Math.max(maxDepth, depth);
    
    const next = flow.connections.filter(c => c.from === stateId);
    next.forEach(c => traverse(c.to, depth + 1));
  }
  
  traverse(flow.entry_state, 0);
  
  return {
    total_states: flow.states.length,
    total_connections: flow.connections.length,
    has_cycles: hasCycles,
    parallel_sections: parallelSplits,
    decision_points: decisionPoints,
    max_depth: maxDepth,
  };
}

/**
 * Get all paths through the flow (simplified)
 */
export function getAllPaths(flow: StateFlow, maxPaths: number = 10): string[][] {
  const paths: string[][] = [];
  
  function findPaths(currentId: string, currentPath: string[]) {
    if (paths.length >= maxPaths) return;
    
    const state = flow.states.find(s => s.id === currentId);
    if (!state) return;
    
    const newPath = [...currentPath, state.name];
    
    if (state.type === 'end') {
      paths.push(newPath);
      return;
    }
    
    const next = flow.connections.filter(c => c.from === currentId);
    next.forEach(c => {
      if (!currentPath.includes(flow.states.find(s => s.id === c.to)?.name || '')) {
        findPaths(c.to, newPath);
      }
    });
  }
  
  findPaths(flow.entry_state, []);
  
  return paths;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'StateFlowEngine',
    version: '1.0.0',
    description: 'Representational state flow modeling',
    parent: 'SimulationEngine',
    safe: {
      isRepresentational: true,
      noAutonomy: true,
    },
  };
}

export default {
  buildStateFlow,
  nextStates,
  previousStates,
  describeFlow,
  analyzeFlow,
  getAllPaths,
  meta,
};

============================================================
SECTION A3 — SUB-MODULE: VariationEngine
============================================================

--- FILE: /che-nu-sdk/core/simulation/variation.engine.ts

/**
 * CHE·NU SDK — Variation Engine
 * ==============================
 * SAFE · NON-AUTONOMOUS · REPRESENTATIONAL
 * 
 * Represents "what-if" SAFE symbolic variations.
 * NO prediction, NO optimization — only structure.
 * 
 * @module VariationEngine
 * @version 1.0.0
 */

// ============================================================
// TYPE DEFINITIONS
// ============================================================

/**
 * Variation type
 */
export type VariationType = 
  | 'alternative_path'
  | 'parameter_change'
  | 'resource_change'
  | 'timing_change'
  | 'scope_change'
  | 'approach_change';

/**
 * Variation point — where divergence can occur
 */
export interface VariationPoint {
  id: string;
  location: string;           // ID of step/state where variation occurs
  location_name: string;
  type: VariationType;
  description: string;
  alternatives: VariationAlternative[];
  metadata: Record<string, unknown>;
}

/**
 * Single alternative variation
 */
export interface VariationAlternative {
  id: string;
  name: string;
  description: string;
  changes: string[];          // What would change in this variation
  affected_elements: string[]; // IDs of affected steps/states
  weight: number;             // Representational weight (not probability)
  metadata: Record<string, unknown>;
}

/**
 * Complete variation analysis
 */
export interface VariationAnalysis {
  id: string;
  subject_id: string;
  subject_name: string;
  variation_points: VariationPoint[];
  total_variations: number;
  complexity_score: number;   // Representational complexity
  metadata: Record<string, unknown>;
  safe: {
    isRepresentational: true;
    noAutonomy: true;
    noPrediction: true;
    noOptimization: true;
  };
}

/**
 * Variation summary
 */
export interface VariationSummary {
  total_points: number;
  total_alternatives: number;
  variation_types: Record<VariationType, number>;
  most_variable_area: string;
}

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

function generateVariationId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `var_${timestamp}_${random}`;
}

function generatePointId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `vpoint_${timestamp}_${random}`;
}

function generateAltId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 4);
  return `valt_${timestamp}_${random}`;
}

// ============================================================
// MAIN FUNCTIONS
// ============================================================

/**
 * Generate variations for a structure
 */
export function generateVariations(
  structure: {
    id: string;
    name: string;
    steps?: Array<{
      id: string;
      name: string;
      required_engines?: string[];
      tags?: string[];
    }>;
    transitions?: Array<{
      from: string;
      to: string;
      condition: string;
      type: string;
    }>;
  }
): VariationAnalysis {
  const variationPoints: VariationPoint[] = [];
  
  // Analyze steps for variation points
  if (structure.steps) {
    structure.steps.forEach(step => {
      // Decision points are natural variation points
      const isDecisionPoint = step.tags?.includes('decision') || step.tags?.includes('gate');
      
      if (isDecisionPoint) {
        variationPoints.push({
          id: generatePointId(),
          location: step.id,
          location_name: step.name,
          type: 'alternative_path',
          description: `Decision point with multiple possible outcomes`,
          alternatives: [
            {
              id: generateAltId(),
              name: 'Approve Path',
              description: 'Proceed with approval',
              changes: ['Continue to next phase'],
              affected_elements: [step.id],
              weight: 0.6,
              metadata: {},
            },
            {
              id: generateAltId(),
              name: 'Reject Path',
              description: 'Rejection or revision required',
              changes: ['Return to previous step', 'Additional review needed'],
              affected_elements: [step.id],
              weight: 0.3,
              metadata: {},
            },
            {
              id: generateAltId(),
              name: 'Defer Path',
              description: 'Decision deferred',
              changes: ['Hold for more information'],
              affected_elements: [step.id],
              weight: 0.1,
              metadata: {},
            },
          ],
          metadata: {},
        });
      }
      
      // Steps with multiple engines have approach variations
      if (step.required_engines && step.required_engines.length > 1) {
        variationPoints.push({
          id: generatePointId(),
          location: step.id,
          location_name: step.name,
          type: 'approach_change',
          description: `Multiple engine approaches available`,
          alternatives: step.required_engines.map(engine => ({
            id: generateAltId(),
            name: `${engine} Primary`,
            description: `Emphasize ${engine} approach`,
            changes: [`Primary engine: ${engine}`],
            affected_elements: [step.id],
            weight: 1 / step.required_engines!.length,
            metadata: { engine },
          })),
          metadata: {},
        });
      }
    });
  }
  
  // Analyze transitions for variation points
  if (structure.transitions) {
    const conditionalTransitions = structure.transitions.filter(
      t => t.type === 'conditional' || t.type === 'loop'
    );
    
    conditionalTransitions.forEach(trans => {
      const existingPoint = variationPoints.find(vp => vp.location === trans.from);
      
      if (!existingPoint) {
        variationPoints.push({
          id: generatePointId(),
          location: trans.from,
          location_name: trans.from,
          type: 'alternative_path',
          description: `Conditional transition: ${trans.condition}`,
          alternatives: [
            {
              id: generateAltId(),
              name: 'Condition Met',
              description: `Proceed when: ${trans.condition}`,
              changes: [`Transition to ${trans.to}`],
              affected_elements: [trans.from, trans.to],
              weight: 0.5,
              metadata: {},
            },
            {
              id: generateAltId(),
              name: 'Condition Not Met',
              description: 'Alternative path when condition fails',
              changes: ['Alternative transition'],
              affected_elements: [trans.from],
              weight: 0.5,
              metadata: {},
            },
          ],
          metadata: { transition: trans },
        });
      }
    });
  }
  
  // Calculate complexity
  const totalAlternatives = variationPoints.reduce(
    (sum, vp) => sum + vp.alternatives.length, 
    0
  );
  const complexityScore = variationPoints.length * 2 + totalAlternatives;
  
  return {
    id: generateVariationId(),
    subject_id: structure.id,
    subject_name: structure.name,
    variation_points: variationPoints,
    total_variations: totalAlternatives,
    complexity_score: complexityScore,
    metadata: {},
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPrediction: true,
      noOptimization: true,
    },
  };
}

/**
 * Find branch points in a structure
 */
export function branchPoints(
  structure: {
    steps?: Array<{ id: string; name: string; tags?: string[] }>;
    transitions?: Array<{ from: string; to: string; type: string }>;
  }
): Array<{ id: string; name: string; reason: string }> {
  const points: Array<{ id: string; name: string; reason: string }> = [];
  
  // Decision steps
  if (structure.steps) {
    structure.steps.forEach(step => {
      if (step.tags?.includes('decision') || step.tags?.includes('gate')) {
        points.push({
          id: step.id,
          name: step.name,
          reason: 'Decision/gate step',
        });
      }
    });
  }
  
  // Steps with multiple outgoing transitions
  if (structure.transitions) {
    const transitionCounts = new Map<string, number>();
    structure.transitions.forEach(t => {
      transitionCounts.set(t.from, (transitionCounts.get(t.from) || 0) + 1);
    });
    
    transitionCounts.forEach((count, stepId) => {
      if (count > 1 && !points.some(p => p.id === stepId)) {
        const step = structure.steps?.find(s => s.id === stepId);
        points.push({
          id: stepId,
          name: step?.name || stepId,
          reason: `Multiple outgoing paths (${count})`,
        });
      }
    });
  }
  
  return points;
}

/**
 * Summarize variation analysis
 */
export function variationSummary(analysis: VariationAnalysis): VariationSummary {
  const typeCounts: Record<VariationType, number> = {
    alternative_path: 0,
    parameter_change: 0,
    resource_change: 0,
    timing_change: 0,
    scope_change: 0,
    approach_change: 0,
  };
  
  analysis.variation_points.forEach(vp => {
    typeCounts[vp.type]++;
  });
  
  // Find most variable area
  let mostVariableArea = 'none';
  let maxAlternatives = 0;
  
  analysis.variation_points.forEach(vp => {
    if (vp.alternatives.length > maxAlternatives) {
      maxAlternatives = vp.alternatives.length;
      mostVariableArea = vp.location_name;
    }
  });
  
  return {
    total_points: analysis.variation_points.length,
    total_alternatives: analysis.total_variations,
    variation_types: typeCounts,
    most_variable_area: mostVariableArea,
  };
}

/**
 * Get variation at a specific location
 */
export function getVariationAt(
  analysis: VariationAnalysis,
  locationId: string
): VariationPoint | null {
  return analysis.variation_points.find(vp => vp.location === locationId) || null;
}

/**
 * List all alternatives across all variation points
 */
export function listAllAlternatives(
  analysis: VariationAnalysis
): Array<{ point: string; alternative: VariationAlternative }> {
  const results: Array<{ point: string; alternative: VariationAlternative }> = [];
  
  analysis.variation_points.forEach(vp => {
    vp.alternatives.forEach(alt => {
      results.push({
        point: vp.location_name,
        alternative: alt,
      });
    });
  });
  
  return results;
}

/**
 * Module metadata
 */
export function meta(): Record<string, unknown> {
  return {
    name: 'VariationEngine',
    version: '1.0.0',
    description: 'Representational what-if variation modeling',
    parent: 'SimulationEngine',
    variationTypes: [
      'alternative_path',
      'parameter_change',
      'resource_change',
      'timing_change',
      'scope_change',
      'approach_change',
    ],
    safe: {
      isRepresentational: true,
      noAutonomy: true,
      noPrediction: true,
      noOptimization: true,
    },
  };
}

export default {
  generateVariations,
  branchPoints,
  variationSummary,
  getVariationAt,
  listAllAlternatives,
  meta,
};

============================================================
SECTION A4 — SIMULATION SCHEMA
============================================================

--- FILE: /che-nu-sdk/schemas/simulation.schema.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://che-nu.ai/schemas/simulation.schema.json",
  "title": "CHE·NU Simulation Schema",
  "description": "JSON Schema for CHE·NU representational simulations",
  "type": "object",
  "required": ["id", "subject_type", "subject_id", "main_timeline", "safe"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique simulation identifier",
      "pattern": "^sim_[a-z0-9]+_[a-z0-9]+$"
    },
    "name": {
      "type": "string",
      "description": "Simulation name"
    },
    "subject_type": {
      "type": "string",
      "description": "Type of subject being simulated",
      "enum": ["project", "mission", "process", "persona", "workflow", "pipeline"]
    },
    "subject_id": {
      "type": "string",
      "description": "ID of the subject being simulated"
    },
    "subject_name": {
      "type": "string",
      "description": "Name of the subject"
    },
    "main_timeline": {
      "type": "array",
      "description": "Main simulation timeline frames",
      "items": {
        "$ref": "#/definitions/simulation_frame"
      }
    },
    "branches": {
      "type": "array",
      "description": "Alternative branches",
      "items": {
        "$ref": "#/definitions/simulation_branch"
      }
    },
    "total_frames": {
      "type": "integer",
      "minimum": 0
    },
    "total_branches": {
      "type": "integer",
      "minimum": 0
    },
    "engines_involved": {
      "type": "array",
      "items": { "type": "string" }
    },
    "agents_involved": {
      "type": "array",
      "items": { "type": "string" }
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    },
    "safe": {
      "$ref": "#/definitions/safe_compliance"
    }
  },
  "definitions": {
    "simulation_frame": {
      "type": "object",
      "required": ["id", "timestamp", "state_id", "description"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^frame_[a-z0-9]+_[a-z0-9]+$"
        },
        "timestamp": {
          "type": "integer",
          "minimum": 0
        },
        "state_id": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "involved_engines": {
          "type": "array",
          "items": { "type": "string" }
        },
        "involved_agents": {
          "type": "array",
          "items": { "type": "string" }
        },
        "inputs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "outputs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "simulation_branch": {
      "type": "object",
      "required": ["id", "name", "branch_point", "frames"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^branch_[a-z0-9]+_[a-z0-9]+$"
        },
        "name": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "branch_point": {
          "type": "integer",
          "minimum": 0
        },
        "condition": {
          "type": "string"
        },
        "frames": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/simulation_frame"
          }
        },
        "probability_weight": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "safe_compliance": {
      "type": "object",
      "required": ["isRepresentational", "noAutonomy", "noExecution", "noPrediction"],
      "properties": {
        "isRepresentational": {
          "type": "boolean",
          "const": true
        },
        "noAutonomy": {
          "type": "boolean",
          "const": true
        },
        "noExecution": {
          "type": "boolean",
          "const": true
        },
        "noPrediction": {
          "type": "boolean",
          "const": true
        }
      }
    }
  },
  "additionalProperties": false
}

============================================================
END OF SIMULATION LAYER CORE
============================================================
