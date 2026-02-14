/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM WebSocket Manager - CHE·NU™ V76
 * Connexion WebSocket Persistante avec Auto-Reconnexion & Sync Logging
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Features:
 * 1. Auto-Reconnection Logic (2s interval, max 10 attempts)
 * 2. Visibility Change Listener (reconnect on tab focus)
 * 3. Console Sync Logger ([SYNC] format)
 * 4. Heartbeat System (ping every 30s)
 * 5. Gratitude Mode Fallback (444Hz) on prolonged disconnection
 * 6. Low Energy Mode for weak connections
 *
 * Usage:
 *   const ws = initATOMWebSocket({
 *       onMessage: (data) => console.log(data),
 *       onConnect: () => console.log('Connected!'),
 *       onDisconnect: () => console.log('Disconnected!')
 *   });
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION - Utilise config.js si disponible, sinon valeurs par défaut
// ═══════════════════════════════════════════════════════════════════════════════

const WS_CONFIG = (typeof ATOM_CONFIG !== 'undefined') ? {
    wsUrl: ATOM_CONFIG.WS_URL,
    maxReconnectAttempts: ATOM_CONFIG.WS_MAX_RECONNECT || 10,
    reconnectInterval: ATOM_CONFIG.WS_RECONNECT_INTERVAL || 2000,
    heartbeatInterval: ATOM_CONFIG.WS_HEARTBEAT_INTERVAL || 30000
} : {
    wsUrl: 'wss://atom-2autu.ondigitalocean.app/ws',
    maxReconnectAttempts: 10,
    reconnectInterval: 2000,
    heartbeatInterval: 30000
};

// Constantes de connexion
const GRATITUDE_FREQUENCY = (typeof ATOM_CONSTANTS !== 'undefined') ? 444 : 444;
const GRATITUDE_FALLBACK_DELAY = 15000; // 15 seconds before fallback

// ═══════════════════════════════════════════════════════════════════════════════
// ATOM WEBSOCKET MANAGER CLASS
// ═══════════════════════════════════════════════════════════════════════════════

class ATOMWebSocketManager {
    constructor(config = {}) {
        // Configuration
        this.wsUrl = config.wsUrl || WS_CONFIG.wsUrl;
        this.maxReconnectAttempts = config.maxReconnectAttempts || WS_CONFIG.maxReconnectAttempts;
        this.reconnectInterval = config.reconnectInterval || WS_CONFIG.reconnectInterval;
        this.heartbeatInterval = config.heartbeatInterval || WS_CONFIG.heartbeatInterval;
        this.enableSyncLog = config.enableSyncLog !== false;

        // State
        this.ws = null;
        this.reconnectAttempts = 0;
        this.reconnectTimer = null;
        this.heartbeatTimer = null;
        this.gratitudeFallbackTimer = null;
        this.gratitudePulseInterval = null;
        this.isIntentionallyClosed = false;
        this.isGratitudeMode = false;
        this.isLowEnergyMode = false;
        this.lastMessageTime = null;
        this.lastPingTime = null;
        this.currentLatency = 0;
        this.connectionState = 'disconnected';

        // Callbacks
        this.onMessage = config.onMessage || null;
        this.onConnect = config.onConnect || null;
        this.onDisconnect = config.onDisconnect || null;
        this.onReconnecting = config.onReconnecting || null;
        this.onError = config.onError || null;
        this.onSyncUpdate = config.onSyncUpdate || null;
        this.onStatusChange = config.onStatusChange || null;

        // Stats
        this.stats = {
            messagesReceived: 0,
            reconnections: 0,
            heartbeatsSent: 0,
            lastConnectedAt: null,
            totalUptime: 0
        };

        // Latency threshold for low energy mode
        this.latencyThreshold = 2000;

        // Bind methods
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);

        // Initialize
        this._setupVisibilityListener();
        this._setupNetworkListener();

        console.log('[AT-OM WS] WebSocket Manager initialized');
        console.log(`[AT-OM WS] URL: ${this.wsUrl}`);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CONNECTION MANAGEMENT
    // ═══════════════════════════════════════════════════════════════════════════

    connect() {
        if (this.connectionState === 'connecting') {
            console.log('[AT-OM WS] Connection already in progress...');
            return;
        }

        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            console.log('[AT-OM WS] Already connected');
            return;
        }

        this.isIntentionallyClosed = false;
        this.connectionState = 'connecting';

        // Clear gratitude fallback timer
        if (this.gratitudeFallbackTimer) {
            clearTimeout(this.gratitudeFallbackTimer);
        }

        console.log(`[AT-OM WS] Connecting to ${this.wsUrl}...`);

        try {
            this.ws = new WebSocket(this.wsUrl);
            this._setupWebSocketHandlers();
        } catch (error) {
            console.error('[AT-OM WS] Failed to create WebSocket:', error);
            this.connectionState = 'disconnected';
            this._scheduleReconnect();
        }
    }

    disconnect() {
        console.log('[AT-OM WS] Intentionally disconnecting...');
        this.isIntentionallyClosed = true;
        this._clearTimers();
        this._stopGratitudePulse();

        if (this.ws) {
            this.ws.close(1000, 'Client disconnect');
            this.ws = null;
        }

        this.connectionState = 'disconnected';
        this._notifyStatusChange('disconnected');
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // WEBSOCKET EVENT HANDLERS
    // ═══════════════════════════════════════════════════════════════════════════

    _setupWebSocketHandlers() {
        this.ws.onopen = () => {
            console.log('%c[AT-OM WS] ✅ Connected!', 'color: #00FF88; font-weight: bold;');
            this.connectionState = 'connected';
            this.reconnectAttempts = 0;
            this.stats.lastConnectedAt = new Date();

            // Exit gratitude mode if active
            this._deactivateGratitudeMode();

            // Start heartbeat
            this._startHeartbeat();

            // Check network quality
            this._checkNetworkQuality();

            // Callbacks
            if (this.onConnect) this.onConnect();
            this._notifyStatusChange('connected');

            // Request initial sync
            this._requestSync();
        };

        this.ws.onmessage = (event) => {
            this.lastMessageTime = Date.now();
            this.stats.messagesReceived++;

            // Calculate latency if pong response
            if (this.lastPingTime) {
                this.currentLatency = Date.now() - this.lastPingTime;
                if (this.currentLatency > this.latencyThreshold) {
                    this._enableLowEnergyMode();
                }
            }

            try {
                const data = JSON.parse(event.data);
                this._processMessage(data);
            } catch (error) {
                console.warn('[AT-OM WS] Failed to parse message:', error);
            }
        };

        this.ws.onclose = (event) => {
            this.connectionState = 'disconnected';
            this._stopHeartbeat();

            if (this.isIntentionallyClosed) {
                console.log('[AT-OM WS] Connection closed intentionally');
                return;
            }

            console.log(`%c[AT-OM WS] ❌ Disconnected (code: ${event.code})`, 'color: #FF6B6B;');

            // Schedule gratitude fallback
            this.gratitudeFallbackTimer = setTimeout(() => {
                this._activateGratitudeMode();
            }, GRATITUDE_FALLBACK_DELAY);

            if (this.onDisconnect) this.onDisconnect(event);
            this._notifyStatusChange('disconnected');

            // Auto-reconnect
            this._scheduleReconnect();
        };

        this.ws.onerror = (error) => {
            console.error('[AT-OM WS] WebSocket error:', error);
            if (this.onError) this.onError(error);
        };
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // MESSAGE PROCESSING & SYNC LOGGING
    // ═══════════════════════════════════════════════════════════════════════════

    _processMessage(data) {
        switch (data.type) {
            case 'pong':
                console.log('[AT-OM WS] 💓 Heartbeat acknowledged');
                break;

            case 'agent_update':
            case 'frequency_change':
            case 'sync':
                this._logSyncUpdate(data);
                break;

            case 'agents_list':
                console.log(`[AT-OM WS] Received agents list: ${data.agents?.length || 0} agents`);
                break;

            case 'gratitude_pulse':
                // Local fallback pulse
                break;

            default:
                if (this.enableSyncLog && (data.id || data.agent)) {
                    this._logSyncUpdate(data);
                }
        }

        // Forward to callbacks
        if (this.onMessage) this.onMessage(data);
        if (this.onSyncUpdate && (data.id || data.agent)) this.onSyncUpdate(data);
    }

    _logSyncUpdate(data) {
        if (!this.enableSyncLog) return;

        const agent = data.agent || data;
        const id = agent.id || data.id || 'N/A';
        const name = agent.name || data.name || 'Unknown';
        const freq = agent.frequency_hz || data.frequency_hz || 0;
        const sphere = agent.sphere || data.sphere || 'Unknown';
        const status = data.status || agent.status || 'active';

        console.log(
            `%c[SYNC]%c ${name} ID: ${id} | Freq: ${freq}Hz | Sphere: ${sphere} | Status: ${status}`,
            'color: #D8B26A; font-weight: bold;',
            'color: #00FF88;'
        );
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AUTO-RECONNECTION LOGIC
    // ═══════════════════════════════════════════════════════════════════════════

    _scheduleReconnect() {
        if (this.isIntentionallyClosed) return;

        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error(`[AT-OM WS] ⛔ Max reconnection attempts (${this.maxReconnectAttempts}) reached`);
            return;
        }

        this.reconnectAttempts++;
        this.stats.reconnections++;

        const delay = this.reconnectInterval * Math.min(this.reconnectAttempts, 5);

        console.log(`[AT-OM WS] 🔄 Reconnecting in ${delay}ms (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

        if (this.onReconnecting) {
            this.onReconnecting(this.reconnectAttempts, this.maxReconnectAttempts);
        }

        this.reconnectTimer = setTimeout(() => this.connect(), delay);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // VISIBILITY CHANGE LISTENER
    // ═══════════════════════════════════════════════════════════════════════════

    _setupVisibilityListener() {
        document.addEventListener('visibilitychange', this.handleVisibilityChange);

        window.addEventListener('focus', () => {
            if (this.connectionState !== 'connected') {
                console.log('[AT-OM WS] 👁️ Window focused - checking connection...');
                this._checkAndReconnect();
            }
        });
    }

    handleVisibilityChange() {
        if (document.visibilityState === 'visible') {
            console.log('[AT-OM WS] 👁️ Tab visible - checking WebSocket...');
            this._checkAndReconnect();
        } else {
            console.log('[AT-OM WS] 😴 Tab hidden');
        }
    }

    _checkAndReconnect() {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            console.log('[AT-OM WS] Socket not open, reconnecting...');
            this.reconnectAttempts = 0;
            this.connect();
            return;
        }

        // Socket appears open, send ping to verify
        this._sendPing();

        // If no response in 5 seconds, reconnect
        setTimeout(() => {
            const timeSinceLastMessage = Date.now() - (this.lastMessageTime || 0);
            if (timeSinceLastMessage > 35000) {
                console.log('[AT-OM WS] No recent messages, forcing reconnect...');
                this.ws.close();
                this.connect();
            }
        }, 5000);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // HEARTBEAT SYSTEM
    // ═══════════════════════════════════════════════════════════════════════════

    _startHeartbeat() {
        this._stopHeartbeat();
        console.log(`[AT-OM WS] 💓 Heartbeat started (every ${this.heartbeatInterval / 1000}s)`);

        this.heartbeatTimer = setInterval(() => {
            this._sendPing();
        }, this.heartbeatInterval);
    }

    _stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }

    _sendPing() {
        if (this.isConnected()) {
            try {
                this.lastPingTime = Date.now();
                this.ws.send(JSON.stringify({ type: 'ping', timestamp: this.lastPingTime }));
                this.stats.heartbeatsSent++;
                console.log('[AT-OM WS] 💓 Ping sent');
            } catch (e) {
                console.error('[AT-OM WS] Failed to send ping:', e);
            }
        }
    }

    _requestSync() {
        if (this.isConnected()) {
            try {
                this.ws.send(JSON.stringify({ type: 'sync_request', timestamp: Date.now() }));
                console.log('[AT-OM WS] 📡 Sync request sent');
            } catch (e) {
                console.error('[AT-OM WS] Failed to send sync request:', e);
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GRATITUDE MODE - 444Hz FALLBACK
    // ═══════════════════════════════════════════════════════════════════════════

    _activateGratitudeMode() {
        if (this.isGratitudeMode) return;
        this.isGratitudeMode = true;

        console.log(`%c[AT-OM WS] 🙏 GRATITUDE MODE ACTIVATED - ${GRATITUDE_FREQUENCY}Hz Fallback`, 'color: #D8B26A; font-size: 14px; font-weight: bold;');

        this._startGratitudePulse();
        this._notifyStatusChange('gratitude');
    }

    _deactivateGratitudeMode() {
        if (!this.isGratitudeMode) return;
        this.isGratitudeMode = false;

        this._stopGratitudePulse();
        console.log('[AT-OM WS] ✅ Connection restored - Exiting Gratitude Mode');
    }

    _startGratitudePulse() {
        this.gratitudePulseInterval = setInterval(() => {
            if (this.onMessage) {
                this.onMessage({
                    type: 'gratitude_pulse',
                    frequency_hz: GRATITUDE_FREQUENCY,
                    is_fallback: true,
                    timestamp: Date.now()
                });
            }
        }, 4440); // 4.44 seconds - resonance cycle
    }

    _stopGratitudePulse() {
        if (this.gratitudePulseInterval) {
            clearInterval(this.gratitudePulseInterval);
            this.gratitudePulseInterval = null;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // LOW ENERGY MODE
    // ═══════════════════════════════════════════════════════════════════════════

    _setupNetworkListener() {
        if ('connection' in navigator) {
            navigator.connection.addEventListener('change', () => this._checkNetworkQuality());
        }
    }

    _checkNetworkQuality() {
        if ('connection' in navigator) {
            const conn = navigator.connection;
            if (conn.effectiveType === '2g' || conn.effectiveType === 'slow-2g' || conn.saveData) {
                this._enableLowEnergyMode();
            } else if (this.isLowEnergyMode && conn.effectiveType === '4g') {
                this._disableLowEnergyMode();
            }
        }
    }

    _enableLowEnergyMode() {
        if (this.isLowEnergyMode) return;
        this.isLowEnergyMode = true;
        this.heartbeatInterval = 60000; // Reduce to 60s

        console.log('%c[AT-OM WS] 🔋 Low Energy Mode ENABLED', 'color: #FFD700;');
        this._notifyStatusChange('low_energy');

        if (window.enableLowEnergyDisplay) window.enableLowEnergyDisplay();
    }

    _disableLowEnergyMode() {
        if (!this.isLowEnergyMode) return;
        this.isLowEnergyMode = false;
        this.heartbeatInterval = WS_CONFIG.heartbeatInterval;

        console.log('%c[AT-OM WS] 🔌 Normal Mode RESTORED', 'color: #00FF88;');

        if (window.disableLowEnergyDisplay) window.disableLowEnergyDisplay();
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // UTILITY METHODS
    // ═══════════════════════════════════════════════════════════════════════════

    _clearTimers() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        if (this.gratitudeFallbackTimer) {
            clearTimeout(this.gratitudeFallbackTimer);
            this.gratitudeFallbackTimer = null;
        }
        this._stopHeartbeat();
    }

    _notifyStatusChange(status) {
        if (this.onStatusChange) {
            this.onStatusChange(status);
        }
    }

    send(data) {
        if (this.isConnected()) {
            const message = typeof data === 'string' ? data : JSON.stringify(data);
            this.ws.send(message);
            return true;
        }
        console.warn('[AT-OM WS] Cannot send - not connected');
        return false;
    }

    getStatus() {
        return {
            connected: this.isConnected(),
            connectionState: this.connectionState,
            isGratitudeMode: this.isGratitudeMode,
            isLowEnergyMode: this.isLowEnergyMode,
            currentLatency: this.currentLatency,
            reconnectAttempts: this.reconnectAttempts,
            stats: this.stats
        };
    }

    destroy() {
        console.log('[AT-OM WS] Destroying WebSocket Manager...');
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        this.disconnect();
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// QUICK START FUNCTION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Initialize AT-OM WebSocket with easy configuration
 * @param {Object} config - Configuration options
 * @returns {ATOMWebSocketManager} - WebSocket manager instance
 */
function initATOMWebSocket(config = {}) {
    const wsManager = new ATOMWebSocketManager({
        wsUrl: WS_CONFIG.wsUrl,
        maxReconnectAttempts: WS_CONFIG.maxReconnectAttempts,
        reconnectInterval: WS_CONFIG.reconnectInterval,
        heartbeatInterval: WS_CONFIG.heartbeatInterval,
        enableSyncLog: true,
        ...config
    });

    // Auto-connect
    wsManager.connect();

    // Expose globally for debugging
    window.atomWS = wsManager;

    console.log('[AT-OM WS] 🚀 WebSocket Manager ready! Access via window.atomWS');

    return wsManager;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ATOMWebSocketManager, initATOMWebSocket };
}
