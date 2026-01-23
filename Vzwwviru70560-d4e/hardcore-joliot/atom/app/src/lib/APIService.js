/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 *
 *       █████╗ ██████╗ ██╗    ███████╗███████╗██████╗ ██╗   ██╗██╗ ██████╗███████╗
 *      ██╔══██╗██╔══██╗██║    ██╔════╝██╔════╝██╔══██╗██║   ██║██║██╔════╝██╔════╝
 *      ███████║██████╔╝██║    ███████╗█████╗  ██████╔╝██║   ██║██║██║     █████╗
 *      ██╔══██║██╔═══╝ ██║    ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║     ██╔══╝
 *      ██║  ██║██║     ██║    ███████║███████╗██║  ██║ ╚████╔╝ ██║╚██████╗███████╗
 *      ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝╚══════╝
 *
 *                              🌐 SERVICE API CENTRAL CHE·NU 🌐
 *                    Gestion centralisée des appels API avec retry et cache
 *
 *   FONCTIONNALITÉS:
 *   ├── Retry automatique avec backoff exponentiel
 *   ├── Cache intelligent avec TTL
 *   ├── Gestion des erreurs unifiée
 *   ├── Rate limiting côté client
 *   ├── Offline detection et queue
 *   └── Request/Response interceptors
 *
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const API_CONFIG = {
  baseUrl: process.env.REACT_APP_API_URL || '',
  timeout: 30000,
  retryAttempts: 3,
  retryDelay: 1000,
  cacheTTL: 5 * 60 * 1000, // 5 minutes
  rateLimitPerMinute: 60
};

// ═══════════════════════════════════════════════════════════════════════════════
// CACHE MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

class CacheManager {
  constructor() {
    this.cache = new Map();
    this.ttl = API_CONFIG.cacheTTL;
  }

  generateKey(url, options = {}) {
    return `${options.method || 'GET'}_${url}_${JSON.stringify(options.body || {})}`;
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  set(key, data, customTTL = null) {
    this.cache.set(key, {
      data,
      expiry: Date.now() + (customTTL || this.ttl)
    });
  }

  invalidate(pattern) {
    if (typeof pattern === 'string') {
      // Supprimer les entrées qui matchent le pattern
      for (const key of this.cache.keys()) {
        if (key.includes(pattern)) {
          this.cache.delete(key);
        }
      }
    } else {
      this.cache.clear();
    }
  }

  clear() {
    this.cache.clear();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// RATE LIMITER
// ═══════════════════════════════════════════════════════════════════════════════

class RateLimiter {
  constructor(requestsPerMinute = API_CONFIG.rateLimitPerMinute) {
    this.requests = [];
    this.limit = requestsPerMinute;
    this.window = 60000; // 1 minute
  }

  canMakeRequest() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.window);
    return this.requests.length < this.limit;
  }

  recordRequest() {
    this.requests.push(Date.now());
  }

  getWaitTime() {
    if (this.canMakeRequest()) return 0;
    const oldestRequest = this.requests[0];
    return this.window - (Date.now() - oldestRequest);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// OFFLINE QUEUE
// ═══════════════════════════════════════════════════════════════════════════════

class OfflineQueue {
  constructor() {
    this.queue = [];
    this.isOnline = navigator.onLine;

    window.addEventListener('online', () => {
      this.isOnline = true;
      this.processQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  add(request) {
    this.queue.push({
      ...request,
      queuedAt: Date.now()
    });

    // Sauvegarder dans localStorage pour persistance
    this.saveToStorage();
  }

  async processQueue() {
    if (!this.isOnline || this.queue.length === 0) return;

    const processedRequests = [];

    for (const request of this.queue) {
      try {
        await fetch(request.url, request.options);
        processedRequests.push(request);
      } catch (error) {
        console.error('[OfflineQueue] Failed to process:', error);
      }
    }

    // Retirer les requêtes traitées
    this.queue = this.queue.filter(r => !processedRequests.includes(r));
    this.saveToStorage();
  }

  saveToStorage() {
    try {
      localStorage.setItem('chenu_offline_queue', JSON.stringify(this.queue));
    } catch (e) {
      console.warn('[OfflineQueue] Failed to save:', e);
    }
  }

  loadFromStorage() {
    try {
      const stored = localStorage.getItem('chenu_offline_queue');
      if (stored) {
        this.queue = JSON.parse(stored);
      }
    } catch (e) {
      console.warn('[OfflineQueue] Failed to load:', e);
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ERROR TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export class APIError extends Error {
  constructor(message, statusCode, response = null) {
    super(message);
    this.name = 'APIError';
    this.statusCode = statusCode;
    this.response = response;
    this.timestamp = new Date().toISOString();
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      statusCode: this.statusCode,
      timestamp: this.timestamp
    };
  }
}

export class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
    this.timestamp = new Date().toISOString();
  }
}

export class ValidationError extends Error {
  constructor(message, fields = {}) {
    super(message);
    this.name = 'ValidationError';
    this.fields = fields;
    this.timestamp = new Date().toISOString();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVICE API PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════════

class APIService {
  constructor() {
    this.baseUrl = API_CONFIG.baseUrl;
    this.cache = new CacheManager();
    this.rateLimiter = new RateLimiter();
    this.offlineQueue = new OfflineQueue();
    this.interceptors = {
      request: [],
      response: []
    };

    // Charger la queue offline au démarrage
    this.offlineQueue.loadFromStorage();
  }

  // Ajouter un intercepteur
  addInterceptor(type, fn) {
    if (this.interceptors[type]) {
      this.interceptors[type].push(fn);
    }
  }

  // Exécuter les intercepteurs
  async runInterceptors(type, data) {
    let result = data;
    for (const interceptor of this.interceptors[type]) {
      result = await interceptor(result);
    }
    return result;
  }

  // Attendre avec backoff exponentiel
  async wait(attempt) {
    const delay = API_CONFIG.retryDelay * Math.pow(2, attempt);
    return new Promise(resolve => setTimeout(resolve, delay));
  }

  // Requête principale avec retry
  async request(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${this.baseUrl}${url}`;

    // Vérifier le rate limit
    if (!this.rateLimiter.canMakeRequest()) {
      const waitTime = this.rateLimiter.getWaitTime();
      console.warn(`[API] Rate limited. Waiting ${waitTime}ms`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }

    // Vérifier le cache pour GET
    if (options.method === 'GET' || !options.method) {
      const cacheKey = this.cache.generateKey(fullUrl, options);
      const cached = this.cache.get(cacheKey);
      if (cached && !options.skipCache) {
        console.log('[API] Cache hit:', fullUrl);
        return cached;
      }
    }

    // Préparer les options
    const requestOptions = await this.runInterceptors('request', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    // Vérifier si en ligne
    if (!navigator.onLine && options.queueOffline) {
      this.offlineQueue.add({ url: fullUrl, options: requestOptions });
      throw new NetworkError('Hors ligne. La requête sera envoyée quand la connexion sera rétablie.');
    }

    // Effectuer la requête avec retry
    let lastError;

    for (let attempt = 0; attempt < API_CONFIG.retryAttempts; attempt++) {
      try {
        this.rateLimiter.recordRequest();

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

        const response = await fetch(fullUrl, {
          ...requestOptions,
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new APIError(
            errorData.message || `HTTP ${response.status}`,
            response.status,
            errorData
          );
        }

        const data = await response.json();
        const result = await this.runInterceptors('response', data);

        // Mettre en cache les GET réussis
        if (requestOptions.method === 'GET' || !requestOptions.method) {
          const cacheKey = this.cache.generateKey(fullUrl, options);
          this.cache.set(cacheKey, result);
        }

        return result;

      } catch (error) {
        lastError = error;

        if (error.name === 'AbortError') {
          lastError = new NetworkError('La requête a expiré');
        }

        // Ne pas retry pour certaines erreurs
        if (error instanceof ValidationError ||
            (error instanceof APIError && error.statusCode >= 400 && error.statusCode < 500)) {
          throw error;
        }

        if (attempt < API_CONFIG.retryAttempts - 1) {
          console.warn(`[API] Retry ${attempt + 1}/${API_CONFIG.retryAttempts}:`, fullUrl);
          await this.wait(attempt);
        }
      }
    }

    throw lastError;
  }

  // Méthodes helper
  async get(url, options = {}) {
    return this.request(url, { ...options, method: 'GET' });
  }

  async post(url, data, options = {}) {
    return this.request(url, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async put(url, data, options = {}) {
    return this.request(url, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async patch(url, data, options = {}) {
    return this.request(url, {
      ...options,
      method: 'PATCH',
      body: JSON.stringify(data)
    });
  }

  async delete(url, options = {}) {
    return this.request(url, { ...options, method: 'DELETE' });
  }

  // Invalider le cache
  invalidateCache(pattern) {
    this.cache.invalidate(pattern);
  }

  // Vider tout le cache
  clearCache() {
    this.cache.clear();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVICE LLM POUR AGENTS
// ═══════════════════════════════════════════════════════════════════════════════

export class LLMService {
  constructor(apiService) {
    this.api = apiService;
    this.endpoint = process.env.REACT_APP_LLM_ENDPOINT || '/api/llm';
    this.model = process.env.REACT_APP_LLM_MODEL || 'claude-3-sonnet';
    this.maxTokens = 2000;
  }

  async generateResponse(prompt, options = {}) {
    try {
      const response = await this.api.post(this.endpoint, {
        model: options.model || this.model,
        messages: [
          { role: 'system', content: prompt.system || '' },
          { role: 'user', content: prompt.user || prompt }
        ],
        max_tokens: options.maxTokens || this.maxTokens,
        temperature: options.temperature || 0.7,
        stream: options.stream || false
      });

      return {
        success: true,
        content: response.choices?.[0]?.message?.content || response.content,
        usage: response.usage,
        model: response.model
      };

    } catch (error) {
      console.error('[LLM] Error:', error);

      // Fallback local si l'API échoue
      if (options.fallbackEnabled !== false) {
        return this.localFallback(prompt, options);
      }

      return {
        success: false,
        error: error.message,
        fallback: false
      };
    }
  }

  // Fallback local intelligent basé sur les templates
  localFallback(prompt, options = {}) {
    const agentName = options.agentName || 'Agent';
    const specialty = options.specialty || 'assistance';

    const responses = {
      greeting: `Bonjour ! Je suis ${agentName}, spécialisé en ${specialty}. Comment puis-je vous aider aujourd'hui ?`,
      help: `En tant que ${agentName}, je peux vous assister dans les domaines suivants : ${specialty}. N'hésitez pas à me poser vos questions.`,
      error: `Je comprends votre demande. Permettez-moi de vous aider avec cela.`,
      default: `[${agentName}] Je traite votre demande concernant "${typeof prompt === 'string' ? prompt.slice(0, 50) : 'votre question'}..."`
    };

    const userMessage = typeof prompt === 'string' ? prompt.toLowerCase() : prompt.user?.toLowerCase() || '';

    let response = responses.default;
    if (userMessage.includes('bonjour') || userMessage.includes('salut')) {
      response = responses.greeting;
    } else if (userMessage.includes('aide') || userMessage.includes('help')) {
      response = responses.help;
    }

    return {
      success: true,
      content: response,
      fallback: true,
      model: 'local-fallback'
    };
  }

  // Streaming response (pour les réponses longues)
  async *streamResponse(prompt, options = {}) {
    try {
      const response = await fetch(`${this.api.baseUrl}${this.endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: options.model || this.model,
          messages: [
            { role: 'system', content: prompt.system || '' },
            { role: 'user', content: prompt.user || prompt }
          ],
          max_tokens: options.maxTokens || this.maxTokens,
          stream: true
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.startsWith('data: '));

        for (const line of lines) {
          const data = line.slice(6);
          if (data === '[DONE]') return;

          try {
            const parsed = JSON.parse(data);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) yield content;
          } catch (e) {
            // Ignorer les erreurs de parsing
          }
        }
      }
    } catch (error) {
      console.error('[LLM Stream] Error:', error);
      yield this.localFallback(prompt, options).content;
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SERVICE ANALYTICS
// ═══════════════════════════════════════════════════════════════════════════════

export class AnalyticsService {
  constructor(apiService) {
    this.api = apiService;
    this.endpoint = '/api/analytics';
    this.queue = [];
    this.flushInterval = 10000; // 10 secondes

    // Flush automatique
    setInterval(() => this.flush(), this.flushInterval);

    // Flush avant de quitter la page
    window.addEventListener('beforeunload', () => this.flush());
  }

  track(event, properties = {}) {
    this.queue.push({
      event,
      properties: {
        ...properties,
        timestamp: new Date().toISOString(),
        sessionId: this.getSessionId(),
        url: window.location.pathname
      }
    });

    // Flush si la queue est grande
    if (this.queue.length >= 10) {
      this.flush();
    }
  }

  getSessionId() {
    let sessionId = sessionStorage.getItem('chenu_session_id');
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2)}`;
      sessionStorage.setItem('chenu_session_id', sessionId);
    }
    return sessionId;
  }

  async flush() {
    if (this.queue.length === 0) return;

    const events = [...this.queue];
    this.queue = [];

    try {
      await this.api.post(this.endpoint, { events }, { skipCache: true });
    } catch (error) {
      // Remettre dans la queue en cas d'erreur
      this.queue = [...events, ...this.queue];
      console.warn('[Analytics] Failed to flush:', error);
    }
  }

  // Events prédéfinis
  pageView(pageName) {
    this.track('page_view', { page: pageName });
  }

  agentInteraction(agentId, action, metadata = {}) {
    this.track('agent_interaction', { agentId, action, ...metadata });
  }

  xrEnvironmentLoad(envId, loadTime) {
    this.track('xr_environment_load', { envId, loadTime });
  }

  userAction(action, target, value = null) {
    this.track('user_action', { action, target, value });
  }

  error(errorType, message, stack = null) {
    this.track('error', { errorType, message, stack });
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCES
// ═══════════════════════════════════════════════════════════════════════════════

const apiService = new APIService();
const llmService = new LLMService(apiService);
const analyticsService = new AnalyticsService(apiService);

// Ajouter intercepteur d'authentification
apiService.addInterceptor('request', async (options) => {
  const token = localStorage.getItem('chenu_auth_token');
  if (token) {
    options.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    };
  }
  return options;
});

// Ajouter intercepteur de logging
apiService.addInterceptor('response', async (data) => {
  console.log('[API Response]', data);
  return data;
});

export { apiService, llmService, analyticsService };
export default apiService;
