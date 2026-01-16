// ═══════════════════════════════════════════════════════════════════════════
// AT·OM OFFLINE SERVICE
// Tulum-Ready: Full offline capability with deferred sync
// ═══════════════════════════════════════════════════════════════════════════

import { openDB, DBSchema, IDBPDatabase } from 'idb';
import { v4 as uuidv4 } from 'uuid';
import type {
  SphereId,
  PendingOperation,
  CachedDataInfo,
  SyncResult,
  SyncError,
  OfflineState,
} from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// DATABASE SCHEMA
// ─────────────────────────────────────────────────────────────────────────────

interface AtomDB extends DBSchema {
  sphereData: {
    key: string;
    value: {
      id: string;
      sphereId: SphereId;
      type: string;
      data: unknown;
      createdAt: Date;
      updatedAt: Date;
      synced: boolean;
    };
    indexes: {
      'by-sphere': SphereId;
      'by-synced': number;
      'by-type': string;
    };
  };
  pendingOperations: {
    key: string;
    value: PendingOperation;
    indexes: {
      'by-sphere': SphereId;
      'by-priority': number;
      'by-created': Date;
    };
  };
  syncLog: {
    key: string;
    value: {
      id: string;
      timestamp: Date;
      operation: string;
      status: 'success' | 'failed';
      details: string;
    };
    indexes: {
      'by-timestamp': Date;
    };
  };
  cache: {
    key: string;
    value: {
      key: string;
      data: unknown;
      expiresAt: Date;
      sphereId: SphereId | null;
    };
    indexes: {
      'by-expires': Date;
      'by-sphere': SphereId;
    };
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// DATABASE INITIALIZATION
// ─────────────────────────────────────────────────────────────────────────────

const DB_NAME = 'atom-offline-db';
const DB_VERSION = 1;

let db: IDBPDatabase<AtomDB> | null = null;

async function getDB(): Promise<IDBPDatabase<AtomDB>> {
  if (db) return db;
  
  db = await openDB<AtomDB>(DB_NAME, DB_VERSION, {
    upgrade(database) {
      // Sphere data store
      if (!database.objectStoreNames.contains('sphereData')) {
        const sphereStore = database.createObjectStore('sphereData', { keyPath: 'id' });
        sphereStore.createIndex('by-sphere', 'sphereId');
        sphereStore.createIndex('by-synced', 'synced');
        sphereStore.createIndex('by-type', 'type');
      }
      
      // Pending operations store
      if (!database.objectStoreNames.contains('pendingOperations')) {
        const opsStore = database.createObjectStore('pendingOperations', { keyPath: 'id' });
        opsStore.createIndex('by-sphere', 'sphereId');
        opsStore.createIndex('by-priority', 'priority');
        opsStore.createIndex('by-created', 'createdAt');
      }
      
      // Sync log store
      if (!database.objectStoreNames.contains('syncLog')) {
        const logStore = database.createObjectStore('syncLog', { keyPath: 'id' });
        logStore.createIndex('by-timestamp', 'timestamp');
      }
      
      // Cache store
      if (!database.objectStoreNames.contains('cache')) {
        const cacheStore = database.createObjectStore('cache', { keyPath: 'key' });
        cacheStore.createIndex('by-expires', 'expiresAt');
        cacheStore.createIndex('by-sphere', 'sphereId');
      }
    },
  });
  
  return db;
}

// ─────────────────────────────────────────────────────────────────────────────
// OFFLINE STATE MANAGEMENT
// ─────────────────────────────────────────────────────────────────────────────

let isOnline = navigator.onLine;
const onlineListeners: ((online: boolean) => void)[] = [];

// Listen for network changes
window.addEventListener('online', () => {
  isOnline = true;
  onlineListeners.forEach(listener => listener(true));
  // Trigger sync when coming back online
  syncPendingOperations();
});

window.addEventListener('offline', () => {
  isOnline = false;
  onlineListeners.forEach(listener => listener(false));
});

export function onNetworkChange(listener: (online: boolean) => void): () => void {
  onlineListeners.push(listener);
  return () => {
    const index = onlineListeners.indexOf(listener);
    if (index > -1) onlineListeners.splice(index, 1);
  };
}

export function getOnlineStatus(): boolean {
  return isOnline;
}

// ─────────────────────────────────────────────────────────────────────────────
// DATA OPERATIONS
// ─────────────────────────────────────────────────────────────────────────────

export async function saveData<T>(
  sphereId: SphereId,
  type: string,
  data: T,
  id?: string
): Promise<string> {
  const database = await getDB();
  const itemId = id || uuidv4();
  const now = new Date();
  
  await database.put('sphereData', {
    id: itemId,
    sphereId,
    type,
    data,
    createdAt: now,
    updatedAt: now,
    synced: false,
  });
  
  // Queue sync operation
  await queueOperation('create', sphereId, { id: itemId, type, data });
  
  return itemId;
}

export async function updateData<T>(
  id: string,
  sphereId: SphereId,
  data: Partial<T>
): Promise<void> {
  const database = await getDB();
  const existing = await database.get('sphereData', id);
  
  if (!existing) {
    throw new Error(`Item ${id} not found`);
  }
  
  await database.put('sphereData', {
    ...existing,
    data: { ...existing.data as object, ...data },
    updatedAt: new Date(),
    synced: false,
  });
  
  // Queue sync operation
  await queueOperation('update', sphereId, { id, data });
}

export async function deleteData(id: string, sphereId: SphereId): Promise<void> {
  const database = await getDB();
  await database.delete('sphereData', id);
  
  // Queue sync operation
  await queueOperation('delete', sphereId, { id });
}

export async function getData<T>(id: string): Promise<T | null> {
  const database = await getDB();
  const item = await database.get('sphereData', id);
  return item?.data as T ?? null;
}

export async function getDataBySphere<T>(
  sphereId: SphereId,
  type?: string
): Promise<Array<{ id: string; data: T }>> {
  const database = await getDB();
  const items = await database.getAllFromIndex('sphereData', 'by-sphere', sphereId);
  
  return items
    .filter(item => !type || item.type === type)
    .map(item => ({ id: item.id, data: item.data as T }));
}

// ─────────────────────────────────────────────────────────────────────────────
// PENDING OPERATIONS QUEUE
// ─────────────────────────────────────────────────────────────────────────────

async function queueOperation(
  type: PendingOperation['type'],
  sphereId: SphereId,
  payload: unknown,
  priority: number = 5
): Promise<void> {
  const database = await getDB();
  
  const operation: PendingOperation = {
    id: uuidv4(),
    type,
    sphereId,
    payload,
    createdAt: new Date(),
    retryCount: 0,
    priority,
  };
  
  await database.add('pendingOperations', operation);
}

export async function getPendingOperations(): Promise<PendingOperation[]> {
  const database = await getDB();
  return database.getAllFromIndex('pendingOperations', 'by-priority');
}

export async function getPendingCount(): Promise<number> {
  const database = await getDB();
  return database.count('pendingOperations');
}

// ─────────────────────────────────────────────────────────────────────────────
// SYNC ENGINE
// ─────────────────────────────────────────────────────────────────────────────

let isSyncing = false;
const syncListeners: ((progress: number) => void)[] = [];

export function onSyncProgress(listener: (progress: number) => void): () => void {
  syncListeners.push(listener);
  return () => {
    const index = syncListeners.indexOf(listener);
    if (index > -1) syncListeners.splice(index, 1);
  };
}

export async function syncPendingOperations(): Promise<SyncResult> {
  if (!isOnline || isSyncing) {
    return {
      success: false,
      synced: 0,
      failed: 0,
      errors: [],
      duration: 0,
    };
  }
  
  isSyncing = true;
  const startTime = Date.now();
  const database = await getDB();
  const operations = await getPendingOperations();
  
  let synced = 0;
  let failed = 0;
  const errors: SyncError[] = [];
  
  for (let i = 0; i < operations.length; i++) {
    const op = operations[i];
    const progress = ((i + 1) / operations.length) * 100;
    syncListeners.forEach(listener => listener(progress));
    
    try {
      await processSyncOperation(op);
      await database.delete('pendingOperations', op.id);
      synced++;
      
      // Log success
      await database.add('syncLog', {
        id: uuidv4(),
        timestamp: new Date(),
        operation: `${op.type}:${op.sphereId}`,
        status: 'success',
        details: JSON.stringify(op.payload),
      });
    } catch (error) {
      failed++;
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      
      errors.push({
        operationId: op.id,
        error: errorMessage,
        recoverable: op.retryCount < 3,
      });
      
      // Update retry count
      if (op.retryCount < 3) {
        await database.put('pendingOperations', {
          ...op,
          retryCount: op.retryCount + 1,
        });
      }
      
      // Log failure
      await database.add('syncLog', {
        id: uuidv4(),
        timestamp: new Date(),
        operation: `${op.type}:${op.sphereId}`,
        status: 'failed',
        details: errorMessage,
      });
    }
  }
  
  isSyncing = false;
  syncListeners.forEach(listener => listener(100));
  
  // Mark all synced data
  const unsyncedData = await database.getAllFromIndex('sphereData', 'by-synced', 0);
  for (const item of unsyncedData) {
    await database.put('sphereData', { ...item, synced: true });
  }
  
  return {
    success: failed === 0,
    synced,
    failed,
    errors,
    duration: Date.now() - startTime,
  };
}

async function processSyncOperation(op: PendingOperation): Promise<void> {
  // This would connect to your actual API
  // For now, simulate network request
  const apiUrl = `/api/spheres/${op.sphereId}/${op.type}`;
  
  const response = await fetch(apiUrl, {
    method: op.type === 'delete' ? 'DELETE' : op.type === 'create' ? 'POST' : 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(op.payload),
  });
  
  if (!response.ok) {
    throw new Error(`Sync failed: ${response.status}`);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// CACHE MANAGEMENT
// ─────────────────────────────────────────────────────────────────────────────

export async function cacheData(
  key: string,
  data: unknown,
  sphereId: SphereId | null = null,
  ttlMinutes: number = 60
): Promise<void> {
  const database = await getDB();
  const expiresAt = new Date(Date.now() + ttlMinutes * 60 * 1000);
  
  await database.put('cache', {
    key,
    data,
    sphereId,
    expiresAt,
  });
}

export async function getCachedData<T>(key: string): Promise<T | null> {
  const database = await getDB();
  const cached = await database.get('cache', key);
  
  if (!cached) return null;
  if (new Date() > cached.expiresAt) {
    await database.delete('cache', key);
    return null;
  }
  
  return cached.data as T;
}

export async function clearExpiredCache(): Promise<number> {
  const database = await getDB();
  const now = new Date();
  const expired = await database.getAllFromIndex('cache', 'by-expires');
  
  let cleared = 0;
  for (const item of expired) {
    if (item.expiresAt < now) {
      await database.delete('cache', item.key);
      cleared++;
    }
  }
  
  return cleared;
}

// ─────────────────────────────────────────────────────────────────────────────
// STATE REPORTING
// ─────────────────────────────────────────────────────────────────────────────

export async function getOfflineState(): Promise<OfflineState> {
  const database = await getDB();
  const pendingOps = await database.getAll('pendingOperations');
  const allData = await database.getAll('sphereData');
  const syncLogs = await database.getAllFromIndex('syncLog', 'by-timestamp');
  
  // Calculate sphere breakdown
  const sphereBreakdown: Record<SphereId, number> = {} as Record<SphereId, number>;
  for (const item of allData) {
    sphereBreakdown[item.sphereId] = (sphereBreakdown[item.sphereId] || 0) + 1;
  }
  
  // Get last online timestamp
  const lastSuccessfulSync = syncLogs
    .filter(log => log.status === 'success')
    .pop();
  
  const cachedInfo: CachedDataInfo = {
    totalSize: JSON.stringify(allData).length,
    itemCount: allData.length,
    oldestItem: allData.length > 0 
      ? new Date(Math.min(...allData.map(d => d.createdAt.getTime())))
      : null,
    newestItem: allData.length > 0
      ? new Date(Math.max(...allData.map(d => d.updatedAt.getTime())))
      : null,
    sphereBreakdown,
  };
  
  return {
    isOnline,
    lastOnline: lastSuccessfulSync?.timestamp ?? null,
    pendingOperations: pendingOps,
    cachedData: cachedInfo,
    syncProgress: 0,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// DATABASE MANAGEMENT
// ─────────────────────────────────────────────────────────────────────────────

export async function clearAllData(): Promise<void> {
  const database = await getDB();
  await database.clear('sphereData');
  await database.clear('pendingOperations');
  await database.clear('syncLog');
  await database.clear('cache');
}

export async function exportAllData(): Promise<string> {
  const database = await getDB();
  const data = {
    sphereData: await database.getAll('sphereData'),
    pendingOperations: await database.getAll('pendingOperations'),
    exportedAt: new Date().toISOString(),
  };
  return JSON.stringify(data, null, 2);
}

export async function importData(jsonData: string): Promise<boolean> {
  try {
    const data = JSON.parse(jsonData);
    const database = await getDB();
    
    for (const item of data.sphereData || []) {
      await database.put('sphereData', item);
    }
    
    for (const op of data.pendingOperations || []) {
      await database.put('pendingOperations', op);
    }
    
    return true;
  } catch {
    return false;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// SERVICE EXPORT
// ─────────────────────────────────────────────────────────────────────────────

export const OfflineService = {
  // Network
  onNetworkChange,
  getOnlineStatus,
  
  // Data operations
  saveData,
  updateData,
  deleteData,
  getData,
  getDataBySphere,
  
  // Pending operations
  getPendingOperations,
  getPendingCount,
  
  // Sync
  syncPendingOperations,
  onSyncProgress,
  
  // Cache
  cacheData,
  getCachedData,
  clearExpiredCache,
  
  // State
  getOfflineState,
  
  // Database management
  clearAllData,
  exportAllData,
  importData,
};

export default OfflineService;
