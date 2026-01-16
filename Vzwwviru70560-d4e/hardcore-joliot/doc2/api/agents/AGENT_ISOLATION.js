/**
 * CHE·NU™ AGENT ISOLATION SYSTEM
 * 
 * CRITICAL SECURITY COMPONENT
 * 
 * Agents NEVER directly manipulate user data.
 * All actions are mediated, reviewed, and governed.
 * 
 * Agents operate in ISOLATED DIRECTORIES.
 * Agents NEVER write directly to user directories.
 * Agents NEVER see user private documents unless explicitly granted.
 */

const fs = require('fs').promises;
const path = require('path');

// ═══════════════════════════════════════════════════════════════
// AGENT DIRECTORY STRUCTURE
// ═══════════════════════════════════════════════════════════════

/**
 * CANONICAL STRUCTURE:
 * 
 * /agents
 *   /L0
 *     /agent-id/
 *       /working/      - temporary internal files
 *       /outputs/      - generated results
 *       /memory/       - agent internal notes (if allowed)
 *   /L1
 *     /agent-id/
 *       /working/
 *       /outputs/
 *       /memory/
 *   /L2
 *     /agent-id/
 *       /working/
 *       /outputs/
 *       /memory/
 * 
 * These directories are NOT user-visible.
 */

const AGENT_BASE_PATH = process.env.AGENT_WORKSPACE_PATH || '/var/chenu/agents';

const AGENT_LEVELS = {
  L0: {
    level: 'L0',
    name: 'Simple',
    description: 'Simple, deterministic agents',
    capabilities: {
      memory: false,
      cross_thread_access: false,
      multi_tool_execution: false
    },
    max_budget_per_task: 100,
    max_execution_time: 30 // seconds
  },
  
  L1: {
    level: 'L1',
    name: 'Contextual',
    description: 'Contextual agents with limited memory',
    capabilities: {
      memory: true,
      cross_thread_access: false,
      multi_tool_execution: true
    },
    max_budget_per_task: 500,
    max_execution_time: 120 // seconds
  },
  
  L2: {
    level: 'L2',
    name: 'Advanced',
    description: 'Advanced reasoning agents',
    capabilities: {
      memory: true,
      cross_thread_access: true, // if explicitly allowed
      multi_tool_execution: true
    },
    max_budget_per_task: 2000,
    max_execution_time: 300 // seconds
  }
};

// ═══════════════════════════════════════════════════════════════
// ISOLATION RULES (NON-NEGOTIABLE)
// ═══════════════════════════════════════════════════════════════

const ISOLATION_RULES = {
  // Agents NEVER write directly to these directories
  FORBIDDEN_WRITE_PATHS: [
    '/user',
    '/notes',
    '/projects',
    '/documents',
    '/personal',
    '/business',
    '/threads' // User threads
  ],
  
  // Agents NEVER read from these unless explicitly granted
  RESTRICTED_READ_PATHS: [
    '/user/private',
    '/notes/private',
    '/personal/sensitive'
  ],
  
  // Agents can only operate in their own workspace
  ALLOWED_AGENT_PATHS: [
    `${AGENT_BASE_PATH}/L0`,
    `${AGENT_BASE_PATH}/L1`,
    `${AGENT_BASE_PATH}/L2`
  ],
  
  // File size limits
  MAX_FILE_SIZE: {
    working: 50 * 1024 * 1024,  // 50 MB
    outputs: 100 * 1024 * 1024, // 100 MB
    memory: 10 * 1024 * 1024    // 10 MB
  },
  
  // Time limits
  MAX_FILE_AGE: {
    working: 24 * 60 * 60,      // 24 hours
    outputs: 7 * 24 * 60 * 60,  // 7 days
    memory: 30 * 24 * 60 * 60   // 30 days
  }
};

// ═══════════════════════════════════════════════════════════════
// AGENT WORKSPACE MANAGER
// ═══════════════════════════════════════════════════════════════

class AgentWorkspace {
  constructor(agentId, level) {
    this.agentId = agentId;
    this.level = level;
    this.basePath = path.join(AGENT_BASE_PATH, level, agentId);
    this.workingPath = path.join(this.basePath, 'working');
    this.outputsPath = path.join(this.basePath, 'outputs');
    this.memoryPath = path.join(this.basePath, 'memory');
  }
  
  /**
   * Initialize agent workspace
   * Creates isolated directories for the agent
   */
  async initialize() {
    try {
      await fs.mkdir(this.basePath, { recursive: true });
      await fs.mkdir(this.workingPath, { recursive: true });
      await fs.mkdir(this.outputsPath, { recursive: true });
      
      // Memory directory only for L1+ agents
      if (this.level !== 'L0') {
        await fs.mkdir(this.memoryPath, { recursive: true });
      }
      
      // Create .isolation marker file
      await fs.writeFile(
        path.join(this.basePath, '.isolation'),
        JSON.stringify({
          agent_id: this.agentId,
          level: this.level,
          created_at: new Date().toISOString(),
          isolation_rules: ISOLATION_RULES
        }),
        'utf8'
      );
      
      return true;
    } catch (error) {
      console.error(`Failed to initialize agent workspace: ${error.message}`);
      return false;
    }
  }
  
  /**
   * Validate path is within agent's allowed workspace
   */
  validatePath(targetPath) {
    const resolvedPath = path.resolve(targetPath);
    const resolvedBase = path.resolve(this.basePath);
    
    // Must be within agent's workspace
    if (!resolvedPath.startsWith(resolvedBase)) {
      return {
        valid: false,
        error: 'PATH_OUTSIDE_WORKSPACE',
        message: `Path ${targetPath} is outside agent workspace`
      };
    }
    
    // Check against forbidden paths
    for (const forbidden of ISOLATION_RULES.FORBIDDEN_WRITE_PATHS) {
      if (resolvedPath.includes(forbidden)) {
        return {
          valid: false,
          error: 'FORBIDDEN_PATH',
          message: `Path ${targetPath} is forbidden for agent access`
        };
      }
    }
    
    return { valid: true };
  }
  
  /**
   * Write file to working directory
   * ONLY place where agents can write temporary files
   */
  async writeWorking(filename, content) {
    const validation = this.validatePath(this.workingPath);
    if (!validation.valid) {
      throw new Error(validation.message);
    }
    
    const filePath = path.join(this.workingPath, filename);
    
    // Check file size
    const size = Buffer.byteLength(content, 'utf8');
    if (size > ISOLATION_RULES.MAX_FILE_SIZE.working) {
      throw new Error(`File size ${size} exceeds maximum ${ISOLATION_RULES.MAX_FILE_SIZE.working}`);
    }
    
    await fs.writeFile(filePath, content, 'utf8');
    return filePath;
  }
  
  /**
   * Write file to outputs directory
   * Results that will be presented to user
   */
  async writeOutput(filename, content) {
    const validation = this.validatePath(this.outputsPath);
    if (!validation.valid) {
      throw new Error(validation.message);
    }
    
    const filePath = path.join(this.outputsPath, filename);
    
    // Check file size
    const size = Buffer.byteLength(content, 'utf8');
    if (size > ISOLATION_RULES.MAX_FILE_SIZE.outputs) {
      throw new Error(`File size ${size} exceeds maximum ${ISOLATION_RULES.MAX_FILE_SIZE.outputs}`);
    }
    
    await fs.writeFile(filePath, content, 'utf8');
    
    // Log output creation
    await this.logAction('OUTPUT_CREATED', { filename, size });
    
    return filePath;
  }
  
  /**
   * Write to agent memory (L1+ only)
   */
  async writeMemory(key, value) {
    if (this.level === 'L0') {
      throw new Error('L0 agents cannot use memory');
    }
    
    const validation = this.validatePath(this.memoryPath);
    if (!validation.valid) {
      throw new Error(validation.message);
    }
    
    const filePath = path.join(this.memoryPath, `${key}.json`);
    const content = JSON.stringify(value, null, 2);
    
    // Check file size
    const size = Buffer.byteLength(content, 'utf8');
    if (size > ISOLATION_RULES.MAX_FILE_SIZE.memory) {
      throw new Error(`Memory size ${size} exceeds maximum ${ISOLATION_RULES.MAX_FILE_SIZE.memory}`);
    }
    
    await fs.writeFile(filePath, content, 'utf8');
    return true;
  }
  
  /**
   * Read from agent memory (L1+ only)
   */
  async readMemory(key) {
    if (this.level === 'L0') {
      throw new Error('L0 agents cannot use memory');
    }
    
    const filePath = path.join(this.memoryPath, `${key}.json`);
    
    try {
      const content = await fs.readFile(filePath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      if (error.code === 'ENOENT') {
        return null; // Memory key doesn't exist
      }
      throw error;
    }
  }
  
  /**
   * List outputs (for Nova to present to user)
   */
  async listOutputs() {
    try {
      const files = await fs.readdir(this.outputsPath);
      const outputs = [];
      
      for (const file of files) {
        const filePath = path.join(this.outputsPath, file);
        const stats = await fs.stat(filePath);
        
        outputs.push({
          filename: file,
          path: filePath,
          size: stats.size,
          created_at: stats.birthtime,
          modified_at: stats.mtime
        });
      }
      
      return outputs;
    } catch (error) {
      return [];
    }
  }
  
  /**
   * Clean working directory (temporary files)
   */
  async cleanWorking() {
    try {
      const files = await fs.readdir(this.workingPath);
      const now = Date.now();
      let cleaned = 0;
      
      for (const file of files) {
        const filePath = path.join(this.workingPath, file);
        const stats = await fs.stat(filePath);
        const age = (now - stats.mtimeMs) / 1000;
        
        // Delete files older than max age
        if (age > ISOLATION_RULES.MAX_FILE_AGE.working) {
          await fs.unlink(filePath);
          cleaned++;
        }
      }
      
      return { cleaned, remaining: files.length - cleaned };
    } catch (error) {
      console.error(`Failed to clean working directory: ${error.message}`);
      return { cleaned: 0, remaining: 0 };
    }
  }
  
  /**
   * Log agent action for audit trail
   */
  async logAction(action, details) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      agent_id: this.agentId,
      level: this.level,
      action,
      details
    };
    
    // In production, this would write to audit log
    console.log('[AGENT ISOLATION]', JSON.stringify(logEntry));
  }
  
  /**
   * Destroy agent workspace (cleanup after task completion)
   */
  async destroy() {
    try {
      // Archive outputs before destroying
      const outputs = await this.listOutputs();
      
      if (outputs.length > 0) {
        // In production, outputs would be moved to permanent storage
        await this.logAction('WORKSPACE_DESTROYED', {
          outputs_count: outputs.length
        });
      }
      
      // Delete workspace
      await fs.rm(this.basePath, { recursive: true, force: true });
      return true;
    } catch (error) {
      console.error(`Failed to destroy workspace: ${error.message}`);
      return false;
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// AGENT EXECUTION GOVERNOR
// ═══════════════════════════════════════════════════════════════

class AgentExecutionGovernor {
  /**
   * Check if agent can escalate level (answer: NO)
   */
  static canEscalateLevel(currentLevel, requestedLevel) {
    return false; // No agent can escalate its level automatically
  }
  
  /**
   * Check if agent can access user data
   */
  static canAccessUserData(agentId, userId, dataPath, permissions) {
    // Must have explicit permission grant
    const hasPermission = permissions.includes('read_user_data');
    
    // Must not be restricted path
    const isRestricted = ISOLATION_RULES.RESTRICTED_READ_PATHS.some(restricted =>
      dataPath.includes(restricted)
    );
    
    return hasPermission && !isRestricted;
  }
  
  /**
   * Validate agent execution request
   */
  static validateExecution(agent, task, budget) {
    const levelConfig = AGENT_LEVELS[agent.level];
    
    if (!levelConfig) {
      return {
        valid: false,
        error: 'INVALID_LEVEL',
        message: `Agent level ${agent.level} is not valid`
      };
    }
    
    // Check budget
    if (budget > levelConfig.max_budget_per_task) {
      return {
        valid: false,
        error: 'BUDGET_EXCEEDED',
        message: `Budget ${budget} exceeds max ${levelConfig.max_budget_per_task} for ${agent.level}`
      };
    }
    
    // Check capabilities
    if (task.requires_memory && !levelConfig.capabilities.memory) {
      return {
        valid: false,
        error: 'CAPABILITY_MISSING',
        message: `Agent ${agent.level} does not support memory`
      };
    }
    
    if (task.requires_cross_thread && !levelConfig.capabilities.cross_thread_access) {
      return {
        valid: false,
        error: 'CAPABILITY_MISSING',
        message: `Agent ${agent.level} does not support cross-thread access`
      };
    }
    
    return { valid: true };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  AgentWorkspace,
  AgentExecutionGovernor,
  AGENT_LEVELS,
  ISOLATION_RULES,
  AGENT_BASE_PATH
};
