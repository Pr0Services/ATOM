/**
 * CHE·NU™ MODE MANAGER
 * 
 * Manages user mode transitions and feature visibility.
 * 
 * CRITICAL RULES:
 * - Users may move forward freely (with confirmation)
 * - Downgrading is always allowed
 * - Upgrading requires confirmation
 * - Mode change is logged
 * - No automatic mode escalation
 */

const {
  USER_MODES,
  MODE_TRANSITION_RULES,
  FEATURE_VISIBILITY_MATRIX,
  AGENT_AUTONOMY_BY_MODE
} = require('./USER_MODES_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// USER MODE CLASS
// ═══════════════════════════════════════════════════════════════

class UserMode {
  constructor(data) {
    this.user_id = data.user_id;
    this.current_mode = data.current_mode || 'discovery';
    this.previous_mode = data.previous_mode || null;
    
    // Mode history
    this.mode_history = data.mode_history || [];
    
    // Settings
    this.auto_suggest_upgrade = data.auto_suggest_upgrade !== undefined 
      ? data.auto_suggest_upgrade 
      : true;
    
    // Timestamps
    this.created_at = data.created_at || new Date().toISOString();
    this.updated_at = data.updated_at || new Date().toISOString();
  }
  
  /**
   * Get current mode configuration
   */
  getModeConfig() {
    return USER_MODES[this.current_mode.toUpperCase()];
  }
  
  /**
   * Check if feature is visible in current mode
   */
  isFeatureVisible(featureName) {
    const visibility = FEATURE_VISIBILITY_MATRIX[featureName];
    if (!visibility) return false;
    
    const modeVisibility = visibility[this.current_mode];
    
    if (typeof modeVisibility === 'boolean') {
      return modeVisibility;
    }
    
    if (modeVisibility === 'user_selected' || 
        modeVisibility === 'if_enabled' ||
        modeVisibility === 'view_only' ||
        modeVisibility === 'limited') {
      return true; // Feature exists but with restrictions
    }
    
    return false;
  }
  
  /**
   * Get agent autonomy for current mode
   */
  getAgentAutonomy() {
    return AGENT_AUTONOMY_BY_MODE[this.current_mode];
  }
  
  /**
   * Check if agent level is allowed
   */
  isAgentLevelAllowed(agentLevel) {
    const autonomy = this.getAgentAutonomy();
    
    if (!autonomy.agents_visible) return false;
    if (autonomy.max_level === null) return false;
    
    return agentLevel <= autonomy.max_level;
  }
}

// ═══════════════════════════════════════════════════════════════
// MODE MANAGER
// ═══════════════════════════════════════════════════════════════

class ModeManager {
  constructor(pool) {
    this.pool = pool;
  }
  
  /**
   * Get or create user mode
   */
  async getUserMode(userId) {
    const result = await this.pool.query(
      `SELECT * FROM user_modes WHERE user_id = $1`,
      [userId]
    );
    
    if (result.rows.length === 0) {
      // Create default mode (discovery)
      return await this.createUserMode(userId, 'discovery');
    }
    
    return new UserMode(this.parseUserModeRow(result.rows[0]));
  }
  
  /**
   * Create user mode
   */
  async createUserMode(userId, initialMode = 'discovery') {
    const userMode = new UserMode({
      user_id: userId,
      current_mode: initialMode
    });
    
    await this.pool.query(
      `INSERT INTO user_modes 
       (user_id, current_mode, mode_history, auto_suggest_upgrade, created_at, updated_at)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [
        userMode.user_id,
        userMode.current_mode,
        JSON.stringify(userMode.mode_history),
        userMode.auto_suggest_upgrade,
        userMode.created_at,
        userMode.updated_at
      ]
    );
    
    return userMode;
  }
  
  /**
   * Request mode change
   * Returns validation result
   */
  async requestModeChange(userId, targetMode) {
    const userMode = await this.getUserMode(userId);
    const currentConfig = USER_MODES[userMode.current_mode.toUpperCase()];
    const targetConfig = USER_MODES[targetMode.toUpperCase()];
    
    if (!targetConfig) {
      return {
        allowed: false,
        error: `Unknown target mode: ${targetMode}`
      };
    }
    
    const isUpgrade = targetConfig.level > currentConfig.level;
    const isDowngrade = targetConfig.level < currentConfig.level;
    
    // Validate transition
    if (isUpgrade) {
      return {
        allowed: true,
        requires_confirmation: true,
        type: 'upgrade',
        message: MODE_TRANSITION_RULES.FORWARD.message,
        from: userMode.current_mode,
        to: targetMode,
        changes: this.getFeatureChanges(userMode.current_mode, targetMode)
      };
    }
    
    if (isDowngrade) {
      return {
        allowed: true,
        requires_confirmation: false,
        type: 'downgrade',
        message: MODE_TRANSITION_RULES.DOWNGRADE.message,
        from: userMode.current_mode,
        to: targetMode,
        changes: this.getFeatureChanges(userMode.current_mode, targetMode)
      };
    }
    
    // Same level (no change)
    return {
      allowed: false,
      error: 'Already in this mode'
    };
  }
  
  /**
   * Execute mode change (after confirmation if required)
   */
  async changeModeMode(userId, targetMode, confirmed = false) {
    const validation = await this.requestModeChange(userId, targetMode);
    
    if (!validation.allowed) {
      throw new Error(validation.error);
    }
    
    if (validation.requires_confirmation && !confirmed) {
      throw new Error('User confirmation required for mode upgrade');
    }
    
    const userMode = await this.getUserMode(userId);
    const previousMode = userMode.current_mode;
    
    // Update mode
    userMode.previous_mode = previousMode;
    userMode.current_mode = targetMode;
    userMode.updated_at = new Date().toISOString();
    
    // Add to history
    userMode.mode_history.push({
      from: previousMode,
      to: targetMode,
      changed_at: userMode.updated_at,
      type: validation.type
    });
    
    // Save to database
    await this.pool.query(
      `UPDATE user_modes 
       SET current_mode = $1, previous_mode = $2, 
           mode_history = $3, updated_at = $4
       WHERE user_id = $5`,
      [
        userMode.current_mode,
        userMode.previous_mode,
        JSON.stringify(userMode.mode_history),
        userMode.updated_at,
        userId
      ]
    );
    
    // Log mode change
    await this.logModeChange(userId, previousMode, targetMode, validation.type);
    
    return {
      success: true,
      previous_mode: previousMode,
      new_mode: targetMode,
      type: validation.type,
      changes: validation.changes,
      message: `Successfully switched to ${targetConfig.name}`
    };
  }
  
  /**
   * Get feature changes between modes
   */
  getFeatureChanges(fromMode, toMode) {
    const changes = {
      newly_visible: [],
      newly_hidden: [],
      changed_behavior: []
    };
    
    for (const [feature, visibility] of Object.entries(FEATURE_VISIBILITY_MATRIX)) {
      const fromVisibility = visibility[fromMode];
      const toVisibility = visibility[toMode];
      
      // Feature becomes visible
      if (!fromVisibility && toVisibility) {
        changes.newly_visible.push(feature);
      }
      
      // Feature becomes hidden
      if (fromVisibility && !toVisibility) {
        changes.newly_hidden.push(feature);
      }
      
      // Feature behavior changes
      if (fromVisibility !== toVisibility && 
          fromVisibility && toVisibility) {
        changes.changed_behavior.push({
          feature,
          from: fromVisibility,
          to: toVisibility
        });
      }
    }
    
    return changes;
  }
  
  /**
   * Check if feature should be visible for user
   */
  async isFeatureVisible(userId, featureName) {
    const userMode = await this.getUserMode(userId);
    return userMode.isFeatureVisible(featureName);
  }
  
  /**
   * Get visible features for user
   */
  async getVisibleFeatures(userId) {
    const userMode = await this.getUserMode(userId);
    const modeConfig = userMode.getModeConfig();
    
    return {
      mode: userMode.current_mode,
      mode_level: modeConfig.level,
      visible: modeConfig.visible,
      automation: modeConfig.automation,
      nova_role: modeConfig.nova_role
    };
  }
  
  /**
   * Get agent permissions for user
   */
  async getAgentPermissions(userId) {
    const userMode = await this.getUserMode(userId);
    return userMode.getAgentAutonomy();
  }
  
  /**
   * Check if user can use agent level
   */
  async canUseAgentLevel(userId, agentLevel) {
    const userMode = await this.getUserMode(userId);
    return userMode.isAgentLevelAllowed(agentLevel);
  }
  
  /**
   * Suggest mode upgrade (if appropriate)
   */
  async suggestModeUpgrade(userId, reason) {
    const userMode = await this.getUserMode(userId);
    
    if (!userMode.auto_suggest_upgrade) {
      return null;
    }
    
    const currentConfig = USER_MODES[userMode.current_mode.toUpperCase()];
    
    // Don't suggest if already in Architect mode
    if (currentConfig.level === 4) {
      return null;
    }
    
    // Get next mode
    const nextModeLevel = currentConfig.level + 1;
    const nextMode = Object.values(USER_MODES).find(m => m.level === nextModeLevel);
    
    if (!nextMode) return null;
    
    return {
      suggested: true,
      current_mode: userMode.current_mode,
      suggested_mode: nextMode.mode,
      reason,
      message: `Consider upgrading to ${nextMode.name} for ${reason}`,
      requires_confirmation: true
    };
  }
  
  /**
   * Log mode change
   */
  async logModeChange(userId, fromMode, toMode, type) {
    await this.pool.query(
      `INSERT INTO mode_change_log 
       (user_id, from_mode, to_mode, change_type, changed_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [userId, fromMode, toMode, type]
    );
  }
  
  /**
   * Get mode change history
   */
  async getModeHistory(userId, limit = 10) {
    const result = await this.pool.query(
      `SELECT * FROM mode_change_log 
       WHERE user_id = $1 
       ORDER BY changed_at DESC 
       LIMIT $2`,
      [userId, limit]
    );
    
    return result.rows;
  }
  
  /**
   * Parse user mode row from database
   */
  parseUserModeRow(row) {
    return {
      ...row,
      mode_history: typeof row.mode_history === 'string'
        ? JSON.parse(row.mode_history)
        : row.mode_history
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// MODE VALIDATOR
// ═══════════════════════════════════════════════════════════════

class ModeValidator {
  /**
   * Validate feature access based on user mode
   */
  static validateFeatureAccess(userMode, featureName) {
    const errors = [];
    
    if (!userMode.isFeatureVisible(featureName)) {
      const modeConfig = userMode.getModeConfig();
      errors.push(`Feature "${featureName}" not available in ${modeConfig.name}`);
      
      // Suggest mode upgrade
      const requiredMode = this.getRequiredMode(featureName);
      if (requiredMode) {
        errors.push(`Upgrade to ${requiredMode.name} to access this feature`);
      }
    }
    
    return {
      allowed: errors.length === 0,
      errors
    };
  }
  
  /**
   * Get required mode for feature
   */
  static getRequiredMode(featureName) {
    const visibility = FEATURE_VISIBILITY_MATRIX[featureName];
    if (!visibility) return null;
    
    // Find first mode where feature is visible
    for (const mode of Object.values(USER_MODES)) {
      const modeVisibility = visibility[mode.mode];
      if (modeVisibility) {
        return mode;
      }
    }
    
    return null;
  }
  
  /**
   * Validate agent usage based on mode
   */
  static validateAgentUsage(userMode, agentLevel) {
    const errors = [];
    
    if (!userMode.isAgentLevelAllowed(agentLevel)) {
      const autonomy = userMode.getAgentAutonomy();
      errors.push(`Agent level L${agentLevel} not allowed in ${userMode.current_mode} mode`);
      errors.push(`Maximum allowed level: L${autonomy.max_level || 'none'}`);
    }
    
    return {
      allowed: errors.length === 0,
      errors
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  UserMode,
  ModeManager,
  ModeValidator
};
