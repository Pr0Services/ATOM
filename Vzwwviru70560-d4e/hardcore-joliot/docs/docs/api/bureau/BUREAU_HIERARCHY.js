/**
 * CHE·NU™ BUREAU HIERARCHY SYSTEM
 * 
 * CRITICAL: EVERY BUREAU (IN EVERY SPHERE) FOLLOWS THIS EXACT ORDER
 * 
 * THIS ORDER IS FINAL. Labels may vary slightly, order must not.
 * 
 * 1. Overview / Dashboard        (See)
 * 2. Notes                       (Think)
 * 3. Tasks                       (Organize effort)
 * 4. Projects                    (Structure over time)
 * 5. Threads (.chenu)            (Connect meaning)
 * 6. Meetings                    (Decide together)
 * 7. Data / Database             (Reliable information)
 * 8. Agents                      (Delegate)
 * 9. Reports / History           (Traceability)
 * 10. Budget & Governance        (Limits & protection)
 */

// ═══════════════════════════════════════════════════════════════
// BUREAU SECTIONS (NON-NEGOTIABLE ORDER)
// ═══════════════════════════════════════════════════════════════

const BUREAU_SECTIONS = [
  {
    order: 1,
    id: 'overview',
    name: 'Overview',
    alt_names: ['Dashboard', 'Home'],
    cognitive_purpose: 'See',
    description: 'High-level view of sphere status and activity',
    icon: '📊',
    permissions_required: ['read_sphere']
  },
  {
    order: 2,
    id: 'notes',
    name: 'Notes',
    alt_names: ['Documents', 'Content'],
    cognitive_purpose: 'Think',
    description: 'Thought capture, documentation, knowledge',
    icon: '📝',
    permissions_required: ['read_notes']
  },
  {
    order: 3,
    id: 'tasks',
    name: 'Tasks',
    alt_names: ['Actions', 'To-Do'],
    cognitive_purpose: 'Organize effort',
    description: 'Individual actions and responsibilities',
    icon: '✓',
    permissions_required: ['read_tasks']
  },
  {
    order: 4,
    id: 'projects',
    name: 'Projects',
    alt_names: ['Initiatives', 'Programs'],
    cognitive_purpose: 'Structure over time',
    description: 'Long-term structured work with milestones',
    icon: '🎯',
    permissions_required: ['read_projects']
  },
  {
    order: 5,
    id: 'threads',
    name: 'Threads',
    alt_names: ['.chenu files', 'Conversations'],
    cognitive_purpose: 'Connect meaning',
    description: 'Persistent lines of thought with context and decisions',
    icon: '🧵',
    permissions_required: ['read_threads']
  },
  {
    order: 6,
    id: 'meetings',
    name: 'Meetings',
    alt_names: ['Sessions', 'Calls'],
    cognitive_purpose: 'Decide together',
    description: 'Collaborative decision-making sessions',
    icon: '👥',
    permissions_required: ['read_meetings']
  },
  {
    order: 7,
    id: 'data',
    name: 'Data',
    alt_names: ['Database', 'Records'],
    cognitive_purpose: 'Reliable information',
    description: 'Structured data storage and retrieval',
    icon: '🗄️',
    permissions_required: ['read_data']
  },
  {
    order: 8,
    id: 'agents',
    name: 'Agents',
    alt_names: ['Automation', 'Assistants'],
    cognitive_purpose: 'Delegate',
    description: 'AI agents available for task delegation',
    icon: '🤖',
    permissions_required: ['manage_agents']
  },
  {
    order: 9,
    id: 'reports',
    name: 'Reports',
    alt_names: ['History', 'Analytics'],
    cognitive_purpose: 'Traceability',
    description: 'Historical records and analysis',
    icon: '📈',
    permissions_required: ['read_reports']
  },
  {
    order: 10,
    id: 'governance',
    name: 'Budget & Governance',
    alt_names: ['Settings', 'Control'],
    cognitive_purpose: 'Limits & protection',
    description: 'Budget control and governance rules',
    icon: '🛡️',
    permissions_required: ['manage_governance']
  }
];

// ═══════════════════════════════════════════════════════════════
// DATA LEVELS (STRICT HIERARCHY)
// ═══════════════════════════════════════════════════════════════

const DATA_LEVELS = {
  GLOBAL: {
    level: 1,
    name: 'Entry Bureau (Global)',
    description: 'Unclassified collection zone',
    rules: [
      'Never final',
      'Never used by agents automatically',
      'Must be intentionally placed into a sphere'
    ],
    scope: 'global'
  },
  
  SPHERE: {
    level: 2,
    name: 'Sphere',
    description: 'Context-specific data ownership',
    rules: [
      'Each data item belongs to ONE sphere only',
      'No data belongs to two spheres',
      'Other spheres may REFERENCE, never COPY',
      'Sphere defines meaning and scope'
    ],
    scope: 'sphere'
  },
  
  BUREAU: {
    level: 3,
    name: 'Bureau (View)',
    description: 'Filtered view, not storage',
    rules: [
      'A bureau section is a FILTERED VIEW',
      'Adds only relevant sphere data',
      'Hides all unrelated data',
      'Respects permissions and scope'
    ],
    scope: 'bureau_section'
  },
  
  THREAD: {
    level: 4,
    name: 'Thread (.chenu)',
    description: 'Unit of truth',
    rules: [
      'Belongs to exactly one sphere',
      'May reference other threads or spheres',
      'Contains context, decisions, links, summaries',
      'Threads CONNECT without MIXING'
    ],
    scope: 'thread'
  }
};

// ═══════════════════════════════════════════════════════════════
// DATA FLOW RULES (ABSOLUTE)
// ═══════════════════════════════════════════════════════════════

const DATA_FLOW_RULES = {
  DIRECTION: 'downward_only',
  ESCALATION: 'never_automatic',
  
  FORBIDDEN: [
    'Duplicating data for visibility',
    'Copying notes between spheres',
    'Merging budgets',
    'Automatic data escalation',
    'Blending contexts'
  ],
  
  ALLOWED: [
    'Linking',
    'Referencing',
    'Summarizing',
    'Read-only projections'
  ],
  
  PRINCIPLE: 'CHE·NU LINKS, IT DOES NOT BLEND'
};

// ═══════════════════════════════════════════════════════════════
// BUREAU CONSTRUCTOR
// ═══════════════════════════════════════════════════════════════

class Bureau {
  constructor(sphereId, userId) {
    this.sphereId = sphereId;
    this.userId = userId;
    this.sections = BUREAU_SECTIONS;
  }
  
  /**
   * Build bureau view for user
   * Applies: permissions, scope, filters
   */
  async build(pool, userPermissions) {
    const builtSections = [];
    
    for (const section of this.sections) {
      // Check permissions
      const hasPermission = this.checkPermissions(section, userPermissions);
      if (!hasPermission) continue;
      
      // Build section with filtered data
      const sectionData = await this.buildSection(pool, section);
      
      builtSections.push({
        ...section,
        data: sectionData,
        visible: true
      });
    }
    
    return {
      sphere_id: this.sphereId,
      user_id: this.userId,
      sections: builtSections,
      built_at: new Date().toISOString()
    };
  }
  
  /**
   * Check if user has permission for section
   */
  checkPermissions(section, userPermissions) {
    return section.permissions_required.every(perm => 
      userPermissions.includes(perm)
    );
  }
  
  /**
   * Build individual section with filtered data
   * CRITICAL: Only shows data relevant to THIS sphere
   */
  async buildSection(pool, section) {
    switch (section.id) {
      case 'overview':
        return await this.buildOverview(pool);
        
      case 'notes':
        return await this.buildNotes(pool);
        
      case 'tasks':
        return await this.buildTasks(pool);
        
      case 'projects':
        return await this.buildProjects(pool);
        
      case 'threads':
        return await this.buildThreads(pool);
        
      case 'meetings':
        return await this.buildMeetings(pool);
        
      case 'data':
        return await this.buildData(pool);
        
      case 'agents':
        return await this.buildAgents(pool);
        
      case 'reports':
        return await this.buildReports(pool);
        
      case 'governance':
        return await this.buildGovernance(pool);
        
      default:
        return null;
    }
  }
  
  /**
   * Build Overview section
   */
  async buildOverview(pool) {
    // Aggregate stats from all sections
    const stats = await pool.query(
      `SELECT 
         (SELECT COUNT(*) FROM notes WHERE sphere_id = $1 AND user_id = $2) as notes_count,
         (SELECT COUNT(*) FROM tasks WHERE sphere_id = $1 AND user_id = $2) as tasks_count,
         (SELECT COUNT(*) FROM projects WHERE sphere_id = $1 AND user_id = $2) as projects_count,
         (SELECT COUNT(*) FROM threads WHERE sphere_id = $1 AND owner_id = $2) as threads_count,
         (SELECT COUNT(*) FROM meetings WHERE sphere_id = $1 AND created_by = $2) as meetings_count`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'overview',
      statistics: stats.rows[0],
      recent_activity: [] // Would fetch recent items
    };
  }
  
  /**
   * Build Notes section
   * CRITICAL: Shows ONLY notes from THIS sphere
   */
  async buildNotes(pool) {
    const result = await pool.query(
      `SELECT * FROM notes 
       WHERE sphere_id = $1 AND user_id = $2
       ORDER BY updated_at DESC
       LIMIT 50`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'notes',
      items: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Tasks section
   * CRITICAL: Shows ONLY tasks from THIS sphere
   */
  async buildTasks(pool) {
    const result = await pool.query(
      `SELECT * FROM tasks 
       WHERE sphere_id = $1 AND user_id = $2
       ORDER BY priority DESC, due_date ASC`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'tasks',
      items: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Projects section
   */
  async buildProjects(pool) {
    const result = await pool.query(
      `SELECT * FROM projects 
       WHERE sphere_id = $1 AND created_by = $2
       ORDER BY created_at DESC`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'projects',
      items: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Threads section
   */
  async buildThreads(pool) {
    const result = await pool.query(
      `SELECT * FROM threads 
       WHERE sphere_id = $1 AND owner_id = $2
       ORDER BY updated_at DESC`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'threads',
      items: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Meetings section
   */
  async buildMeetings(pool) {
    const result = await pool.query(
      `SELECT * FROM meetings 
       WHERE sphere_id = $1 AND created_by = $2
       ORDER BY scheduled_at DESC`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'meetings',
      items: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Data section
   */
  async buildData(pool) {
    const result = await pool.query(
      `SELECT * FROM dataspaces 
       WHERE sphere_id = $1 AND owner_id = $2
       ORDER BY created_at DESC`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'data',
      dataspaces: result.rows,
      count: result.rows.length
    };
  }
  
  /**
   * Build Agents section
   */
  async buildAgents(pool) {
    // Get agents available for this sphere
    const { getSkillsForSphere } = require('../skills/SKILLS_CATALOG');
    const availableSkills = getSkillsForSphere(this.sphereId);
    
    return {
      type: 'agents',
      available_skills: availableSkills.length,
      recent_tasks: [] // Would fetch recent agent tasks
    };
  }
  
  /**
   * Build Reports section
   */
  async buildReports(pool) {
    return {
      type: 'reports',
      available_reports: [
        'Activity Summary',
        'Budget Usage',
        'Task Completion',
        'Thread Analytics'
      ]
    };
  }
  
  /**
   * Build Governance section
   */
  async buildGovernance(pool) {
    const result = await pool.query(
      `SELECT * FROM governance_config 
       WHERE sphere_id = $1 AND user_id = $2`,
      [this.sphereId, this.userId]
    );
    
    return {
      type: 'governance',
      config: result.rows[0] || {},
      budget_status: {} // Would fetch budget info
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  Bureau,
  BUREAU_SECTIONS,
  DATA_LEVELS,
  DATA_FLOW_RULES
};
