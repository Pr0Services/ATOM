// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - TYPE DEFINITIONS
// Sovereign Identity & Productivity Platform
// ═══════════════════════════════════════════════════════════════════════════

// ─────────────────────────────────────────────────────────────────────────────
// SPHERE TYPES - The 10 Pillars of Civilization
// ─────────────────────────────────────────────────────────────────────────────

export type SphereId = 
  | 'health'
  | 'finance'
  | 'education'
  | 'governance'
  | 'energy'
  | 'communication'
  | 'justice'
  | 'logistics'
  | 'food'
  | 'technology';

export interface Sphere {
  id: SphereId;
  name: string;
  description: string;
  icon: string;
  color: string;
  stability: number;       // 0-100
  efficiency: number;      // 0-100
  lastSync: Date | null;
  isActive: boolean;
  apiConnections: ApiConnection[];
  metrics: SphereMetrics;
}

export interface SphereMetrics {
  totalItems: number;
  activeItems: number;
  pendingActions: number;
  healthScore: number;
  trendDirection: 'up' | 'down' | 'stable';
  lastUpdate: Date;
}

export interface SphereConfig {
  id: SphereId;
  name: string;
  icon: string;
  color: string;
  defaultApis: string[];
  requiredPermissions: string[];
}

// ─────────────────────────────────────────────────────────────────────────────
// API CONNECTION TYPES
// ─────────────────────────────────────────────────────────────────────────────

export type ApiAuthType = 'oauth2' | 'apikey' | 'jwt' | 'web3' | 'none';

export interface ApiConnection {
  id: string;
  name: string;
  provider: string;
  sphereId: SphereId;
  authType: ApiAuthType;
  status: 'connected' | 'disconnected' | 'error' | 'pending';
  lastSync: Date | null;
  config: ApiConfig;
  permissions: string[];
}

export interface ApiConfig {
  baseUrl: string;
  endpoints: Record<string, string>;
  headers?: Record<string, string>;
  rateLimit?: number;
  timeout?: number;
  retryCount?: number;
}

export interface OAuth2Config {
  clientId: string;
  authUrl: string;
  tokenUrl: string;
  scopes: string[];
  redirectUri: string;
}

export interface Web3Config {
  chainId: number;
  contractAddress?: string;
  rpcUrl?: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// IDENTITY TYPES - Split Identity (Sovereign Data)
// ─────────────────────────────────────────────────────────────────────────────

export interface SplitIdentity {
  publicId: string;              // Shareable identifier
  privateKey: Uint8Array;        // Never leaves device
  publicKey: Uint8Array;         // For encryption
  createdAt: Date;
  lastAccess: Date;
  recoverySetup: boolean;
}

export interface IdentityFragment {
  id: string;
  type: 'public' | 'private' | 'shared';
  sphereId: SphereId | null;
  encryptedData: string;
  metadata: FragmentMetadata;
  accessLog: AccessLogEntry[];
}

export interface FragmentMetadata {
  createdAt: Date;
  modifiedAt: Date;
  expiresAt?: Date;
  shareCount: number;
  accessCount: number;
}

export interface AccessLogEntry {
  timestamp: Date;
  action: 'read' | 'write' | 'share' | 'revoke';
  source: string;
  success: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// HEARTBEAT SERVICE TYPES (4.44s Cycle)
// ─────────────────────────────────────────────────────────────────────────────

export interface HeartbeatState {
  isConnected: boolean;
  lastBeat: Date | null;
  cycleNumber: number;
  systemStability: number;
  systemEfficiency: number;
  sphereStatus: Record<SphereId, SphereHeartbeat>;
}

export interface SphereHeartbeat {
  sphereId: SphereId;
  stability: number;
  efficiency: number;
  pendingSync: number;
  errors: number;
  lastUpdate: Date;
}

export interface HeartbeatPayload {
  timestamp: number;
  cycle: number;
  stability: number;
  efficiency: number;
  spheres: SphereHeartbeat[];
  alerts: SystemAlert[];
}

// ─────────────────────────────────────────────────────────────────────────────
// ARITHMOS ENGINE TYPES (Balance Calculation)
// ─────────────────────────────────────────────────────────────────────────────

export interface ArithmosState {
  globalBalance: number;          // 0-100
  sphereBalances: Record<SphereId, number>;
  harmonicIndex: number;
  lastCalculation: Date;
  recommendations: ArithmosRecommendation[];
}

export interface ArithmosRecommendation {
  id: string;
  priority: 'high' | 'medium' | 'low';
  sphereId: SphereId;
  action: string;
  impact: number;
  estimatedTime: string;
}

export interface BalanceMetrics {
  current: number;
  trend: number[];
  forecast: number;
  factors: BalanceFactor[];
}

export interface BalanceFactor {
  name: string;
  weight: number;
  currentValue: number;
  optimalValue: number;
  impact: 'positive' | 'negative' | 'neutral';
}

// ─────────────────────────────────────────────────────────────────────────────
// OFFLINE SYNC TYPES (Tulum-Ready)
// ─────────────────────────────────────────────────────────────────────────────

export interface OfflineState {
  isOnline: boolean;
  lastOnline: Date | null;
  pendingOperations: PendingOperation[];
  cachedData: CachedDataInfo;
  syncProgress: number;
}

export interface PendingOperation {
  id: string;
  type: 'create' | 'update' | 'delete' | 'sync';
  sphereId: SphereId;
  payload: unknown;
  createdAt: Date;
  retryCount: number;
  priority: number;
}

export interface CachedDataInfo {
  totalSize: number;
  itemCount: number;
  oldestItem: Date | null;
  newestItem: Date | null;
  sphereBreakdown: Record<SphereId, number>;
}

export interface SyncResult {
  success: boolean;
  synced: number;
  failed: number;
  errors: SyncError[];
  duration: number;
}

export interface SyncError {
  operationId: string;
  error: string;
  recoverable: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// UI STATE TYPES
// ─────────────────────────────────────────────────────────────────────────────

export interface UIState {
  theme: 'light' | 'dark' | 'system';
  sidebarOpen: boolean;
  activeSphere: SphereId | null;
  modalStack: ModalConfig[];
  notifications: Notification[];
  commandPaletteOpen: boolean;
}

export interface ModalConfig {
  id: string;
  type: string;
  title: string;
  data?: unknown;
  closable: boolean;
}

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  action?: NotificationAction;
}

export interface NotificationAction {
  label: string;
  handler: () => void;
}

// ─────────────────────────────────────────────────────────────────────────────
// SYSTEM TYPES
// ─────────────────────────────────────────────────────────────────────────────

export interface SystemAlert {
  id: string;
  level: 'critical' | 'warning' | 'info';
  source: string;
  message: string;
  timestamp: Date;
  acknowledged: boolean;
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'critical';
  uptime: number;
  latency: number;
  lastCheck: Date;
  services: ServiceHealth[];
}

export interface ServiceHealth {
  name: string;
  status: 'up' | 'down' | 'degraded';
  latency: number;
  lastError?: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// WEBSOCKET TYPES
// ─────────────────────────────────────────────────────────────────────────────

export type WebSocketEventType = 
  | 'heartbeat'
  | 'sphere_update'
  | 'balance_change'
  | 'sync_complete'
  | 'alert'
  | 'notification';

export interface WebSocketMessage<T = unknown> {
  type: WebSocketEventType;
  payload: T;
  timestamp: number;
  id: string;
}

export interface WebSocketState {
  connected: boolean;
  reconnecting: boolean;
  reconnectAttempts: number;
  lastMessage: Date | null;
}

// ─────────────────────────────────────────────────────────────────────────────
// ENCRYPTION TYPES
// ─────────────────────────────────────────────────────────────────────────────

export interface EncryptedPayload {
  nonce: string;
  ciphertext: string;
  timestamp: number;
}

export interface KeyPair {
  publicKey: Uint8Array;
  secretKey: Uint8Array;
}

export interface EncryptionConfig {
  algorithm: 'nacl' | 'aes-gcm';
  keyDerivation: 'pbkdf2' | 'argon2';
  iterations: number;
}

// ─────────────────────────────────────────────────────────────────────────────
// STORE TYPES
// ─────────────────────────────────────────────────────────────────────────────

export interface AppState {
  // Identity
  identity: SplitIdentity | null;
  isAuthenticated: boolean;
  
  // Spheres
  spheres: Record<SphereId, Sphere>;
  activeSphere: SphereId | null;
  
  // Services
  heartbeat: HeartbeatState;
  arithmos: ArithmosState;
  offline: OfflineState;
  websocket: WebSocketState;
  
  // UI
  ui: UIState;
  
  // System
  health: SystemHealth | null;
  alerts: SystemAlert[];
}

// ─────────────────────────────────────────────────────────────────────────────
// ACTION TYPES
// ─────────────────────────────────────────────────────────────────────────────

export type AppAction =
  | { type: 'SET_IDENTITY'; payload: SplitIdentity }
  | { type: 'CLEAR_IDENTITY' }
  | { type: 'UPDATE_SPHERE'; payload: { id: SphereId; data: Partial<Sphere> } }
  | { type: 'SET_ACTIVE_SPHERE'; payload: SphereId | null }
  | { type: 'HEARTBEAT_RECEIVED'; payload: HeartbeatPayload }
  | { type: 'BALANCE_UPDATED'; payload: ArithmosState }
  | { type: 'SYNC_COMPLETE'; payload: SyncResult }
  | { type: 'WEBSOCKET_CONNECTED' }
  | { type: 'WEBSOCKET_DISCONNECTED' }
  | { type: 'ADD_NOTIFICATION'; payload: Notification }
  | { type: 'DISMISS_NOTIFICATION'; payload: string }
  | { type: 'ADD_ALERT'; payload: SystemAlert }
  | { type: 'ACKNOWLEDGE_ALERT'; payload: string };

// ─────────────────────────────────────────────────────────────────────────────
// UTILITY TYPES
// ─────────────────────────────────────────────────────────────────────────────

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type AsyncStatus = 'idle' | 'loading' | 'success' | 'error';

export interface AsyncState<T> {
  status: AsyncStatus;
  data: T | null;
  error: string | null;
}
