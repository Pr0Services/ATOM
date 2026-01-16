/**
 * CHE·NU™ IA LABS SYSTEM
 * 
 * IA LABS is a controlled experimentation space.
 * It is NOT a production workspace.
 * 
 * IA LABS is used to:
 * - test new skills
 * - combine tools
 * - adjust parameters
 * - evaluate performance and cost
 * - validate safety and usefulness
 * 
 * Only validated skills can be promoted outside IA LABS.
 */

const { SKILLS_CATALOG } = require('../skills/SKILLS_CATALOG');
const { TOOLS_REGISTRY } = require('../tools/TOOLS_REGISTRY');

// ═══════════════════════════════════════════════════════════════
// IA LABS ENVIRONMENT
// ═══════════════════════════════════════════════════════════════

const IA_LABS_CONFIG = {
  name: 'IA Labs',
  type: 'experimentation',
  isolation_level: 'strict',
  production_impact: 'none',
  
  // Budget limits for experiments
  max_budget_per_experiment: 500,
  max_concurrent_experiments: 3,
  max_experiment_duration: 600, // 10 minutes
  
  // Safety
  requires_approval: true,
  auto_rollback: true,
  output_sandboxed: true
};

// ═══════════════════════════════════════════════════════════════
// EXPERIMENT STATES
// ═══════════════════════════════════════════════════════════════

const EXPERIMENT_STATES = {
  DRAFT: 'draft',           // Being configured
  PENDING: 'pending',       // Awaiting approval
  RUNNING: 'running',       // Active experiment
  COMPLETED: 'completed',   // Finished successfully
  FAILED: 'failed',         // Experiment failed
  CANCELLED: 'cancelled',   // User cancelled
  VALIDATED: 'validated',   // Ready for promotion
  PROMOTED: 'promoted'      // Moved to production
};

// ═══════════════════════════════════════════════════════════════
// EXPERIMENT CLASS
// ═══════════════════════════════════════════════════════════════

class Experiment {
  constructor(data) {
    this.id = data.id || `exp-${Date.now()}`;
    this.name = data.name;
    this.description = data.description;
    this.created_by = data.created_by;
    this.created_at = new Date().toISOString();
    
    // What's being tested
    this.type = data.type; // 'skill_test', 'tool_combo', 'parameter_tuning', 'safety_validation'
    this.skills = data.skills || [];
    this.tools = data.tools || [];
    this.parameters = data.parameters || {};
    
    // Constraints
    this.budget_allocated = data.budget_allocated || 100;
    this.budget_used = 0;
    this.time_limit = data.time_limit || 300; // seconds
    
    // State
    this.state = EXPERIMENT_STATES.DRAFT;
    this.results = [];
    this.metrics = {
      success_rate: 0,
      avg_cost: 0,
      avg_duration: 0,
      quality_score: 0
    };
    
    // Safety
    this.safety_checks_passed = false;
    this.validation_notes = [];
  }
  
  /**
   * Validate experiment before running
   */
  validate() {
    const errors = [];
    
    // Check skills exist
    for (const skillName of this.skills) {
      const skill = Object.values(SKILLS_CATALOG).find(s => s.name === skillName);
      if (!skill) {
        errors.push(`Skill "${skillName}" not found in catalog`);
      }
    }
    
    // Check tools exist
    for (const toolName of this.tools) {
      const tool = TOOLS_REGISTRY[toolName];
      if (!tool) {
        errors.push(`Tool "${toolName}" not found in registry`);
      }
    }
    
    // Check budget
    if (this.budget_allocated > IA_LABS_CONFIG.max_budget_per_experiment) {
      errors.push(`Budget ${this.budget_allocated} exceeds max ${IA_LABS_CONFIG.max_budget_per_experiment}`);
    }
    
    // Check time limit
    if (this.time_limit > IA_LABS_CONFIG.max_experiment_duration) {
      errors.push(`Time limit ${this.time_limit}s exceeds max ${IA_LABS_CONFIG.max_experiment_duration}s`);
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  /**
   * Start experiment
   */
  async start() {
    const validation = this.validate();
    if (!validation.valid) {
      throw new Error(`Experiment validation failed: ${validation.errors.join(', ')}`);
    }
    
    this.state = EXPERIMENT_STATES.RUNNING;
    this.started_at = new Date().toISOString();
    
    return true;
  }
  
  /**
   * Record experiment result
   */
  recordResult(result) {
    this.results.push({
      timestamp: new Date().toISOString(),
      success: result.success,
      cost: result.cost,
      duration: result.duration,
      output: result.output,
      errors: result.errors || []
    });
    
    this.budget_used += result.cost;
    
    // Update metrics
    this.updateMetrics();
  }
  
  /**
   * Update experiment metrics
   */
  updateMetrics() {
    if (this.results.length === 0) return;
    
    const successes = this.results.filter(r => r.success).length;
    const totalCost = this.results.reduce((sum, r) => sum + r.cost, 0);
    const totalDuration = this.results.reduce((sum, r) => sum + r.duration, 0);
    
    this.metrics = {
      success_rate: successes / this.results.length,
      avg_cost: totalCost / this.results.length,
      avg_duration: totalDuration / this.results.length,
      total_runs: this.results.length,
      quality_score: this.calculateQualityScore()
    };
  }
  
  /**
   * Calculate overall quality score
   */
  calculateQualityScore() {
    // Quality = success_rate * cost_efficiency * speed
    const costEfficiency = Math.max(0, 1 - (this.metrics.avg_cost / this.budget_allocated));
    const speedScore = Math.max(0, 1 - (this.metrics.avg_duration / this.time_limit));
    
    return (this.metrics.success_rate * 0.5 + costEfficiency * 0.3 + speedScore * 0.2);
  }
  
  /**
   * Complete experiment
   */
  complete() {
    this.state = EXPERIMENT_STATES.COMPLETED;
    this.completed_at = new Date().toISOString();
    
    // Auto-validate if quality is high
    if (this.metrics.quality_score >= 0.8 && this.metrics.success_rate >= 0.9) {
      this.state = EXPERIMENT_STATES.VALIDATED;
    }
  }
  
  /**
   * Add validation note
   */
  addValidationNote(note, by) {
    this.validation_notes.push({
      timestamp: new Date().toISOString(),
      note,
      by
    });
  }
  
  /**
   * Promote to production
   */
  promoteToProduction() {
    if (this.state !== EXPERIMENT_STATES.VALIDATED) {
      throw new Error('Experiment must be validated before promotion');
    }
    
    this.state = EXPERIMENT_STATES.PROMOTED;
    this.promoted_at = new Date().toISOString();
    
    return {
      skills: this.skills,
      tools: this.tools,
      parameters: this.parameters,
      metrics: this.metrics
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// IA LABS MANAGER
// ═══════════════════════════════════════════════════════════════

class IALabsManager {
  constructor() {
    this.experiments = new Map();
    this.activeExperiments = 0;
  }
  
  /**
   * Create new experiment
   */
  createExperiment(data) {
    if (this.activeExperiments >= IA_LABS_CONFIG.max_concurrent_experiments) {
      throw new Error(`Maximum concurrent experiments (${IA_LABS_CONFIG.max_concurrent_experiments}) reached`);
    }
    
    const experiment = new Experiment(data);
    this.experiments.set(experiment.id, experiment);
    
    return experiment;
  }
  
  /**
   * Get experiment by ID
   */
  getExperiment(experimentId) {
    return this.experiments.get(experimentId);
  }
  
  /**
   * List experiments
   */
  listExperiments(filters = {}) {
    let experiments = Array.from(this.experiments.values());
    
    // Filter by state
    if (filters.state) {
      experiments = experiments.filter(exp => exp.state === filters.state);
    }
    
    // Filter by created_by
    if (filters.created_by) {
      experiments = experiments.filter(exp => exp.created_by === filters.created_by);
    }
    
    // Filter by type
    if (filters.type) {
      experiments = experiments.filter(exp => exp.type === filters.type);
    }
    
    return experiments;
  }
  
  /**
   * Start experiment
   */
  async startExperiment(experimentId) {
    const experiment = this.getExperiment(experimentId);
    if (!experiment) {
      throw new Error('Experiment not found');
    }
    
    if (this.activeExperiments >= IA_LABS_CONFIG.max_concurrent_experiments) {
      throw new Error('Maximum concurrent experiments reached');
    }
    
    await experiment.start();
    this.activeExperiments++;
    
    return experiment;
  }
  
  /**
   * Complete experiment
   */
  completeExperiment(experimentId) {
    const experiment = this.getExperiment(experimentId);
    if (!experiment) {
      throw new Error('Experiment not found');
    }
    
    experiment.complete();
    
    if (experiment.state === EXPERIMENT_STATES.COMPLETED || 
        experiment.state === EXPERIMENT_STATES.VALIDATED) {
      this.activeExperiments--;
    }
    
    return experiment;
  }
  
  /**
   * Validate experiment for promotion
   */
  validateExperiment(experimentId, validatedBy, notes) {
    const experiment = this.getExperiment(experimentId);
    if (!experiment) {
      throw new Error('Experiment not found');
    }
    
    if (experiment.state !== EXPERIMENT_STATES.COMPLETED) {
      throw new Error('Experiment must be completed before validation');
    }
    
    experiment.addValidationNote(notes, validatedBy);
    experiment.safety_checks_passed = true;
    experiment.state = EXPERIMENT_STATES.VALIDATED;
    
    return experiment;
  }
  
  /**
   * Promote validated experiment to production
   */
  promoteExperiment(experimentId) {
    const experiment = this.getExperiment(experimentId);
    if (!experiment) {
      throw new Error('Experiment not found');
    }
    
    return experiment.promoteToProduction();
  }
  
  /**
   * Cancel experiment
   */
  cancelExperiment(experimentId) {
    const experiment = this.getExperiment(experimentId);
    if (!experiment) {
      throw new Error('Experiment not found');
    }
    
    if (experiment.state === EXPERIMENT_STATES.RUNNING) {
      this.activeExperiments--;
    }
    
    experiment.state = EXPERIMENT_STATES.CANCELLED;
    return experiment;
  }
  
  /**
   * Get IA Labs statistics
   */
  getStatistics() {
    const all = Array.from(this.experiments.values());
    
    return {
      total_experiments: all.length,
      active: this.activeExperiments,
      completed: all.filter(e => e.state === EXPERIMENT_STATES.COMPLETED).length,
      validated: all.filter(e => e.state === EXPERIMENT_STATES.VALIDATED).length,
      promoted: all.filter(e => e.state === EXPERIMENT_STATES.PROMOTED).length,
      failed: all.filter(e => e.state === EXPERIMENT_STATES.FAILED).length,
      avg_quality_score: all
        .filter(e => e.metrics.quality_score > 0)
        .reduce((sum, e) => sum + e.metrics.quality_score, 0) / all.length || 0
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPERIMENT TEMPLATES
// ═══════════════════════════════════════════════════════════════

const EXPERIMENT_TEMPLATES = {
  skill_test: {
    name: 'Test New Skill',
    description: 'Test a new skill with various inputs',
    type: 'skill_test',
    budget_allocated: 100,
    time_limit: 300
  },
  
  tool_combination: {
    name: 'Test Tool Combination',
    description: 'Test combining multiple tools for a workflow',
    type: 'tool_combo',
    budget_allocated: 200,
    time_limit: 600
  },
  
  parameter_optimization: {
    name: 'Optimize Parameters',
    description: 'Find optimal parameters for a skill/tool',
    type: 'parameter_tuning',
    budget_allocated: 300,
    time_limit: 900
  },
  
  safety_validation: {
    name: 'Safety Validation',
    description: 'Validate safety and governance compliance',
    type: 'safety_validation',
    budget_allocated: 150,
    time_limit: 300
  }
};

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  Experiment,
  IALabsManager,
  IA_LABS_CONFIG,
  EXPERIMENT_STATES,
  EXPERIMENT_TEMPLATES
};
