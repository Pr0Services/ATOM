/**
 * CHE·NU™ LIFECYCLE AUDIT SYSTEM
 * 
 * Complete audit trail for all state transitions.
 * 
 * AUDIT PRINCIPLES:
 * - All transitions must be logged
 * - All logs are timestamped and attributable
 * - Audit trail is immutable
 * - Historical context is preserved
 * - Traceability is guaranteed
 */

const { LIFECYCLE_REGISTRY } = require('./LIFECYCLE_SYSTEM');

// ═══════════════════════════════════════════════════════════════
// AUDIT LOG ENTRY
// ═══════════════════════════════════════════════════════════════

class AuditLogEntry {
  constructor(data) {
    this.id = data.id || `audit-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    this.timestamp = new Date().toISOString();
    
    // Object identification
    this.object_type = data.object_type;
    this.object_id = data.object_id;
    
    // Transition details
    this.from_state = data.from_state;
    this.to_state = data.to_state;
    this.transition_type = data.transition_type || 'manual'; // manual, automated, system
    
    // Attribution
    this.initiated_by = data.initiated_by; // user_id or 'system'
    this.executed_by = data.executed_by; // user_id, agent_id, or 'system'
    this.approved_by = data.approved_by || null;
    
    // Context
    this.context = data.context || {};
    this.reason = data.reason || null;
    this.requirements_met = data.requirements_met || [];
    
    // Result
    this.success = data.success;
    this.error = data.error || null;
    this.rollback = data.rollback || false;
    
    // Metadata
    this.reversible = data.reversible || false;
    this.immediate = data.immediate || false;
    
    // Traceability
    this.session_id = data.session_id || null;
    this.request_id = data.request_id || null;
  }
  
  /**
   * Convert to database format
   */
  toDatabaseFormat() {
    return {
      id: this.id,
      timestamp: this.timestamp,
      object_type: this.object_type,
      object_id: this.object_id,
      from_state: this.from_state,
      to_state: this.to_state,
      transition_type: this.transition_type,
      initiated_by: this.initiated_by,
      executed_by: this.executed_by,
      approved_by: this.approved_by,
      context: JSON.stringify(this.context),
      reason: this.reason,
      requirements_met: JSON.stringify(this.requirements_met),
      success: this.success,
      error: this.error,
      rollback: this.rollback,
      reversible: this.reversible,
      immediate: this.immediate,
      session_id: this.session_id,
      request_id: this.request_id
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// LIFECYCLE AUDIT MANAGER
// ═══════════════════════════════════════════════════════════════

class LifecycleAuditManager {
  constructor(pool) {
    this.pool = pool;
  }
  
  /**
   * Log state transition
   */
  async logTransition(transitionData) {
    const entry = new AuditLogEntry(transitionData);
    const dbFormat = entry.toDatabaseFormat();
    
    await this.pool.query(
      `INSERT INTO lifecycle_audit_log 
       (id, timestamp, object_type, object_id, from_state, to_state,
        transition_type, initiated_by, executed_by, approved_by,
        context, reason, requirements_met, success, error, rollback,
        reversible, immediate, session_id, request_id)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)`,
      [
        dbFormat.id,
        dbFormat.timestamp,
        dbFormat.object_type,
        dbFormat.object_id,
        dbFormat.from_state,
        dbFormat.to_state,
        dbFormat.transition_type,
        dbFormat.initiated_by,
        dbFormat.executed_by,
        dbFormat.approved_by,
        dbFormat.context,
        dbFormat.reason,
        dbFormat.requirements_met,
        dbFormat.success,
        dbFormat.error,
        dbFormat.rollback,
        dbFormat.reversible,
        dbFormat.immediate,
        dbFormat.session_id,
        dbFormat.request_id
      ]
    );
    
    return entry;
  }
  
  /**
   * Get audit history for object
   */
  async getObjectHistory(objectType, objectId) {
    const result = await this.pool.query(
      `SELECT * FROM lifecycle_audit_log 
       WHERE object_type = $1 AND object_id = $2
       ORDER BY timestamp ASC`,
      [objectType, objectId]
    );
    
    return result.rows.map(row => this.parseAuditEntry(row));
  }
  
  /**
   * Get recent transitions
   */
  async getRecentTransitions(limit = 50, filters = {}) {
    let query = `SELECT * FROM lifecycle_audit_log WHERE 1=1`;
    const params = [];
    let paramCount = 1;
    
    // Apply filters
    if (filters.object_type) {
      query += ` AND object_type = $${paramCount}`;
      params.push(filters.object_type);
      paramCount++;
    }
    
    if (filters.initiated_by) {
      query += ` AND initiated_by = $${paramCount}`;
      params.push(filters.initiated_by);
      paramCount++;
    }
    
    if (filters.success !== undefined) {
      query += ` AND success = $${paramCount}`;
      params.push(filters.success);
      paramCount++;
    }
    
    if (filters.from_date) {
      query += ` AND timestamp >= $${paramCount}`;
      params.push(filters.from_date);
      paramCount++;
    }
    
    query += ` ORDER BY timestamp DESC LIMIT $${paramCount}`;
    params.push(limit);
    
    const result = await this.pool.query(query, params);
    return result.rows.map(row => this.parseAuditEntry(row));
  }
  
  /**
   * Get failed transitions
   */
  async getFailedTransitions(objectType = null, limit = 100) {
    let query = `SELECT * FROM lifecycle_audit_log WHERE success = false`;
    const params = [];
    
    if (objectType) {
      query += ` AND object_type = $1`;
      params.push(objectType);
      query += ` ORDER BY timestamp DESC LIMIT $2`;
      params.push(limit);
    } else {
      query += ` ORDER BY timestamp DESC LIMIT $1`;
      params.push(limit);
    }
    
    const result = await this.pool.query(query, params);
    return result.rows.map(row => this.parseAuditEntry(row));
  }
  
  /**
   * Get transition statistics
   */
  async getStatistics(objectType = null, timeRange = null) {
    let query = `
      SELECT 
        object_type,
        COUNT(*) as total_transitions,
        COUNT(*) FILTER (WHERE success = true) as successful,
        COUNT(*) FILTER (WHERE success = false) as failed,
        COUNT(*) FILTER (WHERE rollback = true) as rollbacks,
        COUNT(DISTINCT object_id) as unique_objects,
        COUNT(DISTINCT initiated_by) as unique_users
      FROM lifecycle_audit_log
      WHERE 1=1
    `;
    
    const params = [];
    let paramCount = 1;
    
    if (objectType) {
      query += ` AND object_type = $${paramCount}`;
      params.push(objectType);
      paramCount++;
    }
    
    if (timeRange) {
      query += ` AND timestamp >= $${paramCount}`;
      params.push(timeRange);
      paramCount++;
    }
    
    query += ` GROUP BY object_type`;
    
    const result = await this.pool.query(query, params);
    return result.rows;
  }
  
  /**
   * Get state transition patterns
   */
  async getTransitionPatterns(objectType, limit = 20) {
    const result = await this.pool.query(
      `SELECT 
         from_state,
         to_state,
         COUNT(*) as frequency,
         AVG(CASE WHEN success THEN 1 ELSE 0 END) as success_rate
       FROM lifecycle_audit_log
       WHERE object_type = $1
       GROUP BY from_state, to_state
       ORDER BY frequency DESC
       LIMIT $2`,
      [objectType, limit]
    );
    
    return result.rows;
  }
  
  /**
   * Verify audit trail integrity
   */
  async verifyIntegrity(objectType, objectId) {
    const history = await this.getObjectHistory(objectType, objectId);
    const lifecycle = LIFECYCLE_REGISTRY[objectType];
    
    if (!lifecycle) {
      return {
        valid: false,
        error: 'Unknown object type'
      };
    }
    
    const issues = [];
    
    // Check if initial state matches
    if (history.length > 0 && history[0].from_state !== lifecycle.initial_state) {
      issues.push('First transition does not start from initial state');
    }
    
    // Check for state continuity
    for (let i = 1; i < history.length; i++) {
      const prev = history[i - 1];
      const curr = history[i];
      
      if (prev.to_state !== curr.from_state) {
        issues.push(`Continuity break at entry ${i}: ${prev.to_state} -> ${curr.from_state}`);
      }
    }
    
    // Check for invalid transitions
    for (const entry of history) {
      const validTransition = lifecycle.transitions.find(
        t => t.from === entry.from_state && t.to === entry.to_state
      );
      
      if (!validTransition) {
        issues.push(`Invalid transition: ${entry.from_state} -> ${entry.to_state} at ${entry.timestamp}`);
      }
    }
    
    return {
      valid: issues.length === 0,
      issues,
      entries_checked: history.length
    };
  }
  
  /**
   * Generate audit report
   */
  async generateReport(filters = {}) {
    const statistics = await this.getStatistics(
      filters.object_type,
      filters.from_date
    );
    
    const recentTransitions = await this.getRecentTransitions(20, filters);
    const failedTransitions = await this.getFailedTransitions(filters.object_type, 10);
    
    let patterns = [];
    if (filters.object_type) {
      patterns = await this.getTransitionPatterns(filters.object_type, 10);
    }
    
    return {
      generated_at: new Date().toISOString(),
      filters,
      statistics,
      recent_transitions: recentTransitions,
      failed_transitions: failedTransitions,
      patterns: patterns.length > 0 ? patterns : null
    };
  }
  
  /**
   * Parse audit entry from database
   */
  parseAuditEntry(row) {
    return {
      ...row,
      context: typeof row.context === 'string' ? JSON.parse(row.context) : row.context,
      requirements_met: typeof row.requirements_met === 'string' 
        ? JSON.parse(row.requirements_met) 
        : row.requirements_met
    };
  }
  
  /**
   * Search audit log
   */
  async search(criteria) {
    let query = `SELECT * FROM lifecycle_audit_log WHERE 1=1`;
    const params = [];
    let paramCount = 1;
    
    // Object filters
    if (criteria.object_type) {
      query += ` AND object_type = $${paramCount}`;
      params.push(criteria.object_type);
      paramCount++;
    }
    
    if (criteria.object_id) {
      query += ` AND object_id = $${paramCount}`;
      params.push(criteria.object_id);
      paramCount++;
    }
    
    // State filters
    if (criteria.from_state) {
      query += ` AND from_state = $${paramCount}`;
      params.push(criteria.from_state);
      paramCount++;
    }
    
    if (criteria.to_state) {
      query += ` AND to_state = $${paramCount}`;
      params.push(criteria.to_state);
      paramCount++;
    }
    
    // User filters
    if (criteria.initiated_by) {
      query += ` AND initiated_by = $${paramCount}`;
      params.push(criteria.initiated_by);
      paramCount++;
    }
    
    if (criteria.executed_by) {
      query += ` AND executed_by = $${paramCount}`;
      params.push(criteria.executed_by);
      paramCount++;
    }
    
    // Time filters
    if (criteria.from_date) {
      query += ` AND timestamp >= $${paramCount}`;
      params.push(criteria.from_date);
      paramCount++;
    }
    
    if (criteria.to_date) {
      query += ` AND timestamp <= $${paramCount}`;
      params.push(criteria.to_date);
      paramCount++;
    }
    
    // Success filter
    if (criteria.success !== undefined) {
      query += ` AND success = $${paramCount}`;
      params.push(criteria.success);
      paramCount++;
    }
    
    query += ` ORDER BY timestamp DESC`;
    
    // Limit
    if (criteria.limit) {
      query += ` LIMIT $${paramCount}`;
      params.push(criteria.limit);
    } else {
      query += ` LIMIT 100`;
    }
    
    const result = await this.pool.query(query, params);
    return result.rows.map(row => this.parseAuditEntry(row));
  }
  
  /**
   * Export audit log
   */
  async exportAuditLog(filters = {}, format = 'json') {
    const entries = await this.search({
      ...filters,
      limit: null // No limit for export
    });
    
    if (format === 'json') {
      return JSON.stringify(entries, null, 2);
    }
    
    if (format === 'csv') {
      // Simplified CSV export
      const headers = [
        'timestamp',
        'object_type',
        'object_id',
        'from_state',
        'to_state',
        'initiated_by',
        'success'
      ];
      
      const rows = entries.map(entry => 
        headers.map(h => entry[h]).join(',')
      );
      
      return [headers.join(','), ...rows].join('\n');
    }
    
    throw new Error(`Unsupported export format: ${format}`);
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

module.exports = {
  AuditLogEntry,
  LifecycleAuditManager
};
