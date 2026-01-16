/**
 * CHE·NU™ PROGRESSIVE DISCLOSURE SYSTEM
 * 
 * Features appear only when:
 * - the user context requires them
 * - the user mode allows them
 * - Nova has explained them
 * 
 * Hidden features still exist,
 * but are not visible or distracting.
 * 
 * PRINCIPLE:
 * Reduce cognitive load through intelligent revelation.
 */

const { USER_MODES, PROGRESSIVE_DISCLOSURE_RULES } = require('./USER_MODES_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// FEATURE DISCLOSURE STATE
// ═══════════════════════════════════════════════════════════════

class FeatureDisclosureState {
  constructor(data) {
    this.user_id = data.user_id;
    this.feature_name = data.feature_name;
    
    // Disclosure state
    this.is_revealed = data.is_revealed || false;
    this.is_explained = data.is_explained || false;
    this.is_used = data.is_used || false;
    
    // Context
    this.revealed_in_mode = data.revealed_in_mode || null;
    this.revealed_by_context = data.revealed_by_context || null;
    
    // Nova explanation
    this.explanation_provided = data.explanation_provided || false;
    this.explanation_text = data.explanation_text || null;
    
    // Timestamps
    this.revealed_at = data.revealed_at || null;
    this.explained_at = data.explained_at || null;
    this.first_used_at = data.first_used_at || null;
  }
  
  /**
   * Reveal feature
   */
  reveal(mode, context) {
    this.is_revealed = true;
    this.revealed_in_mode = mode;
    this.revealed_by_context = context;
    this.revealed_at = new Date().toISOString();
  }
  
  /**
   * Mark as explained by Nova
   */
  explain(explanationText) {
    this.is_explained = true;
    this.explanation_provided = true;
    this.explanation_text = explanationText;
    this.explained_at = new Date().toISOString();
  }
  
  /**
   * Mark as used
   */
  markUsed() {
    if (!this.is_used) {
      this.is_used = true;
      this.first_used_at = new Date().toISOString();
    }
  }
  
  /**
   * Check if feature should be shown
   */
  shouldShow() {
    // Feature must be revealed
    if (!this.is_revealed) return false;
    
    // Feature should be explained before showing (optional for some features)
    // We'll be lenient here - reveal can happen without explanation
    
    return true;
  }
}

// ═══════════════════════════════════════════════════════════════
// DISCLOSURE TRIGGER
// ═══════════════════════════════════════════════════════════════

class DisclosureTrigger {
  constructor(data) {
    this.feature_name = data.feature_name;
    this.trigger_type = data.trigger_type; // 'mode_upgrade', 'context_need', 'user_action', 'time_based'
    this.trigger_condition = data.trigger_condition;
    this.priority = data.priority || 0; // Higher = more important
    this.explanation_required = data.explanation_required !== undefined 
      ? data.explanation_required 
      : true;
  }
  
  /**
   * Check if trigger condition is met
   */
  isTriggered(context) {
    switch (this.trigger_type) {
      case 'mode_upgrade':
        return context.user_mode === this.trigger_condition.required_mode;
        
      case 'context_need':
        return context.current_sphere === this.trigger_condition.sphere ||
               context.current_action === this.trigger_condition.action;
        
      case 'user_action':
        return context.action_count >= this.trigger_condition.min_actions;
        
      case 'time_based':
        const userAge = Date.now() - new Date(context.user_created_at).getTime();
        return userAge >= this.trigger_condition.min_age_ms;
        
      default:
        return false;
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// PROGRESSIVE DISCLOSURE MANAGER
// ═══════════════════════════════════════════════════════════════

class ProgressiveDisclosureManager {
  constructor(pool, modeManager) {
    this.pool = pool;
    this.modeManager = modeManager;
    this.triggers = this.initializeTriggers();
  }
  
  /**
   * Initialize disclosure triggers
   */
  initializeTriggers() {
    return [
      // Projects revealed when user has multiple tasks
      new DisclosureTrigger({
        feature_name: 'projects',
        trigger_type: 'user_action',
        trigger_condition: { min_actions: 5 },
        priority: 1,
        explanation_required: true
      }),
      
      // Threads revealed when user creates multiple related notes
      new DisclosureTrigger({
        feature_name: 'threads',
        trigger_type: 'user_action',
        trigger_condition: { min_actions: 10 },
        priority: 2,
        explanation_required: true
      }),
      
      // Agents revealed in Focus mode
      new DisclosureTrigger({
        feature_name: 'agents',
        trigger_type: 'mode_upgrade',
        trigger_condition: { required_mode: 'focus' },
        priority: 3,
        explanation_required: true
      }),
      
      // Budgets revealed in Power mode
      new DisclosureTrigger({
        feature_name: 'budgets',
        trigger_type: 'mode_upgrade',
        trigger_condition: { required_mode: 'power' },
        priority: 4,
        explanation_required: true
      }),
      
      // IA Labs revealed in Architect mode
      new DisclosureTrigger({
        feature_name: 'ia_labs',
        trigger_type: 'mode_upgrade',
        trigger_condition: { required_mode: 'architect' },
        priority: 5,
        explanation_required: true
      })
    ];
  }
  
  /**
   * Check what features should be disclosed to user
   */
  async checkDisclosures(userId, context) {
    const userMode = await this.modeManager.getUserMode(userId);
    const disclosures = [];
    
    for (const trigger of this.triggers) {
      // Check if feature is allowed in current mode
      if (!userMode.isFeatureVisible(trigger.feature_name)) {
        continue;
      }
      
      // Check if already disclosed
      const state = await this.getDisclosureState(userId, trigger.feature_name);
      if (state && state.is_revealed) {
        continue;
      }
      
      // Check if trigger condition is met
      if (trigger.isTriggered({ ...context, user_mode: userMode.current_mode })) {
        disclosures.push({
          feature_name: trigger.feature_name,
          priority: trigger.priority,
          explanation_required: trigger.explanation_required
        });
      }
    }
    
    // Sort by priority
    disclosures.sort((a, b) => b.priority - a.priority);
    
    return disclosures;
  }
  
  /**
   * Reveal feature to user
   */
  async revealFeature(userId, featureName, context) {
    const userMode = await this.modeManager.getUserMode(userId);
    
    // Validate feature is allowed in current mode
    if (!userMode.isFeatureVisible(featureName)) {
      throw new Error(`Feature ${featureName} not available in ${userMode.current_mode} mode`);
    }
    
    // Get or create disclosure state
    let state = await this.getDisclosureState(userId, featureName);
    if (!state) {
      state = new FeatureDisclosureState({
        user_id: userId,
        feature_name: featureName
      });
    }
    
    // Reveal feature
    state.reveal(userMode.current_mode, context);
    
    // Save state
    await this.saveDisclosureState(state);
    
    return state;
  }
  
  /**
   * Provide Nova explanation for feature
   */
  async explainFeature(userId, featureName, explanationText) {
    const state = await this.getDisclosureState(userId, featureName);
    if (!state) {
      throw new Error('Feature must be revealed before explanation');
    }
    
    state.explain(explanationText);
    await this.saveDisclosureState(state);
    
    return state;
  }
  
  /**
   * Mark feature as used
   */
  async markFeatureUsed(userId, featureName) {
    const state = await this.getDisclosureState(userId, featureName);
    if (!state) {
      // Auto-reveal if not revealed yet
      await this.revealFeature(userId, featureName, 'user_initiated');
      return await this.markFeatureUsed(userId, featureName);
    }
    
    state.markUsed();
    await this.saveDisclosureState(state);
    
    return state;
  }
  
  /**
   * Get disclosure state for feature
   */
  async getDisclosureState(userId, featureName) {
    const result = await this.pool.query(
      `SELECT * FROM feature_disclosure_state 
       WHERE user_id = $1 AND feature_name = $2`,
      [userId, featureName]
    );
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return new FeatureDisclosureState(result.rows[0]);
  }
  
  /**
   * Save disclosure state
   */
  async saveDisclosureState(state) {
    const exists = await this.getDisclosureState(state.user_id, state.feature_name);
    
    if (exists) {
      await this.pool.query(
        `UPDATE feature_disclosure_state 
         SET is_revealed = $1, is_explained = $2, is_used = $3,
             revealed_in_mode = $4, revealed_by_context = $5,
             explanation_provided = $6, explanation_text = $7,
             revealed_at = $8, explained_at = $9, first_used_at = $10
         WHERE user_id = $11 AND feature_name = $12`,
        [
          state.is_revealed,
          state.is_explained,
          state.is_used,
          state.revealed_in_mode,
          state.revealed_by_context,
          state.explanation_provided,
          state.explanation_text,
          state.revealed_at,
          state.explained_at,
          state.first_used_at,
          state.user_id,
          state.feature_name
        ]
      );
    } else {
      await this.pool.query(
        `INSERT INTO feature_disclosure_state 
         (user_id, feature_name, is_revealed, is_explained, is_used,
          revealed_in_mode, revealed_by_context, explanation_provided, 
          explanation_text, revealed_at, explained_at, first_used_at)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
        [
          state.user_id,
          state.feature_name,
          state.is_revealed,
          state.is_explained,
          state.is_used,
          state.revealed_in_mode,
          state.revealed_by_context,
          state.explanation_provided,
          state.explanation_text,
          state.revealed_at,
          state.explained_at,
          state.first_used_at
        ]
      );
    }
  }
  
  /**
   * Get all revealed features for user
   */
  async getRevealedFeatures(userId) {
    const result = await this.pool.query(
      `SELECT * FROM feature_disclosure_state 
       WHERE user_id = $1 AND is_revealed = true
       ORDER BY revealed_at ASC`,
      [userId]
    );
    
    return result.rows.map(row => new FeatureDisclosureState(row));
  }
  
  /**
   * Get features needing explanation
   */
  async getFeaturesNeedingExplanation(userId) {
    const result = await this.pool.query(
      `SELECT * FROM feature_disclosure_state 
       WHERE user_id = $1 AND is_revealed = true AND is_explained = false
       ORDER BY revealed_at ASC`,
      [userId]
    );
    
    return result.rows.map(row => new FeatureDisclosureState(row));
  }
  
  /**
   * Generate Nova explanation for feature
   */
  generateExplanation(featureName, userMode) {
    const explanations = {
      projects: {
        discovery: null,
        focus: "Projects help you organize related tasks over time. Think of them as folders for your work with milestones and deadlines.",
        power: "Projects give you advanced task organization with milestones, dependencies, and team collaboration.",
        architect: "Projects are structured workflows with full governance, resource allocation, and audit trails."
      },
      
      threads: {
        discovery: null,
        focus: "Threads are persistent conversations where you can work through problems and keep decisions organized.",
        power: "Threads (.chenu files) are your unit of truth - they preserve context, decisions, and links across your work.",
        architect: "Threads are immutable decision logs with complete traceability and cross-identity reference capabilities."
      },
      
      agents: {
        discovery: null,
        focus: "Simple agents (L0) can help with basic tasks like creating documents or organizing notes. You always approve their actions.",
        power: "Advanced agents (L1/L2) can handle complex workflows and remember context. They work within your budget and permissions.",
        architect: "Full agent stack (L0-L3) with master coordination, skill configuration, and policy enforcement."
      },
      
      budgets: {
        discovery: null,
        focus: null,
        power: "Budgets control how many tokens (AI resources) agents can use. This keeps costs predictable and manageable.",
        architect: "Complete budget governance with allocation, tracking, thresholds, and organizational policies."
      },
      
      ia_labs: {
        discovery: null,
        focus: null,
        power: "IA Labs is your experimentation space where you can test new skills and tools safely before using them in production.",
        architect: "IA Labs provides full experimentation workflow: test → validate → promote. Control skill lifecycle and performance."
      }
    };
    
    const explanation = explanations[featureName]?.[userMode];
    return explanation || `${featureName} is now available.`;
  }
  
  /**
   * Get disclosure suggestions for Nova
   */
  async getDisclosureSuggestions(userId, context) {
    const pendingDisclosures = await this.checkDisclosures(userId, context);
    
    if (pendingDisclosures.length === 0) {
      return null;
    }
    
    // Get top priority disclosure
    const topDisclosure = pendingDisclosures[0];
    const userMode = await this.modeManager.getUserMode(userId);
    
    return {
      feature_name: topDisclosure.feature_name,
      explanation: this.generateExplanation(topDisclosure.feature_name, userMode.current_mode),
      priority: topDisclosure.priority,
      suggestion: `You might find ${topDisclosure.feature_name} useful now. Would you like me to explain it?`
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  FeatureDisclosureState,
  DisclosureTrigger,
  ProgressiveDisclosureManager
};
