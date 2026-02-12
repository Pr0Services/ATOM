/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM MESSAGE BUS - CHE·NU™ V76
 * Systeme de Communication Inter-Agents avec Routing et Pub/Sub
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Conforme au repo canonique: github.com/Pr0Services/ATOM
 * Components: AgentMailbox, MessageBus, CommunicationChannel
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// AGENT MAILBOX - Boite de reception individuelle par agent
// ═══════════════════════════════════════════════════════════════════════════════

class AgentMailbox {
    constructor(agentId) {
        this.agentId = agentId;
        this.inbox = [];
        this.outbox = [];
        this.maxSize = 1000;
        this.unreadCount = 0;
    }

    /**
     * Ajoute un message a l'inbox
     */
    receive(message) {
        if (this.inbox.length >= this.maxSize) {
            // Supprime les plus anciens messages lus
            const oldRead = this.inbox.findIndex(m => m._read);
            if (oldRead !== -1) {
                this.inbox.splice(oldRead, 1);
            } else {
                this.inbox.shift(); // Supprime le plus ancien
            }
        }

        message._receivedAt = Date.now();
        message._read = false;
        this.inbox.push(message);
        this.unreadCount++;

        // Tri par priorite
        this.inbox.sort((a, b) => (a.priority || 2) - (b.priority || 2));

        return true;
    }

    /**
     * Recupere les messages non lus
     */
    getUnread() {
        return this.inbox.filter(m => !m._read);
    }

    /**
     * Recupere tous les messages
     */
    getAll() {
        return [...this.inbox];
    }

    /**
     * Marque un message comme lu
     */
    markRead(messageId) {
        const msg = this.inbox.find(m => m.id === messageId);
        if (msg && !msg._read) {
            msg._read = true;
            msg._readAt = Date.now();
            this.unreadCount = Math.max(0, this.unreadCount - 1);
            return true;
        }
        return false;
    }

    /**
     * Marque tous comme lus
     */
    markAllRead() {
        this.inbox.forEach(m => {
            if (!m._read) {
                m._read = true;
                m._readAt = Date.now();
            }
        });
        this.unreadCount = 0;
    }

    /**
     * Ajoute a l'outbox (messages envoyes)
     */
    addToOutbox(message) {
        message._sentAt = Date.now();
        this.outbox.push(message);

        // Limite taille outbox
        if (this.outbox.length > this.maxSize) {
            this.outbox.shift();
        }
    }

    /**
     * Recupere l'historique des messages envoyes
     */
    getSent() {
        return [...this.outbox];
    }

    /**
     * Recupere les messages par correlation ID (conversation)
     */
    getConversation(correlationId) {
        const inConv = this.inbox.filter(m =>
            m.correlationId === correlationId || m.id === correlationId
        );
        const outConv = this.outbox.filter(m =>
            m.correlationId === correlationId || m.id === correlationId
        );
        return [...inConv, ...outConv].sort((a, b) => a.timestamp - b.timestamp);
    }

    /**
     * Supprime les messages expires
     */
    cleanup() {
        const now = Date.now();
        const before = this.inbox.length;

        this.inbox = this.inbox.filter(m => {
            if (!m.ttl) return true;
            return now < (m.timestamp + m.ttl);
        });

        // Recalcule unread
        this.unreadCount = this.inbox.filter(m => !m._read).length;

        return before - this.inbox.length;
    }

    /**
     * Stats de la mailbox
     */
    getStats() {
        return {
            agentId: this.agentId,
            inboxCount: this.inbox.length,
            outboxCount: this.outbox.length,
            unreadCount: this.unreadCount,
            oldestMessage: this.inbox[0]?.timestamp || null,
            newestMessage: this.inbox[this.inbox.length - 1]?.timestamp || null
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMMUNICATION CHANNEL - Canal de communication multi-participants
// ═══════════════════════════════════════════════════════════════════════════════

class CommunicationChannel {
    constructor(channelId, name, options = {}) {
        this.channelId = channelId;
        this.name = name;
        this.participants = new Set();
        this.history = [];
        this.maxHistory = options.maxHistory || 500;
        this.createdAt = Date.now();
        this.isPrivate = options.isPrivate || false;
    }

    /**
     * Ajoute un participant
     */
    join(agentId) {
        this.participants.add(agentId);
        return true;
    }

    /**
     * Retire un participant
     */
    leave(agentId) {
        return this.participants.delete(agentId);
    }

    /**
     * Verifie si un agent est participant
     */
    hasParticipant(agentId) {
        return this.participants.has(agentId);
    }

    /**
     * Poste un message dans le canal
     */
    post(message) {
        if (!this.hasParticipant(message.from)) {
            return { success: false, error: 'Not a participant' };
        }

        message._channelId = this.channelId;
        message._postedAt = Date.now();
        this.history.push(message);

        // Limite historique
        if (this.history.length > this.maxHistory) {
            this.history.shift();
        }

        return { success: true, recipients: [...this.participants] };
    }

    /**
     * Recupere l'historique
     */
    getHistory(limit = 50) {
        return this.history.slice(-limit);
    }

    /**
     * Stats du canal
     */
    getStats() {
        return {
            channelId: this.channelId,
            name: this.name,
            participantCount: this.participants.size,
            messageCount: this.history.length,
            createdAt: this.createdAt
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MESSAGE BUS - Routeur central de messages
// ═══════════════════════════════════════════════════════════════════════════════

class ATOMMessageBus {
    constructor() {
        this.mailboxes = new Map();      // agentId -> AgentMailbox
        this.channels = new Map();        // channelId -> CommunicationChannel
        this.topicSubscribers = new Map(); // topic -> Set<agentId>
        this.handlers = new Map();        // agentId -> handler function
        this.messageLog = [];             // Audit trail
        this.maxLogSize = 10000;
        this.stats = {
            messagesSent: 0,
            messagesDelivered: 0,
            messagesFailed: 0,
            broadcastsSent: 0
        };

        // Cleanup automatique toutes les 5 minutes
        this.cleanupInterval = setInterval(() => this.cleanup(), 300000);

        console.log('%c[AT-OM MessageBus] Initialized', 'color: #00FF88;');
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AGENT REGISTRATION
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Enregistre un agent dans le bus
     */
    registerAgent(agentId, handler = null) {
        if (!this.mailboxes.has(agentId)) {
            this.mailboxes.set(agentId, new AgentMailbox(agentId));
        }
        if (handler) {
            this.handlers.set(agentId, handler);
        }
        console.log(`[MessageBus] Agent registered: ${agentId}`);
        return true;
    }

    /**
     * Desenregistre un agent
     */
    unregisterAgent(agentId) {
        this.mailboxes.delete(agentId);
        this.handlers.delete(agentId);

        // Retire des topics
        this.topicSubscribers.forEach(subscribers => {
            subscribers.delete(agentId);
        });

        console.log(`[MessageBus] Agent unregistered: ${agentId}`);
        return true;
    }

    /**
     * Recupere la mailbox d'un agent
     */
    getMailbox(agentId) {
        return this.mailboxes.get(agentId);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // POINT-TO-POINT MESSAGING
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Envoie un message direct a un agent
     */
    send(message) {
        // Validation
        if (typeof ATOMMessageValidator !== 'undefined') {
            const validation = ATOMMessageValidator.validate(message);
            if (!validation.valid) {
                console.error('[MessageBus] Invalid message:', validation.errors);
                this.stats.messagesFailed++;
                return { success: false, errors: validation.errors };
            }
        }

        // Log pour audit
        this._logMessage(message);

        // Ajoute a l'outbox de l'expediteur
        const senderMailbox = this.mailboxes.get(message.from);
        if (senderMailbox) {
            senderMailbox.addToOutbox(message);
        }

        this.stats.messagesSent++;

        // Broadcast special
        if (message.to === 'broadcast') {
            return this._broadcast(message);
        }

        // Delivery directe
        return this._deliver(message);
    }

    /**
     * Livre un message a son destinataire
     */
    _deliver(message) {
        const targetMailbox = this.mailboxes.get(message.to);

        if (!targetMailbox) {
            console.warn(`[MessageBus] Agent not found: ${message.to}`);
            this.stats.messagesFailed++;
            return { success: false, error: 'Agent not found' };
        }

        // Ajoute a l'inbox
        targetMailbox.receive(message);

        // Appelle le handler si enregistre
        const handler = this.handlers.get(message.to);
        if (handler) {
            try {
                handler(message);
            } catch (err) {
                console.error(`[MessageBus] Handler error for ${message.to}:`, err);
            }
        }

        this.stats.messagesDelivered++;

        console.log(`[MessageBus] Delivered: ${message.type} from ${message.from} to ${message.to}`);
        return { success: true, deliveredAt: Date.now() };
    }

    /**
     * Broadcast a tous les agents ou a un topic
     */
    _broadcast(message) {
        let recipients = [];

        if (message.topic) {
            // Broadcast a un topic specifique
            const subscribers = this.topicSubscribers.get(message.topic);
            if (subscribers) {
                recipients = [...subscribers];
            }
        } else {
            // Broadcast a tous les agents
            recipients = [...this.mailboxes.keys()].filter(id => id !== message.from);
        }

        let delivered = 0;
        recipients.forEach(agentId => {
            const result = this._deliver({ ...message, to: agentId });
            if (result.success) delivered++;
        });

        this.stats.broadcastsSent++;

        console.log(`[MessageBus] Broadcast: ${message.type} to ${delivered}/${recipients.length} agents`);
        return { success: true, delivered, total: recipients.length };
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // PUB/SUB - Topics
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Abonne un agent a un topic
     */
    subscribe(agentId, topic) {
        if (!this.topicSubscribers.has(topic)) {
            this.topicSubscribers.set(topic, new Set());
        }
        this.topicSubscribers.get(topic).add(agentId);
        console.log(`[MessageBus] ${agentId} subscribed to topic: ${topic}`);
        return true;
    }

    /**
     * Desabonne un agent d'un topic
     */
    unsubscribe(agentId, topic) {
        const subscribers = this.topicSubscribers.get(topic);
        if (subscribers) {
            subscribers.delete(agentId);
            console.log(`[MessageBus] ${agentId} unsubscribed from topic: ${topic}`);
            return true;
        }
        return false;
    }

    /**
     * Publie un message sur un topic
     */
    publish(topic, message) {
        message.topic = topic;
        message.to = 'broadcast';
        return this.send(message);
    }

    /**
     * Liste les topics actifs
     */
    getTopics() {
        const topics = [];
        this.topicSubscribers.forEach((subscribers, topic) => {
            topics.push({
                topic,
                subscriberCount: subscribers.size
            });
        });
        return topics;
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CHANNELS
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Cree un canal de communication
     */
    createChannel(channelId, name, options = {}) {
        if (this.channels.has(channelId)) {
            return { success: false, error: 'Channel exists' };
        }
        const channel = new CommunicationChannel(channelId, name, options);
        this.channels.set(channelId, channel);
        console.log(`[MessageBus] Channel created: ${name} (${channelId})`);
        return { success: true, channel };
    }

    /**
     * Recupere un canal
     */
    getChannel(channelId) {
        return this.channels.get(channelId);
    }

    /**
     * Liste les canaux
     */
    listChannels() {
        return [...this.channels.values()].map(ch => ch.getStats());
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AUDIT & MAINTENANCE
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Log un message pour audit
     */
    _logMessage(message) {
        this.messageLog.push({
            id: message.id,
            type: message.type,
            from: message.from,
            to: message.to,
            timestamp: message.timestamp,
            priority: message.priority
        });

        // Limite taille log
        if (this.messageLog.length > this.maxLogSize) {
            this.messageLog = this.messageLog.slice(-this.maxLogSize / 2);
        }
    }

    /**
     * Recupere le log d'audit
     */
    getAuditLog(limit = 100) {
        return this.messageLog.slice(-limit);
    }

    /**
     * Nettoyage des messages expires
     */
    cleanup() {
        let totalCleaned = 0;
        this.mailboxes.forEach(mailbox => {
            totalCleaned += mailbox.cleanup();
        });
        if (totalCleaned > 0) {
            console.log(`[MessageBus] Cleaned ${totalCleaned} expired messages`);
        }
        return totalCleaned;
    }

    /**
     * Stats globales du bus
     */
    getStats() {
        return {
            ...this.stats,
            registeredAgents: this.mailboxes.size,
            activeTopics: this.topicSubscribers.size,
            activeChannels: this.channels.size,
            logSize: this.messageLog.length
        };
    }

    /**
     * Destruction propre
     */
    destroy() {
        clearInterval(this.cleanupInterval);
        this.mailboxes.clear();
        this.channels.clear();
        this.topicSubscribers.clear();
        this.handlers.clear();
        console.log('[MessageBus] Destroyed');
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ═══════════════════════════════════════════════════════════════════════════════

let messageBusInstance = null;

function getMessageBus() {
    if (!messageBusInstance) {
        messageBusInstance = new ATOMMessageBus();
    }
    return messageBusInstance;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AgentMailbox,
        CommunicationChannel,
        ATOMMessageBus,
        getMessageBus
    };
}

// Global pour browser
if (typeof window !== 'undefined') {
    window.ATOMMessageBus = ATOMMessageBus;
    window.getATOMMessageBus = getMessageBus;
}

console.log('%c[AT-OM] MessageBus loaded - Inter-agent communication ready', 'color: #D4AF37;');
