/**
 * CHE·NU™ IDENTITY MANAGER
 * 
 * Manages identity switching, session handling, and context isolation.
 * 
 * CRITICAL RULES:
 * 1. One active identity per session
 * 2. Identity switching requires explicit action
 * 3. Identity switch clears working state
 * 4. No background execution across switches
 */

const { 
  IDENTITY_TYPES, 
  Identity, 
  Context, 
  Session,
  IDENTITY_RULES,
  DATA_VISIBILITY_RULES
} = require('./IDENTITY_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// IDENTITY MANAGER
// ═══════════════════════════════════════════════════════════════

class IdentityManager {
  constructor(pool) {
    this.pool = pool;
    this.activeSessions = new Map(); // user_id -> Session
  }
  
  /**
   * Create new identity for user
   */
  async createIdentity(userId, identityData) {
    const identityType = IDENTITY_TYPES[identityData.type.toUpperCase()];
    if (!identityType) {
      throw new Error(`Invalid identity type: ${identityData.type}`);
    }
    
    // Validate organization requirement
    if (identityType.requires_organization && !identityData.organization_id) {
      throw new Error(`Identity type ${identityType.name} requires organization_id`);
    }
    
    // Create identity
    const identity = new Identity({
      user_id: userId,
      type: identityData.type,
      name: identityData.name,
      description: identityData.description,
      organization_id: identityData.organization_id,
      organization_name: identityData.organization_name,
      allowed_spheres: identityData.allowed_spheres || identityType.default_sphere_access,
      permissions: identityData.permissions || [],
      budget_id: identityData.budget_id,
      valid_from: identityData.valid_from,
      valid_until: identityData.valid_until
    });
    
    // Save to database
    const result = await this.pool.query(
      `INSERT INTO identities 
       (id, user_id, type, name, description, organization_id, organization_name,
        allowed_spheres, permissions, budget_id, is_active, is_default,
        valid_from, valid_until, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
       RETURNING *`,
      [
        identity.id,
        identity.user_id,
        identity.type,
        identity.name,
        identity.description,
        identity.organization_id,
        identity.organization_name,
        JSON.stringify(identity.allowed_spheres),
        JSON.stringify(identity.permissions),
        identity.budget_id,
        identity.is_active,
        identity.is_default,
        identity.valid_from,
        identity.valid_until,
        identity.created_at
      ]
    );
    
    return new Identity(this.parseIdentityRow(result.rows[0]));
  }
  
  /**
   * Get all identities for user
   */
  async getUserIdentities(userId) {
    const result = await this.pool.query(
      `SELECT * FROM identities 
       WHERE user_id = $1 AND is_active = true
       ORDER BY is_default DESC, created_at ASC`,
      [userId]
    );
    
    return result.rows.map(row => new Identity(this.parseIdentityRow(row)));
  }
  
  /**
   * Get identity by ID
   */
  async getIdentity(identityId) {
    const result = await this.pool.query(
      `SELECT * FROM identities WHERE id = $1`,
      [identityId]
    );
    
    if (result.rows.length === 0) {
      throw new Error('Identity not found');
    }
    
    return new Identity(this.parseIdentityRow(result.rows[0]));
  }
  
  /**
   * Get default identity for user
   */
  async getDefaultIdentity(userId) {
    const result = await this.pool.query(
      `SELECT * FROM identities 
       WHERE user_id = $1 AND is_default = true AND is_active = true
       LIMIT 1`,
      [userId]
    );
    
    if (result.rows.length === 0) {
      // Create default personal identity
      return await this.createIdentity(userId, {
        type: 'personal',
        name: 'Personal',
        description: 'Default personal identity',
        is_default: true,
        allowed_spheres: ['personal']
      });
    }
    
    return new Identity(this.parseIdentityRow(result.rows[0]));
  }
  
  /**
   * Switch to different identity (EXPLICIT ACTION REQUIRED)
   */
  async switchIdentity(userId, newIdentityId, reason = null) {
    // Get current session
    const currentSession = this.activeSessions.get(userId);
    
    // Get new identity
    const newIdentity = await this.getIdentity(newIdentityId);
    
    // Validate identity belongs to user
    if (newIdentity.user_id !== userId) {
      throw new Error('Identity does not belong to user');
    }
    
    // Validate identity is valid
    if (!newIdentity.isValid()) {
      throw new Error('Identity is not valid');
    }
    
    // IDENTITY SWITCH FLOW:
    // 1. Current execution is paused or stopped
    if (currentSession) {
      await this.pauseCurrentExecution(currentSession);
    }
    
    // 2. Temporary context is cleared
    if (currentSession) {
      currentSession.clearWorkingState();
      currentSession.end();
    }
    
    // 3. Nova confirms new identity (returned to caller)
    const confirmation = {
      previous_identity: currentSession ? currentSession.identity_id : null,
      new_identity: newIdentity.id,
      new_identity_type: newIdentity.type,
      new_identity_name: newIdentity.name,
      timestamp: new Date().toISOString()
    };
    
    // 4. New permissions are loaded (from identity)
    // 5. New budget constraints apply (from identity)
    
    // Create new session (context will be set separately)
    const newSession = new Session({
      user_id: userId,
      identity_id: newIdentity.id
    });
    
    newSession.identity = newIdentity;
    
    // Update active session
    this.activeSessions.set(userId, newSession);
    
    // Log identity switch
    await this.logIdentitySwitch(
      userId,
      currentSession ? currentSession.identity_id : null,
      newIdentity.id,
      reason
    );
    
    // Update identity last used
    newIdentity.updateLastUsed();
    await this.pool.query(
      `UPDATE identities SET last_used_at = $1 WHERE id = $2`,
      [newIdentity.last_used_at, newIdentity.id]
    );
    
    return {
      session: newSession,
      confirmation,
      message: 'Identity switched successfully. Previous session cleared.'
    };
  }
  
  /**
   * Set context for current session
   */
  async setContext(userId, contextData) {
    const session = this.activeSessions.get(userId);
    if (!session) {
      throw new Error('No active session');
    }
    
    // Validate identity can access sphere
    if (!session.identity.canAccessSphere(contextData.sphere_id)) {
      throw new Error(`Identity cannot access sphere: ${contextData.sphere_id}`);
    }
    
    // Create context
    const context = new Context(contextData);
    
    // Save context
    const result = await this.pool.query(
      `INSERT INTO contexts 
       (id, sphere_id, organization_id, project_id, permissions, budget_id, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [
        context.id,
        context.sphere_id,
        context.organization_id,
        context.project_id,
        JSON.stringify(context.permissions),
        context.budget_id,
        context.created_at
      ]
    );
    
    // Update session
    session.context_id = context.id;
    session.context = context;
    session.updateActivity();
    
    return context;
  }
  
  /**
   * Get active session for user
   */
  getActiveSession(userId) {
    const session = this.activeSessions.get(userId);
    
    if (!session) {
      throw new Error('No active session');
    }
    
    // Validate session
    if (!session.is_active) {
      throw new Error('Session is not active');
    }
    
    if (!session.identity) {
      throw new Error('Session has no identity');
    }
    
    if (!session.context) {
      throw new Error('Session has no context');
    }
    
    return session;
  }
  
  /**
   * Pause current execution (on identity switch)
   */
  async pauseCurrentExecution(session) {
    // Stop any running agents
    await this.pool.query(
      `UPDATE agent_tasks 
       SET status = 'paused', 
           paused_at = NOW(),
           pause_reason = 'identity_switch'
       WHERE user_id = $1 AND status = 'running'`,
      [session.user_id]
    );
    
    // Stop orchestrator tasks
    await this.pool.query(
      `UPDATE orchestrator_tasks 
       SET status = 'invalidated',
           invalidated_at = NOW(),
           invalidation_reason = 'identity_switch'
       WHERE user_id = $1 AND status IN ('pending', 'running')`,
      [session.user_id]
    );
  }
  
  /**
   * Log identity switch
   */
  async logIdentitySwitch(userId, fromIdentityId, toIdentityId, reason) {
    await this.pool.query(
      `INSERT INTO identity_switches 
       (user_id, from_identity_id, to_identity_id, reason, switched_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [userId, fromIdentityId, toIdentityId, reason]
    );
  }
  
  /**
   * Check data visibility
   */
  canAccessData(session, dataIdentityType) {
    const identityType = session.identity.type;
    
    // Personal data only visible in personal identity
    if (dataIdentityType === 'personal' && identityType !== 'personal') {
      return false;
    }
    
    // Business data only visible in same business identity
    if (dataIdentityType === 'business') {
      if (identityType !== 'business') return false;
      // Additional check: same organization
      // (would need organization_id comparison)
    }
    
    // Community data is public but contextual
    if (dataIdentityType === 'community') {
      return true;
    }
    
    // Government data strictly isolated
    if (dataIdentityType === 'government') {
      if (identityType !== 'organization') return false;
      // Additional compliance checks would go here
    }
    
    return true;
  }
  
  /**
   * Validate action against identity rules
   */
  validateAction(session, action) {
    const errors = [];
    
    // Check if identity/context is clear
    if (!session.identity || !session.context) {
      errors.push('Identity or context is ambiguous');
    }
    
    // Check if identity is valid
    if (session.identity && !session.identity.isValid()) {
      errors.push('Identity is not valid');
    }
    
    // Check permissions
    if (action.required_permission) {
      if (!session.identity.hasPermission(action.required_permission)) {
        errors.push(`Missing permission: ${action.required_permission}`);
      }
    }
    
    // Check sphere access
    if (action.sphere_id) {
      if (!session.identity.canAccessSphere(action.sphere_id)) {
        errors.push(`Cannot access sphere: ${action.sphere_id}`);
      }
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  /**
   * Get identity context info (for Nova/agents)
   */
  getContextInfo(session) {
    return {
      who: {
        identity_id: session.identity.id,
        identity_type: session.identity.type,
        identity_name: session.identity.name
      },
      where: {
        sphere_id: session.context.sphere_id,
        organization_id: session.context.organization_id,
        project_id: session.context.project_id
      },
      with_what: {
        permissions: session.identity.permissions,
        budget_id: session.identity.budget_id || session.context.budget_id
      }
    };
  }
  
  /**
   * Parse identity row from database
   */
  parseIdentityRow(row) {
    return {
      ...row,
      allowed_spheres: typeof row.allowed_spheres === 'string' 
        ? JSON.parse(row.allowed_spheres) 
        : row.allowed_spheres,
      permissions: typeof row.permissions === 'string'
        ? JSON.parse(row.permissions)
        : row.permissions
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// IDENTITY SWITCH VALIDATOR
// ═══════════════════════════════════════════════════════════════

class IdentitySwitchValidator {
  /**
   * Validate if identity switch is allowed
   */
  static validate(currentIdentity, targetIdentity, reason) {
    const errors = [];
    
    // Check if target identity is valid
    if (!targetIdentity.isValid()) {
      errors.push('Target identity is not valid');
    }
    
    // Check if reason is provided for auditing
    if (!reason) {
      errors.push('Identity switch reason is required for audit');
    }
    
    // Additional validation rules can be added here
    
    return {
      allowed: errors.length === 0,
      errors,
      requires_confirmation: true,
      will_clear: IDENTITY_RULES.CLEAR_ON_SWITCH.items_cleared
    };
  }
  
  /**
   * Check if identity/context is ambiguous
   */
  static isAmbiguous(session) {
    if (!session) return true;
    if (!session.identity) return true;
    if (!session.context) return true;
    if (!session.identity.isValid()) return true;
    
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════
// FAILURE HANDLER
// ═══════════════════════════════════════════════════════════════

class IdentityFailureHandler {
  /**
   * Handle ambiguous identity/context
   */
  static handleAmbiguousIdentity() {
    return {
      status: 'blocked',
      reason: 'ambiguous_identity_or_context',
      message: 'Cannot determine WHO is acting, WHERE, and WITH WHAT PERMISSIONS',
      action_required: 'User must clarify identity and context',
      nova_should_ask: true,
      execution_stopped: true
    };
  }
  
  /**
   * Handle failed identity switch
   */
  static handleFailedSwitch(error, currentIdentity, targetIdentity) {
    return {
      status: 'failed',
      reason: 'identity_switch_failed',
      error: error.message,
      current_identity: currentIdentity ? currentIdentity.id : null,
      target_identity: targetIdentity ? targetIdentity.id : null,
      message: 'Identity switch failed. Remaining in current identity.',
      rollback_completed: true
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  IdentityManager,
  IdentitySwitchValidator,
  IdentityFailureHandler
};
