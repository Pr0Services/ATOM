/**
 * CHE·NU™ STATE TRANSITIONS MANAGER
 * 
 * Validates and executes lifecycle state transitions.
 * 
 * GENERAL TRANSITION RULES:
 * 1. No object may skip a lifecycle state
 * 2. No object may escalate automatically
 * 3. All transitions must be logged
 * 4. All irreversible transitions require explicit confirmation
 * 5. Nova may suggest transitions
 * 6. The Orchestrator may execute transitions only after approval
 */

const { LIFECYCLE_REGISTRY } = require('./LIFECYCLE_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// AUTOMATION BOUNDARIES
// ═══════════════════════════════════════════════════════════════

const AUTOMATION_BOUNDARIES = {
  MAY: [
    'suggest',
    'prepare',
    'simulate'
  ],
  
  MAY_NOT: [
    'decide',
    'escalate',
    'integrate',
    'publish',
    'archive'
  ],
  
  PRINCIPLE: 'Automation assists, User decides'
};

// ═══════════════════════════════════════════════════════════════
// TRANSITION VALIDATOR
// ═══════════════════════════════════════════════════════════════

class TransitionValidator {
  /**
   * Validate if transition is allowed
   */
  static validateTransition(objectType, currentState, targetState, context = {}) {
    const lifecycle = LIFECYCLE_REGISTRY[objectType];
    if (!lifecycle) {
      return {
        valid: false,
        errors: [`Unknown object type: ${objectType}`]
      };
    }
    
    // Check if states exist
    if (!lifecycle.states[currentState]) {
      return {
        valid: false,
        errors: [`Invalid current state: ${currentState}`]
      };
    }
    
    if (!lifecycle.states[targetState]) {
      return {
        valid: false,
        errors: [`Invalid target state: ${targetState}`]
      };
    }
    
    // Find transition definition
    const transition = lifecycle.transitions.find(
      t => t.from === currentState && t.to === targetState
    );
    
    if (!transition) {
      return {
        valid: false,
        errors: [`No valid transition from ${currentState} to ${targetState}`],
        suggestion: this.suggestValidTransitions(lifecycle, currentState)
      };
    }
    
    // Check requirements
    const requirementErrors = this.checkRequirements(transition, context);
    if (requirementErrors.length > 0) {
      return {
        valid: false,
        errors: requirementErrors,
        requires: transition.requires
      };
    }
    
    return {
      valid: true,
      transition,
      immediate: transition.immediate || false,
      reversible: transition.reversible || false
    };
  }
  
  /**
   * Check if transition requirements are met
   */
  static checkRequirements(transition, context) {
    const errors = [];
    const { requires } = transition;
    
    if (!requires) return errors;
    
    switch (requires) {
      case 'user_validation':
      case 'user_confirmation':
      case 'user_action':
      case 'explicit_user_action':
        if (!context.user_confirmed) {
          errors.push(`Requires ${requires}`);
        }
        break;
        
      case 'approval':
        if (!context.approved_by) {
          errors.push('Requires approval from authorized user');
        }
        break;
        
      case 'reason':
        if (!context.reason) {
          errors.push('Requires reason for transition');
        }
        break;
        
      case 'first_message':
        if (!context.has_messages) {
          errors.push('Requires at least one message');
        }
        break;
        
      case 'explicit_decision':
        if (!context.decision_recorded) {
          errors.push('Requires explicit decision to be recorded');
        }
        break;
        
      case 'user_review':
        if (!context.reviewed_by) {
          errors.push('Requires user review');
        }
        break;
        
      case 'experiments_complete':
        if (!context.experiments_passed) {
          errors.push('Requires all experiments to be completed successfully');
        }
        break;
        
      case 'validation_passed':
        if (!context.validation_score || context.validation_score < 0.8) {
          errors.push('Requires validation score >= 0.8');
        }
        break;
        
      case 'promotion_approval':
        if (!context.promotion_approved_by) {
          errors.push('Requires promotion approval from authorized user');
        }
        break;
    }
    
    return errors;
  }
  
  /**
   * Suggest valid transitions from current state
   */
  static suggestValidTransitions(lifecycle, currentState) {
    const validTransitions = lifecycle.transitions
      .filter(t => t.from === currentState)
      .map(t => ({
        to: t.to,
        requires: t.requires,
        description: lifecycle.states[t.to].description
      }));
    
    return validTransitions;
  }
  
  /**
   * Check if transition is reversible
   */
  static isReversible(objectType, fromState, toState) {
    const lifecycle = LIFECYCLE_REGISTRY[objectType];
    if (!lifecycle) return false;
    
    const targetStateInfo = lifecycle.states[toState];
    if (!targetStateInfo) return false;
    
    return targetStateInfo.reversible_from && 
           targetStateInfo.reversible_from.includes(fromState);
  }
  
  /**
   * Check if automation is allowed for this action
   */
  static canAutomate(action) {
    return AUTOMATION_BOUNDARIES.MAY.includes(action);
  }
  
  /**
   * Check if action requires user decision
   */
  static requiresUserDecision(action) {
    return AUTOMATION_BOUNDARIES.MAY_NOT.includes(action);
  }
}

// ═══════════════════════════════════════════════════════════════
// TRANSITION EXECUTOR
// ═══════════════════════════════════════════════════════════════

class TransitionExecutor {
  constructor(pool) {
    this.pool = pool;
  }
  
  /**
   * Execute state transition
   */
  async executeTransition(objectType, objectId, targetState, context = {}) {
    // Get current state
    const currentState = await this.getCurrentState(objectType, objectId);
    if (!currentState) {
      throw new Error(`Object not found: ${objectType}/${objectId}`);
    }
    
    // Validate transition
    const validation = TransitionValidator.validateTransition(
      objectType,
      currentState,
      targetState,
      context
    );
    
    if (!validation.valid) {
      return {
        success: false,
        errors: validation.errors,
        current_state: currentState,
        suggestions: validation.suggestion
      };
    }
    
    // Check if state is unclear (ambiguous context)
    if (this.isStateAmbiguous(context)) {
      return {
        success: false,
        reason: 'state_unclear',
        message: 'State transition is ambiguous. Execution paused.',
        requires_clarification: true,
        current_state: currentState
      };
    }
    
    // Execute transition
    try {
      await this.pool.query('BEGIN');
      
      // Update object state
      await this.updateState(objectType, objectId, targetState);
      
      // Log transition
      await this.logTransition(
        objectType,
        objectId,
        currentState,
        targetState,
        context
      );
      
      // Execute state-specific actions
      await this.executeStateActions(objectType, objectId, targetState, context);
      
      await this.pool.query('COMMIT');
      
      return {
        success: true,
        previous_state: currentState,
        new_state: targetState,
        timestamp: new Date().toISOString(),
        immediate: validation.immediate,
        reversible: validation.reversible
      };
      
    } catch (error) {
      await this.pool.query('ROLLBACK');
      
      return {
        success: false,
        errors: [error.message],
        current_state: currentState,
        failure_mode: 'safe_failure'
      };
    }
  }
  
  /**
   * Get current state of object
   */
  async getCurrentState(objectType, objectId) {
    const tableName = this.getTableName(objectType);
    const result = await this.pool.query(
      `SELECT state FROM ${tableName} WHERE id = $1`,
      [objectId]
    );
    
    if (result.rows.length === 0) return null;
    return result.rows[0].state;
  }
  
  /**
   * Update object state
   */
  async updateState(objectType, objectId, newState) {
    const tableName = this.getTableName(objectType);
    await this.pool.query(
      `UPDATE ${tableName} 
       SET state = $1, state_updated_at = NOW()
       WHERE id = $2`,
      [newState, objectId]
    );
  }
  
  /**
   * Log transition to audit trail
   */
  async logTransition(objectType, objectId, fromState, toState, context) {
    await this.pool.query(
      `INSERT INTO state_transitions 
       (object_type, object_id, from_state, to_state, 
        user_id, context, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, NOW())`,
      [
        objectType,
        objectId,
        fromState,
        toState,
        context.user_id || null,
        JSON.stringify(context)
      ]
    );
  }
  
  /**
   * Execute state-specific actions
   */
  async executeStateActions(objectType, objectId, newState, context) {
    // Implement state-specific side effects
    // Examples:
    // - Send notifications
    // - Update related objects
    // - Trigger workflows
    // - Update permissions
    
    const lifecycle = LIFECYCLE_REGISTRY[objectType];
    const stateInfo = lifecycle.states[newState];
    
    // Handle immutable states
    if (stateInfo.immutable) {
      await this.markAsImmutable(objectType, objectId);
    }
    
    // Handle read-only states
    if (stateInfo.read_only) {
      await this.setReadOnly(objectType, objectId, true);
    }
    
    // Handle archiving
    if (newState === 'ARCHIVED') {
      await this.handleArchiving(objectType, objectId);
    }
  }
  
  /**
   * Check if state is ambiguous
   */
  isStateAmbiguous(context) {
    // If intent is unclear, return true
    if (context.intent_unclear) return true;
    if (context.requires_clarification) return true;
    
    return false;
  }
  
  /**
   * Mark object as immutable
   */
  async markAsImmutable(objectType, objectId) {
    const tableName = this.getTableName(objectType);
    await this.pool.query(
      `UPDATE ${tableName} SET immutable = true WHERE id = $1`,
      [objectId]
    );
  }
  
  /**
   * Set read-only flag
   */
  async setReadOnly(objectType, objectId, readOnly) {
    const tableName = this.getTableName(objectType);
    await this.pool.query(
      `UPDATE ${tableName} SET read_only = $1 WHERE id = $2`,
      [readOnly, objectId]
    );
  }
  
  /**
   * Handle archiving
   */
  async handleArchiving(objectType, objectId) {
    const tableName = this.getTableName(objectType);
    await this.pool.query(
      `UPDATE ${tableName} 
       SET archived_at = NOW(), read_only = true 
       WHERE id = $1`,
      [objectId]
    );
  }
  
  /**
   * Get table name for object type
   */
  getTableName(objectType) {
    const tableMap = {
      note: 'notes',
      task: 'tasks',
      project: 'projects',
      thread: 'threads',
      document: 'documents',
      meeting: 'meetings',
      skill: 'skills',
      agent: 'agents',
      permission: 'permissions',
      budget: 'budgets'
    };
    
    return tableMap[objectType] || objectType + 's';
  }
  
  /**
   * Suggest next transition to user
   */
  async suggestTransition(objectType, objectId) {
    const currentState = await this.getCurrentState(objectType, objectId);
    if (!currentState) {
      throw new Error('Object not found');
    }
    
    const lifecycle = LIFECYCLE_REGISTRY[objectType];
    const suggestions = TransitionValidator.suggestValidTransitions(
      lifecycle,
      currentState
    );
    
    return {
      object_type: objectType,
      object_id: objectId,
      current_state: currentState,
      suggestions,
      note: 'Nova may suggest these transitions, user decides'
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// FAILURE & UNCERTAINTY HANDLER
// ═══════════════════════════════════════════════════════════════

class FailureHandler {
  /**
   * Handle ambiguous state transition
   */
  static handleAmbiguousTransition(objectType, objectId, context) {
    return {
      status: 'paused',
      reason: 'ambiguous_state_transition',
      message: 'State transition is unclear. Please clarify your intent.',
      object_type: objectType,
      object_id: objectId,
      requires_user_input: true,
      nova_should_ask: true,
      principle: 'CHE·NU must fail safely'
    };
  }
  
  /**
   * Handle failed transition
   */
  static handleFailedTransition(error, objectType, objectId, currentState) {
    return {
      status: 'failed',
      error: error.message,
      object_type: objectType,
      object_id: objectId,
      current_state: currentState,
      rollback_completed: true,
      safe_failure: true,
      message: 'Transition failed safely. Object remains in previous state.'
    };
  }
  
  /**
   * Handle missing requirements
   */
  static handleMissingRequirements(requirements, context) {
    return {
      status: 'blocked',
      reason: 'missing_requirements',
      missing: requirements,
      context,
      nova_should_ask: true,
      message: 'Cannot proceed without required information'
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  TransitionValidator,
  TransitionExecutor,
  FailureHandler,
  AUTOMATION_BOUNDARIES
};
