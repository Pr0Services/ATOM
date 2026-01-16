/**
 * CHE·NU™ IDENTITY & CONTEXT ISOLATION SYSTEM
 * Version 1.0 – CANONICAL
 * 
 * CORE PRINCIPLE:
 * CHE·NU assumes that a single human can hold MULTIPLE IDENTITIES.
 * These identities must NEVER bleed into each other by default.
 * 
 * CONTEXT ISOLATION IS STRICT.
 * SHARING IS ALWAYS EXPLICIT.
 */

// ═══════════════════════════════════════════════════════════════
// DEFINITIONS
// ═══════════════════════════════════════════════════════════════

/**
 * IDENTITY:
 * Represents WHO is acting
 * Examples: Personal Self, Business Role, Organization Role
 * 
 * CONTEXT:
 * Represents WHERE the action takes place
 * Defined by Sphere + Organization + Scope
 * 
 * SESSION:
 * A temporary binding between:
 * - one Identity
 * - one Context
 * - one Permission Set
 */

// ═══════════════════════════════════════════════════════════════
// IDENTITY TYPES (CANONICAL)
// ═══════════════════════════════════════════════════════════════

const IDENTITY_TYPES = {
  PERSONAL: {
    type: 'personal',
    name: 'Personal Identity',
    description: 'Default human identity',
    default_sphere_access: ['personal'],
    data_isolation: 'strict',
    rules: [
      'Access to Personal sphere by default',
      'Optional access to other spheres when explicitly granted',
      'Personal data never visible to other identities'
    ]
  },
  
  BUSINESS: {
    type: 'business',
    name: 'Business Identity',
    description: 'Linked to a specific company',
    default_sphere_access: ['business'],
    data_isolation: 'strict',
    requires_organization: true,
    rules: [
      'Isolated data, budget, agents',
      'No access to personal data by default',
      'Company-specific context and permissions',
      'Budget separate from personal budget'
    ]
  },
  
  ORGANIZATION: {
    type: 'organization',
    name: 'Organization / Institution Identity',
    description: 'Government, NGO, Enterprise',
    default_sphere_access: ['government', 'business'],
    data_isolation: 'strict',
    requires_organization: true,
    compliance_required: true,
    rules: [
      'Strong compliance constraints',
      'No cross-entity visibility',
      'Audit trail mandatory',
      'Enhanced security requirements'
    ]
  },
  
  ROLE_BASED: {
    type: 'role',
    name: 'Role-Based Identity',
    description: 'Temporary or functional role',
    default_sphere_access: [],
    data_isolation: 'strict',
    temporary: true,
    rules: [
      'Limited scope',
      'Time-bound or task-bound',
      'Permissions explicitly granted',
      'Auto-expires when role ends'
    ]
  }
};

// ═══════════════════════════════════════════════════════════════
// IDENTITY CLASS
// ═══════════════════════════════════════════════════════════════

class Identity {
  constructor(data) {
    this.id = data.id || `identity-${Date.now()}`;
    this.user_id = data.user_id;
    this.type = data.type; // IDENTITY_TYPES
    this.name = data.name;
    this.description = data.description;
    
    // Organization link (if applicable)
    this.organization_id = data.organization_id || null;
    this.organization_name = data.organization_name || null;
    
    // Sphere access
    this.allowed_spheres = data.allowed_spheres || [];
    
    // Permissions
    this.permissions = data.permissions || [];
    
    // Budget
    this.budget_id = data.budget_id || null;
    
    // Status
    this.is_active = data.is_active !== undefined ? data.is_active : true;
    this.is_default = data.is_default || false;
    
    // Time bounds (for role-based)
    this.valid_from = data.valid_from || null;
    this.valid_until = data.valid_until || null;
    
    // Metadata
    this.created_at = data.created_at || new Date().toISOString();
    this.last_used_at = data.last_used_at || null;
  }
  
  /**
   * Check if identity is valid
   */
  isValid() {
    if (!this.is_active) return false;
    
    // Check time bounds for role-based identities
    if (this.type === 'role') {
      const now = new Date();
      
      if (this.valid_from && new Date(this.valid_from) > now) {
        return false;
      }
      
      if (this.valid_until && new Date(this.valid_until) < now) {
        return false;
      }
    }
    
    return true;
  }
  
  /**
   * Check if identity can access sphere
   */
  canAccessSphere(sphereId) {
    return this.allowed_spheres.includes(sphereId);
  }
  
  /**
   * Check if identity has permission
   */
  hasPermission(permission) {
    return this.permissions.includes(permission);
  }
  
  /**
   * Update last used timestamp
   */
  updateLastUsed() {
    this.last_used_at = new Date().toISOString();
  }
}

// ═══════════════════════════════════════════════════════════════
// CONTEXT CLASS
// ═══════════════════════════════════════════════════════════════

class Context {
  constructor(data) {
    this.id = data.id || `context-${Date.now()}`;
    
    // Context definition
    this.sphere_id = data.sphere_id;
    this.organization_id = data.organization_id || null;
    this.project_id = data.project_id || null;
    
    // Permissions (inherited from identity + context-specific)
    this.permissions = data.permissions || [];
    
    // Budget (context-specific)
    this.budget_id = data.budget_id || null;
    
    // Isolation level
    this.isolation_level = data.isolation_level || 'strict';
    
    // Metadata
    this.created_at = data.created_at || new Date().toISOString();
  }
  
  /**
   * Check if context matches criteria
   */
  matches(criteria) {
    if (criteria.sphere_id && criteria.sphere_id !== this.sphere_id) {
      return false;
    }
    
    if (criteria.organization_id && criteria.organization_id !== this.organization_id) {
      return false;
    }
    
    if (criteria.project_id && criteria.project_id !== this.project_id) {
      return false;
    }
    
    return true;
  }
  
  /**
   * Get context key (unique identifier)
   */
  getKey() {
    return [
      this.sphere_id,
      this.organization_id || 'no-org',
      this.project_id || 'no-project'
    ].join(':');
  }
}

// ═══════════════════════════════════════════════════════════════
// SESSION CLASS
// ═══════════════════════════════════════════════════════════════

class Session {
  constructor(data) {
    this.id = data.id || `session-${Date.now()}`;
    
    // Session binding
    this.user_id = data.user_id;
    this.identity_id = data.identity_id;
    this.context_id = data.context_id;
    
    // References
    this.identity = null; // Loaded from Identity
    this.context = null;  // Loaded from Context
    
    // State
    this.is_active = true;
    this.started_at = new Date().toISOString();
    this.last_activity_at = new Date().toISOString();
    this.ended_at = null;
    
    // Working state (cleared on identity switch)
    this.working_context = {};
    this.cached_suggestions = [];
    this.temporary_memory = {};
  }
  
  /**
   * Clear working state (on identity switch)
   */
  clearWorkingState() {
    this.working_context = {};
    this.cached_suggestions = [];
    this.temporary_memory = {};
  }
  
  /**
   * Update activity timestamp
   */
  updateActivity() {
    this.last_activity_at = new Date().toISOString();
  }
  
  /**
   * End session
   */
  end() {
    this.is_active = false;
    this.ended_at = new Date().toISOString();
    this.clearWorkingState();
  }
}

// ═══════════════════════════════════════════════════════════════
// IDENTITY RULES (NON-NEGOTIABLE)
// ═══════════════════════════════════════════════════════════════

const IDENTITY_RULES = {
  ONE_ACTIVE_PER_SESSION: {
    rule: 'One active identity per session',
    enforcement: 'strict',
    rationale: 'Prevents context confusion and data leakage'
  },
  
  EXPLICIT_SWITCHING: {
    rule: 'Identity switching requires explicit action',
    enforcement: 'strict',
    rationale: 'No automatic or background identity changes'
  },
  
  CLEAR_ON_SWITCH: {
    rule: 'Identity switch clears working context, cached suggestions, temporary memory',
    enforcement: 'strict',
    items_cleared: [
      'working_context',
      'cached_suggestions',
      'temporary_memory'
    ],
    rationale: 'Prevents cross-identity contamination'
  },
  
  NO_BACKGROUND_PERSISTENCE: {
    rule: 'No background execution persists across identity switches',
    enforcement: 'strict',
    rationale: 'Execution is identity-bound'
  }
};

// ═══════════════════════════════════════════════════════════════
// DATA VISIBILITY RULES
// ═══════════════════════════════════════════════════════════════

const DATA_VISIBILITY_RULES = {
  PERSONAL: {
    visibility: 'Personal data is visible ONLY in Personal identity',
    cross_access: false,
    sharing_required: 'explicit'
  },
  
  BUSINESS: {
    visibility: 'Business data is visible ONLY within that business identity',
    cross_access: false,
    sharing_required: 'explicit'
  },
  
  COMMUNITY: {
    visibility: 'Community data is public but still contextual',
    cross_access: true,
    context_aware: true
  },
  
  GOVERNMENT: {
    visibility: 'Government data is strictly isolated',
    cross_access: false,
    compliance_required: true,
    audit_mandatory: true
  },
  
  PRINCIPLE: 'REFERENCING is allowed. COPYING is forbidden unless explicitly requested.'
};

// ═══════════════════════════════════════════════════════════════
// AGENT VISIBILITY & ISOLATION
// ═══════════════════════════════════════════════════════════════

const AGENT_ISOLATION_RULES = {
  INHERITANCE: {
    principle: 'Agents inherit active identity, context, permissions, budget',
    inherits: [
      'active_identity',
      'active_context',
      'active_permissions',
      'active_budget'
    ]
  },
  
  VISIBILITY: {
    rule: 'Agents cannot see data outside their context',
    enforcement: 'strict',
    violation: 'blocked'
  },
  
  ACCESS_REQUEST: {
    rule: 'Agents cannot request broader access',
    enforcement: 'strict',
    only_user_can: 'grant access'
  },
  
  MEMORY: {
    rule: 'Agents cannot remember across identities unless explicitly allowed',
    enforcement: 'strict',
    memory_scope: 'identity-bound'
  }
};

// ═══════════════════════════════════════════════════════════════
// NOVA VISIBILITY RULES
// ═══════════════════════════════════════════════════════════════

const NOVA_VISIBILITY_RULES = {
  AWARENESS: {
    principle: 'Nova is context-aware, not omniscient',
    scope: 'active_context_only'
  },
  
  MAY: [
    'guide within the active context',
    'explain context boundaries',
    'warn about isolation rules'
  ],
  
  MAY_NOT: [
    'recall data from another identity',
    'reference another context without permission',
    'suggest cross-identity sharing without confirmation'
  ],
  
  ROLE: 'Nova respects identity boundaries absolutely'
};

// ═══════════════════════════════════════════════════════════════
// ORCHESTRATOR RULES
// ═══════════════════════════════════════════════════════════════

const ORCHESTRATOR_RULES = {
  SCOPE: {
    rule: 'Orchestrator operates only within the active identity',
    enforcement: 'strict'
  },
  
  EXECUTION: {
    rule: 'Executes tasks only in the active context',
    enforcement: 'strict'
  },
  
  IDENTITY_SWITCH: {
    rule: 'Must stop execution on identity switch',
    enforcement: 'immediate',
    invalidation: 'Orchestrator tasks are invalidated if context changes'
  }
};

// ═══════════════════════════════════════════════════════════════
// SHARING MODES
// ═══════════════════════════════════════════════════════════════

const SHARING_MODES = {
  REFERENCE: {
    mode: 'reference',
    description: 'Link to original data (default)',
    creates_copy: false,
    updates_sync: true
  },
  
  COPY: {
    mode: 'copy',
    description: 'Duplicate data to destination',
    creates_copy: true,
    updates_sync: false,
    requires_explicit: true
  }
};

const DEFAULT_SHARING_MODE = 'reference';

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  IDENTITY_TYPES,
  Identity,
  Context,
  Session,
  IDENTITY_RULES,
  DATA_VISIBILITY_RULES,
  AGENT_ISOLATION_RULES,
  NOVA_VISIBILITY_RULES,
  ORCHESTRATOR_RULES,
  SHARING_MODES,
  DEFAULT_SHARING_MODE
};
