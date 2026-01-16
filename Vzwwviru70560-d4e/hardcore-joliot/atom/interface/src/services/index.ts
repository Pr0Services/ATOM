// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - SERVICES INDEX
// ═══════════════════════════════════════════════════════════════════════════

// Encryption Service (Split Identity)
export {
  EncryptionService,
  createSplitIdentity,
  encryptSymmetric,
  decryptSymmetric,
  encryptAsymmetric,
  decryptAsymmetric,
  signMessage,
  verifySignature,
  saveIdentitySecurely,
  loadIdentitySecurely,
  hasStoredIdentity,
  clearStoredIdentity,
} from './encryption.service';

// Offline Service (Tulum-Ready)
export {
  OfflineService,
  saveData,
  updateData,
  deleteData,
  getData,
  getDataBySphere,
  getPendingOperations,
  getPendingCount,
  syncPendingOperations,
  onSyncProgress,
  onNetworkChange,
  getOnlineStatus,
  cacheData,
  getCachedData,
  clearExpiredCache,
  getOfflineState,
  clearAllData,
  exportAllData,
  importData,
} from './offline.service';

// Real-time Services (WebSocket, Heartbeat, Arithmos)
export {
  websocketService,
  heartbeatService,
  arithmosService,
  alertService,
  initializeRealTimeServices,
  shutdownRealTimeServices,
  WebSocketService,
  HeartbeatService,
  ArithmosService,
  AlertService,
} from './realtime.service';

// API Service (OAuth2, REST, Web3)
export {
  ApiService,
  apiClientFactory,
  oauth2Service,
  web3Service,
  apiConnectionManager,
  SPHERE_API_TEMPLATES,
} from './api.service';
