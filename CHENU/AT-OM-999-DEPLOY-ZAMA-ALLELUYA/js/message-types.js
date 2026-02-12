/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM MESSAGE TYPES - CHE·NU™ V76
 * Types de Messages Standards pour Communication Inter-Agents
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Conforme au repo canonique: github.com/Pr0Services/ATOM
 * 13 types de messages + priorites + factory
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE TYPES - Standards Inter-Agents
// ═══════════════════════════════════════════════════════════════════════════════

const MESSAGE_TYPES = {
    // Communication de base
    REQUEST: 'request',           // Demande d'action
    RESPONSE: 'response',         // Reponse a une requete
    COMMAND: 'command',           // Ordre direct (L0/L1 seulement)
    ACK: 'ack',                   // Accusé de reception

    // Evenements
    EVENT: 'event',               // Notification d'evenement
    STATUS: 'status',             // Mise a jour de statut
    HEARTBEAT: 'heartbeat',       // Signal de vie (health check)

    // Delegation de taches
    TASK_DELEGATE: 'task_delegate',   // Delegation d'une tache
    TASK_ACCEPT: 'task_accept',       // Acceptation de tache
    TASK_REJECT: 'task_reject',       // Refus de tache
    TASK_COMPLETE: 'task_complete',   // Tache terminee

    // Gouvernance
    ESCALATE: 'escalate',         // Escalade vers niveau superieur
    CHECKPOINT: 'checkpoint'      // Point de controle HITL
};

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE PRIORITIES
// ═══════════════════════════════════════════════════════════════════════════════

const MESSAGE_PRIORITIES = {
    CRITICAL: 0,    // Urgence absolue (Gestion de crise)
    HIGH: 1,        // Priorite haute (HITL, escalations)
    MEDIUM: 2,      // Normal
    LOW: 3,         // Basse priorite (logs, stats)
    BACKGROUND: 4   // Arriere-plan (heartbeats)
};

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE SCHEMA
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Structure d'un message AT-OM
 * @typedef {Object} ATOMMessage
 * @property {string} id - UUID unique du message
 * @property {string} type - Type de message (MESSAGE_TYPES)
 * @property {string} from - ID de l'agent emetteur
 * @property {string} to - ID de l'agent destinataire (ou 'broadcast')
 * @property {string} [topic] - Topic pour pub/sub
 * @property {string} [correlationId] - ID de correlation pour chaines
 * @property {string} [replyTo] - ID du message auquel on repond
 * @property {number} priority - Priorite (MESSAGE_PRIORITIES)
 * @property {number} timestamp - Timestamp creation
 * @property {number} [ttl] - Time-to-live en ms
 * @property {Object} payload - Contenu du message
 * @property {Object} [metadata] - Metadata additionnelles
 */

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE FACTORY
// ═══════════════════════════════════════════════════════════════════════════════

const MessageFactory = {
    /**
     * Genere un UUID v4
     */
    generateId() {
        return 'msg_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9);
    },

    /**
     * Cree un message de base
     */
    create(type, from, to, payload, options = {}) {
        return {
            id: this.generateId(),
            type: type,
            from: from,
            to: to,
            topic: options.topic || null,
            correlationId: options.correlationId || null,
            replyTo: options.replyTo || null,
            priority: options.priority ?? MESSAGE_PRIORITIES.MEDIUM,
            timestamp: Date.now(),
            ttl: options.ttl || 300000, // 5 minutes par defaut
            payload: payload,
            metadata: {
                version: 'CHE·NU™ V76',
                ...(options.metadata || {})
            }
        };
    },

    /**
     * Cree une requete
     */
    createRequest(from, to, action, params = {}) {
        return this.create(MESSAGE_TYPES.REQUEST, from, to, {
            action: action,
            params: params
        }, { priority: MESSAGE_PRIORITIES.MEDIUM });
    },

    /**
     * Cree une reponse
     */
    createResponse(from, to, replyTo, result, success = true) {
        return this.create(MESSAGE_TYPES.RESPONSE, from, to, {
            success: success,
            result: result
        }, {
            replyTo: replyTo,
            correlationId: replyTo,
            priority: MESSAGE_PRIORITIES.MEDIUM
        });
    },

    /**
     * Cree une commande (L0/L1 seulement)
     */
    createCommand(from, to, command, params = {}) {
        return this.create(MESSAGE_TYPES.COMMAND, from, to, {
            command: command,
            params: params
        }, { priority: MESSAGE_PRIORITIES.HIGH });
    },

    /**
     * Cree un accusé de reception
     */
    createAck(from, to, messageId) {
        return this.create(MESSAGE_TYPES.ACK, from, to, {
            acknowledgedId: messageId,
            receivedAt: Date.now()
        }, {
            replyTo: messageId,
            priority: MESSAGE_PRIORITIES.LOW
        });
    },

    /**
     * Cree un evenement
     */
    createEvent(from, eventName, data, topic = null) {
        return this.create(MESSAGE_TYPES.EVENT, from, 'broadcast', {
            event: eventName,
            data: data
        }, {
            topic: topic,
            priority: MESSAGE_PRIORITIES.MEDIUM
        });
    },

    /**
     * Cree une mise a jour de statut
     */
    createStatus(from, status, details = {}) {
        return this.create(MESSAGE_TYPES.STATUS, from, 'broadcast', {
            status: status,
            details: details
        }, { priority: MESSAGE_PRIORITIES.LOW });
    },

    /**
     * Cree un heartbeat
     */
    createHeartbeat(from) {
        return this.create(MESSAGE_TYPES.HEARTBEAT, from, 'system', {
            alive: true,
            uptime: performance.now()
        }, {
            priority: MESSAGE_PRIORITIES.BACKGROUND,
            ttl: 60000 // 1 minute
        });
    },

    /**
     * Cree une delegation de tache
     */
    createTaskDelegate(from, to, task, deadline = null) {
        return this.create(MESSAGE_TYPES.TASK_DELEGATE, from, to, {
            task: task,
            delegatedAt: Date.now(),
            deadline: deadline
        }, { priority: MESSAGE_PRIORITIES.HIGH });
    },

    /**
     * Cree une acceptation de tache
     */
    createTaskAccept(from, to, taskMessageId, estimatedCompletion = null) {
        return this.create(MESSAGE_TYPES.TASK_ACCEPT, from, to, {
            taskId: taskMessageId,
            acceptedAt: Date.now(),
            estimatedCompletion: estimatedCompletion
        }, {
            replyTo: taskMessageId,
            correlationId: taskMessageId,
            priority: MESSAGE_PRIORITIES.MEDIUM
        });
    },

    /**
     * Cree un refus de tache
     */
    createTaskReject(from, to, taskMessageId, reason) {
        return this.create(MESSAGE_TYPES.TASK_REJECT, from, to, {
            taskId: taskMessageId,
            rejectedAt: Date.now(),
            reason: reason
        }, {
            replyTo: taskMessageId,
            correlationId: taskMessageId,
            priority: MESSAGE_PRIORITIES.MEDIUM
        });
    },

    /**
     * Cree une completion de tache
     */
    createTaskComplete(from, to, taskMessageId, result) {
        return this.create(MESSAGE_TYPES.TASK_COMPLETE, from, to, {
            taskId: taskMessageId,
            completedAt: Date.now(),
            result: result
        }, {
            replyTo: taskMessageId,
            correlationId: taskMessageId,
            priority: MESSAGE_PRIORITIES.MEDIUM
        });
    },

    /**
     * Cree une escalade
     */
    createEscalate(from, to, originalMessage, reason) {
        return this.create(MESSAGE_TYPES.ESCALATE, from, to, {
            originalMessage: originalMessage,
            escalatedAt: Date.now(),
            reason: reason
        }, {
            correlationId: originalMessage.id,
            priority: MESSAGE_PRIORITIES.HIGH
        });
    },

    /**
     * Cree un checkpoint HITL
     */
    createCheckpoint(from, checkpointType, action, impact) {
        return this.create(MESSAGE_TYPES.CHECKPOINT, from, 'hitl_controller', {
            checkpointType: checkpointType,
            action: action,
            estimatedImpact: impact,
            requiresApproval: true,
            createdAt: Date.now()
        }, { priority: MESSAGE_PRIORITIES.CRITICAL });
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE VALIDATOR
// ═══════════════════════════════════════════════════════════════════════════════

const MessageValidator = {
    /**
     * Valide la structure d'un message
     */
    validate(message) {
        const errors = [];

        if (!message.id) errors.push('Missing id');
        if (!message.type) errors.push('Missing type');
        if (!Object.values(MESSAGE_TYPES).includes(message.type)) {
            errors.push(`Invalid type: ${message.type}`);
        }
        if (!message.from) errors.push('Missing from');
        if (!message.to) errors.push('Missing to');
        if (typeof message.timestamp !== 'number') errors.push('Invalid timestamp');
        if (!message.payload) errors.push('Missing payload');

        return {
            valid: errors.length === 0,
            errors: errors
        };
    },

    /**
     * Verifie si le message a expire (TTL)
     */
    isExpired(message) {
        if (!message.ttl) return false;
        return Date.now() > (message.timestamp + message.ttl);
    },

    /**
     * Verifie si c'est une reponse a un message
     */
    isReplyTo(message, originalId) {
        return message.replyTo === originalId || message.correlationId === originalId;
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MESSAGE_TYPES,
        MESSAGE_PRIORITIES,
        MessageFactory,
        MessageValidator
    };
}

// Global pour browser
if (typeof window !== 'undefined') {
    window.ATOM_MESSAGE_TYPES = MESSAGE_TYPES;
    window.ATOM_MESSAGE_PRIORITIES = MESSAGE_PRIORITIES;
    window.ATOMMessageFactory = MessageFactory;
    window.ATOMMessageValidator = MessageValidator;
}

console.log('%c[AT-OM] Message Types loaded - 13 types standards', 'color: #D4AF37;');
