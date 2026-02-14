/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM CHECKPOINT MANAGER - CHE·NU™ V76
 * Systeme HITL (Human-In-The-Loop) pour Gouvernance des Actions
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * PRINCIPE FONDAMENTAL: GOUVERNANCE > EXECUTION
 * Les agents recommandent, ils ne decident JAMAIS seuls.
 *
 * Conforme au repo canonique: github.com/Pr0Services/ATOM
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKPOINT TYPES
// ═══════════════════════════════════════════════════════════════════════════════

const CHECKPOINT_TYPES = {
    HITL: 'hitl',           // Human-In-The-Loop - Approbation humaine requise
    OPA: 'opa',             // Policy check automatique
    THRESHOLD: 'threshold', // Seuil depasse
    ESCALATION: 'escalation', // Escalade niveau superieur
    APPROVAL: 'approval'    // Approbation explicite requise
};

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKPOINT RESOLUTIONS
// ═══════════════════════════════════════════════════════════════════════════════

const CHECKPOINT_RESOLUTIONS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    REJECTED: 'rejected',
    ESCALATED: 'escalated',
    TIMEOUT: 'timeout',
    AUTO_APPROVED: 'auto_approved'
};

// ═══════════════════════════════════════════════════════════════════════════════
// ACTION TYPES (pour evaluation)
// ═══════════════════════════════════════════════════════════════════════════════

const ACTION_TYPES = {
    READ: 'read',
    WRITE: 'write',
    EXECUTE: 'execute',
    DELETE: 'delete',
    TRANSFER: 'transfer',
    CONFIGURE: 'configure',
    EXTERNAL_API: 'external_api'
};

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKPOINT RULE
// ═══════════════════════════════════════════════════════════════════════════════

class CheckpointRule {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.description = config.description || '';
        this.priority = config.priority || 100; // Plus bas = plus prioritaire
        this.condition = config.condition;      // Function(action) => boolean
        this.checkpointType = config.checkpointType;
        this.timeout = config.timeout || 3600000; // 1 heure par defaut
        this.autoApproveBelow = config.autoApproveBelow || null;
        this.enabled = config.enabled !== false;
    }

    /**
     * Evalue si la regle s'applique a une action
     */
    evaluate(action) {
        if (!this.enabled) return false;

        try {
            return this.condition(action);
        } catch (err) {
            console.error(`[CheckpointRule] Error evaluating ${this.id}:`, err);
            // En cas d'erreur, on cree un checkpoint par securite
            return true;
        }
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKPOINT
// ═══════════════════════════════════════════════════════════════════════════════

class Checkpoint {
    constructor(config) {
        this.id = 'cp_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 6);
        this.type = config.type;
        this.ruleId = config.ruleId || null;
        this.action = config.action;
        this.agentId = config.agentId;
        this.estimatedImpact = config.estimatedImpact || 0.5;

        this.status = CHECKPOINT_RESOLUTIONS.PENDING;
        this.createdAt = Date.now();
        this.timeout = config.timeout || 3600000;
        this.expiresAt = this.createdAt + this.timeout;

        this.resolution = null;
        this.resolvedAt = null;
        this.resolvedBy = null;
        this.resolutionNotes = null;

        this.escalatedTo = null;
        this.escalatedAt = null;
    }

    /**
     * Approuve le checkpoint
     */
    approve(resolvedBy, notes = '') {
        this.status = CHECKPOINT_RESOLUTIONS.APPROVED;
        this.resolution = 'approved';
        this.resolvedAt = Date.now();
        this.resolvedBy = resolvedBy;
        this.resolutionNotes = notes;
        return this;
    }

    /**
     * Rejette le checkpoint
     */
    reject(resolvedBy, notes = '') {
        this.status = CHECKPOINT_RESOLUTIONS.REJECTED;
        this.resolution = 'rejected';
        this.resolvedAt = Date.now();
        this.resolvedBy = resolvedBy;
        this.resolutionNotes = notes;
        return this;
    }

    /**
     * Escalade le checkpoint
     */
    escalate(escalatedTo, notes = '') {
        this.status = CHECKPOINT_RESOLUTIONS.ESCALATED;
        this.escalatedTo = escalatedTo;
        this.escalatedAt = Date.now();
        this.resolutionNotes = notes;
        return this;
    }

    /**
     * Verifie si le checkpoint a expire
     */
    isExpired() {
        return Date.now() > this.expiresAt;
    }

    /**
     * Exporte pour serialisation
     */
    toJSON() {
        return {
            id: this.id,
            type: this.type,
            ruleId: this.ruleId,
            action: this.action,
            agentId: this.agentId,
            estimatedImpact: this.estimatedImpact,
            status: this.status,
            createdAt: this.createdAt,
            expiresAt: this.expiresAt,
            resolution: this.resolution,
            resolvedAt: this.resolvedAt,
            resolvedBy: this.resolvedBy,
            resolutionNotes: this.resolutionNotes
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// DEFAULT RULES - Regles HITL par defaut
// ═══════════════════════════════════════════════════════════════════════════════

const DEFAULT_RULES = [
    // R001: Impact eleve → HITL obligatoire
    new CheckpointRule({
        id: 'R001_HIGH_IMPACT',
        name: 'High Impact Actions',
        description: 'Actions avec impact estime > 0.7 necessitent approbation humaine',
        priority: 10,
        checkpointType: CHECKPOINT_TYPES.HITL,
        condition: (action) => action.estimatedImpact > 0.7,
        timeout: 3600000 // 1 heure
    }),

    // R002: Operations d'ecriture → Approbation
    new CheckpointRule({
        id: 'R002_WRITE_OPS',
        name: 'Write Operations',
        description: 'Toute operation d\'ecriture necessite approbation',
        priority: 20,
        checkpointType: CHECKPOINT_TYPES.APPROVAL,
        condition: (action) => action.type === ACTION_TYPES.WRITE,
        timeout: 1800000 // 30 minutes
    }),

    // R003: Operations de suppression → HITL
    new CheckpointRule({
        id: 'R003_DELETE_OPS',
        name: 'Delete Operations',
        description: 'Les suppressions necessitent validation humaine',
        priority: 5,
        checkpointType: CHECKPOINT_TYPES.HITL,
        condition: (action) => action.type === ACTION_TYPES.DELETE,
        timeout: 3600000
    }),

    // R004: Transferts → HITL
    new CheckpointRule({
        id: 'R004_TRANSFERS',
        name: 'Transfer Operations',
        description: 'Transferts de valeur necessitent validation',
        priority: 5,
        checkpointType: CHECKPOINT_TYPES.HITL,
        condition: (action) => action.type === ACTION_TYPES.TRANSFER,
        timeout: 7200000 // 2 heures
    }),

    // R005: Appels API externes → Policy
    new CheckpointRule({
        id: 'R005_EXTERNAL_API',
        name: 'External API Calls',
        description: 'Appels API externes passes par policy check',
        priority: 30,
        checkpointType: CHECKPOINT_TYPES.OPA,
        condition: (action) => action.type === ACTION_TYPES.EXTERNAL_API,
        autoApproveBelow: 0.3, // Auto-approve si impact < 0.3
        timeout: 300000 // 5 minutes
    }),

    // R006: Configuration systeme → HITL
    new CheckpointRule({
        id: 'R006_CONFIG',
        name: 'System Configuration',
        description: 'Modifications de configuration systeme',
        priority: 15,
        checkpointType: CHECKPOINT_TYPES.HITL,
        condition: (action) => action.type === ACTION_TYPES.CONFIGURE,
        timeout: 3600000
    }),

    // R007: Impact moyen → Threshold check
    new CheckpointRule({
        id: 'R007_MEDIUM_IMPACT',
        name: 'Medium Impact Actions',
        description: 'Actions avec impact 0.3-0.7 passent par threshold',
        priority: 50,
        checkpointType: CHECKPOINT_TYPES.THRESHOLD,
        condition: (action) => action.estimatedImpact >= 0.3 && action.estimatedImpact <= 0.7,
        autoApproveBelow: 0.4,
        timeout: 900000 // 15 minutes
    })
];

// ═══════════════════════════════════════════════════════════════════════════════
// CHECKPOINT MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

class ATOMCheckpointManager {
    constructor(options = {}) {
        this.rules = [...DEFAULT_RULES];
        this.checkpoints = new Map();       // id -> Checkpoint
        this.pendingQueue = [];             // Queue des checkpoints en attente
        this.auditLog = [];
        this.maxLogSize = 5000;

        // Callbacks
        this.onCheckpointCreated = options.onCheckpointCreated || null;
        this.onCheckpointResolved = options.onCheckpointResolved || null;
        this.onApprovalRequired = options.onApprovalRequired || null;

        // Stats
        this.stats = {
            created: 0,
            approved: 0,
            rejected: 0,
            escalated: 0,
            autoApproved: 0,
            expired: 0
        };

        // Check expirations toutes les minutes
        this.expirationInterval = setInterval(() => this._checkExpirations(), 60000);

        console.log('%c[AT-OM CheckpointManager] Initialized with HITL governance', 'color: #9333EA;');
        console.log(`[CheckpointManager] ${this.rules.length} rules loaded`);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // RULE MANAGEMENT
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Ajoute une regle personnalisee
     */
    addRule(rule) {
        if (!(rule instanceof CheckpointRule)) {
            rule = new CheckpointRule(rule);
        }
        this.rules.push(rule);
        // Tri par priorite
        this.rules.sort((a, b) => a.priority - b.priority);
        return rule;
    }

    /**
     * Supprime une regle
     */
    removeRule(ruleId) {
        const idx = this.rules.findIndex(r => r.id === ruleId);
        if (idx !== -1) {
            this.rules.splice(idx, 1);
            return true;
        }
        return false;
    }

    /**
     * Active/desactive une regle
     */
    toggleRule(ruleId, enabled) {
        const rule = this.rules.find(r => r.id === ruleId);
        if (rule) {
            rule.enabled = enabled;
            return true;
        }
        return false;
    }

    /**
     * Liste les regles actives
     */
    getRules() {
        return this.rules.map(r => ({
            id: r.id,
            name: r.name,
            description: r.description,
            type: r.checkpointType,
            priority: r.priority,
            enabled: r.enabled
        }));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ACTION EVALUATION
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Evalue une action et cree un checkpoint si necessaire
     * @param {Object} action - L'action a evaluer
     * @returns {Object} - { needsCheckpoint, checkpoint, autoApproved }
     */
    evaluateAction(action) {
        // Normalise l'action
        action = this._normalizeAction(action);

        // Evalue toutes les regles par priorite
        for (const rule of this.rules) {
            if (rule.evaluate(action)) {
                // Auto-approve si sous le seuil
                if (rule.autoApproveBelow && action.estimatedImpact < rule.autoApproveBelow) {
                    this.stats.autoApproved++;
                    this._log('auto_approved', action, rule.id);
                    return {
                        needsCheckpoint: false,
                        autoApproved: true,
                        rule: rule.id
                    };
                }

                // Cree un checkpoint
                const checkpoint = this.createCheckpoint({
                    type: rule.checkpointType,
                    ruleId: rule.id,
                    action: action,
                    agentId: action.agentId || 'unknown',
                    estimatedImpact: action.estimatedImpact,
                    timeout: rule.timeout
                });

                return {
                    needsCheckpoint: true,
                    checkpoint: checkpoint,
                    autoApproved: false
                };
            }
        }

        // Aucune regle matchee → action autorisee
        this._log('no_checkpoint_needed', action, null);
        return {
            needsCheckpoint: false,
            autoApproved: true
        };
    }

    /**
     * Normalise une action pour evaluation
     */
    _normalizeAction(action) {
        return {
            id: action.id || 'action_' + Date.now(),
            type: action.type || ACTION_TYPES.READ,
            name: action.name || 'Unknown Action',
            description: action.description || '',
            agentId: action.agentId || action.from || 'unknown',
            estimatedImpact: action.estimatedImpact ?? action.impact ?? 0.5,
            target: action.target || null,
            params: action.params || {},
            timestamp: action.timestamp || Date.now()
        };
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CHECKPOINT LIFECYCLE
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Cree un nouveau checkpoint
     */
    createCheckpoint(config) {
        const checkpoint = new Checkpoint(config);

        this.checkpoints.set(checkpoint.id, checkpoint);
        this.pendingQueue.push(checkpoint.id);
        this.stats.created++;

        this._log('checkpoint_created', config.action, config.ruleId, checkpoint.id);

        // Callback
        if (this.onCheckpointCreated) {
            this.onCheckpointCreated(checkpoint);
        }

        // Notification pour approbation
        if (this.onApprovalRequired) {
            this.onApprovalRequired(checkpoint);
        }

        console.log(`%c[CheckpointManager] Checkpoint created: ${checkpoint.id} (${checkpoint.type})`, 'color: #FF6B35;');

        return checkpoint;
    }

    /**
     * Approuve un checkpoint
     */
    approveCheckpoint(checkpointId, approvedBy, notes = '') {
        const checkpoint = this.checkpoints.get(checkpointId);
        if (!checkpoint) {
            return { success: false, error: 'Checkpoint not found' };
        }

        if (checkpoint.status !== CHECKPOINT_RESOLUTIONS.PENDING) {
            return { success: false, error: 'Checkpoint already resolved' };
        }

        checkpoint.approve(approvedBy, notes);
        this._removefromPending(checkpointId);
        this.stats.approved++;

        this._log('checkpoint_approved', checkpoint.action, checkpoint.ruleId, checkpointId, approvedBy);

        if (this.onCheckpointResolved) {
            this.onCheckpointResolved(checkpoint, 'approved');
        }

        // Synchroniser avec le backend (fire-and-forget)
        this._syncResolution(checkpointId, 'approve', approvedBy, notes);

        console.log(`%c[CheckpointManager] Checkpoint APPROVED: ${checkpointId}`, 'color: #00FF88;');
        return { success: true, checkpoint };
    }

    /**
     * Rejette un checkpoint
     */
    rejectCheckpoint(checkpointId, rejectedBy, notes = '') {
        const checkpoint = this.checkpoints.get(checkpointId);
        if (!checkpoint) {
            return { success: false, error: 'Checkpoint not found' };
        }

        if (checkpoint.status !== CHECKPOINT_RESOLUTIONS.PENDING) {
            return { success: false, error: 'Checkpoint already resolved' };
        }

        checkpoint.reject(rejectedBy, notes);
        this._removefromPending(checkpointId);
        this.stats.rejected++;

        this._log('checkpoint_rejected', checkpoint.action, checkpoint.ruleId, checkpointId, rejectedBy);

        if (this.onCheckpointResolved) {
            this.onCheckpointResolved(checkpoint, 'rejected');
        }

        // Synchroniser avec le backend (fire-and-forget)
        this._syncResolution(checkpointId, 'reject', rejectedBy, notes);

        console.log(`%c[CheckpointManager] Checkpoint REJECTED: ${checkpointId}`, 'color: #FF6B6B;');
        return { success: true, checkpoint };
    }

    /**
     * Escalade un checkpoint
     */
    escalateCheckpoint(checkpointId, escalatedTo, notes = '') {
        const checkpoint = this.checkpoints.get(checkpointId);
        if (!checkpoint) {
            return { success: false, error: 'Checkpoint not found' };
        }

        checkpoint.escalate(escalatedTo, notes);
        this.stats.escalated++;

        this._log('checkpoint_escalated', checkpoint.action, checkpoint.ruleId, checkpointId, escalatedTo);

        if (this.onCheckpointResolved) {
            this.onCheckpointResolved(checkpoint, 'escalated');
        }

        console.log(`%c[CheckpointManager] Checkpoint ESCALATED: ${checkpointId} → ${escalatedTo}`, 'color: #FFD700;');
        return { success: true, checkpoint };
    }

    /**
     * Synchronise la résolution d'un checkpoint avec le backend API
     * Fire-and-forget : ne bloque pas le flux local
     */
    _syncResolution(checkpointId, action, resolvedBy, notes) {
        if (typeof atomPost !== 'function') return;
        atomPost(`/api/v2/checkpoints/${checkpointId}/${action}`, {
            resolved_by: resolvedBy,
            notes: notes
        }).then(resp => {
            if (resp.ok) {
                console.log(`[CheckpointManager] Backend synced: ${checkpointId} → ${action}`);
            } else {
                console.warn(`[CheckpointManager] Backend sync failed: HTTP ${resp.status}`);
            }
        }).catch(err => {
            console.warn(`[CheckpointManager] Backend sync error: ${err.message}`);
        });
    }

    /**
     * Retire de la queue pending
     */
    _removefromPending(checkpointId) {
        const idx = this.pendingQueue.indexOf(checkpointId);
        if (idx !== -1) {
            this.pendingQueue.splice(idx, 1);
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // QUERIES
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Recupere un checkpoint
     */
    getCheckpoint(checkpointId) {
        return this.checkpoints.get(checkpointId);
    }

    /**
     * Liste les checkpoints en attente
     */
    getPending() {
        return this.pendingQueue.map(id => this.checkpoints.get(id)).filter(Boolean);
    }

    /**
     * Liste tous les checkpoints
     */
    getAll(limit = 100) {
        return [...this.checkpoints.values()]
            .sort((a, b) => b.createdAt - a.createdAt)
            .slice(0, limit);
    }

    /**
     * Checkpoints par agent
     */
    getByAgent(agentId) {
        return [...this.checkpoints.values()]
            .filter(cp => cp.agentId === agentId)
            .sort((a, b) => b.createdAt - a.createdAt);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // EXPIRATION & CLEANUP
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Verifie les checkpoints expires
     */
    _checkExpirations() {
        const now = Date.now();
        let expiredCount = 0;

        this.pendingQueue.forEach(id => {
            const checkpoint = this.checkpoints.get(id);
            if (checkpoint && checkpoint.isExpired()) {
                checkpoint.status = CHECKPOINT_RESOLUTIONS.TIMEOUT;
                checkpoint.resolvedAt = now;
                this._removefromPending(id);
                this.stats.expired++;
                expiredCount++;

                this._log('checkpoint_expired', checkpoint.action, checkpoint.ruleId, id);

                if (this.onCheckpointResolved) {
                    this.onCheckpointResolved(checkpoint, 'timeout');
                }
            }
        });

        if (expiredCount > 0) {
            console.log(`[CheckpointManager] ${expiredCount} checkpoints expired`);
        }
    }

    /**
     * Nettoie les vieux checkpoints resolus
     */
    cleanup(maxAge = 86400000) { // 24 heures
        const cutoff = Date.now() - maxAge;
        let cleaned = 0;

        this.checkpoints.forEach((cp, id) => {
            if (cp.status !== CHECKPOINT_RESOLUTIONS.PENDING && cp.createdAt < cutoff) {
                this.checkpoints.delete(id);
                cleaned++;
            }
        });

        if (cleaned > 0) {
            console.log(`[CheckpointManager] Cleaned ${cleaned} old checkpoints`);
        }
        return cleaned;
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AUDIT LOG
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Ajoute une entree au log
     */
    _log(event, action, ruleId, checkpointId = null, actor = null) {
        this.auditLog.push({
            timestamp: Date.now(),
            event: event,
            actionId: action?.id,
            actionType: action?.type,
            ruleId: ruleId,
            checkpointId: checkpointId,
            actor: actor
        });

        // Limite taille
        if (this.auditLog.length > this.maxLogSize) {
            this.auditLog = this.auditLog.slice(-this.maxLogSize / 2);
        }
    }

    /**
     * Recupere l'audit log
     */
    getAuditLog(limit = 100) {
        return this.auditLog.slice(-limit);
    }

    /**
     * Stats globales
     */
    getStats() {
        return {
            ...this.stats,
            pendingCount: this.pendingQueue.length,
            totalCheckpoints: this.checkpoints.size,
            rulesCount: this.rules.length
        };
    }

    /**
     * Destruction propre
     */
    destroy() {
        clearInterval(this.expirationInterval);
        this.checkpoints.clear();
        this.pendingQueue = [];
        console.log('[CheckpointManager] Destroyed');
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════════════════

let checkpointManagerInstance = null;

function getCheckpointManager(options = {}) {
    if (!checkpointManagerInstance) {
        checkpointManagerInstance = new ATOMCheckpointManager(options);
    }
    return checkpointManagerInstance;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CHECKPOINT_TYPES,
        CHECKPOINT_RESOLUTIONS,
        ACTION_TYPES,
        CheckpointRule,
        Checkpoint,
        ATOMCheckpointManager,
        getCheckpointManager,
        DEFAULT_RULES
    };
}

// Global pour browser
if (typeof window !== 'undefined') {
    window.ATOM_CHECKPOINT_TYPES = CHECKPOINT_TYPES;
    window.ATOM_CHECKPOINT_RESOLUTIONS = CHECKPOINT_RESOLUTIONS;
    window.ATOM_ACTION_TYPES = ACTION_TYPES;
    window.ATOMCheckpointManager = ATOMCheckpointManager;
    window.getATOMCheckpointManager = getCheckpointManager;
}

console.log('%c[AT-OM] CheckpointManager loaded - GOUVERNANCE > EXECUTION', 'color: #9333EA; font-weight: bold;');
