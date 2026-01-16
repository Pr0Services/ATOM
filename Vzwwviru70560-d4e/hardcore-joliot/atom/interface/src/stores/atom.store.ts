// ═══════════════════════════════════════════════════════════════════════════
// AT·OM INTERFACE - ZUSTAND STORE
// Centralized state management with persistence
// ═══════════════════════════════════════════════════════════════════════════

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type {
  SphereId,
  Sphere,
  SplitIdentity,
  HeartbeatState,
  ArithmosState,
  OfflineState,
  UIState,
  Notification,
  SystemAlert,
  ApiConnection,
} from '@/types';

// ─────────────────────────────────────────────────────────────────────────────
// SPHERE CONFIGURATION
// ─────────────────────────────────────────────────────────────────────────────

export const SPHERE_CONFIG: Record<SphereId, {
  name: string;
  icon: string;
  color: string;
  description: string;
}> = {
  health: {
    name: 'Santé',
    icon: 'Heart',
    color: '#10b981',
    description: 'Gestion de la santé personnelle et bien-être',
  },
  finance: {
    name: 'Finance',
    icon: 'Wallet',
    color: '#f59e0b',
    description: 'Gestion financière et patrimoine',
  },
  education: {
    name: 'Éducation',
    icon: 'GraduationCap',
    color: '#8b5cf6',
    description: 'Formation continue et apprentissage',
  },
  governance: {
    name: 'Gouvernance',
    icon: 'Building2',
    color: '#3b82f6',
    description: 'Administration et documents officiels',
  },
  energy: {
    name: 'Énergie',
    icon: 'Zap',
    color: '#ef4444',
    description: 'Gestion énergétique et ressources',
  },
  communication: {
    name: 'Communication',
    icon: 'MessageCircle',
    color: '#06b6d4',
    description: 'Réseaux et interactions sociales',
  },
  justice: {
    name: 'Justice',
    icon: 'Scale',
    color: '#6366f1',
    description: 'Aspects légaux et droits',
  },
  logistics: {
    name: 'Logistique',
    icon: 'Truck',
    color: '#f97316',
    description: 'Transport et organisation',
  },
  food: {
    name: 'Alimentation',
    icon: 'Utensils',
    color: '#22c55e',
    description: 'Nutrition et approvisionnement',
  },
  technology: {
    name: 'Technologie',
    icon: 'Cpu',
    color: '#a855f7',
    description: 'Outils numériques et innovation',
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// INITIAL SPHERE STATE
// ─────────────────────────────────────────────────────────────────────────────

function createInitialSphere(id: SphereId): Sphere {
  const config = SPHERE_CONFIG[id];
  return {
    id,
    name: config.name,
    description: config.description,
    icon: config.icon,
    color: config.color,
    stability: 100,
    efficiency: 100,
    lastSync: null,
    isActive: true,
    apiConnections: [],
    metrics: {
      totalItems: 0,
      activeItems: 0,
      pendingActions: 0,
      healthScore: 100,
      trendDirection: 'stable',
      lastUpdate: new Date(),
    },
  };
}

function createInitialSpheres(): Record<SphereId, Sphere> {
  const sphereIds: SphereId[] = [
    'health', 'finance', 'education', 'governance', 'energy',
    'communication', 'justice', 'logistics', 'food', 'technology',
  ];
  
  return sphereIds.reduce((acc, id) => {
    acc[id] = createInitialSphere(id);
    return acc;
  }, {} as Record<SphereId, Sphere>);
}

// ─────────────────────────────────────────────────────────────────────────────
// STORE INTERFACE
// ─────────────────────────────────────────────────────────────────────────────

interface AtomStore {
  // Identity
  identity: SplitIdentity | null;
  isAuthenticated: boolean;
  setIdentity: (identity: SplitIdentity | null) => void;
  
  // Spheres
  spheres: Record<SphereId, Sphere>;
  activeSphere: SphereId | null;
  setActiveSphere: (sphereId: SphereId | null) => void;
  updateSphere: (sphereId: SphereId, data: Partial<Sphere>) => void;
  addApiConnection: (sphereId: SphereId, connection: ApiConnection) => void;
  removeApiConnection: (sphereId: SphereId, connectionId: string) => void;
  
  // Heartbeat
  heartbeat: HeartbeatState;
  updateHeartbeat: (state: HeartbeatState) => void;
  
  // Arithmos
  arithmos: ArithmosState;
  updateArithmos: (state: ArithmosState) => void;
  
  // Offline
  offline: OfflineState;
  updateOffline: (state: Partial<OfflineState>) => void;
  
  // UI
  ui: UIState;
  setTheme: (theme: UIState['theme']) => void;
  toggleSidebar: () => void;
  openModal: (modal: UIState['modalStack'][0]) => void;
  closeModal: (id?: string) => void;
  toggleCommandPalette: () => void;
  
  // Notifications
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  dismissNotification: (id: string) => void;
  markNotificationRead: (id: string) => void;
  clearNotifications: () => void;
  
  // Alerts
  alerts: SystemAlert[];
  addAlert: (alert: Omit<SystemAlert, 'id' | 'timestamp' | 'acknowledged'>) => void;
  acknowledgeAlert: (id: string) => void;
  clearAlert: (id: string) => void;
  
  // Reset
  reset: () => void;
}

// ─────────────────────────────────────────────────────────────────────────────
// INITIAL STATE
// ─────────────────────────────────────────────────────────────────────────────

const initialHeartbeat: HeartbeatState = {
  isConnected: false,
  lastBeat: null,
  cycleNumber: 0,
  systemStability: 100,
  systemEfficiency: 100,
  sphereStatus: {} as Record<SphereId, any>,
};

const initialArithmos: ArithmosState = {
  globalBalance: 0,
  sphereBalances: {} as Record<SphereId, number>,
  harmonicIndex: 0,
  lastCalculation: new Date(),
  recommendations: [],
};

const initialOffline: OfflineState = {
  isOnline: true,
  lastOnline: null,
  pendingOperations: [],
  cachedData: {
    totalSize: 0,
    itemCount: 0,
    oldestItem: null,
    newestItem: null,
    sphereBreakdown: {} as Record<SphereId, number>,
  },
  syncProgress: 0,
};

const initialUI: UIState = {
  theme: 'dark',
  sidebarOpen: true,
  activeSphere: null,
  modalStack: [],
  notifications: [],
  commandPaletteOpen: false,
};

// ─────────────────────────────────────────────────────────────────────────────
// STORE IMPLEMENTATION
// ─────────────────────────────────────────────────────────────────────────────

export const useAtomStore = create<AtomStore>()(
  persist(
    (set, get) => ({
      // ═══════════════════════════════════════════════════════════════════
      // IDENTITY
      // ═══════════════════════════════════════════════════════════════════
      identity: null,
      isAuthenticated: false,
      
      setIdentity: (identity) =>
        set({
          identity,
          isAuthenticated: identity !== null,
        }),

      // ═══════════════════════════════════════════════════════════════════
      // SPHERES
      // ═══════════════════════════════════════════════════════════════════
      spheres: createInitialSpheres(),
      activeSphere: null,
      
      setActiveSphere: (sphereId) =>
        set({ activeSphere: sphereId }),
      
      updateSphere: (sphereId, data) =>
        set((state) => ({
          spheres: {
            ...state.spheres,
            [sphereId]: {
              ...state.spheres[sphereId],
              ...data,
            },
          },
        })),
      
      addApiConnection: (sphereId, connection) =>
        set((state) => ({
          spheres: {
            ...state.spheres,
            [sphereId]: {
              ...state.spheres[sphereId],
              apiConnections: [...state.spheres[sphereId].apiConnections, connection],
            },
          },
        })),
      
      removeApiConnection: (sphereId, connectionId) =>
        set((state) => ({
          spheres: {
            ...state.spheres,
            [sphereId]: {
              ...state.spheres[sphereId],
              apiConnections: state.spheres[sphereId].apiConnections.filter(
                (c) => c.id !== connectionId
              ),
            },
          },
        })),

      // ═══════════════════════════════════════════════════════════════════
      // HEARTBEAT
      // ═══════════════════════════════════════════════════════════════════
      heartbeat: initialHeartbeat,
      
      updateHeartbeat: (state) =>
        set({ heartbeat: state }),

      // ═══════════════════════════════════════════════════════════════════
      // ARITHMOS
      // ═══════════════════════════════════════════════════════════════════
      arithmos: initialArithmos,
      
      updateArithmos: (state) =>
        set({ arithmos: state }),

      // ═══════════════════════════════════════════════════════════════════
      // OFFLINE
      // ═══════════════════════════════════════════════════════════════════
      offline: initialOffline,
      
      updateOffline: (state) =>
        set((prev) => ({
          offline: { ...prev.offline, ...state },
        })),

      // ═══════════════════════════════════════════════════════════════════
      // UI
      // ═══════════════════════════════════════════════════════════════════
      ui: initialUI,
      
      setTheme: (theme) =>
        set((state) => ({
          ui: { ...state.ui, theme },
        })),
      
      toggleSidebar: () =>
        set((state) => ({
          ui: { ...state.ui, sidebarOpen: !state.ui.sidebarOpen },
        })),
      
      openModal: (modal) =>
        set((state) => ({
          ui: { ...state.ui, modalStack: [...state.ui.modalStack, modal] },
        })),
      
      closeModal: (id) =>
        set((state) => ({
          ui: {
            ...state.ui,
            modalStack: id
              ? state.ui.modalStack.filter((m) => m.id !== id)
              : state.ui.modalStack.slice(0, -1),
          },
        })),
      
      toggleCommandPalette: () =>
        set((state) => ({
          ui: { ...state.ui, commandPaletteOpen: !state.ui.commandPaletteOpen },
        })),

      // ═══════════════════════════════════════════════════════════════════
      // NOTIFICATIONS
      // ═══════════════════════════════════════════════════════════════════
      addNotification: (notification) =>
        set((state) => ({
          ui: {
            ...state.ui,
            notifications: [
              {
                ...notification,
                id: crypto.randomUUID(),
                timestamp: new Date(),
                read: false,
              },
              ...state.ui.notifications,
            ].slice(0, 50), // Keep last 50
          },
        })),
      
      dismissNotification: (id) =>
        set((state) => ({
          ui: {
            ...state.ui,
            notifications: state.ui.notifications.filter((n) => n.id !== id),
          },
        })),
      
      markNotificationRead: (id) =>
        set((state) => ({
          ui: {
            ...state.ui,
            notifications: state.ui.notifications.map((n) =>
              n.id === id ? { ...n, read: true } : n
            ),
          },
        })),
      
      clearNotifications: () =>
        set((state) => ({
          ui: { ...state.ui, notifications: [] },
        })),

      // ═══════════════════════════════════════════════════════════════════
      // ALERTS
      // ═══════════════════════════════════════════════════════════════════
      alerts: [],
      
      addAlert: (alert) =>
        set((state) => ({
          alerts: [
            {
              ...alert,
              id: crypto.randomUUID(),
              timestamp: new Date(),
              acknowledged: false,
            },
            ...state.alerts,
          ].slice(0, 100),
        })),
      
      acknowledgeAlert: (id) =>
        set((state) => ({
          alerts: state.alerts.map((a) =>
            a.id === id ? { ...a, acknowledged: true } : a
          ),
        })),
      
      clearAlert: (id) =>
        set((state) => ({
          alerts: state.alerts.filter((a) => a.id !== id),
        })),

      // ═══════════════════════════════════════════════════════════════════
      // RESET
      // ═══════════════════════════════════════════════════════════════════
      reset: () =>
        set({
          identity: null,
          isAuthenticated: false,
          spheres: createInitialSpheres(),
          activeSphere: null,
          heartbeat: initialHeartbeat,
          arithmos: initialArithmos,
          offline: initialOffline,
          ui: initialUI,
          alerts: [],
        }),
    }),
    {
      name: 'atom-store',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        // Only persist these fields
        ui: { theme: state.ui.theme, sidebarOpen: state.ui.sidebarOpen },
        spheres: state.spheres,
      }),
    }
  )
);

// ─────────────────────────────────────────────────────────────────────────────
// SELECTORS
// ─────────────────────────────────────────────────────────────────────────────

export const selectSphere = (sphereId: SphereId) => (state: AtomStore) =>
  state.spheres[sphereId];

export const selectActiveSphere = (state: AtomStore) =>
  state.activeSphere ? state.spheres[state.activeSphere] : null;

export const selectUnreadNotifications = (state: AtomStore) =>
  state.ui.notifications.filter((n) => !n.read);

export const selectUnacknowledgedAlerts = (state: AtomStore) =>
  state.alerts.filter((a) => !a.acknowledged);

export const selectGlobalBalance = (state: AtomStore) =>
  state.arithmos.globalBalance;

export const selectSystemStatus = (state: AtomStore) => ({
  stability: state.heartbeat.systemStability,
  efficiency: state.heartbeat.systemEfficiency,
  isConnected: state.heartbeat.isConnected,
  isOnline: state.offline.isOnline,
});

// ─────────────────────────────────────────────────────────────────────────────
// HOOKS
// ─────────────────────────────────────────────────────────────────────────────

export function useSphere(sphereId: SphereId) {
  return useAtomStore(selectSphere(sphereId));
}

export function useActiveSphere() {
  return useAtomStore(selectActiveSphere);
}

export function useSystemStatus() {
  return useAtomStore(selectSystemStatus);
}

export default useAtomStore;
