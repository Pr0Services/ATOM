// ═══════════════════════════════════════════════════════════════════════════
// AT·OM REAL-TIME SERVICES
// WebSocket, Heartbeat (4.44s cycle), and Arithmos Engine
// ═══════════════════════════════════════════════════════════════════════════

import { io, Socket } from 'socket.io-client';
import type {
  SphereId,
  WebSocketMessage,
  WebSocketEventType,
  HeartbeatState,
  HeartbeatPayload,
  SphereHeartbeat,
  ArithmosState,
  ArithmosRecommendation,
  SystemAlert,
} from '@/types';

// ═══════════════════════════════════════════════════════════════════════════
// WEBSOCKET SERVICE
// ═══════════════════════════════════════════════════════════════════════════

type MessageHandler<T = unknown> = (message: WebSocketMessage<T>) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private handlers: Map<WebSocketEventType, Set<MessageHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  
  private connectionListeners: Set<(connected: boolean) => void> = new Set();

  connect(url: string, token?: string): void {
    if (this.socket?.connected) return;

    this.socket = io(url, {
      auth: token ? { token } : undefined,
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: this.reconnectDelay,
    });

    this.setupListeners();
  }

  private setupListeners(): void {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('[WS] Connected');
      this.reconnectAttempts = 0;
      this.notifyConnectionChange(true);
    });

    this.socket.on('disconnect', (reason) => {
      console.log('[WS] Disconnected:', reason);
      this.notifyConnectionChange(false);
    });

    this.socket.on('connect_error', (error) => {
      console.error('[WS] Connection error:', error);
      this.reconnectAttempts++;
    });

    // Handle incoming messages
    this.socket.on('message', (message: WebSocketMessage) => {
      this.dispatchMessage(message);
    });

    // Handle specific event types
    const eventTypes: WebSocketEventType[] = [
      'heartbeat',
      'sphere_update',
      'balance_change',
      'sync_complete',
      'alert',
      'notification',
    ];

    eventTypes.forEach((eventType) => {
      this.socket?.on(eventType, (payload: unknown) => {
        const message: WebSocketMessage = {
          type: eventType,
          payload,
          timestamp: Date.now(),
          id: crypto.randomUUID(),
        };
        this.dispatchMessage(message);
      });
    });
  }

  private dispatchMessage(message: WebSocketMessage): void {
    const handlers = this.handlers.get(message.type);
    if (handlers) {
      handlers.forEach((handler) => handler(message));
    }
  }

  private notifyConnectionChange(connected: boolean): void {
    this.connectionListeners.forEach((listener) => listener(connected));
  }

  subscribe<T>(eventType: WebSocketEventType, handler: MessageHandler<T>): () => void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }
    this.handlers.get(eventType)!.add(handler as MessageHandler);

    return () => {
      this.handlers.get(eventType)?.delete(handler as MessageHandler);
    };
  }

  onConnectionChange(listener: (connected: boolean) => void): () => void {
    this.connectionListeners.add(listener);
    return () => this.connectionListeners.delete(listener);
  }

  send(eventType: string, payload: unknown): void {
    if (this.socket?.connected) {
      this.socket.emit(eventType, payload);
    } else {
      console.warn('[WS] Cannot send, not connected');
    }
  }

  disconnect(): void {
    this.socket?.disconnect();
    this.socket = null;
  }

  isConnected(): boolean {
    return this.socket?.connected ?? false;
  }
}

export const websocketService = new WebSocketService();

// ═══════════════════════════════════════════════════════════════════════════
// HEARTBEAT SERVICE (4.44s Cycle)
// ═══════════════════════════════════════════════════════════════════════════

const HEARTBEAT_INTERVAL = 4440; // 4.44 seconds in ms

class HeartbeatService {
  private state: HeartbeatState = {
    isConnected: false,
    lastBeat: null,
    cycleNumber: 0,
    systemStability: 100,
    systemEfficiency: 100,
    sphereStatus: {} as Record<SphereId, SphereHeartbeat>,
  };

  private listeners: Set<(state: HeartbeatState) => void> = new Set();
  private intervalId: number | null = null;
  private wsUnsubscribe: (() => void) | null = null;

  start(): void {
    // Subscribe to WebSocket heartbeats
    this.wsUnsubscribe = websocketService.subscribe<HeartbeatPayload>(
      'heartbeat',
      (message) => this.handleHeartbeat(message.payload as HeartbeatPayload)
    );

    // Local heartbeat for offline mode
    this.intervalId = window.setInterval(() => {
      if (!websocketService.isConnected()) {
        this.generateLocalHeartbeat();
      }
    }, HEARTBEAT_INTERVAL);

    console.log('[Heartbeat] Service started (4.44s cycle)');
  }

  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.wsUnsubscribe?.();
    console.log('[Heartbeat] Service stopped');
  }

  private handleHeartbeat(payload: HeartbeatPayload): void {
    this.state = {
      isConnected: true,
      lastBeat: new Date(payload.timestamp),
      cycleNumber: payload.cycle,
      systemStability: payload.stability,
      systemEfficiency: payload.efficiency,
      sphereStatus: payload.spheres.reduce(
        (acc, sphere) => ({ ...acc, [sphere.sphereId]: sphere }),
        {} as Record<SphereId, SphereHeartbeat>
      ),
    };

    this.notifyListeners();
  }

  private generateLocalHeartbeat(): void {
    this.state = {
      ...this.state,
      isConnected: false,
      lastBeat: new Date(),
      cycleNumber: this.state.cycleNumber + 1,
      // Maintain last known stability/efficiency in offline mode
    };

    this.notifyListeners();
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener(this.state));
  }

  subscribe(listener: (state: HeartbeatState) => void): () => void {
    this.listeners.add(listener);
    // Immediately send current state
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  getState(): HeartbeatState {
    return { ...this.state };
  }

  getCycleNumber(): number {
    return this.state.cycleNumber;
  }

  getStability(): number {
    return this.state.systemStability;
  }

  getEfficiency(): number {
    return this.state.systemEfficiency;
  }

  getSphereStatus(sphereId: SphereId): SphereHeartbeat | null {
    return this.state.sphereStatus[sphereId] ?? null;
  }
}

export const heartbeatService = new HeartbeatService();

// ═══════════════════════════════════════════════════════════════════════════
// ARITHMOS ENGINE (Balance Calculation)
// ═══════════════════════════════════════════════════════════════════════════

const SPHERE_WEIGHTS: Record<SphereId, number> = {
  health: 0.15,
  finance: 0.12,
  education: 0.10,
  governance: 0.08,
  energy: 0.10,
  communication: 0.10,
  justice: 0.08,
  logistics: 0.09,
  food: 0.10,
  technology: 0.08,
};

class ArithmosService {
  private state: ArithmosState = {
    globalBalance: 0,
    sphereBalances: {} as Record<SphereId, number>,
    harmonicIndex: 0,
    lastCalculation: new Date(),
    recommendations: [],
  };

  private listeners: Set<(state: ArithmosState) => void> = new Set();
  private wsUnsubscribe: (() => void) | null = null;

  start(): void {
    // Subscribe to WebSocket balance updates
    this.wsUnsubscribe = websocketService.subscribe<ArithmosState>(
      'balance_change',
      (message) => this.handleBalanceUpdate(message.payload as ArithmosState)
    );

    // Subscribe to heartbeat for local calculations
    heartbeatService.subscribe((heartbeat) => {
      if (!websocketService.isConnected()) {
        this.calculateLocalBalance(heartbeat);
      }
    });

    console.log('[Arithmos] Engine started');
  }

  stop(): void {
    this.wsUnsubscribe?.();
    console.log('[Arithmos] Engine stopped');
  }

  private handleBalanceUpdate(payload: ArithmosState): void {
    this.state = {
      ...payload,
      lastCalculation: new Date(),
    };
    this.notifyListeners();
  }

  private calculateLocalBalance(heartbeat: HeartbeatState): void {
    // Calculate sphere balances from heartbeat data
    const sphereBalances: Record<SphereId, number> = {} as Record<SphereId, number>;
    
    Object.entries(heartbeat.sphereStatus).forEach(([sphereId, status]) => {
      // Balance = weighted average of stability and efficiency
      const balance = status.stability * 0.6 + status.efficiency * 0.4;
      sphereBalances[sphereId as SphereId] = Math.round(balance);
    });

    // Calculate global balance using weights
    let globalBalance = 0;
    Object.entries(sphereBalances).forEach(([sphereId, balance]) => {
      const weight = SPHERE_WEIGHTS[sphereId as SphereId] || 0.1;
      globalBalance += balance * weight;
    });

    // Calculate harmonic index (measure of balance across spheres)
    const values = Object.values(sphereBalances);
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
    const harmonicIndex = Math.max(0, 100 - Math.sqrt(variance));

    // Generate recommendations
    const recommendations = this.generateRecommendations(sphereBalances);

    this.state = {
      globalBalance: Math.round(globalBalance),
      sphereBalances,
      harmonicIndex: Math.round(harmonicIndex),
      lastCalculation: new Date(),
      recommendations,
    };

    this.notifyListeners();
  }

  private generateRecommendations(balances: Record<SphereId, number>): ArithmosRecommendation[] {
    const recommendations: ArithmosRecommendation[] = [];
    
    // Find spheres that need attention
    Object.entries(balances).forEach(([sphereId, balance]) => {
      if (balance < 50) {
        recommendations.push({
          id: crypto.randomUUID(),
          priority: balance < 30 ? 'high' : 'medium',
          sphereId: sphereId as SphereId,
          action: `Improve ${sphereId} balance - currently at ${balance}%`,
          impact: 100 - balance,
          estimatedTime: balance < 30 ? '1-2 days' : '1 week',
        });
      }
    });

    // Sort by priority and impact
    return recommendations
      .sort((a, b) => {
        if (a.priority !== b.priority) {
          return a.priority === 'high' ? -1 : b.priority === 'high' ? 1 : 0;
        }
        return b.impact - a.impact;
      })
      .slice(0, 5);
  }

  subscribe(listener: (state: ArithmosState) => void): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener(this.state));
  }

  getState(): ArithmosState {
    return { ...this.state };
  }

  getGlobalBalance(): number {
    return this.state.globalBalance;
  }

  getSphereBalance(sphereId: SphereId): number {
    return this.state.sphereBalances[sphereId] ?? 0;
  }

  getHarmonicIndex(): number {
    return this.state.harmonicIndex;
  }

  getRecommendations(): ArithmosRecommendation[] {
    return [...this.state.recommendations];
  }

  // Manual recalculation trigger
  async recalculate(): Promise<ArithmosState> {
    if (websocketService.isConnected()) {
      websocketService.send('arithmos_recalculate', {});
    } else {
      const heartbeat = heartbeatService.getState();
      this.calculateLocalBalance(heartbeat);
    }
    return this.state;
  }
}

export const arithmosService = new ArithmosService();

// ═══════════════════════════════════════════════════════════════════════════
// ALERT SERVICE
// ═══════════════════════════════════════════════════════════════════════════

class AlertService {
  private alerts: SystemAlert[] = [];
  private listeners: Set<(alerts: SystemAlert[]) => void> = new Set();

  start(): void {
    websocketService.subscribe<SystemAlert>('alert', (message) => {
      this.addAlert(message.payload as SystemAlert);
    });
  }

  addAlert(alert: SystemAlert): void {
    this.alerts = [alert, ...this.alerts].slice(0, 100); // Keep last 100
    this.notifyListeners();
  }

  acknowledgeAlert(id: string): void {
    this.alerts = this.alerts.map((alert) =>
      alert.id === id ? { ...alert, acknowledged: true } : alert
    );
    this.notifyListeners();
  }

  clearAlert(id: string): void {
    this.alerts = this.alerts.filter((alert) => alert.id !== id);
    this.notifyListeners();
  }

  getAlerts(): SystemAlert[] {
    return [...this.alerts];
  }

  getUnacknowledged(): SystemAlert[] {
    return this.alerts.filter((alert) => !alert.acknowledged);
  }

  subscribe(listener: (alerts: SystemAlert[]) => void): () => void {
    this.listeners.add(listener);
    listener(this.alerts);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(): void {
    this.listeners.forEach((listener) => listener(this.alerts));
  }
}

export const alertService = new AlertService();

// ═══════════════════════════════════════════════════════════════════════════
// UNIFIED REAL-TIME MANAGER
// ═══════════════════════════════════════════════════════════════════════════

export function initializeRealTimeServices(wsUrl: string, token?: string): void {
  websocketService.connect(wsUrl, token);
  heartbeatService.start();
  arithmosService.start();
  alertService.start();
  
  console.log('[RealTime] All services initialized');
}

export function shutdownRealTimeServices(): void {
  heartbeatService.stop();
  arithmosService.stop();
  websocketService.disconnect();
  
  console.log('[RealTime] All services shut down');
}

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

export {
  WebSocketService,
  HeartbeatService,
  ArithmosService,
  AlertService,
};
