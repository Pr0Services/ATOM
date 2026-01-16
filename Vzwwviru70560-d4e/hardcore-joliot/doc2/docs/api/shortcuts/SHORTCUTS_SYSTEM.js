/**
 * CHE·NU™ SMART SHORTCUTS SYSTEM
 * 
 * Shortcuts are ACCELERATORS, not features.
 * 
 * Rules:
 * - maximum 3–5 shortcuts per sphere
 * - never bypass bureau hierarchy
 * - never shortcut to Governance
 * - always contextual
 * - always explainable by Nova
 * 
 * Shortcuts live in:
 * - Sphere Dashboard
 * - Context Header
 * - Nova voice suggestions
 */

// ═══════════════════════════════════════════════════════════════
// GLOBAL ORCHESTRATOR SHORTCUT
// ═══════════════════════════════════════════════════════════════

const GLOBAL_ORCHESTRATOR = {
  id: 'global-orchestrator',
  name: 'Orchestrator',
  type: 'global',
  icon: '🎯',
  description: 'General coordination and routing',
  
  purpose: [
    'Coordinate across spheres',
    'Route requests to correct bureau',
    'Delegate complex tasks',
    'Summarize multi-sphere context',
    'Open the correct bureau automatically'
  ],
  
  does_not: [
    'Create content directly',
    'Act as a social chat',
    'Make decisions without user approval'
  ],
  
  role_distinction: {
    nova: 'Observes and guides',
    orchestrator: 'Executes and coordinates'
  }
};

// ═══════════════════════════════════════════════════════════════
// SPHERE-SPECIFIC SHORTCUTS
// ═══════════════════════════════════════════════════════════════

const SPHERE_SHORTCUTS = {
  // Personal Sphere: 🏠
  personal: [
    {
      id: 'quick-note',
      name: 'Quick Note',
      icon: '📝',
      action: 'create_note',
      target_section: 'notes',
      description: 'Capture a quick thought'
    },
    {
      id: 'new-task',
      name: 'New Task',
      icon: '✓',
      action: 'create_task',
      target_section: 'tasks',
      description: 'Add personal to-do'
    },
    {
      id: 'my-day',
      name: 'My Day',
      icon: '📅',
      action: 'view_dashboard',
      target_section: 'overview',
      description: 'Daily overview'
    }
  ],
  
  // Business Sphere: 💼
  business: [
    {
      id: 'new-project',
      name: 'New Project',
      icon: '🎯',
      action: 'create_project',
      target_section: 'projects',
      description: 'Start business project'
    },
    {
      id: 'schedule-meeting',
      name: 'Schedule Meeting',
      icon: '👥',
      action: 'create_meeting',
      target_section: 'meetings',
      description: 'Book team meeting'
    },
    {
      id: 'ask-analyst',
      name: 'Ask Analyst',
      icon: '📊',
      action: 'delegate_agent',
      target_section: 'agents',
      agent_type: 'analyst',
      description: 'Request business analysis'
    },
    {
      id: 'budget-check',
      name: 'Budget Check',
      icon: '💰',
      action: 'view_budget',
      target_section: 'governance',
      description: 'Check budget status'
    }
  ],
  
  // Government Sphere: 🏛️
  government: [
    {
      id: 'new-request',
      name: 'New Request',
      icon: '📋',
      action: 'create_task',
      target_section: 'tasks',
      description: 'Government service request'
    },
    {
      id: 'browse-forms',
      name: 'Browse Forms',
      icon: '📄',
      action: 'list_documents',
      target_section: 'notes',
      description: 'Find official forms'
    },
    {
      id: 'compliance-check',
      name: 'Compliance',
      icon: '✓',
      action: 'view_compliance',
      target_section: 'governance',
      description: 'Review requirements'
    }
  ],
  
  // Creative Studio: 🎨
  creative: [
    {
      id: 'new-project',
      name: 'New Project',
      icon: '🎨',
      action: 'create_project',
      target_section: 'projects',
      description: 'Start creative project'
    },
    {
      id: 'generate-image',
      name: 'Generate Image',
      icon: '🖼️',
      action: 'delegate_agent',
      target_section: 'agents',
      agent_type: 'image_generator',
      description: 'Create visual content'
    },
    {
      id: 'my-portfolio',
      name: 'Portfolio',
      icon: '📁',
      action: 'view_portfolio',
      target_section: 'overview',
      description: 'View creative works'
    }
  ],
  
  // Community: 👥
  community: [
    {
      id: 'live-threads',
      name: 'Live Threads',
      icon: '🔴',
      action: 'view_live',
      target_section: 'threads',
      filter: 'live',
      description: 'Active discussions'
    },
    {
      id: 'browse-topics',
      name: 'Browse Topics',
      icon: '🏷️',
      action: 'view_topics',
      target_section: 'threads',
      description: 'Explore by topic'
    },
    {
      id: 'nearby',
      name: 'Nearby',
      icon: '📍',
      action: 'view_local',
      target_section: 'threads',
      filter: 'geolocation',
      description: 'Local discussions'
    },
    {
      id: 'public-requests',
      name: 'Requests',
      icon: '🤝',
      action: 'view_requests',
      target_section: 'threads',
      filter: 'request',
      description: 'Community needs'
    }
  ],
  
  // Social & Media: 📱
  social: [
    {
      id: 'new-post',
      name: 'New Post',
      icon: '✍️',
      action: 'create_note',
      target_section: 'notes',
      description: 'Draft social content'
    },
    {
      id: 'schedule-posts',
      name: 'Schedule',
      icon: '📅',
      action: 'view_schedule',
      target_section: 'tasks',
      description: 'Planned publications'
    },
    {
      id: 'analytics',
      name: 'Analytics',
      icon: '📊',
      action: 'view_reports',
      target_section: 'reports',
      description: 'Engagement metrics'
    }
  ],
  
  // Entertainment: 🎬
  entertainment: [
    {
      id: 'browse-content',
      name: 'Browse',
      icon: '🎬',
      action: 'view_content',
      target_section: 'data',
      description: 'Explore entertainment'
    },
    {
      id: 'my-watchlist',
      name: 'Watchlist',
      icon: '⭐',
      action: 'view_watchlist',
      target_section: 'notes',
      description: 'Saved content'
    },
    {
      id: 'recommendations',
      name: 'Recommendations',
      icon: '💡',
      action: 'delegate_agent',
      target_section: 'agents',
      agent_type: 'recommender',
      description: 'Get suggestions'
    }
  ],
  
  // My Team: 🤝
  my_team: [
    {
      id: 'team-overview',
      name: 'Team',
      icon: '👥',
      action: 'view_dashboard',
      target_section: 'overview',
      description: 'Team status'
    },
    {
      id: 'delegate-task',
      name: 'Delegate',
      icon: '🎯',
      action: 'create_task',
      target_section: 'tasks',
      delegation: true,
      description: 'Assign to team member'
    },
    {
      id: 'team-meeting',
      name: 'Meeting',
      icon: '📅',
      action: 'create_meeting',
      target_section: 'meetings',
      description: 'Schedule team session'
    },
    {
      id: 'ask-orchestrator',
      name: 'Ask Orchestrator',
      icon: '🤖',
      action: 'delegate_agent',
      target_section: 'agents',
      agent_type: 'orchestrator',
      description: 'Coordinate team work'
    }
  ]
};

// ═══════════════════════════════════════════════════════════════
// SHORTCUT MANAGER
// ═══════════════════════════════════════════════════════════════

class ShortcutManager {
  /**
   * Get shortcuts for a sphere
   */
  static getShortcutsForSphere(sphereId) {
    const shortcuts = SPHERE_SHORTCUTS[sphereId] || [];
    
    // Validate max 5 shortcuts
    if (shortcuts.length > 5) {
      console.warn(`Sphere ${sphereId} has ${shortcuts.length} shortcuts (max 5)`);
      return shortcuts.slice(0, 5);
    }
    
    return shortcuts;
  }
  
  /**
   * Get global orchestrator
   */
  static getGlobalOrchestrator() {
    return GLOBAL_ORCHESTRATOR;
  }
  
  /**
   * Execute shortcut action
   */
  static async executeShortcut(shortcut, context) {
    const { action, target_section, agent_type, filter } = shortcut;
    
    switch (action) {
      case 'create_note':
        return { type: 'navigate', target: `/${context.sphere}/notes/new` };
        
      case 'create_task':
        return { type: 'navigate', target: `/${context.sphere}/tasks/new` };
        
      case 'create_project':
        return { type: 'navigate', target: `/${context.sphere}/projects/new` };
        
      case 'create_meeting':
        return { type: 'navigate', target: `/${context.sphere}/meetings/new` };
        
      case 'view_dashboard':
        return { type: 'navigate', target: `/${context.sphere}/overview` };
        
      case 'view_budget':
        return { type: 'navigate', target: `/${context.sphere}/governance/budget` };
        
      case 'delegate_agent':
        return {
          type: 'agent_delegation',
          agent_type,
          sphere: context.sphere
        };
        
      case 'view_live':
      case 'view_topics':
      case 'view_local':
      case 'view_requests':
        return {
          type: 'navigate',
          target: `/${context.sphere}/${target_section}`,
          filter
        };
        
      case 'list_documents':
        return { type: 'navigate', target: `/${context.sphere}/notes` };
        
      case 'view_compliance':
        return { type: 'navigate', target: `/${context.sphere}/governance/compliance` };
        
      case 'view_portfolio':
        return { type: 'navigate', target: `/${context.sphere}/overview/portfolio` };
        
      case 'view_content':
        return { type: 'navigate', target: `/${context.sphere}/data` };
        
      case 'view_watchlist':
        return { type: 'navigate', target: `/${context.sphere}/notes/watchlist` };
        
      case 'view_schedule':
        return { type: 'navigate', target: `/${context.sphere}/tasks/scheduled` };
        
      case 'view_reports':
        return { type: 'navigate', target: `/${context.sphere}/reports` };
        
      default:
        throw new Error(`Unknown shortcut action: ${action}`);
    }
  }
  
  /**
   * Validate shortcut (never bypasses hierarchy)
   */
  static validateShortcut(shortcut) {
    const errors = [];
    
    // Must have target section
    if (!shortcut.target_section) {
      errors.push('Shortcut must have target_section');
    }
    
    // Cannot bypass to Governance directly
    if (shortcut.target_section === 'governance' && 
        shortcut.action !== 'view_budget' && 
        shortcut.action !== 'view_compliance') {
      errors.push('Shortcuts cannot bypass to Governance');
    }
    
    // Must be explainable
    if (!shortcut.description) {
      errors.push('Shortcut must have description (explainable by Nova)');
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  /**
   * Get Nova explanation for shortcut
   */
  static explainShortcut(shortcut, context) {
    return `"${shortcut.name}" takes you to ${shortcut.target_section} in your ${context.sphere} sphere to ${shortcut.description}.`;
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  ShortcutManager,
  GLOBAL_ORCHESTRATOR,
  SPHERE_SHORTCUTS
};
