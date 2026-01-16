/**
 * CHE·NU™ OUTPUT INTEGRATION FLOW
 * 
 * CRITICAL PRINCIPLE:
 * Agents NEVER automatically merge outputs into user space.
 * NO automatic merging. NO silent copy.
 * 
 * OUTPUT INTEGRATION FLOW:
 * 1. Agent completes task
 * 2. Output stored in /outputs
 * 3. Nova notifies the user
 * 4. User explicitly chooses:
 *    - import into Notes
 *    - attach to Project
 *    - link to Thread
 *    - discard or archive
 */

const { AgentWorkspace } = require('../agents/AGENT_ISOLATION');

// ═══════════════════════════════════════════════════════════════
// OUTPUT TYPES
// ═══════════════════════════════════════════════════════════════

const OUTPUT_TYPES = {
  DOCUMENT: 'document',       // Text document
  TABLE: 'table',             // Structured data
  SPREADSHEET: 'spreadsheet', // Excel/CSV
  PDF: 'pdf',                 // PDF file
  IMAGE: 'image',             // Generated image
  ANALYSIS: 'analysis',       // Analysis result
  SUMMARY: 'summary',         // Summary text
  CODE: 'code',               // Code snippet
  THREAD: 'thread',           // Thread artifact
  REPORT: 'report'            // Formatted report
};

// ═══════════════════════════════════════════════════════════════
// INTEGRATION ACTIONS
// ═══════════════════════════════════════════════════════════════

const INTEGRATION_ACTIONS = {
  IMPORT_NOTES: 'import_notes',         // Import into Notes section
  ATTACH_PROJECT: 'attach_project',     // Attach to existing Project
  LINK_THREAD: 'link_thread',           // Link to Thread
  CREATE_DATASPACE: 'create_dataspace', // Create new DataSpace entry
  ARCHIVE: 'archive',                   // Archive for later
  DISCARD: 'discard'                    // Delete permanently
};

// ═══════════════════════════════════════════════════════════════
// AGENT OUTPUT CLASS
// ═══════════════════════════════════════════════════════════════

class AgentOutput {
  constructor(data) {
    this.id = data.id || `output-${Date.now()}`;
    this.agent_id = data.agent_id;
    this.agent_level = data.agent_level;
    this.task_id = data.task_id;
    
    // Output details
    this.type = data.type; // OUTPUT_TYPES
    this.title = data.title;
    this.description = data.description;
    this.file_path = data.file_path;
    this.content = data.content;
    this.format = data.format; // 'text', 'json', 'html', 'markdown', etc.
    
    // Metadata
    this.created_at = new Date().toISOString();
    this.size_bytes = data.size_bytes || 0;
    this.preview = data.preview; // Short preview for UI
    
    // Integration state
    this.status = 'pending_review'; // 'pending_review', 'integrated', 'archived', 'discarded'
    this.integration_action = null;
    this.integration_target = null; // Where it was integrated
    this.integrated_at = null;
    this.integrated_by = null;
    
    // User feedback
    this.user_rating = null; // 1-5 stars
    this.user_notes = null;
  }
  
  /**
   * Generate preview for user
   */
  generatePreview(maxLength = 200) {
    if (this.preview) return this.preview;
    
    if (typeof this.content === 'string') {
      return this.content.substring(0, maxLength) + (this.content.length > maxLength ? '...' : '');
    }
    
    if (typeof this.content === 'object') {
      return JSON.stringify(this.content, null, 2).substring(0, maxLength) + '...';
    }
    
    return `[${this.type}] ${this.title}`;
  }
  
  /**
   * Mark as integrated
   */
  markIntegrated(action, target, userId) {
    this.status = 'integrated';
    this.integration_action = action;
    this.integration_target = target;
    this.integrated_at = new Date().toISOString();
    this.integrated_by = userId;
  }
  
  /**
   * Mark as archived
   */
  archive() {
    this.status = 'archived';
  }
  
  /**
   * Mark as discarded
   */
  discard() {
    this.status = 'discarded';
  }
  
  /**
   * Add user feedback
   */
  addFeedback(rating, notes) {
    this.user_rating = rating;
    this.user_notes = notes;
  }
}

// ═══════════════════════════════════════════════════════════════
// OUTPUT INTEGRATION MANAGER
// ═══════════════════════════════════════════════════════════════

class OutputIntegrationManager {
  constructor(pool) {
    this.pool = pool;
    this.pendingOutputs = new Map();
  }
  
  /**
   * Agent completes task and creates output
   * This is called by agents when they finish work
   */
  async registerOutput(agentId, agentLevel, taskId, outputData) {
    // Create output record
    const output = new AgentOutput({
      ...outputData,
      agent_id: agentId,
      agent_level: agentLevel,
      task_id: taskId
    });
    
    // Store in pending outputs
    this.pendingOutputs.set(output.id, output);
    
    // Persist to database
    await this.pool.query(
      `INSERT INTO agent_outputs 
       (id, agent_id, agent_level, task_id, type, title, description, 
        file_path, format, size_bytes, status, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
      [
        output.id,
        output.agent_id,
        output.agent_level,
        output.task_id,
        output.type,
        output.title,
        output.description,
        output.file_path,
        output.format,
        output.size_bytes,
        output.status,
        output.created_at
      ]
    );
    
    // Nova will be notified to present this to user
    return output;
  }
  
  /**
   * User chooses integration action
   * CRITICAL: User explicitly decides what to do with output
   */
  async integrateOutput(outputId, userId, action, targetDetails) {
    const output = this.pendingOutputs.get(outputId);
    if (!output) {
      throw new Error('Output not found');
    }
    
    if (output.status !== 'pending_review') {
      throw new Error('Output has already been processed');
    }
    
    let integrationResult;
    
    switch (action) {
      case INTEGRATION_ACTIONS.IMPORT_NOTES:
        integrationResult = await this.importToNotes(output, userId, targetDetails);
        break;
        
      case INTEGRATION_ACTIONS.ATTACH_PROJECT:
        integrationResult = await this.attachToProject(output, userId, targetDetails);
        break;
        
      case INTEGRATION_ACTIONS.LINK_THREAD:
        integrationResult = await this.linkToThread(output, userId, targetDetails);
        break;
        
      case INTEGRATION_ACTIONS.CREATE_DATASPACE:
        integrationResult = await this.createDataSpaceEntry(output, userId, targetDetails);
        break;
        
      case INTEGRATION_ACTIONS.ARCHIVE:
        integrationResult = await this.archiveOutput(output, userId);
        break;
        
      case INTEGRATION_ACTIONS.DISCARD:
        integrationResult = await this.discardOutput(output, userId);
        break;
        
      default:
        throw new Error(`Unknown integration action: ${action}`);
    }
    
    // Update output status
    if (action !== INTEGRATION_ACTIONS.DISCARD) {
      output.markIntegrated(action, integrationResult.target_id, userId);
    }
    
    // Update database
    await this.pool.query(
      `UPDATE agent_outputs 
       SET status = $1, integration_action = $2, integration_target = $3, 
           integrated_at = $4, integrated_by = $5
       WHERE id = $6`,
      [
        output.status,
        output.integration_action,
        output.integration_target,
        output.integrated_at,
        output.integrated_by,
        output.id
      ]
    );
    
    return integrationResult;
  }
  
  /**
   * Import output into Notes section
   */
  async importToNotes(output, userId, targetDetails) {
    const { sphere_id, title } = targetDetails;
    
    // Create note entry
    const result = await this.pool.query(
      `INSERT INTO notes (user_id, sphere_id, title, content, type, created_at)
       VALUES ($1, $2, $3, $4, $5, NOW())
       RETURNING id`,
      [userId, sphere_id, title || output.title, output.content, output.type]
    );
    
    return {
      action: INTEGRATION_ACTIONS.IMPORT_NOTES,
      target_id: result.rows[0].id,
      target_type: 'note',
      message: 'Output imported to Notes'
    };
  }
  
  /**
   * Attach output to existing Project
   */
  async attachToProject(output, userId, targetDetails) {
    const { project_id } = targetDetails;
    
    // Create project attachment
    await this.pool.query(
      `INSERT INTO project_attachments 
       (project_id, title, file_path, type, uploaded_by, created_at)
       VALUES ($1, $2, $3, $4, $5, NOW())`,
      [project_id, output.title, output.file_path, output.type, userId]
    );
    
    return {
      action: INTEGRATION_ACTIONS.ATTACH_PROJECT,
      target_id: project_id,
      target_type: 'project',
      message: 'Output attached to Project'
    };
  }
  
  /**
   * Link output to Thread
   */
  async linkToThread(output, userId, targetDetails) {
    const { thread_id } = targetDetails;
    
    // Add message to thread referencing output
    const result = await this.pool.query(
      `INSERT INTO thread_messages 
       (thread_id, role, content, created_at)
       VALUES ($1, $2, $3, NOW())
       RETURNING id`,
      [
        thread_id,
        'assistant',
        JSON.stringify({
          type: 'agent_output',
          output_id: output.id,
          title: output.title,
          preview: output.generatePreview()
        })
      ]
    );
    
    return {
      action: INTEGRATION_ACTIONS.LINK_THREAD,
      target_id: thread_id,
      target_type: 'thread',
      message: 'Output linked to Thread'
    };
  }
  
  /**
   * Create new DataSpace entry
   */
  async createDataSpaceEntry(output, userId, targetDetails) {
    const { dataspace_id, entity_type } = targetDetails;
    
    const result = await this.pool.query(
      `INSERT INTO dataspace_entries 
       (dataspace_id, entity_type, data, created_by, created_at)
       VALUES ($1, $2, $3, $4, NOW())
       RETURNING id`,
      [dataspace_id, entity_type, output.content, userId]
    );
    
    return {
      action: INTEGRATION_ACTIONS.CREATE_DATASPACE,
      target_id: result.rows[0].id,
      target_type: 'dataspace_entry',
      message: 'Output added to DataSpace'
    };
  }
  
  /**
   * Archive output for later
   */
  async archiveOutput(output, userId) {
    output.archive();
    
    return {
      action: INTEGRATION_ACTIONS.ARCHIVE,
      target_id: output.id,
      target_type: 'archived_output',
      message: 'Output archived'
    };
  }
  
  /**
   * Discard output permanently
   */
  async discardOutput(output, userId) {
    output.discard();
    
    // Delete from pending
    this.pendingOutputs.delete(output.id);
    
    // Mark as discarded in database
    await this.pool.query(
      `UPDATE agent_outputs SET status = 'discarded' WHERE id = $1`,
      [output.id]
    );
    
    return {
      action: INTEGRATION_ACTIONS.DISCARD,
      target_id: null,
      target_type: null,
      message: 'Output discarded'
    };
  }
  
  /**
   * Get pending outputs for user review
   */
  async getPendingOutputs(userId) {
    const result = await this.pool.query(
      `SELECT ao.* 
       FROM agent_outputs ao
       JOIN agent_tasks at ON ao.task_id = at.id
       WHERE at.user_id = $1 AND ao.status = 'pending_review'
       ORDER BY ao.created_at DESC`,
      [userId]
    );
    
    return result.rows.map(row => new AgentOutput(row));
  }
  
  /**
   * Get output by ID
   */
  async getOutput(outputId) {
    const result = await this.pool.query(
      `SELECT * FROM agent_outputs WHERE id = $1`,
      [outputId]
    );
    
    if (result.rows.length === 0) return null;
    return new AgentOutput(result.rows[0]);
  }
  
  /**
   * Add user feedback on output
   */
  async addFeedback(outputId, userId, rating, notes) {
    const output = await this.getOutput(outputId);
    if (!output) {
      throw new Error('Output not found');
    }
    
    output.addFeedback(rating, notes);
    
    await this.pool.query(
      `UPDATE agent_outputs 
       SET user_rating = $1, user_notes = $2
       WHERE id = $3`,
      [rating, notes, outputId]
    );
    
    return output;
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  AgentOutput,
  OutputIntegrationManager,
  OUTPUT_TYPES,
  INTEGRATION_ACTIONS
};
