/**
 * CHE·NU™ IDENTITY SHARING SYSTEM
 * 
 * EXPLICIT SHARING MECHANISM
 * 
 * Sharing between identities requires:
 * - user-initiated action
 * - selection of data
 * - destination identity/context
 * - sharing mode (reference / copy)
 * 
 * DEFAULT = reference only
 * 
 * PRINCIPLE:
 * REFERENCING is allowed.
 * COPYING is forbidden unless explicitly requested.
 */

const { SHARING_MODES, DEFAULT_SHARING_MODE } = require('./IDENTITY_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// SHARING REQUEST CLASS
// ═══════════════════════════════════════════════════════════════

class SharingRequest {
  constructor(data) {
    this.id = data.id || `share-${Date.now()}`;
    
    // Source
    this.source_identity_id = data.source_identity_id;
    this.source_context_id = data.source_context_id;
    this.data_type = data.data_type; // 'note', 'task', 'project', 'thread', 'document'
    this.data_id = data.data_id;
    
    // Destination
    this.target_identity_id = data.target_identity_id;
    this.target_context_id = data.target_context_id || null;
    
    // Sharing mode
    this.sharing_mode = data.sharing_mode || DEFAULT_SHARING_MODE;
    
    // Status
    this.status = 'pending'; // pending, approved, rejected, completed
    
    // User who initiated
    this.initiated_by = data.initiated_by;
    
    // Timestamps
    this.requested_at = new Date().toISOString();
    this.approved_at = null;
    this.completed_at = null;
    
    // Result
    this.result_id = null; // ID of created reference or copy
  }
  
  /**
   * Approve sharing request
   */
  approve() {
    this.status = 'approved';
    this.approved_at = new Date().toISOString();
  }
  
  /**
   * Reject sharing request
   */
  reject() {
    this.status = 'rejected';
  }
  
  /**
   * Mark as completed
   */
  complete(resultId) {
    this.status = 'completed';
    this.completed_at = new Date().toISOString();
    this.result_id = resultId;
  }
}

// ═══════════════════════════════════════════════════════════════
// SHARING MANAGER
// ═══════════════════════════════════════════════════════════════

class SharingManager {
  constructor(pool, identityManager) {
    this.pool = pool;
    this.identityManager = identityManager;
  }
  
  /**
   * Request to share data between identities
   * USER-INITIATED ACTION REQUIRED
   */
  async requestSharing(userId, sharingData) {
    // Get active session to validate source
    const session = this.identityManager.getActiveSession(userId);
    
    // Validate source identity matches current identity
    if (session.identity.id !== sharingData.source_identity_id) {
      throw new Error('Source identity must be current active identity');
    }
    
    // Get target identity
    const targetIdentity = await this.identityManager.getIdentity(
      sharingData.target_identity_id
    );
    
    // Validate target identity belongs to same user
    if (targetIdentity.user_id !== userId) {
      throw new Error('Can only share to your own identities');
    }
    
    // Validate data exists and belongs to source context
    await this.validateDataOwnership(
      sharingData.data_type,
      sharingData.data_id,
      session.identity.id,
      session.context.id
    );
    
    // Create sharing request
    const request = new SharingRequest({
      ...sharingData,
      initiated_by: userId,
      source_context_id: session.context.id
    });
    
    // Save to database
    await this.pool.query(
      `INSERT INTO sharing_requests 
       (id, source_identity_id, source_context_id, target_identity_id, target_context_id,
        data_type, data_id, sharing_mode, status, initiated_by, requested_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)`,
      [
        request.id,
        request.source_identity_id,
        request.source_context_id,
        request.target_identity_id,
        request.target_context_id,
        request.data_type,
        request.data_id,
        request.sharing_mode,
        request.status,
        request.initiated_by,
        request.requested_at
      ]
    );
    
    return request;
  }
  
  /**
   * Execute sharing (after user confirmation)
   */
  async executeSharing(userId, requestId, confirmed = false) {
    if (!confirmed) {
      throw new Error('User confirmation required for sharing execution');
    }
    
    // Get sharing request
    const result = await this.pool.query(
      `SELECT * FROM sharing_requests WHERE id = $1`,
      [requestId]
    );
    
    if (result.rows.length === 0) {
      throw new Error('Sharing request not found');
    }
    
    const requestData = result.rows[0];
    const request = new SharingRequest(requestData);
    
    // Validate user
    if (request.initiated_by !== userId) {
      throw new Error('Only the requester can execute sharing');
    }
    
    // Validate status
    if (request.status !== 'pending') {
      throw new Error(`Sharing request is ${request.status}`);
    }
    
    // Approve request
    request.approve();
    
    // Execute based on sharing mode
    let resultId;
    
    if (request.sharing_mode === 'reference') {
      resultId = await this.createReference(request);
    } else if (request.sharing_mode === 'copy') {
      resultId = await this.createCopy(request);
    } else {
      throw new Error(`Unknown sharing mode: ${request.sharing_mode}`);
    }
    
    // Complete request
    request.complete(resultId);
    
    // Update database
    await this.pool.query(
      `UPDATE sharing_requests 
       SET status = $1, approved_at = $2, completed_at = $3, result_id = $4
       WHERE id = $5`,
      [request.status, request.approved_at, request.completed_at, request.result_id, request.id]
    );
    
    // Log sharing action
    await this.logSharing(request);
    
    return {
      request,
      result_id: resultId,
      sharing_mode: request.sharing_mode,
      message: `Data ${request.sharing_mode === 'reference' ? 'referenced' : 'copied'} successfully`
    };
  }
  
  /**
   * Create reference (default sharing mode)
   */
  async createReference(request) {
    const referenceId = `ref-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    await this.pool.query(
      `INSERT INTO identity_references 
       (id, source_identity_id, source_context_id, target_identity_id, target_context_id,
        data_type, data_id, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())`,
      [
        referenceId,
        request.source_identity_id,
        request.source_context_id,
        request.target_identity_id,
        request.target_context_id,
        request.data_type,
        request.data_id
      ]
    );
    
    return referenceId;
  }
  
  /**
   * Create copy (requires explicit request)
   */
  async createCopy(request) {
    // Get original data
    const originalData = await this.getDataById(request.data_type, request.data_id);
    
    // Create copy in target identity/context
    const copyId = await this.duplicateData(
      request.data_type,
      originalData,
      request.target_identity_id,
      request.target_context_id
    );
    
    // Log copy creation
    await this.pool.query(
      `INSERT INTO identity_copies 
       (id, source_identity_id, source_data_id, target_identity_id, 
        target_data_id, data_type, created_at)
       VALUES ($1, $2, $3, $4, $5, $6, NOW())`,
      [
        `copy-${Date.now()}`,
        request.source_identity_id,
        request.data_id,
        request.target_identity_id,
        copyId,
        request.data_type
      ]
    );
    
    return copyId;
  }
  
  /**
   * Get data by ID (type-specific)
   */
  async getDataById(dataType, dataId) {
    const tableMap = {
      note: 'notes',
      task: 'tasks',
      project: 'projects',
      thread: 'threads',
      document: 'documents'
    };
    
    const table = tableMap[dataType];
    if (!table) {
      throw new Error(`Unknown data type: ${dataType}`);
    }
    
    const result = await this.pool.query(
      `SELECT * FROM ${table} WHERE id = $1`,
      [dataId]
    );
    
    if (result.rows.length === 0) {
      throw new Error(`${dataType} not found: ${dataId}`);
    }
    
    return result.rows[0];
  }
  
  /**
   * Duplicate data (type-specific)
   */
  async duplicateData(dataType, originalData, targetIdentityId, targetContextId) {
    const newId = `${dataType}-${Date.now()}-copy`;
    
    const tableMap = {
      note: 'notes',
      task: 'tasks',
      project: 'projects',
      thread: 'threads',
      document: 'documents'
    };
    
    const table = tableMap[dataType];
    
    // This is a simplified version - real implementation would handle
    // all fields properly for each data type
    
    await this.pool.query(
      `INSERT INTO ${table} 
       SELECT $1 as id, * FROM ${table} WHERE id = $2`,
      [newId, originalData.id]
    );
    
    // Update identity and context references
    await this.pool.query(
      `UPDATE ${table} 
       SET identity_id = $1, context_id = $2, 
           created_at = NOW(), is_copy = true, source_id = $3
       WHERE id = $4`,
      [targetIdentityId, targetContextId, originalData.id, newId]
    );
    
    return newId;
  }
  
  /**
   * Validate data ownership
   */
  async validateDataOwnership(dataType, dataId, identityId, contextId) {
    const tableMap = {
      note: 'notes',
      task: 'tasks',
      project: 'projects',
      thread: 'threads',
      document: 'documents'
    };
    
    const table = tableMap[dataType];
    if (!table) {
      throw new Error(`Unknown data type: ${dataType}`);
    }
    
    const result = await this.pool.query(
      `SELECT id FROM ${table} 
       WHERE id = $1 AND identity_id = $2 AND context_id = $3`,
      [dataId, identityId, contextId]
    );
    
    if (result.rows.length === 0) {
      throw new Error('Data not found or does not belong to current identity/context');
    }
    
    return true;
  }
  
  /**
   * Log sharing action
   */
  async logSharing(request) {
    await this.pool.query(
      `INSERT INTO identity_sharing_log 
       (request_id, source_identity_id, target_identity_id, 
        data_type, data_id, sharing_mode, executed_at)
       VALUES ($1, $2, $3, $4, $5, $6, NOW())`,
      [
        request.id,
        request.source_identity_id,
        request.target_identity_id,
        request.data_type,
        request.data_id,
        request.sharing_mode
      ]
    );
  }
  
  /**
   * Get references accessible in current identity
   */
  async getReferences(identityId, contextId = null) {
    let query = `
      SELECT ir.*, 
             i.type as source_identity_type,
             i.name as source_identity_name
      FROM identity_references ir
      JOIN identities i ON ir.source_identity_id = i.id
      WHERE ir.target_identity_id = $1
    `;
    
    const params = [identityId];
    
    if (contextId) {
      query += ` AND ir.target_context_id = $2`;
      params.push(contextId);
    }
    
    query += ` ORDER BY ir.created_at DESC`;
    
    const result = await this.pool.query(query, params);
    return result.rows;
  }
  
  /**
   * Resolve reference (get original data)
   */
  async resolveReference(referenceId, currentIdentityId) {
    // Get reference
    const refResult = await this.pool.query(
      `SELECT * FROM identity_references WHERE id = $1`,
      [referenceId]
    );
    
    if (refResult.rows.length === 0) {
      throw new Error('Reference not found');
    }
    
    const reference = refResult.rows[0];
    
    // Validate access
    if (reference.target_identity_id !== currentIdentityId) {
      throw new Error('Reference not accessible in current identity');
    }
    
    // Get original data
    const originalData = await this.getDataById(
      reference.data_type,
      reference.data_id
    );
    
    return {
      reference,
      data: originalData,
      is_reference: true,
      source_identity_id: reference.source_identity_id
    };
  }
  
  /**
   * Get sharing history
   */
  async getSharingHistory(identityId, options = {}) {
    let query = `
      SELECT sr.*,
             si.name as source_identity_name,
             ti.name as target_identity_name
      FROM sharing_requests sr
      JOIN identities si ON sr.source_identity_id = si.id
      JOIN identities ti ON sr.target_identity_id = ti.id
      WHERE (sr.source_identity_id = $1 OR sr.target_identity_id = $1)
    `;
    
    const params = [identityId];
    
    if (options.status) {
      query += ` AND sr.status = $2`;
      params.push(options.status);
    }
    
    query += ` ORDER BY sr.requested_at DESC`;
    
    if (options.limit) {
      query += ` LIMIT $${params.length + 1}`;
      params.push(options.limit);
    }
    
    const result = await this.pool.query(query, params);
    return result.rows;
  }
  
  /**
   * Revoke reference
   */
  async revokeReference(referenceId, userId) {
    // Get reference
    const refResult = await this.pool.query(
      `SELECT * FROM identity_references WHERE id = $1`,
      [referenceId]
    );
    
    if (refResult.rows.length === 0) {
      throw new Error('Reference not found');
    }
    
    const reference = refResult.rows[0];
    
    // Validate user owns source identity
    const sourceIdentity = await this.identityManager.getIdentity(
      reference.source_identity_id
    );
    
    if (sourceIdentity.user_id !== userId) {
      throw new Error('Only source identity owner can revoke reference');
    }
    
    // Delete reference
    await this.pool.query(
      `DELETE FROM identity_references WHERE id = $1`,
      [referenceId]
    );
    
    // Log revocation
    await this.pool.query(
      `INSERT INTO identity_sharing_log 
       (request_id, source_identity_id, target_identity_id, 
        data_type, data_id, sharing_mode, action, executed_at)
       VALUES (NULL, $1, $2, $3, $4, 'reference', 'revoke', NOW())`,
      [
        reference.source_identity_id,
        reference.target_identity_id,
        reference.data_type,
        reference.data_id
      ]
    );
    
    return {
      revoked: true,
      reference_id: referenceId,
      message: 'Reference revoked successfully'
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  SharingRequest,
  SharingManager
};
