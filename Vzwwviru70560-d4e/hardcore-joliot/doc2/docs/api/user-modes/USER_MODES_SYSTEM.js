/**
 * CHE·NU™ USER MODES & PROGRESSIVE DISCLOSURE SYSTEM
 * Version 1.0 – CANONICAL
 * 
 * CORE PRINCIPLE:
 * CHE·NU adapts its complexity to the USER, not the opposite.
 * 
 * Power is revealed progressively.
 * Clarity always comes before capability.
 * 
 * If the system is too complex to explain,
 * it must not be shown yet.
 */

// ═══════════════════════════════════════════════════════════════
// USER MODES (CANONICAL)
// ═══════════════════════════════════════════════════════════════

/**
 * Modes affect:
 * - UI density
 * - visible features
 * - automation level
 * - agent autonomy
 * - governance exposure
 * 
 * Modes are NOT cosmetic.
 * They are functional boundaries.
 */

const USER_MODES = {
  DISCOVERY: {
    mode: 'discovery',
    level: 1,
    name: 'Discovery Mode',
    description: 'First-time exploration, zero pressure',
    
    target: [
      'first-time users',
      'exploration',
      'zero pressure'
    ],
    
    visible: {
      navigation: 'minimal',
      spheres: ['personal'],
      sections: ['overview', 'notes', 'tasks'],
      community: 'read-only',
      nova: true,
      agents: false,
      budgets: false,
      ia_labs: false,
      multi_identity: false,
      advanced_settings: false
    },
    
    automation: {
      level: 'none',
      agents_allowed: [],
      max_agent_level: null,
      confirmations_required: 'all'
    },
    
    rules: [
      'no irreversible action',
      'no automation',
      'everything explained'
    ],
    
    nova_role: {
      primary: 'narrator',
      secondary: ['educator', 'guide'],
      behavior: 'Nova narrates and educates'
    },
    
    principle: 'Safe exploration without consequences'
  },
  
  FOCUS: {
    mode: 'focus',
    level: 2,
    name: 'Focus Mode',
    description: 'Daily productivity, single-context work',
    
    target: [
      'daily users',
      'productivity',
      'single-context work'
    ],
    
    visible: {
      navigation: 'streamlined',
      spheres: 'user_selected',
      sections: ['overview', 'notes', 'tasks', 'projects', 'threads', 'meetings'],
      community: 'read-write',
      nova: true,
      agents: ['L0'],
      budgets: 'hidden',
      ia_labs: false,
      multi_identity: false,
      advanced_settings: 'limited'
    },
    
    automation: {
      level: 'limited',
      agents_allowed: ['L0'],
      max_agent_level: 0,
      confirmations_required: 'important'
    },
    
    rules: [
      'limited automation',
      'confirmations required',
      'scope always visible'
    ],
    
    nova_role: {
      primary: 'assistant',
      secondary: ['clarifier', 'reminder'],
      behavior: 'Nova suggests, user decides'
    },
    
    principle: 'Productive without overwhelm'
  },
  
  POWER: {
    mode: 'power',
    level: 3,
    name: 'Power Mode',
    description: 'Advanced workflows, multi-project management',
    
    target: [
      'advanced users',
      'professionals',
      'multi-project workflows'
    ],
    
    visible: {
      navigation: 'complete',
      spheres: 'all',
      sections: 'all',
      community: 'read-write',
      nova: true,
      agents: ['L0', 'L1', 'L2'],
      budgets: 'visible',
      skill_configuration: true,
      identity_switching: true,
      ia_labs: 'if_enabled',
      advanced_settings: 'full'
    },
    
    automation: {
      level: 'moderate',
      agents_allowed: ['L0', 'L1', 'L2'],
      max_agent_level: 2,
      confirmations_required: 'critical_only'
    },
    
    rules: [
      'automation allowed within limits',
      'budget thresholds enforced',
      'audit logs always accessible'
    ],
    
    nova_role: {
      primary: 'coordinator',
      secondary: ['analyst', 'advisor'],
      behavior: 'Nova assists, orchestrator executes'
    },
    
    principle: 'Full power with guardrails'
  },
  
  ARCHITECT: {
    mode: 'architect',
    level: 4,
    name: 'Architect Mode',
    description: 'System building, administration, organization management',
    
    target: [
      'system builders',
      'admins',
      'organizations'
    ],
    
    visible: {
      navigation: 'complete',
      spheres: 'all',
      sections: 'all',
      community: 'read-write',
      nova: true,
      agents: ['L0', 'L1', 'L2', 'L3'],
      budgets: 'full_control',
      skill_configuration: 'full',
      identity_switching: 'full',
      ia_labs: 'full_access',
      agent_policies: true,
      security_permissions: true,
      system_configuration: true,
      advanced_settings: 'full'
    },
    
    automation: {
      level: 'full',
      agents_allowed: ['L0', 'L1', 'L2', 'L3'],
      max_agent_level: 3,
      confirmations_required: 'explicit_only'
    },
    
    rules: [
      'full responsibility',
      'no safety abstraction',
      'explicit confirmations required'
    ],
    
    nova_role: {
      primary: 'guardian',
      secondary: ['risk_notifier', 'policy_enforcer'],
      behavior: 'Nova warns, never assumes'
    },
    
    principle: 'Complete control, complete responsibility'
  }
};

// ═══════════════════════════════════════════════════════════════
// MODE TRANSITION RULES
// ═══════════════════════════════════════════════════════════════

const MODE_TRANSITION_RULES = {
  FORWARD: {
    allowed: true,
    requires_confirmation: true,
    message: 'You are unlocking more features. This increases complexity.'
  },
  
  DOWNGRADE: {
    allowed: true,
    requires_confirmation: false,
    message: 'You are simplifying your experience.'
  },
  
  NO_AUTO_ESCALATION: {
    rule: 'No automatic mode escalation',
    enforcement: 'strict',
    rationale: 'User must explicitly choose increased complexity'
  },
  
  LOGGED: {
    rule: 'Mode change is logged',
    enforcement: 'strict',
    audit: true
  }
};

// ═══════════════════════════════════════════════════════════════
// PROGRESSIVE DISCLOSURE RULES
// ═══════════════════════════════════════════════════════════════

const PROGRESSIVE_DISCLOSURE_RULES = {
  PRINCIPLE: 'Features appear only when needed and allowed',
  
  CONDITIONS: [
    'the user context requires them',
    'the user mode allows them',
    'Nova has explained them'
  ],
  
  HIDDEN_FEATURES: {
    rule: 'Hidden features still exist, but are not visible or distracting',
    enforcement: 'UI level',
    principle: 'Reduce cognitive load'
  },
  
  FEATURE_VISIBILITY: {
    discovery: 'minimal',
    focus: 'relevant',
    power: 'comprehensive',
    architect: 'complete'
  }
};

// ═══════════════════════════════════════════════════════════════
// FEATURE VISIBILITY MATRIX
// ═══════════════════════════════════════════════════════════════

const FEATURE_VISIBILITY_MATRIX = {
  // Core Navigation
  spheres: {
    discovery: ['personal'],
    focus: 'user_selected',
    power: 'all',
    architect: 'all'
  },
  
  // Bureau Sections
  overview: { discovery: true, focus: true, power: true, architect: true },
  notes: { discovery: true, focus: true, power: true, architect: true },
  tasks: { discovery: true, focus: true, power: true, architect: true },
  projects: { discovery: false, focus: true, power: true, architect: true },
  threads: { discovery: false, focus: true, power: true, architect: true },
  meetings: { discovery: false, focus: true, power: true, architect: true },
  data: { discovery: false, focus: false, power: true, architect: true },
  agents: { discovery: false, focus: 'limited', power: true, architect: true },
  reports: { discovery: false, focus: false, power: true, architect: true },
  governance: { discovery: false, focus: false, power: 'view_only', architect: true },
  
  // Advanced Features
  budgets: {
    discovery: false,
    focus: false,
    power: 'visible',
    architect: 'full_control'
  },
  
  ia_labs: {
    discovery: false,
    focus: false,
    power: 'if_enabled',
    architect: 'full_access'
  },
  
  multi_identity: {
    discovery: false,
    focus: false,
    power: true,
    architect: true
  },
  
  skill_configuration: {
    discovery: false,
    focus: false,
    power: 'basic',
    architect: 'full'
  },
  
  agent_policies: {
    discovery: false,
    focus: false,
    power: false,
    architect: true
  },
  
  system_configuration: {
    discovery: false,
    focus: false,
    power: false,
    architect: true
  },
  
  security_permissions: {
    discovery: false,
    focus: false,
    power: 'view_only',
    architect: 'full'
  }
};

// ═══════════════════════════════════════════════════════════════
// AGENT AUTONOMY BY MODE
// ═══════════════════════════════════════════════════════════════

const AGENT_AUTONOMY_BY_MODE = {
  discovery: {
    agents_visible: false,
    max_level: null,
    autonomy: 'none',
    confirmation: 'not_applicable'
  },
  
  focus: {
    agents_visible: true,
    max_level: 0,
    agents_allowed: ['L0'],
    autonomy: 'minimal',
    confirmation: 'always'
  },
  
  power: {
    agents_visible: true,
    max_level: 2,
    agents_allowed: ['L0', 'L1', 'L2'],
    autonomy: 'moderate',
    confirmation: 'critical_actions'
  },
  
  architect: {
    agents_visible: true,
    max_level: 3,
    agents_allowed: ['L0', 'L1', 'L2', 'L3'],
    autonomy: 'high',
    confirmation: 'explicit_only'
  }
};

// ═══════════════════════════════════════════════════════════════
// UI DENSITY BY MODE
// ═══════════════════════════════════════════════════════════════

const UI_DENSITY_BY_MODE = {
  discovery: {
    density: 'minimal',
    info_shown: 'essential_only',
    shortcuts: 'hidden',
    advanced_controls: 'hidden'
  },
  
  focus: {
    density: 'balanced',
    info_shown: 'relevant',
    shortcuts: 'contextual',
    advanced_controls: 'hidden'
  },
  
  power: {
    density: 'high',
    info_shown: 'comprehensive',
    shortcuts: 'visible',
    advanced_controls: 'visible'
  },
  
  architect: {
    density: 'maximum',
    info_shown: 'complete',
    shortcuts: 'visible',
    advanced_controls: 'always_visible'
  }
};

// ═══════════════════════════════════════════════════════════════
// NOVA BEHAVIOR BY MODE
// ═══════════════════════════════════════════════════════════════

const NOVA_BEHAVIOR_BY_MODE = {
  discovery: {
    role: 'narrator',
    proactiveness: 'high',
    explanations: 'detailed',
    suggestions: 'educational',
    warnings: 'always',
    principle: 'Nova narrates and educates'
  },
  
  focus: {
    role: 'assistant',
    proactiveness: 'moderate',
    explanations: 'concise',
    suggestions: 'practical',
    warnings: 'important_only',
    principle: 'Nova suggests, user decides'
  },
  
  power: {
    role: 'coordinator',
    proactiveness: 'low',
    explanations: 'on_request',
    suggestions: 'strategic',
    warnings: 'critical_only',
    principle: 'Nova assists, orchestrator executes'
  },
  
  architect: {
    role: 'guardian',
    proactiveness: 'minimal',
    explanations: 'on_request',
    suggestions: 'risk_focused',
    warnings: 'policy_violations',
    principle: 'Nova warns, never assumes'
  }
};

// ═══════════════════════════════════════════════════════════════
// FAILURE & SAFETY
// ═══════════════════════════════════════════════════════════════

const FAILURE_SAFETY = {
  PRINCIPLE: 'If a feature is too complex to explain, it must remain hidden or require Architect Mode',
  
  PROTECTION: 'CHE·NU must protect users from themselves',
  
  RULE: 'The user must always feel: in control, informed, capable',
  
  PHILOSOPHY: 'Complexity is a privilege, not a default'
};

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  USER_MODES,
  MODE_TRANSITION_RULES,
  PROGRESSIVE_DISCLOSURE_RULES,
  FEATURE_VISIBILITY_MATRIX,
  AGENT_AUTONOMY_BY_MODE,
  UI_DENSITY_BY_MODE,
  NOVA_BEHAVIOR_BY_MODE,
  FAILURE_SAFETY
};
