// ═══════════════════════════════════════════════════════════════════════════
// AT·OM API SERVICE
// External API connections: OAuth2, REST, Web3
// ═══════════════════════════════════════════════════════════════════════════

import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';
import type {
  SphereId,
  ApiConnection,
  ApiConfig,
  OAuth2Config,
  Web3Config,
  ApiAuthType,
} from '@/types';
import { OfflineService } from './offline.service';
import { EncryptionService } from './encryption.service';

// ─────────────────────────────────────────────────────────────────────────────
// API CLIENT FACTORY
// ─────────────────────────────────────────────────────────────────────────────

class ApiClientFactory {
  private clients: Map<string, AxiosInstance> = new Map();

  create(connectionId: string, config: ApiConfig): AxiosInstance {
    // Check if client already exists
    if (this.clients.has(connectionId)) {
      return this.clients.get(connectionId)!;
    }

    const client = axios.create({
      baseURL: config.baseUrl,
      timeout: config.timeout || 30000,
      headers: config.headers,
    });

    // Request interceptor
    client.interceptors.request.use(
      async (request) => {
        // Add timestamp for tracking
        request.headers['X-Request-Time'] = Date.now().toString();
        return request;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    client.interceptors.response.use(
      (response) => {
        // Log successful requests
        console.log(`[API] ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
        return response;
      },
      async (error: AxiosError) => {
        // Handle errors
        console.error(`[API] Error: ${error.message}`);
        
        // If offline, queue the request
        if (!navigator.onLine && error.config) {
          await this.queueOfflineRequest(connectionId, error.config);
        }
        
        return Promise.reject(error);
      }
    );

    this.clients.set(connectionId, client);
    return client;
  }

  private async queueOfflineRequest(connectionId: string, config: AxiosRequestConfig): Promise<void> {
    await OfflineService.saveData('technology', 'pending_api_request', {
      connectionId,
      method: config.method,
      url: config.url,
      data: config.data,
      headers: config.headers,
    });
  }

  remove(connectionId: string): void {
    this.clients.delete(connectionId);
  }

  get(connectionId: string): AxiosInstance | undefined {
    return this.clients.get(connectionId);
  }
}

export const apiClientFactory = new ApiClientFactory();

// ─────────────────────────────────────────────────────────────────────────────
// OAUTH2 SERVICE
// ─────────────────────────────────────────────────────────────────────────────

class OAuth2Service {
  private tokens: Map<string, {
    accessToken: string;
    refreshToken: string;
    expiresAt: number;
  }> = new Map();

  async initiateAuth(connectionId: string, config: OAuth2Config): Promise<string> {
    // Generate state for CSRF protection
    const state = crypto.randomUUID();
    sessionStorage.setItem(`oauth_state_${connectionId}`, state);

    // Build authorization URL
    const params = new URLSearchParams({
      client_id: config.clientId,
      redirect_uri: config.redirectUri,
      response_type: 'code',
      scope: config.scopes.join(' '),
      state,
    });

    return `${config.authUrl}?${params.toString()}`;
  }

  async handleCallback(
    connectionId: string,
    config: OAuth2Config,
    code: string,
    state: string
  ): Promise<boolean> {
    // Verify state
    const savedState = sessionStorage.getItem(`oauth_state_${connectionId}`);
    if (state !== savedState) {
      throw new Error('Invalid OAuth state');
    }
    sessionStorage.removeItem(`oauth_state_${connectionId}`);

    // Exchange code for tokens
    const response = await axios.post(config.tokenUrl, {
      grant_type: 'authorization_code',
      client_id: config.clientId,
      code,
      redirect_uri: config.redirectUri,
    });

    const { access_token, refresh_token, expires_in } = response.data;

    // Store tokens securely
    this.tokens.set(connectionId, {
      accessToken: access_token,
      refreshToken: refresh_token,
      expiresAt: Date.now() + expires_in * 1000,
    });

    // Store encrypted in local storage
    const encrypted = EncryptionService.encryptSymmetric(
      JSON.stringify({ accessToken: access_token, refreshToken: refresh_token }),
      new Uint8Array(32) // Would use actual key from identity
    );
    localStorage.setItem(`oauth_tokens_${connectionId}`, JSON.stringify(encrypted));

    return true;
  }

  async refreshTokens(connectionId: string, config: OAuth2Config): Promise<boolean> {
    const stored = this.tokens.get(connectionId);
    if (!stored?.refreshToken) return false;

    try {
      const response = await axios.post(config.tokenUrl, {
        grant_type: 'refresh_token',
        client_id: config.clientId,
        refresh_token: stored.refreshToken,
      });

      const { access_token, refresh_token, expires_in } = response.data;

      this.tokens.set(connectionId, {
        accessToken: access_token,
        refreshToken: refresh_token || stored.refreshToken,
        expiresAt: Date.now() + expires_in * 1000,
      });

      return true;
    } catch {
      this.tokens.delete(connectionId);
      return false;
    }
  }

  getAccessToken(connectionId: string): string | null {
    const stored = this.tokens.get(connectionId);
    if (!stored) return null;

    // Check if expired
    if (Date.now() >= stored.expiresAt) {
      return null; // Caller should refresh
    }

    return stored.accessToken;
  }

  isTokenExpiring(connectionId: string, bufferMs: number = 60000): boolean {
    const stored = this.tokens.get(connectionId);
    if (!stored) return true;
    return Date.now() >= stored.expiresAt - bufferMs;
  }

  revokeTokens(connectionId: string): void {
    this.tokens.delete(connectionId);
    localStorage.removeItem(`oauth_tokens_${connectionId}`);
  }
}

export const oauth2Service = new OAuth2Service();

// ─────────────────────────────────────────────────────────────────────────────
// WEB3 SERVICE
// ─────────────────────────────────────────────────────────────────────────────

class Web3Service {
  private connectedAddress: string | null = null;
  private chainId: number | null = null;

  async connect(): Promise<string | null> {
    if (typeof window.ethereum === 'undefined') {
      console.warn('[Web3] No Ethereum provider found');
      return null;
    }

    try {
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
      });

      this.connectedAddress = accounts[0];
      this.chainId = parseInt(
        await window.ethereum.request({ method: 'eth_chainId' }),
        16
      );

      // Listen for account changes
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        this.connectedAddress = accounts[0] || null;
      });

      // Listen for chain changes
      window.ethereum.on('chainChanged', (chainId: string) => {
        this.chainId = parseInt(chainId, 16);
      });

      return this.connectedAddress;
    } catch (error) {
      console.error('[Web3] Connection failed:', error);
      return null;
    }
  }

  async switchChain(config: Web3Config): Promise<boolean> {
    if (!window.ethereum) return false;

    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: `0x${config.chainId.toString(16)}` }],
      });
      return true;
    } catch (error: any) {
      // Chain doesn't exist, try to add it
      if (error.code === 4902 && config.rpcUrl) {
        try {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [
              {
                chainId: `0x${config.chainId.toString(16)}`,
                rpcUrls: [config.rpcUrl],
              },
            ],
          });
          return true;
        } catch {
          return false;
        }
      }
      return false;
    }
  }

  async signMessage(message: string): Promise<string | null> {
    if (!window.ethereum || !this.connectedAddress) return null;

    try {
      const signature = await window.ethereum.request({
        method: 'personal_sign',
        params: [message, this.connectedAddress],
      });
      return signature;
    } catch {
      return null;
    }
  }

  getConnectedAddress(): string | null {
    return this.connectedAddress;
  }

  getChainId(): number | null {
    return this.chainId;
  }

  disconnect(): void {
    this.connectedAddress = null;
    this.chainId = null;
  }
}

export const web3Service = new Web3Service();

// ─────────────────────────────────────────────────────────────────────────────
// API CONNECTION MANAGER
// ─────────────────────────────────────────────────────────────────────────────

class ApiConnectionManager {
  private connections: Map<string, ApiConnection> = new Map();

  async connect(
    sphereId: SphereId,
    name: string,
    provider: string,
    authType: ApiAuthType,
    config: ApiConfig,
    authConfig?: OAuth2Config | Web3Config
  ): Promise<ApiConnection> {
    const id = crypto.randomUUID();

    const connection: ApiConnection = {
      id,
      name,
      provider,
      sphereId,
      authType,
      status: 'pending',
      lastSync: null,
      config,
      permissions: [],
    };

    // Handle authentication based on type
    switch (authType) {
      case 'oauth2':
        if (authConfig) {
          const authUrl = await oauth2Service.initiateAuth(id, authConfig as OAuth2Config);
          // In real app, would redirect or open popup
          console.log('[API] OAuth URL:', authUrl);
        }
        break;

      case 'web3':
        const address = await web3Service.connect();
        if (address) {
          connection.status = 'connected';
        } else {
          connection.status = 'error';
        }
        break;

      case 'apikey':
      case 'jwt':
        // API key or JWT would be provided in config.headers
        connection.status = 'connected';
        break;

      case 'none':
        connection.status = 'connected';
        break;
    }

    // Create API client
    apiClientFactory.create(id, config);

    // Store connection
    this.connections.set(id, connection);

    return connection;
  }

  async disconnect(connectionId: string): Promise<void> {
    const connection = this.connections.get(connectionId);
    if (!connection) return;

    // Clean up based on auth type
    switch (connection.authType) {
      case 'oauth2':
        oauth2Service.revokeTokens(connectionId);
        break;
      case 'web3':
        web3Service.disconnect();
        break;
    }

    // Remove API client
    apiClientFactory.remove(connectionId);

    // Remove connection
    this.connections.delete(connectionId);
  }

  async request<T>(
    connectionId: string,
    method: 'get' | 'post' | 'put' | 'delete',
    endpoint: string,
    data?: unknown
  ): Promise<T> {
    const client = apiClientFactory.get(connectionId);
    if (!client) {
      throw new Error(`No client for connection ${connectionId}`);
    }

    const connection = this.connections.get(connectionId);
    if (!connection) {
      throw new Error(`Connection ${connectionId} not found`);
    }

    // Add auth headers if needed
    const headers: Record<string, string> = {};
    
    if (connection.authType === 'oauth2') {
      const token = oauth2Service.getAccessToken(connectionId);
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    const response = await client.request<T>({
      method,
      url: endpoint,
      data,
      headers,
    });

    // Update last sync
    connection.lastSync = new Date();
    this.connections.set(connectionId, connection);

    return response.data;
  }

  getConnection(connectionId: string): ApiConnection | undefined {
    return this.connections.get(connectionId);
  }

  getConnectionsBySphere(sphereId: SphereId): ApiConnection[] {
    return Array.from(this.connections.values()).filter(
      (c) => c.sphereId === sphereId
    );
  }

  getAllConnections(): ApiConnection[] {
    return Array.from(this.connections.values());
  }
}

export const apiConnectionManager = new ApiConnectionManager();

// ─────────────────────────────────────────────────────────────────────────────
// SPHERE API MAPPING
// ─────────────────────────────────────────────────────────────────────────────

export const SPHERE_API_TEMPLATES: Record<SphereId, {
  name: string;
  provider: string;
  authType: ApiAuthType;
}[]> = {
  health: [
    { name: 'Apple Health', provider: 'apple', authType: 'oauth2' },
    { name: 'Google Fit', provider: 'google', authType: 'oauth2' },
    { name: 'Withings', provider: 'withings', authType: 'oauth2' },
  ],
  finance: [
    { name: 'Plaid', provider: 'plaid', authType: 'oauth2' },
    { name: 'Stripe', provider: 'stripe', authType: 'apikey' },
    { name: 'MetaMask', provider: 'web3', authType: 'web3' },
  ],
  education: [
    { name: 'Google Classroom', provider: 'google', authType: 'oauth2' },
    { name: 'Canvas LMS', provider: 'canvas', authType: 'oauth2' },
    { name: 'Notion', provider: 'notion', authType: 'oauth2' },
  ],
  governance: [
    { name: 'DocuSign', provider: 'docusign', authType: 'oauth2' },
    { name: 'Gov.uk Verify', provider: 'govuk', authType: 'oauth2' },
  ],
  energy: [
    { name: 'Tesla', provider: 'tesla', authType: 'oauth2' },
    { name: 'Sense', provider: 'sense', authType: 'oauth2' },
  ],
  communication: [
    { name: 'Slack', provider: 'slack', authType: 'oauth2' },
    { name: 'Discord', provider: 'discord', authType: 'oauth2' },
    { name: 'Gmail', provider: 'google', authType: 'oauth2' },
  ],
  justice: [
    { name: 'LegalZoom', provider: 'legalzoom', authType: 'oauth2' },
  ],
  logistics: [
    { name: 'Google Maps', provider: 'google', authType: 'apikey' },
    { name: 'UPS', provider: 'ups', authType: 'oauth2' },
  ],
  food: [
    { name: 'MyFitnessPal', provider: 'myfitnesspal', authType: 'oauth2' },
    { name: 'Instacart', provider: 'instacart', authType: 'oauth2' },
  ],
  technology: [
    { name: 'GitHub', provider: 'github', authType: 'oauth2' },
    { name: 'AWS', provider: 'aws', authType: 'apikey' },
    { name: 'OpenAI', provider: 'openai', authType: 'apikey' },
  ],
};

// ─────────────────────────────────────────────────────────────────────────────
// EXPORTS
// ─────────────────────────────────────────────────────────────────────────────

export const ApiService = {
  // Factory
  clientFactory: apiClientFactory,
  
  // Auth services
  oauth2: oauth2Service,
  web3: web3Service,
  
  // Connection manager
  connections: apiConnectionManager,
  
  // Templates
  templates: SPHERE_API_TEMPLATES,
};

export default ApiService;

// ─────────────────────────────────────────────────────────────────────────────
// TYPE AUGMENTATION FOR ETHEREUM
// ─────────────────────────────────────────────────────────────────────────────

declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string; params?: unknown[] }) => Promise<any>;
      on: (event: string, callback: (...args: any[]) => void) => void;
      removeListener: (event: string, callback: (...args: any[]) => void) => void;
    };
  }
}
