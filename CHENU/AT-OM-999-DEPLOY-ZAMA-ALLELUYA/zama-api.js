/**
 * ZAMA-999 API Utilities - Shared across all pages
 * Includes timeout, fallback, and caching mechanisms
 */

const ZAMA_CONFIG = {
    // Use centralized ATOM_CONFIG if available — MIGRATION: ZAMA → AT-OM$
    API_BASE: (typeof ATOM_CONFIG !== 'undefined') ? ATOM_CONFIG.API_BASE : 'https://atom-2autu.ondigitalocean.app',
    WS_URL: (typeof ATOM_CONFIG !== 'undefined') ? ATOM_CONFIG.WS_URL : 'wss://atom-2autu.ondigitalocean.app/ws',
    FETCH_TIMEOUT: 5000,  // 5 seconds
    WS_TIMEOUT: 8000,     // 8 seconds
    CACHE_KEY: 'zama999_agents_cache',
    CACHE_TIME_KEY: 'zama999_cache_time',
    CACHE_MAX_AGE: 3600000  // 1 hour
};

// Fallback data if API is unreachable
const FALLBACK_AGENTS = [
    { id: 1, name: "Nova", sphere: "Intelligence", frequency_hz: 444 },
    { id: 2, name: "Atlas", sphere: "Construction", frequency_hz: 528 },
    { id: 3, name: "Harmony", sphere: "Communication", frequency_hz: 396 },
    { id: 4, name: "Phoenix", sphere: "Analytics", frequency_hz: 639 },
    { id: 5, name: "Guardian", sphere: "Security", frequency_hz: 741 },
    { id: 6, name: "Nexus", sphere: "Integration", frequency_hz: 852 },
    { id: 7, name: "Oracle", sphere: "Prediction", frequency_hz: 963 },
    { id: 8, name: "Catalyst", sphere: "Finance", frequency_hz: 417 },
    { id: 9, name: "Sentinel", sphere: "Monitoring", frequency_hz: 285 },
    { id: 10, name: "Architect", sphere: "Construction", frequency_hz: 432 },
    { id: 11, name: "Messenger", sphere: "Communication", frequency_hz: 369 },
    { id: 12, name: "Analyst", sphere: "Analytics", frequency_hz: 594 }
];

/**
 * Fetch with timeout - never blocks indefinitely
 */
async function fetchWithTimeout(url, timeout = ZAMA_CONFIG.FETCH_TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, { 
            signal: controller.signal,
            headers: {
                'Accept': 'application/json'
            }
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
}

/**
 * Get agents with automatic fallback
 * Returns: { agents: [], source: 'api'|'cache'|'fallback', error: null|string }
 */
async function getAgents() {
    let result = { agents: [], source: 'fallback', error: null };
    
    // Try API first
    try {
        const response = await fetchWithTimeout(`${ZAMA_CONFIG.API_BASE}/agents`);
        
        if (response.ok) {
            const data = await response.json();
            result.agents = Array.isArray(data) ? data : [];
            result.source = 'api';
            
            // Update cache
            saveToCache(result.agents);
            
            return result;
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        result.error = error.message;
        console.warn('API fetch failed:', error.message);
    }
    
    // Try cache
    const cached = getFromCache();
    if (cached && cached.length > 0) {
        result.agents = cached;
        result.source = 'cache';
        return result;
    }
    
    // Use fallback
    result.agents = FALLBACK_AGENTS;
    result.source = 'fallback';
    return result;
}

/**
 * Save to localStorage cache
 */
function saveToCache(agents) {
    try {
        localStorage.setItem(ZAMA_CONFIG.CACHE_KEY, JSON.stringify(agents));
        localStorage.setItem(ZAMA_CONFIG.CACHE_TIME_KEY, Date.now().toString());
    } catch (e) {
        console.warn('Cache save failed:', e);
    }
}

/**
 * Get from localStorage cache (if not expired)
 */
function getFromCache() {
    try {
        const cached = localStorage.getItem(ZAMA_CONFIG.CACHE_KEY);
        const cacheTime = localStorage.getItem(ZAMA_CONFIG.CACHE_TIME_KEY);
        
        if (cached && cacheTime) {
            const age = Date.now() - parseInt(cacheTime);
            if (age < ZAMA_CONFIG.CACHE_MAX_AGE) {
                return JSON.parse(cached);
            }
        }
    } catch (e) {
        console.warn('Cache read failed:', e);
    }
    return null;
}

/**
 * Create non-blocking WebSocket connection
 * Returns a wrapper object with status
 */
function createWebSocket(onMessage, onStatusChange) {
    const wrapper = {
        ws: null,
        status: 'connecting',
        reconnectAttempts: 0,
        maxReconnects: 5
    };
    
    function connect() {
        const timeoutId = setTimeout(() => {
            if (wrapper.status === 'connecting') {
                wrapper.status = 'timeout';
                if (onStatusChange) onStatusChange('timeout');
                console.warn('WebSocket connection timeout');
            }
        }, ZAMA_CONFIG.WS_TIMEOUT);
        
        try {
            wrapper.ws = new WebSocket(ZAMA_CONFIG.WS_URL);
            
            wrapper.ws.onopen = () => {
                clearTimeout(timeoutId);
                wrapper.status = 'connected';
                wrapper.reconnectAttempts = 0;
                if (onStatusChange) onStatusChange('connected');
            };
            
            wrapper.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    if (onMessage) onMessage(data);
                } catch (e) {
                    console.warn('WS parse error:', e);
                }
            };
            
            wrapper.ws.onclose = () => {
                clearTimeout(timeoutId);
                wrapper.status = 'disconnected';
                if (onStatusChange) onStatusChange('disconnected');
                
                // Auto-reconnect with backoff
                if (wrapper.reconnectAttempts < wrapper.maxReconnects) {
                    wrapper.reconnectAttempts++;
                    const delay = Math.min(1000 * Math.pow(2, wrapper.reconnectAttempts), 30000);
                    setTimeout(connect, delay);
                }
            };
            
            wrapper.ws.onerror = () => {
                clearTimeout(timeoutId);
                wrapper.status = 'error';
                if (onStatusChange) onStatusChange('error');
            };
            
        } catch (error) {
            clearTimeout(timeoutId);
            wrapper.status = 'error';
            if (onStatusChange) onStatusChange('error');
        }
    }
    
    // Start connection after a brief delay to not block rendering
    setTimeout(connect, 500);
    
    return wrapper;
}

/**
 * Initialize ZAMA app - call this on DOMContentLoaded
 * renderCallback receives { agents, source, error }
 */
async function initZamaApp(renderCallback, wsMessageHandler) {
    // 1. Render immediately with empty/cached data
    const cached = getFromCache();
    if (cached) {
        renderCallback({ agents: cached, source: 'cache', error: null });
    }
    
    // 2. Fetch fresh data (non-blocking)
    const result = await getAgents();
    renderCallback(result);
    
    // 3. Setup WebSocket (non-blocking)
    if (wsMessageHandler) {
        createWebSocket(wsMessageHandler, (status) => {
            console.log('WebSocket status:', status);
        });
    }
    
    return result;
}

// Export for ES modules if supported
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        ZAMA_CONFIG, 
        getAgents, 
        createWebSocket, 
        initZamaApp,
        fetchWithTimeout 
    };
}
